# Self-Checkout and Inventory Shrink at Wexford Market Group

**A Research Brief Prepared for the June Capital Review**

Prepared by the Retail Analytics Group
Nadia Farrukhzad, Manager
Cranberry Township, Pennsylvania

---

## The Question and What We Found

Wexford Market Group has converted 24 of its 61 stores to self-checkout since 2023. The finance organization has budgeted $11.5 million to convert 20 more starting in the third quarter. Loss prevention has objected that shrink is rising where the equipment has been installed. The chief operating officer asked this group to determine whether self-checkout conversion causes higher inventory shrink, and if so, how much, before the capital committee meets in June.

The short answer is that self-checkout conversion appears to raise shrink, but by substantially less than the raw comparison of converted and unconverted stores suggests, and the increase is concentrated narrowly enough that it can probably be managed rather than avoided.

Converted stores currently run 1.94 percent shrink as a share of sales. Unconverted stores run 1.41 percent. That gap of 53 basis points is what loss prevention has been pointing to, and taken at face value it would imply roughly $4.6 million in additional annual losses across the converted fleet at current sales volumes. But the 24 converted stores were not chosen at random. They were selected for high volume, and high-volume stores in this chain were already running higher shrink before any self-checkout equipment arrived — 1.62 percent, against a fleet baseline that placed unconverted stores near 1.38 percent in the same pre-installation periods. Roughly 24 of the 53 basis points, then, reflects which stores were picked rather than what was installed in them.

The remaining movement — an increase of about 32 basis points at converted stores from their own pre-installation baseline, against a drift of about 3 basis points at unconverted stores over the same span — is our best estimate of the conversion effect. That works out to approximately 29 basis points, or on the order of $2.5 million annually across the 24 converted stores. Against $6.1 million in realized annual labor savings at those same stores, the conversion program remains net positive by roughly $3.6 million a year, though by a margin about 40 percent narrower than the labor case alone would suggest.

Two further findings bear directly on the capital decision. First, the increase is not spread evenly across the store. Health and beauty and fresh meat account for the large majority of the category-level movement; center-store dry grocery is close to flat. Second, the eleven converted stores that removed staffed express lanes at the same time show materially worse outcomes than the thirteen that kept them. The lane-configuration split is large enough that it may be doing more work in the results than the self-checkout equipment itself, though we cannot separate the two cleanly with the data we have.

Our confidence in the direction of the effect is high. Our confidence in its precise magnitude is moderate. Our confidence in the mechanism — which is what would tell the committee whether the next 20 conversions can be designed to avoid the problem — is low, and we say why below.

---

## Data and Methods

### The shrink measurement and its structure

Shrink at Wexford is measured only at physical inventory. Each store counts twice a year. This is the central constraint on everything that follows, and it deserves to be stated plainly before any results are read.

Because counts happen twice a year, and because the first self-checkout installations went live in 2023, each store has contributed four usable observations. Across 61 stores that yields 244 store-half-years. One of those — a converted store's May 2025 count — was voided after the counting vendor made a systematic error in the perishables sections and the count could not be reconstructed. That observation is excluded entirely rather than imputed. We did not carry the prior period forward or interpolate, because either choice would have manufactured precision we do not have. The working dataset is therefore 243 store-half-years.

Two hundred forty-three observations sounds like a reasonable sample until you consider what is actually being compared. Twenty-four converted stores with four observations each is 96 observations, minus the void, so 95. Thirty-seven unconverted stores give 148. But the observations within a store are not independent of one another; a store that runs high shrink in one period tends to run high in the next, for reasons having to do with its layout, its neighborhood, its management, and its receiving practices. The effective sample size for detecting a store-level treatment effect is much closer to 61 than to 243. This is why we do not report significance tests with the confidence that the raw observation count might invite.

The twice-yearly cadence also means that shrink at Wexford is a *cumulative* measure. A count taken in May tells us what walked out of the building, spoiled, was miscounted, or was written off incorrectly between the prior November count and that May. It does not tell us when in that six-month window the loss occurred, or through what channel. For a store that converted to self-checkout in, say, February, the May count blends eleven weeks of pre-conversion operation with fifteen weeks of post-conversion operation, and there is no way to unbundle them. We handled this by classifying each store-half-year as pre- or post-conversion based on whether the conversion date fell in the first or second half of the measurement window, and by excluding the four store-half-years where conversion fell within three weeks of the window midpoint. This is a crude rule. It is the best available.

### The scan data and what it can support

Item-level scan data — transaction logs identifying what was scanned, at which terminal, in what sequence, with what interventions from staff — exist only from March 2025 forward. Before that, the point-of-sale system retained transaction totals and department-level subtotals but discarded item detail after 90 days.

This is a serious limitation and we want to be precise about its consequences. Sixteen months of item-level data covering conversions that began in 2023 means the scan data cannot be used to compare pre- and post-conversion behavior at any store. Every store that has self-checkout had it before the scan data begins. The scan data can therefore support only cross-sectional comparison — converted stores against unconverted stores, or converted stores against each other — during a period when the treatment assignment was already fixed and already confounded by the selection problem described below.

What the scan data *can* do, and what we used it for, is characterize the mechanics of loss in a way the inventory counts cannot. Specifically:

- It identifies non-scan events at self-checkout terminals where the security scale registers weight in the bagging area without a corresponding item scan.
- It identifies scan-avoidance patterns such as an item scanned and voided, then the transaction completed, with a weight discrepancy.
- It identifies produce and bulk lookups where a lower-priced code was entered for a higher-priced item, when the weight is inconsistent with the entered code.
- It identifies attendant intervention rates and the disposition of those interventions.

What it cannot do is tie any of these events to inventory outcomes. We know a store had 4,200 weight-discrepancy events in a quarter. We do not know that those events cost the store anything, because the discrepancies may reflect a customer setting down a purse, a bagged item shifting, or a legitimate item the scale weighed poorly. The events are a signal about opportunity and behavior, not a measurement of loss. Anyone who reports a scan-data figure as a dollar loss estimate is doing arithmetic the data does not support, and we have avoided it here.

We also want to flag that the scan data covers only self-checkout terminals in a meaningful way. Staffed lane transactions are logged, but the diagnostic fields — weight discrepancy, intervention, void-with-discrepancy — are either absent or structured differently, because staffed lanes have no security scale. The scan data therefore cannot tell us whether loss migrated to staffed lanes, stayed at self-checkout, or occurred somewhere else in the store entirely. This matters more than it might appear, and we return to it in the limitations section.

### Sales and labor data

Sales are taken from the general ledger by store and period, which is the same denominator loss prevention uses, so the shrink percentages here reconcile to the loss prevention reporting. Labor hours are taken from the workforce management system and expressed per thousand dollars of sales, which is the standard the operations group uses. Both series are complete for all 61 stores across the full window and neither presented data quality issues.

The labor figure cited in this brief — an 8 percent reduction in hours per thousand dollars of sales at converted stores, worth roughly $6.1 million annually — was produced by the operations finance group, not by us. We have reviewed the calculation and find it sound, with one caveat. The $6.1 million is a gross labor cost reduction. It does not net out the maintenance contract, the attendant staffing that self-checkout banks still require, or the amortization of the equipment itself. Those are handled elsewhere in the capital model. We cite the figure as given because the committee will see it in that form, but the shrink findings in this brief should be compared against the fully loaded net benefit, not against $6.1 million.

### Method

The analysis proceeds in three steps, each of which answers a narrower question than the last.

**Step one** is the raw comparison: converted stores against unconverted stores in the current period. This is the comparison loss prevention has made and it is the one the committee is most likely to have in mind. We report it and then explain why it overstates the effect.

**Step two** is a difference-in-differences comparison. We compare the change in shrink at converted stores from their own pre-installation baseline to the change at unconverted stores over the same calendar periods. This removes the portion of the gap attributable to converted stores having been higher-shrink stores to begin with. It assumes that, absent conversion, converted and unconverted stores would have drifted in parallel. That assumption is doing a lot of work and we test it as best we can below.

**Step three** is decomposition within the converted group: by merchandise category, and by whether the store removed staffed express lanes at conversion. This is where the actionable findings are, and it is also where the sample sizes get small enough that we report patterns rather than estimates.

We did not attempt a regression with store-level controls. With 61 stores, four periods, and a treatment that was assigned on an observable characteristic that correlates with the outcome, a regression would produce coefficients with standard errors that look more informative than the underlying data warrants. The difference-in-differences framing is more transparent about what is being assumed.

---

## Results

### The raw comparison and the selection problem

The headline numbers are these. Across the most recent two measurement periods, converted stores show shrink of 1.94 percent of sales. Unconverted stores show 1.41 percent. The gap is 53 basis points.

At converted-store sales volumes, 53 basis points is approximately $4.6 million a year. That figure, set against $6.1 million in labor savings, is what has made the conversion program look marginal to loss prevention. If it were the right figure, the objection would be a strong one.

It is not the right figure, because the 24 converted stores were selected for high volume, and volume correlates with shrink in this chain for reasons that have nothing to do with checkout technology. Higher-volume stores in the Wexford fleet are larger, carry deeper assortments in health and beauty and fresh, sit in denser trade areas, receive more frequent deliveries, and turn inventory faster — every one of which is independently associated with higher measured shrink. They also tend to be the stores where physical inventory is hardest to execute cleanly, which introduces measurement noise in the same direction.

The evidence for this is direct. In the measurement periods before any equipment arrived, the 24 stores that would later be converted were already running 1.62 percent shrink. The 37 stores that would remain unconverted were running approximately 1.38 percent in those same periods. The pre-existing gap was therefore about 24 basis points — nearly half the current gap — and it existed before a single self-checkout terminal was installed.

| | Pre-installation | Current | Change |
|---|---|---|---|
| Converted stores (n=24) | 1.62% | 1.94% | +32 bp |
| Unconverted stores (n=37) | ~1.38% | 1.41% | +3 bp |
| Gap | 24 bp | 53 bp | +29 bp |

This is the central table in the brief and we would ask that it be the one carried into the committee discussion. The 53-basis-point gap is real, but roughly 24 basis points of it is a fact about which stores were chosen, not about what happened to them. The difference-in-differences estimate — the change at converted stores net of the change at unconverted stores — is approximately 29 basis points.

Applied to converted-store sales, 29 basis points is roughly $2.5 million a year. That is the number we believe best represents the shrink cost of conversion at the 24 stores converted to date.

### How much confidence the parallel-trends assumption deserves

The difference-in-differences estimate is only as good as the assumption that converted and unconverted stores would have moved in parallel absent conversion. We tested this in the only way available, which is imperfect.

With four observations per store and conversions beginning in 2023, most converted stores have only one or two pre-conversion observations. That is not enough to establish a pre-trend at the store level. What we could do is look at the subset of nine stores converted in late 2024 and 2025, which have three pre-conversion observations each. Across those nine, pre-conversion shrink was flat to slightly rising — a drift of about 2 basis points per period — against an unconverted-store drift of about 1 basis point per period over the same span. The trends are close enough that the parallel-trends assumption looks defensible, but nine stores is a thin basis for the claim and we would not want the committee to treat the 29-basis-point figure as tightly bounded.

Our working view is that the true conversion effect lies somewhere between 20 and 40 basis points, with 29 as the point estimate. In dollar terms that is a range of roughly $1.7 million to $3.4 million annually across the converted fleet. The conclusion that conversion remains net positive against labor savings holds across that entire range, which is worth stating, because it means the decision does not hinge on resolving the imprecision.

### Category decomposition

Within converted stores, the increase is not distributed evenly. Two departments account for the substantial majority of the movement.

**Health and beauty** shows the largest increase. This department runs high-value, small-format, easily concealed merchandise — analgesics, razor cartridges, cosmetics, oral care, over-the-counter remedies — and it is the department where loss prevention has historically concentrated attention across the industry. At converted stores, health and beauty shrink rose by well over a percentage point of department sales from the pre-installation baseline, a change several times the magnitude of the store-level average. Because health and beauty is a relatively small share of total sales, this large departmental movement translates into a moderate share of the store-level effect, but it is the single largest contributor.

**Fresh meat** shows the second-largest increase, and it is the more interesting of the two. Fresh meat is not a department one would expect to move on concealment, because the packages are bulky, cold, and awkward. The pattern in the scan data suggests a different mechanism: mislabeling and code substitution. Self-checkout requires customers to scan a barcode on a service-case or prepackaged item, and the scan data shows an elevated rate of transactions in which a meat item's weight is inconsistent with the price-lookup code entered — the signature of a customer ringing a cheaper cut than the one in the cart, or ringing a smaller weight. This is consistent with the broader industry pattern in which variable-weight and code-entry categories, rather than high-theft categories, drive self-checkout loss.

**Center-store dry grocery** is close to flat. Packaged goods, canned goods, paper, cleaning products, and beverages show departmental shrink changes within a few basis points of their pre-installation levels, indistinguishable from noise given the measurement precision available. This is the finding that most constrains what mechanism can be operating. If self-checkout conversion produced a general increase in opportunistic non-scanning, center-store would move, because center-store is where most items and most transactions are. It does not move. Whatever is happening is category-specific.

**Produce** shows a modest increase, smaller than fresh meat but detectable. The mechanism is presumably similar — code entry on variable-weight items — though produce items are individually low-value enough that the dollar impact is limited.

**Frozen, dairy, bakery, and deli** show no pattern we would report as distinct from noise.

We would describe the category decomposition visually as follows: a horizontal bar chart, departments on the vertical axis ordered by magnitude of change, showing change in departmental shrink as a percentage of departmental sales from pre-installation baseline to current. Health and beauty extends furthest right, fresh meat next, produce third and much shorter, and the remaining departments cluster tightly around zero with two or three extending marginally left of it. A second panel beside it would rescale each bar by the department's share of total store sales, which reorders the chart — fresh meat and health and beauty remain the top two but their relative heights converge, and center-store's near-zero bar becomes visually wide but flat, making the point that the largest department contributes almost nothing to the change.

### Lane configuration

Eleven of the 24 converted stores removed staffed express lanes at the same time they installed self-checkout. Thirteen kept them. This was not a controlled variation; it reflected store-level layout constraints and, in some cases, district manager preference. But it produces a split worth examining closely, because it is the closest thing to a natural experiment in the dataset.

The eleven stores that removed express lanes show markedly higher increases than the thirteen that retained them. The gap between the two groups is large enough that if one analyzed only the thirteen retention stores, the estimated conversion effect would be well under half the fleet-wide figure — closer to 12 to 15 basis points than to 29. Conversely, the eleven removal stores drive most of the aggregate increase.

We want to be careful about what this does and does not establish.

It does not establish that removing express lanes causes shrink. The eleven removal stores may differ from the thirteen retention stores in ways that independently predict shrink. Removal was more common in stores with tighter front-end footprints, which tend to be older stores in denser trade areas. We checked pre-installation shrink for the two subgroups and found the removal stores were running modestly higher even before conversion — perhaps 6 to 8 basis points higher — which accounts for some but not most of the current difference. The subgroups also differ in size: eleven and thirteen stores, four periods each, is not a sample from which to draw confident causal inferences about a second-order interaction.

What it does establish is that the conversion effect is heterogeneous, and that the heterogeneity aligns with a variable the company controls. That is directly relevant to the June decision, because the 20 stores in the proposed tranche have not yet had their front-end configurations finalized.

Two mechanisms could produce this pattern and we cannot distinguish between them. The first is deterrence: a staffed express lane puts an employee in sight-line of the self-checkout bank, and the presence of a staffed lane may also route a portion of small-basket traffic away from self-checkout entirely, reducing exposure. The second is attendant staffing: stores that removed express lanes may have redeployed those hours differently, or may have run leaner self-checkout attendant coverage because the labor savings target was more aggressive at those stores. The scan data shows meaningfully lower attendant intervention rates at removal stores, which is consistent with the second mechanism, but intervention rate is itself a function of traffic volume and terminal count, so the comparison is not clean.

If the second mechanism is the operative one, then the finding is not about express lanes at all — it is about attendant coverage, and the express lane variable is a proxy. That would be a more useful finding, because attendant coverage is cheaper to adjust than store layout. We flag this as the single highest-value follow-up question and address it in the implications section.

A figure describing this result would be a scatter plot with one point per converted store: pre-installation shrink on the horizontal axis, current shrink on the vertical axis, with a forty-five-degree reference line marking no change. Points above the line are stores that got worse. Retention stores would be plotted as open circles and removal stores as filled circles. The visual impression would be that most open circles sit near the reference line, several slightly above it and two or three below, while filled circles sit consistently and sometimes substantially above it. Two removal stores would appear as clear outliers well above the line; excluding them narrows but does not eliminate the group difference.

### Scan-data findings

The scan data, covering March 2025 forward, supports three observations that are consistent with the inventory findings without independently confirming them.

First, weight-discrepancy events at self-checkout terminals are common — several thousand per store per quarter at higher-volume locations — but the overwhelming majority resolve without attendant intervention, either automatically or through customer correction. The subset that involves an attendant override and a subsequent transaction completion is much smaller and is the population most plausibly associated with loss.

Second, the rate of price-lookup code entries inconsistent with registered weight is elevated in fresh meat and produce relative to what a purely mechanical error rate would predict. This is the strongest scan-level corroboration of the fresh meat inventory finding.

Third, attendant intervention rates vary substantially across converted stores, and the variation correlates negatively with the store's shrink increase — stores with higher intervention rates show smaller increases. This is suggestive but must be read cautiously, because intervention rate depends on staffing, terminal count, traffic, and how individual attendants are trained to use the override function. It is a correlation across 24 stores with no pre-period, and it could easily reflect that well-run stores are well-run in multiple respects simultaneously.

We did not find evidence in the scan data of concentrated organized activity — no repeated patterns tied to particular times, terminals, or transaction signatures that would indicate systematic rather than opportunistic loss. Given sixteen months of data and no pre-period comparison, absence of such evidence is weak evidence of absence.

---

## Limitations

We have flagged constraints throughout. This section consolidates the ones that should qualify how the findings are used, in rough order of how much they should temper confidence.

**Shrink is measured twice a year, which is the binding constraint on everything.** Four observations per store is not enough to establish trends, detect timing, or isolate the effect of interventions made between counts. Every estimate in this brief is a comparison of period averages across a small number of coarse observations. If the company wants a more precise answer to this question, the answer is not better analysis — it is more frequent measurement, at least in the categories where the effect concentrates. Cycle counting in health and beauty and fresh meat, even monthly, would transform what can be known here.

**The selection problem is corrected but not eliminated.** Difference-in-differences removes the portion of the gap attributable to converted stores having been higher-shrink to begin with, but only under the assumption that the two groups would have trended in parallel. We have limited ability to test that assumption and the test we could run rests on nine stores. If high-volume stores were on a steeper shrink trajectory than low-volume stores for independent reasons — changing trade area demographics, for instance, or the chain's own assortment decisions concentrating high-theft SKUs in larger stores — then some of the 29 basis points we attribute to conversion belongs elsewhere.

**Item-level scan data begins after all conversions.** There is no before-and-after in the scan data. It cannot confirm that self-checkout caused any observed pattern; it can only describe what self-checkout transactions look like now, at stores that already have it. The mechanism findings — code substitution in fresh meat, intervention-rate correlations — are consistent with the inventory results but are not independent confirmation of them.

**We cannot observe where loss occurs, only that inventory is missing.** Shrink at physical inventory aggregates theft at self-checkout, theft at staffed lanes, theft from the sales floor without a checkout transaction at all, employee theft, receiving errors, vendor shortages, unrecorded markdowns, spoilage, and counting error. Nothing in our data distinguishes among these. It is entirely possible that self-checkout conversion changed the *composition* of shrink without changing its total by as much as we estimate, or that it changed something else about store operations — front-end staffing levels, floor coverage, manager attention — which then affected shrink through a channel unrelated to the checkout terminals. The 29 basis points is an estimate of the effect of *conversion*, understood as a bundle of changes, not of self-checkout terminals in isolation.

**The express-lane finding is observational within an observational study.** Eleven stores against thirteen, non-randomly assigned, with a modest pre-existing difference between them. We report it because it is the most actionable pattern in the data and because ignoring it would be worse than reporting it with caveats. It should be treated as a hypothesis worth testing in the next tranche, not as an established effect.

**The voided count.** One converted store's May 2025 count was excluded after the counting vendor error. We verified that the store is not an outlier in its other three periods and that its exclusion does not materially move any reported figure. But it is a converted store, and its exclusion means the converted group rests on 95 rather than 96 observations at a point where every observation carries weight.

**Sales as a denominator moves with conversion.** Shrink is reported as a percentage of sales. If self-checkout conversion changed sales — through throughput, basket size, or customer mix — then the denominator moved along with the numerator and the percentage comparison is not clean. We checked comparable sales at converted stores against unconverted stores and found no divergence large enough to matter at the precision available, but "no divergence we can detect" is not the same as "no divergence."

**We have not analyzed employee theft separately.** Some portion of any shrink change at a store undergoing significant front-end reorganization may involve employees rather than customers. Loss prevention has better visibility into this than we do and we would defer to their judgment on whether it warrants separate treatment.

**Sixteen months is a short window for a behavioral effect.** There is a body of retail experience suggesting self-checkout shrink effects grow over time as customer familiarity increases, and a competing body suggesting they attenuate as operators tune the technology. Our stores converted between 2023 and 2025 and we do not have enough within-store time series to say which pattern applies here. The 29-basis-point estimate is a current-state estimate. It may not be a steady-state estimate.

---

## Implications for the June Capital Review

### The program as it stands

At the 24 stores converted to date, self-checkout has produced roughly $6.1 million in gross annual labor savings and roughly $2.5 million in additional annual shrink. The net is positive by approximately $3.6 million before equipment amortization, maintenance, and attendant staffing costs, which are accounted for elsewhere in the capital model.

The relevant point for the committee is that shrink erodes about 41 percent of the gross labor benefit. That is a large enough share that it should be carried explicitly in the business case for the next tranche rather than treated as a rounding item, but it is not large enough to reverse the case. The conversion program has been economically sound. It has been less sound than the labor-only analysis represented, by a wide margin.

We would also note that loss prevention's objection was substantively correct in direction even though the 53-basis-point figure overstated the magnitude. Shrink at converted stores is rising, it is rising faster than at unconverted stores, and it is rising for reasons connected to the conversion. Walt Kowalczyk's group identified a real problem that the labor-savings analysis had not accounted for. The correction we have made is to the size of the problem, not to its existence.

### What this implies for the proposed 20 stores

Three considerations bear on the tranche decision.

**First, the shrink cost should be built into the tranche business case at a specific number.** If the 20 proposed stores are similar to the 24 already converted, the shrink cost should be modeled at approximately 29 basis points of their sales, with a sensitivity range of 20 to 40 basis points. We would recommend the committee see the net figure and the sensitivity range, not the gross labor figure alone.

There is a reason to think the effect at the next 20 could be smaller. The first 24 were the highest-volume stores in the chain, and volume correlates with the categories where shrink concentrates — larger health and beauty sets, larger service meat operations. The next tranche is, by construction, lower-volume, and may have less exposure in exactly the departments that moved. There is also a reason to think it could be larger: lower-volume stores run thinner front-end staffing and may have less capacity to absorb attendant coverage requirements. We do not have a basis for choosing between these and would model the tranche at the same 29 basis points absent better information.

**Second, the express-lane question should be resolved before the front-end configurations are finalized.** This is the highest-leverage finding in the brief. If the difference between removal and retention stores is real and causal, then configuring the next 20 stores to retain staffed express lanes would cut the expected shrink cost by more than half — from roughly 29 basis points to something in the range of 12 to 15 — at the cost of some portion of the labor savings.

We do not know how much labor savings that would cost, because that depends on the specific staffing model, but the trade is worth constructing explicitly. If retaining an express lane costs, say, 20 percent of the per-store labor benefit and eliminates half the shrink cost, it is clearly worth doing at the ratios we observe. If it costs 60 percent of the labor benefit, it is not. Operations finance can build that comparison quickly and we would recommend they do so before the committee meets.

**Third, category-specific countermeasures are likely to be more efficient than store-level ones.** Because the effect concentrates in health and beauty and fresh meat, and because center-store is flat, general-purpose interventions — more attendants, more cameras, more signage — are poorly targeted. Interventions aimed at those two departments would address most of the exposure at a fraction of the cost.

The obvious candidates are conventional. In health and beauty: relocating the highest-value, smallest-format SKUs out of the self-checkout adjacency, or moving them behind a service counter or into locked or hook-secured fixtures. In fresh meat: eliminating customer code entry where possible by ensuring service-case and prepackaged items carry scannable weight-embedded barcodes, which removes the substitution opportunity entirely. The second of these is a merchandising and packaging change rather than a loss prevention one, and it may be the single most cost-effective action available, since it addresses the mechanism directly rather than deterring the behavior.

We would not recommend the committee approve the tranche conditional on these countermeasures, because we cannot yet quantify their effect. We would recommend they be scoped in parallel.

### Two recommendations about measurement

Beyond the tranche decision, two changes would materially improve the company's ability to answer this class of question.

**Institute cycle counting in health and beauty and fresh meat at converted stores.** Twice-yearly physical inventory is adequate for financial reporting and inadequate for operational management. Monthly or six-weekly cycle counts in the two departments where the effect concentrates would give the company twelve to twenty observations a year instead of two, in exactly the places where the information is valuable. The cost is modest and the analytical return is large. Without this, the company will be in the same position a year from now: reasoning about a real operational problem from four coarse data points per store.

**Randomize configuration in the next tranche.** If the 20 stores in the proposed tranche were assigned to express-lane retention or removal on some basis unrelated to store characteristics — even a partial randomization within matched pairs — the company would have a clean answer to the express-lane question within two inventory cycles. We recognize this cuts against operational preference, and that district managers have views about their own front ends. But the question is worth several hundred thousand dollars a year in expected shrink across the fleet, and it will not be answerable from observational data no matter how much of it accumulates.

### What we would tell the committee in one paragraph

Self-checkout conversion raises shrink at Wexford stores by roughly 29 basis points of sales, about $2.5 million a year across the 24 stores converted so far, not the 53 basis points and $4.6 million that the raw comparison of converted and unconverted stores suggests — the difference being that the converted stores were chosen for high volume and were already running higher shrink before any equipment arrived. That cost erodes about 41 percent of the labor savings the program generates but does not reverse the case for it. The increase concentrates almost entirely in health and beauty and fresh meat, with center-store dry grocery essentially flat, which means targeted merchandising and fixture changes in two departments could address most of the exposure. Converted stores that removed staffed express lanes show substantially worse outcomes than those that kept them, and while eleven stores against thirteen is too thin a comparison to settle the question, it is strong enough that the front-end configurations for the next 20 stores should not be finalized until operations finance has priced the trade between express-lane labor and express-lane shrink. Our confidence in the direction of these findings is high, our confidence in the magnitudes moderate, and our confidence in the mechanisms low — and the company will not improve on that until it measures shrink more often than twice a year in the departments where it is actually moving.

---

*Retail Analytics Group. Questions to Nadia Farrukhzad. Supporting workbooks, store-level detail, and the scan-data extraction specification are available on request.*
