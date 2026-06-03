# CMS-IMPL-WAVE-1 — Page resolver, `cms.db` DAO, draft store API

**Status:** design artefact — items 1–3 of `CMS-SPEC.md` §13.
**PI directive (2026-05-02):** *"Begin §13 in dependency order, preserving
the conceptual gaps marked at §3.3 strategy-B and §5.2 preview overlay."*
**Implementation gap regime:** type signatures, invariants, and proof
obligations are stated; PI completes the bodies. Hyperparameter / library
glue choices not pre-determined here are deliberately PI's mastery surface.

This document covers wave 1 (items 1–3). Item 4 (preview overlay) and the
v2 §3.3-strategy-B parser are explicitly held back as PI gates and only
their contracts appear here, not their implementations.

---

## 1. Item 1 — Page resolver

### 1.1 Role in the architecture

The single function the editor consults to load any URL. Pure. No I/O
beyond filesystem stat. Unit-testable in isolation.

$$\text{resolve} : \text{URL} \to \text{PageRef} \cup \{\bot\}$$

Used by: page-tree builder (item 5), preview overlay (item 4), publish
pipeline (item 7), search (item 10).

### 1.2 Type signature (PI to finalise import paths / module placement)

```python
# blueprints/admin/cms/resolver.py  (proposed location)

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Protocol


class PageKind(StrEnum):
    DIRECT_MD   = "direct_md"     # editor sees and writes a .md file verbatim
    HYBRID      = "hybrid"        # template-locked layout + named MD slots
    PROJECTED   = "projected"     # corpus leaf — typed YAML form (strategy A)
    SETTINGS    = "settings"      # JSON-backed config surface


class LockKind(StrEnum):
    EDITABLE       = "editable"
    LAYOUT_LOCKED  = "layout_locked"   # Jinja template — code-level edit only
    NOT_EDITABLE   = "not_editable"    # auto-generated (sitemap, feeds)


class Projection(Protocol):
    """The (load, save) algebra for a page. See §1.4."""
    def load(self, srcs: list[Path]) -> "EditorState": ...
    def save(self, state: "EditorState") -> list["FileWrite"]: ...


@dataclass(frozen=True)
class PageRef:
    url:           str
    kind:          PageKind
    source_paths:  tuple[Path, ...]
    projection:    Projection
    lock:          LockKind
    title:         str
    parent_url:    str | None = None    # for tree construction


def resolve(url: str) -> PageRef | None:
    """Pure dispatch. Returns None for URLs outside the editable surface."""
    ...   # PI fills body per §1.3 truth table
```

The `EditorState` and `FileWrite` types are intentionally left abstract
here; PI defines them per projection. Suggested shape:

```python
@dataclass
class EditorState:
    body:        str                       # the MD or YAML buffer the editor edits
    frontmatter: dict | None = None        # parsed YAML frontmatter (direct_md / hybrid)
    typed:       "TypedGraphSlice | None" = None   # projected-only: schema-typed view
    extras:      dict | None = None        # projection-specific (e.g. slot name)


@dataclass
class FileWrite:
    path:    Path
    content: bytes
    mode:    str = "atomic"                # atomic | append (only "atomic" used in v1)
```

### 1.3 Truth table — URL → `PageRef` shape

This table is the resolver's specification. Rows are pattern-matched in
order; first match wins.

| URL pattern | `kind` | `source_paths` | `lock` | Projection name |
|---|---|---|---|---|
| `/` | `HYBRID` | `templates/main/index.html` | `LAYOUT_LOCKED` | `home_slots` |
| `/davidsimmons/` | `HYBRID` | `templates/davidsimmons/index.html` + slot MDs | `LAYOUT_LOCKED` | `davidsimmons_slots` |
| `/davidsimmons/<slot>/` | `HYBRID` | `content/davidsimmons/<slot>.md` | `EDITABLE` | `slot_md` |
| `/blog/` | `DIRECT_MD` | `content/blog/_index.md` (synthesise if missing) | `EDITABLE` | `blog_index` |
| `/blog/<slug>/` | `DIRECT_MD` | `content/blog/<slug>.md` | `EDITABLE` | `direct_md` |
| `/research/` | `HYBRID` | `templates/research/index.html` + `content/research/methodology.md` | `LAYOUT_LOCKED` | `research_index` |
| `/research/methodology/` | `DIRECT_MD` | `docs/METHODOLOGY.md` | `EDITABLE` | `direct_md` |
| `/research/<region>/` | `HYBRID` | `templates/<region>/index.html` (region indexes are computed) | `LAYOUT_LOCKED` | `region_index` |
| `/research/<region>/<theme>/` | `HYBRID` | `content/<region>/pages/_sections/<theme>.md` (if exists) | `EDITABLE` if file present else `LAYOUT_LOCKED` | `section_md` \| `section_computed` |
| `/research/<region>/<theme>/<slug>/` | `PROJECTED` | `content/<region>/data/problem/<theme>.<slug>.yaml` + transitive (drivers, camps, claims, sources) | `EDITABLE` | `corpus_leaf_form_A` |
| `/research/nz/<theme>/` | `PROJECTED` | `content/nz/data/pattern/<theme>.*.yaml` | `EDITABLE` | `pattern_form_A` |
| `/admin/settings/<group>/` | `SETTINGS` | `instance/site_settings.json` (key prefix `<group>.`) | `EDITABLE` | `settings_form` |
| `/sitemap.xml`, `/blog/feed.atom` | — | — | `NOT_EDITABLE` | (returns `None`) |

Region slug is matched against the canonical 16-region list. **Ratified
2026-05-02 (PI):** hard-coded constant in `resolver.py`:

```python
REGIONS: frozenset[str] = frozenset({
    "auckland", "wellington", "northland", "waikato",
    "bay-of-plenty", "gisborne", "hawkes-bay", "taranaki",
    "manawatu-whanganui", "marlborough", "nelson", "tasman",
    "west-coast", "canterbury", "otago", "southland",
})
```

Justification: 16-region list is frozen per ratified architecture
decision #1 (CLAUDE.md §5); manifest path would require migrating
existing hard-coded registries elsewhere in the app, which is out of
CMS scope.

### 1.4 Projection algebra

A `Projection` is the pair $(\text{load}, \text{save})$ defined for each
page kind. The contract:

- $\text{load}$ is a **total** function over `source_paths` whose files
  exist; partial otherwise (resolver returns `None` first).
- $\text{save}$ is **atomic at file granularity** — either all
  `FileWrite`s in the returned list apply, or none. Implementation uses
  `os.replace` after writing to a sibling tempfile.
- For `DIRECT_MD`: $\text{save}(\text{load}(p)) \equiv \text{noop}(p)$
  modulo trailing-newline normalisation. This is the round-trip test.
- For `PROJECTED` (strategy A): $\text{load}$ reconstructs the typed
  graph slice; $\text{save}$ writes YAML and queues the lint pipeline
  (item 7). The graph slice is *not* canonicalised inside the editor —
  edits preserve field order from disk.

The projection registry is itself a finite map:

$$\Pi = \{(\pi_i, (\text{load}_i, \text{save}_i))\}_{i=1}^{k}$$

with $k \approx 10$ projections enumerated in §1.3 column 5. PI to
finalise the registry struct (a frozen dict keyed by name is sufficient;
no plugin loader needed for v1).

### 1.5 Invariants

For all `PageRef`s returned by `resolve`:

1. **Existence.** Every path in `source_paths` either exists or is
   `synthesise-on-write` (only the `blog_index` projection uses this).
2. **Lock consistency.** `lock = LAYOUT_LOCKED` ⟹ `source_paths`
   contains at least one Jinja template that the projection treats as
   read-only.
3. **Title fidelity.** `title` matches the rendered `<h1>` of the
   published page (best-effort; resolver is allowed to use frontmatter
   `title:` or the filename stem).
4. **Tree closure.** If `parent_url` is non-null, `resolve(parent_url)`
   must return a non-null `PageRef`. Tested at startup over the full
   region × theme × leaf cross-product.

### 1.6 Test surface (PI to author)

The resolver should be exercised by a parametrised pytest suite over a
fixture URL set covering each row of the §1.3 table. A randomised
property test asserting **invariant 4 (tree closure)** for every leaf
URL produced by walking `content/` is the high-value test.

### 1.7 Implementation gap (deliberate)

- The body of `resolve` itself.
- The 10 projection objects' `load`/`save` bodies — each is small (≤ 30
  lines) but the failure modes (UTF-8 encoding, frontmatter quoting,
  YAML round-trip preservation of comments) are where mastery accrues.

---

## 2. Item 2 — `cms.db` schema + DAO

### 2.1 Schema

Schema as published in `CMS-SPEC.md` §2.2. Recapitulated only to fix the
identifier `instance/cms.db` and the gitignore obligation:

- `cms.db` lives at `instance/cms.db` (Flask convention).
- `instance/` is added to `.gitignore` if not already present (PI to
  verify; `git check-ignore -v instance/cms.db` is the diagnostic).
- The schema applies idempotently via `CREATE TABLE IF NOT EXISTS`.

### 2.2 Connection management contract

One SQLite connection per Flask request, attached to `flask.g`:

```python
# blueprints/admin/cms/db.py  (proposed location)
from flask import g, current_app
import sqlite3

def get_cms_db() -> sqlite3.Connection:
    if "cms_db" not in g:
        path = current_app.instance_path + "/cms.db"
        conn = sqlite3.connect(path, isolation_level=None)   # autocommit; explicit BEGIN
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        g.cms_db = conn
    return g.cms_db
```

Teardown registered at app-init time closes the connection.

**Why `isolation_level=None` + explicit BEGIN.** It makes transaction
boundaries visible in code rather than implicit per-statement, which
matters for the draft-store conflict gate (§3) where read-then-write
must be atomic.

**Why WAL.** Concurrent readers (preview overlay, page tree, search)
during a writer (autosave) would otherwise serialise. PI's single-author
scenario rarely hits contention but WAL is a $O(0)$-cost insurance.

### 2.3 Type-safe row dataclasses

```python
# blueprints/admin/cms/dao.py
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DraftRow:
    page_id:     str
    body:        str
    frontmatter: str | None
    base_sha:    str
    updated:     datetime
    by_user:     str | None

@dataclass(frozen=True)
class MediaRow:
    id:          int
    sha256:      str
    filename:    str
    mime:        str
    width:       int | None
    height:      int | None
    bytes:       int
    alt_text:    str | None
    caption:     str | None
    uploaded_at: datetime

@dataclass(frozen=True)
class SettingRow:
    key:   str
    value: str
```

The DAO functions take/return these. No ORM. PI to write the trivial
`row_to_DraftRow(sqlite3.Row) -> DraftRow` adapters.

### 2.4 Migration idempotency

A single `migrate(conn)` function runs at app startup. It applies
`CREATE TABLE IF NOT EXISTS` for the three tables in §2.2 and may
introduce a `schema_version` row in `settings` for future migrations.
v1 schema is `1`; v2 (revisions, locks) increments.

The migration is intentionally **not** managed by Alembic for v1 —
overhead exceeds value at three tables.

### 2.5 Implementation gap

- The DAO function bodies (CRUD over the three tables).
- The teardown registration in `app.py`'s factory.
- The `.gitignore` audit.

---

## 3. Item 3 — Draft store API

### 3.1 Surface

```python
# blueprints/admin/cms/drafts.py

def get_draft(page_id: str) -> DraftRow | None: ...
def put_draft(page_id: str, body: str, frontmatter: str | None,
              base_sha: str, by_user: str | None) -> None: ...
def drop_draft(page_id: str) -> None: ...
def list_dirty() -> list[DraftRow]: ...
def has_conflict(page_id: str) -> bool: ...
def conflict_triple(page_id: str) -> tuple[str, str, str] | None: ...
```

`page_id` is the canonical URL string (e.g. `/blog/foo/`,
`/research/auckland/transport/congestion/`). It is the same identifier
the resolver returns; the editor never converts it back to a path.

### 3.2 Conflict detection contract

Let $f(p)$ be the current on-disk SHA-256 of the canonical source file
for page $p$ (for projected pages, the YAML problem entity), and let
$d(p).\text{base\_sha}$ be the hash recorded when the draft was opened.

$$\text{has\_conflict}(p) \;\;\iff\;\; d(p) \neq \bot \;\land\; f(p) \neq d(p).\text{base\_sha}$$

`conflict_triple` returns $(\text{base}, \text{file\_now}, \text{draft\_now})$
as raw byte buffers; the 3-way merge UI (item 6) consumes it. The DAO
itself emits no merge — it only reports.

For a `HYBRID` page with multiple slot files, `base_sha` is computed
over the concatenation in path-sorted order. This deduplicates to a
single hash but sacrifices per-slot conflict granularity. **Ratified
2026-05-02 (PI):** per-page `base_sha` for v1; per-slot granularity
(compound key `(page_id, slot)`) deferred to v2 schema migration if
real conflicts emerge. HYBRID surface is small (~3 pages) and authored
by the sole PI, so the lower granularity is acceptable.

### 3.3 Autosave semantics

Autosave is **client-side debounced** — the server's `put_draft` is
idempotent and contains no rate-limit logic.

$$\text{autosave\_event}(t) \;:=\; \text{lastKeystroke}(t-2\text{s}) \;\land\; \text{not}\;\text{lastKeystroke}(t-2\text{s},\,t)$$

The 400 ms preview-refresh debounce (§5.2) is a *separate, faster*
debounce on a different channel and does not trigger a draft write.

Server contract for `put_draft`:

1. Open transaction.
2. `INSERT OR REPLACE` into `drafts` keyed by `page_id`.
3. Update `updated = NOW()`.
4. Commit.

`base_sha` is set **only on first put** for a `(page_id, by_user)` pair.
Subsequent puts in the same draft session do not advance it — that's the
whole point of conflict detection. PI to enforce this in the body of
`put_draft` via a read-modify-write under the open transaction.

### 3.4 `base_sha` lifecycle

```
[editor opens page p]
        │
        ▼
   sha = sha256(file(p))
        │
        ▼
   put_draft(p, "", None, base_sha=sha, by_user=PI)   ← row created
        │
        ▼
   [PI types; client autosaves every 2 s]
        │
        ▼
   put_draft(p, body_t, fm_t, base_sha=row.base_sha, by_user=PI)
        │   (server clamps base_sha to existing row's value)
        ▼
   [PI clicks Publish]
        │
        ▼
   if has_conflict(p): show 3-way merge UI; abort publish
   else:                proceed to §8 step 2
```

### 3.5 Invariants

1. **Hash provenance.** Every non-null `drafts.base_sha` equals
   $f_{t_0}(p)$ for some past time $t_0$; in particular, it is never
   user-supplied or client-computed (server reads the file at draft
   open).
2. **Singleton draft per page in v1.** `(page_id)` is the primary key;
   v2 may extend to `(page_id, by_user)` when multi-user lands.
3. **Liveness.** A draft row is removed only by `drop_draft` or by a
   successful publish (item 7). Autosave never deletes.

### 3.6 Implementation gap

- All six function bodies in §3.1.
- The `base_sha` clamp logic in `put_draft` (§3.3 step 2-3).

---

## 4. Items 4–10 — staged downstream of wave 1

### 4.1 Item 4 — preview overlay (CONCEPTUAL GAP, do not implement here)

This is the load-bearing novelty of CMS-SPEC and a PI mastery point.
The contract is recapitulated below for completeness; the implementation
is held back deliberately.

**Contract.** A request-scoped overlay $\Omega$ such that, during a
preview render of page $p$:

$$\text{render\_template}(p) \;\;\text{reads}\;\;
\begin{cases}
  \text{draft}(p).\text{body} & \text{if } d(p) \neq \bot \\
  \text{file}(p) & \text{otherwise}
\end{cases}$$

without modifying the public render path's source code.

**Subtleties (PI to handle).**
1. **Jinja's bytecode cache.** Templates that include `{% include %}`
   or `{% extends %}` will be compiled and cached; the cache key is the
   template name, not the content. Naïve overlay of `Path.read_text`
   inside Jinja's loader will be bypassed by the cache. Solution
   surface: a per-request loader subclass that namespaces cache keys by
   draft id, OR `app.jinja_env.cache = None` inside preview routes.
2. **Werkzeug context-locality.** The overlay must be active during the
   request handler and during all nested template renders, but must
   tear down before the next request — including in the error path.
   `flask.g` plus a `try/finally` around the overlay activation is the
   minimal pattern.
3. **Async render paths.** If any render path uses threads (e.g. for
   image processing), the context-local must be propagated explicitly
   or the render path must be kept synchronous. v1 keeps everything
   sync.
4. **Projected pages.** For corpus leaves, the overlay's "file content"
   is the *rendered* MD, not the raw YAML. The overlay's intercept must
   be applied at the point where `render.py` reads YAML and emits MD —
   not at `Path.read_text` of the YAML file. This is a different layer
   and is part of why item 4 sits AFTER items 1–3: the projection
   algebra is what determines the overlay's intercept point per kind.

**PI gate.** Until item 4 ships, items 6 (editor partials) and 7
(publish pipeline) cannot be tested end-to-end with live preview.
Item 5 (page tree) and item 8 (media) are independent of item 4 and may
be developed in parallel.

### 4.2 Item 5 — page tree builder (mechanical, downstream of item 1)

Walks `content/` plus the region-list manifest, calls `resolve` per URL,
emits JSON consumed by the htmx sidebar. Output schema:

```jsonc
{
  "label": "Auckland",
  "url":   "/research/auckland/",
  "kind":  "hybrid",
  "lock":  "layout_locked",
  "children": [ /* recursive */ ]
}
```

Cache invalidation on filesystem mtime; in-memory only.

### 4.3 Items 6–10 — sketched, not authored in wave 1

| Item | Dependency | One-line note |
|---|---|---|
| 6 — two-pane editor partials | items 1, 5 | Jinja + htmx + CodeMirror 6 ESM. Preview iframe waits on item 4. |
| 7 — publish pipeline | items 1, 3 | Wraps `blueprints/admin/save_pipeline.py` (DASHBOARD-SPEC) for `PROJECTED`; identity for `DIRECT_MD`; slot-fanout for `HYBRID`. |
| 8 — media library | item 2 | Pillow thumbnails; `static/media/<sha[:2]>/<sha>.<ext>` layout. |
| 9 — settings surfaces | item 2 | JSON exporter to `instance/site_settings.json`; `before_request` hook. |
| 10 — search & replace | existing search index | Extend `blueprints/search.py` to scan YAML field values; replace UI requires per-match confirmation. |

---

## 5. The two PI mastery gates (do not erode)

1. **§3.3 strategy-B parser** (v2). The bidirectional MD ↔ YAML
   round-trip with anchor-comment preservation. Proof obligation:
   for $R$ the renderer and $R^{-1}$ the parser,
   $$R(R^{-1}(m')) = m' \quad\text{and}\quad R^{-1}(R(g)) \cong g$$
   up to canonical child ordering. Strategy A's existence is what makes
   it acceptable to defer this.

2. **§5.2 preview overlay** (item 4). The Werkzeug context-local that
   diverts content reads inside `render_template`. Subtle because of
   Jinja's bytecode cache, async paths, and the difference in intercept
   point between direct-MD pages (read YAML/MD file) and projected
   pages (render YAML → MD → template).

These two gates are where the CMS earns its keep as a research
artefact rather than a CRUD app. Wave 1 (items 1–3) is plumbing that
makes them tractable.
