# When the Migration Broke: Tidewater Health Interfaces and the Rebuild of a Clinical Middleware Platform

## A Case Study in Platform Modernization, Migration Failure, and Recovery

---

## Executive Summary

Tidewater Health Interfaces, a Durham, North Carolina company selling clinical integration middleware to 340 hospitals, spent 2024 and 2025 rebuilding a thirteen-year-old customer-hosted product into a multi-tenant hosted service. The rebuild was forced by deteriorating fundamentals: uptime running well below contractual commitments, a support queue of 4,100 tickets a month, 14 percent annual churn, and $5.2 million in enterprise renewals at risk. The board approved an $8.5 million, 18-month program in March 2024.

The first large migration wave, in November 2024, failed. The new queueing layer could not absorb overnight batch loads from 28 hospitals migrated at once, 1.2 million clinical messages backed up over four days, three hospitals reverted to the legacy engine, a 900-bed health system left for a competitor, and $1.1 million in service credits went out the door. In December, the company's customer-facing leaders forced a halt to all migrations.

What followed was a fundamental change in method rather than a change in goal: nine additional migration engineers, mandatory two-week shadow-mode validation of every customer against production traffic before cutover, migration of one hospital at a time, and a candid reset with the board that moved the finish date to December 2025. By July 2025, 190 of 340 customers had migrated, uptime stood at 99.96 percent — above the contractual 99.95 percent for the first time in the company's hosted history — monthly tickets had fallen from 4,100 to 1,700, annual churn had dropped from 14 percent to 6 percent, and the annual cost to serve a customer had fallen from $11,400 to $6,900. Total program spend stood at $12.3 million, 45 percent over the original budget, against a business that was measurably healthier on every operating dimension that mattered.

This case follows the story chronologically: the state of the platform and the business that forced the rebuild, the plan and the assumptions embedded in it, the failed wave and its cost in money and customers, the changed method, the results through mid-2025, and what the company's leadership would do differently. It closes with lessons for executives and technical leaders facing similar modernization decisions.

---

## Part One: The Company and the Platform It Outgrew

### The Business Tidewater Built

Tidewater Health Interfaces occupies a corner of health IT that most patients never see and most hospitals cannot live without. Clinical integration middleware is the connective tissue between the systems inside a hospital: the electronic health record, the laboratory information system, the pharmacy system, radiology, admission-discharge-transfer feeds, billing, and the growing constellation of specialty applications that every health system accumulates. When a lab result needs to appear in a physician's chart, when an admission needs to trigger a pharmacy profile, when a discharge needs to flow to a billing system, middleware like Tidewater's carries the message, transforms it into the format the receiving system expects, and guarantees it arrives.

By 2023 the company had built a substantial business on this work: 340 hospital customers, 210 employees, and $46 million in recurring revenue, an average of roughly $135,000 per customer per year. Its customers ranged from small community hospitals to large multi-facility health systems, and its contracts carried the service commitments that clinical infrastructure demands — most notably a 99.95 percent uptime guarantee, which allows for a little over four hours of downtime in a year.

The product itself, however, was showing its age in ways the revenue line concealed. The core interface engine had been written in 2011, in an era when the standard deployment model in health IT was customer-hosted software: the hospital ran Tidewater's engine on its own servers, inside its own data center, managed by its own IT staff with support from Tidewater. That model made sense in 2011. Hospitals were deeply wary of clinical data leaving their walls, cloud infrastructure was immature for regulated workloads, and vendors competed on how well their software behaved inside a customer's environment.

By 2023, that model had become the company's central liability.

### The State of the Platform in 2023

Four numbers describe the situation Tidewater's leadership confronted at the end of 2023.

**First, hosted adoption was almost nonexistent.** Only 14 of 340 customers — about 4 percent — were running on Tidewater's hosted version of the product. The other 326 ran the engine on their own infrastructure, which meant 326 distinct environments, 326 combinations of operating system versions, patch levels, network configurations, and locally applied customizations. Every support call began with the question of what, exactly, the customer was running. Every product release had to be tested against a matrix of environments Tidewater did not control and, in many cases, could not even see.

**Second, the hosted product that did exist was failing its own service commitment.** Uptime on the hosted version averaged 99.1 percent against the contractual 99.95 percent. The gap sounds small expressed in percentage points; expressed in hours it is enormous. A 99.95 percent commitment allows roughly 4.4 hours of downtime per year. A 99.1 percent reality delivers roughly 79 hours — more than three full days of accumulated outage annually, on a product carrying lab results, medication orders, and admission feeds. Every breach of the commitment generated service credits, uncomfortable executive conversations, and ammunition for competitors in renewal negotiations. Worse, it undermined the one argument Tidewater needed to make to its market: that hospitals should trust the company to run this infrastructure on their behalf.

**Third, the support burden was crushing.** Tidewater's support organization was handling 4,100 tickets a month — an average of roughly twelve tickets per customer per year, but distributed unevenly, with the most heavily customized customer-hosted environments generating a disproportionate share. At 4,100 tickets a month, support was not a function that resolved problems; it was a treadmill that consumed the company. Engineers who should have been building product were pulled into escalations. The cost to serve a customer had climbed to $11,400 a year, an unsustainable figure against an average contract value of roughly $135,000 — support and service delivery alone were consuming more than 8 percent of revenue before a single dollar went to sales, engineering, or general operations.

**Fourth, and most dangerously, customers were leaving.** Annual churn had reached 14 percent. On a base of 340 hospitals, that meant Tidewater was losing roughly 48 customers a year and had to replace them just to stand still. In enterprise health IT — where sales cycles run twelve to eighteen months and switching costs are supposed to be a moat — 14 percent churn is not a warning sign; it is a verdict. Customers were not leaving because a competitor had a dramatically better product. They were leaving because the operational experience of being a Tidewater customer — the outages, the ticket volume, the burden of hosting and maintaining the engine themselves — had become worse than the pain of switching.

The verdict had a dollar figure attached. Two enterprise renewals worth a combined $5.2 million — more than 11 percent of the company's entire recurring revenue — were formally at risk, with both customers citing reliability and the customer-hosted operational burden as their reasons for evaluating alternatives.

### The Strategic Diagnosis

Chief Executive Prabha Venkataraman and Chief Technology Officer Nils Bergstrom reached the same conclusion from different directions. Venkataraman saw a business whose unit economics and retention were deteriorating in ways that incremental fixes would not reverse. Bergstrom saw a 2011-era engine whose architecture made every fix expensive: single-tenant by design, deployed into environments the company did not control, impossible to observe centrally, impossible to upgrade uniformly. The company could not fix uptime it could not see, could not reduce ticket volume driven by 326 unique environments, and could not lower cost to serve while every customer required bespoke attention.

The diagnosis they brought to the board in early 2024 was blunt: the customer-hosted model was not a product configuration problem; it was the root cause of nearly everything wrong with the business. The remedy was a rebuild of the product as a multi-tenant hosted service — one platform, operated by Tidewater, running all 340 customers, with the observability, uniform upgrade path, and operational leverage that only a single operated platform can deliver.

---

## Part Two: The Plan and Its Assumptions

### The Board Approval

In March 2024, the board approved an $8.5 million, 18-month program to rebuild the product as a multi-tenant hosted service and migrate the customer base onto it. The target completion date was September 2025. Chief Architect Miguel Arellano was named to lead the rebuild.

The business case was straightforward. The rebuild would attack every deteriorating metric at its root: a single operated platform would give Tidewater direct control over uptime, collapse 326 environments into one, drive down ticket volume, cut cost to serve, and remove the operational burden that was pushing customers out the door. It would also, not incidentally, convert Tidewater from a legacy software vendor into a modern hosted-services company — a repositioning with obvious implications for valuation, competitive posture, and the two at-risk enterprise renewals, whose retention alone would recover a meaningful share of the program's cost.

### The Architecture

Arellano's team designed the new platform around a multi-tenant core: shared infrastructure serving all customers, with logical isolation of each hospital's data and configuration. At the heart of the new system was a modern queueing layer — the component responsible for absorbing incoming clinical messages, buffering them through load spikes, and guaranteeing ordered, reliable delivery to downstream systems. The queueing layer was the single most consequential architectural choice in the design, because in interface middleware the queue is where reliability lives. Messages that cannot be delivered immediately must be held safely; messages that arrive in bursts must be absorbed without loss; and delivery order for clinical data is frequently not optional.

The new platform also included centralized monitoring and observability that the legacy model had made impossible, a uniform configuration model to replace years of per-customer customization, and a migration toolchain to move each customer's interface definitions, transformation logic, and message history from the old engine to the new service.

### The Assumptions That Would Be Tested

Every plan embeds assumptions, and Tidewater's embedded several that would prove costly.

**The migration would proceed in waves.** To hit the 18-month timeline across 340 customers, the plan called for moving hospitals in large batches — cohorts of 25 to 30 at a time — with each wave cut over during a coordinated window. Wave-based migration was the only arithmetic that fit the schedule: at one customer a week, 340 customers would take more than six years.

**Load testing would stand in for production reality.** The new queueing layer was tested against synthetic load profiles built from sampled production traffic. The tests passed. But the samples underweighted a crucial pattern in hospital data flows: the overnight batch. Hospitals do not send messages at a smooth rate. They send them in tidal surges — end-of-day lab batches, overnight billing runs, early-morning census reconciliation — and when 28 hospitals' overnight batches land on shared infrastructure in the same window, the aggregate spike bears little resemblance to any single customer's profile or to a synthetic average.

**Customers migrated in a wave could be validated after cutover.** The plan included pre-migration testing of each customer's interface configurations, but validation against live production traffic was expected to happen after the customer was live on the new platform, with the old engine held warm as a fallback.

**The schedule was the constraint to protect.** The program was managed, as most are, with the timeline as the governing commitment to the board. Pressure to hit the first major wave in November 2024 — eight months after approval — was real and felt throughout the organization.

None of these assumptions was unreasonable in isolation. Together, they created the conditions for what happened in November.

---

## Part Three: The First Wave — November 2024

### The Cutover

Through the spring and summer of 2024, the build proceeded roughly on plan. A small number of pilot customers — drawn largely from the 14 already-hosted accounts — moved to the new platform without major incident, which reinforced confidence in the architecture and the toolchain. The first true migration wave was scheduled for November 2024: 28 hospitals, cut over during a coordinated weekend window, with the legacy engines held available for rollback.

The cutover itself went smoothly. Interfaces came up, connectivity checks passed, daytime message traffic flowed. Through the first business day, dashboards were green.

The failure arrived at night.

### The Queue Backs Up

When the migrated hospitals' overnight batch loads hit the new platform — the end-of-day laboratory result batches, the billing extracts, the census reconciliations, all landing within a few overlapping hours — the new queueing layer could not absorb the aggregate spike. Twenty-eight hospitals' worth of overnight surges, arriving simultaneously on shared infrastructure, produced ingestion rates far beyond anything the synthetic load tests had modeled. The queue began to back up.

In interface middleware, a backed-up queue is not an abstract performance problem. Every queued message is a clinical event that has not yet reached its destination: a lab result not yet in a chart, an admission not yet reflected in the pharmacy system, a discharge not yet flowing to billing. And a queue that falls behind overnight faces the next morning's traffic before it has cleared the last night's — so the backlog compounds.

Over four days, the backlog grew to 1.2 million clinical messages. Tidewater's engineers worked continuously to expand throughput, re-shard queues, and prioritize the most clinically urgent message types, and hospitals fell back on manual processes — phone calls, faxes, direct system lookups — to work around delayed data. But each night's batch surge undid much of each day's recovery, and for four days the company's newest, most strategically important platform was visibly failing the customers it had just been asked to trust it.

### The Damage

By the time the backlog was cleared, the damage was extensive and measurable.

**Three hospitals reverted to the old engine.** The rollback capability worked as designed, which was small comfort: three customers who had been persuaded to move now had firsthand evidence that the new platform was not ready, and every one of them would need to be re-persuaded later.

**A 900-bed health system left for a competitor.** The largest and most consequential loss: a major system that had been among the wave, and whose experience of the backlog ended not in rollback but in departure. In enterprise health IT, a 900-bed system is a flagship account — the kind of reference customer that anchors a vendor's credibility with every other large prospect. Its departure was a revenue loss, a reference loss, and a gift to the competitor who received it.

**$1.1 million in service credits went out.** The contractual uptime and delivery commitments breached during the four-day incident triggered credits across the affected customer base — a direct, immediate hit of more than 2 percent of annual recurring revenue, incurred in a single week, on top of the program's budgeted costs.

**The intangible costs were larger.** News of a four-day message backlog travels fast in hospital IT circles, which are small and tightly networked. Every one of the roughly 300 customers not yet migrated now had a reason to resist their migration date. The two at-risk enterprise renewals — the accounts whose retention had helped justify the program — now had fresh evidence for their skepticism. And inside Tidewater, the teams that had spent eight months building the new platform had watched its debut become the worst operational incident in the company's history.

### The Stop

In December 2024, VP of Customer Success Danielle Oyelowo and Head of Support Tomasz Wieczorek forced a stop to all migrations.

The significance of who forced the stop is worth pausing on. It was not the CTO, not the chief architect, not the program office. It was the two leaders closest to customers — the executives absorbing the escalations, fielding the calls from hospital CIOs, and watching the support queue — who concluded that continuing the wave plan would destroy the customer base the program existed to save. Oyelowo and Wieczorek brought that conclusion to Venkataraman and Bergstrom not as a request but as a demand: no further migrations until the method changed.

To the credit of the executive team, the demand was honored. The migration calendar was frozen. The alternative — pressing forward to protect the September 2025 date — would have been the familiar failure mode of large programs, in which schedule commitments override field evidence until the damage becomes irreversible. Tidewater stopped instead.

---

## Part Four: The Changed Method

The pause lasted through the winter, and what emerged from it was not a revised schedule for the old approach but a different approach entirely. Four changes defined it.

### 1. Nine Migration Engineers

The company added nine dedicated migration engineers — a significant investment for a 210-person firm, and a recognition that migration was not a side activity to be absorbed by the platform team but a discipline of its own. The migration engineers owned the toolchain, the per-customer analysis of interface configurations and traffic patterns, the shadow-mode infrastructure, and the cutover runbooks. Their existence also meant that the platform engineers who had been split between building the new service and firefighting migrations could return to hardening the platform itself — including a rework of the queueing layer's capacity model, now informed by real aggregate overnight load rather than synthetic profiles.

### 2. Shadow Mode: Two Weeks Against Production

The most important change was the introduction of mandatory shadow-mode validation. Before any customer's cutover, their full production message traffic was mirrored to the new platform, which processed it in parallel with the legacy engine for two weeks — long enough to capture two full weekly cycles, including the overnight batches, the end-of-week surges, and the month-boundary billing runs that had ambushed the November wave.

Shadow mode transformed the risk profile of migration. Instead of discovering a customer's traffic anomalies after cutover, with clinical data on the line, Tidewater discovered them while the legacy engine still carried the real workload. Message-by-message comparison of the two systems' outputs surfaced transformation discrepancies, ordering issues, and throughput shortfalls in an environment where a failure cost nothing but engineering time. Every discrepancy found in shadow mode was an incident that never happened in production.

Shadow mode also gave the queueing layer something the original plan never had: continuous, cumulative exposure to real aggregate load. As more customers ran in shadow, the platform absorbed their combined overnight surges before it was ever responsible for them — a rolling, ever-growing stress test against genuine production traffic.

### 3. One Hospital at a Time

The wave model was abandoned. Migrations proceeded one hospital at a time, each with its own two-week shadow period, its own validation sign-off, its own cutover window, and its own rollback plan. The blast radius of any failure shrank from 28 hospitals to one. The migration engineers could give each customer's idiosyncrasies — and after thirteen years of customer-hosted deployment, every customer had idiosyncrasies — the individual attention the wave model had made impossible.

The obvious cost was throughput, and the shadow-mode requirement meant pipeline discipline mattered enormously: to sustain pace, multiple customers had to be moving through overlapping shadow periods at any given time, staged like aircraft on approach. This is precisely what the nine migration engineers made possible. Sequential cutover did not mean sequential preparation.

### 4. Honesty with the Board

The fourth change was a governance decision: Venkataraman and Bergstrom went to the board with a revised finish date of December 2025 — a three-month slip from the original plan — and a program that would ultimately cost well beyond the approved $8.5 million. They presented the November failure without varnish, the changed method with its cost and schedule implications, and the metrics by which the board could hold them accountable going forward.

The reset mattered because it aligned the program's official commitments with its operational reality. A program still nominally committed to September 2025 would have faced constant pressure to abandon shadow mode, re-batch customers, and compress validation — precisely the pressures that had produced November. By moving the date, leadership bought the new method the room it needed to work.

---

## Part Five: The Results — July 2025

By July 2025, seven months into the changed method, the numbers told a story of a program — and a business — transformed.

**Migration progress: 190 of 340 customers.** Fifty-six percent of the customer base was live on the new platform, migrated one at a time, each through a two-week shadow period, with no repeat of the November failure. From the December standstill, the migration engine had moved roughly 160 customers in about seven months — better than five customers a week at steady state — demonstrating that sequential cutover with a staged shadow pipeline could sustain real throughput. The remaining 150 customers put the December 2025 target within reach, demanding a comparable pace through the second half of the year.

**Uptime: 99.96 percent.** For the first time, the platform was operating above its 99.95 percent contractual commitment. The comparison with the 2023 baseline is stark: 99.1 percent uptime meant roughly 79 hours of annual downtime; 99.96 percent means roughly 3.5 hours. The company that had spent years apologizing for its reliability was now exceeding the standard its contracts promised — and doing so on the platform that, eight months earlier, had suffered a four-day backlog on its debut. The reworked queueing layer, hardened against real aggregate overnight load through hundreds of shadow-mode weeks, was carrying more than half the customer base without breaching its commitments.

**Support tickets: 1,700 a month, down from 4,100.** A 59 percent reduction in monthly ticket volume, achieved while the migrated base grew — and achieved for exactly the reasons the original business case predicted. One operated platform replaced hundreds of unique environments. Central observability let Tidewater see and fix problems before customers filed tickets about them. Uniform configuration eliminated whole categories of environment-specific failure. The support organization that had been a treadmill was becoming a function with capacity to spare.

**Churn: 6 percent, down from 14 percent.** The most strategically important number in the set. Churn falling by more than half meant the customer exodus that had threatened the business was ending. On a 340-customer base, the difference between 14 percent and 6 percent churn is roughly 27 customers a year — approximately $3.6 million in recurring revenue retained annually at the average contract value, every year, compounding. Customers were staying because the operational experience of being a Tidewater customer had fundamentally changed: fewer outages, fewer tickets, no hosting burden, and a vendor that had visibly recovered from a public failure with discipline rather than denial.

**Cost to serve: $6,900 per customer per year, down from $11,400.** A 39 percent reduction in unit service cost. Applied across the full base once migration completes, the difference of $4,500 per customer represents roughly $1.5 million a year in structural cost savings — before accounting for the operating leverage of a support organization handling 59 percent fewer tickets and an engineering organization freed from environment-specific firefighting.

**Spend: $12.3 million against an $8.5 million budget.** The honest entry in the ledger. The program was 45 percent over its original budget, with the November failure's direct costs ($1.1 million in credits, the lost 900-bed system, the recovery effort), the nine migration engineers, the shadow-mode infrastructure, and the extended timeline all contributing. The overrun was real, and it belongs in any honest accounting of the program. But the return arithmetic had become compelling: churn reduction alone was retaining revenue at a rate of roughly $3.6 million a year, cost-to-serve improvements were tracking toward $1.5 million a year at full migration, service-credit exposure had collapsed with uptime now above commitment, and the company had converted itself into a multi-tenant hosted-services business with the retention profile and unit economics to match. Measured against the trajectory the business was on in 2023 — 14 percent churn compounding against a $46 million revenue base — the $12.3 million was buying survival, not merely improvement.

---

## Part Six: What Tidewater Would Do Differently

With the benefit of hindsight, the company's leadership identified several things they would change if they could run the program again — and each generalizes beyond Tidewater.

**Shadow mode from day one, not as a corrective.** The single most valuable element of the recovered program — two weeks of parallel processing against real production traffic before every cutover — was available from the beginning. It was omitted from the original plan not because anyone argued against it but because the wave-based schedule left no room for it. Had the November wave's 28 hospitals each run in shadow mode first, the queueing layer's inability to absorb aggregate overnight batch load would have been discovered on mirrored traffic, at zero customer cost, weeks before any cutover. The $1.1 million in credits, the three rollbacks, and quite possibly the 900-bed departure were the price of learning in production what shadow mode would have taught for free.

**Load-test the aggregate, not the average.** The synthetic load tests validated the platform against sampled traffic profiles and passed. The failure came from the pattern the samples underweighted: correlated overnight surges across many customers simultaneously. In any multi-tenant migration, the dangerous load is not any single customer's peak but the coincidence of every customer's peak — and hospital batch schedules, like most institutional batch schedules, are correlated by design, clustered around end of day, end of shift, end of month. Capacity models built on averaged or sampled profiles will systematically miss this.

**Size the first real wave for learning, not for schedule.** Twenty-eight hospitals was the wrong number for a first wave — large enough to produce a catastrophic aggregate load, large enough that failure damaged a meaningful fraction of the customer base, and chosen because the 18-month timeline demanded it rather than because the platform's readiness supported it. The pilot migrations that preceded it, drawn largely from already-hosted customers, had been too easy to be informative. A first wave should be sized to surface problems at survivable scale.

**Staff migration as a discipline before the first cutover.** The nine migration engineers hired after the failure should have been in place before it. Treating migration as an activity the platform team absorbs alongside its build work guarantees that both suffer — and it was only when migration got dedicated ownership that the toolchain, the per-customer analysis, and the shadow pipeline matured into a repeatable process.

**Let the customer-facing organization set the pace — structurally, not heroically.** The December stop was the program's turning point, and it happened because Oyelowo and Wieczorek forced it. That it required forcing is the lesson. The people closest to customers had the clearest early read on the November failure's real cost, but the program's governance gave them no formal brake to pull. Tidewater's leadership would build that brake into the structure from the start: explicit customer-health criteria that pause migration automatically, owned by customer success and support, rather than depending on two executives being willing to stand in front of a moving program.

**Set the schedule the method can honor.** The original 18-month timeline was reverse-engineered from a board commitment, and the wave-based method was reverse-engineered from the timeline. When the method failed, the honest reset — December 2025, more money, a slower and safer approach — restored the alignment between promise and practice, and the program's best months followed. The company would start there next time: derive the schedule from a validated migration method, not the method from a desired schedule.

---

## Part Seven: Lessons for the Reader

For an executive or technical leader contemplating a similar modernization — a legacy, customer-hosted, or single-tenant product that must become an operated, multi-tenant service — Tidewater's experience distills into a set of transferable lessons.

**1. The customer-hosted model fails as a system, and the metrics degrade together.** Tidewater's 99.1 percent uptime, 4,100 monthly tickets, $11,400 cost to serve, and 14 percent churn were not four problems; they were four symptoms of one architecture. This is diagnostic in both directions: if your fragmented deployment model is producing this constellation of symptoms, incremental fixes will not reverse them — and conversely, a genuine platform consolidation should improve all of them together, as Tidewater's did.

**2. Migration is the product, for as long as it lasts.** Companies undertaking rebuilds naturally focus their best thinking on the new platform's architecture. But for the twelve to twenty-four months of transition, the migration is what customers actually experience. Tidewater's new platform was, ultimately, sound; its migration method was not, and customers judged the company on the method. Staff migration as a first-class discipline, invest in its tooling, and design its process with the same rigor as the platform itself.

**3. Validate against reality before you depend on it.** Shadow mode — running real production traffic through the new system in parallel before cutover — is the single highest-leverage risk control in this class of program. It converts production surprises into pre-production findings at the cost of some infrastructure and some calendar time. Tidewater's arithmetic is instructive: the November failure cost $1.1 million in credits, one flagship customer, and months of trust; two weeks of shadow per customer cost engineering time. Pay the cheap price.

**4. Aggregate load is a different phenomenon from individual load.** In any consolidation onto shared infrastructure, model the correlated worst case — every tenant's batch window landing together — not the sampled average. Institutional workloads cluster by design. If your load tests do not reproduce that clustering, they are testing a system that will never exist.

**5. Blast radius is a choice.** Wave size is a dial between speed and risk, and the right setting changes over the life of a program. Tidewater's error was setting the dial to 28 before the platform had ever carried real aggregate load; its recovery set the dial to one and rebuilt throughput through pipeline parallelism instead of batch size. Earn larger batches with demonstrated capacity; never assume them from the schedule.

**6. Give the customer-facing organization real authority — and listen when it uses it.** The most consequential decision in this case was the December stop, forced by the VP of Customer Success and the Head of Support against the momentum of a board-committed schedule. Programs need that circuit breaker, and it works best when it is designed in: explicit stop criteria, owned by the people who hear customers first, honored by executives when triggered. Tidewater's leadership deserves credit for honoring it; better leadership design would not have required the confrontation.

**7. A candid reset beats a defended fiction.** Moving the finish date to December 2025 and acknowledging the overrun cost Venkataraman and Bergstrom a difficult board conversation. It bought the program the room to run its new method without schedule pressure eroding it — and the seven months that followed the reset were the most productive in the program's history. Boards can absorb a revised plan supported by evidence far better than they can absorb a second November.

**8. Judge the program against the counterfactual, not the budget line.** Tidewater spent $12.3 million against an $8.5 million plan, lost a 900-bed flagship customer, and paid $1.1 million in credits. It also cut churn from 14 percent to 6 percent — retaining roughly $3.6 million in annual recurring revenue — cut cost to serve by 39 percent, cut ticket volume by 59 percent, and exceeded its uptime commitment for the first time. The relevant comparison is not the program as executed versus the program as planned; it is the program as executed versus the business's 2023 trajectory, on which 14 percent annual churn was steadily consuming a $46 million revenue base. By that comparison, the rebuild — failure, overrun, and all — was among the best investments the company ever made. The tragedy of November 2024 is not that it made the program a failure; it is that most of its cost was avoidable with methods the company already knew and eventually adopted.

The final lesson is the simplest: Tidewater got the strategy right and the initial execution wrong, and it recovered because it was willing to stop, change its method, and tell the truth about the schedule. Many programs get the strategy right. Fewer survive their first serious failure. The ones that do share Tidewater's distinguishing trait — they treat the failure as information, not as something to be pushed through — and their recoveries, like Tidewater's, tend to be built on the disciplines the original plan skipped in the name of speed.

---

*Case prepared from company records and interviews with Tidewater Health Interfaces leadership, covering the period from year-end 2023 through July 2025. Figures for the second half of 2025, including completion of the remaining 150 customer migrations against the December 2025 target, were not yet available at the time of writing.*
