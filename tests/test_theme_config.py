"""Tests for theme configuration."""

from __future__ import annotations

import unittest

import yaml
from mkdocs.theme import Theme

from .fixtures import ROOT_DIR, THEME_DIR

THEME_CONFIG_PATH = THEME_DIR / "mkdocs_theme.yml"


class ThemeConfigFileTests(unittest.TestCase):
    def test_mkdocs_theme_yml_exists(self) -> None:
        self.assertTrue(THEME_CONFIG_PATH.exists())

    def test_mkdocs_theme_yml_valid(self) -> None:
        config = yaml.safe_load(THEME_CONFIG_PATH.read_text())
        self.assertIsInstance(config, dict)
        self.assertIn("sidebar", config)

    def test_theme_default_config(self) -> None:
        """Custom keys must sit at the file's root, not nested under a
        `theme:` sub-key -- MkDocs' Theme loader merges the root dict
        directly into `config.theme.*`, so a nested `theme:` key would
        just become an inert `config.theme.theme` dict that nothing
        reads, silently breaking every default below."""
        config = yaml.safe_load(THEME_CONFIG_PATH.read_text())

        self.assertNotIn("theme", config)
        self.assertIn("sidebar", config)
        self.assertIn("navigation_depth", config)
        self.assertIn("highlightjs", config)
        self.assertIn("hljs_languages", config)


class ThemeRuntimeDefaultsTests(unittest.TestCase):
    """A consumer who doesn't set `blog`/`components`/`sidebar` in their
    own `mkdocs.yml` must still get this theme's defaults for them --
    the actual regression behind moving these keys out of a nested
    `theme:` sub-key in mkdocs_theme.yml."""

    def setUp(self) -> None:
        self.theme = Theme(name="simple-blog")

    def test_blog_default_is_exposed_directly(self) -> None:
        blog = self.theme.get("blog")
        self.assertIsNotNone(blog)
        self.assertEqual(blog["layout"], "compact")

    def test_components_default_is_exposed_directly(self) -> None:
        components = self.theme.get("components")
        self.assertIsNotNone(components)
        self.assertTrue(components["page_dates"])

    def test_sidebar_default_is_exposed_directly(self) -> None:
        self.assertFalse(self.theme.get("sidebar"))

    def test_locale_default_is_exposed_directly(self) -> None:
        """`locale` is a reserved MkDocs Theme kwarg -- it's already
        defaulted to 'en' and parsed into a Locale object by
        `Theme.__init__` itself, regardless of what mkdocs_theme.yml
        declares, so there's nothing for this theme to set here."""
        self.assertEqual(str(self.theme.get("locale")), "en")

    def test_nested_theme_key_is_not_present(self) -> None:
        self.assertIsNone(self.theme.get("theme"))


class ThemePluginRegistrationTests(unittest.TestCase):
    def test_theme_plugin_registration(self) -> None:
        pyproject = ROOT_DIR / "pyproject.toml"
        self.assertTrue(pyproject.exists())

        content = pyproject.read_text()

        self.assertIn("mkdocs.themes", content)
        self.assertIn("simple-blog", content)
        self.assertIn("mkdocs_simple_blog", content)
