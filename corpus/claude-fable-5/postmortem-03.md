# Incident Postmortem: Compass Control Plane Degradation

**Incident ID:** INC-2027-0309
**Date of Incident:** Tuesday, March 9, 2027
**Duration of Customer Impact:** 4 hours, 52 minutes (14:19 – 19:11 EST)
**Severity:** SEV-1
**Document Status:** Final
**Document Owner:** Priyanka Deshmukh, Staff Site Reliability Engineer
**Reviewed By:** Oliver Baptiste, VP of Engineering; Sofia Grigoryan, Database Platform Lead; Jun-ho Park, Director of Customer Reliability
**Published:** March 19, 2027

---

## 1. Executive Summary

On Tuesday, March 9, 2027, Meridian Stack experienced a severe, extended degradation of its control plane API. The proximate trigger was a schema migration deployed at 2:14 p.m. EST that added a defaulted column to a 400-million-row table in Compass, the PostgreSQL cluster backing our control plane. On the major version of PostgreSQL that Compass still runs — an upgrade deferred for three consecutive quarters in favor of revenue-facing work — this operation required a full table rewrite under an ACCESS EXCLUSIVE lock. Every control plane query touching that table queued behind the lock. API error rates crossed 5 percent within five minutes and reached 71 percent within twenty-seven.

The incident that followed was longer and more damaging than the trigger alone would explain. Four distinct failures compounded it:

1. **A 47-minute detection gap.** The error-rate alert that should have paged within minutes was configured with a 30-minute evaluation window, and a deploy-freeze calendar entry had suppressed the faster-firing variant. A secondary signal — replication lag — fired correctly but routed to a Slack channel that had been archived in January. The first human was paged at 3:01 p.m., 47 minutes after impact began.

2. **A 38-minute misdiagnosis.** Because query timeouts clustered visibly in one availability zone, the incident commander reasonably but incorrectly attributed the degradation to a provider network event. The team pursued that hypothesis for 38 minutes before the database lock was identified at 3:52 p.m.

3. **A remediation step that made things worse.** After the migration was killed, the team restarted the entire control plane fleet simultaneously at 4:05 p.m. Nine hundred instances reconnected at once, exhausting the metadata store's connection pool and creating a secondary outage that added 71 minutes to recovery.

4. **A 52-minute external communication lag.** The status page remained green until 3:53 p.m. — 52 minutes after the first page and 94 minutes after customer impact began. Customers experiencing hard failures had no acknowledgment from us for more than an hour and a half.

The degradation affected 2,140 customers, failed 11.4 million API requests, generated $410,000 in service credits, and contributed to the cancellation of four accounts representing $290,000 in annual recurring revenue within the following month.

This postmortem is blameless. Every individual named in this document acted reasonably given the information, tooling, and processes available to them at the time. The migration author followed a checklist whose lock-duration question was optional. The incident commander followed the strongest available signal. The engineer who initiated the fleet restart executed a standard remediation whose failure mode our runbooks did not document. The failures described here belong to our systems, our processes, and our prioritization decisions — and those are what the action items in Section 8 address.

---

## 2. Impact

### 2.1 Customer Impact

| Metric | Value |
|---|---|
| Customers affected | 2,140 of 6,800 (31.5%) |
| Total failed API requests | 11.4 million |
| Peak control plane error rate | 71% (2:41 p.m.) |
| Duration of degradation | 4 hours, 52 minutes |
| Time above 5% error rate | 4 hours, 12 minutes |
| Time above 50% error rate | 2 hours, 38 minutes |

Affected customers were unable to reliably provision, resize, or reconfigure databases and message queues; rotate credentials; modify access control lists; or retrieve operational metadata through the API or console. Data plane traffic — queries against customer databases and message delivery through customer queues — was **not** directly affected, with one exception: 63 customers whose applications perform control plane lookups on a hot path (for example, resolving connection endpoints at startup) experienced data plane disruption when instances restarted or scaled during the window.

### 2.2 Business Impact

| Metric | Value |
|---|---|
| Service credits issued | $410,000 |
| Confirmed churn attributed to incident | 4 accounts, $290,000 ARR |
| Support tickets opened during incident | 1,847 |
| Support tickets in the 72 hours following | 3,100 |
| Enterprise escalations requiring executive follow-up | 22 |

### 2.3 Internal Impact

Approximately 60 engineers, support staff, and leaders were engaged during the response. Support ticket backlog returned to normal levels on March 13, four days after the incident. Two planned feature releases were delayed one sprint to accommodate immediate remediation work.

---

## 3. Background

### 3.1 The Compass Cluster

Compass is the PostgreSQL cluster that serves as the system of record for Meridian Stack's control plane. It stores customer resource definitions, provisioning state, credentials metadata, access control policies, and billing meters. Nearly every control plane API call reads from or writes to Compass. The table involved in this incident — `resource_events`, an append-heavy audit and state-transition table — held approximately 400 million rows at the time of the incident and is joined by several hot read paths.

### 3.2 The Deferred Upgrade

Compass runs a PostgreSQL major version that is two releases behind current. A major-version upgrade was scheduled for Q2 2026 and deferred three consecutive quarters — in Q2 and Q3 2026 to staff the enterprise single-sign-on initiative, and in Q4 2026 to support the usage-based billing launch. Each deferral was individually defensible; each was made in a planning forum where the operational risk carried by the delay was represented qualitatively ("aging infrastructure") rather than in terms of specific missing capabilities.

The deferral matters because the PostgreSQL version Compass runs performs `ALTER TABLE ... ADD COLUMN ... DEFAULT ...` with a non-volatile default as a **full table rewrite under an ACCESS EXCLUSIVE lock**. In the versions released since — including the version Compass was scheduled to move to in Q2 2026 — the same statement is a metadata-only change that completes in milliseconds regardless of table size. The migration that triggered this incident would have been harmless on the current version. Several engineers, including the migration's author, believed Compass had already been upgraded and that the fast-path behavior applied.

### 3.3 The Migration Checklist

Schema changes to Compass go through a pre-merge migration checklist. The checklist includes a question — "Estimated lock type and maximum lock duration?" — that was made **optional** in a November 2026 revision intended to reduce friction for small migrations. In the 14 weeks between that revision and this incident, the question was answered on 31 percent of migrations. It was left blank on the migration that triggered this incident.

### 3.4 Alerting Configuration at Time of Incident

Three monitoring facts are essential context:

- The **control plane error-rate alert** existed in two variants: a fast alert (5-minute window, pages immediately) and a slow alert (30-minute window, intended as a backstop). A deploy freeze scheduled for the week of March 8 included a calendar-driven suppression rule that silenced the fast variant to reduce pager noise during the freeze. The freeze itself had been lifted on March 8, but the suppression calendar entry ran through March 12 and was not updated.
- The **Compass replication-lag alert**, which would have fired within minutes of the lock being taken, routed exclusively to the Slack channel `#db-platform-alerts`, which was archived on January 21, 2027 during a channel consolidation. Alerts delivered to archived channels are silently dropped.
- The **Compass failover runbook**, last substantively revised in mid-2024, referenced a cluster-management command that was removed from our tooling in 2025. This did not extend the incident directly — failover was briefly considered and rejected at 3:58 p.m. — but it consumed several minutes of confusion and is symptomatic of a broader runbook staleness problem.

---

## 4. Timeline

All times are Eastern Standard Time, Tuesday, March 9, 2027. Key phase boundaries are marked in bold.

| Time | Event |
|---|---|
| **2:14 p.m.** | **Impact begins.** Scheduled migration `20270309-add-retention-class` deploys to Compass. The statement adds a defaulted column to the 400-million-row `resource_events` table, acquiring an ACCESS EXCLUSIVE lock and beginning a full table rewrite. |
| 2:15 p.m. | Queries against `resource_events` begin queueing behind the lock. Connection pool utilization on Compass begins climbing. |
| 2:19 p.m. | Control plane API error rate crosses 5%. The fast error-rate alert evaluates true but is suppressed by the deploy-freeze calendar entry. |
| 2:21 p.m. | Compass replication-lag alert fires and delivers to the archived `#db-platform-alerts` Slack channel. No human sees it. |
| 2:28 p.m. | First customer support tickets referencing API timeouts arrive. Volume is initially within normal noise thresholds; no support-side escalation trigger fires. |
| 2:41 p.m. | Control plane API error rate peaks at 71%. Requests not touching `resource_events` continue to succeed, which keeps the aggregate rate below 100% and contributes to the later misdiagnosis. |
| 2:49 p.m. | Support ticket volume crosses the internal "unusual volume" threshold. Support tooling flags this in a dashboard but does not page. |
| **3:01 p.m.** | **First page fires.** The slow (30-minute window) error-rate alert pages the on-call SRE. Detection gap: 47 minutes. |
| 3:04 p.m. | On-call SRE acknowledges, begins triage, and requests incident command. |
| 3:06 p.m. | Priyanka Deshmukh (Staff SRE) assumes incident command. SEV-2 declared; incident channel opened. |
| 3:09 p.m. | Initial triage shows request timeouts heavily clustered in availability zone `us-east-1b`, where the Compass primary and the largest share of control plane instances reside. |
| 3:11 p.m. | Working hypothesis established: provider network degradation in `us-east-1b`. Team begins checking provider status pages, network path metrics, and cross-AZ latency probes. |
| 3:14 p.m. | Provider status page shows no reported issues. Team opens a provider support case and continues investigating, treating the clean status page as inconclusive (a reasonable position given past provider under-reporting). |
| 3:22 p.m. | Incident upgraded to SEV-1 based on error rate and ticket volume. Malik Tarrant begins running support triage; a canned holding response is prepared for tickets but the **public status page remains green**. |
| 3:29 p.m. | Cross-AZ latency probes return normal. Hypothesis persists because timeout clustering in `us-east-1b` remains the strongest visible signal. Team begins planning traffic shift away from `us-east-1b`. |
| 3:41 p.m. | An engineer notes that data plane services in `us-east-1b` are healthy, which is inconsistent with a zone-wide network event. Database-layer investigation begins in parallel. |
| **3:52 p.m.** | **Root cause identified.** Sofia Grigoryan (Database Platform Lead), pulled into the incident at 3:44, queries `pg_locks` and `pg_stat_activity` on Compass and finds the migration holding an ACCESS EXCLUSIVE lock on `resource_events` with several thousand queries queued behind it. Misdiagnosis duration: 38 minutes. |
| 3:53 p.m. | Jun-ho Park (Director of Customer Reliability) posts the first public status page update — 52 minutes after the first page, 99 minutes after impact began. |
| 3:56 p.m. | Team confirms the migration is a table rewrite that would require an estimated 2+ additional hours to complete. Decision made to terminate it. |
| 3:58 p.m. | Failover to the Compass replica is briefly considered; the failover runbook references a command removed in 2025, and the replica is significantly lagged due to the rewrite. Failover rejected in favor of killing the migration in place. |
| 4:02 p.m. | Migration backend terminated via `pg_terminate_backend`. PostgreSQL begins rolling back the partial rewrite. Lock released at 4:04 p.m. |
| **4:05 p.m.** | **Fleet restart initiated.** Because control plane instances hold poisoned connection pools full of timed-out and stale connections, the team initiates a fleet-wide restart to force clean reconnection. All 900 instances restart within a ~90-second window. |
| 4:07 p.m. | The reconnection storm exhausts the metadata store's connection pool (PgBouncer front-end limit and PostgreSQL `max_connections`). Instances that fail to obtain connections crash-loop and retry with insufficient jitter, sustaining the storm. **Secondary outage begins**; error rates, which had briefly dipped, return above 60%. |
| 4:12 p.m. | Team identifies connection pool exhaustion as the new bottleneck. |
| 4:20 p.m. | Oliver Baptiste (VP of Engineering) joins the incident as executive sponsor; takes ownership of enterprise customer communication and shields the response team from status inquiries. |
| 4:24 p.m. | Second status page update posted with a substantive explanation and ETA. Updates now cadenced at ~20-minute intervals. |
| 4:31 p.m. | Decision made to stop the crash-looping fleet and perform a controlled, batched restart: instances brought up in cohorts of 50 with health-check gating between cohorts. |
| 4:44 p.m. | Batched restart begins. First cohorts connect cleanly. |
| 5:16 p.m. | Fifty percent of the fleet healthy; error rate falls below 40%. |
| 5:52 p.m. | Full fleet healthy; connection pools stable. Error rate below 10%. Secondary outage duration attributable to the simultaneous restart: 71 minutes beyond projected recovery. |
| 6:03 p.m. | Error rate below 5%. Team begins working through the backlog of queued asynchronous provisioning jobs that accumulated during the incident. |
| 6:47 p.m. | Provisioning job backlog cleared; job latencies return to baseline. |
| **7:11 p.m.** | **Impact ends.** All control plane metrics at baseline for 30 consecutive minutes. Incident downgraded; monitoring period begins. |
| 8:30 p.m. | Status page updated to Resolved with a summary and commitment to a public postmortem. Incident formally closed at 9:00 p.m. |
| Mar 10, 10:00 a.m. | Internal postmortem process initiated; migration deploys to Compass frozen pending checklist remediation. |

---

## 5. Root Cause

### 5.1 Proximate Cause

Migration `20270309-add-retention-class` executed `ALTER TABLE resource_events ADD COLUMN retention_class text DEFAULT 'standard'` against a 400-million-row table on a PostgreSQL major version that implements this operation as a full table rewrite under an ACCESS EXCLUSIVE lock. The lock blocked all reads and writes against `resource_events` — a table on the hot path of most control plane API requests — for the duration the migration ran. Queries queued behind the lock until they timed out, consuming connection pool slots and worker threads across the control plane fleet and driving the API error rate to 71 percent.

### 5.2 Why the Migration Shipped

The migration was written, reviewed, and approved through our standard process. Three factors allowed it through:

- **The checklist's lock-duration question was optional.** The November 2026 checklist revision made the "estimated lock type and maximum duration" field non-mandatory. On the version of PostgreSQL the author believed Compass ran, the honest answer would have been "metadata-only, milliseconds" — and the question being skipped meant no one was forced to verify which version Compass actually ran.
- **Version drift between belief and reality.** The Compass upgrade had been on the roadmap so long that several engineers, including the author and one reviewer, believed it had already happened. Our staging environment for control plane services runs a newer PostgreSQL version than Compass production does, so the migration completed instantly in staging, reinforcing the false belief.
- **No automated gate.** We have no CI check that estimates lock behavior of a migration against the production engine version or flags DDL against tables above a size threshold. The only defense was the human checklist, and its relevant question was optional.

### 5.3 Root Cause Statement

The root cause of this incident is **a systemic gap between our schema-change process and the actual behavior of our production database engine**, created by the intersection of (a) a three-quarter deferral of the Compass major-version upgrade, (b) a staging environment that did not match production's engine version, and (c) a migration safety checklist whose critical control was optional and unenforced. The extended duration and severity of the incident were caused by four additional, independent failures — in detection, diagnosis, remediation, and communication — detailed as contributing factors below.

---

## 6. Contributing Factors

### 6.1 Detection: The 47-Minute Gap

Impact began at 2:14 p.m.; the first page fired at 3:01 p.m. Three independent detection mechanisms all failed:

- **The fast error-rate alert was suppressed by a stale calendar entry.** The deploy-freeze suppression window (March 5–12) outlived the freeze itself (lifted March 8). Suppression rules at Meridian Stack are created manually, have no linkage to the freeze they support, and expire silently. No one owns reviewing active suppressions, and nothing surfaces "an alert evaluated true but was suppressed" to a human.
- **The replication-lag alert routed to an archived Slack channel.** The `#db-platform-alerts` channel was archived on January 21 during a workspace cleanup. Our alerting system reports successful delivery to archived channels; the message is simply invisible. No inventory maps alert routes to live destinations, and no synthetic test verifies end-to-end alert delivery.
- **Support signals had no path to paging.** Ticket volume crossed the "unusual" threshold at 2:49 p.m. — twelve minutes before the first page — but the support-side anomaly signal surfaces only on a dashboard. Customers knew we were down before our on-call engineers did.

The alert that eventually fired was the 30-minute-window backstop, functioning exactly as designed. The design assumed the fast alert would always fire first.

### 6.2 Diagnosis: The 38-Minute Provider Hypothesis

From 3:11 to 3:49 p.m., the response focused on a suspected provider network event in `us-east-1b`. This hypothesis was reasonable — the Compass primary and the plurality of control plane instances live in that zone, so timeout telemetry genuinely clustered there — but it was wrong, and several factors kept the team on it too long:

- **Topology-induced signal bias.** Our dashboards aggregate errors by availability zone prominently but do not aggregate by database table, lock wait state, or query fingerprint. A database-level view would have shown the lock immediately; the zone-level view showed a pattern that mimicked a network event.
- **No database expertise in the first 38 minutes.** The initial responder group was SRE and platform engineers. The database platform team was not paged until 3:44 p.m. Our incident process has no trigger of the form "if Compass metrics are anomalous, page database platform," even though nearly every control plane incident involves Compass.
- **No structured hypothesis checkpoint.** The incident process has no prompt to explicitly revisit the working theory when disconfirming evidence arrives. Normal cross-AZ latency probes at 3:29 p.m. were disconfirming; the pivot did not begin until 3:41 p.m., when the healthy-data-plane observation made the hypothesis untenable.
- **Diagnostic access friction.** The first responders lacked ready credentials for direct diagnostic queries against Compass. When Sofia Grigoryan joined with appropriate access and PostgreSQL fluency, root cause was found in eight minutes. The information was always one query away; the responders who were present could not run it.

### 6.3 Remediation: The Restart That Made Things Worse

Killing the migration at 4:02 p.m. was correct. The subsequent decision to restart all 900 control plane instances simultaneously turned a recovering incident into a second one:

- **The thundering herd was foreseeable but undocumented.** Nine hundred instances reconnecting within 90 seconds exceeded the metadata store's connection capacity by roughly a factor of six. Our fleet-restart tooling defaults to "all at once" and offers batching only via manual flags. No runbook documented safe restart procedure after a database-side event, and no capacity math for reconnection storms existed anywhere.
- **Client retry behavior amplified the problem.** Control plane instances that failed to obtain a connection at startup crash-looped with fixed short backoff and minimal jitter, sustaining the storm rather than letting it drain. Exponential backoff with jitter on startup connection acquisition would have allowed partial self-recovery.
- **The connection pooler had no protective admission control.** PgBouncer was configured with limits tuned for steady state, not for cold-start surges, and had no queueing headroom to absorb the herd.
- **The failover runbook was stale.** Though failover was correctly rejected at 3:58 p.m., the runbook's reference to a command removed in 2025 cost minutes and — more importantly — demonstrated that our database emergency documentation could not be trusted under pressure. Runbooks have no review cadence and no validation against current tooling.

The batched restart improvised at 4:31 p.m. (cohorts of 50, health-gated) worked cleanly and is now the documented default.

### 6.4 Communication: The 52-Minute Silence

The first public status update posted at 3:53 p.m. — 52 minutes after the first page and 99 minutes after customers began experiencing failures:

- **Status page updates required Director-level approval.** Under the process in force, only the Director of Customer Reliability or above could authorize a public incident posting. Jun-ho Park was in meetings when the incident began and joined at 3:47 p.m.; no delegate was designated and no on-call rotation existed for communications authority.
- **The uncertainty of the misdiagnosis period froze communication.** Because the team believed the cause was a provider event, there was hesitance to post anything that might need retraction. The correct move — a cause-neutral "we are investigating elevated control plane errors" — was available at 3:10 p.m. and required no diagnosis at all, but our templates and process did not make that path obvious or pre-authorized.
- **Support bore the cost.** Between 2:28 and 3:53 p.m., support agents handled hundreds of tickets with no official acknowledgment to point to, improvising individual responses. This inflated ticket handling time and produced inconsistent messaging that several enterprise customers later cited in escalations.

### 6.5 Organizational: The Deferred Upgrade and Accumulated Staleness

Beneath the four operational failures sits a pattern: **operational debt was consistently deprioritized because its cost was invisible until it wasn't.**

- The Compass upgrade was deferred three quarters with the risk described qualitatively, never as "specific dangerous DDL behaviors persist on our current version."
- The archived alert channel, the stale suppression rule, the outdated runbook, and the optional checklist question are four instances of the same failure mode: safety mechanisms that decayed silently because nothing tested them and no one owned them. Each had been broken for weeks or months before March 9. The incident did not create these gaps; it revealed them simultaneously.
- The staging/production PostgreSQL version mismatch converted staging from a safety net into a source of false confidence.

---

## 7. What Worked and What Did Not

### 7.1 What Worked

- **The 30-minute backstop alert fired.** The last line of detection defense worked as designed. Without it, discovery would have depended entirely on support escalation.
- **Time to root cause once the right expertise arrived.** Sofia Grigoryan identified the lock within eight minutes of joining. The diagnostic path was fast; the failure was in reaching it late.
- **Decisive migration termination.** The kill decision was made and executed in six minutes with clear ownership, including the correct judgment to reject a risky failover with a lagged replica and an untrusted runbook.
- **The improvised batched restart.** Once the reconnection storm was understood, the cohort-based recovery designed under pressure at 4:31 p.m. executed cleanly and completed the fleet recovery without further regression.
- **Support triage under Malik Tarrant.** Despite having no official communication to reference for 85 minutes, support maintained triage discipline, tagged tickets to the incident for later credit processing, and produced the affected-customer list used for follow-up within hours of resolution.
- **Executive engagement model.** Oliver Baptiste joined as sponsor, took enterprise communication and stakeholder management off the response team's plate, and did not redirect the technical response. This is the pattern we want.
- **Communication cadence after 4:24 p.m.** Once updates began, the ~20-minute cadence with substantive content was maintained through resolution and was positively noted in customer follow-ups.

### 7.2 What Did Not Work

- **Every automated detection path except the backstop.** Fast alert suppressed by a stale calendar rule; lag alert delivered to an archived channel; support anomaly signal unable to page. Three independent mechanisms, all silently broken.
- **Zone-first observability.** Dashboards steered diagnosis toward infrastructure and away from the database. We lacked a first-class view of lock waits and blocked query counts on Compass.
- **Escalation to domain expertise.** No trigger existed to pull the database platform team into a control-plane incident, and the responders present lacked diagnostic access to Compass.
- **Hypothesis management.** Disconfirming evidence at 3:29 p.m. did not force a re-evaluation; the pivot took a further 12 minutes.
- **Restart tooling defaults.** All-at-once fleet restart as the default, combined with poorly jittered client retry behavior, converted recovery into a second outage.
- **Runbook and checklist hygiene.** A failover runbook citing a removed command; a migration checklist with its critical question optional; no review cadence or validation for either.
- **Public communication authority.** Approval bottlenecked on a single role with no delegate, and no pre-approved cause-neutral template existed to make early posting the easy path.
- **Risk representation in planning.** Three upgrade deferrals passed through planning without the specific technical risk being stated in terms leadership could weigh against revenue work.

---

## 8. Action Items

Owners are accountable for delivery; due dates were committed in the postmortem review on March 17, 2027. Status is tracked in the engineering program review; items P0-1 through P0-6 block the lifting of the Compass migration freeze imposed March 10.

### 8.1 Prevent Recurrence of the Trigger

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P0-1 | Schedule and execute the Compass PostgreSQL major-version upgrade. Milestone plan approved by March 27; upgrade complete by end of Q2. This item cannot be deferred without CEO-level sign-off. | Sofia Grigoryan | June 30, 2027 | P0 |
| P0-2 | Make the lock-type and lock-duration question **mandatory** on the migration checklist, with merge blocked until answered. Interim manual enforcement live immediately; tooling-enforced by due date. | Sofia Grigoryan | March 26, 2027 | P0 |
| P0-3 | Add an automated CI gate that analyzes migration DDL against the **production** engine version and table-size metadata, and blocks (pending explicit senior DBA override) any operation projected to hold an exclusive lock longer than 5 seconds on a table over 10 million rows. | Devika Rao (Database Platform) | April 23, 2027 | P0 |
| P1-1 | Align staging database engine versions with production for Compass and all other stateful control plane stores; add a drift check to the weekly platform report. | Devika Rao (Database Platform) | April 9, 2027 | P1 |
| P1-2 | Establish a standing pattern library for online schema changes on large tables (batched backfills, add-column-then-default, `NOT VALID` constraints) and require its use for tables over the P0-3 threshold. | Sofia Grigoryan | May 7, 2027 | P1 |

### 8.2 Close the Detection Gap

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P0-4 | Audit **all** alert routes end-to-end; remove or re-route every alert targeting archived channels, departed users, or dead integrations. Deliver a signed-off inventory. | Priyanka Deshmukh | March 26, 2027 | P0 |
| P0-5 | Implement synthetic alert delivery tests: a canary alert per critical route, weekly, that pages the owning team if delivery fails. | Tomasz Lindqvist (Observability) | April 16, 2027 | P0 |
| P1-3 | Rebuild alert suppression: suppressions require an expiry not exceeding the linked freeze window, auto-expire when the freeze is lifted, and appear on a daily "active suppressions" digest to on-call. Suppressed-but-true evaluations are logged and surfaced in a weekly review. | Tomasz Lindqvist (Observability) | April 30, 2027 | P1 |
| P1-4 | Give the support anomaly signal a paging path: sustained abnormal ticket volume referencing platform errors pages the SRE on-call directly. | Malik Tarrant | April 16, 2027 | P1 |
| P1-5 | Add a low-threshold (10-minute window) control plane error-rate alert that **cannot be suppressed** by deploy-freeze rules — freezes suppress deploy-noise alerts only, never top-level customer-impact SLO alerts. | Priyanka Deshmukh | April 9, 2027 | P1 |

### 8.3 Improve Diagnosis Speed

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P1-6 | Build a first-class Compass health dashboard: lock waits, blocked query counts, top blocking PIDs, connection pool saturation, replication lag — linked from the top of the control plane incident dashboard. | Tomasz Lindqvist (Observability) | April 23, 2027 | P1 |
| P1-7 | Add an automatic escalation rule: any SEV-2+ control plane incident pages the database platform on-call within 10 minutes of declaration. | Priyanka Deshmukh | April 2, 2027 | P1 |
| P1-8 | Grant SRE on-call responders break-glass read-only diagnostic access to Compass (`pg_locks`, `pg_stat_activity`, and related views), with automatic audit logging; include lock-diagnosis in on-call training. | Sofia Grigoryan | April 16, 2027 | P1 |
| P2-1 | Add a structured "hypothesis checkpoint" to the incident command process: at 15-minute intervals, the IC states the working theory, evidence for, and evidence against, recorded in the incident channel. Incorporate into IC training. | Priyanka Deshmukh | May 14, 2027 | P2 |

### 8.4 Make Remediation Safe

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P0-6 | Change fleet-restart tooling defaults: batched, health-gated cohorts (max 50 instances) as the default; simultaneous restart requires an explicit override flag and a second engineer's confirmation. | Anaïs Okafor (Platform Tooling) | April 2, 2027 | P0 |
| P1-9 | Fix control plane client startup behavior: exponential backoff with full jitter on connection acquisition, capped retry rates, and a fleet-wide chaos test validating recovery from metadata store connection exhaustion. | Anaïs Okafor (Platform Tooling) | May 7, 2027 | P1 |
| P1-10 | Re-tune connection pooler (PgBouncer) configuration for cold-start surge: queueing headroom, admission control, and documented capacity math for maximum concurrent reconnections. | Devika Rao (Database Platform) | April 30, 2027 | P1 |
| P1-11 | Rewrite and validate the Compass failover runbook against current tooling via a game-day exercise; establish a quarterly runbook review with each critical runbook exercised (in staging or game day) at least twice yearly. First game day by due date. | Sofia Grigoryan | May 21, 2027 | P1 |

### 8.5 Fix Communication

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P1-12 | Delegate status page authority to the incident commander: any SEV-1/SEV-2 IC may post a pre-approved cause-neutral acknowledgment without further sign-off. Target: first public update within 15 minutes of SEV declaration, tracked as an incident-response SLO. | Jun-ho Park | March 26, 2027 | P1 |
| P1-13 | Publish a template library of pre-approved status updates (investigating, identified, mitigating, monitoring, resolved) integrated into the incident tooling as one-click actions. | Jun-ho Park | April 9, 2027 | P1 |
| P2-2 | Create a communications-lead on-call rotation for SEV-1 incidents, responsible for status cadence, support talking points, and enterprise notification, so the IC never owns external communication directly. | Jun-ho Park | May 14, 2027 | P2 |

### 8.6 Address the Organizational Pattern

| ID | Action | Owner | Due Date | Priority |
|---|---|---|---|---|
| P1-14 | Institute an operational-risk register reviewed quarterly with product leadership: each deferred infrastructure item carries a concrete risk statement ("what specifically can go wrong, at what blast radius"), and deferral requires explicit acceptance of that statement by the VP of Engineering. | Oliver Baptiste | April 30, 2027 | P1 |
| P2-3 | Commission a "silent decay" audit across the platform: identify safety mechanisms (alerts, runbooks, checklists, suppressions, escalation paths) with no owner, no test, or no review date; assign owners and validation cadence for each. Report findings to engineering leadership. | Priyanka Deshmukh | June 11, 2027 | P2 |
| P2-4 | Publish the customer-facing version of this postmortem and complete follow-up conversations with all 22 escalated enterprise accounts. | Jun-ho Park | March 31, 2027 | P2 |

---

## 9. Lessons Learned

**A safe change process is defined by its worst permitted path, not its average one.** Our migration process worked fine for hundreds of migrations because most migrations are harmless on any engine version. The optional checklist question meant the process offered no additional protection precisely in the case where protection mattered.

**Deferred infrastructure work is a risk decision, and it must be priced like one.** Nobody decided to accept "a routine ALTER TABLE can take down the control plane for five hours." But that is what three deferrals of the Compass upgrade amounted to. Risk that is described vaguely gets deferred indefinitely; risk that is described concretely gets weighed. Action item P1-14 exists to force the concrete description.

**Safety mechanisms decay silently unless something exercises them.** Four independent safeguards — a fast alert, a lag alert, a runbook, and a checklist question — were all broken before March 9, and nothing told us. Detection systems need their own detection. Suppressions need expiry. Runbooks need game days. The pattern generalizes well beyond the specific fixes in this document, which is why the silent-decay audit (P2-3) may be the most important single item in Section 8.

**Recovery actions need the same scrutiny as changes.** The fleet restart was a remediation step executed under pressure with tooling whose default behavior nobody had modeled at scale. It added 71 minutes — nearly a quarter of the total incident. Runbooks and tooling for recovery deserve capacity math, safe defaults, and rehearsal, because they run exactly when the system is least able to absorb another mistake.

**Say something before you know everything.** The 52-minute public silence did more relationship damage, per minute, than the outage itself. A cause-neutral acknowledgment requires no diagnosis and carries almost no retraction risk. The bar for the first status update should be "customers are affected," not "we understand why."

**Diagnosis speed is a function of who is in the room and what they can see.** The lock was one query away for 98 minutes. The fix is not smarter responders — our responders acted well — but escalation rules that bring domain expertise in automatically, dashboards that surface database internals alongside infrastructure views, and diagnostic access broad enough that the person on call can ask the question that matters.

We are publishing a customer-facing version of this document and will report completion of all P0 and P1 action items in the Q2 2027 engineering review.

---

*This postmortem was prepared under Meridian Stack's blameless postmortem policy. Its purpose is to improve the systems and processes that allowed this incident to occur and to extend as long as it did — not to assign fault to any individual. Questions should be directed to the document owner.*

## Appendix A: Detailed Metrics

### A.1 Error Rate Progression

Control plane API error rate, sampled at 5-minute intervals across the incident window. Values are the percentage of API requests returning 5xx responses or timing out, aggregated across all endpoints.

| Time | Error Rate | Phase |
|---|---|---|
| 2:10 p.m. | 0.3% | Baseline |
| 2:15 p.m. | 1.8% | Lock acquired; queueing begins |
| 2:20 p.m. | 6.4% | Threshold crossed; fast alert suppressed |
| 2:30 p.m. | 34.1% | Connection pools saturating fleet-wide |
| 2:41 p.m. | 71.2% | Peak; steady state under lock |
| 3:00 p.m. | 69.8% | Sustained degradation |
| 3:30 p.m. | 70.5% | Provider hypothesis under investigation |
| 4:00 p.m. | 68.9% | Migration kill in progress |
| 4:05 p.m. | 41.2% | Brief recovery after lock release |
| 4:10 p.m. | 63.7% | Secondary outage; connection pool exhaustion |
| 4:30 p.m. | 66.1% | Crash-loop sustained storm |
| 4:50 p.m. | 51.3% | Batched restart underway |
| 5:16 p.m. | 38.6% | 50% of fleet healthy |
| 5:52 p.m. | 8.9% | Full fleet healthy |
| 6:03 p.m. | 4.1% | Below SLO threshold |
| 6:30 p.m. | 1.2% | Backlog draining |
| 7:11 p.m. | 0.3% | Baseline restored |

The error rate never reached 100% because API endpoints that do not touch `resource_events` — approximately 29 percent of request volume, chiefly read-only billing queries and health endpoints — continued to succeed throughout. As noted in Section 6.2, this partial availability reinforced the provider-network hypothesis by making the failure look selective rather than total.

### A.2 Failed Request Breakdown by Endpoint Category

| Endpoint Category | Failed Requests | Share of Total |
|---|---|---|
| Resource provisioning and lifecycle | 4.6M | 40.4% |
| Configuration reads (endpoint resolution, ACL lookups) | 3.9M | 34.2% |
| Credential operations | 1.4M | 12.3% |
| Console/UI backing calls | 1.1M | 9.6% |
| Webhook and event delivery confirmations | 0.4M | 3.5% |
| **Total** | **11.4M** | **100%** |

The configuration-read category is notable: these are the calls that 63 customers make on data plane hot paths, producing the indirect data plane impact described in Section 2.1.

### A.3 Compass Metrics During the Lock

| Metric | Baseline | Peak During Incident |
|---|---|---|
| Blocked queries (`pg_locks` waiters) | 0–3 | 4,214 (3:52 p.m.) |
| Active connections | ~380 | 500 (hard limit) |
| Replication lag | < 2 seconds | 41 minutes (4:02 p.m.) |
| Lock wait time, p99 | 4 ms | > 300 s (statement timeout) |
| PgBouncer client wait queue | 0 | 2,890 (4:09 p.m., secondary outage) |

The replica lag figure explains the 3:58 p.m. failover rejection: promoting a replica 41 minutes behind would have discarded committed control plane state, including in-flight provisioning records, and would likely have produced a data-consistency incident worse than the availability incident it replaced.

### A.4 Support Volume

| Window | Tickets Opened | Notes |
|---|---|---|
| 2:14 – 3:00 p.m. | 312 | Pre-page; no official acknowledgment available |
| 3:00 – 3:53 p.m. | 604 | Post-page; status page still green |
| 3:53 – 7:11 p.m. | 931 | Status page active; ticket rate declines after 4:24 p.m. update cadence begins |
| **Incident total** | **1,847** | |
| Following 72 hours | 3,100 | Credit inquiries, backlogged jobs, escalations |

Ticket arrival rate dropped approximately 40 percent within 30 minutes of the second, substantive status page update at 4:24 p.m. — direct evidence for the communication findings in Section 6.4: customers who can see an acknowledged incident with an ETA largely stop filing duplicate tickets.

---

## Appendix B: The Migration

### B.1 Statement as Deployed

```sql
-- 20270309-add-retention-class
ALTER TABLE resource_events
  ADD COLUMN retention_class text NOT NULL DEFAULT 'standard';
```

### B.2 Behavior by Engine Version

| Engine | Behavior | Estimated Duration on `resource_events` |
|---|---|---|
| Compass production version | Full table rewrite under ACCESS EXCLUSIVE lock | ~3.5–4 hours projected (killed at 1h 48m) |
| Staging version / upgrade target | Metadata-only change; default stored in catalog | < 50 ms |

### B.3 Safe Equivalent Under the Pattern Library (P1-2)

The pattern that will be required for tables above the P0-3 threshold, expressed against the current production version:

```sql
-- Step 1: add column without default (metadata-only on all versions)
ALTER TABLE resource_events ADD COLUMN retention_class text;

-- Step 2: set default for new rows only
ALTER TABLE resource_events
  ALTER COLUMN retention_class SET DEFAULT 'standard';

-- Step 3: backfill existing rows in batches of 10,000,
--         throttled, via the backfill job framework
--         (runs over hours; no exclusive lock held)

-- Step 4: after backfill verification, add NOT NULL
--         via CHECK constraint NOT VALID + VALIDATE
```

Total exclusive lock time under this pattern: milliseconds per step. The operational cost is a multi-day rollout instead of a single statement — precisely the trade-off the mandatory checklist question (P0-2) and CI gate (P0-3) now force authors to confront explicitly.

---

## Appendix C: Communication Log

External communications issued during the incident, reproduced for the record.

| Time | Channel | Content Summary |
|---|---|---|
| 3:53 p.m. | Status page | Investigating — "We are investigating elevated error rates affecting the control plane API and console." First public acknowledgment; 99 minutes after impact began. |
| 4:24 p.m. | Status page | Identified — Root cause identified as a database operation blocking control plane queries; operation terminated; recovery in progress. First ETA given (60–90 minutes, later revised). |
| 4:45 p.m. | Status page | Mitigating — Acknowledged extended recovery due to "a complication during service restart"; batched recovery underway. |
| 4:52 p.m. | Direct email | Enterprise notification sent by executive sponsor's team to 214 enterprise accounts with named TAM contacts. |
| 5:10 p.m. | Status page | Mitigating — 50% fleet recovery reported; revised ETA. |
| 5:30 p.m. | Status page | Mitigating — Continued progress update. |
| 5:55 p.m. | Status page | Monitoring — Full fleet healthy; error rates falling; backlog processing. |
| 6:15 p.m. | Status page | Monitoring — Error rates below SLO threshold; async job backlog draining. |
| 6:50 p.m. | Status page | Monitoring — Backlog cleared; monitoring for stability. |
| 8:30 p.m. | Status page | Resolved — Summary of incident, apology, commitment to public postmortem within ten business days. |
| Mar 10, 11:00 a.m. | Email | All affected customers (2,140) notified of automatic service credit application; no claim filing required. |
| Mar 19 | Blog / status page | Public postmortem published (customer-facing version of this document). |

The gap between the first and second status updates (31 minutes) and the cadence thereafter (roughly every 20 minutes) reflect the communication discipline that took hold once the executive sponsor and Director of Customer Reliability were both engaged. The target state under P1-12 and P1-13 is that the 3:53 p.m. update happens at approximately 3:20 p.m. — within 15 minutes of SEV declaration — regardless of who is available.

---

## Appendix D: Postmortem Review Attendance and Process

The postmortem review was held March 17, 2027, 1:00–3:30 p.m. EST.

**Attendees:** Priyanka Deshmukh (facilitator, document owner), Sofia Grigoryan, Oliver Baptiste, Jun-ho Park, Malik Tarrant, Devika Rao, Tomasz Lindqvist, Anaïs Okafor, the migration author and both reviewers (names withheld from the published document consistent with blameless policy), two SRE on-call responders, and three observers from adjacent teams.

**Process notes:**

- The timeline in Section 4 was reconstructed from incident channel logs, alerting system audit records, Compass query logs, and status page history, then reviewed line-by-line by all participants for accuracy before analysis began.
- Contributing factors were developed using a "five whys" walk on each of the four compounding failures independently, then cross-checked for shared upstream causes — which is how the "silent decay" pattern in Section 6.5 was identified as common to all four.
- Action items were drafted by the teams that own the affected systems, not assigned top-down; owners committed dates in the review itself. Priority disagreements (two items initially proposed as P2 were promoted to P1) were resolved by the VP of Engineering in the room.
- The migration author participated fully in the review. Consistent with policy, no disciplinary action was taken or considered; the review concluded explicitly that any of roughly a dozen engineers who regularly write Compass migrations could have shipped the same change with the same outcome, which is the definition of a systems failure.

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| **ACCESS EXCLUSIVE lock** | The most restrictive PostgreSQL table lock; blocks all concurrent reads and writes on the table, including `SELECT`. |
| **Compass** | Meridian Stack's control plane PostgreSQL cluster; system of record for customer resources, credentials metadata, ACLs, and billing meters. |
| **Control plane** | The API and console layer through which customers manage resources (provision, configure, rotate credentials), as distinct from the data plane. |
| **Data plane** | The hosted databases and message queues themselves — customer queries and message traffic. |
| **PgBouncer** | Connection pooler sitting in front of Compass, multiplexing many client connections onto a smaller number of database connections. |
| **`resource_events`** | The 400-million-row append-heavy table recording resource state transitions; joined on most control plane read paths. |
| **SEV-1 / SEV-2** | Meridian Stack incident severity levels. SEV-1: major customer-facing outage or degradation; SEV-2: significant degradation with partial impact. |
| **Thundering herd** | Failure pattern in which many clients retry or reconnect simultaneously, overwhelming a shared dependency and preventing recovery. |

---

## Appendix F: Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | March 11, 2027 | P. Deshmukh | Initial draft: timeline and impact figures |
| 0.2 | March 13, 2027 | P. Deshmukh, S. Grigoryan | Root cause and contributing factors sections; migration technical appendix |
| 0.3 | March 16, 2027 | All section owners | Draft action items circulated for owner commitment |
| 0.9 | March 17, 2027 | P. Deshmukh | Incorporated postmortem review outcomes; final action item list with committed dates |
| 1.0 | March 19, 2027 | P. Deshmukh | Final. Approved by O. Baptiste. Customer-facing version derived and published same day. |

**Next scheduled review:** June 15, 2027 — verification of all P0 and P1 action item completion, held as part of the Q2 engineering program review. Any P0 or P1 item at risk of missing its date must be flagged to the VP of Engineering no later than two weeks before the due date, with a revised date and rationale recorded in this document's tracking issue.

*— End of document —*

---

# Addendum 1: 30-Day Follow-Up Review

**Added:** April 9, 2027
**Author:** Priyanka Deshmukh
**Reviewed By:** Oliver Baptiste

Per the commitment made in the March 17 postmortem review, this addendum records the status of all action items due on or before April 9, 2027, notes material developments since publication, and corrects one factual item in the original document.

## AD1.1 Correction to the Original Document

Section 2.2 reported four cancelled accounts representing $290,000 ARR "within a month." Final reconciliation with the revenue operations team confirms the figure at four accounts and $290,000 ARR, but one of the four accounts had opened a cancellation inquiry on February 24, 2027 — thirteen days before the incident — citing pricing. The incident was cited in their final cancellation notice and accelerated the decision, but attributing the full $85,000 ARR of that account solely to this incident overstates the incident's churn impact. The conservatively attributable figure is **three accounts and $205,000 ARR directly caused, with one $85,000 account partially attributable**. The original figure is retained in Section 2.2 for consistency with the customer-facing postmortem already published; this addendum is the corrected record.

## AD1.2 Action Item Status — Items Due On or Before April 9

| ID | Action (abbreviated) | Due | Status |
|---|---|---|---|
| P0-2 | Mandatory lock-duration checklist question | Mar 26 | **Complete** (Mar 24). Tooling-enforced; merge blocks on blank answer. 41 migrations processed since; two flagged and reworked before merge. |
| P0-4 | End-to-end alert route audit | Mar 26 | **Complete** (Mar 26). 1,212 alert routes audited. Findings: 34 routes targeted archived channels, 11 targeted departed employees' direct messages, 6 targeted a deprecated webhook integration. All 51 dead routes remediated. Full inventory signed off by team leads. |
| P1-12 | IC status page authority + 15-minute SLO | Mar 26 | **Complete** (Mar 25). Policy live. Exercised once in earnest (see AD1.4). |
| P2-4 | Public postmortem + enterprise follow-ups | Mar 31 | **Complete** (Mar 30). Public postmortem published Mar 19; all 22 enterprise escalation conversations closed. Two accounts requested contractual SLA amendments, now with legal. |
| P0-6 | Batched fleet-restart defaults | Apr 2 | **Complete** (Apr 1). Default cohort size 50, health-gated. Simultaneous restart now requires `--i-understand-thundering-herd` flag plus second-engineer confirmation in tooling. |
| P1-7 | Auto-escalation of DB platform on-call | Apr 2 | **Complete** (Mar 31). Fired correctly during the April 6 event (AD1.4). |
| P1-1 | Staging/production engine version alignment | Apr 9 | **Complete** (Apr 7). Staging Compass **downgraded** to match production pending the P0-1 upgrade — a deliberately uncomfortable but honest choice. Weekly drift check live. |
| P1-5 | Unsuppressible customer-impact SLO alert | Apr 9 | **Complete** (Apr 8). Deployed and verified via synthetic fault injection. |
| P1-13 | Status update template library | Apr 9 | **Complete** (Apr 9). Five templates live as one-click actions in incident tooling. |

**Nine of nine items due in this window closed on or before their due dates.** Items due after April 9 (P0-1, P0-3, P0-5, P1-2, P1-3, P1-4, P1-6, P1-8, P1-9, P1-10, P1-11, P1-14, P2-1, P2-2, P2-3) remain on track per owner attestation, with two exceptions noted in AD1.3.

## AD1.3 Items At Risk

- **P0-3 (CI lock-analysis gate, due April 23):** The static analysis approach originally scoped cannot reliably determine lock behavior for migrations using dynamic SQL or procedural blocks (approximately 8 percent of historical Compass migrations). The owner (Devika Rao) has proposed a revised design: static analysis for standard DDL, plus a mandatory dry-run against an anonymized production-scale replica for anything the analyzer cannot classify. Revised delivery date **May 14, 2027**, approved by the VP of Engineering on April 6 per the flagging protocol in Appendix F. The interim manual review by a senior DBA, in place since March 10, continues until the gate ships.
- **P0-1 (Compass major-version upgrade, due June 30):** On track but flagged amber. The milestone plan was approved March 26 as required. Load testing on the upgraded replica surfaced a query-planner regression affecting two billing-path queries; fixes (targeted index changes) are validated in staging. The production cutover is scheduled for the **June 12–13 maintenance window**, leaving two weeks of buffer before the hard deadline. Per P0-1's terms, any slip beyond June 30 requires CEO sign-off; no such request is anticipated.

## AD1.4 The April 6 Validation Event

At 9:37 a.m. on April 6, 2027, a misconfigured deploy caused control plane error rates to reach 12 percent for 19 minutes. While minor, the event exercised nearly every newly installed control and is worth recording as a natural experiment:

- **Detection:** The new unsuppressible SLO alert (P1-5) paged at 9:41 a.m. — four minutes after impact began, versus 47 minutes on March 9.
- **Escalation:** The database platform on-call was auto-paged at 9:49 a.m. under P1-7 and confirmed within six minutes that Compass was healthy, eliminating the database hypothesis early rather than late — the inverse of March 9's failure.
- **Communication:** The incident commander posted a cause-neutral status update at 9:52 a.m. using template two from the P1-13 library — 11 minutes after the page, inside the 15-minute SLO.
- **Resolution:** Rollback completed at 9:56 a.m. Total customer impact: 19 minutes, approximately 41,000 failed requests, zero service credits owed under contractual thresholds.

Comparable telemetry from March 9 suggests the same event under March 8 conditions would have run 45–60 minutes before first page. The response was not flawless — the incident channel was slow to link the deploy that caused the event, and one responder initially could not find the new Compass dashboard (P1-6, not yet due) — but the compounding pattern that defined March 9 did not recur.

## AD1.5 Observations for the Q2 Review

Two early findings are forwarded to the June 15 review for discussion:

1. **The suppressed-but-true alert log (P1-3, in progress) is already valuable.** A prototype running since March 28 has logged 14 instances of alerts evaluating true while suppressed. Twelve were legitimate deploy noise; two were genuine anomalies caught days earlier than they otherwise would have been. The weekly review of this log should be made permanent regardless of P1-3's final design.

2. **Checklist friction is real and must be managed, not dismissed.** The mandatory lock-duration question (P0-2) has drawn complaints that it adds ceremony to trivial migrations on small tables. The complaints are reasonable — and they are exactly the pressure that produced the November 2026 "optional" revision that contributed to this incident. The Q2 review should decide deliberately whether to add a size-based exemption (tables under 1 million rows auto-answer the question) rather than allow informal erosion. The lesson of Section 6.5 is not that friction is good; it is that safety controls must be changed by decision, not by decay.

**Next addendum:** Following the June 15, 2027 Q2 verification review, covering completion of all remaining P0 and P1 items and the outcome of the Compass production upgrade.

*— End of Addendum 1 —*
