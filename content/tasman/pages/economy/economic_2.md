---
title: "Pip-fruit and kiwifruit export concentration"
section: economy
subpage: economic_2
order: 2
updated: 2026-04-26
summary: >
  Pip-fruit and kiwifruit orchards cover roughly 8,400 hectares in Tasman, generating around NZD 187 million of exports in 2023. Roughly 85 percent of the crop ships to overseas markets, particularly China, Japan and the European Union.
status: draft
generated_from: problem.tasman.economy.economic_2
---

# Pip-fruit and kiwifruit export concentration

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## An export-shaped industry

Tasman's apple and kiwifruit growers do not produce primarily for the New Zealand market — most of the crop is destined for overseas wholesale and retail. That makes regional incomes sensitive to exchange rates, foreign-market access, and global shipping costs (claim.tasman.economy.economic_2_claim).


## Biosecurity and climate as concentrated risks

A single biosecurity incursion (e.g. fire blight, brown marmorated stink bug) or a single bad-weather season can cost a meaningful share of regional GDP because the industry footprint is so concentrated geographically and in supplier base. The same concentration that produces scale economies also concentrates downside risk.


---


## Drivers

The following structural drivers contribute to this problem.


### Primary-sector concentration in horticulture and viticulture



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

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

- **Horticulture (apples, kiwifruit, cherries) comprises 22% of Tasman's GDP; apple and kiwifruit orchards occupy 8,400 hectares. Export value reached NZD 187 million (2023), with 85% of fruit destined for overseas markets (China, Japan, EU).** [value: 187 NZD million export value; 2023] — Tasman District Council Annual Plan 2024; Stats NZ Census 2023.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* horticulture_export_value, hectares_under_pipfruit_kiwifruit.

*Constraints:* weather_volatility, export_market_access_settings.

*Inputs:* biosecurity_response_capacity, shipping_capacity_to_export_markets.


*Feedback loops:*

- `Export-revenue shocks cause investment cycles in orchard development that lag the original shock, causing further volatility in production a decade later.`


---

*Generated from `problem.tasman.economy.economic_2` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
