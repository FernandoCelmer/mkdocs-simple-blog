"""Generates one listing page per category/tag value."""

from __future__ import annotations

from typing import Any

from mkdocs.structure.files import File

from .slug import slugify


def _yaml_quote(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


class FilterPageGenerator:
    """Groups posts by category/tag and generates one listing page per
    value (e.g. `category/python.md`), so clicking a category or tag in
    the Blog Sidebar shows the posts that actually carry it -- MkDocs is
    a static site generator, so a real page has to exist per filter.

    Each generated page is a normal page as far as the theme is
    concerned: `blog_list: true` (and `blog_sidebar`) in its front
    matter reuses the exact same rendering already used by any
    hand-written page that opts into those components. The only extra
    bit is `blog_category`/`blog_tag`, which `BlogPlugin.on_page_context`
    reads to scope `blog_posts` down to that one group instead of the
    full site-wide collection.
    """

    def group(
        self, posts: list[dict[str, Any]], extract: Any
    ) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for post in posts:
            for value in extract(post):
                grouped.setdefault(value, []).append(post)
        return grouped

    def generate(
        self,
        files: Any,
        config: Any,
        grouped: dict[str, list[dict[str, Any]]],
        *,
        base_dir: str,
        meta_key: str,
        label: str,
    ) -> dict[str, str]:
        components = config.theme.get("components")
        title_component_disabled = (
            bool(components) and components.get("title") is False
        )

        urls: dict[str, str] = {}
        seen_slugs: dict[str, int] = {}
        for name in grouped:
            base_slug = slugify(name)
            if base_slug in seen_slugs:
                seen_slugs[base_slug] += 1
                slug = f"{base_slug}-{seen_slugs[base_slug]}"
            else:
                seen_slugs[base_slug] = 0
                slug = base_slug
            src_uri = f"{base_dir}/{slug}.md"
            title = _yaml_quote(f"{label}: {name}")
            heading = (
                f"\n# {label}: {name}\n" if title_component_disabled else ""
            )
            content = (
                "---\n"
                f"title: {title}\n"
                "blog_list: true\n"
                "blog_sidebar:\n"
                "  recent_posts: true\n"
                "  categories: true\n"
                "  tags: true\n"
                f"{meta_key}: {_yaml_quote(name)}\n"
                "---\n"
                f"{heading}"
            )
            file = File.generated(config, src_uri, content=content)
            files.append(file)
            urls[name] = file.url
        return urls
