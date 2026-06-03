# CMS-IMPL-WAVE-v2-7 — Menu builder UX

**Status:** design artefact — wave v2-7 of `CMS-SPEC-v2.md` §7.
**PI directive (2026-05-03):** mechanical; independent of v2-1 parser.
**Scope:** replace raw-JSON nav editor with drag-reorder + inline-edit UI.

---

## 1. Current state

Nav is stored in `cms.db.settings` at key `group.nav` as a JSON array:

```json
[
  {"label": "Home",     "url": "/"},
  {"label": "Blog",     "url": "/blog/"},
  {"label": "Research", "url": "/research/", "children": [
    {"label": "Auckland", "url": "/research/auckland/"}
  ]}
]
```

Currently editable only as a raw JSON textarea at `/admin/settings/nav/`.

---

## 2. Data model

```
NavItem = {
  "label":    str,          // display text
  "url":      str,          // href (relative OK)
  "children": [NavItem]     // optional; max depth 2 from top (depth cap = 3)
}
```

**Depth cap:** a top-level item may have children; children may have
grandchildren; grandchildren may NOT have children. Depth ≤ 3 total.
The UI enforces this by hiding the "Add child" control when depth = 3.

---

## 3. UI shape

```
┌─ Navigation ──────────────────────────────────────────────────────────────┐
│  ⠿  Home        /                                        [Edit] [Delete]  │
│  ⠿  Blog        /blog/                                   [Edit] [Delete]  │
│  ⠿  Research    /research/                               [Edit] [Delete]  │
│     ┌────────────────────────────────────────────────────────────────────┐│
│     │  ⠿  Auckland   /research/auckland/                [Edit] [Delete] ││
│     │  [+ Add child]                                                     ││
│     └────────────────────────────────────────────────────────────────────┘│
│  [+ Add item]                          [Revert]  [Save]  [Publish all]   │
└──────────────────────────────────────────────────────────────────────────┘
```

Clicking **Edit** on a row expands an inline form (label + URL inputs).
Dragging the ⠿ handle reorders within a level or promotes/demotes one
level (SortableJS `group` option with `pull` / `put` constraints).

---

## 4. Module layout

```
templates/admin/cms/settings/nav.html    — NEW; replaces group.html for nav
blueprints/admin/cms/blueprint.py        — DELTA: special-case nav in settings_group
```

No new Python API routes — the existing `PUT /admin/api/settings/nav/`
accepts the serialised tree.

---

## 5. SortableJS integration

CDN: `https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js`

Options per level:
```js
{
  handle: ".drag-handle",
  animation: 150,
  group: { name: "nav-L" + depth, pull: ["nav-L" + depth, "nav-L" + (depth-1)],
           put: depthOk },
  onEnd: markDirty,
}
```

Depth enforcement: `put` callback returns `false` when target depth
would exceed 3.

---

## 6. Save/publish flow

1. **Save**: serialise DOM tree to JSON array → `PUT /admin/api/settings/nav/`
   with `{value: [...]}` → 200 → toast "Saved".
2. **Publish all**: `POST /admin/api/settings/publish/` — identical to
   the other settings groups.
3. **Revert**: reload the last-saved JSON from the server and re-render
   the list.

---

## 7. Verification gate

1. `/admin/settings/nav/` renders the nav builder (not a raw JSON textarea).
2. Add item → label + URL → Save → `GET /admin/api/settings/nav/` (or
   `/admin/settings/nav/`) reflects the new item.
3. Drag an item to a new position → Save → order persists on reload.
4. Add child → depth check: "Add child" hidden at depth 3.
5. `/admin/theme/` still returns 200 (no regression).
