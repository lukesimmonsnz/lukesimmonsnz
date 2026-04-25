# Briefing v0 — Auckland Housing: Supply Economics

**Status:** Draft for Luke's review. Not for publication. Figures marked `[verify]` need confirming before anything ships publicly.
**Last updated:** 2026-04-22
**Author:** Claude (drafted), Luke (editor)
**Frame:** 10 / 50 / 100-year structural analysis. Named politicians and present-day policy skirmishes are deliberately minimised.

---

## 1. Purpose

Land is the stock. Supply Economics is the **flow**: how much housing gets built each year, by whom, at what cost, and in response to what signals. This sub-page is the place to describe the *system that produces dwellings* on top of the land substrate, and the durable constraints on its output.

The Land sub-page already covered what land is available, owned by whom, and zoned how. This sub-page does not re-litigate that. It picks up one level downstream.

---

## 2. Systems decomposition

Engineering frame first:

```
State variables:   annual_consents, annual_completions, dwelling_stock,
                   housing_typology_mix, construction_cost_index,
                   developer_margin, industry_firm_count, workforce_size,
                   share_of_supply_by_actor_type

Inputs:            price_signals (sale prices, rents), interest_rates,
                   population_growth, migration_flows, infrastructure_capacity,
                   zoning_decisions, public_investment, immigration_of_skills

Constraints:       land_availability, regulatory_consenting_time,
                   infrastructure_pipeline, construction_firm_capacity,
                   labour_force_skill_mix, finance_availability,
                   materials_supply_chain, building_code

Feedback loops:
  - prices -> developer_margin -> new_supply -> prices (negative feedback,
    the classic market response — but lagged 2–4 years)
  - cyclical_contraction -> firm_exits -> workforce_exits -> loss_of_capacity
    -> slower_response_in_next_upturn (hysteresis — supply elasticity falls
    over repeated cycles)
  - infrastructure_capacity <-> supply_rate (bidirectional — capacity gates
    supply, supply-driven rates revenue funds capacity)
  - public_builder_counter_cyclical_investment -> stabilised_workforce ->
    maintained_private_capacity (claimed but empirically contested)

Interventions (per solution camp): each camp proposes to pull different
state variables or relax different constraints. Structured per camp below.
```

---

## 3. Scale and history

**Annual consents.** Auckland has consented roughly 10,000–20,000 new dwellings per year over the last decade, with a peak around 2022 and a material contraction since. Over 50- and 100-year windows, the cycle is the dominant story, not the level. `[verify: Stats NZ building consents series, Auckland region]`

**Completions lag consents by 12–24 months** and are typically lower than consents by 10–20% due to cancellations, defaults, and multi-year projects.

**Dwelling typology mix has shifted sharply.** Historically detached-dominated, Auckland consents are now majority multi-unit (townhouses and apartments). This is the 2016 Unitary Plan's most visible effect. `[verify: RIMU dwelling consents by type]`

**Long-run net additions are small relative to stock.** With ~600,000 dwellings in the region and ~15,000 net additions per year, the stock turns over slowly. Even sustained high-supply regimes change the built environment slowly.

**Historical cycles.** The sector is deeply cyclical — post-1970s oil shock, 1987 crash, 2008 GFC, 2022 contraction. Each downturn destroys productive capacity that is slow to rebuild.

---

## 4. Who builds

Auckland's supply is delivered by a heterogeneous mix of actors with very different time horizons, financial structures, and motivations. This is a durable structural feature.

- **Small-scale residential builders** (1–20 houses/year). Historically the majority of detached supply. Highly cyclical — exit on every downturn.
- **Mid-size developers** (townhouse and small-apartment volume). The fastest-growing segment since the Unitary Plan's intensification zones.
- **Large-scale developers** (apartment towers, master-planned communities). Concentrated; capital-intensive; dependent on pre-sales and project finance.
- **Group-home builders** (Fletcher Living, GJ Gardner, Mike Greer, etc.). National-scale, standardised product, modest productivity gains from scale.
- **Kāinga Ora** — Crown public-housing builder. Significant build programme through 2020s; politically cyclical.
- **Community Housing Providers (CHPs)** — third-sector builders including iwi-linked entities. Growing share.
- **Iwi development arms** — Ngāti Whātua Ōrākei, Tainui Group Holdings, Auckland iwi entities. Intergenerationally motivated; non-exiting.
- **Owner-builders and self-build** — small, but a meaningful share of detached supply historically.

**Durable point:** no one actor dominates. Changes to one channel (e.g. weakening Kāinga Ora) leave others intact. This is both a resilience and a coordination problem.

---

## 5. Construction economics — the cost stack

A rough anatomy of what a new Auckland dwelling costs to produce. Structural categories, not point figures:

| Component                                    | Driver of variation                                  |
|----------------------------------------------|------------------------------------------------------|
| Land (serviced)                              | Location, zoning, infrastructure, title fragmentation |
| Hard construction cost                       | Materials, labour, complexity, code                  |
| Finance cost (during build)                  | Interest rates, project duration, debt/equity mix    |
| Infrastructure contributions (DRCs, levies)  | Council settings, infrastructure need                |
| Consenting and design                        | Regulatory complexity, reviewer capacity, appeals    |
| Developer margin (required to fund next project) | Risk premium, cost of capital                    |
| GST and compliance                           | Policy settings                                      |

**Over 10 years, the stack has shifted materially** — materials and labour cost rose ~30–40% post-2020; financing cost rose with OCR; infrastructure contributions have trended up. On a 50-year view the level is less important than the *relative shares*: NZ construction has one of the lowest productivity growth rates in the OECD, so the labour and materials share has tended to rise relative to GDP-per-hour in other sectors. `[verify: NZ Productivity Commission / MBIE construction sector productivity reports]`

**Developer margin is load-bearing.** A project that doesn't return ~15–20% margin on cost typically cannot finance the next one. If costs rise faster than sale prices, margin compresses, projects get cancelled, and the pipeline thins regardless of underlying demand. This is the main mechanism by which housing affordability crises are self-perpetuating.

---

## 6. Supply elasticity and international comparators

The central analytical question on this page: **how responsive is Auckland's supply to demand?** Elasticity is the quantitative measure.

**Historical consensus:** Auckland was highly supply-inelastic through roughly 1990–2015. Prices rose far faster than supply expanded. This is a definitional property of any housing crisis.

**Post-Unitary Plan evidence:** Greenaway-McGrevy and collaborators argue the 2016 upzoning measurably raised elasticity — Auckland built more than it would have, and rents grew less than in comparable New Zealand cities without upzoning. Magnitude contested; direction mostly agreed.

**International archetypes** (the comparison is the engineering move — it reveals which constraints are binding):

- **Tokyo.** National-level permissive zoning, large number of small private builders, strong small-apartment tradition. Consistently highest supply elasticity of major rich-country cities. Population steady, but housing stock continuously replaced.
- **Houston / Dallas.** Permissive land, greenfield expansion, supply-elastic — at the price of sprawl, car dependence, and climate exposure.
- **Vienna.** Dominant public and cooperative housing sector delivers ~50% of supply at scale, stabilising prices across cycles. Market-share, not market-reform, is the lever.
- **Singapore.** HDB (government builder) delivers the majority of housing; freehold is the exception. Centralised model; not easily transplantable, but instructive on what scale looks like.
- **London, Sydney, Melbourne.** Close structural analogues to Auckland — supply-inelastic, high prices, similar regulatory politics. Worth comparing directly.
- **Nordic prefabrication** (Sweden, Finland). Heavy use of factory-built modular components has raised construction productivity.

Auckland's current supply elasticity is higher than 2015 but lower than any of Tokyo / Houston / Vienna / Singapore. The question for a 100-year frame is which archetype the city is drifting toward — or whether it sustains a distinct hybrid.

---

## 7. Durable constraints on supply

Features of the supply system that a reader in 2076 will still recognise:

1. **Cyclicality.** The sector boom-busts every 7–15 years. Each bust destroys firms and workforce. On a 100-year view, this is the single most consequential structural feature, because it erodes capacity over time.
2. **Weak productivity growth.** NZ construction productivity has been roughly flat for decades. Without structural change, the cost stack will keep rising relative to the economy.
3. **Labour force constraints.** Construction depends on a slow-to-train workforce. Skill shortages in key trades (brickies, sparkies, plumbers) recur in every boom.
4. **Infrastructure-gated capacity.** Even where zoning permits, developments stall on water, wastewater, stormwater, and transport capacity.
5. **Finance pro-cyclicality.** Banks tighten lending at exactly the moment developers need it most. The bank-developer relationship shapes what gets built more than any single regulation.
6. **Material import dependence.** NZ imports most structural materials. Global supply chain shocks feed directly into costs with limited local substitution.
7. **Small domestic market.** Auckland's scale is too small to support standardised mass production at Tokyo or Houston scale. Productivity gains via scale are structurally limited.
8. **Regulatory regime instability.** Consenting rules, heritage overlays, and the broader RMA regime change on decadal timescales. Planning stability is a commons the system regularly loses.
9. **Public builders are politically cyclical.** Kāinga Ora's build rate rises and falls with government. Non-market supply is therefore not a full counter-cyclical stabiliser unless its funding and mandate are insulated from electoral cycles.
10. **Iwi as the only long-horizon builder.** Among actors, iwi development arms alone have a 100-year time horizon and cannot exit. On a 50- and 100-year view, this matters more than the current literature suggests.

---

## 8. The durable long-run questions

- What supply elasticity should Auckland aim for, and is that achievable given the city's physical and market size?
- How is the boom-bust cycle to be damped — through counter-cyclical public build, credit-cycle regulation, or accepting it as a fact of life?
- Should the housing-production system rely on a diverse ecosystem of builders, or concentrate on a few large actors (public, private, or iwi) at scale?
- How is construction productivity to be raised — through prefabrication and MMC, regulatory standardisation, immigration of skills, or structural consolidation?
- What share of new supply should come from non-market actors (Crown, CHPs, iwi) on a 50-year horizon?
- How should the building code be balanced between resilience/thermal performance (raising cost) and affordability (lowering cost)?
- What financing architecture produces stable housing delivery across cycles — current bank-debt-and-pre-sales, or build-to-rent / long-term equity / pension capital?
- How does climate adaptation (insurance pricing, managed retreat) re-shape where and what gets built?

---

## 9. Solution camps on supply economics (neutral presentation)

Distinct from the Land camps — here the camps are interventions on the *production system*, not the land stock.

### A. Market reform / deregulation
**Core claim:** the binding constraints are regulatory consenting time and infrastructure contributions. Remove them and supply rises.
**Flagship moves:** compressed consenting timelines, permitted-activity intensification, reform of DRCs, reduction of appeal pathways.
**Weakness:** the land, skills, finance, and cycle constraints don't disappear; supply-elastic regulation on a supply-inelastic workforce produces delays, not dwellings.

### B. Public / community builder at scale
**Core claim:** the market will always be pro-cyclical; a large, counter-cyclically funded public and community builder is needed to maintain delivery through downturns and at the bottom of the market.
**Flagship moves:** Kāinga Ora recapitalisation, CHP finance and scale, long-horizon housing-investment fund.
**Weakness:** fiscal cost, historical KO build-cost issues, politically fragile when out of favour.

### C. Industrial transformation / prefabrication
**Core claim:** the real constraint is productivity. Shift from site-based craft construction to factory prefabrication, standardised components, and Modern Methods of Construction.
**Flagship moves:** scale prefab factories, standardised designs, code reform to enable manufactured housing, public procurement to anchor demand.
**Weakness:** NZ market is small for standardisation; prefab has repeatedly over-promised; up-front capital required is large.

### D. Infrastructure-first
**Core claim:** zoning without infrastructure is theatre. Supply is gated by water, wastewater, stormwater, and transport capacity. Build capacity ahead of demand and supply will follow.
**Flagship moves:** sustained Crown/Council investment in trunk infrastructure, growth-focused Watercare funding, land-value-capture to fund upfront infrastructure.
**Weakness:** fiscal cost, timing risk, political feasibility of pre-investment.

### E. Demand-smoothing / counter-cyclical management
**Core claim:** the cycle itself is the problem. Policy should aim to damp boom-bust — through credit-cycle regulation, migration smoothing, tax stability.
**Flagship moves:** macroprudential rules tied to housing cycle, stable immigration settings, removal of tax-driven investor boom-bust.
**Weakness:** cross-cutting with national policy; imperfect tools; may trade cycle for lower long-run average.

### F. Skills and workforce
**Core claim:** without enough trained builders, every other lever is noise. Invest in workforce pipeline — training, apprenticeships, skills immigration, retention.
**Flagship moves:** expanded trades training, visa pathways for construction skills, industry-government workforce agreements.
**Weakness:** decade-long payback; training responds to cycles, exacerbating volatility.

### G. Iwi and intergenerational delivery
**Core claim:** iwi development arms are uniquely well-suited to long-horizon supply. Scale them as a durable delivery vector.
**Flagship moves:** Crown co-investment in iwi housing pipelines, enabling of iwi-led master plans, financing vehicles that suit intergenerational ownership.
**Weakness:** scale constraints; capacity building takes time; solves a slice of the problem, not its whole scope.

### H. Finance reform
**Core claim:** the bank-debt-and-pre-sales financing model is the root cause of cyclicality. New architectures (long-term build-to-rent equity, pension capital, state development bank, infrastructure bonds) would stabilise delivery.
**Flagship moves:** build-to-rent tax settings, KiwiSaver channelling into housing finance, a state development bank, infrastructure bond markets.
**Weakness:** untested at NZ scale; regulatory change required; risk of distorting outcomes toward the wrong product types.

In practice, real policy programmes combine three or four of these. The public page should show all eight and let the reader see which overlap and which genuinely conflict.

---

## 10. Conflict-of-interest flag (private to you)

Less direct than the Land page — your disclosed holdings are on the *stock* side, and Supply Economics is on the *flow* side. But two alignments are worth naming:

- **Camp D (Infrastructure-first)** connects to your disclosed view on Auckland wholesale borrowing for infrastructure. Be wary of framing Camp D as more intuitive or better-supported than the others.
- **Camp B (Public / community builder at scale)** and **Camp G (Iwi and intergenerational delivery)** are both *institutional* reform positions, and they align directionally with your conservation/density-favouring preferences only indirectly — scaling public or iwi builders reduces pressure to expand at the metropolitan edge.

The conflict surface here is smaller than on Land. But the same rule applies: if you catch me writing in a way that makes one camp feel more reasonable than the others, flag it.

---

## 11. Sources to spot-check

Primary data:
- **Stats NZ** — building consents (Auckland region), dwelling stock, construction GDP
- **MBIE** — tenancy bond data (rents), construction sector reports
- **RIMU (Auckland Council)** — Auckland-specific consents by type, geography, actor
- **Kāinga Ora** — annual reports, build programme data
- **CoreLogic / REINZ** — market price series

Analytic:
- **NZ Productivity Commission** — construction productivity reports
- **Infrastructure Commission / Te Waihanga** — infrastructure pipeline and fiscal analysis
- **Ryan Greenaway-McGrevy (UoA)** — upzoning and elasticity papers
- **RBNZ** — financial stability reports on construction sector exposure
- **Treasury** — housing affordability and fiscal impact analysis

International:
- **OECD Housing Policy Toolkit**
- **UN-Habitat** — urban economic indicators
- **Tokyo Metropolitan Government** housing stats (for the Tokyo archetype)
- **Vienna Gemeindewohnungen / Wohnfonds Wien** (for the Vienna archetype)
- **HDB Singapore** annual reports
- **Greater London Authority** / Centre for Cities (London comparator)

Commentary:
- **Greater Auckland**
- **Bernard Hickey / The Kākā**
- **New Zealand Initiative** — market-side analysis

---

## 12. Open questions for you

1. **International comparators — how deep?** My default is a half-section referencing four archetypes (Tokyo, Vienna, Houston, London-like cities) to frame what different elasticity regimes look like. Should this be fuller, briefer, or a dedicated sub-section (with its own public heading)?
Luke: Subsection.
2. **Overlap with Public Housing and Māori Housing subpages.** Camps B and G will appear again (in dedicated form) on those subpages. On this page, should the treatment be brief (pointer) or full (same depth as the other camps, accepting some duplication)?
Luke: Brief, there would also be plenty of intergenerational family trusts who have large land holdings but are not public knowledge because of how the trusts act privacy rules work. 
3. **Cost-stack section.** I've used a generic table with structural categories rather than point figures. Do you want point figures (with `[verify]` markers) for the typical Auckland dwelling in 2025, or keep it structural for longevity?
Luke: Structural. 
4. **Charts for this page.** Obvious candidates: (a) annual consents 2000–2025, (b) consents-by-typology over time showing the intensification shift, (c) price-to-consents lag (showing cycle), (d) construction productivity vs. other sectors, (e) international elasticity comparison. Pick any subset.
Luke: Include all.
5. **Cyclicality as a first-class concept.** The engineering frame treats cyclicality as the dominant feature. Some commentators disagree — they treat the long-run average as the thing to fix, arguing cycles will persist regardless. Do you want the page to foreground cyclicality (my current draft) or treat it as one constraint among many?
Luke: Constant among many.
6. **Eight camps vs. fewer.** Land had seven. Supply has eight as drafted; some are close cousins (B and G overlap; D overlaps with institutional reform from Land). Would you prefer me to consolidate to five or six clearer camps on the public page?
Luke: Five camps for simplicity. 

Once you've answered, I'll extract the Problem, Camps, Drivers, Evidence, and Source entities into `data/`, run the lint, regenerate, and the page will be live at `/auckland/housing/supply-economics/`.
