---
title: "Content Engineering for AI Agents: Why Your Repository Isn't Ready"
date: 2026-01-19T00:00:00-07:00
slug: "repos-not-built-for-ai-agents"
summary: "Most repositories are designed for humans, not AI agents. Here’s the minimal set of repo context files and structure that makes agents reliable instead of chaotic."
tags: ["AI", "agents", "content-engineering", "documentation", "developer-experience"]
draft: false
---

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from Claude (Sonnet) and Perplexity, but I curated the content and cross-checked the references.*

![A repository structure diagram for making codebases friendlier to AI agents](/posts/repos-not-built-for-ai-agents/ai-repo.png)

## The Problem

I don't buy that repositories are ready for AI agents. Most aren't. Teams drop in tools like Claude, Codex or Copilot, expect magic, and get messes instead.

The repository assumes human readers. It expects you to remember old decisions or dig through scattered notes. AI can't do that. It guesses. It repeats errors. It breaks patterns you forgot to write down.

That's not the AI's fault. Fix the repo.

## Beyond Prompt Engineering

Prompt engineering is part of it. You craft instructions for one output. But content engineering keeps things working. It's the structure around prompts. Rules. History. Boundaries. In OCI teams, where cloud infrastructure demands precision, this matters more. Agents handle compute tasks, but without clear context, they drift.

Without a solid setup, agents ignore conventions. Prompts get lost in chats. Outputs can't be reproduced. Mistakes loop because memory isn't captured.

Put it in the repo. Plain text. Auditable.

## Core Files for Agent Context

Start with core files at the root.

**AGENT.md** sets rules for agents. Personas, boundaries, what to avoid. For OCI compute projects, it might flag sensitive configs.

**TASKS.md** holds the queue. Short list, acceptance criteria. Links to Jira.

**MEMORY.md** logs lessons. Decisions, failures. In OCI, this could note past scaling issues.

**PROMPTS.md** or a prompts folder stores templates. Versioned.

**README.md** and **CONTRIBUTING.md** stay, but point here.

## Recommended Repository Structure

The structure looks like this:

```
repo/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── AGENT.md
├── TASKS.md
├── MEMORY.md
├── PROMPTS.md
├── design/
│   ├── intake.md
│   ├── poc.md
│   ├── hld.md
│   ├── lld.md
│   ├── ecar-architect.md
│   └── decisions/
│       └── 0001-adopt-diataxis.md
├── conventions/
│   ├── coding-style.md
│   └── metadata-schema.yaml
├── ops/
│   ├── runbook.md
│   └── rca.md
├── prompts/
│   ├── system/
│   ├── developer/
│   └── user/
└── src/
```

Not fixed. Adapt it. For bigger repos, use `.ai/` to avoid clutter. Add a root pointer.

`.agent/AGENT.md` could split rules: one for tests, one for docs.

Sessions folder logs interactions. Prompts used, changes made.

## File Examples

### AGENT.md Example

```markdown
# Agent Rules

Read: README.md, CONTRIBUTING.md, MEMORY.md

Tech stack: Golang, Java, Python, Ops tools.

Do:
- Follow HLD boundaries in design/hld.md.
- Add tests for changes.
- Log with request IDs.

Do not:
- Touch secrets.
- Add deps without TASKS.md note.
- Change OCI deployment configs without approval.
```

Blunt. Specific.

### TASKS.md Example

```markdown
# Now
- [JIRA-123] Add rate limit to OCI compute client
  - Done: Tests cover backoff, runbook updated.

# Upcoming
- [JIRA-141] Split into control and data planes.

# Done
- [JIRA-118] Propagate IDs across services.
```

Current. Short.

### MEMORY.md Example

```markdown
2026-01-18
- Trigger: Perf drop after OCI retry change.
- Decision: Cap retries, add jitter.
- Implication: No retry increases without tests.

Before refactors:
- Check decisions/ for boundaries.
```

Curated. Not logs.

### PROMPTS.md Metadata

```yaml
document_type: prompt
topic: implement-tdd
version: 1.2.0
owners: oci-compute-team
created_date: 2026-01-18
model_compatibility: [gpt5, copilot]
```

## Mapping to Product Flow

This maps to product flow. OCI architects know it: intake, POC, designs, sprints, deploy.

**Requirements** in `design/intake.md`. Link from README.

**POC** in `design/poc.md`. Lessons to MEMORY.md.

**HLD** in `design/hld.md`. System shape.

**LLD** in `design/lld.md`. Details.

**Changes** in `design/ecar-architect.md`. Traceable.

**Sprints** to TASKS.md.

**Development** uses TDD, reads AGENT.md.

**Ops** in `ops/runbook.md`. Agents draft, humans check.

The repo holds the trail. Humans audit. Agents follow.

For scale, `.ai/` works. Specialized rules. Logs.

Markdown keeps it simple. Git-friendly. Tool-agnostic.

## Research and Evidence

Research backs this. GitHub reviewed 2,500+ AGENTS.md files. Success from specifics, boundaries.

Anthropic stresses context for agents. Memory, tools in repo.

Surveys show structured prompts cut variance. McKinsey notes 20-50% faster tasks with clear docs.

In OCI, where compute reliability counts, this prevents drift.

## The Reality: Adoption and Maintenance

It's work. Files need updates. MEMORY.md after bugs. TASKS.md current. AGENT.md evolves.

Teams skip it. Then blame agents.

But patterns emerge. AGENTS.md as standard. Copilot, Claude read it.

Memory, tasks less common. More value.

## The Choice

Choose. Treat agents as prompt takers, or collaborators with context.

The repo decides.

---

## References

1. GitHub Blog. "How to write a great agents.md: Lessons from over 2,500 repositories." [github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

2. Anthropic. "Effective context engineering for AI agents." [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

3. AGENTS.md. "A simple open format for guiding code agents." [agents.md](https://agents.md)

4. Builder.io. "Improve your AI code output with AGENTS.md." [builder.io/blog/agents-md](https://www.builder.io/blog/agents-md)

5. Prompt Engineering Guide. "LLM Agents." [promptingguide.ai/research/llm-agents](https://www.promptingguide.ai/research/llm-agents)

6. Schulhoff, Sander et al. "The Prompt Report: A Systematic Survey of Prompting Techniques." arXiv, June 2024. [arxiv.org/abs/2406.06608](https://arxiv.org/abs/2406.06608)

7. Sahoo, Pranab et al. "A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications." arXiv, February 2024. [arxiv.org/abs/2402.07927](https://arxiv.org/abs/2402.07927)

8. McKinsey & Company. "The economic potential of generative AI: The next productivity frontier." 2023.

9. OpenReview. "Repository-Level Prompt Generation for Large Language Models of Code." [openreview.net/forum?id=MtGmCCPJD-](https://openreview.net/forum?id=MtGmCCPJD-)

10. HumanLayer. "Writing a good CLAUDE.md." [humanlayer.dev/blog/writing-a-good-claude-md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

11. Weng, Lilian. "Prompt Engineering." Lil'Log, March 2023. https://lilianweng.github.io/posts/2023-03-15-prompt-engineering

12. AWS Machine Learning Blog. "Prompt engineering techniques and best practices: Learn by doing with Anthropic's Claude 3 on Amazon Bedrock." https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/

13. PromptHub. "Prompt Engineering Principles for 2024." https://www.prompthub.us/blog/prompt-engineering-principles-for-2024