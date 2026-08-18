"""Shared test doubles and helpers for mkdocs_simple_blog tests."""

from __future__ import annotations

import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from mkdocs.structure.files import File

ROOT_DIR = Path(__file__).parent.parent
THEME_DIR = ROOT_DIR / "mkdocs_simple_blog"


def mkdocs_config() -> dict[str, Any]:
    """Build a minimal MkDocs site config dict for template rendering tests."""
    return {
        "site_name": "Test Site",
        "site_url": "https://example.com",
        "site_description": "Test Description",
        "site_author": "Test Author",
        "theme": {
            "name": "simple-blog",
            "favicon": "assets/favicon.ico",
            "logo": "assets/logo.png",
            "theme_style": "light",
            "site_name_style": "bold",
            "title_style": "bold",
            "sidebar": True,
            "navigation_depth": 2,
            "highlightjs": False,
            "hljs_languages": [],
            "colors": {
                "text": "black",
                "title": "black",
                "primary": "black",
                "background": "white",
            },
            "components": {
                "site_name": True,
                "title": False,
                "menu": True,
                "preview": True,
                "footer": True,
            },
        },
        "extra_css": [],
        "extra_javascript": [],
        "nav": [{"Home": "index.md"}],
    }


def mock_page(**overrides: Any) -> SimpleNamespace:
    """Build a mock MkDocs page object for template rendering tests."""
    defaults: dict[str, Any] = {
        "title": "Test Page",
        "is_homepage": False,
        "canonical_url": "https://example.com/test/",
        "content": "# Test Page\n\nThis is a test page.",
        "url": "test/",
        "abs_url": "https://example.com/test/",
        "meta": {},
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def write_post(
    docs_dir: Path, rel_path: str, front_matter: str, body: str = "content"
) -> None:
    post_path = docs_dir / rel_path
    post_path.parent.mkdir(parents=True, exist_ok=True)
    post_path.write_text(
        f"---\n{front_matter}\n---\n\n{body}\n", encoding="utf-8"
    )


def make_file(docs_dir: Path, rel_path: str) -> File:
    return File(rel_path, str(docs_dir), "site", use_directory_urls=True)


def fake_config(
    blog: dict | None = None,
    components: dict | None = None,
    site_dir: str | None = None,
    locale: str | None = None,
) -> SimpleNamespace:
    """Minimal stand-in for MkDocs' real config object.

    `File.generated()` reads `.site_dir`, `.use_directory_urls` and
    `.plugins._current_plugin`; `config.theme` needs `.get()` the same
    way the real Theme (a MutableMapping) does.

    `site_dir` defaults to a fresh `tempfile.mkdtemp()` rather than a
    hardcoded `/tmp/site` -- on macOS, `/tmp` is a symlink to
    `/private/tmp`, and some MkDocs internals resolve that symlink,
    which can make path comparisons against a hardcoded literal flaky.
    """
    if site_dir is None:
        site_dir = tempfile.mkdtemp()
    theme: dict = {}
    if blog is not None:
        theme["blog"] = blog
    if components is not None:
        theme["components"] = components
    if locale is not None:
        theme["locale"] = locale
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
