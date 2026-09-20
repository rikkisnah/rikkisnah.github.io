---
title: "How I Humanize Articles With AI"
date: 2026-09-19T09:00:00-07:00
draft: true
tags: ["AI", "Writing", "Claude Code", "Codex", "Originality.ai", "Grammarly", "Content"]
categories: ["Writing", "AI"]
summary: "My seven-step workflow for writing with AI and still sounding like me: brainstorm for weeks, research and draft with Claude Code and Codex in minutes, humanize with a public prompt, score with Originality.ai, then edit by hand. Plus my answer to whether that is cheating, and the same prompt run in the voices of Barack Obama, Ernest Hemingway, William Faulkner, and Dario Amodei."
images:
  - /posts/humanize-with-ai/lead.png
---

![A desk with a laptop showing a markdown draft in VS Code, a red pen, and a small robot handing over a page](/posts/humanize-with-ai/lead.png)

*1,929 words · 10 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

*Image: The illustration above was generated with Grok. Figures 1 and 2 are my own drawings.*

**Related readings from this blog:**

- [Beyond the Slop: How to Write With AI Without Sounding Like a Bot](/posts/beyond-the-slop-ai-writing-without-sounding-like-a-bot/) - the prompt template this workflow grew out of

## The Week That Became Two Days

Before the AI wave, writing an article took me a week or more, from idea to paper. Now, with Claude/ChatGPT, the same article takes me at most two days, and most of those days go to my own editing and polishing. This post explains my workflow step by step, how long it takes, and answers the ethical question often asked: Is this cheating and an affront to human creativity?

As back in the golden writing days - when a typewriter was the tool that enabled some of the greatest literature to be created (fun fact: I learned typing in Mauritius, from my mom's old typewriter) - I use the following tools (they are paid but worth it): [Cursor](https://cursor.com) - my AI editor; [Claude Code](https://claude.com/claude-code) and [Codex CLI](https://github.com/openai/codex) for research and analysis; a homegrown prompt to humanize and voicify the text; [Grammarly](https://www.grammarly.com) or Word (for grammar checks); and [Originality.ai](https://originality.ai) to check the AI slop (one of the best tools on the market for AI slop detection).

## The Seven Steps

![Figure 1: the seven steps with the minutes each one takes, and the two hours at the end](/posts/humanize-with-ai/fig-01-seven-steps.png)

1. Brainstorming ideas - this is where the machine can't replace you. I use voice notes/chit sheets/Slack etc. (Also, lately I experimented with Voice mode from ChatGPT and Claude - they are really good for brainstorming ideas - a different blog would warrant this - it is in my draft). Time spent here ~ 1-2 weeks (creativity takes time).
2. Do the research around the idea. I use Claude Code and Codex's ability to access tools (web or research data, books, etc.). At times, if the material is not on the public internet - books from publishers or PDFs - I point the model to the artifacts locally. This takes about 5-10 minutes.
3. With the research on hand and your earlier creative chit sheets, draft a messy doc - don't worry about grammar. This takes about 10-15 minutes.
4. Ask both Claude and Codex to draft from your messy doc in different worktrees (or copies); the goal is to get the best two AI minds to give you a version of your ideas. This takes about 2 minutes.
5. Use a humanizer prompt ([I share my version](/posts/humanize-with-ai/prompt-pack/README.md)) to add your voice (or an author you admire) to make it personal. Then use Word grammar check or Grammarly to remove all grammar errors. About 2 minutes.
6. Score the draft with an AI moderator paragraph by paragraph. I use [Originality.ai](https://originality.ai) as it is the best I have seen on the market. It has amazing features to highlight AI slop and plagiarism visually (and more importantly, it doesn't promise you options to fix the AI writing - because you can't really ask AI not to write AI; similarly, you can't ask a human being not to be a human).
7. Edit the paragraphs in your editor (Word or Grammarly) till you get a personal and unique doc translating your creative idea into a unique document.

Steps 2 to 5 take under an hour, while Steps 6 and 7 are the time sink and can easily take 2-3 hours. But the process is essential to make it a human-written article, instead of the dryness and verbosity that comes from blind AI write-ups.

**Explain it to a ten-year-old.** The robot can build the Lego set fast. I still take every brick off the table and put it back by hand. That is the slow part, and it is the part that makes it my house.

## Removing the AI Grammar From the Draft

The AI detector is just a detector - it shows you where to look. Tools like Originality.ai use a custom language model trained to tell the two apart [1] (funny, isn't it, an AI auditing another AI language - a swarm of agents: one is writing, the other is checking for errors). Detectors like GPTZero measure the "perplexity" (how predictable words are - because AI uses token predictability based on a huge corpus of data) and "burstiness" (the variance of sentence length - because human writing is not consistent) [2]. If the text is predictable and structurally similar, the system flags it as machine-generated.

The human prompt I use (I wrote it for my writings, but there are better ones, I am sure - do use it, and if you like it, buy me a coffee when you are in Seattle) removes most of the easy patterns and the usual AI patterns - like dashes, usual AI patterns / Claudish / ChatGPTism - such as not X but Y [3]. It tells the model to keep everything concise.

At this point in the journey, we are using tools. The last and most difficult step, which tools don't help with but adds humanity to your text, is editing the drafts using your voice paragraph by paragraph. It is hard because it takes time, and the onus is on you to get it where you want - this part no machine can replace.

![Figure 2: one paragraph before and after the hand edit, with the flagged phrases marked](/posts/humanize-with-ai/fig-02-paragraph-edit.png)

Also, be careful about overreliance on AI detectors. I have seen many cases where they flag human writing as AI [4]. And don't use Humanizer tools - they are scams, in my opinion [5]. I rely solely on detectors as a scoring mechanism to identify paragraphs that need rewriting or clarification, because AI tends to be very verbose and at times confusing.

**Explain it to a ten-year-old.** A spell checker underlines the wrong words, but it cannot tell you what you meant to say. The AI checker underlines the sentences that sound like a robot. Only I know what I saw that day, so only I can fix the sentence.

## Using AI for Writing - Is It Cheating or an Affront to Human Creativity?

My answer is an emphatic No. A purist - I know many of them - would say the old way is better to write an article: one person and one keyboard being clacked continuously, like with an old typewriter. I understand that viewpoint (I love literature and am a voracious reader), but using AI writing will be the de facto writing tech and will, in fact, augment human creativity. The process of getting an idea down on paper (or the web) still needs you to audit, edit, and polish it. You will be surprised how well the process works.

Major publishing institutions have embraced Gen AI. [ACM](https://www.acm.org/publications/policies/new-acm-policy-on-authorship) allows Gen AI to be used as long as it is disclosed, is respectful of the quality of the text, and there is no plagiarism [6]. [Nature Portfolio](https://www.nature.com/articles/d41586-023-00191-1) and [Medium](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy) have adopted similar policies to a certain degree [7][8]. The line in the sand is that you are upfront about the disclosure of using AI and don't take credit for work that is not yours - aka plagiarism. I started that practice in all my articles, where I openly disclose the AI tools and reference where I am getting my materials. [Paul Graham](https://paulgraham.com/writes.html) said, "writing is thinking," and "there's a kind of thinking that can only be done by writing" [9]. I am 100% on board with this (and I love the writing culture Amazon - my previous employer - and OCI - my current employer - have: no projects are approved till it is written down and explained to a senior exec [10]).

## Use My Humanizer Prompt to Write Like the Great Thought Leaders of Our Decade

My humanizer prompt from Step 5 is public. I have used it across all of the frontier models for my writings - Claude Code, Codex, and Grok (Grok is still new and still not there yet compared to Claude and Codex). The pack, with my voice prompt and four example voices, is in the [prompt-pack folder](/posts/humanize-with-ai/prompt-pack/README.md) next to this post, and in the [same folder on GitHub](https://github.com/rikkisnah/rikkisnah.github.io/tree/humanize-with-ai-article/static/posts/humanize-with-ai/prompt-pack). Start with [the ready-to-paste version in my voice](/posts/humanize-with-ai/prompt-pack/prompts/humanize-prompt-rik-kisnah.md).

Below, I will show its use with 4 great thought leaders and amazing writers by running one short, machine-sounding paragraph using the prompt and watching the responses in their voices. The leaders (I'm a big fan of them for their writing and thinking process): [Barack Obama](https://en.wikipedia.org/wiki/Barack_Obama), [Ernest Hemingway](https://en.wikipedia.org/wiki/Ernest_Hemingway), [William Faulkner](https://en.wikipedia.org/wiki/William_Faulkner), and [Dario Amodei](https://en.wikipedia.org/wiki/Dario_Amodei).

The input:

> In today's fast-paced world, documentation is not just a nice-to-have, it's the cornerstone of engineering excellence. It is important to note that clear, concise, and comprehensive docs foster collaboration, drive innovation, and ensure long-term success. Isn't it time we asked why writing things down matters? In conclusion, great documentation is a testament to a team's commitment.

In my voice:

> Every team I have joined had the same gap: the code was there and the doc was not. Documentation is part of the engineering, and the cheap part. A clear doc lets two engineers work on one system without a meeting, and it lets the next hire start without someone standing behind them. Write it down while you still remember why.

As Barack Obama:

> Let me be clear. Documentation matters. It matters to the engineer who joins next month, and it matters to the one who leaves next year. When we write down what we know, we hand our work to the people who come after us, and that is how a team outlasts any one of us. So write it down. We owe each other that much.

As Ernest Hemingway:

> Write the docs. Write them clear and write them short and write them before you forget. The team reads them and the team works and no one asks twice. The engineer who comes after you reads them too. He does not know you. He knows the docs. That is enough.

As William Faulkner (his voice asks for long sentences, so the prompt lets it run):

> Because the code was there, had always been there, the way the house had been there before any of them were born and would be there after, but the reason for it was gone, gone with the man who wrote it and never wrote it down, so that the ones who came after (the new ones, the ones who had not watched it built) stood before it as before a locked door, and the doc, the plain small doc that would have been the key, had never been made, and would not be

As Dario Amodei:

> I think the case for documentation is simpler than people make it. To be clear, writing things down is not free, and I could be wrong about how much it pays back on a small team. My guess is that the return comes from a mechanism: a written doc lets a second engineer act without asking the first, which removes the bottleneck of one person's memory.

TL;DR: one prompt on a text; the prompt removes the AI-ism and adds the voice of famous writers and thought leaders. I have a voice I could adapt because, with time, I developed my own writing style which I could send to the AI tool (if you don't have one, pick someone whose writing you love, adopt it in your own documents, and after 10 or 20 documents you have enough to create your own AI writing voice).

## Summary of This Post

1. With AI tools, you can compress weeks of writing into 1-2 days.
2. Let the AI models do the grunt work - research, restructure, remove AI-isms from the text, and add a unique writing voice style to the doc.
3. Use AI detectors to score each paragraph.
4. Edit the paragraphs yourself - make it unique to you.
5. If you use AI, give credit to the machine, yourself, and your readers - don't embrace plagiarism. Fable and Astra will remember it, and beware of the wrath of the machine.

## References

1. Originality.ai, How does AI content detection work: https://originality.ai/blog/how-does-ai-content-detection-work
2. GPTZero, What is perplexity and burstiness for AI detection: https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
3. Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
4. Liang et al., GPT detectors are biased against non-native English writers, Patterns, 2023: https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7
5. Pangram, What is a humanizer?: https://www.pangram.com/blog/what-is-a-humanizer
6. ACM, New ACM Policy on Authorship (generative AI): https://www.acm.org/publications/policies/new-acm-policy-on-authorship
7. Nature, Tools such as ChatGPT threaten transparent science; here are our ground rules for their use, January 2023: https://www.nature.com/articles/d41586-023-00191-1
8. Medium, Artificial Intelligence (AI) content policy: https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy
9. Paul Graham, Writes and Write-Nots, October 2024: https://paulgraham.com/writes.html
10. Jeff Bezos, 2017 Letter to Shareholders (six-page narrative memos instead of PowerPoint): https://www.aboutamazon.com/news/company-news/2017-letter-to-shareholders

<!-- draft-claude.md: Rik's own edit of 2026-09-19 replaced the judged text. Claude only fixed typos, added references and links. Body word count (references excluded): 1,929 -->
