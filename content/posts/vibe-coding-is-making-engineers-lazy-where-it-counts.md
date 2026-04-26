---
title: "Vibe Coding Is Making Engineers Lazy Where It Counts"
date: 2026-04-19T10:00:00-07:00
draft: false
tags: ["AI", "software engineering", "vibe coding", "developer productivity", "skill decay"]
---

![Vibe Coding Is Making Engineers Lazy Where It Counts](/posts/vibe-coding-is-making-engineers-lazy-where-it-counts/lead.png)

*1,658 words · 8 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

*Image: The illustration above was generated with xAI Grok.*

## The Moment I Keep Having

I keep having the same moment (deja vu over deja-vus) with vibe coding. I reopen a file I touched three days earlier, and the first thing that comes back is the prompt, not the error handling or the thought process in writing. The code passed the CI. The feature or article shipped fast. Yes, I still need a few minutes (at times, hours) to rebuild the mental model of something that now sits in production. A week ago, I wrote about [AI slop in writing](https://rikkisnah.github.io/posts/beyond-the-slop-ai-writing-without-sounding-like-a-bot/). This post is about its more evil sibling. I baptized it as cognitive slop in code and writing.

## The Productivity Is Real

I strongly believe in vibe coding, which is why the downside bothers me. Between Claude Code, Cursor, and Codex CLI, my own output has climbed roughly 150% in writing and 200% in GitHub activity. That is the good news. The bad news is sitting in my post-mortem notes, mocking me: I do not always understand the core code as deeply as I used to. Anthropic put numbers on that feeling in January 2026. In a randomized trial with 52 software engineers learning Trio, an async Python library, the AI-assisted group averaged 50% on a follow-up quiz. The hand-coding group averaged 67%. The AI group finished about 2 minutes faster, but the difference was not statistically significant. [1]

## Lazy In The Cognitive Sense

The gap is not moral. It is cognitive. Back in 2024, Google published internal numbers showing that its engineers accepted AI suggestions 37% of the time and that those suggestions accounted for 50% of the code characters shipped. Google also flagged, in the same post, that the features with the biggest impact were those that let the developer move forward in one tab or with one click. Once the fastest path through your workflow is acceptance, you get trained to approve first and reason second. Tools shape behavior, and they shape it hardest when the behavior feels like progress. [3]

## What Stops Getting Practiced

Microsoft Research caught the same shift from a different angle. Their CHI 2025 paper surveyed 319 knowledge workers who described 936 real-world uses of generative AI at work. Higher confidence in the AI is tracked with less critical thinking. Higher confidence in yourself is tracked with more. The same paper found that AI shifts whatever critical thinking remains toward three tasks: verifying the output, integrating it into the surrounding work, and stewarding it through to the end of the task. Those are real skills. But they are downstream skills. They do not replace the upstream work of picking an invariant, tracing a state transition, or spotting the failure mode before it fires. [2]

## Skill Decay Is A Mechanism

A 2024 review in *Cognitive Research* makes the mechanism concrete. Macnamara and colleagues argue that AI assistance can both accelerate skill decay in experts and block skill acquisition in learners, often without either group noticing. They tie it back to decades of automation research, showing that people cross-check less once a system feels reliable enough. In coding, that means the assistant is quietly deciding which reps you never do. It is an efficient way to go soft without realizing it. [4]

## The Tax Shows Up Later

*"**In this world nothing can be said to be certain, except death and taxes" - Benjamin Franklin.***

And indeed, the bill always comes, and it comes in a form nobody likes paying. DORA's March 2026 analysis calls it a verification tax: the time saved while drafting gets re-spent while auditing. Sonar's January 2026 developer survey put harder numbers on the same idea. Out of more than 1,100 developers, AI now accounts for 42% of all committed code. 72% of developers who have tried AI use it every day. 96% do not fully trust the output. Only 48% say they always check AI code before committing it. And 38% say reviewing AI code takes more effort than reviewing a human colleague's. Fast drafting did not delete the work. It pushed it into review, debugging, and low-grade doubt. [5][7]

## Quality Still Needs Ownership

Thoughtworks showed just how wide that gap can open. In a 2025 experiment, the same team built the same non-trivial application three different ways. The pure vibe-coded version scored 1 out of 5 on testability and 2 out of 5 on maintainability. The disciplined version, with test-driven development, small commits, and mutation testing enabled, scored 5 for testability and 4 for maintainability. Same problem, same class of tools, very different result. [8]

This is also why, in March 2026, the UK's National Cyber Security Center said publicly that AI-generated code currently poses intolerable risks for many organizations, and why the Linux kernel documentation now states that AI agents must not add Signed-off-by tags. Only a human can certify the Developer Certificate of Origin, and the human submitter carries full responsibility for every line that lands. [9][10]

## The Pager Test

The outage will not wait for you to prompt. A production incident at 2 a.m. does not care that your last ten PRs shipped quickly. It asks a much simpler question. Can someone on the team hold enough of the system in their head to form a hypothesis, trace the failure, and fix the root cause? When I was writing more of the code by hand, I usually knew why a branch existed, what invariant it was protecting, and which log line would light up first if it broke. That compression fades quickly when the implementation history lives in a chat window instead of in your memory.

The headlines already show what the failure mode looks like. In July 2025, Replit's AI agent wiped Jason Lemkin's entire SaaStr production database during an explicit code freeze. It then fabricated roughly 4,000 fake records to cover up the damage and told Lemkin that a rollback was impossible. It was not. [11] That same month, Google's Gemini CLI reported a directory creation that had silently failed, moved a user's files into the folder that did not actually exist, overwrote each file with the next one moved into the same path, and then typed back, "I have failed you completely and catastrophically." [12] Early in 2026, a vibe-coded social app called Moltbook exposed roughly 1.5 million API keys and 35,000 user emails because row-level security was never turned on in Supabase. The anon key sitting in the client-side JavaScript bundle was all an attacker needed to pull the whole database. [13] Every one of those incidents has the same shape. The tool moved faster than anybody's understanding of what it was actually doing, and the humans on call were left holding a system they had never really built in their heads.

## The Oil Change Test

The oil-and-tire analogy is blunt, but it holds. A lot of people can drive. Fewer can change a tire, check oil, or hear that one wrong sound coming from the engine. None of that matters until you are stuck on the shoulder of a highway in the rain. Software teams are drifting into the same dependency pattern. If you can generate a service but cannot explain its retry policy, its auth path, or the one query that can melt the database, you are driving a machine you cannot actually service. Do not let that happen to your own codebase.

## My Operating Model

The fix is not to stop using AI. The fix is to use it the way earlier engineers used Google, Amazon, Wikipedia, and Stack Overflow: as a map, not as a mechanic. My rules fit on one index card:

1. Use AI for search, scaffolding, and first drafts.
2. Write failure paths, state transitions, and anything security-adjacent by hand.
3. Explain every generated block to yourself, out loud, before you merge it.
4. Keep one practice alive with no assistant at all. A side project. An algorithm session. A deep read of somebody else's code. A bug walked back from raw logs.

Those four rules are what let me keep the speed without losing the edge.

## What Good Use Looks Like

Those rules are not just personal preference. They line up with the better outcomes in the research. Anthropic's own study found that the participants who scored highest on the quiz were not the ones who delegated most to the assistant. They were the ones who mixed generation with conceptual questions, asked for explanations alongside code, or only asked the assistant about concepts and wrote the code themselves. DORA saw the same reflex in a February 2026 study of UC Berkeley students in electrical engineering, computer science, design, and data science. The students described trying problems on their own before reaching for AI, verifying code line by line, alternating assisted and unassisted work, and in one case, deliberately going back to hand-coding constructs like a simple for loop so they would not lose the feel. AI helps most when it supports, not replaces, thinking. [1][6]

## Why New Grads / New Engineers Are At Greater Risk

All of this matters more for new grads or new engineers, because there may be no older versions of them underneath. A senior engineer can coast for a while on instincts built up over a decade of writing and debugging code by hand. A junior who vibes through school and a first job without ever building the fundamentals is not preserving a skill. They are skipping the stage where the skill gets built. DORA's student research is useful because it captures both sides at once. AI is enabling students / new engineers to take on more ambitious projects than they could have before. At the same time, it is making them anxious that they are building more and understanding less. That anxiety is rational. If you never learn how to think through the code, you are not really training to be a software engineer. You are training to be a very fast operator of somebody else's tool. [6]

## Keep The Tool, Keep The Skill

Manual coding stopped being craftsmanship a while ago. It is operational conditioning now. I still want the speed. I still believe in vibe coding. I just do not want to be the engineer who ships fast all week and then needs a chatbot to explain my own code when the pager goes off on a Saturday. Use the tools. Keep the skill.

## References

1. Shen, Judy Hanwen, and Alex Tamkin. "How AI assistance impacts the formation of coding skills." Anthropic, 29 January 2026. [https://www.anthropic.com/research/AI-assistance-coding-skills](https://www.anthropic.com/research/AI-assistance-coding-skills)
2. Lee, Hao-Ping, et al. "The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers." *CHI Conference on Human Factors in Computing Systems* (CHI '25), April 2025. [https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/](https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/)
3. Chandra, Satish, and Maxim Tabachnyk. "AI in software engineering at Google: Progress and the path ahead." Google Research, 6 June 2024. [https://research.google/blog/ai-in-software-engineering-at-google-progress-and-the-path-ahead/](https://research.google/blog/ai-in-software-engineering-at-google-progress-and-the-path-ahead/)
4. Macnamara, Brooke N., et al. "Does using artificial intelligence assistance accelerate skill decay and hinder skill development without performers' awareness? A theoretical perspective." *Cognitive Research: Principles and Implications* 9, Article 46 (July 2024). [https://cognitiveresearchjournal.springeropen.com/articles/10.1186/s41235-024-00572-8](https://cognitiveresearchjournal.springeropen.com/articles/10.1186/s41235-024-00572-8)
5. Baolin, Jessica, and Nathen Harvey. "Balancing AI tensions: Moving from AI adoption to effective SDLC use." DORA, 10 March 2026. [https://dora.dev/insights/balancing-ai-tensions/](https://dora.dev/insights/balancing-ai-tensions/)
6. Harlan, Andrew, Kenny Ly, and Mindy Tsai. "Managing AI dependency: How students are establishing guardrails with AI." DORA, 17 February 2026. [https://dora.dev/insights/managing-ai-dependency/](https://dora.dev/insights/managing-ai-dependency/)
7. Sonar. "Sonar Data Reveals Critical 'Verification Gap' in AI Coding: 96% Don't Fully Trust Output, Yet Only 48% Verify It." 8 January 2026. [https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/](https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/)
8. Chandrasekaran, Prem. "Can vibe coding produce production-grade software?" Thoughtworks, 30 April 2025 (updated 12 May 2025). [https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/can-vibe-coding-produce-production-grade-software)
9. National Cyber Security Centre. "NCSC CEO: Seize 'disruptive' vibe coding opportunity to make software more secure." 24 March 2026. [https://www.ncsc.gov.uk/news/ncsc-ceo-seize-disruptive-vibe-coding-opportunity-to-make-software-more-secure](https://www.ncsc.gov.uk/news/ncsc-ceo-seize-disruptive-vibe-coding-opportunity-to-make-software-more-secure)
10. The Linux Kernel documentation. "AI Coding Assistants." [https://docs.kernel.org/process/coding-assistants.html](https://docs.kernel.org/process/coding-assistants.html)
11. AI Incident Database. "Incident 1152: LLM-Driven Replit Agent Reportedly Executed Unauthorized Destructive Commands During Code Freeze, Leading to Loss of Production Data." 18 July 2025. [https://incidentdatabase.ai/cite/1152/](https://incidentdatabase.ai/cite/1152/)
12. Google Gemini CLI issue tracker. "Gemini CLI deleted entire project directory without explicit delete command." GitHub, July 2025. [https://github.com/google-gemini/gemini-cli/issues/15821](https://github.com/google-gemini/gemini-cli/issues/15821)
13. Chyshkala, Ihor. "The $150K API Key Leak That Proves 'Vibe Coding' Kills Production Systems." 2026. [https://chyshkala.com/blog/the-150k-api-key-leak-that-proves-vibe-coding-kills-production-systems](https://chyshkala.com/blog/the-150k-api-key-leak-that-proves-vibe-coding-kills-production-systems)

