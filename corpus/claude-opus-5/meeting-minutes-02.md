# Rock River Logistics Group, Inc.
## WMS Cutover Steering Committee — Minutes of Four Consecutive Meetings
### September 4, September 18, October 2, and October 16, 2025

---

# MINUTES — REGULAR MEETING OF SEPTEMBER 4, 2025

**Body:** WMS Cutover Steering Committee, Rock River Logistics Group, Inc.
**Date:** Thursday, September 4, 2025
**Time:** Called to order at 1:02 p.m. Central; adjourned at 3:41 p.m. Central
**Place:** Corporate headquarters, 4400 Sandy Hollow Road, Rockford, Illinois — Executive Conference Room B, with a video bridge to the Janesville, Wisconsin distribution center

**Members present (voting):**
- Yolanda Brissette, Chief Operating Officer, Chair
- Sanjay Mirchandani, Vice President of Technology
- Tomas Escalante, Site Director, Janesville DC (present by video bridge)
- Freya Lindqvist, Director of Transportation
- Anders Wahlgren, Program Manager

**Members absent:** None. A quorum of the full committee was present throughout.

**Others attending (non-voting):**
- Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems
- Priyanka Deshmukh, WMS Functional Lead, Rock River Logistics Group
- Karol Mazurek, Manager of IT Infrastructure (for Item 4 only)
- Nadia Kowalczyk, Corporate Secretary, recording

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 1:02 p.m. and confirmed a quorum. Ms. Lindqvist moved approval of the minutes of the August 21, 2025 regular meeting as circulated; Mr. Mirchandani seconded. The motion carried 5–0.

Chair Brissette stated the purpose of the meeting: to receive the Janesville pilot readiness assessment and to decide whether the September 26 go-live date would hold. She reminded the committee that the date had already moved twice, from March 14 to July 11 to September 26, and said that a third slip would be treated by the board as a program failure rather than a schedule adjustment.

### 2. Standing Status Report — Program Manager

Mr. Wahlgren delivered the standing status report.

**Schedule.** Of the 11 milestones in Exhibit D of the Master Services Agreement dated April 12, 2024, seven were complete and accepted, one (Milestone 8, Pilot Acceptance) was in dispute, and three remained. The critical path ran through pilot acceptance, and Mr. Wahlgren reported the pilot had been in operation at Janesville for 39 days against a planned 21-day stabilization window.

**Budget.** Of the $6,800,000 contract value, $4,420,000 had been invoiced and paid, representing 65 percent. A further $1,100,000 tied to Milestone 8 had been invoiced by Meridian Yard Systems on August 29 and was being held unpaid pending acceptance. Internal program spending stood at $1,940,000 against an approved internal budget of $1,750,000, an overrun of $190,000 driven chiefly by contract labor.

**Risks.** Mr. Wahlgren identified four risks rated red: pilot defect burn-down rate, RF device response time under peak load, the parcel manifest interface, and the November 1 peak-season change freeze, which he noted was 58 days away and which would foreclose any production change through January 5, 2026.

### 3. Readiness and Defect Metrics — Janesville Pilot

Mr. Escalante presented the pilot metrics for the four weeks ended August 30, 2025, with defect data supplied by Ms. Deshmukh.

| Measure | Standard | Pilot result | Status |
|---|---|---|---|
| Pick accuracy | 99.20% | 62.0% | Fail |
| Inventory record accuracy | 99.50% | 88.4% | Fail |
| Order cycle time, receipt to trailer | 22 min | 41 min | Fail |
| RF scan response time | ≤ 1.0 sec | 3.8 sec | Fail |
| Same-day shipment completion | 98.0% | 79.6% | Fail |
| Cycle-count adjustment rate | ≤ 0.4% | 2.9% | Fail |
| Training completion, Janesville hourly | 100% | 71% | Fail |

**Open defect tickets: 218.** By severity: Severity 1 (production stopped), 9; Severity 2 (major function impaired, no workaround), 47; Severity 3 (impaired with workaround), 102; Severity 4 (cosmetic or documentation), 60. Ms. Deshmukh reported that 63 tickets had been opened and 44 closed in the preceding two weeks, a net increase of 19, and that the average age of an open Severity 2 ticket was 26 days against a contractual response commitment of 5 business days.

Mr. Escalante reported that Janesville had hired **14 temporary workers** to sustain manual workarounds, principally paper pick verification, a second-touch audit at the pack line, and manual entry of parcel labels. The incremental labor cost was $58,400 for the month of August, and he projected $71,000 for September if the workarounds continued. He stated that Janesville had not missed a customer commitment in the pilot period, but had done so only by absorbing overtime at 118 percent of plan and by holding two carrier appointments per day for late tenders. Ms. Lindqvist confirmed that Transportation had absorbed 41 late trailer departures at Janesville since July 28, with detention charges of $19,200.

Asked by Chair Brissette to characterize the pilot in one sentence, Mr. Escalante said the system was not producing correct work instructions and the site was manually correcting the system's output before it reached the floor.

### 4. Vendor Response

Ms. Dziedzic thanked the committee and responded on behalf of Meridian Yard Systems. She said Meridian did not dispute the accuracy figures as measured, but attributed the majority of the variance to three causes: incomplete master-data conversion in the item dimension file, for which she said Rock River retained responsibility under Section 6.2 of the Agreement; slotting logic configured to a rule set that Rock River's operations team had revised twice after design freeze; and RF hardware on the Janesville floor operating on access points that Meridian had flagged in its March infrastructure assessment.

Mr. Mazurek was invited to respond. He confirmed that 11 of 34 access points at Janesville predated 2019 and that a refresh had been scoped at $86,000 but deferred in the fiscal 2025 capital plan. He stated, however, that latency testing on August 26 showed 3.1 seconds average response on the newest access points, which he said indicated the delay was not principally a wireless problem.

Mr. Mirchandani said the item dimension file had been delivered to Meridian on May 9 in the format Meridian specified, and that Meridian had accepted it in writing on May 16. Ms. Dziedzic acknowledged the acceptance and said Meridian's position was that the file conformed to format but not to content.

Ms. Dziedzic committed that Meridian would place two additional configuration consultants on site at Janesville beginning September 15 at no charge to Rock River for a period of four weeks, and would deliver a written defect burn-down plan by September 12 showing all Severity 1 and Severity 2 tickets closed by October 10.

### 5. Decision on the September 26 Go-Live

Chair Brissette opened the floor. Mr. Mirchandani said that even on Meridian's own burn-down commitment, the earliest date at which two consecutive clean weeks of pick accuracy could be demonstrated was late October, which left no margin before the change freeze. Ms. Lindqvist said Transportation could not plan carrier capacity for peak against a system that might or might not be in production on November 1.

**Motion.** Mr. Mirchandani moved that the committee place the September 26 go-live on hold, that no cutover be scheduled until the exit criteria in Exhibit C were met and certified in writing by the Program Manager and the receiving Site Director, and that Meridian be notified in writing within two business days. Ms. Lindqvist seconded.

**Discussion.** Mr. Wahlgren asked that the motion not fix a new date, so that the committee would not be seen to have slipped a third time to a date it could not defend. The mover accepted this as friendly. Mr. Escalante said Janesville supported the hold and asked that the 14 temporary workers be authorized through October 31 regardless of the outcome.

**Vote.** The motion carried **5–0**. Voting aye: Brissette, Mirchandani, Escalante, Lindqvist, Wahlgren. Voting nay: none. Abstaining: none.

### 6. Closed Session — Contract Remedies

At 2:58 p.m., on motion by Chair Brissette, seconded by Mr. Wahlgren and carried 5–0, the committee resolved into closed session to receive advice of counsel concerning Rock River's rights and remedies under the Master Services Agreement. All non-members withdrew, including Ms. Dziedzic. Harlan Pruitt, General Counsel, joined for the closed session. Ms. Kowalczyk remained to record; a separate confidential minute was kept and sealed.

The committee returned to open session at 3:34 p.m. Chair Brissette reported, for the public record, that the committee had received a privileged briefing on the acceptance, cure, and termination provisions of the Agreement, had directed no action at this meeting, and had asked General Counsel to prepare a written options memorandum for the September 18 meeting.

### 7. Action Items Recorded

| # | Action | Owner | Due |
|---|---|---|---|
| 09-04-1 | Issue written notice to Meridian that go-live is on hold and Milestone 8 is not accepted | Anders Wahlgren | Sept 8, 2025 |
| 09-04-2 | Deliver defect burn-down plan closing all Sev 1 and Sev 2 tickets by Oct 10 | Rebecca Dziedzic | Sept 12, 2025 |
| 09-04-3 | Options memorandum on acceptance, cure, and termination remedies | Harlan Pruitt | Sept 16, 2025 |
| 09-04-4 | Re-validate item dimension file, 100 percent audit of 4,180 active SKUs | Priyanka Deshmukh | Sept 19, 2025 |
| 09-04-5 | Quote and schedule access point refresh at Janesville, 11 units | Karol Mazurek | Sept 15, 2025 |
| 09-04-6 | Extend 14 temporary workers at Janesville through Oct 31; report weekly cost | Tomas Escalante | Sept 9, 2025 |
| 09-04-7 | Model carrier capacity under both legacy and new-system peak scenarios | Freya Lindqvist | Sept 18, 2025 |
| 09-04-8 | Draft revised exit criteria certification form for Site Director sign-off | Anders Wahlgren | Sept 18, 2025 |

### 8. Next Meeting and Adjournment

The next regular meeting was set for Thursday, September 18, 2025, at 1:00 p.m. There being no further business, Chair Brissette adjourned the meeting at 3:41 p.m.

*Recorded by Nadia Kowalczyk, Corporate Secretary. Approved as circulated September 18, 2025.*

---

# MINUTES — REGULAR MEETING OF SEPTEMBER 18, 2025

**Body:** WMS Cutover Steering Committee, Rock River Logistics Group, Inc.
**Date:** Thursday, September 18, 2025
**Time:** Called to order at 1:00 p.m. Central; adjourned at 4:12 p.m. Central
**Place:** Corporate headquarters, 4400 Sandy Hollow Road, Rockford, Illinois — Executive Conference Room B, with a video bridge to Janesville

**Members present (voting):**
- Yolanda Brissette, Chief Operating Officer, Chair
- Sanjay Mirchandani, Vice President of Technology
- Tomas Escalante, Site Director, Janesville DC
- Freya Lindqvist, Director of Transportation
- Anders Wahlgren, Program Manager

**Members absent:** None.

**Others attending (non-voting):**
- Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems
- Curtis Adeyemi, Vice President of Delivery, Meridian Yard Systems (Items 3 and 4)
- Harlan Pruitt, General Counsel (Items 5 and 6)
- Delia Voss, Chief Financial Officer (Items 4 and 5, by invitation)
- Priyanka Deshmukh, WMS Functional Lead
- Nadia Kowalczyk, Corporate Secretary, recording

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 1:00 p.m. Mr. Wahlgren moved approval of the September 4 minutes as circulated; Mr. Escalante seconded. Carried 5–0.

### 2. Review of Open Action Items

Mr. Wahlgren reported on the eight items recorded September 4. Items 09-04-1, 09-04-3, 09-04-6, 09-04-7, and 09-04-8 were closed on time. Item 09-04-2, Meridian's burn-down plan, was delivered September 15, three days late. Item 09-04-4, the SKU audit, was 74 percent complete and Ms. Deshmukh requested an extension to September 30, which the Chair granted. Item 09-04-5 was closed: the access point refresh was quoted at $91,400 and scheduled for September 27–28.

### 3. Standing Status Report and Readiness Metrics

Mr. Wahlgren reported that no milestone had been accepted since the last meeting, that $1,100,000 remained withheld, and that internal program spending had reached $2,061,000, an overrun of $311,000.

Mr. Escalante and Ms. Deshmukh presented the pilot metrics for the two weeks ended September 13.

| Measure | Standard | Sept 13 | Aug 30 | Change |
|---|---|---|---|---|
| Pick accuracy | 99.20% | 71.4% | 62.0% | +9.4 pts |
| Inventory record accuracy | 99.50% | 90.1% | 88.4% | +1.7 pts |
| Order cycle time | 22 min | 38 min | 41 min | −3 min |
| RF scan response time | ≤ 1.0 sec | 3.4 sec | 3.8 sec | −0.4 sec |
| Same-day shipment completion | 98.0% | 83.2% | 79.6% | +3.6 pts |
| Training completion | 100% | 88% | 71% | +17 pts |

**Open defect tickets: 231**, a net increase of 13. Severity 1, 6; Severity 2, 51; Severity 3, 108; Severity 4, 66. Ms. Deshmukh reported 63 tickets opened and 50 closed in the period, and stated that 22 of the newly opened tickets were regressions in functions previously certified.

Mr. Escalante reported that the temporary workforce at Janesville had grown from 14 to **19**, that the September labor variance was tracking to $79,000, and that two of his four shift supervisors had submitted resignations since the last meeting. He said the regression rate, more than the raw defect count, was what concerned him: his floor leads had stopped trusting functions that had already been signed off.

### 4. Disputed Change Order CO-14 ($410,000)

Chair Brissette introduced Change Order 14, submitted by Meridian on September 9 in the amount of **$410,000**, covering rework of the parcel manifest interface, multi-owner inventory segregation for the 3PL billing model, and a redesigned wave planning screen.

Mr. Adeyemi presented for Meridian. He said the three items were outside the requirements baseline in Exhibit C, that multi-owner segregation had first been described in a June 3 workshop, and that the parcel rework had been driven by a carrier's specification change in April. He said Meridian had performed the work at risk in order to protect the schedule and was seeking payment for 1,640 consultant hours at the contracted blended rate of $250.

Mr. Mirchandani responded item by item. On multi-owner segregation he cited requirement identifiers WMS-INV-041 through WMS-INV-047 in Exhibit C, which he said described owner-level segregation in terms, and read WMS-INV-044 into the record. On parcel, he acknowledged the carrier specification change was external but noted Section 7.4 assigned carrier-specification maintenance to Meridian for the term of the implementation. On the wave planning screen, he conceded that Rock River operations had requested changes after design freeze and said approximately $95,000 of the claim appeared legitimate on that item alone.

Ms. Voss reported that paying CO-14 in full would bring total committed spend to $7,210,000, or 106 percent of contract value, before any of the remaining three milestones were accepted, and that the fiscal 2026 capital plan had no headroom for it.

**Motion.** Mr. Mirchandani moved that the committee reject Change Order 14 as submitted; that Rock River tender no payment on the multi-owner segregation and parcel manifest components, which the committee found to be within the requirements baseline; that Rock River offer, without prejudice and subject to General Counsel's review, to negotiate the wave planning component up to a ceiling of $95,000; and that the rejection be delivered in writing by September 24 with the requirement citations attached. Ms. Lindqvist seconded.

**Discussion.** Mr. Wahlgren cautioned that a flat rejection might slow Meridian's remediation effort at the moment the program could least afford it. Chair Brissette answered that the committee could not pay for the correction of work it had already bought. Mr. Escalante said Janesville had no view on the commercial question but asked that any negotiation not divert Meridian consultants from defect closure.

**Vote.** The motion carried **4–1**. Voting aye: Brissette, Mirchandani, Escalante, Lindqvist. Voting nay: Wahlgren. Abstaining: none. Mr. Wahlgren asked that his dissent be recorded on the ground that the timing, not the merits, was wrong.

### 5. Closed Session — Cure and Termination Provisions

At 2:47 p.m., on motion by Ms. Lindqvist, seconded by Mr. Mirchandani, carried 5–0, the committee entered closed session for the purpose of receiving privileged legal advice. Ms. Dziedzic and Mr. Adeyemi withdrew. Mr. Pruitt, Ms. Voss, and outside counsel Bettina Cho of Halloran & Pike participated. A sealed confidential minute was kept.

The committee returned to open session at 3:52 p.m. Chair Brissette reported in open session that the committee had reviewed the notice, cure, and termination architecture of the Agreement, specifically the 30-day cure period, the service-credit mechanism and its cap, and the dispute escalation ladder; that no notice was authorized at this meeting; and that counsel had been directed to prepare a cure notice in draft form so that the committee would be able to act without delay at a future meeting should it choose to do so.

### 6. Other Business

Ms. Lindqvist reported the results of the peak carrier capacity model requested on September 4. Under a legacy-system peak, Transportation could secure committed capacity at a premium of $114,000 over the fourth quarter. Under a new-system peak with unresolved cycle-time variance, carriers had quoted a premium of $290,000 to $340,000 to hold flexible capacity, and two of six core carriers had declined to quote at all. She asked the committee to note that carrier commitments for the fourth quarter had to be placed by October 10.

Mr. Wahlgren circulated the revised exit criteria certification form, which required two consecutive weeks at or above 99.2 percent pick accuracy, zero open Severity 1 defects, no more than 10 open Severity 2 defects, RF response at or below 1.0 second at ninety-fifth percentile, and countersignature by the receiving Site Director. On motion by Mr. Escalante, seconded by Mr. Wahlgren, the form was adopted **5–0** as the sole basis for any future cutover authorization.

### 7. Action Items Recorded

| # | Action | Owner | Due |
|---|---|---|---|
| 09-18-1 | Deliver written rejection of CO-14 with requirement citations | Sanjay Mirchandani | Sept 24, 2025 |
| 09-18-2 | Review and clear rejection letter before issuance | Harlan Pruitt | Sept 23, 2025 |
| 09-18-3 | Prepare cure notice in draft, hold for committee direction | Harlan Pruitt | Sept 30, 2025 |
| 09-18-4 | Root-cause analysis of 22 regression defects, written | Rebecca Dziedzic | Sept 26, 2025 |
| 09-18-5 | Complete SKU dimension audit (extension granted) | Priyanka Deshmukh | Sept 30, 2025 |
| 09-18-6 | Retention plan for Janesville supervisors and floor leads | Tomas Escalante | Oct 2, 2025 |
| 09-18-7 | Secure fourth-quarter carrier capacity under legacy scenario, priced | Freya Lindqvist | Oct 10, 2025 |
| 09-18-8 | Forecast full-year program cost including workaround labor | Delia Voss | Oct 2, 2025 |
| 09-18-9 | Brief Kettleman Foods account team on go-live hold | Yolanda Brissette | Sept 25, 2025 |

### 8. Next Meeting and Adjournment

The next regular meeting was set for Thursday, October 2, 2025. Chair Brissette adjourned the meeting at 4:12 p.m.

*Recorded by Nadia Kowalczyk, Corporate Secretary. Approved as circulated October 2, 2025.*

---

# MINUTES — REGULAR MEETING OF OCTOBER 2, 2025

**Body:** WMS Cutover Steering Committee, Rock River Logistics Group, Inc.
**Date:** Thursday, October 2, 2025
**Time:** Called to order at 1:04 p.m. Central; adjourned at 4:38 p.m. Central
**Place:** Corporate headquarters, 4400 Sandy Hollow Road, Rockford, Illinois — Executive Conference Room B, with video participation from Eau Claire and Janesville

**Members present (voting):**
- Yolanda Brissette, Chief Operating Officer, Chair
- Sanjay Mirchandani, Vice President of Technology
- Tomas Escalante, Site Director, Janesville DC
- Freya Lindqvist, Director of Transportation
- Anders Wahlgren, Program Manager

**Members absent:** None.

**Others attending (non-voting):**
- Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems
- Delia Voss, Chief Financial Officer
- Harlan Pruitt, General Counsel
- Lorna Fitzhugh, Director of Customer Solutions, account lead for Kettleman Foods, LLC
- Dwight Osei-Bonsu, Site Director, Eau Claire DC (by video)
- Priyanka Deshmukh, WMS Functional Lead
- Nadia Kowalczyk, Corporate Secretary, recording

---

### 1. Call to Order and Approval of Prior Minutes

Chair Brissette called the meeting to order at 1:04 p.m. Ms. Lindqvist moved approval of the September 18 minutes; Mr. Mirchandani seconded. Carried 5–0.

### 2. Review of Open Action Items

Mr. Wahlgren reported that items 09-18-1, 09-18-2, 09-18-3, 09-18-5, 09-18-8, and 09-18-9 were closed on time. Item 09-18-4, Meridian's regression root-cause analysis, was received September 30, four days late, and Mr. Mirchandani characterized it as two pages that restated the ticket list without analysis. Item 09-18-6 was closed with a retention plan carrying a cost of $47,000 in stay bonuses. Item 09-18-7 remained open with a due date of October 10.

### 3. Standing Status Report and Readiness Metrics

Mr. Wahlgren reported no milestone acceptances, $1,100,000 still withheld, and internal program spending of $2,214,000 against a $1,750,000 budget, an overrun of $464,000. Meridian had responded to the CO-14 rejection on September 29, declining the $95,000 offer and reserving all rights.

| Measure | Standard | Sept 27 | Sept 13 | Change |
|---|---|---|---|---|
| Pick accuracy | 99.20% | 83.9% | 71.4% | +12.5 pts |
| Inventory record accuracy | 99.50% | 93.8% | 90.1% | +3.7 pts |
| Order cycle time | 22 min | 33 min | 38 min | −5 min |
| RF scan response time | ≤ 1.0 sec | 1.9 sec | 3.4 sec | −1.5 sec |
| Same-day shipment completion | 98.0% | 88.7% | 83.2% | +5.5 pts |

**Open defect tickets: 196.** Severity 1, 3; Severity 2, 44; Severity 3, 91; Severity 4, 58. Ms. Deshmukh reported 41 opened and 76 closed, the first net reduction of the program. She attributed the improvement in RF response to the access point refresh completed September 28.

Mr. Escalante reported the temporary workforce had grown to **22** and that cumulative workaround labor since July 28 had reached $214,000. Ms. Voss added that when overtime, detention, stay bonuses, and the internal budget overrun were included, the total unbudgeted cost of the delay stood at **$412,000** as of September 30.

### 4. Eau Claire Deployment

Mr. Wahlgren reported that Eau Claire was scheduled as wave two, with a cutover window of October 24–27. Mr. Osei-Bonsu stated that Eau Claire had completed 92 percent of end-user training but that his conversion data set had not been validated, that he had no confidence in a system that had not yet succeeded at a smaller site, and that Eau Claire handled 38 percent of the network's cold-chain volume, where an inventory error carried product-loss consequences that Janesville's dry goods did not.

**Motion.** Mr. Escalante moved that the Eau Claire deployment be deferred indefinitely; that no wave-two site be scheduled until the Janesville pilot had been certified under the exit criteria form adopted September 18; and that Meridian be directed to release the four consultants staged for Eau Claire to Janesville defect closure. Mr. Mirchandani seconded.

**Discussion.** Ms. Dziedzic said Meridian would honor the redeployment but noted that its Exhibit D fee schedule assumed a wave-two start in October and that standby costs would be raised as a commercial matter. Chair Brissette answered that the committee had noted her reservation.

**Vote.** The motion carried **5–0**.

### 5. Kettleman Foods Chargeback and Notice

Ms. Fitzhugh reported that Kettleman Foods, LLC, which accounted for **31 percent of consolidated revenue**, had on September 30 issued a chargeback of **$290,000** under the service-level schedule of its master transportation and warehousing agreement, covering 61 late or short shipments from Janesville between August 4 and September 26, and had by letter of the same date placed its contract **on notice**, citing sustained failure of the on-time-in-full commitment. The letter required a written corrective action plan within 21 days and reserved Kettleman's right to terminate for cause on 90 days' notice if performance did not return to 98 percent on-time-in-full by December 31, 2025.

Ms. Voss stated that the chargeback would be recorded as a reduction of revenue in the third quarter and that loss of the Kettleman account would represent approximately $66 million of annual revenue against consolidated revenue of $214 million.

Chair Brissette said she had spoken with Kettleman's senior vice president of supply chain on October 1, that the conversation had been direct but not hostile, and that Kettleman's principal request had been predictability rather than speed. She reported that she had told Kettleman no further system changes would touch its volume without 30 days' written notice, and asked the committee to ratify that commitment.

**Motion.** Ms. Lindqvist moved that the committee ratify the Chair's commitment to Kettleman Foods of 30 days' written notice before any system change affecting Kettleman volume; that Ms. Fitzhugh and Mr. Escalante jointly deliver a corrective action plan to Kettleman by October 17; and that the committee receive a standing Kettleman performance report at every meeting until the notice was withdrawn. Mr. Wahlgren seconded. Carried **5–0**.

### 6. Composition of the Committee

Chair Brissette observed that the committee's business had moved from schedule management to contract remedy and financial exposure, and that the two officers whose functions bore the consequences were attending without a vote.

**Motion.** Chair Brissette moved that the committee be expanded to seven voting members by the addition of the Chief Financial Officer and the General Counsel, effective with the meeting of October 16, 2025; that quorum be five; and that the charter amendment be transmitted to the Chief Executive Officer for confirmation. Mr. Mirchandani seconded.

**Discussion.** Mr. Wahlgren asked whether a seven-member committee could still meet on a two-week cycle. The Chair replied that it would.

**Vote.** Carried **5–0**.

### 7. Closed Session — Contract Remedies

At 3:46 p.m., on motion by Mr. Mirchandani, seconded by Ms. Lindqvist, carried 5–0, the committee entered closed session. Ms. Dziedzic withdrew. Mr. Pruitt, Ms. Voss, and Ms. Cho participated. A sealed confidential minute was kept.

The committee returned to open session at 4:31 p.m. Chair Brissette reported that the committee had reviewed the draft cure notice prepared under item 09-18-3, had reviewed the interaction between Rock River's remedies against Meridian and Rock River's exposure to Kettleman, had reviewed the service-credit calculation to date, and had taken no action other than to place the question of issuing a cure notice on the agenda of the October 16 meeting as a matter for decision.

### 8. Action Items Recorded

| # | Action | Owner | Due |
|---|---|---|---|
| 10-02-1 | Notify Meridian in writing of Eau Claire deferral and consultant redeployment | Anders Wahlgren | Oct 6, 2025 |
| 10-02-2 | Corrective action plan to Kettleman Foods, jointly signed | Lorna Fitzhugh / Tomas Escalante | Oct 17, 2025 |
| 10-02-3 | Charter amendment to CEO for confirmation of expanded membership | Yolanda Brissette | Oct 9, 2025 |
| 10-02-4 | Final cure notice for committee decision, with 30-day cure plan requirements | Harlan Pruitt | Oct 14, 2025 |
| 10-02-5 | Service-credit calculation through Sept 30 under Section 9.6 | Delia Voss | Oct 14, 2025 |
| 10-02-6 | Written analysis: cost and feasibility of running Q4 peak on legacy system | Anders Wahlgren | Oct 14, 2025 |
| 10-02-7 | Re-baseline options for a Q1 2026 attempt, two scenarios with dates | Sanjay Mirchandani | Oct 14, 2025 |
| 10-02-8 | Substantive root-cause analysis of regression defects, replacing Sept 30 submission | Rebecca Dziedzic | Oct 10, 2025 |
| 10-02-9 | Close fourth-quarter carrier capacity under legacy scenario (carryover) | Freya Lindqvist | Oct 10, 2025 |
| 10-02-10 | Cold-chain conversion data validation plan for Eau Claire, held in reserve | Dwight Osei-Bonsu | Oct 30, 2025 |

### 9. Next Meeting and Adjournment

The next regular meeting was set for Thursday, October 16, 2025, at 1:00 p.m., and was designated a decision meeting. Chair Brissette adjourned at 4:38 p.m.

*Recorded by Nadia Kowalczyk, Corporate Secretary. Approved as circulated October 16, 2025.*

---

# MINUTES — REGULAR MEETING OF OCTOBER 16, 2025

**Body:** WMS Cutover Steering Committee, Rock River Logistics Group, Inc.
**Date:** Thursday, October 16, 2025
**Time:** Called to order at 1:00 p.m. Central; adjourned at 5:06 p.m. Central
**Place:** Corporate headquarters, 4400 Sandy Hollow Road, Rockford, Illinois — Executive Conference Room B

**Members present (voting):**
- Yolanda Brissette, Chief Operating Officer, Chair
- Sanjay Mirchandani, Vice President of Technology
- Tomas Escalante, Site Director, Janesville DC
- Freya Lindqvist, Director of Transportation
- Anders Wahlgren, Program Manager
- Delia Voss, Chief Financial Officer (first meeting as voting member)
- Harlan Pruitt, General Counsel (first meeting as voting member)

**Members absent:** None. All seven voting members were present; quorum of five satisfied.

**Others attending (non-voting):**
- Rebecca Dziedzic, Engagement Lead, Meridian Yard Systems
- Curtis Adeyemi, Vice President of Delivery, Meridian Yard Systems
- Bettina Cho, Halloran & Pike, outside counsel (closed session only)
- Lorna Fitzhugh, Director of Customer Solutions
- Priyanka Deshmukh, WMS Functional Lead
- Nadia Kowalczyk, Corporate Secretary, recording

---

### 1. Call to Order, Seating of New Members, Approval of Prior Minutes

Chair Brissette called the meeting to order at 1:00 p.m. She reported that the Chief Executive Officer had confirmed the charter amendment adopted October 2 by memorandum dated October 9, and she seated Ms. Voss and Mr. Pruitt as voting members. Mr. Wahlgren moved approval of the October 2 minutes; Mr. Escalante seconded. Carried 7–0, the new members voting.

Chair Brissette stated that the November 1 peak-season change freeze was 16 days away, that no production change could be made between November 1 and January 5 under standing policy, and that the committee would therefore decide at this meeting rather than defer.

### 2. Review of Open Action Items

Mr. Wahlgren reported items 10-02-1 through 10-02-7 and 10-02-9 closed on time. Item 10-02-10 remained open with a due date of October 30. Item 10-02-8, Meridian's substantive regression analysis, was delivered October 14, four days late; Mr. Mirchandani reported that the document was materially improved and identified a defect in the allocation engine's handling of partial-pallet reservations as the common cause of 17 of the 22 regressions.

### 3. Standing Status Report and Readiness Metrics

| Measure | Standard | Oct 11 | Sept 27 | Change |
|---|---|---|---|---|
| Pick accuracy | 99.20% | 91.6% | 83.9% | +7.7 pts |
| Inventory record accuracy | 99.50% | 96.2% | 93.8% | +2.4 pts |
| Order cycle time | 22 min | 28 min | 33 min | −5 min |
| RF scan response, 95th percentile | ≤ 1.0 sec | 1.2 sec | 1.9 sec | −0.7 sec |
| Same-day shipment completion | 98.0% | 92.4% | 88.7% | +3.7 pts |
| Kettleman on-time-in-full | 98.0% | 93.1% | 86.5% | +6.6 pts |

**Open defect tickets: 171.** Severity 1, 1; Severity 2, 29; Severity 3, 84; Severity 4, 57. Ms. Deshmukh reported 34 opened and 59 closed. Mr. Wahlgren stated plainly that the trend was good and the level was not: against the adopted exit criteria, the pilot required zero Severity 1, no more than 10 Severity 2, and two consecutive weeks at 99.2 percent pick accuracy, and on the current burn-down rate the earliest credible certification date was the week of December 8, inside the freeze.

Mr. Escalante reported the temporary workforce at **26** and cumulative unbudgeted cost, per Ms. Voss's October 14 submission, of **$688,000** since July 28.

### 4. Vendor Position

Mr. Adeyemi presented Meridian's position. He said Meridian believed a November 14 cutover at Janesville was achievable if Rock River would waive the two-week accuracy observation window in favor of a five-business-day window, and offered to fund six consultants on site through December 31 at Meridian's cost. He asked the committee not to issue any formal notice, stating that a notice would trigger Meridian's own internal escalation procedures and would, in his experience, slow rather than accelerate the work.

Ms. Dziedzic added that Meridian accepted responsibility for the allocation engine defect and had committed a fix for October 27, and said that Meridian would withdraw the standby cost claim raised October 2 if the parties reached a negotiated re-baseline.

Mr. Pruitt asked whether Meridian would agree to a written remediation plan with dated deliverables and defined acceptance tests. Mr. Adeyemi said Meridian would, but preferred it as a jointly signed plan rather than as a response to a notice. Chair Brissette thanked the vendor representatives, who then withdrew for the remainder of the meeting.

### 5. Closed Session — Contract Remedies and Customer Exposure

At 2:22 p.m., on motion by Mr. Pruitt, seconded by Ms. Voss, carried 7–0, the committee entered closed session. Ms. Fitzhugh and Ms. Deshmukh withdrew; Ms. Cho joined. A sealed confidential minute was kept.

The committee returned to open session at 4:01 p.m. Chair Brissette reported that the committee had received the final cure notice prepared under item 10-02-4, the service-credit calculation under item 10-02-5, the legacy-peak analysis under item 10-02-6, and the two re-baseline scenarios under item 10-02-7; that it had received advice on the consequences of issuing and of not issuing a cure notice, including the effect on Rock River's position with Kettleman Foods; and that it was prepared to act in open session.

For the record, the Chair reported the following figures from the closed materials, which the committee agreed could be disclosed: service credits accrued through September 30 of $476,000 against a contractual cap of $1,020,000; the cost of operating the fourth-quarter peak on the legacy system, including retained temporary labor, extended license and support, and carrier premium, of $1,240,000; and Mr. Mirchandani's two re-baseline scenarios, being a February 21, 2026 cutover at reduced scope and an April 18, 2026 cutover at full scope.

### 6. Principal Motion

**Motion.** Chair Brissette moved, and Ms. Lindqvist seconded, that the committee:

**(a)** direct the General Counsel to issue to Meridian Yard Systems, no later than October 22, 2025, a formal notice of material breach and demand for cure under the Master Services Agreement, specifying the acceptance failures at the Janesville pilot, the unclosed Severity 1 and Severity 2 defects, and the missed Exhibit D milestone dates, and requiring a written cure plan within 10 business days and cure within the contractual 30-day period;

**(b)** direct that the fourth-quarter peak season be operated in its entirety on the legacy warehouse management system at all six distribution centers, that the Janesville pilot be reduced to a non-production parallel configuration effective October 31, 2025, and that the November 1 change freeze be observed without exception; and

**(c)** direct the Program Manager and the Vice President of Technology to re-baseline the program scope and schedule for a cutover attempt in **February 2026**, taking the February 21, 2026 reduced-scope scenario as the planning basis, and to return a re-baselined plan, budget, and revised Exhibit D for committee approval no later than December 11, 2025.

**Discussion.** Mr. Escalante spoke in favor, saying Janesville could not carry a fourth quarter on manual verification with 26 temporary workers and two supervisor vacancies. Ms. Lindqvist said carrier capacity had been contracted on October 10 against the legacy scenario and that reversing it would cost more than the committee had been told. Ms. Voss said the $1,240,000 legacy peak cost was defensible only if it purchased certainty, and asked whether clause (c) locked the company into February. The Chair replied that clause (c) set a planning basis and that approval of the plan itself would return to the committee in December.

Mr. Mirchandani spoke against. He said he supported (b) and (c) without reservation but could not support (a) in the same motion; that the defect trend of the past six weeks was the best of the program; that the allocation engine root cause had only just been found; and that issuing a notice in the same week Meridian had offered six funded consultants would, in his judgment, cost the program more capability than the notice would recover. He asked that (a) be divided and voted separately. Chair Brissette put the question of division.

**Vote on division.** The motion to divide failed **3–4**. Voting aye: Mirchandani, Wahlgren, Voss. Voting nay: Brissette, Escalante, Lindqvist, Pruitt.

Ms. Voss then spoke against the motion as a whole, stating that she would have supported a notice paired with a negotiated settlement of CO-14 and the withheld $1,100,000, and that issuing a notice while $1,100,000 was withheld and CO-14 was rejected placed three disputes in front of the vendor at once with no path to close any of them.

Mr. Pruitt responded that the 30-day cure period was itself the negotiating window, and that failing to issue a notice before the freeze would leave Rock River without a documented breach record if the February attempt also failed.

**Vote on the principal motion.** The motion carried **5–2**. Voting aye: Brissette, Escalante, Lindqvist, Wahlgren, Pruitt. Voting nay: Mirchandani, Voss. Abstaining: none. Both dissenting members asked that their reasons, as stated above, be recorded, and the Chair so directed.

### 7. Related Motions

**Motion.** Ms. Voss moved that no further payment be released to Meridian, including the withheld $1,100,000, until the committee had accepted a cure plan under the notice; and that the accrued service credits of $476,000 be formally asserted in writing concurrently with the cure notice. Mr. Pruitt seconded. Carried **7–0**.

**Motion.** Ms. Lindqvist moved that the Janesville temporary workforce be reduced from 26 to 8 effective November 7, 2025, retaining 8 through December 31 for cycle-count recovery, and that the retention bonuses adopted September 18 be extended through March 31, 2026 for Janesville supervisors and floor leads. Mr. Escalante seconded. Carried **7–0**.

**Motion.** Mr. Wahlgren moved that Ms. Fitzhugh be directed to inform Kettleman Foods in writing within three business days that Rock River would operate the fourth quarter on the legacy system and that no system change would affect Kettleman volume before February 2026. Ms. Voss seconded. Carried **7–0**.

### 8. Personnel Announcement and Succession

Mr. Escalante announced that he had submitted his resignation and that his last day with the company would be **November 6, 2025**, three weeks from the date of the meeting. He said his decision was personal and had been made before the day's vote, that he had accepted a position outside the third-party logistics sector, and that he had informed Chair Brissette on October 14.

Chair Brissette thanked Mr. Escalante on behalf of the committee and stated for the record that his presentation of the Janesville metrics on September 4 had been the single most consequential contribution to the program's course. She noted the committee would lose both its only site-level voting member and its most detailed operating knowledge of the pilot at the moment the re-baseline work began.

**Motion.** Mr. Mirchandani moved that Mr. Escalante be directed to prepare a written pilot handover dossier covering defect history, workaround inventory, master-data exceptions, and floor-level configuration deviations, to be delivered before his departure; that Chair Brissette appoint an interim Janesville site director and nominate a replacement voting member for the committee by November 6; and that the seat be filled permanently by the December 11 meeting. Ms. Lindqvist seconded. Carried **7–0**, Mr. Escalante voting aye.

### 9. Action Items Recorded

| # | Action | Owner | Due |
|---|---|---|---|
| 10-16-1 | Issue formal cure notice and concurrent assertion of $476,000 in service credits | Harlan Pruitt | Oct 22, 2025 |
| 10-16-2 | Notify Meridian of legacy-peak decision and non-production status of Janesville pilot | Anders Wahlgren | Oct 20, 2025 |
| 10-16-3 | Return Janesville to full legacy operation; certify completion | Tomas Escalante | Oct 31, 2025 |
| 10-16-4 | Reduce temporary workforce 26 to 8; extend retention bonuses to Mar 31, 2026 | Tomas Escalante | Nov 7, 2025 |
| 10-16-5 | Written notice to Kettleman Foods of Q4 legacy operation and change moratorium | Lorna Fitzhugh | Oct 21, 2025 |
| 10-16-6 | Pilot handover dossier | Tomas Escalante | Nov 5, 2025 |
| 10-16-7 | Appoint interim Janesville site director; nominate replacement committee member | Yolanda Brissette | Nov 6, 2025 |
| 10-16-8 | Re-baselined scope, schedule, budget, and revised Exhibit D for February 2026 attempt | Anders Wahlgren / Sanjay Mirchandani | Dec 11, 2025 |
| 10-16-9 | Evaluate Meridian cure plan when received; recommend acceptance or rejection | Sanjay Mirchandani | 5 business days after receipt |
| 10-16-10 | Hold all payment to Meridian pending accepted cure plan | Delia Voss | Ongoing |
| 10-16-11 | Cold-chain conversion data validation plan for Eau Claire (carryover) | Dwight Osei-Bonsu | Oct 30, 2025 |
| 10-16-12 | Report to the Board of Directors on the cure notice and revised program plan | Yolanda Brissette | Nov 13, 2025 |

### 10. Next Meeting and Adjournment

Chair Brissette announced that the committee would meet on Thursday, October 30, 2025, and would then move to a monthly cycle for November and December, resuming the two-week cycle on January 8, 2026, subject to the receipt of Meridian's cure plan, which if received would be taken up at a special meeting within five business days.

There being no further business, Chair Brissette adjourned the meeting at 5:06 p.m.

*Recorded by Nadia Kowalczyk, Corporate Secretary. Submitted for approval at the meeting of October 30, 2025.*
