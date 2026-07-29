"""Every regex tell in the shipped registry must match its examples and miss its counter-examples."""

from __future__ import annotations

from pathlib import Path

import pytest

from telltale.registry import Registry, Tell

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"
REGISTRY = Registry(REGISTRY_PATH)

REGEX_TELLS: list[Tell] = [
    t for t in REGISTRY.active_tells(include_candidates=True) if t.method == "regex"
]
REGEX_IDS = [t.id for t in REGEX_TELLS]

COUNTER_CASES = [
    (t, counter) for t in REGEX_TELLS for counter in t.counter_examples
]
COUNTER_IDS = [f"{t.id}[{i}]" for t in REGEX_TELLS for i, _ in enumerate(t.counter_examples)]


def test_registry_has_regex_tells() -> None:
    assert len(REGEX_TELLS) > 50


@pytest.mark.parametrize("tell", REGEX_TELLS, ids=REGEX_IDS)
def test_pattern_compiles(tell: Tell) -> None:
    assert tell.compiled() is not None


@pytest.mark.parametrize("tell", REGEX_TELLS, ids=REGEX_IDS)
def test_at_least_one_example_matches(tell: Tell) -> None:
    rx = tell.compiled()
    assert tell.examples, f"{tell.id} has no examples"
    matched = [ex for ex in tell.examples if rx.search(ex)]
    assert matched, f"{tell.id}: no example matches {tell.pattern!r}"


@pytest.mark.parametrize(("tell", "counter"), COUNTER_CASES, ids=COUNTER_IDS)
def test_counter_example_does_not_match(tell: Tell, counter: str) -> None:
    rx = tell.compiled()
    hit = rx.search(counter)
    assert hit is None, f"{tell.id}: pattern {tell.pattern!r} matched {hit.group(0)!r} in {counter!r}"
