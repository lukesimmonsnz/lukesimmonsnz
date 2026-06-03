---
title: "Abel Tasman / Mohua tourism dependence"
section: economy
subpage: economic_4
order: 4
updated: 2026-04-26
summary: >
  Abel Tasman National Park draws roughly 230,000 visitors per year, generating around NZD 62 million in regional tourism revenue and supporting more than 180 FTE across DOC and private operators. Activity is heavily seasonal, concentrated in February-April and the December summer peak.
status: draft
generated_from: problem.tasman.economy.economic_4
---

# Abel Tasman / Mohua tourism dependence

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## A small number of seasons carry the year

Water-taxi operators, lodges, and guided-walk operators earn much of their annual revenue between mid-December and late April. Outside that window, fixed costs (staff, vessels, lodges) carry through low cash-flow months (claim.tasman.economy.economic_4_claim).


## Concentration risk in weather, biosecurity and access

A bad summer storm, a marine biosecurity incursion, or a Cook Strait ferry disruption translates almost directly into the regional tourism balance. With Mohua tourism reliant on SH60 over the Takaka Hill, transport disruption sits adjacent to weather and biosecurity in the regional risk register.


---


## Drivers

The following structural drivers contribute to this problem.


### Seasonal labour dependence



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing economy challenges.

**Flagship moves:**

- Implement evidence-based economy policy in Tasman
- Increase investment in economy services and infrastructure
- Build cross-sector partnerships to address economy challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for economy (state variable: `economy_outcome_index`, sign: +)
- Secondary intervention for economy (state variable: `economy_service_access`, sign: +)


---

## Claims cited on this page

- **Abel Tasman National Park attracts 230,000+ visitors annually, generating estimated NZD 62 million in regional tourism revenue (2023). DOC and private operators employ 180+ FTE; seasonal lodges and water taxi services rely on February-April and December summer peaks.** [value: 230000 annual visitors; 2023] — Tasman Tourism Impact and DOC Management 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Tasman Tourism Impact and DOC Management 2023** — Department of Conservation / Abel Tasman Project (Department of Conservation), 2023 — <https://www.doc.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* abel_tasman_annual_visitors, tourism_revenue_njd.

*Constraints:* seasonality, single_road_corridor_to_mohua.

*Inputs:* doc_visitor_management, marketing_off_season_demand.


*Feedback loops:*

- `Operators size capacity to peak season, which leaves them exposed in shoulder months and amplifies the cash-flow effect of any peak-season disruption.`


---

*Generated from `problem.tasman.economy.economic_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
