# Monetisation strategy

A structured view of the options, ranked by expected value **for Luke
specifically** — not for a generic personal-site owner. Written 2026-04-24
to answer the question: if 40 hrs/week on this site is effectively a
full-time job, what's the return?

---

## Bucket 1 — Career capital → income *(highest EV)*

The single highest-ROI use of the hours already sunk is **the site as a
portfolio**. What you've built is not "a blog" — it's a working
demonstration of senior-level engineering judgement:

- A typed-entity-graph with JSON-Schema validation, a lint gate that
  refuses to render when citations are missing, and a deterministic
  renderer. *That is a content-as-data system of the kind companies
  pay architects to design.*
- A two-stage local-agent pipeline (daily drafts → weekly synthesis) that
  demonstrates honest thinking about what LLMs are good at and how to
  structure around their limits.
- A fetcher architecture with declarative specs and automatic caching —
  generalisable to any upstream data source.
- A pure-SVG renderer (no matplotlib, no chart.js) that shows you can
  reason about rendering primitives rather than reaching for a library.
- Two operational modes (daily scheduled task + event-driven reactive)
  running reliably on the same box.

**How to cash this in:**

1. **Explicit "portfolio mode" section on the site** — a page that walks
   a recruiter or hiring manager through *what's interesting* about the
   engineering, not the content. File under /work/ or /portfolio/. Write
   it once; reuse in every application.
2. **A specific "systems I built" entry on LinkedIn and your CV** that
   links here. Not "I built a personal site" but "Auckland research
   content-as-data pipeline — 9 entity types, lint-gated, 140+
   committed YAML entities, deterministic SVG chart generation".
3. **AI/SWE job applications** explicitly citing the agent and fetcher
   work. You're studying AI; the site proves you can *ship* AI, not
   just talk about it.
4. **Open-source at least one component** — the fetcher architecture or
   the SVG chart renderer — as a small self-contained library on GitHub.
   Open-source footprint > private project for signalling.

**Expected value:** A mid-career AI/SWE role in NZ starts at roughly
NZ$120–160k. Having a credible public engineering portfolio moves you
into competitive territory for those roles 6–18 months earlier than you
otherwise would. That's the $50k+/yr delta I referenced — compounded
over a career, it dwarfs any direct revenue the site could realistically
produce.

---

## Bucket 2 — Direct monetisation *(thin and slow)*

Honest, ranked-best-first:

### Paid newsletter on Auckland research

**What:** Substack (or Ghost self-hosted on your machine) covering the
Auckland problems-and-solutions work at a frequency readers can rely
on — weekly or fortnightly. Free tier + paid tier (NZ$5–8/month) with
paid-only deeper analysis, briefings, or data.

**Pros:** Fits content you already produce. Auckland policy audience is
small but engaged and well-connected. Paid subscribers signal real
interest. Compounds over years.

**Cons:** Slow to ramp. Needs consistent weekly output for 12+ months
before there's meaningful revenue. You need to be OK with a paywall on
some research, which runs against the open-publishing grain of the
site. Substack takes 10%.

**Realistic range:** NZ$0–200/mo in year 1, NZ$500–2,000/mo in year 2–3
if it finds traction. Not a salary.

### Consulting using Auckland research as credential

**What:** Once you have 20–30 deeply-researched pages on Auckland
problems, the site becomes the credential that lets you charge for
"systems analysis" engagements — council submissions, private briefings
for property developers or advocacy groups, custom research.

**Pros:** Potentially high $/hr (NZ$150–300/hr is defensible with the
right positioning). Uses skills you're already building.

**Cons:** Requires **sales work** you're not currently doing — reaching
out, maintaining a network, writing proposals, negotiating scope. That
work is itself ~10 hrs/week if done properly. Compounding feedback loop
(clients lead to clients) only kicks in after 2–3 years.

**Realistic range:** Zero until you actively sell; NZ$30–80k/year
side-revenue is possible once the channel is established.

### Open-source the pipeline as a product / SaaS

**What:** Extract the content-as-data + lint-gated pipeline into a
general tool. Sell as hosted SaaS ("research-grade static sites for
policy analysts"), or open-source + support contracts.

**Pros:** Scales independently of your hours. Closest thing to
product-income in this list.

**Cons:** Very long-tail, uncertain product-market fit. Requires shifting
a material chunk of your hours from *doing research* to *building a
product* — different skill, different feedback loop. Most tools like
this don't find buyers.

**Realistic range:** Most likely outcome is zero revenue; tail upside is
a five-figure business. Don't plan on it.

### Donations / Ko-fi / Patreon

**What:** A "Buy me a coffee" button; maybe a Patreon tier for
supporters.

**Pros:** Cheap to set up. Non-commitment — readers give if they feel
like it.

**Cons:** Unreliable. Cool-looking sites with dedicated audiences still
struggle to crack NZ$200/mo this way. Adds visual noise to a site whose
current tone is research-serious.

**Recommendation:** Add a *small, unobtrusive* Ko-fi or similar link on
the `/now/` page or footer. Don't expect it to pay for anything.
Psychologically useful — a tiny signal that someone valued the work.

### Ads and sponsorships

**Don't.** The site's credibility depends on being seen as
independent research. Ads poison that, sponsorships compromise it. Even
non-branded display ads drop the perceived seriousness of the work
enough to hurt bucket 1. The cost is larger than the revenue.

---

## Bucket 3 — The scope question

Worth separating from the monetisation question entirely: **is 40 hrs/week
the right amount**?

The research itself has intrinsic value — to you, to the few hundred
people in Auckland's housing/policy world who will eventually read it,
and to any historian who wants to know what a systems-engineering
perspective on the city looked like in the 2020s. None of that needs
revenue to justify.

But if 40 hrs is interfering with either bucket 1 (job hunting,
open-source contributions, skill-building outside this project) or
generally sustainable living, the answer is probably not "find a way to
monetise the 40 hrs" but "reduce to 20 hrs and redirect the other 20 to
bucket 1".

**A reasonable split given what I know:**

- 10–15 hrs/week on the site — enough to keep the engine running
  (weekly digest, Auckland page every 1–2 weeks, pipeline maintenance).
- 10 hrs/week on **open-source contributions** to known AI/Rust/Python
  projects. Public commits on major projects move your CV faster than
  private work.
- 10 hrs/week on **applications + interview prep + talking to people in
  NZ's AI and housing policy communities**. Paid conversations follow
  unpaid ones by ~6 months.
- 5 hrs/week on **actual job hunting** — targeted applications, not
  spray-and-pray.

That's 40 hrs. It's the same total time but with a portfolio that
already proves the engineering case, aimed at salaried income which is
the only thing in this space that actually replaces a full-time job
within 6–12 months.

---

## What to build on the site to support these

Ranked by cost-to-add vs monetisation-relevance:

1. **`/work/` or `/portfolio/` page** — frames what a recruiter is
   looking at. One or two hours. Highest direct impact on bucket 1.
2. **"Colophon"-style technical breakdown of the pipeline** — link from
   the Auckland overview. Signals engineering seriousness without
   bragging. Maybe half a day.
3. **Newsletter signup form** — if you commit to the Substack path.
   Integrates with whichever provider you pick.
4. **Ko-fi link in the footer** — five minutes.
5. **"Work with me" page with a scoped consulting offer** — only when
   you're ready to take on consulting engagements. Three pages of
   content: what you do, what you've done, how to reach you.

None of this is urgent. Bucket 1 is where the hours you've already
invested pay off, if you choose to cash them in.
