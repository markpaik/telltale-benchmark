"""The scoring engine: normalization, rollups, indices, and uncertainty.

The arithmetic tests build the frame by hand rather than by running detectors,
so the expected number can be worked out on paper and the test fails for one
reason only. The plumbing tests go the long way round — real documents, real
registry entries — so the two halves cannot agree with each other while both
being wrong.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from telltale import scoring
from telltale.corpus import Doc
from telltale.registry import Registry, Tell

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"
REGISTRY = Registry(REGISTRY_PATH)


def make(text: str, model: str = "m1", fmt: str = "memo", index: int = 1) -> Doc:
    return Doc.from_text(f"{model}/{fmt}-{index:02d}", model, fmt, text)


def count_tell(tell_id: str = "lex.fixture", weight: float = 1.0, **over) -> Tell:
    base = dict(
        id=tell_id,
        name=tell_id,
        category="lexical",
        scope="general",
        method="regex",
        unit="count",
        pattern=r"\bwidget\b",
        status="active",
        weight=weight,
    )
    base.update(over)
    return Tell(**base)


def value_tell(tell_id: str = "sta.fixture", **over) -> Tell:
    base = dict(
        id=tell_id,
        name=tell_id,
        category="statistical",
        scope="general",
        method="statistic",
        unit="value",
        stat="em_dash_per_1k",
        direction="high_is_telling",
        ramp=(1.5, 6.0),
        status="active",
    )
    base.update(over)
    return Tell(**base)


def frame(rows: list[dict]) -> pd.DataFrame:
    """A minimal detection frame: only the columns normalization reads."""
    defaults = {
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
        "raw": 0.0,
        "rate_per_1k": 0.0,
    }
    return pd.DataFrame([{**defaults, **row} for row in rows])


# --- winsorization -----------------------------------------------------------

# Twenty-one documents. Rates run 0, 0, 0, 1, 1, 1, ... 6, 6 and then one
# runaway at 100. numpy's linear percentile puts the 95th at sorted position
# 0.95 * (21 - 1) = 19, which is the second 6 — so the cap is 6.0 while the max
# is 100.0, and the two have to be told apart for this test to mean anything.
WINSOR_RATES = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 100]


def winsor_frame() -> pd.DataFrame:
    return frame(
        [
            {
                "doc_id": f"m1/memo-{i:02d}",
                "raw": float(rate),
                "rate_per_1k": float(rate),
            }
            for i, rate in enumerate(WINSOR_RATES)
        ]
    )


def test_winsor_cap_is_the_pooled_p95_not_the_max() -> None:
    rates = np.array(WINSOR_RATES, dtype=float)
    assert scoring.winsorized_cap(rates) == 6.0
    assert rates.max() == 100.0


def test_count_scores_divide_by_the_winsorized_cap() -> None:
    scored = scoring.normalize(winsor_frame(), [count_tell()])
    by_rate = dict(zip(scored["rate_per_1k"], scored["score"]))
    assert by_rate[0.0] == 0.0
    assert by_rate[3.0] == pytest.approx(3.0 / 6.0)  # 0.5
    assert by_rate[6.0] == pytest.approx(1.0)
    # The runaway is clipped to the cap, not allowed to define the scale.
    assert by_rate[100.0] == pytest.approx(1.0)


def test_winsorization_pools_across_models() -> None:
    """One model's ceiling must not be rescaled onto its own worst document."""
    rows = [
        {"doc_id": f"loud/memo-{i:02d}", "model": "loud", "raw": 10.0, "rate_per_1k": 10.0}
        for i in range(10)
    ] + [
        {"doc_id": f"quiet/memo-{i:02d}", "model": "quiet", "raw": 1.0, "rate_per_1k": 1.0}
        for i in range(10)
    ]
    scored = scoring.normalize(frame(rows), [count_tell()])
    matrix = scoring.per_model_tell_matrix(scored)
    # Pooled p95 of ten 1s and ten 10s is 10.0, so the quiet model sits at 0.1 —
    # per-model normalization would have put both at 1.0.
    assert matrix.loc["loud", "lex.fixture"] == pytest.approx(1.0)
    assert matrix.loc["quiet", "lex.fixture"] == pytest.approx(0.1)


def test_a_sparse_tell_falls_back_to_the_max_rather_than_vanishing() -> None:
    """With 95% zeros the percentile is zero; clipping to it would erase the tell."""
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "raw": 0.0, "rate_per_1k": 0.0} for i in range(39)
    ] + [{"doc_id": "m1/memo-99", "raw": 4.0, "rate_per_1k": 8.0}]
    scored = scoring.normalize(frame(rows), [count_tell()])
    hit = scored[scored["doc_id"] == "m1/memo-99"]["score"].iloc[0]
    assert hit == pytest.approx(1.0)
    assert scored[scored["doc_id"] != "m1/memo-99"]["score"].max() == 0.0
    assert "lex.fixture" not in scoring.dormant_tells(scored)


def test_a_count_row_with_no_rate_scores_nan() -> None:
    scored = scoring.normalize(
        frame(
            [
                {"doc_id": "m1/memo-01", "raw": 1.0, "rate_per_1k": 5.0},
                {"doc_id": "m1/memo-02", "raw": 0.0, "rate_per_1k": None},
            ]
        ),
        [count_tell()],
    )
    assert math.isnan(scored[scored["doc_id"] == "m1/memo-02"]["score"].iloc[0])


# --- ramps -------------------------------------------------------------------


def test_high_is_telling_ramp() -> None:
    ramp = (1.5, 6.0)  # span 4.5
    assert scoring.ramp_score(1.5, "high_is_telling", ramp) == 0.0
    assert scoring.ramp_score(6.0, "high_is_telling", ramp) == 1.0
    assert scoring.ramp_score(3.75, "high_is_telling", ramp) == pytest.approx(0.5)
    assert scoring.ramp_score(0.0, "high_is_telling", ramp) == 0.0  # clipped
    assert scoring.ramp_score(99.0, "high_is_telling", ramp) == 1.0  # clipped


def test_low_is_telling_ramp_runs_downhill() -> None:
    ramp = (0.75, 0.40)  # span 0.35, telling as the value falls
    assert scoring.ramp_score(0.75, "low_is_telling", ramp) == 0.0
    assert scoring.ramp_score(0.40, "low_is_telling", ramp) == 1.0
    assert scoring.ramp_score(0.575, "low_is_telling", ramp) == pytest.approx(0.5)
    assert scoring.ramp_score(0.20, "low_is_telling", ramp) == 1.0  # clipped
    assert scoring.ramp_score(1.20, "low_is_telling", ramp) == 0.0  # clipped


def test_ramp_written_against_its_direction_is_rejected() -> None:
    """A ramp entered backwards would silently invert a tell."""
    with pytest.raises(ValueError):
        scoring.ramp_score(1.0, "high_is_telling", (6.0, 1.5))
    with pytest.raises(ValueError):
        scoring.ramp_score(1.0, "low_is_telling", (0.40, 0.75))


def test_degenerate_ramp_is_a_step_not_a_division_by_zero() -> None:
    assert scoring.ramp_score(5.0, "high_is_telling", (5.0, 5.0)) == 1.0
    assert scoring.ramp_score(4.9, "high_is_telling", (5.0, 5.0)) == 0.0
    assert scoring.ramp_score(5.0, "low_is_telling", (5.0, 5.0)) == 1.0
    assert scoring.ramp_score(5.1, "low_is_telling", (5.0, 5.0)) == 0.0


def test_nan_stays_nan_and_is_excluded_from_the_mean() -> None:
    rows = [
        {"doc_id": "m1/memo-01", "unit": "value", "raw": 6.0, "rate_per_1k": None},
        {"doc_id": "m1/memo-02", "unit": "value", "raw": 1.5, "rate_per_1k": None},
        {"doc_id": "m1/memo-03", "unit": "value", "raw": float("nan"), "rate_per_1k": None},
    ]
    rows = [{**r, "tell_id": "sta.fixture", "category": "statistical"} for r in rows]
    scored = scoring.normalize(frame(rows), [value_tell()])
    assert math.isnan(scored[scored["doc_id"] == "m1/memo-03"]["score"].iloc[0])
    matrix = scoring.per_model_tell_matrix(scored)
    # Mean of 1.0 and 0.0 over two documents, not of 1.0, 0.0 and a phantom zero.
    assert matrix.loc["m1", "sta.fixture"] == pytest.approx(0.5)


def test_all_ramps_in_the_shipped_registry_agree_with_their_direction() -> None:
    for tell in REGISTRY.active_tells(include_candidates=True):
        if tell.unit != "value":
            continue
        scoring.ramp_score(float(tell.ramp[0]), tell.direction, tell.ramp)


def test_value_tells_need_their_ramp() -> None:
    rows = [{"unit": "value", "tell_id": "sta.fixture", "raw": 1.0, "rate_per_1k": None}]
    with pytest.raises(ValueError, match="ramp"):
        scoring.normalize(frame(rows), [])


# --- binary ------------------------------------------------------------------


def test_binary_score_is_the_flag_itself() -> None:
    rows = [
        {"doc_id": "m1/memo-01", "unit": "binary", "raw": 1.0, "rate_per_1k": None},
        {"doc_id": "m1/memo-02", "unit": "binary", "raw": 0.0, "rate_per_1k": None},
    ]
    scored = scoring.normalize(frame(rows), [count_tell(unit="binary")])
    assert sorted(scored["score"].tolist()) == [0.0, 1.0]


# --- dormancy ----------------------------------------------------------------


def test_a_tell_that_never_fires_is_dormant_and_scores_zero() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "raw": 0.0, "rate_per_1k": 0.0} for i in range(5)
    ]
    scored = scoring.normalize(frame(rows), [count_tell()])
    assert scoring.dormant_tells(scored) == ["lex.fixture"]
    assert (scored["score"] == 0.0).all()


def test_dormancy_survives_a_round_trip_through_raw_values() -> None:
    """The scorecard recovers dormancy from scores.jsonl, which has no flag column."""
    rows = [{"doc_id": f"m1/memo-{i:02d}", "raw": 0.0, "rate_per_1k": 0.0} for i in range(5)]
    reloaded = scoring.mark_dormant(frame(rows))
    assert scoring.dormant_tells(reloaded) == ["lex.fixture"]


def test_a_value_tell_is_dormant_only_when_it_is_nan_everywhere() -> None:
    nan_rows = [
        {"doc_id": f"m1/memo-{i:02d}", "unit": "value", "tell_id": "sta.fixture",
         "raw": float("nan"), "rate_per_1k": None}
        for i in range(3)
    ]
    assert scoring.dormant_tells(scoring.mark_dormant(frame(nan_rows))) == ["sta.fixture"]

    # A value tell that computes to 0.0 everywhere is measured, not dormant.
    zero_rows = [{**row, "raw": 0.0} for row in nan_rows]
    assert scoring.dormant_tells(scoring.mark_dormant(frame(zero_rows))) == []


# --- format scoping ----------------------------------------------------------


def test_format_scoped_tells_produce_no_rows_outside_their_formats() -> None:
    courtesy = REGISTRY.get("crt.hope-finds-you-well")
    assert courtesy.formats == ("email", "memo", "meeting-minutes")
    docs = [
        make("I hope this email finds you well.", fmt="email"),
        make("Quarterly revenue rose.", fmt="business-report"),
    ]
    df = scoring.detect_all(docs, [courtesy])
    assert set(df["doc_id"]) == {"m1/email-01"}
    assert "m1/business-report-01" not in set(df["doc_id"])


def test_an_out_of_scope_format_is_not_a_zero() -> None:
    """A sign-off tell scored zero on a white paper would libel the white paper."""
    courtesy = REGISTRY.get("crt.warm-signoff")
    docs = [
        make("Warm regards,\nThe team", model="polite", fmt="email"),
        make("Section one.", model="polite", fmt="white-paper", index=2),
    ]
    scored = scoring.normalize(scoring.detect_all(docs, [courtesy]), [courtesy])
    matrix = scoring.per_model_tell_matrix(scored)
    # One applicable document, and it fired: the mean is 1.0, not 0.5.
    assert matrix.loc["polite", "crt.warm-signoff"] == pytest.approx(1.0)


# --- rollups and indices -----------------------------------------------------


def rollup_frame() -> tuple[pd.DataFrame, list[Tell]]:
    """Two lexical tells (weights 1 and 3) and one structural tell.

    S(m1, lex.a) = 0.2, S(m1, lex.b) = 0.6, S(m1, str.c) = 0.25.
    """
    tells = [
        count_tell("lex.a", weight=1.0),
        count_tell("lex.b", weight=3.0),
        count_tell("str.c", weight=1.0, category="structural"),
    ]
    rows = []
    for tell_id, score in (("lex.a", 0.2), ("lex.b", 0.6), ("str.c", 0.25)):
        rows.append(
            {
                "tell_id": tell_id,
                "category": "structural" if tell_id.startswith("str") else "lexical",
                "weight": 3.0 if tell_id == "lex.b" else 1.0,
                "raw": 1.0,
                "rate_per_1k": 1.0,
                "score": score,
            }
        )
    df = frame(rows)
    df["score"] = [0.2, 0.6, 0.25]
    return scoring.mark_dormant(df), tells


def test_category_rollup_is_a_weighted_mean_of_tells() -> None:
    df, tells = rollup_frame()
    rollup = scoring.category_rollup(df, tells)
    # (1 * 0.2 + 3 * 0.6) / (1 + 3) = 2.0 / 4 = 0.5
    assert rollup.loc["m1", "lexical"] == pytest.approx(0.5)
    assert rollup.loc["m1", "structural"] == pytest.approx(0.25)
    # Nothing was measured in the other three categories.
    assert math.isnan(rollup.loc["m1", "syntactic"])


def test_index_renormalizes_over_the_categories_that_exist() -> None:
    df, tells = rollup_frame()
    index = scoring.indices(df, tells)
    # (0.30 * 0.5 + 0.20 * 0.25) / (0.30 + 0.20) = 0.20 / 0.50 = 0.4 -> 40.0
    assert index.loc["m1", "ai_tell_index"] == pytest.approx(40.0)
    assert math.isnan(index.loc["m1", "signature_index"])


def test_model_scoped_tells_stay_out_of_the_general_rollup() -> None:
    tells = [
        count_tell("lex.a", weight=1.0),
        count_tell("lex.b", weight=1.0, scope="model:m1"),
    ]
    df = frame(
        [
            {"tell_id": "lex.a", "scope": "general", "raw": 1.0, "rate_per_1k": 1.0},
            {"tell_id": "lex.b", "scope": "model:m1", "raw": 1.0, "rate_per_1k": 1.0},
        ]
    )
    df["score"] = [0.2, 0.9]
    df = scoring.mark_dormant(df)
    rollup = scoring.category_rollup(df, tells)
    # Only lex.a counts: a tell discovered on m1 cannot then be evidence against m1.
    assert rollup.loc["m1", "lexical"] == pytest.approx(0.2)
    index = scoring.indices(df, tells)
    assert index.loc["m1", "ai_tell_index"] == pytest.approx(20.0)
    assert index.loc["m1", "signature_index"] == pytest.approx(90.0)


def test_candidate_tells_are_reported_but_not_indexed() -> None:
    tells = [count_tell("lex.a"), count_tell("lex.b", status="candidate")]
    df = frame(
        [
            {"tell_id": "lex.a", "status": "active", "raw": 1.0, "rate_per_1k": 1.0},
            {"tell_id": "lex.b", "status": "candidate", "raw": 1.0, "rate_per_1k": 1.0},
        ]
    )
    df["score"] = [0.2, 1.0]
    df = scoring.mark_dormant(df)
    assert scoring.category_rollup(df, tells).loc["m1", "lexical"] == pytest.approx(0.2)


def test_dormant_tells_stay_in_the_denominator_by_default() -> None:
    tells = [count_tell("lex.a"), count_tell("lex.b")]
    df = frame(
        [
            {"tell_id": "lex.a", "raw": 1.0, "rate_per_1k": 4.0},
            {"tell_id": "lex.b", "raw": 0.0, "rate_per_1k": 0.0},
        ]
    )
    scored = scoring.normalize(df, tells)
    assert scoring.dormant_tells(scored) == ["lex.b"]
    # Two tells, one at 1.0 and one dormant at 0.0: the mean is 0.5.
    assert scoring.category_rollup(scored, tells).loc["m1", "lexical"] == pytest.approx(0.5)
    # Dropping them is available, and moves the number.
    assert scoring.category_rollup(scored, tells, include_dormant=False).loc[
        "m1", "lexical"
    ] == pytest.approx(1.0)


def test_matrices_have_sorted_axes() -> None:
    df = frame(
        [
            {"doc_id": "z/memo-01", "model": "z", "tell_id": "lex.b", "raw": 1.0, "rate_per_1k": 2.0},
            {"doc_id": "a/memo-01", "model": "a", "tell_id": "lex.a", "raw": 1.0, "rate_per_1k": 2.0},
        ]
    )
    scored = scoring.normalize(df, [count_tell("lex.a"), count_tell("lex.b")])
    matrix = scoring.per_model_tell_matrix(scored)
    assert list(matrix.index) == ["a", "z"]
    assert list(matrix.columns) == ["lex.a", "lex.b"]
    by_format = scoring.per_model_format_tell(scored)
    assert list(by_format.index) == [("a", "memo"), ("z", "memo")]


# --- Wilson ------------------------------------------------------------------


def test_wilson_interval_for_seven_of_eight() -> None:
    """Published Wilson 95% interval for 7/8 is [0.5291, 0.9776]."""
    lo, hi = scoring.wilson_ci(7, 8)
    assert lo == pytest.approx(0.5291, abs=5e-5)
    assert hi == pytest.approx(0.9776, abs=5e-5)


def test_wilson_never_claims_certainty_from_a_clean_sweep() -> None:
    lo, hi = scoring.wilson_ci(8, 8)
    assert hi == pytest.approx(1.0)
    assert 0.6 < lo < 0.7  # Wald would say 1.0; eight documents cannot show that
    lo, hi = scoring.wilson_ci(0, 8)
    assert lo == 0.0
    assert 0.3 < hi < 0.4


def test_wilson_on_an_empty_sample_is_nan() -> None:
    lo, hi = scoring.wilson_ci(0, 0)
    assert math.isnan(lo) and math.isnan(hi)


def test_binary_tell_rates_report_hits_and_an_interval() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "unit": "binary", "raw": 1.0 if i < 7 else 0.0,
         "rate_per_1k": None}
        for i in range(8)
    ]
    scored = scoring.normalize(frame(rows), [count_tell(unit="binary")])
    rates = scoring.binary_tell_rates(scored)
    row = rates.iloc[0]
    assert row["n_docs"] == 8 and row["n_hits"] == 7
    assert row["rate"] == pytest.approx(0.875)
    assert row["ci_lo"] == pytest.approx(0.5291, abs=5e-5)


# --- minimum evidence --------------------------------------------------------


def test_thin_cells_are_flagged_on_document_count() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "raw": 5.0, "rate_per_1k": 5.0} for i in range(3)
    ]
    flags = scoring.min_evidence_flags(frame(rows))
    assert flags.iloc[0]["flagged"]
    assert "n_docs=3<8" in flags.iloc[0]["reason"]


def test_thin_cells_are_flagged_on_occurrences_even_with_enough_documents() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "raw": 1.0 if i < 4 else 0.0, "rate_per_1k": 1.0}
        for i in range(10)
    ]
    flags = scoring.min_evidence_flags(frame(rows))
    assert flags.iloc[0]["flagged"]
    assert "occurrences=4<10" in flags.iloc[0]["reason"]


def test_a_well_evidenced_cell_is_not_flagged() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "raw": 2.0, "rate_per_1k": 2.0} for i in range(10)
    ]
    flags = scoring.min_evidence_flags(frame(rows))
    assert not flags.iloc[0]["flagged"]
    assert flags.iloc[0]["reason"] == ""


def test_binary_cells_are_only_held_to_the_document_floor() -> None:
    rows = [
        {"doc_id": f"m1/memo-{i:02d}", "unit": "binary", "raw": 1.0 if i < 2 else 0.0,
         "rate_per_1k": None}
        for i in range(10)
    ]
    flags = scoring.min_evidence_flags(frame(rows))
    assert not flags.iloc[0]["flagged"]  # 2 occurrences, but the floor is for counts


# --- bootstrap ---------------------------------------------------------------


def paired_frame() -> tuple[pd.DataFrame, list[Tell]]:
    """Two models over the same eight prompts, one noticeably louder."""
    tells = [count_tell("lex.a"), count_tell("lex.b")]
    rows = []
    for i in range(8):
        for model, base in (("loud", 6.0), ("quiet", 1.0)):
            for tell_id in ("lex.a", "lex.b"):
                rate = base + (i % 3)
                rows.append(
                    {
                        "doc_id": f"{model}/memo-{i:02d}",
                        "model": model,
                        "tell_id": tell_id,
                        "raw": rate,
                        "rate_per_1k": rate,
                    }
                )
    return scoring.normalize(frame(rows), tells), tells


def as_text(result: dict) -> str:
    """Serialize a bootstrap result so NaN compares equal to NaN."""
    import json

    return json.dumps(result, sort_keys=True, default=str)


def test_bootstrap_is_deterministic_under_a_fixed_seed() -> None:
    df, tells = paired_frame()
    first = scoring.bootstrap_ci(df, tells, n=200, seed=7)
    second = scoring.bootstrap_ci(df, tells, n=200, seed=7)
    assert as_text(first) == as_text(second)


def test_a_different_seed_moves_the_interval() -> None:
    df, tells = paired_frame()
    first = scoring.bootstrap_ci(df, tells, n=200, seed=7)
    other = scoring.bootstrap_ci(df, tells, n=200, seed=8)
    assert as_text(first) != as_text(other)
    # The point estimate is data, not a draw: it must not move.
    assert first["models"]["loud"]["index"]["point"] == other["models"]["loud"]["index"]["point"]


def test_bootstrap_pairs_by_prompt_when_the_corpora_are_balanced() -> None:
    df, tells = paired_frame()
    result = scoring.bootstrap_ci(df, tells, n=200, seed=7)
    assert result["method"] == "paired"
    assert result["n_prompts"] == 8
    assert scoring.pairing_summary(df)["method"] == "paired"


def test_bootstrap_falls_back_to_unpaired_on_an_unbalanced_corpus() -> None:
    df, tells = paired_frame()
    df = df[df["doc_id"] != "quiet/memo-07"]
    result = scoring.bootstrap_ci(df, tells, n=100, seed=7)
    assert result["method"] == "unpaired"
    assert result["n_prompts"] is None


def test_the_interval_brackets_the_point_estimate_on_a_balanced_corpus() -> None:
    """Not a universal law — a percentile interval on a tiny, skewed corpus can
    sit to one side of the point — but it must hold where the data is well
    behaved, which is the case this fixture builds."""
    df, tells = paired_frame()
    result = scoring.bootstrap_ci(df, tells, n=500, seed=7)
    for model in ("loud", "quiet"):
        entry = result["models"][model]["index"]
        assert entry["lo"] <= entry["point"] <= entry["hi"]


def test_a_real_gap_is_reported_as_separated() -> None:
    df, tells = paired_frame()
    result = scoring.bootstrap_ci(df, tells, n=500, seed=7)
    delta = result["deltas"]["loud|quiet"]
    assert delta["point"] > 0
    assert delta["significant"] is True


def test_two_identical_models_are_not_separated() -> None:
    tells = [count_tell("lex.a")]
    rows = []
    for i in range(8):
        for model in ("left", "right"):
            rate = 2.0 + (i % 4)
            rows.append(
                {
                    "doc_id": f"{model}/memo-{i:02d}",
                    "model": model,
                    "tell_id": "lex.a",
                    "raw": rate,
                    "rate_per_1k": rate,
                }
            )
    df = scoring.normalize(frame(rows), tells)
    result = scoring.bootstrap_ci(df, tells, n=500, seed=7)
    delta = result["deltas"]["left|right"]
    assert delta["point"] == pytest.approx(0.0)
    assert delta["significant"] is False


def test_bootstrap_on_an_empty_frame_is_inert() -> None:
    result = scoring.bootstrap_ci(pd.DataFrame(), [], n=10, seed=7)
    assert result["models"] == {}
    assert result["method"] == "none"


# --- detect_all plumbing -----------------------------------------------------


def test_detect_all_skips_judge_tells_and_counts_them() -> None:
    tells = REGISTRY.active_tells()
    df = scoring.detect_all([make("A short memo about widgets.")], tells)
    assert df.attrs["judge_tells_skipped"] == len([t for t in tells if t.method == "judge"])
    assert "judge" not in set(df["method"])
    assert scoring.judge_tell_ids(tells) == sorted(df.attrs["judge_tell_ids"])


def test_detect_all_is_ordered_for_determinism() -> None:
    docs = [
        make("widget", model="z", index=2),
        make("widget", model="a", index=1),
    ]
    tells = [count_tell("lex.b"), count_tell("lex.a")]
    df = scoring.detect_all(docs, tells)
    assert list(df["doc_id"]) == ["a/memo-01", "a/memo-01", "z/memo-02", "z/memo-02"]
    assert list(df["tell_id"]) == ["lex.a", "lex.b", "lex.a", "lex.b"]


def test_detect_all_on_an_empty_corpus_returns_an_empty_frame() -> None:
    df = scoring.detect_all([], REGISTRY.active_tells())
    assert df.empty
    assert list(df.columns) == list(scoring.DETECTION_COLUMNS)
    scored = scoring.normalize(df, REGISTRY.active_tells())
    assert scored.empty
    assert scoring.dormant_tells(scored) == []


def test_the_whole_registry_runs_over_a_real_document() -> None:
    tells = REGISTRY.active_tells()
    docs = [
        make(
            "# Report\n\nIt is worth noting that we must delve into the data. "
            "Moreover, the results are robust.\n\n"
            "- **Alpha**: one\n- **Beta**: two\n- **Gamma**: three\n\n"
            "## Conclusion\n\nThus, we conclude.\n",
            model="loud",
        ),
        make("The team met Tuesday. We looked at the numbers.\n", model="quiet"),
    ]
    scored = scoring.normalize(scoring.detect_all(docs, tells), tells)
    index = scoring.indices(scored, tells)
    assert index.loc["loud", "ai_tell_index"] > index.loc["quiet", "ai_tell_index"]
    fired = scored[(scored["model"] == "loud") & (scored["raw"] > 0)]["tell_id"]
    assert {"lex.delve", "lex.robust", "phr.worth-noting"} <= set(fired)


# --- the exploratory annex ---------------------------------------------------


def annex_frame():
    """One evidence document and one annex document, with opposite scores."""
    tells = [count_tell("lex.a", weight=1.0)]
    df = frame(
        [
            {
                "doc_id": "m1/memo-01",
                "format": "memo",
                "tell_id": "lex.a",
                "raw": 1.0,
                "rate_per_1k": 1.0,
            },
            {
                "doc_id": "m1/free-writing-01",
                "format": "free-writing",
                "tell_id": "lex.a",
                "raw": 1.0,
                "rate_per_1k": 1.0,
            },
        ]
    )
    df["score"] = [0.2, 1.0]
    return scoring.mark_dormant(df), tells


def test_the_annex_is_kept_out_of_the_rollup_and_the_index() -> None:
    df, tells = annex_frame()
    # Only the memo counts: 0.2, not the 0.6 mean of both documents.
    assert scoring.category_rollup(df, tells).loc["m1", "lexical"] == pytest.approx(0.2)
    assert scoring.indices(df, tells).loc["m1", "ai_tell_index"] == pytest.approx(20.0)


def test_the_annex_gets_no_index_row_of_its_own() -> None:
    df, tells = annex_frame()
    by_format = scoring.indices(df, tells, by=("model", "format"))
    assert ("m1", "memo") in by_format.index
    assert ("m1", "free-writing") not in by_format.index


def test_the_annex_does_not_move_the_bootstrap_interval() -> None:
    df, tells = annex_frame()
    boot = scoring.bootstrap_ci(df, tells, n=50, seed=7)
    interval = boot["models"]["m1"]["index"]
    # One evidence document scoring 0.2: every resample is that same document.
    assert interval["lo"] == pytest.approx(20.0)
    assert interval["hi"] == pytest.approx(20.0)


def test_the_annex_is_out_of_the_per_model_matrix_but_in_the_by_format_one() -> None:
    df, tells = annex_frame()
    per_model = scoring.per_model_tell_matrix(df)
    assert per_model.loc["m1", "lex.a"] == pytest.approx(0.2)

    by_format = scoring.per_model_format_tell(df)
    assert by_format.loc[("m1", "free-writing"), "lex.a"] == pytest.approx(1.0)
    assert by_format.loc[("m1", "memo"), "lex.a"] == pytest.approx(0.2)


def test_comparable_is_idempotent_and_safe_on_an_empty_frame() -> None:
    df, _ = annex_frame()
    once = scoring.comparable(df)
    assert list(scoring.comparable(once)["doc_id"]) == list(once["doc_id"])
    assert scoring.comparable(pd.DataFrame()).empty


def test_the_winsor_cap_is_computed_without_the_annex() -> None:
    """A runaway annex document must not rescale everyone else's score."""
    tells = [count_tell()]
    rows = [
        {
            "doc_id": f"m1/memo-{i:02d}",
            "format": "memo",
            "raw": 1.0,
            "rate_per_1k": float(rate),
        }
        for i, rate in enumerate(WINSOR_RATES[:-1], start=1)
    ]
    evidence_only = scoring.normalize(frame(rows), tells)
    with_annex = scoring.normalize(
        frame(
            rows
            + [
                {
                    "doc_id": "m1/free-writing-01",
                    "format": "free-writing",
                    "raw": 1.0,
                    "rate_per_1k": 100.0,
                }
            ]
        ),
        tells,
    )
    assert with_annex.attrs["winsor_caps"]["lex.fixture"] == pytest.approx(
        evidence_only.attrs["winsor_caps"]["lex.fixture"]
    )
    # And the annex document is still scored, on that same scale, clipped at 1.
    annex_row = with_annex[with_annex["format"] == "free-writing"]
    assert float(annex_row["score"].iloc[0]) == pytest.approx(1.0)
