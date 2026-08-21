# Q1 2026 Churn Investigation: Disentangling Repricing and Portal Migration Ahead of the July Conversion

**Prepared by:** Ji-Won Paek, Revenue Operations Analyst
**Commissioned by:** Samuel Oyelaran, Chief Revenue Officer
**Exit interview data supplied by:** Beatriz Salgado, VP, Customer Success
**Prepared for:** Diane Abernathy-Pruitt, Chief Executive Officer
**Date:** July 30, 2026

---

## The Question and What We Found

In January 2026, Ledgerline moved 39 percent of its 2,140 accounts from per-seat to per-document pricing at renewal, with the remaining 61 percent scheduled to convert in July. Over the same window, the company was migrating customers from a legacy web portal to a rebuilt one, a project that had begun independently of the pricing change. First-quarter gross churn came in at 9.7 percent annualized, against 5.2 percent in the same quarter a year earlier. Ms. Abernathy-Pruitt asked Revenue Operations to determine what caused the increase before the July conversions proceed.

The honest answer is that we cannot fully separate the two changes from the billing and customer relationship data we have, and we cannot separate either of them from a support staffing collapse that happened to land in the same quarter. What we can say with reasonable confidence is this:

First, the churn increase is not evenly distributed. It is heavily concentrated in small accounts, in accounts that were repriced before they were migrated to the new portal, and in the January renewal cohort, which represents 38 percent of the book by count. Second, a support response time spike, from a 4-hour to a 19-hour median first response, followed the resignation of 5 of 18 support staff in early February and overlaps almost exactly with the highest-churn segment of the quarter. Third, two of the largest-value account departures were coded in exit interviews as driven by acquisition of the customer's business, not by pricing or product decisions, and should be discounted from a pricing narrative even though they inflate the headline number. Fourth, and most consequential for the July decision: product telemetry exists only for the new portal, which went live in September 2025, so we have no usage data at all for the period before an account migrated. We cannot show what changed in customer behavior at the moment of migration because we have no "before" to compare to. Every claim in this brief about the relationship between migration and churn rests on billing outcomes and exit-interview coding, not on observed usage.

The clearest, most actionable finding is the sequence effect: accounts migrated to the new portal before being repriced churned at 5.8 percent, while accounts repriced before migration churned at 11.9 percent. That gap is large enough, and consistent enough with an ordinary account-experience explanation, that it should shape how the July cohort is sequenced, independent of what we ultimately conclude about the pricing model itself.

---

## Data and Methods

Three systems of record inform this brief, and each has a different unit of observation, a different time horizon, and a different set of blind spots. None of the three was built to answer the question the CEO is asking, and the analysis below should be read with that limitation in mind throughout, not just in the section formally labeled "Limitations."

### Billing and Contract Records

The billing system is the most complete and most reliable source. It records, for all 2,140 accounts, the pricing model in effect (per-seat or per-document), annual contract value, renewal date, tenure, industry vertical, and a binary churn flag with a churn date where applicable. This is the backbone of every cut in this brief: account size, renewal month, and pricing-model status are all billing-system fields, and we trust them.

What the billing system cannot show is intent or mechanism. It tells us that an account churned and what its contract terms were at the time, but nothing about why a given customer decided to leave, and nothing about how they used the product before they left. A repriced account that churned might have churned because of the price, because of the portal, because of a support delay, because a champion left the customer's finance team, or because the customer's own business was acquired. The billing record is silent on all of that. It is also silent on accounts that have not yet renewed; for the 61 percent of the book still on per-seat terms, we have no way to observe how they will respond to repricing until July, which is precisely why this brief exists.

### Customer Relationship Records

Ms. Salgado's team supplied exit interview notes and reason codes for churned accounts, along with support ticket volume, first-response and resolution times, and account manager engagement logs. Coverage is incomplete: exit interviews were conducted for 71 percent of churned accounts in the quarter, not all 209. Reason coding is done by the account manager or customer success representative who conducted the interview, using a fixed set of categories (price, product/portal, support, competitor, acquisition/business change, other) with free-text notes. This is a judgment call made by an employee who may have an interest in a particular attribution, and it is made after the fact, based on what the customer said in a single conversation, which is not the same as an independently verified cause.

The most useful thing this data source gave us is the acquisition flag: two of the largest-ACV departures in the quarter were coded as the customer's business being acquired by another firm, with the surviving entity consolidating onto its own systems, rather than as a reaction to Ledgerline's pricing or product changes. We treat these as exogenous to the repricing and migration story, though we note that "coded as acquisition" is not the same as "verified as unrelated to price"; a customer facing an unwelcome price increase in the middle of an acquisition process may not volunteer pricing as a factor even if it contributed to a lack of resistance to being folded into the acquirer's stack. We flag this rather than resolve it.

The CRM records also gave us the support-response-time series, which is unambiguous and internally generated: median first response time was 4 hours through January and rose to 19 hours in February, coincident with the departure of 5 of the company's 18 support staff. This is a real, well-measured degradation in service, but the CRM data cannot tell us how many churned accounts actually experienced the slow response before they decided to leave, only that the two events occurred in the same quarter for the customer base as a whole.

### Product Telemetry

This is the source with the sharpest limitation. Telemetry, meaning logged-in usage, feature adoption, document volume processed, and session frequency, exists only for the rebuilt portal, which launched in September 2025. For any account, we have usage data starting from the date that account was migrated onto the new portal, and nothing before that date. There is no legacy-portal telemetry to draw on; it was either never instrumented at the same level or was not retained, and either way it is not available to us now.

This means we cannot answer a question that seems, on its face, central to the CEO's ask: did usage patterns change when an account moved to the new portal, in a way that predicts churn? We can observe usage after migration, but we have no baseline from before migration for the same account, so we cannot compute a before-and-after difference. We can compare post-migration usage across accounts that behaved differently, but we cannot say whether any account's usage changed as a result of migrating, because we never observed it pre-migration. This is not a sampling gap that more time will fix retroactively; the pre-migration data does not exist and cannot be reconstructed. Any statement in this brief about the portal's effect on churn is therefore based on billing outcomes correlated with migration timing, not on observed behavior change.

### Analytic Approach

Given these constraints, we did not attempt a regression model that would give a false sense of precision about "the effect of price" net of "the effect of the portal." The two changes are confounded at the account level in a way that a churn quarter this size cannot resolve statistically: accounts were not randomly assigned to be repriced before or after migration, renewal timing was set by legacy contract terms rather than by us, and the support staffing shock hit the entire book at once rather than a controlled subset. Instead, we built a set of cross-tabulations, churn by account-size band, churn by the sequence in which an account experienced repricing and migration, and churn by renewal month, and we examined each cut on its own terms, noting where the story is clean and where it is not. We treat this as a diagnostic exercise to inform a near-term operational decision, not as a causal study, and we say so plainly in the results below rather than implying more certainty than the data supports.

---

## Results

### Churn by Account Size

The clearest and least ambiguous pattern in the data is the relationship between account size and churn. Accounts with annual contract value under $12,000 churned at 14.2 percent, annualized, while accounts above $50,000 churned at 4.1 percent, a gap of more than three to one.

| Account Size (ACV) | Q1 2026 Annualized Churn |
|---|---|
| Under $12,000 | 14.2% |
| $12,000–$50,000 | not separately reported, between the two bands |
| Above $50,000 | 4.1% |

This pattern is consistent with several explanations that are not mutually exclusive. Per-document pricing mechanically raises cost most for low-volume, low-seat accounts that were previously paying a flat per-seat fee regardless of document throughput; a small account with light usage under the old model may see a proportionally larger bill increase than a heavy-usage account of similar seat count. Small accounts also tend to receive less account-management attention under Ledgerline's current customer success model, which is weighted toward accounts above roughly $30,000 in ACV, so they may be both more price-sensitive and less cushioned by a relationship that could otherwise absorb the shock or negotiate an accommodation. Finally, small accounts are disproportionately likely to be single-decision-maker purchases where a bill increase triggers an immediate cancellation, compared to larger accounts where a renewal often goes through procurement or budget review on a longer cycle that can absorb a price change without triggering same-quarter churn.

We cannot cleanly attribute the size effect to price alone, because account size also correlates with support ticket volume, tenure, and vertical in ways the exit-interview coding does not disentangle. But this is the sharpest, most reproducible signal in the quarter's data, and it should weigh heavily in how the July conversion is designed, in particular whether some form of graduated increase or continued per-seat option is offered to the smallest tier.

### Churn by Sequence of Migration and Repricing

The second clear pattern concerns order of operations. Among accounts that had already been migrated to the new portal before their renewal converted them to per-document pricing, churn was 5.8 percent. Among accounts that were repriced first and migrated to the new portal afterward, or that remain on the new pricing without having migrated yet, churn was 11.9 percent, roughly double.

| Sequence | Q1 2026 Annualized Churn |
|---|---|
| Migrated to new portal, then repriced | 5.8% |
| Repriced, then migrated (or not yet migrated) | 11.9% |

This is the single most operationally useful finding in the brief, and it deserves more discussion than its two data points might suggest. There are at least three plausible mechanisms, and we want to be direct that we cannot distinguish among them with the data available.

The first is a straightforward change-fatigue explanation: a customer who is asked to absorb a new billing model and a new user interface in close succession experiences the two as a single, larger disruption, and is more likely to treat that combined disruption as a reason to re-evaluate the vendor relationship. An account that had already been through the portal migration, and had presumably stabilized on it, absorbed the pricing change as a single, isolated event rather than as part of a pile-up of change.

The second is a confidence-and-goodwill explanation: an account that experienced the new portal first, and found it to be an improvement, or at least neutral, may have entered its repricing conversation with more goodwill toward Ledgerline and more benefit of the doubt on the price. An account that was repriced first, with no improved product experience yet to point to, may have felt the price increase as pure extraction, unaccompanied by any visible sign that the company was reinvesting in the relationship.

The third is a selection explanation rather than a causal one: since migration to the new portal has been proceeding on its own timeline since September 2025, the accounts that happened to migrate early may differ systematically from accounts that migrated late or have not yet migrated. Early migrators could be more engaged, larger, or more technically capable customers who were prioritized or opted in sooner, and those same traits could independently predict lower churn, regardless of sequencing. We do not have a record of how migration order was determined, so we cannot rule this out.

We want to be explicit that the telemetry limitation described above bears directly on this finding. We can see that accounts migrated-then-repriced churned less, but we have no usage data from before those same accounts migrated, so we cannot say whether their behavior on the legacy portal looked any different from the behavior of accounts that were repriced first. The sequence effect is real in the billing outcomes; its mechanism is not something we can currently observe.

### Churn by Renewal Month

Thirty-eight percent of the book renews in January, which means that any event affecting January renewals disproportionately affects the annualized churn figure for the quarter as a whole. The January repricing wave and the January renewal cluster are the same accounts by construction, since repricing at Ledgerline takes effect at renewal. This is worth stating plainly: the 39 percent of accounts moved to per-document pricing in Q1 are, almost entirely, the accounts whose contracts happened to renew in the first quarter, which is also the heaviest single month of the year for renewals generally. The elevated churn in Q1 is therefore mechanically concentrated in the same window as the pricing change simply because that is when the pricing change was applied, not necessarily because January renewals are more price-sensitive than renewals in other months on some independent basis. We do not have comparable per-month churn data from outside the repricing cohort this quarter to test that separately, since nearly all Q1 renewals were, by design, part of the repricing wave.

The renewal concentration matters most for what it implies about July: if 38 percent of the book renews in January and a comparable or different share renews around July, the July conversion is likely to produce its own concentrated wave, and any support, account-management, or sequencing response should be planned for volume, not treated as evenly spread across the year.

### The Support Backlog

Median first support response time rose from 4 hours to 19 hours in February, following the resignation of 5 of the company's 18 support staff, more than a quarter of the team. This is a severe and abrupt service-level degradation by any standard, and it lands squarely inside the quarter under review. We do not have a clean way to quantify how many churned accounts personally experienced a slow response before leaving, because ticket-level linkage to the churn cohort was not part of the exit-interview process and would require a separate reconstruction from raw ticket logs, which we recommend as a follow-up.

What we can say is that the timing overlap is close enough, and the response-time degradation severe enough, that it is not safe to treat the Q1 churn increase as attributable to pricing and migration alone. A customer newly moved to a more expensive pricing model, on an unfamiliar portal, who then submits a support question and waits most of a business day for a first response, is experiencing three compounding sources of dissatisfaction at once, and the exit interview may reasonably record "price" as the stated reason even where a faster support response might have preserved the account despite the price increase. We treat the support collapse as a real, independent contributor to churn risk in the quarter, and one that is fully within the company's control to remedy before July, regardless of what is ultimately decided about pricing sequencing.

We were also given, via the exit interviews, the finding that two of the largest-ACV departures in the quarter were coded as driven by the customer's business being acquired, rather than by a pricing or product decision. We exclude these two accounts from the pricing-and-migration narrative, since a business being acquired and consolidated onto an acquirer's system is a cause of churn that repricing or portal design would not have prevented. We note, however, that these are only two accounts out of 209 churned in the quarter, and while they are large by ACV and therefore visible in revenue-weighted terms, they do not materially change the account-count churn rate or the patterns described above by size, sequence, or renewal month.

---

## Limitations

We want to state these plainly rather than let them sit implicitly behind the numbers above.

**The two changes are confounded, not merely correlated.** Because repricing occurs at renewal and portal migration has been proceeding on a separate rollout schedule, most accounts that were repriced in January had already migrated or were migrating around the same time. We cannot construct a clean comparison group of accounts that were repriced without any migration exposure at all, because the two initiatives have been running concurrently across nearly the entire customer base since September 2025. The sequence cut above is the best available proxy for isolating an ordering effect, but it is not a controlled comparison, and the two groups may differ on unobserved traits, as discussed above.

**Telemetry has no pre-migration baseline, for any account, ever.** This is worth repeating in its own paragraph because it is the limitation most relevant to a company considering how to sequence the July conversion around product usage. We can measure usage after an account is on the new portal. We cannot measure usage before, for any account, because the instrumentation did not exist before September 2025. Any claim about whether the new portal itself changed customer behavior in a way that predicts churn is not testable with current data and will not become testable retroactively; it can only be addressed going forward, by comparing new-portal telemetry against future outcomes across accounts that are otherwise similar.

**Exit interview coverage and coding are incomplete and subjective.** Seventy-one percent of churned accounts have an exit interview on file; the remainder are unaccounted for in the reason-code breakdown entirely. Reason codes are assigned by the account manager or CS representative who conducted the conversation, based on a single interaction, and are subject to the incentives and framing of the person doing the coding. The acquisition-versus-price distinction for the two largest departures rests on this same imperfect process.

**Sample sizes within some cuts are modest.** While the account-size and sequence splits are directionally strong and consistent with plausible mechanisms, 209 churned accounts split across size bands, sequence groups, and renewal months produces cells that are not large in absolute count, particularly for above-$50,000 accounts, which are a smaller share of the book by count even though they carry more revenue. We would treat any of these splits with more confidence if the pattern persists into a second quarter of data, particularly through the July conversion itself.

**The support staffing shock is itself a confound we cannot fully net out.** Five of 18 support staff resigning in early February, and the resulting response-time spike, overlaps with the same quarter as the pricing and migration changes for the entire customer base, not for a subset we could compare against an unaffected control group. We cannot state what Q1 churn would have looked like absent the support degradation, only that the timing makes it unsafe to assign the full 9.7 percent figure to pricing and portal changes alone.

**We do not yet have a full quarter of comparable data on the 61 percent of the book still to convert.** Everything in this brief describes the January cohort. Whatever pattern holds for that cohort is the best evidence available for what July might bring, but the July cohort could differ in composition, for instance, if it happens to be weighted more toward larger or smaller accounts than the January cohort was.

---

## Implications for the July Decision

We offer four implications, ordered from most to least confident.

**First, fix support capacity before July, independent of any pricing decision.** The response-time spike from 4 to 19 hours is unambiguous, internally caused, and fully within operational control. Whatever the eventual read on pricing and portal sequencing, a repeat of the February staffing shock during the July renewal wave, which is likely to be another concentrated volume event given the renewal clustering described above, would compound whatever churn pressure the repricing itself produces. This is the one lever in this brief that does not depend on resolving any of the attribution ambiguity above; it should be treated as a prerequisite for July, not a parallel workstream.

**Second, sequence migration ahead of repricing for the remaining 61 percent of the book wherever the account has not yet moved to the new portal.** The 5.8 percent versus 11.9 percent split is the strongest, most operationally actionable finding in this brief, even accounting for the selection concerns noted above. If it is feasible to complete portal migration for the July cohort in advance of their renewal date, rather than repricing them on the legacy portal or simultaneously with migration, the January pattern suggests this could materially reduce churn in the July wave. We recommend this as a near-term operational change to test directly, since it does not require resolving the underlying mechanism, whether it is change fatigue, goodwill, or selection, to be worth doing.

**Third, treat the smallest accounts as a distinct decision, not a rounding error.** The 14.2 percent versus 4.1 percent gap by account size is large enough that a uniform per-document conversion for all remaining accounts risks a disproportionate loss of the smallest tier. Options worth considering before July include a graduated transition, a minimum-commitment floor that caps the increase for the lowest-usage accounts, or continued per-seat pricing for accounts below a defined ACV threshold, at least until account-management capacity for that tier is strengthened. We flag that we do not have a clean estimate of what share of ARR the under-$12,000 tier represents, since it is a large share of accounts by count but a much smaller share of revenue; that figure should be pulled before a final decision is made on how much flexibility to extend to that tier.

**Fourth, and least confidently, we cannot tell the CEO how much of the Q1 churn increase to attribute to price itself, as distinct from the portal or the support collapse, and we do not think a more sophisticated model built on the current data would resolve that honestly.** The three changes happened to the same customer base in the same quarter, and the billing and CRM records available to us describe outcomes and after-the-fact reasons, not the customer's actual decision process. What we can say is that the pattern of churn, concentrated in small accounts, concentrated in accounts repriced ahead of migration, and occurring during a support degradation, is consistent with a story in which the pricing change was a real contributor but not the sole one, and in which the manner and order in which it was delivered mattered as much as the change itself. If the company wants a cleaner answer before scaling repricing further after July, we would recommend building ticket-level linkage between support interactions and churned accounts, extending exit-interview coverage toward the full churned population rather than 71 percent, and treating the July cohort's sequence and support conditions as a natural experiment to be tracked deliberately rather than reconstructed after the fact, as this brief has had to do for January.

We are available to walk through any of these cuts in more detail, and we would recommend a short follow-up review in September, once July renewal outcomes are known, using the same framework so that the two quarters can be compared directly.

We would add one further note, prompted by a question Mr. Oyelaran raised when this analysis was first scoped: whether the timing of this review itself, arriving after the January cohort had already converted, limits what can be done differently for July. It does, in one respect and not in another. The pricing model for the July cohort was set by the board decision made before this brief was commissioned, and nothing here is intended to reopen that decision. What remains open is sequencing, staffing, and account-level exceptions within the existing plan, and those are the levers this brief has tried to speak to concretely rather than in the abstract.

## Appendix A: Proposed Monitoring Plan for the July Cohort

If the recommendations above are adopted, we propose the following measurement plan so that the September follow-up review is not built on the same reconstructed, after-the-fact basis as this one.

**Sequence tracking.** For every account converting in July, record the date of portal migration and the date of repricing as two separate fields at the account level, even where both occur close together, so that the sequence split can be computed directly rather than inferred. For the January cohort, we had to derive sequence from migration logs and renewal dates that were not designed to be read together; a purpose-built field would remove that ambiguity for July.

**Support linkage.** Establish a join between support ticket records and the churn flag at the account level, covering at minimum the 60 days preceding a churn date, so that response time exposure can be measured directly for churned accounts rather than inferred from the aggregate median. This would let us state, for the July cohort, what share of churned accounts had a support interaction with an elevated response time before their decision, rather than relying on the coincidence of timing as we have had to here.

**Exit interview coverage.** Extend the exit interview process to the full churned population rather than the 71 percent achieved in Q1, even where the conversation is brief, and add a structured question distinguishing price sensitivity from product friction from service friction, rather than relying on a single reason code chosen after the fact. Where an account's departure is attributed to an external event such as an acquisition, we recommend a secondary confirmation, such as a follow-up email to the departing contact or a note from the account manager corroborating the acquisition independently of the customer's own account, so that this category is not simply the path of least resistance for a coder who does not want to record "price" as the reason.

**Telemetry from day one of migration.** While we cannot recover pre-migration usage for any account already moved, we recommend treating the July cohort's migration dates as the start of a clean observation window, and comparing usage trajectories in the 90 days after migration against churn outcomes in the following two quarters. This will not give us the before-and-after comparison we lack for January, but it will let us build, for the first time, a telemetry-based early-warning signal keyed to the July wave specifically, which the January cohort does not currently have.

**Renewal-month cohort discipline.** Because 38 percent of the book renews in January and a comparable concentration may exist around July, we recommend that any churn figure reported for the July conversion be annualized and compared explicitly against the same calendar quarter a year prior, as this brief has done for Q1, rather than compared against a trailing-twelve-month average that would obscure the same kind of renewal-timing mechanics discussed above.

## Appendix B: Open Questions Not Resolved by This Analysis

We list these separately from the limitations above because they are not flaws in the current data so much as questions that a future analysis, with better instrumentation, should be built to answer.

Does the sequence effect persist once account size is held constant, or is it possible that the migrated-then-repriced group is simply a larger-account group in disguise, given that larger accounts may have been prioritized for early migration by the implementation team for reasons of account importance rather than random rollout order? We do not have migration-order rationale on file and could not test this within the scope of this review.

What share of annual recurring revenue, as distinct from account count, sits in the under-$12,000 tier, and what would a graduated pricing floor for that tier cost the company in ARR terms against what it would likely preserve in retained accounts? This is a modeling exercise that depends on assumptions about price elasticity in that tier that we do not yet have good evidence for beyond the single quarter's churn rate.

Among the 29 percent of churned accounts without an exit interview on file, is there a pattern by size, sequence, or renewal month similar to the 71 percent we do have coded reasons for, or does the missing group differ systematically, for instance, if smaller accounts are also less likely to complete an exit interview because they lack a dedicated account manager to conduct one? If the missing group differs from the coded group, the reason-code distribution we do have may not generalize to the full churned population.

Finally, did the five support staff departures in February have any relationship to the pricing or migration changes themselves, for instance, if support volume or ticket difficulty rose in January in a way that contributed to staff attrition, or were these resignations, like the two acquisition-driven account departures, substantially unrelated to the events under review here? We were not asked to investigate staff attrition causes as part of this brief and did not have access to exit data for departing employees, but the question bears on whether the support degradation should be understood as a consequence of the same underlying stress on the organization or as an independent shock that happened to coincide with it.

We regard these four questions as the natural starting point for the September follow-up review, and we would recommend that data collection for at least the first three begin now, so that the review is not built retrospectively as this one has had to be.
