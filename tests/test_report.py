"""End to end: a synthetic corpus in, a run directory out, and it reproduces.

The mini corpus is two models over the same four prompts, one of them writing
with every tell it can fit in and the other writing plainly. Tells are planted
deliberately and counted by hand below, so the assertions are about specific
documents rather than about "the pipeline ran".
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from telltale import cli, manifest as manifest_mod, report, scoring
from telltale.registry import Registry

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"

LOUD = "claude-tellsalot"
PLAIN = "claude-plainspoken"

# --- the mini corpus ---------------------------------------------------------
#
# Planted in LOUD/email-01: delve x1, crucial x1, robust x1, underscore x1,
# leverage x1, "worth noting" x1, "I hope this email finds you well" (binary),
# "don't hesitate to reach out" (binary), "I look forward to hearing" (binary),
# "Warm regards" sign-off x1, three bolded bullet lead-ins.

LOUD_EMAIL_1 = """Subject: Q3 Attendance Update

I hope this email finds you well. I wanted to delve into the attendance figures
we discussed last week.

Moreover, the data underscores a crucial shift in how families are engaging with
our schools. It is worth noting that chronic absence fell in nine of twelve
buildings. Furthermore, the improvement looks robust across every grade band we
examined this quarter. However, three schools moved in the other direction.

- **Elementary**: down 2.1 points against last year
- **Middle**: down 1.4 points against last year
- **High**: up 0.6 points against last year

Additionally, we should leverage this momentum before the winter term begins.
Therefore, I propose a short working session with the attendance team. Thus, we
can align on next steps well before the board meeting in November.

Please don't hesitate to reach out with any questions at all.
I look forward to hearing your thoughts on the proposed session.

Warm regards,
Alex
"""

LOUD_EMAIL_2 = """Subject: Following up on the staffing plan

I hope this note finds you well. I wanted to delve into the staffing questions
that came up on Thursday.

Moreover, the vacancy data underscores a crucial gap in our middle schools.
Furthermore, the pattern is robust across all three regions. Consequently, the
hiring team has drafted a revised timeline. However, the timeline depends on
approvals we do not yet have.

- **Region One**: eleven vacancies, six offers pending
- **Region Two**: eight vacancies, two offers pending
- **Region Three**: fourteen vacancies, nine offers pending

Additionally, we can leverage the substitute pool while offers clear. Therefore,
no classroom should sit uncovered in November. Thus, the risk is scheduling
churn rather than lost instruction.

Please don't hesitate to reach out if the timeline is a problem.
I look forward to hearing where you land.

Warm regards,
Alex
"""

LOUD_REPORT_1 = """# Q3 Attendance: A Comprehensive Analysis

## Executive Summary

This report delves into attendance performance for the third quarter. It is
worth noting that the findings underscore a crucial shift in family engagement.

## Key Findings

Moreover, chronic absence fell in nine of twelve buildings. Furthermore, the
decline is robust across every grade band examined. Additionally, the pattern
holds when controlling for enrollment change. However, three schools moved in
the other direction, and their results deserve a closer look.

- **Elementary**: down 2.1 points
- **Middle**: down 1.4 points
- **High**: up 0.6 points

## Recommendations

Therefore, the team recommends three actions. Thus, the district can leverage
the momentum from this quarter.

- **Expand** the family outreach pilot to six more buildings
- **Fund** two additional attendance agents in the high school region
- **Report** monthly rather than quarterly through the winter

## Conclusion

Ultimately, the third quarter shows real movement. Notably, the gains are
concentrated where the pilot ran.
"""

LOUD_REPORT_2 = """# Staffing Vacancies: A Comprehensive Analysis

## Executive Summary

This report delves into vacancy patterns across the three regions. It is worth
noting that the data underscores a crucial constraint on the winter schedule.

## Key Findings

Moreover, vacancies concentrate in middle schools. Furthermore, the pattern is
robust across every region examined. Additionally, the offer pipeline has
improved since August. However, acceptance rates remain below the target.

- **Region One**: eleven vacancies
- **Region Two**: eight vacancies
- **Region Three**: fourteen vacancies

## Recommendations

Therefore, the team recommends three actions. Thus, the district can leverage
the substitute pool without losing instructional time.

- **Approve** the revised hiring timeline this week
- **Extend** the referral bonus through December
- **Track** acceptance weekly rather than monthly

## Conclusion

Ultimately, the constraint is acceptance, not applications. Notably, the gap
narrows wherever a principal joins the interview.
"""

PLAIN_EMAIL_1 = """Subject: Q3 attendance numbers

Here are the attendance figures from the meeting last week.

Chronic absence fell in nine of twelve buildings. The largest drop was in
elementary schools, 2.1 points against last year. Middle schools fell 1.4
points. High schools rose 0.6 points, and that is the number I want to talk
about.

Three schools moved the wrong way: Bennett, Carver, and Foster. All three had
staffing gaps in September that we did not fill until October. I have asked
their principals for a short write-up by Friday.

I would like thirty minutes next week to agree on what we tell the board.
Tuesday or Wednesday both work on my end.

Alex
"""

PLAIN_EMAIL_2 = """Subject: Staffing plan, where it stands

Following up on Thursday. Here is where the staffing plan actually sits.

We have thirty-three open positions across the three regions. Fourteen of them
are in Region Three, which is more than the other two regions combined. Seventeen
offers are out. Nine of those are in Region Three.

The hiring team redrew the timeline yesterday. It depends on two approvals that
have not come through, so I would not treat the dates as firm.

Substitutes can cover through November. After that we are guessing. Tell me if
the dates are a problem and I will take it back to the team.

Alex
"""

PLAIN_REPORT_1 = """# Third quarter attendance

Chronic absence fell in nine of twelve buildings this quarter. Elementary
schools drove most of that, at 2.1 points below last year. Middle schools fell
1.4 points. High schools rose 0.6 points.

Three schools moved the wrong way. Bennett, Carver, and Foster all had staffing
gaps that ran from September into October. Their principals owe us a write-up by
Friday, and until we have it the cause is a guess.

The family outreach pilot ran in six buildings. Five of the six are among the
nine that improved. That is suggestive, not proof; the pilot buildings were
picked because they had room to improve.

We recommend expanding the pilot to six more buildings in the winter term,
funding two attendance agents in the high school region, and moving to monthly
reporting until the high school number turns.

The number to watch is high school. Nothing in this quarter explains it.
"""

PLAIN_REPORT_2 = """# Staffing vacancies, third quarter

There are thirty-three open positions across the three regions. Fourteen sit in
Region Three, more than Regions One and Two combined. Middle schools account for
twenty-one of the thirty-three.

Seventeen offers are outstanding. Nine of those are in Region Three, so the gap
there closes fastest if acceptance holds. Acceptance has been running at 62
percent, well under the 75 percent the plan assumed.

The substitute pool covers November. December is the first month where the
arithmetic stops working, and only if acceptance stays where it is.

We recommend approving the revised timeline this week, extending the referral
bonus through December, and tracking acceptance weekly.

One thing worth testing: acceptance is roughly ten points higher wherever a
principal sat on the interview panel. The sample is small.
"""

DOCUMENTS = {
    LOUD: {
        "email-01": LOUD_EMAIL_1,
        "email-02": LOUD_EMAIL_2,
        "business-report-01": LOUD_REPORT_1,
        "business-report-02": LOUD_REPORT_2,
    },
    PLAIN: {
        "email-01": PLAIN_EMAIL_1,
        "email-02": PLAIN_EMAIL_2,
        "business-report-01": PLAIN_REPORT_1,
        "business-report-02": PLAIN_REPORT_2,
    },
}


def build_corpus(root: Path) -> Path:
    """Write the mini corpus to disk in the layout `load_corpus` expects."""
    root = Path(root)
    for model, docs in DOCUMENTS.items():
        (root / model).mkdir(parents=True, exist_ok=True)
        for stem, text in docs.items():
            (root / model / f"{stem}.md").write_text(text, encoding="utf-8")
            (root / model / f"{stem}.json").write_text(
                json.dumps({"model_requested": model, "prompt_id": stem}, indent=2) + "\n",
                encoding="utf-8",
            )
    return root


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    return build_corpus(tmp_path / "corpus")


@pytest.fixture
def run_dir(corpus: Path, tmp_path: Path) -> Path:
    return report.score_run(
        corpus_root=corpus,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs",
        cli_args=["score"],
        bootstrap_n=200,
    )


def rows_of(run_dir: Path) -> list[dict]:
    text = (run_dir / report.SCORES_NAME).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def find(rows: list[dict], doc_id: str, tell_id: str) -> dict:
    hits = [r for r in rows if r["doc_id"] == doc_id and r["tell_id"] == tell_id]
    assert len(hits) == 1, f"expected one row for {doc_id}/{tell_id}, got {len(hits)}"
    return hits[0]


# --- outputs -----------------------------------------------------------------


def test_a_run_writes_all_five_files(run_dir: Path) -> None:
    for name in (
        report.SCORES_NAME,
        report.MATRIX_NAME,
        report.MATRIX_BY_FORMAT_NAME,
        report.SCORECARD_NAME,
        manifest_mod.MANIFEST_NAME,
    ):
        assert (run_dir / name).is_file(), name


def test_run_id_names_its_inputs(run_dir: Path) -> None:
    stamp, corpus_sha, registry_sha = run_dir.name.split("-")
    assert stamp.endswith("Z") and len(stamp) == len("20260729T120000Z")
    manifest = manifest_mod.load_manifest(run_dir)
    assert manifest["corpus"]["corpus_hash"].startswith(corpus_sha)
    assert manifest["registry"]["content_hash"].startswith(registry_sha)


def test_every_document_and_tell_is_present(run_dir: Path) -> None:
    rows = rows_of(run_dir)
    assert len({r["doc_id"] for r in rows}) == 8
    assert not any(r["method"] == "judge" for r in rows)


# --- planted tells -----------------------------------------------------------


@pytest.mark.parametrize(
    ("doc_id", "tell_id", "raw"),
    [
        (f"{LOUD}/email-01", "lex.delve", 1.0),
        (f"{LOUD}/email-01", "lex.crucial", 1.0),
        (f"{LOUD}/email-01", "lex.robust", 1.0),
        (f"{LOUD}/email-01", "lex.underscore", 1.0),
        (f"{LOUD}/email-01", "lex.leverage", 1.0),
        (f"{LOUD}/email-01", "phr.worth-noting", 1.0),
        (f"{LOUD}/email-01", "crt.hope-finds-you-well", 1.0),
        (f"{LOUD}/email-01", "crt.dont-hesitate", 1.0),
        (f"{LOUD}/email-01", "crt.looking-forward", 1.0),
        (f"{LOUD}/email-01", "crt.warm-signoff", 1.0),
        (f"{LOUD}/email-01", "pnc.bold-lead-in-bullet", 3.0),
        (f"{LOUD}/business-report-01", "str.conclusion-heading", 1.0),
        (f"{LOUD}/business-report-01", "pnc.bold-lead-in-bullet", 6.0),
        (f"{PLAIN}/email-01", "lex.delve", 0.0),
        (f"{PLAIN}/email-01", "crt.hope-finds-you-well", 0.0),
        (f"{PLAIN}/email-01", "crt.warm-signoff", 0.0),
        (f"{PLAIN}/business-report-01", "str.conclusion-heading", 0.0),
    ],
)
def test_planted_tells_have_the_hand_counted_value(
    run_dir: Path, doc_id: str, tell_id: str, raw: float
) -> None:
    assert find(rows_of(run_dir), doc_id, tell_id)["raw"] == raw


def test_a_count_tell_carries_its_rate_and_quotes(run_dir: Path) -> None:
    row = find(rows_of(run_dir), f"{LOUD}/email-01", "lex.delve")
    assert row["unit"] == "count"
    assert row["rate_per_1k"] is not None
    assert row["matches"] and "delve" in row["matches"][0]["quote"]
    assert row["matches"][0]["line"] >= 1


def test_format_scoped_tells_are_absent_from_report_rows(run_dir: Path) -> None:
    rows = rows_of(run_dir)
    report_rows = [r for r in rows if r["format"] == "business-report"]
    assert report_rows
    assert not any(r["tell_id"].startswith("crt.") for r in report_rows)
    # ...and present on the emails, so the absence is scoping and not a bug.
    email_rows = [r for r in rows if r["format"] == "email"]
    assert any(r["tell_id"] == "crt.hope-finds-you-well" for r in email_rows)


def test_the_loud_model_scores_higher(run_dir: Path) -> None:
    df = report.read_scores_jsonl(run_dir / report.SCORES_NAME)
    meta = manifest_mod.load_manifest(run_dir)["registry"]["tells"]
    index = scoring.indices(df, scoring.tell_meta(meta))
    assert index.loc[LOUD, "ai_tell_index"] > index.loc[PLAIN, "ai_tell_index"]


def test_statistic_tells_below_their_floor_are_null_not_zero(run_dir: Path) -> None:
    rows = [r for r in rows_of(run_dir) if r["method"] == "statistic"]
    assert rows
    assert any(r["raw"] is None for r in rows), "expected some statistic under its floor"
    for row in rows:
        if row["raw"] is None:
            assert row["score"] is None


# --- matrices ----------------------------------------------------------------


def test_matrices_are_written_with_sorted_axes(run_dir: Path) -> None:
    matrix = (run_dir / report.MATRIX_NAME).read_text(encoding="utf-8").splitlines()
    header = matrix[0].split(",")
    assert header[0] == "model"
    assert header[1:] == sorted(header[1:])
    assert [line.split(",")[0] for line in matrix[1:]] == [PLAIN, LOUD]

    by_format = (run_dir / report.MATRIX_BY_FORMAT_NAME).read_text(encoding="utf-8")
    assert by_format.splitlines()[0].startswith("model,format,")
    assert "business-report" in by_format


# --- scorecard ---------------------------------------------------------------


def test_the_scorecard_has_every_required_section(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    for heading in (
        "## 1. Headline",
        "## 2. Index by format",
        "## 3. Loudest tells per model",
        "## 4. Cells below the evidence floor",
        "## 5. Dormant tells",
        "## 6. Run",
    ):
        assert heading in card, heading


def test_the_scorecard_ranks_the_loud_model_first(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    headline = card.split("### Separation")[0]
    assert headline.index(LOUD) < headline.index(PLAIN)


def test_the_scorecard_shows_an_exemplar_with_a_locator(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert f"{LOUD}/email-01:" in card or f"{LOUD}/business-report-01:" in card


def test_binary_signals_carry_a_wilson_interval(run_dir: Path) -> None:
    """Two documents cannot support "100%", and the card must not imply they can."""
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "100% of docs [" in card
    # The courtesy tells are email-only, so they saw two of the four documents.
    lo, hi = scoring.wilson_ci(2, 2)
    assert lo < 0.35
    assert f"[{100 * lo:.0f}-{100 * hi:.0f}%]" in card


def test_category_intervals_are_reported(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "### Category scores with 95% intervals" in card


def test_the_scorecard_reports_the_skipped_judge_tells(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    registry = Registry(REGISTRY_PATH)
    skipped = len([t for t in registry.active_tells() if t.method == "judge"])
    assert f"| {skipped} (Tier-2, arrives in M6) |" in card


def test_the_scorecard_reports_the_corpus_and_registry_hashes(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    manifest = manifest_mod.load_manifest(run_dir)
    assert manifest["corpus"]["corpus_hash"][:16] in card
    assert manifest["registry"]["content_hash"][:16] in card
    assert "| Documents | 8 |" in card


def test_thin_cells_are_named_and_flagged(run_dir: Path) -> None:
    """Two documents per cell is well under the floor, and the card says so."""
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "Below the 8-document floor" in card
    assert "†" in card


def test_dormant_tells_are_listed(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    df = report.read_scores_jsonl(run_dir / report.SCORES_NAME)
    dormant = scoring.dormant_tells(scoring.mark_dormant(df))
    assert dormant, "the mini corpus is expected to leave most tells dormant"
    assert f"{len(dormant)} of" in card
    assert f"`{dormant[0]}`" in card


def test_separation_reads_in_rank_order_with_its_interval(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    separation = card.split("### Separation")[1].split("## 2.")[0]
    assert f"`{LOUD}` over `{PLAIN}`" in separation
    assert "separated at 95%" in separation
    # The claim is always accompanied by the interval it rests on.
    assert "[" in separation and "]" in separation


def test_a_significance_claim_needs_an_interval_that_excludes_zero() -> None:
    boot = {
        "models": {},
        "deltas": {"a|b": {"point": 1.0, "lo": -3.0, "hi": 5.0, "significant": False}},
    }
    categories = sorted(scoring.CATEGORY_WEIGHTS)
    rollup = pd.DataFrame(
        [[0.1] * len(categories), [0.09] * len(categories)],
        index=["a", "b"],
        columns=categories,
    )
    index = pd.DataFrame(
        {"ai_tell_index": [10.0, 9.0], "signature_index": [float("nan")] * 2},
        index=["a", "b"],
    )
    rendered = "\n".join(report._headline({"corpus": {}}, rollup, index, boot, ["a", "b"]))
    assert "**not** separated at 95%" in rendered
    assert "the interval spans zero" in rendered


def test_a_stored_delta_is_flipped_rather_than_recomputed() -> None:
    deltas = {"a|b": {"point": 3.0, "lo": 1.0, "hi": 5.0, "significant": True}}
    flipped = report._delta(deltas, "b", "a")
    assert flipped["point"] == -3.0
    assert (flipped["lo"], flipped["hi"]) == (-5.0, -1.0)
    assert report._delta(deltas, "a", "b")["point"] == 3.0
    assert report._delta(deltas, "a", "c") is None


def test_the_scorecard_carries_no_timestamp(run_dir: Path) -> None:
    """It has to be byte-reproducible, so nothing wall-clock may leak in."""
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    manifest = manifest_mod.load_manifest(run_dir)
    assert manifest["run_id"] not in card
    assert manifest["created_utc"] not in card


def test_scorecard_can_be_rerendered_from_the_run_directory(run_dir: Path) -> None:
    before = (run_dir / report.SCORECARD_NAME).read_bytes()
    report.render_scorecard(run_dir)
    assert (run_dir / report.SCORECARD_NAME).read_bytes() == before


# --- manifest ----------------------------------------------------------------


def test_the_manifest_records_the_run(run_dir: Path, corpus: Path) -> None:
    manifest = manifest_mod.load_manifest(run_dir)
    registry = Registry(REGISTRY_PATH)
    assert manifest["corpus"]["root"] == str(corpus)
    assert manifest["corpus"]["n_docs"] == 8
    assert manifest["corpus"]["per_model"] == {LOUD: 4, PLAIN: 4}
    assert manifest["registry"]["version"] == registry.version
    assert manifest["registry"]["content_hash"] == registry.content_hash
    assert manifest["registry"]["judge_skipped"] == len(
        [t for t in registry.active_tells() if t.method == "judge"]
    )
    assert manifest["weights"]["categories"] == scoring.CATEGORY_WEIGHTS
    assert manifest["environment"]["python"]
    assert manifest["environment"]["pandas"]
    assert manifest["cli_args"] == ["score"]


def test_the_manifest_carries_enough_to_re_render_without_the_registry(
    run_dir: Path,
) -> None:
    manifest = manifest_mod.load_manifest(run_dir)
    tells = manifest["registry"]["tells"]
    sample = tells["lex.delve"]
    assert {"name", "category", "scope", "status", "weight", "unit"} <= set(sample)


# --- reproducibility ---------------------------------------------------------


def test_verify_passes_on_a_fresh_run(run_dir: Path) -> None:
    result = manifest_mod.verify(run_dir)
    assert result.ok, result.summary()
    assert set(manifest_mod.REPRODUCIBLE_OUTPUTS) <= set(result.checked)


def test_a_second_run_is_byte_identical(run_dir: Path, corpus: Path, tmp_path: Path) -> None:
    again = report.score_run(
        corpus_root=corpus,
        registry_path=REGISTRY_PATH,
        run_dir=tmp_path / "again",
        cli_args=["score"],
        bootstrap_n=200,
    )
    for name in manifest_mod.REPRODUCIBLE_OUTPUTS:
        assert (run_dir / name).read_bytes() == (again / name).read_bytes(), name


def test_verify_notices_an_edited_document(run_dir: Path, corpus: Path) -> None:
    (corpus / LOUD / "email-01.md").write_text("Completely different.\n", encoding="utf-8")
    result = manifest_mod.verify(run_dir)
    assert not result.ok
    assert any("corpus" in d for d in result.diffs)


def test_verify_notices_a_tampered_score_file(run_dir: Path) -> None:
    path = run_dir / report.SCORES_NAME
    rows = rows_of(run_dir)
    rows[0]["raw"] = 999.0
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8"
    )
    result = manifest_mod.verify(run_dir)
    assert not result.ok
    assert any(report.SCORES_NAME in d for d in result.diffs)


def test_verify_notices_a_moved_registry(run_dir: Path) -> None:
    manifest = manifest_mod.load_manifest(run_dir)
    manifest["registry"]["path"] = str(run_dir / "does-not-exist.yaml")
    manifest_mod.write_manifest(manifest, run_dir)
    result = manifest_mod.verify(run_dir)
    assert not result.ok
    assert any("registry missing" in d for d in result.diffs)


# --- CLI ---------------------------------------------------------------------


def test_cli_score_and_verify(corpus: Path, tmp_path: Path, capsys) -> None:
    runs = tmp_path / "runs"
    code = cli.main(
        [
            "--registry",
            str(REGISTRY_PATH),
            "score",
            "--corpus",
            str(corpus),
            "--out",
            str(runs),
            "--bootstrap",
            "100",
        ]
    )
    assert code == 0
    printed = capsys.readouterr().out.strip().splitlines()
    run_dir = Path(printed[-1])
    assert run_dir.is_dir()
    assert "judge tells skipped" in printed[0]

    assert cli.main(["report", "--verify", str(run_dir)]) == 0
    assert "VERIFIED" in capsys.readouterr().out


def test_cli_report_render(run_dir: Path, capsys) -> None:
    assert cli.main(["report", "--render", str(run_dir)]) == 0
    assert report.SCORECARD_NAME in capsys.readouterr().out


def test_cli_score_on_an_empty_corpus(tmp_path: Path, capsys) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    code = cli.main(
        [
            "--registry",
            str(REGISTRY_PATH),
            "score",
            "--corpus",
            str(empty),
            "--out",
            str(tmp_path / "runs"),
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "no documents" in captured.err
    run_dir = Path(captured.out.strip().splitlines()[-1])
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "No documents were scored" in card


def test_score_run_needs_somewhere_to_write(corpus: Path) -> None:
    with pytest.raises(ValueError):
        report.score_run(corpus_root=corpus, registry_path=REGISTRY_PATH)


def test_include_candidates_is_recorded_and_verifiable(corpus: Path, tmp_path: Path) -> None:
    run = report.score_run(
        corpus_root=corpus,
        registry_path=REGISTRY_PATH,
        run_dir=tmp_path / "candidates",
        include_candidates=True,
        bootstrap_n=100,
    )
    manifest = manifest_mod.load_manifest(run)
    assert manifest["registry"]["include_candidates"] is True
    # verify replays with the same flag, so the outputs still match byte for byte.
    assert manifest_mod.verify(run).ok


# --- serialization -----------------------------------------------------------


def test_scores_jsonl_trims_the_quote_list(tmp_path: Path) -> None:
    """Evidence is capped at 50 in memory and at 10 on disk, for file size."""
    df = pd.DataFrame(
        [
            {
                "doc_id": "m/memo-01",
                "model": "m",
                "format": "memo",
                "tell_id": "lex.a",
                "category": "lexical",
                "scope": "general",
                "method": "regex",
                "unit": "count",
                "raw": 20.0,
                "rate_per_1k": 40.0,
                "score": 1.0,
                "matches": [{"quote": f"q{i}", "line": i + 1} for i in range(20)],
                "detail": {},
            }
        ]
    )
    path = report.write_scores_jsonl(df, tmp_path / "scores.jsonl")
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["raw"] == 20.0  # the count is not trimmed
    assert len(row["matches"]) == report.MATCHES_IN_JSONL


def test_scores_jsonl_writes_nan_as_null_and_rounds(tmp_path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                "doc_id": "m/memo-01",
                "model": "m",
                "format": "memo",
                "tell_id": "sta.a",
                "category": "statistical",
                "scope": "general",
                "method": "statistic",
                "unit": "value",
                "raw": float("nan"),
                "rate_per_1k": None,
                "score": 1.0 / 3.0,
                "matches": [],
                "detail": {"stat": "mattr_500"},
            }
        ]
    )
    path = report.write_scores_jsonl(df, tmp_path / "scores.jsonl")
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["raw"] is None
    assert row["rate_per_1k"] is None
    assert row["score"] == 0.333333
    assert row["detail"] == {"stat": "mattr_500"}


def test_scores_jsonl_is_written_in_a_fixed_order(run_dir: Path) -> None:
    rows = rows_of(run_dir)
    keys = [(r["doc_id"], r["tell_id"]) for r in rows]
    assert keys == sorted(keys)
    assert list(rows[0]) == list(report.SCORE_FIELDS)


# --- the exploratory annex ---------------------------------------------------


ANNEX_PIECE = """# Notes on a Kitchen Window

The light comes in at four and stays until the pans are dry. I have never
timed it, but I know when it goes.

Some mornings the sill is warm enough to sit on, and the cat does. Other
mornings it is not, and she looks at me as though I arranged it.
"""


@pytest.fixture
def corpus_with_annex(corpus: Path) -> Path:
    for model in (LOUD, PLAIN):
        for index in (1, 2):
            (corpus / model / f"free-writing-{index:02d}.md").write_text(
                ANNEX_PIECE, encoding="utf-8"
            )
    return corpus


def test_the_annex_lands_in_the_per_document_rows(corpus_with_annex: Path, tmp_path: Path) -> None:
    run_dir = report.score_run(
        corpus_root=corpus_with_annex,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs",
        bootstrap_n=50,
    )
    rows = rows_of(run_dir)
    annex = [r for r in rows if r["format"] == "free-writing"]
    assert annex, "Tier-1 detection still runs on the annex"
    assert {r["doc_id"] for r in annex} == {
        f"{m}/free-writing-{i:02d}" for m in (LOUD, PLAIN) for i in (1, 2)
    }


def test_the_annex_is_its_own_rows_in_the_by_format_matrix_only(
    corpus_with_annex: Path, tmp_path: Path
) -> None:
    run_dir = report.score_run(
        corpus_root=corpus_with_annex,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs",
        bootstrap_n=50,
    )
    by_format = pd.read_csv(run_dir / report.MATRIX_BY_FORMAT_NAME)
    assert "free-writing" in set(by_format["format"])
    # matrix.csv is a per-model average with nowhere to put an annex document.
    per_model = pd.read_csv(run_dir / report.MATRIX_NAME)
    assert list(per_model.columns)[0] == "model"
    assert set(per_model["model"]) == {LOUD, PLAIN}


def test_the_annex_does_not_move_the_index(corpus: Path, tmp_path: Path) -> None:
    """The headline number is the same corpus with and without the annex."""
    without = report.score_run(
        corpus_root=corpus,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs-a",
        bootstrap_n=50,
    )
    for model in (LOUD, PLAIN):
        (corpus / model / "free-writing-01.md").write_text(ANNEX_PIECE, encoding="utf-8")
    with_annex = report.score_run(
        corpus_root=corpus,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs-b",
        bootstrap_n=50,
    )

    meta = scoring.tell_meta(manifest_mod.load_manifest(without)["registry"]["tells"])
    before = scoring.indices(report.read_scores_jsonl(without / report.SCORES_NAME), meta)
    after = scoring.indices(report.read_scores_jsonl(with_annex / report.SCORES_NAME), meta)
    for model in (LOUD, PLAIN):
        assert after.loc[model, "ai_tell_index"] == pytest.approx(
            before.loc[model, "ai_tell_index"]
        )


def test_the_scorecard_reports_the_annex_in_its_own_section(
    corpus_with_annex: Path, tmp_path: Path
) -> None:
    run_dir = report.score_run(
        corpus_root=corpus_with_annex,
        registry_path=REGISTRY_PATH,
        out_root=tmp_path / "runs",
        bootstrap_n=50,
    )
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "## 7. Exploratory annex" in card
    assert "excluded from the AI-Tell Index" in card
    # Section 2 is the index by format; the annex has no index, so no column.
    heat = card.split("## 2. Index by format")[1].split("## 3.")[0]
    assert "free-writing" not in heat


def test_a_corpus_without_an_annex_renders_no_annex_section(run_dir: Path) -> None:
    card = (run_dir / report.SCORECARD_NAME).read_text(encoding="utf-8")
    assert "Exploratory annex" not in card
