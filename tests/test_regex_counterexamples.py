"""Every regex tell in the shipped registry must match its examples and miss its counter-examples.

Checked through `search_guarded`, not through the bare compiled pattern, because
for a tell with `proper_noun_guard` the pattern is only half the detector. A
counter-example like "held at Foster Elementary School" is *meant* to match the
pattern; the guard is what rejects it, and testing the pattern alone would either
fail spuriously or, worse, pass while the guard was broken.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from telltale.detectors import search_guarded
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
    assert tell.examples, f"{tell.id} has no examples"
    matched = [ex for ex in tell.examples if search_guarded(tell, ex)]
    assert matched, f"{tell.id}: no example survives {tell.pattern!r}"


@pytest.mark.parametrize(("tell", "counter"), COUNTER_CASES, ids=COUNTER_IDS)
def test_counter_example_does_not_match(tell: Tell, counter: str) -> None:
    hit = search_guarded(tell, counter)
    assert hit is None, f"{tell.id}: pattern {tell.pattern!r} matched {hit.group(0)!r} in {counter!r}"


GUARDED_TELLS = [t for t in REGEX_TELLS if t.proper_noun_guard]
GUARDED_IDS = [t.id for t in GUARDED_TELLS]


def test_the_registry_ships_proper_noun_guards() -> None:
    assert len(GUARDED_TELLS) >= 12


@pytest.mark.parametrize("tell", GUARDED_TELLS, ids=GUARDED_IDS)
def test_a_guarded_tell_carries_a_name_collision_counter_example(tell: Tell) -> None:
    """The guard is a claim about names; each guarded tell must evidence one.

    A counter-example that the bare pattern already rejects proves nothing about
    the guard, so at least one has to be a case the pattern matches and the guard
    throws out.
    """
    rx = tell.compiled()
    exercises_guard = [
        c for c in tell.counter_examples if rx.search(c) and not search_guarded(tell, c)
    ]
    assert exercises_guard, f"{tell.id}: no counter-example exercises the guard"
