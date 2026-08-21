# Scrap Rate Increase at Keystone Precision Forge: A Decomposition of Shift, Tenure, Heat Lot, and Die Effects

**Prepared by:** Devendra Ramaswamy, Senior Quality Engineer
**Reviewed by:** Rosalind Fairweather, Director of Continuous Improvement
**Prepared for:** Marcus Ellery, Chief Operating Officer; Yolanda Brzezinski, Plant Manager
**Date:** July 30, 2026

---

## The Question and What We Found

Plant-wide scrap climbed from 3.1 percent of units produced in January 2025 to 5.8 percent in February 2026, a near-doubling over thirteen months during which output volume did not change. Yolanda Brzezinski asked quality engineering to explain the increase before the June capital agenda, which includes a $2.4 million die replacement that maintenance director Gerald Tomczak has advocated on the grounds that worn dies are driving the scrap rate up.

We built a working sample of 1.94 million forged parts from the plant's manufacturing execution system (MES), covering January 2025 through February 2026 on press lines 2 through 7, with partial data from line 1 beginning in August 2025. Every part record carries a press identifier, die set, shift, steel heat lot, and — where the scanner was functioning — an operator badge.

Four patterns stand out. Night-shift scrap runs 7.4 percent against 4.2 percent on days. Operators with under six months of tenure scrap at 6.9 percent on nights versus 5.1 percent on days for the same tenure band. Sixty-one percent of night-shift volume is drawn from two heat lots supplied by a new vendor, Allegheny Bar and Billet, whose mill certificates show sulfur at the top of the accepted specification band. And when we hold heat lot and operator tenure constant, the residual difference attributable to shift alone falls from 3.2 percentage points to roughly 0.8 to 1.3 points, depending on the subgroup.

In other words, the aggregate "night shift is worse" finding is largely, though not entirely, a composite of two other things: more first-year operators working nights, and a disproportionate share of a specific, higher-sulfur steel supply routed to the night shift by scheduling practice rather than by design. Die sets do not show a plant-wide degradation pattern that would explain a swing of this magnitude. One die set on line 4, in continuous service since 2021 with a high cycle count, does show an elevated scrap rate that persists after controlling for shift, lot, and tenure — a genuine signal, but a narrow one that does not account for the bulk of the increase and does not, on its own, justify a plant-wide $2.4 million capital program.

Two data problems limit how far these conclusions can be pushed. Roughly 14 percent of night-shift records lack an operator badge because a scanner failed from May to September 2025, which is also when the Allegheny lots entered production and when the new-hire wave was largest — so the gap in badge data overlaps in time with the two effects we most need to measure cleanly. And line 1 has only seven months of instrumented history, which is not enough to assess long-run die wear trends on that line or to include it in a year-over-year comparison starting from January 2025.

Our reading is that the evidence assembled so far does not support attributing the scrap increase primarily to die condition, and it does not support approving the $2.4 million die replacement as currently scoped on the basis of the aggregate trend. It does support two narrower and cheaper actions before June: tightening incoming sulfur acceptance on Allegheny material or requiring a supplier corrective action, and rebalancing new-hire assignment and heat-lot routing away from the night shift while the workforce transition settles. If, after those changes, a scrap gap persists that tracks specific die sets and cycle counts rather than shift, lot, or tenure, that would be the basis for a capital case — and it should be scoped to the dies actually implicated rather than approved as a general remedy.

---

## Data and Methods

### Source system and coverage

Keystone's MES records every forged part at the point of press-cycle completion, tagging it with a press line number, a die set identifier, a shift code, a steel heat lot number traceable to a mill certificate, a timestamp, and, in principle, the badge number of the operator running the press at that cycle. Scrap is logged when a part fails in-process or final inspection and is coded to a disposition (dimensional nonconformance, crack, forging lap, material defect, or other), though disposition coding is not the focus of this brief and is noted only where it bears on the heat-lot and die findings below.

Coverage differs materially across the seven press lines. Lines 2 through 7 have been fully instrumented since 2021, giving five years of continuous part-level history. Line 1 was not wired into the MES until August 2025; everything before that date on line 1 exists only in paper travelers and end-of-shift production counts, which are not part-level and cannot be reconciled to badge, die, or heat lot. For the period this brief covers, line 1 contributes seven months of instrumented data out of the thirteen-month window (January 2025 to February 2026), and none of it can be compared to a January 2025 baseline on that line, because no such baseline exists in machine-readable form.

Badge capture is complete on day shift throughout the window. On night shift, a barcode scanner at two of the four night-shift press stations failed in early May 2025 and was not repaired until late September 2025. During that interval, the MES logged press, die, shift, heat lot, and part disposition normally, but the operator badge field was populated by a shift-default placeholder rather than an individual badge number for an estimated 14 percent of night-shift records plant-wide (a higher share at the two affected stations, partially offset by the two working stations). This gap does not affect the shift, heat lot, or die comparisons directly, since those fields were captured independently of badge status, but it does affect our ability to compute operator-tenure scrap rates precisely for the affected months, a point we return to in Limitations.

### Sample construction

The working sample is 1.94 million parts, produced across lines 2 through 7 for the full window and line 1 from August 2025 forward, spanning January 2025 through February 2026. We excluded parts with missing die-set identifiers (a small share, under 0.5 percent, concentrated in early line 1 records during commissioning) and parts flagged as engineering trial runs, which are run outside normal production control and are not comparable to standard-run scrap.

We defined scrap rate as scrap units divided by units produced (scrap plus accepted units) within a given cell — shift, tenure band, heat lot, die set, or combination thereof — rather than scrap units divided by all units including rework, to match the definition Brzezinski's group has used historically and to keep this analysis comparable to the 3.1 percent and 5.8 percent figures already in circulation.

Operator tenure was computed from badge-linked hire date at the time of each part record, bucketed at the six-month mark because that is the threshold Yolanda Brzezinski's team flagged informally and because it aligns with the plant's probationary training period. Records without a valid badge (the 14 percent gap on nights during the scanner outage, plus a smaller residual gap outside that window from occasional scan misses) were excluded from tenure-specific cells but retained in shift-level and heat-lot-level cells, since those fields did not depend on badge capture.

Heat lots were linked to mill certificates supplied by Keystone's incoming materials group. Each certificate reports chemical composition, including sulfur content, against the plant's accepted specification band for the relevant alloy grade. We flagged any heat lot with certified sulfur at or above 95 percent of the upper specification limit as "high-sulfur" for this analysis; two Allegheny Bar and Billet lots, which together account for 61 percent of night-shift material volume in the period they were active, met that threshold. We refer to them as the Allegheny lots throughout; legacy material from the plant's two longstanding suppliers is referred to as legacy lots.

### Analytical approach

We first replicated the plant's standard monthly scrap-rate series to confirm the January 2025 (3.1 percent) and February 2026 (5.8 percent) figures against the MES, which matched within rounding. We then built cross-tabulations of scrap rate by shift, by tenure band, by heat lot source, and by die set, followed by combined cells crossing shift with heat lot and shift with tenure, to see how much of the raw shift gap survives once lot and tenure are held fixed. Finally, we examined die-set-level scrap rates controlling for shift, lot, and tenure mix, looking for die sets whose scrap rate remains elevated after those adjustments — the pattern Tomczak's argument predicts if die wear is driving the increase.

We did not build a full multivariate regression model for this brief; the cross-tabulations, read together, are sufficient to establish the qualitative decomposition the capital decision needs, and we were conscious of the risk of overstating precision given the data limitations described below. A fuller model, with press-line and month fixed effects, is a reasonable next step if the June decision is deferred, and we say more about that in Implications.

---

## Results

### Shift and tenure

The raw comparison that has driven concern in the plant is stark: 7.4 percent scrap on nights against 4.2 percent on days, a gap of 3.2 percentage points. Tenure shows a related but smaller pattern: operators under six months scrap at 6.9 percent versus 5.1 percent for the same tenure band on days, and — separately — tenure itself matters within each shift, since operators past six months scrap at meaningfully lower rates than new hires on both shifts.

The night shift has drawn a disproportionate share of the plant's recent hiring. Following a turnover wave that began in late 2024, new hires under six months now make up 38 percent of night headcount, against a lower share on days that Brzezinski's team has separately reported at roughly 19 percent. Night shift is therefore not just scrapping at a higher rate; it is also running with a workforce mix that is, on its own, associated with higher scrap regardless of shift.

### Heat lot chemistry

The two Allegheny heat lots carry certified sulfur at the top of the plant's specification band for the relevant forging grade — high enough to be within tolerance but close enough to the ceiling that elevated sulfur is plausible as a contributor to hot-shortness defects and cracking in hydraulic component forgings, a failure mode consistent with the disposition codes we see disproportionately represented in scrap from those lots. Sixty-one percent of night-shift volume in the months those lots were active came from this material, against a much smaller share on day shift, where scheduling has historically routed newer or less-proven heat lots to the shift with more senior operators and closer supervisory coverage — a practice that, in this instance, worked against clean attribution rather than for it, because it concentrated the highest-risk material on the shift that already had the least experienced crew.

### Die sets

We do not find a plant-wide pattern of rising scrap concentrated in older or higher-cycle-count die sets. Scrap rates across the great majority of die sets on lines 2 through 7 move roughly in line with the shift, lot, and tenure factors described above rather than independently of them; a die set running mostly day-shift, legacy-lot, tenured-operator parts shows a scrap rate close to the plant's day/legacy/tenured baseline regardless of its age or cycle count, and a die set running mostly night-shift, Allegheny-lot, new-hire parts shows an elevated rate regardless of whether it is old or comparatively new.

One exception is worth flagging. Die set D-118, on line 4, has been in continuous service since 2021 and carries the highest cumulative cycle count of any die set in the plant. Its scrap rate remains elevated — in the neighborhood of 6.5 percent against a plant-wide die-set average near 4.0 percent — even after we restrict the comparison to legacy-lot parts run by tenured operators on day shift, which strips out the three confounders discussed above. This is a genuine, narrow signal consistent with wear on that specific tool, and it is the kind of evidence that would support a die replacement decision — but it implicates one die set on one press line, not the plant-wide program Tomczak has put on the capital agenda, and it explains a small fraction of the roughly 2.7-percentage-point plant-wide increase.

### Putting the pieces together

The table below summarizes scrap rate by shift, heat lot source, and tenure band for lines 2 through 7 across the full window, restricted to cells with adequate volume for a stable estimate. Cells combining day shift, Allegheny lot, and new-hire operators are thin, because Allegheny material was disproportionately scheduled onto nights; we report that cell for completeness but flag it as imprecise.

| Shift | Heat Lot Source | Tenure Band | Scrap Rate |
|---|---|---|---|
| Day | Legacy | ≥ 6 months | 3.6% |
| Day | Legacy | < 6 months | 4.8% |
| Day | Allegheny | ≥ 6 months | 5.3% |
| Day | Allegheny | < 6 months | 6.2%* |
| Night | Legacy | ≥ 6 months | 4.4% |
| Night | Legacy | < 6 months | 5.6% |
| Night | Allegheny | ≥ 6 months | 7.1% |
| Night | Allegheny | < 6 months | 8.3% |

*Low-volume cell; treat as indicative only.

Three things follow from this table. First, moving from legacy to Allegheny material adds roughly 1.5 to 1.7 percentage points of scrap within a given shift and tenure band, holding those factors fixed — a heat lot effect that appears whether the operator is on days or nights, new or tenured. Second, moving from tenured to new-hire status adds roughly 1.0 to 1.5 points within a given shift and lot combination — a tenure effect that likewise appears on both shifts and with both material sources. Third, once lot and tenure are held constant, the residual shift effect — night versus day within the same lot and tenure cell — runs from about 0.8 points (legacy, tenured: 4.4 versus 3.6) to about 1.3 points (Allegheny, tenured: 7.1 versus 5.3), a good deal smaller than the 3.2-point raw gap between the two shifts.

That residual is not zero, and we do not want to overstate the case that shift itself is irrelevant; something about night operation — supervisory ratios, lighting, fatigue, or press-specific handoff practices we have not examined here — appears to carry a modest independent penalty even after lot and tenure are accounted for. But the bulk of the raw shift gap, on this evidence, is composed of the fact that the night shift disproportionately combines the riskier steel with the least experienced crew, not a shift effect in itself, and not — on the die-set evidence above — a tooling effect.

### Timing

The monthly trend is consistent with this reading. Scrap held in a narrow band around 3.1 to 3.4 percent from January through April 2025. It began climbing in May 2025, the same month the badge scanner failed and roughly the same period the first Allegheny heat lot entered production, reaching approximately 4.5 percent by September 2025. It continued rising through the fall and winter as the new-hire share of night headcount grew and a second Allegheny lot entered production around the turn of the year, reaching 5.8 percent by February 2026. We do not have a die-replacement or die-refurbishment event in the maintenance log during this window that would line up with the timing of the increase; the die sets in service in February 2026 are, with the exception of D-118's ongoing wear, largely the same population that was in service in January 2025, when scrap was 2.7 points lower.

---

## Limitations

### Missing night-shift badge data

The 14 percent of night-shift records without a valid badge between May and September 2025 is the single largest threat to the tenure findings in this brief. Two directions of bias are possible, and we cannot fully rule out either from the data available. If the scanner failure disproportionately affected stations where the newest hires were placed — plausible, since new hires are typically assigned to the stations needing closer supervision, which may also be the stations where a scanner failure was allowed to persist longer before being flagged — then our tenure-band scrap rates for that period understate the true gap, because a portion of the highest-scrap, least-tenured population is missing from the tenure cells entirely and effectively absorbed into shift and lot averages instead. If, conversely, the failure was concentrated at stations run by more senior operators who were less likely to report equipment problems promptly, the bias could run the other way. We lean toward the first explanation based on informal input from shift supervisors, but we have not verified it against maintenance work orders for the affected scanners, and we recommend that verification be completed before the tenure-effect estimate in this brief is treated as final.

Because the gap overlaps almost exactly with both the scanner outage and the period the first Allegheny lot was ramping up, it also limits our ability to fully separate the heat-lot effect from the tenure effect during those five months specifically; we can state the two effects clearly in the months before and after the outage, where badge data is complete, but the middle of the window — which is also when the increase accelerated most sharply — is the period we can decompose least precisely.

### Line 1's short history

Line 1 contributes only seven months of part-level data, all from August 2025 forward, and none of it can be tied to a January 2025 baseline. This has two consequences for the conclusions above. First, the plant-wide scrap figures Brzezinski's office has been tracking, including the 3.1 percent January 2025 figure, could not have included line 1 on a like-for-like basis, since no instrumented line 1 data exists that far back; if line 1's scrap rate has historically run higher or lower than lines 2 through 7, some portion of the reported plant-wide increase could reflect a change in what is being measured rather than a change in the underlying process. We do not believe this is a large effect, because line 1 is one of seven lines and its volume share is modest, but we have not quantified it, and it should be checked before the February 2026 figure is treated as fully comparable to January 2025.

Second, and more directly relevant to the capital decision, seven months is not enough time to assess whether line 1's dies are wearing in a way that would support or undercut Tomczak's argument. Die wear is typically a slow, cycle-count-driven process, and a die set with a genuine wear problem may not show a clearly rising scrap trend within seven months if it started that period already partway through its wear curve, or may show a trend that looks alarming but is within normal variation for a young instrumentation record. We can report line 1's current scrap rate, which sits close to the plant average, but we cannot report a trend on that line with any confidence, and any capital request that includes line 1 dies should be treated as resting on the same weak evidentiary footing as the plant-wide die argument, not a stronger one.

### Other constraints

A handful of additional caveats bear on how much weight this brief's numbers can carry. The Allegheny/day-shift/new-hire cell in the table above is built on comparatively few parts, because scheduling routed most Allegheny material to nights; the 6.2 percent figure in that cell should be read as directional rather than precise, and a wider confidence interval applies to it than to the other seven cells. Mill certificates report composition at the point the heat lot was poured and certified, not composition as-delivered at each press station; we have no reason to doubt the certificates, but we also have not independently verified sulfur content at the press, and cross-contamination or certificate-to-delivery mismatches, while unlikely, cannot be entirely excluded. Finally, the under-six-month tenure cohort may carry a survivorship pattern worth flagging: operators who scrap heavily and struggle in their first months may be more likely to leave before reaching the six-month mark, which would tend to understate rather than overstate the true new-hire effect, since our under-six-month cell only captures those still employed at the time of each part record, not the full population who ever worked in that band.

None of these limitations, individually or together, seem to us large enough to overturn the qualitative pattern in this brief — that heat lot and tenure explain most of the raw shift gap, and that die sets other than D-118 do not show an independent wear signal. But they are large enough that we would caution against treating the specific percentage-point estimates in the table as final figures for a capital budgeting exercise without the follow-up work described below.

---

## Implications for the June Capital Decision

The evidence in this brief does not support Gerald Tomczak's argument that die condition is the primary driver of the scrap increase, and it does not support approving the $2.4 million die replacement, as currently scoped, on the basis of the plant-wide scrap trend. The trend is real, but on the data available it is composed mainly of two things that have nothing to do with die wear: a disproportionate share of high-sulfur Allegheny material routed to the night shift, and a disproportionate share of first-year operators also concentrated on that shift following the 2024–2025 turnover wave. Both effects are visible independently, both are visible in combination, and together they account for most of the residual once the raw shift gap is decomposed. Die sets do not show a matching plant-wide pattern; the one clear exception, D-118 on line 4, is a narrow, single-tool finding that would justify a targeted replacement of that die, not a plant-wide capital program.

We recommend three things happen before the June capital meeting, in order of urgency.

First, address the heat lot. We recommend the materials group either negotiate a tighter sulfur ceiling with Allegheny Bar and Billet below the top of the current specification band, or require a supplier corrective action and hold the current lots in quarantine pending resolution, given the plausible link between sulfur content and the cracking-related dispositions we see disproportionately in scrap from those lots. This is a materials and procurement decision, not a capital one, and it can be actioned well ahead of June.

Second, rebalance workforce and material scheduling. Routing 61 percent of night-shift volume through two high-sulfur lots while also running the shift with 38 percent new-hire headcount stacked two risk factors on top of each other in a way that made the plant's overall scrap number harder to read and, we suspect, harder for supervisors to manage in practice. Spreading Allegheny material more evenly across shifts, or holding it off the night shift until it clears the corrective action above, and continuing to pair new hires with tenured operators on the highest-risk material, should both reduce scrap in the near term and make any subsequent die-wear signal easier to see clearly.

Third, fix the measurement gaps before the next review. The badge scanner issue is already resolved going forward, but we recommend a documented process to flag and escalate any future scanner outage within days rather than months, given how much it has cost this analysis in precision during exactly the period we most needed to see clearly. On line 1, we recommend continuing full instrumentation and treating any die-wear assessment on that line as provisional until at least twelve to eighteen months of data are available, enough to span a meaningful share of a normal die service interval.

If, after the heat lot and workforce actions above have had a few months to take effect, a scrap gap persists that tracks specific die sets and cycle counts rather than shift, lot, or tenure — the pattern D-118 already shows in miniature — that would be solid grounds for a capital request, and we would support bringing it back to the agenda at that point. We would also support a narrower, lower-cost version of Tomczak's request now: replacing or refurbishing D-118 specifically, which the evidence does support, rather than the plant-wide program currently listed. That single-die action could proceed in June on its own merits without waiting on the broader decomposition work, and doing so would also serve as a useful natural experiment: if D-118's replacement closes its scrap gap while the rest of the plant's rate continues to track heat lot and tenure as this brief describes, that will considerably strengthen confidence in the diagnosis above.

We would rather see the June capital decision deferred on the plant-wide die question than see $2.4 million committed against a cause the current data do not clearly implicate, particularly when two lower-cost interventions — supplier sulfur enforcement and workforce-material rebalancing — target factors the data implicate much more directly, and can be tested within a single quarter at a fraction of the cost.

We would also flag a practical sequencing risk in deferring the full program: if the June capital agenda is the plant's normal cycle for approving spending of this size, waiting for a full quarter of post-intervention data could push a genuine die-related capital need into the following cycle, adding months of delay if D-118, or some other die set we have not yet identified, does turn out to need replacement beyond what a single-tool repair addresses. We think that risk is manageable and smaller than the risk of committing $2.4 million against the wrong cause, but Ellery and Brzezinski should weigh it against the plant's capital calendar rather than have it decided implicitly by this brief.

### Proposed verification plan and timeline

We propose the following sequence, designed to produce a clean answer in time for the plant's next scheduled capital review rather than waiting a full year.

By the end of August 2026, procurement should have resolved the Allegheny sulfur question, either through a tightened certificate specification, a corrective action commitment, or a supplier substitution for the two lots in question. Quality engineering will pull certificates on any replacement or corrected material and confirm it falls comfortably inside the specification band before it is released to the floor. This step is inexpensive and can proceed immediately; it does not need to wait on anything else in this plan.

By the end of September 2026, scheduling should have rebalanced heat lot assignment across shifts so that no single shift is absorbing a disproportionate share of any one lot, and workforce assignment should pair new hires more consistently with tenured operators on both shifts rather than concentrating new hires on nights. We recognize this may run against seniority-based shift bidding practices already in place, and we are not in a position to resolve that tension in this brief; we flag it as a decision for Brzezinski and plant HR rather than a quality engineering recommendation on its own.

From October through December 2026, we propose running the cross-tabulation in this brief again on a rolling basis, monthly, watching specifically for two things: whether the shift gap and the tenure gap narrow as the material and scheduling changes take hold, and whether any die set other than D-118 begins to show an independent, persistent elevation once lot and tenure effects are stripped out. We would also use this window to complete the badge-scanner verification described in Limitations, confirming whether the May–September 2025 gap biased the tenure estimates in the direction we suspect, and to extend line 1's instrumented history far enough to include it in a proper year-over-year comparison for the first time.

By the plant's Q4 2026 capital review, we expect to have a clean, three-way-controlled estimate of the residual die effect, including whether D-118 alone accounts for the plant's tooling-related scrap or whether other die sets have emerged as concerns once the confounding factors above are addressed. That review would be the appropriate point to bring back a capital request scoped to whatever the data show at that time, rather than the plant-wide $2.4 million figure currently on the June agenda.

### D-118: interim recommendation

Because the evidence for D-118 already holds up after controlling for shift, lot, and tenure, we see no reason to make its replacement or refurbishment contingent on the broader verification plan above. Maintenance should proceed with a standard tooling assessment of D-118 — dimensional inspection against original specification, cycle-count review against the die's rated service life, and a cost comparison between refurbishment and full replacement — and bring a single-die capital request to the June agenda in place of the plant-wide program. We estimate, based on the plant's historical tooling costs for comparable die sets on line 4, that this request would fall well under $400,000, though maintenance should confirm that figure rather than rely on our estimate, since we have not priced tooling work as part of this analysis.

### A note on the D-118 finding and its limits

We want to be careful not to overstate what the D-118 result shows. A single die set with an elevated, confounder-adjusted scrap rate is consistent with wear, but it is also consistent with other explanations we have not ruled out: a die-specific setup or alignment issue unrelated to cumulative cycle count, a press-specific factor on line 4 that happens to correlate with which die runs there, or a disposition-coding pattern specific to whatever part geometry D-118 produces, which could inflate its apparent scrap rate relative to die sets producing more forgiving geometries. The dimensional inspection maintenance conducts as part of the interim recommendation above should resolve this ambiguity directly, by checking whether D-118's cavity dimensions have in fact drifted outside tolerance, which is a more direct test of the wear hypothesis than a scrap-rate comparison can ever be on its own.

---

## Summary Table of Findings and Recommended Actions

| Finding | Confidence | Recommended Action | Timing |
|---|---|---|---|
| Raw night/day scrap gap (7.4% vs 4.2%) is largely explained by heat lot and tenure, not shift or dies | Moderate–high | No action on shift structure itself; address underlying lot and tenure factors below | — |
| Allegheny lots add ~1.5–1.7 points of scrap independent of shift and tenure | Moderate | Tighten sulfur spec or require supplier corrective action; quarantine current lots pending resolution | By end of August 2026 |
| New-hire tenure adds ~1.0–1.5 points of scrap independent of shift and lot | Moderate | Rebalance new-hire assignment and pairing with tenured operators across shifts | By end of September 2026 |
| Plant-wide die sets show no independent wear signal once lot and tenure are controlled | Moderate, limited by line 1 history | Do not approve plant-wide $2.4M die replacement in June | June 2026 agenda |
| D-118 (line 4) shows a persistent, confounder-adjusted elevated scrap rate | Moderate–high, pending dimensional inspection | Proceed with targeted tooling assessment and single-die capital request | June 2026 agenda |
| 14% of night-shift badge records missing May–September 2025 | Confirmed gap; bias direction uncertain | Verify scanner outage timeline against affected stations; document escalation procedure | By end of Q3 2026 |
| Line 1 has only 7 months of instrumented history | Confirmed limitation | Continue full instrumentation; exclude line 1 from year-over-year die trend claims until 12–18 months of data accrue | Ongoing |

---

## Distribution

This brief is provided to Marcus Ellery, Yolanda Brzezinski, and Rosalind Fairweather ahead of the June capital review, with a copy to Gerald Tomczak given the direct bearing on his die replacement proposal. We are glad to walk through the underlying cross-tabulations, including the low-volume cells flagged above, with any of the four before the agenda is finalized, and we would welcome maintenance's dimensional inspection data on D-118 as soon as it is available, since it bears directly on the one part of this analysis where we believe a capital case is already reasonably well supported.
