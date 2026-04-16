# PROJECT BRIEFING — lukesimmonsnz.kiwi

## What this is
My personal website hosted on GitHub Pages at lukesimmonsnz.kiwi. Plain HTML/CSS only — no frameworks, no build tools, no JavaScript libraries.

**Repo:** `lukesimmonsnz/lukesimmonsnz` on GitHub. The `main` branch is live. Work on `dev` branch locally, push to `main` only when I say "push to live".

---

## File structure
```
index.html      — Home page
projects.html   — Projects (GitHub repos, roadmap, archive)
gaming.html     — Gaming platforms and games
blog.html       — Blog posts (all drafts/templates currently)
contact.html    — Experience + contact details
start.bat       — Double-click to start local server (Windows)
start.sh        — Double-click to start local server (Mac)
Cover Photo.jpg — NZ landscape used as page header background
CNAME           — lukesimmonsnz.kiwi
README.md       — Has an auto-updating changelog table
```

---

## Design system
Used consistently across all pages:
```css
--bg-base:        #0a0a0a
--bg-surface:     #111
--bg-card:        #141414
--bg-card-hover:  #1c1c1c
--border:         #1e1e1e
--border-hover:   #3a3a3a
--text-primary:   #f0f0f0
--text-secondary: #aaa
--text-muted:     #555
--accent-tech:    #8888ff   /* blue-purple, used for AI/tech */
--accent-gaming:  #88cc88   /* green, used for gaming */
```

---

## Shared patterns on every page
- Fixed translucent nav bar (50px height, backdrop-filter blur, z-index 100)
- Page header with `Cover Photo.jpg` as background + dark gradient overlay
- Site-wide footer with links to all pages + email + AI acknowledgement
- Nav links: Home · Projects · Gaming · Blog · Contact (active page gets `.active` class)

### Nav HTML
```html
<nav class="site-nav">
  <div class="nav-inner">
    <a class="nav-logo" href="index.html">Luke Simmons</a>
    <div class="nav-links">
      <a href="index.html" class="nav-link">Home</a>
      <a href="projects.html" class="nav-link">Projects</a>
      <a href="gaming.html" class="nav-link">Gaming</a>
      <a href="blog.html" class="nav-link">Blog</a>
      <a href="contact.html" class="nav-link">Contact</a>
    </div>
  </div>
</nav>
```

### Footer HTML
```html
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-nav">
      <a href="index.html">Home</a>
      <a href="projects.html">Projects</a>
      <a href="gaming.html">Gaming</a>
      <a href="blog.html">Blog</a>
      <a href="contact.html">Contact</a>
      <span class="footer-divider">·</span>
      <a href="mailto:luke@lukesimmonsnz.kiwi">luke@lukesimmonsnz.kiwi</a>
    </div>
    <div class="footer-bottom">
      <span class="footer-copy">lukesimmonsnz.kiwi &nbsp;·&nbsp; New Zealand</span>
      <span class="footer-ai">Designed &amp; built with <a href="https://claude.ai/code" target="_blank" rel="noopener">Claude AI</a> by Anthropic</span>
    </div>
  </div>
</footer>
```

### Page header background
Used on all secondary pages:
```css
.page-header {
  padding: 5rem 2.5rem 2rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(10,10,10,.55) 0%, rgba(10,10,10,.82) 60%, #0a0a0a 100%),
              url('Cover%20Photo.jpg') center 30%/cover no-repeat;
}
```

---

## About Luke
- Based in New Zealand
- Studying AI/software engineering via Codecademy (Python, ML, backend, cybersecurity, game dev)
- Volunteer audio engineer at Gracecity Church (2021–present) and Manukau City Baptist Church (2010–2018)
- Gamer: RuneScape, World of Tanks, Chess (Diamond member on Chess.com, handle: nzgamerluke)
- Streaming on Twitch: nzgamerluke
- YouTube: @nzgamerluke (gaming) and @lukesimmonsnz (main channel)
- Instagram: @nzgamerluke
- Email: luke@lukesimmonsnz.kiwi
- Career goal: AI engineer

---

## Things still to do
- David Simmons Archive section on `projects.html` needs real content (currently "Coming Soon" placeholder)
- Blog posts are all template drafts written by Claude — replace with real content when ready
- GitHub streak stats image (herokuapp) may be unreliable — can replace with a native stat box if needed

---

## Git workflow
- **Local preview:** double-click `start.bat` (Windows) or `start.sh` (Mac) — opens localhost:8000
- **Day-to-day:** commit to `dev` branch
- **Go live:** push to `main` — GitHub Pages deploys in ~60 seconds
- After pushing to `main`, the auto-changelog bot commits back — always `git pull` before the next push to `main`

---

## Rules
- Do not add JavaScript libraries or frameworks
- Keep all styles in `<style>` tags inside each HTML file — no separate CSS files
- Do not change the colour scheme or nav/footer structure without being asked
- Do not push to `main` unless explicitly asked to "push to live"
