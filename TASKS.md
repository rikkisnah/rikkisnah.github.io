# TASKS.md

Working task ledger for this repository.

## Active

- Validate the MCP server exposes only:
  - `list_posts`
  - `latest_posts`
  - `search_posts`
  - `get_post`
- Review deployment notes in `docs/deploy/public-mcp.md` before applying them on the VM.

## Backlog

- Add a small smoke-test script for the deployed `/healthz` endpoint and MCP tool listing.
- Add Cloudflare-side rate limiting once DNS is active.

## Done

- Added initial `mcp_blog/` Python package with read-only content parsing and MCP tool registration.
- Added focused tests for public-only filtering, search, and path traversal rejection.
- Added public deployment notes for DNS, nginx, certbot, systemd, and verification.
- Verified MCP SDK dependency installation with `uv` using a repo-local cache.
- Added Codex and Claude install examples for remote HTTP and local stdio MCP use.
- Removed the unused audio section from the visible site and MCP tool surface.
