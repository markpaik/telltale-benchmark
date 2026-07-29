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
            rows.append(
                [
                    f"`{tell_id}`{mark}",
                    _cell(str(name)),
                    _cell(_signal(unit, rows_for_tell)),
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
        [
            "Judge tells skipped",
            f"{registry.get('judge_skipped', 0)} (Tier-2, arrives in M6)",
        ],
        ["Bootstrap", _bootstrap_line(boot)],
        [
            "Weights",
            ", ".join(f"{c} {w:.2f}" for c, w in sorted(scoring.CATEGORY_WEIGHTS.items())),
        ],
    ]
    lines = ["## 6. Run", ""]
    lines += _table(["Field", "Value"], rows)
    lines += [
        "",
        "Only the deterministic tells ran: regex and statistic. Judge tells are "
        "counted above and scored in M6; until then the index is a floor, not a "
        "total.",
    ]
    return lines


# --- orchestration -----------------------------------------------------------


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
) -> Path:
    """Score a corpus and write the four outputs plus the manifest.

    Returns the run directory. Either `out_root` (a `<run_id>` directory is
    created inside it) or `run_dir` (written to directly, which is what verify
    uses) must be given.
    """
    corpus_root = Path(corpus_root)
    registry = Registry(Path(registry_path))
    docs = load_corpus(corpus_root)
    tells = registry.active_tells(include_candidates=include_candidates)

    df = scoring.detect_all(docs, tells)
    df = scoring.normalize(df, tells)
    judge_skipped = scoring.judge_tell_ids(tells)
    scored = [t for t in tells if t.method != "judge"]

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
    )

    if run_dir is None:
        if out_root is None:
            raise ValueError("score_run needs either out_root or run_dir")
        run_dir = Path(out_root) / manifest["run_id"]
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

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
