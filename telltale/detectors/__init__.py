"""Tier-1 detectors: deterministic measurement of one tell against one document.

    from telltale.detectors import build
    detection = build(tell).detect(doc)

`build` dispatches on `detection.method`. Judge tells need a backend passed in —
`build(tell, judge=JudgeBackend(client))`, see `telltale.judge` — and raise
NotImplementedError without one, so a Tier-1 run has to skip them deliberately
rather than scoring them zero.
"""

from telltale.detectors.base import (
    CONTEXT_CHARS,
    MAX_MATCHES,
    BaseDetector,
    Detection,
    Detector,
    JudgeDetector,
    build,
)
from telltale.detectors.regex_detector import (
    RAW_TEXT_CATEGORIES,
    RegexDetector,
    at_sentence_start,
    finditer_guarded,
    is_proper_noun_use,
    search_guarded,
    source_for,
)
from telltale.detectors.stat_detector import StatDetector

__all__ = [
    "CONTEXT_CHARS",
    "MAX_MATCHES",
    "RAW_TEXT_CATEGORIES",
    "BaseDetector",
    "Detection",
    "Detector",
    "JudgeDetector",
    "RegexDetector",
    "StatDetector",
    "at_sentence_start",
    "build",
    "finditer_guarded",
    "is_proper_noun_use",
    "search_guarded",
    "source_for",
]
