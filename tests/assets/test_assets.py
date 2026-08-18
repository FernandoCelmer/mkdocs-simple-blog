"""Tests for theme assets (CSS, JS, images)."""

from __future__ import annotations

import unittest

from ..fixtures import THEME_DIR

ASSETS_DIR = THEME_DIR / "assets"


class AssetsDirectoryTests(unittest.TestCase):
    def test_assets_directory_exists(self) -> None:
        self.assertTrue(ASSETS_DIR.exists())
        self.assertTrue(ASSETS_DIR.is_dir())

    def test_css_directory_exists(self) -> None:
        css_dir = ASSETS_DIR / "css"
        self.assertTrue(css_dir.exists())
        self.assertTrue(css_dir.is_dir())

    def test_js_directory_exists(self) -> None:
        js_dir = ASSETS_DIR / "js"
        self.assertTrue(js_dir.exists())
        self.assertTrue(js_dir.is_dir())

    def test_img_directory_exists(self) -> None:
        img_dir = ASSETS_DIR / "img"
        self.assertTrue(img_dir.exists())
        self.assertTrue(img_dir.is_dir())


class RequiredAssetFilesTests(unittest.TestCase):
    def test_required_css_files_exist(self) -> None:
        css_dir = ASSETS_DIR / "css"
        required_css = [
            "bootstrap.min.css",
            "main.min.css",
            "root.min.css",
            "media.min.css",
        ]
        for css_file in required_css:
            with self.subTest(css_file=css_file):
                self.assertTrue((css_dir / css_file).exists())

    def test_required_js_files_exist(self) -> None:
        js_dir = ASSETS_DIR / "js"
        required_js = [
            "bootstrap.bundle.min.js",
            "jquery-3.3.1.slim.min.js",
            "main.min.js",
        ]
        for js_file in required_js:
            with self.subTest(js_file=js_file):
                self.assertTrue((js_dir / js_file).exists())

    def test_favicon_exists(self) -> None:
        self.assertTrue((ASSETS_DIR / "img" / "favicon.ico").exists())

    def test_logo_exists(self) -> None:
        self.assertTrue((ASSETS_DIR / "img" / "logo.png").exists())


class AssetFileContentTests(unittest.TestCase):
    def test_css_files_not_empty(self) -> None:
        css_dir = ASSETS_DIR / "css"
        for css_file in css_dir.glob("*.css"):
            with self.subTest(css_file=css_file.name):
                self.assertGreater(css_file.stat().st_size, 0)

    def test_js_files_not_empty(self) -> None:
        js_dir = ASSETS_DIR / "js"
        for js_file in js_dir.glob("*.js"):
            with self.subTest(js_file=js_file.name):
                self.assertGreater(js_file.stat().st_size, 0)
