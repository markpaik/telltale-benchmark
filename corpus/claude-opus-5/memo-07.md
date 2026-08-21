# Quarry Street Systems — Internal Memorandum Packet

*Gateway Migration Program, November 2026 – January 2027*

---

**TO:** All Employees
**FROM:** Dolores Kaminski-Lim, Chief Product Officer
**DATE:** November 6, 2026
**SUBJECT:** Gateway Migration Program — the March 31, 2027 deadline and what it means for us

I want everyone to hear this from me directly and at the same time, rather than in pieces over the next few weeks.

Our card-present processor has confirmed in writing that it will decommission the legacy gateway on March 31, 2027. That is not a target, a preference, or an opening position in a negotiation. It is a scheduled shutdown of infrastructure that our merchants' card transactions travel through today. On April 1, 2027, any Quarry Street merchant still routing through that gateway will be unable to accept a card payment. Not slowly, not with degraded performance — they will swipe a card and nothing will happen.

We have 4,100 merchants. The large majority of them run terminals that can accept a firmware update, be repointed at the new gateway, and continue operating with a short service window and a modest amount of confusion. Approximately 900 merchants run terminal hardware that cannot take the update at all. For those merchants, the only path forward is replacement hardware. There is no software fix, no configuration workaround, and no arrangement in which we or the processor extend the old gateway for a subset of accounts. I asked. The answer was no, and the answer was final in a way I have rarely encountered from a vendor.

I am naming this work the Gateway Migration Program, and I am asking every function in the company to treat it as the organizing priority through the end of the first quarter.

## What this means concretely

For Engineering, it means the migration tooling, the terminal provisioning pipeline, and the new gateway integration are the work. Kwabena and I have already agreed to defer the inventory module rewrite and the second phase of the reporting redesign. Those were good commitments and I am sorry to break them, but a merchant who cannot take a credit card does not care about improved reporting.

For Merchant Support, it means a volume of inbound contact unlike anything this company has handled. Amara will set policy on that separately and I will not preempt her, except to say that she has my full backing on whatever escalation structure she puts in place.

For Product, it means I am pulling two product managers off roadmap work and assigning them full-time to migration sequencing — which merchants go when, in what order, and with what communication. This is not a technical problem alone. A restaurant that gets migrated during Saturday dinner service will remember it for years.

For Sales and Account Management, it means the conversations you are having with prospects and renewals now include a hardware transition. I would rather you raise it early and plainly than have a merchant discover it from a support ticket in February.

For Finance, it means a set of decisions Nathan will address in his own memo. I will not get ahead of him except to note that the choices in front of us are genuinely difficult and that I support the direction he is taking.

## The number that should concern all of us

We are currently migrating merchants at roughly 40 per week. To finish 4,100 merchants before March 31, we need approximately 75 per week, sustained, with no lost weeks for holidays, weather, or system issues. We are running at a little more than half the required pace, and we have been at that pace for six weeks.

I want to be careful here. This is not a message about anyone underperforming. The teams doing this work have been methodical and the migrations they have completed have gone well — our rollback rate is under two percent, which is genuinely good. The problem is that the process as designed cannot go faster, and so the process has to change. That is a leadership problem, not an execution problem, and it belongs to me and to the other principals.

Rohan and Kwabena are examining where the throughput ceiling actually sits. My working assumption is that it is a combination of the manual pre-flight check on each merchant's configuration and the fact that we are scheduling migrations one merchant at a time by phone. Both of those are fixable. Neither is fixed today.

## The hardware question

The 900 merchants with unsupported terminals present a distinct problem. Replacement hardware costs money, and the question of who pays it — us or the merchant — is not settled as I write this. Nathan will speak to the economics. What I will say from the product side is that asking a small independent restaurant to absorb an unbudgeted hardware cost in the first quarter, which is the worst cash quarter of the year for New England restaurants, is asking them to consider whether they would rather switch providers than pay us. Some number of them will conclude they would rather switch. I want us to go into that decision with clear eyes about it.

## On the reduction in force

I am not going to pretend the November staffing decision is unrelated to this program. The board approved a reduction of 29 positions this month. Some of those positions are in functions that touch the migration. It would be insulting to everyone's intelligence for me to announce a company-defining program and say nothing about the fact that we are doing it with fewer people.

What I will say is this. The people who are leaving deserve better than to be a line item in a memo about something else, and I will not treat them that way. The people who are staying deserve to know that we understand the arithmetic and are not pretending it works out on its own. It does not work out on its own. It works out only if we change how the work is done, and that is what the next four months are about.

## What I am asking

Three things.

First, if you see a reason the March 31 date might slip or be softened, tell me and let me chase it down, but plan as though it will not. Every hour we spend hoping for an extension is an hour we are not migrating merchants.

Second, if you are in a function that is not obviously on the critical path, ask your manager what the migration needs from you. The answer may be nothing, and that is fine. But I would rather have twenty people ask and hear no than have two people who could have helped sit idle.

Third, be honest about status. I would rather receive bad news in November than accurate news in March. Nobody in this company will be penalized for reporting that something is behind. People will be penalized for reporting that something is fine when it is not.

I will send a program update every two weeks beginning November 20. Kwabena will report on migration pace, Rohan on platform readiness, and Amara on support load. Nathan and I will speak to the financial and commercial picture as it develops.

This is the hardest operational problem this company has faced. I think we are capable of it. I would not have taken the job if I thought otherwise.

— Dolores

---

**TO:** All Employees
**FROM:** Nathan Rosenblum, Chief Financial Officer
**DATE:** November 13, 2026
**SUBJECT:** Revised operating plan — hardware subsidy decision and the November reduction

Dolores wrote last week about the migration program. This memo covers the money, including the two decisions that most affect people at this company: what we are doing about replacement hardware for the 900 affected merchants, and the staff reduction the board approved on November 4.

I am going to lay out the actual numbers rather than summarize them, because I think people make better decisions when they can see the arithmetic, and because a plan that cannot survive being explained is not a plan.

## Where we stand

Quarry Street ends this year at approximately $48 million in annual recurring revenue across 4,100 merchant accounts. Our gross retention has run in the low nineties for three years, which is respectable for a market of independent single-location restaurants. Our net revenue retention is meaningfully better than that because of payment volume growth and module attach, but gross retention is the number that matters for this discussion, because a merchant who leaves takes their hardware decision with them.

We are not in financial distress. We are in a position where a large unbudgeted expense arrives in the same two quarters as our weakest seasonal cash generation and our highest-risk operational program. Those three things overlapping is the whole problem. Any one of them alone would be manageable.

## The hardware decision

The 900 merchants running unsupported terminals need replacement units. Our hardware vendor has given us two prices.

At list, replacing 900 units costs $2.6 million. If we commit by December 15 to a volume purchase of 3,000 units, the same 900 units cost us $1.5 million, and we hold 2,100 additional units against future need. The commitment is firm and non-cancellable; the December 15 date is the vendor's fiscal year end and they have been clear it will not move.

The choice is therefore not between $2.6 million and $1.5 million. It is between:

**Option A.** Buy 900 units at list for $2.6 million, take no inventory risk, decide nothing before December 15.

**Option B.** Commit to 3,000 units for $1.5 million on the 900 we need now, carry 2,100 units of inventory at roughly $1.1 million of capital, and save $1.1 million on the units we actually need.

**Option C.** Buy nothing and pass the hardware cost to merchants at approximately $2,900 per merchant.

I want to address Option C first, because it is the one that looks cheapest on a spreadsheet and is the one I am rejecting most firmly.

Nine hundred of our merchants are independent restaurants, most doing under $1.5 million in annual food and beverage revenue, in New England, in the first quarter. January and February are the months when these businesses discover whether they will survive the year. Presenting a $2,900 unbudgeted hardware invoice in that window, attached to a message that says *this is required or you cannot take cards*, is not a neutral commercial act. It is a moment at which a rational owner asks what a competitor would charge to switch.

I modeled it. If passing the full cost causes even fifteen percent of those 900 merchants to leave, we lose 135 accounts. At our average revenue per account of roughly $11,700 annually, that is $1.58 million of recurring revenue, gone, permanently, plus the payment volume economics that sit on top of it. We would have saved $1.5 million of cash and destroyed more than that in recurring revenue in the first year alone. In year two it is worse, because recurring revenue recurs and a one-time hardware cost does not.

I do not believe fifteen percent is a pessimistic estimate. I think it is close to the middle of the range. Our win-back rate on churned merchants is under ten percent, and a merchant who leaves over a hardware bill leaves angry.

So we are not passing the cost.

## The decision

We are taking Option B. I have authorized the 3,000-unit commitment and Kwabena's team will place it before December 15.

The reasoning is straightforward. We are going to spend the money on hardware either way, and Option B costs $1.1 million less for the units we know we need. The 2,100 additional units are the real question, and I want to be honest that this is where the judgment sits rather than dressing it up as obvious.

My case for the additional inventory: we add roughly 400 to 500 merchants a year, each needing a terminal. We have a replacement cycle across the installed base that consumes several hundred units annually. And the shutdown of the legacy gateway means every terminal in our fleet is now on a known-obsolete platform, which makes me expect elevated replacement demand for the next several years rather than reduced demand. At that consumption rate, 2,100 units is somewhere between three and four years of inventory. That is longer than I would normally accept. It is acceptable here because the alternative is paying an eighty percent premium on the units we cannot avoid buying.

The risk is that the hardware generation is superseded and we are holding obsolete stock. I have asked the vendor for a written commitment on the support life of this terminal generation and have that in hand through 2032. That does not eliminate the risk but it bounds it.

The cash impact is $1.5 million paid in two installments, December and February. We fund it from operating cash and the revolver, and we will draw approximately $800,000 on the revolver in February. We remain within covenant with room to spare. I have walked the lender through this and they are comfortable.

## Merchant contribution

Merchants will contribute $250 per terminal, payable as $25 per month for ten months on their existing invoice, beginning with the month after installation.

I want to explain why this is not zero, because the argument for zero is decent and I considered it.

The $250 is not about the money. Nine hundred merchants at $250 is $225,000, which is real but does not change the shape of the plan. The $250 is about the relationship. A terminal that costs a merchant nothing is a terminal that gets left in a box, installed badly, or treated as disposable. A modest monthly line item on an invoice a merchant already reviews creates a small, useful sense of ownership, and it gives our support team a legitimate reason to follow up on units that never came online.

It is also, frankly, about not setting a precedent that hardware is free. We will be replacing terminals in this fleet for years.

Merchants in genuine hardship may have the contribution waived. Amara's team can approve waivers up to fifty per month without escalation, and I have asked her not to make people beg for it. If a merchant says the $25 is a problem, believe them and waive it. The cost of an unnecessary waiver is $250. The cost of a churned merchant is $11,700 a year.

## The reduction in force

On November 4 the board approved a reduction of 29 positions, fourteen percent of our 210-person headcount. Affected employees were notified on November 11. Severance is eight weeks base plus one week per year of service, with a floor of ten weeks, medical continuation through the severance period, and full vesting acceleration for anyone within ninety days of a cliff. Anyone who wants to discuss their package should come to me directly.

I am not going to write around the difficulty of the composition. Six of the 29 positions are in Merchant Support, reducing that team from 22 agents to 16. This is happening in the same quarter in which we expect support volume to triple.

I have been asked, reasonably, how those two facts sit together. Here is the honest answer, and it is not a comfortable one.

The reduction was driven by a growth plan we set eighteen months ago that we did not hit. We hired ahead of a bookings ramp that came in roughly sixty percent of plan, and we carried that cost for four quarters hoping the ramp would arrive. It did not. By the time we accepted that, our operating margin had gone from modestly positive to meaningfully negative, and we were consuming cash at a rate that would have put us in a covenant conversation by the middle of next year. The board's view, which I share, is that correcting a structural cost problem is not something you defer because the timing is inconvenient. The timing is always inconvenient.

The support reduction specifically was the hardest line in the plan and I argued against it. I lost that argument on the following basis, which I now think was correct: a support organization sized for tripled volume in a four-month migration window is a support organization that is fifty percent overstaffed for the eight months that follow. The right instrument for a temporary volume spike is temporary capacity, not permanent headcount.

So the plan does not ask 16 agents to do the work of 22 agents at triple volume. That would be a fantasy. Instead:

We have budgeted $340,000 for contract support staffing during the migration window, covering approximately eight contract agents from December through April. These are seasonal roles with a defined end date, sourced through a firm we have used before.

We have budgeted $95,000 for the deflection tooling Amara has specified — scheduling self-service, status lookup, and the outbound notification system — which is the work that keeps the calls from arriving in the first place.

We are redeploying four people from functions with reduced load during the migration freeze into support-adjacent roles for the quarter. Two from implementation, two from the product organization.

Total incremental spend on migration support capacity is approximately $435,000 against annualized savings from the reduction of roughly $3.4 million.

I recognize how that reads to the six people leaving support. I am not going to insult them by claiming it reads any other way. What I will say is that the decision was not that their work was unnecessary. The decision was that this company needs to be able to fund its own operations without a financing event, and the path to that ran through a smaller permanent cost base. Those things are both true and one of them is much harder to be on the receiving end of.

## Revised full-year outlook

The revised plan reflects the following changes from the September operating plan: $1.5 million hardware commitment, offset by $225,000 in merchant contributions collected over ten months; $435,000 in incremental migration support cost; $3.4 million annualized savings from the reduction, of which approximately $1.1 million lands in the current fiscal year net of severance; deferral of approximately $600,000 in planned engineering hiring; and a $400,000 reduction in the marketing program budget for the first quarter, on the basis that we should not be generating demand we cannot implement.

We plan to churn 3.5 percent of accounts during the migration window against a normal quarterly rate of 2.1 percent. That is 143 merchants and roughly $1.7 million of recurring revenue. I would rather plan for it and beat it.

We end the fiscal year with approximately $4.1 million in cash and $800,000 drawn on a $5 million revolver. That is tighter than I like. It is not dangerous.

## One last thing

I will get questions about whether the hardware money should go somewhere else. Kwabena will address the specific version of that question in January, because the account team has raised it and it deserves a real answer rather than a dismissal.

My position in advance: the hardware subsidy is not discretionary spending that we chose over some alternative use. It is the cost of our merchants continuing to be able to accept payment. There is no version of this business in which 900 merchants cannot take a credit card on April 1 and we spend the money on something more strategic instead.

My door is open. If you want to see the model, ask and I will walk you through it.

— Nathan

---

**TO:** Merchant Support; Implementation; Account Management
**CC:** Executive Team
**FROM:** Amara Bakr, Director of Merchant Support
**DATE:** November 20, 2026
**SUBJECT:** Support escalation and merchant outreach policy for the migration window (December 1 – April 30)

This memo sets policy for how we handle merchant contact during the migration. It is binding on Merchant Support and on anyone in Implementation or Account Management who touches a merchant during this window. Please read it fully. I have tried to make every rule here explainable, because rules that people do not understand get ignored under pressure, and we are about to be under pressure.

## The situation we are staffing for

We will have 16 agents plus approximately eight contract agents plus four redeployed staff. Call it 28 bodies, of whom fewer than 20 will be fully proficient at any given point. Normal volume is about 1,100 contacts per week. We expect to peak somewhere near 3,300.

Two things follow. First, we cannot handle triple volume by handling calls faster; we handle it by ensuring a substantial fraction of those contacts never happen. Second, we cannot afford to treat every contact as equally urgent, so we are going to make explicit priority decisions rather than implicit ones.

## Priority tiers

Every migration-window contact gets classified into one of four tiers at first touch. The tier determines the response commitment and who owns it.

**Tier 1 — Merchant cannot accept payment.** Terminal is dark, transactions are declining at the gateway, or the merchant is in a post-migration state where card processing is not functioning. Response commitment is fifteen minutes to live human contact, twenty-four hours a day, seven days a week, throughout the window. There is no queue for Tier 1. A Tier 1 contact interrupts whatever an available agent is doing.

I want to be unambiguous about this. A restaurant that cannot take cards during service is losing money by the minute and, more importantly, is having the worst experience a payments vendor can inflict. Every other rule in this memo yields to Tier 1.

**Tier 2 — Migration blocked or failed, merchant currently operational.** Scheduled migration did not complete, pre-flight check failed, replacement terminal did not arrive or will not provision. The merchant can still take payment today but will not be able to after March 31. Response commitment is four business hours, owned by the migration desk.

**Tier 3 — Migration questions and scheduling.** When am I being migrated, what happens, do I need new hardware, what is the $25 charge on my invoice. Response commitment is one business day. The large majority of these should be answered by self-service and never reach an agent.

**Tier 4 — Everything else.** Ordinary support unrelated to migration. Response commitment is two business days, extended from our normal one business day for the duration of the window.

I want to name the cost of the Tier 4 change honestly. We are telling merchants with ordinary problems that they will wait longer. Some will be annoyed. A few will be angry. That is a real cost and I am accepting it deliberately, because the alternative is a queue in which a merchant who cannot take payment waits behind a merchant who has a question about a report.

If you are an agent and you have a Tier 4 contact from a merchant who is clearly distressed, use your judgment and help them. The tiers are a triage instrument, not a permission structure. I would rather you occasionally spend twenty minutes on something out of tier than have anyone in this organization behaving like a machine.

## Escalation

Escalation from Tier 2 to Tier 1 is automatic and requires no approval. If a merchant's situation deteriorates to not-taking-payment, it is Tier 1 immediately.

Escalation to engineering follows a single path. Tier 1 contacts unresolved after thirty minutes go to the platform on-call directly. Rohan has committed to on-call coverage seven days a week through April 30 and has agreed that a Tier 1 page is answered within ten minutes at any hour. Tier 2 items unresolved after four hours go to the migration engineering queue with a named owner.

Escalation to me: any Tier 1 unresolved after ninety minutes, any merchant who states an intent to cancel, any situation involving a merchant losing money that we may be liable for, and anything an agent finds themselves uncertain about at two in the morning. My mobile number is in the on-call directory. Use it. I will never be irritated at being called about a merchant who cannot take payment. I will be irritated to learn on Monday that someone struggled alone on Saturday night.

Escalation to executive: I will bring anything to Dolores that involves more than twenty merchants simultaneously, any regulatory or card-brand exposure, and any single merchant above $75,000 in annual revenue who is at cancellation risk.

## Cancellation intent

If a merchant states an intent to cancel during this window, the agent does not attempt to save the account and does not argue. Log it, tell the merchant that their account manager will call within four business hours, and route to Account Management with the migration context attached.

I am setting this rule because saves attempted by an agent in the middle of a technical conversation are usually bad saves, and because an agent who is measured on resolution time should not also be carrying the emotional weight of a cancellation conversation. Account Management is better at this and it is their job.

## Outreach policy

Deflection is the whole strategy. Here is the outreach sequence for every merchant.

**Sixty days before migration:** Email announcing the program, the March 31 date, whether the merchant needs replacement hardware, and a link to the self-service scheduling tool. Sent in weekly cohorts beginning December 1.

**Thirty days before:** Second email plus, for merchants needing hardware, an outbound call from the migration desk. The call is not optional for hardware merchants — those 900 accounts get a human voice at least twice before their migration date.

**Fourteen days before:** Confirmation of scheduled window, with a preparation checklist. For unscheduled merchants, this becomes an escalating outbound call sequence.

**Two days before:** SMS reminder to the on-site contact, with a reschedule link.

**Day of:** SMS at start of window and at completion, plus an automated post-migration transaction verification. If we do not see a successful card transaction within four hours of a completed migration during operating hours, we call the merchant proactively. This is the single most valuable thing in this policy and I want it protected. Most merchants do not call us when something is subtly wrong; they work around it and quietly resent us.

**Seven days after:** Check-in email with a direct line to the migration desk.

## Scheduling rules

Migrations are scheduled in the merchant's stated low-volume window. For most restaurants this is Monday or Tuesday between 9 a.m. and 11 a.m., or between 2 p.m. and 4 p.m.

No migrations Thursday through Sunday after 4 p.m. No migrations on the day before or the day of a holiday. No migrations during the week of Valentine's Day for any merchant we have flagged as a reservation-driven restaurant, which is roughly 600 accounts and is the single busiest revenue night of the year for many of them. Kwabena's team knows that this constraint costs us a week of throughput. It is not negotiable, and if it means we finish on March 28 instead of March 21, we finish on March 28.

Merchants who have not self-scheduled by 21 days out get assigned a window and told what it is, with a reschedule option. We have to be willing to assign windows. Waiting for universal opt-in will not get us to 75 a week.

## Contract agents

Contract agents handle Tier 3 and Tier 4 exclusively for their first three weeks. They do not take Tier 1. I would rather have a longer queue on scheduling questions than have a merchant in a payment outage talking to someone in their second week.

After three weeks, contract agents who have passed the Tier 2 certification may take Tier 2. Tier 1 remains with permanent staff and the four redeployed internal people, all of whom have Quarry Street product history.

Every contract agent is paired with a permanent agent as a named buddy. Buddies get four hours a week of protected time for this and it is part of their evaluation. I know that adding a coaching load to people who are already stretched is a real ask. It is also the only way this works.

## What I owe you

I will publish a daily dashboard at 8 a.m. — volume by tier, Tier 1 count and resolution times, migrations completed, and any merchant currently in a payment-down state. It goes to the whole company. If we are failing, everyone will be able to see that we are failing.

I am suspending individual handle-time targets for the duration of the window. They are the wrong instrument here and they will make people do the wrong thing.

I am also going to say something about the six colleagues we lost this month. They were good at this work and several of them trained people who are still here. It is not disloyal to them for the rest of us to make this window work; it is the only thing available to us. But I am not going to stand in front of this team and pretend the reduction did not happen or that it did not cost us something real. It did. We are going to do this anyway, and I am going to be honest with you the entire way through about how it is going.

If any part of this policy is getting in the way of taking care of a merchant, tell me and I will change it. Policy is a tool.

— Amara

---

**TO:** Engineering; Platform Reliability
**CC:** Executive Team; Compliance
**FROM:** Rohan Talwar, Head of Platform Reliability
**DATE:** December 4, 2026
**SUBJECT:** October PCI assessment — seven findings, remediation plan, and the key rotation schedule

Our qualified security assessor delivered the October assessment report on November 24. It identifies seven findings. All seven must be remediated and evidence submitted before our next attestation in May 2027.

This memo assigns owners and dates. I want to be direct about the framing first: these findings are not a surprise and several of them are the predictable result of decisions we made to go faster on other things. That is a normal engineering trade and I am not looking to assign blame for it. What I am looking to do is close them, on schedule, in the same quarter as the migration, without letting either program eat the other.

## The findings

**Finding 1 — Encryption key rotation has not been performed since 2023.**

This is the serious one. Our data encryption keys protecting stored cardholder data have not been rotated in over three years. Our documented policy requires annual rotation. We have a policy, we have a procedure, and we did not execute it — twice.

I want to explain how this happened, because the explanation matters for whether it happens again. The rotation procedure requires a maintenance window with write suspension, and it was scheduled and deferred in 2024 for a release, then scheduled and deferred in 2025 during the datacenter move, and then it fell off the calendar entirely because the person who owned the calendar entry left and the ownership transferred to a role rather than a name. A control owned by a role is a control owned by nobody.

There is no evidence of key compromise. We reviewed access logs for the key management service back to 2023 and found no anomalous access. This is a control failure, not an incident. But it is a control failure that a card brand would take seriously, and the assessor has flagged it as the finding most likely to affect our attestation.

Rotation schedule:

- **December 12–19:** Rotation dry run in staging against a full production data clone. I want the timing measured, not estimated. Owner: Priya Venkataraman.
- **January 9, 2027, 1:00 a.m. – 5:00 a.m. Eastern:** Production rotation of data encryption keys, tranche one, covering the primary cardholder data store. Owner: Priya Venkataraman with me on the bridge.
- **January 16, 2027, same window:** Tranche two, covering the tokenization vault and archived transaction store.
- **January 23, 2027:** Verification, re-encryption confirmation across both tranches, retirement of old key versions, evidence package assembled.
- **February 6, 2027:** Key-encrypting key rotation. Separate operation, separate window, deliberately after the data key work is confirmed clean.

I chose January over December for tranche one, and I want to explain why, because it looks like I am delaying an overdue control. Our December change freeze runs December 18 through January 4, covering the holiday period when our merchants do their highest volume of the year. Rotating encryption keys on the primary cardholder store during the freeze is an unnecessary risk for a control that has been open for three years and will not become materially more open in three more weeks. January 9 is the first Saturday after the freeze lifts. I have documented this reasoning for the assessor and they have accepted it.

I am also explicitly protecting these windows from migration work. If a migration issue arises the night of January 9, the migration issue waits. Kwabena and I have agreed on this in advance so that nobody has to negotiate it at two in the morning.

Ongoing: rotation moves to a semiannual schedule, April and October, with a named individual owner and a named backup, both of whom appear by name in the control register. If either leaves, reassignment is part of the offboarding checklist and is blocking. Automated ticket creation 45 days ahead. Rotation status appears on the platform reliability dashboard permanently, so it is visible whether or not anyone is looking for it.

**Finding 2 — Quarterly internal vulnerability scans incomplete for two of four quarters.**

Q2 and Q3 scans covered the application tier but not the full cardholder data environment; the network segment hosting the batch settlement processors was excluded by a scan configuration that was never updated after the datacenter move. Remediation: corrected scope, out-of-cycle full-CDE scan by December 20, remediation of anything found by January 31, then normal quarterly cadence with scope validated against the network diagram each time. Owner: Marcus Oyelaran. This one is straightforward and I expect it closed early.

**Finding 3 — Privileged access reviews not performed for three consecutive quarters.**

We have not conducted documented quarterly reviews of privileged access to the cardholder data environment since Q4 2025. Preliminary review has already found four accounts belonging to departed employees that remained active, and two contractors with standing access beyond their engagement end.

Those six accounts were disabled on November 26. I am not going to characterize this as low-severity. Standing privileged access for departed people is exactly the condition that turns a small incident into a large one.

Remediation: full privileged access review completed by December 22, quarterly reviews with sign-off by the system owner and by me thereafter, and integration of access revocation into the HR offboarding workflow so it is triggered by termination rather than by someone remembering. Owner: Marcus Oyelaran, with Kwabena on the offboarding integration.

I will note without further comment that the November reduction makes the offboarding integration more urgent than it was in October.

**Finding 4 — Log retention below the twelve-month requirement for two log sources.**

Application audit logs and the gateway transaction logs are retained for 90 days in hot storage with no archive. Requirement is twelve months, three months immediately available. Remediation: archive tier to object storage with lifecycle policy, in place by January 15; retention policy documented and applied to all in-scope sources by January 31. We cannot recover the logs already aged out and I have disclosed that to the assessor. Owner: Priya Venkataraman.

**Finding 5 — Change management records missing approval evidence for 23 percent of sampled production changes.**

Our process requires documented approval before production changes. The assessor sampled 60 changes and found 14 without approval evidence. In most cases approval happened in a chat thread rather than the change record.

This is a documentation failure rather than an uncontrolled-change failure, but the assessor cannot distinguish those from the outside and neither, honestly, could we six months from now. Remediation: change tooling enforces approval capture as a blocking gate, effective January 5. Emergency change path documented with a required 24-hour retroactive record. Owner: Kwabena, since this sits in the engineering workflow rather than in mine.

I recognize that adding a blocking gate to the change process during the highest-volume change period in our history is a hard sell. I have thought about it and I still want it, because 23 percent of changes lacking approval evidence during a period when we are touching every merchant's payment configuration is not a position I am willing to be in.

**Finding 6 — Network segmentation testing not performed in the past twelve months.**

Annual segmentation testing validating isolation between the CDE and the rest of the network was not performed in 2026. Remediation: engaged the assessor's testing team for the week of February 15, with results and any remediation by March 31. Owner: me directly. I am scheduling this in February deliberately — after key rotation, before the migration endgame.

**Finding 7 — Security awareness training completion at 71 percent against a 100 percent requirement.**

Annual training for all personnel with CDE access; we are at 71 percent, with the gap concentrated in engineering and implementation. Remediation: 100 percent completion by January 30, enforced by suspension of CDE access on January 31 for anyone incomplete. Owner: Kwabena with People Operations.

I mean the access suspension literally. It is a thirty-minute training module and I am not going to spend my credibility with the assessor defending why senior engineers did not complete it.

## Sequencing against the migration

Everyone reading this has an obvious question, which is how we do all of this during the migration.

Here is my answer. Four of the seven findings — 2, 3, 4, and 7 — are largely administrative. They require careful work and evidence but very little engineering capacity, and they are owned by Marcus and Priya with support from People Operations. They do not compete with the migration for the same people.

Finding 5 is a change to tooling that costs about a week of one engineer's time and then makes everything slightly slower forever. That is real friction during a high-change period and I have accepted it consciously.

Finding 6 is a week of an external team's time in February plus my attention.

Finding 1 is the one with genuine risk of collision, and I have handled it by carving out four specific overnight windows and getting agreement in advance that the migration yields to them. Four Saturday nights in January and early February is the total engineering cost of closing the most serious finding we have. That is affordable.

What I will not do is defer any of this to April on the theory that the migration comes first. Our attestation is due in May. If we arrive in April with seven open findings and a completed migration, we will have traded a deadline we could have met for one we cannot.

I will report weekly on remediation status alongside the platform reliability metrics. If anything slips, you will hear it from me in the week it slips.

— Rohan

---

**TO:** Executive Team; Account Management; All Engineering
**FROM:** Kwabena Asante, Vice President of Engineering
**DATE:** January 15, 2027
**SUBJECT:** Migration status at the halfway point — pace, projection, and the subsidy question

We are ten weeks from March 31. This memo reports where migration stands and then addresses head-on the argument the account team has raised about the hardware subsidy, which deserves a substantive answer rather than a polite deferral.

## Where we are

As of end of day January 14:

- **Merchants migrated: 1,847** of 4,100. Forty-five percent complete.
- **Current weekly pace: 118 merchants**, averaged over the last three weeks.
- **Remaining: 2,253 merchants** across ten weeks. Required pace: 226 per week.
- **Hardware merchants migrated: 291** of 900.
- **Rollback rate: 1.4 percent**, down from 1.9 percent in November.
- **Post-migration Tier 1 incidents: 34 total**, 31 resolved within the fifteen-minute commitment.

We are behind. I want that stated plainly at the top rather than buried after the good news.

Now the good news, which is real. In early November we were at 40 per week against a required 75. Today we are at 118 against a required 226. The gap has widened in absolute terms because the remaining work compressed into fewer weeks, but our throughput has nearly tripled. The question is whether the curve continues.

## What changed

Three things, in order of impact.

The pre-flight configuration check was the ceiling, exactly as Dolores suspected in November. It was a manual review of each merchant's payment configuration, menu structure, and peripheral inventory, taking an engineer 35 to 50 minutes. Two engineers on pre-flight capped us at roughly 45 merchants a week no matter what else improved. We automated 80 percent of that check in December. Configurations now route automatically unless they hit one of eleven exception patterns; roughly 18 percent hit an exception and get human review. Effective pre-flight capacity went from 45 a week to over 300.

Batch migration replaced sequential migration. We now migrate cohorts of 25 to 40 merchants sharing a configuration profile in a single operation. This is where most of the remaining upside sits.

Self-service scheduling worked better than I expected. Sixty-one percent of merchants scheduled their own window without a phone call. Amara's team estimates this alone prevented about 2,400 inbound calls.

I want to be specific about credit here. Priya Venkataraman built the pre-flight automation in eleven days over the holidays. Marcus Oyelaran and Devon Achebe built the batch orchestrator. Amara's team specified the self-service flow and caught two design errors that would have generated more calls than they prevented. This is the best engineering work I have seen this company do.

## Can we finish

Our projection, with the batch improvements fully deployed and a hardware logistics fix I will describe below, is 195 to 240 merchants per week from February 1. At the midpoint of that range we complete approximately 4,050 merchants by March 31 — between 40 and 90 merchants short.

So my honest answer is: probably, narrowly, if nothing goes badly wrong, and with a small residual population needing individual attention in the final week.

I am not comfortable with a plan whose success case is "narrowly." Three actions.

First, we are adding a Saturday-morning migration block beginning February 7, for merchants who are closed or low-volume Saturday mornings — mostly lunch-oriented and breakfast accounts. Approximately 700 merchants qualify. This is voluntary overtime, paid, and I have budget from Nathan for it.

Second, we are pulling forward the hardware merchants aggressively. The 609 remaining hardware merchants are the population most likely to fail on the last day, because they depend on physical delivery, installation, and a merchant being present. Every hardware merchant is now scheduled before March 7, leaving three weeks of buffer. Software-only merchants can be migrated late; hardware merchants cannot.

Third, the hardware logistics fix. Our terminal fulfillment has been the weak point. We were shipping units individually as merchants were scheduled, and our average time from order to installed-and-live has been 19 days against a planned 10. The failure was that we were shipping to the restaurant and waiting for the owner to be present for a scheduled installation call. Beginning January 20, we ship in weekly regional batches to our four implementation partners in Boston, Providence, Hartford, and Portland, who install on a route. Projected time to live drops to 8 days and, more importantly, it stops depending on a restaurant owner answering the phone.

## The account team's objection

The account team has made an argument that I want to state fairly before responding, because I think it has been characterized dismissively in a couple of conversations and it deserves better.

The argument: we are spending $1.5 million on terminals for 900 merchants, roughly $1,670 per merchant, of which they contribute $250. Meanwhile we are projecting 3.5 percent churn during the window, roughly 143 accounts and $1.7 million of recurring revenue. The account team's position is that the same money spent on retention — dedicated account coverage, service credits for disrupted merchants, competitive-response discounting, a rebate program for merchants who stay through the migration — would preserve more revenue than buying hardware for merchants who might churn anyway. Their sharpest version: we are subsidizing hardware for merchants who will leave, and paying nothing to keep merchants who are wavering.

That is a serious argument. It comes from people who talk to merchants every day, and they are right that we have underinvested in the merchant relationship during this program relative to the technical work.

Here is why I nonetheless think it is wrong, in three parts.

**The subsidy and retention spend are not substitutes, because the subsidy is not discretionary.**

The framing treats $1.5 million as a pot of money we chose to spend on hardware and could redirect. It is not. Nine hundred merchants have terminals that stop working on March 31. If we do not replace them, those merchants cannot accept a card payment on April 1. There is no retention program that survives a merchant being unable to take a credit card.

The actual choice was never hardware versus retention. It was who pays for hardware — us or the merchant. Nathan modeled passing the cost through and concluded that a $2,900 invoice in the first quarter would churn at least fifteen percent of that population, which is 135 merchants and $1.58 million of recurring revenue. The subsidy is a retention program. It is the largest retention program in the company's history. It just does not look like one, because it is denominated in terminals.

I would go further: it is a better retention instrument than a discount, because it removes a reason to leave rather than paying someone not to act on one. A merchant who stays for a discount is a merchant who has learned that threatening to leave produces money.

**The volume commitment was the choice, and it was the right one.**

The genuine decision point in December was the vendor commitment. Buying only what we needed cost $2.6 million. Committing to 3,000 units cost $1.5 million. Nathan took the commitment and saved $1.1 million on the units we could not avoid buying, at the cost of holding inventory we will consume over the next three to four years.

If the account team wants to argue we should have taken Option A and had $1.1 million less to work with, that argument runs the wrong direction. The volume commitment is what created room in the plan. Some of that room is funding the contract support agents, the deflection tooling, and the Saturday migration blocks that are the difference between finishing and not finishing.

**The churn we are projecting is mostly not price-driven, and discounts do not address it.**

I asked Amara's team to break down the cancellation-intent conversations logged since December 1. There have been 47. The distribution:

- 21 cited migration disruption or a bad experience — a failed migration, a long support wait, a terminal that arrived late.
- 11 were already in an evaluation with a competitor before the migration began.
- 8 cited business conditions — closing, selling, or cutting costs generally.
- 5 cited cost of our service specifically.
- 2 were unclassified.

The largest category is people we disappointed operationally. A service credit does not fix that; a migration that works fixes that. The second is competitive processes we were probably going to face regardless. The third is not a retention problem at all. Only five of 47 — roughly eleven percent — cited price, and those are the accounts where the account team's instrument would actually apply.

If that distribution holds across the projected 143 churned accounts, price-driven churn is about sixteen merchants and $190,000 of recurring revenue. Spending seven figures to address a $190,000 problem, while the $800,000 problem is operational execution, would be a poor allocation.

**What I think the account team is right about**

Two things.

They are right that we have not funded merchant relationship work commensurate with the disruption we are causing. The migration program has an engineering budget, a support budget, and a hardware budget. It does not have a relationship budget. That is an oversight and it is partly mine.

They are also right that the merchants at highest churn risk are not receiving proportionate attention. Our outreach is uniform by migration date. It is not weighted by account value or by risk. A merchant doing $2 million in volume with a competitive evaluation open gets the same email sequence as a merchant doing $300,000 who is entirely satisfied.

So I am proposing, and Nathan has agreed to fund at $180,000 through April:

A **white-glove tier** for the top 200 accounts by revenue and the 150 accounts flagged as competitive risk. Named migration engineer, scheduled call before and after migration, direct escalation path. Approximately 310 accounts after overlap.

A **service recovery budget** of $75,000 allowing account managers to issue credits up to $1,500 without approval for merchants who experienced a failed migration or an outage. Discretionary, immediate, no forms. When we break something for a restaurant, we should be able to make it right the same day.

**Post-migration outreach at 30 days** for every merchant, weighted by revenue, as a real conversation rather than a survey.

This does not come from the hardware budget. It comes from the engineering hiring deferral Nathan already booked, and I would rather spend it here than backfill a role in the middle of this quarter anyway.

## What I need

From the executive team: hold the March 31 date and do not soften it internally. Every conversation about what happens if we do not finish makes it likelier that we do not finish.

From Account Management: your merchants know things our dashboards do not. If an account is wavering, tell Amara's team before it becomes a cancellation call.

From Engineering: February is the hard month. Key rotation tranches, segmentation testing, the change-approval gate, and peak migration volume all land in the same six weeks. I have looked at the sequencing with Rohan and I believe it fits, but it fits with no slack. If you see something about to collide, say so early. Nobody in this organization will be criticized for raising a problem in February that we could have handled in February.

Next status January 29.

— Kwabena
