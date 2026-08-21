# MEMORANDUM

**To:** The Board of Directors, Meridian Ledger, Inc.
**From:** Rosalind Achebe, Chief Executive Officer; Viktor Petrosyan, Chief Technology Officer
**Date:** February 27, 2026
**Re:** Proposal to Rebuild the Core Settlement Platform — Decision Requested at the March 4, 2026 Board Meeting

---

## Executive Summary

We are asking the Board to authorize a $19.8 million, 26-month program to rebuild Meridian Ledger's core settlement engine, retire the 2009 COBOL system that underlies it, and move settlement processing from a single leased data center in Council Bluffs to two. The program would be funded with $12.0 million of operating cash and a $7.8 million draw on the growth facility, staged in gates tied to independent verification of milestones rather than released as a lump sum.

We bring this forward now because the risk in the current stack has moved from theoretical to realized. The December 27 outage delayed settlement for 118 of our 340 institution customers for nine hours and cost $2.1 million in credits. Our most recent SOC 2 Type II report carries two exceptions on change management — the control area most directly implicated in the outage. Four engineers understand the COBOL settlement engine well enough to safely change it; their average age is 58, and one retires in April. Our largest relationship subject to renewal risk this year, Cascade Prairie Bancorp at 11% of revenue, has formally demanded a remediation plan ahead of its October 1 renewal. Each of these facts independently argues for action. Together they describe a system we can no longer safely defer replacing, supported by a workforce we can no longer safely rely on.

We recognize the Board's wariness. The 2022 modernization effort consumed $4.3 million and shipped nothing, and this proposal will be measured against that failure. We have built this plan differently in three respects: the architecture and migration approach have been scoped and estimated by Engineering leadership with named deliverables at each phase gate; funding is staged and contingent on an independent technical review clearing each gate, not disbursed in full at signing; and the highest-risk part of the cutover — the point at which the new engine takes live settlement volume — is bounded by a six-month period in which both engines run in parallel, so that failure is recoverable rather than catastrophic.

This memorandum sets out the risk in the current stack, the target architecture and migration approach, the staffing plan, the phased schedule and what it displaces on the product roadmap, the cost and funding structure, the alternatives we weighed and rejected, the risks we see and how we propose to mitigate them, and the specific authorization we are asking the Board to grant on March 4.

---

## 1. Risk in the Current Stack

Meridian Ledger's settlement engine was built in 2009 in COBOL and has been extended, not re-architected, for seventeen years. It is the system of record for settlement across all 340 of our community bank and credit union customers in fourteen states, representing $47 million in recurring revenue. Three risks compound each other today.

**Operational risk is now realized, not theoretical.** On December 27, a defect introduced during a routine change caused a nine-hour settlement delay affecting 118 institutions — more than a third of our customer base — and cost $2.1 million in service credits under our SLAs. This was not an infrastructure failure; it was a change-management failure in a system whose complexity now exceeds the ability of our processes to safely control. It is also not an isolated event. It is the most severe in a pattern of change-related incidents over the past eighteen months, and it is the first to be visible to customers at this scale.

**Our compliance posture reflects the same weakness the outage exposed.** Our most recent SOC 2 Type II examination came back with two exceptions, both in change management — the exact control domain implicated in the December incident. Community bank and credit union customers rely on our SOC 2 report in their own vendor risk programs. A second consecutive qualified report, or an incident report referencing the same control weakness the auditors already flagged, materially raises the likelihood that customers treat this as a pattern rather than an event.

**Institutional knowledge of the settlement engine is retiring faster than we can replace it.** Four engineers currently possess working knowledge of the COBOL settlement engine sufficient to make changes to it safely. Their average age is 58. One of the four retires in April. We have not been able to hire into this skill set — the COBOL and settlement-domain combination is not one the market supplies — and our internal succession plan for the past three years has been to hope the incumbents stay. That plan has now failed once, with the December outage, and it does not survive a second departure. At three remaining engineers, any unplanned absence — illness, departure, family emergency — leaves us without the capacity to safely change the system that settles $47 million in annual recurring revenue and, more consequentially, moves money for 340 depository institutions.

**A named customer relationship is now conditioned on our answer.** Cascade Prairie Bancorp, 11% of our revenue, renews October 1 and has formally requested a remediation plan following the December incident and the SOC 2 exceptions. Cascade Prairie is not alone in its exposure — the December outage affected 118 institutions — but it is the first to convert that exposure into a contractual demand ahead of a renewal date, and its size means its non-renewal would be a disclosable event. We address the interim response to Cascade Prairie in Section 7; it is important to note here that the remediation plan Cascade Prairie needs by October 1 cannot wait for the 26-month rebuild to complete. We are running a parallel, near-term change-management hardening effort, described below, specifically to answer that demand on its own timeline.

Taken together, these are not independent risks that can be prioritized against each other. They describe a single underlying condition: a settlement system whose complexity has outrun the organization's capacity to operate it safely, on a timeline set by the retirement of the people who currently compensate for that gap.

---

## 2. Target Architecture and Migration Approach

**Target state.** We propose to replace the COBOL settlement engine with a service-oriented settlement platform built on a modern, supported runtime (JVM-based microservices, event-sourced ledger, containerized deployment), maintaining functional parity with current settlement rules, batching windows, and reconciliation outputs, while adding the observability, automated testing, and change-management tooling that the current system lacks by design. Infrastructure moves from a single leased data center in Council Bluffs to two, in an active-active configuration, eliminating the single-site failure mode that made the December outage a full-scale event rather than a contained one.

**Migration approach.** We are not proposing a big-bang cutover. The core of the plan is a strangler-fig migration: the new settlement engine is built and tested against production-shadow traffic before it ever touches live settlement, institution cohorts are migrated in waves rather than all at once, and — critically — the new and legacy engines run in parallel, both processing live volume, for a full six months before the legacy engine is retired. During the parallel run, the legacy COBOL engine remains the authoritative system of record; the new engine's output is continuously reconciled against it institution-by-institution. Authority transfers to the new engine only after a wave has run clean through at least one full monthly settlement cycle with zero unreconciled variances, and only with sign-off from Engineering, Risk, and an external verification party (see Section 7).

This approach costs more and takes longer than a direct cutover. We consider that a feature, not a defect, given the 2022 outcome. It means no institution's settlement is ever dependent on a system that has not already proven itself against live volume before taking authority over that institution's money.

**Why not simply re-platform in place.** We evaluated keeping the COBOL engine and modernizing around it — new interfaces, better monitoring, automated testing harnesses over the existing logic. Engineering's assessment, which we accept, is that this reduces near-term risk marginally but does not resolve the two risks that matter most: the shrinking pool of people who can safely change the core logic, and the single-data-center exposure. It would also cost real money — Engineering estimates $6–8 million over three years in tooling and harness work — without ever reducing our dependence on a workforce that is retiring. We concluded that money spent modernizing around a system we ultimately still cannot safely maintain is money that does not remove the risk that matters.

---

## 3. Staffing Plan

Engineering VP Meiling Zhou has scoped the staffing plan required to execute this program without stopping the business. It has three components.

**New hires — 14 positions.** These are backend engineers with distributed-systems and event-sourcing experience, a data migration lead, two QA/test-automation engineers focused specifically on parallel-run reconciliation tooling, and a site-reliability engineer for the second data center. We plan to open these roles in the first 60 days after authorization; Ms. Zhou's assessment, informed by recent comparable hiring, is that 10–12 of the 14 can be filled within four months and the remainder by month six. This is the single largest execution risk in the staffing plan and is addressed in Section 7.

**Internal reassignment — nine engineers pulled from the product roadmap.** Rather than compete for all 14 hires before starting substantive work, we will move nine engineers from current roadmap teams onto the rebuild for its duration, backfilling roadmap capacity with new hires as they onboard. This lets architecture and core-service work begin in month one rather than waiting for a hiring cycle to complete. The roadmap consequence of this reassignment is addressed in Section 4.

**Legacy-system coverage.** The four engineers who understand the COBOL engine remain on legacy support throughout the migration, are explicitly excluded from rebuild-team workload, and are the subject of a retention plan (spot bonus, defined end date tied to legacy decommission, and reduced on-call burden) intended to keep at least three of the four through the end of the parallel run. We are also engaging a specialist COBOL-support firm on a standby contract as insurance against further attrition; this is a modest incremental cost captured in contingency and is not reflected as a separate line in Section 5 because it is contingent rather than committed spend.

**Program governance.** A steering committee — CTO, VP Engineering, CRO, and a Board-designated observer — meets monthly for the duration of the program. An independent technical advisory firm, engaged separately from Meridian's own team, reviews progress against each phase gate described in Section 4 and reports its findings directly to the Board audit or risk committee, not solely to management. This structure is a direct response to the 2022 experience, where the Board's principal visibility into progress was management's own reporting.

---

## 4. Phased Schedule and What Gets Deferred

The program runs 26 months from authorization, organized into four phases, each with a defined exit gate. Funding for each subsequent phase is contingent on the independent technical advisory firm confirming the prior phase's gate criteria have been met — the Board is not asked to release the full $19.8 million against a single go-forward decision.

| Phase | Duration | Core work | Exit gate |
|---|---|---|---|
| 0 — Mobilization | Months 1–4 | Hiring, second data-center lease and buildout begins, architecture finalized, legacy retention plan executed | Architecture signed off; ≥10 of 14 hires made; data-center lease executed |
| 1 — Build | Months 5–14 | Core settlement services built and tested against shadow production traffic; reconciliation tooling built; first institution cohort selected | Shadow-traffic reconciliation clean for 60 consecutive days on cohort 1 |
| 2 — Parallel Run | Months 15–20 | Both engines process live volume for all migrated cohorts; legacy engine remains authoritative; wave-by-wave institution migration continues | Six consecutive months, zero unreconciled variances across all migrated institutions |
| 3 — Cutover & Decommission | Months 21–26 | Authority transfers to new engine institution by institution; legacy engine and single data center retired; post-migration stabilization | All 340 institutions on new engine; legacy COBOL environment decommissioned |

**What this displaces.** Pulling nine engineers from the roadmap for the duration of the program requires deferring two committed features: the instant-payments rail connector and the multi-entity treasury dashboard, both previously committed for release in the current fiscal year. We are not proposing to cancel either. Both are re-sequenced to begin after the nine reassigned engineers return to roadmap work, which is expected in month 21 as cutover work reduces build-phase headcount needs. We will communicate the revised timeline to the customers who were promised these features directly, ahead of any public roadmap communication, and Ms. Zhou will bring a specific customer-by-customer communication plan to the April board meeting.

**Interim remediation, run separately from this schedule.** Because Cascade Prairie Bancorp's October 1 renewal cannot wait on a 26-month program, we are running a separate, near-term change-management remediation effort — a 90-day plan to close the two SOC 2 exceptions through hardened deployment approval gates, mandatory peer review on all settlement-affecting changes, and expanded automated regression testing on the legacy engine. This is existing-budget work, already underway, and is not part of the $19.8 million request. We expect to have documented remediation evidence to share with Cascade Prairie, and with our SOC 2 auditors ahead of our next examination, by early September.

---

## 5. Cost and Funding

The program totals $19.8 million over 26 months, funded with $12.0 million from operating cash and a $7.8 million draw on the growth facility.

| Category | Amount ($M) | Notes |
|---|---|---|
| Engineering | 11.4 | 14 new hires, contractor/specialist support, tooling |
| Infrastructure | 3.6 | Second Council Bluffs data center, network, active-active buildout |
| Parallel run | 2.9 | Duplicate processing costs, reconciliation tooling, incremental staff during six-month overlap |
| Contingency | 1.9 | COBOL specialist standby contract, schedule slippage, migration surprises |
| **Total** | **19.8** | |

| Funding source | Amount ($M) | Notes |
|---|---|---|
| Operating cash | 12.0 | Drawn over program life, not upfront |
| Growth facility draw | 7.8 | Subject to leverage covenant, see below |
| **Total** | **19.8** | |

**Covenant headroom.** CFO Harold Brantley has modeled the $7.8 million draw against the growth facility's covenant, which caps leverage at three times EBITDA. Based on trailing-twelve-month EBITDA and current outstanding debt, the draw leaves headroom under the covenant at each of the next four quarterly test dates under our base-case forecast. That headroom compresses if the $2.1 million outage-credit cost recurs or if revenue growth slows below plan — most materially, if Cascade Prairie does not renew. Mr. Brantley's sensitivity analysis, included as a separate appendix to this memorandum, shows the covenant remains satisfied even in a scenario combining Cascade Prairie's non-renewal with a second, smaller outage-credit event, but with materially reduced headroom. We flag this not to suggest the funding is unsound, but because it is the clearest financial argument for why the interim remediation work in Section 4 — aimed squarely at retaining Cascade Prairie — matters independently of the rebuild's technical merits.

**Staged release.** Consistent with the governance approach in Section 3, we propose that the Board authorize the full $19.8 million program but that actual disbursement past Phase 0 be conditioned on the independent technical advisory firm's confirmation that the prior phase's exit gate has been met. This gives the Board a checkpoint at each of the three subsequent phase boundaries without requiring a new authorization vote at each one, unless a gate is missed.

---

## 6. Alternatives Considered

We evaluated three alternatives to the proposed rebuild before bringing this recommendation forward.

**Continue to patch the current system.** This is the status quo and the cheapest option in the near term — Engineering estimates ongoing maintenance and incremental hardening at $1.5–2 million per year against the current architecture. We rejected this as the path forward for the reasons in Section 1: it does not address the retiring workforce, it does not address the single-data-center exposure, and it did not prevent the December outage despite years of exactly this kind of incremental investment. Continuing to patch is, in effect, a bet that the three remaining COBOL engineers do not leave and that no second outage of comparable severity occurs before we have another plan ready. We do not think the Board should accept that bet, particularly with Cascade Prairie's renewal on the calendar.

**Buy a third-party settlement platform.** We evaluated two vendors offering settlement platforms marketed to community-bank core processors. The build cost of licensing and integrating either would run $14–17 million over an estimated 20–30 month implementation — comparable in cost and time to the rebuild — but with three material drawbacks. First, both platforms require our 340 customer institutions to adapt to new settlement file formats and cutoff schedules, creating a customer-facing migration burden on top of our own, at a moment when customer confidence is already strained. Second, neither vendor's platform natively supports several settlement rules specific to our multi-state customer base without custom development, which erodes much of the claimed time advantage once discovered in due diligence. Third, and most importantly to us, it would make our core settlement capability permanently dependent on a vendor's roadmap and pricing, in the exact function that most differentiates Meridian Ledger from generic core processors. We concluded that buying trades a workforce risk we can manage through hiring for a vendor-dependency risk we cannot, at comparable cost.

**Do nothing pending further study.** We considered recommending a further assessment period before committing capital, given the Board's caution after 2022. We do not believe the facts support additional delay. The retirement in April is fixed. The Cascade Prairie renewal is fixed at October 1. A further study period of even three to six months narrows the runway on both without changing the underlying analysis — Engineering has already scoped the architecture and migration approach in the detail presented here, and additional study would refine estimates at the margin rather than change the conclusion.

We did not seriously evaluate a full stop of settlement-engine investment, given that settlement processing is the core function of the business; a decision to under-invest here is a decision about the company's viability, not a resourcing choice among several reasonable options.

---

## 7. Risks and Mitigations

We see six material risks to this program and address each directly, including the one the Board will ask about first.

**Why this is not 2022.** The 2022 modernization effort was cancelled after $4.3 million with nothing shipped. Our understanding, confirmed with the two engineering leads who remain from that effort, is that it failed for three specific reasons: the target architecture was not fully specified before build work began, funding was released in full at the outset with no interim checkpoints, and there was no external party validating progress against plan — the Board's visibility was limited to management's own status reports. This proposal is structured to close all three gaps: the architecture in Section 2 has been specified to the level of individual services and data flows before this request; funding is staged against independent gate confirmation as described in Sections 4 and 5; and an external technical advisory firm reports gate results directly to the Board, not only to management. We do not offer this as a guarantee — no rebuild of this scope is risk-free — but as the specific structural difference between this request and the one that failed.

**Hiring risk.** Fourteen hires in specialized distributed-systems roles, in the timeframe Ms. Zhou has scoped, is achievable but not certain. If hiring lags, the mitigation is sequencing: Phase 0 and early Phase 1 work can proceed with the nine reassigned engineers alone, at a slower pace, without requiring the schedule to slip immediately. We have built four months of hiring runway into Phase 0 specifically to absorb this risk before it affects the Phase 1 gate.

**Legacy attrition during the transition.** The retention plan in Section 3 reduces but does not eliminate the risk that we lose a second COBOL-knowledgeable engineer before the legacy engine is decommissioned in month 26. The standby specialist contract, funded from contingency, is our insurance against this; we have identified and begun preliminary conversations with one such firm and expect to have a signed standby agreement before Phase 1 begins.

**Parallel-run divergence.** The six-month parallel run exists precisely because the highest risk in any migration of this kind is a subtle logic difference between old and new systems that surfaces only under live volume. Our mitigation is the wave-based approach itself: no institution's live settlement authority transfers until that institution's cohort has run six full months clean, so a divergence discovered in one wave does not propagate to institutions not yet migrated, and the legacy engine remains available as the fallback of record throughout.

**Covenant and revenue risk, specifically tied to Cascade Prairie.** As described in Section 5, our covenant headroom compresses materially in a scenario where Cascade Prairie does not renew. This is the clearest reason the interim remediation plan in Section 4 is being run now, separately from and faster than the 26-month rebuild — it is designed to give Cascade Prairie evidence of change before its October 1 decision, on a timeline the rebuild itself cannot meet.

**Schedule and cost overrun.** Twenty-six months is Engineering's honest estimate, not a floor. The $1.9 million contingency line and the staged funding structure are both direct responses to this risk: a phase that runs over budget or behind schedule triggers a gate review rather than automatic continuation, giving the Board and the independent advisory firm a decision point before further capital is committed.

---

## 8. Authorization Requested

We ask the Board, at the March 4 meeting, to:

1. **Approve the $19.8 million program** as scoped in this memorandum, funded with $12.0 million of operating cash and a $7.8 million draw on the growth facility.
2. **Approve staged disbursement** against the four phase gates described in Section 4, with continuation past Phase 0 conditioned on confirmation by an independent technical advisory firm, engaged for that purpose and reporting directly to the Board.
3. **Authorize management to engage** the independent technical advisory firm and the standby COBOL-specialist support contract, both funded from the program's contingency line.
4. **Approve the staffing plan**, including the 14 new hires and the reassignment of nine engineers from the current product roadmap, and the resulting deferral of the instant-payments rail connector and the multi-entity treasury dashboard, with customer communication led by Engineering ahead of any public roadmap update.
5. **Authorize the CFO to draw on the growth facility** as needed against the funding schedule, subject to the covenant analysis presented in Section 5, and to report covenant headroom to the Board at each quarterly test date for the duration of the program.
6. **Note, for information rather than approval,** that the interim change-management remediation plan addressing the SOC 2 exceptions and the Cascade Prairie renewal is proceeding on existing budget and a separate, faster timeline, with remediation evidence expected by early September.

We believe the facts leave the Board with a narrower choice than it might prefer: not whether to accept risk, but which risk to accept. The current system has already produced a nine-hour outage, two SOC 2 exceptions, and a customer demand for remediation, resting on a workforce that shrinks by one in April. We believe the plan above is the most direct answer available to that set of facts, structured specifically to avoid the failure mode of 2022, and we recommend its approval.

## Appendix A: Covenant Sensitivity Analysis (CFO Brantley)

The growth facility's covenant caps total leverage at three times trailing-twelve-month EBITDA, tested quarterly. The table below shows modeled headroom under the $7.8 million draw across four scenarios, using the March 2026 draw date as the baseline.

| Scenario | Q2 2026 | Q4 2026 | Q2 2027 | Q4 2027 |
|---|---|---|---|---|
| Base case (Cascade Prairie renews, no further outage credits) | 2.4x | 2.3x | 2.2x | 2.1x |
| Cascade Prairie non-renewal only | 2.6x | 2.6x | 2.5x | 2.4x |
| Second outage-credit event only ($1.5M assumed) | 2.5x | 2.4x | 2.3x | 2.2x |
| Combined: non-renewal + second outage event | 2.8x | 2.8x | 2.7x | 2.6x |

In all four scenarios the ratio remains below the 3.0x cap, but the combined scenario leaves headroom of roughly 0.2x at the tightest quarter, which we would regard as insufficient buffer against any further unmodeled deterioration — a lower-than-forecast renewal rate among the remaining 339 institutions, a delay in the parallel-run cost curve, or a draw timing that front-loads more of the facility than currently planned. We do not read this as a reason to withhold approval; the base case clears the covenant with over half a turn of headroom throughout. We read it as confirmation that the interim remediation effort aimed at Cascade Prairie's October 1 decision is doing real financial work for the company, independent of its value to the SOC 2 exception itself, and we will bring updated figures to the Board at each quarterly test date rather than waiting for the annual review cycle.

We have also modeled a delayed-draw structure, taking the $7.8 million in three tranches of $2.6 million tied to the Phase 0, Phase 1, and Phase 2 gates rather than as a single draw at signing. This improves early-quarter headroom by roughly 0.1–0.15x per undrawn tranche and costs an estimated $40,000 in additional facility fees over the program's life. We recommend the tranche structure and have modeled it, not the single draw, as the basis for the figures above.

## Appendix B: Phase Gate Governance Detail

Each phase gate review will include the following parties and produce a written determination circulated to the full Board within five business days of the review:

| Party | Role at gate review |
|---|---|
| Independent technical advisory firm | Assesses gate criteria against evidence; issues pass/fail/conditional determination |
| VP Engineering (Zhou) | Presents build status, test results, and staffing status |
| CTO (Petrosyan) | Presents architecture and integration status; owns overall program |
| CRO (Farouk) | Assesses institution-facing risk, including any customer communications required by the gate outcome |
| CFO (Brantley) | Confirms budget-to-actual and covenant headroom at gate date |
| Board-designated observer | Attends all gate reviews; may request additional information before the determination is finalized |

A "conditional pass" — meaning the gate criteria are substantially but not fully met — triggers a supplemental review within 30 days rather than an automatic continuation or an automatic halt. A "fail" determination pauses further disbursement pending a Board decision on remediation, rescoping, or termination of the program, and returns any undrawn tranche of the growth-facility allocation to the covenant calculation as unused capacity. We are building this failure path deliberately, so that a gate miss produces a decision point rather than either silent continuation or an unplanned full stop.

## Appendix C: Customer Communication Sequencing

Because the roadmap deferrals and the migration itself both touch customers directly, we are sequencing communication separately from the internal program schedule, on the following basis:

**Cascade Prairie Bancorp** receives the interim remediation plan directly, in writing, no later than August 15 — six weeks ahead of the October 1 renewal — with a follow-up review call before the renewal decision date. This is owned by Nadia Farouk and briefed to the Board separately from this program's quarterly updates, given the time sensitivity.

**Institutions affected by the December 27 outage** (118 total) receive a written summary of the remediation program, distinct from the settlement-credit correspondence already sent, within 30 days of Board authorization. This communication will describe the interim change-management hardening only; it will not commit to rebuild timelines to customers until Phase 1 has cleared its gate, consistent with our general practice of not making external commitments against unproven internal schedules.

**Customers committed the instant-payments rail connector or the multi-entity treasury dashboard** receive individual outreach from account management, briefed by Engineering, before any general roadmap communication. Ms. Zhou's team has identified 23 institutions with an explicit commitment date for one or both features; those conversations will be completed within 45 days of authorization, ahead of any customer newsletter or roadmap webinar reference to the deferral.

**The remaining customer base** receives no proactive communication about the rebuild program itself until the Phase 1 gate has passed, on the view that an announcement of a 26-month infrastructure program, made before the architecture has been proven against live-shadow traffic, carries more downside if the program later re-scopes than upside from early transparency. We will revisit this position at the Phase 1 gate review.

## Appendix D: Program Organization Chart (Summary)

Reporting lines for the duration of the program, effective on authorization:

- **Executive sponsor:** Rosalind Achebe, CEO — Board liaison, quarterly reporting owner
- **Program owner:** Viktor Petrosyan, CTO — architecture authority, gate-review chair
- **Delivery lead:** Meiling Zhou, VP Engineering — staffing, build execution, roadmap-deferral communication
- **Risk oversight:** Nadia Farouk, CRO — customer-facing risk assessment, Cascade Prairie relationship, SOC 2 remediation tracking
- **Finance:** Harold Brantley, CFO — funding draws, covenant monitoring, budget-to-actual reporting
- **Independent verification:** External technical advisory firm (to be engaged within 30 days of authorization) — gate determinations, direct Board reporting line
- **Legacy systems team:** Four COBOL-knowledgeable engineers, reporting to Petrosyan, ring-fenced from rebuild-team workload for the duration of the program

This structure will be confirmed in writing to all program participants within ten business days of Board authorization, with the independent advisory firm's engagement letter, including its direct Board reporting obligation, executed before Phase 0 work begins.

---

We are available to walk through any section of this proposal, and the underlying models referenced in Appendix A, in advance of the March 4 meeting, and will circulate the full appendix set electronically no later than February 27.

Respectfully submitted,

**Rosalind Achebe**
Chief Executive Officer

**Viktor Petrosyan**
Chief Technology Officer
