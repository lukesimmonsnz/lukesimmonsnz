---
title: "How a 7B local LLM actually processes a job listing"
date: 2026-05-28
author: luke
summary: "A layer-by-layer walkthrough of the Job Scout scoring loop — from Python function call to transformer forward pass — plus what the replacement dashboard does instead, and why the second approach is more honest about what each tool is good for."
tags: [project-writeup, post-mortem, job-scout, local-llm, transformer, ollama]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## Why this document exists

The [post-mortem on Job Scout](/blog/2026-05-28-why-i-dropped-a-7b-local-llm-from-my-job-aggregator/) explains *what* failed: the 7B model was wrong about 30–40% of location verdicts, and it incorrectly excluded "Junior Front End Developer" as manual labour. This one is about mechanisms — *why* that kind of failure is predictable, not a bug or a bad prompt but a structural property of how these models work. The same pattern shows up everywhere people use small LLMs for judgment-shaped tasks.

---

## Layer 1 — The Python wrapper

Here's the `score_job` function from `scout_mvp.py`, with comments added for this walkthrough:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
MAX_TO_SCORE = 80

def score_job(job: dict) -> dict | None:
    # 1. Truncate long descriptions to fit the context window.
    #    3,500 characters ≈ ~900 tokens at typical English density.
    #    The model has 8,192 tokens total, so this leaves ~7,200 tokens
    #    for the system prompt + output.
    desc = job["description"]
    if len(desc) > 3500:
        desc = desc[:3500] + "\n…[truncated]"

    # 2. Assemble the user-turn payload: structured fields + description.
    #    This is the "document" the model will reason about.
    user_payload = (
        f"TITLE: {job['title']}\n"
        f"COMPANY: {job['company']}\n"
        f"LOCATION: {job['location_raw']}\n"
        f"TAGS: {', '.join(job['tags'])}\n"
        f"SALARY: {job['salary_raw'] or 'unspecified'}\n"
        f"---\n{desc}"
    )

    # 3. Ollama request body.
    body = {
        "model": MODEL,
        "prompt": user_payload,
        "system": SYSTEM_PROMPT,   # ~40 lines encoding Luke's profile + scoring rubric
        "format": "json",          # constrained decoding — explained in Layer 4
        "stream": False,           # wait for complete response, not token-by-token
        "options": {
            "temperature": 0.1,    # near-deterministic — peaks the probability distribution sharply
            "num_ctx": 8192,       # context window size in tokens
        },
    }

    # 4. Synchronous HTTP POST to the local Ollama server.
    #    timeout=180 because inference on 7B takes ~10-30s depending on load.
    try:
        resp = requests.post(OLLAMA_URL, json=body, timeout=180)
        resp.raise_for_status()
    except requests.RequestException as e:
        return None

    # 5. Unwrap: Ollama returns {"response": "<json string>", "done": true, ...}
    #    The inner response is the model's output, already valid JSON (enforced
    #    by constrained decoding).
    envelope = resp.json()
    raw_output = envelope.get("response", "")
    return json.loads(raw_output)   # parse model output into a Python dict
```

Then back in the main loop:

```python
def composite(v: dict) -> float:
    # Weighted average of three 0–100 scores the model returned.
    return (
        0.45 * _num(v.get("growth"))
        + 0.35 * _num(v.get("relevance"))
        + 0.20 * _num(v.get("attainability"))
    )
```

Pipeline: **fetch listing → format as text → POST to Ollama → get back JSON with growth/relevance/attainability + exclude flag + reason → compute composite → sort top 10**. What happens inside that POST is where the interesting machinery lives.

---

## Layer 2 — Ollama as a server

Ollama is a Go HTTP server wrapping `llama.cpp`. On first use it memory-maps the Qwen2.5-7B weights (~4.5 GB in Q4_K_M quantisation) into the RTX 3070's 8 GB VRAM, with room left for the KV cache. The combined system prompt + user payload is tokenised via Qwen's BPE vocabulary (~150K tokens) — most job-listing payloads land around 800–1,200 of the 8,192-token window. The token sequence runs through the forward pass (Layer 3), generating output one token at a time with invalid JSON tokens masked at each step (Layer 4). Because `stream: false`, Ollama accumulates 300–500 output tokens (each ~50–100ms on the 3070) before returning — hence the 180-second timeout — and wraps them in a response envelope:

```json
{
  "model": "qwen2.5:7b",
  "response": "{\"excluded\": false, \"exclude_reason\": \"...\", \"growth\": 75, ...}",
  "done": true,
  "eval_count": 312,
  "eval_duration": 18400000000
}
```

The actual model output is the `response` field — a JSON string that `score_job` parses.

---

## Layer 3 — What the transformer actually does

This is the level most people skip, and it's the one that explains the failure modes.

### Tokens are not words

The model doesn't see text. It sees a sequence of token IDs. "Junior Front End Developer" tokenises to something like `[14571, 11657, 8770, 30567]` — each ID is an index into the vocabulary. Before any computation, each ID gets converted to a high-dimensional vector (an *embedding*) — about 3,584 floats for Qwen2.5-7B.

### 28 layers of attention + feed-forward

The sequence of embeddings passes through 28 transformer blocks. Each block does two things:

1. **Self-attention:** Each token looks at every other token in the context and adjusts its own representation based on which tokens are "relevant" to it. This is the mechanism that creates context — "Developer" can pull in signal from "Junior" and "Front End" earlier in the sequence. Concretely, a matrix multiplication over queries, keys, and values — expensive but parallelisable on GPU.

2. **Feed-forward network:** A two-layer MLP applied to each position independently. This is where the model's "world knowledge" mainly lives — associations baked in during pretraining.

After all 28 layers, each token position has a rich contextual embedding. The last token's embedding is what matters for prediction.

### KV cache

Ollama caches the key and value matrices from each layer after the initial forward pass, so subsequent token generations only need to attend the new token against cached keys/values. This is why generation speeds up after the prompt is processed.

### Temperature 0.1

After the final layer, the model produces a *logit vector* — one float per vocabulary token. To turn logits into probabilities:

```
softmax(logits / temperature)
```

With `temperature: 1.0` the distribution is mildly peaked. With `temperature: 0.1` the division sharpens it dramatically — the top token gets almost all the mass. You're almost always sampling the mode, so output is consistent across runs. It doesn't make output *correct* — it makes it consistently wrong in the same way if the model's probability estimates are off.

---

## Layer 4 — Constrained decoding and why it makes hallucinations look confident

`format: "json"` enables Ollama's constrained decoding mode. This is the feature most responsible for the confident-looking wrong answers.

### How it works

At each generation step, before sampling, Ollama applies a *logit mask* derived from a JSON grammar and the current partial output. Any token that would produce syntactically invalid JSON gets zeroed out. The model can only generate tokens that keep the JSON valid — no unclosed strings, no missing commas, no unquoted keys, no wrong structural types. The output is **always syntactically valid JSON**, even if the model is completely confused about the content.

### Why this is dangerous

The mask enforces *syntax*, not *semantics*. The model still has to produce *some* value for `exclude_reason`, so it produces whatever string has the highest probability given the context — plausible-sounding, not necessarily correct. For "Junior Front End Developer", the high-probability completion after `"requires "` (given the physical-office and "hands-on" cues in the description) was `"manual labour"`. Likely given the preceding tokens; not grounded in what the role actually requires.

Constrained decoding makes this worse in one specific way: correct and incorrect JSON look identical. Free-form hallucinations ramble, hedge, contradict themselves — they're visible. JSON-mode hallucinations are crisp, structured, and authoritative-looking. The `"nz_remote_eligible": false` verdicts that were wrong 30–40% of the time came with coherent `exclude_reason` values like `"appears to require US work authorization"`. Structured, plausible, wrong.

---

## The replacement — what `app.py` does instead

### SQLite schema (same as before, no change here)

```sql
CREATE TABLE IF NOT EXISTS jobs (
    id           TEXT PRIMARY KEY,
    source       TEXT NOT NULL,
    source_id    TEXT,
    url          TEXT,
    title        TEXT,
    company      TEXT,
    location     TEXT,
    description  TEXT,
    posted_at    TEXT,
    salary       TEXT,
    tags         TEXT,
    fetched_at   TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'new'
);
```

No `score`, no `exclude_reason`, no `growth`, no `attainability`. The database stores what was actually observed — nothing inferred by a model that might be wrong.

### Location classification — deterministic regex

```python
AUCKLAND_RE  = re.compile(r"\bauckland\b", re.I)
NZ_CITIES_RE = re.compile(
    r"\b(wellington|christchurch|hamilton|tauranga|dunedin|napier|nelson|"
    r"rotorua|new plymouth|palmerston north|whangarei|invercargill|queenstown|"
    r"hastings|gisborne|whanganui|pukekohe)\b",
    re.I,
)
NZ_RE     = re.compile(r"\b(new zealand|aotearoa|\bnz\b|north island|south island)\b", re.I)
REMOTE_RE = re.compile(r"\b(remote|worldwide|anywhere|telecommute|wfh|work from home)\b", re.I)

def classify_location(location: str) -> str:
    """Return one of: loc:auckland, loc:remote, loc:nz-other, loc:overseas-onsite, loc:unknown."""
    if not location or location.strip() in ("—", "-"):
        return "loc:unknown"
    has_remote = bool(REMOTE_RE.search(location))
    has_akl    = bool(AUCKLAND_RE.search(location))
    has_other_nz_city = bool(NZ_CITIES_RE.search(location))
    has_nz     = bool(NZ_RE.search(location))

    if has_akl:
        return "loc:auckland"
    if has_remote and not has_other_nz_city:
        return "loc:remote"
    if has_other_nz_city or (has_nz and not has_remote):
        return "loc:nz-other"
    if has_remote:
        return "loc:remote"
    return "loc:overseas-onsite"   # conservative: unknown → assume overseas
```

This doesn't *infer* that "Remote (US)" is NZ-ineligible from plausible-sounding reasoning. It looks at the string and returns a label. Ambiguous inputs return `loc:unknown` and stay in the feed — don't hide things you're unsure about. The LLM's failure was inventing reasons *why* a listing was ineligible; this function doesn't reason, it pattern-matches on observable strings.

### Focus classification — tiered regex matching

```python
PRIORITY_RE = re.compile(
    r"\b(python|rust|machine[- ]learning|deep[- ]learning|pytorch|"
    r"llm|gpt|claude|nlp|ai[- ]engineer|ml[- ]engineer|mlops|"
    r"generative[- ]ai|rag\b|retrieval[- ]augmented|ai[- ]agent|"
    r"rlhf|ai[- ]safety|alignment[- ]research|"
    r"developer[- ]advocate|devrel|developer[- ]relations)\b",
    re.I,
)
TECH_RE = re.compile(
    r"\b(engineer|developer|software|programmer|devops|sre|infrastructure|"
    r"backend|frontend|fullstack|technician|network|audio|sound|broadcast)\b",
    re.I,
)
NONTECH_RE = re.compile(
    r"\b(sales[- ]executive|account[- ]executive|accountant|bookkeeper|"
    r"chef|cook|driver|cashier|cleaner|nurse|hospitality|warehouse|forklift)\b",
    re.I,
)
DOMAIN_NONTECH_RE = re.compile(
    r"\b(pharmacy|aviation|civil[- ]engineer|traffic[- ]engineer|"
    r"structural[- ]engineer|mechanical[- ]engineer|electrical[- ]engineer|"
    r"chemical[- ]engineer|food[- ]technologist)\b",
    re.I,
)

def compute_flags(job: dict) -> list[str]:
    flags = [classify_location(job.get("location") or "")]

    title     = job.get("title") or ""
    raw_tags  = job.get("tags") or ""
    desc_head = (job.get("description") or "")[:1500]
    haystack  = " ".join([title, job.get("company") or "", raw_tags, desc_head])

    has_priority    = bool(PRIORITY_RE.search(haystack))
    title_tech      = bool(TECH_RE.search(title))
    title_nontech   = bool(NONTECH_RE.search(title)) or bool(DOMAIN_NONTECH_RE.search(title))
    has_tech_any    = title_tech or bool(TECH_RE.search(desc_head))
    has_nontech_any = title_nontech or bool(NONTECH_RE.search(haystack)) or bool(DOMAIN_NONTECH_RE.search(haystack))

    if has_priority:
        flags.append("focus:priority")
    elif title_nontech:
        flags.append("focus:non-tech")
    elif has_tech_any:
        flags.append("focus:tech")
    elif has_nontech_any:
        flags.append("focus:non-tech")

    return flags
```

Title-level non-tech signals override description-level tech signals — the inverse of the LLM's behaviour. A front-end developer job that mentions "you'll be hands-on" doesn't get excluded. `DOMAIN_NONTECH_RE` handles cases like "Electrical Engineer", which in a job-listing context almost always means a utilities role rather than software.

### Filter endpoint — human does the judgment

```python
@app.route("/api/jobs")
def api_jobs():
    q       = (request.args.get("q") or "").strip().lower()     # keyword search
    source  = request.args.get("source") or ""                   # remoteok | remotive | hn | ...
    status  = request.args.get("status") or "active"             # active | starred | hidden
    eligible = request.args.get("eligible", "1") == "1"          # filter to AKL + remote only
    focus   = request.args.get("focus", "tech")                  # priority | tech | all
    days_param = request.args.get("days", "30")                   # recency filter

    # ... (SQL query + Python-side filtering) ...

    # eligibility filter: drop overseas-onsite and NZ-other-only
    if eligible:
        loc = next((f for f in flags if f.startswith("loc:")), "loc:unknown")
        if loc in ("loc:nz-other", "loc:overseas-onsite"):
            continue

    # focus filter: priority | tech | all
    if focus == "priority":
        if "focus:priority" not in flags:
            continue
    elif focus == "tech":
        if not ("focus:priority" in flags or "focus:tech" in flags):
            continue

    # keyword search with word boundaries (prevents "rust" matching "trust")
    if q_patterns:
        hay = " ".join([title, company, location, description[:3000], tags])
        if not any(p.search(hay) for p in q_patterns):
            continue

    # Priority-tagged jobs float to the top
    out.sort(key=lambda j: 0 if "focus:priority" in j["flags"] else 1)
    return jsonify(out)
```

The dashboard gives the human:
- **Location + focus filters** — AKL/remote toggle and priority/tech/all tiers
- **Keyword search** — word-boundary regex, so `?q=rust` doesn't surface "trust administration"
- **Star / hide / recency** — persistent per-listing status in SQLite, plus 7/30/90-day windows

The human looks at the filtered list and decides what to apply for. Triage takes ~10 minutes for 40 listings. That's all it needs to do.

---

## The actual comparison

| | LLM scoring (`scout_mvp.py`) | Regex + dashboard (`app.py`) |
|---|---|---|
| **Location verdicts** | ~60–70% accurate | ~95% accurate (on clearly-stated locations) |
| **Focus classification** | Inconsistent; over-excluded on edge cases | Consistent; transparent exclusion logic |
| **Latency** | ~15–30s per listing × 80 listings = 20–40 min | Sub-second for any filter change |
| **Failure mode** | Confident wrong answers, hard to spot | Miss (unknown label) rather than misflag; transparent |
| **Debuggability** | "Why did the model exclude this?" requires re-running | Read the regex; it's a function with 10 lines |
| **Where the judgment sits** | Model (unreliable) | Human (reliable, and that's appropriate) |

---

## The lesson as a system design principle

Both systems do the same top-level task: surface job listings worth reading. They differ in *where they put the hard parts*. `scout_mvp.py` offloaded the fuzziest cases — "is this actually manual labour?", "is this truly NZ-remote-eligible?" — to the model. Constrained decoding forced confident-looking output, but the output was pattern-matching against surface text, not reasoning about the real-world referent. `app.py` keeps the hard parts with the human: deterministic classification on observable signals, human judgment on the rest.

The principle: **route extraction tasks to small models or code; route judgment tasks to humans or large models.** Extraction is "pull these fields out of this text." Judgment is "decide whether this text implies a real-world property it doesn't directly state." Small models are reliable at the first and unreliable at the second. This isn't an argument against local LLMs — it's an argument for being precise about which sub-task you're giving them, and testing on the hard cases, not the easy ones.

---

*Companion to: [Why I dropped a 7B local LLM from my job aggregator](/blog/2026-05-28-why-i-dropped-a-7b-local-llm-from-my-job-aggregator/) — the same project, one layer higher.*

*— Luke Simmons, Auckland*
