"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mkdocs_config():
    """Create a minimal MkDocs config for testing."""
    config = {
        "site_name": "Test Site",
        "site_url": "https://example.com",
        "site_description": "Test Description",
        "site_author": "Test Author",
        "theme": {
            "name": "simple-blog",
            "favicon": "assets/favicon.ico",
            "logo": "assets/logo.png",
            "theme_style": "light",
            "site_name_style": "bold",
            "title_style": "bold",
            "sidebar": True,
            "navigation_depth": 2,
            "highlightjs": False,
            "hljs_languages": [],
            "colors": {
                "text": "black",
                "title": "black",
                "primary": "black",
                "background": "white",
            },
            "components": {
                "site_name": True,
                "title": False,
                "menu": True,
                "preview": True,
                "footer": True,
            },
        },
        "extra_css": [],
        "extra_javascript": [],
        "nav": [
            {"Home": "index.md"},
        ],
    }
    return config


@pytest.fixture
def mock_page():
    """Create a mock page object."""
    page = type(
        "Page",
        (),
        {
            "title": "Test Page",
            "is_homepage": False,
            "canonical_url": "https://example.com/test/",
            "content": "# Test Page\n\nThis is a test page.",
            "url": "test/",
            "abs_url": "https://example.com/test/",
        },
    )()
    return page


@pytest.fixture
def theme_dir():
    """Get the theme directory path."""
    return Path(__file__).parent.parent / "mkdocs_simple_blog"
