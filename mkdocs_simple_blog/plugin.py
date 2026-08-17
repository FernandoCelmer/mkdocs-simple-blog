"""MkDocs plugin: collects blog post metadata from front matter.

Scans docs/post/**/*.md (or theme.plugins.simple_blog.posts_dir) once via
on_files -- before any page is rendered -- so the full, sorted post
collection is available to templates through page context, instead of
being accumulated incrementally across per-page on_page_markdown calls.
"""

from __future__ import annotations

from typing import Any

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.utils import meta as meta_utils


class BlogPluginConfig(Config):
    posts_dir = config_options.Type(str, default="post")


class BlogPlugin(BasePlugin[BlogPluginConfig]):
    """Builds a sorted post collection from front matter for use in templates.

    Exposes three context variables on every page via on_page_context:
      - blog_posts: list of post dicts, sorted by date descending
      - blog_categories: dict of {category: first post url}, in first-seen order
      - blog_tags: dict of {tag: first post url}, in first-seen order
    """

    def on_files(self, files, config):
        self.posts: list[dict[str, Any]] = []

        prefix = f"{self.config.posts_dir}/"
        for file in files:
            if not file.src_uri.startswith(prefix):
                continue
            if not file.src_uri.endswith(".md"):
                continue

            page_meta = self._read_front_matter(file.abs_src_path)
            if not page_meta.get("title") or not page_meta.get("date"):
                # Not a post (or missing required metadata) -- let it
                # render as a normal page, just excluded from the collection.
                continue

            self.posts.append(
                {
                    "title": page_meta["title"],
                    "date": page_meta["date"],
                    "category": page_meta.get("category", ""),
                    "tags": page_meta.get("tags") or [],
                    "url": file.url,
                }
            )

        self.posts.sort(key=lambda post: str(post["date"]), reverse=True)
        return files

    def on_page_context(self, context, page, config, nav):
        context["blog_posts"] = self.posts
        context["blog_categories"] = self._collect(
            lambda post: [post["category"]] if post["category"] else []
        )
        context["blog_tags"] = self._collect(lambda post: post["tags"])
        return context

    def _collect(self, extract) -> dict[str, str]:
        seen: dict[str, str] = {}
        for post in self.posts:
            for value in extract(post):
                seen.setdefault(value, post["url"])
        return seen

    @staticmethod
    def _read_front_matter(path: str) -> dict[str, Any]:
        with open(path, encoding="utf-8-sig") as f:
            source = f.read()
        _, page_meta = meta_utils.get_data(source)
        return page_meta
