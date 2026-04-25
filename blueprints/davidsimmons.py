from flask import Blueprint, render_template

from data.david_simmons import PERSON, EDUCATION, AWARDS, TIMELINE, WORKS, REFERENCES

davidsimmons_bp = Blueprint("davidsimmons", __name__)


@davidsimmons_bp.route("/")
def index():
    return render_template(
        "davidsimmons/index.html",
        person=PERSON,
        awards=AWARDS,
        recent_works=[w for w in WORKS if w.get("year", 0) >= 1984][:4],
    )


@davidsimmons_bp.route("/about/")
def about():
    return render_template(
        "davidsimmons/about.html",
        person=PERSON,
        education=EDUCATION,
        awards=AWARDS,
    )


@davidsimmons_bp.route("/timeline/")
def timeline():
    events = sorted(TIMELINE, key=lambda e: (e["year"], e.get("type", "")))
    types = sorted({e["type"] for e in events})
    return render_template(
        "davidsimmons/timeline.html",
        person=PERSON,
        events=events,
        types=types,
    )


@davidsimmons_bp.route("/works/")
def works():
    by_category = {}
    for w in sorted(WORKS, key=lambda w: w["year"]):
        by_category.setdefault(w.get("category", "publication"), []).append(w)
    return render_template(
        "davidsimmons/works.html",
        person=PERSON,
        by_category=by_category,
    )


@davidsimmons_bp.route("/references/")
def references():
    return render_template(
        "davidsimmons/references.html",
        person=PERSON,
        references=REFERENCES,
    )
