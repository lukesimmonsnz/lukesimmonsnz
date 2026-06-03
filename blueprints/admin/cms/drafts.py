"""Draft store API.

See docs/CMS-IMPL-WAVE-1.md §3.

Six functions over the ``drafts`` table:
    get_draft, put_draft, drop_draft, list_dirty,
    has_conflict, conflict_triple

The mathematically interesting bits:

  - has_conflict(p)  iff  sha256(file(p)) != draft(p).base_sha
  - put_draft        clamps base_sha to the existing row's value on
                     subsequent puts within a draft session — once set,
                     never advances. This is the contract that makes
                     has_conflict semantically meaningful.

The SQL CRUD itself is mechanical; the architectural surface is the
``base_sha`` lifecycle in put_draft (§3.4 of WAVE-1).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from blueprints.admin.cms.dao import DraftRow, row_to_draft
from blueprints.admin.cms.db import get_cms_db


# --- file-content hashing -----------------------------------------------


def file_sha256(path: Path) -> str:
    """SHA-256 over the file's raw bytes. Empty string if file missing.

    Defining the missing-file case as the empty-string hash sentinel
    means has_conflict trivially fires when the underlying file has
    been deleted while a draft was open.
    """
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_concat(paths: tuple[Path, ...]) -> str:
    """Concatenated SHA-256 over a path-sorted sequence.

    Used by HYBRID pages whose ``source_paths`` is multi-file
    (per WAVE-1 §3.2 — wave-1 ratification chose per-page granularity).

    Hashes each file and the file's stable identifier (its path string),
    then hashes the concatenation. The path string is included so that
    renaming a slot file produces a different aggregate hash.
    """
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda q: str(q)):
        h.update(str(p).encode("utf-8"))
        h.update(b"\x00")
        h.update(file_sha256(p).encode("ascii"))
        h.update(b"\x00")
    return h.hexdigest()


# --- the six API functions ----------------------------------------------


def get_draft(page_id: str) -> DraftRow | None:
    conn = get_cms_db()
    row = conn.execute(
        "SELECT page_id, body, frontmatter, base_sha, updated, by_user "
        "FROM drafts WHERE page_id = ?",
        (page_id,),
    ).fetchone()
    return row_to_draft(row) if row is not None else None


def put_draft(
    page_id: str,
    body: str,
    frontmatter: str | None,
    base_sha: str,
    by_user: str | None,
) -> None:
    """Insert-or-update a draft, clamping base_sha on update.

    Contract (§3.3, §3.4):
      - First put for a page_id: persists the supplied base_sha.
      - Subsequent puts: server keeps the existing base_sha; the value
        passed in by the client is ignored. This makes the field
        immutable per draft session and is what allows has_conflict to
        compare ``file(p)`` against a known-stable reference point.

    Atomicity is via the explicit BEGIN/COMMIT under autocommit (see
    db.get_cms_db).
    """
    conn = get_cms_db()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        existing = cur.execute(
            "SELECT base_sha FROM drafts WHERE page_id = ?",
            (page_id,),
        ).fetchone()
        effective_base = existing["base_sha"] if existing is not None else base_sha
        cur.execute(
            "INSERT INTO drafts (page_id, body, frontmatter, base_sha, "
            "                    updated, by_user) "
            "VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?) "
            "ON CONFLICT(page_id) DO UPDATE SET "
            "    body = excluded.body, "
            "    frontmatter = excluded.frontmatter, "
            "    updated = CURRENT_TIMESTAMP, "
            "    by_user = excluded.by_user",
            (page_id, body, frontmatter, effective_base, by_user),
        )
        cur.execute("COMMIT")
    except Exception:
        cur.execute("ROLLBACK")
        raise


def drop_draft(page_id: str) -> None:
    conn = get_cms_db()
    conn.execute("DELETE FROM drafts WHERE page_id = ?", (page_id,))


def list_dirty() -> list[DraftRow]:
    conn = get_cms_db()
    rows = conn.execute(
        "SELECT page_id, body, frontmatter, base_sha, updated, by_user "
        "FROM drafts ORDER BY updated DESC"
    ).fetchall()
    return [row_to_draft(r) for r in rows]


def has_conflict(page_id: str, source_paths: tuple[Path, ...]) -> bool:
    """Conflict iff the on-disk source content has shifted since the
    draft opened.

       conflict(p)  iff  hash_concat(source_paths) != draft.base_sha

    For single-file pages (DIRECT_MD), source_paths has one element and
    hash_concat reduces to file_sha256 with the path-prefix wrap.
    """
    draft = get_draft(page_id)
    if draft is None:
        return False
    return hash_concat(source_paths) != draft.base_sha


def conflict_triple(
    page_id: str, source_paths: tuple[Path, ...]
) -> tuple[bytes, bytes, str] | None:
    """Return (base_content, file_now_content, draft_now_body) for the
    3-way merge UI.

    ``base_content`` is approximated as the on-disk content at the time
    the draft was opened — but we don't keep that around, so for v1 we
    return the *current file content* twice (once as base, once as
    file_now) when no conflict, and on conflict the editor surfaces only
    file_now vs draft_now. Pure 3-way merge requires preserving the base
    bytes alongside base_sha; deferred to v2.

    Returns None if no draft exists for page_id.
    """
    draft = get_draft(page_id)
    if draft is None:
        return None
    file_now = b"".join(
        p.read_bytes() if p.is_file() else b"" for p in source_paths
    )
    # v1: base bytes are unavailable; UI uses file_now as both base+file_now
    # and conflict-detection happens against base_sha purely. PI to
    # decide in v2 whether to persist base bytes alongside base_sha.
    return file_now, file_now, draft.body
