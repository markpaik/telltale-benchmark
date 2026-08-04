"""Run outputs: the scores, the matrices, and the scorecard a human reads.

Four files land in a run directory, and the split between them is the point:

* `scores.jsonl` is the evidence — one row per (document, tell) with the raw
  measurement and the quotes that produced it. Everything else is derived from
  it, which is why `render_scorecard` reads it back off disk rather than taking
  the in-memory frame. If the scorecard says a model uses "delve" nine times per
  thousand words, the nine matches are in the jsonl with line numbers.
* `matrix.csv` / `matrix_by_format.csv` are the model x tell surface, for
  anyone who wants to do their own analysis.
* `scorecard.md` is the argument: what the numbers are, how sure we are, and
  which cells are too thin to make a claim from.

The scorecard deliberately contains no timestamp and no run id. Everything in
it is a pure function of the corpus and the registry, so two runs over the same
inputs produce the same bytes, and `manifest.verify` can say so with `cmp`
rather than with a tolerance.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from telltale import scoring
from telltale.corpus import FORMATS, load_corpus
from telltale.manifest import build_manifest, load_manifest, write_manifest
from telltale.registry import Registry

SCORES_NAME = "scores.jsonl"
MATRIX_NAME = "matrix.csv"
MATRIX_BY_FORMAT_NAME = "matrix_by_format.csv"
SCORECARD_NAME = "scorecard.md"

# Fields written per row, in this order. `matches` is trimmed here (the full
# evidence list is capped at 50 during detection) purely for file size: ten
# quotes is more than any reader checks, and a 121-tell corpus of long
# documents would otherwise write tens of megabytes of context windows.
SCORE_FIELDS = (
    "doc_id",
    "model",
    "format",
    "tell_id",
    "category",
    "scope",
    "method",
    "unit",
    "raw",
    "rate_per_1k",
    "score",
    "matches",
    "detail",
)
MATCHES_IN_JSONL = 10
ROUND_DP = 6

# Seven levels, low to high. Deliberately not colour: a scorecard gets pasted
# into a terminal, a code review, and a chat window, and these survive all three.
HEAT_GLYPHS = "▁▂▃▄▅▆▇"
EM_DASH = "—"
TOP_TELLS = 10
EXEMPLAR_CHARS = 120


# --- scores.jsonl ------------------------------------------------------------


def _round(value: Any) -> float | None:
    """Round for serialization; NaN and None both become JSON null.

    JSON has no NaN, and writing 0.0 for "could not be computed" is exactly the
    confusion the scoring code works to avoid. The unit column says whether null
    means "no rate for this unit" or "statistic below its floor".
    """
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return round(number, ROUND_DP)


def write_scores_jsonl(df: pd.DataFrame, path: Path) -> Path:
    """One JSON object per (document, tell), in (doc_id, tell_id) order."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if df.empty:
        path.write_text("", encoding="utf-8")
        return path

    ordered = df.sort_values(["doc_id", "tell_id"], kind="mergesort")
    lines = []
    for row in ordered.to_dict(orient="records"):
        matches = row.get("matches") or []
        record = {
            "doc_id": row["doc_id"],
            "model": row["model"],
            "format": row["format"],
            "tell_id": row["tell_id"],
            "category": row["category"],
            "scope": row["scope"],
            "method": row["method"],
            "unit": row["unit"],
            "raw": _round(row["raw"]),
            "rate_per_1k": _round(row.get("rate_per_1k")),
            "score": _round(row.get("score")),
            "matches": list(matches)[:MATCHES_IN_JSONL],
            "detail": row.get("detail") or {},
        }
        lines.append(json.dumps(record, ensure_ascii=False, sort_keys=False))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def read_scores_jsonl(path: Path) -> pd.DataFrame:
    """Load scores.jsonl back into the frame the aggregation functions take."""
    text = Path(path).read_text(encoding="utf-8")
    rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    df = pd.DataFrame(rows, columns=list(SCORE_FIELDS))
    for column in ("raw", "rate_per_1k", "score"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


# --- matrices ----------------------------------------------------------------


def write_matrices(df: pd.DataFrame, outdir: Path) -> list[Path]:
    """models x tells and (model, format) x tells, as CSV."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, table in (
        (MATRIX_NAME, scoring.per_model_tell_matrix(df)),
        (MATRIX_BY_FORMAT_NAME, scoring.per_model_format_tell(df)),
    ):
        path = outdir / name
        table.round(ROUND_DP).to_csv(path, float_format=f"%.{ROUND_DP}f", lineterminator="\n")
        written.append(path)
    return written


# --- scorecard ---------------------------------------------------------------


def _fmt(value: Any, dp: int = 1) -> str:
    if value is None:
        return EM_DASH
    try:
        number = float(value)
    except (TypeError, ValueError):
        return EM_DASH
    if math.isnan(number):
        return EM_DASH
    return f"{number:.{dp}f}"


def _cell(text: str) -> str:
    """Make a string safe to drop inside a markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ")


def _heat(value: float) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return " "
    bucket = int(max(0.0, min(100.0, float(value))) / 100.0 * len(HEAT_GLYPHS))
    return HEAT_GLYPHS[min(bucket, len(HEAT_GLYPHS) - 1)]


def _table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("|" + "|".join("---" for _ in header) + "|")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def _category_order() -> list[str]:
    """Categories heaviest first, so the table reads in order of influence."""
    return sorted(scoring.CATEGORY_WEIGHTS, key=lambda c: (-scoring.CATEGORY_WEIGHTS[c], c))


def _model_evidence(df: pd.DataFrame) -> set[tuple[str, str]]:
    """(model, tell) pairs whose whole-corpus evidence is below the floor."""
    collapsed = df.copy()
    collapsed["format"] = "*"
    flags = scoring.min_evidence_flags(collapsed)
    if flags.empty:
        return set()
    thin = flags[flags["flagged"]]
    return {(str(r.model), str(r.tell_id)) for r in thin.itertuples()}


def _exemplar(rows: pd.DataFrame) -> str:
    """The best single quote for a (model, tell): from the doc that fired most."""
    with_matches = [r for r in rows.to_dict("records") if r.get("matches")]
    if not with_matches:
        return ""
    best = sorted(
        with_matches,
        key=lambda r: (-(r["raw"] if pd.notna(r["raw"]) else 0.0), r["doc_id"]),
    )[0]
    match = best["matches"][0]
    quote = str(match.get("quote", ""))
    if len(quote) > EXEMPLAR_CHARS:
        quote = quote[: EXEMPLAR_CHARS - 1].rstrip() + "…"
    return f'"{quote}" — {best["doc_id"]}:{match.get("line", 0)}'


def _signal(unit: str, rows: pd.DataFrame) -> str:
    """What the tell actually did, in the terms its unit is measured in.

    Binary tells carry their Wilson 95% interval inline. "100% of documents" off
    four documents and off four hundred are different claims, and the interval is
    the only thing in the cell that says which one this is.
    """
    if unit == "count":
        rate = rows["rate_per_1k"].mean(skipna=True)
        return f"{_fmt(rate, 2)}/1k"
    if unit == "binary":
        n = len(rows)
        if not n:  # pragma: no cover - a tell with no rows has no row here
            return EM_DASH
        hits = int(np.nansum(rows["raw"].to_numpy(dtype=float)))
        lo, hi = scoring.wilson_ci(hits, n)
        return (
            f"{100.0 * hits / n:.0f}% of docs "
            f"[{100.0 * lo:.0f}-{100.0 * hi:.0f}%]"
        )
    value = rows["raw"].mean(skipna=True)
    return _fmt(value, 3)


def render_scorecard(run_dir: Path) -> Path:
    """Write scorecard.md from a run directory's scores.jsonl and manifest.

    Reads from disk on purpose: the scorecard is a reading of the evidence file,
    not a second computation alongside it, so it cannot drift from what was
    written. It also means a scorecard can be re-rendered — with a changed
    template, say — from an archived run.
    """
    run_dir = Path(run_dir)
    manifest = load_manifest(run_dir)
    df = read_scores_jsonl(run_dir / SCORES_NAME)
    meta = scoring.tell_meta(manifest["registry"]["tells"])

    lines: list[str] = ["# telltale scorecard", ""]

    if df.empty:
        lines += [
            "No documents were scored. The corpus at "
            f"`{manifest['corpus']['root']}` is empty.",
            "",
        ]
        lines += _run_stats(manifest, df, {}, [])
        path = run_dir / SCORECARD_NAME
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    for column in ("status", "weight", "name"):
        df[column] = df["tell_id"].map(lambda t, c=column: (meta.get(t) or {}).get(c))
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce").fillna(1.0)
    df = scoring.mark_dormant(df)

    boot_cfg = manifest.get("bootstrap") or {}
    n_boot = int(boot_cfg.get("n") or 1000)
    seed = int(boot_cfg.get("seed") or 7)

    rollup = scoring.category_rollup(df, meta)
    index = scoring.indices(df, meta)
    boot = scoring.bootstrap_ci(df, meta, n=n_boot, seed=seed)
    ranked = sorted(
        index.index.tolist(),
        key=lambda m: (
            -index.loc[m, "ai_tell_index"]
            if not math.isnan(index.loc[m, "ai_tell_index"])
            else float("inf"),
            m,
        ),
    )

    lines += _headline(manifest, rollup, index, boot, ranked)
    lines += _heat_section(df, meta)
    lines += _top_tells(df, meta, ranked)
    lines += _evidence_section(df)
    lines += _dormant_section(df, meta)
    lines += _run_stats(manifest, df, boot, ranked)

    path = run_dir / SCORECARD_NAME
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _headline(
    manifest: Mapping[str, Any],
    rollup: pd.DataFrame,
    index: pd.DataFrame,
    boot: Mapping[str, Any],
    ranked: Sequence[str],
) -> list[str]:
    categories = _category_order()
    header = ["Rank", "Model"]
    header += [f"{c.title()} ({scoring.CATEGORY_WEIGHTS[c]:.2f})" for c in categories]
    header += ["AI-Tell Index [95% CI]", "Signature"]

    rows = []
    for rank, model in enumerate(ranked, start=1):
        cells = [str(rank), f"`{model}`"]
        cells += [_fmt(100.0 * rollup.loc[model, c]) for c in categories]
        entry = (boot.get("models") or {}).get(model, {})
        interval = entry.get("index") or {}
        point = index.loc[model, "ai_tell_index"]
        ci = ""
        if interval.get("lo") is not None and not math.isnan(float(interval.get("lo", float("nan")))):
            ci = f" [{_fmt(interval['lo'])}, {_fmt(interval['hi'])}]"
        cells.append(f"**{_fmt(point)}**{ci}")
        cells.append(_fmt(index.loc[model, "signature_index"]))
        rows.append(cells)

    lines = [
        "## 1. Headline",
        "",
        "Every number is 0-100, where 0 is "
        "\"none of the tells in this category fired\" and 100 is \"all of them, at or "
        "above the ceiling rate\". The index is the category scores weighted as shown "
        "in each column header.",
        "",
    ]
    lines += _table(header, rows)

    interval_rows = []
    for model in ranked:
        cells = [f"`{model}`"]
        entry = ((boot.get("models") or {}).get(model) or {}).get("categories") or {}
        for category in categories:
            band = entry.get(category) or {}
            point = 100.0 * float(rollup.loc[model, category])
            lo, hi = band.get("lo"), band.get("hi")
            if lo is None or (isinstance(lo, float) and math.isnan(lo)):
                cells.append(_fmt(point))
            else:
                cells.append(f"{_fmt(point)} [{_fmt(100.0 * lo)}, {_fmt(100.0 * hi)}]")
        interval_rows.append(cells)
    if interval_rows:
        lines += [
            "",
            "### Category scores with 95% intervals",
            "",
            "Bootstrapped over documents. A category whose interval overlaps another "
            "model's has not been shown to differ in this corpus.",
            "",
        ]
        lines += _table(["Model"] + [c.title() for c in categories], interval_rows)

    lines += ["", "### Separation", ""]

    deltas = boot.get("deltas") or {}
    if not deltas:
        lines.append("Only one model in this run: no comparison to make.")
    else:
        # Rendered in rank order, so the higher-scoring model is always on the
        # left and the delta reads as a lead rather than as a negative number.
        for i, left in enumerate(ranked):
            for right in ranked[i + 1 :]:
                entry = _delta(deltas, left, right)
                if entry is None:  # pragma: no cover - every pair is stored
                    continue
                verdict = (
                    "separated at 95%"
                    if entry.get("significant")
                    else "**not** separated at 95% — the interval spans zero, so this "
                    "run does not tell them apart"
                )
                lines.append(
                    f"- `{left}` over `{right}`: {_fmt(entry['point'])} "
                    f"[{_fmt(entry['lo'])}, {_fmt(entry['hi'])}] — {verdict}."
                )
    lines.append("")
    return lines


def _delta(deltas: Mapping[str, Any], left: str, right: str) -> dict[str, Any] | None:
    """The left-minus-right delta, flipping the stored pair if need be."""
    if f"{left}|{right}" in deltas:
        return dict(deltas[f"{left}|{right}"])
    entry = deltas.get(f"{right}|{left}")
    if entry is None:
        return None
    flipped = dict(entry)
    flipped["point"] = -entry["point"]
    flipped["lo"], flipped["hi"] = -entry["hi"], -entry["lo"]
    return flipped


def _heat_section(df: pd.DataFrame, meta: Mapping[str, Any]) -> list[str]:
    by_format = scoring.indices(df, meta, by=("model", "format"))
    present = [f for f in FORMATS if f in set(df["format"].unique())]
    extra = sorted(set(df["format"].unique()) - set(FORMATS))
    columns = present + extra
    models = sorted(df["model"].unique().tolist())

    header = ["Model"] + columns
    rows = []
    for model in models:
        cells = [f"`{model}`"]
        for fmt in columns:
            try:
                value = float(by_format.loc[(model, fmt), "ai_tell_index"])
            except KeyError:
                cells.append(EM_DASH)
                continue
            cells.append(f"{_heat(value)} {_fmt(value, 0)}")
        rows.append(cells)

    lines = [
        "## 2. Index by format",
        "",
        f"`{HEAT_GLYPHS}` runs 0-100 in equal steps of {100 // len(HEAT_GLYPHS)}. "
        "A blank cell is a format the model has no documents for.",
        "",
    ]
    lines += _table(header, rows)
    lines.append("")
    return lines


def _top_tells(
    df: pd.DataFrame, meta: Mapping[str, Any], ranked: Sequence[str]
) -> list[str]:
    thin = _model_evidence(df)
    lines = [
        "## 3. Loudest tells per model",
        "",
        "Ranked by mean document score. A row marked † is below the evidence floor "
        f"(fewer than {scoring.MIN_DOCS} documents, or fewer than "
        f"{scoring.MIN_OCCURRENCES} total occurrences for a count tell) and is "
        "reported as an observation, not a finding.",
        "",
    ]
    matrix = scoring.per_model_tell_matrix(df)
    for model in ranked:
        lines += [f"### `{model}`", ""]
        if model not in matrix.index:  # pragma: no cover - ranked comes from the matrix
            lines += ["No documents.", ""]
            continue
        series = matrix.loc[model].dropna()
        series = series[series > 0]
        order = sorted(series.index, key=lambda t: (-float(series[t]), t))[:TOP_TELLS]
        if not order:
            lines += ["No tell fired in this model's documents.", ""]
            continue
        rows = []
        for tell_id in order:
            rows_for_tell = df[(df["model"] == model) & (df["tell_id"] == tell_id)]
            unit = str(rows_for_tell["unit"].iloc[0])
            name = (meta.get(tell_id) or {}).get("name") or tell_id
            mark = " †" if (model, tell_id) in thin else ""
            signal = _signal(unit, rows_for_tell)
            # Judge tells may be measured on a sample while Tier-1 reads the
            # whole corpus, so their n is not the corpus n and a reader
            # comparing two rows in this table has to be told which is which.
            if str(rows_for_tell["method"].iloc[0]) == "judge":
                signal += f" (n={len(rows_for_tell)} docs)"
            rows.append(
                [
                    f"`{tell_id}`{mark}",
                    _cell(str(name)),
                    _cell(signal),
                    _fmt(series[tell_id], 3),
                    _cell(_exemplar(rows_for_tell)) or EM_DASH,
                ]
            )
        lines += _table(["Tell", "Name", "Signal", "Score", "Exemplar"], rows)
        lines.append("")
    return lines


def _evidence_section(df: pd.DataFrame) -> list[str]:
    flags = scoring.min_evidence_flags(df)
    total = len(flags)
    flagged = flags[flags["flagged"]] if total else flags
    lines = ["## 4. Cells below the evidence floor", ""]
    if total == 0 or flagged.empty:
        lines += [
            f"None. All {total} model x format x tell cells clear both floors.",
            "",
        ]
        return lines

    thin_cells = (
        df.groupby(["model", "format"])["doc_id"].nunique().reset_index(name="n_docs")
    )
    under_docs = thin_cells[thin_cells["n_docs"] < scoring.MIN_DOCS]

    lines += [
        f"{len(flagged)} of {total} model x format x tell cells fall below a floor. "
        "No ranked claim in this scorecard rests on one.",
        "",
    ]
    if not under_docs.empty:
        lines += [
            f"**Below the {scoring.MIN_DOCS}-document floor** — every tell in these "
            "cells is affected:",
            "",
        ]
        lines += _table(
            ["Model", "Format", "Docs"],
            [
                [f"`{r.model}`", str(r.format), str(int(r.n_docs))]
                for r in under_docs.sort_values(["model", "format"]).itertuples()
            ],
        )
        lines.append("")

    occurrence_only = flagged[flagged["reason"].str.startswith("occurrences")]
    if not occurrence_only.empty:
        lines += [
            f"A further {len(occurrence_only)} count cells clear the document floor "
            f"but hold fewer than {scoring.MIN_OCCURRENCES} occurrences.",
            "",
        ]
    return lines


def _dormant_section(df: pd.DataFrame, meta: Mapping[str, Any]) -> list[str]:
    dormant = scoring.dormant_tells(df)
    scored = sorted(df["tell_id"].unique().tolist())
    lines = ["## 5. Dormant tells", ""]
    if not dormant:
        lines += [f"None. All {len(scored)} scored tells fired somewhere.", ""]
        return lines
    lines += [
        f"{len(dormant)} of {len(scored)} scored tells fired in no document by any "
        "model. They stay in the index denominator on purpose — dropping them "
        "would make the score depend on which tells happened to fire, so two runs "
        "over different corpora would not be comparable — but they contribute "
        "nothing but dilution, and a tell that stays dormant across corpora is a "
        "candidate for deprecation.",
        "",
    ]
    lines += ["  " + ", ".join(f"`{t}`" for t in dormant), ""]
    return lines


def _bootstrap_line(boot: Mapping[str, Any]) -> str:
    if not boot:
        return f"{EM_DASH} (nothing to resample)"
    return (
        f"{boot.get('n', EM_DASH)} replicates, seed {boot.get('seed', EM_DASH)}, "
        f"{boot.get('method', EM_DASH)}"
    )


def _run_stats(
    manifest: Mapping[str, Any],
    df: pd.DataFrame,
    boot: Mapping[str, Any],
    ranked: Sequence[str],
) -> list[str]:
    corpus = manifest.get("corpus") or {}
    registry = manifest.get("registry") or {}
    judge = manifest.get("judge") or {}
    rows = [
        ["Documents", str(corpus.get("n_docs", 0))],
        ["Words", f"{int(corpus.get('n_words', 0)):,}"],
        [
            "Per model",
            ", ".join(f"{m}: {n}" for m, n in sorted((corpus.get("per_model") or {}).items()))
            or EM_DASH,
        ],
        ["Corpus hash", f"`{str(corpus.get('corpus_hash', ''))[:16]}`"],
        ["Registry", f"v{registry.get('version')} `{str(registry.get('content_hash',''))[:16]}`"],
        ["Tells scored", str(registry.get("n_scored", 0))],
    ]
    if judge.get("enabled"):
        rows += _judge_rows(judge, df)
    else:
        rows.append(
            [
                "Judge tells skipped",
                f"{registry.get('judge_skipped', 0)} (Tier-2, arrives in M6)",
            ]
        )
    rows += [
        ["Bootstrap", _bootstrap_line(boot)],
        [
            "Weights",
            ", ".join(f"{c} {w:.2f}" for c, w in sorted(scoring.CATEGORY_WEIGHTS.items())),
        ],
    ]
    lines = ["## 6. Run", ""]
    lines += _table(["Field", "Value"], rows)
    if judge.get("enabled"):
        lines += [
            "",
            "Tier-2 judge tells were scored. The judge never rated anything: it "
            "extracted verbatim quotes, every quote was checked against the "
            "document it came from, and the rubric's criteria were applied in "
            "code. A judge tell is only included when its latest calibration "
            "report clears "
            f"{float(judge.get('gate') or 0.9):.2f} agreement on its 20 labelled "
            "snippets; any tell that did not is named above, and while one is "
            "missing the index is a floor, not a total.",
        ]
    else:
        lines += [
            "",
            "Only the deterministic tells ran: regex and statistic. Judge tells are "
            "counted above and scored in M6; until then the index is a floor, not a "
            "total.",
        ]
    return lines


def _judge_rows(judge: Mapping[str, Any], df: pd.DataFrame) -> list[list[str]]:
    """The judge block of the run table.

    Everything here is a property of the evidence, not of the session that
    produced it. Call counts and cache hit rates are deliberately *not* in the
    scorecard, only in the manifest: a cold first run and a warm replay do the
    same arithmetic over the same answers but pay for them differently, and a
    scorecard that recorded the difference would stop being byte-reproducible —
    which is the one thing `report --verify` exists to check.
    """
    scored = judge.get("tells_scored") or []
    skipped = judge.get("tells_skipped") or {}
    hallucination = judge_hallucination_rate(df)
    rate = hallucination.get("rate")
    disagreement = judge_disagreements(df)
    d_rate = disagreement.get("rate")
    flagged = disagreement.get("over_threshold") or []

    return [
        ["Judge model", f"`{judge.get('model', EM_DASH)}`"],
        ["Judge protocol", f"v{judge.get('protocol_version', EM_DASH)}"],
        [
            "Judge tells scored",
            f"{len(scored)}: " + (", ".join(f"`{t}`" for t in scored) or EM_DASH),
        ],
        [
            "Judge tells skipped",
            f"{len(skipped)}: "
            + (
                _cell("; ".join(f"`{t}` ({why})" for t, why in sorted(skipped.items())))
                or "none"
            ),
        ],
        [
            "Hallucinated quotes",
            f"{hallucination.get('hallucinated', 0)} of "
            f"{hallucination.get('extracted', 0)} extracted"
            + (f" ({100.0 * float(rate):.1f}%)" if rate is not None else ""),
        ],
        [
            "Judge sample",
            (
                f"{(judge.get('sample') or {}).get('n_selected', 0)} of the corpus, "
                f"seed {(judge.get('sample') or {}).get('seed')} — judge tells are "
                "measured on these documents only"
                if judge.get("sample")
                else "whole corpus"
            ),
        ],
        [
            "Judge/code disagreement",
            f"{disagreement.get('total', 0)} of "
            f"{disagreement.get('adjudicated', 0)} adjudicated spans"
            + (f" ({100.0 * float(d_rate):.1f}%)" if d_rate is not None else "")
            + (
                " — over threshold: " + _cell(", ".join(f"`{t}`" for t in flagged))
                if flagged
                else ""
            ),
        ],
    ]


# --- orchestration -----------------------------------------------------------


def _default_runs_root(out_root: Path | None, run_dir: Path | None) -> Path:
    """Where calibration reports are looked for when the caller did not say."""
    if out_root is not None:
        return Path(out_root)
    if run_dir is not None:
        return Path(run_dir).parent
    return Path(__file__).resolve().parent.parent / "runs"


def _judge_setup(
    judge: bool,
    judge_model: str | None,
    judge_tells: Sequence[str] | None,
    judge_cache_only: bool,
    tells: Sequence[Any],
    runs_root: Path,
) -> tuple[Any, list[Any], dict[str, Any]]:
    """Resolve the judge, apply the calibration gate, and report what it cost.

    Returns (backend, tells-to-score, manifest section). Without `judge` the
    tells come back untouched and the section says so, which is what keeps a
    Tier-1 run byte-identical to the way M5 wrote it.
    """
    tells = list(tells)
    if not judge:
        return None, tells, {"enabled": False}

    from telltale.judge import build_backend
    from telltale.judge import calibrate as calibration
    from telltale.judge import protocol as judge_protocol
    from telltale.judge.transport import JUDGE_SYSTEM_PROMPT_SHA256, resolve_judge

    model = judge_model or resolve_judge()

    if judge_tells is not None:
        # A replay. The set is fixed by the run being reproduced, not by whatever
        # has been calibrated since, or `verify` would fail whenever a tell was
        # calibrated between the original run and the check.
        wanted = set(judge_tells)
        skipped = {
            t.id: "not in the run's judge tell list"
            for t in tells
            if t.method == "judge" and t.id not in wanted
        }
        kept = [t for t in tells if t.method != "judge" or t.id in wanted]
    else:
        kept, skipped = calibration.gate_tells(tells, runs_root, judge_model=model)
        if skipped:
            names = ", ".join(sorted(skipped))
            warnings.warn(
                f"judge tells excluded for want of calibration: {names}. "
                "Run `telltale judge calibrate --tell <id>` to admit them; until "
                "then the index is a floor, not a total.",
                stacklevel=2,
            )

    backend = build_backend(model=model, cache_only=judge_cache_only)
    scored_ids = sorted(t.id for t in kept if t.method == "judge")
    section = {
        "enabled": True,
        "model": model,
        "protocol_version": judge_protocol.PROTOCOL_VERSION,
        "system_prompt_sha256": JUDGE_SYSTEM_PROMPT_SHA256,
        "cache_only": bool(judge_cache_only),
        "tells_scored": scored_ids,
        "tells_skipped": dict(sorted(skipped.items())),
        "calibration": calibration.calibration_scores(
            scored_ids, runs_root, judge_model=model
        ),
        "gate": calibration.GATE,
        "consistency_audit": None,
    }
    return backend, kept, section


def _judge_probe(model: str) -> Any:
    """A cheap liveness check the breaker uses to decide the network is back."""

    def probe() -> bool:
        from telltale.judge.transport import probe_judge

        return probe_judge(model)

    return probe


def _judge_run_stats(backend: Any) -> dict[str, Any]:
    """What this run spent: live calls, parse retries, and cache traffic.

    Manifest only. These numbers describe the session, not the measurement, and
    they differ between a cold run and a warm replay of the same evidence — see
    `_judge_rows` for why that keeps them out of the scorecard.
    """
    client = backend.client
    cache_stats = dict(client.cache.stats.as_dict())
    transport_stats = dict(client.transport.stats.as_dict())
    return {
        "calls": transport_stats,
        "cache": cache_stats,
        "live_calls": int(client.stats.get("live_calls", 0)),
    }


#: Above this share of a tell's adjudicated spans, judge-vs-code disagreement stops
#: being noise and starts being a message about the rubric.
DISAGREEMENT_WARN_RATE = 0.20


def judge_disagreements(df: pd.DataFrame) -> dict[str, Any]:
    """Where the judge's own verdict and the code's decision parted company.

    Recorded per detection since M6 and rolled up here, because the per-row
    number is the one nobody reads. The rate is the interesting quantity: a
    judge that keeps saying "not an instance" about spans whose criteria are all
    satisfied is telling us something the rubric has no letter for — it feels an
    exclusion it cannot name. That is precisely the drift the calibration gate
    cannot see, because the gate only asks whether the final answer was right on
    twenty snippets someone wrote on purpose.

    Denominator is every adjudicated span, true and false alike. It used to be
    the true ones only, which made the rate uninterpretable: a disagreement is
    recorded when the judge's own verdict parts from what the criteria compute,
    and that happens just as often on a span the code scored false. Dividing
    those disagreements by the true count alone mixed two populations and could
    exceed 1.0 — a tell where the judge said "not an instance" about ten spans
    the code counted zero of has no rate at all under the old denominator, and
    a tell with two true spans and eight false ones reported 100% when the real
    figure was 20%.
    """
    empty = {"total": 0, "adjudicated": 0, "rate": None, "per_tell": {}, "over_threshold": []}
    if df.empty or "detail" not in df.columns:
        return empty

    per_tell: dict[str, dict[str, Any]] = {}
    for row in df.loc[df["method"] == "judge"].itertuples():
        detail = row.detail
        if not isinstance(detail, dict):
            continue
        entry = per_tell.setdefault(
            str(row.tell_id), {"disagreements": 0, "adjudicated": 0, "rate": None}
        )
        entry["disagreements"] += int(detail.get("judge_disagreements") or 0)
        entry["adjudicated"] += int(detail.get("adjudicated_true") or 0) + int(
            detail.get("adjudicated_false") or 0
        )

    over: list[str] = []
    for tell_id, entry in per_tell.items():
        counted = entry["adjudicated"]
        entry["rate"] = (entry["disagreements"] / counted) if counted else None
        if entry["rate"] is not None:
            if entry["rate"] > DISAGREEMENT_WARN_RATE:
                over.append(tell_id)
        elif entry["disagreements"]:
            # Nothing adjudicated, yet disagreements were recorded. Under the
            # corrected denominator this should be unreachable — a disagreement
            # is only counted while adjudicating a span — so if it happens the
            # accounting itself is broken, which is worth flagging rather than
            # hiding behind a division that could not be performed.
            entry["rate"] = None
            over.append(tell_id)

    total = sum(e["disagreements"] for e in per_tell.values())
    counted = sum(e["adjudicated"] for e in per_tell.values())
    return {
        "total": total,
        "adjudicated": counted,
        "rate": (total / counted) if counted else None,
        "threshold": DISAGREEMENT_WARN_RATE,
        "per_tell": dict(sorted(per_tell.items())),
        "over_threshold": sorted(over),
    }


def judge_hallucination_rate(df: pd.DataFrame) -> dict[str, Any]:
    """Quotes the judge produced that were not in the text it was shown.

    Reported as a rate rather than a count because the denominator matters: two
    bad quotes out of four is a broken instrument, two out of four hundred is
    noise, and the count alone cannot tell them apart.
    """
    if df.empty or "detail" not in df.columns:
        return {"extracted": 0, "hallucinated": 0, "rate": None}
    extracted = 0
    hallucinated = 0
    for detail in df.loc[df["method"] == "judge", "detail"]:
        if not isinstance(detail, dict):
            continue
        extracted += int(detail.get("extracted") or 0)
        hallucinated += int(detail.get("hallucinated") or 0)
    return {
        "extracted": extracted,
        "hallucinated": hallucinated,
        "rate": (hallucinated / extracted) if extracted else None,
    }


def score_run(
    corpus_root: Path,
    registry_path: Path,
    out_root: Path | None = None,
    run_dir: Path | None = None,
    include_candidates: bool = False,
    cli_args: Sequence[str] | None = None,
    bootstrap_n: int = 1000,
    seed: int = 7,
    run_id: str | None = None,
    judge: bool = False,
    judge_model: str | None = None,
    judge_tells: Sequence[str] | None = None,
    judge_cache_only: bool = False,
    runs_root: Path | None = None,
    progress: Any | None = None,
    judge_workers: int = 1,
    judge_ceiling: int = 6,
    judge_sample: int | None = None,
    judge_sample_seed: int = 7,
    judge_doc_list: Sequence[str] | None = None,
    judge_missing_ok: Sequence[tuple[str, str]] | None = None,
    notes: Sequence[str] | None = None,
) -> Path:
    """Score a corpus and write the four outputs plus the manifest.

    Returns the run directory. Either `out_root` (a `<run_id>` directory is
    created inside it) or `run_dir` (written to directly, which is what verify
    uses) must be given.

    With `judge=True` the Tier-2 tells are scored as well, but only the ones
    whose latest calibration report clears the gate; the rest are skipped loudly
    and named in the manifest. `judge_tells` overrides the gate with an explicit
    list, which is how `manifest.verify` replays exactly the set the original
    run scored rather than whatever has been calibrated since.
    """
    corpus_root = Path(corpus_root)
    registry = Registry(Path(registry_path))
    docs = load_corpus(corpus_root)
    tells = registry.active_tells(include_candidates=include_candidates)

    backend, tells, judge_section = _judge_setup(
        judge=judge,
        judge_model=judge_model,
        judge_tells=judge_tells,
        judge_cache_only=judge_cache_only,
        tells=tells,
        runs_root=Path(runs_root) if runs_root is not None else _default_runs_root(out_root, run_dir),
    )

    sample = None
    if backend is not None and (judge_sample or judge_doc_list):
        from telltale.judge import sampling

        sample = (
            sampling.sample_from_list(docs, judge_doc_list)
            if judge_doc_list
            else sampling.stratified_sample(docs, size=judge_sample, seed=judge_sample_seed)
        )
        judge_section["sample"] = {
            k: v for k, v in sample.as_dict().items() if k != "strata"
        }

    controller = None
    if backend is not None and judge_workers > 1:
        from telltale.judge.sweep import SweepController, SweepPolicy

        controller = SweepController(
            policy=SweepPolicy(workers=judge_workers, ceiling=judge_ceiling),
            total=sum(1 for t in tells if t.method == "judge")
            * (len(sample.doc_ids) if sample is not None else len(docs)),
            emit=progress or (lambda line: None),
            # The resolved model, not the requested one: `judge_model` may be
            # None and settled by the allowlist inside `_judge_setup`, and a
            # probe against None would report an outage that is not happening.
            probe=_judge_probe(backend.client.model),
        )
        # Without this the progress line reports "0 calls" forever: the counter
        # lives on the controller and the calls happen inside the client, and
        # nothing joined the two. A rate of zero next to visible progress is
        # worse than no rate at all — it reads as a stalled sweep.
        backend.client.on_call = controller.record_call
    df = scoring.detect_all(
        docs, tells, judge=backend, progress=progress,
        workers=max(1, judge_workers), controller=controller,
        judge_docs=sample.doc_ids if sample is not None else None,
        judge_missing_ok=judge_missing_ok,
    )
    df = scoring.normalize(df, tells)
    judge_skipped = scoring.judge_tell_ids(tells) if backend is None else []
    scored = [t for t in tells if t.method != "judge" or backend is not None]

    if backend is not None:
        judge_section.update(_judge_run_stats(backend))
        judge_section["hallucination"] = judge_hallucination_rate(df)
        judge_section["disagreements"] = judge_disagreements(df)
        judge_errors = list(df.attrs.get("judge_errors") or [])
        judge_section["errors"] = {
            "count": len(judge_errors),
            "sample": judge_errors[:20],
        }
        judge_section["concurrency"] = {
            "breaker_trips": controller.breaker_trips if controller is not None else 0,
            "workers_start": judge_workers,
            "ceiling": judge_ceiling,
            "workers_end": controller.gate.capacity if controller is not None else 1,
            "stopped": controller.stop_reason if controller is not None else None,
        }

    pairing = scoring.pairing_summary(df)
    manifest = build_manifest(
        docs=docs,
        registry=registry,
        scored_tells=scored,
        corpus_root=corpus_root,
        judge_skipped=judge_skipped,
        include_candidates=include_candidates,
        cli_args=cli_args,
        bootstrap={
            "n": bootstrap_n,
            "seed": seed,
            "method": pairing["method"],
            "n_prompts": pairing["n_prompts"],
        },
        run_id=run_id,
        judge=judge_section,
        notes=notes,
    )

    if run_dir is None:
        if out_root is None:
            raise ValueError("score_run needs either out_root or run_dir")
        run_dir = Path(out_root) / manifest["run_id"]
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    if sample is not None:
        from telltale.judge import sampling

        sampling.write_sample(sample, run_dir)

    write_scores_jsonl(df, run_dir / SCORES_NAME)
    write_matrices(df, run_dir)
    write_manifest(manifest, run_dir)
    render_scorecard(run_dir)
    return run_dir


__all__ = [
    "MATRIX_BY_FORMAT_NAME",
    "MATRIX_NAME",
    "SCORECARD_NAME",
    "SCORES_NAME",
    "read_scores_jsonl",
    "render_scorecard",
    "score_run",
    "write_matrices",
    "write_scores_jsonl",
]
