"""The atlas profile layer: what it measures, and what it must never touch.

The atlas (M9e) is an inventory of classical figures and metadiscourse markers
measured for frequency. It is not a set of tells: no atlas entry carries a ramp,
no atlas row gets a score, and no aggregate that produces a headline number may
see one. The exclusion tests here are written as equality against the same frame
with the atlas rows deleted, so they check the *outcome* rather than the filter
that is supposed to produce it.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from telltale import scoring
from telltale.corpus import Doc
from telltale.detectors import build
from telltale.registry import ATLAS_STATUS, Registry, Tell, guarded_search

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"
REGISTRY = Registry(REGISTRY_PATH)
ATLAS = REGISTRY.atlas_tells()


def make(text: str, model: str = "m1", fmt: str = "memo", index: int = 1) -> Doc:
    return Doc.from_text(f"{model}/{fmt}-{index:02d}", model, fmt, text)


def atlas_tell(tell_id: str = "atlas.fixture", **over) -> Tell:
    base = dict(
        id=tell_id,
        name=tell_id,
        category="lexical",
        scope="general",
        method="regex",
        unit="count",
        pattern=r"\bwidget\b",
        status=ATLAS_STATUS,
        weight=1.0,
    )
    base.update(over)
    return Tell(**base)


def row(**over) -> dict:
    base = {
        "doc_id": "m1/memo-01",
        "model": "m1",
        "format": "memo",
        "tell_id": "lex.fixture",
        "category": "lexical",
        "scope": "general",
        "status": "active",
        "weight": 1.0,
        "method": "regex",
        "unit": "count",
        "raw": 1.0,
        "rate_per_1k": 1.0,
    }
    base.update(over)
    return base


def mixed_frame() -> pd.DataFrame:
    """Two models, one real tell, one atlas entry.

    The atlas rates run *opposite* to the tell's — m1 is the quiet model on the
    tell and the loud one on the atlas entry. A leak into the rollup therefore
    changes the numbers rather than scaling them, which a proportional fixture
    would have hidden: each tell is normalized against its own pooled cap, so
    an atlas entry at ten times the rate but the same shape scores identically.
    """
    rows = []
    for model, rate, atlas_rate in (("m1", 1.0, 4.0), ("m2", 3.0, 1.0)):
        for index in range(4):
            rows.append(
                row(
                    doc_id=f"{model}/memo-{index:02d}",
                    model=model,
                    raw=rate,
                    rate_per_1k=rate,
                )
            )
            rows.append(
                row(
                    doc_id=f"{model}/memo-{index:02d}",
                    model=model,
                    tell_id="atlas.fixture",
                    status=ATLAS_STATUS,
                    raw=atlas_rate,
                    rate_per_1k=atlas_rate,
                )
            )
    return pd.DataFrame(rows)


TELLS = [
    Tell(
        id="lex.fixture",
        name="lex.fixture",
        category="lexical",
        scope="general",
        method="regex",
        unit="count",
        pattern=r"\bwidget\b",
        status="active",
    ),
    atlas_tell(),
]


# --- the registry contract ---------------------------------------------------


def test_the_registry_ships_an_atlas_layer() -> None:
    assert len(ATLAS) >= 60
    assert all(t.id.startswith("atlas.") for t in ATLAS)
    assert all(t.status == ATLAS_STATUS for t in ATLAS)
    assert all(t.scope == "general" for t in ATLAS)


def test_atlas_ids_are_unique_and_alphabetical() -> None:
    ids = [t.id for t in ATLAS]
    assert len(set(ids)) == len(ids)
    assert ids == sorted(ids), "the atlas block is kept alphabetical so it diffs by hand"


def test_no_atlas_entry_is_scored_by_a_judge() -> None:
    assert {t.method for t in ATLAS} == {"regex", "statistic"}


def test_no_atlas_entry_carries_a_ramp() -> None:
    for tell in ATLAS:
        assert tell.ramp is None, tell.id
        assert tell.direction is None, tell.id


def test_the_validator_rejects_a_ramp_on_an_atlas_entry(tmp_path: Path) -> None:
    import yaml

    entry = {
        "id": "atlas.fixture",
        "name": "fixture",
        "category": "statistical",
        "scope": "general",
        "detection": {
            "method": "statistic",
            "unit": "value",
            "stat": "em_dash_per_1k",
            "direction": "high_is_telling",
            "ramp": [1.5, 6.0],
        },
        "status": ATLAS_STATUS,
        "weight": 1.0,
    }
    path = tmp_path / "atlas.yaml"
    path.write_text(
        yaml.safe_dump({"registry_version": 1, "schema_version": 1, "tells": [entry]}),
        encoding="utf-8",
    )
    errors = Registry(path).validate()
    assert "atlas.fixture: atlas entries carry no ramp" in errors
    assert "atlas.fixture: atlas entries carry no direction" in errors


def test_a_value_tell_that_is_not_atlas_still_needs_its_ramp(tmp_path: Path) -> None:
    """The relaxation is scoped to the atlas and nothing else."""
    import yaml

    entry = {
        "id": "sta.fixture",
        "name": "fixture",
        "category": "statistical",
        "scope": "general",
        "detection": {"method": "statistic", "unit": "value", "stat": "em_dash_per_1k"},
        "status": "active",
        "weight": 1.0,
    }
    path = tmp_path / "tell.yaml"
    path.write_text(
        yaml.safe_dump({"registry_version": 1, "schema_version": 1, "tells": [entry]}),
        encoding="utf-8",
    )
    errors = Registry(path).validate()
    assert "sta.fixture: value unit requires ramp" in errors
    assert "sta.fixture: value unit requires direction" in errors


def test_atlas_entries_are_out_of_active_tells_unless_asked_for() -> None:
    assert not [t for t in REGISTRY.active_tells() if t.status == ATLAS_STATUS]
    assert not [
        t for t in REGISTRY.active_tells(include_candidates=True) if t.status == ATLAS_STATUS
    ]
    with_atlas = REGISTRY.active_tells(include_atlas=True)
    assert len([t for t in with_atlas if t.status == ATLAS_STATUS]) == len(ATLAS)


def test_include_atlas_and_include_candidates_are_independent() -> None:
    atlas_only = REGISTRY.active_tells(include_atlas=True)
    both = REGISTRY.active_tells(include_candidates=True, include_atlas=True)
    assert {t.status for t in atlas_only} <= {"active", ATLAS_STATUS}
    assert len(both) >= len(atlas_only)


def test_every_atlas_entry_builds_and_measures() -> None:
    """Mirrors the registry-wide detector sweep, which skips the atlas by status."""
    sample = make(
        "Let us look at the numbers. The plan is fast, cheap, and fair.\n\n"
        "Why does this matter? Because families notice first.\n"
    )
    for entry in ATLAS:
        detection = build(entry).detect(sample)
        assert detection.tell_id == entry.id
        assert isinstance(detection.raw, float)


def test_every_atlas_regex_matches_an_example_and_rejects_its_counters() -> None:
    for entry in ATLAS:
        if entry.method != "regex":
            continue
        assert entry.examples, entry.id
        assert any(guarded_search(entry, ex) for ex in entry.examples), entry.id
        for counter in entry.counter_examples:
            assert not guarded_search(entry, counter), f"{entry.id}: {counter}"


def test_ambiguity_prone_atlas_entries_carry_counter_examples() -> None:
    """Every regex entry whose pattern uses a guard has to show what it excludes."""
    for entry in ATLAS:
        if entry.method != "regex":
            continue
        guarded = "(?!" in (entry.pattern or "") or "(?<!" in (entry.pattern or "")
        if guarded or entry.proper_noun_guard:
            assert entry.counter_examples, entry.id


def test_the_deferred_list_names_the_figures_we_do_not_fake() -> None:
    raw = REGISTRY._raw.get("atlas_deferred")
    assert isinstance(raw, list) and len(raw) >= 20
    assert "metaphor" in raw and "polyptoton" in raw
    ids = {t.id for t in ATLAS}
    assert not (set(raw) & ids)


# --- scoring: measured, never scored -----------------------------------------


def test_an_atlas_row_scores_nan_rather_than_zero() -> None:
    scored = scoring.normalize(mixed_frame(), TELLS)
    atlas = scored[scored["tell_id"] == "atlas.fixture"]
    assert len(atlas) == 8
    assert atlas["score"].isna().all()
    assert not scored[scored["tell_id"] == "lex.fixture"]["score"].isna().any()


def test_an_atlas_tell_gets_no_winsor_cap() -> None:
    scored = scoring.normalize(mixed_frame(), TELLS)
    assert "atlas.fixture" not in scored.attrs["winsor_caps"]
    assert "lex.fixture" in scored.attrs["winsor_caps"]


def test_the_atlas_keeps_its_raw_measurement() -> None:
    """Frequency is the deliverable, so raw and rate survive even without a score."""
    scored = scoring.normalize(mixed_frame(), TELLS)
    atlas = scored[scored["tell_id"] == "atlas.fixture"]
    assert sorted(set(atlas["rate_per_1k"])) == [1.0, 4.0]


def test_an_atlas_statistic_scores_nan_without_needing_a_ramp() -> None:
    """Without the atlas branch this raises: a value unit has no score otherwise."""
    frame = pd.DataFrame(
        [
            row(
                tell_id="atlas.stat",
                status=ATLAS_STATUS,
                method="statistic",
                unit="value",
                raw=4.0,
                rate_per_1k=None,
            )
        ]
    )
    scored = scoring.normalize(frame, [atlas_tell("atlas.stat", method="statistic", unit="value", stat="em_dash_per_1k")])
    assert math.isnan(scored["score"].iloc[0])


def test_is_atlas_and_atlas_rows_read_the_status_column() -> None:
    frame = mixed_frame()
    assert not scoring.is_atlas(frame)
    assert scoring.is_atlas(frame[frame["tell_id"] == "atlas.fixture"])
    assert len(scoring.atlas_rows(frame)) == 8


# --- exclusion from every aggregate ------------------------------------------


def without_atlas(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"] != ATLAS_STATUS].reset_index(drop=True)


def test_the_category_rollup_is_identical_with_and_without_the_atlas() -> None:
    scored = scoring.normalize(mixed_frame(), TELLS)
    clean = scoring.normalize(without_atlas(mixed_frame()), TELLS)
    pd.testing.assert_frame_equal(
        scoring.category_rollup(scored, TELLS),
        scoring.category_rollup(clean, TELLS),
    )


def test_the_indices_are_identical_with_and_without_the_atlas() -> None:
    scored = scoring.normalize(mixed_frame(), TELLS)
    clean = scoring.normalize(without_atlas(mixed_frame()), TELLS)
    pd.testing.assert_frame_equal(
        scoring.indices(scored, TELLS),
        scoring.indices(clean, TELLS),
    )


def test_an_atlas_entry_cannot_reach_a_rollup_column() -> None:
    scored = scoring.normalize(mixed_frame(), TELLS)
    matrix = scoring.per_model_tell_matrix(scored)
    assert "atlas.fixture" in matrix.columns  # it is measured and reported
    assert matrix["atlas.fixture"].isna().all()  # and carries no score
    rollup = scoring.category_rollup(scored, TELLS)
    # The lexical rollup is the tell alone: m2 is at the pooled cap, so 1.0.
    # Folding the atlas entry in would pull m2 down (it is the quiet model
    # there), which is what the equality tests above would catch.
    assert rollup.loc["m2", "lexical"] == pytest.approx(1.0)


def test_an_atlas_entry_cannot_reach_a_signature_index() -> None:
    rows = [
        row(
            doc_id="m1/memo-01",
            tell_id="atlas.signature",
            status=ATLAS_STATUS,
            scope="model:m1",
            raw=5.0,
            rate_per_1k=5.0,
        )
    ]
    scored = scoring.normalize(
        pd.DataFrame(rows), [atlas_tell("atlas.signature", scope="model:m1")]
    )
    out = scoring.indices(scored, [atlas_tell("atlas.signature", scope="model:m1")])
    assert out.empty or bool(np.isnan(out["signature_index"].iloc[0]))


def test_the_manifest_records_whether_the_atlas_was_measured(tmp_path: Path) -> None:
    from telltale.manifest import build_manifest

    manifest = build_manifest(
        docs=[],
        registry=REGISTRY,
        scored_tells=[],
        corpus_root=tmp_path,
        judge_skipped=[],
        include_atlas=True,
    )
    assert manifest["registry"]["include_atlas"] is True
    assert manifest["registry"]["include_candidates"] is False
