# Incident Postmortem: Compass Control Plane Degradation

**Incident ID:** INC-2027-0309
**Severity:** SEV-1
**Date of Incident:** Tuesday, March 9, 2027
**Duration of Customer-Visible Degradation:** 4 hours 52 minutes (2:19 p.m. – 7:11 p.m. EST)
**Document Owner:** Priyanka Deshmukh, Staff Site Reliability Engineer
**Reviewers:** Oliver Baptiste (VP Engineering), Sofia Grigoryan (Director, Database Platform), Jun-ho Park (Director, Customer Reliability), Malik Tarrant (Manager, Support Operations)
**Status:** Final — reviewed in Incident Review Forum, March 17, 2027
**Classification:** Internal; redacted summary approved for customer distribution

---

## 1. Summary

On Tuesday, March 9, 2027, a scheduled database migration applied to the Compass PostgreSQL cluster — the system of record for the Meridian Stack control plane — rendered the control plane API substantially unavailable for four hours and fifty-two minutes. The migration added a column with a non-null default to a table holding approximately 400 million rows. On the PostgreSQL major version Compass was running, this operation required a full table rewrite under an ACCESS EXCLUSIVE lock. Every control plane query touching that table queued behind the lock. Error rates crossed five percent within five minutes of the migration's start and reached seventy-one percent by 2:41 p.m.

No human being was notified for forty-seven minutes. The error-rate alert that should have fired within two minutes was configured with a thirty-minute evaluation window, and the alert routing had been placed in a suppression group tied to the quarterly deploy freeze calendar — a suppression that had been extended past its intended expiry. The first page reached the on-call engineer at 3:01 p.m.

Once engaged, the response encountered a second failure of a different kind. Timeout errors surfaced first and most densely in a single availability zone, an artifact of how connection pool exhaustion propagated through the fleet rather than a signal of network trouble. The incident commander formed an early hypothesis of an upstream provider network event and the team pursued that hypothesis for thirty-eight minutes. During this period the public status page remained green. The actual cause was identified at 3:52 p.m., ninety-eight minutes after customer impact began.

Remediation then introduced a third failure. After terminating the migration, the team restarted the entire control plane fleet — approximately 900 instances — in a single action. All 900 instances attempted to re-establish connections to the metadata store simultaneously, exhausting its connection pool and producing a thundering-herd condition that added seventy-one minutes to the outage. Full recovery was confirmed at 7:11 p.m.

The incident affected 2,140 customers, failed approximately 11.4 million API requests, generated $410,000 in service credits under contractual SLA terms, and preceded the cancellation within thirty days of four accounts representing $290,000 in annual recurring revenue.

This document treats the incident as the output of a system rather than the product of individual error. Every person involved acted reasonably given the information visible to them at the time. The failures described here are failures of instrumentation, of maintenance discipline, of process design, and of prioritization — and each of those is correctable.

---

## 2. Impact

### 2.1 Customer Impact

| Metric | Value |
|---|---|
| Total customers on platform | 6,800 |
| Customers experiencing degraded or failed control plane operations | 2,140 (31.5%) |
| Customers experiencing complete control plane unavailability (>50% error rate sustained ≥15 min) | 1,412 |
| Failed API requests | 11,400,000 (approx.) |
| Peak control plane API error rate | 71% |
| Duration of customer-visible degradation | 4h 52m |
| Duration above 50% error rate | 3h 41m |

### 2.2 Scope of Functional Impact

The Compass cluster backs the control plane only. Customer data planes — running database instances and message queue brokers — continued to serve traffic throughout. This distinction matters and was insufficiently communicated during the incident itself.

Affected operations:

- Provisioning of new database instances and queue clusters (100% failure during peak)
- Scaling operations, both manual and autoscaling-triggered
- Configuration changes: parameter groups, network policies, retention settings
- Credential rotation and access key management
- Backup initiation and restore operations
- Console login and session establishment (authentication depends on Compass session tables)
- Programmatic API access via SDK and CLI
- Metrics and log ingestion into the customer-facing observability dashboard (delayed, not lost)

Unaffected operations:

- Read and write traffic to provisioned database instances
- Message publish and consume against provisioned queues
- Existing connections using previously issued credentials
- Automated backups already scheduled and dispatched prior to 2:14 p.m.

Twenty-nine customers had autoscaling events queued during the outage window that failed to execute. Of these, eleven experienced downstream capacity saturation in their own applications. Three of those eleven were among the four accounts that subsequently cancelled.

### 2.3 Financial Impact

| Category | Amount |
|---|---|
| Service credits issued under SLA | $410,000 |
| Annual recurring revenue from accounts cancelling within 30 days | $290,000 |
| Engineering hours consumed (response + remediation, 31 people) | 412 hours |
| Support ticket volume above baseline | 1,847 tickets |
| Estimated first-year cost of remediation program (Section 9) | $340,000 |

The four cancelling accounts were $71,000, $84,000, $52,000, and $83,000 in annual recurring revenue. Exit interviews conducted by the account management team identified the duration of silence on the status page — not the outage itself — as the decisive factor in two of the four cases. One account cited the outage as confirmation of a pre-existing concern about platform maturity. One cited an unrelated budget reduction with the outage as contributing context.

### 2.4 Reputational and Trust Impact

The status page carried no acknowledgment of the incident for fifty-two minutes after the first page fired — ninety-nine minutes after customer impact began. During that window, 1,847 support tickets arrived and customers posted publicly on two developer forums and one social platform. The gap between observable customer experience and published platform status is, by our own operating principles, the most serious single element of this incident.

---

## 3. Timeline

All times are Eastern Standard Time on Tuesday, March 9, 2027, unless otherwise noted. Times are drawn from application logs, the incident channel transcript, paging system records, and the deployment audit log. Where a time is inferred rather than logged, it is marked *(approx.)*.

### 3.1 Pre-Incident

**Thursday, March 4, 11:20 a.m.** — Migration `2027_03_add_tenant_tier_flag` is authored and submitted for review. The migration adds a column `tenant_tier_flag SMALLINT NOT NULL DEFAULT 0` to `control_plane.tenant_resource_index`, a table with approximately 400 million rows.

**Thursday, March 4, 3:45 p.m.** — Migration receives two approvals in code review. The migration checklist attached to the pull request contains the field "Estimated lock duration and lock type," marked in the template as optional. The field is left blank. Both reviewers approve. The checklist's own validation logic does not block on optional fields.

**Monday, March 8, 9:15 a.m.** — Migration is scheduled for the Tuesday afternoon maintenance window, a standing window from 2:00 to 4:00 p.m. Tuesdays and Thursdays.

**Tuesday, March 9, 2:00 p.m.** — Maintenance window opens. Two prior migrations in the batch execute and complete within ninety seconds.

### 3.2 Impact Begins — Undetected

**2:14 p.m.** — Migration `2027_03_add_tenant_tier_flag` begins execution. PostgreSQL acquires an ACCESS EXCLUSIVE lock on `control_plane.tenant_resource_index` and begins a full table rewrite. On the major version Compass runs, `ADD COLUMN ... NOT NULL DEFAULT` cannot be performed as a metadata-only operation.

**2:15 p.m.** — Control plane API request latency begins climbing. Queries against `tenant_resource_index` queue behind the exclusive lock. p99 latency moves from 84 ms to 2,100 ms within sixty seconds.

**2:17 p.m.** — Connection pool utilization on control plane instances reaches 100%. Instances begin rejecting inbound requests with 503 responses as pool checkout timeouts expire.

**2:19 p.m.** — Control plane API error rate crosses 5%. Under intended configuration, this threshold triggers a page within two minutes. **No page is generated.**

**2:19 p.m. – 2:41 p.m.** — Error rate climbs steadily. Cascading pool exhaustion propagates across the fleet. Because instances in `us-east-1a` carry a marginally higher share of session-affinity traffic, that zone's instances exhaust pools first and most completely, producing a zone-skewed error distribution in dashboards.

**2:23 p.m.** — First customer support ticket arrives, reporting provisioning failures.

**2:28 p.m.** — Support ticket volume reaches twelve. Support tier-1 queue begins to back up.

**2:31 p.m.** — Replication lag on Compass read replicas crosses the alert threshold of 30 seconds. The alert fires and routes to Slack channel `#db-platform-alerts`. **That channel was archived on January 14, 2027**, during a workspace consolidation. The message is delivered to an archived channel and seen by no one.

**2:34 p.m.** — Malik Tarrant, Manager of Support Operations, notices the ticket pattern and posts in `#support-eng` asking whether anyone is aware of a control plane issue. The message receives no response; the channel is not monitored by an on-call rotation.

**2:41 p.m.** — Control plane API error rate reaches 71%. This becomes the incident's peak sustained rate.

**2:47 p.m.** *(approx.)* — Malik Tarrant escalates by direct message to a platform engineer he knows personally. The engineer is in a meeting.

**2:58 p.m.** — The thirty-minute rolling evaluation window on the primary error-rate alert completes its first full window in which the averaged error rate exceeds threshold.

### 3.3 Detection

**3:01 p.m.** — **First page fires.** Alert `control-plane-error-rate-critical` pages the SRE on-call rotation. Elapsed time from customer impact: **47 minutes**.

**3:03 p.m.** — Priyanka Deshmukh, Staff Site Reliability Engineer and on-call, acknowledges the page.

**3:04 p.m.** — Incident channel `#inc-2027-0309` is created. Severity set provisionally to SEV-2.

**3:06 p.m.** — Deshmukh declares herself Incident Commander and upgrades severity to SEV-1 after observing the 71% error rate on the control plane dashboard.

**3:07 p.m.** — Deshmukh pages the platform engineering secondary and requests support liaison. Malik Tarrant joins the channel within ninety seconds and reports 340 open tickets.

### 3.4 Misdiagnosis

**3:09 p.m.** — Deshmukh opens the error distribution view. Errors are heavily concentrated in `us-east-1a` — approximately 61% of failures originate from instances in that zone, against an expected baseline of 34%. Timeout errors dominate the error taxonomy.

**3:11 p.m.** — Deshmukh states the working hypothesis in channel: an availability zone network event at the infrastructure provider. The reasoning is documented and, on the evidence available, defensible — zone-correlated timeouts are the canonical signature of provider network degradation, and the team has seen this pattern twice in the preceding eighteen months.

**3:13 p.m.** — Team opens a support case with the infrastructure provider at Severity 1.

**3:14 p.m. – 3:52 p.m.** — Investigation proceeds along the provider-network hypothesis:

- 3:16 p.m. — Team checks provider status dashboard. All green. Interpreted as expected lag in provider status reporting.
- 3:19 p.m. — Attempt to shift traffic away from `us-east-1a` by adjusting load balancer weights. Error rate does not improve; failures redistribute to remaining zones. **This is the first strong disconfirming signal.** It is noted in channel but interpreted as evidence that the network event is broader than one zone.
- 3:24 p.m. — Network path testing between control plane instances and Compass primary. Latency normal, packet loss zero.
- 3:29 p.m. — Team requests provider escalation. Provider engineer joins bridge at 3:38 p.m.
- 3:31 p.m. — Second attempt at zone evacuation, more aggressive. No improvement.
- 3:38 p.m. — Provider engineer reports no infrastructure events affecting the account or region.
- 3:41 p.m. — Hypothesis begins to weaken in channel. Deshmukh asks for a broader look at Compass itself.

**3:44 p.m.** — Deshmukh pages Sofia Grigoryan, Director of Database Platform. Grigoryan joins at 3:47 p.m.

**3:52 p.m.** — **Root cause identified.** Grigoryan queries `pg_locks` joined against `pg_stat_activity` and finds the ACCESS EXCLUSIVE lock held by the migration session on `tenant_resource_index`, with 1,847 sessions in `Lock` wait state behind it. She posts the query output to the incident channel. Elapsed time from customer impact: **1 hour 38 minutes**. Elapsed from first page: **51 minutes**.

**3:53 p.m.** — Working hypothesis revised. Provider support case downgraded.

### 3.5 Remediation and Secondary Failure

**3:55 p.m.** — Team debates whether to terminate the migration or allow it to complete. Grigoryan estimates remaining rewrite time at 40–90 minutes based on observed I/O throughput against table size — an estimate with wide error bars because the table's on-disk footprint had not been profiled recently.

**3:58 p.m.** — Decision to terminate. Rationale: the completion estimate is unreliable and the outage is already at ninety minutes. Rollback path is confirmed available.

**4:01 p.m.** — `pg_terminate_backend` issued against the migration session. Session terminates. PostgreSQL begins rolling back the partial table rewrite.

**4:03 p.m.** — Lock released. Rollback of the partial rewrite completes. Queued queries begin to drain. Error rate begins falling: 71% → 58% within ninety seconds.

**4:04 p.m.** — Team observes that a substantial fraction of control plane instances remain in a degraded state. Their connection pools contain stale connections held open through the lock period; health checks report the instances as unhealthy but the instances are not self-recovering within the observed window. Approximately 640 of 900 instances are in this state.

**4:05 p.m.** — **Fleet-wide restart issued.** The operator invokes the standard rolling restart tooling. The tooling's default concurrency parameter — intended for routine deploys and never revisited for emergency use — permits effectively unbounded parallelism when invoked with the `--emergency` flag. All 900 instances restart within approximately forty seconds.

**4:06 p.m.** — All 900 instances begin startup sequence simultaneously. Each opens its configured minimum pool of 12 connections to the metadata store. Demand: 10,800 connections. Metadata store `max_connections`: 4,000.

**4:07 p.m.** — Metadata store connection pool exhausted. Instances fail startup health checks, are marked unhealthy by the orchestrator, and are restarted — generating a new wave of connection attempts. A self-sustaining restart loop establishes itself.

**4:08 p.m.** — Error rate returns to 69%. **The remediation has restored the outage to near-peak severity.**

**4:12 p.m.** — Team identifies the thundering herd. Attempts to halt the orchestrator's restart loop.

**4:20 p.m.** — Oliver Baptiste, Vice President of Engineering, joins the incident channel. Assumes executive communication role; Deshmukh retains incident command.

**4:26 p.m.** — Orchestrator health check grace period extended from 30 seconds to 300 seconds to break the restart loop. Loop stabilizes but connection demand remains above capacity.

**4:34 p.m.** — Metadata store `max_connections` raised from 4,000 to 9,000. Requires a restart of the metadata store, taking 90 seconds, during which all control plane operations fail. Judged acceptable given prevailing error rate.

**4:41 p.m.** — Team begins deliberate staged recovery: instances scaled to zero, then reintroduced in cohorts of 75 with a 4-minute interval between cohorts.

**4:53 p.m.** — First cohort healthy. Error rate 64% (reflecting reduced serving capacity rather than continued failure).

**5:19 p.m.** — Error rate falls below 50% for the first time since 2:26 p.m.

### 3.6 Communication

**3:53 p.m.** — **First status page update published.** Jun-ho Park, Director of Customer Reliability, posts an "Investigating" notice for the control plane API. Elapsed from first page: **52 minutes**. Elapsed from customer impact: **1 hour 39 minutes**.

**4:15 p.m.** — Second status update: "Identified."

**4:48 p.m.** — Third update, acknowledging that a remediation attempt had extended impact.

**5:30 p.m., 6:15 p.m., 6:50 p.m.** — Progress updates at roughly forty-minute intervals.

**7:15 p.m.** — Resolution notice published.

### 3.7 Recovery

**6:02 p.m.** — All 900 instances restored to service. Error rate 8%, residual failures attributed to retry storms from customer SDK clients with aggressive backoff configurations.

**6:38 p.m.** — Error rate below 2%.

**7:04 p.m.** — Error rate at baseline (0.03%). Latency percentiles within normal bands.

**7:11 p.m.** — **Incident declared resolved.** Total customer-visible degradation: 4 hours 52 minutes.

**7:20 p.m.** — Migration `2027_03_add_tenant_tier_flag` disabled in the migration registry pending redesign.

**8:45 p.m.** — Backlog of queued provisioning and scaling operations fully drained.

**Wednesday, March 10, 10:00 a.m.** — Immediate postmortem convened.

---

## 4. Root Cause

The proximate cause is stated simply: a schema migration adding a column with a non-null default to a 400-million-row table acquired an ACCESS EXCLUSIVE lock for the duration of a full table rewrite, blocking all control plane queries against that table.

The root cause is not the migration. The root cause is that **the Compass cluster was operating on a PostgreSQL major version whose behavior for this class of operation differs materially from the version the team's mental models, tooling, and review practices were calibrated against — and the organization had deferred the upgrade that would have eliminated the hazard for three consecutive quarters.**

On PostgreSQL 11 and later, `ADD COLUMN ... NOT NULL DEFAULT <constant>` is a metadata-only operation. The default is recorded in `pg_attribute` and materialized lazily. The operation completes in milliseconds regardless of table size. Compass was running PostgreSQL 10, where the same statement requires a full table rewrite under an exclusive lock.

Several consequences follow from that single fact:

**The migration author's model was correct for a version we were not running.** The engineer who wrote the migration had, in prior roles and in Meridian Stack's own non-Compass clusters (all on PostgreSQL 14 or 15), performed this operation dozens of times as a routine, instant change. The mental model was accurate; the environment was not what the model assumed.

**Both reviewers held the same model.** The review did not fail through inattention. It failed because the reviewers' shared and largely correct understanding of PostgreSQL behavior did not include the version-specific exception applying to the single most critical cluster in the company.

**The optional checklist field was the only remaining barrier, and optionality removed it.** The migration checklist asked for estimated lock duration and lock type. Marked optional, it was left blank, and no automated validation blocked merge. A required field would have forced the author to reason explicitly about locking, and that reasoning would likely have surfaced the version question.

The upgrade deferral itself deserves examination as a decision rather than an oversight. The Compass major-version upgrade was scoped in Q2 2026 at approximately six engineer-weeks plus a maintenance window of two to four hours. It was deferred in Q2 2026, Q3 2026, and Q4 2026. Each deferral was individually reasonable: each quarter presented revenue-linked commitments with dated external obligations, and the upgrade presented no forcing function — Compass was stable, performant, and within its support window.

The structural problem is that no deferral decision was ever evaluated against its cumulative risk. Each was assessed as a single-quarter delay of a low-urgency task. None was assessed as the third consecutive delay of the sole remediation for a known class of hazard on the company's most critical stateful system. Our planning process had no mechanism for surfacing the aggregate, and no mechanism for attaching a risk statement to a deferral that would travel with it into the next planning cycle.

Three additional failures shaped the incident's duration but did not cause it:

1. **Detection failure (47 minutes):** a thirty-minute evaluation window on a critical alert, compounded by an unexpired suppression rule.
2. **Diagnostic failure (38 minutes):** a plausible hypothesis anchored on a misleading zone-correlated signal, pursued past the point where disconfirming evidence had arrived.
3. **Remediation failure (71 minutes):** an unbounded fleet restart that exhausted a downstream connection pool.

Each is addressed in Section 5.

---

## 5. Contributing Factors

### 5.1 Alert Evaluation Window and Suppression Interaction

The `control-plane-error-rate-critical` alert was defined with a thirty-minute rolling evaluation window. Repository history shows the window was widened from five minutes to thirty in August 2026 to suppress false positives from a since-resolved batch job. The change was reverted for eleven other alerts in the same family. This one was missed.

Compounding this, the alert's routing had been placed in a suppression group associated with the Q1 deploy freeze calendar. The freeze ran January 2 through January 15. The suppression rule was written without an expiry and remained active on March 9. Suppression state is not surfaced on any dashboard and is not included in the weekly alerting health report.

The two defects were independent and either alone would have delayed detection. Together they produced a forty-seven-minute gap. Neither was detectable by anyone not specifically auditing alert configuration, and no such audit was scheduled.

### 5.2 Archived Slack Channel as Alert Destination

The replication-lag alert fired correctly at 2:31 p.m. and would have redirected the investigation to the database layer roughly eighty minutes earlier than it in fact turned. It routed to `#db-platform-alerts`, archived January 14, 2027, during a workspace consolidation.

The consolidation project produced a channel migration mapping but did not audit inbound webhook integrations. Slack accepts webhook posts to archived channels and returns HTTP 200. The alerting platform recorded successful delivery. No component of the system was in a position to know the message was unread.

There is no automated verification that alert destinations are live. There is no synthetic test that fires each alert on a schedule and confirms human acknowledgment.

### 5.3 Misleading Zone Correlation

The zone-skewed error distribution was real and was an artifact. Instances in `us-east-1a` carried approximately 12% more session-affinity traffic than the other two zones, a consequence of a load balancer configuration set during a 2026 capacity expansion. Under connection pool pressure, that zone exhausted its pools first and most completely.

The dashboard the incident commander consulted presents errors by availability zone as a primary dimension, reflecting a period when provider network events were the dominant cause of correlated failures. Database-layer indicators — lock wait counts, longest-running transaction, replication lag — appear on a separate dashboard reachable through two additional navigation steps and are not part of the standard incident triage view.

The information required to reach the correct diagnosis at 3:09 p.m. existed. It was two clicks away and was not part of the default path.

### 5.4 Hypothesis Anchoring and Absence of Disconfirmation Practice

The most consequential response behavior was the persistence of the provider-network hypothesis for thirty-eight minutes after formation, including twenty-two minutes after a strong disconfirming signal.

At 3:19 p.m. traffic was shifted away from `us-east-1a` and the error rate did not improve; failures redistributed. Under the provider-network hypothesis, evacuating the affected zone should have produced measurable improvement. It did not. The observation was recorded in channel and reinterpreted as evidence the event was broader than one zone — a reinterpretation that preserved the hypothesis by expanding it.

This is a well-described failure mode and it is not a failure of the individual. Our incident process contains no structural counterweight: no requirement to state what would falsify the working hypothesis, no assigned role for challenging it, no time-boxing that forces re-derivation from evidence. The hypothesis was formed by the incident commander, which further reduced the likelihood of challenge from a team operating under time pressure and deferring to command authority.

### 5.5 Restart Tooling Without Concurrency Bounds

The fleet restart tool supports staged rollout with configurable concurrency. Under the `--emergency` flag, concurrency limits are bypassed by design — a decision made in 2024 for a scenario in which stale state made staged restart actively harmful.

The tool provides no warning about downstream capacity, no dry-run summary of resulting connection demand, and no reference to metadata store limits. The relationship between fleet size and metadata store connection capacity was documented in a 2025 architecture review and had not been revisited. Fleet size had grown from approximately 400 instances at the time of that review to 900 on March 9. Metadata store `max_connections` had not changed.

The restart was the correct action. The blast radius was the defect.

### 5.6 Stale Failover Runbook

During the 3:55 p.m. discussion the team consulted the Compass failover runbook to evaluate promoting a read replica as an alternative to terminating the migration. The runbook's primary procedure invokes `compass-failover-ctl`, a command decommissioned in 2025 and replaced by a different tooling path. The runbook had not been updated.

This did not extend the outage — the team chose termination on other grounds — but it removed a viable option from consideration under time pressure, and it is representative. A subsequent audit of the twenty-three runbooks in the platform library found that nine contain at least one command, hostname, or path that no longer resolves. The most recent verified execution date across the library averages 14 months.

### 5.7 Status Page Authority and Communication Latency

The first status page update was published fifty-two minutes after the page fired. Investigation of this delay found no single point of failure but a diffuse ambiguity in ownership.

Jun-ho Park, Director of Customer Reliability, holds authority to publish status updates. Park was not paged when the incident was declared; the incident process pages engineering roles and relies on the incident commander to request communications support. Deshmukh, managing diagnosis, requested Park's involvement at 3:31 p.m. — twenty-five minutes after declaration. Park joined at 3:36 p.m., spent time establishing context, drafted an update, and sought confirmation of scope from the engineering team, which was mid-investigation. The update published at 3:53 p.m.

Each step is defensible. The aggregate is not. There is no template for an "investigating, cause unknown" notice that can be published without engineering sign-off, and there is a cultural preference — visible in the channel transcript — for waiting until a statement can be made with confidence. That preference optimizes for accuracy at the direct expense of timeliness, and in this incident it cost fifty-two minutes of customer trust.

### 5.8 Optional Checklist Fields

The migration checklist's lock-duration question was optional. The checklist contains fourteen fields, six of which are optional. Analysis of the preceding six months of migrations shows optional fields are completed 23% of the time; required fields, 99.4%.

An optional field on a safety checklist is not a weak control. It is, in practice, no control at all.

### 5.9 Maintenance Window Overlapping Business Hours

The Tuesday 2:00–4:00 p.m. window was chosen in 2024 to ensure full staffing during migrations. The reasoning was sound. The consequence is that migration risk is realized during the period of highest customer activity. The window represents an explicit and now-revisitable tradeoff between response capability and blast radius.

---

## 6. What Worked

It would be a mistake to read this document as a record of unbroken failure. Several elements of the response performed as designed, and preserving them is as important as fixing what did not.

**Escalation to domain expertise was fast and decisive once initiated.** Deshmukh paged Grigoryan at 3:44 p.m.; Grigoryan joined at 3:47 p.m. and identified the root cause in five minutes. The on-call directory was accurate, the paging path worked, and there was no hesitation about escalating despite the implicit acknowledgment that the standing hypothesis was wrong. That willingness to escalate against one's own hypothesis is a cultural asset.

**Incident command was clear and uncontested.** Deshmukh declared command at 3:06 p.m. and held it throughout. When Baptiste joined at 4:20 p.m. as the most senior person present, he explicitly took the executive communication role and left command in place. This is exactly right and is not universal at organizations of our size.

**Severity was correctly assessed and rapidly escalated.** SEV-2 to SEV-1 within two minutes of the initial page, based on observed error rate rather than on debate about criteria.

**The decision to terminate the migration was correct under uncertainty.** The completion estimate had wide error bars. Terminating a long-running rewrite is not risk-free — rollback carries its own I/O cost. The team reasoned explicitly about the tradeoff, documented it, and chose the bounded-risk path. The rollback completed in two minutes.

**Data plane isolation held completely.** No customer database instance or message queue broker experienced degradation. The architectural separation between control plane and data plane worked precisely as designed, and this is why the incident cost $700,000 rather than an order of magnitude more.

**No data was lost or corrupted.** The partial table rewrite rolled back cleanly. No customer configuration state was lost. Queued operations were preserved and drained by 8:45 p.m.

**Support triage was well-organized under load.** Tarrant established a dedicated tracking tag within twelve minutes of the first ticket cluster, batched customer responses, and maintained a running impact summary that fed the status updates. Support identified the incident nineteen minutes before the paging system did, and Tarrant's 2:34 p.m. and 2:47 p.m. escalation attempts were correct actions that failed for want of a defined channel.

**Recovery execution after the thundering herd was disciplined.** Once the herd was identified, the team moved to staged cohort recovery with defined intervals and health gates and did not deviate under pressure to move faster. Recovery from 4:41 p.m. onward proceeded without further setback.

**The incident channel record was thorough.** Timestamps, reasoning, and decisions were captured in enough detail to reconstruct this timeline without significant gaps. This document exists in its present form because of that discipline.

---

## 7. What Did Not Work

**Detection.** Forty-seven minutes of complete organizational blindness to a 71% error rate is the single most alarming fact in this document. Two independent configuration defects — a widened evaluation window and an unexpired suppression rule — combined in a way no one was positioned to notice. We do not currently test whether our alerts work.

**Alert delivery verification.** The replication-lag alert fired correctly into a void. We had no way to know.

**Triage information architecture.** The default incident dashboard presented the dimension most likely to mislead and buried the dimension that would have resolved the question in five minutes.

**Hypothesis discipline.** A reasonable hypothesis survived twenty-two minutes past its disconfirming evidence because nothing in our process required it to be defended, falsified, or time-boxed.

**Blast radius control in remediation tooling.** A single command restored the outage to near-peak severity for seventy-one minutes. The tool did what it was asked. It should not have been able to.

**Capacity relationship documentation.** The dependency between fleet size and metadata store connections was documented once in 2025 and never revisited as the fleet more than doubled.

**Runbook currency.** Nine of twenty-three runbooks contain broken references. The failover runbook's stale command removed an option from consideration at a decision point.

**Customer communication timeliness.** Ninety-nine minutes between customer impact and public acknowledgment. Two of four cancellations cite this specifically. This is the failure with the clearest link to revenue loss.

**Risk accounting in planning.** Three deferrals, each locally rational, aggregated into an unexamined and ultimately realized risk. Our planning process has no memory.

---

## 8. Lessons

**Alerts are code and decay like code.** We treat alert definitions as configuration set once and forgotten. Both detection failures were the residue of past changes — a window widened for a resolved problem, a suppression written for a completed freeze. Alerting requires the same lifecycle discipline as production software: testing, expiry, and periodic verification.

**Optional safety controls are not controls.** The 23%-versus-99.4% completion gap settles the question. Any checklist item that exists to prevent harm must be required and machine-validated.

**Version-specific behavior must be encoded in tooling, not in memory.** Every human in the review chain held a correct mental model of PostgreSQL that did not apply to the cluster in question. Humans cannot be expected to carry per-cluster version exceptions. The tooling must carry them.

**Deferral decisions need risk statements that persist.** Each deferral was defensible in isolation. What was missing was any artifact recording that this was the third deferral and what the accumulating exposure was. Risk that is not written down does not survive a planning cycle.

**Hypotheses need designated adversaries.** Under time pressure, in a hierarchy, a hypothesis stated by the incident commander is very difficult to challenge. The structure must supply the challenge rather than relying on individual courage.

**Remediation is change, and change under pressure deserves more caution, not less.** The fleet restart was the correct action executed without regard to blast radius, during the period when our judgment was most degraded by stress and our tolerance for further failure was lowest.

**Speed of acknowledgment beats precision of acknowledgment.** Customers who cancelled did not cite the outage's length. They cited the silence. "We are investigating a problem" published at 3:05 p.m. would have cost nothing and been worth more than the carefully accurate notice published at 3:53 p.m.

---

## 9. Action Items

Priority: **P0** — complete before next scheduled migration; **P1** — within 30 days; **P2** — within 90 days.

### 9.1 Detection and Alerting

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| A-01 | Audit all 214 production alert definitions for evaluation window appropriateness. Any alert with a page-severity action must use a window ≤ 5 min. Publish audit results. | Priyanka Deshmukh | 2027-03-20 | P0 |
| A-02 | Require mandatory expiry timestamps on all alert suppression rules, maximum 14 days, with automatic re-enable and notification to the rule author. | Priyanka Deshmukh | 2027-03-27 | P0 |
| A-03 | Build a suppression status dashboard showing all active suppressions with author, reason, and expiry. Include in weekly ops review. | Ines Vardanyan | 2027-04-10 | P1 |
| A-04 | Implement synthetic alert verification: fire each page-severity alert into a test path monthly and confirm delivery and acknowledgment. Alerts failing verification are flagged as broken. | Ines Vardanyan | 2027-05-15 | P1 |
| A-05 | Audit all alert destinations against live Slack channels, PagerDuty services, and email lists. Remediate all broken routes. | Priyanka Deshmukh | 2027-03-20 | P0 |
| A-06 | Add pre-merge validation to the alerting repository rejecting any alert whose destination does not resolve to an active target. | Ines Vardanyan | 2027-04-24 | P1 |
| A-07 | Add a control-plane availability alert independent of the error-rate alert, using synthetic probes against a canonical API operation, 60-second window, separate paging path. | Theo Almeida | 2027-04-17 | P1 |

### 9.2 Database Platform

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| B-01 | Complete Compass PostgreSQL major-version upgrade to version 15. Full plan with rollback procedure delivered by 2027-04-03; execution complete by 2027-06-05. | Sofia Grigoryan | 2027-06-05 | P0 |
| B-02 | Implement automated migration linting: reject any migration containing a full-table-rewrite operation against a table exceeding 10 million rows on the target cluster's actual major version. | Sofia Grigoryan | 2027-04-10 | P0 |
| B-03 | Make all migration checklist fields required with machine validation. Remove the "optional" designation from the checklist template entirely. | Sofia Grigoryan | 2027-03-20 | P0 |
| B-04 | Add a mandatory pre-flight dry run of every migration against a production-sized shadow copy of the target table, reporting measured lock duration. Merge blocked without a passing dry-run artifact. | Theo Almeida | 2027-05-08 | P1 |
| B-05 | Implement a lock-duration circuit breaker: any DDL statement holding ACCESS EXCLUSIVE on a Compass table for more than 45 seconds is automatically terminated and paged. | Sofia Grigoryan | 2027-04-24 | P1 |
| B-06 | Add lock waits, longest-running transaction, and replication lag to the primary control plane triage dashboard as first-class panels. | Priyanka Deshmukh | 2027-04-03 | P1 |
| B-07 | Relocate the migration maintenance window to 6:00–8:00 a.m. Tuesdays and Thursdays with a defined on-call staffing model. Document the tradeoff analysis. | Sofia Grigoryan | 2027-05-01 | P1 |

### 9.3 Remediation Tooling and Capacity

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| C-01 | Add a hard concurrency ceiling to fleet restart tooling: maximum 10% of fleet per wave, minimum 90-second inter-wave interval, no override without two-person approval. Remove the unbounded `--emergency` path. | Theo Almeida | 2027-04-03 | P0 |
| C-02 | Add a pre-execution impact summary to restart tooling showing projected connection demand against all downstream capacity limits, requiring explicit confirmation when demand exceeds 70% of any limit. | Theo Almeida | 2027-05-01 | P1 |
| C-03 | Raise metadata store `max_connections` to 12,000 and implement connection pooling with a proxy layer to decouple instance count from backend connections. | Sofia Grigoryan | 2027-05-22 | P1 |
| C-04 | Document all fleet-size-to-downstream-capacity relationships in a capacity dependency register. Add automated quarterly validation that current fleet size remains within documented limits. | Theo Almeida | 2027-06-12 | P2 |
| C-05 | Add startup jitter of 0–45 seconds randomized per instance to control plane connection establishment. | Theo Almeida | 2027-04-17 | P1 |

### 9.4 Incident Response Process

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| D-01 | Add a mandatory "hypothesis and falsification" step to SEV-1 process: the incident commander states the working hypothesis and what observation would disprove it. Both recorded in channel. | Priyanka Deshmukh | 2027-04-10 | P1 |
| D-02 | Introduce a "Devil's Advocate" role for all SEV-1 incidents, assigned to someone other than the commander, responsible for challenging the working hypothesis at 20-minute intervals. Add to training. | Oliver Baptiste | 2027-05-01 | P1 |
| D-03 | Add a mandatory 30-minute hypothesis checkpoint: if the working hypothesis has not produced improvement, the commander must formally re-derive from evidence and consider at least two alternatives. | Priyanka Deshmukh | 2027-04-10 | P1 |
| D-04 | Audit all 23 platform runbooks for command, hostname, and path validity. Remediate all broken references. | Sofia Grigoryan | 2027-05-15 | P1 |
| D-05 | Establish a quarterly runbook verification exercise in which each runbook is executed in staging. Runbooks unverified for two consecutive quarters are marked untrusted in the index. | Sofia Grigoryan | 2027-06-30 | P2 |
| D-06 | Add support ticket velocity as an automated paging signal: 15 tickets tagged to a single service within 10 minutes pages the service on-call. | Malik Tarrant | 2027-04-17 | P1 |
| D-07 | Define a monitored escalation channel for support-to-engineering escalation with an on-call rotation and a documented 5-minute response SLA. | Malik Tarrant | 2027-04-03 | P0 |

### 9.5 Customer Communication

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| E-01 | Establish a 10-minute status page SLA: any SEV-1 requires a public "investigating" notice within 10 minutes of declaration, publishable without engineering sign-off. | Jun-ho Park | 2027-03-27 | P0 |
| E-02 | Create pre-approved status page templates for investigating, identified, monitoring, and resolved states requiring only service name and impact scope. | Jun-ho Park | 2027-03-27 | P0 |
| E-03 | Add the Customer Reliability on-call to the automatic SEV-1 page. Communications lead joins at declaration, not on request. | Priyanka Deshmukh | 2027-03-20 | P0 |
| E-04 | Establish a mandatory 30-minute status update cadence for all SEV-1 incidents, enforced by an automated reminder in the incident channel. | Jun-ho Park | 2027-04-10 | P1 |
| E-05 | Add data plane status as a distinct component on the public status page so customers can see that provisioned resources remain healthy during control plane incidents. | Jun-ho Park | 2027-05-08 | P1 |
| E-06 | Conduct structured outreach to all 2,140 affected customers with a technical summary and remediation commitments. Prioritize the 89 accounts exceeding $50,000 ARR. | Jun-ho Park | 2027-04-03 | P0 |

### 9.6 Planning and Risk Governance

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| F-01 | Institute a deferred-risk register. Any infrastructure maintenance deferred for revenue work requires a written risk statement carried into the next planning cycle. Second deferral requires director sign-off; third requires VP sign-off. | Oliver Baptiste | 2027-04-30 | P1 |
| F-02 | Reserve 20% of platform engineering capacity per quarter for maintenance, upgrades, and reliability work, protected from reallocation without VP approval. | Oliver Baptiste | 2027-04-30 | P1 |
| F-03 | Complete a version-currency audit of all production stateful systems. Any system more than one major version behind requires a documented upgrade plan with a committed date. | Sofia Grigoryan | 2027-05-29 | P1 |
| F-04 | Present this postmortem and the remediation program to the executive team and the board technology committee. | Oliver Baptiste | 2027-04-15 | P1 |

### 9.7 Verification

| ID | Action | Owner | Due | Priority |
|---|---|---|---|---|
| G-01 | Conduct a game day exercise simulating a Compass lock event, verifying detection within 5 minutes, correct diagnosis within 15, and status page update within 10. | Priyanka Deshmukh | 2027-06-26 | P2 |
| G-02 | Conduct a game day exercise simulating fleet-wide restart under load, verifying that concurrency controls prevent connection pool exhaustion. | Theo Almeida | 2027-07-10 | P2 |
| G-03 | Publish a 90-day progress report on all action items to the full engineering organization. | Oliver Baptiste | 2027-06-15 | P1 |

---

## 10. Appendix: Open Questions

The following were raised during review and remain unresolved. Each is tracked separately.

**Should the control plane degrade gracefully rather than fail?** During the outage, read-only operations that did not require `tenant_resource_index` also failed because they shared a connection pool. A partitioned pool architecture, or a read-only degraded mode, would have preserved a meaningful subset of functionality. Scoping assigned to Theo Almeida, due 2027-06-30.

**Is a single PostgreSQL cluster the right architecture for the control plane at 6,800 customers?** Compass is a single point of failure for all control plane operations. Sharding or functional decomposition would reduce blast radius at significant complexity cost. Architecture review scheduled for Q3 2027, owned by Sofia Grigoryan.

**Should customer SDK retry behavior be revisited?** Retry storms from aggressive client backoff configurations contributed measurably to the recovery tail between 6:02 and 7:04 p.m. Investigation assigned to Theo Almeida, due 2027-07-31.

**What is the appropriate service credit structure?** The $410,000 in credits reflects contractual SLA terms. Whether that structure appropriately reflects the value of control plane availability to customers — and whether it creates the right internal incentives — is a question for commercial and engineering leadership jointly. Owned by Oliver Baptiste, due 2027-06-30.

---

*This postmortem is blameless by policy and by conviction. The individuals named in this document acted competently and in good faith with the information available to them. Where this document identifies failure, it identifies failure of systems, tooling, process, and prioritization — all of which are ours collectively to repair.*
