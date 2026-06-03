# CMS-IMPL-WAVE-v2-4 — Theme presets + override layer + customizer UI

**Status:** design artefact — wave v2-4 of `CMS-SPEC-v2.md` §5.
**PI directive (2026-05-02):** authored in parallel with v2-1 / v2-5 /
v2-6 / v2-8 — independent of the block-parser mastery surface.
**Scope:** mechanical. No PI mastery surface introduced.

---

## 1. Mathematical model

The theme is a flat-after-flattening dict $\Theta : K \to V$ over a
finite token-name set $K$. v2 ships three presets $\Theta_p$
($p \in \{\text{editorial}, \text{documentary}, \text{classic}\}$).

A user override $\Delta : K' \to V$ with $K' \subseteq K$ (sparse) is
stored in the existing `theme` settings group. Effective theme:

$$\Theta_\text{effective} = \Theta_p \oplus \Delta$$

where $\oplus$ is right-biased pointwise overwrite. Empty / `None`
values in $\Delta$ are treated as "unset" and inherit from $\Theta_p$.

`regenerate_theme_css` (v1) is extended to compute $\Theta_\text{effective}$
before emitting `--key: value;` lines.

---

## 2. Token taxonomy (CMS-SPEC-v2 §5.2, frozen)

Eight namespaces. Hyphens within a key are emitted verbatim; dots
joining namespaces become hyphens (`color.primary` → `--color-primary`).

```
typography:
  scale                 : float (modular ratio; 1.2 / 1.25 / 1.333)
  font-family-body      : str
  font-family-heading   : str
  font-family-mono      : str
  line-height-body      : float
  line-height-heading   : float
  weight-body           : int    (400, 500)
  weight-bold           : int    (600, 700)
  weight-heading        : int    (500, 600, 700)

spacing:
  unit                  : str    ("4px" or "8px" — base step)
  scale-0..scale-9      : str    (computed; see §3 below)

color:
  primary, primary-fg
  bg, fg, muted, accent, danger, success
  surface-1, surface-2
  border

radius:
  sm, md, lg, full

shadow:
  sm, md, lg

motion:
  duration-fast, duration-base
  easing-standard, easing-emphasised

layout:
  max-width, gutter
  breakpoint-sm, breakpoint-md, breakpoint-lg
```

---

## 3. Spacing scale derivation

To keep the preset declarative without forcing PI to enumerate ten
spacing tokens by hand, the loader optionally computes
`spacing.scale-N` from `spacing.unit` via a Fibonacci-flavoured
sequence:

$$s_n = u \cdot \phi(n), \quad \phi = (0.5,\, 1,\, 1.5,\, 2,\, 3,\, 4,\, 6,\, 8,\, 12,\, 16)$$

where $u$ is parsed from `unit` (e.g. `"8px"` ⇒ $u = 8$). PI may
override any individual `scale-N` in the preset YAML to break the
sequence; the loader respects explicit values over computed ones.

PI mastery: choosing $\phi$. The Fibonacci-flavoured sequence above is
suggested, not mandated.

---

## 4. Preset files

```
content/_themes/
  editorial.yaml      # serif headings, narrow column, generous spacing
  documentary.yaml    # sans-serif, dense grid layout
  classic.yaml        # current site's tokens, sans-serif single column
```

The three presets are seeded in this wave. Each is hand-authored,
byte-stable. Each declares only the tokens it overrides versus the
loader's defaults; missing tokens fall through to the loader's
canonical defaults (defined in `_theme_loader.py`).

---

## 5. Settings group changes

### 5.1 `theme_preset` key

A new top-level settings key (NOT a group) records which preset is
active:

```sql
INSERT INTO settings (key, value) VALUES ('theme_preset', '"classic"');
```

JSON-encoded so the existing settings k/v table accepts it without
schema change.

### 5.2 `theme` group becomes the override delta

The existing `theme` group (currently a full dict) is reinterpreted as
the override $\Delta$. v1 settings that are full themes still parse —
they simply override every token. PI can prune to only customised keys
post-migration.

---

## 6. Module layout

```
blueprints/admin/cms/
  theme.py              # NEW — preset loader + composer

blueprints/admin/cms/settings.py
  ┣━ regenerate_theme_css     — extended to compose preset ⊕ override
  ┣━ get_active_preset        — NEW thin wrapper on theme_preset key
  ┗━ set_active_preset        — NEW

content/_themes/
  editorial.yaml              — seeded
  documentary.yaml            — seeded
  classic.yaml                — seeded
  defaults.yaml               — fall-through values for any missing token

templates/admin/cms/theme/
  index.html                  — preset selector + per-token form
```

---

## 7. theme.py — module contract

```python
# blueprints/admin/cms/theme.py

from pathlib import Path
import yaml

PRESETS_DIR = Path("content/_themes")
DEFAULTS_PATH = PRESETS_DIR / "defaults.yaml"

KNOWN_PRESETS: tuple[str, ...] = ("editorial", "documentary", "classic")


def load_preset(name: str) -> dict:
    """Load a preset YAML into a nested dict.

    Raises FileNotFoundError if the preset is missing. Missing tokens
    are NOT auto-filled here — that is the composer's job.
    """
    path = PRESETS_DIR / f"{name}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_defaults() -> dict:
    """Fall-through token values, applied when neither preset nor
    override sets a key."""
    return yaml.safe_load(DEFAULTS_PATH.read_text(encoding="utf-8")) or {}


def compose(preset: dict, override: dict) -> dict:
    """Right-biased deep merge: override values shadow preset, preset
    values shadow defaults, recursively. Empty strings and None in
    override are treated as 'inherit from preset'."""
    ...   # PI fills body — straightforward recursive dict merge


def derive_spacing_scale(theme: dict) -> dict:
    """If theme['spacing']['unit'] is set and any spacing.scale-N is
    missing, compute the missing ones from the Fibonacci-ish sequence
    in §3. Returns a new dict; does not mutate input."""
    ...   # PI fills body
```

The composer's contract:

$$\Theta_\text{eff}[k] = \begin{cases}
  \Delta[k] & \text{if } k \in \Delta \land \Delta[k] \notin \{\emptyset, \text{None}\} \\
  \Theta_p[k] & \text{else if } k \in \Theta_p \\
  \Theta_d[k] & \text{else (defaults)}
\end{cases}$$

Tested by: a preset-equality round-trip (compose with empty override
returns preset values verbatim) and a sparse-override test (override
with one key shadows preset for that key only).

---

## 8. Settings.py delta

```diff
-def regenerate_theme_css(theme: dict | None = None) -> Path:
-    theme = theme if theme is not None else get_group("theme")
-    rules = list(_emit_css_vars(theme, prefix=""))
+def regenerate_theme_css(override: dict | None = None) -> Path:
+    """Compose preset ⊕ override and emit CSS. Falls back to the
+    legacy single-dict behaviour when theme_preset is unset."""
+    from blueprints.admin.cms.theme import (
+        load_preset, load_defaults, compose, derive_spacing_scale,
+    )
+    override = override if override is not None else get_group("theme")
+    preset_name = get_active_preset()
+    if preset_name in ("editorial", "documentary", "classic"):
+        defaults = load_defaults()
+        preset = load_preset(preset_name)
+        composed = compose(compose(defaults, preset), override)
+        composed = derive_spacing_scale(composed)
+    else:
+        composed = override          # legacy behaviour
+    rules = list(_emit_css_vars(composed, prefix=""))
     body = ":root {\n" + "\n".join(f"  {r}" for r in rules) + "\n}\n"
     _atomic_write_text(_theme_css_path(), body)
     return _theme_css_path()
+
+
+def get_active_preset() -> str:
+    conn = get_cms_db()
+    row = conn.execute("SELECT value FROM settings WHERE key = ?",
+                       ("theme_preset",)).fetchone()
+    if row is None:
+        return "classic"
+    return json.loads(row["value"])
+
+
+def set_active_preset(name: str) -> None:
+    if name not in ("editorial", "documentary", "classic", "custom"):
+        raise ValueError(f"unknown preset: {name!r}")
+    conn = get_cms_db()
+    conn.execute(
+        "INSERT INTO settings (key, value) VALUES (?, ?) "
+        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
+        ("theme_preset", json.dumps(name)),
+    )
```

---

## 9. Customizer UI

Routes (added to `blueprint.py`):

```
GET  /admin/theme/                 → preset selector + per-token form
PUT  /admin/api/theme/preset/      → {name: "editorial"|...}
PUT  /admin/api/theme/override/    → JSON delta blob
POST /admin/api/theme/publish/     → atomic write theme.css + invalidate cache
GET  /admin/theme/preview/?id=…    → δ overlay-backed live preview
```

The per-token form is generated from the taxonomy in §2:

- Color tokens render as `<input type="color">` plus a text input for
  alpha-bearing rgba values.
- Numeric scale tokens render as a slider with min/max/step.
- Font-family tokens render as text + a dropdown of system-safe stacks.
- Each token gets a "reset to preset" button (un-sets the key in the
  override delta).

Live preview uses the existing δ overlay (CMS wave 3): activates an
`Overlay` whose `intercepts` map shadows `static/theme.css` with an
in-memory composed CSS based on the current form state. The preview
iframe re-fetches `/?theme_preview=1` (a new query-param flag the
customizer adds; the base template injects an extra `<style>` block
when the flag is set, sourcing from the overlay).

---

## 10. Verification gate

Wave v2-4 closes when:

1. `python -c "from blueprints.admin.cms.theme import compose, load_preset, load_defaults; \
    p=load_preset('classic'); d=load_defaults(); \
    assert compose(d, p) == compose(d, p) | p, 'preset shadow violated'"`
   passes for all three presets.
2. `regenerate_theme_css({})` with `theme_preset='editorial'` writes a
   `static/theme.css` that contains every token from the editorial
   preset.
3. `/admin/theme/` route renders without exception and the preset
   selector reflects the current `theme_preset`.
4. PI manual smoke: switch preset → publish → live site reloads CSS;
   no FOUC longer than `theme_css_cache_bust()` mtime jitter.

---

## 11. Out of scope for this wave

- Migrating the existing `static/css/main.css` to consume the v2 token
  names. The wave only adds new tokens; existing CSS continues to use
  its current variable names. PI can schedule a rename pass later.
- Custom-preset authoring UI (only edit-existing-override is supported
  — adding a fourth preset is a hand-edit at `content/_themes/<name>.yaml`).
