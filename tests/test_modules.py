"""Tests for theme modules."""

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def modules_dir(theme_dir):
    """Get modules directory."""
    return theme_dir / "modules"


def test_modules_directory_exists(modules_dir):
    """Test that modules directory exists."""
    assert modules_dir.exists(), "modules directory should exist"
    assert modules_dir.is_dir(), "modules should be a directory"


def test_required_modules_exist(modules_dir):
    """Test that all required module files exist."""
    required_modules = [
        "content.html",
        "copyright.html",
        "dropdown-menu.html",
        "footer.html",
        "head_extra_links.html",
        "header.html",
        "menu.html",
        "preview.html",
        "search.html",
        "searchbox.html",
        "sidebar.html",
        "source.html",
    ]

    for module in required_modules:
        module_path = modules_dir / module
        assert module_path.exists(), f"Module {module} should exist"


def test_modules_are_valid_html(modules_dir):
    """Test that module files contain valid HTML structure."""
    modules = list(modules_dir.glob("*.html"))

    empty_modules_allowed = ["head_extra_links.html"]

    for module_path in modules:
        with open(module_path) as f:
            content = f.read()

        if module_path.name in empty_modules_allowed:
            continue

        assert len(content) > 0, f"{module_path.name} should not be empty"
        assert (
            "{" in content or "<" in content
        ), f"{module_path.name} should contain HTML or Jinja2 syntax"


def test_modules_can_be_loaded(modules_dir):
    """Test that modules can be loaded as Jinja2 templates."""
    env = Environment(
        loader=FileSystemLoader(str(modules_dir)),
        autoescape=True,
    )

    modules = list(modules_dir.glob("*.html"))

    for module_path in modules:
        try:
            template = env.get_template(module_path.name)
            assert (
                template is not None
            ), f"Should be able to load {module_path.name}"
        except Exception as e:
            pytest.fail(f"Failed to load {module_path.name}: {e}")


def test_header_module_structure(modules_dir):
    """Test that header.html has expected structure."""
    header_path = modules_dir / "header.html"

    if header_path.exists():
        with open(header_path) as f:
            content = f.read()

        assert (
            "nav" in content.lower() or "navbar" in content.lower()
        ), "header.html should contain navigation elements"


def test_footer_module_structure(modules_dir):
    """Test that footer.html has expected structure."""
    footer_path = modules_dir / "footer.html"

    if footer_path.exists():
        with open(footer_path) as f:
            content = f.read()

        assert (
            "footer" in content.lower() or "copyright" in content.lower()
        ), "footer.html should contain footer elements"


def test_sidebar_module_structure(modules_dir):
    """Test that sidebar.html has expected structure."""
    sidebar_path = modules_dir / "sidebar.html"

    if sidebar_path.exists():
        with open(sidebar_path) as f:
            content = f.read()

        assert (
            "nav" in content.lower()
            or "sidebar" in content.lower()
            or "menu" in content.lower()
        ), "sidebar.html should contain navigation elements"
