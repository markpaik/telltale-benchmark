"""Load the prompt bank and compose the text handed to a generating model.

One YAML file per format under prompts/formats/, each holding eight scenarios.
The scenarios are the only thing that varies between generations, so they carry
a hard constraint: they describe a *situation*, never a way of writing. A
scenario that said "write this in a professional tone" would plant the very
behavior the benchmark is trying to observe, and the resulting score would
measure the prompt. `bank_lint` is what keeps that from happening quietly — it
is meant to be run in CI, not by hand.

The composed prompt is scenario, then the format's output convention, then a
length ask. Nothing else: no role-play preamble, no quality bar, no examples.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from telltale.corpus import FORMATS

#: Each format file must cover all eight domains, one prompt each.
DOMAINS: tuple[str, ...] = (
    "k12-education",
    "healthcare",
    "manufacturing",
    "nonprofit",
    "municipal-government",
    "retail",
    "logistics",
    "software",
)

#: Formats where one sample is a realistic *collection* of documents rather than
#: a single one. Kept here rather than in the YAML alone so bank_lint can catch a
#: file that drifts from the design.
BUNDLE_FORMATS: frozenset[str] = frozenset(
    {"email", "memo", "meeting-minutes", "executive-summary", "performance-review"}
)

PROMPTS_PER_FORMAT = 8

#: Banned in scenarios, case-insensitive, on word boundaries. "AI" needs the
#: boundary treatment or it would fire on email, training, maintain, chair.
BANNED_SCENARIO_PATTERNS: tuple[tuple[str, str], ...] = (
    ("AI", r"\bAI\b"),
    ("polished", r"\bpolish(?:ed|ing)?\b"),
    ("professional tone", r"\bprofessional[- ]?(?:tone|sounding)\b"),
    ("eloquent", r"\beloquent(?:ly)?\b"),
    ("well-written", r"\bwell[- ]written\b"),
    ("engaging", r"\bengaging\b"),
    ("writing style", r"\bwriting style\b"),
)

_BANNED = tuple(
    (label, re.compile(pattern, re.IGNORECASE)) for label, pattern in BANNED_SCENARIO_PATTERNS
)

ID_PATTERN = re.compile(r"^(?P<fmt>[a-z-]+)-(?P<index>\d{2})$")


@dataclass(frozen=True)
class Prompt:
    """One scenario within a format."""

    id: str
    domain: str
    scenario: str

    @property
    def index(self) -> int:
        match = ID_PATTERN.match(self.id)
        return int(match.group("index")) if match else 0

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.scenario.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FormatSpec:
    """One prompts/formats/<format>.yaml file."""

    format: str
    bundle: bool
    target_words: int
    min_words: int
    output_convention: str
    prompts: list[Prompt] = field(default_factory=list)
    path: Path | None = None

    def prompt(self, prompt_id: str) -> Prompt:
        for item in self.prompts:
            if item.id == prompt_id:
                return item
        raise KeyError(prompt_id)


def default_bank_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "prompts" / "formats"


def _coerce_spec(data: dict[str, Any], path: Path) -> FormatSpec:
    prompts = []
    for raw in data.get("prompts") or []:
        if not isinstance(raw, dict):
            continue
        prompts.append(
            Prompt(
                id=str(raw.get("id", "")).strip(),
                domain=str(raw.get("domain", "")).strip(),
                scenario=str(raw.get("scenario", "")).strip(),
            )
        )
    return FormatSpec(
        format=str(data.get("format", path.stem)).strip(),
        bundle=bool(data.get("bundle", False)),
        target_words=int(data.get("target_words") or 0),
        min_words=int(data.get("min_words") or 0),
        output_convention=str(data.get("output_convention", "")).strip(),
        prompts=prompts,
        path=path,
    )


def load_prompt_bank(directory: Path | None = None) -> dict[str, FormatSpec]:
    """Load every <format>.yaml under `directory`, keyed by format name.

    Raises on unreadable or non-mapping YAML: a half-loaded bank would silently
    shrink a generation run, which is worse than stopping.
    """
    directory = Path(directory) if directory is not None else default_bank_dir()
    bank: dict[str, FormatSpec] = {}
    for path in sorted(directory.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path}: top level is not a mapping")
        spec = _coerce_spec(data, path)
        bank[spec.format] = spec
    return bank


def compose_prompt(spec: FormatSpec, prompt: Prompt) -> str:
    """The exact user text sent to the model for one (format, scenario) cell."""
    pages = max(1, round(spec.target_words / 500))
    if spec.bundle:
        length = (
            f"The full set should run about {pages} pages of writing in total — "
            f"roughly {spec.target_words:,} words."
        )
    else:
        length = (
            f"The full document should run about {pages} pages — "
            f"roughly {spec.target_words:,} words."
        )
    return "\n\n".join([prompt.scenario.strip(), spec.output_convention.strip(), length])


def prompt_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bank_lint(directory: Path | None = None) -> list[str]:
    """Every way the bank can be wrong, as a list of human-readable violations.

    Empty list means the bank is fit to generate from.
    """
    directory = Path(directory) if directory is not None else default_bank_dir()
    violations: list[str] = []

    if not directory.is_dir():
        return [f"prompt bank directory does not exist: {directory}"]

    try:
        bank = load_prompt_bank(directory)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"bank does not load: {exc}"]

    missing = sorted(set(FORMATS) - set(bank))
    extra = sorted(set(bank) - set(FORMATS))
    for fmt in missing:
        violations.append(f"missing format file: {fmt}.yaml")
    for fmt in extra:
        violations.append(f"unexpected format file: {fmt}.yaml (not in corpus.FORMATS)")
    if len(bank) != len(FORMATS):
        violations.append(f"expected {len(FORMATS)} format files, found {len(bank)}")

    seen_ids: dict[str, str] = {}
    for fmt in sorted(bank):
        spec = bank[fmt]
        where = spec.path.name if spec.path else fmt

        if spec.format != Path(where).stem:
            violations.append(f"{where}: format field {spec.format!r} does not match filename")

        expected_bundle = fmt in BUNDLE_FORMATS
        if spec.bundle != expected_bundle:
            violations.append(
                f"{where}: bundle is {spec.bundle}, expected {expected_bundle}"
            )

        if spec.target_words <= 0:
            violations.append(f"{where}: target_words must be positive")
        if spec.min_words <= 0:
            violations.append(f"{where}: min_words must be positive")
        elif spec.min_words > spec.target_words:
            violations.append(
                f"{where}: min_words ({spec.min_words}) exceeds target_words ({spec.target_words})"
            )
        if not spec.output_convention:
            violations.append(f"{where}: output_convention is empty")

        if len(spec.prompts) != PROMPTS_PER_FORMAT:
            violations.append(
                f"{where}: {len(spec.prompts)} prompts, expected {PROMPTS_PER_FORMAT}"
            )

        domains_seen: list[str] = []
        for position, prompt in enumerate(spec.prompts, start=1):
            label = prompt.id or f"{where}#{position}"

            expected_id = f"{fmt}-{position:02d}"
            if prompt.id != expected_id:
                violations.append(f"{where}: prompt {position} has id {prompt.id!r}, expected {expected_id!r}")
            if prompt.id in seen_ids:
                violations.append(f"duplicate prompt id {prompt.id!r} in {where} and {seen_ids[prompt.id]}")
            elif prompt.id:
                seen_ids[prompt.id] = where

            if prompt.domain not in DOMAINS:
                violations.append(f"{label}: unknown domain {prompt.domain!r}")
            domains_seen.append(prompt.domain)

            if not prompt.scenario:
                violations.append(f"{label}: scenario is empty")
            elif len(prompt.scenario.split()) < 100:
                violations.append(
                    f"{label}: scenario is only {len(prompt.scenario.split())} words "
                    "(too thin to sustain a long document)"
                )

            for banned, pattern in _BANNED:
                match = pattern.search(prompt.scenario)
                if match:
                    violations.append(
                        f"{label}: scenario contains banned term {banned!r} "
                        f"(matched {match.group(0)!r}) — scenarios must not direct how to write"
                    )

        if sorted(domains_seen) != sorted(DOMAINS):
            counts = {d: domains_seen.count(d) for d in set(domains_seen)}
            violations.append(
                f"{where}: domains do not cover the rotation exactly once each: {counts}"
            )

    return violations
