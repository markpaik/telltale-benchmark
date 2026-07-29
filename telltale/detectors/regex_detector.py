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
"""

from __future__ import annotations

import re

from telltale.corpus import Doc
from telltale.detectors.base import MAX_MATCHES, BaseDetector, Detection
from telltale.registry import Tell

# Categories whose patterns are written against markdown syntax.
RAW_TEXT_CATEGORIES = frozenset({"punctuation", "structural"})


def source_for(tell: Tell, doc: Doc) -> str:
    """The text this tell's pattern is written against."""
    return doc.text if tell.category in RAW_TEXT_CATEGORIES else doc.plain


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

    def detect(self, doc: Doc) -> Detection:
        source = source_for(self.tell, doc)

        count = 0
        matches: list[dict] = []
        for match in self.pattern.finditer(source):
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
            detail={},
        )
