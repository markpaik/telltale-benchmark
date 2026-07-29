"""The LLM half of discovery: four lenses, one strict output contract.

The sweep finds where to look. The auditor is what looks — a judge model reading
real excerpts and proposing tells the arithmetic cannot name on its own. "This
model opens its second paragraph with a concessive clause" is not an n-gram, and
no amount of log-odds finds it.

Three design decisions carry this file.

**Four lenses, not one prompt.** A single "find the tells" prompt returns four
lexical observations and stops, because word choice is what a reader notices
first — the same reason `scoring.CATEGORY_WEIGHTS` puts lexical highest. Asking
four separate questions, each with its own view of the corpus, is what makes the
rhetorical and structural findings possible at all. The structural lens never
sees prose: it is handed `textstats.doc_skeleton` output, so it cannot propose a
word and has to talk about shape. The formatting lens sees raw markdown, which
the other three never do.

**Proposals, not verdicts.** Every lens is told to output a *candidate* with a
machine-checkable rule and at least three verbatim quotes from the excerpts it
was shown. Nothing here decides whether a candidate is real — `verify.py` does
that, against the whole corpus, with five gates. The auditor's failure mode is
inventing a plausible-sounding tell, and the defence against it is that a quote
which is not in the excerpt is caught by code, before it can become evidence.

**The prompt is a pure function of its inputs.** Same corpus, same sweep, same
registry, same prompt, same cache key. That is what lets a discovery run be
re-executed months later and compared, and it is why the excerpt selection is
sorted and stratified rather than sampled.
"""

from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from telltale import textstats
from telltale.corpus import Doc
from telltale.judge import cache as cache_mod
from telltale.registry import CATEGORIES, METHODS, Tell, is_valid_scope

#: Bumped when a lens prompt or the output contract changes. It is part of every
#: discovery cache key, for the same reason `PROTOCOL_VERSION` is part of every
#: judge cache key: an answer produced under different instructions is a
#: different answer, and reusing it silently would change the instrument.
LENS_PROMPT_VERSION = 1

LENSES: tuple[str, ...] = ("lexical", "rhetorical", "structural", "formatting")

#: Lens calls are generative, not extractive: the judge reads sixteen excerpts
#: and composes regexes, and it takes minutes rather than seconds. The judge
#: stack's own 300s default was set for adjudicating one span and times these
#: out — measured at ~460s for a 13k-character prompt, so the ceiling is set
#: well clear of it rather than at the observed figure.
LENS_TIMEOUT_S = 1800

#: Excerpts per side. Eight is what fits in a prompt beside the sweep table and
#: the registry list while leaving the model room to actually read them.
N_EXCERPTS = 8
EXCERPT_CHARS = 1500

#: Sweep rows shown to the lexical and rhetorical lenses. The structural and
#: formatting lenses get none: an n-gram table invites a lexical answer, which
#: is the one thing those two lenses exist to avoid.
N_SWEEP_ROWS = 40

MAX_EXISTING_LISTED = 400


class AuditError(RuntimeError):
    """A lens call that did not produce usable candidates."""


# --- excerpt selection -------------------------------------------------------


def excerpt_text(text: str, chars: int = EXCERPT_CHARS) -> str:
    """The opening of a document plus a window from its middle.

    Documents in this corpus are front-loaded — every format opens with a
    heading and a framing paragraph — so an excerpt taken from the start alone
    would teach a lens about openings and nothing else. Half from the start and
    half from the middle costs nothing and covers both, and the cut is marked so
    a model does not read across it as continuous prose.
    """
    body = (text or "").strip()
    if len(body) <= chars:
        return body
    half = chars // 2
    head = body[:half]
    middle = max(len(body) // 2 - half // 2, half)
    tail = body[middle : middle + half]
    return f"{head}\n[…]\n{tail}"


def _view_for(lens: str, doc: Doc) -> str:
    """Which rendering of a document a lens is allowed to see."""
    if lens == "structural":
        return textstats.doc_skeleton(doc)
    if lens == "formatting":
        return doc.text
    return doc.plain


def stratified(docs: Sequence[Doc], n: int) -> list[Doc]:
    """`n` documents spread across formats, deterministically.

    Sorted by doc_id, grouped by format, taken round-robin: one document from
    each format before a second from any. Eight documents drawn in doc_id order
    alone would be eight business reports, and a lens shown eight business
    reports proposes business-report tells.
    """
    groups: "OrderedDict[str, list[Doc]]" = OrderedDict()
    for doc in sorted(docs, key=lambda d: d.doc_id):
        groups.setdefault(doc.fmt, []).append(doc)

    out: list[Doc] = []
    depth = 0
    while len(out) < n and any(len(v) > depth for v in groups.values()):
        for fmt in sorted(groups):
            if len(out) >= n:
                break
            if len(groups[fmt]) > depth:
                out.append(groups[fmt][depth])
        depth += 1
    return out[:n]


def select_excerpts(
    docs: Sequence[Doc],
    lens: str,
    model: str | None = None,
    exclude_model: str | None = None,
    n: int = N_EXCERPTS,
    chars: int = EXCERPT_CHARS,
) -> list[dict[str, str]]:
    """The excerpts one side of a lens prompt shows, as records.

    `model` selects one model's documents (the target side); `exclude_model`
    selects everything else (the contrast side), stratified across the remaining
    models as well as the formats so the contrast is not one rival model.
    """
    if model is not None:
        pool = [d for d in docs if d.model == model]
        chosen = stratified(pool, n)
    else:
        others = sorted({d.model for d in docs if d.model != exclude_model})
        per_model = {m: stratified([d for d in docs if d.model == m], n) for m in others}
        chosen = []
        depth = 0
        while len(chosen) < n and any(len(v) > depth for v in per_model.values()):
            for m in others:
                if len(chosen) >= n:
                    break
                if len(per_model[m]) > depth:
                    chosen.append(per_model[m][depth])
            depth += 1

    return [
        {
            "doc_id": doc.doc_id,
            "model": doc.model,
            "format": doc.fmt,
            "text": excerpt_text(_view_for(lens, doc), chars),
        }
        for doc in chosen
    ]


# --- the output contract -----------------------------------------------------

CANDIDATE_SCHEMA: dict[str, Any] = {
    "name": "<short human name, 2-5 words, lowercase>",
    "category": "<lexical|punctuation|syntactic|structural|statistical>",
    "scope_hypothesis": "<general|model:<model-id>>",
    "method": "<regex|statistic|judge>",
    "rule": {
        "regex": {"pattern": "<python re pattern>", "flags": ["IGNORECASE"]},
        "statistic": {
            "stat_name": "<snake_case name>",
            "formula_sketch": "<one sentence: what is counted, over what denominator>",
        },
        "judge": {
            "rubric": "<criteria checklist, see below>",
            "judge_view": "<chunk|skeleton>",
        },
    },
    "examples": ["<verbatim quote from the excerpts>", "<...>", "<... at least three>"],
    "rationale": "<one or two sentences: why this separates the models>",
}

RUBRIC_SHAPE = """\
A judge rubric MUST be written as this three-part checklist, with these exact
headings and these exact label styles, because a downstream parser reads them:

    A span counts as an instance when ALL of the following hold.
    (a) <criterion>
    (b) <criterion>

    EXCLUSIONS: a span does NOT count if any of these applies.
    (x) <exclusion>
    (y) <exclusion>

    Evidence to extract: <what the judge should quote>
"""

_LENS_INSTRUCTIONS: dict[str, str] = {
    "lexical": """\
LENS: LEXICAL. You are looking for words and fixed phrases the target model
overproduces — its vocabulary fingerprint.

- Prefer method "regex". Write the pattern TIGHT: anchor on word boundaries
  (\\b), cover the inflections that belong to the same habit
  (\\bdelv(?:e|es|ed|ing)\\b), and do NOT write a pattern that would match the
  word in an unrelated sense.
- Where the sweep table below gives a z-score for your word or phrase, say so in
  the rationale and quote the z. A candidate the sweep already supports is worth
  more than one you noticed by eye.
- A single common word is rarely a tell on its own. A word in a specific
  collocation usually is. Prefer "landscape of" to "landscape".
- Do not propose a domain word that is simply what these documents are about
  (a corpus of school memos will say "students" constantly, and that is the
  prompt speaking, not the model).""",
    "rhetorical": """\
LENS: RHETORICAL. You are looking for sentence-level and argument-level
constructions — how the target model builds a sentence, not which words it puts
in one.

- Examples of the shape of thing worth proposing: a concessive opener followed
  by a reversal; a question asked and immediately answered; a three-part list
  used as emphasis; a negation-then-assertion pair ("This is not X. It is Y.");
  a sentence fragment used for weight.
- If the construction is LEXICALLY ANCHORED — it always contains particular
  words, so a regex can find it — propose method "regex" with that pattern.
- If it is NOT lexically anchored, propose method "judge" and write the rubric
  as a criteria checklist in the exact shape given below. Do not propose a judge
  rubric you could have written as a regex; a regex is cheaper, auditable, and
  does not drift.""",
    "structural": """\
LENS: STRUCTURAL. You are shown document SKELETONS, not prose: the heading tree,
each paragraph's word count and first sentence, each list's item count and item
openings. You cannot see most of the wording, and that is deliberate — your job
is the shape of the document.

- Examples of the shape of thing worth proposing: a fixed section order; every
  section the same length; lists that are always three items; a heading tree
  that never goes past H2; a closing section that only restates.
- Prefer method "statistic": give a `stat_name` in snake_case and a
  `formula_sketch` saying exactly what is counted and over what denominator. Do
  NOT write code; a human implements the statistic after review.
- If the pattern cannot be reduced to a number, propose method "judge" with
  judge_view "skeleton" and a rubric in the exact checklist shape below.
- Never propose a regex from this lens. You have not seen enough text to write
  one honestly.""",
    "formatting": """\
LENS: FORMATTING. You are shown RAW MARKDOWN, including every marker the other
lenses never see: #, ##, **bold**, bullets, tables, blockquotes, horizontal
rules, emoji, trailing whitespace.

- You are looking for markup habits: bolded lead-ins on bullet items, a bold
  run-in label before every paragraph, tables used for things that are not
  tabular, a horizontal rule before every closing section, headings phrased as
  questions, emoji as section markers.
- Propose method "regex" with a pattern written against the RAW markdown, and
  set flags to include "MULTILINE" whenever your pattern uses ^ or $.
- Your examples must be quoted from the raw markdown including its markers.""",
}


def _sweep_line(row: dict[str, Any]) -> str:
    counts = row.get("counts") or {}
    freqs = row.get("doc_freq") or {}
    counted = " ".join(f"{m}={counts[m]}" for m in sorted(counts))
    seen = " ".join(f"{m}={freqs[m]:.2f}" for m in sorted(freqs))
    return (
        f"  z={float(row.get('z', 0.0)):+.2f}  n={row.get('n')}  "
        f"{row.get('ngram')!r}  counts[{counted}]  doc-freq[{seen}]"
    )


def _existing_block(tells: Iterable[Tell]) -> str:
    listed = sorted(
        ((t.id, t.name) for t in tells), key=lambda pair: pair[0]
    )[:MAX_EXISTING_LISTED]
    lines = [f"  {tell_id}  {name}" for tell_id, name in listed]
    return "\n".join(lines) if lines else "  (the registry is empty)"


def _excerpt_block(excerpts: Sequence[dict[str, str]], header: str) -> str:
    parts = [header]
    for index, item in enumerate(excerpts, start=1):
        parts.append(
            f"[{index}] {item['doc_id']} ({item['model']}, {item['format']})\n"
            f"<<<EXCERPT\n{item['text']}\nEXCERPT>>>"
        )
    if len(parts) == 1:
        parts.append("(none available)")
    return "\n\n".join(parts)


_HEAD = """\
TASK: PROPOSE CANDIDATE TELLS. You are a forensic text analyst comparing how
three language models write the same kinds of business document. Your job is to
propose falsifiable candidate "tells" — patterns that occur more in the TARGET
model's writing than in the others — each with a rule a machine can run.

TARGET MODEL: {target_model}

{lens_instructions}

WHAT IS ALREADY IN THE REGISTRY. Do NOT re-propose any of these, and do not
propose a trivial variant of one (a different inflection of the same word, the
same phrase with a synonym swapped). {n_existing} entries:
{existing}
"""

_SWEEP_HEAD = """\
STATISTICAL SWEEP (already computed, for your reference). Log-odds with an
informative Dirichlet prior, {target_model} against the other models pooled;
z is the posterior z-score, so a large positive z means the target overuses it.
{sweep}
"""

_TAIL = """\
{rubric_shape}

RULES
1. Every candidate needs at least THREE examples, and every example must be
   copied VERBATIM from the excerpts above, character for character. An example
   that is not in the excerpts is discarded and may invalidate the candidate.
2. `scope_hypothesis` is "general" if you believe all three models do this and
   "model:{target_model}" if you believe it separates the target. Say which you
   mean; do not hedge by picking "general" for everything.
3. Propose between 1 and {max_candidates} candidates. Fewer good candidates is
   better than more weak ones. If you genuinely find nothing this lens can
   support, return {{"candidates": []}}.
4. Do not propose anything you cannot point at in the excerpts.
5. `rule` carries exactly ONE key, matching your `method`: "regex", "statistic",
   or "judge".

OUTPUT — reply with this JSON object and nothing else:
{{"candidates": [{schema}]}}
"""


def build_lens_prompt(
    lens: str,
    target_model: str,
    target_excerpts: Sequence[dict[str, str]],
    contrast_excerpts: Sequence[dict[str, str]],
    sweep_rows: Sequence[dict[str, Any]],
    existing_tells: Sequence[Tell],
    max_candidates: int = 6,
    n_sweep_rows: int = N_SWEEP_ROWS,
) -> str:
    """One lens prompt. Deterministic in every argument."""
    if lens not in LENSES:
        raise ValueError(f"unknown lens {lens!r}; expected one of {list(LENSES)}")

    head = _HEAD.format(
        target_model=target_model,
        lens_instructions=_LENS_INSTRUCTIONS[lens],
        n_existing=len(list(existing_tells)),
        existing=_existing_block(existing_tells),
    )

    parts = [head]
    if lens in {"lexical", "rhetorical"} and sweep_rows:
        rows = list(sweep_rows)[:n_sweep_rows]
        parts.append(
            _SWEEP_HEAD.format(
                target_model=target_model,
                sweep="\n".join(_sweep_line(row) for row in rows),
            )
        )

    view = {
        "structural": "document skeletons",
        "formatting": "raw markdown",
    }.get(lens, "prose with markdown stripped")
    parts.append(
        _excerpt_block(
            target_excerpts, f"TARGET EXCERPTS — {target_model}, as {view}:"
        )
    )
    parts.append(
        _excerpt_block(
            contrast_excerpts, f"CONTRAST EXCERPTS — the other models, as {view}:"
        )
    )
    parts.append(
        _TAIL.format(
            rubric_shape=RUBRIC_SHAPE,
            max_candidates=max_candidates,
            target_model=target_model,
            schema=json.dumps(CANDIDATE_SCHEMA, indent=2, ensure_ascii=False),
        )
    )
    return "\n\n".join(parts)


# --- validation --------------------------------------------------------------

_RULE_KEYS = {
    "regex": ("pattern",),
    "statistic": ("stat_name", "formula_sketch"),
    "judge": ("rubric", "judge_view"),
}

MIN_EXAMPLES = 3


def _normalized(text: str) -> str:
    return " ".join(str(text or "").split()).lower()


def validate_candidate(
    candidate: Any, excerpt_texts: Sequence[str] = (), lens: str | None = None
) -> list[str]:
    """Every way one candidate fails the contract, as messages a model can act on.

    The examples check is the load-bearing one: a quote that is not in the
    excerpts is either a hallucination or a memory of some other corpus, and
    either way it is not evidence about these documents. Matching is on
    whitespace-normalized, case-folded text, because a model that re-wraps a
    quote across a line break has still quoted it.
    """
    errors: list[str] = []
    if not isinstance(candidate, dict):
        return [f"candidate is a {type(candidate).__name__}, expected an object"]

    name = str(candidate.get("name") or "").strip()
    if not name:
        errors.append("missing 'name'")
    elif len(name) > 60:
        errors.append(f"'name' is {len(name)} chars, keep it under 60")

    category = str(candidate.get("category") or "").strip()
    if category not in CATEGORIES:
        errors.append(f"'category' must be one of {sorted(CATEGORIES)}, got {category!r}")

    scope = str(candidate.get("scope_hypothesis") or "").strip()
    if not is_valid_scope(scope):
        errors.append(
            f"'scope_hypothesis' must be 'general' or 'model:<id>', got {scope!r}"
        )

    method = str(candidate.get("method") or "").strip()
    if method not in METHODS:
        errors.append(f"'method' must be one of {sorted(METHODS)}, got {method!r}")

    rule = candidate.get("rule")
    if not isinstance(rule, dict):
        errors.append("'rule' must be an object")
    elif method in _RULE_KEYS:
        inner = rule.get(method)
        body = inner if isinstance(inner, dict) else rule
        for key in _RULE_KEYS[method]:
            if not str(body.get(key) or "").strip():
                errors.append(f"'rule' for method {method!r} needs a non-empty {key!r}")
        if method == "judge":
            view = str(body.get("judge_view") or "").strip()
            if view not in {"chunk", "skeleton"}:
                errors.append(f"judge_view must be 'chunk' or 'skeleton', got {view!r}")

    if lens == "structural" and method == "regex":
        errors.append("the structural lens may not propose a regex")

    examples = candidate.get("examples")
    if not isinstance(examples, list):
        errors.append("'examples' must be a list")
    else:
        quotes = [str(e) for e in examples if str(e or "").strip()]
        if len(quotes) < MIN_EXAMPLES:
            errors.append(f"{len(quotes)} example(s), need at least {MIN_EXAMPLES}")
        if excerpt_texts:
            haystack = "\n".join(_normalized(t) for t in excerpt_texts)
            missing = [q for q in quotes if _normalized(q) not in haystack]
            if missing:
                errors.append(
                    "these examples are not verbatim in the excerpts: "
                    + "; ".join(repr(q[:70]) for q in missing[:3])
                )

    if not str(candidate.get("rationale") or "").strip():
        errors.append("missing 'rationale'")
    return errors


def normalize_rule(candidate: dict[str, Any]) -> dict[str, Any]:
    """The `rule` body flattened to the keys this pipeline reads.

    Models write `rule` both ways — `{"pattern": ...}` and
    `{"regex": {"pattern": ...}}`, because the schema shows all three methods
    nested. Both are accepted and normalized here rather than being rejected;
    the shape of the wrapper is not what the contract is protecting.
    """
    method = str(candidate.get("method") or "")
    rule = candidate.get("rule")
    if not isinstance(rule, dict):
        return {}
    inner = rule.get(method)
    body = inner if isinstance(inner, dict) else rule
    wanted = set(_RULE_KEYS.get(method, ()))
    if method == "regex":
        wanted.add("flags")
    out = {k: v for k, v in body.items() if k in wanted}
    if method == "regex":
        flags = out.get("flags")
        out["flags"] = [str(f) for f in flags] if isinstance(flags, list) else []
    return out


def parse_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """The `candidates` list out of a lens payload, defensively."""
    items = payload.get("candidates")
    if items is None and isinstance(payload.get("candidate"), list):
        items = payload["candidate"]
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list):
        return []
    return [c for c in items if isinstance(c, dict)]


RETRY_PREAMBLE = """\
Your previous reply did not satisfy the output contract. The problems were:

{problems}

Fix every one of them and reply again with ONLY the JSON object. Every example
must be copied verbatim from the excerpts in the original task, which is
repeated below in full.

"""


# --- running a lens ----------------------------------------------------------


@dataclass
class LensRun:
    """What one lens call produced, and what it cost."""

    lens: str
    target_model: str
    run_id: str
    prompt_sha: str
    candidates: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    retried: bool = False
    cached: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "lens": self.lens,
            "target_model": self.target_model,
            "run_id": self.run_id,
            "prompt_sha": self.prompt_sha,
            "n_candidates": len(self.candidates),
            "n_rejected": len(self.rejected),
            "retried": self.retried,
            "cached": self.cached,
        }


def prompt_sha(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def make_run_id(now: datetime | None = None) -> str:
    moment = now or datetime.now(timezone.utc)
    return moment.astimezone(timezone.utc).strftime("discover-%Y%m%dT%H%M%SZ")


def candidates_filename(lens: str, target_model: str) -> str:
    return f"{lens}__{target_model}.jsonl"


def run_audit(
    docs: Sequence[Doc],
    judge_client: Any,
    lens: str,
    target_model: str,
    out_dir: Path | None = None,
    sweep_rows: Sequence[dict[str, Any]] = (),
    existing_tells: Sequence[Tell] = (),
    run_id: str | None = None,
    max_candidates: int = 6,
) -> LensRun:
    """One lens, one target model: build the prompt, ask, validate, write.

    Validation failures get exactly one retry, carrying the specific problems
    back to the model — the same discipline as the judge transport's one JSON
    retry, and for the same reason. A second failure is recorded as a rejected
    candidate rather than raising: one bad proposal out of five must not lose the
    other four, and a lens that produced nothing usable is itself a finding worth
    having on disk.
    """
    if lens not in LENSES:
        raise ValueError(f"unknown lens {lens!r}; expected one of {list(LENSES)}")

    run = run_id or make_run_id()
    target = select_excerpts(docs, lens, model=target_model)
    contrast = select_excerpts(docs, lens, exclude_model=target_model)
    prompt = build_lens_prompt(
        lens,
        target_model,
        target,
        contrast,
        sweep_rows,
        existing_tells,
        max_candidates=max_candidates,
    )
    excerpt_texts = [item["text"] for item in (*target, *contrast)]
    sha = prompt_sha(prompt)

    payload, _, cached = judge_client.ask(
        cache_mod.DISCOVER, sha, f"lens:{lens}", LENS_PROMPT_VERSION, prompt
    )
    outcome = LensRun(
        lens=lens, target_model=target_model, run_id=run, prompt_sha=sha, cached=cached
    )

    accepted, rejected = _sift(parse_candidates(payload), excerpt_texts, lens)
    if rejected and not accepted:
        problems = "\n".join(
            f"- candidate {i + 1} ({entry.get('candidate', {}).get('name', '?')}): "
            + "; ".join(entry["errors"])
            for i, entry in enumerate(rejected)
        )
        retry_prompt = RETRY_PREAMBLE.format(problems=problems) + prompt
        retry_payload, _, _ = judge_client.ask(
            cache_mod.DISCOVER,
            prompt_sha(retry_prompt),
            f"lens:{lens}",
            LENS_PROMPT_VERSION,
            retry_prompt,
        )
        outcome.retried = True
        accepted, rejected = _sift(parse_candidates(retry_payload), excerpt_texts, lens)

    provenance = {
        "lens": lens,
        "target_model": target_model,
        "run_id": run,
        "prompt_sha": sha,
        "prompt_version": LENS_PROMPT_VERSION,
        "judge_model": str(getattr(judge_client, "model", "unknown")),
        "excerpt_doc_ids": [item["doc_id"] for item in target],
        "contrast_doc_ids": [item["doc_id"] for item in contrast],
    }
    for candidate in accepted:
        candidate["provenance"] = dict(provenance)
    outcome.candidates = accepted
    outcome.rejected = [{**entry, "provenance": dict(provenance)} for entry in rejected]

    if out_dir is not None:
        write_candidates(Path(out_dir), lens, target_model, outcome)
    return outcome


def _sift(
    candidates: Sequence[dict[str, Any]], excerpt_texts: Sequence[str], lens: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate in candidates:
        errors = validate_candidate(candidate, excerpt_texts, lens=lens)
        if errors:
            rejected.append({"candidate": candidate, "errors": errors})
        else:
            normalized = dict(candidate)
            normalized["rule"] = normalize_rule(candidate)
            accepted.append(normalized)
    return accepted, rejected


def write_candidates(
    out_dir: Path, lens: str, target_model: str, run: LensRun
) -> Path:
    """One jsonl per (lens, model): accepted candidates, then a trailing summary."""
    path = Path(out_dir) / candidates_filename(lens, target_model)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for candidate in run.candidates:
            handle.write(
                json.dumps(candidate, ensure_ascii=False, sort_keys=True) + "\n"
            )
        for entry in run.rejected:
            handle.write(
                json.dumps(
                    {"_rejected": True, **entry}, ensure_ascii=False, sort_keys=True
                )
                + "\n"
            )
    return path


def load_candidates(path: Path) -> list[dict[str, Any]]:
    """Accepted candidates from one jsonl file; rejected rows are skipped."""
    file = Path(path)
    if not file.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and not row.get("_rejected"):
            out.append(row)
    return out


def load_candidate_dir(directory: Path) -> list[dict[str, Any]]:
    """Every accepted candidate under a directory, in filename order."""
    root = Path(directory)
    if not root.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for path in sorted(root.glob("*.jsonl")):
        out.extend(load_candidates(path))
    return out


__all__ = [
    "CANDIDATE_SCHEMA",
    "EXCERPT_CHARS",
    "LENSES",
    "LENS_PROMPT_VERSION",
    "LENS_TIMEOUT_S",
    "MIN_EXAMPLES",
    "N_EXCERPTS",
    "AuditError",
    "LensRun",
    "build_lens_prompt",
    "candidates_filename",
    "excerpt_text",
    "load_candidate_dir",
    "load_candidates",
    "make_run_id",
    "normalize_rule",
    "parse_candidates",
    "prompt_sha",
    "run_audit",
    "select_excerpts",
    "stratified",
    "validate_candidate",
    "write_candidates",
]
