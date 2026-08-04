"""Seam-proximity analysis, on documents built so the answer is known.

The fixtures are synthetic on purpose: a real corpus cannot tell you whether a
share of 30% is high, because you do not know what chance was. Here the
boundary is placed by hand, so a tell planted only at the seam must come out
enriched and a tell spread evenly must come out at about 1.0 whatever its raw
share happens to be.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from telltale import analysis
from telltale.corpus import Doc

FILLER = "filler filler filler filler filler filler filler filler filler fille"


def _doc(
    doc_id: str,
    model: str,
    n_lines: int = 100,
    boundary_line: int | None = 50,
    planted: dict[int, str] | None = None,
) -> Doc:
    """A document of `n_lines` 70-character lines, stitched at `boundary_line`.

    Line k (1-indexed) starts at offset (k-1)*71. `planted` replaces the filler
    on the given lines with distinctive text a detector could have quoted.
    """
    lines = [FILLER for _ in range(n_lines)]
    for line_no, content in (planted or {}).items():
        lines[line_no - 1] = content.ljust(len(FILLER), ".")
    text = "\n".join(lines)
    sidecar: dict = {}
    if boundary_line is not None:
        sidecar["continuation_boundaries"] = [(boundary_line - 1) * (len(FILLER) + 1)]
    return Doc.from_text(doc_id=doc_id, model=model, fmt="memo", text=text, sidecar=sidecar)


def _row(doc: Doc, tell_id: str, quotes: list[str], method: str = "regex") -> dict:
    return {
        "doc_id": doc.doc_id,
        "tell_id": tell_id,
        "method": method,
        "matches": [{"quote": q, "line": 1} for q in quotes],
    }


def _planted(n: int, at_lines: list[int]) -> tuple[dict[int, str], list[str]]:
    """Distinctive line contents and the quotes a detector would have recorded."""
    contents = {line: f"marker number {line} sits here" for line in at_lines}
    quotes = [contents[line] for line in at_lines][:n]
    return contents, quotes


# --- locating a match --------------------------------------------------------


def test_a_quote_is_found_however_it_was_wrapped() -> None:
    text = "alpha beta\ngamma delta epsilon"
    assert analysis.locate(text, "beta gamma delta") == (6, 22)
    assert analysis.locate(text, "…beta   gamma delta…") == (6, 22)


def test_a_quote_whose_context_was_stripped_still_finds_its_middle() -> None:
    """Lexical quotes come from markdown-stripped prose; the ends can differ."""
    text = "Intro **bold** and then we utilize the thing to finish the sentence here."
    quote = "…Intro bold and then we utilize the thing to finish the sentence…"
    span = analysis.locate(text, quote)
    assert span is not None
    assert "utilize" in text[span[0] : span[1]]


def test_a_quote_that_is_not_in_the_document_is_not_invented() -> None:
    assert analysis.locate("alpha beta gamma", "nothing like this at all here") is None
    assert analysis.locate("alpha beta gamma", "") is None
    assert analysis.locate("alpha beta gamma", "…") is None


# --- distance and chance -----------------------------------------------------


def test_distance_is_zero_when_a_boundary_falls_inside_the_span() -> None:
    assert analysis.distance_to_boundary((100, 200), [150]) == 0
    assert analysis.distance_to_boundary((100, 200), [100]) == 0
    assert analysis.distance_to_boundary((100, 200), [200]) == 0


def test_distance_takes_the_nearer_end_and_the_nearer_boundary() -> None:
    assert analysis.distance_to_boundary((100, 200), [80]) == 20
    assert analysis.distance_to_boundary((100, 200), [260]) == 60
    assert analysis.distance_to_boundary((100, 200), [80, 260]) == 20


def test_an_unstitched_document_has_no_distance_rather_than_a_large_one() -> None:
    assert analysis.distance_to_boundary((100, 200), []) is None
    assert analysis.stitching_of(_doc("m/a", "m", boundary_line=None)) == "single"
    assert analysis.stitching_of(_doc("m/a", "m")) == "stitched"


def test_chance_is_the_share_of_positions_a_span_could_occupy_at_a_seam() -> None:
    # A zero-length span in a 1001-position document, one boundary in the
    # middle, 100-character window: 201 of 1001 positions are inside it.
    assert analysis.chance_share(1001, 0, [500], 100) == pytest.approx(201 / 1001)
    # A longer span has more ways to touch the window, so chance rises.
    assert analysis.chance_share(1001, 50, [500], 100) > analysis.chance_share(
        1001, 0, [500], 100
    )
    # Overlapping windows are unioned, not double-counted.
    assert analysis.chance_share(1001, 0, [500, 520], 100) < 2 * analysis.chance_share(
        1001, 0, [500], 100
    )


def test_chance_is_zero_without_boundaries_or_without_room() -> None:
    assert analysis.chance_share(1000, 0, [], 100) == 0.0
    assert analysis.chance_share(10, 50, [5], 100) == 0.0


# --- the report --------------------------------------------------------------


def test_a_tell_that_fires_only_at_the_seam_is_enriched_and_flagged() -> None:
    contents, quotes = _planted(12, [48, 49, 50, 51, 52] * 3)
    doc = _doc("m/a", "m", planted=contents)
    report = analysis.seam_report([doc], [_row(doc, "t.planted", quotes)])
    group = report.groups[0]
    assert group.located == 12
    assert group.unlocated == 0
    assert group.near_seam == 12
    assert group.share == 1.0
    assert 0.0 < group.expected_share < 0.2
    assert group.enrichment is not None and group.enrichment > analysis.ENRICHMENT_FLAG
    assert group.flagged
    assert report.flagged() == [group]


def test_a_tell_spread_through_the_document_lands_near_chance() -> None:
    lines = list(range(1, 100, 4))
    contents, quotes = _planted(len(lines), lines)
    doc = _doc("m/a", "m", planted=contents)
    report = analysis.seam_report([doc], [_row(doc, "t.spread", quotes)])
    group = report.groups[0]
    assert group.located == len(lines)
    assert group.enrichment == pytest.approx(1.0, abs=0.6)
    assert not group.flagged


def test_a_match_that_cannot_be_located_is_counted_not_guessed_at() -> None:
    contents, quotes = _planted(3, [49, 50, 51])
    doc = _doc("m/a", "m", planted=contents)
    row = _row(doc, "t.x", quotes + ["a quote from some other document entirely"])
    report = analysis.seam_report([doc], [row])
    group = report.groups[0]
    assert group.matches == 4
    assert group.located == 3
    assert group.unlocated == 1
    assert any("could not be located" in note for note in report.notes)


def test_matches_in_unstitched_documents_are_counted_but_not_scored() -> None:
    """A single-turn document has no seam, so it cannot dilute the share."""
    contents, quotes = _planted(1, [50])
    stitched = _doc("m/a", "m", planted=contents)
    single = _doc("m/b", "m", boundary_line=None, planted=contents)
    report = analysis.seam_report(
        [stitched, single],
        [_row(stitched, "t.x", quotes), _row(single, "t.x", quotes * 20)],
    )
    cells = {g.cohort: g for g in report.groups}
    assert cells["m stitched"].located == 1
    assert cells["m stitched"].share == 1.0
    assert cells["m single"].matches == 20
    assert cells["m single"].located == 0
    assert cells["m single"].share == 0.0


def test_the_cohorts_separate_the_models_and_the_stitching() -> None:
    contents, quotes = _planted(1, [50])
    docs = [
        _doc("opus/a", "opus", planted=contents),
        _doc("opus/b", "opus", boundary_line=None, planted=contents),
        _doc("sonnet/a", "sonnet", planted=contents),
    ]
    report = analysis.seam_report(docs, [_row(d, "t.x", quotes) for d in docs])
    assert sorted(g.cohort for g in report.groups) == [
        "opus single",
        "opus stitched",
        "sonnet stitched",
    ]


def test_a_thin_cell_is_not_flagged_on_a_handful_of_matches() -> None:
    contents, quotes = _planted(3, [49, 50, 51])
    doc = _doc("m/a", "m", planted=contents)
    report = analysis.seam_report([doc], [_row(doc, "t.thin", quotes)])
    group = report.groups[0]
    assert group.share == 1.0
    assert not group.flagged, "three matches is not evidence of a harness artifact"


def test_a_row_at_the_record_cap_is_reported_as_truncated() -> None:
    contents, quotes = _planted(1, [50])
    doc = _doc("m/a", "m", planted=contents)
    report = analysis.seam_report(
        [doc], [_row(doc, "t.many", quotes * 50)], max_matches=50
    )
    assert report.groups[0].truncated_rows == 1
    assert any("record cap" in note for note in report.notes)


def test_a_score_row_for_a_document_that_is_gone_is_named_not_silently_dropped() -> None:
    doc = _doc("m/a", "m")
    report = analysis.seam_report(
        [doc], [{"doc_id": "m/ghost", "tell_id": "t.x", "method": "regex", "matches": []}]
    )
    assert report.groups == []
    assert any("not in the corpus" in note for note in report.notes)


def test_the_report_serializes_and_tabulates() -> None:
    contents, quotes = _planted(12, [48, 49, 50, 51, 52] * 3)
    doc = _doc("m/a", "m", planted=contents)
    report = analysis.seam_report([doc], [_row(doc, "t.planted", quotes)])
    data = report.as_dict()
    assert data["window"] == 200
    assert data["groups"][0]["tell_id"] == "t.planted"
    assert data["flagged"][0]["share"] == 1.0
    assert "t.planted" in report.table()
    assert "FLAG" in report.table()
    assert "t.planted" not in report.table(min_located=99)
    assert json.loads(json.dumps(data))["window"] == 200


def test_cohort_rates_split_the_same_tell_by_stitching() -> None:
    """The companion measure: a whole-document effect never clusters at a join."""
    stitched = _doc("m/a", "m")
    single = _doc("m/b", "m", boundary_line=None)
    rows = [
        {"doc_id": "m/a", "tell_id": "t.x", "method": "regex", "matches": [], "rate_per_1k": 1.0},
        {"doc_id": "m/a", "tell_id": "t.x", "method": "regex", "matches": [], "rate_per_1k": 3.0},
        {"doc_id": "m/b", "tell_id": "t.x", "method": "regex", "matches": [], "rate_per_1k": 0.5},
    ]
    rates = {r.cohort: r for r in analysis.cohort_rates([stitched, single], rows)}
    assert rates["m stitched"].mean == pytest.approx(2.0)
    assert rates["m stitched"].docs == 2
    assert rates["m single"].mean == pytest.approx(0.5)


def test_cohort_rates_fall_back_to_raw_when_a_tell_has_no_rate() -> None:
    doc = _doc("m/a", "m")
    rows = [{"doc_id": "m/a", "tell_id": "t.p", "method": "judge", "matches": [], "raw": 1.0}]
    rates = analysis.cohort_rates([doc], rows)
    assert rates[0].mean == 1.0


def test_read_scores_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "scores.jsonl"
    path.write_text('{"a": 1}\n\n{"a": 2}\n', encoding="utf-8")
    assert analysis.read_scores(path) == [{"a": 1}, {"a": 2}]
