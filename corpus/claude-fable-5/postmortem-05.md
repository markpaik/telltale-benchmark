# Incident Postmortem: Laboratory Results Interface Silent Filing Failure

**Housatonic Valley Health — Information Services & Laboratory Services**

| Field | Detail |
|---|---|
| Incident ID | HVH-2027-0041 |
| Severity | SEV-1 (Patient Safety Impact) |
| Incident Window | Sunday, February 7, 2027, 10:15 p.m. — Friday, February 12, 2027, 6:00 p.m. |
| Silent Failure Duration | 62 hours (patch application to detection) |
| Detection | Wednesday, February 10, 2027, 12:30 p.m. |
| Document Status | Final — Approved by Quality Review Committee |
| Review Chair | Dr. Elena Vasilenko, VP Quality & Patient Safety |
| Document Owner | Dr. Yusuf Abdullahi, Chief Medical Information Officer |
| Distribution | Executive Leadership, Medical Executive Committee, Board Quality Committee, Laboratory Services, Information Services, Nursing Informatics |

This postmortem examines systems, processes, and decisions. It does not assign fault to individuals. Every person named here acted in good faith on the information available to them at the time. The failures described below are failures of design, monitoring, documentation, and organizational process — the conditions in which reasonable people made reasonable decisions that produced a bad outcome.

---

## 1. Summary

On Sunday, February 7, 2027, at 10:15 p.m., a vendor-supplied patch was applied to Confluence, the interface engine that moves laboratory results from analyzer middleware into the electronic health record across Housatonic Valley Health's two hospitals and 22 clinics. The patch changed how one HL7 message segment was parsed. Two message profiles were affected: microbiology results containing more than three organism entries, and chemistry results carrying a critical-value flag.

Messages matching those profiles did not error out. They queued. Because Confluence's dashboard treats a queued message as a healthy message in transit, every monitoring surface stayed green. Alerts that might have fired routed to an email distribution list that had been emptied during a departmental reorganization 14 months earlier. For 62 hours, 1,120 microbiology results and 340 flagged critical chemistry results — including blood cultures, susceptibility panels, critical potassium and troponin values — accumulated in a queue no one was watching, while the ordering clinicians saw only pending status in the chart.

Detection came not from any monitoring system but from a clinician. At 12:30 p.m. on Wednesday, February 10, hospitalist Dr. Simone Kellerman called the laboratory asking why a blood culture ordered Monday had no result. The laboratory confirmed the result had been finalized and transmitted; the chart showed nothing.

The initial technical response focused on the wrong component. Analyzer middleware was suspected and restarted twice, consuming roughly three hours before attention shifted to Confluence itself. Manual result reporting was activated at 4:40 p.m., but the laboratory downtime procedure, last revised in 2019, listed fax numbers for nursing units that no longer exist following two rounds of unit consolidation. When the queued messages were replayed at 8:15 p.m., approximately 4,800 messages — the backlog plus retransmissions — filed into charts stamped with replay time rather than collection time, producing duplicate and apparently conflicting values that nursing staff had to interpret at the bedside overnight.

Dr. Yusuf Abdullahi, Chief Medical Information Officer, assumed incident command at 9:00 p.m. Wednesday. A clinical reconciliation effort led by Tamika Osei-Bonsu, Chief Nursing Informatics Officer, ran through Friday evening, manually verifying every affected result against the laboratory information system and confirming clinician awareness for every actionable value.

The harm review, chaired by Dr. Elena Vasilenko, identified nine patients whose antibiotic therapy changes were delayed more than 24 hours. Two of those patients were readmitted within 30 days. One case was referred to sentinel event review. Housatonic Valley Health filed a reportable event with the Connecticut Department of Public Health on February 13.

Three systemic conditions made this incident possible and made it long: a monitoring model that equated "no errors" with "healthy," so a silent queue looked identical to a working interface; an alerting path that had been broken for 14 months without anyone noticing, because it had never fired in a way anyone missed; and a testing regime that validates 40 of the 218 message types Confluence handles, which allowed a parsing change to reach production without touching the affected profiles. The patch itself had been available from the vendor since August 2026 and was applied six months later without a test-environment soak against representative message traffic.

---

## 2. Impact

### 2.1 Patient Impact

| Metric | Value |
|---|---|
| Patients with one or more affected results | 1,214 |
| Microbiology results not filed to chart | 1,120 |
| Critical chemistry results not filed to chart | 340 |
| Total results delayed | 1,460 |
| Patients with antibiotic therapy changes delayed > 24 hours | 9 |
| 30-day readmissions among affected patients (attributed) | 2 |
| Cases referred to sentinel event review | 1 |
| Reportable events filed with CT DPH | 1 (filed February 13, 2027) |
| Patients requiring disclosure conversations | 11 |

### 2.2 Operational Impact

| Metric | Value |
|---|---|
| Silent failure duration | 62 hours |
| Time from detection to correct component identification | ~3 hours |
| Time from detection to full chart reconciliation complete | ~53 hours |
| Duplicate/mistimed messages filed during replay | ~4,800 |
| Charts requiring manual reconciliation | 1,214 |
| Staff hours consumed by reconciliation (nursing informatics, lab, HIM) | ~610 hours |
| Manual phoned critical results during downtime period | 214 |
| Units with unreachable fax numbers in downtime procedure | 9 of 31 listed |
| Normal daily interface volume | ~19,000 messages |
| Peak queue depth at replay | 1,460 unfiled + retransmissions |

### 2.3 Scope

Both hospitals (480 beds combined) and all 22 ambulatory clinics were affected, because all laboratory result traffic flows through the single Confluence production instance. Inpatient units bore the majority of clinical impact due to the concentration of blood cultures and critical values in acute care. Emergency departments were partially insulated because point-of-care testing results travel a separate interface, which limited — but did not eliminate — ED exposure.

---

## 3. Timeline

All times Eastern. Sources: Confluence server logs, laboratory information system audit trail, help desk tickets, incident command log maintained by Dr. Abdullahi, and interviews conducted by the quality review team.

### Sunday, February 7

- **10:02 p.m.** — Integration Engineering begins scheduled maintenance window. Vendor patch 14.3.2 for Confluence, released by the vendor in August 2026, is staged for production. No test-environment replay of production message samples was performed against the patch; the change record notes "vendor-certified, low risk."
- **10:15 p.m.** — Patch applied to production Confluence. Engine restarts cleanly. Post-change verification consists of confirming the engine is running and that test ADT and basic chemistry messages file successfully. Both pass. Change closed as successful at 10:40 p.m.
- **11:20 p.m.** — First microbiology result with four organism entries hits the modified parser. The message fails segment parsing, is routed to a hold queue rather than an error queue, and generates a low-severity notification to the "IntEng-Alerts" distribution list — which has had zero members since a December 2025 reorganization. Dashboard remains green.

### Monday, February 8

- **Throughout the day** — Approximately 420 microbiology and 118 critical chemistry results queue silently. Laboratory staff see results finalize and transmit normally on their side; the LIS shows successful handoff to the interface. Clinicians see orders in "pending" or "in lab" status. Pending status for cultures at 24 hours is unremarkable, so no calls are generated.
- **2:40 p.m.** — A floor nurse at the Danbury campus calls the lab about a potassium result phoned earlier by a technologist (critical values are phoned per policy regardless of interface status). The phoned value is documented; the absence of the electronic result is attributed to "the interface being slow." No ticket filed. This is the earliest known signal, identified retrospectively.

### Tuesday, February 9

- **Throughout the day** — Queue grows by approximately 470 additional results. Three help desk tickets are filed referencing missing lab results; each is triaged as an individual chart issue and routed to the EHR application team, which finds the results absent from the EHR and refers the tickets to the lab, where they wait in a shared queue. No one correlates the three tickets.
- **4:15 p.m.** — A laboratory technologist notices that susceptibility results she finalized Monday still show as untransmitted downstream in a secondary verification screen. She mentions it to a shift lead; it is logged for follow-up "when the interface team is in."

### Wednesday, February 10 — Detection and Response

- **12:30 p.m.** — **Detection.** Dr. Simone Kellerman, hospitalist, calls Laboratory Services about a blood culture ordered Monday morning on a patient with a worsening clinical picture. The lab confirms the culture flagged positive Monday evening, with organism identification finalized Tuesday. The chart shows the order still pending. Colleen Brannigan, Director of Laboratory Services, is notified and asks the LIS team to trace the message; the LIS shows successful transmission to Confluence.
- **1:05 p.m.** — Brannigan calls Gerard Thibodeaux, Manager of Integration Engineering. Initial checks show Confluence dashboard fully green, all interfaces "up," no errors. Based on prior incidents in which the analyzer middleware dropped messages while the engine looked healthy, Thibodeaux forms the working hypothesis that the middleware is the failure point.
- **1:30 p.m.** — First middleware restart. Message flow resumes for new results (it was never interrupted); this is misread as partial confirmation of the hypothesis. Missing results do not appear.
- **2:45 p.m.** — Second middleware restart, with vendor middleware support on the phone. Middleware vendor confirms clean transmission logs and timestamps showing every missing message delivered to Confluence.
- **3:35 p.m.** — Attention shifts to Confluence. An engineer queries the hold queue directly — a queue not surfaced on the dashboard — and finds approximately 1,400 messages, the oldest timestamped 11:20 p.m. Sunday. Pattern is immediately apparent: multi-organism micro results and flagged critical chemistry.
- **3:50 p.m.** — Correlation with Sunday's patch established. Confluence vendor engaged; vendor confirms patch 14.3.2 changed OBX/OBR segment parsing behavior for repeating fields and that a known-issue advisory had been posted to the vendor customer portal in October 2026. HVH had not seen the advisory.
- **4:10 p.m.** — Brannigan and Thibodeaux jointly declare a laboratory reporting incident. Decision made to activate manual downtime reporting for all new critical and microbiology results while a replay plan is built.
- **4:40 p.m.** — **Manual reporting activated.** Laboratory staff begin working from the 2019 downtime procedure. Within the first hour, staff discover that 9 of 31 listed fax numbers belong to units closed or consolidated since 2019, and two phone tree extensions are dead. Lab staff improvise: charge nurse cell numbers, unit secretary lines, and hand-carried printouts at the main campus. Critical values continue to be phoned with read-back per standing policy; microbiology narrative results are the primary gap.
- **5:30 p.m.** — Nursing supervisors at both campuses briefed. House-wide notice sent to clinicians: lab results from Sunday night forward may be missing from charts; call the lab for anything clinically pressing.
- **6:45 p.m.** — Replay plan drafted by Integration Engineering with Confluence vendor: revert the parsing change via vendor hotfix, then replay the hold queue. The plan is reviewed for technical completeness. **It is not reviewed by clinical informatics**, and no one asks how replayed messages will be timestamped in the EHR.
- **7:50 p.m.** — Vendor hotfix applied; test messages with four organisms and critical flags file correctly.
- **8:15 p.m.** — **Queue replay begins.** Over roughly 40 minutes, the hold queue drains. Because the LIS had also retransmitted a subset of results during troubleshooting, approximately 4,800 messages file. Replayed messages carry a filing timestamp of Wednesday evening rather than the original collection/result time in the fields the EHR results-review display sorts on. Nurses and physicians reviewing charts see Wednesday-evening potassiums, troponins, and cultures that appear newer than — and sometimes conflict with — values already acted on or phoned earlier in the week.
- **8:40 p.m.** — First calls from nursing units reporting confusing duplicate results. A patient appears to have a critical potassium "resulted 20 minutes ago" that is actually Monday's specimen. Unit charge nurses begin escalating.
- **9:00 p.m.** — **Dr. Yusuf Abdullahi, CMIO, assumes incident command.** Incident command structure established: Abdullahi (command), Brannigan (laboratory), Thibodeaux (technical), Tamika Osei-Bonsu, CNIO (clinical reconciliation), house supervisors (unit communication). Replay is complete and cannot be cleanly retracted; decision made to manage forward with an aggressive communication and reconciliation strategy rather than attempt bulk deletion, which carried its own error risk.
- **9:20 p.m.** — Urgent broadcast to all clinical staff via secure messaging and overhead protocol at both hospitals: any lab result filed after 8:15 p.m. Wednesday may be a delayed result from February 7–10; verify specimen collection time inside the result detail before acting; call the lab with any doubt.
- **10:00 p.m.** — Osei-Bonsu convenes reconciliation team: nursing informatics, laboratory, HIM, and hospitalist representatives. Methodology defined: generate the full list of 1,460 affected results from Confluence logs, match each to the LIS record, verify correct values in chart, flag every actionable result (critical values, positive cultures, new susceptibilities) for direct clinician confirmation.
- **11:30 p.m.** — Overnight priority pass begins on the 340 critical chemistry results and all positive blood cultures, working from most clinically urgent downward.

### Thursday, February 11

- **2:00 a.m.** — Priority pass identifies the first cases in which positive cultures with susceptibility data had sat unfiled while patients remained on empiric antibiotics. Attending physicians for these patients are called overnight where clinically warranted; others queued for morning rounds contact.
- **7:30 a.m.** — Incident command briefing. New-result interface flow confirmed stable overnight under the hotfix. Manual downtime reporting stood down for new results at 8:00 a.m.; reconciliation of the backlog continues.
- **9:00 a.m.** — Dr. Vasilenko initiates the formal harm review in parallel with reconciliation, screening every patient with a delayed actionable result for clinical consequence.
- **Throughout the day** — Reconciliation proceeds chart by chart. HIM begins annotating replayed duplicates so the results-review display distinguishes original values. EHR vendor engaged on correcting displayed timestamps; a display-layer fix mapping the original observation time is validated in the test environment.
- **6:00 p.m.** — Critical chemistry reconciliation complete: all 340 verified, clinician awareness confirmed for each actionable value.

### Friday, February 12

- **11:00 a.m.** — EHR display fix applied; replayed results now sort and display by original collection time, with an annotation noting delayed filing.
- **4:30 p.m.** — Microbiology reconciliation complete: all 1,120 results verified in chart, all positive cultures and susceptibility changes confirmed with responsible clinicians.
- **6:00 p.m.** — **Incident closed** by Dr. Abdullahi. Reconciliation complete, interface stable, monitoring interim measures in place (twice-daily manual hold-queue inspection pending permanent fixes). Harm review continues as a quality process.

### Saturday, February 13

- Reportable event filed with the Connecticut Department of Public Health. Sentinel event review opened for one case. Disclosure conversations scheduled for 11 patients/families per HVH disclosure policy.

---

## 4. Root Cause

**A vendor patch changed HL7 segment parsing such that two clinically significant message profiles — microbiology results with more than three organism entries, and critical-flagged chemistry results — failed parsing and were routed to a hold queue instead of filing or erroring, and the organization's monitoring model had no mechanism to detect messages that neither succeeded nor failed visibly.**

Two elements combine here, and both were necessary:

1. **The parsing defect.** Patch 14.3.2 altered handling of repeating OBX segments. Messages with more than three repetitions of the affected field structure, and messages carrying the abnormal-flag pattern used for criticals, failed the new parser. The vendor had documented this as a known issue in an October 2026 portal advisory that never reached HVH's integration team, because no one at HVH was subscribed to the vendor's advisory feed after the 2025 reorganization.

2. **The silent failure path.** Confluence distinguishes between an *error queue* (surfaced on the dashboard, red) and a *hold queue* (not surfaced, treated as transient). The failed messages routed to hold. The dashboard's health model — interfaces up, error count zero — answered the question "is anything broken?" but not the question "is everything that should have arrived actually arriving?" No volume-based or delivery-confirmation monitoring existed. A 62-hour outage of two entire result categories was invisible to every automated surface the organization operated.

The root cause is therefore not "a bad patch." Vendors ship defective patches; that is an expected hazard. The root cause is that the organization's interface architecture and monitoring design allowed a defective patch to fail *silently*, for days, in a way that only a clinician's phone call could reveal.

---

## 5. Contributing Factors

The quality review identified seven contributing factors. None alone caused the incident; together they determined that it would happen, that it would last 62 hours, and that the recovery would create its own hazard.

### 5.1 Broken alerting path, undetected for 14 months

Confluence's hold-queue notifications routed to the "IntEng-Alerts" distribution list. A December 2025 departmental reorganization migrated staff to new group structures; the old list was emptied but never deleted, so mail to it was silently discarded rather than bouncing. No process existed to verify that alert destinations resolve to actual humans, and no synthetic test alert had ever been sent. The alerting path had been dead for 14 months; nothing in that period exercised it in a way anyone noticed, so its failure was invisible until it mattered.

### 5.2 Regression testing covers 18% of message types

The interface regression suite validates 40 of 218 message types Confluence handles. Coverage was built around the highest-volume profiles (ADT, basic chemistry, common hematology). Multi-organism microbiology results and critical-flag variants — lower volume but among the highest clinical stakes — were not in the suite. The post-patch verification on February 7 passed because it tested only covered profiles. Test coverage was weighted by volume, not by clinical risk.

### 5.3 Six-month patch latency, then application without soak

The patch sat available from August 2026 to February 2027. When applied, it went to production after basic smoke testing rather than a test-environment soak against a representative sample of production messages. The long deferral also meant the October 2026 vendor advisory — published between release and application — was the operative safety information, and the organization had no channel receiving it. There was no defined patch-management cadence for interface infrastructure: patches were applied opportunistically during maintenance windows, with risk assessment based on vendor characterization rather than local testing.

### 5.4 Anchoring on the middleware during diagnosis

Three hours of the response were spent restarting analyzer middleware. This was not an unreasonable hypothesis — the middleware had caused a superficially similar incident in 2024, and the Confluence dashboard was green, which appeared to exonerate the engine. But the diagnostic process had no structured checklist for "message missing downstream, all dashboards green," and the hold queue was not part of anyone's standard triage view. The green dashboard actively misled the responders; the misdiagnosis was a predictable product of the monitoring design (see root cause) rather than a judgment failure. The review notes that direct queue-depth inspection — the query that found the problem at 3:35 p.m. — could have been the first step rather than the fourth if it had been in a runbook.

### 5.5 Stale downtime procedure

The laboratory downtime procedure was last revised in 2019. Since then, two rounds of unit consolidation closed or renamed nine of the 31 units it lists, and telephony changes killed two escalation extensions. The procedure had never been exercised in a drill against the current facility layout. Downtime documentation had no assigned owner, no review cycle, and no linkage to the facilities change process, so unit changes never triggered updates. The consequence was roughly an hour of improvisation during the highest-pressure phase of manual reporting.

### 5.6 Replay executed without clinical informatics review

The replay plan was technically sound — revert, verify, drain the queue — and was reviewed for technical completeness only. No clinical informatics review asked the questions that mattered at the bedside: How will replayed results be timestamped? How will they sort in results review? Will they trigger fresh critical-value alerts? Will clinicians be able to tell a Monday specimen from a Wednesday one? The answers produced 4,800 confusingly timestamped messages and a night of bedside ambiguity that itself created patient-safety risk. Additionally, the LIS retransmissions performed during troubleshooting were not deduplicated against the queue before replay, roughly tripling the message count. There was no organizational standard requiring clinical review of bulk data operations touching the chart.

### 5.7 Weak signal aggregation before detection

At least three early signals existed: the Monday nurse call about a missing electronic potassium, three Tuesday help desk tickets about absent results, and a technologist's Tuesday observation of untransmitted susceptibilities. Each was handled locally and none was correlated. The help desk had no pattern-detection trigger for multiple missing-result reports, and the informal "mention it to the shift lead" path had no guaranteed follow-through. The incident was detectable Tuesday afternoon; it was detected Wednesday midday.

---

## 6. What Worked

An honest accounting requires noting what limited the harm, because several of these are practices worth reinforcing rather than accidents worth ignoring.

**The critical-value phone policy functioned as the safety net it was designed to be.** Laboratory policy requires phoning critical values with read-back regardless of interface status. All 340 critical chemistry results were phoned at the time of resulting, and this is the principal reason the critical chemistry impact, while serious, did not produce the harm its volume suggests. The unmitigated exposure was concentrated in microbiology, where narrative results — organism identification, susceptibilities — are not phoned unless flagged, and where the nine delayed antibiotic changes occurred. The lesson is double-edged: the manual redundancy worked, and the categories without manual redundancy are where the patients were hurt.

**A clinician's low tolerance for an unexplained pending result triggered detection.** Dr. Kellerman called rather than waiting another day. The organization cannot depend on this — it is the failure of every automated layer that made her call the detection mechanism — but the culture in which a hospitalist calls the lab and the lab director personally traces the message within 35 minutes is worth naming and protecting.

**Escalation after detection was fast and non-defensive.** From the 12:30 p.m. call to a declared incident with manual reporting activated took just over four hours, including the three-hour misdiagnosis. Once the hold queue was found at 3:35 p.m., correlation to the patch, vendor engagement, and hotfix took just over four hours. Brannigan's decision to activate manual reporting at 4:40 p.m. — before the technical picture was complete — prioritized patient safety over waiting for certainty.

**Incident command brought order at the moment it was most needed.** Dr. Abdullahi's assumption of command at 9:00 p.m., in the middle of the duplicate-replay confusion, converted a spreading multi-front problem into a structured response with clear lanes: technical stabilization, laboratory operations, clinical reconciliation, and communication. The 9:20 p.m. house-wide broadcast with a concrete instruction — check collection time inside the result before acting — was credited by nursing staff in interviews as the single most useful communication of the incident.

**The reconciliation was rigorous and complete.** Osei-Bonsu's team verified all 1,460 results individually against the LIS, prioritized by clinical urgency, and required affirmative clinician confirmation for every actionable value rather than assuming chart presence equaled awareness. The overnight priority pass on criticals and positive cultures found the delayed-antibiotic cases within hours. Approximately 610 staff hours over 53 hours is a heavy cost, but the review found no affected result that reached Friday evening unverified.

**Laboratory staff improvised effectively around a broken procedure.** When the 2019 downtime document failed, lab staff built a working contact map from charge nurse numbers and hand-carried results within the first hour. Improvisation is not a plan, but the staff's ownership of the outcome prevented the stale procedure from becoming a second outage.

**The harm review and regulatory response were prompt and transparent.** The harm review launched Thursday morning, before reconciliation finished. The reportable event was filed within 24 hours of incident closure, disclosure conversations were initiated per policy, and one case was self-referred to sentinel event review.

---

## 7. What Did Not Work

**Monitoring answered the wrong question.** Every dashboard measured system health; nothing measured delivery completeness. "Green" meant "no visible errors," and this incident's entire failure mode lived in the gap between visible errors and actual delivery. The organization had, in effect, no monitoring for its most dangerous interface failure class.

**The alerting chain was dead and no one knew.** Fourteen months of alerts to an empty distribution list, silently discarded. There was no ownership, no verification, no synthetic testing of the alert path.

**Diagnosis had no runbook, so it followed memory.** The middleware hypothesis came from the most recent similar incident, not from a structured elimination process. Direct queue inspection — a five-minute query — happened three hours in.

**The downtime procedure had rotted.** Nine dead fax numbers and two dead extensions in a document meant to function precisely when systems fail. A downtime procedure that has not been drilled against the current facility is a false assurance, arguably worse than no procedure because it is trusted at the worst possible moment.

**The replay traded one incident for another.** Draining the queue without addressing timestamps, deduplication, or downstream alert behavior converted a "missing results" problem into a "wrong-looking results" problem at 8:15 p.m. on a Wednesday, with night-shift staffing absorbing the confusion. The absence of clinical review of the replay plan was the pivotal process gap of the response phase.

**Early signals dissipated into local channels.** Three independent signals over two days, none correlated, none escalated. Ticket triage treated systemic symptoms as individual chart problems.

**Vendor safety communications had no landing point.** A known-issue advisory relevant to this exact defect sat in a vendor portal for four months with no HVH subscriber.

---

## 8. Action Items

Owners are accountable individuals; several actions will require teams. Due dates were set by the Quality Review Committee and will be tracked at its monthly meeting until all items close. Status reporting to the Board Quality Committee quarterly.

### 8.1 Detection and Monitoring

| # | Action | Owner | Due |
|---|---|---|---|
| A1 | Implement delivery-confirmation (closed-loop) monitoring: every result the LIS marks as transmitted must be confirmed filed in the EHR within a defined SLA (15 min routine, 5 min critical); unconfirmed results alert automatically. | Gerard Thibodeaux, Mgr Integration Engineering | Apr 30, 2027 |
| A2 | Surface all Confluence queues — including hold queues — on the operational dashboard with depth and oldest-message-age thresholds that page on breach. Interim manual twice-daily inspection continues until deployment. | Gerard Thibodeaux | Mar 15, 2027 |
| A3 | Deploy volume-anomaly detection per message type: alert when hourly filing volume for any of the 218 message types deviates beyond statistical thresholds from its baseline. | Priya Ramanathan, Director IT Operations | May 31, 2027 |
| A4 | Audit every alert destination across interface and laboratory systems; assign a named owner to each; implement a monthly synthetic test alert that requires human acknowledgment, with non-acknowledgment escalating automatically. | Priya Ramanathan | Mar 31, 2027 |
| A5 | Integrate distribution list membership changes into the reorganization/offboarding checklist so alert-receiving groups cannot be emptied without a review of what routes to them. | Marcus Delgado, CISO (identity governance) | Apr 30, 2027 |

### 8.2 Testing and Change Management

| # | Action | Owner | Due |
|---|---|---|---|
| B1 | Expand the interface regression suite using risk-weighted coverage: all message types carrying critical values, microbiology, pathology, and blood bank results covered by Jun 30; full 218-type coverage by Oct 31. | Gerard Thibodeaux | Jun 30 / Oct 31, 2027 |
| B2 | Mandate a test-environment soak for all interface engine patches: minimum 72-hour replay of a de-identified representative production message sample, with filing verification per message type, before production approval. Update change-management policy accordingly. | Priya Ramanathan | Apr 15, 2027 |
| B3 | Establish an interface patch cadence: vendor patches assessed within 30 days of release, applied or formally deferred with documented rationale within 90 days. | Gerard Thibodeaux | Apr 15, 2027 |
| B4 | Subscribe named individuals (primary and backup) to all vendor advisory/known-issue feeds for Confluence, middleware, LIS, and EHR; route advisories into the change-management intake queue for triage. | Gerard Thibodeaux | Feb 28, 2027 |
| B5 | Require clinical informatics sign-off on any bulk data operation affecting the chart (replays, migrations, mass corrections), covering timestamps, display behavior, deduplication, and downstream alerting. Add as a mandatory change-record field. | Dr. Yusuf Abdullahi, CMIO | Mar 31, 2027 |

### 8.3 Response Readiness

| # | Action | Owner | Due |
|---|---|---|---|
| C1 | Publish a "results missing downstream, dashboards green" diagnostic runbook, with direct queue inspection as the first step; incorporate into Integration Engineering on-call training. | Gerard Thibodeaux | Mar 31, 2027 |
| C2 | Rewrite the laboratory downtime procedure against the current facility layout; replace fax-dependent routing with the secure messaging platform plus phone verification; assign the document a named owner and an annual review cycle triggered additionally by any unit change in the facilities change process. | Colleen Brannigan, Director Laboratory Services | Apr 30, 2027 |
| C3 | Conduct a live lab-downtime drill at both hospitals exercising the revised procedure end to end, including result delivery to every current unit; repeat semiannually. | Colleen Brannigan | Jun 30, 2027 |
| C4 | Build and test a documented replay procedure with the Confluence vendor: original-timestamp preservation, pre-replay deduplication, throttled release, and defined chart display behavior for delayed results. Validate in test environment. | Gerard Thibodeaux | May 31, 2027 |
| C5 | Implement help desk pattern detection: two or more tickets referencing missing/delayed results within 24 hours auto-escalate to Integration Engineering and Laboratory leadership as a potential systemic event. | Priya Ramanathan | Mar 31, 2027 |

### 8.4 Clinical Safety

| # | Action | Owner | Due |
|---|---|---|---|
| D1 | Evaluate extending manual-notification redundancy (currently limited to critical values) to positive blood cultures and clinically significant susceptibility changes; present recommendation to Medical Executive Committee. | Colleen Brannigan, with Dr. Elena Vasilenko | May 31, 2027 |
| D2 | Complete sentinel event review of the referred case and disclosure follow-up for all 11 patients/families; report findings to the Board Quality Committee. | Dr. Elena Vasilenko, VP Quality | Apr 30, 2027 |
| D3 | Deliver a clinician-facing safety briefing on interpreting delayed-filed results and the new annotation display; incorporate into nursing and provider onboarding. | Tamika Osei-Bonsu, CNIO | Apr 15, 2027 |
| D4 | Add "unexplained pending result beyond expected turnaround" to nursing and provider escalation guidance, with a single published lab contact number, reinforcing the behavior that detected this incident. | Tamika Osei-Bonsu | Apr 15, 2027 |

### 8.5 Verification

| # | Action | Owner | Due |
|---|---|---|---|
| E1 | Conduct a controlled failure-injection exercise: deliberately misroute test messages in the test environment and confirm that A1–A3 monitoring detects the condition within SLA. Repeat annually. | Priya Ramanathan | Jul 31, 2027 |
| E2 | Present a closure report on all action items, with evidence of effectiveness (not merely completion), to the Quality Review Committee and Board Quality Committee. | Dr. Yusuf Abdullahi | Nov 30, 2027 |

---

## 9. Closing Note from the Review Chair

This incident began with a vendor's defect, but it belonged to us. The defect determined *that* messages would fail; our systems determined that the failure would be invisible, our processes determined that it would last 62 hours, and our recovery planning determined that fixing it would briefly create a second hazard. Every one of those determinants was in place long before February 7, and any of several other patches, on other interfaces, could have found them.

The people involved responded well within the systems they were given: a lab director who activated manual reporting before the diagnosis was complete, an integration team that worked a plausible hypothesis and corrected course, a CMIO who imposed order on a chaotic evening, a reconciliation team that refused to close the incident until every result was verified in human hands. The purpose of this document is to change the systems so that the next silent failure — and there will be a next one — is loud, short, and boring.

*— Dr. Elena Vasilenko, on behalf of the Quality Review Committee*

---

## Appendix A: Harm Review Methodology and Case Summaries

### A.1 Methodology

The harm review, conducted February 11–20, 2027, under Dr. Vasilenko's direction, applied a three-tier screening process to all 1,214 affected patients:

**Tier 1 — Automated screen (all 1,214 patients).** Chart queries identified patients whose delayed result met any of the following criteria: critical chemistry value, positive blood culture, positive sterile-site culture, susceptibility result differing from empiric therapy coverage, or result associated with an active order for the corresponding condition. This tier flagged 187 patients for Tier 2 review.

**Tier 2 — Clinical record review (187 patients).** Trained abstractors (two quality nurses, one infectious disease pharmacist) reviewed each flagged chart to determine whether the delayed result would plausibly have changed management if available on time. Determinations were made against the actual clinical course, including whether the phoned critical value or empiric therapy already covered the finding. This tier identified 34 patients for Tier 3 physician review.

**Tier 3 — Physician panel adjudication (34 patients).** A three-physician panel (hospitalist, infectious disease, pathology) adjudicated each case for actual or potential harm using the organization's standard harm classification scale. Disagreements were resolved by consensus; two cases required a fourth reviewer.

### A.2 Findings

| Classification | Count |
|---|---|
| No harm — result delayed, no management change indicated | 153 |
| No harm — management change indicated but occurred on time via other channels (phoned criticals, clinician follow-up call) | 27 |
| Delay in indicated care > 24 hours, no detectable clinical consequence | 5 |
| Delay in indicated care > 24 hours, temporary harm or prolonged treatment | 4 |
| Delay associated with 30-day readmission | 2 (subset of the 4 above) |
| Referred to sentinel event review | 1 |

The nine patients with antibiotic changes delayed more than 24 hours comprise the last three rows. In all nine, a finalized susceptibility result indicated a change from empiric therapy — narrowing in five cases, broadening or switching in four — that did not occur until the result was surfaced during reconciliation or, in two cases, until a clinician independently called the lab.

### A.3 Case Summaries (De-identified)

**Cases 1–5 (delay without detectable consequence).** Susceptibility results indicating de-escalation from broad-spectrum empiric coverage were delayed 26–58 hours. Patients remained on effective but broader-than-necessary therapy. No adverse drug events occurred; antimicrobial stewardship impact noted but no patient-level harm identified.

**Case 6 (temporary harm).** Blood culture speciation and susceptibilities finalized Tuesday morning showed an organism resistant to the empiric agent. The result filed Wednesday at replay; therapy changed Thursday at 3:10 a.m. following the overnight priority pass. The patient experienced persistent fevers during the gap and required an extended stay of approximately two days. Recovered fully.

**Case 7 (temporary harm).** Urine culture from a post-surgical patient discharged Tuesday showed resistance to the discharge antibiotic. The result did not file; the discharge prescription was ineffective. The patient re-presented to the ED on day 6 with pyelonephritis and was readmitted for four days of IV therapy. Counted among the two attributed readmissions. Recovered fully.

**Case 8 (temporary harm, readmission).** Blood culture positivity communicated by phone per policy Monday evening, but organism identification and susceptibilities queued. Empiric coverage was partially active. The patient was discharged Wednesday morning — before detection — on oral step-down therapy chosen without the susceptibility data, which would have contraindicated it. Readmitted day 9 with recurrent bacteremia; treated and recovered. This is the second attributed readmission.

**Case 9 (sentinel event referral).** An immunocompromised inpatient with a multi-organism bloodstream infection — the message profile at the center of the parsing defect — had identification and susceptibility results for all four organisms queued from Monday evening. Empiric therapy did not cover one organism. Therapy was corrected early Thursday following the priority pass, approximately 56 hours after the result finalized. The patient's course included ICU transfer Wednesday night. Because the temporal relationship between the coverage gap and the deterioration could not be excluded, the case met HVH's criteria for sentinel event review, which remains in progress under separate governance (Action D2). The family disclosure conversation occurred February 15 with Dr. Vasilenko and the attending physician present.

### A.4 Disclosure

Eleven patients or families received formal disclosure under HVH's communication-and-resolution policy: the nine delayed-therapy patients plus two patients whose charts contained replay-related duplicate values that a family member observed in the patient portal and questioned. All disclosures were completed by February 20. Two families requested follow-up meetings, both held. No claims had been filed as of this document's approval date.

---

## Appendix B: Technical Detail of the Parsing Defect

### B.1 Affected Message Structures

Confluence patch 14.3.2 modified the engine's handling of repeating field structures within ORU^R01 result messages. Two production message profiles at HVH intersected the change:

**Profile 1 — Multi-organism microbiology (1,120 messages).** HVH's LIS transmits organism-level results as repeating OBX segment groups, one group per isolate, with susceptibility panels nested as sub-repetitions. The patched parser allocated a fixed three-repetition structure for the affected field pattern; a fourth organism group caused a parse exception. Cultures with one to three isolates filed normally throughout the incident, which is why routine microbiology volume appeared largely intact and why the failure pattern was not obvious from gross volume alone — the affected messages were roughly 8% of microbiology traffic but included, by their nature, the most complex and clinically consequential cultures.

**Profile 2 — Critical-flagged chemistry (340 messages).** HVH's LIS populates the abnormal flags field (OBX-8) with a compound flag pattern for critical values (e.g., `HH~CRIT`), using a repetition delimiter within the field. The patched parser rejected the repetition in that position. Non-critical results, carrying single-component flags, parsed normally. The defect thus selected for precisely the results carrying the highest clinical urgency.

### B.2 Queue Routing Behavior

Confluence's error-handling configuration at HVH, dating to the original 2021 implementation, routed parse exceptions of this class to a *hold queue* with a retry policy of zero retries and no expiration — a configuration intended for transient downstream unavailability, misapplied to parse failures. Parse failures should route to the error queue, which is dashboard-visible and alarmed. The vendor's October 2026 advisory recommended a configuration change alongside the patch; HVH never received the advisory (Contributing Factor 5.7 / Action B4). The hold-queue routing rule has since been corrected: all parse exceptions now route to the error queue (completed February 14, 2027, verified by failure injection).

### B.3 Replay Timestamp Behavior

During the February 10 replay, Confluence rewrote the MSH-7 (message date/time) field to the transmission time, per its default replay behavior. The EHR's results-review display at HVH sorted on a derived field influenced by MSH-7 rather than exclusively on OBX-14 (observation date/time), which retained the original collection timestamps throughout. The original data was therefore never lost — it was present in every replayed message — but the display layer surfaced the wrong field. The February 12 EHR display fix remapped sorting and primary display to observation time, with a persistent annotation ("Result filed [date] — delayed transmission; refer to collection time") applied to all 4,800 replay-filed messages. The documented replay procedure under development (Action C4) will configure MSH-7 preservation at the engine level so the display layer is not the only defense.

---

## Appendix C: Communications Record

Key communications issued during the incident, retained in the incident command log:

| Date/Time | Channel | Audience | Summary |
|---|---|---|---|
| Feb 10, 5:30 p.m. | Secure message + email | All clinicians | Lab results from Feb 7 forward may be missing; call lab for anything pressing. |
| Feb 10, 9:20 p.m. | Secure message + overhead protocol | All clinical staff, both campuses | Results filed after 8:15 p.m. may be delayed originals; verify collection time before acting. |
| Feb 11, 7:45 a.m. | Email | All staff | Incident status, manual reporting stand-down for new results, reconciliation underway. |
| Feb 11, 12:00 p.m. | Portal banner | Patients (portal users) | Some lab results displayed with delayed dates; contact care team with questions. |
| Feb 12, 6:30 p.m. | Email | All staff | Incident closed; reconciliation complete; postmortem to follow. |
| Feb 13, 10:00 a.m. | Formal filing | CT Department of Public Health | Reportable event submission. |
| Feb 16, 9:00 a.m. | Meeting | Medical Executive Committee | Preliminary findings briefing by Dr. Abdullahi and Dr. Vasilenko. |
| Feb 24, 2:00 p.m. | Meeting | Board Quality Committee | Full incident briefing and draft action plan. |

The review noted one communications gap for future improvement: no proactive communication was issued to the 22 ambulatory clinics until the Thursday 7:45 a.m. all-staff message, despite clinic patients being within scope. Ambulatory-specific notification has been added to the incident communication template (folded into Action C2's procedural rewrite).

---

## Appendix D: Interview and Evidence Sources

The quality review team conducted 23 interviews between February 13 and February 27, 2027: laboratory leadership and bench staff (7), integration engineering (4), help desk and IT operations (3), nursing staff and supervisors from affected units (5), physicians including Dr. Kellerman (2), and vendor representatives from the Confluence and middleware vendors (2). Documentary evidence included Confluence server and queue logs, LIS audit trails, the change record for patch 14.3.2, help desk tickets #88412, #88437, and #88459, the incident command log, the 2019 downtime procedure document, distribution list audit history, and the vendor's October 2026 known-issue advisory. All interviews were conducted under HVH's just-culture policy; no interview content was used for individual performance evaluation.

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| Confluence | HVH's interface engine; routes and translates messages between clinical systems. |
| Interface engine | Middleware that receives, transforms, and delivers healthcare messages between systems. |
| HL7 / ORU^R01 | The messaging standard and specific message type used to transmit lab results. |
| OBX / OBR / MSH segments | HL7 message components carrying, respectively, observation results, order context, and message header metadata. |
| Hold queue | A Confluence queue for messages awaiting redelivery; not surfaced on the dashboard at the time of the incident. |
| Error queue | A dashboard-visible, alarmed queue for failed messages. |
| LIS | Laboratory information system; manages specimen workflow and result finalization. |
| Replay | Retransmission of queued or stored messages through the engine to downstream systems. |
| Critical value | A result requiring immediate clinician notification; phoned with read-back per policy. |
| Soak test | Extended pre-production testing under representative load and message variety. |
| Closed-loop monitoring | Verification that each transmitted message was actually received and filed downstream. |

---

## Document Approval and Revision History

| Version | Date | Author/Approver | Notes |
|---|---|---|---|
| 0.1 | Feb 18, 2027 | Quality review team | Initial draft; timeline and impact sections. |
| 0.2 | Feb 25, 2027 | Quality review team | Contributing factors and action items added following interviews. |
| 0.3 | Mar 2, 2027 | Dr. Abdullahi, Dr. Vasilenko | Harm review appendix added; action item owners and dates confirmed with owners. |
| 1.0 | Mar 9, 2027 | Quality Review Committee | Approved as final. Distributed per distribution list on page 1. |

**Approvals:**

Dr. Elena Vasilenko, VP Quality & Patient Safety — Review Chair
Dr. Yusuf Abdullahi, Chief Medical Information Officer — Document Owner
Colleen Brannigan, Director of Laboratory Services
Tamika Osei-Bonsu, Chief Nursing Informatics Officer
Priya Ramanathan, Director of IT Operations

*Action item status will be reviewed monthly by the Quality Review Committee until closure, with quarterly reporting to the Board Quality Committee. The effectiveness verification report (Action E2) is due November 30, 2027.*

*— End of Document —*
