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

from .collector import PostCollector
from .dates import format_date
from .filters import FilterPageGenerator
from .git_author import GitAuthorResolver
from .git_dates import GitDatesResolver

__all__ = [
    "BlogPlugin",
    "BlogPluginConfig",
    "GitAuthorResolver",
    "GitDatesResolver",
    "PostCollector",
]


class BlogPluginConfig(Config):
    posts_dir = config_options.Type(str, default="post")
    category_dir = config_options.Type(str, default="category")
    tag_dir = config_options.Type(str, default="tag")


class BlogPlugin(BasePlugin[BlogPluginConfig]):
    """Builds a sorted post collection from front matter for use in templates.

    Exposes three context variables via on_page_context:
      - blog_posts: on most pages, every post sorted by date descending;
        on a generated category/tag page, only the posts in that group
      - blog_categories: dict of {category: listing page url}
      - blog_tags: dict of {tag: listing page url}
    """

    def on_env(self, env, config, files):
        locale = config.theme.get("locale") or "en"
        env.filters["fmt_date"] = lambda value: format_date(
            value, locale=locale
        )
        return env

    def on_files(self, files, config):
        blog_config = config.theme.get("blog") or {}
        collector = PostCollector(blog_config, GitAuthorResolver())
        self.git_dates = GitDatesResolver()

        self.posts: list[dict[str, Any]] = []
        prefix = f"{self.config.posts_dir}/"
        for file in files:
            if not file.src_uri.startswith(prefix):
                continue
            if not file.src_uri.endswith(".md"):
                continue

            page_meta = collector.read_front_matter(file.abs_src_path)
            if not page_meta.get("title") or not page_meta.get("date"):
                continue

            self.posts.append(collector.build(page_meta, file))

        self.posts.sort(key=lambda post: str(post["date"]), reverse=True)

        generator = FilterPageGenerator()
        self.category_posts = generator.group(
            self.posts,
            lambda post: [post["category"]] if post["category"] else [],
        )
        self.tag_posts = generator.group(self.posts, lambda post: post["tags"])

        self.blog_categories = generator.generate(
            files,
            config,
            self.category_posts,
            base_dir=self.config.category_dir,
            meta_key="blog_category",
            label="Category",
        )
        self.blog_tags = generator.generate(
            files,
            config,
            self.tag_posts,
            base_dir=self.config.tag_dir,
            meta_key="blog_tag",
            label="Tag",
        )
        return files

    def on_page_context(self, context, page, config, nav):
        meta = page.meta if page else {}
        category = meta.get("blog_category")
        tag = meta.get("blog_tag")

        if category:
            context["blog_posts"] = self.category_posts.get(category, [])
        elif tag:
            context["blog_posts"] = self.tag_posts.get(tag, [])
        else:
            context["blog_posts"] = self.posts

        context["blog_categories"] = self.blog_categories
        context["blog_tags"] = self.blog_tags

        components = config.theme.get("components") or {}
        path = getattr(getattr(page, "file", None), "abs_src_path", None)
        if (
            page is not None
            and path
            and components.get("page_dates") is not False
        ):
            locale = config.theme.get("locale") or "en"
            meta.setdefault(
                "git_creation_date_localized",
                self.git_dates.created_date(path, locale=locale),
            )
            meta.setdefault(
                "git_revision_date_localized",
                self.git_dates.revision_date(path, locale=locale),
            )

        return context
