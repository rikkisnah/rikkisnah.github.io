from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[3]
BASE_URL = "https://www.rik-kisnah.ai"


@dataclass(frozen=True)
class ContentItem:
    slug: str
    title: str
    date: str
    draft: bool
    url: str
    summary: str
    tags: tuple[str, ...]
    body: str
    path: str
    params: dict[str, Any]


def list_posts(repo_root: Path = DEFAULT_REPO_ROOT) -> list[ContentItem]:
    return _list_content(repo_root / "content" / "posts", "/posts")


def latest_posts(limit: int = 5, repo_root: Path = DEFAULT_REPO_ROOT) -> list[ContentItem]:
    safe_limit = max(1, min(limit, 50))
    return list_posts(repo_root)[:safe_limit]


def search_posts(query: str, limit: int = 10, repo_root: Path = DEFAULT_REPO_ROOT) -> list[ContentItem]:
    terms = [term.lower() for term in re.findall(r"[\w-]+", query)]
    if not terms:
        return []

    scored: list[tuple[int, ContentItem]] = []
    for post in list_posts(repo_root):
        haystacks = [
            (post.title.lower(), 5),
            (" ".join(post.tags).lower(), 4),
            (post.summary.lower(), 3),
            (post.body.lower(), 1),
        ]
        score = sum(text.count(term) * weight for term in terms for text, weight in haystacks)
        if score > 0:
            scored.append((score, post))

    scored.sort(key=lambda item: (item[0], item[1].date), reverse=True)
    return [post for _, post in scored[: max(1, min(limit, 50))]]


def get_post(slug: str, repo_root: Path = DEFAULT_REPO_ROOT) -> ContentItem | None:
    normalized = slug.removesuffix(".md").strip("/")
    if not normalized or "/" in normalized or "\\" in normalized:
        return None
    for post in list_posts(repo_root):
        if post.slug == normalized:
            return post
    return None


def public_dict(item: ContentItem, include_body: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {
        "slug": item.slug,
        "title": item.title,
        "date": item.date,
        "url": item.url,
        "summary": item.summary,
        "tags": list(item.tags),
    }
    if include_body:
        data["body"] = item.body
    return data


def _list_content(directory: Path, url_prefix: str, include_index: bool = True) -> list[ContentItem]:
    items: list[ContentItem] = []
    for path in sorted(directory.glob("*.md")):
        if not include_index and path.name == "_index.md":
            continue
        item = _read_item(path, url_prefix)
        if item and not item.draft:
            items.append(item)
    items.sort(key=lambda item: item.date, reverse=True)
    return items


def _read_item(path: Path, url_prefix: str) -> ContentItem | None:
    text = path.read_text(encoding="utf-8")
    front_matter, body = _split_front_matter(text)
    if front_matter is None:
        return None
    params = _parse_front_matter(front_matter)
    slug = path.stem
    title = str(params.get("title") or slug.replace("-", " ").title())
    date = str(params.get("date") or "")
    draft = bool(params.get("draft", False))
    tags = tuple(str(tag) for tag in params.get("tags", []))
    url = f"{BASE_URL}{url_prefix}/{quote(slug)}/"
    summary = str(params.get("summary") or params.get("description") or _summarize(body))
    return ContentItem(
        slug=slug,
        title=title,
        date=date,
        draft=draft,
        url=url,
        summary=summary,
        tags=tags,
        body=body.strip(),
        path=str(path),
        params=params,
    )


def _split_front_matter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    body_start = text.find("\n", end + 4)
    return text[4:end], text[body_start + 1 :] if body_start != -1 else ""


def _parse_front_matter(front_matter: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for line in front_matter.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        parsed[key.strip()] = _parse_value(value.strip())
    return parsed


def _parse_value(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_value(part.strip()) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _summarize(body: str) -> str:
    clean = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "![", "*Disclaimer", "*Caveat", "*Image:")):
            continue
        clean.append(re.sub(r"\s+", " ", stripped))
    text = " ".join(clean)
    return text[:277] + "..." if len(text) > 280 else text
