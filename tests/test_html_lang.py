"""Tests for the <html> lang and data-bs-theme attributes (issue #109)."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from .fixtures import THEME_DIR


def _html_tag(theme: dict) -> str:
    root = Path(tempfile.mkdtemp())
    (root / "docs").mkdir()
    (root / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    config = {"site_name": "Test", "theme": {"name": "simple-blog", **theme}}
    (root / "mkdocs.yml").write_text(yaml.safe_dump(config), encoding="utf-8")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
        cwd=root,
        check=True,
    )
    html = (root / "site" / "index.html").read_text()
    return re.search(r"<html[^>]*>", html).group(0)


class HtmlLangTests(unittest.TestCase):
    def test_theme_declares_locale_default(self) -> None:
        theme_config = yaml.safe_load(
            (THEME_DIR / "mkdocs_theme.yml").read_text()
        )
        self.assertEqual(theme_config["locale"], "en")
        self.assertNotIn("language", theme_config)

    def test_default_lang_is_en(self) -> None:
        self.assertIn('lang="en"', _html_tag({}))

    def test_lang_follows_locale_as_bcp47(self) -> None:
        self.assertIn('lang="pt-BR"', _html_tag({"locale": "pt_BR"}))

    def test_theme_style_defaults_to_light(self) -> None:
        self.assertIn('data-bs-theme="light"', _html_tag({}))

    def test_theme_style_dark_is_kept(self) -> None:
        self.assertIn(
            'data-bs-theme="dark"', _html_tag({"theme_style": "dark"})
        )


if __name__ == "__main__":
    unittest.main()
