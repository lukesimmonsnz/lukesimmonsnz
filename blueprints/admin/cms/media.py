"""Media library — wave 2 item 8.

See docs/CMS-IMPL-WAVE-2.md §8.

Library functions consumed by the upload / browse route handlers in
wave 3 (item ι in the implementation graph). No Flask context required
beyond ``get_cms_db()``; routes are not registered here.

Storage layout:
    static/media/<sha[:2]>/<sha>.<ext>          original (content-addressed)
    static/media/<sha[:2]>/<sha>_thumb.jpg      thumbnail (always JPEG)

Ratified parameters (CMS-IMPL-WAVE-2 §9):
    W2-5: default insert URL is the original (theme caps max-width: 100%)
    W2-6: thumbnail (max_dim, quality) = (240, 80)
"""
from __future__ import annotations

import hashlib
import io
import sqlite3
from pathlib import Path

from PIL import Image

from blueprints.admin.cms.dao import MediaRow, row_to_media
from blueprints.admin.cms.db import get_cms_db


# --- ratified constants -------------------------------------------------

ALLOWED_MIMES: frozenset[str] = frozenset({
    "image/jpeg", "image/png", "image/webp", "image/gif",
    "application/pdf",
})

THUMB_MAX_DIM:  int = 240
THUMB_QUALITY:  int = 80
THUMB_SUFFIX:   str = "_thumb.jpg"

_MIME_TO_EXT: dict[str, str] = {
    "image/jpeg":      "jpg",
    "image/png":       "png",
    "image/webp":      "webp",
    "image/gif":       "gif",
    "application/pdf": "pdf",
}


# --- storage path resolution --------------------------------------------


def _project_root() -> Path:
    """blueprints/admin/cms/media.py  ->  project root is parents[3]."""
    return Path(__file__).resolve().parents[3]


def _media_root() -> Path:
    """static/media/ — created on first use."""
    root = _project_root() / "static" / "media"
    root.mkdir(parents=True, exist_ok=True)
    return root


def asset_path(sha256: str, ext: str) -> Path:
    """static/media/<sha[:2]>/<sha>.<ext> — content-addressed."""
    bucket = _media_root() / sha256[:2]
    bucket.mkdir(parents=True, exist_ok=True)
    return bucket / f"{sha256}.{ext}"


def thumbnail_path(sha256: str) -> Path:
    """static/media/<sha[:2]>/<sha>_thumb.jpg — sibling of asset."""
    return _media_root() / sha256[:2] / f"{sha256}{THUMB_SUFFIX}"


# --- thumbnail generation -----------------------------------------------


def make_thumbnail(
    src: Path,
    dst: Path,
    max_dim: int = THUMB_MAX_DIM,
    quality: int = THUMB_QUALITY,
) -> tuple[int, int]:
    """Generate a JPEG thumbnail at ``dst``. Returns (width, height).

    Aspect-preserving downscale: longest side bounded by ``max_dim``.
    Source-image transparency is flattened onto white (JPEG has no
    alpha channel).
    """
    with Image.open(src) as im:
        im.load()
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            background = Image.new("RGB", im.size, (255, 255, 255))
            background.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
            im = background
        elif im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        im.save(dst, "JPEG", quality=quality, optimize=True)
        return im.size


def _probe_image_dims(path: Path) -> tuple[int | None, int | None]:
    """Return (width, height) for image files; (None, None) for non-images."""
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None, None


# --- upload --------------------------------------------------------------


class MediaError(ValueError):
    """Raised when an upload fails validation."""


def upload(
    content: bytes,
    filename: str,
    mime: str,
    by_user: str | None = None,
) -> MediaRow:
    """Persist an uploaded asset and return its row.

    Pipeline (CMS-IMPL-WAVE-2 §8.3):
      1. SHA-256 over content.
      2. SELECT by sha256 — dedupe; return existing row if hit.
      3. Validate mime against ALLOWED_MIMES.
      4. Write original to static/media/<sha[:2]>/<sha>.<ext>.
      5. If image: generate thumbnail; record (width, height).
      6. INSERT row; return adapted DraftRow.

    Cleanup: any failure between (4) and (6) unlinks files written at
    (4) and (5) so partial state does not survive.
    """
    if mime not in ALLOWED_MIMES:
        raise MediaError(f"mime not allowed: {mime!r}")
    if mime not in _MIME_TO_EXT:
        raise MediaError(f"no extension mapping for mime {mime!r}")

    sha = hashlib.sha256(content).hexdigest()
    ext = _MIME_TO_EXT[mime]

    # Dedupe — return the existing row if already uploaded.
    existing = _select_by_sha(sha)
    if existing is not None:
        return existing

    src_path = asset_path(sha, ext)
    thumb = thumbnail_path(sha)
    written: list[Path] = []
    try:
        src_path.write_bytes(content)
        written.append(src_path)

        width: int | None = None
        height: int | None = None
        if mime.startswith("image/"):
            width, height = _probe_image_dims(src_path)
            try:
                make_thumbnail(src_path, thumb)
                written.append(thumb)
            except Exception:
                # Thumbnail failure is non-fatal; the original survives.
                # Recovery: media_rebuild_thumbnails admin command (deferred).
                pass

        row_id = _insert_row(
            sha256=sha, filename=filename, mime=mime,
            width=width, height=height, bytes_=len(content),
            alt_text=None, caption=None,
        )

        out = _select_by_id(row_id)
        if out is None:
            raise MediaError(f"insert succeeded but row {row_id} not found")
        return out

    except Exception:
        for p in written:
            try:
                p.unlink()
            except OSError:
                pass
        raise


# --- browse / metadata --------------------------------------------------


def browse(
    query: str = "",
    mime: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[MediaRow]:
    """List media rows. Free-text matches filename / alt_text / caption.

    ``mime`` supports glob suffix wildcards: ``image/*`` matches any
    ``image/jpeg``, ``image/png`` etc.
    """
    conn = get_cms_db()
    where: list[str] = []
    params: list[object] = []

    if query:
        like = f"%{query}%"
        where.append(
            "(filename LIKE ? OR COALESCE(alt_text,'') LIKE ? "
            "OR COALESCE(caption,'') LIKE ?)"
        )
        params.extend([like, like, like])

    if mime:
        if mime.endswith("/*"):
            where.append("mime LIKE ?")
            params.append(mime[:-1] + "%")
        else:
            where.append("mime = ?")
            params.append(mime)

    sql = (
        "SELECT id, sha256, filename, mime, width, height, bytes, "
        "       alt_text, caption, uploaded_at "
        "FROM media "
        + (f"WHERE {' AND '.join(where)} " if where else "")
        + "ORDER BY uploaded_at DESC LIMIT ? OFFSET ?"
    )
    params.extend([limit, offset])
    rows = conn.execute(sql, params).fetchall()
    return [row_to_media(r) for r in rows]


def update_metadata(media_id: int,
                    alt_text: str | None,
                    caption: str | None) -> None:
    """Direct UPDATE — no draft semantics for media metadata (§8.8)."""
    conn = get_cms_db()
    conn.execute(
        "UPDATE media SET alt_text = ?, caption = ? WHERE id = ?",
        (alt_text, caption, media_id),
    )


def insert_url(row: MediaRow) -> str:
    """The URL the editor splices into Markdown for an inserted asset.

    W2-5 ratification: original-resolution URL by default.
    """
    ext = _MIME_TO_EXT[row.mime]
    return f"/static/media/{row.sha256[:2]}/{row.sha256}.{ext}"


# --- internal SQL helpers ------------------------------------------------


def _select_by_sha(sha256: str) -> MediaRow | None:
    conn = get_cms_db()
    row = conn.execute(
        "SELECT id, sha256, filename, mime, width, height, bytes, "
        "       alt_text, caption, uploaded_at "
        "FROM media WHERE sha256 = ?",
        (sha256,),
    ).fetchone()
    return row_to_media(row) if row is not None else None


def _select_by_id(media_id: int) -> MediaRow | None:
    conn = get_cms_db()
    row = conn.execute(
        "SELECT id, sha256, filename, mime, width, height, bytes, "
        "       alt_text, caption, uploaded_at "
        "FROM media WHERE id = ?",
        (media_id,),
    ).fetchone()
    return row_to_media(row) if row is not None else None


def _insert_row(
    sha256: str, filename: str, mime: str,
    width: int | None, height: int | None,
    bytes_: int, alt_text: str | None, caption: str | None,
) -> int:
    """INSERT and return the new ``id``. Dedup is the caller's job."""
    conn = get_cms_db()
    cur = conn.execute(
        "INSERT INTO media (sha256, filename, mime, width, height, "
        "                   bytes, alt_text, caption, uploaded_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        (sha256, filename, mime, width, height,
         bytes_, alt_text, caption),
    )
    return cur.lastrowid
