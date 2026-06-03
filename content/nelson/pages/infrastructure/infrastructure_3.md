---
title: "Port Nelson capacity and access upgrades"
section: infrastructure
subpage: infrastructure_3
order: 3
updated: 2026-04-26
summary: >
  Port Nelson is upgrading to meet container and bulk-export demand growth. Throughput is 130,000-160,000 tonnes of fish and seafood annually plus growing volumes of timber, fruit, and general cargo, with TEU growth around 6 percent per year 2019-2023. Stormwater and wastewater treatment at the port require $18-24 million in upgrades, and SH6 truck access is congested in peak season, with an estimated $45-65 million in widening investment required.
status: draft
generated_from: problem.nelson.infrastructure.infrastructure_3
---

# Port Nelson capacity and access upgrades

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Throughput growth versus environmental discharge standards

Port Nelson is under cumulative pressure to grow throughput while tightening discharge to Tasman Bay (claim.nelson.infrastructure.infrastructure_3_claim). Both are real; meeting both simultaneously requires capital investment that neither the port company nor the council can fully self-fund.


## The SH6 last-mile problem

Trucks access Port Nelson via SH6 and the Haven Road interchange. Peak-season queueing imposes both economic and amenity costs. Widening estimates are large and compete against other Waka Kotahi priorities; rail alternatives are not on the table because there is no rail to Nelson.


---


## Drivers

The following structural drivers contribute to this problem.


### Small population scale against high per-unit infrastructure cost



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Prioritise three-waters infrastructure renewal in Nelson urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Nelson (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Port Nelson infrastructure is being upgraded to meet container and bulk export demand growth. Current facilities handle 130,000–160,000 tonnes of fish/seafood annually and increasing volumes of timber, fruit, and general cargo; container equivalent units (TEU) have grown 6% annually 2019-2023. Wharf and berth capacity are adequate, but stormwater and wastewater treatment at the port require $18–24 million in upgrades to meet discharge standards and sea level rise mitigation. Truck access to the port from SH6 is congested during peak seasons; port–city logistics connectivity requires SH6 widening investment estimated at $45–65 million.** [value: 160000 tonnes/year throughput (fish, cargo combined); 2023] — Port Nelson Annual Report 2023.

---

## Further reading


- **Port Nelson Annual Report 2023** — Port Nelson Limited (Port Nelson Limited), 2023 — <https://www.portnelson.co.nz>


---

## Technical notes

*State variables:* annual_throughput_tonnes, teu_growth_rate_pct, sh6_peak_truck_queue_minutes.

*Constraints:* consent_discharge_limits, land_access_to_port.

*Inputs:* nzta_capex_allocation, port_company_capex.


*Feedback loops:*

- `Throughput-amenity feedback: rising throughput grows truck flow, eroding amenity around the port and city interface, which builds political resistance to further capacity expansion.`


---

*Generated from `problem.nelson.infrastructure.infrastructure_3` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
