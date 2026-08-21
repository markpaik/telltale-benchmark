# Public Interest Technology Fund — Application Narrative

**Applicant:** Sunflower Civic Code, Inc.
**Location:** Lawrence, Kansas
**Request:** $3,100,000 over three years
**Submission Deadline:** April 24
**Primary Contact:** Priscilla Ojeda, Executive Director
**Fiscal Contact:** Hannah Steinmetz, Finance Director

---

## Statement of Need

In the four states where Sunflower Civic Code operates, the distance between a household's legal eligibility for public benefits and that household's actual receipt of those benefits is measured in hours of unpaid administrative labor, in miles driven to county offices with limited hours, and in forms written at a reading level that assumes a stability the applicant does not have. That distance is the problem this organization was built to close, and the three years ahead present a version of it more acute than any we have faced since incorporation.

The unwinding of continuous Medicaid enrollment has moved renewal from a background administrative event to the single largest driver of coverage loss in the region. Kansas, Missouri, Nebraska, and Oklahoma each process renewals on different cadences, through different portals, with different documentation standards and different tolerance for incomplete submissions. A household that moved once during the pandemic, or whose wage income fluctuates across a seasonal agricultural or meatpacking calendar, faces a renewal packet that presumes a fixed address and a steady paycheck. Procedural terminations — coverage lost not because a household became ineligible but because paperwork failed — have accounted for the majority of disenrollments in every state we serve. SNAP recertification produces the same pattern on a shorter interval, with the added complication that a missed interview appointment can restart the entire process.

Our screening data describes who is absorbing this burden. Last year we ran 218,000 screenings. The median household income of users was $27,400. Sixty-one percent of screenings were completed on a mobile phone, a figure that has risen in each of the last three years and that shapes every design decision we make: a tool that assumes a desktop browser, a scanner, and a printer is a tool built for someone else. Users who begin a screening on a phone in a parking lot outside a county office, or during a break at work, do not return to a saved session on a laptop that evening. They finish or they abandon.

The court-date side of our work addresses a parallel failure. A missed hearing is rarely a decision. It is a calendar problem, a transportation problem, a childcare problem, or a notice that arrived at an address the person left four months ago. The consequences are disproportionate to the cause: bench warrants, default judgments, license suspensions, and in eviction and debt collection dockets, the permanent loss of a defense that would have succeeded. Across 14,000 hearings in three pilot counties, our reminder tool reduced failure-to-appear from 22 percent to 9 percent. We report that figure with a precision we have earned the hard way, and we discuss its methodology candidly in the Evaluation Plan below.

The institutional need is as real as the household need. We currently serve 46 county agencies and seven legal aid organizations. County IT budgets in the rural counties of our region are frequently under $100,000 annually, inclusive of hardware refresh. Vendor procurement for benefits screening software carries per-seat licensing that these counties cannot absorb, and the products on offer are built for state-level deployment, not for a three-person eligibility office serving 9,000 residents. Legal aid organizations face the same arithmetic with less staff. Open-source tooling, maintained by an organization accountable to the agencies using it rather than to a licensing model, is not an ideological preference in this market. It is the only economically available option.

Language access compounds every barrier described above. The populations most affected by benefits churn in our region include substantial Spanish-speaking communities across southwest Kansas and central Nebraska, and Vietnamese-speaking communities concentrated in the Kansas City and Oklahoma City metropolitan areas and in Gulf-adjacent processing employment that draws seasonal migration northward. Our tools are currently English-only. Every screening we do not run in Spanish or Vietnamese is a household we have identified as needing help and then declined to help.

Thirty counties in our four-state region have requested access to our screening tools and have not received it, because we do not currently have the onboarding capacity, the multilingual coverage, or the renewal-specific logic to serve them responsibly. That gap — thirty counties, two languages, two benefit programs restructured around renewal rather than initial application — is the shape of this proposal.

---

## Project Description

We propose a three-year program with four integrated components: a rebuilt screening engine oriented to Medicaid renewal and SNAP recertification, multilingual expansion into Spanish and Vietnamese, onboarding of thirty additional county agencies, and the establishment of a paid support tier that converts a portion of our institutional users into recurring revenue.

### Component One: Rebuilding the Screener for Renewal and Recertification

Our existing screener was architected around a single question: does this household appear eligible for a program it is not currently receiving? Renewal and recertification invert that question. The relevant inquiry becomes: what has changed since the last determination, what documentation does this state require to substantiate that change, and what is the deadline?

The rebuild replaces our monolithic eligibility rules engine with a modular rules service in which each state-program pair is a versioned, independently deployable ruleset. This matters operationally because our current architecture requires a full release cycle to accommodate a single state's policy change, and policy changes in this domain arrive with two weeks' notice and no changelog. Under the new architecture, a Kansas SNAP income-disregard adjustment can be authored, tested against a fixture corpus, and deployed without touching Missouri Medicaid logic.

The renewal workflow introduces a persistent household record — with explicit, revocable user consent and a default retention window of 18 months — that allows a returning user to confirm or amend prior answers rather than re-enter them. For a household completing an annual Medicaid renewal and a semiannual SNAP recertification, this reduces a 40-question flow to a 9-question delta confirmation in the common case. We estimate from session analytics that abandonment concentrates between questions 12 and 19 of the current flow; shortening the return path is the single highest-leverage change available to us.

Mobile-first is a constraint, not a feature. The rebuild targets a sub-two-second time-to-interactive on a mid-tier Android device over a 3G connection, offline-tolerant form state, and document capture through the phone camera with client-side image optimization before upload. Sixty-one percent of our traffic requires this; we expect that figure to exceed 70 percent within the grant period.

We will also build a deadline and document tracker that issues renewal reminders on the same delivery infrastructure as our court-date reminders. The infrastructure exists and is proven. Extending it from hearings to renewal deadlines is a modest engineering lift with a substantial expected effect, given that the failure mode in both cases is identical: a date passed and no one was told in a way they could act on.

### Component Two: Spanish and Vietnamese

We are not commissioning translations. We are building a localization pipeline, and the distinction is the whole project.

Benefits screening language is legally consequential. A mistranslated question about household composition produces a wrong eligibility determination, and a wrong determination delivered confidently is worse than no determination at all. Our approach: professional translation by translators with demonstrated public-benefits domain experience; back-translation review by a second independent translator; plain-language review at a target of sixth-grade reading level in each language; and cognitive interviewing with 12–15 native speakers per language, conducted in partnership with our legal aid partner, in which participants complete a screening while narrating their interpretation of each question.

The pipeline itself — extraction of translatable strings, versioning of translations against source changes, and flagging of stale translations when source text changes — is the durable asset. Adding a fourth language after this grant should cost translation and testing, not re-engineering. We will publish the pipeline and the reviewed string corpora under the same open license as the rest of our codebase, so that other civic technology organizations serving the same populations are not required to repeat this work.

### Component Three: Thirty Additional Counties

Our current onboarding process is artisanal: a member of our team spends roughly 40 hours per county on configuration, staff training, and data-sharing agreement negotiation. At that rate, thirty counties consumes 1,200 staff hours and is the binding constraint on our growth.

We will productize onboarding into a self-service configuration console, a standardized data-sharing agreement template pre-reviewed against each of the four states' statutory frameworks, a recorded training curriculum with a live office-hours supplement, and a 30-day guided implementation checklist. Target: 16 staff hours per county, a 60 percent reduction.

Sequencing is deliberate. Year one: eight counties, drawn from Kansas and Missouri where our data-sharing precedents are strongest, functioning as the proving ground for the new onboarding process. Year two: twelve counties, including the first Spanish-language deployments in southwest Kansas and central Nebraska. Year three: ten counties, including Vietnamese-language deployments in the Kansas City and Oklahoma City metropolitan areas and Oklahoma expansion.

We address the Nebraska situation directly. In February, the Nebraska Department of Health and Human Services withdrew from a planned pilot. The withdrawal followed a change in the department's internal data governance posture regarding third-party access to eligibility-adjacent data, and applies to a category of external integration rather than to our organization specifically. We were told this in writing and we have no reason to characterize it otherwise. It was nonetheless a material setback: it removed a state-level channel we had expected to accelerate county recruitment in Nebraska, and we should have identified the shifting governance posture earlier than we did.

Our response has been to decouple Nebraska county deployment from state-level participation. Our screening tool does not require state data integration to function; it requires accurate rules and a county willing to route residents to it. Four Nebraska counties have indicated interest in proceeding independently, and two have begun preliminary conversations with their county attorneys. We have built our Nebraska targets in this proposal on county-level commitments only. If the state department revisits its position, that is upside we have not counted. We would rather present the committee with a plan that survives the state saying no permanently than a plan that requires the state to say yes.

### Component Four: The Paid Support Tier

Described in full under Sustainability. In brief: a tiered annual support subscription offering guaranteed response times, priority configuration assistance, custom reporting, and integration support, offered to county agencies and legal aid organizations while all software remains free and open source. The tier sells service, not access. No county loses functionality by declining to subscribe.

---

## Goals and Measurable Objectives

Objectives below are stated in the reporting units the Foundation has specified: counties onboarded, screenings completed, applications submitted and approved, uptime, failure-to-appear rate, and cost per screening.

**Goal 1: Expand access to benefits screening across the four-state region.**

| Objective | Year 1 | Year 2 | Year 3 | Cumulative |
|---|---|---|---|---|
| 1.1 New county agencies onboarded | 8 | 12 | 10 | 30 |
| 1.2 Total county agencies served | 54 | 66 | 76 | 76 |
| 1.3 Legal aid organizations served | 9 | 11 | 12 | 12 |
| 1.4 Screenings completed (annual) | 265,000 | 340,000 | 425,000 | 1,030,000 |
| 1.5 Screenings in Spanish or Vietnamese | 6,000 | 42,000 | 85,000 | 133,000 |
| 1.6 Share of screenings on mobile | ≥63% | ≥66% | ≥70% | — |

**Goal 2: Convert screenings into completed applications and approved benefits.**

| Objective | Year 1 | Year 2 | Year 3 | Cumulative |
|---|---|---|---|---|
| 2.1 Applications submitted (verified) | 41,000 | 58,000 | 76,000 | 175,000 |
| 2.2 Applications approved (verified) | 28,000 | 41,000 | 55,000 | 124,000 |
| 2.3 Approval rate among verified submissions | ≥68% | ≥70% | ≥72% | — |
| 2.4 Medicaid renewals completed on time | 9,000 | 19,000 | 29,000 | 57,000 |
| 2.5 SNAP recertifications completed on time | 7,000 | 16,000 | 25,000 | 48,000 |

Objectives 2.1 and 2.2 are stated as *verified* counts because they depend on data-sharing agreements permitting outcome confirmation. We currently hold such agreements with 19 of 46 counties. Verified counts therefore understate true totals. Expanding outcome-verification agreements to 45 of 76 counties by year three is itself an objective (2.6), and we will report both verified counts and modeled estimates with the verification denominator stated explicitly. We will not blend them.

**Goal 3: Reduce failure-to-appear through hearing reminders.**

| Objective | Year 1 | Year 2 | Year 3 | Cumulative |
|---|---|---|---|---|
| 3.1 Counties with reminder deployment | 7 | 14 | 22 | 22 |
| 3.2 Hearings covered (annual) | 34,000 | 71,000 | 112,000 | 217,000 |
| 3.3 Failure-to-appear rate, covered hearings | ≤13% | ≤12% | ≤11% | — |
| 3.4 Reminder delivery confirmation rate | ≥88% | ≥90% | ≥91% | — |

We deliberately set 3.3 above the 9 percent observed in our three pilot counties. Those counties were early adopters with engaged court administrators, clean docket data, and a favorable baseline of 22 percent. Scaling to 22 counties will encompass jurisdictions with worse contact data, higher-volume dockets, and less administrative engagement. Projecting 9 percent across that population would be an overreach. We would rather commit to 11 percent and exceed it.

**Goal 4: Achieve platform reliability appropriate to a benefits-critical service.**

| Objective | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| 4.1 Screening platform uptime | ≥99.5% | ≥99.7% | ≥99.9% |
| 4.2 Reminder delivery pipeline uptime | ≥99.7% | ≥99.9% | ≥99.9% |
| 4.3 Median time-to-interactive, mobile 3G | ≤3.0s | ≤2.4s | ≤2.0s |
| 4.4 P1 incident mean time to resolution | ≤4h | ≤3h | ≤2h |

Uptime is measured by third-party external synthetic monitoring from four geographic points, excluding announced maintenance windows, which will not exceed four hours quarterly and will be scheduled outside 7:00 a.m.–9:00 p.m. Central.

**Goal 5: Reduce cost per screening while expanding functionality.**

| Objective | Baseline | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| 5.1 Fully loaded cost per screening | $8.94 | $8.10 | $6.85 | $5.60 |
| 5.2 Marginal cost per screening | $1.42 | $1.30 | $1.10 | $0.95 |

Fully loaded cost divides total organizational expense by total screenings. It rises with investment and falls with volume, and we present it because the Foundation requires it. Marginal cost — infrastructure, delivery, and support attributable to an additional screening — is the better measure of operational efficiency, and we report both.

**Goal 6: Establish earned revenue sufficient to sustain core operations.**

| Objective | Baseline | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| 6.1 Annual earned revenue | $190,000 | $415,000 | $735,000 | $1,100,000 |
| 6.2 Support tier subscribers | 6 | 21 | 42 | 63 |
| 6.3 Subscriber renewal rate | — | ≥85% | ≥88% | ≥90% |

**Goal 7: Meet every reporting obligation on schedule.**

| Objective | Standard |
|---|---|
| 7.1 Foundation reports submitted by deadline | 100%, all three years |
| 7.2 Reported figures restated after submission | Zero |
| 7.3 Pre-submission data reconciliation completed | 100% of reports |

Goal 7 exists because of our history with this Foundation, addressed in full below.

---

## Evaluation Plan

### Governing Principle

Our evaluation design is shaped by a specific failure. In 2024, this Foundation declined to renew a $900,000 grant after we missed two reporting deadlines and restated outcome numbers we had previously submitted. The evaluation plan below is not a generic methodology section. It is the corrective architecture we built in response, and we ask the committee to read it as such.

### What Went Wrong and What We Changed

The restatement had a specific and unglamorous cause. Our outcome figures were assembled from three sources — platform session logs, county-reported application dispositions, and legal aid partner case records — reconciled manually in a spreadsheet by a program staff member as a quarterly task. Two errors compounded. First, a deduplication rule treated a household completing screenings for two programs as two distinct households in some counties and one in others, depending on when that county's integration was built. Second, county-reported approvals arriving after our reporting cutoff were sometimes retroactively included and sometimes not, without a documented rule. The result was an inflated and internally inconsistent count. When we discovered it during preparation of the subsequent report, we restated. The restatement was correct. That it was necessary was our failure.

The missed deadlines had an equally unglamorous cause: reporting was an uncompensated addition to the workload of a program staff member with no backup and no calendar authority, and it lost every scheduling contest against operational urgency.

Six changes followed, all implemented and operating for at least three reporting cycles:

**A single source of truth.** All outcome data now flows into one warehouse with defined ingestion schedules per source. Reports are generated by query against that warehouse. Manual spreadsheet assembly has been eliminated from the reporting path entirely.

**A written measurement dictionary.** Every reported metric has a documented definition, calculation method, data source, deduplication rule, inclusion window, and known limitation. It is versioned in our public repository. Any change requires Executive Director approval and is logged with its effective date. We are attaching the current version as Appendix C and invite the committee to hold us to it literally.

**A stated data cutoff.** All figures reflect data as of the last day of the reporting period. Late-arriving dispositions appear in the following period as a separately labeled prior-period adjustment line. They are never retroactively folded into a closed period.

**Named accountability.** The Finance Director owns report submission. Hannah Steinmetz's performance objectives include on-time submission as an explicit criterion. Report preparation begins 45 days before deadline against a documented schedule, with an internal draft due at 21 days and reconciliation review at 14 days.

**Independent reconciliation.** Before submission, a staff member not involved in preparation independently reconciles reported figures against warehouse queries and signs a reconciliation memo, filed with the report.

**Restatement protocol.** If we discover an error, we notify the funder within five business days of discovery, before the next scheduled report, with the magnitude, the cause, and the remediation. We will not let a funder learn of an error from a document we had the opportunity to correct first.

Since implementation, we have submitted 11 consecutive reports to seven funders on time with zero restatements. We recognize that a track record of this length is suggestive rather than conclusive, and we address the residual risk in Organizational Capacity.

### Evaluation Design

**Output monitoring** is continuous and automated. Counties onboarded, screenings, language distribution, device distribution, uptime, incident resolution, and reminder delivery confirmation are instrumented at the platform level and available on a dashboard we will provide the Foundation with read access to. We would rather the committee see our numbers continuously than quarterly.

**Outcome verification** operates through the data-sharing agreements described above. Where an agreement permits, county eligibility systems return disposition — submitted, approved, denied, pending — matched to screening sessions via a hashed identifier under a matching protocol reviewed by counsel. Where no agreement exists, we capture user-reported outcomes through a 45-day follow-up message, and we report those separately with response-rate denominators, never blended with verified counts.

**Failure-to-appear measurement** uses a design our university partner insisted on and we adopted. Our original pilot compared post-deployment failure-to-appear against a historical pre-deployment baseline in the same counties. That design cannot distinguish the reminder's effect from concurrent docket management changes, and our 22-to-9 figure inherits that limitation. We state this plainly.

For the grant period, we adopt a stepped-wedge design across the 15 new reminder counties. Counties enter deployment in randomized sequence across six waves. At any interval, deployed counties serve as treatment and not-yet-deployed counties as control, with each county eventually contributing to both. This yields defensible causal estimation without withholding an effective intervention from any jurisdiction permanently — a design constraint our judicial partner considered non-negotiable, correctly. The Ramona Chee policy center will hold the randomization sequence and conduct the analysis.

**Language access evaluation** compares completion rates, per-question abandonment, time-on-task, and eligibility-determination accuracy across language versions. Divergence beyond defined thresholds triggers cognitive interview review of the specific questions implicated. Accuracy is assessed against a legal aid–reviewed gold-standard case set of 60 scenarios per language.

**Cost analysis** is prepared by the Finance Director using activity-based allocation with a documented methodology in the measurement dictionary. Personnel costs are allocated by timesheet; infrastructure by usage telemetry; overhead by a documented rate.

### Partner Roles in Evaluation

Our **legal aid partner** conducts user testing across all four states, leads cognitive interviewing in Spanish and Vietnamese, maintains the gold-standard accuracy case set, and reviews eligibility logic changes before release. Their staff attorneys hold the authority to block a release they believe produces incorrect determinations, and have exercised it twice. Compensated at $118,000 over three years.

Our **state judicial office partner** supplies hearing data under an executed data-sharing agreement covering docket identifiers, hearing dates, appearance dispositions, and contact information, with quarterly reciprocal reporting on delivery and appearance rates. They review the stepped-wedge protocol and approve the county entry sequence. Uncompensated; their contribution is data access and administrative facilitation.

The **university policy center led by Ramona Chee** serves as independent evaluator. Chee's center holds the randomization sequence, conducts the failure-to-appear analysis, and produces an independent annual evaluation memo delivered simultaneously to us and to the Foundation. That simultaneity is deliberate and non-negotiable in our subaward: we do not want, and will not have, the ability to review an unfavorable independent finding before the Foundation sees it. Compensated at $246,000 over three years, with the subaward specifying methodological independence and publication rights regardless of findings.

---

## Organizational Capacity

### Organization

Sunflower Civic Code employs 24 staff against a $4.3 million annual budget. Composition: 11 engineering and product, 5 program and partnerships, 3 evaluation and data, 3 finance and operations, 2 executive. We serve 46 county agencies and 7 legal aid organizations across four states and processed 218,000 screenings last year at 99.4 percent uptime.

Priscilla Ojeda has served as Executive Director for six years, through the organization's growth from 6 staff to 24 and from single-state to four-state operation. Hannah Steinmetz has served as Finance Director for four years and led the reporting remediation described above. Our board comprises nine members including two former county human services administrators, a retired district court judge, a technology executive, and two individuals with lived experience of the benefits systems we serve.

### The Chief Technology Officer Vacancy

Our Chief Technology Officer departed in November. Zsofia Balogh has held the role on an interim basis since. We recognize that a permanent technical leadership vacancy is a legitimate concern for a funder evaluating a $3.1 million technical proposal, and we would rather address it in full than have the committee infer around it.

**Circumstances.** The departure was planned and amicable, arising from a relocation. We received nine weeks' notice. That notice period was used for structured transition: documentation review, architectural decision records, vendor and partner introductions, and a handover of the technical roadmap. The departing CTO remains available as a paid advisor and has provided approximately 30 hours since departure.

**Interim leadership.** Balogh is not a placeholder. She joined four years ago, has served as Director of Engineering for two, architected the reminder delivery pipeline that produced the failure-to-appear results cited throughout this proposal, and led the technical work for 22 of our 46 county integrations. She authored the technical appendix accompanying this application. During her interim tenure the platform has sustained 99.6 percent uptime — above our prior-year figure — and delivered two major releases on schedule. She has been granted full CTO authority including budget, hiring, and architectural decision rights.

**Search.** The board authorized a search in January. We are conducting it deliberately rather than quickly, for two reasons. First, we want a permanent CTO whose commitments align with the multi-year program described here rather than one hired under deadline pressure. Second, Balogh is a serious internal candidate, and we owe both her and the organization a process that evaluates her fairly against an external field rather than one that either forecloses or presumes her candidacy. The search committee comprises three board members, the Executive Director, and an external technical advisor. Our target is an offer accepted by the end of the third quarter of the calendar year — before this grant period would begin.

**If the search does not conclude on schedule**, Balogh continues in the interim role with full authority through at least the first year of the grant period. We have structured the program so that no year-one milestone depends on a new CTO's arrival. The rules-engine modularization and localization pipeline architecture are specified in the technical appendix, reviewed by our external technical advisory group, and executable by the current team. A new CTO would inherit a defined plan, not author one.

**Risk we accept.** A permanent hire arriving mid-program will want to revisit architectural decisions. That is appropriate and we have budgeted a 60-day orientation with explicit authority to propose changes to the board, and a contingency of $85,000 for architectural revision. We would rather budget for a new leader's judgment than pretend we have foreclosed it.

### Technical Capacity

Our platform serves 218,000 annual screenings across four states with per-state rules configuration, mobile-optimized delivery, and message delivery infrastructure spanning SMS, voice, and email. Our codebase is public, our infrastructure-as-code definitions are versioned, and our deployment pipeline includes automated testing against a fixture corpus of over 900 eligibility scenarios. We conduct annual third-party penetration testing and maintain a documented incident response protocol with defined severity tiers.

The technical appendix accompanying this application specifies the target architecture, migration sequence, data model changes for household persistence, the localization pipeline, security and privacy controls including our data retention and consent framework, and our accessibility conformance approach.

### Partnership Capacity

Our three principal partners hold executed or committed agreements. The legal aid organization has worked with us for five years across all four states. The state judicial office relationship is governed by a data-sharing agreement executed two years ago and renewed once. Ramona Chee's policy center has served as our independent evaluator for two years, including — and we note this deliberately — producing the methodological critique of our original failure-to-appear design that we have incorporated into this application.

### Honest Assessment of Capacity Risk

We identify three material risks and our mitigations.

**Reporting recurrence.** Our remediation is 11 reports old. It is not yet institutional memory. Mitigation: the reconciliation memo requirement is a hard gate on submission; the board Finance Committee reviews reporting compliance quarterly as a standing agenda item; and we commit to a voluntary mid-year reporting compliance check-in with Foundation staff in each grant year, at our initiative and our cost.

**Growth outpacing support capacity.** Growing from 46 to 76 counties while launching a paid support tier creates a real possibility that support quality degrades exactly when we are asking counties to pay for it. Mitigation: support staffing is front-loaded, with the first support engineer hired in month two of year one, before the first paid subscriber is onboarded; and we have set a hard rule that if support response times breach tier commitments for two consecutive months, county onboarding pauses until they recover. That rule is in our operating plan, and it will cost us onboarding velocity if invoked. We think it should.

**Nebraska.** Discussed above. Our targets assume no state-level participation.

---

## Sustainability

### The Question

The Foundation is being asked to fund a program whose annual operating cost will exceed $1.4 million by year three. The relevant question is not whether the program is valuable but whether it survives the grant. Our answer rests on earned revenue growing from $190,000 to $1,100,000 across three years, and Finance Director Hannah Steinmetz has prepared the following explanation of how that occurs.

### Current Earned Revenue: $190,000

Present earned revenue comprises three streams. Custom integration work for county agencies with non-standard systems generated $94,000 last year across five engagements. Six early-adopter counties pay informal annual support arrangements averaging $9,000, totaling $54,000. Training and technical assistance contracts with legal aid organizations and one state agency generated $42,000.

This revenue is project-based, relationship-dependent, and non-recurring. It has grown modestly and organically without any deliberate revenue function. That is both its limitation and, we argue, evidence for the plan below: institutions in our market already pay us for service, without being asked systematically.

### The Paid Support Tier

The core of the plan is a three-tier annual support subscription. **Essential** ($6,500/year) provides business-hours support with 24-hour response, quarterly configuration assistance, standard reporting, and release notification. **Standard** ($14,000/year) provides extended-hours support with 8-hour response, monthly configuration assistance, custom reporting, integration support up to 20 hours annually, and a named account contact. **Comprehensive** ($28,000/year) provides 24/7 P1 coverage with 2-hour response, dedicated implementation support, unlimited configuration assistance, custom development up to 60 hours annually, and quarterly business review.

Two commitments constrain this model absolutely. First, all software remains free and open source under our existing license. The subscription purchases service, not access, and no county forgoes functionality by declining. Second, we maintain a hardship waiver for counties under 15,000 residents and for legal aid organizations below a defined budget threshold, funded at $65,000 annually from the grant in years one and two and from unrestricted revenue thereafter. We will not build a revenue model that prices out the smallest counties, which are precisely where per-capita need is highest.

### Buildup to $1,100,000

**Year one: $415,000.** Support subscriptions contribute $210,000. Conversion of the six existing informal arrangements to formal Standard subscriptions yields $84,000. Fifteen new subscribers — targeted from our existing 46-county base, where the relationship is established and the value demonstrated — at a blended $8,400 yields $126,000. This requires converting 33 percent of existing counties, and we have non-binding letters of interest from nine. Integration services contribute $135,000, reflecting new-county onboarding work. Training and technical assistance contribute $70,000, growing with the county base.

**Year two: $735,000.** Support subscriptions contribute $455,000. Year-one subscribers renew at 88 percent, and the tier mix shifts upward as counties that began at Essential move to Standard following the renewal-tracking launch. Twenty-three net new subscribers, drawn from both the existing base and the twelve counties onboarded in year one. Blended revenue per subscriber rises to $10,800. Integration services contribute $185,000. Training and technical assistance contribute $95,000.

**Year three: $1,100,000.** Support subscriptions contribute $725,000: 63 subscribers at a blended $11,500, reflecting 90 percent renewal, continued tier migration, and 21 net new subscribers. Integration services contribute $245,000, including three multi-county consortium engagements now in preliminary discussion. Training and technical assistance contribute $130,000, including a certification curriculum for county eligibility staff.

### Why We Believe These Numbers

The central assumption is that 63 of 76 county agencies and legal aid organizations — 83 percent — subscribe by year three. We test that assumption four ways.

**Willingness to pay is already demonstrated.** Six counties pay us today without a formal product. Those arrangements arose from county requests, not our solicitation.

**The alternative is more expensive.** Commercial benefits screening platforms in this market carry annual costs that begin at four to six times our Comprehensive tier for comparable county populations, and require the county to abandon an open-source tool their staff already use. Our $6,500 Essential tier is below the annual cost of one week of a temporary eligibility worker.

**Budget authority exists.** County human services and court administration budgets in our region routinely carry technical assistance and software support lines in the $5,000–$30,000 range. We are not asking counties to create a new budget category. Several counties have told us that a formal invoice is administratively *easier* to process than the informal arrangements we currently use.

**The renewal-tracking functionality creates urgency.** Counties facing Medicaid unwinding volume have a concrete, dated operational problem. A tool that reduces procedural terminations has a value proposition that does not require abstraction.

We also note what would falsify the plan. If year-one subscriptions fall below $150,000, the conversion assumption is wrong and the model requires restructuring rather than patience. We commit to reporting this to the Foundation at the year-one mark with a revised plan rather than an assurance.

### Contingency

If earned revenue reaches only 70 percent of projection ($770,000 by year three), the shortfall of $330,000 is addressed through three levers, in order: reduction of new-county onboarding pace from 10 to 6 counties in year three, saving approximately $145,000; deferral of two planned engineering hires, saving approximately $190,000; and, if necessary, a bridge fundraising campaign against a diversified funder base that now includes four institutional funders beyond this Foundation. Core platform operation and support for existing counties would not be reduced. We would rather grow more slowly than serve existing counties worse.

### Beyond the Grant Period

At year-three run rates, earned revenue of $1,100,000 covers approximately 78 percent of the program's ongoing annual operating cost of roughly $1,410,000, exclusive of new development. The remaining gap is covered by a diversified base including two state-level contracts now in early discussion, continued foundation support at a materially reduced level, and individual and corporate giving. We are not projecting full self-sufficiency, and we would be suspicious of any organization in this domain that did. We are projecting that the majority of the cost of keeping this infrastructure running is borne by the institutions that benefit from it, which we believe is the correct destination.

---

## Budget Narrative

**Total request: $3,100,000 over three years.** Year one: $1,140,000. Year two: $1,040,000. Year three: $920,000. The declining profile is intentional: grant support decreases as earned revenue increases.

### Personnel — $1,984,000 (64%)

Personnel is the dominant cost because this is a program of engineering, evaluation, and relationship work.

**Existing staff allocation — $728,000.** Partial allocation of current staff time to grant activities, based on documented time allocation. Executive Director at 25 percent ($72,000 over three years). Interim/permanent CTO at 60 percent ($198,000). Finance Director at 30 percent ($81,000). Four existing engineers at an average 45 percent ($302,000). Two program staff at 30 percent ($75,000).

**New positions — $1,256,000.** Two full-stack engineers for the screener rebuild, beginning month one, at $118,000 fully loaded ($708,000 over three years). One localization engineer, beginning month three of year one, at $112,000 fully loaded, reducing to 50 percent in year three ($280,000). One support engineer, beginning month two of year one, at $98,000 fully loaded ($268,000).

Fully loaded rates include salary, payroll taxes, health benefits, and retirement contribution at our standard 27 percent.

### Contracted Services — $486,000 (16%)

**Independent evaluation — $246,000.** Subaward to the university policy center led by Ramona Chee: stepped-wedge design and randomization, annual independent evaluation memos, cost analysis validation, and final summative evaluation.

**Legal aid partnership — $118,000.** Compensation to our legal aid partner for user testing, cognitive interviewing in Spanish and Vietnamese, gold-standard case set maintenance, and pre-release eligibility logic review.

**Translation and linguistic review — $92,000.** Professional translation, independent back-translation, plain-language review, and cognitive interview facilitation across both languages, covering approximately 4,200 source strings plus notification templates and help content.

**Security and accessibility audit — $30,000.** Annual third-party penetration testing and WCAG 2.1 AA conformance audit at $10,000 annually.

### Technology and Infrastructure — $312,000 (10%)

**Cloud infrastructure — $174,000.** Compute, storage, database, and content delivery, scaling with volume: $46,000 in year one, $58,000 in year two, $70,000 in year three. Includes redundant multi-region deployment required by our uptime objectives.

**Message delivery — $96,000.** SMS, voice, and email delivery for hearing reminders and renewal notifications, at approximately $0.019 blended per message across a projected 5.05 million messages.

**Development tooling and monitoring — $42,000.** Version control, CI/CD, error tracking, synthetic uptime monitoring, and analytics.

### County Onboarding and Training — $178,000 (6%)

**Onboarding delivery — $96,000.** Travel, on-site implementation support, and configuration assistance across 30 counties at approximately $3,200 per county, declining as the self-service console matures.

**Training curriculum development — $44,000.** Recorded training modules, documentation, and the implementation checklist system, developed in year one and revised in year two.

**Hardship waiver fund — $38,000.** Partial support for the waiver program in years one and two for the smallest counties and legal aid organizations. Transitions to unrestricted funding in year three.

### Contingency — $85,000 (3%)

Architectural revision reserve, available should a permanent CTO arriving mid-program identify changes requiring rework. Any expenditure is reported with justification. Unexpended funds are returned or reallocated with Foundation approval.

### Indirect Costs — $55,000 (2%)

Applied at a rate substantially below our federally negotiated rate, reflecting that most administrative cost is captured directly in the personnel allocations above.

### Cost Per Screening

Across the grant period, total organizational expense of approximately $13.9 million supports 1,030,000 screenings and 217,000 hearing reminders. Fully loaded cost per screening declines from $8.94 at baseline to $5.60 in year three. Marginal cost declines from $1.42 to $0.95. The Foundation's investment amounts to approximately $3.01 per screening across the grant period, against an average benefit value per approved application substantially exceeding $2,000 annually.

### Fiscal Controls

Grant funds are tracked in a restricted fund with expenditures coded to budget categories at entry. The Finance Director prepares monthly budget-to-actual reports reviewed by the Executive Director and quarterly by the board Finance Committee. Variances exceeding 10 percent in any category trigger written explanation. We undergo an annual independent audit; our most recent three audits were unmodified with no material weaknesses or significant deficiencies identified. Any proposed reallocation exceeding 10 percent between categories will be submitted for Foundation approval in advance.

---

## Closing

We are asking this Foundation to fund us again after declining to renew us once. We have tried to write an application that earns that rather than assumes it: one that states our reporting failure and the specific machinery built to prevent its recurrence, that names our interim technical leadership and explains why we consider it sufficient and what happens if the search runs long, that reports a lost Nebraska pilot and rebuilds the plan without it, that sets a failure-to-appear target above our own published result because the published result came from favorable conditions, and that shows the arithmetic behind every dollar of a $1.1 million earned revenue projection.

What we are building is unglamorous infrastructure for people whose median household income is $27,400 and who complete these forms on a phone. The measure of it is whether a household keeps its coverage through a renewal it would otherwise have missed, and whether a person appears at a hearing they would otherwise have defaulted. We have moved those numbers before. With this investment, we intend to move them across 76 counties, in three languages, and to build an organization that can keep doing it after the grant is spent.
