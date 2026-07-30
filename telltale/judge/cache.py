"""Judge answers on disk, keyed by everything that could change them.

A judge call costs money and takes seconds; the same call made twice should not
cost twice. But a cache is only safe if its key covers every input — a stale
answer served under a changed rubric is worse than no cache at all, because it
is invisible. So the key is the whole recipe:

    chunk sha256 | tell id | rubric_version | judge model | protocol version | stage

Bump the rubric in `tells.yaml` and every cached answer for that tell falls out
of reach. Change a prompt and `PROTOCOL_VERSION` moves, and the whole cache does.
Point at a different judge and the answers are separate. Nothing is keyed by
document path or run id, so two runs over the same corpus share their work.

Each entry carries its key fields in cleartext beside the payload. That is
redundant with the key, and deliberately so: a cache directory should be
readable evidence — "this is what claude-opus-4-6 said about this chunk under
rubric v1" — rather than a wall of hashes only the code can interpret.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from telltale.judge.protocol import PROTOCOL_VERSION

EXTRACT = "extract"
ADJUDICATE = "adjudicate"
STRUCTURAL = "structural"
#: M7 discovery lens calls. A lens prompt is not about one chunk of one document
#: and has no rubric to version, so it keys on the sha of the whole prompt with
#: the lens name standing in for the tell id — which is exactly right, because
#: everything that could change the answer (the excerpts, the sweep rows, the
#: existing-tell list) is already in that prompt.
DISCOVER = "discover"


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_key(
    chunk_sha: str,
    tell_id: str,
    rubric_version: Any,
    judge_model: str,
    stage: str,
    quote: str | None = None,
) -> str:
    """The key for one judge call. `quote` is required for adjudication."""
    parts = [
        str(chunk_sha),
        str(tell_id),
        str(rubric_version),
        str(judge_model),
        str(PROTOCOL_VERSION),
    ]
    if stage == ADJUDICATE:
        if quote is None:
            raise ValueError("an adjudication key needs the span quote")
        parts.append(_sha(quote))
    parts.append(stage)
    return _sha("|".join(parts))


@dataclass
class CacheStats:
    """Counters, safe to bump from several sweep workers at once."""

    hits: int = 0
    misses: int = 0
    writes: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def bump(self, field_name: str) -> None:
        with self._lock:
            setattr(self, field_name, getattr(self, field_name) + 1)

    def as_dict(self) -> dict[str, int]:
        with self._lock:
            return {"hits": self.hits, "misses": self.misses, "writes": self.writes}


class JudgeCache:
    """A sharded directory of judge answers: cache/judge/<key[:2]>/<key>.json."""

    def __init__(self, root: Path, transport_name: str = "cli") -> None:
        self.root = Path(root)
        self.transport_name = transport_name
        self.stats = CacheStats()

    def path_for(self, key: str) -> Path:
        return self.root / key[:2] / f"{key}.json"

    def get(self, key: str) -> dict[str, Any] | None:
        path = self.path_for(key)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            self.stats.bump("misses")
            return None
        if not isinstance(data, dict) or "payload" not in data:
            self.stats.bump("misses")
            return None
        self.stats.bump("hits")
        payload = data["payload"]
        return payload if isinstance(payload, dict) else None

    def put(self, key: str, fields: dict[str, Any], payload: dict[str, Any]) -> Path:
        path = self.path_for(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        envelope = {
            "key": key,
            **fields,
            "protocol_version": PROTOCOL_VERSION,
            "transport": self.transport_name,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "payload": payload,
        }
        payload_text = json.dumps(envelope, indent=2, ensure_ascii=False) + "\n"
        # Written through a temp file in the same directory and renamed, because
        # two workers can race the same key and a partially written entry must
        # never be readable as a hit. os.replace is atomic within a filesystem.
        temp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
        temp.write_text(payload_text, encoding="utf-8")
        os.replace(temp, path)
        self.stats.bump("writes")
        return path

    def entries(self) -> list[Path]:
        """Every cached answer, in key order. For the consistency audit."""
        if not self.root.is_dir():
            return []
        return sorted(self.root.glob("*/*.json"))

    def read(self, path: Path) -> dict[str, Any] | None:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            return None
        return data if isinstance(data, dict) else None


class CacheMiss(RuntimeError):
    """Raised when a cache-only client is asked for an answer it does not have."""


@dataclass
class JudgeClient:
    """Cache-first access to the two judge stages.

    Holds no per-document state: the aggregation across chunks lives in
    `detectors/judge_detector.py`, and calibration drives the same primitives
    over snippets. What lives here is exactly the part that must not differ
    between those two callers — the key, the prompt, and the record kept.
    """

    transport: Any
    cache: JudgeCache
    force: bool = False
    cache_only: bool = False
    stats: dict[str, int] = field(default_factory=lambda: {"live_calls": 0})
    #: Called after every live judge call. The sweep uses it to count calls for
    #: the progress line without the cache having to know a sweep exists.
    on_call: Any = None
    _stats_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def model(self) -> str:
        return str(getattr(self.transport, "model", "unknown"))

    def ask(
        self,
        stage: str,
        chunk_sha: str,
        tell_id: str,
        rubric_version: Any,
        prompt: str,
        quote: str | None = None,
    ) -> tuple[dict[str, Any], str, bool]:
        """(payload, key, cached). Cache-first unless `force`."""
        key = cache_key(chunk_sha, tell_id, rubric_version, self.model, stage, quote)
        if not self.force:
            hit = self.cache.get(key)
            if hit is not None:
                return hit, key, True
        elif self.cache_only:  # pragma: no cover - guarded at construction
            raise CacheMiss("force and cache_only cannot both be set")

        if self.cache_only:
            raise CacheMiss(
                f"{stage} for {tell_id} chunk {chunk_sha[:12]} is not cached, and "
                "this client is not allowed to call the judge"
            )

        payload = self.transport.ask(prompt)
        with self._stats_lock:
            self.stats["live_calls"] = self.stats.get("live_calls", 0) + 1
        if self.on_call is not None:
            self.on_call()
        self.cache.put(
            key,
            {
                "stage": stage,
                "tell_id": tell_id,
                "rubric_version": rubric_version,
                "judge_model": self.model,
                "chunk_sha256": chunk_sha,
                "quote_sha256": _sha(quote) if quote is not None else None,
            },
            payload,
        )
        return payload, key, False

    def cache_stats(self) -> dict[str, int]:
        return self.cache.stats.as_dict()


__all__ = [
    "ADJUDICATE",
    "DISCOVER",
    "EXTRACT",
    "STRUCTURAL",
    "CacheMiss",
    "CacheStats",
    "JudgeCache",
    "JudgeClient",
    "cache_key",
]
