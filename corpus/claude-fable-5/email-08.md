From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: June 9 outage — where we are and what I need from each of you
Date: Wednesday, June 10, 2026, 7:52 AM

All —

I'm starting this thread so we have one place for the outage response instead of six side conversations. Everything material goes here until I say otherwise.

What I know as of this morning: authorizations were down 6 hours 14 minutes yesterday, from roughly 11:40 AM to just before 6 PM, straight through the afternoon settlement window. Arun's team estimates 214,000 declined transactions. The phones lit up around 12:15 and didn't stop. I personally took calls from three of our top ten merchants last night, which is not a thing that should ever happen and tells you how bad the front line got.

What I need by end of day today:

Arun — a plain-language account of what failed and why, and an honest read on where the migration actually stands. Not the board version. If we are behind, I want the real number.

Danielle — anything from Cascadia. If they haven't reached out yet, they will, and I'd rather we get ahead of it.

Gabriel — merchant temperature. Who's angry, who's quiet in a way that worries you, and what people are asking for.

Renata — start scoping financial exposure. Credits, revenue at risk, whatever we might need to spend to fix this.

Caleb — hold on any proactive outbound to prospects until we agree on messaging. If a prospect asks, "we had a service disruption Tuesday, full incident report is coming" and nothing more.

I want to be clear about the posture here. We are not going to spin this. 2,400 merchants had their card volume declined for an afternoon because of us. Some of them are single-location restaurants that did maybe 40% of a normal Tuesday. We fix the thing, we tell people the truth about it, and we take the hit.

Talk soon.

Simone

---

From: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: June 9 outage — where we are and what I need from each of you
Date: Wednesday, June 10, 2026, 11:38 AM

Simone, all —

Plain language version, as requested.

The legacy authorization stack runs on a primary/replica database pair. At 11:41 yesterday the primary went unhealthy — disk controller failure on hardware that is, frankly, older than it should be. Failover to the replica is supposed to be automatic and take under two minutes. It did not happen automatically because the replica had been running with replication lag we weren't alerting on, and the failover script refused to promote a replica that far behind, which is actually correct behavior — promoting it would have meant settling against stale data and we'd be having a much worse conversation right now about misposted transactions. But the manual recovery path from that state was documented badly and had never been rehearsed, because for two years the plan has been "we're migrating off this, don't invest in it." My team spent six hours doing careful surgery on a system three of them had never touched at that layer. They did it right and we lost zero data. But six hours is six hours.

The honest read on the migration: we are five months behind the plan I showed the board in January. I own that. Two reasons. First, we've lost four platform engineers since Q4 — we're at 15, were at 19 — and the two who left in March were the two who knew the legacy settlement code best, so everything they'd have done in a week now takes three. Second, we have been pulling migration engineers onto roadmap features roughly one sprint in three, because those features had customer commitments attached. Every time we did it, it felt like a reasonable one-time trade. Cumulatively it has cost us close to a quarter of migration capacity.

Here is what I believe and I want it on the record in this thread: if we freeze the feature roadmap completely — everything, including the Harborline POS integration and the NorthGlen loyalty build that Caleb's team has already sold — I can have all merchant authorization traffic on the new platform by September 30, with the highest-risk cohorts moved by end of August. If we do not freeze, the realistic date is Q1 next year, and every week between now and then we're running settlement on hardware that just demonstrated what it does under stress.

Yesterday was not bad luck. Yesterday was the predictable output of the choices we've been making. I'd rather say that plainly now than say it again after the next one.

Full technical incident report will be done Friday.

Arun

---

From: Danielle Okafor <dokafor@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: RE: June 9 outage — Cascadia letter received, please read
Date: Wednesday, June 10, 2026, 4:21 PM

All —

Well, they didn't wait. Letter from Cascadia Trust arrived by courier at 2 PM, signed by Diane Whitfield, EVP of Payments Risk. Full scan is in the compliance shared drive under Sponsor Bank/2026. The parts that matter:

They are formally invoking the operational-standards section of the sponsorship agreement. We have 21 days from the date of the letter — that's July 1 — to deliver a written remediation plan covering root cause, corrective actions with dates, and "demonstrable improvements to processing resilience, including redundancy of authorization infrastructure." Their words. That redundancy phrase is going to matter, Arun, so read the letter yourself.

Second, and this is the one with teeth: effective immediately they are pausing approval of new merchant boarding until they've accepted the plan. Caleb, that's your 90 to 130 new accounts a month, frozen. They frame it as temporary and "without prejudice," but I've seen how these pauses go at other processors. If they don't like the plan, temporary becomes indefinite.

Third, they're reserving rights under the agreement generally, which is lawyer for "we're keeping termination on the table." I do not read this letter as a bank looking for an exit — the tone is firm but it's a bank that wants to be given a reason to stay comfortable. Diane and I have a working relationship and I spoke to her office to confirm receipt and ask for a call next week. But we get one shot at this plan. If we send them something with soft dates and hedged commitments, we will get a second letter and the second letter will be worse.

Practical point: whatever we decide internally about the migration timeline and redundancy spend needs to be decided before the plan goes out, because the plan has to state it as commitment, not intention. So the freeze question and the standby question are no longer just engineering and budget questions. They're regulator-adjacent questions with a July 1 clock on them.

Danielle

---

From: Gabriel Mwangi <gmwangi@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: June 9 outage — merchant temperature
Date: Wednesday, June 10, 2026, 6:47 PM

Simone —

Merchant picture as of tonight. My team logged 412 inbound contacts yesterday and today, which is about eleven times a normal two-day volume. The tone breaks into three groups.

Angry and loud: 38 merchants have explicitly asked about service credits or compensation. Reminder on the contract mechanics — our MSA caps service credits at 10% of monthly fees, which for a typical merchant is a couple hundred dollars against what some of them lost in an afternoon. Two merchants have already used the word "lawyer" on calls, though I'd rate both as venting.

Quiet in the way you asked about: Timberpine Supply. Hannah Ostrowski's office cancelled our regular Thursday check-in with no reschedule and their AP contact asked us — today, of all days — to confirm the notice address in our contract. Timberpine is 8.4% of total volume and $2.6M of annual revenue and they have been getting courted by two competitors that I know of. When a CFO's office asks for your notice address, they are not planning to send you a card. I'm flagging this as our single biggest account risk and I don't think we have weeks.

Everyone else: rattled but reasonable. The consistent question is not "what happened," it's "will it happen again." Merchants live through outages from all their vendors. What they don't forgive is silence or spin. Which is why I want to send a real incident report to all 2,400 — actual root cause in plain English, actual dates for fixes — rather than the "we experienced a service disruption and take reliability seriously" template. I have a draft going but it's got holes in it shaped exactly like the decisions Danielle just described. I can't tell merchants what we're doing about redundancy until we know.

Gabriel

---

From: Renata Vogel <rvogel@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: RE: June 9 outage — exposure numbers, first pass
Date: Thursday, June 11, 2026, 9:15 AM

Morning all. First pass on the money, rough but directionally right.

Direct revenue loss from the outage itself: roughly $95–110K in processing fees on the declined volume, though some of that came back as retries after we recovered. Call it $80K net.

Credits: if we pay every affected merchant the contractual 10% cap for June, worst case is about $190K. We will not pay everyone because not everyone will ask, but I'd reserve the full number.

The real exposure is churn. Timberpine alone is $2.6M annual. If we lose them and it signals the market, and we shed even 3% of the rest of the book on top, that's another $1.5M+. Against that, whatever we spend on remediation is cheap. I want everyone to hold that frame when we get to the redundancy price tag, because I've heard the number floating around and I don't want the first reaction to be sticker shock. Arun, please put the actual figure and timeline in writing on this thread so we're all working from the same fact.

The boarding pause is the slow bleed. New merchants are roughly $140–180K of new annualized revenue added per month. A 60-day pause costs us that cohort twice over plus pipeline decay. Every week the remediation plan slips past July 1 costs real money, so I'm treating Danielle's deadline as a financial deadline too.

Renata

---

From: Caleb Foster <cfoster@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>
Subject: RE: June 9 outage — before we freeze everything, please read
Date: Thursday, June 11, 2026, 2:33 PM

Simone,

I've held outbound as asked and I'm not going to pretend Tuesday wasn't bad. But I need to push back before "freeze the roadmap" hardens into a decision by momentum.

Two of the items Arun wants to cut are not roadmap wishes, they're signed commitments. Harborline POS is contracted for delivery by August 31 with 14 merchants who chose us specifically because of it — combined they're about $900K of annual revenue and Harborline's own sales team refers us deals. NorthGlen's loyalty integration is written into their renewal, which comes up in October. NorthGlen is 2.1% of volume. If we walk both back in the same month we had a six-hour outage, we are telling two strategic partners and a top-twenty merchant that Alderpoint doesn't keep its word, at the exact moment Timberpine is deciding whether we keep our word.

And with boarding paused, retention and these existing commitments are literally the only revenue motion I have. You'd be freezing new logos and torching the expansion pipeline in the same month.

I'm not asking to keep the whole roadmap. Cut the other seven items, fine. I'm asking whether two engineers on two committed integrations really moves September to Q1. Arun, is it genuinely all-or-nothing, or is there a version where we protect the two things with signatures on them?

Caleb

---

From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
Cc: Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: June 9 outage — questions for Arun before I decide
Date: Thursday, June 11, 2026, 5:58 PM

Caleb's question is fair and I want it answered with specifics, not principle. Arun:

1. What exactly does keeping Harborline and NorthGlen cost the migration in weeks, with names attached — which engineers, doing what, for how long?

2. Renata asked for the redundancy figure in writing. Give us the full picture: cost, timeline, what it actually protects against, and whether it's still worth it once the migration is done. I need to know if we're buying a bridge or a building.

3. The Cascadia letter says "redundancy of authorization infrastructure." Does finishing the migration alone satisfy that in your professional judgment, or does the new platform need the standby too?

I want answers on this thread by tomorrow. I'm deciding the freeze question by Monday at the latest — Danielle's July 1 clock doesn't leave room for a long deliberation, and honestly neither does Timberpine's silence.

Simone

---

From: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: June 9 outage — answers
Date: Friday, June 12, 2026, 10:04 AM

Answers in order.

1. Harborline and NorthGlen. It is not two engineers in the abstract, it's which two. Harborline needs Priya and Marcus because it touches the settlement pipeline, and Priya and Marcus are exactly the people carrying the migration's settlement cutover — the hardest, riskiest piece of the whole program. Pulling them for Harborline through August 31 pushes settlement cutover from late August into November, and everything downstream slides with it. That's how "just one sprint" got us five months behind: the people features need are always the people the migration needs most. NorthGlen's loyalty build is genuinely lighter — it sits on the new platform's API layer, needs one engineer, and doesn't touch legacy settlement at all. If I'm forced to choose, I can absorb NorthGlen and hold September 30. I cannot absorb Harborline and hold anything close to it. So Caleb, my honest answer: it's not all-or-nothing, it's one-not-two, and it has to be NorthGlen we keep, not the bigger revenue number.

2. Redundancy. A hot-standby authorization environment — second full stack in a separate facility, real-time replication, automated failover we actually rehearse monthly — is $780,000 a year run-rate and 10 weeks to stand up from a go decision. Given procurement lead times, a decision by June 22 means live by August 28–29. To Simone's bridge-or-building question: building. The standby protects the legacy stack for its remaining life, and then the new platform fails over to it after cutover. Any processor our size should have had this years ago. The only reason we don't is that it kept losing budget fights to features, including some I lost and some I didn't fight hard enough.

3. Does the migration alone satisfy Cascadia's redundancy language? No. A newer platform with a single point of failure is still a single point of failure. If we send Diane Whitfield a plan that says "we'll finish our migration" and nothing else, we are handing her the question "and what happens when the new one fails over?" and we will not have an answer. Migration plus standby is a plan. Migration alone is a hope with a date on it.

One more thing while I have the floor. My 15 engineers worked until 3 AM Tuesday and got us back with zero data loss, and several of them have been asking me for two years why we keep deferring exactly the investments we're now discussing. When the decisions land, I'd like to be able to tell them something changed. Retention on that team is now itself a migration risk.

Arun

---

From: Renata Vogel <rvogel@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
Cc: Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: June 9 outage — the $780K, funded
Date: Friday, June 12, 2026, 3:41 PM

Short one. I can fund $780K a year without touching headcount: roughly $300K from the marketing program budget for H2 (with boarding paused we can't onboard the leads anyway, so the spend was about to get inefficient), $250K by pushing the office expansion to next year, and the remainder from the contingency reserve, which is precisely what the reserve exists for. It takes 2026 EBITDA down about a point and a half. Losing Timberpine takes it down four. This is the cheapest expensive thing on the table and I recommend we buy it.

On NorthGlen vs Harborline — Caleb, I hear you on the $900K, but $900K at risk over an integration delay is a survivable commercial negotiation. Settlement cutover slipping to November while Cascadia watches is not. Finance vote is with Arun.

Renata

---

From: Gabriel Mwangi <gmwangi@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: FW: NOTICE OF TERMINATION FOR CAUSE — Timberpine Supply Co. / Alderpoint Payments MSA
Date: Tuesday, June 16, 2026, 10:22 AM

It's here. Forwarding the notice we received this morning from Timberpine's counsel. Everyone should read the full attachment but the operative part:

> Pursuant to Section 11.2(b) of the Master Services Agreement, Timberpine Supply Co. hereby provides notice of termination for cause based on Alderpoint's material failure to provide processing services on June 9, 2026, resulting in the decline of approximately 6,100 Timberpine customer transactions during peak trade hours. In accordance with Section 11.2(b), Alderpoint shall have thirty (30) days from the date of this notice to cure the material breach to Timberpine's reasonable satisfaction, failing which termination shall be effective July 16, 2026.

Note the phrasing — "to Timberpine's reasonable satisfaction." Their lawyers left the door open on purpose. A termination-for-cause notice with a cure period is a negotiating document. If Hannah wanted out clean, she'd have sent a non-renewal and gone quiet. She sent this because she wants something specific and she wants it with a deadline on it. I called her office within the hour; she'll take a call but told her EA to say, quote, "I've had the reassurance call, I want the plan call."

Simone, I think this needs you, me, and Arun on it. Not just me.

Gabriel

---

From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Gabriel Mwangi <gmwangi@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
Cc: Danielle Okafor <dokafor@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: FW: NOTICE OF TERMINATION FOR CAUSE — Timberpine Supply Co. / Alderpoint Payments MSA
Date: Tuesday, June 16, 2026, 11:05 AM

Agreed, the three of us. Gabriel, get us on Hannah's calendar Thursday or Friday. Do not offer anything on that call beyond what's been decided on this thread by then — which means I'm moving my decision up. Decision email tomorrow, not Monday. Everyone who wants to be heard on the freeze, the standby, or Harborline/NorthGlen has until 9 AM tomorrow.

Danielle — assume the answer to Cascadia and the answer to Timberpine need to be the same answer. If we commit something to one that we can't show the other, it will surface. These people talk.

Simone

---

From: Danielle Okafor <dokafor@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: RE: Cascadia remediation plan — proposed structure
Date: Wednesday, June 17, 2026, 8:41 AM

Before the decision lands — here's the structure I'd propose for the Cascadia plan, so everyone can see how the pieces have to fit. Spoke with Diane Whitfield's deputy Monday and got useful signal on what they actually want to see.

1. Root cause, unvarnished. Arun's Friday incident report, lightly edited. They will respect specificity; they will punish vagueness. The replication-lag alerting gap goes in, the unrehearsed failover runbook goes in.

2. Immediate corrective actions already done — new alerting live (Arun confirmed Friday), failover runbook rewritten and rehearsed on the legacy stack, hardware inspection of the remaining legacy fleet.

3. Migration commitment with dated milestones and monthly written progress reports to the bank. They specifically want interim milestones, not one September date — they've been burned by processors with a single heroic deadline before. Arun, I need highest-risk-cohort dates from you, in writing, that you would stake your name on.

4. Redundancy. This is the section their deputy circled, metaphorically. If the standby is approved, we state the contract date, the go-live week, and a commitment to monthly failover exercises with results shared. That converts their scariest sentence into our strongest one.

5. Governance — quarterly operational review with the bank, and a named executive owner. Should be Arun with me as liaison.

If we deliver that by June 26, ahead of the July 1 deadline, with real dates in sections 3 and 4, I put good odds on the boarding pause lifting within 30–45 days of acceptance. Their deputy hinted as much without committing. If section 4 is empty, I wouldn't want to guess.

One legal note for the Timberpine conversation: whatever redundancy commitment we make to Hannah, expect her to want it in a contract amendment with remedies attached, not a letter. We should decide in advance what remedy we can live with. My suggestion: if the standby isn't live by a fixed date, Timberpine gets a no-penalty termination right. That's a commitment with teeth that costs us nothing if we simply do what we said.

Danielle

---

From: Caleb Foster <cfoster@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>
Subject: RE: before 9 AM — closing argument, sort of
Date: Wednesday, June 17, 2026, 8:52 AM

Getting in under the wire. I've reread Arun's Friday email three times and I'm not going to keep arguing against the settlement engineers' calendar — if Harborline genuinely costs us the cutover, it costs us the cutover. I concede Harborline, on two conditions I'd ask you to build into the decision.

One, I tell Harborline myself, in person, this week, with a new committed date tied to the migration finishing — not an open-ended "delayed." If we give them a real date in Q4 and hit it, the partnership survives. If they hear it from an email or a rumor, it doesn't. Two, the 14 merchants waiting on that integration get told proactively by my team and Gabriel's jointly, with something in hand — I'd suggest waiving their gateway fees until the integration ships. Renata, that's maybe $60K, tell me if that breaks anything.

And confirming NorthGlen stays, per Arun's one-not-two. If NorthGlen slips too, their October renewal is dead and I'll have conceded Harborline for nothing.

Caleb

---

From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: DECISION — freeze, standby, Harborline/NorthGlen, and who does what
Date: Wednesday, June 17, 2026, 1:47 PM

Decisions. These are final; execution questions welcome, relitigation is not.

The roadmap is frozen through migration completion, with one exception: the NorthGlen loyalty integration continues, per Arun's assessment that it doesn't touch the migration's critical path. Everything else stops, including Harborline. Caleb, your two conditions are granted — you tell Harborline in person this week with a committed Q4 date that Arun signs off on, and we waive gateway fees for the 14 waiting merchants until it ships. Renata says the $60K is fine, she told me this morning.

The hot standby is approved at $780K a year, funded per Renata's June 12 email. Arun, sign the contracts by Monday June 22 so we hold the August 28–29 go-live. That date is about to appear in a bank remediation plan and probably a customer contract amendment, so I want your final confirmation it's real before Danielle writes it down. Padding is acceptable; fiction is not.

Migration target is September 30 for full cutover, highest-risk cohorts by August 31, and Arun owes Danielle interim milestone dates by Friday for the Cascadia plan, which goes out June 26 per her structure. Danielle runs the bank relationship day to day, Arun owns the plan's commitments, I sign the cover letter.

Timberpine: Gabriel has us confirmed with Hannah Ostrowski for Friday at 2. The shape of our offer, which Gabriel, Arun and I will refine Thursday: the standby commitment with a hard date, a contract amendment giving Timberpine a no-penalty exit if we miss it (Danielle's structure), June credits above the contractual cap as a goodwill matter, and monthly reliability reporting for a year. What we are not offering is a price concession. This was a reliability failure and the remedy is reliability. If Hannah wants a discount she'll ask, and the answer is that we're spending the discount on the standby instead, for her benefit.

All other merchants: Gabriel sends the full incident report to all 2,400 once the Cascadia plan is out — same facts, same dates. Every merchant materially affected on June 9 gets the 10% monthly credit applied automatically, without having to ask. Renata, reserve the full $190K. Gabriel, I want to see the draft.

Last thing. Arun, tell your team the freeze is real this time, and tell them it came with $780K of the infrastructure budget they've been asking for. They earned that on Tuesday night at 3 AM. I'll come say it in person at Friday's standup as well.

Simone

---

From: Hannah Ostrowski <hostrowski@timberpinesupply.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Gabriel Mwangi <gmwangi@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>
Subject: RE: Friday's call — what I need to see beforehand
Date: Friday, June 19, 2026, 9:12 AM

Simone,

Ahead of our 2:00 today, I want to be direct about what will and won't move me, so nobody wastes the hour.

On June 9 we declined roughly 6,100 customer transactions. Our stores comped orders, took IOUs from contractors we've known for twenty years, and turned away cash-equivalent business we can't recover. My board asked me a simple question Monday: why does our payment processor have a single point of failure, and what specifically will be different in ninety days? I could not answer the second half. That's why you have the notice.

I've had the apology and I believe it's sincere. What I need today is a specific, dated, contractual commitment on redundancy — not "we're accelerating our platform migration," which is what your account team offered on June 11 and which, respectfully, is a different promise. A newer platform that can also go down for six hours is not what my board asked about. I want to know: is there a second environment, when is it live, what happens contractually if you miss the date, and how do I verify it exists and works rather than taking your word.

If the answer today is concrete, I have room to move. Twelve years with Alderpoint counts for something with me even if it doesn't count for much with my board right now. If the answer is another version of "trust us," I'll spend the cure period on the two proposals sitting in my inbox from your competitors, and I suspect you know whose.

2:00.

Hannah Ostrowski
CFO, Timberpine Supply Co.

---

From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Hannah Ostrowski <hostrowski@timberpinesupply.com>
Cc: Gabriel Mwangi <gmwangi@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>
Subject: RE: Friday's call — in writing, as discussed
Date: Monday, June 22, 2026, 4:36 PM

Hannah,

Thank you for Friday, and for being as direct in the room as you were in your email. As promised, here is everything we discussed, in writing, so your board sees it from me and not as your summary of a phone call. Our counsel will send the formal amendment to yours by Thursday; this email states what will be in it.

First, the redundancy commitment. Alderpoint has contracted for a fully redundant hot-standby authorization environment in a separate facility, with real-time replication and automated failover. The contracts were signed this morning — Arun can confirm the vendor and facility details under NDA if your board wants them. Committed go-live is August 29, 2026. Beginning in September we will run a live failover exercise monthly, and Timberpine will receive the results of every exercise in writing, along with monthly platform reliability reporting for a minimum of twelve months. You asked how you verify rather than trust: that's how. If a failover test fails, you'll know within five business days, from us.

Second, the teeth. The amendment will provide that if the standby environment is not live and verified by September 15, 2026 — two weeks of buffer past our committed date, which exists so that the date I just gave you is one we beat rather than one we defend — Timberpine may terminate the MSA without penalty and without a cure period, and we will support a 90-day transition to any successor processor at our cost. I am comfortable signing that because we are going to hit the date. If we don't, you shouldn't be our customer, and I'd rather put that in a contract than ask you to keep believing it.

Third, June 9 itself. We are crediting Timberpine's full June processing fees — not the 10% contractual cap. I want to be straightforward that this exceeds our contractual obligation and we're doing it once, for this event, because the failure was ours and the cap wasn't written for a six-hour outage in the settlement window. This is being handled as a goodwill credit and Renata Vogel's team will apply it to your July invoice.

Fourth, what I'm not offering, so there's no ambiguity later: we haven't changed your pricing and I'm not proposing to. Every dollar of margin on your account and everyone else's is currently going into the standby environment and finishing our platform migration, which completes September 30 with your traffic moving in the first cohort in August. That spend is your protection. A discount would be coming out of it.

In exchange, we're asking that Timberpine withdraw the termination notice upon execution of the amendment. The amendment gives you a stronger exit right than the notice does — a fixed date with no cure period versus a contestable cause claim — so I don't believe we're asking you to give anything up. Danielle Okafor, copied here, runs our compliance function and will be your named escalation contact alongside Gabriel; she is also the person reporting these same commitments and dates to our sponsor bank, which means the dates in your amendment are dates a federally regulated institution is independently holding us to. You will not be relying on our internal discipline alone.

Twelve years counts for something with me too, Hannah. Tell your board the second half of their question now has an answer with a date on it.

Simone Beauchamp
CEO, Alderpoint Payments

---

From: Hannah Ostrowski <hostrowski@timberpinesupply.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Gabriel Mwangi <gmwangi@alderpointpay.com>; Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>
Subject: RE: Friday's call — in writing, as discussed
Date: Tuesday, June 23, 2026, 11:48 AM

Simone,

This is what I asked for. Three changes and we're done.

One, the September 15 termination right should survive for the twelve months of reporting, triggered by any month with more than 60 minutes of cumulative authorization downtime — not evaporate the day the standby goes live. If the redundancy works, this clause never matters and costs you nothing, by your own logic. Two, the failover exercise results come to us within five business days as you said, but a failed exercise triggers a call with Arun, not just a report. Three, the migration of our traffic in the August cohort goes into the amendment too, since you volunteered the date.

Get those into Thursday's draft and I'll recommend my board approve the amendment and withdraw the notice at our meeting on the 30th. And Simone — the full June credit was the right instinct and it was noticed here. It won't stop me from holding you to every date in this email.

Hannah

---

From: Danielle Okafor <dokafor@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: Cascadia remediation plan — submitted, and first read from the bank
Date: Thursday, June 25, 2026, 5:07 PM

All —

The remediation plan went to Cascadia by courier and secure upload at 2 PM today, five days ahead of deadline, with Simone's cover letter. Final version is in the shared drive. It contains everything we committed to on this thread: the unvarnished root cause, corrective actions already completed, migration milestones (highest-risk cohorts including Timberpine by August 31, full cutover September 30, monthly written progress reports), the standby environment with the signed contract attached as an exhibit and the August 29 go-live, monthly failover exercises with results shared with the bank, and quarterly operational reviews with Arun as named executive owner.

Diane Whitfield's deputy called at 4:30 to confirm receipt and said — informally, not a commitment — that the plan "reflects the seriousness we were looking for" and that they expect to complete review within three weeks. I asked directly about the boarding pause. She said the committee would consider lifting it upon acceptance of the plan rather than upon completion of the milestones, which is the good version, but that they'd likely want the first monthly progress report and the standby go-live confirmed before fully releasing it. Realistic planning assumption: boarding resumes in stages, partial in late July, full in early September. Caleb, build your pipeline math on that and please keep prospects warm honestly — "our sponsor bank is reviewing our post-incident remediation plan" is a fine sentence to say out loud, and far better than a prospect hearing it elsewhere.

One alignment note, per Simone's instruction that everyone hears the same answer: the dates in the Cascadia plan, the Timberpine amendment, and Gabriel's merchant letter are now identical, and they need to stay identical. Any slip gets reported to all three audiences in the same week, by us, first. Arun, that means your monthly report to the bank is effectively a public document as far as our discipline is concerned. Write it accordingly.

Danielle

---

From: Gabriel Mwangi <gmwangi@alderpointpay.com>
To: Simone Beauchamp <sbeauchamp@alderpointpay.com>
Cc: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Subject: All-merchant communication — final draft attached, sends Monday
Date: Friday, June 26, 2026, 12:19 PM

Final draft of the all-merchant letter is attached, going to all 2,400 accounts Monday morning under Simone's signature, followed by direct calls from my team to the top 150 by volume through the week. Summary of what it says, for the record on this thread:

It opens with what actually happened — a database hardware failure, an automated failover that correctly refused to promote a lagging replica, and a manual recovery that took six hours because we had underinvested in a system we were planning to retire. No euphemisms. Arun reviewed for accuracy and, I'd note, pushed to make it more candid, not less.

It then states the four commitments with dates: monitoring and failover procedures already fixed and rehearsed; the fully redundant standby environment live August 29 with monthly live failover testing thereafter; full migration to the new platform by September 30; and a published monthly reliability report for all merchants starting in September — same cadence the bank and Timberpine get, lighter format.

On credits: every merchant with declined transactions on June 9 gets the 10% monthly credit applied automatically to their July invoice, no request needed. The letter says plainly that we know the credit doesn't cover what the afternoon cost many of them, and that the honest compensation is the roughly $1M+ we're now spending annually to make sure there isn't a next one. Renata has signed off on that framing and the reserve.

The 14 Harborline-integration merchants got their calls from Caleb's team and mine on Wednesday with the Q4 date and the gateway-fee waiver; two were annoyed, twelve said some version of "at least you told us." Caleb saw Harborline in person Tuesday — Caleb, you can speak to it, but my understanding is they took the Q4 date professionally and the referral relationship holds.

Of the original 38 credit requesters, 31 are settled by the automatic credit, four wanted calls they've now had, and three are still unhappy; I'm handling those personally and none is a churn risk I'd lose sleep over. And for the thread's benefit: Timberpine's board meets Tuesday the 30th. Hannah's office has already scheduled our regular Thursday check-in for the following week. CFOs don't reschedule standing meetings with vendors they're firing.

Gabriel

---

From: Simone Beauchamp <sbeauchamp@alderpointpay.com>
To: Arun Krishnamurthy <akrishnamurthy@alderpointpay.com>; Danielle Okafor <dokafor@alderpointpay.com>; Gabriel Mwangi <gmwangi@alderpointpay.com>; Renata Vogel <rvogel@alderpointpay.com>; Caleb Foster <cfoster@alderpointpay.com>
Cc:
Subject: RE: All-merchant communication — closing this thread
Date: Monday, June 29, 2026, 8:14 AM

All —

The merchant letter went out twenty minutes ago. Amendment executed with Timberpine Friday, with Hannah's three changes; her board votes tomorrow on withdrawing the notice and Gabriel and I both read that as done. Plan is with Cascadia five days early. Standby contracts signed, clock running to August 29. Roadmap frozen except NorthGlen, Harborline moved to Q4 with the partner and all 14 merchants told to their faces. Nineteen days after the worst operational day in this company's history, every audience — the bank, Timberpine, 2,400 merchants, and our own engineers — has heard the same facts and the same dates from us first.

Now the hard part, which is the boring part. Everything we committed to over the last three weeks is a date on a calendar between now and September 30, and the only thing that discharges any of it is hitting them. Standing weekly review, Mondays at 9 starting next week, this group, until full cutover: migration milestones, standby build, bank status, Timberpine reporting, merchant sentiment. First agenda item every week is the same question — are we still on the dates we published — and I want bad news in week one of a slip, not week four. We've just finished telling everyone who matters that this company tells the truth fast. That's now the product as much as the processing is.

June 9 cost us real money, nearly cost us our biggest merchant, and put our sponsor bank on formal notice. It also got us, in three weeks, the decisions we'd failed to make for three years. I'd rather have made them without the outage. Since we didn't, the least we owe the people who sat through that afternoon is to never need this thread again.

Thank you, all of you. Closing this out.

Simone
