# Ocotillo Payments Group

## Annual Performance Reviews — Merchant Platform Group

**Review Period:** July 1, 2025 – June 30, 2026
**Reviewer:** Sunita Kapadia, Director, Merchant Platform
**Review Cycle:** FY26 Annual
**Date Prepared:** July 29, 2026

---

### A Note on This Cycle's Constraints

Before the individual reviews, a note that each engineer has also received verbally, because the constraints shaped outcomes in ways that would be dishonest to leave unstated.

Compensation set the FY26 merit pool at 3.1 percent of group salary. The rating distribution permits at most two exceeds-expectations ratings in a group of nine. Engineering was funded for one staff-engineer promotion across all 42 engineers in the organization; that decision is made at the VP level with input from all four engineering directors, and it is not mine to award.

These are real limits and I will not pretend otherwise in the pages below. Where a rating or a number is smaller than the work deserves, I say so plainly. Where the constraint is doing work that my own judgment would not do on its own, I say that too.

---
---

# Performance Review — Tobias Ekwueme

| | |
|---|---|
| **Employee** | Tobias Ekwueme |
| **Title** | Senior Engineer, Merchant Platform |
| **Time in Seat** | 4 years (hired July 2022) |
| **Review Period** | July 1, 2025 – June 30, 2026 |
| **Reviewer** | Sunita Kapadia, Director, Merchant Platform |
| **Overall Rating** | **Exceeds Expectations** |

---

## 1. Goals and Results

### Goal 1 — Lead the tokenization vault rewrite to production (Weight: 45%)

**Target:** Replace the legacy vault with a rewritten service, cut p50 authorization latency below 150 ms, migrate all 8,700 merchant token sets with zero data loss, and complete cutover before the December freeze.

**Result: Substantially exceeded.**

Authorization latency moved from 340 ms to 96 ms at p50 — a 72 percent reduction against a target that asked for 56 percent. Migration completed with zero token loss and zero merchant-facing re-enrollment. Cutover landed November 14, three weeks ahead of the freeze date, which gave the group a margin it turned out to need.

I want to be specific about what made this work rather than summarize it as a win. Three things stand out.

First, the phased read-path cutover. Tobias proposed reading from the new vault while continuing to write to both for six weeks, rather than the flip-and-verify approach the original design called for. That decision cost roughly three weeks of additional engineering time and it is the reason the migration was uneventful. When the token-normalization defect surfaced in week four — the one affecting the 1,900 merchant records with legacy PAN formatting — the old vault was still authoritative and the fix was a code change rather than an incident.

Second, the load model. The synthetic traffic generator Tobias built modeled December volume from three years of historical curves rather than a flat multiplier. It predicted the 4.1 million daily peak within four percent. That is the difference between capacity planning and guessing, and it is why nobody was awake on December 22.

Third, the documentation. The vault runbook is 34 pages and it is the only runbook in the group that a new engineer can follow without asking a question. Fatoumata Diallo used it during her ramp and said as much.

### Goal 2 — Carry December peak without a Sev-1 (Weight: 25%)

**Target:** Zero Sev-1 incidents in the authorization path during the November 15 – January 5 peak window.

**Result: Met, with margin.**

Peak day was December 22 at 4.1 million transactions, an 18 percent increase over the prior December. Zero Sev-1s. Two Sev-3s, both in the reporting path rather than authorization, both resolved inside the window without merchant impact.

The margin matters more than the outcome. Headroom analysis after peak showed the vault running at 41 percent of tested capacity at the December high-water mark. We are not going to have this conversation again next December, and that is worth something I cannot put in a number.

### Goal 3 — Reduce single-point ownership in the authorization path (Weight: 20%)

**Target:** At least two additional engineers approved as reviewers for vault and authorization code by end of Q3.

**Result: Met.**

Two engineers cleared review approval in Q3, a third in Q4. Tobias ran the enablement himself — paired review sessions, a written approval rubric, and a deliberate practice of routing his own changes to the newly approved reviewers rather than to the people who would rubber-stamp them.

I am going to flag this goal because it is the one the group as a whole failed at, and Tobias is the person who did not fail at it. The contrast with the settlement service is instructive and I address it in Marisol Ybarra's review. The point here is that reducing your own indispensability is a senior behavior, it is uncomfortable, and Tobias did it without being asked twice.

### Goal 4 — Technical mentorship (Weight: 10%)

**Target:** Serve as onboarding partner for at least one new hire; contribute to group-level design review.

**Result: Met.**

Onboarding partner for Fatoumata Diallo from September. Her ramp — first production change in week seven against a ten-week target — is her achievement, not his, but the runbooks, the paired sessions, and the deliberate early handoff of a real task in week three were his contribution and they were the right ones.

Design review participation was consistent and substantive. Tobias is the person in the room who asks what happens when this fails, and he asks it early enough that the answer can change the design.

---

## 2. Incidents

No Sev-1 or Sev-2 incidents attributable to work Tobias owned during the review period.

He was incident commander for the March 14 settlement outage, which originated outside his area of ownership. His handling of that incident was correct: he took command at the 52-minute mark when the initial escalation path stalled, established a single communication channel, and made the call to fail over to the read replica at 71 minutes rather than continuing to debug the primary. The postmortem is clean and I have used it as a reference document with two other groups.

---

## 3. Feedback from Teammates and Merchants

Skip-level and peer feedback for Tobias was uniformly strong. Three themes recurred:

**Technical judgment under pressure.** Multiple peers described him as the person they want on a call when something is broken. One phrased it as "Tobias slows the room down, which is the opposite of what everyone else does."

**Availability.** Consistently cited as accessible for questions without making people feel they had cost him something. This is rarer than it sounds.

**Reluctance to claim credit.** Two peers independently noted that Tobias attributes work to the group in settings where he did it himself. I raise this in Section 6 because it is a real career risk, not a virtue.

No merchant feedback names Tobias directly, which is a function of his work living below the merchant-visible layer. The 96 ms number is his merchant feedback.

---

## 4. Response to Self-Assessment

> **From Tobias Ekwueme's self-assessment:** *"In January you told me I was the obvious staff candidate. I took that seriously and I have spent the last six months trying to be worth it. I want to be straightforward that I have taken two recruiter calls since April. I am not looking to leave and I did not pursue either conversation past the first call, but I am not going to sit in this review and pretend I have not been thinking about what happens if the answer is not this year. I would rather hear a hard answer than a soft one."*

You will get the hard answer.

**On what I said in January.** I said it and I meant it. I did not say it carelessly and I am not walking it back. You are the strongest staff candidate in this group and, in my assessment, one of the two strongest in the engineering organization. That assessment has not changed and I have put it in writing to the VP of Engineering twice this cycle, in February and again in June.

**On this year's outcome.** Engineering was funded for one staff promotion across 42 engineers. The decision goes to the VP with input from four directors. I advocated for you and I did not carry it. The promotion went to an engineer in Platform Infrastructure whose case I was not in a position to argue against on the merits, because it was also a strong case.

I am not going to dress that up. You did the work, the work was excellent, and the answer this cycle is no. That is a resource outcome, not a performance outcome, and I want the distinction on the record in a document that goes in your file.

**On what I owe you now.** Three things, and you should hold me to them.

1. **A written promotion case, drafted by September 15**, that goes into the FY27 cycle at the front rather than the middle. I will share the draft with you and take your edits. You should see exactly what is being argued on your behalf.
2. **Visibility above my level.** Your problem is not the quality of your work, it is that three people who vote on staff promotions have never watched you work. I am putting you on the Q1 architecture review for the ISO 8583 migration, which is a VP-attended forum, and I am not presenting your material for you.
3. **A direct answer about timing.** I expect a funded staff slot in FY27 and I expect you to be the leading candidate for it. I cannot guarantee it, and anyone who guarantees you a promotion twelve months out is managing you rather than telling you the truth.

**On the recruiter calls.** Thank you for telling me. You did not have to and most people do not.

I will tell you what I think without pretending my interest is neutral. You are four years into a seat where you have outgrown the title, you have been told you are the obvious candidate, and the answer came back no for reasons that have nothing to do with you. That is the precise circumstance in which good engineers leave, and they are usually right to consider it.

What I would ask you to weigh: the scope you have here is unusual. You rewrote the authorization path of a platform moving 1.4 billion dollars a year, and you did it as the technical owner rather than one contributor among twelve. At a larger company that scope is three levels up. At a smaller one it does not exist. The title lag is real and the scope is also real, and only you can weigh those against each other.

If you decide to go, I will give you a reference that reflects what I have written here. I would rather you stay. I am telling you both of those things at the same time because they are both true.

---

## 5. Rating and Compensation

**Overall Rating: Exceeds Expectations**

This is one of two exceeds-expectations ratings available in a group of nine. Tobias holds one of them without qualification. If the distribution permitted a rating above this one, I would have used it.

**Compensation.** The FY26 merit pool is 3.1 percent of group salary. Tobias receives a **4.6 percent** merit increase, the largest in the group and roughly 148 percent of the pool average. This required taking below-pool increases elsewhere in the group, which I did deliberately.

I want to be honest about the size of this number. A 4.6 percent increase on a senior engineer salary does not correspond to the value of a 72 percent latency reduction on the authorization path of a payments platform, and I am not going to argue that it does. It is the largest number available to me inside a 3.1 percent pool. It is not a fair reflection of the year and I have said so to Compensation in writing.

**Equity.** No refresh grant is available in this cycle for senior engineers outside of promotion. I have flagged this to Compensation as a retention exposure with Tobias named specifically.

---

## 6. Goals for FY27

### Goal 1 — Lead the ISO 8583 migration through architecture approval and Phase 1 (Weight: 35%)

Own the technical design and Phase 1 delivery of the message-format migration. Architecture review presentation by end of Q1. Phase 1 — inbound message parsing on the new format, dual-run against legacy — in production by end of Q3.

This is a staff-scope project and it is assigned to you as one. You present it yourself.

### Goal 2 — Establish the authorization-path technical review function (Weight: 25%)

Formalize what you did informally this year. Design a review standard for changes touching the authorization path, get it adopted across the group, and train two engineers to apply it without you. Success is measured by a quarter in which the standard holds and you did not personally review anything under it.

### Goal 3 — Visible technical leadership above the group (Weight: 25%)

Two artifacts presented to an audience that includes the VP of Engineering: the Q1 architecture review, and one written technical document — a design record, a postmortem, or a platform-direction memo — circulated at the organization level. Content is yours to choose.

I am going to say the uncomfortable part directly. You are consistently the strongest engineer in the room and consistently the least visible one, because you attribute your work to the group. That habit reads as generous inside this team and as absence outside it. Two people who vote on staff promotions cannot describe a thing you have personally built. Fixing that is not self-promotion, it is the job at the next level, and I am making it a weighted goal so that neither of us can treat it as optional.

### Goal 4 — Continued mentorship (Weight: 15%)

Serve as technical mentor for at least one engineer, with an explicit development plan rather than an ad-hoc arrangement. I expect this to be Fatoumata Diallo unless one of you prefers otherwise.

---

## 7. Manager's Closing Statement

Tobias had the strongest year of any engineer in this group and one of the strongest in the engineering organization. The tokenization vault rewrite is the most consequential piece of technical work this platform has absorbed in three years, and it landed early, clean, and with headroom.

He also spent the year being told he was the obvious candidate for a promotion that turned out to have one seat and forty-two people in line for it. He handled that with more grace than I would have.

My commitments for FY27 are in Section 4 and I have written them so that he can hold me to them by name. If Ocotillo loses this engineer, it will be because a compensation structure and a single funded promotion slot were allowed to outrank a four-year record, and the responsibility for that will not sit with him.

**Signature:** Sunita Kapadia, Director, Merchant Platform — July 29, 2026

---
---

# Performance Review — Marisol Ybarra

| | |
|---|---|
| **Employee** | Marisol Ybarra |
| **Title** | Senior Engineer, Merchant Platform |
| **Time in Seat** | 6 years (hired March 2020) |
| **Review Period** | July 1, 2025 – June 30, 2026 |
| **Reviewer** | Sunita Kapadia, Director, Merchant Platform |
| **Overall Rating** | **Meets Expectations** |

---

## 1. Goals and Results

### Goal 1 — Settlement service reliability (Weight: 35%)

**Target:** No more than 60 minutes of unplanned settlement downtime across the fiscal year.

**Result: Exceeded substantially.**

22 minutes of unplanned downtime against a 60-minute target — 63 percent better than goal, and the best reliability year the settlement service has had since it was built.

This is not luck and I want the record to show why. Marisol rebuilt the settlement reconciliation checks in Q1, moving from end-of-batch validation to streaming validation, which is why the February ledger drift was caught at 900 records instead of 40,000. She instrumented the batch scheduler so that a stalled job pages someone at four minutes rather than at the next batch boundary. She personally worked the March 14 outage from the 40-minute mark to resolution.

The settlement service moves 1.4 billion dollars a year and it was down for 22 minutes. That is a genuinely excellent number and it belongs at the top of this review.

### Goal 2 — Pull-request turnaround and review throughput (Weight: 25%)

**Target:** Maintain median PR turnaround at or below 24 hours for changes to the settlement service.

**Result: Missed. Significantly.**

Median turnaround grew from 6 hours at the start of the review period to **3.4 days** by Q4 — roughly 3.4x the target. The trend was monotonic across all four quarters. It did not spike; it drifted, every quarter, in the same direction.

The cause is structural and it is not effort. Marisol is the **only approved reviewer** for the settlement service. Every change to a system that touches every transaction on the platform passes through one person, and that person also carried a full delivery load, a reliability goal she beat by 63 percent, and the March 14 incident.

I want to name my own contribution to this before I go further. The single-reviewer condition on the settlement service has existed for over two years. I knew about it. It appeared in my own risk register in FY25. I did not fund a fix, did not set a goal against it, and did not make it anyone's explicit responsibility. Marisol absorbed the consequences of a decision I made by not making it, and she absorbed it by working more hours rather than by letting things break. The 22-minute downtime number and the 3.4-day review number are the same fact seen from two sides.

That said, the outcome is the outcome and it did real damage, which I cover in Section 2.

### Goal 3 — Grocery chain integration delivery (Weight: 25%)

**Target:** Complete settlement integration for a 400-store grocery merchant by the contracted date in Q3.

**Result: Missed. Delivered five weeks late.**

The slip was five weeks against a contracted date. Three of those five weeks are attributable to review latency on the integration branch — code sat waiting for the only approved reviewer. The remaining two weeks came from a scope change on the merchant side in week three, which was outside our control.

Merchant relationship consequences: the account team held two escalation calls with the merchant's operations director, and Ocotillo issued a service credit. The merchant remains a customer and the integration is live and stable. But we told a 400-store chain a date and missed it by five weeks, and the reason we missed it was internal.

### Goal 4 — Knowledge transfer and reviewer expansion (Weight: 15%)

**Target:** Document settlement service architecture; identify candidates for reviewer approval.

**Result: Partially met.**

Architecture documentation was delivered in Q2 and it is good — 40 pages, accurate, current. Reviewer candidates were identified in Q2. Neither candidate completed approval by end of year.

I asked Marisol why during our Q4 one-on-one and her answer was that she could not find a way to run an approval process while she was the bottleneck the approval process was meant to relieve. That is a real trap and it is a real answer. It is also the goal that, had it been met, would have changed the other three outcomes in this review.

---

## 2. Incidents and Feedback

### The March 14 settlement outage

Marisol was engaged at the 40-minute mark, after the initial escalation from Fatoumata Diallo. From engagement to resolution was 31 minutes. Her diagnosis — batch scheduler deadlock following the schema migration — was correct on the first hypothesis. Her handling of the incident itself was excellent and I have no criticism of it.

### Skip-level feedback

Two engineers raised review turnaround in skip-level meetings with me, in November and again in April. I want to characterize this feedback precisely, because how it was delivered matters.

Neither person criticized Marisol's work, her availability, or her willingness to help. Both went out of their way to say the opposite. The November conversation included the phrase "I don't think this is her fault, I think she's the only person allowed to do it." The April conversation was more frustrated and centered on a specific two-week wait that caused the engineer to context-switch three times.

The substance of the feedback is: the queue is real, it is blocking work, and it has not improved despite being raised. That is legitimate and I told both engineers I agreed with them.

What I also told them, and what I am repeating here: raising this with me rather than only with Marisol was the correct move, because the fix was mine to fund and not hers to work harder at.

### Merchant feedback

The grocery chain's operations director cited "responsiveness and technical depth once engaged" in the post-integration debrief, alongside dissatisfaction with the timeline. Both parts are accurate.

---

## 3. Response to Self-Assessment

> **From Marisol Ybarra's self-assessment:** *"I hit the reliability number and I am proud of it. I also know the review queue got bad and that people were waiting on me. I have thought about this a lot. I do not think I could have done both — I think if I had reviewed faster I would have reviewed worse, and the thing I am protecting is the ledger. But I understand that from the outside it looks like I was slow, and I am not going to argue that people waiting five weeks should feel fine about it."*

Your framing is right and I want to affirm it before I add to it.

You could not have done both. The math does not work. One approved reviewer, a full delivery load, a reliability target on a system that moves 1.4 billion dollars, and an incident load — there is no version of that year where the review queue stays at six hours and the ledger stays correct. You chose the ledger. That was the right choice and I would have made the same one.

Here is what I want to add, and it is the substantive coaching in this review.

**You solved the wrong problem well.** The problem you solved was "how do I review carefully under load." The problem in front of you was "why am I the only reviewer, and what would it take to stop being that." The second problem was harder, less familiar, and involved asking me for something. You did not ask.

I understand why. You identified candidates in Q2, you knew the training would cost weeks you did not have, and you made a judgment that the weeks were not available. But that judgment was yours to escalate rather than yours to absorb. If you had come to me in October and said "I need six weeks of protected time to train two reviewers, and the cost is that the grocery integration slips," I would have said yes. It slipped five weeks anyway, and we got no reviewers out of it.

**On the appearance problem.** You wrote that from the outside it looks like you were slow. I want to correct that, because I am part of the outside and it is not what I see. What I see is an engineer who held a critical system together alone for a year and paid for it in throughput. Nobody who understands the settlement service thinks you were slow.

But your reputation is not built only among people who understand the settlement service, and the engineer who waited two weeks in April is forming a view of you based on the queue rather than on the ledger. That is not fair and it is also happening. The fix is not to work faster. It is to stop being the queue.

---

## 4. Rating and Compensation

**Overall Rating: Meets Expectations**

I want to be transparent about how I arrived at this, because Marisol will look at a 63-percent-better-than-target reliability number and reasonably ask why it did not produce a higher rating.

Two exceeds-expectations ratings were available in a group of nine. Marisol was in genuine contention for the second one. The reliability result is the single best goal outcome by any engineer in this group other than the vault rewrite.

What kept her from it: two of four goals missed, one of them a contracted merchant commitment missed by five weeks, and the knowledge-transfer goal — the one that would have prevented the other misses — left incomplete. A senior engineer is accountable for identifying and escalating a structural constraint on their own work, not only for working inside it. That accountability is the gap.

**I want to state clearly what this rating does not mean.** It does not mean an average year. It does not mean I think the review queue was a performance failure in the ordinary sense. Meets Expectations against goals this demanding, on a system this critical, in conditions I failed to fix, is a respectable outcome and I will say so in any forum where it comes up.

**Compensation.** Marisol receives a **3.2 percent** merit increase, slightly above the 3.1 percent pool. In a normal year the reliability result would have carried more. In a 3.1 percent pool with a 4.6 percent increase going to Tobias Ekwueme, the room above pool average is narrow. I made a deliberate choice to keep Marisol above the line rather than at it.

**On advancement.** Marisol has asked about staff-level advancement in each of the last two cycles and I want to give a direct answer rather than defer again.

The single funded staff promotion in FY26 went outside this group. Marisol was not my nominee this cycle; Tobias Ekwueme was, on the strength of the vault rewrite.

For FY27, the honest assessment is that Marisol's technical depth in settlement is at staff level and her demonstrated scope is not. Staff engineers are evaluated on whether the systems they own function without them. The settlement service does not. Every goal in Section 5 is built around changing that, and if FY27 goes the way it is designed to go, Marisol will have a credible case in FY28. I am not going to promise a faster timeline than I believe.

---

## 5. Goals for FY27

### Goal 1 — Eliminate single-reviewer status on the settlement service (Weight: 35%)

**Target:** Three engineers approved as settlement reviewers by end of Q2. By end of Q3, no more than 40 percent of settlement PRs reviewed by Marisol. By end of Q4, median settlement PR turnaround at or below 24 hours with Marisol reviewing fewer than one in three.

This is the highest-weighted goal in this review and it is deliberately weighted above the reliability goal.

**Resources I am committing:** Twelve weeks of Marisol's capacity are protected for reviewer enablement, removed from delivery commitments and not backfilled with anything. I am reducing her FY27 feature load by roughly 30 percent to create this room. Tobias Ekwueme will share his approval rubric from the authorization path — do not build it from scratch.

**What I am telling you about failure modes.** The way this goal fails is that a delivery emergency arrives in month two and you give the twelve weeks back. If someone asks you for that time, including me, the answer is no and you can cite this document. If I am the one asking, remind me I wrote this.

### Goal 2 — Settlement service reliability (Weight: 25%)

**Target:** No more than 45 minutes of unplanned settlement downtime.

The target tightens from 60 to 45 minutes, well above the 22 achieved this year. This is intentional. You are going to spend a third of your capacity on enablement and I do not want you defending a 22-minute number while doing it. The tightened-but-achievable target is the license to spend time elsewhere.

### Goal 3 — Merchant integration delivery (Weight: 25%)

**Target:** Two committed merchant integrations delivered within one week of contracted date.

The grocery chain slip was expensive and the fix is Goal 1. This goal measures whether Goal 1 worked. I am also asking for something procedural: at the point where any integration is at risk of a slip greater than one week, escalate to me in writing with the cause. Not for tracking — so that I can fund the fix while it is still a fix rather than a postmortem.

### Goal 4 — Documented settlement architecture ownership (Weight: 15%)

**Target:** The settlement architecture document becomes a maintained artifact with a defined review cadence and at least two contributors other than Marisol.

Documentation nobody else edits is documentation that encodes one person's model of the system. The measure of success here is other people's commits, not page count.

---

## 6. Manager's Closing Statement

Marisol Ybarra kept the settlement service up for all but 22 minutes of a fiscal year in which it moved 1.4 billion dollars, and she did it as the only approved reviewer on that system. The cost of that arrangement was a review queue that reached 3.4 days, two escalations from teammates, and a five-week slip on a 400-store merchant integration. Both of those facts are true and neither cancels the other.

The single-reviewer condition was on my risk register for two years and I did not fund a fix. Marisol paid the interest on that debt in hours worked and in reputation with teammates who waited. FY27 pays down the principal, and the resources are committed in Section 5 rather than promised in conversation.

The rating this year is Meets Expectations. My assessment of this engineer is considerably higher than that phrase suggests, and the path to a different rating and a different title runs through making herself less necessary — which is the hardest thing to ask of someone whose value has been defined by being indispensable.

**Signature:** Sunita Kapadia, Director, Merchant Platform — July 29, 2026

---
---

# Performance Review — Fatoumata Diallo

| | |
|---|---|
| **Employee** | Fatoumata Diallo |
| **Title** | Engineer, Merchant Platform |
| **Time in Seat** | 10 months (hired September 2025) |
| **Review Period** | September 8, 2025 – June 30, 2026 (partial year) |
| **Reviewer** | Sunita Kapadia, Director, Merchant Platform |
| **Overall Rating** | **Meets Expectations** *(partial-year; see Section 4)* |

---

## 1. Goals and Results

### Goal 1 — Ramp to independent production contribution (Weight: 40%)

**Target:** First production change merged and deployed within 10 weeks of start date.

**Result: Exceeded. Week seven.**

First production change merged October 24, in week seven against a ten-week target — three weeks early, and the fastest ramp in this group in at least four years.

Context matters for how much weight to put on this. Fatoumata came from embedded systems, which meant learning a distributed payments architecture, a deployment model with no analog in embedded work, PCI-scoped change control, and a codebase of roughly 400,000 lines, all at once. The domain distance was larger than for a typical lateral hire and the ramp was faster anyway.

The week-seven change was not trivial filler, either. It was a fix to retry backoff in the merchant webhook dispatcher, in a path with real failure semantics, and it required understanding why the original backoff was wrong rather than only that it was.

### Goal 2 — Contribute to merchant-facing support resolution (Weight: 25%)

**Target:** Participate in support escalation rotation from Q3; resolve assigned merchant issues within SLA.

**Result: Exceeded.**

Entered rotation in January, one quarter early. Resolved 31 assigned merchant issues, 29 within SLA. Two merchants named her by name in support notes following the May settlement backlog — covered in Section 3.

### Goal 3 — Incident response participation (Weight: 20%)

**Target:** Complete on-call training; carry secondary pager from Q2; escalate appropriately per runbook.

**Result: Partially met.**

Training completed on schedule. Secondary pager carried from November, one month early at her request. Escalation practice was inconsistent, and the March 14 outage is the specific instance. Detail in Section 2.

### Goal 4 — Technical domain learning (Weight: 15%)

**Target:** Demonstrate working knowledge of settlement, tokenization, and authorization paths by end of year.

**Result: Met.**

Settlement and authorization knowledge is solid and demonstrated in code review and incident participation. Tokenization is thinner, which is expected — the vault rewrite consumed that area for most of the year and there was limited room for a new engineer inside it. Addressed in FY27 goals.

---

## 2. Incidents

### March 14 settlement outage — escalation delay

**What happened.** Fatoumata was on secondary pager. Settlement batch processing stalled at 02:14. Automated alerting fired at 02:19. She acknowledged at 02:23 and began investigating. Per runbook, settlement batch stalls escalate to the primary settlement owner at the 10-minute mark if not resolved. She escalated at 03:03 — **40 minutes past the runbook threshold**.

Total incident duration was 71 minutes. Marisol Ybarra resolved it 31 minutes after engagement. A meaningful portion of the 40-minute delay was recoverable time.

**Why it happened.** From the postmortem and from my conversation with Fatoumata: she believed she was close to a diagnosis. She was partly right — she had correctly identified that the stall followed the schema migration deployed the previous evening, which was the right thread. She was pulling on the right thread and did not know that pulling on it alone was the wrong choice.

Underneath that was a second thing she named herself in the postmortem: she did not want to wake a senior engineer at two in the morning for something she thought she could handle.

**My assessment.** The delay was a real error with real cost, and it was a predictable error for a strong new engineer in month six. Every engineer who is competent and new makes some version of it. The failure mode of a weak engineer is escalating too fast; the failure mode of a strong one is escalating too slow. Both are errors and only one of them tells you the person can think.

I also hold the runbook partly responsible. The escalation criterion was a time threshold with no guidance on what to do when you have a promising hypothesis. That gap has since been closed — Fatoumata closed it. The current runbook says explicitly that a promising hypothesis is not a reason to hold escalation, and it says so because she wrote that line after her own postmortem.

**Corrective actions taken.** Postmortem authored by Fatoumata within 72 hours, blameless format, presented to the group. Runbook amended. Two on-call shadowing shifts with Tobias Ekwueme in April. No escalation timing issues in the 15 weeks since.

### May settlement backlog — same-day resolution

Fatoumata identified a queue-consumer configuration defect during the May backlog and shipped a fix the same day, clearing the backlog for affected merchants before end of business. Two of those merchants named her in support notes. This is the counter-instance to March 14 and it is not a coincidence that it came after it.

---

## 3. Feedback from Teammates and Merchants

### Merchant feedback

Two merchants named Fatoumata directly in support notes following the May settlement backlog. Both are worth quoting:

> *"Fatoumata called us back within the hour with an actual explanation rather than a ticket number, and told us when it would be fixed. It was fixed when she said it would be."*
> — Merchant operations contact, regional restaurant group

> *"First time in two years someone from the platform side explained what happened in language I could repeat to my own finance team."*
> — Merchant controller, specialty retail

Direct merchant recognition of an engineer ten months into the seat is unusual at Ocotillo. I have forwarded both notes to the VP of Engineering.

### Teammate feedback

Peer feedback was strong. Recurring themes:

**Question quality.** Multiple peers noted that her questions are well-formed — she arrives having read the code and having a hypothesis, and the question is about the gap between the hypothesis and the behavior. Tobias Ekwueme's comment: "She asks questions I have to think about."

**Debugging instinct from embedded.** Two peers noted she reaches for instrumentation and reproduction earlier than most engineers in the group, which several attributed to her embedded background. This is a genuine transfer of skill and I would like to see it spread.

**Self-criticism.** Three peers, unprompted, noted that she is harder on herself than the situation calls for, with two referencing March 14 specifically. One phrased it: "She apologized to me for that outage and I wasn't even on the call."

---

## 4. Response to Self-Assessment

> **From Fatoumata Diallo's self-assessment:** *"I want to ask directly rather than wonder about it: does the March 14 outage follow me? I escalated 40 minutes late and I know that made the outage longer than it had to be. I have read the postmortem probably ten times. I understand this is my first review here and I do not want the first thing written about me to be the thing I got wrong, but I would rather know than guess."*

I am going to answer this as plainly as I can, because you asked plainly and because you have apparently been carrying it for four months.

**No. It does not follow you.**

Here is the specific, concrete version of that answer, so it is not just reassurance.

**In this document.** The incident appears in Section 2, described accurately, alongside the corrective actions and the fifteen clean weeks since. It does not appear in your rating rationale as a limiting factor. It does not appear in my closing statement. The document that goes in your file describes a week-seven ramp against a ten-week target, two merchants naming you by name, and one escalation error in month six that you fixed and then fixed the runbook so it would not happen to the next person.

**In how I talk about you.** I have described you to my peers and to the VP of Engineering four times this year. March 14 came up once, in the context of the postmortem being unusually good. The other three times were the ramp and the May fix.

**In your file, mechanically.** The postmortem is blameless-format and attached to the incident record, not to your personnel record. Nothing about March 14 appears in your compensation history or your promotion file.

**Now the part that is more useful than reassurance.**

March 14 is going to matter to your career, but not in the direction you are worried about. The engineers who become senior are, without exception, the ones who made a judgment error early, understood the actual mechanism of it, and changed how they operate. The mechanism in your case was not "I was slow." It was: *you were reasoning well, you knew you were reasoning well, and you let the quality of your reasoning substitute for the judgment about whether reasoning alone was the right move at 02:40 on a settlement outage.*

That is a specific and durable lesson. It will recur in different clothing for the rest of your career — the moment where you are genuinely close and the right call is still to bring in more people. You now have a real instance of it to reason from. Most engineers get that lesson at year four instead of month six, and by then it costs more.

The thing I would actually correct is not the escalation. It is the ten re-readings. Three peers told me independently that you are harder on yourself than the situation warrants, and one of them said you apologized to someone who was not on the call. A calibrated relationship to your own errors is a professional skill and it is one you are currently underweight on. Overcorrecting toward self-criticism will make you slower to take risks, slower to make calls under pressure, and eventually slower to escalate — which is the opposite of what you want.

Read it once more for the mechanism. Then close it.

---

## 5. Rating and Compensation

**Overall Rating: Meets Expectations** *(partial-year)*

Fatoumata was in the seat for approximately ten months and is rated against ramp-year expectations rather than full-year senior contribution. Against those expectations, the year was strong — a ramp three weeks ahead of target, early entry into support rotation, direct merchant recognition, and one significant judgment error corrected.

**Why this is not Exceeds Expectations, stated directly.** Two exceeds ratings were available in a group of nine. Tobias Ekwueme holds one. The second was contested between Marisol Ybarra and Fatoumata, and I gave it to neither.

My reasoning: exceeds-expectations at Ocotillo is a full-year rating and Fatoumata was here for ten months of it, including two months in which she was not yet productive by design. Rating a ramp year above a colleague's delivery year would not survive comparison, and the distribution forces that comparison whether I want it or not.

**What I want understood:** in a year without a two-rating cap, this would likely have been rated higher. This is a ceiling I ran into, not a judgment I made. Fatoumata should read Meets Expectations, on a partial year, in a capped distribution, as a strong first-year result — and should expect a different conversation in FY27 when she is measured against a full year of full expectations.

**Compensation.** Fatoumata receives a **3.4 percent** merit increase, above the 3.1 percent pool average and the second-largest in the group.

I will note the constraint honestly: a strong performer with ten months of tenure is competing for pool dollars against engineers with four and six years of accumulated contribution, and tenure carries weight in how compensation structures increases. 3.4 percent is a good outcome inside that structure. It is not what a week-seven ramp and direct merchant recognition would command on the open market, and I would rather Fatoumata hear that from me than discover it elsewhere.

**On advancement.** Fatoumata is not eligible for promotion consideration in FY27 — the senior-engineer threshold at Ocotillo requires 24 months of tenure and this is month ten. That is a policy floor and not a performance judgment.

The realistic path: FY27 is the year to build the case, FY28 is the year to make it. Section 6 is designed with that timeline in mind. If FY27 goes the way this year did, Fatoumata will be promoted at the first cycle she is eligible for, and I will say so in writing at that time.

---

## 6. Goals for FY27

### Goal 1 — Full ownership of a merchant-facing service component (Weight: 30%)

**Target:** Take primary ownership of the webhook dispatch and merchant notification subsystem, including on-call primary, roadmap input, and design authority for changes within the component.

This is a deliberate step up. It is a real component with real merchant impact and it is small enough to hold at your tenure. Ownership means the decisions are yours, including the ones you get wrong.

### Goal 2 — Become an approved reviewer for the settlement service (Weight: 25%)

**Target:** Complete settlement reviewer approval by end of Q2. From approval, carry a minimum of 25 percent of settlement PR review volume.

This is coordinated with Goal 1 in Marisol Ybarra's review. She has twelve weeks of protected capacity to train reviewers and you are the first candidate.

This is the highest-leverage thing you can do for this group in FY27. The single-reviewer condition on settlement cost us a five-week merchant slip this year. You are in a position to be part of why that does not happen again, in month twelve of your tenure, which is unusual and which I want you to notice.

### Goal 3 — Incident command readiness (Weight: 20%)

**Target:** Carry primary pager from Q2. Serve as incident commander for at least two Sev-3 incidents by end of year. Zero escalation-timing deviations from runbook.

I am putting the escalation-timing criterion in writing not because I am concerned about it, but because I want you to have an explicit, measurable, closed-out version of March 14 in a document rather than an open question in your head. You will meet this goal. When you do, it is finished.

The incident-command component is the growth edge. Commanding is a different skill from debugging — it is about coordinating people while the system is broken, and the hardest part is not doing the technical work yourself.

### Goal 4 — Tokenization and authorization path depth (Weight: 15%)

**Target:** Complete at least two substantive changes in the tokenization or authorization path, with Tobias Ekwueme as technical mentor.

Settlement and authorization knowledge is solid; tokenization is the gap, for good structural reasons. The vault is now stable and there is room to learn inside it. Tobias will mentor this under Goal 4 of his own review.

### Goal 5 — Embedded-systems practice transfer (Weight: 10%)

**Target:** Deliver one internal technical session on instrumentation and reproduction practice drawn from embedded-systems work.

Several peers independently noted that you reach for instrumentation earlier than the rest of the group. That is a transferable practice this team would benefit from, and teaching it will do more for your visibility than another quarter of good delivery. It also gets you in front of people who will eventually vote on your promotion.

---

## 7. Manager's Closing Statement

Fatoumata Diallo had the strongest first year of any engineer I have hired into this group. She shipped production code in week seven against a ten-week target, entered support rotation a quarter early, and was named by two merchants in support notes — something most engineers here have never had happen.

She also escalated forty minutes late on a settlement outage in month six, wrote an unusually good postmortem about it, amended the runbook so the next person would not repeat it, and has had fifteen clean weeks since. She asked in her self-assessment whether that incident would follow her. It will not, and the fuller answer is in Section 4.

The rating is Meets Expectations on a partial year in a capped distribution, and it understates the year. Fatoumata is not promotion-eligible until FY28 on tenure grounds alone. My job in FY27 is to give her scope that outruns her tenure so that the case is unarguable when the calendar finally permits it, and Section 6 is built for that.

**Signature:** Sunita Kapadia, Director, Merchant Platform — July 29, 2026

---
---

## Reviewer's Summary — Merchant Platform Group, FY26

| Employee | Title | Rating | Merit Increase |
|---|---|---|---|
| Tobias Ekwueme | Senior Engineer | Exceeds Expectations | 4.6% |
| Marisol Ybarra | Senior Engineer | Meets Expectations | 3.2% |
| Fatoumata Diallo | Engineer | Meets Expectations *(partial year)* | 3.4% |

**Group merit pool:** 3.1% | **Exceeds ratings used:** 1 of 2 available | **Staff promotions awarded:** 0 of 1 organization-wide slot

**Notes filed with Compensation and the VP of Engineering:**

1. Retention exposure flagged for Tobias Ekwueme. No equity refresh available at senior level absent promotion; engineer has disclosed inbound recruiter contact. Requesting an off-cycle equity review in Q1 FY27.
2. FY27 staff promotion nomination for Tobias Ekwueme to be submitted September 15, 2026, in advance of the standard cycle.
3. Single-reviewer risk on the settlement service, carried on the group risk register since FY24, materialized in FY26 as a five-week merchant integration slip and two teammate escalations. Twelve weeks of engineering capacity committed to remediation in FY27. This risk was mine to fund and I did not fund it in time.

**Sunita Kapadia**
Director, Merchant Platform
Ocotillo Payments Group — Tempe, Arizona
July 29, 2026
