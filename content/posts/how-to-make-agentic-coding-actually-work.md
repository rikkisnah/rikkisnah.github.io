---
title: "How to Make Agentic Coding Actually Work"
date: 2026-03-14T15:31:48-07:00
draft: true
---

![How to Make Agentic Coding Actually Work](/posts/how-to-make-agentic-coding-actually-work/agentic-coding.png)

*Disclaimer: This post reflects my personal views and does not represent the views of my employer.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

# Your Repository Is the Prompt: How to Make Agentic Coding Actually Work

Most developers using AI coding tools are still copying code into chat windows. I don't think that is agentic coding. Agentic coding means deploying AI agents as contributors inside your repository. They read your codebase, plan changes, write code, run tests, and prepare pull requests. The gap between an agent that behaves like a competent engineer and one that hallucinates your conventions usually comes down to one thing: how well you prepared the repository.

## What Is Agentic Coding?

Agentic coding is a step beyond autocomplete. GitHub Copilot suggests the next line. An agentic tool like OpenAI's `Codex CLI` works more like a semi-autonomous contributor. You describe a task like "add input validation to the user registration endpoint" and the agent reads relevant files, plans an approach, writes the implementation, runs your tests, and presents a diff for review [1].

I think the better way to frame this is bounded delegation. The engineer defines the task, context, and constraints. The agent executes against the codebase. The engineer reviews the result. It feels closer to supervising a fast junior engineer who can search, edit, and execute, but still needs direction.

OpenAI's `Codex CLI`, released as an open-source terminal agent in 2025, reads a file called `AGENTS.md` at the root of your repository to understand project conventions, build commands, and constraints [2]. Anthropic's `Claude Code` follows the same pattern with `CLAUDE.md` [3]. The open `AGENTS.md` standard has become the de facto way to give coding agents context [4].

That is the part people miss. The model is not the system. The context and validation pipeline wrapped around it, that is the system.

## Context Engineering Over Prompt Engineering

Prompt engineering helps with a single instruction. Context engineering is broader. It is how you structure the repository so agents load the right information at the right time. The Redis engineering team found that well-structured context reduced agent hallucinations and improved code quality [5]. Teams that adopt structured guidance files consistently report that agents stay closer to existing conventions. Bare repositories tend to get the opposite. Agents invent patterns. They violate standards. They guess.

For me, context engineering comes down to three things:

- Hierarchical context. A root `AGENTS.md` defines global invariants like language version, coding conventions, and hard constraints. Module-level `AGENTS.md` files add local rules. ADRs explain why decisions were made. That hierarchy matters because it prevents context blowout, where an agent wastes its token budget on irrelevant information.
- Explicit policy boundaries. Some actions should require human approval. API changes. Schema migrations. CI/CD modifications. Other actions can be autonomous. Unit tests. Documentation. Lint fixes. Without clear boundaries, agents make changes that sound reasonable but are still destructive.
- Verifiable workflows. Every agent task should follow the same loop: load context, plan, execute, validate, review. The agent should not merge code itself. Build, test, and lint commands belong in `AGENTS.md` so the agent can validate its own work before it hands anything back.

## Keep It Simple -- Seriously

This is where I think a lot of teams go wrong. They read about agentic coding and immediately design an elaborate framework: context packs, prompt templates with semantic versioning, agent personas with declarative read/write scopes, a seven-level directory hierarchy. I know because I built exactly that kind of framework once, then watched an architect look at it and say: "This is over-engineered. Too many named constructs. Humans have to keep this up to date."

He was right.

If you introduce a separate concept for every category of agent instruction, context packs versus skills versus snippets versus personas versus policies, you create cognitive load that people will not maintain. The teams I have seen succeed usually keep their agent infrastructure to two things:

1. A root `AGENTS.md` under 200 lines
2. A `.agents/skills/` directory with task-specific instruction files

That is enough. Context packs are basically skills with a reading list. Modern agents parse skill frontmatter at startup and auto-activate the right skill when the task matches its description [1]. Policies belong in a `## Constraints` section of your `AGENTS.md`. Prompt templates are often skills by another name.

```text
your-repo/
  AGENTS.md              # Global rules, build commands, constraints
  .agents/
    skills/              # Task instructions, loaded on demand
      unit-testing.md
      api-change.md
      refactoring.md
  docs/
    specs/               # Flat: how things are implemented
    adrs/                # Flat: why decisions were made
```

## Setting Up in One Day

**Step 1: Create `AGENTS.md`.** Keep it short. One paragraph describing the system. Build and test commands. Three to five hard constraints.

```markdown
# AGENTS.md
## Overview
Order processing microservice. Java 17 / Spring Boot / PostgreSQL.

## Build & Test
Build: mvn clean install -DskipTests
Test: mvn test
Lint: mvn checkstyle:check

## Conventions
- Immutable DTOs
- SLF4J logging only
- No wildcard imports

## Constraints
- Do NOT modify CI/CD pipelines
- Do NOT change public APIs without updating the OpenAPI spec
- Do NOT commit secrets or credentials
```

**Step 2: Write one skill file** with frontmatter so the agent auto-activates it:

```markdown
---
name: api-change
description: "API additions or modifications. Trigger when touching
  api.yaml or when the user mentions API changes."
---
1. Read the OpenAPI spec
2. Plan changes
3. Implement
4. Run compatibility checks
5. Update documentation
```

**Step 3: Write a short architecture overview.** One page explaining the major components and how they connect.

**Step 4: Run a real task.** Give the agent a straightforward issue. Watch where it stumbles. Then refine the repo from what you learned.

## The Legitimate Concerns

**Will it make developers lazy?** I don't think that is the right frame. Calculators made routine arithmetic cheaper, but they did not remove the need for mathematical reasoning. Agentic coding will probably do something similar. Repetitive scaffolding becomes less valuable. Task framing, system design, debugging, and the ability to detect when a polished-looking change rests on a flawed assumption become more valuable. In a controlled study, developers using GitHub Copilot completed tasks 55.8% faster [6], and a separate randomized trial found higher code quality scores [7]. The upside looks real. It still depends on disciplined review.

**Will it make debugging harder?** It can, if people accept code they do not understand. If an agent writes code a developer cannot explain, that code is a liability in production. The SWE-bench benchmark, built from 2,294 real GitHub issues, tests whether models can resolve repository-level problems, not only produce isolated samples [8]. Software engineering is contextual. Blind delegation without review exposes that gap fast. Agents should not merge without human review.

**Will it get complicated?** Only if you let it. Start with `AGENTS.md` and one skill. Add complexity only when it is earned, when a real task fails because the agent lacked context. Teams that over-engineer on day one usually abandon it by month two.

## The Capability Curve Makes This Urgent

The METR research group found that frontier models had a 50% task-completion time horizon of roughly 50 minutes, with that horizon doubling approximately every seven months since 2019 [9]. If that trend continues, agents will handle longer and more connected tasks. Weak process will not stay hidden. It will get amplified. If a team cannot specify how an agent should work in a repository today, it will not be in a better position when agents can take on larger refactors tomorrow.

## Start Today

OpenAI `Codex CLI` is open source [2]. The `AGENTS.md` standard is free and tool-agnostic [4]. The teams that do well here probably will not be the teams with the cleverest prompts. They will be the teams with a clean `AGENTS.md`, a few well-written skills, and the discipline to let complexity emerge only when it is earned.

One file. Three constraints. One real task. Start there.

## References

[1] OpenAI, "Codex CLI -- Agent Skills," OpenAI Developer Platform, 2025. https://developers.openai.com/codex/skills

[2] OpenAI, "openai/codex -- Lightweight coding agent that runs in your terminal," GitHub, 2025. https://github.com/openai/codex

[3] Anthropic, "Claude Code -- Agentic coding tool," Anthropic, 2025. https://docs.anthropic.com/en/docs/claude-code

[4] agentsmd, "AGENTS.md -- Open Format for Guiding Coding Agents," 2025. https://agents.md

[5] Redis Engineering, "Context Engineering Best Practices," Redis Blog, 2025. https://redis.io/blog/context-engineering-best-practices

[6] Sida Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot," arXiv:2302.06590, 2023. https://arxiv.org/abs/2302.06590

[7] Jared Bauer, "Does GitHub Copilot improve code quality? Here's what the data says," GitHub Blog, November 2024. https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/

[8] Carlos E. Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?," arXiv:2310.06770, 2024. https://arxiv.org/abs/2310.06770

[9] Thomas Kwa et al., "Measuring AI Ability to Complete Long Software Tasks," arXiv:2503.14499, 2025. https://arxiv.org/abs/2503.14499
