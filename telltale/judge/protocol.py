"""What the judge is asked, and what the code does with the answer.

The judge never scores anything. It is used twice, both times as an extractor:

    stage 1  EXTRACTION     passage        -> verbatim candidate quotes
    stage 2  ADJUDICATION   quote+context  -> which rubric criteria hold

Everything between and after those two calls is arithmetic in this package. The
reason is not distrust of any particular model; it is that a holistic rating is
unfalsifiable. "This document scores 0.7 on rule-of-three" cannot be checked by
a reader, cannot be diffed between runs, and cannot be argued with. A list of
quotes, each with the rubric letters that were found to hold, can be checked
line by line — and when the judge and the code disagree, the disagreement is
recorded rather than averaged away.

Three consequences run through this file:

* **Extraction is recall-first.** The stage-1 prompt asks for over-extraction,
  including borderline candidates, because a span the judge never quotes can
  never be adjudicated. Precision is stage 2's job, and stage 2 is cheap per
  span; a missed span is unrecoverable.
* **Quotes must be real.** `verify_quote` requires a whitespace-normalized
  substring match against the exact text the judge was shown. A quote that does
  not match is dropped and counted as a hallucination — never silently repaired,
  because a repaired quote is evidence the judge did not actually produce.
* **The decision rule lives here, not in the model.** `RULES` mirrors each
  rubric's own (a)/(b)/(x) labels, and `span_counts` applies them. The judge's
  own `instance` flag is recorded for audit and is not consulted.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

from telltale import textstats
from telltale.corpus import Doc
from telltale.registry import Tell

#: Bumped when a prompt, a decision rule, or the chunking changes — the version
#: of the instrument as a whole, recorded on every detection. What the *cache*
#: keys on is `PROMPT_VERSION` below, which moves only when the model-facing
#: question moves; the two were the same number until v3.
#:
#: v2 (2026-07-29) made two changes, both found by the first live calibration
#: round:
#:
#:  1. Stage 1 no longer sees the rubric's exclusions — only its inclusion
#:     criteria, plus a standing instruction not to apply exclusions at all.
#:     Under v1 the extractor sometimes applied them itself and sometimes did
#:     not: one direct-address negative never surfaced a candidate while another
#:     reached stage 2 and was correctly excluded there. That made exclusion
#:     coverage a property of the extractor's mood, and left adjudication
#:     unexercised on exactly the cases the calibration gate exists to test.
#:     Span tells only — see `build_structural_prompt` for why the doc-level
#:     tells keep the whole rubric.
#:  2. `skeleton_view` labels the closing paragraph. The skeleton renders the
#:     last paragraph twice — once as a `PARA:` line, once in full — which made
#:     any final sentence look like it recurred at the end, and pulled
#:     `str.summary-sandwich` toward finding a closing recap that was not there.
#:
#: v3 (2026-08-02) added code-side structural disposition and the adjudication
#: cap. Neither changes a prompt, so every EXTRACTION and STRUCTURAL answer in
#: the cache is still the answer to the same question — but what the code does
#: with a stage-1 answer changed, and a detection produced under v2 is not
#: comparable with one produced under v3. See `structural_exclusion_for`.
PROTOCOL_VERSION = 3

#: What the judge is *asked*, versioned separately from the instrument as a
#: whole — and it is this, not `PROTOCOL_VERSION`, that the cache keys on.
#:
#: The two were one number through v2 because every change so far had been a
#: change to a prompt. v3 is the first that is not: the structural disposition
#: and the adjudication cap are decisions the code makes about answers the judge
#: already gave, and the extraction prompt, the adjudication prompt, the
#: structural prompt and the chunking are all byte-identical to v2. Keying the
#: cache on the instrument version would have thrown away ~3,500 paid-for
#: answers to questions that did not change, which is the cost this task exists
#: to reduce. Any future change to a prompt, to the chunker, or to the rubric
#: split must bump BOTH — the cache is only safe while this number covers
#: everything the model sees.
PROMPT_VERSION = 2

TARGET_WORDS = 2500
OVERLAP_WORDS = 150

#: Context handed to stage 2 around a span, in sentences either side.
CONTEXT_SENTENCES = 2
#: Fallback context window when the span cannot be located in a sentence list.
CONTEXT_CHARS = 400


# --- rubric labels -----------------------------------------------------------

_LABEL_LINE = re.compile(r"^\(([a-z])\)", re.MULTILINE)
_EXCLUSION_HEAD = re.compile(r"^EXCLUSIONS:", re.MULTILINE)
_EVIDENCE_HEAD = re.compile(r"^Evidence to extract:", re.MULTILINE)


def split_rubric(rubric: str) -> tuple[str, str, str]:
    """A rubric cut into (inclusion criteria, exclusions, evidence-to-extract).

    Every rubric in the registry is written in the same three parts, and the two
    headings that separate them are load-bearing rather than decorative: stage 1
    is shown the first and third parts only, so that it proposes candidates on
    the inclusion shape alone and leaves every exclusion to the adjudicator.
    A rubric with no EXCLUSIONS heading comes back whole in the first slot,
    which degrades to v1 behaviour rather than silently dropping its text.
    """
    text = rubric or ""
    head = _EXCLUSION_HEAD.search(text)
    if not head:
        return text, "", ""
    inclusion = text[: head.start()]
    evidence_at = _EVIDENCE_HEAD.search(text, head.end())
    if evidence_at:
        return inclusion, text[head.start() : evidence_at.start()], text[evidence_at.start() :]
    return inclusion, text[head.start() :], ""


def parse_rubric_labels(rubric: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """The (a)/(b)/... criterion letters and the (x)/(y)/... exclusion letters.

    Read out of the rubric text itself so the table below can be tested against
    the registry rather than trusted. Labels are recognized only at the start of
    a line, which is where a rubric writes them; a letter in parentheses inside a
    sentence ("criterion (c) holds") is prose, not a label.
    """
    text = rubric or ""
    split = _EXCLUSION_HEAD.search(text)
    head = text[: split.start()] if split else text
    tail = text[split.end() :] if split else ""
    return (
        tuple(dict.fromkeys(_LABEL_LINE.findall(head))),
        tuple(dict.fromkeys(_LABEL_LINE.findall(tail))),
    )


def normalize_label(label: Any) -> str:
    """"(a)", "a.", "A", "criterion a" -> "a". Anything unreadable -> ""."""
    match = re.search(r"[A-Za-z]", str(label or ""))
    return match.group(0).lower() if match else ""


# --- the decision table ------------------------------------------------------


@dataclass(frozen=True)
class TellRule:
    """How one judge tell's rubric turns into a decision, in code.

    `mode` is "all" when the rubric says ALL criteria must hold and "any" when it
    says ANY criterion holds. `required` and `exclusions` mirror the rubric's own
    letters; `test_criteria_table_matches_the_rubrics` reads both and fails if
    they drift apart, which is the only thing keeping this table honest.
    """

    tell_id: str
    kind: str  # "span" | "structural"
    mode: str  # "all" | "any"
    required: tuple[str, ...]
    exclusions: tuple[str, ...]
    #: Structural tells only: the evidence fields the judge is asked to fill.
    evidence_fields: tuple[str, ...] = ()

    any_exclusion_kills: bool = True

    #: Which of this rubric's exclusions can be decided from the *shape of the
    #: line a span sits on*, and which `textstats` line classes decide them.
    #: A span on one of those lines is dispositioned in code and never
    #: adjudicated. Only exclusions that are purely structural belong here: an
    #: exclusion that needs to know what the words mean stays with the judge.
    structural_exclusions: dict[str, tuple[str, ...]] = field(default_factory=dict)

    #: The most spans one chunk may send to adjudication, or None for no limit.
    #: A cap is a last resort — it truncates the measurement — so it is set only
    #: where the extractor's recall-first instruction produces so many spans per
    #: chunk that the cost is unbounded, and it is always reported.
    adjudication_cap: int | None = None


RULES: dict[str, TellRule] = {
    "rht.rule-of-three": TellRule(
        tell_id="rht.rule-of-three",
        kind="span",
        mode="all",
        required=("a", "b", "c"),
        exclusions=("x", "y", "z"),
        # Only (y) is structural: "a list rendered as bullets or numbered items
        # is out of scope here". A table row is not a list and the rubric does
        # not say it is, so table rows keep going to the judge even though it
        # excludes 40 of them under (x) in the cache — mapping (y) onto
        # `table_row` would be the code inventing an exclusion the rubric does
        # not have. (x) enumerative content and (z) quotation are both about
        # what the words mean and stay judge-side.
        structural_exclusions={"y": ("list_item",)},
        # Set to the p90 of the measured post-triage spans-per-chunk
        # distribution over the 167 cached real-corpus chunks (p50 6, p75 8,
        # p90 11, p95 13, max 22). Recall-first extraction on a densely
        # enumerative document proposes triples faster than adjudication can
        # pay for them, and the tail is where the cost lives: capping at 11
        # bounds 14 of 167 chunks and leaves the other 153 untouched.
        adjudication_cap=11,
    ),
    "rht.rhetorical-qa": TellRule(
        tell_id="rht.rhetorical-qa",
        kind="span",
        mode="all",
        required=("a", "b"),
        # (w) was added at rubric v2. The tell targets the essay cadence — a
        # writer asking themselves a question to set up their own answer. A
        # question put to a named colleague in an email is correspondence, and
        # counting it because the sender went on to answer it would make the
        # tell fire on ordinary human writing, which is the one thing a
        # benchmark of AI tells cannot afford to do.
        exclusions=("x", "y", "z", "w"),
    ),
    "rht.fragment-emphasis": TellRule(
        tell_id="rht.fragment-emphasis",
        kind="span",
        mode="all",
        required=("a", "b"),
        exclusions=("x", "y", "z", "w"),
        # Three of this rubric's four exclusions are about where a fragment
        # sits, not what it says, and that is decidable from the line:
        #   (x) "headings, subheadings, and titles ... including bolded run-in
        #       headings"      -> heading
        #   (y) "list items, table cells, and bullet text"
        #                      -> list_item, table_row
        #   (z) "salutations, sign-offs, captions, labels, bylines, dates, and
        #       callout tags"  -> signoff, caption
        # (w) — a fragment inside quoted speech attributed to someone else —
        # is not a line shape and stays with the judge.
        structural_exclusions={
            "x": ("heading",),
            "y": ("list_item", "table_row"),
            "z": ("signoff", "caption"),
        },
    ),
    "rht.from-x-to-y": TellRule(
        tell_id="rht.from-x-to-y",
        kind="span",
        mode="all",
        required=("a", "b", "c"),
        exclusions=("x", "y", "z"),
    ),
    "str.summary-sandwich": TellRule(
        tell_id="str.summary-sandwich",
        kind="structural",
        mode="all",
        required=("a", "b"),
        exclusions=("x",),
        evidence_fields=(
            "opening_preview_quote",
            "closing_recap_quote",
            "closing_new_info_quote",
        ),
    ),
    "str.parallel-bullet-grammar": TellRule(
        tell_id="str.parallel-bullet-grammar",
        kind="structural",
        mode="all",
        required=("a", "b", "c"),
        exclusions=("x", "y", "z"),
        evidence_fields=("lists",),
    ),
    "str.table-overuse": TellRule(
        tell_id="str.table-overuse",
        kind="structural",
        mode="any",
        required=("a", "b", "c"),
        exclusions=("x", "y", "z"),
        evidence_fields=("tables",),
    ),
}


def rule_for(tell: Tell | str) -> TellRule:
    tell_id = tell if isinstance(tell, str) else tell.id
    try:
        return RULES[tell_id]
    except KeyError:
        raise KeyError(
            f"no judge decision rule for {tell_id!r}; add one to protocol.RULES "
            "and mirror the rubric's own criterion labels"
        ) from None


def structural_exclusion_for(rule: TellRule, line_class: str) -> str | None:
    """The rubric letter a span on a `line_class` line is excluded by, or None.

    This is the whole of fix M8d-1, and it is deliberately small. The judge is
    asked nothing here: the rubric already says, in its own words, that a
    heading or a bullet or a sign-off does not qualify, and whether a line is a
    heading is a fact about the markdown rather than a reading of it. Sending
    those spans to adjudication bought a paid-for confirmation of something the
    parser knew — on the cached real-corpus chunks, 51% of every verified
    `rht.fragment-emphasis` span, and the judge agreed with the line class 98%
    of the time on the run-in headings that dominate the count.

    Two properties keep this honest. It can only ever *reject*: a code
    disposition never makes a tell fire, so the failure mode is a lost instance
    rather than an invented one. And it fires only for letters a tell's rule
    explicitly declares, so a tell whose exclusions are semantic — every one of
    them, for `rht.rule-of-three` except (y) — is untouched.
    """
    for letter, classes in (rule.structural_exclusions or {}).items():
        if line_class in classes:
            return letter
    return None


def criteria_satisfied(rule: TellRule, criteria_met: Iterable[Any]) -> bool:
    """Whether the rubric's required criteria hold, by the rubric's own letters."""
    met = {normalize_label(c) for c in (criteria_met or [])}
    met.discard("")
    required = set(rule.required)
    if rule.mode == "any":
        return bool(met & required)
    return required.issubset(met)


def exclusion_fired(rule: TellRule, exclusion_triggered: Any) -> str | None:
    """The exclusion letter that fired, or None.

    A judge that answers "none" / "null" / "" in words rather than JSON null is
    saying no exclusion fired; treating that string as an exclusion letter would
    silently discard real instances.
    """
    if exclusion_triggered is None:
        return None
    raw = str(exclusion_triggered).strip()
    if not raw or raw.lower() in {"none", "null", "n/a", "na", "false", "-"}:
        return None
    letter = normalize_label(raw)
    if letter in rule.exclusions:
        return letter
    # An unrecognized label is still the judge saying an exclusion applies. It
    # is kept as-is rather than dropped: over-counting exclusions costs recall,
    # ignoring one costs precision, and precision is what a tell claim rests on.
    return raw[:40]


def span_counts(rule: TellRule, adjudication: dict[str, Any]) -> tuple[bool, str]:
    """Does this adjudicated span count? Code decides; the judge's flag does not.

    Returns (counts, why-not). The judge's `instance` boolean is recorded by the
    caller for the audit trail and deliberately not consulted here.
    """
    fired = exclusion_fired(rule, adjudication.get("exclusion_triggered"))
    if fired and rule.any_exclusion_kills:
        return False, f"exclusion ({fired})"
    if not criteria_satisfied(rule, adjudication.get("criteria_met")):
        met = sorted(
            {normalize_label(c) for c in (adjudication.get("criteria_met") or [])} - {""}
        )
        need = "any of" if rule.mode == "any" else "all of"
        return False, f"criteria {met or 'none'} do not meet {need} {list(rule.required)}"
    return True, ""


# --- structural decision rules ----------------------------------------------


def _quote(value: Any) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def decide_summary_sandwich(evidence: dict[str, Any]) -> tuple[bool, str]:
    """(a) preview AND (b) recap in a separate section AND NOT (x) new information.

    The separateness test arrived with rubric v2. Twice in live calibration a
    document that simply ended on its last finding was read as having a closing
    recap, because a final sentence that sounds conclusive reads like a summary
    of the section it is the end of. Labelling the skeleton's own repetition
    (protocol v2) was not enough on its own, so the distinction is now asked for
    as evidence and applied here: the judge reports which section the recap sits
    in, and the code decides whether that makes it a recap at all.
    """
    preview = _quote(evidence.get("opening_preview_quote"))
    recap = _quote(evidence.get("closing_recap_quote"))
    new_info = _quote(evidence.get("closing_new_info_quote"))
    if not preview:
        return False, "no opening preview (a)"
    if not recap:
        return False, "no closing recap (b)"
    if "closing_recap_is_separate_section" in evidence and not bool(
        evidence.get("closing_recap_is_separate_section")
    ):
        return False, "the recap is the last substantive section's own content (b)"
    if new_info:
        return False, "closing adds new information (x)"
    return True, "preview (a) + recap (b) in its own section, nothing new in the close"


def _flag(entry: dict[str, Any], *names: str) -> bool:
    return any(bool(entry.get(name)) for name in names)


def decide_parallel_bullets(evidence: dict[str, Any]) -> tuple[bool, str]:
    """One list of 3+ items, one shared opening form, no item breaking it."""
    lists = evidence.get("lists")
    if not isinstance(lists, list):
        return False, "no lists reported"
    for entry in lists:
        if not isinstance(entry, dict):
            continue
        try:
            count = int(entry.get("item_count") or 0)
        except (TypeError, ValueError):
            count = len(entry.get("item_openings") or [])
        if count < 3:
            continue  # (x): a two-item list does not qualify
        if not _quote(entry.get("shared_opening_form")):
            continue  # (b) fails
        if not bool(entry.get("all_items_match")):
            continue  # (c) fails
        if _flag(entry, "single_word_items"):
            continue  # (y)
        if _flag(entry, "procedural_format"):
            continue  # (z)
        where = _quote(entry.get("heading")) or "unnamed list"
        return True, (
            f"{count} items under {where}, all opening as "
            f"{_quote(entry.get('shared_opening_form'))}"
        )
    return False, "no list satisfies (a)+(b)+(c) without an exclusion"


def decide_table_overuse(evidence: dict[str, Any]) -> tuple[bool, str]:
    """Any table meeting (a), (b), or (c) with no exclusion on it."""
    tables = evidence.get("tables")
    if not isinstance(tables, list):
        return False, "no tables reported"
    for entry in tables:
        if not isinstance(entry, dict):
            continue
        criterion = normalize_label(entry.get("criterion"))
        if criterion not in {"a", "b", "c"}:
            continue
        if _flag(entry, "genuine_data_table"):
            continue  # (x)
        if _flag(entry, "crosswalk_or_schedule"):
            continue  # (y)
        if _flag(entry, "required_by_format"):
            continue  # (z)
        return True, f"table meets ({criterion}): {_quote(entry.get('header_row'))[:60]}"
    return False, "no table meets (a), (b), or (c) without an exclusion"


STRUCTURAL_DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, str]]] = {
    "str.summary-sandwich": decide_summary_sandwich,
    "str.parallel-bullet-grammar": decide_parallel_bullets,
    "str.table-overuse": decide_table_overuse,
}


def structural_quotes(tell_id: str, evidence: dict[str, Any]) -> list[tuple[str, str]]:
    """(field-path, quote) pairs from a structural answer, for verification.

    Every quote a structural answer offers is checked the same way a span is.
    A decision built on a quote that is not in the document is a decision built
    on nothing, however plausible the reasoning around it reads.
    """
    out: list[tuple[str, str]] = []
    if tell_id == "str.summary-sandwich":
        for field in RULES[tell_id].evidence_fields:
            quote = _quote(evidence.get(field))
            if quote:
                out.append((field, quote))
    elif tell_id == "str.parallel-bullet-grammar":
        for i, entry in enumerate(evidence.get("lists") or []):
            if not isinstance(entry, dict):
                continue
            for j, opening in enumerate(entry.get("item_openings") or []):
                quote = _quote(opening)
                if quote:
                    out.append((f"lists[{i}].item_openings[{j}]", quote))
    elif tell_id == "str.table-overuse":
        for i, entry in enumerate(evidence.get("tables") or []):
            if not isinstance(entry, dict):
                continue
            for field in ("header_row", "sample_data_row"):
                quote = _quote(entry.get(field))
                if quote:
                    out.append((f"tables[{i}].{field}", quote))
    return out


def prune_unverified(
    tell_id: str, evidence: dict[str, Any], bad_paths: set[str]
) -> dict[str, Any]:
    """Drop every part of a structural answer whose quote did not verify.

    A hallucinated preview quote must not be able to carry criterion (a); a list
    whose item openings are not in the document must not be able to satisfy the
    parallelism rule. Dropping is the conservative direction — it can only turn
    a "present" into an "absent", never the reverse.
    """
    pruned = dict(evidence)
    if tell_id == "str.summary-sandwich":
        for field in RULES[tell_id].evidence_fields:
            if field in bad_paths:
                pruned[field] = None
    elif tell_id == "str.parallel-bullet-grammar":
        kept = []
        for i, entry in enumerate(evidence.get("lists") or []):
            if any(p.startswith(f"lists[{i}].") for p in bad_paths):
                continue
            kept.append(entry)
        pruned["lists"] = kept
    elif tell_id == "str.table-overuse":
        kept = []
        for i, entry in enumerate(evidence.get("tables") or []):
            if f"tables[{i}].header_row" in bad_paths:
                continue
            kept.append(entry)
        pruned["tables"] = kept
    return pruned


# --- chunking ----------------------------------------------------------------

_H2 = re.compile(r"^\s{0,3}##(?!#)\s+")


@dataclass(frozen=True)
class Chunk:
    """One unit of extraction work: a contiguous slice of one document."""

    doc_id: str
    index: int
    text: str
    sha256: str

    @classmethod
    def make(cls, doc_id: str, index: int, text: str) -> "Chunk":
        return cls(
            doc_id=doc_id,
            index=index,
            text=text,
            sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        )


def _sections(text: str) -> list[list[str]]:
    """Split into H2 sections, keeping the preamble as its own section."""
    sections: list[list[str]] = []
    current: list[str] = []
    for line in text.split("\n"):
        if _H2.match(line) and current:
            sections.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append(current)
    return sections


def _split_oversized(lines: list[str], target: int, overlap: int) -> list[list[str]]:
    """Cut one long section into target-sized pieces with an overlapping tail.

    The overlap exists so a tell straddling a cut is not lost: a rhetorical
    question at the end of one piece and its answer at the start of the next is
    invisible to both halves otherwise. It costs double-counting, which the
    caller resolves by deduplicating spans on their normalized quote.
    """
    pieces: list[list[str]] = []
    current: list[str] = []
    words = 0
    carried = 0  # of `words`, how many came from the previous piece's tail
    for line in lines:
        current.append(line)
        words += textstats.word_count(line)
        if words >= target:
            pieces.append(current)
            tail: list[str] = []
            tail_words = 0
            for previous in reversed(current):
                if tail_words >= overlap:
                    break
                tail.insert(0, previous)
                tail_words += textstats.word_count(previous)
            current = list(tail)
            words = tail_words
            carried = tail_words
    # A trailing piece that is nothing but the overlap tail has already been
    # judged as part of the piece before it, so it is dropped rather than sent
    # again: a duplicate chunk is duplicate cost and duplicate spans.
    if current and words > carried:
        pieces.append(current)
    return pieces or [lines]


def chunk_doc(
    doc: Doc | str,
    target_words: int = TARGET_WORDS,
    overlap_words: int = OVERLAP_WORDS,
    doc_id: str = "text",
) -> list[Chunk]:
    """Split a document into chunks on H2 boundaries, packed to `target_words`.

    Sections are the unit, because a tell is a property of a passage and cutting
    mid-argument invents boundaries the writer did not write. Small sections are
    packed together up to the target; a section bigger than the target on its own
    is split with an overlap, which is the only place overlap appears.
    """
    text = doc if isinstance(doc, str) else doc.text
    identifier = doc_id if isinstance(doc, str) else doc.doc_id

    chunks: list[str] = []
    pending: list[str] = []
    pending_words = 0

    def flush() -> None:
        nonlocal pending, pending_words
        if pending and any(line.strip() for line in pending):
            chunks.append("\n".join(pending).strip("\n"))
        pending = []
        pending_words = 0

    for section in _sections(text):
        words = textstats.word_count("\n".join(section))
        if words > target_words:
            flush()
            for piece in _split_oversized(section, target_words, overlap_words):
                body = "\n".join(piece).strip("\n")
                if body.strip():
                    chunks.append(body)
            continue
        if pending and pending_words + words > target_words:
            flush()
        pending.extend(section)
        pending_words += words
    flush()

    if not chunks:
        chunks = [text.strip("\n")]
    return [Chunk.make(identifier, i, body) for i, body in enumerate(chunks)]


# --- the skeleton view -------------------------------------------------------

TABLES_HEADER = "TABLES"
MAX_TABLE_LINES = 200

#: Labels that stop the skeleton's own repetition reading as a closing recap.
LAST_PARAGRAPH_HEADER = "LAST PARAGRAPH"
CLOSING_PARA_NOTE = "   [this is the closing paragraph; it is printed in full below]"
LAST_PARAGRAPH_NOTE = (
    " [the same closing paragraph already listed in the outline above, "
    "reprinted in full — its appearance here is not a second occurrence in the "
    "document]"
)


def _table_blocks(text: str) -> list[list[str]]:
    """Markdown table blocks, verbatim, in document order.

    `textstats.doc_skeleton` drops tables — it is an outline of the prose, and
    tables are not prose. That is right for the other two structural tells and
    fatal for `str.table-overuse`, whose whole evidence base is the table. So the
    skeleton the judge sees carries the tables back, verbatim, in an appendix.
    """
    lines = textstats._drop_code_fences(text.split("\n"))
    blocks: list[list[str]] = []
    i = 0
    while i < len(lines):
        if "|" not in lines[i]:
            i += 1
            continue
        j = i
        while j < len(lines) and "|" in lines[j] and lines[j].strip():
            j += 1
        run = lines[i:j]
        looks_like_table = len(run) >= 2 and (
            any(textstats._TABLE_DELIM.match(line) for line in run)
            or all(line.strip().startswith("|") for line in run)
        )
        if looks_like_table:
            blocks.append(run)
        i = max(j, i + 1)
    return blocks


def _label_closing_paragraph(skeleton: str) -> str:
    """Say plainly that the closing paragraph is shown twice (protocol v2).

    `doc_skeleton` lists every paragraph's first sentence in the outline and
    then prints the first and last paragraphs in full. So the closing paragraph
    always appears twice, and in the first live round that cost a false positive:
    a document that simply ended — no closing section at all — read as a summary
    sandwich, because its final finding looked like it was being restated at the
    end. The repetition is a rendering artifact, so it is labelled here rather
    than worked around in the rubric; teaching a rubric to compensate for the
    shape of its input would couple the two forever.

    Idempotent: applying it to an already-labelled skeleton returns it
    unchanged. Production calls it exactly once, but the calibration snippets
    are stored pre-labelled so that they match what a real document renders to,
    and a labeller that double-appended on a second pass would quietly corrupt
    the anchor set the gate depends on.
    """
    lines = skeleton.split("\n")
    last_para = max(
        (i for i, line in enumerate(lines) if line.startswith("PARA:")), default=None
    )
    if last_para is not None and CLOSING_PARA_NOTE not in lines[last_para]:
        lines[last_para] += CLOSING_PARA_NOTE
    for index, line in enumerate(lines):
        if line == LAST_PARAGRAPH_HEADER:
            lines[index] = LAST_PARAGRAPH_HEADER + LAST_PARAGRAPH_NOTE
            break
        if line.startswith(LAST_PARAGRAPH_HEADER) and LAST_PARAGRAPH_NOTE in line:
            break  # already labelled
    return "\n".join(lines)


def skeleton_view(doc: Doc) -> str:
    """`textstats.doc_skeleton`, the closing-paragraph labels, and the tables.

    Deterministic and free of timestamps, like the skeleton it extends: the same
    document renders the same string, which is what makes the cache key sound.
    """
    parts = [_label_closing_paragraph(textstats.doc_skeleton(doc)), "", TABLES_HEADER]
    blocks = _table_blocks(doc.text)
    if not blocks:
        parts.append("(none)")
    else:
        emitted = 0
        for index, block in enumerate(blocks, start=1):
            parts.append(f"[table {index}: {len(block)} lines]")
            for line in block:
                if emitted >= MAX_TABLE_LINES:
                    parts.append("… (further tables truncated)")
                    return "\n".join(parts)
                parts.append(line)
                emitted += 1
            parts.append("")
    return "\n".join(parts)


def judge_view_text(tell: Tell, doc: Doc) -> list[Chunk]:
    """The passages one tell's judge sees for one document, in order."""
    if tell.judge_view == "skeleton":
        return [Chunk.make(doc.doc_id, 0, skeleton_view(doc))]
    return chunk_doc(doc)


# --- quote verification ------------------------------------------------------


@dataclass(frozen=True)
class Match:
    """A judge quote located in the source it was supposed to come from."""

    quote: str  # the source text, verbatim, at the located offsets
    start: int
    end: int
    line: int  # 1-based
    normalized: str


_WS = re.compile(r"\s+")


def normalize_ws(text: str) -> str:
    """Collapse every whitespace run to one space and trim."""
    return _WS.sub(" ", text or "").strip()


def _normalized_index(source: str) -> tuple[str, list[int]]:
    """The whitespace-collapsed source, and each of its chars' raw offset."""
    out: list[str] = []
    offsets: list[int] = []
    in_space = True  # leading whitespace is dropped, as strip() would
    for index, char in enumerate(source):
        if char.isspace():
            if not in_space:
                out.append(" ")
                offsets.append(index)
                in_space = True
            continue
        out.append(char)
        offsets.append(index)
        in_space = False
    while out and out[-1] == " ":
        out.pop()
        offsets.pop()
    return "".join(out), offsets


def verify_quote(quote: str, source: str) -> Match | None:
    """Locate a judge quote in the source, ignoring how whitespace was mangled.

    Models re-wrap. A quote that crossed a line break comes back with a space, a
    quote copied out of a list comes back without the marker's indentation, and
    neither is a hallucination. What is a hallucination is a quote whose words do
    not appear in the source at all, and after collapsing whitespace the two
    cases are cleanly separable: substring or not.

    The returned quote is the *source's* text at the located offsets, not the
    judge's — so the evidence a reader checks is the document's own words.
    """
    needle = normalize_ws(quote)
    if not needle:
        return None
    haystack, offsets = _normalized_index(source)
    position = haystack.find(needle)
    if position == -1:
        return None
    start = offsets[position]
    end = offsets[position + len(needle) - 1] + 1
    return Match(
        quote=source[start:end],
        start=start,
        end=end,
        line=source.count("\n", 0, start) + 1,
        normalized=needle,
    )


def context_for(
    match: Match, source: str, sentences: int = CONTEXT_SENTENCES
) -> str:
    """The matched span plus up to `sentences` sentences either side.

    Stage 2 has to see enough to apply the rubric's exclusions — whether a
    question was answered, whether a fragment leans on a neighbouring sentence —
    and no more, because a judge handed the whole document will re-extract
    instead of adjudicating.
    """
    pieces = textstats.split_sentences(source)
    if pieces:
        target = match.normalized
        head = target[:60]
        for index, sentence in enumerate(pieces):
            normalized = normalize_ws(sentence)
            if target in normalized or head in normalized:
                window = pieces[max(0, index - sentences) : index + sentences + 1]
                return " ".join(window)
    left = max(0, match.start - CONTEXT_CHARS)
    right = min(len(source), match.end + CONTEXT_CHARS)
    return normalize_ws(source[left:right])


# --- prompts -----------------------------------------------------------------

_EXTRACTION_HEAD = """\
TASK: EXTRACTION ONLY. Find candidate passages. Do not rate, score, rank, or
judge anything. A separate stage decides which candidates count.

INCLUSION CRITERIA (verbatim, tell {tell_id} "{name}", rubric_version
{rubric_version}). This is a PARTIAL rubric: the full rubric also carries
exclusions, and they are deliberately withheld from you. You must NOT apply
exclusions, and you must not try to guess what they are. A later step handles
them. Your job is recall against the shape described here.
---
{rubric}---
"""

_EXTRACTION_TAIL = """\
RULES
1. Copy every quote VERBATIM from the passage, character for character. Do not
   paraphrase, correct spelling, expand abbreviations, or normalize punctuation.
   A quote that is not in the passage word for word is discarded.
2. Quote the full sentence containing the candidate, so it can be located.
3. OVER-EXTRACT. Include every borderline candidate, including ones you think
   probably do not qualify. Recall matters here; precision is decided later.
4. Surface a candidate even when you suspect some exception ought to rule it
   out — a quotation, a heading, a list, a question meant for a real person,
   an enumeration of real facts. Those judgements are not yours to make at this
   stage, and a candidate you withhold can never be reviewed.
5. Do not deduplicate near-identical candidates; quote each occurrence.
6. If there are no candidates at all, return {{"spans": []}}.

OUTPUT — reply with this JSON object and nothing else:
{{"spans": [{{"quote": "<verbatim text from the passage>", "location_hint": "<a few words saying where>"}}]}}

PASSAGE
<<<PASSAGE
{passage}
PASSAGE>>>
"""

_ADJUDICATION = """\
TASK: ADJUDICATE ONE SPAN against one rubric. Answer only which rubric criteria
hold. Do not rate, score, or rank; do not consider any other span.

RUBRIC (verbatim, tell {tell_id} "{name}", rubric_version {rubric_version}):
---
{rubric}---

SPAN UNDER REVIEW
<<<SPAN
{span}
SPAN>>>

CONTEXT (the span with up to two sentences either side)
<<<CONTEXT
{context}
CONTEXT>>>

RULES
1. "criteria_met" lists the letters of the criteria that HOLD for this span,
   using the rubric's own letters. Available criteria: {criteria}. Include a
   letter only if that criterion genuinely holds for this span.
2. "exclusion_triggered" is the letter of the FIRST exclusion that applies
   ({exclusions}), or null if none applies.
3. "instance" is your own overall read, true or false. It is recorded but not
   used for scoring; the criteria list is what decides.
4. "rationale" is ONE sentence, under 30 words.

OUTPUT — reply with this JSON object and nothing else:
{{"instance": <true|false>, "criteria_met": [<letters>], "exclusion_triggered": <letter or null>, "rationale": "<one sentence>"}}
"""

_STRUCTURAL = """\
TASK: EXTRACT STRUCTURAL EVIDENCE from a document outline. Report what is there.
Do not decide whether the document exhibits the pattern, and do not rate or
score anything — the decision is made from your evidence by a separate rule.

RUBRIC (verbatim, tell {tell_id} "{name}", rubric_version {rubric_version}):
---
{rubric}---

{fields}

RULES
1. Every quote must be copied VERBATIM from the outline below, character for
   character. A quote that is not in the outline is discarded.
2. Report what you find. Leave a field null (or its list empty) when there is
   nothing to report; do not invent an example to fill it.
3. Reply with the JSON object and nothing else.

OUTPUT SCHEMA
{schema}

DOCUMENT OUTLINE
<<<OUTLINE
{passage}
OUTLINE>>>
"""

_STRUCTURAL_FIELDS: dict[str, tuple[str, str]] = {
    "str.summary-sandwich": (
        """\
EVIDENCE TO EXTRACT
- opening_preview_quote: the sentence in the opening section that previews the
  document's structure or restates the ask, or null if there is none.
- closing_recap_quote: the sentence in the closing section that re-summarizes
  points already made, or null if there is none.
- closing_recap_is_separate_section: true only if that recap sits in a section
  DISTINCT from the document's last substantive section. If the document simply
  ends on the last finding of its final content section, this is false — the
  outline labels which paragraph is the closing one, and a sentence that first
  appears inside the final substantive section is that section's own content.
- closing_new_info_quote: a sentence in the closing section that introduces a
  NEW decision, deadline, owner, or open question, or null if there is none.""",
        '{"opening_preview_quote": "<verbatim or null>", '
        '"closing_recap_quote": "<verbatim or null>", '
        '"closing_recap_is_separate_section": <true|false>, '
        '"closing_new_info_quote": "<verbatim or null>"}',
    ),
    "str.parallel-bullet-grammar": (
        """\
EVIDENCE TO EXTRACT — one entry per list in the outline that has 3 or more items
- heading: the nearest heading above the list, verbatim, or "" if none.
- item_count: how many items the list has.
- item_openings: the first three to five words of EVERY item, verbatim, in order.
- shared_opening_form: which ONE of the rubric's five named forms every item
  opens with — "imperative", "gerund", "Noun: lead-in", "same opening word", or
  "noun + past participle". The five are exhaustive: if the items share some
  other resemblance (all noun phrases, all questions, all past-tense clauses),
  that is not one of the five and this must be null.
- all_items_match: true only if NOT ONE item breaks that pattern.
- single_word_items: true if the items are single words, proper nouns, dates, or
  numbers.
- procedural_format: true if the list is a runbook, checklist, or agenda whose
  format requires the imperative.""",
        '{"lists": [{"heading": "<verbatim or empty>", "item_count": <int>, '
        '"item_openings": ["<verbatim>", ...], "shared_opening_form": "<text or null>", '
        '"all_items_match": <true|false>, "single_word_items": <true|false>, '
        '"procedural_format": <true|false>}]}',
    ),
    "str.table-overuse": (
        """\
EVIDENCE TO EXTRACT — one entry per markdown table in the TABLES section
- header_row: the table's header row, verbatim.
- sample_data_row: one representative data row, verbatim, or null.
- row_count: number of data rows (excluding the header and the delimiter).
- column_count: number of columns.
- criterion: "a" if it is a two-column Aspect/Description-style table whose
  second column holds prose sentences; "b" if it has a single data row; "c" if
  its cells hold running prose that would read as paragraphs or bullets with no
  loss; null if none of those.
- genuine_data_table: true if it is numeric or categorical values, one row per
  entity.
- crosswalk_or_schedule: true if it is a schedule, roster, budget, or crosswalk
  whose columns are read against each other.
- required_by_format: true if the document's stated format requires the table.""",
        '{"tables": [{"header_row": "<verbatim>", "sample_data_row": "<verbatim or null>", '
        '"row_count": <int>, "column_count": <int>, "criterion": "<a|b|c or null>", '
        '"genuine_data_table": <true|false>, "crosswalk_or_schedule": <true|false>, '
        '"required_by_format": <true|false>}]}',
    ),
}


def _examples_block(tell: Tell, limit: int = 4) -> str:
    if not tell.examples:
        return ""
    lines = ["EXAMPLES OF THE PATTERN (from the registry, illustrative only):"]
    for example in tell.examples[:limit]:
        lines.append("- " + normalize_ws(example))
    if tell.counter_examples:
        lines.append("PASSAGES THAT DO NOT QUALIFY:")
        for counter in tell.counter_examples[:limit]:
            lines.append("- " + normalize_ws(counter))
    return "\n".join(lines) + "\n"


def _rubric_text(tell: Tell) -> str:
    rubric = tell.rubric or ""
    return rubric if rubric.endswith("\n") else rubric + "\n"


def build_extraction_prompt(tell: Tell, passage: str) -> str:
    """Stage 1: inclusion criteria only, few-shots, recall-first rules.

    The exclusions are withheld on purpose (protocol v2). An extractor that can
    see them applies some of them and not others, which decides the outcome
    before any adjudication is recorded — and an instance rejected silently at
    extraction leaves nothing for a reader to check, which is the one thing this
    whole pipeline is built to prevent.
    """
    inclusion, _, evidence = split_rubric(tell.rubric or "")
    partial = inclusion.rstrip("\n") + "\n"
    if evidence.strip():
        partial += evidence.rstrip("\n") + "\n"
    head = _EXTRACTION_HEAD.format(
        tell_id=tell.id,
        name=tell.name,
        rubric_version=tell.rubric_version,
        rubric=partial,
    )
    examples = _examples_block(tell)
    tail = _EXTRACTION_TAIL.format(passage=passage)
    return "\n".join(part for part in (head, examples, tail) if part)


def build_adjudication_prompt(tell: Tell, span_quote: str, context: str) -> str:
    """Stage 2: one span, its context, and the rubric's own letters."""
    criteria, exclusions = parse_rubric_labels(tell.rubric or "")
    return _ADJUDICATION.format(
        tell_id=tell.id,
        name=tell.name,
        rubric_version=tell.rubric_version,
        rubric=_rubric_text(tell),
        span=span_quote,
        context=context,
        criteria=", ".join(f"({c})" for c in criteria) or "(none listed)",
        exclusions=", ".join(f"({x})" for x in exclusions) or "none",
    )


def build_structural_prompt(tell: Tell, skeleton_text: str) -> str:
    """Doc-level tells: evidence fields only. The decision rule stays in code.

    These three tells keep the WHOLE rubric, exclusions included, and that is
    not an oversight — it is the difference between the two shapes of judge
    call. A span tell asks twice: propose, then adjudicate, so the exclusions
    can be held back from the first question. A doc-level tell asks once, and
    what it asks for is evidence: `genuine_data_table`, `procedural_format`,
    `crosswalk_or_schedule`, `required_by_format` are all *facts about the
    exclusions*, and the code decides from them. Withholding the exclusions here
    would leave those fields unfillable and push the exclusion judgement back
    into the model — the opposite of what the split was for.
    """
    try:
        fields, schema = _STRUCTURAL_FIELDS[tell.id]
    except KeyError:
        raise KeyError(f"no structural evidence schema for {tell.id!r}") from None
    return _STRUCTURAL.format(
        tell_id=tell.id,
        name=tell.name,
        rubric_version=tell.rubric_version,
        rubric=_rubric_text(tell),
        fields=fields,
        schema=schema,
        passage=skeleton_text,
    )


def extraction_spans(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """The `spans` list out of a stage-1 payload, defensively.

    A judge that answers with a bare list, or with `span` singular, has still
    answered; the shapes that carry no quotes at all are the ones that get
    dropped.
    """
    spans = payload.get("spans")
    if spans is None and isinstance(payload.get("span"), list):
        spans = payload["span"]
    if not isinstance(spans, list):
        return []
    out: list[dict[str, Any]] = []
    for entry in spans:
        if isinstance(entry, str):
            out.append({"quote": entry, "location_hint": ""})
        elif isinstance(entry, dict) and _quote(entry.get("quote")):
            out.append(
                {
                    "quote": str(entry["quote"]),
                    "location_hint": str(entry.get("location_hint") or ""),
                }
            )
    return out


__all__ = [
    "CONTEXT_SENTENCES",
    "OVERLAP_WORDS",
    "PROMPT_VERSION",
    "PROTOCOL_VERSION",
    "RULES",
    "STRUCTURAL_DECISIONS",
    "TARGET_WORDS",
    "Chunk",
    "Match",
    "TellRule",
    "build_adjudication_prompt",
    "build_extraction_prompt",
    "build_structural_prompt",
    "chunk_doc",
    "context_for",
    "criteria_satisfied",
    "exclusion_fired",
    "extraction_spans",
    "judge_view_text",
    "normalize_label",
    "normalize_ws",
    "parse_rubric_labels",
    "prune_unverified",
    "rule_for",
    "skeleton_view",
    "span_counts",
    "structural_exclusion_for",
    "structural_quotes",
    "verify_quote",
]
