"""Tests for BlogPlugin's front-matter collection (on_files / on_page_context)."""

from pathlib import Path

import pytest
from mkdocs.structure.files import File

from mkdocs_simple_blog.plugin import BlogPlugin, BlogPluginConfig


def _write_post(
    docs_dir: Path, rel_path: str, front_matter: str, body: str = "content"
) -> None:
    post_path = docs_dir / rel_path
    post_path.parent.mkdir(parents=True, exist_ok=True)
    post_path.write_text(
        f"---\n{front_matter}\n---\n\n{body}\n", encoding="utf-8"
    )


def _make_file(docs_dir: Path, rel_path: str) -> File:
    return File(rel_path, str(docs_dir), "site", use_directory_urls=True)


@pytest.fixture
def plugin() -> BlogPlugin:
    instance = BlogPlugin()
    instance.config = BlogPluginConfig()
    instance.config.load_dict({})
    return instance


def test_posts_missing_title_or_date_are_excluded(temp_dir, plugin):
    _write_post(temp_dir, "post/no-title.md", "date: 2024-01-01")
    _write_post(temp_dir, "post/no-date.md", "title: No Date")
    _write_post(temp_dir, "post/valid.md", "title: Valid\ndate: 2024-01-01")

    files = [
        _make_file(temp_dir, "post/no-title.md"),
        _make_file(temp_dir, "post/no-date.md"),
        _make_file(temp_dir, "post/valid.md"),
    ]

    plugin.on_files(files, config={})

    assert len(plugin.posts) == 1
    assert plugin.posts[0]["title"] == "Valid"


def test_non_post_pages_are_ignored(temp_dir, plugin):
    _write_post(temp_dir, "index.md", "title: Home\ndate: 2024-01-01")
    _write_post(temp_dir, "post/valid.md", "title: Valid\ndate: 2024-01-01")

    files = [
        _make_file(temp_dir, "index.md"),
        _make_file(temp_dir, "post/valid.md"),
    ]

    plugin.on_files(files, config={})

    assert len(plugin.posts) == 1
    assert plugin.posts[0]["title"] == "Valid"


def test_posts_sorted_by_date_descending(temp_dir, plugin):
    _write_post(temp_dir, "post/oldest.md", "title: Oldest\ndate: 2022-01-01")
    _write_post(temp_dir, "post/newest.md", "title: Newest\ndate: 2024-06-01")
    _write_post(temp_dir, "post/middle.md", "title: Middle\ndate: 2023-03-15")

    files = [
        _make_file(temp_dir, "post/oldest.md"),
        _make_file(temp_dir, "post/newest.md"),
        _make_file(temp_dir, "post/middle.md"),
    ]

    plugin.on_files(files, config={})

    titles = [post["title"] for post in plugin.posts]
    assert titles == ["Newest", "Middle", "Oldest"]


def test_categories_and_tags_deduplicated_first_seen_url(temp_dir, plugin):
    _write_post(
        temp_dir,
        "post/a.md",
        "title: A\ndate: 2024-02-01\ncategory: Python\ntags:\n  - python\n  - django",
    )
    _write_post(
        temp_dir,
        "post/b.md",
        "title: B\ndate: 2024-01-01\ncategory: Python\ntags:\n  - python",
    )

    files = [
        _make_file(temp_dir, "post/a.md"),
        _make_file(temp_dir, "post/b.md"),
    ]

    plugin.on_files(files, config={})
    context = plugin.on_page_context({}, page=None, config={}, nav=None)

    assert context["blog_categories"] == {"Python": "post/a/"}
    assert context["blog_tags"] == {"python": "post/a/", "django": "post/a/"}


def test_posts_without_tags_key_default_to_empty_list(temp_dir, plugin):
    _write_post(
        temp_dir, "post/no-tags.md", "title: No Tags\ndate: 2024-01-01"
    )

    files = [_make_file(temp_dir, "post/no-tags.md")]

    plugin.on_files(files, config={})

    assert plugin.posts[0]["tags"] == []


def test_non_markdown_files_under_posts_dir_are_ignored(temp_dir, plugin):
    _write_post(temp_dir, "post/valid.md", "title: Valid\ndate: 2024-01-01")
    image_path = temp_dir / "post" / "cover.png"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"\x89PNG")

    files = [
        _make_file(temp_dir, "post/valid.md"),
        _make_file(temp_dir, "post/cover.png"),
    ]

    plugin.on_files(files, config={})

    assert len(plugin.posts) == 1
    assert plugin.posts[0]["title"] == "Valid"


def test_custom_posts_dir(temp_dir):
    plugin = BlogPlugin()
    plugin.config = BlogPluginConfig()
    plugin.config.load_dict({"posts_dir": "articles"})

    _write_post(temp_dir, "articles/a.md", "title: A\ndate: 2024-01-01")
    _write_post(temp_dir, "post/b.md", "title: B\ndate: 2024-01-01")

    files = [
        _make_file(temp_dir, "articles/a.md"),
        _make_file(temp_dir, "post/b.md"),
    ]

    plugin.on_files(files, config={})

    assert len(plugin.posts) == 1
    assert plugin.posts[0]["title"] == "A"
