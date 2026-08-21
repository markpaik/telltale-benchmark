# Did Hourly Pay Reduce Regional Driver Turnover?

## An Evaluation of the March 2025 Compensation Conversion at Sycamore Ridge Transport, with Implications for the Over-the-Road Fleet

**Prepared by:** Marisol Cabrera-Nunez, Workforce Analytics Lead
**Commissioned by:** Fatima Bensalem, Vice President of Driver Recruiting
**Route and operations context:** Gene Prokop, Terminal Manager, Fort Wayne
**Prepared for:** Terrence Whitlock, Chief Financial Officer, and the Board Compensation Committee

---

## The Question and What We Found

In March 2025, Sycamore Ridge Transport moved its regional driver fleet off mileage-based compensation and onto an hourly rate of $28.50 with guaranteed detention pay. The change costs approximately $3.4 million a year in incremental payroll and payroll-linked expense. The board is now weighing whether to extend the same structure to the 310-driver over-the-road (OTR) fleet at an additional annual cost of $6.2 million. The chief financial officer has asked a narrow and reasonable question: did the March 2025 conversion actually reduce regional driver turnover, and by how much?

The headline number is favorable. Annualized regional turnover fell from 51 percent in the twelve months preceding the conversion to 33 percent in the twelve months following it, measured across 742 regional drivers. That is an 18-percentage-point improvement, or a decline of roughly 35 percent in relative terms.

The headline number is also not, by itself, an answer. Three things make it insufficient as a basis for a $6.2 million decision.

First, the conversion was not the only thing that changed. A $2,500 driver referral bonus went live in February 2025, one month before the pay conversion, and applied to the same regional population. Referral bonuses are known to affect both who joins and how long they stay, and the two programs are close enough in time that no simple before-and-after comparison can separate them.

Second, the external labor market moved. Regional freight volumes fell approximately 9 percent industry-wide during the post-period, which mechanically reduces the number of competing job openings a regional driver can walk into. Turnover falls in soft freight markets regardless of what any individual carrier does with pay. This is the single largest threat to a causal reading of the 18-point improvement.

Third, the OTR fleet — which received neither the pay conversion nor the referral bonus — also improved, from 68 percent to 57 percent over the identical window. That 11-point improvement is a rough measure of how much of the regional gain would likely have happened anyway. Subtracting it from the regional 18-point gain leaves approximately 7 percentage points as the portion plausibly attributable to the regional-specific interventions — the pay conversion and the referral bonus together.

Seven points, not eighteen. And those seven points are shared between two programs, one of which (the referral bonus) costs a fraction of what the pay conversion costs.

The terminal-level pattern complicates the picture further and, in our view, is the most informative finding in this analysis. The improvement was not distributed evenly. Fort Wayne fell from 46 to 24 percent and Louisville from 58 to 30 percent — both large. Columbus moved from 44 to 41 percent, essentially flat. Evansville barely moved at all. Every one of these terminals received the same $28.50 hourly rate, the same detention guarantee, and the same referral bonus on the same dates. A uniform treatment producing radically non-uniform results means the treatment is interacting with something local — route structure, detention exposure, local labor market, or terminal management — and that the mechanism, not the pay rate alone, is what generated the gain.

This matters directly for the OTR question. If the pay conversion worked primarily by compensating drivers for unpaid detention time, then its value depends on how much detention a fleet actually experiences. OTR operations have a different detention profile than regional LTL work. Extending the structure on the assumption that it will reproduce the regional result would be extending it on an assumption the regional data does not support.

Our recommendation is not to approve or reject the OTR extension. It is that the board defer the decision pending three specific pieces of evidence, described in the implications section, that can be assembled within roughly one quarter and that would materially change the confidence attached to a $6.2 million commitment. We also recommend that the board treat the tenure finding — that drivers with less than one year of service account for 71 percent of all separations — as a parallel and possibly larger lever than the pay structure itself.

---

## Data and Methods

### Sources

This analysis draws on four internal systems and one external reference.

**Payroll records** provided compensation history for all regional and OTR drivers, including the mileage-rate history prior to March 2025, the hourly rate thereafter, detention pay disbursements, referral bonus payments, and the effective dates of each driver's transition. Payroll is our most reliable source. It is transactional, it is audited, and it carries exact dates.

**Human resources separation records** provided the population of separations, separation dates, separation type (voluntary, involuntary, retirement, medical), and the coded reason where one was recorded. Separation reason coding is where this dataset weakens considerably, and we address that below.

**Driver master records** provided hire dates, terminal assignment, terminal transfer history, license class, and endorsement status. These allow us to compute tenure at separation and to construct the terminal-level views.

**Telematics records** provided detention events — arrival and departure timestamps at shipper and consignee facilities, with dwell time computed against appointment windows. This is the dataset that would let us test the detention mechanism directly. Its coverage begins only in April 2024, which is the central limitation of this analysis and is discussed at length below.

**External reference:** published industry freight volume indices for regional LTL tonnage, used to characterize the demand environment during the study window.

### Population and Window

The regional analysis population is 742 drivers who held a regional assignment at any point during the 24-month observation window spanning March 2024 through March 2026. The pre-period runs the twelve months to the end of February 2025. The post-period runs the twelve months from March 2025 forward. Drivers are attributed to the period in which their separation occurred; drivers active in both periods contribute exposure to both.

The comparison population is the 310-driver OTR fleet, observed over the identical window. The OTR fleet received neither the hourly conversion nor the referral bonus, which makes it the only internal group that can serve as a rough control.

### Turnover Definition

Turnover is calculated on an annualized basis as separations divided by average headcount over the period. We include voluntary separations, involuntary separations, and terminations for cause. We exclude retirements and separations coded as medical or disability-related, on the grounds that these are unlikely to respond to compensation structure. This is a standard construction and matches how the figure is reported in the monthly operations package, which means the numbers in this brief should reconcile to what the board has already seen.

One methodological note that matters for interpretation: annualized turnover rates above 50 percent are dominated by short-tenure churn. When a fleet turns over at 51 percent, it is not the case that half the drivers left; it is the case that a comparatively small number of positions cycled repeatedly. The tenure finding below makes this concrete.

### Analytic Approach

We used three approaches of increasing strength, and report all three because the gap between them is itself informative.

**Simple before-and-after.** Compare regional turnover in the pre-period to the post-period. This is the 51-to-33 comparison. It is the weakest design available because it attributes every change in the period to the intervention, including changes caused by the freight cycle.

**Difference-in-differences using the OTR fleet as control.** Compare the regional change (18 points) to the OTR change (11 points), yielding a difference-in-differences estimate of approximately 7 percentage points. This is a substantially stronger design, and it is the estimate we consider most defensible. It rests on a parallel trends assumption — that absent the intervention, regional and OTR turnover would have moved together — which we can neither verify nor reject with the data available, for reasons discussed in limitations.

**Terminal-level decomposition.** Because all four terminals received identical treatment on identical dates, differences among them cannot be caused by the treatment itself. They must reflect interaction between the treatment and local conditions. This decomposition is descriptive rather than causal, but it is the most diagnostically useful part of the analysis.

We also stratified separations by tenure band to characterize who is leaving, and attempted to link detention exposure to retention at the driver level. The latter attempt failed for coverage reasons described below.

### Handling of Terminal Transfers

Eighty-nine drivers changed terminal assignment during the observation window. This is roughly 12 percent of the regional population and is large enough to distort terminal-level rates if handled carelessly. We attributed each driver's exposure to the terminal where they were assigned at each point in time, splitting exposure across terminals for transferred drivers, and attributed separations to the terminal of assignment at the separation date.

This is the defensible convention, but it is not free of assumptions. A driver who transfers from Evansville to Fort Wayne in month four and separates in month ten is counted as a Fort Wayne separation, even though the conditions that prompted the transfer — and possibly the eventual separation — originated at Evansville. Under an alternative convention attributing separations to the terminal of longest tenure, the Fort Wayne and Louisville improvements narrow modestly and the Evansville result worsens. The direction of the terminal ranking is stable across conventions; the magnitudes are not. We flag this because the terminal comparison is doing significant work in our conclusions.

### What We Could Not Do

We could not construct a driver-level regression relating detention exposure to separation hazard across the full window, because telematics coverage does not extend into the pre-period far enough to establish a baseline. We could not separate the referral bonus effect from the pay conversion effect, because they overlap in time and population with only one month of separation. We could not use separation reason codes as a primary evidence source, because their quality is inadequate. Each of these is treated in the limitations section.

---

## Results

### The Headline Comparison

Regional annualized turnover fell from 51 percent in the twelve months before the conversion to 33 percent in the twelve months after, across 742 drivers. In absolute terms this is an 18-percentage-point decline; in relative terms, a reduction of approximately 35 percent.

Translated into operational terms, an 18-point reduction on a 742-driver fleet corresponds to roughly 130 fewer separations per year. At a fully loaded replacement cost in the range the recruiting function typically cites — recruiting spend, orientation, road testing, reduced productivity during ramp-up, and the safety cost associated with newer drivers — the avoided cost is substantial and, on the simple comparison alone, would appear to more than offset the $3.4 million program cost.

We would caution the board against that arithmetic, for the reasons that follow.

### The Comparison Fleet

The OTR fleet received neither intervention. Its turnover fell from 68 percent to 57 percent over the same twelve-and-twelve window — an 11-point improvement, or roughly 16 percent in relative terms.

This is the most important single number in the brief after the headline. The OTR fleet's improvement occurred without any compensation change, without a referral bonus, and without any other identified program intervention. Whatever caused it — most plausibly the contraction in freight volumes and the corresponding reduction in outside job openings — was also operating on the regional fleet.

| Fleet | Pre-period turnover | Post-period turnover | Change | Received hourly conversion | Received referral bonus |
|---|---|---|---|---|---|
| Regional (742 drivers) | 51% | 33% | −18 pts | Yes | Yes |
| Over-the-road (310 drivers) | 68% | 57% | −11 pts | No | No |
| Difference-in-differences | — | — | −7 pts | — | — |

The difference-in-differences estimate of approximately 7 percentage points is our best available estimate of the combined effect of the pay conversion and the referral bonus on regional turnover. It is roughly 39 percent of the raw improvement. The remaining 61 percent is most plausibly attributable to the external environment.

Two caveats attach to this estimate, pulling in opposite directions.

The estimate may be **too low** if the freight contraction affected OTR operations more severely than regional operations. Long-haul and truckload-adjacent markets are typically more cyclically exposed than regional LTL, which is anchored to local and retail distribution demand. If OTR drivers faced a sharper reduction in outside options than regional drivers did, then the OTR fleet's 11-point improvement overstates the counterfactual for regional, and the true regional-specific effect exceeds 7 points.

The estimate may be **too high** if regional and OTR drivers do not compete in the same labor market and the two populations were on divergent trends before the intervention. A driver leaving OTR work is often leaving long-haul entirely — for regional work, for local delivery, or out of driving. A driver leaving regional work is more likely moving to another regional carrier in the same metro. These are different substitution patterns and they need not respond to the freight cycle identically.

We cannot resolve this with current data. Extending the turnover series backward by 24 months for both fleets — which is feasible from HR records, though it requires manual reconstruction for the earliest period — would allow a direct test of whether the two fleets moved in parallel before March 2025. We regard this as the single highest-value additional analysis available and recommend it as a precondition for the OTR decision.

### The Referral Bonus Confound

The $2,500 referral bonus launched in February 2025, one month before the pay conversion, and applied to the same regional population. This creates a confound that the current design cannot resolve.

Referral programs affect turnover through at least two channels. The first is selection: referred hires tend to stay longer than hires sourced through job boards, because the referring driver pre-screens for fit and because the new hire enters with an existing social tie at the terminal. The second is retention of the referrer: a driver who has recruited a friend has an additional reason to remain.

Both channels operate on the same outcome the pay conversion is meant to influence, in the same population, beginning one month earlier. With a single month of separation between program starts and turnover measured on an annualized basis, no statistical technique available to us can cleanly apportion the 7-point difference-in-differences effect between the two programs.

What we can say is directional. Referral-sourced hires are a minority of post-period regional hiring, which limits how much of the aggregate improvement the bonus can mechanically explain through selection alone. The bonus is therefore unlikely to account for the entire 7 points. But it could plausibly account for a meaningful share — and it costs a small fraction of $3.4 million.

This has a direct implication for the OTR decision that we want to state plainly. If a substantial portion of the regional improvement came from the referral bonus rather than the pay conversion, then the cheaper intervention is doing disproportionate work. The board has an obvious and inexpensive test available: extend the referral bonus to the OTR fleet first, alone, and observe the effect for two to three quarters before committing to the $6.2 million pay conversion. This sequencing costs a small fraction of the pay conversion and would generate exactly the evidence the current analysis lacks.

### The Freight Cycle

Regional freight volumes fell approximately 9 percent industry-wide during the post-period. The mechanism by which this reduces turnover is direct: fewer loads means fewer trucks needed, which means competing carriers reduce hiring, which means a driver contemplating departure has fewer places to go.

The magnitude is consequential. Industry experience across multiple freight cycles indicates that driver turnover is strongly and inversely correlated with freight demand, and that cyclical swings can move turnover rates by amounts comparable to or larger than most compensation interventions. A 9 percent volume contraction is a meaningful soft patch.

The OTR fleet's unaided 11-point improvement is our best internal evidence of the cycle's magnitude. It is consistent with the external picture.

The forward-looking implication deserves the board's attention. If the freight cycle is responsible for the majority of the observed improvement, then the improvement is not durable. When volumes recover and competing carriers resume hiring, outside options return and turnover pressure returns with them. The relevant question for the board is not whether turnover fell in a soft market — it did, in both fleets, including the one that got nothing — but whether the pay structure will hold turnover down when the market tightens.

The current data cannot answer that question because the post-period contains no tightening market. Only continued observation through a demand recovery will resolve it.

### Terminal-Level Variation

The terminal results are, in our assessment, the most informative finding in this analysis.

| Terminal | Pre-period turnover | Post-period turnover | Change |
|---|---|---|---|
| Fort Wayne | 46% | 24% | −22 pts |
| Louisville | 58% | 30% | −28 pts |
| Columbus | 44% | 41% | −3 pts |
| Evansville | Approximately flat | Approximately flat | Negligible |

All four terminals received the same $28.50 hourly rate, the same detention guarantee, and the same $2,500 referral bonus, on the same effective dates, administered through the same payroll system. The treatment was uniform. The results were not.

Two terminals — Fort Wayne and Louisville — improved dramatically. Louisville's 28-point decline is the largest single movement in the dataset and comes off the highest pre-period base. Fort Wayne's 22-point decline brings it to 24 percent, which is a genuinely strong number for regional LTL. Columbus moved three points, which is within the range of ordinary year-to-year variation for a terminal of its size. Evansville did not move.

Because the treatment was identical, the variation must come from something the treatment interacted with. We considered four candidate explanations.

**Detention exposure.** This is the explanation most consistent with the mechanism the conversion was designed to address. The conversion's distinguishing feature relative to mileage pay is that it compensates non-driving time — specifically, time spent waiting at shipper and consignee docks. Under mileage pay, detention is uncompensated and functions as a pure loss to the driver. Under hourly pay with a detention guarantee, it becomes paid time.

The size of that improvement depends entirely on how much detention a driver actually experiences. A driver on routes averaging four hours of weekly detention gains materially. A driver on routes averaging thirty minutes gains almost nothing, and the conversion is close to a wash.

Gene Prokop's route context supports this reading. Fort Wayne's regional lanes include a substantial share of appointment-based deliveries to distribution centers and manufacturing facilities with known dock congestion — the kind of freight where drivers routinely wait. Louisville's lane structure carries similar exposure, with the added factor of a dense cluster of appointment-driven consignees in the metro. Columbus and Evansville run different freight mixes, with a higher proportion of drop-and-hook and live-load work at facilities with shorter dwell.

If that reading is correct, the pay conversion produced large gains exactly where detention was worst and negligible gains where it was not. This is the pattern we observe. But we want to be explicit that this is an inference built on route context and terminal knowledge, not a measured relationship, because the telematics coverage gap prevents us from testing it directly. We flag it as the leading hypothesis, not as a finding.

**Local labor market conditions.** Terminals compete for drivers in local markets with different characteristics. The Louisville metro carries substantial competing demand from large logistics operations, which typically produces both higher baseline turnover and greater sensitivity to relative pay improvements. Louisville's high pre-period rate of 58 percent is consistent with a competitive local market, and a pay increase that moved Sycamore Ridge from below-market to at-or-above-market would produce exactly the large improvement observed. Evansville's smaller market with fewer competing employers may mean that drivers there had fewer outside options to begin with — meaning turnover was already constrained by lack of alternatives, and improving pay changed little.

This explanation is testable against external wage data and would materially change the interpretation. If Louisville's gain came from closing a market-relative pay gap rather than from detention compensation, then extending the structure to OTR depends on where OTR pay sits relative to its own market, which is a different question with a different answer.

**Baseline levels and regression to the mean.** Louisville and Fort Wayne started higher than Columbus. Terminals with unusually high rates in one period tend to move toward the average in the next for purely statistical reasons. Some portion of the Louisville improvement is likely mean reversion. The effect is unlikely to explain a 28-point movement in full, but it is not zero, and it argues for caution in treating Louisville as the model case.

**Terminal management and local practice.** Turnover is sensitive to dispatcher behavior, scheduling predictability, home-time reliability, and the quality of the relationship between drivers and terminal management. These factors vary across terminals and are not captured in payroll or HR data. A terminal that pairs a pay increase with improved dispatch practice will outperform one that changes pay alone. We have no systematic measurement of this and cannot rule it out; terminal-level exit interview data, if it existed in usable form, would speak to it.

We cannot distinguish among these four explanations with the data in hand. That inability is itself the finding the board should take away. A uniform program produced highly non-uniform results, which means the program's effect is conditional on local factors we have not identified. Any projection of the regional result onto the OTR fleet requires knowing which local factors matter and whether OTR operations share them. We do not currently know that.

### Tenure Concentration

Drivers with less than one year of tenure account for 71 percent of all separations.

This is a large concentration and it reframes the entire problem. The turnover Sycamore Ridge experiences is overwhelmingly early-tenure turnover. Drivers who pass the one-year mark stay at rates that, by implication, are quite good.

The implications run in several directions.

First, it changes what the headline turnover rate means. A 51 percent annualized rate does not describe a fleet where half the drivers depart annually. It describes a fleet where a relatively small number of positions cycle repeatedly — a driver hired in month two leaves in month seven, the replacement leaves in month eleven, and a single position generates two separations in a year while the experienced core remains stable.

Second, it changes what the pay conversion can plausibly have done. Compensation structure affects a driver's assessment of the job over time, and a driver comparing hourly-plus-detention against a mileage offer elsewhere is making a considered comparison. But early-tenure departures are frequently driven by factors other than rate: mismatch between the job as recruited and the job as experienced, dissatisfaction with home time, difficulty with a particular lane or dispatcher, onboarding quality, and the ordinary attrition of people discovering the work is not for them. A pay conversion addresses some of this — particularly if drivers were recruited on mileage-pay earnings expectations that detention made unachievable — but not all of it.

Third, and most importantly for the board's cost analysis, it identifies a lever that may be larger and cheaper than compensation. If 71 percent of separations occur in the first year, then interventions targeting the first year — onboarding, mentorship pairing, realistic job previews during recruiting, structured 30/60/90-day check-ins, deliberate assignment of new drivers to lanes with manageable detention exposure — operate on the majority of the problem. These interventions typically cost far less than $6.2 million.

We recommend that the board consider the OTR pay conversion not against the alternative of doing nothing, but against the alternative of a first-year retention program at a fraction of the cost. That is the comparison that determines whether $6.2 million is well spent, and it is not the comparison currently before the board.

A related question we could not answer: did the tenure distribution of separations shift between periods? If the pay conversion reduced early-tenure departures specifically, that suggests it addressed a recruiting-expectation gap. If it reduced mid-tenure departures, that suggests it improved competitive position against other carriers. These have different implications for OTR, where recruiting expectations and competitive dynamics both differ. The stratified analysis is straightforward from existing HR records and we recommend it be completed before the board decides.

### What We Could Not Measure: The Detention Mechanism

The pay conversion's central design feature is compensation for detention time. Testing whether that feature drove the retention improvement requires linking driver-level detention exposure to driver-level separation outcomes across both periods.

We cannot do this. Telematics detention records begin in April 2024. The pre-period runs from March 2024 through February 2025. Detention data therefore covers eleven of twelve pre-period months, but the deeper problem is that it does not extend far enough back to establish a stable baseline of detention exposure by driver, by lane, or by terminal prior to the intervention. We can characterize detention in the post-period well, and partially in the pre-period, but we cannot construct the pre-intervention exposure profile needed to test whether high-detention drivers responded more strongly than low-detention drivers.

That test is exactly what would settle the terminal-variation question and would provide the strongest available basis for projecting to OTR. If high-detention drivers showed large retention improvements and low-detention drivers showed none, the mechanism would be established and the OTR projection would reduce to a measurable question: how much detention do OTR drivers experience?

Within the post-period alone, we can observe detention distribution across terminals, and preliminary examination is consistent with the pattern Prokop describes — Fort Wayne and Louisville lanes show higher average dwell than Columbus and Evansville lanes. We report this as consistent with the hypothesis but decline to treat it as confirmation, because post-period-only comparison cannot establish that the difference existed before the intervention or that it caused the differential response.

---

## Limitations

We state these plainly because the decision at hand involves $6.2 million and the board should understand precisely how much weight this analysis will bear.

**Confounded interventions.** The referral bonus and the pay conversion launched one month apart in the same population. Their effects cannot be separated with the available data. Any statement attributing the full 7-point difference-in-differences effect to the pay conversion is unsupported.

**Non-equivalent comparison group.** The OTR fleet differs from the regional fleet in work characteristics, home time, driver demographics, tenure distribution, baseline turnover, and labor market exposure. It is the only internal control available and it is better than no control, but it is not a matched comparison. The parallel trends assumption underlying the difference-in-differences estimate is untested. Extending the turnover series backward by 24 months would allow a direct test and should be done before the board relies on the 7-point figure.

**Single external cycle.** The entire post-period sits within a soft freight market. We have no observation of the pay structure's performance under tightening demand, when outside options return. The durability of the improvement is unknown and unknowable from this data.

**Telematics coverage gap.** Detention records begin April 2024, preventing a driver-level test of the mechanism the program was designed around. This is the most consequential data limitation and it is not recoverable retrospectively.

**Terminal transfer attribution.** Eighty-nine drivers changed terminals mid-period. Our attribution convention is defensible but affects terminal-level magnitudes. The ranking of terminals is stable across alternative conventions; the size of the gaps is not.

**Separation reason coding.** HR separation reason codes are unreliable. Departing drivers frequently give non-specific reasons, exit interviews are inconsistently conducted, and coding practice varies across terminals. Coded reasons cannot be used to distinguish pay-motivated departures from other departures, and we have not relied on them. This means we have no direct evidence of driver-stated motivation, which is a real gap in a compensation study.

**No wage benchmarking.** We have not compared Sycamore Ridge's post-conversion hourly rate to prevailing market rates in each of the four terminal markets. The terminal variation may substantially reflect differences in where $28.50 sits relative to local competition. This is obtainable from external survey data and should be obtained.

**Regression to the mean.** Terminals with extreme pre-period rates tend to move toward the average. Louisville's 58 percent starting point makes some portion of its 28-point improvement attributable to this effect.

**Selection into and out of the regional fleet.** Drivers transferring between fleets during the window may bias the comparison if the transfers were systematically related to the pay change. If the hourly rate attracted OTR drivers into regional roles, both the regional improvement and the OTR baseline would be affected. We identified transfers but did not model this selection.

**Cost side not independently verified.** The $3.4 million figure was supplied by finance. We have not audited whether it includes payroll taxes, workers' compensation premium effects, or offsetting productivity changes. Whether hourly pay changed driver productivity — miles per hour worked, stops per shift — is a separate question this brief does not address and one that could materially alter the program's net cost.

---

## Implications

### What the Board Can Reasonably Conclude

Regional turnover improved substantially, from 51 to 33 percent. That is real and it is not disputed.

The majority of that improvement — roughly 11 of 18 points — is most plausibly attributable to the freight cycle rather than to any Sycamore Ridge action, based on the OTR fleet's comparable unaided improvement.

Approximately 7 points appear attributable to the regional-specific interventions, and those 7 points are shared between the pay conversion and the referral bonus in unknown proportion.

The effect was highly concentrated in two of four terminals, which means the intervention interacts strongly with local conditions that have not been identified.

Early-tenure drivers account for 71 percent of separations, identifying a distinct and possibly larger lever.

### What the Board Cannot Conclude

That the pay conversion alone caused the improvement. That the improvement will persist when freight demand recovers. That a comparable effect would occur in the OTR fleet. That $3.4 million was the efficient allocation, or that $6.2 million would be.

### Recommendation on the OTR Extension

We recommend the board defer the decision pending three specific analyses, all of which can be completed within one quarter using existing data or low-cost additions.

**First, extend the turnover series backward.** Reconstruct monthly turnover for both regional and OTR fleets for the 24 months preceding March 2024. This tests the parallel trends assumption directly. If the two fleets moved together historically, the 7-point difference-in-differences estimate gains substantial credibility. If they diverged, the estimate is unreliable and the entire causal reading requires revision. This is the highest-value analysis available and requires no new data collection, only manual reconstruction from HR records.

**Second, characterize detention exposure in the OTR fleet.** Using post-April-2024 telematics, measure current detention exposure for OTR drivers and compare it to regional exposure by terminal. If the detention mechanism is what drove the Fort Wayne and Louisville results, then the OTR extension's value depends directly on OTR detention levels. If OTR detention is comparable to Fort Wayne's, the case strengthens considerably. If it resembles Evansville's, the $6.2 million is likely to purchase very little retention improvement. This is a measurable question with existing data.

**Third, benchmark $28.50 against prevailing market rates** in each terminal market and against prevailing OTR compensation. If the terminal variation reflects competitive positioning rather than detention, the OTR question becomes a question about where OTR pay sits relative to its own market — a different analysis with potentially a different answer.

### A Sequenced Alternative

We recommend the board consider a lower-cost path that generates decision-relevant evidence rather than requiring the full commitment immediately.

**Extend the referral bonus to OTR first, alone.** This costs a small fraction of $6.2 million and, because it is not confounded with a simultaneous pay change, it produces a clean estimate of the bonus's independent effect. That estimate then allows a much better apportionment of the regional 7 points and directly informs the pay conversion decision. This is the single most efficient piece of evidence the company could purchase.

**Pilot the hourly conversion on a defined OTR subgroup** — one domicile or one lane group — rather than fleet-wide. A staged rollout at perhaps a third of the cost creates an internal comparison group and generates causal evidence that the regional rollout, implemented fleet-wide and simultaneously with another program, cannot provide. This would also avoid repeating the design error that limits the present analysis.

**Fund a first-year retention program in parallel.** Given that 71 percent of separations occur within twelve months, structured onboarding, mentorship pairing, realistic job previews, and deliberate lane assignment for new drivers address the majority of the problem at a small fraction of the cost. This is not an alternative to compensation work but a complement, and its omission from the current decision framing is notable.

### On Measurement Going Forward

Three changes would materially improve the company's ability to evaluate future interventions.

Avoid launching overlapping programs in the same population within the same quarter. The referral bonus and the pay conversion are individually sensible and jointly unevaluable. A one-quarter separation would have preserved the ability to distinguish them at essentially no cost.

Preserve telematics history. The April 2024 start date is the binding constraint on the most important analysis in this brief. Detention data cannot be reconstructed retrospectively.

Improve separation reason capture. Structured exit interviews with consistent coding, conducted by someone outside the driver's reporting line, would provide direct evidence of departure motivation. In a compensation study, the absence of driver-stated reasons is a significant gap.

### Closing

The conversion appears to have helped. The honest estimate of how much it helped is considerably smaller than the headline suggests, is shared with a much cheaper program, and is concentrated in terminals whose distinguishing characteristics we have identified as a hypothesis rather than measured as a fact. The $6.2 million OTR question turns on whether the mechanism that worked at Fort Wayne and Louisville exists in the OTR fleet. That is an answerable question, and the answer is within reach in roughly one quarter. We recommend the board obtain it before committing.
