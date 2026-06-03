# DASHBOARD-SPEC — in-browser corpus editor

> **SHELVED 2026-05-30.** Partial implementation existed at `blueprints/admin/` and was registered at `/admin/yaml/`. PI assessment: the build never reached a usable state, the previous Claude sessions couldn't repair it, and the cost of finishing it now is higher than the cost of editing YAML files directly with the existing CLI lint pipeline (which was always the fallback per §1). Code moved to `archive/admin-yaml/`. Route deregistered from `app.py`. The CMS at `blueprints/admin/cms/*` is a different system and stays live. See the 2026-05-30 changelog entry for the full rationale.
>
> The spec below is preserved verbatim for reference. **Do not implement against it without first reopening this status header with explicit PI instruction.**

---

**Status:** ratified 2026-05-02. **Shelved 2026-05-30.** (See header.)
**Goal:** self-service web UI for editing the typed-entity corpus
(`content/<region>/data/**/*.yaml` and `content/nz/data/pattern/*.yaml`)
without Claude in the loop.
**Non-goal:** replace the lint-gate / Opus review regime. The dashboard
must surface lint failures, not bypass them.

---

## 0. Ratified decisions (2026-05-02)

These are **frozen**. Do not reopen without explicit PI instruction.

| # | Decision | Reference |
|---|---|---|
| 1 | **Topology**: B — local Flask + git-backed (`pygit2` or `subprocess git`); auto-commit per save; localhost-only. | §2 |
| 2 | **Edge target-type registry**: sidecar `content/_schema/edges.yaml` mapping `(entity_type, field) → target_type`. JSON Schemas remain vendor-neutral. | §4.2, §9.1 |
| 3 | **Render pipeline refactor precedes dashboard.** Collapse 16 sibling `content/<region>/tools/render.py` into single `content/_render/render.py` parameterised by region. Prerequisite work item. | §9.3 |
| 4 | **Lint posture on save**: soft-block. Write proceeds; lint failures surface as banner. Single-PI assumption justifies. | §5 Q1 |
| 5 | **Commit granularity**: per-save commit. Footer button invokes `git rebase -i HEAD~N` for retroactive squash. | §5 Q2 |
| 6 | **Authorship auto-stamping**: `last_verified: <today>` set on every save. `verification_status` dropdown surfaces only when transitioning from `cited_only` → `primary_verified`. Prevents silent overwrite of bulk-stamp regime. | §9.5 |
| 7 | **Pattern editor scope (v1)**: separate `/admin/nz/pattern/` surface; no inline rollup preview in claim editor. Defer until §3-refactor cost is measured. | §9.2 |
| 8 | **Bulk edit deferred** to CLI scripts. Dashboard is per-entity precision tool only. | §9.4 |
| 9 | **Frontend**: htmx + Jinja partials. Zero build step. | §7 |

---

## 1. Problem statement

Corpus state at 2026-04-27:
$$|E| \approx 4{,}100\text{ entities}, \quad |R| = 11\text{ themes}, \quad |\text{Region}| = 16, \quad |\text{Schema}| = 13.$$

Each entity is a YAML file conforming to one of the schemas in
`content/_schema/`. Edits today require:

1. Locate file under `content/<region>/data/<entity_type>/<theme>/<id>.yaml`.
2. Hand-edit YAML.
3. Run `python -m content.<region>.tools.lint`.
4. Run `python -m content._schema.invariants` (`run_all`).
5. Re-render via `content.<region>.tools.render`.
6. Smoke-test affected routes.

The dashboard collapses (1)–(6) into a single browser session.

---

## 2. Architectural choice — RATIFIED: B

Three viable deployment topologies were considered. **B is locked** (§0
row 1). A and C retained for future-reference only.

| Option | Backend | Persistence | Auth surface | Lint pipeline | Notes |
|---|---|---|---|---|---|
| **A. Local-only Flask blueprint** | existing Flask process | direct filesystem write to `content/` | none (localhost) | in-process subprocess to `lint.py` / `invariants.py` | Simplest. Edits live in working tree; commit via existing git. |
| **B. Local Flask + git-backed** | Flask + `pygit2` / `subprocess git` | filesystem + auto-commit per save | none (localhost) | as A | Preserves a per-edit audit trail; reverts trivial. |
| **C. Cloudflare Pages + GitHub API** | static dashboard JS calling GitHub Contents API | commits to repo via PAT | OAuth or PAT in `localStorage` | GitHub Actions runs lint on push; dashboard polls workflow status | Editable from anywhere; introduces network latency and a CI feedback loop. |

**Ratified: B.** Local Flask is already running for preview; auto-commit
per save gives free undo without inventing a journal; no new auth
surface; no GitHub round-trip.

If PI later needs remote editing, A→B→C is monotonic — C reuses B's
schema-driven form layer unchanged.

---

## 3. URL surface

Mounted under `/admin/` (gated by `request.remote_addr in {"127.0.0.1", "::1"}`
per ratified topology B).

```
/admin/                              → dashboard home: region grid, lint summary
/admin/region/<region>/              → theme grid for a region
/admin/region/<region>/<theme>/      → entity table for a (region, theme) pair
/admin/entity/<region>/<type>/<id>/  → schema-driven edit form
/admin/entity/<region>/<type>/<id>/preview   → rendered Markdown / HTML preview
/admin/entity/<region>/<type>/<id>/lint      → JSON lint report (P1–P18 + schema)
/admin/nz/pattern/                   → NZ-wide pattern editor (no region facet)
/admin/search?q=...                  → corpus search (reuses blueprints/search.py index)
/admin/api/save                      → POST: validate → write → invariants → return report
/admin/api/render                    → POST: re-render affected pages
```

---

## 4. Schema-driven form generation

The form layer is a **pure function of the schema files** — no
hand-written form per entity type. This is the heart of the dashboard
and the only non-trivial piece of logic.

### 4.1 Generation rule

For entity type $T$ with JSON Schema $\mathcal{S}_T$, the form
$\mathcal{F}_T$ is constructed by structural recursion on
$\mathcal{S}_T.\text{properties}$:

$$\mathcal{F}_T = \bigoplus_{p \in \text{properties}(\mathcal{S}_T)} \widehat{\phi}(p, \mathcal{S}_T[p])$$

where $\widehat{\phi}$ is the widget-selection functor:

| `type` / shape | Widget |
|---|---|
| `string` with `enum` | `<select>` |
| `string` with `format: date` | date picker |
| `string` (free) | `<input>` or `<textarea>` if `maxLength > 200` |
| `integer` / `number` | numeric input with `minimum` / `maximum` clamp |
| `boolean` | checkbox |
| `array` of refs | repeating row with autocomplete (queries `/admin/api/entities?type=...`) |
| `array` of strings/enums | tag input |
| `object` (nested) | recursive `<fieldset>` |
| `oneOf` / `anyOf` | discriminator dropdown that swaps inner widget |

Required fields surface a `*` marker; `default` populates initial value;
`description` becomes a `<small>` hint.

### 4.2 Reference resolution

Edges in the typed graph (`source_ids[]`, `methodology_tag`,
`evidenced_by[]`, `applies_in[]`, etc.) are typed references. The
autocomplete must:

- Filter by target entity type via the **ratified sidecar registry**
  `content/_schema/edges.yaml` (§0 row 2). Format:
  ```yaml
  # content/_schema/edges.yaml
  claim:
    source_ids:    {target: source,      arity: many, scope: region}
    methodology_tag: {target: methodology, arity: one, scope: union}
    evidenced_by:  {target: [driver, camp, problem], arity: many, scope: region}
  problem:
    drivers:       {target: driver, arity: many, scope: region}
    camps:         {target: camp,   arity: many, scope: region}
    claims:        {target: claim,  arity: many, scope: region}
  # ...
  ```
  The dashboard loads this once at startup; autocomplete dispatches off it.
- Scope the candidate set by region for region-local edges, by NZ-wide
  for Pattern.
- Display `id` + truncated `statement` / `name` for disambiguation.

### 4.3 Methodology tag

`methodology_tag` is the prefixed form `methodology.<slug>_vN` per the
Option C ratification (CLAUDE.md §6 layer 1c). Autocomplete pulls from
`content/_schema/methodology.schema.json`-validated entries enumerated
across regions; prefer a single dropdown sourced from the registry
union, not free-text.

---

## 5. Save pipeline

```
client form submit
    │
    ▼
POST /admin/api/save  { region, type, id, body }
    │
    ▼
[1] JSON Schema validate body against content/_schema/<type>.schema.json
    │   fail → return 422 + errors[]
    ▼
[2] Write YAML to content/<region>/data/<type>/<theme>/<id>.yaml
    │   (atomic: write to .tmp, fsync, rename)
    ▼
[3] Run content/_schema/invariants.py::run_all over the affected region
    │   fail → return 200 with status="lint_failed", errors[], warnings[]
    │           (file is written; PI sees the failure but is not blocked)
    ▼
[4] Re-render content/<region>/tools/render.py for affected entities
    │
    ▼
[5] git add + git commit -m "edit: <region>/<type>/<id>"   ← ratified per-save (§0 row 5)
    │
    ▼
return { status, lint_report, rendered_pages[] }
```

**Ratified posture:** soft-block (§0 row 4) — write proceeds, lint
report surfaces in banner. Per-save commit (§0 row 5) — footer exposes
`git rebase -i HEAD~N` for retroactive squashing.

**Authorship contract (§0 row 6):** step [2] additionally writes
`last_verified: <today>` and preserves `verification_status`
unless the form has explicitly transitioned the field, in which case
the dropdown's value is honoured.

---

## 6. Lint surface

The dashboard exposes three lint depths:

| Depth | Trigger | Scope | Backend call |
|---|---|---|---|
| **L1 — schema** | on every keystroke (debounced 300 ms) | the entity being edited | client-side AJV against `_schema/<type>.schema.json` |
| **L2 — invariants** | on save | the entity's region | `invariants.run_all(region=...)` |
| **L3 — full corpus** | on demand button | all 16 regions + NZ | `invariants.run_all()` |

L1 is the only path that should not call the backend — embed
[`ajv`](https://ajv.js.org/) in the dashboard bundle and fetch the
schema files at page load.

The 18-predicate invariant table (P1–P18) is rendered as a checklist
in the lint panel; each failure links back to the offending entity's
edit page.

---

## 7. UI components (minimum viable)

```
┌─────────────────────────────────────────────────────────┐
│ HEADER:  region picker  |  theme picker  |  search box │
├──────────────┬──────────────────────────────────────────┤
│ LEFT NAV     │ MAIN PANE                                │
│              │                                          │
│ Auckland     │  ┌─ EditForm ──────────────────────┐    │
│  ├ transport │  │ id: ...                          │    │
│  ├ housing   │  │ statement: [textarea]            │    │
│  ├ environ.. │  │ methodology_tag: [autocomplete]  │    │
│  ...         │  │ source_ids: [tag input]          │    │
│              │  │ ...                              │    │
│ Wellington   │  └──────────────────────────────────┘    │
│  ...         │                                          │
│              │  ┌─ LintPanel ─────────────────────┐    │
│ ...          │  │ ✓ schema OK                      │    │
│              │  │ ✗ P5'  (instance pinning)        │    │
│              │  │ ⚠ P17  (rohe coverage)           │    │
│              │  └──────────────────────────────────┘    │
│              │                                          │
│              │  ┌─ Preview ──────────────────────┐    │
│              │  │ <rendered Markdown>              │    │
│              │  └──────────────────────────────────┘    │
└──────────────┴──────────────────────────────────────────┘
FOOTER: corpus status (entities, errors, warnings) | git HEAD sha
```

**Ratified frontend (§0 row 9): htmx + Jinja partials.** Zero build
step, server-rendered, drops into existing Flask pipeline. Alpine and
SPA paths retained as future-reference only:

- htmx + Jinja partials — RATIFIED.
- Alpine.js + Jinja — fallback if htmx form-state diff display
  proves insufficient.
- Vue / Svelte SPA — only if a future PWA / offline mode is required.

---

## 8. Reusable backend pieces already in repo

| Need | Existing module | Notes |
|---|---|---|
| Search index | `blueprints/search.py` | 709 entries, title/summary/body weighting — wire `/admin/search` to its index |
| Region enumeration | `blueprints/region.py` | `RegionBlueprintFactory` knows the region list |
| Render | `content/<region>/tools/render.py` | per-region renderer; needs uniform interface |
| Lint | `content/<region>/tools/lint.py` + `content/_schema/invariants.py` | already returns structured report from `run_all` |
| Schema | `content/_schema/*.schema.json` (13 files) | serve as static assets to the AJV client |

The dashboard introduces **no new validation logic**. It is a thin
HTTP/UI wrapper over functions that already exist and are already
exercised by the gate process.

---

## 9. Resolved design questions (2026-05-02)

All five questions previously open are closed; outcomes folded into §0.
Rationale retained here for audit.

| # | Question | Resolution | §0 row |
|---|---|---|---|
| 9.1 | Edge type registry | Sidecar `content/_schema/edges.yaml` | 2 |
| 9.2 | Pattern editor scope | Separate `/admin/nz/pattern/` surface only; defer inline rollup | 7 |
| 9.3 | Render pipeline uniformity | Refactor to single `content/_render/render.py` first | 3 |
| 9.4 | Bulk edit | Deferred to CLI | 8 |
| 9.5 | Authorship trail | Auto-stamp `last_verified`; conditional `verification_status` dropdown | 6 |

---

## 10. Out of scope for v1

- Pattern rollup re-computation on every claim save (compute on demand
  or via the existing scheduled task).
- DOI minting / Zenodo handshake (Phase 6 stretch).
- Multi-user concurrent editing (single-PI assumption).
- Tracked-changes / review workflow (the gate posture already covers
  this at the corpus level).

---

## 11. Implementation deltas (left to PI)

Dependency-ordered work items. Each gates the next.

| Order | Item | Description |
|---|---|---|
| 1 | **Render refactor** (§0 row 3) | Collapse 16 sibling `render.py` into `content/_render/render.py(region: str, entity_id: str | None = None)`. Smoke against existing 706 rendered pages — diff must be empty. |
| 2 | **Edge registry** (§0 row 2) | Author `content/_schema/edges.yaml` by enumerating ref-typed fields across the 13 schemas. Add a loader + validator (`edges.yaml` itself wants a meta-schema). |
| 3 | **Schema walker** (§4.1) | Implement $\widehat{\phi}$ as a recursive function `schema_to_form(schema, path) -> [FormField]`. Pure; testable in isolation. |
| 4 | **Save pipeline** (§5) | Atomic write (`tempfile.NamedTemporaryFile(dir=...)` + `os.replace`); `pygit2.Repository.create_commit` for [5]. Wrap [3]+[4] in a transaction: failure at [4] does not commit at [5]. |
| 5 | **Blueprint shell** | Routes per §3, gated to localhost. |
| 6 | **Frontend partials** | Jinja templates per §7 layout, htmx-driven. |

Skeleton (sketch only — PI fills in):

```python
# blueprints/admin.py
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def _localhost_only():
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        abort(404)

@admin_bp.route("/")
def home(): ...

@admin_bp.route("/entity/<region>/<type>/<id>/", methods=["GET", "POST"])
def edit_entity(region, type, id): ...

@admin_bp.route("/api/save", methods=["POST"])
def api_save(): ...
```

The conceptual gap is preserved at items 1, 3, and 4 — the validation
contract belongs to the PI.
