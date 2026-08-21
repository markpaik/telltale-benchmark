# Re: June 9 outage — where we stand

---

**From:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**To:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>
**Cc:** Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** June 9 outage — where we stand
**Date:** Tuesday, June 10, 2025, 7:12 AM

Everyone,

I was on the phone until eleven last night and I'm going to be on it again this morning, so I want to get this thread started before the day eats it.

Yesterday we were down 6 hours and 14 minutes, from 12:46 to 19:00, right through the settlement window on a Monday. Arun's early number is 214,000 declined authorizations. That is not a blip. That is a full afternoon where a merchant in Bend could not take a card, and the reason they could not take a card is us.

I don't want a post-mortem in this thread. Arun, do that separately and do it properly, and I want it written for an audience that includes Cascadia's risk committee because that is where it is going to end up. What I want here is the decision set. As of this morning I count five things we have to land and land quickly:

What we send the sponsor bank, and when.

What we do about the merchants who are already asking for money, and the ones who haven't asked yet but will once this is in the trades.

Whether the migration timeline changes, and if it does, what falls off the roadmap to pay for it.

Whether we commit to redundancy in a form that is contractually meaningful, and what that costs.

What the rest of the book hears, and whether we say it before or after we say it to Cascadia.

I have opinions on most of these and I am going to keep them to myself for about forty-eight hours because I would rather hear what you actually think than watch you all agree with me. Arun, I need your honest read on the migration by end of day tomorrow. Not the read you'd give the board. Danielle, assume Cascadia is going to write to us and tell me what you think it says. Gabriel, give me the merchant picture including anyone we think is a flight risk, not just the ones who've called.

One thing I'll say now so nobody is guessing. I am not interested in a version of this where we tell Cascadia one story and our merchants another and hope the two never meet. They will meet. They always meet.

Simone

---

**From:** Arun Krishnamurthy <arun.k@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Wednesday, June 11, 2025, 6:48 PM

Simone,

You asked for the honest read. Here it is, and I'd ask everyone to read the whole thing before reacting to any one line of it.

The failover failed because the standby database had drifted out of sync with primary and the health check we use to gate promotion checks liveness, not replication lag. So the standby answered "I'm here" and got promoted, and it was eleven minutes behind. We caught that at 13:04, eighteen minutes in, and then spent four hours reconciling before we could safely take traffic again, because promoting a stale replica in an authorization path means you can double-auth or drop auths and we did not know which we'd done until we'd walked the logs. The remaining time was staged traffic restoration. I'm not going to sugar-coat the eleven minutes of drift. That's a monitoring gap we've known about. It was on the backlog. It was below the line.

Now the migration.

We started in January with a plan that said eleven months, done by November. We are five months behind that plan, which means the honest completion date on the current trajectory is somewhere in the second quarter of next year. I know that's not what anyone wants in writing. It's true.

Two reasons and neither is mysterious. The first is that we lost four engineers off a nineteen-person platform team — Devesh and Marta to the same company in Seattle in February, Ray in April, and Callum's last day was three weeks ago. We are fifteen. Two of the four were the people who understood the old authorization stack best, which is the thing we are migrating *off*, which means the migration got slower by more than the headcount math suggests. The second reason is that we have shipped, since January, the Shopify connector, the Level 3 data enhancements, the new chargeback portal, and about forty percent of the tokenization vault work. All of those were roadmap commitments and every one of them came out of the same fifteen people.

You can have the migration finished by end of September. I believe that with the team I have, and I'll put my name on it. The price is that every feature commitment on the roadmap freezes from now until we're done. All of it. That includes the NetSuite integration and it includes the Lightspeed connector, both of which Priya's team has sold and both of which have contractual delivery dates in Q3.

I want to be precise about what "freeze" means because last time we used the word it got negotiated into confetti. Freeze means: no new feature work, no "small" enhancements, no discovery spikes for 2026 planning, no partner-facing pilots. It means the platform team works on migration and on the reliability gaps the outage exposed, and nothing else. Bug fixes and security patches obviously continue. Anything that isn't one of those three things comes to me and I say no.

If we don't freeze, I can't give you September and I won't pretend to. I can give you "sometime in the first half of next year" and a team that is going to lose two or three more people, because the ones who are left are the ones who have been carrying this since February and they are tired in a way that a bonus does not fix.

On the redundancy question, since I know it's coming. A true hot-standby environment — full second region, active-active for the auth path, independently exercised failover — is $780K a year in infrastructure and licensing, and ten weeks to build assuming we have people to build it. We do not currently have people to build it. If we do redundancy and the migration at the same time with fifteen engineers, we do both badly and I'd rather do neither than that.

There is a cheaper middle. About $210K a year gets us proper replication-lag gating, automated failover testing on a weekly cadence, and a warm standby that would have turned Monday into a forty-minute incident instead of a six-hour one. It is not hot-standby. It would not have made Monday invisible. It would have made Monday survivable. Six weeks, and it can share people with the migration because it's the same infrastructure work.

I'd rather we told Cascadia and Timberpine the truth about that distinction than sold them a word.

Arun

---

**From:** Danielle Okafor <d.okafor@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>; Arun Krishnamurthy <arun.k@alderpointpay.com>
**Cc:** Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Thursday, June 12, 2025, 9:31 AM

Simone,

You asked me to guess what Cascadia would write. I don't have to guess anymore. It came in at 4:40 yesterday afternoon, signed by Ellen Sarkisian, and I've attached it. The short version for people who won't open the PDF:

They want a written remediation plan within 21 days of the letter date, so by July 2. They want root cause, corrective actions with owners and dates, a description of our resiliency architecture including recovery time and recovery point objectives, and evidence of testing. They reference our sponsorship agreement section 8.3, which is the operational-standards clause, and they use the phrase "material operational deficiency," which is a term of art and not a compliment.

And in the second-to-last paragraph they say that pending review of the plan they "may elect to suspend approval of new merchant applications." Not will. May. That's a lever they're showing us, not one they've pulled.

New boarding is 90 to 130 accounts a month. Tom can price that better than I can, but if boarding stops for a quarter we are not just losing that quarter's accounts, we're losing the compounding, and we're losing them to competitors who will happily tell the prospect why Alderpoint isn't boarding right now.

A few things about how I'd handle this, and Arun I want to flag that some of this cuts against what you wrote.

First. The single worst thing we can do is send Cascadia a plan that is more confident than our actual capability. Ellen has been doing this for twenty years. If we write "hot standby, active-active, sub-minute failover" and she asks what our current failover test cadence is and the answer is "we don't have one," we don't just lose the plan, we lose the ability to be believed on anything else for the rest of the relationship. And we are going to need to be believed later, because there will be a later.

Second, and Arun this is the part that cuts. Your $210K middle option is, I think, the right engineering answer and I'd support it on the merits. But there is a version of the letter we send that describes it and Cascadia reads it as "they've chosen the cheap option after a six-hour outage." Framing matters enormously here. If we present it as a phased program — phase one is the reliability work, sequenced first *because it comes first*, phase two is a full resiliency review at migration completion with a decision point on further investment — that is a defensible posture and it happens to be true. If we present it as "here's what we're doing, $210K," it reads as a budget decision. Same facts. Very different letter.

Third. I'd like us to volunteer something they haven't asked for. A monthly written operational report to Ellen's team for the next four quarters, with uptime, incident counts, and progress against the remediation milestones. Nobody makes you do that. Doing it voluntarily changes the relationship from supervision to partnership, and it costs us a few hours a month.

Fourth, on timing, and this is where I most want to be heard. The letter is dated June 11. Twenty-one days is July 2. I want to send it by June 27 at the latest and I want it in Ellen's hands with a phone call from Simone the same day, not a PDF landing cold in her inbox on a Wednesday afternoon. Regulators and sponsor banks read early submissions as control. Late-and-perfect is worse than early-and-honest, every time.

One last thing. Arun, in the post-mortem, I need the replication-lag issue described as a known gap that was prioritized below other work, with the date it was first logged. Not softened. If it's in the backlog with a date and we characterize it as a surprise, and that ever surfaces — in a regulatory exam, in discovery, anywhere — we're finished. The truth is survivable. Getting caught shading it is not.

Danielle

---

**From:** Gabriel Mwangi <g.mwangi@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Thursday, June 12, 2025, 4:55 PM

Hi all,

Merchant picture as of close of business today. My team has now spoken to 340 accounts, prioritized by volume.

38 have formally asked about service credits. Under our standard MSA the cap is 10% of that month's fees, which for most of these accounts is somewhere between $180 and $2,400. Total exposure if every one of the 38 gets the full cap is about $61,000. If the whole book asked, it's roughly $340,000 for the month. Tom should confirm.

I want to say something about that $61,000 because I think it's about to become the least interesting number in this thread. Almost nobody who's called us is calling about money. I've listened in on eleven of these calls. What they say, over and over, in different words: *I couldn't take payments on a Monday afternoon and nobody told me what was happening.* Our status page didn't update until 14:20. That's an hour and thirty-four minutes after the first decline. Some of these merchants found out from their own customers standing at the counter.

Three merchants brought up their contract renewal without being asked. Two of those renew in Q4.

The one I'm most worried about is Timberpine Supply Co. They're 8.4% of our volume, $2.6M of annual revenue, and they're by a distance our largest single relationship. Their CFO is Hannah Ostrowski and she is smart, direct, and does not do small talk. Her ops director called us at 13:15 on the 9th — before our status page said anything — and got told by our tier-one queue that we were "investigating reports of intermittent issues." That was the phrase. She has repeated that phrase back to me twice.

Timberpine did somewhere around $890K in attempted volume during the window. They're a wholesale distributor, so a lot of that came back the next day, but their Monday-afternoon slot is when their retail customers place restock orders and they lost some of that permanently. I have not had a number from them.

I don't think Timberpine is going to be solved with a credit. I think they're going to want to know what specifically changes so it doesn't happen again, and I think "we're working on it" ends that relationship.

Simone, a request. Whatever we decide, decide the messaging fast. My team is currently improvising, which means twelve people are each inventing slightly different versions of what we're doing about this, and by next week those versions will be in twelve different merchants' inboxes and one of them will be forwarded to a competitor. I would rather have an imperfect script Monday than a perfect one on the 25th.

Gabriel

---

**From:** Tom Vasquez <tom.vasquez@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Friday, June 13, 2025, 8:04 AM

Numbers, since several are floating around unattached to anything.

Gabriel's credit figures are right. Full-cap for all 38 is $61,400. Whole book at cap is $338,000, one-time.

Boarding suspension. Average new account contributes about $3,100 in first-year revenue, ramping. 110 accounts a month at the midpoint. One quarter of suspended boarding is roughly $1.0M of first-year revenue we never book, and because these compound, the three-year effect is closer to $2.8M. That is materially larger than every other number in this thread except Timberpine.

Timberpine is $2.6M annual, 8.4% of volume. Our contribution margin on them is thinner than average because of their pricing tier — call it $840K a year of contribution. Losing them also means losing the reference, and they are the logo we lead with in wholesale distribution.

Redundancy. Arun's $780K is an annual run-rate, and I want everyone to be clear that's on top of the $210K warm-standby number, not instead of it — the warm standby work is a prerequisite either way. So the full hot-standby path is roughly $990K in year one and $780K annually thereafter, against EBITDA that was $4.1M last year and is tracking to $3.6M this year before any of this.

I'm not saying we can't afford it. I'm saying if we commit to $780K a year in a contract with Timberpine, we should do it because it saves the relationship and we've decided that's worth it, not because it sounds reassuring in an email. And if we commit it to Timberpine we will end up giving it to everyone, because Timberpine's contract terms have a way of becoming the market's terms about ninety days after they're signed.

Tom

---

**From:** Priya Raghunathan <priya.r@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>; Arun Krishnamurthy <arun.k@alderpointpay.com>
**Cc:** Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Friday, June 13, 2025, 11:47 AM

I've been quiet because I've been counting what a freeze actually costs, and I have it now.

Arun, before anything else: I'm not going to fight you on the freeze. I've read your note three times and the part that landed is that four of nineteen left and two of them were the people who knew the old stack. I don't think there's a version of this where we get September without stopping. So take the argument you were bracing for and set it aside.

Here's what stopping costs, precisely, so nobody is surprised in October.

The NetSuite integration is sold to nine merchants, contractually committed to four of them with delivery dates between August 15 and October 1. Combined annual revenue across the nine is $1.8M. Two of the four contracted ones have termination rights if we miss delivery by more than sixty days. One of those two is Kestrel Outfitters, $310K a year, and their COO has already emailed me twice this month about timeline.

Lightspeed is sold to six merchants, contracted with two, delivery committed for September 30, $740K combined. No termination rights, but the two contracted ones have fee abatement clauses that kick in at day thirty of delay — about $4,000 a month combined, which is annoying rather than dangerous.

So the freeze puts roughly $2.5M of merchant relationships into "we told you a date and we're missing it," with about $310K of that at real termination risk.

Two things I want in exchange, and I mean in exchange, not as a favor.

First. I need to tell these merchants a new date, and it has to be a date Arun will actually hold. Not "Q4." Not "as soon as the migration completes." A date. If the answer is January 31 then I will go tell nine merchants January 31 and I will take that conversation, but I will not go tell them a date that moves again in November, because the second slip is the one that loses accounts. The first slip is disappointing. The second one means we're not serious.

Second. When the freeze lifts, NetSuite is first out of the gate. Not renegotiated, not reprioritized against whatever 2026 planning produces. First. I'd like that written down somewhere other than this email.

One more thing that's going to be unpopular. If we're freezing the roadmap and we're going to be down a boarding channel for some period and Timberpine may walk, then the sales team's number for the second half needs to change, and I'd rather change it now with a reason than miss it in December with an excuse. I'll bring a revised model on Monday.

Priya

---

**From:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**To:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Saturday, June 14, 2025, 8:22 AM

Read all of it twice. Some decisions, some still open.

Decided.

The roadmap freezes. Effective Monday, June 16. Arun owns the exception process and the answer is no unless it's a bug, a security patch, or migration work. Priya, that includes exceptions I ask for, and I want Arun to tell me no in front of all of you if I try it. Target for migration completion is September 30. Arun, I'm holding you to that and I'm also going to make sure you have what you need to hold it, which we'll talk about separately because I think fifteen engineers with no contractors is not a plan, it's a hope.

Priya, NetSuite is first out when the freeze lifts. That's now written down. And yes to the revised model Monday.

Gabriel, you get a script by Tuesday. You're right that improvisation is the bigger risk.

Danielle, we send by June 27 and I'll make the call to Ellen myself. Draft it the way you described — phased program, phase one sequenced first because it comes first, phase two a decision point at migration completion. And yes to the voluntary monthly reporting. That was the best idea in the thread.

Still open, and I want more argument on these.

The redundancy commitment. Arun makes an engineering case for the $210K path and Tom makes a financial case against the $780K one and I find both persuasive and neither sufficient, because neither of you is answering the question I actually have, which is: what do we say to a merchant who asks "will this happen again?" We cannot say no. We can say what we've done and let them judge. Is that enough for Timberpine? I don't know yet.

Service credits. Gabriel, I want to propose something and I want to be argued out of it if it's wrong. I don't want to pay the contractual cap. I want to pay more than the cap, unprompted, to every affected merchant, and I want to do it before anyone else asks. Tom, that's $338K at cap, so call it $500K if we go to roughly 15%. The argument for is that the cap is what we owe and going past it is the only unambiguous signal we have that we know this was our fault. The argument against is that it sets a precedent and Tom will tell me we can't afford it. Tell me why I'm wrong.

One thing that is not open. Nobody in this company describes June 9 as an "intermittent issue" ever again. Gabriel, tell your tier-one team that phrase is retired. If a merchant calls and we're down, we say we're down.

Simone

---

**From:** Gabriel Mwangi <g.mwangi@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Monday, June 16, 2025, 5:38 PM

Simone, all —

Two things and the second one is bad.

First, on the credits. I think you're right and I'd go further in a different direction than more money. Paying 15% instead of 10% is a gesture merchants will notice for about a day. What they'll remember for a year is whether we told them the truth about what happened. I'd rather spend $340K at the cap and send every affected merchant a plain-English account of the failure — what broke, why it took six hours, what we're changing — signed by Arun, than spend $500K and send a paragraph of PR. If we can do both, do both. But if I had to pick, pick the letter.

Second. Timberpine served a termination-for-cause notice this afternoon. It came to me and to our legal address, dated today, citing the material-service-failure clause, with a 30-day cure period. Cure window closes July 16.

I've attached it. Hannah Ostrowski is copied on it and so is their outside counsel, which tells you they had this drafted before today.

I called Hannah at 4:15. She took the call, which I'm choosing to read as a good sign. Roughly what she said, and I wrote it down right after:

She said the notice is not a decision, it's a deadline. She said they've been with us four years and would prefer not to move, because moving is nine months of pain for them and she knows it. And then she said — this is close to verbatim — "I need to be able to tell my board that a specific thing changed. Not that you're sorry and not that you're working on it. A specific thing, in the contract, with a number attached."

I asked what specific thing. She said she'd tell us directly and asked to be added to whatever conversation we're having. I said I'd ask.

Simone, I think we should add her. I know that's unusual. But she's going to form a view of whether we're serious in the next two weeks and I'd rather she formed it from watching us work than from a summary I write afterward.

Gabriel

---

**From:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**To:** Gabriel Mwangi <g.mwangi@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Monday, June 16, 2025, 7:02 PM

Set up the call. Wednesday if she's free, and I want her on it, not a summary of her.

Danielle, before Wednesday I need to know: does anything we say to Hannah create exposure with Cascadia, or vice versa. If we commit something to Timberpine that we haven't put in the remediation plan, or the reverse, I want to know that before I say it and not after.

Arun — hard question and I want a hard answer. If we committed to hot standby contractually, ten weeks build, when does it actually exist? Not when it's funded. When does it take traffic in a real failover test?

Gabriel, you're right about the letter versus the money. We'll do both if we can and if we can't, we do the letter.

Simone

---

**From:** Arun Krishnamurthy <arun.k@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Gabriel Mwangi <g.mwangi@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Tuesday, June 17, 2025, 7:15 AM

Hard answer.

If we sign today and start today with the team I have, hot standby takes traffic in a verified failover test in the last week of August. Ten weeks build is real. But it consumes four of my fifteen engineers for that whole period, and those four are the infrastructure people, who are also the people doing the migration's cutover work. So the September 30 migration date becomes December, minimum.

I want to be very clear that this is not a scheduling preference. Those are the same four people. There is no version where they do both.

If instead we do the $210K warm standby, that's six weeks, so it's live and tested by the first week of August, it uses two engineers not four, and it shares infrastructure work with the migration so it costs the migration about ten days, not eleven weeks. September 30 survives. And then hot standby becomes a Q4 project on a rebuilt team, which is when I'd want to do it anyway, because building a second region on top of a stack you're actively migrating off is building it twice.

That last point is the one I'd put in front of Hannah. It is not a cost argument and it isn't a dodge. Building full redundancy for the legacy stack means building infrastructure we are going to throw away in five months. The engineering-correct sequence is: fix the failover gap now, complete the migration, build hot standby on the new platform where it will last. If we do it in the other order we spend $990K on something with a five-month lifespan and we delay the thing that actually reduces risk.

What I can commit to, and mean:

Warm standby with replication-lag gating, live and tested by August 8. Automated failover testing weekly from that date, with results in Danielle's monthly report to Cascadia. Recovery time objective of 30 minutes for the auth path, down from what was effectively undefined. Status page automation so a merchant knows within four minutes, not ninety-four.

And a contractual commitment to hot standby on the new platform, with a defined delivery date — I'd say March 31 — and a service credit that bites if we miss it. Not a promise. A date with a penalty.

If Hannah wants a number in a contract, that's the number I can stand behind. If we give her August for hot standby we will miss it, and missing a written commitment to Timberpine after this is worse than not making it.

Arun

---

**From:** Danielle Okafor <d.okafor@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Tuesday, June 17, 2025, 2:20 PM

Simone, to your question about crossing exposure. Yes, and here's the specific shape of it.

Whatever we commit to Timberpine has to appear in the Cascadia plan, and the dates have to be identical to the day. Ellen's team will eventually see the Timberpine amendment — either because Timberpine's counsel references it, or because it shows up in an exam, or because we're obliged to disclose material contract amendments with our largest merchant under section 11.2. If the Cascadia plan says warm standby by August 8 and the Timberpine amendment says something warmer, we have a problem that is much larger than either commitment.

So my recommendation is that we write one set of commitments and use it in both places. Same milestones, same dates, same language. The Timberpine amendment adds financial consequences that Cascadia doesn't get, which is fine and normal. But the underlying facts must be one set of facts.

Second point, and it's the one I'd most like Simone to hear before Wednesday. Arun's March 31 hot-standby commitment with a penalty is genuinely strong from a compliance standpoint, stronger than a vaguer promise of something sooner. Sponsor banks and examiners have seen a thousand remediation plans and they can smell an aspirational date. A plan that says "we are deliberately sequencing this way, here is why, here is the interim mitigation, here is the dated commitment with consequences" reads as an organization that understands its own risk. A plan that says "hot standby immediately" reads as an organization reacting.

Third, and I'm sorry to add work. Arun, I need the replication-lag ticket number and the date it was opened for the plan. I asked last week. I need it this week.

Danielle

---

**From:** Arun Krishnamurthy <arun.k@alderpointpay.com>
**To:** Danielle Okafor <d.okafor@alderpointpay.com>
**Cc:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Tuesday, June 17, 2025, 3:44 PM

PLAT-2291. Opened August 14, 2023, by Marta. Reprioritized below the line four times, most recently in the January planning round when we moved everything that wasn't migration or committed roadmap into the backlog.

It's mine. I did the reprioritizing. Put it in the plan exactly that way.

Arun

---

**From:** Hannah Ostrowski <h.ostrowski@timberpinesupply.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Thursday, June 19, 2025, 9:05 AM

Simone, Gabriel,

Thank you for yesterday's call and for including me. I've been on the other side of enough vendor incidents to know that being invited into the working conversation rather than the managed one is not the default, and I noticed.

I want to put in writing what I said, because I'd rather you respond to something precise than to my tone.

Timberpine lost approximately $890,000 in attempted volume on June 9. We've now reconciled and the permanent loss is $214,000 — restock orders that went to two of our competitors and, in four cases, appear to have stayed there. That's the number I care about, not the gross.

But I want to be clear that we did not send a termination notice over $214,000. We sent it because on June 9 our operations director called your support line at 13:15 and was told you were investigating reports of intermittent issues, at a moment when your authorization platform had been fully down for twenty-nine minutes. Somebody at your company knew. The person on the phone with us either didn't know or wasn't allowed to say. Both of those are worse than the outage.

I've read Arun's sequencing argument, which Gabriel forwarded with your permission. I want to say something that may surprise you: I find it persuasive. Building full redundancy on a platform you're retiring in five months is a waste of money, and if you had told me you were doing it I would have wondered whether you were making engineering decisions or public relations decisions. The argument for doing the interim work first and the permanent work on the new platform is the argument I would make in your position.

So my problem is not the plan. My problem is that I have no basis to believe the plan will happen, because the last plan you told us about — the migration you announced in January and described to us as an eleven-month program — is, I now understand, five months behind schedule, and nobody told us that either. I found out from this thread.

That's the thing. It isn't the outage. It's that we've been a customer for four years and we learn what's actually happening at Alderpoint by being cc'd on an internal email chain.

Here is what would let me tell my board to withdraw the notice. Four things.

The commitments Arun described, in an amendment to our agreement, with dates. Warm standby and failover gating live and tested by August 8. Weekly automated failover testing from that date. A 30-minute RTO for authorization. Hot standby on the new platform by March 31. If those are the right dates, put them in the contract.

Service credits that mean something. Our cap is 10% of monthly fees, which for June is about $21,000, against $214,000 of permanent loss. I'm not asking you to cover the loss. I'm asking you to change the cap prospectively — to 25% for any incident over two hours — because a 10% cap on a six-hour outage tells me the contract was written on the assumption this wouldn't happen, and now we both know it can.

Notification obligations. If authorization is degraded for more than fifteen minutes, we get a direct notification to a named contact at Timberpine, not a status page. And your support staff are permitted to say "we are down." I'd like that written as an obligation, not a courtesy.

The March 31 date carries a penalty. Arun proposed this himself and I'd hold him to it. I'd suggest fee abatement of 20% per month until delivery. That's the difference between a date and an intention.

What I am not asking for: I'm not asking you to build hot standby before your migration, I'm not asking for damages on the $214,000, and I'm not asking for an exclusivity or MFN clause, which my counsel wanted and I overruled.

One more thing, addressed to Simone. If you tell me you can hit these dates and then you can't, tell me in July. Not in March. The migration slipped five months and I heard about it in June, and if that pattern repeats there is no amendment that saves this.

Hannah Ostrowski
Chief Financial Officer, Timberpine Supply Co.

---

**From:** Tom Vasquez <tom.vasquez@alderpointpay.com>
**To:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand [internal]
**Date:** Thursday, June 19, 2025, 1:30 PM

Dropping Hannah off this one deliberately.

Her four asks price out better than I expected and I want that on the record before anyone gets anxious about the 25% cap.

The prospective cap change costs nothing unless we have another two-hour outage. If we do have one, on Timberpine's fees, 25% is about $54,000. That is not a number that should drive this decision.

The March 31 penalty at 20% monthly abatement is $43,000 per month of delay on Timberpine alone. Painful, appropriately so. Arun, if you don't believe March 31 with a penalty, say so now, because this is the moment.

Notification obligations cost engineering time, which Arun has already scoped into the status page work.

So the whole Timberpine package is roughly $780K of hot-standby run-rate that we were going to have to spend eventually anyway, plus real exposure only if we fail. Against $2.6M of revenue and $840K of contribution. I'd sign this.

The thing I'd flag — and Simone, this is the one you should actually weigh — is Hannah's terms becoming everyone's terms. If we give Timberpine a 25% cap and a fifteen-minute notification obligation, that will be in the market by September and our next twenty renewals will ask for it. I've modelled a 25% cap across the whole book against our historical incident rate. It's about $190K of expected annual cost. That's affordable.

The notification obligation at fifteen minutes across 2,400 merchants is an operational commitment, not a financial one, and it's Gabriel's problem more than mine. Gabriel, can you actually do that?

My recommendation: give Hannah all four, and then proactively offer the notification obligation and the improved cap to the whole book rather than waiting to be asked. If it's going to become the market standard, be the one who set it.

Tom

---

**From:** Gabriel Mwangi <g.mwangi@alderpointpay.com>
**To:** Tom Vasquez <tom.vasquez@alderpointpay.com>
**Cc:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>; Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand [internal]
**Date:** Thursday, June 19, 2025, 4:12 PM

Tom — yes, with a condition.

Fifteen-minute notification to 2,400 merchants is only feasible if it's automated. If it depends on someone in my team deciding to send it, it will fail at 2am on a holiday weekend and then we'll have breached a contractual obligation on top of an outage. Arun, that's a trigger wired into the monitoring that fires a templated notification, and it has to be in the August 8 scope, not a later phase.

If it's automated, I can support it across the whole book and I'd like to, because the honest reason merchants are angry is not the six hours. It's the ninety-four minutes of not knowing.

One correction to Tom. The proactive offer to the whole book shouldn't go out the same week as the credits. If we send money and new contract terms in the same envelope it looks like we're buying silence. Credits first, with Arun's explanation letter. Contract amendment offer two weeks later, framed as what we learned. Same substance, and the sequence is the whole difference.

Gabriel

---

**From:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**To:** Hannah Ostrowski <h.ostrowski@timberpinesupply.com>
**Cc:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand
**Date:** Friday, June 20, 2025, 8:40 AM

Hannah,

Yes to all four. Our counsel will have an amendment to you Monday and I'd like it signed before your cure window closes on July 16, not on it.

To be specific, so there's no daylight between what you asked and what we're agreeing:

Warm standby with replication-lag gating, live and verified by failover test on August 8. Weekly automated failover testing from that date, results shared with you monthly. 30-minute RTO for authorization. Hot standby on the migrated platform by March 31, with 20% monthly fee abatement if we miss it. Prospective service credit cap of 25% for incidents exceeding two hours. Automated notification to a named Timberpine contact within fifteen minutes of degraded authorization, and an explicit provision that our support staff will describe an outage as an outage.

Two things I want to add that you didn't ask for.

The first is that the same commitments and the same dates are going into our remediation plan to Cascadia Trust Bank, which we're submitting June 27. One set of facts, one set of dates. Danielle insisted on that and she was right.

The second is your last paragraph, which is the part of your letter I've reread the most. You said if we can't hit the dates, tell you in July, not March. That's a fair thing to ask and it's also the thing we failed at, more than we failed at redundancy. The migration slipped five months and we didn't tell you, not because we decided not to, but because there was no moment where telling you was anyone's job.

So we're making it someone's job. Starting in July, you'll get a monthly note from Arun — not from Gabriel, not from me — with progress against these dates and an explicit statement of whether any of them are at risk. If a date is at risk you'll hear it the month it becomes at risk. I'd rather send you eight boring notes and one uncomfortable one than nine reassuring ones.

The 2,400 other merchants on our platform are getting the notification obligation and the improved credit cap too, offered rather than requested, in mid-July. You'll have been first, and you'll have set the terms, which strikes me as roughly fair given what June 9 cost you.

Thank you for the way you've handled this. You could have simply left.

Simone

---

**From:** Simone Beauchamp <simone.beauchamp@alderpointpay.com>
**To:** Arun Krishnamurthy <arun.k@alderpointpay.com>; Danielle Okafor <d.okafor@alderpointpay.com>; Gabriel Mwangi <g.mwangi@alderpointpay.com>; Priya Raghunathan <priya.r@alderpointpay.com>; Tom Vasquez <tom.vasquez@alderpointpay.com>
**Subject:** Re: June 9 outage — where we stand [internal]
**Date:** Friday, June 20, 2025, 9:15 AM

Closing this out with the full set, so nobody's working off a different version.

Cascadia. Plan goes June 27, twelve days early against a July 2 deadline. Danielle drafts, Arun supplies the technical sections including PLAT-2291 with the date and the fact that Arun deprioritized it, in those words. I call Ellen Sarkisian the morning it lands. Voluntary monthly operational reporting for four quarters, offered not requested.

Roadmap. Frozen as of Monday past. Arun holds the exception line including against me. Migration target September 30. NetSuite first out of the freeze, written down here and in Priya's plan. Priya tells the nine NetSuite merchants and six Lightspeed merchants a real date next week, and Arun, before she does, you give her a date you will hold — because the second slip is the one that loses them, and she's right about that.

Redundancy. Warm standby and failover gating by August 8, $210K. Automated fifteen-minute notification in that scope, not a later phase. Hot standby on the new platform by March 31 with a penalty. We are not building a second region on a stack we're retiring, and we say that plainly to anyone who asks, because it's the truth and it's also the better engineering.

Timberpine. All four asks, amendment Monday, signed well before July 16.

Everyone else. Credits at the contractual cap paid without anyone having to ask, plus Arun's plain-language explanation of what broke — that goes out next week and Arun, you sign it, not me, because merchants can tell the difference. Then in mid-July, two weeks later and deliberately not in the same envelope, the offer of the improved credit cap and the notification obligation to the whole book. Gabriel owns the sequence and Gabriel is right that the sequence is the whole thing.

Tom, the second-half number changes. Priya has a model. Board call is July 8 and I'll take that.

Two last things.

Arun, we're hiring. Four engineers and I don't care what it costs relative to what a six-hour outage costs. Get me requisitions Monday and I'll approve them Monday. And I want you to think about who on your fifteen is carrying too much, because you named them in your first note without naming them, and I'd like to keep them.

And to all of you — I asked for argument on Saturday and I got it, including from people telling me I was wrong about the credits, which I was. Gabriel's point that they'd remember the letter longer than the money was correct and it changed what we're doing. That is what this thread was for. Thank you for using it that way.

Simone
