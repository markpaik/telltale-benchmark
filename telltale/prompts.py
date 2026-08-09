"""Load the prompt bank and compose the text handed to a generating model.

One YAML file per format under prompts/formats/, each holding eight scenarios
(the exception is an exploratory annex format, which holds one prompt and no
scenario at all — see corpus.EXPLORATORY_FORMATS).
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

from telltale.corpus import EXPLORATORY_FORMATS, FORMATS

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


# --- cast uniqueness ---------------------------------------------------------
#
# Every scenario is supposed to be its own world. When the same person or the
# same company turns up in two scenarios, documents that are meant to be
# independent samples start sharing proper nouns, and a detector that keys on
# repeated names would see structure that is an artifact of how the bank was
# written rather than of how a model writes. Seven full names were reused across
# files on the first pass; this is what stops the eighth.

#: Words that disqualify a capitalized phrase from being read as a person's
#: name. Roles and org/place vocabulary, mostly — "Chief Financial Officer" and
#: "Valley Regional Medical Center" are supposed to recur, people are not.
NON_PERSON_WORDS: frozenset[str] = frozenset(
    """
    Chief Officer Director Deputy Vice President Superintendent Principal Manager
    Supervisor Coordinator Administrator Commissioner Controller Treasurer
    Secretary Chair Chairman Chairwoman Board Executive Senior Junior Assistant
    Associate Interim Acting Head Lead Staff Dr Mr Ms Mrs Prof Professor Nurse
    Physician Attorney Counsel Counselor Engineer Analyst Consultant Auditor
    Inspector Sergeant Captain Officers Trustee Trustees Member Members Chairs
    School Schools District University College Academy Academies Hospital Medical
    Health Center Centre Clinic Foundation Institute Council Committee Commission
    Department Division Office Bureau Agency Authority Group Systems System
    Services Service Company Corporation Corp Inc Llc Partners Alliance Network
    Collaborative Coalition Association Society Union Works Public Community
    Regional National State County City Township Village Town Municipal Valley
    River Lake Mountain Ridge Creek Harbor Bay Island Springs Falls Heights Park
    North South East West Northern Southern Eastern Western Upper Lower Central
    New Old Saint St Fort Port Grand Great Mount
    San Santa Los Las El La Des Du Eau Sault Rio Fond Baton Cape
    January February March April May June July August September October November
    December Monday Tuesday Wednesday Thursday Friday Saturday Sunday
    The A An In On At For And But By This That These Those Their His Her Its
    Last Next After Before During Since When While With Without All Both Each
    Every Most Some No Not First Second Third Fourth Fifth Final Total Annual
    Quarterly Monthly Weekly Daily Two Three Four Five Six Seven Eight Nine Ten
    """.split()
)

#: Org names generic enough that sharing them across scenarios is realistic
#: rather than a collision. Compared case-insensitively.
ORG_NAME_ALLOWLIST: frozenset[str] = frozenset(
    {
        "public works",
        "department of public works",
        "human resources",
        "information technology",
        "city council",
        "town council",
        "county council",
        "board of education",
        "school board",
        "planning commission",
    }
)

#: A capitalized run ending in one of these reads as an organization.
ORG_SUFFIXES: tuple[str, ...] = (
    "Group", "District", "Systems", "System", "Health", "Center", "Centre",
    "Works", "Mills", "Partners", "Alliance", "Foundation", "Academies",
    "Academy", "Schools", "School", "Services", "Logistics", "Markets",
    "Market", "Company", "Corporation", "Authority", "Collaborative",
    "Institute", "Network", "Payments", "Freight", "Carriers", "Labs",
    "Hospital", "Clinic", "Cooperative", "Council", "Coalition", "Association",
    "Industries", "Manufacturing", "Technologies", "Solutions", "Holdings",
)

_PERSON = re.compile(
    r"\b[A-Z][a-z]+(?:-[A-Z][a-z]+)?(?:\s+[A-Z][a-z']+){1,2}\b"
)

# "and" is deliberately not a connector: it over-captures across conjunctions
# ("the Council and Public Works" reads as one seven-word organization).
_ORG = re.compile(
    r"\b(?:[A-Z][A-Za-z&'.-]*\s+(?:of\s+|the\s+|for\s+)?){1,5}"
    r"(?:" + "|".join(ORG_SUFFIXES) + r")\b"
)

_LEADING_ARTICLE = re.compile(r"^(?:The|A|An)\s+")


def person_names(text: str) -> set[str]:
    """Two- and three-word capitalized phrases that read as people's names."""
    names = set()
    for match in _PERSON.findall(text or ""):
        words = re.split(r"[\s-]+", match)
        if any(word.rstrip(".").capitalize() in NON_PERSON_WORDS for word in words):
            continue
        names.add(match)
    return names


def org_names(text: str) -> set[str]:
    """Capitalized runs ending in an organization word, longest match wins."""
    found = set()
    for match in _ORG.findall(text or ""):
        name = _LEADING_ARTICLE.sub("", " ".join(match.split()))
        if name.lower() in ORG_NAME_ALLOWLIST:
            continue
        found.add(name)
    # A shorter name fully contained in a longer one is the same organization
    # seen through a smaller window ("Valley Regional Medical Center" inside
    # "Klamath Valley Regional Medical Center"); keep only the longest.
    return {
        name
        for name in found
        if not any(other != name and name in other for other in found)
    }


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
    #: Exploratory annex format (see corpus.EXPLORATORY_FORMATS): no length
    #: target, no floor, no continuations, and no place in the index.
    exploratory: bool = False

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
        exploratory=bool(data.get("exploratory", False)),
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
    # An exploratory prompt is sent exactly as written. The whole point of the
    # cell is that nothing was asked for — appending an output convention or a
    # length ask would put back the constraint the format exists to remove.
    if spec.exploratory:
        return prompt.scenario.strip()
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

        # The YAML flag and corpus.EXPLORATORY_FORMATS have to agree, or scoring
        # (which reads the constant) and generation (which reads the file) would
        # disagree about which documents are annex.
        expected_exploratory = fmt in EXPLORATORY_FORMATS
        if spec.exploratory != expected_exploratory:
            violations.append(
                f"{where}: exploratory is {spec.exploratory}, expected "
                f"{expected_exploratory} (corpus.EXPLORATORY_FORMATS)"
            )

        if spec.exploratory:
            # Length is the datum, so a target or a floor here would be a bug:
            # generate would compose a length ask and run the continuation ladder.
            if spec.target_words:
                violations.append(f"{where}: exploratory format must not set target_words")
            if spec.min_words:
                violations.append(f"{where}: exploratory format must not set min_words")
            if spec.output_convention:
                violations.append(
                    f"{where}: exploratory format must not set output_convention "
                    "(the prompt is sent verbatim)"
                )
            if not spec.prompts:
                violations.append(f"{where}: no prompts")
        else:
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

            # An exploratory prompt names no situation, so it has no domain and
            # no length to sustain: the domain rotation and the 100-word scenario
            # floor are both checks on a scenario it deliberately does not have.
            if not spec.exploratory and prompt.domain not in DOMAINS:
                violations.append(f"{label}: unknown domain {prompt.domain!r}")
            if spec.exploratory and prompt.domain:
                violations.append(
                    f"{label}: exploratory prompt must not carry a domain "
                    f"(has {prompt.domain!r})"
                )
            domains_seen.append(prompt.domain)

            if not prompt.scenario:
                violations.append(f"{label}: scenario is empty")
            elif not spec.exploratory and len(prompt.scenario.split()) < 100:
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

        if not spec.exploratory and sorted(domains_seen) != sorted(DOMAINS):
            counts = {d: domains_seen.count(d) for d in set(domains_seen)}
            violations.append(
                f"{where}: domains do not cover the rotation exactly once each: {counts}"
            )

    violations.extend(_cast_violations(bank))
    return violations


def _cast_violations(bank: dict[str, FormatSpec]) -> list[str]:
    """Person and organization names that appear in more than one scenario."""
    ordered = [
        prompt
        for fmt in sorted(bank)
        for prompt in sorted(bank[fmt].prompts, key=lambda p: p.id)
    ]
    violations = []
    for label, extract in (("person", person_names), ("organization", org_names)):
        seen: dict[str, str] = {}
        collisions: dict[str, list[str]] = {}
        for prompt in ordered:
            for name in sorted(extract(prompt.scenario)):
                if name in seen and seen[name] != prompt.id:
                    collisions.setdefault(name, [seen[name]]).append(prompt.id)
                else:
                    seen.setdefault(name, prompt.id)
        for name in sorted(collisions):
            where = collisions[name]
            violations.append(
                f"{label} name {name!r} is reused across scenarios "
                f"({', '.join(where)}) — each scenario needs its own cast"
            )
    return violations
