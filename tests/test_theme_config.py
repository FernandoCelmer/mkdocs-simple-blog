"""Tests for theme configuration."""

from __future__ import annotations

import unittest

import yaml

from .fixtures import ROOT_DIR, THEME_DIR

THEME_CONFIG_PATH = THEME_DIR / "mkdocs_theme.yml"


class ThemeConfigFileTests(unittest.TestCase):
    def test_mkdocs_theme_yml_exists(self) -> None:
        self.assertTrue(THEME_CONFIG_PATH.exists())

    def test_mkdocs_theme_yml_valid(self) -> None:
        config = yaml.safe_load(THEME_CONFIG_PATH.read_text())
        self.assertIsInstance(config, dict)
        self.assertIn("theme", config)

    def test_theme_default_config(self) -> None:
        config = yaml.safe_load(THEME_CONFIG_PATH.read_text())
        theme = config.get("theme", {})

        self.assertIn("sidebar", theme)
        self.assertIn("navigation_depth", theme)
        self.assertIn("highlightjs", theme)
        self.assertIn("hljs_languages", theme)


class ThemePluginRegistrationTests(unittest.TestCase):
    def test_theme_plugin_registration(self) -> None:
        pyproject = ROOT_DIR / "pyproject.toml"
        self.assertTrue(pyproject.exists())

        content = pyproject.read_text()

        self.assertIn("mkdocs.themes", content)
        self.assertIn("simple-blog", content)
        self.assertIn("mkdocs_simple_blog", content)
