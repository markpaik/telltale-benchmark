"""Choosing which documents the judge reads, when it cannot read all of them.

Tier-1 detection is free — regexes over 224 documents finish in nine seconds —
so the full corpus is always scored deterministically. Tier-2 is not free: one
judge tell over one document is a dozen-odd subprocess calls, and the whole
matrix runs to five figures. A shakedown whose purpose is to find defects in
the benchmark does not need every cell; it needs a sample nobody can accuse of
being convenient.

Hence stratification rather than a random draw. A plain random 60 of 224 would,
by luck, over-weight some formats and starve others — and format is the single
largest source of variance in how tell-prone a document is (an SOP is all
bullets and headings, a condolence email is neither). Balancing across model and
format first means the sample cannot flatter or punish a model through the mix
of formats it happened to draw.

Selection is deterministic given (seed, size, corpus). Same inputs, same sample,
so a judge run over a sample is as reproducible as one over everything — and the
chosen ids are written into the run directory rather than left to be recomputed,
because a sample you have to re-derive to check is not evidence.
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Sequence

from telltale.corpus import EXPLORATORY_FORMATS, Doc

DEFAULT_SIZE = 60
DEFAULT_SEED = 7


@dataclass(frozen=True)
class SampleStratum:
    """One (model, format) cell of the plan, and what it contributed."""

    model: str
    fmt: str
    available: int
    taken: int
    doc_ids: tuple[str, ...]


@dataclass
class JudgeSample:
    """The documents Tier-2 will read, and the reasoning that picked them."""

    size: int
    seed: int
    doc_ids: tuple[str, ...] = ()
    strata: list[SampleStratum] = field(default_factory=list)
    per_model: dict[str, int] = field(default_factory=dict)
    per_format: dict[str, int] = field(default_factory=dict)
    note: str = ""

    def __contains__(self, doc_id: object) -> bool:
        return doc_id in set(self.doc_ids)

    def as_dict(self) -> dict[str, Any]:
        return {
            "size": self.size,
            "seed": self.seed,
            "n_selected": len(self.doc_ids),
            "doc_ids": list(self.doc_ids),
            "per_model": dict(sorted(self.per_model.items())),
            "per_format": dict(sorted(self.per_format.items())),
            "strata": [
                {
                    "model": s.model,
                    "format": s.fmt,
                    "available": s.available,
                    "taken": s.taken,
                    "doc_ids": list(s.doc_ids),
                }
                for s in self.strata
            ],
            "note": self.note,
        }


def _rng(*parts: Any) -> random.Random:
    """A generator seeded by the stratum it draws for.

    Per-stratum seeding rather than one shared stream: adding a format to the
    corpus then leaves every other stratum's draw untouched, so two samples over
    overlapping corpora stay comparable where they overlap.
    """
    return random.Random("|".join(str(p) for p in parts))


def stratified_sample(
    docs: Sequence[Doc], size: int = DEFAULT_SIZE, seed: int = DEFAULT_SEED
) -> JudgeSample:
    """Pick `size` documents, balanced across model and format.

    Each model gets an equal share. Within a model, every format contributes the
    same base count; whatever is left over goes to the formats with the deepest
    pools, since those are the only ones with documents to spare. Ties break on
    the format name so the result never depends on dict ordering.
    """
    # The exploratory annex never enters the judge sample (R20): those documents
    # are not benchmark cells, and spending a stratum on them would take Tier-2
    # reads away from the formats the index is computed on. Dropping them here
    # rather than at the call sites keeps every sampler caller honest. Per-stratum
    # seeding means the remaining draws are byte-identical to a sample taken from
    # a corpus that had no annex in it.
    docs = [d for d in docs if d.fmt not in EXPLORATORY_FORMATS]

    models = sorted({d.model for d in docs})
    if not models or size <= 0:
        return JudgeSample(size=size, seed=seed, note="empty corpus or zero size")

    pools: dict[tuple[str, str], list[str]] = defaultdict(list)
    for doc in docs:
        pools[(doc.model, doc.fmt)].append(doc.doc_id)
    for key in pools:
        pools[key].sort()

    formats = sorted({d.fmt for d in docs})
    per_model = size // len(models)
    base = per_model // len(formats) if formats else 0

    strata: list[SampleStratum] = []
    chosen: list[str] = []

    for model in models:
        taken_here: list[str] = []
        for fmt in formats:
            pool = pools.get((model, fmt), [])
            take = min(base, len(pool))
            picks = sorted(_rng(seed, model, fmt).sample(pool, take)) if take else []
            taken_here += picks
            strata.append(
                SampleStratum(model, fmt, len(pool), len(picks), tuple(picks))
            )

        # Remainder to the deepest pools: they are the ones that can spare a
        # document without emptying a stratum.
        remaining = per_model - len(taken_here)
        order = sorted(formats, key=lambda f: (-len(pools.get((model, f), [])), f))
        for fmt in order:
            if remaining <= 0:
                break
            spare = [d for d in pools.get((model, fmt), []) if d not in set(taken_here)]
            if not spare:
                continue
            take = min(remaining, len(spare))
            extra = sorted(_rng(seed, model, fmt, "extra").sample(spare, take))
            taken_here += extra
            remaining -= take
            for i, stratum in enumerate(strata):
                if stratum.model == model and stratum.fmt == fmt:
                    strata[i] = SampleStratum(
                        model,
                        fmt,
                        stratum.available,
                        stratum.taken + len(extra),
                        tuple(sorted(stratum.doc_ids + tuple(extra))),
                    )
                    break
        chosen += taken_here

    chosen = sorted(chosen)
    counts_model: dict[str, int] = defaultdict(int)
    counts_format: dict[str, int] = defaultdict(int)
    index = {d.doc_id: d for d in docs}
    for doc_id in chosen:
        doc = index[doc_id]
        counts_model[doc.model] += 1
        counts_format[doc.fmt] += 1

    return JudgeSample(
        size=size,
        seed=seed,
        doc_ids=tuple(chosen),
        strata=strata,
        per_model=dict(counts_model),
        per_format=dict(counts_format),
        note=(
            f"{per_model} per model, {base} per (model, format) plus "
            f"{per_model - base * len(formats)} from the deepest pools"
        ),
    )


def sample_from_list(docs: Sequence[Doc], doc_ids: Sequence[str]) -> JudgeSample:
    """An explicit sample, for re-running exactly what a previous run judged."""
    known = {d.doc_id for d in docs}
    wanted = [d for d in dict.fromkeys(doc_ids) if d in known]
    missing = [d for d in dict.fromkeys(doc_ids) if d not in known]
    index = {d.doc_id: d for d in docs}
    counts_model: dict[str, int] = defaultdict(int)
    counts_format: dict[str, int] = defaultdict(int)
    for doc_id in wanted:
        counts_model[index[doc_id].model] += 1
        counts_format[index[doc_id].fmt] += 1
    return JudgeSample(
        size=len(wanted),
        seed=-1,
        doc_ids=tuple(sorted(wanted)),
        per_model=dict(counts_model),
        per_format=dict(counts_format),
        note=(
            "explicit document list"
            + (f"; {len(missing)} id(s) not in this corpus: {missing[:5]}" if missing else "")
        ),
    )


def read_doc_list(path: Any) -> list[str]:
    """One document id per line; blanks and # comments ignored."""
    from pathlib import Path

    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


SAMPLE_FILENAME = "judge_sample.json"


def write_sample(sample: JudgeSample, run_dir: Any) -> Any:
    """Record the sample beside the scores it explains."""
    import json
    from pathlib import Path

    path = Path(run_dir) / SAMPLE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(sample.as_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return path


__all__ = [
    "DEFAULT_SEED",
    "DEFAULT_SIZE",
    "SAMPLE_FILENAME",
    "JudgeSample",
    "SampleStratum",
    "read_doc_list",
    "sample_from_list",
    "stratified_sample",
    "write_sample",
]
