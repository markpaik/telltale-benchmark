# Closing the Gap: PCI DSS 4.0 Compliance Pathways for Multi-Location Restaurant and Specialty Retail Operators

**An Ironwood Commerce Systems White Paper**

**Authors:**
Devika Ranganathan, Chief Information Security Officer, Ironwood Commerce Systems
Thabo Mokoena, Vice President of Product, Ironwood Commerce Systems
Erin Nakashima-O'Leary, CISA, Compliance Director, Ironwood Commerce Systems
Gareth Sowinski, QSA, Independent Assessment Partner

**Ironwood Commerce Systems | Grand Rapids, Michigan | August 2026**

---

## Abstract

The future-dated requirements of the Payment Card Industry Data Security Standard version 4.0 became mandatory on March 31, 2025, converting more than fifty formerly "best practice" controls into enforceable obligations. For franchise restaurant and specialty retail operators, the consequences are now arriving through three channels at once: franchisor mandates flowing down through franchise agreements, acquirer non-compliance fees of $35 to $100 per month per merchant identifier, and litigation exposure demonstrated by a class action following a 2024 breach at a 38-location franchisee.

This paper draws on Ironwood Commerce Systems' visibility into 8,700 restaurant and specialty retail locations across fourteen states, including 1,120 self-assessment questionnaires and 96 card-present security incidents recorded between 2021 and 2025. That data shows where merchants actually fail: targeted risk analyses, payment page script integrity, authenticated internal vulnerability scanning, and phishing-resistant multifactor authentication for remote access. It also shows what failure costs — an average of $118,000 in forensics, fines, and card reissuance for a four-location operator.

We compare five remediation paths — validated point-to-point encryption, tokenization, full network segmentation, outsourced hosted checkout, and managed compliance services — on cost, scope reduction, operational fit, and time to compliance. We then present an implementation and cost model for a representative multi-location operator and respond directly to the four objections we hear most often: capital constraints, legacy hardware, offline-mode dependence, and tip adjustment workflows. Our conclusion is that for most card-present franchise operators, validated point-to-point encryption combined with tokenization is the fastest and least expensive route to a defensible compliance posture, and that the roughly 2,300 locations in our base still running terminals on an operating system that lost vendor support in October 2025 face a decision that can no longer be deferred.

---

## 1. The Compliance Problem: Why March 2025 Changed the Economics

### 1.1 The standard's future-dated requirements are now mandatory

PCI DSS 4.0 was published in March 2022 with a two-stage transition. Version 3.2.1 was retired on March 31, 2024, and the 51 future-dated requirements of version 4.0 — the controls the PCI Security Standards Council considered significant enough to warrant a longer runway — became mandatory on March 31, 2025. That second date is the one that matters for the merchants Ironwood serves, because the future-dated requirements are precisely the ones that small and mid-sized card-present operators are least equipped to satisfy on their own:

- **Targeted risk analyses (Requirements 12.3.1 and 12.3.2)** requiring documented, periodic analysis for every requirement where the merchant exercises flexibility in frequency or method.
- **Payment page script integrity (Requirements 6.4.3 and 11.6.1)** requiring inventory, authorization, and integrity assurance for all scripts on payment pages, plus tamper-detection mechanisms — a direct response to Magecart-style e-skimming.
- **Authenticated internal vulnerability scanning (Requirement 11.3.1.2)** requiring credentialed scans of internal systems, not just unauthenticated perimeter scans.
- **Expanded multifactor authentication (Requirements 8.4.2, 8.4.3, and 8.5.1)** requiring MFA for all access into the cardholder data environment and phishing-resistant characteristics for remote access, with replay resistance and no null-factor bypass.

For a franchisee with three to ten locations and no dedicated IT staff, each of these represents a discipline the business has never practiced. A targeted risk analysis is a document that most restaurant operators have never seen, let alone written. Authenticated internal scanning presumes a managed scan infrastructure with credential vaulting. Phishing-resistant MFA presumes an identity platform. None of these are things a general manager can bolt on between lunch and dinner service.

### 1.2 Franchisors are pushing the obligation down

Franchise agreements almost universally require franchisees to comply with applicable payment card rules, and franchisors are now enforcing that clause with specificity. Two large franchisors represented in Ironwood's merchant base have set an **April 2026 compliance mandate**, requiring franchisees to demonstrate validated PCI DSS 4.0 compliance — a completed and attested self-assessment questionnaire or a Report on Compliance, depending on transaction volume — as a condition of continued operation under the brand. Franchisees who miss the deadline face escalating remedies up to and including default under the franchise agreement.

This changes the merchant's calculus. Non-compliance was once a quiet risk absorbed as monthly acquirer fees. It is now an existential risk to the franchise relationship itself.

### 1.3 The cost of doing nothing is no longer small

Three forces have raised the price of inaction:

1. **Acquirer non-compliance fees have risen to $35–$100 per month per merchant identifier.** A ten-location operator with one MID per location is paying $4,200 to $12,000 per year for the privilege of remaining non-compliant — money that produces nothing.
2. **Breach costs are documented and material.** Across the 96 card-present incidents in Ironwood's base from 2021 through 2025, the average incident cost a four-location operator **$118,000** in forensic investigation, card brand fines and assessments, and reissuance costs. That figure excludes lost revenue during remediation, legal fees, and reputational damage.
3. **Litigation risk is real at franchise scale.** A class action filed after a 2024 breach at a 38-location franchisee in our footprint demonstrated that plaintiffs' counsel will pursue mid-sized operators, not just national brands, and that documented non-compliance with PCI DSS is central to negligence claims.

### 1.4 The end-of-support problem compounds everything

Approximately **2,300 locations** in Ironwood's merchant base still run point-of-sale terminals on an operating system that lost vendor support in October 2025. PCI DSS Requirement 6.3.3 requires that critical security patches be applied within one month of release; an unsupported operating system receives no patches at all, making sustained compliance impossible on that platform. These locations cannot remediate their way to compliance on existing hardware. They face a forced platform decision, and the only question is whether it happens on a planned schedule or after an incident.

---

## 2. What Ironwood Sees Across Its Merchant Base

### 2.1 The evidence base

Ironwood's visibility is unusual for a company of its size: 8,700 locations across fourteen states, 1,120 completed self-assessment questionnaires reviewed by our compliance team and our independent QSA partner, and incident records for 96 confirmed card-present security events from 2021 through 2025. This section summarizes what that evidence shows.

### 2.2 Where merchants fail

**Table 1. Most frequently failed PCI DSS 4.0 requirements, Ironwood merchant base (n = 1,120 SAQs, 2024–2025 assessment cycle)**

| Rank | Requirement area | PCI DSS reference | Share of merchants failing | Why it fails |
|---|---|---|---|---|
| 1 | Targeted risk analyses | 12.3.1, 12.3.2 | 71% | No template, no process, no owner; most operators have never produced a formal risk analysis |
| 2 | Payment page script integrity | 6.4.3, 11.6.1 | 64% (of merchants with e-commerce/online ordering) | Scripts injected by loyalty, analytics, and ordering plug-ins; no inventory or tamper detection |
| 3 | Authenticated internal vulnerability scanning | 11.3.1.2 | 58% | Merchants run only external ASV scans; no internal scan infrastructure or credentials management |
| 4 | Phishing-resistant MFA for remote access | 8.4.2, 8.4.3, 8.5.1 | 52% | Remote vendor and back-office access secured with passwords or SMS codes only |
| 5 | Patch currency / supported platforms | 6.3.3 | 41% | End-of-support operating systems; deferred terminal refresh cycles |

Two patterns stand out. First, the top failures are *process* failures, not *technology* failures — the merchant lacks a documented discipline, not a product. Second, the failures cluster: a merchant failing one of the top four typically fails at least two others, because all four presume a level of security operations maturity that a franchise operator without dedicated IT staff simply does not have.

### 2.3 What incidents look like

**Table 2. Card-present incident profile, Ironwood merchant base, 2021–2025 (n = 96)**

| Attribute | Finding |
|---|---|
| Median dwell time before detection | 74 days |
| Most common initial vector | Compromised remote access credentials (44% of incidents) |
| Second most common vector | Malware on unsupported/unpatched POS terminals (29%) |
| Third most common vector | E-skimming on online ordering pages (18%) |
| Average total cost, four-location operator | $118,000 |
| Cost breakdown (typical) | Forensics $32,000; card brand fines and assessments $51,000; reissuance $35,000 |
| Incidents where cardholder data was encrypted at point of interaction | 3 of 96 |

The last row is the most important number in this paper. **Of 96 incidents, only three occurred at merchants using validated point-to-point encryption at the point of interaction — and in all three, no usable cardholder data was exposed** because the attacker obtained only ciphertext. The incident cost in those three cases was limited to investigation and cleanup, averaging under $9,000. Encryption at the point of capture does not prevent intrusion, but it removes the asset the intruder came for.

### 2.4 The vector data maps directly to the failure data

Compromised remote access (44% of incidents) corresponds to the 52% MFA failure rate. Malware on unpatched terminals (29%) corresponds to the 41% patch-currency failure rate and the 2,300 end-of-support locations. E-skimming (18%) corresponds to the 64% script-integrity failure rate. The requirements merchants fail are not arbitrary paperwork; they are the exact controls that would have interrupted the incidents we investigated. This alignment is the strongest argument we can make that PCI DSS 4.0's future-dated requirements are worth complying with on the merits, not merely to avoid fees.

---

## 3. Five Paths to Compliance, Compared

There are five realistic remediation paths for a multi-location card-present operator. They are not mutually exclusive — the strongest postures combine them — but each has a distinct cost profile, scope-reduction effect, and operational fit.

### 3.1 The five paths

**Path A — Validated point-to-point encryption (P2PE).** Cardholder data is encrypted inside a PCI-listed secure reading device and decrypted only within the solution provider's hardened environment. The merchant never possesses cleartext card data. Cost: approximately **$640 per lane** for hardware plus **$19 per month per lane** for the P2PE service. Merchants using a validated P2PE solution qualify for SAQ P2PE, reducing the assessment from over 250 requirements to roughly 33.

**Path B — Tokenization.** Card data is replaced with tokens after authorization, so stored data (for tips, tabs, recurring billing, card-on-file) has no exploitable value. Tokenization does not by itself protect data in flight at the point of capture, so it reduces *storage* scope, not *capture* scope. Typically priced as a per-transaction or monthly gateway fee already embedded in Ironwood's platform.

**Path C — Full network segmentation.** The cardholder data environment is isolated behind firewalls and VLANs from back-office, guest Wi-Fi, and vendor networks, shrinking the number of systems in scope. Cost: approximately **$14,000 per site** for design, hardware, implementation, and validation, plus ongoing segmentation testing (now required at least every six months for service providers and annually for merchants, with testing after changes). Segmentation reduces scope but does not remove cleartext card data from the merchant environment; the in-scope systems still must meet the full standard.

**Path D — Outsourced hosted checkout.** For e-commerce and online ordering, payment capture is fully redirected to a compliant provider's hosted page or iframe. The merchant qualifies for SAQ A, the shortest questionnaire — though PCI DSS 4.0 expanded SAQ A to include script integrity and tamper-detection obligations on the page that embeds or redirects to checkout. Cost: typically absorbed into gateway pricing; implementation effort is integration work, not capital.

**Path E — Managed compliance service.** Ironwood or a third party operates the compliance program on the merchant's behalf: targeted risk analyses, authenticated internal scanning, MFA deployment, SAQ preparation, and evidence collection. Cost: **$85–$150 per location per month** depending on tier. This path does not reduce scope; it supplies the operational discipline the merchant lacks to satisfy the scope it has.

### 3.2 Side-by-side comparison

**Table 3. Comparison of compliance paths for a multi-location card-present operator**

| Dimension | A: Validated P2PE | B: Tokenization | C: Segmentation | D: Hosted checkout | E: Managed compliance |
|---|---|---|---|---|---|
| Upfront cost (10-location operator, ~30 lanes) | ~$19,200 | Minimal | ~$140,000 | Minimal (integration only) | Minimal |
| Ongoing cost (annual, same operator) | ~$6,840 | Gateway fees | ~$15,000–$25,000 (testing, maintenance) | Gateway fees | ~$10,200–$18,000 |
| Scope reduction | Very high (SAQ P2PE, ~33 requirements) | Moderate (storage only) | Moderate (fewer in-scope systems, full standard still applies to them) | Very high for e-commerce channel (SAQ A) | None (operational support only) |
| Addresses card-present capture risk | **Yes — removes cleartext data** | No | Partially (limits attacker reach) | No (e-commerce only) | Indirectly |
| Addresses e-skimming risk | No | No | No | **Yes** | Supports script inventory/monitoring |
| Addresses top SAQ failures (risk analyses, scanning, MFA) | Reduces how many apply | No | No | Reduces for e-comm channel | **Yes — directly** |
| Solves end-of-support terminal problem | **Yes — new devices included** | No | No | No | No |
| Time to compliance | 60–120 days | 30–60 days | 6–12 months | 30–90 days | 90–180 days |
| Ongoing merchant burden | Low | Low | **High** (testing, change control, full standard on in-scope systems) | Low | Low (outsourced) |
| Breach cost mitigation | **Very high** (ciphertext only) | High for stored data | Moderate | High for e-comm | Moderate |

### 3.3 Analysis

**Segmentation alone is the weakest value for this merchant profile.** At $14,000 per site, a ten-location operator spends $140,000 to *reduce* scope without removing cardholder data from the environment, and inherits a permanent testing and change-control burden that reintroduces the very process failures documented in Table 1. Segmentation is the right primary strategy for large enterprises with in-house security teams; for franchise operators it is the most expensive way to remain responsible for cleartext card data.

**P2PE is the anchor.** It is the only path that removes cleartext cardholder data from the merchant's card-present environment, the only path that resolves the end-of-support terminal problem (the P2PE devices replace the vulnerable capture hardware), and the path with the largest documented breach-cost mitigation in our incident data (Section 2.3). At $640 per lane plus $19 monthly, its total cost over three years for a ten-location, 30-lane operator is roughly $39,700 — under 30% of the cost of segmenting the same footprint, and one-third of the cost of a single average incident.

**Tokenization and hosted checkout are complements, not alternatives.** Tokenization closes the stored-data exposure that P2PE does not address (tabs, tips, card-on-file). Hosted checkout closes the e-skimming exposure on online ordering — the vector in 18% of our incidents — and collapses the e-commerce channel to SAQ A. Both are largely embedded in platform pricing and cost little to adopt.

**Managed compliance closes what technology cannot.** Even with P2PE, tokenization, and hosted checkout, the merchant retains obligations: the SAQ P2PE and SAQ A requirements, targeted risk analyses, MFA on remaining remote access, and script monitoring on the ordering page. These are exactly the process failures in Table 1. A managed service at $85–$150 per location per month is the difference between a technically strong posture and a *validated* one that survives franchisor and acquirer review.

**Our recommendation for the typical multi-location operator is therefore a layered configuration: P2PE + tokenization + hosted checkout + managed compliance**, with segmentation reserved for the operator's remaining back-office scope rather than deployed as the primary strategy.

---

## 4. Implementation and Cost Model for a Multi-Location Operator

### 4.1 The reference operator

We model a representative franchisee in Ironwood's base: **ten locations, three payment lanes per location (30 lanes total), online ordering at all locations, one merchant identifier per location, no dedicated IT staff**, currently non-compliant and paying acquirer non-compliance fees at the midpoint of the observed range ($67.50/MID/month).

### 4.2 Phased implementation plan

**Table 4. Implementation phases, reference operator (ten locations, 30 lanes)**

| Phase | Timeline | Activities | Milestone |
|---|---|---|---|
| 1. Scoping and baseline | Weeks 1–4 | Data-flow mapping per location; confirm SAQ eligibility per channel; inventory end-of-support terminals; enroll in managed compliance service | Validated scope document; remediation roadmap |
| 2. P2PE deployment | Weeks 4–14 | Deploy validated P2PE devices to all 30 lanes (staged, two locations/week); decommission end-of-support terminals; staff training on device inspection (Req. 9.5.1) | All lanes on P2PE; unsupported OS retired from payment capture |
| 3. E-commerce migration | Weeks 6–12 (parallel) | Migrate online ordering to hosted checkout; implement script inventory and tamper detection on ordering pages | SAQ A eligibility for e-commerce channel |
| 4. Access and process controls | Weeks 8–18 | Deploy phishing-resistant MFA (FIDO2 keys or platform authenticators) for all remote and administrative access; establish authenticated internal scanning on remaining in-scope systems; produce targeted risk analyses via managed service templates | Top four failure areas remediated |
| 5. Validation | Weeks 18–24 | Complete SAQ P2PE (card-present) and SAQ A (e-commerce) with QSA review; submit attestations to acquirer and franchisor | Validated compliance ahead of April 2026 franchisor mandate |

Total elapsed time: approximately **six months**, comfortably inside the window between publication of this paper and the April 2026 franchisor deadlines, provided the operator begins promptly.

### 4.3 Cost model

**Table 5. Three-year cost model, reference operator (ten locations, 30 lanes, 10 MIDs)**

| Item | Year 1 | Year 2 | Year 3 | Three-year total |
|---|---|---|---|---|
| P2PE hardware (30 lanes × $640) | $19,200 | — | — | $19,200 |
| P2PE service (30 lanes × $19/mo) | $6,840 | $6,840 | $6,840 | $20,520 |
| Hosted checkout migration (one-time integration) | $4,500 | — | — | $4,500 |
| Phishing-resistant MFA (hardware keys, licensing) | $3,200 | $1,100 | $1,100 | $5,400 |
| Managed compliance service (10 locations × $120/mo midpoint) | $14,400 | $14,400 | $14,400 | $43,200 |
| Staff training and rollout labor | $6,000 | $1,500 | $1,500 | $9,000 |
| **Gross cost** | **$54,140** | **$23,840** | **$23,840** | **$101,820** |
| Less: eliminated non-compliance fees (10 MIDs × $67.50/mo) | ($4,050)* | ($8,100) | ($8,100) | ($20,250) |
| **Net cost** | **$50,090** | **$15,740** | **$15,740** | **$81,570** |

\* *Fees eliminated for six months of Year 1 following validation.*

### 4.4 The risk-adjusted case

The net three-year cost of $81,570 — roughly **$2,720 per lane, or $75 per location per month on a run-rate basis after Year 1** — should be weighed against the exposure it retires:

- **Expected breach cost.** Our incident base implies a meaningful multi-year probability of an incident for a non-compliant ten-location operator on aging hardware. Scaling the $118,000 four-location average to ten locations suggests single-incident exposure in the $250,000–$300,000 range before litigation. Even at a conservative 15% probability over three years, expected loss exceeds $37,000 — and P2PE's demonstrated effect (Section 2.3) reduces that exposure by more than 90%.
- **Franchise continuity.** The April 2026 mandates make non-compliance a default risk under the franchise agreement. The value of the franchise itself dwarfs every number in Table 5.
- **Forced hardware replacement.** Locations on the end-of-support operating system must replace capture hardware regardless of compliance strategy. For those locations, the $640-per-lane P2PE device is not incremental cost; it is the *form* the unavoidable refresh should take.
- **Litigation posture.** A validated, documented compliance program is the operator's primary defense in post-breach litigation of the kind filed against the 38-location franchisee in 2024.

On these terms, the layered configuration is not a compliance tax. It is the least expensive available resolution of a set of risks the operator already carries.

---

## 5. Answering the Objections

Ironwood's field teams hear four objections consistently. Each deserves a direct answer.

### 5.1 "We don't have the capital."

The Year 1 gross outlay in our model is $54,140 for ten locations — real money for a franchise operator. Three responses:

First, **the counterfactual is not zero.** The operator is already paying roughly $8,100 per year in non-compliance fees, carries breach exposure with an expected cost that likely exceeds the program's net cost, and — for the 2,300 end-of-support locations — faces mandatory hardware replacement anyway. The relevant comparison is not "spend versus don't spend" but "spend on a plan versus spend after an incident, at three to five times the price, plus fines."

Second, **the capital component can be financed.** Ironwood offers the P2PE hardware on a per-lane monthly subscription that folds the $640 device cost into the service fee, converting the Year 1 hardware line into operating expense of approximately $37 per lane per month with no upfront outlay. The three-year total cost is modestly higher; the Year 1 cash requirement drops by over $19,000.

Third, **the phased rollout spreads the remainder.** Deploying two locations per week means costs are incurred over a quarter, not on a single invoice, and each converted location stops accruing its non-compliance fee at validation.

### 5.2 "Our hardware is legacy and we can't rip it out."

For the roughly 2,300 locations on the operating system that lost support in October 2025, this objection inverts itself: **the legacy hardware is the problem, not a constraint on the solution.** An unsupported OS cannot satisfy Requirement 6.3.3, cannot be made compliant by any amount of surrounding effort, and was the malware vector in 29% of the incidents in our base. Retaining it is not a cost-avoidance strategy; it is an uninsured liability.

For merchants whose POS platform is otherwise supportable, the P2PE architecture is specifically designed to *preserve* the existing POS. The secure reading device sits in front of the POS; card data is encrypted inside the device and passes through the POS as ciphertext. The register hardware, menu configuration, and staff workflows remain unchanged. In our deployments, the median per-lane cutover is under 45 minutes and occurs outside service hours.

### 5.3 "We need offline mode during internet outages, and encryption will break it."

It will not. Validated P2PE devices support **store-and-forward operation**: during a connectivity outage, the device captures and encrypts the card data exactly as it does online, stores the encrypted payload locally, and forwards it for authorization when connectivity returns. The merchant continues taking payments; the data at rest during the outage is ciphertext, which is materially *safer* than the cleartext store-and-forward queues on legacy terminals — queues that were harvested in several of the incidents we investigated. Operators should configure store-and-forward floor limits and aging rules to manage authorization risk, and Ironwood's default profiles do so. The offline scenario is an argument *for* encryption at capture, not against it.

### 5.4 "Tip adjustment will stop working."

This is the most operationally specific objection and the most fixable. Restaurant operators adjust authorization amounts after the guest writes a tip on the receipt; they worry that once the card number is encrypted or discarded, the adjustment cannot be processed.

The answer is **tokenization — Path B — which is why it belongs in the layered configuration.** At authorization, the processor returns a token that references the transaction. The tip adjustment is submitted against the token, not the card number. No cardholder data is stored at the location at any point in the workflow. The same mechanism supports bar tabs, incremental authorizations, and card-on-file. Ironwood's platform has processed token-based tip adjustment in production since 2023 across thousands of restaurant locations; the server-facing workflow — enter check number, enter tip, confirm — is unchanged. What changes is that the batch file sitting on the back-office server no longer contains anything a criminal can sell.

### 5.5 A note on the objections collectively

Each objection, examined closely, describes a risk the merchant is *already carrying in worse form*: capital objections ignore the fees and exposure already being paid; legacy-hardware objections defend the platform causing 29% of incidents; offline-mode objections defend cleartext store-and-forward queues; tip-workflow objections defend cleartext batch storage. The remediation paths do not introduce these problems. They surface and then retire them.

---

## 6. Conclusion

The March 31, 2025 effective date for PCI DSS 4.0's future-dated requirements ended a long grace period, and the surrounding environment — franchisor mandates due in April 2026, non-compliance fees of $35 to $100 per MID per month, active class litigation against a mid-sized franchisee, and 2,300 locations on capture hardware that can no longer be patched — has ended the era in which a franchise operator could treat compliance as an indefinitely deferrable expense.

The evidence from Ironwood's 8,700-location base points to a clear conclusion. Merchants fail the standard where it demands operational discipline they do not have — targeted risk analyses, script integrity, authenticated scanning, phishing-resistant MFA — and they suffer incidents through exactly the vectors those controls address. Only three of 96 incidents occurred at merchants with validated point-to-point encryption, and none of the three exposed usable cardholder data.

For the typical multi-location operator, the layered configuration — **validated P2PE at every lane, tokenization for post-authorization workflows, hosted checkout for online ordering, and a managed compliance service for the process obligations that remain** — delivers validated compliance in roughly six months at a net three-year cost of about $81,570 for a ten-location operator, or roughly $75 per location per month at run rate. Full network segmentation, at $14,000 per site, remains the right tool for large enterprises with security staff, but for franchise operators it is the most expensive way to keep custody of data they should not hold at all.

The strategic insight underneath the tactics is simple: **the cheapest cardholder data to protect is the cardholder data you never possess.** Every path that removes cleartext data from the merchant environment shrinks the assessment, shrinks the attack surface, and shrinks the breach. Operators who begin now can meet the April 2026 franchisor deadlines with margin to spare. Operators who wait will make the same investments later, under worse conditions, and possibly after writing the $118,000 check first.

Ironwood Commerce Systems' compliance team and our independent QSA partner are available to conduct scoping assessments for franchise operators, technology directors, acquiring banks, and ISOs evaluating these paths across their portfolios.

---

## References

1. PCI Security Standards Council. *Payment Card Industry Data Security Standard: Requirements and Testing Procedures, Version 4.0.1.* Wakefield, MA: PCI SSC, 2024.
2. PCI Security Standards Council. *PCI DSS v4.x: Summary of Changes from PCI DSS v3.2.1.* Wakefield, MA: PCI SSC, 2024.
3. PCI Security Standards Council. *Self-Assessment Questionnaire P2PE and Attestation of Compliance, Version 4.0.* Wakefield, MA: PCI SSC, 2024.
4. PCI Security Standards Council. *Self-Assessment Questionnaire A and Attestation of Compliance, Version 4.0.* Wakefield, MA: PCI SSC, 2024.
5. PCI Security Standards Council. *Point-to-Point Encryption (P2PE) Solution Requirements and Testing Procedures, Version 3.1.* Wakefield, MA: PCI SSC, 2023.
6. PCI Security Standards Council. *Information Supplement: Guidance for PCI DSS Scoping and Network Segmentation.* Wakefield, MA: PCI SSC, 2017.
7. Ironwood Commerce Systems. *Merchant Compliance Assessment Dataset: Self-Assessment Questionnaire Outcomes, 2024–2025 Cycle (n = 1,120).* Internal dataset, Grand Rapids, MI, 2026.
8. Ironwood Commerce Systems. *Card-Present Incident Register and Cost Analysis, 2021–2025 (n = 96).* Internal dataset, Grand Rapids, MI, 2026.
9. Verizon. *2025 Payment Security Report.* Verizon Business, 2025.
10. Federal Trade Commission. *Franchise Rule Compliance Guide.* Washington, DC: FTC, 2023.

---

*© 2026 Ironwood Commerce Systems, Grand Rapids, Michigan. This white paper is provided for informational purposes and does not constitute legal or assessment advice. Compliance validation requirements vary by card brand, acquirer, and merchant level; operators should confirm their obligations with their acquiring bank and a qualified security assessor.*

## Appendix A. Self-Assessment Questionnaire Eligibility Under the Layered Configuration

Operators frequently ask which validation instrument applies once the layered configuration is deployed. The answer depends on channel, and a multi-location operator will typically validate against two questionnaires simultaneously — one for the card-present channel and one for e-commerce. Table 6 summarizes the eligibility conditions and what each questionnaire demands.

**Table 6. SAQ eligibility by channel after full deployment of the layered configuration**

| Channel | Questionnaire | Approximate requirement count (v4.0) | Key eligibility conditions | Residual merchant obligations |
|---|---|---|---|---|
| Card-present (all lanes) | SAQ P2PE | ~33 | All payment capture through a PCI-listed validated P2PE solution; no cleartext account data stored, processed, or transmitted outside the solution; no legacy capture devices remaining in service | Device inspection and tamper checks (Req. 9.5.1); P2PE Instruction Manual adherence; incident response plan; targeted risk analyses where frequency flexibility is exercised |
| Online ordering / e-commerce | SAQ A | ~29 (expanded under v4.0) | All payment capture fully outsourced to a PCI-compliant provider via redirect or provider-hosted iframe; merchant site does not receive account data | Script inventory, authorization, and integrity on the page invoking checkout (Req. 6.4.3); tamper/change detection (Req. 11.6.1); MFA on administrative access to the site |
| Mail/telephone order, if any | SAQ P2PE (if entered on P2PE device) or SAQ C-VT | Varies | Keyed entry performed on the P2PE device keeps the channel within SAQ P2PE scope | As above; virtual terminal isolation if SAQ C-VT applies |

Two cautions. First, **eligibility is fragile.** A single non-P2PE terminal retained "for backup," or a single online ordering plug-in that touches card data before redirect, disqualifies the merchant from the reduced questionnaire and returns the full standard to scope for that channel. Scope discipline is a permanent operating obligation, and it is one of the specific functions of the managed compliance service in Path E. Second, **SAQ A is no longer trivial.** The version 4.0 expansion of SAQ A to include payment page script integrity and tamper detection means that even fully outsourced e-commerce merchants carry technical monitoring obligations they did not carry under version 3.2.1. Acquiring banks in Ironwood's footprint have begun rejecting SAQ A attestations that do not evidence these controls.

---

## Appendix B. Pre-Engagement Readiness Checklist for Multi-Location Operators

Operators preparing to begin Phase 1 of the implementation plan (Section 4.2) can accelerate scoping by assembling the following before the first engagement meeting:

1. **Location and lane inventory.** Count of locations, payment lanes per location, and merchant identifiers, including seasonal or mobile lanes (patio carts, festival units, food trucks).
2. **Terminal census.** Make, model, operating system, and firmware version of every payment capture device, flagging any device on an operating system past end of vendor support.
3. **Network topology per location.** Even a hand-drawn diagram showing how POS, back office, guest Wi-Fi, kitchen display systems, and third-party devices connect materially shortens the scoping phase.
4. **Remote access register.** Every party — vendors, franchisor systems, off-site bookkeepers, the operator's own managers — with remote access into any location's network, and the authentication method each uses today.
5. **Online ordering architecture.** Provider, integration method (redirect, iframe, API), and a list of every third-party script loaded on ordering pages, including loyalty, analytics, chat, and marketing tags.
6. **Post-authorization workflow inventory.** All uses of card data after the sale: tip adjustment, tabs, incremental authorization, refunds, card-on-file, house accounts.
7. **Current compliance artifacts.** Most recent SAQ or ROC, most recent ASV scan results, and any acquirer or franchisor correspondence regarding compliance status or fees.
8. **Franchisor deadline documentation.** The specific mandate language, deadline, and required evidence format from the franchisor, so the validation deliverables in Phase 5 can be matched to it exactly.

In Ironwood's experience, operators who arrive with items 1 through 4 complete reduce the Phase 1 scoping window from four weeks to two, pulling the entire program timeline forward accordingly — a margin that matters for operators starting close to the April 2026 mandates.

---

## Appendix C. Glossary of Terms

**Acquirer / acquiring bank.** The financial institution that maintains the merchant's account and settles card transactions; the entity that levies non-compliance fees and receives compliance attestations.

**ASV (Approved Scanning Vendor).** A PCI SSC-approved vendor performing the external vulnerability scans required quarterly under Requirement 11.3.2. Distinct from the authenticated *internal* scanning required under 11.3.1.2.

**Cardholder data environment (CDE).** The people, processes, and systems that store, process, or transmit cardholder data or sensitive authentication data, plus connected systems.

**E-skimming (Magecart).** Injection of malicious script into a payment or ordering page to capture card data in the shopper's browser; the vector addressed by Requirements 6.4.3 and 11.6.1.

**MID (Merchant Identifier).** The account number assigned by the acquirer to a merchant location or channel; the unit against which non-compliance fees are assessed.

**P2PE (Point-to-Point Encryption).** Encryption of account data within a secure card-reading device at the point of interaction, decrypted only within the solution provider's environment. "Validated" P2PE refers to solutions listed by the PCI SSC after laboratory and QSA (P2PE) assessment.

**Phishing-resistant MFA.** Multifactor authentication resistant to credential interception and replay — typically FIDO2/WebAuthn hardware keys or platform authenticators — as opposed to SMS one-time codes, which are phishable.

**QSA (Qualified Security Assessor).** An individual certified by the PCI SSC to perform PCI DSS assessments and validate compliance.

**ROC (Report on Compliance).** The full assessment report produced by a QSA for merchants above self-assessment thresholds or where required by an acquirer or franchisor.

**SAQ (Self-Assessment Questionnaire).** The validation instrument for merchants eligible to self-assess; the applicable SAQ type is determined by payment channel architecture.

**Store-and-forward.** Terminal capability to capture and locally queue transactions during a connectivity outage, forwarding them for authorization when connectivity is restored.

**Targeted risk analysis (TRA).** The documented analysis required under Requirements 12.3.1 and 12.3.2 wherever the standard permits the entity to define the frequency or method of a control.

**Tokenization.** Replacement of the primary account number with a surrogate value (token) usable only within a defined context, removing exploitable data from post-authorization storage and workflows.

---

## About the Authors

**Devika Ranganathan** is Chief Information Security Officer at Ironwood Commerce Systems, where she oversees platform security, incident response, and the security architecture of Ironwood's P2PE and tokenization services. She has led the response to card-present incidents across the merchant base since 2020.

**Thabo Mokoena** is Vice President of Product at Ironwood, responsible for the point-of-sale platform, payments integrations, and the offline and tip-adjustment workflows discussed in Section 5. He previously held product leadership roles in restaurant technology and acquiring.

**Erin Nakashima-O'Leary, CISA,** is Compliance Director at Ironwood and leads the team that reviews merchant self-assessment questionnaires and operates the managed compliance service. She maintains the assessment dataset summarized in Section 2.

**Gareth Sowinski, QSA,** is a Qualified Security Assessor with Ironwood's independent assessment partner and performs the QSA reviews referenced in Sections 2 and 4. His contributions to this paper reflect his independent professional judgment; his firm's assessment engagements remain independent of Ironwood's commercial offerings.

---

## Contact

Franchise operators, restaurant technology directors, acquiring banks, and independent sales organizations seeking a scoping assessment or portfolio-level compliance review may contact Ironwood Commerce Systems' compliance practice at compliance@ironwoodcommerce.com or through their Ironwood account representative. Portfolio briefings for acquirers and ISOs covering aggregate compliance posture and remediation planning across sponsored merchants are available on request.

---

*Document version 1.0, published August 2026. Ironwood Commerce Systems, Grand Rapids, Michigan.*
