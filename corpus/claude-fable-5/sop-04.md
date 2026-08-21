# Standard Operating Procedure: Emergency Change Management and Just-in-Time Production Access

---

## 1. Document Control

| Field | Value |
|---|---|
| **Document Number** | SOP-ENG-014 |
| **Version** | 2.0 |
| **Effective Date** | August 24, 2026 |
| **Document Owner** | Nadia Oyelaran, Director of Platform Engineering |
| **Approver** | Ana Lucia Ferreiro, Chief Information Security Officer |
| **Review Cycle** | Annual, or within 30 days of any SOC 2 exception, reportable security incident, or material change to the systems named in Section 3.2 |
| **Classification** | Internal — Shareable with customers under NDA upon Customer Success approval |
| **Supersedes** | SOP-ENG-014 v1.3 (Emergency Change Handling, effective March 15, 2024) |
| **Next Scheduled Review** | August 24, 2027 |

**Approval Signatures**

| Role | Name | Signature | Date |
|---|---|---|---|
| Document Owner | Nadia Oyelaran | *On file in Jira Service Management record LHI-GOV-2026-081* | August 20, 2026 |
| Approver (CISO) | Ana Lucia Ferreiro | *On file in Jira Service Management record LHI-GOV-2026-081* | August 21, 2026 |

---

## 2. Purpose

This procedure defines how Larkspur Health Interfaces ("Larkspur") declares, authorizes, executes, records, and reviews emergency changes to production systems, and how personnel obtain, use, and relinquish just-in-time (JIT) production access, including break-glass access during incidents.

Larkspur operates a clinical integration platform that moves approximately 41 million clinical messages per day on behalf of 62 hospital customers. Emergency changes to this platform carry two categories of risk that this procedure is designed to control:

1. **Change risk** — an unauthorized, unreviewed, or undocumented change may degrade message delivery, corrupt clinical data in transit, or introduce a security vulnerability.
2. **Access risk** — production access granted under time pressure may expose protected health information (PHI) to personnel without a need to know, without session recording, or without timely revocation.

This procedure directly remediates the exception noted in Larkspur's SOC 2 Type II report for the period ending December 31, 2025 (change management criterion: 9 of 34 emergency changes lacked retrospective approval; 4 lacked a ticket entirely) and the March 2026 break-glass incident in which a shared credential was used to query a customer database without session recording, exposing 1,900 patient records to unreviewed access. It is also responsive to the documented-controls demand issued by Sagebrush Health Network under the audit clause of its Master Services Agreement.

Every emergency change, without exception, must produce a ticket, an authorization record, a session recording where production access was used, retrospective approval within the defined window, and attached evidence. There is no path through this procedure that results in an undocumented change.

---

## 3. Scope

### 3.1 In Scope

- All emergency changes to production systems that process, store, or transmit customer clinical messages or PHI, including application code, interface engine configurations, message routing rules, transformation maps, infrastructure defined in Terraform, database schemas and data, network configuration, and identity or access configuration in Okta.
- All JIT and break-glass production access, whether or not associated with a change (for example, read-only diagnostic queries during an incident).
- All personnel who execute, approve, review, or observe such changes or access, including full-time employees, contractors, and vendors with production access.

### 3.2 Systems of Record

| System | Role in this procedure |
|---|---|
| **Jira Service Management (JSM)** | Change tickets, incident tickets, approval records, evidence attachment, retrospective approval workflow |
| **GitHub Enterprise** | Source control, pull requests, peer review records, protected branch enforcement |
| **Terraform Cloud** | Infrastructure changes, plan/apply records, run approvals |
| **PagerDuty** | Incident declaration, paging, escalation, on-call schedules, override records |
| **Okta** | Identity, group membership governing vault access, MFA enforcement |
| **Credential Vault** | Just-in-time production credentials with a four-hour maximum lifetime; break-glass credential issuance; session recording |
| **Logging Platform** | Immutable audit trails, session recordings, and access logs, retained 18 months |

### 3.3 Out of Scope

- Standard (non-emergency) changes, which follow SOP-ENG-010, *Standard Change Management*.
- Changes to non-production environments (development, staging, customer test environments) that contain no production PHI.
- Physical security and facilities changes (see SOP-SEC-021).
- Breach determination and regulatory notification decisions, which are governed by SOP-SEC-030, *Incident Response and Breach Assessment*; this procedure hands off to SOP-SEC-030 at the points identified in Steps 6.8.6 and 6.6.5.

---

## 4. Definitions

| Term | Definition |
|---|---|
| **Emergency change** | A change to production that must be executed before the next scheduled Change Advisory Board (CAB) review because delay would prolong a Severity 1 or Severity 2 incident, or would leave an actively exploited security vulnerability unmitigated. |
| **Severity 1 (SEV1)** | Complete loss of message delivery for one or more customers, confirmed corruption of clinical data in transit, or a confirmed active security compromise. Clinical safety impact is presumed. |
| **Severity 2 (SEV2)** | Degraded message delivery (latency exceeding contractual SLA, partial queue backlog, intermittent failures) affecting one or more customers, or a security vulnerability with a credible, imminent exploitation path. |
| **Severity 3 (SEV3)** | Degradation with no current customer-visible impact (e.g., loss of redundancy). SEV3 issues do **not** qualify for emergency changes and follow standard change management. |
| **Just-in-time (JIT) access** | Production credentials issued by the vault for a specific role and target system, valid for a maximum of four hours, tied to a named individual authenticated through Okta with MFA, and automatically revoked at expiry. |
| **Break-glass access** | JIT access issued under the incident-commander authorization path when the standing approval path is unavailable. Break-glass access is always issued to a named individual, never to a shared account. Shared break-glass credentials are prohibited (see Step 6.3.2). |
| **Two-person rule** | The requirement that every production deployment involve two authenticated individuals: one who executes and one who reviews and confirms, with both identities recorded. |
| **Retrospective approval** | Formal approval of an emergency change by a designated change approver after execution, completed within 24 hours (one business day) of the change, recorded in JSM. |
| **Change approver** | An individual on the CISO-maintained approver roster (Section 5) authorized to approve emergency changes. An approver may not approve a change they executed or peer-reviewed. |
| **Freeze window** | A period during which a customer has contractually prohibited changes affecting their interfaces (e.g., during an EHR go-live). Freeze windows are recorded in the JSM freeze calendar. |
| **PHI-touching change** | Any change or access session in which production PHI was read, written, exported, or displayed, including diagnostic queries — regardless of whether the change itself modified data. |
| **CAB** | Change Advisory Board, which meets each business day at 10:00 Mountain Time and reviews all retrospective approvals from the prior day. |

---

## 5. Responsibilities

| Role | Responsibilities under this procedure |
|---|---|
| **Director of Platform Engineering (Nadia Oyelaran)** | Owns this procedure. Maintains the CAB. Ensures on-call schedules, approver rosters, and tooling integrations remain current. Reports emergency-change metrics monthly to the CISO. |
| **Chief Information Security Officer (Ana Lucia Ferreiro)** | Approves this procedure and all revisions. Maintains the designated change approver roster in Okta group `prod-change-approvers`. Owns quarterly access recertification (Step 6.7). Adjudicates exceptions that cannot be resolved within this procedure. |
| **Incident Commander (IC)** | Declares severity. Authorizes break-glass access when the standing path is unavailable. Coordinates the incident, assigns the deployer and peer reviewer, and ensures the change ticket exists before any production change is executed. The IC is drawn from the PagerDuty `incident-commander` rotation. |
| **On-Call Site Reliability Engineer (SRE)** | First responder. Requests JIT access, executes or peer-reviews changes, ensures session recording is active, and attaches evidence to the change ticket. |
| **Designated Change Approver** | Authorizes emergency changes in real time when reachable; otherwise grants retrospective approval within 24 hours. Verifies evidence completeness before approving. Must be independent of the deployer and peer reviewer for the change in question. |
| **Peer Reviewer** | Second person under the two-person rule. Reviews the proposed change (diff, Terraform plan, or query text) before execution, observes execution, and countersigns the change ticket. |
| **Security Analyst** | Reviews all break-glass sessions and all PHI-touching access within one business day. Confirms session recordings exist and match the ticketed scope. Initiates breach risk assessment under SOP-SEC-030 when access exceeded scope. Runs the quarterly recertification mechanics. |
| **Customer Success Lead** | Delivers customer notifications for PHI-touching changes and freeze-window exceptions per Step 6.8. Maintains the customer notification contact matrix and the freeze calendar. |
| **All engineers with production eligibility** | Follow this procedure without exception. Refuse to execute any production change lacking a ticket or a second person. Report deviations to the Security Analyst within four hours of discovery. |

**Segregation of duties:** For any single emergency change, the deployer, peer reviewer, and approver must be three distinct people. The IC may serve as peer reviewer but may not deploy and may not approve.

---

## 6. Procedure

### 6.1 Severity Declaration

**6.1.1** Any employee who observes a suspected production problem pages the on-call SRE via PagerDuty service `LHI-Platform-Prod`. Do not attempt diagnosis or remediation before paging.

**6.1.2** The on-call SRE acknowledges the page within 5 minutes and performs initial triage using read-only dashboards (no production credentials required). Triage answers three questions: Is message delivery stopped, degraded, or unaffected? Which customers are affected? Is there any indication of data corruption or security compromise?

**6.1.3** If triage indicates SEV1 or SEV2 conditions per the definitions in Section 4, the SRE pages the `incident-commander` rotation in PagerDuty. The IC must acknowledge within 10 minutes; PagerDuty auto-escalates to the next IC in rotation, then to the Director of Platform Engineering, then to the CISO.

**6.1.4** The IC formally declares severity by creating an incident ticket in JSM (project `INC`) with: severity level, declaration timestamp, affected customers, symptom summary, and the IC's name. PagerDuty automatically links the incident to the JSM ticket. **Severity declaration must be recorded before any emergency change is authorized.** If the JSM incident is created from a mobile device under time pressure, the summary may be a single sentence; it must be expanded within four hours.

**6.1.5** Severity can be raised at any time by the IC. Severity may be lowered only by the IC with a ticketed justification. If severity is lowered to SEV3, emergency-change authority ends immediately and any pending remediation moves to standard change management.

**6.1.6** For a suspected security compromise (SEV1), the IC pages the Security Analyst on-call immediately at declaration, not at post-incident review.

### 6.2 Emergency Change Authorization

**6.2.1** Emergency changes are permitted only under a declared SEV1 or SEV2 incident, or for an actively exploited security vulnerability confirmed by the Security Analyst. There is no other qualifying condition. "The next CAB is inconvenient" is not an emergency.

**6.2.2** Before any change is executed, the responder creates an emergency change ticket in JSM (project `CHG`, request type "Emergency Change") linked to the incident ticket. The ticket must contain, at minimum, before execution:

- Description of the intended change and the systems affected
- Rollback plan (see Step 6.9.3 for rollback failure handling)
- Whether the change will or may touch PHI (yes / no / unknown — "unknown" is treated as yes)
- Names of the intended deployer and peer reviewer
- Affected customers

A ticket with these fields takes under five minutes to create. **No production change may be executed, under any circumstance, without a CHG ticket existing first.** This is the control that failed in the SOC 2 period ending December 31, 2025, and it admits no exception.

**6.2.3** The IC requests authorization from a designated change approver via PagerDuty service `LHI-Change-Approvers`. The approver has **15 minutes** to acknowledge.

**6.2.4** If the approver acknowledges: the approver reviews the CHG ticket, asks any clarifying questions in the ticket comments, and records approval in JSM (button "Approve — Emergency, Pre-Execution") before execution begins. Verbal or chat approval is acceptable only if the approver records it in JSM within 60 minutes; the ticket comment must note "verbal approval given at [time]."

**6.2.5** If no approver acknowledges within 15 minutes, the IC invokes the unreachable-approver path in Step 6.9.1.

**6.2.6** Authorization is scoped to the change described in the ticket. If the responders discover during execution that a materially different change is needed, they stop, update the ticket, and re-request authorization. Minor tactical adjustments within the described intent (e.g., restarting a dependent service) do not require re-authorization but must be logged in the ticket timeline.

**6.2.7** Authorization expires four hours after it is granted, matching the JIT credential lifetime. If the change is not complete within four hours, the IC re-requests authorization with a status update.

### 6.3 Just-in-Time Production Access: Request, Grant, Recording, Revocation

**6.3.1** All production access is issued by the credential vault. Standing production credentials, SSH keys held locally, and database passwords stored outside the vault are prohibited. Any such credential discovered is reported to the Security Analyst and rotated within four hours.

**6.3.2** **Shared credentials are prohibited without exception**, including for break-glass. The former shared break-glass account (`bg-prod-shared`) was disabled on April 3, 2026, following the March 2026 incident, and must not be recreated. Break-glass is a *faster authorization path* to individually issued credentials, not a different kind of credential.

**6.3.3 Request.** The engineer requests access from the vault, authenticating through Okta with MFA. The request specifies:

- The CHG or INC ticket number (the vault rejects requests without a valid open ticket)
- The target system and role (e.g., `interface-engine-admin`, `customer-db-readonly`)
- Requested duration, up to the four-hour maximum — request the shortest duration that will do the job; one hour is the default

**6.3.4 Grant.** The vault validates that: the ticket is open and linked to a SEV1/SEV2 incident or has pre-execution approval; the requester is in the appropriate Okta group; and the requested role matches the ticket's declared scope. On validation, the vault issues credentials valid for the requested duration and posts a grant record (who, what role, which ticket, issued/expiry timestamps) to the ticket and to the logging platform.

**6.3.5 Recording.** All interactive sessions (SSH, database consoles, admin UIs) must run through the vault's session gateway, which records the full session to the logging platform. **If the session gateway is unavailable, interactive production access is not permitted** — page the Director of Platform Engineering; do not connect directly. Non-interactive changes (GitHub-driven deployments, Terraform Cloud runs) are recorded by their native audit logs, which stream to the logging platform.

**6.3.6** Before running any query or command against a system containing PHI, the engineer states in the ticket timeline what they are about to do (one line is sufficient: "Querying msg_audit for Sagebrush facility 04 to identify stuck messages, last 2 hours only"). Scope every query as narrowly as possible: filter to the affected customer, facility, time window, and message type. Never `SELECT *` against a table containing PHI. Never export PHI to a local machine; if data must be preserved for analysis, copy it to the designated secure evidence bucket named in the ticket.

**6.3.7 Revocation.** Credentials expire automatically at the end of their lifetime. In addition:

- The engineer **must** relinquish credentials via the vault ("Revoke Now") as soon as the task is complete, even if time remains. Holding unused live credentials is a recorded deviation.
- The IC may revoke any credential issued under the incident at any time.
- Incident resolution in JSM triggers automatic revocation of all credentials linked to the incident.
- The Security Analyst may revoke any credential and lock the requester's vault eligibility pending review.

**6.3.8** The vault posts a revocation record (who, when, whether by expiry, self-revocation, or forced revocation) to the ticket and the logging platform. The grant record, session recording, and revocation record together constitute the access evidence required in Step 6.5.

### 6.4 Two-Person Rule for Deployment

**6.4.1** Every emergency change to production requires two authenticated individuals: a **deployer** and a **peer reviewer**. Both are named in the CHG ticket before execution. Solo deployment to production is prohibited in all circumstances, including at 03:00 — see Step 6.9.1 for how to satisfy this rule when staffing is thin, and note that the rule itself is never waived.

**6.4.2** For **code changes**: the deployer opens a pull request in GitHub Enterprise against the protected production branch. The peer reviewer reviews the diff and approves the PR. Branch protection requires one approving review and passing CI status checks; emergency changes may bypass *non-critical* checks (e.g., long-running performance suites) via the `emergency-deploy` label, which requires the peer reviewer's approval and is logged, but may never bypass the review requirement itself, secret scanning, or build success.

**6.4.3** For **infrastructure changes**: the deployer creates the run in Terraform Cloud. The peer reviewer reads the full plan output — every resource to be created, changed, or destroyed — and confirms the run in Terraform Cloud under their own identity. If the plan shows destruction of any stateful resource (database, queue, storage), the peer reviewer must explicitly confirm in the ticket that destruction is intended.

**6.4.4** For **interactive changes** (console commands, direct queries, configuration edits through admin UIs): the deployer shares their recorded session screen live with the peer reviewer (video call with screen share). The peer reviewer reads each mutating command or query *before* it is executed and says "confirmed" (or objects) aloud; the deployer notes "peer-confirmed" in the ticket timeline for each mutating action or logical group of actions. The session recording plus the ticket timeline evidences compliance.

**6.4.5** The peer reviewer's obligations: understand what the change does before confirming; verify the change matches the ticketed scope; watch for scope drift, especially additional PHI access; and stop the deployer if anything is unclear. A peer reviewer who does not understand the change must say so; the IC then finds a reviewer who does or the change waits.

**6.4.6** After execution, both the deployer and the peer reviewer countersign the CHG ticket (JSM fields "Executed by" and "Peer reviewed by," each completed by the named individual under their own login) within one hour of execution.

### 6.5 Retrospective Approval and Evidence Attachment

**6.5.1** Within **four hours** of change execution, the deployer attaches the following evidence to the CHG ticket:

- Link to the merged PR and/or Terraform Cloud run, or the session recording reference for interactive changes
- Vault grant and revocation records for all credentials used
- Before/after verification: what was checked to confirm the change worked (dashboard screenshot, query result count, message-flow confirmation)
- PHI declaration: whether PHI was touched, and if so, which customers, approximately how many records, and the narrowing filters used
- Timeline of mutating actions (may reference the ticket comment timeline)

**6.5.2** Within **24 hours** of execution, a designated change approver — who was not the deployer or peer reviewer — reviews the ticket and either:

- Grants **retrospective approval** ("Approve — Emergency, Retrospective" in JSM), confirming the change was justified, in scope, executed under the two-person rule, and fully evidenced; or
- Records a **deviation**, itemizing what is missing or out of scope. Deviations are assigned to the Security Analyst and the Director of Platform Engineering, who must close them within five business days and report them in the monthly metrics to the CISO.

**6.5.3** JSM enforces this control mechanically: an emergency CHG ticket that reaches 24 hours post-execution without retrospective approval automatically escalates via PagerDuty to the Director of Platform Engineering, and at 48 hours to the CISO. The ticket cannot be closed without either an approval or a documented deviation. There is no state in which an emergency change is closed unapproved and unexamined.

**6.5.4** The CAB reviews all retrospective approvals and deviations from the prior day at its 10:00 daily meeting, checking for pattern risk (repeated emergencies in the same component, repeated near-miss evidence gaps, the same individuals repeatedly paired).

**6.5.5** The approval record, evidence attachments, and audit-log references are retained in JSM and the logging platform for the full 18-month audit retention period and are the artifacts produced for SOC 2 examination and customer audits, including any audit invoked by Sagebrush Health Network.

### 6.6 Post-Incident Review

**6.6.1** Every SEV1 incident, every incident involving break-glass authorization, and every incident involving a PHI-touching change requires a post-incident review (PIR) within **five business days** of resolution. SEV2 incidents without break-glass or PHI access require a PIR within ten business days; the IC may consolidate related SEV2s into one review.

**6.6.2** The IC owns the PIR. Required attendees: deployer, peer reviewer, approver, Security Analyst, and — for PHI-touching or customer-notified incidents — the Customer Success Lead. The review is blameless with respect to individuals and rigorous with respect to controls.

**6.6.3** The PIR document (JSM `PIR` template, linked to the incident) records: timeline; root cause; customer impact (messages delayed/lost, duration, per customer); every access session and its scope; every emergency change and its approval status; what worked; what failed; and corrective actions with owners and due dates entered as JSM tasks.

**6.6.4** The Security Analyst independently completes the access review section: they compare each session recording against the ticketed scope and confirm every PHI access was necessary and minimal. This review is completed within **one business day** of incident resolution for break-glass sessions, ahead of the full PIR.

**6.6.5** If the Security Analyst finds access that exceeded ticketed scope, touched PHI unnecessarily, or was not recorded, they immediately open a security event under SOP-SEC-030, which governs breach risk assessment and any regulatory or customer breach notification. That determination does not wait for the PIR.

**6.6.6** Corrective actions are tracked to closure at CAB; any action open past its due date is reported to the CISO. PIR documents are retained 18 months minimum and are available to customers under audit rights.

### 6.7 Quarterly Access Recertification

**6.7.1** In the first ten business days of each calendar quarter (January, April, July, October), the Security Analyst generates from Okta and the vault: (a) all members of production-eligible groups (`prod-sre`, `prod-change-approvers`, `incident-commander`, `security-analyst`); (b) all vault roles each group can request; and (c) every credential grant in the prior quarter, with associated tickets.

**6.7.2** Each group owner (Director of Platform Engineering for engineering groups; CISO for approver and security groups) reviews their roster and, for each member, records **certify** (continued need confirmed) or **revoke** in the JSM recertification ticket. "No response" is treated as revoke: access not certified by day ten of the review is removed on day eleven.

**6.7.3** The Security Analyst samples a minimum of 10% of the quarter's credential grants (and 100% of break-glass grants) and verifies each has a valid ticket, session recording where interactive, and timely revocation. Discrepancies become findings on the recertification ticket with corrective actions.

**6.7.4** Leaver and mover checks: the recertification cross-references HR termination and transfer records against Okta; any account active past termination date or retaining access inconsistent with a new role is disabled immediately and recorded as a finding.

**6.7.5** The CISO reviews and signs the completed recertification ticket by the end of the month. The signed ticket, rosters, sample results, and findings constitute the recertification record retained for 18 months.

### 6.8 Customer Notification for PHI-Touching Changes

**6.8.1** A change or access session is PHI-touching per the definition in Section 4. The deployer's PHI declaration in Step 6.5.1 is the trigger for this section; the Security Analyst's access review (Step 6.6.4) can also trigger it if PHI access is discovered that was not declared.

**6.8.2** Within **one business day** of a confirmed PHI-touching change, the Security Analyst provides the Customer Success Lead a notification packet per affected customer: incident and change ticket numbers; date and time of access; the systems and data touched; approximate record count; the purpose; the individuals who accessed (by role, with names available on request); confirmation that sessions were recorded; and the retrospective approval status.

**6.8.3** The Customer Success Lead notifies each affected customer within the timeframe specified in that customer's Business Associate Agreement or MSA, and in no case later than **five business days** after the change, using the customer's designated security contact from the notification contact matrix. Notification is written (email to the designated contact) and offered with a follow-up call. The notification content, recipient, and timestamp are recorded on the CHG ticket.

**6.8.4** If the customer requests supporting evidence, the Customer Success Lead coordinates with the Security Analyst to provide the ticket record, approval record, and — under NDA — session recording excerpts, redacting other customers' data.

**6.8.5** Notification under this section is an operational-transparency notification, not a breach notification. It applies even when access was fully authorized and in scope.

**6.8.6** If SOP-SEC-030 breach risk assessment concludes that access constituted unauthorized acquisition, use, or disclosure of PHI, breach notification obligations under the BAA and HIPAA are handled under SOP-SEC-030, superseding the timelines in this section.

### 6.9 Exception Paths

#### 6.9.1 Unreachable Approver (e.g., 03:00 with no approver acknowledgment)

**6.9.1.1** If no designated change approver acknowledges the PagerDuty page within 15 minutes (Step 6.2.3), PagerDuty auto-escalates through the approver rotation. If no approver has acknowledged within **30 minutes total** of the first page, the IC may invoke **incident-commander authorization**.

**6.9.1.2** Under IC authorization: the IC records in the CHG ticket "IC-authorized under SOP-ENG-014 §6.9.1 — approver unreachable; pages sent [timestamps]," and authorizes the change and any needed break-glass JIT access. The vault accepts an IC-authorized ticket for credential issuance; the credential is still individually issued, MFA-bound, recorded, and four-hour-limited per Section 6.3. Nothing in this path relaxes the two-person rule, the ticket-first rule, session recording, or scoping.

**6.9.1.3** The two-person rule at 03:00: the peer reviewer may be any production-eligible engineer reachable by PagerDuty, including the IC (who may peer-review but not deploy). If genuinely no second qualified person can be reached within 30 minutes — an outcome the on-call staffing model is designed to prevent — the IC pages the Director of Platform Engineering and the CISO simultaneously; either may serve as peer reviewer remotely. A change executed with zero second persons is not permitted; the incident is instead mitigated by non-change means (traffic shedding, failover, customer notification of delay) until a second person is available.

**6.9.1.4** IC-authorized changes carry a compressed retrospective window: a designated change approver must complete retrospective approval within **12 hours** of execution (not 24), and the IC-authorization is a mandatory PIR agenda item, including why the approver rotation failed to answer. Repeated unreachable-approver events in a quarter trigger a staffing review by the Director of Platform Engineering.

#### 6.9.2 Customer-Mandated Freeze Window

**6.9.2.1** Freeze windows are recorded in the JSM freeze calendar by the Customer Success Lead when contracted. JSM flags any CHG ticket whose affected-customer list intersects an active freeze.

**6.9.2.2** During a freeze, no change affecting the frozen customer's interfaces may be executed — even an emergency change — unless **both** of the following are obtained: (a) authorization under this procedure (Step 6.2 or 6.9.1), **and** (b) the frozen customer's explicit consent, obtained by the Customer Success Lead (or, outside business hours, by the IC calling the customer's 24/7 technical contact from the notification matrix) and recorded in the ticket with the consenting person's name, title, and timestamp.

**6.9.2.3** If the emergency affects **only** the frozen customer and that customer declines consent, Larkspur does not change their interfaces; the IC documents the declination, mitigates by non-change means where possible, and the Customer Success Lead confirms the customer's acceptance of continued impact in writing.

**6.9.2.4** If the emergency affects **multiple customers** and the fix cannot be scoped to exclude the frozen customer, and the frozen customer is unreachable or declines: the CISO (or, if unreachable after 30 minutes of paging, the Director of Platform Engineering) may authorize proceeding on a documented risk decision that platform-wide clinical message delivery outweighs the freeze commitment. This decision is recorded in the ticket, the customer is notified as soon as reachable and no later than the next business morning, and the event is a mandatory PIR item and a contractual-notification item for Customer Success.

**6.9.2.5** Wherever technically possible, responders scope emergency changes to exclude frozen customers (per-customer routing, feature flags, per-tenant configuration) so that Step 6.9.2.4 is never needed. The feasibility of exclusion must be explicitly assessed and noted in the ticket before invoking 6.9.2.4.

#### 6.9.3 Rollback That Itself Fails

**6.9.3.1** Every emergency change ticket includes a rollback plan (Step 6.2.2). If a change misbehaves, the default action is to execute that rollback plan under the same two-person rule, logged in the same ticket.

**6.9.3.2** If the rollback fails or worsens the situation, the deployer and peer reviewer **stop immediately**. Do not improvise a second rollback or a "fix-forward" patch without the steps below. The most common way a bad incident becomes a catastrophic one is a rapid sequence of unreviewed corrective actions.

**6.9.3.3** The IC:

1. Raises severity to SEV1 if not already (a failed rollback means the system is in an unplanned, poorly understood state).
2. Pages the Director of Platform Engineering and the relevant subject-matter expert on-call (database, interface engine, or infrastructure, per the PagerDuty SME rotations).
3. Records the failed rollback in the ticket: what was attempted, what happened, and the system's current known state.
4. Assesses whether to **stabilize in place** (leave the system in its current degraded-but-understood state while a recovery plan is written) or attempt **staged recovery**. Stabilize-in-place is the default unless clinical message delivery is fully stopped.

**6.9.3.4** Any recovery action after a failed rollback requires: a written recovery plan in the ticket (which may be brief — numbered steps and expected outcome of each); review by the SME and the peer reviewer; fresh authorization from a change approver or, if unreachable per 6.9.1, the IC; and step-by-step execution in which each step's outcome is verified and logged before the next begins. If any recovery step produces an unexpected result, stop again and reassess — do not continue the plan on momentum.

**6.9.3.5** If the failed rollback involves possible data loss or corruption of clinical messages, the IC directs preservation before recovery: snapshot affected databases and queues to the secure evidence bucket so that no recovery action destroys the ability to reconstruct or replay messages. The Customer Success Lead is briefed immediately, because customers may need to hold or resend messages from their side.

**6.9.3.6** A failed rollback always triggers a SEV1-level PIR regardless of final severity, with explicit examination of why the rollback plan did not work and whether rollback plans in that component are testable in staging.

---

## 7. Records

| Record | System of Record | Retention | Owner |
|---|---|---|---|
| Incident tickets (INC) | Jira Service Management | 18 months minimum | Director of Platform Engineering |
| Emergency change tickets (CHG) with approvals, evidence, PHI declarations, countersignatures | Jira Service Management | 18 months minimum | Director of Platform Engineering |
| Credential grant and revocation records | Vault → Logging Platform | 18 months | CISO |
| Session recordings | Logging Platform | 18 months | CISO |
| GitHub Enterprise PR and review records | GitHub Enterprise (audit stream to Logging Platform) | 18 months | Director of Platform Engineering |
| Terraform Cloud run and confirmation records | Terraform Cloud (audit stream to Logging Platform) | 18 months | Director of Platform Engineering |
| PagerDuty pages, acknowledgments, escalations | PagerDuty (export to Logging Platform) | 18 months | Director of Platform Engineering |
| Post-incident review documents and corrective-action tasks | Jira Service Management | 18 months minimum | Incident Commander of record |
| Quarterly recertification tickets, rosters, sample results, CISO sign-off | Jira Service Management | 18 months minimum | CISO |
| Customer notification records and freeze-window consents/declinations | Jira Service Management | Life of customer contract + 18 months | Customer Success Lead |
| Deviation records and closures | Jira Service Management | 18 months minimum | Security Analyst |

Records supporting SOC 2 examination or a customer audit in progress are placed under legal hold and retained beyond the periods above until released by the CISO.

---

## 8. References

- AICPA Trust Services Criteria (2017, revised 2022), CC6 (Logical Access) and CC8 (Change Management)
- HIPAA Security Rule, 45 CFR §§164.308 (administrative safeguards), 164.312 (technical safeguards, including audit controls and access management)
- HIPAA Breach Notification Rule, 45 CFR §§164.400–414
- Larkspur SOC 2 Type II Report, period ending December 31, 2025 (exception under change management criterion)
- Sagebrush Health Network Master Services Agreement, audit and security schedule
- Customer Business Associate Agreements (notification timelines per customer)
- NIST SP 800-53 Rev. 5, control families AC (Access Control), CM (Configuration Management), IR (Incident Response), AU (Audit and Accountability)

---

## 9. Related Documents

| Document | Title |
|---|---|
| SOP-ENG-010 | Standard Change Management |
| SOP-SEC-030 | Incident Response and Breach Assessment |
| SOP-SEC-021 | Physical and Facilities Security |
| SOP-SEC-018 | Identity Lifecycle Management (Joiner / Mover / Leaver) |
| POL-SEC-001 | Information Security Policy |
| POL-SEC-004 | Access Control Policy |
| RUN-ENG-007 | On-Call Handbook and PagerDuty Rotation Guide |
| REF-CS-002 | Customer Notification Contact Matrix and Freeze Calendar Procedures |

---

## 10. Revision History

| Version | Date | Author | Approver | Summary of Changes |
|---|---|---|---|---|
| 1.0 | 2022-06-01 | J. Whitfield | M. Ito (former CISO) | Initial emergency change handling procedure. |
| 1.2 | 2023-09-12 | J. Whitfield | M. Ito | Added PagerDuty escalation timings; introduced Terraform Cloud. |
| 1.3 | 2024-03-15 | N. Oyelaran | A. L. Ferreiro | Transferred ownership; added JIT vault; shared break-glass credential documented (since prohibited). |
| 2.0 | 2026-08-24 | N. Oyelaran | A. L. Ferreiro | Full rewrite in response to SOC 2 Type II exception (period ending 2025-12-31) and March 2026 break-glass incident. Prohibited shared credentials and disabled `bg-prod-shared`; made ticket-first mandatory with vault enforcement; added mandatory session recording via gateway with no-gateway-no-access rule; formalized two-person rule for all change types including interactive sessions; added 24-hour retrospective approval with automatic escalation and mandatory evidence attachment; added quarterly access recertification with 100% break-glass sampling; added customer PHI-notification procedure; added exception paths for unreachable approver, freeze windows, and failed rollbacks; aligned retention to 18-month logging platform capability; added segregation-of-duties requirements. Issued to satisfy Sagebrush Health Network 30-day documented-controls demand. |

---

*End of SOP-ENG-014 v2.0. Questions about this procedure go to the Director of Platform Engineering. Suspected deviations go to the Security Analyst within four hours of discovery. When in doubt during an incident: create the ticket, get a second person, record the session, and scope narrowly.*

---

## Appendix A — Quick Reference: Emergency Change Checklist

*Print or pin this appendix. It is a memory aid, not a substitute for the full procedure. If this checklist and the body of the SOP ever appear to conflict, the body of the SOP governs.*

### A.1 Before Touching Production

- [ ] Incident declared in JSM (`INC` ticket) with severity SEV1 or SEV2 — Step 6.1.4
- [ ] IC acknowledged and named on the incident — Step 6.1.3
- [ ] Emergency change ticket (`CHG`) created and linked, with description, rollback plan, PHI declaration, deployer and peer reviewer named, affected customers listed — Step 6.2.2
- [ ] Approver paged; approval recorded, **or** 30 minutes elapsed with no acknowledgment and IC authorization recorded — Steps 6.2.3–6.2.5, 6.9.1
- [ ] Freeze calendar checked; if any affected customer is frozen, customer consent obtained and recorded — Step 6.9.2
- [ ] JIT credentials requested from the vault against the ticket, shortest sufficient duration, individually issued — Step 6.3.3
- [ ] Session gateway confirmed recording (interactive work only) — Step 6.3.5
- [ ] Peer reviewer present and briefed — Step 6.4.1

### A.2 During Execution

- [ ] Every mutating command or query read by the peer reviewer *before* execution; "peer-confirmed" logged — Step 6.4.4
- [ ] Every PHI query preceded by a one-line scope statement in the ticket timeline — Step 6.3.6
- [ ] PHI queries filtered to affected customer, facility, time window, and message type; no `SELECT *`; no local exports — Step 6.3.6
- [ ] Scope drift → stop, update ticket, re-authorize — Step 6.2.6
- [ ] Rollback fails → **stop**, escalate per Step 6.9.3; no improvised second attempts

### A.3 Immediately After

- [ ] Credentials self-revoked in the vault ("Revoke Now") — Step 6.3.7
- [ ] Deployer and peer reviewer countersign the CHG ticket within 1 hour — Step 6.4.6
- [ ] Evidence attached within 4 hours — Step 6.5.1

### A.4 Within One Business Day

- [ ] Retrospective approval by an independent approver within 24 hours (12 hours if IC-authorized) — Steps 6.5.2, 6.9.1.4
- [ ] Security Analyst access review complete for break-glass or PHI-touching sessions — Step 6.6.4
- [ ] Customer notification packet prepared if PHI was touched — Step 6.8.2

### A.5 Within Five Business Days

- [ ] Customer notification delivered and recorded — Step 6.8.3
- [ ] PIR held for SEV1, break-glass, or PHI-touching incidents — Step 6.6.1
- [ ] Corrective actions entered as JSM tasks with owners and due dates — Step 6.6.3

---

## Appendix B — Required Ticket Fields and JSM Enforcement

The following fields are configured as mandatory in the JSM "Emergency Change" request type. The workflow enforces the transitions listed; these enforcement points are audited quarterly by the Security Analyst as part of recertification (Step 6.7.3) to confirm no administrator has weakened them.

| Field | Required at | Enforced by |
|---|---|---|
| Linked INC ticket (SEV1/SEV2) | Ticket creation | JSM validator — creation blocked without link |
| Change description | Ticket creation | JSM mandatory field |
| Rollback plan | Ticket creation | JSM mandatory field |
| PHI declaration (yes / no / unknown) | Ticket creation | JSM mandatory field; "unknown" routes ticket to Security Analyst watch queue |
| Affected customers (multi-select from customer registry) | Ticket creation | JSM mandatory field; triggers freeze-calendar check |
| Intended deployer and peer reviewer (distinct users) | Ticket creation | JSM validator — rejects identical names |
| Pre-execution approval **or** IC-authorization note | Before "In Execution" transition | JSM workflow condition |
| Freeze-window consent record (if flagged) | Before "In Execution" transition | JSM workflow condition on freeze-flag |
| Vault grant record(s) | Auto-posted | Vault–JSM integration |
| Countersignatures (Executed by / Peer reviewed by) | Within 1 hour of "Executed" transition | JSM SLA timer; breach pages the IC |
| Evidence attachments per Step 6.5.1 | Before "Awaiting Retrospective Approval" transition | JSM workflow condition — transition blocked without attachments |
| Retrospective approval or deviation record | Before "Closed" transition | JSM workflow condition — ticket cannot close without one |
| Vault revocation record(s) | Before "Closed" transition | Vault–JSM integration; open grants block closure |
| Customer notification record (if PHI-touching) | Before "Closed" transition | JSM workflow condition on PHI flag |

**SLA timers configured in JSM:**

| Timer | Threshold | Escalation target |
|---|---|---|
| Approver acknowledgment | 15 min | Next approver in rotation (PagerDuty) |
| Approver path exhausted | 30 min | IC authorization eligible; logged |
| Countersignature | 1 hour post-execution | Incident Commander |
| Evidence attachment | 4 hours post-execution | Deployer, then Director of Platform Engineering |
| Retrospective approval | 24 hours (12 if IC-authorized) | Director of Platform Engineering |
| Retrospective approval overdue | 48 hours | CISO |
| PHI notification packet | 1 business day | Security Analyst, then CISO |
| Customer notification | Per BAA, max 5 business days | Customer Success Lead, then CISO |

---

## Appendix C — Decision Flow (Textual)

```
Suspected production problem
  └─► Page on-call SRE (PagerDuty LHI-Platform-Prod)
        └─► Triage (read-only, no credentials)
              ├─ No SEV1/SEV2 conditions ──► Standard change (SOP-ENG-010). STOP HERE.
              └─ SEV1/SEV2 conditions
                    └─► Page IC ──► IC declares severity in JSM INC ticket
                          └─► Change needed before next CAB?
                                ├─ No ──► Mitigate without change; standard change later
                                └─ Yes ──► Create CHG ticket (mandatory fields, Appendix B)
                                      └─► Any affected customer frozen?
                                            ├─ Yes ──► Obtain customer consent (6.9.2)
                                            │           ├─ Consent ──► continue
                                            │           ├─ Declined, single customer ──► do not change; document
                                            │           └─ Declined/unreachable, multi-customer,
                                            │              exclusion infeasible ──► CISO risk decision (6.9.2.4)
                                            └─ No ──► continue
                                      └─► Page change approver
                                            ├─ Ack ≤15 min ──► pre-execution approval in JSM
                                            └─ No ack at 30 min ──► IC authorization (6.9.1)
                                      └─► Request JIT credentials (vault, ticket-bound, ≤4 h)
                                      └─► Session gateway recording?
                                            ├─ Yes ──► proceed
                                            └─ No / gateway down ──► NO interactive access;
                                                                     page Director of Platform Engineering
                                      └─► Execute under two-person rule (6.4)
                                            ├─ Change succeeds ──► verify, revoke creds,
                                            │                       countersign, attach evidence
                                            ├─ Change fails ──► execute rollback plan (two-person)
                                            │     ├─ Rollback succeeds ──► verify, revoke, evidence
                                            │     └─ Rollback fails ──► STOP. Raise to SEV1.
                                            │            Page Director + SME. Preserve data.
                                            │            Written recovery plan, fresh authorization,
                                            │            step-verified execution (6.9.3)
                                            └─ Scope drift ──► stop, update ticket, re-authorize
                                      └─► Retrospective approval ≤24 h (≤12 h if IC-authorized)
                                      └─► PHI touched? ──► notification packet ≤1 business day;
                                                            customer notified per BAA, ≤5 business days
                                      └─► PIR per 6.6 ──► corrective actions tracked at CAB
```

---

## Appendix D — Approver Roster and On-Call Coverage Requirements

**D.1** The CISO maintains the `prod-change-approvers` Okta group at a minimum of **six** qualified members so that the PagerDuty `LHI-Change-Approvers` rotation provides 24×7 coverage with a primary and secondary at all times, accounting for time zones, leave, and travel. Falling below six members is reported to the CISO within one business day and remedied within thirty days.

**D.2** Approver qualification requires: at least twelve months in a senior engineering, SRE, or security role at Larkspur; completion of the training in Appendix E; and CISO sign-off recorded in JSM. Qualification lapses if the member does not act as approver (real-time or retrospective) at least once per quarter and does not complete the annual refresher; lapsed members are removed from the Okta group at recertification.

**D.3** The `incident-commander` rotation is maintained by the Director of Platform Engineering at a minimum of five qualified members under the same coverage standard. IC qualification additionally requires having served as deployer or peer reviewer on at least three ticketed emergency changes or exercises.

**D.4** PagerDuty schedule overrides (shift swaps, coverage gaps) are permitted but must be entered in PagerDuty in advance; ad-hoc "call my cell instead" arrangements outside PagerDuty are prohibited because they break the auditable escalation chain relied on by Step 6.9.1.

**D.5** Coverage metrics — approver acknowledgment times, unreachable-approver invocations, and rotation depth — are included in the monthly report to the CISO (Section 5). Two or more unreachable-approver invocations in any rolling 90-day period trigger a mandatory staffing and rotation review.

---

## Appendix E — Training, Competency, and Exercises

**E.1 Initial training.** Before being added to any production-eligible Okta group, personnel complete: (a) a guided read-through of this SOP with the Security Analyst or a delegate; (b) a hands-on walkthrough in the staging environment covering ticket creation, vault credential request and revocation, session-gateway connection, and evidence attachment; and (c) a short scenario assessment (passing score 100% on the control-critical items: ticket-first, two-person rule, recording requirement, PHI scoping). Completion is recorded in JSM.

**E.2 Annual refresher.** All production-eligible personnel complete an annual refresher covering this SOP's current version, the year's deviations and PIR lessons (anonymized), and any procedure changes. Refresher completion is a certification prerequisite at the next quarterly recertification (Step 6.7.2): uncompleted refresher = revoke.

**E.3 Break-glass exercise.** Twice per year, the Director of Platform Engineering runs an announced exercise in staging simulating a SEV1 at 03:00 with an unreachable approver, exercising Steps 6.1 through 6.5 and 6.9.1 end to end, including vault issuance, session recording, IC authorization, and compressed retrospective approval. One exercise per year additionally simulates a failed rollback (Step 6.9.3). Exercise findings are ticketed as corrective actions and reviewed at CAB.

**E.4 New-role shadowing.** A newly qualified IC or approver shadows a qualified peer for their first live emergency change or exercise before acting alone; the shadowing is noted in the relevant ticket.

---

## Appendix F — Metrics and Management Review

**F.1** The Director of Platform Engineering reports the following to the CISO monthly, and the CISO reviews trends quarterly with the executive team:

| Metric | Target | Source |
|---|---|---|
| Emergency changes with ticket created before execution | 100% — no tolerance | JSM / logging platform reconciliation |
| Emergency changes with retrospective approval inside window | 100%; any miss is a deviation | JSM |
| Break-glass sessions with complete recordings | 100% | Vault / logging platform |
| Credentials self-revoked before expiry | ≥ 80% (indicator of right-sized durations) | Vault |
| Median approver acknowledgment time | ≤ 10 minutes | PagerDuty |
| Unreachable-approver invocations | 0 per quarter target; ≥ 2 triggers Appendix D.5 review | JSM |
| PHI notifications delivered within BAA timeline | 100% | JSM |
| PIRs completed within deadline | 100% | JSM |
| Corrective actions closed by due date | ≥ 90% | JSM |
| Emergency changes as share of all changes | ≤ 5% (higher share indicates planning failures, not genuine emergencies) | JSM |

**F.2** The Security Analyst performs a monthly reconciliation between vault grant records and CHG/INC tickets. Any production credential grant that cannot be matched to a valid ticket is treated as a potential unauthorized access and escalated under SOP-SEC-030 the same day.

**F.3** These metrics, the quarterly recertification records, and the deviation log constitute the standing evidence package for the SOC 2 Type II examination and are the materials produced first in response to any customer audit request, including one invoked by Sagebrush Health Network under its audit clause. The Customer Success Lead may share the metric summary (with other customers' identifying details redacted) with any customer on request without further approval; underlying tickets and recordings require CISO approval and NDA per Step 6.8.4.

---

## Appendix G — Contact and Escalation Summary

| Need | Page | Fallback |
|---|---|---|
| Report a production problem | PagerDuty: `LHI-Platform-Prod` | Phone bridge listed in RUN-ENG-007 |
| Reach the Incident Commander | PagerDuty: `incident-commander` | Auto-escalates: next IC → Director of Platform Engineering → CISO |
| Emergency change approval | PagerDuty: `LHI-Change-Approvers` | 30-min exhaustion → IC authorization (Step 6.9.1) |
| Security Analyst on-call | PagerDuty: `LHI-Security` | CISO direct |
| Session gateway down | Director of Platform Engineering (direct page) | CISO; interactive access remains prohibited until restored |
| Customer contact during freeze or PHI event | Customer Success Lead | Customer's 24/7 technical contact per REF-CS-002 (IC may call directly out of hours) |
| Suspected deviation from this SOP | Security Analyst, within 4 hours of discovery | CISO; anonymous reporting per POL-SEC-001 §9 |

---

*Appendices A–G are part of SOP-ENG-014 v2.0 and are governed by the same review cycle, approval, and revision history as the body of the document.*
