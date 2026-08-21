# Predictable Scheduling in Food Retail: What the Evidence Supports for a 61-Store Chain

**Prepared for the Pinal Ridge Markets capital meeting, January 2027**
Dr. Hyun-Woo Chang, labor economist
Internal data extraction: Camille Deschamps-Iyer

---

## 1. Introduction: the question, and what it is not

Pinal Ridge Markets is weighing a twelve-store pilot of predictable scheduling: schedules posted fourteen days in advance, a guaranteed weekly core of hours for each covered employee, and elimination of on-call shifts. Chief people officer Delia Marchbanks has proposed it as a retention intervention against 87 percent annual turnover among front-end clerks at a replacement cost of roughly $2,100 each. Chief financial officer Priyansh Bhatt has costed it at $1.9 million a year. The board's question is narrow and practical: does the research literature support the expectation that this bundle of practices, in a grocery chain of this size and labor composition, will return more than it costs?

This review answers a question in that shape, but it cannot answer it in that form. The literature does not contain a study of Pinal Ridge Markets, and it contains very few studies of any grocery chain. What it contains is a body of work — nine field experiments, twenty-one quasi-experimental evaluations of municipal scheduling ordinances, sixteen administrative-data studies, and seven qualitative studies, fifty-nine in all after screening — that disagrees with itself on nearly every quantity the board cares about. The disagreements are not random noise. They track identifiable differences in how studies define the intervention, which outcomes they measure, over what horizon, in which sector, and against which counterfactual. The useful work of a review is to make those differences legible, so that the board can decide which strand of evidence its own situation most resembles.

Three scope decisions shape what follows.

**First, "stable scheduling" is a bundle, not a variable.** The three components Marchbanks proposes — advance notice, guaranteed core hours, no on-call — are conceptually and operationally distinct. Advance notice is an information practice; it changes what a worker knows and when. Guaranteed core hours is an income-floor practice; it changes what a worker can count on earning. Eliminating on-call is a risk-allocation practice; it changes who absorbs demand uncertainty. The literature almost never separates them. Field experiments deploy them together, often alongside additional staffing budget or manager training. Ordinance evaluations study statutes that combine them with predictability pay, right-to-rest provisions, and access-to-hours rules for existing part-timers. Administrative studies typically observe one component — usually notice — and infer about the rest. When studies disagree about "stable scheduling," some of that disagreement is that they are not studying the same thing (Lambert 2008; Fugiel and Lambert 2019). This review therefore reports, wherever the source permits, which components were actually in the treatment.

**Second, the outcomes of interest are four, and they are not commensurable.** Turnover and its replacement cost; sales and labor productivity; the direct payroll cost of the intervention; and worker outcomes including sleep, health, income volatility, and caregiving stability. The first three enter Bhatt's model. The fourth mostly does not, and the studies that measure it are largely different studies, using different designs, from those that measure the first three. A synthesis that runs them together will produce a false consensus.

**Third, the relevant firm is a mid-market regional grocer with 61 stores, 8,400 employees, and 61 percent part-time composition.** This matters more than it may appear. The best-identified experimental evidence comes from specialty apparel. The best-identified quasi-experimental evidence comes from ordinance jurisdictions where large national chains dominate the covered population. Pinal Ridge is neither. Grocery has different demand predictability, different perishability constraints, different cross-training economics, and — critically — a different relationship between staffing and sales than apparel does. Section 3.7 treats this directly.

Excluded from scope: shift-work and circadian research on night and rotating schedules in healthcare and manufacturing, which addresses a different exposure; gig-platform scheduling autonomy, cited here only where it bears on how workers value schedule control; and European sectoral-bargaining models, which are informative comparatively (Carré and Tilly 2017) but not transferable to Arizona and Nevada.

---

## 2. Note on the search

**Databases and sources.** EconLit; Business Source Complete; PsycINFO; and the working-paper series of four labor research centers, hand-searched by year rather than by keyword because working papers are indexed inconsistently. Reference lists of the eleven most-cited included studies were back-searched, and forward citations were checked in Google Scholar. Date range 1998–2026. The lower bound is deliberate: sustained empirical attention to schedule instability as distinct from nonstandard hours begins in the early 2000s, but the 1998 bound captures the earlier retail-operations literature on labor and sales that the later work builds on.

**Search terms.** Combinations of *(scheduling OR schedule OR "work hours" OR shift)* with *(unpredictab\* OR instabil\* OR volatil\* OR "advance notice" OR "just-in-time" OR "on-call" OR "fair workweek" OR "secure scheduling" OR "predictive scheduling" OR "stable scheduling")* and *(retail OR grocery OR "food retail" OR "service sector" OR hourly)*, plus outcome terms *(turnover OR separation OR quit OR retention OR sales OR productivity OR sleep OR health OR "material hardship" OR "child care")*.

**Screening.** 1,120 records after de-duplication. Title and abstract screening removed 903, principally studies of nonstandard hours without an instability component, healthcare shift-work studies, and gig-economy work. 217 full texts read. 158 excluded at full text: no comparison condition (61), exposure not separable from wage or hours level (34), outcome not among the four domains (29), duplicate sample already represented by a more complete report (21), non-U.S. institutional setting without a transferable design (13). Fifty-nine studies included.

**Included designs.** Nine field experiments or randomized/quasi-randomized firm-level trials. Twenty-one quasi-experimental ordinance evaluations, using difference-in-differences, synthetic control, or pre-post panels with out-of-jurisdiction comparisons. Sixteen administrative-data studies using firm payroll and point-of-sale records or large repeated cross-sectional worker surveys. Seven qualitative studies using ethnography, manager interviews, or worker focus groups.

**Appraisal.** Each study was coded for treatment definition (which of the three components), unit of randomization or assignment, outcome measurement source (self-report vs. administrative), follow-up horizon, sector, firm size, and — for ordinance studies — compliance verification. These codes are the basis for Section 3.8, which is where the review does most of its analytic work.

**Limits and disclosures.** Grey literature from advocacy organizations on both sides was included but coded separately; where it is cited below, the affiliation is stated. Publication bias could not be formally assessed: the field-experiment stratum is too small for funnel-plot methods, and the ordinance stratum is dominated by evaluations commissioned by the enacting jurisdictions, which is a directional concern in both directions — cities want their ordinances to work, and the researchers they hire have professional incentives to report null results credibly. No study was excluded on quality grounds alone; low-quality studies are reported as such.

Citations below are author–year. Full bibliographic detail, extracted effect sizes with confidence intervals, outcome definitions, and firm-size codes are in the extraction file compiled by Deschamps-Iyer. Where a specific point estimate is quoted here, it is the estimate as published; anyone relying on a number for the capital decision should verify it against the file, because several widely repeated figures in this literature are quoted out of their original conditioning.

---

## 3. Synthesis

### 3.1 Turnover: the largest and most consequential disagreement

Turnover is the outcome on which Marchbanks's proposal rests, and it is the outcome on which the literature is most sharply split — not on the sign of the association, which is consistent, but on whether the association is causal and how large the causal effect is.

The observational evidence is unambiguous and large. Using repeated cross-sections of service-sector workers, Choper, Schneider, and Harknett (2022) find that on-call shifts, last-minute cancellations, and short notice are each independently associated with substantially elevated intention to leave and with actual job separation in follow-up waves. The magnitudes are not marginal; in their models, exposure to on-call scheduling predicts turnover at a level comparable to sizeable wage differences. Lambert, Fugiel, and Henly (2014), working with early-career panel data, and Golden (2015), using national survey data, report the same directional pattern. Henly and Lambert (2014), in a women's apparel chain, find unpredictable timing predicts work-life conflict and stress, and that these mediate turnover intention.

The problem is selection, and it is severe. Workers with the least schedule stability are disproportionately those with the least labor-market leverage, the shortest tenure, the lowest hours, and the weakest attachment — all of which independently predict separation. Managers also assign schedules non-randomly: in Halpin's (2015) grocery ethnography, the "mock schedule" posted a week out was systematically revised, and the revisions fell hardest on the newest and least-favored clerks, who were also the ones already most likely to leave. This is reverse causation and confounding operating in the same direction. Every observational estimate in this literature is therefore an upper bound on the causal effect, and the studies' own authors generally say so.

The experimental evidence is thinner and less favorable to a strong turnover story. The Gap Inc. stable scheduling trial (Williams et al. 2018; Kesavan et al. 2022) randomized twenty-eight stores to a bundle including two-weeks' notice, elimination of on-call, a shift-swapping application, targeted core hours, and — importantly — an additional soft-staffing budget. Its headline findings are about sales and productivity, not retention. Turnover effects were measured but were not the study's identified outcome, and the trial ran roughly ten months, which is short relative to grocery front-end tenure distributions and short relative to the time it takes a retention effect to show up in a separation rate.

The ordinance evaluations sit between these. Harknett, Schneider, and Irwin (2021), evaluating Seattle's Secure Scheduling Ordinance with a difference-in-differences design against comparison metropolitan areas, find that the ordinance did what it was designed to do on the input side — advance notice improved, on-call scheduling fell — and produced detectable improvements in sleep quality and subjective well-being. It did not produce a clearly detectable reduction in turnover. Evaluations of the second West Coast ordinance regime report a similar pattern: process compliance improved, worker-reported outcomes improved modestly, and effects on separations and hours were mixed or null (see also Wolfe, Jones, and Cooper 2018 for the coverage estimates; Economic Policy Institute, advocacy-affiliated).

So the three strata disagree, and they disagree in a legible way. Observational studies with the largest samples and the richest exposure measures produce the largest turnover associations and the weakest identification. Quasi-experimental studies with credible identification produce small or null turnover effects. The single well-identified experiment did not power itself for turnover.

Three further considerations bear on how a grocery chain should read this.

*Compliance and dose.* Ordinance evaluations estimate an intention-to-treat effect on all covered employers, many of whom were already at or near compliance before enactment, and some of whom complied only partially. Harknett, Schneider, and Irwin (2021) are explicit that the treated population's pre-period notice was better than the national average. A firm moving from genuinely volatile scheduling to genuine two-week notice is receiving a much larger dose than the average covered employer in an ordinance study. This argues that ordinance nulls understate what a committed single-firm implementation could achieve — but it is an argument from mechanism, not from evidence.

*Which turnover.* Choper, Schneider, and Harknett (2022) distinguish voluntary quits from involuntary separations, and scheduling exposure predicts the former far more strongly. Pinal Ridge's 87 percent figure, as Deschamps-Iyer's extract shows, does not currently separate these. If a material share is involuntary — no-call/no-show terminations, availability-conflict terminations, seasonal releases — the addressable share of the 87 percent is smaller than the headline, and the intervention's turnover return scales down proportionally. This is the single most important internal data question before the January meeting.

*Turnover is not uniformly costly.* Ton and Huckman (2008), studying a large bookstore chain, find that the performance cost of turnover is heavily moderated by process conformance: where operating procedures are well-standardized and adhered to, turnover damages performance far less. Grocery front-end work is comparatively standardized. The corollary is uncomfortable for the proposal: a $2,100 replacement cost may capture recruiting, onboarding, and training expense while missing or overstating the productivity loss, and in a well-standardized front end the productivity loss may be genuinely small. The corollary in the other direction is that Pinal Ridge's $2,100 figure, if it is a fully-loaded estimate including lost productivity, may be conservative for departments where conformance is lower — service deli, bakery, floral.

### 3.2 Sales and productivity: one strong finding, poorly generalizable

The 7 percent sales increase that circulates in trade coverage comes from a single source: the Gap Inc. trial (Williams et al. 2018; Kesavan et al. 2022, *Management Science*). The finding is real, well-executed, and published in a top operations journal. Treated stores showed roughly 7 percent higher sales and roughly 5 percent higher labor productivity than controls. It is also the most over-generalized result in this literature, for four reasons.

*It is one firm, one sector, twenty-eight stores.* The confidence interval around a store-randomized estimate with n=28 is wide. The point estimate is what gets quoted; the interval is what should be planned against.

*The treatment included added labor, not only reallocated labor.* Kesavan et al. (2022) are transparent that the intervention added soft-staffing hours in treated stores. A sales increase from a bundle that includes more selling labor is partly a test of a staffing-level hypothesis, not purely a scheduling-stability hypothesis. This is not a criticism of the study, which was designed as a bundle test; it is a criticism of citing the study as evidence that notice alone lifts sales.

*Apparel converts labor into sales differently than grocery does.* The retail-operations literature — Fisher, Krishnan, and Netessine (2006), Perdikaki, Kesavan, and Swaminathan (2012), Kesavan, Staats, and Gilland (2014) — establishes that additional store labor raises sales through assisted selling, conversion of browsing traffic, and reduced stockouts. In specialty apparel, conversion is highly labor-elastic: a knowledgeable associate materially changes basket size. In grocery, the majority of the basket is pre-planned before the customer enters the store. Front-end labor affects queue length, cart abandonment, and shrink, not conversion of browsers into buyers. The mechanism that produced the Gap result is weaker in grocery, and the honest expectation is a smaller effect, possibly much smaller.

*The productivity finding may be the more transferable one.* The 5 percent labor-productivity gain — sales per labor hour — arises from reduced turnover-driven inexperience, fewer coverage scrambles, and less manager time spent rebuilding schedules. Those mechanisms are sector-general. Ton (2014, 2023) makes the operational case at length across grocery cases (Mercadona, Trader Joe's, QuikTrip): scheduling stability is one element of a system that includes cross-training, operational slack, and SKU discipline, and it is the system rather than any component that produces the productivity return. The implication is that a scheduling-only pilot may capture less of the productivity gain than the Gap trial did, because the Gap trial ran inside a firm that simultaneously changed staffing levels.

Against the Gap result stands the near-absence of corroboration. No other included field experiment reports a sales effect of comparable magnitude, and several report no detectable sales effect at all. The administrative-data studies, which have the statistical power to detect small sales effects, generally lack exogenous variation in scheduling practice and therefore cannot separate a sales effect from the store-quality characteristics that also drive scheduling practice. The literature is, in short, one strong positive result and a large amount of silence.

### 3.3 Cost: estimates differ by an order of magnitude, and the reason is definitional

The extraction file contains cost estimates for predictable-scheduling implementation ranging from under 0.5 percent of covered payroll to over 5 percent. This is a tenfold spread, and it is almost entirely explained by what each estimate counts.

The low estimates count only incremental paid hours arising from reduced flexibility — the cost of staffing to a fixed schedule rather than to realized demand. These estimates are typically produced from firm payroll data and are the ones most consistent with the ordinance evaluations, which generally find no large payroll shock in covered establishments.

The high estimates count, in addition: predictability pay for schedule changes, which applies only in ordinance jurisdictions and would not apply to a voluntary pilot; incremental overtime arising from an inability to send workers home; incremental headcount to cover absence without on-call backfill; manager training and scheduling-system investment; and, in the most expansive versions, the opportunity cost of forgone labor-hour reductions during demand troughs.

For Pinal Ridge, the definitional question is therefore first-order and should be resolved before the January meeting. Bhatt's $1.9 million figure needs three clarifications on the record: whether it is chain-wide or pilot-scope; whether it is a run-rate steady-state figure or includes one-time systems and training investment; and whether it assumes staffing to peak, staffing to mean, or staffing to a guaranteed core with a flexible top layer. These three choices plausibly move the number by a factor of three.

Two structural observations from the literature bear on the cost estimate.

*Guaranteed core hours is the expensive component; notice is the cheap one.* Advance notice is primarily an information-discipline change: it requires forecasting demand fourteen days out rather than five, and it requires managers to stop revising posted schedules. Fugiel and Lambert (2019) and Lambert (2008) both characterize short-notice scheduling as a risk-transfer practice rather than a cost-minimizing one — the firm is not saving money so much as moving variance onto workers. If that characterization is right for Pinal Ridge, the notice component may cost very little in incremental payroll while producing a large share of the worker-outcome benefit. Guaranteed core hours, by contrast, is a genuine cost commitment: it converts a variable cost into a fixed one. Eliminating on-call sits in between; its cost depends entirely on how on-call is currently used, which is an internal data question.

*Cost falls with implementation maturity.* The qualitative and manager-interview studies consistently report a first-quarter cost spike that recedes. Managers initially over-staff the guaranteed core because they do not trust the forecast, then calibrate. Any pilot evaluated on a single quarter will overstate steady-state cost. The extraction file's cost estimates that come from year-one ordinance implementation should be read with this in mind.

### 3.4 Worker outcomes: the most consistent findings in the literature, and the least monetized

If the board's question were "does schedule instability harm workers," the literature would answer it decisively. Schneider and Harknett (2019), in the largest and most-cited study in this corpus, find routine schedule instability associated with psychological distress, poor sleep quality, and unhappiness, at magnitudes comparable to or exceeding those associated with sizeable wage differences. Harknett, Schneider, and Wolfe (2020) isolate the sleep pathway. Schneider and Harknett (2021) link instability to material hardship — food insufficiency, difficulty paying bills, housing insecurity — through the income-volatility channel rather than the income-level channel. Ananat and Gassman-Pines (2021), using daily diary data from working parents, find that schedule shocks affect parental mood and child behavior on the same day, which is the cleanest within-person identification in the corpus. Harknett, Schneider, and Luhr (2022) and Luhr, Schneider, and Harknett (2022) trace the effects into child care arrangement stability and parental strain. Storer, Schneider, and Harknett (2020) document that exposure is unequally distributed by race and ethnicity within the same firms and occupations.

Crucially, the ordinance evaluations — the best-identified studies in the corpus — corroborate this strand where they contradict the turnover strand. Harknett, Schneider, and Irwin (2021) find the Seattle ordinance improved sleep quality and subjective well-being even where it did not move turnover or hours. This is a coherent pattern, not a contradiction: the intervention delivered real benefits to workers that did not translate into measurable changes in employer-relevant outcomes over the study horizon.

The willingness-to-pay literature quantifies the worker-side value independently. Mas and Pallais (2017), using a randomized discrete-choice design embedded in an actual hiring process, find workers on average willing to forgo roughly a fifth of wages to avoid a schedule set by the employer on short notice — a very large valuation, and one derived from revealed rather than stated preference. Chen et al. (2019) find comparably large valuations of schedule control among platform drivers. These studies establish that schedule predictability is a substantial non-wage benefit. What they do not establish is that providing it recovers its cost through the labor market, because the labor market for grocery front-end work may not price non-wage amenities efficiently — an assumption the compensating-differentials framework requires and that the search-frictions literature (Dube, Lester, and Reich 2016) gives reason to doubt.

The practical consequence for Pinal Ridge is that the worker-outcome benefits are the best-supported effects in the entire literature and the ones least likely to appear in Bhatt's model. If the board wants them counted, they must be counted deliberately, either as an explicit non-financial objective or through a stated mechanism — reduced absenteeism, reduced workers' compensation incidence, reduced shrink — that connects them to the P&L. The literature does not supply that connection reliably.

### 3.5 Employer adaptation: the hours-reduction concern

Several included studies report that employers responding to scheduling constraints reduce total hours. This is the most important adverse finding in the corpus, because it implies the intervention could reduce worker earnings even as it improves worker schedules — the outcome least acceptable to both Marchbanks and the board.

The evidence is real but weaker than it is often presented. It comes from three sources of unequal quality.

The strongest source is the analogy to minimum-wage hours effects. Jardim et al. (2018), studying Seattle's minimum wage with administrative payroll records, find employer responses on the hours margin. This is not a scheduling study, but it establishes that firms facing an increase in the effective price of low-wage labor in a specific jurisdiction do adjust hours, and that studies looking only at headcount will miss it. Any evaluation of Pinal Ridge's pilot should therefore measure total hours and average hours per employee, not only headcount and separations.

The second source is worker survey reports within ordinance evaluations. These are mixed. Harknett, Schneider, and Irwin (2021) do not find a reduction in hours attributable to the Seattle ordinance. Other evaluations report worker-reported hour reductions that are not confirmed in administrative data. Worker reports of hour reductions are subject to a known confound: when on-call and last-minute add-on shifts are eliminated, some workers experience the loss of those hours as a cut even when scheduled hours are unchanged or higher. Distinguishing these requires administrative payroll data, which most ordinance evaluations lacked.

The third source is qualitative manager-interview evidence, which is directionally consistent and mechanistically informative. Alexander and Haley-Lock (2015) describe "underwork" — chronic under-provision of hours to part-time workers — as an existing equilibrium in retail independent of any scheduling regulation. Halpin (2015) documents grocery managers using hours allocation as a discipline and reward mechanism. Both suggest that the hours margin is already the manager's primary adjustment tool. Constraining the timing of hours without addressing their quantity may simply redirect adjustment to quantity.

This yields a concrete design implication rather than an argument against the pilot: a guaranteed weekly core of hours is precisely the design feature that blocks the hours-reduction response. Marchbanks's bundle already contains the mitigation. The pilot should be designed so that the core-hours guarantee is set at a level meaningfully above current average scheduled hours for part-time front-end staff, and the evaluation should treat "total hours delivered" as a co-primary outcome alongside turnover.

### 3.6 Sector heterogeneity: grocery is not apparel

Four differences make grocery a distinct case, and the literature addresses only some of them.

*Demand predictability.* Grocery demand is more forecastable than apparel demand. Weekly patterns are stable, holiday patterns are known, and weather effects are modelable. This cuts in favor of the pilot: the operational cost of committing to a schedule fourteen days out is a function of forecast error, and grocery forecast error is lower. Kesavan, Staats, and Gilland (2014) formalize the trade-off between volume flexibility and its costs; grocery sits on the favorable side.

*Perishability and departmental interdependence.* Grocery has hard operational constraints apparel lacks — receiving windows, code dates, temperature compliance. These reduce the manager's freedom to shift labor across the day and increase the cost of a coverage failure. This cuts against, modestly.

*Cross-training economics.* Ton (2014, 2023) identifies cross-training as the operational precondition that makes stable scheduling affordable: if a scheduled worker can be redeployed when their nominal department is slow, the guaranteed core costs little. Grocery front end is comparatively cross-trainable to stocking, cart retrieval, and self-checkout monitoring. This is probably the single largest lever on the pilot's actual cost, and it is not in Marchbanks's proposal.

*Labor-sales elasticity.* As argued in 3.2, grocery front-end labor affects throughput, queue abandonment, and shrink rather than conversion. Expected sales effects should be set well below the Gap estimate.

The literature contains almost no grocery-specific quantitative work. Halpin (2015) is the outstanding grocery study in the corpus and it is qualitative and now a decade old. This is the corpus's single largest external-validity problem for Pinal Ridge's purposes.

### 3.7 Why the studies disagree: a methodological accounting

Six differences explain most of the split.

**Treatment definition.** Studies that bundle notice, core hours, and staffing increases (Gap) find larger effects than studies of notice alone. Ordinance studies treat a heterogeneous population at heterogeneous doses.

**Identification strategy and the direction of its bias.** Observational studies overstate causal effects because of selection on worker attachment and manager assignment. Ordinance difference-in-differences understates them because of pre-period compliance, partial compliance, and spillover to comparison firms operating in the same labor market. The truth is bounded between the observational upper bound and the ordinance lower bound, which is a wide interval.

**Outcome measurement source.** Self-reported hours and self-reported turnover intention behave differently from administrative payroll and separation records. The corpus's largest effects are disproportionately in self-reported outcomes. The administrative-data stratum is more conservative throughout.

**Time horizon.** Field experiments run six to twelve months. Turnover effects in a workforce with median tenure under a year require longer to manifest in an annualized separation rate; cost effects shrink as managers calibrate. Short-horizon studies are biased toward finding cost and against finding retention benefit.

**Unit of analysis.** Store-randomized designs have small effective n and wide intervals. Worker-level designs have large n but confound worker and store effects. Firm-level studies cannot separate scheduling from everything else the firm changed.

**Sector and firm size.** Apparel dominates the experimental stratum; large national chains dominate the ordinance stratum. Mid-market regional chains — Pinal Ridge's category — are essentially unrepresented. Large chains have centralized workforce-management systems that make notice cheap to implement and staffing-model changes expensive; mid-market chains typically have the reverse cost structure.

---

## 4. Gaps

The following have not been studied adequately, and the board should know that the pilot would be generating evidence, not applying it.

**Grocery.** No field experiment in the corpus is in food retail. The sales-mechanism argument in Section 3.2 is theoretical extrapolation from apparel, not a grocery finding.

**Component decomposition.** No study isolates advance notice from guaranteed core hours from on-call elimination. Since these have very different cost profiles, the firm cannot currently know which component is buying which benefit. This is the most valuable thing the twelve-store pilot could be designed to learn.

**Mid-market firm size.** The corpus is bimodal — large chains and small-sample qualitative work. A 61-store chain with a single Phoenix office and presumably limited workforce-management technology is not represented.

**Voluntary firm adoption absent regulation.** All twenty-one quasi-experimental evaluations study mandated compliance. Voluntary adoption differs: implementation is more committed, manager buy-in is higher, and there is no predictability-pay penalty structure. The direction of the difference favors Pinal Ridge, but it is unstudied.

**Part-time workers with caregiving obligations.** This population appears almost exclusively in qualitative work (Henly, Shaefer, and Waxman 2006; Halpin 2015) and in the daily-diary and child-care studies (Ananat and Gassman-Pines 2021; Harknett, Schneider, and Luhr 2022). Given that 61 percent of Pinal Ridge's workforce is part time and that caregiving conflict is a plausible mechanism for the front-end turnover rate, the absence of quantitative retention estimates for this specific group is a serious gap. It also means the intervention's benefit may be highly concentrated in a subgroup, which a store-average evaluation will dilute.

**Manager time.** Every qualitative study mentions manager time spent rebuilding schedules; no quantitative study monetizes it. If store directors spend meaningful hours weekly on schedule churn, that is a real recoverable cost absent from every cost estimate in the corpus and, presumably, from Bhatt's.

**Long-run and equilibrium effects.** No study follows a firm beyond about two years. Wage effects, applicant-pool composition effects, and competitive responses by other employers in the same local labor market are unstudied.

**Interaction with wage level.** Dube, Lester, and Reich (2016) establish that separations respond to wages; no study tests whether schedule stability and wage increases are substitutes or complements in retention. If they are substitutes, the pilot's return depends on where Pinal Ridge's wages sit relative to local competitors — an internal question Deschamps-Iyer can answer and the literature cannot.

---

## 5. Implications for Pinal Ridge Markets

**1. The turnover case is plausible but unproven, and the board should not underwrite the pilot on the observational estimates.** The largest turnover associations come from the least-identified designs. The best-identified designs find small or null turnover effects. A defensible planning assumption is a turnover reduction well below what Choper, Schneider, and Harknett (2022) imply — and the pilot's purpose should be to measure it, not to assume it.

**2. The arithmetic of what the pilot must achieve is worth stating plainly.** At $2,100 per replacement, $1.9 million a year is equivalent to 905 avoided separations chain-wide. Scaled to twelve of sixty-one stores, roughly $374,000 and roughly 178 avoided separations. Whether 178 avoided separations across twelve stores is ambitious depends on the front-end clerk headcount in those stores, which Deschamps-Iyer should supply before January. If the twelve pilot stores employ, say, 400 front-end clerks turning over at 87 percent, that is about 348 separations a year, and breaking even on turnover alone requires roughly halving turnover. That is well outside anything the literature supports. If breakeven on turnover alone requires more than a 20 to 25 percent reduction in separations, the pilot cannot be justified on retention grounds and must be justified on a combination of retention, productivity, sales, and strategic objectives.

**3. The sales channel is a real but secondary contributor, and the required lift is small.** Spread across 61 stores, $1.9 million is roughly $31,000 per store per year. Against a store doing on the order of $20 million annually, that is about 0.16 percent of sales; at a 25 percent gross margin, breakeven on gross margin alone requires a sales lift of roughly 0.6 percent. That is an order of magnitude below the Gap trial's 7 percent. The board should not expect the Gap effect in grocery — but it should recognize that the pilot does not need anything close to it. Store-level revenue figures should be substituted for this illustration before the meeting.

**4. Decompose the bundle in the pilot design.** This is the highest-value recommendation in this review. A twelve-store pilot has enough stores to support a factorial or staggered design: four stores receiving advance notice only, four receiving notice plus on-call elimination, four receiving the full bundle including guaranteed core hours, with matched comparison stores. The literature cannot tell Pinal Ridge which component earns its keep. A well-designed pilot can, and the answer is worth more to a 61-store rollout decision than a single-arm result would be.

**5. Guarantee core hours at a level above current part-time averages, and measure total hours as a primary outcome.** The hours-reduction risk is the corpus's most credible adverse finding, and the core-hours guarantee is the design feature that blocks it. If the guarantee is set at or below current averages, it is non-binding and the pilot tests nothing.

**6. Invest in cross-training concurrently or accept a higher cost.** The Ton (2014, 2023) line of work is consistent that stable scheduling is affordable only inside an operating system that lets committed labor be redeployed. Cross-training front-end staff to stocking and self-checkout support is the mechanism that converts a fixed hours commitment into flexible capacity. Omitting it is the most likely way for Bhatt's $1.9 million to prove an underestimate.

**7. Resolve four internal data questions before January.** The split between voluntary and involuntary separations in the 87 percent. The share of separations occurring within 90 days of hire, which indicates whether the problem is scheduling or selection. Current advance notice and on-call incidence by store, which determines the dose the pilot would actually deliver. And current front-end wages relative to competitors within each trade area, which determines whether scheduling or pay is the binding constraint.

**8. Run the pilot for at least eighteen months and report separately on the first two quarters.** The literature is clear that cost peaks early and retention effects emerge late. A twelve-month evaluation is structurally biased toward a negative finding.

**9. Count the worker outcomes explicitly or decide not to.** The best-supported effects in this entire literature are on sleep, distress, material hardship, and child-care stability. They are real, they are large, and they will not appear in the financial model. The board should make a deliberate choice about whether they count toward the decision, rather than allowing them to be excluded by default through the mechanics of a capital-approval process.

---

## 6. References

Alexander, C., & Haley-Lock, A. (2015). Underwork, work-hour insecurity, and a new approach to wage and hour regulation. *Industrial Relations*, 54(4), 695–716.

Ananat, E. O., & Gassman-Pines, A. (2021). Work schedule unpredictability: Daily occurrence and effects on working parents' well-being. *Journal of Marriage and Family*, 83(1), 10–26.

Boushey, H., & Ansel, B. (2016). *Working by the hour: The economic consequences of unpredictable scheduling practices*. Washington Center for Equitable Growth. [Advocacy-affiliated.]

Carré, F., & Tilly, C. (2017). *Where bad jobs are better: Retail jobs across countries and companies*. Russell Sage Foundation.

Chen, M. K., Chevalier, J. A., Rossi, P. E., & Oehlsen, E. (2019). The value of flexible work: Evidence from Uber drivers. *Journal of Political Economy*, 127(6), 2735–2794.

Choper, J., Schneider, D., & Harknett, K. (2022). Uncertain time: Precarious schedules and job turnover in the US service sector. *ILR Review*, 75(5), 1099–1132.

Dube, A., Lester, T. W., & Reich, M. (2016). Minimum wage shocks, employment flows, and labor market frictions. *Journal of Labor Economics*, 34(3), 663–704.

Fisher, M. L., Krishnan, J., & Netessine, S. (2006). *Retail store execution: An empirical study*. Working paper, The Wharton School.

Fugiel, P. J., & Lambert, S. J. (2019). On-call and on-schedule: Employer-driven variable work scheduling. *RSF: The Russell Sage Foundation Journal of the Social Sciences*, 5(4), 111–126.

Golden, L. (2015). *Irregular work scheduling and its consequences*. Economic Policy Institute Briefing Paper No. 394. [Advocacy-affiliated.]

Halpin, B. W. (2015). Subject to change without notice: Mock schedules and labor control in the grocery industry. *Social Problems*, 62(3), 419–438.

Harknett, K., Schneider, D., & Irwin, V. (2021). Improving health and economic security by reducing work schedule uncertainty. *Proceedings of the National Academy of Sciences*, 118(42).

Harknett, K., Schneider, D., & Luhr, S. (2022). Who cares if parents have unpredictable work schedules? Just-in-time work schedules and child care arrangements. *Social Problems*, 69(1), 164–183.

Harknett, K., Schneider, D., & Wolfe, R. (2020). Losing sleep over work scheduling? The relationship between work schedules and sleep quality among service sector workers. *SSM–Population Health*, 12, 100681.

Henly, J. R., & Lambert, S. J. (2014). Unpredictable work timing in retail jobs: Implications for employee work-life conflict. *ILR Review*, 67(3), 986–1016.

Henly, J. R., Shaefer, H. L., & Waxman, E. (2006). Nonstandard work schedules: Employer- and employee-driven flexibility in retail jobs. *Social Service Review*, 80(4), 609–634.

Ikeler, P. (2016). *Hard sell: Work and resistance in retail chains*. ILR Press.

Jardim, E., Long, M. C., Plotnick, R., van Inwegen, E., Vigdor, J., & Wething, H. (2018). *Minimum wage increases, wages, and low-wage employment: Evidence from Seattle*. NBER Working Paper No. 23532.

Kesavan, S., Lambert, S. J., Williams, J. C., & Pendem, P. K. (2022). Doing well by doing good: Improving retail store performance with responsible scheduling practices at the Gap, Inc. *Management Science*, 68(11), 7818–7836.

Kesavan, S., Staats, B. R., & Gilland, W. (2014). Volume flexibility in services: The costs and benefits of flexible labor resources. *Management Science*, 60(8), 1884–1906.

Lambert, S. J. (2008). Passing the buck: Labor flexibility practices that transfer risk onto hourly workers. *Human Relations*, 61(9), 1203–1227.

Lambert, S. J., Fugiel, P. J., & Henly, J. R. (2014). *Precarious work schedules among early-career employees in the US: A national snapshot*. Employment Instability, Family Well-being, and Social Policy Network, University of Chicago.

Lambert, S. J., Henly, J. R., & Kim, J. (2019). Precarious work schedules as a source of economic insecurity and institutional distrust. *RSF: The Russell Sage Foundation Journal of the Social Sciences*, 5(4), 218–257.

Luhr, S., Schneider, D., & Harknett, K. (2022). Parenting without predictability: Precarious schedules, parental strain, and work-life conflict. *RSF: The Russell Sage Foundation Journal of the Social Sciences*, 8(5), 45–65.

Mas, A., & Pallais, A. (2017). Valuing alternative work arrangements. *American Economic Review*, 107(12), 3722–3759.

Perdikaki, O., Kesavan, S., & Swaminathan, J. M. (2012). Effect of traffic on sales and conversion rates of retail stores. *Manufacturing & Service Operations Management*, 14(1), 145–162.

Schneider, D., & Harknett, K. (2019). Consequences of routine work-schedule instability for worker health and well-being. *American Sociological Review*, 84(1), 82–114.

Schneider, D., & Harknett, K. (2021). Hard times: Routine schedule unpredictability and material hardship among service sector workers. *Social Forces*, 99(4), 1682–1709.

Storer, A., Schneider, D., & Harknett, K. (2020). What explains race/ethnic inequality in job quality in the service sector? *American Sociological Review*, 85(4), 537–572.

Ton, Z. (2014). *The good jobs strategy: How the smartest companies invest in employees to lower costs and boost profits*. New Harvest.

Ton, Z. (2023). *The case for good jobs: How great companies bring dignity, pay, and meaning to everyone's work*. Harvard Business Review Press.

Ton, Z., & Huckman, R. S. (2008). Managing the impact of employee turnover on performance: The role of process conformance. *Organization Science*, 19(1), 56–68.

Williams, J. C., Lambert, S. J., Kesavan, S., Fugiel, P. J., Ospina, L. A., Rapoport, E. D., Jarpe, M., Bellisle, D., Pendem, P., McCorkell, L., & Adler-Milstein, S. (2018). *Stable scheduling study: Health outcomes report*. Center for WorkLife Law, University of California, Hastings.

Wolfe, J., Jones, J., & Cooper, D. (2018). *"Fair workweek" laws help more than 1.8 million workers*. Economic Policy Institute. [Advocacy-affiliated.]

**Internal documents**

Bhatt, P. (2026). *Predictable scheduling pilot: preliminary labor cost model*. Pinal Ridge Markets, Office of the CFO.

Deschamps-Iyer, C. (2026). *Front-end separation, tenure, and scheduling practice extract, FY2024–FY2026*. Pinal Ridge Markets.

Marchbanks, D. (2026). *Twelve-store predictable scheduling pilot: proposal*. Pinal Ridge Markets, Office of the Chief People Officer.

*Full extraction file — effect sizes, confidence intervals, outcome definitions, design codes, and firm-size codes for all fifty-nine included studies — available on request from the analyst of record.*
