---
title: "Active mode infrastructure and cycling adoption"
section: transport
subpage: active-modes
order: 3
updated: 2026-04-26
summary: >
  Cycling accounts for roughly 1–2% of Auckland person-trips — among the lowest shares of any comparable OECD city with a mild climate. The primary barrier is not distance, weather, or topography: it is the absence of a safe, connected network. Auckland has high-quality cycling infrastructure in isolated segments separated by gaps on arterial roads where cyclists must share lanes with vehicles travelling at 50–80km/h. Where protected infrastructure has been built, usage has exceeded projections. The "interested but concerned" majority — approximately 60–70% of non-cyclists who would cycle if roads felt safe — represents the accessible latent demand that connected infrastructure would release.

status: draft
generated_from: problem.auckland.transport.active_modes
---

# Active mode infrastructure and cycling adoption

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The connectivity problem

A cycling network where 80% of routes are excellent but 20% require riding in 50km/h traffic is functionally unusable for most potential cyclists. Network connectivity is a multiplicative property: each gap degrades the utility of every connected segment by making it impossible to complete a trip without an on-road section. Auckland's cycling infrastructure — the Northwestern cycleway, the Lightpath, Beach Road, the Waitemata Harbour shared path — is high-quality within each segment but not connected into a system. The result is infrastructure used by confident cyclists who would cycle anyway, not by the "interested but concerned" majority who would cycle if they felt safe.


## Where infrastructure has been built, people have cycled

Auckland's own evidence refutes the claim that the city is too hilly, too spread out, or too car-oriented to support cycling. Every protected cycleway built in Auckland has exceeded AT's patronage projections: the Lightpath, the Northwestern cycleway extensions, and Beach Road all attracted more cyclists than modelled. The latent demand exists. The constraint is safety perception, not desire, and safety perception is determined by physical infrastructure design — specifically, whether a cyclist is physically separated from motor traffic or merely painted-lane adjacent to it.


## Children and the school trip

In 1990 approximately 50% of Auckland children walked or cycled to school; by the 2020s this proportion had fallen to roughly 20–25%. The school trip is both a major source of peak-hour congestion and the entry point for lifelong active travel habit. School streets programmes — closing streets immediately outside schools to private vehicles during drop-off and pick-up — have demonstrated dramatic increases in walking and cycling rates in cities from London to Melbourne. They are also among the cheapest and fastest-deployable interventions available, requiring temporary signs rather than capital construction.


---

## References



- **Ministry of Transport — Household Travel Survey 2023** (Ministry of Transport (New Zealand)), 2023 — <https://www.transport.govt.nz/statistics-and-insights/household-travel-survey/>

- **Auckland Transport — Annual Report 2022/23** (Auckland Transport (AT)), 2023 — <https://at.govt.nz/about-us/reports-publications/annual-report/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Fragmented and incomplete cycling network



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

#### Road danger and safety perception



- **Category:** physical
- **Timescale:** medium
- **Consensus:** mostly-agreed


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Connected protected cycling network

Cycling mode share cannot reach meaningful levels without a connected network of physically separated cycleways on every arterial route that carries significant trip demand. Painted lanes are insufficient — physical separation from motor traffic is the infrastructure design that changes both actual safety and the perception of safety among the 60–70% of potential cyclists who identify as interested but concerned. Connection is as important as quality: one missing link breaks the utility of every connected segment.

**Flagship moves:**

- Build a connected citywide cycling network by closing all gaps between existing high-quality segments within 800m of schools, town centres, and rapid transit stations
- Convert the highest-volume arterial corridors (Great North Road, Dominion Road, New North Road, Great South Road) to protected cycleway standard within 10 years
- Establish a cycling network completeness standard requiring no on-road gap greater than 200m between protected segments

**Tensions:**

- Protected cycleways on arterials typically require removal of a general traffic lane or parking, creating organised opposition from motorists and local businesses that consistently slows or stops implementation — even where the safety and patronage evidence is compelling.

- Arterial network investment concentrates benefit on the commuter cycling market (confident riders, longer trips) rather than the local access market (children cycling to school, short trips); the two user groups require somewhat different infrastructure priorities.


**Interventions on the system:**

- Close all gaps of >200m in the existing protected cycling network within 5 years, prioritising connections to schools, rapid transit stations, and employment centres.
 (state variable: `cycling_mode_share`, sign: +) (relaxes: `network connectivity gaps forcing on-road cycling`)
- Mandate protected cycling infrastructure on all arterial roads scheduled for reseal or reconstruction, embedding cycling provision in the road renewal programme at near-zero marginal cost.
 (state variable: `cycling_network_km`, sign: +)


#### School streets and local traffic management

The most effective intervention for mass cycling adoption is not arterial infrastructure but local area management: closing streets adjacent to schools during drop-off and pick-up, creating low-traffic neighbourhoods with filtered permeability, and redesigning residential street environments so children can cycle and walk to school safely. Schools are the entry point for lifelong cycling habit; local area schemes deliver safety improvements at lower cost per kilometre than arterial protected lanes.

**Flagship moves:**

- Implement school streets closures (no private vehicle access during drop-off and pick-up) at all Auckland primary schools within 10 years
- Create low-traffic neighbourhood schemes using modal filters in residential areas adjacent to schools and local parks, reducing through-traffic without impeding access
- Establish a safe routes to school programme funding high-quality walking and cycling connections for every school within a 2km radius of a PT or cycling connector

**Tensions:**

- School streets and local area schemes displace vehicle traffic to surrounding arterials, increasing congestion on those routes unless arterial-level alternatives exist simultaneously — the two approaches are complementary but the local scheme alone exports its problem to the arterial network.

- Local area schemes are slow to implement due to community consultation requirements and generate strong opposition from a minority of affected residents, making citywide rollout politically difficult despite aggregate public support for cycling safety.


**Interventions on the system:**

- School streets trial at 50 Auckland primary schools in Year 1, closing the street immediately outside the school gate to private vehicles during the 30-minute drop-off and pick-up window.
 (state variable: `cycling_mode_share`, sign: +) (relaxes: `road danger at school gates preventing child cycling`)
- Modal filter installation on residential streets within 400m of schools that are used as rat-runs, reducing through-traffic speeds and volumes to levels consistent with safe cycling.
 (state variable: `active_mode_safety_perception`, sign: +)


### Claims cited on this page

- **Cycling accounts for approximately 1–2% of Auckland person-trips — among the lowest cycling mode shares of any comparable OECD city with a mild climate. In Dutch cities of comparable topography, cycling accounts for 25–35% of trips. The gap is not primarily climatic or topographic: it reflects the absence of a safe, connected cycling network. Where protected cycleways have been built — the Lightpath, the Northwestern cycleway, the Beach Road corridor — usage has grown faster than AT projections, demonstrating latent demand.
** [value: 2 percent of person-trips by bicycle; 2021-2023] — Ministry of Transport — Household Travel Survey 2023.
- **Auckland's cycling network consists of a series of disconnected high-quality segments — the Northwestern cycleway, the Lightpath, Beach Road, the Waitemata Harbour shared path — separated by gaps on high-speed arterials where cyclists must ride in traffic with vehicles travelling at 50–80km/h. The absence of a connected network means most cycling trips require on-road segments that the majority of potential cyclists identify as too dangerous to attempt, confining cycling to a small self-selecting group of confident riders.
** — Auckland Transport — Annual Report 2022/23.

### Systems-model notes

*State variables:* cycling_mode_share, cycling_network_km, active_mode_safety_perception, child_active_travel_rate.

*Constraints:* Network connectivity: gaps between protected segments force on-road cycling on dangerous arterials, Road design standard: arterial lanes at 50–80km/h without physical separation, Investment level: cycling capital spend per capita well below cities achieving 10%+ mode share, Political friction: parking and lane removal required for protected infrastructure generates organised opposition.

*Inputs:* protected_cycleway_connectivity, arterial_speed_and_volume, school_streets_coverage, cycling_investment_per_capita.


*Feedback loops:*

- `Low cycling_mode_share → few cyclists visible → cycling perceived as dangerous → lower cycling_mode_share (invisibility trap)`
- `Connected protected network → more cyclists → normalisation → more cyclists (safety in numbers)`
- `School streets → children cycle → parents observe safety → adult cycling increases in same neighbourhoods`


</details>

---

*Generated from `problem.auckland.transport.active_modes` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
