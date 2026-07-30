"""Tests for the Tier-2 judge stack.

No test in this file calls a model. Every judge answer is canned, which is the
only way to test the part that matters: what the code does with an answer once
it has one. The live checks are run by hand and their transcripts live in
runs/calibration/.
"""

from __future__ import annotations

import json
import re
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


def test_the_skeleton_labels_the_paragraph_it_prints_twice() -> None:
    """Protocol v2. Without the labels a document that simply ends reads as a recap.

    Also the guard on the string coupling between this module and textstats: if
    `doc_skeleton` ever stops emitting `PARA:` lines or the `LAST PARAGRAPH`
    header, the labels silently stop being applied and this fails loudly.
    """
    doc = doc_from(
        "# Paper\n\nThis paper takes up two questions.\n\n"
        "## What it requires\n\nThe policy requires a call on day one.\n\n"
        "## What it achieves\n\nNeither step has a measurable association.\n"
    )
    view = protocol.skeleton_view(doc)
    outline = view.split("FIRST PARAGRAPH")[0]

    labelled = [ln for ln in outline.splitlines() if protocol.CLOSING_PARA_NOTE in ln]
    assert len(labelled) == 1, "exactly the last PARA line carries the note"
    assert "Neither step has a measurable association." in labelled[0]
    assert protocol.LAST_PARAGRAPH_HEADER + protocol.LAST_PARAGRAPH_NOTE in view
    assert "not a second occurrence" in view
    assert protocol.skeleton_view(doc) == view  # still deterministic


def test_a_document_with_no_paragraphs_is_labelled_without_crashing() -> None:
    view = protocol.skeleton_view(doc_from("# Heading only\n\n## And another\n"))
    assert protocol.CLOSING_PARA_NOTE not in view
    assert protocol.LAST_PARAGRAPH_HEADER in view


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


@pytest.mark.parametrize("separate,expected", [(True, True), (False, False)])
def test_a_recap_must_sit_in_its_own_section(separate: bool, expected: bool) -> None:
    """Rubric v2: a document that ends on its last finding is not a sandwich."""
    present, why = protocol.decide_summary_sandwich(
        {
            "opening_preview_quote": "This paper takes up two questions.",
            "closing_recap_quote": "Neither step has a measurable association.",
            "closing_recap_is_separate_section": separate,
            "closing_new_info_quote": None,
        }
    )
    assert present is expected
    if not expected:
        assert "last substantive section" in why


def test_an_answer_without_the_separateness_field_still_decides() -> None:
    """Older cached answers predate the field; absence must not mean 'not separate'.

    A missing key is no evidence either way, and treating it as False would
    silently reinterpret every v1 answer as a negative rather than leaving it to
    the rubric_version bump to invalidate them honestly.
    """
    present, _ = protocol.decide_summary_sandwich(
        {
            "opening_preview_quote": "p",
            "closing_recap_quote": "r",
            "closing_new_info_quote": None,
        }
    )
    assert present is True


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


def test_the_extraction_prompt_carries_the_inclusion_criteria_only(
    qa_tell: Tell,
) -> None:
    """Protocol v2: stage 1 must not be able to apply exclusions it cannot see."""
    inclusion, exclusions, evidence = protocol.split_rubric(qa_tell.rubric)
    prompt = protocol.build_extraction_prompt(qa_tell, "a passage")

    assert inclusion.strip() in prompt
    assert evidence.strip() in prompt
    assert "EXCLUSIONS:" not in prompt
    assert exclusions.strip() not in prompt
    # Every labelled exclusion clause, by its own distinctive opening.
    for line in exclusions.splitlines():
        if re.match(r"^\([xyzw]\)", line):
            assert line.strip() not in prompt, f"exclusion leaked into stage 1: {line!r}"

    assert "You must NOT apply\nexclusions" in prompt
    assert "OVER-EXTRACT" in prompt
    assert "a passage" in prompt
    for example in qa_tell.examples:
        assert protocol.normalize_ws(example) in prompt


@pytest.mark.parametrize("tell_id", sorted(protocol.RULES))
def test_no_rubric_exclusion_ever_reaches_stage_one(
    tell_id: str, registry: Registry
) -> None:
    tell = registry.get(tell_id)
    if protocol.rule_for(tell).kind == "structural":
        pytest.skip("doc-level tells ask once; their exclusions are the evidence")
    prompt = protocol.build_extraction_prompt(tell, "passage")
    _, exclusions, _ = protocol.split_rubric(tell.rubric)
    assert exclusions.strip()
    assert "EXCLUSIONS" not in prompt


def test_split_rubric_cuts_every_registry_rubric_cleanly(registry: Registry) -> None:
    for tell in registry.active_tells():
        if tell.method != "judge":
            continue
        inclusion, exclusions, evidence = protocol.split_rubric(tell.rubric)
        assert inclusion.strip() and exclusions.strip() and evidence.strip(), tell.id
        assert inclusion + exclusions + evidence == tell.rubric, tell.id
        assert not any(
            line.startswith(("(x)", "(y)", "(z)", "(w)"))
            for line in inclusion.splitlines()
        ), tell.id


def test_a_rubric_without_exclusions_degrades_rather_than_losing_text() -> None:
    inclusion, exclusions, evidence = protocol.split_rubric("A span exhibits X when...")
    assert inclusion == "A span exhibits X when..."
    assert (exclusions, evidence) == ("", "")


def test_the_structural_prompt_keeps_its_exclusions(registry: Registry) -> None:
    """The carve-out: exclusion facts ARE the evidence fields the code decides on."""
    for tell_id in protocol.STRUCTURAL_DECISIONS:
        tell = registry.get(tell_id)
        prompt = protocol.build_structural_prompt(tell, "outline")
        assert "EXCLUSIONS:" in prompt, tell_id
        assert tell.rubric.strip() in prompt, tell_id


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


@pytest.mark.parametrize("tell_id", ["str.summary-sandwich", "str.parallel-bullet-grammar",
                                     "str.table-overuse"])
def test_structural_snippets_match_what_production_renders(tell_id: str) -> None:
    """Calibration must test the representation the corpus is actually judged in.

    These snippets are hand-written rather than rendered from a Doc, so nothing
    but this test keeps them in the shape `skeleton_view` produces. They drifted
    once already: the closing-paragraph labels shipped in protocol v2 and the
    snippets did not carry them, so a whole calibration round scored a fix that
    was never in the text it was scoring.
    """
    for snippet in calibration.load_snippets(tell_id):
        assert protocol.LAST_PARAGRAPH_NOTE in snippet.text, snippet.id
        assert snippet.text.count(protocol.CLOSING_PARA_NOTE) == 1, snippet.id
        assert protocol._label_closing_paragraph(snippet.text) == snippet.text, (
            f"{snippet.id} is not what skeleton_view would render"
        )


@pytest.mark.parametrize("tell_id", ["str.summary-sandwich", "str.parallel-bullet-grammar",
                                     "str.table-overuse"])
def test_structural_snippet_outlines_agree_with_their_trailers(tell_id: str) -> None:
    """The outline must describe the same document the trailer prints.

    Splicing labels onto a malformed outline satisfies the label check and not
    the parity claim. `str.table-overuse` shipped that way: nineteen snippets
    claimed one paragraph in the outline while printing two different ones as
    FIRST and LAST, which `doc_skeleton` cannot produce. A second, subtler case
    hid in `str.parallel-bullet-grammar`, where a PARA line asserted a sentence
    boundary the paragraph did not contain.
    """
    for snippet in calibration.load_snippets(tell_id):
        assert calibration.skeleton_parity_errors(snippet.text) == [], snippet.id


def test_the_parity_check_catches_a_malformed_outline() -> None:
    good = protocol.skeleton_view(
        doc_from("# T\n\nOpening sentence here.\n\n## S\n\nClosing sentence here.\n")
    )
    assert calibration.skeleton_parity_errors(good) == []

    # One PARA line, two different paragraphs printed: the shape that shipped.
    collapsed = "\n".join(
        line for line in good.split("\n")
        if not (line.startswith("PARA:") and protocol.CLOSING_PARA_NOTE not in line)
    )
    problems = calibration.skeleton_parity_errors(collapsed)
    assert any("does not open the FIRST PARAGRAPH" in p for p in problems)

    # A PARA line asserting a sentence break the paragraph does not have.
    truncated = good.replace("Opening sentence here.", "Opening sentence.", 1)
    assert any(
        "does not open the FIRST PARAGRAPH" in p
        for p in calibration.skeleton_parity_errors(truncated)
    )


def test_the_parity_check_catches_a_misplaced_closing_label() -> None:
    good = protocol.skeleton_view(
        doc_from("# T\n\nOpening sentence here.\n\n## S\n\nClosing sentence here.\n")
    )
    moved = good.replace(protocol.CLOSING_PARA_NOTE, "", 1)
    lines = moved.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("PARA:"):
            lines[i] += protocol.CLOSING_PARA_NOTE
            break
    problems = calibration.skeleton_parity_errors("\n".join(lines))
    assert any("closing label sits on PARA line(s)" in p for p in problems)


def test_the_closing_paragraph_labeller_is_idempotent() -> None:
    """Applied twice it must not double-label; the snippets are stored labelled."""
    once = protocol.skeleton_view(doc_from("# T\n\nOpening.\n\n## S\n\nClosing line.\n"))
    assert protocol._label_closing_paragraph(once) == once
    assert once.count(protocol.CLOSING_PARA_NOTE) == 1
    assert once.count(protocol.LAST_PARAGRAPH_NOTE) == 1


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


# --- judge/code disagreement rollup ------------------------------------------


def _judge_frame(rows: list[tuple[str, int, int]]):
    """A minimal detection frame: (tell_id, disagreements, adjudicated_true)."""
    import pandas as pd

    return pd.DataFrame(
        [
            {
                "tell_id": tell_id,
                "method": "judge",
                "detail": {"judge_disagreements": d, "adjudicated_true": t},
            }
            for tell_id, d, t in rows
        ]
    )


def test_disagreements_roll_up_across_documents_and_tells() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(
        _judge_frame([("a", 1, 10), ("a", 2, 10), ("b", 0, 5)])
    )
    assert roll["total"] == 3
    assert roll["counted"] == 25
    assert roll["rate"] == pytest.approx(3 / 25)
    assert roll["per_tell"]["a"] == {"disagreements": 3, "counted": 20, "rate": pytest.approx(0.15)}
    assert roll["per_tell"]["b"]["rate"] == 0.0
    assert roll["over_threshold"] == []


def test_a_tell_over_the_threshold_is_named() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(
        _judge_frame([("noisy", 3, 10), ("quiet", 1, 10)])
    )
    assert roll["per_tell"]["noisy"]["rate"] == pytest.approx(0.30)
    assert roll["over_threshold"] == ["noisy"]
    assert roll["threshold"] == report_mod.DISAGREEMENT_WARN_RATE


def test_the_threshold_is_strict_not_inclusive() -> None:
    from telltale import report as report_mod

    exactly = report_mod.judge_disagreements(_judge_frame([("t", 2, 10)]))
    assert exactly["per_tell"]["t"]["rate"] == pytest.approx(0.20)
    assert exactly["over_threshold"] == [], "at the threshold is not over it"
    assert report_mod.judge_disagreements(_judge_frame([("t", 3, 10)]))["over_threshold"] == ["t"]


def test_a_tell_that_counted_nothing_has_no_disagreement_rate() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("t", 0, 0)]))
    assert roll["per_tell"]["t"]["rate"] is None
    assert roll["rate"] is None
    assert roll["over_threshold"] == []


def test_disagreements_with_nothing_counted_are_still_flagged() -> None:
    """The pathological case: criteria that never close while the judge says yes.

    The rate is undefined because the denominator is zero, and reporting that as
    "no warning" would hide the most suspect rubric of all behind a division it
    could not perform.
    """
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("stuck", 4, 0)]))
    assert roll["per_tell"]["stuck"]["rate"] is None
    assert roll["per_tell"]["stuck"]["disagreements"] == 4
    assert roll["over_threshold"] == ["stuck"]


def test_the_cli_explains_an_undefined_disagreement_rate(capsys) -> None:
    from telltale.cli import _warn_on_disagreement

    _warn_on_disagreement(
        {
            "disagreements": {
                "over_threshold": ["stuck"],
                "threshold": 0.2,
                "per_tell": {"stuck": {"disagreements": 4, "counted": 0, "rate": None}},
            }
        }
    )
    err = capsys.readouterr().err
    assert "nothing counted at all — the criteria never close" in err


def test_an_empty_frame_rolls_up_to_nothing() -> None:
    import pandas as pd

    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(pd.DataFrame())
    assert roll["total"] == 0 and roll["rate"] is None and roll["per_tell"] == {}


def test_the_cli_warns_only_when_a_tell_is_over_the_threshold(capsys) -> None:
    from telltale.cli import _warn_on_disagreement

    _warn_on_disagreement({"disagreements": {"over_threshold": [], "per_tell": {}}})
    assert capsys.readouterr().err == ""

    _warn_on_disagreement(
        {
            "disagreements": {
                "over_threshold": ["rht.rule-of-three"],
                "threshold": 0.2,
                "per_tell": {"rht.rule-of-three": {"disagreements": 9, "counted": 20, "rate": 0.45}},
            }
        }
    )
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert "rht.rule-of-three: 9 of 20 counted spans (45%)" in err
    assert "needs an exclusion it does not have yet" in err


# --- sweep progress and error resilience -------------------------------------


def test_detect_all_reports_judge_progress_per_tell(tmp_path: Path, registry: Registry) -> None:
    from telltale import scoring

    docs = [doc_from(E2E_DOC, doc_id=f"m/doc-{i:02d}") for i in range(3)]
    tells = [registry.get("rht.rhetorical-qa"), registry.get("pnc.arrow-chain")]
    lines: list[str] = []
    scoring.detect_all(
        docs, tells, judge=JudgeBackend(make_client(tmp_path, e2e_router)), progress=lines.append
    )
    assert lines == [
        "JUDGE rht.rhetorical-qa 1/3 docs",
        "JUDGE rht.rhetorical-qa 2/3 docs",
        "JUDGE rht.rhetorical-qa 3/3 docs",
    ], "one line per judge measurement, deterministic tells stay quiet"


def test_a_failing_judge_call_does_not_take_the_sweep_down(
    tmp_path: Path, registry: Registry
) -> None:
    """One bad call must not cost the other 3,000, but it must not be silent."""
    from telltale import scoring

    def flaky(prompt: str):
        # Keyed on the passage, not a call counter: identical documents share a
        # chunk hash and therefore a cache entry, so a counter would fire on
        # whichever call happened to miss.
        if "EXTRACTION ONLY" in prompt and "doomed" in passage_of(prompt):
            raise JudgeError("judge call failed (exit 124): timed out")
        return e2e_router(prompt)

    docs = [
        doc_from(E2E_DOC.replace("Consolidation", f"Consolidation {i}"), doc_id=f"m/doc-{i:02d}")
        for i in range(3)
    ]
    docs[1] = doc_from(E2E_DOC.replace("Consolidation Options", "doomed"), doc_id="m/doc-01")
    tells = [registry.get("rht.rhetorical-qa")]
    lines: list[str] = []
    df = scoring.detect_all(
        docs, tells, judge=JudgeBackend(make_client(tmp_path, flaky)), progress=lines.append
    )

    assert len(df) == 2, "the failed document has no row at all, not a zero row"
    assert set(df["doc_id"]) == {"m/doc-00", "m/doc-02"}
    errors = df.attrs["judge_errors"]
    assert len(errors) == 1
    assert errors[0]["doc_id"] == "m/doc-01"
    assert "timed out" in errors[0]["error"]
    assert any("ERROR[other] rht.rhetorical-qa m/doc-01" in line for line in lines)


# --- sweep concurrency --------------------------------------------------------


def test_failure_classification() -> None:
    from telltale.judge import sweep

    assert sweep.classify_failure("HTTP 429 Too Many Requests") == sweep.THROTTLE
    assert sweep.classify_failure("rate limit exceeded") == sweep.THROTTLE
    assert sweep.classify_failure("Error 529: Overloaded") == sweep.OVERLOAD
    assert sweep.classify_failure("Not logged in - Please run /login") == sweep.AUTH
    assert sweep.classify_failure("401 unauthorized") == sweep.AUTH
    assert sweep.classify_failure("timed out after 300s") == sweep.OTHER
    # Auth wins when a message carries both, because a dead token makes every
    # other diagnosis moot.
    assert sweep.classify_failure("429 after oauth refresh failed") == sweep.AUTH


def test_the_gate_limits_concurrency_and_can_shrink() -> None:
    from telltale.judge.sweep import Gate

    gate = Gate(capacity=2, ceiling=4)
    gate.acquire()
    gate.acquire()
    assert gate.in_flight == 2
    assert gate.set_capacity(9) == 4, "capacity never exceeds the ceiling"
    assert gate.set_capacity(0) == 1, "capacity never drops below one"
    gate.release()
    gate.release()
    assert gate.in_flight == 0


def test_the_gate_blocks_a_worker_over_capacity() -> None:
    import threading

    from telltale.judge.sweep import Gate

    gate = Gate(capacity=1, ceiling=4)
    gate.acquire()
    entered = threading.Event()

    def second() -> None:
        gate.acquire()
        entered.set()

    thread = threading.Thread(target=second, daemon=True)
    thread.start()
    assert not entered.wait(0.2), "the second worker must wait"
    gate.release()
    assert entered.wait(2.0), "and proceed once a permit frees"
    thread.join(2.0)


def test_a_429_halves_the_workers_immediately() -> None:
    from telltale.judge.sweep import SweepController, SweepPolicy

    lines: list[str] = []
    controller = SweepController(
        policy=SweepPolicy(workers=6, ceiling=6), total=10, emit=lines.append
    )
    assert controller.gate.capacity == 6
    controller.record_failure("HTTP 429 rate limited")
    assert controller.gate.capacity == 3
    assert any(line.startswith("THROTTLE 3") for line in lines)
    controller.record_failure("429 again")
    assert controller.gate.capacity == 1
    assert not controller.should_stop


def test_overloads_halve_only_once_they_are_a_trend() -> None:
    from telltale.judge.sweep import SweepController, SweepPolicy

    controller = SweepController(
        policy=SweepPolicy(workers=6, ceiling=6, overload_rate=0.02, min_overloads=3),
        total=10,
    )
    for _ in range(200):
        controller.record_ok()
    controller.record_failure("529 overloaded")
    controller.record_failure("529 overloaded")
    assert controller.gate.capacity == 6, "two overloads in 200 calls is not a trend"
    controller.record_failure("529 overloaded")
    controller.record_failure("529 overloaded")
    controller.record_failure("529 overloaded")
    assert controller.gate.capacity == 3


def test_an_auth_failure_stops_the_sweep() -> None:
    from telltale.judge.sweep import SweepController

    lines: list[str] = []
    controller = SweepController(total=10, emit=lines.append)
    controller.record_failure("Not logged in - Please run /login")
    assert controller.should_stop
    assert controller.stop_reason == "auth"
    assert any(line.startswith("AUTH-LOST") for line in lines)
    assert controller.gate.capacity > 0, "stopping is not throttling"


def test_workers_step_back_up_after_a_quiet_stretch() -> None:
    from telltale.judge.sweep import SweepController, SweepPolicy

    now = [1000.0]
    lines: list[str] = []
    controller = SweepController(
        policy=SweepPolicy(workers=6, ceiling=6, step_up_after_s=1800),
        total=10,
        emit=lines.append,
        clock=lambda: now[0],
    )
    controller.record_failure("429")
    assert controller.gate.capacity == 3

    now[0] += 600
    controller.maybe_step_up()
    assert controller.gate.capacity == 3, "ten minutes is not a quiet stretch"

    now[0] += 1300
    controller.maybe_step_up()
    assert controller.gate.capacity == 4, "one worker at a time, not straight back"
    assert any(line.startswith("WORKERS 4") for line in lines)


def test_the_progress_line_reports_rate_and_eta() -> None:
    from telltale.judge.sweep import SweepController, SweepPolicy

    now = [0.0]
    lines: list[str] = []
    controller = SweepController(
        policy=SweepPolicy(progress_every_s=600),
        total=100,
        emit=lines.append,
        clock=lambda: now[0],
    )
    for _ in range(60):
        controller.record_call()
    now[0] = 600.0
    for _ in range(10):
        controller._done += 1
    controller.tick()
    assert len(lines) == 1
    assert "SWEEP 10/100 measurements, 60 calls, 6.0 calls/min" in lines[0]
    assert "ETA 1.5h" in lines[0]


def test_two_workers_actually_run_concurrently(tmp_path: Path, registry: Registry) -> None:
    """Wall-clock proof, not a proxy: 2 workers must beat 1 on slow calls.

    Every other concurrency test here would pass just as happily against a pool
    that serialized everything, which is exactly the failure this is guarding
    against — the first live sweep looked concurrent by every metric except the
    one that mattered.
    """
    import time

    from telltale import scoring
    from telltale.judge.sweep import SweepController, SweepPolicy

    latency = 0.25

    def slow(prompt: str):
        time.sleep(latency)
        return e2e_router(prompt)

    docs = [
        doc_from(E2E_DOC.replace("Consolidation", f"Consolidation {i}"), doc_id=f"m/doc-{i:02d}")
        for i in range(4)
    ]
    tells = [registry.get("rht.rhetorical-qa")]

    timings = {}
    for workers in (1, 2):
        client = make_client(tmp_path / f"w{workers}", slow)
        controller = SweepController(
            policy=SweepPolicy(workers=workers, ceiling=workers), total=len(docs)
        )
        started = time.monotonic()
        scoring.detect_all(
            docs, tells, judge=JudgeBackend(client), workers=workers, controller=controller
        )
        timings[workers] = time.monotonic() - started

    assert timings[2] < timings[1] * 0.75, (
        f"2 workers took {timings[2]:.2f}s against {timings[1]:.2f}s for 1 — "
        "the pool is not running work in parallel"
    )


def test_the_controller_counts_live_calls(tmp_path: Path, registry: Registry) -> None:
    """The counter the first sweep reported as zero for half an hour."""
    from telltale import scoring
    from telltale.judge.sweep import SweepController

    client = make_client(tmp_path, e2e_router)
    controller = SweepController(total=1)
    client.on_call = controller.record_call

    scoring.detect_all(
        [doc_from(E2E_DOC)], [registry.get("rht.rhetorical-qa")],
        judge=JudgeBackend(client), workers=1, controller=controller,
    )
    assert client.stats["live_calls"] > 0
    assert controller._calls == client.stats["live_calls"]

    lines: list[str] = []
    controller.emit = lines.append
    controller.tick(force=True)
    assert f"{controller._calls} calls" in lines[0]
    assert "0 calls" not in lines[0]


def test_two_workers_produce_byte_identical_scores(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The whole point of the concurrency: same evidence, same file, any width.

    Row order in the frame is sorted before it becomes a DataFrame, so the
    number of workers cannot reach the output. This is the test that says so.
    """
    from telltale import report as report_mod

    outputs = {}
    for workers in (1, 2):
        scratch = tmp_path / f"w{workers}"
        _install_fake_judge(monkeypatch, scratch)
        runs = scratch / "runs"
        _calibrate_all(runs, registry)
        run_dir = report_mod.score_run(
            corpus_root=judged_corpus,
            registry_path=REGISTRY_PATH,
            out_root=runs,
            bootstrap_n=20,
            judge=True,
            judge_model=JUDGE_MODEL_DEFAULT,
            runs_root=runs,
            judge_workers=workers,
            judge_ceiling=4,
        )
        outputs[workers] = {
            name: (run_dir / name).read_text(encoding="utf-8")
            for name in ("scores.jsonl", "matrix.csv", "matrix_by_format.csv", "scorecard.md")
        }

    for name in outputs[1]:
        assert outputs[1][name] == outputs[2][name], f"{name} differs between 1 and 2 workers"


# --- stratified sampling ------------------------------------------------------


def _corpus(models=("m1", "m2"), formats=("memo", "email", "report"), per_cell=6):
    return [
        Doc.from_text(doc_id=f"{m}/{f}-{i:02d}", model=m, fmt=f, text="# T\n\nBody text here.\n")
        for m in models
        for f in formats
        for i in range(per_cell)
    ]


def test_the_sample_is_balanced_across_models_and_formats() -> None:
    from telltale.judge import sampling

    docs = _corpus()
    sample = sampling.stratified_sample(docs, size=12, seed=7)
    assert len(sample.doc_ids) == 12
    assert sample.per_model == {"m1": 6, "m2": 6}
    assert sample.per_format == {"memo": 4, "email": 4, "report": 4}


def test_the_sample_is_deterministic_and_seed_sensitive() -> None:
    from telltale.judge import sampling

    docs = _corpus()
    first = sampling.stratified_sample(docs, size=12, seed=7)
    assert first.doc_ids == sampling.stratified_sample(docs, size=12, seed=7).doc_ids
    assert first.doc_ids == sampling.stratified_sample(list(reversed(docs)), 12, 7).doc_ids
    assert first.doc_ids != sampling.stratified_sample(docs, size=12, seed=8).doc_ids


def test_the_remainder_goes_to_the_deepest_pools() -> None:
    """13 per model over 3 formats is 4 each plus one; it must be reproducible."""
    from telltale.judge import sampling

    docs = [
        Doc.from_text(doc_id=f"m1/{f}-{i:02d}", model="m1", fmt=f, text="# T\n\nBody.\n")
        for f, n in (("memo", 10), ("email", 3), ("report", 5))
        for i in range(n)
    ]
    sample = sampling.stratified_sample(docs, size=10, seed=7)
    assert len(sample.doc_ids) == 10
    # base is 3 per format; email only has 3, so the extra must come from memo
    # (deepest) rather than from the stratum that is already exhausted.
    assert sample.per_format["email"] == 3
    assert sample.per_format["memo"] >= 4


def test_a_thin_stratum_does_not_break_the_draw() -> None:
    from telltale.judge import sampling

    docs = [Doc.from_text(doc_id="m1/memo-01", model="m1", fmt="memo", text="# T\n\nBody.\n")]
    sample = sampling.stratified_sample(docs, size=60, seed=7)
    assert sample.doc_ids == ("m1/memo-01",)


def test_an_explicit_document_list_is_honoured_and_reports_unknown_ids() -> None:
    from telltale.judge import sampling

    docs = _corpus()
    sample = sampling.sample_from_list(docs, ["m1/memo-00", "m2/email-01", "nope/x-99"])
    assert sample.doc_ids == ("m1/memo-00", "m2/email-01")
    assert "not in this corpus" in sample.note


def test_only_judge_tells_respect_the_sample(tmp_path: Path, registry: Registry) -> None:
    """Tier-1 is free, so it always reads everything; Tier-2 obeys the sample."""
    from telltale import scoring

    docs = [
        doc_from(E2E_DOC.replace("Consolidation", f"C{i}"), doc_id=f"m/doc-{i:02d}")
        for i in range(4)
    ]
    tells = [registry.get("rht.rhetorical-qa"), registry.get("pnc.arrow-chain")]
    df = scoring.detect_all(
        docs, tells, judge=JudgeBackend(make_client(tmp_path, e2e_router)),
        judge_docs=["m/doc-00", "m/doc-02"],
    )
    judged = df[df["method"] == "judge"]
    deterministic = df[df["method"] != "judge"]
    assert sorted(judged["doc_id"]) == ["m/doc-00", "m/doc-02"]
    assert len(deterministic["doc_id"].unique()) == 4


def test_a_sampled_run_records_the_sample_beside_its_scores(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    from telltale import report as report_mod
    from telltale.judge import sampling

    _install_fake_judge(monkeypatch, tmp_path)
    runs = tmp_path / "runs"
    _calibrate_all(runs, registry)
    run_dir = report_mod.score_run(
        corpus_root=judged_corpus, registry_path=REGISTRY_PATH, out_root=runs,
        bootstrap_n=20, judge=True, judge_model=JUDGE_MODEL_DEFAULT, runs_root=runs,
        judge_sample=1, judge_sample_seed=7,
    )
    recorded = json.loads((run_dir / sampling.SAMPLE_FILENAME).read_text(encoding="utf-8"))
    assert recorded["n_selected"] == 1
    assert recorded["seed"] == 7

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["judge"]["sample"]["n_selected"] == 1

    rows = [json.loads(l) for l in (run_dir / "scores.jsonl").read_text().splitlines()]
    judged_docs = {r["doc_id"] for r in rows if r["method"] == "judge"}
    all_docs = {r["doc_id"] for r in rows}
    assert judged_docs == set(recorded["doc_ids"])
    assert len(all_docs) == 2, "Tier-1 still scored the whole corpus"
    assert "(n=1 docs)" in (run_dir / "scorecard.md").read_text(encoding="utf-8")


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
    # The canned judge answers only ever supply criteria (a) and (b), so the two
    # tells whose rubrics require (a)+(b)+(c) reject a span the judge called an
    # instance. That is a real disagreement and the rollup has to surface it —
    # and since those tells counted nothing, it is the undefined-rate case.
    disagreement = judge["disagreements"]
    assert disagreement["total"] == 2
    assert set(disagreement["over_threshold"]) == {"rht.rule-of-three", "rht.from-x-to-y"}
    assert disagreement["per_tell"]["rht.rule-of-three"]["disagreements"] == 1
    assert disagreement["per_tell"]["rht.rhetorical-qa"]["disagreements"] == 0
    assert disagreement["per_tell"]["rht.rhetorical-qa"]["rate"] == 0.0
    assert judge["calibration"]["rht.rhetorical-qa"]["agreement"] == 0.95

    rows = [json.loads(line) for line in (run_dir / "scores.jsonl").read_text().splitlines()]
    judged = [r for r in rows if r["method"] == "judge"]
    assert {r["tell_id"] for r in judged} == set(protocol.RULES)
    hit = [r for r in judged if r["tell_id"] == "rht.rhetorical-qa" and r["raw"] == 1.0]
    assert hit and hit[0]["matches"][0]["quote"] == "So why did the count change?"

    card = (run_dir / "scorecard.md").read_text(encoding="utf-8")
    assert f"| Judge model | `{JUDGE_MODEL_DEFAULT}` |" in card
    assert "Hallucinated quotes" in card
    assert "Judge/code disagreement" in card
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
