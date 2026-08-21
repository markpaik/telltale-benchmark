# Standard Operating Procedure: Emergency Change Management and Break-Glass Access Control

## Document Control Block

| Field | Value |
|---|---|
| Document Number | SOP-ENG-014 |
| Version | 1.0 |
| Effective Date | 2026-08-15 |
| Owner | Nadia Oyelaran, Director of Platform Engineering |
| Approver | Ana Lucia Ferreiro, Chief Information Security Officer |
| Review Cycle | Semi-annual, or upon material incident, audit finding, or customer contractual demand |
| Classification | Internal — Controlled Document |
| Applies To | All production systems supporting clinical message routing for Larkspur Health Interfaces customers |

---

## 1. Purpose

This procedure establishes the mandatory controls governing emergency changes to production systems and the issuance, use, and revocation of just-in-time (JIT) break-glass credentials at Larkspur Health Interfaces. It exists to close the exceptions identified in the SOC 2 Type II report for the period ending December 31, 2025, specifically the absence of retrospective approval on emergency changes and the unrecorded, unreviewed use of a shared production credential that exposed 1,900 patient records.

This procedure ensures that every emergency change is authorized before or immediately after execution, every use of elevated production access is individually attributed, time-bound, and recorded, every deployment is subject to a second set of eyes, and every change touching protected health information (PHI) triggers customer notification consistent with Business Associate Agreement obligations and the HIPAA Breach Notification Rule.

## 2. Scope

This procedure applies to all emergency changes — defined in Section 4 — made to any production system that stores, processes, or transmits clinical messages on behalf of Larkspur Health Interfaces' 62 hospital customers, including message routing infrastructure, integration engines, customer-facing APIs, databases containing PHI, and the identity, secrets, and deployment tooling that support them.

It applies to all employees and contractors who hold, request, or approve production access, including the incident commander, on-call site reliability engineers (SREs), change approvers, peer reviewers, security analysts, and customer success leads. It does not cover standard (non-emergency) changes, which are governed separately under SOP-ENG-002, though a standard change that is later escalated to emergency status falls under this procedure from the point of escalation forward.

This procedure is binding on all systems named in Section 3 and supersedes any informal or verbal practice inconsistent with it.

## 3. Systems Referenced

- **GitHub Enterprise** — source control, pull requests, and code review evidence
- **Jira Service Management (JSM)** — system of record for all change tickets, including emergency changes
- **PagerDuty** — paging, on-call scheduling, and escalation policy enforcement
- **Terraform Cloud** — infrastructure-as-code plan and apply for production infrastructure changes
- **Okta** — identity provider, single sign-on, and group-based authorization
- **Vault (JIT credential service)** — issues production credentials scoped to individual users with a four-hour maximum lifetime
- **Logging Platform** — centralized audit log retained for 18 months, covering authentication, credential issuance, database query logs, deployment events, and ticket state changes

## 4. Definitions

**Emergency Change** — Any modification to a production system made outside the standard change window because a service-impacting or patient-safety-impacting condition requires immediate remediation, and the standard change approval lead time cannot be met without unacceptable risk to customers.

**Severity 1 (SEV1)** — Complete or near-complete loss of clinical message delivery for one or more customers, or any condition creating a credible risk of PHI exposure.

**Severity 2 (SEV2)** — Degraded message delivery, elevated error rates, or a security finding requiring same-day remediation but not immediate service loss.

**Severity 3 (SEV3)** — Localized or single-customer impact with an available workaround; escalation to emergency status requires Section 8 justification.

**Break-Glass Access** — Just-in-time, individually attributed, time-limited elevated credentials issued by Vault for the purpose of executing an emergency change or investigating an active incident. Break-glass access is never shared and never persistent.

**Retrospective Approval** — Formal sign-off by a designated Change Approver, recorded in the change ticket within the window defined in Section 9, confirming that an emergency change already executed was necessary, appropriately scoped, and properly evidenced.

**Two-Person Rule** — The requirement that no individual may both author and independently execute a production deployment; a second qualified person must review and approve the deployment artifact before it is applied.

**Protected Health Information (PHI) Touching Change** — Any change that creates, modifies, migrates, queries outside normal application logic, or otherwise provides human access to a database, table, log, or file containing patient-identifiable clinical data.

## 5. Roles and Responsibilities

**Incident Commander (IC)** — Declares severity, activates this procedure, coordinates the Change Approver, SRE, peer reviewer, and Security Analyst, and owns the timeline until the incident is resolved and handed to post-incident review.

**On-Call Site Reliability Engineer (SRE)** — Executes the technical remediation, requests break-glass credentials, and operates under the two-person rule with the peer reviewer.

**Designated Change Approver** — A named individual (never the same person as the executing SRE) authorized to approve emergency changes, either prospectively or retrospectively. The current roster is maintained in PagerDuty as the "Change Approver" escalation policy.

**Peer Reviewer** — A second qualified engineer, distinct from the executing SRE, who reviews the proposed change, Terraform plan, or query before execution and countersigns the change ticket.

**Security Analyst** — Monitors and validates break-glass credential issuance, reviews session logs, and determines whether a change or access event constitutes a reportable security incident under the breach risk assessment process.

**Customer Success Lead** — Executes customer notification when a change is determined to be PHI-touching or customer-impacting, per Section 12.

**Director of Platform Engineering (Procedure Owner)** — Maintains this document, tracks compliance metrics, and reports exceptions to the CISO.

**Chief Information Security Officer (Approver)** — Approves this procedure, approves any deviation request under Section 13, and is the escalation point for unresolved conflicts between Incident Commander and Change Approver.

## 6. Severity Declaration

**6.1** Any employee who identifies a condition meeting the SEV1 or SEV2 definition in Section 4 pages the on-call Incident Commander via PagerDuty using the "Production Incident" service.

**6.2** The Incident Commander declares severity within 10 minutes of being paged. Severity declaration is recorded as the first comment in a new Jira Service Management ticket created from the "Emergency Change" issue type. The ticket must state: the observed condition, the customer(s) affected, the declared severity, and the timestamp of declaration.

**6.3** SEV1 automatically authorizes emergency change procedures. SEV2 authorizes emergency change procedures if the Incident Commander documents in the ticket why the standard change window cannot be met. SEV3 requires escalation per Section 8 before emergency procedures may be invoked.

**6.4** The Incident Commander pages the Change Approver escalation policy in PagerDuty immediately upon severity declaration, regardless of time of day.

## 7. Authorization Window for Emergency Changes

**7.1** Prospective authorization is the default path. The Change Approver must respond to the page within 15 minutes for SEV1 and 30 minutes for SEV2.

**7.2** If the Change Approver responds within the window, they review the proposed remediation as described by the SRE in the Jira ticket, and record explicit approval — the words "Approved" or "Denied" plus their name and timestamp — as a ticket comment before execution begins.

**7.3** If prospective approval is granted, the SRE proceeds to Section 9 (JIT access) and Section 10 (two-person deployment).

**7.4** If the Change Approver cannot be reached within the window, the Incident Commander invokes the unreachable-approver exception in Section 13.1 and proceeds under retrospective authorization, which must still occur within the window defined in Section 11.

**7.5** No emergency change may proceed without either prospective approval recorded in the ticket or a documented invocation of Section 13.1. A change with neither is a procedural violation and must be escalated to the CISO within one business day of discovery.

## 8. Escalating a SEV3 to Emergency Status

**8.1** The Incident Commander (or the reporting engineer, if no IC has yet been assigned) documents in the Jira ticket why the standard change process — which requires a minimum 24-hour peer review and scheduled deployment window — cannot be met.

**8.2** Acceptable justifications include: the workaround is degrading, the issue is trending toward SEV2, or a customer has an active compliance deadline tied to the fix.

**8.3** Escalation requires sign-off from the Change Approver before the ticket is reclassified from "Standard Change" to "Emergency Change" in Jira. Once reclassified, all remaining sections of this procedure apply.

## 9. Just-in-Time Production Access

**9.1** No individual holds standing production credentials. All production access is requested through Vault at the time of need.

**9.2** The SRE authenticates to Vault using Okta single sign-on with multi-factor authentication. Vault verifies the requester's Okta group membership against the target system's authorized role before issuing a credential.

**9.3** The SRE submits the access request through Vault's CLI or web interface, entering the associated Jira ticket number as a mandatory field. Vault rejects any production credential request that does not reference an open, active change or incident ticket.

**9.4** Vault issues a credential scoped to the minimum system and privilege level needed for the declared purpose, with a maximum lifetime of four hours. Credentials do not auto-renew. If the work will exceed four hours, the SRE requests a new credential and states the reason in the ticket; Vault logs the reissuance as a linked event.

**9.5** Vault writes an issuance record to the Logging Platform at the moment of grant, capturing: requester identity, ticket number, target system, scope granted, issuance timestamp, and scheduled expiry.

**9.6** All actions taken under a break-glass credential must occur within a session that is recorded. For database access, this means the query session runs through the bastion/proxy layer configured to log full query text and result-set metadata to the Logging Platform. Direct, unproxied database connections using break-glass credentials are prohibited. Any engineer who cannot complete the work through the proxy must stop and contact the Security Analyst before proceeding by any other means.

**9.7** Credentials are automatically revoked by Vault at expiry. An SRE who completes work before expiry manually revokes the credential through Vault and records the revocation timestamp in the ticket. Vault logs both automatic and manual revocation events to the Logging Platform.

**9.8** Shared credentials of any kind — service accounts, generic "admin" logins, or credentials known to more than one person — are prohibited for emergency change execution or investigation. Any discovery of a shared credential in active use triggers immediate revocation by the Security Analyst and a breach risk assessment per Section 15.

## 10. Two-Person Rule for Deployment

**10.1** No deployment to production may be applied by the same individual who authored the change. This applies to code merged in GitHub Enterprise, infrastructure changes planned in Terraform Cloud, and manual configuration changes of any kind.

**10.2** For code changes: the SRE opens a pull request in GitHub Enterprise referencing the Jira ticket number. The Peer Reviewer reviews the diff and approves the pull request in GitHub before merge. A self-approved pull request cannot be merged; GitHub Enterprise branch protection rules enforce this technically for all production branches.

**10.3** For infrastructure changes: the SRE generates a Terraform Cloud plan. The Peer Reviewer reviews the plan output in Terraform Cloud and clicks "Confirm & Apply." The executing SRE may queue the plan but may not be the one who confirms the apply.

**10.4** For manual production actions that cannot be captured in code (for example, a manual failover or a direct data correction under Section 9.6), the Peer Reviewer must be present on the incident call and verbally confirm each step before the SRE executes it. The Peer Reviewer records their confirmation as a ticket comment with timestamp, listing the specific action approved.

**10.5** If no Peer Reviewer is reachable within 20 minutes of a SEV1 declaration, the Incident Commander may act as Peer Reviewer only if they did not author the change, and must document this substitution in the ticket.

## 11. Retrospective Approval and Evidence Attachment

**11.1** Every emergency change, whether prospectively or retrospectively authorized, requires a documented retrospective approval entry in the Jira ticket. This is the control that failed in 9 of 34 cases in the prior audit period and is treated as non-negotiable.

**11.2** Retrospective approval must be recorded by the Change Approver no later than 24 hours after the change is deployed, regardless of whether prospective approval was already granted. Retrospective approval is a distinct, separately recorded action — a prospective "Approved" comment does not substitute for it.

**11.3** The retrospective approval comment must include: confirmation that the change matched what was authorized, confirmation that evidence is attached, and the Change Approver's assessment of whether the change should inform the standard change process going forward.

**11.4** Evidence attached to the ticket before retrospective approval can be recorded must include, at minimum: the GitHub Enterprise pull request link or Terraform Cloud run link, the Vault credential issuance and revocation timestamps, the Logging Platform session log reference, and screenshots or exported logs showing the post-change validation (health check, error rate, or query result confirming remediation).

**11.5** The Jira ticket automation (configured by the Procedure Owner) flags any Emergency Change ticket that reaches the 24-hour mark without a recorded retrospective approval, notifying the Change Approver, the Incident Commander, and the Director of Platform Engineering. Tickets open past 48 hours without retrospective approval are escalated to the CISO automatically.

**11.6** No emergency change ticket may be closed until retrospective approval is recorded and all evidence in 11.4 is attached. Jira workflow configuration blocks the "Closed" transition until both conditions are met.

## 12. Customer Notification for PHI-Touching Changes

**12.1** At the time an emergency change is declared, the Incident Commander and Security Analyst jointly assess whether the change is PHI-touching per the Section 4 definition. This assessment is recorded in the ticket as "PHI-Touching: Yes/No" with a one-line rationale.

**12.2** If the assessment is "Yes," the Customer Success Lead is paged via PagerDuty within one hour of the determination, regardless of time of day.

**12.3** The Customer Success Lead notifies each affected customer's designated security or compliance contact within 24 hours of the determination, using the approved notification template, stating: the nature of the change, the systems or data elements involved, whether patient data was viewed by an individual as part of the remediation, and the point of contact for follow-up questions.

**12.4** If the assessment later changes — for example, if post-incident review determines that PHI was accessed when it was not previously identified — the Customer Success Lead issues a supplemental notification within 24 hours of the revised determination, and the Security Analyst opens a breach risk assessment per Section 15 if not already open.

**12.5** All notifications are logged in the ticket with timestamp, recipient, and method (email or customer portal), and a copy of the notification content is attached as evidence.

## 13. Exception Paths

**13.1 Unreachable Approver at Non-Business Hours (e.g., 3:00 a.m.)**

If the on-call Change Approver does not respond to PagerDuty paging within the window in Section 7.1, PagerDuty automatically escalates to the secondary Change Approver after 15 minutes. If the secondary also does not respond within a further 15 minutes, the Incident Commander is authorized to proceed under retrospective-only authorization, provided that:

- the Incident Commander records in the ticket the names and timestamps of both paging attempts and non-responses,
- the Peer Reviewer requirement in Section 10 is still fully satisfied,
- retrospective approval is obtained from any available Change Approver within 24 hours per Section 11, and
- the Director of Platform Engineering is notified the same day so PagerDuty escalation coverage can be reviewed.

**13.2 Customer-Mandated Freeze Window**

Some customers, including Sagebrush Health Network, impose contractual freeze windows during which no changes may be deployed to their environment absent an active SEV1. If an emergency change is needed during a customer freeze window:

- the Incident Commander confirms the current severity is SEV1, or escalates it per Section 8 with explicit reference to the freeze conflict,
- the Customer Success Lead contacts the customer's emergency contact before deployment, using the customer's own emergency escalation path, and documents the contact attempt and outcome in the ticket,
- if the customer cannot be reached and the condition is actively causing service loss or PHI exposure, the change may proceed without customer consent, but this decision must be approved by the CISO or, if unreachable, by the Director of Platform Engineering, and documented as a freeze-window override in the ticket, and
- the customer is notified within 4 hours after the fact regardless of the outcome of the pre-deployment contact attempt.

**13.3 Rollback Failure**

If a rollback of an emergency change itself fails or introduces a new fault:

- the Incident Commander immediately re-declares severity to SEV1 if not already at that level,
- a new Jira ticket is opened linked to the original, titled "Rollback Failure — [original ticket number]," and both tickets remain open until resolution,
- the Incident Commander pages the Change Approver, a second SRE distinct from the one who attempted the rollback, and the Security Analyst simultaneously,
- no further changes are attempted by the original SRE alone; the two-person rule applies to every subsequent remediation attempt without exception,
- if the system cannot be restored to either the pre-change or post-change working state within one hour, the Incident Commander escalates to the CISO and the Director of Platform Engineering for a joint decision on next steps, which may include invoking a disaster recovery procedure (SOP-ENG-009), and
- the Customer Success Lead notifies affected customers of the extended impact within 2 hours of the rollback failure being confirmed, separate from any PHI notification under Section 12.

## 14. Quarterly Access Recertification

**14.1** On the first business day of January, April, July, and October, the Security Analyst generates a report from Okta and Vault listing every individual with any standing group membership that grants eligibility to request break-glass production access.

**14.2** The Security Analyst distributes the report to each individual's manager, who must confirm within 5 business days whether continued access is required, with justification tied to current role responsibilities.

**14.3** Any access not affirmatively recertified within 5 business days is automatically revoked in Okta by the Security Analyst, and the affected individual is notified.

**14.4** The Security Analyst separately reviews the prior quarter's Logging Platform records of actual break-glass credential issuance and flags any individual with standing eligibility who has not used access in two consecutive quarters for manager review and possible removal from the eligible group.

**14.5** Recertification results, including all revocations and manager confirmations, are recorded in a Jira ticket of type "Access Recertification" and retained as evidence for the next SOC 2 audit period.

**14.6** The Director of Platform Engineering reviews the completed recertification and reports summary statistics — total eligible population, revocations, and exceptions — to the CISO within 10 business days of the recertification deadline.

## 15. Post-Incident Review

**15.1** Every emergency change ticket, upon closure, automatically generates a Post-Incident Review (PIR) task assigned to the Incident Commander, due within 5 business days.

**15.2** The PIR is documented in Confluence, linked from the original Jira ticket, and must address: root cause, timeline of detection through resolution, whether this procedure was followed in full (with explicit note of any Section 13 exception invoked), whether the retrospective approval and evidence requirements in Section 11 were met on time, and what preventive or process action items result.

**15.3** The Security Analyst independently reviews every PIR involving a Section 13 exception, a PHI-touching change, or a rollback failure, and determines whether a breach risk assessment must be opened under the organization's Incident Response Plan (IRP-001). The 1,900-record exposure event of March 2026 is the reference case for this determination: any unrecorded or unreviewed access to patient data triggers this same assessment path regardless of whether harm is later confirmed.

**15.4** Action items from the PIR are entered as Jira tasks assigned with owners and due dates, and tracked to closure by the Director of Platform Engineering in the monthly engineering operations review.

**15.5** Aggregated PIR themes are reviewed quarterly by the Director of Platform Engineering and the CISO to identify whether this procedure itself requires revision.

## 16. Records

The following records are generated and retained as evidence of compliance with this procedure, each retained for a minimum of 18 months on the Logging Platform or in Jira, whichever is the system of record:

- Emergency Change tickets (Jira Service Management), including severity declaration, prospective and retrospective approvals, and evidence attachments
- Vault credential issuance and revocation logs
- GitHub Enterprise pull request approval records
- Terraform Cloud plan and apply confirmation records
- PagerDuty paging and escalation history
- Customer notification records, including template used and delivery timestamp
- Quarterly Access Recertification tickets and revocation logs
- Post-Incident Review documents in Confluence
- Breach risk assessment records, where triggered, maintained per IRP-001

## 17. References

- SOC 2 Type II Report, period ending December 31, 2025 (Change Management exception)
- HIPAA Security Rule, 45 CFR §164.312 (Technical Safeguards)
- HIPAA Breach Notification Rule, 45 CFR §164.400–414
- Business Associate Agreement — Sagebrush Health Network (audit clause reference)
- Larkspur Health Interfaces Incident Response Plan (IRP-001)

## 18. Related Documents

- SOP-ENG-002: Standard Change Management Procedure
- SOP-ENG-009: Disaster Recovery Procedure
- SOP-SEC-005: Access Control and Identity Management Policy
- SOP-SEC-011: Breach Risk Assessment Procedure
- Customer Notification Template Library (Customer Success shared drive)

## 19. Revision History

| Version | Date | Author | Summary of Change |
|---|---|---|---|
| 0.1 | 2026-06-02 | N. Oyelaran | Initial draft in response to SOC 2 exception and March break-glass incident |
| 0.2 | 2026-06-20 | N. Oyelaran | Added freeze-window and rollback-failure exception paths per Sagebrush requirements |
| 0.3 | 2026-07-10 | N. Oyelaran | Incorporated Security Analyst review; added quarterly recertification section |
| 1.0 | 2026-08-15 | N. Oyelaran (Owner) / A. L. Ferreiro (Approver) | Approved for release; effective date set; distributed to all roles in Section 5 |

## Appendix A: Escalation Contact Matrix

| Role | Primary Contact Method | Escalation Timeout | Secondary Contact Method | Escalation Timeout | Tertiary |
|---|---|---|---|---|---|
| Incident Commander | PagerDuty — "IC On-Call" | 10 min | PagerDuty secondary IC rotation | 10 min | Director of Platform Engineering (direct page) |
| Change Approver | PagerDuty — "Change Approver" | 15 min (SEV1) / 30 min (SEV2) | PagerDuty secondary Change Approver rotation | 15 min | CISO (direct page) |
| On-Call SRE | PagerDuty — "SRE On-Call" | 10 min | PagerDuty secondary SRE rotation | 10 min | IC assigns any available SRE |
| Peer Reviewer | PagerDuty — "Peer Review Pool" | 20 min | Slack #incident-response broadcast | 10 min | IC acts as Peer Reviewer (Section 10.5) |
| Security Analyst | PagerDuty — "Security On-Call" | 15 min | Direct call, CISO-maintained roster | 15 min | CISO (direct page) |
| Customer Success Lead | PagerDuty — "CS Incident Liaison" | 60 min (PHI notification trigger) | Slack #customer-success-oncall | 30 min | VP Customer Success (direct page) |

Contact rosters are maintained in PagerDuty by the Director of Platform Engineering and audited quarterly alongside the access recertification cycle in Section 14. Any gap in coverage discovered during an actual escalation must be logged as a ticket comment and reviewed at the next monthly engineering operations review.

## Appendix B: Emergency Change Ticket — Required Fields

Every ticket created under the "Emergency Change" issue type in Jira Service Management must, at minimum, contain the following fields before it can transition out of "Open" status:

| Field | Description | Populated By | Required Before |
|---|---|---|---|
| Severity | SEV1 / SEV2 / SEV3-escalated | Incident Commander | Section 6 declaration |
| Affected Customer(s) | Named customer(s) or "internal only" | Incident Commander | Section 6 declaration |
| PHI-Touching | Yes / No + one-line rationale | Incident Commander + Security Analyst | Section 12.1 assessment |
| Prospective Approval | Approver name, timestamp, Approved/Denied | Change Approver | Execution start |
| Exception Invoked | None / 13.1 / 13.2 / 13.3 + rationale | Incident Commander | Execution start, if applicable |
| Peer Reviewer | Name of reviewer, method (PR / Terraform / verbal) | SRE | Deployment |
| Vault Credential Reference | Issuance ID, scope, expiry timestamp | SRE (auto-populated by Vault integration where available) | Access grant |
| Evidence Links | GitHub PR, Terraform run, Logging Platform session ID, validation screenshot | SRE | Retrospective approval |
| Retrospective Approval | Approver name, timestamp, confirmation statement | Change Approver | Ticket closure |
| Customer Notification | Sent Yes/No, timestamp, method | Customer Success Lead | Ticket closure, if PHI-Touching = Yes |
| PIR Link | Confluence link to Post-Incident Review | Incident Commander | 5 business days post-closure |

Jira workflow automation, configured by the Procedure Owner, enforces field completeness as workflow gates; a ticket cannot move to "Retrospective Review," "Pending Notification," or "Closed" without the corresponding fields above populated.

## Appendix C: Customer Notification Template — PHI-Touching Change

Subject line: **Notice of System Change Affecting [Customer Name] — [Ticket Number]**

> Dear [Customer Security/Compliance Contact Name],
>
> This notice is provided under the terms of our Business Associate Agreement to inform you of an emergency system change that may have involved access to protected health information within your environment.
>
> **Date/time of change:** [timestamp]
> **System(s) involved:** [system name(s)]
> **Nature of the change:** [one to two sentence plain-language description]
> **Was patient data viewed by a human as part of this change:** [Yes/No — if Yes, describe scope: number of records, data elements, method of access]
> **Root cause:** [one sentence, or "under investigation, follow-up to be provided within 5 business days"]
> **Remediation status:** [Resolved / Monitoring / Ongoing]
> **Your point of contact for questions:** [Customer Success Lead name, email, phone]
>
> We will provide a follow-up report, including outcomes of our internal post-incident review, within 5 business days. If our ongoing assessment identifies that this event meets the threshold for breach notification under 45 CFR §164.400 et seq., we will notify you separately and immediately in accordance with our Business Associate Agreement.
>
> Sincerely,
> [Customer Success Lead Name]
> Larkspur Health Interfaces

The Customer Success Lead may not modify the "Was patient data viewed" or "Nature of the change" fields without confirming exact wording with the Security Analyst, since these statements may be referenced in subsequent regulatory or audit correspondence.

## Appendix D: Decision Path Summary (Text Flowchart)

1. Condition observed → page Incident Commander via PagerDuty.
2. Incident Commander declares severity within 10 minutes → Jira ticket opened.
   - SEV1 → proceed to step 3.
   - SEV2 → Incident Commander documents window justification → proceed to step 3.
   - SEV3 → proceed to Appendix D Section 8 escalation path; if approved, proceed to step 3; if not approved, handle under standard change SOP-ENG-002.
3. Incident Commander pages Change Approver.
   - Response within window → prospective approval recorded → proceed to step 4.
   - No response within window → invoke Section 13.1 → document non-response → proceed to step 4 under retrospective-only authorization.
4. SRE requests Vault credential, referencing ticket number → credential issued, 4-hour maximum, proxied session only.
5. SRE prepares change (PR, Terraform plan, or documented manual step) → Peer Reviewer reviews and approves before execution.
   - Peer Reviewer unavailable within 20 minutes → Incident Commander substitutes if not the change author → documented in ticket.
6. Change executed under two-person rule.
7. Post-execution validation performed and evidence attached to ticket.
8. Incident Commander + Security Analyst determine PHI-Touching status.
   - Yes → Customer Success Lead paged within 1 hour → customer notified within 24 hours.
   - No → proceed to step 9.
9. Change Approver records retrospective approval within 24 hours of deployment.
10. Ticket closed only when retrospective approval and all evidence fields (Appendix B) are complete.
11. Post-Incident Review task auto-generated, due within 5 business days.
12. Security Analyst determines whether a breach risk assessment (IRP-001) must be opened, independent of steps 8–11, based on PIR content and any Section 13 exception invoked.

If at any point a rollback is required and that rollback fails, exit this flow and enter Section 13.3 immediately, re-declaring severity to SEV1.

## Appendix E: Glossary of Acronyms

| Acronym | Meaning |
|---|---|
| IC | Incident Commander |
| SRE | Site Reliability Engineer |
| JIT | Just-in-Time (credential issuance) |
| JSM | Jira Service Management |
| PHI | Protected Health Information |
| PIR | Post-Incident Review |
| SEV1 / SEV2 / SEV3 | Severity levels 1 through 3, per Section 4 |
| SOC 2 | System and Organization Controls report, Type II |
| IRP | Incident Response Plan |
| CISO | Chief Information Security Officer |

---

*End of document. This SOP is a controlled document. Printed or downloaded copies are uncontrolled and may not reflect the current approved version. The current version of record resides in the Larkspur Health Interfaces policy repository under document number SOP-ENG-014.*

## Appendix F: Control Mapping to Audit Findings

This table maps each control established in this procedure to the specific SOC 2 Type II exception and the March 2026 break-glass incident, for use in response to Sagebrush Health Network's audit clause invocation and in preparation for the next SOC 2 examination period.

| Finding | Root Cause Identified | Control(s) Established | Section Reference |
|---|---|---|---|
| 9 of 34 emergency changes lacked retrospective approval | No defined deadline or workflow gate forcing retrospective sign-off; approval treated as optional after prospective authorization | Mandatory 24-hour retrospective approval window; Jira workflow gate blocking ticket closure without it; automated escalation at 24 and 48 hours | Section 11; Section 16 |
| 4 changes had no ticket at all | No technical control preventing production changes outside the ticketing system | Vault credential issuance now requires a valid, open ticket number as a mandatory field; GitHub branch protection and Terraform Cloud apply gates require linked ticket reference | Section 9.3; Section 10.2–10.3 |
| Shared break-glass credential used, session unrecorded | Standing/shared credentials existed; no proxy layer enforced session logging | Elimination of standing and shared credentials; all access issued individually through Vault with 4-hour maximum lifetime; mandatory proxied, logged sessions for all database access | Section 9.1, 9.6, 9.8 |
| 1,900 patient records exposed to unreviewed access | No real-time detection of out-of-band data access; no defined breach risk assessment trigger tied to access anomalies | Security Analyst independent review of all Section 13 exceptions, PHI-touching changes, and rollback failures; explicit breach risk assessment trigger for any unrecorded or unreviewed PHI access | Section 15.3 |
| No documented customer notification process for PHI-touching changes | Notification was ad hoc and undocumented | Formal PHI-touching determination at time of severity declaration; defined notification windows (1 hour to page, 24 hours to notify); approved template (Appendix C) | Section 12 |
| No quarterly review of who holds elevated access eligibility | Access grants persisted indefinitely without re-justification | Quarterly recertification cycle with automatic revocation on non-response | Section 14 |

This mapping is maintained by the Director of Platform Engineering and updated whenever a new audit finding, customer-mandated control, or internal PIR action item requires a change to this procedure.

## Appendix G: Training and Acknowledgment Log

All individuals named in Section 5 as executing roles must complete training on this procedure and record acknowledgment before being added to any PagerDuty escalation policy or Okta group referenced herein.

| Requirement | Detail |
|---|---|
| Initial training | Live walkthrough of Sections 6–15 plus tabletop exercise covering one prospective-approval scenario and one Section 13 exception scenario, conducted by the Director of Platform Engineering or delegate |
| Acknowledgment | Individual signs an attestation in the HR/compliance system confirming they have read this SOP in full, retained as a record alongside the recertification records in Section 16 |
| Refresher cadence | Annual, or immediately upon any version change that modifies Sections 6 through 15 |
| New hire timing | Must be completed before the individual is added to any PagerDuty rotation or granted Okta group membership enabling Vault access requests |
| Tabletop exercise cadence | Quarterly, rotating through the three exception paths in Section 13 so that every eligible on-call individual has rehearsed each at least once every 12 months |

The Security Analyst maintains the acknowledgment and tabletop participation log and reports completion rates to the CISO as part of the quarterly access recertification reporting in Section 14.6. Any individual with production access eligibility who has not completed initial training and acknowledgment is excluded from the eligible population and flagged for removal in the next recertification cycle.

## Appendix H: 30-Day Remediation Milestone Tracker — Sagebrush Health Network

In response to Sagebrush Health Network's demand for documented controls within 30 days, the following milestones apply from the effective date of this procedure.

| Milestone | Owner | Target Date (from effective date) | Evidence Delivered to Sagebrush |
|---|---|---|---|
| SOP-ENG-014 approved and distributed to all executing roles | N. Oyelaran | Day 0 | Copy of approved SOP, version 1.0 |
| Vault ticket-reference enforcement and proxy-only database access deployed to production | N. Oyelaran (technical), A. L. Ferreiro (sign-off) | Day 7 | Change ticket confirming configuration deployed; Security Analyst validation memo |
| Jira workflow gates (retrospective approval, evidence attachment) live in production instance | N. Oyelaran | Day 10 | Screenshot of workflow configuration; sample ticket demonstrating gate enforcement |
| Initial training and tabletop exercise completed for all current on-call personnel | Security Analyst | Day 14 | Training completion log excerpt (names redacted for external delivery, counts provided) |
| First full quarterly access recertification executed under new procedure | Security Analyst | Day 21 | Recertification summary report (Section 14.5) |
| First post-incident review conducted end-to-end under new procedure, if an emergency change occurs in the window | Incident Commander (whoever is on rotation) | Day 30 or upon next emergency change, whichever first | PIR document reference number; confirmation of on-time retrospective approval and evidence attachment |
| Formal written confirmation of control implementation delivered to Sagebrush compliance contact | A. L. Ferreiro | Day 30 | Letter summarizing Appendix F mapping and milestone completion status |

If any milestone slips, the Director of Platform Engineering notifies the CISO within one business day, and the CISO determines whether proactive disclosure to Sagebrush is warranted ahead of the Day 30 deadline, consistent with the audit clause obligations in the Business Associate Agreement.

## Appendix I: Quick Reference Card — On-Call Pocket Guide

This card is distributed separately as a laminated or pinned digital reference for the on-call SRE and Incident Commander rotations. It restates the time-critical thresholds from the body of this procedure for rapid reference during an active incident; it does not replace the full procedure.

**Paging thresholds**
- SEV1 → Change Approver must respond within 15 minutes
- SEV2 → Change Approver must respond within 30 minutes
- Peer Reviewer must respond within 20 minutes or IC substitutes (if not change author)
- PHI-Touching determination → page Customer Success Lead within 1 hour

**Vault access**
- Maximum credential lifetime: 4 hours, no auto-renew
- Ticket number required at request time — no ticket, no credential
- Database access must go through the logged proxy — never direct connection
- Manually revoke on completion; do not wait for auto-expiry if work finishes early

**Two-person rule — non-negotiable**
- You cannot approve/merge/apply your own change
- Verbal manual actions require the Peer Reviewer live on the call, confirming each step before you act

**Retrospective approval**
- Due within 24 hours of deployment — every time, even if pre-approved
- Ticket cannot close without it plus evidence: PR/Terraform link, Vault issuance/revocation timestamps, Logging Platform session ID, validation proof

**If you can't reach the Change Approver (Section 13.1)**
- Two paging attempts, 15 minutes apart, both documented in ticket
- Peer Reviewer requirement still applies — no shortcut
- Retrospective approval still required within 24 hours
- Notify Director of Platform Engineering same day

**If it's a customer freeze window (Section 13.2)**
- Confirm SEV1 or escalate first
- Customer Success Lead attempts contact via customer's own emergency path, documents outcome
- Can't reach customer + active harm → CISO or Director of Platform Engineering approves override
- Customer notified within 4 hours regardless

**If your rollback fails (Section 13.3)**
- Immediately re-declare SEV1
- Open linked "Rollback Failure" ticket
- Stop acting alone — page a second SRE, Change Approver, and Security Analyst together
- No further attempts without two-person rule
- One hour unresolved → escalate to CISO and Director of Platform Engineering jointly

**When in doubt:** page the Incident Commander. Do not proceed on an assumption. Silence in the ticket is treated the same as a missed control.

## Document Distribution List

This procedure, upon approval, is distributed to and acknowledgment tracked for the following:

| Recipient Group | Distribution Method | Acknowledgment Required |
|---|---|---|
| Platform Engineering (all SREs) | Internal policy repository + email notification | Yes — per Appendix G |
| Security team (Security Analysts) | Internal policy repository + email notification | Yes — per Appendix G |
| Incident Commander rotation members | Internal policy repository + PagerDuty onboarding packet | Yes — per Appendix G |
| Change Approver roster | Internal policy repository + direct briefing by Director of Platform Engineering | Yes — per Appendix G |
| Customer Success leadership | Internal policy repository + team briefing | Yes — acknowledgment of Sections 12 and 13.2 specifically |
| Executive team (CEO, CTO) | Internal policy repository | Informational; no acknowledgment required |
| Sagebrush Health Network (external) | Formal letter per Appendix H, Day 30 milestone | Not applicable — external evidence delivery only |
| Auditor (next SOC 2 examination) | Provided as evidence artifact during fieldwork | Not applicable |

## Approval Signatures

By signing below, the Owner and Approver confirm that this procedure has been reviewed in full, reflects current operational practice, and is authorized for distribution and enforcement effective on the date in the Document Control Block.

**Owner**

Name: Nadia Oyelaran
Title: Director of Platform Engineering
Signature: _______________________
Date: _______________________

**Approver**

Name: Ana Lucia Ferreiro
Title: Chief Information Security Officer
Signature: _______________________
Date: _______________________

---

*This concludes SOP-ENG-014, Version 1.0. All appendices (A through I) are integral parts of this controlled document and are subject to the same review cycle stated in the Document Control Block.*
