# Tidewater Health Interfaces: Rebuilding Clinical Middleware Under Load

## A Case Study in Platform Migration, Failure, and Recovery

---

## Introduction

Tidewater Health Interfaces sells clinical integration middleware — the software layer that lets a hospital's lab system talk to its pharmacy system, its pharmacy system talk to its billing system, and all of it talk to the electronic health record without a human re-typing anything in between. It is not a glamorous category of software, but it is one that cannot fail quietly. When an interface engine drops a message, a lab result does not arrive, a medication order does not fire, and somewhere in a hospital a nurse is waiting on information that never comes.

By the end of 2023, Tidewater served 340 hospitals from its headquarters in Durham, North Carolina, with 210 employees and $46 million in annual recurring revenue. The company was profitable, well regarded in the clinical integration niche, and sitting on a piece of software that had not been substantially re-architected since 2011. This case study follows what happened when Tidewater's leadership decided that software needed to change — the plan they built, the wave of migrations that nearly broke the company in the way it broke customers' trust, the reset that followed, and the results that came from doing the work over again, more slowly, in a different order.

The value of the story is less in the rebuild itself, which is a common enough exercise in enterprise software, than in the gap between what the board approved in March 2024 and what the company actually had to do to get to a working multi-tenant platform. That gap is where the lessons live.

---

## Part One: The State of the Platform and the Business That Forced the Rebuild

### An engine built for a different era

The core of Tidewater's product was an interface engine — code that parsed, transformed, validated, and routed HL7 messages between clinical systems. The engine had been written in 2011, when the company's entire customer base ran it as software installed on servers the hospitals themselves owned and operated. That customer-hosted model made sense in 2011, when hospital IT departments still assumed they would run everything behind their own firewall, and it had persisted largely unchanged for over a decade because it worked well enough and because nobody wanted to touch code that hospitals depended on for medication orders and lab results.

By 2023, the market had moved. Hospital IT departments were shrinking, not growing. CIOs wanted vendors to host and operate the software, not hand them a server to patch and monitor. Tidewater had built a hosted version of its engine as a side project starting around 2019, but adoption had been slow — by the end of 2023, only 14 of the company's 340 customers had migrated to it. The other 326 were still running the 2011 engine on premises, with all the operational fragility that implied: version drift between customer environments, patches that had to be scheduled around hospital change-control windows, and a support organization that spent much of its time diagnosing problems that were specific to one hospital's particular configuration rather than problems in the product itself.

### The commitments the company could not keep

Tidewater's standard hospital contract carried a 99.95 percent uptime service level commitment. Through 2023, actual uptime across the customer base averaged 99.1 percent — a gap that sounds small until it is converted into hours. A service commitment of 99.95 percent allows for roughly 4.4 hours of downtime a year; a delivered average of 99.1 percent works out to nearly 79 hours, the better part of three and a half days spread across the year in outages, degraded performance windows, and interface failures that had to be manually restarted.

The support organization absorbed the consequence of that gap. Tomasz Wieczorek's team fielded 4,100 tickets a month across the customer base — roughly twelve tickets per customer per month, an unusually high volume for a mature product that had, in theory, been stable for over a decade. Many of the tickets were not novel problems; they were the same handful of failure modes recurring across different hospitals running slightly different versions of the on-premises engine, each requiring its own diagnosis because no two customer environments were quite identical.

The commercial consequence showed up in the churn number. Annual churn had reached 14 percent by the end of 2023 — high for a business where switching interface engines is disruptive and expensive for a hospital, which should in theory make the product sticky. Hospitals do not change clinical integration vendors lightly; a 14 percent churn rate in that category is a sign that customers were being pushed out by reliability problems rather than pulled away by a better competing product.

Two renewals worth $5.2 million combined were flagged as at risk heading into 2024. Both were large integrated delivery networks that had experienced repeated interface outages over the preceding eighteen months and had begun formal evaluations of competing platforms. Losing either one would have been the single largest customer loss in company history; losing both would have erased more than 11 percent of recurring revenue in one renewal cycle and signaled to the rest of the customer base that Tidewater's reliability problems were structural rather than incidental.

### The case for a full rebuild rather than a repair

CEO Prabha Venkataraman and CTO Nils Bergstrom had debated for over a year whether the answer was to keep patching the 2011 engine or to replace it outright with a true multi-tenant hosted service — one platform, one codebase, one operational environment serving all 340 hospitals rather than 326 separate on-premises installations plus a lightly adopted hosted variant. Patching had an obvious appeal: it was cheaper, it did not require migrating a single existing customer, and it avoided the risk of touching a system that, whatever its flaws, was currently moving clinical messages for 340 hospitals without a catastrophic failure.

But Bergstrom's engineering organization had concluded that the 2011 engine's architecture — a single-threaded message processing core with configuration and routing logic entangled directly in the parsing code — could not be incrementally improved into something that met a 99.95 percent commitment at scale. Every fix required for one customer's configuration risked breaking another's. The team had, in effect, been maintaining 326 forks of the same product for years, and the support ticket volume was the direct cost of that fragmentation. Venkataraman took the position to the board that a full rebuild, painful as it would be, was cheaper over five years than continuing to run the fragmented estate, and that the two at-risk renewals gave the company a hard deadline to prove the new platform could hold enterprise-scale hospital systems reliably.

The board approved an $8.5 million, 18-month rebuild in March 2024. Chief Architect Miguel Arellano was given responsibility for the technical build; the mandate was to design and ship a true multi-tenant hosted service, migrate all 340 hospitals onto it, and retire the 2011 engine, with a target completion date in the fourth quarter of 2025.

---

## Part Two: The Plan and Its Assumptions

### What the $8.5 million was supposed to buy

The plan Arellano brought to the board assumed a phased build-and-migrate approach. Engineering would spend roughly the first six months — through September 2024 — building out the multi-tenant service on top of the existing hosted engine's foundation, adding tenant isolation, a new queueing and message-routing layer intended to replace the point-to-point connections the 2011 engine relied on, and a self-service onboarding flow that would let the 14 already-hosted customers move onto the new architecture with minimal manual work.

From there, the plan called for migration in waves of roughly 25 to 30 hospitals every six to eight weeks, sequenced from the company's smaller and less complex customers toward its largest and most message-intensive ones, with the two at-risk enterprise renewals scheduled for migration toward the end of the program once the platform had proven itself on lower-stakes customers. At that pace, all 340 hospitals would be migrated by the end of 2025, comfortably inside the board's 18-month window with several months of buffer.

### The assumptions baked into the timeline

Three assumptions carried the plan, and each one turned out to be wrong in a way that would not become visible until the first wave was already underway.

The first assumption was that message volume during migration would resemble message volume observed during ordinary operation. The team had load-tested the new queueing layer against production traffic samples pulled from typical weekday operating hours. What those samples did not capture well was the shape of overnight batch traffic — the large, concentrated bursts of lab results, billing feeds, and reconciliation messages that hospital systems push through in scheduled batch jobs between roughly 11 p.m. and 5 a.m., precisely the window when a hospital's live clinical traffic is lightest and therefore the traditional migration cutover window of choice.

The second assumption was that a hospital's production behavior could be adequately validated through a combination of pre-migration configuration review and a short parallel-run period before cutover — in practice, a few days of the new engine processing a copy of live traffic before the migration team flipped the hospital over for real. Arellano's team believed this was sufficient because the 14 existing hosted customers had been onboarded with a similar process without major incident. What the plan did not account for was that those 14 customers had, collectively, agreed to move onto the hosted platform specifically because they were smaller, simpler integration profiles to begin with — they were not a representative sample of the customer base's complexity, and validating against them said little about how the new queueing layer would behave under a 500-bed hospital's full nightly batch load.

The third assumption was speed of batching migrations: that moving 25 to 30 hospitals at once in a single wave was operationally efficient and that any problems that arose could be resolved for the whole cohort at once, the same way a single fix to the 2011 engine's shared codebase used to (in theory, if not always in practice) fix a problem for every customer running it. This assumption reversed the actual lesson of the fragmented estate — that batching customers together concentrates risk rather than diversifying it, especially when the underlying infrastructure has not yet been proven at the concurrency level that a 28-hospital simultaneous cutover implies.

None of these assumptions were tested to failure before the first wave, because there was no non-production environment at Tidewater that could simulate 28 hospitals' overnight batch traffic hitting the new queueing layer concurrently. The team had unit-tested and load-tested components; it had not stress-tested the full multi-tenant system under a realistic migration-day traffic profile, because building such an environment was itself expensive and the schedule did not have slack for it.

---

## Part Three: The First Wave and What It Cost

### November 2024: 28 hospitals move at once

The first migration wave went live in November 2024, moving 28 hospitals onto the new multi-tenant hosted platform in a single coordinated cutover, consistent with the plan's batching approach. For the first several hours after cutover, the platform appeared to hold. Message volumes during the daytime and evening hours were within the ranges the team had modeled.

The trouble began overnight. As each hospital's batch systems began pushing their scheduled nightly loads — lab result reconciliations, pharmacy formulary updates, billing extracts — the new queueing layer, which had never before been asked to absorb 28 hospitals' concurrent overnight batch traffic against a shared multi-tenant infrastructure, began to fall behind. Queue depth grew faster than the consumers processing it could drain, and within the first night the backlog had already reached a size that could not be cleared during the following day's lower-volume window before the next night's batch load added to it again.

Over four days, the backlog compounded. By the time the engineering team had fully diagnosed the bottleneck — a combination of undersized consumer concurrency limits and a message-acknowledgment pattern that held connections open longer than intended under sustained load — 1.2 million clinical messages had backed up in the queue across the 28 hospitals. Some of those messages were lab results delayed by hours; some were pharmacy orders that arrived out of sequence relative to other clinical events; all of them represented information that a hospital's clinical or administrative staff needed and did not have when they expected it.

### The customer and financial cost

The consequences arrived quickly. Three of the 28 hospitals in the wave made the decision to revert to the old 2011 on-premises engine rather than continue to absorb delayed messages, a process that itself required emergency support engagement to execute safely, since the reversion path had not been built or tested as thoroughly as the forward migration path. One customer — a 900-bed hospital system, among the largest in the wave and one of the more message-intensive environments in the entire customer base — used the incident to terminate its contract and move to a competing interface engine vendor, a loss that validated exactly the risk the two at-risk enterprise renewals represented, though this particular hospital had not been one of the two flagged accounts.

Tidewater issued $1.1 million in service credits to affected customers in the wave, a direct and immediate financial cost layered on top of the $8.5 million rebuild budget, and a cost that did not include the harder-to-quantify effect on the company's reputation among the 312 hospitals still waiting to be migrated, many of whom heard about the November incident from peers in hospital IT networks before Tidewater's own account teams could get ahead of the narrative.

### The internal reckoning

VP of Customer Success Danielle Oyelowo and Head of Support Tomasz Wieczorek, whose teams were absorbing the operational and relationship fallout of the incident in real time, pushed for and won a full stop to the migration program in December 2024. This was, by account of people involved, not a straightforward internal decision — Arellano's engineering organization believed the specific queueing bottleneck was identifiable and fixable within weeks, and there was pressure to resume the wave cadence quickly given the board's 18-month clock. Oyelowo and Wieczorek argued, successfully, that the problem was not only the specific technical bottleneck but the migration method itself: batching large numbers of hospitals into single cutovers without a validated way to observe how the new platform behaved under each customer's real production load before that customer's clinical operations depended on it.

The stop held. December 2024 became a month of diagnosis and redesign rather than migration.

---

## Part Four: The Changed Method

### What the post-mortem found

The internal review that followed the December stop identified two compounding failures rather than one. The technical failure was real and specific: the queueing layer's consumer concurrency had been sized against modeled traffic that underestimated the concentration of overnight batch volume when many hospitals' batch windows overlapped on shared infrastructure. But the review also concluded that the technical failure would have been caught before it reached production customers if the migration method had included a way to observe each hospital's actual traffic pattern against the new platform before that hospital's clinical operations depended on the result — and that no amount of additional load testing in a synthetic environment would have been as reliable as watching real traffic in parallel.

The review further concluded that batching 28 hospitals into one cutover event had converted what should have been an isolated, containable problem into a wide-reaching incident, because there was no way to pause or roll back a subset of the cohort without affecting the group, and because the support organization had been sized to handle a normal ticket volume rather than a simultaneous multi-hospital incident.

### The rebuilt approach

Tidewater made three changes to the migration method following the December stop, each aimed directly at one part of the failure.

First, the company added nine migration engineers to the program, roughly doubling the size of the team dedicated specifically to migration execution as distinct from the core platform engineering team building the multi-tenant service itself. The added headcount was allocated primarily to building and operating a shadow-mode validation capability rather than to increasing the pace of cutovers.

Second, every customer scheduled for migration was run in shadow mode against the production platform for two full weeks before cutover — meaning the new platform received a live copy of the hospital's actual traffic, processed it in parallel with the old engine still serving as the system of record, and the migration team compared outputs and monitored queue and processing behavior under that hospital's real load pattern, including its actual overnight batch volume, before any cutover decision was made. This directly addressed the gap in the original plan, where validation had relied on configuration review and short parallel runs rather than sustained observation of real production behavior.

Third, the company abandoned wave-based batching in favor of moving one hospital at a time. Each cutover became an individually planned event, sequenced so that any problem discovered with one hospital's migration could be diagnosed and resolved without any other hospital's migration being affected, and so that the support organization could dedicate focused attention to each cutover rather than splitting attention across two or three dozen simultaneous events.

### The cost of the reset in time

The combined effect of these changes was to slow the pace of migration substantially in exchange for containing risk. Where the original plan had called for waves of 25 to 30 hospitals every six to eight weeks, the revised method moved hospitals individually, each preceded by two weeks of shadow-mode validation. Leadership told the board in early 2025 that the program's completion date, originally intended to land within the 18-month window approved in March 2024, was now pushed to December 2025 — an extension of roughly several months beyond the original target, driven by the four-day incident, the December stop, and the slower per-hospital cadence of the new method, though still within a timeframe the board judged acceptable given what the alternative — resuming the batched approach and risking a repeat incident — would have cost in both money and customer trust.

---

## Part Five: Results

### Where things stood by July 2025

By July 2025, seven months into the revised, one-hospital-at-a-time method, 190 of the 340 hospitals had been migrated onto the multi-tenant hosted platform — roughly 56 percent of the customer base, moved without a repeat of the November 2024 incident. The remaining 150 hospitals, including the two at-risk enterprise accounts whose $5.2 million in combined renewals had been the original trigger for the rebuild, were still being sequenced through the shadow-mode validation and individual cutover process, with the board's December 2025 target still in view.

The operational numbers had moved substantially in the right direction across the customer base as a whole. Uptime, which had averaged 99.1 percent through 2023 against a 99.95 percent commitment, stood at 99.96 percent by July 2025 — a figure that, for the first time in the company's recent history, exceeded the contractual commitment rather than falling short of it. Support ticket volume had fallen from 4,100 a month to 1,700 a month, a reduction of roughly 59 percent, reflecting both the smaller footprint of the fragmented on-premises estate as more customers moved to the unified hosted platform and the reliability improvements the new architecture delivered for hospitals still on the old engine as the support organization's attention concentrated. Annual churn had fallen from 14 percent to 6 percent, a decline that tracked closely with the uptime recovery and suggested that the reliability problems, not competitive product pressure, had indeed been the primary driver of the churn Tidewater experienced through 2023.

The cost-to-serve metric, watched closely internally as the economic justification for the entire rebuild, had fallen from $11,400 per customer per year to $6,900 — a reduction of roughly 40 percent, driven by the elimination of per-customer on-premises configuration management and the consolidation of support effort onto a single platform rather than 326 separate installations.

### The cost of getting there

Cumulative spend on the rebuild program stood at $12.3 million by July 2025, against the $8.5 million the board had approved in March 2024 — an overrun of $3.8 million, or roughly 45 percent above the original budget. That overrun reflected the combined cost of the additional nine migration engineers hired after the December 2024 stop, the $1.1 million in service credits issued after the November incident, the extended timeline that kept the migration team and supporting infrastructure running for longer than originally planned, and the general cost of building the shadow-mode validation capability that had not been part of the original plan's scope.

Set against that overrun, the reduction in cost to serve — from $11,400 to $6,900 per customer per year, applied across a customer base of 340 hospitals — represented an annualized savings run-rate of roughly $1.5 million once fully realized across the whole customer base, a figure that would recur every year going forward rather than being a one-time cost, and one that made the program's economics net positive over a multi-year horizon even accounting for the overrun, provided the remaining 150 hospitals migrated without another incident of the scale seen in November 2024.

---

## Part Six: What the Company Would Do Differently

### On the plan itself

Looking back, Tidewater's leadership concluded that the original plan's central error was not the decision to rebuild — the case for replacing a fragmented, decade-old engine with a true multi-tenant platform held up under scrutiny even after the November incident, and the results by July 2025 supported it. The error was in how migration risk was modeled and sequenced. The plan had tested the new platform's components without testing the platform under the specific, concentrated traffic pattern that a real migration cutover — and in particular a batched cutover of two or three dozen hospitals at once — would actually produce. Load testing against typical operating hours told the team little about behavior at 2 a.m. when two dozen hospitals' batch jobs overlapped for the first time on shared infrastructure.

A reader building a similar migration plan should treat the traffic profile of the migration event itself — not just the steady-state traffic the new system will carry once migration is complete — as a distinct thing to model and test. The overnight batch load that broke the queueing layer in November 2024 was not unusual or hidden; it was well understood by anyone who had worked with hospital batch interfaces before. It simply had not been tested in the specific combination — multiple hospitals, concurrently, on shared new infrastructure — that the actual cutover produced.

### On validation before cutover

The shift to two weeks of shadow-mode validation, in which the new platform processed live production traffic in parallel with the old engine before any hospital's operations depended on the result, was the single change most credited internally with the program's recovery. It replaced a validation approach built on configuration review and short parallel runs — sufficient for the 14 early hosted customers, whose integration profiles were comparatively simple, but not sufficient for the full range of complexity across 340 hospitals — with direct observation of real behavior under real load before risk was transferred to the customer.

The broader lesson for a reader evaluating a similar cutover is that validating against a non-representative early-adopter cohort can create false confidence. Tidewater's original plan pointed to the 14 hosted customers as evidence that the validation approach worked; those customers had self-selected for simplicity, and their smooth onboarding said little about how the platform would handle the message volume and configuration complexity of a 500-bed hospital system's overnight batch load. Shadow-mode validation against each specific customer's actual traffic, sustained over a period long enough to observe the customer's real operating cycle — not just a sample of daytime hours — closed that gap.

### On batching versus sequencing

The decision to abandon wave-based batching in favor of one hospital at a time was the second major change, and it came at a direct cost to the schedule: moving hospitals individually is slower than moving them in groups of 25 to 30, and the extension of the completion date from the original 18-month target to December 2025 was substantially attributable to this change. Leadership concluded the trade was worth it. Batching had been justified originally on the theory that problems could be fixed once for an entire cohort, mirroring how a shared codebase fix used to help every customer on the 2011 engine at once. What batching actually did in November 2024 was ensure that a single undersized queueing parameter affected 28 hospitals simultaneously rather than one, converting a containable engineering problem into a customer-facing incident involving service credits, contract terminations, and a program-wide stop.

A reader planning a migration of any comparable scale should weigh the efficiency of batching against the blast radius of batching, and should recognize that these work in opposite directions: batching a technical fix across many customers at once is efficient when the fix is known to work, but batching an unproven system across many customers at once multiplies the cost of an unknown failure by the size of the batch. Tidewater's experience argues for erring toward smaller cutover units, particularly in the early period of a new platform's life, and expanding batch size only once the platform has demonstrated it can absorb a representative range of customer traffic patterns without incident.

### On organizational friction as an early warning signal

The internal disagreement between the customer-facing organization — Oyelowo and Wieczorek — and the engineering organization building the platform, over whether to stop the program in December 2024, is worth noting as its own lesson. The engineering view, that the specific bottleneck was fixable quickly and the wave cadence should resume, was not unreasonable on its own technical merits. But it was the customer-facing organization, closer to the hospitals absorbing delayed lab results and reverted engines, that recognized the failure was systemic to the method rather than confined to one fixable parameter. A reader in a similar position should treat sustained disagreement between the team measuring customer impact and the team measuring technical progress as a signal worth resolving carefully rather than a disagreement to be settled quickly in favor of the schedule, since the team closer to the customer consequence identified the deeper problem in this case.

### On budget and timeline discipline

Finally, the $3.8 million overrun and the schedule extension were not treated internally as failures of the original decision to rebuild, but they were treated as evidence that the original plan had underpriced the cost of getting migration risk right. The board's willingness to fund the additional nine engineers, absorb the $1.1 million in service credits, and accept a later completion date rather than resume the original batched cadence was, in retrospect, the decision that allowed the program to reach 190 of 340 hospitals migrated with uptime above commitment and churn cut by more than half. A reader facing a similar choice — between resuming an aggressive schedule after a failure or accepting a slower, more expensive path with better validation — should weigh the recovery Tidewater achieved by July 2025 against the alternative cost of a second incident on the scale of November 2024, particularly given that the two enterprise renewals worth $5.2 million that had originally triggered the rebuild were still in the migration queue as of that date, with the company's credibility on reliability now rebuilt but still being tested one hospital at a time.

---

## Conclusion

Tidewater Health Interfaces set out in March 2024 to replace a decade-old, fragmented interface engine with a modern multi-tenant hosted platform, under board-approved funding of $8.5 million and an 18-month timeline, driven by a service level shortfall, a support burden of over 4,000 tickets a month, 14 percent annual churn, and $5.2 million in enterprise renewals at risk. The first attempt at migration, moving 28 hospitals at once in November 2024, exposed an assumption the plan had never tested — that the new queueing layer could absorb concentrated overnight batch traffic from many hospitals simultaneously — and the failure of that assumption cost the company $1.1 million in service credits, three reverted migrations, and one significant customer departure, forcing a full program stop in December 2024.

What followed was not a change in the underlying decision to rebuild, but a change in method: more people dedicated specifically to migration validation, two weeks of shadow-mode observation against real production traffic before every cutover, and a shift from batched waves to one hospital at a time. By July 2025, that changed method had moved 190 of 340 hospitals onto the new platform, lifted uptime from 99.1 to 99.96 percent, cut support tickets from 4,100 to 1,700 a month, brought churn down from 14 to 6 percent, and reduced cost to serve per customer by 40 percent — results achieved at a cumulative cost of $12.3 million against the original $8.5 million budget, with 150 hospitals, including the two originally at-risk enterprise accounts, still to be migrated toward a revised completion target of December 2025.

The case for a reader in a comparable position is not that the rebuild was a mistake, or that the board's original budget and timeline were unreasonable given what was known in March 2024. It is that the risk in a migration of this kind concentrates in the cutover event itself — in the traffic pattern a batched, poorly validated cutover produces — far more than in the steady-state design of the new system, and that the fix, once the company found it, was not more engineering horsepower thrown at the same batched method, but a slower, more carefully sequenced method that traded speed for the ability to observe real behavior before real consequences followed.
