---
title: "Public transport mode share and network gaps"
section: transport
subpage: public-transport
order: 2
updated: 2026-04-26
summary: >
  Auckland's public transport carries roughly 5–8% of person-trips — a fraction of what comparable cities achieve. Patronage recovered to roughly 80–85% of its 2019 peak by 2023 but remains constrained by a rapid transit network that leaves more than half the urban area beyond 800m of any rapid transit stop, bus services with 15–30 minute headways that require timetable planning rather than turn-up-and-go, and fares structured to penalise longer trips made by outer-suburban households. The City Rail Link — delayed and not yet open — will when complete transform rail capacity but cannot by itself close the coverage gap in the Northwest, North Shore, and outer South.

status: draft
generated_from: problem.auckland.transport.public_transport
---

# Public transport mode share and network gaps

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The network coverage problem

Auckland's rapid transit spine — the rail lines, Northern Busway, and Eastern Busway — serves major corridors well but leaves the Northwest, most of the North Shore, and the outer South without fast, frequent connections. More than half of Auckland's residential land area lies beyond 800m of any rapid transit stop: these residents face bus services too slow and infrequent to attract discretionary car trips. The City Rail Link — delayed past its initial 2025 target and not yet open — will transform rail capacity when complete, enabling 24 trains per hour through the CBD tunnel, but it does not extend the geographic reach of the network — it makes the existing spine faster and more reliable.


## Frequency and reliability as the patronage constraint

Bus service frequency — how long passengers must wait if they miss a bus — is the single strongest predictor of PT mode share for discretionary trips. Services at 15-minute headways are usable; services at 30 minutes require timetable planning and penalise any uncertainty in departure. Most Auckland bus services outside the rapid transit spine operate at 15–30 minute headways during peaks, with much longer waits off-peak and on weekends. Combined with shared running in congested traffic — which makes journey times slow and unpredictable — this produces a service that is a last resort rather than a genuine alternative for households with a working car.


## The funding gap

AT's operating budget faces a structural gap between what the fare box and local rates can fund and what frequent, reliable services across the network cost. Farebox recovery is approximately 30–40% of operating costs — meaning the majority of PT is already subsidised — but the subsidy level is insufficient to fund the frequency improvements that would generate the patronage growth to close the gap. The funding architecture, split between AT, Auckland Council, and central government's National Land Transport Fund, creates accountability diffusion that has historically prevented the sustained investment required to break the low-frequency/low-patronage equilibrium.


---

## References



- **Auckland Transport — Public Transport Patronage Statistics 2023** (Auckland Transport (AT)), 2023 — <https://at.govt.nz/about-us/reports-publications/at-metro-patronage-report/>

- **Auckland Transport — Annual Report 2022/23** (Auckland Transport (AT)), 2023 — <https://at.govt.nz/about-us/reports-publications/annual-report/>

- **Auckland Future Development Strategy 2022** (Auckland Council), 2022 — <https://www.aucklandcouncil.govt.nz/plans-projects-policies-reports-bylaws/our-plans-strategies/future-development-strategy/Pages/default.aspx>

- **Ministry of Transport — Household Travel Survey 2023** (Ministry of Transport (New Zealand)), 2023 — <https://www.transport.govt.nz/statistics-and-insights/household-travel-survey/>

- **Ministry of Social Development — Household Incomes Report 2023** (Ministry of Social Development (New Zealand)), 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/monitoring/household-incomes/>

- **Auckland Council Long-Term Plan 2024-2034** — Auckland Council (Auckland Council), 2024 — <https://www.aucklandcouncil.govt.nz/plans-projects-policies-reports-bylaws/our-plans-strategies/long-term-plan/Pages/default.aspx>

- **City Rail Link Project - Programme Information** — City Rail Link Limited (City Rail Link Limited (Crown entity)), 2024 — <https://www.cityraillink.co.nz/about-the-project>

- **Auckland Transport Alignment Project Indicative Strategic Transport Programme (ATAP)** — Auckland Council; New Zealand Government (joint partnership) (Ministry of Transport (Te Manatu Waka)), 2024 — <https://www.transport.govt.nz/area-of-interest/strategy-and-direction/auckland-transport-alignment-project/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Incomplete rapid transit network coverage



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

#### PT service frequency and reliability gaps



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Fare reform and free or low-cost PT

Fare revenue covers only 30–40% of Auckland PT operating costs; the remainder is already subsidised. Reducing or eliminating fares — particularly for under-18s, Community Services Card holders, and off-peak travel — would increase ridership, reduce car trips, and improve equity for low-income households who depend on PT but face regressive fare structures. The marginal cost of an additional PT passenger is close to zero on existing services.

**Flagship moves:**

- Extend the free-fares-for-under-25s programme to all Auckland PT services, funded by central government as a demand-building measure ahead of CRL opening
- Introduce income-tested deeply discounted or free AT HOP passes for Community Services Card holders
- Pilot off-peak free travel across the rail network to shift demand away from peak hours and improve average seat utilisation

**Tensions:**

- Fare reduction increases operating subsidy requirements at a time of fiscal constraint; the AT funding gap is already significant and free fares would widen it without a new funding mechanism.

- Free PT primarily increases discretionary and recreational trips rather than shifting committed car commuters; the mode shift effect per dollar of foregone revenue may be modest compared with frequency improvements or infrastructure investment.


**Interventions on the system:**

- Free AT HOP travel for all Community Services Card holders, funded by a $50M/year central government top-up to AT's operating budget, targeting a 15% ridership increase among low-income households.
 (state variable: `pt_mode_share`, sign: +) (relaxes: `fare barrier for low-income PT-dependent households`)
- Distance-tapered fare structure replacing the current zone system, making longer trips (outer suburbs) proportionally cheaper relative to shorter inner-city trips, reducing fare regressivity.
 (state variable: `pt_fare_affordability`, sign: +)


#### Rapid transit network expansion

Auckland's PT mode share cannot reach European or East Asian levels without a rapid transit network that covers the whole urban area. The City Rail Link doubles rail capacity, but the Northwest, North Shore beyond Albany, and outer South remain unserved. Building out the rapid transit network — Northwest Rapid Transit, the Harbour Crossing mass transit option, and the Eastern Busway — creates the spine around which frequency improvements and TOD can deliver lasting mode shift.

**Flagship moves:**

- Fund and accelerate the Northwest Rapid Transit corridor (City–Westgate–Kumeu) as the highest-priority unbuilt rapid transit extension
- Progress the Auckland Harbour Crossing with a mass transit option (light rail or additional rail tunnel) to replace the Northern Busway which will reach capacity
- Complete the Eastern Busway to Botany and extend to Manukau, closing the gap in the southeastern rapid transit network

**Tensions:**

- Rapid transit capital costs are very high — each major corridor costs $2–5 billion or more — and Crown/Council fiscal constraints mean sequencing decisions necessarily leave parts of the network unserved for decades. Building the network takes longer than political cycles.

- Without land use intensification along new corridors, rapid transit investment may not generate the patronage required to justify capital cost, producing underutilised infrastructure in low-density corridors.


**Interventions on the system:**

- Fund Northwest Rapid Transit (light rail or dedicated busway, Auckland–Westgate–Kumeu) in the 2024–2034 National Land Transport Programme, targeting opening by 2034.
 (state variable: `pt_mode_share`, sign: +) (relaxes: `absence of rapid transit west of the CBD`)
- Implement frequency improvements on all existing rapid transit services to ≤10 minute headways during all waking hours (6am–10pm) as a precondition for the CRL opening, maximising the network effect.
 (state variable: `mode_share_car`, sign: -)


### Claims cited on this page

- **Auckland public transport patronage reached approximately 100 million annual boardings in 2019 before collapsing during COVID-19 lockdowns. By 2023 patronage had recovered to roughly 80–85% of pre-COVID levels, representing approximately 85–90 million annual boardings. Rail and Northern Busway services have recovered fastest; inner-city bus services more slowly. The City Rail Link — delayed past its initial 2025 target and not yet open — is expected when complete to at least double rail capacity through the CBD tunnel and materially increase rail's share of total PT trips.
** — Auckland Transport — Public Transport Patronage Statistics 2023.
- **Auckland's rapid transit network — rail, the Northern Busway, and the Eastern Busway under construction — serves the CBD, Eastern, Southern, and Western rail corridors, and the North Shore via the Northern Busway. It does not yet reach the Northwest (Westgate/Kumeu corridor), the majority of the North Shore beyond Albany, or the rapidly-growing outer South. More than half of Auckland's residential land area lies more than 800m from any rapid transit stop.
** — Auckland Transport — Annual Report 2022/23; Auckland Future Development Strategy 2022.
- **Auckland public transport fares impose a structurally regressive burden on outer-suburban, lower-income households. An AT HOP return trip from Papakura or Manukau to the CBD costs approximately $10-14 per day (2023 fares); for a minimum-wage worker earning approximately $22.70/hr gross, that represents roughly 7-9% of gross daily earnings consumed by commuting alone before food, housing, or childcare. The Ministry of Transport Household Travel Survey consistently shows lower-income households in outer Auckland are more PT-dependent yet face the highest absolute fares. Following the lapse of the half-price public transport subsidy in 2023, outer-zone AT HOP fares reverted to pre-subsidy levels, disproportionately affecting the Papakura, Manukau, Henderson-Massey, and Pukekohe corridors where car ownership rates are lowest relative to population.
** *(confidence: medium)* — Auckland Transport — Public Transport Patronage Statistics 2023; Ministry of Transport — Household Travel Survey 2023; Ministry of Social Development — Household Incomes Report 2023.
- **The National-led government cancelled Auckland's light rail programme in late 2023, terminating both the Dominion Road/City-to-Mangere corridor and the City-to-Airport route. The project had received over $300 million in planning, design, and preliminary works expenditure under the Labour government before cancellation. The decision reversed a decade-long process that included two separate business cases and a competitive procurement process reaching preferred-bidder stage. Auckland Transport and Waka Kotahi estimate the cancellation leaves the Northwest and southern isthmus corridors without a rapid transit upgrade pathway for at least a generation, given the capital and political cycle required to restart any equivalent project.
** — Auckland Council Long-Term Plan 2024-2034; Auckland Transport — Annual Report 2022/23.
- **The City Rail Link, a 3.45 km twin-tunnel underground rail link between Britomart and Mt Eden stations, is designed to enable Auckland's rail system to carry approximately 54,000 passengers per peak hour at full build-out, by adding two new underground stations (Te Wai Horotiu / Aotea, Karanga-a-Hape) and converting Britomart from a terminus to a through-station. Project budget is NZD 5.493 billion, cost-shared 50/50 between the Crown and Auckland Council.
** [value: 54000 peak hour passenger capacity (full build-out); 2026] — City Rail Link Project - Programme Information.
- **The Auckland Transport Alignment Project (ATAP) is the Crown-Auckland Council joint planning vehicle that publishes a 10-year indicative strategic transport programme for Auckland; the programme sequences Crown and Council co-funded investment across road, rail, public transport, walking, and cycling. ATAP is the alignment instrument that reconciles Auckland Council's Long Term Plan with the National Land Transport Programme.
** — Auckland Transport Alignment Project Indicative Strategic Transport Programme (ATAP).

### Systems-model notes

*State variables:* pt_mode_share, annual_pt_boardings, rapid_transit_catchment_coverage, pt_fare_affordability.

*Constraints:* Network coverage: more than half of Auckland beyond 800m of rapid transit, Frequency gap: most bus services at 15–30 minute headways, requiring timetable planning, Fare regressivity: longer outer-suburban trips cost more in absolute terms, Operating funding gap: AT subsidy requirement exceeds available Crown and Council funding.

*Inputs:* rapid_transit_network_extent, service_frequency_headways, fare_level_and_structure, bus_priority_infrastructure, crl_opening_and_capacity.


*Feedback loops:*

- `Low pt_mode_share → low farebox revenue → funding pressure → service cuts → lower pt_mode_share (PT death spiral)`
- `High frequency + network coverage → trip chaining possible → mode shift → higher farebox → investment case for further expansion`


</details>

---

*Generated from `problem.auckland.transport.public_transport` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
