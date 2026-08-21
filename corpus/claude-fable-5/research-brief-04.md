# Self-Checkout Conversion and Inventory Shrink: Evidence from 24 Stores and Implications for the Fiscal 2027 Capital Program

**Wexford Market Group — Retail Analytics**
**Prepared by Nadia Farrukhzad, Manager, Retail Analytics**
**Prepared for Desmond Achebe, Chief Operating Officer, ahead of the June Capital Review**
**Distribution: Rosalind Tan (CFO), Walt Kowalczyk (Director, Loss Prevention)**

---

## The Question and What We Found

Since 2023 Wexford Market Group has installed self-checkout banks in 24 of its 61 stores. The finance organization has budgeted $11.5 million to convert 20 more stores beginning in the third quarter of this year. Loss prevention has objected on the grounds that inventory shrink at converted stores has climbed since the equipment went in. The Chief Operating Officer asked Retail Analytics to answer a single question before the June capital review: **is self-checkout conversion causing higher shrink, by how much, and does the shrink cost outweigh the labor savings that motivated the program?**

The short answer is that self-checkout is raising shrink, but by considerably less than the raw store comparison suggests, and by considerably less than the labor savings the program generates — provided the next wave of conversions is configured differently from the first.

Converted stores currently run shrink of 1.94 percent of sales against 1.41 percent at unconverted stores, a gap of 0.53 percentage points. Taken at face value, that gap would imply roughly $3.7 million a year in incremental loss across the converted fleet. But the comparison is misleading, because the 24 converted stores were not chosen at random. They were selected for high sales volume, and high-volume stores in our chain were already high-shrink stores: before any equipment arrived, the stores later converted were running 1.62 percent shrink against 1.40 percent at the stores that were never converted. When we compare each group's change over time rather than its level — a difference-in-differences design using 243 usable store-half-year inventory observations — the increase attributable to conversion is approximately **0.31 percentage points of sales**, about $2.2 million a year across the converted stores, not $3.7 million.

That 0.31-point increase is not evenly distributed. It concentrates almost entirely in two categories — health and beauty and fresh meat — which together account for roughly two-thirds of the total increase while representing about 18 percent of sales. And it concentrates in a particular subset of stores: the eleven converted stores that removed their staffed express lanes at the same time the self-checkout banks were installed show an attributable shrink increase of roughly 0.47 points, versus 0.18 points at the thirteen converted stores that kept at least one staffed express lane. Item-level scan data, available only from March 2025 forward, are consistent with the inventory evidence and point to non-scanning and price-lookup misuse at self-checkout as the dominant mechanisms.

Against these costs, the labor savings are large and well documented. Labor hours per thousand dollars of sales fell 8 percent at converted stores, worth roughly $6.1 million a year. Netting the attributable shrink against the labor savings, the converted fleet is generating approximately **$3.9 million a year in net benefit**, and even the worst-performing configuration — express lanes removed, no category mitigations — remains net positive today, though its shrink trajectory is deteriorating cycle over cycle.

Our recommendation for the June review is therefore not to cancel the $11.5 million program but to condition it: convert the next 20 stores with at least one staffed express lane retained, deploy specific controls in health and beauty and fresh meat from day one, and build a 0.20-point shrink allowance into the program's financial model rather than the zero allowance in the current pro forma. The remainder of this brief describes the data, the analysis, the results in detail, what the evidence cannot show, and the specific implications for the capital decision.

---

## Background

Wexford Market Group operates 61 grocery stores across western Pennsylvania and eastern Ohio from headquarters in Cranberry Township, employs 7,900 people, and books approximately $1.4 billion in annual sales. The self-checkout program began in the third quarter of 2023, motivated primarily by front-end labor cost and secondarily by chronic difficulty staffing cashier positions in several trade areas. Installations rolled out in waves through 2024; all 24 conversions were complete before the November 2024 physical inventory, which is what makes a clean before-and-after comparison possible.

The 24 converted stores were selected by the operations team on a straightforward criterion: transaction volume. High-volume stores have the longest front-end queues, the most cashier hours to save, and the fastest payback on the roughly $575,000 per-store installation cost. This selection rule is central to interpreting the shrink data, and we return to it repeatedly below. The converted stores average roughly $29 million in annual sales apiece against roughly $19 million at unconverted stores; the 24 converted stores therefore account for approximately $697 million, essentially half of company sales, despite being 39 percent of the store count.

Eleven of the 24 conversions were bundled with a second front-end change: the removal of staffed express lanes, on the logic that self-checkout serves the small-basket customer and the express lane was redundant. Thirteen stores kept at least one staffed express lane. This bundling was an operational choice made store by store, and it turns out to matter a great deal for shrink.

The loss prevention objection, raised by Walt Kowalczyk after the November 2025 inventory cycle, was that converted stores' shrink was visibly higher than the rest of the chain's and rising. That observation is correct as far as it goes. The analytical question is how much of the gap the conversion actually caused, through what mechanisms, in which stores and categories, and whether the cost exceeds the benefit.

---

## Data and Methods

### The inventory data and what they can show

Shrink at Wexford is measured only at physical inventory, which occurs twice a year at every store, in May and November, conducted by a third-party counting vendor. Shrink for a half-year cycle is the difference between book inventory and counted inventory, expressed as a percentage of the period's sales. This is the company's only comprehensive measure of loss, and it has two important properties that shape everything in this brief.

First, it is a low-frequency measure. Each store contributes two observations a year. Since the first installations, each of the 61 stores has completed four post-installation inventory cycles — November 2024, May 2025, November 2025, and May 2026 — yielding a design of 244 store-half-year observations. One observation was lost: the May 2025 count at store 41 (Beaver Falls) was voided after a counting vendor crew error produced an implausible result, and no recount was performed before the books closed. That count is excluded entirely, leaving **243 usable observations** in the post-period panel. We additionally use the two pre-installation cycles (November 2022 and May 2023) to establish baselines, giving the full analysis six cycles per store.

Second, physical inventory measures *net* loss without identifying its cause. A shrink figure of 1.94 percent bundles together external theft, internal theft, spoilage and markdowns not properly recorded, receiving errors, and bookkeeping errors. The inventory data can tell us that converted stores lose more product; they cannot, by themselves, tell us that self-checkout is the mechanism. The category-level detail in the count data (shrink is reported by department) and the timing of changes relative to installation dates are what allow causal inference from this source, and the scan data provide corroborating mechanism evidence.

### The scan data and what they can show

Item-level transaction data from the point-of-sale system — including self-checkout event logs such as weight-security alerts, voids, attendant interventions, and price-lookup entries — exist only from **March 2025 forward**, when the POS data warehouse migration completed. This means scan data cover roughly the last three inventory cycles and none of the pre-conversion period. The scan data therefore cannot support before-and-after comparisons, but they can support cross-sectional comparisons among converted stores (for example, removed-lane versus retained-lane stores) and can characterize *how* loss occurs at self-checkout: unscanned items generating weight discrepancies, mis-keyed price lookups on random-weight items, and unit-movement anomalies in specific categories.

The scan data have their own blind spot, which should be stated plainly: an item that leaves the store without ever being scanned generates no transaction record. We observe the shadows of non-scanning — security alerts, intervention logs, and divergence between units sold and units replenished — not the non-scanning itself.

### The labor data

Labor hours by store and department come from the workforce management system and are complete for the full analysis period. We express labor as hours per thousand dollars of sales to normalize across store volumes, and we convert hour reductions to dollars using fully loaded average front-end wage rates by store.

### The comparison design

The core analytical problem is selection. The 24 converted stores were chosen for high volume, and in our chain high volume is correlated with higher baseline shrink — larger stores sit in denser trade areas, carry broader assortments of theft-prone categories, and run higher transaction counts per labor hour even before any equipment change. A naive comparison of converted versus unconverted stores today attributes to self-checkout a difference that partly existed before self-checkout.

We address this with a difference-in-differences design: we compare the *change* in shrink at converted stores (post-installation cycles versus pre-installation cycles) against the *change* at unconverted stores over the same calendar periods. The unconverted stores absorb chain-wide influences — inflation in retail prices, regional changes in theft activity, changes in counting vendor procedures, seasonal patterns in the May versus November cycles — so that what remains for the converted group is the effect of conversion itself. Formally, we estimate the model on the store-half-year panel with store fixed effects (absorbing each store's permanent shrink level), cycle fixed effects (absorbing chain-wide period shocks), and a treatment indicator switched on for converted stores in post-installation cycles. Standard errors are clustered by store to respect the fact that a store's six observations are not independent. We estimate the same model with the treatment indicator split by lane configuration (express lanes removed versus retained) and, using department-level count data, by merchandise category.

The design rests on a parallel-trends assumption: absent conversion, the converted stores' shrink would have moved in parallel with the unconverted stores'. With only two pre-period cycles we cannot test this assumption as thoroughly as we would like; what we can say is that across the November 2022 and May 2023 cycles, the two groups' shrink moved together (the gap between them was 0.22 points in both cycles, changing by less than 0.02 points), which is consistent with parallel trends over the short pre-window we observe.

---

## Results

### The headline comparison and the selection correction

Table 1 presents the central result of the brief.

**Table 1. Shrink as a percentage of sales, by group and period**

| | Pre-conversion (Nov 2022–May 2023) | Post-conversion (Nov 2024–May 2026) | Change |
|---|---|---|---|
| Converted stores (24) | 1.62% | 1.94% | +0.32 pts |
| Unconverted stores (37) | 1.40% | 1.41% | +0.01 pts |
| **Difference-in-differences** | | | **+0.31 pts** |

The raw cross-sectional gap today — 1.94 against 1.41 — is 0.53 points. But 0.22 points of that gap predates the equipment: the converted stores were already running 1.62 percent shrink when the unconverted group was at 1.40. Meanwhile the unconverted group's shrink has been essentially flat over the analysis period, moving from 1.40 to 1.41, which tells us that chain-wide conditions have not deteriorated. The increase attributable to conversion is the converted group's rise of 0.32 points net of the control group's rise of 0.01 points: **0.31 percentage points of sales**, with a clustered standard error of 0.09 points. The estimate is statistically distinguishable from zero at conventional levels, and also statistically distinguishable from the naive 0.53-point figure. The practical import of the correction is substantial: on the converted stores' roughly $697 million in annual sales, 0.31 points is approximately **$2.2 million a year**, whereas the naive gap would imply $3.7 million. The loss prevention concern is validated in direction but overstated in magnitude by roughly 40 percent if the raw comparison is used.

A figure accompanying this table (described here rather than drawn) would plot mean shrink for the two groups across all six inventory cycles from November 2022 through May 2026. The two lines run parallel through the pre-period, separated by a steady 0.22-point gap; beginning with the November 2024 cycle the converted-store line bends upward while the unconverted line stays flat, and the gap widens cycle by cycle to 0.53 points by May 2026. The visual point is that the *level* difference is old news; the *widening* is what conversion caused — and the widening has not yet plateaued, a point we return to below.

Excluding the voided Beaver Falls May 2025 count does not move these results. As a sensitivity check we re-estimated the model imputing that store's missing cycle from its adjacent counts; the difference-in-differences estimate changes by less than 0.01 points.

### Where the shrink is: category patterns

The department-level count data show that the increase is not a general erosion of control across the store. It is concentrated, sharply, in two places.

**Table 2. Shrink by category at converted stores, pre- versus post-conversion**

| Category | Approx. share of sales | Pre-conversion shrink | Post-conversion shrink | Change |
|---|---|---|---|---|
| Health and beauty | 7% | 2.7% | 4.0% | +1.3 pts |
| Fresh meat | 11% | 2.2% | 3.4% | +1.2 pts |
| Produce | 10% | 2.9% | 3.2% | +0.3 pts |
| Center-store grocery | 45% | 1.1% | 1.1% | +0.0 pts |
| Dairy and frozen | 18% | 0.9% | 1.0% | +0.1 pts |
| All other (GM, bakery-deli, alcohol) | 9% | 2.8% | 3.0% | +0.2 pts |

Health and beauty and fresh meat together contribute roughly two-thirds of the total attributable increase while representing about 18 percent of sales. Center-store grocery — nearly half of sales — shows essentially no change, and dairy and frozen are flat. At unconverted stores, none of these categories moved materially over the same period.

The category pattern is itself evidence about mechanism. Health and beauty items are small, high-value, and easily concealed or passed over a scanner without scanning; the industry literature consistently identifies the category as the most exposed to self-checkout non-scanning. Fresh meat presents a different vulnerability: it is sold largely as random-weight product with scale labels, and at self-checkout a customer can either fail to scan a package or — as the scan data suggest is common — key a random-weight item under a cheap price-lookup code, ringing a ribeye as bananas. Produce, the classic PLU-fraud category, shows a smaller increase than we expected, possibly because our produce margins-of-loss were already high and because the dollar stakes per item are low. That the increase avoids center-store grocery, where items are lower-value and process-driven shrink (receiving, spoilage) dominates, argues against the alternative explanation that converted stores simply became sloppier in general — for instance through the staffing reductions — since general operational decay would show up broadly rather than in the two categories most exposed to checkout-based theft.

### Lane configuration: the eleven-store problem

The second concentration is by store configuration. Eleven of the 24 converted stores removed their staffed express lanes when the self-checkout banks went in; thirteen retained at least one. Estimating the difference-in-differences separately for the two groups:

**Table 3. Attributable shrink increase by front-end configuration**

| Configuration | Stores | Attributable shrink increase | Approx. annual cost |
|---|---|---|---|
| Express lanes removed | 11 | +0.47 pts | ~$1.5M |
| Express lanes retained | 13 | +0.18 pts | ~$0.7M |
| All converted | 24 | +0.31 pts | ~$2.2M |

The removed-lane stores account for roughly two-thirds of the total attributable shrink despite being under half the converted group. The gap between the two configurations (0.29 points) is statistically significant despite the small store counts, and it is robust to controls for store size and trade area.

Two cautions attach to this finding. First, the lane decision was not random either: stores that removed express lanes may differ from stores that kept them in ways we cannot fully observe, and eleven stores is a small sample. Second, the two changes — installing self-checkout and removing the express lane — happened simultaneously at those eleven stores, so we cannot cleanly separate "self-checkout with less supervision" from "less staffed presence at the front end generally." What we can say is that the configuration that pairs self-checkout with a fully staffed express alternative and more staffed presence near the front end produces roughly a third of the shrink increase that the stripped-down configuration produces.

The trajectory difference is at least as important as the level difference. A second described figure would plot the attributable increase by cycle for each configuration across the four post-conversion counts. The retained-lane line is essentially flat, oscillating between 0.15 and 0.21 points across the four cycles — the effect appears at conversion and stays put. The removed-lane line climbs steadily: roughly 0.31 points in the November 2024 cycle, 0.42 in May 2025, 0.53 in November 2025, and 0.61 in May 2026. That pattern is consistent with learning — customers who discover that non-scanning goes unchallenged in a lightly supervised front end repeat and escalate the behavior — and it means the removed-lane stores' current shrink understates where they are heading if nothing changes.

### What the scan data add

The scan data cannot reach back before March 2025, but for the last fourteen months they corroborate the inventory evidence and illuminate mechanism. Three findings stand out.

First, self-checkout weight-security alerts ("item placed in bagging area without scanning" and its variants) run at 14.2 per thousand self-checkout transactions at removed-lane stores against 9.6 at retained-lane stores, and attendant intervention rates per alert are lower at removed-lane stores — alerts are more frequently timed out or overridden without an attendant reaching the station. The alert data are noisy (most alerts are innocent), but the between-configuration gap is stable month over month and consistent with less-supervised stations experiencing and tolerating more non-scanning.

Second, in fresh meat, approximately 2.3 percent of random-weight transactions completed at self-checkout show a mismatch between the scale weight recorded at the station and any plausible weight for the item code entered — the signature of ringing an expensive random-weight item under a cheap PLU. The comparable figure at staffed lanes is under 0.4 percent. Applied to self-checkout meat volume, this single mechanism plausibly accounts for a substantial fraction of the meat-department shrink increase.

Third, in health and beauty, units sold per thousand dollars of store sales declined about 6 percent at converted stores after March 2025 relative to unconverted stores, while replenishment shipments into the category held steady — product is arriving and leaving the building at the old rate, but a smaller share of it is being scanned on the way out. This unit-movement divergence is the closest the scan data come to observing non-scanning directly, and it points at the same category the inventory counts do.

### The labor offset

The program's benefit side is not in dispute. Labor hours per thousand dollars of sales fell 8 percent at converted stores relative to their pre-conversion baseline, with unconverted stores roughly flat over the same period. On a converted-fleet labor base of approximately $76 million a year, the reduction is worth roughly **$6.1 million annually**. The saving is larger at removed-lane stores (about 10.2 percent of labor hours, roughly $3.6 million across the eleven) than at retained-lane stores (about 6.2 percent, roughly $2.5 million across the thirteen), which is mechanical: eliminating the express lane eliminates its staffing.

Netting shrink against labor by configuration: removed-lane stores generate roughly $3.6 million in labor savings against $1.5 million in attributable shrink, a net of about $2.0 million; retained-lane stores generate roughly $2.5 million against $0.7 million, a net of about $1.9 million. Today, in other words, the two configurations net out to similar dollars, and the *marginal* economics of removing the express lane — an extra $1.4 million or so of labor saved against an extra $0.8 to $0.9 million of shrink — are modestly positive on current figures. But the removed-lane shrink line is still rising while its labor savings are fixed; if the May 2026 trajectory continues for two more cycles, the marginal economics of lane removal turn negative, and that calculation ignores the harder-to-quantify costs of a deteriorating theft environment, discussed below.

---

## Limitations

Five limitations deserve explicit statement, because the June decision should be made with them in view.

**The stores were not randomly assigned, and statistics cannot fully cure that.** The difference-in-differences design removes permanent differences between converted and unconverted stores and chain-wide time trends, but it cannot rule out that something else changed differentially at high-volume stores over exactly this period — for example, if organized retail theft intensified specifically in the dense trade areas where converted stores sit, some of the 0.31 points would belong to that trend rather than to the equipment. The flat shrink at unconverted stores, the concentration in checkout-exposed categories, the timing aligned to installation, and the configuration gradient all argue against this alternative, but with 24 treated stores and observational data we characterize the 0.31-point estimate as well-supported rather than proven.

**Two pre-period cycles is a thin baseline.** The parallel-trends check we can run is passed, but a single year of pre-data cannot exclude slower-moving divergence between the groups. Shrink is also a noisy measure at the store-cycle level; individual stores swing several tenths of a point between counts for reasons unrelated to theft, which is why we lean on group averages across 243 observations rather than any store's individual trajectory.

**Inventory counts measure net loss, not theft.** Some portion of shrink at every store is spoilage, markdown bookkeeping, and receiving error. If conversion changed those processes — for example, if reduced front-end staffing degraded markdown discipline in meat — part of the category increase could be process loss rather than theft. The scan-data mechanisms (weight mismatches, unit-movement divergence) indicate theft is the larger component, but the decomposition is approximate.

**The scan data start too late and see too little.** With no pre-March-2025 scan data, every scan-based finding is cross-sectional, inheriting the configuration-selection problem noted above. And non-scanned items are invisible in transaction logs by definition; our unit-movement and alert-based proxies are indirect. The May 2025 Beaver Falls exclusion, by contrast, is immaterial — one observation of 244, with results insensitive to its imputation.

**The estimates describe the first 24 stores, not necessarily the next 20.** The next wave will be somewhat smaller-volume stores (the highest-volume candidates went first), in trade areas with the chain's lower baseline shrink. Effects could be milder there — or the labor savings could be smaller for the same reason. The pro forma should treat 0.31 points as a central estimate for an unmitigated rollout and 0.18 points as the evidence-based estimate for a retained-lane rollout, with appropriate uncertainty around both.

---

## Implications for the June Capital Review

The capital question before the committee is whether to proceed with $11.5 million to convert 20 stores beginning in the third quarter. The evidence supports proceeding, with three conditions that materially change the program's expected economics.

**First, the program remains net positive, and the decision framework should be net, not gross.** The loss prevention objection is directionally correct — conversion causes shrink, roughly 0.31 points of sales as implemented to date — but the debate should not be conducted on shrink alone. The converted fleet nets approximately $3.9 million a year after shrink, against roughly $13.8 million of invested capital in the first wave, and even the worst configuration is net positive today. Cancelling the second wave would forgo an estimated $4.2 million in annual labor savings at the 20 candidate stores (scaled to their volumes) to avoid an estimated $1.0 to $1.7 million in shrink, depending on configuration. That trade fails on the numbers.

**Second, the next wave should be configured as the retained-lane stores were, and the eleven removed-lane stores should be partially re-staffed.** The single largest lever in the data is lane configuration: retaining a staffed express lane cuts the attributable shrink increase by roughly 60 percent (0.18 versus 0.47 points) at a labor cost of roughly four points of front-end hours. On current figures that trade is close to neutral in dollars, but the removed-lane shrink trajectory is still rising after four cycles while the retained-lane effect has been flat since installation — the retained-lane configuration buys a *stable* equilibrium, and stability is worth paying for when the alternative is a loss line compounding at roughly 0.1 points per cycle. We recommend the 20 new conversions retain at least one staffed express lane, and that the eleven removed-lane stores restore one, with the restored labor cost (approximately $1.4 million a year) charged against the program's savings in the pro forma.

**Third, the pro forma should carry a shrink allowance and fund category mitigations.** The current program model assumes zero shrink impact; the evidence says that assumption is wrong even in the best configuration. We recommend the model carry 0.20 points of sales as a shrink allowance for the new wave, and that roughly $400,000 of the $11.5 million be directed to targeted controls in the two categories that carry two-thirds of the loss: camera-assisted scan verification at self-checkout stations for health and beauty items, restriction of the highest-loss health and beauty SKUs to staffed lanes or keeper cases, weight-validation logic that flags random-weight PLU entries inconsistent with recorded scale weight in meat, and attendant staffing standards that keep intervention response inside the alert timeout. Because item-level scan data now exist chain-wide, the new wave can be instrumented from day one — baseline scan data before installation, category unit-movement tracking after — so that the June 2027 review can evaluate the mitigated configuration on evidence rather than extrapolation.

Under these conditions, our central estimate for the 20-store wave is roughly $4.2 million in annual labor savings against roughly $0.8 million in shrink and $0.3 million in incremental mitigation and staffing cost, a net of approximately $3.1 million a year on $11.5 million of capital — a payback of under four years, with the first wave's experience suggesting the estimate is conservative if the mitigations perform. The evidence does not support the program as originally configured at the eleven removed-lane stores; it does support the program the retained-lane stores have been running for four inventory cycles. The June decision, in our view, is not whether to buy more self-checkout, but which of the two programs we have already run to buy more of.

---

*Underlying data: 243 store-half-year inventory observations (Nov 2022–May 2026, one voided count excluded); department-level count detail from the third-party inventory vendor; item-level POS and self-checkout event data, March 2025–May 2026; workforce management labor hours, all periods. Analysis files and model specifications are available from Retail Analytics on request.*

## Appendix A. Technical Notes on Estimation

The difference-in-differences estimates reported in the body were produced from the following specification, estimated on the store-half-year panel of 365 observations (61 stores × 6 cycles, less the voided Beaver Falls May 2025 count):

*Shrink(s,t) = α(s) + γ(t) + β · Converted(s) × Post(t) + ε(s,t)*

where α(s) is a store fixed effect, γ(t) is a cycle fixed effect, and the coefficient of interest β is identified from within-store changes at converted stores relative to within-store changes at unconverted stores. The point estimate is β = 0.313 percentage points with a standard error of 0.091 clustered at the store level (t = 3.44, p < 0.01, 60 clusters). Because the number of treated clusters (24) is modest, we also computed wild-cluster bootstrap p-values; the estimate remains significant at the 1 percent level (bootstrap p = 0.006).

The configuration-split model replaces the single treatment term with two: Converted × Post × LanesRemoved and Converted × Post × LanesRetained. The estimates are 0.468 (SE 0.128) and 0.181 (SE 0.096) respectively; a Wald test rejects equality of the two coefficients at the 5 percent level (p = 0.038). Given eleven and thirteen treated stores per arm, these arm-level estimates carry wider uncertainty than the pooled figure, and the confidence interval on the retained-lane arm extends from roughly 0.00 to 0.37 points — the retained-lane effect is bounded well below the removed-lane effect but is not precisely pinned down on its own.

The cycle-by-cycle event-study version replaces Post with separate indicators for each of the four post-conversion cycles (and, as a placebo, an indicator for the May 2023 pre-cycle). The May 2023 placebo coefficient is 0.014 (SE 0.041), indistinguishable from zero, which is the parallel-trends check referenced in the body. The post-cycle coefficients for the pooled treatment group are 0.24, 0.29, 0.34, and 0.37 for November 2024 through May 2026 respectively; disaggregated by configuration they produce the flat retained-lane path and rising removed-lane path described in the second figure.

Three robustness variants were run. Weighting stores by sales rather than equally moves the pooled estimate to 0.324, reflecting the modest tendency of the largest converted stores to sit in the removed-lane group. Dropping the two converted stores with the largest single-cycle shrink swings moves the estimate to 0.297. Imputing the voided Beaver Falls observation from the mean of its adjacent cycles moves the estimate to 0.309. No variant alters any qualitative conclusion.

## Appendix B. Reconciliation of the Financial Figures

Because several dollar figures in the body are derived rather than directly observed, this appendix shows the arithmetic so the capital committee can trace each number to its source.

**Converted-fleet sales base.** The 24 converted stores average approximately $29.0 million in annual sales; 24 × $29.0M ≈ $697M. The 37 unconverted stores average approximately $19.0 million; 37 × $19.0M ≈ $703M. The sum, $1.40 billion, reconciles to company sales.

**Attributable shrink in dollars.** Pooled: 0.31% × $697M ≈ $2.2M per year. By configuration: removed-lane stores carry approximately $319M in sales (11 stores), so 0.47% × $319M ≈ $1.5M; retained-lane stores carry approximately $378M (13 stores), so 0.18% × $378M ≈ $0.7M. The naive figure cited in the summary applies the raw 0.53-point cross-sectional gap to the same base: 0.53% × $697M ≈ $3.7M.

**Labor savings.** Store labor at converted locations runs approximately $76M annually on a fully loaded basis (roughly 10.9 percent of sales). The 8.0 percent blended reduction yields ≈ $6.1M. By configuration: removed-lane labor base ≈ $34.8M × 10.2% ≈ $3.6M; retained-lane base ≈ $41.2M × 6.2% ≈ $2.5M.

**Net program benefit, first wave.** $6.1M labor − $2.2M shrink ≈ $3.9M per year against approximately $13.8M of installed capital (24 stores × ~$575K).

**Second-wave pro forma (recommended configuration).** The 20 candidate stores carry approximately $470M in combined sales with a labor base of approximately $51M. Applying the retained-lane parameters: labor savings ≈ 6.2% × $51M ≈ $3.2M, plus an allowance for modest attendant-model efficiencies estimated at $1.0M as stations mature, for the $4.2M cited in the body; shrink at the 0.18-point retained-lane estimate ≈ $0.8M (the pro forma carries 0.20 points, ≈ $0.9M, as a conservative allowance); incremental mitigation and monitoring cost ≈ $0.3M. Net ≈ $3.1M annually on $11.5M of capital; simple payback ≈ 3.7 years. At the unmitigated pooled estimate of 0.31 points, net falls to approximately $2.6M and payback extends to roughly 4.4 years — worse, but still inside the company's five-year hurdle. The program breaks even on shrink alone only if attributable shrink at the new stores were to reach approximately 0.9 points of sales, nearly double the worst configuration observed to date; we regard that as an unlikely tail case but note it defines the program's margin of safety.

**Express-lane restoration at the eleven removed-lane stores.** One staffed express lane per store at roughly 70 scheduled hours per week, fully loaded, costs approximately $125K per store, ≈ $1.4M across eleven stores. The offsetting benefit is avoidance of further trajectory deterioration; at the observed 0.09-to-0.11 points-per-cycle drift, two additional cycles of unchecked escalation would add roughly $0.6M to $0.7M of annualized shrink at those stores, and the restoration is expected to arrest rather than merely slow that drift, based on the flat trajectory at retained-lane stores. This is the least certain figure in the brief, since it rests on extrapolating a trend we recommend interrupting, and it should be revisited at the first post-restoration inventory cycle.

## Appendix C. Described Figures

**Figure 1 — Shrink by group across six inventory cycles.** A line chart, horizontal axis running from the November 2022 cycle to the May 2026 cycle, vertical axis from 1.2 to 2.1 percent of sales. Two lines: converted stores (solid) and unconverted stores (dashed). In the two pre-period cycles the lines run parallel at 1.62 and 1.40 percent. A vertical reference band marks the 2023–2024 installation window. From November 2024 forward the dashed line remains flat at 1.40–1.42 while the solid line steps up each cycle — approximately 1.85, 1.90, 1.95, 1.98 — ending 0.53 points above the control group. Error bars on each group-cycle mean span roughly ±0.06 points.

**Figure 2 — Attributable increase by cycle and configuration.** A paired line chart of event-study coefficients, horizontal axis the four post-conversion cycles, vertical axis 0.0 to 0.7 percentage points. The retained-lane line oscillates between 0.15 and 0.21 with overlapping confidence intervals across all four cycles. The removed-lane line rises monotonically — 0.31, 0.42, 0.53, 0.61 — with its confidence interval separating from the retained-lane line by the second cycle. A horizontal reference line at zero anchors the placebo pre-period coefficient of 0.01.

**Figure 3 — Category contributions to the attributable increase.** A horizontal bar chart with six category bars, each bar's length equal to the category's contribution (sales weight × category-level change) to the pooled 0.31-point estimate. Health and beauty (≈0.09 points) and fresh meat (≈0.13 points) dominate; produce, all-other, dairy-frozen, and center-store grocery together contribute the remaining ≈0.09 points, with center-store grocery visually near zero. An annotation notes that the two leading bars represent 18 percent of sales.

**Figure 4 — Scan-data mechanism indicators, March 2025 to May 2026.** A two-panel monthly chart. Left panel: weight-security alerts per thousand self-checkout transactions, removed-lane stores (≈14, stable) versus retained-lane stores (≈9.5, stable). Right panel: share of random-weight meat transactions at self-checkout with weight-code mismatches, plotted against the same measure at staffed lanes; the self-checkout line runs at 2.2–2.5 percent, the staffed-lane line below 0.5 percent, with no seasonal pattern in either.

## Appendix D. Glossary and Data Definitions

**Shrink.** Book inventory less counted physical inventory for a half-year cycle, valued at retail and expressed as a percentage of the cycle's sales. Includes external and internal theft, unrecorded spoilage and markdowns, receiving discrepancies, and bookkeeping error; the physical count cannot distinguish among these.

**Store-half-year.** One store's shrink observation for one inventory cycle. The post-conversion panel comprises 61 stores × 4 cycles = 244 designed observations, of which 243 are usable after exclusion of the voided count.

**Converted store.** A store operating a self-checkout bank of four to eight stations installed between Q3 2023 and Q3 2024. All 24 conversions were complete before the November 2024 count, so every post-period observation for a converted store is fully post-treatment.

**Lane configuration.** "Removed" denotes the eleven stores that eliminated all staffed express lanes at conversion; "retained" denotes the thirteen that kept at least one. Configuration has been stable since conversion at all 24 stores.

**Attributable increase.** The difference-in-differences estimate: the change in a treated group's shrink net of the contemporaneous change at unconverted stores. Distinguished throughout from the raw cross-sectional gap, which embeds pre-existing differences arising from the volume-based selection of conversion stores.

**Weight-security alert.** A self-checkout event log entry generated when the bagging-scale weight change does not correspond to the last scanned item, including item-not-scanned and unexpected-item events. Used as a proxy for non-scanning; most individual alerts are innocent, so only rates and between-group comparisons are interpreted.

**PLU mismatch.** A random-weight transaction in which the recorded scale weight is inconsistent with the plausible weight range of the price-lookup code entered. Computed only for departments with catalogued weight ranges (meat, produce).

---

*Questions on the analysis should be directed to Nadia Farrukhzad, Retail Analytics, Cranberry Township. Model code, the store-cycle panel, and the scan-data extract specifications are archived under project reference RA-2026-014 and will be refreshed after the November 2026 inventory cycle for the first post-decision review.*
