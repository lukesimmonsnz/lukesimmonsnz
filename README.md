# Luke Simmons — lukesimmonsnz.kiwi

Personal portfolio and link-in-bio website hosted via GitHub Pages at [lukesimmonsnz.kiwi](https://lukesimmonsnz.kiwi).

---

## About

Software Development & AI student at Codecademy, aspiring AI Engineer & Researcher, gamer and chess enthusiast based in New Zealand. Open to remote work opportunities and collaborations.

📫 [luke@lukesimmonsnz.kiwi](mailto:luke@lukesimmonsnz.kiwi)

---

## What's on the site

- **Hero section** — NZ landscape background with profile photo, name, and email link
- **Identity strip** — Live GitHub profile data: bio, location, follower/following/repo counts, and member-since date pulled automatically from the GitHub API on every page load
- **Tech & AI section** — Codecademy profile link, Backend Developer Roadmap card with interactive version link, and currently-studying skill tags (Python, Machine Learning, Cybersecurity, Game Dev)
- **Gaming section** — Links to Twitch, YouTube (NZGAMERLUKE & Luke Simmons NZ), Chess.com, and Instagram
- **Contact strip** — Email link with a call to action for remote opportunities
- All external links open in a new tab

---

## Tech

- Plain HTML + CSS — no frameworks, no build process
- Hosted on GitHub Pages with a custom domain (CNAME: `lukesimmonsnz.kiwi`)
- GitHub API integration: fetches live profile data from `api.github.com/users/lukesimmonsnz` at page load with static fallback content if the API is unavailable

---

## Changelog

<!-- CHANGELOG_START -->
| Date (UTC) | What | Files |
|------------|------|-------|
| 2026-04-13 09:43 | Add auto-changelog GitHub Action and backfill README history | `.github/workflows/update-readme.yml` |
| 2026-04-13 | Add GitHub profile link and live stats cards to Tech section | `index.html` |
| 2026-04-13 | Update README with site overview and Claude AI acknowledgement | `README.md` |
| 2026-04-13 | Expand bio card to show up to 3 lines of text | `index.html` |
| 2026-04-13 | Open all external links in a new tab | `index.html` |
| 2026-04-13 | Pull live GitHub profile data onto the page via API | `index.html` |
| 2026-04-13 | Use GitHub avatar for profile picture | `index.html` |
| 2026-04-13 | Fix hero background image filename to match Cover Photo.jpg | `index.html` |
| 2026-04-13 | Website redesign — hero, identity strip, roadmap card, asymmetric grid, contact strip | `index.html` |
<!-- CHANGELOG_END -->

---

## AI Acknowledgement

This website was redesigned and developed with the assistance of **Claude** (Anthropic's AI), used via [Claude Code](https://claude.ai/code). Claude helped plan the layout, write and refactor the HTML/CSS, implement the GitHub API integration, debug image loading issues, and manage git commits and pushes throughout the process.
