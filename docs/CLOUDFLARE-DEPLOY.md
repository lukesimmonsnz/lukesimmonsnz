# Cloudflare Pages deployment

How this site gets from a local Flask process on Luke's machine to
`https://lukesimmonsnz.kiwi` — hosted entirely by Cloudflare so the origin
machine can be off.

## Big picture

```
 Current website/        [DRAFT]    Local Flask on :5000.
       │                            Edit freely with Claude; the scheduled
       │                            task keeps charts/maps/docs fresh.
       │
       ▼ scripts/freeze.py
 _site/                  [BUILD]    Static HTML + assets.
       │                            Walks every route via Flask's test
       │                            client; writes <path>/index.html.
       │                            Draft-status blog posts are skipped.
       │
       ▼ wrangler pages deploy
 lukesimmonsnz.kiwi      [LIVE]     Cloudflare Pages edge.
       │                            Always on. Computer can be off.
       │
       └─ /api/contact           Cloudflare Pages Function at
                                  functions/api/contact.js — handles
                                  form POST, Turnstile verification,
                                  Resend email delivery.
```

## One-time setup

Do these once, in order. After that the day-to-day loop is just
`freeze` → `deploy`.

### 1. Domain in Cloudflare DNS

1. Sign in to the [Cloudflare dashboard](https://dash.cloudflare.com/).
2. Add `lukesimmonsnz.kiwi` as a site (if not already). Cloudflare will
   give two name servers — set those on the domain at your NZ registrar.
3. Wait for DNS propagation (usually < 1 hour) and verify the domain
   shows as active in the dashboard.

### 2. Produce the first build locally

The Cloudflare UI asks you to **upload assets before naming the project**,
so you need a `_site/` folder ready on disk first.

In the project root:

```
set SITE_URL=https://lukesimmonsnz.kiwi
set CONTACT_SUBMIT_URL=/api/contact
:: TURNSTILE_SITE_KEY is optional on this first build; add it once the
:: widget exists (step 5). Without it, the form renders without the
:: Turnstile widget but the Pages Function still expects a token, so
:: don't ship publicly until step 5 is done.
python scripts/freeze.py
```

You should see something like `[freeze] done. 49 OK, 0 failed.` and a
populated `_site/` folder.

### 3. Create the Pages project (upload-first flow)

1. In the dashboard: **Workers & Pages → Create → Pages → Upload assets**.
2. Drag your local `_site/` folder onto the upload target (or **Select
   from computer** and pick the `_site/` folder).
3. **After the files finish uploading**, Cloudflare prompts for a project
   name — e.g. `lukesimmonsnz`. Submit.
4. You now have a Pages project with a first deploy at
   `https://<project>.pages.dev/`. That's your pre-domain preview URL.

### 4. Custom domain

1. In the new Pages project: **Custom domains → Set up a custom domain**.
2. Enter `lukesimmonsnz.kiwi`. Cloudflare automatically creates the CNAME
   record because the domain is on their DNS.
3. Optionally add `www.lukesimmonsnz.kiwi` as an alias.

### 5. Environment variables

In the Pages project: **Settings → Environment variables → Production**.
Add, as **encrypted** values:

| Name                   | Where it comes from                                      |
| ---------------------- | -------------------------------------------------------- |
| `TURNSTILE_SECRET_KEY` | Cloudflare → Turnstile → add a widget → secret half      |
| `RESEND_API_KEY`       | [Resend dashboard](https://resend.com/api-keys)          |
| `CONTACT_TO`           | `luke@lukesimmonsnz.kiwi`                                |
| `CONTACT_FROM`         | `form@lukesimmonsnz.kiwi` (verified sender on Resend)    |

No other secrets are needed by the Function; the Turnstile **site key**
(public) is baked into the HTML by the freezer — see step 6.

### 6. Turnstile widget

1. Cloudflare dashboard → **Turnstile → Add widget**.
2. Site: `lukesimmonsnz.kiwi`. Hostnames: same.
3. Mode: **Managed** (default). Cloudflare will show a challenge only when
   its heuristics flag the visitor.
4. Copy the **site key** (public, starts `0x4AAAAA...`) and the
   **secret key** (private).
5. Put the secret into the Pages env vars as `TURNSTILE_SECRET_KEY`
   (step 5).
6. Keep the site key handy — it goes into `scripts/deploy.bat` as
   `TURNSTILE_SITE_KEY` so the freezer can bake it into the HTML.
7. Re-run `scripts/deploy.bat` so the published HTML now includes the
   Turnstile widget.

### 6. Resend sender verification

1. Sign up at [resend.com](https://resend.com). Free tier is 3,000 emails
   per month — ample for a contact form.
2. Add a domain: `lukesimmonsnz.kiwi`. Resend shows three DNS records
   (MX / TXT / DKIM) — add each to Cloudflare DNS for the domain.
3. Wait for verification (minutes to an hour).
4. Create an API key, copy the value into Pages env vars as
   `RESEND_API_KEY` (step 4).

### 7. Install Wrangler

Wrangler is Cloudflare's CLI. On Windows:

```
npm install -g wrangler
wrangler login
```

`wrangler login` opens a browser so you can authorise the CLI against
your Cloudflare account. One-time step.

## Day-to-day loop

Every time you want to push local changes live:

```
set SITE_URL=https://lukesimmonsnz.kiwi
set CONTACT_SUBMIT_URL=/api/contact
set TURNSTILE_SITE_KEY=0x4AAAAA...               :: the PUBLIC site key
python scripts/freeze.py
wrangler pages deploy _site --project-name lukesimmonsnz
```

The freezer wipes `_site/` at the start of each run, so the output is a
full snapshot. `wrangler pages deploy` diffs against the edge and only
uploads changed assets.

You can also script both steps in `scripts/deploy.bat`:

```bat
@echo off
setlocal
cd /d "%~dp0.."

set SITE_URL=https://lukesimmonsnz.kiwi
set CONTACT_SUBMIT_URL=/api/contact
set TURNSTILE_SITE_KEY=<your-site-key>

call .venv\Scripts\activate.bat
python scripts\freeze.py || exit /b 1
wrangler pages deploy _site --project-name lukesimmonsnz
```

## Pages Function: how the contact form works live

The file [`functions/api/contact.js`](../functions/api/contact.js) is
automatically wired to `https://lukesimmonsnz.kiwi/api/contact` by
Cloudflare's file-based router. On each POST:

1. Parses the form fields.
2. Calls `https://challenges.cloudflare.com/turnstile/v0/siteverify` with
   the submitted Turnstile token + your secret. Rejects on failure.
3. Validates name / email format / topic / message.
4. Calls Resend with `CONTACT_FROM` → `CONTACT_TO`, putting the
   submitter's address in `reply_to` so your reply lands with them.
5. Redirects (303) to `/contact/thanks/`.

Any validation failure redirects to `/contact/?error=<code>`; the tiny
JS on the contact page surfaces a matching human message from a fixed
list.

## What stays on your machine

- Flask process on `http://127.0.0.1:5000` — the live draft you edit.
- `content/blog/*.md` with `status: draft` — not frozen, not shipped.
- `agent/daily_drafts/` — never shipped.
- `data/messages.jsonl` — obsolete once the Pages Function is the
  production contact handler; kept as legacy for local Flask dev.
- The Windows scheduled task `lukesimmonsnz-regen-docs` — keeps
  `docs/SITEMAP.md`, the auto-blocks in `README.md` / `ARCHITECTURE.md`,
  and the rendered charts/maps in sync with the content.

## What stays on Cloudflare

- Every file under `_site/` at the last deploy.
- The Pages Function at `functions/api/contact.js`.
- DNS for `lukesimmonsnz.kiwi`.
- The Turnstile widget's configuration.

## What stays with a third-party

- Resend holds your API key and records the emails it sends. They do
  not host the site content.
- Google Fonts serves `Fraunces` and `Inter` from their edge (as before).
  If you ever want total privacy control, self-host the WOFF2 files.

## Rollback

`wrangler pages deployment list --project-name lukesimmonsnz` shows
previous deploys. To roll back:

```
wrangler pages deployment rollback <deployment-id> --project-name lukesimmonsnz
```

Pages keeps 20 previous deployments by default, so recent mistakes are
cheap to undo.
