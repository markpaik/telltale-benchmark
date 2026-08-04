"""Re-asking the judge the same question, to find out whether it answers twice.

A cache turns a stochastic instrument into a deterministic one — every later
run replays the first answer exactly. That is what makes a judge run
reproducible, and it is also what hides the thing a reader most wants to know:
how stable was the answer in the first place? A rubric that produces the same
span set on two independent calls is measuring something. One that produces a
different set each time is measuring the sampler.

So the audit takes a sample of the work a run cached, asks it again live, and
compares the span sets. It deliberately does **not** write its live answers to
the cache: overwriting the entry would destroy the very thing being compared
against, and would also make a scored run's evidence depend on when someone
last ran an audit.

Agreement is reported as Jaccard overlap on whitespace-normalized verified
quotes — two calls that find the same three spans score 1.0, two calls that
agree on two of three score 0.5. Both-empty counts as full agreement, because
"nothing here" twice is a reproduced answer.

The draw is stratified by tell and round-robin, not uniform over the cache.
Uniform sampling would spend the budget where the cache is deepest, and the
cache is deepest for whichever tell happens to chunk documents most finely —
which has nothing to do with which rubric a reader most needs a stability
number for. Equal coverage per tell means every rubric gets an estimate, and a
budget cap trims the tail of the round rather than a random tell's whole share.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Sequence

from telltale.corpus import Doc
from telltale.judge import cache as cache_mod
from telltale.judge import protocol
from telltale.registry import Tell

DEFAULT_PCT = 5.0
DEFAULT_SEED = 11


@dataclass
class AuditItem:
    """One re-asked extraction, and how the two answers compared."""

    tell_id: str
    doc_id: str
    chunk_index: int
    chunk_sha256: str
    stage: str
    cached_spans: int
    live_spans: int
    shared: int
    agreement: float
    cached_only: list[str] = field(default_factory=list)
    live_only: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditReport:
    judge_model: str
    protocol_version: int
    pct: float
    seed: int
    n_available: int
    n_sampled: int
    mean_agreement: float
    exact_matches: int
    timestamp: str
    items: list[AuditItem] = field(default_factory=list)
    note: str = ""
    n_requested: int = 0
    max_calls: int | None = None
    capped: bool = False

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["items"] = [i.as_dict() for i in self.items]
        data["per_tell"] = self.per_tell()
        return data

    def per_tell(self) -> dict[str, dict[str, Any]]:
        """Agreement per tell. A rubric's stability is a per-rubric fact."""
        out: dict[str, dict[str, Any]] = {}
        for item in self.items:
            row = out.setdefault(
                item.tell_id,
                {"n": 0, "identical": 0, "mean_agreement": 0.0, "_total": 0.0,
                 "cached_spans": 0, "live_spans": 0, "shared": 0},
            )
            row["n"] += 1
            row["_total"] += item.agreement
            row["identical"] += 1 if item.agreement == 1.0 else 0
            row["cached_spans"] += item.cached_spans
            row["live_spans"] += item.live_spans
            row["shared"] += item.shared
        for row in out.values():
            row["mean_agreement"] = row.pop("_total") / row["n"]
        return dict(sorted(out.items()))

    def summary(self) -> str:
        if not self.n_sampled:
            return (
                f"consistency audit: nothing to re-ask "
                f"({self.n_available} cached items available). {self.note}".strip()
            )
        head = (
            f"consistency audit: {self.n_sampled} of {self.n_available} cached "
            f"extractions re-asked live against {self.judge_model}; mean span-set "
            f"agreement {self.mean_agreement:.2f}, "
            f"{self.exact_matches}/{self.n_sampled} identical"
        )
        if self.capped:
            head += (
                f"\n  capped: {self.pct:g}% of the cache is {self.n_requested} "
                f"calls, trimmed to the {self.max_calls}-call budget"
            )
        lines = [head, "  tell                            n  mean  identical"]
        for tell_id, row in self.per_tell().items():
            lines.append(
                f"  {tell_id:<30} {row['n']:>3}  {row['mean_agreement']:.2f}  "
                f"{row['identical']}/{row['n']}"
            )
        return "\n".join(lines)


def _work_items(
    docs: Sequence[Doc], tells: Sequence[Tell]
) -> list[tuple[Tell, Doc, protocol.Chunk, str]]:
    """Every (tell, chunk) pair a judge run would have asked about, in order."""
    out: list[tuple[Tell, Doc, protocol.Chunk, str]] = []
    for tell in sorted(tells, key=lambda t: t.id):
        rule = protocol.rule_for(tell)
        stage = (
            cache_mod.STRUCTURAL if rule.kind == "structural" else cache_mod.EXTRACT
        )
        for doc in sorted(docs, key=lambda d: d.doc_id):
            for chunk in protocol.judge_view_text(tell, doc):
                out.append((tell, doc, chunk, stage))
    return out


def _prompt_for(tell: Tell, chunk: protocol.Chunk, stage: str) -> str:
    if stage == cache_mod.STRUCTURAL:
        return protocol.build_structural_prompt(tell, chunk.text)
    return protocol.build_extraction_prompt(tell, chunk.text)


def _verified_quotes(tell: Tell, payload: dict[str, Any], text: str, stage: str) -> set[str]:
    """The span set one answer actually supports, after quote verification."""
    quotes: set[str] = set()
    if stage == cache_mod.STRUCTURAL:
        pairs = protocol.structural_quotes(tell.id, payload)
        candidates = [quote for _, quote in pairs]
    else:
        candidates = [span["quote"] for span in protocol.extraction_spans(payload)]
    for candidate in candidates:
        match = protocol.verify_quote(candidate, text)
        if match is not None:
            quotes.add(match.normalized)
    return quotes


def _agreement(left: set[str], right: set[str]) -> tuple[int, float]:
    union = left | right
    if not union:
        return 0, 1.0
    shared = len(left & right)
    return shared, shared / len(union)


def _stratified_picks(
    available: Sequence[tuple[Tell, Doc, Any, str, dict[str, Any]]],
    n_sample: int,
    seed: int,
) -> list[int]:
    """Indices into `available`, drawn round-robin over tells.

    Each tell's pool is shuffled on its own seed, so adding a tell to the
    registry does not reshuffle everybody else's draw.
    """
    by_tell: dict[str, list[int]] = {}
    for index, entry in enumerate(available):
        by_tell.setdefault(entry[0].id, []).append(index)
    for tell_id, pool in by_tell.items():
        random.Random(f"{seed}|{tell_id}").shuffle(pool)

    picks: list[int] = []
    order = sorted(by_tell)
    round_index = 0
    while len(picks) < n_sample:
        took = False
        for tell_id in order:
            pool = by_tell[tell_id]
            if round_index < len(pool):
                picks.append(pool[round_index])
                took = True
                if len(picks) >= n_sample:
                    break
        if not took:
            break
        round_index += 1
    return sorted(picks)


def audit(
    docs: Sequence[Doc],
    tells: Sequence[Tell],
    client: Any,
    pct: float = DEFAULT_PCT,
    seed: int = DEFAULT_SEED,
    max_calls: int | None = None,
    progress: Any | None = None,
) -> AuditReport:
    """Re-ask `pct` percent of the cached extractions and compare span sets.

    `max_calls` is a budget ceiling. A live call costs about a minute, so a
    percentage over a large cache can quietly become an hour; the cap is
    recorded in the report rather than applied silently.
    """
    judge = [t for t in tells if t.method == "judge"]
    items = _work_items(docs, judge)

    available: list[tuple[Tell, Doc, protocol.Chunk, str, dict[str, Any]]] = []
    for tell, doc, chunk, stage in items:
        key = cache_mod.cache_key(
            chunk.sha256, tell.id, tell.rubric_version, client.model, stage
        )
        cached = client.cache.get(key)
        if cached is not None:
            available.append((tell, doc, chunk, stage, cached))

    n_requested = min(len(available), math.ceil(len(available) * (pct / 100.0)))
    n_sample = n_requested if max_calls is None else min(n_requested, int(max_calls))
    picks = _stratified_picks(available, n_sample, seed) if n_sample else []

    results: list[AuditItem] = []
    for position, index in enumerate(picks, start=1):
        tell, doc, chunk, stage, cached = available[index]
        if progress is not None:
            progress(f"AUDIT {position}/{len(picks)} {tell.id} {doc.doc_id}#{chunk.index}")
        live = client.transport.ask(_prompt_for(tell, chunk, stage))
        cached_set = _verified_quotes(tell, cached, chunk.text, stage)
        live_set = _verified_quotes(tell, live, chunk.text, stage)
        shared, score = _agreement(cached_set, live_set)
        results.append(
            AuditItem(
                tell_id=tell.id,
                doc_id=doc.doc_id,
                chunk_index=chunk.index,
                chunk_sha256=chunk.sha256[:16],
                stage=stage,
                cached_spans=len(cached_set),
                live_spans=len(live_set),
                shared=shared,
                agreement=score,
                cached_only=sorted(q[:80] for q in cached_set - live_set)[:5],
                live_only=sorted(q[:80] for q in live_set - cached_set)[:5],
            )
        )

    mean = (
        sum(item.agreement for item in results) / len(results) if results else float("nan")
    )
    return AuditReport(
        judge_model=str(client.model),
        protocol_version=protocol.PROTOCOL_VERSION,
        pct=float(pct),
        seed=int(seed),
        n_available=len(available),
        n_sampled=len(results),
        mean_agreement=mean,
        exact_matches=sum(1 for item in results if item.agreement == 1.0),
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        items=results,
        note="" if available else "no cached judge answers to audit",
        n_requested=n_requested,
        max_calls=None if max_calls is None else int(max_calls),
        capped=bool(n_sample < n_requested),
    )


__all__ = ["AuditItem", "AuditReport", "DEFAULT_PCT", "DEFAULT_SEED", "audit"]
