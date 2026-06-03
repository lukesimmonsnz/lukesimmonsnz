---
title: "Rural broadband gap, especially in Mohua"
section: infrastructure
subpage: infrastructure_3
order: 3
updated: 2026-04-26
summary: >
  Around 76 percent of Golden Bay properties have access to fixed broadband at 30 Mbps or above, against a regional average of about 88 percent. Rural blocks beyond five kilometres of Motueka or Richmond rely on satellite or cellular. The Crown's Rural Broadband Initiative Phase 2 is expected to extend fibre to Takaka by 2026.
status: draft
generated_from: problem.tasman.infrastructure.infrastructure_3
---

# Rural broadband gap, especially in Mohua

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The connectivity gap is also a service gap

Telehealth, online tertiary study, remote work, and digital banking all assume a stable fixed connection. Where the only option is satellite or marginal cellular, those services are de facto unavailable (claim.tasman.infrastructure.infrastructure_3_claim).


## Coverage is not the same as capacity

Even where fibre will reach Takaka by 2026, the last-mile economics for properties outside the township and on outlying farms remain marginal. Rural Broadband Phase 2 improves the median, not the worst case, and the worst-case properties are precisely the ones already most isolated by road and health geography.


---


## Drivers

The following structural drivers contribute to this problem.


### Single-route exposure to weather and geology



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Prioritise three-waters infrastructure renewal in Tasman urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Tasman (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Digital connectivity in Golden Bay lags regional average; only 76% of properties have access to fixed broadband (>30 Mbps), vs regional average of 88%. Rural blocks and properties beyond 5km from Motueka/Richmond rely on satellite or cellular. Crown investment in Rural Broadband Initiative Phase 2 will extend fibre to Takaka by 2026.** [value: 76 percent broadband access (>30 Mbps); 2024] *(confidence: medium)* — Tasman District Council Annual Plan 2024; Tasman Housing Demand and Lifestyle Migration 2024.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>


---

## Technical notes

*State variables:* share_premises_30mbps_capable, median_rural_download_speed.

*Constraints:* low_population_density_economics, topographic_line_of_sight_limits.

*Inputs:* rbi2_capex_to_takaka, wireless_isp_capacity.


*Feedback loops:*

- `Lower rural connectivity reduces remote-work in-migration, which keeps population density low, which keeps last-mile economics marginal.`


---

*Generated from `problem.tasman.infrastructure.infrastructure_3` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
