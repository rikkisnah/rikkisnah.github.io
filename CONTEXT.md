# CONTEXT.md

Context map for future agents working in this repository.

## Project Shape

This repository is primarily a Hugo blog, not an application monorepo. Keep changes small and content-focused unless the user explicitly asks for infrastructure or tooling work.

Key paths:

- `hugo.toml` - site configuration, menus, and output formats.
- `content/posts/` - public blog posts in Markdown.
- `static/` - static images, PDFs, and post assets.
- `mcp_blog/` - read-only public MCP service for published content.
- `docs/deploy/public-mcp.md` - deployment runbook for `mcp.rik-kisnah.ai`.

## Agent Rules

- Read `AGENTS.md` first. `CLAUDE.md` is only a compatibility symlink.
- Do not edit `themes/hugo-paper/` directly.
- Do not commit generated cache/build artifacts such as `public/`, `.pytest_cache/`, `__pycache__/`, or `.venv/`.
- For content changes, run a Hugo build when Hugo is available.
- For MCP changes, run `python3 -m pytest mcp_blog/tests` and an import/server smoke test after dependencies are installed.

## MCP Boundary

The public MCP endpoint is intentionally unauthenticated because it serves public website content. Keep future private or write-capable tools on a separate authenticated endpoint.
