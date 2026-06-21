---
title: "MCP"
draft: false
---

## Public Blog MCP

This site has a public, read-only Model Context Protocol server for published blog content.

Endpoint:

```text
https://mcp.rik-kisnah.ai/mcp
```

The endpoint is intentionally unauthenticated because it exposes only public blog content that is already available on this website.

## Available Tools

- `list_posts` - list published blog posts
- `latest_posts` - return the newest published posts
- `search_posts` - search published posts by title, tags, summary, and body
- `get_post` - fetch a published post by slug, including the markdown body

## Codex

Add this to your Codex MCP config:

```toml
[mcp_servers.rik_blog]
url = "https://mcp.rik-kisnah.ai/mcp"
enabled_tools = ["list_posts", "latest_posts", "search_posts", "get_post"]
default_tools_approval_mode = "auto"
```

Then ask Codex questions such as:

```text
List Rik's latest blog posts.
```

```text
Search Rik's blog for posts about agentic coding.
```

```text
Fetch the post "your-ai-strategy-is-read-only" and summarize it.
```

## Claude Code

Add the remote MCP server:

```bash
claude mcp add --transport http rik_blog https://mcp.rik-kisnah.ai/mcp
```

Claude can then use the same public tools to list, search, and read posts.

## Boundary

The public MCP server does not provide tools for:

- editing posts
- reading drafts
- deploying the site
- running shell commands
- accessing Git
- reading private files
- mutating this repository

Future private or write-capable MCP tools should use a separate authenticated endpoint.
