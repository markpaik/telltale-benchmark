# Emergency Change Management and Break-Glass Production Access

## Document Control

| Field | Value |
|---|---|
| Document number | SOP-PE-014 |
| Title | Emergency Change Management and Break-Glass Production Access |
| Version | 3.0 |
| Supersedes | Version 2.2, effective 2024-06-01 |
| Effective date | 2026-08-17 |
| Owner | Nadia Oyelaran, Director, Platform Engineering |
| Approver | Ana Lucia Ferreiro, Chief Information Security Officer |
| Review cycle | Annual, and within 30 days of any SOC 2 exception, security incident of Severity 1, or material change to the systems named in Section 3 |
| Next scheduled review | 2027-08-17 |
| Classification | Internal — may be shared with customers under NDA |
| Storage location | Confluence space `PLATFORM`, page tree `Controlled Documents`; PDF of record in `s3://larkspur-doc-control/sop/` |

**Approval record**

| Role | Name | Method | Date |
|---|---|---|---|
| Author / Owner | Nadia Oyelaran | Signed in Confluence approval workflow | 2026-07-24 |
| Reviewer, Compliance | Priya Raghunathan, Manager, GRC | Signed in Confluence approval workflow | 2026-07-27 |
| Approver | Ana Lucia Ferreiro | Signed in Confluence approval workflow | 2026-07-30 |

---

## 1. Purpose

This procedure defines how Larkspur Health Interfaces declares an incident, authorizes and deploys an emergency change, grants and revokes time-limited production access, and documents both afterward so that a third party can reconstruct what happened, who approved it, and what evidence supports the approval.

It exists because three things went wrong in 2025.

First, the SOC 2 Type II report for the period ending December 31, 2025 recorded an exception under the change management criterion: of 34 emergency changes sampled, 9 had no retrospective approval recorded and 4 had no change ticket of any kind. The control as written required retrospective approval but named no deadline, no approver of record, and no artifact. A control with no deadline is a control with no evidence.

Second, in March 2026 an engineer authenticated to a production customer database using a shared break-glass credential and ran ad hoc queries. The session was not recorded. Because no session transcript existed, Larkspur could not determine which rows were returned, and the assessment had to assume the entire result set was accessed — 1,900 patient records across four hospital tenants. The event was escalated to a breach risk assessment under 45 CFR 164.402. The absence of a recording, not the access itself, is what made the assessment necessary.

Third, Sagebrush Health Network, a 14-hospital customer representing a material share of daily message volume, has issued written notice demanding documented controls within 30 days and has reserved the right to invoke the audit clause in Section 11.4 of its master services agreement.

The procedure is written so that a new site reliability engineer on their first on-call shift can execute it at three in the morning without paging anyone to ask what to do next.

---

## 2. Scope

### 2.1 In scope

This procedure applies to every change to a production system that is deployed outside the normal change window, meaning any change that has not completed the standard review path in SOP-PE-009 *Standard Change Management* before deployment begins. It applies to:

- Application code deployed to production interface engines, routing services, and transformation pipelines.
- Infrastructure changes applied through Terraform Cloud to production workspaces.
- Database schema changes, data corrections, and queue manipulations in production.
- Configuration changes to message routing, endpoint definitions, TLS material, and credential rotation in production.
- Any interactive human session against a production system, whether or not a change is made, including read-only queries.
- Feature flag changes that alter message handling behavior for one or more customer tenants.

It applies to all 320 employees and to contractors with production access, in every environment that processes, stores, or transmits customer clinical data for the 62 hospital customers.

### 2.2 Out of scope

- Standard changes deployed through the normal path. Those follow SOP-PE-009.
- Changes to non-production environments that contain no production data. Note that any environment containing a copy of production clinical data is in scope regardless of its label.
- Customer-side changes made by hospital staff within their own systems.
- Physical security and facilities incidents, which follow SOP-SEC-003.
- Personnel matters arising from an incident, which follow the HR investigation process.

### 2.3 Relationship to other procedures

An emergency change is almost always the product of an incident. Incident detection, triage, and customer communication cadence are governed by SOP-PE-011 *Incident Management*. This procedure governs the *change* made during an incident and the *access* used to make it. The two run in parallel; the incident commander owns the incident, the change approver owns the change.

---

## 3. Definitions

**Break-glass access.** Elevated production access granted outside the standing entitlement model, issued only for a declared incident, always time-limited, always session-recorded. As of Version 3.0 there are no shared break-glass credentials at Larkspur. All break-glass access is issued to a named human identity.

**Change approver, designated.** A named individual on the published emergency approver roster with authority to authorize an emergency change. The roster is maintained in Okta group `emergency-change-approvers` and published in PagerDuty schedule `Change Approver — Emergency`.

**Customer success lead.** The named Larkspur employee accountable for a given hospital customer relationship, and the only role authorized to make first contact with a customer about an incident or change affecting them.

**Emergency change.** A change to production deployed without completing the standard pre-approval path, justified by an active or imminent Severity 1 or Severity 2 condition.

**Evidence bundle.** The set of artifacts attached to the change ticket that allow an auditor to reconstruct the change without interviewing anyone. Contents are enumerated in Section 6.9.

**Incident commander (IC).** The single accountable decision-maker for a declared incident. The IC does not need to be the most senior person present and does not perform hands-on remediation.

**JIT credential.** A just-in-time production credential issued by the vault against a named Okta identity, scoped to a specific system and permission set, with a maximum lifetime of four hours.

**Peer reviewer.** An engineer other than the change author who reviews the diff and observes or co-executes the deployment. Satisfies the two-person rule.

**PHI-touching change.** A change that reads, writes, deletes, moves, transforms, or exposes protected health information, or that alters the routing or retention of messages containing PHI. When in doubt, a change is treated as PHI-touching.

**Retrospective approval.** Formal approval of an emergency change recorded *after* deployment by a designated change approver who was not the change author, within the window in Section 6.10.

**Security analyst.** A member of the security team on the `Security On-Call` PagerDuty schedule, responsible for session review, access anomaly assessment, and breach risk determination input.

**Session recording.** A complete, tamper-evident transcript of an interactive production session, including all commands issued, all output returned, timestamps, and the identity of the operator. Produced automatically by the vault's session proxy. Retained 18 months in the logging platform.

**Severity.** The classification defined in Section 5.1 that governs paging, authorization thresholds, and communication obligations.

**Two-person rule.** No emergency change reaches production through the action of a single individual. One person authors, a second reviews and observes deployment. The two must be different named humans; automation counts as neither.

### 3.1 Systems of record

| System | Purpose in this procedure | Authoritative for |
|---|---|---|
| Jira Service Management, project `ECR` | Emergency change tickets | Change record, approvals, evidence bundle |
| Jira Service Management, project `INC` | Incident tickets | Severity, timeline, IC assignment |
| GitHub Enterprise, org `larkspur` | Code changes, pull requests | Diff, peer review, merge record |
| Terraform Cloud, org `larkspur-prod` | Infrastructure changes | Plan, apply, state |
| PagerDuty | Paging, escalation, on-call rosters | Who was paged, who acknowledged, when |
| Okta | Identity, group membership, MFA | Who a person is, what they are entitled to |
| Vault (HashiCorp Vault Enterprise, cluster `vault-prod-01`) | JIT credential issuance, session proxy and recording | Access grants, session transcripts |
| Logging platform (Splunk, index `larkspur_audit`) | Audit trail aggregation, 18-month retention | Long-term evidence of record |

---

## 4. Responsibilities

**Incident commander.** Declares and, when justified, revises severity. Decides whether an emergency change is warranted. Assigns the change author and peer reviewer. Requests the designated change approver be paged. Owns the incident timeline. Decides when the incident is resolved. Schedules the post-incident review. Does not author changes, does not review diffs, and does not approve their own incident's changes.

**On-call site reliability engineer.** First responder. Performs triage. Authors emergency changes when assigned. Requests JIT access. Executes deployment with a peer reviewer present. Records the timeline contemporaneously. May act as IC for Severity 3 incidents.

**Designated change approver.** Authorizes emergency changes, in advance where time allows and retrospectively where it does not. Verifies that the two-person rule was met, that the evidence bundle is complete, and that the change scope matches the incident. Must not be the change author or the peer reviewer for the same change. Roster maintained by Nadia Oyelaran; minimum six named approvers with coverage in at least two US time zones.

**Peer reviewer.** Reviews the diff or Terraform plan before apply. Observes or co-executes the deployment. Confirms rollback exists and has been tested where testable. Attests in the change ticket. Must be an engineer with production familiarity in the affected system; the peer reviewer role cannot be filled by the change author, by a person with no context, or by the IC.

**Security analyst.** Reviews every break-glass session recording within one business day. Assesses whether access exceeded the stated scope. Provides input to breach risk determination. Owns quarterly access recertification. Escalates to the CISO on any unrecorded session, any session touching PHI outside declared scope, or any use of a credential outside its issued window.

**Customer success lead.** Sole authorized first contact with the affected customer. Determines, with the security analyst and legal, whether a change requires customer notification under Section 6.13. Maintains the per-customer notification matrix including freeze windows, contractual notification clocks, and named contacts.

**Director, Platform Engineering (Nadia Oyelaran).** Owns this procedure. Maintains the approver roster. Reviews the weekly emergency change report. Accountable for the retrospective approval rate metric.

**Chief Information Security Officer (Ana Lucia Ferreiro).** Approves this procedure. Final authority on breach risk determination, on granting the exceptions in Section 7, and on any deviation from the two-person rule.

---

## 5. Severity and Authorization Thresholds

### 5.1 Severity definitions

| Severity | Definition | Examples |
|---|---|---|
| **Sev 1** | Message delivery has stopped or is materially degraded for one or more customers; or PHI confidentiality, integrity, or availability is compromised or reasonably believed to be compromised. | Routing engine down; messages dropping silently; PHI delivered to the wrong tenant; credential compromise suspected. |
| **Sev 2** | Message delivery is degraded but continuing, with a credible path to Sev 1 if untreated; or a single customer interface is down. | Queue depth growing beyond four hours of backlog; one hospital's ADT feed down; transformation producing malformed but non-PHI-leaking output. |
| **Sev 3** | Contained defect with a workaround, no PHI exposure, no delivery impact. | Non-critical alert noise; dashboard failure; scheduled job late without downstream effect. |

Severity is declared by the first responder and may be raised by anyone. Only the IC may lower severity, and the reason must be entered in the incident timeline.

### 5.2 What each severity authorizes

| | Sev 1 | Sev 2 | Sev 3 |
|---|---|---|---|
| Emergency change permitted | Yes | Yes | No — use standard path |
| Pre-approval required before deploy | Attempt required; may proceed under Section 7.1 if unreachable | Required | N/A |
| Retrospective approval deadline | 24 hours | 24 hours | N/A |
| JIT production access permitted | Yes | Yes | Read-only only, standard entitlement |
| Two-person rule | Mandatory, no exceptions | Mandatory, no exceptions | N/A |
| Post-incident review | Mandatory | Mandatory | At IC discretion |
| Customer notification assessment | Mandatory within 2 hours | Mandatory within 8 hours | Not required |

**There is no severity level and no circumstance under which a single person may deploy an emergency change alone.** Section 7.1 provides relief from *approval* timing, never from the two-person rule.

---

## 6. Procedure

### 6.1 Detect and declare

1. On detection of a suspected production issue — by alert, customer report, or observation — the detecting person opens a Jira incident ticket in project `INC` using the `Incident` request type.
2. Populate: title, first symptom observed, time first observed (UTC), affected systems, affected customers if known, and proposed severity.
3. Trigger the PagerDuty incident from the Jira ticket using the `Create PagerDuty Incident` action. Select service `Platform — Production` and the proposed severity. This pages the on-call SRE.
4. If proposed severity is 1, also trigger PagerDuty service `Security On-Call`. Do this even if PHI involvement is uncertain.
5. The on-call SRE acknowledges in PagerDuty within 5 minutes. If unacknowledged at 5 minutes, PagerDuty escalates to the secondary. At 10 minutes it escalates to Nadia Oyelaran.

### 6.2 Assign the incident commander

6. For Sev 1, the first responder pages the `Incident Commander` PagerDuty schedule. The IC acknowledges and posts in the incident Slack channel: `IC is <name>. Severity <n>. Comms cadence <interval>.`
7. For Sev 2, the on-call SRE may act as IC, or may page the IC schedule if the incident requires parallel workstreams.
8. Slack channel `#inc-<ticket-key>` is created automatically by the Jira-Slack integration. All incident coordination happens there. Decisions made in DMs or on calls must be posted to the channel within 10 minutes with the timestamp of the decision.
9. The IC records in the Jira incident ticket, in the `Roles` field: IC name, SRE name, and — once assigned — change author, peer reviewer, and change approver.

### 6.3 Decide whether an emergency change is warranted

10. The IC answers three questions in the incident channel and records the answers in the ticket:
    - Is there a non-change mitigation (failover, traffic shift, feature flag already provisioned, customer-side workaround)? If yes, prefer it.
    - Will waiting for the standard change path materially worsen customer impact or PHI risk? If no, use the standard path.
    - Is the smallest change that resolves the immediate condition identifiable and bounded?
11. If an emergency change is warranted, the IC states in the channel: `Emergency change authorized for investigation. Author <name>. Peer reviewer <name>.` This is not approval to deploy. It is assignment.
12. The IC pages the designated change approver via PagerDuty service `Change Approver — Emergency` at this point, not later. Paging early is what makes pre-approval possible.

### 6.4 Open the emergency change ticket

13. The change author opens a ticket in Jira project `ECR`, request type `Emergency Change`. **This step occurs before any production access is requested.** The ECR key is required as an input to the vault access request in Section 6.5; the vault will reject a request with no valid ECR key. This is the control that makes the "four changes with no ticket at all" finding structurally impossible to repeat.
14. Required fields, all enforced as mandatory by the Jira screen configuration:
    - Linked incident (`INC` key)
    - Severity
    - Change author (auto-populated from reporter)
    - Peer reviewer (must be a member of Okta group `production-engineers`, and validated as ≠ author)
    - Designated change approver (must be a member of `emergency-change-approvers`, validated as ≠ author and ≠ peer reviewer)
    - Systems affected (multi-select)
    - Customer tenants affected (multi-select, or `All`, or `Unknown — pending investigation`)
    - PHI-touching (Yes / No / Unknown — defaults to Unknown)
    - Description of the change, in plain language
    - Rollback plan, in plain language, including the command or action that reverses the change
    - Blast radius if the change is wrong
15. If `PHI-touching` is `Yes` or `Unknown`, Jira automatically adds the security on-call and the customer success lead for each named tenant as watchers, and starts the notification assessment clock (Section 6.13).

### 6.5 Request just-in-time production access

16. Production access is requested through the vault UI at `https://vault.larkspur.internal/jit` or CLI `larkspur-jit request`. There is no other path. Standing production credentials do not exist for human users. Shared credentials were revoked on 2026-04-02 and the accounts deleted.
17. The requester authenticates to the vault through Okta with MFA. Okta step-up MFA is enforced for all JIT requests regardless of session age.
18. The request form requires:
    - ECR ticket key (validated live against Jira; rejected if the ticket does not exist, is closed, or names the requester as neither author nor peer reviewer)
    - Target system, selected from a catalog — free text is not accepted
    - Permission set, selected from the catalog (`read-only`, `read-write`, `schema-change`, `admin`)
    - Requested duration in 30-minute increments, maximum 4 hours
    - Justification, minimum 40 characters, which is copied into the audit record
19. Approval of the JIT grant:
    - `read-only` on a non-PHI system: auto-granted against a valid ECR key.
    - `read-only` on a PHI-bearing system: requires approval by the designated change approver or the security on-call. Approve in PagerDuty or in the vault UI. Target response 10 minutes.
    - `read-write`, `schema-change`, or `admin` on any system: requires approval by the designated change approver **and** notification to security on-call. Security may revoke after the fact but does not block issuance.
20. On grant, the vault issues a credential bound to the requester's Okta identity, scoped to the named system and permission set, expiring at the stated duration or 4 hours, whichever is shorter. The credential is not displayed as a copyable secret; it is injected into a session established through the vault session proxy.
21. **All interactive production sessions traverse the vault session proxy and are recorded.** The proxy records every keystroke, every command, and all returned output, with per-command timestamps and the operator's Okta identity. Direct network paths to production databases and hosts are blocked at the network layer from all non-proxy sources. There is no supported way to reach a production database without a recording. This is the specific control that would have prevented the March 2026 assessment: had a transcript existed, the query result set would have been known, and the scope of access would have been a fact rather than an assumption.
22. If the session proxy is unavailable, see Section 7.4. Do not route around it.
23. Session recordings stream to the logging platform, index `larkspur_audit`, sourcetype `vault:session`, and are retained 18 months. Recordings are write-once; the platform's retention lock prevents deletion or modification within the retention period, including by administrators.

### 6.6 Revoke access

24. Credentials expire automatically at the stated duration. No action is required to revoke on expiry.
25. When work completes before expiry, the holder runs `larkspur-jit revoke --ecr <key>` or clicks `End session and revoke` in the vault UI. This is expected practice, not optional courtesy. Median time-to-revoke is a reported metric.
26. Extension requires a new request with fresh approval. Extensions are not granted by amending an existing grant. A second extension on the same ECR triggers an automatic note to the IC asking whether the change scope has grown beyond the incident.
27. The security analyst reviews the vault access report daily for: sessions held to full expiry without an explicit revoke, permission sets broader than the ECR description implies, and access to tenants not named in the ECR.

### 6.7 Author and review the change

28. **Code changes.** The author opens a pull request in GitHub Enterprise against the production branch. The PR title must begin with the ECR key. Branch protection on production branches requires: one approving review from a user in team `production-engineers` who is not the author, all status checks green or explicitly overridden with a recorded reason, and a linked ECR key. The override, if used, is logged and appears in the evidence bundle.
29. **Infrastructure changes.** The author opens a Terraform Cloud run in the affected production workspace. The run is created from a VCS-backed configuration; `terraform apply` from a local workstation against production state is blocked by workspace settings. The plan output is attached to the ECR ticket before apply. The peer reviewer reads the plan and confirms in Terraform Cloud; Terraform Cloud workspace settings require manual apply with a second approver on all production workspaces.
30. **Database and data changes.** The author writes the statement, including the `WHERE` clause, into the ECR ticket before executing it. The peer reviewer reads it and confirms in the ticket. The statement is executed inside a recorded proxy session. Any `UPDATE` or `DELETE` without a `WHERE` clause requires CISO approval regardless of severity. `SELECT` statements against tables containing PHI must be scoped to the minimum necessary rows; the security analyst assesses this in review.
31. **Feature flags and configuration.** Changed through the config service with the ECR key as a required annotation. Two-person confirmation is enforced in the config service UI for production scopes.

### 6.8 Deploy under the two-person rule

32. Before deployment, the author confirms in the ECR ticket, using the checklist field:
    - Peer reviewer identified and present (name and how they are present — same call, same screen share, same terminal)
    - Rollback plan written and, where testable, tested in staging
    - Blast radius stated
    - Pre-approval obtained, or Section 7.1 invoked with the record required there
33. The peer reviewer confirms separately in the ECR ticket: `Reviewed diff/plan. Observed deployment. Rollback understood.` Jira requires this comment from the named peer reviewer account before the ticket can move to `Deployed`.
34. Deployment proceeds. The author narrates each step in the incident Slack channel as it happens. The channel is the contemporaneous timeline; do not reconstruct it later.
35. Verify the change achieved its purpose. State the verification method and result in the ECR ticket — the specific metric, query, or dashboard, with values before and after.
36. If the change did not resolve the condition or made it worse, execute rollback. If rollback fails, go to Section 7.3 immediately.

### 6.9 Assemble the evidence bundle

37. Within 4 hours of deployment, the change author attaches to the ECR ticket:

| Artifact | Source | Form |
|---|---|---|
| Diff or Terraform plan | GitHub PR link / TFC run link | Permalink, not a screenshot |
| Peer review attestation | Jira comment from reviewer account | In-ticket |
| Deployment log | CI system run, or terminal transcript | Permalink or attachment |
| Session recording reference | Vault session ID(s) | ID and Splunk permalink |
| JIT grant record | Vault | Grant ID, scope, duration, approver, revoke time |
| Verification evidence | Dashboard, query, metric | Screenshot with visible timestamp, plus the query text |
| Rollback record, if executed | As above | Same set |
| PHI determination | ECR field | Yes/No with one-line rationale |
| Customer notification decision | Section 6.13 | Decision, decider, timestamp |

38. Jira blocks transition to `Closed` until every applicable field is populated. `Not applicable` is an accepted value and requires a reason.

### 6.10 Retrospective approval

39. **Every emergency change receives a recorded approval decision from a designated change approver within 24 hours of deployment.** This is the control that failed in 9 of 34 sampled changes. It is now enforced by tooling, not by memory.
40. The approver:
    - Reads the ECR ticket and the linked incident.
    - Confirms the change scope matches the incident condition — that the change did not carry unrelated work.
    - Confirms the two-person rule was met by two distinct named humans.
    - Confirms the evidence bundle is complete per Section 6.9.
    - Confirms JIT access was scoped, recorded, and revoked.
    - Records the decision using the Jira `Retrospective Approval` transition, selecting `Approved`, `Approved with findings`, or `Not approved`.
41. `Approved with findings` requires at least one finding with an owner and a due date. `Not approved` escalates to Nadia Oyelaran and Ana Lucia Ferreiro within 1 hour and requires a written remediation plan within 3 business days.
42. Automated enforcement:
    - At deployment + 12 hours, Jira automation posts a reminder to the approver and the incident channel.
    - At + 20 hours, PagerDuty pages the approver.
    - At + 24 hours with no decision, PagerDuty pages the backup approver and notifies Nadia Oyelaran.
    - At + 48 hours, the ECR is flagged `Approval SLA breach`, the CISO is notified, and it is added to the monthly control report and the next SOC 2 evidence package as a known exception with explanation.
43. The approver may not approve a change they authored, reviewed as peer reviewer, or commanded as IC. Jira enforces the first two; the third is enforced by the approver's own declaration and audited quarterly.

### 6.11 Post-incident review

44. The IC schedules a post-incident review within 5 business days of resolution for every Sev 1 and Sev 2. Attendance is required from the IC, SRE, change author, peer reviewer, change approver, and security analyst. The customer success lead attends when a customer was affected.
45. The review is blameless in tone and specific in output. It covers: timeline, detection latency, whether severity was correct, whether the emergency path was justified over the standard path, whether access was minimum-necessary, whether the two-person rule held, whether the evidence bundle was complete on first pass, and what in the system permitted the condition.
46. Output is a Confluence page in space `POSTMORTEM`, linked from the incident ticket, containing: summary, timeline with UTC timestamps, contributing factors, what went well, and action items each with a named owner, a due date, and a Jira ticket.
47. Action items are tracked to closure by Nadia Oyelaran in the weekly platform review. Items open past due date for 30 days escalate to the CISO.

### 6.12 Quarterly access recertification

48. In the first week of each quarter, the security analyst generates from Okta and the vault:
    - All members of `production-engineers`, `emergency-change-approvers`, and `incident-commanders`
    - All JIT grants issued in the quarter, with scope, duration, approver, and revoke time
    - All sessions held to full expiry without explicit revoke
    - All permission-set escalations
49. Each group owner (Nadia Oyelaran for engineering groups, Ana Lucia Ferreiro for security groups) reviews the membership line by line and marks each member `Retain` or `Remove`, with a reason for `Retain` where the member issued no JIT grant in the prior two quarters.
50. Removals are executed in Okta within 5 business days. The completed attestation is signed and stored in `s3://larkspur-doc-control/recert/<YYYY-Qn>/`.
51. Terminations and role changes are handled at the time of the event through the Okta lifecycle integration with the HRIS, not at recertification. Recertification is a detective control, not the primary one.
52. The security analyst additionally reviews a 10% sample of session recordings each quarter — minimum 5 sessions — for scope adherence, and documents findings in the recertification package.

### 6.13 Customer notification for PHI-touching changes

53. When a change is marked `PHI-touching: Yes` or `Unknown`, the notification assessment clock starts at deployment.
54. The customer success lead, security analyst, and — where the CISO directs — legal counsel jointly determine within 2 hours (Sev 1) or 8 hours (Sev 2):
    - Which customer tenants' PHI was touched
    - Whether the change altered, exposed, deleted, or misrouted PHI
    - Whether the contractual notification threshold in the customer's MSA or BAA is met
    - Whether the HIPAA breach risk assessment under 45 CFR 164.402 is required
55. Notification defaults to `send` when the determination is genuinely uncertain. The cost of an unnecessary notification is smaller than the cost of a late one.
56. The customer success lead sends notification through the customer's contractually specified channel, using template `TMPL-CS-004`, containing: what happened, when, which of the customer's data was involved, what Larkspur did, what the customer should do, and a named contact. Larkspur's standard contractual commitment is notification without unreasonable delay and no later than 24 hours from determination; per-customer clocks in the notification matrix override the standard where shorter. Sagebrush Health Network's MSA specifies 12 hours.
57. The notification, its timestamp, and the recipient are attached to the ECR ticket.
58. If a breach risk assessment is triggered, the security analyst opens a ticket in project `SEC` and follows SOP-SEC-007. The ECR remains open until the assessment reaches a determination.

### 6.14 Reporting

59. Weekly, Jira automation delivers to Nadia Oyelaran and Ana Lucia Ferreiro: all emergency changes in the period, retrospective approval rate, median hours to approval, SLA breaches, JIT grants by permission set, sessions held to expiry, and any unrecorded session (target: zero).
60. Monthly, GRC compiles the control evidence package and files it in the SOC 2 evidence repository.
61. Quarterly, Nadia Oyelaran reports to the executive team on emergency change volume as a share of total changes. A sustained rise indicates the standard path is too slow and is treated as a process defect, not an engineering one.

---

## 7. Exception Paths

Exceptions relieve *timing*. They never relieve the two-person rule, session recording, or the requirement that a change ticket exist.

### 7.1 Approver unreachable

Applies when a designated change approver has been paged and has not acknowledged.

1. Page the primary approver via PagerDuty. Wait 10 minutes.
2. On no acknowledgment, PagerDuty escalates to the secondary approver automatically. Wait 10 minutes.
3. On no acknowledgment, page Nadia Oyelaran, then Ana Lucia Ferreiro.
4. If no approver has acknowledged 30 minutes after the first page, **and** severity is 1, **and** the IC judges that waiting worsens patient-data risk or delivery impact, the IC may authorize deployment under this exception. Sev 2 waits for an approver.
5. The IC records in the ECR ticket, using the `Emergency Approval Exception` field:
   - Times of each page attempt and each escalation, from PagerDuty
   - Names paged
   - IC's written justification for not waiting
   - IC's name — the IC is the authorizing party of record for this deployment
6. The two-person rule still applies. The IC may serve as peer reviewer only if no other qualified engineer is reachable, and that fact must be recorded with the names attempted.
7. Retrospective approval remains due within 24 hours. A designated approver reviews as normal and may record `Approved with findings` or `Not approved`; the exception does not pre-empt the finding.
8. Every use of this exception is reviewed by the CISO in the monthly control review. More than two uses in a quarter triggers a review of approver roster depth and coverage.

### 7.2 Customer-mandated freeze window

Several customers, including Sagebrush Health Network, contractually specify freeze windows — typically year-end, EHR go-live weekends, and Joint Commission survey periods — during which no change may be deployed to their tenant without prior written consent.

1. Freeze windows are recorded in the customer notification matrix and loaded into Jira as a calendar. The ECR ticket displays a red banner when any named tenant is in a freeze.
2. Inside a freeze, first ask whether the affected tenant can be isolated: route around, fail over, or hold messages in a durable queue. If the incident can be contained without touching the frozen tenant, do that and deploy after the freeze.
3. If the change must touch the frozen tenant, the customer success lead contacts the customer's designated freeze-exception contact — named in the matrix, with a 24/7 number for Sev 1 — and requests written consent. Email or a signed message in the customer's ticketing system satisfies "written."
4. Consent obtained: attach it to the ECR, deploy normally, and confirm to the customer within 1 hour of completion.
5. Consent refused: do not deploy to that tenant. The IC documents the customer's decision, the residual risk, and the containment measures in place. Escalate to Nadia Oyelaran and the account executive.
6. Contact unreachable after two attempts 15 minutes apart on Sev 1: escalate to the CISO. Only the CISO may authorize deployment into a freeze without consent, and only where continued inaction poses a greater risk to patient data or care delivery than the freeze breach. The CISO's authorization, reasoning, and time are recorded in the ECR. The customer success lead notifies the customer within 1 hour of deployment with a full account.
7. Sev 2 and Sev 3 never override a freeze. They wait.

### 7.3 Rollback fails

1. Declare or confirm Sev 1. A failed rollback is Sev 1 regardless of the original severity.
2. The IC announces in the incident channel: `Rollback failed. Freezing further changes to <system>.` No further changes to the affected system without explicit IC authorization. Uncoordinated remediation attempts are the mechanism by which a bad incident becomes a very bad one.
3. Preserve state before further action: capture logs, current configuration, database state, and queue depths. Attach to the ECR. If the next action would destroy evidence, capture first.
4. Page in parallel: the system's subject-matter expert (from the service catalog `Owner` field), the security on-call, and Nadia Oyelaran.
5. Evaluate containment options in this order:
   - Isolate the affected component and shed load to healthy capacity
   - Hold messages in the durable queue — capacity is 72 hours at peak volume; state the current headroom in the channel
   - Fail over to the secondary region
   - Restore from the most recent verified backup, accepting the stated RPO
6. Restoration from backup requires CISO approval when the restore would overwrite customer data written after the backup point. The IC states the data-loss window explicitly in the channel before requesting approval.
7. The customer success lead notifies all affected customers within 1 hour of the rollback failure with current status, expected impact, and the next update time — regardless of whether PHI is involved. Update on the stated cadence, minimum hourly, even when the update is "no change."
8. A failed rollback always triggers a post-incident review with the CISO in attendance, and the review must answer specifically why the rollback was believed to work and why it did not.

### 7.4 Session proxy unavailable

1. If the vault session proxy is unavailable, production interactive access is unavailable. This is by design.
2. Attempt proxy recovery first; the proxy is itself a production system and its outage is a Sev 1.
3. If an emergency requires production access while the proxy is down, only the CISO may authorize an unrecorded session, and only for Sev 1. Authorization requires: a second person present for the entire session as an observer, a manually maintained command log written contemporaneously by the observer, the shortest possible scope, and a written summary within 2 hours.
4. Any unrecorded session is automatically treated as a potential PHI access event and enters the breach risk assessment path in SOP-SEC-007, whether or not PHI is believed to have been touched. This is precisely the position Larkspur occupied in March 2026, and the assessment cost is the reason the procedure makes it so difficult to arrive there.

---

## 8. Records

| Record | System | Owner | Retention |
|---|---|---|---|
| Emergency change ticket and evidence bundle | Jira `ECR` | Nadia Oyelaran | 7 years |
| Incident ticket and timeline | Jira `INC` | Nadia Oyelaran | 7 years |
| Session recordings | Logging platform, `larkspur_audit` | Ana Lucia Ferreiro | 18 months |
| JIT grant records | Vault, replicated to logging platform | Ana Lucia Ferreiro | 18 months in platform; grant metadata 7 years in Jira |
| Pull requests and merge records | GitHub Enterprise | Nadia Oyelaran | Life of repository |
| Terraform plans, applies, state versions | Terraform Cloud | Nadia Oyelaran | 7 years |
| Paging and escalation records | PagerDuty | Nadia Oyelaran | 3 years |
| Post-incident reviews | Confluence `POSTMORTEM` | Nadia Oyelaran | 7 years |
| Quarterly recertification attestations | S3 doc-control bucket | Ana Lucia Ferreiro | 7 years |
| Customer notifications | Jira `ECR` + CRM | Customer success lead | 7 years |
| Exception authorizations (Section 7) | Jira `ECR`, CISO decision log | Ana Lucia Ferreiro | 7 years |

Session recordings are the shortest-retained record at 18 months, matching platform capability. Where a session is material to an open breach risk assessment, litigation hold, or audit, the security analyst places a retention hold before month 17. A calendar reminder at month 16 prompts review of any session linked to an open `SEC` ticket.

---

## 9. References

- AICPA Trust Services Criteria, CC6.1, CC6.2, CC6.3, CC7.2, CC8.1
- 45 CFR Part 164, Subparts C and E (HIPAA Security Rule and Privacy Rule)
- 45 CFR 164.402, definition of breach; 45 CFR 164.404–410, notification requirements
- NIST SP 800-53 Rev. 5: AC-2, AC-6, AU-2, AU-12, CM-3, CM-5, IR-4, IR-8
- HITRUST CSF v11, control 01.v, 09.b, 10.k
- Master Services Agreement, Sagebrush Health Network, Sections 8 (Security), 9 (Notification), 11.4 (Audit)
- Larkspur Business Associate Agreement, standard form v4

---

## 10. Related Documents

| Number | Title |
|---|---|
| SOP-PE-009 | Standard Change Management |
| SOP-PE-011 | Incident Management |
| SOP-PE-016 | Production Access Entitlement and Provisioning |
| SOP-SEC-003 | Physical and Environmental Security |
| SOP-SEC-007 | Breach Risk Assessment and Notification |
| SOP-SEC-012 | Logging, Monitoring, and Audit Trail Integrity |
| SOP-CS-002 | Customer Communication During Service Events |
| TMPL-CS-004 | Customer Incident Notification Template |
| REG-CS-001 | Customer Notification Matrix (freeze windows, clocks, contacts) |
| REG-PE-003 | Emergency Change Approver Roster |

---

## 11. Revision History

| Version | Date | Author | Approver | Summary |
|---|---|---|---|---|
| 1.0 | 2022-03-14 | N. Oyelaran | prior CISO | Initial issue. Emergency change defined; approval required "as soon as practical." |
| 1.1 | 2022-11-02 | N. Oyelaran | prior CISO | Added Terraform Cloud. Minor edits. |
| 2.0 | 2023-09-18 | N. Oyelaran | A. L. Ferreiro | Added severity matrix and post-incident review. Break-glass credential documented as shared account. |
| 2.1 | 2024-02-27 | P. Raghunathan | A. L. Ferreiro | Added quarterly recertification following internal audit finding IA-2024-07. |
| 2.2 | 2024-06-01 | N. Oyelaran | A. L. Ferreiro | Added PagerDuty escalation policy references. |
| **3.0** | **2026-08-17** | **N. Oyelaran** | **A. L. Ferreiro** | **Major revision responding to SOC 2 exception (period ending 2025-12-31) and the March 2026 unrecorded session event. Changes: (1) 24-hour retrospective approval deadline with named approver, automated reminder, paging, and SLA-breach escalation, replacing "as soon as practical"; (2) ECR ticket made a technical precondition of JIT credential issuance, making changes without tickets structurally impossible; (3) shared break-glass credentials eliminated, accounts deleted 2026-04-02, replaced by vault-issued JIT credentials bound to named Okta identities with 4-hour maximum lifetime; (4) mandatory session recording through vault session proxy with direct production paths blocked at the network layer; (5) two-person rule made explicit and technically enforced in Jira, GitHub branch protection, and Terraform Cloud; (6) evidence bundle defined and enforced as a close condition; (7) exception paths added for unreachable approver, customer freeze window, failed rollback, and proxy unavailability; (8) customer notification section expanded with per-customer clocks; (9) recertification expanded to include session sampling.** |

---

*End of SOP-PE-014 v3.0.*
