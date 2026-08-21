# Huron Stack, Inc.
# Reliability Review Board — Minutes of Meetings

---

## Minutes of the Meeting of August 20, 2025

**Body:** Reliability Review Board of Huron Stack, Inc.
**Date:** Wednesday, August 20, 2025
**Time:** 2:00 p.m. – 4:12 p.m. Eastern Time
**Place:** Barton Conference Room, Huron Stack headquarters, 210 South First Street, Ann Arbor, Michigan, with video connection available
**Members present:** Meilin Zhao, Vice President of Engineering (chair); Abdirahman Yusuf, Principal Site Reliability Engineer; Gwen Petrosyan, Director of Support; Ivo Radulescu, Staff Security Engineer; Tanisha Whitfield, Director of Customer Success
**Members absent:** None
**Others attending:** Peter Ostrowski, Chief Technology Officer (ex officio); Rob Calloway, Chief Financial Officer (guest, for agenda item 4); Priya Natarajan, Executive Business Partner (recording secretary)

### 1. Call to Order and Adoption of Charter

Ms. Zhao called the meeting to order at 2:00 p.m. and noted that all five voting members were present, constituting a quorum. She stated that the board had been constituted by the executive team on August 15, 2025, in response to the August 12 control plane incident, and that its mandate was to review incidents and error budget status weekly, oversee remediation, and make recommendations on release readiness and customer commitments.

Ms. Zhao presented a draft charter providing for a standing weekly meeting on Wednesday afternoons at 2:00 p.m., a standing agenda beginning with incident and error budget review followed by customer and audit reports, majority voting among the five members with the chair voting, and attendance by the Chief Technology Officer ex officio without vote. Mr. Yusuf moved adoption of the charter as presented. Ms. Petrosyan seconded. The motion carried 5–0. Ms. Zhao directed Ms. Natarajan to file the charter with the minutes.

### 2. Standing Incident Review: Incident INC-2025-0812

Mr. Yusuf presented the timeline of incident INC-2025-0812, the control plane failure of August 12, 2025. He reported that the outage began at 06:41 Eastern Time when the control plane certificate authority rejected internal service certificates, that the deployment pipeline entered a fail-closed state at 06:47, and that full service was not restored until 15:55, a total duration of nine hours and fourteen minutes. He reported that 1,880 of the company's 3,200 customers were unable to execute deployments during the outage window.

Mr. Yusuf presented the root cause analysis. He stated that the proximate cause was an expired intermediate certificate whose automated rotation job had been silently failing since July 29 without alerting, and that the impact was compounded by a configuration change to the deployment router made on August 8 that had bypassed the change review process. The unreviewed change removed the router's fallback path to a secondary certificate store, which converted what would have been a degraded-mode event into a full outage. He stated that recovery was prolonged because the runbook for manual certificate reissuance was eleven months out of date and referenced decommissioned tooling.

Mr. Radulescu stated that the failed rotation job had also masked two expiring certificates in the audit logging pipeline, which he had rotated manually on August 14, and that he considered the certificate lifecycle system a single point of failure requiring redesign rather than patching.

The board discussed the timeline for approximately forty minutes. Mr. Ostrowski asked whether any customer data was exposed during the incident. Mr. Radulescu answered that his review found no evidence of data exposure and that the failure mode was availability only; he committed to deliver a written security assessment. Ms. Zhao asked how the August 8 configuration change had bypassed review. Mr. Yusuf answered that the change was pushed through an emergency-change path that did not require a second reviewer, and that the emergency designation had not been justified in the change record.

### 3. Standing Error Budget Review

Mr. Yusuf presented the error budget position. He reported that the deployment availability service level objective of 99.9 percent measured over a rolling quarter carried an error budget of approximately 131 minutes, and that the August 12 incident had consumed 554 minutes, exhausting the budget for the quarter by a factor of more than four. He recommended that the board treat the budget as exhausted through at least the end of September and weigh that status in any release decision. No motion was made; Ms. Zhao noted the report for the record and stated that error budget status would be a standing agenda item.

### 4. Customer and Financial Impact Report

Ms. Petrosyan reported that support had received 4,312 tickets attributable to the incident between August 12 and August 19, against a normal weekly volume of approximately 900, and that first-response times had recovered to target as of August 18. She reported 61 open executive escalations.

Ms. Whitfield reported that 214 customers had inquired about contractual service level remedies and that 9 customers had requested calls with executive leadership. Mr. Calloway presented the service credit exposure analysis prepared by finance and customer success. He stated that, applying the service level agreement credit schedule across affected customers, the estimated exposure was $1.2 million in service credits against $41 million in annual recurring revenue.

Ms. Whitfield moved that the board record the estimated $1.2 million service credit exposure, endorse proactive issuance of credits to affected customers without requiring individual claims, and refer the credit schedule to finance for execution by September 5. Ms. Petrosyan seconded. In discussion, Mr. Calloway noted that proactive issuance would exceed the strict contractual obligation for an estimated 340 customers whose measured downtime fell below the claim threshold, at an incremental cost of approximately $140,000, and stated that finance supported the approach for retention reasons. The motion carried 5–0.

### 5. Postmortem and Remediation Planning

Ms. Zhao stated that a full internal postmortem was required and asked the board to consider at a future meeting whether a public postmortem should be published. Ms. Whitfield stated her view that publication would be essential to retaining enterprise customers. Mr. Radulescu stated that any public document would need security review before the board considered it. The question was deferred without objection.

### 6. Action Items

The following action items were recorded:

- Mr. Yusuf to complete the internal postmortem for INC-2025-0812, including contributing factors and remediation plan, and circulate it to the board by August 26.
- Mr. Radulescu to deliver a written security assessment of the incident, including the certificate lifecycle single-point-of-failure analysis, by August 27.
- Mr. Yusuf to close the emergency-change loophole by requiring a second reviewer on all changes, including emergency changes, effective August 22, and to report compliance weekly.
- Mr. Yusuf to implement alerting on certificate rotation job failures and certificate expiry within 30 days of expiration, by August 29.
- Ms. Petrosyan to prepare a weekly customer sentiment and escalation summary as a standing report beginning August 27.
- Ms. Whitfield and Mr. Calloway to execute the service credit issuance by September 5 and report completion.
- Ms. Zhao to brief the executive team and the audit liaison on the incident's potential relevance to the SOC 2 Type II examination then in fieldwork, by August 25.

### 7. Adjournment

There being no further business, Ms. Zhao adjourned the meeting at 4:12 p.m. The next meeting was set for Wednesday, August 27, 2025, at 2:00 p.m.

*Minutes recorded by Priya Natarajan.*

---

## Minutes of the Meeting of August 27, 2025

**Body:** Reliability Review Board of Huron Stack, Inc.
**Date:** Wednesday, August 27, 2025
**Time:** 2:00 p.m. – 4:35 p.m. Eastern Time
**Place:** Barton Conference Room, Huron Stack headquarters, 210 South First Street, Ann Arbor, Michigan, with video connection available
**Members present:** Meilin Zhao (chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members absent:** None
**Others attending:** Priya Natarajan, Executive Business Partner (recording secretary). Peter Ostrowski, Chief Technology Officer (ex officio), was absent, traveling; he submitted written comments on agenda item 4, which were read into the record.

### 1. Call to Order and Approval of Minutes

Ms. Zhao called the meeting to order at 2:00 p.m. and confirmed a quorum. Mr. Yusuf moved approval of the minutes of the August 20, 2025 meeting as circulated. Mr. Radulescu seconded. The motion carried 5–0.

### 2. Standing Incident Review: Incident INC-2025-0827

Mr. Yusuf presented a preliminary report on incident INC-2025-0827, which had occurred that morning. He reported that at 05:12 Eastern Time the control plane's certificate validation service began rejecting a subset of internal service certificates following a scheduled rotation, that deployments failed for approximately 620 customers, and that service was restored at 05:59, a duration of 47 minutes. He stated that the incident traced to the same certificate lifecycle subsystem implicated in the August 12 outage: the new rotation alerting installed under the August 20 action item had fired correctly, and the on-call engineer had restored service using the corrected runbook, but the rotation job itself had again produced an invalid certificate chain due to a defect in how the job assembled intermediate certificates.

Mr. Yusuf stated that the shortened duration demonstrated that the detection and response remediations were working, but that the recurrence demonstrated that the underlying subsystem remained unsound, consistent with Mr. Radulescu's August 20 assessment. Mr. Radulescu presented his written security assessment, delivered on schedule, which recommended replacing the internally built certificate lifecycle tooling with a managed certificate authority service and estimated six to eight weeks of engineering work.

Ms. Zhao stated for the record that two incidents in the same subsystem within fifteen days constituted a pattern, not a coincidence, and that the board's posture should shift from remediation of a single incident to stabilization of the subsystem.

### 3. Standing Error Budget Review

Mr. Yusuf reported that the 47-minute incident consumed a further 47 minutes of error budget, bringing quarterly consumption to 601 minutes against a 131-minute budget. He reported that the postmortem for INC-2025-0812 had been circulated on August 26 as required, and that eleven of the fourteen remediation items were on track, with the three remaining items dependent on the certificate subsystem replacement.

### 4. Proposed Error Budget Freeze and Effect on the 4.0 Release

Ms. Zhao proposed that the board adopt a formal error budget freeze: a halt to all non-reliability feature deployments to production, with engineering capacity redirected to the certificate subsystem replacement and the remaining postmortem remediations, effective August 28. She stated plainly that a freeze of the length required would push the 4.0 release, scheduled for October 6, and that the board should not adopt the freeze without acknowledging that consequence.

Ms. Natarajan read Mr. Ostrowski's written comments into the record. Mr. Ostrowski wrote that he supported a freeze, that in his judgment shipping 4.0 onto an unstable control plane would compound risk rather than deliver value, and that he would support the board's recommendation with the chief executive.

In discussion, Ms. Whitfield opposed an open-ended freeze. She stated that 4.0 had been committed to customers in renewal conversations, that at least six enterprise renewals in the fourth quarter referenced 4.0 features, and that a slipped date announced on the heels of two incidents would hand competitors a narrative. She proposed as an alternative a two-week freeze with 4.0 held at October 6 pending reassessment. Ms. Petrosyan stated that support could not absorb a third incident and supported the freeze. Mr. Radulescu supported the freeze and stated that the subsystem replacement could not be done responsibly in two weeks. Mr. Yusuf supported the freeze and stated that pretending October 6 remained achievable would distort the team's engineering decisions.

Ms. Zhao moved that the board (a) adopt an error budget freeze on non-reliability production deployments effective August 28, 2025, for an initial period through September 10, 2025, subject to extension by board vote; (b) direct engineering to reallocate the 4.0 feature teams to the certificate subsystem replacement for the duration of the freeze; and (c) defer a decision on the 4.0 release date to a future meeting, with the record reflecting that October 6 was at risk. Mr. Yusuf seconded.

Ms. Whitfield moved to amend clause (a) to limit the freeze to a fixed two weeks without provision for extension. The amendment was seconded by Ms. Petrosyan for purposes of discussion. On the amendment, the vote was 1 in favor (Whitfield), 4 opposed (Zhao, Yusuf, Petrosyan, Radulescu). The amendment failed.

On the main motion, the vote was 4 in favor (Zhao, Yusuf, Petrosyan, Radulescu), 1 opposed (Whitfield). The motion carried. Ms. Whitfield asked that her dissent be recorded on the ground that the freeze as structured, with an extension mechanism and no committed release date, transferred the cost of engineering instability onto customer-facing commitments without a plan to communicate it. Her dissent was so recorded.

### 5. Customer Report

Ms. Petrosyan presented the first standing customer sentiment summary. She reported ticket volume at 1,240 for the week, elevated but declining, and 38 open executive escalations, down from 61. Ms. Whitfield reported that service credit issuance was on track for September 5, that two enterprise customers — Cobalt Freight Systems and Anders Health Labs — had requested formal briefings on remediation status, and that both customers' contracts contained availability-related termination clauses. She stated she would report further at the next meeting.

### 6. Action Items

- Mr. Yusuf to complete the postmortem for INC-2025-0827 and circulate it by September 2.
- Mr. Yusuf and Mr. Radulescu to present a scoped plan and timeline for the certificate subsystem replacement, including the managed certificate authority option, by September 3.
- Ms. Zhao to communicate the freeze to all engineering staff on August 28 and to define the exception process for critical customer fixes, with exceptions requiring her written approval and weekly reporting to the board.
- Ms. Whitfield to prepare a customer communication plan covering the freeze and the risk to the October 6 date, for board review on September 3.
- Ms. Whitfield to schedule and lead the remediation briefings for Cobalt Freight Systems and Anders Health Labs, with Mr. Yusuf presenting the technical material, before September 3.
- Ms. Petrosyan to continue the weekly sentiment summary.

### 7. Adjournment

Ms. Zhao adjourned the meeting at 4:35 p.m. The next meeting was set for Wednesday, September 3, 2025, at 2:00 p.m.

*Minutes recorded by Priya Natarajan.*

---

## Minutes of the Meeting of September 3, 2025

**Body:** Reliability Review Board of Huron Stack, Inc.
**Date:** Wednesday, September 3, 2025
**Time:** 2:00 p.m. – 5:05 p.m. Eastern Time
**Place:** Barton Conference Room, Huron Stack headquarters, 210 South First Street, Ann Arbor, Michigan, with video connection available
**Members present:** Meilin Zhao (chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members absent:** None
**Others attending:** Peter Ostrowski, Chief Technology Officer (ex officio); Deirdre Whelan, Engagement Partner, Kestrel Assurance (guest, agenda item 3, by video); Elena Marsh, General Counsel (guest, agenda items 4 and 5); Priya Natarajan, Executive Business Partner (recording secretary)

### 1. Call to Order and Approval of Minutes

Ms. Zhao called the meeting to order at 2:00 p.m. and confirmed a quorum. Ms. Petrosyan moved approval of the minutes of the August 27, 2025 meeting as circulated. Mr. Yusuf seconded. The motion carried 5–0.

### 2. Standing Incident and Error Budget Review

Mr. Yusuf reported no new incidents since August 27. He reported that the postmortem for INC-2025-0827 had been circulated on September 2, that the error budget freeze was in effect with full compliance and one approved exception (a security patch deployed August 30 with Ms. Zhao's written approval), and that error budget consumption stood unchanged at 601 minutes against a 131-minute quarterly budget. He and Mr. Radulescu presented the certificate subsystem replacement plan: migration to a managed certificate authority with automated rotation and dual-path validation, estimated at seven weeks of work by the reallocated teams, with completion targeted for October 24 and a two-week soak period thereafter. The board received the plan without objection, and Ms. Zhao stated that the October 24 target would frame the freeze-extension and release-date decisions at the September 10 meeting.

### 3. Audit Report: SOC 2 Type II Examination

Ms. Whelan of Kestrel Assurance presented the auditor's report on the SOC 2 Type II examination covering the period October 1, 2024 through July 31, 2025. She stated that Kestrel had identified a control gap in change management: testing of a sample of production changes found that the emergency-change path permitted single-person deployment without documented justification or secondary review, that the August 8 configuration change implicated in the August 12 incident was within the examination period and exemplified the gap, and that Kestrel expected to report the matter as an exception against the change management control in the final report, with the associated Trust Services criteria noted as not operating effectively for a portion of the period.

Ms. Whelan stated that the remediation already implemented on August 22 — mandatory second review on all changes including emergency changes — was responsive, and that Kestrel would note management's remediation in the report. She advised that a clean bridge letter would depend on demonstrated operation of the remediated control over a sustained period. Mr. Radulescu asked whether the certificate monitoring failure would be reported as a second exception; Ms. Whelan answered that Kestrel expected to treat it within the same exception narrative but reserved final judgment.

Mr. Ostrowski asked what customers relying on the SOC 2 report should be told. Ms. Whelan advised factual disclosure of the exception and the remediation once the report was final, expected in early October. Ms. Whelan left the meeting at 2:55 p.m.

Ms. Zhao directed, without objection, that Mr. Radulescu own the audit remediation evidence file, including weekly change-review compliance reports, and coordinate with Kestrel through issuance of the final report.

### 4. Customer Report: Contractual Exit Notices

Ms. Whitfield reported that two customers had invoked contractual exit language following the two incidents. Cobalt Freight Systems, with $2.1 million in annual recurring revenue renewing in January 2026, delivered notice on August 29 under an availability termination clause triggered by two qualifying outages in a rolling ninety-day period. Anders Health Labs, with $1.3 million renewing in November 2025, delivered notice on September 2 under a similar clause. Together the two accounts represented $3.4 million in renewals.

Ms. Marsh advised the board that both notices opened cure periods — sixty days for Cobalt Freight Systems and forty-five days for Anders Health Labs — during which demonstrated remediation and a sustained period without qualifying incidents could defeat the termination right, and that neither notice was an accomplished termination. She advised that all board communications concerning the two accounts be routed through counsel.

Ms. Whitfield reported that the remediation briefings held August 29 (Cobalt) and September 2 (Anders) under her August 27 action item had been received professionally, and that both customers had asked specifically whether Huron Stack would publish a public postmortem, stating that they regarded transparency as a condition of continued trust.

Ms. Whitfield moved that the board designate the two accounts as executive retention accounts, with Ms. Whitfield as owner, Mr. Yusuf as technical sponsor, and monthly written remediation reports to both customers through their cure periods, subject to counsel's review. Mr. Yusuf seconded. The motion carried 5–0.

Ms. Petrosyan presented the weekly sentiment summary: ticket volume at 1,010, escalations at 24, both declining. The board also received Ms. Whitfield's customer communication plan on the freeze, prepared under her August 27 action item; the board approved it without objection for release on September 5, with the release-date language held pending the September 10 decision.

### 5. Debate on Publication of the Postmortem

Ms. Zhao opened the deferred question of whether to publish a public postmortem of the August incidents. Ms. Marsh remained for this item.

Ms. Whitfield moved that Huron Stack publish the full technical postmortem for INC-2025-0812 and INC-2025-0827, edited only for customer-identifying information, no later than September 12. Ms. Petrosyan seconded. Ms. Whitfield argued that both at-risk accounts had tied trust to transparency, that the developer community expected engineering candor from a developer platform company, and that a thin postmortem would be worse than none. Ms. Petrosyan concurred, reporting that support was fielding daily requests for a public root cause account.

Mr. Radulescu opposed the motion. He stated that the full postmortem described the certificate architecture in detail, that the described weaknesses would remain in production until the replacement completed in late October, and that publishing an attacker's map of an unremediated subsystem was irresponsible. He further noted that publication before the SOC 2 report issued could complicate the audit narrative. Mr. Yusuf stated that he favored eventual publication but agreed the full document could not safely publish before remediation completed. Ms. Zhao stated that she supported publication in principle but not the September 12 date or the full technical content. Mr. Ostrowski, without vote, stated that he favored a redacted publication and cautioned against silence.

The debate continued for approximately forty minutes. On the motion, the vote was 2 in favor (Whitfield, Petrosyan), 3 opposed (Zhao, Yusuf, Radulescu). The motion failed. Ms. Whitfield and Ms. Petrosyan asked that their votes be recorded as dissents from the board's decision not to commit to full publication, on the ground that the customer-trust cost of delay exceeded the security risk as described. The dissents were so recorded.

Mr. Yusuf then moved that the board direct preparation of a redacted public postmortem — preserving the timeline, root causes, customer impact, and remediation commitments, and omitting architectural detail exploitable before remediation — with security review by Mr. Radulescu and legal review by Ms. Marsh, for board decision on September 10. Ms. Zhao seconded. The motion carried 5–0, Ms. Whitfield stating that she voted in favor as the available alternative while maintaining her recorded dissent on the main question.

### 6. Action Items

- Mr. Yusuf to draft the redacted public postmortem by September 8.
- Mr. Radulescu to complete security review of the draft by September 9, and to maintain the audit remediation evidence file for Kestrel Assurance on an ongoing basis.
- Ms. Marsh to complete legal review of the draft by September 9 and to review all written communications to the two exit-notice accounts.
- Ms. Whitfield to deliver the first monthly remediation reports to Cobalt Freight Systems and Anders Health Labs by September 15, and to release the approved freeze communication on September 5.
- Ms. Zhao to prepare recommendations on freeze extension and the 4.0 release date, with engineering capacity analysis, for September 10.
- Ms. Petrosyan to continue the weekly sentiment summary.

### 7. Adjournment

Ms. Zhao adjourned the meeting at 5:05 p.m. The next meeting was set for Wednesday, September 10, 2025, at 2:00 p.m.

*Minutes recorded by Priya Natarajan.*

---

## Minutes of the Meeting of September 10, 2025

**Body:** Reliability Review Board of Huron Stack, Inc.
**Date:** Wednesday, September 10, 2025
**Time:** 2:00 p.m. – 4:50 p.m. Eastern Time
**Place:** Barton Conference Room, Huron Stack headquarters, 210 South First Street, Ann Arbor, Michigan, with video connection available
**Members present:** Meilin Zhao (chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members absent:** None
**Others attending:** Peter Ostrowski, Chief Technology Officer (ex officio); Rob Calloway, Chief Financial Officer (guest, agenda items 5 and 6); Priya Natarajan, Executive Business Partner (recording secretary)

### 1. Call to Order and Approval of Minutes

Ms. Zhao called the meeting to order at 2:00 p.m. and confirmed a quorum. Mr. Radulescu moved approval of the minutes of the September 3, 2025 meeting as circulated. Ms. Whitfield seconded. The motion carried 5–0.

### 2. Standing Incident and Error Budget Review

Mr. Yusuf reported no incidents since August 27, a period of fourteen days. He reported that the certificate subsystem replacement was on schedule against the October 24 target, with the managed certificate authority provisioned, the first of three service groups migrated in staging, and dual-path validation implemented in the deployment router, reversing the August 8 unreviewed change. He reported error budget consumption unchanged at 601 minutes against the 131-minute quarterly budget, with the budget projected to return to positive territory in early November under the rolling-quarter calculation, assuming no further incidents. He reported full freeze compliance with two approved exceptions during the week, both critical customer fixes approved in writing by Ms. Zhao, and change-review compliance at 100 percent for the third consecutive week, with evidence filed by Mr. Radulescu for Kestrel Assurance.

### 3. Extension of the Error Budget Freeze

Ms. Zhao presented her recommendation, prepared under her September 3 action item, that the freeze be extended through October 31, 2025, to cover the replacement completion date of October 24 plus the start of the soak period. She stated that lifting the freeze before the replacement completed would divide the reallocated teams and jeopardize the October 24 date, which in turn anchored the cure-period commitments to the two exit-notice accounts.

Ms. Whitfield stated that she continued to regard a two-month total freeze as commercially costly but acknowledged that the September 5 customer communication had been received without significant attrition signals and that the cure-period logic argued for completion. Ms. Zhao moved that the error budget freeze be extended through October 31, 2025, with the existing exception process continued and weekly compliance reporting maintained. Mr. Yusuf seconded. The motion carried 4–1, Ms. Whitfield opposed. Ms. Whitfield asked that her dissent be recorded on grounds consistent with her August 27 dissent — that the board had still not paired the freeze with a committed customer-facing feature roadmap — and it was so recorded.

### 4. The 4.0 Release Date

Ms. Zhao presented the engineering capacity analysis. She stated that with feature teams reallocated through October 31, the 4.0 release train would require four weeks of integration and hardening after the freeze lifted, making the earliest responsible general availability date December 1, 2025. She stated that an intermediate option of November 3 was achievable only by lifting the freeze on October 6 and accepting the replacement landing without a soak period, which she did not recommend.

Ms. Whitfield argued for November 3, stating that Anders Health Labs' renewal fell on November 15, inside its cure period, and that a December date would place the renewal decision before the release. Mr. Yusuf responded that shipping 4.0 without a soak period onto the newly replaced subsystem recreated the risk pattern that produced August 12, and that a third incident during Anders' cure period would be fatal to the renewal in a way a December date would not. Mr. Radulescu concurred, adding that the SOC 2 exception narrative depended on demonstrating disciplined change management, and that a compressed release would undercut it. Ms. Petrosyan supported December 1, stating that support staffing plans for a major release could not be rebuilt for November on four weeks' notice. Mr. Ostrowski, without vote, stated that he had briefed the chief executive, that the executive team would support the board's recommendation, and that in his own judgment December 1 was the defensible date.

Mr. Yusuf moved that the board recommend, and engineering adopt, December 1, 2025 as the general availability date for the 4.0 release, with a feature-complete integration milestone of November 10 and a go/no-go review by this board on November 19. Mr. Radulescu seconded.

Ms. Whitfield moved to amend the general availability date to November 3, 2025. The amendment, seconded by Ms. Petrosyan for purposes of discussion, failed 1–4 (Whitfield in favor; Zhao, Yusuf, Petrosyan, Radulescu opposed).

On the main motion, the vote was 4 in favor (Zhao, Yusuf, Petrosyan, Radulescu), 1 opposed (Whitfield). The motion carried, and the 4.0 release was moved from October 6 to December 1, 2025. Ms. Whitfield asked that her dissent be recorded on the ground that the December date placed the Anders Health Labs renewal ahead of the release without a compensating commitment; she stated that she would nonetheless carry the decision to customers as the board's decision. The dissent was so recorded. Ms. Zhao directed Ms. Whitfield, with Ms. Marsh's review, to communicate the December 1 date to all customers by September 12, with tailored communications to the two exit-notice accounts including early-access participation in the November 10 feature-complete build, which Mr. Yusuf confirmed engineering could support.

### 5. Revised On-Call Compensation Policy

Mr. Yusuf presented a revised on-call compensation policy, developed with people operations following retention concerns in the site reliability group after the August incidents. The policy provided a flat weekly on-call stipend of $600 for primary and $300 for secondary rotation, hourly incident-response pay at 1.5 times the equivalent hourly rate for pages outside business hours, mandatory recovery time off following any incident exceeding four hours, and a minimum rotation depth of six engineers per rotation by January 1, 2026. Mr. Calloway confirmed that finance had costed the policy at approximately $310,000 annually and that the expense was approved in principle by the chief executive subject to board adoption.

Ms. Petrosyan asked that the recovery-time provision extend to support incident commanders; Mr. Yusuf accepted the extension as a friendly amendment. Ms. Petrosyan moved adoption of the revised on-call compensation policy as amended, effective September 15, 2025. Ms. Whitfield seconded. The motion carried 5–0. Mr. Yusuf was recorded as owner for implementation with people operations, with a compliance report due October 8.

### 6. Reliability Engineering Requisitions

Ms. Zhao presented a request for two reliability engineering requisitions — one senior site reliability engineer and one infrastructure software engineer — noting that the company-wide hiring freeze announced July 21 remained in effect and that the requisitions therefore required an exception. Mr. Yusuf stated that the rotation-depth requirement adopted under item 5 could not be met with current headcount and that the certificate replacement had exposed a bus-factor of one on two critical systems. Mr. Calloway stated that the chief executive had authorized him to confirm that finance would support an exception for up to two reliability roles on the board's recommendation, at a fully loaded cost of approximately $520,000 annually.

Mr. Radulescu moved that the board approve the two reliability engineering requisitions as exceptions to the company-wide hiring freeze and recommend their immediate posting. Ms. Petrosyan seconded. The motion carried 5–0. Ms. Zhao was recorded as owner, with postings due by September 15 and a pipeline report due October 8.

### 7. Publication of the Redacted Postmortem

Ms. Zhao reported that the redacted public postmortem had been drafted by Mr. Yusuf on September 8 and had cleared Mr. Radulescu's security review and Ms. Marsh's legal review on September 9, in accordance with the September 3 action items. Mr. Radulescu stated that the redactions resolved his principal objection but that he continued to believe any publication should wait until the subsystem replacement completed on October 24, and that he would vote against publication now on that ground.

Ms. Whitfield moved that the board approve publication of the redacted postmortem on the company's engineering blog on September 12, 2025, with direct advance copies to Cobalt Freight Systems and Anders Health Labs on September 11, and that the board commit to publishing a follow-up report on completed remediation after the soak period concludes. Ms. Petrosyan seconded. On the motion, the vote was 4 in favor (Zhao, Yusuf, Petrosyan, Whitfield), 1 opposed (Radulescu). The motion carried. Mr. Radulescu asked that his dissent be recorded on the ground that publication of any incident analysis before remediation completed was premature as a matter of security practice, notwithstanding the redactions. The dissent was so recorded.

### 8. Customer and Audit Status

Ms. Petrosyan reported ticket volume at 940 for the week, approaching the normal baseline of 900, and executive escalations at 11. Ms. Whitfield reported that the first monthly remediation reports to the two exit-notice accounts were on track for September 15, and that Cobalt Freight Systems had verbally indicated that a clean record through its cure period, the published postmortem, and the committed December 1 date would likely resolve its notice; Anders Health Labs remained undecided. Mr. Radulescu reported that Kestrel Assurance had acknowledged receipt of three weeks of change-review compliance evidence and continued to project issuance of the final SOC 2 Type II report in early October.

### 9. Action Items

- Ms. Whitfield to communicate the December 1, 2025 release date to all customers by September 12, with counsel-reviewed tailored communications and early-access offers to Cobalt Freight Systems and Anders Health Labs, and to deliver the monthly remediation reports by September 15.
- Mr. Yusuf to publish the redacted postmortem on September 12, following advance delivery to the two accounts on September 11, and to implement the on-call compensation policy with people operations, reporting October 8.
- Ms. Zhao to post the two reliability requisitions by September 15 and report the candidate pipeline on October 8.
- Mr. Radulescu to continue the audit evidence file through issuance of the final SOC 2 report and to report the report's contents to the board upon issuance.
- Mr. Yusuf to report weekly on the certificate subsystem replacement against the October 24 target and on freeze compliance.
- Ms. Petrosyan to continue the weekly sentiment summary.
- Ms. Zhao to place the freeze lift decision on the agenda for the last meeting of October and the 4.0 go/no-go review on the agenda for November 19.

### 10. Adjournment

There being no further business, Ms. Zhao adjourned the meeting at 4:50 p.m. The next meeting was set for Wednesday, September 17, 2025, at 2:00 p.m.

*Minutes recorded by Priya Natarajan.*
