"""
Projects listed on /projects/.

Each entry:
    title       — display name
    subtitle    — short tagline (optional)
    status      — "shipped", "in progress", "ongoing", "archived"
    year        — string, e.g. "2026" or "2024–present"
    stack       — list of short tech labels (rendered as chips)
    summary     — one-line lede
    description — one or more paragraphs (HTML allowed; keep it plain)
    links       — list of {"label": ..., "url": ...}; empty list is fine
"""

PROJECTS = [
    {
        "title": "lukesimmonsnz.kiwi",
        "subtitle": "This site",
        "status": "ongoing",
        "year": "2026–present",
        "stack": ["Flask", "Jinja2", "Python", "CSS"],
        "summary": (
            "A self-contained personal site — a home for my study notes and a "
            "biographical archive of my grandfather."
        ),
        "description": (
            "<p>Written from scratch in Flask with Jinja templates and a single "
            "hand-written stylesheet. No JavaScript framework, no site-owned "
            "analytics, no third-party scripts beyond Google Fonts. Content-driven: "
            "the biographical archive renders entirely from a structured Python "
            "data file.</p>"
            "<p>Currently fronted by Cloudflare while I&rsquo;m still on borrowed "
            "hardware; the architecture is designed to move to dedicated "
            "self-hosting without a rewrite. I&rsquo;m building it this way "
            "partly for privacy and control, partly because I want the whole "
            "stack to be something I understand end-to-end.</p>"
        ),
        "links": [],
    },
    {
        "title": "Auckland — problems and solutions",
        "subtitle": "A long-horizon, systems-engineering research project",
        "status": "in progress",
        "year": "2026–present",
        "stack": ["Python", "Flask", "JSON Schema", "YAML", "Jinja2"],
        "summary": (
            "A structural analysis of Auckland's problems and the solution "
            "camps that address them, written on a 10 / 50 / 100-year frame "
            "and generated from a typed entity graph rather than authored "
            "page-by-page."
        ),
        "description": (
            "<p>Content-as-data: every page is a view over a graph of "
            "typed entities — Problem, Evidence, Driver, Camp, Source, "
            "Metric, Actor — validated against JSON Schema and rendered "
            "through a Jinja pipeline. The aim is reproducibility, "
            "traceable citations, and durability across political "
            "cycles.</p>"
            "<p>Lives under Research as a fourth branch. First section "
            "is Housing, with subpages Land, Supply Economics, and "
            "Affordability; further Housing subpages and domains "
            "(Transport, Infrastructure, Environment, etc.) to come.</p>"
        ),
        "links": [
            {"label": "Auckland research project", "url": "/research/auckland/"},
        ],
    },
    {
        "title": "Local AI agent",
        "subtitle": "A personalised agent running on my own hardware",
        "status": "in progress",
        "year": "2026",
        "stack": ["Python", "Docker", "Ollama", "qwen2.5"],
        "summary": (
            "An AI agent that lives directly on my system — not a cloud service. "
            "Grew out of an earlier experiment (LAWO) that autonomously updated "
            "my websites; evolving now into a more general personal assistant."
        ),
        "description": (
            "<p>Built around Ollama running <code>qwen2.5:14b</code> locally on "
            "an RTX 3070, orchestrated in Docker with a Python watcher for "
            "filesystem events. The original prototype, LAWO (&ldquo;Localised "
            "Agentic Web-Orchestrator&rdquo;), kept my research sites up to date "
            "with daily blog injections and weekly regenerations from fresh "
            "literature searches.</p>"
            "<p>The direction now is more personal: an agent that knows my "
            "projects, my study plan, and the state of my machine, and that I "
            "can trust specifically because it never leaves my network.</p>"
        ),
        "links": [],
    },
]
