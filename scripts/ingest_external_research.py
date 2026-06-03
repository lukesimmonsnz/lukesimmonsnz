#!/usr/bin/env python3
"""Ingest external research material (URL or PDF) → proposed claim/source YAML stubs.

Writes to ``content/<region>/data/_drafts/<timestamp>/`` so existing files
in the typed-graph corpus are never touched. The user reviews the drafts
and either commits them into the live ``claim/`` and ``source/`` folders
or discards them.

Usage::

    python scripts/ingest_external_research.py <URL or PDF path> \
        --region <slug> --theme <slug> [--ollama] [--dry-run]

Behaviour highlights:
  * Fetch via ``requests`` for URLs, ``pypdf`` for PDFs.
  * HTML extraction prefers ``trafilatura``/``readability-lxml``/``bs4``,
    falls back to a stdlib ``html.parser`` text strip.
  * If ``--ollama`` and Ollama is reachable on localhost:11434, qwen2.5:7b
    proposes claims; otherwise heuristic regex extraction (numbers, %, $)
    runs and a notice is printed.

Schema notes (vs the looser brief):
  * Source uses ``type`` (not ``kind``) per ``source.schema.json``.
  * ``accessed`` and per-claim ``theme`` are NOT in the schemas
    (``additionalProperties: false``); they're stashed in a sidecar
    ``_meta.yaml`` so the user has the full proposal context but the
    YAML stubs themselves stay lint-clean.
  * Claim IDs follow the convention ``claim.<region>.<theme>.<slug>``;
    source IDs follow ``source.<slug>``.

Defaults to ``methodology.admin_count_v1`` for ``methodology_tag`` —
override before committing if a more specific methodology applies.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

# yaml and requests are project-default deps; everything else is optional.
import yaml  # type: ignore[import-not-found]

try:
    import requests  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

UA = "ai-website-manager/ingest-external-research (+https://lukesimmonsnz.kiwi)"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"
DEFAULT_METHODOLOGY = "methodology.admin_count_v1"
TODAY = dt.date.today().isoformat()
SOURCE_TYPES = {
    "primary-data",
    "primary-legislation",
    "academic",
    "government-report",
    "news-media",
    "commentary",
    "iwi-publication",
    "tribunal",
    "technical-standard",
}


# ─── Fetching ────────────────────────────────────────────────────────────────

def fetch_url(url: str) -> tuple[str, str]:
    """Return (text_content, content_type) for ``url``."""
    if requests is None:
        # Fallback to urllib if requests is somehow unavailable.
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            ctype = resp.headers.get("Content-Type", "text/html")
            data = resp.read()
        return data.decode("utf-8", errors="replace"), ctype
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    resp.raise_for_status()
    return resp.text, resp.headers.get("Content-Type", "text/html")


def read_pdf(path: Path) -> str:
    """Extract text from a local PDF via ``pypdf``. Fail loudly if absent."""
    try:
        import pypdf  # type: ignore[import-not-found]
    except ImportError as e:
        raise SystemExit(
            "PDF parsing requires `pypdf`. Install it with:\n"
            "    pip install pypdf"
        ) from e
    if not path.exists():
        raise SystemExit(f"PDF not found: {path}")
    reader = pypdf.PdfReader(str(path))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)


# ─── HTML → text ─────────────────────────────────────────────────────────────

class _StdlibHTMLToText(HTMLParser):
    """Last-resort HTML-to-text using only the stdlib. Also pulls the
    page title and meta description (since many JS-rendered SPAs ship
    only a meta description in static HTML).
    """

    SKIP = {"script", "style", "noscript", "nav"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0
        self.title = ""
        self._in_title = False
        self.meta_description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            ad = {k.lower(): (v or "") for k, v in attrs}
            name = ad.get("name", "").lower()
            prop = ad.get("property", "").lower()
            if name in {"description", "twitter:description"} or prop == "og:description":
                if ad.get("content"):
                    self.meta_description = ad["content"]
            if name == "og:title" and not self.title and ad.get("content"):
                self.title = ad["content"]

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "div"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data
        self._chunks.append(data)

    @property
    def text(self) -> str:
        out = "".join(self._chunks)
        out = re.sub(r"[ \t]+", " ", out)
        out = re.sub(r"\n{2,}", "\n\n", out)
        out = out.strip()
        # SPA fallback: if body text is essentially empty, fall back to
        # the meta description so heuristic claim extraction has something
        # to chew on.
        if len(out) < 200 and self.meta_description:
            return f"{self.meta_description}\n\n{out}".strip()
        return out


def _meta_fallback(html: str) -> tuple[str, str | None]:
    """Run the stdlib parser purely to pull meta description / title."""
    p = _StdlibHTMLToText()
    p.feed(html)
    return p.text, p.title or None


def extract_html_text(html: str) -> tuple[str, str | None]:
    """Return (clean_text, title) from raw HTML, using best library available.

    For JS-rendered SPAs (Stats NZ etc.) the static HTML body is often
    near-empty; in that case we fall back to ``<meta name=description>``
    so heuristic extraction still has signal.
    """
    # 1. trafilatura (best quality)
    try:
        import trafilatura  # type: ignore[import-not-found]
        text = trafilatura.extract(html, include_comments=False, include_tables=False) or ""
        meta = trafilatura.extract_metadata(html)
        title = getattr(meta, "title", None) if meta else None
        if text and len(text) > 200:
            return text, title
    except ImportError:
        pass

    # 2. readability-lxml + bs4
    try:
        from readability import Document  # type: ignore[import-not-found]
        from bs4 import BeautifulSoup  # type: ignore[import-not-found]
        doc = Document(html)
        title = doc.short_title()
        soup = BeautifulSoup(doc.summary(), "html.parser")
        text = soup.get_text("\n", strip=True)
        if len(text) > 200:
            return text, title
    except ImportError:
        pass

    # 3. plain bs4
    try:
        from bs4 import BeautifulSoup  # type: ignore[import-not-found]
        soup = BeautifulSoup(html, "html.parser")
        for t in soup(["script", "style", "noscript", "nav"]):
            t.decompose()
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else None
        text = soup.get_text("\n", strip=True)
        if len(text) > 200:
            return text, title
        # Empty SPA body — try meta fallback.
        meta_text, meta_title = _meta_fallback(html)
        if meta_text:
            return meta_text, title or meta_title
    except ImportError:
        pass

    # 4. stdlib fallback (also returns meta description when body is empty)
    return _meta_fallback(html)


# ─── Source-stub heuristics ──────────────────────────────────────────────────

PUBLISHER_HINTS = {
    "stats.govt.nz": ("Stats NZ", "primary-data", "official"),
    "treasury.govt.nz": ("The Treasury", "government-report", "official"),
    "mbie.govt.nz": ("MBIE", "government-report", "official"),
    "mfe.govt.nz": ("Ministry for the Environment", "government-report", "official"),
    "mhud.govt.nz": ("MHUD", "government-report", "official"),
    "hud.govt.nz": ("HUD", "government-report", "official"),
    "nzta.govt.nz": ("NZ Transport Agency Waka Kotahi", "government-report", "official"),
    "rnz.co.nz": ("RNZ", "news-media", "reputable"),
    "stuff.co.nz": ("Stuff", "news-media", "reputable"),
    "nzherald.co.nz": ("NZ Herald", "news-media", "reputable"),
    "nzier.org.nz": ("NZIER", "academic", "reputable"),
    "motu.org.nz": ("Motu", "academic", "reputable"),
    "auckland.ac.nz": ("University of Auckland", "academic", "peer-reviewed"),
    "victoria.ac.nz": ("Victoria University of Wellington", "academic", "peer-reviewed"),
    "otago.ac.nz": ("University of Otago", "academic", "peer-reviewed"),
    "waitangitribunal.govt.nz": ("Waitangi Tribunal", "tribunal", "official"),
    "legislation.govt.nz": ("NZ Legislation", "primary-legislation", "official"),
}


def _slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text[:max_len].rstrip("_") or "untitled"


def _detect_source_metadata(url: str | None, title: str, body: str) -> dict[str, Any]:
    """Heuristically guess publisher / type / credibility / year from url+text."""
    publisher: str | None = None
    src_type = "news-media"
    credibility = "reputable"
    if url:
        host = urllib.parse.urlparse(url).hostname or ""
        host = host.lower().lstrip("www.")
        for hint, (pub, t, c) in PUBLISHER_HINTS.items():
            if host.endswith(hint):
                publisher = pub
                src_type = t
                credibility = c
                break
        if publisher is None and host.endswith(".govt.nz"):
            publisher = host.split(".")[0].upper()
            src_type = "government-report"
            credibility = "official"
    # Year: prefer the most recent 19xx/20xx in title/body.
    year_match = sorted(
        {int(y) for y in re.findall(r"\b(19[5-9]\d|20\d{2})\b", f"{title}\n{body[:4000]}")
         if 1950 <= int(y) <= dt.date.today().year + 1},
        reverse=True,
    )
    year = year_match[0] if year_match else None
    return {
        "publisher": publisher,
        "type": src_type,
        "credibility": credibility,
        "year": year,
    }


def build_source_stub(
    url: str | None,
    title: str,
    body: str,
    region: str,
) -> dict[str, Any]:
    title = title.strip() or "Untitled external source"
    meta = _detect_source_metadata(url, title, body)
    pub_slug = _slugify(meta["publisher"] or "external")
    title_slug = _slugify(title, max_len=40)
    year_slug = str(meta["year"]) if meta["year"] else "ny"
    source_id = f"source.{pub_slug}_{title_slug}_{year_slug}"
    # Schema-clean source dict.
    source: dict[str, Any] = {
        "id": source_id,
        "title": title,
        "author": None,
        "publisher": meta["publisher"],
        "year": meta["year"],
        "url": url,
        "type": meta["type"] if meta["type"] in SOURCE_TYPES else "news-media",
        "credibility": meta["credibility"],
        "geo_granularity": [region] if region != "nz" else ["nz"],
        "notes": f"Auto-ingested {TODAY}; review before committing.",
    }
    return source


# ─── Claim extraction (heuristic + Ollama) ───────────────────────────────────

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
_VALUE_RE = re.compile(
    r"""
    (
        \$?\s*\d{1,3}(?:,\d{3})+(?:\.\d+)?      # 1,234,567.89
      | \$?\s*\d+(?:\.\d+)?\s*(?:million|billion|m|bn)\b
      | \d+(?:\.\d+)?\s*%
      | \d+(?:\.\d+)?\s*(?:per\s+cent|percent|percentage\s+points?)\b
      | \d+(?:\.\d+)?\s*(?:per\s+capita|per\s+1[,]?000|per\s+100[,]?000)\b
      | \d+(?:\.\d+)?\b
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _classify_unit(value_text: str) -> tuple[str | None, str]:
    """Return (unit, normalised_value_str) from the raw matched value text."""
    v = value_text.strip()
    if "%" in v or "percent" in v.lower() or "per cent" in v.lower():
        return ("percent", re.sub(r"[^\d.]", "", v.split()[0]))
    if "$" in v:
        if any(s in v.lower() for s in ("billion", "bn")):
            return ("NZD billion", re.sub(r"[^\d.]", "", v))
        if any(s in v.lower() for s in ("million", "m")):
            return ("NZD million", re.sub(r"[^\d.]", "", v))
        return ("NZD", re.sub(r"[^\d.]", "", v))
    if "per capita" in v.lower():
        return ("rate per capita", re.sub(r"[^\d.]", "", v.split()[0]))
    if "per 1,000" in v.lower() or "per 1000" in v.lower():
        return ("rate per 1,000", re.sub(r"[^\d.]", "", v.split()[0]))
    if "per 100,000" in v.lower() or "per 100000" in v.lower():
        return ("rate per 100,000", re.sub(r"[^\d.]", "", v.split()[0]))
    return (None, re.sub(r"[^\d.]", "", v) or v)


def heuristic_claims(body: str, max_claims: int = 5) -> list[dict[str, Any]]:
    r"""Pull up to ``max_claims`` numerical sentences as candidate claims.

    Sentences are split on ``[.!?]\s+[A-Z]`` so decimals like ``5.1`` don't
    accidentally end a sentence. We then keep sentences that contain a
    quantity (``_VALUE_RE``).
    """
    body = re.sub(r"\s+", " ", body).strip()
    sentences = _SENT_SPLIT.split(body)
    seen: set[str] = set()
    claims: list[dict[str, Any]] = []
    for raw in sentences:
        sentence = raw.strip().rstrip(",;:")
        if not sentence.endswith((".", "!", "?")):
            sentence += "."
        if len(sentence) < 30 or len(sentence) > 400:
            continue
        m = _VALUE_RE.search(sentence)
        if not m:
            continue
        if sentence in seen:
            continue
        seen.add(sentence)
        unit, value_str = _classify_unit(m.group(1))
        try:
            value: float | str = float(value_str)
        except (ValueError, TypeError):
            value = m.group(1).strip()
        claims.append({"statement": sentence, "value": value, "unit": unit})
        if len(claims) >= max_claims:
            break
    return claims


def ollama_available() -> bool:
    if requests is None:
        return False
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def ollama_claims(body: str, source_title: str, region: str, theme: str) -> list[dict[str, Any]]:
    """Ask local qwen2.5:7b for 1–5 quantitative claims as JSON."""
    excerpt = body[:8000]
    prompt = (
        "You are extracting research claims for a typed-graph knowledge base.\n"
        f"Region: {region}. Theme: {theme}. Source title: {source_title}.\n\n"
        "Return STRICT JSON: a list of 1–5 objects, each with keys "
        "`statement` (one sentence, ≤300 chars), `value` (number or null), "
        "`unit` (string or null), `time_period` (string or null), "
        "`confidence` (one of high/medium/low/disputed). "
        "Do not invent facts. Quote numerical claims actually present in the text.\n\n"
        f"TEXT:\n{excerpt}\n\nJSON:"
    )
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1},
    }
    if requests is None:
        return []
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        r.raise_for_status()
    except Exception as e:
        print(f"  warn: Ollama call failed ({e}); falling back to heuristics.", file=sys.stderr)
        return []
    raw = r.json().get("response", "")
    # qwen often wraps JSON in ```json ... ``` fences.
    raw = re.sub(r"^```(?:json)?\s*|\s*```\s*$", "", raw.strip(), flags=re.M)
    # Find the first JSON array in the response.
    arr_match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not arr_match:
        return []
    try:
        data = json.loads(arr_match.group(0))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    out: list[dict[str, Any]] = []
    for item in data[:5]:
        if not isinstance(item, dict) or "statement" not in item:
            continue
        out.append({
            "statement": str(item.get("statement", "")).strip(),
            "value": item.get("value"),
            "unit": item.get("unit"),
            "time_period": item.get("time_period"),
            "confidence": item.get("confidence") or "medium",
        })
    return out


def build_claim_stubs(
    raw_claims: list[dict[str, Any]],
    source_id: str,
    region: str,
    theme: str,
) -> list[dict[str, Any]]:
    stubs: list[dict[str, Any]] = []
    for i, rc in enumerate(raw_claims, start=1):
        slug = _slugify(rc["statement"], max_len=40) or f"claim_{i}"
        claim_id = f"claim.{region}.{theme}.{slug}_{i}"
        confidence = rc.get("confidence") if rc.get("confidence") in {
            "high", "medium", "low", "disputed",
        } else "medium"
        # Schema-strict claim dict (additionalProperties: false).
        claim: dict[str, Any] = {
            "id": claim_id,
            "statement": rc["statement"],
            "value": rc.get("value"),
            "unit": rc.get("unit"),
            "time_period": rc.get("time_period"),
            "confidence": confidence,
            "verification_status": "cited_only",
            "last_verified": TODAY,
            "source_ids": [source_id],
            "scoped_to": [region],
            "national_assertion": region == "nz",
            "region_mentions": [region],
            "methodology_tag": DEFAULT_METHODOLOGY,
            "notes": None,
        }
        stubs.append(claim)
    return stubs


# ─── YAML output (lint-shaped) ───────────────────────────────────────────────

def _dump_yaml(obj: dict[str, Any]) -> str:
    """Match the project's PyYAML default_flow_style=False, sort_keys=False output."""
    return yaml.safe_dump(
        obj,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=110,
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Ingest URL/PDF → claim+source YAML stubs in content/<region>/data/_drafts/",
    )
    p.add_argument("input", help="URL or local PDF path")
    p.add_argument("--region", required=True, help="Region slug (e.g. wellington, auckland, nz)")
    p.add_argument("--theme", required=True, help="Theme slug (e.g. transport, housing)")
    p.add_argument("--ollama", action="store_true", help="Use local Ollama qwen2.5:7b for claim extraction")
    p.add_argument("--dry-run", action="store_true", help="Print proposed YAML; write nothing")
    p.add_argument("--max-claims", type=int, default=5)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    region_dir = repo_root / "content" / args.region / "data"
    if not region_dir.exists() and not args.dry_run:
        raise SystemExit(
            f"Region directory not found: {region_dir}\n"
            "Use --dry-run to preview, or pick an existing region."
        )

    # 1. Fetch
    src_input = args.input
    is_pdf = src_input.lower().endswith(".pdf") and not src_input.startswith("http")
    if is_pdf:
        body = read_pdf(Path(src_input))
        url: str | None = None
        title = Path(src_input).stem.replace("_", " ").replace("-", " ")
    else:
        raw, ctype = fetch_url(src_input)
        url = src_input
        if "pdf" in ctype.lower() or src_input.lower().endswith(".pdf"):
            print("note: remote PDF — pypdf needed; download then pass local path.", file=sys.stderr)
            raise SystemExit(1)
        body, page_title = extract_html_text(raw)
        title = (page_title or "").strip()
    if not body.strip():
        raise SystemExit("No text could be extracted from the input.")

    # Strip the title from body so it doesn't masquerade as a claim.
    if title:
        body = body.replace(title, "").strip()

    # 2. Build source stub
    source = build_source_stub(url, title, body, args.region)

    # 3. Build claim stubs
    used_ollama = False
    if args.ollama:
        if ollama_available():
            raw_claims = ollama_claims(body, source["title"], args.region, args.theme)
            if raw_claims:
                used_ollama = True
            else:
                print("note: Ollama returned no parseable claims; falling back to heuristics.",
                      file=sys.stderr)
                raw_claims = heuristic_claims(body, max_claims=args.max_claims)
        else:
            print("note: Ollama not reachable on localhost:11434; using heuristics.",
                  file=sys.stderr)
            raw_claims = heuristic_claims(body, max_claims=args.max_claims)
    else:
        raw_claims = heuristic_claims(body, max_claims=args.max_claims)

    if not raw_claims:
        print("warn: no quantitative claims could be extracted from the text.", file=sys.stderr)

    claims = build_claim_stubs(raw_claims, source["id"], args.region, args.theme)

    # 4. Render and output
    source_yaml = _dump_yaml(source)
    claim_yamls = {c["id"]: _dump_yaml(c) for c in claims}
    sidecar = {
        "ingested_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input": src_input,
        "region": args.region,
        "theme": args.theme,
        "extractor": "ollama:qwen2.5:7b" if used_ollama else "heuristic-regex",
        "accessed": TODAY,  # `accessed` lives here, not in the source schema.
        "claim_theme": args.theme,  # theme is not a Claim field; keep it sidecar.
        "review_checklist": [
            "Verify source publisher / type / credibility heuristics.",
            "Tighten methodology_tag (default is admin_count_v1).",
            "Confirm value/unit/time_period for each claim.",
            "Confirm scoped_to / region_mentions / national_assertion.",
            "Move stubs into content/<region>/data/{source,claim}/ when accepted.",
        ],
    }
    sidecar_yaml = _dump_yaml(sidecar)

    if args.dry_run:
        print("# === SIDECAR (_meta.yaml) ===")
        print(sidecar_yaml)
        print(f"# === SOURCE ({source['id']}) ===")
        print(source_yaml)
        for cid, ctext in claim_yamls.items():
            print(f"# === CLAIM ({cid}) ===")
            print(ctext)
        print(f"\n# Summary: 1 source + {len(claims)} claim(s); "
              f"extractor={'ollama' if used_ollama else 'heuristic'}.")
        return 0

    # Write to draft directory.
    timestamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    draft_dir = region_dir / "_drafts" / timestamp
    draft_dir.mkdir(parents=True, exist_ok=True)
    (draft_dir / "source").mkdir(exist_ok=True)
    (draft_dir / "claim").mkdir(exist_ok=True)

    src_path = draft_dir / "source" / f"{source['id'].split('.', 1)[1]}.yaml"
    src_path.write_text(source_yaml, encoding="utf-8")

    claim_paths: list[Path] = []
    for c in claims:
        # Claim id is `claim.<region>.<theme>.<slug>_<n>` —
        # filename convention in the live corpus is `<theme>.<slug>.yaml`.
        parts = c["id"].split(".", 3)  # ['claim', region, theme, slug]
        theme_part = parts[2] if len(parts) > 2 else args.theme
        slug = parts[3] if len(parts) > 3 else "untitled"
        cp = draft_dir / "claim" / f"{theme_part}.{slug}.yaml"
        cp.write_text(_dump_yaml(c), encoding="utf-8")
        claim_paths.append(cp)

    (draft_dir / "_meta.yaml").write_text(sidecar_yaml, encoding="utf-8")

    # Summary
    print(f"Wrote drafts to: {draft_dir}")
    print(f"  source: {src_path.relative_to(repo_root)}  ({source['id']})")
    for c, p in zip(claims, claim_paths):
        oneliner = c["statement"][:100] + ("…" if len(c["statement"]) > 100 else "")
        print(f"  claim:  {p.relative_to(repo_root)}  ({c['id']})\n          {oneliner}")
    print(f"\nReview, then move into content/{args.region}/data/{{source,claim}}/ "
          f"and run `python content/{args.region}/tools/lint.py`.")
    if not used_ollama and args.ollama:
        print("(extractor: heuristic regex — Ollama was unreachable or returned no claims)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
