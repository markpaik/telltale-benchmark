# Consolidation Under Fire: How Cahaba Bend County, Alabama, Merged Four Emergency Dispatch Centers, Survived a Catastrophic Cutover, and Emerged With a Faster System

## A Case Study in Public Safety Technology Consolidation

---

## Introduction

On the morning of February 18, 2025, the telecommunicators of Cahaba Bend County's newly consolidated emergency communications center watched their screens go dark. For four hours and forty minutes, in a county of 264,000 people, every 911 call — 812 of them before service was restored — was handled with pen, paper, runners, and radio discipline that most of the staff had never practiced outside of a tabletop exercise. Two of the four municipalities that had helped pay for the new center threatened to pull out of the arrangement entirely. The administrator of a $5.2 million state grant opened a formal review that could have clawed back more than a quarter of the project's funding.

Four months later, the same center was assigning units to emergency calls in two minutes and fourteen seconds on average — nearly ninety seconds faster than the county had ever managed before — with an abandoned-call rate that had fallen from 7.9 percent to 2.1 percent. The project that nearly collapsed in a single morning had, by mid-2025, delivered essentially everything its champions had promised, at a final cost of $21.4 million against an original projection of $18.6 million.

The story of how Cahaba Bend County got from the first of those mornings to the second is a case study in the full life cycle of a public-sector consolidation: the operational failures that made the status quo untenable, the political coalition-building required to authorize change, the vendor and technical failures that nearly destroyed the effort, and the recovery decisions — some expensive, some merely disciplined — that ultimately salvaged it. It is also, in the candid assessment of the county's own leadership, a story about sequencing: nearly every painful lesson the county learned the hard way was a lesson about the order in which things should have been done, not whether they should have been done at all.

This case study follows the project chronologically, from the conditions that existed before 2023 through the results measured in June 2025, and closes with the lessons a county administrator, emergency communications director, or IT leader in a comparable position should take from it.

---

## Part One: The Baseline — Four Centers, Four Systems, One County

### The organization and its situation

Cahaba Bend County sits in central Alabama, a mixed urban-suburban-rural county of 264,000 residents spread across a county seat, three smaller incorporated municipalities, and a substantial unincorporated area served directly by the Sheriff's Office. Like many counties of its size, its emergency communications infrastructure had grown up piecemeal over decades. By 2022, the county was operating four separate emergency dispatch centers — one run by the Sheriff's Office, and the others aligned with municipal police and fire jurisdictions — staffed collectively by 88 telecommunicators.

The four centers ran four incompatible computer-aided dispatch systems. Incompatible is a word that hides a great deal of daily friction. A call originating in one jurisdiction but requiring a unit from another had to be relayed by phone or radio between centers, with the receiving telecommunicator re-entering the call information by hand into a different system with different fields, different codes, and different mapping data. Address databases were maintained separately and drifted apart. A structure fire near a jurisdictional boundary could generate three separate call records in three separate systems, none of which could see the others. Mutual aid, which in principle should have been the county's strength, was in practice its slowest and most error-prone workflow.

### The problem, measured

The consequences showed up in four numbers that would eventually anchor the entire case for consolidation.

First, the average time from call answer to unit assignment across the four centers was **three minutes and 41 seconds**. National best-practice standards for high-priority calls contemplate dispatch times measured in tens of seconds, not minutes. Some of Cahaba Bend's delay was structural — the cross-center relay problem — and some was the accumulated cost of aging systems, inconsistent protocols, and thin staffing on overnight shifts at the smaller centers.

Second, **7.9 percent of incoming calls were abandoned** — callers who hung up before a telecommunicator answered. Every abandoned call generated a callback obligation, consuming still more staff time, and every abandoned call represented a resident in some state of distress who gave up on the system before it responded.

Third, annual dispatch overtime across the four centers ran **$2.1 million**. Four centers meant four sets of minimum staffing requirements around the clock. A center that needed three telecommunicators on an overnight shift needed three whether call volume justified them or not, and a sick call at any one center triggered overtime at that center even if another center across the county was overstaffed at that hour. The overtime figure was, in effect, the annual price of maintaining four separate staffing floors instead of one.

Fourth, and feeding directly into the third, **annual turnover among telecommunicators reached 34 percent**. Emergency telecommunications is a high-stress occupation everywhere, but Cahaba Bend's turnover ran well above regional norms. Exit interviews and internal surveys pointed to forced overtime, outdated tools, and — at the smaller centers — a sense of professional isolation and limited advancement. High turnover meant a workforce perpetually heavy with trainees, which slowed call processing further, which increased stress, which drove more turnover. The four numbers were not independent problems; they were one problem expressed four ways.

### The people who decided to act

Two officials owned the problem. County Administrator **Delphine Roussard**, who had spent years watching the overtime line grow in each budget cycle, saw consolidation primarily as a fiscal and governance issue: the county was paying four times for capabilities it needed once. Emergency Communications Director **Ramon Escalante**, a former telecommunicator himself, saw it as an operational and human issue: the fragmented architecture was slowing dispatch, burning out staff, and creating risk at every jurisdictional seam. In late 2022, the two began building a formal proposal to consolidate the four centers into a single county emergency communications center.

---

## Part Two: The Case for Consolidation — Justified to Whom, and How

### The proposal

The plan Roussard and Escalante brought forward in early 2023 called for a single consolidated dispatch center, a unified computer-aided dispatch platform replacing all four legacy systems, unified call-taking and dispatch protocols, and the absorption of all 88 telecommunicators into a single county workforce. The projected cost was **$18.6 million**, financed through three sources: **$11 million in county bonds**, a **$5.2 million state grant** for emergency communications modernization, and **$2.4 million assessed to the four municipalities** whose residents and public safety agencies would be served by the center.

The funding structure was itself a political design. By splitting the cost three ways, the proposal spread ownership: the county carried the largest share and the debt; the state grant validated the project as consistent with statewide interoperability goals and reduced the local burden; and the municipal assessments — modest relative to what each municipality was spending on its own dispatch operations — bought the municipalities a seat at the governance table and a stake in the outcome. That last piece would prove double-edged. The assessments gave municipalities standing to demand performance, and when performance failed on February 18, 2025, they exercised it.

### The audiences

The consolidation case had to be made to at least five distinct audiences, and Roussard and Escalante tailored the argument to each.

**To the County Commission**, the case was fiscal. The $2.1 million annual overtime figure was the centerpiece: a consolidated center with a single staffing pool could flex personnel across the whole operation, cutting the structural overtime driven by four separate minimum-staffing floors. Combined with the elimination of four separate system maintenance contracts and eventual facility savings, the project projected an operational payback that made the $11 million bond issue defensible.

**To the municipalities**, the case was service and cost avoidance. Each municipality faced its own looming capital costs to replace aging dispatch equipment. The $2.4 million collective assessment was framed as far cheaper than four separate modernization projects, and the consolidated center promised each municipality faster dispatch — particularly on cross-jurisdictional calls — without the burden of running its own center.

**To the state grant administrator**, the case was interoperability and standards compliance. The state's grant program existed precisely to reduce the number of small, incompatible dispatch operations, and Cahaba Bend's application aligned squarely with that goal. The $5.2 million award came with performance conditions — a fact that would matter enormously later.

**To the public**, the case was response time and reliability. Three minutes and 41 seconds to assign a unit, and nearly one in twelve calls abandoned, were numbers that translated directly into a message any resident could understand: when you call 911 in this county, the answer comes too slowly, and sometimes it doesn't come at all.

**To the telecommunicators themselves**, the case was hardest and, in retrospect, the most important. Consolidation projects are routinely read by dispatch staff as job-cut programs, and Escalante moved early to close off that interpretation: all 88 positions would carry over, the consolidated center would offer a unified pay and career structure, and the reduction in forced overtime was pitched as a direct quality-of-life improvement. Escalante's credibility as a former telecommunicator carried weight, but skepticism remained, particularly among senior staff at the smaller centers who stood to lose informal seniority and familiar routines.

### The opposition and the vote

The proposal did not glide through. **Sheriff Wanda Pruitt** opposed consolidation and fought it through two commission votes. Her opposition rested on arguments familiar to anyone who has watched a dispatch consolidation contested: loss of direct operational control over dispatch for Sheriff's Office deputies; concern that a county-run civilian center would not prioritize law enforcement calls with the immediacy of the Sheriff's own dispatchers; and skepticism — which events would partially vindicate — that a large, complex technology migration could be executed on schedule and on budget. Pruitt's position carried institutional weight. Sheriffs in Alabama are independently elected constitutional officers, and her opposition gave political cover to commissioners uneasy about the bond issue.

The first commission vote failed to produce a majority for the project. The proposal was revised — governance provisions were strengthened to guarantee law enforcement representation in operational oversight, and reporting requirements to the commission were tightened — and brought back. In **May 2023**, on the second vote, **Council Chair Elias Mwangi delivered the deciding vote** in favor. Mwangi's public rationale was straightforward: the status quo's numbers were indefensible, the funding package would never be better assembled than it was now, and the risks of the project were manageable while the risks of inaction were not. It was a defensible judgment. It also meant that Mwangi, personally, now owned the project's success or failure — a fact that shaped the political dynamics when failure arrived.

The vote's closeness left a residue. The project began life with the county's most prominent public safety official on record against it and with a commission majority of exactly one. There was no reservoir of political goodwill to absorb a crisis. The project would have to earn its legitimacy through execution — and its execution was about to go badly wrong.

---

## Part Three: Execution — The Vendor, the Slip, and the Cutover

### Procurement and the missed go-live

The county selected **Lattimore Public Safety Systems** as the vendor for the consolidated computer-aided dispatch platform, call-handling integration, and mapping services. The contract set a **go-live date of October 2024** — roughly seventeen months from authorization, an aggressive but not unheard-of timeline for a four-center consolidation.

Lattimore missed the date. The reasons were the usual compound of causes: data migration from four incompatible legacy systems proved messier than scoped, with address and geographic data requiring far more reconciliation than the vendor had budgeted; interface development for records systems and radio integration ran behind; and testing cycles kept surfacing defects faster than they were being closed. The county, to its credit, refused pressure to go live on schedule with known open defects. But the slip carried costs of its own. Every month of delay extended the life of four legacy maintenance contracts, kept the overtime engine running, and — critically — compressed the political patience available for the eventual cutover. By early 2025, the municipalities that had paid their assessments in 2023 were asking pointed questions about what they had bought.

The rescheduled cutover was set for **February 18, 2025**. The plan was a single "big bang" migration: all four centers, all three disciplines — police, fire, and medical — moving to the new consolidated platform at once. In hindsight, every party to the project would identify this as the central error. At the time, the big-bang approach was defended on plausible grounds: running old and new systems simultaneously was operationally complex and expensive; a single cutover minimized the period during which telecommunicators would juggle two systems; and the project was already four months late, with stakeholders demanding a finish line. The pressure to be done overrode the discipline to be careful.

### February 18, 2025: The outage

The cutover began in the early hours of February 18. Initial call handling on the new platform appeared functional. Then the mapping service — the component that translates a caller's location into a dispatchable address and drives unit recommendations — failed. And when it failed, its failover path, the redundant route that was supposed to keep location services alive, failed too, because it had **never been tested under production conditions**.

The result was a **four-hour-and-forty-minute outage** of the consolidated dispatch platform. Calls still reached the center — the telephony layer held — but telecommunicators lost computer-aided dispatch entirely: no automated location, no unit recommendations, no digital call records, no status tracking.

The center fell back to manual operations. Over the course of the outage, **812 calls were handled on paper**: call-takers writing addresses and complaints on cards, runners carrying cards to dispatchers, dispatchers working from wall maps and radio logs, supervisors manually tracking unit status on whiteboards. The staff — 88 telecommunicators, many of whom had never run a sustained manual operation — improvised a functioning paper dispatch center in real time. It is one of the underappreciated facts of the incident that, amid the failure, the human system held. The county has never attributed a death or serious harm directly to the outage, though several calls experienced significant dispatch delays, and the after-action review treated the absence of a catastrophic outcome as substantially a matter of luck and staff competence rather than system design.

By late morning, the mapping service was restored through a manual reconfiguration and the platform came back up. The technical crisis was over. The political crisis was beginning.

### The political fallout

The fallout arrived on three fronts within days.

**The municipalities.** Two of the four municipalities that had contributed to the $2.4 million assessment **threatened to withdraw from the consolidated arrangement** and re-establish independent dispatch. Their argument was blunt: they had traded control for a promise of better service, and the first day of the new system had delivered the worst dispatch failure in county memory. Withdrawal threats were partly genuine and partly leverage — re-establishing independent centers would have been slow and expensive for the municipalities — but they were credible enough to threaten the project's core premise. A consolidation that lost two of its four partners would have been a consolidation in name only, and the financial model, built on shared assessments and shared call volume, would have unraveled.

**The state.** The **state grant administrator opened a formal review** of the $5.2 million award. Grant conditions tied funding to successful implementation and performance milestones; a multi-hour total outage on cutover day put the county in jeopardy of findings that could suspend remaining disbursements or, in the worst case, require repayment. The review meant months of documentation demands, site visits, and reporting obligations layered on top of the recovery effort itself — and it meant the county's remediation plan had to satisfy not just local stakeholders but a state overseer with the power to blow a $5.2 million hole in the budget.

**The commission and the Sheriff.** Sheriff Pruitt, who had opposed the project through two votes, did not need to say much; events had made her argument for her. Calls emerged for pausing the project, for reverting permanently to the legacy systems, and — from some quarters — for personnel consequences. Chair Mwangi, whose deciding vote had authorized the project, faced the sharpest exposure. His response, and Roussard's, set the trajectory for everything that followed: rather than defending the cutover or minimizing the outage, the county leadership publicly acknowledged the failure in full, committed to an independent root-cause analysis, and framed the choice ahead honestly — the county could abandon a project that was 90 percent built and return to a status quo everyone agreed was failing, or it could fix the project. They chose to fix it, and they staked their credibility on doing so transparently.

---

## Part Four: The Recovery — Root Cause, Accountability, and a Rebuilt Rollout

### Finding the cause

The technical investigation was led by **Information Technology Director Vikram Chaudhary**. His finding was precise and damning in its simplicity: the outage was caused by **an untested failover path in the mapping service**. The primary mapping service had failed under production load — itself a defect, but a survivable one. The failover configuration that should have absorbed the failure had been installed and documented but never exercised under realistic conditions. When it was called upon for the first time in production, a configuration error prevented it from taking over. The redundancy existed on paper and in the architecture diagrams. It had simply never been proven.

Chaudhary's report widened from that finding into a broader indictment of the testing regime: failover and disaster-recovery paths across the platform had been verified by inspection rather than by live exercise; load testing had not replicated the combined call volume of all four centers hitting the system simultaneously; and the go/no-go criteria for the cutover had not included demonstrated failover for critical services. The report was made public — a decision Roussard insisted on, over some internal objection, on the theory that the state review and the municipalities would trust nothing less than full disclosure. The transparency proved to be one of the recovery's most valuable assets: it converted the narrative from cover-up risk to competence-rebuilding, and it gave the state grant administrator a documented basis for allowing the project to continue under monitoring rather than pulling funding.

### Holding the vendor to account

The county **enforced a $900,000 contractual penalty against Lattimore Public Safety Systems**. The contract's performance provisions — negotiated, with some prescience, over vendor objection during procurement — tied penalties to availability failures and missed milestones, and the county invoked them in full rather than negotiating them away in exchange for future goodwill. The decision was debated internally: some argued that penalizing the vendor mid-project would poison the working relationship needed to finish it. Roussard's position prevailed: the penalty was the contract working as designed, the municipalities and the state needed to see accountability applied to the vendor and not only absorbed by the county, and a vendor that would sabotage remediation over an enforced penalty was a vendor the county needed to discover sooner rather than later. In the event, Lattimore paid the penalty, retained the contract, and — with its own reputation now attached to the recovery — committed senior engineering resources to the remediation at a level the county had struggled to obtain before the outage.

### Parallel operations: eleven weeks of expensive insurance

The centerpiece of the recovery plan reversed the original cutover philosophy. Instead of a second big-bang attempt, the county ran the **old and new systems in parallel for eleven weeks**. The four legacy dispatch systems were kept alive and staffed as the authoritative fallback while the consolidated platform ran alongside, processing live call data and being exercised — deliberately and repeatedly — through failure scenarios, including full failover drills of the mapping service and every other critical component. Nothing would be trusted that had not been broken and recovered under observation.

Parallel operation was costly. It required maintaining legacy system contracts and infrastructure that had been scheduled for decommissioning, and it demanded extra staff hours to operate and compare both environments — costs that contributed materially to the project's final overrun. But it bought the one thing the February cutover had lacked: proof. By the end of the eleven weeks, the failover paths had been exercised dozens of times, the load characteristics of the full consolidated call volume were known rather than estimated, and the go/no-go criteria for final migration were written in terms of demonstrated behavior, not vendor attestation.

### Retraining all 88 telecommunicators

Concurrently, the county **retrained the entire telecommunicator workforce — all 88 staff** — on the new platform. The original training program, compressed by the schedule pressure of late 2024, had emphasized basic operation of the new system. The retraining program, informed by the outage, was rebuilt around two additions. First, deep proficiency: scenario-based training on the consolidated protocols, cross-discipline call handling, and the unified mapping and unit-recommendation tools, with competency verification rather than attendance as the completion standard. Second — and this was a direct legacy of February 18 — **formalized manual fallback procedures**. The improvised paper operation that had carried 812 calls through the outage was studied, standardized, documented, and drilled, so that a future outage would be met with a practiced procedure rather than heroic improvisation. The retraining also served a morale function that Escalante considered as important as the skills transfer: it signaled to a shaken workforce that the county was investing in them rather than blaming them, and it gave the staff who had held the line during the outage formal ownership of the contingency procedures they had invented.

### Three waves instead of one

The final migration abandoned the single cutover entirely. **Police, fire, and medical dispatch moved to the consolidated platform in three separate waves**, each separated by a stabilization period. Each wave migrated one discipline while the others remained on the parallel-run safety net; each wave had explicit entry criteria (demonstrated performance in parallel operation, completed retraining for the affected staff, tested failover for every service the wave depended on) and explicit rollback criteria that would return the discipline to legacy systems if defined thresholds were breached. Each wave's stabilization period was used to observe real performance, fix defects, and adjust protocols before the next discipline moved.

The phased approach cost time and money that the big-bang approach had been designed to save. It also worked. None of the three waves required rollback. Defects surfaced in each wave — as they always do — but they surfaced in a context where only one discipline was exposed, fallback was rehearsed and available, and the staff operating the system had been trained on exactly the failure modes they might encounter. By late spring 2025, all three disciplines were running on the consolidated platform, the legacy systems were finally decommissioned, and the parallel-run insurance policy was retired.

The state grant review, which had shadowed the entire recovery, closed with the funding intact. The combination of the public root-cause report, the enforced vendor penalty, the parallel-run discipline, and the phased migration gave the grant administrator a documented remediation narrative that satisfied the program's conditions. The two municipalities that had threatened withdrawal stayed. Their price was governance: strengthened performance reporting to the member municipalities and a standing role in operational oversight — concessions the county judged cheap against the alternative.

---

## Part Five: The Results — Before and After, and the True Cost

### The numbers

By **June 2025**, four months after the outage and weeks after the final migration wave, the county measured its performance against the 2022–2023 baseline:

| Measure | Baseline (pre-consolidation) | June 2025 | Change |
|---|---|---|---|
| Average call-answer to unit assignment | 3 min 41 sec | 2 min 14 sec | **–1 min 27 sec (–39%)** |
| Abandoned call rate | 7.9% | 2.1% | **–5.8 points (–73%)** |
| Annual dispatch overtime | $2.1 million | $1.3 million | **–$800,000/yr (–38%)** |
| Dispatch centers / CAD systems | 4 / 4 incompatible | 1 / 1 | Unified |
| Telecommunicator workforce | 88 across four centers | 88, single center | Retained in full |

The call-to-assignment improvement — a minute and 27 seconds shaved from the average — flowed from the structural changes the consolidation had promised all along: no more cross-center relays and manual re-entry, a single accurate address database, unified protocols, and unit recommendations drawn from the county's entire resource pool rather than one jurisdiction's slice of it. The abandoned-call collapse from 7.9 to 2.1 percent reflected the consolidated staffing pool's ability to surge call-takers against demand in a way four separate minimum-staffed rooms never could. The overtime reduction — $800,000 annually — came from the same source: one staffing floor instead of four, and a schedule that could flex across the whole operation.

Turnover, the fourth baseline pathology, is the metric with the shortest measurement window; a 34 percent annual rate cannot be declared cured in four months. But the early indicators — reduced forced overtime, a unified career structure, and, perhaps counterintuitively, the cohesion forged among the staff who had run the paper operation together on February 18 — pointed in the right direction, and the county retained all 88 positions through a transition that many staff had initially feared as a downsizing.

### The true cost

The final project cost was **$21.4 million** against the original projection of **$18.6 million** — an overrun of **$2.8 million, or roughly 15 percent**. The overrun decomposed into the recovery itself: eleven weeks of parallel operations, including extended legacy system contracts and dual-environment staffing; the comprehensive retraining of all 88 telecommunicators; the extended and repeated testing regime; the three-wave migration with its stabilization periods; and the additional program management, independent review, and reporting demanded by the state grant review and the municipal governance concessions. Against the gross overrun, the county set the **$900,000 vendor penalty**, which offset roughly a third of the overage; the net additional cost to the county and its partners was on the order of $1.9 million.

An honest accounting of the true cost extends beyond the capital figure. The county paid four extra months of legacy overtime and maintenance during the vendor delay. It paid, unquantifiably, in the risk carried by 812 callers during the outage. And it paid politically: the project consumed the credibility of its champions for the better part of a year, handed its opponents a vindicating crisis, and survived by a margin — one commission vote, two wavering municipalities, one grant review — that no responsible planner would design into a project on purpose.

Against those costs stand the returns. The $800,000 annual overtime reduction alone, if sustained, recovers the net overrun in under three years. The eliminated legacy maintenance contracts, avoided municipal capital replacements, and consolidated facility footprint compound the operational savings. And the performance improvements — a 39 percent faster dispatch and a 73 percent reduction in abandoned calls — are the kind of returns that do not appear on a balance sheet until the day they matter to a particular caller, at which point they are the only returns that matter.

---

## Part Six: What Cahaba Bend Would Sequence Differently — and What a Reader Should Take From It

The county's own after-action assessment, echoed publicly by Roussard, Escalante, and Chaudhary, is notable for what it does not conclude. It does not conclude that consolidation was a mistake, that the vendor should not have been selected, or that the political coalition was wrongly assembled. Nearly every finding is a finding about **sequence**: the county did most of the right things, and did too many of them in the wrong order, or only after failure forced them. For a reader in a comparable position — a county administrator, communications director, or IT leader contemplating a consolidation — the lessons organize themselves around what Cahaba Bend would reorder.

**1. Prove failover before go-live, not after an outage.** The single proximate cause of the February 18 crisis was a failover path that existed in the architecture and had never been exercised. Everything the county did during the eleven-week parallel run — live failover drills, full-volume load testing, behavior-based go/no-go criteria — was available before the first cutover. The county sequenced testing after commitment; it should have sequenced demonstrated resilience as a precondition of commitment. The rule the county now applies to every critical system is blunt: *redundancy that has not been exercised in production-realistic conditions does not exist.*

**2. Phase the migration from the start.** The three-wave, discipline-by-discipline migration succeeded precisely where the big bang failed, and its costs — duplicated operations, extended timeline — were costs the county ended up paying anyway, plus the price of the outage. A phased rollout should have been the original plan, with the parallel-run period budgeted honestly from day one rather than treated as an emergency expense. The false economy of the big bang is that it books the savings of a short transition while ignoring the expected cost of transition failure. In a system where failure means unanswered 911 calls, that expected cost dominates.

**3. Build and drill the manual fallback before you need it.** The county's staff improvised a paper dispatch operation under live fire and carried 812 calls through it. That the improvisation succeeded was a tribute to the workforce, not the plan. The formalized, drilled fallback procedures created during retraining should have preceded the first cutover. Any organization migrating a life-safety system should treat a rehearsed degraded-mode operation as part of the go-live package, not a lesson of the post-mortem.

**4. Let the schedule slip absorb pressure — don't let pressure compress testing.** The county rightly refused to go live in October 2024 with open defects. But the four-month slip generated political pressure that was then discharged into the February cutover in the form of compressed final testing and a single-shot migration. The sequencing failure was allowing schedule pressure to accumulate against the last, least compressible phase of the project. Leaders should build public expectations around milestone quality rather than calendar dates, and should treat the final testing window as the one element of the schedule that grows, never shrinks, under pressure.

**5. Negotiate accountability instruments before you need them, and use them when you do.** The $900,000 penalty was available only because performance provisions had been negotiated into the contract at procurement — a sequencing decision that paid off years later. Enforcing it, rather than trading it away, offset a third of the overrun and gave municipalities and the state visible evidence that accountability ran to the vendor as well as the county. The counterintuitive result was a more, not less, committed vendor during remediation.

**6. Sequence transparency ahead of the narrative.** The county's decision to publish Chaudhary's root-cause report in full, quickly, converted the political crisis from a question of concealment into a question of competence — a question the recovery could then answer. The grant review closed with funding intact, and the wavering municipalities stayed, in substantial part because the county gave overseers a documented failure analysis and remediation plan before being compelled to. Organizations instinctively sequence disclosure after recovery; Cahaba Bend's experience argues for the reverse.

**7. Treat the workforce as the system's true redundancy.** Retaining all 88 telecommunicators, retraining them comprehensively, and formally adopting the contingency procedures they invented did more than transfer skills — it converted the outage from a trauma into a shared institutional achievement. The staff were the component that did not fail on February 18. Consolidations that treat headcount as the savings target forfeit exactly the resilience that saved this one.

**8. Budget for the recovery you hope not to need.** The honest projected cost of this project was never $18.6 million; it was $18.6 million plus the price of prudence — parallel operations, exhaustive testing, phased migration, deep training — that the original budget omitted and the crisis forced. A reader planning a comparable consolidation should present the prudent number up front. It will be harder to sell. It will be a fraction of the cost, in every currency that matters, of buying the same prudence after a failure.

---

## Conclusion

Cahaba Bend County's consolidation ended where its proponents said it would: one center, one system, dispatch 39 percent faster, abandoned calls down 73 percent, overtime down $800,000 a year, all 88 telecommunicators retained. It arrived there through a four-hour-and-forty-minute failure that nearly unwound the political coalition, the municipal partnership, and the state funding that made the project possible — a failure traceable to a single untested failover path, and behind that, to a sequence of decisions that put the finish line ahead of the proof.

The case's final lesson is the one Roussard has offered when asked what she would tell a peer county: the consolidation was the right project, approved for the right reasons, and it very nearly failed anyway — not because the destination was wrong, but because the county tried to arrive all at once. The counties that will do this well are not the ones that avoid Cahaba Bend's ambition. They are the ones that borrow its recovery plan and run it first.
