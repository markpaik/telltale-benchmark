# Rock River Logistics Group
## Warehouse Management System Cutover Steering Committee
### Minutes of Four Consecutive Meetings

---

## MEETING ONE

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, September 4, 2025
**Time:** 9:00 a.m. – 11:42 a.m. CDT
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Tomas Escalante, Site Director, Janesville Distribution Center; Freya Lindqvist, Director of Transportation; Anders Wahlgren, Program Manager

**Members Absent:** None

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting); Carolyn Maes, Executive Assistant to the COO (Recording Secretary); Priya Natarajan, Senior Business Analyst (for agenda item 3 only)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m. and confirmed that a quorum was present. Mr. Escalante moved to approve the minutes of the August 21, 2025 meeting as circulated. Ms. Lindqvist seconded. The motion carried 5–0.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren delivered the standing status report on the Meridian Compass WMS implementation. He reported that the program remained at Red status for the fourth consecutive reporting period. Overall budget consumption stood at $5.9 million against the $6.8 million contract value, or 87 percent, with the September go-live milestone at risk. He reminded the committee that go-live had already slipped twice, from the original March 2025 date to July, and from July to the currently planned September 15 cutover at Janesville, with subsequent waves at Eau Claire, Kenosha, Rockford, Loves Park, and Peoria running through the first quarter of 2026.

Mr. Wahlgren reported that integration testing of the parcel manifesting interface completed on August 28, three weeks behind plan, and that end-user training at Janesville had reached 71 percent completion against a 100 percent target for this date.

### 3. Janesville Pilot Readiness and Defect Metrics

Mr. Escalante and Ms. Natarajan presented the Janesville pilot results for the two-week measurement window ending August 31, 2025:

- **Pick accuracy:** 62.0 percent against the contractual standard of 99.2 percent.
- **Open defect tickets:** 218 total, comprising 11 Severity 1 (system down or data corruption), 43 Severity 2 (major function impaired, no workaround), 96 Severity 3 (function impaired with workaround), and 68 Severity 4 (cosmetic or documentation).
- **Order cycle time:** 4.1 hours from wave release to dock, against a 1.5-hour standard.
- **Temporary labor:** 14 temporary workers had been hired at Janesville to cover manual workarounds, at a run-rate cost of approximately $9,800 per week.
- **Inventory record accuracy:** 91.3 percent by location, against a 99.5 percent standard.

Mr. Escalante stated that the pick accuracy figure reflected systemic problems with RF device screen flow and slotting logic, not operator error, and that his supervisors were re-verifying every outbound pallet by hand. He stated that in his professional judgment the Janesville site could not support a September 15 cutover without material risk to customer commitments.

### 4. Vendor Response — Rebecca Dziedzic

Ms. Dziedzic responded on behalf of Meridian Yard Systems. She acknowledged the defect count and attributed the pick accuracy shortfall primarily to a slotting algorithm configuration error introduced in the August 14 build, for which a corrective patch (Build 7.3.2) was scheduled for September 9. She stated that Meridian had assigned four additional engineers to the account effective September 2 and committed to reducing Severity 1 defects to zero and Severity 2 defects below ten by September 30. She requested that the committee defer any go-live decision until the September 18 meeting so that the patch results could be evaluated. Mr. Mirchandani questioned whether the September 9 patch had been regression-tested against the parcel manifesting interface; Ms. Dziedzic stated that regression testing was scheduled but not complete.

### 5. Go-Live Decision

Following discussion, Mr. Escalante moved that the committee hold (not proceed with) the September 15 go-live at Janesville, continue pilot operations in parallel-run mode on the legacy Catalyst system, and require Meridian to present a remediation plan with measurable exit criteria at the September 18 meeting. Ms. Lindqvist seconded.

Discussion: Mr. Mirchandani supported the hold but asked that the motion not fix a new go-live date until remediation results were known. The mover and seconder accepted this as a friendly amendment.

**Vote:** The motion carried 5–0. **Decision:** The September 15 Janesville go-live was held; no new date was set.

### 6. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 1 | Deliver written remediation plan with exit criteria (pick accuracy ≥ 97 percent sustained over 10 operating days; zero Sev-1; ≤ 10 Sev-2) | R. Dziedzic | Sept. 16, 2025 |
| 2 | Quantify total cost of delay, including temporary labor, parallel-run costs, and vendor fees | A. Wahlgren | Sept. 16, 2025 |
| 3 | Complete regression testing of Build 7.3.2 against all interfaces and report results | S. Mirchandani | Sept. 17, 2025 |
| 4 | Notify affected customers' account teams of revised timeline; assess service-level exposure | F. Lindqvist | Sept. 11, 2025 |
| 5 | Prepare Janesville labor plan for extended parallel run, including temp-worker cost projection through Q4 | T. Escalante | Sept. 16, 2025 |
| 6 | Retrieve executed contract and change-order file and circulate cure, remedy, and termination provisions to voting members under privilege | Y. Brissette | Sept. 12, 2025 |

### 7. Adjournment

There being no further business, Chair Brissette adjourned the meeting at 11:42 a.m. The next regular meeting was set for Thursday, September 18, 2025, at 9:00 a.m.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approved: September 18, 2025

---

## MEETING TWO

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, September 18, 2025
**Time:** 9:00 a.m. – 12:15 p.m. CDT
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Tomas Escalante, Site Director, Janesville Distribution Center; Anders Wahlgren, Program Manager

**Members Absent:** Freya Lindqvist, Director of Transportation (excused; customer site visit). Ms. Lindqvist submitted her reports in writing.

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting; items 1–5 only); Patricia Gorman, Whitfield & Gorman LLP, outside counsel (item 6 only); Carolyn Maes, Executive Assistant to the COO (Recording Secretary)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m. and confirmed a quorum. Mr. Wahlgren moved to approve the minutes of September 4, 2025 as circulated. Mr. Escalante seconded. The motion carried 4–0.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren reported the program remained Red. His cost-of-delay analysis (Action Item 2) quantified the impact of the September hold at approximately $187,000 per month, comprising temporary labor ($42,000), dual-system licensing and support ($61,000), extended vendor professional services ($58,000), and overtime for parallel-run reconciliation ($26,000). Cumulative program spend stood at $6.05 million.

### 3. Readiness and Defect Metrics

Mr. Wahlgren and Mr. Escalante reported the following for the window ending September 14, reflecting the September 9 deployment of Build 7.3.2:

- **Pick accuracy:** 74.6 percent, up from 62.0 percent, against the 99.2 percent standard.
- **Open defects:** 196 total (7 Sev-1, 38 Sev-2, 89 Sev-3, 62 Sev-4).
- **Order cycle time:** 3.2 hours against the 1.5-hour standard.
- **Temporary labor:** 14 temporary workers remained on the Janesville roster.
- **Regression results (Action Item 3):** Mr. Mirchandani reported that Build 7.3.2 passed regression against the parcel manifesting interface but introduced two new Sev-2 defects in the cycle-count module.

Ms. Lindqvist's written report (Action Item 4) confirmed that account teams for the twelve customers served from Janesville had been notified; three customers had requested formal service-level review meetings.

### 4. Vendor Remediation Plan — Rebecca Dziedzic

Ms. Dziedzic presented Meridian's written remediation plan dated September 16. Meridian committed to zero Sev-1 defects by September 26, Sev-2 defects below ten by October 10, and sustained pick accuracy of 97 percent or better by October 24, with a proposed Janesville cutover in the window of October 27–31. Mr. Escalante objected that an October 27 cutover would leave no stabilization period before the November 1 peak-season change freeze. Ms. Dziedzic acknowledged the risk and stated that Meridian believed the dates were achievable. The committee accepted the plan for tracking purposes without endorsing the proposed cutover window; no vote was taken.

### 5. Disputed Change Order CO-2025-014 ($410,000)

Mr. Wahlgren presented change order CO-2025-014, submitted by Meridian on August 29 in the amount of $410,000, covering rework of the transportation management system interface and additional RF screen-flow development. Meridian's position, stated by Ms. Dziedzic, was that the work exceeded the functional specification signed in November 2024. Mr. Wahlgren's position, supported by a requirements traceability analysis distributed with the agenda, was that the disputed items were within the original statement of work, sections 4.7 and 4.9, and that a substantial portion of the rework corrected Meridian's own defects.

Mr. Mirchandani moved that the committee formally dispute change order CO-2025-014 in its entirety, decline payment pending resolution, and refer the matter to outside counsel and the program manager for a written position statement to Meridian. Mr. Escalante seconded.

**Vote:** The motion carried 4–0. **Decision:** CO-2025-014 was disputed and referred to counsel; payment was withheld.

### 6. Closed Session — Contract Cure and Termination Provisions

At 11:05 a.m., Mr. Wahlgren moved that the committee enter closed session with counsel to receive privileged advice on contract remedies. Mr. Mirchandani seconded. The motion carried 4–0. Ms. Dziedzic and all Meridian personnel were excused; Ms. Gorman joined the session.

The committee met in closed session from 11:08 a.m. to 11:52 a.m. The recording secretary noted for the open record only that counsel briefed the committee on the master services agreement's material breach definition (Section 13.1), the 30-day cure provision (Section 14.2), termination for cause (Section 14.5), the limitation-of-liability clause (Section 16), and the notice requirements for preserving remedies. No motions were made and no votes were taken in closed session. A privileged memorandum of the session was retained by counsel.

Upon return to open session at 11:52 a.m., Chair Brissette reported that no action had been taken and that the committee had directed counsel to prepare, but not send, a draft cure notice so that the company could act quickly if remediation milestones were missed.

### 7. Committee Composition

Chair Brissette stated that given the financial exposure and the enterprise-wide operational impact, the committee should be expanded. She moved that Deborah Okafor, Chief Financial Officer, and Marcus Tran, Director of Distribution Operations, be added as voting members effective October 2, 2025, bringing voting membership to seven. Mr. Wahlgren seconded.

**Vote:** The motion carried 4–0. **Decision:** Ms. Okafor and Mr. Tran were added as voting members effective October 2, 2025.

### 8. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 7 | Issue written position statement disputing CO-2025-014 to Meridian | A. Wahlgren (with P. Gorman) | Sept. 26, 2025 |
| 8 | Prepare draft cure notice under Section 14.2 for the Chair's file (privileged; not to be sent absent committee direction) | P. Gorman | Sept. 30, 2025 |
| 9 | Publish weekly defect burn-down and pick-accuracy dashboard to all members | S. Mirchandani | Weekly, Mondays, beginning Sept. 22, 2025 |
| 10 | Conduct service-level review meetings with the three requesting customers and report exposure | F. Lindqvist | Oct. 1, 2025 |
| 11 | Prepare go/no-go readiness criteria for the Eau Claire wave for decision on October 2 | A. Wahlgren | Sept. 30, 2025 |
| 12 | Brief Ms. Okafor and Mr. Tran on program history and open issues before October 2 | Y. Brissette | Sept. 30, 2025 |

### 9. Adjournment

Chair Brissette adjourned the meeting at 12:15 p.m. The next regular meeting was set for Thursday, October 2, 2025, at 9:00 a.m.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approved: October 2, 2025

---

## MEETING THREE

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, October 2, 2025
**Time:** 9:00 a.m. – 12:34 p.m. CDT
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Tomas Escalante, Site Director, Janesville Distribution Center; Freya Lindqvist, Director of Transportation; Anders Wahlgren, Program Manager; Deborah Okafor, Chief Financial Officer; Marcus Tran, Director of Distribution Operations

**Members Absent:** None

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting; items 1–6 only); Patricia Gorman, Whitfield & Gorman LLP, outside counsel (item 7 only); Carolyn Maes, Executive Assistant to the COO (Recording Secretary)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m., welcomed Ms. Okafor and Mr. Tran as voting members, and confirmed a quorum. Ms. Lindqvist moved to approve the minutes of September 18, 2025 as circulated. Mr. Mirchandani seconded. The motion carried 7–0, Ms. Okafor and Mr. Tran abstaining from none as the minutes had been circulated to them in briefing materials.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren reported the program remained Red. Cumulative spend stood at $6.19 million. The written position statement disputing CO-2025-014 (Action Item 7) was delivered to Meridian on September 25; Meridian responded on September 30 reasserting the charge but offering to reduce it to $265,000, which remained in dispute. The draft cure notice (Action Item 8) had been completed by counsel and was held in the Chair's privileged file. Weekly dashboards (Action Item 9) had been published on schedule.

### 3. Readiness and Defect Metrics

For the measurement window ending September 28:

- **Pick accuracy:** 81.2 percent against the 99.2 percent standard. The Meridian remediation plan had committed to a trajectory reaching 97 percent by October 24; the committee noted the site was behind that trajectory.
- **Open defects:** 174 total (4 Sev-1, 29 Sev-2, 84 Sev-3, 57 Sev-4). The plan milestone of zero Sev-1 by September 26 was missed.
- **Order cycle time:** 2.6 hours against the 1.5-hour standard.
- **Temporary labor:** 14 temporary workers remained; Mr. Escalante reported two resignations and two replacement hires.
- **Inventory record accuracy:** 94.1 percent against the 99.5 percent standard.

### 4. Customer Impact — Freya Lindqvist

Ms. Lindqvist reported the results of the service-level reviews (Action Item 10). She reported that Halvorsen Consumer Brands, Inc., the company's largest customer at 31 percent of revenue, had on September 29 issued a chargeback of $290,000 for mis-shipments and late deliveries originating from the Janesville pilot period, and had placed its logistics services agreement on formal notice, citing its right to terminate for convenience with 90 days' notice if service levels were not restored by December 31, 2025. Two other customers accepted corrective action plans without financial claims.

Ms. Okafor stated that the chargeback, combined with the disputed change order and delay costs, brought identified program-related financial exposure above $1.1 million, and asked that a consolidated exposure schedule be maintained. The Chair so directed (see Action Item 16).

### 5. Vendor Response — Rebecca Dziedzic

Ms. Dziedzic acknowledged that Meridian had missed the September 26 Sev-1 milestone, attributing the miss to a database deadlock defect discovered on September 24 that required architectural review. She stated that Meridian's chief technology officer had personally taken ownership of the deadlock issue, that a fix was in test with deployment expected October 8, and that Meridian stood by its October 24 accuracy commitment. In response to a question from Mr. Tran, she conceded that Meridian had not yet begun site-specific configuration for Eau Claire because engineering resources had been diverted to Janesville remediation.

### 6. Eau Claire Deployment Decision

Mr. Wahlgren presented the Eau Claire go/no-go criteria (Action Item 11) and reported that zero of six readiness criteria had been met, including completion of site configuration, training commencement, and a stable Janesville reference build. Mr. Tran stated that Eau Claire was the company's second-highest-volume site and that attempting deployment there during peak season would compound rather than contain risk.

Mr. Tran moved that the Eau Claire deployment, planned for November 10, 2025, be deferred indefinitely, with re-planning contingent on Janesville achieving sustained contractual performance, and that no further wave dates be published to sites or customers until a re-baselined plan was approved by this committee. Ms. Lindqvist seconded.

**Vote:** The motion carried 7–0. **Decision:** The Eau Claire deployment was deferred; the wave schedule was suspended pending re-baselining.

### 7. Closed Session — Contract Remedies and Customer Notice

At 11:20 a.m., Ms. Okafor moved to enter closed session with counsel to receive privileged advice concerning remedies against Meridian and the Halvorsen contract notice. Mr. Escalante seconded. The motion carried 7–0. Ms. Dziedzic was excused; Ms. Gorman joined.

The committee met in closed session from 11:24 a.m. to 12:18 p.m. For the open record, the recording secretary noted that counsel advised on the evidentiary record supporting a material breach determination, on preservation of documents and communications, on the interaction between the cure provision and the disputed change order, and on the company's obligations and options under the Halvorsen agreement. No motions were made and no votes were taken in closed session; a privileged memorandum was retained by counsel.

On return to open session at 12:18 p.m., Chair Brissette reported that the committee had directed counsel to update the draft cure notice to reflect the missed September 26 milestone and the Halvorsen chargeback, and that a decision on issuing the notice would be taken no later than the October 16 meeting, in light of the November 1 peak-season change freeze.

### 8. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 13 | Update draft cure notice with missed milestones and consequential-impact record (privileged) | P. Gorman | Oct. 10, 2025 |
| 14 | Deliver Halvorsen corrective action plan and schedule executive meeting with Halvorsen leadership | F. Lindqvist (with Y. Brissette) | Oct. 14, 2025 |
| 15 | Prepare Q4 peak-season operating plan on legacy Catalyst system for all six sites, including labor and freight contingencies | M. Tran | Oct. 14, 2025 |
| 16 | Maintain consolidated schedule of program financial exposure; report at each meeting | D. Okafor | Standing, beginning Oct. 16, 2025 |
| 17 | Verify Meridian's October 8 deadlock fix in test environment and report results | S. Mirchandani | Oct. 13, 2025 |
| 18 | Prepare re-baselining options paper (including a February 2026 scenario) with scope, cost, and resource requirements | A. Wahlgren | Oct. 14, 2025 |
| 19 | Confirm document-preservation hold across program teams | Y. Brissette (with P. Gorman) | Oct. 6, 2025 |

### 9. Adjournment

Chair Brissette adjourned the meeting at 12:34 p.m. The next regular meeting was set for Thursday, October 16, 2025, at 9:00 a.m.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approved: October 16, 2025

---

## MEETING FOUR

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, October 16, 2025
**Time:** 9:00 a.m. – 1:05 p.m. CDT
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Tomas Escalante, Site Director, Janesville Distribution Center; Freya Lindqvist, Director of Transportation; Anders Wahlgren, Program Manager; Deborah Okafor, Chief Financial Officer; Marcus Tran, Director of Distribution Operations

**Members Absent:** None

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting; items 1–5 only); Patricia Gorman, Whitfield & Gorman LLP, outside counsel (items 6–7); Carolyn Maes, Executive Assistant to the COO (Recording Secretary)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m. and confirmed a quorum. Mr. Tran moved to approve the minutes of October 2, 2025 as circulated. Ms. Okafor seconded. The motion carried 7–0.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren reported the program remained Red. Cumulative spend stood at $6.31 million. He noted that the November 1 peak-season change freeze was sixteen days away, after which no production system changes would be permitted at any site until January 5, 2026. He reported that the Meridian deadlock fix deployed October 8 and had been verified in test by internal IT (Action Item 17); Mr. Mirchandani confirmed the verification. The re-baselining options paper (Action Item 18) was distributed with the agenda.

Ms. Okafor presented the first standing financial exposure report (Action Item 16): $410,000 disputed change order; $290,000 Halvorsen chargeback; approximately $187,000 per month in delay costs since September; and estimated re-baselining costs of $520,000 to $780,000 depending on the option selected, for total identified exposure of approximately $1.4 million to $1.7 million, excluding any Halvorsen contract loss.

### 3. Readiness and Defect Metrics

For the measurement window ending October 12:

- **Pick accuracy:** 88.4 percent against the 99.2 percent standard, and against Meridian's committed trajectory point of 94 percent for this date.
- **Open defects:** 121 total (2 Sev-1, 18 Sev-2, 61 Sev-3, 40 Sev-4). The plan milestone of Sev-2 below ten by October 10 was missed.
- **Order cycle time:** 2.1 hours against the 1.5-hour standard.
- **Temporary labor:** 14 temporary workers remained at Janesville.
- **Inventory record accuracy:** 96.0 percent against the 99.5 percent standard.

Mr. Escalante stated that the trend was genuinely improving but that the site could not reach, sustain, and prove contractual performance before the November 1 freeze, and that any cutover attempt inside the freeze window would be operationally indefensible during peak.

### 4. Customer Update — Freya Lindqvist

Ms. Lindqvist reported that she and Chair Brissette met with Halvorsen Consumer Brands executives on October 14 (Action Item 14). Halvorsen accepted the corrective action plan, agreed to hold its termination notice in abeyance pending December performance results, and stated that a stable peak season on the legacy system was its expressed preference over any further cutover attempt in 2025.

### 5. Vendor Response — Rebecca Dziedzic

Ms. Dziedzic acknowledged that Meridian had missed the October 10 Sev-2 milestone and was tracking below its accuracy commitment. She presented Meridian's proposal to continue remediation through the freeze, with a cutover in the window of January 12–16, 2026. She stated that Meridian opposed issuance of a formal cure notice, characterizing it as escalatory while measurable progress was being made, and offered a fee credit of $150,000 against future milestones in lieu of formal remedies. Ms. Okafor asked whether the offered credit was conditioned on release of claims; Ms. Dziedzic confirmed that Meridian's offer as drafted included a mutual release, including of the disputed change order. Several members stated that a release on those terms was not acceptable. Ms. Dziedzic was excused at 10:35 a.m. before deliberations on remedies.

### 6. Closed Session — Contract Remedies

At 10:37 a.m., Ms. Okafor moved to enter closed session with counsel. Mr. Wahlgren seconded. The motion carried 7–0. The committee met in closed session from 10:40 a.m. to 11:48 a.m. For the open record, the recording secretary noted that counsel presented the updated draft cure notice (Action Item 13), advised on the consequences of issuing or withholding it before the freeze, on the effect of Meridian's settlement offer on the company's remedy position, and on the standard of documentation required during any cure period. No motions were made and no votes were taken in closed session; a privileged memorandum was retained by counsel.

### 7. Decision on Cure Notice, Q4 Operations, and Re-Baselining

Upon return to open session at 11:48 a.m., the committee took up the re-baselining options paper. Following discussion, Ms. Okafor moved that the company:

(a) issue the formal cure notice to Meridian Yard Systems under Section 14.2 of the master services agreement, specifying the missed remediation milestones and requiring cure within the contractual 30-day period, with all rights and remedies expressly reserved;
(b) operate all six distribution centers on the legacy Catalyst system for the entire fourth-quarter peak season, standing down all cutover activity for 2025; and
(c) direct the program manager to re-baseline program scope, cost, and schedule toward a single-site Janesville cutover attempt in February 2026, with revised go/no-go criteria to be approved by this committee no later than December 11, 2025.

Mr. Tran seconded.

Discussion: Mr. Mirchandani spoke against the motion, stating that the technical trend justified continued collaborative remediation and that a formal cure notice risked hardening Meridian's position on the change order and diverting engineering effort into legal defense. Mr. Wahlgren concurred in part, stating he supported parts (b) and (c) but opposed part (a), preferring a negotiated remediation amendment; a motion by Mr. Wahlgren to divide the question failed for want of a second. Ms. Okafor, Mr. Escalante, and Mr. Tran spoke in favor, citing the missed milestones of September 26 and October 10, the $1.4 million-plus exposure, and the need to preserve legal remedies before the freeze. Ms. Gorman confirmed, in response to a question from the Chair, that issuing the notice did not obligate the company to terminate.

**Vote:** The motion carried 5–2, with Chair Brissette, Mr. Escalante, Ms. Lindqvist, Ms. Okafor, and Mr. Tran voting in favor, and Mr. Mirchandani and Mr. Wahlgren voting against. **Decision:** The formal cure notice was authorized for issuance; the fourth quarter would run on the legacy system at all sites; scope would be re-baselined toward a February 2026 Janesville attempt.

### 8. Announcement — Departure of Tomas Escalante

Mr. Escalante announced that he had accepted a position with another company and would leave Rock River Logistics Group in three weeks, with a final working day of November 7, 2025. Chair Brissette thanked Mr. Escalante for his service and stated that an interim Janesville site director and a replacement committee member would be named before the November 13 meeting. Mr. Escalante committed to completing a written transition file covering pilot history, workaround procedures, and temporary labor arrangements before his departure.

### 9. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 20 | Finalize and transmit the formal cure notice to Meridian under Section 14.2 | P. Gorman (with Y. Brissette signing) | Oct. 20, 2025 |
| 21 | Notify Meridian in writing of the stand-down of 2025 cutover activity and the legacy-system Q4 operating decision | A. Wahlgren | Oct. 21, 2025 |
| 22 | Finalize and distribute the Q4 legacy-system peak operating plan to all six site directors | M. Tran | Oct. 28, 2025 |
| 23 | Deliver re-baselined program plan for February 2026 Janesville attempt, with revised scope, budget, and go/no-go criteria, for committee approval | A. Wahlgren | Dec. 4, 2025 (for approval by Dec. 11, 2025) |
| 24 | Track Meridian performance against the cure notice; report defect and accuracy metrics weekly during the cure period | S. Mirchandani | Weekly, beginning Oct. 27, 2025 |
| 25 | Complete Janesville transition file and knowledge-transfer sessions with the interim site director | T. Escalante | Nov. 7, 2025 |
| 26 | Name interim Janesville site director and replacement voting member | Y. Brissette | Nov. 10, 2025 |
| 27 | Report December performance results to Halvorsen under the corrective action plan | F. Lindqvist | Jan. 6, 2026 |
| 28 | Update consolidated financial exposure schedule to reflect cure-period costs and Meridian's withdrawn or outstanding settlement offer | D. Okafor | Nov. 13, 2025 |

### 10. Adjournment

There being no further business, Chair Brissette adjourned the meeting at 1:05 p.m. The next regular meeting was set for Thursday, November 13, 2025, at 9:00 a.m., reflecting the committee's biweekly schedule adjusted for the October 30 executive planning conflict, as agreed without objection.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approval pending: November 13, 2025

---

## MEETING FIVE

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, November 13, 2025
**Time:** 9:00 a.m. – 11:58 a.m. CST
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Freya Lindqvist, Director of Transportation; Anders Wahlgren, Program Manager; Deborah Okafor, Chief Financial Officer; Marcus Tran, Director of Distribution Operations; Hannah Cichowski, Interim Site Director, Janesville Distribution Center (appointed voting member effective November 10, 2025, per Action Item 26)

**Members Absent:** None

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting; items 1–5 only); Grant Ohlsson, Vice President of Delivery, Meridian Yard Systems (non-voting; items 4–5 only); Patricia Gorman, Whitfield & Gorman LLP, outside counsel (item 6); Carolyn Maes, Executive Assistant to the COO (Recording Secretary)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m., confirmed a quorum, and welcomed Ms. Cichowski, whose appointment as interim Janesville site director and voting committee member effective November 10, 2025 she confirmed for the record. The Chair noted with thanks the departure of Mr. Escalante on November 7 and confirmed that his transition file (Action Item 25) had been delivered complete and reviewed with Ms. Cichowski on November 5 and 6.

Ms. Okafor moved to approve the minutes of October 16, 2025 as circulated. Mr. Tran seconded. The motion carried 6–0, Ms. Cichowski abstaining as she had not been a member at that meeting.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren reported the program status had been revised from Red to Amber, reflecting the stabilized legacy-system operating posture and the cure period now in progress. He confirmed the following against prior action items:

- The formal cure notice (Action Item 20) was transmitted to Meridian by counsel on October 20, 2025, by certified mail and electronic delivery per Section 19.3 of the master services agreement. Meridian acknowledged receipt on October 21. The 30-day cure period would expire November 19, 2025.
- The stand-down notification (Action Item 21) was delivered October 21; Meridian confirmed the stand-down of all 2025 cutover activity on October 23.
- The Q4 legacy operating plan (Action Item 22) was distributed to all six site directors on October 27, one day ahead of schedule. Mr. Tran reported all sites had entered the November 1 change freeze on the legacy Catalyst system without incident, and that the first two weeks of peak volume had been handled at 98.9 percent on-time shipment across the network.

Cumulative program spend stood at $6.38 million. Ms. Okafor presented the updated exposure schedule (Action Item 28): the $410,000 change order remained in dispute; the $290,000 Halvorsen chargeback had been paid and booked in October; Meridian's October settlement offer of a $150,000 credit with mutual release had been formally withdrawn by Meridian on October 24, four days after the cure notice issued; delay costs continued at approximately $187,000 per month. Total identified exposure stood at approximately $1.52 million.

### 3. Cure-Period Readiness and Defect Metrics — Sanjay Mirchandani

Mr. Mirchandani presented the weekly cure-period tracking (Action Item 24) for the window ending November 9, measured in the parallel-run test environment since production changes were frozen:

- **Pick accuracy (parallel-run environment):** 95.1 percent, up from 88.4 percent at last report, against the 99.2 percent contractual standard and the cure notice requirement of 97 percent sustained over ten operating days.
- **Open defects:** 74 total (0 Sev-1, 9 Sev-2, 39 Sev-3, 26 Sev-4). He noted that both cure notice thresholds for defect severity — zero Sev-1 and fewer than ten Sev-2 — had been met as of November 6 and sustained since.
- **Order cycle time (simulated wave testing):** 1.7 hours against the 1.5-hour standard.
- **Inventory record accuracy (test dataset):** 98.2 percent against the 99.5 percent standard.

Ms. Cichowski reported that the fourteen temporary workers at Janesville had been reduced to six as of November 10, as legacy-system operations required fewer manual reconciliation workarounds, reducing the weekly run-rate to approximately $4,200.

### 4. Vendor Response — Grant Ohlsson and Rebecca Dziedzic

Mr. Ohlsson, attending for the first time, stated that Meridian's executive leadership had treated the cure notice as its highest delivery priority. He reported that Meridian had assigned a dedicated cure-period team of eleven engineers, delivered Builds 7.4.0 and 7.4.1 on October 28 and November 6 respectively, and would deliver written certification of cure with supporting evidence on or before November 18. He acknowledged for the record that the pick-accuracy threshold of 97 percent sustained over ten operating days had not yet been demonstrated and that Meridian would request the company's agreement to measure the sustainment window through December 5 in the test environment, given the production change freeze.

Ms. Okafor asked whether Meridian was prepared to resolve CO-2025-014 as part of any cure resolution. Mr. Ohlsson stated Meridian was prepared to withdraw $290,000 of the $410,000 change order and to discuss the remaining $120,000, without conditioning the concession on a release of claims. The Chair directed that the offer be reduced to writing and referred to counsel; no action was taken.

### 5. February 2026 Re-Baselining — Preliminary Review

Mr. Wahlgren previewed the re-baselining plan due December 4 (Action Item 23). The working scope contemplated a single-site Janesville cutover in the window of February 9–13, 2026, a de-scoping of the yard management and labor-standards modules from the initial cutover to a Phase 2 release, revised go/no-go criteria requiring sustained contractual performance in a four-week production pilot, and a resequencing of the remaining five sites through the third quarter of 2026. Preliminary incremental cost was estimated at $610,000, of which Meridian's share would be a subject of the cure resolution negotiation. Members asked questions; no decisions were taken pending the December 4 submission.

Mr. Ohlsson and Ms. Dziedzic were excused at 10:52 a.m.

### 6. Closed Session — Cure Determination Standards

At 10:54 a.m., Mr. Wahlgren moved to enter closed session with counsel. Ms. Lindqvist seconded. The motion carried 7–0. The committee met in closed session from 10:56 a.m. to 11:40 a.m. For the open record, the recording secretary noted that counsel advised on the standard for accepting or rejecting Meridian's forthcoming certification of cure, on the treatment of the test-environment measurement question raised by Mr. Ohlsson, on the effect of accepting the partial change-order withdrawal, and on the company's position should the cure period expire without full cure. No motions were made and no votes were taken in closed session; a privileged memorandum was retained by counsel.

On return to open session at 11:40 a.m., Chair Brissette reported that the committee had directed counsel to prepare a written response protocol so that Meridian's November 18 certification could be evaluated and answered within the contractual window, and had directed that any agreement to a test-environment measurement period be documented as a without-prejudice accommodation expressly preserving all rights under the cure notice.

### 7. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 29 | Evaluate Meridian's certification of cure against the notice criteria and deliver written evaluation to the committee | S. Mirchandani (with A. Wahlgren) | Nov. 21, 2025 |
| 30 | Prepare and, upon the Chair's approval, transmit the company's formal written response to the certification of cure, preserving all rights | P. Gorman | Nov. 25, 2025 |
| 31 | Document the test-environment measurement accommodation as without prejudice to the cure notice | P. Gorman | Nov. 18, 2025 |
| 32 | Obtain Meridian's written withdrawal of $290,000 of CO-2025-014 and counsel's assessment of the residual $120,000 | A. Wahlgren (with P. Gorman) | Nov. 26, 2025 |
| 33 | Submit complete re-baselined program plan for the February 2026 Janesville attempt | A. Wahlgren | Dec. 4, 2025 |
| 34 | Report peak-season network performance on the legacy system, including Halvorsen-specific service levels | M. Tran (with F. Lindqvist) | Dec. 11, 2025 |
| 35 | Recommend permanent Janesville site director staffing plan to the Chair | M. Tran | Dec. 5, 2025 |
| 36 | Update financial exposure schedule for cure-period developments and change-order partial withdrawal | D. Okafor | Dec. 11, 2025 |

### 8. Adjournment

There being no further business, Chair Brissette adjourned the meeting at 11:58 a.m. The committee agreed without objection to hold its next meeting on Thursday, December 11, 2025, at 9:00 a.m., consolidating the November 27 date (Thanksgiving holiday) into a single December session at which the re-baselined plan would be taken up for approval.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approved: December 11, 2025

---

## MEETING SIX

**Body:** Warehouse Management System (WMS) Cutover Steering Committee, Rock River Logistics Group
**Date:** Thursday, December 11, 2025
**Time:** 9:00 a.m. – 12:47 p.m. CST
**Place:** Executive Conference Room B, Corporate Headquarters, 2200 Harrison Avenue, Rockford, Illinois

**Members Present:** Yolanda Brissette, Chief Operating Officer (Chair); Sanjay Mirchandani, Vice President of Technology; Freya Lindqvist, Director of Transportation; Anders Wahlgren, Program Manager; Deborah Okafor, Chief Financial Officer; Marcus Tran, Director of Distribution Operations; Hannah Cichowski, Interim Site Director, Janesville Distribution Center

**Members Absent:** None

**Others Attending:** Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems (non-voting; items 1–5 only); Grant Ohlsson, Vice President of Delivery, Meridian Yard Systems (non-voting; items 3–5 only); Patricia Gorman, Whitfield & Gorman LLP, outside counsel (item 6); Carolyn Maes, Executive Assistant to the COO (Recording Secretary)

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 9:00 a.m. and confirmed a quorum. Ms. Cichowski moved to approve the minutes of November 13, 2025 as circulated. Ms. Okafor seconded. The motion carried 7–0.

### 2. Standing Program Status Report — Anders Wahlgren

Mr. Wahlgren reported the program remained Amber. He confirmed the following against prior action items:

- Meridian delivered its certification of cure on November 18 (one day early). The internal evaluation (Action Item 29) was delivered November 20 and concluded that the defect-severity criteria were fully cured, and that the pick-accuracy criterion was cured in the test environment, with 97.6 percent sustained over the agreed measurement window ending December 5, subject to production confirmation after the freeze.
- The company's formal response (Action Item 30) was transmitted November 24, accepting the certification as to the defect criteria, provisionally accepting the accuracy criterion subject to production validation in a four-week pilot beginning January 12, 2026, and expressly reserving all rights should production performance fall short. Meridian countersigned the response protocol on December 1.
- Meridian's written withdrawal of $290,000 of change order CO-2025-014 (Action Item 32) was received November 25. Counsel assessed the residual $120,000 as attributable in part to legitimate scope refinement; a negotiated resolution was addressed under item 5.

Cumulative program spend stood at $6.46 million. Ms. Okafor presented the updated exposure schedule (Action Item 36): identified net exposure had been reduced to approximately $1.05 million, reflecting the change-order withdrawal and the step-down in temporary labor.

### 3. Peak-Season and Readiness Metrics

Mr. Tran and Ms. Lindqvist presented the peak-season report (Action Item 34): network on-time shipment on the legacy system stood at 99.1 percent for the period November 1 through December 7; Halvorsen-specific on-time performance stood at 99.4 percent with zero chargebacks in the period. Ms. Lindqvist reported that Halvorsen's leadership had confirmed in writing on December 8 that, subject to the January report (Action Item 27), it expected to withdraw its termination notice.

Mr. Mirchandani presented cure-period metrics for the window ending December 7:

- **Pick accuracy (test environment):** 97.6 percent sustained over the ten-day measurement window, against the 97 percent cure threshold and the 99.2 percent contractual standard.
- **Open defects:** 41 total (0 Sev-1, 3 Sev-2, 22 Sev-3, 16 Sev-4).
- **Order cycle time (simulated):** 1.5 hours, meeting the standard.
- **Inventory record accuracy (test dataset):** 99.1 percent against the 99.5 percent standard.

Ms. Cichowski reported that Janesville temporary labor stood at four workers and would be released by December 19.

### 4. Vendor Response — Grant Ohlsson

Mr. Ohlsson thanked the committee for the structured response protocol and confirmed Meridian's commitments for the February attempt: the eleven-person cure team would remain assigned through completion of the four-week production pilot; Meridian would fund $210,000 of the re-baselining cost as a delivery credit, not conditioned on any release; and Meridian's chief technology officer would attend the January go/no-go session. He confirmed that Meridian accepted the revised go/no-go criteria in the re-baselined plan as contractual acceptance criteria by written amendment.

### 5. Approval of the Re-Baselined Program Plan and Change-Order Resolution

Mr. Wahlgren presented the re-baselined plan (Action Item 33) as submitted December 4: a Janesville production cutover in the window of February 9–13, 2026, preceded by a four-week production pilot beginning January 12; de-scoping of the yard management and labor-standards modules to Phase 2; go/no-go criteria of 99.2 percent pick accuracy, zero Sev-1 and fewer than five Sev-2 defects, and 1.5-hour cycle time, each sustained over ten consecutive operating days in production; incremental cost of $610,000 offset by Meridian's $210,000 credit; and remaining site waves at Eau Claire (April), Kenosha (May), Rockford and Loves Park (July), and Peoria (September 2026).

Mr. Mirchandani moved that the committee (a) approve the re-baselined program plan as presented, with a final go/no-go decision on the February cutover reserved to this committee at its meeting of January 29, 2026, and (b) authorize settlement of the residual $120,000 of change order CO-2025-014 at $85,000, payable upon successful completion of the February cutover, as negotiated by counsel, with no release of claims relating to future performance. Mr. Tran seconded.

Discussion: Ms. Okafor confirmed the settlement figure and contingency structure matched counsel's recommendation. Ms. Cichowski confirmed Janesville staffing and training plans supported the January 12 pilot start.

**Vote:** The motion carried 7–0. **Decision:** The re-baselined plan was approved with the February go/no-go reserved to the committee; the change-order settlement was authorized at $85,000, contingent on cutover completion.

Mr. Ohlsson and Ms. Dziedzic were excused at 11:41 a.m.

### 6. Closed Session — Status of Reserved Remedies

At 11:43 a.m., Ms. Okafor moved to enter closed session with counsel. Mr. Wahlgren seconded. The motion carried 7–0. The committee met in closed session from 11:45 a.m. to 12:20 p.m. For the open record, the recording secretary noted that counsel advised on the continued reservation of rights under the November 24 response protocol, on the documentation standard for the January production pilot, and on the disposition of the litigation hold. No motions were made and no votes were taken in closed session; a privileged memorandum was retained by counsel. On return to open session, Chair Brissette reported that the document-preservation hold would remain in effect through successful completion of the February cutover.

### 7. Action Items Recorded

| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 37 | Execute contract amendment incorporating the go/no-go criteria as acceptance criteria and the $210,000 Meridian credit | P. Gorman (with A. Wahlgren) | Dec. 19, 2025 |
| 38 | Complete Janesville pilot readiness checklist, staffing, and training for January 12, 2026 production pilot start | H. Cichowski | Jan. 8, 2026 |
| 39 | Publish production pilot dashboard daily to all members during the pilot | S. Mirchandani | Daily, beginning Jan. 12, 2026 |
| 40 | Deliver December performance report to Halvorsen and obtain written withdrawal of termination notice | F. Lindqvist | Jan. 6, 2026 |
| 41 | Prepare go/no-go decision package for the February cutover | A. Wahlgren | Jan. 26, 2026 (for decision Jan. 29, 2026) |
| 42 | Update financial exposure schedule to reflect the change-order settlement and Meridian credit | D. Okafor | Jan. 29, 2026 |
| 43 | Present permanent Janesville site director recommendation to the Chair | M. Tran | Jan. 9, 2026 |

### 8. Adjournment

There being no further business, Chair Brissette adjourned the meeting at 12:47 p.m. The next regular meetings were set for Thursday, January 15, 2026 (pilot review) and Thursday, January 29, 2026 (go/no-go decision), each at 9:00 a.m.

Respectfully submitted,
Carolyn Maes, Recording Secretary
Approval pending: January 15, 2026

---

## Certification

The foregoing minutes of the Warehouse Management System Cutover Steering Committee for the meetings of September 4, September 18, October 2, October 16, November 13, and December 11, 2025 constitute the official record of the committee's proceedings, maintained by the Office of the Chief Operating Officer, Rock River Logistics Group, Rockford, Illinois. Privileged memoranda of closed sessions are maintained separately by Whitfield & Gorman LLP and are not part of this open record.

**Yolanda Brissette**, Chair, WMS Cutover Steering Committee
**Carolyn Maes**, Recording Secretary
