# CMS-IMPL-WAVE-v2-2 — Visual block editor

Status: design + endpoints scaffolded; UI authoring deferred to a focused
session.
Predecessor: v2-1 parser/serializer (round-trip + locality, tests green
12/12); v2-3 block library Jinja partials + renderer; v3 page slot
promotion (932 editable surfaces).
Mastery surface: NONE — v2-2 is mechanical given v2-1's round-trip
identity. The PI mastery work is already discharged.

---

## 0. Goal

Activate the `Visual` toggle in `/admin/edit/?id=<page>`. In Visual mode
the body MD is parsed to a BlockTree and rendered as a column of
click-editable cells, one per node. Source mode (the existing textarea)
remains the v1 fallback. Toggle is bidirectional — switching modes does
not lose state.

The v2 spec mockup at CMS-SPEC-v2.md §3.5 is the design target. End-to-
end behaviour:

  1. Edit a callout's title via the cell's attr form
  2. Insert a `::section-cta` block via the `+ insert` gutter
  3. Drag-reorder two cells
  4. Switch to Source mode → see the canonical MD
  5. Save → autosave → publish → live page reflects change

## 1. Architecture

```
                  /admin/edit/?id=<page>
                          │
                          ▼
               ┌──────────────────────┐
               │  editor.html (page)  │
               │   ┌─ tab bar ───────┐│
               │   │ Visual / Source ││
               │   └──────┬──────────┘│
               │          │           │
               │ ┌────────┴─────────┐ │
               │ │ Source pane:     │ │
               │ │   <textarea/>    │ │
               │ │   (existing)     │ │
               │ └──────────────────┘ │
               │ ┌──────────────────┐ │
               │ │ Visual pane:     │ │
               │ │   <div id=cells> │ │  ← rendered server-side from
               │ │     ...          │ │     parsed BlockTree
               │ │   </div>         │ │
               │ └──────────────────┘ │
               └──────────────────────┘

State flow on change:
   cell mutate
     → JS updates client tree state
     → POST /admin/api/blocks/serialize/
     → response: new MD body
     → write hidden source textarea
     → autosave timer fires
     → PUT /admin/api/draft/
```

## 2. Server endpoints (already shipped)

Three routes added to `blueprints/admin/cms/blueprint.py` lines 446-509:

| Route | Body / params | Returns |
|---|---|---|
| `POST /admin/api/blocks/parse/` | `{body: "..."}` | `{ok, nodes: [...]}` |
| `POST /admin/api/blocks/serialize/` | `{tree: [...], source: "..."}` | `{ok, body: "..."}` |
| `GET /admin/api/blocks/registry/` | — | `{ok, blocks: {kind: spec, ...}}` |

**SCHEMA RECONCILIATION TASK:** the existing parse endpoint returns
`{ok, nodes: [{type, kind, attrs, body, start, end, level, dirty}, ...]}`.
My session also added `blueprints/admin/cms/blocks/json_adapter.py` with
a different schema (`{type, kind, attrs, body, span: [start, end], level,
dirty}`). The next session must:

  (a) pick one canonical schema (recommend `nodes` + `span: [s, e]` for
      consistency with the AST's SourceSpan dataclass),
  (b) update json_adapter.py and the endpoint to match,
  (c) verify the round-trip serialize endpoint accepts the same shape.

Quick repro:
```
curl -s -XPOST localhost:5050/admin/api/blocks/parse/ \
  -H "Content-Type: application/json" \
  -d '{"body": "::callout{type=warning}\nHi.\n::\n"}'
```

## 3. Visual editor cell contract

Each cell in the visual pane represents one Block or RawSpan node.

```
┌─ cell ──────────────────────────────────────────────────┐
│  [kind badge]   [attr1=value1] [attr2="value 2"]         │
│  ─ toolbar ─────────────────────────────────────────── ─┤
│  + insert above  ↑ up  ↓ down  ⎘ duplicate  × delete    │
│  ────────────────────────────────────────────────────── │
│  body:                                                   │
│    leaf  → <textarea> for raw body string                │
│    container → recursive cell column (nested cards)     │
└──────────────────────────────────────────────────────────┘
```

CSS: classic-preset palette (paper-warm `#fbf8f0`, copper accent
`#c4956a`). Cards `0.5px solid #d9d0bf`, hover state `border-color:
#c4956a`. Active edit state `box-shadow: 0 0 0 2px #c4956a inset`.

## 4. Components to ship

1. **`templates/admin/cms/editor.html` updates**:
   - Add `<div id="visual-pane" hidden>` next to the existing
     `<textarea>` body editor.
   - Mode toggle JS — show/hide the panes; when switching to Visual,
     POST `/api/blocks/parse/` with current body → render cells.
   - Block-insertion gutter at top + between cells.

2. **`static/js/visual-editor.js`** (new file, ~400 lines):
   - `class VisualEditor` — owns tree state.
   - `render()` — builds DOM cells from tree.
   - Per-block toolbar handlers (move, duplicate, delete, insert).
   - On any mutation: serialize → POST → update hidden textarea →
     trigger autosave.

3. **`static/css/visual-editor.css`** (new file, ~150 lines):
   - Cell styling + toolbar + drag-affordance + insertion gutter.

4. **Drag-reorder** — Sortable.js from CDN, OR hand-rolled with HTML5
   drag-and-drop. PI's call.

## 5. Cell rendering algorithm (sketch)

Pure function `render_cell(node, path) -> DOM`. `path` is the index
chain into the tree — used for mutation dispatch.

```js
function renderCell(node, path) {
  if (node.type === 'raw') {
    return cellRaw(node, path);
  }
  // node.type === 'block'
  const spec = REGISTRY[node.kind];
  const card = el('div', { class: 'cell cell-' + node.kind });
  card.append(toolbar(path));
  card.append(badge(node.kind));
  card.append(attrForm(node.attrs, path));
  if (spec.container) {
    const inner = el('div', { class: 'cell-children' });
    node.body.forEach((child, i) => {
      inner.append(insertGutter([...path, i]));
      inner.append(renderCell(child, [...path, i]));
    });
    inner.append(insertGutter([...path, node.body.length]));
    card.append(inner);
  } else {
    card.append(textarea(node.body, path));
  }
  return card;
}
```

Mutation dispatch: every cell action calls `mutate(path, op, payload)`.
The mutator clones the relevant subtree, applies `op`, marks the new
node `dirty=True`, replaces in-place, calls `serializeAndAutosave()`.

## 6. Mode toggle wiring

Toggle button (currently disabled with tooltip) → onClick:
  - If switching to Visual: POST current body to /parse/, replace cells
    with rendered tree, hide textarea.
  - If switching to Source: serialize current tree, write to textarea,
    show textarea, hide cells.

State preservation: switching back-and-forth round-trips through
serialize/parse — guaranteed byte-identical for unmodified content
(v2-1 round-trip identity).

## 7. Verification gate

Wave v2-2 closes when:

  1. `/admin/edit/?id=/blog/2026-04-21-...` opens with Source mode
     active by default; clicking Visual switches the pane and renders
     all paragraphs / headings / lists as cells.
  2. Editing a cell's textarea updates the source textarea byte-
     identically on save (round-trip via serialize endpoint).
  3. Inserting a `::callout` block via the `+ gutter` produces a new
     Source body that, when re-parsed, yields the same tree.
  4. Switching Visual → Source → Visual is a no-op on byte-stable
     content (round-trip identity holds at the editor layer).
  5. Drag-reordering two top-level cells results in a valid serialize.
  6. The body that ships to /api/draft/ on autosave is byte-identical
     whether the PI typed in Source mode or used Visual mode.

## 8. Out of scope for v2-2

  - Inline rich-text within paragraph blocks (V2-10 ratification:
    pass-through; toolbar splices `**...**` at cursor; no DOM rich-text
    engine).
  - Custom block registration UI (V2-3 ratification: hand-edit YAML).
  - Real-time collaborative editing.
  - Undo / redo (browser native suffices; localStorage history is v3+).

## 9. Estimated cost

  - Schema reconciliation in json_adapter.py + endpoint: ~15 min.
  - editor.html updates + mode toggle JS: ~45 min.
  - visual-editor.js + CSS authoring: ~3 hours.
  - Smoke + round-trip verification: ~30 min.

  Total: ~4-5 hours focused. Sonnet-pinned.

## 10. Files touched

```
blueprints/admin/cms/blueprint.py            already added (lines 446-509)
blueprints/admin/cms/blocks/json_adapter.py  already added; reconcile schema
templates/admin/cms/editor.html              add visual pane + toggle JS
static/js/visual-editor.js                   NEW ~400 lines
static/css/visual-editor.css                 NEW ~150 lines
```
