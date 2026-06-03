"""Full deploy pipeline: freeze → merge archives → wrangler deploy.

Prints a top-of-output banner showing what's running, what to expect, and
the git state being deployed — so you don't have to wonder mid-run whether
something is happening. A background ticker prints a one-line progress
update every 10 seconds during the freeze step (which is otherwise silent
for several minutes).

Expected runtime: roughly 3–5 minutes total.
  Step 1/3 (freeze):           3–4 min  (silent — ticker fires every 10s)
  Step 2/3 (merge archives):   <1 sec   (skipped if no archives/ dir)
  Step 3/3 (wrangler deploy):  ~10 sec  (live upload-progress output)

Each run appends one JSONL row to ``logs/deploys.jsonl`` so
``scripts/deploys.py`` can render a history dashboard. The row captures
URL counts from freeze, file counts from wrangler, the preview URL, the
git SHA at time of deploy, and total wall-clock duration.

Usage
-----
    python scripts/deploy.py
    python scripts/deploys.py     # view the dashboard afterward

Environment variables
---------------------
    SITE_URL            Base URL (default: https://lukesimmonsnz.kiwi)
    CONTACT_SUBMIT_URL  Contact form POST target (default: /api/contact)
    TURNSTILE_SITE_KEY  Cloudflare Turnstile site key (optional)

The Cloudflare credentials used by wrangler are taken from the system's
wrangler login state (``wrangler login`` must have been run once).  In CI
set ``CLOUDFLARE_API_TOKEN`` and ``CLOUDFLARE_ACCOUNT_ID`` as env vars
instead.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"
ARCHIVES_SRC = ROOT / "archives"
SITE_ARCHIVES_DST = SITE_DIR / "archives"
LOG_FILE = ROOT / "logs" / "deploys.jsonl"


# ── subprocess helpers ─────────────────────────────────────────────────────

def run(cmd: list[str], **kwargs) -> str:
    """Run a command; tee output to stdout AND return it as a string.

    Exits 1 on non-zero return. The captured string is what the parsers
    below scan for stats (URL counts, file counts, preview URL).
    """
    print(f"[deploy] $ {' '.join(cmd)}")
    # Force UTF-8 decoding with replacement on the captured stream — wrangler
    # emits Unicode glyphs (✨, ⛅, →) that Windows' default cp1252 can't decode
    # and a UnicodeDecodeError mid-tee crashes the entire deploy mid-step.
    proc = subprocess.Popen(
        cmd, cwd=str(ROOT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        bufsize=1, **kwargs,
    )
    chunks: list[str] = []
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        chunks.append(line)
    proc.wait()
    if proc.returncode != 0:
        print(f"[deploy] Command failed (exit {proc.returncode}).", file=sys.stderr)
        sys.exit(proc.returncode)
    return "".join(chunks)


def _git_info() -> dict:
    """Capture git SHA + dirty state at the moment of deploy."""
    def _git(*args: str) -> str:
        try:
            r = subprocess.run(
                ["git", *args],
                cwd=str(ROOT), capture_output=True, text=True, check=False,
            )
            return r.stdout.strip()
        except OSError:
            return ""

    sha = _git("rev-parse", "--short", "HEAD")
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    # `git diff --quiet HEAD` exits 0 if working tree matches HEAD, 1 if dirty.
    dirty_check = subprocess.run(
        ["git", "diff", "--quiet", "HEAD"],
        cwd=str(ROOT), capture_output=True, check=False,
    )
    return {"sha": sha, "branch": branch, "dirty": dirty_check.returncode != 0}


# ── progress UI ────────────────────────────────────────────────────────────

def _print_banner(git: dict) -> None:
    """Top-of-output banner — what's running, what to expect, git state.

    Visible immediately when you run the script so you're never staring at
    a blank terminal wondering if it started.
    """
    dirty_tag = "  (DIRTY — uncommitted changes)" if git.get("dirty") else ""
    sha = git.get("sha") or "?"
    branch = git.get("branch") or "?"
    bar = "=" * 70
    print()
    print(f"[deploy] {bar}")
    print(f"[deploy]  Cloudflare Pages deploy → lukesimmonsnz.kiwi")
    print(f"[deploy]  git: {sha} on {branch}{dirty_tag}")
    print(f"[deploy]  Expected: freeze ~3-4 min  ·  merge instant  ·  wrangler ~10 sec")
    print(f"[deploy]  Progress ticks every 10 seconds while freeze runs (it's silent otherwise).")
    print(f"[deploy]  Run scripts/deploys.py afterward to see the dashboard row.")
    print(f"[deploy] {bar}")
    print()


def _freeze_progress_ticker(stop_event: threading.Event, start_time: float) -> None:
    """Tick every 10 seconds while freeze is silent.

    Reads the live `_site/` HTML count so the user can see frozen-URL
    progress climbing. Stops the instant `stop_event` is set. Daemon
    thread so it can't outlive the main process even if something else
    explodes.
    """
    while not stop_event.wait(10):
        elapsed = int(time.monotonic() - start_time)
        try:
            count = sum(1 for _ in SITE_DIR.rglob("*.html"))
        except OSError:
            count = 0
        print(f"[deploy]   … freeze in progress: {count} URLs rendered "
              f"({elapsed}s elapsed)", flush=True)


# ── pipeline steps ─────────────────────────────────────────────────────────

def step_freeze() -> str:
    """Build _site/ from the Flask app. Returns captured output.

    Spawns a background ticker that prints a one-line progress update every
    10 seconds while freeze runs (which is otherwise silent for ~3 minutes
    and looks indistinguishable from a hung process).
    """
    env = dict(os.environ)
    env.setdefault("SITE_URL", "https://lukesimmonsnz.kiwi")
    env.setdefault("CONTACT_SUBMIT_URL", "/api/contact")

    stop = threading.Event()
    ticker = threading.Thread(
        target=_freeze_progress_ticker,
        args=(stop, time.monotonic()),
        daemon=True,
    )
    ticker.start()
    try:
        return run([sys.executable, str(ROOT / "scripts" / "freeze.py")], env=env)
    finally:
        stop.set()
        ticker.join(timeout=2)


def step_merge_archives() -> None:
    """Copy archives/ → _site/archives/ so Cloudflare Pages serves them."""
    if not ARCHIVES_SRC.exists() or not any(ARCHIVES_SRC.iterdir()):
        print("[deploy] No archives/ snapshots found; skipping merge.")
        return

    SITE_ARCHIVES_DST.mkdir(parents=True, exist_ok=True)
    quarters = sorted(d for d in ARCHIVES_SRC.iterdir() if d.is_dir())

    for quarter_dir in quarters:
        dst = SITE_ARCHIVES_DST / quarter_dir.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(quarter_dir, dst)
        file_count = sum(1 for _ in dst.rglob("*") if _.is_file())
        print(f"[deploy] Merged archive {quarter_dir.name}/ → _site/archives/ ({file_count} files)")

    print(f"[deploy] Archives merged: {[d.name for d in quarters]}")


def _resolve_wrangler() -> str:
    """Find an executable wrangler path.

    On Windows, npm-installed CLIs are ``.cmd`` shims that
    ``subprocess.run`` cannot find via PATH lookup unless ``shell=True``
    or the full filename is given. Resolve via ``shutil.which`` first
    (handles PATHEXT properly), then fall back to the bare name.
    """
    found = shutil.which("wrangler")
    if found:
        return found
    if os.name == "nt":
        found = shutil.which("wrangler.cmd")
        if found:
            return found
    return "wrangler"


def step_wrangler_deploy() -> str:
    """Push _site/ to Cloudflare Pages. Returns captured output."""
    wrangler = _resolve_wrangler()
    return run([wrangler, "pages", "deploy", "_site", "--project-name", "lukesimmonsnz"])


# ── stats parsers ──────────────────────────────────────────────────────────
# Regex against the actual deploy output we tail. Brittle if either tool
# changes its log format — defensive `None` returns mean partial stats
# rather than the dashboard breaking.

_RE_URLS_TO_RENDER = re.compile(r"\[freeze\] (\d+) URLs to render")
_RE_URLS_DONE = re.compile(r"\[freeze\] done\.\s+(\d+) OK,\s+(\d+) failed\.")
_RE_WRANGLER_UPLOAD = re.compile(
    r"Uploaded (\d+) files? \((\d+) already uploaded\) \(([\d.]+) sec\)"
)
_RE_PREVIEW_URL = re.compile(r"(https://[a-f0-9]+\.lukesimmonsnz\.pages\.dev)")


def _parse_freeze(out: str) -> dict:
    stats: dict = {}
    if m := _RE_URLS_TO_RENDER.search(out):
        stats["urls_to_render"] = int(m.group(1))
    if m := _RE_URLS_DONE.search(out):
        stats["urls_ok"] = int(m.group(1))
        stats["urls_failed"] = int(m.group(2))
    return stats


def _parse_wrangler(out: str) -> dict:
    stats: dict = {}
    if m := _RE_WRANGLER_UPLOAD.search(out):
        stats["files_uploaded"] = int(m.group(1))
        stats["files_cached"] = int(m.group(2))
        stats["wrangler_seconds"] = float(m.group(3))
    if m := _RE_PREVIEW_URL.search(out):
        stats["preview_url"] = m.group(1)
    return stats


# ── logging ────────────────────────────────────────────────────────────────

def _log_deploy(row: dict) -> None:
    """Append one JSONL row to logs/deploys.jsonl. Best-effort."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[deploy] WARN: could not write deploy log: {e}", file=sys.stderr)


# ── main ───────────────────────────────────────────────────────────────────

def main() -> int:
    # Force the tee output stream to UTF-8 so wrangler's Unicode glyphs
    # (✨, ⛅, →) don't crash sys.stdout.write on Windows cp1252 consoles.
    # The decode side is already handled in run() via encoding="utf-8".
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass  # not a stream that supports reconfigure; not fatal

    t0 = time.monotonic()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    git = _git_info()
    _print_banner(git)

    print("[deploy] Step 1/3: freeze")
    freeze_out = step_freeze()
    print("[deploy] Step 2/3: merge archives")
    step_merge_archives()
    print("[deploy] Step 3/3: wrangler deploy")
    wrangler_out = step_wrangler_deploy()

    duration_s = round(time.monotonic() - t0, 2)
    row = {
        "ts": started_iso,
        "exit": 0,
        "duration_s": duration_s,
        "git_sha": git["sha"],
        "git_branch": git["branch"],
        "git_dirty": git["dirty"],
        **_parse_freeze(freeze_out),
        **_parse_wrangler(wrangler_out),
    }
    _log_deploy(row)
    preview = row.get("preview_url") or "(no preview URL parsed)"
    print()
    print(f"[deploy] DONE in {duration_s:.0f}s.")
    print(f"[deploy]   preview: {preview}")
    print(f"[deploy]   logged:  {LOG_FILE.relative_to(ROOT)}")
    print(f"[deploy]   view:    .venv\\Scripts\\python.exe scripts\\deploys.py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        # If a pipeline step exited non-zero, log the failure too — same
        # row shape, just with the exit code populated. We don't have the
        # captured outputs in this path, so the stat fields are absent.
        code = e.code if isinstance(e.code, int) else 1
        if code != 0:
            try:
                _log_deploy({
                    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "exit": code,
                    "git_sha": _git_info()["sha"],
                })
            except Exception:
                pass
        raise
