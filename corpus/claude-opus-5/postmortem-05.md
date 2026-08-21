# Incident Postmortem — Lab Results Interface Filing Failure (INC-2027-0219)

**Housatonic Valley Health | Clinical Informatics & Laboratory Services**

| Field | Value |
|---|---|
| Incident ID | INC-2027-0219 |
| Title | Undetected queue-hold of microbiology and critical chemistry results following Confluence 7.4.2 vendor patch |
| Severity | SEV-1 (retroactively classified; initially triaged SEV-3) |
| Systems | Confluence Interface Engine v7.4.2; Laboratory Information System (LIS); Analyzer Middleware (Chemistry/Micro); Electronic Health Record (EHR) |
| Defect window | Sun 07 Feb 2027 22:15 – Wed 10 Feb 2027 20:00 EST (~69h 45m from patch to remediation; 62h 15m to detection) |
| Detection | Wed 10 Feb 2027 12:30 EST, clinician-initiated |
| Operational close | Fri 12 Feb 2027 18:00 EST |
| Regulatory filing | Sat 13 Feb 2027 (CT DPH reportable event) |
| Incident Commander | Dr. Yusuf Abdullahi, Chief Medical Information Officer |
| Postmortem author | Clinical Informatics, with Integration Engineering and Laboratory Services |
| Quality review chair | Dr. Elena Vasilenko, VP Quality & Patient Safety |
| Published | 27 Feb 2027 |
| Status | Final — action items in flight |

---

## 1. Purpose and framing

This document reconstructs what happened between 07 and 13 February 2027, states the measurable impact, and identifies the systemic conditions that allowed a routine vendor patch to remove 1,460 laboratory results from clinical view for more than two and a half days without any automated signal.

This review is conducted under Housatonic Valley Health's blameless postmortem policy. Every person named here acted on the information their tools and procedures presented to them. Where a decision produced a poor outcome — a restart that consumed three hours, a replay that generated 4,800 duplicates — the review asks what made that decision reasonable at the time, and what would have to change for a different decision to be the obvious one. The findings target instrumentation, test coverage, escalation design, procedure currency, and tooling. They do not target individual judgment, and no portion of this document may be used in performance evaluation.

Reader note: all times are Eastern Standard Time. Message counts are drawn from Confluence queue audit tables and LIS-to-EHR reconciliation logs assembled by the reconciliation cell between 11 and 12 February.

---

## 2. Summary

Housatonic Valley Health operates two acute-care hospitals (480 licensed beds) and 22 ambulatory clinics in and around Danbury, Connecticut, with 6,100 employees. Laboratory results flow from analyzer middleware into the Confluence interface engine, which transforms and routes them into the electronic health record. Steady-state volume is approximately 19,000 messages per day.

At 22:15 on Sunday, 07 February 2027, Integration Engineering applied vendor patch 7.4.2 to Confluence during an approved standard-change window. The patch included an undocumented-in-summary change (vendor line item CI-4471) to how the engine parses repeating fields and extended abnormal-flag values within the observation segment of result messages.

Two categories of message stopped filing:

- **Microbiology results containing more than three organism entries** — these use repetition separators in the observation value field beyond the count the new parser tolerated under its stricter schema check.
- **Chemistry results carrying a critical abnormal flag** — these populate an extended flag value that the new parser rejected as schema-invalid.

Critically, the patch also changed the *disposition* of schema-validation failures. Under 7.4.1, a message that failed transformation was rejected, written to the error queue, incremented the error counter, and raised a dashboard alert. Under 7.4.2, such a message was placed in a `PENDING_TRANSFORM` holding state with a retry counter that never incremented. It did not error. It did not appear in the failure count. The interface dashboard, whose health indicator is derived from process liveness and error rate, remained green for the entire event.

Over the following 62 hours and 15 minutes, 1,120 microbiology results and 340 critical chemistry results accumulated in the hold queue and never reached a patient chart. Confluence generated 216 queue-depth warnings during this period. All 216 routed to a distribution list that had been emptied of members during a December 2025 reorganization and had zero recipients for 14 months.

Detection occurred at 12:30 on Wednesday, 10 February, when hospitalist Dr. Simone Kellerman telephoned the microbiology bench about a blood culture ordered Monday morning that showed no result in the chart. The laboratory confirmed the result had been verified in the LIS on Monday at 14:12.

Initial diagnosis focused on the analyzer middleware — the component with a prior history of hung sessions and the one that had *not* been changed. Gerard Thibodeaux, Manager of Integration Engineering, restarted middleware services twice. Approximately three hours elapsed before a direct query against the Confluence queue tables revealed 1,460 messages in a holding state.

Colleen Brannigan, Director of Laboratory Services, activated manual results reporting at 16:40. The downtime procedure in use dated from 2019 and listed 31 fax destinations, 11 of which corresponded to nursing units that had been renamed, consolidated, or closed in the intervening eight years. Manual reporting reverted to telephone, absorbing four laboratory staff for the remainder of the evening.

At 20:15 the held queue was replayed. The replay tooling stamped each message with the replay timestamp rather than preserving the original specimen collection and verification times, and applied no duplicate suppression against results that had already been entered manually or filed on retry. Four thousand eight hundred duplicate observations landed in charts, sorted to the top of results displays as though newly drawn, showing values that conflicted with the manually reported figures nurses had transcribed hours earlier. The replay was halted at 20:52.

Dr. Yusuf Abdullahi assumed formal incident command at 21:00. Tamika Osei-Bonsu, Chief Nursing Informatics Officer, stood up a reconciliation cell that worked continuously until 17:20 Friday. Dr. Elena Vasilenko chaired the quality review beginning 15 February.

Nine patients experienced antibiotic regimen changes delayed by more than 24 hours. Two of those nine were readmitted within 30 days. One case was referred to sentinel event review. The system filed a reportable event with the Connecticut Department of Public Health on 13 February.

---

## 3. Impact in numbers

### 3.1 Message and data impact

| Measure | Value |
|---|---|
| Duration, patch to detection | 62 hours 15 minutes |
| Duration, patch to remediation | 69 hours 45 minutes |
| Duration, patch to reconciliation close | 8 days 0 hours (07 Feb 22:15 – 12 Feb 18:00 operational; harm review continuing) |
| Total messages processed during defect window | 49,062 |
| Messages held and not filed | 1,460 (2.98% of window volume) |
| — Microbiology results (>3 organism entries) | 1,120 |
| — Critical-flagged chemistry results | 340 |
| Messages lost permanently | 0 (queue persistence held all messages) |
| Duplicate observations created by replay | 4,800 |
| Total observations requiring manual reconciliation | 6,260 |
| Confluence queue-depth alerts generated | 216 |
| Confluence queue-depth alerts received by a human | 0 |
| Days the alert distribution list had zero members | 428 (14 months) |
| Days the 7.4.2 patch was available before application | 179 |
| Message types in interface regression suite | 40 of 218 (18.3%) |
| Regression fixtures containing >3 repeating organism entries | 0 |
| Regression fixtures containing extended critical abnormal flags | 0 |
| Synthetic messages in post-patch smoke test | 12 |
| Smoke-test messages matching either affected pattern | 0 |

### 3.2 Patient impact

| Measure | Value |
|---|---|
| Unique patients with at least one held result | 1,214 |
| — Inpatient / observation | 741 |
| — Emergency department | 191 |
| — Ambulatory clinic | 282 |
| Patients discharged before their held result filed | 47 |
| Patients with antibiotic change delayed >24 hours | 9 |
| — Median delay among those nine | 38 hours |
| — Maximum delay | 61 hours |
| Patients among the nine readmitted within 30 days | 2 |
| Cases referred to sentinel event review | 1 |
| Deaths attributed to the event | 0 |
| Cases classified as harm (NCC MERP E or above) | 4 |
| Cases classified as no-harm reaching-patient events | 1,210 |
| Patients or families receiving formal disclosure | 9 (plus 2 estates/proxies contacted for readmission review) |
| Charts requiring correction of duplicate/misdated entries | 1,038 |

### 3.3 Operational and organizational impact

| Measure | Value |
|---|---|
| Laboratory staff hours diverted to telephone reporting | 68 |
| Results phoned manually, 17:30 Wed – 22:00 Thu | 611 |
| Reconciliation cell headcount | 22 (nursing informatics, lab, pharmacy, HIM) |
| Reconciliation cell duration | 41 hours continuous |
| Total incident labor hours (all functions) | ~840 |
| Antimicrobial stewardship chart sweeps performed | 1,214 |
| Fax destinations in 2019 downtime binder | 31 |
| Fax destinations invalid or decommissioned | 11 (35.5%) |
| Estimated direct cost (labor, vendor engagement, corrections) | ~$410,000 |
| Regulatory filings | 1 (CT DPH, 13 Feb 2027) |

---

## 4. Timeline

### 4.1 Antecedent conditions

**December 2025 (specific date not recoverable).** An IT reorganization dissolves the standing Interface Operations team and redistributes its duties into Integration Engineering and Application Services. Group membership in the mail distribution list `confluence-alerts@hvhealth.org` is cleared as part of account cleanup. The list object is not deleted; it continues to accept mail and deliver it to no one. Confluence's alert configuration is not reviewed as part of the reorganization checklist, because the reorganization checklist has no line item for application-level notification targets.

**12 Aug 2026.** Vendor releases Confluence 7.4.2. Release notes list 31 items. Item CI-4471 reads: *"Improved schema conformance for repeating field parsing and extended flag value handling in observation segments. Non-conforming messages now held for operator review rather than rejected."* No clinical-impact rating accompanies the item. The release is categorized by the vendor as a maintenance release.

**Aug 2026 – Jan 2027.** The patch is scheduled and deferred five times: twice for competing EHR upgrade windows, twice for month-end financial close freezes, once for holiday change moratorium. Each deferral is documented and approved. The change record accumulates 179 days of age.

**21 Jan 2027.** Change Advisory Board reviews CHG-0044817. The change is classified **Standard — Low Risk** on the basis of three criteria: vendor-supplied maintenance release, no schema or mapping changes authored in-house, and successful application in the vendor's reference environment. The CAB record notes "no clinical validation required for vendor maintenance releases." Approved unanimously.

**02 Feb 2027.** Patch applied to the Confluence test environment. The interface regression suite executes 40 message types and passes at 100%. The suite does not contain a microbiology message with more than three organism repetitions, nor a chemistry message with an extended critical abnormal flag. The pass result is recorded as full validation.

### 4.2 Sunday, 07 February 2027

**21:00** — Pre-change snapshot of Confluence configuration and queue state captured. Baseline queue depth: 14 messages.

**22:15** — **Patch 7.4.2 applied to production Confluence.** Engine restart completes 22:19.

**22:31** — Post-change smoke test executed: 12 synthetic messages (4 chemistry routine, 4 hematology, 2 radiology, 2 ADT). All file successfully within expected latency. None carries more than three repeating fields; none carries a critical abnormal flag.

**22:52** — Change record CHG-0044817 closed as successful. On-call handoff notes read: "Confluence 7.4.2 in prod, clean smoke, dashboard green."

**23:41** — First microbiology result with four organism entries enters Confluence. It is parsed, fails the new schema check, and is written to `PENDING_TRANSFORM` with retry count 0. No error is logged. No alert fires from the error channel. The message does not appear in the failed-message view.

### 4.3 Monday, 08 February 2027

**00:12** — First critical-flagged chemistry result (a potassium of 6.4) enters the hold queue. It is not filed. The LIS has already auto-generated a critical-value call task, and the laboratory technologist telephones the unit at 00:20 per critical value policy. The nurse documents the verbal report in a nursing note. *This telephone practice, which applies to critical chemistry but not to routine microbiology, is the single largest reason the event did not produce more severe harm.*

**03:17** — Confluence queue-depth threshold (250 messages held) is crossed. Alert #1 generated and delivered to `confluence-alerts@hvhealth.org`. Zero recipients.

**07:30** — Day shift begins. Interface dashboard displays: engine up, throughput 19.1k/day trailing, error rate 0.02%, status **GREEN**.

**09:20** — A microbiology technologist takes a call from a 4-West nurse asking about a wound culture. The technologist reads the result over the phone and notes the LIS shows the result verified and transmitted. The discrepancy is logged as a single "result not visible" service note, closed same-day, and not aggregated anywhere.

**13:00** — Held queue passes 500 messages. Alerts #14 through #22 generated. Zero recipients.

**14:12** — The blood culture that will eventually surface the incident is verified in the LIS for a patient on 6-North, ordered by Dr. Simone Kellerman that morning. It contains four organism entries. It enters the hold queue.

**16:45** — A second "result not visible" service note is opened, this time by an ED charge nurse. It is closed by pointing the nurse to the LIS web viewer, where the result is present. No pattern is drawn between this note and the morning's.

**22:00** — Held queue: 892 messages.

### 4.4 Tuesday, 09 February 2027

**02:40** — A hospitalist covering nights requests a laboratory printout for two patients whose cultures "aren't showing up." Laboratory prints and delivers. No ticket is opened; the exchange is treated as ordinary service.

**08:00** — Interface dashboard: **GREEN**. Daily interface health report distributed to IT leadership shows zero failed messages in the prior 24 hours. The report does not include queue depth by state.

**11:30** — Ambulatory clinics begin experiencing the same gap for outpatient cultures. Because ambulatory results are typically reviewed 24–72 hours after collection, no clinic escalates during the defect window.

**19:00** — Held queue: 1,247 messages. Alerts #147 through #161 generated. Zero recipients.

### 4.5 Wednesday, 10 February 2027 — Detection and response

**12:30** — **DETECTION.** Dr. Simone Kellerman telephones the microbiology bench directly regarding the 6-North blood culture ordered Monday. She has checked the chart twice and asked the unit clerk to re-query. The result is not there. She asks the technologist to look at the LIS.

**12:41** — Laboratory confirms: result verified Monday 14:12, transmission status in LIS shows "sent." Dr. Kellerman asks the technologist to check two other patients on her list. Both cultures are also verified in the LIS and absent from the chart. The technologist escalates to the microbiology supervisor.

**12:58** — Service desk ticket INC-2027-0219 opened. Ticket category selected: **"Results — display question."** This category carries a default priority of **P3** with a 4-hour response target. The ticket text mentions three patients.

**13:20** — Ticket routed to Gerard Thibodeaux, Manager of Integration Engineering. He opens the Confluence dashboard. Status **GREEN**, error rate 0.02%, throughput nominal. He opens the failed-message view: empty for the prior 72 hours.

**13:32** — Thibodeaux checks the analyzer middleware. In the preceding 18 months, the middleware has been the cause of six of eight result-delivery incidents, typically presenting as hung sessions with a healthy-looking upstream. The dashboard's green status and empty error queue are, given every prior incident, strong evidence that Confluence is fine. He forms the hypothesis that middleware sessions are hung.

**13:50** — **First middleware restart.** Services cycle cleanly in 6 minutes. Thibodeaux asks the laboratory to re-transmit one of the three named results.

**14:22** — Re-transmitted result does not appear in the chart. Thibodeaux checks middleware session logs: all sessions active, all acknowledgments received from Confluence. He interprets the acknowledgments as confirmation that Confluence accepted and processed the messages — which is technically true; Confluence did accept them, and then held them.

**14:55** — Thibodeaux contacts the middleware vendor's support line and opens a case. Hold time and initial triage consume 40 minutes.

**15:35** — **Second middleware restart**, this time including the interface adapters, at the middleware vendor's suggestion. Clean cycle.

**16:02** — Third re-transmission fails to appear. Thibodeaux abandons the middleware hypothesis. He connects directly to the Confluence database rather than the dashboard and runs a state-count query against the queue table.

**16:11** — **Root symptom found.** Query returns 1,431 messages in `PENDING_TRANSFORM`, oldest timestamp Sunday 23:41. Thibodeaux immediately correlates the oldest timestamp with the 22:15 patch window.

*Elapsed time from engineering engagement to correct system identification: 2 hours 51 minutes.*

**16:18** — Thibodeaux raises severity to **P1** and pages the Director of Application Services and the on-call laboratory leader.

**16:24** — Colleen Brannigan, Director of Laboratory Services, joins. Thibodeaux breaks the held message counts down by type: microbiology and critical chemistry, nothing else. Brannigan recognizes the clinical exposure immediately.

**16:40** — **Manual results reporting activated** across both hospitals. Brannigan invokes the Laboratory Downtime Reporting Procedure (LAB-DT-004, revision date 11 March 2019).

**16:55** — The procedure's fax distribution fails. Of 31 destinations, 11 are invalid: 3 units closed in the 2021 tower consolidation, 5 renamed, 2 with numbers reassigned to non-clinical departments, 1 with a transposed digit that has apparently been wrong since the document was written. Two faxes are confirmed delivered to a decommissioned number that still answers. Laboratory staff spend 35 minutes attempting delivery.

**17:30** — Brannigan abandons fax and shifts to **telephone-only reporting**, pulling four technologists off bench to the phones and requesting agency coverage for the evening. Priority order established: current inpatients with pending cultures, then ED, then discharged patients, then ambulatory.

**17:52** — Confluence vendor engaged at severity 1. Case CTL-88431 opened.

**18:10** — Dr. Yusuf Abdullahi, CMIO, is briefed by telephone and begins to travel in.

**18:45** — **Vendor confirms the defect.** Engineering support identifies CI-4471 as the cause and confirms the changed failure disposition. The vendor states that a hotfix exists in internal testing but is not released, and recommends reverting the parser conformance setting to legacy mode via configuration flag rather than rolling back the full patch.

**19:20** — Configuration flag `parser.schema.strict=false` applied and engine restarted. Test message with four organism entries files successfully in 11 seconds. Test message with critical flag files successfully.

**19:48** — Discussion of how to deliver the 1,460 held messages. Options considered: (a) replay the queue through the now-corrected engine; (b) have the LIS re-transmit all results from the window; (c) manual entry only. Option (a) is selected on the reasoning that the queue holds the authoritative original messages, that replay is a single operation, and that manual entry of 1,460 results is infeasible. **No dry run is performed and no dedup check is run against results already reported manually or already present from LIS retries.** The replay utility's timestamp behavior is not examined; the team's mental model is that the message carries its own collection and verification times in the segment fields, which it does — but the utility overwrites the message header and observation datetime with the replay clock.

**20:15** — **Queue replay initiated.**

**20:26** — First nursing call: a 5-East nurse reports two potassium values on the same patient, minutes apart, with different results, both timestamped within the last ten minutes. She has already held a scheduled dose pending clarification.

**20:33** — Second and third calls. A charge nurse on 6-North reports a culture result showing a collection time of "tonight" for a specimen she knows was drawn Monday.

**20:41** — Nursing supervisors begin calling the command line. Replay message count at this point: approximately 4,800 delivered.

**20:52** — **Replay halted.** Remaining queue contents held.

**21:00** — **Dr. Yusuf Abdullahi assumes formal incident command.** He establishes a single command structure, opens a bridge line, and assigns roles: Thibodeaux — technical remediation; Brannigan — laboratory operations and manual reporting; Osei-Bonsu — clinical reconciliation and nursing communication; Application Services Director — vendor liaison and documentation.

**21:15** — Abdullahi's first directive: **stop all automated remediation.** No further replay, no further bulk operations, until the reconciliation approach is defined. This decision is the inflection point of the response.

**21:30** — Scope assessment completed: 1,460 originally held results, of which approximately 4,800 duplicate observations have now been created (a single held message often produces multiple observation rows; the 4,800 count is observations, not messages).

**22:05** — **Enterprise clinical communication issued.** EHR banner message and overhead notification to all inpatient units: "Laboratory results displayed with timestamps after 20:00 on 10 February may be duplicates with incorrect collection times. Do not act on new lab values without verbal confirmation from the laboratory. Call the laboratory at extension 4400 for verification."

*Elapsed time from first duplicate reaching a nurse to enterprise notification: 1 hour 39 minutes.*

**22:40** — Pharmacy leadership engaged. Danielle Corcoran, Director of Pharmacy, begins an antimicrobial stewardship sweep against the list of 1,214 affected patients.

**23:10** — Command decides against automated deletion of duplicates. Rationale: automated correction had just produced the current problem, and Health Information Management requires documented chart correction rather than silent removal. **Manual reconciliation with per-chart annotation is selected.**

### 4.6 Thursday, 11 February 2027 — Reconciliation

**00:30** — Tamika Osei-Bonsu stands up the reconciliation cell in the Danbury campus classroom: 22 people drawn from nursing informatics, laboratory, pharmacy, and HIM, working in 6-hour rotations. Method: for each of the 1,214 patients, compare LIS source of truth against chart contents; correct or annotate every observation; confirm the true collection and verification times; document a chart correction note.

**02:00** — Reconciliation workflow validated on a sample of 20 charts. Average handling time: 11 minutes per patient. Projected completion: 38–44 hours.

**06:00** — Shift huddle scripts distributed to all inpatient units, ED, and clinics. Nursing leadership delivers the same message at every huddle for the next four shifts.

**08:00** — Corcoran reports the first antimicrobial findings: 9 patients where a culture and sensitivity result, had it been visible, would have prompted a regimen change that in fact occurred more than 24 hours later. All nine are escalated to Risk Management and to Dr. Vasilenko.

**09:15** — Ambulatory outreach begins for the 282 clinic patients and the 47 patients discharged before their result filed. Clinic managers receive patient lists; primary care and specialty offices place calls.

**10:30** — Vendor delivers hotfix 7.4.2-HF1 for staging. Command declines production application during the active incident; the configuration flag is holding.

**12:00** — Command briefing. Dr. Abdullahi confirms: no permanent data loss; all 1,460 messages accounted for; reconciliation on schedule; harm review underway.

**14:20** — Root cause confirmed jointly with vendor engineering, including reproduction in the test environment: a microbiology message with four organism repetitions is held under `strict=true` and files under `strict=false`.

**16:00** — Remaining held messages (those not delivered in the halted replay) are filed under supervision, individually verified in batches of 25 against the LIS, with original timestamps confirmed before each batch is released.

**19:30** — Interim monitoring deployed: a query-based check on `PENDING_TRANSFORM` depth running every 5 minutes, paging the Integration Engineering on-call phone directly — not a distribution list. Built and tested in 90 minutes.

**22:00** — **All 1,460 originally held results confirmed present and correctly timestamped in the patient record.**

### 4.7 Friday, 12 February 2027 — Close

**08:00** — Reconciliation cell enters final third: 391 charts remaining.

**11:45** — Laboratory stands down telephone-only reporting. Automated filing has run 15 hours without a hold.

**14:00** — Dr. Vasilenko convenes the initial harm review with Risk Management, Infection Prevention, Pharmacy, and the attending physicians of the nine flagged patients.

**17:20** — **Reconciliation complete.** 1,214 patients reviewed; 1,038 charts corrected; 6,260 observations verified.

**18:00** — Dr. Abdullahi declares the incident operationally closed and transfers ownership to the quality review.

### 4.8 Post-incident

**13 Feb (Sat)** — Reportable event filed with the Connecticut Department of Public Health, within the statutory window.

**15 Feb (Mon)** — Sentinel event review chartered for one case: a patient whose bacteremia with an organism resistant to the empiric regimen went 61 hours without regimen change, and who was readmitted on day 19.

**17 Feb** — Formal disclosure conversations completed with 9 patients or families, led by attending physicians with Risk Management support.

**19 Feb** — Confluence 7.4.2-HF1 applied to production during a change window with full clinical validation using production-representative message fixtures, including both affected patterns. Strict parsing re-enabled with corrected handling.

**24 Feb** — Quality review committee, chaired by Dr. Vasilenko, reviews draft findings.

**27 Feb** — This postmortem published.

---

## 5. Root cause

**A vendor patch simultaneously tightened message validation and changed the failure disposition from "reject and alert" to "hold silently," while the organization's only automated health signal measured errors rather than queue state. The change was approved without clinical validation because it was categorized as a low-risk vendor maintenance release, and it was tested against a regression suite covering 18% of message types that contained no fixture matching either affected pattern.**

The causal chain has four links, and severing any one of them would have prevented or sharply shortened the event:

**Link 1 — The parsing change.** Confluence 7.4.2 applied stricter schema conformance to repeating fields and extended flag values in observation segments. Microbiology results with more than three organism repetitions and chemistry results with critical abnormal flags failed the new check. This alone is an ordinary compatibility defect; such defects are expected and are why validation exists.

**Link 2 — The disposition change.** The same patch changed non-conforming messages from *rejected* to *held for operator review*. This converted a loud failure into a silent one. The vendor's design assumption was that an operator watches the review queue; the organization had no such role and no such workflow. The patch's safety model depended on a human function that did not exist here, and nothing in the deployment process checked for that dependency.

**Link 3 — The monitoring blind spot.** The interface dashboard derives health from process liveness and error rate. `PENDING_TRANSFORM` is neither down nor an error. The dashboard was accurate and useless: it correctly reported that the engine was running and not producing errors, which was precisely the condition the defect created. The organization had no service-level objective on queue depth, no objective on message age, and no reconciliation control comparing results verified in the LIS against results filed in the EHR.

**Link 4 — The dead alert channel.** Confluence did detect the condition. It fired 216 queue-depth warnings. Every one went to a distribution list that had been emptied 14 months earlier and never re-populated. There was no synthetic test of the alert path, no requirement that alert destinations be a monitored on-call rotation rather than a mailbox, and no line item in the reorganization checklist for application notification targets.

Had Link 2 not existed, the error queue would have filled and paged within minutes. Had Link 3 not existed, queue depth would have breached an SLO by 03:17 Monday. Had Link 4 not existed, 216 pages would have arrived. The event required all four to hold simultaneously — which is a description of how latent conditions accumulate, not a description of bad luck.

---

## 6. Contributing factors

**6.1 Regression coverage of 18%.** The interface regression suite exercises 40 of 218 message types. Coverage was built incrementally around historically failure-prone interfaces and was never mapped against clinical criticality. Microbiology with high organism counts and critical-flagged chemistry — the two highest-acuity result categories in the catalog — were among the 178 untested types. Coverage percentage was reported to governance as a raw number without a criticality weighting, which made 40/218 look like progress rather than exposure.

**6.2 Change classification decoupled from clinical impact.** CHG-0044817 was classified Standard/Low Risk because the vendor authored it, not because anyone assessed what it touched. The classification rubric asks about the *origin* and *scope of authorship* of a change but not about the *clinical criticality of the data path*. Any change to the results interface moves critical patient data, regardless of who wrote it.

**6.3 Non-representative smoke testing.** The post-change smoke test used 12 synthetic messages selected for convenience and speed. Synthetic fixtures were built years earlier to test connectivity, not content variety. A smoke test drawn from de-identified production traffic would have included high-repetition microbiology within the first few dozen messages.

**6.4 Release notes read for scope, not for meaning.** CI-4471 described the disposition change in plain language. It was read — the change record cites the note count — but the phrase "held for operator review rather than rejected" was not recognized as a change in failure behavior requiring a corresponding operational change. There is no structured review step that asks, of each release note item, "what does this change about how we would learn something is wrong?"

**6.5 Patch age and deferral pressure.** The patch sat available 179 days across five deferrals. Deferral is often correct, but aged changes accumulate two costs: the applying engineer is further from the original evaluation, and pressure builds to clear the backlog with minimal friction. By January the change had been reviewed so many times that re-examining it felt redundant.

**6.6 Change window with thin coverage and no soak period.** The change was applied at 22:15 Sunday with a single engineer on site and an on-call handoff at 22:52. There was no defined soak window during which someone actively watched clinical message flow. Fifteen hours elapsed between the change and the next business-hours look at the interface, and that look was a dashboard glance.

**6.7 Near-miss signals with no aggregation path.** At least four separate "result not visible" contacts occurred Monday and Tuesday — two service notes, one printout request, one direct call. Each was resolved individually and closed. No mechanism aggregates low-severity result-availability complaints, and no threshold exists that converts a cluster into an escalation. Four independent people saw a piece of the incident and had nowhere to put it.

**6.8 Ticket category driving severity.** The detecting ticket was filed under "Results — display question," which carries a P3 default. The category was reasonable from the reporter's vantage — a result was not displaying — but severity inherited from category rather than from scope. Nothing in the intake asked "how many patients?" A ticket describing three patients with missing microbiology results should not be able to enter the queue at P3.

**6.9 Diagnostic anchoring on the historically guilty component.** The middleware had caused six of the previous eight result-delivery incidents. Its failure mode — hung sessions with a healthy-looking engine — matches the observed symptoms almost exactly. Combined with a green dashboard and an empty error queue, the middleware hypothesis was the rational first hypothesis. What was missing was not better instinct but a **rule**: no single hypothesis may be pursued for more than 45 minutes without either confirming evidence or a mandatory review of the change log for the affected path. The change log would have surfaced the 179-day-old patch applied 62 hours earlier in under a minute.

**6.10 Downtime procedure eight years stale.** LAB-DT-004 was last revised in March 2019. In the interval, the organization consolidated a patient tower, renamed five units, and closed three. The procedure had no review cycle, no owner of record, and no dependency on the facility's unit master file. Thirty-five percent of its contact destinations were invalid at the moment of use. The procedure also assumed fax as primary modality with no secure-message or EHR-based fallback.

**6.11 Replay tooling without safety properties.** The replay utility had three defects that only manifest at clinical scale: it overwrote observation datetimes with the replay clock; it had no dry-run mode; and it had no duplicate suppression. It was built for small-batch recovery after brief outages, where all three shortcomings are harmless. Using it for a 1,460-message, 62-hour backlog exceeded its design envelope, and nothing in the tool or the runbook flagged that boundary.

**6.12 Decision fatigue at the replay decision point.** The replay was authorized at 19:48 by a team that had been working the incident for over six hours, immediately after the relief of finding and fixing the parser. The decision was made in a moment of momentum, on a bridge with no assigned devil's advocate and no requirement for a written change plan on emergency remediation actions.

**6.13 No closed-loop acknowledgment for microbiology.** Critical chemistry results carry a mandatory verbal-notification policy, which is why chemistry harm was far lower than message counts would predict — 340 critical chemistry results were held, and nearly all were telephoned. Microbiology final results have no equivalent closed loop; they are expected to reach the clinician through the chart. When the chart path failed, microbiology had no backup. All nine antibiotic-delay cases were microbiology.

**6.14 Ambulatory blind spot.** The 282 affected clinic patients had no equivalent of a nursing unit to notice the gap. Ambulatory result review runs on a 24–72 hour rhythm, which exceeded the entire defect window. Ambulatory was notified last, on Thursday morning, roughly 18 hours after inpatient units.

---

## 7. What worked and what did not

### 7.1 What worked

**Clinician persistence was the detection mechanism.** Dr. Kellerman checked the chart twice, asked a clerk to re-query, and then telephoned the laboratory directly rather than accepting that the result was pending. She then asked the technologist to check two additional patients — the question that turned one missing result into a pattern. The organization should be clear-eyed that this is a fortunate outcome, not a designed control.

**Queue persistence prevented data loss.** Confluence's hold behavior, which caused the incident, also meant that all 1,460 messages survived intact with their original content. Zero results were permanently lost. Recovery was a delivery problem, not a reconstruction problem.

**The pivot from dashboard to direct database query.** At 16:02, Thibodeaux stopped trusting the abstraction and queried the underlying state. Nine minutes later he had the root symptom and the correlation to the patch window. The skill was present; the tooling that should have made it unnecessary was not.

**Laboratory activated manual reporting in 16 minutes.** From confirmation of scope at 16:24 to manual reporting activation at 16:40. Brannigan did not wait for command structure or a full diagnosis. The prioritization scheme she imposed — inpatient, then ED, then discharged, then ambulatory — was correct and was not written in any procedure.

**Rapid abandonment of a failing procedure.** Fax attempts began at 16:55 and were abandoned at 17:30. Thirty-five minutes is a reasonable time to discover that a third of your contact list is invalid and to switch modalities without waiting for authorization.

**Vendor responsiveness.** Confluence support confirmed the defect 53 minutes after engagement and identified the exact release item. The configuration-flag workaround was available and correct.

**Replay halted in 11 minutes.** From the first nursing call at 20:26 to halt at 20:52 — 26 minutes, with the halt decision made 11 minutes after the third independent report. Nurses called instead of assuming the system was right, and the technical team stopped rather than pushing through.

**Assumption of command and the stop order.** Dr. Abdullahi's 21:15 directive to halt all automated remediation is the most important decision in the response. A second bulk operation — deletion of duplicates, or a corrected re-replay — attempted that night by a fatigued team would very likely have compounded the damage.

**Reconciliation cell design and execution.** Osei-Bonsu's cell was operating within 90 minutes of the decision, with a validated workflow, per-chart documentation, and 6-hour rotations. It processed 1,214 patients and 6,260 observations in 41 hours with no reported reconciliation errors.

**Pharmacy stewardship sweep as the harm-detection instrument.** Corcoran's team swept all 1,214 charts against antimicrobial regimens and produced the nine-patient harm list within 10 hours. This converted an ambiguous safety question into a specific, actionable list.

**Timely and complete regulatory filing and disclosure.** The reportable event was filed within the statutory window with a substantially accurate account. Disclosure conversations with nine patients and families were completed by 17 February.

### 7.2 What did not work

**Sixty-two hours of silent failure.** No automated signal, at any point, in any channel, reached any human being. The gap was closed by a phone call.

**A dashboard that was green throughout.** The single artifact most consulted by engineers and leadership was accurate and actively misleading. It was consulted at 13:35 on Wednesday and reinforced the wrong hypothesis.

**Two hours and fifty-one minutes on the wrong component.** Two restarts of a system that had not been changed, while the system that had been changed 62 hours earlier reported itself healthy. The change log was not consulted until after the middleware hypothesis was exhausted.

**A downtime procedure that failed on contact.** Eight years stale, fax-dependent, with 11 of 31 destinations invalid, including two that delivered successfully to a decommissioned number — the worst possible outcome, since it produced no delivery failure signal.

**A replay that made things worse.** Executed with no dry run, no dedup check, and no verification of timestamp behavior, at the end of a six-hour response, generating 4,800 duplicates with false collection times. At least one medication dose was held pending clarification. The duplicate cleanup consumed roughly two-thirds of the 41-hour reconciliation effort — the correction cost more than the original problem.

**Communication lagged the harm.** Nurses encountered conflicting values at 20:26; enterprise notification went out at 22:05. For 99 minutes, nursing staff were discovering the problem faster than the organization was telling them about it.

**Ambulatory was an afterthought.** 282 patients across 22 clinics were addressed on Thursday morning, after inpatient reconciliation was already underway.

**Near-miss signals were absorbed and lost.** Four contacts across two days, each closed as a satisfied individual request. The organization had the information on Monday morning and no mechanism to assemble it.

**Severity was set by dropdown.** A P3 category on a ticket describing three patients with missing microbiology results.

**Manual results created a second reconciliation problem.** Results phoned Wednesday evening were documented in nursing notes and on paper downtime forms, then scanned. When automated filing resumed, the scanned documentation and the filed result had to be reconciled per chart — a foreseeable consequence of manual reporting that no procedure anticipated.

**Sentinel event review chartered five days after the event.** The most serious case was identified Thursday morning and formally chartered the following Monday.

---

## 8. Action items

Priority: **P0** = must complete before next interface change; **P1** = 30 days; **P2** = 90 days; **P3** = fiscal year.

### 8.1 Detection and monitoring

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 1 | Implement queue-state SLO monitoring in Confluence: alert at any message in a non-terminal state >10 min; page at >50 messages or any message >30 min. Cover all states including `PENDING_TRANSFORM` and any future hold state. | Gerard Thibodeaux | 06 Mar 2027 | P0 |
| 2 | Route all interface alerts to the Integration Engineering on-call rotation in the paging platform. Prohibit distribution lists as alert destinations for clinical interfaces; enforce by configuration audit. | Gerard Thibodeaux | 06 Mar 2027 | P0 |
| 3 | Deploy synthetic end-to-end canary: inject 6 test messages per hour into the results path, including a >3-organism microbiology message and a critical-flagged chemistry message; page on non-arrival in the EHR within 5 minutes. | Gerard Thibodeaux | 20 Mar 2027 | P0 |
| 4 | Build a daily automated reconciliation control comparing results verified in the LIS against results filed in the EHR, by result type; report variance >0.1% to laboratory and informatics leadership each morning at 06:00. | Colleen Brannigan / Marisol Reyes-Cantu (Dir., Application Services) | 03 Apr 2027 | P1 |
| 5 | Redesign the interface health dashboard: replace the single status indicator with per-interface panels showing queue depth by state, oldest message age, filed-vs-received counts, and last successful clinical filing per result type. Remove the composite "GREEN" indicator. | Marisol Reyes-Cantu | 17 Apr 2027 | P1 |
| 6 | Institute quarterly alert-path verification: fire a test alert on every clinical interface alert channel and confirm human receipt. Report results to IT governance. | Marisol Reyes-Cantu | 30 Apr 2027, then quarterly | P1 |
| 7 | Add "application alert destinations and on-call routing" as a mandatory line item on the organizational change / reorganization checklist owned by HR-IT liaison. | Diane Kaczmarek (CIO) | 20 Mar 2027 | P1 |

### 8.2 Change management and testing

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 8 | Reclassify all changes to clinical result, order, and medication interfaces as **High Risk** regardless of authorship. Require clinical validation sign-off from Laboratory and Clinical Informatics before production application. Amend CAB rubric accordingly. | Nathaniel Ofori (Chair, CAB) | 13 Mar 2027 | P0 |
| 9 | Expand the interface regression suite from 40 to a minimum of 120 message types, prioritized by clinical criticality, with mandatory boundary fixtures: high-repetition microbiology (4, 6, 10 organisms), all abnormal-flag values, extended-length fields, and non-ASCII characters. | Gerard Thibodeaux | 30 Jun 2027 | P1 |
| 10 | Build a production-representative test corpus of 2,000 de-identified messages sampled across all 218 types; require post-change smoke tests to run against this corpus rather than synthetic fixtures. | Gerard Thibodeaux / Priya Ramanathan (Mgr., Clinical Informatics) | 15 May 2027 | P1 |
| 11 | Establish a mandatory structured release-note review for all interface vendor patches. For each item, document: what data it touches, what it changes about failure behavior, and what operational workflow it assumes. Store in the change record. | Nathaniel Ofori | 27 Mar 2027 | P1 |
| 12 | Define a mandatory 4-hour active soak window following any clinical interface change, with a named engineer monitoring live clinical message flow (not dashboard status) and a documented go/no-go at soak end. | Gerard Thibodeaux | 13 Mar 2027 | P0 |
| 13 | Prohibit clinical interface changes in windows where the following business-hours clinical review is more than 12 hours away. Move interface changes to Tuesday–Thursday evening windows. | Nathaniel Ofori | 13 Mar 2027 | P1 |
| 14 | Institute a change-age policy: any change deferred more than 90 days returns to full CAB review, including re-assessment of risk classification and re-execution of validation. | Nathaniel Ofori | 10 Apr 2027 | P2 |

### 8.3 Incident response and triage

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 15 | Revise service desk intake for all clinical-data tickets: mandatory fields for patient count, clinical service affected, and whether results/orders/medications are involved. Any ticket reporting ≥2 patients with missing clinical data auto-escalates to P1 with immediate informatics page. | Marisol Reyes-Cantu | 27 Mar 2027 | P0 |
| 16 | Publish a diagnostic protocol for clinical data-flow incidents: (a) consult the change log for all components in the path before forming a hypothesis; (b) 45-minute time-box per hypothesis, after which a second engineer must review; (c) query authoritative state directly, never rely on a summary dashboard for incident diagnosis. | Gerard Thibodeaux | 27 Mar 2027 | P0 |
| 17 | Define clinical-data incident command thresholds and pre-assign roles. Any incident affecting ≥25 patients' clinical data triggers automatic CMIO/CNIO notification and formal incident command within 30 minutes. | Dr. Yusuf Abdullahi | 03 Apr 2027 | P1 |
| 18 | Create a monthly aggregation report of all "result not visible / data not displaying" contacts across service desk, laboratory, and nursing channels, with a cluster threshold (≥3 in 24 hours on the same data type) that triggers informatics review. | Priya Ramanathan | 17 Apr 2027 | P1 |
| 19 | Establish a standing clinical communication protocol for data-integrity incidents: EHR banner, unit huddle script, ambulatory clinic notification, and provider secure message, all issuable within 30 minutes by the incident commander. Pre-write templates. | Tamika Osei-Bonsu | 03 Apr 2027 | P1 |
| 20 | Add mandatory ambulatory representation to clinical incident command; define the ambulatory notification path for all 22 clinics with a named contact per site. | Tamika Osei-Bonsu | 17 Apr 2027 | P1 |
| 21 | Conduct a tabletop exercise simulating a silent interface failure with duplicate replay, involving informatics, laboratory, nursing, pharmacy, and ambulatory leadership. | Dr. Yusuf Abdullahi / Wendell Fitzgerald (Dir., Emergency Preparedness) | 30 Jun 2027 | P2 |

### 8.4 Downtime procedures and continuity

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 22 | Rewrite LAB-DT-004 laboratory downtime reporting procedure. Remove fax as primary modality; establish secure message and telephone-tree primaries with defined prioritization (inpatient → ED → discharged → ambulatory). | Colleen Brannigan | 10 Apr 2027 | P0 |
| 23 | Bind all downtime procedure contact data to the facility unit master file with automated quarterly validation; no procedure may contain hard-coded contact information. | Wendell Fitzgerald | 29 May 2027 | P1 |
| 24 | Assign named owners and annual review dates to all 74 clinical downtime procedures; audit for currency and report exceptions to the Environment of Care committee. | Wendell Fitzgerald | 31 Jul 2027 | P2 |
| 25 | Define and document the manual-to-electronic reconciliation workflow that must follow any manual results reporting period, including how phoned results are recorded and later matched to filed results. | Colleen Brannigan / Tamika Osei-Bonsu | 15 May 2027 | P1 |

### 8.5 Data integrity and recovery tooling

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 26 | Rebuild the queue replay utility with mandatory properties: preservation of original message and observation timestamps; duplicate detection against already-filed results; dry-run mode producing a full impact report; batch size limits with per-batch verification. | Gerard Thibodeaux | 12 Jun 2027 | P0 |
| 27 | Require a written remediation plan, reviewed by a second engineer and approved by the incident commander, before any bulk data operation (replay, re-transmit, bulk correction) affecting more than 50 patients during an active incident. | Dr. Yusuf Abdullahi | 20 Mar 2027 | P0 |
| 28 | Assign a designated dissenting reviewer role in clinical incident command whose explicit function is to challenge remediation plans before execution. | Dr. Yusuf Abdullahi | 03 Apr 2027 | P1 |
| 29 | Implement duplicate-observation detection in the EHR results path: flag identical result values on the same patient and analyte within 24 hours for review rather than silent filing. | Marisol Reyes-Cantu | 31 Jul 2027 | P2 |

### 8.6 Clinical safety and closed-loop results

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 30 | Design and pilot a closed-loop acknowledgment requirement for final positive microbiology results, modeled on the existing critical chemistry verbal notification policy. Pilot on 6-North and the ED, then evaluate for enterprise rollout. | Dr. Elena Vasilenko / Dr. Anand Pillai (Medical Dir., Laboratory) | 31 Aug 2027 | P1 |
| 31 | Complete sentinel event review and root cause analysis for the referred case; report findings and corrective actions to the Patient Safety Committee and Board Quality Committee. | Dr. Elena Vasilenko | 15 Apr 2027 | P0 |
| 32 | Complete 30-day and 90-day outcome follow-up on all nine antibiotic-delay patients and both readmitted patients; document in the harm review file. | Dr. Elena Vasilenko / Sondra Whitfield (Dir., Risk Management) | 15 May 2027 | P1 |
| 33 | Implement a standing "unresulted specimen" report: any specimen accessioned in the LIS without a corresponding filed result in the EHR beyond expected turnaround time, reviewed daily by laboratory leadership. | Colleen Brannigan | 31 May 2027 | P1 |
| 34 | Deliver findings and mitigation status to the Board Quality Committee; include interface monitoring maturity as a standing quarterly metric. | Dr. Yusuf Abdullahi / Dr. Elena Vasilenko | 21 May 2027 | P1 |

### 8.7 Vendor management

| # | Action | Owner | Due | Pri |
|---|---|---|---|---|
| 35 | Open a formal quality escalation with the Confluence vendor regarding: (a) release notes that describe a failure-disposition change without a clinical-impact rating; (b) a default configuration that assumes an operator-monitored review queue without deployment-time verification. Request a customer advisory. | Diane Kaczmarek | 27 Mar 2027 | P1 |
| 36 | Amend the Confluence contract at next renewal to require clinical-impact classification on all release items and 30-day advance notice of any change to message validation or failure handling. | Diane Kaczmarek | 30 Sep 2027 | P3 |

---

## 9. Open questions

1. Did any of the 47 patients discharged before their result filed experience a delayed diagnosis not captured by the antimicrobial sweep? A broader chart review of that cohort is underway, due 15 April.
2. Are there other Confluence configuration defaults that assume operational roles the organization does not staff? A full configuration review against operational reality is scoped for Q2.
3. How many of the remaining 178 untested message types carry patterns that would fail under strict schema conformance? A static analysis of 90 days of production traffic against the 7.4.2 parser is due 30 April.
4. The interim monitoring built on 11 February took 90 minutes. Why had it not been built in the preceding several years? This question is directed at prioritization and staffing of interface operations following the December 2025 reorganization, and is referred to IT governance.

---

## 10. Closing note

The most uncomfortable finding of this review is that the technology behaved as designed at every step. The engine held non-conforming messages, as instructed. The dashboard reported no errors, because there were none. The alert system delivered 216 warnings to the address configured. The regression suite passed the tests it contained. The change process approved a change that met its criteria.

The failure was in the seams: between a vendor's assumption about who watches a queue and an organization that had no such role; between a monitoring philosophy built around errors and a defect that produced none; between a distribution list and the people who used to be on it; between a test suite that covered 40 types and a catalog of 218.

For 62 hours, 1,214 patients' clinical picture was incomplete, and no system anywhere in the organization was capable of noticing. It ended because a hospitalist did not accept that a blood culture was still pending on day three, and then asked the right follow-up question. Our obligation from this event is to build the controls that make that phone call unnecessary — and to remember, while we build them, that the phone call is what we had.

---

*Distribution: Executive Leadership, Board Quality Committee, IT Governance, Patient Safety Committee, Laboratory Leadership, Nursing Leadership, Medical Staff Executive Committee, Risk Management, Compliance.*

*Protected under Connecticut peer review and patient safety work product provisions.*
