"""Stage orchestration for a discovery run: sweep, audit, verify, append.

A full run is one cheap deterministic stage followed by a dozen paid model calls
followed by more paid model calls, and the paid parts fail for boring reasons —
a timeout, a rate limit, a laptop lid. So every stage writes its output to a
predictable path and every stage checks for that path before doing any work.
Resuming is therefore the default and not a mode: re-running `run-all` after a
failure re-reads what completed and picks up at the first stage that did not.

`--force` exists for the case where the inputs changed under a completed stage.
It is deliberately all-or-nothing per stage rather than per file: a half-forced
audit whose four lenses were answered under two different prompt versions is
exactly the kind of quietly-mixed evidence this benchmark refuses elsewhere.

The append stage is the only one that writes outside the run directory, and it
appends `status: candidate` entries only. Nothing in this module promotes a tell
or edits an existing one.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

from telltale.corpus import Doc
from telltale.discovery import auditor, sweep, verify
from telltale.registry import Registry

SWEEP_DIR = "sweep"
AUDIT_DIR = "audit"
VERIFY_DIR = "verify"
VERDICTS_FILENAME = "verdicts.jsonl"
APPENDED_FILENAME = "appended.json"
SUMMARY_FILENAME = "summary.json"


@dataclass
class StageLog:
    """What one stage did, or why it did nothing."""

    stage: str
    skipped: bool
    detail: str
    data: dict[str, Any] = field(default_factory=dict)

    def line(self) -> str:
        mark = "SKIP" if self.skipped else "RUN "
        return f"{mark} {self.stage}: {self.detail}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "skipped": self.skipped,
            "detail": self.detail,
            **self.data,
        }


def sweep_dir(out: Path) -> Path:
    return Path(out) / SWEEP_DIR


def audit_dir(out: Path) -> Path:
    return Path(out) / AUDIT_DIR


def verdicts_path(out: Path) -> Path:
    return Path(out) / VERIFY_DIR / VERDICTS_FILENAME


def stage_sweep(
    docs: Sequence[Doc], out: Path, force: bool = False, **kwargs: Any
) -> StageLog:
    """Stage 1: the statistical sweep. Cheap, deterministic, always re-runnable."""
    target = sweep_dir(out)
    marker = target / sweep.SWEEP_FILENAME
    if marker.is_file() and not force:
        return StageLog(
            "sweep", True, f"{marker} exists ({_count_lines(marker)} rows)"
        )
    summary = sweep.run_sweep(docs, target, **kwargs)
    return StageLog(
        "sweep",
        False,
        f"{summary['written'][sweep.SWEEP_FILENAME]} n-gram rows, "
        f"{summary['written'][sweep.COLLOCATIONS_FILENAME]} collocations, "
        f"{summary['flagged_stats']} flagged stat deltas",
        {"summary": summary},
    )


def stage_audit(
    docs: Sequence[Doc],
    out: Path,
    judge_client: Any,
    models: Sequence[str],
    lenses: Sequence[str] = auditor.LENSES,
    registry: Registry | None = None,
    run_id: str = "",
    force: bool = False,
) -> list[StageLog]:
    """Stage 2: every lens against every target model, one file each."""
    logs: list[StageLog] = []
    target = audit_dir(out)
    existing = list(registry.active_tells(include_candidates=True)) if registry else []
    for model in sorted(models):
        rows = sweep.load_sweep(sweep_dir(out), model=model)
        for lens in lenses:
            name = auditor.candidates_filename(lens, model)
            path = target / name
            if path.is_file() and not force:
                logs.append(
                    StageLog(
                        f"audit/{lens}/{model}",
                        True,
                        f"{path} exists ({len(auditor.load_candidates(path))} candidates)",
                    )
                )
                continue
            run = auditor.run_audit(
                docs,
                judge_client,
                lens,
                model,
                out_dir=target,
                sweep_rows=rows,
                existing_tells=existing,
                run_id=run_id or None,
            )
            logs.append(
                StageLog(
                    f"audit/{lens}/{model}",
                    False,
                    f"{len(run.candidates)} candidate(s), {len(run.rejected)} rejected"
                    + (", retried" if run.retried else ""),
                    {"run": run.as_dict()},
                )
            )
    return logs


def stage_verify(
    docs: Sequence[Doc],
    out: Path,
    registry: Registry,
    judge: Any | None,
    candidates_dir: Path | None = None,
    force: bool = False,
    seed: int = verify.PRECISION_SEED,
) -> tuple[StageLog, list[verify.Verdict]]:
    """Stage 3: the five gates over every proposed candidate."""
    path = verdicts_path(out)
    if path.is_file() and not force:
        recovered = load_verdicts(path)
        return (
            StageLog("verify", True, f"{path} exists ({len(recovered)} verdicts)"),
            recovered,
        )
    candidates = auditor.load_candidate_dir(candidates_dir or audit_dir(out))
    verdicts = verify.verify_all(candidates, docs, registry, judge, seed=seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for verdict in verdicts:
            handle.write(
                json.dumps(verdict.as_dict(), ensure_ascii=False, sort_keys=True) + "\n"
            )
    accepted = sum(1 for v in verdicts if v.accepted)
    parked = sum(1 for v in verdicts if v.status == verify.STATUS_NEEDS_STAT)
    return (
        StageLog(
            "verify",
            False,
            f"{len(verdicts)} candidate(s): {accepted} accepted, {parked} parked for "
            f"stat implementation, {len(verdicts) - accepted - parked} rejected",
            {"n": len(verdicts), "accepted": accepted, "parked": parked},
        ),
        verdicts,
    )


def load_verdicts(path: Path) -> list[verify.Verdict]:
    """Read verdicts.jsonl back, so a resumed run does not re-pay for gate 4."""
    file = Path(path)
    if not file.is_file():
        return []
    out: list[verify.Verdict] = []
    for line in file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:  # pragma: no cover - defensive
            continue
        if isinstance(row, dict):
            out.append(verify.Verdict.from_dict(row))
    return out


def stage_append(
    docs: Sequence[Doc],
    out: Path,
    registry: Registry,
    verdicts: Sequence[verify.Verdict],
    run_id: str,
    force: bool = False,
) -> StageLog:
    """Stage 4: accepted verdicts into the registry, as candidates."""
    path = Path(out) / APPENDED_FILENAME
    if path.is_file() and not force:
        return StageLog("append", True, f"{path} exists")
    tells = verify.append_accepted(verdicts, registry, run_id, docs=docs)
    record = {
        "run_id": run_id,
        "registry_version": registry.version,
        "registry_hash": registry.content_hash,
        "appended": [
            {"id": t.id, "name": t.name, "scope": t.scope, "method": t.method}
            for t in tells
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return StageLog(
        "append",
        False,
        f"{len(tells)} candidate tell(s) appended; registry now v{registry.version}",
        {"appended": [t.id for t in tells]},
    )


def run_all(
    docs: Sequence[Doc],
    out: Path,
    registry: Registry,
    judge_client: Any | None = None,
    judge_backend: Any | None = None,
    models: Sequence[str] | None = None,
    lenses: Sequence[str] = auditor.LENSES,
    run_id: str | None = None,
    force: bool = False,
    seed: int = verify.PRECISION_SEED,
    log: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Sweep, four lenses per model, verify, append. Resumable at every stage.

    `judge_client` answers the lens calls; `judge_backend` (a `JudgeClient` too)
    answers gate 4's adjudications. They are separate arguments because a caller
    may legitimately want to audit without a verification budget, or verify
    candidates proposed in an earlier run.
    """
    out = Path(out)
    run = run_id or auditor.make_run_id()
    emit = log or (lambda _line: None)
    logs: list[StageLog] = []

    def record(entry: StageLog) -> None:
        logs.append(entry)
        emit(entry.line())

    record(stage_sweep(docs, out, force=force))

    targets = sorted(models) if models else sweep.models_of(docs)
    if judge_client is not None:
        for entry in stage_audit(
            docs,
            out,
            judge_client,
            targets,
            lenses=lenses,
            registry=registry,
            run_id=run,
            force=force,
        ):
            record(entry)
    else:
        record(StageLog("audit", True, "no judge client supplied; lenses not run"))

    verify_log, verdicts = stage_verify(
        docs, out, registry, judge_backend, force=force, seed=seed
    )
    record(verify_log)

    record(stage_append(docs, out, registry, verdicts, run, force=force))

    summary = {
        "run_id": run,
        "out_dir": str(out),
        "n_docs": len(docs),
        "models": targets,
        "lenses": list(lenses),
        "stages": [entry.as_dict() for entry in logs],
    }
    (out / SUMMARY_FILENAME).parent.mkdir(parents=True, exist_ok=True)
    (out / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    return summary


def _count_lines(path: Path) -> int:
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:  # pragma: no cover - defensive
        return 0


__all__ = [
    "APPENDED_FILENAME",
    "AUDIT_DIR",
    "SUMMARY_FILENAME",
    "SWEEP_DIR",
    "VERDICTS_FILENAME",
    "VERIFY_DIR",
    "StageLog",
    "audit_dir",
    "load_verdicts",
    "run_all",
    "stage_append",
    "stage_audit",
    "stage_sweep",
    "stage_verify",
    "sweep_dir",
    "verdicts_path",
]
