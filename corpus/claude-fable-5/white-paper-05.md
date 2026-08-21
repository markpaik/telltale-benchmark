# Closing the Evidence Gap: A Layered Temperature-Assurance Model for Refrigerated Fleets

**A White Paper of the Northern Reach Cold Chain Consortium**
Eau Claire, Wisconsin

**Authors:**
Malachi Odum, Executive Director, Northern Reach Cold Chain Consortium
Dr. Sofiya Kravchenko, Associate Professor of Supply Chain Management
Yumiko Tanaka-Reeves, Standards Director, Northern Reach Cold Chain Consortium

August 2026

---

## Executive Summary

Refrigerated carriers in the Upper Midwest face a converging set of pressures: rising cargo claims, receiver chargeback programs that penalize any documented temperature excursion, cargo insurance premiums that increased 34 percent at the most recent renewal, and active federal enforcement under the Sanitary Transportation of Human and Animal Food rule. The question is no longer whether temperature assurance justifies investment, but which combination of investments actually reduces losses.

This paper draws on the Consortium's dataset of 1.8 million trailer temperature logs recorded between 2022 and 2025 and 11,400 associated cargo claim files totaling $46.2 million. The data show that most excursions are operational rather than mechanical: door-open dwell at receiving docks accounts for 38 percent of excursions, setpoint entry error for 17 percent, and omitted precool for 14 percent. Only 9 percent trace to refrigeration unit failure. Claim severity is sharply skewed — the median claim is $4,050, but the largest 2 percent of claims carry 41 percent of total dollars.

Members have piloted five approaches individually: trailer-level telematics, pallet-level sensors, door sensors with dwell alarms, two-person precool and seal verification, and contract clauses that fix tolerance bands and pre-agree what counts as evidence. Each addresses part of the problem; none alone addresses the failure modes that drive the losses. The paper compares the five approaches against the observed excursion causes and presents an integrated model sized to a 120-trailer fleet: $1.4 million in capital, integration with the fleet's transportation management system, training for 340 drivers, and a ninety-day pilot with defined go/no-go criteria. Modeled against Consortium loss experience, the layered program addresses roughly 69 percent of excursion causes and reaches payback in approximately three years when claims, chargebacks, insurance, and administrative recoveries are counted.

The paper closes by answering the three objections most often raised by members: the cost burden on low-margin lanes, receivers who refuse to accept carrier sensor data, and disputes over who owns the temperature record.

---

## 1. The Problem: Excursions Have Become an Enterprise Risk

For most of the past two decades, temperature excursions in refrigerated trucking were treated as an operational nuisance — a cost of doing business that was absorbed through claims reserves, deductibles, and occasional customer concessions. Four developments have changed that calculus for carriers operating in the Northern Reach service area.

**First, the direct claims burden has grown.** Across the Consortium's nine member carriers and 4,100 reefer trailers, cargo claims attributable to temperature events totaled $46.2 million over the 2022–2025 period — an average of roughly $11.6 million per year, or approximately $2,800 per trailer per year. That figure understates the true cost, because it excludes freight charges forfeited on rejected loads, redelivery and disposal expense, and the administrative burden of claims processing, which member carriers estimate at $600 to $900 per claim file.

**Second, receivers have shifted from claims to chargebacks.** A national grocery retailer served by seven of the nine member carriers now deducts 3 percent of invoice on any load with a documented excursion — regardless of whether product was rejected, and regardless of fault. Because the chargeback attaches to the *documentation* of an excursion rather than to actual product loss, it converts every logged deviation into an immediate revenue event. Other receivers are adopting similar programs. Chargebacks bypass the claims process entirely: there is no adjuster, no salvage negotiation, and in most cases no practical appeal unless the carrier can produce contemporaneous evidence that the excursion occurred outside its custody or control.

**Third, cargo insurance has repriced.** At the January 2026 renewal, member carriers absorbed a 34 percent average premium increase on cargo coverage, with underwriters citing loss frequency, the severity tail in perishables claims, and the absence of verifiable monitoring on many insured loads. Several members were offered premium credits contingent on demonstrable continuous monitoring and documented corrective-action programs — a signal that underwriters now price the *evidence gap*, not just the loss history.

**Fourth, regulatory exposure is no longer theoretical.** Two federal enforcement actions under the FDA's Sanitary Transportation of Human and Animal Food rule (21 CFR Part 1, Subpart O) have named carriers operating in the region. The rule requires carriers who accept responsibility for temperature control to maintain conditions adequate to prevent food from becoming unsafe, to demonstrate — on request of the shipper or receiver — that conditions were maintained, and to train personnel in sanitary transportation practices. An excursion that a carrier cannot explain, and a training program that a carrier cannot document, are now compliance findings as well as commercial losses.

The combined effect is that a temperature excursion now generates cost through four channels simultaneously: the claim itself, the chargeback, the insurance loss run, and the regulatory record. A carrier that reduces excursion frequency by half does not merely halve its claims — it compounds savings across all four channels. The remainder of this paper asks what the data say about *where* excursions come from, which interventions match those causes, and what a fully specified program costs and returns.

---

## 2. The Evidence Base: 1.8 Million Logs and 11,400 Claims

### 2.1 The Dataset

The Consortium maintains a pooled dataset covering calendar years 2022 through 2025:

- **1.8 million temperature logs** from member trailers, comprising reefer unit download files, trailer telematics records, and — on instrumented lanes — pallet-level logger data.
- **11,400 cargo claim files** with a combined incurred value of $46.2 million, each coded for root cause where the file evidence supported a determination.

The pooled structure matters. No single member carrier generates enough excursion events in a given lane or commodity to draw statistically stable conclusions; nine carriers together do. All figures below are Consortium-wide unless otherwise noted.

### 2.2 Where Excursions Come From

Root-cause coding of excursion events yields the distribution shown in Table 1 and Figure 1.

**Table 1. Root causes of temperature excursions, Consortium dataset, 2022–2025.**

| Root cause | Share of excursion events | Character of the failure |
|---|---|---|
| Door-open dwell at receiving docks | 38% | Operational, at destination, often outside driver control |
| Setpoint entry error | 17% | Human data-entry error at dispatch or loading |
| Omitted precool | 14% | Process omission before loading |
| Defrost cycles misread as excursions | 12% | Measurement/interpretation artifact, not product risk |
| Refrigeration unit failure | 9% | Mechanical |
| Other / undetermined | 10% | Mixed |

**Figure 1. Excursion causes as a share of events (2022–2025).**

```
Door-open dwell      ████████████████████████████████████░░  38%
Setpoint error       ████████████████░                       17%
Omitted precool      █████████████░                          14%
Defrost artifacts    ███████████░                            12%
Unit failure         ████████░                                9%
Other/undetermined   █████████░                              10%
```

Three findings deserve emphasis.

**Excursions are predominantly operational, not mechanical.** Unit failure — the failure mode that trailer telematics is best suited to detect — accounts for only 9 percent of events. By contrast, the three leading causes (door dwell, setpoint error, omitted precool) are all human or process failures, and together account for 69 percent of events. Any assurance program that instruments the refrigeration unit but not the process around it leaves more than two-thirds of the problem unaddressed.

**A meaningful share of "excursions" are not excursions at all.** Twelve percent of coded events are defrost cycles — normal, brief return-air temperature rises during automatic defrost — that were read by a receiver or a claims adjuster as evidence of product exposure. These events generate chargebacks and disputes despite posing no product risk. They are, strictly, an *evidence* problem: the carrier's data was either absent or insufficiently granular to distinguish a fifteen-minute return-air spike from a sustained load-temperature deviation. Pulp temperatures and pallet-level data resolve nearly all such disputes; trailer-level return-air data alone frequently does not.

**The largest single cause occurs at the receiver's dock.** Door-open dwell at receiving — trailers held at the door with doors open, or opened and left waiting — is the leading cause at 38 percent. This has an important commercial implication: the party imposing 3 percent chargebacks for documented excursions is, in a substantial fraction of cases, the party whose dock operations caused the excursion. Without door-event and location data, the carrier absorbs the chargeback. With it, the carrier has a documented basis to contest liability. Section 5 returns to this point.

### 2.3 Claim Severity: A Heavy Tail

**Table 2. Claim severity distribution, 11,400 claims, $46.2 million incurred.**

| Measure | Value |
|---|---|
| Total claims, 2022–2025 | 11,400 |
| Total incurred | $46.2 million |
| Mean claim | $4,053 |
| Median claim | $4,050 |
| Largest 2% of claims (≈228 files) — share of dollars | 41% (≈$18.9 million) |
| Average value, top-2% claims | ≈$83,000 |

The median claim of $4,050 describes the typical event: a partial rejection, a pallet or two of downgraded product, a temperature-abuse allegation settled at salvage value. But the largest 2 percent of claims — roughly 228 files over four years — carry 41 percent of the dollars, averaging approximately $83,000 each. These are full-load rejections of high-value protein and dairy, multi-stop loads where an early excursion condemned every subsequent delivery, and disputed rejections where the absence of granular data forced settlement at or near full invoice value.

Review of the top-2-percent files shows two recurring characteristics. First, they are concentrated in causes that continuous monitoring detects early: unit failure and omitted precool, where an alert in the first hour of transit converts a $90,000 full-load loss into a repositioned load or a partial claim. Second, they are disproportionately *evidence* failures: in a majority of the large disputed files, member carriers settled not because the evidence showed carrier fault, but because the carrier could not produce evidence at all. The severity tail is therefore doubly addressable — by earlier detection and by better records.

### 2.4 The Full Cost per Trailer

Combining claims with chargeback and insurance effects, the Consortium estimates the annual excursion-related cost burden at $4,800 to $5,600 per trailer per year: approximately $2,800 in direct claims, $1,100 to $1,500 in chargebacks on excursion-documented loads, and the balance in insurance premium loading and claims administration. For the 120-trailer reference fleet used in Section 4, that is an addressable annual exposure of roughly $580,000 to $670,000.

---

## 3. Five Approaches Compared

Member carriers have piloted five approaches over the study period, typically one at a time. This section assesses each against the cause distribution in Table 1 and the evidence requirements described above.

### 3.1 Trailer-Level Telematics Alone

**What it is.** Telematics units integrated with the refrigeration unit report setpoint, return-air and discharge-air temperature, unit mode, fuel level, and alarms at intervals, with GPS position.

**What it addresses.** Unit failure (9 percent of causes) — telematics detects mechanical faults early and enables en-route intervention. It also detects setpoint discrepancies *if* someone compares the reported setpoint to the order requirement, which requires TMS integration that most standalone deployments lack.

**Where it falls short.** Return-air temperature is not product temperature. Telematics cannot see inside the load, cannot distinguish a defrost cycle's effect on air temperature from product exposure, and provides no direct evidence of door events or precool completion. Members who deployed telematics alone reported good mechanical uptime and almost no reduction in claims frequency, because the leading causes remained invisible.

**Cost.** Roughly $1,800–$3,200 per trailer installed, plus $15–$30 per trailer per month connectivity.

### 3.2 Pallet-Level Sensors

**What it is.** Single-use or returnable loggers placed in or on pallets, recording product-adjacent temperature at short intervals; costs run $9 to $27 per shipment depending on device class, real-time capability, and return logistics.

**What it addresses.** The evidence gap, comprehensively. Pallet-level data resolves defrost-artifact disputes (12 percent of causes), documents conditions at the product across the full custody chain including receiver dock dwell, and supports zone-level determinations on multi-temp and multi-stop loads. In the Consortium's disputed-claim files, loads carrying pallet-level data settled at an average of 44 percent of the initially claimed amount; loads without it settled at 78 percent.

**Where it falls short.** Cost prohibits universal deployment: at $9–$27 per shipment across a 120-trailer fleet running roughly 21,000 loads per year, blanket coverage would cost $190,000 to $560,000 annually. Sensors also do not *prevent* excursions — they document them. And some receivers refuse to accept or return devices, or decline to recognize carrier sensor data (addressed in Section 5).

### 3.3 Door Sensors with Dwell Alarms

**What it is.** Magnetic or optical door-status sensors reporting open/close events with timestamps and location, with configurable alarms when doors remain open beyond a threshold or open outside a geofence.

**What it addresses.** The single largest cause — door-open dwell at receiving, 38 percent of events. Door data serves two functions: real-time alerting (a driver or dispatcher notified at minute ten of an open-door dwell can intervene before product warms) and liability documentation (a timestamped record that doors opened inside the receiver's geofence and remained open for 47 minutes shifts the chargeback conversation decisively). Door sensors are also the cheapest layer, at roughly $400–$700 per trailer when installed alongside telematics.

**Where it falls short.** Door data without temperature data shows exposure, not consequence; without pallet data, a receiver can still argue product was harmed. And alerting is only as good as the response protocol behind it — a dwell alarm that rings at a dispatch desk with no escalation procedure changes nothing.

### 3.4 Two-Person Precool and Seal Verification

**What it is.** A procedural control: before loading, a second person independently verifies that the trailer has been precooled to the required temperature (measured, not assumed), that the setpoint matches the order, and that the seal is applied and recorded, with both signatures captured electronically.

**What it addresses.** Omitted precool (14 percent) and a substantial share of setpoint entry error (17 percent) — together nearly a third of causes — at almost no capital cost. One member carrier running this procedure on protein lanes for eighteen months saw precool-related excursions fall by more than 80 percent on covered lanes.

**Where it falls short.** It is labor-dependent and erodes without auditing; compliance in the pilot carrier drifted from 96 percent in the first quarter to 71 percent by the fourth until electronic checklist enforcement was added. It also does nothing after departure: it cannot detect en-route failure or dock dwell, and generates no continuous record.

### 3.5 Contract Clauses: Tolerance Bands and Pre-Agreed Evidence

**What it is.** Shipper-carrier (and where possible three-party) agreements that specify, in advance: the temperature tolerance band and measurement point (product pulp versus air), the excursion definition (magnitude *and* duration thresholds, with defrost cycles excluded), the authoritative data source, and the claims/chargeback procedure that follows a documented event.

**What it addresses.** The dispute layer. A large share of the dollar losses in the Consortium files arises not from product damage but from *disagreement about what the data means* — most visibly the 12 percent of events that are defrost artifacts, and the chargebacks applied to brief, shallow deviations that no food-safety standard would treat as significant. Members with evidence clauses in place report materially faster claim resolution and a meaningful reduction in chargebacks on technically compliant loads.

**Where it falls short.** Clauses require leverage; carriers on low-margin spot freight rarely have it. Clauses also presuppose data worth pre-agreeing about — a carrier with no monitoring gains little from a clause naming its data authoritative.

### 3.6 Summary Comparison

**Table 3. Approaches mapped to excursion causes and program functions.**

| Approach | Door dwell (38%) | Setpoint error (17%) | Omitted precool (14%) | Defrost artifacts (12%) | Unit failure (9%) | Prevents? | Documents? | Approx. cost |
|---|---|---|---|---|---|---|---|---|
| Trailer telematics alone | — | Partial* | — | — | **Yes** | Partly | Partly | $1,800–$3,200/trailer + monthly |
| Pallet-level sensors | Documents | Documents | Documents | **Resolves** | Documents | No | **Yes** | $9–$27/shipment |
| Door sensors + dwell alarms | **Yes** | — | — | — | — | Yes (with response protocol) | Yes | $400–$700/trailer |
| Two-person precool/seal | — | **Yes** | **Yes** | — | — | Yes | Checklist only | Labor only |
| Contract evidence clauses | Allocates liability | — | — | **Yes** | — | No | Governs | Legal/negotiation |

\* Only when integrated with TMS order data so reported setpoint is automatically compared to the order requirement.

The pattern is unambiguous: **no single approach covers more than about a third of the cause distribution, and the prevention tools and the evidence tools are different tools.** Telematics and procedures prevent; pallet sensors and clauses document and allocate. The losses run through both channels — excursions that happen, and excursions (real or apparent) that cannot be explained. The program that works is therefore necessarily layered.

---

## 4. The Layered Fleet Model: Specification, Cost, and Pilot Design

### 4.1 Design Logic

The reference model is sized to a 120-trailer fleet with 340 drivers — representative of the mid-size member carrier — and is built on four principles derived from Section 2:

1. **Instrument every trailer for the causes that occur on every trailer.** Telematics with reefer-control integration and door sensors go fleet-wide, because unit health, setpoint verification, and dock dwell are universal exposures.
2. **Deploy pallet-level sensing by risk tier, not universally.** Per-shipment sensors are targeted to (a) commodities and lanes represented in the top-2-percent claim tail, (b) receivers running chargeback programs, and (c) multi-stop and multi-temp loads — an estimated 35 percent of shipments, capturing an estimated 80-plus percent of dollar exposure.
3. **Wire the data into the TMS so alerts become interventions.** A setpoint reported by the reefer that does not match the setpoint on the order should generate an automatic exception before the trailer leaves the yard; a door-dwell alarm should route to a named responder with an escalation path.
4. **Put procedure and contract around the technology.** Two-person precool/seal verification becomes an electronic gate in the dispatch workflow, and evidence clauses are negotiated into shipper agreements as instrumented lanes come online.

### 4.2 Capital Budget

**Table 4. Capital budget, 120-trailer reference fleet.**

| Line item | Basis | Cost |
|---|---|---|
| Trailer telematics with reefer-control integration and two-zone probes | $2,850 × 120 trailers | $342,000 |
| Door sensors with dwell alarms and geofencing | $640 × 120 trailers | $76,800 |
| Pallet-level sensor program: returnable device pool, gateways, initial single-use inventory | Risk-tiered coverage, ~35% of loads | $214,000 |
| TMS integration: order-to-setpoint matching, exception dashboard, alert routing, receiver data portal | Fixed | $310,000 |
| Data platform and tamper-evident record archive (retention, audit trail, export formats) | Fixed | $187,000 |
| Driver and dispatcher training: curriculum development, delivery, electronic checklist tooling | $430 × 340 drivers | $146,200 |
| Precool/seal verification program: SOPs, e-checklists, high-security seals, audit protocol | Fixed | $48,000 |
| Pilot management, third-party data validation, baseline measurement | Fixed | $76,000 |
| **Total capital** | | **$1,400,000** |

Ongoing operating cost is estimated at **$168,000 per year** ($1,400 per trailer per year), covering connectivity, platform subscriptions, sensor consumables on single-use lanes, device pool attrition, and annual refresher training.

### 4.3 Modeled Return

Applying the Consortium loss experience to the 120-trailer fleet (Section 2.4: $580,000–$670,000 annual addressable exposure, midpoint $625,000), and assuming the layered program achieves a 65 percent reduction in the causes it directly addresses (69 percent of events) plus dispute-resolution improvements on the remainder:

**Table 5. Modeled annual benefit, 120-trailer fleet, steady state.**

| Benefit channel | Basis | Annual value |
|---|---|---|
| Claims avoided (prevention: dwell response, setpoint gating, precool verification, early unit-failure intervention) | ~65% reduction on 69% of causes, applied to $338K direct claims | $152,000 |
| Severity-tail reduction (early detection converting full-load losses to partial or repositioned loads) | Applied to top-2% exposure share | $118,000 |
| Chargebacks avoided or successfully contested (defrost artifacts, receiver-dock dwell documentation) | Applied to ~$165K chargeback run rate | $105,000 |
| Insurance premium credit and loss-run improvement | Underwriter-indicated monitoring credit | $90,000 |
| Claims administration savings (faster resolution, fewer files) | ~$700/file × avoided/expedited files | $55,000 |
| **Gross annual benefit** | | **$520,000** |
| Less operating cost | | ($168,000) |
| **Net annual benefit** | | **$352,000** |

At $1.4 million capital and $352,000 net annual benefit, simple payback is approximately **4.0 years on internal savings alone**. Two factors improve the realistic case. First, several member shippers have indicated willingness to pay a monitoring premium of $15–$40 per load on instrumented lanes, which — even at modest uptake — moves payback toward three years. Second, the model assigns no value to regulatory risk reduction, retained business at chargeback-active receivers, or the underwriting position at future renewals; all are real, and all favor the investment.

### 4.4 The Ninety-Day Pilot

Full deployment should follow, not precede, a structured pilot. The recommended design instruments **20 trailers on two lanes** — one high-value protein lane into a chargeback-active receiver, one produce lane with historical dwell problems — with a matched control group of 20 uninstrumented trailers on comparable freight.

**Figure 2. Ninety-day pilot timeline.**

```
Days 1–15    Install hardware; TMS integration to test environment;
             baseline measurement from prior 12 months on both lanes
Days 16–30   Train pilot drivers and dispatchers; activate two-person
             precool/seal gate; alerting in shadow mode (logged, not routed)
Days 31–75   Live operation: alerts routed with escalation protocol;
             pallet sensors on all pilot loads; weekly exception review
Days 76–90   Third-party data validation; pilot vs. control comparison;
             go/no-go decision against pre-set criteria
```

**Go/no-go criteria, set before day one:** (a) ≥50 percent reduction in excursion events versus control on covered causes; (b) ≥90 percent alert-to-response compliance within defined response windows; (c) 100 percent of pilot loads with a complete, exportable temperature record from precool through delivery; (d) at least one chargeback or claim dispute resolved in the carrier's favor using pilot data. A pilot that meets these criteria justifies fleet-wide rollout on the Table 4 budget; a pilot that fails them limits sunk cost to roughly $290,000 and identifies which layer underperformed.

Training deserves specific emphasis. The 340-driver curriculum is not device training; it is *response* training — what a dwell alarm means, who to call, what the driver is empowered to do at a receiver's dock, and how the electronic precool/seal checklist works. Consortium experience is blunt on this point: the member pilots that failed did not fail on hardware. They failed on the human response to what the hardware reported.

---

## 5. Objections and Answers

Three objections recur in member deliberations. Each deserves a direct answer.

### 5.1 "We can't carry this cost on low-margin lanes."

The objection is real: on spot freight running at 3–5 percent operating margin, a $1,400-per-trailer annual operating cost plus capital recovery is material. Three responses.

**First, the model does not spread cost evenly — it tiers it.** The expensive per-shipment layer (pallet sensors) deploys only on the 35 percent of loads carrying an estimated 80-plus percent of dollar exposure. Low-margin, low-risk lanes carry only the fleet-wide layers (telematics, door sensors, procedure), whose combined incremental cost is under $100 per trailer per month — less than a single median claim per trailer every three-and-a-half years, against an observed claims run rate of one median-equivalent claim per trailer *per year*.

**Second, the low-margin lane is precisely where a chargeback hurts most.** A 3 percent chargeback on a load running a 4 percent margin erases three-quarters of the margin. The lanes least able to afford monitoring are the lanes least able to afford unexplained excursions.

**Third, the cost is partially recoverable.** Monitoring-premium pricing on instrumented lanes, insurance credits, and — for consortium members — pooled purchasing on hardware and connectivity (which produced the per-unit figures in Table 4, roughly 20 percent below single-fleet list pricing) all offset the burden. A carrier that cannot justify the program fleet-wide can still capture the majority of the benefit by starting with the risk-tiered lanes and the procedural controls, whose cost is nearly zero.

### 5.2 "Receivers won't accept our sensor data."

Some receivers decline to recognize carrier-generated temperature data, insisting on their own dock readings. Four responses.

**First, the data does not need receiver acceptance to prevent losses.** Prevention — dwell response, setpoint gating, precool verification, early failure detection — operates entirely inside the carrier's own operation. The majority of the modeled benefit in Table 5 accrues whether or not any receiver ever looks at the data.

**Second, refusal to accept data is not refusal of its legal effect.** In claims litigation and in FSMA compliance, contemporaneous, tamper-evident, continuously recorded data from calibrated devices carries evidentiary weight regardless of what a receiving clerk will sign for. The two federal enforcement actions in the region turned on carriers' *inability to produce* records; a carrier that can produce them is in a categorically different position with regulators, insurers, and courts.

**Third, the contract layer converts the objection into a negotiation.** The evidence-clause approach in Section 3.5 exists precisely to settle *in advance* whose data governs. Where the carrier's shipper customer — who bears its own interest in defensible cold-chain records under FSMA — is party to the clause, receiver resistance diminishes sharply. Member experience is that shippers, once shown pallet-level data quality, frequently become advocates for its acceptance downstream.

**Fourth, the receiver refusing the data is often the receiver causing the excursion.** With 38 percent of excursions arising from receiving-dock dwell, timestamped door and location data documents events on the receiver's premises. Several members have successfully reversed chargebacks by presenting dwell records showing doors opened inside the receiver's geofence and held open beyond the receiver's own dock standards. Data a receiver refuses to accept is still data the receiver must answer.

### 5.3 "Who owns the record?"

Ownership questions arise in three forms: as between carrier and shipper, as between carrier and technology vendor, and in discovery — the fear that a comprehensive record becomes evidence *against* the carrier.

**Carrier–shipper.** The Consortium's recommended contract position: the carrier owns records generated by carrier-owned devices on carrier equipment; the shipper receives a contractual right of access to records for its loads, in defined formats, on defined timelines. This mirrors FSMA's own structure, under which the carrier must *demonstrate* conditions on request — a demonstration obligation, not a transfer of ownership. Where the shipper supplies the loggers, ownership reverses and the carrier negotiates the reciprocal access right, so that shipper-owned data cannot be selectively withheld in a dispute.

**Carrier–vendor.** Members should not sign monitoring agreements in which the vendor owns the data and licenses it back. The Consortium's model procurement terms require: carrier ownership of all telemetry; raw-data export in open formats at no additional charge; data return and deletion on contract termination; and retention on the carrier's schedule, not the vendor's. Every major vendor in the members' evaluations agreed to these terms when asked; the terms are only unavailable to carriers who do not ask.

**Discovery exposure.** The candid answer is that comprehensive records occasionally document a carrier's own failure — and that this is still the better position. The claims data are decisive: disputed files *with* complete records settled at 44 percent of claimed value on average; files *without* them settled at 78 percent, because a carrier with no data cannot rebut any allegation. The record that shows an occasional carrier fault also shows every receiver-dock dwell, every defrost artifact misread as abuse, and every load delivered in tolerance. Under a regulatory regime that already obligates the carrier to demonstrate temperature control, the absence of records is not a shield; it is a finding.

A governance note: retention should be fixed by policy (the Consortium recommends the longer of three years or the applicable claims limitation period), applied uniformly, and never adjusted in response to a specific dispute.

---

## 6. Conclusion

The Consortium's four years of pooled data support a conclusion that is uncomfortable for anyone hoping a single purchase will solve the problem: temperature losses in refrigerated trucking flow through two distinct channels — excursions that happen, and excursions that cannot be explained — and the tools that address one channel do not address the other. Trailer telematics watches the 9 percent of causes that are mechanical. Pallet sensors document everything and prevent nothing. Door sensors attack the largest single cause but need a response protocol behind them. Procedural verification eliminates precool and setpoint failures cheaply but decays without enforcement and stops at the yard gate. Contract clauses settle disputes but require data worth disputing over.

Layered together, matched to the cause distribution, and wired into the TMS so that alerts become interventions, these tools address roughly 69 percent of excursion causes directly and materially improve the carrier's position on the remainder. For a 120-trailer fleet the fully specified program costs $1.4 million in capital and $168,000 a year to operate, returns a modeled $352,000 a year net against documented loss experience, and reaches payback in three to four years before counting monitoring-premium revenue, retained business, or regulatory risk reduction. A ninety-day, twenty-trailer pilot with pre-set go/no-go criteria limits the at-risk commitment to under $300,000 while producing the lane-level evidence needed for a full-deployment decision.

The commercial environment has already decided the alternative. Receivers are charging back 3 percent of invoice on any documented excursion; insurers have repriced the absence of monitoring by 34 percent; and federal enforcement has arrived in the region. In that environment, the carrier without a record does not avoid the cost of temperature assurance — it pays that cost through every claim it cannot rebut, every chargeback it cannot contest, and every renewal it cannot negotiate. The question before member fleets is not whether to pay for temperature evidence, but whether to own it.

---

## References

1. U.S. Food and Drug Administration. *Sanitary Transportation of Human and Animal Food; Final Rule.* 21 CFR Part 1, Subpart O. Federal Register, Vol. 81, No. 66 (April 6, 2016).

2. U.S. Food and Drug Administration. *Guidance for Industry: Sanitary Transportation of Human and Animal Food — Small Entity Compliance Guide.* FDA Center for Food Safety and Applied Nutrition, 2017.

3. Northern Reach Cold Chain Consortium. *Pooled Temperature Log and Claims Dataset, 2022–2025: Methodology and Coding Manual.* Eau Claire, WI: NRCCC Standards Office, 2026.

4. Global Cold Chain Alliance. *Cold Chain Best Practices Guide: Transportation.* Arlington, VA: GCCA, 2023.

5. Mercier, S., Villeneuve, S., Mondor, M., and Uysal, I. "Time–Temperature Management Along the Food Cold Chain: A Review of Recent Developments." *Comprehensive Reviews in Food Science and Food Safety*, 16(4), 2017, pp. 647–667.

6. Ndraha, N., Hsiao, H.-I., Vlajic, J., Yang, M.-F., and Lin, H.-T. V. "Time–Temperature Abuse in the Food Cold Chain: Review of Issues, Challenges, and Recommendations." *Food Control*, 89, 2018, pp. 12–21.

7. American Trucking Associations. *Refrigerated Division Annual Claims and Operations Survey.* Arlington, VA: ATA, 2025.

8. Kravchenko, S. "Evidence Asymmetry in Perishable Cargo Claims: Settlement Outcomes With and Without Continuous Monitoring Data." Working paper, Regional University Supply Chain Center, 2026.
