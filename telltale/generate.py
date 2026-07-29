"""Generate the corpus: one document per (model, format, prompt) cell.

Serial by design. There is no parallelism here and none is wanted this
milestone — generation is long-running and rate-limited, and a serial loop that
can be interrupted and resumed is easier to reason about than a pool that fails
halfway through.

Three things in here are load-bearing for the benchmark's validity rather than
its convenience:

* **The isolation gate.** `generate` will not run for a model unless a probe
  battery for that model passed within the last 24 hours. Isolation is a
  property of the machine at a moment in time; a settings edit or a CLI upgrade
  can reintroduce contamination without anyone noticing, and a corpus generated
  through a leaky harness is not detectably bad after the fact.
* **The min_words floor.** A document that stopped short is continued through
  `--resume`, up to four times. Rate statistics are per 1,000 words, so a
  1,200-word "5,000-word document" is not a smaller sample, it is a different
  kind of writing — openings and closings crowd out the middle. Sub-floor
  documents never enter the corpus.
* **The sidecar.** Every document records what produced it, down to the sha256
  of the prompt and of the pinned system prompt, so a scoring run can prove the
  corpus it read was generated under the harness it claims.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence

from telltale import isolation, prompts as prompt_bank
from telltale.corpus import FORMATS
from telltale.isolation import CliResult, Envelope, Transport

MODELS: tuple[str, ...] = ("claude-opus-5", "claude-fable-5", "claude-sonnet-5")

CONTINUE_PROMPT = (
    "Continue the document exactly where it left off — do not summarize, "
    "repeat, or restart. Just continue."
)

MAX_CONTINUATIONS = 4
#: Four attempts, so all three escalating waits actually get used before a cell
#: is written off. At three attempts the 900s step was unreachable.
MAX_ATTEMPTS = 4
BACKOFF_SECONDS: tuple[int, ...] = (60, 300, 900)

#: Substrings that mark an error worth retrying rather than recording as final.
RETRYABLE_MARKERS: tuple[str, ...] = (
    "rate limit",
    "rate_limit",
    "overloaded",
    "429",
    "500",
    "502",
    "503",
    "504",
    "timeout",
    "timed out",
    "connection",
    "econnreset",
    "temporarily unavailable",
    "usage limit",
)

Sleeper = Callable[[float], None]


# --- results -----------------------------------------------------------------


@dataclass
class CellResult:
    """What happened for one (model, format, prompt) cell."""

    model: str
    fmt: str
    prompt_id: str
    status: str  # "written" | "skipped" | "failed"
    words: int = 0
    continuations: int = 0
    path: Path | None = None
    detail: str = ""


@dataclass
class GenerateReport:
    cells: list[CellResult] = field(default_factory=list)

    @property
    def written(self) -> list[CellResult]:
        return [c for c in self.cells if c.status == "written"]

    @property
    def failed(self) -> list[CellResult]:
        return [c for c in self.cells if c.status == "failed"]

    @property
    def skipped(self) -> list[CellResult]:
        return [c for c in self.cells if c.status == "skipped"]


# --- helpers -----------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def doc_path(corpus_root: Path, model: str, prompt_id: str) -> Path:
    return Path(corpus_root) / model / f"{prompt_id}.md"


def sidecar_path(corpus_root: Path, model: str, prompt_id: str) -> Path:
    return doc_path(corpus_root, model, prompt_id).with_suffix(".json")


def failure_path(corpus_root: Path, model: str, prompt_id: str) -> Path:
    return Path(corpus_root) / model / f"{prompt_id}.failed.json"


def is_retryable(envelope: Envelope, cli: CliResult) -> bool:
    """Whether a failed call looks transient rather than structural."""
    if cli.timed_out:
        return True
    blob = " ".join([envelope.result or "", envelope.parse_error or "", cli.stderr or ""]).lower()
    return any(marker in blob for marker in RETRYABLE_MARKERS)


def existing_words(corpus_root: Path, model: str, prompt_id: str) -> int | None:
    """Word count of an already-generated document, preferring the sidecar.

    Returns None when there is no document. Falls back to counting the file when
    the sidecar is missing or unreadable, so a hand-placed document still counts.
    """
    path = doc_path(corpus_root, model, prompt_id)
    if not path.is_file():
        return None
    side = sidecar_path(corpus_root, model, prompt_id)
    if side.is_file():
        try:
            data = json.loads(side.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("words"), int):
                return data["words"]
        except (OSError, json.JSONDecodeError):
            pass
    try:
        return isolation.textstat_words(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return 0


# --- one call ----------------------------------------------------------------


def _call(
    transport: Transport,
    cmd: list[str],
    prompt: str,
    timeout: int,
    sleeper: Sleeper,
    requested_model: str = "",
) -> tuple[Envelope, CliResult, list[str]]:
    """One CLI call with exponential backoff on transient failure."""
    notes: list[str] = []
    envelope = Envelope("", "", 0, True, parse_error="not attempted")
    cli = CliResult(returncode=-1, stdout="", stderr="", duration_s=0.0)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        cli = transport(cmd, prompt, timeout)
        envelope = isolation.parse_envelope(cli.stdout, requested_model=requested_model)
        if cli.returncode == 0 and envelope.ok:
            return envelope, cli, notes

        reason = envelope.parse_error or envelope.result or cli.stderr or f"exit {cli.returncode}"
        notes.append(f"attempt {attempt}: {str(reason)[:300]}")
        if attempt == MAX_ATTEMPTS or not is_retryable(envelope, cli):
            break
        delay = BACKOFF_SECONDS[min(attempt - 1, len(BACKOFF_SECONDS) - 1)]
        notes.append(f"backing off {delay}s")
        sleeper(delay)

    return envelope, cli, notes


# --- one cell ----------------------------------------------------------------


def generate_one(
    model: str,
    spec: prompt_bank.FormatSpec,
    prompt: prompt_bank.Prompt,
    corpus_root: Path,
    probe_transcript: str,
    transport: Transport = isolation.run_cli,
    timeout: int = isolation.GENERATION_TIMEOUT_S,
    sleeper: Sleeper = time.sleep,
    cli_version: str = "",
    target_override: int | None = None,
) -> CellResult:
    """Generate, continue to the floor if short, and write doc + sidecar."""
    effective = spec
    if target_override is not None:
        # Smoke path: shrink the ask without touching the bank on disk. The
        # floor moves with it, so a smoke document is still checked against a
        # floor — it just is not the corpus floor, and it is not corpus-grade.
        effective = prompt_bank.FormatSpec(
            format=spec.format,
            bundle=spec.bundle,
            target_words=target_override,
            min_words=int(target_override * 0.9),
            output_convention=spec.output_convention,
            prompts=spec.prompts,
            path=spec.path,
        )

    composed = prompt_bank.compose_prompt(effective, prompt)
    envelope, cli, notes = _call(
        transport, isolation.build_cmd(model), composed, timeout, sleeper, model
    )

    if not (cli.returncode == 0 and envelope.ok):
        return _record_failure(
            corpus_root, model, spec.format, prompt.id, envelope, cli, notes, composed
        )

    # A document whose text came from a model other than the one on the label is
    # not a weaker data point, it is a false one: the benchmark's whole output is
    # a per-model comparison. Fail the cell loudly rather than write it down.
    if envelope.model_mismatch:
        notes.append(
            f"model mismatch: asked for {model}, modelUsage has "
            f"{sorted(envelope.model_usage) or 'nothing'}"
        )
        return _record_failure(
            corpus_root, model, spec.format, prompt.id, envelope, cli, notes, composed
        )

    chunks = [envelope.result]
    boundaries: list[int] = []
    usage_in = int(envelope.usage.get("input_tokens") or 0)
    usage_out = int(envelope.usage.get("output_tokens") or 0)
    usage_cache = int(envelope.usage.get("cache_read_input_tokens") or 0) + int(
        envelope.usage.get("cache_creation_input_tokens") or 0
    )
    model_usage = dict(envelope.raw.get("modelUsage") or {})
    session_id = envelope.session_id
    model_reported = envelope.model_reported
    continuations = 0

    text = envelope.result
    words = isolation.textstat_words(text)

    while words < effective.min_words and continuations < MAX_CONTINUATIONS:
        if not session_id:
            notes.append("no session_id returned; cannot continue")
            break
        cont_env, cont_cli, cont_notes = _call(
            transport,
            isolation.build_cmd(model, ["--resume", session_id]),
            CONTINUE_PROMPT,
            timeout,
            sleeper,
            model,
        )
        notes.extend(cont_notes)
        if not (cont_cli.returncode == 0 and cont_env.ok) or not cont_env.result.strip():
            notes.append(f"continuation {continuations + 1} produced nothing; stopping")
            break

        if cont_env.model_mismatch:
            notes.append(
                f"model mismatch on continuation {continuations + 1}: asked for "
                f"{model}, modelUsage has {sorted(cont_env.model_usage) or 'nothing'}"
            )
            return _record_failure(
                corpus_root, model, spec.format, prompt.id, cont_env, cont_cli, notes, composed
            )

        # Offset into the concatenated document where this continuation begins.
        boundaries.append(len("\n\n".join(chunks)) + 2)
        chunks.append(cont_env.result)
        continuations += 1
        usage_in += int(cont_env.usage.get("input_tokens") or 0)
        usage_out += int(cont_env.usage.get("output_tokens") or 0)
        usage_cache += int(cont_env.usage.get("cache_read_input_tokens") or 0) + int(
            cont_env.usage.get("cache_creation_input_tokens") or 0
        )
        model_usage.update(cont_env.raw.get("modelUsage") or {})
        if cont_env.session_id:
            session_id = cont_env.session_id
        model_reported = model_reported or cont_env.model_reported

        text = "\n\n".join(chunks)
        words = isolation.textstat_words(text)

    text = "\n\n".join(chunks)
    words = isolation.textstat_words(text)

    path = doc_path(corpus_root, model, prompt.id)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = text if text.endswith("\n") else text + "\n"
    path.write_text(raw, encoding="utf-8")

    sidecar = {
        "model_requested": model,
        "model_reported": model_reported,
        "prompt_id": prompt.id,
        "format": spec.format,
        "domain": prompt.domain,
        "prompt_sha256": prompt_bank.prompt_sha256(composed),
        "system_prompt_sha256": isolation.SYSTEM_PROMPT_SHA256,
        "timestamp": _now(),
        "words": words,
        "target_words": effective.target_words,
        "min_words": effective.min_words,
        "met_floor": words >= effective.min_words,
        "continuations": continuations,
        "continuation_boundaries": boundaries,
        "cli_version": cli_version or isolation.cli_version(),
        "doc_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "isolation_probe": probe_transcript,
        "session_id": session_id,
        "usage": {
            "input_tokens": usage_in,
            "output_tokens": usage_out,
            "cache_input_tokens": usage_cache,
        },
        # Kept whole because it is the only place the harness's own side-calls
        # to other models are visible; model_reported is derived from it.
        "model_usage": model_usage,
        "model_mismatch": False,
        "notes": notes,
    }
    if target_override is not None:
        sidecar["target_override"] = target_override
    sidecar_path(corpus_root, model, prompt.id).write_text(
        json.dumps(sidecar, indent=2) + "\n", encoding="utf-8"
    )

    failure_path(corpus_root, model, prompt.id).unlink(missing_ok=True)

    return CellResult(
        model=model,
        fmt=spec.format,
        prompt_id=prompt.id,
        status="written",
        words=words,
        continuations=continuations,
        path=path,
        detail="" if words >= effective.min_words else f"below floor ({words} < {effective.min_words})",
    )


def _record_failure(
    corpus_root: Path,
    model: str,
    fmt: str,
    prompt_id: str,
    envelope: Envelope,
    cli: CliResult,
    notes: list[str],
    composed: str,
) -> CellResult:
    path = failure_path(corpus_root, model, prompt_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model_requested": model,
                "format": fmt,
                "prompt_id": prompt_id,
                "timestamp": _now(),
                "returncode": cli.returncode,
                "timed_out": cli.timed_out,
                "is_error": envelope.is_error,
                "parse_error": envelope.parse_error,
                "result": envelope.result[:2000],
                "stderr": (cli.stderr or "")[:2000],
                "prompt_sha256": prompt_bank.prompt_sha256(composed),
                "attempts": notes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return CellResult(
        model=model,
        fmt=fmt,
        prompt_id=prompt_id,
        status="failed",
        detail=notes[-1] if notes else "unknown failure",
    )


# --- the batch ---------------------------------------------------------------


def generate(
    models: Sequence[str] | None = None,
    formats: Sequence[str] | None = None,
    limit: int | None = None,
    corpus_root: Path = Path("corpus"),
    force: bool = False,
    bank_dir: Path | None = None,
    runs_root: Path = Path("runs"),
    skip_isolation_check: bool = False,
    transport: Transport = isolation.run_cli,
    timeout: int = isolation.GENERATION_TIMEOUT_S,
    sleeper: Sleeper = time.sleep,
    target_override: int | None = None,
    log: Callable[[str], None] = print,
) -> GenerateReport:
    """Fill every requested cell that is not already filled to the floor."""
    models = list(models) if models else list(MODELS)
    wanted_formats = list(formats) if formats else list(FORMATS)

    violations = prompt_bank.bank_lint(bank_dir)
    if violations:
        raise ValueError(
            "prompt bank does not lint; refusing to generate:\n  "
            + "\n  ".join(violations[:10])
        )
    bank = prompt_bank.load_prompt_bank(bank_dir)

    unknown = [f for f in wanted_formats if f not in bank]
    if unknown:
        raise ValueError(f"unknown format(s): {unknown}")

    probes: dict[str, str] = {}
    for model in models:
        transcript = isolation.latest_passing_battery(runs_root, model)
        if transcript is None:
            if not skip_isolation_check:
                raise RuntimeError(
                    f"no isolation probe battery passed for {model} in the last 24h. "
                    f"Run: python3 -m telltale verify-isolation --model {model}"
                )
            log(
                "\n"
                "!!! WARNING: generating without a fresh isolation probe for "
                f"{model}.\n"
                "!!! Documents produced now cannot be shown to be free of this "
                "machine's\n"
                "!!! CLAUDE.md, skills, and settings. They are not corpus-grade "
                "evidence.\n"
            )
            probes[model] = ""
        else:
            probes[model] = str(transcript)

    version = isolation.cli_version()
    report = GenerateReport()
    produced = 0

    for model in models:
        for fmt in sorted(wanted_formats):
            spec = bank[fmt]
            for prompt in sorted(spec.prompts, key=lambda p: p.id):
                if limit is not None and produced >= limit:
                    return report

                floor = spec.min_words if target_override is None else int(target_override * 0.9)
                have = existing_words(corpus_root, model, prompt.id)
                if not force and have is not None and have >= floor:
                    report.cells.append(
                        CellResult(model, fmt, prompt.id, "skipped", words=have)
                    )
                    continue

                log(f"[generate] {model} {prompt.id} ...")
                cell = generate_one(
                    model=model,
                    spec=spec,
                    prompt=prompt,
                    corpus_root=Path(corpus_root),
                    probe_transcript=probes.get(model, ""),
                    transport=transport,
                    timeout=timeout,
                    sleeper=sleeper,
                    cli_version=version,
                    target_override=target_override,
                )
                report.cells.append(cell)
                produced += 1
                suffix = f" ({cell.detail})" if cell.detail else ""
                log(
                    f"[generate] {model} {prompt.id} -> {cell.status} "
                    f"{cell.words} words, {cell.continuations} continuation(s){suffix}"
                )

    return report


# --- status ------------------------------------------------------------------


def status(
    corpus_root: Path = Path("corpus"),
    models: Sequence[str] | None = None,
    formats: Sequence[str] | None = None,
    bank_dir: Path | None = None,
) -> str:
    """A model x format completion matrix with word totals."""
    models = list(models) if models else list(MODELS)
    wanted = list(formats) if formats else list(FORMATS)
    try:
        bank = prompt_bank.load_prompt_bank(bank_dir)
    except (OSError, ValueError):
        bank = {}

    width = max([len(f) for f in wanted] + [6])
    header = "format".ljust(width) + "  " + "  ".join(m.rjust(16) for m in models)
    lines = [header, "-" * len(header)]

    grand: dict[str, int] = {m: 0 for m in models}
    grand_docs: dict[str, int] = {m: 0 for m in models}

    for fmt in wanted:
        spec = bank.get(fmt)
        expected = len(spec.prompts) if spec else 8
        floor = spec.min_words if spec else 0
        cells = []
        for model in models:
            done = 0
            words = 0
            for index in range(1, expected + 1):
                prompt_id = f"{fmt}-{index:02d}"
                have = existing_words(Path(corpus_root), model, prompt_id)
                if have is not None and have >= floor:
                    done += 1
                    words += have
            grand[model] += words
            grand_docs[model] += done
            cells.append(f"{done}/{expected} {words:>7,}w".rjust(16))
        lines.append(fmt.ljust(width) + "  " + "  ".join(cells))

    lines.append("-" * len(header))
    totals = [f"{grand_docs[m]} {grand[m]:>7,}w".rjust(16) for m in models]
    lines.append("TOTAL".ljust(width) + "  " + "  ".join(totals))
    return "\n".join(lines)


def scan_contamination(
    text: str,
    config_path: Path | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    """Contamination markers present in generated text. Empty is what we want.

    Scans against the committed markers plus whatever this machine resolves at
    call time — the account email above all, since that is the one piece of the
    user's configuration known to reach an isolated session.
    """
    return isolation.found_markers(
        text, isolation.effective_markers(config_path, repo_root)
    )


def iter_cells(
    bank: dict[str, prompt_bank.FormatSpec],
    models: Iterable[str],
    formats: Iterable[str],
) -> Iterable[tuple[str, prompt_bank.FormatSpec, prompt_bank.Prompt]]:
    """Deterministic (model, spec, prompt) order — the order generate walks."""
    for model in models:
        for fmt in sorted(formats):
            spec = bank[fmt]
            for prompt in sorted(spec.prompts, key=lambda p: p.id):
                yield model, spec, prompt


__all__ = [
    "MODELS",
    "CellResult",
    "GenerateReport",
    "generate",
    "generate_one",
    "status",
    "existing_words",
    "scan_contamination",
    "is_retryable",
    "doc_path",
    "sidecar_path",
    "failure_path",
    "iter_cells",
]
