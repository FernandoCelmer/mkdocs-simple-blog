"""Tests for extra_javascript rendering (issue #104)."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader

from .fixtures import THEME_DIR, mkdocs_config

SCRIPTS = ["assets/custom.js", "search/main.js"]
OPTIONED = [
    SimpleNamespace(path="js/dom.js", type="", defer=True, async_=False),
    SimpleNamespace(
        path="js/app.mjs", type="module", defer=False, async_=False
    ),
    SimpleNamespace(path="js/stats.js", type="", defer=False, async_=True),
]


def _render(scripts: list) -> str:
    env = Environment(loader=FileSystemLoader(str(THEME_DIR)), autoescape=True)
    env.filters["url"] = lambda path: path
    config_dict = mkdocs_config()
    config_dict["theme"] = type("Theme", (), config_dict["theme"])()
    config_dict["extra"] = {}
    config_dict["extra_javascript"] = scripts
    config_obj = type("Config", (), config_dict)()
    return env.get_template("base.html").render(
        config=config_obj,
        page=None,
        base_url=".",
        extra_css=[],
        extra_javascript=[str(getattr(s, "path", s)) for s in scripts],
    )


class ExtraJavascriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _render(SCRIPTS)

    def test_each_script_is_included_once(self) -> None:
        for path in SCRIPTS:
            self.assertEqual(self.html.count(f'src="{path}"'), 1, path)

    def test_scripts_load_blocking_in_head(self) -> None:
        head, body = self.html.split("</head>", 1)
        for path in SCRIPTS:
            self.assertIn(f'<script src="{path}"></script>', head)
            self.assertNotIn(path, body)

    def test_scripts_run_before_page_content(self) -> None:
        self.assertLess(
            self.html.index(SCRIPTS[0]),
            self.html.index('id="component-content"'),
        )


class ExtraJavascriptOptionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _render(OPTIONED)

    def test_defer_option_is_rendered(self) -> None:
        self.assertIn('<script src="js/dom.js" defer></script>', self.html)

    def test_type_option_is_rendered(self) -> None:
        self.assertIn(
            '<script src="js/app.mjs" type="module"></script>', self.html
        )

    def test_async_option_is_rendered(self) -> None:
        self.assertIn('<script src="js/stats.js" async></script>', self.html)


if __name__ == "__main__":
    unittest.main()
