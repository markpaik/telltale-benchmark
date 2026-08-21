"""Load, validate, and edit the tell registry (registry/tells.yaml)."""

from __future__ import annotations

import datetime
import hashlib
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterator

import yaml

# --- enums and mappings ------------------------------------------------------

CATEGORIES = {"lexical", "punctuation", "syntactic", "structural", "statistical"}
# A tell is either general or scoped to one model. Discovery (M7) records the
# latter as "model:<model-id>", e.g. "model:claude-opus-5".
SCOPES = {"general"}
MODEL_SCOPE_PATTERN = re.compile(r"^model:[a-z0-9][a-z0-9.-]*$")
# "atlas" is the profile layer (M9e): a device inventory measured for frequency
# only. Atlas entries are validated and detected like any other entry, but they
# are not tells — they carry no ramp, they score NaN, and every aggregate that
# rolls tells up filters on status == "active", so they cannot reach the
# AI-Tell Index or a category rollup until one is individually promoted.
STATUSES = {"active", "candidate", "deprecated", "atlas"}
ATLAS_STATUS = "atlas"
METHODS = {"regex", "statistic", "judge"}
UNITS = {"count", "binary", "value"}
DIRECTIONS = {"high_is_telling", "low_is_telling"}
JUDGE_VIEWS = {"chunk", "skeleton"}

PREFIX_CATEGORY = {
    "lex": "lexical",
    "phr": "lexical",
    "crt": "lexical",
    "cl": "lexical",
    "pnc": "punctuation",
    "rht": "syntactic",
    "str": "structural",
    "sta": "statistical",
}

# "atlas" is the only prefix with no PREFIX_CATEGORY entry: the atlas spans
# every category (alliteration is lexical, tricolon is structural), so the id
# names the device and the `category` field carries the classification.
ID_PATTERN = re.compile(r"^(lex|phr|crt|cl|pnc|rht|str|sta|atlas)\.[a-z0-9-]+$")

FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
    "VERBOSE": re.VERBOSE,
    "UNICODE": re.UNICODE,
    "ASCII": re.ASCII,
}


def is_valid_scope(scope: str) -> bool:
    """True for "general" and for model-specific scopes like "model:claude-opus-5"."""
    return scope in SCOPES or bool(MODEL_SCOPE_PATTERN.match(scope))


def guarded_search(tell: "Tell", text: str) -> "re.Match[str] | None":
    """First match of a tell's pattern in `text`, with its guards applied.

    Validation has to see exactly what the detector will see. A counter-example
    for a guarded tell ("held at Foster Elementary School") *does* match the bare
    pattern — the guard is what rejects it — so checking against `tell.compiled()`
    alone would report an error the run will never make.

    Imported lazily for the same reason `known_stats` is: the registry must be
    able to load and validate without dragging in the detection engine, and
    regex_detector imports this module.
    """
    if not tell.proper_noun_guard:
        return tell.compiled().search(text)
    from telltale.detectors.regex_detector import search_guarded

    return search_guarded(tell, text)


def known_stats() -> set[str]:
    """Names in the textstats registry, imported lazily.

    Kept out of module scope on purpose: the registry has to load and validate
    its own schema without dragging in the measurement engine. If textstats
    cannot be imported at all, statistic tells simply go unchecked rather than
    taking the whole validation down.
    """
    try:
        from telltale.textstats import STATS
    except ImportError:  # pragma: no cover - only if the package is broken
        return set()
    return set(STATS)


class _Dumper(yaml.SafeDumper):
    """SafeDumper that writes multi-line strings as block scalars and no anchors."""

    def ignore_aliases(self, data: Any) -> bool:
        return True


def _represent_str(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _represent_str)


# --- the tell ----------------------------------------------------------------


@dataclass(frozen=True)
class Tell:
    """One registry entry, with the `detection` block flattened onto the record."""

    id: str
    name: str
    category: str
    scope: str = "general"
    formats: tuple[str, ...] | None = None
    # detection
    method: str = "regex"
    unit: str = "count"
    pattern: str | None = None
    flags: tuple[str, ...] = ()
    # Drop mid-sentence capitalized matches as proper nouns. Opt-in, and only
    # meaningful for regex tells; see detectors/regex_detector.py for the rule.
    proper_noun_guard: bool = False
    stat: str | None = None
    direction: str | None = None
    ramp: tuple[float, ...] | None = None
    rubric: str | None = None
    rubric_version: int | None = None
    judge_view: str | None = None
    # everything else
    examples: tuple[str, ...] = ()
    counter_examples: tuple[str, ...] = ()
    provenance: dict[str, Any] | None = None
    status: str = "active"
    weight: float = 1.0
    notes: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Tell":
        """Build a Tell leniently, so a malformed entry can still reach validate()."""
        det = data.get("detection") or {}
        if not isinstance(det, dict):
            det = {}
        formats = data.get("formats")
        ramp = det.get("ramp")
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            category=str(data.get("category", "")),
            scope=str(data.get("scope", "")),
            formats=tuple(formats) if isinstance(formats, list) else None,
            method=str(det.get("method", "")),
            unit=str(det.get("unit", "")),
            pattern=det.get("pattern"),
            flags=tuple(det.get("flags") or ()),
            proper_noun_guard=bool(det.get("proper_noun_guard", False)),
            stat=det.get("stat"),
            direction=det.get("direction"),
            ramp=tuple(ramp) if isinstance(ramp, list) else None,
            rubric=det.get("rubric"),
            rubric_version=det.get("rubric_version"),
            judge_view=det.get("judge_view"),
            examples=tuple(data.get("examples") or ()),
            counter_examples=tuple(data.get("counter_examples") or ()),
            provenance=data.get("provenance"),
            status=str(data.get("status", "")),
            weight=float(data.get("weight", 1.0)),
            notes=data.get("notes"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize back to the nested on-disk shape, keys in registry order."""
        detection: dict[str, Any] = {"method": self.method, "unit": self.unit}
        if self.method == "regex":
            detection["pattern"] = self.pattern
            detection["flags"] = list(self.flags)
            if self.proper_noun_guard:
                detection["proper_noun_guard"] = True
        elif self.method == "statistic":
            detection["stat"] = self.stat
            if self.direction is not None:
                detection["direction"] = self.direction
            if self.ramp is not None:
                detection["ramp"] = [float(x) for x in self.ramp]
        elif self.method == "judge":
            detection["rubric"] = self.rubric
            detection["rubric_version"] = self.rubric_version
            detection["judge_view"] = self.judge_view
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "scope": self.scope,
            "formats": list(self.formats) if self.formats is not None else None,
            "detection": detection,
            "examples": list(self.examples),
            "counter_examples": list(self.counter_examples),
            "provenance": self.provenance,
            "status": self.status,
            "weight": self.weight,
            "notes": self.notes,
        }

    def compiled_flags(self) -> int:
        flags = 0
        for name in self.flags:
            flags |= FLAG_MAP.get(str(name), 0)
        return flags

    def compiled(self) -> re.Pattern[str]:
        """Compile this tell's regex. Raises re.error / TypeError if it is not usable."""
        return re.compile(self.pattern or "", self.compiled_flags())


# --- the registry ------------------------------------------------------------


class Registry:
    """The on-disk tell registry."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        raw = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        self._raw: dict[str, Any] = raw if isinstance(raw, dict) else {}
        self._tells: list[Tell] = [
            Tell.from_dict(d) for d in (self._raw.get("tells") or []) if isinstance(d, dict)
        ]

    # -- reading --

    @property
    def version(self) -> int:
        return int(self._raw.get("registry_version", 0))

    @property
    def schema_version(self) -> int:
        return int(self._raw.get("schema_version", 0))

    @property
    def updated(self) -> Any:
        return self._raw.get("updated")

    @property
    def tells(self) -> list[Tell]:
        return list(self._tells)

    @property
    def content_hash(self) -> str:
        """sha256 of the canonicalized YAML: keys sorted, whitespace stripped."""
        dumped = yaml.dump(
            self._raw,
            Dumper=_Dumper,
            sort_keys=True,
            default_flow_style=False,
            allow_unicode=True,
            width=100000,
        )
        canonical = "\n".join(line.strip() for line in dumped.splitlines()).strip()
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def active_tells(
        self, include_candidates: bool = False, include_atlas: bool = False
    ) -> list[Tell]:
        """The entries a run measures.

        `include_atlas` adds the profile layer. It is off by default and
        separate from `include_candidates` on purpose: a candidate is a tell
        that has not been promoted yet, an atlas entry is not a tell at all, so
        a run that wants one should not silently get the other.
        """
        wanted = {"active", "candidate"} if include_candidates else {"active"}
        if include_atlas:
            wanted = wanted | {ATLAS_STATUS}
        return [t for t in self._tells if t.status in wanted]

    def atlas_tells(self) -> list[Tell]:
        """The profile layer alone, in registry order."""
        return [t for t in self._tells if t.status == ATLAS_STATUS]

    def get(self, tell_id: str) -> Tell:
        for tell in self._tells:
            if tell.id == tell_id:
                return tell
        raise KeyError(tell_id)

    def __len__(self) -> int:
        return len(self._tells)

    def __iter__(self) -> Iterator[Tell]:
        return iter(self._tells)

    # -- validation --

    def validate(self) -> list[str]:
        """Return one error string per violation. An empty list means the file is valid."""
        errors: list[str] = []
        seen: set[str] = set()
        stats = known_stats()

        for tell in self._tells:
            tid = tell.id or "<missing id>"

            if tell.id in seen:
                errors.append(f"{tid}: duplicate id")
            seen.add(tell.id)

            prefix = tell.id.split(".", 1)[0] if "." in tell.id else ""
            if not ID_PATTERN.match(tell.id):
                errors.append(f"{tid}: id does not match ^(lex|phr|crt|cl|pnc|rht|str|sta)\\.[a-z0-9-]+$")

            if tell.category not in CATEGORIES:
                errors.append(f"{tid}: invalid category {tell.category!r}")
            elif prefix in PREFIX_CATEGORY and tell.category != PREFIX_CATEGORY[prefix]:
                errors.append(
                    f"{tid}: category {tell.category!r} does not match prefix {prefix!r} "
                    f"(expected {PREFIX_CATEGORY[prefix]!r})"
                )

            if not is_valid_scope(tell.scope):
                errors.append(
                    f"{tid}: invalid scope {tell.scope!r} "
                    f"(expected 'general' or 'model:<model-id>')"
                )
            if tell.status not in STATUSES:
                errors.append(f"{tid}: invalid status {tell.status!r}")
            if tell.method not in METHODS:
                errors.append(f"{tid}: invalid method {tell.method!r}")
            if tell.unit not in UNITS:
                errors.append(f"{tid}: invalid unit {tell.unit!r}")

            errors.extend(self._validate_detection(tell, tid, stats))

            if tell.unit == "value" and tell.status == ATLAS_STATUS:
                # An atlas entry reports a number, it does not judge one. A ramp
                # is the encoding of "more of this is worse", which is exactly
                # the claim the profile layer does not make; requiring its
                # absence also means promoting an atlas statistic to a tell
                # fails validation until someone supplies a real ramp.
                if tell.direction is not None:
                    errors.append(f"{tid}: atlas entries carry no direction")
                if tell.ramp is not None:
                    errors.append(f"{tid}: atlas entries carry no ramp")
            elif tell.unit == "value":
                if tell.direction is None:
                    errors.append(f"{tid}: value unit requires direction")
                elif tell.direction not in DIRECTIONS:
                    errors.append(f"{tid}: invalid direction {tell.direction!r}")
                if tell.ramp is None:
                    errors.append(f"{tid}: value unit requires ramp")
                elif len(tell.ramp) != 2 or not all(
                    isinstance(x, (int, float)) and not isinstance(x, bool) for x in tell.ramp
                ):
                    errors.append(f"{tid}: ramp must be exactly two numbers, got {list(tell.ramp)!r}")

        return errors

    def _validate_detection(self, tell: Tell, tid: str, stats: set[str]) -> list[str]:
        errors: list[str] = []

        if tell.proper_noun_guard and tell.method != "regex":
            errors.append(
                f"{tid}: proper_noun_guard is only meaningful for regex tells "
                f"(method is {tell.method!r})"
            )

        if tell.method == "regex":
            if not isinstance(tell.pattern, str) or not tell.pattern:
                errors.append(f"{tid}: regex tell has no pattern")
                return errors
            for name in tell.flags:
                if str(name) not in FLAG_MAP:
                    errors.append(f"{tid}: unknown regex flag {name!r}")
            try:
                tell.compiled()
            except re.error as exc:
                errors.append(f"{tid}: pattern does not compile: {exc}")
                return errors
            if not tell.examples:
                errors.append(f"{tid}: regex tell has no examples")
            elif not any(guarded_search(tell, ex) for ex in tell.examples):
                errors.append(
                    f"{tid}: no example matches the pattern"
                    + (" once the proper-noun guard is applied" if tell.proper_noun_guard else "")
                )
            for counter in tell.counter_examples:
                if guarded_search(tell, counter):
                    errors.append(f"{tid}: counter-example matches the pattern: {counter!r}")

        elif tell.method == "statistic":
            if not isinstance(tell.stat, str) or not tell.stat.strip():
                errors.append(f"{tid}: statistic tell requires a stat name")
            elif stats and tell.stat not in stats:
                errors.append(f"{tid}: unknown stat function {tell.stat!r}")

        elif tell.method == "judge":
            if not isinstance(tell.rubric, str) or not tell.rubric.strip():
                errors.append(f"{tid}: judge tell requires a rubric")
            if not isinstance(tell.rubric_version, int):
                errors.append(f"{tid}: judge tell requires rubric_version")
            if tell.judge_view not in JUDGE_VIEWS:
                errors.append(f"{tid}: judge tell requires judge_view (chunk|skeleton)")

        return errors

    # -- writing --

    def append(self, tells: list[Tell]) -> None:
        """Append new tells, bump registry_version and updated, write the file back."""
        if not tells:
            return
        known = {t.id for t in self._tells}
        for tell in tells:
            if tell.id in known:
                raise ValueError(f"tell already in registry: {tell.id}")
            known.add(tell.id)

        self._raw.setdefault("tells", []).extend(t.to_dict() for t in tells)
        self._tells.extend(tells)
        self._bump()
        self._write()

    def set_status(self, tell_id: str, status: str) -> None:
        """Promote or deprecate a tell, bump registry_version and updated, write back."""
        if status not in STATUSES:
            raise ValueError(f"invalid status: {status} (expected one of {sorted(STATUSES)})")

        for entry in self._raw.get("tells") or []:
            if isinstance(entry, dict) and entry.get("id") == tell_id:
                entry["status"] = status
                break
        else:
            raise KeyError(tell_id)

        self._tells = [
            replace(t, status=status) if t.id == tell_id else t for t in self._tells
        ]
        self._bump()
        self._write()

    def _bump(self) -> None:
        self._raw["registry_version"] = self.version + 1
        self._raw["updated"] = datetime.date.today()

    def _write(self) -> None:
        text = yaml.dump(
            self._raw,
            Dumper=_Dumper,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=100000,
        )
        self.path.write_text(text, encoding="utf-8")
