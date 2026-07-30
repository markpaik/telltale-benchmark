"""Generation: the loop, the floor, the skip, the sidecar, and the gate.

Every CLI call goes through an injected transport, so nothing here spends money
or needs a network. The fakes return the same JSON envelope shape the real CLI
emits, taken from a live run.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

from telltale import generate, isolation, prompts
from telltale.corpus import FORMATS, load_corpus
from telltale.isolation import CliResult

WORDS = "The committee reviewed the quarterly figures for the northern region. "


# --- fixtures ----------------------------------------------------------------


def envelope(result: str, session_id="sess-1", num_turns=1, is_error=False, **extra) -> str:
    data = {
        "result": result,
        "session_id": session_id,
        "num_turns": num_turns,
        "is_error": is_error,
        "usage": {"input_tokens": 100, "output_tokens": 500},
        "modelUsage": {"claude-sonnet-5-20260101": {"outputTokens": 500}},
    }
    data.update(extra)
    return json.dumps(data)


# Synthetic banks need a unique cast per scenario, same as the real one: the
# lint that catches reused characters would otherwise fire on the fixture.
_FIRSTS = ["Dana", "Omar", "Ingrid", "Kofi", "Mei", "Rafael", "Nadia", "Tomas",
           "Yuki", "Astrid", "Hassan", "Lucia", "Bjorn", "Amara"]
_LASTS = ["Okonjo", "Vasquez", "Lindqvist", "Marchetti", "Osei", "Nakamura",
          "Ferreira", "Sorensen"]
_PLACES = ["Erie", "Dover", "Salem", "Rome", "Athens", "Marion", "Auburn",
           "Newton", "Clinton", "Franklin", "Madison", "Monroe", "Oxford", "Troy"]


def _scenario(fmt_index: int, position: int) -> str:
    """A unique-cast filler scenario long enough to pass the length checks."""
    person = f"{_FIRSTS[fmt_index % 14]} {_LASTS[(position - 1) % 8]}"
    org = f"{_PLACES[fmt_index % 14]}{position} Freight"
    filler = (
        "The team reviewed the quarterly figures and agreed on a plan for the "
        "next period, which covers 41,200 units against a 45,000 unit target. "
    )
    return f"{org} employs 312 people and {person} runs the site. " + filler * 12


@pytest.fixture
def bank_dir(tmp_path) -> Path:
    directory = tmp_path / "formats"
    directory.mkdir()
    for index, fmt in enumerate(FORMATS):
        (directory / f"{fmt}.yaml").write_text(
            yaml.safe_dump(
                {
                    "format": fmt,
                    "bundle": fmt in prompts.BUNDLE_FORMATS,
                    "target_words": 5000,
                    "min_words": 4500,
                    "output_convention": "One document, written as the format is normally written.",
                    "prompts": [
                        {
                            "id": f"{fmt}-{position:02d}",
                            "domain": prompts.DOMAINS[(index + position - 1) % 8],
                            "scenario": _scenario(index, position),
                        }
                        for position in range(1, 9)
                    ],
                }
            ),
            encoding="utf-8",
        )
    return directory


@pytest.fixture
def runs_root(tmp_path) -> Path:
    root = tmp_path / "runs"
    for model in generate.MODELS:
        path = isolation.battery_path(root, model, datetime.now(timezone.utc))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "model": model,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "passed": True,
                    "system_prompt_sha256": isolation.SYSTEM_PROMPT_SHA256,
                }
            ),
            encoding="utf-8",
        )
    return root


class Recorder:
    """A transport that replays scripted stdout and remembers every argv."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls: list[tuple[list[str], str]] = []

    def __call__(self, cmd, prompt, timeout):
        self.calls.append((list(cmd), prompt))
        out = self.outputs[min(len(self.calls) - 1, len(self.outputs) - 1)]
        if isinstance(out, CliResult):
            return out
        return CliResult(0, out, "", 0.1)


def run(bank_dir, runs_root, tmp_path, transport, **kwargs):
    return generate.generate(
        models=kwargs.pop("models", ["claude-sonnet-5"]),
        formats=kwargs.pop("formats", ["memo"]),
        corpus_root=kwargs.pop("corpus_root", tmp_path / "corpus"),
        bank_dir=bank_dir,
        runs_root=runs_root,
        transport=transport,
        sleeper=lambda _: None,
        log=lambda _: None,
        **kwargs,
    )


# --- the happy path ----------------------------------------------------------


def test_generate_writes_document_and_sidecar(bank_dir, runs_root, tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, "cli_version", lambda: "2.1.220 (Claude Code)")
    transport = Recorder([envelope(WORDS * 700)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)

    assert len(report.written) == 1
    doc = tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.md"
    assert doc.is_file()

    side = json.loads(doc.with_suffix(".json").read_text())
    assert side["model_requested"] == "claude-sonnet-5"
    assert side["model_reported"] == "claude-sonnet-5-20260101"
    assert side["prompt_id"] == "memo-01"
    assert side["format"] == "memo"
    assert side["words"] >= 4500
    assert side["met_floor"] is True
    assert side["continuations"] == 0
    assert side["continuation_boundaries"] == []
    assert side["cli_version"] == "2.1.220 (Claude Code)"
    assert side["system_prompt_sha256"] == isolation.SYSTEM_PROMPT_SHA256
    assert len(side["prompt_sha256"]) == 64
    assert len(side["doc_sha256"]) == 64
    assert side["usage"]["input_tokens"] == 100
    assert side["usage"]["output_tokens"] == 500
    assert side["model_usage"] == {"claude-sonnet-5-20260101": {"outputTokens": 500}}
    assert side["isolation_probe"].endswith(".json")
    datetime.fromisoformat(side["timestamp"])  # parses, and is UTC-aware
    assert side["timestamp"].endswith("+00:00")


def test_generated_document_loads_through_the_corpus_reader(bank_dir, runs_root, tmp_path):
    run(bank_dir, runs_root, tmp_path, Recorder([envelope(WORDS * 700)]), limit=1)
    docs = load_corpus(tmp_path / "corpus")
    assert len(docs) == 1
    assert docs[0].doc_id == "claude-sonnet-5/memo-01"
    assert docs[0].sidecar["prompt_id"] == "memo-01"


def test_the_call_uses_the_isolation_recipe(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 700)])
    run(bank_dir, runs_root, tmp_path, transport, limit=1)
    cmd, prompt = transport.calls[0]
    assert "--safe-mode" in cmd
    assert isolation.MINIMAL_SYSTEM_PROMPT in cmd
    assert cmd[-2:] == ["--model", "claude-sonnet-5"]
    # The scenario and the convention both reach the model; nothing else does.
    assert "Freight" in prompt and "employs 312 people" in prompt
    assert "One document, written as the format is normally written." in prompt
    assert "5,000 words" in prompt


def test_cells_are_walked_in_sorted_order(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 700)])
    report = run(
        bank_dir, runs_root, tmp_path, transport, formats=["sop", "memo"], limit=3
    )
    assert [c.prompt_id for c in report.cells] == ["memo-01", "memo-02", "memo-03"]


# --- continuation ------------------------------------------------------------


def test_short_first_turn_is_continued_to_the_floor(bank_dir, runs_root, tmp_path):
    transport = Recorder(
        [
            envelope(WORDS * 200, session_id="sess-A"),
            envelope(WORDS * 200, session_id="sess-A"),
            envelope(WORDS * 400, session_id="sess-A"),
        ]
    )
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)

    cell = report.written[0]
    assert cell.continuations == 2
    assert cell.words >= 4500

    # Continuations resume the session and carry the same isolation flags.
    for cmd, prompt in transport.calls[1:]:
        assert "--resume" in cmd
        assert cmd[cmd.index("--resume") + 1] == "sess-A"
        assert "--safe-mode" in cmd
        assert prompt == generate.CONTINUE_PROMPT


def test_continuation_boundaries_point_at_the_seams(bank_dir, runs_root, tmp_path):
    first, second, third = WORDS * 200, "SECOND CHUNK. " + WORDS * 200, "THIRD CHUNK. " + WORDS * 400
    transport = Recorder([envelope(first), envelope(second), envelope(third)])
    run(bank_dir, runs_root, tmp_path, transport, limit=1)

    doc = tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.md"
    text = doc.read_text()
    side = json.loads(doc.with_suffix(".json").read_text())
    offsets = side["continuation_boundaries"]

    assert len(offsets) == 2
    assert text[offsets[0]:].startswith("SECOND CHUNK.")
    assert text[offsets[1]:].startswith("THIRD CHUNK.")


def test_continuation_stops_at_the_cap(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope("short. ")])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert report.written[0].continuations == generate.MAX_CONTINUATIONS
    assert len(transport.calls) == 1 + generate.MAX_CONTINUATIONS
    assert "below floor" in report.written[0].detail


def test_continuation_stops_when_the_model_returns_nothing(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 100), envelope("   ")])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert report.written[0].continuations == 0
    assert len(transport.calls) == 2


def test_continuation_needs_a_session_id(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 100, session_id="")])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert report.written[0].continuations == 0
    assert len(transport.calls) == 1
    side = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.json").read_text()
    )
    assert any("cannot continue" in note for note in side["notes"])


def test_usage_accumulates_across_continuations(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 200), envelope(WORDS * 600)])
    run(bank_dir, runs_root, tmp_path, transport, limit=1)
    side = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.json").read_text()
    )
    assert side["usage"]["input_tokens"] == 200
    assert side["usage"]["output_tokens"] == 1000


# --- skip logic --------------------------------------------------------------


def test_second_run_skips_a_document_that_met_the_floor(bank_dir, runs_root, tmp_path):
    corpus = tmp_path / "corpus"
    run(bank_dir, runs_root, tmp_path, Recorder([envelope(WORDS * 700)]), limit=1, corpus_root=corpus)

    second = Recorder([envelope(WORDS * 700)])
    report = run(bank_dir, runs_root, tmp_path, second, limit=1, corpus_root=corpus)

    # A skip does not spend the limit — otherwise resuming a half-finished run
    # would walk the cells already done and stop before reaching new work.
    assert report.skipped[0].prompt_id == "memo-01"
    assert report.skipped[0].words >= 4500
    assert report.written[0].prompt_id == "memo-02"
    assert len(second.calls) == 1


def test_a_sub_floor_document_is_regenerated(bank_dir, runs_root, tmp_path):
    corpus = tmp_path / "corpus"
    run(bank_dir, runs_root, tmp_path, Recorder([envelope("short. ")]), limit=1, corpus_root=corpus)

    second = Recorder([envelope(WORDS * 700)])
    report = run(bank_dir, runs_root, tmp_path, second, limit=1, corpus_root=corpus)

    assert second.calls, "a document below the floor must not be treated as done"
    assert len(report.written) == 1
    assert report.written[0].words >= 4500


def test_force_regenerates_a_complete_document(bank_dir, runs_root, tmp_path):
    corpus = tmp_path / "corpus"
    run(bank_dir, runs_root, tmp_path, Recorder([envelope(WORDS * 700)]), limit=1, corpus_root=corpus)

    second = Recorder([envelope(WORDS * 800)])
    report = run(
        bank_dir, runs_root, tmp_path, second, limit=1, corpus_root=corpus, force=True
    )
    assert second.calls
    assert len(report.written) == 1


def test_existing_words_falls_back_to_counting_the_file(tmp_path):
    path = generate.doc_path(tmp_path, "m", "memo-01")
    path.parent.mkdir(parents=True)
    path.write_text(WORDS * 10, encoding="utf-8")
    assert generate.existing_words(tmp_path, "m", "memo-01") == 100


def test_existing_words_is_none_when_nothing_is_there(tmp_path):
    assert generate.existing_words(tmp_path, "m", "memo-01") is None


# --- errors ------------------------------------------------------------------


def test_a_hard_error_is_persisted_and_the_run_continues(bank_dir, runs_root, tmp_path):
    bad = CliResult(0, envelope("Invalid model name", is_error=True), "", 0.1)
    transport = Recorder([bad, envelope(WORDS * 700)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=2)

    assert len(report.failed) == 1
    assert len(report.written) == 1
    marker = tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.failed.json"
    assert marker.is_file()
    data = json.loads(marker.read_text())
    assert data["is_error"] is True
    assert "Invalid model name" in data["result"]
    # A structural error is not retried three times.
    assert len(data["attempts"]) == 1
    assert not (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.md").exists()


def test_a_rate_limit_is_retried_with_backoff(bank_dir, runs_root, tmp_path):
    slept: list[float] = []
    limited = CliResult(0, envelope("rate limit exceeded", is_error=True), "", 0.1)
    transport = Recorder([limited, limited, envelope(WORDS * 700)])

    report = generate.generate(
        models=["claude-sonnet-5"],
        formats=["memo"],
        limit=1,
        corpus_root=tmp_path / "corpus",
        bank_dir=bank_dir,
        runs_root=runs_root,
        transport=transport,
        sleeper=slept.append,
        log=lambda _: None,
    )
    # Recovers on the third attempt, so only the first two waits are spent.
    assert len(report.written) == 1
    assert slept == [60, 300]
    assert len(transport.calls) == 3


def test_retries_give_up_after_three_attempts(bank_dir, runs_root, tmp_path):
    limited = CliResult(0, envelope("overloaded", is_error=True), "", 0.1)
    transport = Recorder([limited])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert len(report.failed) == 1
    assert len(transport.calls) == generate.MAX_ATTEMPTS


def test_a_timeout_counts_as_retryable(bank_dir, runs_root, tmp_path):
    timed_out = CliResult(124, "", "timed out after 1800s", 1800.0, timed_out=True)
    transport = Recorder([timed_out, timed_out, envelope(WORDS * 700)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert len(report.written) == 1


def test_unparseable_stdout_is_a_failure(bank_dir, runs_root, tmp_path):
    transport = Recorder([CliResult(0, "<html>gateway error</html>", "", 0.1)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)
    assert len(report.failed) == 1
    data = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.failed.json").read_text()
    )
    assert "not JSON" in data["parse_error"]


def test_a_successful_regeneration_clears_the_failure_marker(bank_dir, runs_root, tmp_path):
    corpus = tmp_path / "corpus"
    bad = CliResult(0, envelope("boom", is_error=True), "", 0.1)
    run(bank_dir, runs_root, tmp_path, Recorder([bad]), limit=1, corpus_root=corpus)
    marker = corpus / "claude-sonnet-5" / "memo-01.failed.json"
    assert marker.is_file()

    run(bank_dir, runs_root, tmp_path, Recorder([envelope(WORDS * 700)]), limit=1, corpus_root=corpus)
    assert not marker.exists()


# --- the isolation gate ------------------------------------------------------


def test_generate_refuses_without_a_fresh_probe(bank_dir, tmp_path):
    with pytest.raises(RuntimeError, match="no isolation probe battery passed"):
        generate.generate(
            models=["claude-sonnet-5"],
            formats=["memo"],
            corpus_root=tmp_path / "corpus",
            bank_dir=bank_dir,
            runs_root=tmp_path / "empty-runs",
            transport=Recorder([envelope(WORDS * 700)]),
            log=lambda _: None,
        )


def test_generate_refuses_on_a_stale_probe(bank_dir, tmp_path):
    root = tmp_path / "runs"
    stale = datetime.now(timezone.utc) - timedelta(hours=48)
    path = isolation.battery_path(root, "claude-sonnet-5", stale)
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "passed": True,
                "timestamp": stale.isoformat(),
                "system_prompt_sha256": isolation.SYSTEM_PROMPT_SHA256,
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError):
        generate.generate(
            models=["claude-sonnet-5"],
            formats=["memo"],
            corpus_root=tmp_path / "corpus",
            bank_dir=bank_dir,
            runs_root=root,
            transport=Recorder([envelope(WORDS * 700)]),
            log=lambda _: None,
        )


def test_skip_isolation_check_warns_loudly_and_records_no_probe(bank_dir, tmp_path):
    logged: list[str] = []
    report = generate.generate(
        models=["claude-sonnet-5"],
        formats=["memo"],
        limit=1,
        corpus_root=tmp_path / "corpus",
        bank_dir=bank_dir,
        runs_root=tmp_path / "empty",
        skip_isolation_check=True,
        transport=Recorder([envelope(WORDS * 700)]),
        log=logged.append,
        sleeper=lambda _: None,
    )
    assert len(report.written) == 1
    assert any("WARNING" in line and "not corpus-grade" in line for line in logged)
    side = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.json").read_text()
    )
    assert side["isolation_probe"] == ""


def test_generate_refuses_a_bank_that_does_not_lint(tmp_path, runs_root):
    directory = tmp_path / "formats"
    directory.mkdir()
    (directory / "memo.yaml").write_text(
        yaml.safe_dump({"format": "memo", "bundle": True, "prompts": []}), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="does not lint"):
        generate.generate(
            models=["claude-sonnet-5"],
            formats=["memo"],
            corpus_root=tmp_path / "corpus",
            bank_dir=directory,
            runs_root=runs_root,
            transport=Recorder([envelope(WORDS * 700)]),
            log=lambda _: None,
        )


def test_generate_rejects_an_unknown_format(bank_dir, runs_root, tmp_path):
    with pytest.raises(ValueError, match="unknown format"):
        generate.generate(
            models=["claude-sonnet-5"],
            formats=["haiku-collection"],
            corpus_root=tmp_path / "corpus",
            bank_dir=bank_dir,
            runs_root=runs_root,
            transport=Recorder([envelope(WORDS * 700)]),
            log=lambda _: None,
        )


# --- target override ---------------------------------------------------------


def test_target_override_shrinks_the_ask_and_marks_the_sidecar(bank_dir, runs_root, tmp_path):
    transport = Recorder([envelope(WORDS * 120)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1, target_override=800)

    assert len(report.written) == 1
    assert transport.calls[0][1].endswith("roughly 800 words.")
    side = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.json").read_text()
    )
    assert side["target_override"] == 800
    assert side["min_words"] == 720
    assert side["met_floor"] is True


# --- status ------------------------------------------------------------------


def test_status_matrix_counts_only_documents_that_met_the_floor(bank_dir, runs_root, tmp_path):
    corpus = tmp_path / "corpus"
    run(bank_dir, runs_root, tmp_path, Recorder([envelope(WORDS * 700)]), limit=1, corpus_root=corpus)

    text = generate.status(corpus, models=["claude-sonnet-5"], formats=["memo"], bank_dir=bank_dir)
    assert "1/8" in text
    assert "claude-sonnet-5" in text
    assert "TOTAL" in text


def test_status_on_an_empty_corpus(tmp_path, bank_dir):
    text = generate.status(tmp_path / "nothing", bank_dir=bank_dir)
    assert "0/8" in text
    for model in generate.MODELS:
        assert model in text


# --- contamination scan ------------------------------------------------------


def test_scan_contamination_finds_a_marker():
    assert generate.scan_contamination("per the writing-voice skill") == ["writing-voice"]


def test_scan_contamination_is_clean_on_ordinary_prose():
    assert generate.scan_contamination(WORDS * 20) == []


# --- backoff (DEFECT-4) ------------------------------------------------------


def test_all_three_backoff_waits_are_reachable(bank_dir, runs_root, tmp_path):
    # Three escalating waits means four attempts. At three, 900s was dead code.
    assert generate.MAX_ATTEMPTS == len(generate.BACKOFF_SECONDS) + 1
    slept: list[float] = []
    limited = CliResult(0, envelope("rate limit exceeded", is_error=True), "", 0.1)
    transport = Recorder([limited])
    report = generate.generate(
        models=["claude-sonnet-5"],
        formats=["memo"],
        limit=1,
        corpus_root=tmp_path / "corpus",
        bank_dir=bank_dir,
        runs_root=runs_root,
        transport=transport,
        sleeper=slept.append,
        log=lambda _: None,
    )
    assert slept == list(generate.BACKOFF_SECONDS)
    assert len(transport.calls) == 4
    assert len(report.failed) == 1


# --- model attribution is fatal (DEFECT-5) -----------------------------------


def test_a_document_from_the_wrong_model_is_never_written(bank_dir, runs_root, tmp_path):
    wrong = envelope(WORDS * 700, modelUsage={"claude-haiku-4-5-20251001": {"outputTokens": 9000}})
    transport = Recorder([CliResult(0, wrong, "", 0.1)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)

    assert len(report.failed) == 1
    assert not (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.md").exists()
    marker = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.failed.json").read_text()
    )
    assert any("model mismatch" in note for note in marker["attempts"])
    assert "claude-haiku-4-5-20251001" in str(marker["attempts"])


def test_a_mismatch_is_not_retried(bank_dir, runs_root, tmp_path):
    wrong = envelope(WORDS * 700, modelUsage={"other-model": {"outputTokens": 900}})
    transport = Recorder([CliResult(0, wrong, "", 0.1)])
    run(bank_dir, runs_root, tmp_path, transport, limit=1)
    # Structural, not transient: one call, no backoff.
    assert len(transport.calls) == 1


def test_a_wrong_model_continuation_fails_the_whole_document(bank_dir, runs_root, tmp_path):
    good = envelope(WORDS * 200)
    wrong = envelope(WORDS * 600, modelUsage={"claude-haiku-4-5": {"outputTokens": 9000}})
    transport = Recorder([CliResult(0, good, "", 0.1), CliResult(0, wrong, "", 0.1)])
    report = run(bank_dir, runs_root, tmp_path, transport, limit=1)

    assert len(report.failed) == 1
    assert not (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.md").exists()
    marker = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.failed.json").read_text()
    )
    assert any("model mismatch on continuation" in note for note in marker["attempts"])


def test_the_requested_model_is_passed_to_the_parser(bank_dir, runs_root, tmp_path):
    # Dated key, matched by containment rather than equality.
    dated = envelope(WORDS * 700, modelUsage={
        "claude-sonnet-5-20260101": {"outputTokens": 9000},
        "claude-haiku-4-5-20251001": {"outputTokens": 20},
    })
    report = run(bank_dir, runs_root, tmp_path, Recorder([CliResult(0, dated, "", 0.1)]), limit=1)
    assert len(report.written) == 1
    side = json.loads(
        (tmp_path / "corpus" / "claude-sonnet-5" / "memo-01.json").read_text()
    )
    assert side["model_reported"] == "claude-sonnet-5-20260101"
    assert side["model_mismatch"] is False


# --- contamination scan uses local markers (DEFECT-3) ------------------------


def test_scan_contamination_picks_up_the_account_email(tmp_path):
    config = tmp_path / ".claude.json"
    config.write_text(
        json.dumps({"oauthAccount": {"emailAddress": "jrivera.qa@example.org"}}),
        encoding="utf-8",
    )
    text = "Please contact jrivera.qa@example.org with questions."
    assert generate.scan_contamination(text, config_path=config, repo_root=tmp_path) == [
        "jrivera.qa@example.org"
    ]


def test_scan_contamination_picks_up_a_local_markers_file(tmp_path):
    (tmp_path / "local-markers.txt").write_text("Wolverine Codename\n", encoding="utf-8")
    hits = generate.scan_contamination(
        "The Wolverine Codename programme shipped.",
        config_path=tmp_path / "missing.json",
        repo_root=tmp_path,
    )
    assert hits == ["Wolverine Codename"]


# --- connect-level retries (2026-07-30 ENOTFOUND incident) -------------------


@pytest.mark.parametrize(
    "message",
    [
        "API Error: Unable to connect to API (ENOTFOUND)",
        "Error: connect ECONNREFUSED 160.79.104.10:443",
        "getaddrinfo EAI_AGAIN api.anthropic.com",
        "Error: socket hang up",
        "connect ETIMEDOUT",
        "network error while sending request",
    ],
)
def test_connect_level_failures_are_retryable(message):
    # A few seconds of network loss must not burn a corpus cell on attempt 1.
    # "connection" did not cover these: ENOTFOUND says "connect", not
    # "connection", and the substring match is literal.
    env = isolation.Envelope(result=message, session_id="", num_turns=1, is_error=True)
    cli = CliResult(returncode=1, stdout="", stderr="", duration_s=1.0)
    assert generate.is_retryable(env, cli), message


def test_a_structural_error_is_still_not_retryable():
    # The widening must not turn permanent failures into 21 minutes of backoff.
    env = isolation.Envelope(
        result="Invalid model name: no such model", session_id="", num_turns=1, is_error=True
    )
    cli = CliResult(returncode=1, stdout="", stderr="", duration_s=1.0)
    assert not generate.is_retryable(env, cli)


def test_auth_failure_is_still_not_retryable():
    # Backing off four times against an expired token helps nobody; the run
    # should stop and ask for a login.
    env = isolation.Envelope(
        result="Failed to authenticate: OAuth session expired and could not be refreshed",
        session_id="",
        num_turns=1,
        is_error=True,
    )
    cli = CliResult(returncode=1, stdout="", stderr="", duration_s=1.0)
    assert not generate.is_retryable(env, cli)
