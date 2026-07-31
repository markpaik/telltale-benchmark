"""From detections to a comparable number, with the uncertainty attached.

The pipeline is four steps, each a pure function of the step before it:

    detect_all   docs x tells            -> long DataFrame of raw measurements
    normalize    raw                     -> score in [0, 1], per row
    per_model_*  scores                  -> S(m, t), mean doc score
    indices      S(m, t) + weights       -> C(m, c) and the AI-Tell Index

Three decisions are worth stating up front, because they are the ones that
decide what the headline number means.

**Pooled winsorization.** A count tell's score is its rate divided by the
pooled 95th-percentile rate — pooled across *all* models, once, not per model.
Per-model normalization would rescale every model onto its own worst document
and make everyone look identical; that is the failure mode this benchmark
exists to avoid. Winsorizing at p95 rather than the max stops one runaway
document (a listicle that is 90% bullets) from compressing everyone else into
the bottom of the range.

**NaN is not zero.** A statistic that could not be computed (a six-sentence
email has no meaningful burstiness) yields NaN, and NaN rows are dropped from
means rather than counted as clean. Reading them as zero would reward short
documents, which is the opposite of what the tell measures.

**Dormant tells stay in the denominator.** A tell that fires nowhere in this
corpus scores 0 for everybody. It is tempting to drop it — it adds no
discrimination — but dropping it makes the index denominator depend on what
happened to fire, so adding one document to the corpus could move every
model's score. A fixed denominator from the registry is what makes two runs
comparable; the scorecard lists the dormant tells so the dilution is visible.
"""

from __future__ import annotations

import math
import threading
import warnings
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
import pandas as pd

from telltale.corpus import Doc
from telltale.detectors import build
from telltale.registry import Tell

# Category weights for the AI-Tell Index. They sum to 1.0 and are a judgement
# call, not a fit: lexical tells carry the most weight because word choice is
# what a reader notices first and what survives editing; punctuation the least
# because an em dash is one keystroke away from being fixed.
CATEGORY_WEIGHTS: dict[str, float] = {
    "lexical": 0.30,
    "punctuation": 0.10,
    "syntactic": 0.25,
    "structural": 0.20,
    "statistical": 0.15,
}

# Evidence floors below which a model x format x tell cell is not reported as a
# finding. Eight documents is the smallest cell where a single outlier cannot
# move the cell mean by more than an eighth; ten expected occurrences is the
# usual floor for treating a count as anything but noise.
MIN_DOCS = 8
MIN_OCCURRENCES = 10

WINSOR_PERCENTILE = 95.0
Z_95 = 1.959963984540054

DETECTION_COLUMNS = (
    "doc_id",
    "model",
    "format",
    "words",
    "tell_id",
    "name",
    "category",
    "scope",
    "status",
    "weight",
    "method",
    "unit",
    "raw",
    "rate_per_1k",
    "matches",
    "detail",
)


# --- tell metadata -----------------------------------------------------------

META_FIELDS = (
    "name",
    "category",
    "scope",
    "status",
    "weight",
    "method",
    "unit",
    "direction",
    "ramp",
)


def tell_meta(tells: Iterable[Tell] | Mapping[str, Mapping[str, Any]]) -> dict[str, dict]:
    """Normalize registry entries to the plain dict the scoring functions need.

    Accepts `Tell` objects or the equivalent mapping recovered from a run
    manifest, so a scorecard can be re-rendered from a run directory alone
    without the registry file being present or unchanged.
    """
    if isinstance(tells, Mapping):
        out = {}
        for tell_id, meta in tells.items():
            row = {field: meta.get(field) for field in META_FIELDS}
            row["weight"] = float(row["weight"] if row["weight"] is not None else 1.0)
            out[str(tell_id)] = row
        return out
    return {
        t.id: {
            "name": t.name,
            "category": t.category,
            "scope": t.scope,
            "status": t.status,
            "weight": float(t.weight),
            "method": t.method,
            "unit": t.unit,
            "direction": t.direction,
            "ramp": list(t.ramp) if t.ramp is not None else None,
        }
        for t in tells
    }


def judge_tell_ids(tells: Iterable[Tell]) -> list[str]:
    """The tells a Tier-1 run cannot score, in id order."""
    return sorted(t.id for t in tells if t.method == "judge")


# --- detection ---------------------------------------------------------------


def detect_all(
    docs: Sequence[Doc],
    tells: Sequence[Tell],
    judge: Any | None = None,
    progress: Any | None = None,
    workers: int = 1,
    controller: Any | None = None,
    judge_docs: Any | None = None,
) -> pd.DataFrame:
    """Run every applicable tell over every document.

    One row per (document, applicable tell). A tell scoped to formats it does
    not cover produces no row at all for the documents it does not cover — a
    sign-off tell is not a zero on a white paper, it is a question that was not
    asked, and zeroing it would drag that model's mean down for writing the
    format it was asked to write.

    Judge tells are skipped unless a judge backend is supplied; the count lands
    in `df.attrs["judge_tells_skipped"]` and in the manifest.

    `progress` is called with one status line per completed judge measurement.
    It exists because a corpus-scale judge sweep is thousands of subprocess
    calls over hours, and a run that prints nothing until it finishes is a run
    nobody can tell apart from a hung one.

    A judge measurement that raises is recorded and skipped rather than taking
    the sweep down with it. The failure is not silent — it lands in
    `df.attrs["judge_errors"]` and in the manifest — but three hours of paid
    work should not be lost to one call that timed out. The row is simply
    absent, which reads downstream as "not measured", never as a clean zero.
    """
    ordered_docs = sorted(docs, key=lambda d: d.doc_id)
    ordered_tells = sorted(tells, key=lambda t: t.id)

    skipped: list[str] = []
    detectors = []
    for tell in ordered_tells:
        if tell.method == "judge" and judge is None:
            skipped.append(tell.id)
            continue
        detectors.append((tell, build(tell, judge=judge)))

    # A missing cache entry is not a flaky call, it is a missing input, and a
    # replay that quietly scored 223 of 224 documents would be worse than one
    # that stopped. Everything else about a judge call is recoverable.
    fatal: tuple[type[BaseException], ...] = ()
    if judge is not None:
        from telltale.judge.cache import CacheMiss

        fatal = (CacheMiss,)

    # Tier-1 always reads the whole corpus; Tier-2 may be restricted to a
    # sample, because a judge tell costs a dozen subprocess calls per document
    # and a regex costs microseconds. `judge_docs` is None for a full sweep.
    judged = set(judge_docs) if judge_docs is not None else None

    def judge_applies(detector: Any, doc: Doc) -> bool:
        if not detector.applies_to(doc):
            return False
        return judged is None or doc.doc_id in judged

    totals = {
        tell.id: sum(1 for d in ordered_docs if judge_applies(detector, d))
        for tell, detector in detectors
        if tell.method == "judge"
    }
    done: dict[str, int] = {tell_id: 0 for tell_id in totals}
    errors: list[dict[str, str]] = []

    rows: list[dict] = []
    lock = threading.Lock()

    def row_for(tell: Tell, detection: Any, doc: Doc) -> dict:
        return {
            "doc_id": doc.doc_id,
            "model": doc.model,
            "format": doc.fmt,
            "words": doc.words,
            "tell_id": tell.id,
            "name": tell.name,
            "category": tell.category,
            "scope": tell.scope,
            "status": tell.status,
            "weight": float(tell.weight),
            "method": detection.method,
            "unit": detection.unit,
            "raw": detection.raw,
            "rate_per_1k": detection.rate_per_1k,
            "matches": detection.matches,
            "detail": detection.detail,
        }

    def measure(tell: Tell, detector: Any, doc: Doc) -> None:
        """One (tell, document) measurement, safe to run from a sweep worker."""
        # Waits out an open breaker rather than feeding the queue into a dead
        # network. Returns False once the sweep has stopped for good.
        if controller is not None and not controller.await_ready():
            return
        gate = controller.gate if controller is not None else None
        if gate is not None:
            gate.acquire()
        try:
            detection = detector.detect(doc)
        except fatal:
            raise
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            note = f"{type(exc).__name__}: {exc}"
            with lock:
                errors.append({"tell_id": tell.id, "doc_id": doc.doc_id, "error": note[:300]})
            kind = controller.record_failure(note) if controller is not None else "other"
            if progress is not None:
                progress(f"ERROR[{kind}] {tell.id} {doc.doc_id}: {note}"[:300])
            return
        finally:
            if gate is not None:
                gate.release()

        with lock:
            rows.append(row_for(tell, detection, doc))
            done[tell.id] += 1
            count = done[tell.id]
        if controller is not None:
            controller.record_ok()
            controller.note_done()
        if progress is not None:
            progress(f"JUDGE {tell.id} {count}/{totals[tell.id]} docs")

    # Deterministic tells first and inline: they are microseconds of pure CPU,
    # and handing them to a thread pool would only add contention.
    for doc in ordered_docs:
        for tell, detector in detectors:
            if tell.method != "judge" and detector.applies_to(doc):
                rows.append(row_for(tell, detector.detect(doc), doc))

    # Work ordered (tell, doc) so a cache-warm resume walks contiguous ground
    # rather than skipping about, which keeps the progress line legible.
    work = [
        (tell, detector, doc)
        for tell, detector in detectors
        if tell.method == "judge"
        for doc in ordered_docs
        if judge_applies(detector, doc)
    ]
    if work:
        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(lambda item: measure(*item), work))
        else:
            for item in work:
                measure(*item)
        if controller is not None:
            controller.tick(force=True)

    # Sorted so the frame does not depend on how many workers produced it. The
    # writers sort too, but a frame whose row order varied with concurrency
    # would make every downstream byte-comparison a coin toss.
    rows.sort(key=lambda r: (r["doc_id"], r["tell_id"]))

    df = pd.DataFrame(rows, columns=list(DETECTION_COLUMNS))
    df["raw"] = pd.to_numeric(df["raw"], errors="coerce")
    df["rate_per_1k"] = pd.to_numeric(df["rate_per_1k"], errors="coerce")
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df.attrs["judge_tells_skipped"] = len(skipped)
    df.attrs["judge_tell_ids"] = skipped
    df.attrs["judge_errors"] = errors
    return df


# --- normalization -----------------------------------------------------------


def ramp_score(value: float, direction: str, ramp: Sequence[float]) -> float:
    """Map a statistic onto [0, 1] along the registry's ramp.

    The ramp is always written in telling-direction order: `ramp[0]` is the end
    that reads as human, `ramp[1]` the end that reads as fully machine. So
    `high_is_telling` ramps up (1.5 -> 6.0 em dashes per 1k) and
    `low_is_telling` ramps down (0.75 -> 0.40 paragraph-length CV), and both
    are the same interpolation. Direction is still checked against the ramp
    order, because a ramp written backwards would silently invert a tell.
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return float("nan")
    lo, hi = float(ramp[0]), float(ramp[1])
    if direction == "high_is_telling" and hi < lo:
        raise ValueError(f"high_is_telling ramp must ascend, got {ramp!r}")
    if direction == "low_is_telling" and hi > lo:
        raise ValueError(f"low_is_telling ramp must descend, got {ramp!r}")
    if hi == lo:
        # Degenerate ramp: a step at the threshold rather than a divide by zero.
        if direction == "low_is_telling":
            return 1.0 if value <= lo else 0.0
        return 1.0 if value >= lo else 0.0
    return float(min(1.0, max(0.0, (float(value) - lo) / (hi - lo))))


def winsorized_cap(rates: np.ndarray) -> float:
    """The pooled cap a count tell's rates are clipped to and divided by.

    Normally the 95th percentile. When more than 95% of documents are clean the
    percentile is zero, which would clip every observation to zero and erase a
    rare-but-real tell; in that case the cap falls back to the observed
    maximum, so a tell that fires in one document out of a hundred still scores
    that document at 1.0 instead of vanishing.
    """
    finite = rates[np.isfinite(rates)]
    if finite.size == 0:
        return float("nan")
    cap = float(np.percentile(finite, WINSOR_PERCENTILE))
    if not cap > 0:
        cap = float(finite.max())
    return cap


def normalize(df: pd.DataFrame, tells: Iterable[Tell] | Mapping | None = None) -> pd.DataFrame:
    """Add `score` in [0, 1] (NaN allowed) and `dormant` to a detection frame.

    `tells` supplies the ramp for value tells; pass the same registry entries
    that produced the frame. It may be omitted only when the frame has no value
    tells.
    """
    out = df.copy().reset_index(drop=True)
    if out.empty:
        out["score"] = pd.Series(dtype="float64")
        out["dormant"] = pd.Series(dtype="bool")
        out.attrs.update(df.attrs)
        out.attrs["winsor_caps"] = {}
        return out

    ramps: dict[str, tuple[str | None, Sequence[float] | None]] = {}
    if isinstance(tells, Mapping):
        for tell_id, info in tells.items():
            if info.get("unit") == "value":
                ramps[str(tell_id)] = (info.get("direction"), info.get("ramp"))
    elif tells is not None:
        ramps = {t.id: (t.direction, t.ramp) for t in tells if t.unit == "value"}

    score = np.full(len(out), np.nan)
    caps: dict[str, float] = {}

    for tell_id, group in out.groupby("tell_id", sort=True):
        idx = np.asarray(group.index, dtype=int)
        unit = str(group["unit"].iloc[0])
        raw = group["raw"].to_numpy(dtype=float)

        if unit == "count":
            rates = group["rate_per_1k"].to_numpy(dtype=float)
            cap = winsorized_cap(rates)
            caps[tell_id] = cap
            if not (isinstance(cap, float) and cap > 0):
                score[idx] = np.where(np.isfinite(rates), 0.0, np.nan)
            else:
                score[idx] = np.minimum(rates, cap) / cap

        elif unit == "binary":
            score[idx] = raw

        elif unit == "value":
            direction, ramp = ramps.get(tell_id, (None, None))
            if direction is None or ramp is None:
                raise ValueError(
                    f"{tell_id}: value tell needs its registry direction and ramp to score"
                )
            score[idx] = [ramp_score(x, direction, ramp) for x in raw]

        else:
            raise ValueError(f"{tell_id}: unknown unit {unit!r}")

    out["score"] = score
    out = mark_dormant(out)
    out.attrs.update(df.attrs)
    out.attrs["winsor_caps"] = caps
    return out


def mark_dormant(df: pd.DataFrame) -> pd.DataFrame:
    """Add `dormant`: True on every row of a tell that produced no signal here.

    Computed from `raw`, not from `score`, so it can be recovered from a written
    scores.jsonl without re-running detection. A count or binary tell is dormant
    when it never matched anything in any document; a value tell is dormant when
    it was NaN everywhere (every document fell below the statistic's floor).
    """
    out = df.copy()
    if out.empty:
        out["dormant"] = pd.Series(dtype="bool")
        return out
    dormant = np.zeros(len(out), dtype=bool)
    work = out.reset_index(drop=True)
    for _, group in work.groupby("tell_id", sort=True):
        idx = np.asarray(group.index, dtype=int)
        unit = str(group["unit"].iloc[0])
        raw = group["raw"].to_numpy(dtype=float)
        if unit == "value":
            dormant[idx] = not np.any(np.isfinite(raw))
        else:
            dormant[idx] = not np.any(np.nan_to_num(raw, nan=0.0) > 0)
    out["dormant"] = dormant
    return out


def dormant_tells(df: pd.DataFrame) -> list[str]:
    """Ids of tells that produced no signal anywhere in this corpus."""
    if df.empty:
        return []
    if "dormant" not in df.columns:
        df = mark_dormant(df)
    flagged = df.loc[df["dormant"].astype(bool), "tell_id"]
    return sorted(set(flagged.tolist()))


# --- aggregation -------------------------------------------------------------


def _weighted_nanmean(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Weighted mean along the last axis, dropping NaN from both halves.

    A tell that could not be measured for a model leaves both the numerator and
    the denominator, so it neither counts as zero nor silently reweights the
    tells that were measured.
    """
    mask = np.isfinite(values)
    numerator = np.where(mask, values * weights, 0.0).sum(axis=-1)
    denominator = np.where(mask, weights, 0.0).sum(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(denominator > 0, numerator / denominator, np.nan)


def _mean_scores(df: pd.DataFrame, by: Sequence[str]) -> pd.DataFrame:
    """S(group, t): mean document score, NaN rows excluded."""
    by = list(by)
    if df.empty:
        return pd.DataFrame()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        table = df.pivot_table(
            index=by,
            columns="tell_id",
            values="score",
            aggfunc="mean",
            dropna=False,
        )
    table = table.sort_index(axis=0).sort_index(axis=1)
    return table


def per_model_tell_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Models x tells of S(m, t)."""
    return _mean_scores(df, ["model"])


def per_model_format_tell(df: pd.DataFrame) -> pd.DataFrame:
    """(model, format) x tells of S(m, f, t)."""
    return _mean_scores(df, ["model", "format"])


def _rollup_columns(
    matrix: pd.DataFrame,
    meta: Mapping[str, Mapping[str, Any]],
    category: str,
    include_dormant: bool,
    dormant: set[str],
) -> list[str]:
    cols = []
    for tell_id in matrix.columns:
        info = meta.get(tell_id)
        if info is None:
            continue
        if info.get("category") != category:
            continue
        if info.get("scope") != "general":
            continue
        if info.get("status") != "active":
            continue
        if not include_dormant and tell_id in dormant:
            continue
        cols.append(tell_id)
    return cols


def category_rollup(
    df: pd.DataFrame,
    tells: Iterable[Tell] | Mapping[str, Mapping[str, Any]],
    by: Sequence[str] = ("model",),
    include_dormant: bool = True,
) -> pd.DataFrame:
    """C(group, c): weight-weighted mean of S over active general tells.

    Mean-of-tells, not mean-of-matches: every tell in a category counts once
    (times its registry weight) however often it fires, so one high-frequency
    tell cannot stand in for a category. Model-scoped tells are excluded — they
    feed the Signature Index instead, and letting a tell discovered *on* a
    model into that model's general score would be circular.
    """
    meta = tell_meta(tells)
    matrix = _mean_scores(df, by)
    categories = sorted(CATEGORY_WEIGHTS)
    if matrix.empty:
        return pd.DataFrame(columns=categories)

    dormant = set(dormant_tells(df))
    out = pd.DataFrame(index=matrix.index, columns=categories, dtype=float)
    for category in categories:
        cols = _rollup_columns(matrix, meta, category, include_dormant, dormant)
        if not cols:
            out[category] = np.nan
            continue
        weights = np.array([float(meta[c]["weight"]) for c in cols])
        out[category] = _weighted_nanmean(matrix[cols].to_numpy(dtype=float), weights)
    return out


def indices(
    df: pd.DataFrame,
    tells: Iterable[Tell] | Mapping[str, Mapping[str, Any]],
    by: Sequence[str] = ("model",),
    include_dormant: bool = True,
) -> pd.DataFrame:
    """AI-Tell Index and Signature Index per group, on a 0-100 scale.

    AI-Tell Index = 100 * sum_c W_c * C(m, c), renormalized over the categories
    that are defined for that group, so a corpus with no statistical tells does
    not silently score 15 points lower than one that has them.

    Signature Index = 100 * mean S(m, t) over the tells scoped to *that* model.
    NaN where the model has no signature tells (which is every model until M7
    discovers some).
    """
    meta = tell_meta(tells)
    rollup = category_rollup(df, meta, by=by, include_dormant=include_dormant)
    if rollup.empty:
        return pd.DataFrame(columns=["ai_tell_index", "signature_index"])

    weights = np.array([CATEGORY_WEIGHTS[c] for c in rollup.columns])
    index = 100.0 * _weighted_nanmean(rollup.to_numpy(dtype=float), weights)

    out = pd.DataFrame({"ai_tell_index": index}, index=rollup.index)
    out["signature_index"] = [
        _signature_index(df, meta, group) for group in rollup.index
    ]
    return out


def _group_model(group: Any) -> str:
    """The model out of a rollup index entry, which may be a (model, format) pair."""
    return str(group[0]) if isinstance(group, tuple) else str(group)


def _signature_index(
    df: pd.DataFrame, meta: Mapping[str, Mapping[str, Any]], group: Any
) -> float:
    model = _group_model(group)
    scoped = [
        tell_id
        for tell_id, info in meta.items()
        if info.get("scope") == f"model:{model}" and info.get("status") == "active"
    ]
    if not scoped:
        return float("nan")
    rows = df[(df["model"] == model) & (df["tell_id"].isin(scoped))]
    if rows.empty:
        return float("nan")
    per_tell = rows.groupby("tell_id")["score"].mean()
    value = per_tell.mean(skipna=True)
    return float(100.0 * value) if pd.notna(value) else float("nan")


# --- uncertainty -------------------------------------------------------------


def wilson_ci(hits: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion.

    Wilson rather than Wald because these rates sit near the boundaries: with 8
    documents and 8 hits, Wald reports [1.0, 1.0], which is not a claim any
    corpus of eight can support.
    """
    if n <= 0:
        return (float("nan"), float("nan"))
    p = hits / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, center - half), min(1.0, center + half))


def binary_tell_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Per model x binary tell: documents hit, rate, and its Wilson 95% CI."""
    columns = ["model", "tell_id", "n_docs", "n_hits", "rate", "ci_lo", "ci_hi"]
    if df.empty:
        return pd.DataFrame(columns=columns)
    binary = df[df["unit"] == "binary"]
    if binary.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for (model, tell_id), group in binary.groupby(["model", "tell_id"], sort=True):
        n = int(len(group))
        hits = int(np.nansum(group["raw"].to_numpy(dtype=float)))
        lo, hi = wilson_ci(hits, n)
        rows.append(
            {
                "model": model,
                "tell_id": tell_id,
                "n_docs": n,
                "n_hits": hits,
                "rate": hits / n if n else float("nan"),
                "ci_lo": lo,
                "ci_hi": hi,
            }
        )
    return pd.DataFrame(rows, columns=columns)


def min_evidence_flags(
    df: pd.DataFrame,
    min_docs: int = MIN_DOCS,
    min_occurrences: int = MIN_OCCURRENCES,
) -> pd.DataFrame:
    """Flag model x format x tell cells too thin to make a claim from.

    Two floors. Any cell with fewer than `min_docs` documents is flagged: with
    fewer, one document is most of the estimate. Count cells are flagged again
    when the total observed occurrences fall below `min_occurrences`, because a
    rate built on three matches has a confidence interval wider than the
    difference it would be used to claim.
    """
    columns = ["model", "format", "tell_id", "unit", "n_docs", "occurrences", "flagged", "reason"]
    if df.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for (model, fmt, tell_id), group in df.groupby(["model", "format", "tell_id"], sort=True):
        unit = str(group["unit"].iloc[0])
        n_docs = int(len(group))
        occurrences = float(np.nansum(group["raw"].to_numpy(dtype=float)))
        reasons = []
        if n_docs < min_docs:
            reasons.append(f"n_docs={n_docs}<{min_docs}")
        if unit == "count" and occurrences < min_occurrences:
            reasons.append(f"occurrences={occurrences:g}<{min_occurrences}")
        rows.append(
            {
                "model": model,
                "format": fmt,
                "tell_id": tell_id,
                "unit": unit,
                "n_docs": n_docs,
                "occurrences": occurrences,
                "flagged": bool(reasons),
                "reason": "; ".join(reasons),
            }
        )
    return pd.DataFrame(rows, columns=columns)


# --- bootstrap ---------------------------------------------------------------


def _prompt_id(doc_id: str) -> str:
    """The prompt behind a doc_id: "claude-opus-5/memo-04" -> "memo-04"."""
    return doc_id.split("/", 1)[1] if "/" in doc_id else doc_id


def pairing_summary(df: pd.DataFrame) -> dict[str, Any]:
    """Whether the corpora are balanced enough to bootstrap paired by prompt.

    Cheap enough to call before deciding to spend a thousand replicates, and the
    same predicate `bootstrap_ci` uses, so the manifest cannot disagree with the
    scorecard about which method was applied.
    """
    if df.empty:
        return {"method": "none", "n_prompts": None, "models": []}
    models = sorted(df["model"].unique().tolist())
    prompt_sets = [
        {_prompt_id(d) for d in df.loc[df["model"] == m, "doc_id"].unique()} for m in models
    ]
    shared = set.intersection(*prompt_sets) if prompt_sets else set()
    paired = bool(shared) and all(s == shared for s in prompt_sets) and len(models) > 1
    return {
        "method": "paired" if paired else "unpaired",
        "n_prompts": len(shared) if paired else None,
        "models": models,
    }


def bootstrap_ci(
    df: pd.DataFrame,
    tells: Iterable[Tell] | Mapping[str, Mapping[str, Any]],
    n: int = 1000,
    seed: int = 7,
    include_dormant: bool = True,
) -> dict[str, Any]:
    """Bootstrap 95% CIs on every category rollup, index, and pairwise delta.

    Documents are resampled *within* model, and paired across models by prompt
    when the corpora are balanced: the same prompt draw is applied to every
    model, so the delta CI cancels the prompt effect instead of carrying it.
    Formats differ enormously in how tell-prone they are (an SOP is all bullets
    and headings; a condolence email is neither), so an unpaired delta CI is
    dominated by which prompts each side happened to draw. When the corpora are
    not balanced — different prompts per model, or a mid-generation corpus —
    the pairing is dropped and each model is resampled independently, which is
    wider but honest. `method` in the result records which was used.

    The winsorization cap is *not* recomputed per replicate. It is a property of
    the corpus being described, not of the resample; recomputing it would fold
    the cap's own sampling noise into every score and widen every interval for
    a quantity nobody is estimating.
    """
    meta = tell_meta(tells)
    result: dict[str, Any] = {
        "n": int(n),
        "seed": int(seed),
        "method": "none",
        "models": {},
        "deltas": {},
    }
    if df.empty or "score" not in df.columns:
        return result

    models = sorted(df["model"].unique().tolist())
    point_rollup = category_rollup(df, meta, include_dormant=include_dormant)
    point_index = indices(df, meta, include_dormant=include_dormant)
    categories = list(point_rollup.columns)

    panels = {model: _model_panel(df, model) for model in models}
    pairing = pairing_summary(df)
    result["method"] = pairing["method"]
    result["n_prompts"] = pairing["n_prompts"]

    draws = _resample_draws(panels, pairing["method"] == "paired", n, seed)

    dormant = set(dormant_tells(df)) if not include_dormant else set()
    rep_categories: dict[str, np.ndarray] = {}
    rep_index: dict[str, np.ndarray] = {}
    for model in models:
        reps = _replicate_rollups(
            panels[model], draws[model], meta, categories, dormant, include_dormant
        )
        rep_categories[model] = reps
        rep_index[model] = 100.0 * _weighted_nanmean(
            reps, np.array([CATEGORY_WEIGHTS[c] for c in categories])
        )

    for model in models:
        entry: dict[str, Any] = {"categories": {}}
        for j, category in enumerate(categories):
            entry["categories"][category] = _interval(
                float(point_rollup.loc[model, category]), rep_categories[model][:, j]
            )
        entry["index"] = _interval(
            float(point_index.loc[model, "ai_tell_index"]), rep_index[model]
        )
        signature = float(point_index.loc[model, "signature_index"])
        entry["signature"] = None if math.isnan(signature) else {"point": signature}
        result["models"][model] = entry

    for i, left in enumerate(models):
        for right in models[i + 1 :]:
            delta = rep_index[left] - rep_index[right]
            point = float(
                point_index.loc[left, "ai_tell_index"]
                - point_index.loc[right, "ai_tell_index"]
            )
            interval = _interval(point, delta)
            interval["significant"] = bool(
                np.isfinite(interval["lo"])
                and np.isfinite(interval["hi"])
                and (interval["lo"] > 0 or interval["hi"] < 0)
            )
            result["deltas"][f"{left}|{right}"] = interval
    return result


@dataclass(frozen=True)
class _Panel:
    """One model's scores as a dense array: documents down, tells across."""

    docs: list[str]
    prompts: list[str]
    tells: list[str]
    scores: np.ndarray


def _model_panel(df: pd.DataFrame, model: str) -> _Panel:
    wide = (
        df[df["model"] == model]
        .pivot_table(index="doc_id", columns="tell_id", values="score", aggfunc="mean", dropna=False)
        .sort_index(axis=0)
        .sort_index(axis=1)
    )
    docs = list(wide.index)
    return _Panel(
        docs=docs,
        prompts=[_prompt_id(d) for d in docs],
        tells=list(wide.columns),
        scores=wide.to_numpy(dtype=float),
    )


def _resample_draws(
    panels: Mapping[str, _Panel], paired: bool, n: int, seed: int
) -> dict[str, np.ndarray]:
    """Row indices for each replicate, per model: shape (n, docs_in_that_model).

    Paired draws pick prompts once and translate them into each model's own row
    order, so replicate 40 holds the same prompts on both sides of a delta.
    """
    models = sorted(panels)
    rng = np.random.default_rng(seed)
    if paired:
        shared = sorted(set.intersection(*[set(panels[m].prompts) for m in models]))
        picks = rng.integers(0, len(shared), size=(n, len(shared)))
        out = {}
        for model in models:
            position = {p: i for i, p in enumerate(panels[model].prompts)}
            out[model] = np.array([position[p] for p in shared])[picks]
        return out
    return {
        model: rng.integers(0, len(panels[model].docs), size=(n, len(panels[model].docs)))
        for model in models
    }


# Replicates are computed in blocks so that (block x docs x tells) stays small:
# a full corpus at 1,000 replicates in one array runs to hundreds of megabytes.
REPLICATE_BLOCK = 200


def _replicate_rollups(
    panel: _Panel,
    draws: np.ndarray,
    meta: Mapping[str, Mapping[str, Any]],
    categories: Sequence[str],
    dormant: set[str],
    include_dormant: bool,
) -> np.ndarray:
    """C(m, c) for every replicate: shape (n_replicates, n_categories)."""
    masks: dict[str, np.ndarray] = {}
    weights: dict[str, np.ndarray] = {}
    for category in categories:
        keep = [
            i
            for i, tell_id in enumerate(panel.tells)
            if (info := meta.get(tell_id)) is not None
            and info.get("category") == category
            and info.get("scope") == "general"
            and info.get("status") == "active"
            and (include_dormant or tell_id not in dormant)
        ]
        masks[category] = np.array(keep, dtype=int)
        weights[category] = np.array([float(meta[panel.tells[i]]["weight"]) for i in keep])

    n = draws.shape[0]
    out = np.empty((n, len(categories)))
    for start in range(0, n, REPLICATE_BLOCK):
        stop = min(n, start + REPLICATE_BLOCK)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)  # all-NaN tells are expected
            means = np.nanmean(panel.scores[draws[start:stop]], axis=1)
        for j, category in enumerate(categories):
            keep = masks[category]
            if keep.size == 0:
                out[start:stop, j] = np.nan
                continue
            out[start:stop, j] = _weighted_nanmean(means[:, keep], weights[category])
    return out


def _interval(point: float, replicates: np.ndarray) -> dict[str, float]:
    finite = replicates[np.isfinite(replicates)]
    if finite.size == 0:
        return {"point": point, "lo": float("nan"), "hi": float("nan")}
    return {
        "point": point,
        "lo": float(np.percentile(finite, 2.5)),
        "hi": float(np.percentile(finite, 97.5)),
    }


__all__ = [
    "CATEGORY_WEIGHTS",
    "MIN_DOCS",
    "MIN_OCCURRENCES",
    "binary_tell_rates",
    "bootstrap_ci",
    "category_rollup",
    "detect_all",
    "dormant_tells",
    "indices",
    "judge_tell_ids",
    "mark_dormant",
    "min_evidence_flags",
    "normalize",
    "pairing_summary",
    "per_model_format_tell",
    "per_model_tell_matrix",
    "ramp_score",
    "tell_meta",
    "wilson_ci",
    "winsorized_cap",
]
