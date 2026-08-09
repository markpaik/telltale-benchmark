#!/usr/bin/env python3
"""Does the R16 extraction gate keep the spans the old prompt actually counted?

Ruling R16 moved criterion (c) of `rht.rule-of-three` into the stage-1 prompt so
the extractor stops proposing every three-item structure in business prose. That
buys back roughly half the Tier-2 budget and risks exactly one thing: silently
losing real instances. This script measures that risk before the revision ships.

The method is the cheap one the cache makes possible. The authoritative run
counted 73 spans for this tell. Each of those spans sits in a chunk, and that
chunk's stage-1 answer under the old rubric is already paid for and on disk. So:
re-ask the revised stage-1 question on exactly those chunks, and check how many
of the 73 come back.

Two numbers decide it, both set by R16:

* **recall** — the share of counted spans a revised extraction re-proposes,
  compared by whitespace-normalized containment. Gate is 0.70. Between 0.50 and
  0.70 the misses go to the coordinator. Below 0.50 the revision is abandoned for
  option 2, the deterministic pre-filter.
* **proposal volume** — mean proposed spans per chunk, new against cached. Gate
  is a fall of at least 50%, because a revision that keeps recall by proposing
  everything has changed nothing.

Both thresholds are calibrated against the 0.62 re-ask stability baseline in
SHAKEDOWN §2.7: this tell does not reproduce its own span set exactly on two
identical calls, so a recall figure in the nineties was never the target.

Containment is scored in both directions and reported separately. A revised call
that quotes the whole sentence where the run counted a clause is the same find,
and so is the reverse; the strict direction (the counted span inside a new
proposal) is reported alongside so a reader can take the harder number.

    python3 scripts/rule_of_three_recall.py --dry-run       # zero live calls
    python3 scripts/rule_of_three_recall.py --workers 2     # the live pass

The live pass writes its answers to the judge cache under rubric_version 2,
which is not a side effect but the point: the sweep that follows replays them
free.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(REPO_ROOT))

from telltale.corpus import Doc, load_corpus  # noqa: E402
from telltale.judge import cache as cache_mod  # noqa: E402
from telltale.judge import protocol  # noqa: E402
from telltale.judge.cache import JudgeCache, JudgeClient  # noqa: E402
from telltale.registry import Registry, Tell  # noqa: E402

TELL_ID = "rht.rule-of-three"

#: The rubric version the authoritative run judged under. The cached stage-1
#: answers this script compares against are keyed on it, and R16 bumped the
#: registry to 2 — so the old answers have to be asked for by number, not by
#: whatever the registry says today.
OLD_RUBRIC_VERSION = 1

#: R16's gates.
RECALL_PASS = 0.70
RECALL_REVIEW = 0.50
VOLUME_DROP_REQUIRED = 0.50

DEFAULT_RUNS = REPO_ROOT / "runs"
DEFAULT_CORPUS = REPO_ROOT / "corpus"
DEFAULT_REGISTRY = REPO_ROOT / "registry" / "tells.yaml"
DEFAULT_CACHE = REPO_ROOT / "cache" / "judge"
DEFAULT_OUT = REPO_ROOT / "runs" / "calibration"

_RUN_DIR = re.compile(r"`(\d{8}T\d{6}Z-[0-9a-f]+-[0-9a-f]+)`")


# --- finding the run ---------------------------------------------------------


def authoritative_run(runs_root: Path = DEFAULT_RUNS) -> Path:
    """The run `runs/README.md` names as the reference, not the newest directory.

    Reading the pointer rather than sorting by timestamp is deliberate: a run
    that superseded another is a decision somebody wrote down, and a script that
    guessed would compare against evidence nobody nominated.
    """
    readme = Path(runs_root) / "README.md"
    text = readme.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "reference run" not in line:
            continue
        found = _RUN_DIR.search(line)
        if found:
            return Path(runs_root) / found.group(1)
    # The pointer is written as a bolded name on its own line above the sentence
    # in some revisions; fall back to the first run-shaped name in the file.
    found = _RUN_DIR.search(text)
    if not found:
        raise SystemExit(f"{readme} names no authoritative run")
    return Path(runs_root) / found.group(1)


# --- the counted spans -------------------------------------------------------


def counted_spans(run_dir: Path, tell_id: str = TELL_ID) -> dict[str, list[str]]:
    """Every adjudicated-true span the run counted, by document.

    Read from `scores.jsonl` rather than from the cache: the cache holds every
    answer the judge gave, and what this script has to reproduce is the subset
    the code counted after applying the rubric arithmetic.
    """
    path = Path(run_dir) / "scores.jsonl"
    out: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("tell_id") != tell_id or row.get("method") != "judge":
            continue
        quotes = [
            str(match.get("quote") or "")
            for match in row.get("matches") or []
            if match.get("counted")
        ]
        if quotes:
            out[str(row["doc_id"])] = quotes
    return out


@dataclass
class TargetChunk:
    """One chunk that produced counted spans, and what it cost to get them."""

    doc_id: str
    chunk_index: int
    chunk_sha256: str
    text: str = field(repr=False, default="")
    counted: list[str] = field(default_factory=list)
    cached_proposals: list[str] = field(default_factory=list)
    cached_answer_found: bool = False

    @property
    def label(self) -> str:
        return f"{self.doc_id}#{self.chunk_index}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "chunk_index": self.chunk_index,
            "chunk_sha256": self.chunk_sha256[:16],
            "counted_spans": len(self.counted),
            "cached_proposals": len(self.cached_proposals),
            "cached_answer_found": self.cached_answer_found,
        }


def _normalized_proposals(payload: dict[str, Any], text: str) -> list[str]:
    """The stage-1 spans an answer supports, verified against the chunk."""
    out: list[str] = []
    for span in protocol.extraction_spans(payload):
        match = protocol.verify_quote(span["quote"], text)
        if match is not None:
            out.append(match.normalized)
    return out


def target_chunks(
    docs: Sequence[Doc],
    tell: Tell,
    spans_by_doc: dict[str, list[str]],
    cache: JudgeCache,
    judge_model: str,
) -> tuple[list[TargetChunk], list[dict[str, str]]]:
    """The chunks holding the counted spans, plus any span that cannot be placed.

    A span is placed by quote verification against each chunk of the document, in
    the chunker's own order, which is how the run found it in the first place. A
    span that verifies nowhere is reported rather than dropped: it would silently
    lower recall, and the reason for it — a chunker change, a corpus edit — is
    something a reader needs to see.
    """
    by_id = {doc.doc_id: doc for doc in docs}
    chunks: dict[tuple[str, int], TargetChunk] = {}
    unplaced: list[dict[str, str]] = []

    for doc_id in sorted(spans_by_doc):
        doc = by_id.get(doc_id)
        if doc is None:
            for quote in spans_by_doc[doc_id]:
                unplaced.append({"doc_id": doc_id, "quote": quote, "why": "document not in corpus"})
            continue
        doc_chunks = protocol.judge_view_text(tell, doc)
        for quote in spans_by_doc[doc_id]:
            placed = False
            for chunk in doc_chunks:
                if protocol.verify_quote(quote, chunk.text) is None:
                    continue
                key = (doc_id, chunk.index)
                target = chunks.get(key)
                if target is None:
                    target = TargetChunk(
                        doc_id=doc_id,
                        chunk_index=chunk.index,
                        chunk_sha256=chunk.sha256,
                        text=chunk.text,
                    )
                    chunks[key] = target
                target.counted.append(quote)
                placed = True
                break
            if not placed:
                unplaced.append(
                    {"doc_id": doc_id, "quote": quote, "why": "quote verifies in no chunk"}
                )

    ordered = [chunks[key] for key in sorted(chunks)]
    for target in ordered:
        cached = cache.get(
            cache_mod.cache_key(
                target.chunk_sha256,
                tell.id,
                OLD_RUBRIC_VERSION,
                judge_model,
                cache_mod.EXTRACT,
            )
        )
        if cached is not None:
            target.cached_answer_found = True
            target.cached_proposals = _normalized_proposals(cached, target.text)
    return ordered, unplaced


# --- comparing ---------------------------------------------------------------


def contains(haystack: str, needle: str) -> bool:
    """Whitespace-normalized containment, the comparison R16 names."""
    return bool(needle) and protocol.normalize_ws(needle) in protocol.normalize_ws(haystack)


def match_counted_span(quote: str, proposals: Iterable[str]) -> dict[str, bool]:
    """Whether a counted span survives, by each direction of containment."""
    proposals = list(proposals)
    strict = any(contains(proposal, quote) for proposal in proposals)
    loose = any(contains(quote, proposal) for proposal in proposals)
    return {"strict": strict, "either": strict or loose}


def verdict(recall: float, volume_drop: float) -> str:
    """R16's decision, in R16's words."""
    if recall < RECALL_REVIEW:
        return "fallback-to-prefilter"
    if recall < RECALL_PASS:
        return "coordinator-review"
    if volume_drop < VOLUME_DROP_REQUIRED:
        return "recall-passed-volume-failed"
    return "pass"


# --- the run -----------------------------------------------------------------


def _extract(client: JudgeClient, tell: Tell, target: TargetChunk) -> list[str]:
    payload, _, _ = client.ask(
        cache_mod.EXTRACT,
        target.chunk_sha256,
        tell.id,
        tell.rubric_version,
        protocol.build_extraction_prompt(tell, target.text),
    )
    return _normalized_proposals(payload, target.text)


def replay(
    targets: Sequence[TargetChunk],
    tell: Tell,
    client: JudgeClient,
    workers: int = 2,
    progress: Any | None = None,
) -> dict[str, list[str]]:
    """The revised stage-1 answer for every target chunk, by chunk label."""
    results: dict[str, list[str]] = {}

    def work(target: TargetChunk) -> tuple[str, list[str]]:
        proposals = _extract(client, tell, target)
        if progress is not None:
            progress(f"RECALL {target.label}: {len(proposals)} proposals")
        return target.label, proposals

    if workers <= 1:
        for target in targets:
            label, proposals = work(target)
            results[label] = proposals
        return results

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for label, proposals in pool.map(work, targets):
            results[label] = proposals
    return results


def build_report(
    targets: Sequence[TargetChunk],
    new_proposals: dict[str, list[str]],
    unplaced: Sequence[dict[str, str]],
    run_dir: Path,
    tell: Tell,
    judge_model: str,
) -> dict[str, Any]:
    """The numbers R16 asks for, with the per-span evidence under them."""
    spans: list[dict[str, Any]] = []
    for target in targets:
        proposals = new_proposals.get(target.label, [])
        for quote in target.counted:
            hit = match_counted_span(quote, proposals)
            spans.append(
                {
                    "doc_id": target.doc_id,
                    "chunk": target.label,
                    "quote": quote,
                    "re_proposed_strict": hit["strict"],
                    "re_proposed": hit["either"],
                }
            )

    counted_total = len(spans) + len(unplaced)
    kept = sum(1 for span in spans if span["re_proposed"])
    kept_strict = sum(1 for span in spans if span["re_proposed_strict"])
    recall = kept / counted_total if counted_total else float("nan")
    recall_strict = kept_strict / counted_total if counted_total else float("nan")

    with_cache = [t for t in targets if t.cached_answer_found]
    old_mean = (
        sum(len(t.cached_proposals) for t in with_cache) / len(with_cache)
        if with_cache
        else float("nan")
    )
    new_counts = [len(new_proposals.get(t.label, [])) for t in with_cache]
    new_mean = sum(new_counts) / len(new_counts) if new_counts else float("nan")
    drop = 1.0 - (new_mean / old_mean) if old_mean else float("nan")

    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ruling": "R16",
        "tell_id": tell.id,
        "rubric_version_old": OLD_RUBRIC_VERSION,
        "rubric_version_new": tell.rubric_version,
        "run_dir": str(run_dir),
        "judge_model": judge_model,
        "gates": {
            "recall_pass": RECALL_PASS,
            "recall_review": RECALL_REVIEW,
            "volume_drop_required": VOLUME_DROP_REQUIRED,
        },
        "counted_spans": counted_total,
        "counted_spans_placed": len(spans),
        "target_chunks": len(targets),
        "chunks_with_cached_answer": len(with_cache),
        "recall": recall,
        "recall_strict": recall_strict,
        "re_proposed": kept,
        "missed": counted_total - kept,
        "proposals_per_chunk_old": old_mean,
        "proposals_per_chunk_new": new_mean,
        "proposals_per_chunk_drop": drop,
        "verdict": verdict(recall, drop),
        "unplaced_spans": list(unplaced),
        "spans": spans,
        "chunks": [t.as_dict() for t in targets],
    }


def summarize(report: dict[str, Any]) -> str:
    """The human-readable half. Numbers first, then what they decide."""

    def num(value: Any, fmt: str = "{:.2f}") -> str:
        try:
            return fmt.format(float(value))
        except (TypeError, ValueError):
            return "n/a"

    lines = [
        f"# rule-of-three recall check ({report['ruling']})",
        "",
        f"Generated {report['generated']} against `{report['run_dir']}`.",
        f"Rubric v{report['rubric_version_old']} -> v{report['rubric_version_new']}, "
        f"judge {report['judge_model']}.",
        "",
        f"- counted spans: {report['counted_spans']} "
        f"({report['counted_spans_placed']} placed in a chunk)",
        f"- target chunks: {report['target_chunks']} "
        f"({report['chunks_with_cached_answer']} with a cached stage-1 answer)",
        f"- recall: {num(report['recall'])} "
        f"(strict containment {num(report['recall_strict'])}), "
        f"gate {report['gates']['recall_pass']}",
        f"- proposals per chunk: {num(report['proposals_per_chunk_old'])} -> "
        f"{num(report['proposals_per_chunk_new'])} "
        f"({num(report['proposals_per_chunk_drop'], '{:.0%}')} down), "
        f"gate {report['gates']['volume_drop_required']:.0%}",
        f"- verdict: **{report['verdict']}**",
    ]
    missed = [s for s in report["spans"] if not s["re_proposed"]]
    if missed:
        lines += ["", f"## Spans the revision no longer proposes ({len(missed)})", ""]
        for span in missed[:40]:
            lines.append(f"- `{span['chunk']}` — {span['quote'][:160]}")
    if report["unplaced_spans"]:
        lines += ["", "## Counted spans that could not be placed in a chunk", ""]
        for span in report["unplaced_spans"]:
            lines.append(f"- `{span['doc_id']}` — {span['why']}: {span['quote'][:120]}")
    return "\n".join(lines) + "\n"


def dry_run_text(targets: Sequence[TargetChunk], unplaced: Sequence[dict[str, str]]) -> str:
    """What a live pass would ask, and what it would be compared against."""
    lines = [
        f"DRY RUN — {len(targets)} target chunks, "
        f"{sum(len(t.counted) for t in targets)} counted spans, no live calls",
        "  chunk                                        counted  cached-proposals",
    ]
    for target in targets:
        cached = (
            str(len(target.cached_proposals)) if target.cached_answer_found else "MISS"
        )
        lines.append(f"  {target.label:<44} {len(target.counted):>7}  {cached:>16}")
    with_cache = [t for t in targets if t.cached_answer_found]
    if with_cache:
        mean = sum(len(t.cached_proposals) for t in with_cache) / len(with_cache)
        lines.append(
            f"  cached mean proposals/chunk: {mean:.2f} over {len(with_cache)} chunks"
        )
    if unplaced:
        lines.append(f"  {len(unplaced)} counted spans could not be placed in a chunk:")
        for span in unplaced:
            lines.append(f"    {span['doc_id']}: {span['why']}")
    lines.append(f"  live calls a real pass would make: {len(targets)}")
    return "\n".join(lines)


def prepare(
    run_dir: Path,
    corpus_root: Path,
    registry_path: Path,
    cache_root: Path,
    judge_model: str,
) -> tuple[Tell, list[TargetChunk], list[dict[str, str]]]:
    """Everything the check needs before it decides whether to call anything."""
    tell = Registry(registry_path).get(TELL_ID)
    spans = counted_spans(run_dir)
    docs = [
        doc
        for doc in load_corpus(corpus_root)
        if doc.doc_id in spans
    ]
    targets, unplaced = target_chunks(
        docs, tell, spans, JudgeCache(cache_root), judge_model
    )
    return tell, targets, unplaced


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", type=Path, default=None, help="run dir (default: the one runs/README.md names)")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--model", default=None, help="judge model (default: the pinned one)")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="list the target chunks and their cached span counts; makes no live call",
    )
    args = parser.parse_args(argv)

    from telltale.judge.transport import JUDGE_MODEL_DEFAULT, CliJudgeTransport

    judge_model = args.model or JUDGE_MODEL_DEFAULT
    run_dir = args.run or authoritative_run(DEFAULT_RUNS)
    tell, targets, unplaced = prepare(
        run_dir, args.corpus, args.registry, args.cache, judge_model
    )

    if not targets:
        print("no target chunks: nothing counted, or the corpus is missing", file=sys.stderr)
        return 1

    if args.dry_run:
        print(dry_run_text(targets, unplaced))
        return 0

    client = JudgeClient(
        transport=CliJudgeTransport(model=judge_model),
        cache=JudgeCache(args.cache),
    )
    new_proposals = replay(
        targets,
        tell,
        client,
        workers=max(1, int(args.workers)),
        progress=lambda line: print(line, file=sys.stderr, flush=True),
    )
    report = build_report(targets, new_proposals, unplaced, run_dir, tell, judge_model)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"rule_of_three_recall_{stamp}.json"
    md_path = out_dir / f"rule_of_three_recall_{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(summarize(report), encoding="utf-8")
    print(summarize(report))
    print(f"report: {json_path}")
    print(f"summary: {md_path}")
    return 0 if report["verdict"] == "pass" else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
