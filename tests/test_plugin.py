"""Tests for the mkdocs_simple_blog.plugin package."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from mkdocs.structure.files import File

from mkdocs_simple_blog.plugin import BlogPlugin, BlogPluginConfig
from mkdocs_simple_blog.plugin.collector import PostCollector
from mkdocs_simple_blog.plugin.filters import FilterPageGenerator
from mkdocs_simple_blog.plugin.git_author import GitAuthorResolver


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


def _config(
    blog: dict | None = None,
    components: dict | None = None,
    site_dir: str = "/tmp/site",
) -> SimpleNamespace:
    """Minimal stand-in for MkDocs' real config object.

    `File.generated()` reads `.site_dir`, `.use_directory_urls` and
    `.plugins._current_plugin`; `config.theme` needs `.get()` the same
    way the real Theme (a MutableMapping) does.
    """
    theme: dict = {}
    if blog is not None:
        theme["blog"] = blog
    if components is not None:
        theme["components"] = components
    return SimpleNamespace(
        theme=theme,
        site_dir=site_dir,
        use_directory_urls=True,
        plugins=SimpleNamespace(_current_plugin=None),
    )


class FakeGitAuthorResolver:
    """Deterministic stand-in for GitAuthorResolver, for tests that
    exercise PostCollector's fallback logic without shelling out to git."""

    def __init__(
        self, name: str = "", email: str = "", avatar: str = ""
    ) -> None:
        self._name = name
        self._email = email
        self._avatar = avatar

    def author_and_email(self, path: str) -> tuple[str, str]:
        return self._name, self._email

    def avatar_from_email(self, email: str) -> str:
        return self._avatar if email else ""


class GitAuthorResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = GitAuthorResolver()

    def test_avatar_from_email_github_with_numeric_id_prefix(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "123456+FernandoCelmer@users.noreply.github.com"
        )
        self.assertEqual(avatar, "https://github.com/FernandoCelmer.png")

    def test_avatar_from_email_github_without_id_prefix(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "FernandoCelmer@users.noreply.github.com"
        )
        self.assertEqual(avatar, "https://github.com/FernandoCelmer.png")

    def test_avatar_from_email_gitlab(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "fernandocelmer@users.noreply.gitlab.com"
        )
        self.assertEqual(avatar, "https://gitlab.com/fernandocelmer.png")

    def test_avatar_from_email_bitbucket(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "abc123+fernandocelmer@users.noreply.bitbucket.org"
        )
        self.assertEqual(
            avatar, "https://bitbucket.org/fernandocelmer/avatar/"
        )

    def test_avatar_from_email_unrecognized_domain_returns_empty(self) -> None:
        self.assertEqual(
            self.resolver.avatar_from_email("someone@example.com"), ""
        )

    def test_avatar_from_email_empty_returns_empty(self) -> None:
        self.assertEqual(self.resolver.avatar_from_email(""), "")

    def test_author_and_email_outside_git_repo_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "untracked.md")
            Path(path).write_text("content", encoding="utf-8")
            name, email = self.resolver.author_and_email(path)
        self.assertEqual((name, email), ("", ""))


class PostCollectorTests(unittest.TestCase):
    def _file(self, url: str = "post/a/") -> SimpleNamespace:
        return SimpleNamespace(abs_src_path="/docs/post/a.md", url=url)

    def test_uses_front_matter_author_and_github(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "author": "Fernando Celmer",
                "github": "FernandoCelmer",
            },
            self._file(),
        )
        self.assertEqual(post["author"], "Fernando Celmer")
        self.assertEqual(post["github"], "FernandoCelmer")
        self.assertEqual(
            post["avatar_url"], "https://github.com/FernandoCelmer.png"
        )

    def test_falls_back_to_theme_blog_defaults(self) -> None:
        collector = PostCollector(
            {"author": "Fernando Celmer", "github": "FernandoCelmer"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "Fernando Celmer")
        self.assertEqual(
            post["avatar_url"], "https://github.com/FernandoCelmer.png"
        )

    def test_front_matter_overrides_theme_blog_defaults(self) -> None:
        collector = PostCollector(
            {"author": "Fernando Celmer", "github": "FernandoCelmer"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "author": "Guest Writer",
                "github": "guestwriter",
            },
            self._file(),
        )
        self.assertEqual(post["author"], "Guest Writer")
        self.assertEqual(post["github"], "guestwriter")

    def test_avatar_field_takes_priority_over_github(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "github": "FernandoCelmer",
                "avatar": "https://example.com/me.png",
            },
            self._file(),
        )
        self.assertEqual(post["avatar_url"], "https://example.com/me.png")

    def test_theme_blog_avatar_used_as_fallback(self) -> None:
        collector = PostCollector(
            {"avatar": "https://example.com/default.png"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["avatar_url"], "https://example.com/default.png")

    def test_falls_back_to_git_author_when_no_author_anywhere(self) -> None:
        collector = PostCollector(
            {},
            FakeGitAuthorResolver(name="Git Author", email="git@example.com"),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "Git Author")

    def test_git_author_disabled_via_config(self) -> None:
        collector = PostCollector(
            {"git_author": False},
            FakeGitAuthorResolver(name="Git Author", email="git@example.com"),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "")

    def test_description_and_image_default_to_empty_string(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["description"], "")
        self.assertEqual(post["image"], "")

    def test_description_and_image_are_collected(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "description": "An excerpt",
                "image": "assets/cover.png",
            },
            self._file(),
        )
        self.assertEqual(post["description"], "An excerpt")
        self.assertEqual(post["image"], "assets/cover.png")

    def test_tags_default_to_empty_list(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["tags"], [])

    def test_read_front_matter_parses_yaml_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "post.md"
            path.write_text(
                "---\ntitle: A\ndate: 2024-01-01\n---\n\nbody",
                encoding="utf-8",
            )
            meta = PostCollector.read_front_matter(str(path))
        self.assertEqual(meta["title"], "A")


class FilterPageGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = FilterPageGenerator()
        self.posts = [
            {"title": "A", "category": "Python", "tags": ["python", "django"]},
            {"title": "B", "category": "Python", "tags": ["python"]},
            {"title": "C", "category": "Guides", "tags": []},
        ]

    def test_group_by_category(self) -> None:
        grouped = self.generator.group(
            self.posts, lambda p: [p["category"]] if p["category"] else []
        )
        self.assertEqual([p["title"] for p in grouped["Python"]], ["A", "B"])
        self.assertEqual([p["title"] for p in grouped["Guides"]], ["C"])

    def test_group_by_tags_fans_out_one_post_to_multiple_groups(self) -> None:
        grouped = self.generator.group(self.posts, lambda p: p["tags"])
        self.assertEqual([p["title"] for p in grouped["python"]], ["A", "B"])
        self.assertEqual([p["title"] for p in grouped["django"]], ["A"])

    def test_generate_creates_one_file_per_group_and_returns_its_url(
        self,
    ) -> None:
        files: list[File] = []
        grouped = {"Python": self.posts[:2], "Guides": self.posts[2:]}
        urls = self.generator.generate(
            files,
            _config(),
            grouped,
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertEqual(len(files), 2)
        self.assertEqual(urls["Python"], "category/python/")
        self.assertEqual(urls["Guides"], "category/guides/")

    def test_generate_sets_title_and_filter_meta_in_front_matter(self) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            _config(),
            {"Python": self.posts[:2]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        content = files[0]._content
        self.assertIn('title: "Category: Python"', content)
        self.assertIn('blog_category: "Python"', content)
        self.assertIn("blog_list: true", content)

    def test_generate_quotes_names_with_colons_and_double_quotes_safely(
        self,
    ) -> None:
        files: list[File] = []
        tricky_name = 'C++ "Notes": Vol 1'
        self.generator.generate(
            files,
            _config(),
            {tricky_name: self.posts[:1]},
            base_dir="tag",
            meta_key="blog_tag",
            label="Tag",
        )
        content = files[0]._content
        self.assertIn('blog_tag: "C++ \\"Notes\\": Vol 1"', content)

    def test_generate_omits_manual_heading_when_title_component_is_enabled(
        self,
    ) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            _config(components={"title": True}),
            {"Python": self.posts[:1]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertNotIn("\n# Category: Python\n", files[0]._content)

    def test_generate_includes_manual_heading_when_title_component_is_disabled(
        self,
    ) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            _config(components={"title": False}),
            {"Python": self.posts[:1]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertIn("\n# Category: Python\n", files[0]._content)


class BlogPluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.temp_dir, ignore_errors=True)
        self.plugin = BlogPlugin()
        self.plugin.config = BlogPluginConfig()
        self.plugin.config.load_dict({})

    def _write(
        self, rel_path: str, front_matter: str, body: str = "content"
    ) -> None:
        _write_post(self.temp_dir, rel_path, front_matter, body)

    def _file(self, rel_path: str) -> File:
        return _make_file(self.temp_dir, rel_path)

    def test_posts_missing_title_or_date_are_excluded(self) -> None:
        self._write("post/no-title.md", "date: 2024-01-01")
        self._write("post/no-date.md", "title: No Date")
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")

        files = [
            self._file("post/no-title.md"),
            self._file("post/no-date.md"),
            self._file("post/valid.md"),
        ]
        self.plugin.on_files(files, config=_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "Valid")

    def test_non_post_pages_are_ignored(self) -> None:
        self._write("index.md", "title: Home\ndate: 2024-01-01")
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")

        files = [self._file("index.md"), self._file("post/valid.md")]
        self.plugin.on_files(files, config=_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "Valid")

    def test_non_markdown_files_under_posts_dir_are_ignored(self) -> None:
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")
        image_path = self.temp_dir / "post" / "cover.png"
        image_path.write_bytes(b"\x89PNG")

        files = [self._file("post/valid.md"), self._file("post/cover.png")]
        self.plugin.on_files(files, config=_config())

        self.assertEqual(len(self.plugin.posts), 1)

    def test_posts_sorted_by_date_descending(self) -> None:
        self._write("post/oldest.md", "title: Oldest\ndate: 2022-01-01")
        self._write("post/newest.md", "title: Newest\ndate: 2024-06-01")
        self._write("post/middle.md", "title: Middle\ndate: 2023-03-15")

        files = [
            self._file("post/oldest.md"),
            self._file("post/newest.md"),
            self._file("post/middle.md"),
        ]
        self.plugin.on_files(files, config=_config())

        titles = [post["title"] for post in self.plugin.posts]
        self.assertEqual(titles, ["Newest", "Middle", "Oldest"])

    def test_custom_posts_dir(self) -> None:
        self.plugin.config = BlogPluginConfig()
        self.plugin.config.load_dict({"posts_dir": "articles"})

        self._write("articles/a.md", "title: A\ndate: 2024-01-01")
        self._write("post/b.md", "title: B\ndate: 2024-01-01")

        files = [self._file("articles/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "A")

    def test_category_and_tag_listing_pages_are_generated(self) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ncategory: Python\ntags:\n  - python\n  - django",
        )
        self._write(
            "post/b.md",
            "title: B\ndate: 2024-01-01\ncategory: Python\ntags:\n  - python",
        )

        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=_config())

        generated_uris = {
            f.src_uri for f in files if f.src_uri.startswith("categ")
        }
        self.assertIn("category/python.md", generated_uris)

        tag_uris = {f.src_uri for f in files if f.src_uri.startswith("tag/")}
        self.assertEqual(tag_uris, {"tag/python.md", "tag/django.md"})

    def test_blog_categories_and_tags_urls_point_to_generated_pages(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-01-01\ncategory: Python\ntags:\n  - python",
        )

        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=_config())

        self.assertEqual(
            self.plugin.blog_categories["Python"], "category/python/"
        )
        self.assertEqual(self.plugin.blog_tags["python"], "tag/python/")

    def test_on_page_context_scopes_blog_posts_to_the_generated_category_page(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ncategory: Python\ntags: []",
        )
        self._write(
            "post/b.md",
            "title: B\ndate: 2024-01-01\ncategory: Guides\ntags: []",
        )
        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=_config())

        page = SimpleNamespace(meta={"blog_category": "Python"})
        context = self.plugin.on_page_context(
            {}, page=page, config=_config(), nav=None
        )

        self.assertEqual([p["title"] for p in context["blog_posts"]], ["A"])

    def test_on_page_context_scopes_blog_posts_to_the_generated_tag_page(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ntags:\n  - python\n  - django",
        )
        self._write(
            "post/b.md", "title: B\ndate: 2024-01-01\ntags:\n  - django"
        )
        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=_config())

        page = SimpleNamespace(meta={"blog_tag": "python"})
        context = self.plugin.on_page_context(
            {}, page=page, config=_config(), nav=None
        )

        self.assertEqual([p["title"] for p in context["blog_posts"]], ["A"])

    def test_on_page_context_defaults_to_full_post_list_on_ordinary_pages(
        self,
    ) -> None:
        self._write("post/a.md", "title: A\ndate: 2024-01-01")
        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=_config())

        page = SimpleNamespace(meta={})
        context = self.plugin.on_page_context(
            {}, page=page, config=_config(), nav=None
        )

        self.assertEqual(context["blog_posts"], self.plugin.posts)

    def test_on_page_context_handles_none_page(self) -> None:
        self._write("post/a.md", "title: A\ndate: 2024-01-01")
        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=_config())

        context = self.plugin.on_page_context(
            {}, page=None, config=_config(), nav=None
        )

        self.assertEqual(context["blog_posts"], self.plugin.posts)


if __name__ == "__main__":
    unittest.main()
