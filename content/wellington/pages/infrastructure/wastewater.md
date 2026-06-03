---
title: "Wastewater overflows contaminating Wellington Harbour"
section: infrastructure
subpage: wastewater
order: 2
updated: 2026-04-26
summary: >
  Wellington's combined stormwater and wastewater network produces regular overflow events during heavy rainfall, discharging untreated sewage into Wellington Harbour. These events trigger beach closures and ecosystem damage and reflect decades of underinvestment in separation of stormwater and wastewater infrastructure.
status: draft
generated_from: problem.wellington.infrastructure.wastewater
---

# Wastewater overflows contaminating Wellington Harbour

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Overflow events and harbour health

Wellington Water records approximately 120 wastewater overflow events annually, the majority occurring during rainfall events that cause stormwater inflow into the combined sewer network (claim.wellington.infrastructure.wastewater_overflow_events). These discharges elevate harbour E. coli concentrations and trigger swimming advisories.


## Beach closures

Harbour beaches including Oriental Bay and Kilbirnie Park beach regularly exceed E. coli safety thresholds following rainfall events (claim.wellington.infrastructure.harbour_ecoli_exceedances), directly affecting recreational use and public health.


---


## Drivers

The following structural drivers contribute to this problem.


### Combined stormwater-wastewater sewer network



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Infrastructure renewal funding gap



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Combined Sewer Separation Programme

Eliminating combined sewer overflows requires full separation of storm and wastewater in affected catchments.

**Flagship moves:**

- Complete sewer separation in Brooklyn and Newtown by 2030
- Private property drain separation subsidy scheme
- Real-time overflow monitoring and public reporting dashboard

**Tensions:**

- Full separation is extremely costly ($1B+ estimated for Wellington City alone)
- Stormwater separation diverts volume to receiving environments, requiring separate treatment

**Interventions on the system:**

- Prioritise sewer separation in the 10 highest-overflow-frequency catchments using current WW monitoring data (state variable: `cso_frequency`, sign: -) (relaxes: `combined_sewer_legacy`)


### Wastewater Treatment Technology Upgrade

Upgrading Moa Point WWTP to tertiary treatment reduces harbour contamination without requiring full pipe separation.

**Flagship moves:**

- Tertiary treatment upgrade at Moa Point to reduce nitrogen and phosphorus discharge
- UV disinfection upgrade for wet-weather peak flow treatment
- Real-time harbour water quality notifications linked to overflow events

**Tensions:**

- Treatment upgrades do not address combined overflow events during heavy rain
- Downstream focus may be cheaper short-term but does not resolve the ageing network root cause

**Interventions on the system:**

- Fund Moa Point tertiary treatment upgrade to reduce nitrogen to <5mg/L (state variable: `harbour_nutrient_load`, sign: -)


---

## Claims cited on this page

- **Wellington Water recorded approximately 120 wastewater overflow events annually (2020-2023), exceeding design standards during heavy rain. Aging pipe networks require replacement; inflow and infiltration management remains a $200M+ investment priority to comply with environmental standards and protect public health.** [value: 120 overflow events per year; 2022-2023] *(confidence: medium)* — Wellington Water Asset Management Plan 2023; Wellington Harbour Water Quality Monitoring Report 2023.
- **Wellington Harbour beaches regularly exceed the E. coli safety threshold for swimming following rainfall events, with swimming advisories issued for Oriental Bay, Kio Bay, and other popular locations multiple times per year.** — Wellington Harbour Water Quality Monitoring Report 2023.

---

## Further reading


- **Wellington Water Asset Management Plan 2023** (Wellington Water Limited), 2023 — <https://www.wellingtonwater.co.nz/your-water/infrastructure/>

- **Wellington Harbour Water Quality Monitoring Report 2023** (Greater Wellington Regional Council), 2023 — <https://www.gw.govt.nz/environment/harbours-and-estuaries/wellington-harbour/>


---

## Technical notes

*State variables:* overflow_events_per_year, harbour_ecoli_concentration.

*Constraints:* combined_sewer_overflow_capacity, separation_programme_funding.

*Inputs:* rainfall_intensity, stormwater_inflow_to_sewer.


*Feedback loops:*

- `Rainfall intensification loop: increasing storm intensity under climate change increases overflow frequency, accelerating public demand for remediation while capital costs also rise.`


---

*Generated from `problem.wellington.infrastructure.wastewater` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
