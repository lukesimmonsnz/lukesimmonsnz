"""Promote the most recent draft weekly digest and deploy.

The weekly agent writes posts with ``status: draft`` so they can't
accidentally hit production. This script:

1. Finds the most recent ``content/blog/*-weekly-digest.md`` whose
   frontmatter has ``status: draft``.
2. Runs structural lint (frontmatter fields present, body length
   sensible, slug not colliding with another published post).
3. Strips the ``status: draft`` line from the frontmatter.
4. Hands off to ``scripts/deploy.bat`` for the freeze + wrangler push.

Failure modes:

- No draft found → exit 1 (nothing to do).
- Lint fails → exit 2, file left untouched. Use ``--force`` to override.
- Deploy fails → exit code from deploy.bat, file is already promoted.
  (Re-run ``scripts/deploy.bat`` to retry the push.)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "content" / "blog"
DEPLOY_BAT = ROOT / "scripts" / "deploy.bat"

sys.path.insert(0, str(ROOT))
from agent._env import load_dotenv  # noqa: E402

load_dotenv()

MIN_WORDS = 200
MAX_WORDS = 2000


def find_draft() -> Path | None:
    """Most recent weekly-digest file with status=draft in frontmatter."""
    candidates = sorted(BLOG_DIR.glob("*-weekly-digest.md"), reverse=True)
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^status:\s*draft\s*$", text, flags=re.MULTILINE):
            return path
    return None


def lint(path: Path) -> list[str]:
    """Return a list of lint failure messages. Empty list = clean."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    # Split frontmatter from body.
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    if not m:
        errors.append("No YAML frontmatter block found.")
        return errors
    fm_block, body = m.group(1), m.group(2)

    for required in ("title:", "date:", "summary:", "tags:"):
        if not re.search(rf"^{required}", fm_block, flags=re.MULTILINE):
            errors.append(f"Frontmatter missing field: {required.rstrip(':')}")

    word_count = len(body.split())
    if word_count < MIN_WORDS:
        errors.append(f"Body is too short ({word_count} words; min {MIN_WORDS}).")
    if word_count > MAX_WORDS:
        errors.append(f"Body is suspiciously long ({word_count} words; max {MAX_WORDS}).")

    # Slug collision: any other file with same stem (shouldn't happen,
    # but check for typos / manual edits). Compare resolved paths so
    # relative-vs-absolute Path inputs don't false-positive.
    self_resolved = path.resolve()
    twins = [
        p for p in BLOG_DIR.glob("*.md")
        if p.stem == path.stem and p.resolve() != self_resolved
    ]
    if twins:
        errors.append(f"Slug collision with: {[p.name for p in twins]}")

    return errors


def strip_draft_status(path: Path) -> None:
    """Remove the `status: draft` line from frontmatter. Idempotent."""
    text = path.read_text(encoding="utf-8")
    new_text = re.sub(r"^status:\s*draft\s*\n", "", text, flags=re.MULTILINE)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote the latest draft weekly digest and deploy."
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Promote and deploy even if lint fails.",
    )
    parser.add_argument(
        "--no-deploy", action="store_true",
        help="Flip status only; skip the freeze/wrangler step.",
    )
    args = parser.parse_args()

    draft = find_draft()
    if draft is None:
        print("[publish] No draft weekly digest found in content/blog/.")
        print("          Run agent\\run_weekly.bat first, or check that the file")
        print("          actually has 'status: draft' in its frontmatter.")
        return 1

    print(f"[publish] Found draft: {draft.name}")

    errors = lint(draft)
    if errors:
        print("[publish] Lint failures:")
        for e in errors:
            print(f"          - {e}")
        if not args.force:
            print("[publish] Aborting. Re-run with --force to override.")
            return 2
        print("[publish] --force given; continuing despite lint failures.")
    else:
        print("[publish] Lint: clean.")

    strip_draft_status(draft)
    print(f"[publish] Removed 'status: draft' from {draft.name}.")

    if args.no_deploy:
        print("[publish] --no-deploy given; skipping deploy step.")
        print("          Run scripts\\deploy.bat manually to push.")
        return 0

    print(f"[publish] Invoking {DEPLOY_BAT.name} ...")
    proc = subprocess.run(
        [str(DEPLOY_BAT)],
        cwd=str(ROOT),
        shell=True,
    )
    if proc.returncode != 0:
        print(f"[publish] Deploy returned exit code {proc.returncode}.")
        print("          Frontmatter is already flipped. Re-run scripts\\deploy.bat to retry.")
        return proc.returncode

    print(f"[publish] Done. {draft.name} is live at https://lukesimmonsnz.kiwi/blog/{draft.stem}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
