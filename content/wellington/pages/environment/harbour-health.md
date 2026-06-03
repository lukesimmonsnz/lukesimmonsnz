---
title: "Degraded water quality in Te Whanganui-a-Tara Wellington Harbour"
section: environment
subpage: harbour-health
order: 1
updated: 2026-04-26
summary: >
  Wellington Harbour receives significant stormwater, wastewater overflow, and contaminant loads from the urbanised catchment, resulting in periodic beach closures and impaired ecosystem function. While baseline water quality is moderate, rainfall-driven contamination events are frequent and the long-term trajectory under climate change is adverse.
status: draft
generated_from: problem.wellington.environment.harbour_health
---

# Degraded water quality in Te Whanganui-a-Tara Wellington Harbour

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Beach closures and public health

Several Wellington Harbour beaches experience recurrent E. coli exceedances following rainfall, with beach closure advisories issued multiple times per year at Oriental Bay, Kio Bay, and other popular swimming locations (claim.wellington.environment.harbour_ecoli_beach_closures).


## Stormwater as primary vector

Stormwater from urban catchments carrying surface contaminants — animal waste, litter, sediment, heavy metals from road runoff — is the dominant contamination pathway in the harbour during and immediately after rainfall (claim.wellington.environment.harbour_stormwater_contamination).


---


## Drivers

The following structural drivers contribute to this problem.


### Combined sewer overflow discharge to harbour



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Combined stormwater-wastewater sewer network



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Urban catchment impervious surface expansion



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Urban stormwater contaminant load



- **Category:** physical
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


### CSO Reduction and Harbour Water Quality Programme

Reducing combined sewer overflows is the single most effective intervention for improving Wellington Harbour water quality.

**Flagship moves:**

- Real-time CSO monitoring network across Wellington Harbour catchment
- Priority sewer separation in highest-overflow suburbs
- Stormwater detention basins to buffer peak flows

**Tensions:**

- Full separation is a multi-decade programme; interim water quality improvement is limited
- Stormwater detention land acquisition is expensive in the dense inner city

**Interventions on the system:**

- Install 80 CSO monitoring sensors across Wellington Harbour tributaries and publish real-time data (state variable: `harbour_ecoli_concentration`, sign: -)


### Harbour Ecology and Seagrass Restoration

Active restoration of seagrass beds and intertidal zones will rebuild harbour ecology beyond just reducing pollution inputs.

**Flagship moves:**

- Seagrass restoration trials in Evans Bay and Porirua Harbour
- Expand marine reserve zones in Wellington Harbour
- Community-led predator control on harbour-edge restoration areas

**Tensions:**

- Ecological restoration is ineffective while CSO contamination continues
- Marine reserve expansion creates tensions with recreational fishing communities

**Interventions on the system:**

- Fund 5-year seagrass restoration programme across 3 Evans Bay and Porirua Harbour sites (state variable: `harbour_seagrass_coverage_ha`, sign: +)


---

## Claims cited on this page

- **Greater Wellington Regional Council water quality monitoring records recurrent E. coli exceedances at multiple Wellington Harbour beaches following rainfall, with Oriental Bay and other popular swimming locations subject to periodic swimming advisories throughout the summer season.** — Wellington Harbour Water Quality Monitoring Report 2023.
- **Stormwater discharges from Wellington's urban catchments are the dominant contamination pathway for Wellington Harbour during and immediately after rainfall events, carrying surface contaminants including animal waste, litter, sediment, and heavy metals from road runoff.** — Wellington Harbour Water Quality Monitoring Report 2023; Greater Wellington State of the Environment Report 2022.

---

## Further reading


- **Wellington Harbour Water Quality Monitoring Report 2023** (Greater Wellington Regional Council), 2023 — <https://www.gw.govt.nz/environment/harbours-and-estuaries/wellington-harbour/>

- **Greater Wellington State of the Environment Report 2022** (Greater Wellington Regional Council), 2022 — <https://www.gw.govt.nz/environment/state-of-the-environment/>


---

## Technical notes

*State variables:* harbour_ecoli_concentration, beach_closure_days_per_year.

*Constraints:* combined_sewer_system_design, catchment_impervious_surface_area.

*Inputs:* wastewater_overflow_volume, stormwater_runoff_load.


*Feedback loops:*

- `Rainfall-contamination pulse: each significant rainfall event produces a contamination pulse that temporarily renders recreational zones unsafe, concentrated near stormwater outfalls.`


---

*Generated from `problem.wellington.environment.harbour_health` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
