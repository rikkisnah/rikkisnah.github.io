#!/usr/bin/env bash
set -euo pipefail

claude mcp add rik_blog -- \
  uv --directory /mnt/data/src/rikkisnah/rikkisnah.github.io/mcp_blog \
  run rik-blog-mcp \
  --repo-root /mnt/data/src/rikkisnah/rikkisnah.github.io \
  --transport stdio
