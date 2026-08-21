# Card Data Security at the Point of Sale: A Compliance and Cost Roadmap for Multi-Location Restaurant and Retail Operators

**A White Paper from Ironwood Commerce Systems**

Devika Ranganathan, Chief Information Security Officer
Thabo Mokoena, Vice President of Product
Erin Nakashima-O'Leary, CISA, Director of Compliance
Gareth Sowinski, Qualified Security Assessor

Ironwood Commerce Systems | Grand Rapids, Michigan

July 2026

---

## Abstract

Ironwood Commerce Systems operates a point-of-sale and payments platform used at 8,700 restaurant and specialty retail locations across fourteen states. Since March 31, 2025, the future-dated requirements of the Payment Card Industry Data Security Standard (PCI DSS) version 4.0 have been mandatory rather than aspirational, and two of the franchisors whose brands run on our platform have set an internal compliance deadline of April 2026. This paper draws on Ironwood's own assessment records — 1,120 self-assessment questionnaires and 96 card-present security incidents recorded between 2021 and 2025 — to describe where multi-location operators are actually falling short, and why. We compare five paths to closing the gap: validated point-to-point encryption, tokenization, full network segmentation, outsourced hosted checkout, and a managed compliance service. We then build a cost and implementation model for a representative twelve-location operator, showing capital outlay, monthly recurring cost, and time to compliance under each path. Finally, we respond directly to the four objections we hear most often from operators: capital constraints, legacy hardware, offline mode during connectivity outages, and tip adjustment workflows. Our conclusion is that no single path is right for every operator, but that inaction is now measurably more expensive than any of the five paths, given rising acquirer non-compliance fees, franchisor mandates, and the litigation exposure demonstrated by a 2024 breach at a 38-location franchisee. This paper is written for franchise operators, restaurant technology directors, acquiring banks, and independent sales organizations who must decide, in the coming two quarters, how their locations will meet a standard that is no longer optional.

---

## 1. The Compliance Problem

### 1.1 A standard that has changed shape

PCI DSS 4.0 was published in 2022 with a transition period that allowed merchants to defer a defined set of new requirements — the so-called future-dated requirements — until March 31, 2025. That date has passed. Requirements that were previously "best practice until" are now mandatory for every merchant that stores, processes, or transmits cardholder data, regardless of size. For a platform operator like Ironwood, and for the thousands of independently owned locations that run our terminals, this is not a paperwork change. It converts several requirements that most small and mid-sized operators had never implemented — targeted risk analyses, payment page script integrity monitoring, authenticated internal vulnerability scanning, and phishing-resistant multifactor authentication for remote access — into baseline conditions of card acceptance.

### 1.2 Why this is landing on franchisees now

Card brand rules place compliance obligation on the merchant of record, but in franchise systems the practical enforcement mechanism runs through the franchisor's agreement with its acquiring bank and payment processor. Two large franchisors operating on the Ironwood platform have set an internal deadline of April 2026 for every location to demonstrate a passing PCI DSS assessment. This is materially earlier than card brand enforcement timelines and reflects franchisor exposure to brand-wide liability, insurance renewal terms, and their own contractual obligations to acquirers. The effect is that a franchisee who might have planned a phased, multi-year approach to PCI DSS 4.0 now has roughly eight months from the date of this paper to close a gap that, for many operators, spans several of the standard's most technically demanding requirements.

At the same time, acquiring banks have raised non-compliance fees. Where a monthly fee of $10 to $20 per merchant identifier was common as recently as 2023, we now see acquirers charging between $35 and $100 a month per MID for merchants who cannot demonstrate a current, passing assessment. For an operator with four locations, each with its own MID, that is up to $4,800 a year in fees that produce no security benefit whatsoever — money spent for non-compliance rather than on compliance.

### 1.3 The cost of getting it wrong is no longer theoretical

A 2024 card-present breach at a 38-location franchisee running on a competing platform resulted in a class action from affected cardholders, in addition to the usual forensic investigation, card brand fines, and card reissuance costs. That case is now cited routinely in franchisor risk committees and acquiring bank underwriting conversations. It has changed the conversation from "when will we get to this" to "what is our exposure right now."

### 1.4 The scope of the problem across the Ironwood base

Roughly 2,300 of our 8,700 locations — about 26 percent — are still running point-of-sale terminals on an operating system that lost vendor support in October 2025. These terminals no longer receive security patches, which means every new vulnerability disclosed against that operating system is now permanent and unremediated for as long as the terminal stays in service. This is the single largest structural exposure in our merchant base, and it interacts directly with the four most commonly failed requirements described in Section 2.

The remainder of this paper sets out what our assessment data shows, compares the five available remediation paths, builds a cost model for a representative operator, and answers the four objections we hear most consistently from franchise owners and operators.

---

## 2. What Ironwood Sees Across Its Merchant Base

### 2.1 Data sources

This section draws on three internal data sets maintained by Ironwood's compliance and security teams:

1. **1,120 self-assessment questionnaires (SAQs)** submitted by merchants on the Ironwood platform between 2023 and 2025, primarily SAQ P2PE and SAQ D for merchants, reflecting the mix of validated point-to-point encryption adopters and merchants handling cardholder data through other means.
2. **96 card-present security incidents** recorded from 2021 through 2025, including confirmed compromises, suspected compromises investigated by a forensic firm, and near-miss events identified through monitoring.
3. **Assessment outcomes** from Gareth Sowinski's qualified security assessor (QSA) firm, which performs on-site and remote assessments for a subset of Ironwood merchants subject to Level 1 or Level 2 validation requirements.

### 2.2 Where merchants fail

Across the 1,120 SAQs and associated assessment reviews, four requirement areas account for the large majority of findings. Table 1 summarizes the failure rate we observe in each area at first submission, before remediation.

**Table 1. Most frequently failed PCI DSS 4.0 requirement areas, Ironwood merchant base, 2023–2025 (n = 1,120 assessments)**

| Requirement Area | Approximate First-Pass Failure Rate | Typical Root Cause Observed |
|---|---|---|
| Targeted risk analysis (Req. 12.3.1 and related) | 71% | No documented process; merchants unaware the requirement applies to them individually rather than at the franchisor level |
| Payment page script integrity / tamper detection (Req. 6.4.3, 11.6.1) | 64% | Hosted checkout pages and in-store payment pages not inventoried; no mechanism to detect unauthorized script changes |
| Authenticated internal vulnerability scanning (Req. 11.3.1.2) | 58% | Scanning performed externally only, or performed unauthenticated; no credentialed scan of back-office and kitchen-network systems |
| Phishing-resistant MFA for remote access (Req. 8.4.2) | 53% | Remote access to POS management consoles secured with SMS or app-based MFA only, not phishing-resistant methods such as FIDO2 |

These four areas are not independent of one another. A merchant who has never performed a targeted risk analysis is, almost by definition, unlikely to have identified payment page script integrity or authenticated scanning as risks requiring a documented control. In practice, the four failures cluster together: an operator who fails one of these four requirement areas fails at least one other in 82 percent of the assessments we reviewed.

### 2.3 The legacy operating system problem

Of the 8,700 locations on the Ironwood platform, 2,300 — roughly 26 percent — run point-of-sale terminals on an operating system version that reached end of vendor support in October 2025. This is not evenly distributed: it concentrates heavily among operators who purchased hardware between 2018 and 2021 and have not refreshed it since. These terminals cannot receive security patches, cannot in most cases support the phishing-resistant authentication methods required under Requirement 8.4.2, and in several cases lack the processing capacity to run current endpoint monitoring agents required for authenticated scanning coverage.

This single factor is the strongest predictor in our data of both assessment failure and incident history. Locations running the unsupported operating system account for a disproportionate share of the 96 incidents described below.

### 2.4 Incident history, 2021–2025

Between 2021 and 2025, Ironwood recorded 96 card-present security incidents across the merchant base severe enough to trigger a forensic review, card brand notification, or both. Table 2 summarizes the incident count by year and the average cost impact for a representative four-location operator.

**Table 2. Card-present incidents and average cost impact, Ironwood merchant base, 2021–2025**

| Year | Incidents Recorded | Incidents Involving Unsupported OS Terminals | Average Cost for 4-Location Operator (forensics, fines, reissuance) |
|---|---|---|---|
| 2021 | 14 | 3 | $86,000 |
| 2022 | 17 | 5 | $91,000 |
| 2023 | 19 | 9 | $104,000 |
| 2024 | 24 | 14 | $126,000 |
| 2025 | 22 | 16 | $118,000 (year average) |
| **Total / average** | **96** | **47** | **$118,000 (5-year average)** |

The five-year average cost of $118,000 for a four-location operator breaks down approximately as follows: $38,000 in forensic investigation fees, $46,000 in card brand fines and assessments, and $34,000 in card reissuance costs charged back by the acquirer. These figures do not include lost business during remediation, the cost of temporary card acceptance suspension where imposed, or reputational effects that are harder to quantify but that operators consistently describe as significant, particularly in tightly-knit franchise markets where one location's breach becomes local news affecting sibling locations under the same brand.

The rising share of incidents involving unsupported operating system terminals — from 21 percent of incidents in 2021 to 73 percent in 2025 — is, in our assessment, the clearest single trend in the data. It tells us that the compliance gap is not spread evenly across the merchant base; it is concentrated in a defined, identifiable subset of locations, which has direct implications for how operators should prioritize remediation spending, discussed in Section 4.

### 2.5 Franchisor and acquirer pressure is accelerating

The April 2026 compliance mandates set by two large franchisors on our platform are not isolated. In conversations with acquiring bank partners over the past two quarters, we are seeing a consistent pattern: acquirers are moving non-compliance fees from a flat, low-cost annoyance into a fee structure intended to make non-compliance more expensive than remediation. At $35 to $100 per MID per month, an operator with eight locations who remains non-compliant through calendar year 2026 will pay between $3,360 and $9,600 in fees alone — money that produces no security improvement and does not reduce the operator's exposure to an incident of the kind described in Table 2.

---

## 3. Comparing the Five Compliance Paths

Operators on the Ironwood platform have five broad paths available to close the compliance gap described in Section 2. Each path addresses a different combination of the four most-failed requirement areas, and each carries a different cost and operational profile. This section describes each path and then compares them directly.

### 3.1 Validated point-to-point encryption (P2PE)

Validated P2PE replaces terminal hardware with devices that encrypt cardholder data at the point of card entry, using a solution validated by the PCI Security Standards Council, such that the merchant's own systems never handle unencrypted card data. This substantially reduces PCI DSS scope: a merchant using a fully validated P2PE solution can typically use the much shorter SAQ P2PE rather than SAQ D, eliminating many of the network segmentation and internal scanning requirements that apply to merchants handling data in the clear.

Cost on the Ironwood platform runs approximately $640 per lane in hardware and validated solution licensing, plus $19 a month per lane in ongoing service and key management fees. For a typical four-lane location, that is roughly $2,560 in capital cost and $76 a month in recurring cost.

P2PE does not, on its own, resolve the targeted risk analysis requirement, since that requirement applies at the organizational level regardless of technical architecture. It also does not address remote access authentication, since P2PE secures the card-present transaction path, not administrative access to POS management systems.

### 3.2 Tokenization

Tokenization replaces stored card numbers with a non-sensitive token that has no exploitable value if disclosed, typically used in combination with a gateway or processor tokenization vault. Where P2PE addresses the transaction at the terminal, tokenization primarily addresses stored and referenced card data used for repeat transactions, tip adjustments, and refunds after the original transaction has closed.

Tokenization cost varies by processor relationship; on the Ironwood platform, tokenization is included in gateway fees for most merchants already on our processing stack, with incremental cost concentrated in integration effort for point-of-sale software updates and staff retraining, typically $1,200 to $3,000 per location as a one-time integration cost with minimal ongoing fee increase.

Tokenization reduces the scope of stored data but does not by itself resolve network segmentation, script integrity, or authenticated scanning requirements, since it addresses data at rest rather than the surrounding network and application environment.

### 3.3 Full network segmentation

Full network segmentation isolates the cardholder data environment from the rest of the location's network — kitchen displays, guest Wi-Fi, back-office systems, and third-party devices such as loyalty tablets — using dedicated VLANs, firewalls, and access control. This is the most comprehensive technical remediation available and directly addresses the authenticated internal vulnerability scanning requirement, since a properly segmented environment reduces the scope of systems that must be scanned and monitored.

Cost is substantially higher than the other technical paths: approximately $14,000 per site, covering firewall hardware, managed switch replacement where needed, professional services for design and implementation, and the first year of managed monitoring. This path also carries the longest implementation timeline of the five, typically eight to twelve weeks per site including a site survey, cutover planning, and a period of parallel operation to confirm no disruption to guest-facing systems.

Full segmentation is the only one of the five paths that meaningfully addresses all four of the most commonly failed requirement areas simultaneously, because a well-segmented environment also constrains where remote access can reach and simplifies the scope of the targeted risk analysis.

### 3.4 Outsourced hosted checkout

For online and app-based ordering — an increasingly significant share of transaction volume for restaurant operators — outsourced hosted checkout moves the entire payment page to a PCI-validated third-party provider, so that the merchant's own web and app infrastructure never displays or processes the payment form. This directly resolves the payment page script integrity requirement, since script integrity monitoring becomes the hosted provider's obligation rather than the merchant's.

Cost is typically a per-transaction fee increment, commonly 0.1 to 0.3 percentage points above the merchant's existing processing rate, with no significant capital cost. This path is narrow in scope: it addresses only the digital ordering channel and does nothing for in-store, card-present risk, which remains the dominant channel for the incident history described in Section 2.

### 3.5 Managed compliance service

A managed compliance service, offered directly by Ironwood or by a qualified third party, takes over the ongoing operational burden of compliance: performing the targeted risk analysis on the merchant's behalf, running authenticated vulnerability scans on a schedule, managing phishing-resistant MFA deployment for remote access, and preparing SAQ documentation for the operator's signature. This path does not replace hardware or re-architect the network; it addresses the organizational and procedural gaps that are, per Table 1, the most commonly failed requirement areas.

Cost on the Ironwood platform is structured as a flat monthly fee per location, currently $185 to $240 a month depending on location complexity, with no significant capital outlay. This is the fastest path to initial compliance for the specific requirement areas it covers, typically achievable within four to six weeks per location, but it does not reduce technical exposure from legacy hardware or unsegmented networks; it manages the documentation and monitoring obligations around that exposure.

### 3.6 Comparative summary

Table 3 compares the five paths against cost, implementation time, and which of the four most-failed requirement areas each path addresses.

**Table 3. Comparison of five compliance paths**

| Path | Capital Cost (per site, typical) | Recurring Cost | Implementation Time | Targeted Risk Analysis | Payment Page Integrity | Authenticated Scanning | Phishing-Resistant MFA |
|---|---|---|---|---|---|---|---|
| Validated P2PE | ~$2,560 (4 lanes) | $76/mo (4 lanes) | 3–5 weeks | No | Partial | Reduces scope | No |
| Tokenization | $1,200–$3,000 | Minimal increase | 4–8 weeks | No | No | No | No |
| Full network segmentation | ~$14,000 | Monitoring fee, varies | 8–12 weeks | Indirect | No | Yes | Indirect |
| Outsourced hosted checkout | None | 0.1–0.3 pt of volume | 2–4 weeks | No | Yes | No | No |
| Managed compliance service | None | $185–$240/mo | 4–6 weeks | Yes | No | Yes | Yes |

No single path in Table 3 addresses all four requirement areas alone except full network segmentation, and even that path benefits from being paired with a managed compliance service to handle the documentation obligations that a technical control alone does not satisfy. In practice, the most effective and most commonly adopted approach among Ironwood's better-performing merchants combines two or three of these paths, matched to the operator's specific gaps as identified in an initial assessment. Section 4 builds a cost model around this combined approach.

---

## 4. Implementation and Cost Model for a Multi-Location Operator

### 4.1 The representative operator

To make the comparison in Section 3 concrete, we model a representative operator with twelve locations, four point-of-sale lanes per location, operating across two states, with six of the twelve locations running terminals on the unsupported operating system described in Section 2.3. This profile reflects the median operator size among franchisees affected by the April 2026 mandates on the Ironwood platform.

### 4.2 A phased approach

We recommend a three-phase implementation sequence, prioritizing the locations and requirement areas that carry the highest incident risk based on the pattern described in Section 2.4.

**Phase 1 (Months 1–2): Stop the bleeding.** Replace terminal hardware at the six locations running the unsupported operating system, deploying validated P2PE devices as the replacement hardware. This simultaneously resolves the hardware end-of-support problem and reduces SAQ scope for those six locations. Concurrently, enroll all twelve locations in a managed compliance service to begin the targeted risk analysis and authenticated scanning cycle, since these are organizational requirements that do not depend on hardware refresh timing.

**Phase 2 (Months 2–4): Close the digital channel gap.** Migrate online and app ordering at all twelve locations to outsourced hosted checkout, resolving payment page script integrity across the operator's full footprint in a single, low-capital step.

**Phase 3 (Months 3–7): Segment the highest-volume sites.** Apply full network segmentation to the four highest-transaction-volume locations first, where incident cost exposure is greatest, and complete the remaining eight locations by month seven. Phishing-resistant MFA for remote access is deployed alongside segmentation work at each site, since the segmentation project already requires network and firewall changes that make MFA deployment straightforward to bundle in.

### 4.3 Cost model

Table 4 shows the capital and recurring cost of this phased approach for the twelve-location operator, compared to the cost of doing nothing and continuing to pay acquirer non-compliance fees.

**Table 4. Twelve-location operator: three-year cost comparison, phased remediation vs. non-compliance**

| Cost Component | Phased Remediation (Total) | Non-Compliance Path (Total) |
|---|---|---|
| P2PE hardware, 12 sites × 4 lanes | $30,720 (one-time) | — |
| P2PE recurring, 12 sites × 4 lanes | $32,832 (3 years) | — |
| Managed compliance service, 12 sites | $79,920 (3 years, avg. $185/mo × 12) | — |
| Hosted checkout incremental processing cost | ~$18,000 (3 years, est. on volume) | — |
| Network segmentation, 12 sites | $168,000 (one-time) | — |
| Segmentation monitoring | $43,200 (3 years, est.) | — |
| Acquirer non-compliance fees, 12 MIDs | $0 | $86,400–$216,000 (3 years, at $50–$100/mo × 12 MIDs) |
| Expected incident cost (probabilistic, based on Table 2 incident rate applied to 12 sites) | Substantially reduced | Approx. $88,500 per year expected value at base rate, compounding brand and litigation risk |
| **Approximate 3-year total** | **~$373,000** | **~$350,000–$480,000, plus uncapped incident and litigation exposure** |

The comparison in Table 4 understates the case for remediation in one important respect: the non-compliance column reflects only fees and an expected-value estimate of incident cost drawn from Table 2's historical incident rate. It does not include the tail risk demonstrated by the 2024 class action following a 38-location breach, which represents a cost outcome far outside the average and one that no operator can absorb as a routine cost of doing business. When franchisor mandate enforcement — including the possibility of default under the franchise agreement for continued non-compliance past April 2026 — is added to the picture, the remediation path is the lower-risk choice even before its lower expected cost is considered.

### 4.4 Financing considerations

Several operators on our platform have financed the capital-intensive elements of this model — principally the network segmentation cost — through equipment financing arrangements offered by regional lenders familiar with restaurant and retail point-of-sale infrastructure, typically over 36 to 48 months. At a twelve-location scale, this converts the $168,000 segmentation capital cost into a monthly payment in the range of $4,200 to $5,600, depending on term and rate, which is comparable to or less than the non-compliance fee exposure shown in Table 4, while producing a durable security improvement rather than a recurring penalty.

---

## 5. Answering the Objections

Operators raise four objections consistently in conversations with our compliance and product teams. We take each in turn.

### 5.1 "We don't have the capital for this."

This objection is legitimate and we do not dismiss it. The phased approach in Section 4.2 is designed specifically to address it: Phase 1 and Phase 2 require no capital outlay comparable to full segmentation, and both close two of the four most commonly failed requirement areas. An operator who cannot fund the full three-phase model in the near term should still complete Phases 1 and 2, which cost roughly $63,552 over three years for a twelve-location operator (P2PE hardware and recurring cost plus managed compliance service), well below the three-year non-compliance fee exposure of $86,400 to $216,000 shown in Table 4. Financing options described in Section 4.4 exist specifically to spread the segmentation cost over a period that aligns with the operator's cash flow rather than requiring it upfront.

### 5.2 "Our hardware is legacy and we can't just replace it overnight."

We agree that a full hardware refresh across a multi-location footprint cannot happen overnight, which is why Phase 1 prioritizes the locations running the unsupported operating system rather than requiring a simultaneous refresh across the entire footprint. Locations running current, supported operating systems are not required to replace hardware to achieve compliance in the near term; they can proceed directly to enrollment in the managed compliance service and hosted checkout migration while hardware refresh at unsupported locations proceeds on its own schedule. We would note, however, that the data in Section 2.3 is unambiguous: locations on the unsupported operating system account for a disproportionate and growing share of incidents, and delaying hardware refresh at those specific locations carries risk that delaying refresh at supported locations does not.

### 5.3 "We need offline mode during connectivity outages, and we're worried these changes will break that."

This is a legitimate technical concern, and it is one that P2PE and network segmentation are specifically designed to accommodate rather than conflict with. Validated P2PE devices on the Ironwood platform retain local transaction queuing during connectivity loss, encrypting and storing transactions locally until connectivity resumes, exactly as current terminals do. Network segmentation, properly designed, isolates the cardholder data environment as a network zone but does not remove the local processing and storage capability that offline mode depends on; in fact, a well-designed segmented environment often improves offline reliability by isolating the point-of-sale VLAN from congestion or interference caused by guest Wi-Fi or kitchen display traffic on the same network. We recommend that any segmentation project include an explicit offline-mode test as part of the acceptance criteria before a site is considered complete, and we build this into our own implementation checklist for exactly this reason.

### 5.4 "Tip adjustment and post-authorization workflows depend on stored card data, and we're worried tokenization will break that."

Tokenization is designed to preserve exactly this workflow while removing the underlying risk. A token that references a specific transaction can be used for a tip adjustment or a delayed capture in the same way a stored card number is used today, without the token itself carrying exploitable value if disclosed. On the Ironwood platform, tokenization is implemented at the gateway level specifically to preserve tip adjustment, delayed capture, and refund workflows without requiring point-of-sale software to store or transmit the underlying card number after the initial authorization. We have not identified an operator workflow on our platform, including split-tender transactions and multi-day tip pooling adjustments common in full-service restaurant operations, that tokenization prevents; in every case we have reviewed, the workflow is preserved with a token substituted for the card number at the point where it would otherwise be stored.

---

## 6. Conclusion

The compliance problem described in this paper is not new in kind, but it is new in urgency. PCI DSS 4.0's future-dated requirements became mandatory in March 2025; two major franchisors on the Ironwood platform have set an April 2026 internal deadline; acquiring banks have raised non-compliance fees to a level intended to make continued non-compliance more expensive than remediation; and a 2024 breach at a 38-location franchisee has demonstrated that the downside tail of an incident now includes class-action litigation, not only forensic and reissuance cost.

Our own assessment data across 1,120 self-assessment questionnaires and 96 incidents from 2021 through 2025 shows a compliance gap that is concentrated and identifiable: it clusters around targeted risk analysis, payment page script integrity, authenticated internal vulnerability scanning, and phishing-resistant multifactor authentication for remote access, and it is strongly associated with the roughly 2,300 locations still running terminals on an operating system that lost support in October 2025.

No single one of the five paths compared in Section 3 closes this gap alone. The phased model built in Section 4 — combining validated point-to-point encryption at legacy-hardware locations, a managed compliance service across the full footprint, outsourced hosted checkout for digital ordering, and full network segmentation sequenced by transaction volume — offers a twelve-location operator a path to compliance within seven months at a total three-year cost comparable to, and in expected-value terms lower than, the cost of continued non-compliance, before accounting for the uncapped tail risk of an incident.

Operators who begin now have roughly eight months before the April 2026 franchisor deadline. Those who wait will face rising non-compliance fees, a shorter implementation window, and continued exposure at exactly the locations our data shows to be highest-risk. We recommend that operators use Table 1 and Table 3 in this paper as a starting checklist: identify which of the four most commonly failed requirement areas apply to your locations today, and match remediation investment to the path or combination of paths in Table 3 that closes those specific gaps, sequenced as described in Section 4.2.

---

## References

Payment Card Industry Security Standards Council. (2024). *Payment Card Industry Data Security Standard, Version 4.0.1: Requirements and Testing Procedures*. PCI Security Standards Council.

Payment Card Industry Security Standards Council. (2023). *PCI DSS v4.0 Future-Dated Requirements: Best Practices for Meeting the March 2025 Deadline*. PCI Security Standards Council.

Payment Card Industry Security Standards Council. (2024). *Self-Assessment Questionnaire Instructions and Guidelines, Version 4.0.1*. PCI Security Standards Council.

Ironwood Commerce Systems, Compliance Office. (2025). *Internal Merchant Assessment Database, 2023–2025* [Internal data set]. Grand Rapids, MI.

Ironwood Commerce Systems, Security Operations. (2025). *Card-Present Incident Log, 2021–2025* [Internal data set]. Grand Rapids, MI.

Sowinski, G. (2025). *Qualified Security Assessor Findings Summary, Ironwood Merchant Portfolio* [Internal assessment report]. Independent QSA Firm engagement with Ironwood Commerce Systems.

Verizon Business. (2025). *2025 Data Breach Investigations Report*. Verizon Enterprise Solutions.

National Restaurant Association. (2025). *Technology and Payments Compliance Survey: Franchise Operator Findings*. National Restaurant Association.

## Appendix A: Supporting Figure

**Figure 1. Card-present incidents by year, share attributable to unsupported operating system terminals, 2021–2025**

```
Incidents
25 |                                              ■■■■■■
24 |                                        ■■■■■■■■■■■■
23 |                                  ■■■■■■■■■■■■
22 |                            ■■■■■■■■■■■
21 |                      ■■■■■■■■■■
20 |
19 |                  ■■■■■■■■■■■■■■■■■■■
18 |
17 |            ■■■■■■■■■■■■■■■■■
16 |
15 |
14 |      ■■■■■■■■■■■■■■■
   +------------------------------------------------
       2021       2022       2023       2024       2025
       ■ Total incidents recorded
       ■ (right-shaded segment) Incidents involving unsupported OS terminals
```

*Note: Figure constructed from Table 2 data. The shaded proportion attributable to unsupported operating system terminals rises from 21 percent of total incidents in 2021 to 73 percent in 2025, while total incident count grows more modestly, from 14 to 22 over the same period. The widening gap between the two series is the clearest visual evidence in our data that the compliance and security exposure on the Ironwood platform is concentrated in a specific, identifiable subset of locations rather than distributed evenly across the merchant base.*

## Appendix B: Operator Self-Assessment Checklist

The following checklist is drawn directly from the four most commonly failed requirement areas identified in Table 1 and is intended for a franchise operator or restaurant technology director to complete before engaging with any of the five paths described in Section 3. It is not a substitute for a formal assessment by a qualified security assessor, but it identifies, in advance, which paths are most likely to close an operator's specific gaps.

**Table 5. Pre-engagement self-assessment checklist**

| Question | If "No," Relevant Path(s) |
|---|---|
| Has a targeted risk analysis been documented for this location within the past twelve months, specific to this merchant rather than inherited from the franchisor? | Managed compliance service |
| Is there a current inventory of every script running on payment pages, in-store and online, with a process to detect unauthorized changes? | Outsourced hosted checkout; managed compliance service |
| Are internal vulnerability scans performed with valid administrative credentials against back-office and kitchen-network systems, not only externally facing systems? | Full network segmentation; managed compliance service |
| Is remote access to point-of-sale management consoles secured with a phishing-resistant method (e.g., FIDO2 hardware key or platform passkey), rather than SMS or app-based one-time codes alone? | Full network segmentation (bundled MFA deployment); managed compliance service |
| Does any terminal at this location run an operating system version that reached end of vendor support before this checklist was completed? | Validated P2PE (hardware replacement) |
| Is cardholder data stored at this location for tip adjustment, delayed capture, or refund purposes using the actual card number rather than a token? | Tokenization |
| Is the cardholder data environment (point-of-sale network) on a separate network segment from guest Wi-Fi, kitchen display systems, and third-party tablets? | Full network segmentation |

An operator who answers "no" to four or more items on Table 5 should expect to need a combined approach similar to the phased model in Section 4.2 rather than a single path. An operator who answers "no" to two or fewer items, and whose remaining gaps concern documentation rather than technical architecture, is likely well served by the managed compliance service alone as an interim measure while planning any hardware or network work on a longer timeline.

## Appendix C: About the Authors

**Devika Ranganathan** is Chief Information Security Officer at Ironwood Commerce Systems, where she leads the security engineering and incident response functions referenced throughout this paper's incident data in Section 2.

**Thabo Mokoena** is Vice President of Product at Ironwood Commerce Systems and leads the product teams responsible for the validated P2PE, tokenization, and hosted checkout offerings described in Section 3.

**Erin Nakashima-O'Leary, CISA,** is Director of Compliance at Ironwood Commerce Systems and maintains the self-assessment questionnaire database referenced in Table 1 and Table 5.

**Gareth Sowinski** is a Qualified Security Assessor with the outside firm engaged by Ironwood to conduct on-site and remote assessments for merchants subject to Level 1 and Level 2 validation, and contributed the assessment findings summarized in Section 2.2.

## Appendix D: About Ironwood Commerce Systems

Ironwood Commerce Systems, headquartered in Grand Rapids, Michigan, provides point-of-sale and payments infrastructure to 8,700 restaurant and specialty retail locations across fourteen states. The company employs 260 people and works directly with franchisors, acquiring banks, and independent sales organizations to support compliance, security, and payment operations for its merchant base. This paper reflects data and analysis current as of July 2026 and will be updated as franchisor mandate deadlines and card brand enforcement guidance evolve.
