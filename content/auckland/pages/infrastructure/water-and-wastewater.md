---
title: "Water supply and wastewater network capacity"
section: infrastructure
subpage: water-and-wastewater
order: 1
updated: 2026-04-26
summary: >
  Auckland's water supply and wastewater networks face compounding capacity and condition challenges. The pipe network carries significant aging infrastructure from the 1950s–70s, generating rising failure rates and contributing to hundreds of overflow events annually that contaminate harbours and cause beach closures. Water supply resilience is exposed by drought: the 2020–21 drought triggered restrictions when reservoir storage fell below 40%. The Central Interceptor will partially address wastewater capacity when complete, but the distributed pipe renewal backlog and demand from continued population growth require sustained investment beyond any single major project.

status: draft
generated_from: problem.auckland.infrastructure.water_and_wastewater
---

# Water supply and wastewater network capacity

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The overflow problem

Auckland's combined sewer system — where stormwater and wastewater share the same pipes in older parts of the network — overflows during heavy rainfall when combined flows exceed pipe and treatment capacity. The result is direct discharge to waterways and harbours. The Waitemata and Manukau Harbours receive recurring contamination events that close beaches and degrade ecosystems. The Central Interceptor tunnel, when complete, will capture the largest single source of overflow; but the network of smaller pipes that feed it also requires upgrade, and without that downstream investment the trunk project cannot deliver its full benefit.


## Water supply vulnerability

Auckland's water supply depends primarily on the Waitākere and Hunua catchments, which are vulnerable to sustained drought and to contamination events. The 2020–21 drought was the most serious stress test since the 1990s, exposing the absence of adequate secondary supply options. Watercare's planned additional storage and supply diversification will improve resilience, but the capital programme competes with the wastewater renewal requirement for a constrained funding envelope.


---

## References



- **Watercare — Annual Report 2022/23** (Watercare Services Limited), 2023 — <https://www.watercare.co.nz/about-us/reports>

- **Infrastructure New Zealand — State of Infrastructure Report 2023** (Infrastructure New Zealand), 2023 — <https://www.infrastructure.org.nz/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Aging three-waters pipe network



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

#### Population growth outpacing water and wastewater capacity



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Demand management and water efficiency

Expanding supply capacity is only half the equation: reducing per-capita water demand through pricing signals, appliance standards, and leak reduction reduces the investment required in treatment and distribution infrastructure. A 20% reduction in per-capita demand is equivalent to a 20% increase in system capacity at zero capital cost.

**Flagship moves:**

- Introduce progressive volumetric water pricing to provide a price signal for conservation above a lifeline amount
- Mandate water-efficient appliance standards for all new residential and commercial developments
- Fund a large-scale network leak detection and repair programme targeting a 15% reduction in water losses

**Tensions:**

- Demand management reduces the revenue base for a volume-tariff water utility at the same time as it reduces capital expenditure requirements — the net financial effect depends on tariff design and requires careful modelling.

- Appliance standards and retrofits address new stock quickly but the existing housing stock turns over slowly; the demand reduction from efficiency standards takes 20–30 years to fully materialise.


**Interventions on the system:**

- Progressive water tariff (free lifeline block, rising tiers above) targeting 10% reduction in per-capita water demand over 5 years.
 (state variable: `water_demand_per_capita`, sign: -) (relaxes: `flat-rate pricing without conservation signal`)
- Network leakage detection programme targeting 15% reduction in non-revenue water within 5 years, freeing equivalent treatment and distribution capacity.
 (state variable: `infrastructure_investment_rate`, sign: -)


#### Trunk infrastructure investment and network renewal

Auckland's water and wastewater problems are engineering problems that require engineering solutions: completing the Central Interceptor, accelerating pipe renewal across the network, and expanding treatment capacity ahead of growth. The investment case is straightforward — the economic and environmental cost of deferred renewal and overflow events exceeds the cost of timely investment.

**Flagship moves:**

- Complete the Central Interceptor wastewater tunnel by 2026 and fund the downstream network upgrades required to realise its full overflow-reduction benefit
- Accelerate the three-waters pipe renewal programme to at least 1.5% of network per year, reducing the renewal backlog to zero over 30 years
- Invest in additional water storage to provide 120-day supply at current demand under drought conditions

**Tensions:**

- Trunk investment addresses capacity at specific points in the network but does not resolve the distributed renewal backlog across thousands of kilometres of smaller pipes; the visible large projects crowd out the unglamorous but critical local renewal programme.

- Watercare's capital programme already exceeds what can be funded without significant rate increases or additional Crown support; accelerating investment requires a funding solution, not just a capital programme.


**Interventions on the system:**

- Fund Central Interceptor downstream network upgrades (estimated $400M) to capture the full overflow reduction available from the trunk tunnel investment already committed.
 (state variable: `wastewater_overflow_events`, sign: -) (relaxes: `downstream network bottleneck limiting trunk investment benefit`)
- Increase the annual pipe renewal budget to achieve 1.5% network renewal per year, funded by a 5% annual Watercare tariff increase over 10 years.
 (state variable: `asset_condition_index`, sign: +)


### Claims cited on this page

- **Auckland's combined wastewater and stormwater network experiences hundreds of overflow events annually during heavy rainfall, discharging partially treated or untreated wastewater to waterways and harbours. The Waitemata Harbour and Manukau Harbour both receive chronic stormwater and wastewater contamination that causes persistent beach closures and ecological damage. Overflow events are a direct consequence of undersized network capacity relative to current rainfall intensity and impervious surface coverage.
** — Watercare — Annual Report 2022/23.
- **Auckland's water supply relies primarily on the Waitākere and Hunua reservoir systems, which are vulnerable to drought, contamination events, and climate-driven changes in catchment hydrology. The 2020–21 drought required restrictions when storage fell to 40% of capacity, exposing the absence of sufficient secondary or emergency supply. The planned Central Interceptor project and additional storage will improve resilience but will not be complete until the late 2020s.
** — Watercare — Annual Report 2022/23.
- **A significant share of Auckland's three-waters infrastructure — water mains, wastewater pipes, and stormwater drains — has exceeded or is approaching its design life. Deferred renewal accumulates exponentially: pipe failures increase sharply as assets age past their replacement threshold, and emergency repair costs typically exceed planned renewal costs by a factor of 3–5.
** — Watercare — Annual Report 2022/23; Infrastructure New Zealand — State of Infrastructure Report 2023.

### Systems-model notes

*State variables:* wastewater_overflow_events, water_demand_per_capita, asset_condition_index, reservoir_storage_days.

*Constraints:* Aging pipe network: large share of pipes approaching or past design life, Combined sewer system in older areas: stormwater inflows trigger wastewater overflows, Funding constraint: renewal backlog exceeds affordable annual investment rate.

*Inputs:* population_growth_rate, rainfall_intensity_and_frequency, pipe_renewal_rate, drought_frequency.


*Feedback loops:*

- `Deferred pipe renewal → increased failure rate → emergency repairs → reduced renewal budget → more deferral`
- `Population growth → increased demand and flows → capacity exceedance → overflow events → harbour contamination`


</details>

---

*Generated from `problem.auckland.infrastructure.water_and_wastewater` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
