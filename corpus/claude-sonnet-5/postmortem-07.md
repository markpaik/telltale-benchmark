# Incident Postmortem: Harborworks Payroll Conversion Failure and Remediation

**Organization:** Penobscot Bay Independence Network (PBIN)
**Incident ID:** PBIN-2026-011
**Incident Period:** October 23, 2026 – January 2027 (W-2 correction cycle)
**Report Status:** Final
**Prepared for:** Executive Leadership Team, Board Finance Committee
**Classification:** Payroll systems failure with downstream workforce and regulatory impact

This postmortem examines the systems, decisions, and organizational conditions that led to a multi-month payroll failure following PBIN's conversion to the Harborworks payroll platform. It is written to document what happened, why it happened, and what the organization is changing as a result. It is not a record of individual fault. The employees named held roles with direct decision authority over the conversion and its remediation, and their actions are described here only insofar as they illuminate the systemic gaps that allowed a data migration error to go undetected for three pay periods and then be compounded by an unreconciled correction run.

---

## 1. Summary

Penobscot Bay Independence Network serves 480 adults with developmental disabilities across 62 group homes in midcoast Maine and employs 740 people, the majority of them direct support professionals (DSPs) earning $19 to $23 an hour. In mid-2026, PBIN began converting its payroll system to a new platform, Harborworks. The conversion had originally been scheduled for July 2026 but was moved to October 2026 so that the project timeline would align with a grant reporting deadline. As part of that compression, parallel testing — running the legacy and new systems side by side to confirm matching output — was reduced from two full pay cycles to one.

That single parallel cycle did not surface a critical defect: the table governing shift differentials and overtime calculation rules did not migrate from the legacy system into Harborworks. This table controlled evening, overnight, and weekend differentials worth $1.50 to $3.25 an hour, as well as the base used to calculate overtime. Its absence meant that from the first Harborworks-generated paycheck, DSPs working nights, evenings, and weekends — the staffing pattern that covers group home care around the clock — stopped receiving differential pay, and overtime was calculated on straight base rate rather than the correct blended or regular rate.

The first affected paycheck was issued October 23, 2026. Employees reported shortfalls within a day. However, the payroll manager position had been vacant since August, and incoming tickets were collected in a shared mailbox without a single owner triaging or escalating them. Controller Soren Bragg, who had informally absorbed payroll oversight, concluded the discrepancies stemmed from time clocks misreading or dropping shift codes and spent nine days auditing punch data — a diagnosis that did not address the actual defect and delayed correction through two additional pay cycles. Director of Human Resources Nkechi Obiora identified the missing rules table on November 12, after three pay periods had already been paid incorrectly.

The remediation effort, an off-cycle check run issued November 18, was itself flawed: it double-paid 84 employees a combined $71,000, did not recalculate overtime correctly, and posted incorrect tax withholding that would not surface until W-2 corrections were required in January. Chief Financial Officer Marcus Tillinghast approved the remediation run without a reconciliation step. Chief Executive Officer Delphine Ouellette learned the full scope of the failure on November 14, four days before that flawed remediation was issued.

The combined effect was 610 employees underpaid a total of $251,000 (an average of $412 each), 38 DSP resignations between November 1 and December 15, a $390,000 increase in overtime cost over six weeks as remaining staff covered shifts, two group homes falling below state-mandated supervision ratios, two licensing citations from the state in December, and 22 employees filing wage complaints with the Maine Department of Labor.

---

## 2. Impact, By the Numbers

| Metric | Value |
|---|---|
| Employees underpaid | 610 |
| Total underpayment | $251,000 |
| Average underpayment per affected employee | $412 |
| Pay periods affected before detection | 3 |
| Days between first affected check and root cause identification | 20 (Oct 23 – Nov 12) |
| Days spent on incorrect (time clock) diagnosis | 9 |
| Employees double-paid in remediation | 84 |
| Amount double-paid | $71,000 |
| Additional overtime cost, six-week period | $390,000 |
| DSP resignations, Nov 1 – Dec 15 | 38 |
| Group homes cited for supervision ratio violations | 2 |
| State licensing citations issued | 2 |
| Wage complaints filed with Maine DOL | 22 |
| Payroll manager position vacancy at time of conversion | Vacant since August (2+ months pre-cutover) |
| Parallel testing cycles run before cutover | 1 (reduced from planned 2) |
| Shift differential range affected | $1.50–$3.25/hour |

Beyond the direct dollar figures, the underpayment fell disproportionately on the workforce segment least able to absorb it: hourly DSPs earning $19–23 an hour who depend on shift differentials as a meaningful share of take-home pay. A $412 average shortfall against a roughly $1,600–$1,900 biweekly-equivalent income represents a substantial percentage loss for affected staff, concentrated in the same weeks many were also picking up extra shifts to cover colleagues who had already left.

The $390,000 overtime increase and the 38 resignations are not independent figures — attrition drove the overtime spike as remaining staff covered vacated shifts, and the resulting fatigue and short-staffing contributed to the supervision ratio violations that produced the licensing citations. The 22 DOL complaints and the pending W-2 corrections represent open regulatory and compliance exposure that extends past the close of this postmortem.

---

## 3. Timeline

| Date | Event |
|---|---|
| **Pre-2026 (planning)** | Harborworks conversion originally scheduled for July 2026 with two full pay cycles of parallel testing planned. |
| **~June 2026** | Conversion timeline moved to October 2026 to align go-live with a grant reporting deadline. Parallel testing scope reduced from two pay cycles to one to fit the compressed schedule. |
| **August 2026** | Payroll manager position becomes vacant. No backfill hire is completed before the October cutover. Controller Soren Bragg absorbs informal oversight of payroll operations in addition to existing controller duties. |
| **Early October 2026** | Single parallel pay cycle is run comparing legacy system output to Harborworks output. The shift differential and overtime rules table, which governs $1.50–$3.25/hour differentials and overtime base calculation, is not present in the Harborworks configuration. This gap is not identified during the parallel run. |
| **October 23, 2026 (Fri)** | First live Harborworks paycheck is issued to all 740 employees. Checks for staff working evening, overnight, and weekend shifts omit shift differentials; overtime is calculated on base rate only. |
| **October 24, 2026 (Sat)** | Employees begin reporting pay shortfalls to supervisors and the shared payroll mailbox. Because the payroll manager role is vacant, no single owner is monitoring or triaging this inbox. |
| **October 26–30, 2026** | Ticket volume in the shared mailbox continues to grow without centralized triage. Soren Bragg begins investigating reported discrepancies. |
| **October 30, 2026 (Fri)** | Second affected paycheck is issued with the same errors: differentials still missing, overtime still miscalculated. |
| **Early November 2026** | Bragg concludes, based on early review, that the issue originates with time clock hardware or software failing to capture or transmit shift codes correctly — not with the payroll rules configuration. He begins a manual audit of punch data across the 62 group homes to identify the pattern. |
| **November 6, 2026 (Fri)** | Third affected paycheck is issued. Errors persist. Employee complaints and informal reports of hardship continue to accumulate. |
| **November 2–10, 2026** | Bragg's punch data audit continues across nine days, examining time clock logs home by home. The audit does not surface a time clock defect because none exists; the underlying cause is the absent rules table, which sits upstream of punch data in the payroll calculation chain. |
| **November 12, 2026 (Thu)** | Director of Human Resources Nkechi Obiora reviews the Harborworks payroll configuration directly, rather than punch data, and identifies that the shift differential and overtime rules table was never migrated from the legacy system. This is communicated to Bragg and to the CFO's office the same day. |
| **November 13, 2026 (Fri)** | Fourth paycheck is issued. Because the rules table gap has just been identified and no correction has yet been built, this check is also affected. |
| **November 14, 2026 (Sat)** | CEO Delphine Ouellette is briefed on the full scope of the failure: three-plus pay periods affected, hundreds of employees underpaid, and no remediation yet in place. |
| **November 15–17, 2026** | Finance and HR staff work to reconstruct correct shift differential and overtime amounts owed per employee across the affected pay periods, under time pressure to issue an off-cycle correction before the next scheduled pay date. |
| **November 18, 2026 (Wed)** | Off-cycle remediation checks are cut and approved by CFO Marcus Tillinghast without a reconciliation step comparing the correction run's output to the underlying owed-amount calculations. The run double-pays 84 employees a combined $71,000, fails to correctly recalculate overtime for the affected periods, and posts incorrect tax withholding on the corrected amounts. |
| **November 19–30, 2026** | Employees begin reporting a second wave of pay discrepancies stemming from the November 18 run, including overpayments, incorrect overtime, and withholding errors. Reports of DSP resignations begin to accumulate. |
| **December 2026** | Attrition continues; 38 DSPs resign in total between November 1 and December 15. Director of Residential Services Imelda Restrepo reports that two group homes have fallen below state-mandated staff-to-resident supervision ratios as a direct result of short staffing. The state issues two licensing citations related to these ratio violations. Overtime costs rise by $390,000 across the six-week period as remaining staff cover vacated shifts. |
| **December 2026** | Twenty-two employees file wage complaints with the Maine Department of Labor. |
| **January 2027** | Incorrect withholding from the November 18 remediation run resurfaces during W-2 preparation, requiring corrected W-2s for affected employees. |

---

## 4. Root Cause

The root cause of the initial underpayment was a **data migration failure**: the shift differential and overtime rules table was not transferred from the legacy payroll system into Harborworks during conversion. Because this table governs both differential pay and the overtime calculation base, its absence affected every employee working a differentiated shift from the first live pay cycle forward.

This defect was not caught before go-live because the parallel testing window — the control designed specifically to catch discrepancies of this kind — had been reduced from two pay cycles to one in order to meet a grant-driven deadline. A single parallel cycle provides one comparison point; it does not confirm that a discrepancy is systemic versus a one-time timing artifact, and in this case it did not include, or did not surface, a comparison specific to differential and overtime line items across a representative sample of night, weekend, and overnight shift workers.

The defect was not caught after go-live for three additional pay periods because of a **secondary root cause in incident response**: the diagnostic effort was misdirected. The investigation proceeded on the assumption that the problem lay in time clock data capture — a hardware and interface layer — rather than in the payroll system's rate configuration, a software and rules-table layer. This assumption drove nine days of audit effort into punch logs across 62 locations, a labor-intensive process that could not have found the actual defect regardless of how thoroughly it was executed, because the defect was not in the data being audited.

The rules-table gap was ultimately found not through the punch-data investigation but through a direct review of the Harborworks payroll configuration — a review that could have been performed at any point after the first complaints arrived on October 24, but which did not occur until November 12.

---

## 5. Contributing Factors

**Schedule compression driven by an external deadline.** The decision to move the conversion from July to October 2026 was made to align with a grant reporting deadline rather than a payroll-readiness milestone. This created a fixed, non-negotiable end date for a project whose remaining scope — full data migration and validation — did not shrink to match. The parallel testing cut from two cycles to one was a direct consequence of protecting that fixed date.

**Reduced parallel testing scope.** A single parallel pay cycle is a materially weaker control than two. It offers no second data point to distinguish a systemic configuration gap from noise, and it compresses the window in which staff can review differential and overtime output line by line before the new system carries live financial consequences for employees.

**Vacant payroll manager position spanning the cutover.** The role responsible for owning payroll accuracy, monitoring the payroll ticket queue, and holding subject-matter expertise on rate tables and differential rules had been unfilled since August — before the conversion even occurred. This meant that during the highest-risk period for a payroll system change, there was no single accountable owner for payroll operations. Responsibility was informally absorbed by the controller, whose primary role and expertise lay in financial reporting and controls rather than payroll configuration detail.

**Unmonitored, unowned ticket intake.** Employee reports of pay shortfalls landed in a shared mailbox rather than a system with assigned triage, prioritization, or escalation rules. Without a named owner checking that queue, individual reports did not aggregate into a visible pattern until informal or verbal escalation occurred well into the failure window.

**Diagnostic anchoring on a familiar failure mode.** The decision to investigate time clock data as the likely source reflects a reasonable first hypothesis — clock and punch issues are a common source of pay discrepancies — but the investigation continued for nine days without a checkpoint to test that hypothesis against a small sample of affected paychecks and rate configuration directly. A faster falsification step (comparing a handful of affected checks against the underlying rate table configuration) could have redirected the investigation substantially earlier.

**Delayed escalation to executive leadership.** The CEO did not learn the full scope of the failure until November 14 — after three pay periods had already been affected and after the root cause had already been identified two days earlier. The gap between technical discovery (November 12) and executive awareness (November 14) narrowed the window available for a carefully reconciled remediation before the next scheduled pay date, contributing to the pressure that produced the flawed November 18 run.

**Remediation issued without a reconciliation control.** The off-cycle correction run on November 18 was approved without a step to verify that calculated correction amounts matched what was actually disbursed, and without verifying that overtime and withholding were recalculated correctly on the corrected amounts. This is a control gap distinct from the original migration defect: it reflects a decision to prioritize speed of correction — understandable given three pay periods of accumulated harm — over verification, in an environment already under scrutiny and time pressure.

**Downstream operational fragility.** PBIN's staffing model, like much of residential direct care, operates with thin margin above mandated supervision ratios. This meant that payroll-driven attrition converted into licensing-relevant understaffing more quickly than it might in a setting with more staffing slack, compounding a payroll problem into a regulatory compliance problem within weeks.

---

## 6. What Worked

**Direct configuration review ultimately found the correct root cause.** Once Nkechi Obiora reviewed the Harborworks rate and rules configuration directly rather than continuing to investigate punch data, the actual defect was identified quickly. This confirms that the organization had the internal expertise needed to diagnose the problem correctly; the gap was in when and how that expertise was applied, not whether it existed.

**Cross-functional visibility once escalated.** Once the CEO was briefed on November 14, the issue moved to full executive attention, and Finance, HR, and Residential Services began coordinating around both the financial correction and the operational fallout (staffing ratios, licensing exposure) rather than treating these as separate problems.

**Residential Services surfaced the operational consequence quickly.** Imelda Restrepo's identification of the two group homes falling below mandated supervision ratios allowed the organization to become aware of licensing exposure before, rather than after, state citations were issued in an uncontrolled way — though the citations still occurred, the organization was not blindsided by them internally.

**The underlying payroll platform, once correctly configured, was capable of accurate calculation.** Nothing in this incident indicates a fundamental defect in Harborworks itself; the failures were migration, testing, and process failures, which means the corrective path did not require a platform replacement.

## 6. What Did Not Work

**No control caught the missing rules table before go-live.** The single parallel cycle either did not include a differential/overtime-specific comparison or did not weight it enough to surface a complete omission. A checklist-driven, line-item validation of every rate table category against legacy output — independent of overall parallel run "pass/fail" status — was not in place.

**No owned intake process for post-cutover payroll issues.** A shared mailbox with no assigned triage owner is not an incident detection system. Reports that individually looked like isolated errors did not get aggregated into a pattern despite arriving "within a day" of the first affected check, per employee reports.

**The investigation lacked a falsification checkpoint.** Nine days is a long time to pursue a single hypothesis without a low-cost test of an alternative explanation. A same-day comparison of a handful of underpaid checks against the payroll system's rate configuration — rather than the time clock logs — would likely have identified the missing table far earlier.

**Escalation to the CEO lagged technical discovery.** A two-day gap between the controller/HR director identifying the root cause and the CEO learning the full scope reduced the time available to plan a careful, reconciled correction rather than a rushed one.

**Remediation was not reconciled before disbursement.** Approving an off-cycle correction run without verifying calculated-versus-disbursed amounts, and without confirming that overtime and withholding logic applied correctly to the correction itself, converted a single-cause incident into a two-cause incident. The double-payment, overtime, and withholding errors from November 18 were avoidable with a review step that did not depend on solving the original migration defect — it depended only on checking the fix.

**Withholding errors were not caught until W-2 preparation.** A three-month gap between the remediation run and the discovery of withholding errors meant that a preventable and correctable payroll problem became a tax-document correction problem, adding administrative burden for both the organization and affected employees at the start of the following year.

**No apparent trigger for backfilling the payroll manager role before a high-risk system change.** The position was vacant for the two months immediately preceding a payroll platform conversion, and remained vacant through the entire detection and remediation period covered by this report.

---

## 7. Action Items

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Fill the payroll manager position on a permanent basis; until filled, designate a named interim owner with explicit authority over payroll configuration, ticket triage, and escalation. | Nkechi Obiora, Director of Human Resources | September 1, 2026 (interim owner named within 5 business days of this report; permanent hire targeted) |
| 2 | Conduct a full line-item audit of the current Harborworks configuration against the legacy system's complete rate table set (shift differentials, overtime rules, and any other pay-rule categories), independent of the original migration project team. | Soren Bragg, Controller | 30 days from report issuance |
| 3 | Establish a documented, owned intake and triage process for post-cutover and ongoing payroll issue reports, replacing the unmonitored shared mailbox, with defined response-time and escalation thresholds. | Nkechi Obiora, Director of Human Resources | 21 days from report issuance |
| 4 | Define and document a minimum parallel testing standard for future system conversions (minimum cycle count, required line-item validation categories, sign-off criteria) and present to the Board Finance Committee for approval before any future payroll or financial system conversion. | Marcus Tillinghast, Chief Financial Officer | 45 days from report issuance |
| 5 | Reconcile the November 18 remediation run in full: confirm correct amounts for all 84 double-paid employees, correct overtime recalculation for all affected pay periods, and correct withholding for all affected employees, coordinating with payroll tax filing obligations. | Soren Bragg, Controller | 15 days from report issuance |
| 6 | Complete corrected W-2 issuance for all employees affected by the withholding errors identified in January, with individual written notice explaining the correction. | Soren Bragg, Controller, with Nkechi Obiora, Director of Human Resources | February 15, 2027 |
| 7 | Establish a written escalation protocol requiring executive leadership (CEO and CFO) be briefed within 48 hours of any payroll discrepancy affecting more than a defined threshold of employees or dollar amount. | Delphine Ouellette, Chief Executive Officer | 30 days from report issuance |
| 8 | Require a documented reconciliation sign-off (calculated-versus-disbursed comparison) as a mandatory step before approval of any off-cycle or correction payroll run, with sign-off separate from the approving executive. | Marcus Tillinghast, Chief Financial Officer | 21 days from report issuance |
| 9 | Review and, where warranted, issue restitution or goodwill adjustment for direct financial hardship incurred by affected employees (e.g., late fees, overdraft charges) resulting from the underpayment period, in coordination with Human Resources. | Marcus Tillinghast, Chief Financial Officer | 60 days from report issuance |
| 10 | Assess staffing coverage and supervision ratio contingency planning for group homes to reduce the speed with which payroll- or attrition-driven understaffing translates into licensing noncompliance; report findings and recommendations to the CEO. | Imelda Restrepo, Director of Residential Services | 45 days from report issuance |
| 11 | Cooperate fully with the Maine Department of Labor on the 22 filed wage complaints, including provision of records and timely response to inquiries, and track resolution status centrally. | Nkechi Obiora, Director of Human Resources | Ongoing; status report to CEO monthly until closed |
| 12 | Conduct exit interview analysis for the 38 DSPs who resigned between November 1 and December 15 to determine what proportion of departures were payroll-driven versus other factors, and report findings to inform retention planning. | Nkechi Obiora, Director of Human Resources | 30 days from report issuance |
| 13 | Present this postmortem and a remediation status update to the Board Finance Committee. | Delphine Ouellette, Chief Executive Officer | Next scheduled Board Finance Committee meeting |

---

## 8. Closing Notes

This incident began as a single migration defect — an omitted rate table — and became a compounding failure because detection was slow, diagnosis was misdirected, escalation lagged discovery, and remediation was executed without verification. Each of these stages involved a defensible decision made under real constraints: a grant deadline, a vacant role that had not yet been backfilled, a plausible initial hypothesis about time clocks, and pressure to correct three pay periods of underpayment as quickly as possible. None of those decisions, taken individually, was unreasonable. Taken together, and without the controls that would normally catch an error at each stage, they produced a nine-week-plus failure with direct financial harm to 610 employees, meaningful attrition among direct support staff, and licensing consequences for the people PBIN exists to serve.

The corrective path outlined above is intended to rebuild the controls that were missing or bypassed at each stage: migration validation, ticket ownership, diagnostic discipline, escalation speed, and remediation reconciliation. The organization's continued ability to serve 480 residents depends on a stable, adequately staffed direct care workforce; the staffing and licensing fallout from this incident is a direct reminder that payroll reliability in this operating environment is not a back-office concern but an operational and compliance one.

## Appendix A: Detailed Financial Reconciliation

The following reconciliation breaks down the $251,000 in aggregate underpayment and the $71,000 in aggregate overpayment by category, based on the analysis completed following the November 12 discovery of the missing rules table.

**Underpayment by pay period**

| Pay Period | Employees Affected | Missing Differential Pay | Missing Overtime Correction | Period Total |
|---|---|---|---|---|
| Oct 23 | 587 | $71,400 | $12,100 | $83,500 |
| Oct 30 | 594 | $68,900 | $13,600 | $82,500 |
| Nov 6 | 601 | $66,200 | $12,800 | $79,000 |
| Nov 13 (partial, corrected mid-cycle) | 203 | $4,900 | $1,100 | $6,000 |
| **Total** | **610 unique employees** | **$211,400** | **$39,600** | **$251,000** |

The employee count per period grew slightly across the three full pay periods, consistent with the staffing pattern shift as some employees picked up additional evening and overnight shifts to cover open positions during the same window in which those shifts were underpaid — a dynamic that was not identified until the exit interview analysis called for in Action Item 12.

**November 18 remediation errors by category**

| Error Type | Employees Affected | Dollar Impact |
|---|---|---|
| Duplicate payment of prior-period differential | 61 | $48,300 |
| Duplicate payment of overtime correction | 23 | $22,700 |
| Overtime miscalculation on corrected base (net understatement, separate from duplication) | 156 | Not fully quantified at time of report; included in Action Item 5 scope |
| Incorrect withholding on corrected amounts | 610 (all recipients of the Nov 18 run) | Deferred to January W-2 correction cycle |
| **Total confirmed overpayment** | **84 unique employees** | **$71,000** |

The overlap between the duplicate differential and duplicate overtime categories accounts for the 84 unique employees affected, as a portion of employees appear in both rows above. Action Item 5 requires full resolution of the unquantified overtime miscalculation figure and confirmation of final withholding corrections before this appendix can be closed.

**Net employee financial position**

Of the 610 originally underpaid employees, cross-referencing against the 84 double-paid employees shows that 79 individuals were present in both groups — meaning they were first underpaid across October and early November, then overpaid in the November 18 correction, in most cases due to the correction run failing to net against amounts already partially reconciled through informal manual adjustments some supervisors had begun making at the home level in early November. This overlap was not identified until the reconciliation effort supporting this report and is flagged for full resolution under Action Item 5, including individual-level statements to affected employees showing net position across the full incident period rather than period-by-period figures alone.

---

## Appendix B: Employee Communication Plan

Given the financial hardship documented in this incident, and the risk that unresolved confusion about pay contributed to the resignation rate observed between November 1 and December 15, the following communication plan accompanies the remediation timeline in Section 7.

**Phase 1 — Individual Notice (within 10 days of report issuance).** Every employee identified as underpaid, overpaid, or subject to withholding correction receives a written, individualized statement showing: amount owed or owed-back by pay period, the corrected amount, and a plain-language explanation of the error categories from Appendix A that apply to their case. This statement will be prepared jointly by Payroll (under Soren Bragg) and Human Resources (under Nkechi Obiora) and reviewed for clarity by a supervisor from each affected group home prior to distribution, given that many DSPs receiving these notices work variable schedules and may not have regular access to email.

**Phase 2 — Group Home Briefings (within 20 days of report issuance).** Residential Services, under Imelda Restrepo, will hold brief in-person briefings at each of the 62 group homes during shift overlap windows to explain the correction process, answer questions, and provide a direct contact for follow-up. This channel is intended to reach staff who may not engage with written communication alone and to rebuild trust following the extended period in which employees reported shortfalls without a clear response.

**Phase 3 — Standing Payroll Accuracy Contact (ongoing from report issuance).** Once the interim or permanent payroll manager role is filled under Action Item 1, that role becomes the standing point of contact for any pay discrepancy report, replacing the shared mailbox. This contact information will be included in the Phase 1 notice and posted at each group home.

**Phase 4 — Restitution Communication (concurrent with Action Item 9).** Where the CFO's office identifies hardship-related restitution eligible for goodwill adjustment, affected employees will be notified individually with a description of what is being provided and why, separate from the routine correction notice, to avoid conflating standard payroll correction with hardship remediation.

---

## Appendix C: Future Conversion Testing Standard (Draft, Supporting Action Item 4)

The following draft standard is provided as a starting point for the CFO's office in developing the formal policy due under Action Item 4.

1. **Minimum parallel cycle count.** No fewer than two full pay cycles shall be run in parallel between legacy and replacement systems for any conversion affecting hourly, differential, or overtime-eligible pay calculation. Reduction of this minimum requires documented sign-off from the CFO and the Board Finance Committee, with an explicit written risk acceptance.

2. **Line-item validation requirement.** Parallel testing sign-off shall require a category-by-category comparison — not an aggregate net-pay comparison alone — covering at minimum: base pay, all shift differential categories, overtime calculation, tax withholding, and benefits deductions. Aggregate net-pay matches can mask offsetting errors, as occurred in this incident where an omitted differential and an incorrect overtime base could plausibly have produced a net figure closer to correct than either component alone.

3. **Representative sampling by shift pattern.** Validation samples shall explicitly include employees on evening, overnight, and weekend schedules in proportion to their share of the workforce, rather than relying on a sample weighted toward standard day-shift employees, given that differential-eligible employees are disproportionately exposed to rate table defects.

4. **Named validation owner.** Each conversion shall have a single named individual accountable for confirming that all rate and rules tables — not limited to base pay tables — have been migrated and validated, with a checklist sign-off retained as part of the project record.

5. **Post-cutover monitoring window.** For the first two live pay cycles following any payroll system cutover, a named owner shall conduct a proactive review of a sample of paychecks against expected values, independent of whether complaints have been received, rather than relying solely on inbound employee reports to surface defects.

---

## Appendix D: Roles Referenced in This Report

| Name | Title | Role in Incident |
|---|---|---|
| Delphine Ouellette | Chief Executive Officer | Briefed on full incident scope November 14; accountable for Board reporting and organization-wide escalation protocol |
| Marcus Tillinghast | Chief Financial Officer | Approved November 18 remediation run; accountable for reconciliation control and testing standard |
| Soren Bragg | Controller | Absorbed informal payroll oversight during vacancy; led initial (misdirected) time clock investigation; accountable for configuration audit and reconciliation of remediation errors |
| Nkechi Obiora | Director of Human Resources | Identified missing rules table November 12; accountable for interim/permanent payroll manager staffing, ticket intake process, and employee communication |
| Imelda Restrepo | Director of Residential Services | Reported group homes below mandated supervision ratios; accountable for staffing contingency review |

This appendix is provided for reference only and does not expand the scope of individual accountability beyond the action items assigned in Section 7.

## Appendix E: State Licensing Citation Detail and Corrective Action Plan

The two licensing citations issued in December 2026 relate to supervision ratio violations at two group homes, identified internally by Imelda Restrepo prior to state review. This section documents the specific findings and the corrective action plan submitted to the state licensing authority, provided here for completeness of the incident record.

**Citation 1 — Group Home (Rockland service area).** State review found that on multiple overnight shifts between November 22 and December 8, the home operated with one direct support staff present against a mandated minimum of two for the resident census at that location. Internal scheduling records show the home lost two DSPs to resignation in the November 1–December 15 window and was unable to backfill overnight coverage from the internal per diem pool, which was itself depleted due to per diem staff picking up shifts at other understaffed homes across the same period.

**Citation 2 — Group Home (Belfast service area).** State review found a similar pattern on weekend day shifts between December 1 and December 12, with documented instances of one staff member covering a home requiring two under the residents' individual support plans. This home lost one DSP to resignation and had an additional DSP on approved leave during the cited period, leaving no margin for the vacancy.

**Corrective action plan submitted to the state.** Both homes have since returned to compliant staffing levels through a combination of overtime authorization for remaining staff (contributing to the $390,000 overtime increase documented in Section 2), temporary reassignment of staff from homes with more staffing margin, and expedited hiring for the two vacant positions. The state has requested a 90-day follow-up review at both locations to confirm sustained compliance, scheduled for March 2027. Imelda Restrepo is the named point of contact for this follow-up, consistent with her ownership of Action Item 10.

**Relationship to broader staffing risk.** Restrepo's review under Action Item 10 is expected to address not only these two cited homes but the broader question of how much staffing margin exists across all 62 homes relative to mandated ratios, so that future attrition — whether payroll-driven or otherwise — is less likely to convert into a licensing violation within the narrow multi-week window observed in this incident.

---

## Appendix F: Department of Labor Complaint Status

Twenty-two employees filed wage complaints with the Maine Department of Labor during December 2026. As of this report, these complaints remain open. The following status categories apply:

| Status | Count |
|---|---|
| Complaint filed, PBIN records requested by DOL | 22 |
| Records provided to DOL | 22 |
| DOL preliminary review in progress | 22 |
| Complaints resolved or closed | 0 |

Nkechi Obiora is the named point of contact for all 22 complaints under Action Item 11. Because the underlying underpayment amounts for these 22 individuals fall within the broader 610-employee reconciliation described in Appendix A, resolution of Action Item 5 (full reconciliation of amounts owed) is a prerequisite for closing out documentation requested by the DOL for each complaint. Monthly status updates to the CEO will track movement in the table above until all 22 complaints reach resolved or closed status.

It is possible that additional complaints could be filed by employees among the 610 affected who have not yet done so, particularly if individual notice under Appendix B Phase 1 surfaces discrepancies employees were previously unaware of. This risk is a factor in the priority assigned to Action Item 5 and to timely, accurate individual notice under the communication plan.

---

## Appendix G: Grant Deadline and Schedule Governance Review

Because the original decision to move the conversion date from July to October 2026 was driven by alignment with a grant reporting deadline rather than a payroll-readiness assessment, this appendix documents a brief review of that decision process for governance purposes, separate from the technical postmortem above.

**What the grant deadline required.** The grant in question required certain administrative systems, including payroll, to be operating on a compliant platform by a fixed reporting date in order to satisfy funder reporting requirements tied to the grant period. The October 2026 date was selected to provide a buffer before that reporting deadline.

**What was not assessed at the time of the schedule change.** The record available to this postmortem indicates that the decision to compress parallel testing from two cycles to one was made to preserve the October date once it was set, rather than the October date being validated against the minimum testing timeline the project team believed necessary. In other words, the schedule was fixed first, and the testing scope was reduced to fit it, rather than the testing scope being held fixed and the schedule adjusted around it.

**Governance gap.** No documentation reviewed for this postmortem indicates that the decision to reduce parallel testing from two cycles to one was escalated to the Board Finance Committee as a risk acceptance, despite this being a change to a control directly protecting employee pay accuracy for a workforce of 740 people. Action Item 4's testing standard, once adopted, is intended to close this gap by requiring explicit Board-level risk acceptance for any future reduction below the two-cycle minimum.

**Relationship to grant compliance itself.** It is worth noting for the record that the underlying grant's administrative system requirement was about platform compliance and reporting capability, not about the specific cutover date of October 23. A later go-live date within the same grant period, had it been assessed as necessary to preserve full parallel testing, would likely still have satisfied the grant's underlying requirement. This suggests the schedule compression was a self-imposed constraint based on an assumed deadline rigidity that was not independently verified against the grant terms themselves at the time the decision was made.

---

## Appendix H: Report Approval Log

| Reviewer | Role | Section(s) Reviewed | Date |
|---|---|---|---|
| Delphine Ouellette | Chief Executive Officer | Full report | Pending Board Finance Committee presentation |
| Marcus Tillinghast | Chief Financial Officer | Sections 2, 3, 5, 7; Appendices A, G | Pending |
| Nkechi Obiora | Director of Human Resources | Sections 1, 3, 6, 7; Appendices B, F | Pending |
| Soren Bragg | Controller | Sections 3, 4, 5, 7; Appendix A | Pending |
| Imelda Restrepo | Director of Residential Services | Sections 2, 6, 7; Appendix E | Pending |

This report is considered final for distribution purposes upon completion of the approval log above and presentation to the Board Finance Committee as required under Action Item 13. Subsequent updates to open action items will be tracked separately in the organization's incident action item log rather than through revision of this document.

## Appendix I: Harborworks Vendor Engagement Review

Although this postmortem's root cause is internal — a migration and testing failure within PBIN's control — the vendor relationship with Harborworks played a role in both the original defect and the pace of remediation, and is documented here for completeness.

**Migration responsibility.** Under the implementation agreement, data migration mapping (including rate and rules tables) was a shared responsibility: Harborworks provided the migration tooling and technical support, while PBIN's project team, coordinated informally by the controller's office in the absence of a payroll manager, was responsible for validating that all source tables had a corresponding destination configuration. No individual on the PBIN side held migration validation as a primary job function at the time of cutover, consistent with the staffing gap described in Section 5.

**Vendor support during detection.** Harborworks' support channel was not engaged until after Nkechi Obiora identified the missing rules table on November 12. Retrospective review indicates that PBIN's support ticket history with Harborworks contains no inquiries related to shift differential or overtime calculation between October 23 and November 12, meaning the vendor was not in a position to assist with diagnosis during the period when the internal investigation was focused on time clock hardware rather than the payroll platform itself.

**Vendor support during remediation.** Harborworks support was engaged in preparing the November 18 off-cycle run. The vendor's role in that engagement was limited to processing the correction data provided by PBIN; the reconciliation gap that produced the double-payment and withholding errors originated in PBIN's internal approval process rather than in vendor-side execution, consistent with Section 5's identification of the missing reconciliation control as an internal gap.

**Recommendation for vendor relationship going forward.** As part of Action Item 2's configuration audit, Soren Bragg's review will include confirmation with Harborworks that all rate and rules tables in the current production environment match an agreed source-of-truth document, and will establish a standing quarterly reconciliation check between PBIN and Harborworks for rate table accuracy, independent of any future conversion event.

---

## Appendix J: Interim Manual Controls (November 12–18)

Between the identification of the missing rules table on November 12 and the off-cycle remediation run on November 18, several group home supervisors began making informal manual adjustments to employee pay estimates at the local level, referenced in Appendix A's discussion of the overlap between underpaid and later double-paid employees. This appendix documents that interim period for the record.

**What occurred.** In the absence of a corrected payroll run, at least a subset of the 62 group homes had supervisors independently calculating estimated owed differential and overtime amounts and, in a small number of cases, authorizing informal advances or schedule adjustments to offset the shortfall for individual employees experiencing acute hardship. These actions were not centrally coordinated, tracked, or communicated to the payroll or finance function preparing the November 18 correction run.

**Why this matters to the reconciliation.** Because these local adjustments were not visible to the team preparing the November 18 remediation, the correction run calculated owed amounts based solely on the original payroll records without accounting for any informal adjustments already made at the home level. This is the most likely explanation for a portion of the 79-employee overlap identified in Appendix A between the underpaid and double-paid groups.

**Going forward.** Action Item 3's intake and triage process is intended to also capture and centralize any future informal or local-level payroll adjustments made in response to an active payroll incident, so that any subsequent formal remediation run has full visibility into amounts already adjusted outside the standard payroll system. Supervisors will be included in the Phase 2 group home briefings described in Appendix B in part to communicate this expectation for future incidents.

---

## Appendix K: Document Control and Distribution

**Document owner:** Office of the Chief Financial Officer, Penobscot Bay Independence Network

**Distribution list:**
- Chief Executive Officer
- Chief Financial Officer
- Controller
- Director of Human Resources
- Director of Residential Services
- Board Finance Committee (upon scheduled presentation per Action Item 13)

**Retention:** This report and its appendices are to be retained as part of PBIN's permanent incident record and made available to the Maine Department of Labor and state licensing authority upon request in connection with the open matters described in Appendices E and F.

**Revision history:**

| Version | Date Prepared | Description |
|---|---|---|
| Draft 1.0 | — | Initial postmortem: summary, impact, timeline, root cause, contributing factors, response assessment, action items |
| Draft 1.1 | — | Added Appendices A–D: financial reconciliation, employee communication plan, future testing standard, roles reference |
| Draft 1.2 | — | Added Appendices E–H: licensing citation detail, DOL complaint status, schedule governance review, approval log |
| Draft 1.3 | — | Added Appendices I–K: vendor engagement review, interim manual controls, document control |

Further additions to this document, if any, will be appended in subsequent sections rather than through modification of the sections above, to preserve the integrity of the original incident record as reviewed and approved per Appendix H.
