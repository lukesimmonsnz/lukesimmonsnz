"""Daily digest agent — private drafts, not published.

One job: fetch today's signals (Hacker News + arXiv cs.AI), feed them to a local
Ollama model, and write the result into `agent/daily_drafts/YYYY-MM-DD-<slug>.md`.

These drafts are **not served by Flask** and are gitignored. They are working
notes for Luke and feedstock for the weekly digest agent (`agent/weekly_post.py`),
which composes one public blog post per week at `content/blog/`.

Run it directly:

    .venv\\Scripts\\python -m agent.daily_post               # full run (needs Ollama)
    .venv\\Scripts\\python -m agent.daily_post --dry-run     # fetch sources + show prompt, no Ollama call
    .venv\\Scripts\\python -m agent.daily_post --force       # overwrite today's draft if it exists
    .venv\\Scripts\\python -m agent.daily_post --model qwen2.5:7b

Environment variables (with defaults):

    OLLAMA_URL   = http://localhost:11434
    OLLAMA_MODEL = qwen2.5:14b

The script is idempotent: if a draft for today already exists, it exits 0
without overwriting (unless --force is passed).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    NZ_TZ = ZoneInfo("Pacific/Auckland")
    _NZ_TZ_FALLBACK = False
except Exception:  # pragma: no cover
    # Windows Python ships no tzdata; `pip install tzdata` fixes it.
    # Fall back to UTC, but loudly — silent fallback makes the daily run
    # schedule the wrong "today" and skip posts (see 2026-04-22 incident).
    NZ_TZ = timezone.utc
    _NZ_TZ_FALLBACK = True
    print(
        "WARNING: zoneinfo could not resolve Pacific/Auckland; "
        "falling back to UTC. Install the `tzdata` package to fix.",
        file=sys.stderr,
    )

import requests

# Force UTF-8 on Windows consoles so macrons etc. don't blow up cp1252 stdout.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
# Daily drafts are private working notes — gitignored, not served by Flask.
# The weekly agent reads them to compose the public Sunday blog post.
POSTS_DIR = ROOT / "agent" / "daily_drafts"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "daily_post.md"
LOG_PATH = Path(__file__).resolve().parent / "logs" / "daily.log"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL_DEFAULT = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")

HN_RSS_URL = "https://news.ycombinator.com/rss"
ARXIV_API = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results={n}"
)
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


# ---------------------------------------------------------------------------
# Logging — append-to-file with a cheap line-count rotation at startup.
# Daily cadence means ~10 lines/day; 1000 lines is roughly three months.
# ---------------------------------------------------------------------------

MAX_LOG_LINES = 1000


def rotate_log_if_needed() -> None:
    """Trim the log to the last MAX_LOG_LINES lines if it's grown past that.
    Cheap alternative to logging.handlers.RotatingFileHandler — keeps the file
    human-readable and avoids a second .1/.2 file lying around."""
    if not LOG_PATH.exists():
        return
    try:
        with LOG_PATH.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return
    if len(lines) <= MAX_LOG_LINES:
        return
    kept = lines[-MAX_LOG_LINES:]
    with LOG_PATH.open("w", encoding="utf-8") as f:
        f.writelines(kept)


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(NZ_TZ).isoformat(timespec="seconds")
    line = f"[{stamp}] {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

def fetch_hn(limit: int = 20) -> list[dict]:
    try:
        with urllib.request.urlopen(HN_RSS_URL, timeout=20) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        channel = root.find("channel")
        if channel is None:
            return []
        items = []
        for it in channel.findall("item")[:limit]:
            title = (it.findtext("title") or "").strip()
            url = (it.findtext("link") or "").strip()
            title = re.sub(r"\s*\(\d+[^)]*\)\s*$", "", title).strip()
            if title and url:
                items.append({"title": title, "url": url})
        return items
    except Exception as exc:
        log(f"fetch_hn failed: {exc}")
        return []


def fetch_arxiv_recent(max_results: int = 8, days: int = 3) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        with urllib.request.urlopen(ARXIV_API.format(n=max_results * 2), timeout=30) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        items = []
        for entry in root.findall("atom:entry", ARXIV_NS):
            title = (entry.findtext("atom:title", namespaces=ARXIV_NS) or "").strip().replace("\n", " ")
            summary = (entry.findtext("atom:summary", namespaces=ARXIV_NS) or "").strip().replace("\n", " ")
            link = (entry.findtext("atom:id", namespaces=ARXIV_NS) or "").strip()
            published = (entry.findtext("atom:published", namespaces=ARXIV_NS) or "").strip()
            try:
                pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            except ValueError:
                pub_dt = None
            if pub_dt and pub_dt < cutoff:
                continue
            if title and link:
                # Trim the abstract — we don't need the whole thing for the prompt
                trimmed = summary[:400].rstrip() + ("…" if len(summary) > 400 else "")
                items.append({"title": title, "url": link, "summary": trimmed})
            if len(items) >= max_results:
                break
        return items
    except Exception as exc:
        log(f"fetch_arxiv_recent failed: {exc}")
        return []


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------

def build_prompt(hn: list[dict], arxiv: list[dict]) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) by splitting the template on `## User`."""
    template = PROMPT_PATH.read_text(encoding="utf-8")
    # Split on the first "## User" heading
    parts = re.split(r"^##\s*User\s*$", template, maxsplit=1, flags=re.MULTILINE)
    if len(parts) != 2:
        raise RuntimeError("Prompt template missing ## User section")
    system_section, user_section = parts
    # Strip the leading "## System" heading from the system section
    system_prompt = re.sub(r"^##\s*System\s*$", "", system_section, flags=re.MULTILINE).strip()

    today_nz = datetime.now(NZ_TZ).strftime("%A, %-d %B %Y").lstrip("0") if os.name != "nt" else datetime.now(NZ_TZ).strftime("%A, %#d %B %Y")
    hn_list = "\n".join(f"- {s['title']} — {s['url']}" for s in hn) or "(no stories fetched)"
    arxiv_list = (
        "\n".join(f"- {p['title']}\n  {p['url']}\n  {p['summary']}" for p in arxiv)
        or "(no recent papers fetched)"
    )
    user_prompt = (
        user_section.strip()
        .replace("{{today}}", today_nz)
        .replace("{{hn_list}}", hn_list)
        .replace("{{arxiv_list}}", arxiv_list)
    )
    return system_prompt, user_prompt


# ---------------------------------------------------------------------------
# Ollama client
# ---------------------------------------------------------------------------

def call_ollama(
    system: str,
    user: str,
    model: str,
    timeout: int = 300,
    max_attempts: int = 3,
) -> str:
    """POST to Ollama, retrying on timeouts and 5xx responses.

    ConnectionError fails fast (Ollama almost certainly isn't running, and
    retrying won't start it). Timeouts and transient server errors retry
    with exponential backoff (5s, 10s).
    """
    payload = {
        "model": model,
        "system": system,
        "prompt": user,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.7},
    }
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
            if r.status_code >= 500:
                # Server-side hiccup; worth a retry.
                last_exc = requests.exceptions.HTTPError(
                    f"{r.status_code} {r.reason}", response=r
                )
                log(f"Ollama returned {r.status_code} on attempt {attempt}/{max_attempts}; retrying.")
            else:
                r.raise_for_status()
                return r.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            # Don't retry — Ollama is down, let main() exit with a clear code.
            raise
        except requests.exceptions.Timeout as exc:
            last_exc = exc
            log(f"Ollama timed out on attempt {attempt}/{max_attempts}; retrying.")
        if attempt < max_attempts:
            time.sleep(5 * attempt)  # 5s, 10s
    assert last_exc is not None
    raise last_exc


def parse_response(raw: str) -> dict:
    """Extract the JSON object from Ollama's response, tolerant of fences or junk."""
    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Fall back to the first {...} block in the response
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        raise ValueError("Ollama response contained no JSON object")
    return json.loads(match.group())


# ---------------------------------------------------------------------------
# Post writing
# ---------------------------------------------------------------------------

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    slug = SLUG_RE.sub("-", text.lower()).strip("-")
    return slug[:60] or "post"


def write_post(
    title: str,
    summary: str,
    body_markdown: str,
    tags: list[str],
    post_date: date,
    force: bool = False,
) -> Path:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    filename = f"{post_date.isoformat()}-{slug}.md"
    path = POSTS_DIR / filename

    # Idempotent: if any draft already exists for today and --force not set, skip
    if not force:
        existing = list(POSTS_DIR.glob(f"{post_date.isoformat()}-*.md"))
        if existing:
            log(f"A draft for {post_date.isoformat()} already exists ({existing[0].name}); skipping. Pass --force to overwrite.")
            return existing[0]

    # YAML front-matter — keep simple, quote the string values
    fm_lines = [
        "---",
        f"title: \"{escape_yaml(title)}\"",
        f"date: {post_date.isoformat()}",
        "author: agent",
        f"summary: \"{escape_yaml(summary)}\"",
        "tags: [" + ", ".join(tags) + "]",
        "---",
        "",
        body_markdown.strip(),
        "",
    ]
    path.write_text("\n".join(fm_lines), encoding="utf-8")
    log(f"Wrote {path.name}")
    return path


def escape_yaml(s: str) -> str:
    return s.replace("\\", "\\\\").replace("\"", "\\\"")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Write today's blog post via Ollama.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch sources + show prompt; don't call Ollama, don't write.")
    parser.add_argument("--force", action="store_true", help="Overwrite today's post if one already exists.")
    parser.add_argument("--model", default=OLLAMA_MODEL_DEFAULT, help="Ollama model name (default: %(default)s).")
    args = parser.parse_args()

    rotate_log_if_needed()

    today_nz = datetime.now(NZ_TZ).date()
    log(f"Daily run starting for {today_nz.isoformat()} (NZT). Model: {args.model}. Dry-run: {args.dry_run}.")
    if _NZ_TZ_FALLBACK:
        log("NOTE: running in UTC-fallback mode because tzdata is missing. Today's date may be off by up to 1 day.")

    # Early exit if today's draft exists and --force wasn't passed
    if not args.force and not args.dry_run:
        if list(POSTS_DIR.glob(f"{today_nz.isoformat()}-*.md")):
            log("A draft for today already exists. Nothing to do.")
            return 0

    hn = fetch_hn(limit=20)
    arxiv = fetch_arxiv_recent(max_results=6, days=3)
    log(f"Fetched {len(hn)} HN stories and {len(arxiv)} arXiv papers.")

    if not hn and not arxiv:
        log("Both sources returned nothing. Aborting so we don't write an empty draft.")
        return 1

    system_prompt, user_prompt = build_prompt(hn, arxiv)

    if args.dry_run:
        print("\n----- SYSTEM -----\n")
        print(system_prompt)
        print("\n----- USER -----\n")
        print(user_prompt)
        print("\n----- (dry-run: not calling Ollama, not writing) -----\n")
        return 0

    log(f"Calling Ollama at {OLLAMA_URL} (model {args.model})...")
    try:
        raw = call_ollama(system_prompt, user_prompt, model=args.model)
    except requests.exceptions.ConnectionError as exc:
        log(f"Could not reach Ollama at {OLLAMA_URL}. Is it running? {exc}")
        return 2
    except requests.exceptions.Timeout as exc:
        log(f"Ollama kept timing out after retries: {exc}")
        return 2
    except requests.exceptions.HTTPError as exc:
        body = exc.response.text[:500] if exc.response is not None else "(no body)"
        log(f"Ollama HTTP error: {exc}. Response: {body}")
        return 3

    try:
        parsed = parse_response(raw)
    except (ValueError, json.JSONDecodeError) as exc:
        log(f"Could not parse Ollama response as JSON: {exc}. Raw first 500 chars:\n{raw[:500]}")
        return 4

    title = str(parsed.get("title") or "").strip()
    summary = str(parsed.get("summary") or "").strip()
    body = str(parsed.get("body_markdown") or "").strip()
    tags = [str(t).strip().lower() for t in (parsed.get("tags") or []) if str(t).strip()]

    if not title or not body:
        log(f"Ollama returned a draft with missing title or body. Aborting. Parsed keys: {list(parsed.keys())}")
        return 5

    path = write_post(title, summary, body, tags, today_nz, force=args.force)
    log(f"Done. Draft saved at {path.relative_to(ROOT)}. (Not published; feeds the weekly agent.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
