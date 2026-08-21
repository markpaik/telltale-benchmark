# Huron Stack, Inc.
## Reliability Review Board — Minutes of Meetings

---

# Meeting No. 1

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, August 20, 2025
**Time:** 1:00 p.m. – 3:20 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair, Vice President of Engineering); Abdirahman Yusuf (Principal Site Reliability Engineer); Gwen Petrosyan (Director of Support); Ivo Radulescu (Staff Security Engineer); Tanisha Whitfield (Director of Customer Success)
**Members Absent:** None
**Others Attending:** Peter Ostrowski (Chief Technology Officer, ex officio, non-voting); Colin Ashworth (Chief Financial Officer); Renata Byrne (General Counsel); Dana Okafor (Engineering Program Manager, recording secretary)

### 1. Call to Order and Charter

Zhao called the meeting to order at 1:00 p.m. and stated that this was the first meeting of the Reliability Review Board, convened by Ostrowski on August 14, 2025, in response to the outage of August 12, 2025. Zhao read the board's charter into the record: the board would meet on Wednesday afternoons to review incidents affecting production availability, to monitor the engineering error budget, to oversee remediation, and to report to the executive staff. Zhao stated that Ostrowski would attend in an ex officio, non-voting capacity, and that the five named members constituted the voting membership, with a majority of those present and voting required to carry a motion.

### 2. Standing Incident and Error Budget Review

Yusuf presented the incident timeline for August 12. At 6:41 a.m. Eastern, the certificate used for internal service-to-service authentication in the control plane expired without triggering the automated rotation job. The resulting authentication failures cascaded to the deployment scheduler by 6:53 a.m., taking customer deployments offline. Engineering restored service at 3:55 p.m., an outage of nine hours and fourteen minutes. Yusuf reported that 1,880 of the company's 3,200 customers were affected, concentrated among accounts served from the primary deployment region.

Yusuf stated that the root cause was an expired certificate rotation, compounded by a configuration change to the certificate management service deployed on August 9 that had bypassed code review and had disabled the expiration alert. Radulescu confirmed that the change had been applied directly by an engineer with production access during an unrelated maintenance window and had not passed through the standard review gate.

On Zhao's request, the board entered as its finding of record, subject to revision, that the root cause of the August 12 incident was an expired certificate rotation, compounded by an unreviewed configuration change.

Yusuf reported that the engineering error budget for the quarter was exhausted, the August 12 incident alone having consumed the remaining allowance.

### 3. Financial and Customer Impact

Ashworth presented a preliminary estimate of $1.2 million in service credits owed under the company's uptime service-level agreements as a result of the outage, based on affected customer contracts and the duration of the interruption. Ashworth stated the figure was preliminary pending account-level reconciliation. Whitfield reported that support had logged 340 tickets related to the outage and that account teams were proactively contacting the largest affected customers.

Byrne advised that the $1.2 million estimate should be treated as internal and not disclosed externally until finalized, and recommended that customer communications be routed through legal prior to distribution. The board agreed by consensus.

### 4. Discussion

Petrosyan asked whether the unreviewed configuration change reflected a gap specific to the certificate management service or a broader control weakness. Radulescu stated that a broader audit was warranted. Zhao stated that a corrective action plan would be brought to the board no later than the August 27 meeting.

### 5. Action Items

- Yusuf to complete a formal root cause analysis and circulate it to the board by August 25, 2025.
- Radulescu to audit production configuration changes made outside code review over the preceding ninety days, with findings due September 3, 2025.
- Ashworth to finalize the service credit estimate with account-level detail by August 27, 2025.
- Whitfield to compile a summary of customer escalations for the August 27 meeting.
- Zhao and Yusuf to draft a certificate rotation remediation plan for board review at the August 27 meeting.

### 6. Adjournment

There being no further business, Zhao adjourned the meeting at 3:20 p.m. The next meeting was set for Wednesday, August 27, 2025, at 1:00 p.m.

*Minutes recorded by Dana Okafor.*

---

# Meeting No. 2

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, August 27, 2025
**Time:** 1:00 p.m. – 3:40 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members Absent:** None
**Others Attending:** Peter Ostrowski (ex officio, non-voting); Felix Marsh (Vice President of Product); Dana Okafor (recording secretary)

### 1. Call to Order and Approval of Minutes

Zhao called the meeting to order at 1:00 p.m. The minutes of the August 20 meeting were presented. Petrosyan moved approval; Radulescu seconded. Approved, 5–0.

### 2. Standing Incident and Error Budget Review

Yusuf reported that a second incident had occurred that morning. At 8:14 a.m., the certificate management subsystem again failed, this time because a manual certificate rotation performed as an interim fix following the August 12 incident had used a certificate with an incorrect validity window, again interrupting authentication to the deployment scheduler. Service was restored at 9:01 a.m., an outage of forty-seven minutes. Yusuf estimated 210 customers affected and stated that the incident traced to the same subsystem as August 12, reflecting insufficient interim remediation.

Radulescu reported preliminary results of the configuration audit ordered August 20: fourteen production changes in the preceding ninety days had been made outside standard code review, six of which touched the certificate management service.

The board noted the error budget remained exhausted for the quarter.

### 3. Error Budget Freeze Proposal and Release Date

Zhao stated that, given two incidents in the same subsystem within two weeks, she proposed an immediate error budget freeze, halting non-critical feature deployment and reallocating engineering capacity to remediation of the certificate management subsystem until the board determined the subsystem was stable. Zhao stated that, in her assessment, the freeze would require delaying the general availability date for release 4.0, then scheduled for October 6, 2025.

Marsh stated that release 4.0 included features already communicated to several strategic accounts and expressed concern about the effect of delay on customer commitments and competitive positioning, but stated that Product would defer to the board's judgment on reliability risk.

Whitfield stated she did not oppose a freeze in principle but was concerned that a freeze without a revised release date would create uncertainty that could itself damage customer trust. Petrosyan supported the freeze, citing the volume of support tickets generated by both incidents. Radulescu supported the freeze, citing unresolved exposure in the same subsystem. Yusuf supported the freeze, stating the team could not safely ship new functionality while the underlying subsystem remained unstable.

**Motion:** Zhao moved to adopt an immediate error budget freeze on non-critical production changes, effective August 27, 2025, pending the board's determination that the certificate management subsystem had been stabilized, and to suspend, without cancelling, the October 6 date for release 4.0 pending further review. Yusuf seconded.

**Vote:** Ayes — Zhao, Yusuf, Petrosyan, Radulescu. Nay — Whitfield. **Motion carried, 4–1.**

**Dissent:** Whitfield asked that her dissent be recorded. She stated she supported the freeze itself but believed the motion should have set a date by which the board would revisit the 4.0 schedule, rather than leaving it suspended indefinitely, given contractual commitments referencing 4.0 features held by at least two large accounts.

### 4. Remediation Plan

Yusuf presented the remediation plan drafted with Zhao pursuant to the August 20 action item: replacement of manual certificate rotation with automated rotation and redundant alerting, a two-person review requirement for changes to the certificate management service, and addition of the service to the on-call escalation runbook. The board endorsed the plan by consensus and directed Yusuf to begin implementation immediately.

### 5. Action Items

- Yusuf to lead remediation implementation, targeting completion by September 10, 2025.
- Radulescu to complete the full configuration audit report by September 3, 2025.
- Zhao to bring a revised 4.0 schedule to the board no later than the September 10 meeting, per Whitfield's request.
- Marsh to prepare customer messaging options, for legal review, for accounts awaiting 4.0 features, by September 3, 2025.
- Petrosyan to report the support ticket trend from the second incident at the next meeting.

### 6. Adjournment

Adjourned at 3:40 p.m. Next meeting: Wednesday, September 3, 2025, at 1:00 p.m.

*Minutes recorded by Dana Okafor.*

---

# Meeting No. 3

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, September 3, 2025
**Time:** 1:00 p.m. – 4:05 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair); Abdirahman Yusuf; Gwen Petrosyan; Tanisha Whitfield
**Members Absent:** Ivo Radulescu (excused; attending a security conference)
**Others Attending:** Peter Ostrowski (ex officio, non-voting); Colin Ashworth (Chief Financial Officer); Renata Byrne (General Counsel); Priya Nandakumar (Engagement Partner, Kestrel Assurance); Dana Okafor (recording secretary)

### 1. Call to Order and Approval of Minutes

Zhao called the meeting to order at 1:00 p.m. The minutes of August 27 were presented. Petrosyan moved approval; Whitfield seconded. Approved, 4–0, Radulescu absent.

### 2. Standing Incident and Error Budget Review

Yusuf reported no incidents since August 27. The freeze remained in effect. Automated certificate rotation with redundant alerting had been deployed to staging on September 1, with production rollout scheduled for September 8. The two-person review requirement for the certificate management service had been in effect since August 29. Zhao noted, in Radulescu's absence, that his written configuration audit report had been submitted prior to the meeting and confirmed the prior finding of fourteen out-of-review changes over ninety days, six touching the certificate management service, with the two-person review control now in place as a corrective measure.

### 3. SOC 2 Type II Finding

Nandakumar presented Kestrel Assurance's preliminary findings from the ongoing Type II examination. Kestrel had identified a control deficiency in change management: production changes had been, and could be, deployed without evidence of independent review, consistent with the board's own audit. Nandakumar stated this would likely be reported as a noted exception, and possibly a qualified opinion, unless the company implemented and demonstrated the operating effectiveness of a corrective control over a sustained testing period, typically sixty to ninety days. Byrne noted that approximately forty percent of the company's customers required a clean SOC 2 report to maintain or renew their contracts.

### 4. Customer Impact — Contractual Exits

Whitfield reported that two customers, together representing $3.4 million in annual renewal value, had invoked contractual exit language following the August incidents, one citing the outages and the other citing anticipated SOC 2 findings. Whitfield identified the accounts for the record by internal account code — Account 1142 and Account 2078 — and reported that account teams were engaging both customers in an effort to retain them, offering service credit and escalation commitments. Ashworth stated the $3.4 million represented approximately eight percent of annual recurring revenue and requested that finance be included in retention negotiations given revenue recognition implications.

### 5. Postmortem Publication — Debate and Vote

Zhao opened discussion of whether to publish a public postmortem covering the August 12 and August 27 incidents.

Whitfield argued for prompt, full publication, stating that customers were requesting transparency, that peer companies in the sector routinely published detailed postmortems, and that continued silence was itself damaging trust, particularly with the two accounts then considering exit. Byrne cautioned that a full postmortem disclosing the specific configuration change and control gap could be read as an admission bearing on both the SOC 2 exception and any claim the departing customers might bring, and recommended withholding detail pending completion of the Kestrel examination and legal review. Ostrowski stated that he supported transparency in principle but deferred to Byrne's assessment on timing. Yusuf expressed concern that technical detail in a postmortem could expose information useful to a bad actor, and stated he would have preferred Radulescu's input before voting. Petrosyan stated that support was fielding daily customer questions about the incidents and asked, at minimum, for an interim statement even if full publication were delayed.

**Motion:** Whitfield moved that the board authorize publication of a full public postmortem, including root cause detail, within five business days. Petrosyan seconded.

Zhao stated she could not support publication before legal and Kestrel had reviewed proposed content; Yusuf agreed.

**Vote:** Ayes — Whitfield, Petrosyan. Nays — Zhao, Yusuf. **Motion failed, 2–2, no majority.**

Zhao stated the matter would return to the agenda on September 10, by which time Radulescu would be present and Byrne would have completed review of a draft.

### 6. Action Items

- Byrne to complete legal review of a draft postmortem, including a determination of what detail could safely be disclosed, by September 9, 2025.
- Petrosyan, in coordination with Byrne, to issue an interim customer-facing statement acknowledging the incidents by September 5, 2025.
- Ashworth to bring finance into retention conversations for Accounts 1142 and 2078 by September 4, 2025.
- Nandakumar to deliver Kestrel's written findings letter to the board by September 8, 2025.
- Whitfield and Ashworth to jointly report retention status at the September 10 meeting.

### 7. Adjournment

Adjourned at 4:05 p.m. Next meeting: Wednesday, September 10, 2025, at 1:00 p.m.

*Minutes recorded by Dana Okafor.*

---

# Meeting No. 4

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, September 10, 2025
**Time:** 1:00 p.m. – 4:30 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members Absent:** None
**Others Attending:** Peter Ostrowski (ex officio, non-voting); Colin Ashworth (Chief Financial Officer); Renata Byrne (General Counsel); Odalys Ferreira (Vice President of People); Felix Marsh (Vice President of Product); Dana Okafor (recording secretary)

### 1. Call to Order and Approval of Minutes

Zhao called the meeting to order at 1:00 p.m. The minutes of September 3 were presented. Yusuf moved approval; Radulescu seconded. Approved, 5–0.

### 2. Standing Incident and Error Budget Review

Yusuf reported no incidents since August 27 — fourteen consecutive days without an incident in the certificate management subsystem. Automated rotation with redundant alerting had been deployed to production on September 8, as planned. The two-person review control had operated for twelve days without exception. Yusuf stated the error budget remained at zero for the quarter and would not begin to replenish until the freeze was lifted by board action.

### 3. Kestrel Assurance Follow-Up

Byrne summarized Nandakumar's written findings letter, received September 8. Kestrel confirmed the change management gap as a noted exception for the current examination period, but stated that the newly implemented two-person review control, if it continued to operate effectively through the remainder of the audit period, would support a clean opinion in the following cycle. Kestrel recommended the company retain documentation of control operation.

### 4. Customer Retention Update

Whitfield and Ashworth reported jointly. Account 1142 ($2.1 million) had agreed to remain under contract in exchange for a service credit and a ninety-day right to terminate without penalty in the event of a further incident in the same subsystem. Account 2078 ($1.3 million) had proceeded with its exit and would not renew at contract end in November. Ashworth stated the net revenue impact would be reflected in the Q3 forecast.

### 5. Postmortem Publication — Resumed Debate and Vote

Byrne reported completion of legal review and presented a draft postmortem describing the root cause categorically — an expired certificate compounded by an unreviewed configuration change — without disclosing specific system architecture or referencing the SOC 2 exception. Byrne recommended this version for publication.

Whitfield stated she continued to prefer full disclosure, arguing that the redacted version would not satisfy customers who had already learned informally of the SOC 2 finding and could appear evasive, and that Account 1142's continued relationship depended in part on visible transparency. Radulescu supported the redacted version, stating that disclosure of specific subsystem architecture created unnecessary security exposure. Petrosyan stated the redacted version was sufficient for support's purposes provided it was published promptly. Ostrowski stated he supported the redacted version and noted that Byrne's assessment reflected legal exposure the company could not responsibly disregard.

**Motion:** Zhao moved to authorize publication of the redacted postmortem, as drafted by Byrne, within ten business days of this meeting. Yusuf seconded.

**Vote:** Ayes — Zhao, Yusuf, Petrosyan, Radulescu. Nay — Whitfield. **Motion carried, 4–1.**

**Dissent:** Whitfield asked that her dissent be recorded, stating she believed the redacted version undercut the company's ability to rebuild trust with affected customers and that she would raise the matter again if retention losses continued.

### 6. Error Budget Freeze Extension and Release 4.0 Date

Zhao stated that, given the freeze had not yet produced a sufficient track record to justify resuming normal release velocity, and given the SOC 2 exception and continuing customer sensitivity, she recommended extending the error budget freeze through October 31, 2025, and formally rescheduling the general availability date for release 4.0 from October 6, 2025 to December 1, 2025.

Marsh stated Product had reviewed the proposed date with go-to-market teams and could support December 1, noting it would also allow time to align release communications with the postmortem's commitments.

**Motion:** Zhao moved to extend the error budget freeze through October 31, 2025, and to reschedule the release 4.0 general availability date to December 1, 2025. Radulescu seconded.

**Vote:** Ayes — Zhao, Yusuf, Petrosyan, Radulescu, Whitfield. **Motion carried, 5–0.**

Whitfield stated for the record that, while she supported the motion, she wished it noted that a firm date, even a delayed one, was preferable to the indefinite suspension adopted on August 27, consistent with her dissent of that date.

### 7. Revised On-Call Compensation Policy

Ferreira presented a revised on-call compensation policy developed with Yusuf and Petrosyan, providing increased hourly on-call pay, a minimum rest period following overnight incident response, and a defined escalation cap, intended to address on-call fatigue identified as a contributing factor in the interim fix that caused the August 27 incident.

**Motion:** Petrosyan moved to adopt the revised on-call compensation policy effective September 15, 2025. Yusuf seconded.

**Vote:** Ayes — all five. **Motion carried, 5–0.**

### 8. Hiring Requisitions Against Company-Wide Freeze

Zhao stated that, notwithstanding the company-wide hiring freeze instituted in July, the board should recommend two exception requisitions for reliability engineering roles, given the remediation and monitoring workload identified since August 12. Ostrowski stated he would support the requisitions before the executive staff, noting final approval rested with the Chief Executive Officer.

**Motion:** Yusuf moved that the board recommend to executive staff approval of two reliability engineering requisitions as an exception to the company-wide hiring freeze. Radulescu seconded.

**Vote:** Ayes — all five. **Motion carried, 5–0.**

### 9. Action Items

- Byrne and Whitfield to coordinate publication of the redacted postmortem no later than September 24, 2025.
- Ashworth to reflect the Account 2078 non-renewal in the Q3 forecast and report final Account 1142 credit terms by September 17, 2025.
- Ferreira to communicate the revised on-call compensation policy to affected staff by September 15, 2025.
- Zhao to submit the two reliability engineering requisitions to executive staff by September 12, 2025.
- Yusuf to continue tracking subsystem stability and report incident-free duration at each meeting; the freeze will be reviewed at the board's first meeting in November 2025.
- Marsh to align release 4.0 communications with the published postmortem by October 1, 2025.

### 10. Adjournment

There being no further business, Zhao adjourned the meeting at 4:30 p.m. The next meeting was set for Wednesday, September 17, 2025.

*Minutes recorded by Dana Okafor.*

# Meeting No. 5

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, September 17, 2025
**Time:** 1:00 p.m. – 3:35 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members Absent:** None
**Others Attending:** Peter Ostrowski (ex officio, non-voting); Colin Ashworth (Chief Financial Officer); Renata Byrne (General Counsel); Dana Okafor (recording secretary)

### 1. Call to Order and Approval of Minutes

Zhao called the meeting to order at 1:00 p.m. The minutes of September 10 were presented. Radulescu moved approval; Petrosyan seconded. Approved, 5–0.

### 2. Standing Incident and Error Budget Review

Yusuf reported no incidents since August 27 — twenty-one consecutive days without an incident in the certificate management subsystem. The two-person review control had now operated for nineteen days without exception, and Radulescu confirmed that his team's spot audit of the prior two weeks' production changes found no instances of review bypass. Yusuf stated the error budget remained frozen at zero pending the board's scheduled review in November, consistent with the September 10 motion.

### 3. Postmortem Publication Status

Byrne reported that the redacted postmortem approved on September 10 had cleared final legal review and was scheduled for publication on September 22, within the ten-business-day window set by the board. Whitfield asked that the published version include a named point of contact for follow-up questions from affected customers; Byrne agreed to add one. Petrosyan stated that support had prepared a response script for anticipated customer inquiries following publication.

### 4. Retention and Financial Update

Ashworth reported that the service credit terms for Account 1142 had been finalized at $184,000, consistent with the ninety-day conditional right to terminate approved September 10, and that the credit had been booked against Q3 revenue. Ashworth confirmed Account 2078's non-renewal remained on track for November and had been reflected in the Q3 forecast as previously reported. Whitfield stated no additional accounts had invoked exit language since September 3.

### 5. Requisition and Staffing Update

Zhao reported that the two reliability engineering requisitions had been submitted to executive staff on September 12, as directed, and that both had been approved by the Chief Executive Officer on September 15 as exceptions to the company-wide hiring freeze. Ferreira's office had opened both requisitions for recruiting; Zhao stated she would report candidate pipeline status at a future meeting once available.

### 6. On-Call Compensation Policy Rollout

Petrosyan reported that the revised on-call compensation policy had taken effect September 15 as scheduled and had been communicated to all affected engineering and support staff. Petrosyan stated initial feedback from the on-call rotation had been positive, with no implementation issues reported in the first two days.

### 7. Discussion — Kestrel Testing Period

Byrne reminded the board that Kestrel Assurance's recommendation contemplated a sustained testing period of sixty to ninety days for the two-person review control before a clean opinion could be supported in the next examination cycle. Byrne stated the clock had effectively started August 29 and recommended the board formally track the control's operating history at each meeting through at least late November. Zhao agreed and directed that this tracking be added as a standing sub-item under the incident and error budget review going forward.

### 8. Action Items

- Byrne to publish the redacted postmortem, with a named customer contact, on September 22, 2025.
- Petrosyan to monitor and report customer response to the postmortem at the September 24 meeting.
- Ashworth to confirm final booking of the Account 1142 credit and provide an updated Q3 forecast by September 19, 2025.
- Zhao to add tracking of the two-person review control's operating history as a standing item under the incident and error budget review, beginning September 24, 2025.
- Zhao to report requisition candidate pipeline status once available.

### 9. Adjournment

There being no further business, Zhao adjourned the meeting at 3:35 p.m. The next meeting was set for Wednesday, September 24, 2025, at 1:00 p.m.

*Minutes recorded by Dana Okafor.*

# Meeting No. 6

**Body:** Reliability Review Board, Huron Stack, Inc.
**Date:** Wednesday, September 24, 2025
**Time:** 1:00 p.m. – 3:50 p.m. Eastern
**Place:** Huron Stack, Inc. headquarters, Ann Arbor, Michigan — Conference Room 4B ("Argo")
**Members Present:** Meilin Zhao (Chair); Abdirahman Yusuf; Gwen Petrosyan; Ivo Radulescu; Tanisha Whitfield
**Members Absent:** None
**Others Attending:** Peter Ostrowski (ex officio, non-voting); Colin Ashworth (Chief Financial Officer); Renata Byrne (General Counsel); Dana Okafor (recording secretary)

### 1. Call to Order and Approval of Minutes

Zhao called the meeting to order at 1:00 p.m. The minutes of September 17 were presented. Whitfield moved approval; Yusuf seconded. Approved, 5–0.

### 2. Standing Incident and Error Budget Review

Yusuf reported no incidents since August 27 — twenty-eight consecutive days without an incident in the certificate management subsystem. Radulescu reported that the two-person review control had now operated for twenty-six days without exception, and, per the standing item added September 17, stated the control remained on pace to satisfy Kestrel's recommended testing window if it continued uninterrupted through late November. The error budget remained frozen at zero.

### 3. Postmortem Publication — Customer Response

Byrne confirmed the redacted postmortem had been published on September 22 as scheduled, with a named customer contact as requested by Whitfield on September 17. Petrosyan reported that support had received 62 inbound inquiries in the two days following publication, the substantial majority requesting confirmation of remediation status rather than raising new concerns. Petrosyan characterized the response as "manageable and largely reassured." Whitfield reported that Account 1142 had acknowledged the publication directly and stated it viewed the disclosure as a positive step, though she noted the account's ninety-day conditional termination right remained open through mid-December. Whitfield stated she remained of the view, consistent with her dissent of September 10, that a fuller disclosure would have been preferable, but did not renew a motion on the point.

### 4. Financial Update

Ashworth reported that the Account 1142 service credit of $184,000 had been formally booked against Q3 revenue and that the updated Q3 forecast, reflecting both the Account 1142 credit and the Account 2078 non-renewal, had been circulated to the board in writing prior to the meeting. Ashworth stated total identified financial impact of the August incidents, combining the original $1.2 million service credit estimate, the Account 1142 credit, and lost Account 2078 renewal value, stood at approximately $2.7 million recognized or booked to date, with the Account 2078 impact to be fully realized upon contract expiration in November.

### 5. Requisition and Staffing Update

Zhao reported that recruiting had opened both approved reliability engineering requisitions on September 16 and that, as of the meeting date, one candidate had reached final-round interviews. Zhao stated she expected to report an offer status at the October 1 meeting.

### 6. Discussion — Preparation for November Freeze Review

Zhao stated that, with the freeze scheduled for board review at the board's first meeting in November per the September 10 motion, she wished to begin establishing the criteria the board would use to evaluate whether to lift it. Yusuf proposed that the criteria include, at minimum, sixty consecutive incident-free days in the certificate management subsystem, completed rollout of automated rotation to all remaining environments, and a full cycle of the two-person review control without exception. Radulescu proposed adding a completed internal penetration test of the remediated subsystem. Discussion continued without a motion; Zhao stated a formal criteria proposal would be brought for a vote at the October 1 meeting.

### 7. Action Items

- Petrosyan to continue monitoring customer inquiry volume following the postmortem and report any material change at the next meeting.
- Ashworth to provide a final reconciliation of total incident-related financial impact once the Account 2078 non-renewal is realized in November.
- Zhao to report requisition offer status at the October 1 meeting.
- Zhao to draft formal criteria for lifting the error budget freeze, incorporating Yusuf's and Radulescu's proposals, for a vote at the October 1 meeting.
- Radulescu to scope an internal penetration test of the remediated certificate management subsystem and report timing and resourcing by October 1.

### 8. Adjournment

There being no further business, Zhao adjourned the meeting at 3:50 p.m. The next meeting was set for Wednesday, October 1, 2025, at 1:00 p.m.

*Minutes recorded by Dana Okafor.*
