"""Row dataclasses + adapters for cms.db.

See docs/CMS-IMPL-WAVE-1.md §2.3.

Pure types and conversions. No I/O. No mastery surface — purely
mechanical infrastructure that the rest of the CMS package consumes.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime


# --- frozen row dataclasses ---------------------------------------------


@dataclass(frozen=True)
class DraftRow:
    """A single editor draft. Primary key: page_id (canonical URL).

    ``base_sha`` is the SHA-256 of the on-disk source content at the time
    the draft was opened. It is set ONCE on first put and never advances
    within the lifetime of a single draft session — that is the contract
    that makes ``has_conflict`` meaningful (see drafts.has_conflict).
    """
    page_id:     str
    body:        str
    frontmatter: str | None
    base_sha:    str
    updated:     datetime
    by_user:     str | None


@dataclass(frozen=True)
class MediaRow:
    """An uploaded media asset. Content-addressed by sha256 (UNIQUE)."""
    id:          int
    sha256:      str
    filename:    str
    mime:        str
    width:       int | None
    height:      int | None
    bytes:       int
    alt_text:    str | None
    caption:     str | None
    uploaded_at: datetime


@dataclass(frozen=True)
class SettingRow:
    """A k/v setting (CMS-SPEC §7). For wave 4, value is a JSON blob
    per group (W4-1 ratification: JSON-blob-per-group)."""
    key:   str
    value: str


# --- adapters from sqlite3.Row ------------------------------------------


def _parse_ts(value: str | None) -> datetime:
    """Parse SQLite TIMESTAMP text into a naive datetime.

    SQLite stores timestamps as text via ``CURRENT_TIMESTAMP`` ('YYYY-MM-DD
    HH:MM:SS'). Python 3.11+ ``datetime.fromisoformat`` handles the space
    separator. For pre-3.11 compatibility, replace the space with 'T'.
    """
    if value is None:
        # Should not occur for NOT NULL columns; defensive.
        return datetime.min
    return datetime.fromisoformat(value.replace(" ", "T"))


def row_to_draft(row: sqlite3.Row) -> DraftRow:
    return DraftRow(
        page_id=row["page_id"],
        body=row["body"],
        frontmatter=row["frontmatter"],
        base_sha=row["base_sha"],
        updated=_parse_ts(row["updated"]),
        by_user=row["by_user"],
    )


def row_to_media(row: sqlite3.Row) -> MediaRow:
    return MediaRow(
        id=row["id"],
        sha256=row["sha256"],
        filename=row["filename"],
        mime=row["mime"],
        width=row["width"],
        height=row["height"],
        bytes=row["bytes"],
        alt_text=row["alt_text"],
        caption=row["caption"],
        uploaded_at=_parse_ts(row["uploaded_at"]),
    )


def row_to_setting(row: sqlite3.Row) -> SettingRow:
    return SettingRow(key=row["key"], value=row["value"])
