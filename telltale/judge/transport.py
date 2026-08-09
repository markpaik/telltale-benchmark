"""Talking to the judge model, under the same isolation the corpus was written under.

Three constraints shape this file, and all three are about keeping the judge
from becoming a participant in the thing it is measuring.

**The judge is never a graded model.** A model asked to count its own tells has
an interest in the answer, and no amount of prompt discipline makes that
finding trustworthy. `assert_judge_model` refuses the three graded ids outright
and refuses anything outside the allowlist, so a typo cannot quietly promote
Opus 5 to referee its own benchmark.

**The judge runs under the generation recipe.** Same flags, same env scrub,
same JSON envelope, same model attribution — see isolation.py for why each of
those exists. Only the pinned system prompt differs, because the judge's job is
not to write a document. Reusing the recipe means a judge call cannot pick up
this machine's house-style skill any more than a generation call can, which
matters: a judge that had read the user's writing-voice skill would be grading
against a rubric it had been told to dislike.

**A judge that answers something other than JSON gets exactly one more try.**
Fence-stripping and one retry cover the two failure modes seen in practice
(a ```json wrapper, and a sentence of preamble). Beyond that the call is an
error rather than a zero — a judge tell that silently returns "no instances"
is indistinguishable from clean prose downstream, and that would understate
every model at once.

The same reasoning, applied to model attribution, is why a reply carrying only
the harness's own side-model usage gets one retry (SHAKEDOWN §2.3) while a reply
naming some other real judge does not. The first means nothing judged the
passage; the second means something did, and that is a fact about the run.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from telltale import isolation

# --- who may judge -----------------------------------------------------------

#: The models this benchmark grades. None of them may ever judge.
GRADED_MODELS: frozenset[str] = frozenset(
    {"claude-opus-5", "claude-fable-5", "claude-sonnet-5"}
)

#: Allowed judges, in the order `resolve_judge` tries them.
JUDGE_MODEL_ORDER: tuple[str, ...] = (
    "claude-opus-4-6",
    "claude-opus-4-7",
    "claude-opus-4-8",
)

JUDGE_ALLOWLIST: frozenset[str] = frozenset(JUDGE_MODEL_ORDER)

JUDGE_MODEL_DEFAULT = "claude-opus-4-6"

#: Replaces isolation.MINIMAL_SYSTEM_PROMPT for judge calls. Pinned, hashed, and
#: recorded in the manifest: a change to this string changes every answer the
#: judge gives, so a run has to be able to say which wording produced it.
JUDGE_SYSTEM_PROMPT = (
    "You are a forensic text analyst. Follow the task exactly and reply with "
    "only valid JSON matching the requested schema."
)

JUDGE_SYSTEM_PROMPT_SHA256 = hashlib.sha256(
    JUDGE_SYSTEM_PROMPT.encode("utf-8")
).hexdigest()

JUDGE_TIMEOUT_S = 300
PROBE_TIMEOUT_S = 120

_FENCE_OPEN = re.compile(r"^\s*```[A-Za-z0-9_-]*\s*\n?")
_FENCE_CLOSE = re.compile(r"\n?\s*```\s*$")

RETRY_SUFFIX = "Reply with ONLY the JSON object, no code fences."


class JudgeError(RuntimeError):
    """A judge call that cannot be turned into evidence."""


class TransientJudgeError(JudgeError):
    """A judge call that failed for a reason that may not be true a minute later.

    The distinction is the whole point. A malformed reply or a genuine model
    mismatch is a fact about this call and recording it is right. A dropped
    connection, or an envelope whose modelUsage is empty because nothing ever
    reached the API, is a fact about the network — and recording fifty of those
    as measurement failures burns the queue during an outage instead of waiting
    it out. That happened, at scale, and this class is the difference.
    """


class ModelSubstitutionError(JudgeError):
    """The harness answered with its own side-model instead of the judge.

    Nine of 175 live calls in the shakedown came back attributed to
    `claude-haiku-4-5` when `claude-opus-4-6` was asked (SHAKEDOWN §2.3), every
    one of them on the longest prompt in the stack, and every one of them cost a
    measurement. That is a different fact from "some other model answered": the
    haiku here is the harness's own small side-call standing alone in
    `modelUsage` because the main call died, so nothing judged anything. It is
    worth one retry. A mismatch naming any other model is not — see `_call`.
    """


#: The models the harness itself calls alongside a request. A reply attributed
#: only to one of these is the substitution signature, not a second opinion.
_HARNESS_SIDE_MODEL = re.compile(r"haiku", re.IGNORECASE)


def is_harness_side_model(name: str) -> bool:
    """Whether a modelUsage key names one of the harness's own side-models."""
    return bool(_HARNESS_SIDE_MODEL.search(str(name or "")))


def is_substitution(model_usage: dict[str, Any]) -> bool:
    """Whether a mismatched envelope carries only harness side-model usage."""
    names = list(model_usage or {})
    return bool(names) and all(is_harness_side_model(name) for name in names)


#: Failures that say "the network is down", not "this call was bad".
_TRANSIENT = re.compile(
    r"connection (closed|reset|refused|error)|econnreset|broken pipe|"
    r"timed out|timeout|network is (down|unreachable)|temporary failure|"
    r"name resolution|dns|socket|unexpected eof|stream (closed|ended)",
    re.IGNORECASE,
)


def is_transient(message: str) -> bool:
    """Whether a failure message describes the network rather than the call."""
    return bool(_TRANSIENT.search(str(message or "")))


def assert_judge_model(model: str) -> str:
    """Refuse any model that must not judge. Returns the model on success."""
    name = str(model or "")
    if name in GRADED_MODELS or any(g in name for g in GRADED_MODELS):
        raise JudgeError(
            f"{name!r} is a graded model; a graded model may never judge "
            f"(graded set: {sorted(GRADED_MODELS)})"
        )
    if name not in JUDGE_ALLOWLIST:
        raise JudgeError(
            f"{name!r} is not on the judge allowlist {sorted(JUDGE_ALLOWLIST)}"
        )
    return name


# --- the recipe --------------------------------------------------------------


def judge_flags() -> list[str]:
    """isolation.ISOLATION_FLAGS with the judge's system prompt swapped in."""
    flags = list(isolation.ISOLATION_FLAGS)
    index = flags.index("--system-prompt")
    flags[index + 1] = JUDGE_SYSTEM_PROMPT
    return flags


def build_judge_cmd(model: str, extra: list[str] | None = None) -> list[str]:
    """The full argv for one judge call."""
    return [isolation.CLAUDE_BIN, *judge_flags(), "--model", model, *(extra or [])]


def strip_fences(text: str) -> str:
    """Remove one markdown code fence wrapper, if the reply is wearing one."""
    stripped = (text or "").strip()
    if not stripped.startswith("```"):
        return stripped
    stripped = _FENCE_OPEN.sub("", stripped, count=1)
    stripped = _FENCE_CLOSE.sub("", stripped, count=1)
    return stripped.strip()


def _first_json_object(text: str) -> str:
    """The outermost {...} span, for a reply with prose either side of it."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        return text
    return text[start : end + 1]


def parse_json_reply(text: str) -> dict[str, Any]:
    """Parse a judge reply into an object, tolerating fences and stray prose."""
    candidate = strip_fences(text)
    for attempt in (candidate, _first_json_object(candidate)):
        try:
            data = json.loads(attempt)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(data, dict):
            return data
        raise JudgeError(f"judge reply is a {type(data).__name__}, expected an object")
    raise JudgeError(f"judge reply is not JSON: {candidate[:200]!r}")


# --- transport ---------------------------------------------------------------


@dataclass
class TransportStats:
    """What a run's judge traffic actually cost, in calls rather than dollars.

    Mutated from every sweep worker, so the counters take a lock. They are only
    ever read for the manifest, but a torn count there would be a number nobody
    could reproduce.
    """

    calls: int = 0
    retries: int = 0
    transient_retries: int = 0
    failures: int = 0
    seconds: float = 0.0
    #: The substitution ledger (SHAKEDOWN §2.3, recommendation 2). Detected
    #: counts every envelope carrying only side-model usage; retried, recovered
    #: and failed say what the one retry bought. A run that recovers ten
    #: substitutions and a run that never saw one both report zero failures, and
    #: only these numbers tell them apart.
    substitutions_detected: int = 0
    substitution_retries: int = 0
    substitutions_recovered: int = 0
    substitutions_failed: int = 0
    #: Replies that never parsed as JSON, by the stage that asked
    #: (SHAKEDOWN §2.4, recommendation 3). The exposure is real and the observed
    #: rate is zero, which is exactly the pair of facts a counter turns into a
    #: number: adjudication rationales quote business prose back at the parser,
    #: and a mis-escaped quotation mark fails a whole measurement silently. The
    #: split by stage is the point — one shared total could not tell "the
    #: adjudicator is quoting badly" from "the extractor is wrapping fences".
    parse_failures: dict[str, int] = field(default_factory=dict)
    _lock: "threading.Lock" = field(default_factory=lambda: threading.Lock(), repr=False)

    def bump(self, field_name: str, amount: float = 1) -> None:
        with self._lock:
            setattr(self, field_name, getattr(self, field_name) + amount)

    def bump_parse_failure(self, stage: str | None) -> None:
        """Record one unparseable reply against the stage that asked for it."""
        name = str(stage or "unknown")
        with self._lock:
            self.parse_failures[name] = self.parse_failures.get(name, 0) + 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "retries": self.retries,
            "transient_retries": self.transient_retries,
            "failures": self.failures,
            "seconds": round(self.seconds, 2),
            "substitutions_detected": self.substitutions_detected,
            "substitution_retries": self.substitution_retries,
            "substitutions_recovered": self.substitutions_recovered,
            "substitutions_failed": self.substitutions_failed,
            "parse_failures": dict(sorted(self.parse_failures.items())),
            "parse_failures_total": sum(self.parse_failures.values()),
        }


@dataclass
class CliJudgeTransport:
    """One judge model, reached through the isolated CLI, answering JSON."""

    model: str
    timeout: int = JUDGE_TIMEOUT_S
    transport: isolation.Transport = isolation.run_cli
    stats: TransportStats = field(default_factory=TransportStats)
    #: Pause before the one transient retry. Injectable so tests need no clock.
    retry_delay_s: float = 30.0
    sleep: Any = time.sleep

    def __post_init__(self) -> None:
        assert_judge_model(self.model)

    name = "cli"

    #: Tells a caller this transport records which stage a call served. A
    #: transport without it is asked the plain question, so a stub in a test or
    #: a lens transport in discovery needs no signature change.
    accepts_stage = True

    def ask(self, prompt: str, stage: str | None = None) -> dict[str, Any]:
        """Send one prompt, return the parsed JSON object.

        Three independent retries, for three different kinds of wrong, each with
        a budget of one. A reply that is not JSON gets one more try immediately,
        because the model can be asked again to drop its code fences. A call that
        never reached the API gets one more try after a pause, because a blip
        should not cost a measurement. And a call the harness answered with its
        own side-model gets one more try with no pause — nothing judged anything,
        so there is nothing to wait out, and the shakedown's nine substitutions
        would all have been recovered by exactly this (SHAKEDOWN §2.3).

        A mismatch that names any other model is still immediately fatal. Some
        model really did answer there, and retrying would either reach the same
        wrong judge again or, worse, quietly succeed and put an unaudited judge
        behind a number.
        """
        transient_left = 1
        substitution_left = 1
        substituted = False
        while True:
            try:
                answer = self._ask_parsed(prompt, stage)
            except ModelSubstitutionError:
                if not substitution_left:
                    self.stats.bump("substitutions_failed")
                    self.stats.bump("failures")
                    raise
                substitution_left -= 1
                substituted = True
                self.stats.bump("substitution_retries")
                continue
            except TransientJudgeError:
                if not transient_left:
                    raise
                transient_left -= 1
                self.stats.bump("transient_retries")
                self.sleep(self.retry_delay_s)
                continue
            if substituted:
                self.stats.bump("substitutions_recovered")
            return answer

    def _ask_parsed(self, prompt: str, stage: str | None = None) -> dict[str, Any]:
        """One call, with the JSON-parse retry."""
        payload = prompt
        for attempt in (0, 1):
            text = self._call(payload)
            try:
                return parse_json_reply(text)
            except JudgeError:
                if attempt == 1:
                    self.stats.bump("failures")
                    self.stats.bump_parse_failure(stage)
                    raise
                self.stats.bump("retries")
                payload = f"{prompt}\n\n{RETRY_SUFFIX}"
        raise AssertionError("unreachable")  # pragma: no cover

    def _call(self, prompt: str) -> str:
        cmd = build_judge_cmd(self.model)
        result = self.transport(cmd, prompt, self.timeout)
        self.stats.bump("calls")
        self.stats.bump("seconds", float(result.duration_s or 0.0))
        envelope = isolation.parse_envelope(result.stdout, requested_model=self.model)
        if envelope.model_mismatch:
            if is_substitution(envelope.model_usage):
                # The harness's own side-model, alone in modelUsage: the main
                # call died and nothing judged the passage. Retryable once, and
                # counted whether or not the retry works, so the substitution
                # rate stays visible in the manifest instead of disappearing
                # into a successful run.
                self.stats.bump("substitutions_detected")
                raise ModelSubstitutionError(
                    f"model substitution: asked for {self.model}, only harness "
                    f"side-model usage {sorted(envelope.model_usage)}"
                )
            self.stats.bump("failures")
            if not envelope.model_usage:
                # Nothing was billed to any model, so nothing reached the API.
                # That is the network, not a substituted judge, and it is the
                # signature an outage writes into every call at once.
                raise TransientJudgeError(
                    f"empty modelUsage for {self.model}: no model was reached "
                    f"(exit {result.returncode}) {result.stderr[:120]}"
                )
            raise JudgeError(
                f"model mismatch: asked for {self.model}, modelUsage has "
                f"{sorted(envelope.model_usage)}"
            )
        if not envelope.ok:
            self.stats.bump("failures")
            detail = envelope.parse_error or (envelope.result or "")[:200]
            message = (
                f"judge call failed (exit {result.returncode}): "
                f"{detail or result.stderr[:200]}"
            )
            if result.timed_out or is_transient(message) or is_transient(result.stderr):
                raise TransientJudgeError(message)
            raise JudgeError(message)
        return envelope.result


# --- availability ------------------------------------------------------------

PROBE_PROMPT = (
    'Reply with exactly this JSON object and nothing else: {"ok": true}'
)


def probe_judge(
    model: str,
    transport: isolation.Transport = isolation.run_cli,
    timeout: int = PROBE_TIMEOUT_S,
) -> bool:
    """Cheap liveness check: does this model answer, as itself, in JSON?

    Checks the envelope and the model attribution as well as the JSON, because
    "available" has to mean "answers as the model we asked for". A silent
    fallback to another model would put an unaudited judge behind every number.
    """
    try:
        assert_judge_model(model)
    except JudgeError:
        return False
    # No pause before the transient retry: a probe *is* the retry. The breaker
    # calls this on its own schedule and reads False as "not yet", so a thirty
    # second sleep in here would only make the sweep slower to notice the
    # network came back.
    client = CliJudgeTransport(
        model=model, timeout=timeout, transport=transport, retry_delay_s=0.0
    )
    try:
        data = client.ask(PROBE_PROMPT)
    except JudgeError:
        return False
    return bool(data.get("ok"))


def resolve_judge(
    preferred: str | None = None,
    transport: isolation.Transport = isolation.run_cli,
    timeout: int = PROBE_TIMEOUT_S,
) -> str:
    """The first allowlisted judge that answers, preferred model first.

    Called once per run and recorded in the manifest: which model judged is part
    of what a judge number means, and a fallback that is not written down is a
    silent change of instrument.
    """
    order: list[str] = []
    if preferred:
        assert_judge_model(preferred)
        order.append(preferred)
    order += [m for m in JUDGE_MODEL_ORDER if m not in order]

    tried: list[str] = []
    for model in order:
        tried.append(model)
        if probe_judge(model, transport=transport, timeout=timeout):
            return model
    raise JudgeError(f"no judge model answered; tried {tried}")


__all__ = [
    "GRADED_MODELS",
    "JUDGE_ALLOWLIST",
    "JUDGE_MODEL_DEFAULT",
    "JUDGE_MODEL_ORDER",
    "JUDGE_SYSTEM_PROMPT",
    "JUDGE_SYSTEM_PROMPT_SHA256",
    "CliJudgeTransport",
    "JudgeError",
    "ModelSubstitutionError",
    "TransportStats",
    "assert_judge_model",
    "build_judge_cmd",
    "is_harness_side_model",
    "is_substitution",
    "judge_flags",
    "parse_json_reply",
    "probe_judge",
    "resolve_judge",
    "strip_fences",
]
