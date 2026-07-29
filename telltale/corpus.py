"""Load the generated document corpus from disk.

Layout on disk:

    <root>/<model-id>/<format>-<NN>.md      the document
    <root>/<model-id>/<format>-<NN>.json    optional sidecar (prompt, run metadata)

Everything downstream (detectors, judge, discovery) measures through `Doc`, so
loading is the one place that decides what "the text" is: `text` is the raw
markdown, `plain` is the markdown-stripped prose, and every rate stat is per
1,000 words of `plain`.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from telltale import textstats

# The 14 generation formats. A file whose name does not start with one of these
# (followed by -NN.md) is not part of the corpus.
FORMATS: tuple[str, ...] = (
    "email",
    "memo",
    "research-brief",
    "business-report",
    "project-proposal",
    "meeting-minutes",
    "executive-summary",
    "performance-review",
    "grant-proposal",
    "literature-review",
    "white-paper",
    "case-study",
    "sop",
    "postmortem",
)

FILENAME_PATTERN = re.compile(
    r"^(?P<fmt>" + "|".join(sorted(FORMATS, key=len, reverse=True)) + r")-(?P<index>\d{2})\.md$"
)


def _warn(message: str) -> None:
    print(f"telltale.corpus: {message}", file=sys.stderr)


@dataclass(frozen=True)
class Doc:
    """One generated document, with its derived views computed once at load."""

    doc_id: str  # "<model>/<stem>", e.g. "claude-opus-5/memo-04"
    model: str  # "claude-opus-5"
    fmt: str  # "memo"
    path: Path
    text: str  # raw markdown, utf-8 decoded, newlines normalized to \n
    plain: str  # markdown-stripped prose
    words: int  # word count of plain
    sha256: str  # of the raw file bytes
    sidecar: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_bytes(
        cls,
        doc_id: str,
        model: str,
        fmt: str,
        path: Path,
        raw: bytes,
        sidecar: dict[str, Any] | None = None,
    ) -> "Doc":
        """Build a Doc from the raw file bytes, computing plain/words/sha256."""
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        plain = textstats.strip_markdown(text)
        return cls(
            doc_id=doc_id,
            model=model,
            fmt=fmt,
            path=Path(path),
            text=text,
            plain=plain,
            words=textstats.word_count(plain),
            sha256=hashlib.sha256(raw).hexdigest(),
            sidecar=dict(sidecar or {}),
        )

    @classmethod
    def from_text(
        cls,
        doc_id: str,
        model: str,
        fmt: str,
        text: str,
        path: Path | None = None,
        sidecar: dict[str, Any] | None = None,
    ) -> "Doc":
        """Build a Doc from a string — for tests and for freshly generated text."""
        return cls.from_bytes(
            doc_id=doc_id,
            model=model,
            fmt=fmt,
            path=Path(path) if path is not None else Path(doc_id + ".md"),
            raw=text.encode("utf-8"),
            sidecar=sidecar,
        )


def _read_sidecar(md_path: Path) -> dict[str, Any]:
    """Parse <stem>.json next to the document. Missing or malformed -> {}."""
    sidecar_path = md_path.with_suffix(".json")
    if not sidecar_path.is_file():
        return {}
    try:
        data = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        _warn(f"unreadable sidecar {sidecar_path}: {exc}")
        return {}
    if not isinstance(data, dict):
        _warn(f"sidecar is not a JSON object, ignoring: {sidecar_path}")
        return {}
    return data


def load_corpus(
    root: Path,
    models: list[str] | None = None,
    formats: list[str] | None = None,
) -> list[Doc]:
    """Load every document under root, sorted by doc_id.

    A missing, empty, or entirely unrecognized root is not an error — it returns
    an empty list, so an un-generated corpus reads as "nothing to score" rather
    than a crash. Files that do not match the `<format>-NN.md` contract are
    skipped with a warning on stderr; .json sidecars and dotfiles are skipped
    silently.
    """
    root = Path(root)
    if not root.is_dir():
        return []

    wanted_models = set(models) if models else None
    wanted_formats = set(formats) if formats else None

    docs: list[Doc] = []
    for model_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        model = model_dir.name
        if model.startswith("."):
            continue
        if wanted_models is not None and model not in wanted_models:
            continue

        for path in sorted(p for p in model_dir.iterdir() if p.is_file()):
            name = path.name
            if name.startswith(".") or path.suffix == ".json":
                continue
            match = FILENAME_PATTERN.match(name)
            if not match:
                _warn(f"skipping unrecognized filename: {path}")
                continue
            fmt = match.group("fmt")
            if wanted_formats is not None and fmt not in wanted_formats:
                continue
            try:
                raw = path.read_bytes()
            except OSError as exc:
                _warn(f"unreadable document {path}: {exc}")
                continue
            try:
                doc = Doc.from_bytes(
                    doc_id=f"{model}/{path.stem}",
                    model=model,
                    fmt=fmt,
                    path=path,
                    raw=raw,
                    sidecar=_read_sidecar(path),
                )
            except UnicodeDecodeError as exc:
                _warn(f"not valid utf-8, skipping {path}: {exc}")
                continue
            docs.append(doc)

    docs.sort(key=lambda d: d.doc_id)
    return docs


def corpus_hash(docs: list[Doc]) -> str:
    """Stable fingerprint of a document set: sha256 over sorted doc_id:sha256 lines.

    Order-independent, so two runs over the same files hash the same however the
    list was assembled.
    """
    lines = sorted(f"{d.doc_id}:{d.sha256}" for d in docs)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
