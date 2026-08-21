# Scrap Rate Escalation at Keystone Precision Forge: Attribution Analysis Across Shift, Tenure, Material, and Tooling, January 2025 – February 2026

**Prepared for:** Marcus Ellery, Chief Operating Officer
**Prepared by:** Devendra Ramaswamy, Senior Quality Engineer
**Reviewed by:** Rosalind Fairweather, Director of Continuous Improvement
**Requested by:** Yolanda Brzezinski, Plant Manager
**Date:** March 2026

---

## 1. Question and Summary of Findings

### 1.1 The question posed

In early March, Plant Manager Yolanda Brzezinski asked the quality engineering group to account for a near-doubling of the scrap rate at the Butler forging operations. Scrap, measured as the fraction of units produced that fail final gauge or magnetic particle inspection and are routed to remelt, stood at 3.1 percent of units produced in January 2025. By February 2026 it had reached 5.8 percent. Over the same thirteen months, monthly production volume moved within a band of roughly plus or minus four percent and showed no trend. The product mix shifted only modestly: the share of units in the heavy-wall hydraulic cylinder end cap family rose from 22 to 26 percent of volume, a change too small to explain the movement on its own even under pessimistic assumptions about that family's intrinsic difficulty.

The question is therefore not whether scrap rose — that is established — but what drove it. The question carries an immediate operational consequence. A $2.4 million die replacement program sits on the June capital agenda. Maintenance Director Gerald Tomczak has argued that worn die sets are the proximate cause of the scrap increase and that the capital request should be approved on those grounds and, if anything, accelerated. Competing explanations circulate on the floor: that the night shift has degraded, that the new steel vendor is supplying marginal material, and that the turnover wave of mid-2025 left too many inexperienced operators on the presses. These explanations are not mutually exclusive, and the central analytical difficulty is that they are entangled in the production record in ways that make naive comparison misleading.

This brief sets out the question, describes the records used and how they were assembled, reports what the comparisons across shift, tenure, heat lot, and die set actually show, states plainly what the gaps in the data do to the confidence of those conclusions, and draws out what all of it means for the June decision.

### 1.2 What was found

**The single largest identifiable contributor to the scrap increase is steel chemistry, specifically sulfur content at or near the upper specification limit in material supplied by Allegheny Bar and Billet.** Parts forged from Allegheny heat lots scrap at rates substantially above parts forged from the incumbent supplier's material, and this gap holds after conditioning on shift, operator tenure, die set, and press line. The effect is concentrated in a specific failure mode — subsurface tearing at the flange radius, detected at magnetic particle inspection — that is consistent with hot shortness from manganese sulfide inclusion behavior at forging temperature.

**Operator tenure is a real and separable second contributor, but it is smaller than the raw comparison implies and it interacts with material.** New operators scrap more than experienced operators everywhere, but the tenure penalty is roughly twice as large when they are running Allegheny material as when they are running incumbent material. This is the most operationally useful finding in the brief: inexperienced operators appear to be less able to compensate for marginal steel through the temperature and stroke adjustments that experienced operators make intuitively.

**The night-shift effect largely dissolves under decomposition.** Night shift scraps at 7.4 percent against 4.2 percent on days — a gap of 3.2 percentage points that is the most visible feature of the raw data and the source of most floor-level narrative. But the night shift draws 61 percent of its work from the two problem heat lots and carries 38 percent short-tenure headcount after the turnover wave. Adjusting for material assignment and tenure composition reduces the residual shift effect to roughly 0.6 to 0.9 percentage points, and even that residual is not cleanly estimated because of the badge-scan gap. Night shift is mostly a container for the other two problems, not an independent problem.

**Die condition does not carry the increase.** Die sets do vary in scrap performance, and the variation is statistically real. But the pattern of that variation does not match the pattern of the scrap increase in three specific ways: the timing is wrong, the failure-mode signature is wrong, and the dose-response against die age is weak and non-monotonic. The dies that Tomczak's program would replace first are not the dies carrying the excess scrap. This does not mean the dies are fine or that the capital request is unjustified on other grounds; it means the scrap escalation is not the evidence that justifies it.

**Two data limitations constrain these conclusions and one of them matters a great deal.** Operator badge capture is missing on approximately 14 percent of night-shift records because of a scanner failure running May through September 2025. That missingness is almost certainly not random with respect to the outcome, and it sits precisely where the tenure and shift effects need to be separated. Press line 1 was instrumented only in August 2025 and has no pre-period baseline, so line 1 contributes to level estimates but cannot contribute to trend estimates. Neither limitation overturns the material finding, which is robust across every subset examined. Both limit how precisely the tenure and shift effects can be apportioned.

**Implication for the June decision.** The scrap escalation does not constitute an evidentiary basis for the $2.4 million die replacement. The material and training interventions indicated by this analysis are substantially cheaper, can be executed within sixty to ninety days, and address the mechanisms actually visible in the data. The recommended course is to sequence those interventions first, hold the die capital request for re-evaluation in September on its own merits — throughput, dimensional capability, and maintenance labor — and require that the die business case be rebuilt without reference to the scrap trend.

---

## 2. Data and Methods

### 2.1 Source system and record structure

All production data come from the plant's manufacturing execution system (MES), which has been the system of record for forging operations since its 2021 implementation. The MES writes one record per part at press exit. Each record carries a timestamp, press line identifier, die set serial, operator badge number, shift code, steel heat lot number, part number, and a set of process values sampled at forge: billet temperature at induction exit, press tonnage peak, and stroke count for the die at time of forging. Downstream, each part record is joined to inspection outcomes from the gauge station and the magnetic particle line, which write disposition codes — accept, rework, scrap — and, for scrap, a defect classification from a controlled list of eighteen codes.

Coverage is complete for press lines 2 through 7 back to 2021. This gives roughly four and a half years of history on those six lines. Press line 1 was instrumented in August 2025 as part of a deferred capital project; before that date, line 1 production was logged only in aggregate on paper shift reports, which record total units and total scrap but not part-level attributes. Line 1 accounts for approximately 11 percent of current volume.

Heat lot identifiers link to the incoming material system, which stores mill certificates for each lot: chemistry (carbon, manganese, sulfur, phosphorus, silicon, chromium, nickel, molybdenum), mechanical properties from the mill's test coupons, and supplier identity. Operator badge numbers link to the HR system, which supplies hire date, from which tenure at the time of each part is computed.

### 2.2 Sample construction

The working sample covers January 1, 2025 through February 28, 2026 and contains 1.94 million part records. Construction proceeded as follows.

The raw extract for the period returned 2.07 million records across all seven lines. From this, 43,000 records were removed as engineering trials, first-article runs, and setup pieces, all of which are flagged in the MES and are scrapped by policy rather than by defect. A further 31,000 records were removed where the part number belonged to a discontinued family with fewer than 500 units in the period, on the grounds that these carried no comparative value and unstable rates. Approximately 56,000 records were removed where the join to inspection outcome failed, generally because the part was diverted for destructive testing or customer-witnessed inspection and never received a standard disposition code.

The largest single exclusion was press line 1's pre-August period. Because line 1 has no part-level records before August 2025, and because including it only from August forward would create a composition break at that date, the primary trend analysis uses lines 2 through 7 only. Line 1 is analyzed separately as a level comparison for the period it covers. This removes roughly 21,000 line 1 records from the trend sample while retaining them in the cross-sectional work.

Records with missing operator badge — the scanner failure discussed at length in Section 4 — were retained in all analyses that do not require operator attributes and excluded from tenure-specific analyses. They are not deleted from the file. The count and distribution of these records is itself an object of analysis.

### 2.3 Outcome definition

Scrap rate is defined throughout as scrapped units divided by units produced, where units produced is the count of parts reaching final inspection. Rework is not counted as scrap; parts that are reworked and subsequently pass are counted as accepts, and parts that are reworked and subsequently fail are counted once as scrap. This is the plant's standard convention and matches the figures Brzezinski cited in her request.

Defect classification is preserved throughout. The eighteen codes group into five families for analysis: dimensional (out of tolerance at gauge), surface (laps, seams, scale pits), subsurface (tears, internal cracks, inclusions detected at MPI), fill (underfill, misfill), and other. This grouping matters because different causal mechanisms produce different signatures, and much of the discriminating power in this analysis comes from defect-mode composition rather than from aggregate rate.

### 2.4 Analytical approach

The analysis proceeds in three layers.

**Layer one is descriptive decomposition.** For each candidate factor — shift, tenure band, heat lot supplier, die set, press line — scrap rates are computed marginally and then within cells defined by the other factors. This is the least assumption-laden approach and it does most of the work in this brief. Where a factor's marginal difference survives conditioning on the others, it is a candidate cause. Where it collapses, it was confounded.

**Layer two is regression adjustment.** A logistic model at the part level estimates scrap probability as a function of supplier, tenure band, shift, die set, press line, part family, and month, with interaction terms for supplier by tenure and supplier by shift. Continuous process values — billet temperature, tonnage, die stroke count — enter as controls. The model's purpose is not prediction but apportionment: it provides a consistent accounting of how much of the observed increase each factor absorbs. Standard errors are clustered by heat lot, since parts within a lot share material properties and are not independent.

**Layer three is sensitivity and robustness.** Every headline conclusion is re-estimated under alternative treatments of the missing-badge records, under exclusion of the highest-volume die sets, under alternative tenure cut points, and on the pre-May and post-September subsamples that bracket the scanner outage. Conclusions that move materially under these variations are reported as unstable and flagged accordingly.

A note on what this analysis is not. It is observational. Operators are not randomly assigned to shifts, material is not randomly assigned to lines, and dies are not randomly assigned to jobs. The assignment mechanisms are known in outline — scheduling practice, material staging, and die rotation rules — but they are not documented with enough precision to support a formal causal identification strategy. The strongest claims in this brief rest on the material comparison, where the confounding is least severe and the mechanism is independently corroborated by defect physics. Claims about tenure and shift are weaker and are stated with correspondingly less confidence.

---

## 3. Results

### 3.1 The trend itself

Monthly scrap on lines 2 through 7 was stable through the first four months of 2025, running between 3.0 and 3.4 percent. The series begins to move in May 2025, rises through the summer, and steps up sharply in October. February 2026 is the highest month in the series.

A figure would show this as a line chart of monthly scrap rate against time, with a flat segment through April 2025, a moderate upward slope from May through September, and a distinctly steeper segment from October forward. Overlaid on the same axes, a second line showing the monthly share of volume forged from Allegheny material tracks the scrap series closely from May onward, with Allegheny share rising from zero before April to roughly 18 percent by August and to 34 percent by January 2026. The visual correspondence is strong but not perfect: the October step in scrap is sharper than the October step in Allegheny share, which is one of the reasons the tenure interaction was investigated.

Decomposing the increase by defect family clarifies the picture considerably. Dimensional defects, which are the family most plausibly linked to die wear, rose from 1.10 percent of units in January 2025 to 1.34 percent in February 2026 — an increase of 0.24 points, or roughly 9 percent of the total 2.7-point increase. Surface defects rose from 0.71 to 0.83 percent. Fill defects were essentially flat, moving from 0.42 to 0.45 percent. Subsurface defects — tears and inclusion-related failures at MPI — rose from 0.61 percent to 2.71 percent, an increase of 2.10 points accounting for approximately 78 percent of the total escalation.

| Defect family | Jan 2025 | Feb 2026 | Change (pts) | Share of increase |
|---|---|---|---|---|
| Subsurface (tears, inclusions) | 0.61% | 2.71% | +2.10 | 78% |
| Dimensional | 1.10% | 1.34% | +0.24 | 9% |
| Surface | 0.71% | 0.83% | +0.12 | 4% |
| Fill | 0.42% | 0.45% | +0.03 | 1% |
| Other | 0.26% | 0.47% | +0.21 | 8% |
| **Total** | **3.10%** | **5.80%** | **+2.70** | **100%** |

This table is the most consequential single exhibit in the brief. Whatever is happening at Butler is overwhelmingly a subsurface tearing problem. Die wear does not produce subsurface tearing at the flange radius; it produces dimensional drift, flash irregularity, and surface defects from die surface degradation. The defect signature points away from tooling before any comparison across die sets is made.

### 3.2 Shift

The raw comparison is stark. Night shift scraps at 7.4 percent against 4.2 percent on days across the full sample period, a gap of 3.2 percentage points. This comparison is the origin of most of the informal explanation circulating in the plant, and it is the comparison most likely to be quoted in a meeting.

It is also the comparison most damaged by confounding. Two facts about the night shift are established independently of the scrap data.

First, material assignment is not balanced across shifts. The night shift draws 61 percent of its work from the two Allegheny heat lots, against roughly 19 percent on days. This is not a deliberate policy but a consequence of staging practice: bar stock is staged to the induction lines in the afternoon for the following shifts, and the Allegheny lots — which arrived in larger, less frequent deliveries than the incumbent supplier's — tended to be consumed in blocks that fell disproportionately on nights. Whatever the mechanism, the result is that comparing shifts is substantially comparing materials.

Second, tenure composition is not balanced across shifts. Short-tenure operators — under six months — constitute 38 percent of night headcount following the turnover wave of mid-2025, against approximately 16 percent on days. This reflects standard shift-bidding seniority: as experienced operators left, replacements entered on nights because that is where the openings were, and internal bidders moved from nights to days as day slots opened.

Conditioning on both factors collapses most of the gap. Within cells defined by supplier and tenure band, the night-day difference falls to a range of roughly 0.6 to 0.9 percentage points depending on how the cells are constructed and how the missing-badge records are handled. In the logistic model, the shift coefficient corresponds to an adjusted difference of approximately 0.7 points.

A residual of 0.7 points is not nothing. Plausible mechanisms include thinner supervisory and quality coverage on nights, slower response to process drift, and the known difference in induction line warm-up state at shift start. But it is roughly a fifth of the raw gap, and it does not account for the escalation over time: the night-day gap in January 2025 was 1.1 points and in February 2026 was 3.4 points, and essentially all of that widening is attributable to the growing divergence in material assignment and tenure composition rather than to any change in what happens on nights per se.

The practical conclusion is that "fix the night shift" is not a well-specified intervention. The night shift is where the plant's material and staffing problems have accumulated. Addressing those problems will move the night-shift number; addressing the night shift as such will not.

### 3.3 Tenure

Operators with under six months tenure scrap at 6.9 percent. The same tenure band on days scraps at 5.1 percent. Experienced operators — over twenty-four months — scrap at 3.4 percent on nights and 3.0 percent on days.

The tenure effect is real and it survives conditioning. Within Allegheny material, within a single shift, and within a single die set family, short-tenure operators scrap more than long-tenure operators. This is expected and unremarkable in itself; forging is a skill trade and the learning curve is well documented in the literature and in Butler's own historical records, which show a similar tenure gradient in 2022 and 2023.

What is not unremarkable is the interaction with material. Decomposing the tenure gap by supplier:

On incumbent material, short-tenure operators scrap at approximately 3.9 percent against 2.8 percent for experienced operators — a gap of about 1.1 points.

On Allegheny material, short-tenure operators scrap at approximately 9.6 percent against 6.4 percent for experienced operators — a gap of about 3.2 points.

The tenure penalty is roughly three times larger in absolute terms on the problem material, and the interaction term in the logistic model is statistically distinguishable from zero at conventional levels with heat-lot clustered errors. A figure illustrating this would show four bars grouped in two pairs — incumbent and Allegheny — with the within-pair gap visibly wider on the Allegheny side, and with the Allegheny experienced bar sitting above the incumbent short-tenure bar, which is the visually arresting detail: an experienced operator on bad steel scraps more than a new operator on good steel.

The mechanism proposed here is compensatory adjustment. Sulfur near the upper specification limit narrows the forging temperature window within which the material behaves acceptably; below a threshold, manganese sulfide inclusions become sites for tearing under the strain imposed at the flange radius. Experienced operators at Butler adjust induction dwell and, less formally, stroke rate in response to visual and acoustic cues from the first pieces of a lot. The process values in the MES corroborate this: billet temperature at induction exit shows visibly higher within-lot variance and a higher mean for experienced operators running Allegheny material, consistent with active adjustment, while short-tenure operators on the same material run closer to the nominal setpoint with less variance. New operators run the recipe as written. The recipe as written was validated on the incumbent supplier's chemistry.

If this mechanism is correct — and it is a mechanism inferred from process data and metallurgical reasoning, not established by controlled experiment — then the tenure problem is substantially a documentation and training problem rather than a raw-experience problem. The compensating adjustments experienced operators make are not in any work instruction. Writing them down and revalidating the forging recipe against actual incoming chemistry is a materially different intervention from waiting for the new cohort to accumulate months.

### 3.4 Heat lot and supplier

This is the strongest result in the analysis.

Two Allegheny Bar and Billet heat lots dominate the problem. Their mill certificates show sulfur at 0.048 and 0.051 percent against a specification maximum of 0.050 — one lot marginally over, one at the limit — where the incumbent supplier's material has historically run between 0.018 and 0.029 percent. Manganese-to-sulfur ratio, which governs inclusion morphology, is correspondingly depressed. Nothing about these certificates is out of specification in a way that would justify rejection at receiving under the current incoming inspection standard, which checks against specification limits and not against historical process capability.

Scrap rates by supplier, across the full sample:

Incumbent material: 3.2 percent.
Allegheny material: 8.7 percent.

The gap is 5.5 percentage points. It holds within every shift, every tenure band, every press line, and every die set family with sufficient volume to compare. The smallest conditional gap observed in any adequately powered cell is 3.4 points; the largest is 7.1 points. There is no subset of the data in which Allegheny material performs at parity with incumbent material.

The defect signature confirms the mechanism. Within Allegheny material, subsurface tearing accounts for 61 percent of scrap. Within incumbent material, it accounts for 19 percent. The excess is concentrated in the heavy-wall cylinder end cap family, which imposes the greatest strain at the flange radius, and within that family the scrap rate on Allegheny material reaches 12.8 percent against 3.6 percent on incumbent material.

Timing corroborates. Allegheny material entered the plant in April 2025 and first appeared in production in May. The scrap series begins moving in May. Allegheny share reached 34 percent of volume by January 2026, and the October step in the scrap series coincides with the consumption of the higher-sulfur of the two lots, which was staged into production beginning in the last week of September.

An apportionment exercise, using the logistic model to compute counterfactual scrap under the observed volume mix but with Allegheny parts assigned the incumbent-material scrap probability appropriate to their shift, tenure, die, and part family, suggests that roughly 1.7 of the 2.7-point increase — about 63 percent — is attributable to material. The tenure shift absorbs a further 0.4 to 0.6 points, part of which is the interaction and therefore not cleanly separable from material. Residual shift effects, mix change, and unexplained variation account for the remainder. These apportionments carry meaningful uncertainty and should be read as approximate magnitudes rather than precise decompositions; the sensitivity analyses in Section 4.4 move the material share within a range of roughly 55 to 70 percent.

### 3.5 Die sets

Die condition has been the leading floor explanation and it is the basis of the June capital request. The evidence does not support it as the driver of the scrap escalation.

The plant runs 34 die sets across the forging lines, with cumulative stroke counts ranging from approximately 40,000 to 780,000. Scrap rates by die set range from 2.6 to 7.9 percent, and this dispersion is real — it exceeds what sampling variation alone would produce.

Three tests were applied.

**Timing.** If die wear drove the escalation, scrap on a given die set should rise as its stroke count accumulates. Plotting scrap rate against cumulative strokes within die set, month by month, produces a relationship that is weak and non-monotonic. A figure would show a scatter of die-month points with a fitted line of shallow positive slope and very wide scatter; several of the highest-stroke die sets sit among the lowest scrap performers, and several of the newest sit among the highest. Within-die-set trajectories over the thirteen months are dominated by month-to-month swings that align with the material staged into those dies rather than with accumulated wear.

**Signature.** As established in Section 3.1, 78 percent of the increase is subsurface tearing. Die wear does not produce subsurface tearing. The dimensional and surface families, which are the die-attributable modes, together account for 13 percent of the increase — 0.36 points on a base of 1.81 points for those two families combined. That is a real and worth-tracking deterioration, but it is not the scrap problem Brzezinski asked about.

**Confounding with material.** The die sets showing the worst scrap performance are disproportionately those assigned to the heavy-wall end cap family, which is the family most exposed to Allegheny material and most sensitive to sulfur. Conditioning on supplier and part family compresses the between-die-set dispersion substantially: the adjusted range narrows from 5.3 points (2.6 to 7.9) to roughly 1.9 points. Two die sets — serials 14 and 27 — remain elevated after adjustment and warrant individual attention. Neither is among the six die sets prioritized in Tomczak's replacement schedule, which was built on stroke count.

The conclusion is not that the dies are in good condition. Several are demonstrably old, the dimensional family is deteriorating slowly, and maintenance labor on die repair has risen. Those are legitimate concerns and may well justify capital. The conclusion is narrower and firmer: the scrap escalation from 3.1 to 5.8 percent is not evidence for die replacement, and a business case that rests on it rests on a misattribution.

### 3.6 Press line 1

Line 1, instrumented from August 2025, runs at 5.1 percent scrap over the period for which part-level data exist, against 5.4 percent on lines 2 through 7 over the same months. Its defect composition is similar. Its material exposure is somewhat lower, at 24 percent Allegheny against 31 percent elsewhere, and adjusting for that raises its comparative position slightly.

What cannot be said is anything about line 1's trend. The paper shift reports for the pre-instrumentation period give monthly totals that suggest line 1 scrap ran near 3 percent in early 2025, but these reports are not reconcilable to the MES definition — they appear to count rework inconsistently, and there is no defect classification at all. They are not used in this analysis except as a weak sanity check, which they pass.

Line 1 is therefore a level observation, not a trend observation. It is consistent with the story told by the other lines and it contributes nothing that contradicts it.

---

## 4. Limitations

### 4.1 The missing badge scans

Between May and September 2025, a badge scanner on the night-shift entry to the forge bay failed intermittently. The failure was not detected promptly because the MES accepts null badge fields without error. The result is that operator identity is missing on approximately 14 percent of night-shift records across the sample period, with the missingness concentrated almost entirely in those five months. Within the May–September window itself, night-shift badge capture failed on roughly 41 percent of records.

This is the most serious limitation in the analysis and it deserves to be stated without softening.

**The missingness is not random.** Three things are known about it. First, it is confined to nights, so it differentially removes exactly the shift where the tenure question is most acute. Second, within the outage window, the failures cluster in the first two hours of the shift, which is when induction lines are coming to temperature and when scrap rates are elevated for reasons independent of who is running the press. Third — and this is the most troubling feature — the workaround when the scanner failed was for the shift lead to enter badges manually at the end of the shift for operators who requested it, and there is anecdotal evidence from the shift leads that manual entry was more consistently done for established operators than for new hires who did not know to ask. If that is true, the missing records are enriched in short-tenure operators.

**What this does to the conclusions.** The tenure gradient reported in Section 3.3 is estimated on records with badge data. If missing records are enriched in short-tenure operators and those operators scrap at higher rates, then the observed short-tenure scrap rate is estimated on a subset that under-represents the worst-performing portion of that group, and the true tenure gap may be larger than reported. Conversely, if the missingness is enriched in the high-scrap first two hours regardless of tenure, then both tenure bands lose high-scrap records and the gap is less affected.

Four sensitivity analyses were run:

*Complete-case*, the reported baseline, drops missing-badge records from tenure analyses. This is the default and it produces the figures in Section 3.3.

*Restriction to unaffected periods.* Estimating the tenure gradient only on January–April 2025 and October 2025–February 2026, where capture is near-complete, gives a short-tenure penalty of 1.3 points on incumbent material and 3.5 points on Allegheny material. Both are slightly larger than the full-sample estimates and the interaction is preserved.

*Worst-case imputation.* Assigning all missing-badge records to the short-tenure band raises the short-tenure scrap rate to 7.6 percent and widens the gap. Assigning all to the long-tenure band lowers the short-tenure rate to 6.4 percent and narrows it. The tenure effect survives both extremes in sign, though its magnitude ranges roughly from 0.7 to 2.1 points on incumbent material.

*Shift-effect sensitivity.* The residual shift effect after adjustment is the quantity most damaged. Under complete-case it is 0.7 points; under worst-case imputations it ranges from 0.2 to 1.4 points. This range spans values that would and would not motivate a night-shift intervention, and the honest statement is that the residual night-shift effect cannot be pinned down with the data available.

**What survives untouched.** The supplier comparison does not depend on operator identity at all. Every record has a heat lot. The 5.5-point supplier gap, the defect-signature evidence, and the timing correspondence are entirely unaffected by the badge outage. This is why the material finding is stated with confidence and the tenure and shift findings are hedged.

**Remediation.** The scanner was replaced in late September 2025 and capture has run above 99 percent since. No attempt should be made to reconstruct the missing five months from memory or from paper records; the shift leads' recollections are not a data source. The gap is permanent and should be documented in the MES data dictionary so that future analysts do not stumble into it.

### 4.2 Press line 1's short history

Line 1's lack of pre-August data means the trend analysis rests on six of seven lines, covering roughly 89 percent of volume. Two risks follow.

If line 1 behaved differently from the other lines before August — if, for example, it absorbed a disproportionate share of Allegheny material early, or ran a different tenure mix — then the trend estimated on lines 2 through 7 is not representative of the plant. There is no way to test this directly. Indirect evidence is mildly reassuring: line 1's post-August behavior is unremarkable relative to the others, its part mix is similar, and the paper shift reports do not show it diverging. But this is weak evidence and it should be labeled as such.

The second risk is composition break. Including line 1 from August forward in a trend series creates an artificial step at that date. The analysis avoids this by excluding line 1 from trend work entirely, which is the conservative choice but which costs statistical power in the second half of the period.

Line 1 will have twelve months of history by August 2026. Any re-analysis after that date should include it and should check whether its inclusion moves the apportionment.

### 4.3 Other limitations

**Observational assignment.** Nothing here is randomized. Material assignment to shifts, operator assignment to shifts, and die assignment to jobs all follow operational logic that correlates with outcome. The regression adjustment controls for measured confounders; it cannot control for unmeasured ones. The most plausible unmeasured confounder is job difficulty within part family — some jobs within a family are harder than others, and if harder jobs were disproportionately staged with Allegheny material or run on nights, part of the estimated effect is difficulty rather than material or shift. Process values partly proxy for this but not fully.

**Mill certificate reliance.** Sulfur content is taken from supplier certificates, not from independent verification. Butler does not currently perform incoming chemical analysis. The certificates are presumed accurate but have not been checked. Independent verification of retained samples from the two Allegheny lots is recommended and would take approximately two weeks.

**Two lots is a small sample of a supplier.** The finding is properly stated as "these two heat lots perform badly," not "Allegheny Bar and Billet is a bad supplier." Two lots cannot characterize a vendor. A third Allegheny lot received in January 2026 shows sulfur at 0.031 percent — well within historical norms — and the parts forged from it, though few, do not show elevated scrap. This is encouraging for the supplier relationship and it strengthens rather than weakens the chemistry mechanism, since it is the lots with high sulfur that scrap, not the supplier's material generally.

**Tenure cut point.** The six-month threshold is conventional at Butler but arbitrary. Alternative cut points at three and twelve months preserve the direction and the interaction with material. The twelve-month cut produces a somewhat smaller gap, suggesting most of the learning happens in the first half-year.

**No cost model.** This brief quantifies scrap in units and rates. It does not translate to dollars. Scrap cost per unit varies by part family and by where in the process the part is lost, and building that model is a separate exercise that finance should own. The capital comparison in Section 5 uses order-of-magnitude reasoning only and should not be treated as a financial analysis.

### 4.4 Stability of the headline apportionment

The claim that material accounts for roughly 63 percent of the increase was re-estimated under: exclusion of the heavy-wall end cap family, which is the most material-sensitive; exclusion of the two elevated die sets; restriction to periods of complete badge capture; alternative tenure cut points; and alternative handling of the interaction term, which can be attributed wholly to material, wholly to tenure, or split.

The resulting range for material's share is approximately 55 to 70 percent. The lower bound comes from attributing the entire supplier-tenure interaction to tenure; the upper bound from attributing it entirely to material. The direction and dominance of the material effect never reverses under any specification tried. Tenure's share ranges from 12 to 24 percent. Die sets never exceed 11 percent under any specification, and in the preferred specification account for approximately 6 percent.

---

## 5. Implications

### 5.1 For the June capital decision

The $2.4 million die replacement should not be approved on the strength of the scrap escalation, because the scrap escalation is not attributable to die condition in any specification examined. Approximately 6 percent of the increase — 0.16 points of the 2.70 — is plausibly die-related under the preferred model, and no more than 11 percent under the most die-favorable specification tried.

This is a statement about evidence, not a recommendation to reject the request. Tomczak's underlying concerns about tooling may be entirely sound. Several die sets are past their nominal design life, the dimensional defect family is deteriorating slowly, die repair labor has risen, and there may be throughput and changeover arguments that this analysis has not examined because it was not asked to. If those arguments justify $2.4 million, the request should be approved on those arguments.

The specific recommendation is procedural: **require the die business case to be rebuilt without reference to the scrap trend, and defer the decision to the September capital review.** By September, the material interventions described below will have run for roughly four months, and the plant will be able to observe scrap performance on a stabilized material baseline. If scrap remains elevated after material chemistry is controlled, that residual is the honest measure of what tooling might recover, and the die case can be evaluated against it. If scrap returns toward 3.5 percent, the die case must stand on throughput and maintenance cost alone.

A three-month deferral carries risk. If a die fails catastrophically in the interval, the deferral will look bad in retrospect. That risk should be assessed by maintenance on its own terms — a die at genuine risk of catastrophic failure is a maintenance emergency and should be replaced immediately regardless of the capital calendar, out of the existing maintenance budget. Conflating emergency tooling replacement with a strategic capital program has muddied this discussion and the two should be separated in the September submission.

### 5.2 Material actions

These are the highest-return interventions available and they are inexpensive relative to the capital request.

**Tighten the incoming specification on sulfur.** The current standard checks against a 0.050 percent maximum. Butler's process capability was established on material running 0.018 to 0.029 percent, and the recipe was validated in that range. The specification should be revised to a maximum of 0.035 percent for the heavy-wall end cap family and the other high-strain part families, with a manganese-to-sulfur ratio floor added. This is a procurement action requiring supplier notification and possibly a price adjustment.

**Institute incoming verification.** Butler currently accepts mill certificates without independent check. Spectrographic verification on a sample basis — every lot for new suppliers, every fifth lot for established ones — would cost a small fraction of the scrap it prevents. Retained samples from the two problem Allegheny lots should be tested immediately to verify the certificates.

**Segregate remaining high-sulfur inventory.** Any remaining bar stock from the two lots should be identified and either returned, or restricted to low-strain part families where the sulfur sensitivity is minimal. This is executable within days.

**Do not terminate Allegheny.** The third Allegheny lot at 0.031 percent sulfur performs normally. The problem is lot-level chemistry control, not the vendor. The appropriate response is a tightened specification and a supplier conversation, not a source change, which would carry qualification costs and schedule risk out of proportion to the problem.

### 5.3 Training and documentation actions

The supplier-tenure interaction is the finding with the most leverage per dollar.

**Capture the compensating adjustments.** Experienced operators are making temperature and stroke adjustments in response to material variation that are not documented anywhere. Process engineering should work with three or four senior operators to characterize what they do and why, and formalize it into the work instructions. This is a two-to-three week effort.

**Revalidate the forging recipe against actual incoming chemistry.** The recipe was validated on the incumbent supplier's material. Even with a tightened specification, the recipe should be checked across the allowable chemistry range rather than at a single nominal point.

**Targeted training for the short-tenure cohort.** The training should focus specifically on recognizing and responding to material variation, which is where the tenure penalty concentrates. General forging training will not close a gap that appears only on marginal steel.

**Reconsider shift assignment for the new cohort.** Thirty-eight percent short-tenure headcount on nights, on the shift that also receives 61 percent of its material from the problem lots, is a compounding assignment. Rebalancing either the material staging or the tenure mix would break the compounding. Material staging is the easier lever and should be addressed first.

### 5.4 Measurement actions

**Document the badge gap.** The May–September night-shift missingness should be recorded in the MES data dictionary with its extent and its likely non-random character, so future analyses do not treat that period as clean.

**Add automated completeness monitoring.** The scanner failed for five months without detection because the MES accepts nulls silently. A daily completeness check on badge capture, heat lot capture, and inspection join rate, with an alert threshold, would have caught this in days. This is a small IT change with disproportionate value.

**Extend line 1's history.** Nothing can recover the pre-August period, but line 1 should be included in all analyses from August 2026 forward, when it will have twelve months of comparable data.

**Establish a scrap baseline for September re-evaluation.** The September die review will need a clean comparison. Define now what "material-controlled scrap" means, how it will be measured, and over what window, so that the September discussion is not a fresh argument about definitions.

### 5.5 What would change these conclusions

Three findings would materially revise this brief.

If independent chemical verification of the retained Allegheny samples showed sulfur substantially below certificate values, the mechanism would be undermined and the analysis would need reconstruction around some other lot-level property.

If scrap failed to fall after high-sulfur material was removed from the heavy-wall families, the material attribution would be wrong or incomplete, and tooling would become a substantially more credible explanation.

If metallurgical examination of scrapped parts showed the subsurface tears originating at die-contact surfaces rather than in the bulk at the flange radius, the die argument would strengthen considerably. Ten to fifteen scrapped parts from the affected families should be sectioned and examined. This should be done before June regardless, because it is cheap and because it directly tests the central mechanism in this brief.

### 5.6 Summary of recommended sequence

Immediately: segregate remaining high-sulfur inventory; test retained samples; section and examine scrapped parts; implement MES completeness monitoring.

Within thirty days: revise incoming specification; institute incoming verification; open supplier discussion with Allegheny; begin documentation of operator compensating adjustments.

Within sixty to ninety days: complete recipe revalidation; deliver targeted training to short-tenure cohort; rebalance material staging across shifts.

June capital review: defer the die replacement decision; require rebuilt business case on throughput, dimensional capability, and maintenance cost grounds; separately authorize any emergency tooling replacement from maintenance budget.

September capital review: evaluate die request against material-controlled scrap baseline and against the rebuilt case.

---

*Analysis performed on MES extract dated March 4, 2026. Working sample 1,940,000 part records, January 2025 through February 2026. Questions to Devendra Ramaswamy, Quality Engineering.*
