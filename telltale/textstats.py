"""Text utilities and the statistic registry the benchmark measures through.

Three layers:

1. Utilities — `strip_markdown`, `split_sentences`, `split_paragraphs`,
   `word_count`, `doc_skeleton`. Every number downstream is derived from these,
   so they are deliberately conservative: when a call is ambiguous they prefer
   under-splitting (one sentence too few) to inventing structure.
2. `STATS` — the name -> function table that `registry/tells.yaml` statistic
   tells refer to by `detection.stat`.
3. The 18 stat functions themselves. Rates are per 1,000 words of `doc.plain`;
   stats about markup read `doc.text`. A stat returns NaN when its input floor
   is not met (documented on each function) and never raises.
"""

from __future__ import annotations

import math
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:  # pragma: no cover - import cycle guard, corpus imports us
    from telltale.corpus import Doc

NAN = float("nan")

# --- markdown stripping ------------------------------------------------------

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_FENCE = re.compile(r"^\s{0,3}(```+|~~~+)")
_HR = re.compile(r"^\s{0,3}([-*_])[ \t]*(\1[ \t]*){2,}$")
_LINK_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*\S+")
_BLOCKQUOTE = re.compile(r"^\s{0,3}(>\s?)+")
_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_BULLET = re.compile(r"^\s*[-*+]\s+")
_NUMBERED = re.compile(r"^\s*\d+[.)]\s+")
_TASKBOX = re.compile(r"^\[[ xX]\]\s+")
_TABLE_DELIM = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")

_IMAGE = re.compile(r"!\[[^\]]*\]\((?:[^()]*)\)|!\[[^\]]*\]\[[^\]]*\]")
_INLINE_LINK = re.compile(r"\[([^\]]*)\]\((?:[^()]*)\)")
_REF_LINK = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
_AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")
_CODE_DOUBLE = re.compile(r"``(.+?)``", re.DOTALL)
_CODE_SINGLE = re.compile(r"`([^`\n]*)`")
_BOLD_STAR = re.compile(r"\*\*(.+?)\*\*")
_BOLD_UNDER = re.compile(r"(?<![A-Za-z0-9_])__(.+?)__(?![A-Za-z0-9_])")
_ITALIC_STAR = re.compile(r"\*(?!\s)([^*\n]+?)(?<!\s)\*")
_ITALIC_UNDER = re.compile(r"(?<![A-Za-z0-9_])_(?!\s)([^_\n]+?)(?<!\s)_(?![A-Za-z0-9_])")
_STRIKE = re.compile(r"~~(.+?)~~")
_BLANK_RUN = re.compile(r"\n{3,}")


def _drop_code_fences(lines: list[str]) -> list[str]:
    """Drop fenced code blocks, fences included. An unclosed fence eats the rest."""
    out: list[str] = []
    fence: str | None = None
    for line in lines:
        match = _FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                continue
            out.append(line)
        elif match and match.group(1)[0] == fence:
            fence = None
    return out


def _drop_table_runs(lines: list[str]) -> list[str]:
    """Drop markdown table blocks.

    A table is a run of consecutive non-blank lines that all contain `|` and
    that either includes a `---|---` delimiter row or is fully pipe-fenced. A
    lone prose line with a stray pipe is left alone.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        if "|" not in lines[i]:
            out.append(lines[i])
            i += 1
            continue
        j = i
        while j < len(lines) and "|" in lines[j] and lines[j].strip():
            j += 1
        run = lines[i:j]
        looks_like_table = len(run) >= 2 and (
            any(_TABLE_DELIM.match(line) for line in run)
            or all(line.strip().startswith("|") for line in run)
        )
        if not looks_like_table:
            out.extend(run)
        i = j
    return out


def _strip_inline(text: str) -> str:
    """Remove inline markup, keeping the words."""
    text = _IMAGE.sub("", text)
    text = _CODE_DOUBLE.sub(r"\1", text)
    text = _CODE_SINGLE.sub(r"\1", text)
    text = _INLINE_LINK.sub(r"\1", text)
    text = _REF_LINK.sub(r"\1", text)
    text = _AUTOLINK.sub(r"\1", text)
    text = _BOLD_STAR.sub(r"\1", text)
    text = _BOLD_UNDER.sub(r"\1", text)
    text = _ITALIC_STAR.sub(r"\1", text)
    text = _ITALIC_UNDER.sub(r"\1", text)
    text = _STRIKE.sub(r"\1", text)
    return text


def strip_markdown(md: str) -> str:
    """Return prose-only text: markup removed, wording and paragraphing kept.

    Code blocks, tables, images, horizontal rules, and link definitions go away
    entirely. Headings, list items, blockquotes, links, and emphasis keep their
    text and lose their markers. Runs of 3+ newlines collapse to 2. The function
    is idempotent: strip_markdown(strip_markdown(x)) == strip_markdown(x).
    """
    text = md.replace("\r\n", "\n").replace("\r", "\n")
    text = _HTML_COMMENT.sub("", text)

    lines = _drop_table_runs(_drop_code_fences(text.split("\n")))

    kept: list[str] = []
    for line in lines:
        if _HR.match(line) or _LINK_DEF.match(line):
            continue
        line = _BLOCKQUOTE.sub("", line)
        heading = _HEADING.match(line)
        if heading:
            line = heading.group(2)
        else:
            line = _BULLET.sub("", line, count=1) if _BULLET.match(line) else line
            line = _NUMBERED.sub("", line, count=1) if _NUMBERED.match(line) else line
        line = _TASKBOX.sub("", line, count=1)
        kept.append(line)

    text = _strip_inline("\n".join(kept))
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = _BLANK_RUN.sub("\n\n", text)
    return text.strip()


# --- splitting ---------------------------------------------------------------

WORD_PATTERN = re.compile(r"[A-Za-z0-9'’-]+")

# Never split after these. Sentence-final abbreviations ("...Acme Corp. The
# board met.") are therefore merged into the following sentence — a deliberate
# trade: an occasional under-split is cheaper for every downstream rate than a
# split inside "U.S. Department of Education".
ABBREVIATIONS = {
    "mr.", "mrs.", "ms.", "dr.", "prof.", "sr.", "jr.", "st.",
    "vs.", "etc.", "e.g.", "i.e.", "cf.", "approx.", "dept.", "est.",
    "no.", "inc.", "corp.", "ltd.", "co.", "u.s.", "u.k.", "ph.d.",
    "m.a.", "b.a.", "a.m.", "p.m.", "fig.", "al.",
    "jan.", "feb.", "mar.", "apr.", "jun.", "jul.",
    "aug.", "sep.", "sept.", "oct.", "nov.", "dec.",
}

_SENT_BOUNDARY = re.compile(
    r"""(?P<end>[.!?]+["'”’)\]]*)      # terminator plus any closing quote/bracket
        (?P<gap>[ \t\n]+)              # whitespace
        (?=["'“‘(\[]*[A-Z0-9])         # next sentence opens with a capital or digit
    """,
    re.VERBOSE,
)
_TRAILING_TOKEN = re.compile(r"[A-Za-z0-9.'’-]*\.$")
_INITIAL = re.compile(r"[A-Z]\.")
_DOTTED = re.compile(r"(?:[A-Za-z]\.){2,}")
_NUMBER_DOT = re.compile(r"\d+\.")
_WHITESPACE = re.compile(r"\s+")


def _is_no_split(prefix: str, following: str) -> bool:
    """True if the period ending `prefix` is an abbreviation/decimal, not a stop."""
    if not prefix.endswith("."):
        return False
    match = _TRAILING_TOKEN.search(prefix)
    if not match:
        return False
    token = match.group(0)
    lowered = token.lower()
    if lowered in ABBREVIATIONS:
        return True
    if _INITIAL.fullmatch(token):  # "J. Smith"
        return True
    if _DOTTED.fullmatch(token):  # "U.S.", "i.e.", "a.m."
        return True
    if _NUMBER_DOT.fullmatch(token) and following[:1].isdigit():  # "3. 5" -> decimal
        return True
    return False


@lru_cache(maxsize=128)
def _split_sentences_cached(text: str) -> tuple[str, ...]:
    sentences: list[str] = []
    for block in re.split(r"\n[ \t]*\n", text):
        block = block.strip()
        if not block:
            continue
        start = 0
        for match in _SENT_BOUNDARY.finditer(block):
            cut = match.end("end")
            if _is_no_split(block[:cut], block[match.end() :]):
                continue
            if cut <= start:
                continue
            piece = block[start:cut].strip()
            if piece:
                sentences.append(_WHITESPACE.sub(" ", piece))
            start = match.end()
        tail = block[start:].strip()
        if tail:
            sentences.append(_WHITESPACE.sub(" ", tail))
    return tuple(sentences)


def split_sentences(text: str) -> list[str]:
    """Split prose into trimmed, non-empty sentences.

    Splits on `.`/`!`/`?` followed by whitespace and a capital, digit, or opening
    quote, guarded against abbreviations, initials, and decimals. A blank line is
    always a boundary; a single newline is not, so unpunctuated list items sitting
    on consecutive lines read as one sentence.
    """
    return list(_split_sentences_cached(text))


def split_paragraphs(text: str) -> list[str]:
    """Split on blank lines; trimmed, empties dropped."""
    return [p.strip() for p in re.split(r"\n[ \t]*\n", text) if p.strip()]


def word_count(text: str) -> int:
    """Words = runs of letters, digits, apostrophes, and hyphens."""
    return len(WORD_PATTERN.findall(text))


def _tokens(text: str) -> list[str]:
    return WORD_PATTERN.findall(text)


def _first_word(sentence: str) -> str:
    match = WORD_PATTERN.search(sentence)
    return match.group(0) if match else ""


# --- skeleton ----------------------------------------------------------------

_HEADING_ANY = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")


def doc_skeleton(doc: "Doc") -> str:
    """A deterministic outline of a document, for the judge's skeleton view.

    Emits, in document order, the heading tree, each prose paragraph's word count
    and first sentence, and each list's item count and item openings — then the
    first and last paragraphs in full. No timestamps, no randomness: the same
    document always renders the same string.
    """
    lines = _drop_table_runs(_drop_code_fences(doc.text.split("\n")))

    outline: list[str] = []
    paragraphs: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or _HR.match(line) or _LINK_DEF.match(line):
            i += 1
            continue

        heading = _HEADING_ANY.match(line)
        if heading:
            outline.append(f"H{len(heading.group(1))}: {_strip_inline(heading.group(2)).strip()}")
            i += 1
            continue

        if _LIST_ITEM.match(line):
            items: list[str] = []
            while i < len(lines) and _LIST_ITEM.match(lines[i]):
                item = _strip_inline(_LIST_ITEM.match(lines[i]).group(1)).strip()
                items.append(item)
                i += 1
            outline.append(f"LIST: {len(items)} items")
            for item in items:
                words = item.split()
                opening = " ".join(words[:6])
                outline.append(f"  - {opening}{'...' if len(words) > 6 else ''}")
            continue

        block: list[str] = []
        while i < len(lines):
            current = lines[i]
            if not current.strip() or _HEADING_ANY.match(current) or _LIST_ITEM.match(current):
                break
            if _HR.match(current) or _LINK_DEF.match(current):
                break
            block.append(current)
            i += 1
        paragraph = strip_markdown("\n".join(block))
        if paragraph:
            paragraphs.append(paragraph)
            sentences = split_sentences(paragraph)
            first = sentences[0] if sentences else ""
            outline.append(f"PARA: {word_count(paragraph)}w | {first}")

    parts = [
        f"SKELETON {doc.doc_id}",
        f"format: {doc.fmt}",
        f"words: {doc.words}",
        "",
        "OUTLINE",
        *(outline or ["(empty)"]),
        "",
        "FIRST PARAGRAPH",
        paragraphs[0] if paragraphs else "(none)",
        "",
        "LAST PARAGRAPH",
        paragraphs[-1] if paragraphs else "(none)",
    ]
    return "\n".join(parts)


# --- stat registry -----------------------------------------------------------

STATS: dict[str, Callable[["Doc"], float]] = {}


def stat(name: str) -> Callable[[Callable[["Doc"], float]], Callable[["Doc"], float]]:
    """Register a statistic under the name used by `detection.stat` in the registry."""

    def decorate(fn: Callable[["Doc"], float]) -> Callable[["Doc"], float]:
        if name in STATS:
            raise ValueError(f"duplicate stat name: {name}")
        STATS[name] = fn
        return fn

    return decorate


def compute(name: str, doc: "Doc") -> float:
    """Run one registered stat by name. Raises KeyError if it is not registered."""
    return STATS[name](doc)


def _per_1k(count: int, words: int) -> float:
    """Rate per 1,000 words. An empty document has no rate, so: NaN."""
    if words <= 0:
        return NAN
    return 1000.0 * count / words


def _cv(values: list[int] | list[float]) -> float:
    """Population coefficient of variation. NaN for an empty set or a zero mean."""
    if not values:
        return NAN
    mean = sum(values) / len(values)
    if mean == 0:
        return NAN
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance) / mean


def _sentences(doc: "Doc") -> list[str]:
    return split_sentences(doc.plain)


def _sentence_lengths(doc: "Doc") -> list[int]:
    return [word_count(s) for s in _sentences(doc)]


def _bullet_runs(text: str) -> list[int]:
    """Item counts of each bullet list: a maximal run of bullet lines, single
    blank lines allowed inside it."""
    runs: list[int] = []
    count = 0
    blanks = 0
    for line in text.split("\n"):
        if _BULLET_LINE.match(line):
            count += 1
            blanks = 0
        elif not line.strip():
            if count:
                blanks += 1
                if blanks > 1:
                    runs.append(count)
                    count = 0
                    blanks = 0
        else:
            if count:
                runs.append(count)
            count = 0
            blanks = 0
    if count:
        runs.append(count)
    return runs


MIN_SENTENCES = 10  # floor below which sentence-shaped stats are not meaningful
MIN_PARAGRAPHS = 3
MIN_SECTIONS = 3
MIN_MATTR_TOKENS = 50
MATTR_WINDOW = 500

# --- 1-2: punctuation --------------------------------------------------------

_EM_DASH = re.compile(r"—|–| - ")
_HEADING_LINE = re.compile(r"^#{1,6}\s", re.MULTILINE)
_BULLET_LINE = re.compile(r"^\s*[-*+]\s")
_BULLET_LINE_M = re.compile(r"^\s*[-*+]\s", re.MULTILINE)
_BOLD_SPAN = re.compile(r"\*\*[^*\n]+?\*\*")
_TRANSITIONS = re.compile(
    r"\b(?:moreover|furthermore|additionally|consequently|therefore|thus|hence"
    r"|in addition|notably|ultimately)\b",
    re.IGNORECASE,
)
_LY_ADVERB = re.compile(r"\b[a-z]{3,}ly\b", re.IGNORECASE)
_H2_SPLIT = re.compile(r"^## ", re.MULTILINE)


@stat("em_dash_per_1k")
def em_dash_per_1k(doc: "Doc") -> float:
    """Em dashes, en dashes, and spaced hyphens per 1k prose words. NaN if empty."""
    return _per_1k(len(_EM_DASH.findall(doc.plain)), doc.words)


@stat("semicolon_per_1k")
def semicolon_per_1k(doc: "Doc") -> float:
    """Semicolons per 1k prose words. NaN if empty."""
    return _per_1k(doc.plain.count(";"), doc.words)


# --- 3-6: rhetoric -----------------------------------------------------------


@stat("pct_sentences_starting_while")
def pct_sentences_starting_while(doc: "Doc") -> float:
    """% of sentences opening with capital-W "While". NaN under 10 sentences."""
    sentences = _sentences(doc)
    if len(sentences) < MIN_SENTENCES:
        return NAN
    hits = sum(1 for s in sentences if _first_word(s) == "While")
    return 100.0 * hits / len(sentences)


@stat("pct_sentences_starting_however")
def pct_sentences_starting_however(doc: "Doc") -> float:
    """% of sentences opening with "However". NaN under 10 sentences."""
    sentences = _sentences(doc)
    if len(sentences) < MIN_SENTENCES:
        return NAN
    hits = sum(1 for s in sentences if _first_word(s) == "However")
    return 100.0 * hits / len(sentences)


@stat("transition_words_per_1k")
def transition_words_per_1k(doc: "Doc") -> float:
    """Discourse-marker density per 1k prose words. NaN if empty."""
    return _per_1k(len(_TRANSITIONS.findall(doc.plain)), doc.words)


@stat("anaphora_share")
def anaphora_share(doc: "Doc") -> float:
    """% of adjacent sentence pairs opening with the same two words.

    NaN under 10 sentences.
    """
    sentences = _sentences(doc)
    if len(sentences) < MIN_SENTENCES:
        return NAN
    bigrams: list[str | None] = []
    for sentence in sentences:
        tokens = _tokens(sentence)[:2]
        bigrams.append(" ".join(t.lower() for t in tokens) if len(tokens) == 2 else None)
    pairs = len(bigrams) - 1
    hits = sum(1 for a, b in zip(bigrams, bigrams[1:]) if a is not None and a == b)
    return 100.0 * hits / pairs


# --- 7-12: structure ---------------------------------------------------------


@stat("headings_per_1k")
def headings_per_1k(doc: "Doc") -> float:
    """Markdown heading lines per 1k prose words. NaN if empty."""
    return _per_1k(len(_HEADING_LINE.findall(doc.text)), doc.words)


@stat("bullet_lines_per_1k")
def bullet_lines_per_1k(doc: "Doc") -> float:
    """Bullet lines per 1k prose words. NaN if empty."""
    return _per_1k(len(_BULLET_LINE_M.findall(doc.text)), doc.words)


@stat("bold_spans_per_1k")
def bold_spans_per_1k(doc: "Doc") -> float:
    """**bold** spans per 1k prose words. NaN if empty."""
    return _per_1k(len(_BOLD_SPAN.findall(doc.text)), doc.words)


@stat("paragraph_length_cv")
def paragraph_length_cv(doc: "Doc") -> float:
    """Variation in paragraph length. NaN under 3 paragraphs."""
    paragraphs = split_paragraphs(doc.plain)
    if len(paragraphs) < MIN_PARAGRAPHS:
        return NAN
    return _cv([word_count(p) for p in paragraphs])


@stat("section_length_cv")
def section_length_cv(doc: "Doc") -> float:
    """Variation in H2 section length. NaN under 3 sections.

    Sections are the chunks between `## ` headings; anything before the first H2
    counts as a section of its own when it is not blank.
    """
    chunks = _H2_SPLIT.split(doc.text)
    if chunks and not chunks[0].strip():
        chunks = chunks[1:]
    if len(chunks) < MIN_SECTIONS:
        return NAN
    return _cv([word_count(strip_markdown(chunk)) for chunk in chunks])


@stat("pct_lists_exactly_three")
def pct_lists_exactly_three(doc: "Doc") -> float:
    """% of bullet lists with exactly three items. NaN when there are no lists."""
    runs = _bullet_runs(doc.text)
    if not runs:
        return NAN
    return 100.0 * sum(1 for n in runs if n == 3) / len(runs)


# --- 13-18: sentence-level statistics ----------------------------------------


@stat("sentence_length_cv")
def sentence_length_cv(doc: "Doc") -> float:
    """Burstiness: variation in sentence length. NaN under 10 sentences."""
    lengths = _sentence_lengths(doc)
    if len(lengths) < MIN_SENTENCES:
        return NAN
    return _cv(lengths)


@stat("sentence_length_band_distance")
def sentence_length_band_distance(doc: "Doc") -> float:
    """How far mean sentence length sits outside 14-22 words (0 inside).

    NaN under 10 sentences.
    """
    lengths = _sentence_lengths(doc)
    if len(lengths) < MIN_SENTENCES:
        return NAN
    mean = sum(lengths) / len(lengths)
    if mean < 14.0:
        return 14.0 - mean
    if mean > 22.0:
        return mean - 22.0
    return 0.0


@stat("mattr_500")
def mattr_500(doc: "Doc") -> float:
    """Moving-average type-token ratio over 500-token windows.

    Falls back to plain TTR when the document is shorter than one window;
    NaN under 50 tokens.
    """
    tokens = [t.lower() for t in _tokens(doc.plain)]
    if len(tokens) < MIN_MATTR_TOKENS:
        return NAN
    if len(tokens) < MATTR_WINDOW:
        return len(set(tokens)) / len(tokens)

    counts: dict[str, int] = {}
    for token in tokens[:MATTR_WINDOW]:
        counts[token] = counts.get(token, 0) + 1
    total = len(counts)
    windows = 1
    for i in range(MATTR_WINDOW, len(tokens)):
        leaving = tokens[i - MATTR_WINDOW]
        counts[leaving] -= 1
        if counts[leaving] == 0:
            del counts[leaving]
        entering = tokens[i]
        counts[entering] = counts.get(entering, 0) + 1
        total += len(counts)
        windows += 1
    return total / windows / MATTR_WINDOW


@stat("ly_adverbs_per_1k")
def ly_adverbs_per_1k(doc: "Doc") -> float:
    """-ly adverbs per 1k prose words. NaN if empty."""
    return _per_1k(len(_LY_ADVERB.findall(doc.plain)), doc.words)


@stat("commas_per_sentence")
def commas_per_sentence(doc: "Doc") -> float:
    """Commas divided by sentences. NaN under 10 sentences."""
    sentences = _sentences(doc)
    if len(sentences) < MIN_SENTENCES:
        return NAN
    return doc.plain.count(",") / len(sentences)


@stat("sentence_opener_diversity")
def sentence_opener_diversity(doc: "Doc") -> float:
    """Distinct sentence-opening words over sentence count. NaN under 10 sentences."""
    sentences = _sentences(doc)
    if len(sentences) < MIN_SENTENCES:
        return NAN
    openers = [_first_word(s).lower() for s in sentences]
    return len(set(openers)) / len(openers)
