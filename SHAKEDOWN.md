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

---

## 6. Fable phase generation (2026-08-09, annex closed 2026-08-20)

The third model is in. The corpus is 384 documents — 112 evidence documents per
model plus a 16-document free-writing annex per model — and this section is the
generation record plus the close-out verification that gates the 3-model sweep.

### 6.1 What Fable produced

112/112 evidence cells, **584,708 words**, mean 5,220 words per document against
a 5,000-word ask and a 4,500-word floor. **Zero below-floor documents.**

First-turn yield is the headline number: **81 of 112 documents (72.3%) came back
complete on the first turn**, 28 needed one continuation, 3 needed two. Stitch
rate 27.7%. That sits between Opus (2.7% stitched) and Sonnet (68.8%) and is the
first evidence that continuation dependence is a per-model property rather than
a property of the 5,000-word ask.

Wall-clock span 12:52:26Z to 18:21:36Z, 329 minutes for 112 documents — 2.94
min/document counted naively across the whole span. The span is two segments
either side of a 135-minute session-limit stall (§6.2), and they are not
comparable:

| segment | window (UTC) | docs | minutes | pace |
|---|---|---|---|---|
| pre-stall, serial | 12:52:26 – 15:04:06 | 39 | 131.7 | 3.38 min/doc |
| post-stall, 5 workers | 17:19:01 – 18:21:36 | 73 | 62.6 | **0.86 min/doc** |

The relaunch ran **5 workers in parallel** over disjoint format slices
(`runs/logs/fable-gen-p1.log` … `p5.log`). Just under 4× the serial pace on 5
workers, which is the expected shape once continuations serialize inside a
worker.

### 6.2 Incident: session-limit churn, twice

**2026-08-09 15:04Z.** The plan window closed at 39/112. (The dispatch note
calls this the "13:00 window", which is the Detroit-local *reset* time, not the
hit time — the same convention as the second incident's "6:10pm", quoted
verbatim from the limit message. Measured from sidecar timestamps: last
pre-stall document 15:04:06Z, first post-stall document 17:19:01Z = 13:19 EDT,
just after the 1:00pm reset. The two numbers agree.) The driver did not
stop. It walked the remaining 73 cells, took a session-limit refusal on each,
and recorded 73 per-cell failures. `runs/logs/fable-gen-20260809.log` carries
146 session-limit lines and exactly 73 `FAILED` lines, and
`generate.failure_path` writes a `<prompt_id>.failed.json` marker for each —
73 markers, zero information. Work resumed at 17:19Z after the reset and all 73 cells were
regenerated cleanly.

**2026-08-09 ~18:10Z**, during free-writing annex octet 2. Same shape, 17 cells
across the three models (`runs/logs/fable-freewriting-2.log`: `written 3,
skipped 8, failed 5` for Fable). Those cells were completed on 2026-08-20.

**Defect.** A session limit is a property of the account and the clock, not of
the cell. Treating it as a per-cell failure is wrong three ways: it burns the
remaining cells' entries in the report, it makes the failure list unreadable
(73 identical lines), and it invites a retry loop against a wall that will not
move for hours. `generate.py` already has the right shape for this in
`AUTH-LOST` — a clean stop-and-wait class that halts the driver and reports one
condition, not N failures. **Recommendation: classify session-limit responses
into that class.** The string is stable and specific (`You've hit your session
limit · resets <time>`), and the reset time is in the message, so the stop can
report when to come back.

Scope note: this is generation-side only. The judge transport's cascade breaker
already handles the analogous condition for judge calls, and the 3-model sweep
inherits it.

### 6.3 Incident: generation-side model substitution, caught

At 2026-08-09T17:24Z, under 5-way parallel load, `claude-fable-5/
literature-review-02` came back served by a different model. The sidecar
attribution check refused it:

```
FAILED claude-fable-5 literature-review-02: model mismatch: asked for
claude-fable-5, modelUsage has ['claude-haiku-4-5-20251001', 'claude-opus-5']
```

The check did its job — no mis-attributed document reached the corpus. A manual
re-run at 18:15:45Z recovered the cell with correct attribution (5,797 words, 0
continuations), and it is the one Fable evidence sidecar carrying the
`exploratory` field, because it was written after that field landed.

**Defect.** The judge transport retries once on substitution (R16). `generate.py`
does not: it fails the cell and moves on, which cost a manual re-run and would
have cost a silent hole in the corpus if nobody had read the log. **Recommendation:
mirror the judge transport's retry-once-on-substitution in `generate.py`.** Same
policy, same one-retry ceiling, same refusal to accept a substituted answer.

### 6.4 Probe-A safeguard collision

Fable's probe A began failing on 2026-08-20 with an API-level
`[reasoning_extraction]` refusal — a probe/safeguard collision, not
contamination, resolved by protocol v4 (enumeration instead of extraction).
Full incident, evidence and grader change: `runs/isolation/README.md`,
"The 2026-08-20 probe A safeguard collision".

### 6.5 Free-writing annex: n=16 per model, stopped

**Coordinator verdict: stopped at 16.** Three reasons, recorded so the stop rule
is not re-litigated:

- Meta-clusters saturated. Draws 12–16 produced no cluster the first 11 had not
  already produced.
- Conceit drift is draw-date-correlated, not sample-size-correlated. The
  2026-08-20 octet reads differently from the 2026-08-09 octets in ways that
  track the draw date. More draws on more dates would widen that confound rather
  than close it.
- "Still" appears in both Fable and Opus title space — a cross-model collision
  in a 32-document sample, which is the kind of observation that gets weaker,
  not stronger, from adding draws under a drifting conceit distribution.

The annex is exploratory and bypasses the floor and the continuation ladder
(M9b). It is excluded from every aggregate (M9c). Word totals: Fable 13,677,
Opus 20,617, Sonnet 7,861; zero continuations anywhere in the annex, by design.

### 6.6 Close-out verification (2026-08-20, offline)

Every number below was measured against the corpus on disk, no model calls.

**Completeness.** 384 documents load, 384 `.md` files on disk, 128 per model
(112 evidence + 16 annex), all 14 evidence formats at exactly 8 documents per
model. **Zero `*.failed.json` markers** anywhere under `corpus/`.

**Sidecar integrity. Zero hard anomalies across 384 documents.** Checked per
document: `model_requested` matches its directory, `model_reported` matches,
`model_mismatch` false, `prompt_sha256` recomputes from the prompt bank,
`system_prompt_sha256` uniform (one value, `7461cf6bc32d…`, equal to
`isolation.SYSTEM_PROMPT_SHA256`, across all 384), `words` recomputes through
`textstats`, `doc_sha256` matches the file bytes, `exploratory` true on all 48
annex documents and never true on an evidence document.

Two benign schema-age facts, not anomalies: 335 evidence sidecars predate the
`exploratory` field and simply omit it, and 224 Opus/Sonnet sidecars predate
`below_floor` and carry only `met_floor`. Anything reading shorts must fall back
to `met_floor is False` for those — reading `below_floor` alone reports zero
Sonnet shorts, which is wrong.

**Battery citations.** Every citation resolves to a passing transcript for the
right model, and every one is inside the 24-hour window: citation-to-document
age ranges 0.01h to 20.41h. The protocol-version mix is expected and recorded
honestly:

| model | set | battery | protocol | docs |
|---|---|---|---|---|
| claude-fable-5 | evidence | `20260809T124738Z` | v3 | 112 |
| claude-fable-5 | annex | `20260809T124738Z` | v3 | 11 |
| claude-fable-5 | annex | `20260820T151439Z` | **v4** | 5 |
| claude-opus-5 | evidence | `20260729T121729Z` | v2 | 84 |
| claude-opus-5 | evidence | `20260729T190810Z` | v2 | 26 |
| claude-opus-5 | evidence | `20260730T183650Z` | v3 | 2 |
| claude-opus-5 | annex | `20260809T182908Z` | v3 | 9 |
| claude-opus-5 | annex | `20260820T150623Z` | v3 | 7 |
| claude-sonnet-5 | evidence | `20260729T220027Z` | v2 | 111 |
| claude-sonnet-5 | evidence | `20260730T185436Z` | v3 | 1 |
| claude-sonnet-5 | annex | `20260809T183004Z` | v3 | 11 |
| claude-sonnet-5 | annex | `20260820T150704Z` | v3 | 5 |

The 2026-08-20 annex octet ran under v3 batteries for Opus and Sonnet and a v4
battery for Fable, because Fable's v3 probe A had just been refused by the
safeguard (§6.4) and v4 is what let it pass. Mixed-protocol citation within one
octet, expected, recorded. The Opus and Sonnet v2 evidence citations are older
still — the shakedown corpus was generated before v3 existed. Protocol versions
raised the standard of proof at each bump (`runs/isolation/README.md`), so an
older citation is a weaker gate, not an invalid one; this is a known property of
the shakedown corpus, not a new finding.

**Contamination. Zero hits across all 384 documents.** Scanned with
`generate.scan_contamination` over document text (not sidecars — sidecars carry
`"format": "research-brief"`, which is itself a marker and would manufacture 24
false hits). Effective marker set: 8 markers — the 6 committed ones, plus 2
resolved at scan time from `~/.claude.json` (the account email and its local
part, never printed and never written down). No `local-markers.txt` on this
machine.

**Word and continuation stats.**

| model | set | docs | words | mean | stitched | stitch % | below floor |
|---|---|---|---|---|---|---|---|
| claude-fable-5 | evidence | 112 | 584,708 | 5,220 | 31 | 27.7% | 0 |
| claude-fable-5 | annex | 16 | 13,677 | 854 | 0 | 0.0% | 0 |
| claude-opus-5 | evidence | 112 | 717,150 | 6,403 | 3 | 2.7% | 0 |
| claude-opus-5 | annex | 16 | 20,617 | 1,288 | 0 | 0.0% | 0 |
| claude-sonnet-5 | evidence | 112 | 552,530 | 4,933 | 77 | 68.8% | **9** |
| claude-sonnet-5 | annex | 16 | 7,861 | 491 | 0 | 0.0% | 0 |
| **total** | | **384** | **1,896,543** | | **111** | | **9** |

Sonnet's 9 shorts are the known ones from the old policy, retained per R7:
`executive-summary-01` (4,355), `executive-summary-04` (4,345),
`executive-summary-08` (3,867), `performance-review-01` (3,318),
`performance-review-02` (4,122), `performance-review-05` (3,708),
`performance-review-07` (3,720), `postmortem-06` (4,142), `sop-06` (4,004), all
against a 4,500-word floor. Fable and Opus have none.

**Freeze hash** over all 384 documents, same recipe as the 224-document
`d827d5a5…` (sha256 over sorted `doc_id:sha256` lines, sha256 of raw file
bytes):

```
ef89af247437136061e394aa2b707e2415011213fe01e57d77a8f22faac25c94
```

Short form `ef89af24`. Run directories for the 3-model sweep will carry it.

### 6.7 Defect noticed, out of scope

`runs/isolation/` contains `.DS_Store`. It is untracked and harmless, but the
directory is committed evidence and a stray file there is one `git add` mistake
away from the record. Worth a `.gitignore` line in the next dispatch that
touches git config.

---

## 7. Candidate re-verification against the 3-model corpus (2026-08-20, offline)

Section 5.5 said no candidate should be promoted before the third model existed.
The third model exists, so the 12 candidates went back through the gates. Run
directory `runs/discovery/fable-reverify-1/`; verdicts file committed with
`git add -f`. No model calls: gate 1 is decided by the same pattern text that is
already in the registry, and gate 4's adjudications are already paid for and
recorded per candidate. What was recomputed is gate 2, gate 3, and gate 5.

Corpus: 336 evidence documents, 112 per model. The 48 free-writing documents are
annex (R20) and were excluded — discovery and verification run on evidence
documents only.

**Nothing changed.** All nine regex candidates come back `general`, the same
verdict the two-model run gave them, and all nine still pass dedup against the
accepted registry. Opus and Sonnet document frequencies are identical to the
2026-08-04 numbers to the digit, which is the sanity check that the same 224
documents were read the same way.

| candidate | opus | fable | sonnet | z (target) | verdict |
| --- | --- | --- | --- | --- | --- |
| `pnc.em-dash-heading-separator` | 58% | 53% | 32% | opus 2.70 | general |
| `pnc.lowercase-preposition-in-metadata-label` | 18% | 21% | 28% | sonnet 1.67 | general |
| `phr.sentence-initial-it-is` | 84% | 61% | 45% | opus 5.60 | general |
| `phr.against-numeric-benchmark` | 81% | 62% | 53% | opus 4.37 | general |
| `phr.percent-of-proportion` | 90% | 77% | 71% | opus 3.44 | general |
| `phr.already-temporal-adverb` | 84% | 80% | 94% | sonnet 2.89 | general |
| `phr.within-temporal-deadline` | 87% | 77% | 71% | sonnet -2.15 | general |
| `rht.against-value-benchmark` | 80% | 60% | 51% | opus 4.49 | general |
| `rht.copular-superlative-identification` | 61% | 45% | 42% | opus 3.01 | general |

Fable sits between the other two on every one of them. That is the answer 5.5
was waiting for: these are not Claude-versus-not-Claude habits held up by a
two-way comparison, they are habits all three models have at different strengths.
Model scope fails on the 3x ratio in every case, and it fails by a wide margin —
the closest is `phr.sentence-initial-it-is` at 84% against Fable's 61%.

Two things the table does not say on its own.

The z column is the **target model's** z against the pooled rest, because that is
what `gate_scope` computes when the candidate names a target. It is not the
largest z available, and it is not a measure of anything the verdict turned on:
gate 3 rejects model scope on the ratio first, and the z never gets to matter.
`phr.within-temporal-deadline` shows this most clearly — its lens-nominated
target is Sonnet, Sonnet is the *lowest* of the three, and the z is negative.

The three judge candidates (`rht.subject-interrupting-participial-parenth`,
`rht.this-content-noun-cohesive-opener`, `rht.dense-compound-predicate-sentence`)
are **measurement-deferred, unchanged**. Measuring one costs a judge call per
document, which is a scoring run spent on an unverified proposal, so gates 2 and
3 stay deferred to M6 calibration. They were not judged here.

Registry `registry_version` 2 -> 3, hash `fb8d584a9b5d` -> `938551b40ea1`. The
change is a `provenance.evidence.reverify` block on each of the nine regex
candidates and nothing else — every `scope` and `status` field is untouched, and
a parse-level diff confirms the rest of the file is byte-equivalent in content
(the reflowed long strings are `yaml.dump` re-wrapping, not edits).

### 7.1 Defects noticed, out of scope

**The three judge candidates carry a `scope` the corpus has never tested.** Each
one is `scope: model:claude-sonnet-5` in the registry, and each one's gate-3
record says `chosen: model:claude-sonnet-5` — but that value came from the lens's
`scope_hypothesis`, not from a measurement, and the same entry's evidence block
says `measurement: deferred`. A reader who greps for scope sees a corpus-backed
model claim where there is only a hypothesis. The nine regex candidates show what
the lens is worth here: it nominated a model for all nine and was wrong all nine
times. Worth deciding, at calibration, whether a deferred candidate should carry
its hypothesis in the `scope` field at all.

**Gate 3 records only the target model's z.** When a candidate's lens-nominated
target is not the leading model, the stored `scope_z` is a number about the wrong
model, and it can be negative. Harmless to the verdict — the ratio test decides
first — but it is the kind of stored statistic that gets read later as if it
meant something.
