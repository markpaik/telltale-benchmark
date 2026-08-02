"""The judge backend that fills M5's `build(tell, judge=...)` seam.

`JudgeBackend` is a callable `(tell, doc) -> Detection`, which is exactly what
`detectors.build` wants. Everything model-facing is behind `JudgeClient`; what
this module owns is the arithmetic that turns judge answers into a measurement:

* **Chunk tells** run stage 1 over every chunk of the document, verify each
  quote against the chunk it came from, adjudicate the survivors one at a time,
  and sum the spans the *code* accepted. Chunks overlap, so the same span can be
  extracted twice; spans are deduplicated on their whitespace-normalized quote
  before adjudication, which also keeps the second copy from being paid for.
* **Skeleton tells** run one structural call over the document outline, verify
  every evidence quote it offers, drop the parts that do not verify, and apply
  the decision rule in `protocol`.

Two numbers are carried out of every detection whether or not anyone looks at
them: how many quotes did not verify (`hallucinated`), and how often the judge's
own verdict disagreed with the code's (`judge_disagreements`). The first is the
honesty check on the evidence; the second is the honesty check on the design —
if the code and the judge always agree, the two-stage protocol is costing money
for nothing, and if they never agree, the rubric is not saying what it thinks.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from telltale import textstats
from telltale.corpus import Doc
from telltale.detectors.base import MAX_MATCHES, Detection
from telltale.judge import cache as cache_mod
from telltale.judge import protocol
from telltale.registry import Tell

#: Rejected spans kept in `detail` for the audit trail. Enough to see the shape
#: of what the rubric threw away, not enough to bloat every scores.jsonl row.
MAX_REJECTED = 10


@dataclass
class SpanRun:
    """The outcome of running the two stages over one body of text."""

    counted: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    hallucinated: list[str] = field(default_factory=list)
    extracted: int = 0
    keys: list[str] = field(default_factory=list)
    judge_disagreements: int = 0
    #: Spans the line classifier disposed of without an adjudication call, and
    #: the tally of which line class did it. Kept as records, not just a count:
    #: a saving that cannot be audited is indistinguishable from a bug.
    code_excluded: list[dict[str, Any]] = field(default_factory=list)
    by_class: Counter = field(default_factory=Counter)
    #: Spans the per-chunk adjudication cap dropped, and whether it ever bit.
    capped: bool = False
    spans_skipped: int = 0

    def merge(self, other: "SpanRun") -> None:
        self.counted += other.counted
        self.rejected += other.rejected
        self.hallucinated += other.hallucinated
        self.extracted += other.extracted
        self.keys += other.keys
        self.judge_disagreements += other.judge_disagreements
        self.code_excluded += other.code_excluded
        self.by_class.update(other.by_class)
        self.capped = self.capped or other.capped
        self.spans_skipped += other.spans_skipped


@dataclass
class StructuralRun:
    """The outcome of one doc-level evidence call."""

    present: bool = False
    reason: str = ""
    matches: list[dict[str, Any]] = field(default_factory=list)
    hallucinated: list[str] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)


class JudgeBackend:
    """Callable `(tell, doc) -> Detection`, for `detectors.build(tell, judge=...)`."""

    def __init__(self, client: Any) -> None:
        self.client = client

    # -- the seam --

    def __call__(self, tell: Tell, doc: Doc) -> Detection:
        return self.detect(tell, doc)

    def detect(self, tell: Tell, doc: Doc) -> Detection:
        if tell.method != "judge":
            raise ValueError(f"{tell.id} is not a judge tell")
        rule = protocol.rule_for(tell)
        if rule.kind == "structural":
            return self._detect_structural(tell, doc)
        return self._detect_spans(tell, doc)

    # -- chunk tells --

    def _detect_spans(self, tell: Tell, doc: Doc) -> Detection:
        chunks = protocol.chunk_doc(doc)
        run = SpanRun()
        seen: set[str] = set()
        for chunk in chunks:
            run.merge(self.spans_for_text(tell, chunk.text, chunk.sha256, seen=seen))

        raw = float(len(run.counted))
        rate = (raw / doc.words * 1000.0) if doc.words else None
        # Counted spans first, so a document whose structure produced hundreds
        # of dispositioned spans can never crowd its real evidence out of the
        # window. Every entry says whether it counted, so `matches` is readable
        # as evidence without having to know which list it came from.
        counted = [{**record, "counted": True} for record in run.counted]
        matches = (counted + run.code_excluded)[:MAX_MATCHES]
        detail: dict[str, Any] = dict(
            chunks=len(chunks),
            view="chunk",
            extracted=run.extracted,
            adjudicated_true=len(run.counted),
            adjudicated_false=len(run.rejected),
            excluded_by_code=len(run.code_excluded),
            by_class=dict(sorted(run.by_class.items())),
            hallucinated=len(run.hallucinated),
            hallucinated_quotes=run.hallucinated[:MAX_REJECTED],
            judge_disagreements=run.judge_disagreements,
            rejected=run.rejected[:MAX_REJECTED],
            keys=run.keys,
        )
        if run.capped:
            # Only written when the cap actually bit. A truncated measurement
            # has to be visible in the row that carries it — a reader comparing
            # two documents must be able to see that one of them was cut short.
            detail["adjudication_capped"] = True
            detail["adjudication_cap"] = protocol.rule_for(tell).adjudication_cap
            detail["spans_skipped"] = run.spans_skipped
        return Detection(
            tell_id=tell.id,
            doc_id=doc.doc_id,
            raw=raw,
            rate_per_1k=rate,
            matches=matches,
            method="judge",
            unit=tell.unit,
            detail=self._detail(tell, **detail),
        )

    def spans_for_text(
        self,
        tell: Tell,
        text: str,
        source_sha: str | None = None,
        seen: set[str] | None = None,
    ) -> SpanRun:
        """Extract, verify, triage, and adjudicate over one passage.

        `seen` carries normalized quotes already handled, so a span sitting in
        the overlap between two chunks is counted — and paid for — once.

        Between verification and adjudication sits the structural triage added
        in protocol v3. A verified span whose line is a heading, a list item, a
        table row, a sign-off or a caption is dispositioned here, by the letter
        of the rubric's own structural exclusion, with no judge call — but only
        for tells that declare which of their letters are structural. Everything
        left is adjudicated in document order, up to the tell's cap.
        """
        sha = source_sha or protocol.Chunk.make("text", 0, text).sha256
        rule = protocol.rule_for(tell)
        run = SpanRun()
        seen = seen if seen is not None else set()

        payload, key, _ = self.client.ask(
            cache_mod.EXTRACT,
            sha,
            tell.id,
            tell.rubric_version,
            protocol.build_extraction_prompt(tell, text),
        )
        run.keys.append(key)

        pending: list[tuple[protocol.Match, dict[str, Any]]] = []
        for candidate in protocol.extraction_spans(payload):
            run.extracted += 1
            match = protocol.verify_quote(candidate["quote"], text)
            if match is None:
                run.hallucinated.append(candidate["quote"][:200])
                continue
            if match.normalized in seen:
                continue
            seen.add(match.normalized)

            line_class = textstats.classify_span(text, match.start, match.end)
            letter = protocol.structural_exclusion_for(rule, line_class)
            if letter is not None:
                run.code_excluded.append(
                    self._code_record(match, candidate, letter, line_class)
                )
                run.by_class[line_class] += 1
                continue
            pending.append((match, candidate))

        # Document order, then the cap. Ordering by offset rather than by the
        # judge's own listing order is what makes the truncation reproducible:
        # the same chunk always keeps the same spans, whatever order stage 1
        # happened to emit them in.
        pending.sort(key=lambda item: (item[0].start, item[0].end))
        cap = rule.adjudication_cap
        if cap is not None and len(pending) > cap:
            run.spans_skipped = len(pending) - cap
            run.capped = True
            for match, candidate in pending[cap:]:
                run.rejected.append(
                    {
                        "quote": match.quote,
                        "line": match.line,
                        "location_hint": candidate.get("location_hint", ""),
                        "criteria_met": [],
                        "exclusion_triggered": None,
                        "rationale": (
                            f"not adjudicated: over the {cap}-span per-chunk "
                            "adjudication cap"
                        ),
                        "judge_instance": None,
                        "why_not": "adjudication cap",
                    }
                )
            pending = pending[:cap]

        for match, candidate in pending:
            context = protocol.context_for(match, text)
            answer, adj_key, _ = self.client.ask(
                cache_mod.ADJUDICATE,
                sha,
                tell.id,
                tell.rubric_version,
                protocol.build_adjudication_prompt(tell, match.quote, context),
                quote=match.normalized,
            )
            run.keys.append(adj_key)

            counts, why_not = protocol.span_counts(rule, answer)
            judge_said = bool(answer.get("instance"))
            if judge_said != counts:
                run.judge_disagreements += 1
            record = {
                "quote": match.quote,
                "line": match.line,
                "location_hint": candidate.get("location_hint", ""),
                "criteria_met": [
                    protocol.normalize_label(c)
                    for c in (answer.get("criteria_met") or [])
                ],
                "exclusion_triggered": answer.get("exclusion_triggered"),
                "rationale": str(answer.get("rationale") or "")[:300],
                "judge_instance": judge_said,
            }
            if counts:
                run.counted.append(record)
            else:
                run.rejected.append({**record, "why_not": why_not})
        return run

    @staticmethod
    def _code_record(
        match: protocol.Match,
        candidate: dict[str, Any],
        letter: str,
        line_class: str,
    ) -> dict[str, Any]:
        """One span dispositioned by the line classifier, in the same shape as
        an adjudicated one, so a reader diffing the evidence sees the same
        fields whether a machine or a model decided.

        `judge_instance` is None rather than False: the judge was not asked, and
        recording a False it never said would put words in its mouth and inflate
        the disagreement counter with cases where there was no disagreement to
        have.
        """
        return {
            "quote": match.quote,
            "line": match.line,
            "location_hint": candidate.get("location_hint", ""),
            "criteria_met": [],
            "exclusion_triggered": letter,
            "rationale": f"line classified as {line_class}; excluded by ({letter})",
            "judge_instance": None,
            "excluded_by_code": True,
            "line_class": line_class,
            "counted": False,
        }

    # -- skeleton tells --

    def _detect_structural(self, tell: Tell, doc: Doc) -> Detection:
        view = protocol.skeleton_view(doc)
        chunk = protocol.Chunk.make(doc.doc_id, 0, view)
        run = self.structural_for_text(tell, view, chunk.sha256)
        return Detection(
            tell_id=tell.id,
            doc_id=doc.doc_id,
            raw=1.0 if run.present else 0.0,
            rate_per_1k=None,
            matches=run.matches[:MAX_MATCHES],
            method="judge",
            unit=tell.unit,
            detail=self._detail(
                tell,
                chunks=1,
                view="skeleton",
                extracted=len(run.matches) + len(run.hallucinated),
                adjudicated_true=1 if run.present else 0,
                adjudicated_false=0 if run.present else 1,
                hallucinated=len(run.hallucinated),
                hallucinated_quotes=run.hallucinated[:MAX_REJECTED],
                judge_disagreements=0,
                rejected=[],
                keys=run.keys,
                decision=run.reason,
            ),
        )

    def structural_for_text(
        self, tell: Tell, text: str, source_sha: str | None = None
    ) -> StructuralRun:
        """One evidence call, quote-verified, then the decision rule in code."""
        sha = source_sha or protocol.Chunk.make("text", 0, text).sha256
        payload, key, _ = self.client.ask(
            cache_mod.STRUCTURAL,
            sha,
            tell.id,
            tell.rubric_version,
            protocol.build_structural_prompt(tell, text),
        )
        run = StructuralRun(keys=[key])

        bad_paths: set[str] = set()
        verified: list[dict[str, Any]] = []
        for path, quote in protocol.structural_quotes(tell.id, payload):
            match = protocol.verify_quote(quote, text)
            if match is None:
                bad_paths.add(path)
                run.hallucinated.append(quote[:200])
                continue
            verified.append({"quote": match.quote, "line": match.line, "field": path})

        evidence = protocol.prune_unverified(tell.id, payload, bad_paths)
        decide = protocol.STRUCTURAL_DECISIONS[tell.id]
        run.present, run.reason = decide(evidence)
        run.evidence = evidence
        run.matches = verified if run.present else []
        return run

    # -- shared --

    def _detail(self, tell: Tell, **fields: Any) -> dict[str, Any]:
        detail = {
            "judge_model": getattr(self.client, "model", "unknown"),
            "rubric_version": tell.rubric_version,
            "protocol_version": protocol.PROTOCOL_VERSION,
        }
        keys = fields.pop("keys", [])
        detail.update(fields)
        detail["cache_keys"] = [k[:16] for k in keys]
        # Deliberately no cache hit/miss counts here. They are a property of the
        # run, not of the measurement, and a cumulative counter written into
        # every row would make scores.jsonl differ between a cold first run and
        # a warm replay — which is exactly what `report --verify` compares.
        return detail


def make_judge(client: Any) -> JudgeBackend:
    """The callable `detectors.build(tell, judge=...)` expects."""
    return JudgeBackend(client)


__all__ = ["JudgeBackend", "SpanRun", "StructuralRun", "make_judge"]
