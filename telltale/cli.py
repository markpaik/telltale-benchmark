"""Command line interface: `python3 -m telltale ...`."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from telltale.registry import Registry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = PROJECT_ROOT / "registry" / "tells.yaml"
DEFAULT_CORPUS = PROJECT_ROOT / "corpus"
DEFAULT_RUNS = PROJECT_ROOT / "runs"
DEFAULT_BANK = PROJECT_ROOT / "prompts" / "formats"
DEFAULT_DISCOVERY = PROJECT_ROOT / "runs" / "discovery"


# --- registry subcommands ----------------------------------------------------


def cmd_registry_validate(args: argparse.Namespace) -> int:
    registry = Registry(args.registry)
    errors = registry.validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"\n{len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        f"OK: {len(registry.active_tells())} active tells, "
        f"registry v{registry.version}, hash {registry.content_hash[:12]}"
    )
    return 0


def cmd_registry_promote(args: argparse.Namespace) -> int:
    return _set_status(args, "active")


def cmd_registry_deprecate(args: argparse.Namespace) -> int:
    return _set_status(args, "deprecated")


def _set_status(args: argparse.Namespace, status: str) -> int:
    registry = Registry(args.registry)
    try:
        registry.set_status(args.tell_id, status)
    except KeyError:
        print(f"no such tell: {args.tell_id}", file=sys.stderr)
        return 1
    print(f"{args.tell_id} -> {status} (registry v{registry.version})")
    return 0


def cmd_registry_diff(args: argparse.Namespace) -> int:
    path = Path(args.registry).resolve()
    root = path.parent.parent
    result = subprocess.run(
        ["git", "diff", "--", str(path)],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    sys.stdout.write(result.stdout)
    return 0


def _add_registry_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("registry", help="inspect and edit the tell registry")
    actions = parser.add_subparsers(dest="action", required=True)

    validate = actions.add_parser("validate", help="check the registry against the schema")
    validate.set_defaults(func=cmd_registry_validate)

    promote = actions.add_parser("promote", help="mark a candidate tell active")
    promote.add_argument("tell_id")
    promote.set_defaults(func=cmd_registry_promote)

    deprecate = actions.add_parser("deprecate", help="mark a tell deprecated")
    deprecate.add_argument("tell_id")
    deprecate.set_defaults(func=cmd_registry_deprecate)

    diff = actions.add_parser("diff", help="git diff of the registry file")
    diff.set_defaults(func=cmd_registry_diff)


# --- generation subcommands --------------------------------------------------


def cmd_generate(args: argparse.Namespace) -> int:
    from telltale import generate as gen

    try:
        report = gen.generate(
            models=args.models,
            formats=args.formats,
            limit=args.limit,
            corpus_root=args.corpus,
            force=args.force,
            bank_dir=args.bank,
            runs_root=args.runs,
            skip_isolation_check=args.skip_isolation_check,
            target_override=args.target_override,
        )
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(
        f"\nwritten {len(report.written)}, skipped {len(report.skipped)}, "
        f"failed {len(report.failed)}"
    )
    for cell in report.failed:
        print(f"  FAILED {cell.model} {cell.prompt_id}: {cell.detail}", file=sys.stderr)
    return 1 if report.failed else 0


def cmd_generate_status(args: argparse.Namespace) -> int:
    from telltale import generate as gen

    print(
        gen.status(
            corpus_root=args.corpus,
            models=args.models,
            formats=args.formats,
            bank_dir=args.bank,
        )
    )
    return 0


def cmd_verify_isolation(args: argparse.Namespace) -> int:
    from telltale import isolation

    out = args.out or isolation.battery_path(args.runs, args.model)
    report = isolation.run_probe_battery(args.model, out)
    print(report.summary())
    print(f"transcript: {out}")
    if not report.passed:
        print(
            "\nIsolation is NOT established. Generation would produce documents "
            "that cannot be shown to be free of this machine's configuration.",
            file=sys.stderr,
        )
    return 0 if report.passed else 1


def _add_generate_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("generate", help="generate the document corpus")
    parser.add_argument("--models", nargs="*", default=None, help="model ids (default: all three)")
    parser.add_argument("--formats", nargs="*", default=None, help="formats (default: all 14)")
    parser.add_argument("--limit", type=int, default=None, help="stop after N generations")
    parser.add_argument("--force", action="store_true", help="regenerate cells that already exist")
    parser.add_argument(
        "--skip-isolation-check",
        action="store_true",
        help="generate without a fresh isolation probe (documents are not corpus-grade)",
    )
    parser.add_argument(
        "--target-override",
        type=int,
        default=None,
        help="shrink the word target for a cheap smoke run; marks the sidecar",
    )
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    parser.set_defaults(func=cmd_generate)

    actions = parser.add_subparsers(dest="action")
    status = actions.add_parser("status", help="model x format completion matrix")
    status.add_argument("--models", nargs="*", default=None)
    status.add_argument("--formats", nargs="*", default=None)
    status.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    status.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    status.set_defaults(func=cmd_generate_status)


def _add_verify_isolation_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "verify-isolation",
        help="run the live probe battery and record the transcript",
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--out", type=Path, default=None)
    parser.set_defaults(func=cmd_verify_isolation)


def _add_prompts_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("prompts", help="inspect the prompt bank")
    actions = parser.add_subparsers(dest="action", required=True)

    lint = actions.add_parser("lint", help="check the bank against the design")
    lint.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    lint.set_defaults(func=cmd_prompts_lint)

    show = actions.add_parser("show", help="print the composed prompt for one id")
    show.add_argument("prompt_id")
    show.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    show.set_defaults(func=cmd_prompts_show)


def cmd_prompts_lint(args: argparse.Namespace) -> int:
    from telltale import prompts

    violations = prompts.bank_lint(args.bank)
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        print(f"\n{len(violations)} violation(s)", file=sys.stderr)
        return 1
    bank = prompts.load_prompt_bank(args.bank)
    total = sum(len(spec.prompts) for spec in bank.values())
    print(f"OK: {len(bank)} formats, {total} prompts, no violations")
    return 0


def cmd_prompts_show(args: argparse.Namespace) -> int:
    from telltale import prompts

    bank = prompts.load_prompt_bank(args.bank)
    for spec in bank.values():
        try:
            prompt = spec.prompt(args.prompt_id)
        except KeyError:
            continue
        print(prompts.compose_prompt(spec, prompt))
        return 0
    print(f"no such prompt id: {args.prompt_id}", file=sys.stderr)
    return 1


# --- scoring and reporting ---------------------------------------------------


def _progress_printer():
    """Timestamped progress lines on stdout, flushed, for a detached sweep.

    Flushing matters: a judge sweep is redirected to a log someone is tailing
    for hours, and Python's block buffering on a non-tty would hold the last
    several minutes of it hostage.
    """
    import time

    started = time.monotonic()

    def emit(line: str) -> None:
        elapsed = time.monotonic() - started
        print(f"[{elapsed / 60:7.1f}m] {line}", flush=True)

    return emit


def cmd_score(args: argparse.Namespace) -> int:
    from telltale import report

    run_dir = report.score_run(
        corpus_root=args.corpus,
        registry_path=args.registry,
        out_root=args.out,
        include_candidates=args.include_candidates,
        cli_args=sys.argv[1:],
        bootstrap_n=args.bootstrap,
        seed=args.seed,
        judge=args.judge,
        judge_model=args.judge_model,
        runs_root=args.out,
        progress=_progress_printer() if args.judge else None,
        judge_workers=args.judge_workers,
        judge_ceiling=args.judge_ceiling,
        notes=args.note,
        judge_sample=args.sample,
        judge_sample_seed=args.sample_seed,
        judge_doc_list=(
            __import__("telltale.judge.sampling", fromlist=["x"]).read_doc_list(args.doc_list)
            if args.doc_list
            else None
        ),
    )
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    corpus = manifest["corpus"]
    registry_info = manifest["registry"]
    judge_info = manifest.get("judge") or {}
    if corpus["n_docs"] == 0:
        print(f"no documents under {args.corpus}", file=sys.stderr)
    if judge_info.get("enabled"):
        skipped = judge_info.get("tells_skipped") or {}
        print(
            f"scored {corpus['n_docs']} docs x {registry_info['n_scored']} tells "
            f"({len(judge_info.get('tells_scored') or [])} judge tells via "
            f"{judge_info.get('model')}, {len(skipped)} uncalibrated and skipped)"
        )
        for tell_id, why in sorted(skipped.items()):
            print(f"  SKIPPED {tell_id}: {why}", file=sys.stderr)
        _warn_on_disagreement(judge_info)
    else:
        print(
            f"scored {corpus['n_docs']} docs x {registry_info['n_scored']} tells "
            f"({registry_info['judge_skipped']} judge tells skipped, M6)"
        )
    print(run_dir)
    return 0


def _warn_on_disagreement(judge_info: dict) -> None:
    """Say loudly when the judge kept disagreeing with the decision code.

    A high rate is not a bug in either half. It is a rubric that has an
    exclusion the judge can feel and cannot name, and it is invisible to the
    calibration gate — the gate scores twenty snippets written to be
    unambiguous, which is exactly where this would not show up.
    """
    disagreement = judge_info.get("disagreements") or {}
    per_tell = disagreement.get("per_tell") or {}
    flagged = disagreement.get("over_threshold") or []
    if not flagged:
        return
    threshold = float(disagreement.get("threshold") or 0.20)
    print(
        f"\nWARNING: the judge's own verdict disagreed with the rubric's decision "
        f"on more than {100 * threshold:.0f}% of counted spans for "
        f"{len(flagged)} tell(s):",
        file=sys.stderr,
    )
    for tell_id in flagged:
        entry = per_tell.get(tell_id) or {}
        rate = entry.get("rate")
        share = (
            f"({100.0 * float(rate):.0f}%)"
            if rate is not None
            else "(nothing counted at all — the criteria never close)"
        )
        print(
            f"  {tell_id}: {entry.get('disagreements', 0)} of "
            f"{entry.get('counted', 0)} counted spans {share}",
            file=sys.stderr,
        )
    print(
        "  The criteria are being satisfied on spans the judge does not think "
        "are instances. That usually means the rubric needs an exclusion it "
        "does not have yet; check the rationales in scores.jsonl.",
        file=sys.stderr,
    )


def cmd_report(args: argparse.Namespace) -> int:
    from telltale import manifest as manifest_mod

    if args.verify:
        result = manifest_mod.verify(args.verify)
        print(result.summary())
        return 0 if result.ok else 1

    from telltale import report

    path = report.render_scorecard(args.render)
    print(path)
    return 0


def _add_score_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("score", help="score a corpus and write a run directory")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_RUNS,
        help="runs root; a <run_id> directory is created inside it",
    )
    parser.add_argument(
        "--include-candidates",
        action="store_true",
        help="also detect candidate tells (they are reported but stay out of the index)",
    )
    parser.add_argument("--bootstrap", type=int, default=1000, help="bootstrap replicates")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--judge",
        action="store_true",
        help="also score Tier-2 judge tells (calibrated ones only)",
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help="judge model id; default resolves the allowlist in order",
    )
    parser.add_argument(
        "--judge-workers",
        type=int,
        default=4,
        help="concurrent judge measurements to start with (default: %(default)s)",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        metavar="N",
        help="restrict judge tells to a stratified sample of N documents "
        "(Tier-1 still scores the whole corpus)",
    )
    parser.add_argument(
        "--sample-seed", type=int, default=7, help="seed for the judge sample"
    )
    parser.add_argument(
        "--note",
        action="append",
        default=None,
        metavar="TEXT",
        help="operator note recorded in the manifest (repeatable)",
    )
    parser.add_argument(
        "--doc-list",
        type=Path,
        default=None,
        help="file of document ids, one per line, to judge instead of a sample",
    )
    parser.add_argument(
        "--judge-ceiling",
        type=int,
        default=6,
        help="most concurrent judge measurements to ever run (default: %(default)s)",
    )
    parser.set_defaults(func=cmd_score)


def _add_report_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("report", help="re-render or verify a run directory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--verify",
        type=Path,
        metavar="RUN_DIR",
        help="recompute the run from its manifest and require byte-identical outputs",
    )
    group.add_argument(
        "--render",
        type=Path,
        metavar="RUN_DIR",
        help="re-render scorecard.md from an existing run directory",
    )
    parser.set_defaults(func=cmd_report)


# --- judge subcommands -------------------------------------------------------


def _resolved_judge(args: argparse.Namespace) -> str:
    from telltale.judge.transport import resolve_judge

    if getattr(args, "model", None):
        return str(args.model)
    model = resolve_judge()
    print(f"judge resolved to {model}")
    return model


def cmd_judge_probe(args: argparse.Namespace) -> int:
    from telltale.judge.transport import JUDGE_MODEL_ORDER, probe_judge

    order = [args.model] if args.model else list(JUDGE_MODEL_ORDER)
    ok = False
    for model in order:
        available = probe_judge(model)
        print(f"  {'OK  ' if available else 'DOWN'}  {model}")
        ok = ok or available
    return 0 if ok else 1


def cmd_judge_calibrate(args: argparse.Namespace) -> int:
    from telltale.judge import build_backend
    from telltale.judge import calibrate as calibration
    from telltale.registry import Registry

    registry = Registry(args.registry)
    tells = calibration.judge_tells(registry)
    if args.tell:
        tells = [t for t in tells if t.id == args.tell]
        if not tells:
            print(f"no judge tell with id {args.tell}", file=sys.stderr)
            return 1

    model = _resolved_judge(args)
    backend = build_backend(model=model, force=args.force)

    failed = 0
    for tell in tells:
        try:
            snippets = calibration.load_snippets(tell.id)
        except KeyError as exc:
            print(str(exc), file=sys.stderr)
            failed += 1
            continue
        problems = calibration.lint_snippets(tell, snippets)
        for problem in problems:
            print(f"  lint: {problem}", file=sys.stderr)
        report = calibration.calibrate(tell, backend, snippets=snippets)
        print(report.summary())
        path = calibration.write_report(report, args.runs)
        print(f"    report: {path}")
        if not report.passed:
            failed += 1
    return 1 if failed else 0


def cmd_judge_audit(args: argparse.Namespace) -> int:
    import json as _json

    from telltale.corpus import load_corpus
    from telltale.judge import audit as audit_mod
    from telltale.judge import build_backend
    from telltale.registry import Registry

    registry = Registry(args.registry)
    tells = [t for t in registry.active_tells() if t.method == "judge"]
    if args.tell:
        tells = [t for t in tells if t.id == args.tell]
        if not tells:
            print(f"no judge tell with id {args.tell}", file=sys.stderr)
            return 1

    docs = load_corpus(args.corpus)
    model = _resolved_judge(args)
    backend = build_backend(model=model)
    report = audit_mod.audit(
        docs, tells, backend.client, pct=args.pct, seed=args.seed,
        max_calls=args.max_calls,
        progress=lambda line: print(line, file=sys.stderr, flush=True),
    )
    print(report.summary())
    for item in report.items:
        if item.agreement < 1.0:
            print(
                f"  {item.tell_id} {item.doc_id}#{item.chunk_index}: "
                f"{item.agreement:.2f} (cached {item.cached_spans}, "
                f"live {item.live_spans}, shared {item.shared})"
            )
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_json.dumps(report.as_dict(), indent=2) + "\n", encoding="utf-8")
        print(f"report: {out}")
    return 0


def _add_judge_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("judge", help="Tier-2 judge: probe, calibrate, audit")
    actions = parser.add_subparsers(dest="action", required=True)

    probe = actions.add_parser("probe", help="check which allowlisted judges answer")
    probe.add_argument("--model", default=None)
    probe.set_defaults(func=cmd_judge_probe)

    calibrate = actions.add_parser(
        "calibrate", help="run the labelled snippet sets and write the gate report"
    )
    calibrate.add_argument("--tell", default=None, help="one tell id (default: all seven)")
    calibrate.add_argument("--model", default=None, help="judge model id")
    calibrate.add_argument(
        "--force", action="store_true", help="ignore cached judge answers"
    )
    calibrate.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    calibrate.set_defaults(func=cmd_judge_calibrate)

    audit = actions.add_parser(
        "audit", help="re-ask a sample of cached extractions live and compare span sets"
    )
    audit.add_argument("--pct", type=float, default=5.0)
    audit.add_argument("--seed", type=int, default=11)
    audit.add_argument(
        "--max-calls",
        type=int,
        default=None,
        help="budget ceiling on live judge calls; the draw is trimmed, not the tells",
    )
    audit.add_argument("--tell", default=None)
    audit.add_argument("--model", default=None)
    audit.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    audit.add_argument("--out", type=Path, default=None)
    audit.set_defaults(func=cmd_judge_audit)


# --- discovery subcommands ---------------------------------------------------


def _discover_client(args: argparse.Namespace, cache_only: bool = False) -> Any:
    """A `JudgeClient` on the resolved judge, sharing the run-wide judge cache."""
    from telltale.discovery.auditor import LENS_TIMEOUT_S
    from telltale.judge import DEFAULT_CACHE_ROOT
    from telltale.judge.cache import JudgeCache, JudgeClient
    from telltale.judge.transport import CliJudgeTransport

    model = _resolved_judge(args)
    wire = CliJudgeTransport(model=model, timeout=LENS_TIMEOUT_S)
    cache = JudgeCache(DEFAULT_CACHE_ROOT)
    return JudgeClient(
        transport=wire,
        cache=cache,
        force=getattr(args, "force_judge", False),
        cache_only=cache_only,
    )


def cmd_discover_sweep(args: argparse.Namespace) -> int:
    from telltale.corpus import load_corpus
    from telltale.discovery import pipeline
    from telltale.discovery import sweep as sweep_mod

    docs = load_corpus(args.corpus)
    if not docs:
        print(f"no documents under {args.corpus}", file=sys.stderr)
        return 1
    # Into <out>/sweep, the same place `run-all` puts it and the same place
    # `audit` looks for it, so the three compose without extra flags.
    out = pipeline.sweep_dir(args.out)
    summary = sweep_mod.run_sweep(
        docs,
        out,
        z_min=args.z_min,
        min_count=args.min_count,
        top_k=args.top_k,
    )
    print(
        f"swept {summary['n_docs']} docs across {len(summary['models'])} model(s) -> "
        f"{out}"
    )
    for name, count in sorted(summary["written"].items()):
        print(f"  {name}: {count} rows")
    return 0


def cmd_discover_audit(args: argparse.Namespace) -> int:
    from telltale.corpus import load_corpus
    from telltale.discovery import auditor, pipeline

    docs = load_corpus(args.corpus)
    if not docs:
        print(f"no documents under {args.corpus}", file=sys.stderr)
        return 1
    registry = Registry(args.registry)
    sweep_root = pipeline.sweep_dir(args.out) if args.sweep is None else args.sweep
    from telltale.discovery import sweep as sweep_mod

    rows = sweep_mod.load_sweep(sweep_root, model=args.target_model)
    if not rows:
        print(
            f"note: no sweep rows for {args.target_model} under {sweep_root}; "
            "the lens will run without the n-gram table",
            file=sys.stderr,
        )

    client = _discover_client(args)
    run = auditor.run_audit(
        docs,
        client,
        args.lens,
        args.target_model,
        out_dir=pipeline.audit_dir(args.out),
        sweep_rows=rows,
        existing_tells=registry.active_tells(include_candidates=True),
    )
    print(
        f"{args.lens} lens on {args.target_model}: {len(run.candidates)} candidate(s), "
        f"{len(run.rejected)} rejected"
        + (" (retried once)" if run.retried else "")
        + (" [cached]" if run.cached else "")
    )
    for candidate in run.candidates:
        rule = candidate.get("rule") or {}
        detail = rule.get("pattern") or rule.get("stat_name") or rule.get("judge_view")
        print(f"  {candidate.get('name')!r} [{candidate.get('method')}] {detail!r}")
    for entry in run.rejected:
        print(
            f"  REJECTED {entry.get('candidate', {}).get('name')!r}: "
            + "; ".join(entry.get("errors") or []),
            file=sys.stderr,
        )
    return 0


def cmd_discover_verify(args: argparse.Namespace) -> int:
    from telltale.corpus import load_corpus
    from telltale.discovery import pipeline

    docs = load_corpus(args.corpus)
    if not docs:
        print(f"no documents under {args.corpus}", file=sys.stderr)
        return 1
    registry = Registry(args.registry)
    judge = None if args.no_judge else _discover_client(args)

    log, verdicts = pipeline.stage_verify(
        docs,
        args.out,
        registry,
        judge,
        candidates_dir=args.candidates,
        force=args.force,
        seed=args.seed,
    )
    print(log.line())
    for verdict in verdicts:
        print("  " + verdict.summary())
    if args.append and verdicts:
        append_log = pipeline.stage_append(
            docs, args.out, registry, verdicts, args.run_id or "", force=args.force
        )
        print(append_log.line())
    return 0


def cmd_discover_run_all(args: argparse.Namespace) -> int:
    from telltale.corpus import load_corpus
    from telltale.discovery import pipeline

    docs = load_corpus(args.corpus)
    if not docs:
        print(f"no documents under {args.corpus}", file=sys.stderr)
        return 1
    registry = Registry(args.registry)
    client = None if args.no_judge else _discover_client(args)
    summary = pipeline.run_all(
        docs,
        args.out,
        registry,
        judge_client=client,
        judge_backend=client,
        models=args.models,
        run_id=args.run_id,
        force=args.force,
        seed=args.seed,
        log=print,
    )
    print(f"\nrun {summary['run_id']} -> {summary['out_dir']}")
    return 0


def _add_discover_parser(subparsers: argparse._SubParsersAction) -> None:
    from telltale.discovery.auditor import LENSES

    parser = subparsers.add_parser(
        "discover",
        help="M7: propose, verify, and register new candidate tells",
        description=(
            "Flags shared by every action (--corpus, --out, --model) belong to "
            "this group and go BEFORE the action: `discover --corpus X sweep`, "
            "not `discover sweep --corpus X`."
        ),
    )
    # Declared here and nowhere else. When a subparser re-declares a parent's
    # option, argparse writes its own default over the parsed value on the way
    # out — so `discover --corpus X run-all` silently ran against the default
    # corpus. One declaration per flag is the only version of this that cannot
    # go quietly wrong.
    parser.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help="corpus root (default: %(default)s)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_DISCOVERY,
        help="discovery working directory; every action reads and writes its own "
        "subdirectory of this (default: %(default)s)",
    )
    parser.add_argument("--model", default=None, help="judge model id for the lenses")
    actions = parser.add_subparsers(dest="action", required=True)

    sweep_cmd = actions.add_parser("sweep", help="the statistical sweep; no model calls")
    sweep_cmd.add_argument("--z-min", type=float, default=3.09)
    sweep_cmd.add_argument("--min-count", type=int, default=10)
    sweep_cmd.add_argument("--top-k", type=int, default=200)
    sweep_cmd.set_defaults(func=cmd_discover_sweep)

    audit = actions.add_parser("audit", help="run one lens against one target model")
    audit.add_argument("--lens", required=True, choices=list(LENSES))
    audit.add_argument("--target-model", required=True)
    audit.add_argument("--sweep", type=Path, default=None, help="sweep output directory")
    audit.add_argument(
        "--force-judge", action="store_true", help="ignore cached lens answers"
    )
    audit.set_defaults(func=cmd_discover_audit)

    verify_cmd = actions.add_parser(
        "verify", help="run proposed candidates through the gates"
    )
    verify_cmd.add_argument(
        "--candidates", type=Path, default=None, help="candidate jsonl dir"
    )
    verify_cmd.add_argument(
        "--no-judge",
        action="store_true",
        help="skip gate 4 (no regex candidate can be accepted without it)",
    )
    verify_cmd.add_argument("--force", action="store_true", help="re-verify completed stages")
    verify_cmd.add_argument("--force-judge", action="store_true")
    verify_cmd.add_argument("--append", action="store_true", help="append accepted candidates")
    verify_cmd.add_argument("--run-id", default=None)
    verify_cmd.add_argument("--seed", type=int, default=13)
    verify_cmd.set_defaults(func=cmd_discover_verify)

    run_all_cmd = actions.add_parser(
        "run-all", help="sweep -> lenses -> verify -> append, resumable per stage"
    )
    run_all_cmd.add_argument("--models", nargs="*", default=None)
    run_all_cmd.add_argument("--run-id", default=None)
    run_all_cmd.add_argument("--no-judge", action="store_true")
    run_all_cmd.add_argument("--force", action="store_true")
    run_all_cmd.add_argument("--force-judge", action="store_true")
    run_all_cmd.add_argument("--seed", type=int, default=13)
    run_all_cmd.set_defaults(func=cmd_discover_run_all)


# --- parser ------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telltale",
        description="A benchmark for AI-writing tells.",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="path to tells.yaml (default: %(default)s)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_registry_parser(subparsers)
    _add_prompts_parser(subparsers)
    _add_generate_parser(subparsers)
    _add_verify_isolation_parser(subparsers)
    _add_score_parser(subparsers)
    _add_report_parser(subparsers)
    _add_judge_parser(subparsers)
    _add_discover_parser(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
