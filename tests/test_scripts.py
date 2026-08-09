"""The R16 recall check: does the revised extraction keep the counted spans?

The script itself is a one-shot gate, but the arithmetic it reports decides
whether a rubric revision ships, so every step of it is exercised here against a
synthetic run rather than the real one.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from telltale.corpus import load_corpus
from telltale.judge import cache as cache_mod
from telltale.judge import protocol
from telltale.judge.cache import JudgeCache
from telltale.registry import Registry

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "rule_of_three_recall.py"
REGISTRY_PATH = REPO_ROOT / "registry" / "tells.yaml"
JUDGE_MODEL = "claude-opus-4-6"


def _load_script() -> Any:
    spec = importlib.util.spec_from_file_location("rule_of_three_recall", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    # Registered before execution: a dataclass in the module resolves its own
    # annotations through sys.modules, and a module that is not there yet fails
    # to build its fields.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def recall() -> Any:
    return _load_script()


DOC_TEXT = """\
# Quarterly note

The plan is faster, cleaner, and cheaper. We reviewed the intake process with
the team and agreed on a single owner.

The budget covers 3 sites, 12 staff, and one vehicle, which the board approved
in March.
"""

COUNTED = "The plan is faster, cleaner, and cheaper."
NOT_COUNTED = "The budget covers 3 sites, 12 staff, and one vehicle"


@pytest.fixture
def world(tmp_path: Path, recall: Any) -> dict[str, Any]:
    """A corpus of one document, a run that counted one span, and a warm cache."""
    corpus = tmp_path / "corpus" / "claude-opus-5"
    corpus.mkdir(parents=True)
    (corpus / "memo-01.md").write_text(DOC_TEXT, encoding="utf-8")

    run_dir = tmp_path / "runs" / "20260804T210242Z-aaaaaaaa-bbbbbbbb"
    run_dir.mkdir(parents=True)
    row = {
        "doc_id": "claude-opus-5/memo-01",
        "tell_id": "rht.rule-of-three",
        "method": "judge",
        "raw": 1.0,
        "matches": [
            {"quote": COUNTED, "counted": True},
            {"quote": NOT_COUNTED, "counted": False},
        ],
    }
    other = dict(row, tell_id="rht.rhetorical-qa")
    (run_dir / "scores.jsonl").write_text(
        json.dumps(row) + "\n" + json.dumps(other) + "\n", encoding="utf-8"
    )

    readme = tmp_path / "runs" / "README.md"
    readme.write_text(
        "# Runs\n\n**`20260804T210242Z-aaaaaaaa-bbbbbbbb`** is the current "
        "reference run for the shakedown.\n",
        encoding="utf-8",
    )

    tell = Registry(REGISTRY_PATH).get("rht.rule-of-three")
    doc = load_corpus(tmp_path / "corpus")[0]
    chunk = protocol.judge_view_text(tell, doc)[0]

    cache_root = tmp_path / "cache" / "judge"
    cache = JudgeCache(cache_root)
    cache.put(
        cache_mod.cache_key(
            chunk.sha256,
            tell.id,
            recall.OLD_RUBRIC_VERSION,
            JUDGE_MODEL,
            cache_mod.EXTRACT,
        ),
        {"stage": cache_mod.EXTRACT},
        {
            "spans": [
                {"quote": COUNTED, "location_hint": ""},
                {"quote": NOT_COUNTED, "location_hint": ""},
                {"quote": "We reviewed the intake process", "location_hint": ""},
            ]
        },
    )
    return {
        "root": tmp_path,
        "corpus": tmp_path / "corpus",
        "run_dir": run_dir,
        "cache": cache_root,
        "tell": tell,
        "chunk": chunk,
    }


# --- reading the run ---------------------------------------------------------


def test_it_reads_the_run_the_readme_nominates(recall: Any, world: dict[str, Any]) -> None:
    found = recall.authoritative_run(world["root"] / "runs")
    assert found == world["run_dir"]


def test_the_real_readme_still_names_a_run_that_exists(recall: Any) -> None:
    """The pointer is a file a human maintains; a rename would break the script
    silently, and silently is the wrong way to find that out."""
    found = recall.authoritative_run(REPO_ROOT / "runs")
    assert found.name.startswith("2026")


def test_only_counted_spans_of_this_tell_are_targets(
    recall: Any, world: dict[str, Any]
) -> None:
    spans = recall.counted_spans(world["run_dir"])
    assert spans == {"claude-opus-5/memo-01": [COUNTED]}


# --- placing spans in chunks -------------------------------------------------


def test_a_counted_span_is_placed_in_its_chunk_with_the_cached_cost(
    recall: Any, world: dict[str, Any]
) -> None:
    tell, targets, unplaced = recall.prepare(
        world["run_dir"], world["corpus"], REGISTRY_PATH, world["cache"], JUDGE_MODEL
    )
    assert tell.rubric_version == 2, "the revised rubric is what gets re-asked"
    assert unplaced == []
    assert len(targets) == 1
    target = targets[0]
    assert target.label == "claude-opus-5/memo-01#0"
    assert target.counted == [COUNTED]
    assert target.cached_answer_found is True
    assert len(target.cached_proposals) == 3, "what the old prompt cost, verbatim"


def test_a_span_that_verifies_nowhere_is_reported_not_dropped(
    recall: Any, world: dict[str, Any]
) -> None:
    """A silently dropped span lowers recall by removing its own denominator."""
    run_dir = world["run_dir"]
    (run_dir / "scores.jsonl").write_text(
        json.dumps(
            {
                "doc_id": "claude-opus-5/memo-01",
                "tell_id": "rht.rule-of-three",
                "method": "judge",
                "matches": [
                    {"quote": COUNTED, "counted": True},
                    {"quote": "a sentence from some other document", "counted": True},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    _, targets, unplaced = recall.prepare(
        run_dir, world["corpus"], REGISTRY_PATH, world["cache"], JUDGE_MODEL
    )
    assert len(targets) == 1
    assert len(unplaced) == 1
    assert unplaced[0]["why"] == "quote verifies in no chunk"


def test_a_missing_cached_answer_is_flagged_rather_than_counted_as_zero(
    recall: Any, world: dict[str, Any], tmp_path: Path
) -> None:
    _, targets, _ = recall.prepare(
        world["run_dir"], world["corpus"], REGISTRY_PATH, tmp_path / "empty", JUDGE_MODEL
    )
    assert targets[0].cached_answer_found is False
    assert "MISS" in recall.dry_run_text(targets, [])


# --- the comparison ----------------------------------------------------------


def test_containment_is_whitespace_normalized_and_two_directional(recall: Any) -> None:
    counted = "faster,  cleaner,\nand cheaper"
    assert recall.contains("The plan is faster, cleaner, and cheaper.", counted)
    hit = recall.match_counted_span(counted, ["The plan is faster, cleaner, and cheaper."])
    assert hit == {"strict": True, "either": True}
    # The reverse: the revision quoted less than the run counted.
    loose = recall.match_counted_span(
        "The plan is faster, cleaner, and cheaper.", ["faster, cleaner, and cheaper"]
    )
    assert loose == {"strict": False, "either": True}
    assert recall.match_counted_span(counted, ["something else entirely"]) == {
        "strict": False,
        "either": False,
    }


def test_the_verdict_follows_r16s_thresholds(recall: Any) -> None:
    assert recall.verdict(0.85, 0.60) == "pass"
    assert recall.verdict(0.70, 0.50) == "pass"
    assert recall.verdict(0.85, 0.30) == "recall-passed-volume-failed"
    assert recall.verdict(0.60, 0.90) == "coordinator-review"
    assert recall.verdict(0.49, 0.90) == "fallback-to-prefilter"


def test_the_report_measures_recall_and_the_volume_it_bought(
    recall: Any, world: dict[str, Any]
) -> None:
    _, targets, unplaced = recall.prepare(
        world["run_dir"], world["corpus"], REGISTRY_PATH, world["cache"], JUDGE_MODEL
    )
    report = recall.build_report(
        targets,
        {targets[0].label: [protocol.normalize_ws(COUNTED)]},
        unplaced,
        world["run_dir"],
        world["tell"],
        JUDGE_MODEL,
    )
    assert report["counted_spans"] == 1
    assert report["recall"] == 1.0
    assert report["proposals_per_chunk_old"] == 3.0
    assert report["proposals_per_chunk_new"] == 1.0
    assert report["proposals_per_chunk_drop"] == pytest.approx(2 / 3)
    assert report["verdict"] == "pass"
    assert "recall" in recall.summarize(report)


def test_a_lost_span_shows_up_as_a_miss_with_its_quote(
    recall: Any, world: dict[str, Any]
) -> None:
    _, targets, unplaced = recall.prepare(
        world["run_dir"], world["corpus"], REGISTRY_PATH, world["cache"], JUDGE_MODEL
    )
    report = recall.build_report(
        targets, {targets[0].label: []}, unplaced, world["run_dir"], world["tell"], JUDGE_MODEL
    )
    assert report["recall"] == 0.0
    assert report["verdict"] == "fallback-to-prefilter"
    assert COUNTED[:40] in recall.summarize(report)


def test_replay_asks_the_revised_question_once_per_chunk(
    recall: Any, world: dict[str, Any]
) -> None:
    _, targets, _ = recall.prepare(
        world["run_dir"], world["corpus"], REGISTRY_PATH, world["cache"], JUDGE_MODEL
    )
    prompts: list[str] = []

    class Client:
        model = JUDGE_MODEL

        def ask(self, stage, chunk_sha, tell_id, rubric_version, prompt, quote=None):
            prompts.append(prompt)
            assert stage == cache_mod.EXTRACT
            assert rubric_version == 2, "the revision, not the cached question"
            return {"spans": [{"quote": COUNTED, "location_hint": ""}]}, "key", False

    out = recall.replay(targets, world["tell"], Client(), workers=1)
    assert list(out) == [targets[0].label]
    assert len(prompts) == 1
    assert "APPLY CRITERION (c) BEFORE YOU PROPOSE" in prompts[0]


# --- the dry run -------------------------------------------------------------


def test_the_dry_run_makes_no_live_call(
    recall: Any, world: dict[str, Any], monkeypatch: pytest.MonkeyPatch, capsys: Any
) -> None:
    """The flag exists so the wiring can be proved without spending anything."""
    from telltale.judge import transport as transport_mod

    def explode(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("a dry run must not build a transport")

    monkeypatch.setattr(transport_mod, "CliJudgeTransport", explode)
    code = recall.main(
        [
            "--dry-run",
            "--run",
            str(world["run_dir"]),
            "--corpus",
            str(world["corpus"]),
            "--registry",
            str(REGISTRY_PATH),
            "--cache",
            str(world["cache"]),
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "DRY RUN" in out
    assert "claude-opus-5/memo-01#0" in out
    assert "live calls a real pass would make: 1" in out


def test_nothing_to_check_is_an_error_not_an_empty_pass(
    recall: Any, world: dict[str, Any], tmp_path: Path
) -> None:
    empty = tmp_path / "empty-run"
    empty.mkdir()
    (empty / "scores.jsonl").write_text("", encoding="utf-8")
    code = recall.main(
        [
            "--dry-run",
            "--run",
            str(empty),
            "--corpus",
            str(world["corpus"]),
            "--registry",
            str(REGISTRY_PATH),
            "--cache",
            str(world["cache"]),
        ]
    )
    assert code == 1
