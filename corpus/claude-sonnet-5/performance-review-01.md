# Tobias Ekwueme — Annual Performance Review

**Title:** Senior Engineer, Merchant Platform
**Review Period:** July 1, 2025 – June 30, 2026
**Reviewer:** Sunita Kapadia, Director, Merchant Platform

## Goals and Results

Tobias's primary commitment for the cycle was the tokenization vault rewrite: reduce authorization latency without weakening the isolation guarantees that keep card data out of the merchant-facing path, and do it before the December peak. He delivered against both halves of that goal. Median authorization latency fell from 340 milliseconds to 96, a reduction large enough that two of our top-twenty merchants asked their own engineering leads what had changed on our side, unprompted. The vault carried the December peak of 4.1 million transactions in a single day with no incident, no rollback, and no on-call escalation attributable to the new code path. That is the outcome the goal asked for, delivered on schedule, under real load, with no asterisks.

The work also had a shape to it that matters beyond the metric: he broke the rewrite into six independently reversible migrations rather than one cutover, which is why we were able to run December with confidence instead of hope. Two of the six migrations were paused mid-flight when a downstream reconciliation job flagged unexpected latency variance; he found the cause, fixed it, and resumed within a day rather than pushing through on a deadline. That is the judgment we ask senior engineers to exercise and don't always get.

## Self-Assessment and Manager Response

> **Self-assessment:** "You called me the obvious staff candidate in January, and I've taken this project as far as I know how to take it. I've also taken two recruiter calls since then."

I want to answer this directly rather than around it. In January, watching the early vault design reviews, I said something close to that, and I meant it as encouragement grounded in what I was seeing at the time, not as a commitment on behalf of the promotion committee. I understand why you heard it as more than that, and I should have been clearer in the moment about the distance between my opinion and a funded outcome. I'm not walking back the opinion — the work this year supports it — but I want the record to show what I actually control and what I don't, because that gap is exactly what's put you in front of recruiters.

On that: I'd rather you call me before you take a third one. Not to talk you out of exploring your market value, which is reasonable at four years in seat with this year's results, but because if there's a counter-conversation to have about scope, title, or comp, I want to have it before you're deciding between two offers instead of deciding whether to stay.

## Incidents and Feedback

No production incidents were attributed to Tobias's systems this cycle. The vault migration paused twice, both times on his own initiative and both times before any customer-visible effect. Feedback gathered in calibration from peers on the platform team described his design review documents as the clearest the group has produced this year, and two more junior engineers specifically credited him with unblocking their own work during the migration. On the merchant side, the latency improvement showed up indirectly rather than in support notes — the signal was an absence of timeout-related complaints during December rather than praise, which for a payments platform is the correct kind of quiet.

## Rating: Exceeds Expectations

This is one of two Exceeds Expectations ratings available across the nine-person group this cycle, and it's the clearer of the two calls I had to make. The scope of the vault rewrite, the load it was proven under, and the absence of any incident cost make this an easy allocation of the constrained rating.

## Compensation and Advancement

The group's merit pool this year averages 3.1 percent; individual increases are differentiated around that average by rating. Your increase is 4.5 percent, reflecting the Exceeds rating and the size of the latency and reliability gains. That's toward the top of what the pool structurally allows for a single senior engineer this cycle.

On staff: there is one funded staff-engineer promotion for the entire 42-person engineering organization this year, not one per group. I am nominating you, and I think the case is strong — the vault work is exactly the kind of cross-cutting, high-leverage technical leadership the staff level is meant to recognize. But I want to be honest about the odds rather than let the January comment stand uncorrected twice: you will be one of several strong nominees from other groups, the committee decides on the whole slate, and I do not control the outcome. I expect a decision by the end of Q3, September 30. If it doesn't come through this cycle, I want to talk immediately about what closes the gap next time, and about what I can do in the meantime — including a market-adjustment conversation with compensation — to make sure the answer to the recruiter calls is a good one.

## Goals for the Coming Year

- Extend the vault architecture to the second processor integration, with the same reversible-migration discipline used this cycle.
- Take on structured mentorship of at least one mid-level engineer, with the design-review practice you've already been running informally made explicit and repeatable.
- Write up the vault rewrite as a staff-level case study — architecture, tradeoffs, and the load results — for use in the promotion packet regardless of this cycle's outcome.
- Reduce single-owner risk on the vault itself: document enough of the internals that a second engineer could safely operate it if you were out or moved to new scope.

---

# Marisol Ybarra — Annual Performance Review

**Title:** Senior Engineer, Merchant Platform (Settlement Service)
**Review Period:** July 1, 2025 – June 30, 2026
**Reviewer:** Sunita Kapadia, Director, Merchant Platform

## Goals and Results

Marisol's stated reliability goal was to hold unplanned downtime on the settlement service under 60 minutes for the year. She finished at 22 minutes, a result well ahead of target and, on that axis alone, one of the stronger numbers on the team. No settlement failures reached merchants during the period, and the service's core availability record this year is genuinely good work.

That result sits alongside a second pattern I have to weigh with equal seriousness. Marisol is the only approved reviewer for the settlement service, a status that predates this cycle but that she has not moved to change during it. Median pull-request turnaround on that codebase grew from six hours to 3.4 days over the year. Two teammates raised the growing backlog independently in skip-level conversations with me, not as a complaint about her work but as a description of a bottleneck they didn't feel they could raise with her directly. The concrete cost showed up in April and May: a settlement integration for a 400-store grocery chain slipped five weeks waiting on review capacity that only she could provide. That slip was visible to the client and required an apology call from our account team.

Her self-assessment for the cycle centers on the downtime number and does not address the review backlog or the integration delay. I'm noting that gap plainly rather than filling it in on her behalf, because I think the omission is itself something worth naming: the metric she chose to lead with is real, but it isn't the full picture of the year, and I'd rather the review say so than let the strongest number stand in for the whole.

## Incidents and Feedback

There was no service-reliability incident attributable to Marisol this year; the downtime record supports that directly. The operational cost this cycle came from throughput, not from failure. The grocery-chain slip is best described as a process incident: no data was at risk and no transaction was mishandled, but a client-facing commitment was missed because approval capacity was concentrated in one person who was, for that stretch, unavailable to keep pace with the queue. The two teammates who raised the backlog in skip-levels did so carefully and specifically credited Marisol's technical judgment on the reviews she does complete; their concern was capacity and access, not quality.

## Rating: Meets Expectations

I want to be direct about how I got here, because the reliability number alone would argue for more. Two Exceeds Expectations ratings are available across the group this cycle; I am not withholding one from you to spend it elsewhere as a matter of arithmetic. Even judged on its own terms, this year combines a strong individual outcome with a structural risk you control and did not address — a single point of failure on a system the business depends on, a measurable slowdown in how you served your own teammates' work, and a client-facing delay that resulted from both. That combination is a Meets Expectations year, not an Exceeds one, regardless of how the pool is allocated.

## Compensation and Advancement

Your increase under this year's 3.1 percent average pool is 2.8 percent, consistent with the Meets rating. I know that sits below what the downtime result alone might suggest, and I want the reasoning on the record rather than left implicit: the increase reflects the full year, including the backlog and the slip, not a discount applied on top of a fair rating.

This is not a promotion cycle for you, and I don't think it should be until the settlement service has a second approved reviewer and the PR turnaround trend has reversed. I'd like to revisit that conversation at mid-year if the goals below are on track — this isn't a closed door, it's a sequencing question.

## Goals for the Coming Year

- Train and get formal review approval for at least one additional engineer on the settlement service by end of Q3, so you are no longer the sole gate.
- Bring median PR turnaround back under 24–48 hours within two quarters, tracked monthly.
- Personally own the relationship repair on the grocery-chain account alongside the account team, including a written retrospective on what the review-capacity gap cost and how the new approver structure prevents a repeat.
- Continue the reliability practice that produced this year's downtime number — that part of the job is working and shouldn't be disrupted by the changes above.

---

# Fatoumata Diallo — Annual Performance Review

**Title:** Software Engineer, Merchant Platform
**Review Period:** September 8, 2025 – June 30, 2026 (first review)
**Reviewer:** Sunita Kapadia, Director, Merchant Platform

## Goals and Results

Fatoumata joined the team in September from an embedded-systems background, a deliberate hire against a ten-week ramp target intended to account for the domain shift into card processing and distributed services. She shipped her first production change in week seven, three weeks ahead of that target, and the change itself — a fix to settlement batching that had been sitting in the backlog since before she started — held up without follow-on defects. For a first year that started with an unfamiliar domain, that ramp is one of the faster ones I've overseen in this group.

The rest of the year built on that start reasonably steadily. She took ownership of increasingly independent pieces of settlement and reporting work through the winter and spring, and by the May settlement backlog she was trusted with same-day production fixes without a second engineer shadowing her — a level of autonomy that typically takes new hires longer than eight months to reach, particularly coming from a different engineering discipline.

## Incidents and Feedback

On March 14, a settlement service outage occurred and Fatoumata, on call, escalated 40 minutes after the threshold our runbook calls for. The delay extended customer impact beyond what it should have been, and it is a fair, factual part of this record. The cause was gap in on-call pattern-matching that comes with being five months into a first on-call rotation in an unfamiliar system, not a lapse in effort or judgment — she was actively working the problem the entire time, just without yet recognizing it as escalation-worthy as quickly as a more tenured on-call engineer would have.

Two months later, during the May settlement backlog, she was named directly by two merchants in support notes after delivering a same-day fix that cleared their stuck settlements before end of business. That's the kind of specific, named merchant feedback that doesn't happen often in a first year, and it happened during a stretch when the team was under real pressure.

> **Self-assessment:** "Will the March 14 outage follow me?"

No — not as a mark against you, and I want to say plainly why. One incident in a first on-call rotation, caught and worked correctly once escalated, sitting alongside a ramp that beat its target by three weeks and two merchants naming you by name for fixing their problem two months later, is a normal first year, not a flagged one. What I do want it to leave you with is a specific, addressable gap — escalation timing under uncertainty — rather than a general cloud over the year. That's a skill, not a character trait, and it's the kind of thing that gets fixed by rotations and runbooks, which is exactly what's in your goals below.

## Rating: Meets Expectations

For a first review at ten months, Meets Expectations is the rating and also a genuinely positive one: it reflects a fast ramp, growing scope, direct merchant recognition, and one incident handled imperfectly but not badly, against a target built for someone new to the domain. New hires in their first cycle aren't part of this year's Exceeds Expectations allocation regardless of results — that's a calibration norm across the org, not a judgment specific to your work — so this rating should be read on its own terms rather than against Tobias's or Marisol's.

## Compensation and Advancement

Your increase this cycle is 3.0 percent, at the group's average under the 3.1 percent pool, reflecting a strong first-year trajectory. Advancement conversations — senior track, expanded scope — aren't realistic to start yet at ten months in seat, and I'd rather set that expectation now than let it sit unaddressed. The faster ramp does mean I'd expect that conversation to open earlier for you than it typically would, plausibly at the eighteen-month mark rather than the more standard two years, if the trend holds.

## Goals for the Coming Year

- Complete formal on-call escalation training and shadow at least one senior engineer's rotation before taking further solo on-call weeks, closing the specific gap from March.
- Take ownership of one settlement-adjacent feature area end to end, from design through production support.
- Begin cross-training as a backup reviewer on the settlement service — the team has a documented capacity gap there this year, and your ramp trajectory suggests you could reasonably take part of that on within two quarters with support.
- Build on the May recognition by taking a visible role in the next merchant-facing incident response, with a debrief afterward specifically on escalation timing.

## Acknowledgment

This review has been discussed in a one-on-one meeting between the employee and the reviewer. Signature below indicates the review has been read and discussed; it does not necessarily indicate agreement with every rating or characterization contained in it. Employees who wish to append a written response have thirty days to do so through HR.

**Employee:** Fatoumata Diallo — _______________________ Date: _______

**Reviewer:** Sunita Kapadia, Director, Merchant Platform — _______________________ Date: _______

**Next scheduled review:** Mid-year check-in, December 2026, focused on escalation training completion and progress toward backup-reviewer readiness on the settlement service. Full annual review to follow at the standard cycle, June 30, 2027.

## Calibration Summary — Merchant Platform Group

**Prepared by:** Sunita Kapadia, Director, Merchant Platform
**Submitted to:** Compensation and Promotion Committee
**Cycle:** FY2026 Annual Review

The following summarizes the ratings, pool usage, and advancement recommendations for the three engineers reviewed above, for reconciliation against the group-wide allocation.

**Ratings issued this batch:**

| Employee | Rating | Merit Increase | Pool Contribution |
|---|---|---|---|
| Tobias Ekwueme | Exceeds Expectations | 4.5% | Uses 1 of 2 group Exceeds allocations |
| Marisol Ybarra | Meets Expectations | 2.8% | — |
| Fatoumata Diallo | Meets Expectations | 3.0% | New hire, excluded from Exceeds pool by policy |

Average increase across this batch of three is 3.43 percent against the group's 3.1 percent target. This is expected to reconcile within range once the remaining six engineers in the group are finalized; two of the remaining six are tracking toward below-average increases on Meets ratings, which should bring the full nine-person average to target. Full group reconciliation will be submitted separately by August 7.

The group's second Exceeds Expectations allocation is held for an engineer outside this batch and will be documented in that engineer's individual review; it is not being reserved or withheld from anyone reviewed here.

**Promotion nomination:** Tobias Ekwueme is being submitted as this group's nominee for the single funded staff-engineer promotion available across the 42-person engineering organization. Supporting material — the tokenization vault design history, December peak-load results, and cross-team impact notes — will be included in the packet submitted to the committee ahead of the September 30 decision date. No other engineer in this group is being put forward for staff-level promotion this cycle.

**Flagged operational risk for follow-up outside the review cycle:** the settlement service currently has a single approved reviewer (Marisol Ybarra). This is noted here separately from her individual rating because it represents a team-level continuity risk that compensation and promotion decisions alone will not resolve. I am tracking remediation through the goals set in her review above and will report progress at the Q3 skip-level.

## Distribution and Filing

This packet — the three individual reviews, employee acknowledgments, and this calibration summary — is filed with HR under the Merchant Platform group's FY2026 annual cycle. Copies are routed as follows: employee copies to each individual via the HR portal upon signature; manager copy retained by Sunita Kapadia; committee copy to Compensation and the Promotion Committee for the September 30 staff-track decision; one redacted copy (ratings and increases removed) to the VP of Engineering for organization-wide calibration tracking.

## Appendix: Supporting Documentation Referenced

The following materials were reviewed in preparing these three assessments and are available on request to HR or the Promotion Committee:

- Tokenization vault design review documents and migration logs, July 2025–December 2025
- December peak-volume incident dashboard (zero Sev-1/Sev-2 events attributed to vault systems)
- Tobias Ekwueme self-assessment, submitted June 2026
- Settlement service reliability dashboard, FY2026 (22 minutes cumulative unplanned downtime)
- Pull-request turnaround metrics, settlement service, monthly trend July 2025–June 2026
- Skip-level meeting notes referencing settlement review backlog (two entries, redacted for source)
- Grocery-chain integration timeline and client correspondence, March–May 2026
- March 14 outage postmortem, including escalation timestamp log
- May settlement backlog support-ticket notes citing Fatoumata Diallo by name (two merchants)
- Fatoumata Diallo self-assessment, submitted June 2026
- New-hire ramp tracking record, Fatoumata Diallo, September–November 2025

**End of FY2026 Merchant Platform annual review packet.**

## HR Intake Confirmation

**Received by:** People Operations, Total Rewards
**Date received:** June 30, 2026
**Submitting manager:** Sunita Kapadia, Director, Merchant Platform
**Packet:** FY2026 Annual Review — Merchant Platform Group (partial batch, 3 of 9 reports)

Intake checklist confirmed complete for this batch:

- [x] Individual reviews present for all three employees named in submission
- [x] Ratings recorded and within group allocation limits (1 of 2 Exceeds used)
- [x] Merit increase percentages specified per employee
- [x] Promotion nomination form attached for Tobias Ekwueme (staff-track, org-wide slot)
- [x] Self-assessment references cross-checked against employee-submitted files on record
- [x] Employee acknowledgment fields present (pending signature — see below)
- [x] Calibration summary included with group-level pool reconciliation note

**Outstanding items before processing closes:**

1. Employee signatures on all three acknowledgment pages. Unsigned as of intake; standard 10-business-day window applies before HR proceeds without signature under passive-acknowledgment policy.
2. Remaining six reviews for the Merchant Platform group, due August 7 per manager's note in the calibration summary, required before the group's full pool reconciliation can be closed out.
3. Promotion packet supporting materials (vault design history, peak-load results, cross-team impact notes) referenced but not yet attached in this submission — required before September 30 committee review.

**Processing status:** Held — pending items 1–3 above. Merit increases for Tobias Ekwueme, Marisol Ybarra, and Fatoumata Diallo will be queued for the August payroll cycle contingent on signature receipt; no increase will be released against an unsigned acknowledgment past the 10-day window without an HR exception filed by the manager.

**HR contact for follow-up:** People Operations, Total Rewards — case number assigned upon promotion-packet attachment.
