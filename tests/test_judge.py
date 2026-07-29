"""Tests for the Tier-2 judge stack.

No test in this file calls a model. Every judge answer is canned, which is the
only way to test the part that matters: what the code does with an answer once
it has one. The live checks are run by hand and their transcripts live in
runs/calibration/.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from telltale.corpus import Doc
from telltale.detectors import build
from telltale.detectors.judge_detector import JudgeBackend
from telltale.isolation import CliResult
from telltale.judge import audit as audit_mod
from telltale.judge import calibrate as calibration
from telltale.judge import protocol
from telltale.judge.cache import (
    ADJUDICATE,
    EXTRACT,
    STRUCTURAL,
    CacheMiss,
    JudgeCache,
    JudgeClient,
    cache_key,
)
from telltale.judge.transport import (
    GRADED_MODELS,
    JUDGE_ALLOWLIST,
    JUDGE_MODEL_DEFAULT,
    CliJudgeTransport,
    JudgeError,
    assert_judge_model,
    judge_flags,
    parse_json_reply,
    probe_judge,
    resolve_judge,
    strip_fences,
)
from telltale.registry import Registry, Tell

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry" / "tells.yaml"


# --- fixtures and fakes ------------------------------------------------------


@pytest.fixture(scope="module")
def registry() -> Registry:
    return Registry(REGISTRY_PATH)


@pytest.fixture(scope="module")
def qa_tell(registry: Registry) -> Tell:
    return registry.get("rht.rhetorical-qa")


@pytest.fixture(scope="module")
def sandwich_tell(registry: Registry) -> Tell:
    return registry.get("str.summary-sandwich")


def envelope(result: Any, model: str = JUDGE_MODEL_DEFAULT) -> str:
    """A `--output-format json` envelope carrying `result` as the reply text."""
    text = result if isinstance(result, str) else json.dumps(result)
    return json.dumps(
        {
            "result": text,
            "session_id": "s-1",
            "num_turns": 1,
            "is_error": False,
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "modelUsage": {model: {"outputTokens": 20}},
        }
    )


def fake_cli(*stdouts: str, returncode: int = 0):
    """An isolation-style transport that replays canned stdout, in order."""
    replies = list(stdouts)
    calls: list[tuple[list[str], str]] = []

    def transport(cmd: list[str], prompt: str, timeout: int) -> CliResult:
        calls.append((cmd, prompt))
        stdout = replies.pop(0) if replies else replies_default
        return CliResult(returncode=returncode, stdout=stdout, stderr="", duration_s=0.1)

    replies_default = stdouts[-1] if stdouts else ""
    transport.calls = calls  # type: ignore[attr-defined]
    return transport


class FakeJudge:
    """A judge that answers from a router, at the `ask` level."""

    name = "fake"

    def __init__(self, router, model: str = JUDGE_MODEL_DEFAULT) -> None:
        self.router = router
        self.model = model
        self.prompts: list[str] = []

        class _Stats:
            calls = 0
            retries = 0
            failures = 0
            seconds = 0.0

            def as_dict(self) -> dict[str, Any]:
                return {
                    "calls": self.calls,
                    "retries": self.retries,
                    "failures": self.failures,
                    "seconds": self.seconds,
                }

        self.stats = _Stats()

    def ask(self, prompt: str) -> dict[str, Any]:
        self.prompts.append(prompt)
        self.stats.calls += 1
        answer = self.router(prompt)
        if answer is None:
            raise AssertionError(f"fake judge has no answer for:\n{prompt[:400]}")
        return answer


def make_client(tmp_path: Path, router, **kwargs) -> JudgeClient:
    cache = JudgeCache(tmp_path / "judge")
    return JudgeClient(transport=FakeJudge(router), cache=cache, **kwargs)


def doc_from(text: str, doc_id: str = "m/doc-01", fmt: str = "memo") -> Doc:
    return Doc.from_text(doc_id=doc_id, model="m", fmt=fmt, text=text)


# --- transport ---------------------------------------------------------------


def test_the_graded_models_may_never_judge() -> None:
    for model in sorted(GRADED_MODELS):
        with pytest.raises(JudgeError, match="graded model"):
            assert_judge_model(model)


def test_a_dated_graded_model_id_is_refused_too() -> None:
    with pytest.raises(JudgeError, match="graded model"):
        assert_judge_model("claude-opus-5-20260601")


def test_only_allowlisted_models_may_judge() -> None:
    with pytest.raises(JudgeError, match="allowlist"):
        assert_judge_model("claude-haiku-4-5")
    for model in sorted(JUDGE_ALLOWLIST):
        assert assert_judge_model(model) == model


def test_the_default_judge_is_allowlisted_and_not_graded() -> None:
    assert JUDGE_MODEL_DEFAULT in JUDGE_ALLOWLIST
    assert not JUDGE_ALLOWLIST & GRADED_MODELS


def test_the_judge_runs_the_isolation_recipe_with_its_own_system_prompt() -> None:
    from telltale import isolation
    from telltale.judge.transport import JUDGE_SYSTEM_PROMPT

    flags = judge_flags()
    assert flags[flags.index("--system-prompt") + 1] == JUDGE_SYSTEM_PROMPT
    assert "--safe-mode" in flags
    assert flags.count("--system-prompt") == 1
    # Everything except the prompt value is the recipe the corpus was written under.
    assert len(flags) == len(isolation.ISOLATION_FLAGS)


def test_code_fences_are_stripped_before_parsing() -> None:
    assert strip_fences('```json\n{"spans": []}\n```') == '{"spans": []}'
    assert strip_fences('```\n{"a": 1}\n```') == '{"a": 1}'
    assert strip_fences('{"a": 1}') == '{"a": 1}'


def test_a_fenced_reply_parses_through_the_transport() -> None:
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(envelope('```json\n{"spans": []}\n```')),
    )
    assert transport.ask("go") == {"spans": []}
    assert transport.stats.retries == 0


def test_an_unparseable_reply_is_retried_once_and_then_raises() -> None:
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(envelope("I found three spans."), envelope('{"spans": []}')),
    )
    assert transport.ask("go") == {"spans": []}
    assert transport.stats.retries == 1
    assert transport.stats.calls == 2

    hopeless = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(envelope("nope"), envelope("still nope")),
    )
    with pytest.raises(JudgeError, match="not JSON"):
        hopeless.ask("go")
    assert hopeless.stats.failures == 1


def test_the_retry_tells_the_judge_to_drop_the_fences() -> None:
    cli = fake_cli(envelope("prose"), envelope('{"spans": []}'))
    CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli).ask("go")
    assert "no code fences" in cli.calls[1][1]
    assert "no code fences" not in cli.calls[0][1]


def test_a_model_mismatch_is_a_hard_error() -> None:
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(envelope('{"spans": []}', model="claude-haiku-4-5")),
    )
    with pytest.raises(JudgeError, match="model mismatch"):
        transport.ask("go")


def test_a_failed_call_is_an_error_not_an_empty_answer() -> None:
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=fake_cli("", returncode=1)
    )
    with pytest.raises(JudgeError, match="failed"):
        transport.ask("go")


def test_prose_around_a_json_object_still_parses() -> None:
    assert parse_json_reply('Here you go: {"spans": []} — hope that helps') == {"spans": []}


def test_probe_and_resolution_walk_the_allowlist_in_order() -> None:
    def down(cmd, prompt, timeout):
        return CliResult(returncode=1, stdout="", stderr="no", duration_s=0.0)

    assert probe_judge(JUDGE_MODEL_DEFAULT, transport=down) is False
    assert probe_judge("claude-opus-5", transport=down) is False

    seen: list[str] = []

    def second_one_answers(cmd, prompt, timeout):
        model = cmd[cmd.index("--model") + 1]
        seen.append(model)
        if model == "claude-opus-4-7":
            return CliResult(0, envelope('{"ok": true}', model=model), "", 0.1)
        return CliResult(1, "", "unavailable", 0.0)

    assert resolve_judge(transport=second_one_answers) == "claude-opus-4-7"
    assert seen[0] == JUDGE_MODEL_DEFAULT

    with pytest.raises(JudgeError, match="no judge model answered"):
        resolve_judge(transport=down)


# --- chunking ----------------------------------------------------------------


def test_a_document_smaller_than_the_target_is_one_chunk() -> None:
    doc = doc_from("# Title\n\nA short memo about nothing much.\n")
    chunks = protocol.chunk_doc(doc)
    assert len(chunks) == 1
    assert chunks[0].index == 0
    assert chunks[0].doc_id == doc.doc_id
    assert "short memo" in chunks[0].text


def test_chunks_break_on_h2_boundaries() -> None:
    body = " ".join(["word"] * 400)
    text = "\n\n".join(
        [f"## Section {i}\n\n{body}" for i in range(6)]
    )
    chunks = protocol.chunk_doc(doc_from(text), target_words=900)
    assert len(chunks) > 1
    for chunk in chunks[1:]:
        assert chunk.text.lstrip().startswith("## Section")


def test_h3_is_not_a_chunk_boundary() -> None:
    body = " ".join(["word"] * 300)
    text = f"## One\n\n{body}\n\n### Sub\n\n{body}\n\n## Two\n\n{body}"
    chunks = protocol.chunk_doc(doc_from(text), target_words=700)
    assert all("### Sub" not in c.text.split("\n")[0] for c in chunks)


def test_only_an_oversized_section_is_split_and_it_overlaps() -> None:
    line = " ".join(["alpha"] * 50)
    lines = "\n".join(f"{line} sentinel{i}." for i in range(40))  # ~2000 words
    chunks = protocol.chunk_doc(doc_from(f"## Long\n\n{lines}"), target_words=600, overlap_words=120)
    assert len(chunks) > 2
    for earlier, later in zip(chunks, chunks[1:]):
        tail = earlier.text.split("\n")[-1]
        assert tail in later.text, "an oversized split must overlap"


def test_small_sections_are_packed_up_to_the_target() -> None:
    body = " ".join(["word"] * 100)
    text = "\n\n".join(f"## S{i}\n\n{body}" for i in range(10))
    chunks = protocol.chunk_doc(doc_from(text), target_words=500)
    assert 1 < len(chunks) < 10


def test_chunking_is_deterministic_and_hashes_its_text() -> None:
    doc = doc_from("## A\n\n" + " ".join(["word"] * 3000))
    first = protocol.chunk_doc(doc)
    second = protocol.chunk_doc(doc)
    assert [(c.index, c.sha256) for c in first] == [(c.index, c.sha256) for c in second]
    for chunk in first:
        import hashlib

        assert chunk.sha256 == hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()


def test_the_skeleton_view_carries_the_tables_the_skeleton_drops() -> None:
    text = (
        "# Report\n\nSome prose here.\n\n"
        "| Aspect | Description |\n|---|---|\n| Cost | Under budget. |\n"
    )
    doc = doc_from(text)
    from telltale.textstats import doc_skeleton

    assert "Aspect" not in doc_skeleton(doc)
    view = protocol.skeleton_view(doc)
    assert "| Aspect | Description |" in view
    assert protocol.skeleton_view(doc) == view  # deterministic


def test_the_skeleton_view_says_so_when_there_are_no_tables() -> None:
    view = protocol.skeleton_view(doc_from("# Memo\n\nNo tables at all.\n"))
    assert view.endswith("TABLES\n(none)")


# --- quote verification ------------------------------------------------------

SOURCE = "The count changed in March.\nSo why did the count change?  The rule\nchanged in November."


def test_an_exact_quote_verifies_with_its_offsets_and_line() -> None:
    match = protocol.verify_quote("So why did the count change?", SOURCE)
    assert match is not None
    assert SOURCE[match.start : match.end] == "So why did the count change?"
    assert match.line == 2


def test_whitespace_mangling_does_not_make_a_quote_a_hallucination() -> None:
    for variant in (
        "So why did the count change?   The rule",
        "So  why did the count change? The rule",
        "So why did the count change?\nThe rule",
        "  So why did the count change? The rule  ",
    ):
        match = protocol.verify_quote(variant, SOURCE)
        assert match is not None, variant
        assert match.quote.startswith("So why")


def test_a_quote_spanning_a_line_break_maps_back_to_raw_offsets() -> None:
    match = protocol.verify_quote("The rule changed in November.", SOURCE)
    assert match is not None
    assert "\n" in SOURCE[match.start : match.end]
    assert match.quote == "The rule\nchanged in November."
    assert match.line == 2


def test_a_hallucinated_quote_does_not_verify() -> None:
    assert protocol.verify_quote("The rule changed in December.", SOURCE) is None
    assert protocol.verify_quote("", SOURCE) is None
    assert protocol.verify_quote("   ", SOURCE) is None


def test_the_verified_quote_is_the_sources_text_not_the_judges() -> None:
    match = protocol.verify_quote("so why did the count change?".upper(), SOURCE)
    assert match is None  # matching is exact apart from whitespace
    match = protocol.verify_quote("So  why  did  the  count  change?", SOURCE)
    assert match is not None
    assert match.quote == "So why did the count change?"


def test_context_carries_two_sentences_either_side() -> None:
    text = (
        "One. Two. Three. So why did the count change? The rule changed. Six. Seven. Eight."
    )
    match = protocol.verify_quote("So why did the count change?", text)
    context = protocol.context_for(match, text)
    assert context == "Two. Three. So why did the count change? The rule changed. Six."


def test_hallucinated_quotes_are_dropped_and_counted(tmp_path: Path, qa_tell: Tell) -> None:
    text = "So why did the count change? The rule changed in November."

    def router(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            return {
                "spans": [
                    {"quote": "So why did the count change?", "location_hint": "opening"},
                    {"quote": "Why did the sky turn green?", "location_hint": "invented"},
                ]
            }
        return {"instance": True, "criteria_met": ["a", "b"], "exclusion_triggered": None,
                "rationale": "answered immediately"}

    backend = JudgeBackend(make_client(tmp_path, router))
    run = backend.spans_for_text(qa_tell, text)
    assert len(run.counted) == 1
    assert run.hallucinated == ["Why did the sky turn green?"]
    assert run.extracted == 2


# --- the criteria table ------------------------------------------------------


def test_the_criteria_table_matches_the_rubrics_in_the_registry(registry: Registry) -> None:
    """The table is a mirror of the rubric text. Drift has to fail here."""
    judge_tells = [t for t in registry.active_tells() if t.method == "judge"]
    assert {t.id for t in judge_tells} == set(protocol.RULES)
    for tell in judge_tells:
        criteria, exclusions = protocol.parse_rubric_labels(tell.rubric)
        rule = protocol.RULES[tell.id]
        assert rule.required == criteria, f"{tell.id}: criteria drifted from the rubric"
        assert rule.exclusions == exclusions, f"{tell.id}: exclusions drifted"
        # ALL vs ANY is read off the rubric's own opening line.
        head = tell.rubric.split("\n", 1)[0]
        assert rule.mode == ("any" if "ANY" in head else "all"), tell.id


def test_every_judge_tell_has_a_decision_path(registry: Registry) -> None:
    for tell in registry.active_tells():
        if tell.method != "judge":
            continue
        rule = protocol.rule_for(tell)
        if tell.judge_view == "skeleton":
            assert rule.kind == "structural"
            assert tell.id in protocol.STRUCTURAL_DECISIONS
            assert rule.evidence_fields
        else:
            assert rule.kind == "span"


def test_a_rubric_label_inside_prose_is_not_read_as_a_label(registry: Registry) -> None:
    rubric = registry.get("rht.rule-of-three").rubric
    assert "criterion (c) holds" in rubric  # the trap
    criteria, _ = protocol.parse_rubric_labels(rubric)
    assert criteria == ("a", "b", "c")


# --- adjudication enforcement ------------------------------------------------


def test_the_judges_own_verdict_does_not_decide(qa_tell: Tell) -> None:
    rule = protocol.rule_for(qa_tell)
    counts, why = protocol.span_counts(
        rule,
        {"instance": True, "criteria_met": ["a"], "exclusion_triggered": None},
    )
    assert counts is False
    assert "do not meet" in why


def test_an_exclusion_kills_a_span_however_complete_the_criteria(qa_tell: Tell) -> None:
    rule = protocol.rule_for(qa_tell)
    counts, why = protocol.span_counts(
        rule,
        {"instance": True, "criteria_met": ["a", "b"], "exclusion_triggered": "y"},
    )
    assert counts is False
    assert "exclusion (y)" in why


def test_a_complete_span_with_no_exclusion_counts(qa_tell: Tell) -> None:
    rule = protocol.rule_for(qa_tell)
    counts, why = protocol.span_counts(
        rule,
        {"instance": False, "criteria_met": ["(a)", "B"], "exclusion_triggered": None},
    )
    assert counts is True and why == ""


def test_a_judge_writing_none_in_words_has_not_fired_an_exclusion(qa_tell: Tell) -> None:
    rule = protocol.rule_for(qa_tell)
    for value in (None, "none", "null", "", "N/A", "-"):
        assert protocol.exclusion_fired(rule, value) is None
    assert protocol.exclusion_fired(rule, "(x)") == "x"


def test_an_any_mode_tell_needs_only_one_criterion() -> None:
    rule = protocol.RULES["str.table-overuse"]
    assert protocol.criteria_satisfied(rule, ["b"]) is True
    assert protocol.criteria_satisfied(rule, []) is False


def test_a_judge_that_says_instance_true_but_misses_a_criterion_is_recorded(
    tmp_path: Path, qa_tell: Tell
) -> None:
    text = "So why did the count change? The rule changed in November."

    def router(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            return {"spans": [{"quote": "So why did the count change?", "location_hint": ""}]}
        return {"instance": True, "criteria_met": ["a"], "exclusion_triggered": None,
                "rationale": "looks like one"}

    backend = JudgeBackend(make_client(tmp_path, router))
    run = backend.spans_for_text(qa_tell, text)
    assert run.counted == []
    assert len(run.rejected) == 1
    assert run.rejected[0]["judge_instance"] is True
    assert run.judge_disagreements == 1


# --- structural decision rules -----------------------------------------------

SANDWICH_ROWS = [
    # (preview, recap, new_info, expected)
    ("p", "r", None, True),
    ("p", "r", "n", False),
    ("p", None, None, False),
    ("p", None, "n", False),
    (None, "r", None, False),
    (None, "r", "n", False),
    (None, None, None, False),
    (None, None, "n", False),
]


@pytest.mark.parametrize("preview,recap,new_info,expected", SANDWICH_ROWS)
def test_the_summary_sandwich_truth_table(
    preview: str | None, recap: str | None, new_info: str | None, expected: bool
) -> None:
    present, _ = protocol.decide_summary_sandwich(
        {
            "opening_preview_quote": preview,
            "closing_recap_quote": recap,
            "closing_new_info_quote": new_info,
        }
    )
    assert present is expected


def test_an_empty_string_quote_is_not_evidence() -> None:
    present, _ = protocol.decide_summary_sandwich(
        {"opening_preview_quote": "  ", "closing_recap_quote": "r", "closing_new_info_quote": None}
    )
    assert present is False


def test_the_parallel_bullet_rule() -> None:
    def entry(**overrides: Any) -> dict[str, Any]:
        base = {
            "heading": "Priorities",
            "item_count": 3,
            "item_openings": ["Improving intake", "Reducing manual", "Strengthening data"],
            "shared_opening_form": "gerund",
            "all_items_match": True,
            "single_word_items": False,
            "procedural_format": False,
        }
        base.update(overrides)
        return base

    assert protocol.decide_parallel_bullets({"lists": [entry()]})[0] is True
    assert protocol.decide_parallel_bullets({"lists": [entry(item_count=2)]})[0] is False
    assert protocol.decide_parallel_bullets({"lists": [entry(all_items_match=False)]})[0] is False
    assert protocol.decide_parallel_bullets({"lists": [entry(shared_opening_form=None)]})[0] is False
    assert protocol.decide_parallel_bullets({"lists": [entry(single_word_items=True)]})[0] is False
    assert protocol.decide_parallel_bullets({"lists": [entry(procedural_format=True)]})[0] is False
    assert protocol.decide_parallel_bullets({"lists": []})[0] is False
    # One qualifying list among several disqualified ones is still a hit.
    assert protocol.decide_parallel_bullets(
        {"lists": [entry(item_count=2), entry()]}
    )[0] is True


def test_the_table_overuse_rule() -> None:
    def entry(**overrides: Any) -> dict[str, Any]:
        base = {
            "header_row": "| Aspect | Description |",
            "sample_data_row": "| Cost | Under budget. |",
            "row_count": 2,
            "column_count": 2,
            "criterion": "a",
            "genuine_data_table": False,
            "crosswalk_or_schedule": False,
            "required_by_format": False,
        }
        base.update(overrides)
        return base

    for criterion in ("a", "b", "c"):
        assert protocol.decide_table_overuse({"tables": [entry(criterion=criterion)]})[0] is True
    assert protocol.decide_table_overuse({"tables": [entry(criterion=None)]})[0] is False
    assert protocol.decide_table_overuse({"tables": [entry(genuine_data_table=True)]})[0] is False
    assert protocol.decide_table_overuse({"tables": [entry(crosswalk_or_schedule=True)]})[0] is False
    assert protocol.decide_table_overuse({"tables": [entry(required_by_format=True)]})[0] is False
    assert protocol.decide_table_overuse({"tables": []})[0] is False


def test_structural_evidence_that_does_not_verify_is_pruned_before_the_decision(
    tmp_path: Path, sandwich_tell: Tell
) -> None:
    view = (
        "SKELETON m/doc-01\nformat: memo\nwords: 40\n\nOUTLINE\n"
        "PARA: 12w | This memo will cover cost and timeline.\n\n"
        "FIRST PARAGRAPH\nThis memo will cover cost and timeline.\n\n"
        "LAST PARAGRAPH\nIn summary, we covered cost and timeline.\n\nTABLES\n(none)"
    )

    def router(prompt: str) -> dict[str, Any]:
        return {
            "opening_preview_quote": "This memo will cover cost and timeline.",
            "closing_recap_quote": "In conclusion the board should act now.",  # not in the view
            "closing_new_info_quote": None,
        }

    backend = JudgeBackend(make_client(tmp_path, router))
    run = backend.structural_for_text(sandwich_tell, view)
    assert run.present is False, "a recap quote that is not in the document is not a recap"
    assert len(run.hallucinated) == 1
    assert "no closing recap" in run.reason


# --- cache -------------------------------------------------------------------


def test_a_cache_key_is_stable_and_covers_the_whole_recipe() -> None:
    base = dict(chunk_sha="abc", tell_id="rht.rhetorical-qa", rubric_version=1,
                judge_model=JUDGE_MODEL_DEFAULT, stage=EXTRACT)
    key = cache_key(**base)
    assert key == cache_key(**base)
    assert key != cache_key(**{**base, "chunk_sha": "abd"})
    assert key != cache_key(**{**base, "tell_id": "rht.rule-of-three"})
    assert key != cache_key(**{**base, "rubric_version": 2})
    assert key != cache_key(**{**base, "judge_model": "claude-opus-4-7"})
    assert key != cache_key(**{**base, "stage": STRUCTURAL})


def test_adjudication_keys_are_per_span() -> None:
    base = dict(chunk_sha="abc", tell_id="t", rubric_version=1,
                judge_model=JUDGE_MODEL_DEFAULT, stage=ADJUDICATE)
    assert cache_key(**base, quote="one") != cache_key(**base, quote="two")
    assert cache_key(**base, quote="one") == cache_key(**base, quote="one")
    with pytest.raises(ValueError, match="span quote"):
        cache_key(**base)


def test_the_cache_serves_the_second_call_and_records_its_key_fields(tmp_path: Path) -> None:
    calls: list[str] = []

    def router(prompt: str) -> dict[str, Any]:
        calls.append(prompt)
        return {"spans": []}

    client = make_client(tmp_path, router)
    payload, key, cached = client.ask(EXTRACT, "sha1", "t", 1, "prompt")
    assert (payload, cached) == ({"spans": []}, False)
    payload, key2, cached = client.ask(EXTRACT, "sha1", "t", 1, "prompt")
    assert cached is True and key2 == key
    assert len(calls) == 1

    envelope_on_disk = json.loads(client.cache.path_for(key).read_text(encoding="utf-8"))
    assert envelope_on_disk["tell_id"] == "t"
    assert envelope_on_disk["rubric_version"] == 1
    assert envelope_on_disk["judge_model"] == JUDGE_MODEL_DEFAULT
    assert envelope_on_disk["chunk_sha256"] == "sha1"
    assert envelope_on_disk["protocol_version"] == protocol.PROTOCOL_VERSION
    assert envelope_on_disk["payload"] == {"spans": []}
    assert client.cache.stats.hits == 1


def test_a_rubric_version_bump_invalidates_the_cached_answer(tmp_path: Path) -> None:
    answers = iter([{"spans": [{"quote": "old"}]}, {"spans": [{"quote": "new"}]}])
    client = make_client(tmp_path, lambda prompt: next(answers))
    first, _, _ = client.ask(EXTRACT, "sha1", "t", 1, "prompt")
    second, _, cached = client.ask(EXTRACT, "sha1", "t", 2, "prompt")
    assert first != second
    assert cached is False


def test_force_bypasses_the_cache(tmp_path: Path) -> None:
    calls: list[str] = []
    client = make_client(tmp_path, lambda p: (calls.append(p), {"spans": []})[1])
    client.ask(EXTRACT, "sha1", "t", 1, "prompt")
    client.ask(EXTRACT, "sha1", "t", 1, "prompt")
    assert len(calls) == 1

    forced = JudgeClient(transport=client.transport, cache=client.cache, force=True)
    forced.ask(EXTRACT, "sha1", "t", 1, "prompt")
    assert len(calls) == 2


def test_a_cache_only_client_refuses_to_call_the_judge(tmp_path: Path) -> None:
    client = make_client(tmp_path, lambda p: {"spans": []}, cache_only=True)
    with pytest.raises(CacheMiss, match="not cached"):
        client.ask(EXTRACT, "sha1", "t", 1, "prompt")

    warm = JudgeClient(transport=client.transport, cache=client.cache)
    warm.ask(EXTRACT, "sha1", "t", 1, "prompt")
    assert client.ask(EXTRACT, "sha1", "t", 1, "prompt")[2] is True


# --- end to end --------------------------------------------------------------

E2E_DOC = """\
# Consolidation Options

So why did the count change? The rule changed in November, and three schools
filed on the sixteenth.

## Detail

The board's last actionable meeting is April 20. Nothing between now and then
has slack in it.
"""


def passage_of(prompt: str) -> str:
    """The passage an extraction prompt is about, without the rubric or examples.

    Worth having: the rubric's own few-shot examples quote the pattern, so a
    router that matches on the whole prompt answers "found it" for a document
    that does not contain it — which is a fake judge hallucinating, not a test.
    """
    return prompt.split("<<<PASSAGE", 1)[1].split("PASSAGE>>>", 1)[0]


def e2e_router(prompt: str) -> dict[str, Any] | None:
    if "EXTRACTION ONLY" in prompt:
        if "So why did the count change?" in passage_of(prompt):
            return {
                "spans": [
                    {"quote": "So why did the count change?", "location_hint": "opening"},
                    {"quote": "The board's last actionable meeting is April 20.",
                     "location_hint": "detail"},
                ]
            }
        return {"spans": []}
    if "ADJUDICATE ONE SPAN" in prompt:
        if "So why did the count change?" in prompt.split("SPAN UNDER REVIEW")[1][:200]:
            return {"instance": True, "criteria_met": ["a", "b"],
                    "exclusion_triggered": None, "rationale": "answered in the next clause"}
        return {"instance": False, "criteria_met": [], "exclusion_triggered": None,
                "rationale": "not a question"}
    if "EXTRACT STRUCTURAL EVIDENCE" in prompt:
        # Nothing structural in the fixture documents; the empty answers still
        # exercise the verify-then-decide path for all three doc-level tells.
        if "summary-sandwich" in prompt:
            return {"opening_preview_quote": None, "closing_recap_quote": None,
                    "closing_new_info_quote": None}
        if "parallel-bullet-grammar" in prompt:
            return {"lists": []}
        return {"tables": []}
    return None


def test_a_judge_tell_measures_a_document_end_to_end(tmp_path: Path, qa_tell: Tell) -> None:
    doc = doc_from(E2E_DOC)
    backend = JudgeBackend(make_client(tmp_path, e2e_router))
    detection = backend(qa_tell, doc)

    assert detection.raw == 1.0
    assert detection.method == "judge"
    assert detection.unit == "count"
    assert detection.rate_per_1k == pytest.approx(1000.0 / doc.words, rel=1e-6)
    assert detection.matches[0]["quote"] == "So why did the count change?"
    assert detection.matches[0]["line"] == 3
    assert detection.detail["judge_model"] == JUDGE_MODEL_DEFAULT
    assert detection.detail["rubric_version"] == qa_tell.rubric_version
    assert detection.detail["protocol_version"] == protocol.PROTOCOL_VERSION
    assert detection.detail["hallucinated"] == 0
    assert detection.detail["adjudicated_true"] == 1
    assert detection.detail["adjudicated_false"] == 1
    assert detection.detail["cache_keys"]


def test_the_second_run_of_a_detection_is_all_cache(tmp_path: Path, qa_tell: Tell) -> None:
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    backend = JudgeBackend(client)
    first = backend(qa_tell, doc)
    calls_after_first = client.transport.stats.calls

    second = backend(qa_tell, doc)
    assert client.transport.stats.calls == calls_after_first, "a warm cache calls nobody"
    assert second.raw == first.raw
    assert second.matches == first.matches


def test_a_span_in_the_overlap_is_counted_once(tmp_path: Path, qa_tell: Tell) -> None:
    filler = " ".join(["alpha"] * 40)
    body = "\n".join(
        [f"{filler} line{i}." for i in range(30)]
        + ["So why did the count change? The rule changed."]
    )
    doc = doc_from(f"## Long\n\n{body}")
    chunks = protocol.chunk_doc(doc, target_words=500, overlap_words=200)
    assert len(chunks) > 1

    def router(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            if "So why did the count change?" in passage_of(prompt):
                return {"spans": [{"quote": "So why did the count change?", "location_hint": ""}]}
            return {"spans": []}
        return {"instance": True, "criteria_met": ["a", "b"], "exclusion_triggered": None,
                "rationale": "answered"}

    client = make_client(tmp_path, router)
    detection = JudgeBackend(client).detect(qa_tell, doc)
    assert detection.raw == 1.0, "the overlap must not double-count"


def test_a_skeleton_tell_produces_a_binary_detection(tmp_path: Path, sandwich_tell: Tell) -> None:
    doc = doc_from(
        "# Memo\n\nThis memo will cover cost and timeline.\n\n"
        "## Cost\n\nThe cost is $4.1 million a year.\n\n"
        "## Summary\n\nIn summary, we covered cost and timeline.\n"
    )

    def router(prompt: str) -> dict[str, Any]:
        return {
            "opening_preview_quote": "This memo will cover cost and timeline.",
            "closing_recap_quote": "In summary, we covered cost and timeline.",
            "closing_new_info_quote": None,
        }

    detection = JudgeBackend(make_client(tmp_path, router)).detect(sandwich_tell, doc)
    assert detection.raw == 1.0
    assert detection.unit == "binary"
    assert detection.rate_per_1k is None
    assert len(detection.matches) == 2
    assert detection.detail["view"] == "skeleton"


def test_detect_all_scores_judge_rows_when_a_backend_is_supplied(
    tmp_path: Path, registry: Registry
) -> None:
    from telltale import scoring

    doc = doc_from(E2E_DOC)
    tells = [t for t in registry.active_tells() if t.id in {"rht.rhetorical-qa", "pnc.arrow-chain"}]
    assert len(tells) == 2

    backend = JudgeBackend(make_client(tmp_path, e2e_router))
    df = scoring.detect_all([doc], tells, judge=backend)
    assert df.attrs["judge_tells_skipped"] == 0
    assert "judge" in set(df["method"])
    row = df[df["tell_id"] == "rht.rhetorical-qa"].iloc[0]
    assert row["raw"] == 1.0

    scored = scoring.normalize(df, tells)
    assert scored.loc[scored["tell_id"] == "rht.rhetorical-qa", "score"].iloc[0] == 1.0


def test_the_build_seam_takes_the_backend(tmp_path: Path, qa_tell: Tell) -> None:
    backend = JudgeBackend(make_client(tmp_path, e2e_router))
    detector = build(qa_tell, judge=backend)
    detection = detector.detect(doc_from(E2E_DOC))
    assert detection.tell_id == qa_tell.id


# --- prompts -----------------------------------------------------------------


def test_the_extraction_prompt_carries_the_rubric_and_asks_for_over_extraction(
    qa_tell: Tell,
) -> None:
    prompt = protocol.build_extraction_prompt(qa_tell, "a passage")
    assert qa_tell.rubric.strip() in prompt
    assert "OVER-EXTRACT" in prompt
    assert "a passage" in prompt
    for example in qa_tell.examples:
        assert protocol.normalize_ws(example) in prompt
    assert "score" not in prompt.split("PASSAGE")[0].lower().replace("do not rate, score", "")


def test_the_adjudication_prompt_names_the_rubrics_own_letters(qa_tell: Tell) -> None:
    prompt = protocol.build_adjudication_prompt(qa_tell, "the span", "the context")
    assert "(a), (b)" in prompt
    assert "(x), (y), (z)" in prompt
    assert "the span" in prompt and "the context" in prompt


def test_the_structural_prompt_has_a_schema_for_each_doc_level_tell(
    registry: Registry,
) -> None:
    for tell_id in protocol.STRUCTURAL_DECISIONS:
        tell = registry.get(tell_id)
        prompt = protocol.build_structural_prompt(tell, "the outline")
        assert "OUTPUT SCHEMA" in prompt
        assert "the outline" in prompt
        for field in protocol.RULES[tell_id].evidence_fields:
            assert field in prompt


def test_prompts_are_deterministic(qa_tell: Tell) -> None:
    assert protocol.build_extraction_prompt(qa_tell, "x") == protocol.build_extraction_prompt(
        qa_tell, "x"
    )


# --- calibration -------------------------------------------------------------


@pytest.mark.parametrize("tell_id", sorted(protocol.RULES))
def test_every_judge_tell_has_a_well_formed_calibration_set(
    tell_id: str, registry: Registry
) -> None:
    tell = registry.get(tell_id)
    snippets = calibration.load_snippets(tell_id)
    assert calibration.lint_snippets(tell, snippets) == []
    assert len(snippets) == 20
    assert any(s.source == "registry" for s in snippets), "anchor on the registry examples"


@pytest.mark.parametrize("tell_id", ["str.summary-sandwich", "str.parallel-bullet-grammar",
                                     "str.table-overuse"])
def test_structural_calibration_snippets_are_skeletons(tell_id: str) -> None:
    for snippet in calibration.load_snippets(tell_id):
        assert snippet.text.startswith("SKELETON ")
        assert "OUTLINE" in snippet.text
        assert "TABLES" in snippet.text


def test_calibration_scores_agreement_and_applies_the_gate(
    tmp_path: Path, qa_tell: Tell
) -> None:
    snippets = calibration.load_snippets(qa_tell.id)

    def perfect(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            passage = prompt.split("<<<PASSAGE", 1)[1]
            for line in passage.split("\n"):
                if "?" in line and "PASSAGE>>>" not in line:
                    return {"spans": [{"quote": line.strip(), "location_hint": ""}]}
            return {"spans": []}
        span = prompt.split("<<<SPAN", 1)[1].split("SPAN>>>", 1)[0]
        met = ["a", "b"] if "?" in span else []
        return {"instance": bool(met), "criteria_met": met, "exclusion_triggered": None,
                "rationale": "canned"}

    backend = JudgeBackend(make_client(tmp_path, perfect))
    report = calibration.calibrate(qa_tell, backend, snippets=snippets[:2])
    assert report.n == 2
    assert 0.0 <= report.agreement <= 1.0
    assert report.judge_model == JUDGE_MODEL_DEFAULT
    assert report.rubric_version == qa_tell.rubric_version


def test_a_report_below_the_gate_does_not_pass(tmp_path: Path, qa_tell: Tell) -> None:
    snippets = calibration.load_snippets(qa_tell.id)

    def never_finds_anything(prompt: str) -> dict[str, Any]:
        return {"spans": []} if "EXTRACTION ONLY" in prompt else {"instance": False,
                                                                  "criteria_met": [],
                                                                  "exclusion_triggered": None,
                                                                  "rationale": ""}

    backend = JudgeBackend(make_client(tmp_path, never_finds_anything))
    report = calibration.calibrate(qa_tell, backend, snippets=snippets)
    assert report.agreement == 0.5  # every negative right, every positive missed
    assert report.passed is False
    assert len(report.failures) == 10
    assert "FAIL" in report.summary()


def test_the_gate_refuses_an_uncalibrated_tell(tmp_path: Path, registry: Registry) -> None:
    tells = [t for t in registry.active_tells() if t.id in {"rht.rhetorical-qa", "pnc.arrow-chain"}]
    keep, skipped = calibration.gate_tells(tells, tmp_path, judge_model=JUDGE_MODEL_DEFAULT)
    assert [t.id for t in keep] == ["pnc.arrow-chain"]
    assert "rht.rhetorical-qa" in skipped
    assert "no calibration report" in skipped["rht.rhetorical-qa"]


def test_the_gate_admits_a_tell_whose_latest_report_clears_it(
    tmp_path: Path, registry: Registry, qa_tell: Tell
) -> None:
    report = calibration.CalibrationReport(
        tell_id=qa_tell.id, rubric_version=qa_tell.rubric_version,
        judge_model=JUDGE_MODEL_DEFAULT, protocol_version=protocol.PROTOCOL_VERSION,
        n=20, n_agree=19, agreement=0.95, passed=True, gate=calibration.GATE,
        timestamp="2026-07-29T00:00:00+00:00",
    )
    calibration.write_report(report, tmp_path)
    keep, skipped = calibration.gate_tells([qa_tell], tmp_path, judge_model=JUDGE_MODEL_DEFAULT)
    assert [t.id for t in keep] == [qa_tell.id]
    assert skipped == {}

    # A report against another judge does not admit this one.
    _, other = calibration.gate_tells([qa_tell], tmp_path, judge_model="claude-opus-4-8")
    assert qa_tell.id in other


def test_a_stale_rubric_version_is_not_calibration(
    tmp_path: Path, qa_tell: Tell
) -> None:
    report = calibration.CalibrationReport(
        tell_id=qa_tell.id, rubric_version=0, judge_model=JUDGE_MODEL_DEFAULT,
        protocol_version=protocol.PROTOCOL_VERSION, n=20, n_agree=20, agreement=1.0,
        passed=True, gate=calibration.GATE, timestamp="2026-07-29T00:00:00+00:00",
    )
    calibration.write_report(report, tmp_path)
    _, skipped = calibration.gate_tells([qa_tell], tmp_path, judge_model=JUDGE_MODEL_DEFAULT)
    assert "rubric v0" in skipped[qa_tell.id]


# --- audit -------------------------------------------------------------------


def test_the_audit_compares_span_sets_without_touching_the_cache(
    tmp_path: Path, qa_tell: Tell
) -> None:
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)
    entries_before = len(client.cache.entries())

    # The live re-ask drops one of the two spans.
    def drifted(prompt: str) -> dict[str, Any] | None:
        if "EXTRACTION ONLY" in prompt and "So why did the count change?" in passage_of(prompt):
            return {"spans": [{"quote": "So why did the count change?", "location_hint": ""}]}
        return e2e_router(prompt)

    client.transport.router = drifted
    report = audit_mod.audit([doc], [qa_tell], client, pct=100.0)
    assert report.n_available >= 1
    assert report.n_sampled == report.n_available
    assert 0.0 <= report.mean_agreement <= 1.0
    assert len(client.cache.entries()) == entries_before, "an audit must not rewrite the cache"


def test_an_audit_with_nothing_cached_says_so(tmp_path: Path, qa_tell: Tell) -> None:
    client = make_client(tmp_path, e2e_router)
    report = audit_mod.audit([doc_from(E2E_DOC)], [qa_tell], client, pct=100.0)
    assert report.n_available == 0
    assert report.n_sampled == 0
    assert "nothing to re-ask" in report.summary()


# --- scoring integration -----------------------------------------------------


@pytest.fixture
def judged_corpus(tmp_path: Path) -> Path:
    """A two-document corpus, on disk, in the layout load_corpus expects."""
    root = tmp_path / "corpus" / "claude-opus-5"
    root.mkdir(parents=True)
    (root / "memo-01.md").write_text(E2E_DOC, encoding="utf-8")
    (root / "memo-02.md").write_text(
        "# Second\n\nNothing rhetorical happens in this one at all.\n", encoding="utf-8"
    )
    return tmp_path / "corpus"


def _install_fake_judge(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[JudgeClient]:
    """Point score_run's judge at a canned transport and a scratch cache."""
    import telltale.judge as judge_pkg
    import telltale.judge.transport as transport_mod

    built: list[JudgeClient] = []

    def build_backend(model=None, cache_root=None, force=False, cache_only=False, **_):
        client = JudgeClient(
            transport=FakeJudge(e2e_router, model=model or JUDGE_MODEL_DEFAULT),
            cache=JudgeCache(tmp_path / "cache"),
            force=force,
            cache_only=cache_only,
        )
        built.append(client)
        return JudgeBackend(client)

    monkeypatch.setattr(judge_pkg, "build_backend", build_backend)
    monkeypatch.setattr(transport_mod, "resolve_judge", lambda *a, **k: JUDGE_MODEL_DEFAULT)
    return built


def _calibrate_all(runs_root: Path, registry: Registry, agreement: float = 0.95) -> None:
    for tell in registry.active_tells():
        if tell.method != "judge":
            continue
        calibration.write_report(
            calibration.CalibrationReport(
                tell_id=tell.id,
                rubric_version=tell.rubric_version,
                judge_model=JUDGE_MODEL_DEFAULT,
                protocol_version=protocol.PROTOCOL_VERSION,
                n=20,
                n_agree=int(round(20 * agreement)),
                agreement=agreement,
                passed=agreement >= calibration.GATE,
                gate=calibration.GATE,
                timestamp="2026-07-29T00:00:00+00:00",
            ),
            runs_root,
        )


def test_score_with_judge_writes_judge_rows_and_a_manifest_section(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    from telltale import report as report_mod

    _install_fake_judge(monkeypatch, tmp_path)
    runs = tmp_path / "runs"
    _calibrate_all(runs, registry)

    run_dir = report_mod.score_run(
        corpus_root=judged_corpus,
        registry_path=REGISTRY_PATH,
        out_root=runs,
        bootstrap_n=20,
        judge=True,
        judge_model=JUDGE_MODEL_DEFAULT,
        runs_root=runs,
    )
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    judge = manifest["judge"]
    assert judge["enabled"] is True
    assert judge["model"] == JUDGE_MODEL_DEFAULT
    assert judge["protocol_version"] == protocol.PROTOCOL_VERSION
    assert judge["tells_skipped"] == {}
    assert len(judge["tells_scored"]) == len(protocol.RULES)
    assert judge["cache"]["misses"] >= 1
    assert judge["hallucination"]["rate"] == 0.0
    assert judge["calibration"]["rht.rhetorical-qa"]["agreement"] == 0.95

    rows = [json.loads(line) for line in (run_dir / "scores.jsonl").read_text().splitlines()]
    judged = [r for r in rows if r["method"] == "judge"]
    assert {r["tell_id"] for r in judged} == set(protocol.RULES)
    hit = [r for r in judged if r["tell_id"] == "rht.rhetorical-qa" and r["raw"] == 1.0]
    assert hit and hit[0]["matches"][0]["quote"] == "So why did the count change?"

    card = (run_dir / "scorecard.md").read_text(encoding="utf-8")
    assert f"| Judge model | `{JUDGE_MODEL_DEFAULT}` |" in card
    assert "Hallucinated quotes" in card
    assert "The judge never rated anything" in card


def test_an_uncalibrated_judge_tell_is_skipped_loudly(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    from telltale import report as report_mod

    _install_fake_judge(monkeypatch, tmp_path)
    runs = tmp_path / "runs"
    _calibrate_all(runs, registry)
    # Re-calibrate one tell below the gate; the later report wins.
    calibration.write_report(
        calibration.CalibrationReport(
            tell_id="rht.rule-of-three", rubric_version=1, judge_model=JUDGE_MODEL_DEFAULT,
            protocol_version=protocol.PROTOCOL_VERSION, n=20, n_agree=14, agreement=0.70,
            passed=False, gate=calibration.GATE, timestamp="2026-07-30T00:00:00+00:00",
        ),
        runs,
    )

    with pytest.warns(UserWarning, match="want of calibration"):
        run_dir = report_mod.score_run(
            corpus_root=judged_corpus,
            registry_path=REGISTRY_PATH,
            out_root=runs,
            bootstrap_n=20,
            judge=True,
            judge_model=JUDGE_MODEL_DEFAULT,
            runs_root=runs,
        )

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    skipped = manifest["judge"]["tells_skipped"]
    assert "rht.rule-of-three" in skipped
    assert "0.70" in skipped["rht.rule-of-three"]
    assert "rht.rule-of-three" not in manifest["judge"]["tells_scored"]

    rows = [json.loads(line) for line in (run_dir / "scores.jsonl").read_text().splitlines()]
    assert not any(r["tell_id"] == "rht.rule-of-three" for r in rows)
    assert "`rht.rule-of-three` (calibration 0.70" in (run_dir / "scorecard.md").read_text()


def test_a_judge_run_verifies_off_its_cache_without_calling_the_model(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    from telltale import manifest as manifest_mod
    from telltale import report as report_mod

    built = _install_fake_judge(monkeypatch, tmp_path)
    runs = tmp_path / "runs"
    _calibrate_all(runs, registry)

    run_dir = report_mod.score_run(
        corpus_root=judged_corpus,
        registry_path=REGISTRY_PATH,
        out_root=runs,
        bootstrap_n=20,
        judge=True,
        judge_model=JUDGE_MODEL_DEFAULT,
        runs_root=runs,
    )
    calls_after_scoring = sum(c.transport.stats.calls for c in built)

    result = manifest_mod.verify(run_dir)
    assert result.ok, result.summary()
    assert sum(c.transport.stats.calls for c in built) == calls_after_scoring

    # With the cache gone there is nothing to replay, and verify has to say so
    # rather than quietly re-asking a model and calling the answer identical.
    import shutil

    shutil.rmtree(tmp_path / "cache")
    with pytest.raises(CacheMiss):
        manifest_mod.verify(run_dir)
