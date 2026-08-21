# Predicted Versus Verified Service Line Material: An Assessment of Records Reliability and Verification Coverage Ahead of the December 2026 Inventory Filing

**Prepared for:** Sun-Hee Park, Chief Engineer
**Requested by:** Alma Restrepo, Deputy Director
**Prepared by:** Reginald Boateng, Data Analyst
**Date:** July 29, 2026
**Distribution:** Engineering, Executive, Board Infrastructure Committee

---

## The Question and What Was Found

The Licking Valley Regional Water Authority holds records on 96,400 connections that classify 31,200 of them as unknown material. Those records are the basis on which the authority will file a verified lead service line inventory with the Ohio EPA by December 31, 2026, and they are the basis on which the board is being asked in August to release a $19 million tranche against $58 million in bond authority. The question put to this analysis is narrow and answerable: over the fourteen months of field verification completed to date, how well did the records predict what crews actually found in the ground, and does the pattern of where crews were sent support or undermine the inventory the authority intends to file?

The short answer is that the records are wrong in a specific, directional, and partially predictable way, and that the verification sample is not distributed in a way that permits the authority to extrapolate from it to the remaining unknown population without adjustment.

Three findings carry the weight of this brief.

First, the "unknown" classification is not a coin flip. Among the 4,850 connections verified so far that records had classified as unknown, 42 percent proved to be lead or galvanized requiring replacement. That figure is the headline, but it is also the least useful number in this report, because it is an average across populations that behave very differently. In areas platted after 1960 the rate was 19 percent. In the four oldest wards it was 68 percent. A single authority-wide rate applied to the 26,350 unverified unknowns would produce an estimate that is wrong in both directions depending on which ward one is standing in, and would misallocate replacement dollars accordingly.

Second, the records are not merely incomplete; where they are affirmative they are also unreliable. Where the permit database — the newest and nominally most trustworthy of the three sources — affirmatively recorded copper, crews still found lead 9 percent of the time. This matters more than the unknown-rate finding for the December filing, because it means the 65,200 connections currently classified as known material cannot all be carried into the inventory as verified without qualification. A nine percent error rate on affirmative records is not a rounding problem. It is a category problem.

Third, the coverage pattern raises a question the authority cannot answer from its own data as currently structured. Seventy-one percent of completed potholes fall in three of eleven wards. Refusal rates for interior inspection reached 28 percent on majority-renter blocks against a much lower rate elsewhere. Council member Hutchins's allegation — that crews were sent to wealthier streets first — is not confirmed by the operational record, which shows sequencing driven by paving schedules, main replacement coincidence, and permit-database density rather than by any income variable. But the allegation is also not refuted by the data, because the authority never recorded a sequencing rationale at the work-order level, and the wards that received concentrated attention do differ from the wards that did not on housing tenure and median value. The honest position is that the verification program produced a sample whose geography was determined by operational convenience, that operational convenience correlated with neighborhood characteristics, and that the authority lacks the documentation to demonstrate that this correlation was incidental. That is a weaker claim than the allegation and a stronger admission than the authority has yet made.

The implications for the December filing and the August tranche are set out at the end of this brief. In summary: the filing is achievable but will require the authority to file a substantial number of connections as unknown rather than as verified, and to defend a stratified statistical basis for its remaining estimates; and the August tranche should be released, but the allocation formula attached to it should be revised to reflect ward-level predicted rates rather than the authority-wide average, and a portion should be ring-fenced for verification in the eight under-sampled wards before further replacement work is sequenced.

---

## Data and Methods

### The three record sources

The authority's material classifications derive from three sources of different vintage, different construction, and different failure modes. They overlap inconsistently, and no field in the current asset management system records which source generated a given classification. Reconstructing source attribution was the first substantial task of this analysis and consumed roughly a third of the effort.

**The 1978 tap card file.** The oldest source is a physical card file created in 1978, apparently as a consolidation of earlier records whose originals no longer exist. Each card corresponds to a tap and carries handwritten entries for date, size, material, and installer. The file was scanned in 2009 in a project that produced page images without optical character recognition; a subsequent keying effort transferred what could be read into the asset system. Six percent of cards are illegible in the scans — water damage, fading, and in some cases scanning error where a card was folded or overlapped. Illegibility is not randomly distributed. It is concentrated in the sections of the file corresponding to the oldest service areas, which is to say precisely the areas where lead is most likely.

Two further problems attach to this source. The cards record the material of the tap and the utility-side connection, and in many cases say nothing about the customer-side line. Where a card records "copper," it may be describing a copper gooseneck on a lead line, a distinction the 1978 consolidation did not consistently preserve. Second, the cards were not updated after 1978 in any systematic way; where a service was replaced in 1985, the card may or may not reflect it. The tap card file should therefore be understood as a snapshot of belief in 1978 about installations that predate 1978, degraded by scanning loss and unmaintained since.

**The permit database.** The permit database begins in 1994 and is the authority's only structured, queryable source. It records service line permits issued, including material specified, contractor, and inspection sign-off. Its coverage is good for the period it covers and its data quality is high in the narrow sense that fields are populated and internally consistent.

Its limitations are two. First, it begins in 1994, which means it says nothing about the roughly two-thirds of the system installed before that date except where a post-1994 replacement occurred. Second, and more consequentially for this analysis, it records what was permitted rather than what was installed. The 9 percent lead-found-where-copper-recorded rate is largely a permit-versus-installation gap: permits specifying copper for full replacement where the contractor replaced only the utility side, or where the customer-side portion was left in place by agreement or by omission and never re-permitted. Inspection sign-off does not close this gap, because inspections in the 1994–2006 period were commonly performed at the curb stop.

**Meter replacement notes.** The third source is a body of free-text notes entered by meter technicians during replacement rounds, keyed by hand from paper worksheets. These notes are the only source that reflects direct observation of the customer side of the connection at the meter, and are therefore in principle the most probative. In practice they are the least usable. The notes are unstructured; material observations appear in various phrasings ("lead," "Pb," "galv," "old line," "looks like lead," "not copper"); many worksheets record no material observation at all; and the keying introduced transcription errors that are impossible to distinguish from technician ambiguity. For this analysis I parsed 41,000 note records against a keyword dictionary and manually reviewed a stratified sample of 400 to estimate parsing accuracy, which came out at 87 percent for affirmative lead identifications and materially lower — around 71 percent — for affirmative non-lead identifications, because technicians were more likely to note an anomaly than to note normality.

### How the classifications combine

Where sources disagree, the asset system resolved conflicts by recency, taking the most recent source as authoritative. This rule was never documented as policy and appears to have emerged from the sequence in which data was loaded. Its effect is that a 2011 meter note saying "copper at meter" overrides a 1978 tap card saying "lead," even though the meter note describes only the visible pipe at the meter and the tap card describes the tap. In 1,340 cases in the verification sample, the sources disagreed. I have treated these as a separate analytic category and report them below, because they behave differently from cases where sources agree or where only one source exists.

The 31,200 unknown classifications arise from four distinct situations, which the current system does not distinguish:

| Origin of "unknown" classification | Estimated count | Share |
|---|---|---|
| No record in any source | 11,900 | 38% |
| Tap card illegible or missing | 6,850 | 22% |
| Record exists but material field blank or non-committal | 8,300 | 27% |
| Sources conflict, unresolved | 4,150 | 13% |
| **Total** | **31,200** | **100%** |

These counts are estimates derived from source attribution reconstruction and carry uncertainty of roughly ±400 in each category. The distinction matters because these four groups verified at different rates, as shown in the results.

### The verification sample

Between May 2025 and July 2026, crews potholed and verified 4,850 connections that records classified as unknown. Verification protocol required visual confirmation of material at the curb stop and, where access permitted, at the interior entry point. Where interior access was refused or unavailable, crews recorded utility-side material only and flagged the customer side as unverified. For this analysis, a connection is counted as "verified" only where both sides were observed or where the utility side was observed and the customer side was confirmed by a documented post-1994 full replacement permit. Applying that standard, 4,850 of 5,910 potholes conducted meet the verification bar; the remaining 1,060 are partial and are excluded from rate calculations but discussed under limitations.

Method for comparison was straightforward: for each verified connection, I recorded the records-based prediction (including source, and including the four unknown-origin categories above), the field finding, and a set of covariates — ward, plat date of the subdivision, year of structure construction from county auditor data, housing tenure from the 2020 decennial and 2023 ACS block group estimates, and whether the connection fell within a scheduled paving or main replacement corridor during the verification period. Rates are reported with binomial confidence intervals; ward-level rates in the smaller wards carry wide intervals and are flagged where the interval exceeds ±8 percentage points.

Two methodological cautions apply throughout. The verification sample is not a probability sample of the unknown population; it is the set of connections crews happened to reach. Every rate reported below is therefore a rate within the sample, and extrapolation to the unverified population requires the stratification adjustments described in the results and limitations sections. Second, plat date and structure age are correlated but not identical, and I use structure age where available (91 percent of records) and plat date otherwise.

---

## Results

### Overall verification outcome

Of 4,850 verified connections classified as unknown, 2,037 — 42.0 percent — proved to be lead or galvanized requiring replacement. The 95 percent confidence interval on that proportion, treating the sample as if it were random, is 40.6 to 43.4 percent. That interval is misleadingly tight, because the sample is not random; the true uncertainty about the corresponding population rate is dominated by selection, not by sampling error, and is addressed below.

Within the 2,037 requiring replacement, the split was 1,190 lead (58 percent of replacements, 24.5 percent of all verified) and 847 galvanized-downstream-of-lead or galvanized requiring replacement (42 percent of replacements, 17.5 percent of all verified). The remaining 2,813 verified connections were copper (2,566), plastic or other non-lead (198), or no service line present at an active-billed address (49) — the last a small but operationally interesting category representing billing records that survived demolition.

### Variation by housing age and plat date

The authority-wide 42 percent figure conceals the strongest and most actionable pattern in the data. Verification rates by plat era:

| Plat era | Verified connections | Requiring replacement | Rate |
|---|---|---|---|
| Pre-1920 | 892 | 641 | 71.9% |
| 1920–1945 | 1,104 | 762 | 69.0% |
| 1946–1960 | 1,338 | 431 | 32.2% |
| After 1960 | 1,516 | 203 | 13.4% |
| **All** | **4,850** | **2,037** | **42.0%** |

The post-1960 figure of 13.4 percent in this table differs from the 19 percent figure cited in the framing of this request; the difference is definitional. The 19 percent figure is the rate for *areas platted* after 1960, which includes infill and replacement structures on older plats and includes a number of connections in the 1960–1972 window where lead goosenecks remained in use. Restricting to structures built after 1960 on plats recorded after 1960 gives the 13.4 percent above. Both figures are correct within their definitions; I recommend the authority standardize on the plat-based definition for external reporting, since plat date is documented in county records and structure date depends on auditor data of variable quality, and I use the 19 percent plat-based figure in the implications section for consistency with prior board communications.

The gradient is steep and it is monotonic. The odds of finding lead or galvanized in a pre-1920 plat are roughly sixteen times the odds in a post-1960 plat. This is not surprising as a matter of plumbing history — Ohio permitted lead service lines until 1975 and their use declined through the 1950s — but the magnitude of the gradient is larger than the authority's current planning assumptions, which apply a uniform rate.

### Variation by ward

Ward-level rates range from 68 percent in the four oldest wards, taken together, to a low of 11 percent in Ward 9. Individual ward rates:

| Ward | Verified | Requiring replacement | Rate | 95% CI half-width |
|---|---|---|---|---|
| 1 | 810 | 561 | 69.3% | ±3.2 |
| 2 | 744 | 512 | 68.8% | ±3.3 |
| 3 | 601 | 401 | 66.7% | ±3.8 |
| 4 | 488 | 334 | 68.4% | ±4.1 |
| 5 | 402 | 149 | 37.1% | ±4.7 |
| 6 | 366 | 124 | 33.9% | ±4.9 |
| 7 | 288 | 79 | 27.4% | ±5.2 |
| 8 | 231 | 48 | 20.8% | ±5.2 |
| 9 | 194 | 21 | 10.8% | ±4.4 |
| 10 | 421 | 82 | 19.5% | ±3.8 |
| 11 | 305 | 46 | 15.1% | ±4.0 |
| **Total** | **4,850** | **2,037** | **42.0%** | ±1.4 |

Wards 1 through 4 are the four oldest wards referenced in the framing; their combined rate is 68.4 percent. Their combined verified count is 2,643, which is 54.5 percent of all verification work, and they contain an estimated 9,100 of the 31,200 unknowns, or 29 percent. The verification program has therefore been substantially concentrated in the highest-yield wards, which is defensible as replacement strategy and problematic as inventory strategy — a tension developed below.

*Figure 1 (described).* A scatter plot of ward-level verified lead-or-galvanized rate against median plat year of the ward's unknown-classified connections would show a tight negative relationship, with wards 1–4 clustered in the upper left (plat years 1890–1935, rates 66–70 percent), wards 5–7 in the middle (plat years 1948–1958, rates 27–37 percent), and wards 8–11 in the lower right (plat years 1963–1981, rates 11–21 percent). The relationship is close to linear over this range with an R² of approximately 0.91. Ward 10 sits slightly above the fitted line, reflecting a pocket of pre-1940 housing in its northeast quadrant annexed in 1969; Ward 5 sits slightly below it. The practical import of the figure is that ward is largely a proxy for age, and that age is the variable doing the causal work. A model using plat era alone predicts ward-level rates nearly as well as a model using ward identity, which is reassuring for extrapolation because plat era is known for every connection in the system, verified or not.

### Reliability of affirmative records

The most consequential result for the December filing concerns connections the records do *not* call unknown.

During the verification period, crews encountered 2,180 connections carrying affirmative material classifications, either incidentally during main work or through targeted spot-checking authorized in October 2025. Of the 1,455 that the permit database affirmatively recorded as copper, crews found lead or galvanized in 131 cases — 9.0 percent, with a confidence interval of 7.6 to 10.6 percent.

Disaggregating by permit era clarifies the mechanism:

| Permit era | Checked | Found lead/galv | Rate |
|---|---|---|---|
| 1994–2000 | 402 | 61 | 15.2% |
| 2001–2006 | 511 | 49 | 9.6% |
| 2007–2014 | 338 | 17 | 5.0% |
| 2015–present | 204 | 4 | 2.0% |
| **All** | **1,455** | **131** | **9.0%** |

The declining rate tracks the tightening of inspection practice: curb-stop-only inspection was standard through roughly 2006, and interior verification became routine after the 2014 procedural revision. The residual 2 percent in the most recent era likely reflects partial replacements at the customer's election, documented in the permit remarks field in 3 of the 4 cases.

Tap card affirmative records performed worse, as expected. Of 725 connections where the tap card recorded a non-lead material and no later source contradicted it, crews found lead or galvanized in 148 — 20.4 percent. The gooseneck ambiguity described above accounts for the majority of these; in 94 of the 148, the utility side was copper and the customer side was lead, exactly the configuration a 1978 tap card would have recorded as copper.

Meter note affirmative records, where they were the sole basis of classification, produced a 16.1 percent error rate on a base of 349 checks. Given the parsing accuracy problems described in methods, this figure should be treated as indicative rather than precise.

### Records that conflict

The 1,340 verification-sample cases where sources disagreed verified at 51.3 percent lead or galvanized — meaningfully above the 42.0 percent overall rate and above the rate for cases with no record at all. Where the conflict was specifically between a tap card indicating lead and a later source indicating otherwise, the rate was 63.8 percent on a base of 486. The recency resolution rule embedded in the asset system is, in other words, resolving conflicts in the wrong direction. An older record indicating lead is more informative than a newer record indicating copper, because the newer record is usually a partial observation and the older record is usually a whole-connection observation.

This is a correctable defect. Reclassifying the 4,150 unresolved-conflict unknowns and re-examining the affirmative classifications that a recency rule produced from a lead-indicating tap card would, on these rates, move an estimated 1,900 to 2,400 connections from probable-copper to probable-lead in the planning inventory. Those connections are currently not budgeted for replacement.

### Verification outcome by origin of the unknown classification

| Origin | Verified | Requiring replacement | Rate |
|---|---|---|---|
| No record in any source | 1,982 | 743 | 37.5% |
| Tap card illegible or missing | 1,104 | 619 | 56.1% |
| Record blank or non-committal | 1,153 | 366 | 31.7% |
| Sources conflict, unresolved | 611 | 309 | 50.6% |

Illegible tap cards are the highest-yield category, which follows directly from their concentration in the oldest sections of the file. This finding has an immediate operational use: of the 6,850 unknowns arising from illegible or missing cards, roughly 4,100 sit in wards 1–4, and they should be prioritized in the next verification round both because their expected yield is high and because they are the category for which no amount of records research will produce an answer.

### Coverage and refusals

Seventy-one percent of completed potholes fall in wards 1, 2, and 4. Coverage of the unknown population by ward, expressed as the share of each ward's unknowns that have been verified:

| Ward | Est. unknowns | Verified | Coverage |
|---|---|---|---|
| 1 | 2,850 | 810 | 28.4% |
| 2 | 2,410 | 744 | 30.9% |
| 3 | 1,980 | 601 | 30.4% |
| 4 | 1,860 | 488 | 26.2% |
| 5 | 3,120 | 402 | 12.9% |
| 6 | 2,740 | 366 | 13.4% |
| 7 | 2,590 | 288 | 11.1% |
| 8 | 3,010 | 231 | 7.7% |
| 9 | 3,340 | 194 | 5.8% |
| 10 | 3,890 | 421 | 10.8% |
| 11 | 3,410 | 305 | 8.9% |
| **Total** | **31,200** | **4,850** | **15.5%** |

Coverage in the four oldest wards runs between 26 and 31 percent; coverage in wards 8, 9, and 11 runs between 6 and 9 percent. The disparity is roughly four to one.

The operational record offers explanations that are individually reasonable. Wards 1–4 contained 62 percent of the main replacement footage scheduled during the verification window, and potholing alongside open-cut main work costs approximately $340 per connection against $1,150 for standalone potholing — a genuine efficiency that any engineer would pursue. The 2025 paving program concentrated in wards 1, 2, and 5. And the permit database's density is lowest in the oldest wards, meaning those wards had the highest concentration of unknowns per block and thus the lowest mobilization cost per verification.

What the operational record does not contain is any work-order field recording why a given block was sequenced when it was. I reviewed 240 work orders from the verification period; none carried a documented sequencing rationale beyond crew and date. The authority therefore cannot demonstrate, from its own records, that the sequencing followed the efficiency logic rather than some other logic. It can show that the outcome is consistent with the efficiency logic. That is not the same thing, and it is not what a hostile reader will accept.

On the specific allegation: I tested the association between ward-level verification coverage and two neighborhood measures. Coverage correlates negatively with median household income at the ward level (r = −0.58), which is to say the *lower*-income wards received *more* verification, the opposite direction from the allegation. Coverage correlates positively with median structure age (r = 0.86), which is the expected efficiency pattern. Within wards 1–4, however, block-group-level coverage correlates positively with median owner-occupied home value (r = 0.41 across 88 block groups), meaning that within the oldest wards, higher-value blocks were reached earlier. This within-ward pattern is weaker than the between-ward pattern and is substantially explained by main replacement corridors, which follow arterial streets where housing values are higher, but it is real and it should be reported rather than buried.

The refusal pattern is the more serious equity finding. Interior inspection refusals averaged 11.4 percent authority-wide but reached 28 percent on majority-renter blocks. Refusals were 8.1 percent on blocks with owner-occupancy above 70 percent. The mechanism is not mysterious: interior access requires a resident to admit a crew, and on rental property the person with the legal interest in the pipe is frequently not the person answering the door. Crews reported that in 214 documented instances the occupant stated they would need landlord permission; in 61 of those, follow-up contact with the owner of record was attempted and succeeded in 19.

The consequence is that partial verifications — utility side only — are concentrated on renter-occupied blocks. Of the 1,060 partial potholes excluded from the rate calculations, 604 (57 percent) fall on majority-renter blocks, which contain 31 percent of the unknown population. Because customer-side lead is the dominant configuration in this system — recall that 94 of 148 tap-card errors were copper utility side, lead customer side — excluding partials biases the reported rates downward in exactly the neighborhoods where the authority has the least information and where the affected population has the least capacity to compel action. If the 604 renter-block partials verified at the same customer-side rate as comparable-age fully verified connections, they would add an estimated 240 to 290 replacement-requiring connections to the count.

---

## Limitations

**The sample is not random and cannot be treated as random.** Every extrapolation in this brief rests on the assumption that within a plat era and ward, verified connections resemble unverified ones. That assumption is testable only weakly. Within wards 1–4, where coverage approaches 30 percent, I compared verified and unverified unknowns on structure age, lot size, and distance to main, and found no material differences, which supports the assumption there. In wards 8, 9, and 11, where coverage is under 10 percent, the comparison is uninformative because the verified set is dominated by main-corridor work and differs from the ward's unknown population on distance to main by a substantial margin. Extrapolated estimates for the low-coverage wards should carry uncertainty bands two to three times wider than the binomial intervals reported above. I have not attempted to quantify that inflation formally; doing so would require a modeled selection mechanism the authority's data cannot support.

**Partial verifications are excluded, and their exclusion biases downward.** As described above, 1,060 potholes yielded utility-side observation only. Their exclusion removes disproportionately renter-occupied, customer-side-lead-likely connections from the denominator and the numerator alike, with net downward bias on the reported rates. A sensitivity analysis imputing customer-side material for partials at within-stratum rates raises the overall 42.0 percent to an estimated 44.1 percent, and raises the wards 1–4 combined rate from 68.4 to 70.2 percent. I report the unimputed figures as primary because the imputation rests on an untested assumption, but the direction of the bias is not in doubt.

**Source attribution is reconstructed, not recorded.** The four-way decomposition of unknown origins, and the source-specific error rates, depend on my reconstruction of which source generated which classification. That reconstruction used load timestamps, field-population patterns, and format signatures, and I validated it against 300 manually traced records with 93 percent agreement. Seven percent misattribution propagates into the source-specific error rates; it does not materially affect the overall rate or the ward and era breakdowns, which do not depend on attribution.

**Meter note parsing is imperfect.** The 87 percent and 71 percent parsing accuracies described in methods mean that any result resting primarily on meter notes — chiefly the 16.1 percent meter-note error rate — should be read as approximate.

**Structure age data is incomplete.** County auditor construction dates are missing or implausible for 9 percent of records. I substituted plat era in those cases, which is coarser and which may attenuate the age gradient slightly.

**The spot-check sample of affirmative records was not designed as a probability sample.** The 2,180 affirmative-record checks arose partly incidentally and partly from targeted selection after October 2025. Targeted selection favored records suspected to be unreliable, which biases the 9 percent copper-error rate *upward*. Restricting to the 1,004 incidental checks only yields 7.4 percent, which is probably closer to the population rate. I use 9.0 percent in the headline because it is the figure already in circulation, but the implications section uses a range of 7 to 9 percent.

**Fourteen months is not a stable operating period.** Crew composition, protocol, and equipment changed over the verification window; the vacuum excavation unit acquired in January 2026 changed both throughput and, plausibly, the completeness of observation. I found no statistically detectable change in found-rate before and after that acquisition within matched strata, but the test had limited power.

**No cost data is integrated here.** This brief addresses prediction accuracy and coverage, not replacement cost, and the tranche implications below are stated in terms of connection counts and allocation logic rather than dollars per connection.

---

## Implications

### For the December 31, 2026 filing

The consent order requires a verified inventory. The authority will not have physically verified 31,200 connections by December 31; at current throughput of roughly 350 verifications per month, it will add perhaps 1,750 more, reaching approximately 6,600 verified of 31,200 unknowns, or 21 percent coverage. The filing must therefore rest substantially on records-based classification and statistical inference, and the defensibility of the filing depends on the defensibility of that inference.

Three consequences follow.

First, **the authority should not file a single authority-wide unknown rate.** Applying 42 percent uniformly to the 24,600 still-unknown connections would produce an estimate of about 10,300 requiring replacement. Applying stratum-specific rates — 68 to 72 percent in the pre-1945 strata, 32 percent in 1946–1960, 19 percent post-1960 — to the actual composition of the remaining unknown population produces an estimate of approximately 8,900, with the difference arising because the remaining unknowns skew newer than the verified ones. The stratified estimate is both lower and more defensible, and the stratification uses plat era, which is documented for every connection in county records and is therefore auditable by the state. I recommend the filing present stratified estimates with explicit strata definitions and stratum-level confidence intervals.

Second, **the affirmatively-classified population cannot be filed as verified without qualification.** At a 7 to 9 percent error rate on permit-database copper classifications and a 20 percent error rate on tap-card non-lead classifications, the 65,200 connections currently carried as known material contain somewhere between 3,900 and 5,600 misclassified lead or galvanized connections. Filing these as verified non-lead would be inaccurate on its face and would expose the authority to a compliance finding when subsequent work discovers them. The defensible course is to reclassify affirmative records by source and era into confidence tiers — permit-database records post-2015 as high confidence, permit-database records 1994–2006 and all tap-card-only records as requiring verification — and to file the lower tiers as unknown. This will increase the filed unknown count from 31,200 to roughly 40,000 to 42,000, which is uncomfortable but accurate, and it is far preferable to filing a number the authority knows to be wrong by four to five thousand.

Third, **the recency conflict-resolution rule should be reversed before the filing is generated.** As shown, tap cards indicating lead that were overridden by later partial observations verify at 63.8 percent. The asset system should be amended so that any lead indication in any source, at any date, controls unless a documented full-replacement permit exists. This is a configuration change, not a data collection effort, and it can be completed well before December. It will move an estimated 1,900 to 2,400 connections into the replacement-required category — connections that are currently invisible to both the inventory and the budget.

Fourth, and as a matter of filing integrity rather than arithmetic, **the filing should disclose the coverage disparity.** The authority will be filing an inventory in which four wards are 28 percent verified and three are under 9 percent. That fact will be evident to any reader who examines the supporting data, and it is better disclosed with the operational explanation attached than discovered later. The disclosure should state the coverage figures by ward, state the efficiency rationale, and state plainly that the rationale is inferred from operational patterns rather than documented at the work-order level.

### For the August tranche

The $19 million tranche should be released. The verification results confirm that a large replacement population exists and that delay carries public health cost. But the allocation formula attached to the tranche requires three revisions.

**Revise the allocation basis from the authority-wide rate to stratum-specific rates.** If the tranche is allocated on an assumption of 42 percent lead prevalence across all wards, it will over-fund replacement in wards 8 through 11, where the true rate is near 19 percent, and under-fund wards 1 through 4, where it is near 68 percent. The board should be shown the stratum table and asked to allocate against it.

**Ring-fence a verification component for the under-covered wards.** I recommend approximately $2.4 million of the tranche — roughly 12 percent — be dedicated to standalone verification in wards 7 through 11, targeting a minimum coverage floor of 15 percent in every ward before the following tranche. At $1,150 per standalone pothole this funds approximately 2,090 verifications, sufficient to bring the seven under-covered wards to a 13 to 16 percent floor. The purpose is not primarily to find lead — the yield in those wards is low — but to establish that the inventory rests on a sample that touches every part of the service area, which is both an equity requirement and an audit requirement.

**Fund a renter-access protocol.** The 28 percent refusal rate on majority-renter blocks is the single clearest equity failure in the program, and it is not self-correcting; it will persist and it will concentrate unverified customer-side lead in rental housing. I recommend a modest allocation — on the order of $300,000 — for landlord notification in advance of crew arrival, evening and weekend appointment availability, and a documented escalation path to owners of record. The 19 successful follow-ups out of 61 attempts suggests that direct owner contact works when it is attempted; it has been attempted in fewer than a third of cases.

### On the Hutchins allegation

The board will want a position. The defensible position is this: between wards, verification was concentrated in older, lower-income wards, which is the opposite of the allegation. Within the four oldest wards, higher-value blocks were reached somewhat earlier, largely because main replacement corridors follow arterial streets. The authority did not document sequencing rationale and therefore cannot prove intent either way. The refusal pattern, which is a separate and larger equity problem, has produced systematically worse information for renter-occupied housing and requires remedy regardless of how the sequencing question is resolved.

Recommending that work-order records begin capturing a sequencing rationale field, effective immediately, would cost almost nothing and would make this question answerable the next time it is asked.
