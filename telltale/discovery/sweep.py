"""The statistical half of discovery: what the corpus says before anyone asks a model.

Nothing in this file calls an LLM. It is the cheap, deterministic, endlessly
re-runnable pass that finds *where to look* — and it runs first on purpose. A
lens prompt that arrives with "these are the 200 n-grams this model
overproduces, with z-scores" asks a much narrower question than one that arrives
empty, and a narrow question is one whose answer can be checked.

Four measurements, each chosen because it answers a different question:

* **Log-odds with an informative Dirichlet prior** (Monroe, Colaresi & Quinn
  2008) for *which words separate the models*. The naive alternatives both fail
  in the ways this corpus guarantees: raw frequency differences are dominated by
  function words, and a plain log-odds ratio is dominated by hapaxes, where one
  extra occurrence swings the estimate by an order of magnitude. MCQ fixes both
  by shrinking every word toward the pooled corpus rate in proportion to how
  rare it is, then dividing by the posterior standard deviation — so the score
  is "how confidently is this word overused", not "by what factor".
* **Dunning's G²** for *which word pairs are phrases rather than coincidences*.
  A bigram like "it is worth" is only interesting if the two halves co-occur
  more than their independent rates predict, and G² is the likelihood-ratio test
  for exactly that, valid at the small counts where chi-square is not.
* **Cohen's d over every registered statistic** for *which measurable habits
  differ*, on the same scale for every stat so "0.8 on bullet density" and "0.8
  on sentence-length CV" mean the same thing.
* **KWIC** for *what the hit actually looks like in context*, because a z-score
  of 6 on "landscape" and a z-score of 6 on "leverage" are the same number and
  very different findings, and nobody should be asked to propose a regex without
  reading the lines.

Everything writes sorted output. A sweep re-run on an unchanged corpus produces
byte-identical files, which is what makes the discovery run auditable rather
than merely repeatable-ish.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Iterable, Sequence

import pandas as pd

from telltale import textstats
from telltale.corpus import Doc

#: z at p < 0.001, one-tailed. The sweep proposes hundreds of n-grams per model,
#: so the threshold is set where a single uncorrected 0.05 test would be absurd.
DEFAULT_Z_MIN = 3.09

#: G² at p < 0.001 with one degree of freedom.
G2_CRITICAL = 10.83

#: Cohen's conventional "medium" effect. Below it, a stat difference is not worth
#: a tell even when the corpus is large enough to call it significant.
COHEN_D_FLAG = 0.5

MAX_N = 4

KWIC_CONTEXT = 60

SWEEP_FILENAME = "candidates_sweep.jsonl"
COLLOCATIONS_FILENAME = "collocations.jsonl"
STAT_DELTAS_FILENAME = "stat_deltas.jsonl"


# --- tokenizing --------------------------------------------------------------


def doc_tokens(doc: Doc) -> list[list[str]]:
    """One lowercased token list per sentence of the document's stripped prose.

    Sentence-bounded on purpose. Ngrams built over a flat token stream invent
    phrases across a full stop ("...the budget. Moreover the board..." would
    yield "budget moreover"), and those artefacts sort straight to the top of a
    log-odds table because they are rare everywhere. The one place they would be
    genuinely informative — a habit of *opening* sentences a certain way — is
    already measured by `textstats.sentence_opener_diversity` and by the
    `pct_sentences_starting_*` stats.
    """
    return [
        [t.lower() for t in textstats.WORD_PATTERN.findall(sentence)]
        for sentence in textstats.split_sentences(doc.plain)
    ]


def ngrams(tokens: Sequence[str], n: int) -> list[str]:
    """Space-joined n-grams of one token sequence."""
    if n <= 0 or len(tokens) < n:
        return []
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def doc_ngrams(doc: Doc, n: int) -> list[str]:
    """Every n-gram of a document, sentence by sentence."""
    out: list[str] = []
    for sentence in doc_tokens(doc):
        out.extend(ngrams(sentence, n))
    return out


def models_of(docs: Iterable[Doc]) -> list[str]:
    return sorted({d.model for d in docs})


def token_counts(docs: Sequence[Doc], n: int) -> pd.DataFrame:
    """n-gram x model count matrix, index sorted, columns sorted by model id.

    Counts, not rates: the log-odds estimator below needs the raw counts and the
    per-model totals separately, and dividing early would throw away the sample
    size the prior is built from.
    """
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    models = models_of(docs)
    tallies: dict[str, dict[str, int]] = {}
    for doc in sorted(docs, key=lambda d: d.doc_id):
        column = tallies.setdefault(doc.model, {})
        for gram in doc_ngrams(doc, n):
            column[gram] = column.get(gram, 0) + 1

    frame = pd.DataFrame(
        {model: pd.Series(tallies.get(model, {}), dtype="float64") for model in models}
    )
    if frame.empty:
        frame = pd.DataFrame(columns=models, dtype="float64")
    frame = frame.fillna(0.0).astype("int64")
    frame.index.name = "ngram"
    frame = frame.sort_index()
    frame.attrs["n"] = n
    return frame


# --- log-odds with an informative Dirichlet prior ----------------------------


def log_odds_dirichlet(
    counts: pd.DataFrame, target_model: str, alpha0: float = 500.0
) -> pd.DataFrame:
    """Monroe-Colaresi-Quinn log-odds of `target_model` against the pooled rest.

    The prior is the pooled corpus itself: a word's prior mass `alpha_w` is
    `alpha0 * y_w / n_total`, so a word that is common everywhere is shrunk a
    lot and a word that is rare everywhere is shrunk toward nothing. `alpha0` is
    the strength of that prior in pseudo-counts; 500 is MCQ's own default and is
    roughly "half a short document's worth of evidence before I believe you".

        delta = ln[(y_iw + a_w) / (n_i + a0 - y_iw - a_w)]
              - ln[(y_jw + a_w) / (n_j + a0 - y_jw - a_w)]
        sigma^2 ~ 1/(y_iw + a_w) + 1/(y_jw + a_w)
        z = delta / sigma

    Returns the per-model counts, `count_target`, `count_rest`, `alpha`,
    `delta`, `sigma`, and `z`, sorted by z descending then n-gram — so the head
    of the frame is what the target model overuses and the tail is what it
    avoids, both of which are findings.
    """
    if target_model not in counts.columns:
        raise KeyError(f"{target_model!r} is not a column of the count frame")
    if len(counts.columns) < 2:
        raise ValueError("log-odds needs at least two models to contrast")

    numeric = counts.astype("float64")
    pooled = numeric.sum(axis=1)
    n_total = float(numeric.to_numpy().sum())
    if n_total <= 0:
        empty = counts.copy()
        for column in ("count_target", "count_rest", "alpha", "delta", "sigma", "z"):
            empty[column] = pd.Series(dtype="float64")
        return empty

    alpha = alpha0 * pooled / n_total
    y_i = numeric[target_model]
    y_j = numeric.drop(columns=[target_model]).sum(axis=1)
    n_i = float(y_i.sum())
    n_j = float(y_j.sum())

    a_i = y_i + alpha
    a_j = y_j + alpha
    delta = (a_i / (n_i + alpha0 - a_i)).apply(math.log) - (
        a_j / (n_j + alpha0 - a_j)
    ).apply(math.log)
    sigma = (1.0 / a_i + 1.0 / a_j) ** 0.5

    out = counts.copy()
    out["count_target"] = y_i.astype("int64")
    out["count_rest"] = y_j.astype("int64")
    out["alpha"] = alpha
    out["delta"] = delta
    out["sigma"] = sigma
    out["z"] = delta / sigma
    out = out.sort_values(["z", "ngram"], ascending=[False, True], kind="mergesort")
    out.attrs["target_model"] = target_model
    out.attrs["alpha0"] = float(alpha0)
    out.attrs["n_target"] = n_i
    out.attrs["n_rest"] = n_j
    out.attrs["n"] = counts.attrs.get("n")
    return out


# --- Dunning's G2 ------------------------------------------------------------


def _xlogx(observed: float, expected: float) -> float:
    if observed <= 0 or expected <= 0:
        return 0.0
    return observed * math.log(observed / expected)


def g2_contingency(o11: float, o12: float, o21: float, o22: float) -> float:
    """Dunning's log-likelihood ratio for one 2x2 table.

    G2 = 2 * sum(O * ln(O / E)) over the four cells, with E from the margins.
    Cells with no observations contribute nothing, which is the limit of
    `x ln x` as x goes to zero and is why this test is usable where chi-square
    is not.
    """
    total = o11 + o12 + o21 + o22
    if total <= 0:
        return 0.0
    row1, row2 = o11 + o12, o21 + o22
    col1, col2 = o11 + o21, o12 + o22
    e11 = row1 * col1 / total
    e12 = row1 * col2 / total
    e21 = row2 * col1 / total
    e22 = row2 * col2 / total
    return 2.0 * (
        _xlogx(o11, e11) + _xlogx(o12, e12) + _xlogx(o21, e21) + _xlogx(o22, e22)
    )


def collocations_g2(
    docs: Sequence[Doc], min_count: int = 10, critical: float = G2_CRITICAL
) -> pd.DataFrame:
    """Bigrams that co-occur more than chance, pooled over the whole corpus.

    The contingency table for bigram (w1, w2) is built over bigram *slots*, not
    over tokens: how often w1 was followed by w2, by anything else, how often
    anything else was followed by w2, and the remainder. Rows are kept when they
    clear `min_count` occurrences and `critical` (p < 0.001 by default), sorted
    by G2 descending.
    """
    models = models_of(docs)
    bigrams: dict[str, int] = {}
    per_model: dict[str, dict[str, int]] = {m: {} for m in models}
    first: dict[str, int] = {}
    second: dict[str, int] = {}
    total = 0

    for doc in sorted(docs, key=lambda d: d.doc_id):
        for sentence in doc_tokens(doc):
            for i in range(len(sentence) - 1):
                w1, w2 = sentence[i], sentence[i + 1]
                key = f"{w1} {w2}"
                bigrams[key] = bigrams.get(key, 0) + 1
                per_model[doc.model][key] = per_model[doc.model].get(key, 0) + 1
                first[w1] = first.get(w1, 0) + 1
                second[w2] = second.get(w2, 0) + 1
                total += 1

    rows: list[dict[str, Any]] = []
    for key in sorted(bigrams):
        o11 = bigrams[key]
        if o11 < min_count:
            continue
        w1, w2 = key.split(" ", 1)
        o12 = first[w1] - o11
        o21 = second[w2] - o11
        o22 = total - o11 - o12 - o21
        g2 = g2_contingency(o11, o12, o21, o22)
        if g2 < critical:
            continue
        row: dict[str, Any] = {
            "bigram": key,
            "count": o11,
            "g2": g2,
            "expected": (o11 + o12) * (o11 + o21) / total if total else 0.0,
        }
        for model in models:
            row[f"count_{model}"] = per_model[model].get(key, 0)
        rows.append(row)

    frame = pd.DataFrame(
        rows,
        columns=["bigram", "count", "g2", "expected", *[f"count_{m}" for m in models]],
    )
    if not frame.empty:
        frame = frame.sort_values(
            ["g2", "bigram"], ascending=[False, True], kind="mergesort"
        ).reset_index(drop=True)
    frame.attrs["n_bigrams"] = total
    return frame


# --- statistic deltas --------------------------------------------------------


def _mean_sd(values: Sequence[float]) -> tuple[float, float]:
    n = len(values)
    if n == 0:
        return float("nan"), float("nan")
    mean = sum(values) / n
    if n < 2:
        return mean, float("nan")
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(variance)


def cohens_d(target: Sequence[float], rest: Sequence[float]) -> float:
    """Standardized mean difference with the pooled SD. NaN when it is undefined."""
    n1, n2 = len(target), len(rest)
    if n1 < 2 or n2 < 2:
        return float("nan")
    m1, s1 = _mean_sd(target)
    m2, s2 = _mean_sd(rest)
    pooled_var = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2)
    if pooled_var <= 0:
        return float("nan")
    return (m1 - m2) / math.sqrt(pooled_var)


def stat_deltas(docs: Sequence[Doc], flag_at: float = COHEN_D_FLAG) -> pd.DataFrame:
    """Every registered statistic, per model, against the pooled other models.

    NaN is dropped rather than zeroed, exactly as scoring does: a stat that is
    not computable on a six-sentence email is a missing observation, and reading
    it as zero would manufacture a difference out of document length.
    """
    models = models_of(docs)
    ordered = sorted(docs, key=lambda d: d.doc_id)

    rows: list[dict[str, Any]] = []
    for stat_name in sorted(textstats.STATS):
        values: dict[str, list[float]] = {m: [] for m in models}
        for doc in ordered:
            value = float(textstats.compute(stat_name, doc))
            if math.isnan(value):
                continue
            values[doc.model].append(value)
        for model in models:
            target = values[model]
            rest = [v for m in models if m != model for v in values[m]]
            mean_t, sd_t = _mean_sd(target)
            mean_r, sd_r = _mean_sd(rest)
            d = cohens_d(target, rest)
            rows.append(
                {
                    "stat": stat_name,
                    "model": model,
                    "n_target": len(target),
                    "mean_target": mean_t,
                    "sd_target": sd_t,
                    "n_rest": len(rest),
                    "mean_rest": mean_r,
                    "sd_rest": sd_r,
                    "cohens_d": d,
                    "flagged": bool(not math.isnan(d) and abs(d) >= flag_at),
                }
            )

    frame = pd.DataFrame(
        rows,
        columns=[
            "stat",
            "model",
            "n_target",
            "mean_target",
            "sd_target",
            "n_rest",
            "mean_rest",
            "sd_rest",
            "cohens_d",
            "flagged",
        ],
    )
    if not frame.empty:
        frame = frame.sort_values(["stat", "model"], kind="mergesort").reset_index(
            drop=True
        )
    return frame


# --- keyword in context ------------------------------------------------------


def needle_pattern(needle: str) -> re.Pattern[str]:
    """A word-bounded, whitespace-tolerant pattern for one n-gram."""
    tokens = textstats.WORD_PATTERN.findall(needle)
    if not tokens:
        return re.compile(re.escape(needle), re.IGNORECASE)
    body = r"\W+".join(re.escape(t) for t in tokens)
    return re.compile(rf"\b{body}\b", re.IGNORECASE)


def kwic(docs: Sequence[Doc], needle: str, k: int = 8) -> list[str]:
    """Up to `k` keyword-in-context lines, one per document, in doc_id order.

    One line per document rather than `k` lines from whichever document happens
    to be first: a lens prompt showing eight hits from one memo teaches the
    model about that memo. The match is marked with guillemets so a reader can
    see what was counted, and whitespace is collapsed so each hit is one line.
    """
    pattern = needle_pattern(needle)
    lines: list[str] = []
    for doc in sorted(docs, key=lambda d: d.doc_id):
        if len(lines) >= k:
            break
        match = pattern.search(doc.plain)
        if match is None:
            continue
        left = max(0, match.start() - KWIC_CONTEXT)
        right = min(len(doc.plain), match.end() + KWIC_CONTEXT)
        before = " ".join(doc.plain[left : match.start()].split())
        hit = " ".join(doc.plain[match.start() : match.end()].split())
        after = " ".join(doc.plain[match.end() : right].split())
        head = ("…" + before if left > 0 else before).strip()
        tail = (after + "…" if right < len(doc.plain) else after).strip()
        body = " ".join(part for part in (head, f"«{hit}»", tail) if part)
        lines.append(f"{doc.doc_id}: {body}")
    return lines


def doc_frequency(docs: Sequence[Doc], needle: str) -> dict[str, float]:
    """Share of each model's documents containing the n-gram at least once."""
    pattern = needle_pattern(needle)
    hits: dict[str, int] = {}
    totals: dict[str, int] = {}
    for doc in docs:
        totals[doc.model] = totals.get(doc.model, 0) + 1
        if pattern.search(doc.plain):
            hits[doc.model] = hits.get(doc.model, 0) + 1
    return {
        model: (hits.get(model, 0) / totals[model] if totals[model] else 0.0)
        for model in sorted(totals)
    }


# --- the sweep ---------------------------------------------------------------


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            written += 1
    return written


def sweep_rows(
    docs: Sequence[Doc],
    target_model: str,
    z_min: float = DEFAULT_Z_MIN,
    min_count: int = 10,
    top_k: int = 200,
    max_n: int = MAX_N,
    alpha0: float = 500.0,
    kwic_k: int = 8,
) -> list[dict[str, Any]]:
    """The n-gram candidates for one model, in |z| order, evidence attached.

    Filtered on both sides of the estimator: `z_min` is the confidence floor,
    `min_count` the evidence floor. Either alone lets something through that
    should not be proposed — a huge z on three occurrences, or two hundred
    occurrences at z = 1.2.
    """
    models = models_of(docs)
    if target_model not in models:
        return []
    rows: list[dict[str, Any]] = []
    totals = {
        model: sum(len(textstats.WORD_PATTERN.findall(d.plain)) for d in docs if d.model == model)
        for model in models
    }

    for n in range(1, max_n + 1):
        counts = token_counts(docs, n)
        if counts.empty or len(counts.columns) < 2:
            continue
        scored = log_odds_dirichlet(counts, target_model, alpha0=alpha0)
        keep = scored[
            (scored["z"].abs() >= z_min) & (scored["count_target"] >= min_count)
        ]
        keep = keep.reindex(
            keep["z"].abs().sort_values(ascending=False, kind="mergesort").index
        )
        for ngram, row in list(keep.iterrows())[:top_k]:
            rows.append(
                {
                    "kind": "ngram",
                    "model": target_model,
                    "n": n,
                    "ngram": str(ngram),
                    "z": float(row["z"]),
                    "delta": float(row["delta"]),
                    "alpha": float(row["alpha"]),
                    "counts": {m: int(row[m]) for m in models},
                    "rates_per_1k": {
                        m: (1000.0 * float(row[m]) / totals[m]) if totals[m] else 0.0
                        for m in models
                    },
                    "doc_freq": doc_frequency(docs, str(ngram)),
                    "kwic": kwic(docs, str(ngram), k=kwic_k),
                }
            )

    rows.sort(key=lambda r: (-abs(r["z"]), r["n"], r["ngram"]))
    return rows


def run_sweep(
    docs: Sequence[Doc],
    out_dir: Path,
    z_min: float = DEFAULT_Z_MIN,
    min_count: int = 10,
    top_k: int = 200,
    max_n: int = MAX_N,
    alpha0: float = 500.0,
) -> dict[str, Any]:
    """Write the three sweep artefacts and return a summary of what was written."""
    out = Path(out_dir)
    models = models_of(docs)

    ngram_rows: list[dict[str, Any]] = []
    for model in models:
        ngram_rows.extend(
            sweep_rows(
                docs,
                model,
                z_min=z_min,
                min_count=min_count,
                top_k=top_k,
                max_n=max_n,
                alpha0=alpha0,
            )
        )
    ngram_rows.sort(key=lambda r: (r["model"], -abs(r["z"]), r["n"], r["ngram"]))

    collocations = collocations_g2(docs, min_count=min_count)
    deltas = stat_deltas(docs)

    written = {
        SWEEP_FILENAME: _write_jsonl(out / SWEEP_FILENAME, ngram_rows),
        COLLOCATIONS_FILENAME: _write_jsonl(
            out / COLLOCATIONS_FILENAME,
            (
                {k: (v.item() if hasattr(v, "item") else v) for k, v in row.items()}
                for row in collocations.to_dict("records")
            ),
        ),
        STAT_DELTAS_FILENAME: _write_jsonl(
            out / STAT_DELTAS_FILENAME,
            (
                {k: (v.item() if hasattr(v, "item") else v) for k, v in row.items()}
                for row in deltas.to_dict("records")
            ),
        ),
    }
    return {
        "out_dir": str(out),
        "n_docs": len(docs),
        "models": models,
        "z_min": z_min,
        "min_count": min_count,
        "top_k": top_k,
        "written": written,
        "flagged_stats": int(deltas["flagged"].sum()) if not deltas.empty else 0,
    }


def load_sweep(out_dir: Path, model: str | None = None) -> list[dict[str, Any]]:
    """Read candidates_sweep.jsonl back, optionally for one model."""
    path = Path(out_dir) / SWEEP_FILENAME
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and (model is None or row.get("model") == model):
            rows.append(row)
    return rows


__all__ = [
    "COHEN_D_FLAG",
    "COLLOCATIONS_FILENAME",
    "DEFAULT_Z_MIN",
    "G2_CRITICAL",
    "MAX_N",
    "STAT_DELTAS_FILENAME",
    "SWEEP_FILENAME",
    "cohens_d",
    "collocations_g2",
    "doc_frequency",
    "doc_ngrams",
    "doc_tokens",
    "g2_contingency",
    "kwic",
    "load_sweep",
    "log_odds_dirichlet",
    "models_of",
    "needle_pattern",
    "ngrams",
    "run_sweep",
    "stat_deltas",
    "sweep_rows",
    "token_counts",
]
