"""Tests for theme configuration."""

from pathlib import Path

import yaml


def test_mkdocs_theme_yml_exists():
    """Test that mkdocs_theme.yml exists."""
    theme_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"
    theme_config = theme_dir / "mkdocs_theme.yml"

    assert theme_config.exists(), "mkdocs_theme.yml should exist"


def test_mkdocs_theme_yml_valid():
    """Test that mkdocs_theme.yml is valid YAML."""
    theme_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"
    theme_config = theme_dir / "mkdocs_theme.yml"

    with open(theme_config) as f:
        config = yaml.safe_load(f)

    assert isinstance(config, dict), "mkdocs_theme.yml should be a dictionary"
    assert "theme" in config, "mkdocs_theme.yml should have 'theme' key"


def test_theme_default_config():
    """Test default theme configuration values."""
    theme_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"
    theme_config = theme_dir / "mkdocs_theme.yml"

    with open(theme_config) as f:
        config = yaml.safe_load(f)

    theme = config.get("theme", {})

    assert "sidebar" in theme, "theme should have 'sidebar' key"
    assert "navigation_depth" in theme, (
        "theme should have 'navigation_depth' key"
    )
    assert "highlightjs" in theme, "theme should have 'highlightjs' key"
    assert "hljs_languages" in theme, "theme should have 'hljs_languages' key"


def test_theme_plugin_registration():
    """Test that theme is registered as a plugin."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"

    assert pyproject.exists(), "pyproject.toml should exist"

    with open(pyproject) as f:
        content = f.read()

    assert "mkdocs.themes" in content, (
        "Should have mkdocs.themes plugin configuration"
    )
    assert "simple-blog" in content, (
        "Theme should be registered as 'simple-blog'"
    )
    assert "mkdocs_simple_blog" in content, (
        "Theme should point to 'mkdocs_simple_blog' package"
    )
