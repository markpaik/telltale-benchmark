"""Text utilities and the 18 registered statistics.

Every expected value here is worked out by hand from a small fixture and written
as arithmetic, not as a number copied back out of the implementation.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from telltale import textstats as ts
from telltale.corpus import Doc
from telltale.registry import Registry

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "tells.yaml"


def make(text: str, fmt: str = "memo", doc_id: str = "test-model/memo-01") -> Doc:
    return Doc.from_text(doc_id, "test-model", fmt, text)


# --- strip_markdown ----------------------------------------------------------

RICH_MARKDOWN = """# Quarterly Attendance Update

Intro with **bold**, *italic*, `inline_code`, a [dashboard link](https://example.org/dash),
and an image ![chart](chart.png).

## Findings

> Chronic absence fell two points.

- First finding
- Second finding

1. Numbered one
2. Numbered two

| Grade | Rate |
|-------|------|
| K     | 91.2 |
| 1     | 90.4 |

```python
secretcode = "never prose"
print("| pipe inside a fence |")
```

---

Closing paragraph.
"""


def test_strip_markdown_drops_fenced_code() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "secretcode" not in plain
    assert "never prose" not in plain
    assert "```" not in plain


def test_strip_markdown_drops_table_rows() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "|" not in plain
    assert "Grade" not in plain
    assert "91.2" not in plain


def test_strip_markdown_keeps_link_text_and_drops_urls() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "dashboard link" in plain
    assert "example.org" not in plain


def test_strip_markdown_drops_images_entirely() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "chart" not in plain


def test_strip_markdown_keeps_heading_text_without_markers() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "Quarterly Attendance Update" in plain
    assert "Findings" in plain
    assert "#" not in plain


def test_strip_markdown_drops_emphasis_markers_keeps_words() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "Intro with bold, italic, inline_code" in plain
    assert "**" not in plain
    assert "*" not in plain


def test_strip_markdown_keeps_blockquote_and_list_text() -> None:
    plain = ts.strip_markdown(RICH_MARKDOWN)
    assert "Chronic absence fell two points." in plain
    assert ">" not in plain
    assert "First finding\nSecond finding" in plain
    assert "Numbered one\nNumbered two" in plain
    assert "1." not in plain


def test_strip_markdown_drops_horizontal_rules() -> None:
    assert ts.strip_markdown("a\n\n---\n\nb") == "a\n\nb"
    assert ts.strip_markdown("a\n\n***\n\nb") == "a\n\nb"
    assert ts.strip_markdown("a\n\n___\n\nb") == "a\n\nb"


def test_strip_markdown_collapses_blank_runs() -> None:
    assert ts.strip_markdown("one\n\n\n\n\ntwo") == "one\n\ntwo"


def test_strip_markdown_keeps_a_prose_line_with_a_stray_pipe() -> None:
    """Only a run that looks like a table is dropped, not any line with a pipe."""
    assert ts.strip_markdown("Use the a | b syntax here.") == "Use the a | b syntax here."


def test_strip_markdown_is_idempotent() -> None:
    once = ts.strip_markdown(RICH_MARKDOWN)
    assert ts.strip_markdown(once) == once


@pytest.mark.parametrize(
    "source",
    [
        RICH_MARKDOWN,
        "# H1\n## H2\n### H3\n",
        "- a\n- b\n\n1. c\n2. d\n",
        "***triple emphasis*** and ~~struck~~ text",
        "> quote\n> more quote\n",
        "| a | b |\n|---|---|\n| 1 | 2 |\n",
        "```\nunclosed fence\n",
        "text with snake_case_names and 3 * 4 * 5 arithmetic",
        "",
        "\n\n\n",
    ],
)
def test_strip_markdown_idempotent_across_shapes(source: str) -> None:
    once = ts.strip_markdown(source)
    assert ts.strip_markdown(once) == once


def test_strip_markdown_does_not_eat_snake_case_or_multiplication() -> None:
    plain = ts.strip_markdown("text with snake_case_names and 3 * 4 * 5 arithmetic")
    assert plain == "text with snake_case_names and 3 * 4 * 5 arithmetic"


@pytest.mark.parametrize(
    "text",
    [
        "3*4*5",  # unspaced arithmetic is not emphasis
        "qty*price*2",
        "the formula is n*m*k here",
        "2*3",
    ],
)
def test_strip_markdown_leaves_unspaced_arithmetic_alone(text: str) -> None:
    assert ts.strip_markdown(text) == text


@pytest.mark.parametrize(
    "text,expected",
    [
        ("*emphasis*", "emphasis"),
        ("an *emphatic* word", "an emphatic word"),
        ("(*emphatic*)", "(emphatic)"),
        ("**bold** and *italic*", "bold and italic"),
    ],
)
def test_strip_markdown_still_removes_real_italics(text: str, expected: str) -> None:
    assert ts.strip_markdown(text) == expected


def test_strip_markdown_handles_urls_containing_parens() -> None:
    """A Wikipedia-style disambiguation target must not leak into the prose."""
    text = "See [the article](https://en.wikipedia.org/wiki/Example_(disambiguation)) today."
    assert ts.strip_markdown(text) == "See the article today."


def test_strip_markdown_handles_images_with_parens_in_the_url() -> None:
    assert ts.strip_markdown("Before ![chart](https://x.org/a_(b).png) after") == "Before  after"


# --- split_sentences ---------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        # titles
        ("Dr. Smith met Mrs. Lee.", 1),
        ("Prof. Adams and Ms. Ruiz saw Mr. Diaz.", 1),
        ("Sr. Vega and Jr. Vega met at St. Mary.", 1),
        # latin and clerical abbreviations
        ("The vote was 12 vs. 4 in favor. It passed.", 2),
        ("Pick a lead metric, e.g. Attendance, and hold to it.", 1),
        ("One measure, i.e. Attendance, drives the rest.", 1),
        ("cf. Smith 2019 for the method. It holds.", 2),
        ("approx. 40 staff attended. The room was full.", 2),
        ("Founded est. 2019 by two teachers. It grew fast.", 2),
        ("Ask the dept. Anna will follow up.", 1),
        ("See No. 5 in the table. It shows the trend.", 2),
        # company suffixes
        ("Acme Inc. and Beta Corp. signed. Gamma Ltd. and Delta Co. did not.", 2),
        # dotted initialisms
        ("The U.S. economy grew. The U.K. lagged.", 2),
        ("She holds a Ph.D. and an M.A. from 2019. He holds a B.A. too.", 2),
        # months
        ("The report is due Jan. 15 and covers Dec. 31 totals. Feb. 1 is the backup.", 2),
        # single initials
        ("J. Smith wrote the memo. A. Jones signed it.", 2),
        # decimals
        ("Revenue grew 3.5 percent. Costs fell 1.2 percent.", 2),
        ("The rate was 91.4 percent in 2024.", 1),
        # ordinary terminators
        ("Is the plan ready? Yes! Ship it now.", 3),
        ("One. Two. Three.", 3),
        # hard paragraph boundary, no terminator needed
        ("First block\n\nSecond block", 2),
    ],
)
def test_split_sentences_counts(text: str, expected: int) -> None:
    assert len(ts.split_sentences(text)) == expected


def test_split_sentences_does_not_split_inside_us_economy() -> None:
    """The single case the spec calls out by name."""
    assert ts.split_sentences("The U.S. economy grew last year.") == [
        "The U.S. economy grew last year."
    ]


def test_split_sentences_keeps_quoted_endings_whole() -> None:
    assert ts.split_sentences('She said "We will win." Then she left.') == [
        'She said "We will win."',
        "Then she left.",
    ]
    assert ts.split_sentences("He asked, 'Why now?' The team paused.") == [
        "He asked, 'Why now?'",
        "The team paused.",
    ]


def test_split_sentences_normalizes_internal_whitespace() -> None:
    assert ts.split_sentences("One sentence\nwrapped across lines. Two follows.") == [
        "One sentence wrapped across lines.",
        "Two follows.",
    ]


def test_sentence_final_abbreviation_merges_by_design() -> None:
    """Documented behavior: an abbreviation that really did end the sentence is
    merged into the next one. Under-splitting is the cheaper error — the guard
    exists so "U.S. Department" never becomes two sentences."""
    assert ts.split_sentences("Bring pens, paper, etc. The meeting starts at nine.") == [
        "Bring pens, paper, etc. The meeting starts at nine."
    ]


def test_lowercase_after_a_period_does_not_split_by_design() -> None:
    """Documented behavior: the splitter requires a capital or digit opener."""
    assert len(ts.split_sentences("The build shipped. it worked.")) == 1


def test_split_sentences_drops_empties_and_trims() -> None:
    assert ts.split_sentences("   \n\n  ") == []
    assert ts.split_sentences("  Padded sentence.  ") == ["Padded sentence."]


# --- split_paragraphs / word_count -------------------------------------------


def test_split_paragraphs() -> None:
    text = "  First para\nstill first.  \n\n\nSecond para.\n\n   \n\nThird."
    assert ts.split_paragraphs(text) == ["First para\nstill first.", "Second para.", "Third."]
    assert ts.split_paragraphs("") == []


def test_word_count() -> None:
    assert ts.word_count("one two three") == 3
    assert ts.word_count("school-based data-driven") == 2  # hyphens stay inside a word
    assert ts.word_count("don't stop; keep going!") == 4
    assert ts.word_count("Q1 2024 rose 3.5 points") == 6  # "3" and "5" split on the period
    assert ts.word_count("") == 0


@pytest.mark.parametrize(
    "text,expected",
    [
        ("a - b", 2),  # a lone spaced hyphen is punctuation, not a word
        ("one — two", 2),
        ("fast-paced", 1),  # a hyphenated compound is one word
        ("a fast-paced state-by-state rollout", 4),
        ("-5 degrees", 2),
        ("well- known", 2),  # a dangling hyphen joins nothing
        ("2022-2023", 1),
        ("- - -", 0),
    ],
)
def test_word_count_treats_hyphens_as_joiners_only(text: str, expected: int) -> None:
    assert ts.word_count(text) == expected


# --- stat registry -----------------------------------------------------------


def test_eighteen_stats_are_registered() -> None:
    assert len(ts.STATS) == 18
    assert all(callable(fn) for fn in ts.STATS.values())


def test_registry_stat_names_all_resolve() -> None:
    """Every statistic tell in tells.yaml points at a function that exists."""
    registry = Registry(REGISTRY_PATH)
    named = {t.stat for t in registry if t.method == "statistic"}
    assert named == set(ts.STATS)


def test_stat_decorator_rejects_duplicates() -> None:
    with pytest.raises(ValueError):
        ts.stat("em_dash_per_1k")(lambda doc: 0.0)


def test_compute_runs_a_stat_by_name() -> None:
    doc = make("Alpha; beta gamma delta.")
    assert ts.compute("semicolon_per_1k", doc) == pytest.approx(1000.0 / 4)


# --- 1-2: punctuation rates --------------------------------------------------


def test_em_dash_per_1k() -> None:
    # 8 words: Alpha, beta, and, gamma, delta, plus, epsilon, zeta. The lone
    # spaced hyphen is punctuation, not a word — it used to tokenize as one and
    # inflate the denominator of every per-1k rate.
    # 3 dash forms: em dash, letter-flanked en dash, letter-flanked hyphen.
    doc = make("Alpha — beta and gamma – delta plus epsilon - zeta.")
    assert doc.words == 8
    assert ts.STATS["em_dash_per_1k"](doc) == pytest.approx(1000.0 * 3 / 8)


def test_em_dash_ignores_unspaced_hyphens() -> None:
    doc = make("A school-based data-driven plan.")
    assert ts.STATS["em_dash_per_1k"](doc) == pytest.approx(0.0)


@pytest.mark.parametrize(
    "text,dashes",
    [
        ("pages 3 - 5", 0),  # numeric range, not a dash
        ("FY 2022 - 2023", 0),
        ("3–5 students", 0),  # digit-flanked en dash
        ("the range is 3–5–7 across grades", 0),
        ("the plan — ambitious as it is — hinges on Q3", 2),
        ("a sharp change - not a small one - in retention", 2),
        ("the New York - Boston route", 1),  # accepted residual noise
    ],
)
def test_dash_counting_excludes_numeric_ranges(text: str, dashes: int) -> None:
    doc = make(text)
    assert ts.STATS["em_dash_per_1k"](doc) == pytest.approx(1000.0 * dashes / doc.words)


def test_a_range_heavy_document_scores_zero_dashes() -> None:
    """The construct-validity case: ranges everywhere, no dash habit at all."""
    doc = make(
        "Grades 3 - 5 improved. Cohorts 2020 - 2021 and 2022 - 2023 held. "
        "See pages 12 - 18 and rows 4–9 for the detail."
    )
    assert ts.STATS["em_dash_per_1k"](doc) == pytest.approx(0.0)


def test_semicolon_per_1k() -> None:
    doc = make("Alpha; beta; gamma delta.")  # 4 words, 2 semicolons
    assert doc.words == 4
    assert ts.STATS["semicolon_per_1k"](doc) == pytest.approx(1000.0 * 2 / 4)


# --- 3-6: rhetoric -----------------------------------------------------------

# Ten sentences: five of 5 words, five of 3 words. Three commas.
TEN_SENTENCES = [
    "While costs rose, service held.",
    "While budgets fell, staffing grew.",
    "However, the board approved it.",
    "The team shipped the product.",
    "The team missed the deadline.",
    "Costs fell again.",
    "Results improved sharply.",
    "Staff turnover dropped.",
    "Funding stayed flat.",
    "Outcomes held steady.",
]
SENTENCE_TEXT = " ".join(TEN_SENTENCES)
NINE_SENTENCES = " ".join(TEN_SENTENCES[:9])


@pytest.fixture
def sentence_doc() -> Doc:
    return make(SENTENCE_TEXT)


@pytest.fixture
def short_doc() -> Doc:
    """Nine sentences — one under every sentence floor."""
    return make(NINE_SENTENCES)


def test_the_sentence_fixture_is_what_we_think_it_is(sentence_doc: Doc, short_doc: Doc) -> None:
    lengths = [ts.word_count(s) for s in ts.split_sentences(sentence_doc.plain)]
    assert lengths == [5, 5, 5, 5, 5, 3, 3, 3, 3, 3]
    assert sentence_doc.words == 40
    assert sentence_doc.plain.count(",") == 3
    assert len(ts.split_sentences(short_doc.plain)) == 9


def test_pct_sentences_starting_while(sentence_doc: Doc) -> None:
    assert ts.STATS["pct_sentences_starting_while"](sentence_doc) == pytest.approx(20.0)


def test_pct_sentences_starting_while_is_case_sensitive() -> None:
    text = SENTENCE_TEXT.replace("While costs", "while costs")
    assert ts.STATS["pct_sentences_starting_while"](make(text)) == pytest.approx(10.0)


def test_pct_sentences_starting_however(sentence_doc: Doc) -> None:
    assert ts.STATS["pct_sentences_starting_however"](sentence_doc) == pytest.approx(10.0)


def test_transition_words_per_1k() -> None:
    doc = make(
        "Moreover, furthermore, additionally, consequently, therefore, "
        "thus, hence, in addition, notably, ultimately."
    )
    # 11 words ("in addition" is two), 10 marker hits.
    assert doc.words == 11
    assert ts.STATS["transition_words_per_1k"](doc) == pytest.approx(1000.0 * 10 / 11)


def test_transition_words_respect_word_boundaries() -> None:
    doc = make("Thusly the authors hence moved therefore onward.")  # 2 hits in 7 words
    assert doc.words == 7
    assert ts.STATS["transition_words_per_1k"](doc) == pytest.approx(1000.0 * 2 / 7)


def test_anaphora_share(sentence_doc: Doc) -> None:
    # 9 adjacent pairs; only "the team" / "the team" repeats.
    assert ts.STATS["anaphora_share"](sentence_doc) == pytest.approx(100.0 / 9)


def test_anaphora_share_all_pairs() -> None:
    text = " ".join(["The team shipped the product."] * 10)
    assert ts.STATS["anaphora_share"](make(text)) == pytest.approx(100.0)


# --- 7-12: structure ---------------------------------------------------------

STRUCTURE_MD = """# Title

## Section

- one two
- three four
- five six

**Bold one** and **bold two** here.
"""


@pytest.fixture
def structure_doc() -> Doc:
    return make(STRUCTURE_MD)


def test_structure_fixture_word_count(structure_doc: Doc) -> None:
    # 2 heading words + 6 list words + 6 words in the closing line.
    assert structure_doc.words == 14


def test_headings_per_1k(structure_doc: Doc) -> None:
    assert ts.STATS["headings_per_1k"](structure_doc) == pytest.approx(1000.0 * 2 / 14)


def test_bullet_lines_per_1k(structure_doc: Doc) -> None:
    assert ts.STATS["bullet_lines_per_1k"](structure_doc) == pytest.approx(1000.0 * 3 / 14)


def test_bold_spans_per_1k(structure_doc: Doc) -> None:
    assert ts.STATS["bold_spans_per_1k"](structure_doc) == pytest.approx(1000.0 * 2 / 14)


def test_paragraph_length_cv() -> None:
    doc = make("one two\n\nthree four five six\n\nseven eight nine ten eleven twelve")
    # counts 2, 4, 6 -> mean 4, population variance (4+0+4)/3 = 8/3
    assert ts.STATS["paragraph_length_cv"](doc) == pytest.approx(math.sqrt(8 / 3) / 4)


def test_paragraph_length_cv_is_zero_for_uniform_paragraphs() -> None:
    doc = make("one two\n\nthree four\n\nfive six")
    assert ts.STATS["paragraph_length_cv"](doc) == pytest.approx(0.0)


def test_section_length_cv() -> None:
    doc = make(
        "Intro line here.\n\n"
        "## A\n\nalpha beta\n\n"
        "## B\n\ngamma\n\n"
        "## C\n\ndelta epsilon zeta\n"
    )
    # sections: preamble 3 words, then 1+2, 1+1, 1+3 -> [3, 3, 2, 4], mean 3,
    # population variance (0+0+1+1)/4 = 0.5
    assert ts.STATS["section_length_cv"](doc) == pytest.approx(math.sqrt(0.5) / 3)


def test_section_length_cv_ignores_an_empty_preamble() -> None:
    doc = make("## A\n\nalpha beta\n\n## B\n\ngamma\n\n## C\n\ndelta epsilon zeta\n")
    # [3, 2, 4] -> mean 3, variance (0+1+1)/3 = 2/3
    assert ts.STATS["section_length_cv"](doc) == pytest.approx(math.sqrt(2 / 3) / 3)


def test_pct_lists_exactly_three() -> None:
    doc = make(
        "- a\n- b\n- c\n\n"
        "Prose paragraph.\n\n"
        "- d\n- e\n\n- f\n\n"  # one single blank line inside: still one list
        "Prose again.\n\n"
        "- g\n- h\n- i\n- j\n"
    )
    # runs of 3, 3, 4 -> two of three
    assert ts.STATS["pct_lists_exactly_three"](doc) == pytest.approx(100.0 * 2 / 3)


def test_pct_lists_exactly_three_splits_on_a_double_blank() -> None:
    doc = make("- a\n- b\n- c\n\n\n- d\n- e\n")
    assert ts.STATS["pct_lists_exactly_three"](doc) == pytest.approx(50.0)


def test_pct_lists_exactly_three_all_threes() -> None:
    doc = make("- a\n- b\n- c\n\nProse.\n\n- d\n- e\n- f\n")
    assert ts.STATS["pct_lists_exactly_three"](doc) == pytest.approx(100.0)


# --- 13-18: sentence-level statistics ----------------------------------------


def test_sentence_length_cv(sentence_doc: Doc) -> None:
    # lengths 5x5 and 5x3 -> mean 4, every deviation 1 -> std 1 -> cv 0.25
    assert ts.STATS["sentence_length_cv"](sentence_doc) == pytest.approx(0.25)


def test_sentence_length_band_distance_below_the_band(sentence_doc: Doc) -> None:
    assert ts.STATS["sentence_length_band_distance"](sentence_doc) == pytest.approx(10.0)


def test_sentence_length_band_distance_inside_the_band() -> None:
    sentence = "Word0 " + " ".join(f"word{i}" for i in range(1, 16)) + "."  # 16 words
    doc = make(" ".join([sentence] * 10))
    assert ts.word_count(sentence) == 16
    assert ts.STATS["sentence_length_band_distance"](doc) == pytest.approx(0.0)


def test_sentence_length_band_distance_above_the_band() -> None:
    sentence = "Word0 " + " ".join(f"word{i}" for i in range(1, 25)) + "."  # 25 words
    doc = make(" ".join([sentence] * 10))
    assert ts.word_count(sentence) == 25
    assert ts.STATS["sentence_length_band_distance"](doc) == pytest.approx(3.0)


def test_mattr_falls_back_to_plain_ttr_under_one_window() -> None:
    doc = make("alpha beta gamma delta epsilon zeta eta theta iota kappa " * 6)
    # 60 tokens, 10 types
    assert ts.STATS["mattr_500"](doc) == pytest.approx(10 / 60)


def test_mattr_over_a_full_window_of_one_repeated_token() -> None:
    doc = make("x " * 600)  # every 500-token window holds a single type
    assert ts.STATS["mattr_500"](doc) == pytest.approx(1 / 500)


def test_mattr_over_a_full_window_of_all_distinct_tokens() -> None:
    doc = make(" ".join(f"w{i}" for i in range(600)))
    assert ts.STATS["mattr_500"](doc) == pytest.approx(1.0)


def test_mattr_is_case_insensitive() -> None:
    doc = make("Alpha alpha ALPHA " * 20)  # 60 tokens, 1 type
    assert ts.STATS["mattr_500"](doc) == pytest.approx(1 / 60)


def test_ly_adverbs_per_1k() -> None:
    doc = make("Quickly, the sharply written report was only fairly notably good.")
    # 10 words; quickly, sharply, fairly, notably match; "only" is too short
    assert doc.words == 10
    assert ts.STATS["ly_adverbs_per_1k"](doc) == pytest.approx(400.0)


def test_commas_per_sentence(sentence_doc: Doc) -> None:
    assert ts.STATS["commas_per_sentence"](sentence_doc) == pytest.approx(3 / 10)


def test_sentence_opener_diversity(sentence_doc: Doc) -> None:
    # openers: while, while, however, the, the, costs, results, staff, funding,
    # outcomes -> 8 distinct over 10 sentences
    assert ts.STATS["sentence_opener_diversity"](sentence_doc) == pytest.approx(0.8)


def test_sentence_opener_diversity_is_one_when_every_opener_differs() -> None:
    starts = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]
    doc = make(" ".join(f"{s} held steady." for s in starts))
    assert ts.STATS["sentence_opener_diversity"](doc) == pytest.approx(1.0)


# --- floors ------------------------------------------------------------------

SENTENCE_FLOOR_STATS = [
    "pct_sentences_starting_while",
    "pct_sentences_starting_however",
    "anaphora_share",
    "sentence_length_cv",
    "sentence_length_band_distance",
    "commas_per_sentence",
    "sentence_opener_diversity",
]

RATE_STATS = [
    "em_dash_per_1k",
    "semicolon_per_1k",
    "transition_words_per_1k",
    "headings_per_1k",
    "bullet_lines_per_1k",
    "bold_spans_per_1k",
    "ly_adverbs_per_1k",
]


@pytest.mark.parametrize("name", SENTENCE_FLOOR_STATS)
def test_sentence_floor_is_nan_under_ten_sentences(name: str, short_doc: Doc) -> None:
    assert math.isnan(ts.STATS[name](short_doc))


@pytest.mark.parametrize("name", SENTENCE_FLOOR_STATS)
def test_sentence_floor_is_met_at_exactly_ten(name: str, sentence_doc: Doc) -> None:
    assert not math.isnan(ts.STATS[name](sentence_doc))


@pytest.mark.parametrize("name", RATE_STATS)
def test_rate_stats_are_nan_for_an_empty_document(name: str) -> None:
    assert math.isnan(ts.STATS[name](make("")))


def test_paragraph_length_cv_floor() -> None:
    assert math.isnan(ts.STATS["paragraph_length_cv"](make("one two\n\nthree four")))
    assert not math.isnan(ts.STATS["paragraph_length_cv"](make("a\n\nb c\n\nd e f")))


def test_section_length_cv_floor() -> None:
    assert math.isnan(ts.STATS["section_length_cv"](make("## A\n\nalpha\n\n## B\n\nbeta\n")))
    assert math.isnan(ts.STATS["section_length_cv"](make("No headings at all.")))


def test_pct_lists_exactly_three_floor() -> None:
    assert math.isnan(ts.STATS["pct_lists_exactly_three"](make("Prose only, no lists.")))


def test_mattr_floor() -> None:
    assert math.isnan(ts.STATS["mattr_500"](make("word " * 49)))
    assert not math.isnan(ts.STATS["mattr_500"](make("word " * 50)))


# --- robustness --------------------------------------------------------------

WEIRD_INPUTS = [
    "",
    "   \n\n\t\n",
    "```\nunclosed fence with words\n",
    "!!! ??? ... ;;; ,,,",
    "| a | b |\n|---|---|\n",
    "#" * 200,
    "word" * 500,
    "—" * 50,
    "   odd unicode  ",
    "# Heading with no body\n",
]


@pytest.mark.parametrize("text", WEIRD_INPUTS)
@pytest.mark.parametrize("name", sorted(ts.STATS))
def test_no_stat_raises_on_weird_input(name: str, text: str) -> None:
    value = ts.STATS[name](make(text))
    assert isinstance(value, float)


@pytest.mark.parametrize("text", WEIRD_INPUTS)
def test_utilities_do_not_raise_on_weird_input(text: str) -> None:
    plain = ts.strip_markdown(text)
    assert ts.strip_markdown(plain) == plain
    ts.split_sentences(plain)
    ts.split_paragraphs(plain)
    assert ts.word_count(plain) >= 0
    ts.doc_skeleton(make(text))


# --- doc_skeleton ------------------------------------------------------------

SKELETON_MD = """# Quarterly Update

Attendance rose two points this quarter. The gain held across all grade bands.

## Rollout Plan

- Hire two more school-based data analysts this spring
- Publish the dashboard
- Train principals

We will report again in October.
"""

SKELETON_EXPECTED = """SKELETON claude-opus-5/memo-04
format: memo
words: 36

OUTLINE
H1: Quarterly Update
PARA: 13w | Attendance rose two points this quarter.
H2: Rollout Plan
LIST: 3 items
  - Hire two more school-based data analysts...
  - Publish the dashboard
  - Train principals
PARA: 6w | We will report again in October.

FIRST PARAGRAPH
Attendance rose two points this quarter. The gain held across all grade bands.

LAST PARAGRAPH
We will report again in October."""


def test_doc_skeleton_golden() -> None:
    doc = Doc.from_text("claude-opus-5/memo-04", "claude-opus-5", "memo", SKELETON_MD)
    assert ts.doc_skeleton(doc) == SKELETON_EXPECTED


def test_doc_skeleton_is_deterministic() -> None:
    doc = Doc.from_text("claude-opus-5/memo-04", "claude-opus-5", "memo", SKELETON_MD)
    assert ts.doc_skeleton(doc) == ts.doc_skeleton(doc)


def test_doc_skeleton_drops_code_and_tables() -> None:
    doc = make(
        "# T\n\nProse here.\n\n```\nsecretcode = 1\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"
    )
    skeleton = ts.doc_skeleton(doc)
    assert "secretcode" not in skeleton
    assert "a | b" not in skeleton  # the only pipes left are the PARA separator
    assert "---" not in skeleton


def test_doc_skeleton_handles_an_empty_document() -> None:
    skeleton = ts.doc_skeleton(make(""))
    assert "OUTLINE\n(empty)" in skeleton
    assert "FIRST PARAGRAPH\n(none)" in skeleton
    assert "LAST PARAGRAPH\n(none)" in skeleton


# --- line classification (protocol v3) ---------------------------------------

#: (line, expected class). Every fixture is a shape that showed up in the cached
#: real-corpus extractions the M8d cost fix was measured against.
LINE_FIXTURES = [
    ("", "blank"),
    ("   \t ", "blank"),
    ("---", "rule"),
    ("***", "rule"),
    ("# Executive summary", "heading"),
    ("### Findings ###", "heading"),
    ("   ## Indented but still a heading", "heading"),
    ("- a bulleted item", "list_item"),
    ("* another one", "list_item"),
    ("  3. a numbered item", "list_item"),
    ("2) a paren-numbered item", "list_item"),
    ("[x] a bare checkbox", "list_item"),
    ("| Site | Cost |", "table_row"),
    ("|------|------|", "table_row"),
    ("| Ashford Lane | $1.3M", "table_row"),
    ("**Bold run-in heading**", "heading"),
    ("__Underscore heading__:", "heading"),
    ("**Scope:** the pilot covers four sites.", "heading"),
    ("Dear Amara,", "signoff"),
    ("Hi team,", "signoff"),
    ("Best regards,", "signoff"),
    ("Thanks —", "signoff"),
    ("Sincerely", "signoff"),
    ("— Priya Raman, Director of Analytics", "signoff"),
    ("March 4, 2026", "signoff"),
    ("2026-03-04", "signoff"),
    ("Note: the vendor missed the window.", "caption"),
    ("Figure 3: enrollment by building", "caption"),
    ("Action: confirm the cutover date.", "caption"),
    ("Subject: Q3 platform review", "caption"),
    ("Owner — Facilities", "caption"),
    ("The reconciliation script wrote to the wrong column.", "prose"),
    ("Six weeks.", "prose"),
    ("Not anymore.", "prose"),
    ("Thanks for turning that around so quickly.", "prose"),
    ("We moved from a manual process to an automated one.", "prose"),
]


@pytest.mark.parametrize("line,expected", LINE_FIXTURES)
def test_classify_line(line: str, expected: str) -> None:
    assert ts.classify_line(line) == expected


def test_every_class_it_returns_is_declared() -> None:
    for line, expected in LINE_FIXTURES:
        assert expected in ts.LINE_CLASSES
    assert "prose" in ts.LINE_CLASSES


def test_classify_line_is_the_conservative_direction() -> None:
    """Anything it is unsure about is prose, so the span goes to the judge."""
    for line in (
        "A fragment. And then the sentence it leans on.",
        "12 percent of sites reported the same failure.",
        "e.g. the vendor's own log",
        "Table stakes for any vendor: a working export.",
    ):
        assert ts.classify_line(line) == "prose"


def test_line_classes_walks_a_passage() -> None:
    assert ts.line_classes("# T\n\n- one\nprose\n") == [
        "heading",
        "blank",
        "list_item",
        "prose",
        "blank",
    ]


def test_class_of_line_is_one_based_and_survives_a_bad_number() -> None:
    text = "# T\nprose\n"
    assert ts.class_of_line(text, 1) == "heading"
    assert ts.class_of_line(text, 2) == "prose"
    assert ts.class_of_line(text, 0) == "blank"
    assert ts.class_of_line(text, 99) == "blank"


def test_runin_heading_end_needs_text_after_the_bold() -> None:
    # The offset runs to the start of the paragraph text, trailing space and all.
    assert ts.runin_heading_end("**Grade crossings.** Thirteen crossings.") == 21
    assert ts.runin_heading_end("**Grade crossings.**") == 0  # a whole-line heading
    assert ts.runin_heading_end("Ordinary prose about **bold** words.") == 0
    # Several bold spans and their separators all count as the run-in.
    line = "**4:05 p.m.** — **Restart issued.** The operator invokes the tooling."
    assert ts.runin_heading_end(line) == line.index("The operator")


def test_classify_span_splits_a_run_in_heading_from_its_paragraph() -> None:
    """The dominant real-corpus shape: heading and paragraph on one line."""
    text = "Intro.\n\n**Grade crossings.** Thirteen crossings need work.\n"
    start = text.index("**Grade")
    assert ts.classify_span(text, start, start + len("**Grade crossings.**")) == "heading"
    body = text.index("Thirteen")
    assert ts.classify_span(text, body, body + len("Thirteen crossings need work.")) == "prose"
    # The line itself is prose — the split is a property of the span, not the line.
    assert ts.classify_line("**Grade crossings.** Thirteen crossings need work.") == "prose"


def test_classify_span_takes_the_line_class_otherwise() -> None:
    text = "# Heading here\n- a bullet\nplain prose\n"
    assert ts.classify_span(text, 2, 9) == "heading"
    assert ts.classify_span(text, text.index("a bullet"), text.index("a bullet") + 8) == "list_item"
    assert ts.classify_span(text, text.index("plain"), text.index("plain") + 5) == "prose"
    assert ts.classify_span(text, -1, 3) == "blank"
