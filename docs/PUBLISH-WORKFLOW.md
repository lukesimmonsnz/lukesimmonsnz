# Publishing to GitHub

The repo at <https://github.com/lukesimmonsnz/lukesimmonsnz> is *not* pushed
to directly from this workspace. Instead, a dedicated **mirror directory**
at `D:/ai-website-manager/lukesimmonsnz-public/` holds only the
publication-safe subset of files, and a script syncs + scans + pushes
from there.

## Layout

```
D:/ai-website-manager/
├── Current website/                ← work here. Full state incl. private notes.
│   ├── .git/                       ← local-only history (no origin remote).
│   ├── .gitignore                  ← excludes secrets, drafts, build output.
│   ├── .publishignore              ← extra "tracked locally, never publish".
│   ├── docs/BRIEFING-*.md          ← private; gitignored AND publishignored.
│   ├── docs/MONETIZATION.md        ← private.
│   ├── content/auckland/briefings/ ← private.
│   └── scripts/publish_to_github.py  ← the publish script.
│
└── lukesimmonsnz-public/           ← curated mirror. Pushes to GitHub.
    ├── .git/                       ← origin = lukesimmonsnz/lukesimmonsnz
    └── (only the publishable subset of files)
```

## Day-to-day

When you have changes ready to ship:

```
scripts\publish_to_github.bat
```

That runs `publish_to_github.py`, which:

1. Reads `.gitignore` + `.publishignore` to build the exclusion set.
2. Walks `Current website/` and collects the files allowed to publish.
3. Scans those files for sensitive patterns:
   - **Blockers** (refuse to publish): named individuals known to be private,
     personal paths like `D:/Luke's Brain/`, API key shapes (`re_…`, `ghp_…`,
     `sk-ant-…`, `AKIA…`), in-code secret assignments.
   - **Warnings** (prompt to confirm): bank names, "family trust",
     "rental arrears", "back issues", off-allowlist email addresses.
4. Mirrors the allowed files into `lukesimmonsnz-public/`, deleting any
   stale files no longer in the source publish set.
5. Stages everything (`git add -A`) and shows the mirror's `git status`.
6. Asks you for a commit message.
7. Commits and pushes to GitHub.

## Flags

```
scripts\publish_to_github.bat --dry-run        # show what would happen
scripts\publish_to_github.bat --force          # publish despite blockers
scripts\publish_to_github.bat -m "fix typo"    # skip commit-message prompt
```

`--force` exists for cases where a pattern is a false positive (a research
claim that legitimately mentions "$200/km", a quote that says "back issues"
in a clearly non-personal context, etc.). Use it after reading the
findings list.

## When you find a new pattern that should be blocked

Edit `scripts/publish_to_github.py`:

- `SCAN_BLOCK` — refuse to publish on a match
- `SCAN_WARN` — print and require confirmation on a match
- `EMAIL_ALLOWLIST` — addresses considered fine to appear in published content

Then run `--dry-run` to confirm the new pattern fires where you expect.

## When you want to add a path to the "never publish" list

Add it to `.publishignore` (gitignore-style patterns). Re-run the publish
script; the next push will drop those files from the mirror.

## Setup (one-time, already done)

```
cd D:/ai-website-manager
git clone https://github.com/lukesimmonsnz/lukesimmonsnz.git lukesimmonsnz-public
cd "Current website"
git remote remove origin
```

After that, `Current website/` has no `origin` remote — `git push` from
there errors out, by design. The only path to GitHub is the publish script.

## Why this exists

On 2026-06-03 a catch-up commit was force-pushed to GitHub containing
named third-party financial details inside `docs/CHANGELOG.md` that
should never have left the local workspace. The leak was scrubbed via
`commit --amend` + force-push, but the orphaned commit remained
reachable by SHA for a window before GitHub's garbage collection ran.

The dedicated-mirror pattern makes that class of mistake much harder:

- Sensitive files literally do not exist in the mirror directory;
  there's no `.gitignore` entry that could miss them.
- The content scan provides a second backstop for patterns rather than
  paths (the original leak was inside a tracked file, not a gitignored
  one — `.gitignore` alone could not have prevented it).
- `git push` from the source workspace is impossible (no remote), so
  muscle-memory `git push` cannot leak.
