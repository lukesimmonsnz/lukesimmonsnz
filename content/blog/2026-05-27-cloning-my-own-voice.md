---
title: "Cloning my own voice"
date: 2026-05-27
author: luke
summary: "A voice-cloning pipeline trained on my own audio — what it took to make it convincing, how the listener test went, and where I'll actually use it."
tags: [project-writeup, voice-clone, ai-audio, build-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

The narrator on the YouTube intro for my portfolio site isn't me reading a script. It's a model reading a script in my voice. I trained it on about 25 seconds of audio I recorded at my desk, it runs locally on an RTX 3070, and the first person I played it to who knows me well couldn't tell. That's the build log.

## The stack

The engine is **Chatterbox-Turbo** from Resemble AI — a ~350M-parameter zero-shot TTS model, MIT-licensed, released as `chatterbox-tts==0.1.7` on PyPI. Zero-shot is the load-bearing word: there's no fine-tuning step. You hand the model a reference clip of the target voice and a string of text, and it produces speech in that voice. The weights don't change between calls. The voice "training data" is just the reference clip.

I considered the obvious alternatives and ruled them out by licensing — Fish Speech (Apache 2.0) was the closest contender and lost on a blind-test, but XTTS-v2, F5-TTS, and Kokoro were all eliminated on license or fit before they got that far. The decision rule was strict: **MIT or Apache only**, because the YouTube channel this feeds into is monetised and I'd rather not discover a licensing problem after the fact.

The rest of the stack is Python 3.11 in a fresh venv, Torch + CUDA, and FFmpeg on PATH for muxing the narration onto scene images. Hardware is a Ryzen 7 7700X with an RTX 3070 (8 GB VRAM). VRAM peak on a two-line smoke run was **~3.3 GB**. The 8 GB ceiling only becomes a real constraint if I ever try to fine-tune on a larger corpus of my own audio, which I haven't and probably won't.

## The training data isn't really training data

This part is worth being honest about. With a zero-shot model, what most people would call "training" is really "providing a reference clip." There is no gradient step. The model has already been trained on huge multi-speaker corpora; what I'm giving it is a *prompt* in audio form that tells it which speaker to mimic.

The reference clip is `ref/my_voice.wav` — about 25 seconds of me reading paragraph-length text into a USB condenser mic in my home office. Mono, 24 kHz WAV, with a light cleanup pass in Audacity.

The quality lever everyone misses is that **clone quality is dominated by reference quality, not model choice**. Most of my time on this build wasn't writing code — it was re-recording the reference until the take was clean. Quiet room, no keyboard tapping, consistent mic distance, no hard breath sounds before the first word. I kept two versions — a calm explainer-VO reference and a slightly more energetic one — because the clone inherits prosody and energy from the sample. If I want the narrator to sound bored, I record the reference bored. The model copies what you give it.

If your clone sounds bad, the answer is almost never "use a bigger model." It's "record a better reference."

## The first time it sounded convincing

The smoke test was two throwaway lines:

> "This is the first line of the smoke test narration."
> "And this is the second line, generated as a separate file so a single bad take can be re-rolled."

First take, played through my desk speakers, I had the genuine *that's me* reaction — the timbre was right, the pace was right, the way I clip the end of "narration" was right. The first generation that worked was also the first generation, full stop. Zero-shot earns its name.

What it got wrong early — and still gets wrong occasionally — falls into three categories: **proper nouns** (less-common technical terms like Chatterbox or Ollama land the stress wrong, fixed by spelling them phonetically in the script), **hard consonant transitions** (back-to-back sibilants occasionally smear), and **question inflection** (rising intonation is hit-or-miss, and rephrasing as a statement is more reliable than relying on the question mark).

The pipeline writes one `.wav` per line, so `generate.py --only 7` re-rolls line 7 in isolation. First-take keep-rate is roughly 90%.

## The listener test

I played a 40-second narration sample to two people who know my voice well, without telling them what it was. Both reactions were variants of "yeah, what about it?" — they assumed I'd recorded it. When I told them it was a clone, the response was the kind of pause that's more informative than any analysis: they replayed it twice, listening for the seam, and couldn't find one.

The artefacts a trained ear can catch, if they're listening for them: a slight flatness to the prosody on longer sentences, occasional consonant smearing on fast clusters, and a subtle but consistent lack of the breath-and-restart pattern you get from a real human reading aloud. None of these jump out in normal listening. All of them would be obvious in a 10-minute audiobook.

That's the honest bound: it passes for short-form narration, where listeners aren't braced for it. It would not pass for a 30-minute podcast, where the cumulative absence of human pacing irregularities would start to register as *off*.

## The disclosure call

The choice that took the most thought wasn't technical. It was framing.

Using a voice clone as the narrator on my own portfolio site is meta. It's also exactly the kind of thing that could feel deceptive if I didn't say what it is. So I made the rule explicit, for myself: **the narrator is disclosed as a clone, on the page, in plain text.** The site copy frames it as "the narrator is an AI voice clone trained on Luke's voice" — not buried in a footer, but in the intro context where you'd encounter it on first watch.

The reasoning is consequentialist, not deontological. I don't think there's anything inherently wrong with using a voice clone. I do think there's something wrong with using one in a context where the listener would reasonably assume it's a human, and not telling them. Disclosure is the easy fix for the easy version of the problem.

One technical detail worth mentioning: Chatterbox bakes in **PerthNet (Implicit)**, Resemble AI's inaudible audio-provenance watermark, on every output. The audio is identifiable as Chatterbox-generated to anyone running a detector. It's the right default for a model used on monetised content.

## Where I'll use it next, and where I won't

**Will use:**

- YouTube intro narration on the portfolio site (the current target).
- Voiceover for short project demos — sub-2-minute videos where the disclosure framing is in the intro.
- Drafts of longer narrations, to hear how a script lands before I decide whether to record it properly.

**Won't use:**

- Anything where the clone could plausibly be mistaken for me speaking live, without disclosure.
- Long-form podcasts or audiobooks. The honest quality bound says: not yet.
- Anything that involves saying things I wouldn't actually say. The model is willing. I'm the constraint.

The next question, and the one I'm deferring, is whether to fine-tune on a larger sample of my own audio. Zero-shot at this quality is already past my disclosure threshold for the use cases I actually have. I'll revisit if it starts to feel limiting. It hasn't yet.

*— Luke Simmons, Auckland*
