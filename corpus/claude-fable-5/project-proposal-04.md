# Meridian Ledger, Inc.

## Proposal to the Board of Directors: Settlement Platform Rebuild and Data Center Resilience Program

**To:** The Board of Directors, Meridian Ledger, Inc.
**From:** Rosalind Achebe, Chief Executive Officer; Viktor Petrosyan, Chief Technology Officer
**Date:** February 18, 2026
**For decision at the board meeting of:** March 4, 2026
**Classification:** Board Confidential

---

## 1. Executive Summary

Management requests board authorization of a $19.8 million, 26-month program to rebuild Meridian Ledger's core settlement engine on a supported platform and to move production from a single leased data center in Council Bluffs to an active-active pair of facilities. The program culminates in a six-month parallel run in which the existing engine and the new engine process identical live volume, with cutover permitted only after both engines reconcile to the penny across a full quarter-end cycle.

The reason to act is not that the current system is failing every day. It is that the conditions under which it fails, and the conditions under which we cannot repair it, are now converging. The settlement engine was written in 2009 in COBOL on a stack the vendor stopped supporting in 2021. Four engineers understand it; their average age is 58; one, Dale Kowalcik, retires in April and has declined an extension. On December 27, 2025, a nine-hour outage delayed settlement for 118 of our 340 client institutions and cost $2.1 million in service credits — 4.5 percent of annual recurring revenue erased in one shift. Our most recent SOC 2 Type II report carries two exceptions on change management, both traceable to the fact that changes to the legacy engine cannot be tested in any environment that faithfully replicates production. Cascade Prairie Bancorp, at 11 percent of revenue our largest client, has demanded a written remediation plan as a condition of its October 1 renewal.

The program costs $19.8 million: $11.4 million in engineering, $3.6 million in infrastructure, $2.9 million for the parallel run, and $1.9 million of contingency. CFO Harold Brantley proposes to fund $12.0 million from operating cash over the 26 months and $7.8 million from the existing growth facility. Modeled draw and EBITDA scenarios keep leverage below 2.6x against a covenant cap of 3.0x, with 0.4x of headroom in the worst modeled case.

The board is entitled to skepticism. In 2022 this company cancelled a modernization effort after spending $4.3 million and shipping nothing. This proposal is structured explicitly around the lessons of that failure: fixed-scope replication of existing behavior rather than a redesign, live-volume parallel running as the sole acceptance criterion, quarterly tranche funding that the board releases only against demonstrated milestones, and a governance structure in which the board sees reconciliation data — not status narratives — every quarter.

We considered and rejected two alternatives at length: purchasing a third-party settlement platform, and continuing to patch the current engine. Section 8 sets out that analysis. In brief, the buy option costs less up front but surrenders the product differentiation on which our pricing and our client relationships rest, and the two credible vendors are both owned by competitors of our clients. The patch option is the cheapest for approximately 24 months and then becomes the most expensive option we could choose, because it spends money extending an asset whose maintainability expires with its maintainers.

**The specific decision requested on March 4** is set out in full in Section 10: authorization of the $19.8 million program budget, release of the first tranche of $4.7 million, approval of the $7.8 million facility draw schedule, and establishment of a board Technology Oversight Subcommittee with defined go/no-go authority at three gates.

---

## 2. Why Now: The Risk in the Current Stack

### 2.1 What the settlement engine does and why it cannot be allowed to fail

Meridian Ledger's settlement engine is the system of record through which 340 community banks and credit unions in fourteen states clear and settle payments. When it runs, roughly $1.9 billion in daily volume moves correctly and invisibly. When it stops, our clients cannot tell their depositors whether payrolls posted, whether loan payments cleared, or whether their own positions with correspondent banks are accurate. For a community bank, that is not an inconvenience; it is a regulatory and reputational event. Several of our clients faced examiner inquiries after December 27. Their problem becomes our problem within one renewal cycle.

### 2.2 The December 27 outage, plainly described

At 2:14 a.m. Central on December 27, a batch job in the end-of-day settlement cycle deadlocked against a file maintenance process. The deadlock itself was recoverable. What turned a 40-minute incident into a nine-hour outage was that the recovery procedure — restarting the cycle from the last checkpoint — depends on operator knowledge that exists in the heads of four people. The on-call engineer that night was not one of the four. The engineer who was reached at 4:50 a.m., Dale Kowalcik, diagnosed the checkpoint corruption in under an hour, but the cycle then had to be re-run serially. Settlement completed at 11:12 a.m. for 118 institutions that expected finality by 6:00 a.m.

Direct cost: $2.1 million in contractually mandated service credits. Indirect cost: Cascade Prairie's remediation demand, elevated churn conversations at six other institutions, and a formal question from two clients' examiners about our business continuity posture. The root cause was not exotic. It was a system that requires artisanal recovery, operated by an artisan pool that is shrinking to zero.

### 2.3 Key-person concentration

Four engineers can safely modify or recover the settlement engine. Their average age is 58. Dale Kowalcik retires April 30, 2026, and has declined both a retention bonus and a consulting arrangement beyond limited advisory hours. Of the remaining three, one has disclosed an intention to retire "within two to three years." We have tried for four years to cross-train younger engineers into the codebase; the constraint is not willingness but the absence of any non-production environment in which a trainee can safely make mistakes, which brings us to the audit findings.

### 2.4 The SOC 2 exceptions

Our SOC 2 Type II report for the period ended September 30, 2025 contains two exceptions, both in change management:

- **Exception 1:** Changes to the settlement engine were promoted to production without evidence of testing in a representative pre-production environment. The finding is accurate: no representative pre-production environment exists. The legacy stack cannot be virtualized, and a second physical instance was priced in 2023 at $1.4 million on hardware the manufacturer no longer warranties.
- **Exception 2:** Segregation of duties between change development and change deployment was not maintained for settlement engine changes. Also accurate: with four qualified engineers covering 24/7 operations, the same individual frequently writes and deploys a change.

These exceptions are not paperwork problems. Our contracts with 61 institutions, including Cascade Prairie, require a clean SOC 2 or a remediation plan with dates. Neither exception can be remediated within the current architecture at acceptable cost. The rebuild remediates both structurally: the new platform includes full pre-production environments and pipeline-enforced segregation of duties from day one.

### 2.5 Single-site exposure

All production runs from one leased facility in Council Bluffs. Our disaster recovery arrangement is a cold-restore contract with a 48-to-72-hour recovery time objective. For a settlement system, 48 hours of downtime is not recovery; it is the event our clients' regulators plan against. The facility itself sits in the Missouri River flood plain; the 2019 and 2024 flood events did not reach it, but our insurer repriced the exposure in the 2025 renewal. Two-site active-active operation is table stakes for the business we are actually in, and it cannot be retrofitted onto the legacy engine, whose licensing and hardware dependencies do not permit a second live instance.

### 2.6 Cascade Prairie Bancorp

Cascade Prairie represents 11 percent of revenue, approximately $5.2 million annually. Their renewal date is October 1, 2026. Following December 27, their COO informed Chief Risk Officer Nadia Farouk in writing that renewal is conditioned on "a board-approved remediation plan addressing platform obsolescence, single-site concentration, and the audit exceptions, with funded milestones." They have asked to see evidence of board action by mid-April. A board-authorized program on March 4, with the first tranche released, satisfies that condition. A deferral does not, and we should assume Cascade Prairie's advisors will read a deferral accurately.

### 2.7 The shape of the risk

None of these threads — outage, audit, retirements, single site, client demand — is individually fatal. Together they describe a business whose core asset is depreciating faster than its revenue, and whose window for an orderly transition is bounded by the working lives of four people. The question before the board is not whether to replace the settlement engine. It is whether to replace it now, deliberately, with the people who understand it still on payroll to validate the replacement — or later, under duress, without them.

---

## 3. What Is Proposed: Target Architecture and Migration Approach

### 3.1 Design principle: replicate, then improve

The 2022 effort failed in part because it attempted to redesign settlement behavior while replacing the platform. This program does the opposite. **Phase one scope is a behavioral clone**: the new engine must produce, for identical inputs, outputs identical to the legacy engine — same settlement results, same file formats, same cutoff behavior, same edge-case handling, including edge cases we may consider inelegant. Improvements to settlement logic are explicitly out of scope until after cutover. This discipline is what makes a six-month parallel run a meaningful acceptance test: any discrepancy between the engines is by definition a defect, with no ambiguity about which behavior is "intended."

### 3.2 Target platform

- **Application tier:** The settlement engine is rewritten in Java on a supported runtime, structured as a modular monolith — deliberately not a fine-grained microservices architecture, which would add operational complexity we do not need and did contribute to the 2022 effort's collapse under its own design ambition. Modules mirror the legacy engine's functional decomposition (intake, validation, netting, settlement, distribution, reconciliation) to make behavioral comparison tractable.
- **Data tier:** PostgreSQL with synchronous replication between sites for the system of record; the legacy VSAM file structures are mapped to relational schemas with automated bidirectional conversion tooling so that during the parallel run either engine's output can be compared field-by-field.
- **Infrastructure:** Two leased data centers — the existing Council Bluffs facility (re-racked with new hardware) and a second facility in the Des Moines metro, approximately 130 miles away, outside the flood plain and on a separate power grid. Active-active for intake and inquiry; active-passive with automated failover for the settlement cycle itself, with a recovery time objective of 15 minutes and recovery point objective of zero (no acknowledged transaction lost). We evaluated public cloud and concluded that our clients' examiners, our data residency commitments in three state contracts, and our latency profile favor dedicated facilities at our scale; the architecture does not preclude a later cloud migration.
- **Controls:** Deployment exclusively through a CI/CD pipeline with enforced peer review, automated regression suites replaying sanitized production transaction histories, and pipeline-level segregation of duties. Both SOC 2 exceptions are structurally closed by this design, and our auditors have reviewed the control design in draft.

### 3.3 Migration approach: the parallel run

Months 21 through 26 are the heart of the program. Both engines receive identical live transaction streams. The legacy engine remains the engine of record — its outputs are what clients receive — while the new engine runs in full shadow. Every night, an automated reconciliation compares outputs at the field level and publishes a discrepancy count.

Cutover criteria, which we propose the board fix now and reserve to itself to waive:

1. **Zero unexplained discrepancies** across 60 consecutive processing days, including one month-end and one quarter-end;
2. **Successful live failover test** between sites under load, meeting the 15-minute RTO;
3. **Clean control testing** of the change management pipeline by our SOC 2 auditors;
4. **Sign-off** by the CTO, CRO, and the head of the legacy engineering team (a deliberate requirement: the people who know the old engine best must attest the new one matches it).

If criteria are not met by month 26, the parallel run extends — the legacy engine keeps running, clients see nothing, and the contingency budget covers extension at approximately $480,000 per month. The program cannot strand clients on an unproven platform, because the unproven platform never becomes the engine of record until it has proven itself against live volume.

### 3.4 What happens to the legacy engine

After cutover, the legacy engine runs in reverse shadow for 90 days as a fallback, then is decommissioned. Legacy hardware maintenance contracts (approximately $610,000 annually) and the associated licensing terminate, contributing to the run-rate savings in Section 6.

---

## 4. How It Would Be Run and Staffed

### 4.1 Program leadership and governance

- **Executive sponsor:** Viktor Petrosyan, CTO, accountable to the CEO and board for delivery.
- **Program director:** We will hire a dedicated program director with prior experience delivering a core-system replacement at a financial technology or core-processing firm. This role did not exist in 2022; the effort was run as a side responsibility of a VP who also carried the roadmap. The search is underway; two finalists have been interviewed.
- **Board Technology Oversight Subcommittee:** We ask the board to constitute a subcommittee of two to three directors to meet monthly with the program director and quarterly with the full delivery leadership. The subcommittee receives the reconciliation dashboards, milestone evidence, and spend-versus-tranche reporting directly, not filtered through management summary. It recommends tranche releases to the full board.
- **Independent verification:** A third-party firm (budgeted within engineering at $420,000) audits milestone completion each quarter against pre-defined, objective evidence — code coverage, replay-test pass rates, reconciliation results — and reports to the subcommittee.

### 4.2 The team

Engineering VP Meiling Zhou's plan requires **14 new hires** and **nine internal transfers** from the product roadmap teams, organized as follows:

| Function | New hires | Internal transfers | Notes |
|---|---|---|---|
| Settlement engine rewrite | 6 | 4 | Core Java engineers; transfers bring domain knowledge |
| Legacy analysis & behavioral specification | 0 | 3 | Includes 2 of the 4 COBOL engineers, backfilled on ops by contractor support |
| Data migration & reconciliation tooling | 3 | 1 | |
| Infrastructure & site build-out | 2 | 1 | Plus data center vendor professional services |
| QA / replay testing | 2 | 0 | |
| Program office | 1 | 0 | Program director |
| **Total** | **14** | **9** | |

Hiring plan: seven offers in the first 90 days post-authorization, the remainder by month 8. Omaha's engineering labor market supports this at budgeted compensation; we have validated with two recruiting firms and hold a warm pipeline from the December-January passive search.

### 4.3 Retaining and using the legacy team

The four COBOL engineers are the program's most important asset. Their role is not to write the new engine but to **specify the old one's behavior and adjudicate discrepancies** during the parallel run. Retention packages (included in the engineering budget at $780,000 total) are structured with cliffs at cutover, not at calendar dates, so the incentive is aligned with completion. Dale Kowalcik has agreed to a limited advisory contract post-retirement covering documented knowledge transfer through month 12. This is precisely the window that closes if we defer: every year of delay removes irreplaceable validation capacity from the parallel run.

### 4.4 What the roadmap gives up

Pulling nine engineers from product teams defers two committed features:

1. **Real-time payment rail integration (FedNow expansion)** — committed to 22 institutions for Q4 2026, deferred to Q3 2027. Six of the 22 have contractual language; Nadia Farouk has reviewed it, and remediation is a fee credit capped at $18,000 aggregate. Client communications are drafted for delivery within two weeks of board approval, framed honestly: we are deferring a growth feature to secure the core.
2. **Analytics dashboard suite** — a competitive-parity feature with no contractual commitments, deferred to 2028.

We considered protecting the roadmap by hiring more externally instead of transferring. Zhou's judgment, which we endorse, is that a rewrite staffed entirely by people who have never operated our settlement flows is how 2022 happened. The transfers are the point, not a cost-saving compromise.

---

## 5. Phased Schedule

The program runs 26 months from authorization, April 2026 through May 2028, in four phases separated by three board-level gates.

**Phase 1 — Foundation (Months 1–6, Apr–Sep 2026).** Hire the first wave; stand up the second data center shell and network; build the behavioral specification of the legacy engine, including a replay harness that can feed historical production days through both engines; deliver the intake and validation modules. **Gate 1 (Month 6):** replay harness demonstrably reproducing 30 days of historical production through the legacy engine with zero variance; second site network-live; hiring ≥ 80 percent of plan. Board subcommittee reviews evidence; full board releases Tranche 2. *This gate also lands before Cascade Prairie's October 1 renewal, giving them a funded plan and a passed first milestone.*

**Phase 2 — Core Build (Months 7–14, Oct 2026–May 2027).** Netting and settlement modules built and validated against replayed history; data migration tooling complete; second site hardware installed and burned in. **Gate 2 (Month 14):** new engine reproduces 90 days of replayed historical production with zero unexplained variance; failover infrastructure tested with synthetic load. Tranche 3 release.

**Phase 3 — Integration and Hardening (Months 15–20, Jun–Nov 2027).** Distribution and reconciliation modules; client file-format certification (formats are unchanged by design, so this is verification, not client work); SOC 2 auditors test the new change-management controls; operational runbooks and failover drills. **Gate 3 (Month 20):** authorization to begin the live parallel run. This is the highest-consequence gate and requires full board approval, not subcommittee.

**Phase 4 — Parallel Run and Cutover (Months 21–26, Dec 2027–May 2028).** Both engines on live volume as described in Section 3.3. Cutover on satisfaction of the four criteria; 90-day reverse shadow; decommissioning. If criteria are unmet, extension funded from contingency at ~$480,000/month, with monthly board review.

At every gate, the board's realistic options are preserved: because the legacy engine remains the engine of record until the final criteria are met, a decision to pause or stop at any gate leaves clients unaffected. The program is structured so that the board never faces a "too far in to stop" argument — the argument that trapped the 2022 effort into two extra quarters of spend.

---

## 6. Cost and Funding

### 6.1 Program budget

| Category | Amount ($M) | Contents |
|---|---|---|
| Engineering | 11.4 | 14 hires (26-month loaded cost, $6.1M); 9 transfer backfill and contractor coverage ($1.8M); legacy team retention ($0.78M); program director and program office ($0.9M); independent verification ($0.42M); tooling, licenses, replay infrastructure ($1.4M) |
| Infrastructure | 3.6 | Second site build-out and 26 months' lease ($1.7M); hardware both sites ($1.5M); network, security appliances ($0.4M) |
| Parallel run | 2.9 | Six months' dual operation: duplicate processing capacity, reconciliation operations staffing, extended legacy support contracts ($2.9M) |
| Contingency | 1.9 | 10.6% of base cost; sized to cover a 4-month parallel-run extension ($1.9M) or equivalent schedule slip; released only by the board subcommittee |
| **Total** | **19.8** | |

### 6.2 Tranche schedule

| Tranche | Released at | Amount ($M) | Covers |
|---|---|---|---|
| 1 | March 4 authorization | 4.7 | Phase 1 |
| 2 | Gate 1 (Month 6) | 5.4 | Phase 2 |
| 3 | Gate 2 (Month 14) | 4.6 | Phase 3 |
| 4 | Gate 3 (Month 20) | 3.2 | Phase 4 |
| Contingency | Subcommittee approval as needed | 1.9 | |
| **Total** | | **19.8** | |

### 6.3 Funding and covenant analysis

Harold Brantley's funding plan draws **$12.0 million from operating cash** spread across the 26 months — averaging $460,000 per month against current free cash flow of approximately $650,000 per month — and **$7.8 million from the growth facility** in three draws timed to Tranches 2 through 4.

The facility covenant caps net leverage at 3.0x trailing EBITDA. Current leverage is 1.4x. Modeled at full draw:

| Scenario | Trailing EBITDA ($M) | Peak leverage | Headroom |
|---|---|---|---|
| Base case (revenue flat, credits normalize) | 9.7 | 2.2x | 0.8x |
| Stress: Cascade Prairie lost + one more $2M credit event | 7.9 | 2.6x | 0.4x |
| Severe: above plus 5% additional churn | 7.2 | 2.9x | 0.1x |

The severe case is tight but does not breach, and it describes a world in which we lost Cascade Prairie — an outcome this program exists to prevent and which deferral makes more likely, not less. Brantley has briefed the facility agent informally; the agent views the program as credit-positive and has indicated openness to a covenant amendment if the severe case materialized, though the plan does not rely on that.

### 6.4 Run-rate economics after completion

Post-cutover, annual run-rate changes: legacy hardware maintenance and licensing eliminated (−$0.61M); second site lease and operations added (+$0.9M); avoided key-person premium contracting we would otherwise need from 2027 (−$0.5M estimated); and, critically, a credible expectation of avoiding outage credits at the December 27 scale. One avoided December 27 per two years is worth $1.05M annually. The program does not pay for itself through cost savings alone and we will not pretend it does; it pays for itself by preserving $47 million of recurring revenue whose renewal now depends on it.

---

## 7. Alternatives Weighed

### 7.1 Alternative A: Buy a third-party settlement platform

Two credible platforms exist that could, with configuration, process our clients' settlement volumes. Estimated cost: $8–11 million over three years in license, integration, and migration — cheaper than the rebuild.

We recommend against it for three reasons:

1. **Ownership conflicts.** Both vendors are subsidiaries of large core-processing companies that compete directly with our community bank clients' independence positioning and, in one case, with us. Nadia Farouk's diligence found that 40+ of our clients have contract language or board policies restricting data flows to those parent companies. We would begin the migration by triggering our clients' vendor-risk objections.
2. **Loss of differentiation.** Our settlement behavior — cutoff flexibility, correspondent handling, exception workflows tuned over 17 years to community-institution needs — is why 340 institutions pay us rather than a national processor. On a licensed platform we become a reseller of someone else's engine, with our pricing power repriced accordingly. The strategic cost dwarfs the $9–12 million of nominal savings.
3. **Migration risk is not lower.** A third-party platform still requires full data migration, behavioral mapping, and client conversion — the risky parts of our plan — while removing our ability to make the new system behave identically to the old. Every behavioral difference becomes a client conversion issue instead of an internal defect.

We do, however, incorporate one lesson from this analysis: our target architecture keeps client-facing file formats unchanged, precisely because client-side conversion is where third-party migrations bleed.

### 7.2 Alternative B: Continue to patch

Estimated cost: $1.5–2.5 million annually — emergency hardware sourcing on the secondary market, contractor COBOL support (a shrinking and increasingly expensive pool), incremental monitoring, and retention payments. It is the cheapest path for roughly the next 24 months.

It fails on four counts. It does not remediate the SOC 2 exceptions, because the environment and segregation problems are architectural. It does not satisfy Cascade Prairie, whose demand is explicitly for a plan addressing obsolescence, not maintenance. It does not address single-site exposure, since the legacy stack cannot run active-active. And it spends money to extend a system whose maintainer pool goes from four to three in April and plausibly to two by 2028 — after which every option we have gets worse and more expensive, because the parallel-run validation strategy that de-risks this program requires the legacy experts to be here. Patching is not a lower-risk alternative; it is a decision to run the same migration later with fewer of the people who make it safe.

### 7.3 Alternative C: Incremental strangler-pattern migration

For completeness: rebuilding the engine module-by-module in place, routing slices of live traffic to new components progressively. This is often the right pattern, and we examined it seriously. It fails here because settlement is transactionally atomic — netting cannot be split across two engines mid-cycle without creating exactly the reconciliation ambiguity that destroys client trust — and because the legacy stack has no integration surface that would allow partial routing without invasive changes to the very code we can barely modify safely. The parallel-run approach captures the strangler pattern's core virtue (the old system keeps running until the new one is proven) without requiring the two engines to interoperate mid-cycle.

### 7.4 Alternative D: Sell the company or the client book

Raised by a director informally in January; addressed here for transparency. The board may of course consider strategic alternatives at any time, but the platform condition depresses valuation now — any acquirer's diligence will find December 27, the SOC 2 exceptions, and the key-person exposure, and will price the rebuild into their bid at their assumed cost, not ours. Completing this program is value-accretive under every ownership scenario, including a sale.

---

## 8. What Could Go Wrong: Risks and Mitigations

We present these in the order of our concern, not convenience.

**Risk 1: This becomes 2022 again — spend without shipping.**
The 2022 effort failed for identifiable reasons: scope that grew from replacement into redesign; no dedicated program leadership; no objective acceptance criterion, so "done" was perpetually negotiable; and funding released as a lump sum, so there was no natural checkpoint at which the board could act on early warning signs. Every element of this proposal is a direct response: frozen behavioral-clone scope with post-cutover improvements explicitly out of bounds; a dedicated, experienced program director; live-volume reconciliation as a binary acceptance test that cannot be argued with; quarterly tranche funding against evidence verified by an independent third party; and a board subcommittee with direct access to that evidence. The honest residual risk is execution quality, which is why the gates are designed so that stopping at any of them costs only the tranches spent, never client service.

**Risk 2: The parallel run surfaces persistent discrepancies and the schedule slips.**
Likelihood: moderate — some discrepancy volume in the first weeks of parallel running is expected and healthy. Mitigation: the replay harness in Phases 1–2 is designed to burn down behavioral discrepancies against historical data before live parallel running begins, so Phase 4 should confirm rather than discover. Contingency is sized for a four-month extension; each extension month costs ~$480,000 and the legacy engine remains the engine of record throughout, so slippage costs money, not client trust. Beyond four months, the board decides with full information.

**Risk 3: We cannot hire 14 qualified engineers on schedule.**
Likelihood: low-to-moderate. Mitigation: hiring front-loaded with Gate 1 measuring it at 80 percent; two contracted staffing firms as overflow; compensation benchmarked in December 2025; and the internal transfers mean the program's domain knowledge does not depend on external hiring succeeding perfectly. If hiring runs materially behind at Gate 1, the board sees it before releasing Tranche 2.

**Risk 4: Legacy engineer availability collapses — retirement, illness, departure.**
This is the risk we cannot fully mitigate and the strongest argument for the timeline. Mitigations: retention packages cliffed at cutover; Kowalcik's advisory contract through month 12; the behavioral specification and replay harness in Phase 1 are explicitly designed to convert head-knowledge into executable artifacts as early as possible, so that dependence on the individuals declines each quarter. The program is, among other things, a 26-month controlled extraction of knowledge that currently exists in four heads.

**Risk 5: A major legacy outage during the program.**
The legacy engine keeps running for at least 21 more months regardless of what the board decides; this risk exists under every alternative. Within the program, Phase 1 includes $300,000 (inside the infrastructure line) of targeted legacy stabilization: automated checkpoint validation and a documented, drilled recovery runbook addressing the specific failure mode of December 27. This is patching, but patching with an end date.

**Risk 6: Financial stress compresses covenant headroom.**
Addressed in Section 6.3. The severe scenario leaves 0.1x headroom; the escalation path is a covenant amendment conversation the agent has signaled openness to, and the board subcommittee will see leverage projections at every tranche release, with authority to slow the draw schedule.

**Risk 7: Cascade Prairie declines to renew despite the program.**
Possible; their demand is a necessary condition, not a promise. Mitigation: Farouk and Achebe present the board-approved plan to Cascade Prairie's executive team in April, with Gate 1 evidence delivered in September ahead of the October 1 renewal, and a proposed renewal structure that ties a portion of their fees to program milestones — converting them from a skeptical customer into a monitored beneficiary. If they nonetheless depart, the stress scenario in Section 6.3 shows the program remains fundable, and their departure would make the program more necessary for the remaining 89 percent of revenue, not less.

**Risk 8: Cutover itself fails.**
The lowest-probability, highest-visibility risk. Mitigation: cutover occurs only after 60 clean days including a quarter-end; the 90-day reverse shadow keeps the legacy engine warm as a fallback; and the cutover runbook includes a tested reversion procedure. No client is moved to an engine that has not already processed their live volume correctly for two months.

---

## 9. Why This Program and Not a Smaller One

Directors may reasonably ask whether a $10–12 million version exists. It does, and we costed it: rebuild the engine but stay single-site ($16.2M), or rebuild with a three-month parallel run ($17.9M), or defer the second site to a later program ($16.2M plus an estimated $5.5M standalone site program later, at higher total cost and with the single-site risk retained through 2029). Each smaller version removes the element that answers one of the specific findings against us — the site concentration our insurer and Cascade Prairie have both flagged, or the parallel-run duration that makes cutover defensible to our clients' examiners. The $19.8 million figure is not the ambitious version of this program. It is the complete version of the minimum program, and we would rather ask the board once for the real number than return in 2027 for the difference. That, too, is a lesson of 2022.

---

## 10. The Decision Requested on March 4

Management requests that the board resolve as follows:

1. **Approve** the Settlement Platform Rebuild and Data Center Resilience Program with a total authorized budget of **$19.8 million** over 26 months, comprising $11.4 million engineering, $3.6 million infrastructure, $2.9 million parallel-run operations, and $1.9 million contingency, on the phased plan described in Section 5.

2. **Release Tranche 1 of $4.7 million** immediately upon approval, funding Phase 1 through Gate 1, with Tranches 2–4 released by full board vote upon subcommittee-verified satisfaction of Gates 1–3 respectively, and contingency released only by the Technology Oversight Subcommittee against documented need.

3. **Approve the funding plan**: up to $12.0 million from operating cash over the program term and up to $7.8 million drawn on the growth facility in three draws timed to Tranches 2–4, with the CFO directed to report covenant headroom at each tranche release and authorized to open covenant-amendment discussions with the facility agent if projected headroom falls below 0.3x.

4. **Constitute a Technology Oversight Subcommittee** of the board, of two to three directors, meeting monthly with the program director, receiving milestone evidence and independent verification reports directly, and recommending tranche releases to the full board; and **reserve to the full board** the Gate 3 decision to commence the live parallel run and any waiver of the four cutover criteria set out in Section 3.3.

5. **Authorize management** to (a) proceed with the 14 program hires and nine internal transfers, including the associated retention arrangements for the legacy engineering team; (b) execute the second data center lease and hardware procurement within the infrastructure budget; (c) communicate the deferral of the two committed roadmap features to affected clients per the plan reviewed by the Chief Risk Officer; and (d) present the approved program to Cascade Prairie Bancorp in support of the October 1 renewal.

6. **Direct management** to report to the full board quarterly on program status, including reconciliation and milestone data in the form provided to the subcommittee, and to return to the board immediately upon any projected breach of a gate criterion, the contingency budget, or covenant headroom.

We are asking the board to fund the replacement of the asset this company is built on, while the people who understand that asset are still here to guarantee the replacement is faithful. Every year of delay raises the cost, shrinks the validation capacity, and shifts more of the decision from us to events. We ask for authorization on March 4.

Respectfully submitted,

**Rosalind Achebe**, Chief Executive Officer
**Viktor Petrosyan**, Chief Technology Officer

*Concurring: Harold Brantley, Chief Financial Officer; Meiling Zhou, Vice President of Engineering; Nadia Farouk, Chief Risk Officer*

---

*Appendices available to directors on request: A — December 27 incident post-mortem (full); B — SOC 2 Type II report and auditor correspondence; C — Third-party platform diligence summaries; D — Detailed staffing and compensation model; E — Covenant model workbook; F — 2022 program post-mortem; G — Cascade Prairie correspondence.*
