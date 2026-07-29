"""Command line interface: `python3 -m telltale ...`."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from telltale.registry import Registry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = PROJECT_ROOT / "registry" / "tells.yaml"


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
    # Later milestones register their own groups here the same way:
    # _add_generate_parser(subparsers)   # M3
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
