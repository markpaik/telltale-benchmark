"""Command line interface: `python3 -m telltale ...`."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from telltale.registry import Registry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = PROJECT_ROOT / "registry" / "tells.yaml"
DEFAULT_CORPUS = PROJECT_ROOT / "corpus"
DEFAULT_RUNS = PROJECT_ROOT / "runs"
DEFAULT_BANK = PROJECT_ROOT / "prompts" / "formats"


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
    # Later milestones register their own groups here the same way:
    # _add_score_parser(subparsers)      # M2
    # _add_discover_parser(subparsers)   # M4
    # _add_report_parser(subparsers)     # M5

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
