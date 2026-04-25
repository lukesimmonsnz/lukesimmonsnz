# Placeholder status — per-figure data-source audit

Last reviewed: **2026-04-24**. Nine figures are currently referenced from
the three housing subpages. **Two are verified (real data live): the Rural
Urban Boundary map and the NIWA coastal-inundation map on [`land.md`](pages/housing/land.md).**
Seven remain as chart placeholders.
(Three purely-manual figures — REINZ price-vs-consents lag, supply
elasticity, long-run PTI — have been replaced with inline citations in the
page prose. One verified map — volcanic viewshafts — was removed because it
was visually confusing without basemap context.)

This document lists what each remaining figure needs to become real and
whether an open API exists to automate the fetch.

"API" here means: a public HTTP endpoint returning machine-readable data,
no paid subscription. A site that requires free registration + an API key
counts as "API with free key". A PDF or XLSX download via a stable URL
does not count as an API — it's a direct file, still automatable but
fragile.

## Status summary

| Access tier | Count | Figures |
|---|---|---|
| ✅ Real data live | 2 | `sea-level-rise-2100`, `supply-construction-productivity` |
| 🟢 Fully open API, no key | 0 | (all previously-green figures are now live) |
| 🔵 Direct CSV/ZIP download (stable URL) | 4 | `supply-annual-consents`, `supply-consents-by-typology`, `affordability-homeownership-cohort`, `affordability-rent-income-quartile` |
| 🟡 Open API, free key required (optional upgrade) | 1 | `affordability-rent-income-quartile` has a key-gated API path in addition to the no-auth CSV — not needed for the current chart |
| 🟠 Partial / composite | 1 | `affordability-deposit-gap` (derived from other feeds once they land) |
| 🔴 Manual curation only | 1 | `affordability-international-pti` — OECD half automatable via SDMX, Demographia cities remain manual |
| ⚫ Needs reconnaissance | 1 | `sea-level-rise-2100` (NIWA layer hosting unclear) |

*(Three purely-manual figures — REINZ price-vs-consents lag, Saiz/Glaeser
supply elasticity, Demographia long-run PTI — have been removed from the
pages and replaced with inline citations. They are not listed below.)*

## Charts

### 1. `supply-annual-consents` 🔵 direct CSV

- **What it shows:** Annual dwelling consents issued in the Auckland region, long-run.
- **Upstream:** Stats NZ — Building consents issued (monthly release).
- **API:** Stats NZ's old Open Data API closed August 2024. The replacement "Aotearoa Data Explorer API" exists but its public-key access tier is not documented as free + open. In practice: download the monthly CSV ZIP from the latest [Building consents issued release](https://www.stats.govt.nz/information-releases/) — the URL changes each month but the filename pattern is stable. Extract `Building consents by region (Monthly)` → filter `Auckland region` + `New dwellings` → sum to calendar-year.
- **To automate:** a small `statsnz.py` fetcher that scrapes the latest release URL from the information-releases index and pulls the CSV.

### 2. `supply-consents-by-typology` 🔵 direct CSV

- **What it shows:** Auckland consents split by detached / townhouse / apartment.
- **Upstream:** Stats NZ (same CSV bundle as above — dwelling type is a column) + Auckland Council RIMU summaries ([Knowledge Auckland](https://www.knowledgeauckland.org.nz/)) for cross-check.
- **API:** Same as above — no true API, but the Stats NZ monthly CSV has the typology split. Knowledge Auckland publishes RIMU PDFs which would need manual extraction if used.
- **To automate:** same `statsnz.py` fetcher with a different column filter.

### 3. `supply-price-consents-lag` 🔴 manual (price side)

- **What it shows:** Auckland dwelling prices vs consents, annual, illustrating the ~2–4 year lag.
- **Upstream:** REINZ median price (monthly property report) + Stats NZ consents.
- **API:** REINZ is a **commercial data provider**. Their real-time API is paid; the monthly statistics are published as a PDF + XLSX on [reinz.co.nz](https://www.reinz.co.nz/) with no direct CSV URL. Prices can also be derived from the public House Price Index published by RBNZ / Stats NZ in some series.
- **To automate:** not trivially. A `reinz.py` fetcher would need to parse monthly PDFs or XLSX attachments. Alternatively, switch the chart to use RBNZ / QV / Stats NZ price series (lower frequency, less granular, but open).

### 4. `supply-construction-productivity` 🟢 open API

- **What it shows:** NZ labour productivity by sector, rebased to 2000 = 100.
- **Upstream:** Stats NZ productivity statistics, with OECD for cross-country context.
- **API:** [OECD SDMX REST API](https://sdmx.oecd.org/public/rest/data/) — free, no key, returns CSV via `format=csvfilewithlabels`. The productivity dataflow is `DSD_PDB@DF_PDB_LV` under agency `OECD.SDD.TPS`.
- **To automate:** simplest fetcher of the lot. An `oecd.py` module with a generic SDMX helper would unlock this chart and any future OECD-sourced figure.

### 5. `supply-international-elasticity` 🔴 manual (academic)

- **What it shows:** Long-run housing supply elasticity for selected cities.
- **Upstream:** Saiz (2010), Glaeser & Gyourko, OECD housing working papers.
- **API:** None. These are academic estimates published in papers — each city's value is a single transcribed number with a citation.
- **To automate:** not applicable. Maintain as a small hand-curated CSV with a `# source` comment per row pointing to the paper.

### 6. `affordability-pti-over-time` 🔴 manual (Demographia)

- **What it shows:** Auckland median dwelling price ÷ median household income, long-run.
- **Upstream:** Demographia International Housing Affordability Survey (annual, January).
- **API:** None. Demographia publishes the annual survey as a [PDF](http://www.demographia.com/db-dhi-index.pdf). The Auckland PTI value appears in the same summary table each year.
- **To automate:** a `demographia.py` fetcher could parse the PDF, but it's brittle — one table layout change breaks the pipeline. Alternatively, compute PTI from Stats NZ income + QV/REINZ price directly (more work per year, but no third-party dependency).

### 7. `affordability-homeownership-cohort` 🔵 direct CSV

- **What it shows:** Homeownership rate in Auckland by age cohort over 40 years.
- **Upstream:** NZ Census — tenure by age, Auckland region (1986 onwards).
- **API:** Census tabulations are on [Stats NZ Aotearoa Data Explorer](https://explore.data.stats.govt.nz/) — interactive filter UI with a "Download CSV" option. No documented programmatic endpoint. Specific Census datasets sometimes appear on [data.govt.nz](https://catalogue.data.govt.nz/) as direct CSV.
- **To automate:** a `statsnz.py` helper could hit ADE's internal JSON endpoints (documented in their [ADE API user guide](https://www.stats.govt.nz/tools/aotearoa-data-explorer/ade-api-user-guide/)) but the terms may restrict automated use. Safe fallback: manual CSV download, commit, forget.

### 8. `affordability-deposit-gap` 🟠 composite

- **What it shows:** Years of median saving to assemble a 20% deposit.
- **Upstream:** Derived — 20% × median Auckland price ÷ median household net saving.
- **API:** N/A (computed). Needs the `supply-price-consents-lag` price feed + a Stats NZ household saving series.
- **To automate:** once the two input feeds land, this chart's CSV is a one-liner derivation.

### 9. `affordability-rent-income-quartile` 🔵 direct CSV (preferred) / 🟡 API with key (optional)

- **What it shows:** Rent-to-income ratio in Auckland by household income quartile.
- **Upstream:** MBIE rental bond data + Stats NZ household income.
- **API:** Two paths for the rent side:
  - **Preferred:** [Raw rental bond data on data.govt.nz](https://catalogue.data.govt.nz/dataset/rental-bond-data-by-region) — **direct CSV URLs, no auth**. Coarser grain than the API but plenty for quartile analysis at annual frequency.
  - **Optional:** [MBIE Market Rent API](https://portal.api.business.govt.nz/api/market-rent) — free but requires subscription-key signup on the business.govt.nz portal. Worth setting up only if this project ever needs sub-annual frequency or live percentile breakdowns — for the current chart the no-auth CSV is sufficient and saves the key-management overhead.
  - Income side: Stats NZ household income by quartile via Aotearoa Data Explorer (manual download, see figure 7 notes).
- **To automate:** `mbie.py` fetcher pointing at the data.govt.nz CSV URLs + `statsnz.py` for income.

### 10. `affordability-international-pti` 🟡 partial API

- **What it shows:** Price-to-income ratios across major rich-country metropolitan markets.
- **Upstream:** Demographia (same survey as figure 6) + OECD Affordable Housing Database.
- **API:** OECD AHD is available via the same [SDMX REST API](https://sdmx.oecd.org/public/rest/data/) as productivity. Demographia is still PDF-only.
- **To automate:** partly via `oecd.py`; the Demographia-sourced cities remain manual.

## Maps

### 11. `volcanic-cones-viewshafts` ✅ live

- **What it shows:** Locally-significant viewshaft polygons protecting views of 3 Auckland volcanic cones under Unitary Plan D14.
- **Upstream:** Auckland Council Open Data — `Locally_Significant_Volcanic_Viewshafts_Overlay` FeatureServer.
- **API:** ArcGIS Hub public FeatureServer, **no auth**. Already wired up via [`data/maps/volcanic-cones-viewshafts.yaml`](maps/volcanic-cones-viewshafts.yaml).

### 12. `land-use-by-category` 🟢 open API

- **What it shows:** Auckland land-use mosaic.
- **Upstream:** Auckland Council Unitary Plan Base Zone layer.
- **API:** [`Unitary_Plan_Base_Zone` FeatureServer](https://services1.arcgis.com/n4yPwebTjJCmXB6W/arcgis/rest/services/Unitary_Plan_Base_Zone/FeatureServer/0) — no auth. **Caveat: 139,368 polygons** (as of 2026-04-24). A full fetch is feasible but would produce a ~50–100 MB cache and a large SVG; the renderer would need either a bbox filter (inner Auckland isthmus only) or a category aggregation (dissolve polygons by zone type before rendering).
- **To automate:** a map spec analogous to the viewshafts one, with a bbox filter and a category colouring by `ZONE` field. Expect a couple of hours of tuning to get the scale right.

### 13. `sea-level-rise-2100` ⚫ reconnaissance needed

- **What it shows:** Auckland land exposed to higher inundation risk under 2100 sea-level-rise scenarios.
- **Upstream:** NIWA coastal hazard projections for the Auckland region.
- **API:** NIWA publishes some coastal layers via [its OPeNDAP server](https://data.niwa.co.nz/opendap/) and [NZOCR](https://www.niwa.co.nz/climate/nz-ocean-climate-reports). Whether the specific "Auckland coastal inundation under RCP 2.6 / 4.5 / 8.5 at 2100" layer is hosted on a public WFS/FeatureServer is **not confirmed**. Likely path: LINZ Data Service hosts a NIWA-derived layer, which would need the LINZ API key.
- **To automate:** needs a 30-minute reconnaissance session to find the canonical dataset and check its hosting. If it ends up being a one-off PDF/XLSX download, treat it as manual + commit the derived CSV.

## Suggested fetcher build order

Ordered by (ease × coverage):

1. **`acouncil.py`** — extract the FeatureServer logic already in [`render_maps.py`](tools/render_maps.py) into a reusable fetcher module. Unlocks `land-use-by-category` and any future Auckland Council layer.
2. **`oecd.py`** — SDMX CSV, no auth. Unlocks `supply-construction-productivity` and the OECD half of `affordability-international-pti`.
3. **`mbie.py`** — EITHER the key-gated Market Rent API OR the no-auth data.govt.nz CSV. Latter is simpler. Unlocks the rent side of `affordability-rent-income-quartile`.
4. **`statsnz.py`** — hardest but highest coverage. Scrapes the Stats NZ information-releases index for the latest Building Consents CSV + (optionally) calls Aotearoa Data Explorer endpoints for tenure/income. Unlocks figures 1, 2, 7 (partially), and the income half of 9.
5. **`linz.py`** — WFS + API key. Unlocks figure 13 if NIWA's sea-level-rise layer is hosted on LDS. Build last because of the key-management story.
6. **`demographia.py`** — PDF scraper. High-effort, brittle, low coverage. Probably never worth it compared to just transcribing two numbers per year manually.

## Fetcher module signature

Each `tools/fetchers/<name>.py` should expose one or more functions with a
consistent shape:

```python
def fetch(params: dict[str, str]) -> bytes:
    """Return the raw fetched payload (CSV bytes or GeoJSON bytes).

    The spec's `fetcher.params` block is passed in verbatim; the fetcher
    is responsible for mapping those to the upstream query. It must NOT
    read the filesystem or write to it — caching is the renderer's job.
    Raises RuntimeError with a clear message on failure.
    """
```

A spec references a fetcher by dotted name (`fetcher.name: oecd.productivity`),
with the params block as a free-form dict. This keeps specs small and
fetchers testable in isolation.
