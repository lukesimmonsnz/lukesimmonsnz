"""Deploy dashboard — show recent Cloudflare Pages deploys.

Reads ``logs/deploys.jsonl`` (one row per ``scripts/deploy.py`` run) and
prints a plain-text table. Newest first. The most recent successful
deploy is tagged ``live``.

Usage
-----
    python scripts/deploys.py            # last 10
    python scripts/deploys.py --limit 25 # last 25
    python scripts/deploys.py --full     # include preview URL column
    python scripts/deploys.py --json     # raw JSONL passthrough

The log starts empty until the first deploy after this script lands.
Historical deploys made before then are visible only via the Cloudflare
dashboard or ``wrangler pages deployment list --project-name lukesimmonsnz``.

This script is deliberately dependency-free — uses stdlib only, no Rich,
no Flask. The point is to read it cold in any terminal.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "deploys.jsonl"


def _read_log(limit: int = 10) -> list[dict]:
    if not LOG_FILE.exists():
        return []
    rows: list[dict] = []
    with LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # ignore corrupt lines, don't crash the viewer
    rows.reverse()  # newest first
    return rows[:limit]


def _fmt_when(iso: str) -> str:
    """Format the deploy timestamp into 'YYYY-MM-DD HH:MM' + ' (Nm ago)' or
    ' (Nh ago)' for the most recent.
    """
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return iso
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")


def _fmt_age(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return ""
    delta = datetime.now(timezone.utc) - dt
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def _fmt_status(row: dict) -> str:
    if row.get("exit", 0) == 0:
        return "ok"
    return f"FAIL ({row['exit']})"


def _fmt_changes(row: dict) -> str:
    new = row.get("files_uploaded")
    cached = row.get("files_cached")
    if new is None and cached is None:
        return "-"
    total = (new or 0) + (cached or 0)
    return f"{new or 0} new / {total} total"


def _fmt_urls(row: dict) -> str:
    ok = row.get("urls_ok")
    failed = row.get("urls_failed")
    if ok is None and failed is None:
        return "-"
    if failed:
        return f"{ok or 0} OK / {failed} FAIL"
    return str(ok or 0)


def _fmt_git(row: dict) -> str:
    sha = row.get("git_sha") or "—"
    if row.get("git_dirty"):
        return f"{sha} *"
    return sha


def _fmt_duration(row: dict) -> str:
    d = row.get("duration_s")
    if d is None:
        return "-"
    if d < 60:
        return f"{d:.0f}s"
    return f"{d/60:.1f}m"


def _print_table(rows: list[dict], full: bool) -> None:
    if not rows:
        print("No deploys logged yet.")
        print(f"  (log file: {LOG_FILE.relative_to(ROOT)})")
        print()
        print("Once you run scripts/deploy.py, entries will appear here.")
        print("To see deploys before this dashboard was added, use:")
        print("  wrangler pages deployment list --project-name lukesimmonsnz")
        return

    print(f"Cloudflare Pages deploys (lukesimmonsnz) - last {len(rows)}")
    print()

    headers = ["WHEN", "AGE", "STATUS", "CHANGES", "URLS", "DUR", "GIT"]
    if full:
        headers.append("PREVIEW URL")

    table: list[list[str]] = []
    for i, row in enumerate(rows):
        cells = [
            _fmt_when(row.get("ts", "")),
            _fmt_age(row.get("ts", "")),
            _fmt_status(row) + ("  <- live" if i == 0 and row.get("exit", 0) == 0 else ""),
            _fmt_changes(row),
            _fmt_urls(row),
            _fmt_duration(row),
            _fmt_git(row),
        ]
        if full:
            cells.append(row.get("preview_url") or "—")
        table.append(cells)

    # Compute column widths
    cols = list(zip(headers, *table))
    widths = [max(len(str(c)) for c in col) for col in cols]

    def _row(parts: list[str]) -> str:
        return "  ".join(p.ljust(w) for p, w in zip(parts, widths))

    print(_row(headers))
    print(_row(["-" * w for w in widths]))
    for r in table:
        print(_row(r))

    print()
    if not full:
        print("(Pass --full to also show preview URLs.)")
    if any(row.get("git_dirty") for row in rows):
        print("(* = deploy was made with uncommitted local changes - preview may differ from main.)")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="deploys",
        description="Show recent Cloudflare Pages deploys (from logs/deploys.jsonl).",
    )
    p.add_argument("--limit", "-n", type=int, default=10,
                   help="How many deploys to show (default: 10)")
    p.add_argument("--full", action="store_true",
                   help="Include preview URL column")
    p.add_argument("--json", action="store_true",
                   help="Output raw JSONL (one row per line) for piping")
    args = p.parse_args(argv)

    rows = _read_log(limit=args.limit)
    if args.json:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return 0

    _print_table(rows, full=args.full)
    return 0


if __name__ == "__main__":
    sys.exit(main())
