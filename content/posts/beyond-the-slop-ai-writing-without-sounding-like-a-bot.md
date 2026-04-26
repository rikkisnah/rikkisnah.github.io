---
title: "Beyond the Slop: How to Write With AI Without Sounding Like a Bot"
date: 2026-04-12T00:00:00-07:00
draft: false
tags: ["AI", "writing", "LinkedIn", "prompt engineering", "content"]
---

![Beyond the Slop: Write With AI Without Sounding Like a Bot](/posts/beyond-the-slop-ai-writing-without-sounding-like-a-bot/lead.png)

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references. I also used several models and Grammarly in a multi-pass workflow; the prompt pack is linked just below, with more context in the section titled "Prompt pack and tooling for this post."*

*Image: The illustration above was generated with Google Gemini.*

*My prompts (ZIP, Oracle Cloud Infrastructure): if you want to read exactly what I prompted for this article, download [2026-04-12-ai-slop-writing.zip](https://objectstorage.us-phoenix-1.oraclecloud.com/p/iJfWQcg_rgC5UNQYZKXpCCXnIAzfMtFcqGO1XVxgcukmJgcEJigbFHCg07hPMdoK/n/axbtr6skl2h2/b/rikkisnah-github-media/o/2026-04-12-ai-slop/2026-04-12-ai-slop-writing.zip).*

# Beyond the Slop: How to Write With AI Without Sounding Like a Bot

Last month, I ran three of my own LinkedIn drafts through GPTZero. Two came back flagged "likely AI." I had written all three myself, but after two years of leaning on ChatGPT, my own voice had drifted toward the mean.

I am not alone. An [Originality.AI](http://Originality.AI) analysis of **8,795 long-form LinkedIn posts across 82 months** found that **54% of long posts on LinkedIn are likely AI-generated**, with volume jumping **189%** after ChatGPT launched in late 2022 [1]. A 2025 follow-up tracking 3,368 posts from 99 influential profiles found that the number was **53.7%** [2]. This is the AI slop era: fluent prose with very low signal. The tools did not make us worse writers. We let them.

## Why LLM prose reads as "slop."

You usually feel it before you can name it. A 2025 Florida State University paper presented at the *International Conference on Computational Linguistics* identified **21 "focal words"** that ChatGPT overuses in scientific writing, including *delve*, *intricate*, *pivotal*, *meticulous*, and *commendable*, and traced the overuse to reinforcement learning from human feedback, where annotators in specific regions preferred those words [3]. Beyond vocabulary, the EMNLP 2024 paper *Detection and Measurement of Syntactic Templates in Generated Text* found that generated text reuses syntactic templates at a measurable rate higher than human writing [4]. The sentences share both shape and wording.

The editorial tells are familiar: tricolon ("not X, not Y, but Z"), scaffolding phrases ("It's important to note," "In today's fast-paced world"), flat rhythm, safe, centrist takes, and a closing moral that would fit any topic. **Stacked em dashes** are another common signal: readers often associate long runs of em-dash breaks with model prose, where a comma, colon, or hyphen would read more naturally. That is still not proof of authorship on its own: *The Washington Post* and *Rolling Stone* both ran 2025 features arguing the em dash alone is a weak basis for a witch hunt, in part because the mark is common in training data and in human writing too [5]. On an edit pass, try replacing unnecessary em dashes with a hyphen (in compounds), a colon (before an explanation), or a comma (for a light pause), and keep only the breaks that still earn their place.

## What the research actually says

The honest question is not *whether* to use AI but *how*. A meta-analysis in *Nature Human Behavior* (October 2024) pooled **370 experimental results from 106 studies** and found that human-AI teams *underperformed on decision-making tasks but outperformed humans or AI working alone on creative and content-generation tasks* [6]. The same analysis flagged a darker pattern: when AI output was already good, humans deferred and stopped thinking. Slop creeps in at exactly the moment we relax.

A CHI 2024 study on human-AI co-writing reinforced this. More AI scaffolding improved productivity for some writers. However, it was accompanied by a measurable drop in text ownership and satisfaction [7]. The more the model writes for you, the less the piece feels like yours.

## A workflow that survives editing

This workflow is built on Madaan et al.'s *Self-Refine* (2023), which showed that iterative critique→revise loops using the same model as both generator and critic outperform one-shot generation across writing tasks [8], and on Anthropic's and OpenAI's published prompting guidance [9][10].

1. Start by outlining your thesis and three supporting points in a notebook *before* opening the LLM. Defend your point confidently; if you can't, AI won't help.
2. **Assemble a source pack.** Collect 5-10 real sources: PDFs, quotes, numbers. Paste them into the prompt. Anthropic recommends placing long documents near the top of the prompt and asking the model to extract quotes before answering [9]. Never let the model invent citations. A 2025 audit of eight chatbots found only **26.5%** of generated references were fully correct, while **39.8%** were partly or entirely fabricated [11].
3. **Write the first draft yourself by hand.** Use your natural voice and do not worry about perfection at this stage.
4. **Use the model as an editor, not an author.** Ask it to critique against your rubric, tighten sentences, and propose cuts: the Self-Refine pattern [8].
5. **After editing, cross-check every fact and number by running them through a second model with search capabilities and demand citations for each**.

## The anti-slop prompt template

This is the template I use, adapted from published prompt-engineering guidance [9][10]:

```
ROLE: You are my editorial partner. Help me publish a 1,000-1,200-word
LinkedIn article that sounds like an experienced professional, not generic AI.
AUDIENCE + GOAL: [e.g., senior engineers / product leaders].
After reading, they should [change their belief / adopt a practice / avoid a mistake].

THESIS: "[one-sentence claim]"
VOICE SAMPLES (mine): [paste 2-4 short excerpts from past posts]
NON-NEGOTIABLE RULES
- No generic opener ("In today's world…", "fast-paced landscape…").
- Do not lean on em dashes for clause breaks; prefer commas, colons,
  or hyphens unless an em dash is clearly best.
- Ban these empty verbs unless I explicitly allow: leverage, unlock,
  revolutionize, empower, seamless, robust, delve, pivotal, meticulous.
- Each paragraph must contain one claim + (a) a concrete example,
  (b) a specific mechanism, or (c) a number.
- No summary paragraph unless it introduces a NEW takeaway.
- If you cannot support a claim from the SOURCE PACK, mark it
  [NEEDS SOURCE]. Never fabricate.
SOURCE PACK: [paste quotes/snippets with titles and links]
TASK STAGING

1. Propose 3 distinct outlines (different argument spines).
2. For the outline I pick, produce a section-by-section evidence plan.
3. Draft ONLY after I approve the outline and evidence plan.
```
The banned-verb list and the task staging are the load-bearing parts. They narrow the output space *before* generation. This way, you don't have to sand clichés off afterward.

## Prompt pack and tooling for this post

The archive linked under the disclaimers above is the same file: [2026-04-12-ai-slop-writing.zip](https://objectstorage.us-phoenix-1.oraclecloud.com/p/iJfWQcg_rgC5UNQYZKXpCCXnIAzfMtFcqGO1XVxgcukmJgcEJigbFHCg07hPMdoK/n/axbtr6skl2h2/b/rikkisnah-github-media/o/2026-04-12-ai-slop/2026-04-12-ai-slop-writing.zip). It holds the prompts and staging I used while writing this article.

Across drafts and revisions I did not rely on a single vendor. I used **Google Gemini**, **xAI Grok**, **OpenAI ChatGPT**, and **Microsoft Copilot** in overlapping roles: brainstorming, structural critique, line-level edits, and chain-of-thought style passes where showing intermediate reasoning helped me decide what to keep. I also ran the text through **Grammarly** for grammar and clarity. The goal was a wider set of lenses on the same thesis, not a single model’s default voice.

## Measurable spot-checks before you publish

If you want to quantify slop risk, run four cheap checks on your draft. All are grounded in the linguistic-fingerprint literature [12]:

- **Sentence-length variance.** Standard deviation under ~4 words across a 1,000-word post signals monotone rhythm.
- **Transition-start rate.** If more than **20%** of sentences begin with "Moreover / However / Therefore / In addition / Ultimately," cut them.
- **Hedging rate.** Keep "may / might / could / likely / potentially" under roughly **1%** of tokens unless you are writing about uncertain evidence.
- **Flesch Reading Ease 50-70** for a LinkedIn general-professional audience. Plain does not mean dumb.

## Detectors are smoke alarms, not judges.

A detector returning "90% AI" is a prompt to inspect the draft, not a verdict on authorship. OpenAI discontinued its own AI text classifier in 2023, citing low accuracy [13]. Turnitin's own documentation warns its detector may misidentify text and should not be the sole basis for decisions [14]. In August 2025, the US Federal Trade Commission finalized an order against Workado for misrepresenting the accuracy of its AI content detection product [15]. Academic work shows that detectors can be defeated by paraphrasing [16] and struggle with mixed human-AI text [17]. Use detectors to trigger a closer read. Do the editorial work yourself.

## The real test

The point of writing is not to produce content. It is to be read, remembered, and sometimes disagreed with. A sharp mind with a good prompt still beats both a blank page and a lazy one. Garbage in, slop out. Borrowed voice in, forgettable article out. The writers who thrive will not be those who publish the most. Instead, they will be those whose writing still sounds like a person who made deliberate choices.

---

## References

[1] Originality.AI. "Over ½ of Long Posts on LinkedIn are Likely AI-Generated Since ChatGPT Launched." [https://originality.ai/blog/ai-content-published-linkedin](https://originality.ai/blog/ai-content-published-linkedin)

[2] Originality.AI. "50%+ of LinkedIn Posts were Likely AI in 2025 + Engagement Insights." [https://originality.ai/blog/linkedin-ai-study-engagement](https://originality.ai/blog/linkedin-ai-study-engagement)

[3] Liang, K., et al. "Why Does ChatGPT 'Delve' So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models." *Proceedings of the 31st International Conference on Computational Linguistics*, 2025. [https://arxiv.org/abs/2412.11385](https://arxiv.org/abs/2412.11385)

[4] Shaib, C., Elazar, Y., Li, J. J., & Wallace, B. C. "Detection and Measurement of Syntactic Templates in Generated Text." EMNLP 2024. [https://arxiv.org/abs/2407.00211](https://arxiv.org/abs/2407.00211)

[5] *The Washington Post*, "Some people think AI writing has a tell - the em dash. Writers disagree." April 9, 2025. [https://www.washingtonpost.com/technology/2025/04/09/ai-em-dash-writing-punctuation-chatgpt/](https://www.washingtonpost.com/technology/2025/04/09/ai-em-dash-writing-punctuation-chatgpt/) ; *Rolling Stone*. [https://www.rollingstone.com/culture/culture-features/chatgpt-hypen-em-dash-ai-writing-1235314945/](https://www.rollingstone.com/culture/culture-features/chatgpt-hypen-em-dash-ai-writing-1235314945/)

[6] Vaccaro, M., Almaatouq, A., & Malone, T. "When Combinations of Humans and AI Are Useful: A Systematic Review and Meta-Analysis." *Nature Human Behaviour*, October 2024. [https://mitsloan.mit.edu/press/humans-and-ai-do-they-work-better-together-or-alone](https://mitsloan.mit.edu/press/humans-and-ai-do-they-work-better-together-or-alone)

[7] Dhillon, P. S., et al. "Shaping Human-AI Collaboration: Varied Scaffolding Levels in Co-writing with Language Models." CHI 2024. [https://arxiv.org/abs/2402.11723](https://arxiv.org/abs/2402.11723)

[8] Madaan, A., et al. "Self-Refine: Iterative Refinement with Self-Feedback." 2023. [https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651)

[9] Anthropic. "Prompt engineering overview." [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

[10] OpenAI. "Best practices for prompt engineering with the OpenAI API." [https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

[11] Khosrowjerdi, M., et al. "Assessing the performance of 8 AI chatbots in bibliographic reference retrieval." 2025. [https://arxiv.org/abs/2505.18059](https://arxiv.org/abs/2505.18059)

[12] Reinhart, A., et al. "Do LLMs write like humans? Variation in grammatical and rhetorical styles." 2024 SwissText workshop analysis of linguistic fingerprints in generated text. [https://aclanthology.org/2024.swisstext-1.9.pdf](https://aclanthology.org/2024.swisstext-1.9.pdf)

[13] OpenAI. "New AI classifier for indicating AI-written text." (Discontinued notice.) [https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/)

[14] Turnitin. "Using the AI Writing Report." [https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)

[15] US Federal Trade Commission. "FTC Approves Final Order Against Workado, LLC, Which Misrepresented Accuracy of Its AI Content Detection Product." August 2025. [https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-approves-final-order-against-workado-llc-which-misrepresented-accuracy-its-artificial](https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-approves-final-order-against-workado-llc-which-misrepresented-accuracy-its-artificial)

[16] Sadasivan, V. S., et al. "Can AI-Generated Text be Reliably Detected?" 2023. [https://arxiv.org/abs/2303.11156](https://arxiv.org/abs/2303.11156)

[17] Zhang, Q., et al. "LLM-as-a-Coauthor: Can Mixed Human-Written and Machine-Generated Text Be Detected?" NAACL 2024. [https://arxiv.org/abs/2401.05952](https://arxiv.org/abs/2401.05952)