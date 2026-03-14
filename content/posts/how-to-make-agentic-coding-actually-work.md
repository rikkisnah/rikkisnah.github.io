---
title: "How to Make Agentic Coding Actually Work"
date: 2026-03-14T15:31:48-07:00
draft: false
---

![How to Make Agentic Coding Actually Work](/posts/how-to-make-agentic-coding-actually-work/agentic-coding.png)

*Disclaimer: This post reflects my personal views and does not represent the views of my employer.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

# Your Repository Is the Prompt: How to Make Agentic Coding Actually Work

Most developers using AI coding tools are still copying code into chat windows. I don't think that is agentic coding. Some have embraced *vibe coding*—coined by Andrej Karpathy in 2025—where you describe what you want in natural language, accept AI-generated code without reviewing it, and iterate on results [10]. Vibe coding is "fully give in to the vibes, embrace exponentials, and forget that the code even exists" [10]. It works for throwaway prototypes. For production codebases, it is risky: accepting code without review is how hallucinated output gets into the codebase. Agentic coding is the opposite: bounded delegation with context and validation. Agentic coding means deploying AI agents as contributors inside your repository. They read your codebase, plan changes, write code, run tests, and prepare pull requests. The gap between an agent that behaves like a competent engineer and one that hallucinates your conventions usually comes down to one thing: how well you prepared the repository. Hallucination here means the agent invents APIs, patterns, or conventions that do not exist in your codebase—it confidently produces plausible-looking code that is wrong. That is why context and validation matter.

## What Is Agentic Coding?

Agentic coding is a step beyond autocomplete. GitHub Copilot suggests the next line. An agentic tool like OpenAI's `Codex CLI` works more like a semi-autonomous contributor. You describe a task like "add input validation to the user registration endpoint" and the agent reads relevant files, plans an approach, writes the implementation, runs your tests, and presents a diff for review [1].

I think the better way to frame this is bounded delegation. The engineer defines the task, context, and constraints. The agent executes against the codebase. The engineer reviews the result. It feels closer to supervising a fast junior engineer who can search, edit, and execute, but still needs direction.

OpenAI's `Codex CLI`, released as an open-source terminal agent in 2025, reads a file called `AGENTS.md` at the root of your repository to understand project conventions, build commands, and constraints [2]. Anthropic's `Claude Code` follows the same pattern with `CLAUDE.md` [3]. The open `AGENTS.md` standard has become the de facto way to give coding agents context [4].

That is the part people miss. The model is not the system. The context and validation pipeline wrapped around it, that is the system.

## Context Engineering Over Prompt Engineering

Prompt engineering helps with a single instruction. Context engineering is broader. It is how you structure the repository so agents load the right information at the right time. The Redis engineering team found that well-structured context reduced agent hallucinations and improved code quality [5]. Teams that adopt structured guidance files consistently report that agents stay closer to existing conventions. Bare repositories tend to get the opposite. Without grounded context, agents hallucinate: they invent patterns, APIs, and conventions that do not exist. They violate standards. They guess. Hallucination is not random noise—it is plausible, confident output that passes a quick glance but fails under validation.

For me, context engineering comes down to three things:

- Hierarchical context. A root `AGENTS.md` defines global invariants like language version, coding conventions, and hard constraints. Module-level `AGENTS.md` files add local rules. ADRs explain why decisions were made. That hierarchy matters because it prevents context blowout, where an agent wastes its token budget on irrelevant information.
- Explicit policy boundaries. Some actions should require human approval. API changes. Schema migrations. CI/CD modifications. Other actions can be autonomous. Unit tests. Documentation. Lint fixes. Without clear boundaries, agents make changes that sound reasonable but are still destructive.
- Verifiable workflows. Every agent task should follow the same loop: load context, plan, execute, validate, review. Hallucination is caught at the validate step. The agent should not merge code itself. Build, test, and lint commands belong in `AGENTS.md` so the agent can validate its own work before it hands anything back. If the agent invents a non-existent utility or calls a method that does not exist, the build or tests fail. That feedback loop is the primary defense against hallucinated code.

## Keep It Simple -- Seriously

This is where I think a lot of teams go wrong. They read about agentic coding and immediately design an elaborate framework: context packs, prompt templates with semantic versioning, agent personas with declarative read/write scopes, a seven-level directory hierarchy. I know because I built exactly that kind of framework once, then watched an architect look at it and say: "This is over-engineered. Too many named constructs. Humans have to keep this up to date."

He was right.

If you introduce a separate concept for every category of agent instruction, context packs versus skills versus snippets versus personas versus policies, you create cognitive load that people will not maintain. The teams I have seen succeed usually keep their agent infrastructure to two things:

1. A root `AGENTS.md` under 200 lines
2. A `.agents/skills/` directory with task-specific instruction files

That is enough. Context packs are basically skills with a reading list. Modern agents parse skill frontmatter at startup and auto-activate the right skill when the task matches its description [1]. Policies belong in a `## Constraints` section of your `AGENTS.md`. Prompt templates are often skills by another name.

## Superpowers: Curated Skills That Work

If you want structure without writing it yourself, [Superpowers](https://github.com/obra/superpowers) is an agentic skills framework that embeds a full software development workflow [15]. Instead of jumping straight into code, the agent steps back, teases out a spec through questions, presents the design in digestible chunks, and gets your sign-off before implementation. It then produces a detailed plan—bite-sized tasks with exact file paths and verification steps—and runs subagent-driven development with two-stage review (spec compliance, then code quality). Skills trigger automatically: brainstorming, writing-plans, test-driven-development, requesting-code-review, finishing-a-development-branch. The philosophy is TDD, YAGNI, DRY, and evidence over claims. It works with Claude Code, Cursor, Codex, and Gemini CLI. For teams that want mandatory workflows rather than suggestions, Superpowers is a plug-and-play alternative to rolling your own skills. It is more opinionated than a minimal `AGENTS.md` plus one skill, but it encodes practices this article advocates: validate before declaring success, human checkpoints, no blind delegation.

## Beads: Does Agent Memory Actually Help?

Steve Yegge's [Beads](https://github.com/steveyegge/beads) (`bd`) is a git-backed issue tracker built for AI coding agents [13]. It addresses a real problem: agents have no persistent memory between sessions. Usable context lasts about 5–15 minutes before agents need a restart or "mind wipe" compaction. Without structured memory, agents accumulate hundreds of scattered markdown plan files—conflicting, obsolete, indistinguishable. Yegge reported 605 inscrutable plans before building Beads [13]. Beads replaces that chaos with a dependency-aware task graph stored in Git (via Dolt), so agent context survives branch switches, merges, and new sessions. Commands like `bd ready` show only unblocked work; hash-based IDs prevent collisions when multiple agents run concurrently [13][14].

Does it really help? Yes, when you have hit the wall. If your agents routinely lose track of nested workstreams, forget architectural decisions, or drown in plan files, Beads gives them addressable memory. It is an instant upgrade for long-horizon, multi-session tasks. But it is earned complexity. Beads adds Dolt, formulas, molecules, and gates. For a team starting with `AGENTS.md` and one skill, that is overkill. Add Beads when you find agents repeatedly losing context or when markdown plans become unmanageable—not on day one. The same rule applies: let complexity emerge when a real task fails because the agent lacked it.

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

The steps below assume [OpenAI Codex](https://github.com/openai/codex) [2]; adapt paths and commands for Claude Code or Cursor as needed.

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

**Step 5 (optional): Install Beads for agent memory.** If agents lose context across sessions or markdown plans pile up, add [Beads](https://github.com/steveyegge/beads) [13]. With Codex:

```bash
brew install beads
cd your-project
bd init --quiet
bd setup codex
bd hooks install
```

This populates `AGENTS.md` with Beads guidance so Codex uses it for task tracking. Skip this until you hit the memory wall.

**Step 6 (optional): Install curated skills.** Codex includes a skill-installer. To add a curated skill, tell Codex: `$skill-installer gh-address-comments` (or another skill from [openai/skills](https://github.com/openai/skills)). To install a full workflow framework, tell Codex: *Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md* [15]. Skills install into `$CODEX_HOME/skills`; restart Codex after installing. Skip this until you want mandatory workflows instead of your own minimal skills.

## The Legitimate Concerns

**Will it make developers lazy?** I don't think that is the right frame. Calculators made routine arithmetic cheaper, but they did not remove the need for mathematical reasoning. Agentic coding will probably do something similar. Repetitive scaffolding becomes less valuable. Task framing, system design, debugging, and the ability to detect when a polished-looking change rests on a flawed assumption become more valuable. In a controlled study, developers using GitHub Copilot completed tasks 55.8% faster [6], and a separate randomized trial found higher code quality scores [7]. The upside looks real. It still depends on disciplined review.

**Will it make debugging harder?** It can, if people accept code they do not understand. If an agent writes code a developer cannot explain, that code is a liability in production. The SWE-bench benchmark, built from 2,294 real GitHub issues, tests whether models can resolve repository-level problems, not only produce isolated samples [8]. Software engineering is contextual. Blind delegation without review exposes that gap fast. Agents should not merge without human review.

**Will it hallucinate?** Yes, sometimes. Hallucination—confident output that is wrong—is inherent to how language models work. The term has a long history in AI. It first appeared in computer vision in the 1980s (Eric Mjolsness's thesis on "fingerprint hallucination") and in text processing in 1982 (John Irving Tait's FRUMP system "hallucinating matches" by seeing expected text regardless of input) [11]. Andrej Karpathy used it in 2015 to describe RNNs generating plausible but incorrect citations; Google researchers applied it to neural machine translation in 2017–2018 [11][12]. The Cambridge Dictionary added the AI sense in 2023. Some researchers prefer "confabulation" or "bullshit" to avoid anthropomorphizing models—the output is indifferent to truth, not mistakenly perceiving something [11]. Whatever you call it, the mitigation is layered: structured context reduces how often it happens, automated validation catches many cases before review, and human review catches the rest. A developer who skips tests or rubber-stamps diffs is accepting hallucinated code into the codebase. The process exists to surface it.

**Will it get complicated?** Only if you let it. Start with `AGENTS.md` and one skill. Add complexity only when it is earned, when a real task fails because the agent lacked context. Teams that over-engineer on day one usually abandon it by month two.

## What the Research Says: Benefits and Controversy

The evidence on agentic coding is mixed, and the controversy is real. On the positive side: GitHub Copilot users completed 12–22% more pull requests per week in field experiments [6]. A study of 567 agent-assisted PRs across 157 open-source projects found 83.77% accepted and merged, with 54.95% integrated without modification [16]. Agents excel at refactoring, documentation, testing, and bug fixes—tasks developers routinely delegate [16]. Adoption has been rapid: an estimated 15–22% of GitHub projects use coding agents only months after their emergence [17].

The counterevidence is striking. METR's 2025 randomized controlled trial with experienced open-source developers on large repositories (averaging 1M lines) found that developers using AI tools like Cursor Pro were **19% slower**—even though they believed they were 20% faster [18]. The 39-point gap between perception and reality comes from an illusion of speed: fast autocomplete feels productive, but developers spend substantial time prompting, reviewing unreliable output, and fixing AI-generated code. They accepted fewer than 44% of AI suggestions. AI helps on greenfield projects and simple tasks; it hurts on complex mature codebases where developers already have deep contextual knowledge [18].

Code quality research adds to the controversy. GitClear's analysis of 211 million changed lines found refactoring dropped from 25% of changed lines in 2021 to under 10% by 2024, copy-pasted code exceeded moved code for the first time in two decades, and code churn nearly doubled [19]. Veracode's 2025 study of 100+ models across 80 coding tasks found 45% of AI-generated code failed security tests and introduced OWASP Top 10 vulnerabilities; security performance has not improved with larger models [20]. The takeaway is not that agentic coding is useless—it is that context, validation, and human review matter more when the research shows both real gains and real risks. The teams that do well are the ones that treat agents as contributors to be supervised, not oracles to be trusted.

## The Capability Curve Makes This Urgent

The METR research group found that frontier models had a 50% task-completion time horizon of roughly 50 minutes, with that horizon doubling approximately every seven months since 2019 [9]. If that trend continues, agents will handle longer and more connected tasks. Weak process will not stay hidden. It will get amplified. If a team cannot specify how an agent should work in a repository today, it will not be in a better position when agents can take on larger refactors tomorrow.

## Start Today

OpenAI `Codex CLI` is open source [2]. The `AGENTS.md` standard is free and tool-agnostic [4]. The teams that do well here probably will not be the teams with the cleverest prompts. They will be the teams with a clean `AGENTS.md`, a few well-written skills, and the discipline to let complexity emerge only when it is earned. If you prefer a curated workflow out of the box, install [Superpowers](https://github.com/obra/superpowers) [15].

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

[10] Wikipedia, "Vibe coding," 2025. https://en.wikipedia.org/wiki/Vibe_coding

[11] Joshua Pearson, "Why 'Hallucination'? Examining the History, and Stakes, of How We Label AI's Undesirable Output," Los Angeles Review of Books, May 2024. https://lareviewofbooks.org/article/why-hallucination-examining-the-history-and-stakes-of-how-we-label-ais-undesirable-output/

[12] Wikipedia, "Hallucination (artificial intelligence)," 2025. https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)

[13] Steve Yegge, "Introducing Beads: A coding agent memory system," Medium, October 2025. https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a

[14] Beads, "Introduction," Beads Documentation. https://steveyegge.github.io/beads/

[15] obra, "Superpowers — An agentic skills framework & software development methodology that works," GitHub, 2025. https://github.com/obra/superpowers

[16] Miku Watanabe et al., "On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub," arXiv:2509.14745, 2025. https://arxiv.org/abs/2509.14745

[17] Romain Robbes et al., "Agentic Much? Adoption of Coding Agents on GitHub," arXiv:2601.18341, 2026. https://arxiv.org/abs/2601.18341

[18] METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," July 2025. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

[19] GitClear, "AI Assistant Code Quality: 2025 Data Suggests 4x Growth in Code Clones," 2025. https://www.gitclear.com/ai_assistant_code_quality_2025_research

[20] Veracode, "We Asked 100+ AI Models to Write Code. Here's How Many Failed Security Tests.," 2025. https://veracode.com/blog/genai-code-security-report
