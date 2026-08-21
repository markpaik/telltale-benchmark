# Incident Postmortem — March 14, 2027 Wet Weather Bypass, Outfall 002

**Quinsigamond Regional Water Pollution Control Authority (QRWPCA)**
**Blackstone River Water Reclamation Facility**

| Field | Entry |
|---|---|
| Incident ID | INC-2027-004 |
| Classification | Category 1 — Permit-limited discharge of partially treated wastewater |
| Event date | March 13–15, 2027 (event designated by the March 14 bypass declaration) |
| Document status | Final, Rev. 2 |
| Issued | April 22, 2027 |
| Prepared by | Incident Review Panel (see §2.2) |
| Approved by | Alonzo Ferreira, Executive Director |
| Distribution | Authority Board; five member town administrators; MassDEP Central Regional Office (courtesy copy); all QRWPCA staff |
| Review method | Blameless systems analysis (see §2.1) |

---

## 1. Summary

Between 9:52 p.m. Saturday, March 13, 2027, and 11:05 p.m. Monday, March 15, 2027, the Blackstone River Water Reclamation Facility lost the majority of its influent pumping capacity during a 3.1-inch, 14-hour rainfall event and discharged 11.4 million gallons of screened but otherwise partially treated wastewater to the Blackstone River through Outfall 002. The bypass ran 41 hours. It is prohibited by Part I.B.4 of the facility's NPDES permit except under conditions of unavoidable equipment failure that could not have been prevented by adequate maintenance or by installation of adequate backup equipment — an exception the Authority does not expect to sustain on these facts, and does not attempt to sustain in this document.

The sequence began with a variable frequency drive fault that took influent pump 2 out of service. That single failure was survivable; the facility ran on three of four pumps for four hours without incident. What made it consequential was that the high wet well level alarm — the plant's only automated indication that pumping capacity had fallen behind inflow — had been placed in an inhibit state during a contractor point-to-point test on February 3 and never returned to service. For 39 days the plant's daily Silenced and Inhibited Point Report identified the inhibit correctly. The report was addressed to a distribution list whose only member was the mailbox of a supervisor who had retired the previous November.

The result was a 5-hour, 48-minute detection gap. By the time the Chief Plant Operator found the condition on physical rounds at 3:40 a.m., the wet well had surcharged, the influent channel was at weir elevation, and the crew had roughly twenty minutes of margin. In that compressed window the response made two decisions that made things worse: it attributed the drive fault to a utility voltage dip logged four minutes before the trip, which closed off diagnosis of the actual failure; and it started standby pump 4 against a discharge valve that had been left closed after a January valve exercise, destroying the impeller and reducing firm pumping capacity from 57 MGD to 19 MGD against an influent flow then peaking near 61 MGD. Bar screen 1 had been out of service on a work order open 94 days; when the surviving screen blinded at 5:20 a.m., the last hydraulic path was gone. The bypass was declared at 6:05 a.m.

Verbal notice to the Commonwealth was given at 6:40 a.m., one hour outside the two-hour window that began at the 3:40 a.m. discovery. The state issued a Notice of Noncompliance on March 27 carrying $312,000 in penalty exposure. A downstream community water system ran on backup supply for four days. Nine miles of river access were posted closed for nine days.

**The Panel's conclusion is that this was not an equipment failure that overwhelmed a sound system. It was a system that had quietly lost every one of its layers of protection over the preceding fourteen months, in each case through a normal and individually defensible administrative act — a maintenance test, a retirement, a budget rebalancing, a parts lead time, a routine valve exercise — with no mechanism anywhere in the organization capable of noticing that the layers were gone.** The people on shift that night were operating a plant they reasonably believed had protections it did not have.

---

## 2. Scope and Method

### 2.1 Blameless protocol

This review was conducted under the Authority's Learning Review Protocol, adopted 2024. Its terms:

- Statements made to the Panel are not admissible in any disciplinary proceeding and were not shared with supervisors in an evaluative capacity.
- The Panel is directed to identify the conditions under which the observed decisions were locally rational — that is, why each action made sense to the person taking it, given what they knew at the time.
- Findings name systems, procedures, and decisions. Where individuals appear, it is because they held a role and made a decision that the system will need to support differently in future. No finding in this document should be read as a determination of individual fault, and none is intended.
- Action items are assigned to named owners because accountability for repair requires a name. That is a forward-looking assignment, not a backward-looking one.

### 2.2 Panel composition

Kathleen Ng, Director of Operations (chair); Rochelle Grantham, Compliance Manager; Hollis Pruitt, Maintenance Supervisor; Dmitri Sokolov, Chief Plant Operator; Priya Raghunathan, Director of Engineering; one operator representative selected by the bargaining unit; and an external facilitator (regional wastewater consultant, retained to conduct interviews and draft findings independent of Authority management).

### 2.3 Evidence base

SCADA historian extraction (10-second resolution, March 12–17); alarm and event journal; the February 3 contractor point test package and punch list; 39 archived Silenced and Inhibited Point Reports; CMMS work order history for FY25–FY27; FY25–FY27 capital budget documents and Board minutes; the January 21 valve exercise PM record; shift logs and rounds sheets; the 2016 Wet Weather Operating Plan; permit Part I and Part II; 22 interviews conducted March 19–April 6; laboratory results and bypass sampling records; utility (National Grid) power quality data for the Millbury feeder; NOAA rainfall data from the Worcester Regional Airport and the plant's own tipping bucket.

### 2.4 Facility context

The Authority treats an average of 34 MGD for five member towns in Worcester County. Design average flow is 36 MGD; permitted peak hydraulic capacity through secondary treatment is 68 MGD. Influent pumping consists of four constant-speed-equivalent pumps on variable frequency drives, each rated 19 MGD, giving 76 MGD installed and 57 MGD firm capacity (largest unit out of service). Preliminary treatment is two mechanically raked bar screens in parallel, each sized for full peak flow with the other out of service. Staffing is 128 budgeted positions with 9 of 34 licensed operator posts vacant, a 26.5 percent operator vacancy rate that has persisted above 20 percent since June 2025.

---

## 3. Impact

### 3.1 Environmental and regulatory

| Measure | Value |
|---|---|
| Bypass duration | 41 h 0 min (06:05 Mar 14 – 23:05 Mar 15) |
| Volume discharged | 11.4 million gallons |
| Average bypass rate | 6.7 MGD |
| Peak bypass rate | 14.2 MGD (07:20 Mar 14) |
| Treatment received | Coarse screening only (partial), grit removal degraded, no primary settling after 06:40, no secondary, no disinfection |
| Estimated excess BOD₅ load | ≈ 9,700 lb above permitted equivalent |
| Estimated excess TSS load | ≈ 11,600 lb above permitted equivalent |
| Estimated excess total nitrogen | ≈ 1,900 lb |
| Estimated excess total phosphorus | ≈ 290 lb |
| Additional permit exceedance | Effluent TSS daily maximum, March 16 (35 mg/L against 30 mg/L limit), attributable to secondary system upset |
| Notice of Noncompliance | Issued March 27, 2027 |
| Stated penalty exposure | $312,000 |

### 3.2 Public and downstream

| Measure | Value |
|---|---|
| Downstream community water system on backup supply | 4 days (Mar 14–17) |
| River access posted closed | 9 days (Mar 14–22), approximately 9 river miles |
| Public boat launches closed | 3 |
| Member towns issuing public advisories | 5 of 5 |
| Recreational events cancelled or relocated | 2 |
| Fish kill observed | None reported |
| Injuries to staff or contractors | None |

### 3.3 Facility and financial

| Measure | Value |
|---|---|
| Firm pumping capacity, normal | 57 MGD |
| Firm pumping capacity, 04:14–18:00 Mar 14 | 19 MGD (−67%) |
| Peak influent flow observed | 61.4 MGD (03:10 Mar 14) |
| Detection gap (trip to discovery) | 5 h 48 min |
| Diagnostic gap (discovery to correct root cause of VFD fault) | 29 h 20 min |
| Regulatory notification delay | 60 min past window |
| Pump 4 repair (impeller, wear rings, seal, shaft) | $148,000 |
| Emergency VFD replacement, pump 2 | $96,000 |
| Temporary bypass pumping rental (12 MGD, 9 days) | $84,600 |
| Valve and piping rework | $26,500 |
| Overtime, 1,410 hours | $71,400 |
| Sampling, laboratory, and river monitoring | $18,900 |
| **Direct response cost subtotal** | **$445,400** |
| Direct cost plus stated penalty exposure | $757,400 |
| Secondary sludge inventory lost | 22% |
| Days to restore full secondary nitrification | 6 |

### 3.4 Latent-condition metrics (measured after the fact)

| Measure | Value |
|---|---|
| Days the high wet well alarm was inhibited | 39 |
| Silenced/Inhibited Point Reports generated and unread | 39 |
| Other SCADA points found inhibited during post-incident audit | 4 (2 safety-related) |
| Days pump 4 discharge valve was closed and believed open | 51 |
| Age of bar screen 1 work order at time of event | 94 days |
| Open work orders >90 days on assets designated critical | 41 |
| Fiscal years the influent VFD replacement was deferred | 2 (FY26, FY27) |
| Age of the Wet Weather Operating Plan | 11 years |
| Operators on shift, 20:15 Mar 13 – 07:00 Mar 14 | 3 (plan assumes 5 for a declared wet weather watch) |
| Alarms and events presented in the 90 min after the trip | 347 |

---

## 4. Timeline

All times Eastern Daylight Time. Times marked (H) are from the SCADA historian; (L) from shift logs; (I) reconstructed from interviews and marked approximate.

### 4.1 Latent conditions (chronological)

| Date | Event |
|---|---|
| Jun 2024 | FY25 capital budget adopts $410,000 for replacement of the four influent pump VFDs (installed 2009, manufacturer support ended 2023). |
| Sep 2025 | FY26 rebalancing defers the VFD line item to fund an emergency digester cover repair. No risk-transfer entry is made; the Authority has no capital deferral risk register. |
| Jun 2026 | FY27 budget defers the VFD line a second time in favor of headworks odor control, a project with member town political salience. Deferral recorded as a scheduling decision. |
| Nov 6, 2026 | Supervisor of Instrumentation and Controls retires after 24 years. Position not backfilled (part of the 9 vacancies). Ownership of the SCADA alarm configuration and of the daily Silenced/Inhibited Point Report is not formally reassigned. The email distribution list `SCADA-ALARMS` retains his mailbox as its sole member; the mailbox remains active per the Authority's 12-month retention policy and silently accumulates mail. |
| Dec 10, 2026 | Work order 26-1841 opened: bar screen 1 rake drive motor and gearbox failure. Replacement gearbox quoted at 12 weeks. WO aging generates no escalation because the CMMS escalation rule applies only to work orders flagged "Priority 1," and redundant equipment is auto-classified "Priority 2." |
| Jan 21, 2027 | Quarterly valve exercise PM completed on influent pump discharge valves V-1D through V-4D. The PM task text reads "cycle valve full closed to full open, verify travel." It contains no final-position verification step and no independent second check. V-4D is left closed. Pump 4 is the designated standby and is not started, so nothing reveals the condition. |
| Feb 3, 2027 | Contractor performs point-to-point verification of 61 SCADA points following a controller firmware upgrade. Points are placed in inhibit to prevent nuisance annunciation. Sixty are restored at end of work. LIT-101 high and high-high wet well level alarms are not restored. The contractor's punch list, submitted Feb 6, lists "confirm alarm enables at LIT-101" as an open item; the punch list was received by the retired supervisor's distribution list address. |
| Feb 4 – Mar 13 | The nightly Silenced and Inhibited Point Report correctly lists LIT-101 HI and HI-HI as inhibited, 39 consecutive nights. No human being reads it. |
| Mar 12, 09:00 | National Weather Service issues a flood watch for Worcester County for the period beginning Saturday evening. |
| Mar 13, 14:00 | Day shift reviews the forecast. Under the 2016 Wet Weather Operating Plan, a "wet weather watch" is discretionary below a 2-inch forecast; the forecast is 1.5–2.5 inches. No watch is declared. Standard three-operator night crew is scheduled. |

### 4.2 Incident and detection

| Time | Event |
|---|---|
| **Mar 13** | |
| 19:40 (H) | Rain begins. Plant tipping bucket records first tip. |
| 20:15 (L) | Shift turnover. Three operators on shift; Sokolov on call from home. Turnover notes rain and a rising flow trend. |
| 21:48 (H) | Utility voltage sag on the Millbury feeder: 0.42 seconds at 79% nominal, logged by the plant power monitor. Two lighting contactors drop and reclose. |
| 21:52:11 (H) | **Influent pump 2 VFD trips.** Drive fault code F-072. Pump 2 stops. |
| 21:52:14 (H) | Event journal records "PMP-102 NOT RUNNING — status change," priority 3 (log only, no audible). Pump 2 is shown gray on the headworks graphic. |
| 21:52–23:00 (H) | 347 alarms and events are presented in the alarm summary, predominantly rain-derived: manhole level highs across the collection system, three lift station high-wet-well alarms, CSO regulator level alarms, and grit conveyor jams. The pump 2 status change is one line among them. |
| 22:00–02:00 (H) | Pumps 1, 3, and 4 — correction: pumps 1, 3 in service, pump 4 is standby and does not auto-start. **Pump 4 auto-start on high level is armed but is enabled by the same LIT-101 HI alarm point that is inhibited; it therefore never calls.** Pumps 1 and 3 carry flow. Wet well level 6.8–9.1 ft, within normal band. Influent 34 → 51 MGD. |
| 02:10 (H) | Influent flow crosses 38 MGD, exceeding the two-pump capacity. Wet well level begins to climb at 0.9 ft/hr, then accelerating. |
| 02:34 (H) | Level reaches HI setpoint, 11.5 ft. **No annunciation. No pump 4 auto-call.** |
| 03:05 (H) | Level reaches HI-HI setpoint, 13.0 ft. **No annunciation.** |
| 03:10 (H) | Influent flow peaks at 61.4 MGD. |
| 03:38 (H) | Level 14.5 ft. Emergency overflow weir in Structure 3 is at 15.2 ft. |
| **03:40 (L)** | **Detection.** Sokolov, having come in at 03:15 on his own initiative because of the rain, is walking headworks rounds. He observes the wet well surcharged to within inches of the channel deck and pump 2 dark at the local panel. |

### 4.3 Response

| Time | Event |
|---|---|
| 03:44 (L) | Sokolov telephones Ng at home. Reports pump 2 down, wet well high, "the alarm never came in." |
| 03:47 (I) | Sokolov reads the drive fault at the local HMI and scrolls the plant power monitor. He sees the 21:48 voltage sag. **The times are four minutes apart; he concludes the sag tripped the drive.** This is a reasonable inference — the facility had experienced two prior sag-related drive trips in 2023 and 2024, both cleared by reset — and it establishes an expectation that a reset will restore the pump. |
| 03:49–03:58 (H) | Two reset attempts. The drive faults again within 8 seconds each time. Sokolov attributes the failure to reset to a residual bus condition and elects not to spend further time on it. **No one opens the drive enclosure or retrieves the fault code definition, which would have shown a hardware fault, not an undervoltage fault. Undervoltage on this drive family is F-011; F-072 is a phase-loss/module fault.** |
| 04:02 (L) | Ng, on the phone, concurs with starting standby pump 4. Both parties understand pump 4 to be available: it is shown "READY" on the graphic, which reflects motor and drive status only and carries no valve position input. |
| 04:05 (I) | Operator proceeds to start pump 4. There is no valve lineup check step in the standby start procedure and no valve position transmitter on V-4D. The valve is a manual gear-operated butterfly valve whose position indicator is at the top of a 14-foot stem in the pump gallery. |
| 04:10:22 (H) | **Pump 4 started against closed discharge valve V-4D.** Motor amps 62% of full load, discharge pressure rises to 41 psi against a 22 psi normal, vibration channel goes off-scale at 0.9 in/s. |
| 04:14:40 (H) | Pump 4 secured after 4 min 18 s. Seal flush temperature high. |
| 04:22 (L) | Restart attempted; pump will not build pressure. Water is observed in the pump pit. Pump 4 is declared out of service. **Firm capacity is now 19 MGD.** |
| 04:25 (L) | Ng arrives on site. |
| 04:28 (L) | Pruitt called out; arrives 05:05. |
| 04:35 (I) | Ng directs that all screening and grit be maximized and that primary effluent be routed for maximum surface loading. Collection system storage assessment begins; three upstream regulators are already in overflow. |
| 04:50 (L) | Ng requests that Grantham be called. Grantham is reached at 05:02 and begins driving to the plant, arriving 05:38. The notification decision is not made by phone en route; the Panel finds no procedure directing that it should have been. |
| 05:20 (H) | **Bar screen 2 blinds.** Differential level across the screen reaches 3.1 ft. With bar screen 1 out of service on WO 26-1841, there is no parallel path. Headworks channel surcharges to the deck. Grit channel overtops. |
| 05:35 (L) | Ng convenes Sokolov, Pruitt, and the shift on the headworks deck. Options identified: (a) continue and accept flooding of the headworks building and probable loss of the electrical room at elevation 216; (b) declare a bypass at Structure 3. |
| 05:50 (L) | Ferreira notified by telephone. |
| **06:05 (H/L)** | **Ng declares a bypass** and directs the Structure 3 gate open to Outfall 002. Gate confirmed open at 06:07. Wet well level begins to fall at 06:19. |
| 06:12 (L) | First bypass composite sample initiated at the Outfall 002 sample point. |
| 06:20 (I) | Grantham begins preparing the verbal notification, locating the after-hours number in the 2016 plan appendix. The number listed is the MassDEP Central Regional Office main line, which is not staffed at 06:20. The correct 24-hour Emergency Response line is obtained by calling the Massachusetts State Police. |
| **06:40 (L)** | **Verbal notification made to MassDEP Emergency Response.** Under Part II.D.1.e the two-hour clock began at 03:40, when the Authority first became aware of a condition likely to result in a bypass; notice was due 05:40. **Notice was 60 minutes late.** The Authority initially took the position that the clock began at 06:05; it has since withdrawn that position and treats 03:40 as the correct trigger for all internal purposes. |
| 06:52 (L) | Downstream community water system notified by direct call to its on-call operator. Intake is shifted to backup supply at 07:15. |
| 07:15–08:10 (L) | Boards of health for all five member towns notified. Two learn of the event first from MassDEP's own outreach at approximately 07:00. |
| 08:00 (L) | Emergency bypass pumping contractor contacted; 12 MGD of diesel-driven pumps ordered from Springfield. |
| 09:30 (L) | Pruitt's crew, tracing the pump 4 failure, finds V-4D in the closed position. This is the first moment anyone in the response understands why pump 4 failed. |
| 10:40 (L) | Pump 4 pulled. Three of five impeller vanes fractured; wear rings destroyed; shaft runout 0.021 in; mechanical seal failed. Repair estimated at 5 weeks. |
| **14:00 (L)** | **Valve arrangement rebuilt.** V-4D exercised and confirmed open with two-person verification; pump 4 isolated with a blind flange; discharge header cross-tie opened to allow pumps 1 and 3 to load the full header. Physical position tags applied to all four discharge valves. |
| 15:20 (L) | Manual raking rotation established on bar screen 2 with six staff on 20-minute cycles; screen differential falls to 1.4 ft. |
| 16:30 (L) | Ferreira briefs member town administrators by conference call. This is 10 h 25 min after the bypass began and after four of five towns had already been contacted by residents or press. |
| 18:00 (L) | Rental pumps online. Available capacity 50 MGD; firm capacity 31 MGD. |
| **Mar 15** | |
| 02:00 (H) | Influent falls below 50 MGD. |
| 09:00 (L) | Drive manufacturer's field service technician arrives. **Pump 2 VFD diagnosis: failed IGBT power module and DC bus capacitors degraded to 61% of rated capacitance, consistent with 18 years of thermal aging.** The 21:48 voltage sag was coincident, not causal. No spare module is stocked; none is available in New England. |
| 11:30 (L) | Decision to procure a complete replacement drive on emergency purchase. |
| 16:00 (L) | Secondary system assessed: 22% of MLSS inventory washed out; nitrification suppressed. |
| **23:05 (H/L)** | **Bypass gate closed. Bypass duration 41 h 0 min. Volume 11.4 MG.** All flow returned through preliminary, primary, secondary, and disinfection. |
| **Mar 16–22** | |
| Mar 16 | Effluent TSS daily maximum exceeded (35 mg/L). Bar screen 1 gearbox expedited; arrives Mar 24. |
| Mar 17 | Replacement VFD installed and commissioned; pump 2 returned to service. Downstream intake returns to primary supply. |
| Mar 18 | Five-day written notice filed with MassDEP (within requirement). |
| Mar 19 | Post-incident SCADA alarm audit begins; four additional inhibited points discovered. |
| Mar 20 | Full nitrification restored. |
| Mar 22 | River access postings lifted (day 9). |
| Mar 27 | Notice of Noncompliance issued; $312,000 penalty exposure stated. |
| Apr 18 | Pump 4 returned to service; firm capacity restored to 57 MGD. Rental pumps demobilized. |

---

## 5. Root Cause

### 5.1 Statement

**The Authority had no closed-loop control over the state of its protective functions.** Protections could be removed — by a maintenance action, a retirement, a budget decision, a parts delay, or a valve exercise — and the organization had no mechanism capable of detecting that they were gone. Every barrier that should have stopped this event had already been removed before the storm arrived, and the removals were invisible.

The proximate trigger, a VFD hardware failure on an 18-year-old drive during a 3.1-inch rain, is a foreseeable and routine event for a facility of this type. A plant with intact protections absorbs it. The March 14 bypass occurred because there were no intact protections.

### 5.2 Causal ladder

*Why was there a bypass?* Because influent pumping capacity fell to 19 MGD against 61 MGD of inflow, and the surviving bar screen blinded with no parallel path.

*Why did capacity fall to 19 MGD?* Because pump 2's drive had failed and pump 4 was destroyed on start against a closed discharge valve.

*Why was pump 4 started against a closed valve?* Because the standby start procedure contains no valve lineup verification, the SCADA "READY" indication does not include valve position, V-4D has no position transmitter, and the valve had been left closed by a January PM whose task text does not require final-position verification.

*Why was the crew starting a standby pump under emergency conditions at 4:10 a.m. instead of at 10:00 p.m.?* Because no one knew pump 2 had tripped for five hours and 48 minutes.

*Why did no one know?* Because the high wet well alarm was inhibited, its auto-start permissive with it, and the pump status change was a log-only event inside a 347-event storm alarm flood.

*Why was the alarm inhibited for 39 days?* Because a contractor test placed it in inhibit, the restoration was captured on a punch list and on 39 daily exception reports, and the recipient of both was a mailbox belonging to a person who had retired four months earlier.

*Why did no one notice a report going to a departed employee?* Because ownership of the SCADA alarm configuration was attached to a person, not to a role or a documented function; when the position went vacant amid a 26.5 percent operator vacancy rate, the function went vacant with it, and no offboarding process examined what the person had owned.

*Why did the failure of a single drive matter so much?* Because the replacement of all four influent VFDs had been funded in FY25 and deferred twice, without any process that registered the resulting increase in operational risk, and without a stocked spare module for a drive family the manufacturer had stopped supporting in 2023.

### 5.3 Counterfactual gates

Seven independent points at which the event would have been stopped or materially reduced. That all seven were open simultaneously is the finding.

| Gate | If it had held | Effect |
|---|---|---|
| 1. Alarm restoration verified Feb 3 | HI alarm annunciates 02:34; pump 4 auto-start calls at 11.5 ft | Event does not occur |
| 2. Inhibited-point report read by anyone, any of 39 days | Inhibit corrected before the storm | Event does not occur |
| 3. Valve exercise PM requires final-position verification | V-4D open; pump 4 starts normally at 04:10 | Capacity 38 MGD; bypass likely avoided or ≤4 hours |
| 4. Standby start procedure requires valve lineup check | Closed valve found at 04:06 | Pump 4 preserved |
| 5. Bar screen 1 WO escalated at 30 days | Parallel screen available at 05:20 | Bypass duration substantially reduced |
| 6. VFD replacement executed FY25 or FY26 | No drive failure | Event does not occur |
| 7. Wet weather watch declared for a 1.5–2.5 in forecast | 5 operators on shift; rounds at 22:00 | Detection gap ≈ 30 min, not 5 h 48 min |

---

## 6. Contributing Factors

### 6.1 Technical and design

**T-1. No independent high-level detection.** The wet well has one level transmitter (LIT-101) and no float switch, staff gauge with alarm, or ultrasonic backup. A single point of failure in instrumentation is also a single point of failure in detection. This is below current practice for a facility of this size.

**T-2. Auto-start permissive derived from an alarm point.** Pump 4's auto-start logic used the LIT-101 HI alarm bit rather than the raw level value. Inhibiting the alarm therefore disabled the standby pump call — an unintended coupling of an operator-notification function to a control function that no one at the facility knew existed. This is a design defect in the 2019 controls upgrade, not an operating error.

**T-3. No valve position feedback on influent discharge valves.** Four critical valves, all manually operated, all without position transmitters, all displayed to operators only as an implied condition of a pump "READY" status that does not consider them.

**T-4. Alarm system never rationalized.** The plant presents an average of 4,100 alarms per day, with rates exceeding 200 per 10 minutes during wet weather. This is roughly 20 times the EEMUA 191 guidance for a manageable rate. In a flood of that density, priority-3 events are functionally invisible, and priority-1 events are diluted. The alarm system does not distinguish between "the river is rising" and "the plant is failing."

**T-5. No spare for an unsupported drive.** The drive family lost manufacturer support in 2023. The Authority did not stock a spare power module or a complete spare drive, and had no documented decision accepting that risk.

### 6.2 Procedural

**P-1. The Wet Weather Operating Plan is 11 years old.** Issued 2016, it predates the 2019 controls upgrade, the current organization chart, the current staffing levels, the two-hour notification condition added at the 2021 permit reissuance, and the current outfall configuration. It lists a MassDEP phone number that no longer reaches a staffed desk after hours. Its wet weather watch trigger — a 2-inch forecast — was set when the plant had firm capacity to spare and no operator vacancies.

**P-2. Standby equipment start has no lineup verification.** No procedure, no checklist, no second person.

**P-3. Valve exercise PM lacks a restoration step.** The task verifies travel, not final position. There is no as-left position record and no tag system.

**P-4. Work order aging escalation excludes redundant assets.** Because bar screen 1 is redundant, its failure is Priority 2 and never escalates. The rule does not consider that redundancy that persists for 94 days is not redundancy; it is a single-train plant with a long-standing hole in it. Forty-one open work orders over 90 days on critical assets were found in the post-incident audit.

**P-5. No temporary-defeat register.** There is no log of protective functions temporarily disabled, no requirement to record the reason, the expected duration, the compensatory measure, or the person responsible for restoration.

**P-6. Notification is treated as a compliance task, not a response task.** The Compliance Manager was called after the bypass decision, not with it. There is no standing rule that the notification clock starts at the discovery of a condition likely to cause a bypass, and no one-page decision aid at the operator console stating the trigger, the number, and the required content.

### 6.3 Organizational

**O-1. Capital deferral without risk transfer.** The Authority defers capital work through an ordinary budget process that produces no record of what risk is being accepted, by whom, or for how long. The influent VFD line was deferred twice by decisions that no participant would characterize as unreasonable in isolation — a digester cover failure and a member-town odor complaint are both real. What was absent was any artifact that would have told the FY27 decision-makers that this was the third year of running unsupported drives on the plant's only wet weather defense.

**O-2. Function ownership attached to a person.** The Supervisor of Instrumentation and Controls owned the alarm configuration by long practice rather than by documented assignment. His departure removed the function silently. The Authority's offboarding checklist covers keys, credentials, and equipment; it does not ask what recurring reports, distribution lists, or unwritten responsibilities the departing person held.

**O-3. Vacancy rate has become structural.** Nine of 34 operator posts have been open for periods averaging 14 months. The organization has adapted to this by informally lowering thresholds — running three-operator nights, deferring rounds frequency, declaring fewer wet weather watches. These adaptations are invisible in any metric the Board sees. The night crew on March 13 was not understaffed by exception; it was understaffed by the current normal.

**O-4. No independent verification of contractor work on protective systems.** The February 3 contractor delivered a punch list identifying its own open item. No Authority employee was assigned to close it, and the acceptance of the work was administrative.

**O-5. External communication had no owner or trigger.** Member town notification depended on the Executive Director's judgment with no defined time standard. Ten and a half hours elapsed, during which residents and press became the primary information channel.

### 6.4 Cognitive and situational

**C-1. Anchoring on the voltage sag.** A logged power event four minutes before a drive trip, with two prior sag-related trips in facility memory, is a strong and locally rational hypothesis. It was wrong, and it foreclosed the diagnostic path within three minutes. The Panel notes that no job aid existed mapping fault codes to causes, and that the fault code definition was available only in a manual stored off-site. **The system gave the operator a plausible wrong answer faster than it gave him the right one.**

**C-2. Time compression.** From discovery to bypass declaration was 2 h 25 min, of which the truly decisive window — before pump 4 was started — was 30 minutes. Decisions made in that window carried consequences the crew could not evaluate; they were choosing between unknowns under a rising wet well.

**C-3. Automation trust.** The crew's belief that the plant would alarm on high level was correct as a description of the design and wrong as a description of the plant. The absence of alarms during a heavy rain was, to them, evidence that levels were normal.

---

## 7. What Worked

The Panel identifies the following as effective and worth preserving. It notes that most of them are attributable to individual initiative rather than to system design, which is itself a finding.

1. **Sokolov's decision to come in at 03:15 uncalled.** He was not on shift and not required to report. Physical rounds were the only detection mechanism the plant had left, and they worked. Without that judgment the wet well would have overtopped the Structure 3 weir uncontrolled, likely flooding the headworks electrical room at elevation 216 and extending the outage by weeks.

2. **The bypass decision itself was correct and timely.** Ng declared the bypass 45 minutes after the screen blinded and 25 minutes after the option was framed. A controlled bypass at a monitored, sampled outfall is materially better than an uncontrolled overflow at an unsampled structure with electrical room loss. The Panel endorses this decision without reservation.

3. **Pruitt's valve rebuild.** Diagnosis at 09:30, full arrangement rebuilt and verified by 14:00, on a Sunday, with a callout crew. Firm capacity was restored to the maximum available from surviving equipment 8 hours after the fault was identified.

4. **Sampling discipline.** The first bypass composite was underway at 06:12, seven minutes after the gate opened. Sampling was maintained continuously for the full 41 hours and for 5 days afterward, at 6 river stations. The data set is complete and defensible, and it materially supported the shortening of the access closure from an initially proposed 14 days to 9.

5. **The downstream water system call.** Made at 06:52, 12 minutes after the state, by direct call to an on-call operator whose number Grantham maintained personally. The intake was on backup by 07:15, well ahead of the leading edge of the plume. No drinking water quality impact occurred.

6. **Manual raking rotation.** An improvised, physically demanding solution that reduced screen differential from 3.1 ft to 1.4 ft and preserved partial screening throughout the bypass, meaningfully reducing floatables reaching the river.

7. **Rental pump mobilization.** Contractor called at 08:00, 12 MGD online by 18:00 on a Sunday.

8. **Data integrity.** The SCADA historian, alarm journal, and archived exception reports permitted a complete reconstruction. Nothing was purged, edited, or lost. The 39 unread reports, retained in an unread mailbox, are what allowed the Panel to establish the inhibit duration precisely.

---

## 8. What Did Not Work

1. **Detection.** Five hours and 48 minutes. The plant's automated detection did not exist, and its human detection was one unscheduled walk.

2. **The alarm system as a whole.** 347 events in 90 minutes made the one relevant status change invisible even to an attentive operator. An alarm system that cannot distinguish a plant failure from routine wet weather noise is not performing its function.

3. **Restoration control after contractor work.** A contractor's own punch list identified the open item. Nothing existed to act on it.

4. **Diagnosis.** Twenty-nine hours elapsed between the trip and the correct identification of its cause, and the wrong cause was fixed on within three minutes of the trip's discovery. The misdiagnosis did not directly cause the bypass, but it foreclosed the possibility of returning pump 2 to service and it framed pump 4 as the only option.

5. **The standby pump start.** The single most consequential action of the response. Firm capacity 57 → 19 MGD in 258 seconds. The Panel emphasizes: a system that permits a correct-in-intent action to destroy a critical asset in four minutes, with no interlock, no checklist, and no indication, has misallocated the burden of vigilance to the person least able to bear it at 4:10 a.m.

6. **Regulatory notification.** Sixty minutes late, delayed further by an obsolete phone number in an 11-year-old plan, and structured as a downstream compliance act rather than a parallel response task.

7. **Internal escalation and external communication.** The Executive Director learned of the event 2 h 10 min after discovery. Member towns were briefed 10 h 25 min after the bypass began, and two boards of health heard from the state first. The Authority ceded the narrative entirely.

8. **Incident command.** No incident commander was formally designated until 05:35. For 1 h 55 min the response was a phone call between two people, each assuming the other held a fuller picture.

9. **Preparedness posture.** A flood watch, a 1.5–2.5-inch forecast, a plant with a 26.5 percent operator vacancy rate, an unsupported drive fleet, one bar screen, and an 11-year-old plan, and the facility went into the night with three operators and no watch declared. Nothing in that decision violated a procedure. That is the problem.

---

## 9. Action Items

Status tracked in the Authority's corrective action register; monthly reporting to the Executive Director, quarterly to the Board. Verification method is specified for each item; "closed" requires the named verifier's sign-off, not the owner's.

### 9.1 Immediate (completed or due within 30 days of issue)

| ID | Action | Owner | Due | Verification |
|---|---|---|---|---|
| AI-01 | Full audit of all 4,100 SCADA points for inhibit, suppress, force, and simulate states; restore all not covered by an approved defeat permit. *(4 additional inhibits found and cleared; complete)* | Hollis Pruitt | Mar 31, 2027 ✔ | Point-by-point report signed by Ng |
| AI-02 | Redirect the daily Silenced and Inhibited Point Report to a role-based distribution list (Chief Plant Operator, Maintenance Supervisor, Director of Operations) with mandatory acknowledgment; report escalates to the Executive Director if unacknowledged 48 hours. | Dmitri Sokolov | Apr 30, 2027 | 30 consecutive days of logged acknowledgments |
| AI-03 | Decouple all standby-pump auto-start permissives from alarm bits; derive from raw process values. Test each permissive by simulated level. | Priya Raghunathan | May 15, 2027 | Witnessed functional test, results to Panel |
| AI-04 | Add valve lineup verification with two-person sign-off to all standby equipment start procedures; issue as an interim operating directive pending full procedure revision. | Kathleen Ng | Apr 15, 2027 ✔ | Directive posted at all consoles; read-and-sign by all operators |
| AI-05 | Revise valve exercise PM task text to require as-left position verification, position tagging, and independent second check. Apply retroactively: verify position of all 63 critical valves. | Hollis Pruitt | May 31, 2027 | Completed PM records; valve position audit report |
| AI-06 | Post a one-page notification decision aid at every operator console: trigger ("discovery of a condition likely to result in a bypass"), 2-hour clock, verified 24-hour MassDEP number, required content, and a standing instruction to notify early and amend rather than delay. | Rochelle Grantham | Apr 15, 2027 ✔ | Physical posting audit; quarterly number verification |
| AI-07 | Stock a complete spare influent VFD and one spare power module; establish emergency service agreement with a drive service house. | Priya Raghunathan | Jun 15, 2027 | Purchase order and receipt inspection |

### 9.2 Near-term (due within 120 days)

| ID | Action | Owner | Due | Verification |
|---|---|---|---|---|
| AI-08 | Establish a **Temporary Defeat Permit** system: no protective function may be inhibited without a written permit specifying reason, compensatory measure, responsible person, and expiry not to exceed 7 days without renewal by the Director of Operations. Daily open-permit report to the shift. | Kathleen Ng | Jun 30, 2027 | Permit log audit at 30, 60, 90 days |
| AI-09 | Install independent high-level detection in the influent wet well: float switch hardwired to a dedicated horn and beacon, independent of the SCADA network and of LIT-101. | Priya Raghunathan | Jul 31, 2027 | Functional test with LIT-101 out of service |
| AI-10 | Install position transmitters on influent pump discharge valves V-1D through V-4D; add valve position to the pump READY permissive and to the headworks graphic. | Priya Raghunathan | Aug 31, 2027 | Witnessed test: pump will not start with valve closed |
| AI-11 | Rewrite the Wet Weather Operating Plan. Scope to include: watch trigger revised to 1.0 in forecast or any flood watch; staffing table matched to actual complement; incident commander designation at first alarm; notification triggers and verified contacts; capacity-degraded operating modes; annual review requirement with a named owner. | Kathleen Ng | Aug 15, 2027 | Board adoption; tabletop exercise before adoption |
| AI-12 | Revise CMMS escalation rules: any work order on a redundant critical asset escalates to the Director of Operations at 30 days and to the Executive Director at 60 days, with a written compensatory-measure plan required at 30 days. | Hollis Pruitt | Jun 30, 2027 | Rule test on the 41 identified aged work orders |
| AI-13 | Close out the 41 open work orders over 90 days on critical assets, or document an accepted-risk determination signed by the Executive Director for each. | Hollis Pruitt | Sep 30, 2027 | Register review by Panel |
| AI-14 | Revise offboarding and vacancy procedures to require a documented transfer of *functions* — recurring reports, distribution lists, system ownerships, informal responsibilities — with a named receiving role. Apply retroactively to all 9 vacant operator posts and the vacant I&C supervisor post. | Terrence Boyle, HR Manager | Jul 15, 2027 | Function transfer records for all vacancies |
| AI-15 | Establish contractor work acceptance standard for protective systems: no acceptance without a named Authority employee's functional verification of every point touched, and formal closure of every punch list item. | Priya Raghunathan | Jun 30, 2027 | Applied to next two contracted SCADA scopes |
| AI-16 | Create fault-code job aids at each drive and major equipment local panel; place manufacturer manuals on the plant network accessible from the control room. | Dmitri Sokolov | Jul 31, 2027 | Spot check at 6 locations |

### 9.3 Structural (due within 12 months)

| ID | Action | Owner | Due | Verification |
|---|---|---|---|---|
| AI-17 | Execute the deferred influent VFD replacement, all four drives. Present to the Board as a compliance-driven emergency capital item. | Priya Raghunathan | Dec 31, 2027 | Commissioning report; drive fleet under manufacturer support |
| AI-18 | Establish a **Capital Deferral Risk Register**. Any deferral of a funded renewal item on a critical asset requires a written risk statement, a compensatory measure, and Board acknowledgment at the meeting where the deferral is approved. The register is a standing agenda item at every quarterly Board meeting. | Colleen Marchetti, Finance Director | Sep 30, 2027 | First register presented to Board Q1 FY28 |
| AI-19 | Conduct a formal alarm rationalization for the entire facility to EEMUA 191 / ISA 18.2 principles. Target: steady-state rate below 6 alarms per operator per hour; wet weather peak below 10 per 10 minutes; every priority-1 alarm to have a defined operator action. | Priya Raghunathan | Feb 29, 2028 | Measured alarm rates over 90 days post-implementation |
| AI-20 | Complete bar screen 1 restoration and establish a formal single-train operating protocol: whenever any preliminary treatment train is out of service beyond 14 days, a written compensatory plan and a daily capacity statement are required. | Hollis Pruitt | Jun 30, 2027 | Screen 1 in service; protocol issued |
| AI-21 | Present to the Board a staffing recovery plan addressing the 26.5% operator vacancy rate, including a market wage analysis, an operator-in-training pipeline with two member town vocational programs, and a licensing support program. Include an explicit statement of the operational limits the Authority accepts at current staffing. | Alonzo Ferreira | Oct 31, 2027 | Board action recorded |
| AI-22 | Establish an external communication protocol: member town administrators and boards of health notified within 60 minutes of any Category 1 event, by a designated public information officer, with a pre-approved initial message template. Public notice posted within 2 hours. | Alonzo Ferreira | Jul 31, 2027 | Tested in the AI-11 tabletop exercise |
| AI-23 | Institute quarterly full-scale wet weather drills, including at least one annually on a night shift with the actual on-duty complement, scored against detection time, notification time, and correct capacity-degraded lineup. | Kathleen Ng | First drill Sep 30, 2027 | Drill after-action reports to Board |
| AI-24 | Commission an independent reliability assessment of all wet weather critical assets — pumping, screening, grit, primary bypass structures, standby power — with condition scores and a 10-year renewal schedule to be embedded in the capital plan. | Priya Raghunathan | Mar 31, 2028 | Report delivered; renewal schedule adopted |

### 9.4 Tracking

The corrective action register is maintained by Rochelle Grantham. Overdue items escalate automatically to the Executive Director at 15 days and to the Board Chair at 30 days. The Panel will reconvene at 6 months (October 22, 2027) and 12 months (April 22, 2028) to assess whether the actions have produced measurable change in the underlying conditions, using the latent-condition metrics in §3.4 as the baseline. **The Panel notes that this event was preceded by fourteen months of individually invisible degradation; the appropriate test of this postmortem is not whether the action items are marked complete, but whether the Authority can now see the next fourteen months coming.**

---

## Appendix A — Abbreviations

BOD₅ five-day biochemical oxygen demand · CMMS computerized maintenance management system · CSO combined sewer overflow · EEMUA Engineering Equipment and Materials Users Association · HMI human-machine interface · IGBT insulated-gate bipolar transistor · ISA International Society of Automation · MassDEP Massachusetts Department of Environmental Protection · MGD million gallons per day · MLSS mixed liquor suspended solids · NPDES National Pollutant Discharge Elimination System · PM preventive maintenance · SCADA supervisory control and data acquisition · TSS total suspended solids · VFD variable frequency drive · WO work order

## Appendix B — Note on Penalty Exposure

The $312,000 figure is the exposure stated in the March 27 Notice of Noncompliance and is not a determined penalty. The Authority is preparing a response. Nothing in this document is an admission for the purposes of that proceeding; it is an internal learning artifact prepared under the Learning Review Protocol. Counsel has reviewed and does not object to the distribution list at the head of this document.

## Appendix C — Load Estimation Basis

Bypass loads in §3.1 are calculated from 14 composite samples collected at the Outfall 002 sample point over the 41-hour discharge, flow-weighted against the Structure 3 gate rating curve, and expressed as the difference from the load that would have been discharged had the same volume received full treatment at the facility's rolling 12-month average effluent quality. Volume (11.4 MG) is derived from the gate rating curve and cross-checked against the difference between influent flow totalization and final effluent totalization over the discharge period; the two methods agree within 4.1 percent.

## Appendix D — Rainfall and Hydraulic Data

**D.1 Precipitation, March 13–14, 2027**

| Interval ending | Depth (in) | Cumulative (in) | Plant influent at interval end (MGD) |
|---|---|---|---|
| 20:40 Mar 13 | 0.09 | 0.09 | 34.6 |
| 21:40 | 0.14 | 0.23 | 36.1 |
| 22:40 | 0.21 | 0.44 | 38.9 |
| 23:40 | 0.26 | 0.70 | 41.4 |
| 00:40 Mar 14 | 0.31 | 1.01 | 44.8 |
| 01:40 | 0.39 | 1.40 | 49.2 |
| 02:40 | 0.48 | 1.88 | 57.6 |
| 03:40 | 0.41 | 2.29 | 60.9 |
| 04:40 | 0.29 | 2.58 | 58.2 |
| 05:40 | 0.22 | 2.80 | 54.7 |
| 06:40 | 0.13 | 2.93 | 51.0 |
| 07:40 | 0.09 | 3.02 | 47.8 |
| 08:40 | 0.05 | 3.07 | 44.9 |
| 09:40 | 0.03 | 3.10 | 43.1 |

Total 3.10 in over 14.0 hours. Peak 60-minute intensity 0.48 in (02:40). NOAA Atlas 14 places this event between the 5-year and 10-year recurrence interval for the 12-hour duration at this location. **It is not an extreme event.** The 2016 Wet Weather Operating Plan's stated design condition is the 10-year, 24-hour storm (4.8 in), which the facility is nominally capable of passing through secondary treatment at 68 MGD. The March 13–14 storm produced approximately 65 percent of that design depth and a peak influent of 61.4 MGD, which is 90 percent of permitted peak hydraulic capacity and 108 percent of firm pumping capacity. The Panel notes that even with all four pumps healthy, firm capacity (57 MGD) would have been exceeded for approximately 2 hours 40 minutes on the night in question. That fact was not known to anyone in the organization before this review, is not documented in the Wet Weather Operating Plan, and constitutes a standing latent condition addressed by AI-11 and AI-24.

**D.2 Influent wet well level, March 13–14**

| Time | Level (ft) | Rate (ft/hr) | Condition |
|---|---|---|---|
| 21:52 Mar 13 | 6.8 | — | Pump 2 trips; pumps 1 and 3 in service |
| 23:00 | 7.4 | +0.5 | Within normal band (5.0–10.0 ft) |
| 01:00 Mar 14 | 8.6 | +0.6 | Normal |
| 02:10 | 9.5 | +0.9 | Inflow exceeds two-pump capacity |
| 02:34 | 11.5 | +1.7 | **HI setpoint — inhibited; no auto-start call** |
| 03:05 | 13.0 | +2.9 | **HI-HI setpoint — inhibited** |
| 03:38 | 14.5 | +2.7 | Discovery imminent |
| 03:40 | 14.6 | +2.7 | **Discovery** |
| 04:10 | 14.9 | +0.6 | Pump 4 started (against closed valve) |
| 04:14 | 14.9 | +0.6 | Pump 4 secured |
| 05:20 | 15.1 | +0.2 | Bar screen 2 blinds; channel surcharges |
| 06:05 | 15.2 | 0.0 | At weir elevation; **bypass declared** |
| 06:19 | 15.0 | −0.9 | Level falling |
| 07:30 | 12.4 | −2.2 | Stabilizing |

Structure 3 emergency overflow weir crest: 15.2 ft. Headworks channel deck: 15.6 ft. Electrical Room 216 floor slab: 16.1 ft. **At the moment of the bypass declaration the margin between the wet well and an uncontrolled overflow was zero, and the margin to loss of the headworks electrical room was 0.9 ft.** The Panel records this to make explicit the conditions under which the 06:05 decision was made and to support its endorsement of that decision in §7.2.

**D.3 Pumping capacity, hour by hour**

| Period | Pumps available | Installed capacity (MGD) | Firm capacity (MGD) | Influent (MGD) | Deficit |
|---|---|---|---|---|---|
| Pre-event | 1, 2, 3, 4 | 76 | 57 | 34 | none |
| 21:52–04:10 Mar 14 | 1, 3, 4 (standby) | 57 | 38 | 39–61 | up to 4 |
| 04:14–14:00 Mar 14 | 1, 3 | 38 | 19 | 47–58 | up to 20 |
| 14:00–18:00 Mar 14 | 1, 3 + header cross-tie | 38 | 19 | 44–47 | up to 9 |
| 18:00 Mar 14–Mar 17 | 1, 3 + rentals | 50 | 31 | 34–44 | intermittent |
| Mar 17–Apr 18 | 1, 2, 3 + rentals | 69 | 50 | 32–38 | none |
| Apr 18 onward | 1, 2, 3, 4 | 76 | 57 | 34 | none |

The controlling observation is in row two. Between the trip and the pump 4 start, the plant had 57 MGD of installed capacity against an influent that peaked at 61.4 MGD — a deficit of roughly 4 MGD for under three hours, entirely absorbable by wet well and upstream interceptor storage had the standby pump been started successfully at any point before 03:10. **A pump 4 start at 22:00 with an open discharge valve would have ended this incident as a logbook entry.**

---

## Appendix E — The Thirty-Nine Reports

The Panel examined all 39 Silenced and Inhibited Point Reports generated between February 4 and March 14, 2027, recovered from the retired supervisor's retained mailbox. Each is a two-page PDF. Each lists, under the heading *ALARM INHIBIT — ACTIVE*, the following two lines:

```
LIT-101_HI      INFLUENT WET WELL LEVEL HIGH        INHIBITED  02/03/27 14:22
LIT-101_HIHI    INFLUENT WET WELL LEVEL HIGH HIGH   INHIBITED  02/03/27 14:22
```

The reports functioned exactly as designed. The detection system for the failure of the detection system worked perfectly for 39 consecutive days and produced no effect whatsoever, because its output had no destination.

The Panel considers this the most instructive single artifact of the incident, and recommends that a redacted copy of the February 4 report be included in the annual operator refresher curriculum under AI-23. The lesson is not that someone should have read it. The lesson is that **a control is not a control until someone is obligated to act on it, that obligation is attached to a role rather than a person, and the absence of the action is itself detected.** Reports that no one is required to acknowledge are, from a reliability standpoint, indistinguishable from reports that are not generated at all — with the additional hazard that the organization believes itself to be monitored.

The report generator was not modified after the supervisor's retirement because no process existed that would have prompted anyone to examine what he was receiving. His mailbox received 412 automated messages between November 6, 2026, and March 14, 2027, spanning 11 distinct recurring reports, of which the Panel judges 4 to be safety- or compliance-relevant. All 11 have been reassigned to role-based lists under AI-02 and AI-14.

---

## Appendix F — Items Considered and Not Adopted

The Panel records the following to document that they were examined, and why they were rejected. A postmortem that lists only its conclusions invites the same proposals to be re-litigated later.

**F.1 Disciplinary action.** Considered and rejected on the merits, not merely on protocol grounds. Every individual action in this sequence was locally rational and consistent with the training, procedures, indications, and staffing the organization provided. The contractor technician who inhibited two points followed a standard practice and documented the open item. The operator who exercised V-4D executed the PM task as written. The operator who started pump 4 followed the standby start procedure as written. The Chief Plant Operator's diagnosis of the drive fault was the hypothesis the available evidence best supported. The budget officers who deferred the VFD line had no artifact telling them what they were accepting. **Discipline would remove the small number of people who now understand this failure most deeply, and would replace a systems finding with a personnel event, guaranteeing recurrence.** The Panel is unanimous.

**F.2 Attributing the event primarily to the storm.** Rejected. The rainfall was between a 5- and 10-year event, well within design condition. Attribution to weather would foreclose every corrective action in §9.

**F.3 Attributing the event primarily to the VFD failure.** Rejected. Component failure on 18-year-old, manufacturer-unsupported hardware is an expected condition, not a cause. A facility with intact redundancy, intact detection, and a correct valve lineup absorbs it without a bypass. The drive failure is properly characterized as the *trigger* of an already-failed system.

**F.4 Attributing the event primarily to staffing vacancies.** Considered seriously and rejected as a primary cause, while retained as a significant contributing factor (O-3). Five operators on shift would very likely have shortened the detection gap materially. But five operators would not have restored the alarm, opened the valve, repaired the screen, or replaced the drive. The Panel cautions specifically against a corrective posture in which staffing becomes the explanation for all failures, because it converts a set of fixable engineering and process problems into a single problem the Authority cannot solve quickly, and thereby licenses inaction on the rest.

**F.5 Interlocking the bypass gate to prevent operator-initiated opening.** Rejected as actively harmful. The 06:05 decision was correct and was made with zero margin. Any control that would have slowed or blocked it would have produced an uncontrolled, unsampled overflow and probable loss of the headworks electrical room. **The Authority's problem on March 14 was not that a bypass occurred; it was that the plant arrived at a condition where a bypass was the best available option.**

**F.6 Immediate replacement of the SCADA platform.** Deferred. The platform is serviceable; the failures were in configuration governance, alarm rationalization, and function ownership, none of which a new platform would remedy and all of which a migration would disrupt. Revisit after AI-19 is complete and measured.

**F.7 A standing 24-hour on-site instrumentation technician.** Deferred to AI-21. Not affordable at current staffing levels and would not have prevented this event, since no one was looking for the inhibit.

---

## Appendix G — Metrics for Verifying That This Postmortem Worked

The Panel proposes the following leading indicators, to be reported to the Board quarterly beginning Q1 FY28. Each is chosen because it would have moved before March 14, 2027, had it existed.

| Indicator | Baseline (Mar 14, 2027) | Target | Owner |
|---|---|---|---|
| Protective functions in an undocumented defeat state | 6 | 0 | Hollis Pruitt |
| Median age of open defeat permits | n/a (no system) | ≤ 3 days | Kathleen Ng |
| Daily inhibit report acknowledgment rate | 0% | 100% | Dmitri Sokolov |
| Open work orders >90 days on critical assets | 41 | ≤ 5 | Hollis Pruitt |
| Critical assets operating without manufacturer support | 4 drives, 2 screens | 0 | Priya Raghunathan |
| Funded capital renewal items deferred without a risk entry | 2 | 0 | Colleen Marchetti |
| Steady-state alarm rate (per operator per hour) | 171 | ≤ 6 | Priya Raghunathan |
| Wet weather peak alarm rate (per 10 min) | 200+ | ≤ 10 | Priya Raghunathan |
| Critical valves without verified as-left position record | 63 | 0 | Hollis Pruitt |
| Licensed operator vacancy rate | 26.5% | ≤ 10% | Terrence Boyle |
| Median detection time in night-shift drills | not measured | ≤ 10 min | Kathleen Ng |
| Median regulatory notification time in drills | not measured | ≤ 45 min | Rochelle Grantham |
| Member town notification time, Category 1 events | 10 h 25 min | ≤ 60 min | Alonzo Ferreira |
| Age of the Wet Weather Operating Plan | 11 years | ≤ 12 months since review | Kathleen Ng |

---

## Appendix H — Statement of the Panel

Eleven and a half million gallons reached the Blackstone River because a level alarm was switched off on a Tuesday afternoon in February and no one was obligated to switch it back on; because a valve was left closed in January and nothing was required to notice; because a gearbox was on a twelve-week lead time and the work order that tracked it was classified as low priority precisely *because* there was a second screen; because a budget line was moved twice for reasons that were each defensible and were never written down together; and because a supervisor retired in November and took an unwritten job with him.

None of those five conditions was hidden. All five were recorded somewhere — in a punch list, a PM record, a CMMS queue, a set of Board minutes, an HR file. What the Authority lacked was not information. It was any mechanism that assembled the information into a picture of its own degraded state, and any person whose defined job was to look at that picture.

The Panel's central recommendation, beneath all twenty-four action items, is this: **the Authority must build and maintain a continuously visible account of which of its protections are presently working.** Not which were designed. Not which were installed. Which are working, today, verified, with a named person answerable for each. Every item in §9 is an instance of that principle. The Panel believes the Authority can build it within twelve months, that it costs less than the penalty exposure of a single event of this kind, and that in its absence the specific failures corrected here will be replaced by different ones with the same shape.

The staff who worked the night of March 13–14 and the two days that followed did so in cold rain, on a Sunday, under conditions the organization had unknowingly created for them, and they kept an uncontrolled overflow and the loss of the plant's electrical heart from being added to what did occur. The Panel thanks them, and directs the reader who wants to know what went wrong to look upstream of them — in February, in January, in December, in November, and in two budget cycles before that.

---

*Submitted by the Incident Review Panel, April 22, 2027.*

*Approved: Alonzo Ferreira, Executive Director — April 22, 2027*
*Received: Quinsigamond Regional Water Pollution Control Authority Board — April 29, 2027*

*Next Panel review: October 22, 2027. Second review: April 22, 2028.*
