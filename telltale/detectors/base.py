"""What a detector is, and how one gets built from a registry entry.

A detector turns one `Tell` plus one `Doc` into one `Detection`: a raw number,
an optional rate, and the evidence that produced it. Nothing here normalizes,
weights, or compares — scoring.py owns all of that. The split matters because
evidence has to survive independently of the scale it is later put on: a run
whose weights change should not need re-detection, and a disputed number should
be answerable with the quotes that produced it.

Three methods exist in the registry. Two of them are deterministic and land
here (`regex`, `statistic`); the third (`judge`) needs a model in the loop and
arrives in M6. Until then `build` refuses judge tells loudly rather than
returning a detector that silently scores zero — a zero is indistinguishable
from "clean" downstream, and that would quietly understate every model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from telltale.corpus import Doc
from telltale.registry import Tell

# Evidence limits. Fifty matches is far more than a reader will ever check and
# still small enough that a pathological document cannot blow up the run;
# the count in `raw` is never truncated, only the quote list is.
MAX_MATCHES = 50
CONTEXT_CHARS = 60


@dataclass(frozen=True)
class Detection:
    """One tell measured against one document.

    `raw` carries the measurement in the tell's own unit: a match count
    (`count`), 0.0/1.0 (`binary`), or the statistic's value (`value`, which may
    be NaN when the statistic's input floor is not met). `rate_per_1k` is set
    only for count tells, and only when the document has words to divide by.
    """

    tell_id: str
    doc_id: str
    raw: float
    rate_per_1k: float | None
    matches: list[dict[str, Any]]
    method: str
    unit: str
    detail: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class Detector(Protocol):
    """Anything that can measure one tell against one document."""

    tell: Tell

    def detect(self, doc: Doc) -> Detection: ...

    def applies_to(self, doc: Doc) -> bool: ...


class BaseDetector:
    """Shared behaviour: format scoping and the evidence helpers."""

    def __init__(self, tell: Tell) -> None:
        self.tell = tell

    def applies_to(self, doc: Doc) -> bool:
        """False when the tell declares formats and this document is not one.

        A greeting tell ("I hope this finds you well") is not a miss on a white
        paper; it is not a question that was asked. Callers skip the row rather
        than record a zero, so out-of-scope documents never dilute a rate.
        """
        if self.tell.formats is None:
            return True
        return doc.fmt in self.tell.formats

    def detect(self, doc: Doc) -> Detection:  # pragma: no cover - abstract
        raise NotImplementedError

    # -- evidence --

    @staticmethod
    def quote(source: str, start: int, end: int) -> dict[str, Any]:
        """A match with +/-60 characters of context and a 1-based line number.

        Whitespace inside the window is collapsed so a quote is one line however
        the match straddled the source, and an ellipsis marks each end that was
        cut. The line number counts newlines in the *source actually searched*,
        which is the raw markdown for structural tells and the stripped prose for
        lexical ones — see regex_detector for why those are different texts.
        """
        left = max(0, start - CONTEXT_CHARS)
        right = min(len(source), end + CONTEXT_CHARS)
        window = " ".join(source[left:right].split())
        if left > 0:
            window = "…" + window
        if right < len(source):
            window = window + "…"
        return {"quote": window, "line": source.count("\n", 0, start) + 1}


class JudgeDetector(BaseDetector):
    """Seam for M6. Delegates to an injected judge; there is no default one."""

    def __init__(self, tell: Tell, judge: Any) -> None:
        super().__init__(tell)
        self.judge = judge

    def detect(self, doc: Doc) -> Detection:
        detection = self.judge(self.tell, doc)
        if not isinstance(detection, Detection):
            raise TypeError(
                f"judge for {self.tell.id} returned {type(detection).__name__}, "
                "expected a Detection"
            )
        return detection


def build(tell: Tell, judge: Any | None = None) -> Detector:
    """Return the detector for one registry entry.

    `judge` is the seam for M6: pass a callable `(tell, doc) -> Detection` and
    judge tells become scoreable. Without one they raise, so a Tier-1 run has to
    skip them deliberately and report how many it skipped.
    """
    from telltale.detectors.regex_detector import RegexDetector
    from telltale.detectors.stat_detector import StatDetector

    if tell.method == "regex":
        return RegexDetector(tell)
    if tell.method == "statistic":
        return StatDetector(tell)
    if tell.method == "judge":
        if judge is None:
            raise NotImplementedError(
                f"M6: judge tells need a judge backend ({tell.id})"
            )
        return JudgeDetector(tell, judge)
    raise ValueError(f"{tell.id}: unknown detection method {tell.method!r}")
