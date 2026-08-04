"""The five gates a proposed tell has to clear before it enters the registry.

A model asked "what does this model overuse?" will always answer. That is the
whole problem: the lens is generative, so the pipeline downstream of it has to
be the opposite — a sequence of ways for a proposal to die, each testing
something a plausible-sounding candidate can still fail.

    1  executability   does the rule RUN, cheaply, without matching everything?
    2  prevalence      does it fire often enough to be worth a registry slot?
    3  discrimination  does it separate models, and at what scope?
    4  precision       when it fires, is that a real instance? (judge-adjudicated)
    5  dedup           is this already a tell under another name?

The order is cost-ascending and the gates short-circuit, which is not a
micro-optimization: gate 4 spends real money per candidate, so a degenerate
pattern must be dead long before it gets there. `.*` matches every token and
dies at gate 1 for a hundredth of a cent.

Two decisions worth stating.

**Gate 3 decides scope; it does not merely check it.** The lens offers a
`scope_hypothesis` and the lens is guessing. What lands in the registry is what
the corpus supports: model-scoped only when the target's document frequency is
at least three times *every* other model's and a two-proportion z clears 2.58,
general when it is common in at least two models, and rejected when neither
holds. A tell that fires equally everywhere is a fact about the genre, not about
a model, and the benchmark has no use for it.

**Nothing here writes stat code, and nothing here promotes.** A statistic
candidate naming a function that does not exist is not rejected — it is parked
at `needs-stat-implementation` for a human, because the alternative is a
discovery pipeline that writes its own measurement instruments. Everything that
does pass enters the registry with `status: candidate`, which the default
scoring path ignores; promotion stays a human decision, and for judge candidates
it stays a human decision *after* the M6 calibration gate.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping, Sequence

from telltale import textstats
from telltale.corpus import Doc
from telltale.detectors.regex_detector import finditer_guarded
from telltale.discovery import dedup as dedup_mod
from telltale.judge import cache as cache_mod
from telltale.judge import protocol
from telltale.registry import FLAG_MAP, Registry, Tell

# --- thresholds --------------------------------------------------------------

#: Gate 1. A pattern is a measurement instrument, not a search: one that matches
#: 5% of the corpus's tokens is measuring English.
MAX_TOKEN_SHARE = 0.05
MAX_MEDIAN_MS = 100.0
TIMING_DOCS = 20

#: Wall-clock budget for the whole regex probe, and why it is this number rather
#: than a round one: `MAX_MEDIAN_MS` already says a pattern may take 100ms per
#: document, and the probe runs `TIMING_DOCS` of them, so 2.0s is exactly the
#: time the median check would tolerate. A pattern that cannot finish inside it
#: is failing gate 1 either way — the timeout only makes it fail in bounded
#: time instead of unbounded. The allowance covers interpreter start (~15ms
#: measured) with room to spare on a loaded machine.
REGEX_PROBE_BUDGET_S = TIMING_DOCS * MAX_MEDIAN_MS / 1000.0
REGEX_PROBE_STARTUP_S = 0.3

#: Matches carried back from the probe. A pattern producing more than this over
#: twenty documents has already blown the token-share ceiling many times over,
#: so the excess is counted and discarded rather than serialized.
MAX_PROBE_SPANS = 50000

#: Gate 2. Either floor is enough — a binary-ish habit that shows up in one
#: document in twenty, or a steady drip of a tenth of an occurrence per 1k words.
MIN_DOC_FREQ = 0.05
MIN_MEAN_RATE = 0.1

#: Gate 3. Three times the next model's document frequency, and a two-proportion
#: z past the 0.01 two-tailed critical value.
SCOPE_RATIO = 3.0
SCOPE_Z = 2.58
GENERAL_MIN_MODELS = 2

#: Gate 4. Ten adjudicated spans, eight of which must be true instances.
PRECISION_SAMPLE = 10
PRECISION_MIN = 0.8
PRECISION_SEED = 13

#: The ad-hoc rubric's version, for the judge cache key. Bumped when the wording
#: below changes, because a different question is a different answer.
ADHOC_RUBRIC_VERSION = 1

STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"
STATUS_NEEDS_STAT = "needs-stat-implementation"

RAW_TEXT_CATEGORIES = frozenset({"punctuation", "structural"})

CATEGORY_PREFIX = {
    "lexical": "lex",
    "punctuation": "pnc",
    "syntactic": "rht",
    "structural": "str",
    "statistical": "sta",
}


# --- results -----------------------------------------------------------------


@dataclass
class GateResult:
    """One gate's verdict on one candidate."""

    gate: int
    name: str
    passed: bool
    detail: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "name": self.name,
            "passed": self.passed,
            "detail": self.detail,
            "data": _clean(self.data),
        }


@dataclass
class Verdict:
    """Everything the pipeline concluded about one candidate."""

    candidate: dict[str, Any]
    status: str = STATUS_REJECTED
    scope: str = ""
    reason: str = ""
    gates: list[GateResult] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return self.status == STATUS_ACCEPTED

    @property
    def name(self) -> str:
        return str(self.candidate.get("name") or "")

    def gate(self, number: int) -> GateResult | None:
        for result in self.gates:
            if result.gate == number:
                return result
        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate": self.candidate,
            "status": self.status,
            "scope": self.scope,
            "reason": self.reason,
            "flags": list(self.flags),
            "gates": [g.as_dict() for g in self.gates],
            "evidence": _clean(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Verdict":
        """Rebuild a verdict written to verdicts.jsonl.

        Needed for resuming: a run that died between the verify stage and the
        append stage has the verdicts on disk and nothing in the registry, and
        re-verifying would spend gate 4's judge calls again to reach the same
        answer.
        """
        return cls(
            candidate=dict(data.get("candidate") or {}),
            status=str(data.get("status") or STATUS_REJECTED),
            scope=str(data.get("scope") or ""),
            reason=str(data.get("reason") or ""),
            gates=[
                GateResult(
                    gate=int(g.get("gate", 0)),
                    name=str(g.get("name") or ""),
                    passed=bool(g.get("passed")),
                    detail=str(g.get("detail") or ""),
                    data=dict(g.get("data") or {}),
                )
                for g in (data.get("gates") or [])
                if isinstance(g, Mapping)
            ],
            evidence=dict(data.get("evidence") or {}),
            flags=[str(f) for f in (data.get("flags") or [])],
        )

    def summary(self) -> str:
        mark = {
            STATUS_ACCEPTED: "ACCEPT",
            STATUS_REJECTED: "REJECT",
            STATUS_NEEDS_STAT: "PARK  ",
        }.get(self.status, "?     ")
        scope = f" [{self.scope}]" if self.scope else ""
        flags = f" flags={','.join(self.flags)}" if self.flags else ""
        return f"{mark} {self.name!r}{scope}: {self.reason}{flags}"


def _clean(value: Any) -> Any:
    """NaN and numpy scalars out; plain JSON/YAML-safe values in."""
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            value = value.item()
        except (ValueError, AttributeError):  # pragma: no cover - defensive
            return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, 6)
    return value


# --- measuring a candidate over the corpus -----------------------------------


def compile_rule(candidate: Mapping[str, Any]) -> re.Pattern[str]:
    """Compile a regex candidate's pattern with its declared flags."""
    rule = candidate.get("rule") or {}
    flags = 0
    for name in rule.get("flags") or []:
        flags |= FLAG_MAP.get(str(name), 0)
    return re.compile(str(rule.get("pattern") or ""), flags)


def source_for(category: str, doc: Doc) -> str:
    """The view of a document a candidate's rule runs against.

    Routed exactly as `detectors/regex_detector.source_for` routes it, because a
    candidate verified against one text and detected against another has not
    been verified at all.
    """
    return doc.text if category in RAW_TEXT_CATEGORIES else doc.plain


@dataclass
class Measurement:
    """One candidate's behaviour over the corpus, per document."""

    counts: dict[str, float] = field(default_factory=dict)
    values: dict[str, float] = field(default_factory=dict)
    model_of: dict[str, str] = field(default_factory=dict)
    words: dict[str, int] = field(default_factory=dict)
    spans: list[tuple[str, str]] = field(default_factory=list)  # (doc_id, quote)
    kind: str = "count"

    @property
    def models(self) -> list[str]:
        return sorted(set(self.model_of.values()))

    def docs_of(self, model: str) -> list[str]:
        return sorted(d for d, m in self.model_of.items() if m == model)

    def fired(self, doc_id: str) -> bool:
        if self.kind == "value":
            value = self.values.get(doc_id, float("nan"))
            return not math.isnan(value)
        return self.counts.get(doc_id, 0.0) > 0

    def doc_freq(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for model in self.models:
            docs = self.docs_of(model)
            out[model] = (
                sum(1 for d in docs if self.fired(d)) / len(docs) if docs else 0.0
            )
        return out

    def doc_hits(self) -> dict[str, tuple[int, int]]:
        return {
            model: (
                sum(1 for d in self.docs_of(model) if self.fired(d)),
                len(self.docs_of(model)),
            )
            for model in self.models
        }

    def mean_rate(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for model in self.models:
            rates = [
                1000.0 * self.counts.get(d, 0.0) / self.words[d]
                for d in self.docs_of(model)
                if self.words.get(d)
            ]
            out[model] = sum(rates) / len(rates) if rates else 0.0
        return out

    def model_values(self, model: str) -> list[float]:
        return [
            self.values[d]
            for d in self.docs_of(model)
            if d in self.values and not math.isnan(self.values[d])
        ]


def measure(candidate: Mapping[str, Any], docs: Sequence[Doc]) -> Measurement:
    """Run a candidate over every document. Regex and statistic only.

    Judge candidates are not measured here and must not be: measuring one means
    a judge call per document, which is the cost of a full scoring run spent on
    an unverified proposal. `verify_candidate` defers their prevalence and scope
    to calibration instead, and records that it did.
    """
    method = str(candidate.get("method") or "")
    category = str(candidate.get("category") or "")
    out = Measurement(kind="value" if method == "statistic" else "count")

    ordered = sorted(docs, key=lambda d: d.doc_id)
    if method == "regex":
        pattern = compile_rule(candidate)
        for doc in ordered:
            source = source_for(category, doc)
            hits = list(pattern.finditer(source))
            out.counts[doc.doc_id] = float(len(hits))
            out.model_of[doc.doc_id] = doc.model
            out.words[doc.doc_id] = doc.words
            for hit in hits:
                out.spans.append((doc.doc_id, source[hit.start() : hit.end()]))
    elif method == "statistic":
        rule = candidate.get("rule") or {}
        stat_name = str(rule.get("stat_name") or "")
        fn = textstats.STATS.get(stat_name)
        for doc in ordered:
            out.model_of[doc.doc_id] = doc.model
            out.words[doc.doc_id] = doc.words
            value = float(fn(doc)) if fn is not None else float("nan")
            out.values[doc.doc_id] = value
            out.counts[doc.doc_id] = 0.0 if math.isnan(value) else value
    else:
        for doc in ordered:
            out.model_of[doc.doc_id] = doc.model
            out.words[doc.doc_id] = doc.words
    return out


# --- gate 1: executability ---------------------------------------------------


def gate_executable(
    candidate: Mapping[str, Any], docs: Sequence[Doc]
) -> tuple[GateResult, str]:
    """Does the rule run, fast, without matching the language itself?

    Returns the gate result and a status hint: a statistic naming a function
    nobody has written is `needs-stat-implementation`, which is a different
    outcome from a failure and must not be recorded as one.
    """
    method = str(candidate.get("method") or "")
    if method == "regex":
        return _gate_regex(candidate, docs), ""
    if method == "statistic":
        return _gate_statistic(candidate)
    if method == "judge":
        return _gate_judge_rubric(candidate), ""
    return (
        GateResult(1, "executability", False, f"unknown method {method!r}"),
        "",
    )


#: The probe body, run by a fresh interpreter. Deliberately tiny and importing
#: nothing from this package: it has to start fast, and everything it could get
#: wrong is a threshold decision that belongs in the parent where it is testable.
#: It reports spans and timings; the parent counts tokens and applies the rules.
_PROBE_SOURCE = """\
import json, re, sys, time
payload = json.loads(sys.stdin.read())
pattern = re.compile(payload["pattern"], payload["flags"])
limit = payload["max_spans"]
out = []
for source in payload["sources"]:
    start = time.perf_counter()
    spans = []
    dropped = 0
    for match in pattern.finditer(source):
        if len(spans) < limit:
            spans.append([match.start(), match.end()])
        else:
            dropped += 1
    out.append({
        "ms": (time.perf_counter() - start) * 1000.0,
        "spans": spans,
        "dropped": dropped,
    })
sys.stdout.write(json.dumps({"docs": out}))
"""


class ProbeTimeout(RuntimeError):
    """The regex probe did not finish inside its budget."""


def probe_regex(
    pattern_text: str,
    flags: int,
    sources: Sequence[str],
    budget_s: float = REGEX_PROBE_BUDGET_S,
    max_spans: int = MAX_PROBE_SPANS,
) -> list[dict[str, Any]]:
    """Run one pattern over `sources` in a child process, under a hard deadline.

    A separate PROCESS rather than a separate thread, and that is not a style
    preference. CPython's `re` engine holds the GIL for the whole of a match, so
    a catastrophically backtracking pattern — `(a+)+b` against a run of forty
    unbroken `a`s, which an LLM will happily propose after seeing a dashed rule
    or a repeated placeholder — freezes every thread in the interpreter. A
    `Thread.join(timeout=...)` in the parent never gets scheduled to return.
    Measured here: that call does not come back at all.

    A child process has no such problem. `subprocess.run` sends SIGKILL after
    the deadline, so nothing is left running and nothing has to be documented as
    "dies with the process later" — the cost is one interpreter start, measured
    at ~15ms against a budget of seconds.

    Raises `ProbeTimeout` when the deadline passes, which the caller turns into
    a rejection rather than a crash.
    """
    payload = json.dumps(
        {
            "pattern": pattern_text,
            "flags": int(flags),
            "sources": list(sources),
            "max_spans": int(max_spans),
        }
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", _PROBE_SOURCE],
            input=payload,
            capture_output=True,
            text=True,
            timeout=budget_s + REGEX_PROBE_STARTUP_S,
        )
    except subprocess.TimeoutExpired as exc:
        raise ProbeTimeout(
            f"the pattern did not finish {len(sources)} document(s) in "
            f"{budget_s:.1f}s"
        ) from exc
    if result.returncode != 0:
        raise ProbeTimeout(
            f"the regex probe exited {result.returncode}: {result.stderr.strip()[:200]}"
        )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise ProbeTimeout(f"the regex probe returned no usable result: {exc}") from None
    return list(data.get("docs") or [])


def _gate_regex(candidate: Mapping[str, Any], docs: Sequence[Doc]) -> GateResult:
    rule = candidate.get("rule") or {}
    pattern_text = str(rule.get("pattern") or "")
    if not pattern_text:
        return GateResult(1, "executability", False, "regex candidate has no pattern")
    for name in rule.get("flags") or []:
        if str(name) not in FLAG_MAP:
            return GateResult(
                1, "executability", False, f"unknown regex flag {str(name)!r}"
            )
    try:
        compiled = compile_rule(candidate)
    except (re.error, TypeError) as exc:
        return GateResult(1, "executability", False, f"pattern does not compile: {exc}")

    category = str(candidate.get("category") or "")
    sample = sorted(docs, key=lambda d: d.doc_id)[:TIMING_DOCS]
    if not sample:
        return GateResult(
            1, "executability", True, "compiles; no documents to time it against"
        )

    sources = [source_for(category, doc) for doc in sample]
    try:
        probed = probe_regex(pattern_text, compiled.flags, sources)
    except ProbeTimeout as exc:
        return GateResult(
            1,
            "executability",
            False,
            f"pathological-regex (timed out): {exc}. A pattern that can backtrack "
            "this far is not a measurement instrument, whatever it matches",
            {
                "timed_out": True,
                "budget_s": REGEX_PROBE_BUDGET_S,
                "docs_timed": len(sample),
            },
        )

    timings: list[float] = []
    matched_tokens = 0
    total_tokens = 0
    dropped = 0
    for source, entry in zip(sources, probed):
        timings.append(float(entry.get("ms") or 0.0))
        dropped += int(entry.get("dropped") or 0)
        for start, end in entry.get("spans") or []:
            matched_tokens += len(textstats.WORD_PATTERN.findall(source[start:end]))
        total_tokens += len(textstats.WORD_PATTERN.findall(source))

    if not timings:  # pragma: no cover - defensive
        return GateResult(1, "executability", False, "the regex probe reported nothing")

    timings.sort()
    median_ms = timings[len(timings) // 2]
    share = (matched_tokens / total_tokens) if total_tokens else 0.0
    data = {
        "median_ms": median_ms,
        "matched_token_share": share,
        "docs_timed": len(sample),
        "matched_tokens": matched_tokens,
        "total_tokens": total_tokens,
    }
    if dropped:
        data["spans_dropped"] = dropped
    if median_ms >= MAX_MEDIAN_MS:
        return GateResult(
            1,
            "executability",
            False,
            f"median {median_ms:.1f}ms over {len(sample)} docs exceeds {MAX_MEDIAN_MS:.0f}ms",
            data,
        )
    if share >= MAX_TOKEN_SHARE:
        return GateResult(
            1,
            "executability",
            False,
            f"matches {100 * share:.1f}% of tokens, over the {100 * MAX_TOKEN_SHARE:.0f}% ceiling "
            "— this is measuring the language, not a habit",
            data,
        )
    return GateResult(
        1,
        "executability",
        True,
        f"compiles, median {median_ms:.1f}ms, {100 * share:.2f}% of tokens",
        data,
    )


def _gate_statistic(candidate: Mapping[str, Any]) -> tuple[GateResult, str]:
    rule = candidate.get("rule") or {}
    stat_name = str(rule.get("stat_name") or "").strip()
    if not stat_name:
        return (
            GateResult(1, "executability", False, "statistic candidate names no stat"),
            "",
        )
    if stat_name not in textstats.STATS:
        return (
            GateResult(
                1,
                "executability",
                False,
                f"{stat_name!r} is not a registered textstats function; a human has to "
                "implement and review it before it can be measured",
                {"stat_name": stat_name, "formula_sketch": rule.get("formula_sketch")},
            ),
            STATUS_NEEDS_STAT,
        )
    return (
        GateResult(
            1,
            "executability",
            True,
            f"{stat_name} is a registered statistic",
            {"stat_name": stat_name},
        ),
        "",
    )


def _gate_judge_rubric(candidate: Mapping[str, Any]) -> GateResult:
    rule = candidate.get("rule") or {}
    rubric = str(rule.get("rubric") or "")
    view = str(rule.get("judge_view") or "")
    if view not in {"chunk", "skeleton"}:
        return GateResult(
            1, "executability", False, f"judge_view must be chunk|skeleton, got {view!r}"
        )
    inclusion, exclusions, _ = protocol.split_rubric(rubric)
    criteria, exclusion_labels = protocol.parse_rubric_labels(rubric)
    data = {
        "criteria": list(criteria),
        "exclusions": list(exclusion_labels),
        "has_exclusion_heading": bool(exclusions.strip()),
        "judge_view": view,
    }
    if not inclusion.strip():
        return GateResult(1, "executability", False, "rubric has no inclusion criteria", data)
    if not criteria:
        return GateResult(
            1,
            "executability",
            False,
            "rubric has no (a)/(b)-style criterion labels at line starts, so no decision "
            "rule can be built from it",
            data,
        )
    return GateResult(
        1,
        "executability",
        True,
        f"rubric parses: criteria {list(criteria)}, exclusions {list(exclusion_labels)}",
        data,
    )


# --- gate 2: prevalence ------------------------------------------------------


def gate_prevalence(measurement: Measurement) -> GateResult:
    """Does it fire often enough anywhere to be worth measuring?"""
    freqs = measurement.doc_freq()
    rates = measurement.mean_rate()
    data = {"doc_freq": freqs, "mean_rate_per_1k": rates}
    if not freqs:
        return GateResult(2, "prevalence", False, "no documents to measure against", data)

    by_freq = max(freqs.values())
    by_rate = max(rates.values()) if rates else 0.0
    if by_freq >= MIN_DOC_FREQ or by_rate >= MIN_MEAN_RATE:
        winner = max(freqs, key=lambda m: freqs[m])
        return GateResult(
            2,
            "prevalence",
            True,
            f"fires in {100 * by_freq:.0f}% of {winner} docs, top mean rate "
            f"{by_rate:.2f}/1k",
            data,
        )
    return GateResult(
        2,
        "prevalence",
        False,
        f"top document frequency {100 * by_freq:.1f}% < {100 * MIN_DOC_FREQ:.0f}% and top "
        f"mean rate {by_rate:.3f} < {MIN_MEAN_RATE}/1k",
        data,
    )


# --- gate 3: discrimination and scope ---------------------------------------


def two_proportion_z(k1: int, n1: int, k2: int, n2: int) -> float:
    """Pooled two-proportion z for (k1/n1) against (k2/n2). NaN when undefined."""
    if n1 <= 0 or n2 <= 0:
        return float("nan")
    p1, p2 = k1 / n1, k2 / n2
    pooled = (k1 + k2) / (n1 + n2)
    denominator = pooled * (1 - pooled) * (1 / n1 + 1 / n2)
    if denominator <= 0:
        return float("nan")
    return (p1 - p2) / math.sqrt(denominator)


def gate_scope(
    measurement: Measurement, target_model: str | None = None
) -> tuple[GateResult, str]:
    """Decide the scope the corpus supports. Returns (gate, scope)."""
    hits = measurement.doc_hits()
    freqs = measurement.doc_freq()
    data: dict[str, Any] = {"doc_freq": freqs, "doc_hits": {k: list(v) for k, v in hits.items()}}
    if not hits:
        return GateResult(3, "discrimination", False, "no documents", data), ""

    candidates = [target_model] if target_model in hits else sorted(hits)
    best: tuple[str, float, float] | None = None
    for model in candidates:
        k1, n1 = hits[model]
        k2 = sum(hits[m][0] for m in hits if m != model)
        n2 = sum(hits[m][1] for m in hits if m != model)
        others = [freqs[m] for m in freqs if m != model]
        ratio_ok = bool(others) and all(
            freqs[model] >= SCOPE_RATIO * other for other in others
        )
        z = two_proportion_z(k1, n1, k2, n2)
        data.setdefault("scope_z", {})[model] = z
        if ratio_ok and not math.isnan(z) and z >= SCOPE_Z:
            if best is None or z > best[2]:
                best = (model, freqs[model], z)

    if best is not None:
        model, freq, z = best
        scope = f"model:{model}"
        return (
            GateResult(
                3,
                "discrimination",
                True,
                f"{model} fires in {100 * freq:.0f}% of its docs, at least {SCOPE_RATIO:g}x "
                f"every other model, two-proportion z = {z:.2f}",
                {**data, "chosen": scope},
            ),
            scope,
        )

    common = sorted(m for m, f in freqs.items() if f >= MIN_DOC_FREQ)
    if len(common) >= GENERAL_MIN_MODELS:
        return (
            GateResult(
                3,
                "discrimination",
                True,
                f"fires in >= {100 * MIN_DOC_FREQ:.0f}% of docs for {len(common)} models "
                f"({', '.join(common)}); general",
                {**data, "chosen": "general"},
            ),
            "general",
        )
    return (
        GateResult(
            3,
            "discrimination",
            False,
            "concentrated in no model (no 3x + z >= 2.58) and common in fewer than "
            f"{GENERAL_MIN_MODELS} models",
            data,
        ),
        "",
    )


# --- gate 4: precision -------------------------------------------------------


def adhoc_rubric(candidate: Mapping[str, Any]) -> str:
    """The rubric gate 4 adjudicates against, built from the candidate itself.

    Deterministic in the candidate, and written in the three-part shape
    `protocol.split_rubric` parses, so the M6 adjudication prompt can be reused
    unchanged. There is exactly one criterion — is this quote a true instance of
    the described pattern — because that is the only question gate 4 asks; the
    single exclusion covers the failure mode a regex has and a reader does not:
    the surface string appearing in some other sense.
    """
    name = str(candidate.get("name") or "unnamed pattern").strip()
    rationale = " ".join(str(candidate.get("rationale") or "").split())
    rule = candidate.get("rule") or {}
    method = str(candidate.get("method") or "")
    if method == "regex":
        rule_line = f"Detected by the regular expression: {rule.get('pattern')!r}"
    elif method == "statistic":
        rule_line = f"Measured by the statistic {rule.get('stat_name')!r}."
    else:
        rule_line = "Detected by a judge rubric."

    return (
        "A span counts as an instance when ALL of the following hold.\n"
        f"(a) The span is a true instance of this pattern: {name} — {rationale}\n"
        f"    {rule_line}\n"
        "\n"
        "EXCLUSIONS: a span does NOT count if any of these applies.\n"
        "(x) The surface text matches but not in the sense the pattern describes — "
        "it is a proper name, a quotation of someone else's words, a fragment of "
        "code, a URL, or a heading label rather than the prose habit being "
        "described.\n"
        "\n"
        "Evidence to extract: the words in the span that instantiate the pattern.\n"
    )


def _adhoc_tell(candidate: Mapping[str, Any], tell_id: str) -> Tell:
    return Tell(
        id=tell_id,
        name=str(candidate.get("name") or "candidate"),
        category=str(candidate.get("category") or "lexical"),
        scope="general",
        method="judge",
        unit="count",
        rubric=adhoc_rubric(candidate),
        rubric_version=ADHOC_RUBRIC_VERSION,
        judge_view="chunk",
        status="candidate",
    )


ADHOC_RULE = protocol.TellRule(
    tell_id="discover.adhoc",
    kind="span",
    mode="all",
    required=("a",),
    exclusions=("x",),
)


def gate_precision(
    candidate: Mapping[str, Any],
    measurement: Measurement,
    docs: Sequence[Doc],
    judge: Any,
    seed: int = PRECISION_SEED,
    sample_size: int = PRECISION_SAMPLE,
) -> GateResult:
    """Adjudicate a seeded sample of this candidate's own matches.

    The matches ARE the extraction — a regex has already proposed the spans — so
    what runs here is the second half of the M6 protocol: verify each quote
    against the document it came from, hand the adjudicator the span with two
    sentences of context, and let `protocol.span_counts` decide from the criteria
    rather than from the judge's own verdict.
    """
    method = str(candidate.get("method") or "")
    if method != "regex":
        why = (
            "judge candidates are not spot-checked here; the rubric faces the full M6 "
            "calibration set (20 hand-labelled snippets, 0.90 gate) before promotion"
            if method == "judge"
            else "a statistic produces no spans to quote, so precision is not defined "
            "for it; its evidence is the effect size at gate 3"
        )
        return GateResult(4, "precision", True, f"skipped: {why}", {"skipped": True})

    pool = sorted(set(measurement.spans))
    if not pool:
        return GateResult(4, "precision", False, "no matches to adjudicate", {})
    rng = random.Random(seed)
    sample = sorted(rng.sample(pool, min(sample_size, len(pool))))

    by_id = {doc.doc_id: doc for doc in docs}
    category = str(candidate.get("category") or "")
    tell_id = f"discover:{slugify(str(candidate.get('name') or 'candidate'))}"
    tell = _adhoc_tell(candidate, tell_id)

    adjudicated: list[dict[str, Any]] = []
    true_count = 0
    for doc_id, quote in sample:
        doc = by_id.get(doc_id)
        if doc is None:  # pragma: no cover - defensive
            continue
        source = source_for(category, doc)
        chunk = protocol.Chunk.make(doc_id, 0, source)
        match = protocol.verify_quote(quote, source)
        if match is None:
            adjudicated.append({"doc_id": doc_id, "quote": quote, "counts": False,
                                "why": "quote did not verify against its own document"})
            continue
        context = protocol.context_for(match, source)
        answer, _, _ = judge.ask(
            cache_mod.ADJUDICATE,
            chunk.sha256,
            tell_id,
            ADHOC_RUBRIC_VERSION,
            protocol.build_adjudication_prompt(tell, match.quote, context),
            quote=match.normalized,
        )
        counts, why_not = protocol.span_counts(ADHOC_RULE, answer)
        true_count += 1 if counts else 0
        adjudicated.append(
            {
                "doc_id": doc_id,
                "quote": match.quote,
                "counts": counts,
                "why": why_not,
                "rationale": str(answer.get("rationale") or "")[:200],
            }
        )

    n = len(adjudicated)
    precision = (true_count / n) if n else 0.0
    needed = math.ceil(PRECISION_MIN * n) if n else 0
    data = {
        "n": n,
        "true": true_count,
        "precision": precision,
        "required": needed,
        "seed": seed,
        "pool_size": len(pool),
        "adjudicated": adjudicated,
    }
    if n and true_count >= needed:
        return GateResult(
            4, "precision", True, f"{true_count}/{n} adjudicated true", data
        )
    return GateResult(
        4,
        "precision",
        False,
        f"{true_count}/{n} adjudicated true, needs {needed}",
        data,
    )


# --- gate 5: dedup -----------------------------------------------------------


def registry_counts(
    registry: Registry, docs: Sequence[Doc], include_candidates: bool = True
) -> tuple[dict[str, dict[str, float]], dict[str, str], dict[str, str]]:
    """Per-document counts, patterns, and names for every measurable active tell.

    Judge tells are excluded from the behavioural half on purpose: measuring one
    costs a judge call per document, and gate 5 is not worth a scoring run. They
    are still compared by name, which is the collision a reader would notice.
    """
    counts: dict[str, dict[str, float]] = {}
    patterns: dict[str, str] = {}
    names: dict[str, str] = {}
    ordered = sorted(docs, key=lambda d: d.doc_id)

    for tell in registry.active_tells(include_candidates=include_candidates):
        names[tell.id] = tell.name
        if tell.method == "regex" and tell.pattern:
            patterns[tell.id] = tell.pattern
            try:
                compiled = tell.compiled()
            except (re.error, TypeError):  # pragma: no cover - registry is validated
                continue
            # Through `finditer_guarded`, so a guarded tell's count here is the
            # count the detector will produce. Comparing a candidate against an
            # unguarded reading of `lex.foster` would compare it to a tell that
            # does not exist.
            counts[tell.id] = {
                doc.doc_id: float(
                    sum(
                        1
                        for _ in finditer_guarded(
                            compiled,
                            source_for(tell.category, doc),
                            tell.proper_noun_guard,
                        )
                    )
                )
                for doc in ordered
            }
        elif tell.method == "statistic" and tell.stat in textstats.STATS:
            fn = textstats.STATS[tell.stat]
            row: dict[str, float] = {}
            for doc in ordered:
                value = float(fn(doc))
                row[doc.doc_id] = 0.0 if math.isnan(value) else value
            counts[tell.id] = row
    return counts, patterns, names


def gate_dedup(
    candidate: Mapping[str, Any],
    measurement: Measurement,
    existing_counts: Mapping[str, Mapping[str, float]],
    existing_patterns: Mapping[str, str],
    existing_names: Mapping[str, str],
) -> tuple[GateResult, dedup_mod.DedupResult]:
    result = dedup_mod.dedup_check(
        candidate,
        measurement.counts,
        existing_patterns,
        existing_counts,
        existing_names,
    )
    if result.is_duplicate:
        return (
            GateResult(5, "dedup", False, result.reason, result.as_dict()),
            result,
        )
    detail = "no pattern or behavioural duplicate in the registry"
    if result.flags:
        detail += f"; flagged for human review: {', '.join(result.flags)}"
    return GateResult(5, "dedup", True, detail, result.as_dict()), result


# --- the pipeline ------------------------------------------------------------


def verify_candidate(
    candidate: Mapping[str, Any],
    docs: Sequence[Doc],
    registry: Registry,
    judge: Any | None = None,
    existing: tuple[dict, dict, dict] | None = None,
    seed: int = PRECISION_SEED,
) -> Verdict:
    """Run one candidate through all five gates, short-circuiting on the first miss."""
    entry = dict(candidate)
    verdict = Verdict(candidate=entry)
    provenance = entry.get("provenance") or {}
    target_model = str(provenance.get("target_model") or "") or None

    gate1, hint = gate_executable(entry, docs)
    verdict.gates.append(gate1)
    if not gate1.passed:
        verdict.status = hint or STATUS_REJECTED
        verdict.reason = gate1.detail
        verdict.evidence = _evidence(entry, None, verdict)
        return verdict

    method = str(entry.get("method") or "")
    measurement = measure(entry, docs)

    if method == "judge":
        # Prevalence and scope both need the candidate run over the corpus, and
        # for a judge candidate that is one model call per document. Deferring is
        # not a shortcut: a judge tell cannot be scored at all until it clears the
        # M6 calibration gate, and prevalence measured before then would be a
        # number produced by an instrument nobody has checked.
        deferred = GateResult(
            2,
            "prevalence",
            True,
            "deferred: measuring a judge candidate costs one call per document; "
            "prevalence is established by the M6 calibration set before promotion",
            {"deferred": True},
        )
        verdict.gates.append(deferred)
        scope = str(entry.get("scope_hypothesis") or "general")
        verdict.gates.append(
            GateResult(
                3,
                "discrimination",
                True,
                f"deferred: scope taken from the lens hypothesis ({scope}) and "
                "re-decided when the tell is calibrated",
                {"deferred": True, "chosen": scope},
            )
        )
    else:
        gate2 = gate_prevalence(measurement)
        verdict.gates.append(gate2)
        if not gate2.passed:
            verdict.status = STATUS_REJECTED
            verdict.reason = gate2.detail
            verdict.evidence = _evidence(entry, measurement, verdict)
            return verdict

        gate3, scope = gate_scope(measurement, target_model)
        verdict.gates.append(gate3)
        if not gate3.passed:
            verdict.status = STATUS_REJECTED
            verdict.reason = gate3.detail
            verdict.evidence = _evidence(entry, measurement, verdict)
            return verdict

    verdict.scope = scope

    if judge is not None:
        gate4 = gate_precision(entry, measurement, docs, judge, seed=seed)
    else:
        gate4 = GateResult(
            4,
            "precision",
            method != "regex",
            "skipped: no judge backend supplied"
            if method != "regex"
            else "no judge backend supplied, and a regex candidate cannot be accepted "
            "without one",
            {"skipped": True},
        )
    verdict.gates.append(gate4)
    if not gate4.passed:
        verdict.status = STATUS_REJECTED
        verdict.reason = gate4.detail
        verdict.evidence = _evidence(entry, measurement, verdict)
        return verdict

    counts, patterns, names = existing or registry_counts(registry, docs)
    gate5, dedup_result = gate_dedup(entry, measurement, counts, patterns, names)
    verdict.gates.append(gate5)
    verdict.flags = list(dedup_result.flags)
    if not gate5.passed:
        verdict.status = STATUS_REJECTED
        verdict.reason = gate5.detail
        verdict.evidence = _evidence(entry, measurement, verdict)
        return verdict

    verdict.status = STATUS_ACCEPTED
    verdict.reason = f"all five gates passed; scope {verdict.scope}"
    verdict.evidence = _evidence(entry, measurement, verdict)
    return verdict


def verify_all(
    candidates: Sequence[Mapping[str, Any]],
    docs: Sequence[Doc],
    registry: Registry,
    judge: Any | None = None,
    seed: int = PRECISION_SEED,
) -> list[Verdict]:
    """Verify every candidate against one corpus and one registry.

    The registry's own per-document counts are computed once and shared: gate 5
    otherwise re-runs 96 regex tells over the whole corpus for every candidate,
    which turns a cheap gate into the most expensive one in the pipeline.
    """
    existing = registry_counts(registry, docs)
    return [
        verify_candidate(candidate, docs, registry, judge, existing=existing, seed=seed)
        for candidate in candidates
    ]


def _evidence(
    candidate: Mapping[str, Any], measurement: Measurement | None, verdict: Verdict
) -> dict[str, Any]:
    provenance = candidate.get("provenance") or {}
    evidence: dict[str, Any] = {
        "lens": provenance.get("lens"),
        "target_model": provenance.get("target_model"),
        "judge_model": provenance.get("judge_model"),
        "prompt_sha": provenance.get("prompt_sha"),
        "discovery_run_id": provenance.get("run_id"),
        "scope_hypothesis": candidate.get("scope_hypothesis"),
        "rationale": candidate.get("rationale"),
        "examples": list(candidate.get("examples") or [])[:5],
        "gates": [g.as_dict() for g in verdict.gates],
    }
    if str(candidate.get("method") or "") == "judge":
        # A judge candidate has no regex to run, so `measure` counts nothing and
        # every model comes back 0/112. Written out as doc_freq that reads as a
        # measured zero — the tell was looked for and never found — which is the
        # opposite of the truth: it was never looked for. Deferred must say
        # deferred.
        evidence["measurement"] = "deferred"
        evidence["reason"] = "judge-method: gates 2-3 deferred to calibration"
    elif measurement is not None:
        evidence["doc_freq"] = measurement.doc_freq()
        evidence["doc_hits"] = {k: list(v) for k, v in measurement.doc_hits().items()}
        evidence["mean_rate_per_1k"] = measurement.mean_rate()
    gate3 = verdict.gate(3)
    if gate3 is not None:
        evidence["scope_z"] = (gate3.data or {}).get("scope_z")
    gate4 = verdict.gate(4)
    if gate4 is not None and not (gate4.data or {}).get("skipped"):
        evidence["precision"] = {
            "n": gate4.data.get("n"),
            "true": gate4.data.get("true"),
            "seed": gate4.data.get("seed"),
        }
    sweep_z = provenance.get("sweep_z")
    if sweep_z is not None:
        evidence["sweep_z"] = sweep_z
    return _clean(evidence)


# --- turning a verdict into a registry entry ---------------------------------

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(name: str, limit: int = 40) -> str:
    """A registry-legal id fragment from a human name."""
    slug = _SLUG_STRIP.sub("-", str(name or "").lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)[:limit].strip("-")
    return slug or "candidate"


def make_tell_id(name: str, category: str, taken: set[str]) -> str:
    """`<prefix>.<slug>`, disambiguated with a numeric suffix if it is taken.

    Lexical tells split between the `lex.` and `phr.` prefixes exactly as the
    seed registry does — one word is a word, several are a phrase — because
    `Registry.validate` checks the prefix against the category and a reader uses
    it to know what kind of thing they are looking at.
    """
    prefix = CATEGORY_PREFIX.get(category, "lex")
    if category == "lexical" and len(str(name or "").split()) > 1:
        prefix = "phr"
    slug = slugify(name)
    base = f"{prefix}.{slug}"
    if base not in taken:
        return base
    for suffix in range(2, 100):
        nudged = f"{prefix}.{slug}-{suffix}"
        if nudged not in taken:
            return nudged
    raise ValueError(f"cannot find a free id for {name!r}")  # pragma: no cover


def _matching_examples(
    candidate: Mapping[str, Any], measurement: Measurement, limit: int = 3
) -> list[str]:
    """Examples that provably match, preferring the model's own quotes.

    `Registry.validate` requires at least one example a regex tell actually
    matches, and a lens quote can fail that honestly — the model quoted the
    sentence around the habit rather than the habit. So the candidate's own
    examples are kept when they match and topped up from real corpus matches
    when they do not, which also means the registry entry carries evidence from
    the corpus rather than from the prompt.
    """
    try:
        pattern = compile_rule(candidate)
    except (re.error, TypeError):  # pragma: no cover - gate 1 caught this
        return [str(e) for e in (candidate.get("examples") or [])][:limit]

    out: list[str] = []
    for example in candidate.get("examples") or []:
        text = " ".join(str(example).split())
        if text and pattern.search(text) and text not in out:
            out.append(text)
        if len(out) >= limit:
            return out

    for _, quote in sorted(set(measurement.spans)):
        text = " ".join(str(quote).split())
        if text and pattern.search(text) and text not in out:
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _statistic_shape(
    measurement: Measurement, scope: str
) -> tuple[str, tuple[float, float]]:
    """A direction and a two-point ramp for a statistic candidate.

    The ramp is written in telling-direction order, as `scoring.ramp_score`
    requires: the human end first, the machine end second. The human end is the
    other models' mean, the machine end the target's 90th percentile — so the
    ramp spans the gap the evidence actually found rather than a round number
    somebody liked.
    """
    target = scope.split(":", 1)[1] if scope.startswith("model:") else None
    models = measurement.models
    focus = target if target in models else (models[0] if models else "")
    mine = sorted(measurement.model_values(focus)) if focus else []
    rest = sorted(v for m in models if m != focus for v in measurement.model_values(m))
    if not mine or not rest:
        return "high_is_telling", (0.0, 1.0)

    mean_rest = sum(rest) / len(rest)
    high = mine[min(len(mine) - 1, int(0.9 * (len(mine) - 1)))]
    low = mine[int(0.1 * (len(mine) - 1))]
    if sum(mine) / len(mine) >= mean_rest:
        lo, hi = mean_rest, high
        if hi <= lo:
            hi = lo + max(abs(lo), 1.0) * 0.1
        return "high_is_telling", (lo, hi)
    lo, hi = mean_rest, low
    if hi >= lo:
        hi = lo - max(abs(lo), 1.0) * 0.1
    return "low_is_telling", (lo, hi)


def to_tell(
    verdict: Verdict,
    run_id: str,
    taken: set[str] | None = None,
    docs: Sequence[Doc] = (),
    added: date | None = None,
) -> Tell:
    """Turn an accepted verdict into a registry entry with `status: candidate`.

    Every number a reader might want to argue with travels with the tell: the
    per-model document frequencies, the scope z, the precision sample, the lens
    that proposed it, and the sweep z where the sweep found it first. A tell
    whose provenance is "discovery" and nothing else is unfalsifiable, which is
    the failure mode this whole milestone exists to avoid.
    """
    candidate = verdict.candidate
    category = str(candidate.get("category") or "lexical")
    method = str(candidate.get("method") or "regex")
    rule = candidate.get("rule") or {}
    measurement = measure(candidate, docs) if docs else Measurement()

    tell_id = make_tell_id(str(candidate.get("name") or ""), category, taken or set())

    common = {
        "id": tell_id,
        "name": str(candidate.get("name") or tell_id),
        "category": category,
        "scope": verdict.scope or "general",
        "formats": None,
        "status": "candidate",
        "weight": 1.0,
        "notes": " ".join(str(candidate.get("rationale") or "").split())[:400] or None,
        "provenance": {
            "source": "discovery",
            "added": added or date.today(),
            "run_id": run_id,
            "evidence": verdict.evidence,
        },
    }

    if method == "regex":
        examples = _matching_examples(candidate, measurement)
        return Tell(
            method="regex",
            unit="count",
            pattern=str(rule.get("pattern") or ""),
            flags=tuple(str(f) for f in (rule.get("flags") or ())),
            examples=tuple(examples),
            counter_examples=(),
            **common,
        )
    if method == "statistic":
        direction, ramp = _statistic_shape(measurement, verdict.scope or "general")
        return Tell(
            method="statistic",
            unit="value",
            stat=str(rule.get("stat_name") or ""),
            direction=direction,
            ramp=ramp,
            examples=tuple(" ".join(str(e).split()) for e in (candidate.get("examples") or ()))[:3],
            **common,
        )
    return Tell(
        method="judge",
        unit="binary" if str(rule.get("judge_view")) == "skeleton" else "count",
        rubric=str(rule.get("rubric") or ""),
        rubric_version=1,
        judge_view=str(rule.get("judge_view") or "chunk"),
        examples=tuple(" ".join(str(e).split()) for e in (candidate.get("examples") or ()))[:3],
        **common,
    )


def rule_fingerprint(
    method: str, pattern: str = "", stat: str = "", rubric: str = ""
) -> str:
    """A normalized identity for one detection rule, for the idempotence check.

    Method-specific because the three methods have nothing comparable in common:
    a regex folds to its normalized pattern, a statistic *is* its function name,
    and a rubric folds to a hash of its whitespace-normalized text.
    """
    if method == "regex":
        return "regex:" + dedup_mod.normalize_pattern(pattern)
    if method == "statistic":
        return "statistic:" + str(stat or "").strip()
    normalized = " ".join(str(rubric or "").split())
    return "judge:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:32]


def tell_fingerprint(tell: Tell) -> str:
    return rule_fingerprint(
        tell.method,
        pattern=tell.pattern or "",
        stat=tell.stat or "",
        rubric=tell.rubric or "",
    )


def _warn(message: str) -> None:
    print(f"telltale.discovery: {message}", file=sys.stderr)


def append_accepted(
    verdicts: Sequence[Verdict],
    registry: Registry,
    run_id: str,
    docs: Sequence[Doc] = (),
) -> list[Tell]:
    """Append every accepted verdict to the registry as a candidate tell.

    Validated before it is written: a discovery run that corrupts the registry
    has destroyed the thing it was extending, and `Registry.append` writes the
    file before anybody looks at it. So the tells are built, checked against a
    throwaway validation pass, and only then committed.

    Idempotent on content, not just on the marker file. `pipeline`'s
    `appended.json` is the fast path, but it is a file on disk and files get
    lost, copied, or bypassed by someone calling this directly — and because
    `make_tell_id` politely disambiguates a taken id, a second append would land
    the same finding again as `phr.bears-emphasis-2` rather than failing. That is
    the worst kind of duplicate: it inflates the category denominator, and it
    looks like a discovery. So a candidate whose (run_id, rule) pair is already
    in the registry is skipped and said aloud.
    """
    seen = {
        (str((t.provenance or {}).get("run_id") or ""), tell_fingerprint(t))
        for t in registry
        if isinstance(t.provenance, dict)
    }
    taken = {t.id for t in registry}
    tells: list[Tell] = []
    for verdict in verdicts:
        if not verdict.accepted:
            continue
        tell = to_tell(verdict, run_id, taken=taken, docs=docs)
        key = (run_id, tell_fingerprint(tell))
        if key in seen:
            _warn(
                f"skipping {tell.name!r}: run {run_id} already contributed this exact "
                f"rule to the registry"
            )
            continue
        seen.add(key)
        taken.add(tell.id)
        tells.append(tell)
    if not tells:
        return []

    problems = _validation_errors(registry, tells)
    if problems:
        raise ValueError(
            "refusing to write invalid tells to the registry: " + "; ".join(problems)
        )
    registry.append(tells)
    return tells


def _validation_errors(registry: Registry, tells: Sequence[Tell]) -> list[str]:
    """Validate candidate tells without touching the registry file."""
    from telltale.registry import Registry as _Registry

    probe = _Registry.__new__(_Registry)
    probe.path = registry.path
    probe._raw = {}
    probe._tells = list(registry.tells) + list(tells)
    known = {t.id for t in registry}
    return [e for e in probe.validate() if not any(e.startswith(k + ":") for k in known)]


__all__ = [
    "ADHOC_RUBRIC_VERSION",
    "GENERAL_MIN_MODELS",
    "MAX_MEDIAN_MS",
    "MAX_TOKEN_SHARE",
    "MIN_DOC_FREQ",
    "MIN_MEAN_RATE",
    "MAX_PROBE_SPANS",
    "PRECISION_MIN",
    "PRECISION_SAMPLE",
    "PRECISION_SEED",
    "SCOPE_RATIO",
    "SCOPE_Z",
    "STATUS_ACCEPTED",
    "STATUS_NEEDS_STAT",
    "STATUS_REJECTED",
    "REGEX_PROBE_BUDGET_S",
    "REGEX_PROBE_STARTUP_S",
    "GateResult",
    "Measurement",
    "ProbeTimeout",
    "Verdict",
    "probe_regex",
    "adhoc_rubric",
    "append_accepted",
    "compile_rule",
    "gate_dedup",
    "gate_executable",
    "gate_precision",
    "gate_prevalence",
    "gate_scope",
    "make_tell_id",
    "measure",
    "registry_counts",
    "rule_fingerprint",
    "slugify",
    "tell_fingerprint",
    "source_for",
    "to_tell",
    "two_proportion_z",
    "verify_all",
    "verify_candidate",
]
