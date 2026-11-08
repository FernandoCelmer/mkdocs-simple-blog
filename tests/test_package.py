"""Tests for package structure and metadata."""

from __future__ import annotations

import importlib
import unittest

from .fixtures import THEME_DIR


class PackageStructureTests(unittest.TestCase):
    def test_package_init_exists(self) -> None:
        self.assertTrue((THEME_DIR / "__init__.py").exists())

    def test_package_structure(self) -> None:
        required_files = [
            "__init__.py",
            "base.html",
            "main.html",
            "search.html",
            "mkdocs_theme.yml",
        ]
        for file_name in required_files:
            with self.subTest(file_name=file_name):
                self.assertTrue((THEME_DIR / file_name).exists())

        required_dirs = ["modules", "assets"]
        for dir_name in required_dirs:
            with self.subTest(dir_name=dir_name):
                dir_path = THEME_DIR / dir_name
                self.assertTrue(dir_path.exists())
                self.assertTrue(dir_path.is_dir())


class PackageMetadataTests(unittest.TestCase):
    def test_package_version(self) -> None:
        from mkdocs_simple_blog import __version__

        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)
        self.assertGreater(len(__version__), 0)

    def test_package_author(self) -> None:
        from mkdocs_simple_blog import __author__

        self.assertIsNotNone(__author__)
        self.assertIsInstance(__author__, str)
        self.assertGreater(len(__author__), 0)


class PackagingConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            tomllib = importlib.import_module("tomllib")
        except ModuleNotFoundError:
            self.skipTest("tomllib requires Python 3.11+")
        self.root = THEME_DIR.parent
        with open(self.root / "pyproject.toml", "rb") as handle:
            self.pyproject = tomllib.load(handle)

    def test_pyproject_is_the_only_build_config(self) -> None:
        for legacy in ("setup.py", "setup.cfg", "MANIFEST.in"):
            with self.subTest(file=legacy):
                self.assertFalse((self.root / legacy).exists())

    def test_pyproject_declares_theme_and_plugin_entry_points(self) -> None:
        plugins = self.pyproject["tool"]["poetry"]["plugins"]
        self.assertEqual(
            plugins["mkdocs.themes"]["simple-blog"], "mkdocs_simple_blog"
        )
        self.assertEqual(
            plugins["mkdocs.plugins"]["simple-blog-posts"],
            "mkdocs_simple_blog.plugin:BlogPlugin",
        )

    def test_pyproject_version_matches_package(self) -> None:
        from mkdocs_simple_blog import __version__

        self.assertEqual(self.pyproject["project"]["version"], __version__)
