# What Drove First-Quarter Churn at Ledgerline Systems: An Assessment Ahead of the July Pricing Conversion

**Prepared by:** Ji-Won Paek, Revenue Operations Analyst
**Commissioned by:** Samuel Oyelaran, Chief Revenue Officer
**Exit interview data supplied by:** Beatriz Salgado, Vice President of Customer Success
**Date:** 29 July 2026
**Distribution:** D. Abernathy-Pruitt (CEO), S. Oyelaran (CRO), B. Salgado (VP CS), Executive Staff

---

## The Question and What Was Found

Chief Executive Diane Abernathy-Pruitt asked revenue operations a direct question: what caused gross churn to rise from 5.2 percent annualized in the first quarter of 2025 to 9.7 percent annualized in the first quarter of 2026, and does the answer bear on whether the second tranche of pricing conversions should proceed in July as scheduled?

The question is urgent because the January 2026 repackaging moved 39 percent of accounts from per-seat licensing to a per-document rate at renewal, and the remaining 61 percent are scheduled to convert on the July renewal cycle. If the repricing caused the churn increase, converting the balance of the book would extend the damage across a larger population. If something else caused it, delaying the conversion would forfeit the commercial rationale for the change without addressing the actual problem.

**The short answer is that the available records cannot cleanly separate the effect of the repricing from three other things that happened at the same time, and the largest of those confounds — a simultaneous platform migration with no usage telemetry on the old system — is not recoverable after the fact.** What the records do support is a narrower and still useful set of findings.

First, churn concentrated sharply in small accounts. Accounts under $12,000 of annual contract value churned at 14.2 percent annualized; accounts above $50,000 churned at 4.1 percent. This is a 3.5-fold difference and it is the single strongest pattern in the data.

Second, the *order* in which accounts experienced the platform migration and the repricing is associated with a large difference in outcome. Accounts migrated to the new portal before being repriced churned at 5.8 percent. Accounts repriced before being migrated churned at 11.9 percent. This is the most decision-relevant finding in the brief, and it is also the one most vulnerable to confounding, because migration sequence was not randomly assigned.

Third, a support capacity collapse in February — five of eighteen support staff resigned, and median first response time rose from four hours to nineteen — overlaps the churn window closely enough that it cannot be excluded as a contributing cause and may be a substantial one.

Fourth, the renewal calendar concentrates 38 percent of the book in January, which means the first quarter is structurally the highest-exposure quarter of the year. Comparisons to a full-year rate, or to quarters with lighter renewal loads, will overstate the anomaly.

Fifth, two of the largest departures by contract value were documented in exit interviews as acquisition-driven — the customer was acquired and consolidated onto an acquirer's existing system — and are not attributable to pricing, product, or service. Because the book is small enough that individual large accounts move the aggregate, removing these two materially changes the revenue-weighted picture while leaving the logo-count picture nearly unchanged.

The recommendation that follows from this is not "proceed" or "halt." It is that the July conversion should proceed only in a modified form that (a) sequences migration ahead of repricing for every remaining account, (b) excludes or specially handles the sub-$12,000 segment, and (c) does not begin until support first response time has recovered to a stated threshold. Each of these conditions is derived from a specific finding below, and each is testable in a way the January cohort was not.

---

## Data and Methods

### Records used

Three record systems were consulted. Each was built for an operational purpose other than churn analysis, and each carries limitations that follow from that.

**Billing records.** The billing system holds contract value, billing frequency, invoice history, payment status, renewal date, and the licensing model in effect for each account. Coverage is complete for all 2,140 accounts, and the data are reliable because they are the basis on which the company invoices and recognizes revenue. Annual contract value figures used in this brief are taken from the contract in effect at the start of the first quarter, not from the renewal quote, which matters because for repriced accounts those two numbers differ by construction. The billing system also carries the date on which each account's licensing model changed, which is how the repricing date used in the sequence analysis was derived.

The principal limitation of billing records for this purpose is that they record the terms of the relationship, not the customer's experience of it. A billing record shows that an account moved from per-seat to per-document pricing on 14 January and did not renew on 12 February. It does not show whether the customer objected to the new rate, whether the customer understood it, whether the customer's document volume made the new rate favorable or unfavorable relative to the old, or whether the customer's decision had anything to do with price at all.

**Customer relationship records.** The CRM holds account ownership, segment classification, industry code, support ticket history, renewal opportunity stages, notes from customer success managers, and the structured exit interview forms that Beatriz Salgado's team completes when an account gives notice. Coverage of the structured fields is complete. Coverage of the free-text fields is uneven and depends on the diligence of the individual owner, which varies.

Exit interviews were completed for a majority of the first-quarter departures but not all of them. Some accounts simply stopped responding and lapsed at term. Where an exit interview exists, it records a primary reason selected from a fixed list and a free-text elaboration. The fixed list was designed before the repricing and does not contain a "pricing model change" option; representatives have been recording these under "price" or "other," which means the structured field cannot be used to count repricing-attributed departures without reading the free text alongside it. This is a material weakness and it is the reason this brief does not present a clean count of "accounts that left because of the repricing." No such count can be produced honestly from the current records.

Exit interviews carry a further and more fundamental limitation, which is that they capture what a departing customer chose to say to a vendor representative at a moment when the relationship was ending. Customers routinely cite price when the underlying dissatisfaction is with service, because price is the least confrontational reason to give. Customers also cite budget or reorganization when the real reason is a competitive displacement they would rather not discuss. Exit interviews are evidence, but they are testimony, not measurement, and they should be weighted accordingly.

**Product telemetry.** The new portal, live since September 2025, emits event-level telemetry: logins, sessions, documents processed, features used, error encounters, and time-to-completion for core workflows. This is high quality data and it is the kind of data most useful for churn analysis, because it measures behavior rather than stated intent.

It exists only for the new portal. The legacy web portal was never instrumented. There is no login history, no usage history, no feature adoption history, and no engagement trend for any account prior to its migration. This is the single most consequential gap in the analysis and it is discussed at length in the limitations section.

### Population and definitions

The analysis covers all 2,140 accounts active as of 1 January 2026. Gross churn is defined as annual recurring revenue lost from cancellations and non-renewals, expressed as a percentage of beginning-period ARR and annualized by multiplying the quarterly rate by four. This is the same definition used in the prior-year comparison, so the 5.2 percent and 9.7 percent figures are constructed identically. Downgrades are excluded from gross churn and are not analyzed here; a separate downgrade analysis is recommended below because the repricing may be producing contraction that the churn metric does not capture.

Account size bands were set at the existing segment boundaries used by customer success — under $12,000, $12,000 to $50,000, and above $50,000 — rather than at boundaries chosen to maximize contrast. This matters for credibility: the bands were not selected after seeing the results.

Migration and repricing dates were both taken from system-of-record timestamps rather than from project plans, because project plans reflect intent and timestamps reflect what happened. Where an account's migration timestamp and repricing timestamp fell within the same seven-day window, the account was classified as "concurrent" and excluded from the sequence comparison; this affected a modest number of accounts and their exclusion is noted where relevant.

### Methods

The analysis is descriptive. It reports churn rates by segment and by cohort and compares them. It does not attempt causal inference through regression, matching, or any other technique, and the reason is worth stating plainly rather than burying.

The conditions for credible causal estimation are not present. The repricing was not randomly assigned — it was assigned by renewal date, which correlates with when the account was originally sold, which correlates with account size, industry, and tenure. The migration was not randomly assigned either; it was sequenced by the platform team according to technical criteria including data complexity and integration count, both of which correlate with account size. The two treatments overlap in time with each other and with a support capacity failure that affected all accounts but would affect high-touch accounts differently from low-touch ones. And the outcome window is one quarter, in which the renewal calendar concentrates 38 percent of the book.

A regression run on this data would produce coefficients. Those coefficients would not mean what a reader would take them to mean, and presenting them would create false precision on a question where the honest answer is that the design does not support a clean estimate. The descriptive results below are reported with their confounds named alongside them, which is less satisfying than a point estimate and more defensible.

---

## Results

### Churn by account size

Churn is concentrated in small accounts to a degree that dominates every other pattern in the data.

| ACV band | Annualized gross churn, Q1 2026 |
|---|---|
| Under $12,000 | 14.2% |
| $12,000–$50,000 | (intermediate) |
| Above $50,000 | 4.1% |

The under-$12,000 band churned at 3.5 times the rate of the above-$50,000 band. The middle band falls between them and does not disturb the monotonic pattern.

Two readings of this are possible and they carry different implications.

The first reading is that this is normal. Small accounts churn more than large accounts in essentially every business-to-business software company. They have less invested in the relationship, less switching cost, fewer integrations, less internal political commitment to the decision, and less vendor attention. A 3.5-fold gradient between the smallest and largest bands is not by itself evidence of anything unusual. Under this reading, the relevant question is not why small accounts churned at 14.2 percent but whether they churned at 14.2 percent last year too.

The second reading is that the repricing interacted with account size. A per-document rate changes the economics of the relationship differently depending on the ratio of seats to document volume. An account with many light users processing few documents was well served by per-seat pricing and is poorly served by per-document pricing, or the reverse, depending on where the rate was set. Small accounts are more likely to sit at the extremes of that ratio, because they have less internal averaging. A small account with three users processing high document volume may have seen a large increase; a small account with twelve occasional users processing low volume may have seen a decrease. The aggregate churn rate does not distinguish these cases.

**The prior-year comparison by band is the test that separates these readings, and it should be run before the July decision.** If the under-$12,000 band churned at approximately 14 percent in the first quarter of 2025, the size gradient is structural and the repricing story weakens considerably. If that band churned at 7 or 8 percent last year and 14.2 percent this year, the gradient steepened, and the steepening requires explanation. This comparison is straightforward to produce from billing records and was not completed in time for this brief. It is the highest-priority open item.

A figure supporting this section would show annualized churn on the vertical axis against ACV band on the horizontal, with two series — first quarter 2025 and first quarter 2026 — plotted as paired bars. The visual question the figure answers is whether the 2026 series is uniformly elevated above 2025 or whether the elevation is concentrated in the left-hand bands. Uniform elevation points toward a general cause such as the support failure. Left-concentrated elevation points toward something that affected small accounts specifically, which the repricing plausibly did.

A second consideration bears on how much weight the size finding should carry. Because the under-$12,000 band contains many accounts each contributing little revenue, a 14.2 percent churn rate in that band translates into a modest absolute ARR loss. The 4.1 percent rate in the above-$50,000 band, applied to a much larger revenue base per account, may represent comparable or greater absolute dollars. The brief reports rates because rates are what the CEO asked about, but the July decision should be made with the absolute revenue exposure in view as well, and those figures should accompany any recommendation that treats the small-account segment differently.

### Churn by sequence of migration and repricing

This is the finding most directly relevant to the July decision.

Accounts that were migrated to the new portal *before* their repricing took effect churned at 5.8 percent annualized. Accounts that were repriced *before* they were migrated churned at 11.9 percent. The repriced-first group churned at roughly twice the rate of the migrated-first group. Accounts where the two events fell within seven days of each other were classified as concurrent and excluded.

The mechanism this suggests is intuitive and worth stating because it explains why the direction of the effect is the direction observed rather than the reverse. An account that has already moved to the new portal has experienced the improved product before being asked to accept new commercial terms. The value proposition and the price change arrive in a defensible order: here is the better system you are now using, and here is the pricing that goes with it. An account that is repriced first experiences the sequence in the opposite and less defensible order: here is a new rate, and separately, at some point in the coming months, here is a platform change you will need to absorb. The second sequence asks the customer to accept a commercial change on the strength of a promise rather than a demonstration, and it delivers two disruptions as two separate events rather than one coherent transition.

This mechanism is plausible. It is also exactly the kind of story that fits observed data without being the reason for it, and the brief must be explicit about why.

**Migration sequence was not randomly assigned.** The platform team sequenced migrations according to technical criteria — data volume, integration count, custom field usage, and the complexity of each account's approval workflow configuration. Accounts with simpler configurations migrated earlier. Accounts with complex configurations migrated later. Configuration complexity correlates with account size, with tenure, and with the depth of the customer's operational dependence on the product.

This creates a specific and serious problem. Deep operational dependence is one of the strongest known predictors of retention in business software. An account with sixteen integrations and a heavily customized approval workflow is hard to migrate *and* hard to leave. If such accounts systematically landed in the migrated-first or repriced-first group, the sequence comparison is measuring embeddedness rather than sequence. The direction of the bias depends on which way the platform team's criteria sorted, and determining that requires examining the actual composition of the two groups — which has not been done.

**This is the second-highest-priority open item and it is answerable.** The composition of the two sequence groups should be compared on every dimension available in billing and CRM records: ACV distribution, tenure distribution, integration count, user count, industry mix, and document volume. If the two groups are similar on these dimensions, the sequence finding survives and becomes the primary basis for the July recommendation. If the migrated-first group skews toward larger, older, more embedded accounts, the 5.8 versus 11.9 percent gap is partly or wholly explained by composition, and the sequence recommendation loses its evidentiary basis even though it may remain sensible on other grounds.

There is a further complication specific to the concurrent group. Excluding accounts where migration and repricing fell within seven days was methodologically reasonable — those accounts cannot be assigned a sequence — but it removes from the comparison precisely the accounts that experienced both changes as a single combined event, which is arguably the most operationally realistic scenario and may be the one the company would adopt in July. Their churn rate should be reported separately even though the group is small, because it bears directly on whether a combined approach in July is better or worse than a sequenced one.

A figure supporting this section would show three bars — migrated first, concurrent, repriced first — with annualized churn on the vertical axis, and would carry a second panel beneath it showing the ACV distribution of each group as overlapping density curves. The second panel is the important one. If the three distributions sit on top of each other, the top panel means what it appears to mean. If they are displaced, the top panel is partly a size finding in different clothing, and the size finding has already been reported.

### Churn by renewal month

Thirty-eight percent of the book renews in January. This single fact conditions the interpretation of every other number in this brief.

An account can only churn at a renewal decision point, so churn is not distributed evenly through the year — it is distributed according to the renewal calendar. A quarter containing the January cluster carries far more renewal exposure than a quarter that does not. Comparing first-quarter churn against a smoothed annual rate, or against a quarter with lighter renewal volume, will make the first quarter look anomalous even when nothing anomalous has occurred.

The 5.2 percent prior-year figure is the correct comparison in this respect, since it is also a first-quarter figure drawn from a book with a similar renewal distribution. The year-over-year comparison is therefore sound in structure. The increase from 5.2 to 9.7 percent is a real increase in first-quarter churn, not an artifact of seasonal exposure.

But the renewal calendar affects the analysis in a second and less obvious way, and this one is not neutralized by the year-over-year comparison. **The repricing was applied at renewal, and 38 percent of renewals occur in January.** This means the repriced population and the January-renewing population are very nearly the same population. Any factor specific to January-renewing accounts — the seasonal characteristics of customers who originally bought in January, the budget cycles of their industries, the tenure profile that follows from a January sale in a given year — is entangled with the repricing and cannot be separated from it within this quarter's data.

The month-by-month breakdown within the first quarter is worth reporting for a different reason. Support first response time degraded in February, not January. If churn is elevated in February and March relative to January, that pattern is more consistent with the support failure driving departures than with the repricing driving them, since the repricing landed hardest in January. If churn is elevated in January and declines through the quarter, the reverse. The monthly distribution is a genuine discriminator between the two leading explanations and it should be examined closely.

One caveat attaches to this discriminator. Non-renewal decisions are typically made and communicated in advance of the contract end date, often thirty to sixty days ahead. An account recorded as churning in March may have made its decision in January. The lag between decision and recorded churn blurs the monthly signal, and the analysis should use notice date rather than contract end date where notice date is captured in the CRM. Where it is not captured, the monthly attribution is approximate and should be described as such.

A figure supporting this section would show monthly churn counts and churned ARR across the full trailing twenty-four months, with the January renewal cluster marked and the February support degradation marked. Two years of monthly data make the seasonal shape visible and let a reader judge for themselves whether the first quarter of 2026 departs from the established pattern or merely sits at the high end of it.

### The support backlog

In February, five of eighteen support staff resigned. Median first response time rose from four hours to nineteen — a 4.75-fold increase — and the department lost 28 percent of its capacity in a single month.

The timing places this squarely inside the churn window. A customer who was already unsettled by a new pricing model, or already frustrated by a platform migration, and who then waited nineteen hours for a first response to a problem, encountered three negative experiences in close succession. The support failure is not merely a candidate explanation competing with the repricing; it is a plausible amplifier of it. A customer with a pricing question who receives a same-day answer may be reassured. The same customer who waits most of a business day may conclude that the vendor's service is deteriorating along with its pricing, and that conclusion is much harder to reverse.

Three points about the support data deserve emphasis.

**First, median first response time is the wrong statistic for this purpose.** The median describes the typical ticket. Churn is driven by the worst experiences, not the typical ones. If the median rose from four to nineteen hours, the ninetieth percentile and the maximum rose by considerably more, and it is the customers in that tail who are most likely to have left. The ninetieth-percentile and ninety-fifth-percentile first response times should be pulled, along with the distribution of *resolution* time, which matters more than first response for a customer with a blocking problem. First response can be a holding acknowledgment; resolution is what the customer needs.

**Second, ticket volume during this period is unknown and material.** A 28 percent capacity loss produces a 4.75-fold response time increase only under specific assumptions about demand. If ticket volume was simultaneously elevated — which would be expected during a platform migration, as customers encounter an unfamiliar interface — then the capacity loss and the migration were compounding each other, and the resulting service failure was worse than either alone would produce. Ticket volume by week, segmented by whether the submitting account had migrated, would establish this.

**Third, and most useful for the July decision, support experience can be linked to churn at the account level.** Every ticket is associated with an account. Every account has a retention outcome. The analysis that should be run is straightforward: for accounts that submitted at least one ticket in February or March, compare the churn rate of those whose worst first response time exceeded some threshold — twenty-four hours, say — against those whose tickets were all handled within a few hours. This is not a randomized comparison and it has its own confound, since accounts in distress submit more tickets and are also more likely to churn for the underlying reason that put them in distress. But it is far more informative than the department-level median, and it can be produced from existing CRM records without new instrumentation.

This account-level linkage is the third high-priority open item. Together with the prior-year size comparison and the sequence group composition check, it constitutes the analytical work that should be completed before the July decision is finalized.

A figure supporting this section would overlay two lines on a common weekly time axis: median and ninetieth-percentile first response time on the left vertical axis, and weekly churn notice count on the right. The visual question is whether the churn line moves with the response time line and with what lag. A lag of two to six weeks between service degradation and churn notice would be consistent with the mechanism; a churn peak preceding the service degradation would rule it out as a cause for that peak.

### The two acquisition-driven departures

Two of the largest departures by contract value were documented in exit interviews as acquisitions. In each case the customer was acquired and consolidated onto an acquirer's existing accounts payable system. These departures are not attributable to Ledgerline's pricing, product, or service, and no action the company could have taken would have prevented them.

With 2,140 accounts and $41 million in ARR, the average account carries roughly $19,000 in ARR, but the distribution is heavily skewed and the largest accounts carry many multiples of that. Two large departures can therefore move the aggregate churn rate by a noticeable margin. The exact effect depends on the contract values involved, which should be stated explicitly in any version of this analysis presented to the board.

Two cautions apply to excluding them.

**Acquisition-driven churn is a recurring feature of the business, not a one-time event.** Ledgerline sells to mid-market manufacturers and distributors, sectors with active consolidation. Some acquisition-driven churn occurs every quarter, and some was certainly present in the 5.2 percent prior-year baseline. Excluding it from the current quarter without excluding it from the comparison quarter would manufacture an improvement that does not exist. If the adjustment is made, it must be made symmetrically to both periods, and this brief does not have the prior-year exclusion figure available.

**"Acquisition" in an exit interview is sometimes a proximate cause standing in front of a contributing one.** An acquirer consolidating systems chooses which system to keep. That choice is influenced by contract terms, by the relative satisfaction of the acquired organization with its incumbent vendor, and by switching cost. An acquired customer who was happy with Ledgerline and locked into a favorable multi-year rate is more likely to survive consolidation than one who had just been repriced and was unhappy about it. The exit interviews should be reread with this specifically in mind — not to overturn the classification, which is probably correct, but to determine whether the repricing or the migration featured in the customer's account of how the consolidation decision was made.

The practical handling is to report both figures wherever the aggregate churn rate appears: 9.7 percent as measured, and the adjusted figure excluding documented acquisition churn, with the same adjustment applied to the prior-year comparison. Reporting only the adjusted figure invites the criticism that inconvenient departures were explained away. Reporting only the unadjusted figure overstates the addressable problem.

---

## Limitations

### The telemetry gap is not recoverable

The new portal went live in September 2025 and only accounts on the new portal emit telemetry. There is no usage data of any kind for any account prior to its migration.

This forecloses the most valuable analysis available for a churn question of this type. The standard approach — establish each account's baseline engagement, measure the change following the intervention, and test whether engagement decline predicts departure — requires a pre-intervention baseline. For accounts repriced before migration, no baseline exists. For accounts migrated before repricing, the earliest observation postdates the migration, so any migration effect on usage is invisible; the account is first observed already in its post-treatment state.

This is not a gap that can be filled by better analysis of the existing data. It is not a gap that will close over time, because the past was never recorded. It is a permanent limitation on what can be known about the January cohort, and it should be stated as such rather than treated as an item pending resolution.

The forward-looking consequence is important. **From July onward, both cohorts will be on the new portal and telemetry will be complete.** The July conversion, if it proceeds, can be analyzed with the tools that were unavailable in January — provided the analytical design is established before the conversion rather than after. That is a real argument for proceeding with July under a structured design, and it is addressed in the implications section.

A secondary telemetry issue deserves mention. Even where telemetry exists, an account's usage after migration reflects both the account's underlying engagement and its adaptation to an unfamiliar interface. A drop in documents processed in the weeks following migration might indicate disengagement or might indicate that users were slower on a new system. Distinguishing these requires a stabilization period, and comparisons drawn too soon after migration will conflate learning curve with disengagement.

### Confounds cannot be separated

Four things happened to overlapping populations in overlapping timeframes:

1. Thirty-nine percent of accounts were repriced from per-seat to per-document at renewal.
2. Accounts were migrated from the legacy portal to the rebuilt portal on a technical sequencing.
3. Support capacity fell 28 percent in February and response times rose nearly fivefold.
4. Thirty-eight percent of the book reached its renewal decision point in January.

No account experienced only one of these. Every repriced account also faced a renewal decision, most in January, and every account was exposed to the support degradation. The treatment groups are not clean, the control group is not clean, and there is no population that experienced the repricing without the migration environment or the support failure.

Under these conditions the question "how much of the churn increase was caused by the repricing?" does not have an answerable form. The data cannot produce a number, and any number produced would be an artifact of modeling assumptions rather than a measurement. This brief declines to produce one. That is a limitation of the evidence, not an omission in the analysis, and the distinction matters for how the finding should be used in the July decision.

### Selection into treatment

Neither the repricing nor the migration was randomly assigned.

Repricing was assigned by renewal date. Renewal date is a function of original sale date, which correlates with tenure, with the sales motion in effect at the time, with the pricing in effect at the time, and with account characteristics that varied as the company's target market evolved. January-renewing accounts are not a random sample of the book.

Migration was assigned by technical complexity, which correlates with account size, integration depth, and operational embeddedness. Migration-sequence groups are not random samples either.

The consequence is that every cohort comparison in this brief is potentially a comparison of different kinds of accounts rather than a comparison of different treatments. The size analysis is least affected, because size is measured directly rather than inferred. The sequence analysis is most affected, and its principal finding should be treated as provisional until the composition check described above is complete.

### Exit interviews are incomplete and structurally biased

Exit interviews were not completed for all departures. Accounts that lapsed without responding are systematically absent, and those accounts are plausibly different from accounts that engaged enough to give an exit interview — likely less engaged, possibly smaller, possibly more price-sensitive. The exit interview sample is not representative of the churned population.

The response categories do not include a pricing-model option, so repricing-related departures are distributed across "price," "other," and free text. This makes structured tabulation unreliable.

And exit interview responses reflect what customers chose to tell a vendor at a difficult moment. Price is a socially easy reason to give. Service dissatisfaction is harder to articulate and easier to fold into a price complaint. The reported reason distribution should be read as directional evidence about customer framing, not as a measurement of cause.

### Single-quarter window

One quarter is a short observation period for a change of this kind. Some effects of the January repricing will not appear until the accounts reach their next renewal in 2027. Others may appear as downgrades, seat reductions, or document-volume management rather than as churn — a customer on per-document pricing has a direct incentive to process fewer documents through the system, which reduces revenue without producing a cancellation. **This form of contraction is entirely invisible to a gross churn analysis and should be measured separately before the July decision**, since it may be a larger effect than churn and is the specific revenue risk that per-document pricing introduces.

Conversely, some first-quarter churn may reflect accounts that had already decided to leave for reasons predating the repricing, and whose departure happened to be recorded in a quarter when the repricing was underway.

### Small numbers in subgroups

Some of the cells reported here contain modest account counts. The concurrent migration-and-repricing group in particular is small. Rates computed on small denominators are unstable, and a difference of a few accounts can move a subgroup rate by several percentage points. Where subgroup rates are cited in the July discussion, the underlying counts should be cited alongside them so that readers can judge their reliability.

---

## Implications for the July Decision

### What the evidence does and does not support

The evidence supports three claims with reasonable confidence:

- Churn is concentrated in small accounts, at 14.2 percent versus 4.1 percent between the extreme bands.
- Accounts repriced before migration churned at roughly twice the rate of accounts migrated before repricing, 11.9 versus 5.8 percent, though this comparison's composition has not been verified.
- A severe support degradation coincided with the churn window and cannot be excluded as a contributing cause.

The evidence does not support any claim about how much of the churn increase the repricing caused. That question is not answerable from these records and will not become answerable through further analysis of them.

### Three conditions on the July conversion

The following conditions are each derived from a specific finding and each is stated so that compliance can be verified.

**One: sequence migration ahead of repricing for every remaining account.** This is the most actionable implication. The sequence finding is provisional, but the asymmetry of the decision favors acting on it. If the sequence effect is real, following it avoids roughly half the churn in the July cohort. If it is an artifact of composition, following it costs only scheduling flexibility. There is no plausible mechanism by which repricing before migration is *better* than the reverse, so the downside of acting on a possibly-spurious finding is close to zero and the upside is large.

Whether this condition can be met for all accounts is a platform-team question. If some accounts cannot be migrated before their July renewal date, those accounts should have their repricing deferred to a later renewal rather than being repriced on the legacy portal.

**Two: exclude or specially handle the sub-$12,000 segment.** The size finding is the strongest in the data, and pending the prior-year comparison, its interpretation is open. The prudent course is to hold this segment back from the July conversion until the prior-year figure establishes whether the 14.2 percent rate is elevated or normal. If it is normal, the segment can be converted in a subsequent cycle with no loss. If it is elevated, the segment needs a modified approach — a rate floor, a transition credit, a longer notice period, or a different document-tier structure — designed specifically for accounts whose seat-to-document ratio makes the standard conversion punitive.

The absolute revenue at stake in this segment is modest, which makes holding it back inexpensive. It is also the segment where a bad outcome is most likely and where the company has the least ability to intervene account by account, since these accounts do not carry dedicated customer success coverage.

**Three: do not begin the conversion until support response times have recovered to a stated threshold.** Whatever the support failure's contribution to first-quarter churn, converting the remaining 61 percent of the book while the support organization is operating at reduced capacity compounds risk without benefit. A conversion generates support volume by design — billing questions, rate explanations, invoice reconciliation — and delivering that volume into a department that has not recovered its staffing is a predictable failure.

The threshold should be stated numerically and verified before the conversion begins. Median first response time returning to its prior four-hour level is the obvious benchmark; the ninetieth-percentile figure should be included as well, since the tail is what drives churn. Current staffing against the eighteen-person establishment, and the ramp status of any replacements hired, should be reported alongside.

### The argument for proceeding rather than deferring

There is a substantive argument for proceeding in July under these conditions rather than deferring the conversion.

**Telemetry will be complete.** By July, the migration will be finished or nearly so, and both the converted and unconverted populations will be on the instrumented portal. For the first time, the company can observe usage before and after a pricing change. This is the analysis that could not be run in January and it is the analysis that answers the question the CEO actually asked. Deferring the conversion defers that measurement indefinitely.

**Deferral has costs that are easy to overlook.** It extends the period during which the company operates two pricing models, complicating billing, quoting, forecasting, and sales compensation. It leaves 61 percent of the book on a model the company has decided is wrong. And a deferral announced after a conversion was scheduled signals uncertainty to a customer base that has already absorbed one disruption.

**The remaining population is not the same as the January population.** July-renewing accounts differ from January-renewing accounts in tenure, size mix, and industry composition. The January experience is informative but not directly transferable, and the differences should be characterized before the July cohort's risk is estimated from January's outcome.

### The design that should accompany the conversion

If July proceeds, it should proceed as a measured event rather than a repeat of January. Four elements:

**A pre-registered analysis plan.** Specify before the conversion what will be measured, on what population, over what window, and against what comparison. Written in advance, this prevents the outcome from being reinterpreted after the fact, which is the failure mode that made January uninterpretable.

**A staggered rollout.** Convert in waves rather than all at once. Accounts converted in the second wave serve as a partial comparison group for the first, and if early waves show elevated churn or usage decline, later waves can be halted. Wave assignment should be as close to random as operational constraints allow — the absence of anything resembling random assignment is the single largest reason the January cohort cannot be analyzed.

**Baseline telemetry capture.** Record each account's usage profile in the weeks before its conversion: documents processed, active users, session frequency, feature usage. This is the baseline that did not exist in January and it is available now at no cost beyond the discipline of capturing it.

**Downgrade and volume monitoring alongside churn.** Per-document pricing creates a direct incentive to reduce document volume. Monitor document throughput per account after conversion. A decline is a revenue loss that gross churn will not show and may be the dominant financial effect of the change.

### Open items before the decision

Three analyses should be completed. Each is answerable from existing records and none requires new instrumentation.

**Prior-year churn by ACV band.** Determines whether the 14.2 percent small-account rate is elevated or structural. This single figure changes the interpretation of the strongest pattern in the data.

**Composition check on the sequence groups.** Compare migrated-first and repriced-first accounts on size, tenure, integration count, user count, industry, and document volume. Determines whether the 5.8 versus 11.9 percent gap reflects sequence or selection.

**Account-level support experience linked to retention.** For accounts with tickets in February or March, compare churn rates by worst first response time experienced. Determines whether the support failure contributed at the account level or merely coincided at the department level.

A fourth item is recommended but not blocking: reread the exit interviews for the two acquisition-driven departures to determine whether the repricing or migration featured in the customer's account of the consolidation decision.

### Closing

The honest position is that the first quarter of 2026 combined a pricing change, a platform migration, a support failure, and the year's heaviest renewal cluster into a single quarter, and the records the company keeps cannot separate them. The 9.7 percent figure is real. Its causes are not individually measurable from what was recorded.

What can be said is that small accounts fared badly, that sequence appears to matter and costs nothing to respect, and that converting the remaining book while support is impaired would be a choice to repeat the conditions that made January uninterpretable. The July conversion can proceed on those terms, and if it does, it should be built so that in October the company can answer the question it cannot answer today.
