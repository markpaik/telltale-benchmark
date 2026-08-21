# Incident Postmortem: PRB-2026-1204 — Anchor Partial Price Book Publish and Point-of-Sale Outage

**Document classification:** Internal — Blameless Postmortem
**Incident ID:** PRB-2026-1204
**Severity:** SEV-1
**Incident dates:** Friday, December 4 – Sunday, December 6, 2026
**Author:** Retail Technology Incident Review Group
**Reviewed by:** Nia Broadwater (Director, Retail Technology); Fatima Zubairi (VP, Store Operations); Doug Pelletier (Manager, Point-of-Sale Engineering)
**Postmortem review meeting:** December 16, 2026, Latham Support Center
**Distribution:** Executive team, Retail Technology, Store Operations, Finance, Legal & Compliance, Loss Prevention, Customer Care
**Status:** Final

---

## 1. Purpose and Ground Rules

This document records what happened during the December 4–6, 2026 price book and point-of-sale incident, why it happened, how the organization responded, and what we will change so it does not happen again.

This is a blameless postmortem. Every person named in this document acted in good faith, with incomplete information, under time pressure, inside systems and processes that the organization built and maintained. Where this document describes a decision that turned out badly, the question we ask is not "who made the mistake?" but "why did the system make that decision look reasonable at the time, and what would have to be true for a different decision to have been made?" Individuals are named so the record is accurate and so action-item ownership is clear — not to assign fault. The failures described here are failures of system design, alerting hygiene, change governance, and documentation. Any of the engineers on the current rotation would likely have made the same calls given the same inputs.

---

## 2. Executive Summary

At 11:40 p.m. on Friday, December 4, 2026, the nightly price book publishing job in Anchor — the system of record that distributes item pricing to in-store controllers across Northway Fuel and Provisions' 190 locations — failed partway through its run but reported success to its own job monitor and to the operations dashboard. One hundred eighteen stores received a partial file containing new prices for approximately 2,900 items but **not** the matching loyalty exclusion records that normally accompany a price change. As a result, Waypoint, the loyalty engine that applies discounts at the point-of-sale terminal, treated the already-reduced prices as full-price items still eligible for active promotions and stacked loyalty discounts on top of them. Some items sold for a small fraction of intended retail — most visibly, single energy drinks ringing at 61 cents.

The mispricing ran undetected for approximately 19 hours, through the entirety of Saturday's business day at the 118 affected stores, on the busiest weekend of the fiscal quarter. Detection ultimately came not from any monitoring system but from a Plattsburgh district manager who called the support center at 6:15 p.m. Saturday after a customer purchased 40 cases of energy drinks at 61 cents per can.

The on-call engineer, Miguel Arellano, investigated with the information available to him: Anchor's dashboard showed the Friday publish as successful, and the visible symptom — improbable discounts at the register — pointed at the loyalty engine. He concluded Waypoint was misfiring and, at 8:10 p.m., disabled it by pushing a null promotion table to the in-store controllers. The controllers were not designed to accept an empty table; they treated it as a schema validation failure and entered a fault state, taking point-of-sale fully offline at all 118 affected stores for three hours and forty minutes on a Saturday evening. Store teams improvised cash-only operations with paper logs and hand calculations; many suspended fuel sales entirely because pump authorization runs through the POS.

Doug Pelletier, manager of point-of-sale engineering, was paged at 9:05 p.m. and identified the partial Anchor file as the true root cause. Nia Broadwater, Director of Retail Technology, assumed incident command at 9:30 p.m. A verified full republish of the price book and promotion tables restored point-of-sale by 11:50 p.m. Fatima Zubairi, VP of Store Operations, coordinated store communications throughout the outage window, and Renee Saint-Fleur's customer care team absorbed roughly 2,100 calls on Sunday.

The total accounted impact: **41,300 mispriced transactions, $312,000 in undercharges, $88,000 in customer refunds and goodwill payments, approximately 26,000 lost transactions during the POS outage, and an estimated $1.1 million in lost sales.** The New York State Bureau of Weights and Measures opened an inquiry on December 11.

Three latent conditions turned a routine job failure into a SEV-1: the Anchor publisher upgrade that would have added transactional (all-or-nothing) publishing was deferred twice from its March 2026 date; the queue-depth alert that fired at the moment of failure was routed to the mailbox of an engineer who left the company in August 2025 and was seen by no one; and the rollback runbook, last edited in 2023, referenced a tool decommissioned in 2024, leaving the on-call engineer to improvise the Waypoint disable that caused the outage.

---

## 3. Impact

### 3.1 Financial and Transactional Impact

| Metric | Value |
|---|---|
| Stores affected (partial price file) | 118 of 190 |
| Stores affected (POS outage) | 118 |
| Items published with incorrect effective pricing | ~2,900 |
| Mispriced transactions (mispricing window, ~19 hours) | 41,300 |
| Gross undercharges (goods sold below intended retail) | $312,000 |
| Customer refunds and goodwill payments issued | $88,000 |
| POS outage duration | 3 hours 40 minutes (8:10 p.m. – 11:50 p.m. Saturday) |
| Estimated transactions lost during outage | ~26,000 |
| Estimated lost sales (outage + suspended fuel + Sunday softness) | $1.1 million |
| Customer care call volume, Sunday, December 6 | ~2,100 calls |
| Manual cash-handling reconciliation variance (net, all stores) | $6,340 under-deposit, still under review |
| Regulatory exposure | NYS Weights and Measures inquiry opened December 11, 2026 |

### 3.2 Operational Impact

- **Store teams:** 118 stores operated for up to 3 hours 40 minutes without registers, on the highest-volume Saturday evening of the quarter, using improvised paper procedures with no company-issued playbook. Approximately 70 stores suspended fuel sales for some or all of the outage because pump pre-authorization could not be completed.
- **Employees:** Store staff absorbed significant customer frustration at the counter. Several district managers reported employees staying past scheduled shifts to complete manual reconciliation. No safety incidents were reported, though four stores reported verbal confrontations with customers turned away at the pumps.
- **Customer trust:** Sunday's 2,100 care calls included customers charged incorrectly during manual operations, customers seeking honored "advertised" (mispriced) prices, and loyalty members whose Waypoint accounts showed anomalous point activity. Social media posts advertising the 61-cent energy drinks circulated Saturday afternoon and drew opportunistic bulk-buying traffic to at least nine stores before the outage.
- **Regulatory:** The mispricing — specifically, discrepancies between shelf tags and register prices in both directions during the incident and the manual period — triggered the state inquiry. Legal & Compliance is coordinating the response as a tracked action item (AI-14).

### 3.3 What Was Not Impacted

- The 72 stores that had not yet pulled the nightly file when the publish failed operated normally throughout.
- No payment card data, loyalty account data, or personally identifiable information was exposed. This was a pricing-integrity and availability incident, not a security incident.
- Fuel price signs, which publish through a separate channel, were unaffected; fuel *dispensing* was affected only by the POS outage.

---

## 4. Timeline

All times Eastern. Sources: Anchor job logs, controller sync logs, Waypoint transaction records, PagerDuty history, incident bridge notes, and interviews conducted December 8–12.

### Friday, December 4, 2026

**11:40 p.m.** — The Anchor nightly price book publish job begins its distribution phase. Approximately 40% through serialization, the job's message queue stalls on a malformed record batch. The publisher's worker process exhausts its retry budget, drops the remaining queue contents — which include the loyalty exclusion records tied to the night's 2,900 price changes — and exits. Due to a known defect in the publisher's completion handler (the defect the deferred March 2026 upgrade was scheduled to fix), the job writes a `SUCCESS` status because the *distribution* step technically completed for the records that made it into the output file. The operations dashboard shows green.

**11:52 p.m.** — Anchor's queue-depth monitor detects the stalled-then-dropped queue and fires an alert email. The alert routes to the personal work mailbox of an engineer who left the company in August 2025. The mailbox is inactive but not disabled; the mail is delivered and read by no one. No secondary route, escalation, or paging integration exists for this alert.

### Saturday, December 5, 2026

**12:05 a.m. – 1:30 a.m.** — In-store controllers at 118 stores complete their scheduled nightly sync and ingest the partial file. The file passes controller-side validation: it is well-formed, correctly signed, and internally consistent. The controllers have no mechanism to know that companion exclusion records are missing, because the file format does not carry a manifest or record count for the full intended payload. The remaining 72 stores were scheduled for a later sync window and, because the publisher had already exited, received no file and retained the prior day's complete price book.

**5:00 a.m. – 6:30 a.m.** — Affected stores open. New reduced prices are live at the shelf edge and the register. Waypoint, receiving no updated exclusion table, continues applying active promotions — multi-buy deals, member discounts, and a December energy-drink promotion — on top of the already-reduced base prices.

**Morning – afternoon** — Mispriced transactions accumulate: roughly 41,300 across the day. Notably, no automated control flags the pattern. Anchor shows green. Waypoint is operating exactly as designed against the data it has. Store-level margin reporting runs on a next-day batch cycle. Loss-prevention exception reporting, which flags unusual discount depth, also runs next-day. Several store employees later reported noticing "really good deals" on specific items during the day; none escalated, and no procedure asks them to.

**~2:00 p.m. – 6:00 p.m.** — Social media posts about deeply discounted energy drinks begin circulating regionally. Bulk-purchasing behavior appears at multiple stores; at least nine stores see customers buying by the case.

**6:15 p.m.** — **Detection.** The Plattsburgh district manager calls the support center: a customer has just purchased 40 cases of energy drinks at 61 cents per can. The support center logs the ticket as a pricing discrepancy.

**6:38 p.m.** — The ticket is escalated to the Retail Technology on-call rotation. Miguel Arellano acknowledges the page.

**6:45 p.m. – 8:00 p.m.** — Arellano investigates. He checks the Anchor dashboard first: the Friday publish shows `SUCCESS`. He pulls sample transactions from three affected stores and confirms the symptom — promotions applying on top of reduced prices. With Anchor apparently healthy and the visible anomaly living entirely in the discount logic, the evidence points to Waypoint. He consults the price-and-promotion rollback runbook, last edited in 2023. Its primary rollback procedure names a promotion-management tool that was decommissioned in 2024; the documented commands fail against systems that no longer exist. With Saturday-evening transaction volume climbing and money visibly leaving the building on every mispriced sale, Arellano determines the fastest available lever is to disable Waypoint by pushing a null (empty) promotion table to the affected controllers — a technique used once before in a 2024 test environment, never validated in production.

**8:10 p.m.** — **Outage begins.** The null promotion table publishes to the 118 affected stores. The controller firmware treats an empty promotion table as a schema validation failure — a condition its designers assumed indicated file corruption — and enters a protective fault state that halts all transaction processing. Point-of-sale goes fully offline at all 118 stores. Because pump pre-authorization routes through the POS, fuel dispensing halts as well except where stores use manual pump authorization.

**8:15 p.m. – 8:45 p.m.** — Store calls flood the support center. Stores begin improvising: some close entirely; most shift to cash-only sales with hand-written logs and shelf-tag prices totaled on calculators; roughly 70 stores suspend fuel sales. There is no company-issued offline-operations kit or procedure, so practices vary widely store to store (see Section 7.3).

**9:05 p.m.** — Doug Pelletier, manager of point-of-sale engineering, is paged and joins. This is the first management-level page of the incident, 2 hours 27 minutes after the initial escalation, because the paging policy at the time required management escalation only when the on-call engineer requested it or when an outage ticket (as distinct from a pricing ticket) was opened.

**9:20 p.m.** — Pelletier pulls the raw Anchor publish logs — not the dashboard — and identifies the truncated distribution run: the output file contains price records but is missing the entire exclusion block. Root cause is now understood: **partial publish reported as success**, not a Waypoint malfunction. He also identifies why the controllers faulted on the null table.

**9:30 p.m.** — Nia Broadwater, Director of Retail Technology, assumes incident command and opens a formal bridge. Incident is declared SEV-1. Workstreams established: (1) restore POS, (2) republish correct price book and promotion data, (3) store operations and communications, (4) financial exposure tracking.

**9:40 p.m.** — Fatima Zubairi, VP of Store Operations, joins the bridge and takes ownership of store-facing communication. First consolidated guidance to stores goes out at 9:55 p.m.: remain cash-only if safe to operate, log all sales on paper with item and amount, secure cash in drop safes hourly, do not attempt controller restarts, and managers may close at their discretion with district-manager notification.

**10:05 p.m.** — Recovery plan finalized: rebuild the full price book and promotion/exclusion tables from Anchor's source data, verify record counts against the source of truth *before* distribution, then publish in three store waves with a five-store canary.

**10:20 p.m.** — Full rebuild completes. Engineering manually reconciles record counts against Anchor's database — the verification step the publisher itself does not perform.

**10:45 p.m.** — Canary wave: five stores receive the corrected full file. Controllers clear the fault state on ingesting a valid promotion table, and POS resumes at all five. Test transactions confirm correct pricing and correct promotion behavior.

**11:00 p.m. – 11:50 p.m.** — Remaining stores restored in two waves. **11:50 p.m. — Outage ends.** All 118 stores confirm POS online with correct pricing. Total outage: 3 hours 40 minutes.

### Sunday, December 6, 2026

**12:15 a.m.** — Incident downgraded to SEV-2 (recovery/reconciliation). Bridge closes; recovery channel remains open.

**8:00 a.m.** — Renee Saint-Fleur's customer care team opens with surge staffing pulled together overnight; the team fields approximately 2,100 calls during the day covering refund requests, disputed manual-sale charges, and loyalty account questions.

**9:00 a.m.** — Finance and Loss Prevention begin transaction reconciliation: quantifying undercharges from the mispricing window and auditing paper logs and cash deposits from the manual period.

**All day** — Stores submit manual sale logs and cash reconciliation sheets. Initial variance: $6,340 net under-deposit across all affected stores, within a plausible range for untrained manual operations at this volume; review continues.

### Follow-on Dates

**December 7** — Refund and goodwill process stood up; $88,000 ultimately issued.
**December 8–12** — Postmortem interviews and log analysis.
**December 11** — New York State Bureau of Weights and Measures opens an inquiry into pricing accuracy at affected stores.
**December 16** — Postmortem review meeting; action items ratified.

---

## 5. Root Cause

**The Anchor nightly publisher can fail partway through a run and report success, and no downstream system verifies that the published payload is complete.**

The publish job's completion handler evaluates only whether the distribution step exited without an unhandled exception. When the message queue stalled and the worker dropped the remaining records — including every loyalty exclusion tied to that night's price changes — the distribution step still "completed" for the truncated payload, and the job wrote `SUCCESS`. This defect was known: it is item ANC-1147 in the Anchor backlog, and fixing it (by making publishes transactional — all records commit or none do — with checksummed manifests) was a headline feature of the publisher upgrade originally scheduled for March 2026.

The partial payload was dangerous in a specific way: **prices and their exclusions travel as separable record types in the same file, with the exclusions serialized last.** A truncation therefore produces the worst possible partial state — new low prices without the guardrails that tell Waypoint not to discount them further. A file format with a manifest, or a controller-side completeness check, or exclusions serialized *before* the prices they protect, would each independently have prevented the stacking behavior.

Everything downstream behaved correctly against bad data. The controllers validated and ingested a well-formed file. Waypoint applied active promotions to items its exclusion table said were eligible. The registers rang what they were told. The root cause is not any of those systems; it is that the pipeline's single source of truth about "did the publish work?" was a status flag that could lie.

---

## 6. Contributing Factors

Root cause explains why the incident *started*. The following factors explain why it *lasted 19 hours*, why the first response *made it worse*, and why the organization was *positioned* for this failure.

### 6.1 The Deferred Publisher Upgrade (why the defect still existed)

The Anchor publisher upgrade containing the transactional-publish fix was scheduled for March 2026. It was deferred twice: first in February 2026 to prioritize the loyalty program relaunch, and again in June 2026 due to a staffing gap after two platform engineers moved to the Waypoint integration team. Both deferrals were made through the normal quarterly planning process. Critically, **neither deferral decision was accompanied by a risk assessment of what the upgrade fixed.** The upgrade was tracked as a "platform modernization" item; ANC-1147, the false-success defect, was buried in its scope and never surfaced to the planning forum as an open production risk. The organization deferred a risk it did not know it was carrying. This is a governance gap, not a judgment failure by any individual planner.

### 6.2 The Orphaned Alert (why nobody knew at 11:52 p.m. Friday)

The one monitoring signal that fired at the moment of failure — the queue-depth alert — went to a departed engineer's mailbox. When that engineer left in August 2025, offboarding disabled their accounts per policy, but the *mailbox* was retained for mail-forwarding continuity, and no process audited alert destinations against active staff. The alert had no team distribution list, no paging integration, and no escalation path. A review conducted during this postmortem found **31 additional alerts across Retail Technology routed to individual mailboxes rather than team channels, of which 6 belong to former employees.** This is a systemic hygiene problem: the alert worked; the wiring was broken.

### 6.3 The Detection Gap (why 19 hours passed)

With the orphaned alert lost, every remaining detection layer operated on a next-day cycle:

- **Margin and exception reporting** runs as an overnight batch; Saturday's mispricing would have surfaced in reports on Sunday morning — after the damage.
- **No real-time pricing anomaly detection exists.** Nothing watches for transactions ringing significantly below cost, sudden shifts in average discount depth, or bulk purchases of single SKUs.
- **Store employees had no channel or mandate to report pricing anomalies.** Several noticed unusual prices; the culture and procedure treat register prices as authoritative, so "the system says 61 cents" reads as "the price is 61 cents." The eventual detection came from a district manager exercising judgment outside any defined process — which means detection was luck.

The 19-hour gap was not a failure to react to a signal; it was the absence of any signal reaching a human.

### 6.4 The False-Success Dashboard (why the on-call diagnosis went wrong)

When Arellano investigated, the Anchor dashboard — the tool the on-call rotation is trained to trust first — showed the publish as successful. This single false datum eliminated the true root cause from consideration and pointed the investigation at Waypoint, the system where the symptom was visible. Pelletier reached the correct diagnosis 15 minutes after joining not because of superior reasoning but because of privileged knowledge: he knew from prior work that the dashboard status could be unreliable and went straight to raw logs. **Diagnostic knowledge that lives in one person's head is a single point of failure**, and the on-call engineer cannot be faulted for trusting the instrumentation the organization gave him.

### 6.5 The Stale Runbook and the Improvised Disable (why the fix caused an outage)

The rollback runbook for pricing and promotion incidents was last edited in 2023 and names a promotion-management tool decommissioned in 2024. When Arellano opened it under pressure, its primary procedure was inoperable. With no valid documented path and financial loss accruing every minute, he improvised the null-promotion-table push — a technique observed once in a 2024 test environment. Nothing in any document warned that controllers treat an empty promotion table as corruption and fault-stop. The controller behavior itself is defensible in isolation (fail safe on suspect data); the *combination* of an undocumented safe-disable path and an unvalidated improvised one is the gap. **When runbooks decay, on-call engineers don't stop acting — they act without a map.**

### 6.6 Delayed Escalation and Late Incident Command

Formal incident command began at 9:30 p.m. — nearly three hours after detection and 80 minutes after the outage began. The paging policy in force treated the initial event as a pricing ticket, not an outage, and left management escalation to the on-call engineer's discretion. A solo engineer working a complex, ambiguous, financially bleeding incident on a Saturday evening is exactly the situation where a second set of eyes changes outcomes; the policy did not provide one until the situation had already escalated itself.

### 6.7 Timing and Seasonal Load

The failure occurred entering the quarter's busiest weekend, which amplified every dimension: more mispriced transactions per hour, more lost sales per outage minute, more customers in stores during manual operations, and more social-media velocity for the 61-cent discovery. Timing is not a cause, but it converted a serious incident into a seven-figure one.

---

## 7. Response Assessment

### 7.1 What Worked

1. **The district manager's escalation.** The Plattsburgh DM recognized that a 40-case, 61-cent purchase was a system problem, not a promotion, and called it in immediately. This judgment — exercised without a procedure requiring it — ended the mispricing window.
2. **Rapid true-root-cause identification once escalated.** Pelletier isolated the truncated publish within 15 minutes of joining. The raw logs contained everything needed; the diagnostic path existed, even if it wasn't the trained one.
3. **Disciplined recovery once incident command stood up.** Broadwater's bridge imposed structure quickly: parallel workstreams, a verified rebuild with manual record-count reconciliation, and a canary wave before full redistribution. The canary caught nothing wrong, but the decision to use one — resisting pressure to blast the fix to all 118 stores at once — was correct and is the pattern to institutionalize. From incident command to full restoration took 2 hours 20 minutes.
4. **Store operations communication.** Zubairi's consolidated 9:55 p.m. guidance replaced 118 stores' worth of improvisation with a common minimum standard (cash-only rules, paper logging, hourly safe drops, manager closure discretion) within 25 minutes of her joining. District managers relayed effectively; interviews confirmed most stores received and followed it.
5. **Customer care surge.** Saint-Fleur assembled Sunday surge staffing overnight with no pre-existing surge playbook and absorbed 2,100 calls with average wait times peaking at 14 minutes — imperfect, but far better than the abandonment cliff that volume would normally cause. The empowerment decision (frontline agents authorized to issue refunds up to $50 without escalation) resolved most calls on first contact.
6. **Store teams' improvisation and honesty.** With no offline kit and no training, most stores kept serving customers safely, and the manual-period cash reconciliation variance ($6,340 net across 118 high-volume stores) is remarkably small. Employees stayed late to complete paperwork. This goodwill is an asset the organization spent and must not treat as a plan.

### 7.2 What Did Not Work

1. **Detection depended entirely on a customer buying 40 cases of energy drinks.** Every automated layer failed or didn't exist: the alert was orphaned, the dashboard lied, exception reporting was next-day, and no real-time anomaly detection watches transactions.
2. **The first remediation caused a larger incident than the one it addressed.** The Waypoint disable converted a mispricing problem (real but bounded — roughly $16,000/hour in undercharges) into a full POS outage (roughly $300,000/hour in lost sales). This is the predictable output of a stale runbook plus a false dashboard plus a solo responder — not an individual error.
3. **The escalation policy left one engineer alone too long.** 2 hours 27 minutes elapsed between on-call acknowledgment and the first management page; incident command followed only 25 minutes later. Structure arrived after the worst decision point had already passed.
4. **No documented safe-disable path for Waypoint existed.** "Turn off the loyalty engine" is an obvious operational need; the fact that the only known method was an unvalidated null-table push discovered in a test environment is a design and documentation gap.
5. **No offline-operations playbook for stores.** Improvised practices varied dangerously: a minority of stores initially estimated prices from memory rather than shelf tags, some did not log sales at all for the first 30–40 minutes, and fuel-suspension decisions were inconsistent, producing the customer confrontations noted in Section 3.2.
6. **Financial-exposure tracking started late.** Undercharge quantification did not begin until Sunday morning, meaning refund/honor decisions during the Saturday-night bridge were made without numbers.

### 7.3 The Improvised Cash Handling — Detail and Assessment

Because this incident will not be the last POS outage, the manual period deserves specific examination.

Between 8:10 p.m. and the arrival of consolidated guidance at 9:55 p.m., stores self-organized. Observed patterns from district-manager reports and reconciliation review:

- **~80 stores** went cash-only using shelf-tag prices, hand-totaled on calculators, with sales recorded on whatever paper was available — notebook pages, delivery invoices, receipt-tape backs. Log quality varied from itemized lists to single running totals.
- **~70 stores** suspended fuel sales; a small number with staff who knew manual pump authorization continued fuel with attendant-controlled dispensing.
- **~15 stores** closed outright, generally single-coverage stores where the manager judged cash-only operation unsafe at Saturday-night volume.
- **A handful of stores** initially rounded prices from memory rather than checking shelf tags — the practice most exposed to the weights-and-measures inquiry, since it produced both under- and over-charges relative to posted prices.
- Cash security was generally good: hourly drop-safe practice was widely followed after the 9:55 p.m. guidance, and no losses or safety incidents occurred.

Assessment: store teams performed admirably with nothing to work from, and the small net reconciliation variance reflects that. But the variance in practice — especially unlogged sales and estimated pricing — created regulatory exposure, refund disputes (a meaningful share of Sunday's 2,100 calls), and accounting gaps we cannot fully close. The organization owes stores a real offline kit, a defined price authority (shelf tags), pre-printed log sheets, and a trained decision tree for cash-only versus closure. That is action item AI-9.

---

## 8. Action Items

Owners named below are accountable for delivery, not implicated in the incident. Due dates were ratified at the December 16 review. Nia Broadwater will track all items in the incident action register with monthly status reporting to the executive team until closure.

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| AI-1 | **Complete the Anchor publisher upgrade**, including transactional (all-or-nothing) publishing, checksummed manifests, and elimination of the false-success completion handler (ANC-1147). No further deferral without executive sign-off per AI-12. | Doug Pelletier | Feb 27, 2027 | Critical |
| AI-2 | **Interim publish verification (stopgap until AI-1):** automated post-publish reconciliation comparing published record counts and checksums, by record type, against Anchor's database, with a hard failure page if counts mismatch. Deployed to production. | Sanjay Kotecha, Anchor Platform Lead | Dec 24, 2026 | Critical |
| AI-3 | **Controller-side completeness check:** controllers reject and page on files whose manifest is absent or whose record-type counts don't match the manifest, retaining the prior known-good price book. Requires AI-1 manifest format; firmware rollout in waves. | Doug Pelletier | Apr 15, 2027 | High |
| AI-4 | **Alert routing audit and remediation:** re-route all 31 individually-addressed alerts (including the 6 orphaned ones) to team paging channels with escalation policies; establish a quarterly automated audit that flags any alert destination not tied to an active on-call rotation; add alert-destination review to the IT offboarding checklist. | Erin Delgado, IT Service Management Lead | Jan 15, 2027 | Critical |
| AI-5 | **Real-time pricing anomaly detection:** production alerting on transactions ringing below item cost, discount depth exceeding thresholds, and single-SKU bulk-purchase patterns, paging the Retail Technology on-call within 15 minutes of threshold breach. | Nia Broadwater | Mar 31, 2027 | High |
| AI-6 | **Runbook remediation program:** rewrite and live-validate (in the staging environment against production-equivalent controllers) the pricing rollback and promotion-disable runbooks by the near-term date; institute quarterly runbook validation with a "last validated" date visible on every runbook and automatic staleness flags at 6 months. | Doug Pelletier | Jan 31, 2027 (rewrite); ongoing quarterly | Critical |
| AI-7 | **Engineered Waypoint safe-disable:** build and document a supported "promotions off" mode in which Waypoint returns zero-discount responses while POS continues transacting at base price; validate in staging and one pilot store; deprecate the null-table technique with an explicit warning in tooling. | Priya Raghunathan, Waypoint Integration Lead | Feb 13, 2027 | Critical |
| AI-8 | **Incident escalation policy revision:** any pricing-integrity incident affecting more than 10 stores auto-pages the engineering manager alongside the on-call engineer; any customer-facing outage auto-declares SEV-1 and pages the incident-commander rotation; no solo response beyond 45 minutes on multi-store incidents. Policy published and drilled. | Nia Broadwater | Jan 9, 2027 | Critical |
| AI-9 | **Store offline-operations kit:** pre-positioned kit at all 190 stores containing pre-printed manual sale logs, cash-only procedure card designating shelf tags as sole price authority, fuel suspension/manual-authorization decision tree, safe-drop cadence, and closure criteria; incorporated into new-hire and manager training; tabletop-drilled once per store by the due date. | Fatima Zubairi | Feb 28, 2027 | High |
| AI-10 | **Customer care surge playbook:** documented surge-staffing tree, pre-approved refund authority matrix (formalizing the $50 frontline authority used December 6), incident-specific IVR messaging templates, and a defined intake path for pricing-incident disputes. | Renee Saint-Fleur | Jan 30, 2027 | Medium |
| AI-11 | **Store-employee pricing-anomaly reporting channel:** a one-tap report in the store manager app routing suspected pricing errors to the support center with automatic pattern detection across stores (3+ stores reporting the same SKU pages on-call); paired with communication that reporting anomalies is expected, not exceptional. | Fatima Zubairi | Mar 13, 2027 | Medium |
| AI-12 | **Change-deferral governance:** any deferral of a scheduled system change must document the production risks the change addresses; deferral of changes carrying known SEV-1-class defects requires VP-level sign-off with the defect explicitly named. Retroactive risk review of all currently deferred Retail Technology changes. | Nia Broadwater | Jan 23, 2027 | High |
| AI-13 | **Financial-exposure workstream in incident process:** SEV-1 incidents with pricing or revenue impact activate a Finance on-call to produce running exposure estimates on the bridge within 60 minutes of declaration. | Colleen Vasquez, Director of Finance Operations | Feb 6, 2027 | Medium |
| AI-14 | **Weights-and-measures inquiry response:** compile the pricing-accuracy record for the inquiry (mispricing window transactions, manual-period practices, remediation evidence including this postmortem and AI-1 through AI-3); single point of contact for the Bureau. | Tomas Okafor, Legal & Compliance | Per Bureau schedule; internal package by Jan 9, 2027 | Critical |
| AI-15 | **Dashboard truth audit:** review all Retail Technology operational dashboards for status indicators derived from self-reported job status rather than verified outcomes; remediate or clearly label any indicator that cannot be trusted as ground truth. | Sanjay Kotecha | Mar 6, 2027 | Medium |

---

## 9. Lessons

Five lessons generalize beyond this incident:

1. **A system that can fail while reporting success is worse than one that fails loudly.** The green dashboard did not merely fail to help; it actively misdirected the response. Verification must measure outcomes, not job exit codes.
2. **Alerting is infrastructure, and it decays.** An alert routed to a departed employee is functionally identical to no alert, and nothing in our operations told us the difference for sixteen months. Alert destinations must be audited like any other production dependency.
3. **Deferral decisions must know what they are deferring.** The March upgrade was postponed twice as "modernization." Had either planning session seen "this fixes a defect where the price book can partially publish and report success," the calculus would likely have differed. Risk must travel with the work item.
4. **Runbooks are load-bearing at exactly the moment nobody is checking them.** An engineer under pressure will act; the only question is whether the organization has given them a validated path or left them to improvise. The runbook's staleness, not the engineer's improvisation, is the correctable failure.
5. **Frontline judgment was our only working detection layer — and our best recovery asset.** A district manager's phone call, store teams' disciplined improvisation, and empowered care agents carried this incident. The action plan aims to give those people real tools and channels rather than continuing to rely on their unsupported good judgment.

---

## Appendix A: Systems Referenced

| System | Function |
|---|---|
| **Anchor** | Price book system of record; publishes item pricing and loyalty exclusion records nightly to in-store controllers. |
| **In-store controllers** | Per-store devices that ingest the nightly price book, serve prices to POS terminals, and gate pump authorization. |
| **Waypoint** | Loyalty engine; evaluates promotion and member-discount eligibility per transaction at the terminal, governed by the exclusion table. |

## Appendix B: Key Metrics Summary

- Mispricing window: ~19 hours (11:40 p.m. Dec 4 – 6:38 p.m. Dec 5 escalation)
- POS outage: 3 hours 40 minutes (8:10 p.m. – 11:50 p.m. Dec 5)
- Detection-to-incident-command: 3 hours 15 minutes
- Incident-command-to-restoration: 2 hours 20 minutes
- Total quantified financial impact: ~$1.5 million ($312K undercharges + $88K refunds + $1.1M lost sales)

## Appendix C: Interview and Evidence Sources

Anchor publish and job-monitor logs (Dec 4–5); controller sync and fault logs, 118 affected stores; Waypoint transaction records for the mispricing window; PagerDuty acknowledgment and escalation history; incident bridge recording and scribe notes; store manual-sale logs and cash reconciliation sheets; customer care call dispositions (Dec 6); interviews with M. Arellano, D. Pelletier, N. Broadwater, F. Zubairi, R. Saint-Fleur, the Plattsburgh district manager, and eleven store managers, conducted December 8–12, 2026.

---

*This postmortem was reviewed and accepted at the December 16, 2026 incident review. Action-item status will be reported monthly to the executive team until all items are closed. Questions regarding this document should be directed to the Retail Technology Incident Review Group.*
