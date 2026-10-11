---
title: "Physical AI - the beginning of a new AI era"
date: 2026-10-11T12:00:00-07:00
draft: false
tags: ["Physical AI", "World Models", "Robotics", "AI Infrastructure", "GPU", "Engineering"]
summary: "Physical AI is the next stage of AI's future, but we don't yet have the technology or data to reach it. A view from an infrastructure engineer after the Bezos Prometheus interview."
images:
  - /posts/physical-ai-needs-practice/lead.png
---

![Two ways to learn about the world: a language model reads what people wrote; a child predicts, acts, compares, and updates](/posts/physical-ai-needs-practice/lead.png)

*2,010 words · 11 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: I used Claude, ChatGPT, and Perplexity for research. The words and the ideation are mine, and I cross-checked the references. Originality.ai rates this post at 5 to 10 percent AI generated.*

*Image: The diagrams in this post were generated with Grok and re-rendered with matplotlib for readability.*

Jeff Bezos (Fun fact: I met him briefly at Kindle, when my manager gave a presentation on the Kindle Reader in the Day 1 North building in Seattle) gave his first [interview about Prometheus](https://www.geekwire.com/2026/jeff-bezos-describes-his-38b-startup-prometheus-for-the-first-time-nothing-to-do-with-robotics/) to CNBC in June-2026. (Prometheus, I suspect the name is based on the Greek Titan who stole fire from the Gods and gave it to humanity). A company name means a lot (do read my article on [Anthropic](https://www.rik-kisnah.ai/posts/anthropic-how-the-pieces-fit/)) - your name defines your values and vision. He co-leads a company with Vik Bajaj. As usual, Jeff, with legendary vision and directness, called it a "very modern version" of CAD (computer-aided design), an AI generalist engineer that shortens ideation to manufacturing. The company aims to build models for physical tasks across different vertical domains, i.e., engineering, manufacturing, and drug design.

For nearly the past decade, I have worked in Cloud Infra, with the last four years focused on GPU cluster quality (burn-in, fault diagnostics at scale for GPU fleets). I listened to the interview on CNBC with the curious mind of an infrastructure engineer, and it clicked: the future is to build a model that learns how humans mimic and train on that, but the data isn't ready yet.

By the end of this article, I hope you understand what I meant: Physical AI is the next stage of AI's future, but we don't yet have the technology or data to reach it.

## Text has no gravity

An LLM (Large Language Model) learns from and is trained on a large corpus of human-written knowledge (text, books, code, etc.). It reads what people wrote about the world (and there is a level of bias because the last 100 years of written history is verged towards western viewpoints - different topic for a different blog). An LLM is a probabilistic model (augmented by amazing algorithms, Google's [Attention is All You Need](https://arxiv.org/abs/1706.03762), and compute innovation from NVIDIA and AMD). Still, it has its glass ceiling: it has never experienced it. Reading about falling in love is not the same as falling in love…

Text (and LLMs) is a lossy summary of the world, written by people at times with certain biases in how they view it. A model trained on this corpus inherits that gravity without any of the human intuition. You can get really far in the descriptions, but you will never get all the way.

## How a child learns - the foundations of Physical AI

When my kids were toddlers nearly 2 decades ago, the engineer in me (Engineer dad can relate) took notes to see how my daughter (2 years old) and my son (3 months) were learning. They don't just pick up books; they experiment, watch, and try again. I recall them pushing the cup of water and watching with amazement as it crashed, then doing it again until Mama stopped them. What emerged from me that time was a loop: predict, act, compare, and update. At this age, kids are watching; only a small fraction of it is doing.

Yann LeCun in his 2022 paper, "[A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf)", explain this analogy in a really clear way - do read it if you can - this is the future. At the center of the thesis is a world model where a module predicts how the world changes given the current state and a proposed action; the system plans instead of reacting (back to the analogy of the child: she watches, experiments, and then reacts).

Meta's [V-JEPA-2](https://arxiv.org/abs/2506.09985), released in June 2025, further affirms that loop. The model was pre-trained without any action labels on a million hours of videos and images. A second stage then trained the predictor on 62 hours of robot data from the open [DROID](https://droid-dataset.github.io/) set (Distributed Robot Interaction Dataset—a massive, open-source robotic manipulation dataset widely used to train generalist robot policies and foundational world models). In the lab, robots using image goals rather than language instructions could perform human actions like reach, grasp, and pick objects never seen before in new environments! The success rate was about 65-80%!

The takeaway here is the foundation of Physical AI: learn a usable model of the world from an observation. At a scale that no child can match, and adapt it with a small amount of robot data. We are not a general physical intelligence, but this is the right direction. The model still plans over short horizons, and video models, as of today, remain weak on some of the physics only people can pass easily.

<div class="diagram-wide">

![Public data for Physical AI by order of magnitude: internet video, open robot datasets, proprietary robot trajectories, high-precision physical measurements](/posts/physical-ai-needs-practice/data-pyramid.png)

*Public data for physical AI, by order of magnitude. Cheap and plentiful at the bottom, expensive and scarce at the top.*

</div>

The same shape shows up across bodies. [Open X-Embodiment](https://arxiv.org/abs/2310.08864) pooled about a million robot episodes from 22 robot types and found that one model trained on all of them beat models trained on any single one. What transfers is not "how this arm moves." It is closer to "how objects behave."

## Learning starts when prediction meets measurement.

Biased opinion, so take it with a pinch of salt, as trillions of dollars from smarter people are working on LLMs across Frontier Labs. I think the industry is about to focus on only half the system.

Invention has four pipelines: propose, predict, measure, and correct. The first two (especially now with LLMs) make impressive demos. The harder part is testing against reality and fixing what fails. This is what turns AI into an engineer. Without the last two, we have a cosmetic/aesthetic product (beauty without brains), a better-looking tool…

<div class="diagram-wide">

![Invention has four pipelines: propose, predict, measure, correct. The harder half turns demos into engineering](/posts/physical-ai-needs-practice/four-pipelines.png)

*Measure means the test cell, the strain gauge, the log a senior engineer would trust on a bad day. Correct means the disagreement is written back into a system the company owns.*

</div>

Let me use a project I was following at the office: a cooling plate for an AI server. The AI-assisted design looked good in simulation. However, when an engineer built and tested it, it took too much pressure to push the coolant through. To learn from that failure, you need more than the result; you need a range of other parameters, materials, sensors, and environments, because without the context of the physical model, the model was off base. In the physical world, you need a physical AI who can visualize and get the right context.

I am not against simulation. Simulations are essential in any engineering project. They let you test changes cheaply and safely (in fact, any engineering project that doesn't treat a simulator as a first-class citizen is doomed to be expensive to develop; I know this for a fact). However, if the assumptions are wrong, the old adage holds: Garbage In, Garbage Out. Simulated data needs to be grounded in reality and real measurements.

[Anima Anandkumar and Benedikt Jenik](https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/08/25/the-ai-founders-who-walked-away-from-bezos-backed-prometheus-to-model-the-universe-reuters-exclusive/), who declined involvement in the Bezos-backed effort, are building models that predict physical behavior directly rather than through language. I see this as another way to close the same gap: starting with physics rather than physical tests. Either way, predictions still have to match what we measure.

## Three computers - the circle of Physical AI Lifecycle - who owns the arrows

NVIDIA described physical AI as a [three-compute problem](https://blogs.nvidia.com/blog/three-computers-robotics/). After working with a physical GPU fleet, the framing sounds right to me.

<div class="diagram-wide">

![Three computers, the circle of the Physical AI lifecycle: training cluster, simulation farm, onboard compute, with real-world logs and failures flowing back](/posts/physical-ai-needs-practice/three-computers.png)

*Every arrow is a data pipeline someone has to own, monitor, and debug at 3 a.m.*

</div>

I am intimately familiar with the training cluster (that is my daily bread and butter), running thousands of GPUs, fighting with NVLink and RDMA fabric (where a stubby finger or some dust will make the optics cable flap) and stall the whole collective. The simulation farm is very unknown to most. Omniverse and Isaac workloads (both AI models for physical worlds from NVIDIA), are rendering-bound (not the usual matmul), and nobody has written a burn-in guide for them (an old blog of [burn-in](https://www.rik-kisnah.ai/posts/gpu-burn-in-at-scale-reference-guide/) I wrote).

Then there is the computer inside the robot. A [Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/) (NVIDIA's high-performance computer designed to power next-generation humanoid robots and physical AI applications) packs roughly 2,070 FP4 TFLOPS and 128 GB of memory into a 130-watt power budget. It must respond dozens of times per second without waiting for the cloud. A delay can mean dropping a part instead of placing it. The Burn-in / infra engineers make me think this is a problem of how to test/validate at scale … a great area for innovation - none of the paradigms I wrote for [regular GPU clusters](https://www.rik-kisnah.ai/posts/gpu-burn-in-at-scale-reference-guide/) apply.

Reliability compounds in ways many folks underestimate. If a workflow has 100 steps, each succeeding one has a 99% probability, and any failure ends the run. The chance is about 37%. Some maths if you are curious about 37%

For 100 independent steps, each with a 99% (0.99) chance of success, the calculation is:

```
Total Success Probability = 0.99 × 0.99 × 0.99 × … × 0.99 = 0.99^100
0.99^100 ≈ 0.36603
```

This means there is only a 36.6% chance that the entire workflow finishes without a single failure, leaving a 63.4% chance of failure.

The number is scary; it explains and reinforces why recovery and validation in physical AI are extremely important. Questions infra engineers working on physical AI need to address: can the system detect a slipped part, and can it stop in a known state and resume without irreversible action? In software, a rollback is harmless; reversing a drilling operation is not.

<div class="diagram-wide">

![Completion probability over sequential steps for per-step success of 99, 99.5, 99.9, and 99.99 percent, no recovery assumed](/posts/physical-ai-needs-practice/reliability.png)

*Completion probability equals per-step reliability raised to the number of steps. No recovery assumed.*

</div>

## What I would build first - if I were Jeff or Elon

Everyone wants to be a luminary technology leader like Jeff Bezos or Elon Musk, with the same financing powers. Let me imagine I was Jeff or Elon…. (most probably they already thought about those - I am just re-transcribing in my own non-specialist words what I think is right)

I would start with four priorities for my Physical AI models.

<div class="diagram-wide">

![Four priorities for Physical AI models: Prima, Secondo, Terza, Quarta](/posts/physical-ai-needs-practice/four-priorities.png)

</div>

Priority Prima - capture the gap between prediction and reality. Record and transcribe what the system expects and what actually happens (and what design or action creates the best result). Use synthetic data to build those measures.

Priority Secondo - Give each tool a clear job, and use world models to explore scenarios and situations that are too dangerous to test. Use physics engines, test rigs, and specialized solvers to check physical behavior. Each module needs to specialize in its job. Think of Henry Ford's factory process, where each worker has a specialized task; here, the tasks are tools that are fundamentally good at physics in a specific physical domain.

Priority Terza - Measure and capture mistakes /bad behavior as early as possible. I would recommend building what Dario and his team did at Anthropic, constitution or RSPs, for physical AI. Use reinforcement learning that's fully grounded in the physical world. Don't be amazed by demos; watch and observe in real physical actions.

Priority Quarta - make the computing trustworthy. Results must be reproducible. Data must be available. If we are using videos of human interaction, earn the public's trust early (don't make the same mistake as LLM Frontier models, which are in lawsuits for using books that infringe on copyrights). Physical AI will be deemed more dangerous than LLMs, so start building trust early; otherwise, you will face the same scrutiny as when the whole world worried AI would destroy humanity, which brings me to my Priority Terza: Constitution and Rules in the Physical AI model.

Daily at OCI (my current employer), we burn in GPU nodes for days before they take a customer job. Nobody has yet said what the humanoid equivalent of nccl-tests is, and someone will have to.

## The honest gap - Hiatus honetus

It seems great on paper. I want to be careful - getting to physical AI requires tens of billions of hours of videos in multiple domains. However great YouTube is (and Google, a private entity, owns the data), or its equivalent, accessing it for training is a huge computational challenge and costly. If you look at OpenAI, it started in 2015 and OpenAI introduced GPT-1 in 2018.

But to be frank, LLMs felt sudden because the corpus was already there, and venture capital funding saw it in Silicon Valley. Physical corpus, however, is not there yet; it hasn't gotten funding at the scale LLMs (if you look at the West) everyone is putting money into, so that's the test in physical AI. If you look around, Jeff and Vik are building with Prometheus, Elon with Optimus, and NVIDIA with Thor/Omniverse; that work has started, but on a smaller scale.

Whoever wins that race will bring us to a world where machines and humans interact (with the hope and prayer that we have laws governing physical AI and don't hamper progress).

The next generation of models will learn the world directly, just as your child does, by predicting and being wrong. This is the next stage, and I am very interested in contributing to it in the future.
