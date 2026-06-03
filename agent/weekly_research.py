"""
Weekly research-corpus maintenance.

Runs alongside the weekly blog post (called from agent/run_weekly.bat).
Does the deterministic, no-judgement work that keeps the typed-graph
corpus and rendered pages in sync — and surfaces draft research proposals
from a watchlist of monitored URLs without ever auto-publishing.

Steps in order:

    1. Lint pass across all 16 regions. Any failure aborts.
    2. Regenerate consolidated section essays for every region.
    3. Process agent/watchlist.txt: for each `<region>\\t<theme>\\t<url>`
       line, call scripts/ingest_external_research.py to deposit claim
       and source stubs under content/<region>/data/_drafts/<timestamp>/.
       The PI reviews drafts manually before promoting to the live corpus.
    4. Write a structured log entry to agent/logs/weekly_research.log.

Editorial firewall: this script never modifies a live claim or source
file. Watchlist results are always written to _drafts/.

Exit codes:
    0  success (lint clean, essays regenerated, drafts written if any)
    1  lint failed (one or more regions report errors)
    2  essay regeneration failed
    3  watchlist parse error
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "agent" / "logs"
LOG_FILE = LOG_DIR / "weekly_research.log"
WATCHLIST = ROOT / "agent" / "watchlist.txt"
INGEST_SCRIPT = ROOT / "scripts" / "ingest_external_research.py"
ESSAY_SCRIPT = ROOT / "scripts" / "generate_section_essays.py"
AUCKLAND_RENDER = ROOT / "content" / "auckland" / "tools" / "render.py"

REGIONS = [
    "auckland", "wellington", "northland", "waikato", "bay-of-plenty",
    "gisborne", "hawkes-bay", "taranaki", "manawatu-whanganui", "nelson",
    "tasman", "marlborough", "west-coast", "canterbury", "otago", "southland",
]


def _python() -> str:
    """Path to the venv python — the one that has the project's deps."""
    win = ROOT / ".venv" / "Scripts" / "python.exe"
    nix = ROOT / ".venv" / "bin" / "python"
    return str(win if win.exists() else nix)


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def lint_all() -> tuple[bool, dict]:
    """Lint every region. Returns (ok, per-region-summary)."""
    summary: dict[str, str] = {}
    all_ok = True
    for region in REGIONS:
        lint_path = ROOT / "content" / region / "tools" / "lint.py"
        if not lint_path.is_file():
            summary[region] = "no-lint"
            continue
        proc = _run([_python(), str(lint_path)])
        last = (proc.stdout or proc.stderr).strip().splitlines()[-1] if (proc.stdout or proc.stderr).strip() else ""
        if proc.returncode != 0 or "0 schema errors" not in last:
            all_ok = False
            summary[region] = f"FAIL: {last[:120]}"
        else:
            summary[region] = last
    return all_ok, summary


def regenerate_essays() -> tuple[bool, dict]:
    """Re-render all consolidated section essays. 15 non-Auckland regions
    via scripts/generate_section_essays.py; Auckland via its own pipeline."""
    out: dict[str, str] = {}

    # 15 non-Auckland regions
    proc = _run([_python(), str(ESSAY_SCRIPT)])
    out["non_auckland"] = proc.stdout.strip()[-400:] if proc.stdout else ""
    if proc.returncode != 0:
        out["non_auckland_error"] = (proc.stderr or "")[-400:]
        return False, out

    # Auckland uses its own --all-sections in its tools/
    proc = _run([_python(), str(AUCKLAND_RENDER), "--all-sections"])
    out["auckland"] = proc.stdout.strip()[-400:] if proc.stdout else ""
    if proc.returncode != 0:
        out["auckland_error"] = (proc.stderr or "")[-400:]
        return False, out

    return True, out


def parse_watchlist(path: Path) -> list[tuple[str, str, str]]:
    """Each non-blank, non-comment line is `region\\ttheme\\turl`."""
    if not path.is_file():
        return []
    items: list[tuple[str, str, str]] = []
    for ln, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = [p.strip() for p in s.split("\t")]
        if len(parts) != 3 or not all(parts):
            raise ValueError(
                f"watchlist.txt:{ln}: expected '<region>\\t<theme>\\t<url>', "
                f"got: {raw!r}"
            )
        region, theme, url = parts
        if region not in REGIONS:
            raise ValueError(f"watchlist.txt:{ln}: unknown region '{region}'")
        items.append((region, theme, url))
    return items


def run_watchlist(items: list[tuple[str, str, str]]) -> dict:
    """For each watchlist entry, run the ingestion CLI to deposit a draft.
    Each draft lands in content/<region>/data/_drafts/<timestamp>/.
    Returns a per-URL summary dict for the log."""
    out: dict = {"items": [], "errors": []}
    for region, theme, url in items:
        cmd = [
            _python(), str(INGEST_SCRIPT), url,
            "--region", region,
            "--theme", theme,
        ]
        # Allow Ollama if reachable; the script falls back to heuristic.
        if os.environ.get("OLLAMA_HOST"):
            cmd.append("--ollama")
        proc = _run(cmd)
        if proc.returncode != 0:
            out["errors"].append({
                "region": region,
                "theme":  theme,
                "url":    url,
                "stderr": (proc.stderr or "")[-300:],
            })
            continue
        out["items"].append({
            "region": region,
            "theme":  theme,
            "url":    url,
            "summary": (proc.stdout or "").strip().splitlines()[-1][:200],
        })
    return out


def append_log(payload: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> int:
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    payload: dict = {"started": started}

    # 1. Lint sweep — must be clean before doing anything else.
    print("[weekly_research] linting all 16 regions ...")
    lint_ok, lint_summary = lint_all()
    payload["lint"] = lint_summary
    if not lint_ok:
        payload["status"] = "lint_failed"
        append_log(payload)
        for region, line in lint_summary.items():
            print(f"  {region}: {line}")
        print("[weekly_research] aborting: lint not clean")
        return 1

    # 2. Regenerate consolidated essays.
    print("[weekly_research] regenerating section essays ...")
    essays_ok, essays_summary = regenerate_essays()
    payload["essays"] = essays_summary
    if not essays_ok:
        payload["status"] = "essays_failed"
        append_log(payload)
        print("[weekly_research] aborting: essay regeneration failed")
        return 2

    # 3. Process the watchlist (optional, never required).
    print("[weekly_research] processing watchlist ...")
    try:
        items = parse_watchlist(WATCHLIST)
    except ValueError as exc:
        payload["status"] = "watchlist_parse_error"
        payload["error"] = str(exc)
        append_log(payload)
        print(f"[weekly_research] watchlist parse error: {exc}")
        return 3
    if items:
        watchlist_summary = run_watchlist(items)
        payload["watchlist"] = watchlist_summary
        print(f"[weekly_research] watchlist: {len(watchlist_summary['items'])} drafts written, {len(watchlist_summary['errors'])} errors")
    else:
        payload["watchlist"] = {"items": [], "errors": [], "note": "empty"}
        print("[weekly_research] watchlist empty — skipped")

    payload["status"] = "ok"
    payload["finished"] = dt.datetime.now(dt.timezone.utc).isoformat()
    append_log(payload)
    print("[weekly_research] done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
