"""Gate 5: is this candidate already in the registry under another name?

A discovery pipeline that cannot recognize its own prior findings fills the
registry with synonyms, and a registry full of synonyms silently triple-counts
one habit in the index. So a candidate is compared to the registry three ways,
and the three are deliberately different in kind:

* **Pattern identity** catches the literal re-proposal — `\\bdelve\\b` against
  `\\bdelv(?:e|es|ed|ing)\\b`. Cheap, exact, and narrow: it only sees textual
  sameness, so it is a first pass and never the only one.
* **Behavioural overlap** catches the same tell written differently. If two
  patterns fire on the same documents (Jaccard of the matched-document sets)
  *and* fire the same number of times within each document (Spearman rho of the
  per-document counts), they are measuring one thing whatever they look like.
  Both are required: Jaccard alone would merge two common tells that appear in
  every document, and rho alone would merge two rare tells that both fire once
  in the documents where they fire at all.
* **Name similarity** catches the human-facing collision — "rich tapestry" and
  "tapestry" read as duplicates in a scorecard even when they measure different
  things. This one only *flags*: a name clash is a naming problem, and
  auto-rejecting on it would throw away a real finding because someone had
  already used the obvious word for it.

Rank correlation rather than Pearson, and computed here rather than borrowed:
counts per document are heavily skewed (most documents zero, one document nine),
and Pearson on that is a report about the outlier. Ranks are also why this needs
no scipy — `pandas.Series.rank` plus a Pearson on the ranks *is* Spearman.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

#: Both must hold before two detectors are called the same detector.
JACCARD_DUPLICATE = 0.8
SPEARMAN_DUPLICATE = 0.9

#: Name similarity that earns a human look, not a rejection.
NAME_FUZZ_FLAG = 0.85

_FLAG_INLINE = re.compile(r"\(\?[aiLmsux]+\)")
_NONCAPTURING = re.compile(r"\(\?:")
_WHITESPACE = re.compile(r"\s+")


def normalize_pattern(pattern: str) -> str:
    """A coarse canonical form for comparing two regexes as text.

    Deliberately coarse. Deciding whether two regular expressions accept the
    same language is not something to attempt here, and a normalizer that tried
    would be wrong in ways nobody could audit. This one folds the differences
    that are pure notation — case, whitespace, inline flag groups, non-capturing
    group syntax, redundant escaping of literals — and stops. Everything it
    misses is exactly what the behavioural test is for.
    """
    text = str(pattern or "")
    text = _FLAG_INLINE.sub("", text)
    text = _NONCAPTURING.sub("(", text)
    text = _WHITESPACE.sub("", text)
    text = re.sub(r"\\([-_/'\", ])", r"\1", text)
    return text.lower()


def patterns_match(candidate: str, existing: str) -> bool:
    """True when two patterns are the same up to notation."""
    left, right = normalize_pattern(candidate), normalize_pattern(existing)
    return bool(left) and left == right


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    """|A ∩ B| / |A ∪ B|. Two empty sets overlap on nothing, so: 0.0."""
    a, b = set(left), set(right)
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    """Rank correlation of two equal-length series. NaN when it is undefined.

    Ties get average ranks (pandas' default), which is what makes this usable on
    count data where "zero" is most of the sample. A series with no variation
    has no rank correlation with anything — that is NaN, not zero, and the
    caller must not read it as "not a duplicate" on its own.
    """
    if len(left) != len(right) or len(left) < 3:
        return float("nan")
    a = pd.Series(list(left), dtype="float64").rank()
    b = pd.Series(list(right), dtype="float64").rank()
    if a.nunique() < 2 or b.nunique() < 2:
        return float("nan")
    return float(a.corr(b))


def name_fuzz(name: str, existing: Mapping[str, str]) -> tuple[str, float]:
    """The registry entry whose name reads most like this one, and how close.

    `existing` maps tell id -> name. Ties break on the id, so the answer does not
    depend on dictionary order.
    """
    best_id, best_ratio = "", 0.0
    target = str(name or "").strip().lower()
    if not target:
        return best_id, best_ratio
    for tell_id in sorted(existing):
        ratio = difflib.SequenceMatcher(
            None, target, str(existing[tell_id] or "").strip().lower()
        ).ratio()
        if ratio > best_ratio:
            best_id, best_ratio = tell_id, ratio
    return best_id, best_ratio


@dataclass
class DedupResult:
    """What gate 5 found: a duplicate, a name clash, or neither."""

    duplicate_of: str = ""
    reason: str = ""
    flags: list[str] = field(default_factory=list)
    #: Per-tell (jaccard, rho) for everything actually compared, for the record.
    overlaps: dict[str, tuple[float, float]] = field(default_factory=dict)
    name_match: tuple[str, float] = ("", 0.0)

    @property
    def is_duplicate(self) -> bool:
        return bool(self.duplicate_of)

    def as_dict(self) -> dict[str, Any]:
        return {
            "duplicate_of": self.duplicate_of,
            "reason": self.reason,
            "flags": list(self.flags),
            "overlaps": {
                k: {"jaccard": round(j, 4), "spearman": (None if r != r else round(r, 4))}
                for k, (j, r) in sorted(self.overlaps.items())
            },
            "name_match": {
                "tell_id": self.name_match[0],
                "ratio": round(self.name_match[1], 4),
            },
        }


def behavioural_duplicate(
    candidate_counts: Mapping[str, float],
    tell_counts: Mapping[str, float],
    jaccard_min: float = JACCARD_DUPLICATE,
    rho_min: float = SPEARMAN_DUPLICATE,
) -> tuple[bool, float, float]:
    """(duplicate, jaccard, rho) for one candidate against one existing tell.

    Both series are keyed by doc_id over the same corpus, so the comparison is
    aligned document by document rather than by position.
    """
    doc_ids = sorted(set(candidate_counts) | set(tell_counts))
    left = [float(candidate_counts.get(d, 0.0)) for d in doc_ids]
    right = [float(tell_counts.get(d, 0.0)) for d in doc_ids]
    overlap = jaccard(
        [d for d, v in zip(doc_ids, left) if v > 0],
        [d for d, v in zip(doc_ids, right) if v > 0],
    )
    rho = spearman(left, right)
    duplicate = overlap >= jaccard_min and rho == rho and rho >= rho_min
    return duplicate, overlap, rho


def dedup_check(
    candidate: Mapping[str, Any],
    candidate_counts: Mapping[str, float],
    existing_patterns: Mapping[str, str],
    existing_counts: Mapping[str, Mapping[str, float]],
    existing_names: Mapping[str, str],
    jaccard_min: float = JACCARD_DUPLICATE,
    rho_min: float = SPEARMAN_DUPLICATE,
    name_min: float = NAME_FUZZ_FLAG,
) -> DedupResult:
    """Run all three comparisons. Pattern identity short-circuits; naming never does."""
    result = DedupResult()
    result.name_match = name_fuzz(str(candidate.get("name") or ""), existing_names)
    if result.name_match[1] >= name_min:
        result.flags.append(
            f"name-fuzz:{result.name_match[0]}:{result.name_match[1]:.2f}"
        )

    rule = candidate.get("rule") or {}
    pattern = str(rule.get("pattern") or "") if isinstance(rule, Mapping) else ""
    if pattern:
        for tell_id in sorted(existing_patterns):
            if patterns_match(pattern, existing_patterns[tell_id]):
                result.duplicate_of = tell_id
                result.reason = (
                    f"pattern is textually identical to {tell_id} once notation is "
                    f"normalized"
                )
                return result

    for tell_id in sorted(existing_counts):
        duplicate, overlap, rho = behavioural_duplicate(
            candidate_counts, existing_counts[tell_id], jaccard_min, rho_min
        )
        result.overlaps[tell_id] = (overlap, rho)
        if duplicate and not result.duplicate_of:
            result.duplicate_of = tell_id
            result.reason = (
                f"fires on the same documents as {tell_id} (Jaccard {overlap:.2f} >= "
                f"{jaccard_min}) with the same per-document counts (Spearman "
                f"{rho:.2f} >= {rho_min})"
            )
    return result


__all__ = [
    "JACCARD_DUPLICATE",
    "NAME_FUZZ_FLAG",
    "SPEARMAN_DUPLICATE",
    "DedupResult",
    "behavioural_duplicate",
    "dedup_check",
    "jaccard",
    "name_fuzz",
    "normalize_pattern",
    "patterns_match",
    "spearman",
]
