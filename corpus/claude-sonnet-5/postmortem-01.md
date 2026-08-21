# Incident Postmortem: Anchor Price Publication Failure and Extended Point-of-Sale Outage

**Incident ID:** INC-2026-1204-ANCHOR
**Date of Incident:** December 4–5, 2026
**Date of Report:** December 18, 2026
**Status:** Final
**Distribution:** Executive Leadership, Retail Technology, Store Operations, Finance, Compliance, Board Risk Committee (summary only)

**Prepared by:** Retail Technology Incident Review Team
**Reviewed by:** Nia Broadwater (Director, Retail Technology), Doug Pelletier (Manager, Point-of-Sale Engineering), Fatima Zubairi (VP, Store Operations)

---

## 1. Summary

On the night of Friday, December 4, 2026, the nightly Anchor price-book publication job — the system of record that distributes updated pricing to in-store controllers across Northway Fuel and Provisions' 190 stores — failed partway through its run. The job's completion logic did not distinguish between a fully confirmed distribution and a partial one, and it reported success. As a result, 118 of 190 stores received a partial price file covering roughly 2,900 items, without the corresponding loyalty-exclusion updates that would normally accompany a price change. Waypoint, the loyalty and promotions engine that applies discounts at the terminal, had no way to know these items were already repriced downward, and it stacked existing promotions on top of the new, lower list prices. The combined effect, in the affected stores, was severely underpriced merchandise — in the most visible case, energy drinks ringing at 61 cents a unit.

The problem went undetected for approximately 19 hours. It surfaced only because a district manager in Plattsburgh happened to observe a customer purchasing 40 cases of energy drinks at the mispriced rate and called it in at 6:15 p.m. Saturday, December 5 — the start of the quarter's busiest retail evening.

The on-call engineer, Miguel Arellano, correctly identified that loyalty discounts were stacking on erroneous prices but, lacking a validated rollback path, made the judgment call to disable the Waypoint engine outright and push a null promotion table to store controllers to stop further mispricing. This action had a consequence that was not fully anticipated: it took point-of-sale systems offline across all 118 affected stores for three hours and forty minutes, from 8:10 p.m. to approximately 11:50 p.m., during one of the highest-volume selling windows of the year.

What followed was a rapid, if improvised, incident response: point-of-sale engineering leadership was paged, incident command was established, store operations leadership managed field communications, and a customer care team absorbed over 2,100 calls the following day. Stores without functioning terminals fell back to manual, cash-based transactions with no standing playbook for doing so consistently.

This postmortem examines the systems and decisions that produced both the pricing error and the extended outage that resulted from the response to it. Two structural weaknesses recur throughout the findings: monitoring and alerting that had quietly decayed over time (an unmonitored mailbox, a queue-depth alert with no living owner), and remediation tooling that was stale relative to the production environment it was meant to protect (a rollback runbook referencing a decommissioned tool, a deferred platform upgrade that would have prevented the initial failure mode entirely). This report does not attribute the incident to any individual's error; the actions taken by on-call and incident response staff were reasonable given the information and tools available to them at the time.

---

## 2. Impact

| Metric | Value |
|---|---|
| Stores affected (partial price file) | 118 of 190 |
| Items mispriced | 2,900 SKUs |
| Detection gap (fault to first report) | ~19 hours (11:40 p.m. Fri. to 6:15 p.m. Sat.) |
| Point-of-sale outage duration | 3 hours, 40 minutes (8:10 p.m.–11:50 p.m. Sat.) |
| Total mispriced transactions | 41,300 |
| Total undercharge amount | $312,000 |
| Amount refunded to date | $88,000 |
| Estimated lost transactions during POS outage | ~26,000 |
| Estimated lost sales during POS outage | $1.1 million |
| Customer care calls handled (Sunday, Dec. 6) | 2,100 |
| Regulatory inquiries opened | 1 (NY State Weights and Measures, opened Dec. 11, 2026) |

The financial figures above are directly attributable and separable: the $312,000 undercharge reflects the difference between correct and mispriced totals across the 41,300 affected transactions, as reconciled by Finance against Anchor's published price book and point-of-sale journals. The $1.1 million in lost sales is an estimate derived from year-over-year and week-over-week comparable-store sales for the affected 118 stores during the outage window, and carries wider uncertainty than the undercharge figure. The $88,000 in refunds reflects proactive and requested reimbursements processed through December 15; refund processing remains open for a small number of disputed transactions.

No injuries, fuel-dispensing safety issues, or data security exposures resulted from this incident. The scope was limited to retail pricing accuracy and point-of-sale availability.

---

## 3. Timeline

All times Eastern. Timeline reconstructed from Anchor job logs, Waypoint transaction logs, store controller logs, the incident bridge transcript, and interviews with participants.

### Friday, December 4, 2026

**11:40 p.m.** — The nightly Anchor price-book publication job begins its scheduled run, distributing the next day's price file to all 190 store controllers.

**11:44 p.m.** — The publication job begins transmitting to a batch of stores served by a secondary distribution segment. A network timeout interrupts transmission partway through this batch.

**11:46 p.m.** — The job's retry logic attempts redelivery to the affected batch three times, per its configured retry policy, and exhausts retries. Internally, 118 stores are marked as not having confirmed receipt of the complete file.

**11:49 p.m.** — The job's top-level status check evaluates only whether the process exited without a fatal exception. It does not check per-store confirmation counts against the total store count. The job logs a status of **SUCCESS**.

**11:51 p.m.** — A queue-depth monitor, unrelated to the job's own status logic, detects an abnormal backlog consistent with the incomplete distribution and fires an automated alert. The alert routes to a distribution mailbox whose sole named recipient departed the company in August 2025. No one receives or actions the alert.

### Saturday, December 5, 2026

**12:03–12:40 a.m.** — The 118 affected stores' controllers ingest the partial price file as received, applying new, lower prices to approximately 2,900 items. No corresponding loyalty-exclusion flags accompany these items, because the exclusion update was part of the portion of the file that did not complete transmission.

**6:00 a.m.–5:00 p.m.** — Affected stores open and operate through the day. Individual instances of unusually low prices are reported informally at a handful of registers, but they are treated as one-off scanning or shelf-tag errors and resolved locally by store staff without escalation to Retail Technology.

**6:15 p.m.** — A district manager covering the Plattsburgh region observes a customer at the register purchasing 40 cases of energy drinks and calls the Retail Technology help desk to report the register total: 61 cents per unit.

**6:30 p.m.** — The help desk logs a ticket, initially triaged as a store-level pricing or shelf-tag discrepancy rather than a systemic issue.

**6:55 p.m.** — On-call engineer Miguel Arellano begins investigating the ticket.

**7:20 p.m.** — Arellano pulls transaction data from additional stores and identifies that the underpricing pattern is not isolated to Plattsburgh; multiple stores across the affected distribution segment show the same items at anomalously low prices.

**7:40 p.m.** — Arellano cross-references the affected item list against the prior night's Anchor publication log and Waypoint's applied-discount log, and determines that Waypoint promotions are stacking on top of new, already-reduced list prices — the loyalty engine has no record that these items were repriced and is applying discounts as though the prices were unchanged.

**8:10 p.m.** — With no validated rollback procedure available (see Section 4 and 5) and mispricing actively occurring at registers during peak Saturday evening volume, Arellano disables the Waypoint promotion engine and pushes a null promotion table to store controllers, intending to stop further discount stacking. This action causes point-of-sale terminals in the 118 affected stores to fault and go offline, as the controllers were not able to gracefully handle the abrupt removal of the active promotion table during live transaction processing.

**8:10 p.m.–11:50 p.m.** — Point-of-sale systems are unavailable in all 118 affected stores.

**8:15 p.m.** — Store-level staff at multiple locations begin improvising: some stores shift to cash-only transactions with manually written receipts; others attempt to hold transactions and ask customers to wait; practices vary by store because no standing outage playbook existed for this scenario. Fuel dispensing (which operates on a separate control path) continues at all sites without interruption.

**9:05 p.m.** — Doug Pelletier, Manager of Point-of-Sale Engineering, is paged as the outage scope becomes clear.

**9:15 p.m.** — Pelletier confirms the outage is store-wide across all 118 affected locations and escalates further.

**9:30 p.m.** — Nia Broadwater, Director of Retail Technology, is engaged and assumes incident command, formally opening a major incident bridge.

**9:35 p.m.** — Broadwater directs parallel workstreams: technical remediation (Pelletier, Arellano), field/store communication, and customer care staffing.

**9:45 p.m.** — Fatima Zubairi, VP of Store Operations, is looped in and takes ownership of store-facing messaging, issuing initial guidance to district managers to maintain cash transactions, log manual sales records, and hold restocking on affected items pending price correction.

**10:00 p.m.** — Technical team begins work to (a) correct the underlying price file and redistribute a complete, confirmed version to all 118 stores, and (b) restore point-of-sale service without immediately re-enabling live promotions.

**10:40 p.m.** — First batch of corrected price data begins redistribution to affected controllers with manual confirmation checks (rather than the automated job) to ensure completeness this time.

**11:20 p.m.** — Point-of-sale service begins coming back online at the first subset of stores as corrected data is confirmed received.

**11:50 p.m.** — All 118 affected stores confirmed with point-of-sale service restored and verified pricing. Waypoint remains disabled fleet-wide as a precaution pending validation of the loyalty exclusion table.

### Sunday, December 6, 2026

**12:10 a.m.** — Incident downgraded from active outage to monitoring status; overnight watch established.

**7:00 a.m.** — Renee Saint-Fleur's customer care team is briefed and staffed up in anticipation of customer inquiries related to Saturday night's pricing and outage.

**7:00 a.m.–8:00 p.m.** — Customer care fields 2,100 calls related to the incident, ranging from receipt disputes and refund requests to general complaints about the outage.

**9:00 a.m.** — Store Operations issues retroactive written guidance to all district managers on cash-handling and manual-transaction procedures, formalizing practices that had been improvised the night before, to ensure consistency should a similar event recur before permanent fixes are in place.

**2:00 p.m.** — Waypoint loyalty engine is re-enabled fleet-wide after the exclusion table is manually validated against the corrected price book.

**Evening** — Finance begins initial reconciliation of affected transactions from Friday night through Saturday's outage.

### Following Week

**December 7–9** — Finance and Retail Technology jointly reconcile the full universe of affected transactions, arriving at the preliminary figures of 41,300 mispriced transactions and $312,000 in undercharges.

**December 10** — Refund process opens for customers who contact the company or are identifiable from loyalty-account transaction records.

**December 11** — New York State Division of Weights and Measures opens an inquiry following consumer complaints and media inquiries about the pricing incident.

**December 12–15** — $88,000 in refunds processed; store-level lost-sales estimate for the outage window finalized at approximately $1.1 million based on comparable-period sales analysis.

**December 18** — This postmortem finalized.

---

## 4. Root Cause

The root cause of the initial pricing error was a **gap between the Anchor publication job's completion status and actual, confirmed delivery of the price file to every store controller**. The job's status logic checked only whether the process completed without throwing a fatal exception; it did not verify that all 190 stores had acknowledged receipt of the complete file before reporting success. When a network interruption caused partial delivery to a batch of 118 stores, the job exhausted its retries silently and still reported success at the job level, because no store-count reconciliation existed between "process completed" and "distribution confirmed complete."

This is a design gap in the publication pipeline, not a one-time failure of infrastructure. The network timeout that triggered the partial delivery was an ordinary, foreseeable failure mode; the system's inability to detect and surface that partial delivery as a failure is the structural root cause. A publication job that reports success only on full, confirmed distribution — and hard-fails or holds back promotion-engine synchronization otherwise — would have prevented the mispricing entirely, regardless of the underlying network hiccup.

A secondary root cause contributed to the outage that followed detection: **there was no tested, low-blast-radius method to suspend loyalty promotions in response to a pricing discrepancy without disrupting point-of-sale availability.** The only tool available to the responding engineer under time pressure was a full promotion-table reset, which the store controllers could not process gracefully during live transactions. The absence of a safer intermediate control — for example, the ability to suspend promotions for a specific item list, or to apply the change only at store open/close boundaries — meant that stopping the pricing bleed required accepting a much larger disruption.

---

## 5. Contributing Factors

**5.1 Deferred platform upgrade.** An upgrade to the Anchor publisher, originally scheduled for March 2026, was deferred twice over the course of the year. Per the upgrade's design documentation, it would have introduced per-store delivery confirmation and would have caused the publication job to fail loudly — rather than report success — on partial distribution. Had this upgrade shipped on its original schedule, the initiating failure mode of this incident would very likely have been caught automatically, before any store received a partial file.

**5.2 Orphaned alert routing.** The queue-depth monitor did fire an alert consistent with the partial distribution, within minutes of the failure. That alert routed to a mailbox associated with an engineer who left the company in August 2025. The distribution list was never updated to reflect a current owner, and no secondary or team-based routing existed as a fallback. This alert, if received, could plausibly have shortened the 19-hour detection gap to well under an hour.

**5.3 Stale rollback runbook.** The documented rollback procedure for a bad Anchor publication was last edited in 2023 and referenced a tool that was decommissioned the following year. When the on-call engineer needed a rollback path on the night of the incident, no accurate procedure existed to follow. This absence of a working runbook was a direct contributor to the decision to take the broader, more disruptive action of disabling Waypoint and pushing a null promotion table.

**5.4 No real-time price-anomaly detection at the point of sale.** There was no automated control — such as an alert on transactions priced significantly below cost, or a threshold check on unusually large single-item quantities at deep discounts — that could have flagged the 61-cent energy drink transactions (or the broader pattern) as they occurred. Detection depended entirely on a manual, human observation by a district manager, 19 hours after the fault occurred and after tens of thousands of dollars in undercharges had already accumulated.

**5.5 Single on-call coverage across adjacent domains.** One on-call engineer was responsible for triaging an issue that ultimately spanned both the Anchor pricing platform and the Waypoint loyalty engine, and whose remediation required point-of-sale engineering expertise. Escalation to point-of-sale engineering leadership occurred only after the disabling action had already caused a store-wide outage, rather than as part of an earlier, coordinated response.

**5.6 No standing store-level contingency for point-of-sale unavailability.** Store staff had no documented procedure for handling a multi-hour point-of-sale outage during a high-volume period. The cash-based, manually logged transactions that stores improvised on the night of December 5 were a reasonable field-level response given the absence of guidance, but the resulting inconsistency across the 118 stores complicated reconciliation, likely contributed to some portion of the lost-transaction total, and created downstream cash-handling and audit questions that Store Operations had to resolve after the fact rather than in advance.

**5.7 Low-severity signals not escalated earlier.** Isolated reports of unusually low prices at individual registers occurred throughout the day on Saturday, prior to the Plattsburgh call, and were resolved locally as apparent one-off errors rather than escalated or aggregated. No mechanism existed to correlate multiple, independent reports of pricing anomalies across different stores into a single signal of a systemic issue.

---

## 6. What Worked

- **Field escalation, once recognized as unusual, moved quickly.** The Plattsburgh district manager's direct call to the help desk, rather than routing the observation through normal store-issue channels, got the report in front of an engineer within 15 minutes.
- **Technical diagnosis was fast once engaged.** From first investigating the ticket to correctly identifying the stacking mechanism between Anchor and Waypoint took the on-call engineer under 90 minutes, without the benefit of an accurate runbook or prior documentation of this failure mode.
- **Incident command stood up promptly and the division of labor was clear.** Once paged, Doug Pelletier and Nia Broadwater established a functioning incident bridge within 25 minutes, and responsibilities split cleanly across technical remediation (Pelletier, Arellano), store communication (Zubairi), and customer response (Saint-Fleur), with minimal overlap or confusion about ownership.
- **Store communication reached the field despite the outage.** Store Operations was able to get cash-handling and hold-transaction guidance to district managers during the incident itself, even without a pre-built playbook, limiting some of the inconsistency that would otherwise have resulted.
- **Customer care absorbed a large volume without collapsing.** Fielding 2,100 calls in a single day, on short notice, without a pre-existing incident-specific script, represents a significant surge capacity that functioned as intended.
- **Reconciliation and refunds moved at a reasonable pace after the fact.** Finance produced a defensible, itemized accounting of affected transactions within a week, and refunds began flowing within days of the incident closing.

## 7. What Did Not Work

- **Detection relied entirely on a customer-facing coincidence.** No system-level control caught the initial failure for 19 hours; the incident was discovered only because a district manager happened to witness an extreme case in person.
- **Two independent monitoring and alerting mechanisms had silently decayed.** The queue-depth alert had a dead-letter destination for over a year, and the rollback runbook referenced tooling that had not existed for two years. Neither gap was caught by any periodic review process, because no such review process existed for on-call documentation or alert routing ownership.
- **The remediation action taken had a larger blast radius than anticipated.** Disabling Waypoint and pushing a null promotion table was a reasonable response given the tools available, but it was not a tested action, and its effect of taking point-of-sale fully offline in 118 stores was discovered only when it happened, on the year's busiest selling night to that point.
- **Cash handling during the outage was genuinely improvised, not executed against a plan.** Store-level practices varied, complicating later reconciliation and creating operational and audit exposure that had to be cleaned up after the fact rather than avoided.
- **A twice-deferred upgrade left the organization exposed to a known-preventable failure mode.** The upgrade that would have caught this specific failure had been in the queue for nine months at the time of the incident.
- **External discovery outpaced internal disclosure.** The scale of consumer-facing pricing errors and the subsequent outage drew sufficient public and customer attention that a state regulatory inquiry was opened within a week, indicating the response, while operationally sound, did not include an external-facing regulatory or public-disclosure component fast enough to get ahead of that inquiry.

---

## 8. Action Items

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Complete the deferred Anchor publisher upgrade, including per-store delivery confirmation and hard-fail (not silent success) on incomplete distribution | Priya Natarajan, Anchor Platform Engineering Lead | Jan 30, 2027 |
| 2 | Audit all on-call and monitoring alert distribution lists across Retail Technology for orphaned recipients; implement quarterly ownership review as a standing process | Sam Okafor, IT Service Management | Jan 15, 2027 |
| 3 | Rewrite the Anchor/Waypoint rollback runbook against current production tooling; validate it via tabletop exercise with on-call staff | Doug Pelletier, Manager, Point-of-Sale Engineering | Feb 6, 2027 |
| 4 | Design and implement a low-blast-radius method to suspend specific loyalty promotions (by item or exclusion list) without requiring a full promotion-table reset or point-of-sale restart | Doug Pelletier, Manager, Point-of-Sale Engineering | Mar 13, 2027 |
| 5 | Build automated price-anomaly detection at the point of sale (below-cost thresholds, large-quantity deep-discount flags) with real-time alerting to Retail Technology | Priya Natarajan, Anchor Platform Engineering Lead | Mar 31, 2027 |
| 6 | Establish a documented store-level contingency procedure for extended point-of-sale outages, including standardized cash-handling and manual-transaction logging | Fatima Zubairi, VP, Store Operations | Feb 20, 2027 |
| 7 | Revise on-call staffing model to ensure cross-domain incidents (pricing platform, loyalty engine, point-of-sale) automatically page relevant engineering leads rather than relying on a single on-call escalation | Nia Broadwater, Director, Retail Technology | Feb 6, 2027 |
| 8 | Implement aggregation/correlation of low-severity store-reported pricing anomalies across locations to surface systemic patterns before they require customer or field escalation | Priya Natarajan, Anchor Platform Engineering Lead | Apr 17, 2027 |
| 9 | Develop and publish an incident communications protocol that includes proactive regulatory and public disclosure triggers for consumer-facing pricing incidents | Lena Vogt, Compliance & Regulatory Affairs | Jan 23, 2027 |
| 10 | Formalize a customer care incident-response playbook (staffing triggers, scripting, refund criteria) based on lessons from the December 6 call surge | Renee Saint-Fleur, Customer Care Lead | Feb 13, 2027 |
| 11 | Conduct a fleet-wide reconciliation audit process to catch price-book distribution discrepancies proactively, independent of the publication job's own self-reported status | Priya Natarajan, Anchor Platform Engineering Lead | Mar 31, 2027 |
| 12 | Present findings and remediation status to the Board Risk Committee, including status of the state weights-and-measures inquiry | Nia Broadwater, Director, Retail Technology | Jan 9, 2027 |

Progress against these items will be reviewed at a 60-day and 120-day checkpoint by the Retail Technology leadership team, with status reported to store operations and executive leadership.

---

## 9. Closing Note

This incident resulted from the ordinary and expected failure of a network segment during a routine nightly job — a failure mode that any distributed retail system will eventually encounter. What turned that ordinary failure into a 19-hour undetected pricing error, a three-hour-and-forty-minute point-of-sale outage on the busiest night of the quarter, and a state regulatory inquiry was not any single mistake made on December 4th or 5th, but the accumulated gap between the systems Northway believed it had — a validated publication pipeline, a monitored alert, a working rollback tool, an upgraded platform — and the systems it actually had at the time. The response, once the problem was recognized, was fast and reasonably well-coordinated given the tools available. The work ahead is to close the gap between the intended safety systems and the actual ones, so that the next partial file, network timeout, or queue backlog is caught in minutes by a system, rather than 19 hours later by a customer.

## Appendix A: Technical Detail — Anchor Publication Failure Mechanics

For engineering teams implementing Action Items 1, 5, and 11, this appendix documents the specific failure sequence at a level of detail omitted from the main timeline for readability.

The Anchor publication job runs as a single orchestrating process that fans out to store controllers in batches, grouped by the regional network segment each store's controller connects through. On the night of December 4, the job processed nine batches sequentially. Batches one through six and eight and nine completed and confirmed normally. Batch seven — the 118 stores served by the secondary distribution segment covering the northern and eastern regions — encountered a TCP-level timeout approximately four minutes into transmission, after roughly 60% of the batch's stores had already received and acknowledged the file.

The job's retry handler, on encountering the timeout, re-attempted transmission to the batch as a whole rather than to only the unacknowledged subset. This is itself a secondary defect worth noting: because the retry logic did not track which stores within the batch had already confirmed, each retry re-sent the full file to all 118 stores in the batch, including those that had already received it. This did not cause double-application of prices (controllers correctly de-duplicate by file version), but it meant that retries were less efficient than they could have been and took longer to exhaust than necessary, narrowing the window in which the job could have still succeeded before its retry budget ran out.

After three retries, each waiting 90 seconds, the retry handler logged a `WARN`-level event — not `ERROR` or `FATAL` — reading `batch 7 delivery unconfirmed after retry exhaustion, proceeding`, and moved on to batches eight and nine. The top-level job status aggregator, which determines the SUCCESS/FAILURE flag surfaced to monitoring dashboards and to the nightly operations summary email, only inspects log lines at `ERROR` severity or above. The `WARN`-level line for batch seven was therefore invisible to the aggregator, and the job exited 0, which the surrounding scheduler interpreted as complete success.

This is the specific code path that Action Item 1 (Anchor publisher upgrade) is intended to close: delivery confirmation needs to be tracked per store rather than per batch, retry logic needs to target only unacknowledged stores, and the top-level status check needs to require full-fleet confirmation — not merely the absence of a fatal exception — before logging success. The March 2026 upgrade proposal, reviewed as part of this postmortem, already specified all three changes; it was deferred for unrelated roadmap prioritization reasons both times, and no compensating control was put in place in the interim to cover the risk the upgrade was meant to address.

## Appendix B: Waypoint Stacking Mechanism

Waypoint applies loyalty and promotional discounts at the terminal based on a locally cached promotion table that references item price as of the last confirmed Anchor publication. Under normal operation, when Anchor publishes a price change for an item that also carries an active promotion, the same publication includes an updated exclusion or adjustment flag so that Waypoint either suspends the promotion for that item or recalculates the discount off the new base price, depending on the promotion type.

Because batch seven's stores received the price change for approximately 2,900 items but did not receive the corresponding exclusion/adjustment flags (which were sequenced later in the same file and fell after the point of transmission failure), Waypoint on those controllers continued to apply promotions calculated against the old, higher list price, while the register was simultaneously charging the new, lower list price as the base. In cases where an item carried a straightforward percentage-off or dollar-off promotion, this produced a final price equal to the new (already reduced) list price minus a discount that should only have applied to the old, higher price — in effect, double-counting the price reduction. The energy drink case reported from Plattsburgh involved a combination of a list price reduction from $2.29 to $1.49 and a "buy more, save more" case-quantity promotion that, applied against the un-adjusted baseline, drove the effective per-unit price to $0.61.

This mechanism is specific to promotions calculated as relative discounts against list price. Flat-price promotions and fixed-bundle pricing were not affected in the same way, which is part of why the mispricing, while widespread, did not affect all 2,900 repriced items uniformly — Finance's reconciliation found that of the 2,900 items with changed prices in the partial file, 1,140 also carried active promotions eligible for stacking, and it is this subset that accounts for the large majority of the $312,000 in undercharges.

## Appendix C: Financial Reconciliation Methodology

Finance's calculation of the $312,000 undercharge figure used the following method, applied per affected transaction line item:

1. Identify the 118 affected store IDs and the transaction window from 12:03 a.m. Saturday (first controller ingestion of the partial file) through 11:50 p.m. Saturday (point-of-sale restoration).
2. For each transaction line item within that window at an affected store, compare the price actually charged (from the point-of-sale journal) against the price that should have been charged under the correct, fully-confirmed price file plus correctly-applied loyalty exclusions (reconstructed from the corrected file distributed during remediation).
3. Sum the per-line differences where the actual charge was lower than the correct charge, excluding differences attributable to unrelated, previously-approved markdowns or clearance pricing not connected to this incident.

This produced the count of 41,300 mispriced transactions and the $312,000 undercharge figure. The $88,000 in refunds reflects a separate, narrower calculation: refunds were issued only where a customer contacted the company directly, where a transaction was flagged by a store manager as needing correction at the time, or where loyalty-account-linked purchases could be identified and proactively adjusted. The gap between the $312,000 undercharge and the $88,000 refunded does not represent unresolved consumer harm in the ordinary sense — undercharges by definition benefited the purchasing customer rather than harming them financially — but it is the figure most relevant to the weights-and-measures inquiry, which concerns pricing accuracy and compliance rather than customer financial loss.

The $1.1 million lost-sales estimate was calculated separately by comparing per-store, per-hour sales for the outage window (8:10 p.m.–11:50 p.m.) against a blended baseline of the same stores' performance over the same hours on the preceding four Saturdays, adjusted for the fact that this was a notably higher-traffic date on the promotional calendar. Finance flagged this figure as an estimate with a wider confidence interval than the undercharge figure, given the inherent uncertainty in modeling foregone sales rather than measuring completed transactions.

## Appendix D: Store-Level Accounts

As part of this review, Store Operations collected brief accounts from a sample of 14 of the 118 affected store managers describing how their location handled the outage window. These accounts are summarized, not attributed to individual stores, to inform Action Item 6.

Several stores held all in-progress transactions and asked customers to wait, resuming once systems were restored; this worked reasonably well at lower-traffic locations but produced long lines and some abandoned baskets at busier sites. Other stores shifted immediately to cash-only sales, using handwritten receipts or, in a few cases, a store's backup manual credit card imprinter retained from a prior system migration — a device most staff on shift that night had never used and had to be walked through by phone. At least two stores report having given away certain items rather than manage manual pricing under pressure, unable to quickly determine correct prices without a working terminal or current price book in hand. One store manager reported calling a neighboring location to ask what price to charge for fuel-adjacent convenience items, since the store's own posted shelf tags were understood to be unreliable given the day's earlier anomaly reports.

No two stores handled the outage identically, and several managers independently noted in their accounts that a short printed reference — even a single page of "if systems are down, do this" guidance — would have resolved much of the on-the-spot improvisation. This feedback directly informs the scope of Action Item 6.

## Appendix E: Glossary

**Anchor** — Northway's price-book publication system, responsible for distributing nightly pricing updates from the Latham support center to in-store controllers.

**Waypoint** — Northway's loyalty and promotions engine, responsible for applying member discounts and promotional pricing at the point-of-sale terminal.

**Batch** — A grouping of stores, organized by network distribution segment, to which the Anchor publication job transmits price files as a unit.

**Exclusion flag** — A data element normally published alongside a price change, instructing Waypoint to suspend or recalculate a promotion for a given item to prevent discount stacking on a newly changed price.

**Controller** — The in-store computing system that receives published price files from Anchor and coordinates point-of-sale terminal behavior, including communication with Waypoint.

**Weights and Measures** — The New York State regulatory authority responsible for oversight of retail pricing and measurement accuracy, whose inquiry into this incident opened December 11, 2026, and remains open as of the date of this report.

---

*This postmortem and its appendices are maintained by Retail Technology and are subject to update as remediation items close and as the state inquiry progresses. Questions regarding this document should be directed to Nia Broadwater, Director of Retail Technology.*
