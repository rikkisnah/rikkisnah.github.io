---
title: "How I humanize articles with AI"
date: 2026-09-19T16:00:00-07:00
draft: true
tags: ["AI", "Writing", "Editing", "Prompt Engineering"]
categories: ["Writing", "AI"]
summary: "My process for turning an idea into an AI-assisted article, and why checking and editing each paragraph still takes most of the work."
images: []
---

*805 words · 5 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

## Two minutes to draft, hours to edit

Turning rough material into an article with AI takes me about two minutes. Reviewing and editing the paragraphs afterward can easily take one to two hours. The short drafting step gets plenty of attention. The work that follows deserves an explanation too.

I covered generic AI prose in [Beyond the Slop](/posts/beyond-the-slop-ai-writing-without-sounding-like-a-bot/). Here, I want to walk through how I actually write. These timings are estimates from my own workflow, not a benchmark. They also leave out the days I might spend deciding whether an idea is worth an article.

## Start with something to say

I draft in Cursor or VS Code so the work stays visual. I use VS Code for quick passes with a language model, and Claude Code or Codex CLI for everything else. I want the writing in front of me as I work through it.

Brainstorming comes first. Thinking can take days, and that is the creative part: finding what I want to say about a subject. Once the idea is there, writing the initial draft takes under 30 minutes. When I talk about saving time with AI, I still have to account for that thinking.

Then I research against the draft. Claude Code, Codex, and Perplexity help me check facts, usually in about five to ten minutes. Having something written gives the research a direction. For anyone trying this, compare each claim with its source and keep the qualifications attached. Several models agreeing with one another cannot replace reading the evidence.

## Leave room for the rough draft

From that research, I write a messy draft in about ten minutes. It is incomplete on purpose. I then ask Claude Code and Codex to turn the material into an article, which takes about two minutes.

Rough writing can make a missing explanation easier to spot. A polished sentence can conceal it. Saying that a tool saves time, for example, leaves a reader wondering whose time it saves and on what task. Here, I can describe my own timings. Turning those estimates into a claim about every writer would go beyond what I know.

Next, I apply a humanizing prompt, which takes about one minute. A grammar check in Word or Grammarly takes about another minute. After those passes, the article is ready for a close reading.

## Tell the prompt what to preserve

An editing prompt needs a clear job. My suggested starting point is to keep the facts, numbers, qualifications, and opinions while replacing generic phrasing with familiar words. Ask for varied sentence lengths and provide examples of your writing. Tell the model explicitly that it must not invent personal experience to make the article sound more natural.

Here is a made-up sentence: "The process offers significant productivity benefits." For the workflow in this article, I can replace it with "The article takes me at most two days once the idea is settled." The second sentence gives the reader a person, a duration, and a condition. Changing the adjective in the first sentence would leave the question unanswered. The prompt should make those details easier to read while leaving the underlying account intact.

Reading aloud can help too. Purdue OWL includes it in its revision advice. If you stumble over a sentence, stop and inspect it. You can hear some awkward passages without asking a model to score how closely they resemble your voice. [Purdue OWL](https://owl.purdue.edu/owl/general_writing/the_writing_process/proofreading/steps_for_revising.html)

## Read one paragraph at a time

I score the draft with an AI moderator. Originality.ai is the best option I have used to identify phrasing that sounds like AI. That is a personal preference; I am not claiming it is the most accurate detector available. I review one paragraph at a time and edit in Word or Grammarly.

The score gives me something to inspect. It cannot establish who wrote a passage. Sadasivan and colleagues found that paraphrasing could reduce detection rates for the systems they tested. A changed score does not prove human authorship or factual accuracy. [Sadasivan et al.](https://arxiv.org/abs/2303.11156)

Scoring and paragraph editing together easily take one to two hours. Those minutes spent generating and rewriting the draft tell only part of the story. Each paragraph still needs a decision: does it belong, does it say what I mean, and does the evidence support it?

## What I gain, and what I still owe the reader

Before these tools, a 1,200 to 3,000 word article took me about a week. Once the idea is settled, AI and this workflow get it done in at most two days. Those are personal estimates, with the final editing included.

A purist might say the old way is cleaner. I think this process is still worth it because I humanize the result. That is my opinion, and it does not answer every ethical question about AI-assisted writing. The Authors Guild, for example, recommends telling readers about substantial use of generated text. [Authors Guild](https://authorsguild.org/resource/ai-best-practices-for-authors/)

If you try this workflow, leave time for the paragraph review. Read the sentences, check their claims, and decide which ones you are willing to publish under your name.

## References

- Purdue OWL. [Steps for Revising](https://owl.purdue.edu/owl/general_writing/the_writing_process/proofreading/steps_for_revising.html).
- Sadasivan et al. [Can AI-Generated Text be Reliably Detected?](https://arxiv.org/abs/2303.11156), version 4, 2025.
- Authors Guild. [AI Best Practices for Authors](https://authorsguild.org/resource/ai-best-practices-for-authors/), 2026.

Body word count: 805 (references excluded).
