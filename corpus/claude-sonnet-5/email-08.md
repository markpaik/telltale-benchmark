# Thread: June 9 Outage — Path Forward

**From:** Simone Beauchamp
**To:** Arun Krishnamurthy, Danielle Okafor, Gabriel Mwangi
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** June 9 Outage — Path Forward
**Date:** June 10, 2026, 7:41 AM

Team,

I don't need to tell anyone on this thread how bad yesterday was. Six hours and fourteen minutes down during the afternoon settlement window, roughly 214,000 declined transactions across 2,400 merchants, and it happened because a database failover we've triggered cleanly a dozen times in testing didn't work in production. I want us aligned before this becomes five separate conversations happening in five different rooms.

I need from each of you, by end of day tomorrow:

Arun — a real accounting of where the migration stands, not the version we've been giving the board. If September is at risk, I need to know now, not in August.

Danielle — anything from Cascadia Trust or from a compliance angle I need to see today, not this week.

Gabriel — what merchants are actually saying, especially the ones threatening to leave or asking for credits.

I'm going to want a single remediation narrative we can put in front of the bank, Timberpine, and everyone else, and I'd rather build it once, carefully, than patch it three times under pressure.

Simone

---

**From:** Arun Krishnamurthy
**To:** Simone Beauchamp, Danielle Okafor, Gabriel Mwangi
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Re: June 9 Outage — Path Forward
**Date:** June 10, 2026, 11:52 AM

Simone,

Straight answer: we are five months behind where the January plan said we'd be. The original target was legacy fully decommissioned by end of April. We're now looking at late September at the earliest, and that assumes nothing else goes wrong, which is a bad assumption given what just happened.

The failover issue yesterday wasn't actually the migration — it was the old stack, which is exactly the problem. We are running dual infrastructure, patching the thing we're trying to retire while building the thing that replaces it, with a platform team that's gone from 19 engineers to 15 since February. Two left for other jobs, one is on leave, and we haven't backfilled because Marcus needed integration engineers on the new merchant deals instead.

If we want September, I need the roadmap frozen. That means no new feature work, no scope additions, and it specifically means the two integrations sales already sold — the loyalty-platform connector for Briarwood and the split-tender work for the regional grocery deal — get pushed. I know that's a real conversation with Marcus and with those customers. I'd rather have that conversation now than explain in October why we're still on legacy hardware when it fails again.

I can have a detailed week-by-week plan by Friday. But I need a decision on the freeze before I write it, because the plan looks completely different depending on how many engineers I actually have.

Arun

---

**From:** Danielle Okafor
**To:** Simone Beauchamp, Arun Krishnamurthy, Gabriel Mwangi
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Re: June 9 Outage — Path Forward
**Date:** June 10, 2026, 2:15 PM

Simone,

Forwarding below — Cascadia sent this at 9 AM. Regina Alvarez is the relationship manager but the letter is signed by their head of merchant risk, which tells you how seriously they're taking it.

Short version: they want a written remediation plan within 21 days (deadline is June 30), they want specifics on root cause and on redundancy, not generalities, and they are explicit that they will pause new merchant boarding until they're satisfied. That's 90 to 130 accounts a month sitting in the pipeline. I don't have to explain what that does to Q3.

They also flagged the outage under their operational risk reporting obligations, which means this isn't just a relationship issue, it's something they may have to disclose upward to their own regulators depending on how it's categorized. That's part of why the tone is what it is.

I'd like to get in front of this rather than react to their deadline. My instinct is we want something on their desk by June 22 or 23, a week ahead of the 21-day mark, so it reads as us being proactive rather than compliant-by-the-skin-of-our-teeth. But I need Arun's real plan to write it, and I need to know if we're committing to redundancy investment, because Cascadia is going to ask specifically whether we have a hot standby or equivalent, and "we're migrating" is not going to satisfy them a second time.

Danielle

---

**From:** Danielle Okafor
**To:** Simone Beauchamp, Arun Krishnamurthy, Gabriel Mwangi
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Fwd: Notice of Operational Risk Concern — Alderpoint Payments
**Date:** June 10, 2026, 2:16 PM

---------- Forwarded message ---------
From: Cascadia Trust Bank — Merchant Risk
To: Danielle Okafor
Date: June 10, 2026, 9:02 AM

Ms. Okafor,

We are writing regarding the June 9 authorization outage affecting merchants processed under our sponsorship. Cascadia Trust Bank requires a written remediation plan within 21 calendar days of this notice, addressing root cause, corrective action taken to date, and a specific description of redundancy measures to prevent recurrence, including timeline and resourcing.

Pending our review of this plan, we are suspending approval of new merchant boarding applications submitted by Alderpoint Payments effective immediately. We understand this affects a meaningful volume of pending accounts and do not take the step lightly, but an event of this duration and scope requires it.

We would welcome a call this week if useful.

Regards,
Merchant Risk, Cascadia Trust Bank

---

**From:** Gabriel Mwangi
**To:** Simone Beauchamp, Arun Krishnamurthy, Danielle Okafor
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Re: June 9 Outage — Path Forward
**Date:** June 11, 2026, 9:03 AM

Morning all,

Numbers as of this morning: 38 merchants have contacted us specifically asking about service credits, out of roughly 60 who've reached out at all. A handful are asking pointed questions about SLA language, which tells me they've had someone read the contract. Our cap under the standard agreement is 10% of that month's processing fees, which for most of these accounts is a few hundred to a couple thousand dollars — not nothing, but not going to move anyone who's genuinely worried about reliability.

Two accounts worth flagging specifically. Timberpine Supply, our fourth largest by volume, has not asked about credits — their ops director called wanting to know if this is a pattern or a one-off, which usually means they're deciding something internally before they talk numbers with us. And a regional pharmacy chain, smaller account, mentioned to their rep offhand that they'd had "a conversation" with a competitor. I don't think that one's serious yet but wanted it on the record.

I'd like guidance this week on two things: what I'm authorized to offer beyond the contractual credit for accounts that are clearly on the edge, and what the company-wide message is. Right now every rep is improvising slightly differently and merchants talk to each other. I'd rather send one clean note to all 2,400 accounts than have this leak out unevenly over the next two weeks.

Gabriel

---

**From:** Simone Beauchamp
**To:** Arun Krishnamurthy, Danielle Okafor, Gabriel Mwangi
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Re: June 9 Outage — Path Forward
**Date:** June 11, 2026, 4:47 PM

Okay. Here's how I want to sequence this so we're not all pulling in different directions.

Arun — freeze is approved in principle. I want the Friday plan to assume the freeze so we can see what September actually looks like with 15 engineers and no new scope. I'll deal with Marcus and the two sold integrations separately, that's not something you need to carry.

Marcus — I know this affects deals you closed. Let's talk tomorrow before I say anything to those customers. I'd rather you and I land on language together than have this come from Arun's team.

Danielle — go ahead and request the call with Cascadia this week, but let's not commit to a specific redundancy number until Arun and I have talked cost and timeline. I don't want to promise something to the bank we then have to explain we can't afford, or that takes longer than we told them.

Gabriel — for now, hold at contractual credits, but flag any account that feels like it's genuinely at risk of leaving, not just annoyed, directly to me. I want to know before it becomes a termination letter, not after. On the company-wide note, give me a draft by Friday. I'd rather it go out once we know what we're actually offering, because right now I don't want to write "we're investing in redundancy" without knowing if that's true yet.

This is going to be a hard three weeks. Let's not make it harder by working around each other.

Simone

---

**From:** Marcus Webb
**To:** Simone Beauchamp
**Cc:** Arun Krishnamurthy
**Subject:** Two integrations — before we talk tomorrow
**Date:** June 12, 2026, 8:15 AM

Simone,

Wanted to get this to you before we're in the room. Briarwood and the grocery split-tender deal aren't abstractions to me, I want to make sure that's understood going in. Briarwood signed in March specifically because we committed to the loyalty connector by Q3, it's in their board deck internally, their VP of digital told our rep that. If we go tell them it's not happening, or even "not happening on the date we promised," that's not a delayed feature, that's a company that made a decision based on our word and now has to explain to their own leadership why it's wrong.

The grocery deal is newer, less baked in, more room to move, but it's also $1.4M in annual revenue we modeled starting in Q4 and if that integration slips past their fall reset window they've told us flat out they'll wait until next spring, which functionally means we lose most of a year of that revenue.

I'm not going to fight you on the freeze itself — I watched yesterday happen same as everyone else, I get why Arun needs his people. But I want us to think hard about whether it's both integrations or whether there's a version where we protect Briarwood, which is the relationship with the most exposure, and push only the grocery deal. I'd rather lose revenue than lose a reference customer who talks to other retailers about us.

Let's talk through options before we decide it's binary.

Marcus

---

**From:** Simone Beauchamp
**To:** Marcus Webb
**Cc:** Arun Krishnamurthy
**Subject:** Re: Two integrations — before we talk tomorrow
**Date:** June 12, 2026, 6:40 PM

Marcus,

Talked to Arun this afternoon. Here's where I've landed, and I want to say it plainly rather than let it get soft in the retelling.

Both integrations move. Not because Briarwood doesn't matter, but because the actual choice in front of us isn't "freeze both" versus "freeze one." It's "freeze the roadmap" versus "risk a second outage while we're still explaining the first one to our sponsor bank." Arun's team is 15 people trying to do 19 people's work while running two production environments in parallel. Any engineer I let you keep on Briarwood is an engineer not finishing cutover work, and cutover work is what stops the next six-hour outage.

What I will commit to: Briarwood gets a new date, and it gets priority the moment the freeze lifts, ahead of grocery, ahead of anything else in the backlog. I want you and me on a call with Briarwood's VP together, this week if we can get it, so it comes from both of us and doesn't sound like sales quietly walking back a promise. I'd rather eat a hard conversation now than a worse one in October.

On grocery — if losing the fall window effectively costs us the deal, I want a real number on that, not the optimistic one, so I can weigh it honestly against outage risk. But my default is it moves too.

I know this isn't the answer you wanted. It's the one I think keeps us out of a second incident.

Simone

---

**From:** Arun Krishnamurthy
**To:** Simone Beauchamp, Danielle Okafor
**Cc:** Priya Chandrasekaran, Marcus Webb
**Subject:** Migration plan — with freeze assumed
**Date:** June 13, 2026, 5:58 PM

Simone,

Here's the plan you asked for Friday, a little early because Danielle needs it for the bank conversation.

With the freeze and 15 engineers dedicated full-time to cutover, legacy decommission is realistic by September 18. That's not a padded date — it assumes no further attrition and it assumes I don't lose anyone to firefighting on the old stack, which is the part I can't fully control.

On redundancy specifically, since I know that's what Cascadia is going to press on: right now we have none for the legacy authorization stack, which is exactly why yesterday turned into six hours instead of six minutes. A proper hot standby environment — separate infrastructure, synchronous replication, automated failover we've actually load-tested — would cost roughly $780,000 annualized and take about 10 weeks to stand up, mostly because of the database replication work and because we'd want to run it through at least two full failover drills before I'd trust it in production.

I want to be direct about the tradeoff. If I put engineers on the hot standby build starting now, in parallel with cutover, September slips — probably to late October, because it's largely the same team doing both. If I wait until cutover is done in September and then build the standby, we're exposed on legacy for another three months with no better protection than we had on June 9. Neither option is comfortable. I don't think there's a version of this where the answer is comfortable.

I'd rather you and I decide this before it becomes a promise to the bank we then have to reverse-engineer a timeline for.

Arun

---

**From:** Priya Chandrasekaran
**To:** Simone Beauchamp, Danielle Okafor, Arun Krishnamurthy
**Cc:** Marcus Webb, Gabriel Mwangi
**Subject:** Re: Migration plan — with freeze assumed
**Date:** June 14, 2026, 10:22 AM

A few things from a legal and contract standpoint before this goes further.

On Cascadia: the sponsorship agreement gives them the right to suspend boarding on reasonable risk grounds, and unfortunately "six-hour outage with a quarter million declines" clears that bar without much argument. I don't think we fight the boarding pause. I think we focus the 21-day submission on demonstrating that we understand root cause and have committed, funded resourcing behind a fix, because that's what gets boarding unpaused, not disputing their authority to pause it.

On the credit cap: the 10% monthly-fee cap is enforceable and I'd resist the instinct to blow past it broadly, because if we do it for one merchant we'll functionally have to do it for all 2,400 or explain very carefully why we didn't, and that's a harder conversation than the one we're avoiding. Where I think we have room is case-by-case commercial gestures outside the credit clause entirely — extended terms, waived fees on something unrelated, that kind of thing — for accounts Gabriel flags as genuinely at risk. That's a business decision, not a contract one, and it doesn't create precedent the way a credit-cap exception would.

On Timberpine specifically, separate from all this: their contract has a termination-for-cause clause tied to service availability commitments, and depending on how their MSA reads I want to look closely before anyone talks to them about numbers. I'll have a memo by Monday.

Priya

---

**From:** Gabriel Mwangi
**To:** Simone Beauchamp, Danielle Okafor, Priya Chandrasekaran
**Cc:** Arun Krishnamurthy
**Subject:** Timberpine — termination notice received
**Date:** June 16, 2026, 8:44 AM

Simone,

It happened. Timberpine sent formal notice this morning — termination for cause, citing the June 9 outage and, worse, referencing "a pattern of service degradation" which I think refers to two shorter incidents in March and April that were minor at the time but are apparently still on their radar. There's a 30-day cure period per their contract, so we have until roughly July 16 before it's final, but their tone is not "let's talk," it's "here's the letter our lawyer told us to send."

This is 8.4% of our processing volume and $2.6 million of annual revenue. It's also a reference account other prospects call for a recommendation before signing, so the damage isn't limited to their number.

Their CFO, Hannah Ostrowski, copied herself on the notice, which I read as a signal she's the one actually driving this, not their outside counsel. I'd like to get ahead of the 30 days rather than wait for their next move. Can we get Priya's read on the cure clause today or tomorrow, and can we figure out what we're actually willing to offer before Hannah calls, because I think she will call, and I'd rather Simone be ready than caught flat-footed.

Gabriel

---

**From:** Priya Chandrasekaran
**To:** Simone Beauchamp, Gabriel Mwangi, Danielle Okafor
**Cc:** Arun Krishnamurthy
**Subject:** Re: Timberpine — termination notice received
**Date:** June 16, 2026, 3:10 PM

Reviewed the MSA. The cure period is 30 days from notice, so July 16, and it requires us to cure "the deficiency giving rise to termination," which their notice frames broadly as inadequate infrastructure redundancy, not just the specific June 9 incident. That's actually useful for us in one sense — it means we can point to a concrete redundancy commitment as cure, rather than needing to prove the outage itself won't happen again, which we obviously can't fully promise.

The risk is that if we can't point to something concrete and funded, "we're working on it" will not read as cure to their counsel, and 30 days runs out fast. I'd treat this as effectively forcing the redundancy decision Arun raised on the 13th — we may not have the luxury of deciding that on our own timeline anymore.

One more thing: their notice references the March and April incidents, which I want to pull the internal reports on, because if those were previously disclosed to Timberpine as resolved and now they're being cited again, I want our story to be consistent about what we said then versus what we're saying now.

Priya

---

**From:** Simone Beauchamp
**To:** Priya Chandrasekaran, Gabriel Mwangi, Danielle Okafor, Arun Krishnamurthy
**Subject:** Re: Timberpine — termination notice received
**Date:** June 17, 2026, 7:55 AM

Understood. Arun, I know I said take the weekend to think about the standby decision, but Priya's right that we may not have that runway with Timberpine. Can you and I talk this morning before I have to be reactive instead of deliberate about this.

Gabriel, when Hannah calls — and I agree she will — I don't want anyone but me on that call, at least the first one. This is a relationship where I think the CFO wants to hear from the CEO, not be routed to account management. Please loop me in the moment you hear from her.

Simone

---

**From:** Hannah Ostrowski
**To:** Simone Beauchamp
**Cc:** Gabriel Mwangi
**Subject:** Redundancy — need something specific
**Date:** June 19, 2026, 11:30 AM

Simone,

I'll skip the pleasantries since we haven't met and get to it. I sent the termination notice because that's what my board and our auditors expect given the exposure, not because I want to leave Alderpoint — you've been our processor for four years and switching costs are real on our side too. But I need something I can bring back to my CFO peers on our board committee, and "we're investigating" isn't it after three incidents in four months.

Specifically: do you have a redundant environment, hot standby, whatever the term is, that would have kept us processing on June 9 even with the failure you had? If yes, when did it go live, or if not yet, when will it, and what's the actual commitment behind that date — not a target, a commitment I can put in a memo to our board with your name on it.

I have until July 16 under the cure clause per your legal team's reading, which I assume matches ours. I'd rather resolve this well before that date than have it come down to the wire. If I don't have something concrete by early July, I have to start actively planning a transition, because I can't wait until the 15th to find out the answer is no.

Hannah Ostrowski
CFO, Timberpine Supply Co.

---

**From:** Simone Beauchamp
**To:** Hannah Ostrowski
**Cc:** Gabriel Mwangi
**Subject:** Re: Redundancy — need something specific
**Date:** June 20, 2026, 5:12 PM

Hannah,

Appreciate the directness, I'll match it.

Today, no, we do not have a hot standby for the authorization stack, and June 9 happened because we did not. I'm not going to dress that up. What I can tell you is that we've approved building one — I finalized this internally yesterday after your notice, if I'm honest, though the work was already being scoped before that. It's a separate environment with synchronous database replication and automated failover, engineered to keep us processing through exactly the kind of failure we had on the 9th. Cost is $780,000 a year to run, and my CTO's honest estimate is 10 weeks to build and validate, which includes running it through actual failover drills before we call it production-ready, not just standing it up and hoping.

10 weeks from this week puts a tested, live standby environment at roughly the first week of September. I know that's after your July 16 cure deadline, and I'm not going to pretend otherwise or ask you to take that on faith without something in between.

What I can commit to in writing before the 16th: a signed statement of work with our infrastructure vendor, dated and funded, with the 10-week build already underway by the time you need to make your decision, plus weekly written status updates to you personally until it's live. I'd rather show you the receipts of an active build in progress than promise you a finished thing I can't deliver by your deadline.

I'd like to get on a call this week if you're open to it. I think this is better said than typed past this point.

Simone

---

**From:** Tom Liu
**To:** Simone Beauchamp
**Cc:** Arun Krishnamurthy
**Subject:** Standby build — cost question
**Date:** June 22, 2026, 9:04 AM

Simone,

Danielle's board update mentioned the $780K commitment for the standby environment. I'm not going to fight you on it, I think it's the right call given Cascadia and Timberpine both, but I want to understand the framing before next week's board call so I'm not caught explaining it cold.

$780K annualized against $3.1B in processed volume is not a big number in isolation. What I want to be able to say is what it costs us if we don't do it — one more outage of this size, in credits, in Timberpine's $2.6M walking, in whatever boarding pause costs us in lost new-merchant revenue while Cascadia sits on approvals. If you can get me a rough number on the other side of that ledger before Thursday, I can carry this to the rest of the board as a straightforward decision rather than a number that needs defending on its own.

Tom

---

**From:** Simone Beauchamp
**To:** Tom Liu
**Cc:** Arun Krishnamurthy, Danielle Okafor
**Subject:** Re: Standby build — cost question
**Date:** June 23, 2026, 6:20 PM

Tom,

Rough math, and I mean rough: Timberpine alone is $2.6M if we lose them, which the standby commitment is directly aimed at preventing. Cascadia's boarding pause, at the low end of 90 accounts a month and a conservative average account value, is somewhere north of $400K a month in delayed new revenue for every month it stays paused — and it doesn't lift until they're satisfied on redundancy specifically, so this isn't a hypothetical, it's the actual key to unlocking that. The June 9 credits alone, even capped at 10%, are running just under $180K across the merchants who qualify, and that's for one incident.

$780K a year to prevent a repeat of any one of those looks inexpensive against that backdrop. I'll have Danielle put a version of this math in the board deck, cleaner than what I just wrote you at 6 PM, so it's not just my numbers.

Simone

---

**From:** Arun Krishnamurthy
**To:** Simone Beauchamp
**Cc:** Danielle Okafor
**Subject:** Standby build — kickoff and sequencing
**Date:** June 24, 2026, 2:37 PM

Simone,

Confirming what we agreed Monday. I'm pulling four engineers onto the standby build starting this week, which does push the legacy decommission date from September 18 to approximately October 30 — I want to be honest that this is the real cost of the sequencing, not a footnote. I don't love pushing the migration further, but I agree it's the right tradeoff given Timberpine's deadline and Cascadia's letter both turning on this specific thing.

Vendor SOW for the replication infrastructure will be signed by Friday, which gives us something dated and real to put in front of Hannah before July 16, and I'll have the first status update format ready for whoever needs to send it to her weekly. First failover drill is targeted for week 7, second for week 9, go-live week 10, which lands right around September 1 if nothing slips. I'll flag immediately if anything does — I'd rather over-communicate on this one than have anyone surprised twice.

Arun

---

**From:** Danielle Okafor
**To:** Simone Beauchamp, Priya Chandrasekaran, Arun Krishnamurthy
**Subject:** Draft remediation letter to Cascadia — for review
**Date:** June 25, 2026, 4:00 PM

Attached is the draft for Cascadia, due to them by June 30 per the 21-day window but I'd like to send by the 27th so it lands with a few days to spare. Structure is: root cause on June 9 specifically, what's changed since, the standby build with the signed SOW as evidence it's real and funded rather than aspirational, and the revised migration timeline including the October 30 decommission date, framed honestly as the cost of prioritizing redundancy first.

I've included the September 1 standby go-live date and October 30 legacy decommission date exactly as Arun gave them, no rounding to make it look better, because I think the credibility of giving them a real date that includes real tradeoffs is worth more than a prettier one that slips. I've also proposed we offer Regina a monthly check-in call through go-live rather than waiting for them to ask for one, partly to keep boarding pause discussions moving in parallel rather than waiting for the full remediation to be "done" before that conversation restarts.

One open question — do we want to request they reconsider a partial lift on boarding, say allowing lower-risk existing-category merchants through while the standby is built, or do we hold off asking until the letter lands and we've had the check-in call. I lean toward asking, framed as a proposal not a demand, since the downside of asking is just "no."

Danielle

---

**From:** Priya Chandrasekaran
**To:** Danielle Okafor, Simone Beauchamp, Arun Krishnamurthy
**Subject:** Re: Draft remediation letter to Cascadia — for review
**Date:** June 26, 2026, 10:15 AM

Read through it. Two edits, both small. First, where you describe the March and April incidents in the background section, I'd soften "unrelated to the June 9 root cause" to "distinct in mechanism from the June 9 root cause" — unrelated is a stronger claim than we can fully back given they were all on the same legacy stack, and if this letter ever gets read next to what we tell Timberpine, I want the language to hold up side by side.

Second, on the partial boarding-lift ask — I'd include it, agree with Danielle, but frame it as contingent on the first monthly check-in going well rather than asking for it in the same breath as the remediation plan itself. Asking for relief in the same letter where we're disclosing we're still five weeks from a tested standby risks reading as presumptuous. Ask for the check-in cadence now, raise boarding at the first one once they've seen we're following through.

Otherwise this is good. Simone, your call on send.

Priya

---

**From:** Simone Beauchamp
**To:** Danielle Okafor, Priya Chandrasekaran, Arun Krishnamurthy
**Subject:** Re: Draft remediation letter to Cascadia — for review
**Date:** June 26, 2026, 3:45 PM

Both edits make sense, please make them and send today rather than waiting for the 30th — I'd rather they have extra runway to read it than us cutting it close.

Danielle, good work pulling this together fast. I know the last two weeks haven't been easy on your team either.

Simone

---

**From:** Gabriel Mwangi
**To:** Simone Beauchamp, Danielle Okafor
**Cc:** Priya Chandrasekaran
**Subject:** Merchant-wide communication — draft
**Date:** June 29, 2026, 1:20 PM

Simone,

Draft below for the note going to all 2,400 merchants. I kept it short on purpose — I think a long explanation reads as defensive, and most of these accounts want to know three things: what happened, what we're doing about it, and what's in it for them if they were affected.

---

Subject: An update on the June 9 service disruption

To our merchants,

On June 9, a failure in our legacy authorization infrastructure caused an outage lasting just over six hours during the afternoon processing window. If your business was affected, you have our sincere apology — we know what a disruption like this costs you, not just in declined transactions but in trust with your own customers.

Here is what we're doing. We've committed to building a fully redundant standby processing environment, funded and already under construction, targeted to be live and tested by early September. In the meantime, we've accelerated our broader infrastructure migration to reduce reliance on the systems involved in this incident.

If your account was affected by the June 9 outage, a service credit consistent with your agreement has been or will be applied automatically to your next statement — you do not need to request it. If you have questions about your specific account, your account manager is available directly.

We take this seriously, and we're grateful for your continued trust while we make these systems better.

Simone Beauchamp
CEO, Alderpoint Payments

---

Let me know what you'd change. I'd like to send by Wednesday so it doesn't look like it took us three weeks to say anything, even though realistically that's about right.

Gabriel

---

**From:** Simone Beauchamp
**To:** Gabriel Mwangi, Danielle Okafor, Priya Chandrasekaran
**Subject:** Re: Merchant-wide communication — draft
**Date:** June 29, 2026, 6:50 PM

This is close. Two changes. Cut "your continued trust while we make these systems better" — it reads like we're asking them to be patient with an ongoing problem, and I'd rather the note end on what we've already done than what we're still working on. Something closer to "we're committed to being a partner you can rely on going forward" — forward-looking without sounding unfinished.

Second, I want the credit line to say explicitly that it's automatic and already calculated, not "has been or will be," pick one — Danielle, is it done yet? If not, let's hold the send until it actually is, because I don't want 2,400 merchants checking a statement and not finding it there yet.

Otherwise, send Wednesday. Good work, Gabriel, this whole thing has needed exactly this kind of plain, short writing and most of what's crossed my desk this month hasn't been.

Simone

---

**From:** Danielle Okafor
**To:** Simone Beauchamp, Gabriel Mwangi
**Subject:** Re: Merchant-wide communication — draft
**Date:** June 30, 2026, 9:10 AM

Credits are calculated and queued to post with next billing cycle, which for the majority of affected accounts is July 3. Gabriel, safe to say "has been applied" for anyone billed before the 3rd is not accurate, so let's use "will be applied to your next statement, no action needed on your part" — true for everyone regardless of billing date, and still reads as automatic and already handled procedurally, which is the part that matters.

Sent the Cascadia letter yesterday as planned, ahead of the 21-day deadline. Regina acknowledged receipt this morning and proposed the first monthly check-in call for July 10.

Danielle

---

**From:** Hannah Ostrowski
**To:** Simone Beauchamp
**Cc:** Gabriel Mwangi
**Subject:** Re: Redundancy — need something specific
**Date:** July 6, 2026, 2:44 PM

Simone,

Following up after our call last week and the SOW documentation you sent over. I took it to our board committee Friday. It wasn't a unanimous "stay," I'll be honest, a couple of members wanted to see the standby actually live before we withdraw the notice. But the combination of a signed, funded contract with a real vendor and dates, plus weekly updates that have actually been showing up on schedule the last two weeks, was enough to get majority support for staying, conditioned on continued weekly reporting through go-live and a right to revisit if the September date slips.

I'm formally withdrawing the termination notice as of this email. I want to be clear this isn't me saying June 9 didn't matter or that I've forgotten March and April — it's that you gave me something specific when I asked for something specific, and that's rarer than you'd think in this industry.

I'd like the credit language and any commercial terms formalized in writing so I have it for our file, and I'll want to be on the list for the failover drill results in weeks 7 and 9, not just the go-live announcement.

Hannah

---

**From:** Priya Chandrasekaran
**To:** Simone Beauchamp, Gabriel Mwangi, Hannah Ostrowski
**Subject:** Re: Redundancy — need something specific
**Date:** July 7, 2026, 11:00 AM

Hannah,

Glad to have this resolved. I'll prepare a short amendment to your MSA documenting the withdrawal of the termination notice, the weekly reporting commitment through standby go-live, and the September 1 target with the right to revisit you mentioned if it slips materially. Should have a draft to you by end of week for your counsel to review alongside ours.

Priya Chandrasekaran
General Counsel, Alderpoint Payments

---

**From:** Simone Beauchamp
**To:** Arun Krishnamurthy, Danielle Okafor, Gabriel Mwangi, Priya Chandrasekaran, Marcus Webb
**Subject:** Where we landed
**Date:** July 10, 2026, 5:30 PM

Wanted to close the loop on this now that the pieces have settled, since it's been a month of a lot of moving parts and I don't want the lessons to get lost once things calm down.

Cascadia's remediation letter went out ahead of deadline and the first check-in call happened today — Regina indicated boarding could resume in phases once we hit the first successful failover drill in a few weeks, which is sooner than I expected. Timberpine withdrew termination, contract amendment is in process. The roadmap freeze held — both integrations are pushed, Briarwood has a firm new date and Marcus and I spoke to their VP together, which I think mattered. Standby build is on schedule for early September, legacy decommission now targets October 30, which is later than we wanted five weeks ago but is honest about what redundancy-first actually costs. Merchant-wide note went out July 1, credits posted July 3, and Gabriel's team hasn't flagged any new at-risk accounts since.

None of this makes June 9 okay. But I think we handled the five weeks after it about as well as we could have, and a lot of that is because everyone on this thread told me the real number instead of the comfortable one, starting with Arun on day one. I'd like to keep that habit past this specific fire.

Thank you all. Let's talk Monday about what we do differently so we're not writing this same thread again in a year.

Simone
