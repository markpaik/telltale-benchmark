# Incident Postmortem: Baseline 11.0 Upgrade — Location Master Corruption and Extended Fulfillment Outage

**Facility:** Rome, New York Fulfillment Center (900,000 sq ft)
**Incident window:** November 22, 2026, 04:10 EST — December 6, 2026, 18:00 EST
**Severity:** Sev-1 (facility-wide fulfillment degradation, multi-client service failure)
**Document status:** Final, issued December 18, 2026
**Prepared by:** Incident Review Working Group
**Distribution:** Executive Committee, Site Leadership, IT, Client Services, Quality, Vendor Relations

---

## 1. Summary

On the weekend of November 21–22, 2026, Tannery Row Logistics upgraded its warehouse management system, Baseline, from version 9.2 to version 11.0 at the Rome, New York fulfillment center. The upgrade completed at 04:10 on Sunday, November 22, inside the planned window and with no errors reported by the vendor's installation log.

The upgrade included a location master transformation intended to normalize location identifiers to a new schema. The transformation silently dropped the aisle prefix from 61,000 of the facility's 214,000 pick locations — approximately 28.5 percent of the location master. Locations that had previously been unique became ambiguous. A scan of a stripped location returned a validation success against a bin that was not the bin the picker was standing in front of. The system did not throw an error, did not log a warning, and did not fail the transformation. The pick confirmed. The unit went into the tote. The order shipped.

Pick accuracy at the Rome facility fell from a trailing baseline of 99.6 percent to 91.2 percent by Monday afternoon, November 23. The facility did not know this. The quality report that would have surfaced the drop runs on a two-shift lag, and the exception queue that would have surfaced anomalous scan patterns had lost its designated owner to an internal transfer in September; the queue had been accumulating unreviewed items for nine weeks. No alert fired. No human looked.

Detection came from outside the building. At 11:20 on Tuesday, November 24 — 31 hours and 10 minutes after the upgrade completed — a returns team at one of the fourteen brands served by the facility called Client Services to report 900 wrong items received in a single trailer. That call was the first indication anyone had that something was wrong.

The initial diagnosis was incorrect. Scanner firmware had been pushed to the handheld fleet the week prior, and the correlation was compelling enough that the Director of Information Technology ordered a full fleet rollback. The rollback consumed nine hours of Tuesday and Wednesday and did not change the error rate, because the firmware was not the cause.

With accuracy still degraded and no known root cause, the Vice President of Operations moved the entire building to paper pick sheets on Wednesday, November 25. This was the correct call under the information available and it stopped the production of wrong shipments. It also cut throughput from approximately 78,000 units per day to approximately 31,000 units per day, a 60 percent reduction, entering the highest-volume week of the year. The facility began accumulating a backlog that peaked at 214,000 orders.

The Continuous Improvement Manager identified the actual defect at approximately 02:00 on Thursday, November 26, by diffing the live location master against a pre-upgrade export she had pulled for an unrelated slotting analysis. Remediation of the location master was completed and validated by 21:40 Thursday. Scan-based picking resumed on the morning shift of Friday, November 27.

Clearing the backlog took 11 days, concluding December 6. Thirty-eight thousand orders shipped wrong or late. Expedited freight to recover service commitments cost $1.8 million. Two clients took service credits totaling $640,000. One client issued notice of termination on a contract worth $9 million in annual revenue.

This document reconstructs the upgrade decision, the detection gap, the scanner misdiagnosis, the paper picking tradeoff, and the testing gaps. It examines the systems and decision structures that produced the outcome. It does not assign fault to individuals. Every decision described here was made by a competent person acting on the information available to them at the time, inside a process that did not give them what they needed.

---

## 2. Impact

### 2.1 Operational impact

| Measure | Baseline | Incident period | Delta |
|---|---|---|---|
| Pick accuracy | 99.6% | 91.2% (Nov 23 low) | −8.4 pts |
| Daily throughput (units) | 78,000 | 31,000 (paper picking) | −60.3% |
| Peak order backlog | ~0 | 214,000 orders | — |
| Days to clear backlog | — | 11 | — |
| Total degraded-operation duration | — | 14 days, 14 hours | — |
| Time from upgrade completion to detection | — | 31 hours 10 minutes | — |
| Time from detection to correct root cause | — | 62 hours 40 minutes | — |
| Time from root cause to remediation complete | — | 19 hours 40 minutes | — |

### 2.2 Order-level impact

- **38,000 orders** shipped wrong or late across the incident window.
- **Approximately 11,400 orders** shipped with at least one incorrect item during the November 22–25 scan-validated window, based on reconciliation of returns and client-reported discrepancies.
- **Approximately 26,600 orders** shipped late during the paper-picking and backlog-recovery period.
- **900 units** in the single trailer that triggered detection — the visible fraction of an error population that had by then been accumulating for 31 hours.

### 2.3 Financial impact

| Category | Amount |
|---|---|
| Expedited freight | $1,800,000 |
| Client service credits (2 clients) | $640,000 |
| Annualized revenue under termination notice | $9,000,000 |
| Direct labor premium (overtime, temp staffing, Nov 25–Dec 6) | $1,240,000 |
| Return processing and re-ship cost (11,400 orders) | $418,000 |
| Vendor emergency engagement fees | $87,000 |
| **Total quantified cost, excluding contract loss** | **$4,185,000** |

The $9 million contract notice is stated separately because the outcome remains open as of this document's issuance; the client has entered a 90-day transition-planning period and has not executed a final termination.

### 2.4 Client impact distribution

Of the 14 brands served by the facility:

- 4 brands experienced material accuracy impact (>2% of shipments affected).
- 9 brands experienced material lateness impact (>10% of orders shipped outside SLA).
- 2 brands invoked service credit provisions.
- 1 brand issued termination notice.
- 3 brands reported no measurable impact, having low order volume during the affected window.

### 2.5 Workforce impact

- 1,150 associates worked in degraded conditions for 14 days.
- Paper picking required approximately 340 hours of supervisory time per day in manual sheet distribution, reconciliation, and error correction — work that does not exist in normal operation.
- Voluntary turnover in the pick function ran at 4.1 percent in the 30 days following the incident, against a trailing 12-month average of 1.6 percent.

---

## 3. Timeline

All times Eastern. Times marked **(reconstructed)** are derived from system logs, badge data, or corroborated recollection rather than contemporaneous records.

### Pre-incident

**May 2026 (original date).** Baseline 11.0 upgrade originally scheduled for the weekend of May 16–17, 2026. This date was selected specifically because it sat in the facility's lowest-volume window and allowed a full recovery runway before peak season.

**June 4, 2026.** Vendor requests deferral of the upgrade. The vendor cited resource constraints in its implementation practice and proposed a revised date of November 21–22. Vendor communication characterized the November window as "acceptable given the maturity of the 11.0 release."

**June 11, 2026 (reconstructed).** Internal discussion of the deferral. Concerns raised regarding proximity to peak. The decision to accept the November date was made on the basis that (a) the vendor would not commit to an alternative before Q4, (b) version 9.2 was scheduled to leave full support in Q1 2027, and (c) the 11.0 release had by then been deployed at 40+ vendor sites without reported major incident. No formal risk assessment document was produced. No peak-season deployment freeze policy existed to prevent the scheduling.

**September 8, 2026.** The associate who owned the WMS exception queue transferred to a different function within the company. Queue ownership was not reassigned. The queue continued to receive items; no one reviewed them. This was not detected because the queue has no aging alert and no unreviewed-volume threshold.

**October 12–30, 2026.** Regression testing performed against Baseline 11.0 in the staging environment. The regression suite used was the suite last modified for the version 9.0 upgrade. It contained 312 test cases. None exercised the location master transformation, because no prior version upgrade had included one.

**November 2–5, 2026.** Parallel validation window. Originally scoped at two weeks; compressed to four days. The compression was a consequence of the schedule shift — the November date left less runway between vendor delivery of the release candidate and the cutover than the May date would have. Parallel validation covered order flow, wave planning, shipping manifest generation, and receiving. It did not include a location master integrity check.

**November 16, 2026.** Scanner firmware version 4.7.2 pushed to the handheld fleet (approximately 620 devices). This was a routine, unrelated maintenance push addressing battery reporting accuracy. It completed without incident and had no effect on scan validation logic. Its proximity to the upgrade would prove consequential.

**November 20, 2026.** Cutover runbook finalized. The runbook was the vendor's template document with facility names and contact numbers substituted. It contained 47 steps. Step 41 was "Validate master data." The validation criterion specified was "Confirm record counts match pre-upgrade totals." Record counts did match — the transformation did not delete records, it modified them. The check passed.

### Upgrade and silent failure

**Saturday, November 21, 22:00.** Cutover begins. Facility in planned shutdown. Vendor implementation engineer on site, two Tannery Row IT staff on site, one on call.

**Sunday, November 22, 01:15.** Database migration completes. Location master transformation executes as part of the migration package. The transformation is a schema normalization routine intended to move location identifiers from a legacy composite format to a delimited format. For 61,000 records where the aisle prefix contained a character the transformation's parsing logic did not anticipate, the prefix was dropped rather than migrated. The routine logged the records as processed successfully. No exception was raised.

**Sunday, November 22, 03:20.** Step 41 validation executed. Record counts match: 214,000 pre-upgrade, 214,000 post-upgrade. Validation marked complete.

**Sunday, November 22, 04:10.** Upgrade declared complete. Vendor engineer departs. Go/no-go call held with site leadership; decision is go. Facility opens for Sunday partial shift.

**Sunday, November 22, 06:00–14:00.** Sunday shift runs at reduced volume (approximately 22,000 units, normal for Sunday). Pickers begin encountering locations that scan valid but contain unexpected inventory. Reconciliation is handled ad hoc at the floor level; associates pick the item they were sent for if it is present nearby, or report a discrepancy. Discrepancy reports flow to the exception queue. Nobody is reading the exception queue.

**Sunday, November 22, 14:00 (reconstructed).** Shift supervisor notes "more bin issues than usual, probably settling in after the upgrade" in a shift handover note. This is a rational inference. Post-upgrade friction is expected and normal. The note is not escalated.

### Undetected degradation

**Monday, November 23, 06:00.** Full production Monday begins. Facility runs approximately 74,000 units. Scan validation returns success on stripped locations throughout the day. Wrong items are picked, packed, manifested, and loaded.

**Monday, November 23, 12:00–16:00.** Pick accuracy, measured after the fact, is at its low point of 91.2 percent. This is not visible to anyone. The quality report covering Sunday's shifts will not publish until Monday evening; the report covering Monday will not publish until Tuesday evening.

**Monday, November 23, 18:30.** Quality report publishes covering Sunday, November 22. It shows accuracy at 97.9 percent — degraded, but Sunday is a low-volume shift with high variance and the figure does not breach the alerting threshold of 97.0 percent. No alert fires.

**Monday, November 23, 22:00.** Night shift begins. Trailer containing the 900 misfilled units for the reporting brand is sealed and dispatched.

**Tuesday, November 24, 06:00.** Day shift begins. Facility continues at production volume with degraded accuracy.

### Detection

**Tuesday, November 24, 11:20.** Returns team at a client brand contacts Client Services Director Tanya Whitehorse to report 900 wrong items received in a single trailer. This is the first external signal. **T+31:10 from upgrade completion.**

**Tuesday, November 24, 11:45.** Whitehorse escalates to site leadership. Initial working assumption is a single mis-staged trailer — a load error, not a systemic one.

**Tuesday, November 24, 12:30.** Vice President of Operations Bianca Cardoso-Reyes requests an accuracy pull for the preceding 72 hours. The two-shift lag means the most recent complete data is from Sunday.

**Tuesday, November 24, 13:15.** Manual sampling of outbound totes on the pack line begins. Sample of 200 totes returns 17 with at least one incorrect item — an 8.5 percent tote-level error rate. The problem is confirmed as systemic and current, not a single trailer.

**Tuesday, November 24, 13:40.** Sev-1 declared. Incident bridge opened. Participants: Cardoso-Reyes (Operations), Ephraim Sackey (IT), Whitehorse (Client Services), Marguerite Lapointe (Continuous Improvement), site quality lead, shift managers.

### Misdiagnosis and rollback

**Tuesday, November 24, 14:10.** Sackey identifies scanner firmware 4.7.2, pushed November 16, as the leading hypothesis. The reasoning is documented on the bridge: the symptom presents as scan-layer misbehavior; a scan-layer change had recently been made; the WMS upgrade had passed its validation gate and the vendor had reported no issues at other sites. The firmware is the newer, less-validated change in the mental model of the room. This is a defensible inference from the available evidence.

**Tuesday, November 24, 14:50.** Decision made to roll the handheld fleet back to firmware 4.6.9. Rollback requires devices to be docked and reimaged in batches; the fleet cannot be rolled back all at once without halting picking entirely.

**Tuesday, November 24, 15:30 — Wednesday, November 25, 00:30.** Fleet rollback executes in batches across three shifts. Approximately 620 devices reimaged. Nine hours of elapsed effort. Picking continues on rolled-back devices as they return to service.

**Tuesday, November 24, 19:00.** Quality report publishes covering Monday, November 23. Accuracy: 91.2 percent. This is the first time the magnitude of the accuracy failure is visible in a system report. It arrives 24 hours after the events it describes and more than five hours after the incident was already declared through other means. The report confirms severity but contributes nothing to diagnosis.

**Wednesday, November 25, 01:00.** Post-rollback sampling begins. Sample of 200 totes returns 16 with incorrect items — 8.0 percent. Statistically indistinguishable from the pre-rollback rate. The firmware hypothesis is disconfirmed.

**Wednesday, November 25, 02:15.** Bridge reconvenes. No working hypothesis. Nine hours spent, no diagnostic progress, error rate unchanged, and the facility is generating wrong shipments at production volume.

### Paper picking decision

**Wednesday, November 25, 03:00.** Cardoso-Reyes convenes site leadership. The decision framing on the bridge: the facility cannot continue producing wrong shipments at 78,000 units per day into an unknown fault, and no root cause is in sight. The available options are stated as:

1. Continue scan-based picking with 100 percent outbound QC inspection. Rejected — inspection capacity could not cover 78,000 units, and staffing to that level was not achievable inside 24 hours.
2. Halt outbound entirely. Rejected — creates the same backlog with none of the throughput.
3. Move to paper pick sheets generated from the pre-upgrade location master export held in the reporting environment. Accepted.

**Wednesday, November 25, 04:00.** Decision to convert the building to paper picking, effective the 06:00 shift. Paper sheets to be generated from the reporting-environment copy of the location master, which predates the upgrade and is known-good.

**Wednesday, November 25, 06:00.** Paper picking begins. Throughput drops immediately. First full paper day produces approximately 31,000 units.

**Wednesday, November 25, 08:00.** Whitehorse begins structured client notification. All 14 brands contacted within four hours with a standing commitment to twice-daily updates.

**Wednesday, November 25, all day.** Backlog begins accumulating at approximately 47,000 orders per day against normal demand, higher against pre-Black Friday demand.

### Root cause identification

**Wednesday, November 25, 20:00 (reconstructed).** Lapointe begins independent investigation. Her entry point is not the incident bridge. She had pulled a full location master export in early November for an unrelated slotting density analysis. Her hypothesis: if paper sheets generated from the old export are producing correct picks and scan-based picking against the new system is not, the difference is in the location data itself.

**Thursday, November 26, 02:00.** Lapointe completes a field-level diff of the live location master against her pre-upgrade export. The diff identifies 61,000 records where the aisle prefix is present in the export and absent in the live table. Root cause identified. **T+94:50 from upgrade completion. T+62:40 from detection.**

**Thursday, November 26, 02:40.** Lapointe escalates to Sackey and Cardoso-Reyes. Bridge reconvened at 03:15.

**Thursday, November 26, 04:00.** Vendor emergency engagement opened. Vendor confirms the transformation routine's parsing logic and acknowledges the defect. Vendor reports the defect had been observed at one prior site in a limited form and had not been published to the customer base.

### Remediation

**Thursday, November 26, 05:30.** Remediation approach agreed: restore aisle prefixes to the 61,000 affected records from the pre-upgrade export, with full-population reconciliation rather than targeted repair, to avoid assuming the diff had found every affected record.

**Thursday, November 26, 07:00–14:00.** Remediation script developed and tested against a restored copy of the production database.

**Thursday, November 26, 14:00–18:20.** Remediation executed against production during a picking pause. All 214,000 location records reconciled against the pre-upgrade export.

**Thursday, November 26, 18:20–21:40.** Post-remediation validation. Physical scan verification of a 1,200-location stratified sample across all zones. Zero discrepancies. Remediation declared complete at 21:40.

**Friday, November 27, 06:00.** Scan-based picking resumes. Throughput recovers to approximately 68,000 units on the first day back, reaching 81,000 by November 29 with overtime staffing.

### Recovery

**Friday, November 27 — Sunday, December 6.** Backlog recovery. Peak backlog of 214,000 orders reached November 27. Recovery ran at an average of approximately 19,500 orders per day of backlog reduction on top of incoming demand, supported by overtime, weekend shifts, and temporary staffing.

**Sunday, December 6, 18:00.** Backlog cleared. Facility returns to normal operating state. Incident closed.

**December 8–16.** Postmortem interviews conducted with 23 participants across Operations, IT, Quality, Client Services, and Continuous Improvement.

**December 18.** This document issued.

---

## 4. Root cause

The proximate technical cause was a defect in the Baseline 11.0 location master transformation routine. The routine parsed legacy composite location identifiers to split them into a delimited format. For location identifiers where the aisle prefix contained a character class outside the routine's expected pattern, the parser returned the identifier's remainder and silently discarded the prefix. The routine treated a partial parse as a successful parse.

This affected 61,000 of 214,000 records. The resulting identifiers were no longer unique across the facility, because the aisle prefix was the disambiguating element. A stripped identifier could match multiple physical bins. Baseline's scan validation logic checks whether a scanned identifier exists in the location master and whether it is associated with the expected item. Against a stripped identifier, the check could return true for a bin the picker was not standing at, because the match was made against a different physical location that shared the now-ambiguous identifier.

The system behaved exactly as designed given the data it held. The failure was not in the scan validation logic; it was in the data that logic trusted.

**The technical defect was the vendor's. The exposure was ours.** A transformation routine that silently discards data is a serious vendor quality failure, and the vendor's decision not to publish a defect it had observed at a prior site compounded it. But no organization can outsource the assumption that a vendor's data transformation is correct. Our validation gate was designed to catch a transformation that dropped records. It was not designed to catch a transformation that corrupted them. That design choice — record counts as the sole master data validation criterion — is what allowed 61,000 corrupted records into production.

The root cause, stated at the level where we can act on it: **the facility deployed a version upgrade containing an untested data transformation, into peak season, behind a validation gate that checked record volume rather than record integrity, with no independent detection capability that could surface the resulting error faster than a customer could.**

---

## 5. Contributing factors

### 5.1 The upgrade decision and the schedule shift

The upgrade was originally scheduled for May 2026 — a deliberate choice placing it in the lowest-volume window with maximum recovery runway. The vendor's June request to defer moved it to November 21, nine days before Black Friday and inside the highest-volume, lowest-tolerance period of the operating year.

The decision to accept the November date was made without a formal risk assessment. The reasoning was sound in its parts: version 9.2 was approaching end of full support; the vendor would not commit to an alternative before Q4; the release had a substantial installed base. What was absent was an explicit weighing of those considerations against the consequence profile of a peak-season failure.

Three structural gaps enabled this:

- **No peak-season deployment freeze policy existed.** There was no rule that would have made a November 21 date require executive exception. The date was accepted through normal scheduling channels.
- **No blast-radius framework existed** for classifying changes by consequence. A WMS version upgrade at the primary fulfillment center was scheduled through the same process as a routine patch.
- **Vendor schedule requests were treated as constraints rather than as inputs.** The vendor's deferral was accommodated. It does not appear to have been negotiated, escalated commercially, or treated as a trigger for reassessing whether the upgrade should proceed in 2026 at all.

The schedule shift also had a second-order effect that mattered more than the date itself: it compressed the validation runway. Parallel validation dropped from two weeks to four days. The November date left less time between the vendor's release-candidate delivery and cutover than May would have. The compression was not a decision anyone made deliberately; it was a consequence of the date change that nobody re-derived.

### 5.2 The testing gaps

**The regression suite had not changed since version 9.0.** The suite contained 312 cases built to validate a two-major-version-old system. It tested what 9.0 did. Version 11.0 introduced a location master transformation that had no analogue in any prior upgrade, and therefore no test.

This is the central testing failure, and it is a specific instance of a general pattern: our regression suites are maintained as artifacts of past upgrades rather than as instruments aimed at the current change. Nobody asked "what is new in 11.0, and what tests do we need that we do not have?" The suite was run because running the suite was the process step. It passed, because it tested things that still worked.

**Parallel validation shrank from two weeks to four days.** Two weeks of parallel running against production-representative volume would likely have surfaced the defect through accumulated pick discrepancies. Four days did not, in part because parallel validation was scoped to transaction flows — order intake, wave planning, manifest generation, receiving — rather than to master data integrity. A longer window running the same scope might still have missed it.

**The cutover runbook was the vendor's template.** Step 41, "Validate master data," specified record count matching as its criterion. This is the vendor's generic check. It is adequate for detecting a failed load. It is useless against a transformation that modifies records in place. A facility-specific runbook would have known that location identifier uniqueness is the load-bearing property of the location master at this site, and would have checked it.

**No independent post-cutover data integrity verification existed.** The only master data check was the one in the vendor's runbook. There was no separate, facility-owned verification step performed by someone other than the implementation team. The people validating the upgrade were the people who had just performed it.

### 5.3 The detection gap

Thirty-one hours elapsed between the upgrade completing and anyone knowing something was wrong. The facility shipped approximately 96,000 units in that window. The detection failure has three independent components, each of which alone would have been survivable.

**The quality report runs on a two-shift lag.** This lag is a design characteristic, not a malfunction — the report aggregates completed-shift data and publishes after reconciliation. For its intended purpose, monitoring accuracy trends, a two-shift lag is acceptable. For its actual role in this incident, which was as the facility's only automated accuracy signal, it was fatal. The Monday-morning accuracy collapse was not visible in a system report until Tuesday at 19:00, more than five hours after the incident had already been declared through a customer phone call.

**The exception queue had no owner.** The queue's owner transferred to another function on September 8. Ownership was not reassigned. The queue continued receiving items for nine weeks with no reviewer. During the incident, pickers were filing discrepancy reports into it in volume — the queue contained the signal — and nobody was reading it.

The specific failure is not that a person transferred. It is that a monitoring function could lose its owner and continue to appear operational. The queue had no aging alert, no unreviewed-volume threshold, and no ownership attestation. There was nothing in the system that would notice its own neglect.

**Nothing was watching for the upgrade specifically.** There was no elevated-monitoring posture for the 72 hours following a major version upgrade. No accuracy sampling cadence was increased. No threshold was tightened. The facility returned to steady-state monitoring the moment the upgrade was declared complete, which is precisely when the risk of an upgrade-induced defect is highest.

There is one further factor worth stating plainly. On Sunday afternoon, a shift supervisor noted elevated bin discrepancies and attributed them to post-upgrade settling. That inference was reasonable — post-upgrade friction is real and expected. But "it's probably the upgrade settling in" is an explanation that absorbs anomalies rather than escalating them, and it is most dangerous exactly when an upgrade has actually broken something. The organization has no mechanism that treats post-upgrade anomalies as requiring disproof rather than explanation.

### 5.4 The scanner misdiagnosis

Nine hours were spent rolling back scanner firmware that was not the cause. It is important to be precise about why.

The firmware hypothesis was reasonable. The symptom presented at the scan layer. A scan-layer change had been made six days prior. The WMS upgrade had passed its validation gate, had a large installed base, and had generated no vendor-reported issues. Given the evidence in the room at 14:10 on Tuesday, firmware was a rational first hypothesis.

The failure was not in forming the hypothesis. It was in three things that surrounded it:

**No cheap disconfirmation was attempted before committing to an expensive remediation.** A rollback of 620 devices is a nine-hour, multi-shift operation. A test of the firmware hypothesis on a single zone — roll back twenty devices, sample their output — would have taken under two hours and would have disconfirmed the hypothesis before the full fleet was committed. The incident process had no norm requiring hypotheses to be tested at small scale before being acted on at full scale.

**The most recent change was not treated as the primary suspect.** The WMS upgrade was 34 hours old at the time of the bridge. The firmware was six days old. The upgrade was the larger, more recent, more invasive change, and it was implicitly exonerated by the fact that it had passed its own validation gate — a gate we now know was incapable of catching the defect. A validation gate's passing should never confer immunity from suspicion during an active incident.

**Single-hypothesis pursuit.** From 14:10 Tuesday to 01:00 Wednesday, the bridge pursued one hypothesis and did no parallel investigation. There was no second workstream examining the WMS upgrade, no one diffing master data, no one asking what the upgrade had changed. When the firmware hypothesis died at 01:00 Wednesday, the incident had zero accumulated knowledge to fall back on and started over from nothing.

It is worth noting that the actual root cause was found by someone working outside the incident structure, using data she happened to have for an unrelated purpose, at two in the morning. That is a fortunate outcome, not a repeatable process. Had Lapointe not pulled that export in early November for a slotting analysis, the facility would not have had a known-good reference copy readily available, and root cause identification would have taken substantially longer.

### 5.5 The paper picking tradeoff

The decision to move the building to paper pick sheets on Wednesday morning was correct, and this document states that without qualification. Under the information available at 03:00 Wednesday — no root cause, disconfirmed hypothesis, confirmed 8 percent tote error rate, production volume flowing to customers — continuing to ship at 78,000 units per day would have multiplied the error population by a factor of three or four before root cause was found.

The tradeoff was severe and it was understood at the time:

**What it bought:** It stopped the production of wrong shipments. Paper sheets generated from the pre-upgrade export bypassed the corrupted data entirely. Accuracy on paper picking ran at 98.1 percent — below scan-validated baseline, as expected without system verification, but far above the 91.2 percent the corrupted system was producing. It also, incidentally, produced the diagnostic clue that led Lapointe to root cause: paper worked, scanning did not, therefore the difference was in the data.

**What it cost:** Throughput fell 60 percent, from 78,000 to 31,000 units per day, for two full days before scan picking resumed. Against pre-Black Friday demand, this generated the 214,000-order backlog that took 11 days and $1.8 million in expedited freight to clear. It also imposed a substantial supervisory burden and contributed to the elevated post-incident turnover in the pick function.

The decision was correct. What is worth examining is the absence of intermediate options.

The choice presented on the bridge was effectively binary: full-speed scanning with known errors, or paper at 40 percent throughput. There was no pre-built degraded-operations mode between them. Options that could have existed but did not:

- **Zone-limited scanning.** The defect affected 28.5 percent of locations. Had the facility been able to identify which zones were affected — which it could not, because it did not yet know the nature of the defect — scanning could have continued in clean zones. This was not available because the diagnosis was not available, but a general capability to partition the building by data confidence would have been valuable.
- **Scanning with elevated outbound QC on a sampled basis.** Rejected as all-or-nothing, but a partial inspection regime targeted at high-value or high-sensitivity client orders was not considered.
- **A pre-built paper fallback.** Paper pick sheets had to be generated and distributed ad hoc on Wednesday morning. The facility has no maintained, tested paper picking procedure. Sheet formats, distribution logistics, and reconciliation processes were improvised, which cost throughput beyond the inherent slowness of paper.

The absence of a maintained fallback mode meant the facility paid full price for the safest option because no cheaper safe option existed.

### 5.6 Client communication

Client Services performed well under difficult conditions, and this is treated in Section 6. The contributing factor worth noting here is structural: notification began at 08:00 Wednesday, approximately 21 hours after the incident was declared and more than 51 hours after the first wrong shipments left the building. The delay was not a Client Services decision — Client Services notified as soon as it had a picture worth communicating.

The gap is that there was no protocol requiring client notification at Sev-1 declaration regardless of diagnostic status. The implicit norm was to notify once there was something to say. In an incident where diagnosis took 62 hours, that norm produced a two-day silence toward clients who were, during that silence, receiving wrong product.

The client that issued termination notice cited the notification delay specifically in its correspondence, above the accuracy failure itself.

---

## 6. What worked

**The paper picking decision.** Made quickly, on incomplete information, against significant throughput cost, and correct. It stopped error production and produced the diagnostic contrast that led to root cause.

**Independent investigation outside the incident structure.** Lapointe's diff against a pre-upgrade export was the single action that resolved the incident. It came from someone who was not on the primary diagnostic path, working from data she held for another purpose, testing a hypothesis nobody on the bridge had formed. Organizations benefit from people who investigate sideways. This one should be structurally encouraged, not left to chance.

**The pre-upgrade export existed at all.** The reporting environment held a location master copy that predated the upgrade. It enabled both paper sheet generation and root cause identification. It existed because of an unrelated slotting analysis, not by design.

**Hypothesis abandonment.** When post-rollback sampling disconfirmed the firmware hypothesis at 01:00 Wednesday, the hypothesis was dropped within 75 minutes. Nine hours had been invested. There was no attempt to rescue it. That is disciplined incident behavior and it is not universal.

**Remediation execution.** From root cause identification at 02:00 Thursday to validated remediation at 21:40 Thursday was 19 hours 40 minutes, including vendor engagement, script development, testing against a restored copy, production execution, and physical scan verification of a 1,200-location sample. The decision to reconcile the full 214,000-record population rather than repair only the 61,000 identified records was correct — it did not assume the diff had found everything.

**Client Services execution.** Once notification began, Whitehorse maintained twice-daily updates to all 14 brands for 14 consecutive days, coordinated returns processing for 11,400 affected orders, and negotiated service credit terms with two clients. Twelve of fourteen brands remained without credit claims. This was substantially harder than it appears in summary.

**Backlog recovery.** 214,000 orders cleared in 11 days while running normal incoming demand, through overtime, weekend shifts, and temporary staffing. Recovery ran ahead of the initial 14-day estimate.

**Blameless incident conduct.** Twenty-three interview participants spoke candidly. No participant declined. This document exists in usable form because people described what they actually did and thought, including where they were wrong. That is a property of the organization worth protecting.

---

## 7. What did not work

**Master data validation.** Record counts as the sole criterion for validating a transformation that modifies records in place. The check could not have detected the defect under any circumstances.

**The regression suite.** Two major versions stale. Tested nothing that 11.0 introduced. Passing it created false confidence.

**Parallel validation scope and duration.** Four days instead of two weeks, and scoped to transaction flows rather than master data integrity.

**The cutover runbook.** Vendor template with names substituted. No facility-specific knowledge of what matters at this site.

**Detection.** Thirty-one hours to detect, and detection came from a customer. The quality report's two-shift lag made it useless for incident detection. The exception queue had no owner and held the signal unread.

**Monitoring ownership integrity.** A monitoring function lost its owner in September and continued to appear operational for nine weeks. Nothing in the system noticed.

**Post-upgrade monitoring posture.** No elevated monitoring for the highest-risk period. Steady-state monitoring resumed at 04:10 Sunday.

**Diagnostic method.** Single-hypothesis pursuit for eleven hours. No cheap disconfirmation before expensive remediation. No parallel workstream. Implicit exoneration of the most recent and most invasive change because it had passed a gate.

**Absence of a degraded-operations mode.** Binary choice between full-speed-with-errors and paper-at-40-percent. No maintained fallback, no partition capability, no intermediate posture.

**Client notification timing.** Fifty-one hours from first wrong shipment to first client notification, driven by an implicit norm of notifying only once diagnosis exists.

**Vendor defect disclosure.** The vendor had observed a related defect at a prior site and had not published it. Our vendor management process had no mechanism that would have surfaced it.

**Schedule governance.** No peak-season freeze policy. No blast-radius classification. No formal risk assessment on the date change. No re-derivation of validation runway after the schedule moved.

---

## 8. Action items

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Establish a peak-season deployment freeze (October 15 – January 15) covering all WMS, host, and material-handling system changes at all facilities. Exceptions require written executive approval with documented risk assessment. | Bianca Cardoso-Reyes | Feb 13, 2027 |
| 2 | Define and publish a change blast-radius classification. Class 1 (facility-wide system version changes) requires independent validation, executive go/no-go, and a documented rollback plan with tested execution time. | Ephraim Sackey | Mar 6, 2027 |
| 3 | Rebuild the WMS regression suite against version 11.0. Establish a standing requirement that every version upgrade produce net-new test cases covering every changed data transformation, with sign-off that the delta has been enumerated. | Marguerite Lapointe | Apr 17, 2027 |
| 4 | Replace record-count master data validation with an integrity validation standard: field-level diff against pre-change export, uniqueness constraint verification on all identifier fields, and referential integrity checks. Applies to all master data objects. | Ephraim Sackey | Feb 27, 2027 |
| 5 | Establish mandatory pre-upgrade export and retention of all master data objects, with automated post-cutover diff. Retention 90 days minimum. Diff results reviewed by a party independent of the implementation team. | Ephraim Sackey | Feb 27, 2027 |
| 6 | Replace the vendor cutover runbook template with a facility-owned runbook for Rome, including site-specific validation criteria for every master data object. Review annually and after every version upgrade. | Marguerite Lapointe | Mar 20, 2027 |
| 7 | Restore parallel validation to a two-week minimum for Class 1 changes. Prohibit compression without executive approval. Require validation runway to be re-derived and re-approved whenever a cutover date moves. | Bianca Cardoso-Reyes | Feb 13, 2027 |
| 8 | Implement near-real-time pick accuracy monitoring with a maximum four-hour data lag and automated alerting at 99.0% (warning) and 98.0% (page). Retain the existing two-shift report for trend analysis; it is not a detection instrument. | Marguerite Lapointe | May 15, 2027 |
| 9 | Implement ownership attestation for all monitoring queues and exception queues: named owner, quarterly re-attestation, automatic alert on unreviewed volume threshold and item aging beyond 24 hours. Audit all existing queues for orphaned ownership. | Marguerite Lapointe | Mar 13, 2027 |
| 10 | Add monitoring-ownership transfer to the standard internal transfer checklist. No transfer completes without explicit reassignment of every monitoring responsibility held. | Bianca Cardoso-Reyes | Feb 6, 2027 |
| 11 | Define a 72-hour post-upgrade elevated monitoring posture: hourly accuracy sampling at 3x normal rate, tightened alert thresholds, named on-call owner per shift, and an explicit stand-down decision at 72 hours. | Marguerite Lapointe | Mar 6, 2027 |
| 12 | Establish an incident diagnostic protocol requiring (a) minimum two hypotheses under parallel investigation, (b) cheap disconfirmation testing before any remediation exceeding two hours, and (c) explicit examination of the most recent change regardless of validation status. | Ephraim Sackey | Mar 20, 2027 |
| 13 | Build and maintain a tested degraded-operations playbook: pre-formatted paper pick sheets, zone-partitioned scanning capability, sampled-QC inspection protocol, and documented throughput expectations for each mode. Exercise semi-annually. | Bianca Cardoso-Reyes | Jun 12, 2027 |
| 14 | Establish a client notification protocol requiring initial notification within four hours of Sev-1 declaration regardless of diagnostic status, with a standard "we do not yet know" template and committed update cadence. | Tanya Whitehorse | Feb 20, 2027 |
| 15 | Add contractual requirements to the Baseline vendor agreement covering defect disclosure across the installed base, root cause documentation within 10 business days, and a schedule-change clause with commercial consequence. Escalate the undisclosed prior-site defect. | Ephraim Sackey | Apr 3, 2027 |
| 16 | Conduct a location master integrity audit at all Tannery Row facilities running Baseline 11.0 or scheduled to upgrade, verifying identifier uniqueness and aisle prefix integrity. | Marguerite Lapointe | Feb 6, 2027 |
| 17 | Establish a quarterly cross-functional review of monitoring coverage: for each critical operational metric, document the detection instrument, its lag, its alert threshold, and its named owner. Identify metrics whose only detection path is a customer. | Marguerite Lapointe | Apr 30, 2027 |
| 18 | Conduct client relationship recovery review for all 14 brands. Produce a written remediation plan for the client under termination notice and a retention risk assessment for the remaining 13. | Tanya Whitehorse | Feb 6, 2027 |
| 19 | Review pick-function retention data at 30/60/90 days post-incident and produce a workforce impact assessment with retention actions if elevated turnover persists. | Bianca Cardoso-Reyes | Mar 6, 2027 |
| 20 | Schedule a 90-day review of all action items in this document, with status reported to the Executive Committee. Items not complete require written explanation and revised date. | Marguerite Lapointe | Mar 18, 2027 |

---

## 9. Closing note

The most uncomfortable fact in this document is that the facility shipped approximately 96,000 units over 31 hours without knowing anything was wrong, and learned it was wrong because a customer called. Every internal signal that could have surfaced the problem either ran too slowly to matter or had no one attached to it. The building was operating without functional detection, and had been for nine weeks before the upgrade ever ran.

The second most uncomfortable fact is that this was found by someone who was not assigned to find it, using data she happened to have, at two in the morning. The organization was fortunate. Fortune is not a control.

Nothing in this incident required extraordinary failure. A vendor shipped a defect — vendors do. A validation check was too shallow — checks often are. A person transferred and a queue was orphaned — this happens continuously in every organization. A reasonable hypothesis was wrong — most first hypotheses are. Each of these is ordinary. What made them catastrophic was that they aligned, in peak season, at the facility that carries the most volume, with nothing in the path capable of stopping the sequence.

The work ahead is not to prevent ordinary failures. It is to build a facility in which ordinary failures stop being able to line up.
