# Code Review Practices and Defect Detection: A Literature Review

**Prepared for:** Oluwaseun Bamgbose, Vice President of Engineering
**Prepared by:** Wen-Li Tsai, PhD, Staff Research Engineer
**Data support:** Ingrid Vasquez-Thorne, Developer Experience Lead
**Date:** 29 July 2026

---

## 1. Introduction: The Question and Its Scope

Ironwood Labs has required two approving reviewers on every code change since 2019. The platform group has proposed relaxing this to a single approving reviewer for changes under 200 lines, on the grounds that median review latency of 41 hours is the single largest component of lead time from first commit to production. Against this, the severity-one outage of 14 March — 900,000 dollars in service credits, traced to a two-line configuration change that received two approvals in under four minutes — is offered as evidence that review discipline is already too thin rather than too thick.

These two positions are not actually in conflict, and recognizing why is the starting point of this review. The March 14 incident is not evidence that two reviewers are better than one. It is evidence that two reviewers who spend four minutes between them produce approximately the same defect detection as one reviewer who spends four minutes, which is to say very little. The mandate creates a procedural obligation; it does not create attention. The question worth asking is therefore not "one reviewer or two?" but rather: **under what conditions does an additional reviewer produce additional defect detection, what does that additional detection cost in latency, and does the relationship hold for the kinds of changes Ironwood actually produces?**

This review addresses that question against the published research literature on software code review, spanning formal inspection studies from the late 1970s through contemporary repository mining of modern pull-request workflows. It is organized around three outcome dimensions that map onto the decision at hand:

1. **Defect detection** — what proportion of latent defects does review find, and how does that vary with the number of reviewers?
2. **Latency** — what does review cost in elapsed time, and what drives that cost?
3. **Reviewer count specifically** — what is the marginal contribution of the *n*th reviewer?

A fourth theme, **review quality versus review presence**, emerged during screening as the dominant explanatory variable across otherwise contradictory studies, and is treated as a synthesis category in its own right.

The scope is deliberately bounded. This review covers peer code review of source changes: formal inspection, walkthroughs, tool-assisted asynchronous review, and pair programming as a continuous-review variant. It does not cover static analysis, automated testing, formal verification, or fuzzing, except where studies compare these directly against human review. It does not cover architectural or design review conducted at a level above the source change. It covers defect detection and latency as outcomes; it does not systematically cover knowledge transfer, code ownership diffusion, or onboarding effects, though these appear in the discussion where the primary studies raise them, since Ironwood's decision may well hinge on them.

The reader should be warned at the outset about the shape of the answer. The literature does not settle this question. It contains a large body of high-quality work from the formal inspection era whose findings do not transfer cleanly to modern practice; a large body of recent observational work whose findings are heavily confounded; and a small body of controlled experiments that disagree with each other along population lines. What the literature does support is a set of conditional statements — if your changes look like *this*, and your reviewers behave like *that*, then the marginal reviewer is worth approximately *this much*. Whether Ironwood's changes and reviewers fit those conditions is an empirical question that the three years of review telemetry Vasquez-Thorne holds can answer, and which no published study can answer on our behalf. Section 6 sets out what those measurements should be.

---

## 2. How the Literature Was Searched

Searches were conducted between April and June 2026 across two computing digital libraries (the ACM Digital Library and IEEE Xplore), the Scopus abstract and citation database, and the proceedings of eight venues searched directly to capture material indexed inconsistently or not at all: the International Conference on Software Engineering (ICSE), the ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE), the International Conference on Mining Software Repositories (MSR), the International Symposium on Empirical Software Engineering and Measurement (ESEM), the International Conference on Automated Software Engineering (ASE), the International Conference on Software Maintenance and Evolution (ICSME), the Conference on Computer-Supported Cooperative Work (CSCW), and the International Conference on Agile Software Development (XP).

The date range was 1976 through 2026. The lower bound was chosen to capture the formal inspection literature from its origin, on the reasoning that the inspection studies remain the only body of work with rigorously controlled defect-seeding designs, and excluding them would leave the review with no experimental foundation at all.

The search strategy combined three concept blocks: review practice terms (*code review*, *peer review*, *software inspection*, *walkthrough*, *pull request*, *patch review*, *modern code review*, *pair programming*), outcome terms (*defect detection*, *defect density*, *fault*, *post-release defect*, *review effectiveness*, *review latency*, *review turnaround*, *lead time*), and design terms (*reviewer*, *inspector*, *team size*, *number of reviewers*, *review participation*). Backward and forward citation chaining was applied to all included studies and to four prior secondary reviews.

The search returned 1,540 unique records after de-duplication. Title and abstract screening removed 1,291, principally studies of static analysis tools presented as "automated review," studies of academic peer review of manuscripts, and tool papers reporting no empirical evaluation. Full text was obtained and read for 249 records. Of these, 84 were included.

**Inclusion criteria.** Studies were included if they reported primary empirical data — experimental, observational, or case-based — on human review of software changes, and reported at least one outcome relating to defect detection, defect density, review latency, or reviewer count. Both quantitative and qualitative studies were eligible. Studies had to describe their method in enough detail to permit assessment of population, unit of analysis, and defect definition.

**Exclusion criteria.** Excluded were: purely theoretical or simulation studies with no empirical grounding; tool papers with no evaluation against a baseline; studies where review was one undifferentiated component of a bundled process intervention; secondary reviews (used for citation chaining but not counted among the 84); and studies reporting only practitioner opinion without behavioral or defect outcomes.

**The included set** comprises 22 controlled experiments (including quasi-experiments with non-random assignment where allocation was described), 31 repository mining studies, 13 industrial case studies, nine studies of pair programming, and nine studies that fall outside these categories — survey and interview work on reviewer behavior, and observational studies of review interaction that do not mine repositories.

**Extraction.** Data were extracted into a structured sheet held by Vasquez-Thorne, with fields for: population (student, professional, mixed, open-source contributor), unit of analysis (change, file, module, release, developer), defect definition and detection mechanism, review modality, reviewer count (as designed or as observed), change size distribution where reported, latency measures, effect estimates with dispersion, and a structured note on confounding control. Citations throughout this review are by author and year and correspond to the extraction sheet.

**Limitations of the search.** Three should be stated plainly. First, grey literature — engineering blogs, internal reports from large technology firms — was not systematically searched, and a meaningful amount of practical knowledge about review at scale exists only there. Second, the search was English-language only. Third, publication bias in this literature runs in a specific and awkward direction: studies finding that review *works* are more publishable than studies finding it does not, and studies of process interventions are typically published by the people who implemented them. The 60-to-90-percent detection figures from the inspection era in particular should be read with this in mind.

---

## 3. Synthesis

### 3.1 Defect Detection: Two Literatures That Do Not Speak to Each Other

The most striking feature of the defect detection literature is that it splits into two bodies of work that use the same vocabulary to describe different things, and whose numbers cannot be placed on the same axis.

The **formal inspection literature**, originating with Fagan (1976) and elaborated through the 1980s and early 1990s, reports detection rates of 60 to 90 percent of latent defects. Fagan (1976) reported 82 percent detection in the original IBM studies. Russell (1991) reported comparable figures across telecommunications software at scale. Weller (1993) reported detection rates in the 70 percent range across three years of inspection data at Bull HN. These are not casual estimates; several were derived from defect-seeding designs or from capture-recapture estimation of the residual defect pool, and the inspection literature is methodologically the strongest thing this field has produced.

The problem is transfer. Three differences make the inspection numbers inapplicable to Ironwood's decision without heavy qualification.

**The defect definition differs.** Inspection studies counted every deviation from specification found during the inspection meeting, including documentation defects, standards violations, and maintainability concerns. Modern repository studies almost universally define a defect as a change later reverted, or a change linked to a bug-tracker issue, or a line modified by a subsequent fix commit. These are not the same construct. Porter and Votta (1994; 1997) noted explicitly that inspection defect counts included a large proportion of items that would never manifest as runtime failures. The inspection 82 percent and the repository-mined defect linkage rate are measuring different populations of problems, and the inspection figure is inflated relative to the failure-relevant subset by an amount no study in the included set quantifies precisely — though Porter and Votta's (1997) breakdown suggests the failure-relevant fraction may be well under half.

**The baseline differs.** Inspection was introduced into organizations with essentially no other systematic defect-finding mechanism before system test. The counterfactual against which 82 percent detection was measured was "nothing." Ironwood's counterfactual is a pipeline containing unit tests, integration tests, static analysis, type checking, canary deployment, and automated rollback. McIntosh et al. (2014) and Thongtanunam et al. (2016) both observe that the marginal contribution of review must be assessed against what the rest of the pipeline already catches, and that the defect classes review uniquely catches are narrower than the inspection literature implies. The inspection studies measured the value of *any* pre-test defect filter; they cannot tell us the value of the *second reviewer* in a pipeline that already has six other filters.

**The process differs.** Fagan inspection involved individual preparation with a checklist, a synchronous meeting with defined roles (moderator, reader, author, inspector), a rework phase, and a formal follow-up gate. Modern tool-assisted review involves an asynchronous comment thread, often with no preparation phase, no checklist, no defined roles, and no verified rework. Votta (1993) — a finding that deserves more attention than it receives — showed that the synchronous meeting itself contributed only about 4 percent of defects found, with the overwhelming majority discovered during individual preparation. This is the single most transferable finding in the inspection literature, and it cuts *toward* the platform group's proposal rather than against it: if detection is produced by individual preparation rather than by collective discussion, then the mechanism by which a second reviewer might add value is simply "a second independent pass," not "discussion between reviewers." That framing makes the marginal contribution of reviewer two an independence question, which Section 3.3 addresses directly.

The **modern repository literature** finds consistently that review participation correlates with lower post-release defect density, but with effect sizes far below what the inspection literature would predict, and with a persistent inability to separate review from its correlates.

McIntosh et al. (2014), analyzing Qt, VTK, and ITK, found that components with lower review coverage and lower reviewer participation had significantly higher post-release defect density. This is among the most-cited findings in the modern literature and is frequently invoked as evidence that more review is better. Its limitation is that review coverage is not randomly assigned: components receiving little review are disproportionately peripheral, unfamiliar, low-traffic, or maintained by fewer people, and each of those is independently associated with defects. McIntosh et al. were careful about this; many who cite them are not.

Thongtanunam et al. (2016) extended this with a code-ownership lens and found that review participation effects attenuated substantially once ownership concentration was controlled. Kononenko et al. (2015), working on Mozilla, found that reviewer experience and review *thoroughness* — measured through comment density and review duration — predicted defect-proneness of reviewed changes far better than reviewer count did. This is the pivot point of the entire modern literature: **the measured quantity that predicts outcomes is the intensity of attention, not the number of people nominally attached to the change.**

Bacchelli and Bird (2013), in interview and observational work at Microsoft, provided the mechanism behind that statistic. Reviewers reported that defect finding was one of several goals, and often not the primary one; knowledge transfer, awareness of concurrent work, and maintenance of shared standards ranked comparably. Critically, they found that reviewers' ability to find functional defects depended heavily on prior familiarity with the code under review, and that a reviewer without context could reliably comment only on style, naming, and local structure. This finding recurs throughout the qualitative literature (Sadowski et al., 2018; MacLeod et al., 2018) and has a sharp implication for reviewer-count policy: a *second* reviewer assigned for procedural coverage rather than for context is systematically likely to be the less-contextual of the two, and therefore to contribute disproportionately style-level rather than defect-level feedback.

Rigby and Bird (2013), comparing review practice across open-source projects and Microsoft, found convergent behavior across radically different governance models: small changes, few reviewers, and rapid turnaround, with two reviewers as a common *observed* equilibrium — but with the second reviewer's comments overwhelmingly concentrated in the first review round and dropping off sharply thereafter. Their data are consistent with a model in which two reviewers is a social convention that emerged for reasons partly unrelated to defect detection.

### 3.2 Latency: The Cost Side, and What Actually Drives It

Ironwood's median review latency is 41 hours. The literature is clear that this figure is unremarkable and that its causes are probably not what the platform group's proposal assumes.

The most consistent finding across the latency literature is that **review latency is dominated by waiting, not by reviewing.** Rigby et al. (2014), analyzing review intervals across multiple projects, decomposed turnaround into time-to-first-response and time-in-active-review, and found the former dominant by a wide margin. Baysal et al. (2016), studying WebKit and Blink, found that non-technical factors — reviewer workload, organizational affiliation of the submitter, time of submission relative to reviewer working hours — explained substantial variance in review latency beyond change characteristics. Thongtanunam et al. (2017) found that changes with no explicitly assigned reviewer waited significantly longer, and that reviewer assignment, not reviewer count, was the actionable lever.

This has a direct bearing on the proposal. If Ironwood's 41-hour median is composed principally of time-to-first-response, then removing the second reviewer removes a *sequential* wait only if the two reviews are in fact sequential. Where reviews proceed in parallel — both reviewers notified simultaneously, both able to approve independently — the latency of a two-reviewer change is the *maximum* of two waiting times rather than their sum. Under a plausible distribution of individual response times, moving from the max of two draws to a single draw reduces expected latency by considerably less than half. Vasquez-Thorne's telemetry can distinguish these cases directly: the relevant measurement is the distribution of the gap between first approval and second approval, and whether the second reviewer's clock starts at submission or at first approval.

A second latency finding cuts against the proposal's framing. Multiple studies find that **change size is the strongest single predictor of review latency**, and that the relationship is steeply non-linear. Rigby et al. (2014) and Baysal et al. (2016) both report that large changes wait disproportionately longer, both because reviewers defer them and because they generate more review rounds. Weißgerber et al. (2008), studying open-source patch acceptance, found small patches were accepted faster and at higher rates. If Ironwood's latency is concentrated in changes *above* the 200-line threshold, then a policy that relaxes review only for changes *below* the threshold will address the part of the distribution that is already fast, and the median may move far less than expected. This is measurable: the relevant figure is the latency distribution conditioned on change size, not the aggregate median.

There is also a real cost to latency that the literature supports and that should not be dismissed as developer preference. Studies of review queue effects (Gousios et al., 2014; 2015) document that long review waits drive context-switching, work-in-progress accumulation, and batching of changes into larger units — which then take even longer to review, producing a reinforcing cycle. The mechanism by which high review latency *increases* defect rates is through change size inflation: developers waiting on review continue working, and their next change is built atop unmerged work or bundled to amortize the review cost. Kudrjavets et al. (2022) found associations between long review cycle times and larger subsequent changes. If this dynamic is present at Ironwood, then latency is not merely a velocity cost; it is a quality cost operating through the change-size channel, and the platform group's proposal has a defect-reduction argument available to it that it has not made.

### 3.3 Reviewer Count: The Direct Evidence

On the specific question of the marginal reviewer, the literature is thinner than the volume of surrounding work suggests, and what exists points consistently in one direction with important caveats.

**The inspection-era experimental evidence.** Porter, Siy, Mockus, and Votta (1997), in the strongest experimental treatment of this question, varied inspection team size and structure in a professional setting over 18 months. They found that larger teams did not detect proportionally more defects, and that two-person inspections performed comparably to four-person inspections on defect detection while consuming substantially less effort. Porter and Votta (1994) had earlier found similar diminishing returns. Bisant and Lyle (1989) found a two-person inspection effective relative to no inspection — a comparison that establishes the value of the *first* reviewer, not the second.

The mechanism proposed in this literature is defect overlap: reviewers examining the same artifact with similar training and similar tooling find substantially overlapping defect sets. The marginal reviewer contributes only their *non-overlapping* detections, and overlap rises as reviewers become more similar. Sauer et al. (2000), in a theoretical synthesis grounded in the behavioral decision literature, argued that inspection performance is driven principally by individual expertise rather than group process, predicting steep diminishing returns to team size — a prediction the empirical work has broadly borne out.

**The modern observational evidence.** Rigby and Bird (2013) found that the number of reviewers converged to approximately two across diverse projects, but that comment volume and defect-relevant feedback dropped sharply after the first reviewer. Beller et al. (2014), analyzing review comments in two open-source projects, found that the great majority of review-triggered changes were maintainability-related rather than functional, with functional defect findings concentrated in the first review pass. McIntosh et al. (2016), extending their earlier work, found that *proportion of reviewers with prior file experience* mattered more than raw count.

Several studies find the second reviewer adds little beyond the first. The important qualification is that nearly all of these observe reviewer count as it naturally occurs rather than as assigned, which introduces a selection problem running in a specific direction: changes that attract more reviewers are disproportionately changes someone thought were risky. This biases observational estimates of the marginal reviewer's *defect-reduction* effect toward zero or negative, because high-reviewer changes are riskier changes. The finding that "the second reviewer adds little" is therefore *conservative* in an unhelpful way — it may understate the true effect of an assigned second reviewer on a randomly selected change.

There is a countervailing consideration the literature supports less directly but consistently raises. **Reviewer count may matter for reasons other than defect detection.** Bacchelli and Bird (2013), Sadowski et al. (2018), and MacLeod et al. (2018) all report knowledge transfer and code familiarity diffusion as primary perceived benefits. Thongtanunam et al. (2016) found that concentrated ownership was itself a defect risk factor. If the second reviewer's function at Ironwood is to spread familiarity across a 430-person organization — reducing bus factor, keeping more engineers competent in more subsystems — then evaluating the policy solely on defect detection measures the wrong thing. This should be surfaced explicitly rather than left implicit, because it is a genuine cost of the proposal that the defect-detection literature will not capture.

### 3.4 Review Quality Versus Review Presence: The March 14 Problem

The March 14 outage — two approvals in under four minutes on a two-line configuration change — is a specific instance of a phenomenon the literature names and studies: rubber-stamping.

Multiple studies document that a substantial fraction of approvals occur too quickly to represent meaningful examination. Czerwonka et al. (2015), reporting on Microsoft data, found large proportions of reviews producing no comments at all, and argued that review effectiveness varies enormously with reviewer engagement. Bosu et al. (2015) found that a minority of review comments were classified as useful by recipients, with usefulness strongly predicted by reviewer familiarity with the code. Kononenko et al. (2016), surveying Mozilla reviewers, found reviewers themselves reported time pressure and unfamiliarity as the dominant causes of superficial review.

Two mechanisms in this literature bear directly on the March 14 incident.

**Diffusion of responsibility.** When multiple reviewers are assigned, each may reason that the others will examine carefully. This is a classic social-loafing prediction, and while the software-specific evidence is not as strong as one would like, Rigby and Bird (2013) observed lower per-reviewer comment rates in higher-reviewer-count reviews, consistent with it. If this operates at Ironwood, then the two-reviewer mandate may *reduce* per-reviewer diligence relative to a single-reviewer regime with clear accountability. A four-minute double approval is exactly what this mechanism predicts. It is entirely possible — and the telemetry can test it — that the March 14 change would have received *more* scrutiny under a single-reviewer policy in which one named person was unambiguously accountable.

**Size-based heuristics and the small-change blind spot.** The literature consistently finds that reviewers calibrate effort to apparent size (Rigby et al., 2014; Baysal et al., 2016; Beller et al., 2014). A two-line configuration change presents as trivial. But defect *severity* does not scale with change size, and configuration changes in particular have a well-documented capacity to produce large-blast-radius failures from tiny diffs. This is not merely a review problem — Ironwood's deployment pipeline evidently propagated a configuration change to a severity-one blast radius without staged rollout or automated rollback catching it — but the review-relevant lesson is sharp and cuts *against* the platform group's specific proposal.

**The 200-line threshold is the wrong discriminator.** The proposal uses change size as a proxy for risk. The literature does not support this proxy. Size predicts *review effort required* and *number of defects present*, but it does not predict *severity of the worst defect*, which is what the March 14 incident was about. The correct discriminator is blast radius: what can this change break, how fast, and how quickly can it be reversed? Configuration touching production traffic routing, authentication, data retention, or billing warrants the strongest review regardless of line count. A 400-line refactor of a well-tested internal library with no behavioral change warrants less. A line-count threshold gets both of these backwards. This is, in my assessment, the most actionable finding in the entire review, and it suggests the proposal should be *restructured* rather than accepted or rejected.

### 3.5 Pair Programming: A Population-Split Finding

Nine included studies address pair programming as a continuous-review variant. The finding is a clean population split.

Student-sample experiments generally report positive effects on defect rates and, in some designs, on total effort. Williams et al. (2000) reported higher-quality output from pairs at modest effort premium. Nagappan et al. (2003), in an educational setting, reported similar directional findings. Multiple replications with student populations report positive effects.

Professional-sample studies are markedly weaker. Arisholm et al. (2007), in the largest controlled experiment in this literature — 295 professional developers — found that pair programming produced no significant overall improvement in correctness, with effects varying substantially by task complexity and developer expertise. Pairs showed benefit on complex tasks with junior developers and little or no benefit for senior developers on simpler tasks, at roughly an 84 percent effort premium. Müller (2005) found pair programming produced quality comparable to solo development followed by review, at comparable total cost. Hannay et al. (2009), meta-analyzing the pair programming literature, found small overall effects with substantial heterogeneity and evidence consistent with publication bias.

The explanation for the split is plausible and matters for Ironwood. Student populations have low and homogeneous baseline expertise; the second person supplies knowledge the first lacks. Professional populations have higher and more heterogeneous expertise; the second person more often supplies redundant knowledge. **This is the same overlap mechanism that explains diminishing returns to inspection team size, appearing in a different literature.** Both point to the same conclusion: *the marginal reviewer's value is a function of the knowledge they hold that the first reviewer does not.*

For a 430-person organization with specialized subsystems, this is encouraging for a targeted policy and discouraging for a blanket one. Two reviewers drawn from the same team, with the same context, reviewing the same change, are close to the professional pair-programming case — redundant. Two reviewers drawn deliberately from different areas, one with subsystem context and one with cross-cutting concern context (security, data handling, operational behavior), are close to the student case — complementary. A policy that mandates two reviewers without specifying *which two* is capturing the redundant case most of the time.

### 3.6 Setting the Bodies of Evidence Against Each Other

Three specific disagreements are worth stating explicitly, along with the design differences that produce them.

**Inspection studies report 60–90 percent detection; repository studies report modest effects.** The disagreement is largely definitional and contextual rather than substantive. Different defect constructs (specification deviations versus failure-linked defects), different baselines (no prior filter versus a full modern pipeline), different processes (prepared, checklisted, role-assigned versus asynchronous and unstructured). These numbers should never be placed side by side. The transferable inspection findings are the *structural* ones — Votta's (1993) finding that preparation rather than meeting produces detection, and Porter et al.'s (1997) finding of diminishing returns to team size — not the headline percentages.

**Repository studies find review participation reduces defects; several find the second reviewer adds little.** These are compatible. The first reviewer captures most of the available benefit; the curve is steeply concave. McIntosh et al. (2014) measured the difference between *little or no* review and *some* review; the studies finding weak marginal effects measured the difference between one and two. Both can be true and probably are. The policy-relevant reading is that Ironwood is operating on the flat part of the curve, where the first reviewer is doing most of the work.

**Pair programming experiments split by population.** Explained above by knowledge overlap. The design difference is subject expertise distribution, and it is not a nuisance variable — it is the mechanism.

Across all three, the same underlying variable does the explanatory work: **the marginal value of an additional reviewer equals the non-redundant knowledge and attention that reviewer brings.** Every finding in this review is consistent with that principle. Policies that add reviewers without adding non-redundant knowledge add latency and little else.

---

## 4. Gaps in the Literature

**Reviewer count is almost never randomly assigned.** The dominant limitation. Nearly all modern evidence is observational with reviewer count as an outcome of a risk-assessment process, not an input. The selection bias runs against detecting a true marginal-reviewer effect. Randomized assignment of one versus two reviewers within a change-risk stratum, at organizational scale, has essentially not been done and would be the single most valuable study this field could produce. Ironwood is positioned to run it.

**Rubber-stamping is under-instrumented.** Studies measure review presence, comment counts, and duration, but rarely distinguish substantive from perfunctory approval with validated measures. Time-to-approval is a crude proxy — a four-minute approval by a reviewer who wrote the surrounding code may be well-founded; a forty-minute approval by someone lost in unfamiliar code may not be. No included study offers a validated measure of review depth.

**Distributed and cross-time-zone review is nearly absent.** Almost nothing in the included set addresses teams reviewing across time zones. This is a serious gap given that time-zone offset is mechanically one of the largest drivers of review waiting time. Ironwood is single-site in Austin, which means the literature's latency figures — largely drawn from distributed open-source projects — likely *overstate* the latency Ironwood should expect and correspondingly *understate* how much of Ironwood's 41 hours is attributable to queueing and prioritization rather than to unavoidable scheduling friction. This should sharpen rather than soften scrutiny of the 41-hour figure: single-site teams have fewer structural excuses for it.

**Configuration and infrastructure changes are barely studied.** The literature is overwhelmingly about application source code. Configuration changes, infrastructure-as-code, feature flags, and deployment manifests — precisely the category implicated on March 14 — are close to absent, despite a distinctive risk profile: tiny diffs, large blast radius, weak test coverage, immediate production effect. This is the most important gap for Ironwood specifically.

**Change size and author experience confound nearly everything.** Both correlate with reviewer count, review latency, review depth, and defect probability. Studies controlling for them find attenuated effects; many do not control adequately. Effect estimates in this literature should be read as upper bounds.

**Severity is rarely modeled.** Most studies treat defects as countable and interchangeable. The March 14 incident cost 900,000 dollars; a typographical defect in a log message costs nothing. A policy optimized for defect *count* may be badly misaligned with one optimized for expected *loss*. Almost no study in the included set models severity-weighted outcomes.

**Publication and reporting bias.** Process interventions are typically evaluated by their implementers. Hannay et al. (2009) found evidence consistent with publication bias in the pair programming literature; there is no reason to think the code review literature is immune.

**Interaction with the modern pipeline is untested.** No included study estimates the marginal contribution of human review conditional on the presence of comprehensive automated testing, static analysis, type checking, and canary deployment. Every effect estimate in this review was produced against a weaker automated baseline than Ironwood operates, and should be discounted accordingly.

---

## 5. Implications for Ironwood Labs

The literature does not support the two-reviewer mandate as currently constituted, and it does not support the platform group's proposal as currently constituted either. It supports a third option.

**What the literature supports with reasonable confidence:**

1. *The first reviewer captures most of the available benefit.* Diminishing returns to reviewer count are among the most consistent findings across inspection experiments, modern repository work, and pair programming (Porter et al., 1997; Sauer et al., 2000; Rigby & Bird, 2013; Hannay et al., 2009).

2. *Review depth predicts outcomes better than reviewer count.* Kononenko et al. (2015; 2016), Bosu et al. (2015), and Bacchelli & Bird (2013) converge here. A blanket count requirement optimizes an ineffective variable.

3. *The marginal reviewer's value equals their non-redundant knowledge.* The unifying principle across all three literatures. Two reviewers from the same context are largely redundant.

4. *Latency has real quality costs through the change-size channel.* Long waits inflate change size, and larger changes are harder to review and more defect-prone (Gousios et al., 2014; Kudrjavets et al., 2022).

5. *Size is a poor proxy for risk.* March 14 is a textbook instance. Blast radius, not line count, is the appropriate discriminator.

**What follows for the decision:**

**Do not adopt the 200-line threshold as proposed.** It uses the wrong discriminator and would have permitted single-reviewer approval of exactly the change that caused March 14. Adopting it would be defensible on velocity grounds and indefensible on risk grounds, and the risk objection is the one that will be raised after the next incident.

**Do relax the blanket two-reviewer requirement, replacing it with a risk-tiered policy.** The recommended structure:

- **Tier 1 — elevated review, two reviewers with specified complementary roles:** changes touching production configuration, traffic routing, authentication and authorization, data retention or deletion, billing, or any path lacking automated test coverage or automated rollback. Two reviewers, one with subsystem context and one with cross-cutting concern context, regardless of line count.
- **Tier 2 — standard review, one reviewer:** application source changes with test coverage and automated rollback available, regardless of line count within reason.
- **Tier 3 — expedited:** documentation, comments, test-only changes, dependency version bumps with automated verification.

Tier assignment should be automated from path-based rules with author-initiated escalation and reviewer-initiated escalation, not left to individual judgment.

**Pair the change with depth instrumentation, not count instrumentation.** Measure time-in-review, comment density, and files-viewed-versus-files-changed. Establish minimum expectations for Tier 1 review depth. A four-minute approval on a Tier 1 change should be flagged automatically. This addresses the actual March 14 failure mode, which was not too few reviewers.

**Address the knowledge-diffusion cost explicitly.** If the second reviewer currently serves familiarity-spreading purposes, removing it has a cost the defect literature will not measure. Recommended mitigation: retain a non-blocking second reviewer as an asynchronous notification for Tier 2 changes — informed but not gating. This preserves diffusion while removing the latency.

**Run the experiment the literature has not.** Ironwood is unusually well-positioned. With three years of telemetry and 430 engineers, a staged rollout — Tier 2 single-reviewer in two or three teams first, with defect escape rate, severity-weighted incident cost, latency, and change size tracked against matched control teams for at least two quarters — would produce better evidence for this decision than anything in the published literature. Pre-register the outcome measures, including a severity-weighted incident cost measure, before rollout.

**Measurements to make before deciding.** From Vasquez-Thorne's telemetry:

1. Latency distribution conditioned on change size — is the 41-hour median driven by changes above or below 200 lines?
2. Gap between first and second approval — are reviews parallel or sequential? This determines the latency saving available.
3. Time-to-approval distribution — what fraction of approvals occur under five minutes, and does this differ between first and second reviewers?
4. Reviewer context overlap — how often do both reviewers come from the same team with the same file history?
5. Defect escape rate by change size — do sub-200-line changes actually escape fewer defects, or fewer *severe* defects?
6. Blast-radius classification of the past two years of incidents — what fraction involved changes that would fall under the proposed threshold?

Measurement 6 is decisive. If a substantial share of severity-one incidents trace to sub-200-line changes, the proposal as written is disqualified on its own evidence, and the tiered alternative becomes the only defensible option.

**A closing note on the framing.** The March 14 incident is being used to argue that review discipline is too thin. The literature suggests a different reading: that a mandate producing four-minute double approvals was never producing the protection it appeared to. The organization has been paying 41 hours of latency for a control that, on the evidence, was not functioning as designed. The choice is not between velocity and safety. It is between a control that is expensive and ineffective, and one that is cheaper and targeted at the changes that can actually cause a 900,000-dollar loss.

---

## 6. References

Arisholm, E., Gallis, H., Dybå, T., & Sjøberg, D. I. K. (2007). Evaluating pair programming with respect to system complexity and programmer expertise. *IEEE Transactions on Software Engineering*, 33(2), 65–86.

Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. In *Proceedings of the 35th International Conference on Software Engineering* (pp. 712–721).

Baysal, O., Kononenko, O., Holmes, R., & Godfrey, M. W. (2016). Investigating technical and non-technical factors influencing modern code review. *Empirical Software Engineering*, 21(3), 932–959.

Beller, M., Bacchelli, A., Zaidman, A., & Juergens, E. (2014). Modern code reviews in open-source projects: Which problems do they fix? In *Proceedings of the 11th Working Conference on Mining Software Repositories* (pp. 202–211).

Bisant, D. B., & Lyle, J. R. (1989). A two-person inspection method to improve programming productivity. *IEEE Transactions on Software Engineering*, 15(10), 1294–1304.

Bosu, A., Greiler, M., & Bird, C. (2015). Characteristics of useful code reviews: An empirical study at Microsoft. In *Proceedings of the 12th Working Conference on Mining Software Repositories* (pp. 146–156).

Czerwonka, J., Greiler, M., & Tilford, J. (2015). Code reviews do not find bugs: How the current code review best practice slows us down. In *Proceedings of the 37th International Conference on Software Engineering* (Vol. 2, pp. 27–28).

Fagan, M. E. (1976). Design and code inspections to reduce errors in program development. *IBM Systems Journal*, 15(3), 182–211.

Gousios, G., Pinzger, M., & van Deursen, A. (2014). An exploratory study of the pull-based software development model. In *Proceedings of the 36th International Conference on Software Engineering* (pp. 345–355).

Gousios, G., Zaidman, A., Storey, M.-A., & van Deursen, A. (2015). Work practices and challenges in pull-based development: The integrator's perspective. In *Proceedings of the 37th International Conference on Software Engineering* (pp. 358–368).

Hannay, J. E., Dybå, T., Arisholm, E., & Sjøberg, D. I. K. (2009). The effectiveness of pair programming: A meta-analysis. *Information and Software Technology*, 51(7), 1110–1122.

Kononenko, O., Baysal, O., Guerrouj, L., Cao, Y., & Godfrey, M. W. (2015). Investigating code review quality: Do people and participation matter? In *Proceedings of the 31st International Conference on Software Maintenance and Evolution* (pp. 111–120).

Kononenko, O., Baysal, O., & Godfrey, M. W. (2016). Code review quality: How developers see it. In *Proceedings of the 38th International Conference on Software Engineering* (pp. 1028–1038).

Kudrjavets, G., Nagappan, N., & Rastogi, A. (2022). Do small code changes merge faster? A multi-language empirical investigation. In *Proceedings of the 19th International Conference on Mining Software Repositories* (pp. 537–548).

MacLeod, L., Greiler, M., Storey, M.-A., Bird, C., & Czerwonka, J. (2018). Code reviewing in the trenches: Challenges and best practices. *IEEE Software*, 35(4), 34–42.

McIntosh, S., Kamei, Y., Adams, B., & Hassan, A. E. (2014). The impact of code review coverage and code review participation on software quality. In *Proceedings of the 11th Working Conference on Mining Software Repositories* (pp. 192–201).

McIntosh, S., Kamei, Y., Adams, B., & Hassan, A. E. (2016). An empirical study of the impact of modern code review practices on software quality. *Empirical Software Engineering*, 21(5), 2146–2189.

Müller, M. M. (2005). Two controlled experiments concerning the comparison of pair programming to peer review. *Journal of Systems and Software*, 78(2), 166–179.

Nagappan, N., Williams, L., Ferzli, M., Wiebe, E., Yang, K., Miller, C., & Balik, S. (2003). Improving the CS1 experience with pair programming. In *Proceedings of the 34th SIGCSE Technical Symposium on Computer Science Education* (pp. 359–362).

Porter, A. A., & Votta, L. G. (1994). An experiment to assess different defect detection methods for software requirements inspections. In *Proceedings of the 16th International Conference on Software Engineering* (pp. 103–112).

Porter, A. A., Siy, H., Mockus, A., & Votta, L. G. (1997). Understanding the sources of variation in software inspections. *ACM Transactions on Software Engineering and Methodology*, 7(1), 41–79.

Rigby, P. C., & Bird, C. (2013). Convergent contemporary software peer review practices. In *Proceedings of the 9th Joint Meeting on Foundations of Software Engineering* (pp. 202–212).

Rigby, P. C., German, D. M., Cowen, L., & Storey, M.-A. (2014). Peer review on open-source software projects: Parameters, statistical models, and theory. *ACM Transactions on Software Engineering and Methodology*, 23(4), Article 35.

Russell, G. W. (1991). Experience with inspection in ultralarge-scale developments. *IEEE Software*, 8(1), 25–31.

Sadowski, C., Söderberg, E., Church, L., Sipko, M., & Bacchelli, A. (2018). Modern code review: A case study at Google. In *Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice* (pp. 181–190).

Sauer, C., Jeffery, D. R., Land, L., & Yetton, P. (2000). The effectiveness of software development technical reviews: A behaviorally motivated program of research. *IEEE Transactions on Software Engineering*, 26(1), 1–14.

Thongtanunam, P., McIntosh, S., Hassan, A. E., & Iida, H. (2016). Revisiting code ownership and its relationship with software quality in the scope of modern code review. In *Proceedings of the 38th International Conference on Software Engineering* (pp. 1039–1050).

Thongtanunam, P., McIntosh, S., Hassan, A. E., & Iida, H. (2017). Review participation in modern code review: An empirical study of the Android, Qt, and OpenStack projects. *Empirical Software Engineering*, 22(2), 768–817.

Votta, L. G. (1993). Does every inspection need a meeting? *ACM SIGSOFT Software Engineering Notes*, 18(5), 107–114.

Weißgerber, P., Neu, D., & Diehl, S. (2008). Small patches get in! In *Proceedings of the 5th Working Conference on Mining Software Repositories* (pp. 67–76).

Weller, E. F. (1993). Lessons from three years of inspection data. *IEEE Software*, 10(5), 38–45.

Williams, L., Kessler, R. R., Cunningham, W., & Jeffries, R. (2000). Strengthening the case for pair programming. *IEEE Software*, 17(4), 19–25.

---

*The full extraction sheet covering all 84 included studies — with population, unit of analysis, defect definition, reviewer count, change size distribution, latency measures, effect estimates, and confounding-control assessment — is held by I. Vasquez-Thorne and is available on request. The 36 studies cited above are those bearing most directly on the three outcome dimensions framing this review; the remaining 48 inform the synthesis without being individually cited.*
