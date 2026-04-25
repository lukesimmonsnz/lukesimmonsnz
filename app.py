import os
import re

from flask import Flask, render_template

from blueprints.main import main_bp
from blueprints.research import research_bp
from blueprints.davidsimmons import davidsimmons_bp
from blueprints.blog import blog_bp
from blueprints.auckland import auckland_bp


# Absolute base for feeds, sitemap, and Open Graph tags. Default is local-only.
# Set SITE_URL in .flaskenv (or the process env) before deploying so the feed
# and sitemap emit real URLs instead of 127.0.0.1.
SITE_URL_DEFAULT = "http://127.0.0.1:5000"

# Hosts whose links should stay in the same tab (our own pages). Anything
# else with an http(s) href gets target="_blank" rel="noopener" added by the
# after-request filter below.
_OWN_HOSTS = ("127.0.0.1", "localhost", "lukesimmonsnz.kiwi")

_ANCHOR_RE = re.compile(r"<a\s+([^>]*?)>", re.IGNORECASE | re.DOTALL)


def _rewrite_external_anchor(match: "re.Match[str]") -> str:
    attrs = match.group(1)
    # Preserve any anchor that already has target= set — the template author
    # made an explicit choice.
    if re.search(r"\btarget\s*=", attrs, re.IGNORECASE):
        return match.group(0)
    href = re.search(r'href\s*=\s*"(https?://[^"]+)"', attrs, re.IGNORECASE)
    if not href:
        return match.group(0)  # relative / mailto / fragment — leave alone
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
    app.register_blueprint(auckland_bp, url_prefix="/research/auckland")

    # Deployment switches — populated from the process environment so the
    # same templates render correctly under both the local Flask origin
    # (dev) and the Cloudflare Pages static build (prod).
    app.config["TURNSTILE_SITE_KEY"] = os.environ.get("TURNSTILE_SITE_KEY", "").strip()
    app.config["CONTACT_SUBMIT_URL"] = os.environ.get("CONTACT_SUBMIT_URL", "").strip()

    # Make site-level constants available in every template without passing
    # them through every render_template call.
    @app.context_processor
    def _inject_site():
        return {
            "site_url": app.config["SITE_URL"],
            "site_name": app.config["SITE_NAME"],
            "site_tagline": app.config["SITE_TAGLINE"],
            "turnstile_site_key": app.config["TURNSTILE_SITE_KEY"],
            "contact_submit_url": app.config["CONTACT_SUBMIT_URL"],
        }

    @app.errorhandler(404)
    def _not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def _server_error(e):
        return render_template("500.html"), 500

    @app.after_request
    def _open_external_links_in_new_tab(response):
        """Post-process HTML responses so every off-site link opens in a new
        tab. Same-tab is preserved for our own domain (and 127.0.0.1 /
        localhost for dev), and for any anchor that already carries an
        explicit target attribute."""
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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
