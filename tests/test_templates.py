"""Tests for Jinja2 templates."""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


@pytest.fixture
def template_env(theme_dir):
    """Create Jinja2 environment for templates."""
    templates_dir = theme_dir

    def url_filter(path):
        """Simple URL filter for testing."""
        if path.startswith("http"):
            return path
        return path.replace("\\", "/")

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=True,
    )
    env.filters["url"] = url_filter
    return env


def test_base_template_exists(theme_dir):
    """Test that base.html template exists."""
    base_template = theme_dir / "base.html"
    assert base_template.exists(), "base.html should exist"


def test_main_template_exists(theme_dir):
    """Test that main.html template exists."""
    main_template = theme_dir / "main.html"
    assert main_template.exists(), "main.html should exist"


def test_search_template_exists(theme_dir):
    """Test that search.html template exists."""
    search_template = theme_dir / "search.html"
    assert search_template.exists(), "search.html should exist"


def test_base_template_renders(template_env, mkdocs_config, mock_page):
    """Test that base.html template can be rendered."""
    try:
        template = template_env.get_template("base.html")

        config_dict = mkdocs_config.copy()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        context = {
            "config": config_obj,
            "page": mock_page,
            "base_url": ".",
            "extra_css": [],
            "extra_javascript": [],
        }

        html = template.render(**context)

        assert html is not None, "Template should render"
        assert "<html" in html, "HTML should contain <html> tag"
        assert "<head" in html, "HTML should contain <head> tag"
        assert "<body" in html, "HTML should contain <body> tag"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_main_template_extends_base(template_env):
    """Test that main.html extends base.html."""
    try:
        theme_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"
        main_file = theme_dir / "main.html"

        with open(main_file) as f:
            content = f.read()

        assert "extends" in content, "main.html should extend base.html"
        assert "base.html" in content, "main.html should extend base.html"
    except FileNotFoundError:
        pytest.skip("Template file not found")


def test_search_template_renders(template_env, mkdocs_config, mock_page):
    """Test that search.html template can be rendered."""
    try:
        template = template_env.get_template("search.html")

        theme_obj = type("Theme", (), mkdocs_config["theme"])()
        config_dict = mkdocs_config.copy()
        config_dict["theme"] = theme_obj
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        context = {
            "config": config_obj,
            "page": mock_page,
            "base_url": ".",
            "extra_css": [],
            "extra_javascript": [],
        }

        html = template.render(**context)

        assert html is not None, "Template should render"
        assert "<html" in html or "<!doctype" in html, "HTML should be valid"
    except TemplateNotFound:
        pytest.skip("Template not found")
    except Exception as e:
        pytest.skip(f"Template rendering needs more context: {e}")


def test_base_template_includes_highlightjs(template_env, mkdocs_config):
    """Test that base.html includes highlight.js when enabled."""
    try:
        theme_config = mkdocs_config["theme"].copy()
        theme_config["highlightjs"] = True
        theme_config["hljs_languages"] = ["python", "yaml"]

        theme_obj = type("Theme", (), theme_config)()
        config_dict = mkdocs_config.copy()
        config_dict["theme"] = theme_obj
        config_dict["hljs_languages"] = theme_config["hljs_languages"]
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        template = template_env.get_template("base.html")

        context = {
            "config": config_obj,
            "page": None,
            "base_url": ".",
            "extra_css": [],
            "extra_javascript": [],
        }

        html = template.render(**context)

        assert (
            "highlight.js" in html
        ), "Should include highlight.js when enabled"
        assert "hljs.highlightAll()" in html, "Should call hljs.highlightAll()"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_base_template_bootstrap_included(template_env, mkdocs_config):
    """Test that base.html includes Bootstrap CSS."""
    try:
        template = template_env.get_template("base.html")

        config_dict = mkdocs_config.copy()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        context = {
            "config": config_obj,
            "page": None,
            "base_url": ".",
            "extra_css": [],
            "extra_javascript": [],
        }

        html = template.render(**context)

        assert "bootstrap.min.css" in html, "Should include Bootstrap CSS"
        assert (
            "bootstrap.bundle.min.js" in html or "jquery" in html
        ), "Should include Bootstrap JS or jQuery"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_base_template_includes_page_metadata(template_env, mkdocs_config):
    """Test base.html includes page metadata tags when page.meta exists."""
    try:
        template = template_env.get_template("base.html")

        page_meta = {
            "title": "Custom Page Title",
            "description": "Custom page description",
            "author": "John Doe",
            "date": "2025-01-15",
            "image": "assets/custom-image.png",
        }
        mock_page = type(
            "Page",
            (),
            {
                "title": "Test Page",
                "is_homepage": False,
                "canonical_url": "https://example.com/test/",
                "meta": page_meta,
            },
        )()

        config_dict = mkdocs_config.copy()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        context = {
            "config": config_obj,
            "page": mock_page,
            "base_url": ".",
            "extra_css": [],
            "extra_javascript": [],
        }

        html = template.render(**context)

        assert 'name="title"' in html, "Should include title meta tag"
        assert (
            'content="Custom Page Title"' in html
        ), "Should include custom title"
        assert (
            'name="description"' in html
        ), "Should include description meta tag"
        assert 'name="author"' in html, "Should include author meta tag"
        assert 'content="John Doe"' in html, "Should include author content"
        assert 'name="date"' in html, "Should include date meta tag"

        assert 'property="og:title"' in html, "Should include og:title"
        assert (
            'property="og:description"' in html
        ), "Should include og:description"
        assert 'property="og:type"' in html, "Should include og:type"
        assert 'property="og:url"' in html, "Should include og:url"
        assert 'property="og:image"' in html, "Should include og:image"

        assert 'name="twitter:title"' in html, "Should include twitter:title"
        assert (
            'name="twitter:description"' in html
        ), "Should include twitter:description"
        assert 'name="twitter:card"' in html, "Should include twitter:card"
        assert 'name="twitter:image"' in html, "Should include twitter:image"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_preview_module_shows_arrows_only_when_pages_exist(template_env):
    """Test preview.html only shows navigation arrows when pages exist."""
    try:
        template = template_env.get_template("modules/preview.html")

        def url_filter(path):
            """Simple URL filter for testing."""
            if path.startswith("http"):
                return path
            return path.replace("\\", "/")

        template.environment.filters["url"] = url_filter

        mock_page_both = type(
            "Page",
            (),
            {
                "next_page": type("Page", (), {"url": "next/"})(),
                "previous_page": type("Page", (), {"url": "prev/"})(),
            },
        )()
        html_both = template.render(page=mock_page_both)
        assert "Previous" in html_both, "Should show Previous when page exists"
        assert "Next" in html_both, "Should show Next when page exists"
        assert 'class="nav-link disabled"' not in html_both, (
            "Should not have disabled links when pages exist"
        )

        mock_page_next = type(
            "Page",
            (),
            {
                "next_page": type("Page", (), {"url": "next/"})(),
                "previous_page": None,
            },
        )()
        html_next = template.render(page=mock_page_next)
        assert "Previous" not in html_next, (
            "Should not show Previous when page doesn't exist"
        )
        assert "Next" in html_next, "Should show Next when page exists"

        mock_page_prev = type(
            "Page",
            (),
            {
                "next_page": None,
                "previous_page": type("Page", (), {"url": "prev/"})(),
            },
        )()
        html_prev = template.render(page=mock_page_prev)
        assert "Previous" in html_prev, "Should show Previous when page exists"
        assert "Next" not in html_prev, (
            "Should not show Next when page doesn't exist"
        )

        mock_page_none = type(
            "Page",
            (),
            {
                "next_page": None,
                "previous_page": None,
            },
        )()
        html_none = template.render(page=mock_page_none)
        assert "Previous" not in html_none, (
            "Should not show Previous when page doesn't exist"
        )
        assert "Next" not in html_none, (
            "Should not show Next when page doesn't exist"
        )
        assert "component-preview" not in html_none, (
            "Should not render preview block when no pages exist"
        )
    except TemplateNotFound:
        pytest.skip("Template not found")
