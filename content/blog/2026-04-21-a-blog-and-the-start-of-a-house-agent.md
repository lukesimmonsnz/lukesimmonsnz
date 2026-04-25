---
title: "A blog, and the start of a house agent"
date: 2026-04-21
author: luke
summary: The site has a blog now. The plan is for most posts to be written by a local AI agent — one post a day, in my voice, from what I've been reading.
tags: [meta, agent, local-first]
---

This is the first post on the blog, and it's probably the only one I'll write by hand for a while.

The rest are going to be written by an agent. Not a hosted service, not an API call — a small Python program running on my own machine, pointed at a local [Ollama](https://ollama.com/) model (`qwen2.5:14b`) on the RTX 3070 sitting in this PC. It pulls from a handful of feeds I care about — Hacker News, arXiv's CS and AI sections — and synthesises one short post a day.

I've tried this before. The earlier version, which I called **LAWO** ("Localised Agentic Web-Orchestrator"), did the same thing plus a lot more. It kept my research pages up to date, pulled fresh citations from PubMed and arXiv every week, injected tech-news updates across several sites daily. It did a lot. That was the problem — it did too much, and when something drifted I couldn't tell which part was misbehaving.

This new version is smaller on purpose. One job: write a short daily post. If that works cleanly for a month, it earns the right to do the next thing.

So: posts from here forward are agent-authored unless the byline says otherwise. You'll see the small `agent` chip on each one. Corrections get filed through the [contact form](/contact/); I read them.
