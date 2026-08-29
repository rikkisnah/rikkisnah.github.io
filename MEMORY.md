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

## Publishing Definition of Done

- A Git push is not a completed publication.
- Before saying a post is ready, verify that the post is not a draft, the production Hugo build includes it, the GitHub Pages workflow for the exact pushed SHA succeeded, and the public canonical URL returns HTTP 200 with the new title.
- When the post has a lead image, verify its public URL too.
- Until the public page is verified, state what is pending. When it is verified, say: `Ready to check now:` and give the canonical public URL.
