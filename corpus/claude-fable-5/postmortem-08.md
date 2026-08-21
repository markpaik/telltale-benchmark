# Incident Postmortem Report

## Quinsigamond Regional Water Pollution Control Authority

### Unpermitted Bypass Discharge to the Blackstone River — March 14–16, 2027

| | |
|---|---|
| **Incident ID** | QRWPCA-2027-003 |
| **Incident Classification** | Severity 1 — Unpermitted Discharge / NPDES Permit Violation |
| **Incident Period** | March 14, 2027, 9:48 p.m. through March 16, 2027, 11:05 p.m. |
| **Report Status** | Final |
| **Report Date** | April 24, 2027 |
| **Approved By** | Alonzo Ferreira, Executive Director |
| **Distribution** | QRWPCA Board of Directors; Member Town Administrators; Massachusetts Department of Environmental Protection (upon request); All QRWPCA Staff |

**Statement of Purpose.** This postmortem examines the systems, procedures, and organizational conditions that produced a 41-hour bypass of partially treated wastewater to the Blackstone River. Consistent with the Authority's just-culture commitment, this document does not assign individual fault. Every person named acted on the information available to them at the time, within systems that this report finds were inadequate to the situation. The purpose of naming individuals is to establish an accurate factual record and to assign ownership of corrective actions — not to attribute blame. The failures described here are failures of design, maintenance prioritization, configuration management, and institutional knowledge transfer. They could have manifested on any shift, with any crew.

---

## 1. Executive Summary

On the night of March 14, 2027, a storm delivered 3.1 inches of rain in 14 hours across the Quinsigamond Regional Water Pollution Control Authority's service area, driving influent flows well above the facility's average daily treatment volume of 34 million gallons per day (MGD). At 9:52 p.m., influent pump 2 tripped offline on a fault in its variable frequency drive (VFD) — a component whose replacement had been budgeted in FY25 and deferred in two successive capital cycles. Under normal conditions, the resulting rise in the influent wet well would have triggered a high wet well alarm at the operator console within minutes.

The alarm never annunciated. It had been silenced on February 3, 2027, during a contractor's SCADA point-verification test and was never restored to service. The automated silenced-point exception report that should have flagged the condition was routed to a supervisory position vacated by retirement in November 2026 and never re-assigned. As a result, the plant operated for six hours with a rising wet well and no operator awareness of the pump failure.

Chief Plant Operator Dmitri Sokolov discovered the high wet well condition on physical rounds at 3:40 a.m. on March 15. Working without alarm history to guide diagnosis, the on-shift crew attributed the condition to a utility power dip logged at 9:48 p.m. — a plausible but incorrect explanation that consumed additional response time. At 4:10 a.m., the crew started standby pump 4 to recover capacity. The pump's discharge valve had been left closed following a January valve exercise, a condition not detectable from the control room and not covered by a pre-start verification step. The pump ran dead-headed, destroying its impeller and reducing the plant's firm influent pumping capacity to 19 MGD at the height of the storm inflow.

Compounding the capacity loss, bar screen 1 had been out of service on a maintenance work order open for 94 days, forcing all flow through bar screen 2, which blinded with storm debris at 5:20 a.m. With headworks capacity collapsing and the wet well at overflow elevation, Director of Operations Kathleen Ng declared a bypass at 6:05 a.m. Compliance Manager Rochelle Grantham notified the Massachusetts Department of Environmental Protection at 6:40 a.m. — approximately one hour past the two-hour regulatory notification window, which began when staff became aware of the uncontrolled discharge condition at 3:40 a.m. Maintenance Supervisor Hollis Pruitt's team restored the standby pump valve arrangement by 2:00 p.m. on March 15, but sustained high inflow and reduced firm capacity kept the bypass in operation for 41 hours, ending at 11:05 p.m. on March 16.

The bypass released 11.4 million gallons of partially treated wastewater to the Blackstone River, in violation of the Authority's NPDES permit. A downstream drinking water intake operated on its backup source for four days. River recreational access remained posted closed for nine days. The state issued a notice of noncompliance carrying $312,000 in potential penalty exposure.

The root cause of this incident is not the storm, the pump trip, or any single operator decision. It is the systematic erosion of the plant's defense-in-depth: an alarm layer defeated by an unmanaged configuration change, a monitoring layer defeated by an orphaned report, a redundancy layer defeated by an unverified valve lineup, a screening layer defeated by deferred maintenance, and a response layer working from a wet weather operating plan last updated in 2016 — all under a staffing condition in which nine of 34 operator positions were vacant. Each layer failed independently and silently before the storm arrived. The storm merely revealed that they had failed.

This report identifies 18 corrective actions with named owners and due dates, spanning alarm management, maintenance governance, capital planning, emergency notification, and wet weather operations.

---

## 2. Impact

### 2.1 Environmental and Public Impact

| Measure | Value |
|---|---|
| Untreated/partially treated wastewater discharged | 11.4 million gallons |
| Duration of bypass discharge | 41 hours |
| Downstream drinking water intake on backup supply | 4 days |
| River recreational access posted closed | 9 days |
| Receiving water | Blackstone River |
| Permit status | Unpermitted bypass; NPDES violation |

### 2.2 Regulatory and Financial Impact

| Measure | Value |
|---|---|
| State notice of noncompliance | Issued |
| Penalty exposure | $312,000 |
| Regulatory notification delay | Approximately 1 hour past the 2-hour window |
| Standby pump 4 impeller replacement (estimated) | $87,000 (parts, labor, crane) |
| Emergency contractor and overtime costs (estimated) | $64,000 |
| Deferred VFD replacement now expedited | $118,000 |

### 2.3 Operational Impact

| Measure | Value |
|---|---|
| Firm influent pumping capacity during event | Reduced from 34 MGD to 19 MGD |
| Duration of undetected pump failure | 5 hours 48 minutes |
| Time from detection to bypass declaration | 2 hours 25 minutes |
| Standby pump 4 | Out of service (impeller destroyed) — restored to service April 2 |
| Bar screen 1 | Out of service 94+ days at time of event — restored March 20 |
| Time from bypass declaration to valve arrangement restoration | 7 hours 55 minutes |

### 2.4 Member Town Impact

Five member towns experienced no interruption of collection service; no sanitary sewer overflows occurred in the collection system. However, member towns absorbed public communication burdens related to river closures and the downstream intake switchover, and the Executive Director's briefing to town administrators did not occur until Sunday, March 21 — six days after the bypass began.

---

## 3. Timeline of Events

All times are Eastern. Timeline is reconstructed from SCADA historian records, work order logs, the plant operations logbook, contractor test documentation, and structured interviews with on-shift and responding personnel.

### 3.1 Latent Conditions (Pre-Incident)

**FY25 capital budget cycle** — Replacement of the influent pump 2 variable frequency drive is approved in the FY25 capital plan, then deferred to FY26 during mid-year budget rebalancing. It is deferred a second time in the FY27 plan. The drive remains in service beyond its manufacturer-recommended service life with a documented history of nuisance faults.

**November 2026** — The operations supervisor who received the SCADA silenced-point exception report retires. The report's distribution list is not updated; the report continues to generate and route to an inactive mailbox. No procedure exists for reassigning system-generated reports upon personnel departure.

**December 11, 2026** — Work order WO-26-1847 is opened for bar screen 1's failed rake motor. The motor requires a sourced replacement; the work order enters the backlog. No escalation trigger exists for aging work orders on redundancy-critical equipment. At the time of the incident, the work order has been open 94 days.

**January 2027** — During a scheduled quarterly valve exercise on the standby pump 4 discharge line, the discharge valve is cycled and left in the closed position. The valve exercise procedure does not include a documented return-to-service lineup verification, and the valve has no remote position indication on SCADA. The closed condition persists undetected for approximately two months.

**February 3, 2027** — A SCADA integration contractor performs point-verification testing on wet well instrumentation. To prevent nuisance annunciation during testing, the high wet well alarm is placed in a silenced (suppressed) state. Testing concludes, but the alarm is not restored. The management-of-change process in effect does not require a documented restoration checklist or independent verification for temporary alarm suppression. The nightly silenced-point exception report flags the condition — into the unmonitored mailbox of the retired supervisor — every night for 39 nights.

### 3.2 Event Sequence

**Saturday, March 14, 2027**

| Time | Event |
|---|---|
| ~8:00 a.m. | Rainfall begins. The storm ultimately delivers 3.1 inches over 14 hours. Influent flows climb through the day. The on-shift crew operates per routine wet weather practice; the wet weather operating plan (2016 edition) contains no defined staffing surge trigger for forecast events of this magnitude. |
| 9:48 p.m. | A momentary utility power dip is logged by the plant electrical monitoring system. All major equipment rides through or restarts normally. This log entry later anchors the crew's misdiagnosis. |
| 9:52 p.m. | Influent pump 2 trips offline on a VFD fault. SCADA historian records the trip. The high wet well alarm point — the designed annunciation path for this failure mode — is in a suppressed state and does not alarm. No console indication reaches the operator on duty. The pump trip itself generates a status change in the historian but not a configured priority alarm. |
| 9:52 p.m. – 3:40 a.m. | Wet well level rises steadily as storm inflow exceeds remaining pumping capacity. With one operator covering the console and process areas across a plant carrying nine operator vacancies, physical rounds of the headworks occur on an extended interval. **Detection gap: 5 hours 48 minutes.** |

**Sunday, March 15, 2027**

| Time | Event |
|---|---|
| 3:40 a.m. | Chief Plant Operator Dmitri Sokolov, performing rounds, observes the wet well at critically high level and pump 2 stopped. He returns to the control room and finds no active alarm and no alarm history for the wet well point — consistent with, and caused by, the suppression. |
| 3:40 – 4:05 a.m. | Diagnosis. The absence of alarm history leads the crew away from an instrumentation or suppression explanation. The 9:48 p.m. power dip in the electrical log offers a coherent narrative — a dip tripped the pump and (the crew reasons) may have disrupted alarming. The crew attempts remote reset of pump 2; the VFD fault will not clear. **Misdiagnosis cost: approximately 25 minutes**, though the more consequential effect was directing attention away from the SCADA configuration, which delayed recognition that other alarms might also be unreliable. |
| 4:10 a.m. | The crew starts standby pump 4 to restore firm capacity. The pump's discharge valve — left closed since the January valve exercise, with no remote position indication and no pre-start lineup verification step in the operating procedure — blocks flow. The pump dead-heads. |
| 4:10 – 4:22 a.m. | Pump 4 runs against the closed valve. Abnormal amperage and no discharge flow are recognized; the pump is secured. Post-incident inspection confirms the impeller is destroyed. **Firm influent pumping capacity falls to 19 MGD** against storm inflows substantially exceeding that figure. |
| 4:22 – 5:20 a.m. | The crew maximizes remaining pumping and begins storm response callouts. Callout response is slowed by the vacancy-thinned roster; the 2016 wet weather plan's call list contains outdated names and numbers. |
| 5:20 a.m. | Bar screen 2 — carrying the entire plant flow because bar screen 1 has been out of service 94 days on WO-26-1847 — blinds with storm debris. Headworks throughput drops further. Manual raking begins but cannot keep pace. |
| 5:40 a.m. | *Regulatory notification deadline passes.* Two hours have elapsed since staff became aware of conditions constituting an imminent or actual uncontrolled discharge (3:40 a.m.). The 2016 wet weather plan does not clearly define the notification trigger point or assign a notification role to the overnight shift; notification is understood in practice to follow a formal bypass declaration by senior management. |
| 6:05 a.m. | Director of Operations Kathleen Ng, on site following callout, declares a controlled bypass to protect upstream collection system integrity and prevent uncontrolled flooding of the headworks and electrical galleries. Bypass discharge to the Blackstone River begins. |
| 6:40 a.m. | Compliance Manager Rochelle Grantham notifies the Massachusetts Department of Environmental Protection. **Notification is approximately one hour past the two-hour window** measured from 3:40 a.m. awareness. |
| 7:15 a.m. | Maintenance Supervisor Hollis Pruitt arrives with a maintenance crew and begins assessment of the pump 4 valve arrangement and impeller damage. |
| 9:30 a.m. | Downstream drinking water utility, notified through state channels, switches its intake to backup supply as a precaution. |
| 2:00 p.m. | Pruitt's crew completes restoration of the standby pump discharge valve arrangement and verifies the lineup. Pump 4 remains unavailable due to impeller destruction; the corrected lineup permits future standby operation once the impeller is replaced and supports hydraulic management of the headworks. |
| Afternoon/evening | Bypass continues. Sustained elevated inflow from the saturated collection system, combined with firm capacity limited to 19 MGD and degraded screening, prevents bypass termination. State posts river access closures. |

**Monday, March 16, 2027**

| Time | Event |
|---|---|
| Through the day | Inflow recedes as the collection system drains. Bar screen 2 is progressively cleared; contract crews assist with manual screening. Plant flows are brought fully back through the treatment train in stages. |
| 11:05 p.m. | Inflow falls sustainably below available firm capacity. **Bypass is terminated after 41 hours.** Total discharge: 11.4 million gallons. |

### 3.3 Post-Event

| Date | Event |
|---|---|
| March 17–19 | River sampling program conducted with state oversight. Downstream intake remains on backup supply through March 19 (4 days). |
| March 20 | Bar screen 1 rake motor replacement completed; screen returned to service. |
| March 21 (Sunday) | Executive Director Alonzo Ferreira briefs member town administrators — six days after the bypass began. Towns had received no direct Authority communication before this briefing. |
| March 24 | River access closure lifted (9 days). |
| March 27 | State issues notice of noncompliance; penalty exposure $312,000. |
| April 2 | Standby pump 4 impeller replaced; pump returned to service. |
| April 6–17 | Postmortem interviews and record reconstruction conducted. |

---

## 4. Root Cause Analysis

### 4.1 Method

The analysis team applied a "five whys" progression on each failure thread, then consolidated threads using a Swiss-cheese (defense-in-depth) model to identify where independent barriers failed and why those failures shared common organizational origins.

### 4.2 Root Cause Statement

**The Authority lacked effective configuration management and life-cycle governance for its safety-critical systems — alarms, standby equipment lineups, redundancy-critical maintenance, and emergency procedures — such that multiple independent layers of protection were silently defeated before the storm and no mechanism existed to detect their defeated state.**

Stated differently: the incident was not caused by the failure of pump 2. Pump failures during storms are an anticipated event, and the plant was designed with layered defenses against exactly this scenario. The incident was caused by the fact that every one of those layers had already failed, invisibly, through gaps in the organization's change management, knowledge transfer, and asset governance:

1. **The alarm layer** was defeated on February 3 by a temporary suppression with no restoration control.
2. **The monitoring layer** (the silenced-point report) was defeated in November 2026 by an unmanaged personnel departure.
3. **The redundancy layer** (standby pump 4) was defeated in January by a valve exercise with no return-to-service verification.
4. **The screening redundancy layer** was defeated in December by a work order backlog with no criticality-based escalation.
5. **The equipment reliability layer** was defeated across FY25–FY27 by capital deferral without an accompanying risk assessment.
6. **The response layer** was degraded by a wet weather plan eleven years out of date and a staffing level nine operators below complement.

No individual on shift the night of March 14 could have known that all six layers were compromised, because the organization possessed no process for knowing it either.

### 4.3 Why-Chain Illustration (Alarm Thread)

- *Why did the plant not detect the pump trip for six hours?* The high wet well alarm did not annunciate.
- *Why did it not annunciate?* It was suppressed during contractor testing on February 3 and never restored.
- *Why was it never restored?* The suppression process required no restoration checklist, no time limit, no supervisor sign-off, and no independent verification.
- *Why did the exception report not catch it?* The report routed to a position vacated in November; no offboarding step reassigns system-generated reports.
- *Why did no periodic review catch it?* The Authority conducts no scheduled audit of suppressed, inhibited, or forced SCADA points.

Each thread in Sections 5.1–5.6 resolves to the same terminal answer: absence of a governance process, not absence of individual diligence.

---

## 5. Contributing Factors

### 5.1 Alarm Suppression Without Management of Change

The February 3 suppression was a reasonable and routine testing practice. What was missing was everything around it: a suppression log requiring an expiration time, a restoration step with independent verification, contractor closeout documentation confirming point states, and any recurring audit of suppressed points. The alarm system's own safety net — the nightly silenced-point exception report — existed but had been severed from human attention by the November retirement. **Two independent controls failed for the same underlying reason: the Authority manages alarm configuration informally, and manages report distribution not at all.** The suppression persisted 39 days, flagged nightly to no one.

### 5.2 The Detection Gap (5 Hours 48 Minutes)

Even with the primary alarm defeated, three secondary mechanisms could have shortened the gap and did not:

- **Alarm rationalization.** The pump 2 trip itself generated only a status change, not a priority alarm. The alarm philosophy (undocumented) does not designate influent pump trips during wet weather as high-priority annunciations.
- **Rounds frequency.** With nine of 34 operator positions vacant, overnight rounds intervals had lengthened informally. There is no documented minimum rounds frequency for storm conditions; the 2016 wet weather plan predates the current staffing reality and assumes a headworks-dedicated operator during major storms.
- **Trend monitoring.** Wet well level was trending upward on the historian for nearly six hours. No level-rate-of-change alarm exists, and console layout does not surface wet well trends prominently. A rate-of-change alarm would have annunciated independently of the suppressed high-level point.

The detection gap converted a manageable single-pump failure into a crisis. At 10:15 p.m., the response options were numerous; at 3:40 a.m., they were few and time-pressured.

### 5.3 The Misdiagnosis

The crew's attribution of the failure to the 9:48 p.m. power dip was rational given available evidence: a logged electrical event four minutes before the trip, and — critically — an alarm history that showed nothing, which argued against believing the alarm system itself. The misdiagnosis was a direct downstream effect of the suppression: **the defeated alarm not only failed to alert, it actively corrupted the diagnostic picture.** The direct time cost (~25 minutes) was modest; the larger cost was that the crew proceeded into the pump 4 start without suspecting that other unverified states (such as valve lineups) might also exist. No troubleshooting aid, decision tree, or SCADA point-state display was available to prompt the question "is this alarm suppressed?" — a single-click check that would have reframed the entire response.

### 5.4 The Pump Start That Cut Firm Capacity

Starting standby pump 4 was the correct decision. Its execution was defeated by three converging design and procedural gaps:

- **No return-to-service verification after valve exercises.** The January procedure ended with the valve cycled, not with a documented restoration to the required lineup, and no second-person check.
- **No remote valve position indication.** The discharge valve state is invisible from the control room. Under time pressure at 4:10 a.m., with one crew member available and the wet well approaching overflow, dispatching someone to physically walk the discharge line before start was a trade-off the situation punished.
- **No pre-start checklist for standby equipment.** The standby pump start procedure contains no valve lineup confirmation step and no direction to verify discharge flow/pressure within a defined interval after start. Dead-head protection (low-flow or high-discharge-pressure trip) was not configured on pump 4.

The consequence was severe: the plant's remaining margin was destroyed at the worst possible moment, dropping firm capacity to 19 MGD and making the bypass effectively unavoidable.

### 5.5 The Late Regulatory Notification

Notification at 6:40 a.m. was roughly one hour past the two-hour window that began with 3:40 a.m. awareness. The delay was procedural, not evasive:

- The 2016 wet weather plan ties notification to a **formal bypass declaration by senior management**, rather than to the regulatory trigger of *awareness of an actual or imminent noncompliant discharge*.
- The overnight shift had **no delegated notification authority** and no quick-reference notification card at the console.
- The compliance on-call structure routed through a single individual; Compliance Manager Grantham was called out through the general callout tree and notified the state 35 minutes after the declaration — promptly, once the process reached her. The delay accrued upstream of her involvement.

The late notice carried real consequences: it compressed the state's and the downstream water utility's response window, contributed to the precautionary four-day intake switchover, and is an aggravating element in the noncompliance notice.

### 5.6 Deferred Capital Work and Maintenance Backlog

Two deferred items sat directly in the causal chain:

- **The pump 2 VFD**, budgeted in FY25 and deferred twice, initiated the event. The deferral decisions were made as budget line items without a documented operational risk assessment, and without visibility to operations leadership of the aggregate risk created by successive deferrals on the same asset.
- **Bar screen 1's rake motor**, on a work order open 94 days, eliminated screening redundancy. The CMMS has no aging-escalation rule and no criticality flag that would elevate redundancy-loss conditions to management review.

Both reflect the same governance gap: **the Authority tracks maintenance and capital work by cost and schedule, not by risk.** A risk-ranked view would have shown, before the storm, that the plant was operating with degraded influent pumping reliability, no screening redundancy, and (had suppression audits existed) a defeated primary alarm — a combination no one would knowingly have accepted heading into a forecast 3-inch rain event.

### 5.7 Organizational and Systemic Factors

- **Staffing:** Nine of 34 operator positions vacant (26%). This lengthened rounds intervals, slowed callout response, and eliminated the second set of eyes that catches lineup and configuration errors.
- **Wet weather operating plan (2016):** Predates current SCADA architecture, current staffing levels, and two rounds of equipment changes. Call lists were outdated; storm staffing triggers, notification triggers, and bypass decision criteria were absent or ambiguous.
- **Knowledge transfer:** The November retirement removed not only a report recipient but institutional knowledge of the alarm exception process itself. No offboarding checklist covers system roles, report distributions, or procedural knowledge capture.

---

## 6. Response Assessment

### 6.1 What Worked

1. **Physical rounds caught what technology missed.** Sokolov's 3:40 a.m. rounds discovery was the event's first successful barrier. Disciplined rounds practice, even under short staffing, bounded the detection gap at six hours rather than allowing an uncontrolled overflow with no operator awareness at all.
2. **The bypass decision was timely and correct once conditions were understood.** Ng's 6:05 a.m. declaration protected the collection system from backups into homes and businesses and protected plant electrical infrastructure from flooding that would have extended the outage from days to weeks. No sanitary sewer overflows occurred in any member town.
3. **Rapid recognition of the dead-head condition.** The crew secured pump 4 within 12 minutes of start, limiting damage to the impeller. A longer run risked motor, seal, and casing damage and a far longer standby outage.
4. **Maintenance mobilization and valve restoration.** Pruitt's crew assessed, corrected, and verified the standby pump valve arrangement within eight hours of the bypass declaration, on a Sunday, restoring the hydraulic flexibility needed to manage the remainder of the event.
5. **Notification quality, once initiated.** Grantham's report to the state was complete and accurate, and her subsequent coordination — sampling plans, discharge volume accounting, and daily status reports — was cited by state staff as cooperative and thorough. The downstream intake switchover proceeded smoothly through the state channel.
6. **Bypass operation and termination discipline.** The bypass was metered, sampled, and documented throughout, enabling the precise 11.4-million-gallon accounting in this report, and was terminated promptly when inflow receded.
7. **No injuries.** Despite overnight emergency work around an overflowing wet well, energized equipment, and confined-space-adjacent areas, no staff or contractor injuries occurred.

### 6.2 What Did Not Work

1. **The plant's automated detection layer was entirely absent** — the defining failure of the event. Six hours of rising wet well level generated zero operator-facing annunciations.
2. **Alarm and configuration state was invisible to responders.** The crew had no ready means to see that the wet well alarm was suppressed, which corrupted diagnosis and concealed the possibility of other unverified states.
3. **Standby equipment was not ready when called.** The plant's core redundancy asset failed on start due to a two-month-old lineup error that verification steps would have caught in January, and that remote position indication or a pre-start check would have caught at 4:10 a.m.
4. **The notification process was structurally late.** Tying notification to a management bypass declaration guaranteed a violation of the two-hour window in any scenario where awareness precedes declaration by more than two hours — as it did here.
5. **The 2016 wet weather plan actively hindered the response.** Outdated call lists slowed mobilization; missing staffing triggers left the overnight shift thin during a forecast major storm; missing notification triggers produced the late report.
6. **Maintenance and capital governance did not surface accumulating risk.** A 94-day redundancy-loss work order and a twice-deferred VFD replacement sat in routine backlogs with no escalation, review, or risk flag.
7. **Member town communication lagged badly.** Towns learned of a nine-day river closure affecting their residents largely through state postings and media; the Authority's first direct briefing came six days after the bypass began. This damaged institutional trust independent of the environmental impact.
8. **Single-operator overnight coverage during a major storm** left no capacity for parallel tasks — console monitoring, rounds, diagnosis, and physical valve verification all competed for one person's attention at the critical moment.

---

## 7. Action Items

All actions are tracked in the Authority's corrective action register. The Executive Director reviews status monthly with the Board's Operations Committee until closure. Owners are accountable for delivery; execution may be delegated.

### 7.1 Alarm Management and SCADA Configuration

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Immediately audit all SCADA points for suppressed, inhibited, forced, or out-of-service states; restore or formally document each. **(Completed April 3 — 11 additional suppressed points found and restored.)** | Dmitri Sokolov, Chief Plant Operator | **Complete** |
| 2 | Implement an alarm suppression management-of-change procedure: written authorization, expiration time, restoration checklist, and independent second-person verification for any suppression, including contractor testing. | Kathleen Ng, Director of Operations | May 29, 2027 |
| 3 | Reroute all system-generated exception reports to role-based distribution lists (not individual mailboxes); add report/system-role reassignment to the HR offboarding checklist. | Alonzo Ferreira, Executive Director (with HR Manager) | June 12, 2027 |
| 4 | Add suppressed-point count and list to the daily shift turnover report and console dashboard so alarm state is visible to every shift. | Dmitri Sokolov, Chief Plant Operator | June 26, 2027 |
| 5 | Develop a documented alarm philosophy and complete rationalization of headworks and influent pumping alarms, including priority annunciation of influent pump trips and a wet well level rate-of-change alarm. | Kathleen Ng, Director of Operations | September 25, 2027 |

### 7.2 Standby Equipment Readiness

| # | Action | Owner | Due Date |
|---|---|---|---|
| 6 | Revise all valve exercise and equipment isolation procedures to require a documented return-to-service lineup verification with second-person sign-off. | Hollis Pruitt, Maintenance Supervisor | May 15, 2027 |
| 7 | Issue pre-start checklists for all standby pumps, including valve lineup confirmation and a discharge flow/pressure verification within two minutes of start. | Dmitri Sokolov, Chief Plant Operator | May 15, 2027 |
| 8 | Configure dead-head protection (low-flow / high-discharge-pressure trip) on all influent and standby pumps. | Hollis Pruitt, Maintenance Supervisor | July 31, 2027 |
| 9 | Engineer and install remote position indication on standby pump discharge valves and other critical manual valves; interim measure: locked-open administrative control with monthly verified lineup walkdowns. | Kathleen Ng, Director of Operations (interim walkdowns: Hollis Pruitt, effective immediately) | December 17, 2027 (interim: in effect) |
| 10 | Institute a monthly standby equipment functional test program (start, flow verification, return to standby) for influent pumps, screens, and emergency power. | Hollis Pruitt, Maintenance Supervisor | June 30, 2027 |

### 7.3 Notification and Regulatory Compliance

| # | Action | Owner | Due Date |
|---|---|---|---|
| 11 | Rewrite the notification protocol to trigger on *awareness of actual or imminent noncompliant discharge*, delegate notification authority to the on-shift senior operator, and post a notification quick-reference card (contacts, script, required content) at the operator console. | Rochelle Grantham, Compliance Manager | May 8, 2027 |
| 12 | Establish a 24/7 compliance on-call rotation with a defined 15-minute response standard, and conduct quarterly notification drills on all shifts. | Rochelle Grantham, Compliance Manager | June 12, 2027 (first drill: July 2027) |
| 13 | Establish a member town communication protocol: initial notification to town administrators within 4 hours of any Severity 1 declaration, with update cadence defined through event closure. | Alonzo Ferreira, Executive Director | May 22, 2027 |

### 7.4 Maintenance and Capital Governance

| # | Action | Owner | Due Date |
|---|---|---|---|
| 14 | Assign criticality codes to all assets in the CMMS; configure automatic escalation to the Director of Operations for any redundancy-loss work order open more than 14 days, with monthly aged-backlog review by criticality. | Hollis Pruitt, Maintenance Supervisor | August 28, 2027 |
| 15 | Expedite replacement of the influent pump 2 VFD (emergency procurement) and complete a condition assessment of all remaining influent pump drives. | Kathleen Ng, Director of Operations | VFD: July 31, 2027; assessment: September 30, 2027 |
| 16 | Institute a capital deferral risk-review requirement: no deferral of a project on a criticality-coded asset without a documented operational risk assessment signed by the Director of Operations and reported to the Board. | Alonzo Ferreira, Executive Director | For FY28 budget cycle — September 30, 2027 |

### 7.5 Wet Weather Operations and Staffing

| # | Action | Owner | Due Date |
|---|---|---|---|
| 17 | Complete a full rewrite of the wet weather operating plan: forecast-based staffing surge triggers, minimum storm rounds frequency, bypass decision criteria, notification triggers, current call lists (verified quarterly), and annual tabletop exercise. Interim measure: updated call list and two-operator minimum overnight staffing during National Weather Service flood watch conditions, effective immediately. | Kathleen Ng, Director of Operations | October 30, 2027 (interim: in effect) |
| 18 | Deliver an operator recruitment and retention plan to the Board addressing the nine vacant positions, including wage benchmarking, an operator-in-training pipeline with area vocational programs, and certification incentives; report vacancy risk quarterly to the Board. | Alonzo Ferreira, Executive Director | July 24, 2027 |

---

## 8. Lessons Learned

1. **Defenses fail silently; only deliberate verification reveals them.** Every layer that failed on March 14 had been failed for weeks or months. Alarms, lineups, redundancy, and plans must be *proven* ready on a schedule — assumed readiness is indistinguishable from unreadiness until the storm arrives.
2. **A defeated alarm is worse than no alarm.** The suppressed wet well point not only failed to warn; its empty history misled the diagnosis. Alarm state must be as visible to operators as process state.
3. **Temporary changes are permanent until a process makes them temporary.** The February 3 suppression and the January valve position were both intended to last hours. Without expiration and restoration controls, "temporary" is a hope, not a fact.
4. **People are a control layer, and vacancies are a control failure.** The 26% operator vacancy rate did not appear in any risk register, yet it lengthened detection, thinned diagnosis, and removed verification capacity. Staffing levels belong in operational risk governance alongside equipment condition.
5. **Deferral decisions are risk decisions and must be made as such.** The VFD deferrals were fiscally rational in isolation. Viewed as risk acceptances on the plant's influent lifeline, they would likely have been decided differently — or at least knowingly.
6. **Regulatory clocks start at awareness, not at declaration.** Notification procedures must be built around the regulator's trigger, not the organization's internal decision structure, and the authority to notify must sit with whoever is on shift.
7. **Communication is part of the response, not an afterthought.** The six-day gap before member town briefings converted an operational failure into an institutional trust failure. Stakeholder notification deserves the same procedural rigor as regulatory notification.

---

## 9. Appendices

### Appendix A — Referenced Records

- SCADA historian export, March 13–17, 2027 (points: wet well level, influent pump status/amperage, screen differential)
- Plant electrical monitoring log, March 14, 2027
- Contractor point-verification test report, February 3, 2027
- CMMS work order WO-26-1847 (bar screen 1 rake motor)
- January 2027 valve exercise record, standby pump 4 discharge line
- FY25–FY27 capital plans and deferral records (influent pump 2 VFD)
- Bypass flow metering and sampling records, March 15–16, 2027
- MassDEP notice of noncompliance, March 27, 2027
- Operations logbook, March 14–17, 2027
- Structured interviews: on-shift operations crew, D. Sokolov, K. Ng, H. Pruitt, R. Grantham, A. Ferreira, SCADA contractor project lead (April 6–17, 2027)

### Appendix B — Severity Classification Reference

**Severity 1:** Unpermitted discharge to receiving waters; NPDES violation; public health protective action triggered downstream; regulatory enforcement exposure. This event met all four criteria.

### Appendix C — Review and Revision

This postmortem was reviewed in draft by all named individuals and by the on-shift operations crew for factual accuracy prior to finalization. Corrective action status will be appended quarterly until all 18 items are closed. A one-year effectiveness review, including a full-scale wet weather exercise validating actions 5, 7, 11, and 17, is scheduled for March 2028 under the ownership of the Director of Operations.

*— End of Report —*

### Appendix D — Hydraulic and Flow Data Summary

**D.1 Rainfall and Inflow Profile, March 14–16, 2027**

| Interval | Rainfall (in) | Peak Influent Flow (MGD) | Available Firm Pumping Capacity (MGD) |
|---|---|---|---|
| Mar 14, 8:00 a.m. – 4:00 p.m. | 1.4 | 41.2 | 34.0 |
| Mar 14, 4:00 p.m. – 9:52 p.m. | 1.1 | 48.6 | 34.0 |
| Mar 14, 9:52 p.m. – Mar 15, 4:10 a.m. | 0.6 | 51.3 | 26.5 (pump 2 offline) |
| Mar 15, 4:22 a.m. – 2:00 p.m. | — | 49.8 | 19.0 (pumps 2 and 4 offline) |
| Mar 15, 2:00 p.m. – Mar 16, 11:05 p.m. | — | Receding, 44.1 → 17.8 | 19.0 |

Storm total: 3.1 inches over 14 hours. Peak hourly intensity 0.41 inches (Mar 14, 7:00–8:00 p.m.). Collection system inflow lagged rainfall by approximately three to five hours, sustaining above-capacity flows through March 16 evening and extending the bypass well beyond the end of precipitation.

**D.2 Wet Well Level Reconstruction (SCADA Historian)**

| Time (Mar 14–15) | Level (ft above pump floor) | Condition |
|---|---|---|
| 9:52 p.m. | 8.2 | Pump 2 trips; normal operating band (6–9 ft) |
| 11:30 p.m. | 11.6 | High-level alarm setpoint (11.5 ft) crossed — no annunciation (suppressed) |
| 1:00 a.m. | 14.9 | High-high setpoint (14.5 ft) crossed — no annunciation (same suppression group) |
| 3:40 a.m. | 18.3 | Discovered on rounds; 1.2 ft below overflow elevation |
| 4:22 a.m. | 19.1 | Post pump 4 dead-head; 0.4 ft below overflow elevation |
| 6:05 a.m. | 19.4 | Bypass declared at overflow elevation (19.5 ft) |

A material finding of this reconstruction: the high-high alarm point was suppressed within the same February 3 test group as the high alarm, eliminating the intended second annunciation barrier. This was not known to the analysis team until historian review and has been incorporated into Action 1's completed audit scope.

**D.3 Bypass Discharge Accounting**

| Period | Duration | Metered Discharge (MG) |
|---|---|---|
| Mar 15, 6:05 a.m. – 6:00 p.m. | 11.9 hr | 4.8 |
| Mar 15, 6:00 p.m. – Mar 16, 6:00 a.m. | 12.0 hr | 3.9 |
| Mar 16, 6:00 a.m. – 11:05 p.m. | 17.1 hr | 2.7 |
| **Total** | **41.0 hr** | **11.4** |

Discharge received screening (partial, through blinded/recovering bar screen 2) and no biological or disinfection treatment. Sampling results (fecal coliform, BOD₅, TSS, ammonia) are on file with MassDEP under the March 15–19 sampling plan and are excluded here pending enforcement resolution.

---

### Appendix E — Completed Suppressed-Point Audit Results (Action 1)

The April 3 audit (Action 1) examined 2,847 configured SCADA points. Findings:

| Category | Count | Disposition |
|---|---|---|
| Points in suppressed/silenced state | 13 | 11 restored; 2 documented as permanently retired instruments, removed from database |
| Points in forced/override state | 4 | 3 released; 1 documented with authorized temporary force (chlorine analyzer, calibration in progress, expiration set) |
| Points with alarm setpoints deviating from design basis | 27 | Referred to alarm rationalization effort (Action 5) |
| Points routing to inactive or individual mailboxes | 61 | Rerouted to role-based lists (Action 3, partial early completion) |

Of the 11 restored suppressed points, two were assessed as safety- or compliance-significant beyond the wet well pair: the headworks combustible gas high alarm (suppressed since a September 2026 sensor replacement) and the effluent chlorine residual low alarm (suppressed during the same February 3 contractor test). Neither caused harm during their suppression periods; both represented live regulatory and safety exposure. These findings materially reinforce the root cause determination in Section 4.2: the March 14 suppression was not an isolated lapse but an instance of a systemic condition.

---

### Appendix F — Corrective Action Register Detail and Verification Criteria

Each action in Section 7 closes only upon documented verification. Closure evidence requirements:

| # | Verification Evidence Required for Closure |
|---|---|
| 1 | Audit report with point-by-point disposition (filed April 3, 2027) — **Closed** |
| 2 | Signed procedure; first three suppression MOC records demonstrating use; training sign-off sheet, all shifts |
| 3 | Screenshot/export of role-based distribution configuration; revised HR offboarding checklist; test of one simulated departure |
| 4 | Console dashboard live; 30 consecutive days of turnover reports showing suppressed-point line item |
| 5 | Alarm philosophy document Board-accepted; rationalization worksheets for headworks/influent points; rate-of-change alarm functional test record |
| 6 | Revised procedures issued; first quarterly valve exercise executed under new procedure with dual sign-off |
| 7 | Checklists posted at equipment and in SCADA; one witnessed standby start using checklist per shift |
| 8 | Trip settings configured and documented; witnessed functional test of dead-head trip on each pump |
| 9 | Interim: 12 monthly walkdown records; final: commissioning report for position indication with SCADA display verification |
| 10 | First three monthly test cycles completed with logged results |
| 11 | Protocol issued; console card posted; tabletop walkthrough with each shift's senior operator |
| 12 | On-call schedule published; first drill after-action report showing notification initiated within 30 minutes of simulated awareness |
| 13 | Protocol issued; acknowledgment from all five town administrators; first drill or actual use meeting 4-hour standard |
| 14 | CMMS criticality codes populated ≥95% of assets; escalation rule demonstrated on test work order; first monthly aged-backlog review minutes |
| 15 | VFD commissioning record; drive condition assessment report with prioritized replacement schedule |
| 16 | Board-adopted policy; FY28 budget package showing risk assessments attached to any deferral of criticality-coded work |
| 17 | Board-accepted plan; tabletop exercise after-action report; quarterly call-list verification log initiated |
| 18 | Plan delivered to Board; first quarterly vacancy risk report; documented recruitment actions (postings, program agreements) |

**Escalation rule:** any action forecast to miss its due date must be reported by its owner to the Executive Director at least 14 days before the due date with a recovery plan; a second slip on the same action escalates to the Board's Operations Committee.

---

### Appendix G — Glossary

| Term | Definition |
|---|---|
| **Bypass** | Intentional diversion of wastewater around one or more treatment processes, resulting in discharge that does not receive full permitted treatment. |
| **Blinding** | Obstruction of a bar screen's openings by accumulated debris, restricting flow through the headworks. |
| **CMMS** | Computerized Maintenance Management System; the Authority's work order and asset database. |
| **Dead-heading** | Operating a pump against a closed discharge path, producing no flow; rapidly damages impellers, seals, and casings through recirculation heating and vibration. |
| **Firm capacity** | Pumping capacity available with the largest single unit out of service; the design basis for reliable operation. |
| **Headworks** | The plant's first treatment stage: influent pumping, screening, and grit removal. |
| **MGD** | Million gallons per day. |
| **MOC** | Management of change; a formal process for authorizing, documenting, and reversing temporary or permanent modifications. |
| **NPDES** | National Pollutant Discharge Elimination System; the federal permit program governing the Authority's discharge, administered in Massachusetts jointly with MassDEP. |
| **Point (SCADA)** | A single monitored or controlled parameter in the control system (e.g., a level reading or alarm). |
| **SCADA** | Supervisory Control and Data Acquisition; the plant's monitoring and control system. |
| **Suppressed/silenced point** | A SCADA point configured not to annunciate alarms, typically for testing or maintenance. |
| **VFD** | Variable frequency drive; the electronic controller regulating a pump motor's speed. |
| **Wet well** | The influent collection basin from which raw wastewater is pumped into the treatment train. |

---

### Appendix H — Acknowledgments and Sign-Off

The analysis team thanks the on-shift operations crew of March 14–15 for their candor in interviews conducted under difficult circumstances, the maintenance crew for Sunday emergency mobilization, and MassDEP regional staff for cooperative coordination during sampling and closure activities. The willingness of staff at every level to describe events plainly — including their own decisions — made the systemic findings of this report possible and reflects the just culture this Authority intends to strengthen.

| Role | Name | Signature | Date |
|---|---|---|---|
| Executive Director | Alonzo Ferreira | *(signed)* | April 24, 2027 |
| Director of Operations | Kathleen Ng | *(signed)* | April 24, 2027 |
| Chief Plant Operator | Dmitri Sokolov | *(signed)* | April 23, 2027 |
| Maintenance Supervisor | Hollis Pruitt | *(signed)* | April 23, 2027 |
| Compliance Manager | Rochelle Grantham | *(signed)* | April 23, 2027 |
| Board Operations Committee Chair | *(accepted at April 28, 2027 meeting)* | *(signed)* | April 28, 2027 |

**Revision History**

| Rev | Date | Description |
|---|---|---|
| 0.1 | April 10, 2027 | Initial draft; timeline and impact sections circulated for factual review |
| 0.2 | April 17, 2027 | Incorporated interview corrections; added Appendix E audit results |
| 1.0 | April 24, 2027 | Final; approved for distribution |
| — | Quarterly | Corrective action status updates to be appended per Appendix C until closure |

**Next scheduled update:** July 31, 2027 (Q2 corrective action status appendix).

*— End of Document —*

---

## Quarterly Update Appendix I — Corrective Action Status Report, Q2 2027

| | |
|---|---|
| **Appended to** | QRWPCA-2027-003 Final Postmortem, Rev 1.0 |
| **Reporting Period** | April 25 – July 31, 2027 |
| **Prepared By** | Alonzo Ferreira, Executive Director |
| **Reviewed By** | Board Operations Committee, July 28, 2027 meeting |
| **Appendix Status** | Accepted; appended per Appendix C revision protocol |

### I.1 Summary of Status

Of 18 corrective actions, **9 are closed, 6 are on track, 2 are at risk, and 1 has slipped with an approved recovery plan.** No action is unaddressed. Two interim controls (locked-open valve administrative control; two-operator overnight storm staffing) remain in effect and were exercised during actual wet weather on June 19–20 (see Section I.4).

| Status | Count | Actions |
|---|---|---|
| Closed | 9 | 1, 2, 3, 6, 7, 11, 12, 13, 18 |
| On track | 6 | 4, 5, 10, 14, 16, 17 |
| At risk | 2 | 8, 15 (VFD portion) |
| Slipped — recovery plan approved | 1 | 9 (final engineering portion) |

### I.2 Action-by-Action Status

**Action 1 — SCADA suppressed-point audit.** *Closed April 3, 2027* (reported in Rev 1.0). A recurring monthly mini-audit has been voluntarily added by the Chief Plant Operator; June and July audits found zero unauthorized suppressed points.

**Action 2 — Alarm suppression MOC procedure.** *Closed May 27, 2027.* Procedure OPS-114 issued; all-shift training completed June 5. Four suppression MOCs have been executed under the procedure to date, all restored on or before expiration with dual verification. Closure evidence on file.

**Action 3 — Role-based report distribution and offboarding checklist.** *Closed June 10, 2027.* All 61 identified reports rerouted; HR offboarding checklist revised; simulated-departure test conducted June 9 confirmed no orphaned distributions.

**Action 4 — Suppressed-point visibility on turnover and dashboard.** *On track.* Dashboard element live since June 22; turnover report line item in use since June 24. Closure requires 30 consecutive days of turnover records — expected closure August 24, 2027.

**Action 5 — Alarm philosophy and headworks rationalization.** *On track.* Philosophy document in second draft; consultant workshops for headworks rationalization held July 14–16. The wet well rate-of-change alarm was **implemented early on May 20** and annunciated correctly during the June 19 storm (Section I.4). Full closure remains forecast for September 25, 2027.

**Action 6 — Return-to-service lineup verification.** *Closed May 14, 2027.* All valve exercise and isolation procedures revised. The Q2 valve exercise (June 3–5) was executed under the new procedure with dual sign-off on 34 valve restorations; zero discrepancies at the subsequent verification walkdown.

**Action 7 — Standby pump pre-start checklists.** *Closed May 13, 2027.* Checklists posted at equipment and embedded as a mandatory SCADA confirmation dialog. Witnessed starts completed on all four shifts by May 30.

**Action 8 — Dead-head protection on all pumps.** *At risk.* Protection configured and tested on influent pumps 1, 3, and 4. Pump 2 configuration is dependent on the delayed VFD replacement (Action 15), as trip logic resides in the new drive. Owner (H. Pruitt) has proposed an interim relay-based low-flow trip on pump 2, to be installed by August 21 pending parts. Revised full-closure forecast: within 30 days of VFD commissioning.

**Action 9 — Remote valve position indication.** *Final portion slipped; recovery plan approved.* Interim control (locked-open administrative status, monthly verified walkdowns) has operated without exception — four monthly walkdown records on file, zero discrepancies. Engineering design for position indication was delayed by instrument vendor lead times (26 weeks quoted vs. 12 assumed). Recovery plan approved by the Executive Director July 10: limit switches ordered July 12; revised installation completion **February 25, 2028**. Interim control continues until commissioning. Second slip escalates to the Operations Committee per Appendix F.

**Action 10 — Monthly standby functional test program.** *On track.* Program launched June; June and July cycles complete. The June test cycle identified a degraded check valve on influent pump 3 — repaired within nine days under the new criticality escalation rule (Action 14), a direct demonstration of intended program value. Closure upon completion of the August cycle (third consecutive), expected September 4, 2027.

**Action 11 — Notification protocol rewrite and console card.** *Closed May 7, 2027.* Protocol COMP-201 issued; trigger redefined to awareness of actual or imminent noncompliant discharge; notification authority delegated to on-shift senior operators; quick-reference card posted and walked through with each shift's senior operator by May 21.

**Action 12 — Compliance on-call rotation and drills.** *Closed June 11, 2027 (rotation); first drill complete July 9.* Drill result: simulated awareness to completed notification in **22 minutes** (standard: 30). Two refinement items from the drill after-action (script clarity on discharge volume estimation; backup contact for state after-hours line) were closed July 18. Quarterly drills continue as a standing program.

**Action 13 — Member town communication protocol.** *Closed May 20, 2027.* Protocol issued; written acknowledgments received from all five town administrators by June 2. Protocol was activated in earnest during the June 19–20 storm: precautionary notifications reached all five towns within 1 hour 40 minutes of the Authority's internal storm declaration — well inside the 4-hour standard (Section I.4).

**Action 14 — CMMS criticality coding and escalation.** *On track.* Criticality codes populated for 91% of assets as of July 25 (target ≥95%); escalation rule live since June 15 and demonstrated on both a test work order and the live pump 3 check valve order (Action 10). First two monthly aged-backlog reviews held June 26 and July 24; redundancy-critical backlog reduced from 14 open orders to 5. Closure expected August 28, 2027 as scheduled.

**Action 15 — Pump 2 VFD replacement and drive assessments.** *VFD portion at risk; assessment portion on track.* Emergency procurement executed May 5; manufacturer shipment slipped from June 30 to August 18 due to component availability. Installation contractor is mobilized for the week of August 24; revised commissioning forecast **September 12, 2027** (44 days past the July 31 due date). Recovery plan approved; pump 2 remains operable on the existing drive with enhanced weekly thermographic and fault-log monitoring instituted May 8 as a compensating measure. Condition assessment of remaining drives is 60% complete and on schedule for September 30.

**Action 16 — Capital deferral risk-review policy.** *On track.* Draft policy presented to the Operations Committee June 23; Board adoption scheduled September 14, ahead of FY28 budget deliberations. The FY28 capital request package is being prepared with risk assessments attached to all criticality-coded items, including three items proposed for deferral.

**Action 17 — Wet weather operating plan rewrite.** *On track.* Rewrite is 70% complete. Staffing surge triggers, storm rounds frequency, and notification triggers are drafted and were **exercised in interim form during the June 19–20 storm** with corrective observations folded into the draft. Call lists verified April 30 and July 15 (quarterly cadence established). Tabletop exercise scheduled October 21; Board acceptance forecast on schedule for October 30, 2027.

**Action 18 — Operator staffing plan.** *Closed July 22, 2027 (plan delivery).* Plan delivered to the Board July 22 and accepted. Contents: wage benchmarking against eight comparable authorities (QRWPCA found 7–12% below median for licensed grades); Board-approved wage adjustment effective September 1; operator-in-training agreements signed with two area vocational programs (first cohort of four begins September 2027); certification incentive schedule adopted. **Vacancy status: 9 vacancies at incident date → 6 as of July 31** (two external hires started June; one internal promotion backfilled externally). First quarterly vacancy risk report delivered with the plan. Ongoing recruitment execution transfers to standing quarterly Board reporting.

### I.3 At-Risk and Slipped Action Recovery Summary

| # | Original Due | Revised Forecast | Compensating Measure in Effect | Escalation Status |
|---|---|---|---|---|
| 8 (pump 2 portion) | July 31, 2027 | ~Oct 12, 2027 | Interim relay-based low-flow trip by Aug 21; operator flow-verification step in start checklist (Action 7) | ED notified June 29; recovery plan approved |
| 9 (final portion) | Dec 17, 2027 | Feb 25, 2028 | Locked-open control + monthly verified walkdowns (zero discrepancies to date) | ED notified July 2; recovery plan approved July 10 |
| 15 (VFD portion) | July 31, 2027 | Sept 12, 2027 | Weekly thermography and fault-log review on existing drive since May 8 | ED notified June 12; Committee briefed July 28 |

### I.4 Real-World Validation: June 19–20, 2027 Storm

A storm delivering 2.2 inches in 11 hours on June 19–20 provided an unplanned but instructive test of implemented controls. Outcomes:

- **Staffing surge trigger (interim, Action 17):** National Weather Service flood watch issued 2:40 p.m. June 19; two-operator overnight coverage and a maintenance standby were in place by shift change. Peak influent flow reached 44.7 MGD.
- **Rate-of-change alarm (Action 5, early implementation):** At 11:56 p.m. June 19, influent pump 1 tripped on a motor overtemperature. The wet well rate-of-change alarm annunciated **at 12:03 a.m., seven minutes later** — against the 5-hour-48-minute detection gap of March 14. The high wet well alarm (restored, Action 1) annunciated independently at 12:41 a.m. as level crossed setpoint.
- **Standby start under checklist (Action 7):** Standby pump 4 was started at 12:19 a.m. using the pre-start checklist; discharge valve lineup confirmed open (locked-open control, Action 9 interim); discharge flow verified within 90 seconds of start. Firm capacity restored. Pump 1 was reset and returned to service at 6:50 a.m. after cooldown and inspection.
- **Notification posture (Actions 11–13):** On-shift senior operator initiated the compliance on-call at 12:08 a.m. per the awareness-based trigger. No bypass occurred and no noncompliant discharge condition arose; the notification stood down at 1:15 a.m. Member towns received precautionary notice per Action 13. **No permit exceedance occurred.**
- **Observations for improvement:** (1) the rate-of-change alarm's initial setpoint produced two nuisance annunciations earlier that evening during normal storm ramp — setpoint refined June 24; (2) the maintenance standby's callout acknowledgment took 34 minutes against a 20-minute draft standard — paging redundancy added to the wet weather plan draft.

The Committee noted that the June event replicated the initiating condition of the March incident — an influent pump trip during a significant storm at night — and that the reconstructed defense layers functioned as designed. This does not close the effectiveness review requirement (Appendix C; March 2028 full-scale exercise remains scheduled) but constitutes substantial interim evidence of corrective action effectiveness.

### I.5 Regulatory and Financial Status Update

- **Enforcement:** Consent negotiations with MassDEP commenced June 8. The Authority's corrective action record, including this appendix, has been provided to the Department. Penalty resolution remains open; the Department has indicated the demonstrated corrective program will be considered under its penalty mitigation policy. No figure is final as of this report.
- **Costs incurred to date (event and corrective, through July 31):** pump 4 impeller replacement $91,240 (final, vs. $87,000 estimate); emergency contractor and overtime $58,875 (final, vs. $64,000 estimate); VFD replacement committed $122,600; corrective action program expenditures (consultant, instrumentation, limit switches, training backfill) $147,300 committed.
- **Insurance:** Property claim for pump 4 damage settled July 14 at $63,500 net of deductible.

### I.6 Next Update

Q3 corrective action status appendix due **October 30, 2027**, to include: closure verification for Actions 4, 5, 10, 14, and 16; VFD commissioning report (Action 15); wet weather plan Board acceptance and tabletop exercise after-action (Action 17); and updated enforcement status.

| Accepted for Appending | |
|---|---|
| Alonzo Ferreira, Executive Director | *(signed)* July 31, 2027 |
| Board Operations Committee Chair | *(signed)* July 28, 2027 |

*— End of Appendix I —*
