"""Delete the most recent draft weekly digest.

The opposite of ``publish_weekly.py``. Finds the most recent
``content/blog/*-weekly-digest.md`` with ``status: draft`` and deletes
it, after a confirmation prompt. Use ``--yes`` to skip the prompt
(suitable for non-interactive contexts).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "content" / "blog"


def find_draft() -> Path | None:
    candidates = sorted(BLOG_DIR.glob("*-weekly-digest.md"), reverse=True)
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^status:\s*draft\s*$", text, flags=re.MULTILINE):
            return path
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete the most recent draft weekly digest."
    )
    parser.add_argument(
        "--yes", action="store_true",
        help="Skip the confirmation prompt.",
    )
    args = parser.parse_args()

    draft = find_draft()
    if draft is None:
        print("[reject] No draft weekly digest found in content/blog/.")
        return 1

    print(f"[reject] Will DELETE: {draft.name}")
    if not args.yes:
        try:
            answer = input("Confirm? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("[reject] Aborted.")
            return 0

    draft.unlink()
    print(f"[reject] Deleted {draft.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
