---
title: "How I Humanize Articles With AI"
date: 2026-09-19T09:00:00-07:00
draft: true
tags: ["AI", "Writing", "Claude Code", "Codex", "Originality.ai", "Grammarly", "Content"]
categories: ["Writing", "AI"]
summary: "The seven steps I use to write with AI and still sound like me: think for days, draft by hand, let Claude Code and Codex research and restructure, humanize with a prompt, then spend the real hours with Originality.ai one paragraph at a time. And my answer to whether that is cheating."
images:
  - /posts/humanize-with-ai/lead.png
---

![A desk with a laptop showing a markdown draft in VS Code, a red pen, and a small robot handing over a page](/posts/humanize-with-ai/lead.png)

*989 words · 5 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

*Image: The illustration above was generated with Grok. Figures 1 and 2 are my own drawings.*

**Related readings from this blog:**

- [Beyond the Slop: How to Write With AI Without Sounding Like a Bot](/posts/beyond-the-slop-ai-writing-without-sounding-like-a-bot/) - the prompt template this workflow grew out of

## The Week That Became Two Days

Before these tools, a 1,200 to 3,000 word article took me about a week. Now, once the idea is settled, the same article takes at most two days, and most of those two days go to my own editing. This post is the workflow, step by step, with the time each step takes, and my answer to the question I get most, whether this counts as cheating.

Three tools do all the work. Cursor or VS Code holds every draft, so the work stays visual and I can see the whole file at once. VS Code also runs the quick LLM passes. Claude Code or Codex CLI does everything else: the research, the restructuring, and the humanize pass.

## The Seven Steps

![Figure 1: the seven steps with the minutes each one takes, and the two hours at the end](/posts/humanize-with-ai/fig-01-seven-steps.png)

1. Brainstorm and draft the idea. The thinking can take days. That is the creative part, and no tool shortens it. The written draft of the idea takes under 30 minutes.
2. Research against that draft. I hand it to Claude Code, Codex, and Perplexity and ask them to check the facts and find sources. About 5 to 10 minutes.
3. Write a messy draft from the research. About 10 minutes. Dirty and incomplete on purpose: I want my argument and my examples on the page before the model gets near it.
4. Ask Claude Code and Codex to turn the messy draft into an article. About 2 minutes.
5. Humanize the draft with prompts. About 1 minute. Then run Word or Grammarly for grammar. Another minute.
6. Score the draft with an AI moderator. Originality.ai is the best I have used. It highlights the phrasing that sounds like a model, and I review one paragraph at a time.
7. Edit paragraph by paragraph in Word or Grammarly.

Add up the minutes and steps 1 to 5 come to under an hour once the idea is settled. Steps 6 and 7 are the slow part. They easily take 1 to 2 hours, and they are where the article becomes mine.

**Explain it to a ten-year-old.** The robot can build the Lego set fast. I still take every brick off the table and put it back with my own hands. That is the slow part, and it is the part that makes it my house.

## What the Score Catches

The detector is a smoke alarm. It tells me where to look. Originality.ai marks sentences, and the marks land on the same handful of habits every time. Wikipedia's editors keep a public list of those habits, built from thousands of flagged drafts: em dashes where a comma would do, "not just X but Y", lists of exactly three, "serves as" instead of "is", and a closing paragraph that repeats the piece [1]. Juzek and Ward counted 21 words that jumped in scientific abstracts after 2022, and pointed at the human feedback used to train the models as the likely cause [2].

The humanize prompt in step 5 removes most of the easy ones. Mine bans the dashes, bans the word list from my Beyond the Slop post, forbids the "not X but Y" pattern, and tells the model to keep every fact and add none. It runs in a minute and it fixes the surface.

The hard flags survive that pass. What remains is what only I can fix: a paragraph with no number in it, a claim with no name attached, an example the model made generic because it has never stood in a data center. That is why step 7 is done by hand, one paragraph at a time. A prompt cannot add an experience I have not written down yet.

Two cautions on detectors. They fail in both directions: Liang and colleagues ran seven detectors on 91 essays by non-native English speakers and more than half were flagged as AI [3]. And the "humanizer" tools that swap synonyms to beat the score make the text worse, and the newer detectors are trained on their output anyway [4]. I use the score to pick the paragraphs to reread, and that is its only job.

![Figure 2: one paragraph before and after the hand edit, with the flagged phrases marked](/posts/humanize-with-ai/fig-02-paragraph-edit.png)

**Explain it to a ten-year-old.** A spell checker underlines the wrong words, but it cannot tell you what you meant to say. The AI checker underlines the sentences that sound like a robot. Only I know what I saw that day, so only I can fix the sentence.

## Is It Cheating

A purist would say the old way is cleaner: one person and one week at the keyboard. I understand the view, and I still think it is worth it, because I humanize the result. Every fact was checked and every paragraph passed through my hands. My name is on it, and I stand behind every sentence.

The published policies land in the same place. ACM lets authors use generative AI if they disclose it and stay responsible for the text [5]. Nature Portfolio wants substantial use declared in the methods section and does not count copyediting [6]. Medium asks for a disclosure in the first two paragraphs [7]. None of them forbids the tools, and none of them treats them as a spell checker. The line they all draw is disclosure plus responsibility. That is why every post on this site carries a caveat line above the first heading.

Paul Graham's worry is the one I take most seriously: writing is how thinking happens, so people who stop writing stop thinking [8]. My answer is step 1. The days of thinking and the 30 minutes of drafting are still mine, and no tool touches them.

## The Whole Post in Five Lines

1. Think for days, then draft by hand in under 30 minutes.
2. Let the models research, restructure, and humanize in under 15 minutes.
3. Score the draft with Originality.ai and read every flagged paragraph.
4. Edit the flagged paragraphs yourself. Budget 2 hours.
5. Disclose it, then sign it.

## References

1. Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
2. Juzek and Ward, Exploring the Sources of Lexical Overrepresentation in Large Language Models, arXiv 2412.11385: https://arxiv.org/abs/2412.11385
3. Liang et al., GPT detectors are biased against non-native English writers, Patterns, 2023: https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7
4. Pangram, What is a humanizer?: https://www.pangram.com/blog/what-is-a-humanizer
5. ACM Policy on Authorship, as restated by SIGCSE TS 2025: https://sigcse2025.sigcse.org/info/policies-ai
6. Nature Portfolio AI policy, CASRAI summary: https://casrai.org/dictionary/term/nature-portfolio-ai-policy
7. Medium, Artificial Intelligence (AI) content policy: https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy
8. Paul Graham, Writes and Write-Nots, October 2024, quoted by Medium: https://medium.com/blog/a-world-divided-into-writes-and-write-nots-is-more-dangerous-than-it-sounds-218cbb18ed89

<!-- draft-claude.md: after one pass of task-2-humanize-prompt/best-prompt-claude.md over draft-raw-claude.md. Body word count (references excluded): 989 -->
<!-- Humanize pass changes: removed "not X, it is Y" contrasts in the opening paragraph, the smoke-alarm line, the "surface is not" line, and "I do not write for the score"; turned the "is this cheating?" question into a statement; broke the "one person, one keyboard, one week" triad and the "Every fact. Every paragraph. My name." anaphora; simplified "Nobody serious ... nobody serious" to "None of them ... none of them". No facts added or removed. -->
