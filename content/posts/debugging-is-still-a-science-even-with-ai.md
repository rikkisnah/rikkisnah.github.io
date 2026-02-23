---
title: "Debugging Is Still a Science Even With AI"
date: 2026-02-22T20:25:02-08:00
draft: false
---

# Debugging Is Science, Even When It Feels Like Art. AI Didn't Change That.

![Debugging science visual](/posts/debugging-is-still-a-science-even-with-ai/debugging-science.png)

*Disclaimer: This post was generated with Claude and researched with Perplexity, but the final technical judgment, edits, and conclusions are mine.*

I don't think AI made debugging automatic. I see engineers paste a stack trace into a chat window, copy the patch back, watch the red line disappear, and declare it fixed. I've done it too. Then the bug returns two weeks later under a different name, with more pages and more pain.

AI made bad debugging faster. It also made good debugging faster. The difference is discipline, not speed or blanket AI usage. Root-cause accuracy is still the end game.

This perspective builds on a post by [Alexandre Zajac](https://www.linkedin.com/posts/alexandre-zajac_i-studied-how-6-legendary-engineers-debug-activity-7431374226223349760-_HDB) about how six great engineers debug: Carmack isolates, Torvalds reads code flow, Hamilton thinks defensively, Hopper reproduces, Abramov explains clearly, Gosling instruments deeply. Those are not history lessons. They are load-bearing constraints for anyone working in complex systems.

I work on large-scale GPU infrastructure: thousands of GPUs, RDMA networks, firmware layers, and distributed orchestrators. When things fail, blast radius is measured in racks, not requests. I use AI tools every day (as approved in OCI), but I've learned this: an LLM is a lab instrument, not the scientist.

The six legends and habits referenced here are:

- **John Carmack:** methodical isolation
- **Linus Torvalds:** read the code path, not only logs
- **Margaret Hamilton:** defensive thinking
- **Grace Hopper:** reproduce reality at the source
- **Dan Abramov:** explain it to debug it
- **James Gosling:** trace and instrument deeply

***

## Isolate Before You Speculate

Carmack trims a system to the smallest failing case. He removes everything that can go wrong until only the bug remains. He trusts process over intuition. His writing on static code analysis captures this precisely: *"The most important thing I have done as a programmer in recent years is to aggressively pursue static code analysis"* - a discipline rooted in the same instinct to remove uncertainty systematically. His philosophy of eliminating unexpected state and side effects through inlined code is the intellectual foundation of isolation-first debugging. [sevangelatos](http://www.sevangelatos.com/john-carmack-on-static-code-analysis/)

That matters even more with AI. LLMs can generate many plausible explanations quickly. If you feed noisy context, you get noisy hypotheses. Modern models still miss a meaningful share of complex tasks, including hallucinating causes for multi-step failures. A minimal reproducible example is still the highest-leverage debugging tool. [projectpro](https://www.projectpro.io/article/llm-limitations/1045)

I cut scope hard: which region, which rack, which test, which config delta. I strip until one failure remains. Then I prompt:

> *"This is the smallest failing example in terms of inputs and outputs. Do not suggest fixes. Report three possible root causes and one observation that would disprove each."*

That keeps the investigation scientific. The model stops being a slot machine and starts being a thought partner.

***

## Read Code Flow, Not Chatbot Fluency

Torvalds distrusts symptoms. Logs are downstream evidence; most bugs live in upstream assumptions. His position is unambiguous: *"Without a debugger, you basically have to go the next step: understand what the program does. Not just that particular line. At the meaning of things."* That philosophy - understanding over observing - is what separates root-cause thinking from surface-level pattern matching. [yarchive](https://yarchive.net/comp/linux/debuggers.html)

The same is true for AI explanations. They are downstream of whatever context you gave the model. Partial context produces confident nonsense. I trace entry point to failure point before asking AI anything. I include expected input shape, assumed state, and side effects, then ask the model to walk the same path and flag brittle assumptions. [projectpro](https://www.projectpro.io/article/llm-limitations/1045)

Then I validate against runtime evidence: breakpoints, traces, stack frames. I trust execution semantics over polished summaries.

***

## Test What You Don't Want to Happen

Hamilton built systems where failure was a first-class design constraint, not an afterthought. Her team on the Apollo Guidance Computer pioneered what she called "defensive programming" - software that could detect, report, and recover from its own errors in real time. The Apollo 11 mission itself validated this: her fault-tolerant task-prioritization design handled a hardware overload at 3,000 feet and still landed the crew. [exaud](https://exaud.com/blog/margaret-hamilton-s-legacy-in-software-engineering)

I watch teams write happy-path code, ask AI for tests later, then act surprised in production. That's backwards. Defensive thinking belongs at design time.

AI helps with breadth. After I define failure handling, I ask it for edge cases I missed: race conditions, partial dependency failures, timeout cascades, malformed payloads, ordering violations, stale reads after writes. That gives me a faster failure-oriented matrix.

But breadth without structure is a spreadsheet, not a safety net. I convert incidents into regression tests before closing tickets. If I skip that, I'm writing future pain into the repo.

***

## Reproduce Before You Theorize

Hopper's principle is uncompromising: if you can't reproduce the bug, you are not done debugging. The origin of the word itself traces to her team's 1947 logbook entry at Harvard - a moth taped to paper after being extracted from a relay in the Mark II. What mattered wasn't the moth. It was that her team documented it, reproduced the exact conditions, and verified the fix against physical evidence. [economictimes](https://economictimes.com/news/international/us/grace-hopper-found-the-first-computer-bug-a-real-one/articleshow/128299349.cms)

LLMs accelerate the temptation to skip reproduction. The longer you iterate without stable repro, the worse the advice gets.

I collect environment facts first: version hashes, feature flags, data shape, region, concurrency level, dependency versions. Then I ask AI for a deterministic reproduction plan and treat it as a checklist, not truth. I run it and verify each step before touching fixes.

***

## Describe It or You Don't Own It

Abramov's discipline is simple: "I expected X, I got Y." The gap is where the bug lives. His blog, *overreacted.io*, consistently demonstrates this habit - surfacing hidden assumptions, defending mental models, and resisting the pull of clean-looking but wrong abstractions. [overreacted](https://overreacted.io)

I use AI as a Socratic partner. I don't ask for answers first; I ask for questions:

> *"I expected the third retry to pass validation, but it didn't. Ask me five clarifying questions that could expose where my mental model is wrong. Do not propose fixes yet."*

That forces my assumptions into the open. Often, the bug hides in the sentence I can't defend cleanly.

***

## Build Systems That Describe Themselves

For Gosling, structured logging beats hero debugging: correlation IDs across boundaries, traces that explain *why*, not just *what*. The Java ecosystem he helped shape pioneered this - JVM observability tooling, event filtering, and trace-level instrumentation are direct descendants of that design philosophy. His 2025 retrospective on Java's 30-year arc reinforces that system-level visibility was always part of the original intent. [digitalcommons.unl](https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1024&context=computerscidiss)

Without observability, debugging is archaeology. With observability, it's diagnosis.

After each high-profile incident, I ask:

> *"Given this architecture and incident timeline, what minimum logging and tracing schema would have detected root cause twice as fast?"*

Then I implement the answer. That's where AI compounds value over time.

***

## The Loop

Seven steps:

1. Reproduce deterministically.
2. Isolate the simplest failing case.
3. Trace the actual code path end to end.
4. Explain expected vs. actual behavior plainly.
5. Interrogate assumptions with targeted prompts.
6. Patch lightly, then test with regressions and edge cases.
7. Instrument so the next failure is cheaper to diagnose.

AI accelerates steps 5 and 6 and can help design step 7. Steps 1 to 4 are still on me. That's where the science lives. The 2025 Stack Overflow Developer Survey confirms this instinct: developers show the highest resistance to AI for exactly the high-responsibility, systemic decisions that steps 1-4 require. [survey.stackoverflow](https://survey.stackoverflow.co/2025/ai)

***

## Where It Breaks

I've done this wrong plenty of times. I asked for fixes before reproduction. I dumped too much context and buried the one line that mattered. I accepted the first neat explanation because noise felt exhausting. I shipped code that compiled but violated contract behavior.

The worst failure mode is first-answer bias. One tidy explanation appears, and I want it to be true. I now fight that by deliberate disconfirmation. I ask AI what evidence would falsify the top hypothesis, then I run that check first. If it survives, I go deeper. If it dies, I move on. Research on LLM limitations consistently flags this as a real risk: models produce confident, coherent responses even when the underlying reasoning is flawed. [projectpro](https://www.projectpro.io/article/llm-limitations/1045)

The fundamentals haven't changed: isolate, trace, test failure paths, reproduce reality, explain clearly, instrument deeply. AI amplifies these habits. It doesn't create them.

I keep one sentence close:

> *Use AI to speed up the scientific method of debugging, not to replace it.*

I'm always one rushed moment away from breaking my own rules. That's exactly why the rules matter.

***

## References

1. [Alexandre Zajac LinkedIn post](https://www.linkedin.com/posts/alexandre-zajac_i-studied-how-6-legendary-engineers-debug-activity-7431374226223349760-_HDB)
2. [John Carmack on static code analysis](http://www.sevangelatos.com/john-carmack-on-static-code-analysis/)
3. [LLM limitations overview (ProjectPro)](https://www.projectpro.io/article/llm-limitations/1045)
4. [Linus Torvalds on understanding program behavior](https://yarchive.net/comp/linux/debuggers.html)
5. [Margaret Hamilton legacy and defensive programming](https://exaud.com/blog/margaret-hamilton-s-legacy-in-software-engineering)
6. [Grace Hopper and the first computer bug story](https://economictimes.com/news/international/us/grace-hopper-found-the-first-computer-bug-a-real-one/articleshow/128299349.cms)
7. [Dan Abramov's blog (Overreacted)](https://overreacted.io)
8. [Java retrospective and observability context](https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1024&context=computerscidiss)
9. [Stack Overflow Developer Survey 2025 - AI](https://survey.stackoverflow.co/2025/ai)