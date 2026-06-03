---
title: "Productivity Gap and Economic Underperformance"
section: economy
subpage: productivity
order: 0
updated: 2026-04-26
summary: >
  New Zealand labour productivity is 30-35% below the OECD frontier; Auckland has not closed this gap over two decades. Business R&D investment (0.7% of GDP) is less than half the OECD average. Transport congestion costs Auckland approximately $1.3 billion per year in productivity losses. The debate centres on whether innovation investment incentives or urban density and agglomeration improvements are the higher-return lever.

status: draft
generated_from: problem.auckland.economy.productivity
---

# Productivity Gap and Economic Underperformance

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The persistent gap

New Zealand has been approximately 30% less productive per hour worked than the OECD frontier since at least the 1990s. The gap has not closed with GDP growth because growth in New Zealand has been driven more by labour and capital quantity than by efficiency improvement. Auckland, as New Zealand's most productive city, sets the ceiling; the gap between Auckland's actual productivity and what a well-connected city of its size should achieve is primarily an urban form and investment problem.


## Agglomeration as the underused lever

The research evidence on agglomeration economies is that doubling a city's effective density (connected, walkable, transit-accessible) increases productivity by 5-10% through face-to-face knowledge exchange and labour market pooling. Auckland has the population for a major city productivity premium but has built a suburban sprawl pattern that captures only part of it. The congestion cost is the most visible symptom; the opportunity cost of the foregone agglomeration premium is larger and less visible.


---

## References



- **NZIER Productivity and Economic Performance 2023**, 2023 — <https://www.nzier.org.nz/publications>

- **The Treasury Living Standards Framework Dashboard 2023**, 2023 — <https://www.treasury.govt.nz/information-and-services/nz-economy/living-standards>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Agglomeration Friction from Urban Form



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

#### Capital Shallowness and Low R&D Investment



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Innovation Investment and R&D Tax Incentives

Auckland's productivity gap is an investment gap; firms do not invest in R&D at the rates required to sustain productivity growth because the returns are partly captured by others (knowledge spillovers) and the domestic market is too small to justify the fixed cost. Government co-investment — R&D tax credits at international rates, a sovereign innovation fund, and university-industry research partnerships — corrects the market failure and builds the knowledge base that drives long-run productivity growth.

**Flagship moves:**

- Increase R&D tax credit rate to 15% and extend eligibility to software and service sector R&D.
- Establish an Auckland Innovation Fund of $200M over 5 years, co-invested with university and private capital.
- Fund three Auckland-based university-industry research institutes in health technology, agri-tech, and clean energy.

**Tensions:**

- R&D tax credits are captured by large firms with existing R&D capacity; startups and SMEs — the majority of Auckland businesses — may not benefit proportionately unless there is also direct grant support for early-stage innovation.

- Innovation investment has long lags before it appears in productivity statistics; political cycles favour interventions with shorter payoffs.


**Interventions on the system:**

- Increase R&D tax credit from 12.5% to 15% and extend the definition of eligible R&D to include software product development and service innovation.
 (state variable: `business_rd_as_gdp_share`, sign: +) (relaxes: `Partial-appropriability market failure in R&D`)
- Establish a $200M Auckland Innovation Fund administered by Callaghan Innovation, requiring 1:1 private co-investment and 5-year commercialisation milestones.
 (state variable: `labour_productivity_index`, sign: +)


#### Urban Density and Agglomeration Investment

Auckland's most efficient productivity investment is urban form: denser, better-connected housing and commercial clusters reduce the friction cost of agglomeration and allow Auckland to capture the city-scale productivity premium that comparable cities already enjoy. Light rail, rezoning for density, and mixed-use city centre investment are productivity infrastructure, not just liveability projects.

**Flagship moves:**

- Prioritise light rail and rapid transit investment as productivity infrastructure, not just transport.
- Allow high-density mixed-use development within 1km of all Auckland rapid transit stations.
- Fund Auckland CBD commercial and innovation precinct development to concentrate knowledge workers.

**Tensions:**

- Urban density investment has very long payback periods measured in productivity; the mechanism runs through agglomeration effects that require decades of urban restructuring to manifest.

- Concentrating knowledge sector investment in the CBD may intensify the spatial mismatch between where high-productivity jobs are and where Auckland's most disadvantaged communities live.


**Interventions on the system:**

- Rezone all land within 800m of current and proposed rapid transit stations to allow mixed-use development up to 8 storeys by right.
 (state variable: `agglomeration_productivity_index`, sign: +)
- Fund an Auckland innovation precinct in the CBD with subsidised co-working and lab space for tech and life science startups, adjacent to the City Rail Link.
 (state variable: `labour_productivity_index`, sign: +)


### Claims cited on this page

- **New Zealand's labour productivity is approximately 30-35% below the OECD frontier (measured by GDP per hour worked); Auckland, as the primary economic engine, has not closed this gap over two decades despite periods of strong GDP growth. The gap is largest in traded goods sectors and reflects low business R&D investment and slow technology adoption.
** — NZIER Productivity and Economic Performance 2023; The Treasury Living Standards Framework Dashboard 2023.
- **New Zealand business R&D investment as a share of GDP (approximately 0.7%) is less than half the OECD average (approximately 1.7%); Auckland-based firms account for the majority of New Zealand's R&D but are under-resourced relative to comparable city-regions in Australia, Canada, and Northern Europe.
** — NZIER Productivity and Economic Performance 2023.
- **Auckland's transport congestion costs the economy approximately $1.3 billion per year in lost productivity through delayed freight, missed appointments, and worker commute time; agglomeration productivity benefits of Auckland's city-scale are partially negated by the friction cost of a car-dependent, congested transport network.
** [value: 1300 NZD millions/year; 2022-2023] *(confidence: medium)* — The Treasury Living Standards Framework Dashboard 2023; NZIER Productivity and Economic Performance 2023.

### Systems-model notes

*State variables:* labour_productivity_index, business_rd_as_gdp_share, agglomeration_productivity_index, congestion_cost_annual.

*Constraints:* Distance: NZ's geographic isolation raises per-unit technology adoption cost, Market size: small domestic market makes R&D fixed costs harder to amortise, Urban lock-in: car-dependent urban form is expensive to reverse; density benefits take decades.

*Inputs:* rd_tax_credit_rate, innovation_fund_size, rapid_transit_network_km, mixed_use_zoning_coverage.


*Feedback loops:*

- `Low productivity → low wages → lower consumer spending → smaller domestic market → lower R&D returns`
- `Congestion → reduced agglomeration benefit → lower productivity premium of city scale`


</details>

---

*Generated from `problem.auckland.economy.productivity` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
