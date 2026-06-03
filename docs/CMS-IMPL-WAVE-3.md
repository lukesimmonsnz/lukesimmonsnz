# CMS-IMPL-WAVE-3 — Preview overlay (mastery gate) + two-pane editor partials

**Status:** design artefact — items 4 and 6 of `CMS-SPEC.md` §13.
**Predecessors:** `docs/CMS-IMPL-WAVE-1.md` (items 1–3 ratified 2026-05-02);
`docs/CMS-IMPL-WAVE-2.md` (items 5, 7, 8 ratified 2026-05-02).
**Held-back gate:** §3.3 strategy-B parser remains v2.

**On the conceptual gap.** Item 4 (preview overlay) is the load-bearing
novelty of CMS-SPEC and was named in the original PI directive
(2026-05-02) as a gap to preserve: *"preserving the conceptual gaps
marked at §3.3 strategy-B and §5.2 preview overlay."* This document
discharges item 4 to the level of a **rigorous design contract with
candidate-architecture analysis** but stops short of writing the
implementation. PI completes the chosen candidate.

Item 6 is mechanical wiring (htmx + CodeMirror + partials) and is
treated more concretely.

---

## 4. Item 4 — Preview overlay (PI mastery — implementation gap preserved)

### 4.1 Role

During a preview render, the CMS must show the page **as it would render
if the active draft were published**, *without* writing the draft to
disk and *without* duplicating the production render path.

Without this overlay, the only ways to achieve preview fidelity would be:

1. **Auto-save-then-render:** every keystroke writes to disk and renders.
   Discarded — defeats the draft/publish lifecycle.
2. **Parallel preview pipeline:** a second render path that consumes the
   draft directly. Discarded — violates ratification §11-Q4 (single
   source of truth).

The overlay is what makes Q4 cheap to honour.

### 4.2 Contract (precise)

Let:

- $\mathcal{F}$ — current filesystem state, $\mathcal{F}: \text{Path} \to \text{bytes}$.
- $\mathcal{D}$ — current draft state, $\mathcal{D}: \text{page\_id} \to (\text{body}, \text{frontmatter}, \text{base\_sha}) \cup \{\bot\}$.
- $S(p)$ — the source-paths set for page $p$, equal to $\text{resolve}(p).\text{source\_paths}$ (item 1).
- $M(p, d)$ — the materialised file content from a draft $d$ for page
  $p$. Identity for `DIRECT_MD`; per-slot serialisation for `HYBRID`;
  YAML-graph serialisation for `PROJECTED`. Already specified in
  wave 2 §7.4 dispatch table.
- $R$ — the public render function, $R: \text{Path} \to \text{HTML}$,
  reading $\mathcal{F}$ implicitly via `Path.read_text` / Jinja loaders /
  YAML loaders.

Define the **overlaid filesystem** for preview of page $p$:

$$\mathcal{F}_p^\Omega(q) \;=\; \begin{cases}
  M(p, \mathcal{D}(p))_q & q \in S(p) \;\land\; \mathcal{D}(p) \neq \bot \\
  \mathcal{F}(q) & \text{otherwise}
\end{cases}$$

The overlay $\Omega$ is the runtime mechanism that makes $R$ read from
$\mathcal{F}_p^\Omega$ instead of $\mathcal{F}$ for the duration of one
request, with no persistent change to $\mathcal{F}$.

Correctness obligation:

$$R_\text{preview}(p) \;\equiv\; R\big|_{\mathcal{F} := \mathcal{F}_p^\Omega}(p)$$

i.e. the preview HTML is byte-identical to what production would emit
**if** $M(p, \mathcal{D}(p))$ were written to disk and $R$ run normally.

### 4.3 Subtleties — five specific failure modes

The contract is simple in symbols and intricate in implementation
because $R$ is not a pure function of `Path.read_text`. Five failure
modes the PI must defend against:

#### 4.3.1 Jinja bytecode cache

`flask.Flask.jinja_env` is a `jinja2.Environment` whose default
`cache_size` is non-zero. Compiled templates are cached by template
name. If two consecutive requests render the same template name with
different on-disk bytes, the second request returns the cached compiled
form of the first. Naïve overlay of a `FileSystemLoader.get_source`
method does not invalidate the cache.

Mitigations (PI to elect):

- **(M1) Disable cache for `/admin/preview/*` routes.** Set
  `app.jinja_env.cache = None` inside the preview view, restore on
  teardown. Simplest. Cost: every preview render recompiles templates
  (~ms-scale; negligible for single-PI workload).
- **(M2) Per-request `Environment` clone with a draft-keyed cache
  namespace.** More complex; preserves caching across drafts. Premature
  optimisation for single-PI scale.
- **(M3) Custom loader that reports a non-cacheable `uptodate` thunk**
  (Jinja's loader API allows `(source, filename, uptodate_fn)` returns
  where `uptodate_fn` returning `False` invalidates). Elegant; requires
  understanding Jinja's loader contract.

Recommendation skeleton: M1 for v1; M3 for v2. PI elects.

#### 4.3.2 Werkzeug context-locality

The overlay must be active during the request handler **and** all
nested template renders, **and** must tear down before the next request
— including when the handler raises. The mechanism is
`contextvars.ContextVar` (Python 3.7+) or `flask.g` plus a
`try/finally`:

```python
# blueprints/admin/cms/overlay.py  (proposed location, contract only)

from contextvars import ContextVar
from contextlib import contextmanager

# the overlay is keyed by page_id; absence means no overlay active
_active_overlay: ContextVar["Overlay | None"] = ContextVar(
    "cms_preview_overlay", default=None
)

@contextmanager
def overlay_active(page_id: str):
    """Activate the overlay for the duration of the with-block."""
    ...   # PI fills body
```

The `try/finally` guarantee is non-negotiable: any code path that sets
the `ContextVar` MUST reset it. This is the kind of bug whose only
symptom is preview-leak across requests after an error.

#### 4.3.3 Async render paths

Python's `contextvars` propagate to threads spawned via
`concurrent.futures.ThreadPoolExecutor` only if explicitly captured.
Asyncio tasks inherit `ContextVar`s by default but a task that returns
to the event loop and is resumed in a different request context will
leak.

**v1 mitigation:** keep all preview render paths synchronous. No
threading, no async. Documented constraint, not a code defence — if a
later wave introduces a thread (e.g. for image processing during render),
that wave's design must explicitly handle context propagation.

#### 4.3.4 Per-kind intercept point

The overlay's intercept point is **not** uniform across page kinds.

| Kind | What "draft body" represents | Intercept point |
|---|---|---|
| `DIRECT_MD` | the .md file's bytes | `Path.read_text` of `content/blog/<slug>.md` |
| `HYBRID` | per-slot .md files | `Path.read_text` of each slot file |
| `PROJECTED` (strategy A) | the YAML graph slice | the YAML loader's input — *upstream* of the `render.py` MD generator |
| `SETTINGS` | the JSON merge | not previewable in the same sense; the settings UI uses its own preview |

For `PROJECTED` this is critical: the rendered MD is computed from the
YAML graph by `content/<region>/tools/render.py`. The overlay must not
intercept the on-disk **rendered MD** (that file does not yet exist for
the draft); it must intercept the **YAML read** that feeds the renderer,
then let `render.py` produce fresh MD from the draft YAML.

In practice: each projection in item 1 declares an `intercepts: list[Path]`
field — the set of file paths the overlay should redirect during
preview. The overlay consults this list and maps each path to a virtual
content stream backed by the draft.

#### 4.3.5 Cache invalidation in the typed-graph loaders

Some YAML loaders memoise. The corpus tooling at
`content/<region>/tools/render.py` may cache `theme → graph` lookups
across calls. If the overlay activates mid-process and the loader has
already cached the on-disk YAML, the overlay's redirect is bypassed.

Mitigation: clear the loader cache at overlay activation. `lru_cache`
provides `.cache_clear()`. PI to audit existing loader code and either
expose a `clear_caches()` entry point or arrange the overlay to
construct a fresh loader instance per preview request.

### 4.4 Three candidate implementations (PI elects)

#### Candidate A — Jinja loader subclass (handles `DIRECT_MD` / `HYBRID` cleanly)

```python
class OverlayLoader(FileSystemLoader):
    def get_source(self, environment, template):
        # If a draft active and template path matches, return draft bytes
        # ... PI body
```

**Strengths:** lives entirely inside Jinja's interface; no monkey-patch
of `Path`. Works for templates and template-included MD files (via a
custom `{% include_md %}` tag or pre-render).

**Weaknesses:** doesn't help with `PROJECTED` because the YAML read
happens outside Jinja, in `render.py`.

#### Candidate B — `Path.read_text` context-local intercept

```python
_real_read_text = Path.read_text

def _overlaid_read_text(self, *args, **kwargs):
    overlay = _active_overlay.get()
    if overlay and self in overlay.intercepts:
        return overlay.read(self)
    return _real_read_text(self, *args, **kwargs)

Path.read_text = _overlaid_read_text   # at module import time
```

**Strengths:** uniform across all kinds — every read goes through
`Path.read_text`. One mechanism covers `DIRECT_MD`, `HYBRID`, and the
YAML reads inside `render.py`.

**Weaknesses:** monkey-patching `pathlib` is process-global; affects
all code, not just the editor. False positives possible. Audit
required.

#### Candidate D — explicit `read()` injection at render boundaries

Refactor `render.py` and the slot-loading code to take a `read` callable
as parameter:

```python
def render_leaf(theme: str, slug: str,
                read: Callable[[Path], bytes] = Path.read_bytes) -> str:
    ...
```

The overlay supplies a `read` that consults the draft. Production code
keeps the default.

**Strengths:** no global state; testable; explicit. Architecturally
cleanest.

**Weaknesses:** invasive — every existing read site must be located
and threaded. Touches code outside the CMS module.

### 4.5 PI decision needed (W3-1)

| Option | Coverage | Invasiveness |
|---|---|---|
| **A** (Jinja loader) | DIRECT_MD, HYBRID | low |
| **B** (Path monkey-patch) | all four kinds | medium (process-global) |
| **D** (read injection) | all four kinds | high (refactor) |
| **A + B** layered | all four kinds | low+medium |

Recommendation skeleton: **A for `DIRECT_MD` / `HYBRID`, B narrowly
scoped to `PROJECTED` reads only**. The combination uses each
mechanism where it's cleanest and avoids B's global-monkey-patch
footgun for the cases where A suffices. PI elects.

### 4.6 Test surface

The high-value test is the round-trip:

1. Take a published page $p$ with on-disk source $s_0$.
2. Render normally — capture HTML $h_0$.
3. Open a draft for $p$, type nothing, autosave.
4. Render via preview — assert HTML $h_p = h_0$ byte-for-byte.

If $h_p \neq h_0$ for an empty draft, the overlay is broken (almost
certainly cache-related, §4.3.1).

A second test:

1. Open a draft, modify body to a known string.
2. Preview-render — assert the modified string appears in the output.
3. Read $s_0$ from disk — assert unchanged.

### 4.7 Implementation gap (deliberately preserved)

- The body of `overlay_active` (4.3.2).
- The chosen candidate from 4.5 — and its full implementation.
- The audit / clearing of loader caches (4.3.5).
- The two tests in 4.6.

This is the PI mastery gate. The contract above is exhaustive enough
that the PI can reason about correctness; the implementation choices
are where the conceptual elegance manifests.

---

## 6. Item 6 — Two-pane editor partials

### 6.1 Architectural choice — htmx vs SPA

The CMS-SPEC §2 architecture diagram shows server-rendered partials
with htmx for interactivity. This is the right choice for a single-PI
admin surface — it minimises JavaScript surface, keeps the editor
debug-friendly, and reuses the Flask render path. SPA frameworks would
add ~MB of bundle for marginal UX gain at this scale.

The only client-side JavaScript is:

1. CodeMirror 6 ESM bundle (~200 KB).
2. A small autosave / postMessage shim (~2 KB hand-written).

### 6.2 Layout partials

```
templates/admin/cms/
  base.html                    ← admin layout (sidebar + main)
  _sidebar.html                ← page tree from item 5 JSON
  editor.html                  ← two-pane editor
  _toolbar.html                ← Save / Publish / Discard / Media / ⋯
  _frontmatter.html            ← collapsible YAML editor
  _editor_pane.html            ← CodeMirror mount point + autosave shim
  _preview_pane.html           ← <iframe src="/admin/preview/<page_id>">
  _status_bar.html             ← autosave, base_sha, lint badges
  _conflict_modal.html         ← 3-way merge UI from §3.2 of wave 1
  _media_modal.html            ← grid of media thumbnails
```

The `editor.html` template composes the partials. htmx attributes drive
the autosave / publish / media interactions.

### 6.3 CodeMirror 6 wiring

Single-file ESM bundle pulled at page load from a CDN or vendored to
`static/vendor/codemirror.bundle.js`. **PI to choose** (W3-2): CDN is
zero-effort; vendored is offline-friendly and avoids supply-chain
exposure for the admin surface.

Initialisation skeleton:

```html
<!-- _editor_pane.html -->
<div id="cm-host"></div>
<script type="module">
import {EditorView, basicSetup} from "/static/vendor/codemirror.bundle.js";
import {markdown} from "/static/vendor/codemirror.bundle.js";
// PI fills: extensions list, vim mode toggle, theme

const view = new EditorView({
  doc: {{ draft.body | tojson }},
  extensions: [basicSetup, markdown(), /* PI extensions */],
  parent: document.getElementById("cm-host"),
});

// autosave shim: 2 s debounce → POST /admin/api/draft
let timer = null;
view.dom.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(() => {
    fetch("/admin/api/draft/{{ page_id | urlencode }}", {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ body: view.state.doc.toString() }),
    });
  }, 2000);
});

// preview-refresh shim: 400 ms debounce → postMessage to iframe
let pTimer = null;
view.dom.addEventListener("input", () => {
  clearTimeout(pTimer);
  pTimer = setTimeout(() => {
    document.getElementById("preview-iframe")
            .contentWindow.postMessage({ type: "cms-refresh" }, "*");
  }, 400);
});
</script>
```

The two debounces are **independent**: 2 s autosave (server-bound),
400 ms preview-refresh (client-only postMessage). The iframe's preview
listens for the message and reloads — this drives the overlay (item 4)
each cycle.

### 6.4 Frontmatter pane

The collapsible YAML editor sits above the main MD editor. CodeMirror
with the `yaml` extension. Same ESM bundle.

Collapsed by default; PI clicks to expand. State persists in
`localStorage` under `cms.frontmatter.collapsed.<page_id>`.

### 6.5 Toolbar interactions (htmx)

```html
<!-- _toolbar.html -->
<button hx-put="/admin/api/draft/{{ page_id }}"
        hx-vals='js:{body: editorView.state.doc.toString()}'
        hx-target="#status-bar"
        hx-swap="innerHTML">
  Save draft
</button>

<button hx-post="/admin/api/publish/{{ page_id }}"
        hx-confirm="Publish {{ page_id }} to git?"
        hx-target="#publish-result"
        hx-swap="innerHTML">
  Publish
</button>

<button hx-delete="/admin/api/draft/{{ page_id }}"
        hx-confirm="Discard draft? This cannot be undone."
        hx-target="#status-bar"
        hx-swap="innerHTML">
  Discard
</button>
```

Each interaction is a single htmx round-trip returning HTML for the
target slot. No JSON parsing client-side.

### 6.6 Status bar

```
┌────────────────────────────────────────────────────────────────┐
│ • autosaved 2 s ago    • base sha matches    • lint: 0/0 ✓     │
└────────────────────────────────────────────────────────────────┘
```

Three independent badges. Each has a server-rendered partial endpoint
that htmx polls every 5 s (or refreshes on autosave / publish events).
Lint counts come from `PublishResult.lint_warnings` after a dry-run
lint endpoint (`POST /admin/api/lint/<page_id>` returns lint counts
without writing to disk).

### 6.7 Page tree sidebar

`_sidebar.html` consumes the JSON from item 5 (page tree builder).
Server-side rendering preferred for initial load; htmx for filter /
expand interactions.

```html
<!-- _sidebar.html -->
<input type="search" hx-get="/admin/tree/filter"
       hx-trigger="input changed delay:200ms"
       hx-target="#tree-body" name="q">
<select hx-get="/admin/tree/filter" hx-target="#tree-body" name="kind">
  <option value="">All kinds</option>
  <option value="direct_md">Direct MD</option>
  <option value="hybrid">Hybrid</option>
  <option value="projected">Projected</option>
</select>
<div id="tree-body">
  {% include "admin/cms/_tree_nodes.html" %}
</div>
```

### 6.8 Diff / history surface (deferred to wave 4 if pressed)

The toolbar mentions Diff and History. These are thin views over `git
log -- <file>` and `git diff` and can be deferred without blocking
publish. PI elects whether to include in wave 3 or push to wave 4.

### 6.9 Invariants

1. **No state in URLs.** `page_id` is the only identifier; no draft id
   leaks into the URL. The current draft for a page is implicit.
2. **Idempotent autosave.** Two autosaves in flight for the same page
   produce the same final state; the latter overwrites the former (no
   merge — that's what `base_sha` is for at publish time).
3. **No silent discard.** `Discard` always confirms; tab close after a
   long edit prompts via `beforeunload` (PI to wire — small JS).

### 6.10 Implementation gap

- The Jinja partials' bodies (mechanical).
- The CodeMirror extension list (vim mode, line numbers, theme — PI
  taste).
- The vendored vs CDN CodeMirror bundle (W3-2).
- The htmx lint-poll endpoint and its 5 s polling interval (PI tunes).
- The conflict-modal 3-way merge UI (uses `conflict_triple` from
  wave 1 §3.1; UI library or hand-rolled — PI elects).

---

## 11. Open decisions for PI (wave 3) — **all ratified 2026-05-02 by directive to proceed**

| # | Decision | Ratified |
|---|---|---|
| W3-1 | Preview overlay candidate (§4.5) | **A + B narrowly scoped** — A for `DIRECT_MD`/`HYBRID`, B (Path intercept) for `PROJECTED` YAML reads only |
| W3-2 | CodeMirror bundle (§6.3) | **vendored** (`static/vendor/codemirror.bundle.js`) |
| W3-3 | Diff / history surface (§6.8) | **wave 4** |

---

## 12. Wave 4 preview

- **Item 9** — Settings surfaces: forms per group, JSON exporter to
  `instance/site_settings.json`, `before_request` hook to populate
  `g.site_settings`.
- **Item 10** — Search & replace: extend `blueprints/search.py` to
  scan YAML field values; replace UI with per-match confirmation.
- **Diff / history** (W3-3 → wave 4): thin views over `git log -- <file>`
  and `git diff <sha>...HEAD -- <file>`.

After wave 4: CMS v1 is feature-complete. The §3.3 strategy-B
round-trip parser remains the v2 stretch.
