# Quarry Street Systems — Internal Memo Packet

---

TO: All Employees
FROM: Dolores Kaminski-Lim, Chief Product Officer
DATE: September 15, 2026
SUBJECT: Terminal Migration Program — March 31, 2027 Gateway Sunset

I'm writing to open a company-wide effort that will occupy a significant share of our attention through the first quarter of next year, and to make sure everyone understands why.

Our card-present processing partner has confirmed, in writing, that it will decommission the legacy authorization gateway on March 31, 2027. This is not a soft deadline or a renewal notice — it is a hard cutover. On that date, any terminal still pointed at the old gateway loses the ability to authorize card transactions. There is no grace period and no fallback path from the processor's side. For a restaurant, that means a terminal that works perfectly on March 31 stops taking cards entirely on April 1.

**What we've found.** Engineering and platform reliability have spent the last several weeks auditing our installed base. Of the roughly 4,100 independent restaurants running Quarry Street point-of-sale and payments hardware across New England, 900 are running terminals — mostly first-generation countertop units and a smaller number of pre-2020 tablets — that cannot accept the firmware update required to move to the new gateway. These merchants require either a firmware path we don't yet have or, in most cases, a full hardware swap.

**Why this is urgent.** We have roughly 28 weeks between today and the sunset date. To finish with any real margin for holidays, weather, no-shows, and the inevitable slippage that comes with coordinating installs across hundreds of independent, busy restaurants, we need to be converting merchants at a sustained pace of 75 a week starting now. That number only goes up the longer we wait to hit it. If we are still ramping in December, the math stops working.

**What this program touches.** This is not a support-desk project or an engineering project. It touches nearly every function in the company:

- Engineering and platform reliability, under Rohan Talwar, own the technical rollout — packaging the firmware update where it's viable, validating the new gateway integration, and building the tooling we'll use to track merchant-by-merchant status.
- Merchant support, under Amara Bakr, owns scheduling, inbound calls, and the merchant-facing communication cadence. Amara's team will publish a detailed outreach and escalation policy in the coming weeks; expect more from her directly.
- Finance, under Nathan Rosenblum, is finalizing the capital plan for the hardware replacements themselves — how many units we buy, on what terms, and how the cost is absorbed. Nathan will communicate the operating plan separately.
- Product is finalizing which replacement terminal SKUs we offer to merchants who need a full swap versus a firmware-only path, and building the self-service tools merchants will use to check their own status.

**What I'm asking of every team lead.** Between now and March 31, this migration is the top company priority, ahead of other roadmap commitments. If your team's plan conflicts with the migration's needs, raise it with me directly rather than deferring quietly. I would rather reshuffle a roadmap in September than discover in February that we're behind.

**How we'll track this.** Starting the first week of October, I will publish a weekly migration dashboard to the leadership team showing merchants converted, merchants remaining, and pace against the 75-a-week target. I want this visible, not something we discuss only when it's already a problem.

**What happens if we miss the date.** I want to be direct about the stakes rather than soften them. Every merchant still on a legacy terminal on March 31, 2027 stops accepting cards that day. For an independent restaurant, that is not an inconvenience — it is an existential threat to their business for as long as it takes us to get them converted afterward. We are the reason they'd be in that position, and we will treat every one of those 900 merchants accordingly between now and then.

I know this is a lot to absorb, and more detail is coming from each of the functional leads named above over the next month. For now, the two things I want everyone to carry out of this memo are the date — March 31, 2027 — and the number — 900 merchants who are not ready for it as of today. We have time to fix this if we start now.

Questions can come to me directly or through your manager.

— Dolores

---

TO: Engineering
FROM: Rohan Talwar, Head of Platform Reliability
DATE: November 3, 2026
SUBJECT: PCI Assessment Findings and Remediation Schedule

The external assessor completed our periodic PCI assessment in October, and the report is in. I want to walk engineering through the findings directly rather than let this circulate as a summary slide, because several of these findings require real work from this team before our next attestation in May, and I want no ambiguity about ownership or timeline.

**The seven findings.** In descending order of severity as scored by the assessor:

1. **Encryption key rotation has not executed since 2023.** This is the finding I'm most concerned about. Our documented policy calls for annual rotation of the keys used for cardholder data encryption at rest and for terminal-to-gateway session encryption. The last rotation on record is from October 2023. We are two cycles behind policy, and the assessor flagged it as a material gap rather than a documentation lapse.
2. **Access control review overdue.** Quarterly access recertification for systems in scope of the cardholder data environment has not been performed since Q1 of this year. We have accounts with standing access that should have been revalidated three times over.
3. **Deprecated TLS cipher suites still enabled** on two of the gateway-facing load balancers. These are ciphers we stopped issuing in new configs over a year ago but never fully retired from the existing fleet.
4. **Log retention below the required window** on the transaction audit trail for one of the three regions we operate in — currently 60 days against a 90-day minimum.
5. **Vendor risk assessments lapsed** for two subprocessors we rely on for tokenization services. Annual reassessment was due in the spring and was not completed.
6. **Incident response plan untested.** We have a written plan but no tabletop exercise on record in the last 18 months.
7. **Network segmentation gap** between point-of-sale processing systems and back-office reporting systems in our secondary data center, which does not mirror the segmentation we have in the primary.

**Why this matters on our timeline.** All seven need to be remediated before the May attestation, but finding one is the one that will draw the most scrutiny, and it is also the one most entangled with the terminal migration work already underway. Key rotation touches the same session-key handling that the new gateway integration depends on, which means we have an opportunity — and a requirement — to do this work once, correctly, rather than rotate keys now and touch the same code path again during the gateway cutover.

**Key rotation plan.** I'm setting the following schedule:

- By November 14: complete an inventory of every key currently in scope, confirm which are managed through our HSM and which are legacy file-based keys that predate it.
- By November 21: execute rotation for all HSM-managed keys. This should be low-risk and largely automated.
- By December 12: execute rotation for the legacy file-based keys, which requires a coordinated cutover window with support and account teams, since a subset of pre-2020 terminals validate against these keys directly. I want this scheduled with Amara's team so it doesn't collide with active migration installs that week.
- By January 9: full rotation confirmed complete, documentation updated, and a dry run of the new gateway session-key handshake using rotated keys, ahead of the broader migration ramp.

**Owners for the remaining six.**

- Access control review: owned by the platform reliability team, target completion December 5.
- TLS cipher cleanup: owned by infrastructure, target completion November 21.
- Log retention: owned by the data platform team, target completion December 1.
- Vendor risk reassessments: owned by security, in coordination with legal, target completion December 19.
- Incident response tabletop: owned by me directly, scheduling a cross-functional exercise for the week of January 12.
- Network segmentation: owned by infrastructure, target completion February 6, the longest lead item on the list given the physical work required in the secondary data center.

I recognize this lands in the same window as the terminal migration ramp and, separately, the staffing changes the company announced last month. I don't have slack to offer on the May attestation date — it is fixed — so I need each owner above to flag immediately, not at the deadline, if something is going to slip. I would rather move a resource in December than explain a missed finding in May.

I'll send a two-week status update to this list until all seven are closed.

— Rohan

---

TO: Executive Team and Department Leads
FROM: Nathan Rosenblum, Chief Financial Officer
DATE: November 12, 2026
SUBJECT: Revised Operating Plan — Hardware Subsidy Commitment and Staffing Reduction

This memo covers two decisions the board finalized last week and lays out how they interact with the migration program Dolores opened in September. Both are difficult, and I want to be transparent about the reasoning rather than let either land as an unexplained line item.

**Where we stand financially.** We are carrying $48 million in annual recurring revenue against a cost structure that has grown faster than that revenue for two consecutive quarters. The board's view, which I share, is that we needed to correct that before taking on the capital commitment the terminal migration requires. That correction takes two forms: a workforce reduction and a hardware financing decision, both described below.

**Staffing reduction.** The board approved a reduction of 29 positions, roughly 14 percent of the company, effective this month. This includes six of our 22 merchant support agents. I want to address that specific number directly because I know it will be the one people focus on: we are reducing merchant support headcount by more than a quarter at the same time we expect support call volume to roughly triple during the migration window. That is a real tension, not an oversight. Amara is publishing a revised support and escalation policy separately that reflects how her team will manage volume with fewer agents — prioritization by merchant risk, expanded self-service, and temporary contract support during peak weeks. I'd ask leads not to treat the two decisions as contradictory in isolation; they were sized together, with the expectation that outreach efficiency has to improve to compensate for the headcount reduction.

**Hardware subsidy commitment.** Replacing the 900 terminals that cannot take the firmware update costs $2.6 million if we purchase at standard volume pricing over the course of the migration. Our hardware vendor has offered materially better terms — $1.5 million total, a savings of $1.1 million — if we commit to a 3,000-unit order by December 15. The difference is driven by their manufacturing batch scheduling; 3,000 units lets them run a single production lot rather than staggered smaller orders, and they're passing part of that efficiency back to us contractually.

I am recommending, and the board has now approved, that we take the committed pricing. Practically, this means:

- We will order 3,000 units by December 15, roughly 2,100 more than the 900 we currently need for this migration. The additional units become our standing replacement inventory for normal hardware attrition and future customer growth over the next 18 to 24 months, so this is not purely excess capacity — it pulls forward a purchase we'd have made anyway, at a better price.
- The $1.1 million in savings is committed capital efficiency, not discretionary budget. It reduces what we need to draw against our credit facility for this program; it does not create a new pool of unallocated cash. I want to be specific about this now because I expect questions about alternative uses for that savings, and I'll address one directly below.

**On the proposal to redirect hardware savings to merchant retention.** Several members of the account team have raised, informally and now formally, that the $1.1 million saved on hardware should instead fund a retention incentive program for merchants affected by the migration — discounts, credits, or similar goodwill gestures. I understand the instinct. I don't think it's the right use of this specific dollar, for two reasons. First, the $1.5 million commitment is not a discretionary spend we're choosing to reduce; it's a capital purchase already built into this quarter's financing plan, and the "savings" only exist relative to the $2.6 million alternative — they were never cash sitting idle. Second, and more importantly, the single most effective retention action available to us is finishing the migration on time. A merchant who loses card acceptance on March 31 because we didn't get to them is a merchant we are far more likely to lose permanently than one we spend the intervening months getting installed. I'd rather put marginal dollars behind moving the migration pace up than behind incentives layered on top of a program that hasn't yet hit its targets. Kwabena is addressing the pace question directly in his January update, and I expect this will come up there again; I wanted the financial framing on record first.

**Bottom line.** We are entering Q1 2027 leaner in headcount, committed to a $1.5 million hardware order, and dependent on the migration hitting its pace targets to make both of those decisions look correct in hindsight. I'll circulate updated budget-to-actual reporting monthly through Q1.

— Nathan

---

TO: Merchant Support Team and Account Management
FROM: Amara Bakr, Director of Merchant Support
DATE: December 8, 2026
SUBJECT: Support Escalation and Merchant Outreach Policy for the Migration Window

This memo sets the operating policy for merchant support through the end of the terminal migration program. I'm publishing it now, three weeks after the staffing reduction took effect, because I want the team working from a single, specific plan rather than improvising case by case as volume increases.

**Where we stand.** We are a team of 16 agents, down from 22 as of last month's reduction, supporting all 4,100 merchants on our platform, with the 900 affected by the gateway sunset requiring direct, individual scheduling and follow-through between now and March 31. Migration-related contact volume is already running well above baseline and is expected to roughly triple at peak versus a normal month. I will not pretend the reduced headcount and the volume increase net out evenly — they don't, and this policy is built around closing that gap through prioritization and process rather than pretending it isn't there.

**Prioritization criteria.** Not all 900 merchants carry equal urgency, and we will treat them accordingly. Merchants are sorted into three tiers:

- **Tier 1 — highest risk:** merchants on the oldest terminal hardware with no interim firmware path, and merchants processing above our median transaction volume, since they have the most to lose and the least flexibility to route around an outage. These merchants get proactive outreach, not just inbound response, and a named scheduler.
- **Tier 2 — standard:** merchants requiring a firmware update but not a full hardware swap, where the install is faster and the risk of falling behind schedule is lower.
- **Tier 3 — self-sufficient:** merchants who, based on prior support history, are comfortable completing a guided self-service update with phone support available but not required.

Engineering's rollout schedule and my team's calendar are being merged into a single tracker so that Tier 1 merchants are never more than two weeks out from a scheduled install date once they're identified.

**Escalation tiers.** Front-line agents handle standard scheduling, rescheduling, and status questions. Anything involving a merchant who reports they are within 30 days of losing card acceptance and has no install scheduled escalates immediately to a shift lead, same day, not queued. Anything involving a Tier 1 merchant who has missed two scheduled install windows escalates to me directly. I would rather be pulled into a case too early than find out about a missed Tier 1 merchant after the fact.

**Outreach cadence.** Every Tier 1 merchant receives outreach at minimum once every two weeks until an install date is confirmed, then again 48 hours before the scheduled install. Tier 2 and 3 merchants receive outreach on a six-week cadence until scheduled. Outreach happens by phone first, not email, for Tier 1; our merchants are independent operators running restaurants during service hours, and a missed email is not a substitute for a live conversation about losing the ability to take payment.

**Capacity measures.** To manage volume against the reduced headcount, we are: bringing on eight contract agents for a 10-week period covering peak call volume in January and February; expanding the self-service status portal so Tier 3 and low-complexity Tier 2 merchants can check and reschedule installs without a call; and setting a target average handle time of eight minutes for routine scheduling calls, down from eleven, achieved through a revised call script rather than rushing merchants.

**Coordination with engineering.** Rohan's team is running a key-rotation cutover for legacy file-based keys in mid-December that affects a subset of pre-2020 terminals. My schedulers have the affected merchant list and will not book Tier 1 installs for those merchants during that window to avoid double-touching the same account.

**What success looks like.** By the last week of February, I want every Tier 1 merchant either installed or on a confirmed calendar date inside the following two weeks. That is the measure I will report against, not aggregate call volume, because aggregate volume can look fine while the merchants who matter most fall through.

I know this is a demanding stretch for a smaller team. I'll be on the floor during peak call hours through January, and I want any agent who sees the tiering breaking down in practice to tell me directly rather than wait for the next review.

— Amara

---

TO: Executive Team and Board
FROM: Kwabena Asante, Vice President of Engineering
DATE: January 26, 2027
SUBJECT: Migration Status — January and Response to the Retention Reallocation Proposal

This is my scheduled update on terminal migration pace, and I'm also using it to respond directly to the proposal, raised again by several members of the account team this month, that the hardware subsidy savings should be redirected to merchant retention incentives rather than the terminal order.

**Current pace.** We are converting merchants at approximately 40 a week, against the 75 a week required to finish the remaining installs with adequate margin before March 31. We have completed roughly 280 of the 900 affected merchants since the program opened in September, leaving about 620 with nine weeks remaining before the sunset date. At the current rate, we finish in mid-June, roughly eleven weeks past the deadline. I want to state that plainly rather than qualify it: on the current trajectory, we miss the date for a meaningful number of merchants.

**Why we're behind.** Three factors, in order of impact. First, the reduced support headcount from November's reduction has slowed scheduling throughput more than the tiering policy Amara published in December has been able to offset so far, though her team reports the Tier 1 list is now current and the two-week install window target is holding for merchants once they're scheduled — the bottleneck is upstream of that, in initial contact and scheduling capacity. Second, the December key-rotation cutover Rohan's team ran, while necessary for the PCI remediation and correctly sequenced to avoid touching legacy terminals twice, consumed installer bandwidth for roughly ten days in a way we underestimated when we set the original 75-a-week target. Third, a subset of Tier 1 merchants — call it 60 to 80 accounts — require on-site hardware swaps rather than remote firmware updates, and we have fewer certified installers than we assumed we'd have by this point in the program.

**Response to the retention reallocation proposal.** I understand why this keeps coming up, particularly from the account team, who are the ones fielding merchant frustration directly. I don't think redirecting the hardware subsidy savings to retention incentives is the right move, for reasons that are somewhat different from Nathan's November memo but arrive at the same conclusion.

The $1.1 million difference between the $2.6 million standard-pricing cost and the $1.5 million committed-volume cost was locked in on December 15 when we placed the 3,000-unit order. That capital decision is closed; the units are in production. There is no undrawn pool of savings sitting available for reallocation — the number only ever existed as an avoided cost against a purchase we were always going to make. Redirecting it now would mean either canceling part of a manufacturing commitment already in motion, which the vendor has told us is not possible without forfeiting the pricing entirely, or drawing new money from elsewhere in the budget, which is a different decision than the one being proposed and should be evaluated on its own terms if the account team wants to make that case to Nathan directly.

More to the point: I don't believe incentive spending is what closes our gap. Our problem is not that merchants don't want to be migrated — it's that we are not reaching and installing them fast enough. A retention credit does nothing for a merchant whose terminal stops accepting cards on March 31 because no installer visited. The highest-value use of any incremental dollar right now is capacity to convert merchants faster, not compensation for the risk that we don't.

**What I'm doing instead.** I've approved three changes, effective this week, funded from the existing engineering and operations budget rather than any hardware line: adding four contract installers through a staffing vendor we've used before, bringing our on-site install capacity from six to ten teams; authorizing weekend install slots for Tier 1 merchants for the next seven weeks; and moving two engineers temporarily off secondary roadmap work to build a faster remote-provisioning path for the subset of Tier 2 merchants who don't require an on-site visit, which should let Amara's team route more volume away from scarce on-site installer time.

**Where this leaves the date.** With these changes, I project we can reach 65 to 70 a week by mid-February and hold there through the remaining weeks, which gets us to substantially all 900 merchants converted by the March 31 deadline, with a small tail — likely under 40 merchants — carrying into the first two weeks of April. I will not tell the board we are certain to hit zero past the deadline; I think that would be dishonest given where we stand today. I will tell you that the plan above is the fastest path I can build without a further capital ask, and that I'll report weekly rather than monthly for the remainder of the program so this board sees pace movement in real time rather than at month-end.

I'm available to walk through any of this in more detail before the next board meeting.

— Kwabena

**Attachment: Weekly Migration Tracking — Detail by Region**

| Week Ending | Merchants Converted (Weekly) | Cumulative Converted | Remaining | Installer Teams Active |
|---|---|---|---|---|
| Sept 20 | 12 | 12 | 888 | 4 |
| Sept 27 | 18 | 30 | 870 | 4 |
| Oct 4 | 22 | 52 | 848 | 5 |
| Oct 11 | 26 | 78 | 822 | 5 |
| Oct 18 | 29 | 107 | 793 | 5 |
| Oct 25 | 31 | 138 | 762 | 6 |
| Nov 1 | 33 | 171 | 729 | 6 |
| Nov 8 | 30 | 201 | 699 | 6 |
| Nov 15 | 27 | 228 | 672 | 6 |
| Nov 22 | 19 | 247 | 653 | 5 |
| Nov 29 | 14 | 261 | 639 | 5 |
| Dec 6 | 22 | 283 | 617 | 6 |
| Dec 13 | 8 | 291 | 609 | 6 |
| Dec 20 | 6 | 297 | 603 | 6 |
| Dec 27 | 9 | 306 | 594 | 6 |
| Jan 3 | 24 | 330 | 570 | 6 |
| Jan 10 | 38 | 368 | 532 | 6 |
| Jan 17 | 41 | 409 | 491 | 6 |
| Jan 24 | 40 | 449 | 461 | 6 |

Note the drop across the December 13 and December 20 weeks, corresponding to the key-rotation cutover Rohan's team ran on legacy file-based keys; installer teams were pulled to support the cutover validation rather than new installs during that window, which is the single largest visible dent in cumulative pace on this table. The January recovery reflects the tiering policy taking hold and the additional contract installers coming online mid-month, not yet the four additional installers or weekend slots approved in this memo, which begin the week of February 2.

Regional breakdown as of January 24:

- **Greater Boston (312 affected merchants):** 201 converted, 111 remaining. This region has our highest installer density and is tracking closest to the recovery pace needed.
- **North Shore / Merrimack Valley (188 affected merchants):** 94 converted, 94 remaining. Behind plan; two of our six certified installers are based in this region and have been pulled twice to cover Boston shortfalls.
- **Central and Western Massachusetts (241 affected merchants):** 98 converted, 143 remaining. Longest average drive time between installs, which caps daily throughput per team regardless of scheduling efficiency.
- **Rhode Island and Southeastern Massachusetts (97 affected merchants):** 41 converted, 56 remaining. On pace.
- **New Hampshire, Vermont, and Maine (62 affected merchants):** 15 converted, 47 remaining. Lowest installer coverage of any region; this is where I intend to route two of the four new contract installers first.

I'm attaching this level of detail because I want the board looking at the same numbers I am rather than a rolled-up percentage. The Central/Western Massachusetts and northern New England regions are where the plan is most fragile, and where I'd want any board question focused if there's appetite to discuss further capital for regional installer capacity beyond what I've already authorized from the existing budget.

— Kwabena

**Attachment B: Installer Capacity and Cost Detail**

The four additional contract installers approved in this memo are sourced through the same staffing vendor we used for the original six-team buildout in September, at a blended rate of $58 per hour including travel time, versus $71 per hour for a comparable increase in permanent headcount once benefits and onboarding are included. Contract terms run through April 30, with an option to extend two additional weeks if the tail described above runs past mid-April. Total incremental cost for the four installers through the contract period is approximately $187,000, funded from the engineering operating budget already approved for Q1, not from any hardware line item.

Weekend install slots for Tier 1 merchants carry a 1.5x rate for the same installer pool rather than a separate hire, since weekend work is voluntary overtime for staff already certified on our hardware. Based on the six teams currently active, I expect four to five to opt into weekend availability in any given week, adding roughly 8 to 10 additional installs per weekend across the program. That capacity is reflected in the 65-to-70-a-week projection above; it is not incremental to it.

The remote-provisioning path the two reassigned engineers are building is intended to qualify for automated deployment any Tier 2 merchant running a terminal manufactured after 2018 that only needs the firmware update itself, without a physical hardware swap. Based on Amara's tiering data, that's approximately 340 of the 461 remaining merchants as of January 24. If the tool ships on the timeline the team committed to — a working version by February 13, full rollout by February 27 — it removes the majority of Tier 2 volume from the on-site installer queue entirely, which is the single largest lever in this plan. I've flagged to both engineers that this date is not soft; if it slips past the end of February, we lose the benefit for the weeks that matter most, since the on-site teams will already be at capacity handling the Central and Western Massachusetts backlog.

I want to be clear that the remote-provisioning tool is the piece of this plan I'm least certain about, not because the engineering work is unusually hard but because it hasn't been attempted at this volume before on our platform. If it underperforms, the fallback is simply more on-site installer hours, which is a cost question rather than a feasibility question, and one I'd rather bring to Nathan directly in mid-February with real data than raise now as a hypothetical.

I'll fold updated cost figures into next week's tracking memo once the four contract installers are confirmed and scheduled.

— Kwabena
