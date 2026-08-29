---
title: "AI Makes Zeroes Feel Like Heroes and Heroes Become Superheroes"
date: 2026-08-29T10:00:00-07:00
draft: false
tags: ["AI", "software engineering", "technical leadership", "developer productivity"]
summary: "AI can make weak work look convincing. Used with judgment, it gives strong engineers and leaders more room to make the hard calls."
images:
  - /posts/ai-does-not-make-everyone-better/lead.jpg
---

![AI makes the judgment gap obvious](/posts/ai-does-not-make-everyone-better/lead.jpg)

*Image generated with Grok.*

*About 900 words · 4 min read*

*Disclaimer: These are my personal views, not those of my employer or community. I wrote and edited this article; ChatGPT, Claude, and Grammarly were used only minimally for background information. Originality.ai scored the final text 100% human-written.*

AI does not magically make everyone better, especially engineers. It makes the gap between real judgment and bullshit analysis, sorry for my French; French, ironically, is my first language, painfully obvious.

Give a junior or weak engineer an AI assistant and, for a hot minute, you feel you are talking to Alan Turing or Grace Hopper. The pull requests are huge, and the state diagrams resemble a painting by Leonardo da Vinci. It is like a regular Joe trying to drive a Lamborghini in an F1 race.

Then someone asks a small question: “What does this number mean or measure?” “What happens when the service goes through this code path?” The Lamborghini suddenly has no engine.

This is a redefinition of AI slop. It is beyond laziness; it is a public hazard. It is the death of critical thinking in product engineering, and that can have dire consequences when you work on critical systems: AI infrastructure, health care, or defence.

## The zero-to-hero illusion

AI is very good at producing external expertise based on probabilistic matching to your current context. Think of it as a consultant you hired to help find a problem in your code. It does not understand your business or code as much as someone in the trenches. It can create the illusion of a polished piece of work and real understanding. AI models are notoriously sycophantic.

The blueprint for this failure, which I have seen in my teams, is to give the model a vague prompt, read the response superficially, produce a design doc with AI fluff, and push code that is not comprehensive or does not match the problem statement.

This is where the domino effect begins. The next engineer or leader has to reverse-engineer the information, and the lazy ones pass it to the model to summarize. That magnifies the incomprehension and leads to more bugs.

AI gives a megaphone to people who are good at looking impressive. The output might not always be wrong, but it can be more dangerous: it gives you a mirage that can lead to a bad product, code, or business decision. It makes zeroes, duds, feel like heroes.

## The hero-to-superhero effect

A strong leader or engineer equipped with an AI tool is a different story altogether.

They do not ask AI to replace their judgment, acquired through years of rigorous engineering. They use it to question their judgment, find missing cases, explain unfamiliar code, produce tests, and challenge design decisions. They inspect the answer, simplify it, and decide. The really good ones turn this into repeatable workflows: schedulers and skills.

This is my definition of the hero-to-superhero effect: “My Codex or Claude is my assistant. It saves me from the grunt work so I can focus on critical decisions that only I can make.”

I have seen great leaders, already good in their domain before AI, use it to augment themselves and insist that engineers using AI have human guardrails and human audit. I strongly believe that this top-down direction will make successful companies and teams. We grew so fast from using AI as a chat assistant to treating token usage as an economic barometer that we forgot the technology is just a tool. It has not replaced human intellect yet.

## Zeroes, heroes, superheroes

So how do we solve it? I do not have a holy-grail solution, but one pattern that has worked in the last few months is auditing the work and its ownership.

- Ask whether you can explain the work in plain language with the AI window closed. If you cannot explain what the code does, what the data means, or what could fail, you do not own the work. Do not forward or approve it. Revisit it and review it.
- AI is great for writing the zero-draft. A human still has to stand behind the final product. Simplify it and explain it plainly.
- Anyone who forwards AI-generated advice without understanding it is not delegating. They are creating a very articulate game of telephone.

## My five precepts

- **Senior leaders and tech leads:** Ask engineers to explain the code path in their own words before review.
- **Engineers:** Keep agent work small and reviewable. One huge AI-generated pull request is a hostage situation with syntax highlighting. Use an IDE with an agent; it forces you to see the code instead of treating AI output as biblical direction.
- **Tech leads and engineers:** Simplify, understand what the AI does, and rinse and repeat.
- **Everyone:** Do not send raw AI text to the next person. Add decisions, data, and conclusions in your own language, with AI as a supporting document.
- **Everyone:** Use AI as a check, not the only checker.

AI will make mediocre work faster: zeroes to heroes. It will also give strong engineers and leaders more room to do the work that matters: heroes to superheroes.

Be a superhero!
