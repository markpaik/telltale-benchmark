"""Tests for M7 discovery: the sweep, the lenses, the five gates, and dedup.

No test here calls a model. The sweep is arithmetic and is checked against
numbers computed by hand in the test itself rather than against a golden file —
a golden file records what the code did, which is not the same as recording what
is correct. The lens tests use canned judge answers, so what is under test is
the prompt built and the contract enforced, not the model's taste.
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from typing import Any

import pytest

from telltale.corpus import Doc
from telltale.discovery import auditor, dedup, pipeline, sweep, verify
from telltale.judge import cache as cache_mod
from telltale.registry import Registry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry" / "tells.yaml"


# --- a synthetic corpus with planted habits ----------------------------------

MODELS = ("model-a", "model-b", "model-c")
FORMATS = ("email", "memo", "business-report", "case-study", "postmortem")

#: Neutral filler, long enough that a planted phrase is a small share of the
#: document. That matters: gate 1 rejects a pattern matching 5% of tokens, and a
#: sixty-word test document makes every planted phrase look degenerate.
FILLER = (
    "The team reviewed the quarterly plan and agreed on a revised schedule.",
    "Each working group reported progress against its own milestones.",
    "Two sites asked for more time to finish their intake process.",
    "The budget line for materials was left unchanged for now.",
    "Staffing at the two smaller sites remains the open question.",
    "The vendor sent a revised quote that lands inside the approved range.",
    "Attendance data for the spring term arrives at the end of the month.",
    "Nobody objected to moving the standing meeting to Thursday mornings.",
    "The facilities request is still sitting with the district office.",
    "Training dates were set for the first week after the break.",
    "One site reported a shortfall in supplies that was covered locally.",
    "The reporting template was simplified after feedback from three leads.",
    "A short pilot ran at one site and the results were mixed.",
    "The next status update goes out on the first Monday of the month.",
)
BASE = "\n\n".join(" ".join(FILLER[i : i + 5]) for i in (0, 5, 9))

#: In the first 14 documents of every model. Uniform across models, so it lands
#: as `general` — and it is `lex.delve`, so a candidate proposing it again is
#: the duplicate case.
UNIFORM = "The next review will delve into the intake numbers by site."

#: In the last 14 documents of every model. Also uniform, but on a *different*
#: subset, so it is `general` without being behaviourally identical to `delve`.
UNIFORM_LATE = "The intake window closes on Friday for every site."

#: Twice in every model-a document and nowhere else, so it lands as
#: `model:model-a`. Twice because a phrase occurring ten times in a 1,800-token
#: corpus does not clear a z of 3.09 — which is the estimator being honest about
#: a small sample, not a bug to tune away.
CONCENTRATED = "It bears emphasis that the schedule has not moved."

DOCS_PER_MODEL = 20


def make_doc(model: str, fmt: str, index: int) -> Doc:
    lines = [f"# {fmt.replace('-', ' ').title()} {index + 1:02d}", "", BASE]
    if index < 14:
        lines += ["", UNIFORM]
    if index >= 6:
        lines += ["", UNIFORM_LATE]
    if model == "model-a":
        lines += ["", CONCENTRATED, "", CONCENTRATED]
    return Doc.from_text(
        doc_id=f"{model}/{fmt}-{index + 1:02d}",
        model=model,
        fmt=fmt,
        text="\n".join(lines),
    )


@pytest.fixture(scope="module")
def corpus() -> list[Doc]:
    docs: list[Doc] = []
    for model in MODELS:
        for i in range(DOCS_PER_MODEL):
            docs.append(make_doc(model, FORMATS[i % len(FORMATS)], i))
    return sorted(docs, key=lambda d: d.doc_id)


@pytest.fixture
def registry(tmp_path: Path) -> Registry:
    """A throwaway copy of the real registry, so appends cannot touch the repo."""
    path = tmp_path / "tells.yaml"
    shutil.copy(REGISTRY_PATH, path)
    return Registry(path)


# --- fakes -------------------------------------------------------------------


class FakeClient:
    """A `JudgeClient` stand-in: same `ask` contract, answers from a router."""

    def __init__(self, router: Any, model: str = "claude-opus-4-6") -> None:
        self.router = router
        self.model = model
        self.calls: list[dict[str, Any]] = []

    def ask(
        self,
        stage: str,
        chunk_sha: str,
        tell_id: str,
        rubric_version: Any,
        prompt: str,
        quote: str | None = None,
    ) -> tuple[dict[str, Any], str, bool]:
        self.calls.append(
            {
                "stage": stage,
                "tell_id": tell_id,
                "rubric_version": rubric_version,
                "prompt": prompt,
                "quote": quote,
            }
        )
        answer = self.router(stage, tell_id, prompt, len(self.calls) - 1)
        if answer is None:
            raise AssertionError(f"fake client has no answer for {stage}/{tell_id}")
        return answer, f"key-{len(self.calls)}", False


def always_true_adjudicator(stage: str, tell_id: str, prompt: str, index: int):
    if stage == cache_mod.ADJUDICATE:
        return {
            "instance": True,
            "criteria_met": ["a"],
            "exclusion_triggered": None,
            "rationale": "a true instance of the described pattern",
        }
    return None


def always_false_adjudicator(stage: str, tell_id: str, prompt: str, index: int):
    if stage == cache_mod.ADJUDICATE:
        return {
            "instance": False,
            "criteria_met": [],
            "exclusion_triggered": "x",
            "rationale": "the surface string only",
        }
    return None


# --- sweep: log-odds ---------------------------------------------------------


def test_log_odds_matches_a_hand_computed_two_model_example() -> None:
    """Two models, four words, alpha0 = 4: every term derived by hand below."""
    docs = [
        Doc.from_text("a/memo-01", "A", "memo", "Alpha beta alpha. Alpha gamma alpha alpha."),
        Doc.from_text("b/memo-01", "B", "memo", "Beta gamma beta. Beta delta beta beta."),
    ]
    counts = sweep.token_counts(docs, 1)
    assert counts.loc["alpha", "A"] == 5 and counts.loc["alpha", "B"] == 0
    assert counts.loc["beta", "A"] == 1 and counts.loc["beta", "B"] == 5

    frame = sweep.log_odds_dirichlet(counts, "A", alpha0=4.0)

    # n_A = n_B = 7, n_total = 14, alpha0 = 4.
    # For "alpha": y_w = 5, so a_w = 4 * 5 / 14 = 10/7.
    a_w = 4.0 * 5.0 / 14.0
    numerator_i = 5 + a_w  # 45/7
    denominator_i = 7 + 4 - 5 - a_w  # 32/7
    numerator_j = 0 + a_w  # 10/7
    denominator_j = 7 + 4 - 0 - a_w  # 67/7
    delta = math.log(numerator_i / denominator_i) - math.log(numerator_j / denominator_j)
    sigma = math.sqrt(1.0 / numerator_i + 1.0 / numerator_j)

    assert delta == pytest.approx(math.log(45 * 67 / (32 * 10)))
    assert frame.loc["alpha", "delta"] == pytest.approx(delta)
    assert frame.loc["alpha", "z"] == pytest.approx(delta / sigma)
    assert frame.loc["alpha", "z"] == pytest.approx(2.42500, abs=1e-5)


def test_log_odds_is_antisymmetric_between_two_models() -> None:
    docs = [
        Doc.from_text("a/memo-01", "A", "memo", "Alpha beta alpha. Alpha gamma alpha alpha."),
        Doc.from_text("b/memo-01", "B", "memo", "Beta gamma beta. Beta delta beta beta."),
    ]
    counts = sweep.token_counts(docs, 1)
    left = sweep.log_odds_dirichlet(counts, "A", alpha0=4.0)
    right = sweep.log_odds_dirichlet(counts, "B", alpha0=4.0)
    for word in ("alpha", "beta", "gamma", "delta"):
        assert left.loc[word, "z"] == pytest.approx(-right.loc[word, "z"])


def test_the_z_threshold_filters_and_the_sweep_is_deterministic(corpus: list[Doc]) -> None:
    rows = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=50)
    assert rows, "the planted model-a phrase should clear the threshold"
    assert all(abs(row["z"]) >= 3.09 for row in rows)
    assert all(row["counts"]["model-a"] >= 5 for row in rows)

    again = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=50)
    assert rows == again

    strict = sweep.sweep_rows(corpus, "model-a", z_min=50.0, min_count=5, top_k=50)
    assert strict == []


def test_the_sweep_finds_the_planted_model_a_phrase(corpus: list[Doc]) -> None:
    rows = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=200)
    found = {row["ngram"] for row in rows}
    assert "bears emphasis" in found
    row = next(r for r in rows if r["ngram"] == "bears emphasis")
    assert row["counts"] == {"model-a": 40, "model-b": 0, "model-c": 0}
    assert row["doc_freq"]["model-a"] == pytest.approx(1.0)
    assert row["doc_freq"]["model-b"] == pytest.approx(0.0)
    assert row["kwic"] and all(d.startswith("model-a/") for d in
                               (line.split(":", 1)[0] for line in row["kwic"]))


def test_a_uniform_phrase_is_not_a_model_signal(corpus: list[Doc]) -> None:
    rows = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=200)
    assert "delve into" not in {row["ngram"] for row in rows}


def test_run_sweep_writes_three_sorted_files(corpus: list[Doc], tmp_path: Path) -> None:
    summary = sweep.run_sweep(corpus, tmp_path, z_min=3.09, min_count=5, top_k=20)
    for name in (
        sweep.SWEEP_FILENAME,
        sweep.COLLOCATIONS_FILENAME,
        sweep.STAT_DELTAS_FILENAME,
    ):
        assert (tmp_path / name).is_file()
    assert summary["models"] == list(MODELS)

    first = (tmp_path / sweep.SWEEP_FILENAME).read_bytes()
    sweep.run_sweep(corpus, tmp_path, z_min=3.09, min_count=5, top_k=20)
    assert (tmp_path / sweep.SWEEP_FILENAME).read_bytes() == first

    rows = [json.loads(line) for line in
            (tmp_path / sweep.SWEEP_FILENAME).read_text().splitlines()]
    keys = [(r["model"], -abs(r["z"]), r["n"], r["ngram"]) for r in rows]
    assert keys == sorted(keys)


# --- sweep: G2 ---------------------------------------------------------------


def test_g2_matches_a_hand_computed_contingency_table() -> None:
    """o11=20, o12=80, o21=80, o22=820; margins 100/900 by 100/900, N=1000."""
    expected = 2.0 * (
        20 * math.log(20 / 10.0)
        + 80 * math.log(80 / 90.0)
        + 80 * math.log(80 / 90.0)
        + 820 * math.log(820 / 810.0)
    )
    assert sweep.g2_contingency(20, 80, 80, 820) == pytest.approx(expected)
    assert sweep.g2_contingency(20, 80, 80, 820) == pytest.approx(10.158267, abs=1e-6)


def test_g2_is_zero_when_the_cells_are_exactly_independent() -> None:
    assert sweep.g2_contingency(10, 90, 90, 810) == pytest.approx(0.0, abs=1e-12)


def test_g2_ignores_empty_cells_rather_than_dividing_by_zero() -> None:
    assert sweep.g2_contingency(0, 0, 0, 0) == 0.0
    assert sweep.g2_contingency(5, 0, 0, 5) > 0


def test_collocations_keep_only_significant_frequent_bigrams(corpus: list[Doc]) -> None:
    frame = sweep.collocations_g2(corpus, min_count=10)
    assert not frame.empty
    assert (frame["count"] >= 10).all()
    assert (frame["g2"] >= sweep.G2_CRITICAL).all()
    assert list(frame["g2"]) == sorted(frame["g2"], reverse=True)
    assert "bears emphasis" in set(frame["bigram"])


# --- sweep: stat deltas ------------------------------------------------------


def _fixed_length_doc(model: str, index: int, dashes: int) -> Doc:
    """Exactly 100 word tokens, with `dashes` em dashes between them."""
    words = ["alpha"] * 100
    for slot in range(dashes):
        words.insert(10 * (slot + 1) + slot, "—")
    return Doc.from_text(f"{model}/memo-{index:02d}", model, "memo", " ".join(words))


def test_stat_deltas_recovers_a_planted_cohens_d() -> None:
    """Rates 20/20/30 against 10/10/20 give a pooled SD of sqrt(100/3), so d = sqrt(3)."""
    docs = [_fixed_length_doc("model-a", i, n) for i, n in enumerate([2, 2, 3])]
    docs += [_fixed_length_doc("model-b", i, n) for i, n in enumerate([1, 1, 2])]
    for doc in docs:
        assert doc.words == 100

    frame = sweep.stat_deltas(docs)
    row = frame[(frame["stat"] == "em_dash_per_1k") & (frame["model"] == "model-a")]
    assert len(row) == 1
    assert row.iloc[0]["mean_target"] == pytest.approx(70.0 / 3.0)
    assert row.iloc[0]["mean_rest"] == pytest.approx(40.0 / 3.0)
    assert row.iloc[0]["cohens_d"] == pytest.approx(math.sqrt(3.0))
    assert bool(row.iloc[0]["flagged"]) is True

    mirror = frame[(frame["stat"] == "em_dash_per_1k") & (frame["model"] == "model-b")]
    assert mirror.iloc[0]["cohens_d"] == pytest.approx(-math.sqrt(3.0))


def test_cohens_d_is_undefined_without_variation() -> None:
    assert math.isnan(sweep.cohens_d([1.0, 1.0], [1.0, 1.0]))
    assert math.isnan(sweep.cohens_d([1.0], [2.0, 3.0]))


def test_stat_deltas_drops_nan_rather_than_reading_it_as_zero() -> None:
    """A doc too short for a sentence stat contributes no observation to it."""
    docs = [
        Doc.from_text("model-a/email-01", "model-a", "email", "Short note. Two lines."),
        Doc.from_text("model-b/email-01", "model-b", "email", "Also short. Two lines."),
    ]
    frame = sweep.stat_deltas(docs)
    row = frame[
        (frame["stat"] == "sentence_length_cv") & (frame["model"] == "model-a")
    ].iloc[0]
    assert row["n_target"] == 0
    assert math.isnan(row["cohens_d"])


# --- sweep: kwic -------------------------------------------------------------


def test_kwic_returns_one_marked_line_per_document(corpus: list[Doc]) -> None:
    lines = sweep.kwic(corpus, "bears emphasis", k=4)
    assert len(lines) == 4
    assert all("«" in line and "»" in line for line in lines)
    doc_ids = [line.split(":", 1)[0] for line in lines]
    assert doc_ids == sorted(doc_ids)
    assert len(set(doc_ids)) == len(doc_ids)


def test_kwic_is_whitespace_tolerant_across_a_line_break() -> None:
    doc = Doc.from_text("m/memo-01", "m", "memo", "We will delve\ninto the numbers.")
    assert sweep.kwic([doc], "delve into", k=2)


# --- the lenses --------------------------------------------------------------


def test_excerpt_selection_is_stratified_and_deterministic(corpus: list[Doc]) -> None:
    chosen = auditor.select_excerpts(corpus, "lexical", model="model-a", n=5)
    assert len(chosen) == 5
    assert {item["model"] for item in chosen} == {"model-a"}
    assert len({item["format"] for item in chosen}) == 5
    assert chosen == auditor.select_excerpts(corpus, "lexical", model="model-a", n=5)


def test_contrast_excerpts_exclude_the_target_and_span_the_others(corpus: list[Doc]) -> None:
    chosen = auditor.select_excerpts(corpus, "lexical", exclude_model="model-a", n=6)
    assert {item["model"] for item in chosen} == {"model-b", "model-c"}


def test_each_lens_sees_its_own_view_of_a_document(corpus: list[Doc]) -> None:
    doc = corpus[0]
    lexical = auditor.select_excerpts([doc], "lexical", model=doc.model, n=1)[0]["text"]
    formatting = auditor.select_excerpts([doc], "formatting", model=doc.model, n=1)[0]["text"]
    structural = auditor.select_excerpts([doc], "structural", model=doc.model, n=1)[0]["text"]
    assert "#" not in lexical
    assert "#" in formatting
    assert structural.startswith("SKELETON ")
    assert "PARA:" in structural


def test_excerpt_text_takes_the_head_and_the_middle() -> None:
    body = "".join(f"{i:04d} " for i in range(1000))
    excerpt = auditor.excerpt_text(body, chars=200)
    assert excerpt.startswith("0000 ")
    assert "\n[…]\n" in excerpt
    assert len(excerpt) <= 200 + len("\n[…]\n")


def test_a_lens_prompt_is_deterministic_and_carries_its_inputs(
    corpus: list[Doc], registry: Registry
) -> None:
    rows = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=5)
    target = auditor.select_excerpts(corpus, "lexical", model="model-a")
    contrast = auditor.select_excerpts(corpus, "lexical", exclude_model="model-a")
    tells = registry.active_tells()

    prompt = auditor.build_lens_prompt(
        "lexical", "model-a", target, contrast, rows, tells
    )
    assert prompt == auditor.build_lens_prompt(
        "lexical", "model-a", target, contrast, rows, tells
    )

    assert "TARGET MODEL: model-a" in prompt
    assert "LENS: LEXICAL" in prompt
    assert target[0]["doc_id"] in prompt
    assert contrast[0]["doc_id"] in prompt
    assert "bears emphasis" in prompt  # a sweep row
    assert "lex.delve" in prompt  # an existing tell id
    assert "Do NOT re-propose" in prompt
    assert '"scope_hypothesis"' in prompt


def test_the_structural_lens_gets_skeletons_and_no_ngram_table(
    corpus: list[Doc], registry: Registry
) -> None:
    rows = sweep.sweep_rows(corpus, "model-a", z_min=3.09, min_count=5, top_k=5)
    prompt = auditor.build_lens_prompt(
        "structural",
        "model-a",
        auditor.select_excerpts(corpus, "structural", model="model-a"),
        auditor.select_excerpts(corpus, "structural", exclude_model="model-a"),
        rows,
        registry.active_tells(),
    )
    assert "STATISTICAL SWEEP" not in prompt
    assert "SKELETON " in prompt
    assert "Never propose a regex from this lens" in prompt


def test_an_unknown_lens_is_refused() -> None:
    with pytest.raises(ValueError, match="unknown lens"):
        auditor.build_lens_prompt("vibes", "model-a", [], [], [], [])


# --- the output contract -----------------------------------------------------


GOOD_CANDIDATE = {
    "name": "bears emphasis",
    "category": "lexical",
    "scope_hypothesis": "model:model-a",
    "method": "regex",
    "rule": {"pattern": r"\bit bears emphasis\b", "flags": ["IGNORECASE"]},
    "examples": [CONCENTRATED, CONCENTRATED, CONCENTRATED],
    "rationale": "model-a opens a closing beat with this phrase; the others never do.",
}


def test_a_well_formed_candidate_validates() -> None:
    assert validate_ok(GOOD_CANDIDATE, [CONCENTRATED])


def validate_ok(candidate: dict, excerpts: list[str]) -> bool:
    return auditor.validate_candidate(candidate, excerpts) == []


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ({"category": "vibes"}, "category"),
        ({"scope_hypothesis": "sometimes"}, "scope_hypothesis"),
        ({"method": "vibes"}, "method"),
        ({"examples": ["one", "two"]}, "at least"),
        ({"rationale": ""}, "rationale"),
        ({"name": ""}, "name"),
        ({"rule": {"flags": []}}, "pattern"),
    ],
)
def test_the_schema_catches_each_way_a_candidate_can_be_malformed(
    mutation: dict, expected: str
) -> None:
    candidate = {**GOOD_CANDIDATE, **mutation}
    errors = auditor.validate_candidate(candidate, [CONCENTRATED])
    assert any(expected in error for error in errors), errors


def test_an_example_that_is_not_in_the_excerpts_is_rejected() -> None:
    candidate = {**GOOD_CANDIDATE, "examples": ["A sentence nobody wrote."] * 3}
    errors = auditor.validate_candidate(candidate, [CONCENTRATED])
    assert any("not verbatim in the excerpts" in error for error in errors)


def test_examples_are_matched_after_whitespace_is_normalized() -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "examples": ["It bears\n  emphasis that the schedule has not moved."] * 3,
    }
    assert auditor.validate_candidate(candidate, [CONCENTRATED]) == []


def test_the_structural_lens_may_not_propose_a_regex() -> None:
    errors = auditor.validate_candidate(GOOD_CANDIDATE, [CONCENTRATED], lens="structural")
    assert any("structural lens may not propose a regex" in e for e in errors)


def test_a_nested_rule_body_is_normalized_to_flat_keys() -> None:
    nested = {**GOOD_CANDIDATE, "rule": {"regex": {"pattern": r"\bx\b", "flags": []}}}
    assert auditor.validate_candidate(nested, [CONCENTRATED]) == []
    assert auditor.normalize_rule(nested) == {"pattern": r"\bx\b", "flags": []}


# --- running a lens ----------------------------------------------------------


def lens_router(payloads: list[dict[str, Any]]):
    """Answer DISCOVER calls from a list, in order."""
    box = list(payloads)

    def router(stage: str, tell_id: str, prompt: str, index: int):
        if stage != cache_mod.DISCOVER:
            return None
        return box.pop(0) if box else {"candidates": []}

    return router


def test_run_audit_writes_validated_candidates_with_provenance(
    corpus: list[Doc], tmp_path: Path
) -> None:
    client = FakeClient(lens_router([{"candidates": [GOOD_CANDIDATE]}]))
    run = auditor.run_audit(
        corpus, client, "lexical", "model-a", out_dir=tmp_path, run_id="run-1"
    )
    assert len(run.candidates) == 1
    assert run.retried is False

    provenance = run.candidates[0]["provenance"]
    assert provenance["lens"] == "lexical"
    assert provenance["target_model"] == "model-a"
    assert provenance["run_id"] == "run-1"
    assert provenance["judge_model"] == "claude-opus-4-6"
    assert len(provenance["excerpt_doc_ids"]) == auditor.N_EXCERPTS

    path = tmp_path / auditor.candidates_filename("lexical", "model-a")
    assert auditor.load_candidates(path)[0]["name"] == "bears emphasis"


def test_the_lens_call_is_keyed_in_the_discover_namespace(corpus: list[Doc]) -> None:
    client = FakeClient(lens_router([{"candidates": []}]))
    auditor.run_audit(corpus, client, "rhetorical", "model-a")
    call = client.calls[0]
    assert call["stage"] == cache_mod.DISCOVER
    assert call["tell_id"] == "lens:rhetorical"
    assert call["rubric_version"] == auditor.LENS_PROMPT_VERSION


def test_a_bad_reply_earns_exactly_one_retry_carrying_the_problems(
    corpus: list[Doc],
) -> None:
    bad = {**GOOD_CANDIDATE, "examples": ["never written anywhere"] * 3}
    client = FakeClient(
        lens_router([{"candidates": [bad]}, {"candidates": [GOOD_CANDIDATE]}])
    )
    run = auditor.run_audit(corpus, client, "lexical", "model-a")

    assert run.retried is True
    assert len(client.calls) == 2
    assert "did not satisfy the output contract" in client.calls[1]["prompt"]
    assert "not verbatim in the excerpts" in client.calls[1]["prompt"]
    assert len(run.candidates) == 1
    assert run.rejected == []


def test_a_second_bad_reply_is_recorded_rather_than_raised(corpus: list[Doc]) -> None:
    bad = {**GOOD_CANDIDATE, "category": "vibes"}
    client = FakeClient(lens_router([{"candidates": [bad]}, {"candidates": [bad]}]))
    run = auditor.run_audit(corpus, client, "lexical", "model-a")
    assert run.candidates == []
    assert len(run.rejected) == 1
    assert len(client.calls) == 2


def test_one_good_candidate_beside_a_bad_one_does_not_trigger_a_retry(
    corpus: list[Doc],
) -> None:
    bad = {**GOOD_CANDIDATE, "name": ""}
    client = FakeClient(lens_router([{"candidates": [GOOD_CANDIDATE, bad]}]))
    run = auditor.run_audit(corpus, client, "lexical", "model-a")
    assert len(run.candidates) == 1
    assert len(run.rejected) == 1
    assert len(client.calls) == 1


# --- gate 1: executability ---------------------------------------------------


def test_a_degenerate_pattern_fails_the_token_share_ceiling(corpus: list[Doc]) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": ".*", "flags": []}}
    gate, hint = verify.gate_executable(candidate, corpus)
    assert gate.passed is False
    assert hint == ""
    assert "measuring the language" in gate.detail
    assert gate.data["matched_token_share"] >= verify.MAX_TOKEN_SHARE


def test_a_pattern_that_does_not_compile_fails_gate_one(corpus: list[Doc]) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": "(unclosed", "flags": []}}
    gate, _ = verify.gate_executable(candidate, corpus)
    assert gate.passed is False and "does not compile" in gate.detail


def test_an_unknown_regex_flag_fails_gate_one(corpus: list[Doc]) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": r"\bx\b", "flags": ["SLOPPY"]}}
    gate, _ = verify.gate_executable(candidate, corpus)
    assert gate.passed is False and "unknown regex flag" in gate.detail


def test_a_tight_pattern_passes_gate_one(corpus: list[Doc]) -> None:
    gate, hint = verify.gate_executable(GOOD_CANDIDATE, corpus)
    assert gate.passed is True and hint == ""
    assert gate.data["median_ms"] < verify.MAX_MEDIAN_MS
    assert gate.data["matched_token_share"] < verify.MAX_TOKEN_SHARE


def test_an_unimplemented_statistic_is_parked_not_rejected(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "structural",
        "method": "statistic",
        "rule": {"stat_name": "heading_depth_entropy", "formula_sketch": "entropy of levels"},
    }
    gate, hint = verify.gate_executable(candidate, corpus)
    assert gate.passed is False
    assert hint == verify.STATUS_NEEDS_STAT
    assert "a human has to implement" in gate.detail


def test_a_registered_statistic_passes_gate_one(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "structural",
        "method": "statistic",
        "rule": {"stat_name": "bullet_lines_per_1k", "formula_sketch": "bullets per 1k"},
    }
    gate, hint = verify.gate_executable(candidate, corpus)
    assert gate.passed is True and hint == ""


JUDGE_RUBRIC = """\
A span counts as an instance when ALL of the following hold.
(a) The sentence asks a question the writer immediately answers.
(b) The question is not addressed to a named person.

EXCLUSIONS: a span does NOT count if any of these applies.
(x) The question appears inside a quotation.

Evidence to extract: the question and the sentence answering it.
"""


def test_a_judge_rubric_that_parses_passes_gate_one(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "syntactic",
        "method": "judge",
        "rule": {"rubric": JUDGE_RUBRIC, "judge_view": "chunk"},
    }
    gate, _ = verify.gate_executable(candidate, corpus)
    assert gate.passed is True
    assert gate.data["criteria"] == ["a", "b"]
    assert gate.data["exclusions"] == ["x"]


def test_a_rubric_without_criterion_labels_fails_gate_one(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "syntactic",
        "method": "judge",
        "rule": {"rubric": "Look for questions that get answered.", "judge_view": "chunk"},
    }
    gate, _ = verify.gate_executable(candidate, corpus)
    assert gate.passed is False and "criterion labels" in gate.detail


def test_a_bad_judge_view_fails_gate_one(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "syntactic",
        "method": "judge",
        "rule": {"rubric": JUDGE_RUBRIC, "judge_view": "whole-document"},
    }
    gate, _ = verify.gate_executable(candidate, corpus)
    assert gate.passed is False and "judge_view" in gate.detail


# --- gate 2: prevalence ------------------------------------------------------


def test_a_pattern_that_fires_nowhere_fails_gate_two(corpus: list[Doc]) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": r"\bquixotic zephyr\b", "flags": []}}
    gate = verify.gate_prevalence(verify.measure(candidate, corpus))
    assert gate.passed is False
    assert "top document frequency" in gate.detail


def test_a_planted_phrase_passes_gate_two(corpus: list[Doc]) -> None:
    gate = verify.gate_prevalence(verify.measure(GOOD_CANDIDATE, corpus))
    assert gate.passed is True
    assert gate.data["doc_freq"]["model-a"] == pytest.approx(1.0)


# --- gate 3: discrimination and scope ---------------------------------------


def test_a_concentrated_pattern_lands_model_scoped_with_the_right_z(
    corpus: list[Doc],
) -> None:
    measurement = verify.measure(GOOD_CANDIDATE, corpus)
    gate, scope = verify.gate_scope(measurement, "model-a")
    assert gate.passed is True
    assert scope == "model:model-a"

    # k1=20 n1=20 against k2=0 n2=40; pooled p = 1/3.
    expected = (1.0 - 0.0) / math.sqrt((1 / 3) * (2 / 3) * (1 / 20 + 1 / 40))
    assert gate.data["scope_z"]["model-a"] == pytest.approx(expected)
    assert gate.data["scope_z"]["model-a"] == pytest.approx(7.745967, abs=1e-6)


def test_a_uniform_pattern_lands_general(corpus: list[Doc]) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": r"\bdelve\b", "flags": []}}
    gate, scope = verify.gate_scope(verify.measure(candidate, corpus))
    assert gate.passed is True and scope == "general"
    assert "general" in gate.detail


def test_a_thin_signal_in_one_model_is_rejected_rather_than_scoped() -> None:
    """One document in twenty: clears prevalence, fails the z, and is not general."""
    docs: list[Doc] = []
    for model in ("model-a", "model-b"):
        for i in range(20):
            planted = model == "model-a" and i == 0
            text = BASE + (" The lodestar remains the same." if planted else "")
            docs.append(Doc.from_text(f"{model}/memo-{i:02d}", model, "memo", text))
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": r"\blodestar\b", "flags": []}}
    measurement = verify.measure(candidate, docs)
    assert verify.gate_prevalence(measurement).passed is True

    gate, scope = verify.gate_scope(measurement)
    assert gate.passed is False and scope == ""
    assert "concentrated in no model" in gate.detail
    assert gate.data["scope_z"]["model-a"] < verify.SCOPE_Z


def test_the_two_proportion_z_is_undefined_on_an_empty_group() -> None:
    assert math.isnan(verify.two_proportion_z(0, 0, 0, 0))
    assert math.isnan(verify.two_proportion_z(0, 10, 0, 10))


# --- gate 4: precision -------------------------------------------------------


def test_the_adhoc_rubric_parses_the_way_the_protocol_expects() -> None:
    from telltale.judge import protocol

    rubric = verify.adhoc_rubric(GOOD_CANDIDATE)
    inclusion, exclusions, evidence = protocol.split_rubric(rubric)
    assert "bears emphasis" in inclusion
    assert exclusions.startswith("EXCLUSIONS:")
    assert evidence.startswith("Evidence to extract:")
    assert protocol.parse_rubric_labels(rubric) == (("a",), ("x",))


def test_gate_four_accepts_when_the_adjudicator_confirms(corpus: list[Doc]) -> None:
    client = FakeClient(always_true_adjudicator)
    gate = verify.gate_precision(
        GOOD_CANDIDATE, verify.measure(GOOD_CANDIDATE, corpus), corpus, client
    )
    assert gate.passed is True
    assert gate.data["n"] == verify.PRECISION_SAMPLE
    assert gate.data["true"] == verify.PRECISION_SAMPLE
    assert all(call["stage"] == cache_mod.ADJUDICATE for call in client.calls)


def test_gate_four_rejects_when_the_adjudicator_excludes(corpus: list[Doc]) -> None:
    client = FakeClient(always_false_adjudicator)
    gate = verify.gate_precision(
        GOOD_CANDIDATE, verify.measure(GOOD_CANDIDATE, corpus), corpus, client
    )
    assert gate.passed is False
    assert gate.data["true"] == 0
    assert "needs 8" in gate.detail


def test_gate_four_is_seeded_and_reproducible(corpus: list[Doc]) -> None:
    measurement = verify.measure(GOOD_CANDIDATE, corpus)
    first = verify.gate_precision(
        GOOD_CANDIDATE, measurement, corpus, FakeClient(always_true_adjudicator)
    )
    second = verify.gate_precision(
        GOOD_CANDIDATE, measurement, corpus, FakeClient(always_true_adjudicator)
    )
    assert [row["doc_id"] for row in first.data["adjudicated"]] == [
        row["doc_id"] for row in second.data["adjudicated"]
    ]


def test_gate_four_is_skipped_for_judge_candidates(corpus: list[Doc]) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "category": "syntactic",
        "method": "judge",
        "rule": {"rubric": JUDGE_RUBRIC, "judge_view": "chunk"},
    }
    client = FakeClient(always_false_adjudicator)
    gate = verify.gate_precision(candidate, verify.Measurement(), corpus, client)
    assert gate.passed is True
    assert gate.data["skipped"] is True
    assert "calibration" in gate.detail
    assert client.calls == []


def test_the_judge_verdict_does_not_override_the_criteria(corpus: list[Doc]) -> None:
    """The code decides from criteria_met; `instance` is recorded, not consulted."""

    def contrarian(stage: str, tell_id: str, prompt: str, index: int):
        if stage == cache_mod.ADJUDICATE:
            return {
                "instance": False,
                "criteria_met": ["a"],
                "exclusion_triggered": None,
                "rationale": "criteria hold although I would not call it one",
            }
        return None

    gate = verify.gate_precision(
        GOOD_CANDIDATE,
        verify.measure(GOOD_CANDIDATE, corpus),
        corpus,
        FakeClient(contrarian),
    )
    assert gate.passed is True


# --- gate 5: dedup -----------------------------------------------------------


def test_pattern_normalization_folds_notation_not_meaning() -> None:
    assert dedup.patterns_match(r"\bdelve\b", r"\b delve \b")
    assert dedup.patterns_match(r"(?:a|b)", r"(a|b)")
    assert not dedup.patterns_match(r"\bdelve\b", r"\bdelved\b")


def test_a_re_proposal_of_lex_delve_is_caught_by_the_pattern_test(
    corpus: list[Doc], registry: Registry
) -> None:
    existing = registry.get("lex.delve")
    candidate = {
        **GOOD_CANDIDATE,
        "name": "delve",
        "rule": {"pattern": existing.pattern, "flags": ["IGNORECASE"]},
    }
    counts, patterns, names = verify.registry_counts(registry, corpus)
    gate, result = verify.gate_dedup(
        candidate, verify.measure(candidate, corpus), counts, patterns, names
    )
    assert gate.passed is False
    assert result.duplicate_of == "lex.delve"
    assert "textually identical" in result.reason


def test_a_differently_written_delve_is_caught_behaviourally(
    corpus: list[Doc], registry: Registry
) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "name": "digs into the detail",
        "rule": {"pattern": r"\bdelve(?:s|d)?\b|\bdelving\b", "flags": ["IGNORECASE"]},
    }
    counts, patterns, names = verify.registry_counts(registry, corpus)
    assert not dedup.patterns_match(
        candidate["rule"]["pattern"], registry.get("lex.delve").pattern
    )

    gate, result = verify.gate_dedup(
        candidate, verify.measure(candidate, corpus), counts, patterns, names
    )
    assert gate.passed is False
    assert result.duplicate_of == "lex.delve"
    jaccard, rho = result.overlaps["lex.delve"]
    assert jaccard == pytest.approx(1.0)
    assert rho == pytest.approx(1.0)


def test_a_near_name_collision_is_flagged_not_rejected(
    corpus: list[Doc], registry: Registry
) -> None:
    candidate = {**GOOD_CANDIDATE, "name": "delves"}
    counts, patterns, names = verify.registry_counts(registry, corpus)
    gate, result = verify.gate_dedup(
        candidate, verify.measure(candidate, corpus), counts, patterns, names
    )
    assert gate.passed is True
    assert result.duplicate_of == ""
    assert any(flag.startswith("name-fuzz:lex.delve") for flag in result.flags)
    assert "flagged for human review" in gate.detail


def test_jaccard_and_spearman_behave_at_the_edges() -> None:
    assert dedup.jaccard([], []) == 0.0
    assert dedup.jaccard(["a"], ["a"]) == 1.0
    assert dedup.jaccard(["a", "b"], ["b", "c"]) == pytest.approx(1 / 3)
    assert math.isnan(dedup.spearman([1, 1, 1], [1, 2, 3]))
    assert dedup.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert dedup.spearman([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)


def test_both_overlap_measures_are_required_to_call_it_a_duplicate() -> None:
    """Same documents, opposite intensities: not one measurement."""
    left = {"d1": 1.0, "d2": 2.0, "d3": 3.0, "d4": 4.0}
    right = {"d1": 4.0, "d2": 3.0, "d3": 2.0, "d4": 1.0}
    duplicate, jaccard, rho = dedup.behavioural_duplicate(left, right)
    assert jaccard == pytest.approx(1.0)
    assert rho == pytest.approx(-1.0)
    assert duplicate is False


# --- the pipeline end to end -------------------------------------------------


def test_verify_all_runs_every_gate_in_order(corpus: list[Doc], registry: Registry) -> None:
    verdicts = verify.verify_all(
        [GOOD_CANDIDATE], corpus, registry, FakeClient(always_true_adjudicator)
    )
    assert len(verdicts) == 1
    verdict = verdicts[0]
    assert verdict.accepted
    assert verdict.scope == "model:model-a"
    assert [g.gate for g in verdict.gates] == [1, 2, 3, 4, 5]


def test_a_rejected_candidate_short_circuits_at_the_gate_that_failed(
    corpus: list[Doc], registry: Registry
) -> None:
    candidate = {**GOOD_CANDIDATE, "rule": {"pattern": ".*", "flags": []}}
    verdict = verify.verify_all([candidate], corpus, registry, None)[0]
    assert verdict.status == verify.STATUS_REJECTED
    assert [g.gate for g in verdict.gates] == [1]


def test_a_regex_candidate_cannot_be_accepted_without_a_judge(
    corpus: list[Doc], registry: Registry
) -> None:
    verdict = verify.verify_all([GOOD_CANDIDATE], corpus, registry, None)[0]
    assert verdict.status == verify.STATUS_REJECTED
    assert "no judge backend" in verdict.reason


def test_a_judge_candidate_defers_prevalence_and_scope(
    corpus: list[Doc], registry: Registry
) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "name": "question then answer",
        "category": "syntactic",
        "scope_hypothesis": "general",
        "method": "judge",
        "rule": {"rubric": JUDGE_RUBRIC, "judge_view": "chunk"},
    }
    verdict = verify.verify_all(
        [candidate], corpus, registry, FakeClient(always_true_adjudicator)
    )[0]
    assert verdict.accepted
    assert verdict.scope == "general"
    assert verdict.gate(2).data["deferred"] is True
    assert verdict.gate(3).data["deferred"] is True
    assert verdict.gate(4).data["skipped"] is True


# --- to_tell and the registry round trip -------------------------------------


def test_to_tell_produces_a_valid_candidate_that_survives_a_reload(
    corpus: list[Doc], registry: Registry
) -> None:
    verdict = verify.verify_all(
        [GOOD_CANDIDATE], corpus, registry, FakeClient(always_true_adjudicator)
    )[0]
    tells = verify.append_accepted([verdict], registry, "discover-test", docs=corpus)
    assert len(tells) == 1
    tell = tells[0]
    assert tell.id == "phr.bears-emphasis"
    assert tell.status == "candidate"
    assert tell.scope == "model:model-a"
    assert tell.provenance["source"] == "discovery"
    assert tell.provenance["run_id"] == "discover-test"
    assert tell.provenance["evidence"]["lens"] is None  # no lens provenance on this one
    assert tell.provenance["evidence"]["doc_freq"]["model-a"] == 1.0
    assert tell.provenance["evidence"]["precision"]["true"] == 10

    reloaded = Registry(registry.path)
    assert reloaded.validate() == []
    again = reloaded.get("phr.bears-emphasis")
    assert again.scope == "model:model-a"
    assert again.status == "candidate"
    assert again.examples


def test_a_candidate_is_ignored_by_default_scoring_and_seen_with_the_flag(
    corpus: list[Doc], registry: Registry
) -> None:
    from telltale import scoring

    verdict = verify.verify_all(
        [GOOD_CANDIDATE], corpus, registry, FakeClient(always_true_adjudicator)
    )[0]
    verify.append_accepted([verdict], registry, "discover-test", docs=corpus)
    reloaded = Registry(registry.path)

    default = scoring.detect_all(corpus, [t for t in reloaded.active_tells()
                                          if t.method != "judge"])
    assert "phr.bears-emphasis" not in set(default["tell_id"])

    with_candidates = scoring.detect_all(
        corpus,
        [t for t in reloaded.active_tells(include_candidates=True) if t.method != "judge"],
    )
    rows = with_candidates[with_candidates["tell_id"] == "phr.bears-emphasis"]
    assert len(rows) == len(corpus)
    assert rows[rows["model"] == "model-a"]["raw"].sum() == 2.0 * DOCS_PER_MODEL
    assert rows[rows["model"] == "model-b"]["raw"].sum() == 0.0
    assert set(rows["scope"]) == {"model:model-a"}


def test_an_id_collision_is_disambiguated_rather_than_overwriting() -> None:
    taken = {"phr.bears-emphasis"}
    assert verify.make_tell_id("bears emphasis", "lexical", taken) == "phr.bears-emphasis-2"


def test_single_word_lexical_tells_get_the_lex_prefix() -> None:
    assert verify.make_tell_id("lodestar", "lexical", set()) == "lex.lodestar"
    assert verify.make_tell_id("bullet density", "structural", set()) == "str.bullet-density"
    assert verify.make_tell_id("em dashes", "punctuation", set()) == "pnc.em-dashes"


def test_examples_are_topped_up_from_the_corpus_when_the_model_quotes_loosely(
    corpus: list[Doc], registry: Registry
) -> None:
    """A quote that does not itself match the pattern cannot be the only example."""
    loose = {
        **GOOD_CANDIDATE,
        "examples": [BASE.split(". ")[0] + "."] * 3,  # true prose, no match
    }
    verdict = verify.verify_all(
        [loose], corpus, registry, FakeClient(always_true_adjudicator)
    )[0]
    tell = verify.to_tell(verdict, "discover-test", docs=corpus)
    assert tell.examples
    compiled = tell.compiled()
    assert any(compiled.search(example) for example in tell.examples)


def test_a_statistic_candidate_gets_a_direction_and_an_ordered_ramp(
    corpus: list[Doc], registry: Registry
) -> None:
    candidate = {
        **GOOD_CANDIDATE,
        "name": "bullet density",
        "category": "structural",
        "method": "statistic",
        "rule": {"stat_name": "headings_per_1k", "formula_sketch": "headings per 1k words"},
    }
    verdict = verify.Verdict(candidate=candidate, status=verify.STATUS_ACCEPTED,
                             scope="model:model-a")
    tell = verify.to_tell(verdict, "discover-test", docs=corpus)
    assert tell.unit == "value"
    assert tell.direction in {"high_is_telling", "low_is_telling"}
    assert len(tell.ramp) == 2
    if tell.direction == "high_is_telling":
        assert tell.ramp[0] < tell.ramp[1]
    else:
        assert tell.ramp[0] > tell.ramp[1]


# --- run-all -----------------------------------------------------------------

ACCEPT_GENERAL = {
    "name": "intake window",
    "category": "lexical",
    "scope_hypothesis": "general",
    "method": "regex",
    "rule": {"pattern": r"\bintake window\b", "flags": ["IGNORECASE"]},
    "examples": [UNIFORM_LATE] * 3,
    "rationale": "All three models reach for this framing before a deadline.",
}

ACCEPT_MODEL = dict(GOOD_CANDIDATE)

DUPLICATE = {
    "name": "delve",
    "category": "lexical",
    "scope_hypothesis": "general",
    "method": "regex",
    "rule": {"pattern": r"\bdelv(?:e|es|ed|ing)\b", "flags": ["IGNORECASE"]},
    "examples": [UNIFORM] * 3,
    "rationale": "The canonical marker, proposed again.",
}


def run_all_router(stage: str, tell_id: str, prompt: str, index: int):
    if stage == cache_mod.DISCOVER:
        if tell_id == "lens:lexical":
            return {"candidates": [ACCEPT_GENERAL, ACCEPT_MODEL, DUPLICATE]}
        return {"candidates": []}
    return always_true_adjudicator(stage, tell_id, prompt, index)


def test_run_all_appends_exactly_the_candidates_that_survive(
    corpus: list[Doc], registry: Registry, tmp_path: Path
) -> None:
    client = FakeClient(run_all_router)
    lines: list[str] = []
    summary = pipeline.run_all(
        corpus,
        tmp_path / "discovery",
        registry,
        judge_client=client,
        judge_backend=client,
        models=["model-a"],
        run_id="discover-e2e",
        log=lines.append,
    )

    assert summary["run_id"] == "discover-e2e"
    assert [s["stage"] for s in summary["stages"]] == [
        "sweep",
        "audit/lexical/model-a",
        "audit/rhetorical/model-a",
        "audit/structural/model-a",
        "audit/formatting/model-a",
        "verify",
        "append",
    ]

    reloaded = Registry(registry.path)
    assert reloaded.validate() == []
    added = [t for t in reloaded if t.provenance and t.provenance.get("run_id") == "discover-e2e"]
    assert len(added) == 2
    by_scope = {t.scope: t for t in added}
    assert set(by_scope) == {"general", "model:model-a"}
    assert by_scope["general"].name == "intake window"
    assert by_scope["model:model-a"].name == "bears emphasis"
    assert all(t.status == "candidate" for t in added)
    assert all(t.provenance["evidence"]["lens"] == "lexical" for t in added)
    assert all(t.provenance["evidence"]["target_model"] == "model-a" for t in added)

    verdicts = [
        json.loads(line)
        for line in pipeline.verdicts_path(tmp_path / "discovery").read_text().splitlines()
    ]
    assert len(verdicts) == 3
    rejected = [v for v in verdicts if v["status"] == verify.STATUS_REJECTED]
    assert len(rejected) == 1
    assert rejected[0]["candidate"]["name"] == "delve"
    assert "lex.delve" in rejected[0]["reason"]


def test_run_all_resumes_by_skipping_completed_stages(
    corpus: list[Doc], registry: Registry, tmp_path: Path
) -> None:
    out = tmp_path / "discovery"
    first = FakeClient(run_all_router)
    pipeline.run_all(
        corpus, out, registry, judge_client=first, judge_backend=first,
        models=["model-a"], run_id="discover-e2e",
    )
    calls_first = len(first.calls)

    second = FakeClient(run_all_router)
    summary = pipeline.run_all(
        corpus, out, registry, judge_client=second, judge_backend=second,
        models=["model-a"], run_id="discover-e2e",
    )
    assert second.calls == []
    assert calls_first > 0
    assert all(stage["skipped"] for stage in summary["stages"])

    reloaded = Registry(registry.path)
    added = [t for t in reloaded if t.provenance and t.provenance.get("run_id") == "discover-e2e"]
    assert len(added) == 2, "a resumed run must not append a second copy"


def test_forcing_a_stage_reruns_it(
    corpus: list[Doc], registry: Registry, tmp_path: Path
) -> None:
    out = tmp_path / "discovery"
    client = FakeClient(run_all_router)
    pipeline.stage_sweep(corpus, out)
    log = pipeline.stage_sweep(corpus, out)
    assert log.skipped is True
    assert pipeline.stage_sweep(corpus, out, force=True).skipped is False


def test_a_run_that_died_between_verify_and_append_still_appends(
    corpus: list[Doc], registry: Registry, tmp_path: Path
) -> None:
    """The verdicts are on disk; resuming must use them, not re-pay for gate 4."""
    out = tmp_path / "discovery"
    client = FakeClient(run_all_router)
    pipeline.stage_sweep(corpus, out)
    pipeline.stage_audit(
        corpus, out, client, ["model-a"], registry=registry, run_id="discover-crash"
    )
    log, verdicts = pipeline.stage_verify(corpus, out, registry, client)
    assert log.skipped is False and len(verdicts) == 3
    assert not (out / pipeline.APPENDED_FILENAME).exists()

    resumed = FakeClient(run_all_router)
    summary = pipeline.run_all(
        corpus, out, registry, judge_client=resumed, judge_backend=resumed,
        models=["model-a"], run_id="discover-crash",
    )
    assert resumed.calls == [], "resuming must not spend a single judge call"
    stages = {s["stage"]: s for s in summary["stages"]}
    assert stages["verify"]["skipped"] is True
    assert stages["append"]["skipped"] is False

    reloaded = Registry(registry.path)
    added = [t for t in reloaded if t.provenance and t.provenance.get("run_id") == "discover-crash"]
    assert len(added) == 2


def test_a_verdict_survives_a_round_trip_through_jsonl(
    corpus: list[Doc], registry: Registry
) -> None:
    original = verify.verify_all(
        [GOOD_CANDIDATE], corpus, registry, FakeClient(always_true_adjudicator)
    )[0]
    restored = verify.Verdict.from_dict(json.loads(json.dumps(original.as_dict())))
    assert restored.status == original.status
    assert restored.scope == original.scope
    assert [g.gate for g in restored.gates] == [g.gate for g in original.gates]
    assert restored.candidate["name"] == original.candidate["name"]


def test_run_all_without_a_judge_client_skips_the_lenses(
    corpus: list[Doc], registry: Registry, tmp_path: Path
) -> None:
    summary = pipeline.run_all(
        corpus, tmp_path / "discovery", registry, judge_client=None, run_id="dry"
    )
    stages = {s["stage"]: s for s in summary["stages"]}
    assert stages["audit"]["skipped"] is True
    assert stages["verify"]["skipped"] is False
    assert stages["verify"]["n"] == 0


# --- the CLI surface ---------------------------------------------------------


def test_the_discover_group_exposes_all_four_subcommands() -> None:
    from telltale.cli import build_parser

    parser = build_parser()
    for action, extra in (
        ("sweep", []),
        ("audit", ["--lens", "lexical", "--target-model", "model-a"]),
        ("verify", []),
        ("run-all", []),
    ):
        args = parser.parse_args(["discover", action, *extra])
        assert callable(args.func)
        assert args.action == action


def test_the_audit_subcommand_refuses_an_unknown_lens() -> None:
    from telltale.cli import build_parser

    with pytest.raises(SystemExit):
        build_parser().parse_args(
            ["discover", "audit", "--lens", "vibes", "--target-model", "m"]
        )


def test_lens_calls_get_a_longer_ceiling_than_span_adjudication() -> None:
    """A lens composes; an adjudication answers. The second is not the first."""
    from telltale.judge.transport import JUDGE_TIMEOUT_S

    assert auditor.LENS_TIMEOUT_S > JUDGE_TIMEOUT_S


def test_the_append_stage_refuses_to_write_an_invalid_tell(
    corpus: list[Doc], registry: Registry
) -> None:
    broken = verify.Verdict(
        candidate={
            "name": "broken",
            "category": "lexical",
            "method": "regex",
            "rule": {"pattern": r"\bnothing here at all\b", "flags": []},
            "examples": ["not a match"],
            "rationale": "x",
        },
        status=verify.STATUS_ACCEPTED,
        scope="general",
    )
    with pytest.raises(ValueError, match="refusing to write invalid tells"):
        verify.append_accepted([broken], registry, "discover-test", docs=[])
    assert Registry(registry.path).validate() == []
