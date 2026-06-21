from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import content


def build_server(repo_root: Path = content.DEFAULT_REPO_ROOT) -> FastMCP:
    mcp = FastMCP("rik-blog-public")

    @mcp.tool()
    def list_posts() -> list[dict[str, Any]]:
        """List all published public blog posts."""
        return [content.public_dict(post) for post in content.list_posts(repo_root)]

    @mcp.tool()
    def latest_posts(limit: int = 5) -> list[dict[str, Any]]:
        """Return the latest published public blog posts."""
        return [content.public_dict(post) for post in content.latest_posts(limit, repo_root)]

    @mcp.tool()
    def search_posts(query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search published public blog posts by title, tags, summary, and body."""
        return [
            content.public_dict(post)
            for post in content.search_posts(query=query, limit=limit, repo_root=repo_root)
        ]

    @mcp.tool()
    def get_post(slug: str) -> dict[str, Any] | None:
        """Return a published public blog post by slug, including its markdown body."""
        post = content.get_post(slug, repo_root)
        return content.public_dict(post, include_body=True) if post else None

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the public read-only blog MCP server.")
    parser.add_argument("--repo-root", type=Path, default=content.DEFAULT_REPO_ROOT)
    parser.add_argument("--transport", choices=["stdio", "streamable-http", "sse"], default="streamable-http")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    mcp = build_server(args.repo_root.resolve())
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
