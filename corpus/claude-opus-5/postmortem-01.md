# Incident Postmortem: Price Book Publishing Failure and Point-of-Sale Outage

**Incident ID:** INC-2026-1204-01
**Severity:** SEV-1
**Systems Involved:** Anchor (price book publishing), Waypoint (loyalty and promotions engine), in-store controllers, point-of-sale terminals
**Stores Affected:** 118 of 190
**Incident Window:** December 4, 2026, 23:40 EST — December 6, 2026, 14:20 EST
**Document Owner:** Nia Broadwater, Director of Retail Technology
**Review Date:** December 18, 2026
**Distribution:** Executive Leadership Team, Retail Technology, Store Operations, Finance, Legal, Customer Care, District Management

---

## 1. Summary

On the night of Friday, December 4, 2026, the nightly Anchor price book publishing job failed partway through its run and reported a successful completion to its monitoring interface. The job had transmitted an incomplete payload to 118 of 190 in-store controllers: new prices for 2,900 items, without the accompanying loyalty exclusion table that instructs the Waypoint promotions engine which items are ineligible for further discounting.

The absence of that exclusion table did not cause Waypoint to fail. It caused Waypoint to behave exactly as designed under a condition its design did not anticipate. With no exclusions present, Waypoint treated every item in the price book as promotion-eligible and stacked active loyalty offers on top of prices that had already been reduced for the December promotional cycle. Discounts compounded. A 12-pack of energy drinks with a shelf price of $12.99, marked to $8.99 for the December cycle, then discounted 40 percent by a category offer, then reduced again by a member-tier multiplier and a fuel-points conversion, rang at $0.61 per unit.

The condition persisted, undetected by any automated system, for nineteen hours and thirty-five minutes across a Friday overnight and a full Saturday trading day. Detection came not from monitoring but from a phone call: a district manager in Plattsburgh, alerted by a store associate who had watched a customer purchase forty cases of energy drinks in a single transaction, called the on-call line at 18:15 Saturday.

The response compounded the harm. The on-call engineer, working from a symptom description that pointed at discounting behavior and a runbook that named a decommissioned tool, concluded that the loyalty engine was the fault and disabled it. The mechanism available to him for disabling Waypoint was to publish a null promotion table to the controllers. In-store controllers running the current firmware treat a null promotion table as a malformed configuration and halt transaction processing rather than proceeding without promotions. Point-of-sale went down in all 118 affected stores at 20:10 Saturday and did not return until 23:50 — three hours and forty minutes on the highest-volume Saturday evening of the fourth quarter.

Stores improvised. Some closed. Some sold fuel only, on the pump-side card readers, which run independently of the store controller. Some ran manual cash sales with handwritten tickets and calculator totals, a practice for which no current procedure exists and which produced reconciliation and cash-control exposures that Finance is still resolving.

The proximate cause was a publishing job that could partially fail and report success. The conditions that allowed a partial failure to become a nineteen-hour pricing exposure and a four-hour outage were older and more mundane: an upgrade deferred twice for capacity reasons, an alert routed to the mailbox of an engineer who left the company in August 2025, and a rollback runbook last edited in 2023 that named a tool decommissioned in 2024.

This document examines those systems and decisions. It does not assign fault to individuals. Every person named acted on the information available to them, within the procedures they had been given, under time pressure they did not create.

---

## 2. Impact

### 2.1 Financial

| Measure | Value |
|---|---|
| Mispriced transactions | 41,300 |
| Gross undercharges (revenue not collected) | $312,000 |
| Refunds and goodwill credits issued | $88,000 |
| Estimated lost transactions during outage | 26,000 |
| Estimated lost sales during outage | $1,100,000 |
| **Total identified financial impact** | **$1,500,000** |

Undercharges of $312,000 represent the difference between the price that should have been charged and the price actually charged, across 41,300 transactions in 118 stores between 00:00 and 20:10 on December 5. The figure was derived from a transaction-level replay of the affected period against the correct price book and exclusion table, completed by the Retail Analytics team on December 9.

The $88,000 in refunds is separate from and additive to the undercharge figure. It reflects credits issued to customers who were charged correctly but complained about pricing inconsistency, customers affected by the outage who had prepaid fuel that could not be dispensed, and goodwill credits authorized by Store Operations during the Sunday call surge. It does not represent recovery of undercharged amounts; no attempt was made to recover from customers, and none will be.

Lost sales of $1.1 million reflects 26,000 transactions that did not occur during the outage window, valued at the trailing four-week average basket for a December Saturday evening in comparable stores. The estimate carries a stated uncertainty of plus or minus 18 percent. It excludes fuel volume at sites where pump-side card readers remained operational, which continued to transact.

### 2.2 Operational

- 118 stores with corrupted pricing for 19 hours 35 minutes
- 118 stores with point-of-sale unavailable for 3 hours 40 minutes
- 31 stores closed entirely during some portion of the outage
- 54 stores operated fuel-only on pump-side readers
- 33 stores ran manual cash transactions with handwritten tickets
- 2,100 customer care calls received Sunday, December 6, against a normal Sunday volume of approximately 240
- Average speed to answer Sunday peaked at 41 minutes; abandonment rate 34 percent
- 187 store associates worked unscheduled hours; 42 store managers were called in on days off
- Cash variances at 33 stores requiring individual reconciliation, 11 unresolved as of December 18

### 2.3 Inventory

Approximately 2,900 items were exposed to compounded discounting. Nineteen SKUs experienced sell-through exceeding 400 percent of forecast, producing out-of-stocks at 61 stores that persisted into the following week. Energy drinks, single-serve and multipack, accounted for 71 percent of the abnormal volume. Fourteen stores reported complete depletion of the energy drink category. Replenishment required expedited shipments from two distribution centers at a freight premium of $19,400.

### 2.4 Regulatory

The New York State Department of Agriculture and Markets, Bureau of Weights and Measures, opened an inquiry on December 11, 2026, following consumer complaints regarding price accuracy. The inquiry covers price posting and scanner accuracy at affected locations. Northway has retained outside counsel and is cooperating fully. Response documentation is due January 15, 2027. Potential exposure includes per-violation civil penalties across affected locations; Legal has advised that the range cannot be responsibly estimated at this stage.

### 2.5 Reputational

Regional media coverage in Plattsburgh, Watertown, and Glens Falls markets ran December 7 and 8. Social media activity peaked Saturday evening with images of receipts showing anomalous pricing. Brand sentiment tracking showed a 14-point decline in the affected districts, recovering to a 6-point deficit by December 20. No enterprise customer or fuel supply relationship was placed at risk.

---

## 3. Timeline

All times Eastern Standard Time. Times marked (recon) were reconstructed from system logs during investigation and were not observed in real time.

### Friday, December 4

**23:15** — Anchor nightly publishing job initiates on schedule. Payload comprises 2,900 item price changes for the December promotional cycle effective December 5, plus the corresponding loyalty exclusion table designating 1,140 of those items as ineligible for stacked promotion.

**23:38 (recon)** — Anchor publisher completes transmission of the price segment to 118 of 190 controllers. Transmission proceeds in store-number order; the 118 stores that received the file are the first 118 in that sequence.

**23:40 (recon)** — The publisher process encounters a connection reset while opening the exclusion table segment. The exception is caught by a handler that logs at INFO level and returns control to the job's completion routine. The completion routine evaluates only whether the price segment transmitted, which it had. Job status writes as SUCCESS.

**23:40 (recon)** — Queue depth on the Anchor publishing queue begins to climb as the remaining 72 stores' payloads back up behind the halted process. Queue depth alert threshold (500 messages) is crossed at 23:47.

**23:47 (recon)** — Queue depth alert fires. Notification routes to `pricebook-oncall@northwayfp.com`, an alias configured in 2021 that forwards to the individual mailbox of an engineer who separated from the company in August 2025. The mailbox remains active under IT's twenty-four-month retention policy for departed employees. Mail is delivered successfully. No bounce is generated. No human being reads it.

**23:52 (recon)** — Anchor dashboard displays the nightly publish as complete and successful. No operator is on duty; the dashboard is reviewed during the morning shift.

### Saturday, December 5

**00:00 (recon)** — New pricing takes effect at 118 stores. Waypoint, finding no exclusion table for the current price book version, applies its default behavior: all items promotion-eligible. Compounded discounting begins at first transaction.

**00:00–06:00 (recon)** — Overnight volume is low. An estimated 1,900 mispriced transactions occur. Aggregate undercharge in this window is approximately $11,000. Six stores in the affected set are 24-hour locations; the remainder open between 05:00 and 06:00.

**06:14** — First customer complaint logged by Customer Care, from a Malone location, regarding a receipt showing a negative line-item total on a coffee promotion. The call is coded as a loyalty card issue and closed with a $5 goodwill credit. The care agent follows the correct procedure for a single-customer loyalty discrepancy. No escalation path exists that would connect a single anomalous receipt to a systemic pricing condition.

**07:30** — Anchor morning dashboard review occurs as part of the Retail Technology daily operations checklist. The reviewer sees SUCCESS status for the December 4 publish. Queue depth is not on the daily checklist; it is considered an infrastructure metric rather than an application metric. Review completes in four minutes and is marked green.

**08:00–12:00 (recon)** — Transaction volume ramps. An estimated 9,400 mispriced transactions occur in this window. Undercharge accumulates to approximately $71,000 cumulative. Three additional customer care calls are logged and closed individually.

**10:20 (recon)** — Item-level movement for energy drinks at store 0447 (Plattsburgh) exceeds three standard deviations from the trailing mean. The anomaly is captured in the merchandising analytics warehouse. That system produces a weekly exception report distributed Monday mornings. It has no real-time alerting.

**12:00–18:00 (recon)** — Peak Saturday trading. An estimated 26,800 mispriced transactions occur. Undercharge accumulates to approximately $267,000 cumulative. Social media posts showing anomalous receipts begin appearing in local community groups around 14:00. Northway's social listening tool flags the activity at 15:40 and routes it to the Marketing queue, which is not staffed on weekends.

**17:50** — An associate at store 0447 processes a transaction for forty cases of energy drinks totaling $292.80 against a normal retail value of approximately $2,880. The associate completes the sale — she has no override authority to refuse a price the system presents and no procedure directing her to — and notifies her store manager at shift change.

**18:15** — **DETECTION.** District Manager Carla Hobbs (District 7, Plattsburgh) calls the Retail Technology on-call line. She reports "prices are wrong at multiple stores in my district, somebody just bought forty cases of Monster for sixty-one cents apiece." She has confirmed with three other stores in her district that similar pricing is present. Total elapsed from onset: 18 hours 15 minutes. Total elapsed from the queue-depth alert that no one read: 18 hours 28 minutes.

**18:22** — On-call engineer Miguel Arellano acknowledges the page and begins investigation. He opens the pricing incident runbook, last edited March 2023.

**18:31** — Arellano confirms the reported pricing on a test transaction at store 0447 via remote controller session. He observes that the price book version on the controller matches the expected December 5 version.

**18:40** — Arellano checks the Anchor job status. It reads SUCCESS. He reasonably concludes that price book publishing is not the problem, because the system that would tell him it was a problem is telling him it is not.

**18:55** — Arellano opens the rollback runbook. Step 3 instructs the responder to "initiate reversion via PriceSync Console." PriceSync was decommissioned in Q2 2024 and replaced by the Anchor Publisher Admin interface. The runbook was not updated. Arellano does not have documentation for the current tool's rollback function and cannot locate it in the internal wiki, which returns the same 2023 document.

**19:10** — Arellano attempts to reach the Anchor platform team's secondary on-call. The rotation calendar for that team was migrated to a new scheduling tool in October 2026. The entry Arellano reaches is stale and pages a person no longer in the rotation. No response.

**19:24** — Arellano observes in the Waypoint administrative console that promotions are applying to items he believes should be excluded. This observation is accurate. His inference — that Waypoint is misapplying its rules — is incorrect but entirely consistent with what he can see. He cannot see the exclusion table's absence, because the Waypoint console displays applied promotions, not the exclusion set it evaluated against. There is no view in any system that shows "exclusions expected: 1,140; exclusions loaded: 0."

**19:40** — Arellano attempts to disable individual promotion campaigns through the Waypoint console. The console requires campaigns to be disabled one at a time with a confirmation dialog. There are 214 active campaigns. At approximately fifteen seconds each, this path would require just under an hour, during peak trading, with pricing exposure accumulating at roughly $12,000 per hour. He abandons this approach after eleven campaigns.

**19:58** — Arellano identifies the bulk disable path documented in the Waypoint operations guide: publishing a null promotion table to the controllers. The operations guide describes this as "the supported method for suspending all promotional activity." It does not state, because its authors did not know, that controllers running firmware 4.2 and later — deployed fleet-wide in early 2026 — treat a null promotion table as a malformed configuration and halt transaction processing. The firmware release notes documented the behavior change. The Waypoint operations guide was not updated.

**20:05** — Arellano notifies the on-call channel that he is disabling Waypoint promotions to stop the pricing exposure. No one is monitoring the channel. Under the current escalation policy, a SEV-2 does not require manager notification until the sixty-minute mark, which had not yet elapsed.

**20:10** — **OUTAGE BEGINS.** Null promotion table publishes to 118 controllers. Point-of-sale halts at all 118 stores. Terminals display "CONFIGURATION ERROR — CONTACT SUPPORT." Fuel dispensers on pump-side card readers continue operating independently.

**20:12–20:30** — Store calls flood the support line. The help desk receives 74 calls in eighteen minutes against a normal Saturday evening rate of three to five.

**20:34** — Arellano recognizes that the null table publish has taken point-of-sale down. He attempts to republish the prior promotion table. The publish is accepted by Anchor and queued. Queue depth, still elevated from the previous night's stall, is now at 3,140 messages. The republish enters the back of the queue.

**20:47** — Arellano escalates to SEV-1 and pages the point-of-sale engineering manager.

**21:05** — **Doug Pelletier, Manager of Point-of-Sale Engineering, is paged and joins.** He instructs Arellano to stop remediation attempts pending assessment. He begins reconstructing the sequence of events. Within nine minutes he identifies the queue backlog as the reason the republish has not landed.

**21:14** — Pelletier initiates queue drain, purging the 72-store backlog from the previous night and prioritizing the promotion table republish. Drain is estimated at 40 minutes.

**21:22** — Pelletier pages Retail Technology leadership.

**21:30** — **Nia Broadwater, Director of Retail Technology, takes incident command.** She establishes a bridge, assigns roles, and requests Store Operations and Customer Care leadership.

**21:38** — **Fatima Zubairi, Vice President of Store Operations, joins and assumes store communications.** She initiates the store mass-notification sequence, the first structured communication any store has received in the ninety minutes since terminals went dark.

**21:45** — Zubairi's first mass message goes to all 118 stores: acknowledge the outage, confirm engineering is engaged, instruct stores to continue fuel sales on pump-side readers, and direct store managers to await further instruction before attempting manual sales. This last instruction arrives after 33 stores have already begun manual cash transactions.

**21:52** — Broadwater requests that a member of the Anchor platform team be located. The team's on-call is reached through a manager's personal contact list rather than the rotation system.

**22:04** — Anchor platform engineer Priya Raghunathan joins the bridge. Within twelve minutes she identifies the caught exception in the publisher log and the resulting absence of the exclusion table.

**22:16** — **ROOT CAUSE IDENTIFIED.** The bridge understands that the failure originated in Anchor, not Waypoint; that Waypoint behaved correctly given the input it received; and that restoring service requires both the promotion table republish and a complete price book republish including the exclusion segment.

**22:30** — Zubairi's second store message provides guidance on manual sales: stores already running manual transactions should continue with specified documentation requirements; stores not running manual transactions should not begin. The guidance is drafted live on the bridge because no current procedure exists.

**22:48** — Queue drain completes. Promotion table republish transmits.

**23:05** — First controllers begin accepting the promotion table. Point-of-sale restores at 22 stores.

**23:18** — Restoration proceeding store by store. 71 stores restored. Nine controllers require manual restart initiated remotely by the help desk.

**23:41** — 114 stores restored. Four controllers at stores 0392, 0518, 0603, and 0771 require on-site intervention.

**23:50** — **OUTAGE RESOLVED.** All 118 stores processing transactions. Outage duration: 3 hours 40 minutes.

**23:55** — Broadwater directs that the corrected price book publish be held until after close of business Sunday to avoid a second disruption during Sunday trading. Affected stores will operate on the incorrect prices overnight with a manual mitigation.

### Sunday, December 6

**00:15** — Zubairi issues a third store message with a manual mitigation: a list of the nineteen highest-exposure SKUs to be pulled from sale or manually rung at a corrected price, effective at open. Store managers acknowledge receipt through the store communication portal; 104 of 118 acknowledge by 06:00.

**06:00** — Stores open. Manual mitigation in effect. Pricing on remaining affected items is still incorrect but exposure is concentrated in the pulled SKUs.

**07:00** — **Renee Saint-Fleur's Customer Care team activates surge staffing.** Nineteen agents called in on overtime against a normal Sunday complement of six.

**07:00–22:00** — Customer Care fields 2,100 calls. Peak hour 11:00–12:00 with 287 calls. Average speed to answer peaks at 41 minutes. Abandonment 34 percent. Agents work from a script drafted at 06:30 and revised twice during the day.

**09:00** — Executive briefing. Finance begins undercharge quantification. Legal begins regulatory assessment.

**13:00** — Retail Analytics delivers preliminary transaction impact: approximately 40,000 affected transactions, undercharge in the $300,000 range.

**19:00** — Stores close. Corrected price book with full exclusion table publishes to all 190 stores.

**20:40** — Publish confirmed complete. Manual verification of pricing at twelve sample stores across four districts confirms correct application.

**22:15** — Manual mitigation lifted. Store communication issued.

### Monday, December 7 — Saturday, December 12

**December 7, 08:00** — Incident review kickoff. Broadwater assigns investigation leads.

**December 7, 14:00** — Finance opens cash variance reconciliation for the 33 stores that ran manual transactions.

**December 8** — Regional media coverage begins.

**December 9** — Retail Analytics delivers final transaction replay: 41,300 transactions, $312,000 undercharge.

**December 11** — **New York State Department of Agriculture and Markets opens weights-and-measures inquiry.**

**December 12** — Outside counsel retained. Document preservation notice issued.

**December 14, 14:20** — Incident formally closed following completion of pricing verification across all 190 stores.

---

## 4. Root Cause

The root cause was a defect in the Anchor publisher's error handling that permitted partial completion to be reported as full success.

The publisher transmits a price book in two segments: the price segment and the loyalty exclusion segment. These are separate operations against separate endpoints. The publisher's completion routine evaluates only the price segment's transmission status. This design reflects an assumption embedded in the 2019 implementation: that the exclusion segment could not fail independently of the price segment, because both were then transmitted over a single persistent connection. A 2022 infrastructure change separated the connections. The completion logic was not revisited.

On December 4, the connection carrying the exclusion segment was reset during handshake. The exception was caught by a broad handler wrapping the entire transmission block. That handler logs at INFO level and returns normally — behavior appropriate for the transient, retryable conditions it was written to absorb, and inappropriate for a condition that leaves the payload incomplete. Control returned to the completion routine, which found the price segment transmitted and wrote SUCCESS.

Three properties of this defect made it uniquely damaging. First, it was silent: the only signal was an INFO-level log line among approximately 4,000 written during a normal publish. Second, it was partial in a way that produced a *plausible* system state rather than an obviously broken one — 118 stores held a valid, well-formed, internally consistent price book that was simply missing a component nothing checked for. Third, it inverted the trust relationship between operator and monitoring: the SUCCESS status did not merely fail to help Arellano, it actively directed him away from the true cause for over three hours.

The downstream behavior of Waypoint was not a defect. Waypoint's promotion evaluator treats an absent exclusion table as an empty exclusion table. Absent and empty are represented identically in the interface contract between the two systems. There is no way for Waypoint to distinguish "no items are excluded" from "the exclusion data did not arrive." This is a gap in the contract, not a bug in the implementation, and it is addressed in the action items.

---

## 5. Contributing Factors

### 5.1 The deferred Anchor publisher upgrade

Anchor Publisher 4.0, scheduled for March 2026, would have replaced the completion routine with transactional publishing: all segments commit or none do. The upgrade was deferred in February to Q3, and again in July to Q1 2027.

Both deferrals were made through the correct governance process with documented rationale. The February deferral cited resource contention with the fuel-pricing integration, a revenue-generating program with an external commitment date. The July deferral cited the loyalty platform migration. Neither deferral was unreasonable. Both were made by people acting responsibly within their authority.

The failure is not in either decision. It is in the absence of any mechanism that accumulated their combined effect. Each deferral was evaluated as a fresh decision about a single quarter's capacity. Neither review surfaced the question of what risk the upgrade was intended to retire, how long that risk had been carried, or whether it was growing. The deferral record described the upgrade as "platform modernization" — accurate but uninformative. The transactional publishing change was one line in a nineteen-item scope document.

An organization can defer a fix indefinitely if each deferral is evaluated in isolation. Northway has no mechanism that makes the second deferral of a risk-retiring change harder than the first.

### 5.2 The orphaned queue-depth alert

The queue-depth alert functioned correctly. It fired at 23:47 on December 4, twelve minutes after the condition began, and was delivered successfully to `pricebook-oncall@northwayfp.com`.

That alias was configured in 2021 with a single member. When that engineer separated in August 2025, offboarding removed his access to production systems, revoked his credentials, and disabled his badge. It did not enumerate distribution aliases of which he was a member. His mailbox remained active under the standard twenty-four-month retention policy. Mail delivered cleanly. No bounce.

This alert had not been actionable for sixteen months. In that period it fired eleven times. Ten were transient conditions that self-resolved. The eleventh was December 4.

Northway has no alert ownership audit. There is no periodic verification that alert destinations resolve to on-duty humans, no requirement for named ownership, no synthetic test confirming delivery reaches a person. There are, per the current inventory, 340 configured alerts across Retail Technology. There is no reason to believe this was the only orphan.

The design was also fragile in a way independent of the offboarding gap: a single point of contact with no fallback, no escalation on non-acknowledgment, and delivery over a channel with no acknowledgment semantics. Even had the engineer remained, the alert would have failed if he were asleep, which at 23:47 on a Friday is likely.

### 5.3 The stale rollback runbook

The pricing incident runbook was last edited in March 2023. Step 3 named PriceSync Console, decommissioned in Q2 2024.

The 2024 migration project's checklist included updating operational documentation. That item was marked complete. Interviews indicate it referred to the Anchor Publisher Admin user guide, not the incident runbook, which lived in a different repository under a different owner. Neither party understood the other's scope.

The cost was direct: 33 minutes between 18:55 and 19:28 spent by the responder attempting to locate a tool that did not exist, followed by an escalation attempt against a stale rotation. During that period, undercharge accumulated at roughly $200 per minute and the responder's confidence in his own understanding degraded — a contributor to the subsequent decision.

Runbooks are the most fragile documentation an organization maintains: consulted rarely, under maximum stress, by people who cannot verify them. Northway has no expiry, no review cadence, no test.

### 5.4 The undocumented firmware behavior change

Controller firmware 4.2, deployed fleet-wide in Q1 2026, changed null promotion table handling from "proceed without promotions" to "halt with configuration error." The change was deliberate, made after a 2025 incident in which a partially corrupted promotion table caused silent mispricing — a fail-safe change, and a sound one.

It was documented in the firmware release notes. It was not propagated to the Waypoint operations guide, which continued to describe the null publish as "the supported method for suspending all promotional activity."

The responder followed documented procedure. The procedure was wrong. There is no cross-reference between firmware release notes and operational procedures, and no test that validates documented procedures against current system behavior.

### 5.5 Detection dependent on human observation

Nineteen hours and thirty-five minutes elapsed between onset and detection. In that window:

- 41,300 anomalous transactions processed
- Nineteen SKUs exceeded three standard deviations from mean movement
- Four customer complaints were logged and individually closed
- Social listening flagged anomalous activity at 15:40
- Aggregate margin in 118 stores collapsed by a measurable and extreme amount

Every one of these signals existed in a system Northway operates. None was connected to an alert.

- Merchandising analytics detects movement anomalies but reports weekly.
- Customer Care logs complaints but has no threshold that aggregates across stores.
- Social listening routes to a queue unstaffed on weekends.
- Financial reporting computes margin daily but produces reports on a T+1 schedule.
- The Anchor dashboard shows queue depth but it is not on the daily checklist.

Northway's detection posture assumes failures announce themselves as errors. This failure announced itself as revenue — a category of signal that no monitoring system observes and every business system records.

### 5.6 The decision to disable Waypoint

This is the most consequential decision in the incident and the one that most requires examination free of hindsight.

At 19:58, the responder had been engaged for 96 minutes. He had confirmed the mispricing. He had checked the authoritative publishing status, which said SUCCESS. His rollback procedure named a nonexistent tool. His escalation path to the owning team had failed. Pricing exposure was accumulating at roughly $12,000 per hour on a Saturday evening. He could observe, in the Waypoint console, promotions applying where they should not — a true observation. And the Waypoint operations guide told him that publishing a null table was the supported way to stop it.

Given his information, the decision was defensible. It was also wrong, and it converted a $312,000 pricing incident into a $1.5 million pricing-and-outage incident.

The systemic conditions that produced it:

**No blast-radius gate.** No control required a second approver before an action touching 118 stores. The null publish was a single operation available to a single engineer with no confirmation reflecting its scope.

**No sanctioned partial mitigation.** The responder's options were disable one campaign at a time (an hour, during peak) or disable everything at once. Nothing existed between. A store-group-scoped or category-scoped promotion suspension would have let him bound the exposure while investigating.

**Escalation policy calibrated to duration, not stakes.** Manager notification was required at sixty minutes for a SEV-2. The responder was at 96 minutes and had notified the channel, but no one monitored it. The policy did not account for the possibility that the *remediation* carried more risk than the incident.

**Isolation.** For 96 minutes, one engineer held the entire problem. Escalation existed but required his judgment to invoke, at precisely the moment his judgment was most loaded. Every subsequent phase — Pelletier's assessment, Broadwater's command, Raghunathan's diagnosis — moved quickly. The single largest lever in this incident was not a tool. It was a second person.

### 5.7 Improvised cash handling

Thirty-three stores ran manual cash transactions with handwritten tickets and calculator totals during the outage. They did so with no procedure, no authorization, and no guidance, for ninety minutes before Zubairi's first message.

They did so because store managers judged — correctly, in commercial terms — that turning away customers on a December Saturday evening was worse than transacting imperfectly. That judgment reflects well on them. The organization put them in a position where they had to make it alone.

Consequences:

- Handwritten tickets in inconsistent formats; some captured item detail, others only totals
- No tax calculation; some stores estimated, some omitted, some applied a flat percentage
- Age-restricted product sales without electronic verification at nine stores
- Fuel prepay without electronic authorization at six stores
- Cash accepted with no register control, reconciled against manual tallies
- Loyalty accrual not captured, generating a secondary complaint stream Sunday

Finance identified variances at all 33 stores. Aggregate net variance was $4,100 — small, and consistent with honest people doing arithmetic under pressure, not with loss. Eleven stores remained unreconciled at the time of review.

The last manual-sales procedure was retired in 2019 with the cash-register replacement program, on the reasoning that the new terminals had battery backup and offline mode. Offline mode handles network loss. It does not handle a controller that has halted on a configuration error. The 2019 assessment did not anticipate a failure mode in which the terminal is powered, connected, and refusing to transact.

---

## 6. What Worked

**District manager escalation.** Detection came from a district manager who recognized an anomalous report, verified it across three stores before calling, and escalated with specifics. Absent that call, exposure would likely have continued to Monday's exception report — an additional 36 hours and, by extrapolation, $400,000 to $500,000 in further undercharge.

**Incident command.** From 21:30, command structure functioned as designed. Broadwater established the bridge, assigned roles, and separated technical resolution from store communications and customer response. From command establishment to root cause identification: 46 minutes. From command establishment to full restoration: 2 hours 20 minutes.

**Technical diagnosis under pressure.** Pelletier identified the queue backlog nine minutes after joining. Raghunathan identified the caught exception twelve minutes after joining. Both worked from first principles against a monitoring system actively reporting the opposite of the truth.

**Store communications once initiated.** Zubairi's three messages between 21:45 and 00:15 were clear, sequenced, and actionable. The 00:15 message containing the nineteen-SKU manual mitigation was drafted, approved, and distributed in under two hours from a standing start, and achieved 88 percent acknowledgment by open.

**Customer Care surge.** Saint-Fleur's team went from six agents to nineteen on four hours' notice on a Sunday in December. They absorbed nine times normal volume. Abandonment at 34 percent was poor in absolute terms and creditable given the ratio.

**The decision to delay the corrected publish.** Broadwater's 23:55 decision to hold the corrected price book until after Sunday close, accepting continued pricing exposure in exchange for avoiding a second disruption during Sunday trading, was the correct trade and was made deliberately with the trade named aloud on the bridge.

**Store manager judgment.** Thirty-three store managers found a way to serve customers with no procedure and no guidance. The aggregate $4,100 variance across 33 stores handling improvised cash is evidence of conscientiousness.

**Financial reconstruction.** Retail Analytics delivered a defensible transaction-level replay within four days, providing Legal and Finance a firm basis for regulatory response.

---

## 7. What Did Not Work

**Automated detection.** Detection took 18 hours 15 minutes and came by telephone. No automated system detected the condition. This is the central failure.

**The alert that fired correctly and reached no one.** The queue-depth alert did its job at 23:47 and was read by nobody. Sixteen months of undetected orphaning.

**Publishing job status as a source of truth.** SUCCESS status did not merely fail to indicate a problem; it directed the responder away from the cause for over three hours.

**The rollback runbook.** Three years stale, naming a tool decommissioned two years prior. Cost: 33 minutes and a significant degradation of responder confidence.

**Escalation paths.** The Anchor team's rotation entry was stale following an October tooling migration. The responder's channel notification at 20:05 was unmonitored. Escalation ultimately succeeded through a personal contact list.

**Absence of graduated remediation.** The gap between "disable one campaign" and "disable everything" left the responder without a proportionate option under time pressure.

**Absence of blast-radius controls.** An action affecting 118 stores required one person, one command, no second approval.

**Waypoint's inability to distinguish absent from empty.** A contract gap that made the downstream system structurally incapable of detecting the upstream failure.

**Documentation propagation.** The firmware behavior change was documented where it was made and nowhere it was used.

**Manual sales readiness.** No procedure, retired in 2019 on an assumption that did not hold, leaving 33 stores to improvise for ninety minutes.

**Weekend coverage.** Social listening flagged anomalous activity at 15:40 into an unstaffed queue — two hours and thirty-five minutes before detection.

**Complaint aggregation.** Four calls across four stores, all correctly handled in isolation, none aggregated. No threshold exists that would connect them.

---

## 8. Action Items

### Priority 1 — Complete by January 31, 2027

**A1. Ship transactional publishing in Anchor.**
Refactor the publisher so that a price book publish commits all segments or none. Eliminate the completion routine's single-segment evaluation. Remove the broad exception handler. Includes the removal of the Q1 2027 deferral.
**Owner:** Priya Raghunathan, Anchor Platform Lead | **Sponsor:** Nia Broadwater | **Due:** January 31, 2027

**A2. Complete alert ownership audit across Retail Technology.**
Audit all 340 configured alerts. For each: verify the destination resolves to an on-duty human, assign a named owner and named backup, remove individual mailboxes as destinations, and confirm delivery via synthetic test.
**Owner:** Doug Pelletier | **Due:** January 15, 2027

**A3. Implement price book integrity validation at the controller.**
Controllers must validate that a received price book contains all required segments and that the exclusion table item count is within expected bounds. Reject and alert on failure; retain the prior version.
**Owner:** Doug Pelletier | **Due:** January 31, 2027

**A4. Implement margin anomaly detection with real-time alerting.**
Continuous monitoring of gross margin by store and category against rolling baseline. Alert on deviation beyond defined thresholds, routed to on-call with acknowledgment required. Target detection within 30 minutes of a comparable condition.
**Owner:** Marcus Delacroix, Director of Retail Analytics | **Due:** January 31, 2027

**A5. Publish an interim manual sales procedure.**
Covering cash handling, ticket format, tax, age-restricted product, fuel prepay, reconciliation, and authorization thresholds. Distribute to all 190 stores with acknowledgment.
**Owner:** Fatima Zubairi | **Due:** December 31, 2026

### Priority 2 — Complete by March 31, 2027

**A6. Rebuild the pricing incident runbook and institute runbook lifecycle management.**
Rewrite against current tooling. Establish quarterly review with expiry, automatic flagging of overdue runbooks, and a requirement that any tool decommission enumerate and update referencing runbooks.
**Owner:** Miguel Arellano | **Reviewer:** Doug Pelletier | **Due:** February 28, 2027

**A7. Implement blast-radius controls for fleet-wide operations.**
Any operation affecting more than 25 stores requires second-approver authorization. Implement a canary path: apply to five stores, verify, then proceed.
**Owner:** Doug Pelletier | **Due:** March 15, 2027

**A8. Build graduated promotion suspension in Waypoint.**
Suspension scoped by store group, district, category, or campaign group, executable in under two minutes, without publishing a null table. Deprecate the null-table method and remove it from documentation.
**Owner:** Sandra Okonjo, Loyalty Platform Manager | **Due:** March 31, 2027

**A9. Close the absent-versus-empty contract gap.**
Amend the Anchor-to-Waypoint contract so exclusion tables carry an explicit item count and version. Waypoint refuses to evaluate promotions when the received count does not match the declared count, alerting rather than defaulting to permissive behavior.
**Owner:** Priya Raghunathan and Sandra Okonjo | **Due:** March 31, 2027

**A10. Revise escalation policy to account for remediation risk.**
Introduce mandatory manager engagement when a responder proposes an action affecting more than 25 stores, independent of elapsed time or severity. Add a "second set of eyes" trigger at 45 minutes of unresolved single-responder work.
**Owner:** Nia Broadwater | **Due:** February 15, 2027

**A11. Establish weekend and overnight coverage for anomaly-bearing signal channels.**
Social listening, complaint aggregation, and merchandising exception reporting to route to a staffed destination during all trading hours.
**Owner:** Fatima Zubairi and Renee Saint-Fleur | **Due:** March 15, 2027

**A12. Implement customer complaint aggregation thresholds.**
Automatic escalation when complaints of the same category exceed a threshold across multiple stores within a rolling window.
**Owner:** Renee Saint-Fleur | **Due:** March 31, 2027

**A13. Institute deferral accumulation review.**
Any change deferred more than once must be reviewed at the ELT level with explicit documentation of the risk being carried, its duration, and the compensating controls. Second deferrals require VP sponsorship; third deferrals require ELT approval.
**Owner:** Nia Broadwater | **Sponsor:** Chief Information Officer | **Due:** February 28, 2027

**A14. Establish documentation propagation requirements for firmware and platform changes.**
Any change altering documented operational behavior must enumerate and update all referencing operational documentation before release. Add to the release checklist as a blocking item.
**Owner:** Doug Pelletier | **Due:** February 28, 2027

**A15. Validate and consolidate on-call rotation data.**
Audit all Retail Technology rotations following the October 2026 tooling migration. Establish a single authoritative source with monthly verification.
**Owner:** Doug Pelletier | **Due:** January 31, 2027

### Priority 3 — Complete by June 30, 2027

**A16. Develop full offline transaction capability.**
Enable terminals to complete transactions from a locally cached price book when the controller is unavailable, with queued reconciliation on restoration. Replaces the interim manual procedure (A5).
**Owner:** Doug Pelletier | **Sponsor:** Nia Broadwater | **Due:** June 30, 2027

**A17. Establish a pricing incident simulation program.**
Quarterly exercises covering pricing anomaly detection, escalation, and rollback, validating runbooks against current tooling. First exercise by March 31, 2027.
**Owner:** Miguel Arellano | **Reviewer:** Nia Broadwater | **Due:** March 31, 2027, then quarterly

**A18. Complete cash variance reconciliation and issue findings.**
Close the eleven outstanding store reconciliations. Issue findings on control gaps in improvised cash handling.
**Owner:** Theresa Vandenberg, Controller | **Due:** January 31, 2027

**A19. Deliver regulatory response and remediation plan.**
Complete the response to the Department of Agriculture and Markets. Implement any required scanner accuracy remediation.
**Owner:** General Counsel | **Due:** January 15, 2027 (filing); June 30, 2027 (remediation)

**A20. Conduct a full price book pipeline resilience review.**
End-to-end review of the Anchor-to-Waypoint-to-controller pipeline identifying additional single points of failure, silent failure modes, and unvalidated contract assumptions.
**Owner:** Priya Raghunathan | **Sponsor:** Nia Broadwater | **Due:** June 30, 2027

---

## 9. Closing Observations

Three observations warrant retention beyond the action items.

**The failure was not the outage.** The outage was loud, expensive, and resolved in under four hours by people who performed well. The pricing exposure was quiet, ran nineteen hours, and was caught by a phone call. Northway is well-equipped to respond to failures that announce themselves and poorly equipped to detect failures that do not. Correctness failures are harder to detect than availability failures because a correctness failure looks, to every system watching, like success. The largest investments in this action plan address detection, not response.

**Every individual decision was defensible.** Two deferrals were made through proper governance with sound rationale. Offboarding followed policy. The firmware change was a fail-safe improvement, correctly documented where it was made. The responder followed the operations guide. The store managers who improvised cash sales made a reasonable commercial judgment. Each choice was locally rational; the system that contained them was not. The organization's task is not to find better people. It is to build a system in which reasonable local decisions do not compose into a $1.5 million failure.

**Isolation was the strongest amplifier.** From 18:22 to 21:05, one engineer held the entire problem, working against monitoring that lied to him, a runbook that misled him, and an escalation path that failed him. The consequential decision was made in that window. From 21:05 forward, with a second engineer, then a director, then a VP, the incident moved quickly toward resolution. No tool in this action plan is worth as much as a second person on the bridge at minute forty-five.

---

*Prepared by Retail Technology, Northway Fuel and Provisions. Reviewed December 18, 2026. Action item progress reported monthly to the Executive Leadership Team until closure.*
