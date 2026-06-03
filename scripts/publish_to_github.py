"""publish_to_github.py — curated mirror-and-push to GitHub.

Workflow:

1. Read .gitignore + .publishignore to compute the exclusion set.
2. Walk source tree, build the list of files allowed to publish.
3. Run a content scan on those files looking for sensitive patterns
   (names, financial details, API keys, personal paths, off-allowlist
   emails). Hard blockers abort; warnings ask for confirmation.
4. Mirror the allowed files into ``../lukesimmonsnz-public/``,
   removing any files in the mirror that are no longer in the source
   publishable set.
5. ``git add -A`` in the mirror, show status, prompt for commit message.
6. ``git commit`` + ``git push origin main``.

Flags:
    --dry-run     Show what would be published; don't sync or commit.
    --force       Publish despite blockers / warnings (use carefully).
    --message M   Commit message (otherwise prompted).

Setup (one-time):
    cd D:/ai-website-manager
    git clone https://github.com/lukesimmonsnz/lukesimmonsnz.git lukesimmonsnz-public
    cd "Current website"
    git remote remove origin    # prevent accidental direct push
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = ROOT.parent / "lukesimmonsnz-public"
GITIGNORE = ROOT / ".gitignore"
PUBLISHIGNORE = ROOT / ".publishignore"

# ----------------------------------------------------------------------
# Content scan patterns
# ----------------------------------------------------------------------

# Hard blockers — refuse to publish unless --force.
SCAN_BLOCK = [
    # Sensitive names known from prior leak. Add more here as you discover them.
    (r"\bGallifrey\b",                            "name: Gallifrey"),
    (r"\bPLATT\b",                                "name: PLATT"),
    # Personal directory naming we don't want public.
    (r"D:[/\\]Luke[' ]?s Brain",                  "private path: Luke's Brain"),
    (r"D:[/\\]Gallifrey",                         "private path: Gallifrey"),
    (r"C:[/\\]Users[/\\]Luke Simmons[/\\]\.claude", "private path: .claude memory"),
    # API key shapes.
    (r"\bre_[A-Za-z0-9_]{25,}\b",                 "Resend-style API key"),
    (r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b", "GitHub token"),
    (r"\bsk-(ant|proj|live)-[A-Za-z0-9_-]{20,}\b", "OpenAI/Anthropic key"),
    (r"\bAKIA[0-9A-Z]{16}\b",                     "AWS access key"),
    (r"\bxoxb-[0-9]+-[A-Za-z0-9]+",               "Slack bot token"),
    # In-code assignments with real-looking values (not env lookups).
    (r"RESEND_API_KEY\s*=\s*['\"]?re_[A-Za-z0-9_]{25,}", "Resend key in code"),
    (r"TURNSTILE_SECRET_KEY\s*=\s*['\"]?0x[A-Za-z0-9_]{20,}", "Turnstile secret in code"),
]

# Warnings — printed, ask for confirmation, don't auto-block.
SCAN_WARN = [
    (r"\bfamily trust\b",         "phrase: family trust"),
    (r"\brental arrears\b",       "phrase: rental arrears"),
    (r"\btenant.{0,40}\bnamed?\b", "phrase: tenant named"),
    (r"\bback issues\b",          "phrase: back issues (possibly health-related)"),
    # Bank names + MATS are proper nouns — case-sensitive to avoid matching
    # lowercase 'nz', 'asb', 'mats' that appear in regex code (`\bnz\b`)
    # or compound words.
    (r"(?-i:\b(BNZ|ANZ|ASB|Westpac|Kiwibank)\b)", "NZ bank named"),
    (r"(?-i:\bMATS[- ]?fellowship\b)",  "MATS fellowship - was redacted previously"),
]

# Files to skip during the content scan. These files legitimately contain
# the pattern strings themselves (the scanner) or document them
# (the workflow note). Scanning them would only produce self-matches.
SCAN_SKIP_FILES = {
    "scripts/publish_to_github.py",
    "scripts/publish_to_github.bat",
    "docs/PUBLISH-WORKFLOW.md",
}

# Emails not on this allowlist are flagged as warnings.
EMAIL_ALLOWLIST = {
    "lukesimmonsnz@gmail.com",
    "lukesimmonsnz+form@gmail.com",
    "luke@lukesimmonsnz.kiwi",
    "form@lukesimmonsnz.kiwi",
    "cms@lukesimmonsnz.kiwi",
    "noreply@anthropic.com",
    "noreply@github.com",
}
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Text file extensions we'll actually scan. (Binary files get skipped.)
TEXT_EXTS = {
    ".md", ".txt", ".rst", ".py", ".pyi", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".htm", ".css", ".scss", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".sh", ".bat", ".ps1", ".xml", ".j2", ".jinja",
    ".env", ".example",  # template files
    ".gitignore", ".publishignore",
}


# ----------------------------------------------------------------------
# Ignore-pattern handling
# ----------------------------------------------------------------------

def _load_patterns(path: Path) -> list[str]:
    if not path.exists():
        return []
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Skip negation patterns for simplicity (gitignore's !pattern).
        # Our publish set is small enough we don't need them.
        if line.startswith("!"):
            continue
        out.append(line)
    return out


def _matches_pattern(rel_posix: str, pattern: str) -> bool:
    """Approximate gitignore semantics. Good enough for our cases."""
    pat = pattern.rstrip("/")
    is_dir_pattern = pattern.endswith("/")

    # Anchored to root if pattern starts with /
    anchored = pat.startswith("/")
    if anchored:
        pat = pat.lstrip("/")

    # Plain glob match against the full relpath
    if fnmatch.fnmatch(rel_posix, pat):
        return True
    # Match against directory prefix (covers `dir/` patterns)
    if is_dir_pattern:
        prefix = pat + "/"
        if rel_posix == pat or rel_posix.startswith(prefix):
            return True

    if not anchored:
        # Also match the pattern at any depth (gitignore's default behaviour
        # for patterns without a slash).
        if "/" not in pat:
            for part in rel_posix.split("/"):
                if fnmatch.fnmatch(part, pat):
                    return True
        # Or as a substring path component sequence at any depth
        for i in range(len(rel_posix.split("/"))):
            sub = "/".join(rel_posix.split("/")[i:])
            if fnmatch.fnmatch(sub, pat):
                return True
            if is_dir_pattern and (sub == pat or sub.startswith(pat + "/")):
                return True

    return False


def _is_ignored(rel_path: Path, patterns: list[str]) -> bool:
    rel_posix = rel_path.as_posix()
    return any(_matches_pattern(rel_posix, p) for p in patterns)


# ----------------------------------------------------------------------
# Walk + scan
# ----------------------------------------------------------------------

def collect_publish_files() -> list[Path]:
    patterns = _load_patterns(GITIGNORE) + _load_patterns(PUBLISHIGNORE)
    # Always exclude these regardless of files
    patterns.extend([".git/", ".git", ".publishignore.tmp"])

    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        # Quick reject: anything under .git
        if rel.parts and rel.parts[0] == ".git":
            continue
        if _is_ignored(rel, patterns):
            continue
        files.append(path)
    return files


def scan_files(files: list[Path]) -> tuple[list, list]:
    """Return (blockers, warnings) — each list of (file, line, desc, snippet)."""
    blockers: list = []
    warns: list = []

    for f in files:
        rel_posix = f.relative_to(ROOT).as_posix()
        if rel_posix in SCAN_SKIP_FILES:
            # Files that legitimately contain the scanner's pattern strings
            # (the scanner itself, its docs). Skipping avoids self-matches.
            continue
        if f.suffix.lower() not in TEXT_EXTS and not f.name.startswith("."):
            # Skip binary-ish files; scan only known text types.
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for pat, desc in SCAN_BLOCK:
            for m in re.finditer(pat, text):
                lineno = text[:m.start()].count("\n") + 1
                blockers.append((f, lineno, desc, m.group()))

        for pat, desc in SCAN_WARN:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                lineno = text[:m.start()].count("\n") + 1
                warns.append((f, lineno, desc, m.group()))

        for m in EMAIL_RE.finditer(text):
            email = m.group().lower()
            if email not in EMAIL_ALLOWLIST:
                lineno = text[:m.start()].count("\n") + 1
                warns.append((f, lineno, "email off allowlist", email))

    return blockers, warns


def _print_findings(label: str, findings: list, limit: int = 25) -> None:
    if not findings:
        return
    print(f"\n[publish] {label} ({len(findings)}):")
    for f, ln, desc, snippet in findings[:limit]:
        rel = f.relative_to(ROOT).as_posix()
        snip = snippet[:80].replace("\n", " ")
        # ASCII arrow — Windows cp1252 consoles can't render unicode arrows.
        print(f"  {rel}:{ln}  {desc}  ->  {snip}")
    if len(findings) > limit:
        print(f"  ... +{len(findings) - limit} more")


# ----------------------------------------------------------------------
# Sync to mirror
# ----------------------------------------------------------------------

def sync_to_mirror(files: list[Path]) -> dict:
    """Copy publishable files to mirror; remove files no longer in source set.

    Skips unchanged files (same mtime + size) for speed and to avoid
    permission errors on locked binaries. On PermissionError, makes the
    target writable and retries once; logs and skips if still failing.

    Returns a dict {copied, skipped_unchanged, skipped_locked, removed}.
    """
    import os, stat

    publish_rels = {f.relative_to(ROOT) for f in files}
    copied = 0
    skipped_unchanged = 0
    skipped_locked: list[str] = []
    removed = 0

    # Copy / update
    for src in files:
        rel = src.relative_to(ROOT)
        dst = MIRROR_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Skip unchanged files (fast path + avoids touching locked binaries).
        if dst.exists():
            try:
                ssrc = src.stat()
                sdst = dst.stat()
                if int(ssrc.st_mtime) == int(sdst.st_mtime) and ssrc.st_size == sdst.st_size:
                    skipped_unchanged += 1
                    continue
            except OSError:
                pass

        try:
            shutil.copy2(src, dst)
            copied += 1
        except PermissionError:
            # Try to clear read-only and retry.
            try:
                if dst.exists():
                    os.chmod(dst, stat.S_IWRITE)
                shutil.copy2(src, dst)
                copied += 1
            except (PermissionError, OSError) as exc:
                skipped_locked.append(f"{rel.as_posix()}  ({exc})")

    # Delete files in mirror that aren't in publish set
    for path in MIRROR_DIR.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(MIRROR_DIR)
        if rel.parts and rel.parts[0] == ".git":
            continue
        if rel not in publish_rels:
            path.unlink()
            removed += 1

    # Best-effort: prune empty dirs left after deletes
    for path in sorted(MIRROR_DIR.rglob("*"), key=lambda p: -len(p.parts)):
        if path.is_dir() and not any(path.iterdir()) and path.name != ".git":
            try:
                path.rmdir()
            except OSError:
                pass

    return {
        "copied": copied,
        "skipped_unchanged": skipped_unchanged,
        "skipped_locked": skipped_locked,
        "removed": removed,
    }


# ----------------------------------------------------------------------
# Git ops in the mirror
# ----------------------------------------------------------------------

def _git(args: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(MIRROR_DIR), *args],
        check=check, capture_output=capture, text=True,
        # Force UTF-8 + replace-on-error so unicode in file paths or
        # commit messages doesn't crash on a Windows cp1252 console.
        encoding="utf-8", errors="replace",
    )


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Publish curated source tree to the GitHub mirror.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen; don't sync or push.")
    parser.add_argument("--force", action="store_true", help="Publish despite blockers / warnings.")
    parser.add_argument("--message", "-m", help="Commit message (otherwise prompted).")
    args = parser.parse_args()

    if not MIRROR_DIR.exists():
        print(f"[publish] Mirror not found at {MIRROR_DIR}.", file=sys.stderr)
        print("           Set it up once:", file=sys.stderr)
        print("           cd D:/ai-website-manager", file=sys.stderr)
        print("           git clone https://github.com/lukesimmonsnz/lukesimmonsnz.git lukesimmonsnz-public", file=sys.stderr)
        return 1
    if not (MIRROR_DIR / ".git").exists():
        print(f"[publish] Mirror exists but isn't a git repo: {MIRROR_DIR}", file=sys.stderr)
        return 1

    print(f"[publish] Source: {ROOT}")
    print(f"[publish] Mirror: {MIRROR_DIR}")
    print()

    print("[publish] Collecting publishable files...")
    files = collect_publish_files()
    print(f"[publish] {len(files)} files in publish set.")

    print("[publish] Scanning for sensitive content...")
    blockers, warns = scan_files(files)
    _print_findings("BLOCKING findings", blockers)
    _print_findings("Warnings", warns)

    if blockers and not args.force:
        print("\n[publish] Aborted by blocker(s). Fix them or re-run with --force.")
        return 2

    if warns and not args.force and not args.dry_run:
        print()
        ans = input("[publish] Continue despite warnings? [y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            print("[publish] Aborted by user.")
            return 0

    if args.dry_run:
        print("\n[publish] --dry-run; not syncing, not committing, not pushing.")
        return 0

    print(f"\n[publish] Syncing to mirror...")
    stats = sync_to_mirror(files)
    print(
        f"[publish] copied={stats['copied']} "
        f"unchanged={stats['skipped_unchanged']} "
        f"removed={stats['removed']} "
        f"locked={len(stats['skipped_locked'])}"
    )
    if stats["skipped_locked"]:
        print("[publish] WARN — files locked or unwritable; not copied:")
        for entry in stats["skipped_locked"][:10]:
            print(f"  {entry}")
        if len(stats["skipped_locked"]) > 10:
            print(f"  ... +{len(stats['skipped_locked']) - 10} more")

    _git(["add", "-A"])
    status = _git(["status", "--short"]).stdout
    if not status.strip():
        print("[publish] No changes vs current mirror state. Nothing to commit.")
        return 0

    print("\n[publish] Mirror status preview:")
    for line in status.splitlines()[:40]:
        print(f"  {line}")
    if len(status.splitlines()) > 40:
        print(f"  ... +{len(status.splitlines()) - 40} more")

    msg = args.message
    if not msg:
        msg = input("\n[publish] Commit message: ").strip()
        if not msg:
            print("[publish] Empty message; aborting (changes left staged in mirror).")
            return 0

    _git(["commit", "-m", msg])
    print("\n[publish] Pushing to GitHub...")
    push = _git(["push", "origin", "main"], capture=False)
    if push.returncode != 0:
        print(f"[publish] git push failed (exit {push.returncode}).")
        return push.returncode

    print("[publish] Done. https://github.com/lukesimmonsnz/lukesimmonsnz")
    return 0


if __name__ == "__main__":
    sys.exit(main())
