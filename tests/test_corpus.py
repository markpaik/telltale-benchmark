"""Corpus loading: the filename contract, sidecars, sorting, and hashing."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from telltale.corpus import Doc, corpus_hash, load_corpus

MODELS = ["claude-opus-5", "gpt-5-1"]
FORMATS = ["email", "memo"]


def _body(model: str, fmt: str, index: int) -> str:
    return (
        f"# {fmt.title()} {index} from {model}\n\n"
        f"This is the opening paragraph of {fmt} number {index}.\n\n"
        "- one\n- two\n- three\n\n"
        "A closing line of prose.\n"
    )


@pytest.fixture
def corpus_root(tmp_path: Path) -> Path:
    """2 models x 2 formats x 2 docs, each with a sidecar, plus junk to skip."""
    root = tmp_path / "corpus"
    for model in MODELS:
        model_dir = root / model
        model_dir.mkdir(parents=True)
        for fmt in FORMATS:
            for index in (1, 2):
                stem = f"{fmt}-{index:02d}"
                (model_dir / f"{stem}.md").write_text(_body(model, fmt, index), encoding="utf-8")
                (model_dir / f"{stem}.json").write_text(
                    json.dumps({"model": model, "format": fmt, "index": index}),
                    encoding="utf-8",
                )
    # Junk that must be skipped: wrong digit count, unknown format, stray file.
    (root / MODELS[0] / "memo-3.md").write_text("nope\n", encoding="utf-8")
    (root / MODELS[0] / "haiku-01.md").write_text("nope\n", encoding="utf-8")
    (root / MODELS[0] / "README.txt").write_text("nope\n", encoding="utf-8")
    (root / MODELS[0] / ".DS_Store").write_bytes(b"\x00\x01")
    return root


# --- loading -----------------------------------------------------------------


def test_loads_every_matching_document(corpus_root: Path) -> None:
    docs = load_corpus(corpus_root)
    assert len(docs) == 8
    assert [d.doc_id for d in docs] == [
        "claude-opus-5/email-01",
        "claude-opus-5/email-02",
        "claude-opus-5/memo-01",
        "claude-opus-5/memo-02",
        "gpt-5-1/email-01",
        "gpt-5-1/email-02",
        "gpt-5-1/memo-01",
        "gpt-5-1/memo-02",
    ]


def test_sorted_by_doc_id(corpus_root: Path) -> None:
    docs = load_corpus(corpus_root)
    assert [d.doc_id for d in docs] == sorted(d.doc_id for d in docs)


def test_fields_are_parsed_from_the_path(corpus_root: Path) -> None:
    doc = load_corpus(corpus_root)[2]
    assert doc.doc_id == "claude-opus-5/memo-01"
    assert doc.model == "claude-opus-5"
    assert doc.fmt == "memo"
    assert doc.path == corpus_root / "claude-opus-5" / "memo-01.md"


def test_text_plain_and_words(corpus_root: Path) -> None:
    doc = load_corpus(corpus_root, models=["claude-opus-5"], formats=["memo"])[0]
    assert doc.text.startswith("# Memo 1 from claude-opus-5")
    assert "#" not in doc.plain and "- one" not in doc.plain
    assert "Memo 1 from claude-opus-5" in doc.plain
    # 4 heading words + 9 in the paragraph + 3 list items + 5 in the closing line.
    assert doc.words == 21


def test_sha256_is_over_the_raw_bytes(corpus_root: Path) -> None:
    doc = load_corpus(corpus_root)[0]
    expected = hashlib.sha256(doc.path.read_bytes()).hexdigest()
    assert doc.sha256 == expected
    assert len(doc.sha256) == 64


def test_sidecar_is_parsed(corpus_root: Path) -> None:
    doc = load_corpus(corpus_root)[0]
    assert doc.sidecar == {"model": "claude-opus-5", "format": "email", "index": 1}


def test_missing_sidecar_is_an_empty_dict(corpus_root: Path) -> None:
    (corpus_root / "gpt-5-1" / "memo-02.json").unlink()
    doc = [d for d in load_corpus(corpus_root) if d.doc_id == "gpt-5-1/memo-02"][0]
    assert doc.sidecar == {}


def test_malformed_sidecar_warns_and_yields_empty_dict(
    corpus_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (corpus_root / "gpt-5-1" / "memo-01.json").write_text("{not json", encoding="utf-8")
    doc = [d for d in load_corpus(corpus_root) if d.doc_id == "gpt-5-1/memo-01"][0]
    assert doc.sidecar == {}
    assert "unreadable sidecar" in capsys.readouterr().err


def test_junk_filenames_are_skipped_with_a_warning(
    corpus_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    docs = load_corpus(corpus_root)
    stems = {d.path.name for d in docs}
    assert "memo-3.md" not in stems
    assert "haiku-01.md" not in stems
    assert "README.txt" not in stems

    err = capsys.readouterr().err
    assert "memo-3.md" in err
    assert "haiku-01.md" in err
    assert "README.txt" in err
    # Sidecars and dotfiles are expected company, not junk.
    assert "email-01.json" not in err
    assert ".DS_Store" not in err


def test_filters(corpus_root: Path) -> None:
    only_memo = load_corpus(corpus_root, formats=["memo"])
    assert len(only_memo) == 4
    assert {d.fmt for d in only_memo} == {"memo"}

    only_model = load_corpus(corpus_root, models=["gpt-5-1"])
    assert len(only_model) == 4
    assert {d.model for d in only_model} == {"gpt-5-1"}

    both = load_corpus(corpus_root, models=["gpt-5-1"], formats=["email"])
    assert [d.doc_id for d in both] == ["gpt-5-1/email-01", "gpt-5-1/email-02"]

    assert load_corpus(corpus_root, models=["no-such-model"]) == []


def test_missing_or_empty_root_is_not_an_error(tmp_path: Path) -> None:
    assert load_corpus(tmp_path / "does-not-exist") == []
    empty = tmp_path / "empty"
    empty.mkdir()
    assert load_corpus(empty) == []


def test_crlf_is_normalized_but_hash_is_of_the_raw_bytes(tmp_path: Path) -> None:
    model_dir = tmp_path / "m"
    model_dir.mkdir()
    raw = b"# Title\r\n\r\nOne line.\r\n"
    path = model_dir / "memo-01.md"
    path.write_bytes(raw)
    doc = load_corpus(tmp_path)[0]
    assert "\r" not in doc.text
    assert doc.sha256 == hashlib.sha256(raw).hexdigest()


def test_non_utf8_file_is_skipped_with_a_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    model_dir = tmp_path / "m"
    model_dir.mkdir()
    (model_dir / "memo-01.md").write_bytes(b"\xff\xfe not utf-8")
    assert load_corpus(tmp_path) == []
    assert "not valid utf-8" in capsys.readouterr().err


# --- Doc.from_text -----------------------------------------------------------


def test_from_text_matches_a_loaded_doc(corpus_root: Path) -> None:
    loaded = load_corpus(corpus_root)[0]
    built = Doc.from_text(
        loaded.doc_id, loaded.model, loaded.fmt, loaded.text, path=loaded.path
    )
    assert built.sha256 == loaded.sha256
    assert built.plain == loaded.plain
    assert built.words == loaded.words


# --- corpus_hash -------------------------------------------------------------


def test_corpus_hash_is_stable_and_order_independent(corpus_root: Path) -> None:
    docs = load_corpus(corpus_root)
    first = corpus_hash(docs)
    assert first == corpus_hash(load_corpus(corpus_root))
    assert first == corpus_hash(list(reversed(docs)))
    assert len(first) == 64


def test_corpus_hash_tracks_content(corpus_root: Path) -> None:
    before = corpus_hash(load_corpus(corpus_root))
    path = corpus_root / "claude-opus-5" / "memo-01.md"
    path.write_text(path.read_text(encoding="utf-8") + "One more line.\n", encoding="utf-8")
    assert corpus_hash(load_corpus(corpus_root)) != before


def test_corpus_hash_tracks_membership(corpus_root: Path) -> None:
    docs = load_corpus(corpus_root)
    assert corpus_hash(docs[:-1]) != corpus_hash(docs)
    assert corpus_hash([]) == hashlib.sha256(b"").hexdigest()
