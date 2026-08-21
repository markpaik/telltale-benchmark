# HURON STACK, INC.

## RELIABILITY REVIEW BOARD

### MINUTES OF FOUR CONSECUTIVE MEETINGS

### August 20, August 27, September 3, and September 10, 2025

---

---

## MEETING OF WEDNESDAY, AUGUST 20, 2025

**Body:** Reliability Review Board, Huron Stack, Inc.

**Date:** Wednesday, August 20, 2025

**Time:** Called to order at 2:00 p.m. Eastern Daylight Time; adjourned at 4:12 p.m. Eastern Daylight Time

**Place:** Conference Room 3B ("Cavendish"), 411 North Fourth Avenue, Ann Arbor, Michigan, with remote participation by video conference

**Members Present:** Meilin Zhao, Vice President of Engineering, Chair; Abdirahman Yusuf, Principal Site Reliability Engineer; Gwen Petrosyan, Director of Support; Ivo Radulescu, Staff Security Engineer; Tanisha Whitfield, Director of Customer Success

**Members Absent:** None

**Others Attending:** Peter Ostrowski, Chief Technology Officer, ex officio; Dana Kurniawan, Senior Technical Program Manager, recording secretary; Rosalind Achebe, Associate General Counsel (present for Items 4 and 5 only); Hollis Bergstrom, Staff Engineer, Control Plane Team (present for Item 2 only, by invitation)

---

### 1. Call to Order and Establishment of the Board

Chair Zhao called the meeting to order at 2:00 p.m. and stated that this was the first meeting of the Reliability Review Board, constituted by memorandum of the Chief Technology Officer dated August 14, 2025, following the control plane failure of August 12, 2025.

Zhao read the charter language into the record. The board is charged with reviewing all severity-one and severity-two incidents, maintaining the service level objective error budget for the deployment control plane, recommending release gating decisions to the Engineering Leadership Team, and reporting monthly to the Chief Technology Officer. The board holds authority to recommend, and in the case of release gating and error budget enforcement, to decide. Decisions requiring capital expenditure above one hundred thousand dollars or headcount changes remain subject to executive approval.

Zhao stated that the board would meet Wednesdays at 2:00 p.m. Eastern until further notice. Four members constitute a quorum. Ostrowski attends ex officio and does not vote.

Kurniawan was appointed recording secretary by the Chair without objection.

### 2. Standing Item — Incident Review: INC-2025-0812 (Control Plane Deployment Failure)

Yusuf presented the incident timeline, assisted by Bergstrom. The board walked the timeline event by event.

**Timeline as recorded.** At 03:41 EDT on August 12, the internal certificate authority issued a rotation for the mutual TLS certificate used between the control plane scheduler and the regional deployment agents. The prior certificate had been issued on August 12, 2024 with a 365-day validity window and had expired at 03:12 EDT. The automated rotation job had been disabled on July 29 during a migration of the secrets management service and was never re-enabled. At 03:12 the regional agents began rejecting scheduler connections.

At 03:19 the first automated alert fired to the on-call pager for the platform team. Yusuf noted that the alert was titled "agent heartbeat degraded (us-east-2)" and was classified as severity three by the alert routing rules, which meant it did not page a secondary responder or open a bridge.

At 04:02 the primary on-call engineer acknowledged the page and began investigation. At 04:31 the engineer escalated to severity two. At 04:40 an incident bridge was opened. At 05:15 the incident was escalated to severity one after support confirmed customer-reported deployment failures across three regions.

At 05:50 the responding team identified the expired certificate. At 06:20 a manual certificate issuance was completed and pushed to the first region. Yusuf stated that recovery was expected at that point and did not occur.

Yusuf then described what he called the compounding failure. On August 8, a configuration change to the agent connection retry policy had been merged and deployed. The change reduced the retry backoff ceiling from 300 seconds to 30 seconds and removed a jitter parameter. The change was authored by a contractor engineer, approved by a single reviewer who was the change author's direct manager, and was not reviewed by the control plane owning team. Under normal conditions the change was benign. Following the certificate restoration, approximately 41,000 agents attempted reconnection in a synchronized pattern and saturated the scheduler's connection accept queue. The scheduler entered a crash-restart cycle that persisted from 06:22 to 11:40.

At 09:05 the team identified the retry storm as the cause of the failed recovery. At 09:48 a rate-limiting configuration was applied at the load balancer. At 10:30 the first region recovered. At 11:40 the final region recovered. At 12:26 the incident was declared resolved.

**Duration.** Yusuf stated total customer-impacting duration as nine hours and fourteen minutes, measured from 03:12 to 12:26.

**Scope.** Petrosyan reported that 1,880 customers of the 3,200 total customer base experienced complete deployment unavailability. The remaining 1,320 customers were on the legacy single-tenant deployment path, which does not use the affected scheduler, and were unaffected.

Radulescu asked whether any security exposure arose from the manual certificate issuance. Bergstrom stated the manual issuance used the standard hardware security module workflow with two-person control and that the issued certificate carried a 90-day validity. Radulescu asked that the shortened validity be logged as a tracked item so that it does not itself expire unremarked in November. Zhao agreed and this became Action Item 2025-08-20-03.

Yusuf identified two contributing conditions beyond the immediate causes. First, no monitoring existed for certificate expiry as a leading indicator; the only signal was the failure itself. Second, the alert routing rules classified agent heartbeat degradation as severity three, which Yusuf characterized as a misclassification dating to a 2023 rules revision.

Petrosyan added a third. She stated that the support team received 214 tickets between 03:30 and 05:00 and that the ticket volume itself was a stronger signal than any monitoring alert, but that no mechanism existed to route ticket volume anomalies to the engineering on-call. Zhao asked her to draft a proposal. This became Action Item 2025-08-20-04.

Ostrowski asked whether the contractor engineer who authored the August 8 change had been identified for any consequence. Zhao stated that the board's charter is causal and systemic, not disciplinary, and that in her view the failure was in the review requirement rather than in the individual. Radulescu concurred and stated that a change of that nature ought not to have been mergeable with a single reviewer regardless of who wrote it. Ostrowski accepted the response and withdrew the question.

### 3. Standing Item — Error Budget Review

Yusuf presented the error budget position for the deployment control plane. The published service level objective is 99.9 percent monthly availability, which permits 43 minutes and 12 seconds of unavailability in a 30-day window.

The August 12 incident consumed 554 minutes against a 43-minute budget. Yusuf stated the budget was exhausted at 1,282 percent of allowance and that the rolling 90-day budget was also exhausted, standing at 412 percent of allowance.

Yusuf stated that under the error budget policy adopted by the Engineering Leadership Team in March 2024, exhaustion of the monthly budget triggers a mandatory reliability review and gives the reliability owner discretion to recommend a feature freeze. He said he was not making that recommendation at this meeting and wished to see whether the corrective actions held.

### 4. Customer Impact and Service Credits

Whitfield reported on customer response. She stated that 640 of the 1,880 affected customers had contacted their account teams within 72 hours of the incident. Eleven customers requested written root cause analyses under contractual entitlement. Four customers requested calls with an executive.

Whitfield presented the service credit estimate. Under the standard master service agreement, availability below 99.9 percent in a month entitles the customer to a credit of 10 percent of monthly recurring revenue; below 99.0 percent, 25 percent; below 95.0 percent, 50 percent. The August 12 incident placed all 1,880 affected customers below the 99.0 percent tier and 1,140 of them below the 95.0 percent tier for the month.

Whitfield stated the estimated credit exposure at $1.2 million. She noted this figure carried three qualifications: it assumed no further August incidents; it excluded 47 customers on negotiated agreements with higher credit multiples, which were being calculated separately by Finance; and it represented credits owed rather than credits claimed, which historically ran at approximately 70 percent of owed.

Achebe stated that the credit obligation attaches on breach and not on claim, and that the company's revenue recognition treatment required the full $1.2 million be recorded as a contra-revenue accrual regardless of claim rate. She stated she had already advised the Controller accordingly.

Zhao directed that the $1.2 million figure be recorded in the minutes as the board's estimate as of August 20, 2025, subject to revision.

Petrosyan reported support ticket volume for the week following the incident at 1,847 tickets, against a trailing four-week average of 620. She stated her team had absorbed the volume with 94 hours of unplanned overtime across eleven agents and that two agents had raised concerns about sustainability.

### 5. New Business — Preliminary Discussion of Postmortem Publication

Zhao raised the question of whether the company would publish a public postmortem. She stated she was not seeking a decision at this meeting but wanted the question on the record early.

Whitfield stated that seven customers had specifically asked whether a public postmortem would be issued and that in her experience the absence of one was read as concealment.

Radulescu stated that a public postmortem describing an expired certificate and an unreviewed configuration change discloses information about internal controls that has some value to an adversary, though he characterized that value as modest.

Achebe stated that any public document would need legal review and that she would want to understand the SOC 2 examination status before advising, because a published admission of a control failure during an examination window creates a question for the auditor that is better anticipated than discovered.

Zhao deferred the matter. This became a standing agenda item.

### 6. Action Items

| No. | Item | Owner | Due |
|---|---|---|---|
| 2025-08-20-01 | Re-enable automated certificate rotation for all mutual TLS certificates and add expiry monitoring at 30, 14, and 7 days | Abdirahman Yusuf | August 26, 2025 |
| 2025-08-20-02 | Reclassify agent heartbeat alerts from severity three to severity two and require secondary page | Abdirahman Yusuf | August 26, 2025 |
| 2025-08-20-03 | Track the 90-day manual certificate issued August 12 to rotation before November 10, 2025 | Ivo Radulescu | August 26, 2025 |
| 2025-08-20-04 | Draft proposal for routing support ticket volume anomalies to engineering on-call | Gwen Petrosyan | September 3, 2025 |
| 2025-08-20-05 | Deliver finalized service credit calculation including negotiated-agreement customers | Tanisha Whitfield | September 3, 2025 |
| 2025-08-20-06 | Draft change management control requiring owning-team review for all control plane configuration changes | Meilin Zhao | August 27, 2025 |
| 2025-08-20-07 | Complete written root cause analyses for the eleven customers holding contractual entitlement | Gwen Petrosyan | September 5, 2025 |

### 7. Adjournment

There being no further business, Zhao adjourned the meeting at 4:12 p.m. The next meeting was set for Wednesday, August 27, 2025 at 2:00 p.m.

*Respectfully submitted, Dana Kurniawan, Recording Secretary. Approved August 27, 2025.*

---

---

## MEETING OF WEDNESDAY, AUGUST 27, 2025

**Body:** Reliability Review Board, Huron Stack, Inc.

**Date:** Wednesday, August 27, 2025

**Time:** Called to order at 2:03 p.m. Eastern Daylight Time; adjourned at 4:47 p.m. Eastern Daylight Time

**Place:** Conference Room 3B ("Cavendish"), 411 North Fourth Avenue, Ann Arbor, Michigan, with remote participation by video conference

**Members Present:** Meilin Zhao, Chair; Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield

**Members Absent:** None

**Others Attending:** Peter Ostrowski, Chief Technology Officer, ex officio; Dana Kurniawan, recording secretary; Rosalind Achebe, Associate General Counsel; Emeka Duarte, Director of Product Management (present for Item 5 only, by invitation)

---

### 1. Call to Order and Approval of Prior Minutes

Zhao called the meeting to order at 2:03 p.m. and noted a quorum.

Radulescu moved to approve the minutes of August 20, 2025 as distributed. Petrosyan seconded. Whitfield requested one correction: that her service credit estimate be recorded as $1.2 million rather than "approximately $1.2 million," as the figure was a calculation and not an approximation. Zhao accepted the correction as friendly.

**Vote:** Approved as corrected, 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

### 2. Standing Item — Incident Review

**a. INC-2025-0812 corrective action status.**

Yusuf reported on Action Items 2025-08-20-01 and 02. Automated certificate rotation was re-enabled on August 22 across all thirteen mutual TLS certificate pairs. Expiry monitoring at 30, 14, and 7 days was deployed August 25. Yusuf stated that the monitoring surfaced two additional certificates expiring within 45 days that had not been on any tracked list, and that both had been rotated on August 25. Zhao asked that this finding be noted in the minutes as evidence that the gap was not isolated to the single certificate involved in the incident. Yusuf agreed.

Alert reclassification was completed August 24. Radulescu confirmed Action Item 03 was logged in the security tracking system with a hard due date of November 3, 2025.

**b. INC-2025-0827 (Scheduler Connection Saturation).**

Yusuf reported a new severity-one incident that had occurred that morning, from 06:14 to 07:01 EDT, a duration of 47 minutes.

He described the cause. A scheduled batch reconciliation job, which runs at 06:00 daily, triggered a re-registration sweep across all agents in the us-west-1 and eu-central-1 regions. Under the retry policy configuration, which had been partially but not fully reverted following the August 12 incident, the sweep produced the same connection accept queue saturation observed on August 12. The scheduler entered a restart cycle. Recovery occurred when the rate limiting applied on August 12 as an emergency measure engaged and shed load.

Yusuf stated plainly that this was the same subsystem, the same failure mode, and in substantial part the same unremediated condition. He stated that the August 12 emergency rate limit had been treated as a stopgap and that the underlying retry configuration had been placed on the backlog rather than fixed, and that this was his own error of prioritization.

Zhao asked whether the August 12 remediation plan had specified the retry configuration as a required action. Yusuf said it had, as item seven of eleven, with no date attached. Zhao asked why no date was attached. Yusuf said the remediation plan had been written at 02:00 on August 13 and that item seven had been the last thing written.

Ostrowski stated that he did not want the board to spend its time on self-criticism and asked what the fix was. Yusuf stated that the full retry policy revert with restored jitter was in review and would deploy August 28, and that a permanent admission control layer in front of the scheduler was scoped at approximately six engineer-weeks.

Petrosyan reported customer impact of the August 27 incident. All 1,880 customers on the multi-tenant path were affected. Support received 380 tickets. She stated that 62 of those tickets came from customers who had also filed on August 12, and that the language in those tickets was materially different in tone. She read two examples into the record at Zhao's request.

Whitfield stated that the August 27 incident, though short, would push affected customers into a second consecutive month of service level objective breach and that the credit exposure for September would begin from an already-compromised position. She stated she could not yet quantify.

### 3. Standing Item — Error Budget Review

Yusuf presented. The monthly budget for August was consumed at 1,391 percent of allowance following the August 27 incident, total unavailability standing at 601 minutes against 43 minutes permitted. The rolling 90-day budget stood at 447 percent.

Yusuf stated that under the error budget policy, two exhaustions in a single window with a shared causal subsystem constituted the condition under which he was obligated to recommend enforcement action rather than merely permitted to.

### 4. Old Business — Change Management Control

Zhao presented the draft change management control prepared under Action Item 2025-08-20-06. The control would require that any configuration change to control plane components receive review and approval from a member of the control plane owning team, that the reviewer not report to and not be reported to by the author, and that the approval be recorded in the change management system with a stated rationale.

Radulescu supported the control and proposed an amendment adding that emergency changes made during an active incident be exempt from pre-approval but require retroactive review within two business days. Zhao accepted the amendment.

Yusuf raised a concern about throughput, stating that the control plane owning team was seven engineers and that routing all configuration changes through them created a bottleneck. Zhao stated that the bottleneck was the point.

**Motion:** Radulescu moved to adopt the change management control as amended and to recommend it to the Engineering Leadership Team for immediate implementation. Whitfield seconded.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

### 5. New Business — Proposed Error Budget Freeze

Zhao introduced the principal item of business. She stated that in light of two error budget exhaustions in sixteen days arising from the same subsystem, she was proposing an error budget freeze on feature development for the deployment control plane and its dependent services, effective immediately and running through September 30, 2025.

She described the freeze terms. All engineering capacity on the affected services would be directed to reliability work. No new feature merges would be accepted. Bug fixes, security patches, and reliability work would proceed. The freeze would be reviewed weekly by this board.

Zhao stated the consequence directly: the 4.0 release, scheduled for October 6, 2025, could not be delivered on that date under the freeze. She estimated a slip of at least four weeks and possibly more.

Duarte was recognized. He stated that 4.0 had been announced to customers at the June user conference with an October date, that three of the top twenty accounts had made purchasing decisions contingent on 4.0 features, and that the sales team had approximately $6 million in pipeline attributed to 4.0 capability. He stated he was not opposing the freeze but wanted the cost on the record.

Whitfield stated that she had a view on this and that it differed from what Duarte might expect. She stated that the customers who had bought on the 4.0 roadmap were also the customers who had been down for nine hours on August 12, and that in her conversations the appetite for new features had substantially diminished relative to the appetite for the platform working. She stated she would rather explain a delayed release than a third outage.

Petrosyan concurred and added that her team could not absorb a major release on top of the current ticket volume in any case.

Radulescu supported the freeze and stated that from a security standpoint the change management control adopted under Item 4 would be materially harder to enforce under release pressure.

Yusuf supported the freeze and stated that he had asked for it in substance by declining to ask for it the week prior, which he now regarded as an error.

Ostrowski stated that he would support the board's decision and would carry it to the Chief Executive Officer himself. He asked that the board not set a new release date at this meeting, on the ground that a date set under duress and missed again would cost more than the current delay. Zhao agreed.

**Motion:** Yusuf moved to declare an error budget freeze on the deployment control plane and dependent services, effective August 27, 2025 and running through September 30, 2025, with weekly review by this board, and to notify the Engineering Leadership Team that the 4.0 release scheduled for October 6, 2025 cannot be delivered on that date. Petrosyan seconded.

**Discussion on the motion.** Whitfield asked whether the motion should specify a new release date. Zhao stated it should not, per the discussion above. Duarte asked whether the freeze could carve out the three features tied to named accounts. Yusuf stated that a carve-out reintroduces exactly the review-pressure condition that produced the August 8 change. Zhao declined the carve-out.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

Zhao directed that the decision be communicated to the Engineering Leadership Team by end of day August 27 and to affected customers through account teams no later than September 2.

### 6. Standing Item — Postmortem Publication

Zhao raised the standing item. Achebe reported that she had been informed that Kestrel Assurance, the company's SOC 2 examiner, had scheduled interim testing for the week of September 1 and that she recommended the board defer any publication decision until the examination position was known.

Radulescu stated that the August 27 incident changed the calculation, because a published postmortem for August 12 that did not also address August 27 would be incomplete on the day it was issued.

Zhao deferred the item to September 3.

### 7. Action Items

| No. | Item | Owner | Due |
|---|---|---|---|
| 2025-08-27-01 | Deploy full retry policy revert with restored jitter parameter | Abdirahman Yusuf | August 28, 2025 |
| 2025-08-27-02 | Scope and staff permanent admission control layer for scheduler | Abdirahman Yusuf | September 10, 2025 |
| 2025-08-27-03 | Communicate freeze decision and 4.0 slip to Engineering Leadership Team | Meilin Zhao | August 27, 2025 |
| 2025-08-27-04 | Prepare customer communication regarding 4.0 timing for account team delivery | Tanisha Whitfield | September 2, 2025 |
| 2025-08-27-05 | Submit change management control to Engineering Leadership Team for implementation | Meilin Zhao | August 29, 2025 |
| 2025-08-27-06 | Prepare support staffing plan addressing overtime sustainability | Gwen Petrosyan | September 10, 2025 |
| 2025-08-27-07 | Retroactive review of all emergency changes made August 12 and August 27 | Ivo Radulescu | September 3, 2025 |

### 8. Adjournment

Zhao adjourned the meeting at 4:47 p.m. The next meeting was set for Wednesday, September 3, 2025 at 2:00 p.m.

*Respectfully submitted, Dana Kurniawan, Recording Secretary. Approved September 3, 2025.*

---

---

## MEETING OF WEDNESDAY, SEPTEMBER 3, 2025

**Body:** Reliability Review Board, Huron Stack, Inc.

**Date:** Wednesday, September 3, 2025

**Time:** Called to order at 2:00 p.m. Eastern Daylight Time; adjourned at 5:34 p.m. Eastern Daylight Time

**Place:** Conference Room 3B ("Cavendish"), 411 North Fourth Avenue, Ann Arbor, Michigan, with remote participation by video conference

**Members Present:** Meilin Zhao, Chair; Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield

**Members Absent:** None

**Others Attending:** Peter Ostrowski, Chief Technology Officer, ex officio; Dana Kurniawan, recording secretary; Rosalind Achebe, Associate General Counsel; Marguerite Delacroix-Hyun, Chief Financial Officer (present for Items 4 and 5 only); Solomon Farkas, Engagement Partner, Kestrel Assurance LLP (present for Item 3 only, by invitation)

---

### 1. Call to Order and Approval of Prior Minutes

Zhao called the meeting to order at 2:00 p.m. and noted a quorum. She stated the agenda would be taken out of the customary order to accommodate Farkas, who was present by invitation for a limited time.

Whitfield moved to approve the minutes of August 27, 2025 as distributed. Yusuf seconded.

**Vote:** Approved 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

### 2. Standing Item — Incident and Error Budget Review

Yusuf reported no severity-one or severity-two incidents in the period August 28 through September 3. The retry policy revert deployed August 28 as scheduled. The scheduler had processed two full reconciliation sweeps without saturation.

He presented the error budget position. August closed at 601 minutes of unavailability against 43 permitted, 1,391 percent of allowance. September stood at zero minutes consumed as of the meeting. The rolling 90-day budget stood at 447 percent of allowance and would not return to compliance before mid-November under any incident-free projection.

Yusuf presented the freeze status. Eleven feature merges had been blocked. Nineteen engineers had been redirected to reliability work. The admission control layer was in design with a target of September 24 for deployment to staging.

### 3. Report of the Outside Auditor — SOC 2 Type II Examination

Farkas was recognized. He stated that Kestrel Assurance had conducted interim testing during the week of September 1 covering the examination period of January 1 through December 31, 2025, and that he wished to convey a finding in advance of the formal management letter so that the company had time to respond.

Farkas stated that Kestrel had identified a control deficiency in change management, specifically against Common Criteria 8.1 concerning the authorization, design, development, configuration, testing, approval, and implementation of changes to infrastructure and software. He stated the deficiency rested on two observations. First, testing of a sample of forty configuration changes to production infrastructure between January and August found nine changes approved by a reviewer in the author's direct reporting line, which the company's own documented control prohibits. Second, testing found that the company's documented control did not require review by the owning team for changes to shared infrastructure components, a gap Kestrel characterized as a design deficiency rather than merely an operating deficiency.

Farkas stated that Kestrel had not yet concluded whether the deficiency rose to the level of a significant deficiency or a material weakness for purposes of the opinion, and that the conclusion would depend substantially on remediation evidence.

Zhao stated that the board had adopted a change management control on August 27 addressing precisely the design gap Farkas described. Farkas responded that he was aware of the adoption and that it was constructive, but that a control adopted in August provides limited evidence of operating effectiveness for a period ending in December. He stated that Kestrel would need to test the new control over a period of not less than ninety days of operation, which placed the earliest sufficient testing window at late November.

Radulescu asked what evidence Kestrel would require. Farkas listed: the documented control, evidence of communication to affected personnel, a complete population of changes for the tested period, and evidence of approval consistent with the control for a sample drawn from that population. He stated that gaps in the population itself were more damaging than exceptions within it.

Radulescu asked whether the August 12 and August 27 incidents were themselves within scope. Farkas stated that the incidents were not directly a change management matter but that the August 12 incident involved an unreviewed configuration change and that Kestrel would reference it in the deficiency narrative as a manifestation of the control gap. He stated further that the disabled certificate rotation job touched on Common Criteria 6.1 and that Kestrel was evaluating whether a separate observation was warranted.

Ostrowski asked directly whether the company would receive a qualified opinion. Farkas declined to answer, stating that the conclusion was not his alone to reach and that it would not be reached before the examination closed.

Farkas departed at 3:06 p.m.

Following his departure, Achebe stated that the customer-facing consequence of a qualified SOC 2 opinion was significant, as approximately 400 of the company's customers had contractual provisions requiring delivery of an unqualified SOC 2 Type II report annually. Whitfield stated the figure was 437 by her count and that 61 of those were in the top 200 by revenue.

Zhao directed that remediation evidence collection begin immediately and be treated as a first-class deliverable of the freeze. This became Action Item 2025-09-03-02.

### 4. Customer Report — Contractual Exit Notices

Whitfield reported that two customers had invoked contractual exit language in the period since the last meeting.

**Meridian Logistics Group.** Notice received August 29. Annual contract value $2.1 million, renewal date January 31, 2026. The customer invoked a chronic outage provision permitting termination without penalty upon two or more service level objective breaches in any rolling ninety-day period. Whitfield stated the provision was clearly triggered on its face.

**Calderon Biosciences.** Notice received September 2. Annual contract value $1.3 million, renewal date March 15, 2026. The customer invoked a similar provision and additionally referenced the pending SOC 2 examination, which Whitfield noted was not public information and which she believed had reached the customer through an industry contact.

Combined exposure $3.4 million in renewals. Whitfield stated that both notices were formally notices of intent to exercise and that both contracts provided a cure period, thirty days for Meridian and sixty days for Calderon.

Delacroix-Hyun was recognized. She stated that $3.4 million represented 8.3 percent of the company's $41 million in annual recurring revenue and that the two accounts alone would move the company's net revenue retention below 100 percent for the fiscal year. She stated that the service credit accrual, which Whitfield had now finalized at $1.34 million including negotiated-agreement customers, was material but manageable; that the renewal loss was not.

She stated further, in response to a question from Petrosyan, that the company-wide hiring freeze instituted in July remained in effect and that she was not in a position to lift it.

Whitfield presented her retention plan for both accounts. For Meridian: an executive sponsor call with Ostrowski, a written remediation commitment with dates, and a proposed contractual amendment adding enhanced service level objective terms with escalating credits. For Calderon: the same, plus a commitment to share the SOC 2 remediation plan under non-disclosure.

Radulescu objected to sharing the SOC 2 remediation plan, stating that it constitutes a catalog of the company's control weaknesses and that once shared it cannot be recovered. Achebe stated that a redacted version could be prepared. Whitfield stated that a redacted version of a document about control gaps would be read as evasion and would do more harm than silence.

Zhao ruled that the question of SOC 2 disclosure to Calderon be deferred to a decision by the Chief Executive Officer on Achebe's recommendation, as it exceeded the board's charter. Ostrowski concurred.

### 5. Standing Item — Postmortem Publication

Zhao stated that the deferred question of publishing a public postmortem was now ripe and moved it to a decision.

She summarized the positions as she understood them and invited correction.

**Whitfield** argued for publication. She stated that eleven customers had now asked directly, that the information was substantially already in customer hands through the individual root cause analyses delivered September 5 under Action Item 2025-08-20-07, and that the difference between eleven customers holding a document and the market holding it was smaller than the board imagined. She stated that Meridian's notice cited "lack of transparency regarding root cause" as a contributing reason and read the relevant sentence into the record.

**Radulescu** argued against publication in its proposed form. He stated that he did not object to transparency in principle and did object to publishing, during an open SOC 2 examination with an identified change management deficiency, a document stating that an unreviewed configuration change contributed to a nine-hour outage. He stated the document would be Exhibit A in any subsequent dispute and would be read by the auditor as a management admission.

**Achebe**, in response to a question from Zhao, stated that she shared Radulescu's concern but framed it differently. She stated that the risk was not the publication but the asymmetry: publishing detail about August 12 while the September position was still unresolved would create an expectation of continued disclosure that the company might not be able to meet.

**Petrosyan** argued for publication and stated that her agents were fielding the question forty times a day and had nothing to say, and that the operational cost of the silence was real and was being borne by eleven people in her organization.

**Yusuf** stated that he was of two minds. He said that the engineering culture argument for public postmortems was one he believed in and had argued for at prior employers. He also said that he had written the August 12 postmortem and that in his judgment the document as written was not fit to publish, because it was written for engineers who already knew the system and would read as either incomprehensible or damning to anyone else. He stated that a publishable document was a different document and would take two weeks he did not have.

**Ostrowski** stated that he would abstain from the discussion, as ex officio, but wished the record to reflect that the Chief Executive Officer had asked him the same question on Monday and that he had said he did not know.

**Motion:** Whitfield moved that the board direct publication of a public postmortem covering the August 12 and August 27 incidents, to be published no later than September 19, 2025, with content prepared by Yusuf and reviewed by Achebe. Petrosyan seconded.

**Discussion on the motion.** Radulescu moved to amend by substituting a date of October 15, 2025, after the freeze period and after the interim SOC 2 position had clarified. Whitfield opposed the amendment, stating that a postmortem published two months after the incident was not transparency but archaeology. Yusuf supported the amendment on the ground that it made the deliverable achievable. Zhao stated she opposed the amendment because the cure period on the Meridian contract expired September 28 and a postmortem published after that date could not affect the outcome the board most needed to affect.

**Vote on the amendment:** Failed 2–3. Yea: Yusuf, Radulescu. Nay: Zhao, Petrosyan, Whitfield.

**Vote on the main motion:** Failed 2–3. Yea: Petrosyan, Whitfield. Nay: Yusuf, Radulescu, Zhao.

Zhao stated for the record that she had voted against the motion she had partly argued for. She explained that she opposed the amendment because the date was wrong and opposed the motion because Yusuf's objection was correct on the merits: the board could not direct the publication of a document by September 19 that its author had stated could not be written by September 19 without either bad content or displaced reliability work, and she was unwilling to direct either.

Whitfield asked to record a dissent.

**Dissent of Tanisha Whitfield, entered September 3, 2025.** "I dissent from the board's failure to direct publication of a public postmortem. The board has now deliberated this question at three consecutive meetings and resolved it at none. The reasons advanced against publication have changed each week while the answer has stayed the same, which suggests the answer preceded the reasons. Two customers representing $3.4 million have cited transparency in their exit notices. I do not believe the board is weighing that against anything of comparable weight, and I want the record to show that the cost of this decision will be paid in the renewal line and not in engineering."

**Dissent of Gwen Petrosyan, entered September 3, 2025.** "I join Director Whitfield's dissent and add that the operational burden of the board's non-decision falls on the support organization, which has been instructed to say nothing to customers who ask a reasonable question. I have asked for guidance on what my agents may say. I have not received it."

Zhao accepted both dissents for the record and stated that Petrosyan's request for agent guidance would be answered within two business days regardless of the publication question. This became Action Item 2025-09-03-05.

### 6. Action Items

| No. | Item | Owner | Due |
|---|---|---|---|
| 2025-09-03-01 | Deliver retention plans and executive sponsor calls for Meridian and Calderon | Tanisha Whitfield | September 12, 2025 |
| 2025-09-03-02 | Establish SOC 2 remediation evidence collection process for change management control | Ivo Radulescu | September 10, 2025 |
| 2025-09-03-03 | Prepare recommendation to Chief Executive Officer on SOC 2 disclosure to Calderon Biosciences | Rosalind Achebe | September 9, 2025 |
| 2025-09-03-04 | Rewrite August 12 and August 27 postmortem for general audience; return to board with draft and realistic date | Abdirahman Yusuf | September 10, 2025 |
| 2025-09-03-05 | Issue approved talking points to support agents regarding incident root cause | Meilin Zhao | September 5, 2025 |
| 2025-09-03-06 | Deliver revised on-call compensation proposal | Gwen Petrosyan and Abdirahman Yusuf | September 10, 2025 |
| 2025-09-03-07 | Finalize contra-revenue accrual at $1.34 million and confirm with Controller | Tanisha Whitfield | September 8, 2025 |

### 7. Adjournment

Zhao adjourned the meeting at 5:34 p.m. The next meeting was set for Wednesday, September 10, 2025 at 2:00 p.m.

*Respectfully submitted, Dana Kurniawan, Recording Secretary. Approved September 10, 2025.*

---

---

## MEETING OF WEDNESDAY, SEPTEMBER 10, 2025

**Body:** Reliability Review Board, Huron Stack, Inc.

**Date:** Wednesday, September 10, 2025

**Time:** Called to order at 2:00 p.m. Eastern Daylight Time; adjourned at 5:58 p.m. Eastern Daylight Time

**Place:** Conference Room 3B ("Cavendish"), 411 North Fourth Avenue, Ann Arbor, Michigan, with remote participation by video conference

**Members Present:** Meilin Zhao, Chair; Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield

**Members Absent:** None

**Others Attending:** Peter Ostrowski, Chief Technology Officer, ex officio; Dana Kurniawan, recording secretary; Rosalind Achebe, Associate General Counsel; Marguerite Delacroix-Hyun, Chief Financial Officer (present for Items 5 and 6 only); Emeka Duarte, Director of Product Management (present for Item 4 only); Nikoletta Abramyan, Director of People Operations (present for Items 5 and 6 only)

---

### 1. Call to Order and Approval of Prior Minutes

Zhao called the meeting to order at 2:00 p.m. and noted a quorum.

Radulescu moved to approve the minutes of September 3, 2025 as distributed, including the dissents of Whitfield and Petrosyan as entered. Yusuf seconded.

**Vote:** Approved 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

### 2. Standing Item — Incident and Error Budget Review

Yusuf reported no severity-one incidents in the period September 4 through September 10. One severity-two incident occurred September 8 from 14:22 to 14:29, seven minutes, caused by a failed deployment of the admission control layer to the staging environment which briefly affected a shared metrics service. No customer impact. Yusuf noted that the incident was surfaced by the reclassified alerting adopted under Action Item 2025-08-20-02 and paged a secondary responder within ninety seconds.

Error budget position: September stood at zero customer-impacting minutes consumed against 43 permitted. The rolling 90-day budget stood at 447 percent of allowance, unchanged, and was projected to return to compliance on November 12, 2025 assuming no further incidents.

Yusuf presented freeze status. Twenty-three feature merges blocked to date. The admission control layer had deployed to staging September 9 and was under load testing with a production target of September 26. Certificate expiry monitoring had fired twice on 30-day warnings, both handled without incident. Yusuf stated that the change management control adopted August 27 had processed 84 changes with 3 rejections, and that the median review time was 4.2 hours against a pre-control median of 22 minutes.

Radulescu reported on SOC 2 remediation evidence. The evidence collection process was established September 8. He stated that a complete change population had been reconstructed for the period January 1 through September 8 and that the reconstruction had revealed 1,340 changes, against 1,190 previously recorded in the change management system. He stated the 150-change discrepancy was itself a finding and that he had disclosed it to Kestrel proactively on September 9 rather than waiting for them to discover it.

Zhao asked whether proactive disclosure was the right call. Radulescu stated that Farkas had told the board on September 3 that population gaps were more damaging than exceptions, and that a gap discovered by the auditor after the company had certified a population was categorically worse than a gap the company reported itself. Achebe concurred. Zhao commended the decision on the record.

### 3. Old Business — Postmortem

Yusuf presented the rewritten postmortem prepared under Action Item 2025-09-03-04. He stated the document ran to nine pages, covered both incidents, described the certificate rotation failure and the configuration review gap in terms he characterized as accurate and non-technical, listed eleven corrective actions with owners and dates, and did not include internal system architecture detail beyond what was necessary.

Achebe stated that she had reviewed the draft on September 9 and had proposed four changes, all of which Yusuf had accepted. She stated that in its current form she had no legal objection to publication.

Radulescu stated that he had also reviewed the draft and that his security objection was substantially answered. He stated that he retained a residual concern about the timing relative to the SOC 2 examination but that he no longer regarded it as sufficient to oppose.

Whitfield stated she had shared the draft under embargo with the Meridian account team, who had reported that the customer's technical lead described it as "the first thing that's made sense."

**Motion:** Whitfield moved that the board direct publication of the postmortem as drafted and reviewed, on the company engineering blog and via direct notice to all 3,200 customers, no later than September 17, 2025. Radulescu seconded.

**Discussion.** Petrosyan asked that support agents receive the document 48 hours before publication with prepared responses. Whitfield accepted the request as a friendly amendment.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

Zhao stated for the record that the board had reached on September 10 the decision it had failed to reach on September 3, and that the difference was the existence of a document that could be published rather than an intention to publish one. She stated that Whitfield's dissent of September 3 stood as entered and would not be withdrawn or amended by this vote, and that she believed the dissent had been correct as to the board's pattern of deferral even where the September 3 vote had been correct as to the September 19 date.

Whitfield stated she was satisfied and did not wish to amend her dissent.

### 4. Extension of the Error Budget Freeze and Release Date for 4.0

Zhao introduced the item. The freeze adopted August 27 expired September 30. She proposed extension through October 31, 2025.

Yusuf supported extension. He stated that the admission control layer would reach production September 26 and would require a minimum of three weeks of production operation before he would characterize the subsystem as stable. He stated further that six of the eleven corrective actions from the postmortem had target dates in October and that lifting the freeze on September 30 would place those actions in direct competition with feature work.

Duarte was recognized. He stated that the product organization accepted the extension and had already replanned. He presented three release date options developed with engineering: November 3, which he characterized as achievable only if nothing further went wrong; December 1, which he characterized as achievable with margin; and January 12, which he characterized as safe but which crossed the fiscal year boundary and would move $6 million in attributed pipeline into the next fiscal year.

Delacroix-Hyun stated that the January date was not acceptable from a planning standpoint and that she would rather the company take a modest risk on December 1 than move the revenue.

Whitfield stated that she had tested the December 1 date informally with the three named accounts Duarte had cited on August 27 and that all three had indicated it was workable, with one noting that they would rather have December 1 held than November 3 missed.

Petrosyan supported December 1 and stated that her staffing plan, delivered under Action Item 2025-08-27-06, assumed a December release and could not support November.

Radulescu raised a concern that December 1 placed the release two weeks after the SOC 2 examination testing window closed and that any release-induced incident in late November would land directly in the examination period. Zhao stated that the freeze extension through October 31 and a December 1 release provided a full month of unfrozen but pre-release engineering time in November, which she regarded as the correct sequence.

**Motion:** Yusuf moved to extend the error budget freeze through October 31, 2025, with weekly review by this board, and to set the 4.0 release date at December 1, 2025, and to recommend both to the Engineering Leadership Team. Whitfield seconded.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

Zhao directed that the December 1 date be communicated externally as a committed date and that no further movement would be entertained absent a severity-one incident.

### 5. On-Call Compensation Policy

Petrosyan and Yusuf presented the revised on-call compensation policy prepared under Action Item 2025-09-03-06.

Petrosyan described the current condition. Fourteen engineers and eleven support agents carried on-call rotations. Engineers received no additional compensation for on-call, only compensatory time off at manager discretion. Support agents received an hourly overtime rate for hours worked but nothing for hours held. Since August 12, the engineering on-call rotation had absorbed 340 hours of active incident work outside business hours and the support rotation 94 hours of overtime.

She stated that three engineers had asked to be removed from the rotation and that one had resigned on September 5, citing on-call burden in the exit interview. Abramyan confirmed the resignation and the stated reason.

The proposed policy provided: a flat weekly stipend of $750 for engineering on-call primary and $400 for secondary; an hourly rate of 1.5 times base for support agents for held hours outside scheduled shifts; a guaranteed minimum of eight consecutive off-hours following any incident engagement exceeding two hours between 22:00 and 06:00; a cap of one primary rotation week per engineer per four-week period; and a requirement that any rotation with fewer than six participants be escalated to the Vice President of Engineering.

Abramyan stated that People Operations had reviewed the policy for consistency with the compensation framework and had no objection, and that the stipend structure was consistent with market practice for companies of comparable size.

Delacroix-Hyun stated that the annualized cost was approximately $486,000 and that she would fund it. She stated that she wished the record to reflect that she regarded the cost as unavoidable and the alternative as more expensive, referencing the September 5 resignation.

Radulescu proposed an amendment adding the security on-call rotation, which comprised four engineers, to the same terms. Petrosyan accepted the amendment as friendly.

**Motion:** Petrosyan moved to adopt the revised on-call compensation policy as amended, effective September 15, 2025, and to recommend it to the Engineering Leadership Team and People Operations for implementation. Radulescu seconded.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

### 6. Reliability Engineering Requisitions

Zhao introduced the item. She stated that she was requesting board approval to open two requisitions for site reliability engineers, one at senior level and one at staff level, notwithstanding the company-wide hiring freeze instituted in July 2025.

Yusuf presented the case. He stated that the site reliability engineering team stood at six engineers supporting a platform serving 3,200 customers, that the September 5 resignation would reduce it to five on September 19, and that the corrective action backlog from the August incidents required an estimated 42 engineer-weeks against a team capacity, after operational load, of approximately 14 engineer-weeks per month. He stated that the team could deliver the corrective actions or operate the platform, and had been attempting both since August 12.

Delacroix-Hyun stated her position plainly. She stated that the hiring freeze had been instituted in July because the company was tracking to miss its annual recurring revenue plan, that the situation had since worsened by $3.4 million in exit notices, and that approving exceptions to a freeze in the same quarter it was instituted damaged the credibility of the freeze itself. She stated she was not opposing the requisitions but wanted the difficulty on the record.

Abramyan stated that People Operations had processed nineteen exception requests since July and approved two, both for revenue-generating roles, and that approving these would be the first non-revenue exceptions.

Whitfield stated that she regarded the roles as revenue-protecting and that the distinction between generating and protecting revenue had become difficult to sustain in the current period. She stated that $3.4 million in exit notices was, by any measure, larger than the fully loaded cost of two engineers.

Radulescu stated that the SOC 2 remediation work alone, exclusive of the reliability corrective actions, required sustained effort through November that the current team could not provide without displacing operational work.

Ostrowski stated that he had discussed the matter with the Chief Executive Officer on September 8 and that the Chief Executive Officer had indicated willingness to approve the exception on the board's recommendation, subject to the roles being backfilled within the engineering headcount plan for the following fiscal year rather than added to it.

Petrosyan asked whether the support organization would be permitted a similar exception. Zhao stated that support headcount was outside the board's charter and directed Petrosyan to raise it through her own management line, offering to write a supporting memorandum. Petrosyan accepted.

**Motion:** Whitfield moved that the board recommend to the Chief Executive Officer and Chief Financial Officer approval of two reliability engineering requisitions, one senior and one staff level, as an exception to the company-wide hiring freeze, on the finding that the site reliability engineering team lacks capacity to complete the corrective actions arising from the August 12 and August 27 incidents and the SOC 2 change management remediation while sustaining platform operations, and subject to the condition stated by the Chief Technology Officer regarding the following fiscal year headcount plan. Radulescu seconded.

**Discussion.** Delacroix-Hyun asked that the recommendation specify that the requisitions expire if unfilled by December 31, 2025. Whitfield accepted the condition as friendly.

**Vote:** Adopted 5–0. Yea: Zhao, Yusuf, Petrosyan, Radulescu, Whitfield.

Delacroix-Hyun asked to record a concurrence.

**Concurrence of Marguerite Delacroix-Hyun, entered September 10, 2025.** "I concur in the board's recommendation and note that I am not a member of the board and my concurrence carries no vote. I record it because I will be asked, and I want the answer written down. I supported these requisitions. I did so because the reliability of the platform is now the binding constraint on the company's revenue and not, as I would ordinarily assess it, a cost center subject to the same discipline as any other. I do not regard this as an exception to the hiring freeze so much as a recognition that the freeze was designed for a different problem than the one we have."

### 7. Customer and Renewal Status

Whitfield reported. The Meridian executive sponsor call occurred September 9 with Ostrowski and the customer's Chief Information Officer. The customer indicated it would hold the exit notice in abeyance pending the postmortem publication and the December 1 release commitment, and would make a final determination at the January 31, 2026 renewal date. Whitfield characterized the account as recoverable.

The Calderon call was scheduled for September 15. Achebe reported that the Chief Executive Officer had approved sharing the SOC 2 remediation plan under non-disclosure, in redacted form omitting specific system identifiers, and that Radulescu had reviewed and approved the redactions.

Whitfield reported that no additional exit notices had been received. She reported that 34 customers had requested renegotiated service level objective terms with enhanced credits and that a standard amendment was in preparation with Achebe.

The finalized service credit accrual stood at $1.34 million. Whitfield reported that claims received as of September 10 totaled $610,000.

### 8. Action Items

| No. | Item | Owner | Due |
|---|---|---|---|
| 2025-09-10-01 | Publish postmortem to engineering blog and notify all customers | Abdirahman Yusuf | September 17, 2025 |
| 2025-09-10-02 | Deliver postmortem and prepared responses to support agents 48 hours prior to publication | Gwen Petrosyan | September 15, 2025 |
| 2025-09-10-03 | Submit freeze extension and December 1 release date to Engineering Leadership Team | Meilin Zhao | September 12, 2025 |
| 2025-09-10-04 | Communicate December 1 release date to customers and market | Emeka Duarte | September 19, 2025 |
| 2025-09-10-05 | Implement on-call compensation policy effective September 15 | Nikoletta Abramyan | September 15, 2025 |
| 2025-09-10-06 | Submit requisition exception request to Chief Executive Officer and Chief Financial Officer | Meilin Zhao | September 11, 2025 |
| 2025-09-10-07 | Deploy admission control layer to production | Abdirahman Yusuf | September 26, 2025 |
| 2025-09-10-08 | Complete Calderon executive sponsor call and report outcome | Tanisha Whitfield | September 17, 2025 |
| 2025-09-10-09 | Deliver reconstructed change population and discrepancy analysis to Kestrel Assurance | Ivo Radulescu | September 19, 2025 |
| 2025-09-10-10 | Draft supporting memorandum for support organization headcount request | Meilin Zhao | September 19, 2025 |
| 2025-09-10-11 | Complete standard enhanced service level objective amendment for customer execution | Rosalind Achebe and Tanisha Whitfield | September 26, 2025 |

### 9. Adjournment

Zhao thanked the members for four weeks of sustained attention and noted that the board would continue to meet weekly through the freeze period and would revisit its meeting cadence at the November 5 meeting. She adjourned the meeting at 5:58 p.m. The next meeting was set for Wednesday, September 17, 2025 at 2:00 p.m.

*Respectfully submitted, Dana Kurniawan, Recording Secretary. Approved September 17, 2025.*
