"""Weekly digest agent — writes one public blog post per week.

Runs on Sundays (via agent/run_weekly.bat + Task Scheduler). Reads the last
seven daily digests from ``agent/daily_drafts/``, fetches this week's
highest-scoring Hacker News stories and the week's cs.AI arXiv papers,
feeds everything to local Ollama, and writes the result to
``content/blog/YYYY-MM-DD-weekly-digest.md``.

Run it directly:

    .venv\\Scripts\\python -m agent.weekly_post               # full run (needs Ollama)
    .venv\\Scripts\\python -m agent.weekly_post --dry-run     # show inputs + prompt, no Ollama call
    .venv\\Scripts\\python -m agent.weekly_post --force       # overwrite this week's post if it exists
    .venv\\Scripts\\python -m agent.weekly_post --model qwen2.5:7b

Idempotent: if a weekly post for this week already exists, exits 0 without
overwriting unless ``--force`` is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    NZ_TZ = ZoneInfo("Pacific/Auckland")
    _NZ_TZ_FALLBACK = False
except Exception:  # pragma: no cover
    NZ_TZ = timezone.utc
    _NZ_TZ_FALLBACK = True
    print(
        "WARNING: zoneinfo could not resolve Pacific/Auckland; "
        "falling back to UTC. Install the `tzdata` package to fix.",
        file=sys.stderr,
    )

import requests

from agent._env import load_dotenv

load_dotenv()

# Force UTF-8 on Windows consoles so macrons etc. don't blow up cp1252 stdout.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "agent" / "daily_drafts"
POSTS_DIR = ROOT / "content" / "blog"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "weekly_post.md"
LOG_PATH = Path(__file__).resolve().parent / "logs" / "weekly.log"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL_DEFAULT = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")

# HN Algolia Search API — "front_page" tag with a created_at_i > week_ago
# gives us stories that hit the front page in the last 7 days, ranked by
# points. We want roughly 25 items so the model has breadth without being
# overwhelmed.
HN_ALGOLIA = "https://hn.algolia.com/api/v1/search"
HN_HITS = 25

ARXIV_API = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results={n}"
)
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_MAX = 25
ARXIV_WINDOW_DAYS = 7


MAX_LOG_LINES = 1000


def rotate_log_if_needed() -> None:
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
# Inputs
# ---------------------------------------------------------------------------


def read_daily_drafts(today: date, days: int = 7) -> list[dict]:
    """Return up to ``days`` most recent daily drafts ending on ``today``."""
    if not DRAFTS_DIR.exists():
        return []
    cutoff = today - timedelta(days=days - 1)
    drafts: list[dict] = []
    for path in sorted(DRAFTS_DIR.glob("*.md")):
        stem = path.stem  # YYYY-MM-DD-slug
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-", stem)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d < cutoff or d > today:
            continue
        drafts.append({"date": d, "path": path, "text": path.read_text(encoding="utf-8")})
    drafts.sort(key=lambda x: x["date"])
    return drafts


def fetch_hn_weekly(today: date, hits: int = HN_HITS) -> list[dict]:
    """Top front-page HN stories from the past 7 days, by points."""
    week_ago = int(
        datetime.combine(today - timedelta(days=7), datetime.min.time(), tzinfo=timezone.utc).timestamp()
    )
    params = {
        "tags": "front_page",
        "numericFilters": f"created_at_i>{week_ago}",
        "hitsPerPage": str(hits),
    }
    url = f"{HN_ALGOLIA}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())
        items: list[dict] = []
        for hit in data.get("hits", []):
            title = (hit.get("title") or "").strip()
            story_url = (hit.get("url") or "").strip()
            points = hit.get("points") or 0
            if not title:
                continue
            # Prefer the story's original URL; fall back to the HN item page
            # for Ask HN / Show HN where `url` is empty.
            if not story_url and hit.get("objectID"):
                story_url = f"https://news.ycombinator.com/item?id={hit['objectID']}"
            if not story_url:
                continue
            items.append({"title": title, "url": story_url, "points": points})
        # Sort by points desc to bias the prompt toward higher-signal stories.
        items.sort(key=lambda x: x["points"], reverse=True)
        return items
    except Exception as exc:
        log(f"fetch_hn_weekly failed: {exc}")
        return []


def fetch_arxiv_weekly(max_results: int = ARXIV_MAX, days: int = ARXIV_WINDOW_DAYS) -> list[dict]:
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
                trimmed = summary[:350].rstrip() + ("…" if len(summary) > 350 else "")
                items.append({"title": title, "url": link, "summary": trimmed})
            if len(items) >= max_results:
                break
        return items
    except Exception as exc:
        log(f"fetch_arxiv_weekly failed: {exc}")
        return []


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------


def _format_digest(d: dict) -> str:
    """Render one daily draft as a heading + body for the weekly prompt."""
    return f"### {d['date'].isoformat()} — {d['path'].name}\n\n{d['text'].strip()}"


def build_prompt(drafts: list[dict], hn: list[dict], arxiv: list[dict]) -> tuple[str, str]:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    parts = re.split(r"^##\s*User\s*$", template, maxsplit=1, flags=re.MULTILINE)
    if len(parts) != 2:
        raise RuntimeError("Prompt template missing ## User section")
    system_section, user_section = parts
    system_prompt = re.sub(r"^##\s*System\s*$", "", system_section, flags=re.MULTILINE).strip()

    today_nz = datetime.now(NZ_TZ)
    if os.name == "nt":
        today_fmt = today_nz.strftime("%A, %#d %B %Y")
    else:
        today_fmt = today_nz.strftime("%A, %-d %B %Y")

    daily_block = (
        "\n\n".join(_format_digest(d) for d in drafts)
        if drafts
        else "(no daily digests found for this week)"
    )
    hn_block = (
        "\n".join(f"- {s['title']} ({s['points']} pts) — {s['url']}" for s in hn)
        or "(no HN stories fetched)"
    )
    arxiv_block = (
        "\n".join(f"- {p['title']}\n  {p['url']}\n  {p['summary']}" for p in arxiv)
        or "(no recent papers fetched)"
    )

    user_prompt = (
        user_section.strip()
        .replace("{{today}}", today_fmt)
        .replace("{{daily_digests}}", daily_block)
        .replace("{{hn_list}}", hn_block)
        .replace("{{arxiv_list}}", arxiv_block)
    )
    return system_prompt, user_prompt


# ---------------------------------------------------------------------------
# Ollama client (same shape as daily_post, kept local so the two agents are
# independent — copying ten lines beats coupling the two modules)
# ---------------------------------------------------------------------------


def call_ollama(
    system: str,
    user: str,
    model: str,
    timeout: int = 600,
    max_attempts: int = 3,
) -> str:
    payload = {
        "model": model,
        "system": system,
        "prompt": user,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.6, "num_ctx": 16384},
    }
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
            if r.status_code >= 500:
                last_exc = requests.exceptions.HTTPError(
                    f"{r.status_code} {r.reason}", response=r
                )
                log(f"Ollama returned {r.status_code} on attempt {attempt}/{max_attempts}; retrying.")
            else:
                r.raise_for_status()
                return r.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.Timeout as exc:
            last_exc = exc
            log(f"Ollama timed out on attempt {attempt}/{max_attempts}; retrying.")
        if attempt < max_attempts:
            time.sleep(5 * attempt)
    assert last_exc is not None
    raise last_exc


def parse_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        raise ValueError("Ollama response contained no JSON object")
    return json.loads(match.group())


# ---------------------------------------------------------------------------
# Post writing
# ---------------------------------------------------------------------------


def _existing_for_week(week_sunday: date) -> Path | None:
    """Return any existing weekly post file for the week ending `week_sunday`."""
    if not POSTS_DIR.exists():
        return None
    matches = list(POSTS_DIR.glob(f"{week_sunday.isoformat()}-*weekly*.md"))
    return matches[0] if matches else None


def escape_yaml(s: str) -> str:
    return s.replace("\\", "\\\\").replace("\"", "\\\"")


def write_post(
    title: str,
    summary: str,
    body_markdown: str,
    tags: list[str],
    post_date: date,
    force: bool = False,
) -> Path:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{post_date.isoformat()}-weekly-digest.md"
    path = POSTS_DIR / filename

    if path.exists() and not force:
        log(f"A weekly post for {post_date.isoformat()} already exists; skipping. Pass --force to overwrite.")
        return path

    if not tags:
        tags = ["weekly-digest"]
    elif "weekly-digest" not in tags:
        tags = ["weekly-digest"] + tags

    # Always write as draft. freeze.py skips status=draft posts when
    # building the static site, so this is the production gate. Use
    # `scripts/publish_weekly.bat` to flip status and deploy, or
    # `scripts/reject_weekly.bat` to delete the draft.
    fm_lines = [
        "---",
        f"title: \"{escape_yaml(title)}\"",
        f"date: {post_date.isoformat()}",
        "author: agent",
        f"summary: \"{escape_yaml(summary)}\"",
        "tags: [" + ", ".join(tags) + "]",
        "status: draft",
        "---",
        "",
        body_markdown.strip(),
        "",
    ]
    path.write_text("\n".join(fm_lines), encoding="utf-8")
    log(f"Wrote {path.name} (status=draft; not yet public)")
    return path


# ---------------------------------------------------------------------------
# Review-email notification
# ---------------------------------------------------------------------------


def send_review_email(post_path: Path, title: str, summary: str) -> bool:
    """Email the draft to CONTACT_TO so Luke can review on phone/desktop.

    Reads RESEND_API_KEY, CONTACT_FROM, CONTACT_TO from env (or .env file
    in project root). If any are missing, logs and returns False — the
    weekly run is *not* failed because of email issues; the draft is
    still on disk and visible at /blog/ in local Flask.
    """
    api_key = os.environ.get("RESEND_API_KEY")
    sender = os.environ.get("CONTACT_FROM", "form@lukesimmonsnz.kiwi")
    recipient = os.environ.get("CONTACT_TO")

    if not api_key:
        log("Skipping review email: RESEND_API_KEY not set (check .env).")
        return False
    if not recipient:
        log("Skipping review email: CONTACT_TO not set (check .env).")
        return False

    body_md = post_path.read_text(encoding="utf-8")

    text = (
        f"Weekly digest draft is ready: {post_path.name}\n\n"
        f"Title:    {title}\n"
        f"Summary:  {summary}\n\n"
        "Decide:\n"
        "  publish  →  scripts\\publish_weekly.bat\n"
        "  reject   →  scripts\\reject_weekly.bat\n\n"
        "(Both commands operate on the most recent draft weekly digest "
        "in content/blog/. Publish flips status, freezes the site, and "
        "deploys to Cloudflare Pages. Reject deletes the draft file.)\n\n"
        "----- DRAFT BODY BELOW -----\n\n"
        f"{body_md}"
    )
    subject = f"[lukesimmonsnz weekly DRAFT] {title}"

    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": sender,
                "to": [recipient],
                "subject": subject,
                "text": text,
            },
            timeout=30,
        )
        if r.status_code >= 400:
            log(f"Resend returned {r.status_code}: {r.text[:300]}")
            return False
        log(f"Sent review email to {recipient} via Resend.")
        return True
    except Exception as exc:
        log(f"Review email failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _this_week_sunday(today: date) -> date:
    """Return the Sunday of the ISO week containing `today` (weekday 6 = Sun).

    If today is already Sunday, returns today."""
    # Python weekday: Mon=0 ... Sun=6
    return today + timedelta(days=(6 - today.weekday()) % 7)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose this week's weekly-digest blog post.")
    parser.add_argument("--dry-run", action="store_true", help="Show inputs + prompt; don't call Ollama, don't write.")
    parser.add_argument("--force", action="store_true", help="Overwrite this week's weekly post if one already exists.")
    parser.add_argument("--model", default=OLLAMA_MODEL_DEFAULT, help="Ollama model name (default: %(default)s).")
    parser.add_argument("--date", help="Override the post date (YYYY-MM-DD). Default: upcoming/current Sunday in NZT.")
    args = parser.parse_args()

    rotate_log_if_needed()

    today_nz = datetime.now(NZ_TZ).date()
    post_date = (
        date.fromisoformat(args.date)
        if args.date
        else _this_week_sunday(today_nz)
    )
    log(f"Weekly run starting. today={today_nz.isoformat()} post_date={post_date.isoformat()} model={args.model} dry-run={args.dry_run}")
    if _NZ_TZ_FALLBACK:
        log("NOTE: running in UTC-fallback mode because tzdata is missing.")

    if not args.force and not args.dry_run and _existing_for_week(post_date):
        log("A weekly post for this week already exists. Nothing to do.")
        return 0

    drafts = read_daily_drafts(today_nz, days=7)
    log(f"Loaded {len(drafts)} daily drafts from the past 7 days.")
    hn = fetch_hn_weekly(today_nz)
    arxiv = fetch_arxiv_weekly()
    log(f"Fetched {len(hn)} HN stories (last 7 days) and {len(arxiv)} arXiv papers.")

    if not drafts and not hn and not arxiv:
        log("No drafts and no fresh sources. Aborting so we don't publish an empty post.")
        return 1

    system_prompt, user_prompt = build_prompt(drafts, hn, arxiv)

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
        log(f"Ollama returned a post with missing title or body. Aborting. Parsed keys: {list(parsed.keys())}")
        return 5

    path = write_post(title, summary, body, tags, post_date, force=args.force)
    log(f"Draft saved to content/blog/{path.name} (status=draft).")

    # Email Luke for review — non-fatal if it fails.
    send_review_email(path, title, summary)

    log("Done. Use scripts\\publish_weekly.bat to ship, scripts\\reject_weekly.bat to discard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
