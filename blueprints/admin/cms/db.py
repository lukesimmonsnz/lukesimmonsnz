"""SQLite connection management for cms.db.

See docs/CMS-IMPL-WAVE-1.md §2.2 (schema) and §2.4 (migration idempotency).

Per-request connection on flask.g, autocommit + explicit BEGIN, WAL
journal mode. Connection is closed on app teardown. Migration is
idempotent (CREATE TABLE IF NOT EXISTS) and runs at first connect.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, current_app, g


# --- schema (mirrors CMS-SPEC §2.2) -------------------------------------

_SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS drafts (
        page_id     TEXT PRIMARY KEY,
        body        TEXT NOT NULL,
        frontmatter TEXT,
        base_sha    TEXT NOT NULL,
        updated     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        by_user     TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS media (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        sha256      TEXT UNIQUE NOT NULL,
        filename    TEXT NOT NULL,
        mime        TEXT NOT NULL,
        width       INTEGER,
        height      INTEGER,
        bytes       INTEGER NOT NULL,
        alt_text    TEXT,
        caption     TEXT,
        uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS settings (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    # schema_version row — incremented on future migrations
    """
    INSERT OR IGNORE INTO settings (key, value) VALUES ('schema_version', '1')
    """,
    # v2-5: media transform derivatives (crop, focal, resize)
    """
    CREATE TABLE IF NOT EXISTS media_transforms (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        media_id    INTEGER NOT NULL REFERENCES media(id) ON DELETE CASCADE,
        kind        TEXT NOT NULL CHECK(kind IN ('crop','focal','resize')),
        params      TEXT NOT NULL,
        output_sha  TEXT,
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
    INSERT OR IGNORE INTO settings (key, value) VALUES ('schema_version', '2')
    """,
)


def migrate(conn: sqlite3.Connection) -> None:
    """Apply the schema idempotently. Safe to call on every connect."""
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        for stmt in _SCHEMA:
            cur.execute(stmt)
        cur.execute("COMMIT")
    except Exception:
        cur.execute("ROLLBACK")
        raise


# --- connection helpers --------------------------------------------------


def _db_path() -> Path:
    """Resolve cms.db's path. Falls back to /tmp on FUSE mount failures."""
    instance = Path(current_app.instance_path)
    try:
        instance.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    p = instance / "cms.db"
    # Probe SQLite-level writability — FUSE mounts may reject SQLite locking
    # even when normal append-write works.
    try:
        probe = sqlite3.connect(str(p), isolation_level=None, timeout=0.5)
        probe.execute("CREATE TABLE IF NOT EXISTS _probe (x INTEGER)").close()
        probe.close()
        return p
    except sqlite3.OperationalError:
        import tempfile
        return Path(tempfile.gettempdir()) / "cms_lukesimmons.db"


def get_cms_db() -> sqlite3.Connection:
    """Return the per-request connection; create on first call.

    Settings used:
      - ``isolation_level=None``   — autocommit; transactions are explicit
        ``BEGIN`` / ``COMMIT`` so callers can compose multi-statement
        atomic operations (e.g. the base_sha clamp in drafts.put_draft).
      - ``row_factory=sqlite3.Row`` — column access by name in DAO adapters.
      - ``journal_mode=WAL``       — concurrent readers don't block the
        autosave writer.
      - ``foreign_keys=ON``        — defensive; v1 has no FKs but v2 may.
    """
    if "cms_db" not in g:
        conn = sqlite3.connect(_db_path(), isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            conn.execute("PRAGMA journal_mode = WAL")
        except sqlite3.OperationalError:
            pass  # FUSE mounts may reject WAL; default DELETE journal works fine for single-PI
        migrate(conn)
        g.cms_db = conn
    return g.cms_db


def _close_cms_db(_exc: BaseException | None) -> None:
    conn: sqlite3.Connection | None = g.pop("cms_db", None)
    if conn is not None:
        conn.close()


def init_cms_db(app: Flask) -> None:
    """Register the teardown hook on the Flask app.

    Call this once from ``create_app`` after blueprint registration.
    """
    app.teardown_appcontext(_close_cms_db)
