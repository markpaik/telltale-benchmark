# Ledgerline Systems — Research Brief

**Title:** First-Quarter 2026 Churn at Ledgerline Systems: Attribution Across Repricing, Portal Migration, and Support Degradation, and Implications for the Deferred Per-Document Conversion

**Prepared by:** Ji-Won Paek, Revenue Operations Analyst
**Commissioned by:** Samuel Oyelaran, Chief Revenue Officer
**For:** Diane Abernathy-Pruitt, Chief Executive Officer
**Exit interview program:** Beatriz Salgado, Vice President of Customer Success
**Date:** August 9, 2026

---

## 1. The Question and What Was Found

In January 2026, Ledgerline Systems converted 39 percent of its 2,140 accounts from per-seat licensing to per-document pricing at renewal, with the remaining 61 percent scheduled to convert on July 1. Gross churn in the first quarter came in at 9.7 percent annualized, against 5.2 percent in the same quarter a year earlier. The chief executive asked a direct question: what caused the increase, and should the July conversions proceed as planned? On June 12, the July conversion was placed on hold pending this analysis; the currently proposed conversion window is October 1. This brief answers the causal question to the extent the records permit and lays out what bears on the rescheduled decision.

The short answer is that the churn increase is real but is not, in the main, a repricing story — or at least not the repricing story the headline number suggests. Four findings support that conclusion.

First, roughly a third of the churned revenue was not a pricing decision at all. Two of the largest departures, together representing $310,000 of the $994,000 in annual recurring revenue lost during the quarter, were documented acquisitions of the customer by third parties. Excluding those two accounts, gross revenue churn was 6.7 percent annualized — elevated against the 5.2 percent baseline, but far less alarming than 9.7 percent.

Second, the January renewal cohort — the accounts that were actually repriced — churned at close to the prior year's rate in aggregate. Of 813 accounts renewing in January, 2.3 percent did not renew, against 2.7 percent in January 2025. The churn spike is concentrated in February and March, among accounts that renewed on unchanged per-seat terms: 10.5 percent of February renewals and 9.4 percent of March renewals did not renew, three to four times the prior year's rates. Those months coincide exactly with the collapse of support responsiveness, when median first response time rose from 4 hours to 19 hours after 5 of 18 support staff resigned.

Third, within the repriced cohort, the sequence of the two overlapping change programs mattered substantially. Accounts that had completed migration to the rebuilt web portal before they were repriced churned at 5.8 percent annualized — near baseline. Accounts repriced while still on the legacy portal churned at 11.9 percent. The gap persists, though it narrows, when comparing accounts of similar size, which suggests it is not purely a composition effect.

Fourth, the pain is concentrated in the long tail of small accounts. Accounts under $12,000 in annual contract value churned at 14.2 percent annualized; accounts above $50,000 churned at 4.1 percent. Small accounts absorbed the largest effective price increases under the per-document rate card, received the slowest support during the backlog, and were disproportionately unmigrated at the time of repricing.

The implication for the deferred conversion is not to cancel it, and not to proceed on the original all-at-once design, but to change its preconditions and sequencing: restore support capacity to a defined service level before any conversion; require portal migration to precede repricing by a defined interval; and protect or deliberately triage the sub-$12,000 tier, where the effective price increases and the churn are concentrated. Preliminary second-quarter data, discussed briefly in Section 4.7, is consistent with this reading: as first response times recovered through the spring, monthly non-renewal rates fell back toward baseline without any change to pricing.

---

## 2. Data and Methods

### 2.1 Billing and contract records

The primary quantitative source is the billing ledger and contract system of record, covering all 2,140 active accounts as of January 1, 2026: contract start and renewal dates, annual contract value, pricing model (per-seat or per-document), invoice history, conversion date where applicable, and termination records. These records establish the denominator and the churn events with high confidence — an account either renewed, did not renew, or terminated mid-contract, and the associated revenue is unambiguous.

What the billing records cannot show is why. They record the outcome of a decision, not its inputs. They also cannot show usage, product engagement, or the customer's experience of either the migration or the support queue. A further structural limitation is worth stating plainly: because 38 percent of the book renews in January, the billing data delivers most of its annual churn signal in a single month, and annualizing a first quarter dominated by that cluster produces rates that are sensitive to the composition of one cohort. This brief therefore reports renewal-event rates by month alongside annualized figures, and flags throughout which basis is in use.

### 2.2 Customer relationship records and exit interviews

The customer relationship system contributes account ownership, customer success manager notes, health scores, escalation records, and — for churned accounts — the exit interview program run by Beatriz Salgado's team. Of the 54 accounts that churned in the first quarter, 41 completed a structured exit interview (a 76 percent completion rate); 13 declined or could not be reached, and non-respondents skew toward the smallest accounts.

The exit interviews are the only source that speaks directly to motive, and they carry the standard caveats. Stated reasons for leaving are retrospective rationalizations gathered by the vendor being left; price is a socially easy answer that can stand in for accumulated dissatisfaction; and the interviews were conducted by the customer success organization whose service levels are one of the candidate causes. The two acquisition-driven departures were identified through these records and corroborated by public announcements. Health scores in the CRM proved to have little predictive value in this period — 61 percent of churned accounts were rated "green" or "yellow" within 60 days of departure — largely because the scores are updated manually and were stale during the migration push.

### 2.3 Support records

The support platform provides ticket volume, first response time, resolution time, ticket categorization, and open-backlog counts, joined to accounts by domain. Staffing levels come from the HR roster: the support team stood at 18 at the start of January and 13 by February 6, after five resignations between January 12 and February 6. Support records show the customer's experience of the queue precisely, but they cannot show the experience of customers who stopped submitting tickets — silence in the support data is ambiguous between satisfaction and disengagement.

### 2.4 Product telemetry and what it cannot show

Product telemetry exists only for the rebuilt portal, which went live on September 22, 2025. The legacy portal was never instrumented beyond authentication logs, which were purged on a 90-day cycle and are unrecoverable for the relevant period. By March 31, 1,062 accounts (49.6 percent of the book) had migrated and were generating telemetry; the remaining 1,078 accounts were entirely unobserved from a usage standpoint.

The consequence for this analysis is severe and asymmetric. For migrated accounts, we can observe activation depth, document throughput, and login cadence in the weeks preceding a renewal decision. For unmigrated accounts — which include the entire "repriced-first" cohort at the moment of their renewal decision — we cannot observe usage at all. This means we cannot distinguish between two rival explanations for the elevated churn among repriced-first accounts: that the repricing pushed out otherwise healthy customers, or that these accounts were already disengaged and the renewal-plus-repricing event merely surfaced a departure that was coming anyway. Pre-migration usage cannot be reconstructed for anyone, so no before-and-after usage comparison is possible for any account, migrated or not. The telemetry is also left-truncated in a way that guarantees survivorship bias: accounts that churned before migrating never appear in it.

### 2.5 Cohort definitions and analytic approach

The analysis is descriptive. Churn is measured two ways: gross revenue churn (annualized annual recurring revenue lost as a share of the January 1 base — the basis for the 9.7 percent headline) and logo churn (accounts lost as a share of accounts). The two diverge meaningfully this quarter and the divergence is itself a finding.

Accounts are segmented three ways. By size: under $12,000 ACV (1,014 accounts, $7.1 million ARR), $12,000 to $50,000 (836 accounts, $18.4 million), and above $50,000 (290 accounts, $15.5 million). By sequence: among the accounts converted to per-document pricing in the quarter, "migrated-first" (portal migration completed before the renewal date) versus "repriced-first" (converted while still on the legacy portal or mid-migration). By renewal month: January, February, March, plus mid-contract terminations. Of the 835 accounts slated for January conversion, 816 were converted (345 migrated-first, 471 repriced-first) and 19 negotiated deferrals. February and March renewals — 171 and 128 accounts respectively — renewed on unchanged per-seat terms with conversion deferred to the July batch, which makes them an imperfect but useful comparison group: exposed to the migration program, the support degradation, and the announcement of future repricing, but not to a price change at their renewal.

To estimate the effective price impact of the conversion, fourth-quarter 2025 document volumes (available only for migrated accounts, plus invoice-derived estimates for a subset of others) were re-rated under the per-document card and compared to the per-seat price actually paid. No causal identification strategy is available: the repricing, the migration, and the support collapse overlapped in time, none was assigned randomly, and the analysis can bound and order the candidate explanations but cannot cleanly separate them.

---

## 3. Background on the Two Change Programs

Two programs ran concurrently through the winter. The pricing conversion replaced per-seat licensing with a per-document rate card carrying volume-tiered discounts; it was announced to all customers in November 2025 and applied to January renewals. The portal migration moved accounts from the legacy web application to the rebuilt portal in scheduled waves beginning October 2025, sequenced primarily by ERP connector type — accounts on standard connectors (disproportionately larger, more sophisticated customers) migrated first. Migration throughput ran at roughly 160 to 180 accounts per month and generated substantial support volume: migration-related tickets were 44 percent of February's inbound queue. The two programs were planned independently and their interaction — an account receiving a new price, a new interface, and a slow support queue in the same sixty days — was not modeled in advance.

---

## 4. Results

### 4.1 Decomposing the headline

The first quarter saw 54 accounts churn, carrying $994,000 in annual recurring revenue — 9.7 percent of the base, annualized, against 5.2 percent a year earlier. Logo churn was 10.1 percent annualized against roughly 5.0 percent.

Two of the largest departures were acquisitions, not decisions about Ledgerline: a $186,000 account acquired by a strategic buyer that consolidated onto the acquirer's AP platform, and a $124,000 account absorbed into a private-equity rollup with a competing incumbent system. Together they account for $310,000 — 31 percent of churned revenue in the quarter — and neither exit interview nor CSM record suggests price or service played any role. Excluding them, gross revenue churn was 6.7 percent annualized. The controllable revenue problem is therefore an increase of roughly one and a half points over baseline, not four and a half. The logo problem is larger: excluding the acquisitions, 52 accounts still left, nearly double the prior year's count, and they are overwhelmingly small.

### 4.2 Churn by account size

| Segment (ACV) | Accounts | ARR | Q1 churned accounts | Annualized logo churn |
|---|---|---|---|---|
| Under $12,000 | 1,014 | $7.1M | 36 | 14.2% |
| $12,000–$50,000 | 836 | $18.4M | 15 | 7.2% |
| Over $50,000 | 290 | $15.5M | 3 | 4.1% |
| **Total** | **2,140** | **$41.0M** | **54** | **10.1%** |

The gradient is steep and monotonic. The sub-$12,000 tier — 47 percent of logos but 17 percent of revenue — supplied two-thirds of churned accounts while contributing $252,000, about a quarter of churned revenue. The over-$50,000 tier lost only three logos, but because two were the acquisitions, its revenue churn (10.6 percent annualized) exceeds its logo churn several times over — a reminder that revenue and logo measures answer different questions and should be reported separately in board materials.

The size gradient has a mechanical component. Re-rating fourth-quarter document volumes under the per-document card, the median modeled price change was +9 percent for accounts under $12,000 (interquartile range −2 to +21 percent), +1 percent for the middle tier, and −3 percent for accounts above $50,000, whose volumes reach the deeper discount tiers. Twenty-two percent of small accounts faced modeled increases above 25 percent. Among the small accounts that were repriced and churned, the median modeled increase was +19 percent. The rate card, as constructed, functions as a targeted price increase on the long tail.

### 4.3 Churn by sequence of migration and repricing

Among the 816 accounts converted in the quarter, sequence was strongly associated with the outcome. The 345 migrated-first accounts — those already working in the new portal when their renewal and repricing arrived — churned at 5.8 percent annualized (5 accounts), essentially baseline. The 471 repriced-first accounts, still on the legacy portal at their renewal, churned at 11.9 percent (14 accounts), roughly double.

Sequence was not randomly assigned. Migration waves were ordered by ERP connector type, and migrated-first accounts skew larger (median ACV approximately $24,000 versus $13,000) and more operationally sophisticated. Some of the gap is therefore composition. But within the sub-$12,000 band, where composition is most homogeneous, the gap persists at roughly 8 percent for migrated-first versus 15 percent for repriced-first — narrower, but still nearly two to one. Two mechanisms are plausible and the data cannot separate them: a genuine sequencing effect, in which customers who have already absorbed the platform change and can see current product value tolerate a pricing change better; and a selection effect the telemetry gap makes untestable, in which accounts that engaged early with migration were healthier to begin with. Described as a figure, the pattern is a two-bar chart with a confidence band: the migrated-first bar sitting on the prior-year baseline, the repriced-first bar at more than double it, with the within-small-segment comparison inset showing the same ordering at higher levels.

### 4.4 Churn by renewal month

| Renewal month | Accounts renewing | Non-renewals | Event rate, 2026 | Event rate, 2025 |
|---|---|---|---|---|
| January (repriced) | 813 | 19 | 2.3% | 2.7% |
| February (per-seat) | 171 | 18 | 10.5% | 2.9% |
| March (per-seat) | 128 | 12 | 9.4% | 2.4% |
| Mid-contract terminations | — | 5 | — | (2 in 2025) |

This table carries the central finding of the brief. The repriced January cohort, in aggregate, churned at slightly below its prior-year rate. The February and March cohorts — which received no price change at renewal — churned at three to four times theirs. Because January holds 38 percent of the book, its near-baseline performance dilutes the February–March deterioration in the blended figure; the annualized 9.7 percent headline is arithmetically dominated by a large calm cohort and a small distressed one, and misstates both.

Described as a figure: a two-line monthly chart, 2025 versus 2026 renewal-event churn, with the lines nearly overlapping in January and diverging sharply in February and March; a second panel below plots median support first response time by month, whose February peak aligns visually with the divergence.

Three explanations for the February–March deterioration are available and cannot be fully separated. The support collapse (Section 4.5) is the most proximate and best-evidenced. Migration friction is second: migration-related tickets flooded the queue in exactly this window. Third is an announcement effect — February and March renewers signed twelve-month agreements knowing the July conversion awaited them mid-term, and eight exit interviews from these months reference the coming price model unprompted. On this reading, some of the "non-pricing" churn is anticipatory pricing churn, which would shift attribution back toward the conversion program. The data cannot rule this out; it can only note that the timing of the deterioration tracks the support metrics more tightly than it tracks the pricing announcement, which was made in November with no comparable January effect.

### 4.5 The support backlog

Five of eighteen support staff resigned between January 12 and February 6 — exit paperwork cites compensation and the migration workload. Median first response time moved from 4 hours in December to 9 hours in January, 19 hours in February, and 16 hours in March. The open-ticket backlog grew from roughly 140 to 610. Because triage prioritized by account value during the crisis, the degradation was regressive: small accounts experienced the worst of it, compounding the price increases already concentrated on them.

The join between support and churn records is the strongest single association in the dataset: of the 30 February and March non-renewals, 23 had at least one ticket open ten days or longer at the time the renewal decision was due. Among February–March accounts that renewed, the comparable figure is under one in five. Eleven of 41 exit interviews named support responsiveness as the primary reason for leaving, the second most cited reason overall and the most cited among February–March departures. The usual caution applies — struggling accounts generate tickets, so open tickets partly mark rather than cause distress — but the timing, the dose-response pattern in first response times, and the interview testimony point the same direction.

### 4.6 Exit interview evidence

Primary stated reasons among the 41 completed interviews: price or price-to-value, 14; support responsiveness, 11; portal migration friction, 7; acquisition or corporate consolidation, 4 (including the two large departures); switched to an ERP-native AP module, 3; other, 2. Price leads, as it nearly always does in exit data, but the 14 price citations skew heavily toward repriced-first small accounts with large modeled increases — the interviews and the billing re-rating identify the same pocket of the book. Notably, several interviews describe the conjunction rather than any single cause: a new invoice, an unfamiliar portal, and a ticket that sat for two weeks, arriving within the same billing cycle.

### 4.7 Preliminary corroboration from the second quarter

Though outside the formal scope, the spring is a natural test of the support hypothesis. Four support hires started between March and May; median first response time recovered to 7 hours by June. April, May, and June renewals — roughly 300 accounts, all still per-seat — showed monthly non-renewal event rates of 8.1, 5.5, and 3.4 percent respectively, declining in step with the recovery, with no pricing change in the period. Second-quarter gross churn ran at approximately 6.8 percent annualized. This pattern is consistent with support degradation as the dominant proximate driver of the spring churn and is difficult to reconcile with a story in which the pricing announcement alone drove it.

---

## 5. Limitations

The limitations are material and several bear directly on how much weight the findings can carry.

**No causal identification.** Repricing, portal migration, the support collapse, and the November pricing announcement overlapped in a single winter. Nothing was randomized, and the natural comparison groups differ systematically. The February–March cohort is the closest thing to a pricing control group, but it was exposed to the announcement effect and disproportionately exposed to the support collapse, so it controls for the price change while confounding everything else.

**The telemetry gap.** Usage before migration is unobservable for every account, and usage at decision time is unobservable for every repriced-first account. The central rival to the sequencing finding — that repriced-first accounts were already disengaged — is therefore untestable with existing data, permanently, for this cohort.

**Annualization from a clustered quarter.** With 38 percent of renewals in January, annualized quarterly rates are dominated by one cohort and are unstable for the others; February and March event rates rest on 171 and 128 renewals respectively, so their percentages carry wide uncertainty. Cohort rates in this brief are computed on differing bases (annualized cohort rates and renewal-event rates), which are not directly interchangeable; a unified event-history analysis on account-level data is the correct next step and is recommended below.

**Exit interview coverage and bias.** Thirteen of 54 churned accounts were not interviewed, skewing small; stated reasons are retrospective and gathered by the departing vendor's own success organization; price is an easy answer. The acquisition classification depends on CSM documentation, and smaller churned accounts may include unrecorded consolidation events, which would push the adjusted churn figure lower still.

**Modeled price changes are estimates.** Re-rated document volumes exist only where telemetry or invoice detail permits; for unmigrated accounts, volumes were estimated from invoice line items and are least reliable precisely for the small, unmigrated accounts where the estimated increases are largest.

---

## 6. Implications for the Deferred Conversion Decision

The July 1 conversion, now proposed for October 1, would convert the remaining 1,324 accounts — roughly $25.4 million of ARR — many of them mid-contract rather than at renewal. The first-quarter evidence supports proceeding, but not on the original design. Five conditions follow from the findings.

**First, restore and verify support capacity before converting anyone.** The support collapse is the best-evidenced driver of the spring churn, and it interacted with every other stressor. Conversion should be gated on a sustained service level — median first response under 8 hours and backlog under 200 for six consecutive weeks — with staffing headroom for the ticket surge that conversion itself will generate.

**Second, sequence migration before repricing, contractually and operationally.** The 5.8-versus-11.9 gap, even discounted for selection, is the strongest lever the data offers. Roughly 810 of the not-yet-converted accounts remain unmigrated; at current throughput of 160–180 migrations per month, migration cannot complete before October. The conversion should therefore be staggered — accounts convert only after 60 days of verified activity on the new portal — which implies a rolling conversion through the fourth quarter and into early 2027 rather than a single date. The single-date design should be abandoned.

**Third, decide deliberately about the long tail.** The sub-$12,000 tier will absorb median modeled increases near 9 percent, with a fifth of accounts above 25 percent, while receiving the thinnest support. Options include a first-year increase collar of 10 percent, a flat small-account tier, or an explicit decision to accept elevated logo churn there as rationalization of a low-margin segment. Any of these is defensible; losing 14 percent of the tier by accident is not.

**Fourth, fix measurement before the next intervention.** Mid-contract conversion removes the renewal event as a natural observation point, so churn from the October program will dribble out across twelve months of scattered renewal dates and be harder to attribute than the January cohort was. Before conversion: instrument decision-time leading indicators (ticket age at renewal, migration status, modeled price delta), pre-register cohort definitions, and build the unified account-level event-history dataset this brief lacked.

**Fifth, report churn honestly.** Headline gross churn should be presented alongside an ex-acquisition figure and separate logo and revenue measures. The 9.7 percent number triggered this inquiry; the 6.7 percent controllable figure, the near-baseline January cohort, and the February support signature are what the decision should actually rest on.

The first quarter did not demonstrate that per-document pricing fails. It demonstrated that a price change, a platform change, and a service failure delivered simultaneously to the smallest customers is a churn machine — and that each element, separated and sequenced, appears survivable.

**Sixth, treat the October program as an experiment, not a rollout.** Because the remaining conversions will be staggered by migration completion, the schedule itself creates the comparison structure the first quarter lacked. Conversion waves should be balanced on size, region, and connector type where the migration queue permits, and a small holdout — on the order of 100 accounts, drawn proportionally across segments and converted last, in the first quarter of 2027 — should be preserved deliberately. The holdout costs roughly one quarter of per-document uplift on approximately $1.9 million of ARR, an estimated $40,000 to $60,000 of deferred revenue, and buys the first clean read this company will have had on what its pricing model does to retention. That trade is worth making.

---

## 7. Monitoring Plan and Tripwires for the Rescheduled Conversion

If the October program proceeds under the conditions above, it should carry pre-committed stopping rules rather than rely on quarter-end review. The first quarter's lesson on measurement is that a renewal-clustered book delivers its churn signal in bursts and the annualized headline lags the underlying deterioration by months; a mid-contract conversion program will invert that problem, spreading the signal thinly across the year. The monitoring plan compensates by tracking leading indicators weekly and outcome indicators monthly, with thresholds agreed in advance by the chief revenue officer and chief executive.

**Leading indicators, reviewed weekly.** (1) Median support first response time and open-backlog count, overall and for the sub-$12,000 tier separately; conversion waves pause automatically if median first response exceeds 8 hours for two consecutive weeks or backlog exceeds 250. (2) Migration throughput against the 60-day-precedence requirement; any wave in which more than 5 percent of accounts reach their conversion date unmigrated is deferred, not exempted. (3) Save-desk volume and concession rate on conversion-related escalations, which in the first quarter proved a faster-moving signal than non-renewal notices by roughly five weeks.

**Outcome indicators, reviewed monthly.** (1) Non-renewal event rates by wave and by size band, compared against the same account's prior-year renewal behavior where available and against the holdout once it accrues renewals. (2) Mid-contract termination and non-payment counts, which under mid-term conversion become a churn channel in their own right; the first quarter's five mid-contract terminations against two the prior year is a small-number signal but should be watched, since the October design will shift more of the churn expression into this channel. (3) Effective invoice change realized versus modeled, by band; if realized increases in the small tier exceed the modeled +9 percent median by more than five points, the rate card's volume assumptions are wrong and the collar should bind before the customer sees the invoice, not after.

**Tripwires.** Two conditions should halt the program pending review by this office: annualized gross churn ex-acquisitions above 8 percent measured on a trailing three-month basis, or a sub-$12,000 logo churn rate above 12 percent annualized in any converted wave. Neither threshold is derived from a statistical model; both are set at roughly the midpoint between baseline and the first quarter's observed distress levels, on the reasoning that a program halted at the midpoint can be repaired, while one reviewed only after matching the first quarter cannot.

---

## Appendix A. Described Figures

**Figure 1 (described).** *Monthly renewal-event churn, 2025 versus 2026, with support first response time.* Upper panel: two lines across January–June, prior year and current year, plotting the share of each month's renewing accounts that did not renew. The lines sit within half a point of each other in January (2.7 versus 2.3 percent), diverge sharply in February (2.9 versus 10.5 percent) and March (2.4 versus 9.4 percent), and reconverge through the second quarter (April 8.1, May 5.5, June 3.4 percent against a prior-year band of 2.3–3.0). Lower panel, shared x-axis: median first response time by month — 4, 9, 19, 16, 11, 7 hours from December through June — whose rise and fall visibly brackets the divergence above. The visual argument of the brief is contained in the alignment of these two panels.

**Figure 2 (described).** *Churn by sequence of migration and repricing.* Two bars: migrated-first at 5.8 percent annualized and repriced-first at 11.9 percent, each with an interval reflecting cohort size (345 and 471 accounts), against a dashed horizontal baseline at 5.2 percent. An inset repeats the comparison restricted to sub-$12,000 accounts, at approximately 8 and 15 percent, demonstrating persistence of the ordering within the size band.

**Figure 3 (described).** *Composition of churned revenue.* A single stacked bar decomposing the $994,000 of churned ARR: $310,000 acquisitions (two accounts), $252,000 sub-$12,000 tier (36 accounts), $330,000 middle tier (15 accounts), $102,000 remaining large-tier account. A companion bar decomposes churned logos, showing the inversion: the segment contributing the most revenue loss per the left bar contributes the fewest logos, and vice versa.

**Figure 4 (described).** *Modeled invoice change under per-document pricing, by segment.* Three box plots showing the distribution of re-rated price changes: sub-$12,000 median +9 percent with an upper quartile at +21 and a visible right tail beyond +25 covering 22 percent of the segment; middle tier centered near +1; large tier centered near −3. Churned repriced small accounts are overplotted as individual points, clustering in the right tail with a median of +19 percent.

---

## Appendix B. Supplementary Table — First-Quarter Churn Ledger

| Category | Accounts | Churned ARR | Share of churned ARR |
|---|---|---|---|
| Acquisitions (large tier) | 2 | $310,000 | 31.2% |
| Other large tier | 1 | $102,000 | 10.3% |
| Middle tier ($12k–$50k) | 15 | $330,000 | 33.2% |
| Small tier (under $12k) | 36 | $252,000 | 25.4% |
| **Total** | **54** | **$994,000** | **100%** |

Of the 54: 19 were January renewals (18 converted, 1 deferral), 18 were February renewals (17 per-seat, 1 converted co-terminating account), 12 were March per-seat renewals, and 5 were mid-contract terminations. Gross revenue churn annualized: 9.7 percent; excluding acquisitions: 6.7 percent; logo churn annualized: 10.1 percent.

---

## Appendix C. Cohort Construction Notes

Conversion status was taken from the contract amendment records, not the invoice date, because invoicing lagged amendment by up to three weeks in January. Migration status was defined as first successful production login by any user of the account on the rebuilt portal, per telemetry, occurring before the account's renewal date; accounts mid-migration (provisioned but never logged in) were classified as repriced-first, affecting 38 accounts, and reclassifying them does not change the ordering of the sequence result. The 19 deferral accounts negotiated per-seat renewals with a contractual conversion date matching the July (now October) batch and are counted in neither sequence cohort. Renewal month was assigned by contractual renewal date, not by the date the renewal was executed; eleven January renewals executed in early February are counted as January. Prior-year comparison rates were computed on the year-earlier book of 2,048 accounts using identical definitions.

---

## Appendix D. Exit Interview Method

Interviews were conducted by two customer success team leads using a structured instrument of eleven questions, within 45 days of the termination effective date, by video call (29) or phone (12). Primary reason was coded by the interviewer from a closed list with a free-text supplement, and 15 interviews were double-coded by Salgado for reliability, with agreement on 13 of 15 primary codes. Interviewees were offered no incentive. The 13 non-respondents comprise 10 sub-$12,000 accounts, 2 middle-tier accounts, and 1 of the two acquired accounts (classified from public announcement and CSM record rather than interview). Full transcripts are retained in the CRM under restricted access; quoted material in Section 4.6 is paraphrased to preserve anonymity.

---

## Appendix E. Data Lineage and Reproducibility

All figures in this brief derive from four extracts pulled between July 21 and August 4, 2026: the billing ledger as of the July 31 close, the CRM account and interview objects as of August 1, the support platform's ticket warehouse as of August 1, and the telemetry warehouse as of August 4. Extraction queries, the cohort assignment script, and the re-rating model are stored in the revenue operations repository under `churn-brief-2026q1`, tagged `v1.3`. The re-rating model's volume estimates for unmigrated accounts carry a documented ±15 percent error band derived from back-testing against the 214 accounts for which both invoice-derived and telemetry-observed volumes exist. Second-quarter figures cited in Section 4.7 are preliminary and will be restated at the August close; no restatement to date has moved a monthly event rate by more than 0.4 points.

---

*Prepared by Ji-Won Paek, Revenue Operations. Questions on method or data lineage to revenue operations; questions on the exit interview program to Beatriz Salgado. Distribution: D. Abernathy-Pruitt, S. Oyelaran, B. Salgado, CFO, VP Product. This brief supersedes the interim memorandum of June 12, 2026.*
