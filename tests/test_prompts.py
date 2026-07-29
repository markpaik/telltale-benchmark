"""The prompt bank: it loads, it composes, and it never tells a model how to write."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from telltale import prompts
from telltale.corpus import FORMATS

BANK = Path(__file__).resolve().parent.parent / "prompts" / "formats"


# --- the real bank -----------------------------------------------------------


def test_real_bank_lints_clean():
    violations = prompts.bank_lint(BANK)
    assert violations == [], "\n".join(violations)


def test_real_bank_has_fourteen_formats_and_112_prompts():
    bank = prompts.load_prompt_bank(BANK)
    assert sorted(bank) == sorted(FORMATS)
    assert sum(len(spec.prompts) for spec in bank.values()) == 112


def test_all_112_ids_are_unique():
    bank = prompts.load_prompt_bank(BANK)
    ids = [p.id for spec in bank.values() for p in spec.prompts]
    assert len(ids) == 112
    assert len(set(ids)) == 112


def test_bundle_flags_match_the_design():
    bank = prompts.load_prompt_bank(BANK)
    bundled = {fmt for fmt, spec in bank.items() if spec.bundle}
    assert bundled == set(prompts.BUNDLE_FORMATS)


def test_every_format_covers_the_domain_rotation_once_each():
    bank = prompts.load_prompt_bank(BANK)
    for fmt, spec in bank.items():
        assert sorted(p.domain for p in spec.prompts) == sorted(prompts.DOMAINS), fmt


def test_scenarios_carry_no_markdown_formatting():
    # Formatting in the prompt leaks into the model's output formatting, which
    # would contaminate every structural tell the benchmark counts.
    bank = prompts.load_prompt_bank(BANK)
    for spec in bank.values():
        for prompt in spec.prompts:
            for line in prompt.scenario.splitlines():
                stripped = line.strip()
                assert not stripped.startswith(("#", "- ", "* ", "|")), (
                    f"{prompt.id}: markdown in scenario: {line!r}"
                )


def test_scenarios_are_substantial():
    bank = prompts.load_prompt_bank(BANK)
    for spec in bank.values():
        for prompt in spec.prompts:
            words = len(prompt.scenario.split())
            assert 100 <= words <= 400, f"{prompt.id}: {words} words"


def test_scenarios_contain_concrete_numbers():
    # The quality bar the bank was written to: figures, not vibes.
    import re

    bank = prompts.load_prompt_bank(BANK)
    for spec in bank.values():
        for prompt in spec.prompts:
            figures = re.findall(r"\d", prompt.scenario)
            assert len(figures) >= 10, f"{prompt.id}: too few digits to anchor a document"


# --- loader ------------------------------------------------------------------


def _write_bank(tmp_path: Path, **overrides) -> Path:
    directory = tmp_path / "formats"
    directory.mkdir(parents=True, exist_ok=True)
    scenario = " ".join(["Bellwether Freight moved 41,000 pallets in March."] * 20)
    for index, fmt in enumerate(FORMATS):
        data = {
            "format": fmt,
            "bundle": fmt in prompts.BUNDLE_FORMATS,
            "target_words": 5000,
            "min_words": 4500,
            "output_convention": "One document.",
            "prompts": [
                {
                    "id": f"{fmt}-{position:02d}",
                    "domain": prompts.DOMAINS[(index + position - 1) % 8],
                    "scenario": scenario,
                }
                for position in range(1, 9)
            ],
        }
        data.update(overrides.get(fmt, {}))
        (directory / f"{fmt}.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    return directory


def test_loader_round_trips_a_synthetic_bank(tmp_path):
    directory = _write_bank(tmp_path)
    bank = prompts.load_prompt_bank(directory)
    assert sorted(bank) == sorted(FORMATS)
    spec = bank["memo"]
    assert spec.bundle is True
    assert spec.target_words == 5000
    assert spec.prompt("memo-03").id == "memo-03"
    assert spec.prompts[2].index == 3
    assert prompts.bank_lint(directory) == []


def test_loader_rejects_non_mapping_yaml(tmp_path):
    directory = tmp_path / "formats"
    directory.mkdir()
    (directory / "memo.yaml").write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(ValueError):
        prompts.load_prompt_bank(directory)


def test_prompt_sha256_is_stable_and_content_addressed():
    spec = prompts.load_prompt_bank(BANK)["memo"]
    first = spec.prompts[0]
    assert first.sha256 == prompts.prompt_sha256(first.scenario)
    assert first.sha256 != spec.prompts[1].sha256


# --- compose -----------------------------------------------------------------


def test_compose_prompt_includes_scenario_convention_and_length_ask():
    spec = prompts.load_prompt_bank(BANK)["business-report"]
    prompt = spec.prompts[0]
    composed = prompts.compose_prompt(spec, prompt)
    assert prompt.scenario.strip() in composed
    assert spec.output_convention.strip() in composed
    assert "5,000 words" in composed
    assert "10 pages" in composed


def test_compose_prompt_says_set_for_bundles_and_document_for_singles():
    bank = prompts.load_prompt_bank(BANK)
    bundled = prompts.compose_prompt(bank["email"], bank["email"].prompts[0])
    single = prompts.compose_prompt(bank["white-paper"], bank["white-paper"].prompts[0])
    assert "The full set should run" in bundled
    assert "The full document should run" in single


def test_compose_prompt_adds_no_style_guidance():
    # The composed text is the whole of what the model is told. If a banned term
    # can reach it through the convention or the length ask, the bank lint alone
    # would not catch it.
    bank = prompts.load_prompt_bank(BANK)
    for spec in bank.values():
        for prompt in spec.prompts:
            composed = prompts.compose_prompt(spec, prompt)
            for label, pattern in prompts._BANNED:
                assert not pattern.search(composed), f"{prompt.id}: {label}"


# --- lint catches things -----------------------------------------------------


@pytest.mark.parametrize(
    "banned",
    [
        "The vendor uses AI to sort parcels.",
        "The board wants a polished result.",
        "Keep a professional tone throughout.",
        "The chair is eloquent about the deficit.",
        "It must be well-written for the funder.",
        "Make the section engaging for readers.",
        "Match the firm's writing style.",
    ],
)
def test_lint_flags_style_guidance_in_a_scenario(tmp_path, banned):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "memo.yaml").read_text())
    data["prompts"][0]["scenario"] += " " + banned
    (directory / "memo.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")

    violations = prompts.bank_lint(directory)
    assert any("memo-01" in v and "banned term" in v for v in violations), violations


@pytest.mark.parametrize(
    "innocent",
    [
        "The email chain ran for three weeks.",
        "Staff training resumed in April.",
        "They must maintain the chair lift.",
        "Detail the available capacity.",
        "Community engagement rose 12 percent.",
    ],
)
def test_lint_does_not_flag_words_that_merely_contain_banned_letters(tmp_path, innocent):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "memo.yaml").read_text())
    data["prompts"][0]["scenario"] += " " + innocent
    (directory / "memo.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")

    assert prompts.bank_lint(directory) == []


def test_lint_flags_a_missing_format_file(tmp_path):
    directory = _write_bank(tmp_path)
    (directory / "postmortem.yaml").unlink()
    violations = prompts.bank_lint(directory)
    assert any("missing format file: postmortem.yaml" in v for v in violations)


def test_lint_flags_wrong_prompt_count(tmp_path):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "sop.yaml").read_text())
    data["prompts"] = data["prompts"][:6]
    (directory / "sop.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    violations = prompts.bank_lint(directory)
    assert any("6 prompts, expected 8" in v for v in violations)


def test_lint_flags_duplicate_ids_across_files(tmp_path):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "sop.yaml").read_text())
    data["prompts"][0]["id"] = "memo-01"
    (directory / "sop.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    violations = prompts.bank_lint(directory)
    assert any("duplicate prompt id" in v or "expected 'sop-01'" in v for v in violations)


def test_lint_flags_a_broken_domain_rotation(tmp_path):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "memo.yaml").read_text())
    data["prompts"][0]["domain"] = data["prompts"][1]["domain"]
    (directory / "memo.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    violations = prompts.bank_lint(directory)
    assert any("do not cover the rotation" in v for v in violations)


def test_lint_flags_a_bundle_flag_that_drifted(tmp_path):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "email.yaml").read_text())
    data["bundle"] = False
    (directory / "email.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    violations = prompts.bank_lint(directory)
    assert any("bundle is False, expected True" in v for v in violations)


def test_lint_flags_min_words_above_target(tmp_path):
    directory = _write_bank(tmp_path)
    data = yaml.safe_load((directory / "memo.yaml").read_text())
    data["min_words"] = 9000
    (directory / "memo.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    violations = prompts.bank_lint(directory)
    assert any("exceeds target_words" in v for v in violations)


def test_lint_reports_a_missing_directory(tmp_path):
    violations = prompts.bank_lint(tmp_path / "nope")
    assert violations and "does not exist" in violations[0]
