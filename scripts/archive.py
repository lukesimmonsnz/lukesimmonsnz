"""Quarterly archive script — SEP pattern.

Produces an immutable snapshot of the current live build under
``archives/YYYY-QN/``.  The archive directory is committed to git and
merged into ``_site/archives/`` at deploy time, so Cloudflare Pages
serves it at ``/archives/YYYY-QN/...``.

Immutability contract
---------------------
Once created, an archive directory is *never* overwritten.  The script
exits with code 2 if the target quarter already exists.  Pass
``--force`` only in exceptional circumstances (e.g., fixing a corrupt
archive immediately after the quarterly job ran).

Usage
-----
    # Auto-detect current quarter and archive
    python scripts/archive.py

    # Archive a specific quarter (manual backfill)
    python scripts/archive.py --quarter 2026-Q2

    # Force-overwrite (emergency use only)
    python scripts/archive.py --quarter 2026-Q2 --force

Quarter labels
--------------
    Q1 = Jan–Mar   Q2 = Apr–Jun   Q3 = Jul–Sep   Q4 = Oct–Dec
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"
ARCHIVES_DIR = ROOT / "archives"


# ---------------------------------------------------------------------------
# Quarter helpers
# ---------------------------------------------------------------------------

def current_quarter() -> str:
    """Return the label for the calendar quarter containing today (UTC)."""
    now = datetime.now(tz=timezone.utc)
    q = math.ceil(now.month / 3)
    return f"{now.year}-Q{q}"


def validate_quarter(label: str) -> str:
    """Raise ValueError if *label* does not match YYYY-QN format."""
    import re
    if not re.fullmatch(r"\d{4}-Q[1-4]", label):
        raise ValueError(
            f"Quarter label must match YYYY-QN (e.g. 2026-Q2), got: {label!r}"
        )
    return label


# ---------------------------------------------------------------------------
# Build helpers
# ---------------------------------------------------------------------------

def run_freeze() -> None:
    """Run scripts/freeze.py to produce a fresh _site/ build."""
    import os
    env = dict(os.environ)
    env.setdefault("SITE_URL", "https://lukesimmonsnz.kiwi")
    env.setdefault("CONTACT_SUBMIT_URL", "/api/contact")

    print("[archive] Running freeze.py …")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "freeze.py")],
        env=env,
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        print(f"[archive] freeze.py exited {result.returncode}. Aborting.", file=sys.stderr)
        sys.exit(result.returncode)
    print("[archive] freeze.py done.")


# ---------------------------------------------------------------------------
# Archive helpers
# ---------------------------------------------------------------------------

def _is_archive_child(path: Path, archives_dir: Path) -> bool:
    """True iff *path* is inside *archives_dir* (avoid recursive copies)."""
    try:
        path.relative_to(archives_dir)
        return True
    except ValueError:
        return False


def copy_build_to_archive(quarter: str, force: bool = False) -> Path:
    """Copy ``_site/`` → ``archives/<quarter>/``.

    Excludes the ``_site/archives/`` subtree (if present from a previous
    merged deploy) to prevent infinite nesting.

    Returns the destination path.
    """
    dest = ARCHIVES_DIR / quarter
    site_archives = SITE_DIR / "archives"

    if dest.exists():
        if force:
            print(f"[archive] WARNING: force-overwriting existing archive {dest}")
            shutil.rmtree(dest)
        else:
            print(
                f"[archive] Archive {quarter} already exists at {dest}.\n"
                f"          Use --force to overwrite (emergency use only).",
                file=sys.stderr,
            )
            sys.exit(2)

    if not SITE_DIR.exists():
        print(
            f"[archive] _site/ does not exist. Run freeze.py first or "
            f"pass --freeze.",
            file=sys.stderr,
        )
        sys.exit(1)

    dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    for src_path in SITE_DIR.rglob("*"):
        if src_path.is_dir():
            continue
        # Skip the archives subtree inside _site/ to avoid recursion.
        if _is_archive_child(src_path, site_archives):
            skipped += 1
            continue
        rel = src_path.relative_to(SITE_DIR)
        dst_path = dest / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        copied += 1

    print(f"[archive] Archived {copied} files to {dest}/ (skipped {skipped} archive files).")
    return dest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Quarterly archive (SEP pattern).")
    parser.add_argument(
        "--quarter",
        metavar="YYYY-QN",
        help="Quarter to archive (default: auto-detect from current date).",
    )
    parser.add_argument(
        "--freeze",
        action="store_true",
        default=False,
        help="Run scripts/freeze.py before archiving (rebuilds _site/).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Overwrite an existing archive (emergency use only).",
    )
    args = parser.parse_args()

    quarter = validate_quarter(args.quarter) if args.quarter else current_quarter()
    print(f"[archive] Target quarter: {quarter}")

    if args.freeze:
        run_freeze()

    dest = copy_build_to_archive(quarter, force=args.force)
    print(f"[archive] Done. Snapshot at archives/{quarter}/")
    print(f"[archive] Commit this directory to git to make the archive permanent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
