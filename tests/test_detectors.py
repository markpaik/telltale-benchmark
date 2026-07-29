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
    at_sentence_start,
    build,
    is_proper_noun_use,
    search_guarded,
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


# A list almost always follows a blank line, so this is the shape of nearly
# every real bullet-lead-in match rather than an edge case.
BLANK_LINE_BEFORE_LIST = """# Report

Some paragraph text here.

- **Alpha**: one
- **Beta**: two

1. **First**: a
2. **Second**: b
"""


@pytest.mark.parametrize(
    ("tell_id", "expected_lines"),
    [("pnc.bold-lead-in-bullet", [5, 6]), ("pnc.numbered-bold-lead", [8, 9])],
)
def test_a_blank_line_before_a_list_does_not_shift_the_line_number(
    tell_id: str, expected_lines: list[int]
) -> None:
    """A leading `\\s*` under MULTILINE anchors on the blank line above the list.

    `\\s` matches a newline, so `^\\s*[-*+]` could start at the blank line, eat the
    newline, and still match the bullet — putting the quote's line number one
    line high and pointing a reviewer at an empty line. The character class has
    to be horizontal whitespace only.
    """
    detection = build(REGISTRY.get(tell_id)).detect(make(BLANK_LINE_BEFORE_LIST))
    assert [m["line"] for m in detection.matches] == expected_lines

    source_lines = BLANK_LINE_BEFORE_LIST.split("\n")
    for match, line in zip(detection.matches, expected_lines):
        assert source_lines[line - 1].lstrip().startswith(("-", "1.", "2."))
        assert "**" in source_lines[line - 1]


def test_the_blank_line_fix_did_not_change_what_counts() -> None:
    """Indented and tab-indented continuation items still match."""
    doc = make("Intro.\n\n- **Top**: one\n    - **Nested**: two\n\t- **Tabbed**: three\n")
    detection = build(REGISTRY.get("pnc.bold-lead-in-bullet")).detect(doc)
    assert detection.raw == 3.0
    assert [m["line"] for m in detection.matches] == [3, 4, 5]


def test_a_list_at_the_very_top_of_a_document_still_matches() -> None:
    doc = make("- **Alpha**: one\n- **Beta**: two\n")
    detection = build(REGISTRY.get("pnc.bold-lead-in-bullet")).detect(doc)
    assert detection.raw == 2.0
    assert [m["line"] for m in detection.matches] == [1, 2]


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


# --- the proper-noun guard ---------------------------------------------------
#
# The five sentences QA reproduced the class defect with. Each fires the bare
# pattern and must not survive the guard.

QA_REPRO = [
    ("lex.foster", "The event was held at Foster Elementary School."),
    ("lex.harness", "Ms. Harness led the session on grading policy."),
    ("lex.bolster", "Mr. Bolster asked for the revised timeline."),
    ("lex.streamline", "We hired Streamline Consulting to review the intake process."),
    ("cl.north-star", "Students at North Star Academy improved on every measure."),
]


def guarded(**overrides) -> Tell:
    return tell(proper_noun_guard=True, flags=("IGNORECASE",), **overrides)


@pytest.mark.parametrize(("tell_id", "sentence"), QA_REPRO, ids=[t for t, _ in QA_REPRO])
def test_qa_repro_sentences_no_longer_fire(tell_id: str, sentence: str) -> None:
    entry = REGISTRY.get(tell_id)
    assert entry.proper_noun_guard, f"{tell_id} is expected to carry the guard"
    # The pattern still matches — the guard is what rejects it.
    assert entry.compiled().search(sentence)
    assert search_guarded(entry, sentence) is None
    assert build(entry).detect(make(sentence)).raw == 0.0


def test_the_word_itself_still_counts() -> None:
    """The guard must not cost the tell its actual job."""
    entry = REGISTRY.get("lex.foster")
    doc = make("The new schedule fosters more collaboration between departments.")
    assert build(entry).detect(doc).raw == 1.0


def test_guard_drops_a_mid_sentence_capital() -> None:
    doc = make("We met the Widget team on Tuesday.")
    assert build(guarded()).detect(doc).raw == 0.0
    assert build(tell(flags=("IGNORECASE",))).detect(doc).raw == 1.0


def test_guard_keeps_a_lowercase_match_anywhere() -> None:
    doc = make("We shipped the widget on Tuesday. Another widget followed.")
    assert build(guarded()).detect(doc).raw == 2.0


@pytest.mark.parametrize(
    "text",
    [
        "Widget is the first word of the text.",
        "The meeting ended. Widget spoke next.",
        "Was it done? Widget says yes.",
        "It arrived! Widget confirmed.",
        "One question remains: Widget or nothing.",
        'She replied: "Widget is fine."',
        "He asked around. (Widget was in the room.)",
    ],
)
def test_guard_keeps_sentence_initial_capitals(text: str) -> None:
    """Sentence-initial capitals are ambiguous between word and name, so they stay."""
    assert build(guarded()).detect(make(text)).raw == 1.0


def test_a_mid_sentence_parenthetical_is_not_a_sentence_start() -> None:
    """An opening bracket only carries the exemption when a terminator precedes it."""
    assert build(guarded()).detect(make("He asked (Widget was there) about it.")).raw == 0.0


def test_guard_keeps_the_first_word_of_a_line() -> None:
    """Headings and list items sit on their own line once markdown is stripped."""
    doc = make("# Widget adoption\n\n- Widget rollout is on track\n")
    assert build(guarded()).detect(doc).raw == 2.0


def test_guard_uses_the_projects_own_abbreviation_rule() -> None:
    """"Ms. Harness" is not a new sentence, so the capital is a name."""
    assert build(guarded()).detect(make("We asked Ms. Widget for the file.")).raw == 0.0
    assert build(guarded()).detect(make("The vote passed. Widget abstained.")).raw == 1.0


def test_guard_reports_what_it_dropped() -> None:
    doc = make(
        "Widget Corp. sells them.\n"
        "We met the Widget team on Tuesday.\n"
        "The widget policy is unchanged.\n"
    )
    detection = build(guarded()).detect(doc)
    # Line 1 opens the text and line 3 is lowercase, so both survive. Line 2 is a
    # capital in the middle of a sentence: a name, and dropped.
    assert detection.raw == 2.0
    assert detection.detail == {"guard_dropped": 1}
    assert [m["line"] for m in detection.matches] == [1, 3]


def test_an_unguarded_tell_reports_no_guard_detail() -> None:
    doc = make("We met the Widget team about widget policy.")
    assert build(tell(flags=("IGNORECASE",))).detect(doc).detail == {}


def test_at_sentence_start_edges() -> None:
    assert at_sentence_start("", 0)
    assert at_sentence_start("Widget", 0)
    assert at_sentence_start("a.\nWidget", 3)
    assert not at_sentence_start("a Widget", 2)


def test_is_proper_noun_use_ignores_lowercase_and_punctuation_starts() -> None:
    assert not is_proper_noun_use("a widget", 2)
    assert not is_proper_noun_use("a 3-widget rack", 2)
    assert not is_proper_noun_use("short", 99)  # past the end
    assert is_proper_noun_use("a Widget", 2)


def test_the_guard_is_off_unless_the_registry_asks_for_it() -> None:
    assert tell().proper_noun_guard is False
    assert not build(tell()).guard
    unguarded = [t for t in REGISTRY.active_tells() if t.method == "regex" and not t.proper_noun_guard]
    assert len(unguarded) > 60, "the guard is meant to be opt-in, not the default"


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
