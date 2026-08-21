# Incident Postmortem: Compass Control Plane Degradation — March 9, 2027

**Document status:** Final
**Incident ID:** INC-2027-0309-01
**Authored:** March 16, 2027
**Distribution:** Engineering leadership, SRE, Database Platform, Customer Reliability, Executive staff

---

## 1. Summary

On Tuesday, March 9, 2027, a routine schema migration against Compass — the PostgreSQL cluster that backs Meridian Stack's control plane — took an exclusive table lock that it was never expected to hold for more than a few seconds. It held that lock for the better part of an hour. The migration added a column with a default value to a 400-million-row table. On the PostgreSQL major version Compass was running, that operation requires rewriting the entire table under an `ACCESS EXCLUSIVE` lock. Compass had been scheduled for a major-version upgrade that would have eliminated this behavior; the upgrade had been deferred three consecutive quarters in favor of revenue-facing work.

The lock stalled control-plane API traffic for 6,800 customers' worth of provisioning, authentication, and management operations beginning at 2:14 p.m. Error rates crossed 5 percent within five minutes and 71 percent within 27 minutes, but the paging system did not notify an engineer until 3:01 p.m. — 47 minutes after the first error-rate breach — because the alert's 30-minute detection window overlapped a deploy-freeze suppression rule. Once paged, the incident commander correctly observed that failed requests were clustering in a single availability zone and, reasonably but incorrectly, spent 38 minutes pursuing a provider-network-event hypothesis before the database platform lead identified the blocking migration directly. The remediation — killing the migration and restarting the control-plane fleet — was itself undermined by a reconnection storm: 900 instances reconnecting simultaneously exhausted the metadata store's connection pool and added 71 minutes to the outage. Customer-facing communication lagged internal detection by nearly an hour, and the status page remained green for the first 90 minutes of a multi-hour outage.

The incident lasted 4 hours and 52 minutes, from 2:14 p.m. to 7:06 p.m. It affected 2,140 customers, failed 11.4 million API requests, and resulted in $410,000 in service credits and the cancellation of four accounts worth $290,000 in annual recurring revenue.

This postmortem covers five areas in detail: the detection gap between the error spike and the page, the provider misdiagnosis that consumed the first third of the response, the fleet restart that introduced a second failure mode, the delay in external communication, and the underlying organizational decisions — a deferred database upgrade, an optional checklist field, and alerting infrastructure that had silently decayed — that made all of the above possible. The intent of this document is to examine the systems, defaults, and decision points that produced this outcome, not to evaluate the individuals who operated within them.

---

## 2. Impact

| Metric | Value |
|---|---|
| Incident duration | 4 hours 52 minutes (2:14 p.m. – 7:06 p.m. ET) |
| Time to first page | 47 minutes |
| Time to correct root-cause identification | 98 minutes (2:14 p.m. – 3:52 p.m.) |
| Time to first external status update | 52 minutes after page (99 minutes into incident) |
| Customers affected | 2,140 of 6,800 (~31%) |
| Failed API requests | 11.4 million |
| Peak control-plane error rate | 71% |
| Service credits issued | $410,000 |
| Accounts cancelled within 30 days | 4 accounts, $290,000 ARR |
| Instances involved in fleet restart | 900 |
| Additional downtime caused by restart | 71 minutes |

The customer-facing impact was concentrated in control-plane operations: provisioning new database and message-queue instances, authenticating API clients, scaling existing clusters, and viewing account/billing state. The underlying data plane — customers' running databases and queues — remained available throughout; customers experienced this incident as an inability to manage their infrastructure, not as data loss or query downtime on their production workloads. That distinction did not prevent material business impact: four customers cited the incident specifically, and the multi-hour silence on the status page, as their reason for cancellation.

---

## 3. Timeline

All times Eastern, March 9, 2027, unless noted.

**2:14 p.m.** — A scheduled migration deploys an `ALTER TABLE ... ADD COLUMN ... DEFAULT` statement against a 400-million-row table in Compass. On the PostgreSQL major version Compass currently runs, this operation requires a full table rewrite performed under an `ACCESS EXCLUSIVE` lock, blocking all reads and writes to the table for the duration of the rewrite. The migration checklist's lock-duration risk field, marked optional, was left blank at review.

**2:16 p.m.** — Queries against the affected table begin queuing behind the lock. Control-plane services dependent on that table start timing out.

**2:19 p.m.** — Control-plane API error rate crosses 5 percent.

**2:22 p.m.** — Connection pools on dependent control-plane services begin saturating with queued requests waiting on the locked table.

**2:41 p.m.** — Control-plane API error rate reaches 71 percent. Customer support ticket volume begins climbing sharply.

**3:01 p.m.** — The error-rate alert fires and pages the on-call rotation for the first time — 47 minutes after the initial threshold breach. The alert is configured with a 30-minute rolling evaluation window; that window itself overlapped a suppression rule tied to an entry on the deploy-freeze calendar, delaying evaluation further. This is the first automated signal any engineer receives.

**3:06 p.m.** — Priyanka Deshmukh, staff site reliability engineer, acknowledges the page and assumes incident command.

**3:08 p.m.** — Initial triage shows failed requests clustering heavily in one availability zone.

**3:10 p.m.** — Based on the AZ clustering, the working hypothesis is set: a provider-side network event affecting a single zone. This hypothesis is consistent with the observed signal and with prior incidents of this shape.

**3:10 p.m. – 3:44 p.m.** — The team opens a ticket with the cloud provider, reviews provider status pages and internal network telemetry, and checks for corroborating signals (packet loss, latency, routing changes) in the affected zone. No direct check of database lock state or long-running queries is performed during this window; the runbook followed does not list lock inspection as an early diagnostic step for control-plane error spikes.

**3:44 p.m.** — Provider tooling and support show no active incident in the affected zone. The provider-network hypothesis is set aside.

**3:52 p.m.** — Sofia Grigoryan, who leads the database platform team, is looped in and queries `pg_stat_activity` and `pg_locks` directly on the Compass primary. She identifies the migration's `ALTER TABLE` statement holding an `ACCESS EXCLUSIVE` lock on the 400-million-row table for approximately 98 minutes at that point, blocking all dependent control-plane queries.

**3:53 p.m.** — Jun-ho Park, Director of Customer Reliability, posts the first external status page update, 52 minutes after the initial page and 99 minutes after the first customer-facing errors began. The status page had shown a fully operational state for the preceding 90 minutes.

**3:58 p.m.** — Incident command, with database platform, decides to terminate the migration process to release the lock rather than wait for the rewrite to complete, given uncertain remaining duration.

**4:02 p.m.** — The migration process is killed. The lock is released.

**4:05 p.m.** — To clear the backlog of queued connections and stuck application state across the control-plane fleet, the team restarts all control-plane service instances — approximately 900 instances — simultaneously.

**4:07 p.m.** — All 900 instances attempt to reconnect to the metadata store at once. The metadata store's connection pool, sized for steady-state traffic and not for a full-fleet cold start, saturates almost immediately. New connections begin failing; control-plane error rates, which had begun to recover after the lock was released, spike again.

**4:20 p.m.** — Oliver Baptiste, Vice President of Engineering, joins the incident call to help coordinate cross-team response and resourcing. Malik Tarrant continues running support ticket triage, which by this point has a substantial backlog from the preceding two hours.

**4:20 p.m. – 5:16 p.m.** — The team diagnoses the connection pool exhaustion, raises pool limits on the metadata store, and staggers the remaining reconnection attempts to avoid a repeat spike. This work adds 71 minutes to the incident beyond the point at which the original lock had been cleared.

**5:16 p.m.** — Metadata store connections stabilize. Control-plane error rates begin a sustained decline.

**5:45 p.m.** — Control-plane error rate falls below 5 percent.

**6:20 p.m.** — Error rate returns to baseline (under 0.5 percent). Monitoring continues to confirm stability before declaring resolution.

**7:06 p.m.** — Incident declared resolved. Total duration: 4 hours 52 minutes from first customer impact to full resolution.

---

## 4. Root Cause

The root cause of the outage was a schema migration that took a full-table exclusive lock on a 400-million-row table for an extended duration, because Compass was running a PostgreSQL major version that does not support lock-free addition of a defaulted column.

In current PostgreSQL major versions, adding a column with a default value is a fast, metadata-only operation: the engine records the default and applies it lazily on read, without rewriting existing rows or holding a long-lived exclusive lock. On the version Compass was running, the same statement instead triggers a full rewrite of every row in the table, and PostgreSQL must hold an `ACCESS EXCLUSIVE` lock — the strongest lock mode, blocking all reads and writes to the table, including by processes that only want a row lock — for the entire duration of that rewrite. On a table of 400 million rows, that rewrite took on the order of an hour and a half before it was manually terminated.

Because Compass is the control plane's own database, the tables affected by this lock were not customer data tables but the tables that Meridian Stack's provisioning, authentication, and management services query on every request. A lock that would be a brief, invisible blip on an ordinary application table became, on this table, a full stop for a third of the customer base's ability to manage their infrastructure.

The major-version upgrade that would have eliminated this failure mode had been identified, scoped, and scheduled, and had been deferred in each of the three preceding planning quarters in favor of work with more direct, nearer-term revenue impact. This was not a single oversight; it was a recurring prioritization decision made three times, by people weighing a known but diffuse future risk against concrete near-term commitments — a trade-off that is common in engineering organizations and that, in this instance, resolved in favor of an outage.

---

## 5. Contributing Factors

**5.1 The lock-duration checklist field was optional.** Meridian Stack's migration review checklist includes a question intended to flag exactly this class of risk — how long a migration is expected to hold locks, and on what size of table. That field is marked optional in the checklist tool, and the migration that caused this incident shipped with it blank. A required field with an enforced answer, or an automated check that flags `ALTER TABLE` statements against tables above a row-count threshold, would have surfaced this risk before deploy rather than during an outage.

**5.2 The error-rate alert's detection window overlapped deploy-freeze suppression.** The alert that eventually paged on-call uses a 30-minute rolling evaluation window, and that window's suppression logic is keyed to entries on the deploy-freeze calendar — a mechanism built to prevent false pages during planned deploy activity, when transient error blips are common and expected. This migration was logged on that calendar. The same suppression designed to reduce noise around planned changes suppressed a genuine, escalating signal for a large share of the 47 minutes between the first error-rate breach and the first page. The alert's own window added additional delay on top of that suppression.

**5.3 The incident runbook did not direct responders to check for locks early.** The control-plane troubleshooting runbook, as followed during this incident, leads with infrastructure-level checks — provider status, network telemetry, zone health — before database-internal checks such as active queries and lock state. Given that error signals clustered by availability zone, the provider hypothesis was a reasonable first read of the runbook's guidance. The runbook did not include a step to check for long-running locks or blocking queries on Compass early in the diagnostic sequence, despite Compass being the single dependency underlying nearly all control-plane functionality.

**5.4 The control-plane fleet had no staggered restart procedure.** When the team needed to clear queued connections and stuck state after the lock was released, the only available remediation was a full fleet restart. No staggered, jittered, or canary-first restart procedure existed for the control-plane service, and the metadata store's connection pool had not been load-tested against a full-fleet simultaneous reconnect. The result was a second, self-inflicted outage layered on top of the first.

**5.5 The replication-lag alert had been silently broken since January.** A separate alert intended to catch replication lag on Compass — which could have provided an earlier, independent signal that something was wrong with the database — routed to a Slack channel that was archived in January as part of a workspace cleanup. The alert continued firing; it simply had no destination that anyone was watching. Its failure was not discovered during this incident and was only found during postmortem review, meaning it had provided zero effective monitoring coverage for over two months without anyone's knowledge.

**5.6 The failover runbook referenced a command removed in 2025.** Although failover was not ultimately exercised in this incident, the runbook that would have guided that decision was found during review to name a command-line tool retired two years prior. Had the incident progressed to requiring failover, responders would have discovered this gap in real time, under pressure, rather than during a calm review. This points to a broader pattern: operational runbooks were not being validated against the infrastructure they describe as that infrastructure changed.

**5.7 Status page updates were gated on confirmed root cause rather than on customer impact.** The first external communication went out 52 minutes after the page and roughly 99 minutes after customers began experiencing errors. The practice that produced this delay was not a single person's judgment call but the informal norm that public status communication should wait until the team has something concrete and correct to say. That norm serves accuracy well and customers poorly when the diagnostic phase itself runs long, as it did here.

---

## 6. What Worked and What Did Not

**What worked:**

- Once the correct diagnostic step was taken — querying `pg_locks` and `pg_stat_activity` directly against the Compass primary — root cause was identified quickly and unambiguously. The database platform team's familiarity with Compass's internals meant there was no ambiguity once the right question was asked.
- The decision to kill the migration rather than wait for the rewrite to complete was made promptly once the lock was found, avoiding an open-ended wait of uncertain length.
- Cross-team escalation functioned as intended: engineering leadership joined within 20 minutes of the page becoming a multi-team effort, and support triage ran in parallel with technical remediation rather than blocking on it, keeping the ticket backlog from growing unmanageably during the diagnostic phase.
- The team correctly diagnosed the second failure mode — connection pool exhaustion from the simultaneous restart — quickly enough to apply a targeted fix (raised pool limits, staggered reconnects) rather than repeating the same restart and compounding the problem a third time.

**What did not work:**

- Detection was slow by nearly 50 minutes due to the interaction between a rolling alert window and deploy-freeze suppression logic that were each individually reasonable but combined to blind the system precisely when a deploy-related change was the actual cause of the problem.
- The first diagnostic hypothesis was investigated for 38 minutes without a cheap, fast check (querying for long-running locks) that would have redirected the investigation almost immediately. The AZ clustering of errors was a real signal, but it was consistent with more than one cause, and the runbook did not prompt responders to rule out the cheaper, faster-to-check cause first.
- The remediation for the original problem introduced a new, distinct outage. The fleet restart was executed without a mechanism to control the rate or order of reconnection, and the dependency it stressed — the metadata store's connection pool — had not been sized or tested for that load pattern.
- External communication lagged internal awareness substantially. For 90 minutes, the status page told customers everything was fine while nearly a third of them were experiencing failures. This gap shaped customer sentiment independent of the technical resolution.
- Two pieces of safety infrastructure — the replication-lag alert and the failover runbook — had quietly stopped being reliable months and years, respectively, before this incident, and nothing in the organization's processes caught either decay before it mattered.

---

## 7. Action Items

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Complete the deferred Compass PostgreSQL major-version upgrade, eliminating full-rewrite behavior for defaulted-column additions | Sofia Grigoryan (Database Platform) | May 15, 2027 |
| 2 | Make the migration checklist's lock-duration/lock-mode field required, and add automated static analysis to flag `ALTER TABLE` statements against tables above 10 million rows for mandatory review | Priyanka Deshmukh (SRE) | April 6, 2027 |
| 3 | Audit all production alert routing destinations for validity (channel existence, membership, ownership); establish quarterly recurring audit | Priyanka Deshmukh (SRE) | April 13, 2027 |
| 4 | Redesign error-rate alert suppression so deploy-freeze entries reduce alert sensitivity rather than eliminate paging outright, and decouple the rolling evaluation window from freeze-calendar logic | SRE on-call tooling lead (reporting to Priyanka Deshmukh) | April 20, 2027 |
| 5 | Add "check `pg_locks` / `pg_stat_activity` on Compass" as the first diagnostic step in the control-plane incident runbook, ahead of infrastructure/provider checks | Priyanka Deshmukh (SRE) | April 6, 2027 |
| 6 | Design and implement a staggered/jittered restart procedure for the control-plane fleet; load-test the metadata store connection pool against a full-fleet simultaneous reconnect scenario | Sofia Grigoryan (Database Platform) | May 1, 2027 |
| 7 | Review and correct the failover runbook end-to-end against current tooling; establish a semiannual runbook validation exercise for all tier-1 runbooks | Sofia Grigoryan (Database Platform) | April 27, 2027 |
| 8 | Define a time-to-first-status-page-update SLA (target: 15 minutes from page) decoupled from confirmed root cause, and update status page process accordingly | Jun-ho Park (Customer Reliability) | April 13, 2027 |
| 9 | Establish an ongoing quarterly technical-debt review that explicitly re-evaluates deferred infrastructure upgrades with known risk, with a standing report to engineering leadership | Oliver Baptiste (VP Engineering) | Q3 2027 planning cycle (July 2027) |
| 10 | Conduct customer outreach and account-risk review for the 2,140 affected customers, with prioritized follow-up for accounts flagging cancellation risk | Jun-ho Park (Customer Reliability) with Malik Tarrant (Support) | April 6, 2027 |

---

## 8. Closing Note

This incident was the product of several individually defensible decisions and a small number of quietly decayed systems arriving in the same afternoon: a deferred upgrade whose risk had been accepted three times in a row, a checklist field that made a critical risk question optional, an alerting rule whose interaction with deploy-freeze logic no one had traced end to end, a runbook ordered around a plausible but not cheapest-to-check hypothesis, a restart procedure never tested at full-fleet scale, and two pieces of safety tooling — an alert routed to an archived channel and a runbook citing a retired command — that had stopped working without anyone noticing. None of these was, by itself, sufficient to produce a five-hour outage. Together, they were.

## 9. Appendix A: Supporting Technical Detail

### 9.1 The Locking Mechanics in Detail

For engineers reviewing this incident who want the underlying database behavior rather than the summary: prior to PostgreSQL 11, adding a column with a `DEFAULT` clause required the database to write the default value into every existing row of the table as part of the `ALTER TABLE` statement. This is because the on-disk row format at that time had no mechanism to represent "this column is absent from the stored row; substitute this default at read time." Every row had to be physically rewritten to include the new column's value before the statement could complete.

Because the rewrite touches every row, and because other transactions must not be able to read a half-rewritten table, PostgreSQL takes the strongest lock in its hierarchy — `ACCESS EXCLUSIVE` — for the duration. This lock is incompatible with every other lock mode, including the lightweight `ACCESS SHARE` lock taken by a plain `SELECT`. Any query touching the table, no matter how simple, queues behind the `ALTER TABLE` until it either completes or is terminated.

Versions from PostgreSQL 11 onward changed the row format so that a new column with a constant default can be recorded as metadata on the table itself, with the actual default substituted lazily whenever an old-format row is read. This makes the `ALTER TABLE ADD COLUMN ... DEFAULT` statement near-instantaneous regardless of table size, because no existing row needs to be touched at add-time. Compass's deferred upgrade meant this optimization was never available to the migration in question. The migration author had reasonable grounds to expect the operation to be fast, because on any currently supported PostgreSQL version, it would have been; the operation is only slow and lock-heavy on the version Compass happened to still be running.

This is worth stating plainly because it reframes part of the incident: the migration itself was written in a way that would be safe on a modern PostgreSQL major version. The unsafe condition was entirely a property of which major version Compass was on at the time, which returns the analysis to the deferred upgrade as the structural root cause rather than to any error in migration authorship.

### 9.2 Connection Pool Exhaustion During the Restart

The metadata store fronting the control-plane fleet maintains a fixed-size connection pool per backend node, sized against steady-state connection churn — new instances rolling in during ordinary deploys, at a rate of roughly 20–40 instances over several minutes during a typical release. The pool had never been exercised against 900 instances reconnecting within the same few seconds, because no prior operational scenario had required restarting the entire fleet simultaneously; ordinary deploys are rolling by design specifically to avoid this pattern.

When the pool saturated, new connection attempts began failing with pool-exhaustion errors rather than queuing, which meant instances that failed to connect on their first attempt immediately retried, compounding the connection pressure rather than backing off. The retry logic in the control-plane service's client library did not include jitter or exponential backoff tuned for this failure mode; it was tuned for transient network blips, not for a sustained pool-exhaustion condition affecting the entire fleet at once. This is the specific mechanism by which a five-minute intended remediation step turned into 71 additional minutes of degraded service.

### 9.3 Alert Suppression Logic

The deploy-freeze calendar is a shared scheduling system that engineering teams use to declare windows during which they intend to make production changes, primarily so that other teams can avoid overlapping risky changes and so that the on-call rotation has context if error rates move during a declared window. At some point after this suppression feature was introduced, it was extended so that any alert with a rolling evaluation window would not fire while a relevant calendar entry was active, on the theory that transient errors during a declared deploy window are expected and would otherwise generate noise. This extension was not documented as a formal design decision; it was added incrementally and was not revisited when the error-rate alert's evaluation window was later changed from 10 minutes to 30 minutes, which widened the blind period correspondingly. No single change here was unreasonable in isolation; the combination had not been tested against a scenario where the declared deploy window's own change was the cause of a genuine, escalating incident.

---

## 10. Appendix B: Customer Communication Log

| Time | Channel | Content |
|---|---|---|
| 3:53 p.m. | Status page | Initial post acknowledging "elevated error rates affecting control-plane operations for a subset of customers," investigation in progress |
| 4:22 p.m. | Status page | Update noting root cause identified as a database migration issue, remediation in progress |
| 4:40 p.m. | Status page | Update acknowledging that remediation efforts introduced additional instability, apologizing for extended impact |
| 5:20 p.m. | Status page | Update noting recovery in progress, error rates declining |
| 6:25 p.m. | Status page | Update confirming error rates at baseline, monitoring continuing before full resolution declared |
| 7:10 p.m. | Status page | Final update declaring incident resolved, committing to a public postmortem summary |
| 7:15 p.m. | Direct email | Sent to all 2,140 affected accounts summarizing impact and service credit process |
| March 11 | Direct outreach | Account management follow-up initiated for the top 50 affected accounts by ARR |
| March 14 | Public summary | Abbreviated public-facing incident summary published, referencing this internal postmortem |

The gap between the first customer-visible error (2:16 p.m.) and the first status page update (3:53 p.m.) — roughly 97 minutes — is the single largest driver of customer sentiment identified in post-incident account interviews, independent of the technical resolution time. Three of the four cancelling accounts specifically referenced "finding out from our own monitoring before Meridian told us anything" in cancellation conversations logged by the account management team.

---

## 11. Appendix C: Verification of Action Item Completion

To close the loop on this incident, the following verification steps are attached to the action items in Section 7 and will be checked at the engineering leadership review scheduled for June 1, 2027:

- **Item 1 (Compass upgrade):** Verification requires a successful staging-environment migration mirroring the March 9 schema change, confirmed to complete without an `ACCESS EXCLUSIVE` lock exceeding 5 seconds, run against a table of at least 400 million rows.
- **Item 2 (checklist field):** Verification requires a sample audit of the next 20 migrations submitted after April 6, confirming the lock-duration field is populated and, where flagged, has an attached sign-off from the database platform team.
- **Item 3 (alert routing audit):** Verification requires a written audit report listing every production alert, its destination, and a confirmation timestamp that the destination was tested with a synthetic firing within the prior 30 days.
- **Item 4 (alert/suppression redesign):** Verification requires a documented design review, sign-off from both the SRE tooling lead and the on-call rotation, and a game-day exercise simulating an incident during a declared freeze window to confirm paging still occurs.
- **Item 5 (runbook reordering):** Verification requires the updated runbook document and a tabletop walkthrough with at least two engineers who did not author the change.
- **Item 6 (staggered restart):** Verification requires a documented load test of the metadata store connection pool under a simulated full-fleet reconnect, with results attached to the action item record.
- **Item 7 (failover runbook):** Verification requires a live failover drill in staging, executed by an engineer other than Sofia Grigoryan, following the corrected runbook without deviation.
- **Item 8 (status page SLA):** Verification requires the published SLA document and confirmation that the next declared-severity incident, regardless of cause, receives a first update within the 15-minute target.
- **Item 9 (technical debt review):** Verification requires a standing agenda item and a written report delivered to engineering leadership at the Q3 2027 planning session.
- **Item 10 (customer outreach):** Verification requires a completed outreach log for all 2,140 affected accounts and a summary of retention outcomes delivered to the executive team.

---

## 12. Appendix D: Glossary

**ACCESS EXCLUSIVE lock** — The strongest lock mode in PostgreSQL's lock hierarchy; incompatible with all other lock modes, meaning no other transaction may read from or write to the locked table while it is held.

**Control plane** — The set of services responsible for provisioning, authenticating, configuring, and managing customer database and message queue instances, as distinct from the data plane, which is the customers' running instances themselves.

**Deploy freeze calendar** — An internal scheduling tool used to declare windows of planned production change, originally intended for change coordination and later extended into alert-suppression logic.

**Metadata store** — The internal service used by control-plane instances to register presence, discover peers, and coordinate configuration state; distinct from Compass, which stores customer-facing control-plane data such as account and provisioning records.

**Rolling evaluation window** — An alerting configuration in which a metric must remain above (or below) a threshold for a specified duration before an alert is considered triggered, used to reduce false positives from brief spikes.

---

*End of document.*

## 13. Appendix E: Related Incident History

This is not the first incident in which Compass's deferred upgrade or its migration process has surfaced as a contributing factor, and the review board considered that history relevant context for evaluating why the March 9 outage was allowed to occur despite known risk.

**INC-2026-1103** (November 3, 2026): A migration adding an index to a mid-sized Compass table caused a 12-minute period of elevated write latency. The postmortem for that incident recommended, as an action item, "evaluate lock behavior for all Compass schema changes against table size before deploy." That recommendation was logged but not implemented as an enforced check; it became the informal expectation reflected in the checklist's now-optional lock-duration field rather than a required gate.

**INC-2026-0714** (July 14, 2026): A planning review ahead of Q3 2026 roadmap commitments deferred the Compass major-version upgrade for the first time, citing capacity constraints against a customer-facing feature commitment. The deferral was reviewed and re-approved in the Q4 2026 and Q1 2027 planning cycles, each time citing similar tradeoffs. No formal risk acceptance document was produced at any of the three deferrals; the decision was made in planning discussions and reflected only in roadmap tracking, not in a risk register visible to the incident response teams who would eventually be paged.

**INC-2025-0822** (August 22, 2025, prior to the current on-call rotation's tenure): A control-plane fleet-wide restart during a different incident produced a similar, smaller-scale connection pool saturation event against the same metadata store. That incident's postmortem is on file but was not referenced during the March 9 response; none of the responders present on March 9 had been party to the 2025 incident, and the recommendation from that postmortem — to implement staggered restart logic — appears as an open action item in that document, never closed, and was not surfaced by any automated tracking of overdue postmortem action items.

The review board's specific observation here is not that any individual failed to recall a prior incident, but that the organization had no mechanism ensuring that an unresolved action item from a 2025 postmortem remained visible and prioritized until closed. The same gap — staggered restart logic — appears as Action Item 6 in this document, nineteen months after it was first identified.

---

## 14. Appendix F: Cost and Risk Accounting

For the purposes of prioritization against other engineering work, the review board compiled the following accounting of this incident's total cost, alongside the estimated cost of the deferred work that would have prevented it.

**Direct incident costs:**
- Service credits issued: $410,000
- Estimated annual recurring revenue lost to cancellation: $290,000
- Engineering hours spent in incident response (approximately 14 engineers across 4 hours 52 minutes, plus approximately 40 additional hours of same-week follow-up triage and customer outreach): estimated at 105 person-hours
- Support triage hours during and immediately after the incident: estimated at 60 person-hours
- Postmortem authorship, review, and action item planning: estimated at 25 person-hours

**Estimated cost of the deferred preventive work:**
- The Compass major-version upgrade, as scoped in the Q3 2026 planning cycle prior to its first deferral, was estimated at approximately 3 engineer-weeks of dedicated database platform time, plus a coordinated maintenance window requiring customer notice.
- Across three deferrals, the cumulative estimated cost of the delayed work did not change materially; the scope of the upgrade itself was stable. What changed each quarter was the estimated opportunity cost of not doing other work in its place.

The review board notes this comparison not to argue that the upgrade should always take precedence over revenue-facing work in the abstract, but to make the specific tradeoff visible in the same terms on both sides. In each of the three planning cycles where the deferral was decided, the cost of deferring was represented only as delayed customer feature delivery being avoided; the risk being carried forward had no comparably concrete figure attached to it, because no incident had yet occurred to attach one. Action Item 9, establishing a standing technical-debt review with reporting to engineering leadership, is intended specifically to close this asymmetry — ensuring that deferred infrastructure risk is represented in planning discussions with the same specificity as the revenue-facing work it is weighed against, rather than being visible only in retrospect.

---

*End of document.*
