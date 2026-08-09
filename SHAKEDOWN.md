# Shakedown findings

The shakedown put the whole telltale pipeline through one full pass on a frozen
224-document corpus (112 Opus 5, 112 Sonnet 5, 1.27M words) and one sampled
Tier-2 judge run over 60 of those documents. Everything below comes from that
work: run `20260803T145220Z-d827d5a5-051c8ca2`, the judge cache behind it
(4,330 answers), and the git history of the fixes made along the way.

The instrument works. It reproduces byte-for-byte, it never lets the graded
models judge themselves, and it refuses to publish a Tier-2 number that has not
cleared a calibration gate. What the shakedown bought is the list of things that
are still wrong, and they are not small. The calibration gate cannot see the
failure that dominates Tier-2 cost. The two most expensive judge tells return a
different set of spans about a third of the time when the same question is asked
twice. Three of the ramp calibrations are set for a generation of models that no
longer exists. And a quarter of one top-ten Sonnet tell's evidence turns out to
be an artifact of the generation harness rather than anything Sonnet does.

The two models are not separated by this corpus. Sonnet indexes 12.3 [11.5,
13.1] against Opus 11.6 [10.8, 12.4], and the paired difference of 0.7 [-0.2,
1.8] spans zero. Nothing below should be read as a claim that one writes more
like a machine than the other.

---

## 1. Defects found and fixed during the shakedown

Each of these was a real failure on real work, not a hypothetical. The commit is
named so the reasoning is recoverable.

**The sleep clock stopped three generation calls (`ead587e`).** The first
generation run lost three documents to an expired OAuth token after one Opus
call sat for 4 hours 41 minutes against a 1,800-second timeout. Nothing hung.
The Mac went to sleep eight seconds into the call, and `time.monotonic()`, which
is what a subprocess timeout counts, does not advance across macOS sleep.
`run_cli` now enforces the deadline against wall clock as well, and kills the
child's process group so helpers holding the inherited pipes cannot wedge the
reap. Tests that actually shell out pin it, because no fake transport reaches
that failure.

**A DNS blip was classified as a permanent failure (`8d954da`).** The CLI reports
a dropped connection as "Unable to connect to API (ENOTFOUND)". The retryable
marker list carried the string "connection" but not "connect", and the match is
a literal substring, so the 60/300/900-second backoff never engaged and the
corpus cell was written off. The connect-level signatures are all in the list
now. Bad model names and expired credentials are still deliberately
non-retryable, pinned by tests on both sides of that line.

**Probe B failed a clean session six times running (`6a5006f`).** The isolation
battery's tool-surface probe rejected an Opus 5 session that listed Task, Bash,
Glob, Grep, Read, Edit, Write, the Skill tool and the bundled document skills.
Structured, specific, reproducible. It was still a false positive: asked to run
`echo TOOLTEST` or reply CANNOT, the session replied CANNOT in one turn with no
tool result, and the same call carried 183 input tokens against 21,129 for an
identical call with tools present. A tool-definitions block is thousands of
tokens, and there was none. The model was describing the product it knows it is
part of, from training, in answer to a question it could answer without
consulting its context. The variance gave it away: `AskUserQuestion` appeared in
only some of the six answers, and a fixed context list does not flicker. Probe B
now demands a verbatim quotation and says outright that recall does not count.
Probe B2 adds the invocation test, graded strictly. Where a property can be
measured instead of asked about, measure it.

The same reasoning had already been applied once, to probe A (`ead587e`): a
question a clean session can fail depending on how talkative the model feels is
not a usable gate, because it gates every future batch. Both failed transcripts
are kept in `runs/isolation/superseded/`, and the probe-A failure is the only
reason `KNOWN_RESIDUAL_CONTEXT` got corrected, which is the second reason to
keep them.

**Model attribution is checked on every call, and it catches things
(`1b043f6`, `transport.py:264`).** Every generation and judge call compares the
model it asked for against the `modelUsage` the CLI reports. The shakedown run
caught nine calls where the judge request for `claude-opus-4-6` came back
attributed to `claude-haiku-4-5-20251001`. All nine were
`str.parallel-bullet-grammar`, and all nine failed loudly rather than silently
contributing a haiku's opinion to an Opus judge's numbers. That is the check
working, and Section 2 covers what is still open about it.

**The sweep serialized invisibly, and the counter that would have shown it was
never wired (`cd838a8`).** `SweepController.record_call` existed,
`JudgeClient.on_call` existed, and nothing joined them, so the progress line
reported "0 calls, 0.0 calls/min" beside visibly advancing measurements for half
an hour. Concurrency itself turned out to be fine: sampling `ps` five times
during the live sweep found exactly four concurrent `claude -p` subprocesses
every time. Only the instrument was broken. The test that closes the gap is the
wall-clock one, because every existing concurrency test asserted on structure
and would have passed against a pool that silently ran everything in one thread.

**A cascade breaker stops the sweep feeding a dead network (`4d28e1d`,
`2335ee3`).** Repeated transient failures now open a breaker, and the probe that
tests whether the network is back skips the retry pause, because a probe is
already the retry.

**Extraction cost exploded on real prose, and two fixes brought it back
(`ac7b4b1`, `9e4b3b7`).** The cost estimate for Tier-2 was built on calibration
snippets, which yield 0.74 candidate spans per extraction. Real business
markdown yields 4.17. The full sweep measured out at 10,000 to 16,000 calls,
14 to 23 hours at the worker ceiling. Two changes:

- Tier-2 can be restricted to a stratified sample while Tier-1 keeps reading
  everything, which costs nine seconds. `--sample 60 --seed 7` gives 30
  documents per model, two from each of the fourteen formats, and the remaining
  two per model from the deepest pools. Stratified rather than random because
  format is the largest source of variance in how tell-prone a document is, and
  a random draw would flatter or punish a model for the mix it happened to get.
- Spans the rubric already excludes by shape are dispositioned in code. On 1,145
  cached `rht.fragment-emphasis` spans, 51% sat on a heading, a bullet, a table
  row, a sign-off or a callout, and the judge was being paid to confirm what the
  markdown parser already knew. It agreed with the line class 98% of the time.
  In the sampled run this disposed of 521 of 1,084 `rht.fragment-emphasis` spans
  and 86 `rht.rule-of-three` spans with no call at all.

Both fixes are post-extraction, so no cached judge answer was discarded, and
`PROTOCOL_VERSION` moved to 3 while `PROMPT_VERSION` stayed at 2 because nothing
the model sees changed.

**Verification could not replay a sampled judge run (`be98801`, this
milestone).** `report --verify` on the shakedown run died on a cache miss for
`claude-opus-5/case-study-07`, a document that run never judged. `verify`
rebuilt the run from the manifest without its judge sample, so the replay asked
the judge about all 224 documents instead of the 60 the run measured, and the
first unsampled document had no cached answer. The sample is an input to the
run, exactly like the corpus. It now replays from the recorded size and seed,
and the ids the sampler draws are checked against what the run wrote down, so
the sampler is under test rather than trusted.

Behind that sat a second blocker. The nine haiku-substitution failures wrote
nothing to the cache, so a cache-only replay met nine misses for work nobody
did. Those pairs now replay as the failures they were, named from the manifest's
own error list and nothing else, so an emptied cache still stops the replay
dead. `report --verify` passes on the shakedown run.

**The consistency audit spent its budget in the wrong place (`539faae`, this
milestone).** The audit drew uniformly over the cache, and the cache is deepest
for whichever tell chunks documents most finely, which is a fact about chunking
rather than about which rubric needs a stability number. The draw is now
round-robin over tells, `--max-calls` caps the live spend, and the report prints
agreement per tell.

---

## 2. Open defects and decisions

### 2.1 The calibration gate cannot see the failure that dominates Tier-2 cost

All seven judge tells calibrate at 1.00 against a gate of 0.90, on 20
hand-labelled snippets each. On the real corpus, `rht.from-x-to-y` counted one
span in 60 documents after 133 adjudication calls, and `rht.rhetorical-qa`
proposed 133 candidate spans of which 72 contained no question at all.

The gate measures the adjudicator and cannot see the extractor. Calibration
scores a snippet as correct when at least one extracted span survives
adjudication, which is the right question for the final answer and the wrong
question for cost. A snippet where stage 1 proposes eight spans and stage 2
keeps one scores exactly the same as a snippet where stage 1 proposes one. Every
extra span costs a call and no points. That is why a set of tells at 1.00
agreement produced 1,981 adjudications to count 244 spans.

Here is what the adjudicator is actually rejecting, per tell, over every
adjudication in the run rather than the ten kept per document:

| Tell | Adjudicated | Counted | Top rejection reason |
|---|---|---|---|
| `rht.rule-of-three` | 1,221 | 73 (6.0%) | exclusion (x), genuine enumeration: 1,060 (86.8%) |
| `rht.fragment-emphasis` | 500 | 131 (26.2%) | criterion (b) fails, not positioned for emphasis: 187 (37.4%) |
| `rht.rhetorical-qa` | 133 | 39 (29.3%) | no question in the span at all: 72 (54.1%) |
| `rht.from-x-to-y` | 127 | 1 (0.8%) | exclusion (x) literal range: 68, (y) literal transfer: 53 |

The rationales say why, and they are worth reading in full because they are the
first honest test of these rubrics on prose nobody wrote for them.

`rht.rule-of-three` is the semantic case. Its criterion (c) is the entire tell:
the third item has to add cadence rather than information. The extractor cannot
apply it, so it proposes every three-item coordinate structure, and business
writing is made of those. The judge then rejects them one at a time:

> "Rate structure, staffing model, or scope of operation" are three distinct
> policy levers staff recommend the Board examine; dropping any one removes a
> substantive recommendation.

> "Self-finance repair, relocate, or absorb repeated insurance deductibles" are
> three parallel verb phrases, but each names a distinct financial burden;
> dropping the third removes the specific fact about insurance deductibles.

`rht.rhetorical-qa` is not a rubric problem at all, it is extraction precision.
Over half its rejections are the adjudicator pointing out that the proposed span
is a declarative sentence:

> The span contains embedded indirect questions in declarative statements but
> poses no explicit question ending in '?', so criterion (a) is not met.

> The heading is a declarative noun clause ("What I Need…") without a question
> mark, so it does not qualify as a question under criterion (a).

`rht.from-x-to-y` fires almost entirely on literal ranges and literal transfers,
which its own exclusions then kill:

> "From container issue through laboratory analysis" names actual sequential
> process steps in sample custody transfer, triggering exclusion (y).

`rht.fragment-emphasis` is the one working as designed. Its rejections are real
discriminations about position, which is what criterion (b) asks for:

> The fragment lacks a finite verb, satisfying (a), but it follows a bolded
> heading rather than a complete sentence it would intensify or restate, so (b)
> fails.

**Options for the rule-of-three rubric.** The cap at 11 spans per chunk is
containment, not a cure. It bit on 16 of 60 documents and skipped 58 spans, all
of them recorded with `adjudication_capped`, `spans_skipped`, and the dropped
spans kept as evidence. The underlying problem is that 86.8% of what stage 1
proposes is genuinely enumerative content, and the extraction prompt does not
ask about that.

1. *Move criterion (c) into the extraction prompt.* Ask stage 1 to name the fact
   that would be lost if the third item were deleted, and to propose the span
   only when it can find none. Cheapest change, keeps the tell, and the risk is
   that recall drops silently. It would need a recall check against the current
   cached spans before it ships, which the cache makes free.
2. *Add a deterministic pre-filter.* Reject any triple whose members contain a
   number, a date, a proper noun, or a currency amount before the adjudication
   call. Cheap and auditable, and it would catch a large share of the (x)
   rejections above, but it is a heuristic layered on a semantic rubric and will
   have its own false negatives.
3. *Retire the tell.* It counted 73 spans across 60 documents, 0.26 per thousand
   words for Sonnet and 0.19 for Opus, for 1,427 of the run's 2,985 judge
   calls: 48% of the entire Tier-2 budget. On a cost-per-bit-of-signal basis it is the worst tell in the
   registry.
4. *Keep it as-is and pay.* Defensible only if rule-of-three is thought to
   separate models, and this corpus gives no reason to think so.

The same question applies to `rht.from-x-to-y` with less ambiguity: one counted
span in 60 documents, at a cost of 206 extraction calls and 127 adjudications.

**Resolved 2026-08-09 (rulings R16 and R17, HANDOFF §6).** Rule-of-three takes
option 1: criterion (c) now sits in the stage-1 prompt, which proposes a triple
only when deleting the third item would remove no distinct fact — no unique
number, date, proper noun, obligation, or policy lever — and still proposes when
the extractor genuinely cannot tell. That required more than a rubric edit: the
shared extraction rules told every extractor to over-extract and named "an
enumeration of real facts" as a judgement it must not make, so the recall-first
pair is now a per-tell slot and this is the only tell that fills it. The tell's
`rubric_version` went to 2, which strands its cached answers and nobody else's;
`PROMPT_VERSION` deliberately did not move, and the scoping is proved by test
against prompt and key hashes captured before the change. The revision ships
only after re-passing the 0.90 calibration gate and the recall check in
`scripts/rule_of_three_recall.py`, which re-asks the revised question on the 57
chunks that produced the 73 counted spans (recall gate 0.70, proposals-per-chunk
must fall by half against a cached baseline of 8.11 per chunk).

`rht.from-x-to-y` is retired: status `deprecated`, entry and calibration set kept
for history, scoring already excludes non-active tells.

### 2.2 The disagreement rate has the wrong denominator (fixed, M8g.2)

Judge/code disagreement is 0 of 292 across every tell, and that is a real
result: the model's own `instance` boolean never once contradicted the rubric
arithmetic applied to its own `criteria_met` and `exclusion_triggered` labels.
Checked directly against all 1,981 cached adjudications, not just the ten
retained per document, it is still zero. What that establishes is internal
consistency. It does not establish that the rubric is right, because code and
judge are reading the same labels.

The metric itself is miscounted. `report.judge_disagreements` divides by
`adjudicated_true`, on the reasoning that a disagreement only matters where it
changed a number. But a span where the judge said "instance" and the code said
no also changed a number, downward, and those spans land in
`adjudicated_false`, which is excluded from the denominator. The right
denominator is every adjudicated span: 1,981 here, not 292. The rate is zero
either way, so nothing published is wrong, and the metric would report 6.8x too
high the first time a disagreement appears.

Fixed in M8g.2: the denominator is now `adjudicated_true + adjudicated_false`,
and the key is renamed `counted` -> `adjudicated` in the rollup, the scorecard
row, and the CLI warning. That changes `scorecard.md`, so it invalidates
`--verify` against run `20260803T145220Z`; the run was re-rendered under the
fixed code and the new run supersedes it as the shakedown reference.

### 2.3 Haiku substitution

Nine of 175 live judge calls (5.1%) came back attributed to
`claude-haiku-4-5-20251001` when `claude-opus-4-6` was requested. Every one was
`str.parallel-bullet-grammar`, which is the largest single prompt in the judge
stack, and every one failed the measurement rather than corrupting it. Nine
documents therefore have no `str.parallel-bullet-grammar` row, which is why that
tell reports 51 documents where the others report 60.

The clustering on one tell points at a length or load trigger rather than random
substitution, but the shakedown did not test that, and one run of nine cases
cannot separate "the longest prompt gets downgraded" from "the sweep was
downgraded during a busy window". The failure is loud and the model attribution
check is what makes it loud. What is missing is a retry: a model mismatch is
currently non-retryable by design, on the reasoning that a different model
answering is a fact about the run. For substitution that is probably wrong, and
one retry would have recovered all nine.

### 2.4 JSON escaping in adjudication replies

Frequency in this run: zero. Across 175 live calls and 4,330 cached answers,
nothing failed to parse, and the manifest's nine errors are all model mismatch.

The exposure is still real and worth writing down. `parse_json_reply` tries the
whole reply, then the outermost `{...}` span, and then raises. There is no
repair path. An adjudication rationale quotes the span it is judging, spans come
from business prose, and business prose contains quotation marks and
backslashes. A reply that mis-escapes one of them fails the whole measurement
and writes nothing to the cache, which is also what makes it invisible until it
happens. The honest statement is that this is a code-reading hypothesis with no
observed instances, and it is cheap to instrument: count parse failures
separately in the manifest so the canonical run can report a real rate instead
of a guess.

### 2.5 Line numbers are not document line numbers

A match's recorded `line` counts newlines in whatever text that detector
searched. For lexical tells that is the markdown-stripped prose; for structural
tells the raw markdown; for a judge span tell the current chunk; for a judge
structural tell a synthesized skeleton. Four coordinate systems, none of them
the document.

Measured against the corpus, judge spans past the first chunk are off by the
chunk offset, with observed errors of 58, 60, 133, 166, 215 and 240 lines, and
only 106 of about 500 sampled judge matches resolve to the line they claim.
Lexical matches are off by an even number of lines, growing with position, which
is the stripped blank lines accumulating.

This is documented behaviour in `detectors/base.py`, and every rate the
benchmark publishes is unaffected, because nothing downstream uses `line`
arithmetically. What it breaks is the evidence: `scorecard.md` prints exemplars
as `claude-opus-5/email-08:27`, and for anything past the first chunk that
citation points at the wrong line. It also blocked the seam analysis until that
analysis was rewritten to locate matches by quote. A reader who cannot follow a
citation to the text cannot check the finding.

### 2.6 Throughput ceiling

Peak sustained throughput across the whole shakedown was 8.8 judge calls per
minute, measured from cache write timestamps in one-hour buckets on 2026-07-30
(517 and 527 calls in consecutive hours). Typical sustained rate was 5.0 to 5.3
per minute. Mean live call latency in the sampled run was 71.8 seconds.

Raising the worker count past five or six did not raise the rate. Four
concurrent `claude -p` subprocesses were confirmed by sampling `ps` during a live
sweep, so the pool was not the constraint. The ceiling is upstream of this
machine, and the practical planning number for the canonical run is 5 calls per
minute sustained, 8.8 at best.

### 2.7 The judge finds different spans when asked the same question twice

Asked the same extraction question a second time, the judge returns the same set
of spans 21 times out of 40. Mean span-set agreement across 40 re-asked
extractions is 0.79, where 1.0 means the two calls found exactly the same spans
and 0.5 means they agreed on two of three.

The two tells that produce most of the counted evidence are the two least
stable, and neither reproduced a single answer exactly:

| Tell | Re-asked | Mean agreement | Identical |
|---|---|---|---|
| `rht.rhetorical-qa` | 6 | 1.00 | 6 of 6 |
| `str.summary-sandwich` | 5 | 0.93 | 4 of 5 |
| `str.parallel-bullet-grammar` | 6 | 0.83 | 5 of 6 |
| `str.table-overuse` | 5 | 0.82 | 2 of 5 |
| `rht.from-x-to-y` | 6 | 0.72 | 4 of 6 |
| `rht.fragment-emphasis` | 6 | 0.63 | 0 of 6 |
| `rht.rule-of-three` | 6 | 0.62 | 0 of 6 |
| **all** | **40** | **0.79** | **21 of 40** |

The cache is what makes a judge run reproducible: every later run replays the
first answer exactly, which is why `--verify` passes. What the audit measures is
the thing the cache hides, which is how stable the first answer was. For
`rht.rule-of-three` and `rht.fragment-emphasis`, roughly a third of the spans a
run counts would have been different spans had the run happened an hour later.

Two things bound how bad that is. Agreement is measured on exact
whitespace-normalized quote strings, so a call that found the same span and
quoted one clause more of it scores as a complete miss. The worst single result
in the audit, a `str.parallel-bullet-grammar` chunk scoring 0.00 with ten spans
on each side, is exactly that: both calls found "Accelerate the Groveport
slotting reprofile", and one of them kept going to "…reprofile to". Read the 0.79
as a lower bound on how much the two calls agreed about the text.

The other bound is that this measures extraction, not the final count. A span
that only one of the two calls proposes still has to survive adjudication, and
for `rht.rule-of-three` 94% of proposals do not. Instability in a stage that
throws away 19 of every 20 candidates matters much less than the raw number
suggests, but nobody has measured how much less, and the way to do that is to
re-ask the adjudications too.

Two notes on method. The 5% draw came to 52 calls and was capped at 40 by
budget, which the report records. And the audit walks the whole cache, so 38 of
the 1,033 auditable items come from chunks cached by the earlier full sweep
rather than from the 60 sampled documents.

### 2.8 Three ramp calibrations are set for the wrong generation

`sta.mattr` scores zero for every document of both models. Its ramp runs from
0.78 to 0.86; the observed median is 0.55 for Opus and 0.55 for Sonnet, and 100%
of documents sit at or below the floor. `sta.comma-rate` has no document at its
ceiling and 96% of Opus documents at or below its floor. `str.para-uniformity`
has no document at its ceiling in either model. These three tells contribute
nothing but dilution to the index, and unlike the 49 dormant tells they are
firing, so they do not show up on the dormancy list.

---

## 3. Measurement findings

### 3.1 Both models sit above the em-dash ceiling

Em dashes per thousand words: Opus median 6.73, Sonnet median 8.44, against a
ramp that runs from 1.5 to a ceiling of 6.0. Two thirds of the documents from
each model are at or above the ceiling, and only 4% of Opus and 6% of Sonnet
documents are at or below the floor. The tell is the loudest in the scorecard
for both models, scoring 0.855 and 0.863 out of 1.

Two readings fit that equally well and the shakedown cannot separate them.
Either the ramp was calibrated on an earlier generation of models and now sits
too low to discriminate, in which case recalibrating it to something like 4 to
12 would restore its ability to tell documents apart; or heavy em-dash use is
genuinely saturated in the Claude 5 generation, in which case a ceiling that
everything exceeds is the finding and moving it would hide it.

Both can be true at once, and the resolution is a human baseline rather than an
argument. Until there is one, the honest reading is that em-dash rate no longer
discriminates between these two models, which is a different claim from saying
they use few em dashes.

The same pattern, less severely, in `pnc.semicolon-rate`: ramp ceiling 4.0,
Opus median 3.46 with 46% at or above the ceiling, Sonnet median 3.09 with 29%.

### 3.2 The legacy vocabulary tells have nearly died out

Lexical is the heaviest category in the index at 0.30, and it is the quietest
result in the run: Sonnet scores 1.4 [1.1, 1.7] out of 100 and Opus 0.9 [0.7,
1.0].

In raw terms, 80 lexical tells fired 226 times across 112 Opus documents and 255
times across 112 Sonnet documents, which is 0.32 and 0.45 hits per thousand
words. Two tells carry most of it: `lex.utilize` (107 Opus, 92 Sonnet) and
`lex.leverage` (37 and 33). Twenty-eight of the 80 lexical tells fired at all for
Opus and 25 for Sonnet. Forty-six of the 80 never fired once for either model in
1.27 million words, including all nineteen dormant single-word tells that every
"how to spot AI writing" list opens with: `delve`, `tapestry`, `myriad`,
`plethora`, `realm`, `seamless`, `synergy`, `holistic`, `meticulous`,
`intricate`, `pivotal`, `game-changer`, `cutting-edge`, `ever-evolving`,
`unlock-potential`, `navigate-complexity`, `bolster`, and the two metaphor tells
for journeys and landscapes.

The Claude 5 generation does not write like this, and an index that gives 30% of
its weight to vocabulary is spending most of its weight on a signal that no
longer exists. That is a finding about where AI writing tells now live, not a
bug, but it does argue for rebalancing before the canonical run.

### 3.3 Opener uniformity is an Opus signature

Sentence opener diversity is the one place the two models come apart clearly.
Opus's median is 0.367 against Sonnet's 0.427, and 43% of Opus documents fall at
or below the ramp ceiling of 0.35 against 11% of Sonnet's. It scores 0.816 for
Opus, second only to em dashes, and 0.586 for Sonnet.

In plain terms, Opus starts its sentences the same handful of ways more often
than Sonnet does. Sonnet compensates elsewhere: it runs higher on the
statistical category overall (23.9 against 16.7), driven by mean sentence
length, where 23% of Sonnet documents sit at or above the ceiling against 1% of
Opus documents.

### 3.4 Parallel bullet grammar separates the models, on thin evidence

Opus writes grammatically parallel bullet lists in 62% of the documents where
the tell applies (15 of 24) against Sonnet's 48% (13 of 27). It is Opus's
fourth-loudest tell.

That comparison rests on 51 documents, not 60, because nine measurements failed
on haiku substitution (Section 2.3), and the 95% intervals on the two rates
overlap: 43-79% for Opus against 31-66% for Sonnet. Treat it as a lead for the
canonical run, not a finding.

The other two structural judge tells barely move: `str.summary-sandwich` fires
in 17% of documents for both models, `str.table-overuse` in 20% of Opus and 13%
of Sonnet.

### 3.5 A quarter of one Sonnet tell's evidence is generation harness

The corpus was not stitched evenly. Sonnet needed at least one continuation on
77 of 112 documents (69%); Opus needed one on 3 of 112 (3%). Every continuation
leaves a seam where the model read its own prose and was asked to carry on,
which is exactly the situation that produces a recap or a fresh scene-setting
heading. Any tell that fires at those seams lands disproportionately on one side
of the model comparison.

`pnc.colon-subtitle-heading` does. In Sonnet's stitched documents, 70 of 290
matches (24.1%) sit within 200 characters of a seam, against 3.8% of the
positions a match that size could have occupied there. That is 6.4 times chance.
Reading the spans says why:

> …ng this report may be directed to Ms. Nwachukwu's office.* ## Appendix A:
> Supporting Program Metrics The tables below provide the unde…

> …issions coordinated by Danielle Ferraro, Chief Clerk* --- ## Appendix A:
> Second-Half Action Item Timeline | Date | Action | Responsib…

The model finished a report, the harness asked for more, and it appended
appendices with colon-subtitle headings. `pnc.colon-subtitle-heading` is Sonnet's
ninth-loudest tell in the scorecard at 0.348, and a quarter of the evidence
under it was manufactured by asking for a longer document.

Four other cells clear the flag thresholds, all of them thin or small:
`str.table-overuse` in Sonnet stitched (2 of 30 matches at a seam, 5.0x chance),
`pnc.emoji` in Sonnet stitched (7 of 69, 2.0x), `lex.leverage` in Sonnet stitched
(1 of 17, 2.4x), and `pnc.hr-density` in Opus stitched (2 of 23, 7.6x, but across
only 3 documents). None of those carries a finding on its own.

Whole-document differences between stitched and single-turn Sonnet documents are
much larger than the seam effects: bullet density 2.85 against 0.48, bold
lead-in bullets 0.505 against 0.037, emoji 0.402 against 0.000. Those are almost
certainly not the harness. The confound is format, not length: stitched and
single-turn Sonnet documents have nearly identical median word counts (4,798
against 4,889), but every memo, postmortem, performance review, research brief
and executive summary needed a continuation while every email and literature
review did not. Bullet-heavy formats are the ones that ran long. Seam proximity,
which compares positions inside a single document, does not carry that confound,
which is why it is the measure to trust.

The continuation cap has since dropped from 4 rounds to 2 (`91ee1d8`),
specifically so the word floor stops manufacturing seams out of the shortfall it
is meant to measure. The 224 shakedown documents were generated under the old
policy and were not rewritten.

### 3.6 Quote hallucination is low and concentrated

The judge invented 35 quotes out of 3,603 extracted (1.0%), every one caught by
verification against the source and discarded. By tell: `rht.rule-of-three` 25 of
1,418 (1.8%), `rht.from-x-to-y` 5 of 133 (3.8%), `rht.rhetorical-qa` 2 of 136
(1.5%), `rht.fragment-emphasis` 3 of 1,084 (0.3%), and zero for all three
structural tells. The hallucinations are paraphrases and merges of nearby text
rather than fabrications, which is what the rate being highest on the two tells
with the longest spans would predict.

---

## 4. Recommendations for the canonical run

Cost is stated in judge calls and in hours at the 5 calls per minute sustained
rate from Section 2.6. Tier-1 costs nine seconds regardless and does not appear
below.

**Baseline for comparison.** A full Tier-2 sweep over 224 documents and 7 tells
is about 11,150 calls (49.75 asks per document, measured from this run's 2,985
cache lookups over 60 documents), which is 37 hours sustained or 21 hours at
peak. A sampled sweep at 60 documents is about 3,000 calls, 10 hours sustained.

1. **Fix the judge-sample replay path before anything else. Zero calls.** Already
   done (`be98801`); it is listed because a canonical run that cannot be verified
   is not canonical. Confirm `report --verify` passes on the canonical run the
   day it finishes, not later.

2. **Retry a model mismatch once, then fail. About 10 calls.** Nine of 175 calls
   were silently downgraded to Haiku and cost nine measurements. A single retry
   would have recovered all of them for roughly 5% overhead. Keep the hard
   failure after the retry, and keep the count in the manifest so substitution
   rate stays visible.

3. **Count JSON parse failures separately in the manifest. Zero calls.** Section
   2.4 is a hypothesis with no observed instances, and one counter turns it into
   a measured rate.

4. **Decide `rht.rule-of-three` and `rht.from-x-to-y` before the run, not after.
   Saves about 6,700 calls, 22 hours.** Together they consumed 1,348
   adjudications and 412 extraction calls to count 74 spans in 60 documents:
   59% of the Tier-2 call budget for 25% of the counted evidence. The cheapest
   defensible path is option 1 from Section 2.1 for rule-of-three: move criterion
   (c) into the extraction prompt and check recall against the existing cached
   spans, which costs nothing because the cache holds the comparison. Retiring
   `rht.from-x-to-y` outright is hard to argue against at one counted span per
   60 documents.

5. **Run Tier-2 on a sample of 90, not 60 or 224. About 4,500 calls, 15 hours.**
   Sixty documents put `str.parallel-bullet-grammar` on 51 usable documents and
   left `str.summary-sandwich` with 10 counted spans. Ninety keeps the same
   stratification (45 per model, three per model-format cell) and lifts every
   Tier-2 cell above the evidence floor, at half the cost of the full corpus. If
   recommendation 4 lands first, 90 documents cost less than 60 do today.

6. **Run the consistency audit on the canonical run and publish its number in
   the scorecard. About 60 calls, 20 minutes.** A reader looking at a
   `rht.rule-of-three` rate of 0.26 per thousand words deserves to know that the
   spans behind it reproduce at 0.62. Extend the audit to re-ask adjudications as
   well as extractions, which is what turns Section 2.7 from a fact about stage 1
   into a fact about the published count. Budget another 60 calls for that.

7. **Recalibrate `sta.mattr`, `sta.comma-rate` and `str.para-uniformity`, or
   deprecate them. Zero calls.** All three are Tier-1 statistics, so recomputing
   them across the corpus under new ramps is free. `sta.mattr` currently scores
   zero for all 224 documents.

8. **Decide the em-dash ramp explicitly and record the decision. Zero calls.**
   Either recalibrate to roughly 4 to 12 and say why, or leave it and state in
   the scorecard that the tell is saturated for this generation. What should not
   happen is a canonical run whose loudest tell is pinned at the ceiling for two
   thirds of the corpus without a written reason.

9. **Rebalance the category weights, or say why 0.30 on lexical still holds.
   Zero calls.** The heaviest category produces scores under 1.5 out of 100 for
   both models, and 46 of its 80 tells never fire. Any rebalancing has to be
   decided before the run and frozen, since changing weights after seeing scores
   is how a benchmark stops meaning anything.

10. **Report the seam analysis alongside the scorecard. Zero calls.**
   `report --seams` is deterministic and takes seconds. Any tell flagged above
   2x chance should carry that flag in the scorecard rather than being reported
   as a clean model difference.

11. **Fix line numbers to be document-relative before the canonical run. Zero
    calls.** Adding the chunk offset to judge span lines and mapping lexical
    matches back through the stripped text is a small change, and it is what makes
    every exemplar in the scorecard checkable.

12. **Generate the canonical corpus under the 2-round continuation cap, and
    record the stitch rate per model in the manifest.** The 69%-against-3%
    asymmetry is the single largest known bias in the current corpus. Halving the
    continuation ladder shrinks it; recording it makes it auditable either way.

---

## 5. Discovery findings

The M8f discovery run put four lenses over the same 224-document corpus, one
pass per model, and put every proposal through the five verification gates. It
produced 23 candidates: 12 accepted and appended to the registry as
`status: candidate`, 5 rejected, and 6 parked for want of a statistic that does
not exist yet. Everything in this section comes from
`runs/discovery/shakedown-1/`.

### 5.1 The twelve appended candidates

Nine regex tells and three judge rubrics. Every regex candidate cleared a
10-of-10 precision spot-check, adjudicated by the judge against the rubric
rather than by eye. Document frequencies are Opus / Sonnet across all 224
documents. All twelve are candidates, not active tells: none of them counts
toward an index until it is promoted.

| id | lens | Opus / Sonnet doc freq |
|---|---|---|
| `pnc.em-dash-heading-separator` | formatting | 58% / 32% |
| `pnc.lowercase-preposition-in-metadata-label` | formatting | 18% / 28% |
| `phr.sentence-initial-it-is` | lexical | 84% / 45% |
| `phr.against-numeric-benchmark` | lexical | 81% / 53% |
| `phr.percent-of-proportion` | lexical | 90% / 71% |
| `phr.already-temporal-adverb` | lexical | 84% / 94% |
| `phr.within-temporal-deadline` | lexical | 87% / 71% |
| `rht.against-value-benchmark` | rhetorical | 80% / 51% |
| `rht.copular-superlative-identification` | rhetorical | 61% / 42% |
| `rht.subject-interrupting-participial-parenth` | rhetorical | deferred |
| `rht.this-content-noun-cohesive-opener` | rhetorical | deferred |
| `rht.dense-compound-predicate-sentence` | rhetorical | deferred |

The three judge candidates carry no frequencies because measuring a judge tell
costs one model call per document and the rubric has not been calibrated yet;
gates 2 and 3 are deferred to the M6 calibration set. They record
`measurement: deferred` rather than a zero (M8g.1) — the first write of these
entries put `doc_freq: 0.0` on disk, which reads as "looked for across 112
documents and never found" when the truth is that nobody looked.

### 5.2 The lens over-attributes to the model it was shown

Every lens is run against one model with the other as contrast, and it is asked
for a scope hypothesis. Of the 12 candidates that reached gate 3 and came out
with a scope, **12 of 12 had their model-specific hypothesis overturned**. Not
one survived as `model:*`. Every one landed at `general`.

Two were worse than merely over-attributed — they were pointed at the wrong
model outright:

- `within temporal deadline`, proposed as Sonnet, z = **-2.79**. Opus uses it in
  87% of documents against Sonnet's 71%.
- `address verb for resolve`, proposed as Sonnet, z = -0.98, and rejected. Opus
  87% document frequency against Sonnet's 76%.

A third, `email addresses in bold headers`, was also proposed as Sonnet with a
negative z and was rejected at the gate.

This is what a lens is for — it generates hypotheses, and gate 3 is what tests
them — but it means a lens report read on its own is systematically wrong about
scope. **Any lens output quoted anywhere must carry its gate-3 numbers.** The
model's rationale for `within temporal deadline` reads as confidently as the
rationale for `sentence-initial it is`, and one of them is backwards.

### 5.3 Commas per sentence is the largest separator, and its ramp misses it

The statistical sweep's biggest effect by a wide margin:

| stat | Opus mean | Sonnet mean | Cohen's d |
|---|---|---|---|
| `commas_per_sentence` | 0.97 | 1.46 | **1.45** |
| `sentence_length_band_distance` | 0.21 | 4.60 | 1.22 |
| `sentence_opener_diversity` | 0.42 | 0.37 | 0.72 |

A d of 1.45 on 112 documents per side is the cleanest model separation anything
in this project has produced. The registry already has a tell for it —
`sta.comma-rate`, seeded from the literature on 2026-07-28, ramp `[1.6, 3.0]`,
`high_is_telling`. **Both models' means sit below the floor of that ramp.**
Sonnet's 1.46 does not reach 1.6; Opus's 0.97 is nowhere near it. The tell that
should be the loudest discriminator in the benchmark scores approximately zero
for every document in the corpus.

This is the same failure as Section 2.8 and it belongs with it: fold
`sta.comma-rate` into that recalibration item. A ramp of roughly `[0.9, 1.8]`
would put Opus near the floor and Sonnet well up the slope, but the number
should be chosen and frozen before the canonical run, not after seeing what it
does to the scores.

### 5.4 Six statistic candidates parked for M9

Six proposals were well-formed and survived the executability gate but named
statistics `textstats.py` does not compute. They are recorded as
`needs-stat-implementation`, which is neither an acceptance nor a rejection:

- `document_total_word_count` — high total word count (Opus)
- `h3_heading_share` — h3 heading depth prevalence (Opus), and, from the Sonnet
  pass, shallow heading hierarchy off the same statistic in the other direction
- `short_opener_long_para_rate` — short claim-opener paragraphs (Opus)
- `inline_topic_label_rate` — inline topic-label paragraphs (Sonnet)
- `max_topic_label_run` — topic-label paragraph runs (Sonnet)

Two of the six are the same statistic proposed from opposite ends, which is
itself a small piece of evidence that the heading-depth difference is real.
Implementing these is M9 work: each one needs a function, a test, and a ramp
chosen against the corpus, and none of that should be rushed to make a
milestone.

### 5.5 Every scope here is provisional until Fable is in the corpus

The corpus has two models. "General" in this run means "not different between
Opus 5 and Sonnet 5" — it does not mean "characteristic of machine writing."
The distinction matters most for exactly the 12 candidates in Section 5.2, whose
scope was set to `general` by a two-way comparison that a third model could
overturn in either direction: a habit both Claudes share and Fable does not is a
Claude tell, not a general one.

So: **no candidate discovered in this run should be promoted to `active` before
the three-model corpus exists.** The gate-3 result is a falsification of the
model-specific hypothesis, which is real and worth having. It is not a
confirmation of the general one, and treating it as one would put roughly a
dozen unfalsified tells into the index at once.
