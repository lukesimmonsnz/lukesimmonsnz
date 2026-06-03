import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, render_template

from blueprints.main import main_bp
from blueprints.research import research_bp
from blueprints.davidsimmons import davidsimmons_bp
from blueprints.blog import blog_bp
from blueprints.auckland import auckland_bp
from blueprints.nz import nz_bp
from blueprints.wellington import wellington_bp
from blueprints.northland import northland_bp
from blueprints.waikato import waikato_bp
from blueprints.bay_of_plenty import bay_of_plenty_bp
from blueprints.gisborne import gisborne_bp
from blueprints.hawkes_bay import hawkes_bay_bp
from blueprints.taranaki import taranaki_bp
from blueprints.manawatu_whanganui import manawatu_whanganui_bp
from blueprints.tasman import tasman_bp
from blueprints.nelson import nelson_bp
from blueprints.marlborough import marlborough_bp
from blueprints.west_coast import west_coast_bp
from blueprints.canterbury import canterbury_bp
from blueprints.otago import otago_bp
from blueprints.southland import southland_bp
from blueprints.search import search_bp, build_search_index
from blueprints.admin.cms.blueprint import cms_bp
from blueprints.admin.cms.db import init_cms_db
from blueprints.admin.cms.overlay import install as _install_preview_overlay
from blueprints.admin.cms.settings import (
    load_site_settings as _load_site_settings,
    theme_css_cache_bust as _theme_css_cache_bust,
)

# Absolute base for feeds, sitemap, and Open Graph tags. Default is local-only.
# Set SITE_URL in .flaskenv (or the process env) before deploying.
SITE_URL_DEFAULT = "http://127.0.0.1:5000"

_OWN_HOSTS = ("127.0.0.1", "localhost", "lukesimmonsnz.kiwi")

_ANCHOR_RE = re.compile(r"<a\s+([^>]*?)>", re.IGNORECASE | re.DOTALL)

# Resolve content root relative to this file (works in both Flask dev and
# importlib test harness as long as __file__ is set to an absolute path).
_APP_DIR = Path(__file__).resolve().parent


def _rewrite_external_anchor(match):
    attrs = match.group(1)
    if re.search(r"\btarget\s*=", attrs, re.IGNORECASE):
        return match.group(0)
    href = re.search(r'href\s*=\s*"(https?://[^"]+)"', attrs, re.IGNORECASE)
    if not href:
        return match.group(0)
    url = href.group(1)
    if any(host in url for host in _OWN_HOSTS):
        return match.group(0)
    return f'<a {attrs} target="_blank" rel="noopener">'


def create_app():
    app = Flask(__name__)
    app.config["SITE_URL"] = os.environ.get("SITE_URL", SITE_URL_DEFAULT).rstrip("/")
    app.config["SITE_NAME"] = "Luke Simmons"
    app.config["SITE_TAGLINE"] = (
        "Personal site, research notes, and a biography of David Roy Simmons."
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(research_bp, url_prefix="/research")
    app.register_blueprint(davidsimmons_bp, url_prefix="/davidsimmons")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(auckland_bp)
    app.register_blueprint(nz_bp)
    app.register_blueprint(wellington_bp)
    app.register_blueprint(northland_bp)
    app.register_blueprint(waikato_bp)
    app.register_blueprint(bay_of_plenty_bp)
    app.register_blueprint(gisborne_bp)
    app.register_blueprint(hawkes_bay_bp)
    app.register_blueprint(taranaki_bp)
    app.register_blueprint(manawatu_whanganui_bp)
    app.register_blueprint(tasman_bp)
    app.register_blueprint(nelson_bp)
    app.register_blueprint(marlborough_bp)
    app.register_blueprint(west_coast_bp)
    app.register_blueprint(canterbury_bp)
    app.register_blueprint(otago_bp)
    app.register_blueprint(southland_bp)
    app.register_blueprint(search_bp)
    # CMS-SPEC §10 migration: DASHBOARD-SPEC admin moves to /admin/yaml/
    # so the new CMS can claim /admin/. Templates use url_for('admin.X')
    # which resolves by blueprint name, so existing links continue to work.
    # /admin/yaml/ typed-entity editor was shelved 2026-05-30 — code moved
    # to archive/admin-yaml/. See docs/DASHBOARD-SPEC.md (status header) and
    # CHANGELOG entry for the rationale.
    app.register_blueprint(cms_bp)
    init_cms_db(app)
    _install_preview_overlay()        # δ — Path.read_text intercept

    app.config["TURNSTILE_SITE_KEY"] = os.environ.get("TURNSTILE_SITE_KEY", "").strip()
    app.config["CONTACT_SUBMIT_URL"] = os.environ.get("CONTACT_SUBMIT_URL", "").strip()

    _now = datetime.now(tz=timezone.utc)
    app.config["CURRENT_QUARTER"] = f"{_now.year}-Q{math.ceil(_now.month / 3)}"

    # Build search index at startup — scans all region pages/ directories once.
    app.config["SEARCH_INDEX"] = build_search_index(_APP_DIR / "content")

    # Per-request load of instance/site_settings.json (mtime-cached).
    # ζ ratification (CMS-IMPL-WAVE-4 §9.4): site_settings.json shadows
    # app.config / .env when keys are present.
    @app.before_request
    def _load_site_settings_hook():
        g.site_settings = _load_site_settings()

    @app.context_processor
    def _inject_site():
        s = getattr(g, "site_settings", None) or {}
        site = s.get("site") or {}
        contact = s.get("contact") or {}
        # Precedence: site_settings shadows app.config (which derives from .env / hardcoded).
        return {
            "site_url":            site.get("url")    or app.config["SITE_URL"],
            "site_name":           site.get("name")   or app.config["SITE_NAME"],
            "site_tagline":        site.get("tagline") or app.config["SITE_TAGLINE"],
            "turnstile_site_key":  contact.get("turnstile_site_key") or app.config["TURNSTILE_SITE_KEY"],
            "contact_submit_url":  contact.get("submit_url")          or app.config["CONTACT_SUBMIT_URL"],
            "current_quarter":     app.config["CURRENT_QUARTER"],
            "site_settings":       s,
            "theme_css_bust":      _theme_css_cache_bust(),
        }

    @app.errorhandler(404)
    def _not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def _server_error(e):
        return render_template("500.html"), 500

    @app.after_request
    def _open_external_links_in_new_tab(response):
        if response.mimetype != "text/html":
            return response
        if response.direct_passthrough:
            return response
        try:
            body = response.get_data(as_text=True)
        except UnicodeDecodeError:
            return response
        new_body = _ANCHOR_RE.sub(_rewrite_external_anchor, body)
        if new_body != body:
            response.set_data(new_body)
        return response

    # v2-6: regenerate slot caches at startup so a fresh checkout has populated cache.
    try:
        from blueprints.admin.cms.theme_slots import regenerate_all_slots
        regenerate_all_slots()
    except Exception:
        pass

    # v2-6: register slot_render Jinja global so base.html can include theme MD.
    try:
        from blueprints.admin.cms.theme_slots import slot_render
        app.jinja_env.globals['slot_render'] = slot_render
    except Exception:
        pass

    # v2-3: register render_md_with_blocks as Jinja global for templates
    # that render block-directive Markdown into HTML.
    try:
        from blueprints.admin.cms.blocks.renderer import render_md_with_blocks
        app.jinja_env.globals['render_md_with_blocks'] = render_md_with_blocks
    except Exception:
        pass

    # Demote heading levels by one (h1->h2, h2->h3, ..., h5->h6). Used by
    # region section pages that concatenate per-leaf rendered HTML inline:
    # the leaf's own <h1>title</h1> becomes <h2>, slotting under the page
    # header's h1, and subsequent heading levels shift accordingly.
    _DEMOTE_OPEN = re.compile(r"<h([1-5])(\b[^>]*)>", re.IGNORECASE)
    _DEMOTE_CLOSE = re.compile(r"</h([1-5])>", re.IGNORECASE)

    def _demote_headings(html: str) -> str:
        if not html:
            return html
        html = _DEMOTE_OPEN.sub(
            lambda m: f"<h{int(m.group(1)) + 1}{m.group(2)}>", html
        )
        html = _DEMOTE_CLOSE.sub(
            lambda m: f"</h{int(m.group(1)) + 1}>", html
        )
        return html

    app.jinja_env.filters['demote_headings'] = _demote_headings


    # v3: register page slot renderers as Jinja globals.
    try:
        from blueprints.admin.cms.page_slots import (
            page_slot_render, region_intro_render, nz_intro_render,
            davidsimmons_slot_render, regenerate_all_v3,
        )
        app.jinja_env.globals['page_slot_render'] = page_slot_render
        app.jinja_env.globals['region_intro_render'] = region_intro_render
        app.jinja_env.globals['nz_intro_render'] = nz_intro_render
        app.jinja_env.globals['davidsimmons_slot_render'] = davidsimmons_slot_render
        try:
            regenerate_all_v3(jinja_env=app.jinja_env)
        except Exception as _re_exc:
            import traceback
            print("[v3] regenerate_all_v3 failed:", _re_exc)
            traceback.print_exc()
    except Exception as _imp_exc:
        import traceback
        print("[v3] page_slots import / register FAILED — Jinja globals will be missing:", _imp_exc)
        traceback.print_exc()

    # v3 confirmation print — visible at startup so PI can verify registration.
    _have = [k for k in ('slot_render', 'render_md_with_blocks',
                         'page_slot_render', 'region_intro_render',
                         'nz_intro_render', 'davidsimmons_slot_render')
             if k in app.jinja_env.globals]
    print(f"[v3] Jinja globals registered: {_have}")
    print(f"[v3] missing:                   {sorted(set(('slot_render','render_md_with_blocks','page_slot_render','region_intro_render','nz_intro_render','davidsimmons_slot_render')) - set(_have))}")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
