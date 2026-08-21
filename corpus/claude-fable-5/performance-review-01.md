# Ocotillo Payments Group — Annual Performance Review

**Employee:** Tobias Ekwueme
**Title:** Senior Software Engineer, Merchant Platform
**Review Period:** July 1, 2025 – June 30, 2026
**Reviewer:** Sunita Kapadia, Director, Merchant Platform
**Date of Review:** August 9, 2026

---

## Summary of Role and Year

Tobias completed his fourth year at Ocotillo and his second on the Merchant Platform group. He entered the review period as the technical lead for the tokenization vault, our most sensitive and most heavily trafficked service, and he ended the period as the engineer whose work most directly shaped the platform's performance profile. This was the strongest year of Tobias's tenure and one of the strongest individual years I have reviewed in this organization.

## Goals and Results

**Goal 1: Complete the tokenization vault rewrite with authorization latency at or below 150 milliseconds at the 50th percentile, with zero data-loss incidents during migration.**

Result: Exceeded. The rewritten vault went fully live in October, six weeks ahead of the December peak window, which was the deadline that mattered even if it was not the one written on the goal. Median authorization latency came down from 340 milliseconds to 96 — a 72 percent reduction, and 36 percent better than the target. The migration of stored tokens for all 8,700 merchants completed with zero data-loss incidents and zero merchant-visible cutover events. I want to be specific about why the latency number matters commercially: authorization latency is the number our largest merchants quote back to us in quarterly reviews, and it is the number our sales team is now leading with in competitive deals. Tobias did not just hit an engineering target; he changed what the company can say about itself.

The manner of execution deserves as much comment as the outcome. Tobias wrote and circulated the migration design in July, ran two full dress rehearsals against a shadow environment, and built the dual-write reconciliation tooling that let us verify token parity continuously rather than at cutover. When a discrepancy surfaced in the second rehearsal — roughly 0.02 percent of tokens with stale key references — he paused the schedule for nine days over the objection of at least one stakeholder, root-caused it, and resumed. That decision looked expensive in September. It looked very cheap in December.

**Goal 2: Carry December peak volume without a Severity 1 or Severity 2 incident attributable to the vault.**

Result: Exceeded. The platform processed a peak of 4.1 million daily transactions in December — a company record and roughly 30 percent above the prior year's peak — with no incidents of any severity attributable to the vault, and no degradation of the latency numbers above. Tobias staffed the on-call rotation personally for the two highest-volume weeks, wrote the peak-readiness runbook that the rest of the group used, and ran the load tests that identified a connection-pool ceiling in an adjacent service before it became December's problem. That last item was outside his goal and outside his service boundary, and it is characteristic of how he worked all year.

**Goal 3: Raise the readiness of the vault team so that Tobias is not a single point of failure on the service.**

Result: Met. This was the goal I added specifically because the previous vault architecture lived largely in one person's head, and I did not want the rewrite to reproduce that condition. Tobias ran eleven recorded design walkthroughs, wrote operator documentation that two engineers have since used to handle vault pages without escalating to him, and delegated the key-rotation subsystem to a mid-level engineer whom he mentored through it. Two engineers on the team are now approved reviewers on the vault codebase. I rate this Met rather than Exceeded only because the hardest module — the HSM integration layer — still effectively requires Tobias for any nontrivial change, and I want that closed next year.

## Incidents

There were no incidents attributable to Tobias's services this period. He served as incident commander twice for incidents originating elsewhere on the platform, including the March 14 outage, where his post-incident review was thorough, blameless in tone, and produced four remediation items, all of which shipped.

## Feedback from Teammates and Merchants

Peer feedback was uniformly strong. Three engineers cited his design reviews as the most useful they receive; one wrote that "Tobias reviews the idea, not just the code." The mid-level engineer he mentored on key rotation named him as the primary reason her own year went well. The single developmental note, raised by two peers and one that I echo: in design debates Tobias is usually right, and he knows it, and on two occasions this year he closed a discussion faster than the room was ready to close it. At staff level, the job is not to win the argument efficiently; it is to leave behind people who could have won it without you. This is a refinement, not a deficiency.

Two enterprise merchants referenced the latency improvement unprompted in quarterly business reviews, and one cited it as a reason for renewing.

## Response to Self-Assessment

Tobias's self-assessment is accurate about his results and direct about his situation, and he deserves a direct answer. He writes:

> "In our January one-on-one you described me as the obvious staff candidate. I have structured this year around that expectation. I want to be transparent that I have taken two calls from external recruiters, not because I want to leave, but because I need to understand my market position if the promotion does not materialize."

I did say that in January, and I stand behind the assessment: Tobias is performing at staff level now. What I owe him, and did not adequately convey in January, is the distinction between my assessment and the company's process. This year the engineering organization funded exactly one staff-engineer promotion across all 42 engineers. I have submitted Tobias as my sole nomination, with this review and the vault results as the case. The decision is made at the VP level in September, and I will not promise an outcome I do not control. What I can promise is that his packet is the strongest I have written, that I have advocated for it in calibration explicitly, and that if the answer is no this cycle, I will tell him exactly why and exactly what the path looks like, in writing, within a week of the decision. His candor about the recruiter calls is professional and I have treated it as information, not leverage or threat. I would rather retain him with the truth than with vagueness.

## Overall Rating

**Exceeds Expectations.**

Under this year's calibration guidelines, at most two engineers in a group of nine may receive this rating. Tobias receives one of them, and it was not a close call.

## Compensation and Advancement

The merit pool for this cycle is 3.1 percent. Tobias will receive a **4.6 percent** merit increase, funded by differentiating within the pool, along with the maximum discretionary bonus multiplier available at his level. The staff promotion nomination is submitted and pending as described above; if approved, the promotional increase is separate from and additional to this merit adjustment.

## Goals for the Coming Year

1. **Close the HSM single-point-of-failure gap.** By end of Q2, at least two engineers other than Tobias can independently ship a nontrivial change to the HSM integration layer, evidenced by merged changes he did not author.
2. **Own platform-wide latency architecture.** Extend the vault's performance discipline to the two adjacent services in the authorization path, with a published latency budget for the full path and quarterly reporting against it. Target: end-to-end authorization under 200 milliseconds at p95.
3. **Peak 2026 readiness for 5.5 million daily transactions,** including the load-test program and runbooks, delivered by November 1.
4. **Staff-level influence, regardless of title:** lead one cross-team design review per quarter for work outside Merchant Platform, and demonstrate the facilitation refinement noted in peer feedback — measured by the same peers in next year's cycle.

---
---

# Ocotillo Payments Group — Annual Performance Review

**Employee:** Marisol Ybarra
**Title:** Senior Software Engineer, Merchant Platform
**Review Period:** July 1, 2025 – June 30, 2026
**Reviewer:** Sunita Kapadia, Director, Merchant Platform
**Date of Review:** August 9, 2026

---

## Summary of Role and Year

Marisol completed her sixth year at Ocotillo, all of it on or around the settlement service, of which she is the acknowledged expert and — this is the central tension of this review — the sole approved reviewer. Her year contains a genuinely excellent reliability result sitting next to a collaboration and throughput problem that had real merchant consequences. Both halves are true, both are documented below, and the rating reflects both.

## Goals and Results

**Goal 1: Hold settlement service unplanned downtime under 60 minutes for the year.**

Result: Exceeded. The settlement service recorded 22 minutes of unplanned downtime against a 60-minute budget — a 63 percent margin, and the best result the service has posted in the five years we have measured it. This is not luck. Marisol's proactive work is visible in the record: she identified and remediated the reconciliation-job memory leak in August before it caused an outage, she rebuilt the retry logic for acquirer timeouts in Q2, and during the May settlement backlog — an upstream problem not of her making — the service degraded gracefully exactly as her backpressure design intended, which is the only reason a bad day was not a catastrophic one. Settlement is where merchant money actually moves; 22 minutes on that service is a result the whole company benefits from, and I want the record to say so plainly.

**Goal 2: Maintain code-review turnaround at a median of one business day or better for settlement-service pull requests.**

Result: Not met, significantly. Median turnaround on settlement pull requests grew from six hours at the start of the period to 3.4 days by Q3, and it stayed there. Because Marisol is the only approved reviewer for the service, her queue is the service's queue: there is no alternate path, so every hour of her delay is an hour of everyone's delay. The consequences were concrete. The integration for the 400-store grocery chain — one of the largest merchant onboardings in company history — slipped five weeks, and when I reconstructed the timeline with the integration team, review latency on eleven settlement-side pull requests accounted for roughly three of those five weeks. The remaining slippage had other causes, and I am not assigning her the whole delay. I am assigning her the three weeks that the data supports.

I also want to name the structural cause honestly, because it is partly mine. The single-reviewer arrangement predates this year and I allowed it to persist because it was convenient and because Marisol's judgment on settlement code is genuinely the best we have. But an arrangement that concentrates all approval authority in one person guarantees exactly this failure mode the moment that person's load rises — and her load did rise, partly because of the reliability work I praised two paragraphs ago. The structure is my responsibility to fix. Her responsiveness within that structure, and her engagement with the fix, are hers.

**Goal 3: Onboard at least one additional approved reviewer for the settlement service by end of Q3.**

Result: Not met. This goal was set precisely to relieve the bottleneck above, and it did not happen. Two candidates began shadowing reviews in the fall; neither reached approved status. When we discussed it in the spring, Marisol's stated concern was that neither candidate yet had the context to catch the class of subtle correctness bugs that settlement code punishes severely. I do not dismiss that concern — settlement errors move real money in the wrong direction — but "no one else is ready" is a condition this goal existed to change, and after nine months the honest reading is that readiness was being held to a standard that guarantees the answer stays no. High standards for settlement correctness are right. A standard that only one person can ever meet is not a standard; it is a bottleneck with a rationale.

## Incidents

No Severity 1 or 2 incidents were attributed to the settlement service this year. During the May settlement backlog, Marisol's on-call performance was strong: she diagnosed the upstream cause within the hour and her communication to the incident channel was clear and steady. The service's graceful degradation during that event, noted above, is to her direct credit.

## Feedback from Teammates and Merchants

This is where the year's tension is sharpest. Two teammates raised the review-turnaround problem in skip-level meetings — meaning it reached me through the escalation channel rather than through resolution between peers, which itself says something about how approachable the problem felt. One described "planning my sprint around when Marisol might get to my PR." Both were explicit that the delays did not come with hostility or carelessness; the reviews, when they arrived, were rigorous and educational. The frustration was availability, not quality. Separately, two engineers named Marisol's incident write-ups as a model they imitate, and the integration team lead, despite the grocery-chain slippage, described her eventual reviews on that project as "the reason the integration will not break in production."

No merchant feedback named Marisol directly this year, but the grocery-chain merchant escalated the schedule slip to our VP of Sales, and that escalation is part of this record.

## Response to Self-Assessment

Marisol's self-assessment leads with the reliability result and addresses the review-latency issue briefly, writing:

> "Review turnaround suffered this year because the volume of settlement changes grew faster than my capacity, and because I do not believe we should lower the bar for who approves settlement code. I would rather a PR wait three days than a settlement bug reach production."

I understand the value system behind this, and it is the same value system that produced 22 minutes of downtime. But the framing presents a false choice. The alternative to a three-day queue is not lowered standards; it is a second and third reviewer trained to her standards, which was Goal 3, and which is fully within her power to produce. The grocery-chain merchant did not experience her rigor. They experienced a five-week delay. Sustaining the bar and scaling the bar are both part of a senior engineer's job, and this year she did the first and not the second.

## Overall Rating

**Meets Expectations.**

I want to be transparent about how I weighed this. The reliability result, taken alone, is exceeds-level work. The missed turnaround goal, the missed reviewer-onboarding goal, the skip-level escalations, and three weeks of merchant-visible delay, taken together, are below the bar for a senior engineer whose scope includes the health of the team around her service, not only the service itself. A senior engineer's expectations at Ocotillo explicitly include multiplying others' output. Weighed whole, this is a solid Meets, with a clearly identified path back to Exceeds that runs directly through Goal 1 below.

## Compensation and Advancement

Marisol will receive a **3.0 percent** merit increase, essentially at the 3.1 percent pool, reflecting a year that met expectations overall. Regarding advancement: Marisol has previously expressed interest in the staff track. I told her in our conversation, and record here, that the current pattern is the specific obstacle. Staff-level impact at Ocotillo is defined by leverage — making other engineers more capable — and the settlement service today is the clearest counterexample in my group: deep individual excellence with negative leverage on throughput. If the coming year's goals below are met, she will be a credible staff candidate in a future cycle. This year's single funded promotion went to another nomination, and I told her that directly rather than letting her infer it.

## Goals for the Coming Year

1. **Two additional approved settlement reviewers by December 31, three by June 30**, with "approved" defined by a written competency checklist that Marisol authors by September 30 — so the bar is explicit, high, and reachable. This is the year's top-priority goal and will be weighted accordingly.
2. **Restore median settlement PR turnaround to one business day by end of Q2** and hold it, measured monthly. The goal is a property of the review system, not of Marisol personally; the point of Goal 1 is to make Goal 2 achievable without heroics.
3. **Hold unplanned downtime under 60 minutes again** — the standard she set this year is now the standard, and I expect her to defend it while sharing the load.
4. **Zero collaboration issues surfacing via skip-level rather than directly.** Concretely: establish a published review SLA with the team, and a documented escalation path when her queue exceeds it, by end of Q1.

---
---

# Ocotillo Payments Group — Annual Performance Review

**Employee:** Fatoumata Diallo
**Title:** Software Engineer, Merchant Platform
**Review Period:** September 8, 2025 – June 30, 2026 (partial year, from date of hire)
**Reviewer:** Sunita Kapadia, Director, Merchant Platform
**Date of Review:** August 9, 2026

---

## Summary of Role and Year

Fatoumata joined Ocotillo in September from an embedded-systems background, which means this review covers roughly ten months in which she changed not only companies but domains — from firmware to distributed payments infrastructure, which differ in almost every operational instinct they reward. Against that backdrop, this was a strong first year: an ahead-of-schedule ramp, merchant-visible impact by May, and one significant incident-response mistake in March that she has handled about as well as a mistake can be handled. All three of those things are covered honestly below, including a direct answer to the question she asked in her self-assessment.

## Goals and Results

**Goal 1: Complete onboarding and ship a first production change within ten weeks of start date.**

Result: Exceeded. Fatoumata shipped her first production change in week seven — a fix to duplicate-webhook handling in the merchant notification service — three weeks ahead of the ramp target. More telling than the date was the character of the change: it included a regression test for the duplicate case and a small piece of documentation on webhook idempotency that two other engineers have since referenced. New engineers usually ship something small and leave quietly. She shipped something small and left the codebase better documented than she found it. That instinct has held all year.

**Goal 2: Reach independent on-call readiness for the merchant notification and webhook services by end of Q3, and serve in the rotation.**

Result: Met, with one significant exception discussed under Incidents. Fatoumata completed on-call certification on schedule in January and served five rotations through June. Four of the five were clean, including one overnight page in April that she resolved independently in under 40 minutes with a clear write-up. The fifth was March 14.

**Goal 3: Own at least one merchant-affecting improvement independently by end of the review period.**

Result: Exceeded. During the May settlement backlog, Fatoumata identified that a subset of merchants were receiving stale settlement-status webhooks — a downstream symptom nobody had yet connected to the backlog — built and shipped a fix the same day, and personally verified recovery for the affected merchants. Two merchants named her in support notes afterward; one wrote that she "stayed on the ticket until our finance team confirmed the numbers matched." For an engineer nine months into a new domain, finding the problem was impressive; the same-day fix, in code she had owned for only a few months, was more so. This is also worth situating: the May backlog was a hard day for the platform, and multiple senior engineers were consumed by the primary incident. Fatoumata found and closed a secondary merchant-facing problem largely on her own initiative.

## Incidents

**March 14 outage.** Fatoumata was on call when the notification service began failing at 2:12 a.m. Our incident policy requires escalation to a Severity 2 within 15 minutes if the on-call engineer has not identified a mitigation path. Fatoumata continued debugging alone and escalated at 3:07 a.m. — roughly 40 minutes past the threshold. The delayed escalation extended merchant-visible impact by an estimated 30 to 40 minutes.

Here is my full assessment of that event, because she has asked for it and because the record should be complete. First, the mistake was real, the policy is not ceremonial, and the extended impact was borne by merchants. That is on the record and it belongs there. Second, the mistake is a recognizable one for an engineer from embedded systems, where the professional instinct is that you own the problem until you solve it, and calling for help early is a failure mode rather than a discipline. Payments operations inverts that instinct, and nothing in her prior career would have taught her so. Third — and this is the part that determines how much the incident should weigh — her response afterward was exemplary. She escalated the moment she recognized the situation was beyond her, her communication from 3:07 onward was clear, she wrote her own blameless postmortem without being asked, she proposed the change to the on-call training that now includes an explicit "escalation is a skill, not a defeat" module, and her four subsequent rotations show the lesson was absorbed: her April overnight page included a proactive heads-up to the secondary on-call at minute ten, before she even needed help. That is what corrected looks like.

## Feedback from Teammates and Merchants

Peer feedback for a first-year engineer is unusually specific and warm. Her onboarding buddy described her as "the fastest ramp I've supported." Two engineers cited her questions in design reviews as the kind that "make you realize you hadn't finished thinking." One senior engineer noted the March incident but framed it exactly as I have: "one bad call, followed by the best postmortem a first-year has written here." The two merchant support notes from May are quoted above and are attached to this review in full. The single developmental theme in peer feedback: Fatoumata is sometimes slow to ask for help outside of incidents too — she will spend a day on a problem a teammate could unblock in ten minutes. This is the same instinct that produced March 14 in a milder form, and it is the growth edge for the coming year.

## Response to Self-Assessment

Fatoumata's self-assessment is candid throughout, and it ends with a direct question that deserves a direct answer. She writes:

> "I know the March 14 outage is part of my record, and I escalated 40 minutes later than I should have. My question is whether this incident will follow me — whether it will be attached to how I am evaluated going forward, or whether the record can show that I learned from it."

The answer is this: the incident is part of your record, because it happened, and this review documents it fully — including its consequences and including everything you did afterward. It will not follow you in the sense you fear. It is a data point, not a label. What follows engineers at Ocotillo is patterns, and your pattern since March 14 — the postmortem, the training module, the early escalation in April — is the pattern of someone who converted a mistake into a capability. If a future review references March 14, it should reference it the way this one does: as the origin story of an on-call habit that is now a strength. I will hold to that framing in calibration discussions, and I have already done so this cycle. What would change that answer is repetition, and there is no sign of repetition.

## Overall Rating

**Meets Expectations**, with an explicit note of strong trajectory.

I want Fatoumata to understand precisely what this rating does and does not say. Under this year's guidelines, at most two engineers in this group could receive Exceeds Expectations, and calibration weighs sustained scope over a full year. On a ten-month partial year that includes both an exceeded ramp goal and a genuine incident-response miss, Meets Expectations is the accurate rating — and it is a fully solid one, not a consolation. The trajectory note is the important part: her slope is the steepest in the group, and if the second year extends the line the first year drew, an Exceeds rating is realistically in reach.

## Compensation and Advancement

Fatoumata will receive a **3.4 percent** merit increase, modestly above the 3.1 percent pool, funded by differentiation within the group and reflecting the trajectory noted above. Regarding advancement: she is on a normal path toward senior engineer. The typical readiness window from her current level is two to three years; her ramp suggests the near end of that range is plausible. This year's constraints — the merit pool, the ratings distribution, and the single funded promotion, which applied to the staff level and not to her band — did not disadvantage her in any way she should worry about. The honest message is that nothing structural stands between her and senior engineer except accumulated evidence, and the coming year's goals are designed to accumulate it.

## Goals for the Coming Year

1. **Own a service.** Take primary ownership of the merchant notification service, including its roadmap, its reliability budget (target: under 90 minutes unplanned downtime), and its quarterly review with me. This is the scope evidence the senior-engineer case is built on.
2. **Make escalation and help-seeking a documented strength.** Concretely: no incident-policy deviations across all rotations, and — addressing the peer feedback — adopt a personal "one-hour rule" for non-incident blockers, asking for help after an hour of being stuck. I will check this in one-on-ones, not to police it, but because the habit compounds.
3. **Ship one cross-team project.** Lead the webhook-reliability workstream with the integrations team through to delivery by end of Q3, including the design review, so that engineers outside Merchant Platform can speak to her work next cycle.
4. **Teach the ramp.** Serve as onboarding buddy for at least one new engineer, and convert her own ramp notes into the standard onboarding path for engineers joining from non-payments backgrounds by December 31. She ramped faster than our program expects; the program should learn why.

---

**Reviews prepared by:** Sunita Kapadia, Director, Merchant Platform
**Calibration completed:** July 2026 cycle, Engineering Organization (42 engineers)
**Distribution:** Employee, HR file, VP of Engineering

**Acknowledgment of Receipt:** Signature blocks follow each employee's appendix section below. Signature indicates receipt and discussion of the review, not necessarily agreement with its contents. Employees may attach a written response within ten business days, which becomes part of the permanent review record.

---

# Appendices and Supporting Record

## Appendix A — Calibration Summary and Constraint Disclosure

Per this year's HR guidance, managers are required to disclose to employees, in writing, the structural constraints that shaped ratings and compensation decisions. For the Merchant Platform group (nine engineers), those constraints were:

1. **Merit pool:** 3.1 percent of aggregate group base salary. Differentiation above the pool for any individual required offsetting differentiation below it elsewhere in the group. The three reviews in this document account for 4.6, 3.0, and 3.4 percent respectively; the remaining six engineers' adjustments, documented in their own reviews, bring the group aggregate to 3.1 percent exactly.
2. **Ratings distribution:** A maximum of two Exceeds Expectations ratings in a group of nine. One of the two available Exceeds ratings was awarded within this set of three reviews (Ekwueme); the second was awarded elsewhere in the group. No minimum quota for Needs Improvement was imposed, and none was assigned in this group.
3. **Promotion funding:** One staff-engineer promotion funded across the 42-person engineering organization. Each director was permitted a single nomination. My nomination was Tobias Ekwueme. Decision expected from the VP of Engineering in September 2026. Promotions within the engineer-to-senior band (relevant to Diallo in a future cycle) are governed by a separate process and were not affected by this constraint.

I record these constraints here because two of the three employees in this document asked questions this cycle — about advancement and about how a partial-year rating was weighed — whose honest answers depend on them. Where a rating or a number was shaped by a constraint rather than purely by performance, these reviews say so in the body text. Where performance alone drove the outcome, no constraint is cited, and none applied.

## Appendix B — Metrics Referenced in These Reviews

| Metric | Baseline | Target | Result | Employee |
|---|---|---|---|---|
| Authorization latency, p50 | 340 ms | ≤150 ms | 96 ms | Ekwueme |
| Peak daily transactions carried without vault incident | 3.15M (prior yr) | Peak season | 4.1M | Ekwueme |
| Token migration data-loss incidents | — | 0 | 0 | Ekwueme |
| Approved vault reviewers other than lead | 0 | ≥2 | 2 | Ekwueme |
| Settlement unplanned downtime | 41 min (prior yr) | ≤60 min | 22 min | Ybarra |
| Settlement PR median turnaround | 6 hrs | ≤1 business day | 3.4 days | Ybarra |
| Additional approved settlement reviewers | 0 | ≥1 | 0 | Ybarra |
| Grocery-chain integration schedule variance | — | On time | +5 weeks (~3 attributable to review latency) | Ybarra |
| First production change (weeks from start) | — | ≤10 | 7 | Diallo |
| On-call rotations served / clean | — | Certified by Q3 | 5 / 4 | Diallo |
| March 14 escalation delay vs. 15-min policy | — | 0 | ~40 min | Diallo |
| Merchant support notes naming engineer | — | — | 2 | Diallo |

Source systems: incident ledger (PagerDuty export, FY26), repository analytics (July 2025 – June 2026), merchant support ticketing (Zendesk, May 2026 extract), integration program tracker. Raw extracts are retained in the review file and available to each employee on request for the metrics concerning them.

## Appendix C — Merchant Support Notes (Diallo), Reproduced with Merchant Identifiers Redacted

> **Note 1, May 19, 2026 (merchant redacted, mid-market retail):** "Wanted to flag that Fatoumata on your engineering side stayed on the ticket until our finance team confirmed the numbers matched. We've had settlement discrepancies with other processors that took weeks. This took an afternoon."

> **Note 2, May 20, 2026 (merchant redacted, food service):** "Please pass along thanks to Fatoumata D. — she explained what happened with the stale webhooks in plain language and confirmed the fix herself. That's the first time an engineer, not an account manager, closed the loop with us directly."

Both notes were logged by Merchant Support without solicitation and forwarded to me by the support lead. They are included in full because the review body paraphrases them and the employee is entitled to the source text.

## Appendix D — Follow-Up Commitments by Reviewer

These are my commitments, with dates, so that the employees in this document can hold me to them:

1. **Ekwueme:** Communicate the staff promotion decision, with written rationale either way, within five business days of the VP decision in September. If the answer is no, deliver a written path-to-staff plan for the next cycle within ten business days of that communication.
2. **Ybarra:** Approve or return the settlement-reviewer competency checklist within five business days of her September 30 draft, so that the year's top-priority goal is not delayed by my own review latency. Additionally, I will remove one recurring obligation from her plate — the monthly acquirer-liaison call, which I am reassigning effective September 1 — because the reviewer-onboarding goal requires hours that must come from somewhere, and it is my job to find them.
3. **Diallo:** Confirm in the January mid-cycle check-in, in writing, whether the trajectory noted in her rating is holding, so that "strong trajectory" is a tracked claim rather than a pleasantry. Sponsor her attendance at one external payments-infrastructure conference this fiscal year as part of the domain-transition investment.
4. **All three:** Mid-cycle written check-ins against the coming year's goals no later than January 31, 2027, so that nothing in next year's reviews is a surprise.

## Appendix E — Signature and Response Blocks

**Tobias Ekwueme**
Employee signature: ______________________ Date: __________
Reviewer signature: ______________________ Date: __________
Employee written response attached: ☐ Yes ☐ No

**Marisol Ybarra**
Employee signature: ______________________ Date: __________
Reviewer signature: ______________________ Date: __________
Employee written response attached: ☐ Yes ☐ No

**Fatoumata Diallo**
Employee signature: ______________________ Date: __________
Reviewer signature: ______________________ Date: __________
Employee written response attached: ☐ Yes ☐ No

---

*End of annual review packet, Merchant Platform group (partial — three of nine reviews), fiscal year ending June 30, 2026. Remaining six reviews filed separately under the same cycle. Retention per company policy: seven years from date of signature.*
