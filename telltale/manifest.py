"""The run manifest: what a scoring run was computed from, and proof it holds.

A benchmark number is worth exactly as much as the reader's ability to
reproduce it. The manifest is the record that makes that possible: the corpus
it read (and that corpus's hash), the registry version and content hash, the
weights, the environment, and the exact command line. `verify` then closes the
loop — it re-runs the pipeline from those same inputs and requires the outputs
to come back byte for byte.

The manifest is deliberately the *only* output that is not byte-reproducible:
it carries the wall-clock timestamp and the run id derived from it. Everything
else — scores, matrices, scorecard — is a pure function of the corpus and the
registry, which is what lets `verify` compare bytes instead of tolerances.
"""

from __future__ import annotations

import datetime
import filecmp
import json
import platform
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

import telltale
from telltale import scoring
from telltale.corpus import Doc, corpus_hash
from telltale.registry import Registry, Tell

MANIFEST_NAME = "manifest.json"

# Everything a run writes apart from the manifest itself. All four are pure
# functions of (corpus, registry), so all four must survive a byte comparison.
REPRODUCIBLE_OUTPUTS = (
    "scores.jsonl",
    "matrix.csv",
    "matrix_by_format.csv",
    "scorecard.md",
)


def utc_stamp(now: datetime.datetime | None = None) -> str:
    moment = now or datetime.datetime.now(datetime.timezone.utc)
    return moment.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_run_id(corpus_sha: str, registry_sha: str, now: datetime.datetime | None = None) -> str:
    """A run id that sorts by time and names its inputs: TS-corpus8-registry8."""
    return f"{utc_stamp(now)}-{corpus_sha[:8]}-{registry_sha[:8]}"


def build_manifest(
    docs: Sequence[Doc],
    registry: Registry,
    scored_tells: Sequence[Tell],
    corpus_root: Path,
    judge_skipped: Sequence[str],
    include_candidates: bool = False,
    cli_args: Sequence[str] | None = None,
    bootstrap: dict[str, Any] | None = None,
    now: datetime.datetime | None = None,
    run_id: str | None = None,
    judge: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the manifest for one scoring run."""
    sha = corpus_hash(list(docs))
    registry_sha = registry.content_hash

    per_model: dict[str, int] = {}
    per_format: dict[str, int] = {}
    for doc in docs:
        per_model[doc.model] = per_model.get(doc.model, 0) + 1
        per_format[doc.fmt] = per_format.get(doc.fmt, 0) + 1

    return {
        "run_id": run_id or make_run_id(sha, registry_sha, now=now),
        "created_utc": (now or datetime.datetime.now(datetime.timezone.utc))
        .astimezone(datetime.timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "corpus": {
            "root": str(Path(corpus_root)),
            "n_docs": len(docs),
            "n_words": int(sum(d.words for d in docs)),
            "per_model": dict(sorted(per_model.items())),
            "per_format": dict(sorted(per_format.items())),
            "corpus_hash": sha,
        },
        "registry": {
            "path": str(Path(registry.path)),
            "version": registry.version,
            "schema_version": registry.schema_version,
            "content_hash": registry_sha,
            "n_active": len(registry.active_tells()),
            "n_scored": len(scored_tells),
            "include_candidates": bool(include_candidates),
            "judge_skipped": len(judge_skipped),
            "judge_skipped_ids": sorted(judge_skipped),
            "tells": scoring.tell_meta(scored_tells),
        },
        "weights": {
            "categories": dict(sorted(scoring.CATEGORY_WEIGHTS.items())),
            "min_docs": scoring.MIN_DOCS,
            "min_occurrences": scoring.MIN_OCCURRENCES,
            "winsor_percentile": scoring.WINSOR_PERCENTILE,
        },
        "bootstrap": {
            "n": (bootstrap or {}).get("n"),
            "seed": (bootstrap or {}).get("seed"),
            "method": (bootstrap or {}).get("method"),
            "n_prompts": (bootstrap or {}).get("n_prompts"),
        },
        # Tier-2. `enabled: false` is the M5 shape and stays the default, so a
        # deterministic run's manifest is unchanged by this section existing.
        "judge": dict(judge or {"enabled": False}),
        "environment": {
            "python": platform.python_version(),
            "pandas": _version("pandas"),
            "numpy": _version("numpy"),
            "telltale": telltale.__version__,
        },
        "cli_args": list(cli_args if cli_args is not None else sys.argv[1:]),
    }


def _version(module_name: str) -> str:
    try:
        module = __import__(module_name)
    except ImportError:  # pragma: no cover - both are hard dependencies
        return "unavailable"
    return str(getattr(module, "__version__", "unknown"))


def write_manifest(manifest: dict[str, Any], run_dir: Path) -> Path:
    path = Path(run_dir) / MANIFEST_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def load_manifest(run_dir: Path) -> dict[str, Any]:
    path = Path(run_dir)
    if path.is_dir():
        path = path / MANIFEST_NAME
    return json.loads(path.read_text(encoding="utf-8"))


# --- verification ------------------------------------------------------------


@dataclass
class VerifyResult:
    """Outcome of re-running a scoring run from its own manifest."""

    ok: bool
    run_dir: Path
    checked: list[str] = field(default_factory=list)
    diffs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def summary(self) -> str:
        head = "VERIFIED" if self.ok else "MISMATCH"
        lines = [f"{head}: {self.run_dir}"]
        lines += [f"  ok   {name}" for name in self.checked]
        lines += [f"  DIFF {detail}" for detail in self.diffs]
        lines += [f"  note {detail}" for detail in self.notes]
        return "\n".join(lines)


def verify(run_dir: Path) -> VerifyResult:
    """Recompute a run from its manifest and require byte-identical outputs.

    The inputs are checked first and separately. If the corpus or the registry
    has changed since the run, that is the finding — reporting a diff in
    scores.jsonl would blame the code for someone editing a document.
    """
    from telltale.report import score_run  # local: report imports this module

    run_dir = Path(run_dir)
    manifest = load_manifest(run_dir)
    result = VerifyResult(ok=True, run_dir=run_dir)

    from telltale.corpus import load_corpus

    corpus_root = Path(manifest["corpus"]["root"])
    docs = load_corpus(corpus_root)
    fresh_corpus_hash = corpus_hash(docs)
    if fresh_corpus_hash != manifest["corpus"]["corpus_hash"]:
        result.ok = False
        result.diffs.append(
            f"corpus at {corpus_root} hashes {fresh_corpus_hash[:12]}, "
            f"manifest recorded {manifest['corpus']['corpus_hash'][:12]}"
        )
        return result
    result.checked.append(f"corpus_hash {fresh_corpus_hash[:12]}")

    registry_path = Path(manifest["registry"]["path"])
    if not registry_path.is_file():
        result.ok = False
        result.diffs.append(f"registry missing: {registry_path}")
        return result
    registry = Registry(registry_path)
    if registry.content_hash != manifest["registry"]["content_hash"]:
        result.ok = False
        result.diffs.append(
            f"registry hashes {registry.content_hash[:12]}, "
            f"manifest recorded {manifest['registry']['content_hash'][:12]}"
        )
        return result
    result.checked.append(f"registry_hash {registry.content_hash[:12]}")

    bootstrap = manifest.get("bootstrap") or {}
    judge = manifest.get("judge") or {}
    with tempfile.TemporaryDirectory(prefix="telltale-verify-") as tmp:
        replay = Path(tmp) / "replay"
        score_run(
            corpus_root=corpus_root,
            registry_path=registry_path,
            run_dir=replay,
            include_candidates=bool(manifest["registry"].get("include_candidates", False)),
            cli_args=list(manifest.get("cli_args") or []),
            run_id=manifest.get("run_id"),
            # The replicate count and seed are part of the recipe: a scorecard
            # rendered with a different budget is a different scorecard.
            bootstrap_n=int(bootstrap.get("n") or 1000),
            seed=int(bootstrap.get("seed") or 7),
            # A judge run replays off the cache and never calls the model: the
            # answers are inputs to the run, exactly like the corpus, and
            # re-asking would be measuring the sampler rather than verifying the
            # arithmetic. A cleared cache therefore fails verification loudly,
            # which is the honest outcome — the inputs really are gone.
            judge=bool(judge.get("enabled")),
            judge_model=judge.get("model"),
            judge_tells=judge.get("tells_scored"),
            judge_cache_only=True,
        )
        for name in REPRODUCIBLE_OUTPUTS:
            original = run_dir / name
            fresh = replay / name
            if not original.is_file():
                result.ok = False
                result.diffs.append(f"{name}: missing from the run directory")
                continue
            if not fresh.is_file():  # pragma: no cover - score_run writes all four
                result.ok = False
                result.diffs.append(f"{name}: replay produced nothing")
                continue
            if filecmp.cmp(original, fresh, shallow=False):
                result.checked.append(name)
            else:
                result.ok = False
                result.diffs.append(f"{name}: {_first_difference(original, fresh)}")

    result.notes.append(
        "manifest.json is excluded: it carries the run timestamp by design."
    )
    return result


def _first_difference(left: Path, right: Path) -> str:
    """A one-line pointer at the first line that differs, for the CLI."""
    lhs = left.read_text(encoding="utf-8").splitlines()
    rhs = right.read_text(encoding="utf-8").splitlines()
    for number, (a, b) in enumerate(zip(lhs, rhs), start=1):
        if a != b:
            return f"line {number} differs\n    was:  {a[:160]}\n    now:  {b[:160]}"
    if len(lhs) != len(rhs):
        return f"line count differs ({len(lhs)} vs {len(rhs)})"
    return "files differ"  # pragma: no cover - unreachable when cmp said differ


__all__ = [
    "MANIFEST_NAME",
    "REPRODUCIBLE_OUTPUTS",
    "VerifyResult",
    "build_manifest",
    "load_manifest",
    "make_run_id",
    "utc_stamp",
    "verify",
    "write_manifest",
]
