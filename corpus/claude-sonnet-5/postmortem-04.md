# Incident Postmortem: Willow Brook Public Schools Transportation Launch Failure

**Incident Period:** September 8–11, 2026 (acute phase); reconciliation ongoing through September 21, 2026
**Document Status:** Final
**Prepared For:** Superintendent's Cabinet, Board of Education, Willow Brook Public Schools
**Prepared By:** Office of the Superintendent, in coordination with Transportation, Technology, Special Services, and Business Administration
**Distribution:** Board of Education, Cabinet, Transportation Department, Trailhead Implementation Team, New Jersey Department of Education (upon request)
**Classification:** Internal — Operational Review

This postmortem examines the systems, processes, and decisions that led to a failed transportation launch on the first day of school and the four days that followed. It is not an assignment of individual fault. Where individuals are named, it is because their role in a decision or a handoff illuminates a gap in the system that produced the outcome. The purpose of this document is to establish a factual record, quantify impact, and generate binding corrective actions with named owners and dates.

---

## 1. Executive Summary

Willow Brook Public Schools enrolls 9,800 students across 14 schools in Middlesex County, New Jersey, and provides transportation to 5,600 of them via a fleet of 112 buses. In June 2026, the district's incumbent transportation contractor lost a competitive rebid. This decision, while procedurally sound and the product of a lawful procurement process, compressed the runway for standing up a new contracted operator, a new routing software platform (Trailhead), and a new set of operational runbooks into eight weeks — a window substantially shorter than the sixteen-to-twenty weeks industry practice and the district's own prior transitions have required.

Within that compressed window, the district migrated student address and eligibility data into Trailhead. The migration ran on August 24, 2026. It silently dropped 1,340 student records because the apartment/unit field in the source system exceeded the maximum field length accepted by Trailhead's import schema. Among the dropped records were 41 students whose Individualized Education Programs (IEPs) mandate door-to-door transportation — a legally required service under the Individuals with Disabilities Education Act (IDEA) and New Jersey special education code. The import process generated validation reports that flagged the discrepancy in raw form, but no owner in the new operating runbook was assigned to reconcile those reports. The prior contractor's runbook had assigned this function to a position that did not exist, and was not recreated, in the new operating model.

The district opened school with a staggered entry: a soft-open for early childhood and select special-education routes on September 3–4, followed by full district-wide opening on September 8. On September 8, 62 of the district's routes ran late by an average of 47 minutes, nine buses did not arrive at their assigned schools at all, and a kindergartner was released from her bus 1.2 miles from her registered address before a crossing guard recognized the error and intervened. Transportation Director Rudolph Sciarra attributed the failures publicly and internally to a driver shortage, and the shortage was real — the department carried 14 open driver positions against a need of 126 to run all routes without spares. However, the shortage does not account for the address-matching failures, the absence of the 41 IEP students from any route manifest, or the tier collisions that followed. Chief Technology Officer Bethany Kwan did not compare pre- and post-migration address counts — a check that would have surfaced the 1,340-record discrepancy — until the evening of Wednesday, September 9, more than 24 hours after the first missed pickups.

In the absence of validated route data, transportation supervisors issued hand-written route sheets at the bus yard on Tuesday and Wednesday. These sheets carried no tier (elementary/middle/high school) assignments, causing elementary and high school runs to be dispatched on overlapping schedules and compounding delays that had originated with the data defect. Tuesday's system-wide average delay of 47 minutes grew to 63 minutes on Wednesday before Superintendent Dr. Ifeoma Adeyemi opened a district command post that afternoon. Marisela Duarte, Supervisor of Special Services, arranged contracted van service for the 41 affected IEP students, with service beginning Thursday, September 10 — four school days after the first missed pickup for this population. Business Administrator Gerald Ostrowski approved $214,000 in emergency funding for the van contracts and related remediation.

The district received 3,100 parent phone calls on September 9 alone, logged 890 students absent or tardy for transportation-related reasons over the first week, and is the subject of two state complaints filed with the New Jersey Department of Education alleging failure to provide mandated transportation services under students' IEPs.

The root cause of this incident was a **process ownership gap**: the transition from the incumbent contractor to the new operating model eliminated a data-reconciliation function without reassigning it, and no compensating control (automated record-count validation, a go/no-live data-quality gate, or an assigned human reviewer) existed in the new system to catch a schema-level data defect before it reached production routing. This gap was compounded by an accelerated procurement timeline, a routing platform implementation that prioritized go-live over data validation, a public and internal narrative that attributed early failures to a labor shortage without confirming that hypothesis against the data, and route-sheet practices that lacked the tier-separation safeguards the routing software would otherwise have enforced automatically.

---

## 2. Impact, in Numbers

| Metric | Value |
|---|---|
| Total district enrollment | 9,800 students, 14 schools |
| Students eligible for transportation | 5,600 |
| Bus fleet | 112 vehicles |
| Compressed procurement-to-launch window | 8 weeks (incumbent contract loss to first day of school) |
| Records dropped in the August 24 data migration | 1,340 |
| Affected students with IEP-mandated door-to-door service | 41 |
| Days the validation report went unreconciled before detection | 16 (August 24 – September 9) |
| Open driver positions on opening day | 14 (against a full complement of 126) |
| Routes running late on September 8 | 62 |
| Average delay, September 8 | 47 minutes |
| Buses that did not arrive at all, September 8 | 9 |
| Average delay, September 9 (Wednesday) | 63 minutes |
| Distance a kindergartner was released from her registered address | 1.2 miles |
| School days between first missed IEP pickup and contracted van service | 4 |
| Emergency funds approved for contracted van service | $214,000 |
| Parent/guardian calls received, September 9 alone | 3,100 |
| Students absent or tardy for transportation reasons, week of September 8 | 890 |
| State complaints filed alleging missed mandated service | 2 |
| Days from incident onset to command post activation | 2 (September 8 onset; command post opened afternoon of September 9) |
| Days from incident onset to restored IEP transportation service | 4 |

These figures understate second-order impact that the district is still quantifying: instructional time lost to late arrivals and early releases, staff overtime incurred running the command post and manual dispatch, the reputational and enrollment-retention effect of a chaotic opening week, and the district's exposure under the two pending state complaints, which under New Jersey special education regulations can carry compensatory service obligations independent of any financial penalty.

---

## 3. Timeline

All times are local (Eastern). Dates are 2026 unless otherwise noted. This timeline draws on system logs, the transportation department's dispatch records, command post notes, and interviews with staff named in this document.

### Pre-Incident: Procurement and Implementation

**June 9** — Board of Education awards the district's transportation services contract to a new operator following a competitive rebid. The incumbent contractor, which had held the contract for eleven years and possessed institutional knowledge of the district's routing, driver roster, and data-handling practices, is not retained. The award leaves 91 calendar days (roughly eight instructional weeks accounting for July closures) until the September 8 opening.

**June 15** — Transportation Department and CTO's office jointly select Trailhead as the new routing and dispatch platform, replacing the incumbent contractor's legacy in-house routing tool. Contract execution and platform provisioning begin the same week.

**June 22 – July 31** — Trailhead implementation team and district IT conduct platform configuration, staff onboarding, and driver/vehicle data setup. The new contracted operator begins driver recruitment against a projected need of 126 drivers.

**August 3** — New operator reports 22 open driver positions to Transportation Director Sciarra. Recruitment continues through the summer.

**August 10** — District finalizes the "new operating runbook" for the 2026–27 launch, adapted from the incumbent contractor's prior procedures. The runbook does not carry forward a discrete role for post-import data reconciliation that existed under the prior contractor's internal process; the function is assumed, but never explicitly assigned, to fall under "Transportation Data Coordinator," a position that is vacant and not filled before opening.

**August 24, 6:12 AM** — Student information system (SIS) export of active student addresses and transportation eligibility runs and is handed off to the Trailhead import pipeline.

**August 24, 6:47 AM** — Trailhead import completes. The import schema enforces a maximum field length for the apartment/unit subfield of the address record. 1,340 records exceed this limit (predominantly multi-unit residential buildings in the district's denser municipalities) and are silently excluded from the imported dataset rather than flagged as hard failures requiring resolution before proceeding. Among these are the 41 students with IEP-mandated door-to-door service.

**August 24, 7:15 AM** — Trailhead generates a standard post-import validation report, which includes total records submitted versus records successfully imported (8,460 submitted; 7,120 imported). The report is emailed to a distribution list that includes the CTO's office and Transportation Department leadership. No individual is assigned to open, read, or act on this specific report under the new runbook.

**August 24 – September 2** — The validation report remains in inboxes, unopened or unreconciled against the source SIS record count. Route-building proceeds in Trailhead using the incomplete 7,120-record dataset. 1,340 students, including the 41 IEP students, do not appear on any bus route.

**September 3–4** — District conducts a staggered soft-open for early childhood programs and a subset of special-education transportation routes, ahead of the full district-wide opening on September 8. Several of the 41 affected IEP students are scheduled for this soft-open window; because they do not exist in the routed dataset, their scheduled pickups on September 3 do not occur. This is the first missed pickup referenced later in this timeline. Calls from affected families reach Special Services and school-level staff but are handled as isolated missing-student inquiries rather than escalated as a systemic data issue.

### September 8 (Tuesday) — District-Wide Opening

**5:30 AM** — Buses begin morning routes district-wide under Trailhead-generated route assignments for the 7,120 students in the imported dataset, supplemented by hand-corrected paper additions for a small number of individually reported missing students from the soft-open period. The 41 IEP door-to-door students remain unrouted; their absence has not yet been systematically identified.

**6:45 AM – 8:15 AM** — Dispatch begins receiving school-level and parent reports of buses running significantly behind schedule. By 8:00 AM, Transportation Department has logged reports of delays on 40+ routes.

**8:20 AM** — A kindergartner is released from her bus 1.2 miles from her registered address, at a stop that does not match her route assignment. A crossing guard at the intersection recognizes the child does not belong in the area, does not release her to walk, and contacts the elementary school and Transportation dispatch. The child is safely returned to her family by early afternoon. This event is escalated internally as a critical safety incident and becomes the catalyst for elevated attention to the broader routing failure, though the district's response over the following 24 hours remains focused primarily on driver staffing.

**Mid-morning** — Transportation Director Sciarra, briefing Cabinet on the day's disruptions, attributes the delays to the driver shortage (14 open positions as of that morning). This explanation is accepted without cross-referencing route counts, student counts, or the August 24 validation report.

**By end of day** — Final tally: 62 routes late by an average of 47 minutes; 9 buses never complete their assigned run; 41 IEP students receive no transportation service; hundreds of additional families report no-shows or major delays not yet centrally logged.

**Evening** — Transportation Department, working overnight, begins issuing hand-written route sheets at the bus yard to cover gaps and reassign drivers, in place of relying solely on Trailhead-generated manifests, which are believed (correctly, though not yet diagnosed as a data problem) to be incomplete. These hand-written sheets do not carry tier designations distinguishing elementary, middle, and high school runs.

### September 9 (Wednesday) — Escalation

**5:30 AM – 9:00 AM** — Hand-written route sheets, issued without tier assignments, result in elementary and high school routes being dispatched on overlapping timeframes, competing for the same buses and drivers and causing secondary congestion at multiple school driveways. System-wide average delay grows to 63 minutes, worse than the prior day despite the added drivers and manual corrections.

**Throughout the day** — District call center logs 3,100 parent and guardian calls, overwhelming available phone lines and reception staff at all 14 schools.

**Afternoon** — CTO Bethany Kwan, reviewing the day's operational data with Transportation staff in preparation for an afternoon Cabinet briefing, requests a comparison of the SIS student count against the Trailhead routed-student count for the first time since the August 24 import. This comparison had not been performed at any point during implementation, testing, or the first two days of live operation.

**Evening, approximately 6:30 PM** — The comparison confirms a 1,340-record discrepancy. Cross-referencing against the Special Services caseload identifies the 41 students with IEP-mandated door-to-door transportation among the missing records. This is the first point at which the data import failure is identified as the root technical cause of the launch failure, 16 days after the defective import occurred and roughly 60 hours after the first missed pickup on September 3.

**Evening** — Superintendent Dr. Ifeoma Adeyemi convenes department heads and opens a district command post, consolidating Transportation, Technology, Special Services, Business Administration, and Communications into a single coordinated response structure operating out of the district administration building.

### September 10 (Thursday) — Stabilization Begins

**Morning** — Command post directs Trailhead implementation team to re-run the address import using the corrected field-length schema, restoring the 1,340 previously dropped records to the routable dataset. Interim manual route assignments continue for the general student population while restored records are reintegrated into the platform.

**Morning** — Marisela Duarte, Supervisor of Special Services, finalizes arrangements with a contracted van service provider to begin door-to-door transportation for the 41 IEP-mandated students that day — the fourth school day after the first missed pickup on September 3.

**Afternoon** — Business Administrator Gerald Ostrowski approves $214,000 in emergency funding to cover the contracted van service, additional driver overtime, and command-post operational costs.

**Throughout the day** — Command post begins issuing tiered, Trailhead-validated route sheets in place of hand-written sheets. Elementary/middle/high school tier separation is restored to dispatch practice.

### September 11 (Friday) and Following Week

**September 11** — First day with fully restored dataset in Trailhead and tiered route assignments. Delays persist on a reduced number of routes attributable to the confirmed driver shortage, now addressed through overtime and route consolidation rather than data gaps.

**September 14–18** — District logs 890 total student absences or tardies attributable to transportation issues for the week of September 8–11. Two families file complaints with the New Jersey Department of Education alleging failure to provide mandated transportation services under their children's IEPs.

**September 21** — Reconciliation of the restored dataset against active enrollment is completed and independently verified by both Transportation and Technology staff. This marks the close of the acute incident phase for purposes of this postmortem.

---

## 4. Root Cause

**The root cause of this incident is an unassigned process ownership gap created during the transition from the incumbent transportation contractor's operating model to the new operator and platform.**

Under the prior contractor, post-import data reconciliation — comparing the count and content of records submitted for import against the count and content of records successfully loaded into the routing system — was performed by a specific role within the contractor's own operations team, as a condition of their service agreement. This function was not a formal, documented control owned by the district; it existed inside a vendor relationship the district did not fully map when designing its own operating model for the transition.

When the district built its new runbook for the 2026–27 launch, it carried forward many procedural steps from the prior arrangement but did not identify that data reconciliation had previously been performed by the outgoing contractor rather than by the district itself. The new runbook created a "Transportation Data Coordinator" role intended to absorb this and similar functions, but the position was never filled before opening, and no interim owner was designated. The result was a control that existed on paper (the validation report was generated automatically by Trailhead on every import) but had no owner in practice. A report that no one is assigned to read is not a control; it is a document.

This ownership gap converted what should have been a same-day, low-severity data-quality catch — a record-count mismatch of roughly 16%, which any reconciliation step would have caught immediately — into a 16-day-old, undetected defect that shaped route-building, staffing assumptions, and the operational narrative of the launch itself. Because the missing 1,340 students were never in the routed dataset, no route existed for them to fail; their absence looked, to anyone not specifically checking total counts, like normal attrition or late registration rather than a systemic defect. This is why the failure was not caught by ordinary route-quality review before opening day.

The same root cause — a control that exists in documentation but has no assigned human owner — recurs in a secondary form in the hand-written route sheet practice on September 8 and 9. Trailhead's platform is capable of enforcing tier separation automatically as part of route generation. When staff reverted to manual, paper-based dispatch to work around the data gap, they did so without a corresponding manual control to preserve tier separation, because no one owned the responsibility of translating that automated safeguard into the manual process it was temporarily replacing.

---

## 5. Contributing Factors

The root cause above explains why a data defect went undetected. The following factors explain why the defect's consequences were as severe as they were, and why detection and recovery took as long as they did.

**1. Compressed procurement-to-launch timeline.** Eight weeks between contract award and opening day left no meaningful contingency for parallel-run testing, in which the new platform's routing output could have been validated against the prior year's known-good route assignments before go-live. Industry and the district's own prior transitions typically allow four to five months for this kind of changeover. The compressed timeline did not cause the data defect, but it foreclosed nearly every opportunity to catch it before students were affected.

**2. No go-live data-quality gate.** Trailhead's import pipeline treats field-length violations as silent exclusions rather than hard failures requiring resolution before the import can be marked complete. The platform generated the information needed to catch the problem (the validation report) but did not require any human sign-off before that data was used to build live routes. A formal go/no-go checkpoint tied to a reconciled record count did not exist in the launch plan.

**3. Institutional-knowledge loss from the contractor transition.** The incumbent contractor's departure removed staff who had handled address data, apartment-unit formatting conventions, and known data-quality issues for years. That knowledge — including awareness that the district's housing stock includes a significant number of multi-unit buildings with long unit designations — was not systematically transferred to the new operator or captured in the new platform's configuration.

**4. Confirmation bias toward a known, real problem.** The driver shortage was genuine, visible, and already a subject of department attention before opening day. When delays began, this pre-existing and well-understood explanation was the path of least resistance, and it did not require anyone to question whether the underlying data was correct. A real problem crowded out investigation of a coexisting, hidden one. The shortage explained why some routes might run late; it did not explain why 1,340 students had no route at all, but this distinction was not examined until Wednesday evening.

**5. Absence of a routine reconciliation cadence.** Even after the launch, no daily or weekly practice existed of comparing SIS enrollment counts to Trailhead's routed-student counts. This is the same control gap as the root cause, but its absence as an ongoing practice — not just a one-time go-live gate — meant the discrepancy could have persisted indefinitely had Wednesday's ad hoc review not occurred.

**6. Manual workarounds without compensating controls.** The shift to hand-written route sheets was a reasonable, good-faith response to visibly incomplete Trailhead data. However, it removed the platform's built-in tier-separation logic without replacing it with any manual equivalent (color-coded sheets, separate yard staging areas, or a checklist step), which is why Wednesday's delays exceeded Tuesday's despite additional staff effort.

**7. Delayed escalation structure.** No formal incident command or cross-departmental escalation process existed for the first day and a half of visible failure. Departments worked their individual pieces of the problem — Transportation on staffing, Special Services on individual family inquiries, Technology on platform support tickets — without a shared, elevated view of the total pattern until the Superintendent convened the command post on Wednesday evening, roughly 36 hours after the first district-wide missed pickups on September 8, and six days after the very first missed pickup during the September 3 soft-open.

**8. Soft-open signal not escalated.** The missed pickups on September 3–4 during the early childhood and special-education soft-open were the earliest concrete evidence of the address-import defect, four to five days before the full opening. These were handled as individual family service issues by school-level and Special Services staff rather than flagged to Technology or Transportation leadership as a possible systemic data problem, losing a window in which the defect could have been caught and corrected before the far larger September 8 opening.

---

## 6. Response Analysis: What Worked and What Did Not

### What Worked

**The crossing guard's intervention on September 8.** A trained adult recognized a child was out of place and did not release her to walk unsupervised, instead holding her and notifying both the school and dispatch. This was a manual, human safety control operating correctly precisely where automated systems had failed, and it prevented the incident from becoming materially worse.

**Command post activation, once triggered, consolidated the response.** Once Superintendent Adeyemi convened department heads on Wednesday evening, the district moved from fragmented, department-by-department problem-solving to a coordinated structure that produced same-week results: a corrected data import, restored tiered routing, and contracted van service for the 41 IEP students, all within roughly 48 hours of the command post's formation.

**Special Services moved quickly once the affected population was identified.** From the moment the 41 students were identified as a discrete, named group on Wednesday evening, Marisela Duarte's office secured contracted van service within one business day, restoring mandated transportation for this population faster than the general-population routing was fully stabilized.

**Financial authority was available and used without delay.** Business Administrator Gerald Ostrowski's approval of $214,000 in emergency funding was not itself a source of delay in the response; funding followed the operational decision to contract van service rather than gating it.

**The underlying data infrastructure, once corrected, held.** The September 10 re-import and subsequent September 21 reconciliation confirmed that the defect was a discrete, fixable schema issue rather than a broader platform failure. Trailhead's routing logic performed as designed once given complete data, which is evidenced by the absence of further tier-collision incidents after tiered route sheets were restored on September 10.

### What Did Not Work

**No one owned the validation report.** This is the central failure of the incident. A system generated the exact information needed to prevent this outcome, on the first day it was relevant, and no person or role was accountable for acting on it. This gap persisted for 16 days.

**The driver-shortage explanation was accepted without verification against the data.** Attributing Tuesday's delays to staffing was a reasonable initial hypothesis but was never tested against available information — specifically, the route count and student count discrepancy that Trailhead's own validation report could have surfaced immediately. No one asked "does the number of missing or delayed students match what a 14-driver shortfall would predict?" before the explanation was adopted and communicated.

**The soft-open missed pickups were not escalated as a systemic signal.** The September 3–4 missed pickups for early childhood and special-education students were the earliest available evidence of the defect and were treated as isolated case management issues rather than routed to Technology or Transportation leadership as a possible platform or data problem.

**Manual workarounds lacked compensating controls.** Hand-written route sheets solved the immediate problem of incomplete Trailhead data but introduced a new, entirely preventable failure mode — tier collisions — because the manual process did not replicate a safeguard the automated system would have provided.

**Escalation to a unified command structure took too long.** More than a day and a half elapsed between the first district-wide evidence of systemic failure (the morning of September 8) and the formation of a coordinated cross-departmental response (the evening of September 9). During that window, departments worked in parallel on different pieces of the same problem without a shared operating picture.

**Communications capacity was not sized for the failure mode.** 3,100 calls in a single day on September 9 overwhelmed front-line staff at all 14 schools and the district office, indicating no surge communication plan (a dedicated hotline, a proactive districtwide notification, or a triage script) existed for a transportation-specific crisis of this scale.

**The transition plan did not map functions performed by the outgoing contractor that the district needed to explicitly re-own.** The most consequential single planning gap was the failure to recognize, during the eight-week transition, that a critical data-quality function had been performed informally by the outgoing vendor and needed to be deliberately reassigned rather than assumed to carry forward.

---

## 7. Action Items

The following actions are organized by the system or process they address. Each has a named owner and a due date. Items marked **(Board)** require Board of Education notification or approval as a condition of funding or policy change.

| # | Action Item | Owner | Due Date |
|---|---|---|---|
| 1 | Formally fill the Transportation Data Coordinator role, with explicit written accountability for reconciling every Trailhead import against source SIS record counts before any route is built on new data. | Bethany Kwan, Chief Technology Officer | September 30, 2026 |
| 2 | Configure Trailhead's import pipeline to reject, rather than silently exclude, any record that fails field-length or schema validation; require a zero-discrepancy or explicitly reviewed-and-approved record count before an import can be used for route generation. | Priya Nandakumar, Director of Information Systems (with Trailhead vendor account team) | September 25, 2026 |
| 3 | Establish a standing weekly reconciliation of SIS enrollment/eligibility counts against Trailhead routed-student counts for the remainder of the 2026–27 school year, with discrepancies over 1% escalated same-day to the CTO and Transportation Director. | Bethany Kwan, Chief Technology Officer | Recurring, beginning October 1, 2026 |
| 4 | Conduct a full audit of all students flagged in IEPs or 504 plans as requiring door-to-door or specialized transportation, cross-referenced against current Trailhead route assignments, with written confirmation of correct routing for each student. | Marisela Duarte, Supervisor of Special Services | September 15, 2026 (complete) |
| 5 | Establish a documented escalation protocol requiring any missed pickup or transportation service failure involving a student with an IEP-mandated transportation provision to be reported to Special Services leadership and Technology leadership within 24 hours, regardless of how isolated the initial report appears. | Marisela Duarte, Supervisor of Special Services | September 20, 2026 (complete) |
| 6 | Draft and file the district's written response to the two pending New Jersey Department of Education complaints, including a remediation and compensatory-services plan for affected families. | Dr. Ifeoma Adeyemi, Superintendent, with district legal counsel | October 15, 2026 |
| 7 | Complete driver recruitment to close the 14-position gap, with monthly hiring progress reported to Cabinet; in the interim, formalize route-consolidation and overtime protocols that do not require deviation from Trailhead-generated, tier-separated route sheets. | Rudolph Sciarra, Transportation Director, with Antonio Colón, Director of Human Resources | Full staffing by November 30, 2026; interim protocol in place by September 18, 2026 (complete) |
| 8 | Formalize a policy prohibiting hand-written or otherwise manually generated route sheets from being issued without an explicit tier-assignment field, and require supervisor sign-off confirming tier separation before any manual route sheet is distributed at the yard. | Rudolph Sciarra, Transportation Director | September 22, 2026 (complete) |
| 9 | Establish a formal Incident Command protocol for operational disruptions affecting more than 10% of transported students or any safety event, defining automatic activation triggers, cross-departmental roles, and a maximum time-to-activation target of 4 hours from confirmed systemic pattern detection. **(Board)** | Dr. Ifeoma Adeyemi, Superintendent | October 20, 2026 |
| 10 | Design and resource a surge communications plan for transportation-related disruptions, including a dedicated overflow phone line, proactive district-wide notification templates, and front-desk triage scripts for all 14 schools. | Director of Communications, with Dr. Ifeoma Adeyemi, Superintendent | October 31, 2026 |
| 11 | Complete a formal transition-mapping exercise documenting every function previously performed informally by an outgoing vendor or contractor, for use in any future procurement transition, and incorporate this mapping requirement into district procurement policy. **(Board)** | Gerald Ostrowski, Business Administrator | November 15, 2026 |
| 12 | Conduct a post-implementation financial review of the $214,000 in emergency remediation spending and present findings, including any recoverable costs from the Trailhead vendor relationship, to the Board. **(Board)** | Gerald Ostrowski, Business Administrator | October 5, 2026 |
| 13 | Present this postmortem, along with a 30-, 60-, and 90-day status update on all action items above, to the Board of Education in public session. **(Board)** | Dr. Ifeoma Adeyemi, Superintendent | September 22, 2026 (initial presentation, complete); 30/60/90-day updates on October 20, November 24, and December 22, 2026 |

---

## 8. Closing Note

The failures of September 8 were not the result of any single decision made in bad faith or any single person's negligence. They were the product of a compressed timeline, an inherited process that did not survive a vendor transition intact, a validation step that existed in a system but not in anyone's job description, and a set of individually reasonable responses — trusting a known driver shortage, reverting to manual dispatch when software data looked wrong — that combined without the compensating controls each would have needed to succeed independently. The corrective actions above are designed to close the specific gaps this incident exposed: unowned data controls, an escalation structure that activates too slowly, and a transition process that does not force explicit reassignment of functions a departing vendor was quietly performing. The district's obligation now is to verify, not merely document, that each of these gaps has been closed before they are tested again by ordinary operating conditions rather than by a crisis.

## Appendix A: Compressed Procurement Timeline — Detailed Reconstruction

The eight-week window between contract award and opening day is referenced throughout this postmortem as a contributing factor. This appendix reconstructs that window in greater detail to inform the transition-mapping policy directed in Action Item 11.

**June 9 – June 15 (Week 1).** Contract award to new transportation operator. Immediate priorities were fleet insertion (vehicle inspection, registration transfer, and depot logistics) and driver roster transfer discussions, which did not result in a meaningful transfer of drivers from the incumbent contractor; only 6 of the incumbent's approximately 98 drivers accepted employment with the new operator, contributing directly to the 14-position gap at opening.

**June 15 – June 22 (Week 2).** Platform selection. Trailhead was chosen over two competing routing platforms based on cost, a compressed implementation timeline promised by the vendor, and referenceable district partners. The selection process did not include a formal data-migration risk assessment as part of vendor evaluation; this is addressed in Action Item 2's requirement for hard-failure validation and should be incorporated into future procurement scoring criteria under Action Item 11.

**June 22 – July 13 (Weeks 3–5).** Platform configuration and staff onboarding. District IT staff, working with the Trailhead implementation team, configured school calendars, bell schedules, bus stop libraries, and driver/vehicle records. Configuration work during this period did not include a parallel-run comparison against the prior year's finalized routes, which would have required maintaining read access to the incumbent contractor's legacy routing system — access that lapsed at contract termination and was not preserved by agreement.

**July 13 – August 3 (Weeks 6–8).** Driver recruitment intensifies under the new operator; district and operator jointly conduct two hiring events. Student data migration planning begins but is scheduled late in the window relative to the September 8 opening, leaving a single planned import date (August 24) rather than an iterative import-and-validate cycle with multiple checkpoints.

**August 3 – September 8 (Final five weeks).** Final configuration, the August 24 import, staff training on Trailhead's dispatch interface, and the September 3–4 soft-open. No formal go/no-go readiness review involving Cabinet-level sign-off occurred between the August 24 import and the September 8 opening.

This reconstruction indicates that the compressed timeline was not uniformly compressed — the heaviest data-quality risk (the single, late, unvalidated import) fell in the final two weeks before opening, when schedule pressure to finalize routes was at its highest and tolerance for discovering a major data problem was at its lowest. Future transitions conducted under similarly compressed timelines should front-load data migration to allow at least two full validation-and-correction cycles before any route-building begins, even if this requires delaying platform configuration or driver-facing training to a later point in the sequence.

## Appendix B: Technical Detail — The Field-Length Defect

For the benefit of future implementation teams, this appendix documents the specific technical mechanism of the August 24 failure.

The district's student information system stores residential addresses in discrete fields, including a free-text "Address Line 2" field used for apartment, unit, floor, and building designations. This field in the SIS permits up to 50 characters. Trailhead's standard import template, as configured for the district by the vendor's implementation team, mapped this field to a routing-address subfield with a 30-character limit, a default inherited from the platform's out-of-the-box configuration and not adjusted during the June–August configuration period.

Of the district's 8,460 active student address records at the time of the August 24 import, 1,340 contained Address Line 2 values exceeding 30 characters — disproportionately concentrated among students residing in a small number of large multi-unit apartment complexes in the district's more densely populated municipalities, where unit designations commonly include building letter, floor number, and unit number in a single field (for example, "Building C, 3rd Floor, Unit 314, Mailbox 27").

Rather than rejecting these records or flagging them as requiring manual correction, the import pipeline truncated evaluation of any record exceeding the field limit and, per its default error-handling configuration, excluded the record from the successful-import set entirely rather than importing a truncated address. This behavior is standard and documented in Trailhead's technical specifications, but it was not identified as a district-specific risk during configuration, because no test import using a representative sample of the district's actual address data — as opposed to sample or default test data — was performed before the August 24 production import.

The corrective configuration implemented on September 10 increased the mapped field limit to 100 characters and added a secondary validation rule requiring manual review and correction, rather than silent exclusion, for any record still exceeding that expanded limit. As of September 21, zero records required manual review under the new threshold, confirming the expanded field length resolved the defect for the district's current address data profile.

## Appendix C: Distribution and Acknowledgment Log

This postmortem was distributed to the following parties for review and acknowledgment prior to public Board presentation. Acknowledgment indicates review of the factual record and action items, not agreement with every characterization in the narrative sections.

| Reviewer | Role | Date Reviewed |
|---|---|---|
| Dr. Ifeoma Adeyemi | Superintendent | September 21, 2026 |
| Bethany Kwan | Chief Technology Officer | September 21, 2026 |
| Rudolph Sciarra | Transportation Director | September 21, 2026 |
| Marisela Duarte | Supervisor of Special Services | September 20, 2026 |
| Gerald Ostrowski | Business Administrator | September 21, 2026 |
| District Legal Counsel | — | September 19, 2026 |
| Trailhead Implementation Lead (vendor) | — | September 18, 2026 |

## Appendix D: Glossary

**Import (data import):** The scheduled or on-demand transfer of student address, enrollment, and eligibility data from the district's student information system into Trailhead for the purpose of generating bus routes.

**Reconciliation:** The act of comparing the count and content of records submitted for import against the count and content of records successfully loaded, to confirm no data was lost or altered in transfer.

**Tier:** A scheduling category (elementary, middle, or high school) used to stagger bus routes so that a single vehicle and driver can serve multiple schools with different start times without schedule conflicts.

**Go/no-go gate:** A formal checkpoint requiring explicit sign-off that a defined set of readiness conditions has been met before a system or process is permitted to move to the next phase — in this context, before a data import is used to build live, dispatched routes.

**Door-to-door transportation:** A transportation service level, typically mandated by a student's IEP, in which the bus stop is located at or immediately adjacent to the student's residence rather than at a shared neighborhood stop, and often requires a driver or aide to escort the student between the vehicle and the residence.

**Soft-open:** A limited, phased start to the school year for a subset of students or programs, conducted prior to the full district-wide opening, used to identify operational issues at lower volume before they affect the entire transported population.
