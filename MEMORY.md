# MEMORY.md

Persistent notes for human and AI-assisted work in this repository.

## Repository Facts

- This is a Hugo static site published at `https://www.rik-kisnah.ai/`.
- The theme is `themes/hugo-paper/` and is a Git submodule. Do not edit theme files directly.
- `AGENTS.md` is the source agent-instruction file. `CLAUDE.md` must remain a symlink to `AGENTS.md`.
- Blog posts live in `content/posts/`.
- Generated site output belongs in `public/` and should not be committed.

## Current Direction

- A public, read-only MCP service is being added under `mcp_blog/`.
- The intended public endpoint is `https://mcp.rik-kisnah.ai/mcp`.
- The public MCP service must expose only published blog content and no write, deploy, Git, shell, admin, auth, or private-data tools.

## Operational Notes

- Keep `.nojekyll`, `_config.yml`, and `.github/workflows/hugo.yaml` intact for GitHub Pages.
- Use Pacific time offsets in content front matter.
- For blog posts, preserve the required top-of-post stack: lead image, reading metadata, disclaimer, caveat, optional image credit, then body heading.
