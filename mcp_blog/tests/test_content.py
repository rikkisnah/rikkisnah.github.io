from pathlib import Path

from rik_blog_mcp import content


def write_post(root: Path, name: str, front_matter: str, body: str) -> None:
    path = root / "content" / "posts" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{front_matter}\n---\n\n{body}\n", encoding="utf-8")

def test_list_posts_returns_only_published_posts(tmp_path: Path) -> None:
    write_post(
        tmp_path,
        "published",
        'title: "Published"\ndate: 2026-01-02T10:00:00-07:00\ndraft: false\ntags: ["ai", "cloud"]',
        "Published body",
    )
    write_post(
        tmp_path,
        "draft",
        'title: "Draft"\ndate: 2026-01-03T10:00:00-07:00\ndraft: true',
        "Private draft body",
    )

    posts = content.list_posts(tmp_path)

    assert [post.slug for post in posts] == ["published"]
    assert posts[0].tags == ("ai", "cloud")


def test_search_posts_scores_public_content(tmp_path: Path) -> None:
    write_post(
        tmp_path,
        "agentic-coding",
        'title: "Agentic Coding"\ndate: 2026-01-02T10:00:00-07:00\ndraft: false',
        "Repository context makes agentic coding work.",
    )
    write_post(
        tmp_path,
        "family",
        'title: "Family"\ndate: 2026-01-01T10:00:00-07:00\ndraft: false',
        "A birthday note.",
    )

    matches = content.search_posts("repository agentic", repo_root=tmp_path)

    assert [post.slug for post in matches] == ["agentic-coding"]


def test_get_post_rejects_path_traversal(tmp_path: Path) -> None:
    assert content.get_post("../secret", tmp_path) is None
    assert content.get_post("nested/secret", tmp_path) is None
