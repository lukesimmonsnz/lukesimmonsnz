---
title: "Digital inclusion gaps in Wellington region"
section: infrastructure
subpage: digital-connectivity
order: 4
updated: 2026-04-26
summary: >
  While Wellington City has strong broadband infrastructure, digital inclusion gaps persist across the wider region — particularly in rural Wairarapa, Kāpiti hinterland, and lower-income urban households. Device access and digital literacy barriers compound connectivity shortfalls for high-deprivation communities.
status: draft
generated_from: problem.wellington.infrastructure.digital_connectivity
---

# Digital inclusion gaps in Wellington region

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Urban-rural connectivity gap

While Wellington City's fibre coverage exceeds 90%, rural Wairarapa and Kāpiti hinterland areas remain on slower fixed-wireless or copper connections that do not meet the broadband performance benchmarks required for reliable remote work and digital services (claim.wellington.infrastructure.rural_broadband_coverage).


## Deprivation and digital inclusion

In high-deprivation areas of Porirua and Hutt Valley, affordability of broadband plans and device access are primary barriers to digital inclusion, compounding the economic disadvantage of already vulnerable households (claim.wellington.infrastructure.digital_inclusion_gap).


---


## Drivers

The following structural drivers contribute to this problem.


### Broadband affordability barrier



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

### Rural fibre deployment economics



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Digital Connectivity Subsidy for Low-Income Households

Affordability barriers to internet access must be addressed through targeted subsidies, not infrastructure expansion alone.

**Flagship moves:**

- Expand RBI2 subsidy to cover fixed-wireless for low-income households
- School-based device and data access programmes in Porirua and Hutt
- Community Wi-Fi in social housing complexes

**Tensions:**

- Demand-side subsidies do not resolve infrastructure gaps in rural fringes
- Data caps on subsidised connections still limit effective participation

**Interventions on the system:**

- Extend digital inclusion subsidy to 15,000 low-income Wellington households via MSD benefit integration (state variable: `broadband_uptake_low_income`, sign: +)


### Rural Fibre and Fixed-Wireless Infrastructure Extension

Supply-side investment to extend fibre and fixed-wireless to underserved rural Wellington communities is essential and requires Crown co-investment.

**Flagship moves:**

- Crown co-investment for Wairarapa rural fibre extension
- Mandatory wholesale access for rural fixed-wireless infrastructure
- Satellite backup connectivity for rural marae and schools

**Tensions:**

- Per-premise costs in rural areas may not be commercially viable even with subsidy
- Satellite latency limits utility for some applications

**Interventions on the system:**

- Negotiate rural fixed-wireless co-investment with Crown Infrastructure Partners targeting 2,000 under-served Wellington premises (state variable: `rural_broadband_coverage_pct`, sign: +)


---

## Claims cited on this page

- **Rural Wairarapa and Kāpiti hinterland areas within the Wellington region remain dependent on fixed-wireless or copper broadband connections that do not reliably meet the 50 Mbps download / 10 Mbps upload benchmark for modern digital service delivery.** *(confidence: medium)* — Wellington City Council Annual Plan 2024/25.
- **In high-deprivation areas of Porirua and Hutt Valley, the primary barriers to digital inclusion are affordability of broadband plans and device access, not infrastructure availability — indicating that infrastructure investment alone is insufficient to close the digital divide.** *(confidence: medium)* — Census 2023: Wellington Regional Profile.

---

## Further reading


- **Wellington City Council Annual Plan 2024/25** (Wellington City Council), 2024 — <https://www.wellington.govt.nz/your-council/plans-policies-and-bylaws/annual-plan>

- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* broadband_coverage_pct, digital_inclusion_rate.

*Constraints:* rural_deployment_cost, affordability_of_plans.

*Inputs:* fibre_rollout_investment, device_access_programme_funding.


*Feedback loops:*

- `Affordability trap: high plan costs relative to income exclude low-income households from connectivity benefits even where infrastructure exists.`


---

*Generated from `problem.wellington.infrastructure.digital_connectivity` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
