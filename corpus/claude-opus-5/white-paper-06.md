# The Franchise Compliance Gap: PCI DSS v4.0.1 and the Multi-Location Payment Environment

**A White Paper from Ironwood Commerce Systems**
Grand Rapids, Michigan

**Authors:**
Devika Ranganathan, Chief Information Security Officer, Ironwood Commerce Systems
Thabo Mokoena, Vice President of Product, Ironwood Commerce Systems
Erin Nakashima-O'Leary, CISA, Compliance Director, Ironwood Commerce Systems
Gareth Sowinski, QSA, Meridian Assurance Partners

*Published July 2026*

---

## Abstract

The future-dated requirements of the Payment Card Industry Data Security Standard version 4.0 became mandatory on March 31, 2025. Fifteen months later, the operational consequences are concentrated not at the enterprise level but at the franchisee level, where compliance obligations are being pushed downward through franchise agreements to operators who have neither dedicated security staff nor the capital plans to absorb infrastructure change on a compliance calendar.

Ironwood Commerce Systems serves 8,700 restaurant and specialty retail locations across fourteen states. This paper reports what our compliance and assessment data show across that base: 1,120 self-assessment questionnaires filed between 2021 and 2025, 96 card-present security incidents in the same period, and assessment outcomes that identify four requirements failing far more often than any others. The average incident in our data cost a four-location operator $118,000 in forensic investigation, card brand assessments, and card reissuance. Approximately 2,300 locations in our base continue to run payment terminals on an operating system that reached end of support in October 2025.

The paper compares five remediation paths available to multi-location operators — validated point-to-point encryption, tokenization, full network segmentation, outsourced hosted checkout, and managed compliance services — on scope reduction, capital cost, recurring cost, and operational disruption. It presents a five-year cost model for a representative twelve-location operator and addresses the four objections we hear most consistently from operators: capital constraint, legacy hardware, offline transaction handling during connectivity outages, and tip adjustment workflows.

Our conclusion is that validated point-to-point encryption combined with tokenization produces the largest scope reduction per dollar for the typical franchise operator, that full network segmentation is rarely justifiable below roughly forty locations, and that the compliance deadlines now being set by franchisors — including two April 2026 mandates affecting operators in our base — leave insufficient time for sequential deployment. Operators who have not begun should begin now.

---

## 1. The Problem Stated

### 1.1 What Changed

PCI DSS v4.0 was published in March 2022 with a transition structure unusual in the standard's history. Version 3.2.1 was retired on March 31, 2024. A second tier of requirements — the "future-dated" requirements, fifty-one of them — remained best practice until March 31, 2025, at which point they became mandatory for all assessments. Version 4.0.1, published in June 2024, clarified language but did not move the date.

The future-dated requirements are not incremental. They introduce obligations that did not previously exist in any form: documented targeted risk analyses for requirements with customized frequencies, integrity monitoring of scripts executing on payment pages, authenticated internal vulnerability scanning, phishing-resistant multifactor authentication for all remote access into the cardholder data environment, and expanded requirements around access to and management of cryptographic material.

For a large merchant with a security team, these are project items. For a franchisee operating four locations with a general manager who handles technology alongside scheduling and inventory, they are something else. Several of them cannot be satisfied by purchasing a product. A targeted risk analysis is a document that must be written, reviewed, and updated, and it must reflect the actual environment of the actual merchant.

### 1.2 The Downward Push

Franchise agreements have long contained provisions requiring franchisees to comply with applicable law and with brand technology standards. What has changed since March 2025 is enforcement. Franchisors that previously treated PCI compliance as a franchisee responsibility in the abstract are now treating it as an auditable brand standard with consequences attached.

Two franchisors representing a combined 1,340 locations in the Ironwood base have set April 2026 as the date by which all franchised locations must demonstrate validated compliance, defined in both cases as a completed and signed self-assessment questionnaire of the appropriate type plus passing quarterly external scans from an approved scanning vendor. One of the two has stated that failure to demonstrate compliance constitutes a curable default under the franchise agreement.

The economic pressure is reinforced from the acquiring side. Non-compliance fees assessed by acquirers on merchants who have not validated have risen materially. Across the acquirers serving our merchant base, monthly non-compliance fees now range from $35 to $100 per merchant identifier. For a twelve-location operator with a merchant identifier per location, the annual exposure at the high end is $14,400 — an amount that begins to approach the cost of actually solving the problem.

And there is litigation. A 2024 breach at a 38-location franchisee in our base was followed by a putative class action filed on behalf of affected cardholders. The franchisor was named. The suit is unresolved as of this writing, but its existence has changed how franchisors think about franchisee compliance, and it is the single factor most cited to us by franchise technology leadership when explaining the timing of new mandates.

### 1.3 Why This Paper

Ironwood occupies an unusual vantage point. We are the payment platform for 8,700 locations, we hold their assessment outcomes and questionnaire responses, and we handle incident response coordination when something goes wrong. We see which requirements fail, how often, and what happens next. We also sell products that address some of these failures, and we want to be direct about that: this paper recommends approaches, several of which we implement commercially. We have tried to present the comparative data in a form that supports the reader's own analysis rather than ours, and Mr. Sowinski's participation as an independent qualified security assessor is intended to constrain the temptation toward self-service.

---

## 2. What the Merchant Base Shows

### 2.1 Assessment Outcomes

Between January 2021 and December 2025 we collected 1,120 self-assessment questionnaires from merchants in our base. The distribution across questionnaire types is itself informative and is presented in Table 1.

**Table 1. Self-assessment questionnaire type by merchant count, Ironwood base, 2021–2025 (n=1,120)**

| SAQ Type | Description | Merchants | Share |
|---|---|---|---|
| SAQ B-IP | Standalone PTS terminals, IP-connected | 218 | 19.5% |
| SAQ C | Payment application connected to internet | 496 | 44.3% |
| SAQ D (Merchant) | All other card-present environments | 291 | 26.0% |
| SAQ P2PE | Validated P2PE solution, hardware terminals | 87 | 7.8% |
| SAQ A / A-EP | E-commerce, outsourced or partially outsourced | 28 | 2.5% |

The concentration in SAQ C and SAQ D is the central fact. Together they account for 70.3 percent of merchants and, because these tend to be the larger multi-location operators, a larger share of transaction volume. SAQ C contains 139 requirements. SAQ D for merchants contains over 250. SAQ P2PE contains 33.

That differential is the entire argument for scope reduction, and it is worth stating plainly: the same physical business, running the same number of lanes and taking the same cards, faces roughly eight times the documentation burden depending on how its payment path is architected.

### 2.2 The Four Failures

Across the assessments we hold, and consistent with what Meridian observes in its own QSA practice across a broader merchant population, four requirements fail disproportionately. Table 2 summarizes.

**Table 2. Most frequently failed PCI DSS v4.0.1 requirements, Ironwood merchant base, assessments conducted April 2025 – June 2026 (n=634 assessments)**

| Requirement | Description | Failure rate | Primary cause of failure |
|---|---|---|---|
| 12.3.1 | Targeted risk analysis for each requirement with customized frequency | 71% | Document does not exist; frequency chosen without documented rationale |
| 6.4.3 / 11.6.1 | Payment page script inventory, authorization, integrity monitoring | 63% | No inventory; third-party tags added by marketing without review |
| 11.3.1.2 | Authenticated internal vulnerability scanning | 58% | Scans run unauthenticated; credentials not provisioned to scanner |
| 8.4.2 / 8.5.1 | MFA for all access into the CDE; phishing-resistant factors for remote access | 54% | SMS or app-push MFA in use where phishing-resistant factor required; vendor remote access unmanaged |

A note on each.

**Targeted risk analyses (12.3.1).** This is the highest-failure requirement in our data and the least understood. Version 4.0 introduced flexibility: several requirements allow the entity to define its own frequency for a periodic activity rather than following a prescribed interval. The price of that flexibility is a documented analysis justifying the chosen frequency, reviewed at least annually. Merchants hear "flexibility" and do not hear "documented analysis." The remedy is not technical. It is roughly six to twelve hours of structured writing per merchant, and it is the single cheapest requirement to fix in our entire dataset.

**Payment page script integrity (6.4.3, 11.6.1).** Applies to merchants whose payment pages are served from systems they control, including many restaurant online ordering environments. The failure mode is consistent: a marketing team or a third-party ordering vendor adds an analytics tag, a chat widget, or a pixel to a page that also collects card data. Nobody inventories it. Nobody authorizes it. Nothing monitors it for change. This is the requirement that exists because of Magecart-class attacks, and it is the requirement where the gap between paper compliance and actual risk reduction is narrowest — the attacks it addresses are real and active.

**Authenticated internal vulnerability scanning (11.3.1.2).** Merchants who scan at all frequently scan without credentials, which produces a report showing far fewer findings than the environment actually contains. The fix is provisioning scanner credentials and rerunning. The cost is low. The reason it fails is that the unauthenticated report looked clean and nobody questioned it.

**Phishing-resistant MFA (8.4.2, 8.5.1).** Version 4.0.1 requires multifactor authentication for all access into the cardholder data environment, and the guidance on remote access has pushed the market toward phishing-resistant factors — FIDO2 security keys or platform authenticators — in place of one-time codes and push notifications. Two populations fail here: merchants using SMS-based codes, and merchants whose POS vendor, hardware maintenance contractor, or kitchen display integrator holds standing remote access credentials that nobody has inventoried. The second population is the more dangerous.

### 2.3 Incidents

We coordinated response on 96 card-present security incidents in our merchant base between 2021 and 2025. Figure 1 describes their distribution by initial vector.

**Figure 1. Card-present incidents by initial access vector, Ironwood merchant base, 2021–2025 (n=96)**

```
Remote access compromise (vendor or operator credentials)   ████████████████████████  38  (39.6%)
Malware on back-office workstation with CDE connectivity    ██████████████  22  (22.9%)
Physical terminal tampering / skimming                      ███████████  17  (17.7%)
Unpatched OS or application on POS endpoint                 ████████  13  (13.5%)
Insider / social engineering of staff                       ████  6  (6.3%)
```

Nearly forty percent of incidents began with compromised remote access. This is the requirement (8.5.1) failing at 54 percent in our assessment data, and it is the vector producing the most incidents. The correspondence is not coincidental.

The financial consequences are concentrated. Table 3 summarizes cost by operator size.

**Table 3. Mean incident cost by operator size, Ironwood merchant base, 2021–2025**

| Operator size | Incidents | Mean total cost | Forensics (PFI) | Card brand assessments | Reissuance & fraud | Other* |
|---|---|---|---|---|---|---|
| 1–3 locations | 41 | $74,000 | $31,000 | $19,000 | $18,000 | $6,000 |
| 4–9 locations | 33 | $118,000 | $42,000 | $34,000 | $33,000 | $9,000 |
| 10–24 locations | 15 | $216,000 | $58,000 | $71,000 | $74,000 | $13,000 |
| 25+ locations | 7 | $487,000 | $86,000 | $164,000 | $198,000 | $39,000 |

*\*Other includes legal counsel, notification, credit monitoring where offered, and temporary staffing. Excludes litigation and excludes business interruption.*

The $118,000 figure for a four-to-nine location operator is the number we cite most often in conversation with merchants, because it is the modal franchisee in our base. It is worth noting what it excludes: litigation, lost business, and the cost of the operator's own time. The 38-location franchisee whose 2024 breach produced the pending class action has, by its own account, spent more on legal defense than on remediation.

Note also that costs scale faster than linearly with location count. This is because assessments and reissuance scale with the number of cards exposed, which scales with transaction volume, while forensic costs scale with environment complexity rather than size. A large operator does not get a discount.

### 2.4 The Operating System Problem

Approximately 2,300 locations in our base — 26.4 percent — run payment terminals or POS endpoints on an operating system that reached end of support in October 2025. These systems no longer receive security patches.

This creates an immediate and unresolvable failure of Requirement 6.3.3, which requires that critical and high-severity patches be installed within one month of release. There is no compensating control that makes an unpatched, unsupported operating system compliant in the general case. A QSA may accept isolation-based compensating controls for a bounded period while a replacement is procured, but this is a bridge, not a destination, and Mr. Sowinski's practice will not accept it for a second consecutive assessment cycle absent evidence of an executing replacement plan.

These 2,300 locations are the population most exposed to the April 2026 franchisor mandates, and they are disproportionately the population with the least capital available.

---

## 3. The Five Paths

Five architectural approaches are available to a multi-location operator seeking compliance. They are not mutually exclusive; in practice the best outcomes combine two or three. We describe each, then compare.

### 3.1 Validated Point-to-Point Encryption (P2PE)

A PCI-validated P2PE solution encrypts card data within the terminal's secure card reader, at the moment of read, using keys the merchant never holds. The encrypted data traverses the merchant's network as ciphertext that the merchant cannot decrypt. Decryption occurs at the solution provider's secure environment.

The compliance effect is the largest available from any single measure. A merchant using a validated P2PE solution with no other electronic cardholder data storage becomes eligible for SAQ P2PE: 33 requirements, down from 139 (SAQ C) or 250-plus (SAQ D). The merchant's network drops out of scope for segmentation, internal scanning, and most access control requirements as they apply to cardholder data.

The critical qualifier is *validated*. A solution described as "P2PE" or "end-to-end encryption" that does not appear on the PCI SSC's list of validated P2PE solutions does not confer SAQ P2PE eligibility. It may still reduce risk. It does not reduce documented scope. We see merchants confuse these constantly, and the confusion is sometimes encouraged by vendors.

Cost in the Ironwood implementation: approximately $640 per lane in hardware and deployment, plus $19 per lane per month for solution provider services, key management, and terminal lifecycle. Deployment per location runs four to six hours including staff training.

### 3.2 Tokenization

Tokenization replaces the primary account number with a surrogate value that has no exploitable relationship to the original. The token can be stored, referenced, and reused for subsequent operations — refunds, recurring charges, tip adjustments, loyalty matching — without the merchant retaining card data.

Tokenization addresses storage; P2PE addresses transmission. They solve different halves of the problem, and this is why they pair well. P2PE alone leaves an operator who needs post-authorization card reference in an awkward position. Tokenization alone leaves data in the clear during capture.

For restaurant operators specifically, tokenization is what makes tip adjustment work without card data retention — an issue we address directly in Section 6.4.

Cost in the Ironwood implementation: no per-lane hardware. $0.004 per tokenized transaction, or a flat $45 per location per month above 11,250 monthly transactions. Integration effort at the POS layer, typically covered by platform upgrade for merchants on current Ironwood releases.

### 3.3 Full Network Segmentation

Segmentation isolates the cardholder data environment from the rest of the merchant network using firewalls, VLANs, and access control lists, such that systems outside the segment are out of scope. It does not reduce the requirements applying to the segment; it reduces what is inside it.

Segmentation is the traditional approach and remains valid. It is also the most expensive, the most operationally demanding, and the one most likely to degrade over time. Segmentation requires annual penetration testing to validate that the isolation holds (Requirement 11.4.5). It requires firewall rule review every six months. It requires that every network change — a new kitchen display, a new music system, a new guest Wi-Fi access point — be evaluated against the segmentation boundary.

In our experience, segmentation implemented at a franchise location degrades within eighteen months absent ongoing network management, because the people making network changes at a restaurant are not the people who designed the segmentation.

Cost: approximately $14,000 per site in equipment, design, and implementation. Annual penetration testing of segmentation adds $6,000 to $18,000 per environment depending on how many distinct network designs exist across the operator's locations.

### 3.4 Outsourced Hosted Checkout

For the e-commerce and online ordering portion of a restaurant business, redirecting the payment step to a PCI-compliant service provider's hosted page or embedding an iframe served entirely by the provider removes the merchant's systems from the card data path. Where implemented completely, the merchant may qualify for SAQ A — 31 requirements.

This path does nothing for card-present transactions, which are the majority of restaurant volume. But it addresses the payment page script integrity requirements (6.4.3, 11.6.1) failing at 63 percent in our data, and it addresses them more cleanly than script monitoring does. A merchant with a full redirect has no payment page scripts to monitor.

The tradeoff is control over the customer experience. Operators with strong brand requirements around the ordering flow resist redirects. Iframe implementations preserve more of the visual experience but must be implemented precisely; a partial implementation that leaves any card field on merchant-controlled markup drops the merchant to SAQ A-EP and reintroduces the script requirements.

Cost: typically included in payment processing arrangements. Integration effort of 20 to 60 hours depending on ordering platform.

### 3.5 Managed Compliance Service

A managed compliance service does not change architecture. It supplies the people and process that franchise operators lack: questionnaire completion support, targeted risk analysis authoring, evidence collection, scan scheduling and remediation tracking, policy templates, and annual review.

This addresses a different failure mode than the other four paths. Requirements 12.3.1 (targeted risk analysis), and much of Requirement 12 generally, fail not because the merchant's architecture is wrong but because nobody wrote anything down. Architecture cannot fix that.

We are candid that a managed service applied to a badly architected environment produces expensive documentation of non-compliance. The correct sequence is architecture first, managed service to sustain it.

Cost in the Ironwood implementation: $340 per location per month for operators under ten locations, declining to $210 per location per month above twenty-five locations.

### 3.6 Comparison

**Table 4. Comparative assessment of the five paths**

| | P2PE (validated) | Tokenization | Full segmentation | Hosted checkout | Managed compliance |
|---|---|---|---|---|---|
| **Scope reduction** | Very high (SAQ D/C → P2PE, 33 reqs) | Moderate (eliminates storage scope) | High within CDE boundary; no SAQ change | High for CNP only (SAQ A, 31 reqs) | None |
| **Addresses 12.3.1 (TRA)** | Reduces applicable TRAs | No | No | Reduces applicable TRAs | Yes — directly |
| **Addresses 6.4.3 / 11.6.1** | N/A (card-present) | No | No | Yes — eliminates | Partial (monitoring only) |
| **Addresses 11.3.1.2** | Largely eliminates | No | No — increases scan burden | N/A | Yes — operationalizes |
| **Addresses 8.4.2 / 8.5.1** | Reduces CDE access surface | No | No | Reduces | Yes — inventory and enforcement |
| **Resolves EOL OS exposure** | Yes, if terminal replaced | No | No — isolates only | Partial | No |
| **Capital per location (4 lanes)** | $2,560 | $0 | $14,000 | $0 | $0 |
| **Recurring per location/month** | $76 | $45 | $180 (mgmt + amortized pen test) | $0 | $210–$340 |
| **Deployment time per location** | 4–6 hours | 1–2 hours | 3–5 days | N/A (central) | 2 weeks onboarding |
| **Offline mode preserved** | Yes (store-and-forward) | Yes | Yes | N/A | N/A |
| **Tip adjustment preserved** | Yes, with tokenization | Yes | Yes | N/A | N/A |
| **Degrades without maintenance** | Low | Low | High | Low | N/A |
| **Best suited to** | All card-present operators | All operators | 40+ locations, central IT | Operators with online ordering | Operators without security staff |

The pattern in Table 4 is that no single path is sufficient and that two of the five — P2PE and tokenization — deliver most of the available scope reduction at the lowest cost per location. Segmentation delivers less scope reduction per dollar and carries the highest ongoing operational risk. Hosted checkout is essentially free and should be adopted by any operator with online ordering, but it addresses a minority of transaction volume. Managed compliance addresses the documentation failures that architecture cannot.

Our recommendation for the typical franchise operator is P2PE plus tokenization plus hosted checkout for the online channel, with managed compliance for operators lacking internal capacity, and segmentation reserved for operators above roughly forty locations with dedicated IT staff or for specific locations where P2PE is not achievable.

---

## 4. Implementation Model: A Twelve-Location Operator

To make the economics concrete, we model a representative operator: twelve restaurant locations, four payment lanes per location (48 lanes total), currently on SAQ C, with online ordering through a third-party platform, no dedicated IT staff, and nine of twelve locations running terminals on the October 2025 end-of-support operating system.

This profile matches 84 operators in our base within a reasonable tolerance.

### 4.1 Phasing

**Table 5. Recommended implementation sequence, twelve-location operator**

| Phase | Duration | Activities | Locations affected |
|---|---|---|---|
| 0 — Assessment | Weeks 1–3 | Scope validation, network discovery, remote access inventory, vendor account audit | All 12 |
| 1 — Immediate risk | Weeks 2–6 | Phishing-resistant MFA deployment; disable or credential unmanaged vendor access; authenticated scanning stood up | All 12 |
| 2 — Documentation | Weeks 4–10 | Targeted risk analyses authored; policies updated to v4.0.1; incident response plan tested | All 12 |
| 3 — EOL remediation + P2PE | Weeks 8–20 | Terminal replacement with P2PE-validated devices, 3 locations per 3-week wave | 9 first, then 3 |
| 4 — Tokenization | Weeks 12–22 | POS configuration for token vault; tip adjustment and refund flows converted and tested | All 12 |
| 5 — Online channel | Weeks 14–20 | Hosted checkout iframe implementation; script inventory retired | Central |
| 6 — Validation | Weeks 22–28 | SAQ P2PE completion, quarterly ASV scan, attestation to franchisor and acquirer | All 12 |

Total elapsed time: approximately 28 weeks, or six and a half months. An operator facing an April 2026 franchisor deadline and beginning in July 2026 is already past it. An operator beginning in August 2026 for a deadline in early 2027 has adequate margin.

Phase 1 deserves emphasis. Deploying phishing-resistant MFA and auditing vendor remote access addresses the vector behind 39.6 percent of the incidents in our dataset, costs very little, and can be completed in under six weeks. It should not wait for the architecture work. An operator who does nothing else this quarter should do this.

### 4.2 Cost Model

**Table 6. Five-year cost model, twelve-location operator, 48 lanes**

| Line item | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Five-year total |
|---|---|---|---|---|---|---|
| **Capital** | | | | | | |
| P2PE terminals & deployment (48 lanes @ $640) | $30,720 | — | — | — | $10,240¹ | $40,960 |
| Network remediation (non-segmentation) | $8,400 | — | — | — | — | $8,400 |
| Implementation labor (internal + Ironwood) | $11,500 | — | — | — | — | $11,500 |
| **Recurring** | | | | | | |
| P2PE service (48 lanes @ $19/mo) | $10,944 | $10,944 | $10,944 | $10,944 | $10,944 | $54,720 |
| Tokenization (12 loc @ $45/mo) | $6,480 | $6,480 | $6,480 | $6,480 | $6,480 | $32,400 |
| Managed compliance (12 loc @ $340/mo) | $48,960 | $48,960 | $48,960 | $48,960 | $48,960 | $244,800 |
| ASV quarterly scanning | $2,400 | $2,400 | $2,400 | $2,400 | $2,400 | $12,000 |
| **Total outlay** | **$119,404** | **$68,784** | **$68,784** | **$68,784** | **$79,024** | **$404,780** |
| | | | | | | |
| **Avoided cost** | | | | | | |
| Acquirer non-compliance fees (12 MIDs @ $70/mo)² | ($9,240)³ | ($10,080) | ($10,080) | ($10,080) | ($10,080) | ($49,560) |
| **Net five-year cost** | | | | | | **$355,220** |
| **Net cost per location per year** | | | | | | **$5,920** |

*¹ Terminal refresh, one-third of fleet, beginning year 5.*
*² Midpoint of observed $35–$100 range.*
*³ Eleven months, assuming compliance achieved in month two of validation.*

### 4.3 Comparison Against Alternatives

**Table 7. Five-year total cost, twelve-location operator, by approach**

| Approach | Five-year cost | Resulting SAQ | Requirements in scope |
|---|---|---|---|
| Status quo (non-compliance fees only) | $60,480 fees + unquantified risk | None valid | 139+ unmet |
| Full segmentation + managed compliance | $482,600 | SAQ D | 250+ |
| P2PE + tokenization + managed compliance (recommended) | $355,220 | SAQ P2PE | 33 |
| P2PE + tokenization, self-managed | $110,420 | SAQ P2PE | 33 |

The self-managed row is included because some operators can do it. An operator with a capable general manager, a supportive franchisor providing templates, and the discipline to maintain documentation can achieve SAQ P2PE compliance for roughly $110,000 over five years — $1,840 per location per year. The managed service premium of $244,800 buys the assurance that it actually gets done and stays done. In our base, operators who attempt self-management without prior compliance experience fail their second-year attestation at a rate of roughly one in three.

### 4.4 Risk-Adjusted View

The status quo row in Table 7 shows $60,480 in non-compliance fees over five years, which is cheaper than any remediation path. Operators notice this. The response requires putting a number on the risk.

In our base, the annualized card-present incident rate over 2021–2025 was 0.22 percent per location-year among merchants on SAQ C or D with no P2PE, and 0.03 percent per location-year among merchants on validated P2PE. For a twelve-location operator over five years:

- Without P2PE: 12 × 5 × 0.0022 = 0.132 expected incidents
- With P2PE: 12 × 5 × 0.0003 = 0.018 expected incidents

At the $216,000 mean cost for a 10–24 location operator (Table 3), expected incident cost falls from $28,512 to $3,888 — a $24,624 reduction. That alone does not justify $355,220 in spending, and we will not pretend it does.

What justifies the spending is the tail. The distribution of incident costs is heavily right-skewed. The 25+ location mean of $487,000 excludes litigation, and the 38-location franchisee facing class action has incurred defense costs alone exceeding that figure. Add the franchise agreement default exposure — the loss of the franchise itself — and the calculation stops being an expected-value problem and becomes a solvency problem. Operators do not buy fire insurance because the expected value is positive.

There is also the matter that non-compliance fees are not a purchased indulgence. Acquirers assess them as a spur to compliance, and acquirers reserve the right to terminate merchant agreements. An operator whose acquirer exits leaves the operator scrambling to reboard at worse rates, if at all.

---

## 5. What the Franchisor Mandates Require

Operators frequently ask what, precisely, satisfies an April 2026-type mandate. Based on the language of the two mandates in our base and on Meridian's review:

1. **A completed and signed SAQ of the correct type.** The most common error is filing SAQ A or SAQ B-IP when the environment requires SAQ C or D. A signed attestation to the wrong questionnaire is worse than no attestation; it is a false statement.

2. **Passing quarterly ASV scans** of all external-facing IP addresses associated with the payment environment, from a scanning vendor on the PCI SSC's approved list, with all findings above the passing threshold remediated and rescanned.

3. **Evidence of the future-dated requirements.** Both mandates specifically enumerate targeted risk analyses, MFA coverage, and — for operators with online ordering — payment page script inventories. These are exactly the requirements failing in Table 2. This is not coincidence; the franchisors are reading the same assessment data we are.

4. **Attestation of compliance from service providers.** Operators must collect and retain AOCs from their POS platform, payment processor, and any third party touching card data. Ironwood publishes its AOC annually and provides a responsibility matrix; not all vendors do, and an operator whose online ordering vendor cannot produce an AOC has a problem that predates any mandate.

---

## 6. The Objections

Four objections come up in nearly every operator conversation. Each is legitimate. Each has an answer.

### 6.1 "I don't have the capital."

The Year 1 capital in Table 6 — $50,620 across twelve locations, or $4,218 per location — arrives at a time when restaurant operators are managing labor cost inflation, softening traffic, and in many cases remodel obligations under franchise agreements. This is a real constraint, not an excuse.

Three responses.

First, sequence. Phase 1 of Table 5 — MFA and vendor access remediation — costs under $4,000 across all twelve locations and addresses the vector behind 39.6 percent of incidents. Phase 2, the documentation work, costs internal time and addresses the highest-failure requirement in our data. An operator can materially improve both risk posture and mandate readiness for under $15,000, before touching hardware. Do that first.

Second, financing. Terminal capital is financeable. Ironwood offers 36-month terms at rates that convert the $30,720 terminal outlay to approximately $940 per month, moving it from capital to operating expense. Several acquirers offer similar arrangements, occasionally with fee waivers during the deployment period. Ask.

Third, the terminals need replacing anyway. Nine of the twelve modeled locations run end-of-support operating systems. Those terminals are not compliant, are not patchable, and are not supportable. The capital is not incremental to compliance; it is a deferred replacement cycle that compliance is forcing into the present. The honest framing is that the operator has been running on borrowed time and the loan is being called.

### 6.2 "My hardware is legacy and my POS won't support this."

Two distinct concerns.

For terminals: end-of-support terminals cannot be brought into compliance. There is no path. The compensating control conversation — isolate the device, restrict its network reachability, monitor it intensively — buys a bounded period, typically one assessment cycle, during which a replacement plan must be executing. Mr. Sowinski's practice will document such controls once, with a dated remediation plan attached, and will not accept the same controls in the following cycle. Operators should treat this as a twelve-month runway, not a solution.

For POS software: the concern is usually that a P2PE terminal will not integrate with an older POS version. This is sometimes true. Ironwood's semi-integrated P2PE architecture is specifically designed to address it — the terminal communicates directly with the payment gateway and returns only a token and approval status to the POS, meaning the POS requires a relatively thin integration rather than a full card data handling path. We support this architecture back to Ironwood platform release 8.2, which covers 91 percent of our installed base. Operators on releases older than 8.2 need a platform upgrade, which is a separate conversation with its own cost.

Operators on third-party POS platforms should ask their vendor two questions: does the platform support semi-integrated P2PE, and can the vendor produce a current AOC. A "no" to either is a finding, and it belongs in the operator's risk register regardless of what else they do.

### 6.3 "What happens when the internet goes down?"

This is the objection we take most seriously, because operators are right to raise it and because it is where poorly designed compliance architectures genuinely hurt businesses.

A restaurant that cannot take payment during a connectivity outage does not merely lose transactions; it loses seated guests, staff morale, and reputation. Operators who have experienced a bad outage under a cloud-dependent payment system are permanently skeptical, and reasonably so.

The answer is store-and-forward. In a properly designed P2PE deployment, when the terminal cannot reach the gateway, it reads the card, encrypts the data within the secure reader as it always does, and stores the encrypted transaction locally in the terminal's secure element. When connectivity returns, the queued transactions are forwarded for authorization.

Three properties matter for compliance and for operations:

- The stored data is ciphertext the merchant cannot decrypt. It does not constitute cardholder data storage for scoping purposes, and it does not create SAQ D obligations.
- Storage is within the PCI PTS-approved secure card reader, not on the POS or a back-office system. The POS never holds anything but a token reference and a pending status.
- Authorization risk transfers according to the terms of the merchant agreement. Offline transactions are approved on a floor-limit basis; some will decline on forward. This is a business risk, not a compliance risk, and it exists identically in non-P2PE offline modes.

Ironwood's default configuration permits offline store-and-forward up to a $75 transaction floor limit and a 72-hour queue depth, both operator-configurable. Across our P2PE base in 2025, the mean offline forward decline rate was 1.4 percent of offline transactions, and offline transactions were 0.6 percent of total volume — an aggregate exposure of roughly 8 basis points of gross card volume.

The compliance architecture is not what creates outage risk. Connectivity does. P2PE is neutral on this, and a well-configured P2PE deployment handles outages better than many legacy integrated systems because the secure reader is a purpose-built device rather than a general-purpose computer.

### 6.4 "Tip adjustment won't work."

The full-service restaurant workflow — authorize at the table or counter for the check amount, print a slip, capture a signed tip, adjust the authorization before batch close — requires the ability to reference the original transaction hours after the card has left. Operators reasonably fear that removing card data from their environment removes that ability.

It does not, and this is precisely what tokenization exists for.

In the Ironwood implementation, the initial authorization returns a token alongside the approval. The token is a persistent reference to the transaction and to the underlying card, held in the vault. The POS stores the token. When the server enters the tip, the POS transmits an adjustment referencing the token and the new amount. At batch close, the adjusted amounts settle. No card data is ever present in the POS, the back-office system, or the operator's network.

The workflow the staff sees is unchanged. Server presents check, guest pays, slip prints, tip entered, batch closes. Training time in our deployments averages 25 minutes per location, and it is almost entirely about the terminal's physical interface rather than the tip process.

The same mechanism supports the other post-authorization operations restaurants need: partial refunds, split adjustments, incremental authorizations for bar tabs, recurring charges for catering accounts, and card-on-file matching for loyalty. Each references the token.

Two caveats. First, an operator who currently retains full PANs in the POS database to support these workflows — and some legacy configurations do — is holding cardholder data and is on SAQ D whether they have filed one or not. Migrating to tokens is not a new burden; it is the resolution of an existing violation. Second, token vaults are provider-specific. Tokens issued by Ironwood's vault do not port to another provider's vault without a migration process. Operators should understand this as a switching cost and should ask about token portability terms before signing. We think that is a fair question and we answer it in writing.

---

## 7. Conclusion

The compliance gap in franchised retail and restaurant payments is not primarily a technology gap. The technology to remove card data from a franchisee's environment has existed for a decade and is neither exotic nor expensive relative to other capital the operator routinely deploys. The gap is one of information, capacity, and timing.

What our data show is a merchant base in which seven of ten operators carry the heaviest available compliance burden — SAQ C or SAQ D — when a substantially lighter one is architecturally available to them. In which the four most-failed requirements are, three of the four, matters of documentation and configuration rather than capital. In which the vector behind two of every five incidents is unmanaged remote access, addressable in six weeks for under $4,000 at a twelve-location operator. And in which 2,300 locations are running payment endpoints on an operating system that stopped receiving patches nine months ago.

The pressures are now aligned in a way they were not before March 2025. Franchisors are enforcing, because a class action taught them what franchisee negligence costs the brand. Acquirers are pricing, at $35 to $100 per merchant identifier per month. And the standard itself has moved to a place where the old approach — file the easiest questionnaire, hope nobody looks — has become a documented false attestation rather than an ambiguity.

Our recommendations:

**For operators.** Begin with remote access. Inventory every credential held by every vendor, contractor, and integrator. Deploy phishing-resistant MFA. Do this in the next sixty days regardless of what else you decide. Then write your targeted risk analyses, or have someone write them. Then, on a financed basis if necessary, move to validated P2PE with tokenization and get to SAQ P2PE. If you have online ordering, move the payment step to a hosted iframe and delete your script inventory problem. Do not build full segmentation unless you are above forty locations and have someone whose job it is to maintain it.

**For franchisors.** Mandates without support produce attestations without compliance. The franchisees most likely to breach are the ones least able to fund remediation, and a deadline alone will not change that. Consider approved-vendor programs with negotiated pricing, template documentation for the requirements that fail on paperwork rather than architecture, and phased deadlines that acknowledge a 28-week implementation cycle.

**For acquirers and ISOs.** Non-compliance fees have become a revenue line. The merchants paying them longest are the merchants most likely to generate a loss event, and the fee is not priced to the risk. Fee revenue from a merchant who eventually breaches is a poor trade. Consider directing that revenue toward remediation subsidy for merchants who commit to a documented plan.

The date has passed. What remains is the work.

---

## References

1. PCI Security Standards Council. *Payment Card Industry Data Security Standard: Requirements and Testing Procedures, Version 4.0.1.* Wakefield, MA: PCI SSC, June 2024.

2. PCI Security Standards Council. *PCI DSS v4.x: Targeted Risk Analysis Guidance.* Information Supplement. Wakefield, MA: PCI SSC, June 2024.

3. PCI Security Standards Council. *Payment Card Industry Point-to-Point Encryption Standard: Solution Requirements and Testing Procedures, Version 3.1.* Wakefield, MA: PCI SSC, 2021.

4. PCI Security Standards Council. *Self-Assessment Questionnaire P2PE and Attestation of Compliance, Version 4.0.1.* Wakefield, MA: PCI SSC, 2024.

5. PCI Security Standards Council. *Guidance for PCI DSS Requirements 6.4.3 and 11.6.1.* Information Supplement. Wakefield, MA: PCI SSC, 2025.

6. PCI Security Standards Council. *Information Supplement: Guidance for PCI DSS Scoping and Network Segmentation.* Wakefield, MA: PCI SSC, revised 2024.

7. PCI Security Standards Council. *Information Supplement: Multi-Factor Authentication.* Wakefield, MA: PCI SSC, revised 2025.

8. Verizon. *2025 Payment Security Report.* Basking Ridge, NJ: Verizon Business, 2025.

9. Verizon. *2025 Data Breach Investigations Report.* Basking Ridge, NJ: Verizon Business, 2025.

10. National Institute of Standards and Technology. *Digital Identity Guidelines: Authentication and Lifecycle Management.* NIST Special Publication 800-63B, Revision 4. Gaithersburg, MD: NIST, 2024.

11. International Franchise Association Educational Foundation. *Franchise Business Economic Outlook.* Washington, DC: IFA, 2025.

12. Ironwood Commerce Systems. *Merchant Assessment and Incident Response Dataset, 2021–2025.* Internal, Grand Rapids, MI, 2026. Aggregate figures cited in this paper; underlying merchant-level data not published.

---

*Correspondence regarding this paper may be directed to the Ironwood Commerce Systems compliance office. Ironwood Commerce Systems provides payment platform, point-to-point encryption, tokenization, and managed compliance services described in this paper and has a commercial interest in several of the approaches evaluated. Meridian Assurance Partners is an independent PCI Qualified Security Assessor company and conducts assessments of Ironwood merchants; Meridian receives no compensation from Ironwood for product recommendations and did not participate in the pricing sections of this document. This paper is informational and does not constitute a compliance validation, legal advice, or a guarantee of assessment outcome.*
