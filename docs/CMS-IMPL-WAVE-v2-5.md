# CMS-IMPL-WAVE-v2-5 — Media transforms (crop, focal, srcset)

**Status:** design artefact — wave v2-5 of `CMS-SPEC-v2.md` §4.
**PI directive (2026-05-02):** authored in parallel; mechanical.
**Scope:** crop, focal-point, responsive `srcset`. No PI mastery.

---

## 1. Architectural shape

v1: each upload writes `static/media/<sha[:2]>/<sha>.<ext>` (original)
plus `static/media/<sha[:2]>/<sha>.thumb.jpg` (240px max-dim JPEG).

v2 adds a `media_transforms` table and three transform pipelines:

| Transform | Storage | Trigger |
|---|---|---|
| **Crop** | `<sha>__crop_<id>.<ext>` | PI clicks "Save crop" in the media browser |
| **Focal** | (metadata only — JSON in transforms.params) | PI drags the focal-point target |
| **Resize-N** | `<sha>__r<width>.<ext>` | First request for that width via the renderer's `srcset` filter |

Crop and focal are PI-authored derived assets. Resize-N is lazy and
machine-derived from the original (or, if the asset has a crop, from
the cropped derived asset).

---

## 2. DDL extension to `db.py`

Append to `_SCHEMA`:

```python
"""
CREATE TABLE IF NOT EXISTS media_transforms (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id    INTEGER NOT NULL REFERENCES media(id) ON DELETE CASCADE,
    kind        TEXT NOT NULL CHECK(kind IN ('crop','focal','resize')),
    params      TEXT NOT NULL,           -- JSON
    output_sha  TEXT,                    -- NULL for 'focal' (metadata only)
    width       INTEGER,
    height      INTEGER,
    bytes       INTEGER,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (media_id, kind, params)
)
""",
"""
CREATE INDEX IF NOT EXISTS ix_media_transforms_media_id
    ON media_transforms(media_id)
""",
"""
UPDATE settings SET value = '2' WHERE key = 'schema_version' AND value = '1'
""",
```

The `UNIQUE (media_id, kind, params)` index makes lookups idempotent —
re-issuing the same crop is a no-op. The `params` JSON is canonicalised
on write (sort_keys=True, separators (',', ':')) so semantically-equal
specs hash to the same string.

---

## 3. Transform parameter schemas

### 3.1 Crop

```json
{
  "x": 0, "y": 0,           // top-left, fractional [0,1] of original
  "w": 1.0, "h": 1.0,       // size, fractional
  "format": "jpeg",         // "jpeg" | "png" | "webp"
  "quality": 85             // for jpeg/webp
}
```

### 3.2 Focal point

```json
{
  "x": 0.5, "y": 0.5         // fractional [0,1] — ratio-relative anchor
}
```

Focal is metadata only — no derived asset is written. It is consumed by
the `<img style="object-position: ...">` filter at render time.

### 3.3 Resize

```json
{
  "width": 320,              // 320 | 640 | 1024 | 1920 (canonical breaks)
  "of": "original"           // "original" | "crop_<id>"
}
```

The renderer requests `resize?width=640&of=original`; if the
`media_transforms` row exists, serve the file. If not, generate (Pillow
LANCZOS resample), insert the row, serve.

---

## 4. transforms.py — module contract

```python
# blueprints/admin/cms/transforms.py

from dataclasses import dataclass
from pathlib import Path
import io, json, hashlib

from PIL import Image       # already a transitive dep via media.py thumbs


CANONICAL_WIDTHS = (320, 640, 1024, 1920)


@dataclass(frozen=True)
class TransformResult:
    output_path:  Path
    output_sha:   str
    width:        int
    height:       int
    bytes:        int


def crop_transform(
    media_id: int,
    src_path: Path,
    *, x: float, y: float, w: float, h: float,
    format: str = "jpeg", quality: int = 85,
) -> TransformResult:
    """Apply a crop, write derived asset, insert media_transforms row.

    Idempotent on (media_id, params): existing row is returned unchanged.
    """
    ...   # PI fills body — Pillow open → crop → save → insert


def focal_set(media_id: int, *, x: float, y: float) -> None:
    """Persist (or upsert) the focal-point metadata for media_id."""
    ...   # PI fills body — single INSERT...ON CONFLICT


def resize_lazy(
    media_id: int, src_path: Path, *, width: int,
) -> TransformResult:
    """Look up or generate a resized derived asset for `width`.

    `width` MUST be in CANONICAL_WIDTHS. Aspect ratio preserved.
    Resample via Image.LANCZOS. Format inherits from src_path suffix.
    """
    ...   # PI fills body


def srcset_for(media_id: int, src_path: Path) -> str:
    """Return the `srcset` attribute string for media_id.

    Format: '<url320> 320w, <url640> 640w, <url1024> 1024w, <url1920> 1920w'

    Generates missing widths lazily via resize_lazy.
    """
    ...   # PI fills body


def derived_path(sha: str, transform_id: int, ext: str) -> Path:
    """Canonical derived-asset path:
        static/media/<sha[:2]>/<sha>__t<id>.<ext>
    """
    return Path("static/media") / sha[:2] / f"{sha}__t{transform_id}.{ext}"
```

---

## 5. Crop UI surface

Modal extension to the existing `templates/admin/cms/editor.html` media
browser:

- Selecting an image in the modal shows a `<canvas>`-based crop overlay
  (draggable rectangle, resize handles at the four corners).
- A focal-point target overlay (a small crosshair the PI drags within
  the cropped area).
- "Save crop" → POST to `/admin/api/media/<media_id>/crop/` with the
  fractional rectangle.
- "Save focal" → POST to `/admin/api/media/<media_id>/focal/` with `(x, y)`.

Vendored library: `cropperjs` v1.6.x at `static/js/cropper.min.js` —
~50 KB minified, no transitive deps. Drop in via plain `<script>`,
match the v1 zero-build-tooling posture.

---

## 6. Renderer integration

A new Jinja filter `srcset` and a partial `templates/_partials/img.html`:

```jinja
{# partial — replaces hand-written <img> in the rendered MD when
   the renderer encounters an image whose src has a media_id #}
<img src="{{ media.url }}"
     srcset="{{ media | srcset }}"
     sizes="(max-width: 640px) 100vw, (max-width: 1024px) 80vw, 1024px"
     alt="{{ media.alt_text }}"
     {% if media.focal %}style="object-position: {{ media.focal.x*100 }}% {{ media.focal.y*100 }}%;"{% endif %}>
```

Resolution of "src has a media_id" is via `static/media/<sha[:2]>/<sha>.<ext>`
URL pattern matching against the `media` table; non-matching `<img>` tags
pass through unchanged.

---

## 7. Module layout

```
blueprints/admin/cms/transforms.py     — NEW
blueprints/admin/cms/db.py             — extended _SCHEMA (delta in §2)
blueprints/admin/cms/blueprint.py      — 3 new routes + filter registration
templates/admin/cms/editor.html        — crop modal extension
templates/_partials/img.html           — NEW (srcset-aware <img>)
static/js/cropper.min.js               — vendored
```

---

## 8. Verification gate

1. `python -c "from blueprints.admin.cms.transforms import derived_path; \
    assert derived_path('abc123', 7, 'jpg').as_posix() == 'static/media/ab/abc123__t7.jpg'"`
2. Upload a 4000×3000 JPEG → crop to 0.1, 0.1, 0.5, 0.5 → derived asset
   exists at the canonical path; `media_transforms` row written;
   re-issuing the same crop returns the existing row (idempotency).
3. Request `<img | srcset>` for an uploaded image → all four widths in
   `CANONICAL_WIDTHS` get derived and listed in the returned `srcset`.
4. Set focal point (0.3, 0.4) → next render of that image emits
   `object-position: 30% 40%`.

---

## 9. Out of scope

- Animated GIF / video transforms.
- AVIF / WebP auto-conversion (only Pillow-supported sources).
- Smart-crop / face detection (focal point is PI-authored, not
  ML-derived).
- CDN integration (Cloudflare Images etc.) — the on-disk derived
  asset model is the only path in v2.
