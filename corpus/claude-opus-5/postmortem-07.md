# Incident Postmortem: Payroll Conversion Failure and Wage Underpayment Event

**Penobscot Bay Independence Network**
**Incident ID:** PM-2026-014
**Classification:** Severity 1 — Compensation Integrity, Regulatory Exposure, Service Continuity
**Period Covered:** July 14, 2026 – January 30, 2027
**Document Status:** Final, approved for board and staff distribution
**Prepared for:** Board of Directors, Executive Team, All Staff
**Date of Issue:** February 6, 2027

---

## 1. Purpose and Framing

This postmortem examines the failure of the Harborworks payroll conversion and the wage underpayment event that followed. It is written to be read by people who were harmed by the failure. Six hundred ten of our colleagues were paid less than they earned, in some cases for six consecutive weeks, while continuing to provide overnight and weekend support to the 480 adults who depend on us.

This document does not assign personal blame. That is a deliberate choice and it is worth stating plainly why. Every decision described here was made by a competent person acting on the information available to them, inside a set of constraints the organization created. A controller who spends nine days auditing time clock data is not careless; he is a person who formed a reasonable hypothesis and had no mechanism telling him to test it against alternatives. A CFO who approves a remediation run without reconciliation is not indifferent; he is a person under enormous pressure to get money to employees who could not pay rent, working without a payroll manager and without a documented off-cycle procedure. If we replace these individuals and change nothing else, we will reproduce this incident with different names attached.

The failure here is organizational. It lives in a compressed timeline, an unstaffed function, an absent test plan, a broken intake channel, and an approval process that had no independent check. Those are the things this document examines, and those are the things the action items address.

---

## 2. Summary

Penobscot Bay Independence Network converted its payroll processing from its legacy system to the Harborworks platform in October 2026. The conversion had been scheduled for July 2026 and was moved to October to free staff capacity for a federal grant application deadline. As part of that compression, parallel testing — running both systems simultaneously and comparing outputs — was reduced from two full pay cycles to one.

The shift differential and overtime rules table did not migrate to the new platform. This table encoded the premium rates paid for evening, overnight, and weekend coverage, ranging from $1.50 to $3.25 per hour, and defined the regular rate of pay used in overtime calculations. Without it, Harborworks paid base rates only and calculated overtime at 1.5 times base rather than 1.5 times the regular rate inclusive of differentials.

The first affected paychecks issued October 23, 2026. Employees reported discrepancies beginning October 24. The payroll manager position had been vacant since August 2026, and incoming reports collected in a shared mailbox that had no assigned owner, no service-level expectation, and no triage process. Controller Soren Bragg formed an early hypothesis that the time clock system was failing to transmit shift codes and directed nine days of punch-data auditing. That hypothesis was plausible, consistent with the symptom pattern as initially described, and wrong. Director of Human Resources Nkechi Obiora identified the missing rules table on November 12, 2026, after three affected pay periods had run.

The remediation compounded the harm. Off-cycle checks issued November 18, 2026 double-paid 84 employees a combined $71,000, omitted the overtime recalculation entirely, and applied incorrect withholding treatment that was not discovered until W-2 preparation in January 2027. Chief Financial Officer Marcus Tillinghast approved the off-cycle run without reconciliation against the underpayment schedule. Chief Executive Officer Delphine Ouellette was briefed on the full scope on November 14, 2026.

The downstream consequences were severe and are the reason this incident is classified Severity 1. Thirty-eight direct support professionals resigned between November 1 and December 15, 2026. Overtime expense rose $390,000 over six weeks as remaining staff absorbed vacant shifts. Director of Residential Services Imelda Restrepo reported two homes operating below mandated supervision ratios, resulting in two state licensing citations in December 2026. Twenty-two employees filed a wage complaint with the Maine Department of Labor.

Full remediation, including corrected overtime, corrected withholding, and W-2C issuance, completed January 30, 2027.

---

## 3. Impact

### 3.1 Compensation Impact

| Measure | Value |
|---|---|
| Employees underpaid | 610 |
| Total underpayment | $251,000 |
| Average underpayment per employee | $412 |
| Pay periods affected before identification | 3 |
| Days from first affected check to root cause identification | 20 |
| Days from first employee report to root cause identification | 19 |
| Employees double-paid in remediation | 84 |
| Value of overpayment | $71,000 |
| Employees requiring W-2C corrections | 610 |
| Days from first affected check to full financial remediation | 99 |

The $412 average obscures the distribution. Employees working predominantly day shifts on weekdays saw little or no impact. Employees carrying overnight and weekend rotations — disproportionately those with the least schedule flexibility, and disproportionately those in the $19 to $23 hourly band — experienced shortfalls exceeding $700 across the three periods. For a direct support professional earning $20 an hour, a $700 shortfall over six weeks is roughly a fifth of net pay. This is not an accounting variance. It is a missed rent payment, a car repair deferred, a heating oil delivery skipped in a Maine November.

### 3.2 Workforce Impact

| Measure | Value |
|---|---|
| DSP resignations, Nov 1 – Dec 15, 2026 | 38 |
| DSP headcount at incident start | 610 (of 740 total employees) |
| Resignation rate over the 45-day window | 6.2% of DSP workforce |
| Incremental overtime expense, 6 weeks | $390,000 |
| Homes falling below mandated supervision ratio | 2 |
| State licensing citations issued | 2 |

Exit interviews were conducted with 29 of the 38 departing employees. Twenty-four cited the payroll failure directly. Eleven cited not the shortfall itself but the absence of a response — the experience of reporting a problem and receiving no acknowledgment for two weeks or more. Several described the shared mailbox specifically.

The overtime figure of $390,000 deserves emphasis because it inverts the economics that drove the original decision. The conversion was compressed to protect a grant application. The compression produced a failure whose overtime cost alone exceeded the value of the grant sought.

### 3.3 Regulatory and Legal Impact

| Measure | Value |
|---|---|
| Maine DOL wage complaints filed | 22 |
| State licensing citations | 2 |
| Homes subject to corrective action plans | 2 |
| Anticipated federal wage-and-hour exposure | Under review |

The two licensing citations relate to supervision ratios in homes where DSP departures could not be covered. Both homes have submitted corrective action plans. Neither citation involved harm to a person we support, a fact that reflects the extraordinary effort of remaining staff rather than the adequacy of our systems.

The 22 wage complaints raise a question beyond the underpayment: whether overtime calculated on base rate alone, excluding shift differentials from the regular rate of pay, constitutes a Fair Labor Standards Act violation independent of the underpayment itself. Outside counsel has been engaged. The organization's position is to remediate fully regardless of the legal determination.

### 3.4 Impact on People We Support

No documented adverse events occurred. Two homes experienced staffing patterns that increased risk. Continuity of relationship — a core element of quality in developmental disability services — was disrupted in at least nine homes where departing DSPs had tenures exceeding two years. This impact is real and not quantifiable in the tables above.

---

## 4. Timeline

All times Eastern.

### Phase 1 — Decision and Compression (July – September 2026)

**July 14, 2026, 10:00** — Executive team reviews the Harborworks implementation plan. Go-live is scheduled for the first July pay cycle. Parallel testing is scoped at two full pay cycles with variance reconciliation between legacy and Harborworks outputs.

**July 14, 2026, 11:20** — In the same meeting, the team reviews a federal grant opportunity with an August submission deadline requiring significant finance and HR staff time for budget narrative and workforce data. The conversion is moved from July to October 2026 to free capacity.

**July 21, 2026** — Revised implementation plan issued. Parallel testing reduced from two pay cycles to one. The plan documents the reduction but records no assessment of what testing coverage is lost. No risk acceptance is logged. No compensating control is added.

**August 8, 2026** — The payroll manager resigns, effective August 21. This role owned the differential rules table, the pay-code mapping, and the pre-release payroll review. Duties are informally distributed: transactional processing to a payroll specialist, oversight to the Controller, employee inquiries to a shared mailbox monitored on a best-effort basis.

**August 21, 2026** — Payroll manager position becomes vacant. Recruitment opens. The position remains unfilled through the entire incident window.

**September 2026** — Harborworks data migration executed. Employee master records, tax profiles, direct deposit information, and accrual balances migrate. The shift differential and overtime rules table does not migrate. No migration completeness checklist exists that would enumerate this table as a required object. No failure is logged by either system. The omission is silent.

**September 28 – October 9, 2026** — Single parallel test cycle runs. The comparison is performed at the level of aggregate gross-to-net and total employer tax liability. Variances fall within the tolerance threshold set for the test. The differential shortfall is present in the test data but is diluted at the aggregate level and is not surfaced because no component-level comparison of differential earnings is performed. The two-cycle plan had specified component-level reconciliation in the second cycle.

**October 12, 2026** — Conversion signed off. Harborworks becomes system of record.

### Phase 2 — Failure and Detection (October 23 – November 12, 2026)

**October 23, 2026, 06:00** — First Harborworks-processed payroll issues, covering the October 5–18 work period. Differentials are absent. Overtime is calculated at 1.5 × base rate. 610 employees are underpaid.

**October 24, 2026, 07:15** — First employee report arrives in the shared payroll mailbox. An overnight DSP notes that her check is short approximately $88 and that the pay stub shows no differential line.

**October 24, 2026, through end of day** — Fourteen further reports arrive by email. An unknown additional number are raised verbally to house managers, who lack a defined escalation path for pay issues and in most cases advise employees to email payroll.

**October 26, 2026, 09:00** — Payroll specialist flags the accumulating volume to Controller Soren Bragg. Approximately 40 reports are in the mailbox. None have been acknowledged.

**October 26, 2026, 14:00** — Bragg reviews a sample of affected records. He observes that affected employees are concentrated in evening, overnight, and weekend rotations, and that shift codes appear inconsistently in the imported time data. He forms the hypothesis that the time clock system is failing to transmit shift codes to Harborworks. This hypothesis explains the observed symptom pattern and is consistent with a known category of interface failure during conversions. It is a reasonable first hypothesis. It is not tested against alternatives, and no alternative hypothesis is recorded.

**October 27 – November 4, 2026** — Nine days of time clock punch-data auditing. Bragg and the payroll specialist pull raw punch records, compare them to Harborworks imports, and validate clock configurations at multiple sites. The audit consumes essentially all available payroll capacity. No mechanism exists that would require the hypothesis to be revisited on a schedule or that would trigger escalation on elapsed time.

**November 4, 2026** — Second Harborworks payroll issues, covering October 19 – November 1. Differentials absent again. Same population affected. The audit is still in progress and the payroll is not held.

**November 5, 2026, 08:30** — Mailbox volume exceeds 300 messages. Some employees have written three or more times. Response rate remains near zero.

**November 6, 2026** — Director of Residential Services Imelda Restrepo escalates to HR, reporting that house managers across multiple sites are fielding pay complaints and that she is beginning to see call-out and resignation activity she attributes to the pay issue.

**November 9, 2026, 11:00** — Director of Human Resources Nkechi Obiora joins the investigation. She requests the pay-code configuration in Harborworks rather than additional time data — a shift in investigative frame from the input side to the calculation side.

**November 10 – 11, 2026** — Obiora and an HR analyst reconstruct the legacy differential rules from the prior system's configuration export and compare them to Harborworks. The comparison is manual.

**November 12, 2026, 15:40** — Obiora identifies that the shift differential and overtime rules table does not exist in Harborworks. There is no partial or corrupted table. The object was never created. The time clocks are transmitting shift codes correctly; Harborworks has no rules to apply to them. **Root cause identified: day 20 after the first affected check, day 19 after the first employee report.**

**November 12, 2026, 17:00** — Obiora notifies Bragg and CFO Marcus Tillinghast.

### Phase 3 — Remediation and Compounding (November 13 – 18, 2026)

**November 13, 2026, 09:00** — Third Harborworks payroll processes with the same defect. The rules table is not yet rebuilt and there is no mechanism to hold or manually adjust the run. Three pay periods are now affected.

**November 13, 2026, 13:00** — Harborworks vendor support engaged. Vendor confirms the table was not included in the migration package and that no migration validation report was generated or requested.

**November 14, 2026, 08:00** — CEO Delphine Ouellette briefed on full scope: 610 employees, three pay periods, estimated $251,000. **This is 22 days after the first affected check and the first executive-level awareness of the incident's magnitude.**

**November 14, 2026, 10:00** — Ouellette directs immediate off-cycle remediation and organization-wide communication.

**November 14, 2026, 16:00** — First all-staff communication issued acknowledging the error and committing to correction by November 18.

**November 16 – 17, 2026** — Underpayment schedule constructed by reconstructing three pay periods of differential earnings for 610 employees from time data. The work is performed under acute time pressure by staff already stretched, without a payroll manager, and without a documented off-cycle procedure. Three specific decisions are made under that pressure:

- Overtime recalculation is deferred, on the reasoning that base differential recovery is the larger and more urgent component and overtime can follow. This deferral is not communicated to employees.
- Withholding treatment is applied as supplemental wages using a default flat rate rather than aggregating with regular wages as the retroactive nature of the payment required.
- Reconciliation of the off-cycle file against the underpayment schedule is skipped for time.

**November 17, 2026, 20:00** — Tillinghast approves the off-cycle run. The approval control as designed requires only a single executive signature and does not require attestation that reconciliation has occurred. The control cannot detect its own bypass.

**November 18, 2026, 06:00** — Off-cycle checks issue. Most employees receive substantially correct base differential recovery. Eighty-four employees receive duplicate payments totaling $71,000, caused by a merge error in which a partial file from an earlier working session was combined with the final file. Reconciliation would have caught this. Overtime remains unpaid. Withholding is incorrect for all 610 recipients.

### Phase 4 — Extended Remediation (November 19, 2026 – January 30, 2027)

**November 19, 2026** — Duplicate payments identified during post-issue review. Decision made not to demand immediate repayment, given the circumstances and the credibility cost of asking underpaid employees to return money days after being made partially whole. Repayment arrangements are offered as voluntary and interest-free over up to twelve months.

**November 20, 2026** — Rules table rebuilt in Harborworks and validated against 40 sample employees spanning all differential combinations. Regular payroll processing returns to correct operation from the November 27 cycle forward.

**November 24, 2026** — Maine Department of Labor notifies the organization of wage complaints filed by 22 employees.

**December 2, 2026** — Restrepo reports two homes below mandated supervision ratios. Contingency staffing plans activated, including administrative staff with current certifications covering direct support shifts.

**December 8 and December 15, 2026** — Two state licensing citations issued for supervision ratio deficiencies. Corrective action plans submitted within required timeframes.

**December 15, 2026** — Cumulative DSP resignations reach 38 for the window beginning November 1.

**December 22, 2026** — Overtime recalculation completed. Supplemental payments issued to affected employees covering the FLSA regular-rate correction across the three periods.

**January 9, 2027** — W-2 preparation identifies the withholding error on the November 18 off-cycle run. All 610 recipients require correction.

**January 12, 2027** — Employees notified of the withholding error and the W-2C process. This is the fourth corrective communication employees have received about the same underlying event.

**January 30, 2027** — W-2C forms issued. Financial remediation complete. **Ninety-nine days from the first affected check.**

**February 6, 2027** — This postmortem issued.

---

## 5. Root Cause

**The shift differential and overtime rules table was not migrated to Harborworks, and no control existed at any stage of the conversion capable of detecting its absence before employees were paid.**

The root cause has two inseparable halves. The first is the migration omission itself: a required configuration object was not transferred, and the transfer process generated no error, warning, or completeness report. The second is the detection gap: the organization had four sequential opportunities to catch the omission and every one of them was structurally incapable of doing so.

**Opportunity 1 — Migration validation.** No completeness checklist enumerated the configuration objects required for correct calculation. Migration was verified by confirming that employee records arrived, not by confirming that the rules governing how those records are paid arrived. The vendor generated no validation report and none was requested. A missing table looked identical to a table that was never needed.

**Opportunity 2 — Parallel testing.** The two-cycle test plan included component-level earnings reconciliation in the second cycle. Compression eliminated the second cycle. The surviving single cycle compared aggregate gross-to-net and employer tax liability against a tolerance threshold. Differential earnings across 740 employees represent a small enough share of aggregate gross that the variance fell inside tolerance. The test was executed correctly and was structurally blind to the defect.

**Opportunity 3 — Pre-release payroll review.** The payroll manager role owned a pre-release review that historically included spot-checking pay components on a sample of employees across shift patterns. When the role went vacant, transactional processing transferred but this review did not. It was not documented as a discrete control; it lived in the incumbent's practice. It disappeared without a decision being made to remove it.

**Opportunity 4 — Employee reports.** Fourteen reports arrived within 24 hours of the first affected check. This was the fastest and most accurate detection signal available, and the organization possessed no mechanism to convert it into action. The shared mailbox had no owner, no service level, no triage, no acknowledgment, and no volume-based escalation trigger. Forty reports accumulated before anyone with authority saw them, and by then the investigation had already been framed around a different hypothesis.

The four-controls-blind pattern is the actual finding. Any single failure is survivable. The organization built a system in which all four failed for related reasons — compression, vacancy, undocumented practice, and an unstaffed channel — and those reasons trace back to decisions made in July and August, months before any employee was underpaid.

---

## 6. Contributing Factors

### 6.1 Timeline Compression Without Risk Assessment

The July decision to move the conversion to October and halve parallel testing was made in a single meeting alongside the grant discussion that motivated it. The decision was recorded; the risk transfer was not. No one asked, in writing or otherwise, what the second test cycle was for and what would go undetected without it.

This is a governance gap, not a judgment failure. The organization had no requirement that scope reductions to a testing plan be accompanied by a documented statement of coverage lost and compensating control added. Absent that requirement, the reduction was invisible as a risk decision. It appeared as a schedule adjustment.

It is also worth noting what compression did not do: it did not cause the migration omission. The table would likely have been missed regardless. What compression removed was the mechanism that would have caught it. Compression converted a recoverable configuration error into a three-pay-period wage failure.

### 6.2 Sustained Vacancy in the Payroll Manager Role

The role was vacant from August 21 through the entire incident. The organization treated this as a staffing problem to be resolved by recruitment while distributing duties informally. It was in fact a control problem.

Three controls lived in this role: the pre-release payroll review, ownership of differential rules configuration, and ownership of employee pay inquiries. The redistribution moved transactional work to a payroll specialist and oversight to the Controller. None of the three controls transferred, because none of the three were documented as controls. They were practices, and practices do not survive the departure of the practitioner.

Eighty-seven days elapsed between the vacancy and the first affected check. That is ample time to have identified the control gap had any process existed to review control ownership when a position becomes vacant. No such process existed.

### 6.3 Absence of an Employee Pay Inquiry Channel

The shared mailbox was not a channel. It was a container. It had no owner, no acknowledgment commitment, no categorization, no aging visibility, and no trigger by which unusual volume would escalate on its own.

The signal that arrived in that mailbox on October 24 was excellent. Fourteen people independently and accurately reported a real defect within a day of its manifestation. The organization's fastest and most reliable detection instrument was its own workforce, and the instrument's output went nowhere for two days and was never acknowledged at all.

The secondary damage is at least as significant. Twenty-four departing employees cited the payroll failure; eleven cited the silence rather than the shortfall. An error that is acknowledged within hours is a system problem. An error that goes unanswered for weeks is experienced as something else — as evidence about how the organization regards the people doing its hardest work. The retention consequence traces substantially to the silence, not the error.

House managers compounded this without meaning to. Employees raising issues verbally were told to email payroll, because managers had no escalation path of their own. The advice routed the signal directly into the container.

### 6.4 Hypothesis Fixation Without Structured Review

The time clock hypothesis was reasonable. Affected employees clustered in differential-eligible shifts, shift codes appeared inconsistent in imported data, and interface failures are a common conversion problem. A competent investigator would form this hypothesis.

What went wrong is that the organization had no mechanism requiring the hypothesis to compete with alternatives. Nine days is a long time for a single unfalsified theory to consume all available capacity. Three structural absences allowed it:

- **No alternative hypothesis logging.** A five-minute exercise listing plausible causes would almost certainly have produced "differential rules not configured correctly in the new system" as a candidate, and that candidate is cheap to test — one query of the pay-code configuration.
- **No time-boxing.** No rule stated that an unresolved payroll investigation escalates at 48 or 72 hours regardless of progress. The investigation could run indefinitely as long as it appeared to be progressing.
- **No investigative frame diversity.** The investigation was staffed entirely from finance. Finance frames payroll problems as data problems. When Obiora joined on November 9, she reframed within hours from input data to calculation configuration and reached root cause in three days. The difference was not competence. It was the question being asked. HR owns pay policy and therefore instinctively asks whether the system knows the policy; finance owns transactions and asks whether the data is right.

### 6.5 Remediation Executed Without Procedure or Independent Check

The organization had never documented an off-cycle payroll procedure. The November 16–18 work was improvised under acute pressure by people who had been working the incident for three weeks, with a CEO commitment to a public deadline and 610 colleagues waiting on money.

Three defects resulted, each traceable to an absent structural element:

- **Duplicate payments (84 employees, $71,000).** A merge error combining a partial working file with the final file. Reconciliation against the underpayment schedule was the designed defense; it was skipped for time. The approval control required a signature but not an attestation that reconciliation had occurred, so skipping it was invisible to the approver.
- **Omitted overtime recalculation.** A defensible sequencing decision — base recovery first, overtime second — made without a checklist that would have required all components to be enumerated and either included or explicitly deferred with a date. Because the deferral was implicit, it was not communicated, and employees who had been told they were being made whole discovered five weeks later that they had not been.
- **Incorrect withholding.** Retroactive wage payments spanning prior periods require aggregation with regular wages; the run applied a supplemental flat rate. This is a technical determination that the vacant payroll manager role would have owned. It surfaced in January, generating 610 W-2C corrections and a fourth corrective communication.

The single-signature approval is the structural finding here. A control that requires one executive's judgment under time pressure, with no independent verification and no attestation of prerequisite steps, is not a control. It is a formality that records who was present when the decision was made.

### 6.6 Compounding Communication Failures

Employees received four separate corrective communications over eleven weeks: the November 14 acknowledgment, the November 18 partial remediation, the December 22 overtime correction, and the January 12 withholding notice. Each was accurate. Together they produced an impression of an organization that did not know the extent of its own problem.

There was no incident communication plan. Each message was drafted in response to the latest discovery rather than as part of a sequence that had set expectations about what remained uncertain. The November 14 message in particular committed to correction by November 18 without qualifying that overtime and tax treatment were still being worked. That commitment was made in good faith and it was not kept, and the gap between the two did more reputational damage than a more hedged initial message would have.

### 6.7 Sector Conditions

Two contextual factors do not excuse the failure but explain its severity.

Direct support professional work at $19 to $23 an hour is performed by people with limited financial buffer. A $400 shortfall in this workforce produces immediate hardship in a way it would not in a higher-wage setting. The organization's tolerance for payroll error is therefore lower than a generic risk assessment would suggest, and the conversion risk was not evaluated with that in mind.

The DSP labor market in midcoast Maine is tight, with competing employers and a thin applicant pool. Thirty-eight resignations could not be backfilled at pace. This converted a compensation error into a staffing crisis and then into a licensing matter within six weeks. The chain from payroll defect to regulatory citation is short in this sector, and nothing in the conversion risk assessment recognized it.

---

## 7. What Worked

**Employee reporting.** Fourteen accurate reports within 24 hours. The workforce detected the failure faster and more precisely than any system the organization owned. This is a genuine asset and the action items are built around making it usable.

**Cross-functional reframing.** Obiora reached root cause in three days after nine days of investigation had not. The mechanism was a change in the question being asked, and it demonstrates that multi-function investigation is a high-yield practice worth institutionalizing.

**Executive decisiveness after escalation.** Ouellette received the briefing on November 14 and directed remediation and public acknowledgment within two hours. The four-day turnaround to an off-cycle run is fast. The defects in that run came from missing procedure, not from hesitation.

**The decision not to claw back.** Choosing not to demand immediate repayment from 84 employees, days after they had been underpaid for six weeks, was correct. It cost $71,000 in short-term cash and preserved something more valuable. Voluntary repayment arrangements have since recovered a substantial portion.

**Operational continuity.** Restrepo's team maintained services across 62 homes through 38 departures and a six-week overtime surge. Two homes fell below ratio; sixty did not. Administrative staff with current certifications covered direct support shifts. No person we support experienced a documented adverse event. This was accomplished by people absorbing extraordinary load, which is a testament to them and an indictment of the systems that required it.

**Regulatory cooperation.** Corrective action plans were submitted within required timeframes and the Department of Labor engagement has been fully cooperative, including proactive disclosure of the overtime and withholding errors before they were asked about.

---

## 8. What Did Not Work

**Aggregate-level testing.** Comparing totals within a tolerance threshold cannot detect a component-level defect affecting a minority of earnings. The test passed and the system was broken.

**Informal duty redistribution.** Distributing a vacant role's tasks without inventorying its controls silently removed three defenses. This is the most transferable lesson in the document: when a role becomes vacant, the question is not who does the work but which controls just disappeared.

**The shared mailbox.** No owner, no acknowledgment, no escalation. It converted the organization's best detection signal into silence and converted silence into resignations.

**Single-hypothesis investigation.** Nine days on one unfalsified theory with no time-box and no alternatives logged.

**Improvised remediation.** Three defects in one run, each traceable to a missing procedural element, extending the incident from 26 days to 99.

**Single-signature approval.** An approval that cannot verify its own prerequisites is not a control.

**Sequential communication.** Four corrective messages, each accurate, cumulatively corrosive.

**Absence of a payroll incident severity framework.** Nothing in the organization defined a wage error affecting hundreds of employees as an executive-notification event. Twenty-two days elapsed before the CEO knew the scope. That was not a decision anyone made; it was the absence of a rule.

---

## 9. Action Items

Priority 1 items address controls that would have prevented or contained this incident. Priority 2 items address systemic gaps. Priority 3 items address organizational learning.

### Priority 1 — Immediate

| # | Action | Owner | Due |
|---|---|---|---|
| 1.1 | Fill the payroll manager position. If unfilled by the due date, engage an interim contractor at manager level with documented control ownership. | Nkechi Obiora, Director of HR | Mar 31, 2027 |
| 1.2 | Publish a payroll control inventory naming every control, its owner, its frequency, and its evidence artifact. Include the three controls lost in the August vacancy. | Soren Bragg, Controller | Mar 13, 2027 |
| 1.3 | Establish a payroll inquiry channel with a named owner, 1-business-day acknowledgment standard, categorization, aging visibility, and automatic escalation to the Controller and HR Director when 10+ inquiries of the same category arrive within 48 hours. | Nkechi Obiora | Feb 27, 2027 |
| 1.4 | Implement a mandatory pre-release payroll review: component-level verification for a stratified sample of at least 40 employees covering every differential and overtime combination, with sign-off required before release. | Soren Bragg | Feb 27, 2027 |
| 1.5 | Rewrite the off-cycle payroll procedure to require a completeness checklist enumerating all pay components, mandatory reconciliation against the source schedule, dual sign-off by Controller and HR Director, and explicit tax-treatment determination. | Marcus Tillinghast, CFO | Mar 6, 2027 |
| 1.6 | Replace single-signature payroll approval with dual approval requiring written attestation that reconciliation was performed and all components addressed or explicitly deferred with a communicated date. | Marcus Tillinghast | Mar 6, 2027 |

### Priority 2 — Systemic

| # | Action | Owner | Due |
|---|---|---|---|
| 2.1 | Adopt a system conversion standard requiring: a configuration object inventory with sign-off, minimum two parallel cycles with at least one component-level reconciliation, vendor migration validation report, and documented executive risk acceptance for any reduction in test scope. | Marcus Tillinghast | Apr 17, 2027 |
| 2.2 | Establish a vacancy control-transfer protocol: within 10 business days of any resignation in a control-bearing role, the department head must produce a control inventory for that role and a named interim owner for each control, filed with HR. | Nkechi Obiora | Mar 20, 2027 |
| 2.3 | Publish a payroll incident severity framework defining thresholds for executive and board notification. Any wage error affecting 25+ employees or exceeding $10,000 triggers CEO notification within 24 hours. | Delphine Ouellette, CEO | Mar 13, 2027 |
| 2.4 | Adopt an investigation protocol requiring: minimum three logged hypotheses for any payroll incident, mandatory cross-functional staffing including HR and finance, and mandatory escalation review at 48 hours regardless of progress. | Soren Bragg | Mar 27, 2027 |
| 2.5 | Establish a house-manager escalation path for pay inquiries with direct routing to the payroll channel and manager-side visibility into resolution status. | Imelda Restrepo, Director of Residential Services | Mar 20, 2027 |
| 2.6 | Build an incident communication template covering initial acknowledgment, uncertainty disclosure, correction sequencing, and completion, with a standing requirement that any commitment to a remediation date state what remains unresolved. | Delphine Ouellette | Apr 3, 2027 |
| 2.7 | Implement automated payroll anomaly detection comparing differential and overtime earnings period-over-period at the component level, with variance alerts exceeding 15% routed to the Controller before release. | Soren Bragg | May 29, 2027 |

### Priority 3 — Organizational

| # | Action | Owner | Due |
|---|---|---|---|
| 3.1 | Complete Maine DOL wage complaint resolution and document all findings for board review. | Marcus Tillinghast | Apr 30, 2027 |
| 3.2 | Close both licensing corrective action plans and report closure to the board. | Imelda Restrepo | Apr 30, 2027 |
| 3.3 | Complete a DSP retention analysis for the Nov 1 – Dec 15 window, including full exit interview review, and present findings with recommendations. | Nkechi Obiora | Apr 10, 2027 |
| 3.4 | Present this postmortem and action item status at the March and June 2027 board meetings, and hold at least four open staff sessions across regions where employees may ask questions directly of executives. | Delphine Ouellette | Mar 31, 2027 (first cycle) |
| 3.5 | Establish quarterly payroll control testing performed independently of payroll operations, reporting to the Audit Committee. | Marcus Tillinghast | Jun 30, 2027 |
| 3.6 | Conduct a 90-day review of action item completion and effectiveness, including verification that new controls have been exercised at least once. | Soren Bragg | Aug 7, 2027 |

---

## 10. Closing

Two observations should stay with anyone who reads this document.

The first is that the organization's most effective detection mechanism was its employees, and the organization had no way to hear them. Fourteen people told us exactly what was wrong within a day. It took nineteen more days to reach the same conclusion through internal investigation, and the intervening silence cost more in retention than the underpayment cost in dollars. The single highest-return investment identified here is the inquiry channel in item 1.3 — a modest operational change that would have shortened this incident from twenty days to roughly two.

The second is that this incident was set in motion in July and August, months before any check was wrong. A testing plan halved without a risk assessment, and a control-bearing role vacated without a control inventory. Both decisions were made by capable people addressing real priorities. Neither was reviewed against the question this document exists to institutionalize: what defense did we just remove, and what replaces it?

Six hundred ten colleagues were paid less than they earned for work performed in the homes of people who depend on us, through six weeks of a Maine autumn. Thirty-eight of them left. The action items above are the organization's commitment that the conditions permitting this will not persist.

---

**Document Control**

| Field | Value |
|---|---|
| Prepared by | Incident Review Team |
| Contributors | D. Ouellette, M. Tillinghast, N. Obiora, S. Bragg, I. Restrepo |
| Reviewed by | Executive Team, February 3, 2027 |
| Approved by | Delphine Ouellette, Chief Executive Officer |
| Board presentation | March 2027 |
| Next review | Ninety-day action item review, August 7, 2027 |
| Distribution | Board of Directors; all staff; Maine DOL upon request |
