"""Regex tells: pattern in, count or flag out, quotes attached.

The one non-obvious decision here is *which text* a pattern runs against.
`Doc` carries two views — `text` (raw markdown) and `plain` (markdown stripped
out). Running every pattern on one of them would break half the registry:

* A structural pattern like `^#{1,4}\\s+.*\\?$` (question headings) or
  `^\\s*[-*+]\\s+\\*\\*...\\*\\*` (bolded bullet lead-ins) is *about* the markup.
  On `plain` the markers are gone and the tell can never fire.
* A lexical pattern like "it's worth noting" must not be able to match inside a
  code fence, a table cell, or a URL — all of which `plain` has already removed.
  On `text` a link target or a fenced example would count as prose.

So routing is by category: punctuation and structural tells read the raw
markdown, everything else reads the stripped prose. Category, not a per-tell
flag, because the registry already forces the prefix and the category to agree
(`pnc.*` -> punctuation, `str.*` -> structural), which makes the routing rule
checkable by reading an id.

The proper-noun guard
---------------------

A word-list tell counts a word, and a word is also a name. "Foster Elementary
School", "Ms. Harness", "Mr. Bolster", "Streamline Consulting", and "North Star
Academy" all fired against the seed registry, and no amount of per-tell
lookahead fixes the class: the sense guards that exist (`foster(?!\\s+care)`)
rule out the wrong sense, not the wrong *kind of word*. A tell may therefore set
`detection.proper_noun_guard: true`, and this module drops any match that starts
with a capital letter unless that capital is explainable as a sentence opening.

A capital mid-sentence is overwhelmingly a proper noun — English does not
capitalize common nouns there — while a capital at a sentence opening is
ambiguous between the word and the name, so it stays counted. Sentence openings
are: the start of the text, the start of a line, or a position after `.`, `!`,
`?`, or `:`, optionally through an opening quote or bracket. The terminating
period is tested with `textstats`'s own abbreviation rule, so "Ms. Harness" is
correctly *not* a sentence opening; that check is imported rather than
reimplemented, because two notions of a sentence boundary in one codebase will
drift apart.

Two residuals are accepted, both of them under-counting rather than over-:

* **A sentence-initial name still counts.** "Foster Elementary enrolled 40 more
  students" reads to the guard exactly like "Foster a culture of review". No
  local rule can separate them, and inventing one would need a gazetteer.
* **Title Case suppresses a guarded tell mid-heading.** In a heading like
  "Key Pivotal Findings", "Pivotal" is mid-sentence and capitalized, so it is
  dropped. The first word of a heading survives, because a heading sits on its
  own line. This is why the guard is opt-in per tell rather than global: it is
  only worth that cost where the name collision is real.
"""

from __future__ import annotations

import re
from typing import Iterator

from telltale.corpus import Doc
from telltale.detectors.base import MAX_MATCHES, BaseDetector, Detection
from telltale.registry import Tell

# One notion of "is this period a sentence boundary" for the whole codebase.
from telltale.textstats import _is_no_split

# Categories whose patterns are written against markdown syntax.
RAW_TEXT_CATEGORIES = frozenset({"punctuation", "structural"})

# What can end a sentence, and what may sit between that and the next word.
TERMINATORS = frozenset(".!?:")
OPENERS = frozenset("\"'“”‘’([{«")


def source_for(tell: Tell, doc: Doc) -> str:
    """The text this tell's pattern is written against."""
    return doc.text if tell.category in RAW_TEXT_CATEGORIES else doc.plain


def at_sentence_start(source: str, start: int) -> bool:
    """True when position `start` opens a sentence, a line, or the text."""
    i = start - 1
    saw_newline = False
    while i >= 0 and (source[i].isspace() or source[i] in OPENERS):
        if source[i] == "\n":
            saw_newline = True
        i -= 1
    if i < 0 or saw_newline:
        return True
    char = source[i]
    if char in TERMINATORS and char != ".":
        return True
    if char == ".":
        # "the meeting ended. Foster spoke" opens a sentence; "Ms. Harness"
        # does not, and telling them apart is exactly what _is_no_split does.
        return not _is_no_split(source[: i + 1], source[start:])
    return False


def is_proper_noun_use(source: str, start: int) -> bool:
    """True when the match at `start` reads as a name rather than as the word."""
    if start >= len(source) or not source[start].isupper():
        return False
    return not at_sentence_start(source, start)


def finditer_guarded(
    pattern: re.Pattern[str], source: str, guard: bool
) -> Iterator[re.Match[str]]:
    """Every match, minus the ones the proper-noun guard rejects."""
    for match in pattern.finditer(source):
        if guard and is_proper_noun_use(source, match.start()):
            continue
        yield match


def search_guarded(tell: Tell, text: str) -> re.Match[str] | None:
    """First surviving match of a tell in `text` — what the registry validates."""
    return next(finditer_guarded(tell.compiled(), text, tell.proper_noun_guard), None)


class RegexDetector(BaseDetector):
    """Count (or flag) a compiled pattern's matches in the right view of a doc."""

    def __init__(self, tell: Tell) -> None:
        super().__init__(tell)
        if tell.method != "regex":
            raise ValueError(f"{tell.id}: not a regex tell ({tell.method})")
        # Compiled once, at build time: a bad pattern fails the run immediately
        # rather than on whichever document happens to reach it first.
        self.pattern: re.Pattern[str] = tell.compiled()
        self.raw_text = tell.category in RAW_TEXT_CATEGORIES
        self.guard = bool(tell.proper_noun_guard)

    def detect(self, doc: Doc) -> Detection:
        source = source_for(self.tell, doc)

        count = 0
        dropped = 0
        matches: list[dict] = []
        for match in self.pattern.finditer(source):
            if self.guard and is_proper_noun_use(source, match.start()):
                dropped += 1
                continue
            count += 1
            if len(matches) < MAX_MATCHES:
                matches.append(self.quote(source, match.start(), match.end()))

        if self.tell.unit == "binary":
            raw = 1.0 if count else 0.0
            rate = None
        elif self.tell.unit == "count":
            raw = float(count)
            # No words, no rate. Returning None rather than 0.0 keeps an empty
            # document out of the pooled distribution instead of anchoring it.
            rate = (1000.0 * count / doc.words) if doc.words > 0 else None
        else:
            raise ValueError(
                f"{self.tell.id}: regex tells cannot use unit {self.tell.unit!r}"
            )

        return Detection(
            tell_id=self.tell.id,
            doc_id=doc.doc_id,
            raw=raw,
            rate_per_1k=rate,
            matches=matches,
            method="regex",
            unit=self.tell.unit,
            # Recorded only when it bit, so the common case stays {} and a
            # reviewer can measure what the guard is actually costing.
            detail={"guard_dropped": dropped} if dropped else {},
        )
