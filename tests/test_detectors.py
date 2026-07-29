"""Tier-1 detectors: counting, flagging, routing, and the evidence they carry.

Every expected number here is worked out from the fixture by hand. The fixtures
are small enough to count on your fingers on purpose — a detector test that
needs a calculator is testing the calculator.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from telltale import textstats
from telltale.corpus import Doc
from telltale.detectors import (
    MAX_MATCHES,
    Detection,
    RegexDetector,
    StatDetector,
    build,
    source_for,
)
from telltale.registry import Registry, Tell

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"
REGISTRY = Registry(REGISTRY_PATH)


def make(text: str, fmt: str = "memo", doc_id: str = "test-model/memo-01") -> Doc:
    return Doc.from_text(doc_id, "test-model", fmt, text)


def tell(**overrides) -> Tell:
    base = dict(
        id="lex.fixture",
        name="fixture",
        category="lexical",
        scope="general",
        method="regex",
        unit="count",
        pattern=r"\bwidget\b",
        flags=(),
        status="active",
    )
    base.update(overrides)
    return Tell(**base)


# --- counting ----------------------------------------------------------------


def test_count_unit_counts_every_match() -> None:
    doc = make("A widget and a widget and one more widget.")
    detection = build(tell()).detect(doc)
    assert detection.raw == 3.0
    assert len(detection.matches) == 3
    assert detection.method == "regex"
    assert detection.unit == "count"
    assert detection.detail == {}


def test_count_rate_is_per_thousand_prose_words() -> None:
    # Eight words, one match: 1 / 8 * 1000 = 125.0 per 1k.
    doc = make("One widget sits here in this short line")
    assert doc.words == 8
    detection = build(tell()).detect(doc)
    assert detection.rate_per_1k == pytest.approx(125.0)


def test_empty_document_has_no_rate() -> None:
    doc = make("")
    detection = build(tell()).detect(doc)
    assert detection.raw == 0.0
    assert detection.rate_per_1k is None


def test_binary_unit_is_one_however_many_matches() -> None:
    doc = make("A widget and a widget and one more widget.")
    detection = build(tell(unit="binary")).detect(doc)
    assert detection.raw == 1.0
    assert detection.rate_per_1k is None
    # The flag is 1.0 but the evidence is not thrown away.
    assert len(detection.matches) == 3


def test_binary_unit_is_zero_on_a_miss() -> None:
    detection = build(tell(unit="binary")).detect(make("Nothing here."))
    assert detection.raw == 0.0
    assert detection.matches == []


def test_matches_are_capped_but_the_count_is_not() -> None:
    doc = make("widget " * 80)
    detection = build(tell()).detect(doc)
    assert detection.raw == 80.0
    assert len(detection.matches) == MAX_MATCHES


def test_regex_flags_come_from_the_registry() -> None:
    doc = make("A WIDGET in shouting caps.")
    assert build(tell()).detect(doc).raw == 0.0
    assert build(tell(flags=("IGNORECASE",))).detect(doc).raw == 1.0


# --- plain vs raw routing ----------------------------------------------------

FENCED = """# Widget report

The team met.

```python
widget = "this is code, not prose"
```

| column | widget |
|--------|--------|
| a      | b      |

See the [widget dashboard](https://example.org/widget) for detail.
"""


def test_lexical_patterns_read_the_stripped_prose() -> None:
    """A word inside a code fence, a table, or a URL is not prose."""
    doc = make(FENCED)
    detection = build(tell(flags=("IGNORECASE",))).detect(doc)
    # Two survive stripping: the heading text and the link's anchor text. The
    # fenced assignment, the table cell, and the URL are all gone.
    assert detection.raw == 2.0
    quotes = " ".join(m["quote"] for m in detection.matches)
    assert "this is code" not in quotes
    assert "https://example.org" not in quotes


def test_structural_patterns_read_the_raw_markdown() -> None:
    """A heading pattern cannot fire on text whose `#` markers were stripped."""
    heading = tell(
        id="str.fixture",
        category="structural",
        unit="binary",
        pattern=r"^#{1,4}\s+widget",
        flags=("MULTILINE", "IGNORECASE"),
    )
    doc = make(FENCED)
    assert build(heading).detect(doc).raw == 1.0

    prose_version = tell(
        id="lex.fixture",
        category="lexical",
        unit="binary",
        pattern=r"^#{1,4}\s+widget",
        flags=("MULTILINE", "IGNORECASE"),
    )
    assert build(prose_version).detect(doc).raw == 0.0


@pytest.mark.parametrize(
    ("category", "expected_raw"),
    [("punctuation", True), ("structural", True), ("lexical", False), ("syntactic", False)],
)
def test_routing_is_by_category(category: str, expected_raw: bool) -> None:
    doc = make("# Heading\n\nBody text.\n")
    fixture = tell(id="pnc.fixture" if expected_raw else "lex.fixture", category=category)
    source = source_for(fixture, doc)
    assert (source is doc.text) is expected_raw


def test_shipped_structural_tells_all_route_to_raw_text() -> None:
    """Guards the routing rule against a future tell filed in the wrong category."""
    for entry in REGISTRY.active_tells():
        if entry.method != "regex":
            continue
        detector = RegexDetector(entry)
        assert detector.raw_text == (entry.category in {"punctuation", "structural"})


# --- evidence ----------------------------------------------------------------

LINES = "\n".join(
    [
        "First line of the document.",
        "Second line has a widget in the middle of it.",
        "Third line.",
        "Fourth line also mentions a widget right here.",
    ]
)


def test_quotes_carry_one_based_line_numbers() -> None:
    detection = build(tell()).detect(make(LINES))
    assert [m["line"] for m in detection.matches] == [2, 4]


def test_quote_window_is_sixty_characters_each_side() -> None:
    # "widget" starts at character 100, with 100 characters either side.
    text = "y " * 50 + "widget" + " z" * 50
    assert text.index("widget") == 100
    detection = build(tell()).detect(make(text))
    quote = detection.matches[0]["quote"]
    # 60 characters each side is 30 tokens each side, and both ends are cut.
    assert quote.startswith("…") and quote.endswith("…")
    assert quote.strip("…") == " ".join(["y"] * 30 + ["widget"] + ["z"] * 30)


def test_quote_window_has_no_ellipsis_when_it_reaches_the_edge() -> None:
    detection = build(tell()).detect(make("a widget b"))
    quote = detection.matches[0]["quote"]
    assert quote == "a widget b"


def test_quote_collapses_whitespace_to_one_line() -> None:
    detection = build(tell()).detect(make("before\n\nwidget\n\nafter"))
    assert detection.matches[0]["quote"] == "before widget after"


def test_line_numbers_count_in_the_source_actually_searched() -> None:
    """A structural tell's line number points into the raw file, not the prose.

    The fence and the blank lines around it exist in `text` and not in `plain`,
    so a line number taken from the wrong source would point a reader at the
    wrong line of the document on disk.
    """
    text = "# Title\n\n```\ncode\n```\n\n## Conclusion\n\nDone.\n"
    doc = make(text)
    heading = tell(
        id="str.fixture",
        category="structural",
        pattern=r"^##\s+Conclusion",
        flags=("MULTILINE",),
    )
    detection = build(heading).detect(doc)
    assert detection.matches[0]["line"] == 7
    assert text.split("\n")[6] == "## Conclusion"


# --- format scoping ----------------------------------------------------------


def test_applies_to_is_true_when_no_formats_are_declared() -> None:
    detector = build(tell())
    assert detector.applies_to(make("x", fmt="white-paper"))


def test_applies_to_respects_declared_formats() -> None:
    detector = build(tell(formats=("email", "memo")))
    assert detector.applies_to(make("x", fmt="memo"))
    assert not detector.applies_to(make("x", fmt="white-paper"))


# --- statistic detector ------------------------------------------------------


def stat_tell(**overrides) -> Tell:
    base = dict(
        id="sta.fixture",
        name="fixture stat",
        category="statistical",
        scope="general",
        method="statistic",
        unit="value",
        stat="em_dash_per_1k",
        direction="high_is_telling",
        ramp=(1.5, 6.0),
        status="active",
    )
    base.update(overrides)
    return Tell(**base)


def test_stat_detector_returns_the_statistic() -> None:
    # Two em dashes in ten words: 2 / 10 * 1000 = 200.0 per 1k.
    doc = make("One — two three four — five six seven eight nine ten")
    assert doc.words == 10
    detection = build(stat_tell()).detect(doc)
    assert detection.raw == pytest.approx(200.0)
    assert detection.rate_per_1k is None
    assert detection.matches == []
    assert detection.detail == {"stat": "em_dash_per_1k"}
    assert detection.unit == "value"


def test_stat_detector_passes_nan_through() -> None:
    """A statistic below its input floor stays NaN; it must not become zero."""
    doc = make("Three sentences. Not ten. So burstiness is undefined.")
    detection = build(stat_tell(stat="sentence_length_cv")).detect(doc)
    assert math.isnan(detection.raw)


def test_stat_detector_rejects_an_unregistered_stat() -> None:
    with pytest.raises(KeyError):
        build(stat_tell(stat="not_a_real_stat"))


def test_stat_detector_rejects_a_non_statistic_tell() -> None:
    with pytest.raises(ValueError):
        StatDetector(tell())


def test_regex_detector_rejects_a_non_regex_tell() -> None:
    with pytest.raises(ValueError):
        RegexDetector(stat_tell())


def test_regex_detector_rejects_an_impossible_unit() -> None:
    with pytest.raises(ValueError):
        build(tell(unit="value")).detect(make("widget"))


def test_every_registered_stat_is_reachable_through_a_detector() -> None:
    doc = make("Some prose. " * 30)
    for name in sorted(textstats.STATS):
        detection = build(stat_tell(stat=name)).detect(doc)
        assert detection.detail == {"stat": name}


# --- judge seam --------------------------------------------------------------


def judge_tell() -> Tell:
    return Tell(
        id="rht.fixture",
        name="fixture judge",
        category="syntactic",
        scope="general",
        method="judge",
        unit="count",
        rubric="count the things",
        rubric_version=1,
        judge_view="chunk",
        status="active",
    )


def test_judge_tells_raise_without_a_judge() -> None:
    with pytest.raises(NotImplementedError, match="M6"):
        build(judge_tell())


def test_judge_tells_work_through_an_injected_judge() -> None:
    def fake_judge(entry: Tell, doc: Doc) -> Detection:
        return Detection(
            tell_id=entry.id,
            doc_id=doc.doc_id,
            raw=2.0,
            rate_per_1k=None,
            matches=[{"quote": "a rule of three, four, and five", "line": 1}],
            method="judge",
            unit=entry.unit,
            detail={"rubric_version": entry.rubric_version},
        )

    detection = build(judge_tell(), judge=fake_judge).detect(make("anything"))
    assert detection.raw == 2.0
    assert detection.method == "judge"


def test_a_judge_that_returns_junk_is_rejected() -> None:
    detector = build(judge_tell(), judge=lambda entry, doc: 3.0)
    with pytest.raises(TypeError):
        detector.detect(make("anything"))


def test_unknown_method_is_an_error() -> None:
    with pytest.raises(ValueError, match="unknown detection method"):
        build(tell(method="haruspicy"))


# --- the shipped registry ----------------------------------------------------


def test_every_deterministic_registry_tell_builds() -> None:
    built = 0
    for entry in REGISTRY.active_tells(include_candidates=True):
        if entry.method == "judge":
            with pytest.raises(NotImplementedError):
                build(entry)
            continue
        detector = build(entry)
        detector.detect(make("A short sample document about widgets.\n"))
        built += 1
    assert built > 100
