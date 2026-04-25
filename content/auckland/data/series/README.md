# Auckland data series

CSV files consumed by the chart renderer. One file per underlying series.

> **See also:** [`../PLACEHOLDER-STATUS.md`](../PLACEHOLDER-STATUS.md) for a
> per-figure audit of upstream sources — which have open APIs, which need a
> free-key signup, and which need manual curation.

## Conventions

- UTF-8, comma-separated, header row mandatory.
- Lines starting with `#` are skipped by the renderer — use them for source
  notes, retrieval dates, or a "this is placeholder data" warning.
- One calendar year per row where the series is annual. Use `year` as the
  x-axis column so specs stay uniform.
- Commit **real downloaded files** rather than scraped or computed-on-the-fly
  data. The point is that a reader can audit the chart back to a Stats NZ
  (or equivalent) CSV committed alongside the render spec.

## What each chart needs

The figures referenced in the existing Auckland housing pages map to the
specs and data series below. `status: placeholder` in the corresponding
chart spec is the signal that real data has not yet been committed, and a
"placeholder data" stamp appears on the rendered SVG.

### Chart figures (need CSV data)

| Chart spec | Series CSV (this directory) | Upstream source |
|---|---|---|
| `supply-annual-consents` | `auckland-annual-consents.csv` | Stats NZ — Building consents issued, monthly by region → aggregate to calendar year for Auckland region |
| `supply-consents-by-typology` | `auckland-consents-by-typology.csv` | Stats NZ / Auckland Council RIMU — consents split by detached / townhouse / apartment |
| `supply-price-consents-lag` | `auckland-price-and-consents.csv` | REINZ (price) + Stats NZ (consents), annual, Auckland region |
| `supply-construction-productivity` | `nz-construction-productivity.csv` | Stats NZ productivity statistics — labour productivity index by industry |
| `supply-international-elasticity` | `international-supply-elasticity.csv` | OECD / Saiz (2010) / Glaeser & Gyourko — approximate long-run supply elasticity |
| `affordability-pti-over-time` | `auckland-pti.csv` | Demographia International Housing Affordability Survey (annual) |
| `affordability-homeownership-cohort` | `auckland-homeownership-by-cohort.csv` | NZ Census (1986+) — tenure by age band, Auckland region |
| `affordability-deposit-gap` | `auckland-deposit-gap.csv` | Derived: 20% of median Auckland dwelling price ÷ median household net saving |
| `affordability-rent-income-quartile` | `auckland-rent-to-income-quartile.csv` | MBIE tenancy bond data + Stats NZ household income by quartile |
| `affordability-international-pti` | `international-pti.csv` | Demographia International Housing Affordability Survey + OECD Affordable Housing Database |

### Map figures (render as placeholder until a GIS export exists)

These three specs use `type: placeholder` so the renderer produces a styled
"figure placeholder" box rather than demanding CSV data. When a real map
SVG exists the renderer gets out of the way — see **Escape hatch for
hand-produced SVGs** below.

| Chart spec | Upstream source |
|---|---|
| `land-use-by-category` | LINZ parcel data + Auckland Council RIMU land-use classifications |
| `sea-level-rise-2100` | NIWA coastal hazard datasets + Auckland region boundary |
| `volcanic-cones-viewshafts` | GNS Science Auckland Volcanic Field + Auckland Council Unitary Plan viewshaft polygons |

## Escape hatch for hand-produced SVGs

The renderer will **not overwrite** an SVG it didn't produce. Two ways to
claim ownership of an output file:

1. **Drop an SVG in, let mtime speak.** Produce the SVG outside the pipeline
   (e.g. QGIS export) and save it to `static/img/auckland/<spec-id>.svg`.
   Because it lacks the pipeline's `data-pipeline=render_charts` signature
   and is newer than every input, the next render run logs
   *"hand-produced SVG newer than inputs (not overwriting)"* and leaves it
   alone.
2. **Set `manual: true` on the spec.** Explicit and permanent. The renderer
   logs *"manual: true (leaving hand-produced SVG alone)"* and never
   regenerates, regardless of mtimes.

The mtime path is good for one-off replacements; `manual: true` is good for
specs you know will always be hand-produced (the three map figures are the
obvious candidates once real maps land).

## Workflow for adding real data

1. Download the raw CSV from the upstream source; note the retrieval URL and
   date in a `#` comment at the top of the file committed here.
2. Keep column names short and ASCII — they are referenced verbatim from the
   chart spec (`x:` and `y[].column`).
3. Change the corresponding chart spec's `status:` from `placeholder` to
   `verified`. That flips the "placeholder data" stamp off the rendered SVG.
4. Running `python content/auckland/tools/render_charts.py` re-renders only
   the specs whose inputs changed (mtime check). The scheduled task
   `lukesimmonsnz-regen-docs` picks this up on its next 15-minute tick.
