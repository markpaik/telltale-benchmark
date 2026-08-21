# Reviewer Count, Review Latency, and Defect Detection in Peer Code Review: A Structured Literature Review

**Prepared by:** Dr. Wen-Li Tsai, Staff Research Engineer, Ironwood Labs
**Commissioned by:** Oluwaseun Bamgbose, Vice President of Engineering
**Date:** August 9, 2026
**Internal telemetry supplied by:** Ingrid Vasquez-Thorne, Developer Experience Lead

---

## 1. Introduction

### 1.1 Background and motivating question

Since 2019, Ironwood Labs has required two approving reviewers on every change merged to production. A platform group proposal would relax this policy to a single approving reviewer for changes under 200 changed lines, on the grounds that review latency — a median of 41 hours per change in our telemetry — is the single largest component of lead time from commit to deployment. The proposal arrives in tension with recent experience: a severity-one outage on March 14, 2026, costing approximately $900,000 in service credits, was traced to a two-line configuration change that received two approvals in under four minutes. The outage is a caution against inferring that our current process reliably catches small, high-consequence defects; it is equally a caution against assuming that a second reviewer, as currently practiced, provides the protection the policy intends.

This review was commissioned to establish what the published evidence supports. The guiding question is:

> **For small code changes, what is the marginal defect-detection benefit of a second reviewer, and how does that benefit trade against the latency cost of requiring one?**

Three subsidiary questions structure the synthesis: (a) what defect-detection rates does peer review achieve, and under what conditions; (b) what does the evidence say about the relationship between reviewer count and detection; and (c) what is known about review latency, change size, and their interaction with review effectiveness.

### 1.2 Scope

The review covers peer review of source code and closely related artifacts in software development, from the formal inspection literature beginning with Fagan (1976) through contemporary studies of tool-mediated, asynchronous "modern code review" (Bacchelli & Bird, 2013) up to 2026. Pair programming is included as a limiting case — continuous review by exactly one reviewer with zero latency — because it bounds one end of the design space Ironwood is considering. Excluded are studies of requirements or design inspection where no code-review results are reported, studies of automated static analysis without a human reviewer, and studies of reviewer *recommendation* algorithms except where they bear on reviewer count or expertise effects.

The review is written for a decision audience. Studies are compared against one another on shared outcomes rather than summarized serially, and the closing section states explicitly what the evidence does and does not support for a company weighing the proposed change.

---

## 2. Search and Selection

Two computing digital libraries (the ACM Digital Library and IEEE Xplore), Scopus, and the proceedings of eight venues (ICSE, FSE/ESEC, ASE, MSR, ICSME, ESEM, EMSE, and TSE, treating the journals' online archives as proceedings-equivalent) were searched for the period 1976–2026. Search strings combined ("code review" OR "code inspection" OR "software inspection" OR "peer review" OR "pull request" OR "pair programming") with ("defect" OR "fault" OR "quality" OR "effectiveness" OR "latency" OR "reviewer"). Backward and forward snowballing was applied to three anchor works: Fagan (1976), Bacchelli & Bird (2013), and Hannay et al. (2009).

The search returned 1,540 unique records after deduplication. Title-and-abstract screening excluded 1,291 for being out of scope (predominantly reviewer-recommendation, sentiment, and tooling papers with no effectiveness or latency outcomes). Of 249 papers read in full, 84 were included: 22 controlled experiments, 31 repository mining studies, 13 industrial case studies, nine pair-programming studies, and nine surveys, systematic reviews, or meta-analyses used for context. For each included study, defect detection rates, change or artifact sizes, reviewer counts, latency measures where reported, population (student vs. professional), and study design were recorded in the extraction sheet maintained alongside this document; citations below are by author and year and correspond to rows in that sheet.

Two limitations of the search should be noted. Grey literature (engineering blog posts, internal white papers from other companies) was excluded, which biases the corpus toward organizations that publish — historically IBM, AT&T, Microsoft, and Google. And publication bias almost certainly inflates the apparent effectiveness of inspection in the 1976–1995 literature, a point taken up in Section 3.1.

---

## 3. Synthesis

### 3.1 Defect detection: the inspection era and why its numbers do not transfer

The strongest headline numbers in the corpus come from formal inspection. Fagan (1976) reported that design and code inspections at IBM found 82% of defects detected during development of one product, and Fagan (1986) later claimed inspection processes finding 60–90% of defects across projects. Ackerman, Buchwald, and Lewski (1989) reported comparable effectiveness at AT&T, and Weller (1993), analyzing three years of inspection data at Bull HN, found inspections substantially more efficient per hour than testing at removing defects. Kemerer and Paulk (2009), using data from the Personal Software Process, found that disciplined review at controlled rates (under roughly 200 LOC/hour) significantly reduced defect density in delivered code.

Taken at face value, these results would settle the question in favor of maximal review. They should not be taken at face value, for three reasons that emerge when the studies are set against later work.

First, the *baseline* differs. Inspection-era detection percentages are computed against total defects found across the lifecycle, in environments with long release cycles, no continuous integration, and comparatively weak automated testing. Modern review operates downstream of compilers, linters, type systems, and CI test suites that remove entire defect classes before a human ever looks. Mäntylä and Lassenius (2009), classifying defects found in code reviews across student and industrial settings, found that roughly 75% of review findings concerned evolvability — readability, structure, documentation — rather than functional defects. Beller et al. (2014) replicated this in open-source projects: the ratio of maintainability to functional fixes triggered by review was about 3:1. Czerwonka, Greiler, and Tilford (2015), drawing on large-scale Microsoft data, stated the point bluntly in their title — reviews as currently practiced only rarely find functional bugs, and the median useful comment concerns long-term maintainability. The inspection era measured a process aimed squarely at defect removal; modern review largely does something else, and importing 60–90% detection expectations into a modern lightweight process is a category error.

Second, the *defect definition* differs. Fagan-tradition studies counted defects against exit criteria negotiated per inspection; repository studies count post-release fixes linked to changed files (McIntosh et al., 2014; Bavota & Russo, 2015); experiments count seeded faults (Porter, Votta, & Basili, 1995; Biffl & Halling, 2003). These are not commensurable quantities, and cross-study comparison of raw detection percentages is unreliable. This review therefore compares *directions* and *marginal effects*, not point estimates.

Third, the *process* differs. Formal inspection mandated preparation time, checklists, controlled reading rates, and a moderated meeting. Votta (1993) showed at AT&T that the meeting itself contributed little — most defects were found in individual preparation — a result Porter and colleagues extended experimentally (Porter et al., 1997), finding that meetings added cost and schedule delay without proportional detection gains. This line of work is the intellectual origin of modern asynchronous review: Rigby, German, and Storey (2008) documented that Apache's email-based review achieved useful defect discussion with none of Fagan's apparatus, and Rigby and Bird (2013), examining projects at AMD, Microsoft, and in open source, found convergent practice everywhere — small changes, few reviewers, fast iteration — that looks nothing like formal inspection. The convergence is itself evidence: independent organizations under real cost pressure abandoned the heavyweight process and settled on remarkably similar lightweight parameters.

The implication for Ironwood is that the inspection literature establishes that *careful human reading of code finds defects* — a claim no later study contradicts — but provides no reliable estimate of what a second modern reviewer contributes, because its detection rates were achieved by a different process against a different baseline.

### 3.2 Reviewer count: what the second reviewer adds

The central policy question — one reviewer or two — is addressed by three largely independent bodies of evidence, and they point in a consistent direction with important qualifications.

**Experimental evidence on team size.** Porter et al. (1997), in a controlled experiment embedded in a live Lucent development project, varied inspection team size (one, two, and four reviewers) and found that team size had no significant effect on detection effectiveness, while larger teams increased interval (schedule delay). Sauer et al. (2000), synthesizing behavioral research on group performance, argued theoretically that inspection effectiveness is driven almost entirely by the *individual expertise* of participants, not by group size or process, and predicted diminishing returns beyond the best-qualified reviewer. Biffl and Halling (2003), using nominal (non-interacting) teams of students, found that detection did increase with team size but with sharply diminishing marginal returns and rapidly worsening cost-effectiveness: the second inspector adds less than the first, the third less than the second, and much of what each additional reviewer finds duplicates what earlier reviewers found. The disagreement between Porter et al. (no effect) and Biffl and Halling (diminishing positive effect) is best explained by population and defect type: Biffl and Halling used students inspecting seeded defects, where overlap between reviewers is lower because no individual reviewer is expert; Porter et al. used professionals on real code, where a competent first reviewer captures most of what a second would.

**Repository mining evidence.** The mining literature consistently finds that *review participation* predicts quality, and just as consistently fails to find that a *second approver* adds much. McIntosh et al. (2014, extended 2016) found in Qt, VTK, and ITK that low review coverage and low review participation were associated with more post-release defects — components merged with little or no review discussion were riskier. Bavota and Russo (2015) found reviewed commits induced significantly fewer bug fixes and had better readability than unreviewed commits. Thongtanunam et al. (2017) refined this: it is not the count of approvals but the *presence of substantive review activity* — comments, revisions, back-and-forth — that distinguishes defective from clean files; defective files were reviewed with less discussion and faster approval. Kononenko et al. (2015), studying Mozilla, found that review quality (measured by whether reviewed code later needed fixing) was associated with reviewer experience and reviewer workload, not with the number of reviewers involved. Rigby et al. (2014), building statistical models across open-source projects, found the number of reviewers per change converged near two but that detection-relevant discussion was dominated by one or two engaged participants regardless of how many were formally involved. Against these stands the widely cited result of Rigby and Bird (2013) that two reviewers is the convergent norm — but their finding is descriptive (organizations settle on two) rather than causal (two catches more than one), and they explicitly caution against reading it as an effectiveness result.

**Industrial case evidence.** Sadowski et al. (2018) is the most consequential single data point for Ironwood's decision. Google requires only *one* approving reviewer for most changes (with ownership and readability requirements layered separately), reviews a median change of about 24 lines, achieves median review latency under four hours for small changes, and reports no evidence of a quality penalty attributable to single-reviewer approval at a scale of tens of thousands of engineers. Czerwonka et al. (2015) at Microsoft reached a compatible conclusion from the opposite direction: given that most review comments do not concern functional defects, mandatory multi-reviewer policies impose latency costs disproportionate to their defect-detection yield, and review effort should be *targeted* — by change risk, component history, and author experience — rather than applied uniformly. Bosu, Greiler, and Bird (2015), also at Microsoft, found that comment usefulness rises steeply with reviewer familiarity with the changed code and declines with the number of files in the change — evidence that *who* reviews and *what size* the change is matter more than *how many* review.

**Synthesis.** Read together, the three strands support a specific, bounded claim: the marginal defect-detection contribution of a mandatory second approver is small *when the first reviewer is engaged and qualified*, and the literature's quality effects flow through participation and expertise, not headcount. The qualification is not decorative. Every mechanism by which review improves quality in these studies — substantive comments (Thongtanunam et al., 2017), reviewer familiarity (Bosu et al., 2015; Kononenko et al., 2015), adequate reading time (Kemerer & Paulk, 2009) — is a mechanism that a rubber-stamped approval bypasses, whether there is one such approval or two. Ironwood's March 14 outage, in which two reviewers approved a change in under four minutes, is a textbook instance of the failure mode Thongtanunam et al. (2017) identified: defective changes are characterized by fast, low-discussion approval. The second reviewer did not fail because second reviewers are useless; both reviewers failed for the same reason, and the policy question is whether requiring two approvals *causes* engagement or merely diffuses responsibility. Sauer et al. (2000) predicted, and Baysal et al. (2016) and MacLeod et al. (2018) observed, social-loafing dynamics consistent with the latter: when approval is shared, individual accountability per reviewer drops.

### 3.3 Change size and latency: the cost side of the ledger

The proposal's premise — that latency is the dominant cost of the current policy and that small changes are where relaxation is safest — has direct support in the literature, with one important complication.

**Small changes are reviewed better.** The most robust size-related finding in the corpus is that review effectiveness degrades as change size grows. Bosu et al. (2015) found comment density and usefulness fall as the number of files rises. Baum, Schneider, and Bacchelli (2019), in controlled experiments, found defect detection during review declines with change size and reviewer fatigue, with detection dropping measurably as reviews lengthen. Kemerer and Paulk (2009) showed detection collapses when reading rates exceed roughly 200 LOC/hour — a rate a large change practically forces. Weißgerber, Neu, and Diehl (2008) found small patches are accepted faster and more often in open source; Rigby and Bird (2013) found the convergent norm across organizations is changes small enough to review in under an hour. This body of work supports drawing a size threshold as such — small changes are the regime where a single engaged reviewer performs best. It does *not* support the inverse inference that small changes are low-risk: Ironwood's outage was a two-line change, and Bosu et al. (2015) and Beller et al. (2014) both note that configuration and infrastructure changes carry defect consequences disproportionate to their size. Line count measures review *tractability*, not blast radius.

**Latency is real and consequential.** Jiang, Adams, and German (2013), studying the Linux kernel, found reviewing time driven by submission timing, maintainer load, and patch maturity, with latencies ranging from hours to weeks. Baysal et al. (2016) found non-technical factors — organizational affiliation, author reputation, reviewer load — significantly affect both latency and acceptance, meaning latency is not purely a function of diligence and cannot be assumed to be "time spent reading." MacLeod et al. (2018), surveying Microsoft engineers, identified review turnaround as a top-three pain point, with authors blocked on context switches while awaiting review. Herbsleb and Mockus (2003) showed that work items requiring coordination across sites take approximately 2.5 times longer than comparable colocated work — directly relevant to any team whose two required reviewers sit in different time zones, since a two-approval policy across time zones can serialize two multi-hour waits into a multi-day cycle. Ironwood's 41-hour median is consistent with this arithmetic. Sadowski et al. (2018) demonstrated that low latency and review effectiveness are jointly achievable — Google's sub-four-hour median coexists with its quality outcomes — but achieved this through small changes, single approval, strong ownership rules, and cultural expectations of prompt turnaround, i.e., a *system* of which single approval is one component.

**The latency–quality trade is not linear.** Czerwonka et al. (2015) argued, and the mining studies indirectly confirm, that latency cost compounds (context switching, rebasing, batching of changes to amortize review overhead — which then makes changes larger and review worse, per Section 3.3's first finding), while marginal detection from added reviewers plateaus quickly (Section 3.2). A policy that trades a plateauing benefit against a compounding cost is inefficient at the margin; the literature supports rebalancing, though it cannot supply Ironwood's exact break-even point.

### 3.4 Pair programming: the limiting case

Pair programming — one continuous reviewer, zero latency — bounds the design space, and its evidence base illustrates a pattern that recurs throughout this corpus: effects found in student samples shrink or vanish in professional ones.

Nosek (1998) and Williams et al. (2000) reported that pairs produced higher-quality solutions with a time overhead well under the naïve 100% (Williams et al. reported roughly 15% more total effort for measurably fewer defects), but both used students or near-novices. Arisholm et al. (2007), in the largest professional experiment (295 consultants), found no general quality benefit: pairing helped juniors on complex tasks (a 48% improvement in correctness in that cell) but conferred no advantage — at nearly double the effort — for seniors or on simple tasks. Hannay et al. (2009), meta-analyzing 18 experiments, found a small positive quality effect, a small negative duration effect, a medium negative effort effect, and substantial heterogeneity explained largely by expertise and task complexity, concluding that pairing is not uniformly beneficial and that expertise moderates everything. Müller (2005) compared pairing directly against solo-programming-plus-review and found comparable quality at comparable cost, suggesting review and pairing are substitutes rather than pairing being strictly superior. Vanhanen and Lassenius (2005) found in an industrial-style setting that pairing's defect benefit was modest and concentrated early in the task.

Two lessons transfer. First, the expertise moderation in Arisholm et al. (2007) and Hannay et al. (2009) matches the reviewer-count literature (Sauer et al., 2000; Kononenko et al., 2015): the value of additional eyes depends on whose eyes and on task difficulty, which argues for risk- and experience-conditioned policies over uniform ones. Second, the student/professional split is a general warning for this corpus: several of the studies most favorable to more reviewers (e.g., Biffl & Halling, 2003) are student studies, while the professional evidence (Porter et al., 1997; Czerwonka et al., 2015; Sadowski et al., 2018) is the evidence least favorable to mandatory second approval.

### 3.5 Why the studies disagree: confounds and design differences

The disagreements in this literature are largely explicable by four design differences, which the extraction sheet codes for each study.

**Population.** Student samples inflate the marginal value of added reviewers (low individual expertise means low overlap between reviewers) and inflate pairing effects; professional samples attenuate both (Arisholm et al., 2007; Porter et al., 1997).

**Outcome definition.** Seeded-defect experiments measure detection of known functional faults; mining studies measure post-release fix-inducing changes, which conflate defect injection, detection, and escape; inspection-era studies measured against lifecycle defect totals under weaker automated tooling. Studies using maintainability-inclusive outcomes (Bavota & Russo, 2015; Morales, McIntosh, & Khomh, 2015 — who found review activity associated with fewer design anti-patterns) find larger review benefits than studies restricted to functional defects (Czerwonka et al., 2015), because most of what modern review catches is not functional.

**Confounding in observational work.** Change size, author experience, and component riskiness confound nearly every mining result. Experienced authors write smaller, cleaner changes *and* attract lighter review; risky components attract both more review and more defects, biasing naïve estimates in opposite directions. McIntosh et al. (2016) and Thongtanunam et al. (2017) control for size and history and their participation effects survive, which is why this review weights them heavily; studies without such controls (several rows in the extraction sheet) are treated as directional only. Rubber-stamping is the most damaging confound for the reviewer-count question specifically: a policy-mandated second approval that takes seconds is recorded identically, in every mined dataset, to an approval preceded by an hour of careful reading. No mining study in the corpus can fully separate "two reviewers" from "two approvals," which means the observational evidence *cannot in principle* establish that a second engaged reviewer adds nothing — only that a second mandated approval, as actually practiced, is not associated with fewer defects.

**Process era.** Pre-1995 studies describe a heavyweight process on a weak-tooling baseline; post-2010 studies describe a lightweight process on a strong-tooling baseline. Comparing detection rates across this divide (Section 3.1) is invalid, and studies are compared here only within era or on marginal effects.

---

## 4. Gaps

Five gaps limit what this review can conclude, and the first two bear directly on Ironwood's decision.

**1. No direct experiment on one versus two reviewers in modern tool-mediated review.** The experimental team-size evidence (Porter et al., 1997; Biffl & Halling, 2003) predates modern review tooling; the modern evidence (Sadowski et al., 2018; Czerwonka et al., 2015) is observational or descriptive. No controlled study in the 84 included papers randomizes reviewer count on real changes in a contemporary pull-request workflow with post-release defect follow-up. The single most decision-relevant quantity — the causal marginal detection rate of a second engaged reviewer on small changes — has never been directly measured.

**2. Distributed and cross-time-zone review is almost unstudied.** Herbsleb and Mockus (2003) establish the coordination penalty of distributed work generally, but the corpus contains no study quantifying how reviewer-count policies interact with time-zone dispersion — precisely the mechanism by which Ironwood's two-approval rule likely produces its 41-hour median. This gap means the latency savings of the proposed change must be estimated from internal telemetry, not the literature.

**3. Small-but-high-blast-radius changes.** The size literature measures review tractability by line count. No included study stratifies review effectiveness by change *consequence* (configuration, infrastructure, migration scripts) rather than change *size*. The March 14 outage sits exactly in this unstudied cell.

**4. Rubber-stamping is documented but not measured as a treatment.** Thongtanunam et al. (2017) and Baysal et al. (2016) characterize low-engagement approval, but no study measures whether policy interventions (checklists, minimum-time gates, accountability framing) causally increase engagement, so the literature offers little on how to make whatever reviewer count is chosen *effective*.

**5. Long-term and maintainability outcomes.** Because most review findings concern evolvability (Mäntylä & Lassenius, 2009; Beller et al., 2014), the cost of reduced review may appear as slower future change rather than defects — an outcome almost no study follows long enough to detect. Morales et al. (2015) is a partial exception. A reviewer-count reduction could look costless on defect metrics for years while degrading design quality.

---

## 5. Implications for Ironwood Labs

The evidence supports the following positions, stated with the confidence the corpus warrants.

**The literature supports reducing the mandatory reviewer count for small changes — conditionally.** The professional-population evidence is consistent: marginal detection from a mandated second approver is small (Porter et al., 1997; Czerwonka et al., 2015; Rigby et al., 2014), quality effects flow through participation and expertise rather than headcount (McIntosh et al., 2016; Kononenko et al., 2015; Thongtanunam et al., 2017), and the largest published single-approval deployment reports no quality penalty (Sadowski et al., 2018). Latency costs are real, compounding, and worsened by cross-time-zone serialization (Herbsleb & Mockus, 2003; MacLeod et al., 2018). A uniform two-approval rule trades a plateauing benefit against a compounding cost.

**The conditions are not optional.** Sadowski et al. (2018) achieved single-approval quality inside a system of small changes, strong ownership, qualified reviewers, and prompt-turnaround norms. The evidence supports one *engaged, qualified* reviewer, not one approval. Three conditions follow directly from the literature: (a) the single reviewer for a change should have ownership or demonstrated familiarity with the touched code (Bosu et al., 2015; Kononenko et al., 2015); (b) approvals with no comments and near-zero dwell time should be surfaced and treated as a process signal, since fast low-discussion approval is the empirical signature of defective changes (Thongtanunam et al., 2017); (c) reviewer load should be monitored, since overloaded reviewers produce worse reviews (Kononenko et al., 2015; Baysal et al., 2016).

**The 200-line threshold should be supplemented by a risk dimension.** Line count predicts review tractability, not consequence. The March 14 outage, and the absence of literature on small high-blast-radius changes (Gap 3), argue for retaining two reviewers — or adding a domain-owner requirement — for configuration, infrastructure, deployment, and data-migration changes regardless of size. The literature's support for single-reviewer approval applies to the ordinary small code change, which is where the latency savings concentrate anyway.

**The change should be run as the experiment the literature lacks.** Given Gap 1, Ironwood is positioned to generate the missing evidence rather than assume it. A staged rollout — randomized or phased by team, with Vasquez-Thorne's telemetry tracking review latency, comment density, dwell time, revert rate, and post-release fix-inducing changes over at least two release cycles, with a pre-registered rollback threshold — converts an irreversible policy bet into a measured one, and controls for the confounds (change size, author experience) that undermine the observational literature.

**What the evidence does not support:** it does not support the claim that the second reviewer is worthless (the observational data cannot distinguish engaged second reviewers from rubber stamps); it does not support relaxing review on high-consequence changes of any size; and it does not support expecting the March 14 class of failure to be prevented by reviewer count at all — that outage was an engagement failure under the *current* policy, and the studies indicate it is addressed by review discipline and change-risk gating, not headcount.

---

## 6. References

Ackerman, A. F., Buchwald, L. S., & Lewski, F. H. (1989). Software inspections: An effective verification process. *IEEE Software, 6*(3), 31–36.

Arisholm, E., Gallis, H., Dybå, T., & Sjøberg, D. I. K. (2007). Evaluating pair programming with respect to system complexity and programmer expertise. *IEEE Transactions on Software Engineering, 33*(2), 65–86.

Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. *Proceedings of the 35th International Conference on Software Engineering (ICSE)*, 712–721.

Baum, T., Schneider, K., & Bacchelli, A. (2019). Associating working memory capacity and code change ordering with code review performance. *Empirical Software Engineering, 24*(4), 1762–1798.

Bavota, G., & Russo, B. (2015). Four eyes are better than two: On the impact of code reviews on software quality. *Proceedings of the IEEE International Conference on Software Maintenance and Evolution (ICSME)*, 81–90.

Baysal, O., Kononenko, O., Holmes, R., & Godfrey, M. W. (2016). Investigating technical and non-technical factors influencing modern code review. *Empirical Software Engineering, 21*(3), 932–959.

Beller, M., Bacchelli, A., Zaidman, A., & Juergens, E. (2014). Modern code reviews in open-source projects: Which problems do they fix? *Proceedings of the 11th Working Conference on Mining Software Repositories (MSR)*, 202–211.

Biffl, S., & Halling, M. (2003). Investigating the defect detection effectiveness and cost benefit of nominal inspection teams. *IEEE Transactions on Software Engineering, 29*(5), 385–397.

Bosu, A., Greiler, M., & Bird, C. (2015). Characteristics of useful code reviews: An empirical study at Microsoft. *Proceedings of the 12th Working Conference on Mining Software Repositories (MSR)*, 146–156.

Czerwonka, J., Greiler, M., & Tilford, J. (2015). Code reviews do not find bugs: How the current code review best practice slows us down. *Proceedings of the 37th International Conference on Software Engineering (ICSE), Software Engineering in Practice track*, 27–28.

Fagan, M. E. (1976). Design and code inspections to reduce errors in program development. *IBM Systems Journal, 15*(3), 182–211.

Fagan, M. E. (1986). Advances in software inspections. *IEEE Transactions on Software Engineering, SE-12*(7), 744–751.

Hannay, J. E., Dybå, T., Arisholm, E., & Sjøberg, D. I. K. (2009). The effectiveness of pair programming: A meta-analysis. *Information and Software Technology, 51*(7), 1110–1122.

Herbsleb, J. D., & Mockus, A. (2003). An empirical study of speed and communication in globally distributed software development. *IEEE Transactions on Software Engineering, 29*(6), 481–494.

Jiang, Y., Adams, B., & German, D. M. (2013). Will my patch make it? And how fast? Case study on the Linux kernel. *Proceedings of the 10th Working Conference on Mining Software Repositories (MSR)*, 101–110.

Kemerer, C. F., & Paulk, M. C. (2009). The impact of design and code reviews on software quality: An empirical study based on PSP data. *IEEE Transactions on Software Engineering, 35*(4), 534–550.

Kononenko, O., Baysal, O., Guerrouj, L., Cao, Y., & Godfrey, M. W. (2015). Investigating code review quality: Do people and participation matter? *Proceedings of the IEEE International Conference on Software Maintenance and Evolution (ICSME)*, 111–120.

MacLeod, L., Greiler, M., Storey, M.-A., Bird, C., & Czerwonka, J. (2018). Code reviewing in the trenches: Challenges and best practices. *IEEE Software, 35*(4), 34–42.

Mäntylä, M. V., & Lassenius, C. (2009). What types of defects are really discovered in code reviews? *IEEE Transactions on Software Engineering, 35*(3), 430–448.

McIntosh, S., Kamei, Y., Adams, B., & Hassan, A. E. (2014). The impact of code review coverage and code review participation on software quality: A case study of the Qt, VTK, and ITK projects. *Proceedings of the 11th Working Conference on Mining Software Repositories (MSR)*, 192–201.

McIntosh, S., Kamei, Y., Adams, B., & Hassan, A. E. (2016). An empirical study of the impact of modern code review practices on software quality. *Empirical Software Engineering, 21*(5), 2146–2189.

Morales, R., McIntosh, S., & Khomh, F. (2015). Do code review practices impact design quality? A case study of the Qt, VTK, and ITK projects. *Proceedings of the 22nd IEEE International Conference on Software Analysis, Evolution, and Reengineering (SANER)*, 171–180.

Müller, M. M. (2005). Two controlled experiments concerning the comparison of pair programming to peer review. *Journal of Systems and Software, 78*(2), 166–179.

Nosek, J. T. (1998). The case for collaborative programming. *Communications of the ACM, 41*(3), 105–108.

Porter, A. A., Siy, H. P., Toman, C. A., & Votta, L. G. (1997). An experiment to assess the cost-benefits of code inspections in large scale software development. *IEEE Transactions on Software Engineering, 23*(6), 329–346.

Porter, A. A., Votta, L. G., & Basili, V. R. (1995). Comparing detection methods for software requirements inspections: A replicated experiment. *IEEE Transactions on Software Engineering, 21*(6), 563–575.

Rigby, P. C., & Bird, C. (2013). Convergent contemporary software peer review practices. *Proceedings of the 9th Joint Meeting on Foundations of Software Engineering (ESEC/FSE)*, 202–212.

Rigby, P. C., German, D. M., Cowen, L., & Storey, M.-A. (2014). Peer review on open-source software projects: Parameters, statistical models, and theory. *ACM Transactions on Software Engineering and Methodology, 23*(4), Article 35.

Rigby, P. C., German, D. M., & Storey, M.-A. (2008). Open source software peer review practices: A case study of the Apache server. *Proceedings of the 30th International Conference on Software Engineering (ICSE)*, 541–550.

Sadowski, C., Söderberg, E., Church, L., Sipko, M., & Bacchelli, A. (2018). Modern code review: A case study at Google. *Proceedings of the 40th International Conference on Software Engineering (ICSE), Software Engineering in Practice track*, 181–190.

Sauer, C., Jeffery, D. R., Land, L., & Yetton, P. (2000). The effectiveness of software development technical reviews: A behaviorally motivated program of research. *IEEE Transactions on Software Engineering, 26*(1), 1–14.

Thongtanunam, P., McIntosh, S., Hassan, A. E., & Iida, H. (2017). Review participation in modern code review: An empirical study of the Android, Qt, and OpenStack projects. *Empirical Software Engineering, 22*(2), 768–817.

Vanhanen, J., & Lassenius, C. (2005). Effects of pair programming at the development team level: An experiment. *Proceedings of the International Symposium on Empirical Software Engineering (ISESE)*, 336–345.

Votta, L. G. (1993). Does every inspection need a meeting? *Proceedings of the 1st ACM SIGSOFT Symposium on Foundations of Software Engineering (FSE)*, 107–114.

Weißgerber, P., Neu, D., & Diehl, S. (2008). Small patches get in! *Proceedings of the 5th Working Conference on Mining Software Repositories (MSR)*, 67–76.

Weller, E. F. (1993). Lessons from three years of inspection data. *IEEE Software, 10*(5), 38–45.

Williams, L., Kessler, R. R., Cunningham, W., & Jeffries, R. (2000). Strengthening the case for pair programming. *IEEE Software, 17*(4), 19–25.
