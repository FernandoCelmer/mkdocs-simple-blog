"""Tests for theme assets (CSS, JS, images)."""
import pytest


@pytest.fixture
def assets_dir(theme_dir):
    """Get assets directory."""
    return theme_dir / 'assets'


def test_assets_directory_exists(assets_dir):
    """Test that assets directory exists."""
    assert assets_dir.exists(), "assets directory should exist"
    assert assets_dir.is_dir(), "assets should be a directory"


def test_css_directory_exists(assets_dir):
    """Test that CSS directory exists."""
    css_dir = assets_dir / 'css'
    assert css_dir.exists(), "CSS directory should exist"
    assert css_dir.is_dir(), "CSS should be a directory"


def test_js_directory_exists(assets_dir):
    """Test that JS directory exists."""
    js_dir = assets_dir / 'js'
    assert js_dir.exists(), "JS directory should exist"
    assert js_dir.is_dir(), "JS should be a directory"


def test_img_directory_exists(assets_dir):
    """Test that img directory exists."""
    img_dir = assets_dir / 'img'
    assert img_dir.exists(), "img directory should exist"
    assert img_dir.is_dir(), "img should be a directory"


def test_required_css_files_exist(assets_dir):
    """Test that required CSS files exist."""
    css_dir = assets_dir / 'css'
    required_css = [
        'bootstrap.min.css',
        'main.min.css',
        'root.min.css',
        'media.min.css',
    ]
    
    for css_file in required_css:
        css_path = css_dir / css_file
        assert css_path.exists(), f"CSS file {css_file} should exist"


def test_required_js_files_exist(assets_dir):
    """Test that required JS files exist."""
    js_dir = assets_dir / 'js'
    required_js = [
        'bootstrap.bundle.min.js',
        'jquery-3.3.1.slim.min.js',
        'main.min.js',
    ]
    
    for js_file in required_js:
        js_path = js_dir / js_file
        assert js_path.exists(), f"JS file {js_file} should exist"


def test_favicon_exists(assets_dir):
    """Test that favicon exists."""
    img_dir = assets_dir / 'img'
    favicon = img_dir / 'favicon.ico'
    assert favicon.exists(), "favicon.ico should exist"


def test_logo_exists(assets_dir):
    """Test that logo exists."""
    img_dir = assets_dir / 'img'
    logo = img_dir / 'logo.png'
    assert logo.exists(), "logo.png should exist"


def test_css_files_not_empty(assets_dir):
    """Test that CSS files are not empty."""
    css_dir = assets_dir / 'css'
    css_files = list(css_dir.glob('*.css'))
    
    for css_file in css_files:
        assert css_file.stat().st_size > 0, f"{css_file.name} should not be empty"


def test_js_files_not_empty(assets_dir):
    """Test that JS files are not empty."""
    js_dir = assets_dir / 'js'
    js_files = list(js_dir.glob('*.js'))
    
    for js_file in js_files:
        assert js_file.stat().st_size > 0, f"{js_file.name} should not be empty"

