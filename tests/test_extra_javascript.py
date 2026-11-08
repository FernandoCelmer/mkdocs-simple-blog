"""Tests for extra_javascript rendering (issue #104)."""

from __future__ import annotations

import unittest

from jinja2 import Environment, FileSystemLoader

from .fixtures import THEME_DIR, mkdocs_config

SCRIPTS = ["assets/custom.js", "search/main.js"]


def _render() -> str:
    env = Environment(loader=FileSystemLoader(str(THEME_DIR)), autoescape=True)
    env.filters["url"] = lambda path: path
    config_dict = mkdocs_config()
    config_dict["theme"] = type("Theme", (), config_dict["theme"])()
    config_dict["extra"] = {}
    config_obj = type("Config", (), config_dict)()
    return env.get_template("base.html").render(
        config=config_obj,
        page=None,
        base_url=".",
        extra_css=[],
        extra_javascript=SCRIPTS,
    )


class ExtraJavascriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _render()

    def test_each_script_is_included_once(self) -> None:
        for path in SCRIPTS:
            self.assertEqual(self.html.count(f'src="{path}"'), 1, path)

    def test_scripts_are_deferred_in_body(self) -> None:
        head, body = self.html.split("</head>", 1)
        for path in SCRIPTS:
            self.assertNotIn(path, head)
            self.assertIn(f'<script src="{path}" defer></script>', body)

    def test_scripts_load_after_theme_bundle(self) -> None:
        self.assertLess(
            self.html.index("bootstrap.bundle.min.js"),
            self.html.index(SCRIPTS[0]),
        )


if __name__ == "__main__":
    unittest.main()
