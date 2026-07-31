"""Running a corpus-scale judge sweep without melting anything.

The sweep is ~6,000 subprocess calls at ~30 seconds each. Sequentially that is
two days, which is not a shakedown, it is a hostage situation. The calls are
independent per (tell, document), so the fix is a thread pool — the GIL is
irrelevant here because every worker spends its life blocked on
`subprocess.communicate`.

What needs care is not the parallelism, it is the manners. Three policies:

**A ceiling, not a maximum.** This machine also runs the discovery executor and
its owner's own interactive sessions. The pool holds at six deliberately, with
room left over, rather than taking everything the API will give.

**Backpressure that believes the server.** A 429 is not a hiccup to retry
through, it is the service saying the request rate is wrong; the pool halves on
the first one. Overload (529) is noisier, so it halves only when it exceeds a
small share of a rolling window. Recovery is one worker at a time after a quiet
period, because stepping straight back to the old number is how you get the
next 429.

**Auth failure stops everything.** A sweep that keeps 5,000 calls of momentum
after the token dies just writes 5,000 failures into the manifest. Stopping is
free to recover from: the cache is content-addressed, so relaunching the same
command resumes exactly where it left off.
"""

from __future__ import annotations

import re
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Deque

#: A judge call that failed because the service is refusing the rate.
_THROTTLE = re.compile(
    r"\b429\b|rate.?limit|too many requests|quota exceeded", re.IGNORECASE
)
#: A judge call that failed because the service is over capacity.
_OVERLOAD = re.compile(r"\b529\b|overloaded|capacity|\b503\b", re.IGNORECASE)
#: A judge call that failed because this machine can no longer authenticate.
_AUTH = re.compile(
    r"not logged in|\b401\b|\b403\b|unauthor|authentication|invalid api key|"
    r"oauth|credential|please run /login",
    re.IGNORECASE,
)

OK = "ok"
THROTTLE = "throttle"
OVERLOAD = "overload"
AUTH = "auth"
OTHER = "other"


def classify_failure(message: str) -> str:
    """What kind of failure a judge error message describes.

    Auth is checked first: an expired token often surfaces alongside other
    noise, and reading it as a generic failure would keep the sweep running
    against a machine that can no longer call anything.
    """
    text = str(message or "")
    if _AUTH.search(text):
        return AUTH
    if _THROTTLE.search(text):
        return THROTTLE
    if _OVERLOAD.search(text):
        return OVERLOAD
    return OTHER


class Gate:
    """A semaphore whose capacity can move while workers are using it."""

    def __init__(self, capacity: int, ceiling: int) -> None:
        self._cv = threading.Condition()
        self._ceiling = max(1, int(ceiling))
        self._capacity = max(1, min(int(capacity), self._ceiling))
        self._in_flight = 0

    @property
    def capacity(self) -> int:
        with self._cv:
            return self._capacity

    @property
    def in_flight(self) -> int:
        with self._cv:
            return self._in_flight

    def set_capacity(self, value: int) -> int:
        """Move the ceiling on concurrent work. Returns the capacity now in force.

        Reducing does not interrupt work already in flight; it just stops more
        starting until the number drops. Nothing is killed mid-call, because a
        killed call is a wasted 30 seconds and a cache entry that never lands.
        """
        with self._cv:
            self._capacity = max(1, min(int(value), self._ceiling))
            self._cv.notify_all()
            return self._capacity

    def acquire(self) -> None:
        with self._cv:
            while self._in_flight >= self._capacity:
                self._cv.wait()
            self._in_flight += 1

    def release(self) -> None:
        with self._cv:
            self._in_flight -= 1
            self._cv.notify()

    def __enter__(self) -> "Gate":
        self.acquire()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.release()


@dataclass
class SweepPolicy:
    """The knobs, with the values this benchmark's operator settled on."""

    workers: int = 4
    ceiling: int = 6
    #: Quiet time before adding one worker back.
    step_up_after_s: float = 1800.0
    #: Rolling window for the overload-rate test.
    window_s: float = 600.0
    #: Share of calls in the window that may be overloads before halving.
    overload_rate: float = 0.02
    #: How often the global progress line is emitted.
    progress_every_s: float = 600.0
    #: Overloads below this count never trip the rate test, however few calls
    #: have been made — one 529 out of three calls is not a trend.
    min_overloads: int = 3
    #: Consecutive failures across all workers before the pool stops dead.
    breaker_after: int = 8
    #: How often a paused sweep probes for the network coming back.
    probe_every_s: float = 60.0
    #: How long a paused sweep waits before giving up and halting cleanly.
    breaker_timeout_s: float = 1800.0


@dataclass
class SweepController:
    """Concurrency, backpressure, and the progress cadence for one sweep."""

    policy: SweepPolicy = field(default_factory=SweepPolicy)
    total: int = 0
    emit: Callable[[str], None] = lambda line: None
    clock: Callable[[], float] = time.monotonic
    #: A cheap live call that answers True when the judge is reachable again.
    probe: Callable[[], bool] | None = None
    sleep: Callable[[float], None] = time.sleep

    def __post_init__(self) -> None:
        self.gate = Gate(self.policy.workers, self.policy.ceiling)
        self._lock = threading.Lock()
        self._cv = threading.Condition()
        self._events: Deque[tuple[float, str]] = deque()
        self._done = 0
        self._calls = 0
        self._started = self.clock()
        self._last_progress = self._started
        self._last_incident = self._started
        self._consecutive = 0
        self._breaker_open = False
        self._breaker_since = 0.0
        self.breaker_trips = 0
        self.stop_reason: str | None = None

    # -- outcomes --

    def record_call(self) -> None:
        with self._lock:
            self._calls += 1

    def record_ok(self) -> None:
        self._note(OK)
        with self._lock:
            self._consecutive = 0

    def record_failure(self, message: str) -> str:
        """Classify a failure, apply the policy, and return the classification."""
        kind = classify_failure(message)
        self._note(kind)

        # The cascade check comes first and is deliberately blind to the kind of
        # failure. What distinguishes an outage from bad data is not what any
        # one call said, it is that every call is saying it: eight in a row
        # across four workers is not eight bad documents.
        with self._lock:
            self._consecutive += 1
            tripped = self._consecutive >= self.policy.breaker_after
        if tripped:
            self.open_breaker(f"{self._consecutive} consecutive failures")
        if kind == AUTH:
            with self._lock:
                if self.stop_reason is None:
                    self.stop_reason = "auth"
                    self.emit(f"AUTH-LOST {str(message)[:200]}")
            return kind
        if kind == THROTTLE:
            self._halve("429")
        elif kind == OVERLOAD and self._overloaded():
            self._halve("529 rate")
        return kind

    def _note(self, kind: str) -> None:
        now = self.clock()
        with self._lock:
            self._events.append((now, kind))
            cutoff = now - self.policy.window_s
            while self._events and self._events[0][0] < cutoff:
                self._events.popleft()
            if kind in (THROTTLE, OVERLOAD, AUTH):
                self._last_incident = now

    def _overloaded(self) -> bool:
        with self._lock:
            if not self._events:
                return False
            overloads = sum(1 for _, kind in self._events if kind == OVERLOAD)
            if overloads < self.policy.min_overloads:
                return False
            return overloads / len(self._events) > self.policy.overload_rate

    def _halve(self, why: str) -> None:
        current = self.gate.capacity
        if current <= 1:
            return
        now = self.gate.set_capacity(max(1, current // 2))
        if now != current:
            self.emit(f"THROTTLE {now} (was {current}, {why})")

    # -- the cascade breaker --

    def open_breaker(self, why: str) -> None:
        """Stop the pool taking new work and start probing for recovery.

        Workers already inside a call finish it; nobody starts another. The
        alternative — which is what happened — is that the queue keeps feeding
        work into a dead network and every measurement in it is recorded as a
        failure. Fifty measurements burned in seventeen minutes, none of them
        because of anything in the documents.
        """
        with self._cv:
            if self._breaker_open or self.stop_reason is not None:
                return
            self._breaker_open = True
            self._breaker_since = self.clock()
            self.breaker_trips += 1
            self._cv.notify_all()
        self.emit(f"BREAKER-OPEN {why}; pausing, probing every {self.policy.probe_every_s:.0f}s")
        threading.Thread(target=self._probe_until_recovered, daemon=True).start()

    def _probe_until_recovered(self) -> None:
        while True:
            self.sleep(self.policy.probe_every_s)
            with self._cv:
                if self.stop_reason is not None or not self._breaker_open:
                    return
                open_for = self.clock() - self._breaker_since
            if open_for >= self.policy.breaker_timeout_s:
                with self._cv:
                    self.stop_reason = "outage"
                    self._breaker_open = False
                    self._cv.notify_all()
                self.emit(
                    f"SWEEP-HALTED (outage) after {open_for / 60:.0f}m; "
                    "cache is intact, the same command resumes"
                )
                return
            try:
                recovered = bool(self.probe()) if self.probe is not None else False
            except Exception:  # noqa: BLE001 - a failing probe is just "not yet"
                recovered = False
            if recovered:
                # The count belongs to `_lock` everywhere else; take it here
                # too, and never while holding `_cv`, so the two locks stay in
                # a fixed order and cannot close on each other.
                with self._lock:
                    self._consecutive = 0
                with self._cv:
                    self._breaker_open = False
                    self._cv.notify_all()
                self.emit(f"BREAKER-CLOSED after {open_for / 60:.1f}m; resuming")
                return

    def await_ready(self) -> bool:
        """Block while the breaker is open. False means stop working."""
        with self._cv:
            while self._breaker_open and self.stop_reason is None:
                self._cv.wait(timeout=0.5)
            return self.stop_reason is None

    @property
    def breaker_open(self) -> bool:
        with self._cv:
            return self._breaker_open

    # -- recovery --

    def maybe_step_up(self) -> None:
        """Add one worker back after a quiet stretch, up to the ceiling."""
        with self._lock:
            quiet_for = self.clock() - self._last_incident
            current = self.gate.capacity
            if quiet_for < self.policy.step_up_after_s or current >= self.policy.ceiling:
                return
            self._last_incident = self.clock()
        raised = self.gate.set_capacity(current + 1)
        if raised != current:
            self.emit(f"WORKERS {raised} (stable for {quiet_for / 60:.0f}m)")

    # -- progress --

    def note_done(self) -> None:
        with self._lock:
            self._done += 1
        self.maybe_step_up()
        self.tick()

    def tick(self, force: bool = False) -> None:
        now = self.clock()
        with self._lock:
            if not force and now - self._last_progress < self.policy.progress_every_s:
                return
            self._last_progress = now
            done, calls, total = self._done, self._calls, self.total
            elapsed = max(1e-9, now - self._started)
        rate = calls / (elapsed / 60.0)
        remaining = max(0, total - done)
        eta_h = (remaining / (done / (elapsed / 3600.0))) if done else float("nan")
        self.emit(
            f"SWEEP {done}/{total} measurements, {calls} calls, "
            f"{rate:.1f} calls/min, workers {self.gate.capacity}, "
            + (f"ETA {eta_h:.1f}h" if eta_h == eta_h else "ETA -")
        )

    @property
    def should_stop(self) -> bool:
        return self.stop_reason is not None


__all__ = [
    "AUTH",
    "OK",
    "OTHER",
    "OVERLOAD",
    "THROTTLE",
    "Gate",
    "SweepController",
    "SweepPolicy",
    "classify_failure",
]
