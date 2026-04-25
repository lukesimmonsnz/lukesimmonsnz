# Scaling Auckland to Aotearoa: a migration plan

The dominant scaling challenge is **schema redesign first, content authoring volume second** — the two are coupled, but the schema decision determines whether content scales linearly (~16×) or super-linearly (~16² for cross-comparisons). The recommended target is a **single unified site backed by a region-tagged typed entity graph**, not 16 sibling projects and not a strict national→regional→local hierarchy. The graph itself is the hierarchy; the URL structure exposes a region facet (`/research/<region>/<theme>/`) over a flat data store. This preserves the existing Auckland project as `region=auckland` and lets Wellington, Northland, and the national rollup share schema, lint rules, citation infrastructure, and the AI-co-authoring workflow without forking the codebase.

The rest of this document is the working plan. **Section 1** sets the architecture. **Section 2** redesigns the entity graph. **Section 3** is the NZ data-source catalogue Claude Code can ingest directly. **Section 4** is the authoring strategy. **Section 5** specifies tooling changes (lint, graph, agent workflow, Flask). **Section 6** mines international precedents. **Section 7** is a phased migration plan with effort estimates.

---

## 1. Architectural recommendation: unified-with-region-facets

### The three options compared

| Dimension | **Unified + region facets** (recommended) | 16 sibling projects + national overlay | Strict national → regional → local hierarchy |
|---|---|---|---|
| **URL structure** | `/research/<region>/<theme>/[sub]` with `nz` as a first-class region | `/auckland/...`, `/wellington/...`, plus `/nz/...` overlay | `/nz/<theme>/<region>/<theme>/<ta>/...` |
| **Graph topology** | Flat node store; every node tagged `region_scope: list[Region]` | 16 disjoint graphs + a 17th national graph; cross-graph joins are manual | Tree with strict parent edges; awkward for cross-cutting concerns |
| **Claim reusability** | **Native** — a national claim with `region_scope: [nz]` is one node; a multi-region comparison is one node citing region-tagged claims | Painful — same claim duplicated or split across repos; cross-region comparison requires CI-time joins | Possible but rigid; "national pattern manifest in Auckland" is hard to model without duplication |
| **Lint complexity** | Single rule set with region-aware predicates | 17× rule sets to keep in sync | Rules must traverse hierarchy; "is this claim national or regional?" becomes a structural decision |
| **Navigation UX** | Region switcher + theme switcher are independent facets | Region change = full site change (jarring); cross-comparison is a separate site | Forced top-down navigation; users who arrive at "Auckland housing" via search must traverse upward |
| **Content drift** | **Lowest** — same Pydantic schema, same methodology registry, single CLAUDE.md per theme | **Highest** — Auckland's framings ossify and get copy-paste-mutated to other regions | Medium — hierarchy implies national authority but leaves regional authors free to drift |
| **National vs regional reasoning** | Naturally expressed: a `Pattern` node has `manifests_in: [region_a, region_b...]`; an `Instance` node has `region: <single>` | Requires explicit "national overlay" repo, double-counting risk | Confuses scale with authority — national doesn't always precede regional empirically |
| **Solo-developer overhead** | One repo, one CI, one schema | 17 repos to maintain | One repo, but rigid traversal logic is brittle |
| **Auckland backwards compat** | Trivial — existing nodes get `region_scope: [auckland]` retroactively | Trivial — Auckland repo unchanged | Requires re-rooting Auckland under a national parent |

**Why unified wins for this project specifically.** The Auckland project's existing strengths — a typed entity graph, every claim citing a primary source, neutral framing, AI co-authoring — are *all* properties of the schema and the build pipeline, not the URL structure. Sibling projects double the surface area for those properties to drift. A strict hierarchy embeds an empirical claim — that national patterns precede regional ones — that is **wrong for half of NZ's policy domains** (housing dynamics in Auckland drive national policy; West Coast climate-adaptation needs are not derivable from the national plan).

The unified architecture treats **scale as a tag, not a structure**. National, regional, and TA-level claims are all nodes in the same graph; what differs is `region_scope` and `granularity` metadata. This is the same insight Stats NZ's Aotearoa Data Explorer and ONS's Subnational Indicators Explorer converged on — geography is a dimension, not a partition.

### Recommended URL scheme

```
/research/                                 # site root
/research/nz/                              # national overview
/research/nz/housing/                      # national housing rollup
/research/auckland/                        # regional overview (existing)
/research/auckland/housing/                # regional theme page
/research/auckland/housing/affordability/  # sub-theme
/research/compare/housing/akl-vs-wlg/      # pre-rendered comparison
/research/themes/housing/                  # theme-first navigation (cross-region small multiples)
/entities/                                 # typed-entity browser (Datasette)
/archives/2026-Q2/...                      # immutable quarterly snapshots (SEP pattern)
```

Region-first beats theme-first for most search intent ("Auckland housing" > "housing in Auckland"), but theme-first pages exist as cross-region small-multiples views. Pre-render the most useful pairwise comparisons; for the long tail, lean on Pagefind's filter facets rather than generating C(16,2)=120 comparison pages.

### Versioned archives, after Stanford Encyclopedia of Philosophy

A 100-year horizon project must be **citable at a fixed version** even while the live document evolves. SEP's quarterly archive pattern is the proven solution. Implement `/archives/2026-Q2/...` as immutable snapshots written by a CI job, with a "How to cite" footer on every page directing scholars to the archived URL. The live site stays at `/research/...`. This is one small piece of build pipeline that pays compounding interest over decades.

---

## 2. Schema and entity-graph evolution

### Core question: when is something national vs regional?

This is a **modeling decision, not a data decision**, and the schema must let both shapes coexist without forcing a choice. The discipline:

- A **`Pattern`** is a generalisation that may manifest in multiple regions (e.g., "speculative land-banking inflates urban-fringe prices"). Patterns have `manifests_in: list[Region]` and `evidence: list[ClaimId]`.
- An **`Instance`** is a region-specific claim (e.g., "Auckland's median-multiple was 8.4 in 2024"). Instances have `region_scope: list[Region]` (typically a single region, but a Wellington-and-Auckland comparison is `[auckland, wellington]`).
- A `Pattern` cites `Instance`s as evidence; an `Instance` may *invoke* a `Pattern` to explain its causes.
- A claim is **national** when its evidence base is a national dataset OR when it generalises across a documented set of regions; it is **regional** when its evidence is region-specific. Don't confuse "produced by a national agency" with "scoped nationally" — Stats NZ produces region-specific datasets too.

### Recommended graph shape

The minimal node and edge inventory:

```
Node types:
  Region          (taxonomy: 16 regions + nz + the 67 TAs as sub-regions)
  Theme           (housing, transport, ...)
  Source          (citable artifact: dataset version, report, page)
  Claim           (statement with region_scope, evidence, methodology_tag)
  Pattern         (cross-regional generalisation)
  Problem         (named issue, e.g. "missing middle housing")
  Driver          (causal/contributing factor)
  Camp            (named solution school of thought)
  Evidence        (claim used as support; can be the same node as Claim)
  Indicator       (typed metric: e.g. dwellings_consented_per_capita)
  Methodology     (named, versioned: e.g. demographia_median_multiple_v2024)
  IbisNode        (Issue / Position / Argument-pro / Argument-con)
  Actor           (gov body, council, iwi, firm)
  Policy          (named instrument: NPS-UD, MDRS, RMA replacements)

Edge types:
  cites           Claim → Source
  manifests_in    Pattern → Region
  evidenced_by    Pattern → Claim
  scoped_to       Claim → Region (multi-cardinality)
  measured_by     Claim → Indicator
  follows         Claim → Methodology
  causes          Driver → Problem
  addresses       Camp → Problem
  governs         Actor → Region
  applies_in      Policy → Region
  supersedes      Claim → Claim (versioning)
  parent          IbisNode → IbisNode
  invokes         Claim → Pattern
```

### Region parameterisation: the seven entities

| Entity | Region parameterisation | National vs regional rule |
|---|---|---|
| **Problem** | `manifests_in: list[Region]`; severity may vary by region. | A Problem is national if it manifests in ≥10 regions (rule of thumb) or is governed by a national instrument. Otherwise regional. |
| **Driver** | Drivers can be national (RMA framework) or regional (Auckland geographic constraint). Tag with `scope` enum {national, regional, local}. | A driver causing a national pattern can still have region-specific intensities. Use `intensity_by_region: dict[Region, float]`. |
| **Camp** | Solution camps are usually national in their canonical statement, but their **applicability** varies by region. Add `applicable_in: list[Region]` and `evidence_of_efficacy_in: list[Region]`. | A camp built on Tokyo zoning evidence applies to Auckland with weaker confidence; encode confidence as edge weight. |
| **Evidence (Claim)** | `region_scope` is the primary parameter. | Comparison claims have ≥2 regions and require shared `methodology_tag`. |
| **Source** | Sources are not regional per se — a Stats NZ dataset *contains* regional breakdowns. Tag sources with `geo_granularity: Set[Granularity]` instead. | A source can ground both national and regional claims if the data supports it. |
| **Indicator** | Indicators are method-defined, not region-defined. The same indicator (e.g., `median_house_price_to_income`) is computed per region. | Define each indicator once with `granularities_supported`. |
| **Methodology** | Versioned, named, region-agnostic in definition. | The lint rule: comparison claims require **identical methodology_tag** across compared regions, otherwise raise. |

### Cross-regional comparisons as first-class nodes

A claim like "Auckland housing is less affordable than Wellington" is a `Claim` with:

```yaml
id: c_akl_wlg_affordability_2024
statement: "In 2024, Auckland's median-multiple (8.4) exceeded Wellington's (6.1)."
region_scope: [auckland, wellington]
theme: housing
methodology_tag: demographia_median_multiple_v2024
evidence:
  - c_akl_median_multiple_2024
  - c_wlg_median_multiple_2024
sources: [src_demographia_2024]
as_of: 2024-12-31
```

The graph stores both the rolled-up comparison node and its two evidence nodes. The lint enforces (a) both evidence nodes exist, (b) both share `methodology_tag`, (c) the comparison's `as_of` is consistent with both. This pattern handles 2-region, 16-region, and quartile-rank claims uniformly.

### Inheritance vs composition

Avoid OO-style inheritance; favour **composition with tags**. Don't create `AucklandHousingProblem(HousingProblem)`. Create one `Problem` node tagged with region scope and link it to region-specific `Instance`s. Inheritance bakes in a hierarchy that the graph should be free to refute.

### Backwards compatibility with Auckland data

Every existing Auckland claim gets `region_scope: [auckland]` retroactively in a one-time migration script. Existing nodes without `methodology_tag` get a placeholder `legacy_v0` tag and are flagged by lint until a real tag is supplied. A `migration_log.yaml` records the script's transformations for auditability — the same provenance discipline applied to the schema itself.

---

## 3. NZ-specific data sources

The catalogue below summarises what is citable, what has APIs, and what is paywalled. Verified as of April 2026; several recent structural changes (Productivity Commission disestablished 2024, Te Aka Whai Ora dissolved June 2024, NIWA + GNS merged July 2025 into Earth Sciences NZ, Three Waters repealed and replaced with "Local Water Done Well") materially affect a national-scale project and are flagged.

### Status of named bodies (April 2026)

| Body | Status | What this means for the project |
|---|---|---|
| Stats NZ, LINZ, MfE, MoH, MoE, MBIE, RBNZ, Treasury, OAG, Climate Change Commission, Te Waihanga, HQSC, ERO, Manaaki Whenua, TPK | All active | Use as primary sources |
| **NZ Productivity Commission** | **Disestablished 29 Feb 2024**. Archive at `treasury.govt.nz/.../productivity-commission-2011-2024`. URL mapping CSV released Aug 2024. | Successor: **Ministry for Regulation** (new agency, est. 2024) holds the regulatory-stewardship function. Treat ProdComm as a frozen archive for citing; new policy analysis comes from Treasury, MfR, or Te Waihanga. |
| **Te Aka Whai Ora (Māori Health Authority)** | **Disestablished 30 Jun 2024**. | Functions absorbed into Health NZ Hauora Māori directorate + IMPBs (Iwi-Māori Partnership Boards). Localities work paused until 2029/30. Series-break in Māori health datasets — flag in lint. |
| **Three Waters / Water Services Entities** | **Repealed Feb 2024**. Replaced by "Local Water Done Well" (LGWS Acts 2024–25). | Taumata Arowai retained as drinking-water regulator; Commerce Commission as economic regulator. Council water-services data heterogeneity returns. |
| **NIWA + GNS** | **Merged 1 Jul 2025 → Earth Sciences New Zealand**. | Both legacy domains still active and redirect/co-brand. NIWA also acquired MetService (Sept 2024). |
| **Te Whatu Ora / Health NZ** | Active; absorbed Te Aka Whai Ora and most former-DHB data 2022. | Primary health data publisher. |
| **Regional councils (16)** | All active. | **Watch:** Feb 2026 government floated abolishing/restructuring regional councils; no legislation yet. Treat as a continuity risk for LAWA. |

**The 16 regional/unitary councils.** Eleven regional councils (Northland, Waikato, Bay of Plenty, Hawke's Bay, Taranaki, Manawatū-Whanganui [Horizons], Greater Wellington, West Coast, Canterbury [ECan], Otago, Southland) plus five unitary authorities combining regional + TA functions (Auckland, Gisborne District, Tasman District, Nelson City, Marlborough). 67 TAs total. Aggregator bodies: Te Uru Kahika (regional councils' collective, runs LAWA), LGNZ (peak body), Local Government Commission (boundary reviews), DIA's localcouncils.govt.nz directory.

### Cross-cutting data infrastructure

The portals and APIs that should be the project's ingestion backbone:

| Portal | API surface | Format | Licence |
|---|---|---|---|
| **Stats NZ Aotearoa Data Explorer (ADE)** at `api.data.stats.govt.nz/rest/` | **SDMX REST**; subscription key (free, sign up at API Portal); header `Ocp-Apim-Subscription-Key` | JSON, XML, CSV | CC-BY 4.0 |
| **data.govt.nz CKAN** at `catalogue.data.govt.nz/api/action/` | **CKAN action + datastore APIs** | JSON | Per-dataset, mostly CC-BY 4.0 (NZGOAL) |
| **LINZ Data Service (LDS)** at `data.linz.govt.nz/services` | **WFS 2.0, WMS, WMTS, OGC API Features**; API key (free) | GeoPackage, Shapefile, GeoJSON, KML, MBTiles | CC-BY 4.0 (most) |
| **MfE Data Service** at `data.mfe.govt.nz` | Koordinates WFS/WMS | GeoPackage, Shapefile, GeoJSON, CSV | CC-BY 4.0 |
| **Stats NZ Geographic Data Service** at `datafinder.stats.govt.nz` | Koordinates WFS/WMS/WMTS | Boundaries (Reg Council 2025, TA 2025, SA1, SA2, meshblock) | CC-BY 4.0 |
| **LRIS Portal (Manaaki Whenua)** at `lris.scinfo.org.nz` | WFS + CSW | GeoTIFF, Shapefile, GeoPackage | CC-BY 4.0 (mostly) |
| **NZTA Open Data** at `opendata-nzta.opendata.arcgis.com` | **ArcGIS REST + GeoJSON + CSV** | GeoJSON, Shapefile, CSV, KML | CC-BY 4.0 |
| **Companies/Charities Registers (DIA)** | Companies Office REST API; Charities Register bulk download | JSON, CSV | CC-BY 4.0 |
| **GeoNet (Earth Sciences NZ)** at `api.geonet.org.nz` | REST, real-time seismic/volcanic | JSON, GeoJSON, miniSEED | CC-BY 4.0 |
| **Education Counts (MoE)** | Schools Directory API + ECE Directory API (CKAN datastore-backed) | JSON, CSV, XLSX | CC-BY 4.0 |
| **Electricity Authority EMI** | Bulk + Azure APIs (`emi.azure-api.net`); WITS via NZX | CSV, XLSX | EA reuse w/ attribution |
| **RBNZ** | **No REST API** — XLSX scraping; CRAN package `RBNZ` exists | XLSX, CSV | RBNZ terms (permissive w/ attribution) |
| **NZ Police data** | **No public API** (confirmed via OIA — SAS-generated CSVs only) | CSV, XLSX | CC-BY 4.0 |
| **NIWA CliFlo** | API key (free non-commercial) | CSV | **CC-BY-NC** — flag |
| **Te Whata** at `tewhata.io` | Iwi-led Census/Māori dashboard | Web + some CSV | Mana Ōrite governance — engagement required |
| **Pātaka Raraunga (Figure.NZ)** at `maori.figure.nz` | Curated Māori-focused data | Embed | Source-dependent |

### Per-theme priority sources

**Land and Housing** — Stats NZ building consents (monthly, API, SA2); HUD Government Housing Dashboard (quarterly, TA); Kāinga Ora tenancy reports (quarterly); MBIE Building Consent System Performance (quarterly, 70 BCAs); LINZ parcels and titles (daily, parcel-level); Tenancy Services / MBIE rental bond data (monthly, SA2); MfE NPS-UD/MDRS implementation (ad-hoc). Paywalled: CoreLogic, REINZ, QV for sale prices. **Critical gap:** there is **no national zoning/district-plan aggregator** — 67 TAs publish district plans heterogeneously, some on Koordinates, many in static PDFs. This is the single biggest pain point for Land & Housing systems-engineering work and will require either OIA requests or a per-TA harmonisation layer over time.

**Transport** — NZTA Open Data (ArcGIS REST, mostly monthly, RCA/segment); CAS open subset (monthly, lat/long, restricted full dataset by agreement); NZTA TMS traffic counts (daily); NZTA Speed Limit Register (continuous since May 2022); regional GTFS feeds per council (real-time + static); MoT Transport Outlook + Household Travel Survey (annual). **Gaps:** KiwiRail publishes almost no open freight/track data; no national GTFS aggregator (NZTA's national PT dataset is incomplete).

**Infrastructure** — Te Waihanga National Infrastructure Pipeline (quarterly, project-level, no formal API but bulk download); Taumata Arowai Hinekōrako register (drinking-water suppliers); council Water Services Delivery Plans (submitted Sept 2025; heterogeneous); Electricity Authority EMI; MBIE Energy Statistics (quarterly XLSX); Transpower data via EMI; Commerce Commission Information Disclosures (annual XLSX per regulated firm); Telecoms Monitoring Report.

**Environment** — MfE environmental reporting (domain reports every 3 years; synthesis biennial); MfE Data Service (Koordinates WFS/WMS); LAWA (16 RCs + partners, ~1,100 freshwater sites, bulk CSV); NZ Greenhouse Gas Inventory (annual April); Earth Sciences NZ CliFlo (CC-BY-NC — flag); Manaaki Whenua S-Map and LCDB (ad-hoc); DOC biodiversity. **Watch:** if regional council restructure proceeds, LAWA's federated model is at risk.

**Inequality** — Stats NZ HES (annual income, 3-yearly net worth); Census 2023 / Te Whata (5-yearly, SA1, iwi); MSD benefit statistics (quarterly TA); IRD tax distributions (annual, OIA-route useful for high-end concentration); IDI (DataLab access; Ngā Tikanga Paihere required for Māori data); Treasury wellbeing indicators; Child Poverty measures (annual, legislated). **Te Whata is critical for ethnic disparity analyses with Māori data.**

**Crime and safety** — `policedata.nz` (monthly, district + meshblock for some victimisations, no API); MoJ justice statistics (twice-yearly, ANZSOC 2025 revision in force from 1 July 2025 — series break); Corrections (quarterly + annual); NZCVS (annual since 2018); FENZ. **Court charge and family-violence detail is research-only.**

**Health** — Health NZ Te Whatu Ora data and statistics (varies, formerly-DHB regions in transition); MoH (annual, NZHS annual); national collections (NMDS, NMC mortality, PHARMS, NIR, Cancer Registry — restricted access; aggregates public); HQSC Atlas of Healthcare Variation (annual per domain); Pharmac; Coronial Services (quarterly provisional, annual confirmed). **Te Aka Whai Ora dissolution Jun 2024 created series breaks**; IMPB data outputs vary widely; localities paused.

**Education** — Education Counts (MoE) Schools Directory API (nightly), ECE Directory API; rolls/leavers/attendance/qualifications (annual + termly, EQI replaced decile 2023 — series break); NZQA NCEA stats; **ERO review reports have no bulk-download API — scraping ~2,500 schools required**; TEC.

**Economy** — Stats NZ ADE (SDMX API; replaced NZ.Stat retired Sept 2024); Stats NZ Infoshare (legacy, winding down); RBNZ (XLSX scrape; no API); Treasury HYEFU/BEFU/Budget; MBIE; NZIER, Motu (replication packages, CC-BY where possible), BERL, Sense Partners, Infometrics. ProdComm archive at Treasury frozen Feb 2024.

**Governance** — DIA `localcouncils.govt.nz` + CKAN datasets; OAG audit reports (annual local-govt audit results, no machine-readable opinion API); LGNZ; Local Government Commission; Ombudsman; Electoral Commission (booth + electorate, triennial + ad-hoc returns); Companies/Charities registers (APIs); Hansard XML + legislation.govt.nz (Crown copyright, CC-BY for legislation under NZGOAL since 2014); Public Service Commission Kiwis Count.

**Climate adaptation** — He Pou a Rangi Climate Change Commission (annual emissions reduction monitoring; 5-yearly assessments; first budget-period evaluation due 2027); MfE GHG Inventory + Interactive Emissions Tracker (annual April); MfE National Adaptation Plan + Climate Risk Assessment (NCRA every 6 yrs); Earth Sciences NZ (GeoNet CC-BY 4.0, CliFlo CC-BY-NC — flag); EPA ETS register (quarterly); Manaaki Whenua LCDB/S-Map. **Critical gap:** no national aggregator for council-level climate adaptation plans.

### Iwi data and Māori data sovereignty

This is non-negotiable architecture, not an afterthought. The framework that must shape ingestion design:

- **Te Mana Raraunga (TMR)** — Māori Data Sovereignty Network. Six principles: rangatiratanga, whakapapa, whanaungatanga, kotahitanga, manaakitanga, kaitiakitanga.
- **Te Kāhui Raraunga (TKR)** — operationalises the Mana Ōrite agreement between the Data Iwi Leaders Group and Stats NZ. Runs **Te Whata** (`tewhata.io`), the iwi-led Census platform (first used for Census 2023). Its **Māori Data Governance Model (2023)** is designed for use across the public service.
- **CARE Principles** (Collective benefit, Authority to control, Responsibility, Ethics) from the Global Indigenous Data Alliance — complement FAIR; reference both.
- **Ngā Tikanga Paihere** — Stats NZ framework (2020) for culturally appropriate IDI use.

**Practical implications.** Don't store Māori data on offshore cloud (sovereignty position). Engage relevant iwi authority before any iwi-disaggregated analysis. For Te Whata data, follow Te Kāhui Raraunga's terms (governance, not just licensing). The schema should treat iwi/rohe as a parallel `Region` taxonomy, not a sub-type of TA — they don't align geographically.

### Licensing quick reference

NZGOAL recommends CC-BY 4.0 as default for non-copyright open content. Most LINZ, Stats NZ, MfE, NZTA, MoH, MoE, OAG output is CC-BY 4.0. **Flags:** NIWA CliFlo is **CC-BY-NC** (commercial licence required for commercial use); some Koordinates layers carry the restrictive Koordinates Commercial Geodata License v1; RBNZ and EA have permissive-but-bespoke terms.

### Known gaps to plan around

The ten gaps that will shape the migration:

1. **No national zoning/district-plan aggregator** (67 TAs, heterogeneous schemas).
2. **No national GTFS aggregator** (each region; NZTA's national set incomplete).
3. **KiwiRail** publishes almost no open data.
4. **NZ Police** has no JSON API; CSVs only.
5. **ERO review reports** require scraping (no bulk API).
6. **RBNZ** XLSX-scrape only.
7. **DHB → Health NZ transition** introduces 2022 series breaks across health data; localities paused mid-2024.
8. **Sale-price truth data** is paywalled (CoreLogic, REINZ, QV).
9. **Climate adaptation at locality level** is fragmented; no national aggregator.
10. **Council financial/asset data heterogeneity** — no standardised national local-government data warehouse (OAG flagged repeatedly).

Plus three watch-items: ANZSOC offence classification revised 1 Jul 2025 (justice-data series break); Census 2018 quality issues persist into Census 2023 release rolling through 2026; regional-council restructuring proposals (Feb 2026) could disrupt LAWA continuity.

---

## 4. Authoring strategy and content scaling

### The volume problem, sized

Auckland today: ~5 themes drafted, ~10 in progress, ~hundreds of claims. A reasonable v1 NZ scope: 11 themes × 16 regions × ~30 claims per (theme, region) = **~5,300 regional claims**, plus ~500 national-pattern claims and ~200 cross-region comparison claims. At an authoring rate of 5 claims per Claude Code session-hour (with verification), that's ~1,200 hours. **This is not feasible solo without leverage.**

The leverage strategy has four components: **template-driven generation, AI-co-authored region-by-region with human review, structured framing primitives that prevent drift, and aggressive deferral of low-value regions.**

### Template-driven generation, after Scholia/mySociety

The Wikidata Scholia model — **one rendering template per entity type, generated from queries over the graph** — is the only pattern that lets a solo operator credibly cover 16 regions. Adapt it:

- For each `(Region, Theme)` pair, generate the *page skeleton* from the graph (overview, key indicators, problems, drivers, camps, IBIS-structured contested issues).
- Authoring is then **filling in narrative connective tissue**, not writing structure from scratch. Auckland's existing prose becomes the highest-fidelity regional template; other regions inherit the structure but not the framings.
- The AI's job per region is to (a) gather region-specific evidence, (b) verify or refute that the Auckland framing applies, (c) draft narrative around the structured nodes, (d) flag patterns that don't fit.

### Avoiding "same Problem framed 16 different ways"

The drift mechanism is real: ask Claude to "draft Wellington housing affordability" 16 times and you get 16 sibling essays with subtly different definitions of the problem. Three structural countermeasures:

1. **Problems are nodes, not prose.** A `Problem` like "missing-middle housing supply gap" is one canonical node with a canonical statement. Region pages render that node and add region-specific evidence. The Problem statement is edited *once* across all 16 regions.
2. **Methodology registry.** Every quantitative comparison routes through a named, versioned `Methodology` (e.g., `demographia_median_multiple_v2024`). The lint enforces shared methodology for cross-region claims; this prevents "Auckland uses median-multiple but Wellington uses price-to-rent ratio" drift.
3. **IBIS structure for contested topics.** Per Conklin's primer, Positions are stated neutrally; rhetoric lives only in Arguments. The schema enforces this typing (an `IbisNode` of kind `position` cannot contain a value-loaded verb; lint regex). When the same Issue arises in Auckland and Northland, the Positions are shared; the Arguments differ by evidence and intensity.

### Neutrality across politically diverse regions

Auckland-vs-West Coast-vs-Northland have very different political and economic profiles. The neutrality risk is that AI co-authoring will silently absorb the dominant political framing of source material (Auckland-centric urbanist literature; West Coast extractive-industry advocacy; Northland Treaty-settlement framings). Three patterns:

- **IBIS arguments must cite their source's political positioning** (`source.tier` plus a new optional `source.framing_note`). A reader can see "this Pro is from a free-market think-tank; this Con is from a tenants' union."
- **Mandate that every Issue have at least one Position from each broad camp identified for that theme.** If only one Position exists, lint warns; this prevents single-perspective drift even when the AI doesn't naturally surface alternatives.
- **Per-theme neutrality reviews** — a periodic pass (semi-annual) where the orchestrator agent reads cross-region IBIS structures and flags themes where Positions are unbalanced. This is a structural counterpart to peer review.

### Auckland as template without overfitting

The risk is well-founded: Auckland's housing dynamics (large city, port-constrained, Pacific-immigration-shaped, Unitary Plan upzoning experiment) are *not* a template for Westport. Two safeguards:

- **Pattern abstraction precedes regional rollout.** Before drafting Wellington housing, abstract Auckland's housing analysis into Patterns (which are explicitly cross-regional generalisations) separated from Auckland-specific Instances. The pattern "speculative land-banking on the urban fringe" generalises; the instance "the South Auckland 2010s greenfield lag" does not.
- **First-region-after-Auckland is deliberately distant.** Pick Westland, Gisborne, or Southland as the second region drafted, *not* Wellington. Distant cases force the schema and the patterns to bend; nearby cases let Auckland framings sail through unchallenged. Wellington and Christchurch can come later when the patterns have been stress-tested.

### Te Tiriti o Waitangi and iwi-specific governance

Treaty-related governance varies by rohe (Tāmaki Makaurau Collective, Ngāi Tahu, Tūhoe, Waikato-Tainui all have very different post-settlement structures and powers). The schema treatment:

- **Iwi/rohe is a parallel taxonomy** to regions, not a sub-type. A claim about Ngāi Tahu's Mahaanui co-management role has `region_scope: [canterbury]` AND `iwi_scope: [ngai_tahu]`.
- **Per-rohe Treaty governance is its own theme branch**, distinct from the national Te Tiriti analysis. The national theme covers Treaty principles, settlement framework, and pan-iwi institutions; per-rohe pages cover local co-governance arrangements.
- **Engagement, not just licensing.** For any iwi-disaggregated analysis, follow Te Kāhui Raraunga's Mana Ōrite framework. Te Whata data is governed, not merely licensed; respect that. Document engagement steps in `migration_log.yaml` for accountability.

### Sequenced authoring order

After Auckland (existing): one distant region (Westland or Gisborne), then a small/rural counter-case (Southland or Northland), then Wellington (urban comparator), then sequenced rollout of remaining 12 regions in pairs. National rollups draft *after* enough regional evidence exists to ground them — typically after 4–6 regions are complete. Premature national framings risk crystallising as Auckland-plus-extras.

---

## 5. Tooling changes

This section is the working tooling spec for Claude Code.

### 5a. Lint system: claim-citation enforcement at national scale

The recommended architecture is a three-layer lint pipeline.

**Layer 1 — pre-commit (fast, deterministic, on staged YAML):**
- Pydantic schema validation on every changed file.
- "Every claim has ≥1 source" — guaranteed by `min_length=1` on `Claim.sources`.
- yaml-lint formatting.
- Region-vocabulary check (`region_scope` values must be in canonical enum).
- `methodology_tag` referenced must exist in the methodology registry.
- Banned weasel-word regex (`many experts`, `some say`, `studies show`).
- IBIS Position-text neutrality regex (no value-loaded verbs in Position nodes).

**Layer 2 — CI on every PR (slower OK):**
- `lychee` link-check on all source URLs with `--archive wayback` to suggest replacements.
- DOI/URL metadata fetch (Manubot-style); cache resolved metadata in `data/.cache/`.
- Cross-region methodology consistency check via DuckDB SQL: every comparison claim with ≥2 regions must have backing claims for each region with the same `methodology_tag`.
- Staleness check: `claim.as_of < today - threshold(theme)` raises a warning.
- Comparison-claim rule: if statement matches `\b(more|less|higher|lower|cheaper|costlier) than\b` AND `region_scope.length ≥ 2`, all regions need same methodology.
- National-scope coherence: claims using national-keywords (`NZ`, `New Zealand`, `OECD`, `national`, `nationwide`) must include `nz` in `region_scope`.
- SAFE-style LLM verifier on changed claims only (see 5c).

**Layer 3 — nightly cron (GitHub Actions schedule):**
- Re-archive all source URLs to Wayback (`https://web.archive.org/save/{url}`).
- Detect underlying-dataset version bumps (HTTP HEAD / ETag / content-hash); file GitHub issue if changed.
- Surface stale-but-published claims as auto-tagged issues sorted by age (Wikipedia's TagDater pattern).

**New rules specifically for region-tagged content:**

```python
# Rule R1: National wording must include nz tag
if any(k in txt for k in NATIONAL_KEYWORDS) and Region.NZ not in claim.region_scope:
    err("national wording but no `nz` in region_scope")

# Rule R2: Region named in text must be in scope
for r in Region:
    if r.value in txt.lower() and r not in claim.region_scope:
        err(f"mentions {r.value} but not in region_scope")

# Rule R3: Comparison claims need ≥2 regions and shared methodology
if any(re.search(p, txt) for p in COMPARISON_PATTERNS):
    if len(claim.region_scope) < 2:
        err("comparison claim needs ≥2 regions in scope")
    if not claim.methodology_tag:
        err("comparison claim must have methodology_tag")
    for region in claim.region_scope:
        if not has_backing(region, claim.theme, claim.methodology_tag):
            err(f"no backing claim for {region} with methodology={claim.methodology_tag}")

# Rule R4: Theme-specific freshness
THEME_WINDOWS = {"housing": 365, "elections": 1825, "demographics": 1825,
                 "transport": 730, "health": 365, "economy": 180}
if (today - claim.as_of).days > THEME_WINDOWS.get(claim.theme, 730):
    warn(f"as_of {claim.as_of} older than freshness window")
```

**Stale-citation handling.** Cite-by-version, not cite-by-URL. A `Source` carries both `retrieved` (when *we* accessed) and a `methodology_tag` (e.g., `statsnz_hlfs_2024q4`). When Stats NZ publishes 2025q1, don't mutate — create `src_statsnz_hlfs_2025q1` and a new `Claim` with `supersedes: <old_id>`. The lint flags any *published* claim where a successor methodology_tag exists. This is the OurWorldInData pattern adapted: never mutate, always supersede; the graph keeps history. Wayback archival happens on every source ingestion; the `archived_url` field is populated from the Save Page Now API response.

### 5b. Typed entity graph: storage, schema migration, validation

**Recommended stack: Pydantic v2 models → YAML files in Git, with a derived in-memory NetworkX graph + DuckDB index built at load time.**

Reasoning:

1. **Git diffs are source of truth.** Every claim, entity, relationship lives as YAML in a directory tree (`data/regions/auckland/entities/*.yaml`, `data/claims/*.yaml`). PRs become reviewable; Claude Code reads/writes YAML directly without DB drivers.
2. **Pydantic = single schema doing five jobs:** load-time validation, auto-generated JSON Schema (for Claude's system prompts — "here is the exact schema you must produce"), custom field validators (cross-field rules like region_scope-vs-statement consistency), IDE LSP support, Datasette schema for read-only data exploration.
3. **Build a derived graph at site-build time.** Load all YAML into `networkx.MultiDiGraph` for traversal queries; load the same data into `:memory:` DuckDB for analytic SQL (DuckDB reads JSON natively).
4. **Avoid Kùzu** — the embedded graph DB Luke might have considered was acquired by Apple in October 2025 and the open-source repo archived. Avoid for new projects.
5. **Avoid Neo4j Community** — server-process operational overhead with no value at this scale.
6. **Skip RDF/SHACL as source of truth** but keep JSON-LD as an *export* format for future Wikidata/Schema.org interop.

Schema sketch (Pydantic v2):

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import date

class Region(str, Enum):
    NZ = "nz"
    AUCKLAND = "auckland"
    # ... 16 regions + nz
    # Iwi taxonomy parallel:
class Iwi(str, Enum):
    NGAI_TAHU = "ngai_tahu"
    # ...

class SourceTier(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"

class Source(BaseModel):
    id: str = Field(pattern=r"^src_[a-z0-9_]+$")
    title: str
    publisher: str
    url: HttpUrl
    retrieved: date
    archived_url: HttpUrl | None = None
    tier: SourceTier
    methodology_tag: str | None = None
    framing_note: str | None = None  # source's political positioning if relevant
    geo_granularity: list[str] = []  # ["national","regional","ta","sa2"]

class Claim(BaseModel):
    id: str = Field(pattern=r"^c_[a-z0-9_]+$")
    statement: str
    region_scope: list[Region] = Field(min_length=1)
    iwi_scope: list[Iwi] = []
    theme: str
    sources: list[str] = Field(min_length=1)
    methodology_tag: str | None = None
    quantitative: bool = False
    figure: float | None = None
    unit: str | None = None
    as_of: date
    supersedes: str | None = None
    invokes_pattern: list[str] = []

    @field_validator("statement")
    def no_weasel_words(cls, v):
        banned = ["many experts", "some say", "studies show"]
        for b in banned:
            if b in v.lower():
                raise ValueError(f"Weasel phrase: {b}")
        return v

class Pattern(BaseModel):
    id: str
    name: str
    statement: str
    manifests_in: list[Region]
    evidence: list[str]  # claim ids
    theme: str

class IbisNode(BaseModel):
    id: str
    kind: Literal["issue","position","argument_pro","argument_con"]
    text: str
    region_scope: list[Region]
    parent: str | None = None
    sources: list[str] = []
```

YAML example:

```yaml
# data/claims/auckland_house_price_income.yaml
id: c_akl_house_price_income_2024
statement: "In 2024 Auckland's median house price was 8.4× the median household income."
region_scope: [auckland]
theme: housing
sources: [src_demographia_2024, src_statsnz_hlfs_2024q4]
methodology_tag: demographia_median_multiple_v2024
quantitative: true
figure: 8.4
unit: ratio
as_of: 2024-12-31
```

**Schema migration approach (backwards compat with existing Auckland data).** A one-time migration script:

1. Read all current Auckland YAML / data structures.
2. For each claim: add `region_scope: [auckland]`; if missing, populate `methodology_tag: legacy_v0` and flag with a `data:legacy_methodology` GitHub label.
3. Validate every migrated claim against the new Pydantic schema; failures get hand-review issues.
4. Write a `migration_log.yaml` recording every transformation.
5. Run lint Layers 1+2 and triage failures over a focused 1–2 week window before merging to main.

The migration is reversible (Git revert) until the YAML is committed to main; treat it as a feature branch with full test coverage.

**Validation tooling.** Pydantic's `model_json_schema()` exports JSON Schema; this becomes a system-prompt artifact for Claude AND a JSON Schema validator usable from any language. `mypy --strict` on the schema module catches drift. CI runs the full lint pipeline on every PR. Tests in `pytest` cover known-good and known-bad YAML fixtures.

### 5c. AI agent workflow

The dominant constraint: 16 regions of context don't fit in one Claude session. Don't try. Decompose along **theme** rather than region.

**Recommended structure: per-theme orchestrator with per-task region subagents.**

```
.claude/agents/
  theme-housing.md          (orchestrator, owns methodology + cross-region patterns)
  theme-transport.md
  ... (11 themes)
  region-researcher.md      (subagent, fetches/quotes sources for one region)
  claim-extractor.md        (subagent, prose → Claim YAML)
  ibis-structurer.md        (subagent, contested topics → IBIS)
  verifier.md               (subagent, NLI cite-matching + SAFE-style)
  pattern-abstractor.md     (subagent, instances → Pattern abstraction)

CLAUDE.md (root):
  - schema reference: data/schema.py
  - canonical region + iwi enums
  - methodology_tag registry
  - "every numeric claim cites primary source" rule
  - banned weasel phrases
  - IBIS neutrality grammar
```

Per-theme orchestrator owns the methodology and centralises framings. Region-specialist subagents are *spawned* per task; they inherit theme CLAUDE.md plus region-specific data files and don't need to know other regions exist. Cross-region comparisons are a separate orchestrator task that loads only comparison-relevant claims (typically dozens, not thousands) — fits in one window.

Why this beats "one Claude session per region": 16 region-CLAUDE.md files quickly drift out of sync; theme-orchestrators centralise methodology. Theme-orchestration is the canonical Claude Code orchestrator-worker pattern — each subagent has its own 200k window, isolated working memory, no persistent memory between invocations, max ~10 concurrent.

**Workflow command (e.g., `/draft-region housing wellington`):**

1. Theme orchestrator loads `data/schema.py`, `data/themes/housing/methodology.md`, all existing housing claims (national + Auckland + any prior regions).
2. Spawns region-researcher: "Find primary sources for Wellington housing 2024. Stats NZ, Wellington City Council, MBIE. Return JSON list of `Source` candidates."
3. Spawns claim-extractor with the sources: produces draft `Claim` YAML files. Pydantic validates inline → fail loop if invalid.
4. Spawns ibis-structurer for contested issues identified.
5. Orchestrator runs `python -m build.lint_claims data/regions/wellington/housing/` (deterministic, layer 1).
6. Spawns verifier (using a *different* model — see below) which runs NLI cite-matching on every new claim.
7. Orchestrator commits to a feature branch; PR triggers CI Layer 2 (lychee, methodology consistency, SAFE-style web verifier on changed claims).

**Independent per-claim verification (the missing step Luke flagged).** The drafter must NOT also verify. Two-tier architecture:

```
PR opened → CI: changed-claims diff → for each new/edited claim:
  1. (different model) atomicize claim.statement → atomic facts
  2. for each cited source URL:
     - fetch + cache HTML (trafilatura)
     - chunk + embed locally (sentence-transformers/all-MiniLM-L6-v2)
     - NLI-score (claim, top-k chunks) using cross-encoder/nli-deberta-v3-base
  3. if max NLI score < τ: post PR comment "UNSUPPORTED";
     add `verification:failed` label
  4. SAFE-style fallback: if cite-match fails, run web search verifier
```

All free / local on Luke's RTX 3070. Embedding (`all-MiniLM-L6-v2`) and NLI (`nli-deberta-v3-base`) both fit in 8GB easily. Atomicization via Sonnet API or local Qwen2.5-7B (free, on the 3070). Source fetching via `trafilatura`. Web search fallback via SearxNG self-hosted or `duckduckgo-search`. Pipeline structure: copy OpenFactCheck's three-class skeleton (`claim_processor`, `retriever`, `verifier`).

**Cross-LLM verification matters.** Use a different model for verification than for drafting (Claude drafts → Qwen or GPT verifies). The "different model = different priors" property; SAFE works because the verifier is anchored on retrieved evidence, not the drafter's framing.

**Neutrality prompt scaffold (IBIS):**

```
Decompose this regional issue into IBIS structure:
1. State the Issue as a neutral question (no value-loaded words).
2. List 2-4 Positions. Each Position must be a neutral statement
   that a reasonable advocate would accept as their own view.
3. For each Position, give 2-3 Pros and 2-3 Cons. Each must cite a
   source. Mark which Pros/Cons appeal to evidence vs. values.
4. Do NOT recommend a Position. The reader decides.
```

Force structurally rather than via vibes prompting.

### 5d. Static site generation: Flask/Jinja changes

**Recommendation: stay on Flask + Frozen-Flask.** The data layer is Python (Pydantic, networkx, DuckDB); migration cost to Astro / 11ty / mkdocs is real and not justified at projected scale. Re-evaluate at 10k+ pages or if hot-reload pain dominates authoring.

**Sizing.** 16 regions × 11 themes × ~5 sub-pages ≈ ~880 base pages, plus comparison and entity pages: ~1500–3000 pages. Frozen-Flask handles this fine (each page is a single WSGI request); the bottleneck is Python data-loading code, not Frozen-Flask.

**Required Flask/Jinja changes:**

1. **Routes parameterised by region.** Add `<region>` URL converter constrained to the canonical 16+`nz` enum. Existing `/research/auckland/...` routes become `/research/<region>/...` with Auckland as one valid value.
2. **Region-aware base template.** Add a region switcher and a theme switcher as Jinja macros in `templates/_base.html`. Switchers are pre-rendered (no JS-SPA), each <a href> goes to the equivalent path under a different region.
3. **Faceted search via Pagefind.** Add `data-pagefind-filter="region:<region>"` and `data-pagefind-filter="theme:<theme>"` attributes to page templates. Pagefind's chunked index + BM25 ranking handles filter facets natively. Lunr loads the whole index upfront; for ~3000 pages this gets large. Pagefind is unmaintained-Lunr's strict successor in 2026.
4. **Cross-region comparison rendering.** Generate Vega-Lite specs from the typed graph at build time using `repeat`/`facet` operators for small multiples across regions. JSON specs are diff-friendly and AI-editable. For archival figures, also commit matplotlib-rendered SVG alongside.
5. **Datasette over the build-time SQLite.** Deploy `civic.lukesimmonsnz.kiwi/data/` running Datasette (or Datasette-Lite WASM, entirely client-side) on top of the SQLite/DuckDB built from YAML. Free SQL-explorable interface to your typed graph; major credibility win for a research project; matches Simon Willison's "Baked Data pattern."
6. **Versioned archives.** A scheduled GitHub Actions job (quarterly) copies the live build to `/archives/YYYY-QN/` as immutable snapshots; "How to cite" footer directs scholars to the archive URL.
7. **Incremental builds (optional, Phase 5).** Hash all input YAML files; cache rendered HTML keyed by `(template_name, input_hashes)`. ~50 lines of Python; defer until builds exceed 5 min.

**Deployment.** GitHub Pages via a custom Actions workflow (`actions/configure-pages` → `python build.py` → `actions/upload-pages-artifact` → `actions/deploy-pages`) — bypasses the legacy 10-min Jekyll limit. Cloudflare Pages is the upgrade path with unlimited bandwidth on free tier and 500 builds/month if Luke ever exceeds GitHub's soft caps (1GB repo, 100GB bandwidth/month). **Avoid Vercel** — Hobby plan prohibits commercial use; civic-research status is ambiguous and the licensing risk isn't worth it.

---

## 6. International precedents

Ten projects offer transferable architecture. Three are top-recommended. The full list is summarised below; the synthesis follows.

| Project | Scope | Architecture | Why relevant |
|---|---|---|---|
| **Our World in Data** | Global, all topics | Unified static site; MySQL DB + JSON chart configs + Markdown essays → "Baker" pipeline → static HTML | The only precedent that fully integrates typed structured data + source-alongside-data + long-form essays + static site + multi-decade durability mindset |
| **Stanford Encyclopedia of Philosophy** | Global topic domain | Unified site with **quarterly archived editions**; live entry mutable, archived snapshots immutable + citable | Solves the "living document + citable fixed reference" paradox — directly applicable to the 100-year horizon |
| **Australia State of the Environment + EcoAssets** | National + regional, 12 themes | Common DPSIR (Drivers–Pressures–State–Impact–Response) structure across all chapters; quinquennial cycle since 1996 | Multi-theme civic reporting with uniform structure and assessment-confidence ratings; EcoAssets retrofitting structured data pipelines |
| **Centre for Cities (UK)** | 63 cities × 17 indicators | Unified site; consistent city-by-city template; annual flagship + themed sub-tools | Closest in granularity to Luke's 16-region target |
| **ONS Subnational Indicators Explorer (UK)** | 12 ITL1 + lower geographies | Geography-first user journey; 41 indicators standardised; prototypes on GitHub for reuse | Geography-as-facet UX; open prototype habit |
| **Wikidata + Scholia** | Global, all entities | Typed triples → SPARQL → on-the-fly "aspect" page templates | Proves typed-entity graph can *generate* public-facing pages automatically |
| **mySociety (Alaveteli, FixMyStreet, Pombola)** | 40+ countries | Reusable code kernels + per-jurisdiction templates + open-source federation | Per-entity page template + open-source kernel → solo-scalable federation |
| **Centre for Liveable Cities (Singapore)** | Singapore + comparative | Liveability Framework (3 outcomes × 3 systems + enablers) applied across Urban Systems Studies books | Framework-as-typed-ontology forces consistency |
| **Singapore Centre for Strategic Futures** | Whole-of-government | Scenario Planning Plus 6-phase methodology; 20–30 yr horizons | Long-horizon institutional methodology |
| **Finland Committee for the Future** | National parliament | Cross-party, multi-generational; 30+ years operational since 1993 | Proof-of-concept that long-horizon institutions endure |

### Three patterns to adopt directly

**Pattern 1 — OWID's "data + source + narrative baked into one static build."** Single-source-of-truth database where every indicator carries source metadata, plus Markdown essays, plus chart configs, all flowing through one build pipeline to static HTML. Luke's stack should mirror this. Critically, OWID's own retrospective regret — that Grapher is hard to reuse outside OWID — is a warning: design the graph to be portable (RDF-or-JSON-LD-exportable), don't over-couple to one visualisation tool.

**Pattern 2 — SEP's quarterly versioned archive.** The 100-year horizon requires "living document + stable citation." SEP's quarterly archive solves this. Implement `/archives/YYYY-QN/` immutable snapshots with citation footer pointing scholars there. Solo-automatable via a scheduled CI job.

**Pattern 3 — mySociety federation × Scholia "aspect" templates.** The scaling challenge is "Auckland → 16 regions." mySociety proves reusable per-jurisdiction templates from an open-source kernel let one team serve many regions. Combined with Scholia's "one rendering template per entity type, generated from queries over the graph," every region's profile page is generated, not hand-authored. Adding the 17th region (or a TA-level page) costs near-zero. Open-sourcing the template (per ONS ESS habit) invites external contributors.

### Cross-cutting lessons and warnings

- **Source-with-data, not source-as-footnote.** OWID, Wikidata, ONS ESS all store citations as first-class structured fields. Luke's lint-enforced citation discipline is in excellent company.
- **Structured frameworks force cross-region comparability where narrative drifts** — DPSIR (Australia SoE) and the Liveability Framework (Singapore CLC) both work this way.
- **Open-sourcing the code disproportionately benefits durability** (OWID, mySociety, ONS).
- **Watch-outs from precedent failures:** tightly-coupled viz layers (OWID's regret); federation coordination overhead (Poplus and EveryPolitician went dormant); half-done data-to-graph retrofits (Australia SoE took 25 years to start retrofitting); narrow foresight horizons despite ambitious framing (Koskimaa & Raunio's critique of Finland's CF).
- **AI-co-authoring is genuinely novel** — none of the established precedents use AI in primary authoring. ONS has "robo-journalism" prototypes; vTaiwan 2024 uses LLMs to summarise deliberation. Luke is at the frontier here; expect to set precedent rather than follow it.

---

## 7. Sequenced migration plan

The plan is six phases over ~12 months of part-time work. Phase 0 is preparation; Phases 1–5 are sequenced; effort estimates assume ~10 hrs/week solo with Claude Code leverage.

### Phase 0 — Preparation (1–2 weeks, ~20 hours)

Goal: lock the architectural decisions before touching code.

- Read this document end-to-end with Claude Code; resolve any disagreements.
- Decide: stay on Flask (recommended) vs migrate. Document decision in `ARCHITECTURE.md`.
- Decide: Pydantic+YAML+Git (recommended) vs alternative graph store. Document.
- Set up `ARCHITECTURE.md`, `SCHEMA.md`, `METHODOLOGY_REGISTRY.md`, `CLAUDE.md` updates as living documents.
- Create a feature branch `national-migration` for all Phase 1–3 work.

Dependencies: none. Risk: low. Output: written architectural decisions.

### Phase 1 — Schema and lint foundations (3–4 weeks, ~40 hours)

Goal: stand up the new typed graph and lint pipeline without touching content.

- Implement `schema.py` (Pydantic v2 models per section 5b).
- Implement loader (`load_graph.py`) producing both NetworkX and DuckDB views.
- Implement Layer 1 pre-commit lint (deterministic Python).
- Implement Layer 2 CI lint (lychee, methodology consistency, staleness, comparison rules).
- Add `methodology_registry.yaml` with initial entries for current Auckland metrics.
- Set up Wayback Save Page Now archival hook on source ingestion.
- Write Pydantic JSON Schema export and add to Claude system-prompt artifacts.
- Tests: `pytest` fixtures for known-good/known-bad YAML.

Dependencies: Phase 0. Risk: medium (Pydantic edge cases). Output: schema and lint infrastructure ready, no content migrated yet.

### Phase 2 — Auckland data migration (2–3 weeks, ~25 hours)

Goal: migrate existing Auckland content into the new schema without breaking the live site.

- Write one-time migration script that reads current Auckland data and produces new YAML.
- Backfill `region_scope: [auckland]` on every claim; placeholder `legacy_v0` methodology where unknown.
- Run Layer 1+2 lint; triage failures over 1–2 weeks; fix or label.
- Diff the rendered Auckland site before/after migration — the public output should be byte-identical or trivially close.
- Merge migration to main; the Auckland site is now running on the new schema.
- Write `migration_log.yaml` capturing every transformation.

Dependencies: Phase 1. Risk: medium (data discovery). Output: Auckland fully on new schema; site unchanged externally; lint passes.

### Phase 3 — Site infrastructure for facets (2–3 weeks, ~25 hours)

Goal: extend Flask/Jinja to support region facets without yet adding new regions.

- Refactor routes to `<region>` URL converter; existing Auckland URLs preserve via redirect or canonical path.
- Add region/theme switchers in `_base.html` (initially showing Auckland + "national" + "more regions coming").
- Integrate Pagefind with `data-pagefind-filter` attributes.
- Generate first Vega-Lite small-multiples spec from the graph (even with 1 region, validates the build pipeline).
- Stand up Datasette read-only over the build-time SQLite at `/data/`.
- Set up quarterly archive cron in GitHub Actions (Phase 3 produces first archive).
- Update GitHub Pages deploy to use custom Actions workflow if not already.

Dependencies: Phase 2. Risk: low–medium (template surgery). Output: Auckland site visually similar but architecturally ready for siblings; faceted search works; Datasette live; first quarterly archive exists.

### Phase 4 — First three new regions + AI workflow stabilisation (4–6 weeks, ~60 hours)

Goal: prove the multi-region authoring loop works end-to-end with a deliberately diverse trio.

- Choose Westland (or Gisborne) as the *first* new region — distant from Auckland, forces schema and patterns to bend.
- Then choose Southland (or Northland) — small/rural counter-case.
- Then Wellington — urban comparator.
- Set up `.claude/agents/` with theme orchestrators and per-task subagents per section 5c.
- Implement independent verifier subagent (NLI cite-matching on RTX 3070; cross-LLM via Qwen2.5-7B local).
- For each new region: draft 2–3 themes (start with housing, then transport, then one local-priority theme).
- Abstract Auckland-specific framings into Patterns where appropriate; keep Instances region-specific.
- First cross-region comparison page published (e.g., housing affordability across Auckland/Wellington/Westland).
- Engage with Te Kāhui Raraunga / iwi authorities before publishing any iwi-disaggregated analyses.
- Public soft-launch of multi-region site (still mostly Auckland content, three new regions partial).

Dependencies: Phase 3. Risk: high (content quality, neutrality drift, time pressure). Output: 4 regions published, AI workflow proven, verifier in production, lint catching real issues.

### Phase 5 — Remaining regions + national rollups (4–6 months, ~150 hours)

Goal: complete NZ-wide v1 coverage.

- Sequence remaining 12 regions in pairs (~2 weeks per pair for 2–3 themes each).
- Suggested order: Bay of Plenty + Waikato; Canterbury + Otago; Hawke's Bay + Manawatū-Whanganui; Northland + Tasman; Marlborough + Nelson; Taranaki + Gisborne. Plus catch-up on Auckland-equivalent depth for early regions.
- After 6 regions complete, begin national rollup pages — patterns and national instruments now have enough regional grounding to avoid Auckland-projection.
- Per-rohe Treaty governance content for regions with significant settlement frameworks (Tāmaki Makaurau, Waikato-Tainui, Ngāi Tahu, Tūhoe, Te Tau Ihu, etc.).
- Cross-region small-multiples charts for every theme.
- IBIS-structured contested issues built out for housing, climate adaptation, governance, health.
- Per-theme neutrality reviews (semi-annual cadence begins).
- Second quarterly archive published.

Dependencies: Phase 4. Risk: high (content drift, methodology drift, time). Output: NZ-wide v1 with all 16 regions + national, cross-region comparisons, IBIS depth on contested issues.

### Phase 6 — Hardening and durability (ongoing, ~40 hours initial then maintenance)

Goal: lock in the durability properties for the long horizon.

- Incremental builds if build time exceeds 5 min.
- Open-source the schema and templates publicly (per ONS ESS / mySociety habit).
- Publish the typed graph as JSON-LD export for Wikidata-style interop.
- DOI minting for archived editions (Zenodo free tier).
- External fact-checking review cycle (invite peer feedback via Issues).
- Migrate to Cloudflare Pages if/when GitHub Pages soft-caps are hit.
- Document the methodology in a single `METHODOLOGY.md` page citable as a meta-source.

Dependencies: Phase 5 (most parts). Risk: low. Output: project is durable, citable, contributable, and open.

### Total effort estimate

**~320 hours** part-time over **~12 months** at 10 hrs/week with Claude Code leverage. The bottleneck is Phase 5 (regional content authoring volume); leverage the AI workflow aggressively and accept that v1 won't have Auckland-equivalent depth in every region — that's a Phase 7+ problem.

### Critical path and dependency graph

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
              ↓         ↓          ↓        ↓
         schema/     migration   facets   AI workflow
         lint        of Auck     UX       proven
```

Phases 1, 2, 3 are sequential (each depends on the prior). Phase 4 can begin partial work as soon as Phase 3 is in late stages. Phase 5 strictly follows Phase 4. Phase 6 work can begin in parallel with late Phase 5.

### Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Schema thrash mid-Phase 5 | Medium | Stress-test schema in Phase 4 with diverse regions before committing; reserve a `schema_v2` migration window in Phase 6 |
| Content drift across 16 regions | High | IBIS structural typing; methodology registry; per-theme orchestrator; semi-annual neutrality reviews |
| AI verifier produces too many false positives | Medium | NLI threshold τ tunable; manual override label; track precision/recall on a labeled set |
| Te Tiriti / iwi engagement gap | Medium | Engage TKR before any iwi-disaggregated analysis; document engagement in migration_log; treat iwi taxonomy as parallel |
| Regional-council restructure (gov't 2026 proposal) | Low–Medium | Schema is region-tagged not region-structural; LAWA continuity is the main exposure; mitigate by archiving LAWA snapshots quarterly |
| ProdComm-style disestablishments break source links | Medium | Always archive to Wayback on ingest; supersede rather than mutate |
| Solo burnout | High | Aggressive scope discipline (10–15 indicators per region in v1, not 50); accept "good enough" for low-priority regions; treat Phase 5 as iterative |
| Verifier compute on RTX 3070 too slow | Low | NLI on 8GB is comfortable; if needed, run verifier nightly batch instead of per-PR |

---

## Appendix A — Model routing and session decomposition

Token economy is a first-order concern for a solo-operator project at this scope. The plan as drafted in §5c assumed uniform Opus usage for orchestration; that is correct for *coordination* but wrong for the ~80% of subagent calls that are mechanical. This appendix specifies the routing discipline and a session-decomposition pattern that keeps Opus scarce, Sonnet dominant in drafting, Haiku dominant in extraction, and Opus reserved for final verification of produced data.

### A.1 The routing principle

For each task, choose the smallest model that passes the quality bar. With Haiku : Sonnet : Opus output pricing roughly in a 1 : 12 : 60 ratio, tier mismatch is a 5–60× cost multiplier. On Luke's Claude Premium subscription the binding constraint is quota rather than per-token cost, but the ratio still applies: Opus burns quota ~5× faster than Sonnet on equivalent tasks; Haiku barely touches quota.

The workflow inverts from "Opus everywhere by default" to **Haiku-first, Sonnet for judgement, Opus for verification and rare synthesis**.

### A.2 Task → tier mapping

| Task | Load | Tier | Rationale |
|---|---|---|---|
| Schema validation / lint rule execution | None | **No model** | Pydantic + regex; zero tokens |
| YAML/Markdown formatting checks | None | **No model** | yamllint, prettier |
| Source metadata extraction (title, author, date from HTML) | Low, structured | **Haiku** | Pattern extraction, not reasoning |
| Claim atomicization (statement → atomic facts) | Low–medium | **Haiku** | SAFE paper shows this works at small-model scale |
| Prose → Claim YAML conversion | Low | **Haiku** | Mechanical transformation with Pydantic validation loop |
| NLI cite-matching (claim vs retrieved chunk) | None | **Local `nli-deberta-v3-base`** | Free, RTX 3070, purpose-built |
| Embedding generation for retrieval | None | **Local `all-MiniLM-L6-v2`** | Free, local |
| Banned-phrase / weasel-word detection | None | **Regex** | Deterministic |
| IBIS structural typing check | None | **Regex + Pydantic** | Grammar rules |
| Region-tag consistency check | None | **DuckDB SQL** | Joins over graph |
| Wayback archival re-check | None | **HTTP HEAD** | No model |
| Region-researcher: finding + quoting sources | Medium | **Sonnet** | Balance of search, citation discipline, domain parsing |
| YAML → prose narrative drafting | Medium | **Sonnet** | Quality matters; Haiku drifts over long narrative |
| IBIS structurer (contested issues → Positions + Args) | Medium | **Sonnet** | Judgement required, regex alone insufficient |
| Independent verifier subagent (drafter ≠ verifier) | Medium | **Local Qwen2.5-7B** or **Haiku** | Cross-LLM property matters more than tier |
| Cross-region pattern abstraction | High | **Opus** | Genuine synthesis; rare task |
| Neutrality review across regions (semi-annual) | High | **Opus** | Editorial judgement at whole-project scope |
| Methodology registry authoring | High | **Opus or human** | Canonical definitions; affects everything downstream |
| Final data-correctness verification (see A.5) | High | **Opus** | The one place Opus is non-negotiable |

### A.3 Subagent frontmatter (`.claude/agents/*.md`)

Every subagent specifies its model explicitly. Claude Code does not auto-route; the routing lives in these files.

```yaml
# .claude/agents/claim-extractor.md
---
name: claim-extractor
model: claude-haiku-4-5
description: Convert prose passages into validated Claim YAML.
tools: Read, Write, Bash
---
You take prose input and emit one or more Claim YAML records
conforming to schema.py. Every claim must cite a primary source.
Validate your output by running `python -m build.lint_claim <file>`
before returning. If validation fails, fix and retry up to 3 times.
Escalate to Sonnet only if 3 retries fail.
```

```yaml
# .claude/agents/region-researcher.md
---
name: region-researcher
model: claude-sonnet-4-6
---
# ...
```

```yaml
# .claude/agents/theme-housing.md
---
name: theme-housing
model: claude-opus-4-7
---
# Orchestrator. Rare, high-value coordination.
```

**Haiku drift mitigation.** Haiku 4.5 occasionally produces malformed YAML on long claim lists. The claim-extractor template bakes in a Pydantic-validate retry loop (3 retries); on third failure, escalate the specific claim to Sonnet. In practice ~95% of extractions succeed at Haiku; the 5% escalation cost is negligible.

### A.4 Session decomposition

Splitting work across multiple sessions is a first-class cost optimisation, not a workaround. Three reasons:

1. **Context accumulation = linear cost inflation.** A single session drafting all of Wellington housing accumulates ~80k tokens of context by turn 20; every subsequent turn pays for all of it. Fresh sessions restart the cost clock.
2. **Task-type homogeneity allows tier pinning.** A session that does only claim-extraction can pin Haiku; a session that does only orchestration can pin Opus. Mixed sessions force the highest tier used in the session across all turns.
3. **Failure isolation.** A corrupted context (hallucination propagating, schema misremembered) in one session doesn't poison the next region.

**Recommended session structure per region-theme:**

```
Session 1 — Research (Sonnet, ~1–2 hours)
  Input: region, theme, existing methodology registry, schema
  Output: source_candidates.yaml (list of Source records),
          raw_extracts.md (quoted passages per source)

Session 2 — Extraction (Haiku, ~30 min, potentially parallel)
  Input: source_candidates.yaml, raw_extracts.md, schema
  Output: draft_claims/*.yaml (one file per claim)
  Behaviour: loop with Pydantic validation; escalate to Sonnet on retry-fail

Session 3 — IBIS structuring, if theme is contested (Sonnet, ~45 min)
  Input: draft_claims/, raw_extracts.md
  Output: ibis/<theme>_<region>.yaml

Session 4 — Verification (local Qwen or Haiku via API, batch, ~15 min)
  Input: draft_claims/*.yaml
  Output: verification_report.yaml (NLI scores per claim)
  No LLM cost if run locally.

Session 5 — Lint + PR (no model, CI)
  Deterministic. Produces PR with labels.

Session 6 — Opus verification pass (Opus, ~20 min, gate before merge)
  Input: PR diff, verification_report.yaml
  Output: approval or change-requests on specific claims
  The sole Opus call per region-theme.
```

Per region-theme this is approximately **1 Opus call, 2 Sonnet sessions, 1 Haiku session, 1 local session**. Compared to the naïve "do it all in one Opus session" baseline, this is roughly an **8–12× quota reduction** while *improving* quality because tier-appropriate models beat Opus-on-mechanical-tasks on both cost and reliability (Opus overthinks structured extraction).

**Parallelism.** Sessions 2 (extraction) and 4 (verification) can run in parallel across multiple regions once Session 1 outputs exist. A batch of 4 regions at Session-2 stage is ~2 hours wall-clock using parallel Claude Code subagent spawns, not 8.

### A.5 Opus as the data-correctness gate

Opus is held back for one specific purpose: **verifying that produced data is correct before it enters main**. This is the single non-negotiable Opus call in the workflow. It runs against the PR diff, not against the full corpus.

The gate prompt (schematic):

```
You are reviewing a PR that adds claims to the Aotearoa research graph.

For each claim in the diff:
1. Read the claim statement and its cited sources.
2. For each citation, verify the source actually supports the claim.
   Fetch the source URL if needed. The verifier subagent (Session 4)
   has pre-scored cite-matching — use its report as a starting point
   but form your own judgement.
3. Check methodology_tag is consistent across compared regions for
   comparison claims.
4. Check region_scope aligns with the statement's geographic language.
5. Check the claim is neutral in framing; flag value-loaded verbs.
6. Flag any claim where you would not stake your own epistemic
   reputation on the citation-claim linkage.

Output: per-claim approve/change-request with specific reasoning.
Do NOT approve claims where you have < 90% confidence.
```

This is the step that closes the "independent per-claim verification" gap Luke explicitly flagged on the project's `agent + luke` header. The drafter is Sonnet or Haiku. The verifier-of-record is Opus. The two models carry different priors; Opus anchored on retrieved evidence is genuinely independent from Sonnet or Haiku having drafted the prose.

**Frequency.** One Opus gate-pass per PR, not per claim. A PR typically bundles one region-theme's worth of claims (10–30). Opus gate call size is bounded by PR diff, not by corpus.

**Escalation rule.** If Opus gate raises change-requests on >20% of claims in a PR, treat as a signal that the drafter (Sonnet/Haiku) had a systemic miscalibration for that theme-region; re-run Session 1 with tightened source-selection constraints rather than patching individual claims.

### A.6 Monthly quota sanity check

Estimate, assuming Phase 5 steady-state at ~2 region-themes per week:

- **8 Opus gate calls/month** (~20 min of Opus thinking each) = low quota spend
- **~16 Sonnet sessions/month** (research + IBIS) = moderate quota spend, dominant
- **~8 Haiku sessions/month** (extraction) = negligible
- **Rare Opus calls** for pattern abstraction, methodology authoring, neutrality reviews = episodic spikes

If monthly quota starts straining, the lever to pull first is **Haiku share of extraction** (currently 40% of calls; push to 60%+ by moving some IBIS work to Haiku with tighter Pydantic schemas). The lever to avoid pulling is the Opus gate — that's where epistemic integrity lives.

### A.7 What *not* to optimise

Some things look like token-waste and aren't:

- **Schema in every subagent's system prompt.** Reloading the Pydantic JSON Schema costs ~2k tokens per call. Do not strip this; schema-less calls drift and the retry cost dwarfs the saving.
- **Methodology registry in theme orchestrator context.** This is the single most important anti-drift artifact; it must be in context for every drafting call.
- **The `agent + luke` audit trail.** Each PR records which model drafted, which verified, which pattern was invoked. This is cheap to write and expensive to reconstruct.

Token optimisation is not context-minimisation; it is **putting the right tokens in front of the right model**.

---

## Conclusion: what this plan actually changes

The migration is dominated by **schema design, not content volume**. Once the typed entity graph treats region as a tag rather than a partition, content scales at near-linear cost per region rather than the quadratic cost of cross-region comparisons in a sibling-projects architecture. The lint pipeline does the heavy lifting on consistency: a methodology registry plus comparison-claim rules prevent the dominant drift mode (same Problem framed 16 different ways). The AI workflow shifts from "drafter and verifier in one session" to "theme orchestrator + region subagents + independent verifier on a different model" — this closes the per-claim verification gap Luke flagged and is the only structurally honest way to ground 5,000+ claims at solo scale.

Three precedent-derived ideas are load-bearing. **OWID's data+source+narrative-in-one-build** keeps citations first-class and the static site durable. **SEP's quarterly archives** give the 100-year horizon its citability without sacrificing the living-document property. **mySociety + Scholia template-driven generation** is what makes 16 regions tractable for one person.

The thing this plan does *not* do is change the values: neutrality, primary-source citation, claim traceability, AI-co-authoring with human oversight. Those properties survive the scale-up because they are encoded in the schema and the lint, not in any individual page or essay. That's the whole point of the typed entity graph: it's the carrier of the project's epistemics into a future where the content surface is too large for any one human to keep in working memory.