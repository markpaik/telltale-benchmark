**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>
**Subject:** STOP SHIP — P/N 4471-B — Supplier Quality Notification SQN-25-0912
**Date:** Tuesday, September 9, 2025, 8:47 AM

Ofelia,

This is formal notification that Chelan Aerostructures is issuing a stop-ship on part number 4471-B effective immediately, all dash numbers, all open purchase orders.

Receiving inspection at our Wenatchee facility rejected 7 of 60 brackets from lot 4471-B-2287 (your packing slip 118834, received 9/4). Nonconformances are at hole-position features H4 and H7 — true position out of tolerance by 0.004" to 0.011" against a 0.005" requirement. Given the failure rate we are treating the entire lot as suspect and have quarantined all 4471-B inventory on our shelves, which is approximately 240 pieces across three receipts.

Until further notice: do not ship, do not present certs, and any material in transit will be received into quarantine.

Per your quality agreement (QAG-19, section 7.2) we require your written containment response within 24 hours, to include suspect lot boundaries, root cause hypothesis, and your plan for sorting or replacing affected stock. Tom Ehrlich is copied for the schedule impact discussion, which I'd keep separate from the quality response.

I'm available today after 1 PM if you want to walk the data. The dimensional reports are attached.

Regards,
Jae-won Park
Supplier Quality Manager, Chelan Aerostructures
(509) 555-0173

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**Cc:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** FW: STOP SHIP — P/N 4471-B — Supplier Quality Notification SQN-25-0912
**Date:** Tuesday, September 9, 2025, 9:04 AM

Nils — see below. Drop whatever you're on. I want quarantine tags on every 4471-B in the building by noon — finished goods, WIP, anything staged for the anodize run. Pull the CMM history on the last six lots and get me a suspect window before you and I call Park at 1.

Priya — freeze all 4471-B ship releases in the system so nothing goes out the dock by accident.

This is 38% of our revenue. Everything else waits.

Ofelia

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** RE: STOP SHIP — P/N 4471-B — containment status EOD
**Date:** Tuesday, September 9, 2025, 6:41 PM

Ofelia,

Where we stand as of 6:30:

1. Quarantine complete. 412 finished pieces in FG stores, 198 in WIP at various ops, 74 staged at the anodize line. All red-tagged and moved to the cage or locked in the system.
2. Shipments frozen. Nothing left the dock today. One shipment of 60 is in transit to Wenatchee (left Friday) — I told Park's receiving clerk to quarantine on arrival, he already knew.
3. CMM review — this is where it gets uncomfortable. Our in-process checks on 4471-B sample H4 and H7 at 1-in-10 on the Zeiss. The last three lots show a trend I don't like: H4 true position creeping from 0.002 average in June to 0.0038 in the most recent lot, still "passing" on the sampled parts but the distribution is walking toward the wall. The parts Chelan rejected are consistent with the tail of that distribution. Meaning the sampling caught the average and missed the spread.
4. Suspect window: everything machined on the 5-axis cell since roughly mid-June until I can prove otherwise. That's about 1,850 parts including what's already at Chelan.

The drift pattern points at the rotary table on the Mazak — the errors on H4 and H7 are both B-axis dependent features. I've got the laser tracker guy from Meridian coming tomorrow at 7 AM to check the table. I'll know more by mid-morning.

I'd rather not speculate to Park until Meridian gives me numbers, but I think we should tell him the suspect window honestly. He'll figure out the lot boundaries from the certs anyway.

Nils

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** RE: STOP SHIP — root cause confirmed + a second problem
**Date:** Wednesday, September 10, 2025, 11:18 AM

Ofelia,

Two things and neither is good.

First — Meridian ran the laser check this morning. The rotary table on the Mazak is out. B-axis positioning error of 22 arc-seconds at the extremes, which translates almost exactly to the hole-position error Chelan is seeing at H4/H7 given the part geometry and fixture offset. So root cause on the escape is confirmed: table accuracy degradation, undetected.

Here's the part I have to own. I pulled the calibration record. That table was last laser-calibrated in February 2024. Our own procedure calls for 12-month intervals on rotary axes. It's 19 months. It never came up on the recall list — I'm digging into why, but the short version is the asset was tracked on a spreadsheet Gary maintained before he retired last year and it didn't migrate cleanly into the gage system. That's on my department, full stop.

Second — the Nadcap chemical processing audit that closed out last Thursday came back this morning. Major nonconformance on the anodize line: titration records for tank 3 show 41 missing entries between April and August. The chemistry checks were apparently being done — we have the reagent consumption to show it — but the log entries weren't made. Under Nadcap rules a records gap is treated the same as tests not performed. We have 21 days to submit root cause and corrective action or we risk suspension of the chem processing accreditation, which would shut down anodize for every customer, not just Chelan.

I know how this reads. Two systemic record/calibration failures in the same week is going to look to Park like the quality system is broken, and I can't argue the optics. I'd rather we disclose the Nadcap finding to him proactively than have him find it on eAuditNet, because he will.

Meridian says the table needs a full rebuild, not an adjustment — bearing wear. Their estimate is 15 working days with the cell down. I'll have Priya run the schedule impact.

Nils

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**Subject:** RE: STOP SHIP — root cause confirmed + a second problem
**Date:** Wednesday, September 10, 2025, 11:34 AM

Nils — how does a 19-month gap on our most critical machine not trip a single flag anywhere? I'm not looking for a head, I'm looking for how many other assets are sitting in the same hole. I want a full sweep of every calibrated asset in the building against its interval by Friday. If there are others, I need to know before Park asks me, because he is going to ask me.

Ofelia

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Subject:** RE: STOP SHIP — root cause confirmed + a second problem
**Date:** Wednesday, September 10, 2025, 2:52 PM

Understood, sweep is underway. Early answer on the how: when Gary retired in October '23 his machine-tool assets lived on a standalone spreadsheet separate from GageTrak, because machine geometrics were "maintenance's thing" and gages were "quality's thing." When we consolidated, three machine-level assets never got entered — the Mazak rotary table, the Okuma spindle probe, and a granite plate in the tool crib. The probe was verified in July as part of a service call so it's fine, the granite plate I'm having checked Thursday. Everything actually in GageTrak is current, I've verified 61 of ~340 line items so far and no surprises. Full report Friday as requested.

Nils

---

**From:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** RE: STOP SHIP — cash reality before anyone promises anything
**Date:** Wednesday, September 10, 2025, 4:20 PM

All — before we start committing to recovery spending in front of the customer, everyone needs to understand the box we're in.

We're drawn $2.4M on the $3M revolver. Chelan is 38% of revenue and their receivables run about $1.8M at any given time. If they slow-pay or start debiting us for sort costs while the stop-ship halts new invoicing, the line gets very tight very fast. Every week 4471-B doesn't ship is roughly $420K of revenue that doesn't bill.

The late-penalty exposure Priya flagged — 1,400 parts past the 10/31 dates if the cell is down 15 days — is $340K under the LTA. That is not a number we absorb quietly. Outside 100% CMM at the Portland lab is $46/part; if we sort everything in the suspect window that's roughly $85K before freight, and Chelan will almost certainly debit us for their internal sorting hours on top.

I'm not saying don't spend. I'm saying every commitment goes through one plan and one owner, and we negotiate the penalties rather than eat them, because $340K plus sort costs plus a rebuild plus a Nadcap remediation in the same quarter takes us within sight of the covenant. I'll call First Interstate Thursday and get ahead of it with the bank either way.

Colleen

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Jae-won Park \<jaewon.park@chelanaero.com>
**Cc:** Tom Ehrlich \<tom.ehrlich@chelanaero.com>; Nils Hedstrom \<nhedstrom@latahprecision.com>
**Subject:** RE: STOP SHIP — P/N 4471-B — Latah 24-hour containment response, SQN-25-0912
**Date:** Thursday, September 11, 2025, 8:15 AM

Jae-won,

Per section 7.2, here is our containment response. Nils will send the formal document on our CAR form today, but I want you to have the substance from me directly.

Root cause of the escape is confirmed: the rotary table on our 5-axis cell degraded beyond spec and the degradation went undetected because the table missed its 12-month laser calibration — it had gone 19 months. That is a calibration recall system failure on our side and I'm not going to dress it up as anything else. The B-axis error accounts for the H4/H7 position misses in your data.

Suspect population: all 4471-B machined on that cell since June 16 — approximately 1,850 pieces. That includes the 240 in your quarantine, the 60 in transit, and about 680 finished/WIP here. Everything is locked down.

Containment actions: the cell is down and will not run until the table is rebuilt and re-qualified with a full first-article. All suspect stock will be 100% CMM inspected at Cascade Metrology in Portland, an accredited independent lab, on all hole-position features, at Latah's expense. First sorted lot ships to them tomorrow. We'll present sorted, certified parts to you against the sort reports — nothing ships on our in-process data alone until you tell us you're satisfied.

One more thing you should hear from me before you see it elsewhere: our Nadcap chemical processing audit last week returned a major nonconformance on anodize titration record-keeping. It is a records gap, not a chemistry excursion — we have reagent consumption and periodic external lab checks supporting that the tanks were in control — but I'm disclosing it because you deserve the whole picture of what we're fixing. Our formal Nadcap response is due October 1 and I'll share it with you.

I'd like 30 minutes with you and Tom Friday on the recovery schedule.

Ofelia Barragan
Plant Manager, Latah Precision Aerospace
(509) 555-0418

---

**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Tom Ehrlich \<tom.ehrlich@chelanaero.com>; Nils Hedstrom \<nhedstrom@latahprecision.com>
**Subject:** RE: STOP SHIP — P/N 4471-B — Latah 24-hour containment response, SQN-25-0912
**Date:** Thursday, September 11, 2025, 2:38 PM

Ofelia,

Acknowledged, and I'll say the directness is noted and appreciated. It doesn't change what we need, but it changes how the conversation goes.

Conditions for resuming shipments: 100% independent CMM sort with actuals reported per serial number, sort reports attached to each cert, and I want source inspection at your dock for the first three sorted lots — I'll send Dana Okafor up, she can be there Monday. The stop-ship stays on until the table is rebuilt, the machine passes a first article witnessed by us, and I've reviewed your corrective action, which I need in full 8D format within 30 days.

On the Nadcap finding — thank you for not making me find it myself. I need your written response to us as well, because 4471-B goes through that anodize line and my materials engineer will want the reagent consumption data you referenced before we accept the "records only" characterization. Send what you have.

Costs: Chelan will debit Latah for receiving-inspection and sort labor on the quarantined 240 at our standard rate of $85/hour, and any expedite freight on recovery shipments is yours. Tom will cover the late-penalty question Friday — I stay out of commercial.

The 240 pieces in our quarantine — do you want them shipped back to you for the Portland sort, or do you want to send a sort team here? Faster for us if they come back to you, frankly. Advise by tomorrow.

Friday 10 AM works. I'll send an invite.

Regards,
Jae-won Park

---

**From:** Marcus Ballard \<mballard@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Denise Kowalczyk \<dkowalczyk@latahprecision.com>
**Subject:** heard about weekend schedules — we need to talk first
**Date:** Thursday, September 11, 2025, 3:55 PM

Ofelia,

Word travels. Guys on seconds are hearing we're going to weekend recovery schedules once the Mazak is back up. Before anybody puts a schedule on the board, Article 14 says mandatory weekend work needs 14 calendar days written notice. If you post something Monday for that weekend I'll have to grieve it and neither of us wants to spend October in grievance meetings.

Also being straight with you — second shift is down four operators right now. Reyes quit in August, two on medical, one never got backfilled. Those guys are already running two machines apiece some nights. If the recovery plan assumes seconds absorbs a bunch of extra 4471-B hours the way it's staffed today, it's not going to work and somebody's going to get hurt or scrap a part, and then we're right back here.

What the crew actually wants to know is whether this stop-ship means layoffs. That's the question I got asked six times today. The rumor on the floor is Chelan's pulling the work. If you can tell people something real, tell them soon, because the vacuum is filling up with garbage.

I'm not trying to be a roadblock. Give me a real plan and enough notice and my guys will bust it out. They always have.

Marcus

---

**From:** Priya Raghunathan \<praghunathan@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Colleen Fitzgerald \<cfitzgerald@latahprecision.com>
**Subject:** 4471-B recovery schedule scenarios
**Date:** Friday, September 12, 2025, 7:10 AM

Ofelia,

Ran the scenarios overnight. Assumptions: rebuild starts Monday 9/15, 15 working days puts the Mazak back up October 6, plus 2 days for re-qual and witnessed FAI, so first new production October 8.

Do-nothing case: 1,400 pieces slip past their 10/31 dates, worst piece slips to roughly December 5. That's the $340K penalty exposure.

But the sort changes the math and I don't think anyone's given Chelan this picture yet. We have ~680 finished/WIP pieces here plus 240 coming back from their quarantine plus 60 in transit — call it 980 in the sortable pool. Historical fallout from Nils's distribution data suggests 85–90% of those will pass the 100% sort, so roughly 850 conforming pieces we can start delivering against the October dates within about two weeks, given Cascade's 4-day turn and running them in batches of 200. That alone covers the October 15 and October 22 deliveries.

Remaining gap after the sort: roughly 550–600 pieces of new production needed by 10/31 that we can't make in time. Options to close it: the old DMG can run 4471-B with a modified fixture at about a 40% longer cycle — Hank thinks he can have the fixture ready in a week — which gets us maybe 180 pieces before month-end if we staff it on seconds. The rest, honestly, needs Chelan to flex. If Tom will move the 10/31 dates on ~400 pieces to November 21, we can commit to that with OT and hit it.

So my recommendation for today's 10 AM call: offer them 850 sorted pieces on the original October dates, 180 off the DMG, and ask for relief to 11/21 on the last ~400 in exchange for us eating sort/expedite. That's a much better conversation than "1,400 late, pay us nothing."

One flag: the seconds staffing problem Marcus raised is real. The DMG plan and the OT plan both assume bodies we don't currently have.

Priya

---

**From:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Priya Raghunathan \<praghunathan@latahprecision.com>; Nils Hedstrom \<nhedstrom@latahprecision.com>
**Subject:** RE: 4471-B recovery schedule scenarios — cost rollup
**Date:** Friday, September 12, 2025, 8:42 AM

Rough rollup on Priya's plan so you have numbers going into the 10 AM:

Cascade sort, ~980 pieces @ $46 = ~$45K plus about $6K freight both ways. Rebuild: Meridian quoted $68K firm yesterday. Chelan sort-labor debit on the 240, guessing $8–12K based on their rate. Expedite freight on recovery shipments through November, budget $15K. DMG fixture $9K. OT premium for the recovery window, ballpark $35K. Call the whole recovery ~$180K if the penalties go away, versus $520K+ if they don't. So the entire game today is getting Tom to trade penalty relief for a firm 11/21 commitment. We have room on the line for $180K. We do not have room for $520K without going back to the bank for a bigger facility, and asking for more money the same month our biggest customer stops shipments is a conversation I'd rather not have.

Bank update: talked to First Interstate yesterday, gave them the honest version. They're fine for now but want a written recovery plan by month-end. I'll use whatever we send Chelan.

Colleen

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>; Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Marcus Ballard \<mballard@latahprecision.com>; Denise Kowalczyk \<dkowalczyk@latahprecision.com>
**Subject:** Recovery plan — decisions from today's Chelan call
**Date:** Friday, September 12, 2025, 1:20 PM

Team,

Call with Park and Ehrlich went about as well as it could have. Decisions, so we're all working from the same page:

The sort-first plan is approved by Chelan. The 240 quarantined pieces ship back to us Monday; everything goes through Cascade 100%, actuals by serial, source inspection by Dana Okafor on the first three sorted lots. Tom agreed in principle to move ~400 pieces to November 21 with penalties waived on those, CONDITIONED on us hitting every other committed date. If we miss a date, the full penalty schedule snaps back on everything late. So there is zero slack in this plan. He's papering it as a PO amendment next week.

Meridian starts the rebuild Monday morning. Nils owns the re-qual and witnessed FAI, target October 8 for first production.

Hank builds the DMG fixture, Priya owns loading it on seconds.

Marcus — I heard you on Article 14 and on staffing, and here's my answer. I am posting written notice today for weekend work beginning Saturday September 27, which clears the 14 days. Between now and then everything is voluntary OT sign-up. Denise is authorized to start two operator requisitions Monday and to bring in two temps for deburr/support work so your machinists stay on spindles. And to answer the question your guys are actually asking: nobody is getting laid off over this. Chelan is not pulling the work — they told me that directly today — but they are watching how we recover. I want to talk to second shift myself; let's do it at Monday's shift start, you and me together. I'll send you what I plan to say over the weekend and you tell me where it's wrong.

Colleen — send Tom's team the sort cost breakdown when they ask, and cap our acknowledgment of their $85/hr debit at actual documented hours, not an estimate.

We hit every date on this plan or the whole thing unravels. Weekend calls at 8 AM until further notice, 15 minutes, no slides.

Ofelia

---

**From:** Marcus Ballard \<mballard@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Denise Kowalczyk \<dkowalczyk@latahprecision.com>
**Subject:** RE: Recovery plan — decisions from today's Chelan call
**Date:** Monday, September 15, 2025, 6:22 AM

Ofelia,

Notice posted Friday is clean, no grievance from me. OT sign-up sheet went up Saturday and I'll tell you something — 19 names already, including three guys from days offering to rotate to seconds for the recovery window. Told you they'd bust it out.

Your talking points are mostly fine. Two changes. Take out the line "mistakes were made in our quality system" — say what actually happened, a calibration got missed on the Mazak table. The machinists already know the table was drunk, half of them suspected it in July, and if you get vague on the one thing they know cold they'll stop believing the rest. Second, when you say no layoffs, say it plain and don't lawyer it up with "at this time." Say it or don't.

And Ofelia — Kowalski on seconds flagged that H4 position was walking back in July and wrote it on the check sheet. Somebody should pull that sheet and figure out why it went nowhere, because that's the part that'll actually make the guys mad if it gets buried.

See you at 2:30 shift start.

Marcus

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>
**Subject:** Drafts for review — Chelan 8D and Nadcap response
**Date:** Monday, September 15, 2025, 5:47 PM

Ofelia,

Both drafts attached, need your review by Wednesday.

Chelan 8D (CAR-25-041): root cause chain is documented as (1) rotary table accuracy degradation from bearing wear, (2) undetected due to calibration recall failure, (3) recall failure caused by incomplete asset migration when the maintenance-owned calibration spreadsheet was consolidated into GageTrak in late 2023. Corrective actions: all machine-level metrology assets now in GageTrak with automated recall (done — the full sweep found only the granite plate outstanding, and it checked good Thursday), 12-month laser verification on all rotary axes with a 30-day early warning flag, and — this one matters — in-process SPC on hole-position features for 4471-B with control limits, not just spec limits, so a walking mean trips an alarm before it reaches the wall. Which brings me to Marcus's point about Kowalski's check sheet: he's right, the note is there on the July 22 sheet, "H4 trending high." It went nowhere because our check sheets have no trigger mechanism — a written comment relies on someone reading it. I've added that as a contributing cause in the 8D rather than pretending we didn't see it. Park will respect it more than he'll punish it, and it's true.

Nadcap response: root cause on the 41 missing titration entries is that when our lab tech went out on leave in April, the backup operators ran the titrations off the shift task list but the logging step lived in a separate binder they weren't trained to. Corrective: titration logging moved to the tablet system with a hard stop — the tank can't be statused "in control" for the day without the entry — plus retraining with records, a 90-day daily supervisor verification, and a backfill cross-training matrix for the lab. Objective evidence package includes reagent consumption reconciliation and the quarterly external lab results showing tank chemistry stayed in range through the gap. Submission due to Nadcap October 1; I want it in by the 25th. Copy to Park per your commitment.

Nils

---

**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>
**Subject:** RE: Sorted lot 1 — source inspection results
**Date:** Wednesday, September 17, 2025, 4:12 PM

Ofelia, Nils,

Dana completed source inspection on sorted lot 1 (200 pieces) today. Cascade's data is well organized and the serialized actuals are what I asked for. Fallout on the lot was 22 pieces — consistent with your predicted 85–90% yield. The 178 conforming pieces are released to ship against the October 15 delivery. Lots 2 and 3 same protocol, and if those are clean I'll drop source inspection to a data review.

One administrative item: your certs need to reference the sort report number and this SQN so my receiving doesn't quarantine them out of habit.

The scrapped 22 — hold them segregated. Tom's team will process the debit for the original piece price against them, standard practice, don't shoot the messenger.

Regards,
Jae-won Park

---

**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>; Renata Voss \<renata.voss@chelanaero.com>
**Subject:** URGENT — 4471-B — suspect parts installed on assemblies at Renton
**Date:** Thursday, September 18, 2025, 9:26 AM

Ofelia,

This just escalated. Our Renton assembly line ran a traceability check as part of the containment audit and found that two brackets from suspect lot 4471-B-2241 (received 8/14, before the stop-ship) were installed on wing-attach fittings on assemblies A-1187 and A-1191. A-1187 is complete and staged for delivery to the airframer. A-1191 is mid-build.

This is now a nonconforming-material-in-product situation and it goes to our customer notification process if we can't disposition it fast. I need from you, by end of day tomorrow at the absolute latest:

Serial-level traceability confirming which machine and which date those two brackets were made, and any actual dimensional data you hold on those specific serials — in-process CMM results, anything. If you can show measured conformance on the specific parts, our engineering can run a use-as-is disposition and A-1187 doesn't come apart. If you can't, both brackets come off, and removal on a completed assembly is disassembly of the attach fitting — Renata (cc'd, our MRB engineering lead) estimates roughly $19K in labor and re-inspection, which will be claimed to Latah.

Renata is standing by for your data. Please treat this as the top priority over everything else including the sort.

Regards,
Jae-won Park

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**Cc:** Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** FW: URGENT — 4471-B — suspect parts installed on assemblies at Renton
**Date:** Thursday, September 18, 2025, 9:38 AM

Nils — read below, then clear your day. Serial numbers are in Park's attachment: S/N 2241-084 and 2241-117. I need to know within the hour whether those specific serials were in the 1-in-10 CMM sample for that lot. If either one was actually measured, we may save that assembly. Pull the raw Zeiss files, not just the summary sheets — Renata will want the actuals, uncertainty, cal status of the Zeiss, all of it. Do not send Chelan anything until you and I have looked at it together. If we can't support use-as-is with real data, we say so fast and cleanly. What we do not do is stretch.

Ofelia

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** RE: URGENT — 4471-B — suspect serials 2241-084 and 2241-117
**Date:** Thursday, September 18, 2025, 8:03 PM

Ofelia,

Full day in the QA vault, here's where we landed.

S/N 2241-084: we got lucky. It WAS in the CMM sample for that lot — measured on the Zeiss July 31. All hole positions conforming with margin: H4 true position 0.0031, H7 0.0029, against 0.005. The Zeiss itself is in cal (verified January 2025, artifact checks current) so the measurement stands on its own regardless of the Mazak's condition. I have the raw file, the program revision, the probe qual record, and the operator stamp. This one supports use-as-is and I'd defend it in front of anybody.

S/N 2241-117: not sampled. No direct measurement exists on that serial. Best I can offer Renata is the lot-level distribution — 6 of 60 sampled in that lot, all conforming, worst case H4 at 0.0041 — plus the B-axis error map from Meridian showing which fixture positions produced the out-of-tolerance parts. -117 ran in fixture position 3, which the error map shows as the second-worst position. Honestly, the circumstantial case is against it, not for it. My recommendation is we tell them straight: no data on the serial, position analysis says elevated risk, we recommend removal. If we shade this one and they later find it out of spec at teardown, everything else we've told them for two weeks is retroactively suspect.

Draft response to Renata attached with the -084 evidence package. Say the word and it goes out first thing tomorrow.

Nils

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Jae-won Park \<jaewon.park@chelanaero.com>; Renata Voss \<renata.voss@chelanaero.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>
**Subject:** RE: URGENT — 4471-B — suspect parts installed on assemblies at Renton — Latah data response
**Date:** Friday, September 19, 2025, 7:55 AM

Jae-won, Renata,

Data package attached, and the two serials have different answers.

S/N 2241-084 (assembly A-1187): this serial was directly measured on our Zeiss CMM on July 31 as part of in-process sampling, prior to any suspicion of the rotary table. All hole-position features conform with margin — actuals, raw measurement file, CMM calibration status, and probe qualification records are in the package. We believe this supports a use-as-is disposition, subject of course to your engineering's judgment.

S/N 2241-117 (assembly A-1191): we have no direct measurement on this serial. Lot sample data is included for completeness, but our position-level analysis of the machine error map shows this part ran in a fixture position with elevated risk. We are not going to argue for use-as-is on inference. Latah's recommendation is removal and replacement with a sorted, certified part, which we will overnight to Renton at our cost. We accept responsibility for the removal labor claim on that assembly at documented actuals.

Nils is available all day for Renata's questions on the -084 measurement pedigree.

Ofelia Barragan

---

**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Renata Voss \<renata.voss@chelanaero.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>
**Subject:** RE: URGENT — 4471-B — Renton disposition
**Date:** Saturday, September 20, 2025, 11:41 AM

Ofelia,

Dispositions are signed. -084 is use-as-is; Renata's team reviewed the measurement pedigree and had no findings — A-1187 delivers on schedule, which spared everyone a customer notification, and I want to acknowledge that the quality of your records is what made that possible. -117 comes off A-1191 next week; replacement bracket received this morning, thank you for the overnight. Removal claim will come through Tom at documented actuals, current estimate $19,400, and given that you volunteered responsibility before we asked, I don't expect a fight about it and neither should you.

I'll say one more thing, off the official record. The way you handled -117 — recommending removal against your own interest when you could have argued the lot data — is the reason I'm going to recommend internally that Chelan keep this program with Latah through the recovery rather than second-sourcing. Keep hitting your dates.

Regards,
Jae-won Park

---

**From:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** Cost position as of 9/22 — for the bank package
**Date:** Monday, September 22, 2025, 3:15 PM

All — updated rollup for the recovery plan going to First Interstate this week. Committed/incurred: Meridian rebuild $68K, Cascade sort running $41K of an estimated $47K, freight and expedite $14K to date with maybe $10K more coming, Chelan sort-labor debit came in at $9,350 actual, Renton removal claim $19,400, scrap debit on sort fallout tracking toward $28K at current yield, DMG fixture $9K, OT premium accruing about $8K/week for six weeks. All-in estimate $215K, against penalty exposure avoided of $340K assuming we hold the 11/21 commitment. The PO amendment from Ehrlich came through Friday and the penalty waiver language is clean — I had Whitman & Cole read it. Line balance today $2.55M drawn of $3M; invoicing restarted with the sorted lots so receivables are rebuilding. Tight but manageable IF the dates hold. Priya, I need weekly actuals-vs-plan from you every Friday through November, the bank made it a condition.

Colleen

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Marcus Ballard \<mballard@latahprecision.com>
**Cc:** Denise Kowalczyk \<dkowalczyk@latahprecision.com>
**Subject:** Second shift — follow-up from Monday's talk + Kowalski
**Date:** Monday, September 22, 2025, 6:40 PM

Marcus,

Wanted to close the loop after the shift-start talk last Monday and today's follow-up questions Denise collected. For the record, since people asked me to put it in writing: nobody is being laid off because of the stop-ship. Chelan confirmed the program stays with us. The recovery schedule runs through November 21, weekend work starts September 27 per the posted notice, OT sign-ups have covered the first two weekends fully so nothing mandatory has been needed yet. Both operator requisitions are posted and Denise has four interviews this week; the two temps started today on deburr.

On Kowalski — I pulled his July 22 check sheet myself. He wrote the trend down and the system gave him no way to make anyone listen. That's in our formal corrective action to Chelan, in writing, as a contributing cause — the fix is SPC alarms so a comment like his stops the line instead of sitting in a binder. I told him that face to face this afternoon and I'm telling you so the floor hears it from both directions: he did it right, the system failed him, and the system is what we changed. If anybody on seconds sees something walking again, I want it loud, and I've told the supervisors that a stopped machine over a quality concern will never be held against anyone. You have my word on that and now you have it in writing.

Ofelia

---

**From:** Marcus Ballard \<mballard@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Subject:** RE: Second shift — follow-up from Monday's talk + Kowalski
**Date:** Tuesday, September 23, 2025, 5:48 AM

Ofelia — that'll do. Kowalski told the crew about your conversation before I even got in last night, which did more for morale than anything HR could print. Sign-up sheet for the Oct 4 weekend filled by end of shift. Keep leveling with them and they'll carry you through November.

Marcus

---

**From:** Nils Hedstrom \<nhedstrom@latahprecision.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>
**Subject:** Status — Nadcap submitted, rebuild ahead of schedule
**Date:** Thursday, September 25, 2025, 4:31 PM

Ofelia,

Nadcap response uploaded to eAuditNet this morning, six days ahead of the deadline, with the objective evidence package — reagent reconciliation, external lab results, tablet system screenshots showing the hard stop, training records. Copy went to Park per your commitment; his materials engineer already replied that the reagent data "adequately supports process control through the gap," which is about as warm as those people get. Staff engineer review typically runs 2–3 weeks, I'll track it.

Better news: Meridian is running ahead. Bearing sets arrived early and the rebuild is tracking to finish Wednesday October 1 instead of October 6. If the laser verification is clean Thursday, we cut the FAI parts Friday and Dana can witness the FAI Monday October 6. That pulls first production in by three days, which per Priya converts about 60 more pieces inside the original October dates and takes pressure off the November 21 tail.

The 8D went to Park on the 23rd, one day inside the 30. He accepted D1 through D6 and left D7/D8 open pending 60 days of SPC data, which is standard.

Nils

---

**From:** Jae-won Park \<jaewon.park@chelanaero.com>
**To:** Ofelia Barragan \<obarragan@latahprecision.com>
**Cc:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Tom Ehrlich \<tom.ehrlich@chelanaero.com>
**Subject:** SQN-25-0912 — stop-ship lifted, conditions
**Date:** Tuesday, October 7, 2025, 3:19 PM

Ofelia,

Dana witnessed the first article yesterday on the rebuilt cell. All characteristics conforming, hole positions running at roughly 30% of tolerance, and the laser verification report on the table is in order. Effective today, the stop-ship on 4471-B is lifted, subject to the following through December 31: 100% inspection of H4/H7 on your rebuilt cell's output (your CMM is acceptable, sort lab no longer required), SPC charts for those features submitted with each cert, and immediate notification of any out-of-control condition even if parts conform. Sorted legacy stock continues under the existing protocol until exhausted.

The SQN stays open until the 8D closes at the 60-day data review, which I've set for November 24. Delivery performance to the amended dates is Tom's to track, but for what it's worth you're currently ahead of the recovery curve.

Regards,
Jae-won Park

---

**From:** Ofelia Barragan \<obarragan@latahprecision.com>
**To:** Nils Hedstrom \<nhedstrom@latahprecision.com>; Priya Raghunathan \<praghunathan@latahprecision.com>; Colleen Fitzgerald \<cfitzgerald@latahprecision.com>; Marcus Ballard \<mballard@latahprecision.com>; Denise Kowalczyk \<dkowalczyk@latahprecision.com>
**Subject:** FW: SQN-25-0912 — stop-ship lifted, conditions
**Date:** Tuesday, October 7, 2025, 4:02 PM

Team,

Read Park's note below. Twenty-eight days from stop-ship to release, a rebuilt cell, a first article at 30% of tolerance, the Nadcap response in early, the Renton situation closed without a customer notification, and per Colleen we're tracking to roughly $215K total against what could have been north of half a million and a lost program. Marcus, tell seconds and the weekend crews they did that — I'll come say it in person at Thursday's shift start, both shifts.

We are not done. Every date through November 21 still has to land or the penalty waiver evaporates, the 8D data review is November 24, and the daily 100% checks and SPC submittals cannot slip once, because the entire relationship we just rebuilt is standing on them. Priya keeps the Friday tracker going, Nils owns the SPC discipline, Colleen closes out the claims and the bank package.

One more thing and then I'll stop. The lesson out of this isn't the rotary table. It's that a machinist wrote down a warning in July and the building had no ears for it. We fixed that with software and alarms, but the real fix is what Park saw on the -117 bracket: when the answer was against us, we said so first. That's the habit that kept a $22M program in Spokane Valley. Protect it.

Back to work. 8 AM calls drop to Mondays only starting next week.

Ofelia
