# Rebuilding the Engine While the Hospital Runs

## A Case Study of Tidewater Health Interfaces, 2011–2025

---

## I. The Company and the Machine Underneath It

Tidewater Health Interfaces occupies four floors of a converted tobacco warehouse in downtown Durham, North Carolina, a few blocks from the Amtrak station. The company was founded in 2009 by two engineers who had spent the previous decade building point-to-point HL7 feeds inside a regional health system and concluded, correctly, that every hospital in the country was solving the same problem badly and separately. By 2023 Tidewater sold clinical integration middleware to 340 hospitals, employed 210 people, and carried $46 million in recurring revenue. It was profitable, it was well regarded by the people who used it, and it was resting on a foundation that had not been meaningfully rearchitected since 2011.

What Tidewater sells is unglamorous and load-bearing. When a lab result leaves an analyzer, when an admission is registered at a bedside terminal, when a pharmacy order is transmitted to a dispensing cabinet, something has to receive that message, understand its dialect, translate it into the dialect the receiving system expects, guarantee its delivery, and log the fact that it happened. Hospitals run dozens to hundreds of these interfaces. They break constantly, for reasons ranging from a vendor's version upgrade to a nurse typing a patient name with an apostrophe in it. Tidewater's engine sat in the middle and absorbed that chaos, and the customers who ran it had, over a decade, come to trust it the way you trust a load-bearing wall — without thinking about it, until it moves.

The engine was written in 2011 in Java, deployed as a customer-hosted installation, and it was, by the standards of its era, competently built. It was also single-tenant by design, configured through a thick client, and dependent on a message-persistence model that assumed the machine it ran on had a local disk and would not be shared with anyone. Every one of the 340 customers ran their own copy. Every copy drifted. By 2023, Tidewater's support organization was maintaining eleven distinct minor versions in the field, with a long tail of customers who had customized their deployment in ways that were documented, when they were documented at all, in the memory of whichever field engineer had done the work.

Only 14 customers ran on the hosted version, which was not truly hosted in any modern sense. It was the same single-tenant software, installed on virtual machines Tidewater rented and managed on the customer's behalf, one stack per hospital. It cost more to run than it earned, and the company kept it alive mostly as a proof point for sales conversations with prospects who had begun to ask, with increasing frequency and diminishing patience, whether Tidewater had a cloud offering.

The numbers that eventually forced the decision were not subtle. Uptime across the installed base averaged 99.1 percent against a contractual service commitment of 99.95 percent — a gap that sounds small and is not. Nine tenths of a percent of a year is roughly seventy-nine hours. For a health system running admissions and lab results through Tidewater, seventy-nine hours of degraded or absent integration means downtime procedures, paper requisitions, and a clinical informatics director explaining to a chief medical officer why the emergency department cannot see yesterday's radiology.

Support handled 4,100 tickets a month against a customer base of 340. That is twelve tickets per customer per month, or roughly one every two business days, for a product that in principle should sit invisibly in the background. The ticket mix told the real story: a plurality were version-specific issues that would not reproduce on any other customer's installation, and resolving them required a support engineer to reconstruct, from logs and screen shares, the specific configuration of a specific machine in a specific hospital basement.

Annual churn had reached 14 percent. In a business with $46 million in recurring revenue, that is $6.4 million walking out the door every year, against a sales organization sized to add perhaps $8 million. The company was running to stand still, and the running was getting harder because the reference customers were the ones leaving.

Two enterprise renewals worth $5.2 million combined were flagged as at-risk going into 2024. One was a multi-hospital system in the Ohio Valley whose CIO had told Tidewater's account team, in writing, that the next contract would require a hosted architecture with a credible uptime record. The other was a large academic medical center that had begun a formal evaluation of two competitors. Neither had left. Both had made clear that the status quo had an expiration date.

Chief Executive Prabha Venkataraman had joined Tidewater in 2020 from a larger healthcare software company, where she had watched a comparable product line die slowly of architectural neglect. She had spent her first two years at Tidewater fixing go-to-market problems and had deferred the platform question, partly because the company was profitable and partly because she did not yet have a Chief Technology Officer she trusted to lead the answer. Nils Bergstrom arrived in mid-2022. By the fall of 2023 the two of them had reached the same conclusion independently, which is generally the point at which a company stops debating and starts planning.

The conclusion was that the engine could not be incrementally modernized. Bergstrom's technical argument, which he made to the board in a memo that circulated for three months before the vote, was that the persistence layer and the tenancy model were entangled in a way that made multi-tenancy impossible to retrofit. Every path to a hosted product ran through a rewrite of the core. Venkataraman's business argument was simpler: the cost to serve was $11,400 per customer per year and rising, churn was accelerating, and the two at-risk renewals were early indicators rather than isolated events.

---

## II. The Plan, and What It Assumed

In March 2024 the board approved $8.5 million over eighteen months to rebuild the product as a multi-tenant hosted service. The target completion date was September 2025. Miguel Arellano, who had been Tidewater's principal engineer on the message-routing subsystem since 2016 and had been promoted to Chief Architect in January, took technical leadership.

The plan had four pillars, and it is worth setting them down as they were written, because the gap between them and what happened is the substance of this case.

**Rebuild the core as a genuinely multi-tenant service.** One deployment, many customers, shared infrastructure, with tenant isolation enforced at the data and routing layers rather than by giving everyone their own box. This was the whole point. Multi-tenancy is what makes hosted software cheaper to run than customer-hosted software; without it, a hosted product is just customer-hosted software with a different owner of the pager.

**Replace the persistence and queueing layer.** The 2011 engine wrote messages to a local durable store and processed them in-order per interface. The new architecture used a distributed queueing layer designed to handle much higher throughput with horizontal scaling. This was, in the plan, the single largest technical change and the one Bergstrom flagged as carrying the most risk. He was right, though not in the way he expected.

**Build a migration path that customers could walk without a project of their own.** Tidewater's customers are hospitals. Hospitals do not have spare integration engineers sitting idle. The plan committed to migrating each customer's interface configurations automatically, with Tidewater engineers doing the work and the customer providing a testing window and a cutover approval.

**Migrate in waves.** This was the assumption that broke. The plan called for waves of twenty-five to thirty-five customers, grouped by similarity of configuration, with roughly one wave a month beginning in the fourth quarter of 2024. Twelve waves would carry the base. The logic was sound on paper: waves amortize the coordination overhead, they let the migration team develop rhythm, and they get the fleet consolidated fast enough that the company can decommission the old support burden and realize the cost savings that justified the investment.

Underneath the wave plan sat three assumptions that nobody wrote down as assumptions, which is how assumptions usually work.

The first was that customer configurations were more similar than they were different. The migration tooling was built and tested against a sample of thirty configurations pulled from the customer base, and it handled them well. Nobody had established that thirty was a representative sample of a population that had been drifting independently for thirteen years.

The second was that production load could be inferred from steady-state metrics. The team had good telemetry on message volumes, throughput, and latency, collected across the installed base and averaged. The new queueing layer was sized against those numbers with substantial headroom. What the averages did not capture was the shape of the load.

The third was that failure would be graceful. The architecture had been designed with backpressure, retry, and dead-letter handling. In testing, when the team pushed load beyond capacity, the system degraded in an orderly way. Nobody had tested what happened when several tenants degraded simultaneously and their retry behavior compounded.

Development ran from March through October 2024. It went well. The team hit its internal milestones, the new engine performed impressively in load testing, and by late October Tidewater had a product that was, by every measure it had chosen to apply, ready. Arellano's team had built something genuinely better than what it replaced. That fact would get lost for about four months.

---

## III. Wave One

The first migration wave moved 28 hospitals over the first two weeks of November 2024. Customers were selected for relatively clean configurations, moderate message volumes, and engaged clinical informatics teams — a deliberately favorable cohort. Each cutover followed a runbook: freeze configuration changes, run the automated migration, validate interface-by-interface in a test environment, cut over during a low-volume window, monitor for forty-eight hours.

The first eleven cutovers went fine. Message flow was clean, latency was better than the old engine, and the migration team began to feel the rhythm the plan had promised. Two customers reported minor mapping discrepancies, both resolved within a day.

The problem started on the night of November 19th, by which point roughly twenty tenants were live on the shared platform.

Hospitals do not generate load evenly. During the day, message traffic is a steady stream of admissions, orders, and results. At night — typically between eleven and three — hospital source systems run batch jobs. Census reconciliation, billing extracts, lab result backfills, chart abstraction feeds. These jobs dump large volumes of messages in short bursts. On the old engine, each customer's batch load hit their own dedicated machine, sized generously because hardware is cheap relative to hospital software, and it was absorbed without anyone noticing.

On the new multi-tenant platform, twenty hospitals' overnight batch loads arrived at the same queueing layer within the same three-hour window. The aggregate burst was roughly eleven times the sustained daytime throughput the layer had been sized for. Peak capacity had been provisioned at four times sustained load, which the team had considered conservative.

The queueing layer did not crash. It did something worse: it slowed down. Consumers fell behind producers, queue depth grew, and as latency increased, the upstream interface engines began hitting their acknowledgment timeouts and retransmitting. The retransmissions added load. The added load increased latency further. By 2 a.m. the system was in a stable, self-sustaining congestion state — the distributed-systems equivalent of a traffic jam that persists after the accident has been cleared.

The on-call engineer was paged at 1:47 a.m. and correctly identified the problem as backpressure. What he did not have was a way to shed load selectively. The isolation model separated tenants at the data layer, so no customer could see another's messages, but the queueing layer was shared. There was no per-tenant throttle. The only available controls were to scale the consumer fleet, which he did, and to wait.

Scaling helped, but the batch windows across twenty hospitals in three time zones did not align neatly, and each night's backlog rolled into the next day's steady-state load. Over four days, message backlog peaked at approximately 1.2 million clinical messages.

A backed-up clinical message is not a delayed email. It is a lab result that has not reached the ordering physician. It is an admission that has not propagated to the pharmacy system, so the pharmacist does not know the patient exists. It is a discharge that has not reached billing, and — more urgently — a transfer that has not reached the bed-management system. Hospitals have downtime procedures for exactly this situation, and over those four days, eleven of the twenty-eight went to some form of downtime procedure. Two went to full paper for a shift.

The engineering response was competent and fast. Arellano's team shipped a per-tenant rate limiter in thirty-one hours, added dedicated consumer pools for high-volume tenants, and re-sized the fleet. By November 24th the backlog was cleared and the platform was stable. From a purely technical standpoint the incident was over in five days.

From every other standpoint it was just beginning.

---

## IV. What It Cost

Three hospitals reverted to the old engine. Each reversion took four to six days of engineering time, involved reconstructing a configuration that had been migrated away, and — most damaging — required Tidewater to admit in writing that the new platform was not ready. Those three reversion letters circulated. Health system CIOs talk to each other constantly, through formal associations and informal networks, and the story of Tidewater's November was in circulation before Thanksgiving.

One 900-bed system left for a competitor. This customer had been with Tidewater since 2014, ran 214 interfaces, and represented roughly $680,000 in annual recurring revenue. Their integration team had been sharply critical during the incident and had escalated to their CIO on day two. The termination notice arrived January 8th, 2025. The stated reason was the November outage. The truer reason, which their CIO said directly in an exit conversation with Venkataraman, was that the outage confirmed a concern they had already formed: that Tidewater had let its platform age past the point of safety and was now trying to fix it in production, on their patients.

$1.1 million in service credits went out. Tidewater's contracts carried standard availability credits, and the company chose not to argue the fine print. Venkataraman's instruction to the account team was to calculate the credits generously, apply them without requiring customers to file claims, and communicate them proactively. Several account managers argued this was leaving money on the table. She overruled them on the grounds that the company was not in a position to be seen negotiating over an incident it had caused. In retrospect, both she and Oyelowo identified this as one of the few decisions from that period they would repeat without modification.

The harder costs were not on the ledger. Migration volunteers evaporated: Tidewater had a pipeline of roughly forty customers who had asked to be in early waves, and by mid-December that list had four names on it. Sales cycles extended as prospects asked, reasonably, about the November incident. Two of the nine engineers on the platform team resigned in the first quarter of 2025, both citing burnout from the incident response and the months of scrutiny that followed.

And the at-risk renewals got worse. The Ohio Valley system, which had told Tidewater it needed a hosted architecture, now had evidence that Tidewater's hosted architecture was dangerous. The account team's own assessment in December put the probability of renewal below forty percent.

---

## V. The Stop

Danielle Oyelowo, VP of Customer Success, and Tomasz Wieczorek, Head of Support, forced a halt in December 2024.

The word "forced" is accurate and worth dwelling on. There was pressure to continue. The engineering fix had worked, the platform was stable, the December wave had been planned and staffed, and the December 2025 board commitment assumed twelve waves. Every month of delay pushed the cost-to-serve savings further out and extended the period during which Tidewater ran two platforms simultaneously — the most expensive possible state.

Arellano's position, defensible at the time, was that the specific failure mode had been identified and fixed, that the new rate limiting and dedicated consumer pools addressed it directly, and that the next wave could proceed with additional monitoring. He was technically correct about the specific failure.

Oyelowo's argument was not technical. She had spent three weeks on calls with the twenty-eight wave-one customers and had reached a conclusion the engineering data did not show: the company did not understand its own product in the field well enough to predict how it would behave. The overnight batch load had surprised them. What else would surprise them? She could not answer that, and neither could anyone else, and she argued that proceeding without an answer was not a calculated risk but an uncalculated one.

Wieczorek brought the operational case. His support organization had absorbed a 60 percent ticket spike in November and was still working through the tail in mid-December. Ticket volume across the base had gone from 4,100 to over 6,500 in November. His team was, in his phrase to the executive group, "spending its credibility faster than it was earning it." If the December wave went badly, he did not have the staff to absorb it, and the failure would spread to customers who were not even involved.

The stop was called on December 11th, 2024. No migrations occurred in December or January. The pause lasted seven weeks.

Venkataraman's decision on how to communicate it mattered more than the decision itself. She wrote directly to every customer — all 340, not just the migrated ones — describing what had happened, what it had cost, what Tidewater had gotten wrong, and what would change. The letter did not use the word "unprecedented" and did not describe the incident as a learning opportunity. It said the company had made a planning error, that the error had caused patient-facing disruption at eleven hospitals, and that migrations were stopping until Tidewater could demonstrate they were safe.

She also went to the board in January and moved the completion date from September 2025 to December 2025 — a three-month extension that would prove insufficient, and that she extended again in a March update. The board approved. One director, a former hospital system CIO, told her afterward that the letter to customers had done more for the company's position than the schedule extension had cost it.

---

## VI. The Changed Method

What Tidewater rebuilt during the pause was not the platform. The platform was fine. What it rebuilt was the migration process, and the changes came in four parts.

**Nine additional migration engineers.** Tidewater's migration capacity had been eleven engineers, most of them borrowed part-time from the platform and field organizations. The company hired nine dedicated migration engineers between December and February, drawing heavily from health-system integration teams — people who had lived on the customer side and knew what a batch job looked like at 1 a.m.

The cost was roughly $1.6 million annualized. Bergstrom's argument to the board was that the migration was not an engineering project with a customer-facing component but a customer-facing project with an engineering component, and it had been staffed backward. The nine hires changed the ratio of people who understood hospital operations to people who understood distributed systems, and that ratio, more than any technical control, was what had been missing in November.

**Shadow mode against production for two weeks before every cutover.** This was the single most important change. Before any customer cut over, Tidewater ran that customer's full production message traffic through the new platform in parallel with the old engine for two weeks. The new platform processed everything and produced output that was compared against the old engine's output message-by-message, but its output went nowhere. The old engine remained authoritative.

Two weeks was chosen deliberately, over some internal objection that one week would suffice. Two weeks captures two weekend cycles, at least one month-end boundary for roughly half of customers, and — critically — fourteen overnight batch windows. The November failure would have been visible in shadow mode on the first night.

Shadow mode also produced something nobody had anticipated: a precise, empirical map of configuration drift. The message-by-message comparison surfaced discrepancies between old and new behavior that were invisible in configuration review, because they arose from undocumented customizations, version-specific bug behavior that customers had come to depend on, and in a few memorable cases, deliberate workarounds installed by field engineers who had left the company years earlier. Across the customers migrated between February and July 2025, shadow mode surfaced an average of 4.7 discrepancies per customer, of which roughly one in six would have caused a clinically significant error.

That number retroactively explains wave one. The team had assumed configurations were similar. They were similar in structure and different in detail, and the details were where patients lived.

**One hospital at a time.** The wave model was abandoned entirely. Tidewater moved to a single-customer pipeline: one hospital in shadow mode, one hospital in cutover, one hospital in post-cutover monitoring, with the pipeline staggered so that several customers were in different stages simultaneously but only one cut over on any given night.

This was the most expensive change and the most contested. It capped throughput. Even with twenty migration engineers, a two-week shadow period and a staged pipeline meant roughly eight to twelve customers a month at steady state, against the plan's thirty. It stretched the timeline and extended the dual-platform period.

The counter-argument was blunt: waves had concentrated risk. In November, one failure had touched twenty-eight customers because twenty-eight customers had been in flight together. Under the new model, a comparable failure would touch one, and the migrated tenants running alongside would be protected by the per-tenant isolation and throttling built in December. The company traded speed for blast radius, consciously, and Venkataraman told the board that the trade was permanent for the remainder of the program.

**The finish date moved to December 2025.** Communicated to the board in January and to customers in February. It later moved again, to March 2026, in the March board update — a fact Venkataraman has been careful to include when telling this story, because the January date was itself optimistic and was set before the new pipeline had produced enough data to forecast honestly.

A fifth change, less formal, deserves mention. Wieczorek instituted a practice he called the pre-cutover interview: before any customer entered shadow mode, a migration engineer spent ninety minutes with that hospital's integration staff asking what was strange about their environment. Not a configuration review — a conversation, structured around questions like "what breaks on the third Tuesday of the month" and "what do you do differently than the manual says." The interviews were transcribed and attached to the migration record. They surfaced roughly a third of the issues that shadow mode later confirmed, several weeks earlier and much more cheaply.

---

## VII. Where Things Stood in July 2025

Migrations resumed February 3rd, 2025, with a single 140-bed community hospital in eastern North Carolina, chosen because its integration director had been the most vocally supportive customer during the November incident. That cutover took three weeks end to end and went cleanly.

By July 2025, twenty-two months into an eighteen-month program:

**190 of 340 customers were migrated** — 56 percent of the base, representing roughly 61 percent of recurring revenue, since the migration pipeline had been deliberately weighted toward larger accounts once the process stabilized.

**Uptime was 99.96 percent** across the migrated fleet, measured over the trailing ninety days. This exceeded the 99.95 percent contractual commitment and stood against the 99.1 percent the old customer-hosted base had averaged. The improvement came less from the new architecture's inherent reliability than from operational consolidation: one platform, monitored continuously by a team whose entire job was to watch it, instead of 340 installations monitored by hospital IT staff who noticed problems when a clinician called.

**Support tickets were 1,700 a month**, down from 4,100 — a 59 percent reduction against a customer base that had shrunk by only a handful of accounts. The composition changed as much as the volume. Version-specific issues, which had been the largest category, essentially disappeared for migrated customers, because there was one version. What remained was concentrated in genuine integration problems — a source system changing its message format, a new interface being stood up — which is the work Tidewater's support organization exists to do.

**Churn was 6 percent**, down from 14. This was the number Venkataraman watched most closely, and it recovered more slowly than the operational metrics; it was still above 9 percent in March. The Ohio Valley system renewed in May 2025 for three years, after spending nine weeks in shadow mode and cutting over in April. The academic medical center renewed in June. Together the two contracts were worth $5.2 million.

**Cost to serve fell from $11,400 to $6,900 per customer per year** — a 39 percent reduction, and the number that carried the business case. The savings came from three places: support labor, which fell with ticket volume; infrastructure, where shared multi-tenant capacity replaced 340 independent deployments; and field engineering, where the elimination of version drift removed most of the on-site work that had previously consumed the field team. At full migration, the annualized saving across 340 customers would be roughly $1.5 million against a revenue base of $46 million.

**Spend stood at $12.3 million** against an approved $8.5 million — a 45 percent overrun. The variance decomposed roughly as follows: $1.6 million in additional migration engineering headcount, $1.1 million in service credits, approximately $2.4 million in extended dual-platform operating costs from running both stacks eleven months longer than planned, and the remainder in incident response, remediation engineering, and the shadow-mode infrastructure, which required a parallel processing environment nobody had budgeted for.

The board approved the additional spend in two tranches, in January and March 2025. The January conversation was difficult. The March conversation was not, because by March the migrated cohort's metrics were unambiguous and the trend line was doing the arguing.

One number Tidewater tracks internally that does not appear in board materials: of the 190 migrated customers, 187 completed cutover without a service-affecting incident. Of the three that did not, two experienced brief interface-specific outages resolved within four hours, and one required a rollback to the old engine, completed in six hours, with a successful re-migration eleven weeks later. That ratio — 98.4 percent clean cutovers — is what the changed method bought.

---

## VIII. What the Company Would Do Differently

Venkataraman, Bergstrom, and Arellano each gave separate accounts of what they would change, and the accounts differ in instructive ways.

**Arellano's answer is about validation.** The team validated the new platform against synthetic load derived from aggregate production telemetry. What it should have done — and what shadow mode later did automatically — was run real production traffic from real customers through the new platform before anyone depended on it. The capability was not hard to build; the team built it in six weeks during the pause. It was not built earlier because nobody framed it as a requirement. Load testing felt like validation. It was not. It was validation of the model, and the model was wrong about the shape of the load.

The broader lesson he draws: when replacing a system that has run in production for a decade, the old system is the specification. Not the documentation, not the requirements, not the architects' understanding — the running system, including its bugs, its accidents, and the behaviors customers have unknowingly built on top of. Any replacement program that does not have a mechanism for comparing new behavior against old behavior on real traffic is guessing.

**Bergstrom's answer is about staging.** He would not have run waves at all, at any point. The wave model was inherited from thinking about deployment rather than migration, and the two are different: a deployment is reversible and affects your infrastructure, while a migration is expensive to reverse and affects someone else's operations. Waves optimize for throughput and concentrate risk, and Tidewater had no evidence in November 2024 that its risk was low enough to concentrate.

His refinement is that the correct sequence is not "start slow and accelerate" as a schedule but as an evidence threshold. Tidewater should have committed in advance to migrating one customer at a time until a specific, pre-declared number of consecutive clean cutovers — his suggestion is twenty — before increasing batch size, and to reverting to single-customer pace after any service-affecting incident. That rule would have cost the company nothing in the good case and would have prevented November entirely.

**Venkataraman's answer is about who holds the schedule.** The December 2025 date, and the September 2025 date before it, were engineering estimates converted into board commitments and then defended as commitments. When wave one failed, the schedule became an argument for proceeding rather than a piece of information to be updated. Oyelowo and Wieczorek had to force a stop against organizational momentum, and the fact that forcing was necessary was itself the defect.

What she would build differently: an explicit, pre-agreed authority for the customer-facing organization to halt migration, exercisable without executive approval, with a defined re-start process. She has since implemented this. Oyelowo and Wieczorek jointly hold a standing halt authority over the migration pipeline, and the halt does not require Venkataraman's or Bergstrom's consent. It has been exercised twice since February 2025, once for four days and once for nine, both times over patterns in shadow-mode data that turned out to be real.

She would also have set the board expectation differently from the start. The March 2024 approval was framed as an $8.5 million, eighteen-month project with a defined scope. She now believes the honest framing was a range — $8 to $14 million, eighteen to thirty months — with the width of the range explicitly attributed to unknown configuration drift across 340 independently evolving deployments. The board would have approved it. She did not offer it because she was not confident enough in her own understanding of the risk to defend a number that wide, which she describes as the least defensible thing she did in the entire program.

Two further items appear on all three lists.

**The 14 hosted customers were treated as a proof point rather than a data source.** Tidewater had fourteen customers whose infrastructure it operated directly, with full telemetry, for years before the rebuild. Nobody mined that data for load-shape characteristics. The overnight batch pattern that broke wave one was visible in the hosted customers' metrics going back to at least 2021. It had never been looked at, because those deployments were single-tenant and the pattern was operationally irrelevant until tenants started sharing a queue.

**The migration should have been priced.** Tidewater migrated customers at no charge, on the theory that the move benefited Tidewater as much as the customer and that charging would slow adoption. The unintended consequence was that customers had no stake in the migration's success. Several treated their shadow-mode validation window as low priority, delaying cutover by weeks. Several more were unavailable during their own cutover windows. Bergstrom's suggestion — a nominal migration fee, credited back on successful cutover — would have cost the company nothing and created a scheduling commitment on both sides.

---

## IX. What to Take From It

For a reader running a similar program — an aging platform, a customer base that depends on it, and a rebuild that has to happen while the old thing keeps running — several things in this account generalize.

**The architecture was never the hard part.** Arellano's team built the new platform roughly on schedule and it worked. Every dollar of the $3.8 million overrun and every one of the lost customers traces to migration, not construction. Programs like this are consistently under-planned on the migration side because migration is unglamorous, hard to estimate, and owned ambiguously between engineering and customer success. If your plan devotes more thought to what you are building than to how customers will get onto it, your plan is wrong in the way Tidewater's was wrong.

**A decade-old system in production is a specification you do not possess.** Tidewater had 340 deployments that had drifted independently for thirteen years, and it discovered the extent of that drift only when shadow mode began producing message-level comparisons — 4.7 material discrepancies per customer, one in six of them clinically significant. No amount of configuration review would have found those, because they were not in the configuration. They were in the interaction between configuration, version, data, and undocumented human intervention. The only reliable way to find them is to run the real thing through the new system and compare.

**Test against the shape of the load, not its average.** Aggregate telemetry told Tidewater its new queueing layer had four times the headroom it needed. Reality delivered eleven times the sustained load in a three-hour window, because twenty hospitals ran batch jobs at the same time of night. Averages destroy exactly the information that matters for capacity planning. Ask what happens at the worst hour, on the worst day, when every tenant does the same thing simultaneously — and if you cannot answer from data, you have not tested.

**Batch size is a risk control, and the correct default is one.** The wave model concentrated twenty-eight customers into a single failure. Nothing about the November incident was made worse by the underlying defect being severe; it was made worse by twenty-eight customers being exposed to it at once. Moving to one customer at a time cost Tidewater time and money and prevented every subsequent failure from becoming an event. Increase batch size only against evidence — a declared number of consecutive clean migrations — and revert to one on any incident.

**Give the customer-facing organization real authority to stop.** Oyelowo and Wieczorek were right in December 2024, and they were right on evidence that engineering leadership did not find persuasive, because it was not the kind of evidence engineering leadership was looking at. They had to spend political capital to be heard. That is a design flaw in the organization, and it is common. Whoever talks to customers should be able to halt the program without asking permission, because they will see the problem first and they will see it in a form that does not look like a graph.

**Own the failure faster and more completely than feels comfortable.** Venkataraman's letter to all 340 customers, and the decision to pay $1.1 million in credits without requiring claims, were expensive and they worked. Tidewater lost one customer to the November incident. It could easily have lost fifteen. In a market where buyers talk to each other constantly, the currency is not perfection — customers know software breaks — it is whether the vendor tells the truth quickly. The company that hedges in week one spends the next two years being asked what else it hedged about.

**Budget in ranges and defend the range.** The $8.5 million, eighteen-month commitment was a point estimate for a program with irreducible uncertainty about 340 independently drifted deployments. It came in at $12.3 million and will finish near thirty months. The board approved the overruns, but Venkataraman spent credibility in January 2025 that she would have kept had she framed the original approval honestly. If you cannot defend a wide range to your board, the problem is not the board.

Tidewater will finish the migration in early 2026. When it does, the company will run one version of one product for 340 hospitals, at $6,900 per customer per year instead of $11,400, with uptime that clears its contractual commitment and a support organization that handles less than half the volume it did in 2023. That is a good outcome, and the rebuild was the right decision. It cost 45 percent more than planned and about a year longer, and roughly $1.8 million of that overrun — the credits, the lost account, the remediation — bought nothing at all. It was the price of four days in November when twenty-eight hospitals learned something about Tidewater's platform that Tidewater should have learned first, in shadow mode, with nobody watching.
