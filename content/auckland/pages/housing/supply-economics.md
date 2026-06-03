---
title: "Supply economics — construction costs and delivery capacity"
section: housing
subpage: supply-economics
order: 5
updated: 2026-04-26
summary: >
  Even where land is available and zoning permits, dwellings are expensive to build and slow to deliver in Auckland. Construction-sector labour productivity has been flat for decades, post-COVID cost inflation eroded developer margins, and the pre-sales finance model means supply contracts precisely when affordability pressure is highest. A fragmented builder ecosystem of mostly small firms amplifies cyclical workforce losses and prevents the scale economies that could change the cost structure. Infrastructure capacity acts as an additional gate: trunk water, wastewater, and transport networks constrain where and how fast consented land can be built out.

status: draft
generated_from: problem.auckland.housing.supply_economics
---

# Supply economics

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The productivity floor

Dwelling construction in New Zealand has not meaningfully improved in labour productivity since the 1990s — an outcome the NZ Productivity Commission identified in 2012 and that remains largely unremedied. Post-COVID, construction costs rose approximately 30–40% on the Capital Goods Price Index, compressing developer margins and rendering marginal projects unviable even at elevated market prices. Rising nominal costs are a real resource problem, not a speculative artefact: they reflect the cost of labour, materials, and consenting delay that site-based craft construction cannot reduce without structural change to the production model.


## Cyclicality and hysteresis

Auckland's consent volumes swung from roughly 10,000 to 20,000 per year across the 2015–2024 decade, tracking credit conditions and buyer confidence more closely than underlying demand. Each contractionary phase destroys firms and workforce skills that are slow to rebuild — hysteresis means that supply capacity in each recovery starts below the previous peak. The pre-sales finance model amplifies this: because 50–70% of units must be pre-sold before banks will fund construction, supply is structurally unable to maintain output through a confidence trough, regardless of whether underlying affordability metrics indicate that new supply is needed.


## Infrastructure as a binding gate

Even consented, zoned, and financially viable projects cannot proceed where trunk infrastructure — water, wastewater, stormwater, transport — lacks headroom. Auckland Council's infrastructure funding gap, driven by the mismatch between growth-related capital requirements and the revenue tools available to a local authority, means that infrastructure investment has lagged the pace required to unlock the supply potential of the NPS-UD upzoning. Trunk capacity is a necessary condition for the consent-and-build pipeline to function.


---

## References



- **Building Consents Issued: December 2023** (Stats NZ | Tatauranga Aotearoa), 2023 — <https://www.stats.govt.nz/information-releases/building-consents-issued-december-2023>

- **New Zealand Productivity Commission — Housing Affordability Inquiry (2012)** (New Zealand Productivity Commission), 2012 — <https://www.productivity.govt.nz/inquiries/housing-affordability/>

- **Housing in Aotearoa: 2023** (Ministry of Housing and Urban Development | Manatū Wāhanga Okioki), 2023 — <https://www.hud.govt.nz/our-work/research-and-evaluation/housing-in-aotearoa-2023/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Cyclicality of the construction sector



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

#### Fragmented builder ecosystem



- **Category:** economic
- **Timescale:** long
- **Consensus:** mostly-agreed

#### Pro-cyclical construction finance



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

#### Weak construction-sector productivity growth



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Industrial transformation of construction

The real long-run supply constraint is weak construction-sector productivity. Shifting from site-based craft construction to factory-based prefabrication, standardised components, and a stable workforce pipeline is the only structural pathway to materially reduce the cost of producing a dwelling in Auckland.

**Flagship moves:**

- Establish a publicly-anchored off-site manufacturing hub to demonstrate and de-risk prefabricated volumetric construction at scale
- Mandate standardised component specifications across Crown and Kāinga Ora procurement to create a stable demand base for prefab manufacturers
- Reform Building Code and consent pathways to create a fast-track for certified prefabricated structural systems

**Tensions:**

- The upfront capital cost of transitioning to factory-based production is substantial; without a guaranteed demand pipeline from public or institutional buyers, private investment in prefab capacity is difficult to justify given the cyclicality of the construction market.

- Workforce and skills reform is a decade-long project; near-term supply shortfalls require conventional construction to continue at scale in parallel, limiting the immediate impact of transformation investment.


**Interventions on the system:**

- Crown co-investment in volumetric prefab facilities producing standardised medium-density typologies (2–4 storey), targeting a 20% reduction in per-m² construction cost within a decade.
 (state variable: `construction_cost_index`, sign: -) (relaxes: `craft-based production cost floor`)
- Guaranteed volume procurement contract (Crown and Kāinga Ora) of ≥1,000 prefab units/year to underwrite factory utilisation.
 (state variable: `annual_completions`, sign: +)


#### Infrastructure-first / trunk capacity investment

Zoning without infrastructure is theatre. Supply is gated by the capacity of water, wastewater, stormwater, and transport networks. Building trunk capacity ahead of private demand — rather than in response to it — is a precondition for any other supply lever to work at the volumes required to change Auckland's affordability trajectory.

**Flagship moves:**

- Sustained Crown and Council co-investment in trunk infrastructure ahead of demand, funded by long-term infrastructure bonds
- Reform Watercare and Auckland Transport funding models to enable forward-looking investment without requiring development contributions at the point of consent
- Establish a land-value-capture mechanism that recycles rezoning uplift into infrastructure funding, breaking the infrastructure-consent chicken-and-egg

**Tensions:**

- Infrastructure-first investment requires Crown willingness to fund capacity before private development confirms demand; the fiscal risk of stranded assets is non-trivial if growth assumptions do not materialise at projected density.

- Prioritising trunk capacity investment crowds out other housing expenditure; without parallel supply-side reforms, new infrastructure may simply be captured by land value uplift rather than translating to more affordable supply.


**Interventions on the system:**

- Multi-decade infrastructure investment programme for the Northwest and Southern growth corridors, co-funded Crown/Council at 70/30, unlocking consented capacity for ≥50,000 dwellings within 15 years.
 (state variable: `annual_consents`, sign: +) (relaxes: `infrastructure capacity gate on supply`)
- Mandatory land-value-capture levy on rezoning uplift, ring-fenced to infrastructure funding, reducing the net fiscal cost of the infrastructure-first programme.
 (state variable: `construction_cost_index`, sign: -)


### Claims cited on this page

- **Auckland has consented roughly 10,000–20,000 new dwellings per year over the past decade, with a peak around 2022 driven by the NPS-UD pipeline and material contraction since. Completions lag consents by 12–24 months and are typically 10–20% lower due to cancellations and project delays.
** — Building Consents Issued: December 2023.
- **Construction costs in New Zealand rose approximately 30–40% between 2020 and 2023 on the Capital Goods Price Index for construction, driven by materials and labour cost inflation following COVID-19 supply disruptions. The rise has only partially unwound since, compressing developer margins and reducing the viability of new housing projects.
** — Building Consents Issued: December 2023; New Zealand Productivity Commission — Housing Affordability Inquiry (2012).
- **New Zealand construction-sector labour productivity growth has been close to flat for decades — among the lowest in the OECD. Output per worker in residential construction has not improved materially since the 1990s, meaning that rising dwelling costs reflect real resource inputs rather than speculative margin, and that supply-side cost reduction requires structural change to the production model, not incremental reform.
** — New Zealand Productivity Commission — Housing Affordability Inquiry (2012); Housing in Aotearoa: 2023.

### Systems-model notes

*State variables:* construction_cost_index, annual_consents, annual_completions, construction_sector_capacity.

*Constraints:* Craft-based production model with flat productivity limits cost reduction without structural transformation, Pre-sales finance model ties construction starts to buyer confidence, amplifying cyclical contraction, Infrastructure gating: trunk capacity must precede private development at scale, Fragmented builder ecosystem prevents scale economies and amplifies workforce hysteresis.

*Inputs:* materials_price_index, skilled_workforce_availability, credit_conditions_for_developers, infrastructure_capacity_headroom, prefab_adoption_rate.


*Feedback loops:*

- `Construction downturn → firm exits → workforce exits → slower capacity recovery in next upturn (hysteresis)`
- `Higher construction_cost_index → reduced developer margin → fewer viable projects → lower annual_completions → sustained price pressure`
- `Infrastructure under-investment → consented land not built out → supply pipeline stalls despite zoning reform`


</details>

---

*Generated from `problem.auckland.housing.supply_economics` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
