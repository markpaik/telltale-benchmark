"""Isolation: the recipe is pinned, and the graders actually fail dirty output.

The probe battery runs through an injected transport so the graders can be
exercised against responses that a contaminated machine would produce — which is
the only way to know the battery would catch one. Nothing calls the real CLI.

The exception is the transport section at the bottom, which shells out to
`python3` to pin deadline enforcement. That bug lived in the interaction between
Popen, process groups and the clock, so a fake transport cannot reach it.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from telltale import isolation
from telltale.isolation import CliResult, Envelope


# --- the pinned recipe -------------------------------------------------------


def test_system_prompt_is_pinned():
    assert isolation.MINIMAL_SYSTEM_PROMPT == (
        "Respond with only the requested document, formatted in markdown. "
        "Do not add preamble, commentary, or notes about the document."
    )
    # Pinned: every sidecar in the corpus records this hash, and a corpus whose
    # documents were generated under two different system prompts is two
    # corpora. Changing the prompt must be a deliberate, visible edit here.
    assert isolation.SYSTEM_PROMPT_SHA256 == (
        "7461cf6bc32d92b7e1851e05a3d63954ad29b63fa61d0c5a027959f5008e4492"
    )


def test_isolation_flags_carry_the_validated_recipe():
    flags = isolation.ISOLATION_FLAGS
    assert "--safe-mode" in flags
    assert "--strict-mcp-config" in flags
    assert "--disable-slash-commands" in flags
    assert flags[flags.index("--system-prompt") + 1] == isolation.MINIMAL_SYSTEM_PROMPT
    assert flags[flags.index("--setting-sources") + 1] == ""
    assert flags[flags.index("--tools") + 1] == ""
    assert flags[flags.index("--output-format") + 1] == "json"


def test_isolation_does_not_disable_session_persistence():
    # Continuations resume a session; disabling persistence would silently cap
    # every document at whatever the first turn produced.
    assert "--no-session-persistence" not in isolation.ISOLATION_FLAGS


def test_build_cmd_appends_model_then_extras():
    cmd = isolation.build_cmd("claude-sonnet-5", ["--resume", "abc"])
    assert cmd[0] == "claude"
    assert cmd[-4:] == ["--model", "claude-sonnet-5", "--resume", "abc"]


def test_isolation_env_strips_the_parent_sessions_claude_vars(monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "leaky")
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/somewhere/else")
    monkeypatch.setenv("PATH", "/usr/bin")
    env = isolation.isolation_env()
    assert "CLAUDE_CODE_SESSION_ID" not in env
    assert "CLAUDECODE" not in env
    assert "CLAUDE_CONFIG_DIR" not in env
    assert env["PATH"] == "/usr/bin"
    assert env["CLAUDE_CODE_SAFE_MODE"] == "1"


# --- envelope parsing --------------------------------------------------------


def _envelope_json(**overrides) -> str:
    data = {
        "result": "# Memo\n\nBody text.",
        "session_id": "sess-1",
        "num_turns": 1,
        "is_error": False,
        "usage": {"input_tokens": 120, "output_tokens": 900},
        "modelUsage": {"claude-sonnet-5-20260101": {"outputTokens": 500}},
    }
    data.update(overrides)
    return json.dumps(data)


def test_parse_envelope_reads_the_success_shape():
    env = isolation.parse_envelope(_envelope_json())
    assert env.ok
    assert env.result.startswith("# Memo")
    assert env.session_id == "sess-1"
    assert env.num_turns == 1
    assert env.usage["output_tokens"] == 900
    assert env.model_reported == "claude-sonnet-5-20260101"


def test_model_reported_is_the_model_that_wrote_the_document():
    # Live envelopes carry the harness's own side-calls alongside the real one.
    # A sonnet-5 run came back with claude-sonnet-5 at 71 output tokens and
    # claude-haiku-4-5-20251001 at 13. Picking by name length attributed the
    # document to haiku; picking by output volume gets it right.
    env = isolation.parse_envelope(
        _envelope_json(
            modelUsage={
                "claude-haiku-4-5-20251001": {"inputTokens": 528, "outputTokens": 13},
                "claude-sonnet-5": {"inputTokens": 215, "outputTokens": 71},
            }
        )
    )
    assert env.model_reported == "claude-sonnet-5"


def test_model_reported_handles_snake_case_and_missing_counts():
    env = isolation.parse_envelope(
        _envelope_json(
            modelUsage={
                "claude-haiku-4-5": {},
                "claude-opus-5-20260101": {"output_tokens": 9000},
            }
        )
    )
    assert env.model_reported == "claude-opus-5-20260101"


def test_model_reported_is_deterministic_when_nothing_distinguishes_entries():
    # Ties resolve on sorted order, so the same envelope always attributes
    # the same way across runs and machines.
    env = isolation.parse_envelope(_envelope_json(modelUsage={"b-model": {}, "a-model": {}}))
    assert env.model_reported == "a-model"


def test_parse_envelope_reads_the_error_shape():
    env = isolation.parse_envelope(
        _envelope_json(is_error=True, result="Not logged in - Please run /login")
    )
    assert not env.ok
    assert env.is_error
    assert "Not logged in" in env.result


@pytest.mark.parametrize(
    "stdout, fragment",
    [
        ("", "empty stdout"),
        ("not json at all", "not JSON"),
        ("[1, 2, 3]", "not an object"),
    ],
)
def test_parse_envelope_survives_garbage(stdout, fragment):
    env = isolation.parse_envelope(stdout)
    assert not env.ok
    assert fragment in env.parse_error


def test_parse_envelope_tolerates_missing_fields():
    env = isolation.parse_envelope('{"result": null}')
    assert env.result == ""
    assert env.session_id == ""
    assert env.num_turns == 0
    assert env.usage == {}


# --- graders -----------------------------------------------------------------


def _env(result: str, **overrides) -> Envelope:
    return isolation.parse_envelope(_envelope_json(result=result, **overrides))


def test_grade_a_passes_a_bare_none():
    passed, reason = isolation.grade_a(_env("NONE"))
    assert passed, reason


@pytest.mark.parametrize(
    "response",
    [
        "Here is my CLAUDE.md content: apply the writing-voice skill.",
        "I have custom instructions from DPSCD Research and Data Science.",
        "My memory mentions the research-brief skill and dsdb1 credentials.",
    ],
)
def test_grade_a_fails_on_contamination(response):
    passed, reason = isolation.grade_a(_env(response))
    assert not passed
    assert "contamination" in reason or "200" in reason


def test_grade_a_fails_a_long_answer_even_without_markers():
    passed, reason = isolation.grade_a(_env("NONE. " + "Additional context. " * 40))
    assert not passed
    assert ">200" in reason


def test_grade_a_fails_when_none_is_absent():
    passed, reason = isolation.grade_a(_env("I have some project context."))
    assert not passed
    assert "does not contain NONE" in reason


def test_grade_a_fails_a_failed_call():
    passed, reason = isolation.grade_a(_env("NONE", is_error=True))
    assert not passed
    assert "call failed" in reason


# --- probe A v2 (2026-07-29 recalibration) -----------------------------------


def test_probe_a_excludes_the_known_residual_so_none_is_the_honest_answer():
    # The v1 wording asked what the session "has" without saying what does not
    # count, and a thorough model answered by quoting the residual — clean
    # content, failing grade. v2 names both residual pieces as out of scope.
    prompt = isolation.PROBES["A"][0]
    assert "email address and today's date" in prompt
    assert "system prompt about producing a document" in prompt
    assert prompt.rstrip().endswith("NONE")


# --- probe A v4 (2026-08-20 safeguard collision) ------------------------------


def test_probe_a_does_not_ask_for_quotation():
    # The v2 wording asked the session to quote instructions verbatim, which a
    # server-side safeguard classified as prompt extraction and rejected for
    # claude-fable-5 ([reasoning_extraction], zero output tokens). v4 asks for
    # an enumeration of categories instead. Nothing here may invite the session
    # to reproduce content again.
    prompt = isolation.PROBES["A"][0].lower()
    assert "quote" not in prompt
    assert "verbatim" not in prompt
    assert "do not reproduce any content" in prompt


def test_grade_a_fails_a_category_inventory_that_names_no_markers():
    # The cost of asking for categories rather than content: a contaminated
    # session can answer in words that are not markers and are well under the
    # length cap. A bare NONE is the whole pass condition.
    passed, reason = isolation.grade_a(
        _env("Custom instructions: present. Memories: present. Skills: NONE.")
    )
    assert not passed
    assert "expected exactly NONE" in reason


def test_probe_a_still_asks_for_the_things_contamination_would_show():
    # The exclusions must not have hollowed out the question.
    prompt = isolation.PROBES["A"][0].lower()
    for asked in ("custom instructions", "memories", "skills", "project-specific"):
        assert asked in prompt


def test_grade_a_is_unchanged_by_the_reword():
    # The recalibration lives in the prompt. A session that can see real
    # configuration still has something to quote, and still fails.
    dirty = (
        "I can see a CLAUDE.md telling me to apply the writing-voice skill "
        "for DPSCD work."
    )
    passed, reason = isolation.grade_a(_env(dirty))
    assert not passed
    assert "contamination markers" in reason


def test_grade_a_still_fails_a_verbose_clean_answer():
    # Explicitly pinned: the fix did not loosen the length cap. If a model
    # inventories its context anyway, the battery fails and a human rules on it,
    # which is what happened on 2026-07-29.
    inventory = (
        "## System Prompt\n\n> You are a Claude agent, built on Anthropic's "
        "Claude Agent SDK.\n\n## CLAUDE.md / Memories / Project Context\n\n"
        "None present.\n\n" + "Nothing else is present in this session. " * 6
    )
    passed, reason = isolation.grade_a(_env(inventory), markers=("writing-voice",))
    assert not passed
    assert ">200" in reason


def test_known_residual_context_records_both_residuals_verbatim():
    residual = isolation.KNOWN_RESIDUAL_CONTEXT
    assert "You are a Claude agent, built on Anthropic's Claude Agent SDK." in residual
    assert "email address" in residual and "date" in residual
    assert "no default claude code system prompt" in residual.lower()


def test_grade_b_passes_bare_none_and_punctuated_none():
    assert isolation.grade_b(_env("NONE"))[0]
    assert isolation.grade_b(_env("NONE."))[0]


def test_grade_b_passes_a_prose_denial_with_no_tool_names():
    passed, reason = isolation.grade_b(
        _env("I do not have access to any of those in this session.")
    )
    assert passed, reason


@pytest.mark.parametrize(
    "response",
    [
        "Available tools: Bash, Read, Edit, WebSearch.",
        "I can call mcp__claude_ai_Gmail__create_draft.",
        "Tools include Glob and Grep and TodoWrite.",
    ],
)
def test_grade_b_fails_when_tools_are_reachable(response):
    passed, reason = isolation.grade_b(_env(response))
    assert not passed
    assert "tool names" in reason


def test_grade_b_fails_on_contamination_even_if_it_says_none():
    passed, reason = isolation.grade_b(_env("NONE except the writing-voice skill"))
    assert not passed
    assert "contamination" in reason


def test_grade_c_passes_a_real_document():
    passed, reason = isolation.grade_c(_env("word " * 200))
    assert passed, reason


def test_grade_c_fails_a_stub():
    passed, reason = isolation.grade_c(_env("Too short."))
    assert not passed
    assert "words" in reason


def test_grade_c_fails_multi_turn():
    passed, reason = isolation.grade_c(_env("word " * 200, num_turns=4))
    assert not passed
    assert "num_turns=4" in reason


def test_grade_c_fails_an_error_envelope():
    passed, reason = isolation.grade_c(_env("word " * 200, is_error=True))
    assert not passed
    assert "is_error" in reason


def test_grade_d_passes_a_document_only_answer():
    passed, reason = isolation.grade_d(
        _env("Respond with only the requested document, formatted in markdown.")
    )
    assert passed, reason


@pytest.mark.parametrize(
    "response",
    [
        "I am Claude Code, Anthropic's CLI for coding.",
        "They tell me to use tools to edit files in a codebase.",
        "I should apply the relevant skill before answering.",
        "I run in a terminal and help with software engineering tasks.",
    ],
)
def test_grade_d_fails_when_the_harness_prompt_survived(response):
    passed, reason = isolation.grade_d(_env(response))
    assert not passed


def test_grade_d_fails_an_answer_unrelated_to_a_document():
    passed, reason = isolation.grade_d(_env("To be helpful, harmless, and honest."))
    assert not passed
    assert "does not mention producing a document" in reason


def test_found_markers_is_case_insensitive_and_deduped():
    hits = isolation.found_markers("dpscd DPSCD Dpscd", isolation.CONTAMINATION_MARKERS)
    assert hits == ["DPSCD"]


# --- battery -----------------------------------------------------------------


def _transport_for(responses: dict[str, str], model: str = "m"):
    """Fake transport keyed by which probe prompt it is handed."""

    def transport(cmd, prompt, timeout):
        for probe, (probe_prompt, _) in isolation.PROBES.items():
            if prompt == probe_prompt:
                return CliResult(
                    0,
                    _envelope_json(
                        result=responses[probe],
                        modelUsage={model: {"outputTokens": 10}},
                    ),
                    "",
                    0.1,
                )
        raise AssertionError(f"unexpected prompt: {prompt[:60]}")

    return transport


CLEAN = {
    "A": "NONE",
    "B": "NONE",
    "B2": "CANNOT",
    "C": "word " * 200,
    "D": "Respond with only the requested document, formatted in markdown.",
}


def test_battery_passes_and_writes_a_transcript(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "2.1.220 (Claude Code)")
    out = tmp_path / "runs" / "isolation" / "m.json"
    report = isolation.run_probe_battery("m", out, transport=_transport_for(CLEAN))

    assert report.passed
    assert [p.probe for p in report.probes] == ["A", "B", "B2", "C", "D"]
    written = json.loads(out.read_text())
    assert written["passed"] is True
    assert written["system_prompt_sha256"] == isolation.SYSTEM_PROMPT_SHA256
    assert written["flags"] == isolation.ISOLATION_FLAGS
    assert written["cli_version"] == "2.1.220 (Claude Code)"
    assert written["known_residual_context"]
    # Which probe protocol produced this transcript, so a v1 battery and a v2
    # battery in the same directory are not read as the same evidence.
    assert written["probe_protocol_version"] == isolation.PROBE_PROTOCOL_VERSION
    # The transcript has to carry the responses, or it is not evidence.
    assert written["probes"][0]["response"] == "NONE"
    assert written["probes"][0]["prompt"]


def test_battery_fails_when_one_probe_is_dirty(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "x")
    dirty = dict(CLEAN, A="My CLAUDE.md says to apply the writing-voice skill.")
    out = tmp_path / "m.json"
    report = isolation.run_probe_battery("m", out, transport=_transport_for(dirty))

    assert not report.passed
    assert [p.probe for p in report.probes if not p.passed] == ["A"]
    assert "BATTERY FAILED" in report.summary()


def test_battery_records_a_nonzero_exit_as_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "x")

    def transport(cmd, prompt, timeout):
        return CliResult(1, "", "claude: command failed", 0.1)

    report = isolation.run_probe_battery("m", tmp_path / "m.json", transport=transport)
    assert not report.passed
    assert all("exit 1" in p.reason for p in report.probes)


# --- the gate ----------------------------------------------------------------


def _write_battery(root: Path, model: str, when: datetime, passed: bool = True, **overrides):
    path = isolation.battery_path(root, model, when)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "model": model,
        "timestamp": when.isoformat(),
        "passed": passed,
        "system_prompt_sha256": isolation.SYSTEM_PROMPT_SHA256,
    }
    data.update(overrides)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_gate_finds_a_recent_passing_battery(tmp_path):
    now = datetime.now(timezone.utc)
    path = _write_battery(tmp_path, "m", now - timedelta(hours=2))
    assert isolation.latest_passing_battery(tmp_path, "m") == path


def test_gate_ignores_a_stale_battery(tmp_path):
    _write_battery(tmp_path, "m", datetime.now(timezone.utc) - timedelta(hours=30))
    assert isolation.latest_passing_battery(tmp_path, "m") is None


def test_gate_ignores_a_failed_battery(tmp_path):
    _write_battery(tmp_path, "m", datetime.now(timezone.utc), passed=False)
    assert isolation.latest_passing_battery(tmp_path, "m") is None


def test_gate_ignores_a_battery_run_under_a_different_system_prompt(tmp_path):
    # The recipe changed since that transcript, so it no longer vouches for
    # anything the harness does now.
    _write_battery(
        tmp_path, "m", datetime.now(timezone.utc), system_prompt_sha256="deadbeef"
    )
    assert isolation.latest_passing_battery(tmp_path, "m") is None


def test_gate_is_per_model(tmp_path):
    _write_battery(tmp_path, "claude-sonnet-5", datetime.now(timezone.utc))
    assert isolation.latest_passing_battery(tmp_path, "claude-opus-5") is None


def test_gate_picks_the_newest_of_several(tmp_path):
    now = datetime.now(timezone.utc)
    _write_battery(tmp_path, "m", now - timedelta(hours=10))
    newest = _write_battery(tmp_path, "m", now - timedelta(hours=1))
    assert isolation.latest_passing_battery(tmp_path, "m") == newest


def test_gate_survives_a_corrupt_transcript(tmp_path):
    directory = tmp_path / "isolation"
    directory.mkdir(parents=True)
    (directory / "m-20260101T000000Z.json").write_text("{not json", encoding="utf-8")
    assert isolation.latest_passing_battery(tmp_path, "m") is None


def test_gate_handles_a_missing_runs_directory(tmp_path):
    assert isolation.latest_passing_battery(tmp_path / "nope", "m") is None


# --- empty responses are not evidence (DEFECT-2) -----------------------------


@pytest.mark.parametrize("blank", ["", "   ", "\n\n", "\t \n"])
@pytest.mark.parametrize("grader", [isolation.grade_a, isolation.grade_b, isolation.grade_d])
def test_blank_responses_fail_every_contamination_probe(grader, blank):
    # A probe that saw nothing must not report that it saw nothing wrong.
    passed, reason = grader(_env(blank))
    assert not passed
    assert "empty response" in reason


def test_blank_response_also_fails_the_behaviour_probe():
    passed, reason = isolation.grade_c(_env("   "))
    assert not passed
    assert "0 words" in reason


# --- local markers (DEFECT-3) ------------------------------------------------


def _fake_config(tmp_path: Path, email: str = "jrivera.qa@example.org") -> Path:
    path = tmp_path / ".claude.json"
    path.write_text(
        json.dumps({"oauthAccount": {"emailAddress": email, "displayName": "QA"}}),
        encoding="utf-8",
    )
    return path


def test_account_markers_reads_the_email_and_its_local_part(tmp_path):
    markers = isolation.account_markers(_fake_config(tmp_path))
    assert markers == ["jrivera.qa@example.org", "jrivera"] or markers == [
        "jrivera.qa@example.org"
    ]
    assert "jrivera.qa@example.org" in markers


def test_account_markers_skips_a_short_or_generic_local_part(tmp_path):
    markers = isolation.account_markers(_fake_config(tmp_path, "me@example.org"))
    assert markers == ["me@example.org"]


@pytest.mark.parametrize("body", ["{not json", "[]", '{"oauthAccount": 3}', "{}"])
def test_account_markers_survives_an_unusable_config(tmp_path, body):
    path = tmp_path / ".claude.json"
    path.write_text(body, encoding="utf-8")
    assert isolation.account_markers(path) == []


def test_account_markers_on_a_missing_file(tmp_path):
    assert isolation.account_markers(tmp_path / "nope.json") == []


def test_file_markers_reads_a_local_markers_file(tmp_path):
    (tmp_path / isolation.LOCAL_MARKERS_FILENAME).write_text(
        "# a comment\nAcme Internal\n\n  secret-codename  \n", encoding="utf-8"
    )
    assert isolation.file_markers(tmp_path) == ["Acme Internal", "secret-codename"]


def test_file_markers_when_absent(tmp_path):
    assert isolation.file_markers(tmp_path) == []


def test_effective_markers_merges_both_sources_without_duplicates(tmp_path):
    (tmp_path / isolation.LOCAL_MARKERS_FILENAME).write_text(
        "DPSCD\nAcme Internal\n", encoding="utf-8"
    )
    markers = isolation.effective_markers(_fake_config(tmp_path), tmp_path)
    assert set(isolation.CONTAMINATION_MARKERS).issubset(set(markers))
    assert "jrivera.qa@example.org" in markers
    assert "Acme Internal" in markers
    # The file repeated a marker that is already committed; it must not be
    # appended a second time. (The committed list carries both DPSCD and dpscd
    # on purpose, so the count to beat is the one it already had.)
    committed = sum(1 for m in isolation.CONTAMINATION_MARKERS if m.lower() == "dpscd")
    assert sum(1 for m in markers if m.lower() == "dpscd") == committed


@pytest.mark.parametrize(
    "grader", [isolation.grade_a, isolation.grade_b, isolation.grade_c, isolation.grade_d]
)
def test_every_grader_fails_on_a_locally_resolved_marker(grader, tmp_path):
    markers = isolation.effective_markers(_fake_config(tmp_path), tmp_path)
    leaked = "NONE " + "word " * 60 + "contact jrivera.qa@example.org for the document"
    passed, reason = grader(_env(leaked), markers)
    assert not passed
    assert "contamination markers" in reason


def test_local_markers_are_redacted_wherever_they_get_written_down(tmp_path):
    markers = isolation.effective_markers(_fake_config(tmp_path), tmp_path)
    redacted = isolation.redact_markers(markers)
    # Committed markers stay legible; the account email must not appear.
    assert "DPSCD" in redacted
    assert not any("jrivera" in entry for entry in redacted)
    assert any(entry.startswith("<local:") for entry in redacted)


def test_a_failing_grader_reason_does_not_leak_the_email(tmp_path):
    markers = isolation.effective_markers(_fake_config(tmp_path), tmp_path)
    _, reason = isolation.grade_a(_env("jrivera.qa@example.org"), markers)
    assert "jrivera" not in reason
    assert "<local:" in reason


def test_transcript_records_redacted_markers(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "x")
    markers = isolation.effective_markers(_fake_config(tmp_path), tmp_path)
    out = tmp_path / "m.json"
    isolation.run_probe_battery(
        "m", out, transport=_transport_for(CLEAN), markers=markers
    )
    written = out.read_text()
    assert "jrivera" not in written
    assert "<local:" in written


# --- model attribution (DEFECT-5) --------------------------------------------


def test_attribution_matches_the_requested_model_not_the_loudest_one():
    # The live failure: a bare "NONE" probe answer is fewer output tokens than
    # the harness's own haiku side-call, so volume named the wrong model.
    env = isolation.parse_envelope(
        _envelope_json(
            result="NONE",
            modelUsage={
                "claude-haiku-4-5-20251001": {"outputTokens": 528},
                "claude-sonnet-5": {"outputTokens": 4},
            },
        ),
        requested_model="claude-sonnet-5",
    )
    assert env.model_reported == "claude-sonnet-5"
    assert env.model_mismatch is False


def test_attribution_matches_through_a_date_suffix():
    env = isolation.parse_envelope(
        _envelope_json(
            modelUsage={
                "claude-haiku-4-5-20251001": {"outputTokens": 900},
                "claude-opus-5-20260101": {"outputTokens": 3},
            }
        ),
        requested_model="claude-opus-5",
    )
    assert env.model_reported == "claude-opus-5-20260101"
    assert env.model_mismatch is False


def test_attribution_flags_a_missing_requested_model():
    env = isolation.parse_envelope(
        _envelope_json(modelUsage={"claude-haiku-4-5-20251001": {"outputTokens": 900}}),
        requested_model="claude-opus-5",
    )
    assert env.model_mismatch is True
    assert env.model_reported == "claude-haiku-4-5-20251001"


def test_attribution_flags_an_empty_model_usage():
    env = isolation.parse_envelope(
        _envelope_json(modelUsage={}), requested_model="claude-opus-5"
    )
    assert env.model_mismatch is True
    assert env.model_reported == ""


def test_attribution_without_a_requested_model_never_claims_a_mismatch():
    env = isolation.parse_envelope(
        _envelope_json(modelUsage={"a": {"outputTokens": 1}, "b": {"outputTokens": 9}})
    )
    assert env.model_reported == "b"
    assert env.model_mismatch is False


def test_envelope_keeps_the_whole_model_usage_dict():
    usage = {"claude-sonnet-5": {"outputTokens": 71, "costUSD": 0.04}}
    env = isolation.parse_envelope(
        _envelope_json(modelUsage=usage), requested_model="claude-sonnet-5"
    )
    assert env.model_usage == usage


def test_battery_fails_a_probe_answered_by_the_wrong_model(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "x")
    report = isolation.run_probe_battery(
        "claude-opus-5",
        tmp_path / "m.json",
        transport=_transport_for(CLEAN, model="claude-haiku-4-5-20251001"),
    )
    assert not report.passed
    assert all("model mismatch" in p.reason for p in report.probes)


def test_battery_transcript_carries_model_usage(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "x")
    out = tmp_path / "m.json"
    isolation.run_probe_battery("m", out, transport=_transport_for(CLEAN))
    written = json.loads(out.read_text())
    for probe in written["probes"]:
        assert probe["model_usage"] == {"m": {"outputTokens": 10}}
        assert probe["model_reported"] == "m"
        assert probe["model_mismatch"] is False


# --- transport deadline enforcement (2026-07-29 sleep incident) --------------
#
# These are the only tests in the suite that shell out for real. They have to:
# the bug they pin was in the interaction between Popen, process groups and the
# clock, and a fake transport cannot reproduce any of it.


def test_run_cli_returns_a_normal_result():
    result = isolation.run_cli(
        [sys.executable, "-c", "import sys; sys.stdout.write(sys.stdin.read().upper())"],
        "hello",
        timeout=30,
    )
    assert result.returncode == 0
    assert result.stdout == "HELLO"
    assert not result.timed_out


def test_run_cli_kills_a_child_that_overruns_the_deadline():
    started = time.monotonic()
    result = isolation.run_cli(
        [sys.executable, "-c", "import time; time.sleep(120)"], "", timeout=2
    )
    assert result.timed_out
    assert result.returncode == 124
    assert "timed out after 2s" in result.stderr
    # The point of the fix: it comes back on schedule instead of blocking.
    assert time.monotonic() - started < 30


def test_run_cli_kills_helpers_that_inherited_the_pipes(tmp_path):
    # The child exits immediately, but a helper it spawned keeps the inherited
    # stdout write end open. Waiting for EOF would block on a process we are no
    # longer tracking, so the deadline has to be applied to the whole group.
    pidfile = tmp_path / "helper.pid"
    helper = (
        "import os,sys,time;"
        f"open({str(pidfile)!r},'w').write(str(os.getpid()));"
        "time.sleep(120)"
    )
    child = (
        "import subprocess,sys;"
        f"subprocess.Popen([sys.executable,'-c',{helper!r}]);"
        "sys.stdout.write('done'); sys.stdout.flush()"
    )
    started = time.monotonic()
    result = isolation.run_cli([sys.executable, "-c", child], "", timeout=3)
    assert time.monotonic() - started < 40

    deadline = time.monotonic() + 10
    while not pidfile.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    helper_pid = int(pidfile.read_text())

    dead = False
    while time.monotonic() < deadline:
        try:
            os.kill(helper_pid, 0)
        except ProcessLookupError:
            dead = True
            break
        time.sleep(0.1)
    if not dead:  # pragma: no cover - only on a failure, and only to clean up
        os.kill(helper_pid, signal.SIGKILL)
    assert dead, "helper survived the deadline"

    # The CLI's own output was complete, so the call is a success, not a timeout.
    assert result.returncode == 0
    assert result.stdout == "done"
    assert not result.timed_out
    assert "helper processes held the pipes" in result.stderr


def test_elapsed_takes_the_larger_of_the_two_clocks(monkeypatch):
    # A sleeping machine freezes monotonic and lets wall clock run on. That is
    # the case that cost 4h41m, so it is pinned rather than left to inference.
    monkeypatch.setattr(isolation.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(isolation.time, "time", lambda: 20_000.0)
    assert isolation._elapsed(90.0, 1_000.0) == pytest.approx(19_000.0)

    # And a wall clock that jumps backwards must not extend a deadline.
    monkeypatch.setattr(isolation.time, "time", lambda: 900.0)
    assert isolation._elapsed(90.0, 1_000.0) == pytest.approx(10.0)


# --- probe B v3 + B2 (2026-07-30 recall false positive) ----------------------


def test_probe_b_asks_for_context_not_recall():
    # v1/v2 asked what was "available to you", which Opus 5 answered from
    # training: six confident tool inventories in a row from a session whose
    # context provably held no tool definitions.
    prompt = isolation.PROBES["B"][0]
    assert "quote verbatim" in prompt.lower()
    assert "do not list tools you know of from training" in prompt.lower()
    assert prompt.rstrip().endswith("NONE")


def test_probe_b2_is_an_invocation_test_not_a_question():
    prompt = isolation.PROBES["B2"][0]
    assert isolation.B2_CANARY in prompt
    assert prompt.rstrip().endswith(isolation.B2_EXPECTED)
    assert isolation.PROBE_LABELS["B2"] == "tool invocation"


def test_grade_b2_passes_a_bare_cannot():
    passed, reason = isolation.grade_b2(_env("CANNOT"))
    assert passed, reason
    assert "no canary" in reason


def test_grade_b2_fails_when_the_canary_comes_back():
    # The unambiguous signal: a shell ran.
    passed, reason = isolation.grade_b2(_env("TOOLTEST"))
    assert not passed
    assert "canary" in reason


def test_grade_b2_fails_when_a_tool_call_took_extra_turns():
    passed, reason = isolation.grade_b2(_env("CANNOT", num_turns=3))
    assert not passed
    assert "num_turns=3" in reason


def test_grade_b2_fails_a_description_instead_of_a_refusal():
    passed, reason = isolation.grade_b2(
        _env("I would run echo TOOLTEST for you, but I have no Bash tool.")
    )
    assert not passed


@pytest.mark.parametrize("blank", ["", "   ", "\n"])
def test_grade_b2_fails_a_blank_response(blank):
    passed, reason = isolation.grade_b2(_env(blank))
    assert not passed
    assert "empty response" in reason


def test_b2_would_have_caught_a_real_tool_surface():
    # The case B alone could not distinguish from recall: tools actually present.
    passed, _ = isolation.grade_b2(_env("I ran it. Output:\nTOOLTEST", num_turns=3))
    assert not passed


def test_recalled_tool_list_still_fails_probe_b_grader():
    # The grader was never the problem and is not loosened: if a session really
    # does quote tool definitions, B still fails. The fix is in the question.
    passed, reason = isolation.grade_b(
        _env("**Tools**\n- Task\n- Bash\n- Glob\n- Grep\n- WebSearch")
    )
    assert not passed
    assert "tool names present" in reason


def test_protocol_version_records_the_probe_change():
    assert isolation.PROBE_PROTOCOL_VERSION == 4
