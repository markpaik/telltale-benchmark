"""Re-asking the judge the same question, to find out whether it answers twice.

A cache turns a stochastic instrument into a deterministic one — every later
run replays the first answer exactly. That is what makes a judge run
reproducible, and it is also what hides the thing a reader most wants to know:
how stable was the answer in the first place? A rubric that produces the same
span set on two independent calls is measuring something. One that produces a
different set each time is measuring the sampler.

So the audit takes a sample of the work a run cached, asks it again live, and
compares the answers. It deliberately does **not** write its live answers to
the cache: overwriting the entry would destroy the very thing being compared
against, and would also make a scored run's evidence depend on when someone
last ran an audit.

**Both stages, because only both stages answer the question.** Stage-1
agreement is reported as Jaccard overlap on whitespace-normalized verified
quotes — two calls that find the same three spans score 1.0, two calls that
agree on two of three score 0.5, and both-empty is full agreement because
"nothing here" twice is a reproduced answer. That number alone overstates the
instability of a published count: `rht.rule-of-three` reproduced only 0.62 of
its spans, and 94% of those spans were then thrown away by an adjudicator
nobody had re-asked (SHAKEDOWN §2.7). Ruling R19 extends the audit to the
adjudications, where agreement is all-or-nothing on the three things that
decide a count: the verdict the *code* computes, the criteria letters the judge
returned, and the exclusion letter it returned. Two calls that reach the same
verdict by different criteria do not agree here, because the rubric arithmetic
is the measurement.

An adjudication is not reconstructible from its own cache entry — the key holds
the sha of the quote, not the quote. So the adjudication pool is rebuilt the way
the run built it: cached stage-1 answer, verified spans, context, adjudication
key. A span that never reached adjudication (dispositioned in code, or over the
cap) has no cached answer and so never enters the pool, which is right: the
audit measures what the run actually asked.

The draw is stratified by tell *and stage*, round-robin, not uniform over the
cache. Uniform sampling would spend the budget where the cache is deepest, and
the cache is deepest for whichever tell happens to chunk documents most finely —
which has nothing to do with which rubric a reader most needs a stability
number for. Equal coverage per tell means every rubric gets an estimate, and a
budget cap trims the tail of the round rather than a random tell's whole share.
`max_calls` caps the two stages together: it is a spend ceiling, and a live call
costs the same whichever stage asked it.
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

#: What an audited item re-asks: a stage-1 span proposal, or a stage-2 verdict.
EXTRACTION = "extraction"
ADJUDICATION = "adjudication"


@dataclass
class AuditItem:
    """One re-asked judge call, and how the two answers compared."""

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
    #: EXTRACTION or ADJUDICATION. Defaulted so an item written by the stage-1
    #: path reads exactly as it did before ruling R19.
    kind: str = EXTRACTION
    #: Adjudication items only: the span under review and the two verdicts, so a
    #: disagreement can be read without going back to the cache.
    quote: str = ""
    cached_verdict: bool | None = None
    live_verdict: bool | None = None
    cached_criteria: list[str] = field(default_factory=list)
    live_criteria: list[str] = field(default_factory=list)
    cached_exclusion: str | None = None
    live_exclusion: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


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

    # -- per-kind views --

    def of_kind(self, kind: str) -> list[AuditItem]:
        return [item for item in self.items if item.kind == kind]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["items"] = [i.as_dict() for i in self.items]
        data["per_tell"] = self.per_tell()
        data["per_tell_adjudication"] = self.per_tell_adjudication()
        data["extraction"] = self.kind_summary(EXTRACTION)
        data["adjudication"] = self.kind_summary(ADJUDICATION)
        return data

    def kind_summary(self, kind: str) -> dict[str, Any]:
        items = self.of_kind(kind)
        return {
            "n": len(items),
            "mean_agreement": _mean([i.agreement for i in items]),
            "identical": sum(1 for i in items if i.agreement == 1.0),
        }

    def _per_tell(self, kind: str) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for item in self.of_kind(kind):
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

    def per_tell(self) -> dict[str, dict[str, Any]]:
        """Stage-1 agreement per tell. A rubric's stability is a per-rubric fact."""
        return self._per_tell(EXTRACTION)

    def per_tell_adjudication(self) -> dict[str, dict[str, Any]]:
        """Stage-2 agreement per tell, kept in its own table on purpose.

        The two numbers are not the same measurement and averaging them would
        hide the one a reader needs: a tell can propose different spans every
        time and still adjudicate them the same way.
        """
        return self._per_tell(ADJUDICATION)

    def summary(self) -> str:
        if not self.n_sampled:
            return (
                f"consistency audit: nothing to re-ask "
                f"({self.n_available} cached items available). {self.note}".strip()
            )
        extraction = self.kind_summary(EXTRACTION)
        adjudication = self.kind_summary(ADJUDICATION)
        head = (
            f"consistency audit: {self.n_sampled} of {self.n_available} cached "
            f"judge calls re-asked live against {self.judge_model} "
            f"({extraction['n']} extraction, {adjudication['n']} adjudication)"
        )
        if self.capped:
            head += (
                f"\n  capped: {self.pct:g}% of the cache is {self.n_requested} "
                f"calls, trimmed to the {self.max_calls}-call budget"
            )
        lines = [head]
        for label, stats, table in (
            ("extraction", extraction, self.per_tell()),
            ("adjudication", adjudication, self.per_tell_adjudication()),
        ):
            if not stats["n"]:
                continue
            lines.append(
                f"  {label}: mean agreement {stats['mean_agreement']:.2f}, "
                f"{stats['identical']}/{stats['n']} identical"
            )
            lines.append("    tell                          n  mean  identical")
            for tell_id, row in table.items():
                lines.append(
                    f"    {tell_id:<28} {row['n']:>3}  {row['mean_agreement']:.2f}  "
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


def _verdict(
    rule: protocol.TellRule, payload: dict[str, Any]
) -> tuple[bool, tuple[str, ...], str | None]:
    """What one adjudication answer decides: verdict, criteria, exclusion.

    The verdict is the code's, not the judge's `instance` field, because the
    code's is what a published count is made of.
    """
    counts, _ = protocol.span_counts(rule, payload)
    criteria = {
        protocol.normalize_label(c) for c in (payload.get("criteria_met") or [])
    }
    criteria.discard("")
    exclusion = protocol.exclusion_fired(rule, payload.get("exclusion_triggered"))
    return bool(counts), tuple(sorted(criteria)), exclusion


def _adjudication_pool(
    tell: Tell,
    doc: Doc,
    chunk: protocol.Chunk,
    cached_extraction: dict[str, Any],
    client: Any,
) -> list[tuple[Tell, Doc, protocol.Chunk, str, dict[str, Any], dict[str, Any]]]:
    """Every adjudication this chunk's cached spans actually paid for.

    Rebuilt rather than read: the adjudication cache entry holds the sha of the
    quote, so the quote itself has to come back from the stage-1 answer. A span
    whose adjudication is not in the cache was never adjudicated — code
    disposition, the per-chunk cap, or a failed call — and it is not audited,
    because the audit re-asks questions the run asked.
    """
    out = []
    seen: set[str] = set()
    for candidate in protocol.extraction_spans(cached_extraction):
        match = protocol.verify_quote(candidate["quote"], chunk.text)
        if match is None or match.normalized in seen:
            continue
        seen.add(match.normalized)
        key = cache_mod.cache_key(
            chunk.sha256,
            tell.id,
            tell.rubric_version,
            client.model,
            cache_mod.ADJUDICATE,
            match.normalized,
        )
        cached = client.cache.get(key)
        if cached is None:
            continue
        out.append(
            (
                tell,
                doc,
                chunk,
                cache_mod.ADJUDICATE,
                cached,
                {"quote": match.quote, "context": protocol.context_for(match, chunk.text)},
            )
        )
    return out


def _stratified_picks(
    available: Sequence[tuple[Any, ...]],
    n_sample: int,
    seed: int,
) -> list[int]:
    """Indices into `available`, drawn round-robin over (tell, stage) pools.

    Each pool is shuffled on its own seed, so adding a tell to the registry — or
    adding the adjudication stage, as ruling R19 did — does not reshuffle
    everybody else's draw.
    """
    by_pool: dict[str, list[int]] = {}
    for index, entry in enumerate(available):
        pool_id = f"{entry[0].id}|{entry[3]}"
        by_pool.setdefault(pool_id, []).append(index)
    for pool_id, pool in by_pool.items():
        random.Random(f"{seed}|{pool_id}").shuffle(pool)

    picks: list[int] = []
    order = sorted(by_pool)
    round_index = 0
    while len(picks) < n_sample:
        took = False
        for pool_id in order:
            pool = by_pool[pool_id]
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
    stages: Sequence[str] = (EXTRACTION, ADJUDICATION),
) -> AuditReport:
    """Re-ask `pct` percent of the cached judge calls and compare the answers.

    `max_calls` is a budget ceiling over both stages together. A live call costs
    about a minute, so a percentage over a large cache can quietly become an
    hour; the cap is recorded in the report rather than applied silently.
    """
    judge = [t for t in tells if t.method == "judge"]
    items = _work_items(docs, judge)

    available: list[tuple[Any, ...]] = []
    for tell, doc, chunk, stage in items:
        key = cache_mod.cache_key(
            chunk.sha256, tell.id, tell.rubric_version, client.model, stage
        )
        cached = client.cache.get(key)
        if cached is None:
            continue
        if EXTRACTION in stages:
            available.append((tell, doc, chunk, stage, cached, None))
        if ADJUDICATION in stages and stage == cache_mod.EXTRACT:
            available.extend(
                _adjudication_pool(tell, doc, chunk, cached, client)
            )

    n_requested = min(len(available), math.ceil(len(available) * (pct / 100.0)))
    n_sample = n_requested if max_calls is None else min(n_requested, int(max_calls))
    picks = _stratified_picks(available, n_sample, seed) if n_sample else []

    results: list[AuditItem] = []
    for position, index in enumerate(picks, start=1):
        tell, doc, chunk, stage, cached, extra = available[index]
        kind = ADJUDICATION if stage == cache_mod.ADJUDICATE else EXTRACTION
        if progress is not None:
            progress(
                f"AUDIT {position}/{len(picks)} {kind} {tell.id} "
                f"{doc.doc_id}#{chunk.index}"
            )
        if kind == ADJUDICATION:
            prompt = protocol.build_adjudication_prompt(
                tell, extra["quote"], extra["context"]
            )
            live = client.transport.ask(prompt)
            rule = protocol.rule_for(tell)
            cached_verdict, cached_criteria, cached_exclusion = _verdict(rule, cached)
            live_verdict, live_criteria, live_exclusion = _verdict(rule, live)
            same = (
                cached_verdict == live_verdict
                and cached_criteria == live_criteria
                and cached_exclusion == live_exclusion
            )
            results.append(
                AuditItem(
                    tell_id=tell.id,
                    doc_id=doc.doc_id,
                    chunk_index=chunk.index,
                    chunk_sha256=chunk.sha256[:16],
                    stage=stage,
                    kind=ADJUDICATION,
                    cached_spans=1,
                    live_spans=1,
                    shared=1 if same else 0,
                    agreement=1.0 if same else 0.0,
                    quote=extra["quote"][:200],
                    cached_verdict=cached_verdict,
                    live_verdict=live_verdict,
                    cached_criteria=list(cached_criteria),
                    live_criteria=list(live_criteria),
                    cached_exclusion=cached_exclusion,
                    live_exclusion=live_exclusion,
                )
            )
            continue

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
                kind=EXTRACTION,
                cached_spans=len(cached_set),
                live_spans=len(live_set),
                shared=shared,
                agreement=score,
                cached_only=sorted(q[:80] for q in cached_set - live_set)[:5],
                live_only=sorted(q[:80] for q in live_set - cached_set)[:5],
            )
        )

    return AuditReport(
        judge_model=str(client.model),
        protocol_version=protocol.PROTOCOL_VERSION,
        pct=float(pct),
        seed=int(seed),
        n_available=len(available),
        n_sampled=len(results),
        # Deliberately the stage-1 figure alone: it is the number SHAKEDOWN §2.7
        # publishes, and averaging a Jaccard overlap together with an
        # all-or-nothing verdict match would produce a number that means
        # nothing. The stage-2 figure lives in `kind_summary(ADJUDICATION)`.
        mean_agreement=_mean(
            [i.agreement for i in results if i.kind == EXTRACTION]
        ),
        exact_matches=sum(
            1 for i in results if i.kind == EXTRACTION and i.agreement == 1.0
        ),
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        items=results,
        note="" if available else "no cached judge answers to audit",
        n_requested=n_requested,
        max_calls=None if max_calls is None else int(max_calls),
        capped=bool(n_sample < n_requested),
    )


__all__ = [
    "ADJUDICATION",
    "EXTRACTION",
    "AuditItem",
    "AuditReport",
    "DEFAULT_PCT",
    "DEFAULT_SEED",
    "audit",
]
