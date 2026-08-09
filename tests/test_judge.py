"""Tests for the Tier-2 judge stack.

No test in this file calls a model. Every judge answer is canned, which is the
only way to test the part that matters: what the code does with an answer once
it has one. The live checks are run by hand and their transcripts live in
runs/calibration/.
"""

from __future__ import annotations

import json
import re
import threading
import time
from pathlib import Path
from typing import Any, Sequence

import pytest

from telltale.corpus import Doc
from telltale.detectors import build
from telltale.detectors.judge_detector import JudgeBackend
from telltale.isolation import CliResult
from telltale.judge import audit as audit_mod
from telltale.judge import calibrate as calibration
from telltale.judge import protocol
from telltale import textstats
from telltale.judge import transport as transport_mod
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
    """A model that is not the harness's side-model answering is fatal at once.

    R16-era recommendation 2 made the haiku substitution retryable; it did not
    make "some other judge answered" retryable, and this is the case that keeps
    the two apart.
    """
    cli = fake_cli(envelope('{"spans": []}', model="claude-opus-4-7"))
    transport = CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli)
    with pytest.raises(JudgeError, match="model mismatch"):
        transport.ask("go")
    assert len(cli.calls) == 1, "and it costs exactly one call"
    assert transport.stats.substitutions_detected == 0


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
    """The table is a mirror of the rubric text. Drift has to fail here.

    The table covers every judge tell the registry carries, not only the active
    ones: `rht.from-x-to-y` was deprecated by ruling R17 (2026-08-09) and its
    entry stays in the registry for history, so its rule stays here to keep the
    cached answers for it readable and its calibration set replayable.
    """
    judge_tells = [
        t
        for t in registry.tells
        if t.method == "judge" and t.status in {"active", "deprecated"}
    ]
    assert {t.id for t in judge_tells} == set(protocol.RULES)
    active = {t.id for t in registry.active_tells() if t.method == "judge"}
    assert active == set(protocol.RULES) - {"rht.from-x-to-y"}
    for tell in judge_tells:
        criteria, exclusions = protocol.parse_rubric_labels(tell.rubric)
        rule = protocol.RULES[tell.id]
        assert rule.required == criteria, f"{tell.id}: criteria drifted from the rubric"
        assert rule.exclusions == exclusions, f"{tell.id}: exclusions drifted"
        # ALL vs ANY is read off the rubric's own opening line.
        head = tell.rubric.split("\n", 1)[0]
        assert rule.mode == ("any" if "ANY" in head else "all"), tell.id
        # Protocol v3: a structural exclusion disposes of spans in code, so its
        # letter has to be one the rubric actually writes, and the classes it
        # maps to have to be classes `classify_line` can return. A letter
        # invented here would reject spans under an exclusion nobody wrote.
        for letter, classes in rule.structural_exclusions.items():
            assert letter in exclusions, f"{tell.id}: ({letter}) is not in the rubric"
            assert classes, f"{tell.id}: ({letter}) maps to no line class"
            for line_class in classes:
                assert line_class in textstats.LINE_CLASSES, f"{tell.id}: {line_class}"
            assert "prose" not in classes, f"{tell.id}: prose is not a structural shape"


def test_the_structural_exclusion_map_says_what_the_two_rubrics_say() -> None:
    """The mapping, spelled out against the rubric text it was read from.

    The test above proves the letters exist; this one proves they are the right
    ones. Both are needed — a map that moved (x) onto list items would pass the
    first check and still be excluding bullets as headings.
    """
    fragment = protocol.RULES["rht.fragment-emphasis"]
    assert fragment.structural_exclusions == {
        "x": ("heading",),  # headings, subheadings, titles, bolded run-ins
        "y": ("list_item", "table_row"),  # list items, table cells, bullet text
        "z": ("signoff", "caption"),  # salutations, sign-offs, captions, labels
    }
    # (w) is quoted speech: not a line shape, so the judge keeps it.
    assert "w" in fragment.exclusions
    assert "w" not in fragment.structural_exclusions

    three = protocol.RULES["rht.rule-of-three"]
    # (y) alone: "a list rendered as bullets or numbered items is out of scope".
    # (x) enumerative content and (z) quotation are both semantic.
    assert three.structural_exclusions == {"y": ("list_item",)}
    assert three.adjudication_cap == 11

    # No other judge tell disposes of anything in code.
    for tell_id, rule in protocol.RULES.items():
        if tell_id not in {"rht.fragment-emphasis", "rht.rule-of-three"}:
            assert rule.structural_exclusions == {}
            assert rule.adjudication_cap is None


def test_structural_exclusion_for_returns_the_rubric_letter() -> None:
    rule = protocol.RULES["rht.fragment-emphasis"]
    assert protocol.structural_exclusion_for(rule, "heading") == "x"
    assert protocol.structural_exclusion_for(rule, "table_row") == "y"
    assert protocol.structural_exclusion_for(rule, "signoff") == "z"
    assert protocol.structural_exclusion_for(rule, "caption") == "z"
    assert protocol.structural_exclusion_for(rule, "prose") is None
    # A class the tell does not declare is not disposed of, even if another
    # tell declares it.
    assert protocol.structural_exclusion_for(rule, "rule") is None
    assert protocol.structural_exclusion_for(rule, "blank") is None

    three = protocol.RULES["rht.rule-of-three"]
    assert protocol.structural_exclusion_for(three, "list_item") == "y"
    assert protocol.structural_exclusion_for(three, "table_row") is None
    assert protocol.structural_exclusion_for(three, "heading") is None

    assert protocol.structural_exclusion_for(protocol.RULES["rht.from-x-to-y"], "heading") is None


def test_the_prompt_version_is_what_the_cache_keys_on() -> None:
    """Protocol v3 changed no prompt, so v2's cached answers stay reachable."""
    assert protocol.PROTOCOL_VERSION == 3
    assert protocol.PROMPT_VERSION == 2
    key = cache_key("sha", "rht.rule-of-three", 1, "model", EXTRACT)
    assert key == _sha_of_parts("sha", "rht.rule-of-three", "1", "model", "2", "extract")


def _sha_of_parts(*parts: str) -> str:
    import hashlib

    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


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
    assert "which is criterion (c)" in rubric  # the trap
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


# --- structural disposition and the adjudication cap (protocol v3) -----------


TRIAGE_DOC = """\
# Quarterly platform review

Dear Amara,

**The grant.** The reconciliation script wrote to the wrong column for six
weeks. Six weeks.

## Findings

- No go-live gate.
- Silent exclusions.

| Site | Status |
|------|--------|
| Ashford | Red. |

Note: the vendor has not answered.

Best regards,
"""


def span_under_review(prompt: str) -> str:
    return prompt.split("<<<SPAN", 1)[1].split("SPAN>>>", 1)[0].strip()


def triage_router(prompt: str) -> dict[str, Any]:
    """Extracts one candidate per structural shape, plus one real prose fragment.

    Every span it proposes is a verbatim quote from TRIAGE_DOC, so the only
    thing that can stop one reaching adjudication is the code.
    """
    if "EXTRACTION ONLY" in prompt:
        return {
            "spans": [
                {"quote": "# Quarterly platform review", "location_hint": "title"},
                {"quote": "Dear Amara,", "location_hint": "salutation"},
                {"quote": "**The grant.**", "location_hint": "run-in heading"},
                {"quote": "Six weeks.", "location_hint": "after the sentence"},
                {"quote": "- No go-live gate.", "location_hint": "bullet"},
                {"quote": "| Ashford | Red. |", "location_hint": "table"},
                {"quote": "Note: the vendor has not answered.", "location_hint": "callout"},
                {"quote": "Best regards,", "location_hint": "sign-off"},
            ]
        }
    return {
        "instance": True,
        "criteria_met": ["a", "b"],
        "exclusion_triggered": None,
        "rationale": "a verbless fragment leaning on the sentence before it",
    }


def test_structural_spans_never_reach_the_judge(tmp_path: Path, registry: Registry) -> None:
    """Fix M8d-1, end to end: only the prose span is paid for."""
    tell = registry.get("rht.fragment-emphasis")
    client = make_client(tmp_path, triage_router)
    detection = JudgeBackend(client).detect(tell, doc_from(TRIAGE_DOC))

    adjudications = [p for p in client.transport.prompts if "ADJUDICATE ONE SPAN" in p]
    assert [span_under_review(p) for p in adjudications] == ["Six weeks."]
    assert detection.raw == 1.0

    detail = detection.detail
    assert detail["extracted"] == 8
    assert detail["excluded_by_code"] == 7
    assert detail["by_class"] == {
        "caption": 1,
        "heading": 2,  # the ATX title and the bolded run-in
        "list_item": 1,
        "signoff": 2,  # the salutation and the closing
        "table_row": 1,
    }
    assert detail["adjudicated_true"] == 1
    assert detail["adjudicated_false"] == 0


def test_a_dispositioned_span_stays_in_the_evidence(tmp_path: Path, registry: Registry) -> None:
    """A saving that cannot be audited is indistinguishable from a bug."""
    tell = registry.get("rht.fragment-emphasis")
    detection = JudgeBackend(make_client(tmp_path, triage_router)).detect(
        tell, doc_from(TRIAGE_DOC)
    )
    assert len(detection.matches) == 8
    counted = [m for m in detection.matches if m["counted"]]
    assert [m["quote"] for m in counted] == ["Six weeks."]
    assert detection.matches[0]["quote"] == "Six weeks.", "counted evidence comes first"

    disposed = {m["quote"]: m for m in detection.matches if not m["counted"]}
    assert disposed["Dear Amara,"]["exclusion_triggered"] == "z"
    assert disposed["Dear Amara,"]["line_class"] == "signoff"
    assert disposed["- No go-live gate."]["exclusion_triggered"] == "y"
    assert disposed["**The grant.**"]["exclusion_triggered"] == "x"
    for record in disposed.values():
        assert record["excluded_by_code"] is True
        # The judge was not asked, so it did not say False either.
        assert record["judge_instance"] is None
        assert record["line"] >= 1


def test_a_tell_without_structural_exclusions_sends_everything(
    tmp_path: Path, registry: Registry
) -> None:
    """The triage fires only where the criteria table declares it."""
    tell = registry.get("rht.rule-of-three")
    client = make_client(tmp_path, triage_router)
    detection = JudgeBackend(client).detect(tell, doc_from(TRIAGE_DOC))
    adjudicated = [
        span_under_review(p) for p in client.transport.prompts if "ADJUDICATE ONE SPAN" in p
    ]
    # rule-of-three declares (y) -> list_item and nothing else, so the heading,
    # the table row, the sign-offs and the callout all still go to the judge.
    assert "- No go-live gate." not in adjudicated
    assert "# Quarterly platform review" in adjudicated
    assert "| Ashford | Red. |" in adjudicated
    assert detection.detail["by_class"] == {"list_item": 1}


def _numbered_prose(n: int) -> str:
    """A chunk of n prose lines, each with a quotable triple."""
    return "\n\n".join(
        f"Finding {i} covers scope{i}, budget{i}, and timeline{i} in one sentence."
        for i in range(n)
    )


def cap_router(prompt: str) -> dict[str, Any]:
    if "EXTRACTION ONLY" in prompt:
        passage = passage_of(prompt)
        return {
            "spans": [
                {"quote": line.strip(), "location_hint": ""}
                for line in passage.split("\n")
                if line.strip().startswith("Finding ")
            ]
        }
    return {
        "instance": True,
        "criteria_met": ["a", "b", "c"],
        "exclusion_triggered": None,
        "rationale": "three coordinate nouns, the third adds cadence",
    }


def test_the_adjudication_cap_bites_in_document_order(
    tmp_path: Path, registry: Registry
) -> None:
    tell = registry.get("rht.rule-of-three")
    cap = protocol.RULES[tell.id].adjudication_cap
    assert cap == 11
    doc = doc_from(_numbered_prose(cap + 4))

    client = make_client(tmp_path, cap_router)
    detection = JudgeBackend(client).detect(tell, doc)

    adjudicated = [
        span_under_review(p) for p in client.transport.prompts if "ADJUDICATE ONE SPAN" in p
    ]
    assert len(adjudicated) == cap
    assert adjudicated == sorted(adjudicated, key=lambda q: int(q.split()[1]))
    assert [int(q.split()[1]) for q in adjudicated] == list(range(cap))
    assert detection.raw == float(cap)


def test_the_cap_is_visible_in_the_detection(tmp_path: Path, registry: Registry) -> None:
    """Truncation is never silent: the row that carries it says so."""
    tell = registry.get("rht.rule-of-three")
    cap = protocol.RULES[tell.id].adjudication_cap
    detection = JudgeBackend(make_client(tmp_path, cap_router)).detect(
        tell, doc_from(_numbered_prose(cap + 4))
    )
    assert detection.detail["adjudication_capped"] is True
    assert detection.detail["adjudication_cap"] == cap
    assert detection.detail["spans_skipped"] == 4
    skipped = [r for r in detection.detail["rejected"] if r["why_not"] == "adjudication cap"]
    assert len(skipped) == 4
    assert all(r["judge_instance"] is None for r in skipped)


def test_the_cap_is_absent_when_it_did_not_bite(tmp_path: Path, registry: Registry) -> None:
    tell = registry.get("rht.rule-of-three")
    detection = JudgeBackend(make_client(tmp_path, cap_router)).detect(
        tell, doc_from(_numbered_prose(3))
    )
    assert "adjudication_capped" not in detection.detail
    assert "spans_skipped" not in detection.detail
    assert detection.raw == 3.0


def test_the_cap_counts_adjudications_not_extractions(
    tmp_path: Path, registry: Registry
) -> None:
    """Spans the triage disposed of do not consume the cap."""
    tell = registry.get("rht.rule-of-three")
    cap = protocol.RULES[tell.id].adjudication_cap
    bullets = "\n".join(f"- bullet {i} of scope, budget, and timeline." for i in range(6))
    doc = doc_from(bullets + "\n\n" + _numbered_prose(cap))

    def router(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            return {
                "spans": [
                    {"quote": line.strip(), "location_hint": ""}
                    for line in passage_of(prompt).split("\n")
                    if line.strip()
                ]
            }
        return {"instance": True, "criteria_met": ["a", "b", "c"],
                "exclusion_triggered": None, "rationale": "triple"}

    client = make_client(tmp_path, router)
    detection = JudgeBackend(client).detect(tell, doc)
    assert detection.detail["by_class"] == {"list_item": 6}
    assert "adjudication_capped" not in detection.detail
    assert len([p for p in client.transport.prompts if "ADJUDICATE ONE SPAN" in p]) == cap


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


def test_a_code_disposition_is_named_in_the_calibration_detail(
    tmp_path: Path, registry: Registry
) -> None:
    """The gate report has to say a snippet was disposed of by the classifier.

    Otherwise "the line classifier rejected it" and "the judge found nothing to
    quote" read identically, and the gate stops being able to see the behaviour
    it exists to check.
    """
    tell = registry.get("rht.fragment-emphasis")
    snippet = calibration.Snippet(
        id="neg-x", label="negative", source="synthetic", text="## Every single school\n"
    )

    def router(prompt: str) -> dict[str, Any]:
        if "EXTRACTION ONLY" in prompt:
            return {"spans": [{"quote": "## Every single school", "location_hint": ""}]}
        raise AssertionError("a heading must never be adjudicated")

    backend = JudgeBackend(make_client(tmp_path, router))
    outcome = calibration.run_snippet(tell, snippet, backend)
    assert outcome.observed is False
    assert outcome.extracted == 1
    assert "(x) by structure: heading" in outcome.detail


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


def test_the_audit_draw_covers_every_tell_and_respects_a_budget() -> None:
    """Uniform sampling would spend the budget on whichever tell chunks most."""
    from telltale.registry import Tell

    def entry(tell_id: str, i: int):
        tell = Tell(id=tell_id, name=tell_id, category="rhetorical", method="judge")
        return (tell, f"m/doc-{i:02d}", None, "extract", {})

    # 90 cached items for one tell, 5 for another: a uniform draw of 10 would
    # be expected to take 9 and 1.
    available = [entry("deep", i) for i in range(90)] + [entry("thin", i) for i in range(5)]
    picks = audit_mod._stratified_picks(available, 10, seed=11)
    assert len(picks) == 10
    taken = [available[i][0].id for i in picks]
    assert taken.count("thin") == 5, "the thin tell's whole pool should be drawn first"
    assert taken.count("deep") == 5

    # Deterministic under the same seed, and the cap trims the tail of the
    # round rather than dropping a tell.
    assert audit_mod._stratified_picks(available, 10, seed=11) == picks
    small = audit_mod._stratified_picks(available, 4, seed=11)
    assert {available[i][0].id for i in small} == {"deep", "thin"}


# --- judge/code disagreement rollup ------------------------------------------


def _judge_frame(rows: list[tuple[str, int, int, int]]):
    """A minimal detection frame: (tell_id, disagreements, true, false)."""
    import pandas as pd

    return pd.DataFrame(
        [
            {
                "tell_id": tell_id,
                "method": "judge",
                "detail": {
                    "judge_disagreements": d,
                    "adjudicated_true": t,
                    "adjudicated_false": f,
                },
            }
            for tell_id, d, t, f in rows
        ]
    )


def test_disagreements_roll_up_across_documents_and_tells() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(
        _judge_frame([("a", 1, 6, 4), ("a", 2, 7, 3), ("b", 0, 3, 2)])
    )
    assert roll["total"] == 3
    assert roll["adjudicated"] == 25
    assert roll["rate"] == pytest.approx(3 / 25)
    assert roll["per_tell"]["a"] == {
        "disagreements": 3,
        "adjudicated": 20,
        "rate": pytest.approx(0.15),
    }
    assert roll["per_tell"]["b"]["rate"] == 0.0
    assert roll["over_threshold"] == []


def test_the_denominator_is_every_adjudicated_span_not_the_true_ones() -> None:
    """The M8 shakedown defect: dividing by adjudicated_true alone.

    A disagreement is recorded whenever the judge's own verdict parts from what
    the criteria compute, and that happens just as readily on a span the code
    scored false. Over the true count alone the rate mixed two populations and
    could exceed 1.0 outright.
    """
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("t", 2, 2, 8)]))
    assert roll["per_tell"]["t"]["adjudicated"] == 10
    assert roll["per_tell"]["t"]["rate"] == pytest.approx(0.20)
    assert roll["over_threshold"] == [], "1.0 under the old denominator"


def test_a_tell_over_the_threshold_is_named() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(
        _judge_frame([("noisy", 3, 5, 5), ("quiet", 1, 5, 5)])
    )
    assert roll["per_tell"]["noisy"]["rate"] == pytest.approx(0.30)
    assert roll["over_threshold"] == ["noisy"]
    assert roll["threshold"] == report_mod.DISAGREEMENT_WARN_RATE


def test_the_threshold_is_strict_not_inclusive() -> None:
    from telltale import report as report_mod

    exactly = report_mod.judge_disagreements(_judge_frame([("t", 2, 4, 6)]))
    assert exactly["per_tell"]["t"]["rate"] == pytest.approx(0.20)
    assert exactly["over_threshold"] == [], "at the threshold is not over it"
    assert (
        report_mod.judge_disagreements(_judge_frame([("t", 3, 4, 6)]))["over_threshold"]
        == ["t"]
    )


def test_a_tell_that_adjudicated_nothing_has_no_disagreement_rate() -> None:
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("t", 0, 0, 0)]))
    assert roll["per_tell"]["t"]["rate"] is None
    assert roll["rate"] is None
    assert roll["over_threshold"] == []


def test_a_tell_the_code_never_counted_still_gets_a_rate() -> None:
    """Under the old denominator this tell had no rate at all.

    Ten spans adjudicated, none of them true, and the judge called four of them
    instances: that is the rubric-drift case the rollup exists to surface, and
    dividing by the true count made it invisible behind a zero denominator.
    """
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("stuck", 4, 0, 10)]))
    assert roll["per_tell"]["stuck"]["rate"] == pytest.approx(0.40)
    assert roll["over_threshold"] == ["stuck"]


def test_disagreements_with_nothing_adjudicated_are_still_flagged() -> None:
    """Unreachable if the accounting is sound, so worth saying aloud if it happens."""
    from telltale import report as report_mod

    roll = report_mod.judge_disagreements(_judge_frame([("broken", 4, 0, 0)]))
    assert roll["per_tell"]["broken"]["rate"] is None
    assert roll["per_tell"]["broken"]["disagreements"] == 4
    assert roll["over_threshold"] == ["broken"]


def test_the_cli_explains_an_undefined_disagreement_rate(capsys) -> None:
    from telltale.cli import _warn_on_disagreement

    _warn_on_disagreement(
        {
            "disagreements": {
                "over_threshold": ["broken"],
                "threshold": 0.2,
                "per_tell": {
                    "broken": {"disagreements": 4, "adjudicated": 0, "rate": None}
                },
            }
        }
    )
    err = capsys.readouterr().err
    assert "nothing adjudicated at all" in err


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
                "per_tell": {
                        "rht.rule-of-three": {
                            "disagreements": 9,
                            "adjudicated": 20,
                            "rate": 0.45,
                        }
                    },
            }
        }
    )
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert "rht.rule-of-three: 9 of 20 adjudicated spans (45%)" in err
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
    assert f"{controller._calls} calls," in lines[0]
    # The bug this test exists for was a progress line reading "0 calls" while
    # calls were in flight. Anchored on the comma: the same line also carries a
    # calls-per-minute rate, and on a fast machine that rate can end in "0",
    # which made a bare "0 calls" substring check fail at random.
    assert controller._calls > 0
    assert "0 calls," not in lines[0]


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


# --- outage handling: transient retry and the cascade breaker -----------------


def test_empty_model_usage_is_transient_but_a_real_mismatch_is_not() -> None:
    """The two shapes of "model_mismatch" mean opposite things.

    Empty modelUsage means nothing reached the API — the network. A different
    model actually present means something else answered — a fact about the
    run, and never retried.
    """
    from telltale.judge.transport import TransientJudgeError

    outage = json.dumps(
        {"result": "", "session_id": "s", "num_turns": 0, "is_error": True, "modelUsage": {}}
    )
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=fake_cli(outage, outage),
        retry_delay_s=0, sleep=lambda s: None,
    )
    with pytest.raises(TransientJudgeError, match="empty modelUsage"):
        transport.ask("go")

    wrong_judge = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(envelope('{"spans": []}', model="claude-opus-4-7")),
    )
    with pytest.raises(JudgeError, match="model mismatch") as caught:
        wrong_judge.ask("go")
    assert not isinstance(caught.value, TransientJudgeError)


def test_a_haiku_substitution_is_retried_once_and_recovers() -> None:
    """SHAKEDOWN §2.3: the main call died and the harness's side-call is all
    that is left in the envelope. Nothing judged the passage, so one more try
    costs a call and buys back a measurement — nine of them, in the run that
    found this."""
    from telltale.judge.transport import ModelSubstitutionError

    slept: list[float] = []
    cli = fake_cli(
        envelope('{"spans": []}', model="claude-haiku-4-5"),
        envelope('{"spans": [{"quote": "q", "location_hint": ""}]}'),
    )
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=cli, sleep=slept.append
    )
    answer = transport.ask("go")
    assert answer["spans"][0]["quote"] == "q"
    assert len(cli.calls) == 2
    assert cli.calls[0][1] == cli.calls[1][1], "the retry asks the same question"
    assert slept == [], "a substitution is not congestion; there is nothing to wait out"
    stats = transport.stats.as_dict()
    assert stats["substitutions_detected"] == 1
    assert stats["substitution_retries"] == 1
    assert stats["substitutions_recovered"] == 1
    assert stats["substitutions_failed"] == 0
    assert stats["failures"] == 0, "a recovered substitution is not a failure"
    assert issubclass(ModelSubstitutionError, JudgeError)


def test_a_second_substitution_hard_fails() -> None:
    """One retry, then it is a fact about the run like any other mismatch."""
    from telltale.judge.transport import ModelSubstitutionError

    cli = fake_cli(
        envelope('{"spans": []}', model="claude-haiku-4-5"),
        envelope('{"spans": []}', model="claude-haiku-4-5"),
    )
    transport = CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli)
    with pytest.raises(ModelSubstitutionError, match="model substitution"):
        transport.ask("go")
    assert len(cli.calls) == 2, "exactly one retry, never two"
    stats = transport.stats.as_dict()
    assert stats["substitutions_detected"] == 2
    assert stats["substitution_retries"] == 1
    assert stats["substitutions_recovered"] == 0
    assert stats["substitutions_failed"] == 1
    assert stats["failures"] == 1


def test_a_side_model_alongside_the_judge_is_not_a_mismatch_at_all() -> None:
    """The harness always makes side-calls; only their standing alone is the bug."""
    both = json.dumps(
        {
            "result": '{"spans": []}',
            "session_id": "s-1",
            "num_turns": 1,
            "is_error": False,
            "modelUsage": {
                JUDGE_MODEL_DEFAULT: {"outputTokens": 40},
                "claude-haiku-4-5": {"outputTokens": 3},
            },
        }
    )
    cli = fake_cli(both)
    transport = CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli)
    assert transport.ask("go") == {"spans": []}
    assert transport.stats.substitutions_detected == 0
    assert len(cli.calls) == 1


def test_a_transient_failure_gets_one_retry_then_succeeds() -> None:
    outage = json.dumps(
        {"result": "", "session_id": "s", "num_turns": 0, "is_error": True, "modelUsage": {}}
    )
    slept: list[float] = []
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT,
        transport=fake_cli(outage, envelope('{"spans": []}')),
        retry_delay_s=30.0,
        sleep=slept.append,
    )
    assert transport.ask("go") == {"spans": []}
    assert slept == [30.0], "it waits before the one retry"
    assert transport.stats.transient_retries == 1


def test_a_transient_failure_that_persists_is_raised_not_retried_forever() -> None:
    from telltale.judge.transport import TransientJudgeError

    outage = json.dumps(
        {"result": "", "session_id": "s", "num_turns": 0, "is_error": True, "modelUsage": {}}
    )
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=fake_cli(outage, outage, outage),
        retry_delay_s=0, sleep=lambda s: None,
    )
    with pytest.raises(TransientJudgeError):
        transport.ask("go")
    assert transport.stats.transient_retries == 1, "one retry, not a loop"


def test_a_timed_out_call_is_transient() -> None:
    from telltale.isolation import CliResult
    from telltale.judge.transport import TransientJudgeError

    def timing_out(cmd, prompt, timeout):
        return CliResult(124, "", "timed out after 300s", 300.0, timed_out=True)

    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=timing_out, retry_delay_s=0,
        sleep=lambda s: None,
    )
    with pytest.raises(TransientJudgeError):
        transport.ask("go")


OUTAGE_ENVELOPE = json.dumps(
    {"result": "", "session_id": "s", "num_turns": 0, "is_error": True, "modelUsage": {}}
)


def test_the_liveness_probe_does_not_sit_through_the_retry_pause() -> None:
    """A probe is already the breaker's retry, so it must not sleep inside one.

    Thirty seconds here would be thirty seconds the sweep spends not noticing
    the network came back, once per probe, for the whole outage.
    """
    slept: list[float] = []
    calls: list[str] = []

    def down(cmd: list[str], prompt: str, timeout: int) -> CliResult:
        calls.append(prompt)
        return CliResult(returncode=1, stdout=OUTAGE_ENVELOPE, stderr="", duration_s=0.1)

    # `sleep` is a dataclass default, bound at import, so the pause has to be
    # observed on the instance the probe builds rather than by patching a clock.
    built: list[CliJudgeTransport] = []
    real = transport_mod.CliJudgeTransport

    def spy(**kwargs):
        made = real(**kwargs, sleep=slept.append)
        built.append(made)
        return made

    transport_mod.CliJudgeTransport = spy
    try:
        assert probe_judge(JUDGE_MODEL_DEFAULT, transport=down) is False
    finally:
        transport_mod.CliJudgeTransport = real

    assert built and built[0].retry_delay_s == 0
    assert slept == [0], "it waits for nothing, but it still waits once"
    assert len(calls) == 2, "it still gets its one retry, just without the pause"


def _cli_backend(tmp_path: Path, router, script: Sequence[str] = (), **kwargs):
    """A judge wired through the real CliJudgeTransport, so retries are exercised.

    `script` is replayed as raw stdout before the router takes over, which is
    how an outage is staged: the first call comes back with nothing billed to
    any model, exactly as it did on the night this was written.
    """
    pending = list(script)
    calls: list[str] = []

    def transport(cmd: list[str], prompt: str, timeout: int) -> CliResult:
        calls.append(prompt)
        if pending:
            return CliResult(returncode=1, stdout=pending.pop(0), stderr="", duration_s=0.1)
        return CliResult(returncode=0, stdout=envelope(router(prompt)), stderr="", duration_s=0.1)

    wire = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=transport, retry_delay_s=0,
        sleep=lambda s: None, **kwargs
    )
    client = JudgeClient(transport=wire, cache=JudgeCache(tmp_path / "judge"))
    return JudgeBackend(client), wire, calls


def test_an_outage_blip_costs_a_pause_not_a_measurement(
    tmp_path: Path, registry: Registry
) -> None:
    """The retry that matters: an empty-modelUsage call is re-asked, and the
    measurement lands as if nothing had happened."""
    from telltale import scoring

    backend, wire, calls = _cli_backend(tmp_path, e2e_router, script=[OUTAGE_ENVELOPE])
    df = scoring.detect_all([doc_from(E2E_DOC)], [registry.get("rht.rhetorical-qa")], judge=backend)

    assert df.attrs["judge_errors"] == [], "a blip is not a measurement failure"
    assert len(df) == 1, "the measurement completed"
    assert wire.stats.transient_retries == 1
    assert calls[0] == calls[1], "the retry re-asks the same question"


def test_a_substituted_judge_fails_the_measurement_immediately(
    tmp_path: Path, registry: Registry
) -> None:
    """The other half: if some other model really answered, that is not a blip.

    Retrying would be worse than useless — it would spend a second call to
    reach the same wrong judge, and might quietly succeed on it. The harness's
    own side-model is the one exception, covered by the test below.
    """
    from telltale import scoring

    wrong = envelope('{"spans": []}', model="claude-opus-4-7")
    backend, wire, calls = _cli_backend(tmp_path, e2e_router, script=[wrong])
    df = scoring.detect_all([doc_from(E2E_DOC)], [registry.get("rht.rhetorical-qa")], judge=backend)

    errors = df.attrs["judge_errors"]
    assert len(errors) == 1
    assert "model mismatch" in errors[0]["error"]
    assert "claude-opus-4-7" in errors[0]["error"], "it names the model that answered"
    assert wire.stats.transient_retries == 0, "a real mismatch is never retried"
    assert wire.stats.substitution_retries == 0
    assert len(calls) == 1, "and it costs exactly one call"


def test_a_substituted_judge_is_retried_and_the_measurement_lands(
    tmp_path: Path, registry: Registry
) -> None:
    """End to end: the substitution costs a call, not a measurement."""
    from telltale import scoring

    substituted = envelope('{"spans": []}', model="claude-haiku-4-5")
    backend, wire, calls = _cli_backend(tmp_path, e2e_router, script=[substituted])
    df = scoring.detect_all([doc_from(E2E_DOC)], [registry.get("rht.rhetorical-qa")], judge=backend)

    assert df.attrs["judge_errors"] == [], "the retry recovered it"
    assert len(df) == 1
    assert wire.stats.substitutions_detected == 1
    assert wire.stats.substitutions_recovered == 1
    assert calls[0] == calls[1], "the retry re-asks the same question"


class _ProbeDriver:
    """Drives a paused sweep's probe loop one iteration at a time.

    The loop's shape is sleep, check the clock, probe. Handing it a semaphore
    to sleep on turns "every sixty seconds" into "when the test says so", and
    handing it a clock the test moves turns "after thirty minutes" into one
    assignment — so these tests exercise the shipped defaults, 60s and 1800s,
    rather than a miniature of them that might not be the same code path.
    """

    def __init__(self, results: Sequence[bool] = ()) -> None:
        self.now = 0.0
        self.probes = 0
        self._results = list(results)
        self._go = threading.Semaphore(0)

    def clock(self) -> float:
        return self.now

    def sleep(self, _seconds: float) -> None:
        self._go.acquire()

    def probe(self) -> bool:
        self.probes += 1
        return self._results.pop(0) if self._results else False

    def step(self, until, timeout: float = 5.0) -> bool:
        """Release one probe iteration and wait for `until` to come true."""
        self._go.release()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if until():
                return True
            time.sleep(0.002)
        return False


def _breaker(driver: _ProbeDriver, **policy):
    from telltale.judge.sweep import SweepController, SweepPolicy

    lines: list[str] = []
    defaults = dict(workers=4, ceiling=4, breaker_after=8)
    defaults.update(policy)
    return (
        SweepController(
            policy=SweepPolicy(**defaults), total=10, emit=lines.append,
            probe=driver.probe, sleep=driver.sleep, clock=driver.clock,
        ),
        lines,
    )


def test_the_breaker_opens_at_exactly_eight_consecutive_failures() -> None:
    driver = _ProbeDriver()
    controller, lines = _breaker(driver)
    for _ in range(7):
        controller.record_failure("connection closed")
    assert not controller.breaker_open, "seven is not a cascade"
    assert controller.breaker_trips == 0

    controller.record_failure("connection closed")
    assert controller.breaker_open
    assert controller.breaker_trips == 1
    assert any(line.startswith("BREAKER-OPEN") for line in lines)
    assert any("8 consecutive failures" in line for line in lines)

    # Further failures from workers already in flight do not re-trip it.
    controller.record_failure("connection closed")
    assert controller.breaker_trips == 1


def test_a_success_between_failures_resets_the_cascade_count() -> None:
    driver = _ProbeDriver()
    controller, _ = _breaker(driver)
    for _ in range(7):
        controller.record_failure("bad json")
    controller.record_ok()
    for _ in range(7):
        controller.record_failure("bad json")
    assert not controller.breaker_open, "scattered failures are data, not an outage"
    assert driver.probes == 0, "a sweep that never paused never probes"


def test_the_breaker_closes_when_the_probe_succeeds_and_workers_resume() -> None:
    driver = _ProbeDriver(results=[False, False, True])
    controller, lines = _breaker(driver)
    for _ in range(8):
        controller.record_failure("connection reset")
    assert controller.breaker_open

    # A worker asking for its next measurement parks until the breaker closes.
    parked: list[bool] = []
    worker = threading.Thread(target=lambda: parked.append(controller.await_ready()))
    worker.start()

    driver.now += 60.0
    assert driver.step(lambda: driver.probes == 1)
    assert controller.breaker_open, "one failed probe is not recovery"
    worker.join(timeout=0.2)
    assert worker.is_alive() and not parked, "the worker is still parked"

    driver.now += 60.0
    assert driver.step(lambda: driver.probes == 2)
    assert controller.breaker_open

    driver.now += 60.0
    assert driver.step(lambda: not controller.breaker_open)
    worker.join(timeout=5)
    assert parked == [True], "the parked worker was released, not stopped"
    assert controller.await_ready() is True
    assert controller.stop_reason is None
    assert any(line.startswith("BREAKER-CLOSED") for line in lines)
    assert any("after 3.0m" in line for line in lines)

    # And the sweep goes on: the cascade count started over, so the next eight
    # failures are what re-trips it, not the ones from before the outage.
    for _ in range(7):
        controller.record_failure("connection reset")
    assert not controller.breaker_open
    controller.record_failure("connection reset")
    assert controller.breaker_open
    assert controller.breaker_trips == 2


def test_a_breaker_that_never_closes_halts_the_sweep_cleanly() -> None:
    driver = _ProbeDriver()  # every probe fails, forever
    controller, lines = _breaker(driver)
    for _ in range(8):
        controller.record_failure("connection closed")

    # Twenty-nine minutes of failed probes still leaves the sweep waiting.
    for minute in range(1, 30):
        driver.now = 60.0 * minute
        assert driver.step(lambda n=minute: driver.probes == n)
        assert controller.stop_reason is None, f"gave up at {minute}m"

    driver.now = 60.0 * 30
    assert driver.step(lambda: controller.stop_reason is not None)
    assert controller.stop_reason == "outage"
    assert controller.await_ready() is False, "workers stop asking for work"
    assert not controller.breaker_open
    assert any(line.startswith("SWEEP-HALTED (outage)") for line in lines)
    assert any("after 30m" in line for line in lines)
    assert any("the same command resumes" in line for line in lines)


def test_an_open_breaker_stops_measurements_being_burned(
    tmp_path: Path, registry: Registry
) -> None:
    """The behaviour the outage exposed: don't record failures against a dead network."""
    from telltale import scoring
    from telltale.judge.sweep import SweepController, SweepPolicy

    docs = [
        doc_from(E2E_DOC.replace("Consolidation", f"C{i}"), doc_id=f"m/doc-{i:02d}")
        for i in range(20)
    ]
    tells = [registry.get("rht.rhetorical-qa")]

    def dead(prompt: str):
        raise JudgeError("connection closed by remote host")

    # The probe never recovers and the deadline has already passed, so the
    # first probe iteration halts the sweep — the same path a real thirty
    # minutes reaches, without the thirty minutes.
    controller = SweepController(
        policy=SweepPolicy(workers=1, ceiling=1, breaker_after=8, breaker_timeout_s=0.0),
        total=len(docs), probe=lambda: False, sleep=lambda s: time.sleep(0.001),
    )
    df = scoring.detect_all(
        docs, tells, judge=JudgeBackend(make_client(tmp_path, dead)),
        workers=1, controller=controller,
    )
    assert df.empty
    errors = df.attrs["judge_errors"]
    assert 8 <= len(errors) <= 12, (
        f"the breaker should stop the queue near the threshold, got {len(errors)} "
        "of 20 documents burned"
    )
    assert controller.stop_reason == "outage"


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


def test_the_exploratory_annex_is_never_drawn_into_the_sample() -> None:
    """R20: free-writing documents are not benchmark cells and never get judged."""
    from telltale.judge import sampling

    docs = _corpus() + [
        Doc.from_text(
            doc_id=f"{m}/free-writing-{i:02d}",
            model=m,
            fmt="free-writing",
            text="# T\n\nBody text here.\n",
        )
        for m in ("m1", "m2")
        for i in range(1, 9)
    ]
    sample = sampling.stratified_sample(docs, size=12, seed=7)
    assert "free-writing" not in sample.per_format
    assert not any("free-writing" in d for d in sample.doc_ids)
    assert all(s.fmt != "free-writing" for s in sample.strata)


def test_adding_the_annex_does_not_move_the_sample() -> None:
    """The annex must not change which evidence documents Tier-2 reads."""
    from telltale.judge import sampling

    plain = _corpus()
    annexed = plain + [
        Doc.from_text(
            doc_id=f"{m}/free-writing-{i:02d}",
            model=m,
            fmt="free-writing",
            text="# T\n\nBody text here.\n",
        )
        for m in ("m1", "m2")
        for i in range(1, 9)
    ]
    assert (
        sampling.stratified_sample(annexed, size=12, seed=7).doc_ids
        == sampling.stratified_sample(plain, size=12, seed=7).doc_ids
    )


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


def test_an_unsampled_judge_run_still_skips_the_exploratory_annex(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """R20: Tier-2 never reads annex documents, sample or no sample."""
    from telltale import report as report_mod

    (judged_corpus / "claude-opus-5" / "free-writing-01.md").write_text(E2E_DOC, encoding="utf-8")

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
    rows = [json.loads(line) for line in (run_dir / "scores.jsonl").read_text().splitlines()]
    annex = [r for r in rows if r["doc_id"] == "claude-opus-5/free-writing-01"]
    assert annex, "Tier-1 must still run on the annex document"
    assert all(r["method"] != "judge" for r in annex), "Tier-2 must not read it"
    # The evidence documents were judged as usual.
    assert any(r["method"] == "judge" for r in rows if r["doc_id"] == "claude-opus-5/memo-01")


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
    # Every judge tell with a rule except the deprecated one (R17): scoring
    # never asks about a tell that is not active.
    assert len(judge["tells_scored"]) == len(protocol.RULES) - 1
    assert "rht.from-x-to-y" not in judge["tells_scored"]
    assert judge["cache"]["misses"] >= 1
    assert judge["hallucination"]["rate"] == 0.0
    # The canned judge answers only ever supply criteria (a) and (b), so the
    # tell whose rubric requires (a)+(b)+(c) rejects a span the judge called an
    # instance. That is a real disagreement and the rollup has to surface it —
    # and since that tell counted nothing, it is the undefined-rate case.
    # (`rht.from-x-to-y` used to be the second such tell; R17 deprecated it.)
    disagreement = judge["disagreements"]
    assert disagreement["total"] == 1
    assert set(disagreement["over_threshold"]) == {"rht.rule-of-three"}
    assert disagreement["per_tell"]["rht.rule-of-three"]["disagreements"] == 1
    assert disagreement["per_tell"]["rht.rhetorical-qa"]["disagreements"] == 0
    assert disagreement["per_tell"]["rht.rhetorical-qa"]["rate"] == 0.0
    assert judge["calibration"]["rht.rhetorical-qa"]["agreement"] == 0.95

    rows = [json.loads(line) for line in (run_dir / "scores.jsonl").read_text().splitlines()]
    judged = [r for r in rows if r["method"] == "judge"]
    assert {r["tell_id"] for r in judged} == set(protocol.RULES) - {"rht.from-x-to-y"}
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


def test_a_sampled_judge_run_verifies_on_the_documents_it_actually_judged(
    tmp_path: Path, judged_corpus: Path, registry: Registry, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The sample is an input to the run, so the replay has to draw it too.

    A replay that ignored the sample would ask the judge about documents the
    run never judged, and the first one is a cache miss — the verifier failing
    on work nobody did.
    """
    from telltale import manifest as manifest_mod
    from telltale import report as report_mod

    _install_fake_judge(monkeypatch, tmp_path)
    runs = tmp_path / "runs"
    _calibrate_all(runs, registry)
    run_dir = report_mod.score_run(
        corpus_root=judged_corpus, registry_path=REGISTRY_PATH, out_root=runs,
        bootstrap_n=20, judge=True, judge_model=JUDGE_MODEL_DEFAULT, runs_root=runs,
        judge_sample=1, judge_sample_seed=7,
    )

    result = manifest_mod.verify(run_dir)
    assert result.ok, result.summary()
    assert any("judge_sample" in name for name in result.checked)


def test_a_measurement_that_failed_live_replays_as_a_failure_not_a_lost_input(
    tmp_path: Path, registry: Registry
) -> None:
    """A call that failed live wrote nothing to the cache.

    On replay its absence is the faithful reproduction of that run, not a
    vanished input — but only for the (tell, document) pairs the manifest
    actually recorded as failures. Any other miss still stops the replay.
    """
    from telltale import scoring

    docs = [
        doc_from(E2E_DOC.replace("Consolidation", f"C{i}"), doc_id=f"m/doc-{i:02d}")
        for i in range(2)
    ]
    tells = [registry.get("rht.rhetorical-qa")]

    # Warm the cache for doc-01 only; doc-00 stands in for the failed call.
    warm = make_client(tmp_path, e2e_router)
    scoring.detect_all(docs[1:], tells, judge=JudgeBackend(warm))

    replay = make_client(tmp_path, e2e_router, cache_only=True)
    df = scoring.detect_all(
        docs, tells, judge=JudgeBackend(replay),
        judge_missing_ok=[("rht.rhetorical-qa", "m/doc-00")],
    )
    assert sorted(df[df["method"] == "judge"]["doc_id"]) == ["m/doc-01"]
    errors = list(df.attrs.get("judge_errors") or [])
    assert [e["doc_id"] for e in errors] == ["m/doc-00"]
    assert "never cached" in errors[0]["error"]

    # Without that pair named, the same miss is a missing input and must stop.
    with pytest.raises(CacheMiss):
        scoring.detect_all(
            docs, tells, judge=JudgeBackend(make_client(tmp_path, e2e_router, cache_only=True))
        )


# --- R16: scoped cache invalidation ------------------------------------------

#: sha256 of every judge prompt this repo could render, captured at commit
#: 2335ee3 — the last commit before ruling R16 changed the stage-1 rules for
#: `rht.rule-of-three`. These are the "before" side of the scoping claim, and
#: they cannot be recomputed after the fact, which is why they are literals.
_PROMPT_HASHES_BEFORE_R16: dict[str, dict[str, str]] = {
    "rht.fragment-emphasis": {
        "extraction": "a3dc712de3acfeeb04238bba631c49970e4285e26c9aac85a44cac40d0f351c1",
        "adjudication": "5c8f2f1ab89aa487d91f98ffb738a79ea86af6420f4045b26f1fc01186692e9c",
    },
    "rht.from-x-to-y": {
        "extraction": "22f7544da4cc4d0b002f233ee6137764ba15ae3e206380020f0fa5e5f2cc8571",
        "adjudication": "011572ce7e9da09e6b5407b2e8dbe43d48b82b823738ca4f8e1ca0abbabbada4",
    },
    "rht.rhetorical-qa": {
        "extraction": "192a80f35cffe1545b8efe3820ad58743c8d3c27d2a09aa3928be200f7638d8c",
        "adjudication": "1e7fc73d3bf048b70ae360715c43c3c67611c2dcd82584c930c3bbbd81ecbcdb",
    },
    "rht.rule-of-three": {
        "extraction": "11851bc209bf31d026277672d7817e406d6ed6e7eaabd45a4c8b15b1beffe067",
        "adjudication": "ce4b2e6cae67e4b024a2a71cd3ed793e237e3e8c04784b50711cdbcc9e9274ab",
    },
    "str.parallel-bullet-grammar": {
        "structural": "1c5bf60d2b80ce27f2593589d2b02467fbf608b6a7f3147e3d1d34dac46c0c11",
    },
    "str.summary-sandwich": {
        "structural": "1fd0c997df3adf362e8cace31a417351515658e25269ca6113ce8a533af8f5ab",
    },
    "str.table-overuse": {
        "structural": "d414a72dc2cfd0aea78c7a846c4bf0b6925c6ecfa75ac465bc31e7e32849a1c0",
    },
}

#: Cache keys under the same pre-R16 conditions: a fixed chunk sha, the pinned
#: judge, and each tell's rubric_version as it stood then (rule-of-three at 1).
_CACHE_KEYS_BEFORE_R16: dict[str, dict[str, str]] = {
    "rht.fragment-emphasis": {
        "extract": "9d0c6db560dfdc94924be3a5a793babf1faa1845c56b9d80912bbc6448be6b18",
        "adjudicate": "96c0a7c821798acf6dc448d1ac65a0c1f2132158a70bf3c7d14d75f5cd541478",
    },
    "rht.from-x-to-y": {
        "extract": "7ae9896de2283b984e1b11c332d77459b0825b2dc94368db2f223daa45ea0f9d",
        "adjudicate": "67d546e94b1fafe10a425e4a84966a2981b08955efa755d25ebee7f565a5a16d",
    },
    "rht.rhetorical-qa": {
        "extract": "aea4e924b13ef425407d8799519c30e5e32f53d0c308b18101f2f10355201476",
        "adjudicate": "cce6524e52cfd32af6fc4f9b0f5e9f6ab2103cd5f46dbf220fd5f1d70bc7be7b",
    },
    "rht.rule-of-three": {
        "extract": "74830e916cb8beac8ba07fded129646affe0630675bea9d4dbe495b62c96f7cd",
        "adjudicate": "703abb6dbf638ca520c91bbd635fdaa6fe8b0b58b73a57228d1b1553256a6c3e",
    },
    "str.parallel-bullet-grammar": {
        "structural": "79e141227ef739b44b2561a4865d8326e7936fa746f6af07c1b13c14ff39eb80",
    },
    "str.summary-sandwich": {
        "structural": "ca8bd60077d34b3b75a1d9d40adbc6f527f6961aba77ae932d12967c496dd78b",
    },
    "str.table-overuse": {
        "structural": "136acd0e9b74f624c86ca9ffa412e48c5c43b8e8bf23350a57c0ef9d416739b1",
    },
}

_R16_CHUNK = (
    "Alpha, beta, and gamma. From March to June we moved from intake to "
    "reporting.\n\n- one\n- two\n"
)
_R16_SPAN = "Alpha, beta, and gamma."
_R16_CHUNK_SHA = "a" * 64


def _rendered_prompts(tell: Tell) -> dict[str, str]:
    import hashlib

    rule = protocol.RULES[tell.id]
    if rule.kind == "structural":
        rendered = {"structural": protocol.build_structural_prompt(tell, _R16_CHUNK)}
    else:
        rendered = {
            "extraction": protocol.build_extraction_prompt(tell, _R16_CHUNK),
            "adjudication": protocol.build_adjudication_prompt(
                tell, _R16_SPAN, _R16_CHUNK
            ),
        }
    return {
        name: hashlib.sha256(text.encode("utf-8")).hexdigest()
        for name, text in rendered.items()
    }


def _current_keys(tell: Tell) -> dict[str, str]:
    rule = protocol.RULES[tell.id]
    if rule.kind == "structural":
        return {
            "structural": cache_key(
                _R16_CHUNK_SHA,
                tell.id,
                tell.rubric_version,
                JUDGE_MODEL_DEFAULT,
                STRUCTURAL,
            )
        }
    return {
        "extract": cache_key(
            _R16_CHUNK_SHA, tell.id, tell.rubric_version, JUDGE_MODEL_DEFAULT, EXTRACT
        ),
        "adjudicate": cache_key(
            _R16_CHUNK_SHA,
            tell.id,
            tell.rubric_version,
            JUDGE_MODEL_DEFAULT,
            ADJUDICATE,
            _R16_SPAN,
        ),
    }


def test_r16_invalidates_only_rule_of_three(registry: Registry) -> None:
    """The scoping claim behind R16, checked rather than asserted in prose.

    R16 changed what stage 1 is asked about one tell without bumping
    PROMPT_VERSION, on the argument that the change is per-tell and that tell's
    own rubric_version carries it. That argument is only safe if the other six
    tells still ask byte-identical questions and still land on the same cache
    keys — a prompt that moved without its key moving would serve a stale answer
    to a changed question, which is the one failure a content-addressed cache
    cannot show you.
    """
    for tell_id in protocol.RULES:
        tell = registry.get(tell_id)
        prompts = _rendered_prompts(tell)
        keys = _current_keys(tell)
        before_prompts = _PROMPT_HASHES_BEFORE_R16[tell_id]
        before_keys = _CACHE_KEYS_BEFORE_R16[tell_id]
        if tell_id == "rht.rule-of-three":
            assert tell.rubric_version == 2
            assert prompts["extraction"] != before_prompts["extraction"]
            assert prompts["adjudication"] != before_prompts["adjudication"]
            assert keys["extract"] != before_keys["extract"]
            assert keys["adjudicate"] != before_keys["adjudicate"]
        else:
            assert prompts == before_prompts, f"{tell_id}: the prompt bytes moved"
            assert keys == before_keys, f"{tell_id}: the cache key moved"


def test_only_rule_of_three_replaces_the_recall_first_rules() -> None:
    """Every other tell keeps the standing pair, by construction and by bytes."""
    gated = [tid for tid, rule in protocol.RULES.items() if rule.extraction_rules]
    assert gated == ["rht.rule-of-three"]


def test_the_r16_gate_reaches_the_extraction_prompt(registry: Registry) -> None:
    prompt = protocol.build_extraction_prompt(
        registry.get("rht.rule-of-three"), _R16_CHUNK
    )
    assert "APPLY CRITERION (c) BEFORE YOU PROPOSE" in prompt
    assert "OVER-EXTRACT" not in prompt, "the firehose rule is what R16 replaced"
    assert "an enumeration of real facts" not in prompt
    # Recall-first survives where the extractor cannot tell.
    assert "propose it anyway" in prompt
    # And the exclusions are still withheld: R16 moved an inclusion criterion,
    # not the protocol-v2 split.
    assert "EXCLUSIONS:" not in prompt
    other = protocol.build_extraction_prompt(
        registry.get("rht.fragment-emphasis"), _R16_CHUNK
    )
    assert "OVER-EXTRACT" in other
    assert "APPLY CRITERION (c)" not in other


# --- SHAKEDOWN rec 3: parse failures are counted per stage --------------------


def test_a_parse_failure_is_counted_against_the_stage_that_asked() -> None:
    """§2.4 is a code-reading hypothesis with no observed instances. A counter
    is what turns it into a rate the canonical run can report."""
    cli = fake_cli(envelope("not json at all"), envelope("still not json"))
    transport = CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli)
    with pytest.raises(JudgeError, match="not JSON"):
        transport.ask("go", stage=ADJUDICATE)
    stats = transport.stats.as_dict()
    assert stats["parse_failures"] == {ADJUDICATE: 1}
    assert stats["parse_failures_total"] == 1
    assert stats["retries"] == 1, "the fence retry still happens first"
    assert stats["failures"] == 1


def test_parse_failures_do_not_pool_across_stages() -> None:
    transport = CliJudgeTransport(
        model=JUDGE_MODEL_DEFAULT, transport=fake_cli(envelope("prose"))
    )
    for stage in (EXTRACT, ADJUDICATE, ADJUDICATE, STRUCTURAL):
        with pytest.raises(JudgeError):
            transport.ask("go", stage=stage)
    assert transport.stats.as_dict()["parse_failures"] == {
        ADJUDICATE: 2,
        EXTRACT: 1,
        STRUCTURAL: 1,
    }


def test_a_recovered_parse_failure_is_not_counted() -> None:
    """The fence retry working is not a failure — only the second miss is."""
    cli = fake_cli(envelope('```json\n{"spans": []}\n```'))
    transport = CliJudgeTransport(model=JUDGE_MODEL_DEFAULT, transport=cli)
    assert transport.ask("go", stage=EXTRACT) == {"spans": []}
    assert transport.stats.as_dict()["parse_failures"] == {}


def test_the_client_tells_the_transport_which_stage_it_is_serving(
    tmp_path: Path,
) -> None:
    """The stage reaches the transport through the cache client, and a transport
    that does not want it is asked the plain question."""
    seen: list[str | None] = []

    class Recording:
        model = JUDGE_MODEL_DEFAULT
        accepts_stage = True

        def ask(self, prompt: str, stage: str | None = None) -> dict[str, Any]:
            seen.append(stage)
            return {"spans": []}

    class Plain:
        model = JUDGE_MODEL_DEFAULT

        def ask(self, prompt: str) -> dict[str, Any]:
            return {"spans": []}

    client = JudgeClient(transport=Recording(), cache=JudgeCache(tmp_path / "recording"))
    client.ask(EXTRACT, "a" * 64, "rht.rule-of-three", 2, "prompt")
    client.ask(ADJUDICATE, "a" * 64, "rht.rule-of-three", 2, "prompt", quote="q")
    assert seen == [EXTRACT, ADJUDICATE]

    plain = JudgeClient(transport=Plain(), cache=JudgeCache(tmp_path / "plain"))
    assert plain.ask(EXTRACT, "b" * 64, "rht.rule-of-three", 2, "prompt")[0] == {
        "spans": []
    }


# --- R19: the audit re-asks adjudications too ---------------------------------


def test_the_audit_re_asks_adjudications_and_tables_them_separately(
    tmp_path: Path, qa_tell: Tell
) -> None:
    """SHAKEDOWN §2.7 measured stage 1 only, which overstates the instability of
    a published count: a span that only one call proposes still has to survive
    an adjudicator nobody had re-asked."""
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)
    entries_before = len(client.cache.entries())

    report = audit_mod.audit([doc], [qa_tell], client, pct=100.0)
    kinds = {item.kind for item in report.items}
    assert kinds == {audit_mod.EXTRACTION, audit_mod.ADJUDICATION}
    assert report.kind_summary(audit_mod.ADJUDICATION)["n"] >= 1
    # Same answers replayed by the router, so both stages reproduce exactly.
    assert report.kind_summary(audit_mod.ADJUDICATION)["mean_agreement"] == 1.0
    assert report.mean_agreement == 1.0

    adjudicated = report.per_tell_adjudication()
    assert set(adjudicated) == {qa_tell.id}
    assert adjudicated[qa_tell.id]["n"] == report.kind_summary(
        audit_mod.ADJUDICATION
    )["n"]
    # The stage-1 table is unchanged and does not absorb the stage-2 items.
    assert report.per_tell()[qa_tell.id]["n"] == report.kind_summary(
        audit_mod.EXTRACTION
    )["n"]
    assert "adjudication" in report.summary()
    assert len(client.cache.entries()) == entries_before, "an audit must not write"


def test_an_adjudication_disagreement_is_all_or_nothing(
    tmp_path: Path, qa_tell: Tell
) -> None:
    """Agreement is verdict AND criteria AND exclusion: two calls that reach the
    same answer by different criteria did not reproduce the measurement."""
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)

    def drifted(prompt: str) -> dict[str, Any] | None:
        if "ADJUDICATE ONE SPAN" in prompt:
            return {
                "instance": True,
                "criteria_met": ["a"],
                "exclusion_triggered": None,
                "rationale": "changed my mind",
            }
        return e2e_router(prompt)

    client.transport.router = drifted
    report = audit_mod.audit([doc], [qa_tell], client, pct=100.0)
    items = report.of_kind(audit_mod.ADJUDICATION)
    assert items, "there is at least one adjudication in the cache to re-ask"
    for item in items:
        assert item.agreement in {0.0, 1.0}
        assert item.quote
        assert item.live_criteria == ["a"]
    assert any(item.agreement == 0.0 for item in items)
    assert report.per_tell_adjudication()[qa_tell.id]["mean_agreement"] < 1.0


def test_only_adjudications_the_run_paid_for_are_auditable(
    tmp_path: Path, qa_tell: Tell
) -> None:
    """A span dispositioned in code or dropped by the cap has no cached answer,
    so it never enters the pool — the audit re-asks questions that were asked."""
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)

    cached_adjudications = sum(
        1
        for path in client.cache.entries()
        if (client.cache.read(path) or {}).get("stage") == ADJUDICATE
    )
    report = audit_mod.audit([doc], [qa_tell], client, pct=100.0)
    assert report.kind_summary(audit_mod.ADJUDICATION)["n"] == cached_adjudications


def test_the_budget_cap_covers_both_stages_together(
    tmp_path: Path, qa_tell: Tell
) -> None:
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)

    full = audit_mod.audit([doc], [qa_tell], client, pct=100.0)
    assert full.n_available >= 2
    capped = audit_mod.audit([doc], [qa_tell], client, pct=100.0, max_calls=1)
    assert capped.n_sampled == 1
    assert capped.capped is True
    assert capped.max_calls == 1


def test_the_audit_can_be_asked_for_one_stage_only(
    tmp_path: Path, qa_tell: Tell
) -> None:
    doc = doc_from(E2E_DOC)
    client = make_client(tmp_path, e2e_router)
    JudgeBackend(client).detect(qa_tell, doc)

    only_extraction = audit_mod.audit(
        [doc], [qa_tell], client, pct=100.0, stages=(audit_mod.EXTRACTION,)
    )
    assert {i.kind for i in only_extraction.items} == {audit_mod.EXTRACTION}
    only_adjudication = audit_mod.audit(
        [doc], [qa_tell], client, pct=100.0, stages=(audit_mod.ADJUDICATION,)
    )
    assert {i.kind for i in only_adjudication.items} == {audit_mod.ADJUDICATION}


def test_the_draw_round_robins_over_stages_as_well_as_tells() -> None:
    """A tell with a deep adjudication pool must not crowd out its own
    extractions, or another tell's."""
    from telltale.registry import Tell as RegistryTell

    def entry(tell_id: str, stage: str, i: int):
        tell = RegistryTell(id=tell_id, name=tell_id, category="rhetorical", method="judge")
        return (tell, f"m/doc-{i:02d}", None, stage, {}, None)

    available = (
        [entry("deep", "adjudicate", i) for i in range(40)]
        + [entry("deep", "extract", i) for i in range(4)]
        + [entry("thin", "extract", i) for i in range(4)]
    )
    picks = audit_mod._stratified_picks(available, 9, seed=11)
    pools = [f"{available[i][0].id}|{available[i][3]}" for i in picks]
    assert set(pools) == {"deep|adjudicate", "deep|extract", "thin|extract"}
    assert pools.count("deep|adjudicate") == 3, "one pool cannot take the budget"
