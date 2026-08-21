# The Two-Hour Promise: How Blue Ridge Hardware and Supply Rebuilt Its Inventory Foundation Before It Could Sell Online

## A Case Study in Retail Technology, Operational Discipline, and the Cost of Skipping Steps

---

## I. The Company and Its Situation

Blue Ridge Hardware and Supply is, by most measures, a successful regional retailer of the kind that dots the American landscape but rarely draws attention beyond its own trade area. Headquartered in Knoxville, Tennessee, the company operates 38 stores spread across eastern Tennessee and southwest Virginia — a footprint that runs roughly from Chattanooga up the Interstate 81 corridor through Bristol, Abingdon, and into the coalfield counties of Virginia. The stores range from 14,000 to 40,000 square feet, sell hardware, building materials, farm and ranch supplies, paint, plumbing, and seasonal goods, and employ about 1,900 people. Annual revenue in 2022 stood at $310 million.

The company's identity had been built over decades on two propositions: proximity and knowledge. In the small cities and rural counties Blue Ridge serves, the nearest big-box home improvement store might be forty minutes away, and the Blue Ridge associate behind the counter had often worked in the trades or on a farm before working in the store. Contractors, farmers, and serious do-it-yourselfers were the core customer base, and for many of them a trip to Blue Ridge was a routine part of the working week.

By late 2022, however, the numbers told a story that the company's culture had been slow to acknowledge. Comparable store sales — the standard retail measure of revenue growth at stores open more than a year — had declined for six consecutive quarters, averaging minus 4.2 percent. That is not a collapse; it is an erosion. But six quarters of erosion in a business with thin retail margins is the kind of trend that, left unaddressed, turns a healthy regional chain into a distressed one within three to five years.

The causes were partly external. The big-box chains had continued to press into secondary markets, and more importantly, they had built digital capabilities that changed customer expectations everywhere, including in rural Appalachia. A contractor in Kingsport could open an app, confirm that a specific ball valve was in stock at a store twenty miles away, order it, and have it waiting at a pickup counter when he arrived. At Blue Ridge, the same contractor had to call the store and hope the person who answered could physically walk to the shelf and check — because the system could not be trusted to know.

That last point was the internal cause, and it was the more serious one. Blue Ridge's inventory management ran on a system installed in 2007 and heavily customized since. Two internal audits in 2022 established that **inventory record accuracy — the percentage of SKU-store combinations where the system's on-hand count matched the physical shelf — stood at 71 percent**. Put differently, for nearly three of every ten items in every store, the computer was wrong about how many were on the shelf.

The consequences cascaded. Automated replenishment ordered against phantom inventory, so shelves went empty while the system believed them full. The company's own analysis found that **its top 200 items — the fast-moving core of the assortment, the items contractors came in for — were out of stock 18 percent of the time**. A contractor who makes two trips and twice fails to find PVC cement or a common breaker does not make a third trip. He drives the forty minutes to the big box, and while he is there, he buys everything else too. Store managers understood this viscerally; several had quietly begun over-ordering key items and stashing safety stock in back rooms, which further corrupted the system's records and made the underlying problem worse.

This was the situation confronting Chief Executive Officer Loretta Ashby-Ng, who had run the company since 2018, and Chief Information Officer Ellis Trumbo, hired in 2021 with a mandate to modernize. Both understood that the sales decline and the inventory problem were the same problem wearing two coats.

---

## II. The Bet: Why Blue Ridge Chose This Program

Through the fall of 2022, Ashby-Ng and Trumbo developed and debated the response. Three strategic options were on the table.

The first was defensive cost management: accept the sales decline, close the four or five weakest stores, cut labor, and manage for cash. The board gave this option a serious hearing — it was the lowest-risk path in the short term — but Ashby-Ng argued it amounted to a managed liquidation. Once a regional retailer starts closing stores and cutting service, the trust that sustains the remaining stores erodes, and the decline accelerates.

The second was a pure remediation program: fix the inventory system, but stop there. Replace the 2007-era platform, clean up the data, restore in-stock rates, and let the improved customer experience win back sales. This was defensible, and in hindsight several members of the leadership team would argue it was where the company should have started and stayed for at least a year.

The third option — the one chosen — combined remediation with offense. Replace the inventory system *and* simultaneously launch a buy-online-pickup-in-store (BOPIS) capability, so that Blue Ridge would not merely catch up to customer expectations but meet them head-on. The reasoning was straightforward and, on paper, compelling: the new inventory system was a prerequisite for BOPIS anyway, since you cannot sell online inventory you cannot see accurately. Doing both at once meant one vendor selection, one integration effort, one change management push, and a revenue-generating capability at the end rather than just a cleaner back office. The pickup model also played to Blue Ridge's strengths — its customers wanted their goods now, not in two days from a fulfillment center, and 38 stores within short drives of the customer base were, in the language of the strategy deck, "38 micro-fulfillment centers we already own."

In January 2023, the board approved a **$6.8 million program**. The budget covered software licensing, systems integration, data migration, hardware (handheld scanners, pickup lockers and staging areas, label printers), training, and a program office. The vendor selected after a three-way competitive process was **Cardinal Retail Systems**, a mid-market retail technology firm with a combined inventory management and order fulfillment platform. Cardinal's references were solid, its price was roughly 30 percent below the enterprise-tier alternatives, and its sales team made one promise that became central to the program's public identity: with Cardinal's task-routing engine, a customer order placed online could be picked, staged, and ready at the counter in **nine minutes**.

The nine-minute pickup promise deserves a moment's attention, because it shaped everything that followed. It was a genuine differentiator — faster than the big boxes advertised — and it became the marketing centerpiece. "Order it on your phone; it's waiting before you park." Internally, the promise was treated as a system capability. What the leadership team did not fully interrogate at the time was that nine minutes was a *demonstration* figure, achieved in Cardinal's reference environments at retailers with inventory record accuracy above 97 percent, mature cycle counting programs, and dedicated fulfillment staff. Nine minutes was not a property of the software. It was a property of an operating environment Blue Ridge did not have.

Two dissenting voices are worth recording. Sofia Karagiannis, VP of Merchandising, argued in the planning phase that the company should sequence the program — fix inventory accuracy first, prove it stable for two quarters, then launch pickup. Bo Nakashima, Director of Store Operations, raised a related concern: the stores had no labor model for fulfillment. Who, exactly, would pick these orders? The floor associates were already stretched, and picking an online order while a contractor waits at the paint desk is a choice between two customers. Both concerns were noted, discussed, and set aside in favor of speed. The competitive erosion argued for urgency, and the integrated timeline promised a pilot by the 2023 holiday season — the year's biggest selling period and, the team reasoned, the best possible proving ground.

That reasoning — launch the pilot into peak season to maximize learning and revenue — would come to be seen as the single most consequential mistake of the program.

---

## III. The Pilot: November–December 2023

Implementation through 2023 was, by the standards of retail systems projects, unremarkable. There were the usual integration difficulties, a six-week slip in data migration, and friction over customization requests, but by October the new Cardinal platform was live in twelve pilot stores — a deliberately mixed set spanning large and small formats, urban Knoxville locations and rural stores, strong managers and average ones. The BOPIS capability launched at those twelve stores in early **November 2023**, supported by regional radio and digital advertising built around the pickup promise.

Orders came in immediately. That, at least, validated the demand thesis: customers in Blue Ridge's markets wanted this service. Everything after the order arrived went wrong.

The core failure was simple and brutal: **the system offered for sale items the stores did not have.** Cardinal's platform published on-hand inventory to the website, and the on-hand data was the migrated data from the old system — 71 percent accurate on a good day, and degrading further under holiday volume. A customer would order a cordless drill kit the system showed as in stock. An associate would receive the pick task, walk to the aisle, and find the peg empty. The associate would then search the back room, the overstock steel, the seasonal displays, and the receiving area — a hunt that could consume twenty minutes — before either finding the item somewhere the system didn't know about, or giving up and cancelling the line.

The measured results over the six-week pilot period:

- **Pick accuracy ran 62 percent.** Roughly four in ten ordered items could not be picked as ordered — cancelled, substituted, or fulfilled only after a manual search.
- **Actual pickup time averaged 41 minutes** against the advertised nine. Customers arrived on the strength of the promise and stood at the counter while associates were still hunting the floor.
- **2,300 orders were cancelled in six weeks** across twelve stores — a cancellation experience delivered, in many cases, to exactly the loyal contractor customers the program was meant to retain, during the busiest season of the year.

The damage was not confined to the online channel. Picking was assigned to floor associates as an additional task on top of their existing duties, with no added labor hours. During holiday peak, every hour spent hunting a phantom item was an hour taken from the sales floor. Walk-in service — the company's historic strength — degraded at the pilot stores. Two of the twelve pilot stores posted their worst December comparable sales in company history.

The most telling symptom, though, was behavioral. By mid-December, **store managers at a majority of the pilot locations had begun keeping their own paper counts** of high-velocity items — clipboards in the back room tracking what was really on hand, updated by hand, consulted before promising anything to anyone. This was rational self-defense by experienced operators, and it was also a devastating verdict: the front line had concluded, within six weeks, that the $6.8 million system could not be trusted, and had reverted to methods predating the 2007 system it replaced. Worse, the paper counts guaranteed the system would never converge on accuracy, because corrections were being recorded on clipboards instead of in the database.

Cardinal's field team, on site through December, ran diagnostics on their platform and found it performing to specification. The task routing worked. The order flow worked. The picking application worked. The software was doing exactly what it was designed to do with the data it was given. This finding, delivered in a tense January meeting, reframed the entire program: Blue Ridge did not have a software failure. It had exposed an operational one.

---

## IV. The Diagnostic: January–February 2024

Ashby-Ng resisted the two instinctive responses — blaming the vendor and pushing forward on willpower — and instead commissioned a formal diagnostic. She assigned it to the two executives who had raised concerns in the planning phase: **Sofia Karagiannis** and **Bo Nakashima**. The choice was deliberate. They had the credibility of having been right, and they had no incentive to protect the original plan.

For two months, Karagiannis and Nakashima worked the pilot stores directly: full physical audits of high-velocity categories, shadowing of receiving and picking processes, interviews with 60-plus associates and all twelve store managers, and transaction-level tracing of how specific inventory errors originated.

Their report, delivered to the board in late February 2024, made one central finding: **the cycle counting discipline the system assumed had never been built.**

Cycle counting — the practice of counting a small rotating slice of inventory every day, correcting the records, and investigating discrepancies — is the operational foundation on which every modern inventory system rests. The Cardinal platform, like all such platforms, was designed on the assumption that a mature cycle count program was feeding it corrections continuously. Blue Ridge had no such program. It had an annual full-store physical inventory, conducted by an outside service for financial reporting purposes, whose corrections were often applied in bulk months later. Between annual counts, errors accumulated without correction: receiving discrepancies when vendor shipments didn't match packing slips, unrecorded damage, theft, mis-shelved product, contractor returns processed inconsistently, and the managers' informal safety stock. The 71 percent accuracy figure wasn't a data problem to be fixed once by migration. It was the steady-state output of an operating model that generated errors faster than it corrected them.

The diagnostic identified a set of contributing findings:

1. **No error-correction loop.** Errors compounded for up to twelve months between annual counts. Any migration of this data into a new system simply gave the new system a corrupt starting point that would re-corrupt regardless of software quality.
2. **No fulfillment labor model.** Picking as an unstaffed side duty failed under any meaningful volume. At peak, pick tasks queued for over an hour before an associate could even begin.
3. **The promise drove the failure mode.** The nine-minute commitment meant customers arrived before problems could be resolved. A slower promise would have converted many 41-minute scrambles into invisible operational work completed before the customer showed up.
4. **Receiving was the largest error source.** Roughly 40 percent of traced discrepancies originated at the back door — shipments checked in against the purchase order rather than the physical count of what actually arrived.
5. **The front line had not been enrolled.** Store managers experienced the program as something done *to* them. Training covered how to use the software, not why accuracy mattered or how their behavior created or destroyed it. The clipboard counts were the natural result.

The report's recommendation was blunt: pause the rollout entirely, build the operational foundation the software required, and relaunch only when accuracy data — not the calendar — said the stores were ready. The estimated cost of the reset was an additional $2 million-plus in program spend and a permanent increase in store labor cost.

The board meeting that considered this recommendation was, by several accounts, the hardest of the program. $6.8 million was committed, the pilot had visibly failed in the company's own market, and the choice was between spending more to fix it or writing much of it off. Trumbo, to his credit, endorsed the pause rather than defending the original timeline. Ashby-Ng framed the decision to the board in terms that later circulated widely inside the company: *"We bought a system that assumes we tell it the truth. The project in front of us is learning to tell the truth."*

The board approved the reset in **spring 2024**.

---

## V. The Reset: Spring–Fall 2024

The reset program had four components, executed in sequence and in parallel over roughly nine months.

**1. The rollout was paused.** BOPIS marketing stopped. The twelve pilot stores kept the capability live at reduced promotion — the team judged that withdrawing the service entirely would be a second broken promise — but no new stores were added, and the advertised pickup commitment was immediately changed while the deeper work proceeded.

**2. A dedicated picker was funded at every store.** Rather than continuing to treat fulfillment as a side duty, the company created a defined fulfillment role — one dedicated associate per store during peak hours, flexing with volume — responsible for picking, staging, and pickup handoff, and, critically, for logging every discrepancy encountered during picking into the system as a count correction. This turned every failed pick from a customer disaster into a data repair event. The role added approximately **$1.4 million in annualized store labor cost**, a permanent operating expense the original business case had assumed away.

**3. A six-month cycle count program was built and run.** This was the heart of the reset and the least glamorous work of the entire program. Every store received a daily count discipline: ABC-classified, with the fastest-moving 200 SKUs counted weekly, mid-velocity items monthly, and the long tail quarterly. Fifteen to twenty minutes of counting per associate shift, built into the schedule rather than added on top. Receiving was rebuilt around blind counts — the receiver counts what physically arrived before seeing what the purchase order says should have arrived — attacking the largest single error source. Discrepancies above a threshold triggered root-cause investigation, not just correction, so the program fixed error *sources* rather than endlessly mopping error *symptoms*.

Crucially, the program was run through the store managers rather than around them. Nakashima toured every store, and the managers who had kept clipboard counts were treated not as saboteurs but as the diagnosticians they were — their paper records were used to seed corrections, and several were recruited to design the counting procedures. Each store's inventory accuracy became a posted, weekly, visible metric in the break room, and store managers' incentive plans were amended to include it. Accuracy stopped being an IT statistic and became an operational score the stores owned.

The trajectory was tracked weekly. Accuracy at the pilot stores moved from the low 70s in April 2024 to the mid-80s by July and crossed 90 percent by early fall. The company set a gate: **no store would relaunch pickup until it sustained 92 percent accuracy for four consecutive weeks.**

**4. The customer promise was changed from nine minutes to two hours.** This decision generated real internal debate — the nine-minute promise had been the marketing centerpiece, and lengthening it felt like retreat. Karagiannis argued the opposite: the promise that matters is the one you keep. Two hours gave the picker time to pick, resolve any discrepancy, source a substitute, or call the customer *before* they left the job site — converting nearly every potential failure into a quiet fix. Customer research conducted during the pause supported her: Blue Ridge's contractor customers overwhelmingly ordered from job sites and came by at day's end. What they demanded was not nine-minute speed but **certainty** — the order is here, complete, correct, guaranteed. The relaunch messaging was rebuilt around that: *"Ready in two hours. Ready means ready."*

**The relaunch itself was store by store**, beginning in late summer 2024, gated on the accuracy threshold, with each store's pickup volume ramped deliberately. Stores relaunched roughly two to four per month through the fall and winter. The final stores came online in early 2025. The contrast with the original big-bang holiday pilot was total: no store took a customer promise it had not first proven, with data, it could keep.

---

## VI. The Results: Measured Through March 2025

By **March 2025** — fifteen months after the failed pilot and roughly a year into the reset — the results were as follows.

**Inventory record accuracy: 94 percent**, up from 71 percent, sustained across all 38 stores, verified by independent audit sampling. This is at or near the benchmark range for well-run mid-market retailers and, more importantly, it is a *maintained* figure — the daily cycle count discipline means errors are now corrected within days of creation rather than accumulating for a year.

**Out-of-stock rate on the top 200 items: 6 percent**, down from 18 percent. This may be the single most commercially important number in the case. The replenishment system, now ordering against records it could trust, kept the core assortment on the shelf. The contractor who came in for PVC cement found PVC cement — and stayed to buy everything else.

**The pickup channel carried 11 percent of sales, at $34 million annualized.** From a standing start — indeed, from a public failure — the two-hour pickup service became a material channel in under a year of full operation. Order cancellation rates at relaunched stores ran under 2 percent, versus the pilot's catastrophic rate. Pickup customers, internal analysis showed, skewed toward exactly the contractor segment the company had been losing, and their total spend — pickup plus in-store — ran meaningfully above the customer average. The channel was not cannibalizing store sales; it was recovering trips that had been going to competitors.

**Comparable store sales: plus 3.8 percent**, reversing six quarters of decline averaging minus 4.2 percent — a swing of eight percentage points. Leadership was careful in attributing this: some of the recovery reflected market conditions, and disentangling the in-stock improvement from the pickup channel is analytically difficult since both flowed from the same accuracy foundation. But the store-level pattern was persuasive: the stores that relaunched earliest showed the comp improvement earliest, and the improvement tracked the accuracy gate rather than the calendar.

Two softer results deserve mention. First, the paper counts disappeared — not by edict, but because managers stopped needing them, which is the only durable way an informal workaround ever dies. Second, store manager turnover, which had ticked up during the erosion years, declined through 2024–25; several managers told Nakashima that having accurate inventory had removed the most demoralizing part of the job, which was disappointing customers they had known for twenty years.

---

## VII. The Full Cost

An honest accounting of the program:

- **Original approved budget: $6.8 million** (January 2023)
- **Final program cost: $9.1 million** — a 34 percent overrun, driven by the extended timeline, the diagnostic, the cycle count program build, retraining, and the reset of the relaunch
- **Added store labor: $1.4 million annualized** — the dedicated picker roles, a permanent operating cost absent from the original business case
- Not formally quantified, but real: the six weeks of damaged customer experience at twelve stores during the 2023 holiday season, including 2,300 cancelled orders delivered largely to the company's best customers, and the two pilot stores' worst-ever December comps

Against this, the return: a $34 million channel carrying an above-average customer, an eight-point comp swing on a $310 million base, a two-thirds reduction in core-item out-of-stocks, and — hardest to price but arguably most valuable — an operational discipline that makes every future system, analysis, and automation investment viable, because the underlying data is finally true. On the sales recovery alone, the incremental spend versus the original budget paid back within the first year of full operation. The leadership team's own assessment is more nuanced: the program succeeded, but roughly a third of its cost and a full year of its timeline were the price of learning something that was knowable in advance.

---

## VIII. What the Leadership Team Would Do Differently

In retrospective sessions conducted in mid-2025, Ashby-Ng, Trumbo, Karagiannis, and Nakashima converged on a candid set of conclusions.

**They would have sequenced, not bundled.** The integrated program — fix inventory and launch pickup simultaneously — looked efficient and was actually the root cause of the failure. Karagiannis's original proposal — build accuracy first, prove it stable, then sell against it — would have delayed the pickup launch by perhaps nine months and avoided the holiday failure, the customer damage, and much of the overrun. The team's consensus: *the offensive capability was only ever going to be as good as the defensive foundation, so the foundation was never optional and never parallel.*

**They would not have launched a pilot into peak season.** The logic of maximizing learning during the biggest volume period was exactly backward. Peak season maximizes the *cost* of failure and minimizes the organization's *capacity to respond*. A February pilot would have exposed the same problems at one-third the volume, with slack labor available to absorb them and low-stakes customers rather than holiday shoppers.

**They would have interrogated the vendor's reference conditions.** The nine-minute promise was real — at retailers with 97-percent-plus accuracy and dedicated fulfillment staff. Cardinal never hid this; Blue Ridge never asked the right question, which was not "what can the system do?" but "what must *we* be, operationally, for the system to do it?" Trumbo has since institutionalized a rule for technology selection: every vendor performance claim must be accompanied by a written statement of the operating conditions under which it was achieved, and a gap assessment against Blue Ridge's current state.

**They would have set the customer promise from operational data, not marketing ambition.** Two hours proved not merely survivable but *preferred* by the actual customer base, whose real requirement was certainty. The team now regards the promise itself as an operational parameter to be earned, tightened only when the data supports it — several high-accuracy stores began piloting a one-hour tier in 2025, gated exactly as the relaunch was.

**They would have staffed and enrolled the front line from day one.** The unfunded fulfillment labor and the manager clipboards were both foreseeable — indeed, Nakashima foresaw them. The reset succeeded largely because it made store managers owners of accuracy rather than users of software. Ashby-Ng's summary: "We spent $6.8 million on a system and about $40 a store on clipboards, and for six weeks the clipboards won. That should have told us everything."

**They would have treated the front line's workarounds as diagnosis, not resistance.** The paper counts were the stores telling headquarters, precisely and early, what was broken. The reset began working the day leadership started reading them that way.

---

## IX. What a Reader in a Similar Position Should Take From This Case

Blue Ridge's story is specific — a regional hardware chain, one vendor, one holiday season — but the pattern it exhibits is among the most common in operational technology programs, and the lessons generalize.

**1. Software assumes an operating model. Buy the software only after you have, or have a plan to build, the model.** The Cardinal platform did not fail; it performed to specification on data that was 29 percent wrong, because Blue Ridge lacked the cycle counting discipline the platform presumed. Every serious system embeds assumptions about the processes and behaviors surrounding it. The right diligence question is never "does the software work?" It is "under what operational conditions does it work, and how far are we from those conditions?" The gap between a vendor's reference environment and your own is your true project — usually larger, slower, and less glamorous than the implementation itself.

**2. Data accuracy is not a migration task; it is a maintained state.** Blue Ridge's instinct — that new software plus a data cleanup would fix a 71 percent accuracy problem — misunderstood the problem's nature. Accuracy is the output of a continuous correction loop. Without the loop, any clean starting point re-corrupts at the rate errors are generated. Before automating decisions against your data, ask what mechanism corrects that data daily, who owns it, and how it is measured. If the answer is an annual event, the data cannot support real-time promises.

**3. Sequence the foundation before the offense, even when bundling looks efficient.** The temptation to combine remediation with a revenue-generating launch is powerful — one budget approval, one change effort, a better story for the board. But the revenue capability inherits every weakness of the foundation, and it inherits them *in front of customers*. Blue Ridge paid $2.3 million over budget, a year of delay, and 2,300 cancelled orders to learn what sequencing would have cost only patience.

**4. Never pilot into peak.** Pilot when failure is cheap and capacity to learn is high. Volume stress-testing has its place — after the process works at low volume, not as the first exposure.

**5. Set customer promises from proven operational capability, and gate expansion on data, not calendars.** The single most effective mechanism in Blue Ridge's recovery was the relaunch gate: no store sold the promise until it sustained 92 percent accuracy for four weeks. The promise followed the proof. Note also that the "worse" promise — two hours instead of nine minutes — produced the better business, because the customers' actual requirement was reliability. Discover what your customers truly need before assuming it is speed.

**6. Fund the labor the new work requires.** New capabilities create new work. Business cases that absorb that work into existing headcount are usually not saving money; they are hiding a cost that will be paid in failed execution. Blue Ridge's $1.4 million in picker labor was not overhead on a $34 million channel — it was the channel's operating engine, at about four cents per revenue dollar.

**7. Read frontline workarounds as free diagnostics.** When experienced operators build shadow systems — paper counts, private spreadsheets, informal safety stock — they are documenting exactly where the official system fails. Organizations that punish workarounds lose the signal; organizations that study them, as Blue Ridge eventually did, get their diagnosis at clipboard prices.

**8. When a program fails, resist both blame and momentum.** The pivotal management act in this case was Ashby-Ng's response to the pilot: not firing the vendor, not doubling down on the schedule, but commissioning an honest diagnostic — and assigning it to the executives who had dissented, whose credibility made the hard findings actionable. Programs rarely fail at the failure; they fail at the response to it. Blue Ridge's willingness to pause, absorb a 34 percent overrun in public view of its board, and rebuild from the foundation converted a failed launch into a durable capability.

The arithmetic of the case makes the final point. Blue Ridge spent $9.1 million and $1.4 million a year in labor and got a $34 million channel, an eight-point comp reversal, and clean data underneath the whole company. But the same result was available for roughly $7 million and a year less time, without the holiday damage, to a version of the company that had asked one question at the start: *what does this system assume we already are — and are we that?* For any leader weighing an ambitious customer-facing technology program atop an aging operational foundation, that is the question this case exists to make unavoidable.
