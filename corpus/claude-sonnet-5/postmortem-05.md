# Housatonic Valley Health — Incident Postmortem

## Confluence Interface Engine Message Filing Failure — February 7–13, 2027

**Document Status:** Final
**Classification:** Internal — Quality & Patient Safety
**Prepared by:** Office of the Chief Medical Information Officer, in coordination with Laboratory Services, Integration Engineering, Nursing Informatics, and the Quality Review Committee
**Chair, Quality Review:** Dr. Elena Vasilenko
**Distribution:** Executive Leadership, Patient Safety Committee, Board Quality Subcommittee, Connecticut Department of Public Health (reportable event filing)
**Date of Report:** March 2027

---

## 1. Summary

Beginning at 10:15 p.m. on Sunday, February 7, 2027, a vendor-supplied patch applied to the Confluence interface engine altered how a message segment was parsed for two categories of laboratory results: microbiology results containing more than three organism entries, and chemistry results flagged as critical. Rather than failing visibly, affected messages queued silently. The interface engine's status dashboard, which tracked connection health and throughput but not message-type-level filing success, continued to display a normal (green) status throughout the event.

Over the following 62 hours, 1,120 microbiology results and 340 critical chemistry results failed to file into the electronic health record. No system alert, dashboard indicator, or automated check identified the accumulation. The failure was first identified by a clinician — Dr. Simone Kellerman, a hospitalist — who called the laboratory on Wednesday, February 10, at 12:30 p.m. after a blood culture ordered two days earlier had not appeared in the chart.

The response that followed was hampered by three compounding problems: an initial misdiagnosis that directed troubleshooting effort at the analyzer middleware rather than the interface engine, a downtime reporting procedure that had not been updated since 2019 and referenced fax lines for units that no longer existed, and a queue replay intended to restore the missing results that instead created 4,800 duplicate entries timestamped with replay time rather than original collection time, producing conflicting values in the chart during a period when clinicians were already trying to reconcile missing data.

Nine patients experienced antibiotic therapy changes delayed more than 24 hours as a direct result of missing or delayed culture and chemistry data. Two of these patients were readmitted within 30 days. One case has been referred to sentinel event review. Housatonic Valley Health filed a reportable event with the Connecticut Department of Public Health on February 13, 2027.

This postmortem was commissioned to establish what happened, in what order, and why the organization's detection and response systems did not perform as designed. It is not an evaluation of individual performance. The findings point to systemic gaps in alert distribution ownership, regression testing scope, downtime procedure maintenance, and the change-management review that allowed a patch to sit available for six months before being applied to a live production interface without a documented review of its effect on outbound message types.

---

## 2. Impact, Stated in Numbers

**Scale of the organization**
- 2 hospitals, 480 licensed beds
- 22 outpatient clinics
- 6,100 employees
- Approximately 19,000 interface messages processed daily through Confluence under normal operating conditions

**Duration and volume of the failure**
- Duration of undetected message-filing failure: 62 hours (10:15 p.m. Sunday, February 7 to 12:30 p.m. Wednesday, February 10)
- Microbiology results affected (more than three organism entries): 1,120
- Critical chemistry results affected (flagged critical values): 340
- Total results that failed to file during the primary failure window: 1,460
- Regression test coverage of the interface engine's message-type library at time of patch: 40 of 218 message types (18.3%)
- Time the patch had been available from the vendor prior to application: approximately 6 months (since August 2026)
- Time the Confluence alert distribution list had been unpopulated prior to the incident: 14 months (since a departmental reorganization)

**Response timeline metrics**
- Time from failure onset to detection: 62 hours, 15 minutes
- Time from detection to activation of manual/downtime reporting procedures: 4 hours, 10 minutes
- Time lost to middleware restart troubleshooting before the interface engine was identified as the fault domain: approximately 3 hours
- Time from command structure activation (Dr. Abdullahi) to full reconciliation completion: approximately 4 days (Wednesday 9:00 p.m. to Friday, end of day)

**Duplicate replay event**
- Queue replay executed: 8:15 p.m., Wednesday, February 10
- Duplicate results generated: 4,800
- Duplicates incorrectly timestamped with replay time rather than original collection time: 4,800 (100% of replayed messages)

**Clinical impact**
- Patients with antibiotic therapy changes delayed more than 24 hours: 9
- Patients among these readmitted within 30 days: 2
- Cases referred to sentinel event review: 1
- Reportable events filed with state health department: 1 (filed February 13, 2027)

**Reconciliation scope**
- Total lab results requiring manual reconciliation against the chart (missing results plus duplicates): 6,260 (1,460 originally missing + 4,800 duplicates)
- Clinical and informatics staff hours logged during reconciliation effort (Wednesday 9:00 p.m. through Friday close): estimated 340 person-hours across nursing informatics, laboratory, and medical staff reviewers

---

## 3. Timeline of Detection Through Resolution

All times Eastern Standard Time. Timeline reconstructed from Confluence system logs, laboratory information system audit trails, paging and call records, and interviews with responding staff.

**Sunday, February 7**

- **10:15 p.m.** — Vendor patch applied to Confluence interface engine during a scheduled maintenance window. The patch changed segment-parsing logic for messages containing certain repeating field structures, affecting microbiology results with more than three organism entries and chemistry results carrying a critical-flag indicator. Affected messages began queuing rather than filing or erroring.
- **10:15 p.m.–11:00 p.m.** — Post-patch verification performed by the on-call integration engineer confirmed that the interface engine was connected to all endpoints, throughput counters were incrementing, and the dashboard displayed normal (green) status across all monitored channels. Verification did not include message-type-specific filing confirmation, as no such check existed in the standard post-patch checklist.

**Monday, February 8**

- **Overnight through midday** — Microbiology and flagged critical chemistry results continued to queue silently. Non-critical chemistry, hematology, and standard microbiology results (three or fewer organisms) continued to file normally, meaning the majority of the day's ~19,000 messages processed without visible disruption.
- **Approximately 9:40 a.m.** — A blood culture is ordered for a patient under Dr. Kellerman's service (later identified as the index case that triggers detection). The order-to-result workflow proceeds normally on the analyzer side; the resulting message queues in Confluence rather than filing.
- Throughout the day — No alert is generated. The Confluence alerting system does have logic to flag queue backlogs exceeding a threshold, but the alert routes to a distribution list that was emptied 14 months earlier during a departmental reorganization and never repopulated or redirected. No bounce-back, delivery failure notice, or secondary alerting path existed to catch this.

**Tuesday, February 9**

- Queue of unfiled microbiology and critical chemistry results continues to grow. No clinical or technical staff member is yet aware of the failure. Isolated instances of clinicians noting "pending" or missing results are not yet recognized as a systemic pattern; a small number of individual follow-up calls to the lab are handled as routine result-tracing requests rather than escalated.

**Wednesday, February 10**

- **12:30 p.m.** — Dr. Simone Kellerman, hospitalist, calls the laboratory directly regarding a blood culture ordered Monday morning that still does not appear in the chart. This call is the first point at which the scale of the problem begins to surface, as laboratory staff checking the analyzer confirm the result was finalized on the instrument side days earlier.
- **12:30 p.m.–1:15 p.m.** — Laboratory staff query additional recent orders and identify multiple additional microbiology results present on the analyzer but absent from the chart. The issue is escalated to Integration Engineering.
- **1:15 p.m.** — Gerard Thibodeaux, Manager of Integration Engineering, is notified and begins investigation. Initial hypothesis, based on the pattern of results being confirmed at the analyzer but not reaching the chart, points toward the analyzer middleware layer as the point of failure, since the interface engine dashboard continues to show normal connectivity and throughput.
- **1:15 p.m.–4:00 p.m.** — Middleware is restarted twice as a corrective action based on the working hypothesis. Each restart requires reconnection and stabilization time. Neither restart resolves the filing gap, as the fault lies downstream in Confluence's parsing logic, not in the middleware. Approximately three hours elapse in this diagnostic path before attention shifts to the interface engine itself.
- **Approximately 4:00 p.m.** — Investigation redirects to Confluence. Review of interface engine logs identifies a growing queue of unfiled messages and correlates the onset with the Sunday night patch window.
- **4:00 p.m.–4:40 p.m.** — Colleen Brannigan, Director of Laboratory Services, is briefed on the scope of the problem and the likely inability to resolve the interface issue immediately given the need for vendor input.
- **4:40 p.m.** — Colleen Brannigan activates manual/downtime critical result reporting procedures across affected units to ensure that any new critical or significant results are communicated directly by phone pending interface resolution. The activated procedure is the standing 2019 downtime document. Staff attempting to use it discover that a number of the listed unit fax numbers correspond to units that have since been closed, merged, or renamed, requiring real-time improvisation of contact routing during an already active event.
- **4:40 p.m.–8:00 p.m.** — Parallel efforts proceed: laboratory staff begin manually cross-referencing analyzer records against the chart to identify the full scope of missing results; Integration Engineering engages the interface engine vendor to confirm the patch as the causal agent and to identify a safe method for releasing the queued messages.
- **8:15 p.m.** — Queued messages are released via a replay of the message queue into the health record, intended to file the 1,460 backlogged results. The replay succeeds in delivering the queued content but does so using replay execution time as the message timestamp rather than preserving original specimen collection or result-finalization time. Because a portion of affected orders had, in the intervening hours, already been partially addressed through manual reporting or repeat testing, the replay introduces a total of 4,800 duplicate entries into affected patient charts, several of which carry values that differ from manually reported or repeat-test values obtained earlier in the day, creating conflicting information in the chart at the point of highest clinical attention.
- **8:15 p.m.–9:00 p.m.** — Nursing and physician staff on affected units begin reporting confusion over conflicting or duplicated lab values appearing in patient charts, in some cases for patients whose care team had already acted on a manually communicated value.
- **9:00 p.m.** — Dr. Yusuf Abdullahi, Chief Medical Information Officer, assumes formal incident command, establishing a single point of coordination across Laboratory Services, Integration Engineering, Nursing Informatics, and Medical Staff leadership. This marks the formal transition from a laboratory- and engineering-led technical response to an organization-wide incident structure.

**Wednesday night through Friday, February 12**

- Tamika Osei-Bonsu, Chief Nursing Informatics Officer, leads a structured reconciliation process to review all 6,260 affected results (1,460 originally missing plus 4,800 duplicates), confirm correct values against source analyzer data, correct or annotate charts, and verify that clinical teams had accurate, current information for every affected patient.
- Reconciliation proceeds unit by unit and patient by patient, prioritizing patients with pending antibiotic decisions, active sepsis workups, and other time-sensitive clinical circumstances identified through chart review and direct outreach to unit charge nurses and attending physicians.
- **Friday, February 12** — Reconciliation effort concludes; Tamika Osei-Bonsu confirms all affected patient records have been reviewed and corrected, and communicates closure of the active reconciliation phase to incident command.

**Saturday, February 13**

- Housatonic Valley Health files a reportable event with the Connecticut Department of Public Health, consistent with regulatory requirements for events involving delayed diagnostic information with potential patient harm.

**Following weeks**

- Dr. Elena Vasilenko convenes and chairs a formal quality review of the incident, encompassing chart review of the nine patients with delayed antibiotic changes, the two readmissions, and the case referred to sentinel event review, alongside the technical and procedural review reflected in this postmortem.

---

## 4. Root Cause

The proximate technical cause of the incident was a vendor patch applied to the Confluence interface engine that altered segment-parsing behavior for two specific message patterns — microbiology results with more than three organism entries and chemistry results carrying a critical-value flag — causing those messages to enter a queued, non-erroring state rather than filing to the health record or generating a visible failure.

However, the patch itself is properly understood as a triggering event rather than the sole root cause. The incident was made possible, and was allowed to persist for 62 hours, by the coincidence of the following systemic conditions, any one of which, had it been absent, would likely have prevented the incident or sharply reduced its duration and impact:

1. **No message-type-level filing verification existed as part of routine or post-change monitoring.** The interface engine's dashboard reported connectivity, throughput, and queue depth in aggregate, but had no mechanism to confirm that messages of a specific type or pattern were successfully filing to their destination. A patch could silently break a subset of message types indefinitely without any dashboard indicator changing state.

2. **The alert distribution list for Confluence system alerts had been empty for 14 months.** A departmental reorganization removed the individuals previously on this list and no process existed to confirm distribution lists remained populated and correctly targeted after organizational changes. Even if the queue-backlog alert logic had fired (and it is not confirmed from available logs that it did, given the specific parsing failure mode), it would have reached no one.

3. **Regression testing coverage for the interface engine covered only 40 of 218 message types (18.3%).** The affected message patterns — high-organism-count microbiology and critical-flag chemistry — were not within the tested subset. This gap meant the patch could pass the organization's standard pre-deployment testing process without the affected behavior ever being exercised.

4. **The patch had been available since August 2026 and was applied in February 2027 without a documented review of its effect on outbound message parsing for all message types in current use.** A six-month gap between availability and application suggests the patch was not treated as urgent, yet when it was applied, it appears to have been treated as routine, without a compensating increase in post-deployment scrutiny proportional to its age or scope of change.

Taken together, the root cause is best described as: **an unverified change to a critical clinical data pathway was deployed into an environment whose monitoring, alerting, and testing infrastructure had degraded over time in ways that were individually known or knowable but not connected to one another as a compound risk.** No single control failure caused the 62-hour detection gap; the absence of any single functioning layer of defense — verification, alerting, or test coverage — would have surfaced the problem far sooner.

---

## 5. Contributing Factors

The following factors did not independently cause the incident but shaped its duration, its detection pathway, and the severity of its downstream effects.

**5.1 Absence of message-type-specific health checks**
The interface engine's monitoring architecture was built around connection- and volume-level indicators appropriate to detecting outages or connectivity failures, but not designed to detect partial, silent failures affecting a subset of message content. This is a design gap rather than a maintenance lapse, and it means the current monitoring architecture would not catch a structurally similar failure today without a specific fix.

**5.2 Distribution list decay following organizational change**
The emptied alert distribution list is illustrative of a broader pattern: technical configurations that reference organizational structures (individuals, teams, roles) are vulnerable to silent decay when the organization changes but the technical configuration is not included in reorganization checklists. There is no evidence any process exists to audit distribution lists, escalation trees, or paging configurations against current organizational structure on a recurring basis.

**5.3 Incomplete regression suite scope**
The 40-of-218 message type coverage reflects, by report, a historical pattern of adding tests reactively after specific issues rather than building toward comprehensive coverage of the message library. The two message categories affected in this incident — high-cardinality microbiology results and critical-flagged chemistry — are both clinically high-stakes categories, which sharpens the significance of their absence from the tested set.

**5.4 Patch aging without corresponding risk review**
No evidence was found of a documented decision process explaining why the patch sat available for six months or why, once applied, it did not receive elevated scrutiny appropriate to a change that had not been kept current with other vendor updates. Long-dormant patches may interact with system configurations that have since changed, increasing rather than decreasing risk relative to prompt application.

**5.5 Diagnostic anchoring toward the middleware**
The initial three hours of troubleshooting focused on the analyzer middleware. This was a reasonable initial hypothesis given that the interface engine dashboard showed normal status and the pattern of "confirmed at analyzer, absent from chart" is classically associated with middleware transmission failure. The absence of message-type-level filing confirmation (see 5.1) meant that ruling out Confluence as the fault domain took longer than it would have if such visibility existed, contributing directly to the time lost to middleware restarts.

**5.6 Downtime procedure currency**
The manual reporting procedure activated at 4:40 p.m. Wednesday was last updated in 2019. Hospital unit configurations — closures, mergers, renamings — had changed in the interim without a corresponding update to the downtime document. This gap surfaced at the worst possible time: during active use under time pressure, rather than during a scheduled drill where it could have been caught and corrected without clinical consequence.

**5.7 Replay mechanism design and timestamp handling**
The queue replay used to release the 1,460 backlogged messages was executed as an available technical remedy but was not designed, or was not used in a manner, that preserved original message timestamps. The consequence — 4,800 duplicates carrying replay time rather than collection time — compounded the incident rather than resolving it, and occurred at a point when parallel manual reporting had already begun to independently communicate some of the same results, creating a foreseeable (in hindsight) collision between two simultaneous remediation paths.

**5.8 Absence of a pre-established "silent failure" playbook**
The organization had established incident command structures and downtime procedures oriented around visible outages — a system going down, a connection failing. The organization did not have an established playbook for the scenario that in fact occurred: a system that remains visibly "up" while silently failing to complete its function for a subset of transactions. This gap shaped both the detection delay and aspects of the response, including the sequencing of middleware troubleshooting before interface engine investigation.

---

## 6. What Worked

Several aspects of the response performed as intended or better, and merit preservation and reinforcement in any remediation plan.

- **Clinical vigilance closed the detection gap that automated systems did not.** Dr. Kellerman's direct call to the laboratory, prompted by clinical judgment that an expected result was overdue, was the actual mechanism of detection. This reflects a functioning norm of clinical follow-up on pending critical results, even though it should not have been the last line of defense.

- **Escalation from the laboratory to Integration Engineering, once triggered, was prompt.** The interval between the 12:30 p.m. call and Gerard Thibodeaux's engagement at 1:15 p.m. was short, reflecting effective interpersonal escalation pathways within the organization even where automated pathways failed.

- **Manual downtime reporting was activated within the same operational day of detection.** Despite the procedural document being outdated, Colleen Brannigan's decision to activate manual critical-result reporting at 4:40 p.m. — roughly four hours after detection — provided a stopgap communication channel for new critical results while the interface issue remained unresolved, reducing the risk of further undetected results during the active remediation window.

- **Escalation to unified incident command occurred once the scope became clear.** Dr. Abdullahi's assumption of command at 9:00 p.m. Wednesday established a single point of coordination at the point when the duplicate-replay complication made clear that the incident required organization-wide management rather than departmental handling. Once this structure was in place, the response gained clear direction.

- **Reconciliation was thorough and patient-centered.** Tamika Osei-Bonsu's reconciliation process addressed the full scope of both missing and duplicate results (6,260 total) rather than a partial or sampled review, and appears to have prioritized clinically time-sensitive cases appropriately based on available records.

- **The organization self-identified and self-reported.** The reportable event filing on February 13 reflects a functioning compliance and transparency culture; the event was not discovered externally, and the organization moved to formal disclosure within days of resolution.

- **A formal, structured quality review was convened promptly**, chaired by Dr. Vasilenko, reflecting institutional commitment to systemic learning rather than closing the matter at the point of clinical stabilization.

---

## 7. What Did Not Work

- **No system-level mechanism detected the failure for 62 hours.** Detection depended entirely on an individual clinician noticing a specific missing result and choosing to call rather than assume a delay. This is not a resilient detection model for a pathway carrying 19,000 messages a day.

- **The alert distribution list failure meant that even where automated alerting logic may have existed, it had no path to a human being.** This represents a silent, long-standing (14-month) failure of a safety control that was not discovered by any audit, drill, or review in the intervening period.

- **Initial troubleshooting effort was misdirected toward the middleware, consuming approximately three hours** before attention correctly shifted to the interface engine — time during which the queue of unfiled results continued to grow and manual reporting had not yet begun.

- **The downtime procedure activated in the response was six years out of date** and contained fax numbers for units that no longer existed, requiring real-time improvisation during an active incident rather than reliable execution of a pre-validated plan.

- **The queue replay used to remediate the original failure introduced a new, larger-scale problem** — 4,800 duplicate results with incorrect timestamps — that arguably created more acute clinical confusion in its immediate aftermath than the original silent failure, because it produced actively conflicting information rather than simply absent information.

- **The regression suite's 18% coverage of message types meant the specific failure mode was structurally untestable within the existing quality assurance process** as it stood at the time of the patch, regardless of how carefully that process was executed.

- **The six-month gap between patch availability and application was not accompanied by any documented risk reassessment**, representing a missed opportunity to apply extra scrutiny to a change that had, by virtue of its age, already deviated from a "prompt patching" risk model.

---

## 8. Action Items

Action items are organized by the systemic gap they address. Each includes a named owner and due date. Owners are accountable for either completing the item or formally reassigning it with documented rationale; due dates reflect target completion, not mere initiation.

| # | Action Item | Addresses | Owner | Due Date |
|---|---|---|---|---|
| 1 | Design and implement message-type-level filing verification within the Confluence monitoring dashboard, including automated reconciliation counts between messages received by the interface engine and messages successfully filed to the health record, broken out by message type category. | Absence of silent-failure detection (Root Cause; 5.1) | Gerard Thibodeaux, Manager of Integration Engineering | May 15, 2027 |
| 2 | Audit all Confluence and related interface alert distribution lists, escalation trees, and paging configurations against current organizational structure; establish a recurring (semiannual) audit process tied to HR/org-change notifications going forward. | Alert distribution list decay (Root Cause; 5.2) | Gerard Thibodeaux, in coordination with IT Security and HR Business Partner for Clinical Operations | April 1, 2027 (initial audit); recurring semiannually thereafter |
| 3 | Expand the interface engine regression test suite to cover a documented, risk-prioritized path toward full 218-message-type coverage, with high-cardinality microbiology results and critical-flagged chemistry results addressed in the first phase. | Regression suite coverage gap (Root Cause; 5.3) | Gerard Thibodeaux, with vendor technical partner | Phase 1 (critical/high-risk message types, target 100 of 218): July 1, 2027. Full coverage roadmap with milestones: June 1, 2027 |
| 4 | Establish a formal change-management policy requiring documented risk review, including regression test coverage confirmation and rollback plan, prior to application of any vendor patch to production interface systems — with mandatory elevated review for patches held longer than 90 days from vendor release. | Patch aging without risk review (Root Cause; 5.4) | Dr. Yusuf Abdullahi, CMIO, with Integration Engineering and IT Governance Committee | April 15, 2027 |
| 5 | Fully revise the laboratory and clinical downtime/manual reporting procedure, validating all contact points (phone, fax, unit designations) against current facility structure; establish a schedule of biannual live drills of the downtime procedure independent of any active incident. | Outdated downtime procedure (5.6) | Colleen Brannigan, Director of Laboratory Services | First revised procedure: March 15, 2027. First live drill: June 2027 |
| 6 | Develop a documented interface message replay protocol that preserves original message timestamps (collection/result time) rather than replay execution time, and that includes a pre-replay reconciliation check against any results already manually reported during the outage window, to prevent duplicate or conflicting entries. | Replay/duplicate timestamp failure (5.7) | Gerard Thibodeaux, with Tamika Osei-Bonsu for clinical workflow input | May 1, 2027 |
| 7 | Develop and formally adopt a "silent failure" incident response playbook distinct from existing outage-response procedures, addressing scenarios where systems remain nominally operational while failing to complete a subset of transactions, including defined criteria for when to suspect a partial/silent failure versus a source-system (e.g., middleware) failure. | Absence of silent-failure playbook (5.8); diagnostic anchoring (5.5) | Dr. Yusuf Abdullahi, CMIO | June 1, 2027 |
| 8 | Complete the harm review and case-level analysis for all nine patients with delayed antibiotic changes, both readmissions, and the sentinel event referral; finalize findings and any individual case-level clinical practice recommendations through the standing sentinel event and quality review process. | Harm review completion | Dr. Elena Vasilenko, Quality Review Chair | April 30, 2027 |
| 9 | Present final quality review findings, including this postmortem and associated action item status, to the Board Quality Subcommittee. | Organizational accountability and closure | Dr. Elena Vasilenko, Quality Review Chair | June 15, 2027 |
| 10 | Establish a standing quarterly reconciliation audit — a scheduled, non-incident-triggered comparison of a sample of analyzer-confirmed results against health record filing status across all message types — as an ongoing detective control independent of item #1's real-time monitoring build. | Layered detection redundancy | Colleen Brannigan and Gerard Thibodeaux, jointly | First audit: August 1, 2027; recurring quarterly thereafter |
| 11 | Review and, where necessary, renegotiate vendor patch notification and support terms to require vendor notification of any known parsing or message-handling changes in patch release notes, and to establish a defined SLA for vendor engagement during in-progress interface incidents. | Vendor coordination and future prevention | Dr. Yusuf Abdullahi, CMIO, with Vendor Management/Contracts | May 1, 2027 |

---

## 9. Closing Note

This event did not result from a single failure but from the simultaneous, largely independent degradation of several protective layers — monitoring granularity, alert routing, test coverage, and procedural currency — that had each drifted from their intended state over months or years without detection, until they were all needed at once. The 62-hour detection gap, the misdirected middleware troubleshooting, the outdated downtime procedure, and the duplicate-replay complication each represent points where a functioning system would have caught or contained the problem sooner. The action items above are intended to rebuild redundancy across detection, alerting, testing, and procedure currency so that no single silent gap can again persist undetected for this long. The Quality Review Committee will track completion of all items through the June 2027 Board Quality Subcommittee presentation and will report any missed milestones with revised timelines at that time.

## Appendix A: Methodology and Sources

This postmortem was compiled through review of the following source materials and interviews, conducted between February 14 and March 5, 2027:

- Confluence interface engine system logs, February 7–13, 2027, including queue depth records, message type classification logs, and vendor patch deployment records
- Laboratory information system audit trail exports correlating analyzer-confirmed results against health record filing timestamps
- Paging, phone, and on-call escalation records for Integration Engineering and Laboratory Services staff, February 8–10
- The 2019 downtime and manual reporting procedure document, as activated February 10
- Interviews with Gerard Thibodeaux (Manager, Integration Engineering), Colleen Brannigan (Director, Laboratory Services), Dr. Yusuf Abdullahi (CMIO), Tamika Osei-Bonsu (Chief Nursing Informatics Officer), and Dr. Simone Kellerman (Hospitalist, index detection)
- Vendor change documentation and release notes for the February 7 patch, cross-referenced against the internal change-management ticket
- Regression test suite documentation maintained by Integration Engineering, reviewed to confirm the 40-of-218 message type coverage figure
- Reconciliation worksheets produced by the Nursing Informatics team during the February 10–12 reconciliation effort
- Reportable event filing submitted to the Connecticut Department of Public Health, February 13, 2027
- Sentinel event referral documentation for the case under separate review

Where system logs and interview accounts differed on specific timestamps, system log timestamps were treated as authoritative; interview accounts were used to establish sequence, reasoning, and decision context that logs do not capture.

This review did not have access to the vendor's internal patch development or testing records and therefore cannot independently confirm why the parsing change was introduced or whether the vendor's own testing identified the affected message patterns prior to release. Action item 11 addresses this gap prospectively.

---

## Appendix B: Glossary

**Confluence** — The interface engine used by Housatonic Valley Health to route, transform, and file clinical messages (primarily laboratory results) from source systems, including analyzer middleware, into the electronic health record.

**Analyzer middleware** — The intermediate software layer that receives raw results from laboratory analyzers, applies instrument-level formatting, and forwards results to the interface engine.

**Message segment parsing** — The process by which the interface engine interprets structured fields within an incoming clinical message (in this case, HL7-format laboratory result messages) to determine how content should be mapped into the health record.

**Queued (non-erroring) failure** — A failure mode in which a message is accepted by the interface engine but not successfully processed to completion, and is held in an internal queue rather than being either filed or flagged as failed. This mode is distinguished from a hard error, which typically generates a visible alert or log entry actionable by monitoring staff.

**Critical-flagged result** — A laboratory result, typically a chemistry value, that falls outside a predefined critical range and is flagged by the analyzer or laboratory information system for expedited clinical notification.

**High-organism-count microbiology result** — A microbiology culture result identifying more than three distinct organisms, typically associated with polymicrobial infections or contaminated specimens, and requiring more complex message structure to convey than single- or low-organism results.

**Queue replay** — A remediation technique in which messages held in an interface engine's internal queue are reprocessed and resubmitted for filing, used here to attempt to release the 1,460 backlogged results on the evening of February 10.

**Downtime/manual reporting procedure** — The documented fallback process by which critical laboratory results are communicated directly to clinical units by phone or fax when electronic interface pathways are known to be unavailable or unreliable.

**Reconciliation** — The structured process, in this case led by Nursing Informatics, of comparing source-system (analyzer) data against health record content to identify, correct, and confirm accuracy of all affected patient results following an interface failure.

**Regression test suite** — The set of automated or manual tests run against the interface engine, typically prior to deployment of a change, intended to confirm that existing message-handling behavior continues to function as expected across the range of message types the system processes.

---

## Appendix C: Regression Coverage Detail

At the time of the February 7 patch deployment, the Confluence regression test suite comprised 40 automated test cases, each corresponding to a distinct message type. The 218 total message types reflect the full range of clinical message categories currently transmitted through the interface engine across both hospitals and 22 clinics, spanning laboratory (chemistry, hematology, microbiology, blood bank, pathology), radiology, pharmacy, dietary, registration/ADT, and ancillary order-and-result categories.

Of the 40 covered message types, 31 corresponded to laboratory result categories. Neither of the two categories affected by the February 7 patch — microbiology results with greater than three organism entries, and chemistry results with a critical-value flag — was among the 31 laboratory message types under test. Both represent structurally more complex variants of message types that were covered (standard microbiology results with three or fewer organisms, and non-critical chemistry results, respectively), meaning the suite tested the base case of each message family without testing the higher-complexity variant most likely to expose parsing edge cases.

Integration Engineering has indicated that historical test case development followed a pattern of adding coverage reactively, typically after a specific defect was identified in production, rather than following a structured coverage plan built from the full message type inventory. No prior incident is on record that would have prompted specific coverage of these two message variants prior to this event.

Action item 3 (Section 8) establishes a phased plan to close this gap, prioritizing message types associated with time-critical clinical decision-making.

---

## Appendix D: Harm Review Summary (De-identified)

The following summary reflects the status of the clinical harm review as of this report's publication. Full case-level detail resides with the Quality Review Committee under standard peer-review protections and is not reproduced here.

- **Nine patients** experienced a delay of more than 24 hours in an antibiotic therapy change that would otherwise have been prompted by a microbiology or critical chemistry result affected by this incident. Of these:
  - Delays ranged from approximately 26 hours to approximately 68 hours from the point at which the result would, under normal interface function, have been available to the clinical team.
  - Clinical settings included both inpatient medical units and, in a smaller number of cases, step-down or intermediate care settings.
- **Two patients** among the nine were readmitted within 30 days of the index admission. Both readmissions are under review to determine the degree to which the delayed antibiotic change contributed to the readmission, alongside other clinical factors present in each case. Neither determination is finalized as of this report.
- **One case** has been referred to the organization's sentinel event review process based on the severity of clinical deterioration observed in combination with the delayed result. This review follows the standing sentinel event protocol and will produce findings and recommendations independent of, but coordinated with, this postmortem.
- No deaths have been attributed to this incident as of the date of this report.

The harm review remains open pending completion of the two readmission causality assessments and the sentinel event review. Final harm review findings will be incorporated into the June 15, 2027 presentation to the Board Quality Subcommittee (Action Item 9).

---

## Appendix E: Communication and Disclosure Record

- **February 13, 2027** — Reportable event filed with the Connecticut Department of Public Health, consistent with state reporting requirements for events involving diagnostic delay with potential patient harm.
- **February 14–20, 2027** — Affected patients and, where applicable, their designated decision-makers were notified in accordance with the organization's standing disclosure policy for events involving delayed or duplicated clinical information, with notification led by each patient's attending physician in coordination with the Office of Patient Safety.
- **Ongoing** — The organization has committed to providing the Connecticut Department of Public Health with a copy of this postmortem and confirmation of action item completion status at the 90-day mark following the reportable event filing (approximately May 14, 2027), consistent with standard follow-up expectations for reportable events of this nature.

This concludes the postmortem record for the February 7–13, 2027 Confluence message filing incident. Updates to action item status will be tracked in the Quality Review Committee's standing action item log and reported at each scheduled interval referenced in Section 8.
