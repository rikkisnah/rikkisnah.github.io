---
title: "Markdown Is the New Source Code: A Paradigm Shift for AI-Assisted Development"
date: 2025-12-14T10:00:00-07:00
draft: false
tags: ["AI", "documentation", "markdown", "development", "Claude Code", "agents", "token-hygiene"]
---

![Markdown Is the New Source Code](/posts/markdown-Is-the-new-source-code/markdown-Is-the-new-source-code.png)

> **Disclaimer:** This blog post was written with AI assistance using Claude Code. The ideas and perspectives are my own, refined through conversation with AI. The accompanying image was generated using AI tools.

The way we write software is changing. Not just the tools—the fundamental structure of how we organize information for development.

For the past two years, most of us have used AI assistants that autocomplete code and speed up boilerplate. These tools are useful, but they keep humans firmly in the driver's seat. You type, the model suggests, you accept or reject. Simple.

But something bigger is happening. Teams that achieve the best outcomes with AI tooling are doing something different: they are treating **Markdown as a first-class citizen** in their repositories. This sounds almost too simple to matter. It is not.

## The Token-Based Reality

Here is the fundamental shift: Large Language Models operate on tokens, not lines of code, not wiki pages, not Confluence articles. Every character, every whitespace, every piece of context consumes tokens. Tokens have a cost—both financial and cognitive for the model.

This changes everything about how we should structure information.

Traditional workflows push documentation to external systems—Jira for tickets, Confluence for design docs, wikis for runbooks. The code lives in one place, the context lives in another. For human developers, this is manageable. We can hold context in our heads, switch between browser tabs, piece together information from multiple sources.

AI tools cannot do this efficiently. When you ask an AI to work on your codebase, it sees only what you put in front of it. If your architecture, your constraints, your design decisions live in scattered wiki pages and stale Confluence documents, the AI is flying blind. It has to guess at intent. It hallucinates confidently about things it should have been told.

The fix is straightforward: bring the context to where the code lives.

## Documentation as the Prompt

The insight that changed how I think about AI-assisted development came from a simple realization: **documentation is no longer an afterthought—it becomes the prompt that drives implementation**.

Consider the traditional workflow:
1. Ticket gets created in Jira
2. Someone writes a design doc in Confluence
3. Design doc gets stale within weeks
4. Developer writes code based on half-remembered conversations
5. Documentation is updated (maybe) after the fact

Now consider the emerging workflow:
1. Design document lives in the repository as Markdown
2. Document describes architecture, constraints, and intent
3. AI agent reads the document as context
4. AI proposes implementation that respects the documented constraints
5. Implementation and documentation evolve together

The second workflow treats the design document as source-controlled, version-tracked, and executable context. When the AI reads your HLD (High-Level Design) before proposing changes, it produces dramatically better output than when it jumps straight into code generation.

This is not theoretical. Teams that begin with structured Markdown documents—design docs, intake specs, architectural decision records—consistently achieve better outcomes than teams that jump straight into prompting for code. The upfront investment in structured context pays dividends in reduced iteration and fewer hallucinated assumptions.

## The Diátaxis Connection

There is a documentation framework called [Diátaxis](https://diataxis.fr/) that organizes content into four categories: tutorials (learning-oriented), how-to guides (problem-solving), reference (information-oriented), and explanation (understanding-oriented). The framework predates the current AI wave, but it maps remarkably well to how AI agents discover and consume information.

The core insight is that these four types serve different purposes and should be separated. Mixing them creates documents that are too long, too unfocused, and difficult to navigate—for humans and AI alike.

When you structure repository documentation using this separation of concerns, agents can locate the right kind of guidance for the right kind of task. Need to understand *why* something is designed a certain way? Look in explanations. Need the exact API shape? Look in references. Need to accomplish a specific task? Look in how-tos.

This dual-purpose documentation serves both human onboarding and AI context. As one colleague put it: "Technically, we are onboarding the AI agent every time in a new session." If your documentation is good enough to onboard a new developer, it is good enough to provide context to an AI agent.

## Token Hygiene and TOON

Once you accept that tokens are the fundamental unit of AI interaction, optimization patterns start to emerge.

There is a concept called TOON (Token-Oriented Object Notation) that treats token efficiency the same way we treat byte efficiency in web performance. If you have ever minified JavaScript to reduce download time, you already understand the principle: same data, more compact encoding, optimized for a different consumer.

TOON applies this to AI context. Instead of passing verbose, semi-structured data through the context window, you compress it into intentional, compact representations that preserve meaning while cutting token spend.

This is not about being cheap with API costs (though that matters). It is about keeping the most relevant context in the model's attention. A bloated context window filled with noise means the model pays less attention to the signal. Compact, intentional structure helps the model focus on what matters.

Practically, this means:
- Preferring structured Markdown over prose where possible
- Using YAML or JSON for configuration and structured data
- Creating explicit schemas rather than ad-hoc formats
- Treating context size as a constraint to design around

## The Agents.md Standard

A concrete example of this paradigm shift is the emerging [Agents.md](https://agents.md/) standard. This is a simple Markdown file that lives at the repository root and acts as a "README for agents." It provides machine-readable instructions on setup, testing, coding style, and boundaries.

The format is straightforward: a Markdown document with specific sections that AI tools can parse. Different tools (Cline, Aider, Cursor, and others) are starting to recognize this file automatically, providing consistent guidance across tooling.

This is what "Markdown as first-class citizen" looks like in practice. The same document that helps a human developer understand how to contribute to a project also tells an AI agent how to behave in that repository.

## What This Means for Your Workflow

If you are exploring AI-assisted development, here are practical steps based on what I have seen work:

**Start with structure, not prompts.** Before asking an AI to write code, write down the context it needs. What are the constraints? What architectural patterns should it follow? What should it absolutely not do? Put this in Markdown files in your repository.

**Adopt a documentation framework.** Diátaxis is one option. The specific framework matters less than having separation between different types of content. Make it easy to find the right information for the right purpose.

**Version-control your context.** Design docs, architectural decision records, and coding standards belong in the repository, not in a wiki that drifts out of sync. When context is version-controlled, it evolves with the code.

**Treat context size as a constraint.** Think about token efficiency the way you think about memory efficiency or API response times. Compact, intentional structure is not premature optimization—it is hygiene.

**Write for dual audiences.** The best documentation serves both human developers and AI agents. If a new team member could onboard from your docs, an AI agent can get useful context from them too.

## The Shift in Mindset

The paradigm shift is not really about Markdown versus other formats. It is about recognizing that the structure of information—how it is organized, where it lives, how explicit it is—directly affects the quality of AI-assisted work.

Code will always matter. But in an AI-assisted world, the context around code matters just as much. Engineers who invest in structured, explicit, version-controlled documentation will get better outcomes from AI tools than those who do not.

Markdown and JSON are not the destination. They are the most practical vehicles right now for making context explicit and machine-readable. The underlying principle is simpler: treat context as seriously as you treat code.

Tokens are money, but well-structured context is the hygiene that unlocks leverage.

---

## Watch & Listen

<iframe width="560" height="315" src="https://www.youtube.com/embed/jYPSvKXUhcg" title="Markdown Is the New Source Code" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

- [Watch on YouTube](https://www.youtube.com/watch?v=jYPSvKXUhcg)

---

*Rik Kisnah is a Senior Principal Engineer working on GPU/AI infrastructure. He writes about infrastructure engineering, AI-assisted development, and the practical realities of building systems at scale.*

---

**References:**
- [Diátaxis Documentation Framework](https://diataxis.fr/)
- [Agents.md Standard](https://agents.md/)
- [Anthropic: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
