# Executive Summary 1 of 4 — Merchant Onboarding Service

**Program:** Merchant Onboarding Service (MOS), Program 2024-07
**Sponsors:** Simone Adeyinka (CPO), Gustavo Peralta (VP Engineering)
**Standing reviewer:** Deborah Yankelovich (Head of Compliance)
**Prepared by:** Bao Tran-Nguyen, Director of Portfolio Strategy
**Prepared for:** Portfolio Review Board, 22 January 2026
**Review period:** 1 January – 31 December 2025

---

## Finding and recommendation

The Merchant Onboarding Service is the only program in the 2025 portfolio that beat its approved business case on every metric it was chartered against, and it did so at or under budget. The finding is not in dispute. What the Board should take from this review is the second-order point: the program's success has quietly made it the single largest dependency in Kestrel's 2026 growth plan, and it is currently staffed and governed as though it were a finished project.

The recommendation is that the Board approve $2.4 million of continuation funding for 2026, expand the program's charter to cover underwriting decisioning as a shared platform service and onboarding for the UK and EU corridor, and approve the retention arrangements described in the confidential appendix for the eleven-person delivery team. The Board should specifically decline to declare the program complete and return its engineers to the general pool. Two other programs in this portfolio — terminal firmware and the ledger migration — will bid for those engineers within days of any such declaration, and both bids will be defensible on urgency grounds. That is precisely why the decision needs to be made at the Board rather than by whoever is next to ask.

## What the program was funded to do

MOS was approved in the FY24 planning cycle at $3.1 million against a single primary objective: reduce median merchant time-to-first-transaction from nine days to under 48 hours. The objective came out of loss analysis rather than aspiration. In the 2023 lost-deal interviews, onboarding duration was the most frequently cited reason for choosing a competitor among merchants under $10 million in annual card volume, ahead of pricing and ahead of feature gaps. The business case projected that closing that gap would add roughly 1,400 net new merchants in the first full year and would improve first-year retention in the small and mid-market segment, where early churn had historically clustered in the first ninety days.

The case carried three secondary commitments: that automated underwriting decisions would not degrade fraud loss performance, that the manual review queue would shrink rather than move, and that the resulting decisioning components would be built as reusable services rather than as a single-purpose pipeline.

## What it delivered against that

Median time-to-first-transaction for 2025 was 31 hours, against a target of 48 and a baseline of nine days. The program added 1,914 merchants during the year, 37 percent above the business-case projection. The 2025 onboarding cohort returned net revenue retention of 118 percent. Total spend closed at $3.1 million, on budget.

On a straight cost-per-merchant basis, the build cost $1,620 for each merchant onboarded in year one. If 2026 volumes hold and no further platform build is required, that figure falls below $650 as the fixed cost amortizes across a second cohort. This is the strongest unit economic result in the portfolio by a wide margin.

Three qualifications belong in front of the Board rather than in a footnote, because each of them shapes the 2026 decision.

First, the 1,914 figure is not wholly attributable to the program. Sales capacity in the small and mid-market segment grew during the same period, and the two effects have not been separated. Sales leadership and the program office disagree, in good faith, about the split. The program office proposes a geographic holdout test in the first half of 2026 to settle it. That test costs nothing but discipline, and I recommend the Board ask for the result at the July session.

Second, the median is excellent and the tail is not. P90 time-to-first-transaction remains at 6.2 days, concentrated in the roughly 8 percent of applications routed to manual review — high-risk MCCs, thin-file principals, and any applicant tripping a sanctions screening near-match. The manual queue did shrink in absolute terms, which satisfies the secondary commitment, but it did not get faster. Merchants in that 8 percent experience a materially worse Kestrel than the median merchant does, and they are disproportionately the larger accounts.

Third, the 118 percent retention figure covers a cohort with less than twelve months of tenure in most cases. It is a genuine early signal, not a settled result, and it should be re-reported at the twenty-four-month mark before it is used in any external material.

Ms. Yankelovich's review raised one substantive concern that I have adopted into the recommendation. The auto-approval model was trained on 2023–2024 application data. Fraud losses on the auto-approved cohort rose from 0.9 to 1.4 basis points of processed volume over the second half of 2025. That level remains well inside tolerance and well inside the business case, but the direction is consistent across four consecutive months, and it is the pattern one expects when a model is being probed. Retraining and a revised challenger framework are inside the $2.4 million request.

## What the Board is being asked to decide

The Board is asked to approve three things. First, $2.4 million of 2026 funding, of which approximately $900,000 is model retraining, monitoring, and manual-queue automation on the existing footprint, and approximately $1.5 million is new scope. Second, the reclassification of onboarding decisioning from a product feature to a shared platform service with a named accountable owner, which is the precondition for the terminal and partner channels reusing it rather than rebuilding it. Third, the team retention arrangements, which require Board notice because two of them exceed the CPO's delegated authority.

The Board is not being asked to approve the EU corridor as a market entry. That decision belongs to the commercial plan and comes to the Board separately in March. This request funds the onboarding and underwriting capability that entry would require, on the reasoning that the capability has an eleven-month lead time and the market decision has a two-month lead time.

## Exposure if the decision waits a quarter

The exposure is not financial in the first instance. It is the team.

The MOS delivery group is eleven people, four of whom hold the working knowledge of the decisioning pipeline. Both of the other two major programs in this portfolio are behind and will be looking for exactly those skills in February. If the Board defers, the practical outcome is not that the team waits — it is that the team is dispersed by ordinary managerial pressure, and the 2026 request returns in April as a rebuild rather than a continuation. The program office's estimate is that a three-month gap adds roughly $700,000 to the same scope, most of it re-establishing context.

The second exposure is the model. Fraud loss drift on auto-approved merchants is currently manageable at 1.4 basis points. If the trend continues at the observed rate and retraining slips a quarter, the projected exposure at the June measurement point is 2.1 to 2.4 basis points, which crosses the threshold at which the compliance function would recommend reverting a share of auto-approvals to manual review. Doing so would push the median back toward three days and would forfeit the program's headline result to protect a loss rate that costs less to fix directly.

The third exposure is sequencing. A Q2 start on the EU corridor puts first revenue in Q1 2027 rather than Q3 2026, on the current implementation estimate. Given what the rest of this portfolio review contains, the Board should be reluctant to give away the one growth item that is presently on schedule.

---

# Executive Summary 2 of 4 — Terminal Firmware Modernization

**Program:** Terminal Firmware Modernization (TFM), Program 2023-11
**Sponsors:** Gustavo Peralta (VP Engineering), Simone Adeyinka (CPO)
**Standing reviewer:** Deborah Yankelovich (Head of Compliance)
**Prepared by:** Bao Tran-Nguyen, Director of Portfolio Strategy
**Prepared for:** Portfolio Review Board, 22 January 2026
**Review period:** 1 January – 31 December 2025

---

## Finding and recommendation

Terminal Firmware Modernization missed three of its five 2025 milestones, leaves 22 percent of the installed base — 9,020 of 41,000 terminals — running an unsupported build, and has lost the delivery capacity it was depending on. The payment-card attestation deadline of 31 October 2026 is not merely at risk; on the current plan and the current vendor, it will not be met. This is the finding, and I want to be unambiguous about it because previous reporting on this program has used the word "amber" for three consecutive quarters and the word has stopped carrying information.

The recommendation is that the Board authorize $4.8 million of contingency funding, direct management to exit the incumbent firmware vendor under the change-of-capability provisions of the master agreement, approve the standing-up of an in-house firmware build and signing capability, and — this is the item most likely to be resisted and most likely to matter — instruct management to open a written, proactive conversation with the acquiring bank and the card networks about the attestation timeline within thirty days, before the deadline is missed rather than after. Kestrel's negotiating position on a disclosed, plan-backed delay is categorically different from its position on a discovered one.

## What the program was funded to do

TFM was approved in late 2023 at $6.2 million over two years, with a single hard external constraint: every terminal in the installed base must be running an attestable firmware build by 31 October 2026, the date on which the previous validation for the legacy build expires. The program was also chartered to deliver the capability that makes the next such deadline survivable — remote, signed, over-the-air updates — so that Kestrel would not have to repeat a fleet-wide truck-roll exercise every certification cycle. That second objective is worth as much as the first over any five-year horizon, and it is the one most likely to be sacrificed under time pressure.

The 2025 plan carried five milestones:

- **M1 — Signed build toolchain and key ceremony.** Delivered, four weeks late, and the only fully clean milestone of the year.
- **M2 — Remote update agent, general availability across all three terminal families.** Delivered for one family only. The two older families, which together represent 61 percent of the fleet, remain manual-update.
- **M3 — Pilot cohort of 2,500 terminals migrated and stable for sixty days.** Missed. 1,180 terminals migrated; stability window restarted twice after rollback.
- **M4 — Cryptographic key rotation across the fleet.** Missed. Not started.
- **M5 — 60 percent fleet cutover by year end.** Missed. Actual cutover 78 percent, which sounds like an overachievement until one reads the definition: 78 percent are on *a* supported build, of which most were already there at program start. Net movement attributable to TFM in 2025 was approximately 4,400 terminals.

## What it delivered against that

The honest summary is that 2025 produced the foundation and none of the fleet work. The toolchain exists, the signing infrastructure is real and well built, and the remote agent works on the newest terminal family. Against the external deadline, none of that matters yet, because 9,020 terminals are still running a build that will not be attestable in nine months.

The delivery problem is now acute. The lead firmware vendor lost approximately half its engineering team in the fourth quarter following its acquisition. Kestrel's account is served by four engineers, two of whom joined in November. The vendor has not repudiated the contract and has not proposed a revised schedule; it has simply stopped committing to dates, which is a more difficult position to manage than outright breach because it delays the moment at which contractual remedies become available.

The arithmetic of the remaining work is the core of this summary. Nine thousand and twenty terminals must be remediated by 31 October 2026. From 1 February, that is nine months, or roughly 1,000 terminals a month. From 1 May — which is where a deferral to the April session puts us, allowing for vendor transition — it is six months, or roughly 1,500 a month. The highest monthly rate the program has ever achieved is 740. The remediation is not uniformly remote: on current family mix, an estimated 3,300 of the 9,020 require physical access, at an average field cost of $210 per unit inclusive of scheduling and merchant downtime.

Ms. Yankelovich's assessment, which I endorse without qualification, is that an attestation lapse is not a technical event. It is a reportable condition to the acquiring bank, it appears in every subsequent diligence process Kestrel undertakes, and it moves liability for fraudulent transactions on affected terminals in a direction that the merchant contracts do not fully anticipate.

## What the Board is being asked to decide

The Board is asked to authorize $4.8 million in contingency funding, taking program lifetime authorization to $11.0 million. Approximately $2.1 million funds a second firmware integrator engaged in parallel rather than sequentially. Approximately $1.4 million funds the in-house build and signing capability, which ends the single-vendor dependency permanently. Approximately $900,000 funds field remediation for the terminals that cannot be reached remotely. The remainder is a hardware-replacement reserve for an estimated 400 to 600 units of the oldest family, for which the program office now believes remediation will cost more than replacement.

The Board is also asked to name a single accountable executive with authority across engineering, field operations, and vendor management. The program's 2025 failure is not primarily technical. Three functions each held a veto and none held the schedule.

## Exposure if the decision waits a quarter

A deferral to the April session removes three of the nine remaining months and raises the required remediation rate from roughly 1,000 terminals a month to roughly 1,500 — a rate 100 percent above anything the program has demonstrated. My assessment is that a deferral does not delay the decision; it converts it. In April the Board will not be deciding whether to fund the plan. It will be deciding between a negotiated extension with the networks and a partial fleet shutdown, and it will be doing so with less credibility on both counts.

The quantified exposure has three parts. Field remediation costs rise with compression: the program office estimates a 35 to 50 percent premium for the same work performed in six months rather than nine, on the order of $600,000 to $900,000. Vendor transition lead time is eight to ten weeks and does not compress at all, so a quarter of delay is a full quarter of lost delivery, not a partial one. And the negotiating window with the networks closes: a request for accommodation made in February, backed by a funded plan and a demonstrated remediation rate, is a routine matter. The same request made in August is an incident.

The residual exposure, if 9,020 terminals reach 31 October 2026 unattested, is the merchant volume running across them. Those terminals carry an estimated $340 million in annual card volume across roughly 2,600 merchants, and the affected merchants skew toward the older, higher-tenure, lower-churn end of the base — which is to say, toward the accounts Kestrel can least afford to disrupt.

---

# Executive Summary 3 of 4 — Self-Serve Developer Tier

**Program:** Self-Serve Developer Tier (SSDT), Program 2024-14
**Sponsors:** Simone Adeyinka (CPO)
**Standing reviewer:** Deborah Yankelovich (Head of Compliance)
**Prepared by:** Bao Tran-Nguyen, Director of Portfolio Strategy
**Prepared for:** Portfolio Review Board, 22 January 2026
**Review period:** 1 January – 31 December 2025

---

## Finding and recommendation

The Self-Serve Developer Tier succeeded at the part of its thesis that was uncertain and failed at the part that was assumed. It attracted 12,400 signups, essentially in line with the volume the business case required, which establishes that Kestrel can generate developer demand without a sales motion. It converted 380 of them to paid accounts against a plan of 1,500 — 25 percent of plan — which establishes that the product does not carry a developer from evaluation to production on its own. The program spent $2.1 million and now generates a support load of roughly 900 tickets a month, borne by a paid tier that receives no benefit from it.

The recommendation is that the Board approve Option B below: close the free tier to new signups within thirty days, convert it to a time-boxed 45-day trial requiring a payment instrument, migrate the 380 paying accounts to the standard commercial plan on their existing pricing, and sunset all remaining free accounts on 30 June 2026 with ninety days' notice. This preserves the demand-generation asset, which is genuinely valuable, and stops the subsidy, which is not. I do not recommend outright termination, and I do not recommend continuing as-is; my reasoning on both is below.

## What the program was funded to do

SSDT was approved at $2.0 million to test a specific proposition: that Kestrel could reach the long tail of independent software vendors and in-house development teams without direct sales, and that a free tier with production-grade APIs would produce a self-serve revenue line of $1.8 million to $2.4 million in annual recurring revenue by the end of the second year. The plan called for 12,500 signups and 1,500 paid conversions in year one, an assumed 12 percent conversion rate drawn from published comparables in adjacent developer-tools markets.

The program was explicitly framed to the Board as an experiment with a decision point at twelve months. That framing was correct, and this summary is that decision point arriving on schedule. The Board should note that reaching a negative finding on time is a better outcome than most experiments produce.

## What it delivered against that

Signups came in at 12,400 against a plan of 12,500 — within one percent. Conversion came in at 380 against 1,500. The conversion rate was 3.1 percent against an assumed 12 percent, a four-fold miss on the single assumption the business case did not test.

Spend closed at $2.1 million against $2.0 million authorized. Cost per paid account acquired is therefore $5,526. The average self-serve account bills approximately $310 per month, or $3,720 annually, meaning the acquisition cost is recovered in month eighteen before any gross-margin adjustment and considerably later after it. For comparison, blended customer acquisition cost in the direct mid-market channel is under $4,000 against materially higher account values.

The support load is the finding the Board has not previously seen quantified. Nine hundred tickets a month arrive from a population of 12,400 accounts, of which 12,020 pay nothing. At an average handle time of 33 minutes, this is approximately 495 support-hours a month, or 3.1 full-time equivalents, an annualized fully loaded cost of approximately $341,000. That cost sits in the paid-tier support budget. Expressed differently, every paying Kestrel merchant contributes to answering questions from developers who have not paid and, on the evidence of the last twelve months, are 97 percent likely never to pay. Ticket analysis shows 71 percent are integration and environment questions that documentation should absorb, which is a genuine product deficiency and also a genuine reason to expect that the current cost is structural rather than transitional.

Ms. Yankelovich raised a further issue that changes the urgency of the decision. The 12,400 accounts hold live API credentials. An estimated 8,900 have been dormant for more than 120 days. Dormant credentials on a sandbox that shares an identity plane with production is a standing finding in Kestrel's own internal security review and will be a finding in the next external assessment. A tier that is being wound down does not accumulate more of them; a tier left open for another quarter accumulates roughly 3,100 more.

## What the Board is being asked to decide

Three options were modelled. The Board is asked to select one.

- **Option A — Terminate.** Sunset the tier entirely by 31 March 2026, migrate or lose the 380 paying accounts. Saves the full $341,000 support cost and eliminates the credential exposure. Forfeits $1.4 million of annualized revenue currently attached to those 380 accounts and to the 26 partner-sourced deals the tier has been credited with originating. Cost of execution, approximately $180,000.
- **Option B — Restructure (recommended).** Close to new free signups within thirty days; replace with a 45-day trial requiring a payment instrument; migrate the 380 to standard commercial terms; sunset remaining free accounts 30 June 2026 with ninety days' notice; reassign the tier from a standalone revenue line to a distribution channel reporting into the partner and ISV motion. Modelled to retain 300 to 330 of the 380 accounts, reduce ticket volume by 60 to 70 percent within two quarters, and require $290,000 of transition funding.
- **Option C — Continue and invest.** Fund a further $1.6 million to fix onboarding, documentation, and the self-serve upgrade path on the argument that the conversion miss is a product problem rather than a market problem. Defensible on the evidence, but it asks the Board to spend $3.7 million cumulatively against a revenue line the market has not yet validated, at a moment when the ledger migration needs $6.9 million and terminal firmware needs $4.8 million.

Option B is recommended because the demand-generation result is real and should not be destroyed, while the revenue thesis is not proven and should not be funded further from this portfolio.

## Exposure if the decision waits a quarter

The direct cost of a quarter's delay is modest and calculable: approximately $525,000 in program run rate and support, and approximately 2,700 additional tickets against the paid tier's support capacity.

The indirect costs are larger. Roughly 3,100 additional signups arrive per quarter, each of which becomes an account to be notified, migrated, or terminated, and each of which extends the credential exposure. Sunset cost scales with population, so every quarter of delay raises the cost of the eventual decision by an estimated $60,000 to $80,000.

The reputational exposure compounds faster than the financial one. The free tier now appears in third-party tutorials, two published integration guides, and a widely used open-source SDK. A tier closed at 12,400 accounts is a product decision; a tier closed at 20,000 accounts, having become load-bearing infrastructure for other people's projects, is a public event that Kestrel's developer relations function is not staffed to manage. The right moment to close a free tier is always earlier than it feels.

---

# Executive Summary 4 of 4 — Core Ledger Migration

**Program:** Core Ledger Migration (CLM), Program 2023-02
**Sponsors:** Gustavo Peralta (VP Engineering), Simone Adeyinka (CPO)
**Standing reviewer:** Deborah Yankelovich (Head of Compliance)
**Prepared by:** Bao Tran-Nguyen, Director of Portfolio Strategy
**Prepared for:** Portfolio Review Board, 22 January 2026
**Review period:** 1 January – 31 December 2025

---

## Finding and recommendation

The Core Ledger Migration was approved at $7.5 million, has spent $11.3 million, and has moved 61 percent of accounts. Straight-line extrapolation puts completion at approximately $18.5 million, and straight-line extrapolation understates it, because the 39 percent of accounts not yet moved are disproportionately the exception cases the program deliberately sequenced last. The program has also produced eleven dual-write reconciliation breaks in the last quarter alone, two of which required manual settlement totalling $1.4 million.

The finding is that the program is materially over budget and that its estimating process is not currently capable of producing a number the Board should rely on. The recommendation is nonetheless **not** to pause it. The dominant risk in this program is not the overrun. It is the duration of the dual-write period, during which two ledgers must agree and every quarter of disagreement costs real money and creates a control deficiency. Pausing extends that period indefinitely and converts a cost problem into an audit problem.

I recommend the Board re-baseline the program at $6.9 million of incremental funding with a contractual exit from dual-write no later than 31 December 2026, commission an independent estimate review at approximately $180,000 to be delivered before the April session, and direct that the reconciliation breaks be treated and reported as a control deficiency rather than as engineering defects.

## What the program was funded to do

CLM was approved in early 2023 to replace a ledger that had reached its architectural limits. The legacy system could not support intraday settlement, could not partition by jurisdiction — which caps Kestrel's ability to expand beyond the United States — and required a maintenance window that had become the single largest source of merchant-facing incident minutes. The business case was defensive rather than revenue-generating, and correctly so. The approved scope was $7.5 million over 24 months, migrating all merchant and settlement accounts to the new ledger with a dual-write period of no more than two quarters.

## What it delivered against that

Sixty-one percent of accounts are migrated and operating on the new ledger. The migrated population is stable and the new ledger's performance characteristics have met specification, which is worth stating plainly because it establishes that the target architecture is sound. The problem is entirely one of execution economics and elapsed time.

Spend stands at $11.3 million against $7.5 million approved — 151 percent of authorization, $3.8 million over. On unit economics, $11.3 million has bought 61 percent of the migration, implying $18.5 million for the whole, or $7.2 million to complete. The program office's own estimate is $6.9 million; the difference is a productivity improvement they expect from tooling now in place. That expectation may be sound, but the same program office estimated $7.5 million for the whole migration in 2023, and the Board is entitled to require external corroboration before accepting a second estimate from the same source. That is the reasoning behind the independent review, and I want to be clear that it is a governance measure rather than a statement about the team's competence. Estimating a migration of this kind from the inside is genuinely hard, and the program has been consistently transparent about its overruns as they occurred, which is the reason this review contains no surprises.

The dual-write period is the more serious finding. It was scoped at two quarters and has now run seven. Eleven reconciliation breaks occurred in the fourth quarter — a rate of roughly one every eight days. Nine were caught by automated reconciliation and corrected within the settlement cycle. Two were not, and required manual settlement of $1.4 million to bring merchant balances to a correct state.

Ms. Yankelovich's position, which I have adopted into the recommendation and which the Board should weigh carefully, is that the significance of those two breaks is not the $1.4 million. Kestrel recovered the funds and no merchant was left short. The significance is that a $1.4 million settlement adjustment was executed manually, outside the automated control path, on the authority of a small number of individuals. That is precisely the fact pattern an external auditor is trained to look for, and if the pattern persists into the current fiscal year it is a credible candidate for a significant deficiency finding, with a material weakness available if the frequency increases. It would also be visible in any SOC 2 Type II report Kestrel issues covering the period, and therefore visible to every enterprise prospect who asks for one.

The critical property of this risk is that it is a function of *time in dual-write*, not of accounts migrated. Every additional quarter of dual-write is, on the observed rate, another eleven breaks and another manual settlement event of comparable size. This is why acceleration is the risk-reducing option and delay is the risk-increasing one, notwithstanding that acceleration is the one that costs money.

## What the Board is being asked to decide

The Board is asked to decide three things. First, whether to authorize $6.9 million of incremental funding, taking lifetime authorization to $18.2 million, subject to the independent estimate review confirming the figure within a 15 percent tolerance and subject to a hard dual-write exit date of 31 December 2026 written into the program charter with monthly reporting to this Board rather than quarterly. Second, whether to commission the independent estimate review at approximately $180,000 for delivery before the April session. Third, whether to direct that reconciliation breaks be logged, escalated, and reported through the control framework rather than the engineering defect process, with a standing report to the Audit Committee.

The Board should also record what it is choosing against. The alternative to completing the migration is not the status quo; it is a deliberate decision to stop at 61 percent and consolidate back onto the legacy ledger, abandoning $11.3 million and reacquiring every constraint the program was chartered to remove. The program office estimates that reversal at $4.1 million and eighteen months. It is a genuine option and it is on the table, but it is not a cheaper one.

## Exposure if the decision waits a quarter

A deferral to the April session carries four exposures, and unlike the other programs in this portfolio they are all quantifiable.

The program continues to burn at approximately $1.6 million a quarter and cannot be idled without dispersing the team, so a quarter of deferral spends $1.6 million against no approved plan — which is itself an authorization problem the Board should not want to repeat.

A further quarter of dual-write is, on the fourth-quarter rate, approximately eleven more reconciliation breaks and an expected manual settlement exposure in the range of $1.2 million to $1.6 million.

The 31 December 2026 dual-write exit is achievable on a February start and becomes marginal on a May start. Every quarter of deferral pushes the exit into 2027, which means dual-write spans a second fiscal year end and a second external audit — the point at which the control deficiency stops being a matter Kestrel is remediating and becomes a matter Kestrel has carried across two reporting periods.

Finally, key-person risk. Four engineers hold the dual-write reconciliation logic. Two are named in the Merchant Onboarding retention appendix as well, because they are the same class of scarce skill. A program without an approved forward plan is a program people leave, and the working knowledge of why two ledgers disagree is not written down anywhere I would want to rely on.
