"""Builds a single post dict from front matter for the blog collection."""

from __future__ import annotations

from typing import Any

from mkdocs.utils import meta as meta_utils

from .git_author import GitAuthorResolver


class PostCollector:
    """Builds a single post dict from front matter, theme.blog defaults,
    and (optionally) git-derived author/avatar fallback."""

    def __init__(
        self, blog_config: dict[str, Any], git: GitAuthorResolver
    ) -> None:
        self.default_author = blog_config.get("author", "")
        self.default_github = blog_config.get("github", "")
        self.default_avatar = blog_config.get("avatar", "")
        self.use_git_author = blog_config.get("git_author", True)
        self.git = git

    def build(self, page_meta: dict[str, Any], file: Any) -> dict[str, Any]:
        author = page_meta.get("author") or self.default_author
        github = page_meta.get("github") or self.default_github
        avatar_url = page_meta.get("avatar") or self.default_avatar

        if self.use_git_author and (
            not author or (not avatar_url and not github)
        ):
            git_name, git_email = self.git.author_and_email(file.abs_src_path)
            author = author or git_name
            if not avatar_url and not github:
                avatar_url = self.git.avatar_from_email(git_email)

        if not avatar_url and github:
            avatar_url = f"https://github.com/{github}.png"

        return {
            "title": page_meta["title"],
            "date": page_meta["date"],
            "category": page_meta.get("category", ""),
            "tags": page_meta.get("tags") or [],
            "url": file.url,
            "author": author,
            "github": github,
            "avatar_url": avatar_url,
            "description": page_meta.get("description", ""),
            "image": page_meta.get("image", ""),
        }

    @staticmethod
    def read_front_matter(path: str) -> dict[str, Any]:
        with open(path, encoding="utf-8-sig") as f:
            source = f.read()
        _, page_meta = meta_utils.get_data(source)
        return page_meta
