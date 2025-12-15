---
title: "Episode 2: Markdown Is the New Source Code"
date: 2025-12-14T10:00:00-07:00
draft: false
audioUrl: "https://objectstorage.us-phoenix-1.oraclecloud.com/n/axbtr6skl2h2/b/rikkisnah-github-podcast-media/o/markdown-is-the-new-source-code-podcast.mp3"
youtubeVideo: "https://www.youtube.com/watch?v=jYPSvKXUhcg"
length: 0
duration: "00:05:00"
episode: 2
season: 1
summary: "A paradigm shift in AI-assisted development: treating Markdown as first-class source code for better AI outcomes"
description: "Exploring how teams achieve better AI-assisted development outcomes by treating Markdown documentation as a first-class citizen in their repositories. Topics include token hygiene, the Diátaxis framework, and the emerging Agents.md standard."
keywords: ["AI", "markdown", "development", "documentation", "token-hygiene", "Claude Code", "agents"]
episodeImage: "/posts/markdown-Is-the-new-source-code/markdown-Is-the-new-source-code.png"
---

## Show Notes

The way we write software is changing. Not just the tools—the fundamental structure of how we organize information for development.

For the past two years, most of us have used AI assistants that autocomplete code and speed up boilerplate. These tools are useful, but they keep humans firmly in the driver's seat. You type, the model suggests, you accept or reject. Simple.

But something bigger is happening. Teams that achieve the best outcomes with AI tooling are doing something different: they are treating Markdown as a first-class citizen in their repositories. This sounds almost too simple to matter. It is not.

### The Token-Based Reality

Large Language Models operate on tokens, not lines of code, not wiki pages, not Confluence articles. Every character, every whitespace, every piece of context consumes tokens. Tokens have a cost—both financial and cognitive for the model.

This changes everything about how we should structure information.

Traditional workflows push documentation to external systems—Jira for tickets, Confluence for design docs, wikis for runbooks. The code lives in one place, the context lives in another. For human developers, this is manageable. We can hold context in our heads, switch between browser tabs, piece together information from multiple sources.

AI tools cannot do this efficiently. When you ask an AI to work on your codebase, it sees only what you put in front of it. If your architecture, your constraints, your design decisions live in scattered wiki pages and stale Confluence documents, the AI is flying blind. It has to guess at intent. It hallucinates confidently about things it should have been told.

The fix is straightforward: bring the context to where the code lives.

### Documentation as the Prompt

The insight that changed how I think about AI-assisted development came from a simple realization: documentation is no longer an afterthought—it becomes the prompt that drives implementation.

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

### The Diátaxis Connection

There is a documentation framework called Diátaxis that organizes content into four categories: tutorials (learning-oriented), how-to guides (problem-solving), reference (information-oriented), and explanation (understanding-oriented). The framework predates the current AI wave, but it maps remarkably well to how AI agents discover and consume information.

When you structure repository documentation using this separation of concerns, agents can locate the right kind of guidance for the right kind of task.

### Token Hygiene and TOON

Once you accept that tokens are the fundamental unit of AI interaction, optimization patterns start to emerge.

There is a concept called TOON (Token-Oriented Object Notation) that treats token efficiency the same way we treat byte efficiency in web performance. If you have ever minified JavaScript to reduce download time, you already understand the principle: same data, more compact encoding, optimized for a different consumer.

Practically, this means:
- Preferring structured Markdown over prose where possible
- Using YAML or JSON for configuration and structured data
- Creating explicit schemas rather than ad-hoc formats
- Treating context size as a constraint to design around

### The Agents.md Standard

A concrete example of this paradigm shift is the emerging Agents.md standard. This is a simple Markdown file that lives at the repository root and acts as a "README for agents." It provides machine-readable instructions on setup, testing, coding style, and boundaries.

This is what "Markdown as first-class citizen" looks like in practice. The same document that helps a human developer understand how to contribute to a project also tells an AI agent how to behave in that repository.

### The Shift in Mindset

The paradigm shift is not really about Markdown versus other formats. It is about recognizing that the structure of information—how it is organized, where it lives, how explicit it is—directly affects the quality of AI-assisted work.

Code will always matter. But in an AI-assisted world, the context around code matters just as much. Engineers who invest in structured, explicit, version-controlled documentation will get better outcomes from AI tools than those who do not.

Tokens are money, but well-structured context is the hygiene that unlocks leverage.

## Watch on YouTube

<iframe width="560" height="315" src="https://www.youtube.com/embed/jYPSvKXUhcg" title="Markdown Is the New Source Code" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

[Watch on YouTube](https://www.youtube.com/watch?v=jYPSvKXUhcg)

## Links Mentioned

- [Diátaxis Documentation Framework](https://diataxis.fr/)
- [Agents.md Standard](https://agents.md/)
- [Anthropic: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Related

- [Blog post: Markdown Is the New Source Code](/posts/markdown-is-the-new-source-code/)
