"""Statistic tells: one registered `textstats` function, one number.

There is no evidence list for a statistic — the "quote" for a burstiness score
is the whole document — so `matches` is always empty and `detail` names the
function, which is what makes a suspicious number traceable.

NaN is a first-class result, not a failure. Every stat returns NaN when its
input floor is not met (fewer than ten sentences, no bullet lists at all), and
that NaN has to survive all the way to scoring, where it is *excluded* from
means rather than read as zero. A short email that has no measurable sentence
burstiness is not a maximally bursty email.
"""

from __future__ import annotations

from telltale.corpus import Doc
from telltale.detectors.base import BaseDetector, Detection
from telltale.registry import Tell
from telltale import textstats


class StatDetector(BaseDetector):
    """Evaluate one registered statistic against a document."""

    def __init__(self, tell: Tell) -> None:
        super().__init__(tell)
        if tell.method != "statistic":
            raise ValueError(f"{tell.id}: not a statistic tell ({tell.method})")
        if not tell.stat or tell.stat not in textstats.STATS:
            raise KeyError(f"{tell.id}: unknown stat {tell.stat!r}")
        self.stat = tell.stat

    def detect(self, doc: Doc) -> Detection:
        value = float(textstats.compute(self.stat, doc))
        return Detection(
            tell_id=self.tell.id,
            doc_id=doc.doc_id,
            raw=value,
            rate_per_1k=None,
            matches=[],
            method="statistic",
            unit=self.tell.unit,
            detail={"stat": self.stat},
        )
