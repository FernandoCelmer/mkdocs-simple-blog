"""Tests for the 404 page (issue #105)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from .fixtures import THEME_DIR


def _build(theme: dict, overrides: dict[str, str] | None = None) -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "docs").mkdir()
    (root / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    if overrides:
        (root / "overrides").mkdir()
        for name, content in overrides.items():
            (root / "overrides" / name).write_text(content, encoding="utf-8")
        theme = {**theme, "custom_dir": "overrides"}
    config = {"site_name": "Test", "theme": {"name": "simple-blog", **theme}}
    (root / "mkdocs.yml").write_text(yaml.safe_dump(config), encoding="utf-8")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
        cwd=root,
        check=True,
    )
    return root / "site"


class NotFoundTemplateTests(unittest.TestCase):
    def test_theme_registers_404_as_static_template(self) -> None:
        theme_config = yaml.safe_load(
            (THEME_DIR / "mkdocs_theme.yml").read_text()
        )
        self.assertIn("404.html", theme_config["static_templates"])

    def test_build_generates_404_page(self) -> None:
        html = (_build({}) / "404.html").read_text()
        self.assertIn("<title>Page not found - Test", html)
        self.assertIn('id="component-not-found"', html)
        self.assertIn("Back to home", html)

    def test_404_renders_with_sidebar_layout(self) -> None:
        html = (_build({"sidebar": True}) / "404.html").read_text()
        self.assertIn('id="component-sidebar"', html)
        self.assertIn('id="component-not-found"', html)

    def test_custom_dir_can_override_404(self) -> None:
        custom = '{% extends "base.html" %}{% block content %}<h1 id="mine">Gone</h1>{% endblock %}'
        html = (_build({}, {"404.html": custom}) / "404.html").read_text()
        self.assertIn('id="mine"', html)
        self.assertNotIn('id="component-not-found"', html)


if __name__ == "__main__":
    unittest.main()
