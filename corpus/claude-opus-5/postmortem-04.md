# Incident Postmortem: September 2026 Transportation Service Failure

**Willow Brook Public Schools**
**Prepared for the Board of Education, Office of the Superintendent, and Department of Transportation Services**
**Document status: Final**
**Date of issue: October 12, 2026**
**Incident window: September 8–17, 2026**
**Classification: Severity 1 — Districtwide service failure with mandated-service noncompliance**

---

## 1. Summary

Willow Brook Public Schools opened the 2026–2027 academic year on September 8 with a transportation system that could not deliver students to school reliably. Sixty-two of 112 routes ran late on the first day by an average of 47 minutes. Nine buses never arrived at any stop. A kindergarten student was released from a bus 1.2 miles from the student's home address and was returned to a school building only after a municipal crossing guard recognized that the child was unaccompanied and unable to state a destination.

The proximate cause was a data defect. A student address import executed on August 24 dropped 1,340 records without raising a blocking error. The dropped records shared a single characteristic: an apartment or unit field whose character length exceeded the destination field in the Trailhead routing platform. The import job wrote these rejections to a validation report, and the validation report generated on schedule. No person opened it. The reconciliation step that would have caught the discrepancy existed as a named task with a named owner in the transportation runbook used under the prior contractor. It did not appear in the runbook assembled for the new operator and the new platform. The task was not reassigned, deferred, or waived. It ceased to exist as a unit of accountable work.

Forty-one of the 1,340 dropped students carry individualized education programs that mandate door-to-door transportation. Those students had no route, no stop, and no vehicle assigned on the first day of school. They remained without district-provided mandated service for four school days.

The response compounded the failure before it corrected it. For the first two days, the operating assumption held by both the Transportation Director and the Chief Technology Officer was that the delays reflected the district's driver shortage — a genuine condition, with 14 driver positions open against an authorized complement of 126. That assumption was plausible, was partially supported by the observable evidence, and was wrong as an explanation for the magnitude and pattern of what occurred. It directed the response toward staffing mitigation rather than data reconciliation for approximately 60 hours. During that period, hand-written route sheets issued to drivers at the yard on Tuesday morning and Wednesday morning omitted tier assignments. Elementary and secondary runs that had been designed to operate in sequence instead operated simultaneously, and average delay on Tuesday rose to 63 minutes — worse than day one.

The failure resolved through a combination of correct diagnosis on Wednesday evening, a command post structure stood up by the Superintendent that consolidated decision authority, and a contracted-van arrangement for the 41 mandated-service students that began Thursday, September 17, at an approved cost of $214,000.

This document examines the systems and decisions that produced the outcome. It does not assign fault to individuals. The people named in this report acted within the information available to them, under a compressed timeline that the district itself created, using a runbook that the district itself failed to validate. Where this report identifies a decision as incorrect, it identifies the conditions that made the incorrect decision reasonable at the time it was made. The purpose is to change those conditions.

---

## 2. Impact

### 2.1 Service impact

| Measure | Value |
|---|---|
| Students transported daily (design) | 5,600 |
| Routes in operation | 112 |
| Routes late on September 8 | 62 |
| Average delay, September 8 | 47 minutes |
| Average delay, September 9 | 63 minutes |
| Buses that never arrived, September 8 | 9 |
| Student address records dropped in import | 1,340 |
| Dropped records with mandated door-to-door IEP service | 41 |
| School days of mandated-service gap | 4 |
| Students released at an incorrect location | 1 |

### 2.2 Instructional impact

Eight hundred ninety students were recorded absent or tardy for transportation-attributable reasons during the week of September 8. At the district's 9,800-student enrollment, that represents 9.1 percent of all students and 15.9 percent of the transported population. Instructional minutes lost are not precisely recoverable from attendance records, but at an average tardy of 47 to 63 minutes and a first-period length of 52 minutes, the district estimates that the majority of the 890 affected students lost at least one full instructional period, and a substantial minority lost more.

Four schools — Willow Brook High School, Cedar Ridge Middle School, Marshfield Elementary, and Northgate Elementary — held first period as a supervised study block on September 9 and 10 because instructional continuity was not achievable with arrival times spread across 60-plus minutes.

### 2.3 Operational impact

The district logged 3,100 parent contacts on September 9 alone through the central office line, school main offices, and the transportation office. Peak concurrent hold time on the central line reached 41 minutes. Fourteen central office staff were reassigned from their regular duties to phone coverage for portions of September 9 through September 11, including staff from Curriculum, Human Resources, and Facilities.

School-based staff absorbed unplanned supervision duty for students arriving off-schedule and for students whose buses did not arrive for dismissal. Building principals reported that between 30 and 90 minutes of administrative time per day per building was consumed by transportation triage during the incident window.

### 2.4 Compliance and legal impact

Two complaints were filed with the New Jersey Department of Education regarding failure to provide transportation services mandated by individualized education programs. Both complaints relate to the 41-student cohort. Both are pending as of this document's issue date. The district has retained counsel and has initiated a compensatory-services review for all 41 students under the direction of the Supervisor of Special Services.

The district's obligation under N.J.A.C. 6A:14 to provide transportation as specified in an IEP is not conditioned on operational difficulty, contractor transition, or system implementation. A four-school-day gap in mandated service is a gap in mandated service.

### 2.5 Financial impact

| Item | Amount |
|---|---|
| Contracted van service, 41 students (approved September 16) | $214,000 |
| Emergency overtime, transportation and central office (Sept 8–17) | $47,300 |
| Contracted driver premium, operator pass-through | $61,800 |
| Estimated total direct incident cost | $323,100 |

The $214,000 van authorization covers the period from September 17 through the end of the first semester. It does not include compensatory services, which are not yet scoped, or any costs associated with the two state complaints.

### 2.6 Trust impact

Trust impact does not reduce to a number, and the district should resist the temptation to treat it as resolved when the routes run on time. A kindergarten student was released alone, more than a mile from home, on the first day of school. Every family in the transported population learned that this was possible. The recovery of confidence will run on a longer timeline than the recovery of service, and the action items in Section 8 reflect that.

---

## 3. Timeline

All times are Eastern. Times are drawn from system logs, the Trailhead audit trail, dispatch recordings, the central office call system, and interviews conducted between September 21 and October 3. Where a time is approximate, it is marked.

### Phase 1 — Procurement and transition (June 12 – August 23)

**June 12, 2026, 7:40 p.m.** — Board of Education awards the pupil transportation contract to a new operator following a competitive bid. The incumbent, which had held the contract for eleven years, is not selected. Contract start date is set at July 1, with full service required September 8. Elapsed time from award to service: 88 calendar days, of which 58 are business days.

**June 15–30** — Transition planning begins. The district and the new operator identify that the incumbent's proprietary routing system will not transfer. The district selects Trailhead, a cloud routing platform, on June 26. Implementation timeline is set at six weeks against a vendor-recommended twelve.

**July 6** — Trailhead implementation kickoff. The vendor's standard implementation includes a two-week data validation phase. The district and vendor agree to compress this to four days to preserve the September 8 date.

**July 13 – August 7** — Route design in Trailhead using prior-year address data. Tier structure defined: Tier 1 secondary (high school), Tier 2 middle, Tier 3 elementary. Tier assignment is a required field on every route object in Trailhead and drives the sequencing of vehicle reuse across the three bell schedules.

**August 10** — Transportation runbook v1 issued for the new operator. The runbook is assembled by the Transportation Director's office from the prior runbook, the operator's standard operating procedures, and Trailhead vendor documentation. It runs 61 pages. The prior runbook ran 94.

**August 14** — Runbook v1 reviewed in a joint meeting of Transportation, Technology, and the operator's general manager. The review is scoped to "operational readiness." Data procedures are not on the agenda. No participant identifies that the address reconciliation step present in the prior runbook (section 7.3, "Post-Import Count Verification," owned by the Transportation Data Coordinator) does not appear in v1. The Transportation Data Coordinator position had been eliminated in the FY2026 budget and its duties distributed; the elimination is not reflected in any runbook ownership map.

**August 21** — Student information system freeze for the annual rollover. Address data of record is locked for import.

### Phase 2 — The defect is created (August 24)

**August 24, 2:14 a.m.** — Scheduled address import job runs, moving 5,612 student address records from the student information system into Trailhead.

**August 24, 2:31 a.m.** — Import completes. Job status: **Completed with warnings**. Records written: 4,272. Records rejected: 1,340. Rejection reason for all 1,340: destination field `unit_designator` maximum length 12 characters; source value exceeds maximum. Trailhead's default behavior for field-length violations on non-required fields is row rejection with a warning-level log entry, not a job failure.

**August 24, 2:31 a.m.** — Validation report `IMP-0824-ADDR` generates and is deposited in the Trailhead reports directory. The report's first page carries the line: *Records rejected: 1,340. Review required before route publication.*

**August 24, 8:00 a.m. – August 26** — The report is not opened. Trailhead's audit trail confirms zero views of `IMP-0824-ADDR` between generation and September 16. No automated alert was configured for warning-level import outcomes; alerting was scoped during implementation to error-level events only, a scoping decision made during the compressed four-day validation phase.

**August 26 – September 4** — Route publication proceeds against 4,272 addresses. Trailhead's route builder does not flag the 1,340 missing students, because from the platform's perspective those students do not exist. Route counts, vehicle counts, and seat utilization all compute correctly against the smaller population. Utilization actually improves relative to the prior year, which is noted approvingly in an internal readiness memo on September 2 as evidence of route optimization.

**September 3** — Route letters mail to families. Families of the 1,340 receive no letter. Central office logs 47 calls between September 3 and September 5 from families reporting no route assignment. These are handled individually as new-enrollment or data-entry exceptions and manually added where the caller followed through. Nineteen of the 47 are resolved this way. No one aggregates the call volume or asks why 47 families are missing at once.

### Phase 3 — Day one (September 8)

**5:12 a.m.** — First yard report. Nine drivers are absent without replacement. Dispatch begins doubling routes.

**6:35 a.m.** — First late-arrival reports from Willow Brook High School. Tier 1 runs are 20 to 35 minutes behind.

**7:10 a.m.** — Central office call line opens. Volume immediately exceeds two-person staffing.

**7:48 a.m.** — Transportation Director Rudolph Sciarra briefs the Superintendent's office by phone. Assessment: driver shortage plus first-day traffic. Expected to normalize by day three. This assessment is consistent with the district's experience in prior years and with the 14 documented open positions.

**8:15 a.m. – 9:40 a.m.** — Tier 3 elementary runs cascade. Buses returning late from Tier 1 and Tier 2 cannot begin Tier 3 on schedule. Sixty-two routes ultimately record late arrival.

**9:52 a.m.** — Marshfield Elementary reports a kindergarten student unaccounted for on the arrival manifest. The student is not at school and is not at home.

**10:07 a.m.** — Municipal crossing guard at Route 27 and Hollins Avenue reports an unaccompanied kindergarten-age child. The child had been released at a stop 1.2 miles from the home address. The guard walks the child to the Hollins Avenue municipal building and contacts the district.

**10:31 a.m.** — Student is confirmed safe and transported to Marshfield Elementary. Family is contacted by the principal.

**10:31 a.m.** — Root cause of the misrouting is recorded in the incident log as "driver unfamiliar with route." The driver was in fact operating a doubled route without the student's stop on the manifest; the student boarded at a stop that was on the manifest and was released at the nearest listed stop to the driver's best understanding of the address. The address the driver needed was among the 1,340.

**1:15 p.m.** — Special Services begins receiving calls from families of students with door-to-door mandates. By end of day, 23 such calls are logged. Supervisor of Special Services Marisela Duarte requests route confirmations from Transportation for the affected students.

**4:50 p.m.** — Afternoon dismissal runs late across 58 routes. Nine schools hold students past 5:00 p.m.

**6:30 p.m.** — Evening call between Sciarra and Chief Technology Officer Bethany Kwan. Topic is driver coverage for day two. Data integrity is not discussed. Neither participant has cause to raise it: the platform reported no errors, the route counts looked correct, and the visible failure mode — buses late, buses missing — matched a staffing explanation.

### Phase 4 — The response worsens the incident (September 9)

**4:45 a.m.** — Dispatch determines that Trailhead's published route sheets cannot be regenerated in time to reflect overnight doubling decisions. Supervisors write route sheets by hand at the yard.

**5:30 a.m. – 6:15 a.m.** — Hand-written sheets are distributed. The sheets carry stop lists and times. **They do not carry tier designations.** The hand-written format was improvised; no template existed in the runbook for manual route issuance, because under the prior contractor manual issuance had been rare and had used a pre-printed form that included a tier field.

**6:20 a.m. onward** — Drivers without tier designations begin runs in the order the stops are listed. Elementary and high school runs that were designed to be sequential are executed concurrently. Vehicles are not available for their second and third assignments. The cascade is now structural rather than incidental.

**8:00 a.m. – 10:00 a.m.** — Average delay reaches **63 minutes**, exceeding day one. Twelve routes are more than 90 minutes late.

**9:00 a.m. – 5:00 p.m.** — Central office logs **3,100 parent calls**. Fourteen staff are pulled to phones.

**11:20 a.m.** — Duarte escalates in writing to the Superintendent and the Business Administrator: at least 30 students with door-to-door mandates have received no service in two days. This is the first written escalation that frames the problem as a service-eligibility issue rather than a service-timeliness issue.

**2:00 p.m.** — Transportation adds four contracted spare vehicles for day three. The mitigation remains staffing-focused.

**7:15 p.m.** — Superintendent Dr. Ifeoma Adeyemi convenes an evening call and directs that a command post open the following morning.

### Phase 5 — Detection (September 10)

**6:00 a.m.** — Command post opens in the central office board room. Standing membership: Superintendent, Business Administrator Gerald Ostrowski, CTO Kwan, Transportation Director Sciarra, Supervisor of Special Services Duarte, Director of Communications, and the operator's general manager. Cadence: 6:00 a.m., 11:00 a.m., 4:00 p.m.

**6:00 a.m.** — Hand-written sheets are issued again for a second day, still without tier designations. The command post's first meeting does not surface the tier omission because no one present has seen a hand-written sheet.

**8:00 a.m. – 10:00 a.m.** — Delays remain above 55 minutes. Adeyemi asks a question that redirects the investigation: *if the shortage is 14 drivers out of 126, why are 62 routes failing?* The arithmetic does not support the diagnosis. Eleven percent of drivers cannot produce 55 percent route failure without a second factor.

**11:00 a.m. briefing** — Kwan takes the action item to reconcile the transported-student count in Trailhead against the student information system.

**4:00 p.m. briefing** — Duarte reports the confirmed door-to-door cohort at 41 students, established by cross-referencing IEP transportation mandates against Trailhead route assignments manually.

**6:40 p.m.** — Kwan runs the comparison. Trailhead: 4,272 student address records. Student information system: 5,612. **Variance: 1,340.**

**7:05 p.m.** — Kwan opens `IMP-0824-ADDR` for the first time. The report has been sitting in the reports directory for seventeen days and names the defect on page one.

**7:30 p.m.** — Kwan notifies the Superintendent, the Transportation Director, and the operator. The incident is reclassified from a staffing failure to a data failure with a staffing complication.

### Phase 6 — Correction (September 11 – 17)

**September 11, 12:30 a.m.** — Trailhead vendor engaged on emergency support. Field length for `unit_designator` extended from 12 to 40 characters.

**September 11, 3:15 a.m.** — Corrected import runs. Records written: 5,612. Records rejected: 0.

**September 11, 4:00 a.m. – September 12** — Route rebuild against the full population. Rebuild requires 31 hours because route geometry, not just stop assignment, changes when 1,340 addresses re-enter the model.

**September 11, 6:00 a.m.** — Tier omission on hand-written sheets is identified at the command post when a supervisor brings a physical sheet to the briefing. A tier field is added to the manual template immediately. Delay drops to 38 minutes on September 11.

**September 14 (Monday), 5:00 a.m.** — First runs on rebuilt routes. Average delay: 19 minutes. Zero missed buses.

**September 15** — Average delay 11 minutes. Call volume returns to 210, within normal first-week range.

**September 16, 2:00 p.m.** — Ostrowski approves **$214,000** for contracted van service for the 41 mandated-service students, using emergency procurement authority with ratification scheduled for the October board meeting.

**September 17 (Thursday), 6:30 a.m.** — Contracted vans begin service for all 41 students. This is **four school days** after the first missed pickup on September 8.

**September 17, 4:00 p.m.** — Command post moves to daily single briefing.

**September 21** — Average delay 6 minutes, within the district's 10-minute operational standard. Command post closes. Postmortem process begins.

---

## 4. Root Cause

**The address import of August 24 rejected 1,340 student records for field-length violation, wrote the rejection to a validation report, and completed with a warning rather than an error. The reconciliation step that would have detected the rejection had been removed from the operational runbook during the transition and was not reassigned to any role. The defect therefore had no owner, and an unowned defect in a system that reports warnings quietly is a defect that will not be found.**

Three properties of this failure deserve separate statement, because each is independently correctable.

**The system failed quietly.** Trailhead treated a 24 percent data loss as a warning. This is a defensible platform default — field-length rejection on a non-required subfield is ordinarily a minor exception — but it was catastrophically wrong for this transaction. The district configured alerting for error-level events only, a decision made in a compressed four-day window that replaced a two-week validation phase. No one asked what the platform considered non-critical, and the platform's answer included "one quarter of your students."

**The check was deleted rather than reassigned.** Section 7.3 of the prior runbook, "Post-Import Count Verification," was owned by a Transportation Data Coordinator. That position was eliminated in the FY2026 budget and its duties were described as "distributed." No document recorded where each duty went. When runbook v1 was assembled in August, the section was not carried forward. This was not a decision to accept the risk. It was the absence of a decision. The controls inventory was never reconciled against the position elimination, so the district had no way to know it was operating without a control it believed it had.

**The runbook review was scoped to exclude the failure.** The August 14 review examined operational readiness — vehicles, drivers, radios, yard procedures. Data procedures were out of scope. A review that cannot find a missing data control is not a defective review; it is a review pointed at the wrong target. The district had no readiness gate that asked *what verification steps existed last year that do not exist this year?*

Underneath all three sits the compressed timeline. Eighty-eight days from contract award to full service, with a six-week platform implementation against a twelve-week recommendation and a four-day validation phase against a two-week recommendation, does not create defects on its own. It removes the slack in which defects are normally caught. Every shortcut taken between June and August was individually reasonable and defensible against the September 8 deadline. Collectively they eliminated the district's capacity to discover its own errors.

---

## 5. Contributing Factors

**5.1 The procurement calendar left no schedule reserve.** A June 12 award for September 8 service, with a platform replacement inside it, is a schedule with zero float. Any defect discovered late would be discovered in production. The award timing was driven by bid protest windows and board meeting calendars, not by transition requirements. The district never modeled the transition duration before committing to the award date.

**5.2 Vendor-recommended validation was treated as negotiable.** The twelve-week implementation and two-week validation phase were vendor defaults derived from prior implementations. Compressing them was framed internally as an aggressive but achievable schedule. There is no record of anyone asking what the validation phase was designed to catch, or what the district would be blind to without it. The compression was a schedule decision that silently became a risk decision.

**5.3 Position elimination without controls reconciliation.** The Transportation Data Coordinator role was eliminated for budget reasons in FY2026. The controls that role executed were not inventoried, assigned, or automated. This is a general pattern risk: the district has no requirement that position eliminations be accompanied by a control-transfer memo.

**5.4 Alerting was scoped to errors, not to warnings.** Trailhead's warning-level events include row rejection, geocode failure, and duplicate suppression — three categories that describe silent data loss. None generated a notification. The scoping was done under time pressure by staff configuring many settings quickly.

**5.5 Improved utilization metrics masked the loss.** With 1,340 students removed, seat utilization improved and appeared in the September 2 readiness memo as a positive indicator. A metric that improves when data disappears is a metric that will conceal data disappearance. The district had no denominator check — no dashboard element comparing transported-student count to enrollment.

**5.6 Early signals were handled as individual exceptions.** Forty-seven families called between September 3 and 5 reporting no route assignment. Each was handled as a discrete ticket. Nineteen were resolved individually, which is to say nineteen instances of the defect were manually patched without anyone recognizing a pattern. The service desk had no threshold rule that escalates a repeated symptom to problem investigation.

**5.7 A real problem provided a sufficient-seeming explanation.** Fourteen open driver positions is a genuine and serious shortage. It explained the nine missing buses well. It explained 62 late routes poorly, but the poor fit was not tested until September 10 because the shortage was visible, familiar, and already the subject of an active remediation effort. Availability of a known cause suppressed search for an unknown one. This is not an individual failing; it is a predictable feature of diagnosis under load, and the countermeasure is procedural, not personal.

**5.8 No standing rule required data verification during service incidents.** The district's incident procedure had no step directing anyone to compare source-of-truth counts against operational-system counts. Had such a step existed as a mandatory first-hour action, the defect would have surfaced on September 8 rather than September 10.

**5.9 The manual route sheet had no controlled template.** Under the prior contractor, manual issuance used a pre-printed form with a tier field. That form was contractor property and did not transfer. The improvised replacement omitted the field. The tier assignment is not intuitively necessary to a driver executing a stop list, which is precisely why it must be printed rather than remembered.

**5.10 Two days of hand-written sheets were issued before any review.** The tier omission was found on September 11 only because a supervisor physically carried a sheet into the command post. No process required that improvised artifacts be reviewed before their second use.

**5.11 Special education transportation had no independent verification.** The 41 mandated students were identified by manual cross-reference on September 10. There was no automated reconciliation between IEP transportation mandates and route assignments. Special Services had no read access to Trailhead route data and could not have performed the check earlier without a request to Transportation.

**5.12 Escalation authority was ambiguous during the first 48 hours.** Duarte identified a service-eligibility problem on September 8 and escalated in writing on September 9. There was no defined threshold at which a mandated-service gap automatically triggers command-post activation independent of the operational chain.

**5.13 Communications capacity was sized for normal operations.** Two-person phone coverage against 3,100 calls produced 41-minute hold times, which generated additional calls. The district had no surge staffing plan for transportation events.

**5.14 The alternate-provider path was not pre-established.** Contracted vans required scoping, quoting, and emergency procurement approval between September 10 and 16 — six days. No standby contract existed for special-education transportation continuity.

---

## 6. What Worked

**The Superintendent's arithmetic question broke the diagnosis.** On September 10, the question *why do 14 missing drivers out of 126 produce 62 failed routes out of 112?* did what three days of operational escalation had not. Testing the proportionality of a hypothesis against observed magnitude is a cheap, fast, generalizable technique. It belongs in the incident procedure as a required step.

**The command post consolidated authority.** Once convened on September 10, the command post produced a decision cadence — 6:00 a.m., 11:00 a.m., 4:00 p.m. — with all decision-makers present. Diagnosis, van procurement, and route rebuild sequencing all moved through it in under 72 hours. The structure worked. The failure was that it was activated on day three rather than day one.

**Special Services identified and tracked the mandated cohort independently.** Duarte's office established the 41-student number by manual cross-reference before Transportation could produce it, escalated in writing when the operational chain was focused elsewhere, and had the van requirement scoped and ready when procurement authority arrived. That work was done without system access, using IEP records and phone calls.

**Emergency procurement functioned.** The Business Administrator moved $214,000 through emergency authority in under 48 hours from scoping to approval. The procurement mechanism was not the constraint; the absence of a pre-negotiated standby contract was.

**The vendor responded within hours.** Trailhead's field-length change was implemented between 12:30 a.m. and 3:15 a.m. on September 11. Once the defect was named, technical correction took under three hours.

**The crossing guard prevented a far worse outcome.** A municipal employee outside the district's chain of responsibility recognized an unaccompanied child, secured the child, and made contact. The district's own systems did not detect the misrouting; a person did. Any reading of this incident that credits systems for the safe outcome is misreading it.

**Route rebuild was executed correctly under pressure.** Thirty-one hours to rebuild 112 routes across three tiers, delivered on time and correct, with delay dropping from 63 minutes to 19 minutes on first run. The operations work was sound. It was pointed at the wrong problem for two days.

---

## 7. What Did Not Work

**The first 60 hours were spent on the wrong problem.** Between 5:12 a.m. September 8 and 6:40 p.m. September 10, the response added spare vehicles, doubled routes, and pursued driver coverage. All of it was reasonable against the staffing hypothesis and none of it addressed the defect. The cost of that misdirection was two additional days of service failure and two additional days of mandated-service gap.

**Hand-written route sheets made the incident worse.** The improvised mitigation on September 9 produced a 63-minute average delay against day one's 47. A response action that degrades service by 34 percent is a response action that was not reviewed before deployment. It was then repeated on September 10.

**Forty-seven early-warning calls were absorbed without aggregation.** The defect announced itself on September 3, five days before service. The service desk resolved nineteen instances of a systemic problem one at a time.

**The validation report was never opened.** Seventeen days. The report named the defect, the count, and the reason on page one. The failure was not analytical; the district had the answer in writing and nobody was assigned to read it.

**Four school days of mandated-service gap.** For students whose IEPs specify door-to-door transportation, the district provided none from September 8 through September 16. This is the most serious item in this report. It is not mitigated by the difficulty of the week.

**Communications was reactive throughout.** No proactive notification went to families on September 8 or 9. The first districtwide communication issued on September 10 at 4:30 p.m., after two days of 47- and 63-minute delays and 3,100 calls. Families learned from other families.

**The readiness memo asserted readiness.** The September 2 memo cited improved seat utilization as evidence of optimization. It was evidence of data loss. No readiness artifact required a count reconciliation against enrollment.

**No one owned the question "is our data right?"** The genuine finding of this postmortem is not that a specific person missed a check. It is that after the transition, no role in the district was accountable for the correctness of the data on which 5,600 students' transportation depended. The Transportation Director owned operations. The CTO owned systems. Neither owned data integrity as a named responsibility, and the runbook that formerly bridged the gap no longer contained the bridge.

---

## 8. Action Items

Owners are accountable for completion, not necessarily for execution. Items marked **[Board]** require board action.

### Immediate — complete by November 6, 2026

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Complete compensatory-services determination for all 41 students; individual written plans to families | M. Duarte | Oct 30 |
| 2 | Respond to both NJDOE complaints with full remediation record | I. Adeyemi | Per state deadline |
| 3 | Configure Trailhead alerting for all warning-level events (row rejection, geocode failure, duplicate suppression) with notification to CTO and Transportation Director | B. Kwan | Oct 23 |
| 4 | Implement daily automated reconciliation of Trailhead student count against SIS enrollment; variance >0.5% blocks route publication and pages CTO | B. Kwan | Nov 6 |
| 5 | Field-length audit of all SIS-to-Trailhead mapped fields; extend or truncate-with-flag as appropriate | B. Kwan | Oct 30 |
| 6 | Issue controlled manual route sheet template including mandatory tier field; distribute to all yard supervisors | R. Sciarra | Oct 16 |
| 7 | Retain contracted vans for the 41 students until Transportation certifies door-to-door capacity in writing | G. Ostrowski | Ongoing |

### Near-term — complete by January 15, 2027

| # | Action | Owner | Due |
|---|---|---|---|
| 8 | Create and staff a named Data Integrity Owner role for transportation data, with defined verification duties and Trailhead audit access | I. Adeyemi | Dec 4 |
| 9 | Rebuild the transportation runbook with a controls register: every verification step listed with named owner, frequency, and evidence artifact | R. Sciarra / B. Kwan | Dec 18 |
| 10 | Reconcile controls register against every position eliminated or restructured since FY2024; document disposition of each orphaned control | G. Ostrowski | Jan 15 |
| 11 | Grant Special Services standing read access to Trailhead route data; build automated weekly IEP-mandate-to-route-assignment reconciliation | B. Kwan / M. Duarte | Dec 11 |
| 12 | Revise incident procedure: mandatory first-hour source-of-truth count verification; mandatory proportionality test on any diagnosis; command-post activation triggered automatically by mandated-service gap of any duration | I. Adeyemi | Nov 20 |
| 13 | Establish service-desk aggregation rule: 5+ tickets sharing a symptom within 48 hours escalates to problem investigation with named investigator | Dir. of Communications | Nov 20 |
| 14 | Build transportation surge communications plan: staffing tiers, pre-drafted templates, proactive notification triggers at 20 and 40 minutes average delay | Dir. of Communications | Dec 11 |
| 15 | Execute standby contract for emergency special-education transportation, activatable within 24 hours **[Board]** | G. Ostrowski | Jan 15 |

### Structural — complete by June 30, 2027

| # | Action | Owner | Due |
|---|---|---|---|
| 16 | Adopt minimum transition-period policy for pupil transportation procurement: no award-to-service window under 180 days absent board-documented risk acceptance **[Board]** | G. Ostrowski / I. Adeyemi | Mar 31 |
| 17 | Adopt policy that vendor-recommended validation phases may be compressed only with written risk assessment naming what the compression forgoes | B. Kwan | Feb 27 |
| 18 | Establish pre-opening readiness gate with hard go/no-go criteria including count reconciliation, mandated-service verification, and tier-integrity check; gate held 10 business days before opening | I. Adeyemi | Jun 30 |
| 19 | Conduct annual tabletop exercise on transportation system failure, including a silent-data-loss scenario | R. Sciarra | Jun 30 |
| 20 | Report incident closure and action-item status to the Board **[Board]** | I. Adeyemi | Feb 2027 board meeting |

---

## 9. Closing Note

This district compressed a transition, deleted a control without noticing, configured a system to be quiet about the exact failure it experienced, and then spent two days treating a real problem as the explanation for a different problem. Each of those was a systems decision. None of them was a person's failure of diligence.

The most useful thing in this report is not the root cause. It is the observation in Section 7 that no role owned the question of whether the data was right. Every other finding follows from that vacancy. Action items 8, 9, and 10 exist to fill it, and their completion is the measure by which the Board should judge whether this district has actually learned anything from September.

Forty-one students who are legally entitled to a ride to school did not get one for four days. That is the sentence this district should carry forward.
