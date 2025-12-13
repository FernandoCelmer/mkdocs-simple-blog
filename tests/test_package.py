"""Tests for package structure and metadata."""

from pathlib import Path


def test_package_init_exists():
    """Test that __init__.py exists."""
    package_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"
    init_file = package_dir / "__init__.py"

    assert init_file.exists(), "__init__.py should exist"


def test_package_version():
    """Test that package has a version defined."""
    from mkdocs_simple_blog import __version__

    assert __version__ is not None, "Package should have a version"
    assert isinstance(__version__, str), "Version should be a string"
    assert len(__version__) > 0, "Version should not be empty"


def test_package_author():
    """Test that package has an author defined."""
    from mkdocs_simple_blog import __author__

    assert __author__ is not None, "Package should have an author"
    assert isinstance(__author__, str), "Author should be a string"
    assert len(__author__) > 0, "Author should not be empty"


def test_package_structure():
    """Test that package has required structure."""
    package_dir = Path(__file__).parent.parent / "mkdocs_simple_blog"

    required_files = [
        "__init__.py",
        "base.html",
        "main.html",
        "search.html",
        "mkdocs_theme.yml",
    ]

    required_dirs = [
        "modules",
        "assets",
    ]

    for file_name in required_files:
        file_path = package_dir / file_name
        assert file_path.exists(), f"{file_name} should exist"

    for dir_name in required_dirs:
        dir_path = package_dir / dir_name
        assert dir_path.exists(), f"{dir_name} directory should exist"
        assert dir_path.is_dir(), f"{dir_name} should be a directory"
