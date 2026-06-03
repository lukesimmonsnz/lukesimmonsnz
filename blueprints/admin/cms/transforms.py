"""Media transforms — crop, focal point, lazy resize (CMS v2 wave v2-5).

Spec: docs/CMS-SPEC-v2.md §4
Wave: docs/CMS-IMPL-WAVE-v2-5.md

Architectural shape
-------------------
Original asset:           static/media/<sha[:2]>/<sha>.<ext>
Crop derivative:          static/media/<sha[:2]>/<sha>__t<id>.<ext>
Resize derivative:        static/media/<sha[:2]>/<sha>__t<id>.<ext>
Focal point:              metadata only (no derivative)

All derivatives are content-addressed by transform_id (the
media_transforms.id), keeping the on-disk path stable across rerenders.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import io
import json


CANONICAL_WIDTHS: tuple[int, ...] = (320, 640, 1024, 1920)

_EXT_TO_PIL: dict[str, str] = {
    "jpg": "JPEG", "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "gif": "GIF",
}


@dataclass(frozen=True)
class TransformResult:
    transform_id: int
    output_path:  Path
    output_sha:   str
    width:        int
    height:       int
    bytes:        int


def derived_path(sha: str, transform_id: int, ext: str) -> Path:
    """Canonical derived-asset path.

        static/media/<sha[:2]>/<sha>__t<id>.<ext>

    Pure — no I/O. Mirrors the v1 media.asset_path convention but adds
    the __t<id> infix for derivatives.
    """
    ext = ext.lstrip(".")
    return Path("static/media") / sha[:2] / f"{sha}__t{transform_id}.{ext}"


def canonical_params(params: dict) -> str:
    """JSON-canonicalise transform params for the UNIQUE constraint
    on (media_id, kind, params). sort_keys + tight separators.

    Two semantically-equal param dicts MUST hash to the same string,
    so that re-issuing a transform is idempotent.
    """
    return json.dumps(params, sort_keys=True, separators=(",", ":"))


def _src_sha(src_path: Path) -> str:
    """Extract the original media SHA from a src_path stem.

    Original:  static/media/ab/abc123.<ext>   -> stem = "abc123"
    Derived:   static/media/ab/abc123__t7.<ext> -> stem = "abc123__t7"
    In both cases the sha is the part before the first "__t".
    """
    return src_path.stem.split("__t")[0]


# ---------------- crop ------------------------------------------------


def crop_transform(
    media_id: int,
    src_path: Path,
    *,
    x: float, y: float, w: float, h: float,
    format: str = "jpeg",
    quality: int = 85,
) -> TransformResult:
    """Apply a fractional crop, write derivative, insert media_transforms row.

    Args:
        media_id:  FK into media.id.
        src_path:  Original asset path.
        x, y:      Crop top-left, fractional [0, 1] of original.
        w, h:      Crop size, fractional.
        format:    Output container — "jpeg" | "png" | "webp".
        quality:   85 default for jpeg/webp; ignored for png.

    Idempotent on (media_id, kind='crop', canonical_params({x,y,w,h,format,quality})).

    Returns the existing or newly-created TransformResult.

    Raises:
        ValueError if x+w > 1.0 or y+h > 1.0 or any out-of-range param.
    """
    if not (0.0 <= x < 1.0 and 0.0 <= y < 1.0
            and 0.0 < w <= 1.0 and 0.0 < h <= 1.0
            and x + w <= 1.0 and y + h <= 1.0):
        raise ValueError(
            f"Crop params out of range: x={x} y={y} w={w} h={h} "
            f"(require x+w≤1 and y+h≤1)"
        )

    params = {"format": format, "h": h, "quality": quality, "w": w, "x": x, "y": y}
    cp = canonical_params(params)

    from blueprints.admin.cms.db import get_cms_db
    conn = get_cms_db()

    # idempotency: return existing row if already computed
    row = conn.execute(
        "SELECT id, output_sha, width, height, bytes FROM media_transforms "
        "WHERE media_id = ? AND kind = 'crop' AND params = ?",
        (media_id, cp),
    ).fetchone()
    if row is not None:
        ext = "jpg" if format == "jpeg" else format
        return TransformResult(
            transform_id=row["id"],
            output_path=derived_path(row["output_sha"], row["id"], ext),
            output_sha=row["output_sha"],
            width=row["width"],
            height=row["height"],
            bytes=row["bytes"],
        )

    # Insert placeholder row to acquire a stable transform_id before writing file
    conn.execute("BEGIN")
    try:
        cur = conn.execute(
            "INSERT INTO media_transforms (media_id, kind, params) VALUES (?, 'crop', ?)",
            (media_id, cp),
        )
        transform_id = cur.lastrowid

        ext = "jpg" if format == "jpeg" else format
        src_sha = _src_sha(src_path)
        out_path = derived_path(src_sha, transform_id, ext)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        from PIL import Image
        pil_format = _EXT_TO_PIL.get(ext, "JPEG")

        with Image.open(src_path) as im:
            im.load()
            iw, ih = im.size
            box = (
                int(x * iw), int(y * ih),
                int((x + w) * iw), int((y + h) * ih),
            )
            cropped = im.crop(box)
            cw, ch = cropped.size

            # JPEG cannot carry alpha; flatten onto white
            if pil_format == "JPEG" and cropped.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", cropped.size, (255, 255, 255))
                if cropped.mode == "P":
                    cropped = cropped.convert("RGBA")
                bg.paste(cropped, mask=cropped.split()[-1] if cropped.mode in ("RGBA", "LA") else None)
                cropped = bg
            elif pil_format == "JPEG" and cropped.mode != "RGB":
                cropped = cropped.convert("RGB")

            buf = io.BytesIO()
            save_kw: dict = {}
            if pil_format in ("JPEG", "WEBP"):
                save_kw["quality"] = quality
            cropped.save(buf, pil_format, **save_kw)

        raw = buf.getvalue()
        out_sha = hashlib.sha256(raw).hexdigest()
        out_path.write_bytes(raw)
        sz = len(raw)

        conn.execute(
            "UPDATE media_transforms "
            "SET output_sha=?, width=?, height=?, bytes=? WHERE id=?",
            (out_sha, cw, ch, sz, transform_id),
        )
        conn.execute("COMMIT")

        return TransformResult(
            transform_id=transform_id,
            output_path=out_path,
            output_sha=out_sha,
            width=cw,
            height=ch,
            bytes=sz,
        )
    except Exception:
        conn.execute("ROLLBACK")
        # Clean up any partial write
        try:
            if out_path.exists():
                out_path.unlink()
        except Exception:
            pass
        raise


# ---------------- focal point (metadata only) ------------------------


def focal_set(media_id: int, *, x: float, y: float) -> None:
    """Persist (or upsert) the focal-point metadata for media_id.

    No derived asset is written. The value is consumed by the renderer's
    object-position CSS in templates/_partials/img.html.

    Validates x, y in [0, 1].
    """
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        raise ValueError(f"Focal point out of range: x={x} y={y} (require [0,1])")

    from blueprints.admin.cms.db import get_cms_db
    conn = get_cms_db()

    cp = canonical_params({"x": x, "y": y})
    # Delete any existing focal row for this media_id (focal is a singleton per asset)
    # then insert fresh — simpler than ON CONFLICT when the x,y values may differ.
    conn.execute(
        "DELETE FROM media_transforms WHERE media_id = ? AND kind = 'focal'",
        (media_id,),
    )
    conn.execute(
        "INSERT INTO media_transforms (media_id, kind, params) VALUES (?, 'focal', ?)",
        (media_id, cp),
    )


def focal_get(media_id: int) -> tuple[float, float] | None:
    """Look up the focal point for media_id, or None if not set."""
    from blueprints.admin.cms.db import get_cms_db
    conn = get_cms_db()
    row = conn.execute(
        "SELECT params FROM media_transforms WHERE media_id = ? AND kind = 'focal'",
        (media_id,),
    ).fetchone()
    if row is None:
        return None
    p = json.loads(row["params"])
    return (float(p["x"]), float(p["y"]))


# ---------------- lazy resize ----------------------------------------


def resize_lazy(
    media_id: int,
    src_path: Path,
    *,
    width: int,
) -> TransformResult:
    """Look up or generate a resized derivative for `width`.

    Args:
        width:  MUST be in CANONICAL_WIDTHS.

    Aspect ratio preserved. Resample via PIL.Image.LANCZOS. Format
    inherits from src_path suffix.

    Idempotent on (media_id, kind='resize', canonical_params({width})).
    """
    if width not in CANONICAL_WIDTHS:
        raise ValueError(f"width {width} not in CANONICAL_WIDTHS {CANONICAL_WIDTHS}")

    from blueprints.admin.cms.db import get_cms_db
    conn = get_cms_db()

    cp = canonical_params({"of": "original", "width": width})

    # idempotency check
    row = conn.execute(
        "SELECT id, output_sha, width, height, bytes FROM media_transforms "
        "WHERE media_id = ? AND kind = 'resize' AND params = ?",
        (media_id, cp),
    ).fetchone()
    if row is not None:
        ext = src_path.suffix.lstrip(".")
        return TransformResult(
            transform_id=row["id"],
            output_path=derived_path(row["output_sha"], row["id"], ext),
            output_sha=row["output_sha"],
            width=row["width"],
            height=row["height"],
            bytes=row["bytes"],
        )

    # Insert placeholder to get stable ID
    conn.execute("BEGIN")
    try:
        cur = conn.execute(
            "INSERT INTO media_transforms (media_id, kind, params) VALUES (?, 'resize', ?)",
            (media_id, cp),
        )
        transform_id = cur.lastrowid

        ext = src_path.suffix.lstrip(".")
        src_sha = _src_sha(src_path)
        out_path = derived_path(src_sha, transform_id, ext)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        from PIL import Image
        pil_format = _EXT_TO_PIL.get(ext.lower(), "JPEG")

        with Image.open(src_path) as im:
            im.load()
            iw, ih = im.size

            if iw <= width:
                # Already at or below target width — copy verbatim
                rw, rh = iw, ih
                buf = io.BytesIO()
                save_kw: dict = {"quality": 85} if pil_format in ("JPEG", "WEBP") else {}
                im.save(buf, pil_format, **save_kw)
            else:
                # Downscale: thumbnail respects aspect ratio
                im.thumbnail((width, 10 * ih), Image.Resampling.LANCZOS)
                rw, rh = im.size
                buf = io.BytesIO()
                save_kw = {"quality": 85} if pil_format in ("JPEG", "WEBP") else {}
                im.save(buf, pil_format, **save_kw)

        raw = buf.getvalue()
        out_sha = hashlib.sha256(raw).hexdigest()
        out_path.write_bytes(raw)
        sz = len(raw)

        conn.execute(
            "UPDATE media_transforms "
            "SET output_sha=?, width=?, height=?, bytes=? WHERE id=?",
            (out_sha, rw, rh, sz, transform_id),
        )
        conn.execute("COMMIT")

        return TransformResult(
            transform_id=transform_id,
            output_path=out_path,
            output_sha=out_sha,
            width=rw,
            height=rh,
            bytes=sz,
        )
    except Exception:
        conn.execute("ROLLBACK")
        try:
            if out_path.exists():
                out_path.unlink()
        except Exception:
            pass
        raise


# ---------------- srcset emission ------------------------------------


def srcset_for(media_id: int, src_path: Path) -> str:
    """Return the `srcset` attribute value for media_id.

    Format:
        '<url320> 320w, <url640> 640w, <url1024> 1024w, <url1920> 1920w'

    Generates missing widths lazily via resize_lazy. The URL is the
    Flask static path (/static/media/<sha[:2]>/<sha>__t<id>.<ext>).
    """
    parts: list[str] = []
    for w in CANONICAL_WIDTHS:
        result = resize_lazy(media_id, src_path, width=w)
        # derived_path returns a relative path like static/media/...
        url = "/" + result.output_path.as_posix()
        parts.append(f"{url} {w}w")
    return ", ".join(parts)
