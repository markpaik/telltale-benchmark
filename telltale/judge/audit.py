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

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["items"] = [i.as_dict() for i in self.items]
        return data

    def summary(self) -> str:
        if not self.n_sampled:
            return (
                f"consistency audit: nothing to re-ask "
                f"({self.n_available} cached items available). {self.note}".strip()
            )
        return (
            f"consistency audit: {self.n_sampled} of {self.n_available} cached "
            f"extractions re-asked live against {self.judge_model}; mean span-set "
            f"agreement {self.mean_agreement:.2f}, "
            f"{self.exact_matches}/{self.n_sampled} identical"
        )


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


def audit(
    docs: Sequence[Doc],
    tells: Sequence[Tell],
    client: Any,
    pct: float = DEFAULT_PCT,
    seed: int = DEFAULT_SEED,
) -> AuditReport:
    """Re-ask `pct` percent of the cached extractions and compare span sets."""
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

    n_sample = min(len(available), math.ceil(len(available) * (pct / 100.0)))
    picks = (
        sorted(random.Random(seed).sample(range(len(available)), n_sample))
        if n_sample
        else []
    )

    results: list[AuditItem] = []
    for index in picks:
        tell, doc, chunk, stage, cached = available[index]
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
    )


__all__ = ["AuditItem", "AuditReport", "DEFAULT_PCT", "DEFAULT_SEED", "audit"]
