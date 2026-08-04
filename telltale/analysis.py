"""Where in a document a tell fired, relative to the seams the harness left.

A document longer than one model turn is stitched: the harness asks for a
continuation and concatenates. Every stitch is a place where the model saw its
own prose as context and resumed — and resuming is exactly the situation that
produces a recap, a fresh scene-setter, a bolded restatement of what came
before. If a tell fires disproportionately at those joins, the benchmark is
partly measuring its own generation harness rather than the model's prose, and
any cross-model comparison inherits that bias, because the two models were not
stitched equally often.

So: for every match, how far is it from the nearest continuation boundary, and
is that closer than chance?

**Matches are located by quote, not by line number.** A match's recorded `line`
counts newlines in *the source that detector searched*, which is the stripped
prose for lexical tells, the raw markdown for structural ones, the current chunk
for a judge span tell, and a synthesized skeleton for a judge structural tell.
Four different coordinate systems, none of which is the document. Joining them
against a character offset produces confident nonsense — measured on the
shakedown run, a line-number join put 0 of 152 `pnc.bold-lead-in-bullet` matches
near a seam where chance alone predicted 9. Quotes are verbatim, so the text is
searched for the quote instead, whitespace-flexibly, and anything that cannot be
found is counted as unlocated rather than guessed at.

The null matters as much as the raw share. A 30,000-character document with one
boundary has about 400 characters — 1.3% of itself — inside a 200-character
window, so "3% of matches sit at a seam" is not evidence of anything, and a raw
threshold alone would flag whichever tell happens to fire in short documents.
Every number is reported against the share of that document's positions a match
of the same length could occupy inside the window, and the ratio of the two is
the finding. A tell with no seam preference lands at 1.0.
"""

from __future__ import annotations

import json
import re
from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from telltale.corpus import Doc

#: Characters either side of a boundary that count as "at the seam". A model
#: resuming its own prose re-establishes context in roughly a paragraph.
DEFAULT_WINDOW = 200

#: Above this share-over-chance a tell fires near seams often enough that the
#: harness, not the model, is a live explanation.
ENRICHMENT_FLAG = 2.0

#: And above this raw share, enough of the tell's evidence sits at seams that
#: the finding itself is in question regardless of the null.
SHARE_FLAG = 0.30

#: Below this many located matches a cell is too thin to flag on.
MIN_MATCHES = 10

_ELLIPSIS = "…"


# --- locating a match in the document ----------------------------------------


def _flexible(fragment: str) -> re.Pattern[str]:
    """A pattern matching `fragment` with any whitespace between its tokens.

    Evidence quotes are whitespace-collapsed when recorded, so a quote that
    straddled a line break is one line by the time it reaches the score file.
    """
    tokens = fragment.split()
    return re.compile(r"\s+".join(re.escape(token) for token in tokens))


def locate(text: str, quote: str) -> tuple[int, int] | None:
    """Character span of a recorded quote in the document, or None.

    Tries the whole quote first, then shorter runs taken from its middle. The
    middle is where the actual match sits — the ends are context, and context is
    where markdown that the detector stripped is most likely to reappear.
    """
    core = (quote or "").strip().strip(_ELLIPSIS).strip()
    if not core:
        return None
    for candidate in _candidates(core):
        found = _flexible(candidate).search(text)
        if found is not None:
            return found.start(), found.end()
    return None


def _candidates(core: str) -> list[str]:
    """The whole quote, then progressively shorter windows from its centre."""
    out = [core]
    if "\\|" in core:  # escaped for a markdown table on the way in
        out.append(core.replace("\\|", "|"))
    middle = len(core) // 2
    for width in (60, 40, 24):
        if len(core) > width:
            out.append(core[max(0, middle - width // 2) : middle + width // 2].strip())
    return [c for c in out if len(c.strip()) >= 8]


def distance_to_boundary(span: tuple[int, int], boundaries: Sequence[int]) -> int | None:
    """Characters from an interval to the nearest boundary; 0 if it straddles one.

    None when the document has no boundaries — an unstitched document has no
    seam to be near, which is different from being far from one.
    """
    if not boundaries:
        return None
    start, end = span
    ordered = sorted(boundaries)
    best: int | None = None
    # Both ends of the interval are probed, each against the boundary just below
    # and just above it, so a boundary inside the interval scores zero without a
    # separate straddle test.
    for offset in (start, end):
        position = bisect_right(ordered, offset)
        for candidate in (position - 1, position):
            if 0 <= candidate < len(ordered):
                value = ordered[candidate]
                gap = 0 if start <= value <= end else abs(value - offset)
                best = gap if best is None else min(best, gap)
    return best


def chance_share(
    length: int, span_length: int, boundaries: Sequence[int], window: int
) -> float:
    """Share of the positions a span of this length could occupy that are at a seam.

    The exact null for "a match of this size dropped uniformly into this
    document". Windows that overlap are unioned, so two boundaries close
    together do not double-count.
    """
    room = length - span_length
    if room <= 0 or not boundaries:
        return 0.0
    # A span starts anywhere in [0, room-1]. It touches the window around a
    # boundary b when its start lies in [b - window - span_length, b + window].
    intervals = sorted(
        (max(0, b - window - span_length), min(room - 1, b + window)) for b in boundaries
    )
    covered = 0
    reach = -1
    for start, end in intervals:
        start = max(start, reach + 1)
        if end >= start:
            covered += end - start + 1
            reach = end
    return covered / room


def boundaries_of(doc: Doc) -> list[int]:
    raw = doc.sidecar.get("continuation_boundaries") or []
    return [int(b) for b in raw if isinstance(b, (int, float))]


def stitching_of(doc: Doc) -> str:
    """"stitched" if the harness had to ask for a continuation, else "single"."""
    return "stitched" if boundaries_of(doc) else "single"


def cohort_of(doc: Doc) -> str:
    """The comparison cell: model, split by whether the harness stitched it."""
    return f"{doc.model} {stitching_of(doc)}"


# --- the report --------------------------------------------------------------


@dataclass
class SeamGroup:
    """Seam statistics for one (tell, cohort) cell."""

    tell_id: str
    cohort: str
    method: str = ""
    docs: int = 0
    stitched_docs: int = 0
    matches: int = 0
    located: int = 0
    unlocated: int = 0
    near_seam: int = 0
    expected_near: float = 0.0
    truncated_rows: int = 0

    @property
    def share(self) -> float:
        """Share of located matches in stitched documents that sit at a seam."""
        return self.near_seam / self.located if self.located else 0.0

    @property
    def expected_share(self) -> float:
        return self.expected_near / self.located if self.located else 0.0

    @property
    def enrichment(self) -> float | None:
        """Observed share over chance. None when chance is zero — nothing to beat."""
        expected = self.expected_share
        return (self.share / expected) if expected > 0 else None

    @property
    def flagged(self) -> bool:
        enrichment = self.enrichment
        return self.located >= MIN_MATCHES and (
            self.share > SHARE_FLAG
            or (enrichment is not None and enrichment >= ENRICHMENT_FLAG)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "tell_id": self.tell_id,
            "cohort": self.cohort,
            "method": self.method,
            "docs": self.docs,
            "stitched_docs": self.stitched_docs,
            "matches": self.matches,
            "located": self.located,
            "unlocated": self.unlocated,
            "near_seam": self.near_seam,
            "share": round(self.share, 4),
            "expected_share": round(self.expected_share, 4),
            "enrichment": None if self.enrichment is None else round(self.enrichment, 2),
            "flagged": self.flagged,
            "truncated_rows": self.truncated_rows,
        }


@dataclass
class SeamReport:
    window: int
    groups: list[SeamGroup] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def flagged(self) -> list[SeamGroup]:
        return [g for g in self.groups if g.flagged]

    def as_dict(self) -> dict[str, Any]:
        return {
            "window": self.window,
            "groups": [g.as_dict() for g in self.groups],
            "flagged": [g.as_dict() for g in self.flagged()],
            "notes": list(self.notes),
        }

    def table(self, min_located: int = 0) -> str:
        header = (
            f"{'tell':<30} {'cohort':<26} {'meth':<9} {'docs':>4} {'loc':>5} "
            f"{'unloc':>5} {'seam':>5} {'share':>7} {'chance':>7} {'enr':>6}  flag"
        )
        lines = [header, "-" * len(header)]
        for group in self.groups:
            if group.located < min_located:
                continue
            enrichment = group.enrichment
            lines.append(
                f"{group.tell_id:<30} {group.cohort:<26} {group.method:<9} "
                f"{group.docs:>4} {group.located:>5} {group.unlocated:>5} "
                f"{group.near_seam:>5} {group.share:>6.1%} {group.expected_share:>6.1%} "
                f"{'   n/a' if enrichment is None else f'{enrichment:>6.2f}'}"
                f"  {'FLAG' if group.flagged else ''}"
            )
        return "\n".join(lines)


def seam_report(
    docs: Iterable[Doc],
    rows: Iterable[dict[str, Any]],
    window: int = DEFAULT_WINDOW,
    cohort: Any = cohort_of,
    max_matches: int = 50,
) -> SeamReport:
    """Join score rows against each document's continuation boundaries.

    `rows` are score records as written to scores.jsonl. `cohort` maps a Doc to
    the cell it belongs in; the default splits each model by stitched vs single
    turn, which is the comparison that answers "is this a harness artifact".

    Only stitched documents contribute to the seam numbers — a single-turn
    document has no seam, so counting its matches as "far from one" would
    dilute every share by however much of the corpus fit in one turn.
    """
    by_id = {doc.doc_id: doc for doc in docs}
    groups: dict[tuple[str, str], SeamGroup] = {}
    seen_docs: dict[tuple[str, str], set[str]] = defaultdict(set)
    seen_stitched: dict[tuple[str, str], set[str]] = defaultdict(set)
    unknown: set[str] = set()

    for row in rows:
        doc_id = str(row.get("doc_id"))
        doc = by_id.get(doc_id)
        if doc is None:
            unknown.add(doc_id)
            continue
        tell_id = str(row.get("tell_id"))
        cell = (tell_id, str(cohort(doc)))
        group = groups.setdefault(
            cell,
            SeamGroup(tell_id=tell_id, cohort=cell[1], method=str(row.get("method") or "")),
        )
        seen_docs[cell].add(doc_id)
        boundaries = boundaries_of(doc)
        if boundaries:
            seen_stitched[cell].add(doc_id)

        matches = row.get("matches") or []
        group.matches += len(matches)
        if len(matches) >= max_matches:
            group.truncated_rows += 1
        if not boundaries or not matches:
            continue

        text = doc.text
        for match in matches:
            span = locate(text, str(match.get("quote") or ""))
            if span is None:
                group.unlocated += 1
                continue
            group.located += 1
            group.expected_near += chance_share(
                len(text), span[1] - span[0], boundaries, window
            )
            gap = distance_to_boundary(span, boundaries)
            if gap is not None and gap <= window:
                group.near_seam += 1

    for cell, group in groups.items():
        group.docs = len(seen_docs[cell])
        group.stitched_docs = len(seen_stitched[cell])

    report = SeamReport(
        window=window,
        groups=sorted(groups.values(), key=lambda g: (g.tell_id, g.cohort)),
    )
    if unknown:
        report.notes.append(
            f"{len(unknown)} document id(s) in the score rows are not in the corpus"
        )
    truncated = sum(g.truncated_rows for g in report.groups)
    if truncated:
        report.notes.append(
            f"{truncated} (document, tell) rows hit the {max_matches}-match record "
            "cap; their later matches are not in this analysis, which biases it "
            "against finding late-document seams"
        )
    unlocated = sum(g.unlocated for g in report.groups)
    located = sum(g.located for g in report.groups)
    if unlocated:
        report.notes.append(
            f"{unlocated} of {unlocated + located} matches in stitched documents "
            "could not be located by quote and are excluded rather than guessed at"
        )
    return report


# --- the other half: whole-document divergence -------------------------------


@dataclass
class CohortRate:
    """A tell's mean rate in one cohort, for the stitched-vs-single comparison."""

    tell_id: str
    cohort: str
    docs: int
    mean: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "tell_id": self.tell_id,
            "cohort": self.cohort,
            "docs": self.docs,
            "mean": round(self.mean, 5),
        }


def cohort_rates(
    docs: Iterable[Doc],
    rows: Iterable[dict[str, Any]],
    cohort: Any = cohort_of,
) -> list[CohortRate]:
    """Mean rate per tell per cohort.

    Seam proximity finds a tell that clusters *at* the join. It cannot see a
    tell that the continuation regime turns on for the whole document — the
    shakedown corpus has both, and the second is larger. This is the crude
    companion measure: the same tell's rate in stitched and single-turn
    documents of the same model.

    It is confounded and says so. On the shakedown corpus the confound was not
    length — stitched and single-turn sonnet documents had near-identical
    median word counts — but format: every memo, postmortem, performance review
    and research brief needed a continuation, while every email and literature
    review did not. So the cohorts differ in what they are, and a tell that
    looks stitched-driven here may simply be a bullet-heavy format. Read a
    divergence as a question. Seam proximity, which compares positions inside
    one document, does not carry that confound and is the measure to trust.
    """
    by_id = {doc.doc_id: doc for doc in docs}
    buckets: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        doc = by_id.get(str(row.get("doc_id")))
        if doc is None:
            continue
        value = row.get("rate_per_1k")
        if value is None:
            value = row.get("raw")
        if value is None:
            continue
        buckets[(str(row.get("tell_id")), str(cohort(doc)))].append(float(value))
    return [
        CohortRate(tell_id=tell_id, cohort=name, docs=len(values), mean=sum(values) / len(values))
        for (tell_id, name), values in sorted(buckets.items())
        if values
    ]


def read_scores(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


__all__ = [
    "DEFAULT_WINDOW",
    "ENRICHMENT_FLAG",
    "MIN_MATCHES",
    "SHARE_FLAG",
    "CohortRate",
    "SeamGroup",
    "SeamReport",
    "boundaries_of",
    "chance_share",
    "cohort_of",
    "cohort_rates",
    "distance_to_boundary",
    "locate",
    "read_scores",
    "seam_report",
    "stitching_of",
]
