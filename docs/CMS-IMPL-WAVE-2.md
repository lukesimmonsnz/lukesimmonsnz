# CMS-IMPL-WAVE-2 — Page tree builder, publish pipeline, media library

**Status:** design artefact — items 5, 7, 8 of `CMS-SPEC.md` §13.
**Predecessor:** `docs/CMS-IMPL-WAVE-1.md` (items 1–3 ratified 2026-05-02).
**Held-back gates:**

- §3.3 strategy-B parser (v2 round-trip MD ↔ YAML).
- §5.2 preview overlay (item 4) — paired with item 6 in wave 3.

**Why this grouping.** Items 5, 7, 8 share one property: they are
downstream of wave 1 and **independent of item 4**. They can be authored
without the preview overlay being in place, which keeps that PI-mastery
gate untouched until the PI elects to take it. Items 9 and 10 are wave 4
on the same independence criterion.

---

## 5. Item 5 — Page tree builder

### 5.1 Role

Produces the JSON consumed by the htmx sidebar. Sole input: the
filesystem under `content/` plus the resolver's URL→`PageRef` mapping
from item 1. Output: a recursive tree.

$$\text{build\_tree} : () \to \text{TreeNode}$$

The tree is the **only** structure the editor uses for navigation;
breadcrumbs, "next/prev" links, and search facets all derive from it.

### 5.2 Output schema

```python
# blueprints/admin/cms/tree.py  (proposed location)

from dataclasses import dataclass

@dataclass(frozen=True)
class TreeNode:
    label:    str          # short display name, e.g. "congestion"
    url:      str          # canonical URL (matches PageRef.url)
    kind:     str          # PageKind.value
    lock:     str          # LockKind.value
    children: tuple["TreeNode", ...] = ()
```

Serialised with `dataclasses.asdict` to JSON for the sidebar consumer.

### 5.3 Tree topology (matches CMS-SPEC §4)

```
root
 ├─ Home                                  (/)
 ├─ About                                 (/davidsimmons/)
 │   ├─ Biography                         (/davidsimmons/biography/)
 │   └─ Citations                         (/davidsimmons/citations/)
 ├─ Blog                                  (/blog/)
 │   ├─ <date> <slug>                     (/blog/<slug>/)
 │   └─ ...
 ├─ Research                              (/research/)
 │   ├─ Methodology                       (/research/methodology/)
 │   ├─ Auckland                          (/research/auckland/)
 │   │   ├─ transport                     (/research/auckland/transport/)
 │   │   │   ├─ congestion                (/research/auckland/transport/congestion/)
 │   │   │   └─ ...
 │   │   └─ ...
 │   ├─ Wellington
 │   ├─ ...                               (15 more regions)
 │   └─ NZ
 │       └─ Pattern: <theme>              (/research/nz/<theme>/)
 └─ Settings                              (/admin/settings/)
     └─ ...
```

### 5.4 Construction algorithm (sketch)

```python
def build_tree() -> TreeNode:
    return TreeNode(
        label="root", url="", kind="", lock="",
        children=(
            _build_home(),
            _build_about(),
            _build_blog(),
            _build_research(),
            _build_settings(),
        ),
    )
```

Each `_build_*` is a thin walk:

- `_build_blog`: enumerate `content/blog/*.md`, sort by frontmatter
  `date:` desc, call `resolve(/blog/<slug>/)` per entry.
- `_build_research`: iterate `REGIONS` in canonical order, recurse into
  `content/<region>/data/problem/<theme>.<slug>.yaml`, group by theme.
- `_build_settings`: enumerate the four settings groups (§7 of
  CMS-SPEC).

The resolver from wave 1 is the single source of truth for `kind` and
`lock` — `_build_*` never duplicates that classification.

### 5.5 Caching strategy — **decision needed**

Two regimes:

| Regime | Implementation | Trade-off |
|---|---|---|
| **(a) Per-request rebuild** | No cache. `build_tree()` runs on every `/admin/` page load. | At ~760 leaves on consumer SSD, walk completes in well under 50 ms. Trivial; no invalidation logic. |
| **(b) Module-level mtime cache** | Cache hash $h_t = \text{sha256}\big(\sorted{(p, \text{mtime}(p))}_{p \in \text{walk}}\big)$; rebuild only if $h_t \neq h_{t-1}$. | Avoids redundant walks under fast typing. Adds a stale-cache failure mode on filesystem clock skew. |

Recommendation: **(a) for v1**. The per-request cost is dominated by
template rendering, not the walk. (b) is a micro-optimisation with a
correctness footgun (clock skew on WSL / network drives) that's not
worth taking on at this stage.

### 5.6 Invariants

1. **Resolver consistency.** $\forall n \in \text{tree}, \text{resolve}(n.\text{url}).\text{kind} = n.\text{kind}$.
2. **Closure.** Every `TreeNode` whose `url` is non-empty resolves to a
   non-null `PageRef` (item 1 invariant 4 implies this).
3. **Order stability.** Sibling order within blog is by `date:` desc,
   within research by canonical region order, within a theme by slug
   ascending. Stable across calls given identical filesystem state.

### 5.7 Filtering surface

The sidebar UI exposes free-text and by-`kind` filtering. These are
**client-side** transforms over the JSON; the server emits the full
tree. At ~760 nodes ≈ ~150 KB JSON, this is well within sensible
payload limits.

### 5.8 Implementation gap

- The `_build_*` walk bodies.
- The hash function in regime (b), iff PI elects to adopt it.
- Sidebar Jinja partial that consumes the JSON (this is item 6 territory
  — wave 3).

---

## 7. Item 7 — Publish pipeline

### 7.1 Role

The single entry point that promotes a draft to published state. Wraps
DASHBOARD-SPEC's `blueprints/admin/save_pipeline.py` for `PROJECTED`
pages; adds `DIRECT_MD` / `HYBRID` / `SETTINGS` handlers.

The pipeline is a fixed sequence; per-kind dispatch happens at the
`materialise` step (7.4).

### 7.2 Compositional structure

$$\text{publish}(p) \;=\; \text{reload} \circ \text{drop\_draft} \circ \text{git\_commit} \circ \text{render} \circ \text{lint} \circ \text{write} \circ \text{materialise} \circ \text{read\_draft}$$

Read right-to-left: read draft → materialise to file content per kind →
atomic write → lint (kind-dependent) → render derived pages
(kind-dependent) → git commit → drop draft row → reload editor with new
base SHA.

### 7.3 Top-level signature

```python
# blueprints/admin/cms/publish.py

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class LintIssue:
    severity: str   # "error" | "warning"
    code:     str
    path:     Path
    message:  str

@dataclass(frozen=True)
class PublishResult:
    ok:            bool
    written:       tuple[Path, ...]
    rendered:      tuple[Path, ...]
    lint_errors:   tuple[LintIssue, ...]
    lint_warnings: tuple[LintIssue, ...]
    commit_sha:    str | None

def publish(page_id: str,
            commit_message: str | None = None) -> PublishResult: ...
```

`ok = True` iff no `lint_errors` AND `git_commit` succeeded.
`lint_warnings` are always non-blocking and informational.

### 7.4 Per-kind dispatch table

| `kind` | `materialise` | `lint` | `render` | `git_commit` |
|---|---|---|---|---|
| `DIRECT_MD` | serialise frontmatter + body to file bytes | nothing | nothing | yes — single file |
| `HYBRID` | per-slot serialise; layout template untouched | nothing | nothing (templates render at request time) | yes — multi-file in one commit |
| `PROJECTED` | YAML graph delta → typed entity files | JSON Schema + `invariants.run_all` | leaf MD via `content/<region>/tools/render.py` | yes — entity files + rendered MD in one commit |
| `SETTINGS` | merge into `instance/site_settings.json` | nothing | nothing | **decision needed (§7.7)** |

### 7.5 Atomic write contract

Step `write` uses the cross-platform atomic-rename pattern:

```python
def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)   # atomic on POSIX and Windows NTFS
```

Multi-file writes in `HYBRID` and `PROJECTED` are NOT transactionally
atomic across files — Python has no portable mechanism for that. The
mitigation is ordering: write all sources first, then run lint. If lint
fails post-write, the corpus is left in a known-inconsistent state and
the publish result reports `lint_errors`; PI handles by editing again.

This is a deliberate weakening — true cross-file atomicity would
require a write-ahead log we don't want to maintain. PI to ratify.

### 7.6 Lint behaviour — **decision needed**

For `PROJECTED` pages only.

| Mode | Behaviour |
|---|---|
| **(a) Hard-block on errors** | Lint errors abort `publish` after `write` (file is on disk). PI must fix and re-publish to clear lint state. Same regime as wave 4* corpus rebuilds. |
| **(b) Soft-block** | Lint errors reported but pipeline continues. Corpus may temporarily violate invariants. |
| **(c) Split — schema hard, invariants soft** | JSON Schema errors hard-block (data shape integrity); `invariants.run_all` errors soft-block (cross-entity warnings reported to PI but do not abort). |

Recommendation: **(c) split**. Justification: JSON Schema errors mean
the YAML is structurally malformed and downstream render will crash;
fail-fast is correct. Invariant errors are semantic ($P3$
source-citation, $P5'$ comparison-claim, etc.) and PI may legitimately
publish work-in-progress that violates them mid-edit. The wave 4*
corpus regime ("0 errors 0 warnings") was a release gate, not an
authoring gate — different audience, different threshold.

### 7.7 Settings persistence — **decision needed**

`SETTINGS` writes to `instance/site_settings.json`, which is in
`.gitignore` (Flask convention; instance/ excluded from version
control). Two regimes:

| Regime | Behaviour |
|---|---|
| **(a) Untracked** | `instance/site_settings.json` stays out of git; settings changes leave no commit history. |
| **(b) Tracked** | Move to `config/site_settings.json`; commit on settings publish. |

Recommendation: **(a) untracked**. Settings include keys (Turnstile,
contact form URL) that may be environment-specific or sensitive; git
history of those is anti-feature. PI overrides via Settings UI are
ephemeral by design — if they need to be permanent, the change goes
into `.env` or a code-level template change.

### 7.8 Git commit semantics

Per CMS-SPEC §0 row 10 (per-page commit ratified):

```
commit message default:
  "cms: publish <page_url>"

editable in toolbar:
  "cms: <PI's freeform message> [<page_url>]"
```

The `[<page_url>]` suffix is auto-appended for grep-ability of CMS
commits in `git log`.

Author identity: `cms@lukesimmonsnz.kiwi` or PI's git identity (PI to
choose; default is the latter so commits are attributable).

### 7.9 Failure modes and the `PublishResult` truth table

| Step that failed | `ok` | `written` | `rendered` | `commit_sha` |
|---|---|---|---|---|
| `read_draft` (no draft) | `False` | `()` | `()` | `None` |
| `materialise` (frontmatter parse error) | `False` | `()` | `()` | `None` |
| `write` (disk full / permissions) | `False` | partial | `()` | `None` |
| `lint` schema error (mode c) | `False` | populated | `()` | `None` |
| `lint` invariant error (mode c) | `True` | populated | populated | populated; warnings in `lint_warnings` |
| `render` failure | `False` | populated | partial | `None` |
| `git_commit` failure (e.g. detached HEAD) | `False` | populated | populated | `None` |
| nominal | `True` | populated | populated | populated |

The editor surfaces `lint_warnings` even when `ok = True` so the PI sees
the soft-block state without surprise.

### 7.10 Reuse of DASHBOARD-SPEC components

Per CMS-SPEC §10:

- `blueprints/admin/save_pipeline.py` — atomic write + JSON Schema
  validate + `invariants.run_all` + git commit. Reused as the
  `PROJECTED` branch of `materialise → lint → render → git_commit`.
- `content/_render/` (or per-region `tools/render.py`) — invoked at the
  `render` step for `PROJECTED`.
- `content/_schema/edges.yaml` + `invariants.py` — invoked at `lint`.

The wrapper code in this wave is essentially a per-kind dispatcher that
delegates to existing machinery.

### 7.11 Invariants

1. **Idempotence on no-op edit.** $\text{publish}(p)$ over a draft
   whose `body` and `frontmatter` are bit-identical to the on-disk
   source is a no-op: no commit, no render, draft row dropped.
2. **Atomic visibility per file.** A reader observing a source file
   during `publish` sees either the pre-publish or post-publish bytes,
   never a torn write (guaranteed by `os.replace`).
3. **Draft lifecycle.** `drop_draft` runs iff the prior steps reach
   `git_commit` OK. On any failure before commit, the draft row
   survives so the PI can retry without retyping.

### 7.12 Implementation gap

- The dispatcher body in `materialise` (per-kind switch).
- The `HYBRID` per-slot serialiser — depends on the slot manifest
  format chosen in wave 1 §1.3.
- The git plumbing (subprocess vs `git`-Python library — PI's call;
  subprocess is one less dependency).
- Author identity choice (§7.8).

---

## 8. Item 8 — Media library

### 8.1 Role

Upload + dedupe + browse + insert. Uploads land in `static/media/`,
metadata in `cms.db.media`, dedupe by SHA-256.

### 8.2 Storage layout

```
static/media/
  ab/
    abcd1234...ef.png            ← original, content-addressed
    abcd1234...ef_thumb.jpg      ← Pillow-generated thumbnail
  cd/
    cdef5678...ab.pdf
  ...
```

The two-character prefix from `sha256[:2]` distributes files across 256
top-level directories — bounds per-directory file count at
$|files| / 256$ for any plausible scale.

### 8.3 Upload flow

```
POST /admin/api/media   (multipart, field "file")
        │
        ▼
[1] read bytes; compute sha256
[2] SELECT id FROM media WHERE sha256 = ?
       └─ if hit: return existing id, url, dimensions   (dedupe)
       └─ if miss: continue
[3] validate mime against whitelist (§8.5)
[4] write original to static/media/<sha[:2]>/<sha>.<ext>
[5] if image: open with Pillow, generate thumbnail
[6] INSERT into media (sha256, filename, mime, width, height,
                       bytes, alt_text=NULL, caption=NULL, uploaded_at)
[7] respond { id, url, thumb_url, width, height, mime, bytes }
```

Failure at any step before [6] requires cleanup of any file written at
[4] or [5] — implementation must use a `try/except` around the whole
sequence.

### 8.4 Pillow processing

```python
def make_thumbnail(src: Path, dst: Path,
                   max_dim: int, quality: int) -> tuple[int, int]: ...
```

`max_dim` and `quality` are PI hyperparameters — `(240, 80)` is a
sensible starting point but the PI sets the trade-off between bandwidth
and visual fidelity. The thumbnail is always JPEG regardless of source
mime (smaller files; transparency in source images is flattened onto
white). PI may amend that policy if a transparent thumbnail is needed
for any UX surface.

### 8.5 MIME whitelist

```python
ALLOWED_MIMES: frozenset[str] = frozenset({
    "image/jpeg", "image/png", "image/webp", "image/gif",
    "application/pdf",
})
```

PDF is included so blog posts can link to research artefacts. SVG is
excluded — SVG is XML and can carry script payloads; allowing it is a
stored-XSS surface that the CMS does not need to take on.

### 8.6 Browse modal

`/admin/media/` returns a JSON list filtered by query string:

```
GET /admin/media/?q=<text>&mime=image%2F*&limit=50&offset=0
```

Filter `q` matches against `filename`, `alt_text`, `caption`. `mime`
supports glob (`image/*`). Results sorted by `uploaded_at DESC`.

### 8.7 Insert into editor

When PI clicks a media item in the browse modal, the editor splices:

```markdown
![<alt_text or filename>](/static/media/<sha[:2]>/<sha>.<ext>)
```

at the cursor. PI to decide whether default insertion uses original or
thumbnail URL — recommendation is **original** with a CSS rule that
caps `max-width: 100%`, since the corpus theme is text-heavy and image
size is rarely the bottleneck.

### 8.8 Metadata editing

Alt text and caption are post-upload editable via a metadata pane in
the browse modal. `UPDATE media SET alt_text = ?, caption = ? WHERE id
= ?`. No history; no draft semantics — metadata changes are direct.

### 8.9 Invariants

1. **Content addressing.** $\text{disk\_path}(m) = \text{static/media/}\,\text{sha256}(m)[:2]\,/\,\text{sha256}(m)\,.\,\text{ext}(m)$.
2. **Dedupe correctness.** $\forall m_1, m_2 \in \text{media},\;
   \text{sha256}(m_1) = \text{sha256}(m_2) \implies m_1.\text{id} = m_2.\text{id}$.
   Enforced by the `UNIQUE` constraint in §2.2 of CMS-SPEC.
3. **Thumbnail derivability.** Every image row has a sibling `*_thumb.jpg`
   on disk. Recovery: a `media_rebuild_thumbnails` admin command that
   walks the table and regenerates missing thumbnails.

### 8.10 Implementation gap

- The upload route handler (`POST /admin/api/media`).
- The browse handler (`GET /admin/media/`).
- The Pillow `make_thumbnail` body — `(max_dim, quality)` are PI-set.
- The `media_rebuild_thumbnails` recovery command (deferrable to wave 5).

---

## 9. Open decisions for PI (wave 2) — **all ratified 2026-05-02 by directive to proceed**

| # | Decision | Ratified |
|---|---|---|
| W2-1 | Page tree caching (§5.5) | **(a)** per-request rebuild |
| W2-2 | Lint behaviour on publish (§7.6) | **(c)** split — JSON Schema hard, invariants soft |
| W2-3 | Settings persistence (§7.7) | **(a)** untracked (`instance/`) |
| W2-4 | Git author identity (§7.8) | PI's git config |
| W2-5 | Default media insert URL (§8.7) | original (`max-width: 100%` via theme) |
| W2-6 | Pillow `(max_dim, quality)` (§8.4) | `(240, 80)` start; PI tunes |

---

## 10. Wave 3 / wave 4 preview

To keep the dependency graph visible:

- **Wave 3** = item 4 (preview overlay, the PI mastery gate) + item 6
  (two-pane editor partials, depends on item 4). The CodeMirror /
  htmx wiring is mechanical; the overlay's request-scoped intercept is
  the load-bearing novelty.

- **Wave 4** = item 9 (settings surfaces) + item 10 (search & replace).
  Both are independent of item 4 — could be scheduled before wave 3 if
  PI prefers — but their UI slots into the wave 3 editor shell, so
  pulling them forward saves no compounding effort.

The §3.3 strategy-B parser remains a v2 work item; it has no place in
wave 1–4.
