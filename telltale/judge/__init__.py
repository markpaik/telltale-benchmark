"""Tier-2 detection: the evidence-first judge stack.

    from telltale.judge import build_backend
    backend = build_backend(model="claude-opus-4-6")
    detection = backend(tell, doc)

The stack is four layers, and the split between them is the design:

    transport.py   one judge model, isolated, answering JSON
    protocol.py    what it is asked, and the decision rules applied to the answer
    cache.py       answers on disk, keyed by the whole recipe
    calibrate.py   the gate a tell passes before its numbers count

`detectors/judge_detector.py` sits on top and fills M5's `build(tell, judge=...)`
seam. Nothing in this package emits a rating: the judge extracts quotes and
reports which rubric criteria it found, and every number is computed in code
from verified evidence.
"""

from pathlib import Path
from typing import Any

DEFAULT_CACHE_ROOT = Path(__file__).resolve().parents[2] / "cache" / "judge"


def build_backend(
    model: str | None = None,
    cache_root: Path | None = None,
    force: bool = False,
    cache_only: bool = False,
    timeout: int | None = None,
    transport: Any = None,
) -> Any:
    """A ready judge backend: transport + cache + client + aggregation.

    `model` must already be resolved (see `transport.resolve_judge`); this
    function does not probe, so a caller can rebuild the backend a run used
    straight from its manifest without spending a live call to do it.
    """
    from telltale.detectors.judge_detector import JudgeBackend
    from telltale.judge.cache import JudgeCache, JudgeClient
    from telltale.judge.transport import (
        JUDGE_MODEL_DEFAULT,
        JUDGE_TIMEOUT_S,
        CliJudgeTransport,
    )

    name = model or JUDGE_MODEL_DEFAULT
    wire = CliJudgeTransport(
        model=name,
        timeout=timeout if timeout is not None else JUDGE_TIMEOUT_S,
        **({"transport": transport} if transport is not None else {}),
    )
    cache = JudgeCache(Path(cache_root) if cache_root else DEFAULT_CACHE_ROOT)
    client = JudgeClient(transport=wire, cache=cache, force=force, cache_only=cache_only)
    return JudgeBackend(client)


__all__ = ["DEFAULT_CACHE_ROOT", "build_backend"]
