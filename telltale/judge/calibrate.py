"""The gate a judge tell has to pass before its numbers count.

A rubric is a claim about what a judge will do. `calibration/<tell_id>.yaml`
turns that claim into something falsifiable: ten snippets that unambiguously
contain the pattern and ten that unambiguously do not, each labelled by hand.
`calibrate` runs the whole pipeline over all twenty — extraction, quote
verification, adjudication, the decision rule — and reports the share it got
right. Below 0.90 the tell does not ship, and `score --judge` refuses to include
it rather than quietly publishing a number nobody has checked.

Two things about the design are deliberate.

**Agreement is measured at the snippet level, not the span level.** A positive
snippet passes if at least one span survives adjudication; a negative passes if
none does. That is the same question the detector asks of a real document, so a
tell that calibrates at 0.95 has been tested on the decision it will actually
make — not on a proxy for it.

**The negatives are near misses.** Most of them contain something that looks
like the pattern and is caught by one of the rubric's own exclusions. A set of
obviously-clean negatives would calibrate at 1.00 and tell nobody anything; the
failure mode worth catching is a judge that fires on surface form, and only a
near miss catches it.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import yaml

from telltale.judge import protocol
from telltale.registry import Registry, Tell

#: The share of the 20 snippets a tell must get right to be scoreable.
GATE = 0.90

CALIBRATION_DIRNAME = "calibration"
REPORTS_SUBDIR = "calibration"


@dataclass(frozen=True)
class Snippet:
    """One hand-labelled passage."""

    id: str
    label: str  # "positive" | "negative"
    source: str  # "registry" | "synthetic"
    text: str
    note: str = ""

    @property
    def expected(self) -> bool:
        return self.label == "positive"


@dataclass
class SnippetOutcome:
    """What the pipeline made of one snippet."""

    id: str
    label: str
    source: str
    expected: bool
    observed: bool
    agree: bool
    detail: str = ""
    extracted: int = 0
    counted: int = 0
    hallucinated: int = 0
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CalibrationReport:
    """One tell's calibration run, and whether it clears the gate."""

    tell_id: str
    rubric_version: Any
    judge_model: str
    protocol_version: int
    n: int
    n_agree: int
    agreement: float
    passed: bool
    gate: float
    timestamp: str
    outcomes: list[SnippetOutcome] = field(default_factory=list)

    @property
    def failures(self) -> list[SnippetOutcome]:
        return [o for o in self.outcomes if not o.agree]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["outcomes"] = [o.as_dict() for o in self.outcomes]
        return data

    def summary(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        lines = [
            f"{mark}  {self.tell_id}  agreement {self.agreement:.2f} "
            f"({self.n_agree}/{self.n}, gate {self.gate:.2f}) "
            f"judge {self.judge_model} rubric v{self.rubric_version}"
        ]
        for outcome in self.failures:
            expected = "positive" if outcome.expected else "negative"
            observed = "present" if outcome.observed else "absent"
            lines.append(
                f"    MISS {outcome.id} (labelled {expected}, judged {observed}): "
                f"{outcome.detail}"
            )
        return "\n".join(lines)


# --- the sets ----------------------------------------------------------------


def calibration_root(project_root: Path | None = None) -> Path:
    root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
    return root / CALIBRATION_DIRNAME


def load_snippets(tell_id: str, root: Path | None = None) -> list[Snippet]:
    """Read one tell's labelled set. Missing file -> KeyError, not an empty set."""
    directory = Path(root) if root else calibration_root()
    path = directory / f"{tell_id}.yaml"
    if not path.is_file():
        raise KeyError(f"no calibration set for {tell_id}: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: list[Snippet] = []
    for entry in data.get("snippets") or []:
        if not isinstance(entry, dict):
            continue
        out.append(
            Snippet(
                id=str(entry.get("id") or ""),
                label=str(entry.get("label") or ""),
                source=str(entry.get("source") or "synthetic"),
                text=str(entry.get("text") or ""),
                note=str(entry.get("note") or ""),
            )
        )
    return out


def skeleton_parity_errors(text: str) -> list[str]:
    """Ways a hand-written mini-skeleton could not have come from `skeleton_view`.

    A structural snippet is an anchor for a doc-level tell, so it has to be the
    shape a real document renders to — otherwise calibration measures the judge
    against a representation the corpus never produces. Splicing labels onto a
    malformed outline satisfies the letter of that and not the substance, which
    is exactly what happened to `str.table-overuse`: nineteen of its twenty
    snippets claimed a single paragraph in the outline while printing two
    different ones in the trailer, a shape `doc_skeleton` cannot emit.

    So the invariants checked here are the ones that tie the outline to the
    trailer: the first `PARA:` line must open the FIRST PARAGRAPH, the last must
    open the LAST PARAGRAPH, and the closing label must sit on the last one.
    """
    errors: list[str] = []
    lines = text.split("\n")
    if not lines or not lines[0].startswith("SKELETON "):
        return ["does not start with a SKELETON header"]

    para_lines = [(i, l) for i, l in enumerate(lines) if l.startswith("PARA:")]

    def block(header: str) -> str:
        for i, line in enumerate(lines):
            if line.startswith(header):
                out = []
                for follow in lines[i + 1 :]:
                    if not follow.strip() or follow.startswith(
                        ("TABLES", "FIRST PARAGRAPH", "LAST PARAGRAPH")
                    ):
                        break
                    out.append(follow)
                return " ".join(out).strip()
        return ""

    first, last = block("FIRST PARAGRAPH"), block("LAST PARAGRAPH")
    if not para_lines:
        if first and first != "(none)":
            errors.append("outline has no PARA lines but a FIRST PARAGRAPH is printed")
        return errors

    def opener(para_line: str) -> str:
        body = para_line.split("|", 1)[1] if "|" in para_line else ""
        return body.split(protocol.CLOSING_PARA_NOTE)[0].strip()

    if first and not first.startswith(opener(para_lines[0][1])):
        errors.append(
            f"first PARA line {opener(para_lines[0][1])[:50]!r} does not open the "
            f"FIRST PARAGRAPH {first[:50]!r}"
        )
    if last and not last.startswith(opener(para_lines[-1][1])):
        errors.append(
            f"last PARA line {opener(para_lines[-1][1])[:50]!r} does not open the "
            f"LAST PARAGRAPH {last[:50]!r}"
        )
    if first and last and first != last and len(para_lines) < 2:
        errors.append(
            f"{len(para_lines)} PARA line(s) but FIRST and LAST PARAGRAPH differ"
        )

    labelled = [i for i, (_, l) in enumerate(para_lines) if protocol.CLOSING_PARA_NOTE in l]
    if labelled != [len(para_lines) - 1]:
        errors.append(
            f"closing label sits on PARA line(s) {labelled}, expected only the last "
            f"({len(para_lines) - 1})"
        )
    if protocol.LAST_PARAGRAPH_NOTE not in text:
        errors.append("LAST PARAGRAPH header is not labelled")
    if protocol._label_closing_paragraph(text) != text:
        errors.append("not idempotent under the production labeller")
    return errors


def lint_snippets(tell: Tell, snippets: Sequence[Snippet]) -> list[str]:
    """Structural problems with a set, before any judge call is paid for."""
    errors: list[str] = []
    ids = [s.id for s in snippets]
    if len(set(ids)) != len(ids):
        errors.append(f"{tell.id}: duplicate snippet ids")
    positives = [s for s in snippets if s.label == "positive"]
    negatives = [s for s in snippets if s.label == "negative"]
    if len(positives) != 10:
        errors.append(f"{tell.id}: {len(positives)} positives, expected 10")
    if len(negatives) != 10:
        errors.append(f"{tell.id}: {len(negatives)} negatives, expected 10")
    for snippet in snippets:
        if snippet.label not in {"positive", "negative"}:
            errors.append(f"{tell.id}/{snippet.id}: label {snippet.label!r}")
        if snippet.source not in {"registry", "synthetic"}:
            errors.append(f"{tell.id}/{snippet.id}: source {snippet.source!r}")
        if not snippet.text.strip():
            errors.append(f"{tell.id}/{snippet.id}: empty text")
        if tell.judge_view == "skeleton":
            for problem in skeleton_parity_errors(snippet.text):
                errors.append(f"{tell.id}/{snippet.id}: {problem}")
    return errors


# --- running -----------------------------------------------------------------


def run_snippet(tell: Tell, snippet: Snippet, backend: Any) -> SnippetOutcome:
    """The full pipeline over one snippet, as the detector would run it."""
    rule = protocol.rule_for(tell)
    if rule.kind == "structural":
        run = backend.structural_for_text(tell, snippet.text)
        observed = bool(run.present)
        detail = run.reason
        extracted = len(run.matches) + len(run.hallucinated)
        counted = 1 if observed else 0
        hallucinated = len(run.hallucinated)
    else:
        run = backend.spans_for_text(tell, snippet.text)
        observed = bool(run.counted)
        counted = len(run.counted)
        extracted = run.extracted
        hallucinated = len(run.hallucinated)
        if observed:
            detail = f"{counted} span(s) counted: " + "; ".join(
                q["quote"][:70] for q in run.counted[:2]
            )
        elif run.rejected or run.code_excluded:
            # Structural dispositions have to show up here by name. A snippet
            # that was rejected by the line classifier and one where the judge
            # found nothing to quote both end with nothing counted, and reading
            # the second for the first would hide the whole of protocol v3's
            # behaviour from the gate report it is supposed to be judged by.
            why = [str(r["why_not"]) for r in run.rejected[:3]]
            why += [
                f"({r['exclusion_triggered']}) by structure: {r['line_class']}"
                for r in run.code_excluded[:3]
            ]
            detail = "all spans rejected: " + "; ".join(why)
        else:
            detail = "no spans extracted"

    return SnippetOutcome(
        id=snippet.id,
        label=snippet.label,
        source=snippet.source,
        expected=snippet.expected,
        observed=observed,
        agree=observed == snippet.expected,
        detail=detail[:400],
        extracted=extracted,
        counted=counted,
        hallucinated=hallucinated,
        note=snippet.note,
    )


def calibrate(
    tell: Tell,
    backend: Any,
    snippets: Sequence[Snippet] | None = None,
    root: Path | None = None,
    gate: float = GATE,
) -> CalibrationReport:
    """Run every labelled snippet for one tell and score the agreement."""
    items = list(snippets) if snippets is not None else load_snippets(tell.id, root)
    outcomes = [run_snippet(tell, snippet, backend) for snippet in items]
    n = len(outcomes)
    agree = sum(1 for o in outcomes if o.agree)
    agreement = (agree / n) if n else 0.0
    return CalibrationReport(
        tell_id=tell.id,
        rubric_version=tell.rubric_version,
        judge_model=str(getattr(backend.client, "model", "unknown")),
        protocol_version=protocol.PROTOCOL_VERSION,
        n=n,
        n_agree=agree,
        agreement=agreement,
        passed=bool(n) and agreement >= gate,
        gate=gate,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        outcomes=outcomes,
    )


# --- reports on disk ---------------------------------------------------------


def report_path(runs_root: Path, tell_id: str, when: datetime | None = None) -> Path:
    stamp = (when or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    return Path(runs_root) / REPORTS_SUBDIR / f"{stamp}-{tell_id}.json"


def write_report(report: CalibrationReport, runs_root: Path) -> Path:
    path = report_path(runs_root, report.tell_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report.as_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def latest_report(
    tell_id: str, runs_root: Path, judge_model: str | None = None
) -> dict[str, Any] | None:
    """The most recent calibration report for a tell, by timestamp in the name.

    Filtered by judge model when one is given: a tell calibrated against
    claude-opus-4-6 has not been calibrated against claude-opus-4-8, and
    treating the two as interchangeable is exactly the silent instrument change
    the rest of this package works to prevent.
    """
    directory = Path(runs_root) / REPORTS_SUBDIR
    if not directory.is_dir():
        return None
    best: tuple[str, dict[str, Any]] | None = None
    for path in sorted(directory.glob(f"*-{tell_id}.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(data, dict) or data.get("tell_id") != tell_id:
            continue
        if judge_model and data.get("judge_model") != judge_model:
            continue
        stamp = str(data.get("timestamp") or path.name)
        if best is None or stamp >= best[0]:
            best = (stamp, data)
    return best[1] if best else None


def gate_tells(
    tells: Sequence[Tell],
    runs_root: Path,
    judge_model: str | None = None,
    gate: float = GATE,
) -> tuple[list[Tell], dict[str, str]]:
    """Split judge tells into "calibrated enough to score" and "not, because…".

    Non-judge tells pass through untouched. The refusal is loud on purpose: a
    judge tell that silently scores zero across a corpus is indistinguishable
    from a corpus with none of that tell in it, and would understate every model
    at once.
    """
    keep: list[Tell] = []
    skipped: dict[str, str] = {}
    for tell in tells:
        if tell.method != "judge":
            keep.append(tell)
            continue
        report = latest_report(tell.id, runs_root, judge_model=judge_model)
        if report is None:
            skipped[tell.id] = (
                f"no calibration report"
                + (f" for judge {judge_model}" if judge_model else "")
            )
            continue
        agreement = float(report.get("agreement") or 0.0)
        if agreement < gate:
            skipped[tell.id] = (
                f"calibration {agreement:.2f} < {gate:.2f} "
                f"({report.get('timestamp')})"
            )
            continue
        if report.get("rubric_version") != tell.rubric_version:
            skipped[tell.id] = (
                f"calibrated against rubric v{report.get('rubric_version')}, "
                f"registry has v{tell.rubric_version}"
            )
            continue
        keep.append(tell)
    return keep, skipped


def calibration_scores(
    tell_ids: Sequence[str], runs_root: Path, judge_model: str | None = None
) -> dict[str, Any]:
    """Per-tell calibration facts for the run manifest."""
    out: dict[str, Any] = {}
    for tell_id in sorted(tell_ids):
        report = latest_report(tell_id, runs_root, judge_model=judge_model)
        if report is None:
            out[tell_id] = None
            continue
        out[tell_id] = {
            "agreement": report.get("agreement"),
            "n": report.get("n"),
            "judge_model": report.get("judge_model"),
            "rubric_version": report.get("rubric_version"),
            "timestamp": report.get("timestamp"),
        }
    return out


def judge_tells(registry: Registry, include_candidates: bool = False) -> list[Tell]:
    return [
        t
        for t in registry.active_tells(include_candidates=include_candidates)
        if t.method == "judge"
    ]


__all__ = [
    "GATE",
    "CalibrationReport",
    "Snippet",
    "SnippetOutcome",
    "calibrate",
    "calibration_root",
    "calibration_scores",
    "gate_tells",
    "judge_tells",
    "latest_report",
    "lint_snippets",
    "load_snippets",
    "report_path",
    "run_snippet",
    "write_report",
]
