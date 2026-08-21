# Incident Postmortem: Baseline WMS 11.0 Upgrade — Location Master Corruption and Peak-Season Fulfillment Disruption

**Tannery Row Logistics — Rome, New York Fulfillment Center**

| | |
|---|---|
| **Document status** | Final |
| **Incident ID** | INC-2026-1122 |
| **Incident window** | November 22 – December 8, 2026 |
| **Severity** | SEV-1 (highest) |
| **Prepared by** | Marguerite Lapointe, Continuous Improvement Manager |
| **Reviewed by** | Bianca Cardoso-Reyes, VP Operations; Ephraim Sackey, Director of IT; Tanya Whitehorse, Client Services Director |
| **Distribution** | Executive team, site leadership, Baseline vendor account team (redacted version) |
| **Publication date** | December 18, 2026 |

This postmortem is blameless. Its purpose is to understand how our systems, processes, and decision structures produced this outcome, and to change them so that a similar failure cannot recur. Every individual named in this document acted reasonably given the information available to them at the time. The failures described here are failures of process design, testing discipline, monitoring architecture, and organizational handoffs — not of individual judgment or effort.

---

## 1. Executive Summary

Over the weekend of November 21–22, 2026, the Rome fulfillment center upgraded its warehouse management system, Baseline, from version 9.2 to version 11.0. The cutover completed at 4:10 a.m. Sunday and passed all smoke tests. Unknown to the cutover team, a data transformation script in the vendor's migration toolkit silently truncated the aisle prefix from 61,000 of the building's 214,000 pick location records — roughly 28.5 percent of the location master. The corrupted records remained structurally valid, so no load errors fired. The practical effect was that RF scan validation directed pickers to, and confirmed picks against, the wrong physical bins across large sections of the building.

Pick accuracy fell from a trailing baseline of 99.6 percent to 91.2 percent by Monday afternoon, November 23. Because the quality reporting pipeline operates on a two-shift lag, and because the exception queue that would have surfaced the anomaly in near-real time had lost its designated owner in a September organizational transfer, no one saw the signal. The defect went undetected for 31 hours, until 11:20 a.m. Tuesday, November 24, when a client brand's returns team reported approximately 900 incorrect items in a single inbound trailer.

The initial diagnosis attributed the errors to scanner firmware that had been pushed to the RF fleet the prior week. A full fleet firmware rollback consumed nine hours on Tuesday and produced no improvement, because the firmware was not the cause. On Wednesday, November 25, with error rates unabated and Black Friday three days out, the VP of Operations moved the entire building to paper pick sheets — a deliberate tradeoff that stopped the accuracy bleed but cut daily throughput from 78,000 units to 31,000 units and allowed a backlog of 214,000 orders to accumulate against peak-season volume.

At 2:05 a.m. Thursday, November 26, the Continuous Improvement Manager identified the true root cause by comparing the live location master against a pre-upgrade export: 61,000 records were missing their aisle prefix. The vendor confirmed the transformation defect within hours. A corrected location master was built, validated, and loaded Thursday evening, and system-directed picking resumed in phases Friday morning, reaching full RF operation by Friday afternoon — the morning of Black Friday.

Clearing the accumulated backlog took 11 days, concluding December 8. In total, approximately 38,000 orders shipped incorrect or late, expedited freight to protect client delivery commitments cost $1.8 million, two clients invoked service credits totaling $640,000, and one client issued notice of termination on a $9 million annual contract.

The root cause was a vendor migration script defect. But the script defect alone did not produce a $2.4 million-plus incident. Five organizational and process conditions converted a data bug into a multi-week peak-season crisis: a compressed upgrade schedule moved from May to the weekend before Thanksgiving; a regression test suite unchanged since version 9.0 that contained no location master integrity checks; parallel validation shortened from two weeks to four days; a monitoring architecture with a two-shift reporting lag and an orphaned exception queue; and an incident response that anchored on a recent change (scanner firmware) rather than the largest change (the WMS upgrade itself).

---

## 2. Impact

All figures reconciled against WMS, transportation management, and finance records as of December 15, 2026.

### 2.1 Operational impact

| Metric | Baseline | During incident | Delta |
|---|---|---|---|
| Pick accuracy | 99.6% | 91.2% (trough, Nov 23) | −8.4 pts |
| Daily throughput (units) | 78,000 | 31,000 (paper picking, Nov 25–27) | −60% |
| Pick locations corrupted | 0 | 61,000 of 214,000 | 28.5% of location master |
| Undetected defect duration | — | 31 hours | Nov 22, 4:10 a.m. – Nov 24, 11:20 a.m. |
| Misdiagnosis duration (firmware rollback) | — | 9 hours | Nov 24 |
| Peak order backlog | ~0 | 214,000 orders | Nov 27 |
| Backlog clearance duration | — | 11 days | Nov 27 – Dec 8 |
| Orders shipped wrong or late | — | ~38,000 | — |

### 2.2 Financial impact

| Category | Amount |
|---|---|
| Expedited freight (backlog recovery, client commitments) | $1,800,000 |
| Service credits (two clients) | $640,000 |
| Overtime and temporary labor (backlog recovery, returns processing) | ~$310,000 (est.) |
| Returns processing and reverse logistics for misshipments | ~$140,000 (est.) |
| **Direct cost subtotal** | **~$2,890,000** |
| Contract termination notice (annualized revenue at risk) | $9,000,000 |

### 2.3 Client impact

- 14 client brands experienced degraded service levels for between 6 and 16 days.
- 2 clients invoked contractual service credits ($640,000 combined).
- 1 client issued formal notice on a $9 million annual contract. Retention discussions are ongoing under Client Services.
- Approximately 900 incorrect items were identified in the single returns trailer that triggered detection; total misshipped units across the incident are estimated at 41,000–46,000 based on returns and claims data still being reconciled.

### 2.4 Workforce impact

- 1,150 associates operated under changed procedures for up to 16 days, including a full reversion to paper picking that most associates hired since 2019 had never performed.
- Extended shifts and six-day weeks ran from November 27 through December 8. Voluntary attrition during the recovery window was slightly elevated (11 separations vs. a 4–6 expected range for the period).

---

## 3. Background: The Upgrade Decision

The Baseline 9.2-to-11.0 upgrade was originally scheduled for the weekend of May 16, 2026 — a deliberately low-volume window with a full peak season of buffer before Black Friday. In February 2026, the vendor requested a postponement, citing resourcing constraints and a desire to deploy version 11.0 rather than the interim 10.4 release, which was approaching end of support. After two further scheduling rounds, the parties agreed on the weekend of November 21, 2026.

The decision record shows that site leadership raised the proximity to peak season and was given three assurances: (1) version 11.0's migration tooling was "mature and field-proven" at comparable sites; (2) the vendor would provide on-call migration support through the cutover weekend; and (3) rollback to 9.2 was possible within eight hours if smoke tests failed. All three assurances were technically honored — and none of them addressed the actual failure mode, which was a silent data corruption that passed smoke tests and only manifested under production picking volume.

Two compressions accompanied the date change:

- **Parallel validation shrank from two weeks to four days.** The original May plan called for a two-week parallel run in which a shadow instance of 11.0 processed mirrored transaction volume. The November plan cut this to four days to fit between the prior client onboarding freeze and the cutover date. The four-day parallel run processed synthetic waves against a subset of the location master; the corrupted-prefix scenario never had the opportunity to surface because the parallel environment used a smaller, clean location extract rather than the full production master run through the vendor's transformation pipeline.
- **The cutover runbook was the vendor's generic template**, lightly annotated for Rome. It contained no site-specific data validation gates. The template's post-migration checklist verified record counts (which matched — 214,000 in, 214,000 out) and schema validity (which passed — the truncated records were structurally legal) but performed no field-level reconciliation against the source system.

Separately, the site's own regression test suite had not been updated since version 9.0, three major versions and roughly four years earlier. It contained 212 test cases, of which 184 still passed against 11.0 in pre-cutover testing. None of the 212 cases validated location master data integrity post-migration, because location master migration had not been in scope when the suite was written.

**Assessment.** The decision to accept a November date was made in good faith, with vendor assurances that appeared substantive. The failure was not the date itself but that the schedule compression was absorbed entirely by validation activities — the exact activities that would have caught this defect — without a corresponding risk acceptance decision being escalated to the executive level. The two-week parallel run was cut to four days at the project-team level; no risk memo documenting that tradeoff reached the VP of Operations or the executive sponsor.

---

## 4. Timeline

All times Eastern.

### Cutover and silent failure

**Saturday, November 22 21, 6:00 p.m.** — Final outbound waves complete. WMS transaction freeze begins. Cutover team (site IT, vendor migration engineers on remote bridge) begins the 9.2-to-11.0 migration.

**Sunday, November 22, 2:35 a.m.** — Data migration completes, including the location master transformation. The transformation script's parsing logic mishandles location IDs in the site's legacy 2019 numbering format, truncating the aisle prefix on 61,000 records. Record counts reconcile (214,000/214,000). No errors logged.

**Sunday, November 22, 4:10 a.m.** — Upgrade declared complete. Smoke tests pass: system login, wave creation, a scripted pick-pack-ship cycle in the test zone (which happened to use post-2019-format locations unaffected by the defect), label generation, host interface handshakes. Rollback window closes per runbook.

**Sunday, November 22, 6:00 a.m.** — Reduced Sunday shift (approx. 210 associates) resumes live picking. Scattered "bin mismatch" scan exceptions begin appearing. Associates, briefed to expect "minor system quirkiness" post-upgrade, use supervisor overrides to keep waves moving. 340 override events logged by end of shift — roughly 8x a normal Sunday.

**Monday, November 23, 7:00 a.m.** — Full first shift begins. Override and short-pick exceptions climb throughout the day. The exception queue, which would normally page its owner at threshold, accumulates unread: its designated owner transferred to the Syracuse site in September and the queue's alert routing was never reassigned.

**Monday, November 23, ~2:00 p.m.** — Pick accuracy, as later reconstructed, has fallen to 91.2 percent. The quality accuracy report that would display this figure runs on a two-shift lag; the degraded numbers will not render on any dashboard until Tuesday morning, and no one is watching the queue that reflects it in real time.

**Monday, November 23, evening** — Second shift logs the highest single-shift exception count in site history (2,140 events). Shift supervisors attribute the exceptions to "post-upgrade settling" consistent with the briefing they received. Outbound trailers ship on schedule — containing a growing proportion of wrong items.

### Detection

**Tuesday, November 24, 8:40 a.m.** — The lagged quality report renders Monday first-shift data showing accuracy in the low 90s. The report distributes to a 14-person email list. A quality analyst flags it in a team channel at 9:55 a.m.; the flag is queued behind peak-readiness traffic.

**Tuesday, November 24, 11:20 a.m. — DETECTION.** Client Services Director Tanya Whitehorse receives an urgent call from a client brand's returns manager: a returns trailer received that morning contains approximately 900 items that do not match order manifests — an order of magnitude beyond normal. Whitehorse escalates immediately to site leadership. **Elapsed time since defect introduction: 31 hours.**

**Tuesday, November 24, 12:15 p.m.** — SEV-1 incident bridge opened. Bianca Cardoso-Reyes (VP Operations) designated incident commander. Attendees: IT, Operations, Quality, Client Services.

### Misdiagnosis

**Tuesday, November 24, 12:50 p.m.** — Ephraim Sackey, Director of IT, presents the leading hypothesis: RF scanner firmware version 6.4.1, pushed to the 640-device fleet on November 17, is corrupting barcode reads. The hypothesis is plausible — the firmware push was recent, scanner-adjacent, and the errors present as scan validation failures. The WMS upgrade is discounted because "it passed smoke tests and the vendor confirmed a clean migration." No structured differential diagnosis is performed; the upgrade is not tested as a hypothesis before the firmware theory is actioned.

**Tuesday, November 24, 1:10 p.m. – 10:15 p.m.** — Fleet-wide firmware rollback to 6.3.8. Each device requires manual docking and reflash; the process consumes the IT team, two shifts of device downtime rotation, and nine hours. Picking continues on rotating device availability throughout, continuing to generate errors.

**Tuesday, November 24, 11:30 p.m.** — Rollback complete. Sample audits on rolled-back devices show mismatch errors continuing at an unchanged rate. Firmware hypothesis falsified. **Elapsed misdiagnosis cost: 9 hours of IT capacity plus a full additional shift of erroneous shipping.**

### Containment

**Wednesday, November 25, 5:30 a.m.** — Overnight bridge session. Error rate unabated; Black Friday is 48 hours out; the building is still shipping wrong product at scale. Cardoso-Reyes frames the decision explicitly: continue system-directed picking and ship a known ~9 percent error rate into peak, or revert to paper pick sheets — stopping the accuracy bleed at the cost of throughput.

**Wednesday, November 25, 6:00 a.m. — CONTAINMENT.** Cardoso-Reyes orders full reversion to paper pick sheets, printed from order data with human-readable location descriptions that pickers can verify against physical aisle signage, bypassing the corrupted scan validation entirely. Throughput drops to 31,000 units/day against 78,000 baseline demand. Misshipments effectively stop. Backlog begins accumulating at ~47,000 orders/day.

**Wednesday, November 25, 9:00 a.m.** — Whitehorse initiates proactive client notifications to all 14 brands: known accuracy incident, containment in place, root cause under investigation, twice-daily updates committed. Vendor escalated to SEV-1 under the support contract; vendor engineers join the bridge and begin log review.

**Wednesday, November 25, all day** — Vendor log review finds no anomalies in application logs (correct: the application was behaving exactly as designed against corrupt data). Investigation remains focused on runtime behavior rather than migrated data.

### Root cause identification

**Thursday, November 26, 2:05 a.m. — ROOT CAUSE FOUND.** Marguerite Lapointe, Continuous Improvement Manager, working from the hypothesis that the errors clustered geographically by aisle rather than randomly by device or picker, pulls the pre-upgrade location master export (retained from the cutover backup set) and diffs it field-by-field against the live 11.0 location master. The diff shows 61,000 records with the aisle prefix absent. The affected records correspond exactly to the site's pre-2019 location numbering format. Error heat-mapping confirms: mismatch exceptions occur only in aisles with legacy-format location IDs.

**Thursday, November 26, 4:30 a.m.** — Vendor engineers reproduce the defect in the transformation script: a parsing routine assumed a fixed-width location ID format and truncated the leading segment of legacy-format IDs. Vendor confirms the defect is present in the migration toolkit shipped with 11.0 and opens a product defect ticket.

### Remediation

**Thursday, November 26, 10:00 a.m. – 6:00 p.m.** — Corrected location master built from the pre-upgrade export, transformed with a patched script, and validated in staging with a full 214,000-record field-level reconciliation (a check that, notably, took under two hours to build and run — and had not existed in the cutover runbook).

**Thursday, November 26, 9:40 p.m.** — Corrected location master loaded to production during shift changeover. Targeted cycle counts across 400 sampled locations in previously affected aisles: 100 percent scan validation success.

**Friday, November 27, 6:00 a.m.** — System-directed RF picking resumes in two pilot zones with quality auditors performing 100 percent outbound audit. Accuracy in pilot zones: 99.5 percent.

**Friday, November 27, 2:00 p.m. — RESOLUTION (system).** Full building returns to RF-directed picking. Black Friday operates on the restored system at full accuracy. Backlog stands at 214,000 orders.

### Recovery

**November 27 – December 8** — Backlog burn-down: extended shifts, weekend operation, temporary labor, and $1.8 million in expedited freight to protect client delivery commitments where contractually or relationally required. Whitehorse's team manages brand-by-brand prioritization and twice-daily communication. Approximately 38,000 orders ultimately ship wrong (pre-containment) or late (backlog).

**Monday, December 8 — RESOLUTION (operational).** Backlog cleared. Standard shift patterns resume.

**Tuesday, December 9** — Incident formally closed. Postmortem process initiated.

---

## 5. Root Cause

**A defect in the vendor's version 11.0 migration toolkit truncated the aisle prefix from location ID records that used the site's pre-2019 numbering format, silently corrupting 61,000 of 214,000 pick location records during the November 21–22 cutover.**

The transformation script assumed a fixed-width location ID structure introduced in the site's 2019 slotting redesign. Locations created before that redesign — concentrated in the building's original footprint — carry a longer legacy format. The script's parser read legacy IDs from the wrong offset and dropped the leading aisle segment. Because the truncated IDs remained syntactically valid and unique, no constraint violations or load errors occurred, and record counts reconciled perfectly.

The corrupted records caused the WMS to associate inventory and pick tasks with incorrect physical bins. Scan validation — the system's core accuracy safeguard — then actively *confirmed* wrong picks as correct wherever the corrupted mapping happened to align a real barcode with a wrong record, and generated mismatch exceptions elsewhere. The system's error-prevention mechanism became an error-production mechanism.

It is essential to state clearly: **the script defect is the root cause of the corruption, but not the root cause of the business impact.** A corrupted migration caught in a two-week parallel run, or in a post-load reconciliation, or within two hours by a monitored exception queue, is a footnote. The magnitude of this incident was produced by the contributing factors below.

---

## 6. Contributing Factors

### 6.1 Schedule compression absorbed by validation (upgrade decision)

The move from May to November was accepted with vendor assurances that addressed rollback and support but not data integrity. Critically, the schedule pressure was absorbed by cutting exactly the activities designed to catch silent defects:

- Parallel validation: two weeks → four days, and run against a clean subset extract rather than the full production location master passed through the actual migration pipeline. The parallel environment therefore could not have surfaced the defect even in principle.
- No executive-level risk acceptance was documented for either compression. The tradeoff was made at working-team level and never surfaced as a decision requiring sign-off.

**Systemic gap:** no policy defines minimum validation requirements for major-version WMS changes, and no policy prohibits major system changes inside a peak-season freeze window.

### 6.2 Stale regression suite and template runbook (testing gaps)

- The regression suite dated to version 9.0 and contained zero data-migration integrity checks. Test coverage had not been reviewed against the actual scope of the change being tested.
- The cutover runbook was the vendor's generic template. Its post-migration verification consisted of record counts and schema checks — both of which the corrupted data passed. A field-level source-to-target reconciliation of the location master, subsequently built in under two hours during the incident, was not in the runbook and was not requested.
- Smoke tests exercised only the test zone, which by coincidence used post-2019 locations. The smoke test passed not because the system was healthy but because it never touched the 28.5 percent of the building that was broken. Smoke test coverage was never mapped against data-format diversity in the location master.

### 6.3 Monitoring lag and the orphaned exception queue (detection gap)

Two independent monitoring failures combined to produce the 31-hour detection gap:

- **The two-shift reporting lag.** The pick accuracy report is a batch process reflecting data two shifts old. It is a management report, not a monitoring tool, but it was the de facto accuracy monitor. Real-time accuracy telemetry existed in the exception queue but nowhere on a dashboard.
- **The orphaned exception queue.** The queue's owner transferred to another site in September. The transfer checklist covered badge, payroll, and system access — not monitoring responsibilities. Alert routing was never reassigned. The queue accumulated over 4,000 exception events across Sunday and Monday, any threshold-based review of which would have triggered escalation within hours of go-live.
- **Normalized anomaly.** Associates and supervisors were briefed to expect post-upgrade "quirkiness." This briefing, intended to reduce friction, functioned as an instruction to suppress the exact human signal — "the scanner keeps sending me to the wrong bin" — that would otherwise have escalated Sunday morning. Override counts at 8x baseline were interpreted as expected settling rather than as an alarm, because no one had defined what "expected settling" should quantitatively look like.

### 6.4 Anchoring on the recent adjacent change (scanner misdiagnosis)

The nine-hour firmware rollback was a reasonable-sounding hypothesis actioned without falsification testing:

- The firmware push (November 17) was recent, scanner-related, and the symptoms presented at the scanner. The much larger change — a two-major-version WMS upgrade completed 31 hours earlier — was discounted because it had "passed" its checks, an assessment that treated the smoke tests as far stronger evidence than they were.
- No differential diagnosis was performed before committing the full IT team to a nine-hour irreversible-in-the-moment remediation. A ten-minute falsification test was available: hand-scan a known item at a known bin in an affected aisle using a device still on old firmware (several spares existed), or diff a sample of location records. Either would have eliminated the firmware hypothesis immediately.
- The incident bridge had no structured hypothesis-tracking discipline. The first plausible theory presented became the plan. Notably, the theory also located the fault in a change the team controlled (firmware) rather than in the vendor-led upgrade — a pattern worth naming without attributing it to any individual, because it recurs in incident response generally.

**Systemic gap:** the site's incident process has no requirement to enumerate candidate causes, rank them by change magnitude and recency, and run cheap falsification tests before committing to expensive remediations.

### 6.5 The paper picking tradeoff (containment)

The Wednesday decision to move to paper deserves specific analysis because it was simultaneously the most costly single operational decision of the incident and, on review, the correct one.

- **What it cost:** throughput fell 60 percent for 2.5 days; the 214,000-order backlog it allowed to build drove most of the $1.8 million expedited freight spend and the majority of late orders.
- **What it bought:** it stopped misshipments immediately. Modeling from the pre-containment error rate indicates that continuing system-directed picking through Black Friday weekend would have shipped an additional 55,000–70,000 wrong orders into 14 brands' peak season — an outcome plausibly costing multiples of the actual incident total in credits, returns, and client attrition.
- **What it exposed:** the paper contingency was improvised, not exercised. Pick sheet formats were designed overnight; most associates had never paper-picked; supervisor ratios were wrong for manual verification; and throughput at 31,000 units/day reflects an unpracticed process. A rehearsed degraded-mode procedure could plausibly have sustained 45,000–50,000 units/day, materially shrinking the backlog and the freight bill.

**Assessment:** right decision, made at the right level, executed without a playbook that should have existed.

### 6.6 Backup practices as an unplanned save

One contributing factor was positive and should be institutionalized rather than left to habit: the pre-upgrade location master export that enabled both root cause identification and the corrected reload existed because a team member retained it as personal practice, not because the runbook required it. The runbook's backup provisions covered database-level snapshots for full rollback — which were expired by the time the defect was found, the rollback window having closed Sunday morning. Without the ad hoc export, root cause identification and remediation would have taken materially longer.

---

## 7. What Worked and What Did Not

### 7.1 What worked

1. **Client-initiated detection was acted on immediately.** Once the returns signal arrived, escalation to SEV-1 took under an hour. No minimization, no delay.
2. **Containment decision-making was decisive and correctly weighted.** The paper picking decision consciously traded a measurable, recoverable cost (throughput) against an unbounded one (peak-season misshipments), was made by the accountable executive, and was communicated clearly to 1,150 associates within a shift.
3. **Hypothesis-driven analysis found the root cause.** The geographic clustering insight — errors by aisle, not by device or picker — redirected the investigation from runtime behavior to migrated data and produced root cause within 15 hours of the firmware hypothesis failing.
4. **Proactive client communication limited relationship damage.** Twice-daily updates to all 14 brands, initiated before root cause was known, were cited by multiple clients as the reason they held position. The terminating client cited the incident's operational facts, not the communication.
5. **Remediation was disciplined despite time pressure.** The corrected master was validated in staging with full field-level reconciliation, loaded during a shift break, verified with 400 cycle counts, and rolled out via audited pilot zones before full cutback — the day before Black Friday, when pressure to skip steps was maximal.
6. **The workforce absorbed extraordinary change.** A full building reverted to a manual process most associates had never used, then reverted back, across a holiday week, while sustaining an 11-day recovery push.
7. **Data retention (albeit informal) enabled recovery.** The pre-upgrade export was the single most valuable artifact of the incident.

### 7.2 What did not work

1. **Every automated safety net failed simultaneously and silently.** Migration validation, smoke tests, regression suite, exception alerting, and quality reporting all either passed corrupt data or failed to surface it in time. The system had multiple layers of defense; all were misconfigured, stale, or unowned.
2. **Detection took 31 hours and came from a client.** The site's own instrumentation never triggered the escalation. A client's returns dock was, functionally, our monitoring system.
3. **The two-shift reporting lag made the primary quality metric useless for incident detection.** By design, it can never catch anything faster than ~16 hours.
4. **Monitoring ownership did not survive an org change.** A single September transfer silently disabled the exception queue; no process existed to catch the orphaned responsibility.
5. **The misdiagnosis consumed nine hours without a falsification test.** The full IT team executed an expensive remediation against an untested hypothesis while erroneous shipments continued.
6. **Pre-cutover validation was theater relative to the risk.** Four days of parallel running against a clean subset, a template runbook, and a version-9.0-era regression suite provided the appearance of validation without meaningful coverage of the change actually being made.
7. **The "expect quirkiness" briefing suppressed the human alarm.** Frontline associates saw the problem Sunday morning and were procedurally conditioned to override it.
8. **No rehearsed degraded-mode operation existed.** Paper picking was improvised at 40 percent of achievable throughput.
9. **Schedule risk was accepted without governance.** The validation compressions that enabled this incident were decided below the level accountable for their consequences, with no written risk acceptance.

---

## 8. Action Items

Owners are accountable individuals; several items require vendor or cross-site participation, noted where applicable. Status reviews biweekly at site leadership meeting; the CI Manager tracks closure.

### Prevent (recurrence of the failure mode)

| # | Action | Owner | Due |
|---|---|---|---|
| A1 | Establish a change-freeze policy prohibiting major-version changes to WMS, host interfaces, and material handling control systems between October 15 and January 15 absent CEO-level written risk acceptance. | Bianca Cardoso-Reyes (VP Operations) | Jan 16, 2027 |
| A2 | Define minimum validation standards for major system changes: full-production-data parallel run of not less than 10 operating days; any reduction requires a written risk memo approved by the VP Operations and executive sponsor. | Ephraim Sackey (Dir. IT) | Feb 13, 2027 |
| A3 | Build and mandate a field-level source-to-target reconciliation for all master data migrations (locations, items, clients), with cutover go/no-go gated on 100 percent reconciliation. Productionize the diff tooling built during this incident. | Priya Raghunathan (WMS Applications Manager) | Feb 27, 2027 |
| A4 | Rebuild the regression suite against Baseline 11.0, including data-integrity cases, legacy-format location coverage, and smoke tests that span every location ID format in the building. Institute annual suite review tied to version currency. | Priya Raghunathan (WMS Applications Manager) | Mar 31, 2027 |
| A5 | Replace vendor template runbooks with site-owned cutover runbooks including mandatory data validation gates, retained-export requirements (formalizing the practice that saved this incident), and defined rollback triggers that remain valid post-go-live for 72 hours. | Ephraim Sackey (Dir. IT) | Mar 13, 2027 |
| A6 | Obtain from the vendor: (a) confirmed fix and regression coverage for the migration toolkit defect; (b) root cause report; (c) contract amendment adding data-integrity warranties and validation deliverables to future upgrades. | Ephraim Sackey (Dir. IT), with Legal | Feb 28, 2027 |

### Detect (shrink the 31-hour gap to under 2 hours)

| # | Action | Owner | Due |
|---|---|---|---|
| B1 | Deploy real-time pick accuracy and exception-rate dashboards with automated paging at defined thresholds (exception rate > 2x trailing 4-week baseline sustained 30 minutes). Retire the two-shift-lag report as a monitoring instrument. | Devon Okafor (Quality Assurance Manager) | Feb 6, 2027 |
| B2 | Audit all alert queues and monitoring responsibilities site-wide; assign primary and backup owners to each; add monitoring-responsibility transfer to the HR/IT personnel transfer checklist so no queue can be orphaned by an org change. | Devon Okafor (QA Manager), with HR | Jan 30, 2027 |
| B3 | Institute hypercare protocol for the first 72 hours after any system change: dedicated exception-queue watch each shift, hourly accuracy sampling via physical audit, and explicit quantitative definitions of "expected" post-change anomaly rates. Replace "expect quirkiness" briefings with "report anything unusual immediately, here is the channel." | Bianca Cardoso-Reyes (VP Operations) | Feb 6, 2027 |
| B4 | Create a frontline fast-path escalation channel (scan-a-QR-code incident report at every supervisor station) with a 30-minute acknowledgment SLA, so associate observations reach the incident process without supervisor filtering. | Devon Okafor (QA Manager) | Feb 20, 2027 |

### Respond (eliminate misdiagnosis and improvised containment)

| # | Action | Owner | Due |
|---|---|---|---|
| C1 | Add a structured differential-diagnosis step to the SEV-1 process: enumerate all changes in the trailing 14 days ranked by magnitude, and require a documented, cheap falsification test for the leading hypothesis before committing remediations estimated over 2 hours of effort. | Marguerite Lapointe (CI Manager) | Feb 13, 2027 |
| C2 | Develop, document, and drill a degraded-mode paper picking playbook (pre-built pick sheet templates, supervisor ratios, verification procedure, target throughput ≥ 45,000 units/day). Run a live 4-hour drill once per half. First drill by due date. | Bianca Cardoso-Reyes (VP Operations) | Apr 30, 2027 |
| C3 | Formalize the client crisis-communication protocol used in this incident (proactive notification triggers, twice-daily cadence, brand prioritization framework) as a standing playbook. | Tanya Whitehorse (Client Services Director) | Feb 27, 2027 |
| C4 | Conduct retention and remediation program for the terminating client and the two credited clients, including sharing this postmortem's action plan and quarterly evidence of completion. | Tanya Whitehorse (Client Services Director) | Ongoing; plan by Jan 23, 2027 |

### Govern (make risk tradeoffs visible)

| # | Action | Owner | Due |
|---|---|---|---|
| D1 | Institute a change-risk review board for all major system changes, chaired by VP Operations, with authority to approve schedules, validation scope, and any compression thereof. No validation activity may be reduced without a board-approved written risk acceptance. | Bianca Cardoso-Reyes (VP Operations) | Feb 27, 2027 |
| D2 | Present this postmortem and action-item status to the executive team and, in redacted form, to all 14 client brands. | Marguerite Lapointe (CI Manager) | Jan 16, 2027 |
| D3 | Conduct a 90-day effectiveness review verifying closure evidence for all items above; publish results to the same distribution as this document. | Marguerite Lapointe (CI Manager) | Apr 17, 2027 |

---

## 9. Closing Note

The most uncomfortable finding of this review is not the vendor's defective script — vendors ship defects, and always will. It is that Tannery Row's layered defenses were, in November 2026, largely decorative: a regression suite three versions stale, a parallel run that could not have caught the failure it existed to catch, a monitoring queue with no owner, and a quality report that reports history rather than the present. Each of these had decayed gradually and invisibly, and each decay was individually survivable. Together, they meant that when a defect finally arrived, the first functioning detector in the entire system was a client's returns dock, 31 hours and tens of thousands of orders too late.

The response, by contrast, showed the organization at its best once it had accurate information: decisive containment, disciplined root cause work, honest client communication, and an 11-day recovery executed through a holiday peak. The action plan above is therefore aimed almost entirely at the left side of the incident — validation, detection, and diagnosis — because that is where this incident was lost, and where the next one will be won.

**Document owner:** Marguerite Lapointe, Continuous Improvement Manager
**Next review:** April 17, 2027 (90-day effectiveness review, action item D3)

---

## Appendix A: Glossary of Terms

| Term | Definition |
|---|---|
| **Aisle prefix** | The leading segment of a pick location ID identifying the physical aisle (e.g., the "A14" in A14-03-B-02). Its truncation caused location records to resolve to bins in different aisles. |
| **Baseline** | The site's warehouse management system (WMS), vendor-supplied. Versions referenced: 9.0 (regression suite era), 9.2 (pre-upgrade production), 10.4 (skipped interim release), 11.0 (current production). |
| **Cutover** | The transition window during which the production system is migrated from the old version to the new, including data migration, verification, and go-live. |
| **Exception queue** | The WMS work queue collecting scan mismatches, short picks, and supervisor overrides for review and disposition. Designed to page its owner at volume thresholds. |
| **Hypercare** | An elevated-monitoring period immediately following a system change, with dedicated staffing and lowered escalation thresholds. Did not exist as formal practice at Rome prior to this incident. |
| **Location master** | The master data table defining all 214,000 physical storage and pick locations in the building, including their IDs, zones, and slotting attributes. |
| **Parallel validation / parallel run** | Operating a shadow instance of the new system version against mirrored or replayed production transactions to compare outputs before cutover. |
| **Pick accuracy** | Percentage of order lines picked with the correct item and quantity, measured via outbound audit sampling and returns reconciliation. Site baseline: 99.6 percent. |
| **RF picking** | Radio-frequency-directed picking: the WMS directs each associate to a location via handheld scanner, and the associate confirms by scanning the bin and item barcodes. |
| **Smoke test** | A brief post-change test of core functions to confirm basic system health. Not a substitute for regression or data-integrity testing. |
| **SEV-1** | Highest incident severity: material impact to client commitments or building-wide operations, requiring an incident commander and continuous bridge. |
| **Wave** | A batch of orders released to the floor for picking as a unit. |

---

## Appendix B: Error Distribution Analysis

Prepared by the Continuous Improvement team from exception logs, returns data, and the location master diff. This analysis is the evidentiary basis for the root cause finding in Section 5.

### B.1 Corruption distribution by zone

The 61,000 corrupted records were not randomly distributed. They corresponded exactly to locations created before the 2019 slotting redesign, concentrated in the building's original footprint:

| Zone | Total locations | Corrupted | % corrupted | Notes |
|---|---|---|---|---|
| Zone A (original build, 2011) | 48,200 | 44,900 | 93.2% | Almost entirely legacy-format IDs |
| Zone B (original build, 2011) | 41,600 | 15,400 | 37.0% | Partially re-slotted in 2019 |
| Zone C (2016 expansion) | 38,700 | 700 | 1.8% | Re-slotted 2019; residual legacy IDs |
| Zone D (2019 expansion) | 44,300 | 0 | 0% | Post-2019 format only |
| Zone E (2022 expansion) | 41,200 | 0 | 0% | Post-2019 format only |
| **Total** | **214,000** | **61,000** | **28.5%** | |

Two observations follow. First, the smoke-test zone sits inside Zone D — the cleanest zone in the building — which is why go-live verification passed. Second, the strong zone clustering is precisely the signal that, once noticed at 2:05 a.m. Thursday, redirected the investigation from runtime behavior (firmware, application logic) to migrated data. Errors caused by device firmware would distribute by device; errors caused by picker behavior would distribute by associate; these errors distributed by aisle construction era. Heat-mapping exception events against the building floor plan would have revealed this pattern as early as Sunday afternoon had anyone been looking at the exception queue.

### B.2 Exception volume by shift (reconstructed)

| Shift | Exception events | Baseline expected | Multiple of baseline |
|---|---|---|---|
| Sun Nov 22, day (reduced) | 340 | ~40 | 8.5x |
| Mon Nov 23, first | 1,870 | ~110 | 17x |
| Mon Nov 23, second | 2,140 | ~105 | 20x |
| Tue Nov 24, first (to 11:20 a.m.) | 1,390 | ~60 | 23x |

Cumulative unreviewed exception events at time of detection: approximately 5,740. The queue's paging threshold, had routing been active, was 3x baseline sustained for one hour — a condition first met at approximately 9:40 a.m. Sunday, November 22, roughly 5.5 hours after go-live. **A functioning exception queue would have compressed the detection gap from 31 hours to under 6.**

### B.3 Misshipment estimate reconciliation

| Source | Estimate | Basis |
|---|---|---|
| Pre-containment error-rate model | 43,500 units | (78,000 units/day × ~2.6 days × 8.4% error, adjusted for zone mix) |
| Returns and claims received (as of Dec 15) | 31,200 units | Actual; still accruing at ~600 units/day |
| Client-reported discrepancies | 39,800 units | Brand reconciliation files, 11 of 14 brands reporting |
| **Working estimate** | **41,000–46,000 units** | Convergence expected by end of January 2027 |

The 38,000-order figure in Section 2 counts *orders* affected (wrong or late); unit counts run higher because multi-line orders often contained multiple errors.

---

## Appendix C: Decision Log

Key decisions during the incident, recorded for the governance review (action item D1). Each entry notes the decision, the decision-maker, the information available at the time, and the retrospective assessment. The assessments evaluate the decision *process*, not outcomes known only in hindsight.

| # | Date/time | Decision | Decider | Information available | Retrospective assessment |
|---|---|---|---|---|---|
| DL-1 | Feb 2026 | Accept vendor request to move upgrade from May to November | Site leadership w/ vendor | Vendor assurances on tooling maturity, support, rollback | Defensible on its face, but should have triggered a formal peak-proximity risk review. No such mechanism existed. |
| DL-2 | Oct 2026 | Compress parallel validation from 14 days to 4; use subset extract | Project team | Schedule conflict with client onboarding freeze | **Process failure.** Decision made below accountable level; no risk memo; the compression eliminated the only test capable of catching the defect. |
| DL-3 | Nov 22, 4:10 a.m. | Declare go-live; close rollback window | Cutover lead w/ vendor concurrence | Smoke tests passed; record counts reconciled | Followed the runbook as written. The runbook's verification gates were inadequate; the decision inherited that inadequacy. |
| DL-4 | Nov 24, 12:50 p.m. | Commit full IT team to fleet firmware rollback | IT Director | Recent firmware push; scanner-presenting symptoms; upgrade "verified clean" | **Process failure.** Plausible hypothesis, but no falsification test performed and no alternative hypotheses tracked. A 10-minute test was available. |
| DL-5 | Nov 25, 6:00 a.m. | Revert building to paper picking | VP Operations | Error rate unabated post-rollback; Black Friday in 48 hrs; cause unknown | **Correct decision, correctly made.** Explicit tradeoff framing, right decision level, clear communication. Execution hampered by absence of a rehearsed playbook. |
| DL-6 | Nov 25, 9:00 a.m. | Proactively notify all 14 brands before root cause known | Client Services Director | Confirmed accuracy incident; containment in place | Correct. Cited by clients as trust-preserving. Now formalized (action C3). |
| DL-7 | Nov 26, 10:00 a.m. | Full staging validation of corrected master before production load, despite Black Friday pressure | IT Director w/ VP Operations | Confirmed root cause; vendor-patched script | Correct. Resisted pressure to hot-load; the two-hour reconciliation prevented any possibility of a second bad load. |
| DL-8 | Nov 27, 6:00 a.m. | Phased pilot-zone return to RF rather than building-wide cutback | VP Operations | 400/400 cycle counts clean | Correct. Cost ~8 hours of throughput; bought verified confidence entering the highest-volume day of the year. |
| DL-9 | Nov 27–Dec 8 | Authorize $1.8M expedited freight, prioritized by contractual exposure and client risk | VP Operations w/ Client Services | Backlog model; brand-by-brand SLA exposure | Reasonable. Post-incident modeling suggests a rehearsed degraded mode (action C2) would have reduced this spend by an estimated $500K–$700K. |

---

## Appendix D: Client Communication Record (Summary)

Maintained by Client Services. Full correspondence archived under INC-2026-1122/comms.

| Date | Communication | Audience |
|---|---|---|
| Nov 24, 1:45 p.m. | Initial acknowledgment to reporting brand: incident confirmed, investigation underway | 1 brand |
| Nov 25, 9:00 a.m. | Proactive incident notification: known accuracy issue, containment implemented, cadence commitment | All 14 brands |
| Nov 25 – Nov 27 | Twice-daily written updates (9 a.m. / 6 p.m.): status, containment metrics, root cause progress | All 14 brands |
| Nov 26, 8:00 a.m. | Root cause identified notice; remediation plan and timeline | All 14 brands |
| Nov 27, 4:00 p.m. | Resolution notice: full RF operation restored; backlog recovery plan and per-brand impact estimates | All 14 brands |
| Nov 28 – Dec 8 | Daily backlog burn-down reports with per-brand order status files | All 14 brands |
| Dec 9 | Incident closure notice; commitment to share postmortem findings | All 14 brands |
| Dec 11 – Dec 15 | Individual account reviews; service credit processing (2 brands); retention discussions opened (1 brand) | 3 brands |
| Jan 16, 2027 (planned) | Redacted postmortem and action plan distribution (action D2) | All 14 brands |

---

## Appendix E: Backlog Burn-Down

| Date | Orders in backlog (EOD) | Daily shipped | Notes |
|---|---|---|---|
| Nov 25 (Wed) | 47,000 | 31,000 | Paper picking day 1 |
| Nov 26 (Thu) | 96,000 | 30,500 | Paper picking; Thanksgiving reduced inbound demand |
| Nov 27 (Fri) | 214,000 | 52,000 | RF restored 2 p.m.; Black Friday order surge |
| Nov 28 (Sat) | 219,000 | 89,000 | Peak demand exceeded elevated capacity |
| Nov 29 (Sun) | 205,000 | 84,000 | Extended shifts begin |
| Nov 30 (Mon) | 181,000 | 96,000 | Cyber Monday; temp labor onboarded |
| Dec 1 (Tue) | 152,000 | 91,000 | |
| Dec 2 (Wed) | 121,000 | 88,000 | |
| Dec 3 (Thu) | 92,000 | 86,000 | |
| Dec 4 (Fri) | 64,000 | 85,000 | |
| Dec 5 (Sat) | 38,000 | 82,000 | |
| Dec 6 (Sun) | 17,000 | 78,000 | |
| Dec 7 (Mon) | 4,000 | 84,000 | |
| Dec 8 (Mon) | 0 | 79,000 | Backlog cleared; standard operations resume Dec 9 |

Peak sustained throughput during recovery (96,000 units, Nov 30) exceeded the building's rated capacity by 23 percent, achieved through extended shifts, weekend operation, and 140 temporary associates. This figure now informs the site's documented surge-capacity planning assumption.

---

## Appendix F: Related Documents and Evidence Index

| Ref | Document | Location |
|---|---|---|
| F-1 | Baseline 11.0 cutover runbook (vendor template, as executed) | INC-2026-1122/evidence/runbook-v11-executed.pdf |
| F-2 | Pre-upgrade location master export (Nov 21, 5:52 p.m.) | INC-2026-1122/evidence/locmaster-92-final.csv |
| F-3 | Location master diff output (Nov 26, 2:05 a.m.) | INC-2026-1122/evidence/locmaster-diff-20261126.xlsx |
| F-4 | Vendor defect confirmation and product ticket (BASE-11-4471) | INC-2026-1122/evidence/vendor-rca-draft.pdf |
| F-5 | Exception queue export, Nov 22–24 | INC-2026-1122/evidence/exception-log-full.csv |
| F-6 | Firmware rollback change record (CHG-2026-3318) | IT change management system |
| F-7 | Incident bridge notes and timeline (contemporaneous) | INC-2026-1122/bridge-notes/ |
| F-8 | February 2026 reschedule decision record | Project archive, Baseline-11 program folder |
| F-9 | Financial impact reconciliation workbook | Finance, restricted access |
| F-10 | Client communication archive | INC-2026-1122/comms/ |

---

## Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | Dec 10, 2026 | M. Lapointe | Initial draft; timeline and impact sections |
| 0.2 | Dec 12, 2026 | M. Lapointe | Added root cause, contributing factors; incorporated vendor defect confirmation (F-4) |
| 0.3 | Dec 15, 2026 | M. Lapointe | Financial figures reconciled with Finance; appendices B and E added |
| 0.9 | Dec 16, 2026 | Review group | Blameless-language review; decision log added at VP Operations request; action item owners and dates confirmed by each owner |
| 1.0 | Dec 18, 2026 | M. Lapointe | Final. Published to distribution list |

---

*End of document. Questions, corrections, or additional evidence should be directed to the document owner. This postmortem will be amended if the vendor's final root cause report (expected February 2027) or the ongoing client reconciliation materially changes any finding herein.*
