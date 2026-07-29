"""Tier-1 detectors: deterministic measurement of one tell against one document.

    from telltale.detectors import build
    detection = build(tell).detect(doc)

`build` dispatches on `detection.method`. Judge tells raise NotImplementedError
until M6 supplies a judge backend.
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
from telltale.detectors.regex_detector import RAW_TEXT_CATEGORIES, RegexDetector, source_for
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
    "build",
    "source_for",
]
