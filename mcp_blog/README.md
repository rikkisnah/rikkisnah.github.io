# Rik Blog Public MCP

Read-only MCP server for public blog content at `www.rik-kisnah.ai`.

## Tools

- `list_posts`
- `latest_posts`
- `search_posts`
- `get_post`

The server exposes no authentication, write operations, deployment operations, Git access, shell access, or private data access. It reads only published Hugo content from `content/posts/`.

## Install

```bash
cd mcp_blog
uv sync
```

This installs the `rik-blog-mcp` console script in the local uv environment.

## Local Run

HTTP mode, useful behind nginx or for local HTTP testing:

```bash
cd mcp_blog
uv run rik-blog-mcp \
  --repo-root /mnt/data/src/rikkisnah/rikkisnah.github.io \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8765
```

Stdio mode, useful for Claude Desktop, Claude Code, and local Codex command-based MCP installs:

```bash
cd mcp_blog
uv run rik-blog-mcp \
  --repo-root /mnt/data/src/rikkisnah/rikkisnah.github.io \
  --transport stdio
```

The VM deployment should place nginx in front of this process and expose only:

- `https://mcp.rik-kisnah.ai/mcp`
- `https://mcp.rik-kisnah.ai/healthz`

## Codex Client

Remote public endpoint:

```toml
[mcp_servers.rik_blog]
url = "https://mcp.rik-kisnah.ai/mcp"
enabled_tools = ["list_posts", "latest_posts", "search_posts", "get_post"]
default_tools_approval_mode = "auto"
```

Local stdio install:

```toml
[mcp_servers.rik_blog]
command = "uv"
args = [
  "--directory",
  "/mnt/data/src/rikkisnah/rikkisnah.github.io/mcp_blog",
  "run",
  "rik-blog-mcp",
  "--repo-root",
  "/mnt/data/src/rikkisnah/rikkisnah.github.io",
  "--transport",
  "stdio",
]
enabled_tools = ["list_posts", "latest_posts", "search_posts", "get_post"]
default_tools_approval_mode = "auto"
```

Ready-to-copy examples are in:

- `client-configs/codex-remote.toml`
- `client-configs/codex-local-stdio.toml`

## Claude Client

Claude Desktop local stdio config:

```json
{
  "mcpServers": {
    "rik_blog": {
      "command": "uv",
      "args": [
        "--directory",
        "/mnt/data/src/rikkisnah/rikkisnah.github.io/mcp_blog",
        "run",
        "rik-blog-mcp",
        "--repo-root",
        "/mnt/data/src/rikkisnah/rikkisnah.github.io",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

Claude Code local stdio:

```bash
claude mcp add rik_blog -- \
  uv --directory /mnt/data/src/rikkisnah/rikkisnah.github.io/mcp_blog \
  run rik-blog-mcp \
  --repo-root /mnt/data/src/rikkisnah/rikkisnah.github.io \
  --transport stdio
```

Claude Code remote HTTP, when the public endpoint is live:

```bash
claude mcp add --transport http rik_blog https://mcp.rik-kisnah.ai/mcp
```

Ready-to-use examples are in:

- `client-configs/claude-desktop-local.json`
- `client-configs/claude-code-local.sh`
- `client-configs/claude-code-remote.sh`
