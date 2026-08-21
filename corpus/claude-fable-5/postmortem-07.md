# Incident Postmortem: Harborworks Payroll Conversion Failure

**Penobscot Bay Independence Network**
**Incident Reference:** PBIN-2026-011
**Document Status:** Final
**Date Issued:** August 9, 2026 (Draft) — Final Revision Approved for Distribution
**Prepared for:** Executive Leadership Team, Board Finance Committee, Board Quality & Compliance Committee
**Classification:** Internal — Blameless Postmortem
**Review Facilitator:** Director of Human Resources, with Finance and Residential Services participation

---

## 1. Purpose and Ground Rules

This postmortem documents the failure of the October 2026 payroll conversion to the Harborworks platform, the three-pay-period underpayment of shift differentials and overtime that followed, the flawed remediation of November 18, and the downstream staffing, financial, and licensing consequences that extended into January 2027.

This document follows Penobscot Bay Independence Network's blameless postmortem standard. Individuals are named only to establish the factual sequence of events and to assign forward-looking action items. The analysis examines systems, decision structures, incentives, and process gaps — not personal fault. Every decision described here was made by a reasonable person acting on the information available to them at the time, under real constraints. The purpose of this document is to change the conditions that made those decisions insufficient, so that the same conditions do not produce the same outcome again.

Penobscot Bay Independence Network (PBIN) serves 480 adults with developmental disabilities across 62 group homes in midcoast Maine. The organization employs 740 people, the majority of whom are direct support professionals (DSPs) earning $19 to $23 per hour. For this workforce, a payroll shortfall averaging $412 is not an accounting abstraction. It is a missed rent payment, a skipped car repair, a reason to take a job somewhere else. The severity assessment in this document reflects that reality.

---

## 2. Executive Summary

In October 2026, PBIN converted its payroll processing from its legacy system to the Harborworks platform. The conversion had originally been scheduled for July 2026 but was moved to October to align spending with a grant deadline. To hold the new date, parallel testing — running the old and new systems side by side and comparing outputs — was compressed from two pay cycles to one.

During data migration, the shift differential and overtime rules table failed to transfer to Harborworks. This table governed evening, overnight, and weekend differentials worth $1.50 to $3.25 per hour, and it drove the calculation of overtime on the differential-inflated rate rather than base rate alone. The single parallel test cycle did not surface the omission. The first affected paycheck issued October 23, 2026.

Employees reported shortfalls within one day. However, the payroll manager position had been vacant since August, and employee reports accumulated in an unmonitored shared mailbox. When the volume of complaints reached the Controller, the initial diagnosis focused on the time clock system — a hypothesis that the clocks were dropping shift codes at the punch level. Nine days of punch-data auditing followed before that hypothesis was ruled out. The Director of Human Resources identified the true cause — the missing rules table — on November 12, after three pay periods had processed incorrectly.

The remediation compounded the harm. An off-cycle correction run cut on November 18, approved without reconciliation against source records, double-paid 84 employees a combined $71,000, omitted the overtime recalculation entirely, and applied incorrect tax withholding that required W-2 corrections in January 2027.

The organizational consequences were severe. Six hundred ten employees were underpaid a combined $251,000. Thirty-eight direct support professionals resigned between November 1 and December 15. Overtime spending rose $390,000 in six weeks as remaining staff covered vacancies. Two group homes fell below state-mandated supervision ratios, drawing two state licensing citations in December. Twenty-two employees filed a wage complaint with the Maine Department of Labor.

The root cause was a data migration verification gap: no control existed to confirm that all configuration tables — not just employee records and pay rates — transferred and functioned in the new system. Six contributing factors turned that gap into an eleven-week organizational crisis: the compressed timeline, the truncated parallel test, the vacant payroll manager role, the unowned intake channel for employee reports, an unvalidated diagnostic hypothesis that consumed nine days, and a remediation executed without reconciliation controls.

This document closes with fourteen action items, each with a named owner and due date.

---

## 3. Impact Statement

All figures below are verified against payroll records, general ledger entries, HR separation records, and state correspondence as of the date of this document.

### 3.1 Direct Financial Impact on Employees

| Measure | Value |
|---|---|
| Employees underpaid | 610 |
| Total underpayment (differentials and overtime) | $251,000 |
| Average underpayment per affected employee | $412 |
| Pay periods affected before detection | 3 (checks of Oct 23, Nov 6, Nov 20 cycle exposure) |
| Differential rates that failed to pay | $1.50 – $3.25/hour (evening, overnight, weekend) |
| Overtime miscalculation | Computed on base rate only, excluding differentials from the regular rate |

### 3.2 Remediation Errors

| Measure | Value |
|---|---|
| Employees double-paid in November 18 off-cycle run | 84 |
| Total overpayment | $71,000 |
| Overtime recalculation included in Nov 18 run | No — omitted entirely |
| Withholding errors | Yes — incorrect tax withholding on off-cycle checks |
| W-2 corrections required | Yes — issued January 2027 |

### 3.3 Workforce Impact

| Measure | Value |
|---|---|
| DSP resignations, Nov 1 – Dec 15, 2026 | 38 |
| Incremental overtime cost over six weeks | $390,000 |
| Estimated replacement cost (recruiting, onboarding, training at ~$4,500/DSP) | ~$171,000 |

For context, PBIN's trailing average DSP attrition over a comparable six-week window is 9 to 12 separations. The 38 resignations represent roughly three to four times baseline turnover. Exit interviews and resignation letters cited pay errors, the slow correction, or both in 31 of the 38 cases.

### 3.4 Regulatory and Compliance Impact

| Measure | Value |
|---|---|
| Group homes below mandated supervision ratios | 2 |
| State licensing citations issued (December 2026) | 2 |
| Wage complaint filed with Maine Department of Labor | 1 complaint, 22 employee complainants |
| Potential statutory exposure | Liquidated damages, penalties, and interest under Maine wage payment law (under review with outside counsel) |

### 3.5 Aggregate Financial Exposure

| Category | Amount |
|---|---|
| Employee underpayment (owed and remediated) | $251,000 |
| Overpayment at risk of non-recovery | up to $71,000 |
| Incremental overtime | $390,000 |
| Estimated turnover replacement cost | ~$171,000 |
| W-2 correction processing, filing, and outside accounting support | ~$18,000 (estimated) |
| Regulatory penalties and legal costs | Undetermined |
| **Identified exposure to date** | **~$901,000, excluding regulatory outcomes** |

### 3.6 Non-Quantified Impact

- Erosion of workforce trust in payroll accuracy, evidenced by a sustained increase in manual paycheck verification requests through January.
- Supervisory and administrative time diverted to complaint handling, manual calculations, and state response — conservatively several hundred staff hours.
- Reputational impact in a regional labor market where PBIN competes for a scarce DSP workforce.
- Stress on residents in the two homes cited for ratio violations, where shift coverage relied heavily on unfamiliar float and overtime staff.

---

## 4. Background

### 4.1 The Legacy Environment

PBIN's legacy payroll system had been in place for eleven years. Its shift differential and overtime configuration was mature and stable: evening differentials of $1.50/hour, overnight differentials of $2.75/hour, and weekend differentials ranging to $3.25/hour, layered by shift code at the timekeeping level and consumed by the payroll engine as a rules table. Overtime was calculated on the regular rate inclusive of differentials, consistent with federal and state wage law. Because the configuration had been stable for years, institutional knowledge of *how* it worked was concentrated in the payroll manager role — and largely undocumented outside it.

### 4.2 The Conversion Decision

The move to Harborworks was approved in early 2026 to replace an end-of-life system, with go-live planned for July 2026 — a deliberately quiet period between fiscal-year close and fall program expansion. In the second quarter, Finance identified that a grant funding the conversion carried a spending and reporting deadline that the July schedule would strain. To keep the grant intact, go-live moved to October 2026. This decision was financially rational in isolation: losing the grant would have forced the conversion cost onto unrestricted operating funds in a tight budget year.

The schedule change had two second-order effects that were not fully weighed:

1. **Parallel testing was cut from two pay cycles to one** to fit the compressed implementation window while still meeting the grant milestone.
2. **The conversion now landed in October**, a period of high scheduling complexity — fall shift bids, holiday scheduling preparation, and elevated overtime — meaning the first live payrolls were among the year's most differential-heavy.

### 4.3 The Vacant Payroll Manager Role

The payroll manager resigned in August 2026, two months before go-live. The position was posted but unfilled at conversion. The role's responsibilities were split as an interim measure: the Controller absorbed processing oversight, and a payroll specialist handled transactional work. Two critical functions fell into the gap:

- **Monitoring the payroll shared mailbox**, the designated intake channel for employee pay questions.
- **Conversion validation from the practitioner's perspective** — the person most likely to look at a parallel-test output and notice that differential lines were absent was the person who had just left.

No single individual owned the question "does the new system pay differentials correctly?" at go-live.

---

## 5. Timeline

All times are Eastern. Dates are 2026 unless noted.

**Early Q2** — Grant deadline analysis prompts decision to move Harborworks go-live from July to October. Parallel testing scope reduced from two pay cycles to one to hold the new date.

**August (mid-month)** — Payroll manager resigns. Position posted; duties split between Controller Soren Bragg and a payroll specialist as an interim arrangement.

**Late September** — Data migration executed by the implementation vendor and internal team. Employee master data, base pay rates, deductions, and tax setup migrate and validate. The shift differential and overtime rules table does not migrate. No migration completeness checklist enumerates configuration tables individually, so the omission is not flagged.

**Early October** — Single parallel test cycle runs. Comparison focuses on headcount, gross pay totals at the batch level, and net pay spot checks. Aggregate variances fall within the tolerance the team had set. The differential-specific line items are not compared pay-code by pay-code. The test is signed off.

**Mid-October** — Harborworks go-live. Legacy system decommissioned to read-only.

**Friday, October 23** — First live paycheck issues. Evening, overnight, and weekend differentials absent; overtime paid on base rate only. Six hundred ten employees are underpaid on this and subsequent checks.

**Saturday, October 24 – Monday, October 26** — Employees begin reporting shortfalls, primarily via the payroll shared mailbox and through residential supervisors. With the payroll manager role vacant, the mailbox is effectively unmonitored. Tickets accumulate without acknowledgment, triage, or escalation.

**Wednesday, October 28** — Volume of supervisor escalations reaches Controller Soren Bragg. Bragg reviews a sample of complaints and forms the hypothesis that the time clock system is dropping shift codes at the punch level — a known failure mode from a minor incident two years prior. Bragg initiates a punch-data audit.

**October 29 – November 6** — Nine-day punch-data audit. The audit examines clock exports, shift code assignments, and interface files between timekeeping and Harborworks. The data consistently shows shift codes present and correct in the punch data. The hypothesis is not formally re-examined during this period; the audit continues on the assumption that the fault is intermittent.

**Friday, November 6** — Second affected paycheck issues. Complaint volume roughly doubles. Several employees report the issue to supervisors as a reason they are seeking other employment.

**Monday, November 9 – Wednesday, November 11** — Director of Human Resources Nkechi Obiora, responding to escalations from Director of Residential Services Imelda Restrepo about pay-driven resignation threats, begins an independent review. Obiora traces a single employee's pay from punch to gross pay line by line and observes that shift codes arrive in Harborworks correctly but generate no differential earnings — indicating the failure is inside the payroll engine's configuration, not the clocks.

**Thursday, November 12, approximately 2:00 p.m.** — Obiora, working with the Harborworks vendor support team, confirms the shift differential and overtime rules table is absent from the production configuration. Root cause identified. Three pay periods have been affected.

**Thursday, November 12, evening** — Bragg and Obiora brief CFO Marcus Tillinghast. Decision made to (a) restore the rules table before the next regular cycle and (b) issue off-cycle correction checks as fast as possible, given mounting resignations.

**Saturday, November 14** — CEO Delphine Ouellette is briefed on the full scope for the first time — three weeks after the first bad check. Ouellette directs an all-staff communication, which issues November 16, acknowledging the error and committing to correction by November 18.

**Monday, November 16 – Tuesday, November 17** — Rules table rebuilt in Harborworks from legacy documentation and vendor records. Correction amounts calculated under time pressure, partly by manual spreadsheet, partly by a vendor-run retroactive utility. The two methods overlap for a subset of employees. The November 18 date, publicly committed, becomes a hard deadline.

**Wednesday, November 18** — Off-cycle correction run executes. CFO Tillinghast approves the run without a reconciliation of the correction file against source underpayment calculations, in order to hold the committed date. The run: double-pays 84 employees $71,000 (the spreadsheet/utility overlap); omits the overtime recalculation entirely (the retroactive utility corrected differential pay codes but was not configured to recompute the regular rate for overtime); and applies incorrect withholding (off-cycle checks taxed under wrong supplemental settings).

**November 19 – 25** — Overpayments and continued overtime shortfalls surface within days. Trust in the correction erodes; several employees who received accurate corrections request manual verification anyway.

**December 1 – 15** — Resignation total reaches 38 DSPs since November 1. Overtime spending accelerates. Restrepo reports two homes below mandated supervision ratios despite float coverage and mandatory overtime.

**December (mid-month)** — State licensing conducts visits; issues two citations for supervision ratio violations at the two homes.

**December (mid-to-late month)** — Twenty-two employees file a wage complaint with the Maine Department of Labor covering the underpayment period and the delayed correction.

**Late December** — Second remediation run, this time with full reconciliation: overtime recalculated on the correct regular rate for all three affected periods plus the November 18 gap; overpayment repayment plans offered to the 84 double-paid employees on voluntary schedules compliant with state wage deduction law.

**January 2027** — Corrected W-2s issued to employees affected by the November 18 withholding errors. Department of Labor response submitted with full accounting of amounts owed and paid. Payroll manager position filled.

**Elapsed time, first bad check to root cause identification:** 20 days.
**Elapsed time, first bad check to complete and accurate remediation:** approximately 9 weeks.

---

## 6. Root Cause

**The shift differential and overtime rules table was not migrated to Harborworks, and no verification control existed that would have detected its absence before, during, or immediately after go-live.**

Stated as a systems failure rather than an event: PBIN's conversion plan treated data migration as primarily an *employee-record* problem — names, rates, deductions, taxes — and validated it at that level. Configuration tables that transform inputs into pay (differential rules, overtime calculation logic, accrual rules) were not enumerated as discrete migration items with individual sign-offs. The rules table's absence was therefore invisible to every checkpoint the plan contained:

- The **migration checklist** did not list configuration tables individually, so nothing was marked incomplete.
- The **single parallel test** compared aggregate gross pay within a tolerance band. Differentials represent a modest share of total gross across 740 employees; their complete absence produced a variance that read as acceptable at the batch level. A pay-code-level comparison would have shown differential earnings at zero — an unmissable signal — but no pay-code-level comparison was performed.
- **Post-go-live monitoring** contained no automated check comparing pay-code distributions against historical baselines.

Three independent layers of defense — checklist, parallel test, monitoring — all failed for the same underlying reason: none was designed to ask, "is every rule that existed in the old system present and firing in the new one?"

---

## 7. Contributing Factors

The root cause explains why the error occurred. The following six factors explain why it persisted for three pay periods, why remediation failed, and why the organizational damage was as large as it was. They are ordered roughly by sequence, not severity.

### 7.1 Compressed Timeline Driven by Grant Deadline

Moving go-live from July to October to preserve grant funding was a defensible financial decision made without a structured assessment of implementation risk. No one asked the project team to quantify what the schedule compression would cost in testing coverage, or to present the executive team with the tradeoff explicitly ("we keep the grant, and we accept a single parallel cycle — here is what a single cycle cannot catch"). The grant deadline functioned as an unexamined constraint rather than one input to a risk-weighted decision. Additionally, the October date placed go-live in one of the most differential-intensive periods of the year, maximizing both the probability that a differential error would occur and the harm when it did — though, notably, *not* maximizing the chance of detection, because the detection controls were aggregate-based.

### 7.2 Parallel Testing Cut to One Cycle, and Shallow at That

The reduction from two cycles to one was the direct casualty of the schedule change, but the deeper problem was test *design*, not test *quantity*. Even one cycle would have caught the missing table if the comparison had been performed at the pay-code level. The test plan specified batch-total comparison within tolerance — a design that could and did pass while an entire earnings category was missing. A second cycle with the same design would likely have passed too. The lesson is that the test's acceptance criteria were never reviewed by anyone with deep knowledge of the pay structure — a gap tied directly to factor 7.3.

### 7.3 Vacant Payroll Manager Role at Go-Live

The payroll manager resigned two months before conversion, and the organization proceeded to go-live without either filling the role or formally reassigning its conversion-critical functions. The consequences ran through the entire incident:

- No practitioner-level review of migration completeness or parallel-test design.
- No owner for the payroll shared mailbox, the primary employee intake channel.
- No one whose daily work would have surfaced the anomaly on October 23 within hours rather than weeks.

The interim split of duties between the Controller and a payroll specialist covered transactional processing but left the *judgment* functions of the role unassigned. The organization treated the vacancy as a staffing inconvenience rather than a go-live risk requiring explicit mitigation or a go/no-go discussion.

### 7.4 Unowned Intake Channel Delayed Escalation by Five Days

Employees did their part: reports began within one day of the October 23 check. Those reports went where employees had been told to send them — the payroll shared mailbox — and sat unread. The signal reached decision-makers only when supervisors escalated verbally, five days later. There was no service-level expectation for acknowledging pay complaints, no auto-escalation for complaint volume spikes, and no backup owner designated when the mailbox's owner departed in August. The organization's fastest and most reliable error-detection system — its own employees — was connected to a dead channel.

### 7.5 Nine-Day Diagnostic Anchor on the Time Clock Hypothesis

When the Controller engaged on October 28, he formed a reasonable initial hypothesis based on a prior incident: the clocks were dropping shift codes. The failure was not the hypothesis but the process around it. The audit ran nine days without a checkpoint to ask whether the accumulating evidence (shift codes consistently present and correct in punch data) had falsified the theory. No differential diagnosis was performed — no structured enumeration of the other places in the chain where differentials could fail (interface, mapping, payroll engine configuration). A single end-to-end trace of one employee's pay, from punch to gross line — the exercise HR performed on November 9–11 — would have localized the fault in hours. During the nine days, a second bad payroll issued, doubling employee harm and complaint volume. This is a classic anchoring pattern, and the corrective is procedural: time-boxed hypotheses, mandatory end-to-end tracing early, and a rule that pay-impacting incidents affecting a broad population trigger cross-functional diagnosis rather than single-department investigation.

### 7.6 Remediation Executed Without Reconciliation Controls

The November 18 off-cycle run was scoped, calculated, and executed in roughly four business days under a publicly committed deadline. Three control failures converged:

- **Dual calculation methods without deduplication.** Manual spreadsheets and the vendor's retroactive utility both generated corrections for an overlapping subset of employees; no reconciliation step compared the combined output against a single source-of-truth underpayment file. Result: 84 double payments, $71,000.
- **Incomplete scope definition.** The correction was defined as "pay the missing differentials." The overtime recalculation — recomputing the regular rate with differentials included and paying the difference — was a distinct calculation that the vendor utility did not perform and the spreadsheet work did not cover. No one signed off on a scope document enumerating every component of the underpayment.
- **Approval without verification.** The CFO approved the run to hold the November 18 commitment, without a reconciliation report. The public commitment, made to rebuild trust, became a deadline that overrode the controls that would have protected trust. The December remediation — done with full reconciliation — took longer and was correct, demonstrating that the capability existed and the November failure was a process choice under pressure, not a capability gap.

The withholding errors flowed from the same haste: off-cycle runs required supplemental tax configuration that was not verified before execution, converting a November payroll error into a January tax-document problem touching hundreds of employees.

### 7.7 Late Executive Visibility (Cross-Cutting)

The CEO learned the scope on November 14 — twenty-two days after the first bad check and two days after root cause was found. No escalation threshold existed defining when a payroll or employee-impact event must reach the executive team. Earlier executive visibility would likely have accelerated cross-functional diagnosis (breaking the anchor described in 7.5), triggered earlier employee communication (mitigating the trust damage that drove resignations), and brought scrutiny to the remediation plan before execution.

---

## 8. What Worked

An honest postmortem records the strengths to preserve, not only the failures to fix.

1. **Employees detected the error within 24 hours.** The workforce noticed, checked their math, and reported through the designated channel immediately. Detection was never the problem; intake and escalation were. Any redesign should build on this demonstrated vigilance rather than replace it.

2. **Supervisor escalation functioned as an effective backup channel.** When the mailbox failed, residential supervisors carried the signal to leadership within five days. Informal, but it worked, and it should be formalized rather than left to chance.

3. **HR's end-to-end trace methodology found root cause quickly once applied.** The line-by-line trace of a single employee's pay from punch to gross localized the fault in under three days. This technique should be codified as the standard first diagnostic step for any pay-accuracy incident.

4. **The rules table rebuild was fast and accurate.** Once identified, the configuration was reconstructed from legacy documentation and vendor records in two days, and regular payroll cycles from that point forward paid differentials correctly. The technical fix held.

5. **The November 16 all-staff communication was direct and honest.** It acknowledged the error plainly, took organizational responsibility, and committed to a correction date. The communication itself was well received; the failure was that the operational execution behind the commitment did not match it.

6. **The December remediation demonstrated the correct model.** Full reconciliation against a single source-of-truth file, complete scope including overtime recalculation, verified tax treatment, and lawful voluntary repayment plans for overpaid employees. This run should be treated as the template for any future correction.

7. **Residential Services surfaced the ratio risk proactively.** The Director of Residential Services flagged the supervision ratio exposure internally before the state visits, enabling at least partial mitigation through float staffing and giving leadership accurate information for the regulatory response.

8. **Legacy system retained in read-only mode.** The decision to keep the old system accessible rather than fully decommissioning it made both the diagnosis and the rules table reconstruction dramatically faster than they would otherwise have been.

---

## 9. What Did Not Work

1. **Migration validation stopped at employee records.** Configuration — the logic that turns hours into pay — was never enumerated, migrated with individual sign-off, or verified.

2. **The parallel test's acceptance criteria could not detect a missing earnings category.** Batch-level tolerance comparison passed while an entire class of pay was absent. Test depth, not just test duration, was inadequate.

3. **The primary employee intake channel was unowned for weeks.** Five days of clear, actionable employee reports went unread during the most critical detection window.

4. **Diagnosis anchored on a prior incident's pattern for nine days** without falsification checkpoints or a structured differential diagnosis, during which a second incorrect payroll issued.

5. **The go-live proceeded with a known critical vacancy and no formal risk acceptance.** No go/no-go review weighed the payroll manager vacancy as a conversion risk.

6. **The remediation deadline overrode remediation controls.** A commitment made to restore trust drove the omission of the reconciliation that would have protected it, producing $71,000 in overpayments, a missed overtime component, and W-2 corrections.

7. **No executive escalation threshold existed for employee-impact incidents.** A 610-employee pay error ran for three weeks before the CEO knew its scope.

8. **The correction's scope was never formally defined and signed off.** "Fix the differentials" and "fix the underpayment" were treated as synonymous; the overtime component fell through the gap.

9. **The staffing consequence was foreseeable and unmodeled.** No one connected sustained pay errors in a $19–$23/hour workforce to resignation risk, coverage gaps, and licensing exposure until resignations were underway. The link between payroll accuracy and regulatory compliance in a ratio-mandated care environment was not part of anyone's incident severity assessment.

---

## 10. Action Items

Each action has a single accountable owner. Owners may delegate execution but not accountability. Status will be reviewed monthly by the executive team until all items close; the Board Finance Committee will receive a quarterly summary.

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | Complete final remediation audit: confirm every affected employee's underpayment (differentials and overtime, all periods) is fully paid; reconcile against source-of-truth file; publish confirmation to each affected employee. | Marcus Tillinghast, CFO | Sept 30, 2026* |
| 2 | Complete overpayment recovery program for the 84 double-paid employees via voluntary, wage-law-compliant repayment plans; write off amounts where recovery cost exceeds value; report net recovery to the Board Finance Committee. | Soren Bragg, Controller | Dec 31, 2026 |
| 3 | Fill the payroll manager position; until filled, formally reassign each function of the role (including intake channel ownership and configuration change review) in writing to named individuals. | Nkechi Obiora, Director of HR | Oct 31, 2026 |
| 4 | Establish payroll intake service levels: 1-business-day acknowledgment, 3-business-day substantive response, automatic escalation to Controller and HR Director when complaint volume exceeds 10 in any 48-hour window; designate a permanent backup mailbox owner. | Nkechi Obiora, Director of HR | Oct 15, 2026 |
| 5 | Implement automated pay-code baseline monitoring: every payroll run compared against a trailing 6-cycle baseline by pay code; any earnings category varying more than 15% (or dropping to zero) blocks finalization pending review. | Soren Bragg, Controller | Nov 30, 2026 |
| 6 | Create a system-conversion configuration inventory standard: all future migrations must enumerate every configuration table and rule set as a discrete migration item with individual verification sign-off; apply retroactively to audit the full Harborworks configuration against legacy. | Marcus Tillinghast, CFO | Dec 31, 2026 |
| 7 | Rewrite parallel-testing standards: minimum two full cycles for any pay-impacting system change; comparison at the pay-code level per employee, not batch tolerance; test plan acceptance criteria reviewed and signed by the payroll manager (or formally designated practitioner) and HR Director. | Marcus Tillinghast, CFO | Dec 31, 2026 |
| 8 | Adopt a payroll incident diagnostic protocol: any pay-accuracy incident affecting more than 25 employees triggers (a) an end-to-end single-employee trace within 48 hours, (b) a cross-functional team (Finance, HR, IT/vendor), and (c) time-boxed hypotheses with mandatory 72-hour falsification checkpoints. | Nkechi Obiora, Director of HR | Nov 15, 2026 |
| 9 | Establish an executive escalation threshold: any incident affecting the pay of more than 50 employees, or any incident with potential licensing impact, must be reported to the CEO within 2 business days of identification. | Delphine Ouellette, CEO | Oct 15, 2026 |
| 10 | Implement off-cycle payroll run controls: no off-cycle or correction run executes without (a) a written scope document enumerating all pay components, (b) reconciliation of the run file against a single source-of-truth calculation, and (c) verified tax configuration — each signed before approval. Deadline commitments to staff may not be made before the scope document exists. | Marcus Tillinghast, CFO | Nov 30, 2026 |
| 11 | Complete and verify all W-2 corrections from the November 18 run; provide affected employees with plain-language explanation and a contact for tax questions; fund reasonable tax-preparation cost reimbursement for affected employees. | Soren Bragg, Controller | Jan 31, 2027 |
| 12 | Deliver corrective action plans for the two cited homes to state licensing; implement staffing stabilization for ratio-vulnerable homes, including a contingency float pool sized against a defined attrition trigger; report ratio compliance weekly to the CEO until both citations are resolved. | Imelda Restrepo, Director of Residential Services | Jan 31, 2027 |
| 13 | Manage the Department of Labor complaint response to closure with outside counsel: full accounting of amounts owed and paid, cooperation with any audit, and payment of any assessed penalties without contest where the underpayment is undisputed. | Marcus Tillinghast, CFO | Ongoing; status monthly to Board until closed |
| 14 | Add a go/no-go gate to all future major system implementations: a formal review 30 days before go-live assessing staffing readiness (including key vacancies), testing completeness, and rollback capability, with documented executive risk acceptance required to proceed past any red condition. Grant or funding deadlines must be presented alongside implementation risk in the same decision document. | Delphine Ouellette, CEO | Feb 28, 2027 |

*Item 1 reflects completion verification of remediation payments largely executed in the December 2026 correction run; the audit confirms completeness.

---

## 11. Lessons Learned

Five lessons generalize beyond this incident and should inform decision-making across the organization.

**1. Funding deadlines are inputs to risk decisions, not overrides of them.** The grant deadline was real and the money mattered. But the schedule decision was made as if implementation risk were fixed, when in fact the compression converted a recoverable funding problem into a $900,000 operational crisis with regulatory consequences. Future decisions of this kind must put the funding benefit and the implementation risk in the same document, in front of the same decision-makers, at the same time.

**2. Testing catches what it is designed to catch, and nothing else.** The parallel test passed. It was designed to pass under exactly these conditions. Test coverage must be evaluated against the question "what failure modes would this test miss?" — and reviewed by the people who know the system's edge cases best.

**3. A vacancy in a control role is a control failure in waiting.** The payroll manager vacancy did not cause the migration error, but it disabled the three mechanisms most likely to catch it: expert review of the test design, ownership of the intake channel, and daily practitioner scrutiny of output. Key-role vacancies must be treated as material risks in any go/no-go decision.

**4. In hourly-wage care work, payroll accuracy is a safety and compliance system.** The causal chain from a missing rules table to state licensing citations ran through the paychecks of people earning $19 to $23 an hour who had other options. Payroll incidents in this organization must be severity-assessed for resident-care impact from the first hour, not treated as back-office matters.

**5. A correction executed without controls is a second incident, not a remedy.** The pressure to fix things fast — amplified by a public commitment — produced a remediation that damaged trust more than the original error, because employees can forgive a mistake more readily than a botched apology. The December run proved the organization could remediate correctly. The standard going forward is simple: no correction ships without reconciliation, complete scope sign-off, and verified tax treatment, regardless of deadline.

---

## 12. Document Control

| Field | Detail |
|---|---|
| Distribution | Executive Leadership Team; Board Finance Committee; Board Quality & Compliance Committee; action item owners |
| Retention | Permanent — organizational incident record |
| Follow-up review | Action item status reviewed monthly at executive team meeting; formal 6-month effectiveness review of implemented controls scheduled for Q1 2027 close |
| Related records | Payroll remediation reconciliation files; Maine DOL complaint correspondence; state licensing citation and corrective action plans; Harborworks vendor incident report; W-2 correction filings |

*This postmortem was prepared under PBIN's blameless review standard. Its findings concern systems, processes, and decision structures. It is not a disciplinary document and may not be used as the basis for individual personnel action.*

---

## Appendix A: Detailed Remediation Accounting

### A.1 Underpayment by Component and Pay Period

The following breakdown reconciles the $251,000 total underpayment across the three affected pay periods and the two error components. Figures are drawn from the December source-of-truth reconciliation file, verified against legacy-system shadow calculations.

| Pay Period (Check Date) | Missing Differentials | Overtime Shortfall | Period Total | Employees Affected |
|---|---|---|---|---|
| Period 1 (Oct 23) | $68,400 | $16,900 | $85,300 | 594 |
| Period 2 (Nov 6) | $66,100 | $18,300 | $84,400 | 588 |
| Period 3 (Nov 20)* | $63,700 | $17,600 | $81,300 | 581 |
| **Total** | **$198,200** | **$52,800** | **$251,000** | **610 unique** |

*The rules table was restored November 17; however, the November 20 check covered a work period that predated the restoration, so retroactive correction was still required for hours worked before the fix. Employee counts vary by period because differential eligibility depends on shifts actually worked; 610 unique employees were affected across the three periods.

The overtime shortfall warrants explanation, as it was the component missed in the November 18 remediation. Under federal and Maine wage law, overtime must be paid at one and one-half times the *regular rate*, which includes shift differentials earned during the workweek. When the rules table failed to migrate, two distinct errors occurred: differentials were not paid at all, and overtime for employees who worked more than 40 hours was calculated at 1.5 times base rate rather than 1.5 times the differential-inclusive regular rate. Because October and November carried elevated overtime volume, the second error alone represented $52,800 — more than one-fifth of the total underpayment — concentrated among the employees working the most hours to cover existing vacancies. The employees most harmed by the overtime miscalculation were, by definition, the employees the organization could least afford to lose.

### A.2 November 18 Off-Cycle Run — Error Decomposition

| Error | Mechanism | Employees | Amount |
|---|---|---|---|
| Duplicate payment | Employee appeared in both manual spreadsheet batch and vendor retroactive utility batch; no deduplication pass | 84 | $71,000 overpaid |
| Omitted overtime recalculation | Vendor utility corrected differential pay codes only; regular-rate recomputation out of scope; spreadsheet work did not cover it | 412 | $52,800 still owed after run |
| Incorrect withholding | Off-cycle run processed under default rather than supplemental tax configuration | ~530 | No net wage impact; W-2 corrections required |

The overlap that produced the 84 duplicates was mechanical and predictable: the manual spreadsheet effort had begun on November 13 covering the highest-complaint employees, and the vendor utility, run November 17, processed the full affected population. The 84 employees in both files were precisely the employees who had complained earliest and loudest — meaning the organization's most frustrated employees received confusing overpayments requiring clawback conversations, a compounding of trust damage that a single one-hour reconciliation pass would have prevented.

### A.3 Overpayment Recovery Status

As of this document's finalization, recovery of the $71,000 stands as follows:

| Category | Employees | Amount |
|---|---|---|
| Voluntary repayment plans in progress | 61 | $51,300 |
| Repaid in full | 9 | $7,200 |
| Separated employees — recovery under review with counsel | 8 | $8,900 |
| Written off (amount below recovery cost threshold of $75) | 6 | $400 |
| Unresolved | 0 | $3,200 in disputed calculations pending individual review |

All repayment plans are voluntary and structured in compliance with Maine wage deduction law; no involuntary deductions have been or will be taken. Employees were offered plans of up to twelve months with no interest. The organization has elected not to pursue recovery from separated employees where the individual's departure was attributable to the pay errors themselves, a determination made case by case with HR and counsel; the $8,900 figure reflects cases still under that review.

### A.4 December Remediation Run — Verification Summary

The December correction run, used as the template for future corrections (Section 8, item 6), included the following controls, each documented and signed:

1. Single source-of-truth underpayment file built from legacy-system shadow calculations, itemized by employee, pay period, and component (differential vs. overtime).
2. Net-owed calculation subtracting all November 18 payments per employee, eliminating any possibility of further duplication.
3. Independent recalculation of a 40-employee sample (approximately 7%) by an outside accounting firm; zero discrepancies found.
4. Supplemental tax configuration verified in a test environment before execution.
5. Reconciliation report — run file totals against source-of-truth totals — reviewed and signed by the Controller and CFO before release.
6. Post-run confirmation statement mailed to each affected employee showing the arithmetic: total owed, previously paid, this payment, balance (zero).

Total elapsed time from scope sign-off to checks issued: eight business days. This is the benchmark: a fully controlled correction of a 610-employee, multi-component underpayment is an eight-day process, not a four-day one. The difference between the November and December runs — four business days — is the price the organization was unwilling to pay in November and paid many times over as a result.

---

## Appendix B: Workforce Impact Detail

### B.1 Resignation Analysis, November 1 – December 15

| Attribute | Count |
|---|---|
| Total DSP resignations | 38 |
| Cited pay errors as primary reason (exit interview or letter) | 24 |
| Cited pay errors as contributing reason | 7 |
| Unrelated or unstated reasons | 7 |
| Tenure over 3 years among the 38 | 16 |
| Held overnight or weekend regular assignments | 29 |

Two patterns deserve emphasis. First, the resignations skewed toward employees with overnight and weekend assignments — the employees for whom differentials represented the largest share of pay and whose checks were therefore most visibly wrong. Second, the loss of 16 employees with more than three years of tenure represents a disproportionate loss of institutional and resident-specific knowledge; several of the departed staff were primary supports for residents with complex behavioral plans, and continuity-of-care disruption in those homes contributed directly to the supervision strain documented in the licensing citations.

### B.2 Overtime Escalation

Weekly overtime spending, baseline versus incident period:

| Week Ending | Overtime Spend | Variance from Baseline (~$48,000/week) |
|---|---|---|
| Nov 7 | $61,000 | +$13,000 |
| Nov 14 | $74,000 | +$26,000 |
| Nov 21 | $98,000 | +$50,000 |
| Nov 28 | $112,000 | +$64,000 |
| Dec 5 | $131,000 | +$83,000 |
| Dec 12 | $128,000 | +$80,000 |
| **Six-week incremental total** | | **+$316,000** |

The remaining ~$74,000 of the $390,000 incremental figure cited in Section 3 accrued in the two weeks following December 12 as coverage gaps persisted into late December. Note the compounding structure: the pay errors drove resignations, resignations drove overtime, and — until the December remediation — that overtime was itself being *underpaid* because the regular-rate correction had not yet been made. Employees working mandatory overtime to cover for colleagues who quit over pay errors were simultaneously being shorted on that overtime. This feedback loop is the single clearest illustration of why payroll incidents in this organization must be treated as operational emergencies from the first day.

### B.3 Supervision Ratio Exposure

Of the 62 group homes, coverage analysis during the peak vacancy period (December 1–15) showed:

| Status | Homes |
|---|---|
| Fully staffed within normal scheduling | 41 |
| Maintained ratios via float pool and voluntary overtime | 14 |
| Maintained ratios via mandatory overtime | 5 |
| Fell below mandated ratios on one or more shifts | 2 |

The two cited homes shared three characteristics: both had lost two or more resigning staff, both relied heavily on overnight differential-earning positions that proved hardest to backfill, and both served residents whose plans required experienced staff, limiting the usability of agency temporary labor. The corrective action plans filed with state licensing (Action Item 12) address these structural vulnerabilities, including a standing rule that any home losing two or more staff within 30 days triggers immediate float pool prioritization regardless of cause.

---

## Appendix C: Diagnostic Timeline Reconstruction

This appendix reconstructs the October 28 – November 12 diagnostic period in detail, because the nine-day anchor (Section 7.5) was the single largest contributor to incident duration and is the failure mode most likely to recur in a different guise.

**October 28.** Controller reviews escalated complaints. Common feature: missing differential pay. Prior incident (2024) involved time clocks intermittently dropping shift codes; symptoms superficially similar. Hypothesis formed: clock-level failure. Punch audit initiated. *No alternative hypotheses documented.*

**October 29–30.** Audit examines clock exports for the October 23 pay period across a sample of 60 employees. Shift codes present and correct in 60 of 60 records. *Finding interpreted as evidence the failure is intermittent, rather than as evidence against the hypothesis.*

**October 31 – November 3.** Audit expands to interface files between the timekeeping system and Harborworks. Shift codes confirmed present in transmitted files. *At this point the fault had been localized to Harborworks itself by elimination, but this inference was not drawn, because the audit was structured to find dropped codes, not to answer the broader question "where in the chain do differentials disappear?"*

**November 4–6.** Audit continues into historical punch data seeking the intermittent pattern. Second incorrect payroll issues November 6. Complaint volume doubles.

**November 9.** HR Director, prompted by Residential Services escalations, begins independent review. Method: single-employee end-to-end trace — one overnight DSP, one pay period, every data element from punch to paycheck.

**November 10–11.** Trace shows shift codes arriving intact inside Harborworks but generating zero differential earnings at the gross pay calculation step. Fault localized to payroll engine configuration.

**November 12, ~2:00 p.m.** Vendor confirms rules table absent from production. Root cause established. Elapsed diagnostic time: 15 days. Elapsed time the end-to-end trace method required: under 3 days.

The structural lesson: the audit generated correct data for eleven days but was never re-aimed, because no checkpoint forced the question "does the evidence still support the hypothesis?" The diagnostic protocol in Action Item 8 — 48-hour end-to-end trace, cross-functional team, 72-hour falsification checkpoints — is designed specifically against this pattern. Had the protocol existed on October 28, the incident's employee-facing duration would likely have been cut by roughly two weeks and the second bad payroll avoided entirely.

---

## Appendix D: Communications Record

| Date | Communication | Audience | Assessment |
|---|---|---|---|
| Oct 23 – Nov 13 | None (organizational) | — | Twenty-one days of silence while 610 employees saw incorrect checks; supervisors improvised answers without information. Largest communication failure of the incident. |
| Nov 16 | All-staff message from CEO acknowledging error, taking responsibility, committing to Nov 18 correction | All employees | Well received in tone; the date commitment, made before remediation scope was defined, drove the control omissions of Nov 18. |
| Nov 20 | Follow-up acknowledging overpayments and continuing overtime shortfall; no new date committed | All employees | Correct decision not to re-commit a date; credibility already damaged. |
| Dec (late) | Individual confirmation statements with full payment arithmetic | 610 affected employees | Effective; manual verification requests declined ~70% within two weeks of issuance. |
| Jan 2027 | W-2 correction notice with plain-language explanation and tax-question contact | Affected employees | Adequate; tax-preparation reimbursement offer (Action Item 11) reduced complaint volume. |

The communications lesson mirrors the remediation lesson: speed of acknowledgment matters more than completeness of answers. A message on October 29 saying "we know, we are investigating, here is who to contact, here is when you will hear from us next" would have cost nothing and preserved substantial goodwill. The revised incident protocol (Action Item 8) includes a mandatory employee acknowledgment communication within 2 business days of any confirmed pay-accuracy incident, regardless of diagnostic status.

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| **DSP** | Direct support professional; frontline staff providing daily care and support to residents. |
| **Shift differential** | Additional hourly pay for evening, overnight, or weekend shifts; at PBIN, $1.50–$3.25/hour by shift type. |
| **Regular rate** | The hourly rate on which overtime must be calculated under wage law; includes shift differentials and certain other earnings, not base rate alone. |
| **Rules table** | The payroll system configuration defining which shift codes trigger which differentials and how the regular rate is computed. |
| **Parallel testing** | Running legacy and new payroll systems simultaneously on identical inputs and comparing outputs before cutover. |
| **Off-cycle run** | A payroll processing run outside the regular schedule, typically for corrections. |
| **Reconciliation** | Verification that a payment file matches an independently derived source-of-truth calculation before funds are released. |
| **Supervision ratio** | State-mandated minimum ratio of qualified staff to residents per shift in licensed group homes. |
| **Source-of-truth file** | The single authoritative calculation of amounts owed, against which all correction payments are reconciled. |

---

## Appendix F: Sign-Off and Acknowledgment

The following individuals participated in the postmortem review sessions, confirm the factual accuracy of the timeline and impact figures as they pertain to their areas, and accept the action items assigned to them.

| Name | Title | Role in Review | Signature / Date |
|---|---|---|---|
| Delphine Ouellette | Chief Executive Officer | Executive sponsor; owner, Action Items 9, 14 | ______________ |
| Marcus Tillinghast | Chief Financial Officer | Finance review; owner, Action Items 1, 6, 7, 10, 13 | ______________ |
| Nkechi Obiora | Director of Human Resources | Review facilitator; owner, Action Items 3, 4, 8 | ______________ |
| Soren Bragg | Controller | Payroll operations review; owner, Action Items 2, 5, 11 | ______________ |
| Imelda Restrepo | Director of Residential Services | Program impact review; owner, Action Item 12 | ______________ |

First monthly action-item status review: scheduled at the next regular executive team meeting following distribution of this document. Six-month effectiveness review of implemented controls: Q1 2027 close, with results reported to the Board Finance Committee and the Board Quality & Compliance Committee.

**End of document.**
