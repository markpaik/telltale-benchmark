# Settlement Platform Modernization Program

**A Proposal to the Board of Directors of Meridian Ledger, Inc.**

**Submitted by:** Rosalind Achebe, Chief Executive Officer, and Viktor Petrosyan, Chief Technology Officer
**Date of submission:** February 18, 2026
**Board meeting:** March 4, 2026
**Authorization requested:** $19,800,000 over 26 months, with staged release against defined gates

---

## 1. Executive Summary

We ask the Board to authorize a $19.8 million, 26-month program to replace the COBOL settlement engine that has run Meridian Ledger's core product since 2009, and to move production from a single leased facility in Council Bluffs to a two-site active-active configuration. We ask for the authorization on March 4 because the schedule requires hiring to begin in March, because our largest customer has demanded a remediation plan before an October 1 renewal, and because the engineering staff who understand the current system are leaving.

The December 27 outage is the proximate cause. Nine hours of downtime delayed settlement for 118 institutions, produced $2.1 million in service credits, and required manual reconciliation by client staff on a Saturday between Christmas and New Year. The root cause was a change to a batch scheduling parameter that interacted with a date-handling routine written in 2011 by an engineer who left the company in 2017. No one on the current staff had read that routine before December 27. Four people found the defect in six hours because they knew where to look; three of them are over 55.

That is the real exposure. The technology risk and the personnel risk are the same risk. We have four engineers who can safely modify the settlement engine. Their average age is 58. Dennis Okonkwo retires April 17. When the count reaches three we lose the ability to run two independent reviewers on a settlement change, which is the control that our last SOC 2 Type II already flagged as deficient — two exceptions on change management, both concerning insufficient segregation of review and approval. We cannot remediate those exceptions with the staff we have, and we cannot hire our way out because the labor market for production COBOL on a proprietary settlement engine is, in Omaha, approximately four people, and we employ all of them.

The Board is right to be skeptical. In 2022 we spent $4.3 million on a modernization attempt and shipped nothing. Section 9 sets out what went wrong in that program and what is structurally different in this one. The short version: the 2022 program had no parallel run, no defined scope freeze, no separate program leadership, and no gate at which the Board could stop it. This program has all four. We are asking for staged release of funds against four gates, and we are asking the Board to hold the authority to terminate at each.

We evaluated three alternatives: continue to patch, license a third-party settlement platform, and rebuild. Continuing to patch is not a strategy, it is a decision to accept an outage of unknown duration at an unknown date with a staff that shrinks by one engineer per year. Licensing a third-party platform is genuinely attractive on cost and we came close to recommending it; we did not, for reasons of margin structure and customer concentration that Section 8 sets out in detail. Rebuilding is the most expensive option and the one we recommend.

**The decision requested:** authorize $19.8 million, release $4.2 million immediately for Phase 1, and delegate to the Audit and Risk Committee the authority to release subsequent phases against the gate criteria in Section 7.

---

## 2. Why Now

### 2.1 The December 27 outage

At 04:12 Central on Saturday, December 27, the overnight settlement batch for the Central region failed to complete. The failure was not detected by automated monitoring because the batch had not failed — it had entered a state in which it reported progress while processing zero records, a condition our monitoring does not test for. The on-call engineer was paged at 05:40 by a client, not by our systems. Full settlement was restored at 13:07.

One hundred eighteen institutions had delayed settlement. Forty-one had to hold ACH origination files. Nine reported customer-visible impact — declined debit transactions at institutions that hold intraday positions tightly. We issued $2.1 million in credits under contractual SLA terms, of which $1.4 million went to eleven institutions and $700,000 was spread across the remaining 107.

The technical cause was a change made December 19 to the batch window parameter for a client onboarding in the Mountain region. The parameter change was correct. Its interaction with a date-boundary routine in module SETL0447 was not, and produced a condition in which the batch believed it had already run. SETL0447 was written in 2011. It has 1,840 lines. It is not documented. It has been modified fourteen times. No test in our regression suite exercised the specific date boundary that occurred on December 27, because the suite was built from historical defects and this defect had never occurred before.

We do not think this specific failure will recur; we patched it December 29. We think failures of this class will recur, because there are approximately 340 modules in the settlement engine of comparable age and documentation quality, and we have no systematic way to find the next one.

### 2.2 Key-person concentration

| Engineer | Age | Years on settlement engine | Status |
|---|---|---|---|
| Dennis Okonkwo | 63 | 17 | Retires April 17, 2026 |
| Marguerite Lindqvist | 61 | 14 | Has declined to commit past 2027 |
| Samuel Achterberg | 57 | 11 | No stated plan |
| Priya Ramanathan | 51 | 9 | No stated plan |

Mr. Okonkwo has agreed to a twelve-month advisory contract at 12 hours per week beginning May 1. That is a mitigation, not a solution; advisory hours cannot substitute for the ability to debug a production incident at 05:00.

The SOC 2 Type II exceptions follow directly from this table. Our change management policy requires an independent reviewer and an independent approver for production changes to settlement logic. With four qualified engineers, one of whom is frequently the author, we can satisfy this on most changes but not all. The auditor sampled 40 settlement changes and found 6 in which reviewer and approver were the same person, and 3 in which the reviewer had not, by their own account, read the changed code in full. Both exceptions are rated as significant deficiencies rather than material weaknesses. At three qualified engineers we expect the auditor to escalate.

Two of our largest clients require an unqualified SOC 2 Type II as a condition of contract. A material weakness finding would put those contracts in breach.

### 2.3 The Cascade Prairie renewal

Cascade Prairie Bancorp represents $5.2 million of annual recurring revenue, 11 percent of the total, across 28 charters. Their contract renews October 1, 2026. On January 8, their Chief Information Officer, Theodore Vasquez, wrote to Nadia Farouk requesting "a documented remediation plan with dated milestones addressing the architectural causes of the December 27 event, not the proximate cause." A follow-up call on January 22 made clear that Cascade Prairie's board had asked their management to evaluate alternatives.

Cascade Prairie is not likely to leave in 2026 — the switching cost for 28 charters is high and the timeline is short. They are likely to run a competitive evaluation for a 2028 or 2029 transition if we cannot demonstrate a credible plan. A Board-authorized, funded, dated program is the strongest response available to us. An unfunded intention is not.

Ms. Farouk's assessment, which we endorse: the probability of losing Cascade Prairie within 36 months is approximately 15 percent if this program is authorized and executing to plan, and approximately 45 percent if it is not.

### 2.4 The single data center

Council Bluffs is a leased facility with a single utility feed, N+1 cooling, and a diesel generator we test monthly. Our recovery point objective is 15 minutes and our recovery time objective is four hours, achieved by asynchronous replication to a colocation cage in Des Moines that holds standby hardware but has never processed live settlement volume. We have tested failover twice, both times in a maintenance window, both times with partial success.

We would not survive a total loss of Council Bluffs within our stated RTO. We have told clients we would. This is the single largest gap between our represented and actual resilience posture, and it is the item that most concerns Ms. Farouk.

---

## 3. Risk in the Current Stack

**Language and runtime.** The settlement engine is approximately 640,000 lines of COBOL running on a Micro Focus runtime on Red Hat Enterprise Linux. The runtime is supported. The code is not maintainable in any meaningful sense: no module-level ownership, no automated test coverage below 20 percent, no static analysis, and a build process that requires manual steps documented in a wiki page last updated in 2019.

**Data model.** Settlement state lives in a DB2 instance with 1,100 tables, of which we believe 340 are active. We say "believe" because there is no data dictionary. Approximately 60 tables are written by more than one module without a defined ownership convention, which is the source of the majority of our data-integrity incidents.

**Batch dependency.** Settlement is a batch process with a four-hour window. Institutions that need intraday position updates are served by a read replica that lags the batch. Six clients have asked for real-time settlement visibility; we have declined all six because the architecture cannot support it. This is a competitive exposure as much as a risk one.

**Change management.** Median time from code change to production for settlement logic is 34 days. Emergency changes bypass three of eight control steps. The SOC 2 exceptions arise here.

**Observability.** We have host-level and process-level monitoring. We have no transaction-level tracing, which is why the December 27 batch could report healthy while processing nothing.

**Third-party dependencies.** Four integrations — Fedwire, ACH via a correspondent, a card network, and a wire screening vendor — are implemented as bespoke COBOL adapters. Two of the four use file drops over SFTP with formats defined in the 2010s. The wire screening vendor has notified us that their file interface sunsets in Q3 2027.

That last point deserves emphasis. Even under a decision to continue patching, we face a mandatory integration rewrite by Q3 2027. The "do nothing" option is not actually available; it is a decision to do the same work later, under deadline pressure, with fewer engineers.

---

## 4. Target Architecture

### 4.1 Principles

1. **Settlement logic must be readable by an engineer hired last month.** Every architectural choice is subordinate to this.
2. **Correctness is demonstrated by comparison, not by assertion.** The parallel run is the core of the program, not an appendix.
3. **No new functional scope.** The target system does what the current system does. Real-time settlement, intraday visibility, and the six client requests we have declined are explicitly out of scope and will be considered as roadmap items after cutover.
4. **Two sites, both live.** No standby-that-has-never-run.

### 4.2 Components

**Settlement core.** A Java 21 service implementing settlement logic as an explicit state machine over a ledger of immutable entries. Business rules — netting, cut-off handling, holiday calendars, exception routing — are expressed in a rules module with declarative configuration per institution, replacing approximately 90 client-specific COBOL branches. Target test coverage on settlement logic is 85 percent line, 100 percent of documented business rules covered by a named test.

**Ledger store.** PostgreSQL 16 with logical replication between sites, append-only entry tables, partitioned by settlement date. Single-writer per settlement group with explicit ownership; no shared-write tables.

**Event backbone.** Kafka for inter-service events and for the comparison feed that drives the parallel run. Retention of 30 days on settlement topics.

**Integration adapters.** Four rewritten adapters — Fedwire, ACH, card network, wire screening — with the wire screening adapter targeting the vendor's post-2027 API, resolving the sunset dependency inside this program rather than as separate work.

**Observability.** OpenTelemetry tracing on every settlement transaction, with SLOs defined per settlement group and alerting on rate-of-progress rather than process liveness. A batch that processes zero records will page.

**Topology.** Two leased facilities: Council Bluffs (existing, renegotiated) and a second site in the Kansas City metro, selected for network path diversity and a separate utility region. Active-active for read traffic and for non-settlement services; active-passive with sub-five-minute promotion for the settlement writer, because we are not prepared to accept the correctness risk of multi-master settlement writes. Target RPO under 60 seconds, RTO under 20 minutes, both to be demonstrated by unannounced failover tests quarterly from Phase 3 onward.

### 4.3 Migration approach

We reject a big-bang cutover. We propose a strangler pattern with a mandatory six-month parallel run.

**Stage A — Shadow read.** New engine consumes the same input feeds, computes settlement, writes to its own ledger, produces no client-visible output. Outputs compared to production, discrepancies triaged daily.

**Stage B — Parallel run, production-of-record unchanged.** Both engines process live volume for six months. Current engine remains authoritative. Discrepancy rate must reach and hold zero material discrepancies for 60 consecutive days before Stage C.

**Stage C — Cohort cutover.** New engine becomes authoritative for cohorts of institutions, smallest first. Five cohorts: 20 institutions, then 45, then 80, then 100, then 95. Minimum 21 days between cohorts. Old engine continues to shadow every cohort for 90 days after cutover, providing a rollback path.

**Stage D — Decommission.** Old engine retired 90 days after final cohort. DB2 licenses released. Council Bluffs footprint reduced.

The rollback boundary is the cohort. At every point after Stage C begins, we can return any cohort to the old engine within one settlement cycle, because the old engine has never stopped running for that cohort. This is what the 2022 program lacked and it is the single most important structural difference.

**Definition of a material discrepancy:** any difference in settled position, timing of settlement, or exception routing that would be visible to an institution or affect its books. Formatting differences, internal identifiers, and log content are non-material. The Audit and Risk Committee will receive the discrepancy log monthly from Stage A onward.

---

## 5. Staffing Plan

### 5.1 Program leadership

We propose a dedicated program organization reporting to the CTO, with a full-time Program Director hired externally at Director level. This is a departure from 2022, when the modernization effort was led by an engineering manager who retained line responsibilities and was consequently unable to hold scope.

The Program Director owns schedule, scope, and gate readiness, and reports to the Audit and Risk Committee monthly in writing. We are budgeting for a search and expect the role filled by May.

### 5.2 Team structure

| Team | Size at peak | Responsibility |
|---|---|---|
| Settlement Core | 11 | Settlement state machine, rules engine, ledger |
| Data & Migration | 6 | Data model, migration tooling, reconciliation |
| Platform & SRE | 7 | Two-site build, observability, failover |
| Integrations | 5 | Four adapter rewrites |
| Parallel Run & Assurance | 5 | Comparison harness, discrepancy triage, cutover |
| Program & Change | 3 | Program Director, TPM, change/comms |
| **Total** | **37** | |

Of 37 seats, 23 are filled from existing staff and 14 are new hires.

### 5.3 The fourteen hires

| Role | Count | Notes |
|---|---|---|
| Senior Java engineers (settlement domain) | 5 | Payments or core banking background required |
| Site reliability engineers | 3 | One with active-active Postgres experience |
| Data engineers | 2 | Migration and reconciliation tooling |
| QA automation engineers | 2 | Comparison harness |
| Program Director | 1 | External, Director level |
| Technical program manager | 1 | |

Meiling Zhou's hiring plan assumes a 14-week median time-to-fill and a 20 percent premium over current bands for the senior Java roles, both reflected in the budget. Six of fourteen are targeted for Q2, six for Q3, two for Q4.

The largest staffing risk is not the count but the sequencing: the settlement core team must be at eight engineers by August 1 to hold the Phase 2 date. If it is at five, the schedule moves. We have budgeted for two contract senior engineers as a bridge, at a cost premium, to be engaged only if the August headcount is short.

### 5.4 The legacy engineers

None of the four current settlement engineers moves to the new engine full-time. This is deliberate and it is the most-questioned decision in the plan, so we will state the reasoning.

The old engine must be operated flawlessly for 26 months. If we move the people who understand it onto the new build, we degrade the thing we are trying to protect. Instead:

- Ms. Lindqvist, Mr. Achterberg, and Ms. Ramanathan remain on the current engine, at 30 percent time allocated to the new program as domain consultants — rule extraction, discrepancy triage, and review of the rules configuration.
- Mr. Okonkwo's advisory contract, 12 hours weekly from May 1 for twelve months, is directed entirely at rule extraction and documentation of the 340 active modules.
- We add two mid-level engineers to the current engine team in Q2, funded from run-rate rather than program budget, to build bench depth on the legacy system. These are not part of the fourteen.

Rule extraction is the critical path activity of Phase 1. If we cannot document what the current system does, we cannot build a system that does the same thing, and the parallel run becomes an exercise in discovering requirements at the worst possible moment.

### 5.5 Roadmap impact

Nine engineers move from product roadmap to program. Ms. Zhou's assessment of the consequence:

**Deferred, committed to clients:**

- **Real-time payments (RTP) send capability** — committed to 14 institutions for Q3 2026, deferred to Q2 2027. Contractual exposure is limited; these were roadmap commitments in QBRs, not contract amendments. Reputational exposure is real, particularly at three institutions that have told their own boards.
- **Digital account opening API v3** — committed to 9 institutions for Q4 2026, deferred to Q3 2027. Two institutions have integration work underway that will idle.

**Deferred, uncommitted:** fraud scoring enhancements, reporting redesign, two smaller integrations. Approximately 14 months of aggregate roadmap capacity.

**Not deferred:** all regulatory and compliance work, all security patching, all client-specific configuration work, and the standard support burden. These are ring-fenced. The program does not draw on the client-facing support organization.

Ms. Zhou's judgment, which we share: the RTP deferral is the one that hurts. It is a competitive gap and two competitors ship it today. We accept it because an institution that leaves over a missing feature is a slower loss than an institution that leaves over a settlement outage, and because we cannot do both.

---

## 6. Cost and Funding

### 6.1 Program budget

| Category | Line item | Amount |
|---|---|---|
| **Engineering** | | **$11,400,000** |
| | New hire compensation, loaded (14 FTE, ramped) | $4,180,000 |
| | Internal reallocated staff, loaded (23 FTE, allocated share) | $5,020,000 |
| | Contract engineering bridge (conditional) | $740,000 |
| | Program leadership and TPM | $620,000 |
| | Recruiting fees and search | $410,000 |
| | Training, certification, tooling licenses | $430,000 |
| **Infrastructure** | | **$3,600,000** |
| | Second data center: lease, buildout, cross-connects (26 mo.) | $1,240,000 |
| | Compute and storage hardware, both sites | $1,090,000 |
| | Network: diverse paths, circuits, DDoS/edge | $385,000 |
| | Software licenses: Postgres support, Kafka, observability | $520,000 |
| | Dual-running infrastructure overlap (old + new) | $365,000 |
| **Parallel Run** | | **$2,900,000** |
| | Comparison harness build and operation | $780,000 |
| | Discrepancy triage staffing (26 mo.) | $960,000 |
| | Duplicate compute and storage during parallel period | $610,000 |
| | Cutover operations, cohort rehearsals, war-room coverage | $340,000 |
| | Independent third-party assurance review (2 engagements) | $210,000 |
| **Contingency** | | **$1,900,000** |
| | Schedule contingency (3 months at burn) | $1,050,000 |
| | Scope/technical contingency | $560,000 |
| | Cutover reserve (rollback, client remediation) | $290,000 |
| **Total** | | **$19,800,000** |

Contingency is 9.6 percent of the total and 10.6 percent of the non-contingency base. This is at the low end of industry practice for a program of this type, and we want the Board to understand that we chose it deliberately: a larger contingency would have been defensible, but we prefer to return to the Board for a specific, justified increment than to hold a reserve that invites scope drift. Contingency release requires Program Director request and CFO approval, with any single draw above $250,000 requiring Audit and Risk Committee notification.

### 6.2 Spend profile

| Period | Phase | Spend | Cumulative |
|---|---|---|---|
| Q2 2026 | Phase 1 | $1,650,000 | $1,650,000 |
| Q3 2026 | Phase 1–2 | $2,550,000 | $4,200,000 |
| Q4 2026 | Phase 2 | $2,720,000 | $6,920,000 |
| Q1 2027 | Phase 2 | $2,610,000 | $9,530,000 |
| Q2 2027 | Phase 3 | $2,480,000 | $12,010,000 |
| Q3 2027 | Phase 3 | $2,390,000 | $14,400,000 |
| Q4 2027 | Phase 3–4 | $2,210,000 | $16,610,000 |
| Q1 2028 | Phase 4 | $1,840,000 | $18,450,000 |
| Q2 2028 | Phase 4 / close | $1,350,000 | $19,800,000 |

### 6.3 Funding

Harold Brantley proposes $12.0 million from operating cash and $7.8 million drawn on the existing growth facility.

Operating cash at January 31 was $18.4 million with trailing twelve-month operating cash generation of $9.2 million. The $12.0 million is drawn over nine quarters, peaking at a $2.1 million quarterly draw, and Mr. Brantley's model retains a minimum cash balance of $9.5 million throughout — above the $7.0 million floor the Board set in 2024.

The growth facility permits drawings to $15.0 million and carries a covenant capping total leverage at 3.0x trailing twelve-month EBITDA, tested quarterly. Current position:

| Measure | Value |
|---|---|
| TTM EBITDA (Dec 31, 2025) | $8.9M |
| Existing debt | $4.2M |
| Current leverage | 0.47x |
| Covenant cap | 3.00x |
| Proposed incremental draw | $7.8M |
| Pro forma debt at full draw | $12.0M |
| Pro forma leverage at current EBITDA | 1.35x |
| Headroom at 3.0x | $14.7M of debt capacity |

Headroom is substantial, but it is a function of EBITDA, and EBITDA is under pressure from this program. Program costs are approximately 62 percent capitalizable under our policy and 38 percent expensed, which Mr. Brantley models as a $2.6 million to $3.1 million annual EBITDA drag in 2027, the peak year. At $6.0 million EBITDA and $12.0 million debt, leverage reaches 2.00x — still inside the covenant, but the margin narrows.

The scenario that breaches is EBITDA below $4.0 million with the facility fully drawn. That requires the program drag plus loss of a major client plus flat new bookings. Loss of Cascade Prairie alone, at $5.2 million ARR and roughly $3.4 million of contribution, would produce approximately $3.5 million EBITDA against $12.0 million debt — a leverage ratio of 3.43x and a covenant breach.

We want this stated plainly because it cuts both ways. **The covenant risk in this program is dominated by client retention, and client retention is the thing the program is meant to protect.** Not doing the program does not eliminate the covenant risk; it raises the probability of the event that causes the breach while removing the tool that prevents it.

Mitigations: (a) draw the facility in tranches tied to phase gates rather than at close, so exposure builds with progress; (b) Mr. Brantley to open discussions with the lender in Q2 on a covenant holiday or EBITDA add-back for defined program costs, which is a common accommodation and which we would expect to secure; (c) hold $3.0 million of the operating cash allocation as a substitutable source, allowing us to reduce the draw if EBITDA underperforms.

### 6.4 What we avoid

The program is not justified by cost avoidance, but the Board should have the figures.

| Avoided cost | Annual | Basis |
|---|---|---|
| DB2 and mainframe-adjacent licensing | $610,000 | Post-decommission, from 2029 |
| SLA credits (expected value) | $840,000 | 3-year average, adjusted |
| Legacy engineer premium / retention | $290,000 | Above-band retention on 4 roles |
| Change velocity (deferred revenue recovery) | Not quantified | 34-day median change cycle |

Approximately $1.7 million of annual run-rate reduction from 2029. Against $19.8 million, a simple payback in excess of eleven years. **We are not proposing this on payback.** We are proposing it because the current system carries a risk of catastrophic failure that we cannot quantify and cannot mitigate with the staff we have.

---

## 7. Schedule and Gates

### Phase 1 — Foundation and Extraction (March – September 2026, 7 months, $4.2M)

Hire the Program Director and the first six engineers. Complete rule extraction and documentation of the 340 active settlement modules, led by Mr. Okonkwo's advisory engagement and the three remaining legacy engineers at 30 percent. Sign the second data center lease and begin buildout. Stand up development and test environments. Build the comparison harness. Deliver the settlement state machine for the two simplest settlement groups. Deliver the remediation plan document to Cascade Prairie by **June 15**, ahead of the October 1 renewal.

*Gate 1 (September 2026):* rule documentation complete and reviewed by two legacy engineers; comparison harness operational against historical data; second site under lease with power and network delivered; settlement core team at eight or greater; spend within 10 percent of plan.

### Phase 2 — Build and Shadow (October 2026 – December 2027, 15 months, $10.2M cumulative through Q4 2027 less Phase 1)

Complete the settlement core across all settlement groups. Rewrite all four integration adapters, with wire screening targeting the post-sunset API. Complete the second site and establish replication. Begin **Stage A shadow read** in March 2027. Begin **Stage B parallel run** in July 2027 — six months of both engines on live volume, old engine authoritative.

*Gate 2 (December 2027):* parallel run has completed six months; material discrepancy rate zero for 60 consecutive days; two-site failover demonstrated in unannounced test meeting RTO under 20 minutes and RPO under 60 seconds; independent third-party assurance review complete with no critical findings; cutover runbooks rehearsed twice.

### Phase 3 — Cohort Cutover (January – July 2028, 7 months)

Five cohorts at minimum 21-day intervals: 20 institutions, 45, 80, 100, 95. Old engine shadows each cohort for 90 days post-cutover. Rollback available per cohort within one settlement cycle.

*Gate 3 (per cohort):* prior cohort stable 21 days with zero material discrepancies and no SLA breach; Audit and Risk Committee notified before each cohort; **CRO holds unilateral authority to pause the sequence.**

### Phase 4 — Decommission and Close (August 2028 – December 2028)

Old engine retired 90 days after final cohort. DB2 licenses released. Council Bluffs footprint reduced. SOC 2 Type II with new control environment. Program closeout report to Board.

*Gate 4:* clean SOC 2 Type II; decommission complete; benefits realization reported.

**Total elapsed: 26 months from March 2026 authorization to close.** The three months of schedule contingency in the budget are not in this timeline; if consumed, close moves to Q1 2029.

---

## 8. Alternatives Considered

### 8.1 Continue to patch

Retain the COBOL engine, hire and train replacement COBOL engineers, invest in test coverage and observability, and address the wire screening sunset as standalone work.

Estimated cost: $4.8 million over three years — three COBOL-capable hires at a market premium, a test-coverage program, observability retrofit, adapter rewrite for wire screening, and second-site work which is required regardless.

**Rejected.** Not because of cost but because it does not work. The COBOL hires do not exist in a quantity we can source; we ran a search in 2024 and filled zero of two roles in nine months. Test coverage retrofit on undocumented code requires the same rule extraction as a rewrite, at similar cost, without the benefit. And the option fails the Cascade Prairie test: "we have hired more COBOL engineers" is not a remediation plan that survives a CIO's board presentation.

The option also understates its own cost. Second site, wire screening rewrite, and observability are required in every scenario and total roughly $3.9 million of the $4.8 million. The genuine incremental cost of *not* modernizing is under $1 million — which tells you the option is not really a plan, it is a deferral.

### 8.2 License a third-party settlement platform

We ran a structured evaluation between January 12 and February 10 with three vendors. Two returned indicative proposals: a tier-one core banking vendor whose settlement module serves institutions of our clients' size, and a specialist payments platform.

Indicative economics for the stronger of the two:

| Item | Amount |
|---|---|
| License, initial 5 years | $8,200,000 |
| Implementation and integration (vendor + internal) | $6,400,000 |
| Data migration | $1,900,000 |
| Internal program cost | $2,800,000 |
| **Five-year total** | **$19,300,000** |
| Annual license, years 6+ | $2,050,000 |

Cost is comparable in five years and materially worse in ten — $2.05 million of annual license against roughly $600,000 of incremental run cost for a system we own.

**Rejected for three reasons.**

*Margin structure.* At $2.05 million annual license against $47 million ARR, we transfer 4.4 percent of revenue to a vendor permanently, on a cost base that grows with our client count. Our gross margin is 71 percent; this takes it to approximately 66 percent, and it takes it in the direction we cannot recover, because the license scales with the business.

*Client-specific logic.* Approximately 90 client-specific settlement branches encode arrangements our institutions depend on — non-standard cut-offs, netting conventions, exception routing to specific operations teams. Both vendors proposed handling these through configuration and, where configuration was insufficient, through "customization services." Neither would commit to covering all 90 in the base implementation. Our estimate is that 30 to 40 would require customization, at a cost the proposals did not bound and on a timeline the vendor controls. This is the single largest risk in the option and it is unpriced.

*Cascade Prairie and the concentration problem.* Cascade Prairie's 28 charters run 22 of the 90 client-specific branches. A vendor implementation that cannot replicate them puts an 11-percent-of-revenue relationship in the vendor's hands during the renewal window. We are not willing to make our largest client's retention dependent on a third party's implementation team.

We want the Board to know this was close. If our client base were more homogeneous, or our concentration lower, the vendor option would likely win. We are recommending against it on structure, not on price, and we would revisit it if Gate 1 or Gate 2 fails.

### 8.3 Rebuild (recommended)

Set out above. Most expensive, longest, highest execution risk, and the only option that resolves the personnel concentration, the SOC 2 exceptions, the single-site exposure, and the wire screening sunset within one program, while retaining the client-specific logic that our concentration makes non-negotiable.

### 8.4 Hybrid: rebuild core, license periphery

Briefly considered: rebuild settlement, license adapters and reconciliation. Rejected — the integration work is 12 percent of program cost and the coordination overhead of a vendor on the critical path exceeds the saving.

---

## 9. What Went Wrong in 2022, and What Is Different

The Board's skepticism is earned. The 2022 program consumed $4.3 million over 14 months and was cancelled in November 2023 with no production deliverable. Our post-mortem, conducted in early 2024, identified four causes.

**1. Scope was never frozen.** The 2022 program began as a settlement rewrite and accumulated real-time payments, a new reporting layer, and a client portal refresh. At cancellation the scope was roughly 2.4 times the original.
*Different now:* scope is explicitly frozen to functional parity. No new client-facing capability is in scope. Scope changes require Audit and Risk Committee approval, not CTO approval. We have written the six declined client requests into Section 4.1 as out-of-scope so that they cannot re-enter quietly.

**2. No parallel run.** The 2022 plan called for a weekend cutover with a rollback window of six hours. As the date approached the team could not convince itself the cutover was safe, and could not prove it either way, because there was no mechanism for comparing outputs. The program stalled at 80 percent complete and was cancelled.
*Different now:* the parallel run is $2.9 million and six months, and it is the largest single de-risking investment in the program. Correctness is demonstrated by 60 consecutive days of zero material discrepancy on live volume before any client is moved.

**3. Leadership was part-time.** The 2022 program was led by an engineering manager who retained a line team of nine. When production incidents occurred, the program lost its leader for days at a time.
*Different now:* a full-time external Program Director at Director level, no line responsibilities, monthly written reporting to the Audit and Risk Committee.

**4. No stopping point.** The 2022 program had no gates. The Board received quarterly updates that reported percentage-complete against a plan that was itself moving. There was no defined moment at which the Board could ask "should we continue?" with the information to answer it.
*Different now:* four gates with objective, pre-defined criteria and staged fund release. The Board is asked to authorize $19.8 million but to release $4.2 million. Everything after Gate 1 is a decision the Board still holds.

A fifth difference is not from the post-mortem but is worth stating: **the legacy engineers stay on the legacy system.** In 2022 we moved three of four settlement engineers onto the new build. Production stability degraded, they were pulled back to firefight, and the new build lost its domain knowledge at the moment it needed it most.

---

## 10. Risks and Mitigations

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | Cannot hire 14 engineers on schedule | Medium | High | Bridge contractors budgeted ($740K); remote-first for 6 of 14; Q2 start; Gate 1 tests headcount at 8 | Zhou |
| 2 | Rule extraction incomplete or wrong | Medium | Critical | Okonkwo advisory; two-engineer review of every rule; parallel run surfaces gaps before cutover, not after | Petrosyan |
| 3 | Parallel run reveals persistent discrepancies | Medium | High | 6 months budgeted with 3 months contingency; gate requires 60 clean days; extension funded before cutover permitted | Program Director |
| 4 | Major production incident on legacy engine during program | Medium | High | Legacy team intact + 2 added engineers; observability retrofit in Phase 1; no legacy staff on new build | Petrosyan |
| 5 | Cascade Prairie does not renew | Medium | Critical | Remediation plan delivered June 15; quarterly briefings; named exec sponsor (Achebe); cohort 1 includes 2 Cascade charters as early proof | Achebe / Farouk |
| 6 | Covenant breach | Low | Critical | Tranched draws; lender discussion on add-back in Q2; $3.0M substitutable cash; quarterly covenant reporting to Board | Brantley |
| 7 | Roadmap deferral causes client loss | Medium | Medium | Proactive comms to 23 affected institutions in March; RTP re-committed for Q2 2027 with written dates | Zhou / Achebe |
| 8 | Second site delivery delayed | Low | Medium | Lease signed Phase 1; two candidate sites under evaluation; Council Bluffs remains primary until proven | Petrosyan |
| 9 | Cutover incident affecting client settlement | Low | Critical | Cohort sequencing smallest-first; 90-day shadow post-cutover; per-cohort rollback in one cycle; $290K reserve; CRO pause authority | Farouk |
| 10 | Scope creep repeats 2022 | Medium | High | Written scope freeze; ARC approval required for changes; out-of-scope items enumerated | Program Director |
| 11 | Key new hire attrition mid-program | Medium | Medium | Retention awards at Gates 2 and 3; documentation standards enforced; no single-owner modules | Zhou |
| 12 | Wire screening vendor accelerates sunset | Low | High | Adapter scheduled Phase 2, ahead of Q3 2027 deadline; vendor relationship managed by Petrosyan directly | Petrosyan |

**Residual risk statement (Chief Risk Officer).** Ms. Farouk's assessment: with this program authorized and gated as described, residual risk of a settlement-affecting catastrophic event over 36 months falls from *high* to *moderate*, and the primary residual exposure shifts from technology to execution — which is a form of risk the Board can observe and act on at defined intervals. Without the program, residual risk remains *high* and increases as engineering headcount on the legacy system declines. Ms. Farouk supports the proposal.

---

## 11. Governance and Reporting

- **Monthly:** Program Director written report to the Audit and Risk Committee — schedule, spend against plan, headcount, risk register changes, discrepancy log from Stage A onward.
- **Quarterly:** CEO and CTO present to the full Board — gate status, covenant position, client retention, roadmap impact.
- **At each gate:** formal readiness review with pre-defined criteria; Audit and Risk Committee decision to release next tranche.
- **Independent assurance:** two third-party reviews, at Gate 1 and Gate 2, reporting directly to the Audit and Risk Committee, budgeted at $210,000.
- **Escalation:** any single risk moving to critical, any variance above 10 percent of phase budget, or any contingency draw above $250,000 triggers immediate Audit and Risk Committee notification.

---

## 12. Decision Requested

The Board is asked, on March 4, 2026, to:

**1. Authorize** the Settlement Platform Modernization Program at a total budget of **$19,800,000** over 26 months, with the scope, architecture, and migration approach described in Sections 4 through 7.

**2. Release** **$4,200,000** for Phase 1 (March – September 2026), covering rule extraction, initial hiring, second-site lease and buildout commencement, comparison harness construction, and the Cascade Prairie remediation plan.

**3. Approve** the funding structure of **$12,000,000 from operating cash** and **up to $7,800,000 drawn on the growth facility**, drawn in tranches tied to phase gates, and authorize the CFO to negotiate a covenant accommodation with the lender for defined program costs.

**4. Approve** the addition of **14 permanent engineering positions** and the reallocation of **nine engineers** from product roadmap, with the consequent deferral of RTP send capability to Q2 2027 and digital account opening API v3 to Q3 2027.

**5. Delegate** to the Audit and Risk Committee the authority to release Phase 2, 3, and 4 funding against the gate criteria in Section 7, and to terminate or suspend the program at any gate.

**6. Note** the Chief Risk Officer's residual risk assessment (Section 10) and the reporting cadence in Section 11.

---

We are asking for a large sum against a history that does not recommend us. We think the case is nonetheless clear. The settlement engine is a system we no longer fully understand, operated by four people, three of whom are near the end of their careers, in a building with one power feed. December 27 cost $2.1 million and did not damage a single client relationship beyond repair. The next one might.

We have structured this proposal so the Board never has to trust us for more than seven months at a time. That is the most honest thing we can offer.

Respectfully submitted,

**Rosalind Achebe**, Chief Executive Officer
**Viktor Petrosyan**, Chief Technology Officer

*Endorsed by:* Harold Brantley, CFO — funding structure and covenant analysis (§6) · Meiling Zhou, VP Engineering — staffing and roadmap (§5) · Nadia Farouk, CRO — risk assessment and client exposure (§2.3, §10)
