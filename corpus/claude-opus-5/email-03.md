# STOP SHIP — 4471-B — dimensional NC at 2 features

**From:** Jae-won Park <jpark@chelanaero.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>; Nils Hedstrom <nhedstrom@latahprecision.com>
**Cc:** Renae Sutcliffe <rsutcliffe@chelanaero.com>; Dale Okonkwo <dokonkwo@chelanaero.com>
**Subject:** STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 7:52 AM

Ofelia, Nils,

Effective this morning we are placing PN 4471-B on stop ship. Receiving inspection pulled a 60-piece sample off lot LP-25-2211 (your packing list 44902, received 9/4) and seven pieces are out of tolerance at hole positions H7 and H12. True position callout is .010 diametral at MMC. Measured values on the seven range .0134 to .0191. Both features are on the same side of the part and the deviation is directional, not scattered, which reads to me like a machine or fixture condition rather than random variation.

No 4471-B material moves from your dock to ours until we have agreed containment. I also need to know, today if possible:

The date and lot of the last conforming shipment you believe is clean, your assessment of how far back the condition may extend, what you have on hand at Spokane Valley in WIP and finished goods, and whether any 4471-B has shipped to us since 44902.

I've asked Renae to pull what we have in our stores and quarantine it. Dale is checking whether any of this part number has gone to the floor in Renton. I'll know more on that by Thursday.

Formal SCAR is being written and you'll have it by end of day. Containment response is due in 24 hours per our supplier manual, root cause and corrective action in 15 calendar days. I'd rather have the conversation than the paperwork, so please call me if it's faster.

Jae-won Park
Supplier Quality Manager
Chelan Aerostructures

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Jae-won Park <jpark@chelanaero.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 8:41 AM

Jae-won,

Received and understood. We are stopping shipment on our side as of now and Nils has quarantined everything with a 4471-B traveler on it, WIP and FG both. I'll have counts to you before noon.

Nils is on the floor pulling the last six months of CMM data on that part number. Directional and same-side matches what you'd expect from the rotary table on cell 4, which is where 4471-B runs its second op. He's checking calibration history now.

I'll call you at 10 your time.

Ofelia Barragan
Plant Manager
Latah Precision Aerospace

---

**From:** Nils Hedstrom <nhedstrom@latahprecision.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Warren Delacroix <wdelacroix@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 11:20 AM

Ofelia — before you get back on with Park, you need to know two things and neither of them is good.

First, cell 4 rotary table. Last laser calibration was 2/14/24. Nineteen months ago. Our own procedure QOP-7.6 says twelve. It fell off the schedule when we moved from the spreadsheet to the new maintenance module last spring and it never got re-entered. I pulled the interim check sheets, the operators have been running the ball bar weekly like they're supposed to and the ball bar has been passing, but a ball bar catches circularity and squareness, it does not catch a slow angular positioning drift on the B axis. That's what we have. I put a laser on it this morning, we're at 41 arc-seconds of positioning error at the 90 degree index. Spec is 8.

Second, and this is separate, the Nadcap chemical processing audit that closed Friday came back with a major on the anodize line. Titration records for tank 3, they found 41 missing entries between March and August. Not out-of-range entries. Missing. Nobody wrote them down. Auditor's position is we cannot demonstrate the bath was in control for those periods, and he's right, we can't. Response due to PRI in 21 days.

I know how those two land in the same email. They are not the same failure but a customer is going to read them as the same failure, which is that our system for making sure things get checked on time has a hole in it. I'd rather we say that ourselves than have Park say it.

On the parts. I have CMM data back to March. The drift starts showing in the trend around week of 6/30 — still inside print but the mean at H7 walks from about .004 to .0072 across July, then we start seeing individual pieces over .010 in mid-August. First lot I'd call suspect is LP-25-1907, shipped 7/14. Since then we've shipped six lots to Chelan, 1,340 pieces total. On hand here: 212 finished, 396 in WIP at various ops.

Nils Hedstrom
Quality Director

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**Cc:** Marcus Ballard <mballard@latahprecision.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 12:06 PM

Nils, thank you for putting it plainly. You're right that we say it first.

Warren, I need engineering's read on the table by end of day. Rebuild or can it be compensated. I know what I think the answer is but I want it from you in writing.

Colleen, start building the number. Late penalty exposure, outside inspection cost, rebuild cost, and what it does to the line.

Marcus, adding you now because whatever we decide is going to land on the floor and I don't want you hearing it secondhand. Nothing is decided. When it is, you and I talk before anyone else does.

I have Park at 1:00, moved from 10.

Ofelia

---

**From:** Warren Delacroix <wdelacroix@latahprecision.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>; Nils Hedstrom <nhedstrom@latahprecision.com>
**Cc:** Colleen Fitzgerald <cfitzgerald@latahprecision.com>; Marcus Ballard <mballard@latahprecision.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 4:48 PM

Ofelia,

You want it in writing so here it is in writing. The table has to come apart.

Forty-one arc-seconds at the index is not a compensation problem. I spent two hours on this with Ivo and we put a dial on the worm and there is measurable backlash that changes depending on where in the rotation you are, which means the wear is not uniform. You can build a compensation table for a linear error. You cannot reliably compensate a nonuniform one, and even if we got it close today it would walk again in six weeks and we would be right back here except this time we'd have told a customer we fixed it. I am not signing that.

Rebuild is worm, wormwheel, both bearing sets, seals, and a re-grind on the faceplate if it's marked, which I won't know until it's open. Vendor is Kuehn in Portland, they did the table on cell 2 in 2022 and they were straight with us. Their number today was 15 working days from receipt, plus two days each way freight, plus a day to pull and a day to reinstall and a day to laser and prove out. Call it 20 working days door to door. Cost 68 to 84 thousand depending on the faceplate.

I want to be honest that I am partly responsible for where we are. The calibration schedule migration was my project. I signed off that everything transferred. It didn't and I didn't audit it.

There is a second thing nobody has asked about yet. 4471-B is not the only part that runs on cell 4. There are eleven active part numbers on that machine and four of them have angular features tight enough to care about 41 arc-seconds. Two of those go to Chelan on other programs, two go to Bergstrom. Nils and I need to look at those tonight because if we tell Park only about 4471-B and then find something on 3320-A in three weeks, we are finished with him.

Warren Delacroix
Engineering Manager

---

**From:** Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features
**Date:** Tue, Sep 9, 2025 6:15 PM

Ofelia,

Numbers as of tonight, rough but not wildly so.

Cell 4 down 20 working days puts approximately 1,400 pieces past their contract delivery dates across the Chelan and Bergstrom books. The Chelan agreement has liquidated damages at 1.5 percent of line value per week late, capped at 15 percent. Running it lot by lot against the October 31 dates I get $340,000 if we go the full rebuild and don't recover any of it. That is the number if we do nothing else.

Outside CMM at Callender Metrology in Portland, they quoted $46 a part, four-day turn, they can take 400 a week. If we sort everything on hand plus what we'd need to run to stay current, that's roughly 1,900 pieces over the next seven weeks, $87,400, plus freight both ways which they estimate at $6,800 total, plus we tie up somebody here full time managing it. Call it a hundred thousand all in.

Table rebuild 68 to 84.

The line is the problem. We're drawn $2.4 million on $3 million. Availability today is $600,000. October is already a heavy month, we have the Q3 estimated tax payment on 9/15 and the insurance renewal 10/1, which together are $310,000. So my real headroom for anything unplanned between now and the end of October is closer to $290,000, and that assumes Chelan pays 44902 and 44911 on time, which they will not if we are on stop ship, because their AP holds against open SCARs. That's another $412,000 sitting out there.

I want to be very clear about the shape of this. It is not that we cannot afford the rebuild. It is that we cannot afford the rebuild and the sorting and the penalties and a customer who stops paying us, all inside of six weeks. Any two of those we survive. All four and I am calling Sandpoint First about the covenant before they call me.

Colleen Fitzgerald
Controller

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Jae-won Park <jpark@chelanaero.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Dale Okonkwo <dokonkwo@chelanaero.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features — containment response
**Date:** Wed, Sep 10, 2025 8:30 AM

Jae-won,

Following our call yesterday, here is our containment response in writing, inside your 24 hours.

Cause is identified with reasonable confidence. The rotary table on our 5-axis cell 4 has developed nonuniform angular positioning error on the B axis. We laser-checked it Tuesday morning and measured 41 arc-seconds at the 90 degree index against an 8 arc-second spec. 4471-B indexes to that position for the H7 and H12 drilling, which explains why the deviation is directional and confined to those two features. Our engineering manager's judgment, which I accept, is that this cannot be compensated in software and the table requires a full rebuild.

I need to tell you the part of this that is worse than the machine. That table was due for laser calibration in February 2025 and it did not get done. The requirement was in our procedure, the asset was on our calibration master, and when we migrated to a new maintenance system last spring the record did not carry over and no one caught it. Nineteen months elapsed against a twelve month standard. Our operators ran the weekly ball bar check throughout and it passed every time, but a ball bar does not detect this failure mode, so the routine check gave us false comfort. The gap is ours and I am not going to characterize it as anything other than a system failure on our side.

Containment actions in place as of this morning:

Cell 4 is down. Nothing runs on it, not 4471-B and not anything else, until the table is repaired and laser-verified. We are 100 percent CMM inspecting H7 and H12 on all 212 finished pieces here and all 396 in WIP, on our own machines, at our own cost. Suspect population going back, we believe, to lot LP-25-1907 shipped 7/14 — six lots, 1,340 pieces, all listed in the attached with quantities and ship dates. Nils will send Renae the CMM raw data on the 60-piece sample and our trend charts so your people can check our math on where the drift starts.

Warren and Nils spent last night on the other ten part numbers that run cell 4. Four of them have angular features tight enough to be at risk and two of those are yours — 3320-A and 3355-C. We are pulling and measuring in-house stock on both today and I will report to you tomorrow whether they are affected regardless of what we find. I would rather tell you about a problem you didn't know to ask about than have you find it.

The two open items I owe you are recovery schedule and commercial. I will have a proposal to you Friday. I am not going to send you a schedule I haven't confirmed with my own people first.

Ofelia

---

**From:** Jae-won Park <jpark@chelanaero.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Dale Okonkwo <dokonkwo@chelanaero.com>; Priya Ramnarine <pramnarine@chelanaero.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features — containment response
**Date:** Wed, Sep 10, 2025 2:11 PM

Ofelia,

That is the most useful containment response I've gotten from a supplier this year and I want to say so before I say the rest of it.

Telling me about 3320-A and 3355-C before I asked buys you something with me. It does not buy you anything with Priya, who I've added, because she runs the program office and her problem is airplanes not process. But it matters to me and I'll say so in the room.

Where I need to push. Your suspect population starts at LP-25-1907 on a trend argument. I understand the argument and the charts probably support it. But the fleet doesn't care about your mean, it cares about individual parts, and a part shipped in June from a machine that was already drifting is a part I can't prove was good. I want you to extend the suspect population to the last shipment after a known-good machine condition. Since the machine's last verified condition is February 2024, that is technically nineteen months of production and I recognize that is not a workable answer. So let's find the defensible middle. Do you have any independent measurement on that part number between February 2024 and June 2025 — a first article, a customer source inspection, a layered audit, anything with a real number attached to those two features? If there's a clean data point in, say, April, I'll accept April as the boundary.

Second. My understanding from your note is the rebuild takes the cell down about four weeks. You have 4,100 a year from us on 4471-B which is roughly 340 a month, and October 31 dates. Walk me through what that does to my deliveries before you send me a proposal Friday, because if the answer is that I get nothing for four weeks then I need to start a conversation in Renton today and not Friday.

Third, and I'm sorry to add to it. Renae flagged that your Nadcap chemical processing accreditation shows an open major in the PRI database as of yesterday. Anodize. Is that related to this or is that a separate thing, and is our material affected? I need an answer on that specifically because 4471-B is anodized and if you have a bath control issue on top of a dimensional issue then my containment is not adequate.

Jae-won

---

**From:** Nils Hedstrom <nhedstrom@latahprecision.com>
**To:** Jae-won Park <jpark@chelanaero.com>; Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Warren Delacroix <wdelacroix@latahprecision.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Priya Ramnarine <pramnarine@chelanaero.com>
**Subject:** RE: STOP SHIP — 4471-B — dimensional NC at 2 features — containment response
**Date:** Wed, Sep 10, 2025 5:39 PM

Jae-won,

Taking your third question first because it's the one that should worry you most and I don't want it buried.

The Nadcap finding is real and it is separate from the table. It is a major on our anodize line, tank 3, for missing titration records — 41 log entries not made between March and August. It is a records failure, not a demonstrated process failure. Every process control chart we do have for tank 3 in that window is in range, the tank was pulled and analyzed by an outside lab twice in that period on our normal quarterly and both came back in spec, and we have no coating thickness or adhesion rejections on any part number in that window. So my technical position is that the baths were in control and I believe it.

My quality position is different and you should hold me to the quality position. I cannot demonstrate control for 41 shifts. I can build an argument from surrounding data and outside lab results and product performance, and that argument is decent, but it is an argument and not a record. If you told me a supplier of mine had that finding I would want the same thing I'm about to offer you: we will pull retained samples from the affected windows and run coating weight and Taber abrasion at an outside lab, and we will run tape adhesion on a sample from every 4471-B lot we currently have in quarantine, and I will send you all of it including anything I don't like. If something comes back off, you'll have it the day I have it.

On your first question, the clean data point. Yes, I have one, and it's better than I expected. We did a full FAI on 4471-B on 4/22/25 for the drawing revision change to Rev K — that's the revision that added the chamfer at the outboard flange. Ballooned FAI, thirty-two pieces, dimensional layout on a Zeiss, and H7 and H12 are both on it. H7 measured .0031 and .0037 on the two pieces we laid out fully, everything else in the sample checked at those features on our shop CMM and the max was .0049. That is a real, independent, documented measurement and it is inside half the tolerance. Rev K FAI package was submitted to your Renae on 4/29 and approved 5/12, so you have it too.

So I'd propose the boundary is the first shipment after 4/22/25, which is lot LP-25-1520 shipped 5/6. That extends the suspect population from six lots to eleven lots, 2,470 pieces instead of 1,340. It nearly doubles our problem and I'm proposing it anyway because it's the defensible line and I'd rather draw it myself than have you draw it for me in three weeks.

I'll have the 3320-A and 3355-C measurements tomorrow.

Nils

---

**From:** Marcus Ballard <mballard@latahprecision.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>
**Subject:** cell 4 / what second shift is hearing
**Date:** Wed, Sep 10, 2025 6:02 PM

Ofelia,

You said you'd tell me before anyone else. I appreciate that. Second shift already knows, because Ivo helped Warren put the laser on the table Tuesday and Ivo talks, and by last night the version going around was that Chelan caught us shipping bad parts and there's going to be layoffs when the machine goes down for a month.

I'm not telling you that to make trouble. I'm telling you because the rumor is worse than the truth and you have about a day before the rumor sets.

The other thing you need to hear from me. There is a version of this where somebody decides the operators should have caught the drift. They ran the ball bar every week like the procedure says and they signed it and it passed. If the ball bar was the wrong check, that is not on the man running it. I have been doing this twenty-six years and I have watched three different companies solve a management problem by finding an hourly guy who signed something. If that starts here I will be a problem about it and I would rather tell you that now, in a normal tone of voice, than later.

On the weekend schedule I know you're going to ask for. Article 14 is fourteen days notice for a scheduled weekend, which means if you post Friday the 12th the first weekend you can work is the 27th. There's an emergency provision at 14.3 but it requires mutual agreement with the local and it's meant for a fire or a flood, and if I sign it for a calibration that didn't get done I will get asked why by people who work for me. I'm not saying no. I'm saying it costs something and you should know what before you ask.

Second shift is short four operators and has been since June. You know that. Two of those reqs have been open since April. If the plan involves second shift running more hours the honest version is that we don't have the bodies and overtime on a short crew on a 5-axis is how you get somebody hurt or a $40,000 tool crash.

Marcus

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Marcus Ballard <mballard@latahprecision.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**Subject:** RE: cell 4 / what second shift is hearing
**Date:** Wed, Sep 10, 2025 8:44 PM

Marcus,

On the operators. You have my word in writing and you can hold this email up in any room you want to. No operator is being disciplined or blamed for the table. They ran the check the procedure told them to run. The procedure was inadequate for the failure mode and the calibration that would have caught it was missed at the management level, specifically in a system migration Warren has already put his name to. If anyone in this building starts building a story that runs the other direction, send them to me.

On the rumor. I'll do a floor meeting Thursday at shift change, both crews, and I'll do it standing on the floor and not in the conference room. What I'm going to say is: we have a machine problem we caused ourselves, we found it because a customer's inspection caught it and that's not how we want to find things, the machine is going out for four weeks, and nobody is being laid off over it. That last part is true and Colleen has confirmed it's true.

On the weekend. I'm not going to ask you for 14.3. You're right that it's meant for a flood and you're right about what it costs you to sign it. I'll post fourteen days and take the 27th, and Warren and I will build the recovery around that constraint instead of pretending it isn't there.

On the four open reqs. I'll get you an answer on those by Monday and it's going to be a real answer, not "we're looking at it."

Ofelia

---

**From:** Warren Delacroix <wdelacroix@latahprecision.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>; Nils Hedstrom <nhedstrom@latahprecision.com>
**Cc:** Colleen Fitzgerald <cfitzgerald@latahprecision.com>; Marcus Ballard <mballard@latahprecision.com>
**Subject:** cell 4 recovery — three options and what I actually think
**Date:** Thu, Sep 11, 2025 3:22 PM

Before Friday. I've run this three ways with Ivo and with Delphine on scheduling.

Option one, straight rebuild. Table out Monday 9/15, back and proved out by 10/13 if Kuehn holds their 15 days, which they might not. Cell 4 dark for four weeks. We ship nothing on 4471-B in that window. Every October 31 date slips, we eat Colleen's $340,000, and Chelan's line in Renton starves around the third week of October by my read of their takt. That last part is the one that ends the relationship, not the penalty.

Option two, no rebuild, sort everything. Keep running cell 4 with the bad table and 100 percent CMM every piece at Callender in Portland. We make rate, we ship, but we're deliberately producing a known-nonconforming process and screening for good ones. Yield at current drift is maybe 82 percent and getting worse, so we'd run 420 to make 340, we'd burn material and hours, and every four days we'd be waiting on a truck from Portland. And we would be telling a customer that our containment is inspection on a process we know is out of control. Nils will not sign it and he shouldn't. Also, in about six weeks the drift walks far enough that yield collapses and we've spent the money for nothing.

Option three, the one I want. Split it.

Cell 2 has the same spindle and the same envelope. Its table was rebuilt in 2022 and lasered in March, it's at 5 arc-seconds. 4471-B has run on cell 2 before — we ran it there for eight weeks in 2023 when cell 4 had the spindle issue, so we have a proven program and a proven fixture, and I found the fixture in the tool crib this morning, which frankly I did not expect. Cell 2 is currently loaded with 2290 series for Bergstrom and a Hutchings job.

If I move 4471-B to cell 2 and push the Bergstrom 2290s to the horizontal cell where they'll run slower but they'll run, I can make roughly 240 a week on 4471-B on cell 2 running two shifts. That is 70 percent of rate, not 100. Combined with the 212 finished pieces here that clear inspection and whatever of the 396 WIP we can save, I think we cover October and slip about 300 pieces into the first week of November instead of 1,400 pieces into December.

The cost. Bergstrom's 2290 dates move by about a week and I need someone to call Ellery Voth over there and it should not be me. We give up the Hutchings work for the window, which is $31,000 of revenue Colleen is going to hate losing. And I need one setup guy for two days to move and prove the fixture, and Marcus, that's Ivo, and it's a Saturday or it's four days instead of two.

I want to be clear that option three is not a clever escape. We still take the table apart, we still miss dates, we still have a customer who caught us. It just fails smaller.

Warren

---

**From:** Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**To:** Warren Delacroix <wdelacroix@latahprecision.com>; Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Marcus Ballard <mballard@latahprecision.com>
**Subject:** RE: cell 4 recovery — three options and what I actually think
**Date:** Thu, Sep 11, 2025 5:57 PM

Warren, option three re-run:

Late penalties drop from $340,000 to about $61,000 if we're only slipping ~300 pieces by a week. That's the whole ballgame and everything else is noise next to it.

Losing Hutchings for six weeks is $31,000 of revenue at roughly 34 points of margin so call it $10,500 of contribution. I'll live.

Sorting cost changes shape. If cell 2 is making conforming parts we don't need Callender for ongoing production at all — we only need capacity to burn down the 2,470-piece suspect population that's already out there, and 608 of those are in this building. So Callender is a one-time cleanup expense, not a running one. That's maybe $60,000 not $100,000, and I can stage it over six weeks instead of paying it in three.

The line still doesn't love this. Rebuild is 68 to 84, Callender is 60, that's $144,000 against $290,000 of headroom, and it holds only if Chelan pays 44902 and 44911. Ofelia, that is the single most important thing you negotiate this week. Not the penalties. The receivable. If Park's AP holds $412,000 for the duration of an open SCAR, we are borrowing against the rebuild to make payroll on October 17 and I will be having a very different conversation with you.

One more thing and I'll say it since nobody has. We should decide now, before Park asks, what we're willing to pay for. My view is we pay for all of it — sorting, expedite freight, the CMM, our own inspection labor, and the rebuild. We do not ask him to split the sort cost. The condition is ours, the missed calibration is ours, and the $46 a part is real money but it is small money against a customer who is 38 percent of our book and is currently deciding what kind of company we are. Where I would push back is on penalties, because if we recover the schedule the penalties were written to compensate for a harm that didn't happen, and on any consequential claim from Renton, which we should not agree to before we know what it is.

Colleen

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Jae-won Park <jpark@chelanaero.com>; Priya Ramnarine <pramnarine@chelanaero.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Dale Okonkwo <dokonkwo@chelanaero.com>
**Subject:** 4471-B — recovery plan and commercial position
**Date:** Fri, Sep 12, 2025 9:15 AM

Jae-won, Priya,

Recovery plan and where we stand commercially. This is what we're doing, not what we're proposing to consider.

Production. We are moving 4471-B off cell 4 and onto cell 2 rather than waiting out the rebuild. Cell 2 is the same spindle and envelope, its table was rebuilt in 2022 and laser-verified in March 2025 at 5 arc-seconds, and we ran 4471-B on that cell for eight weeks in 2023 during an unrelated outage, so the program and the fixture are proven and both are in hand. Fixture moves and proves out Monday and Tuesday. First cell 2 parts to CMM Wednesday 9/17.

Cell 2 gives us about 240 pieces a week against your 340 a month, so we are not rate-limited on your part. What we lose is the buffer. My schedule shows us meeting every October 31 date except one lot of roughly 300 pieces which lands the first week of November, six to eight days late. I would rather tell you six to eight days late in September than tell you on October 29. Nils is sending Renae the lot-level schedule with dates.

Cell 4 table ships to Kuehn in Portland Monday. Fifteen working days at the vendor, back in the machine and laser-verified by 10/13. Cell 4 does not run a Chelan part number until it has a passing laser report and Nils has signed a requalification. Every part number that runs cell 4 gets a first-article requalification before production resumes, and you'll get copies of the ones that are yours whether or not you ask.

Suspect population. We accept Nils's 4/22/25 boundary, which is the Rev K FAI. Eleven lots, 2,470 pieces, of which 608 are here and 1,862 are at your facilities or downstream. We are 100 percent CMM inspecting H7 and H12 on all of it. The 608 here we do on our own machines. For your 1,862 I am proposing we sort at Callender Metrology in Portland — they're a Nadcap-accredited lab, they can take 400 a week, and Nils has their calibration and correlation data if Renae wants it. Alternative is we send two of our inspectors to your site with portable equipment and sort in place, and honestly if your material is staged where sorting in place is practical I'd prefer that because it's faster and nothing sits on a truck. Your call, tell me which and we'll do it.

Who pays. We do. All of it. The sorting, the freight, the expedite, our inspection labor, the Callender invoices, and the rebuild. I am not asking you to split any part of the containment cost and I don't want a negotiation about it, because the condition is ours and the missed calibration is ours and I'd rather spend the week fixing it than dividing it.

Two things I am asking for.

The first is that you release the receivable. You have $412,000 open on invoices 44902 and 44911 for material that shipped before any of this and that we believe is conforming — and if the sort says otherwise on any piece I'll credit it that day. I understand your AP holds against an open SCAR and I understand why the policy exists. I am asking you to make an exception, or to release the portion not associated with suspect lots, because we are funding a hundred and forty thousand dollars of containment out of a revolver and the arithmetic gets bad in October if that money sits. I'd rather tell you that directly than manage around it and have you find out.

The second is the penalties. Our agreement has liquidated damages at 1.5 percent per week and against the original four-week outage that was $340,000. Against the plan above it's about $61,000 on the one late lot. I'm asking you to waive that $61,000 — not the concept, this instance — on the grounds that we self-reported the extent, extended the suspect population beyond what your data supported, are absorbing the full containment cost, and are going to land your October within a week. If the answer is no I'll pay it and not raise it again.

On the Nadcap major. Nils sent you the technical position Wednesday and he's right that you should hold him to the quality position rather than the technical one. Our formal response to PRI goes in by 10/1 and you'll get it the same day. Outside lab testing on retained samples starts Monday.

I'll be in Renton Tuesday if it's useful for me to be in a room. I don't need it to be a good meeting.

Ofelia

---

**From:** Priya Ramnarine <pramnarine@chelanaero.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Jae-won Park <jpark@chelanaero.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Dale Okonkwo <dokonkwo@chelanaero.com>; Nils Hedstrom <nhedstrom@latahprecision.com>
**Subject:** RE: 4471-B — recovery plan and commercial position
**Date:** Fri, Sep 12, 2025 4:33 PM

Ofelia,

Jae-won has been telling me since Wednesday that you're handling this well and he's right, so let me be equally direct about the parts that are still problems for me.

Six to eight days late on 300 pieces is not a small thing in my world even though it's a small thing in yours. That lot feeds a subassembly that has a two-week float and the float is currently one week because of something unrelated on a different supplier. So your six days lands on top of somebody else's seven and I have a stoppage. I need you to look again at whether cell 2 plus overtime closes those six days, and if it can't, I need to know by Wednesday so I can go re-sequence work in Renton, which takes me ten days to arrange.

On the receivable, that's not mine, but I've talked to Jae-won and he's talked to our finance side. Answer is a partial. We'll release 44902 in full, $247,000, this week — that material predates your April boundary and there's no basis to hold it. 44911 stays held until the sort clears the lots on it. If the sort comes back clean we release inside 48 hours of Renae signing off. That's the best I can get you and I did push.

Penalties. Not my call either, but my recommendation to contracts is going to be that we waive the $61,000 if you hit the schedule you just sent me, and that we don't waive anything if you miss it. I'm not trying to be clever. You've put a number on the wall and I'd rather the incentive point at the number.

The thing I actually need from you is different from all of the above. I have to decide whether to dual-source 4471-B and I have to decide in the next sixty days. Right now the case for it is that my largest single-part-number dependency sits on one machine at one supplier that went nineteen months without a calibration and didn't know. The case against it is that qualifying a second source on this part is nine months and half a million dollars and I'd rather spend that on you. What I want from you, and not this week, is a written answer to how you know this isn't happening somewhere else in your plant right now. Not a promise. A method.

Priya Ramnarine
Program Director, 737 Structures
Chelan Aerostructures

---

**From:** Dale Okonkwo <dokonkwo@chelanaero.com>
**To:** Nils Hedstrom <nhedstrom@latahprecision.com>; Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Jae-won Park <jpark@chelanaero.com>; Priya Ramnarine <pramnarine@chelanaero.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>
**Subject:** 4471-B — two suspect units installed in Renton
**Date:** Thu, Sep 18, 2025 11:07 AM

Nils, Ofelia,

Escalating. We have found two brackets from suspect lots already installed on assemblies at Renton. Traceability puts them on lot LP-25-2104, shipped 8/8. Assemblies are S/N 4419 and S/N 4426, both in position 3 on the line, both past the point where the bracket is accessible without disassembly of the surrounding structure.

Neither was dimensionally verified before install. Our receiving sample on 2104 was 30 pieces and passed, which is how they got through.

What this triggers on our side: a stress and interchangeability assessment by our engineering to determine whether an out-of-position condition at H7 and H12 at the observed magnitudes is acceptable as-is, repairable, or requires removal. That's a formal disposition and it goes to our chief engineer. If the answer is removal, we're looking at roughly 40 hours of disassembly per unit plus the fastener holes in the mating structure become an issue and it may go to our customer as a nonconformance, which is a different order of problem for everyone on this email.

What I need from Latah, urgently:

The actual measured values on every piece from lot 2104 you've sorted so far. Not pass/fail. Numbers, all of them, including the passing ones, because our stress people need the distribution to bound the worst case. If the maximum observed deviation across the whole suspect population is .0191 that is a different analysis than if it's .0400.

Whether either of those two features is a fastener hole that carries load in shear or a locating feature. I have the drawing but I want your manufacturing engineering's read.

Any data you have on hole perpendicularity and surface condition at those features, since an out-of-position hole drilled with a drifting rotary may also be out of perpendicular and that matters more to our analysis than position does.

I'd like this by close of business tomorrow. I know that's fast.

Dale Okonkwo
Materials Review Engineer

---

**From:** Nils Hedstrom <nhedstrom@latahprecision.com>
**To:** Dale Okonkwo <dokonkwo@chelanaero.com>
**Cc:** Ofelia Barragan <obarragan@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Jae-won Park <jpark@chelanaero.com>; Priya Ramnarine <pramnarine@chelanaero.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>
**Subject:** RE: 4471-B — two suspect units installed in Renton
**Date:** Thu, Sep 18, 2025 8:12 PM

Dale,

You'll have the full data set tonight, not tomorrow. Renae is getting a file with every measured value from every piece we've sorted, 1,043 pieces as of this evening across all eleven suspect lots, raw CMM output not summarized, with lot and serial. Passing and failing both.

Ahead of the file, the answers to your three questions.

Distribution. Across everything sorted, maximum observed true position at H7 is .0244 and at H12 is .0217. Both of those are on lot 2211, the last one we shipped, which is consistent with a drift that was still worsening. For lot 2104 specifically, which is your lot, we have sorted 218 of 340 and the maximum is .0163 at H7. Mean .0074. Ninety-one of 218 are over the .010 print callout. I'll have the remaining 122 by Saturday and I'll send them the moment I have them, but I don't expect the max to move much because 2104 ran in a two-day window and the drift inside a lot is small.

I want to give you one more number that you didn't ask for. Our worst case is not .0244. Our worst case is the last part we ran on cell 4 before we shut it down, which was 9/8, and I pulled that specific piece out of quarantine and laid it out. .0271 at H7. Nothing from that day shipped, it's all here, but if you're bounding the analysis you should bound it at .0271 and not at what shipped, because that's where the machine actually was.

Feature function. Warren's read, and he'll confirm in his own words: H7 is a fastener hole in a shear-loaded joint attaching the bracket to the frame. H12 is also a fastener hole but our understanding from the assembly drawing is that it picks up a secondary clip and is lightly loaded. So the one that matters to your stress people is H7 and I'd focus there. Warren wants to say directly to your engineering that we are not the design authority and our reading of load paths from an assembly drawing is worth exactly what it's worth.

Perpendicularity. You're asking the right question and I wish I had a better answer. Perpendicularity at H7 and H12 is not a called-out characteristic on the print, so it is not on our standard inspection plan and I do not have historical data on it. What I have done since your email came in is put twelve pieces from lot 2104 on the CMM and measure it, and I'm going to give you the answer even though it's the answer I didn't want. Perpendicularity ranges .0026 to .0119 over the .38 depth. The high ones correlate with the high position values, which makes sense — the table was indexing to a slightly wrong angle so the hole is both displaced and tilted. I'm running twenty more overnight and adding perpendicularity to the sort plan for every remaining suspect piece, which slows the sort by about a day and a half and is obviously the right thing to do.

That last item is a finding we generated because you asked a question my inspection plan didn't cover. That is going into our corrective action as its own item, because the deeper problem is that our inspection plan checks what the print calls out and doesn't ask what the failure mode would do.

On the two installed units. Whatever your chief engineer decides, including removal, we will fund the disassembly and rework labor and we'll send people if people help. I'd rather you make the engineering call without a cost conversation sitting in the middle of it.

Nils

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** All Latah Employees <all@latahprecision.com>
**Subject:** cell 4 and where we are
**Date:** Fri, Sep 19, 2025 6:30 AM

I said most of this on the floor Thursday of last week and again at second shift change, but people on days off missed it and I've heard three versions of it come back to me, so here it is written down.

We shipped parts to Chelan that were out of tolerance. They caught it, we didn't. The cause is a rotary table on cell 4 that drifted out of position because a calibration that was due in February didn't happen. It didn't happen because the record didn't carry over in a software migration and nobody audited the migration. That is a management failure and it is specifically not an operator failure. The weekly ball bar check was run every week and passed every week and the check was never going to catch this. If you ran that check and signed it, you did your job correctly.

Nobody is being laid off. Cell 4's table is at the rebuilder and comes back around October 13. We moved 4471-B to cell 2 and Bergstrom's 2290s to the horizontal, and Ivo and Dwayne got the cell 2 fixture proved out in a day and a half instead of two days, which saved us more than anyone outside this building will ever understand.

There will be a weekend schedule posted for October 4 and 5 and the notice goes up today, which is more than the fourteen days the contract requires. It's voluntary first and Marcus and I have agreed on how the list works.

The last thing. Chelan has asked us a fair question, which is how we know this isn't happening somewhere else in the plant right now. We don't fully know, and answering it properly is going to mean going through every piece of equipment on the calibration master by hand against the actual machines on the floor. Nils is running that and he's going to need people's time and people's memory, especially from anyone who's been here longer than the maintenance system has. If he asks you when something was last touched, the useful answer is the true one, including "I don't know."

I'd rather we be the company that found the other ones ourselves.

Ofelia

---

**From:** Ofelia Barragan <obarragan@latahprecision.com>
**To:** Priya Ramnarine <pramnarine@chelanaero.com>; Jae-won Park <jpark@chelanaero.com>
**Cc:** Nils Hedstrom <nhedstrom@latahprecision.com>; Warren Delacroix <wdelacroix@latahprecision.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>; Dale Okonkwo <dokonkwo@chelanaero.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>
**Subject:** RE: 4471-B — recovery plan and commercial position — 9/26 status
**Date:** Fri, Sep 26, 2025 5:41 PM

Priya, Jae-won,

Weekly status. I'll keep sending these Fridays until you tell me to stop.

Schedule. Cell 2 has been running 4471-B since 9/17 and we're at 251 pieces in the first full week against a plan of 240. All conforming, max true position .0038. Nils's requalification and the first-article package for the cell 2 move went to Renae Wednesday.

Priya, on your six-to-eight-day problem. We closed it. The 300-piece lot now lands 10/29, two days early, not six days late. It took the October 4-5 weekend, which Marcus posted with more than the contractual notice and filled voluntarily, and it took Warren finding about eleven hours of cycle time by rebalancing the op sequence on cell 2. Please don't re-sequence Renton on our account. If anything changes I'll tell you the day it changes and not the week after.

Sort. 2,183 of 2,470 complete. 341 nonconforming to date, 15.6 percent. Everything at your facilities has been sorted in place by our two inspectors working in Renae's area since 9/15, which was faster than shipping to Portland and I'm glad you took that option. Callender has the remainder and finishes the week of 10/6. Perpendicularity is now measured on every piece per Dale's question and is in every report.

Cell 4. Kuehn opened the table 9/22. Faceplate was marked and needs the re-grind, so we're at the top of their range on cost and they've asked for three extra days. Back in the machine 10/16, laser-verified and requalified by 10/21. Cell 4 runs nothing of yours before then.

Nadcap. Response went to PRI Wednesday, 9/24, ahead of the 10/1 due date, and Renae has a copy. Outside lab results on retained anodize samples came back on 34 pieces spanning the March–August window. Coating weight all in range, Taber all in range, tape adhesion all pass. That supports what Nils said in September and it does not undo the records finding, which we've addressed with an interlock — the tank log is now a required entry in the shop system and the anodize line will not release a load without it. Nils fought for that over a paper form and he was right.

Priya, your real question. "A method, not a promise." Nils has the full answer coming to you the second week of October, but the short version is that we have physically walked every piece of equipment on the floor against the calibration master, machine by machine, and found four more assets where the record and the reality don't agree. Three are minor. One is a CMM in the inspection room that was calibrated on schedule but against a standard whose own certification lapsed in January, which means eight months of our own inspection data is technically unsupported. We are re-certifying the standard, re-verifying the CMM, and Nils is scoping what re-inspection that implies. I would guess it is a small number of parts and I would rather guess out loud to you now than discover it and tell you in November.

That is the fifth problem this month and I'm aware of how it reads. But it's the first one we found ourselves, before it found a customer, and that is the difference I'd point at if you're weighing us against nine months and half a million dollars.

Ofelia

---

**From:** Jae-won Park <jpark@chelanaero.com>
**To:** Ofelia Barragan <obarragan@latahprecision.com>
**Cc:** Priya Ramnarine <pramnarine@chelanaero.com>; Nils Hedstrom <nhedstrom@latahprecision.com>; Dale Okonkwo <dokonkwo@chelanaero.com>; Renae Sutcliffe <rsutcliffe@chelanaero.com>; Colleen Fitzgerald <cfitzgerald@latahprecision.com>
**Subject:** RE: 4471-B — recovery plan and commercial position — 9/26 status
**Date:** Mon, Sep 29, 2025 8:19 AM

Ofelia,

Stop ship lifts on 4471-B effective today for cell 2 production only, on the strength of the requalification package and 251 conforming pieces. Cell 4 stays on stop ship until Nils signs the requalification and Renae has the laser report in hand. I'll issue the formal notice this morning.

Dale's disposition on 4419 and 4426 came back Friday. Use-as-is on both, with the perpendicularity data being what made it possible — his stress group said if all they'd had was position they'd have gone to removal, but the tilt values you sent were low enough at the specific pieces to close the analysis. So the twelve pieces Nils ran overnight on 9/18 because he didn't want to answer with "not on the plan" saved somebody eighty hours of disassembly and saved me a conversation with our customer. I've told Dale to say so in his report.

44911 releases this week. Contracts has approved the penalty waiver contingent on the 10/29 date, which per your last note you're now beating.

SCAR closes when the cell 4 requalification lands and the CMM standard issue has a scoped answer. Keep the Friday notes coming — I'd rather have them than not.

One personal note. The email you sent your plant on 9/19, somebody forwarded it to me. I don't know if that was intentional. The line about how the useful answer is the true one, including "I don't know" — I've been doing supplier quality for fourteen years and that is the whole job. I'd have told Priya what I told her regardless, but that email is why I told her twice.

Jae-won
