# Postmortem: Baseline WMS Upgrade Failure and Pick Accuracy Collapse
### Tannery Row Logistics — Rome, New York Fulfillment Center

**Incident Window:** November 21 – December 6, 2026
**Document Status:** Final
**Prepared For:** Executive Leadership, Operations, Information Technology, Client Services
**Classification:** Internal — Incident Review

---

## 1. Summary

Over the weekend of November 21–22, 2026, Tannery Row Logistics upgraded its warehouse management system, Baseline, from version 9.2 to version 11.0 at its 900,000-square-foot Rome, New York fulfillment center. The cutover window had been moved from an originally planned May date at the vendor's request. The technical upgrade itself completed without incident at 4:10 a.m. Sunday, November 22. A location master data transformation run during that upgrade silently stripped the aisle prefix from 61,000 of the facility's 214,000 pick locations — roughly 28 percent of all bins. Scanner validation logic continued to function, but it was now checking scans against malformed location records, so it approved picks from the wrong bins without raising an error.

The defect did not announce itself. Pick accuracy, normally 99.6 percent, began degrading as soon as full production picking resumed Monday morning, November 23, but the facility's quality reporting ran on a two-shift lag and the team responsible for triaging the exception queue had been unstaffed since a transfer in September. By Monday afternoon accuracy had fallen to 91.2 percent — an eightfold increase in the error rate — with no one positioned to see it, own it, or act on it. The defect was not escalated until 11:20 a.m. Tuesday, November 24, when a brand's returns team physically discovered 900 wrong items in a single outbound trailer.

The initial response misdiagnosed the problem as a scanner firmware defect from a push the previous week and spent nine hours executing a fleet-wide rollback that had no effect on the underlying issue. With accuracy still degraded and Black Friday volume approaching, the facility moved to full paper pick sheets on Wednesday, November 25, which stopped the bad data from causing mis-shipments but cut throughput by 60 percent and began building a backlog. The location master defect was correctly identified early Thursday morning, November 26, by comparing the live location table against a pre-upgrade export. Clearing the resulting 214,000-order backlog took 11 days, spanning the facility's highest-volume week of the year.

The direct, quantified cost of the incident — expedited freight, service credits, and 38,000 wrong or late orders — exceeded $2.4 million, and one client with a $9 million annual contract gave notice during the recovery. This postmortem examines the upgrade decision, the detection gap, the scanner misdiagnosis, the paper-picking tradeoff, and the testing program that allowed a data transformation defect of this scale to reach production undetected.

---

## 2. Impact

| Metric | Baseline / Target | During Incident | Delta |
|---|---|---|---|
| Pick accuracy | 99.6% | 91.2% (Mon. afternoon) | Error rate rose from 0.4% to 8.8% (~22x) |
| Daily throughput | 78,000 units/day | 31,000 units/day (paper picking) | -60% |
| Affected pick locations | — | 61,000 of 214,000 | 28.5% of all bins |
| Time to escalation | — | 31 hours from first live production shift under v11.0 | — |
| Scanner rollback duration | — | 9 hours, fleet-wide | No effect on root cause |
| Backlog at peak | — | 214,000 orders | Coincided with Black Friday ramp |
| Time to clear backlog | — | 11 days | — |
| Orders shipped wrong or late | — | 38,000 | — |
| Expedited freight cost | — | $1.8 million | — |
| Client service credits issued | — | $640,000 (2 clients) | — |
| Contract value under notice | — | $9 million (1 client) | — |
| Parallel validation window (planned vs. actual) | 2 weeks | 4 days | -71% |
| Regression suite currency | Last updated at v9.0 | Unchanged through v9.2 → v11.0 | Two major versions stale |

**Total quantified direct cost:** approximately $2.44 million (expedited freight plus service credits), excluding the at-risk $9 million contract, labor cost of the paper-picking period, and unrecovered brand trust.

---

## 3. Timeline

All times local (Eastern), Rome, New York facility.

### Pre-Incident

**Q1 2026 (date not specified) — Upgrade originally scheduled for May 2026.**
The version 9.2-to-11.0 upgrade was planned for a May cutover window, selected to sit well ahead of peak season and allow a full validation and stabilization period before Black Friday.

**Spring 2026 — Cutover date moved to November 21 at vendor request.**
Baseline's vendor requested the reschedule. The new date placed the cutover five days before Thanksgiving and six days before Black Friday, compressing the available stabilization window from roughly six months to five days.

**September 2026 — Exception queue owner transferred out of role.**
The associate responsible for triaging the daily pick-accuracy exception queue was transferred to another team. The role was not backfilled. The queue continued to generate entries; no one was assigned to review them.

### Cutover Weekend

**Saturday, November 21, ~10:00 p.m. — Cutover window opens.**
Baseline version 11.0 installation and data migration begin, following a cutover runbook supplied by the vendor as a template and not substantially modified for Tannery Row's location schema or scale.

**Sunday, November 22, 4:10 a.m. — Upgrade completes.**
Version 11.0 is live. Post-upgrade smoke tests are run against aggregate counts (total locations, total SKUs, total open orders) rather than scan-level location validation. Counts reconcile; the upgrade is marked successful. The location master transformation has, without error or warning, dropped the aisle prefix from 61,000 of 214,000 pick-location records.

**Sunday, November 22, daytime — Limited weekend volume.**
Skeleton weekend crew processes a reduced order volume. Pick volume is too low, and supervisory attention too diffuse, for the emerging accuracy problem to surface against normal noise.

### Day 1 of Production Under v11.0

**Monday, November 23, 4:10 a.m. — First full production shift begins under version 11.0.**
Full-volume picking resumes across all three shifts. Associates begin encountering scan confirmations that do not match physical location signage on the affected 61,000 bins; because the WMS accepts the scans, the picks proceed and the resulting mis-shipments are invisible at the point of pick.

**Monday, throughout the day — Pick accuracy degrades in real time, unseen.**
The quality report that would show pick accuracy runs on a two-shift lag; the data generated during the Sunday-night and Monday-day shifts is not available in reviewable form until later. The unstaffed exception queue accumulates flagged discrepancies without triage.

**Monday, midafternoon — Quality report shows accuracy at 91.2%.**
The report, reflecting an earlier shift's data due to the built-in lag, shows pick accuracy at 91.2 percent against a 99.6 percent baseline. No process routes this report to an owner empowered to act on it same-day; it lands in a review cycle rather than an alert.

**Monday evening/night shift — Mis-shipments continue to accumulate.**
Individual associates and a few supervisors note isolated mispick complaints but nothing rises to the level of a facility-wide signal. No single person has visibility into the aggregate pattern.

### Detection and Misdiagnosis

**Tuesday, November 24, 11:20 a.m. — Escalation.**
Thirty-one hours after full production resumed under version 11.0, a brand's returns team, receiving an outbound trailer, discovers approximately 900 wrong items in a single load. This physical, client-side discovery — not an internal system or report — triggers the first facility-wide escalation.

**Tuesday, ~11:45 a.m. — Investigation opens.**
Ephraim Sackey, Director of Information Technology, is engaged. Attention centers on a scanner firmware update pushed to the handheld fleet the prior week, on the theory that a firmware regression is causing scan validation to misfire.

**Tuesday, ~1:00 p.m. — Fleet firmware rollback ordered.**
A rollback of scanner firmware across the handheld fleet is initiated as the primary corrective action.

**Tuesday afternoon through Wednesday, ~10:00 p.m.–7:00 a.m. — Rollback executed.**
The rollback takes approximately nine hours to complete across the fleet. Pick accuracy does not improve. The firmware hypothesis is not supported by the outcome.

### Paper Picking

**Wednesday, November 25, morning — Decision to suspend scanner-validated picking.**
With the firmware rollback showing no effect and accuracy still degraded, Bianca Cardoso-Reyes, Vice President of Operations, orders the facility to move to paper pick sheets facility-wide, removing scan validation against the corrupted location data from the pick process entirely.

**Wednesday, daytime — Paper picking begins; throughput falls to 31,000 units/day.**
The change stops further mis-shipments driven by the location defect but reduces daily throughput by roughly 60 percent against the 78,000-unit baseline, five days before Black Friday.

**Wednesday through Thursday — Backlog begins accumulating.**
With inbound order volume ramping for the holiday period and outbound throughput reduced by more than half, the order backlog begins to build rapidly.

### Root Cause Identified

**Thursday, November 26, 2:00 a.m. — Defect identified.**
Marguerite Lapointe, Continuous Improvement Manager, working overnight, compares the live post-upgrade location master against a pre-upgrade export and identifies that 61,000 of 214,000 pick-location records are missing their aisle prefix. This is the first correct identification of the actual defect, more than four days after the upgrade completed and roughly 39 hours after the initial escalation.

**Thursday, morning — Root cause confirmed and communicated.**
The finding is validated against the transformation logic from the cutover. IT and Operations confirm the fix path: restoring the aisle prefix to the affected records from the pre-upgrade export, with validation before any location is returned to scanner-based picking.

**Thursday onward — Client communications.**
Tanya Whitehorse, Client Services Director, manages outreach to the 14 brands served by the facility, providing status, revised delivery expectations, and beginning service-credit and expedite-cost conversations with the two most heavily affected clients.

### Recovery

**Thursday–Friday, November 26–27 (Thanksgiving/Black Friday) — Fix rolled out incrementally.**
Corrected location records are validated and returned to production in batches, with scanner-based picking restored zone by zone as each batch is confirmed against a hard reconciliation (not aggregate counts). Paper picking continues in parallel for un-remediated zones through the peak volume days.

**Late November through early December — Backlog worked down alongside peak volume.**
The facility works the 214,000-order backlog concurrently with incoming Black Friday and Cyber Monday volume, using expedited freight to protect service levels on the oldest and highest-priority orders.

**By approximately December 6, 2026 — Backlog cleared.**
Eleven days after the shift to paper picking, the order backlog is fully cleared. Final tally: 38,000 orders shipped wrong or late during the incident and recovery window, $1.8 million in expedited freight cost, and $640,000 in service credits issued to two clients. One client subsequently gives notice on a $9 million annual contract.

---

## 4. Root Cause

**The location master transformation run during the Baseline 9.2-to-11.0 upgrade silently dropped the aisle prefix from 61,000 of 214,000 pick-location records, and post-upgrade validation did not check location-level data integrity — only aggregate counts.**

The upgrade's data migration remapped the facility's location master into a new schema. For a subset of locations — those following a particular legacy naming pattern — the transformation logic did not correctly carry forward the aisle prefix field, leaving those records with a location code that resembled a valid location but pointed to the wrong physical bin, or to no unambiguous bin at all. Because the malformed records were still structurally valid — populated fields, correct format, resolvable to *some* address — no schema validation, referential-integrity check, or count-based smoke test flagged them. The system did not fail to migrate 61,000 locations; it migrated them incorrectly and silently.

Scanner validation logic in Baseline confirms that a scanned location code exists and matches an expected pattern; it does not independently verify that the code corresponds to the *correct* physical location for a given pick task. Once the location master was corrupted, scans against the affected 61,000 bins validated successfully against the wrong location data, so the system had no internal signal that anything was wrong. The defect was invisible to the WMS itself and became visible only through downstream evidence: degraded pick accuracy, and eventually a client physically finding wrong items in a trailer.

This is fundamentally a data-migration validation gap, not a picking-process failure, a scanner-hardware failure, or an individual error. The system that should have caught the defect — pre-cutover data validation — did not check the right thing, and the system that should have surfaced it quickly post-cutover — quality reporting and exception handling — was structurally unable to do so in time.

---

## 5. Contributing Factors

**5.1 Compressed validation window.** The cutover date moved from May to November at the vendor's request, without a corresponding change to the validation plan. Parallel validation, originally scoped at two weeks, shrank to four days. A defect affecting more than a quarter of all pick locations plausibly would have surfaced during a full two-week parallel run against real order volume; it did not surface in four days, much of which fell over a low-volume weekend.

**5.2 Stale regression suite.** The regression test suite had not been updated since version 9.0 — two major versions behind the software being deployed. It was not designed to test the location master transformation logic introduced in later versions and would not have been expected to catch this class of defect even if run comprehensively.

**5.3 Vendor-template runbook.** The cutover runbook used was the vendor's standard template, not one adapted to Tannery Row's specific location schema, scale (214,000 locations across 900,000 square feet), or history of legacy naming conventions. Aggregate-count validation was sufficient for the template's generic use case but not for a facility with a heterogeneous, legacy-influenced location master.

**5.4 Peak-timing of the cutover.** Moving the cutover from May to late November placed it five days before Thanksgiving and six before Black Friday — the facility's highest-consequence season for both volume and client sensitivity. Any stabilization period needed after go-live collided directly with peak ramp, removing slack that would have existed under the original May date.

**5.5 Reporting latency.** The pick-accuracy quality report ran on an inherent two-shift lag by design, intended for trend monitoring rather than incident detection. Used as the sole facility-wide accuracy signal, this lag meant that even functioning reporting could not have surfaced the defect faster than roughly a full shift-and-a-half after it began.

**5.6 Unowned exception queue.** The exception queue — the mechanism designed to catch and route discrepancies in real time, independent of the lagging report — had been unowned since a September transfer. This was the single most direct point at which faster detection was structurally possible and did not happen: real-time signals existed and were not reviewed.

**5.7 No real-time accuracy alerting independent of the daily report.** The facility had no automated threshold alert (e.g., "pick accuracy has dropped more than X points versus rolling baseline") that did not depend on a human reviewing a lagged report or an unowned queue. Detection was entirely dependent on the two weakest links in the system.

**5.8 Anchoring on recent, familiar change.** The scanner firmware push the week prior was a recent, known change, and it became the working hypothesis under time pressure without an equally weighted look at the WMS upgrade itself — despite the upgrade being the far larger and more recent system-wide change. The investigation pattern-matched to the more legible, more familiar type of failure (hardware/firmware) before the less familiar one (a silent data transformation defect).

**5.9 No location-level reconciliation tooling.** The pre-upgrade export existed and was exactly what was needed to detect the defect — it is what Lapointe ultimately used — but no automated reconciliation between pre- and post-upgrade location masters was run as a standard part of cutover validation. The tool that solved the problem in minutes once applied was not applied for four days because it was not a defined step.

---

## 6. What Worked

- **The pre-upgrade export existed and was retained.** Its availability made root-cause identification possible at all, and once applied, the comparison was fast and conclusive.
- **Client-facing evidence eventually forced escalation.** Although slow, the brand returns team's discovery was a reliable, hard-to-ignore signal, and the facility responded to it immediately rather than downplaying it.
- **The decision to move to paper picking, once made, was decisive and stopped further damage from the known-bad location data.** It was a costly tradeoff but a correct one given the information available at the time: it prioritized shipment correctness over throughput once the scanner/firmware theory was exhausted, rather than continuing to run corrupted validation against client orders.
- **Client Services engaged early and stayed engaged.** Tanya Whitehorse's ownership of brand communications throughout the incident meant clients received status updates and were not learning about problems solely from their own receiving docks after the initial trigger event.
- **Root-cause investigation, once redirected, moved quickly.** From the moment Lapointe applied the pre-upgrade comparison, the actual defect was identified and confirmed within hours, and a remediation path (batch correction with hard reconciliation, zone-by-zone re-enablement) was defined and executed without a second false start.
- **The remediation approach for restoring scanner picking was more rigorous than the original cutover validation.** Zone-by-zone reconciliation against corrected data, rather than aggregate counts, reflects an appropriate escalation of validation rigor in response to what was learned.

## 7. What Did Not Work

- **Post-upgrade validation checked aggregate counts, not location-level integrity.** This was the primary technical gap: a check that would have caught the defect (location-level reconciliation) existed in principle and was not run as part of standard cutover validation.
- **The exception queue had no owner for over two months before the incident, and this was not identified as a risk ahead of a major system cutover.** A known gap in a real-time detection mechanism was not remediated or backstopped before a high-risk change was introduced into the environment it was meant to monitor.
- **Quality reporting cadence was mismatched to the risk profile of the cutover.** A two-shift lag is acceptable for steady-state trend monitoring; it is not acceptable as the primary detection mechanism in the days immediately following a major system change with no backfilled real-time alternative.
- **The validation timeline was compressed to accommodate a vendor-requested date without a compensating change to test scope, regression currency, or reconciliation depth.** The schedule moved; the validation plan did not adapt to the reduced time available.
- **The cutover runbook was not adapted to the facility.** Using a vendor's generic template for a 214,000-location, 14-brand operation left validation steps calibrated for a simpler or smaller deployment.
- **Initial root-cause investigation focused on the most recent familiar change rather than the most recent large change.** Nine hours were spent rolling back scanner firmware fleet-wide with no evidence linking it to the symptom pattern beyond recency, while the WMS upgrade — the larger, more obvious candidate — was not investigated with equal priority from the outset.
- **No one held responsibility for verifying that the location master migrated correctly, distinct from verifying that the upgrade "completed."** Completion and correctness were treated as the same signal.
- **The regression suite was allowed to go two major versions stale without a corresponding decision to either update it, formally retire it, or explicitly flag it as non-authoritative for the November upgrade.**

---

## 8. Action Items

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Implement automated pre/post location-master reconciliation as a mandatory, blocking step in all future WMS cutover runbooks — not just aggregate count checks. | Ephraim Sackey, Director of IT | Aug 31, 2026 |
| 2 | Permanently staff and define an on-call ownership rotation for the pick-accuracy exception queue, with explicit backfill coverage for any transfer or vacancy exceeding 5 business days. | Bianca Cardoso-Reyes, VP of Operations | Aug 14, 2026 |
| 3 | Build a real-time pick-accuracy threshold alert (independent of the two-shift lagged report) that pages an on-call owner when accuracy drops more than 2 points below rolling baseline within a shift. | Ephraim Sackey, Director of IT | Sep 15, 2026 |
| 4 | Rewrite the cutover runbook to remove reliance on the vendor's generic template; incorporate facility-specific location schema, scale, and legacy-naming edge cases into validation steps. | Ephraim Sackey, Director of IT, with Marguerite Lapointe, Continuous Improvement Manager | Sep 30, 2026 |
| 5 | Establish a standing policy that any change to a previously agreed cutover date (vendor- or internally-driven) triggers a mandatory re-scoping of the validation window and regression coverage, not just a calendar move. | Bianca Cardoso-Reyes, VP of Operations | Aug 21, 2026 |
| 6 | Refresh the regression test suite to current production version (11.0) and establish a policy that the suite is updated with every major version release, not left to drift. | Ephraim Sackey, Director of IT | Oct 15, 2026 |
| 7 | Restore parallel validation to a minimum two-week window for all future major WMS version upgrades, with no exceptions absent a documented, leadership-approved risk acceptance. | Bianca Cardoso-Reyes, VP of Operations | Aug 14, 2026 (policy effective date) |
| 8 | Document and formally test a "root-cause triage checklist" for production anomalies that requires evaluating all recent system changes by scope and recency — not defaulting to the most recently touched familiar component — before committing response resources to a single hypothesis. | Ephraim Sackey, Director of IT | Sep 30, 2026 |
| 9 | Define and rehearse a documented "degrade to manual process" playbook (including paper-pick throughput expectations and backlog-risk thresholds) so that the tradeoff decision and its operational consequences are pre-modeled rather than made under live pressure. | Bianca Cardoso-Reyes, VP of Operations | Oct 30, 2026 |
| 10 | Establish a standing client-notification protocol for facility-wide operational incidents, triggered automatically at defined severity thresholds rather than after client-side discovery. | Tanya Whitehorse, Client Services Director | Sep 15, 2026 |
| 11 | Conduct a joint IT/Operations tabletop exercise simulating a silent data-migration defect post-cutover, to pressure-test detection and escalation paths before the next major system change. | Marguerite Lapointe, Continuous Improvement Manager | Nov 1, 2026 |
| 12 | Review vendor contract terms regarding cutover-date changes requested by the vendor, including requirements for compensating validation time or vendor-side liability for defects surfaced within a defined post-upgrade window. | Bianca Cardoso-Reyes, VP of Operations | Oct 1, 2026 |

---

## 9. Closing Note

This incident was not caused by a single failed check or a single missed alert; it was caused by a stack of independently reasonable-looking gaps — a compressed validation window, a generic runbook, a lagged report, an unstaffed queue, a stale regression suite — that individually might each have been survivable, but together left a defect affecting more than a quarter of the facility's pick locations undetected for 31 hours and unresolved for another two days after that. The systems designed to catch this class of problem either weren't looking at the right layer of data (aggregate counts instead of location-level integrity) or weren't staffed to look at all (the exception queue). The corrective actions above are aimed at rebuilding redundancy into detection — so that no single missing owner or single lagging report is ever again the only thing standing between a migration defect and a client's dock.

## Appendix A: Systems and Data Flow Involved

**Baseline WMS (v9.2 → v11.0).** Core warehouse management system governing location master data, pick-task generation, scan validation, and inventory movement across all 14 brands operating in the facility. Version 11.0 introduced a revised location master schema; the migration from the 9.2 schema is where the aisle-prefix truncation occurred.

**Location Master Table.** The authoritative record of all 214,000 pick locations, including aisle, bay, shelf, and bin identifiers. Prior to the upgrade, location codes followed a compound format in which the aisle prefix was a required leading segment. Post-migration, 61,000 records retained a syntactically valid but semantically incomplete code, missing that leading segment.

**Handheld Scanner Fleet.** Approximately 1,150 associate-carried devices used to confirm pick-location and item accuracy at the point of pick. Scanner firmware was updated the week of November 16–18, unrelated to the WMS upgrade, and was the initial (incorrect) focus of root-cause investigation.

**Quality Reporting Pipeline.** A downstream reporting process that aggregates scan and exception data into a facility-wide pick-accuracy metric, refreshed on a two-shift lag by design. Not architected for near-real-time anomaly detection.

**Exception Queue.** A system-generated queue of flagged pick/scan discrepancies requiring human triage, intended to function as a faster, more granular detection path than the lagged aggregate report. Unowned since September 2026.

**Pre-Upgrade Export.** A full snapshot of the location master table taken before the November 21 cutover, retained per standard change-management practice. Used by Marguerite Lapointe on November 26 to identify the defect via direct comparison against the live post-upgrade table.

---

## Appendix B: Cost Breakdown

| Cost Category | Amount | Notes |
|---|---|---|
| Expedited freight | $1,800,000 | Incurred clearing the 214,000-order backlog against Black Friday volume |
| Service credits — Client A | Included in $640,000 total | Issued in direct response to mis-shipment volume |
| Service credits — Client B | Included in $640,000 total | Issued in direct response to mis-shipment volume |
| Service credits, combined | $640,000 | Two clients |
| At-risk contract value | $9,000,000 annually | Client gave notice during recovery period; value not yet realized as loss, contingent on retention efforts |
| Scanner firmware rollback labor | Not separately quantified | Approx. 9 hours fleet-wide, effort determined non-contributory to resolution |
| Paper-picking labor premium | Not separately quantified | Reflects reduced throughput (31,000 vs. 78,000 units/day) over the paper-picking period, partially offset upon zone-by-zone scanner restoration |
| **Total quantified direct cost** | **$2,440,000** | Excludes at-risk contract, labor premium, and reputational cost |

---

## Appendix C: Glossary

**Aisle prefix** — The leading alphanumeric segment of a pick-location code identifying which aisle a bin resides in. Its removal from 61,000 records caused location codes to resolve ambiguously or incorrectly during scan validation.

**Cutover** — The defined window during which a system upgrade is executed and the prior version is retired from production use.

**Location master** — The system-of-record table mapping every physical storage and pick location in the facility to a unique, structured identifier.

**Parallel validation** — A pre-cutover practice of running new and old system versions concurrently against live or shadow data to compare outputs before fully committing to the new version.

**Pick accuracy** — The percentage of picks in which the item and quantity shipped match the item and quantity ordered, measured against scan and downstream audit data.

**Regression suite** — A defined set of automated tests run against a system after a change to confirm that existing functionality has not been broken.

**Two-shift lag** — The built-in delay between when data is generated on the floor and when it appears in the facility's standard quality report, originally designed for trend visibility rather than incident detection.

---

## Appendix D: Distribution and Review

This postmortem was prepared for internal distribution to Operations, Information Technology, Client Services, and Continuous Improvement leadership. It is intended to inform the action items in Section 8 and to serve as a reference document for future major system change planning at this facility and others in the network.

**Next scheduled review of action-item completion status:** October 1, 2026, coinciding with Action Item 12.

## Appendix E: Revision History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1 (Draft) | Nov 28, 2026 | Marguerite Lapointe, Continuous Improvement Manager | Initial timeline reconstruction from system logs, escalation records, and root-cause findings |
| 0.2 (Draft) | Dec 2, 2026 | Marguerite Lapointe, with input from Ephraim Sackey | Added technical root-cause detail, contributing factors, and cost figures pending finalization |
| 0.3 (Draft) | Dec 5, 2026 | Marguerite Lapointe, with input from Tanya Whitehorse | Incorporated finalized service-credit figures and client-impact language reviewed by Client Services |
| 0.4 (Draft) | Dec 8, 2026 | Bianca Cardoso-Reyes | Reviewed for accuracy of operational decisions and paper-picking impact figures; backlog-clearance date confirmed |
| 1.0 (Final) | Dec 10, 2026 | Marguerite Lapointe | Finalized for distribution following sign-off from IT, Operations, and Client Services leadership |

---

## Appendix F: Sign-Off

This postmortem has been reviewed and approved for distribution by the following:

**Bianca Cardoso-Reyes**
Vice President, Operations
Approved: Dec 9, 2026

**Ephraim Sackey**
Director, Information Technology
Approved: Dec 9, 2026

**Tanya Whitehorse**
Director, Client Services
Approved: Dec 10, 2026

**Marguerite Lapointe**
Continuous Improvement Manager
Prepared and Approved: Dec 10, 2026

---

## Appendix G: Related Documents

- Baseline WMS Cutover Runbook, v11.0 (vendor template, as executed November 21–22, 2026) — retained for audit purposes; superseded by facility-specific runbook per Action Item 4.
- Pre-Upgrade Location Master Export, captured November 20, 2026 — retained as reference dataset used in root-cause analysis.
- Quality Report Archive, November 22–December 6, 2026 — retained showing lagged accuracy figures across the incident window.
- Client Communication Log, Client Services Director, November 24–December 6, 2026 — retained by Client Services, referenced in Section 3 and Section 7.
- Scanner Firmware Rollback Change Record, November 24–25, 2026 — retained showing scope, duration, and outcome of the fleet rollback.
- Backlog Recovery Tracking Log, November 25–December 6, 2026 — daily order-count and throughput data supporting Section 2 impact figures.

**End of document.**

## Appendix H: Network Advisory

Because Tannery Row Logistics operates additional fulfillment centers on the same Baseline WMS platform, findings from this incident have been escalated beyond the Rome, New York facility.

**Facilities on Baseline v9.2, scheduled or pending upgrade to v11.0** should not proceed under the existing vendor-template runbook. Any facility with a cutover date already set is directed to pause and confirm the following before proceeding:

1. A location-level pre/post reconciliation step has been added to their runbook, independent of aggregate count validation.
2. Parallel validation is scoped for a minimum of two weeks, with no schedule compression permitted without a documented, leadership-signed risk acceptance.
3. The exception queue and quality-report ownership for that facility is confirmed staffed, with named backup coverage, prior to cutover — not assumed staffed based on org chart.
4. Regression suite currency has been confirmed against the target version, not merely the most recent version the suite was last validated for.

Facilities already running v11.0 that migrated location master data under the same vendor transformation logic used at Rome are directed to run the Appendix A-style pre/post location reconciliation retroactively, using retained pre-upgrade exports, to rule out latent instances of the same defect. Any facility unable to locate a retained pre-upgrade export should treat this as a standalone finding and escalate to IT leadership, as it represents a gap in change-management data retention independent of this incident.

This advisory does not extend to facilities on the Baseline platform operated by other companies; those relationships are managed through the vendor directly, and Tannery Row's Director of Information Technology has opened a case with the vendor regarding the transformation logic defect for its own remediation on the vendor's side.

---

## Appendix I: Open Items for Further Investigation

The following questions remain open as of this document's finalization and are not resolved by the action items in Section 8. They are noted here so they are not lost to the closure of the immediate incident response.

**Whether the location master transformation defect is deterministic or data-dependent.** Root-cause analysis confirmed *that* 61,000 of 214,000 records were affected and *that* a specific legacy naming pattern was implicated, but did not fully characterize why that pattern, specifically, triggered the truncation in the vendor's transformation logic. This has been referred to the vendor as part of the open case referenced in Appendix H but is not yet closed.

**Whether the two clients who received service credits, and the client that gave notice, experienced downstream inventory or system-of-record discrepancies beyond the mis-shipments already identified.** Client Services has confirmed the mis-shipment counts underlying the credits issued but has not completed a full audit of whether incorrect location data affected those clients' inventory visibility or forecasting during the incident window.

**Whether the four-day parallel validation period, had it run the full two weeks originally planned, would have surfaced the defect at the volumes tested, given that the defect only became clearly visible at full production volume on November 23.** This bears on how much confidence to place in the two-week restoration (Action Item 7) as a sufficient control on its own, versus requiring it in combination with the location-level reconciliation step (Action Item 1).

**Whether other exception queues or unowned monitoring roles exist elsewhere in the facility's operational structure as a result of the same transfer or similar unfilled-role patterns.** This incident surfaced one unowned queue; no facility-wide audit of monitoring role coverage has yet been conducted.

Resolution of these items will be tracked outside this postmortem, through the standard continuous-improvement backlog, with status reviewed at the October 1, 2026 review referenced in Appendix D.

**End of document.**

## Appendix J: Incident Classification and Severity Scoring

For internal tracking purposes, this incident has been retroactively scored against Tannery Row Logistics' operational incident severity framework, to calibrate future response protocols.

| Dimension | Rating | Basis |
|---|---|---|
| Client impact | Severe | 38,000 orders wrong or late; $640,000 in service credits; one $9M contract under notice |
| Financial impact | Severe | $2.44M direct quantified cost, excluding at-risk contract value |
| Duration | Extended | 11 days from onset of paper-picking to full backlog clearance; 15 days from cutover to backlog clearance |
| Detection speed | Poor | 31 hours from defect onset to first escalation; escalation was client-triggered, not internally detected |
| Diagnostic accuracy | Poor | Initial 9-hour response effort (scanner rollback) directed at incorrect root cause |
| Containment effectiveness | Adequate | Paper-picking transition, once executed, reliably stopped further mis-shipments from the known defect |
| Recovery execution | Adequate | Zone-by-zone reconciliation and re-enablement, once root cause was known, proceeded without further false starts |

**Overall classification: Severity 1 (facility-wide, client-impacting, financially material).**

This is the first Severity 1 incident recorded at the Rome facility since the severity framework was adopted. Its scoring establishes a reference case for calibrating future incident response time targets, specifically around detection speed and diagnostic accuracy, both of which scored poorly here relative to containment and recovery execution.

---

## Appendix K: Training and Documentation Updates Triggered by This Incident

The following existing training and reference materials have been identified as requiring updates as a direct result of findings in this postmortem. These are distinct from the systemic action items in Section 8 and represent documentation/training debt rather than process or tooling gaps.

- **New Associate Scanner Training Module.** Currently does not instruct associates on what to do when a scan confirms successfully but the physical location does not visually match expected signage. To be updated to include an explicit "scan-confirmed but location looks wrong" reporting path, independent of the exception queue.

- **Shift Supervisor Escalation Guide.** Currently does not define a threshold or process for aggregating multiple isolated mispick complaints into a facility-wide signal. To be updated with guidance on pattern recognition across shift handoffs.

- **IT On-Call Runbook for WMS Incidents.** Currently does not include a decision tree distinguishing "recent familiar change" from "recent large change" when scoping initial root-cause hypotheses. To be updated per Action Item 8 once that checklist is finalized.

- **Client Services Incident Communication Template.** Used reactively during this incident; not previously formalized as a standing template triggered by defined severity thresholds. To be formalized per Action Item 10.

- **New Hire Onboarding for Continuous Improvement Role.** Does not currently include training on using pre-change data exports for post-change reconciliation as a standard diagnostic technique. To be added, given its central role in this incident's resolution.

Ownership and timelines for these documentation updates will be assigned separately through the Continuous Improvement team's standard documentation-maintenance process, distinct from the Section 8 action item tracker, and are noted here for completeness of the incident record.

**End of document.**
