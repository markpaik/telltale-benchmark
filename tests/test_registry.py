"""Registry loading, validation, and edit round-trips."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from telltale.registry import Registry, Tell, is_valid_scope, known_stats

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"


@pytest.fixture
def registry() -> Registry:
    return Registry(REGISTRY_PATH)


def test_real_registry_is_valid(registry: Registry) -> None:
    assert registry.validate() == []


def test_registry_yaml_has_no_duplicate_keys() -> None:
    """Hand-editing the registry must not silently shadow a key (e.g. two `notes:`)."""

    class StrictLoader(yaml.SafeLoader):
        pass

    def no_duplicates(loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
        seen: list[object] = []
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            assert key not in seen, f"duplicate key {key!r} at line {key_node.start_mark.line + 1}"
            seen.append(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates
    )
    yaml.load(REGISTRY_PATH.read_text(encoding="utf-8"), Loader=StrictLoader)


def test_header_fields(registry: Registry) -> None:
    assert registry.version >= 1
    assert registry.schema_version == 1
    assert len(registry) > 100


def test_content_hash_is_stable_across_loads() -> None:
    first = Registry(REGISTRY_PATH).content_hash
    second = Registry(REGISTRY_PATH).content_hash
    assert first == second
    assert len(first) == 64
    assert all(c in "0123456789abcdef" for c in first)


def test_get_returns_the_tell(registry: Registry) -> None:
    tell = registry.get("lex.delve")
    assert tell.id == "lex.delve"
    assert tell.category == "lexical"
    assert tell.method == "regex"
    assert tell.compiled().search("We should delve into the numbers.")


def test_get_raises_for_unknown_id(registry: Registry) -> None:
    with pytest.raises(KeyError):
        registry.get("lex.does-not-exist")


def test_active_tells(registry: Registry) -> None:
    active = registry.active_tells()
    # Not `len(registry)`: once a discovery run has appended candidates the
    # registry holds more tells than it scores, which is the whole point of the
    # candidate status. The invariant is that `active_tells` returns exactly the
    # active-status ones, not that every tell is active.
    assert len(active) == sum(1 for t in registry if t.status == "active")
    assert all(t.status == "active" for t in active)
    assert len(registry.active_tells(include_candidates=True)) >= len(active)


def test_crt_tells_restrict_formats(registry: Registry) -> None:
    tell = registry.get("crt.feel-free")
    assert tell.formats == ("email", "memo", "meeting-minutes")
    assert registry.get("lex.delve").formats is None


def test_judge_tells_have_rubrics(registry: Registry) -> None:
    judges = [t for t in registry.active_tells() if t.method == "judge"]
    assert len(judges) == 7
    for tell in judges:
        # Not pinned to 1: a rubric that turns out to be wrong is supposed to be
        # rewritten and its version bumped, which is what invalidates the judge
        # cache and the tell's calibration report. Pinning the number here would
        # make the correct move fail the build.
        assert isinstance(tell.rubric_version, int) and tell.rubric_version >= 1
        assert tell.judge_view in {"chunk", "skeleton"}
        assert "EXCLUSION" in tell.rubric
        assert "Evidence to extract" in tell.rubric


def test_simply_put_requires_the_idiomatic_comma(registry: Registry) -> None:
    rx = registry.get("phr.simply-put").compiled()
    assert rx.search("Simply put, the program works.")
    assert rx.search("Put simply, the rule changed.")
    assert rx.search("In other words, the count moved.")
    assert not rx.search("The event was simply put together at the last minute.")
    assert not rx.search("The kit was simply put back on the shelf.")


def test_landscape_metaphor_documents_its_limitation(registry: Registry) -> None:
    notes = registry.get("lex.landscape-metaphor").notes or ""
    assert "Known limitation" in notes
    assert "accepted for v1" in notes


def test_append_and_set_status_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "tells.yaml"
    shutil.copy(REGISTRY_PATH, path)

    registry = Registry(path)
    start_version = registry.version
    start_count = len(registry)
    start_active = len(registry.active_tells())

    new = Tell(
        id="lex.testword",
        name="testword",
        category="lexical",
        scope="general",
        method="regex",
        unit="count",
        pattern=r"\btestword\b",
        flags=("IGNORECASE",),
        examples=("The testword appears here.",),
        counter_examples=("Nothing to see.",),
        provenance={"source": "seed", "run_id": None, "evidence": "literature"},
        status="candidate",
        weight=1.0,
    )
    registry.append([new])

    reloaded = Registry(path)
    assert reloaded.version == start_version + 1
    assert len(reloaded) == start_count + 1
    assert reloaded.validate() == []

    appended = reloaded.get("lex.testword")
    assert appended.status == "candidate"
    assert appended.pattern == r"\btestword\b"
    assert appended.flags == ("IGNORECASE",)
    assert appended not in reloaded.active_tells()
    assert appended in reloaded.active_tells(include_candidates=True)

    reloaded.set_status("lex.testword", "active")
    promoted = Registry(path)
    assert promoted.version == start_version + 2
    assert promoted.get("lex.testword").status == "active"

    promoted.set_status("lex.testword", "deprecated")
    deprecated = Registry(path)
    assert deprecated.version == start_version + 3
    assert deprecated.get("lex.testword").status == "deprecated"
    assert len(deprecated.active_tells()) == start_active


def test_append_rejects_duplicate_id(tmp_path: Path) -> None:
    path = tmp_path / "tells.yaml"
    shutil.copy(REGISTRY_PATH, path)
    registry = Registry(path)
    clone = registry.get("lex.delve")
    with pytest.raises(ValueError):
        registry.append([clone])


def test_set_status_rejects_unknown_tell_and_status(tmp_path: Path) -> None:
    path = tmp_path / "tells.yaml"
    shutil.copy(REGISTRY_PATH, path)
    registry = Registry(path)
    with pytest.raises(KeyError):
        registry.set_status("lex.nope", "deprecated")
    with pytest.raises(ValueError):
        registry.set_status("lex.delve", "retired")


# --- scope enum --------------------------------------------------------------


def _scoped_registry(tmp_path: Path, scope: str) -> Registry:
    """A minimal one-tell registry carrying the given scope."""
    doc = {
        "registry_version": 1,
        "schema_version": 1,
        "updated": "2026-07-28",
        "tells": [
            {
                "id": "lex.scopecheck",
                "name": "scope check",
                "category": "lexical",
                "scope": scope,
                "formats": None,
                "detection": {
                    "method": "regex",
                    "unit": "count",
                    "pattern": r"\bscopecheck\b",
                    "flags": ["IGNORECASE"],
                },
                "examples": ["The scopecheck fires here."],
                "counter_examples": [],
                "provenance": {"source": "seed", "run_id": None, "evidence": "literature"},
                "status": "active",
                "weight": 1.0,
                "notes": None,
            }
        ],
    }
    path = tmp_path / f"scope.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return Registry(path)


@pytest.mark.parametrize(
    "scope",
    ["general", "model:claude-opus-5", "model:gpt-4.1", "model:llama-3.1-70b"],
)
def test_validate_accepts_scope(tmp_path: Path, scope: str) -> None:
    assert is_valid_scope(scope)
    assert _scoped_registry(tmp_path, scope).validate() == []


@pytest.mark.parametrize(
    "scope",
    ["modelclaude", "team:foo", "model:", "model:-leading-dash", "MODEL:Claude", "", "model:CLAUDE"],
)
def test_validate_rejects_scope(tmp_path: Path, scope: str) -> None:
    assert not is_valid_scope(scope)
    errors = _scoped_registry(tmp_path, scope).validate()
    assert any("invalid scope" in e for e in errors), errors


def test_seed_tells_are_all_general(registry: Registry) -> None:
    # Seed tells only. Discovery is allowed to propose a model-scoped tell — that
    # is what gate 3 decides — so scoping this assertion to every tell in the
    # file would turn "the seed set makes no per-model claims" into "no tell ever
    # may", which is a different and wrong statement.
    seed = [t for t in registry if (t.provenance or {}).get("source") != "discovery"]
    assert {t.scope for t in seed} == {"general"}


# --- proper_noun_guard -------------------------------------------------------


def _guard_registry(tmp_path: Path, detection: dict, **overrides) -> Registry:
    """A one-tell registry whose detection block is given wholesale."""
    tell = {
        "id": "lex.guardcheck",
        "name": "guard check",
        "category": "lexical",
        "scope": "general",
        "formats": None,
        "detection": detection,
        "examples": ["The widget fires here."],
        "counter_examples": [],
        "provenance": {"source": "seed", "run_id": None, "evidence": "literature"},
        "status": "active",
        "weight": 1.0,
        "notes": None,
    }
    tell.update(overrides)
    doc = {
        "registry_version": 1,
        "schema_version": 1,
        "updated": "2026-07-28",
        "tells": [tell],
    }
    path = tmp_path / "guard.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return Registry(path)


def test_proper_noun_guard_defaults_to_off(registry: Registry) -> None:
    unguarded = [t for t in registry if not t.proper_noun_guard]
    assert len(unguarded) == len(list(registry)) - 12


def test_proper_noun_guard_round_trips(tmp_path: Path) -> None:
    detection = {
        "method": "regex",
        "unit": "count",
        "pattern": r"\bwidget\b",
        "flags": ["IGNORECASE"],
        "proper_noun_guard": True,
    }
    tell = _guard_registry(tmp_path, detection).get("lex.guardcheck")
    assert tell.proper_noun_guard is True
    assert tell.to_dict()["detection"] == detection


def test_an_unguarded_tell_does_not_serialize_the_key(tmp_path: Path) -> None:
    """Omitted rather than written false, so 109 tells keep a quiet diff."""
    detection = {
        "method": "regex",
        "unit": "count",
        "pattern": r"\bwidget\b",
        "flags": ["IGNORECASE"],
    }
    tell = _guard_registry(tmp_path, detection).get("lex.guardcheck")
    assert "proper_noun_guard" not in tell.to_dict()["detection"]


def test_the_guard_is_rejected_on_a_statistic_tell(tmp_path: Path) -> None:
    registry = _guard_registry(
        tmp_path,
        {
            "method": "statistic",
            "unit": "value",
            "stat": "mattr_500",
            "direction": "high_is_telling",
            "ramp": [0.78, 0.86],
            "proper_noun_guard": True,
        },
        id="sta.guardcheck",
        category="statistical",
    )
    errors = registry.validate()
    assert any("proper_noun_guard is only meaningful for regex tells" in e for e in errors), errors


def test_validation_applies_the_guard_to_counter_examples(tmp_path: Path) -> None:
    """A guarded counter-example matches the pattern; only the guard rejects it.

    Validating against the bare pattern would report an error for a registry the
    detector handles perfectly well, so the two have to agree.
    """
    detection = {
        "method": "regex",
        "unit": "count",
        "pattern": r"\bwidget\b",
        "flags": ["IGNORECASE"],
        "proper_noun_guard": True,
    }
    counter = "We met the Widget team on Tuesday."
    guarded = _guard_registry(tmp_path, detection, counter_examples=[counter])
    assert guarded.validate() == []

    unguarded = _guard_registry(
        tmp_path,
        {k: v for k, v in detection.items() if k != "proper_noun_guard"},
        counter_examples=[counter],
    )
    assert any("counter-example matches" in e for e in unguarded.validate())


# --- deliberately broken registry -------------------------------------------

BROKEN = {
    "registry_version": 1,
    "schema_version": 1,
    "updated": "2026-07-28",
    "tells": [
        {
            "id": "lex.badregex",
            "name": "bad regex",
            "category": "lexical",
            "scope": "general",
            "formats": None,
            "detection": {
                "method": "regex",
                "unit": "count",
                "pattern": r"\b(unclosed",
                "flags": ["IGNORECASE"],
            },
            "examples": ["unclosed group here"],
            "counter_examples": [],
            "status": "active",
            "weight": 1.0,
        },
        {
            "id": "str.norubric",
            "name": "judge without a rubric",
            "category": "structural",
            "scope": "general",
            "formats": None,
            "detection": {"method": "judge", "unit": "binary"},
            "examples": ["Something."],
            "counter_examples": [],
            "status": "active",
            "weight": 1.0,
        },
        {
            "id": "lex.badregex",
            "name": "duplicate id, wrong category, bad enums",
            "category": "structural",
            "scope": "universal",
            "formats": None,
            "detection": {"method": "vibes", "unit": "quantity"},
            "examples": [],
            "counter_examples": [],
            "status": "retired",
            "weight": 1.0,
        },
        {
            "id": "lex.nomatch",
            "name": "examples do not match",
            "category": "lexical",
            "scope": "general",
            "formats": None,
            "detection": {
                "method": "regex",
                "unit": "count",
                "pattern": r"\bsynergy\b",
                "flags": ["IGNORECASE"],
            },
            "examples": ["This example has nothing to do with the pattern."],
            "counter_examples": ["The synergy between the teams was real."],
            "status": "active",
            "weight": 1.0,
        },
        {
            "id": "sta.noramp",
            "name": "value unit without direction or ramp",
            "category": "statistical",
            "scope": "general",
            "formats": None,
            "detection": {"method": "statistic", "unit": "value", "stat": "commas_per_sentence"},
            "examples": ["Illustration."],
            "counter_examples": [],
            "status": "active",
            "weight": 1.0,
        },
        {
            "id": "sta.badramp",
            "name": "ramp with three values and no stat",
            "category": "statistical",
            "scope": "general",
            "formats": None,
            "detection": {
                "method": "statistic",
                "unit": "value",
                "stat": "",
                "direction": "sideways",
                "ramp": [1.0, 2.0, 3.0],
            },
            "examples": ["Illustration."],
            "counter_examples": [],
            "status": "active",
            "weight": 1.0,
        },
        {
            "id": "BAD.Id_Format",
            "name": "malformed id",
            "category": "lexical",
            "scope": "general",
            "formats": None,
            "detection": {
                "method": "regex",
                "unit": "count",
                "pattern": r"\bwhatever\b",
                "flags": [],
            },
            "examples": ["whatever"],
            "counter_examples": [],
            "status": "active",
            "weight": 1.0,
        },
    ],
}


@pytest.fixture
def broken_errors(tmp_path: Path) -> list[str]:
    path = tmp_path / "broken.yaml"
    path.write_text(yaml.safe_dump(BROKEN, sort_keys=False), encoding="utf-8")
    return Registry(path).validate()


@pytest.mark.parametrize(
    "needle",
    [
        "lex.badregex: pattern does not compile",
        "lex.badregex: duplicate id",
        "str.norubric: judge tell requires a rubric",
        "str.norubric: judge tell requires rubric_version",
        "str.norubric: judge tell requires judge_view",
        "lex.badregex: invalid scope 'universal'",
        "lex.badregex: invalid status 'retired'",
        "lex.badregex: invalid method 'vibes'",
        "lex.badregex: invalid unit 'quantity'",
        "lex.badregex: category 'structural' does not match prefix 'lex'",
        "lex.nomatch: no example matches the pattern",
        "lex.nomatch: counter-example matches the pattern",
        "sta.noramp: value unit requires direction",
        "sta.noramp: value unit requires ramp",
        "sta.badramp: invalid direction 'sideways'",
        "sta.badramp: ramp must be exactly two numbers",
        "sta.badramp: statistic tell requires a stat name",
        "BAD.Id_Format: id does not match",
    ],
)
def test_broken_registry_reports_error(broken_errors: list[str], needle: str) -> None:
    assert any(needle in error for error in broken_errors), broken_errors


def test_valid_registry_reports_no_errors_for_broken_only(broken_errors: list[str]) -> None:
    assert broken_errors  # sanity: the broken fixture really is broken


# --- statistic tells resolve to real stat functions --------------------------


def _stat_registry(tmp_path: Path, stat_name: str) -> Registry:
    """A minimal one-tell registry whose statistic tell names the given stat."""
    doc = {
        "registry_version": 1,
        "schema_version": 1,
        "updated": "2026-07-28",
        "tells": [
            {
                "id": "sta.statcheck",
                "name": "stat check",
                "category": "statistical",
                "scope": "general",
                "formats": None,
                "detection": {
                    "method": "statistic",
                    "unit": "value",
                    "stat": stat_name,
                    "direction": "high_is_telling",
                    "ramp": [1.0, 2.0],
                },
                "examples": ["Illustration."],
                "counter_examples": [],
                "provenance": {"source": "seed", "run_id": None, "evidence": "literature"},
                "status": "active",
                "weight": 1.0,
                "notes": None,
            }
        ],
    }
    path = tmp_path / "stat.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return Registry(path)


def test_validate_rejects_an_unknown_stat_function(tmp_path: Path) -> None:
    errors = _stat_registry(tmp_path, "no_such_stat").validate()
    assert "sta.statcheck: unknown stat function 'no_such_stat'" in errors


def test_validate_accepts_a_registered_stat_function(tmp_path: Path) -> None:
    assert _stat_registry(tmp_path, "mattr_500").validate() == []


def test_known_stats_matches_the_textstats_registry() -> None:
    from telltale.textstats import STATS

    assert known_stats() == set(STATS)
    assert len(known_stats()) == 18


def test_every_statistic_tell_in_the_real_registry_resolves(registry: Registry) -> None:
    named = {t.stat for t in registry if t.method == "statistic"}
    assert named
    assert named <= known_stats()
