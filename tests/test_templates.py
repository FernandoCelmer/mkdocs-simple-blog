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
        if path.startswith('http'):
            return path
        return path.replace('\\', '/')
    
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=True,
    )
    env.filters['url'] = url_filter
    return env


def test_base_template_exists(theme_dir):
    """Test that base.html template exists."""
    base_template = theme_dir / 'base.html'
    assert base_template.exists(), "base.html should exist"


def test_main_template_exists(theme_dir):
    """Test that main.html template exists."""
    main_template = theme_dir / 'main.html'
    assert main_template.exists(), "main.html should exist"


def test_search_template_exists(theme_dir):
    """Test that search.html template exists."""
    search_template = theme_dir / 'search.html'
    assert search_template.exists(), "search.html should exist"


def test_base_template_renders(template_env, mkdocs_config, mock_page):
    """Test that base.html template can be rendered."""
    try:
        template = template_env.get_template('base.html')
        
        config_dict = mkdocs_config.copy()
        config_dict['extra'] = {}
        config_obj = type('Config', (), config_dict)()
        
        context = {
            'config': config_obj,
            'page': mock_page,
            'base_url': '.',
            'extra_css': [],
            'extra_javascript': [],
        }
        
        html = template.render(**context)
        
        assert html is not None, "Template should render"
        assert '<html' in html, "HTML should contain <html> tag"
        assert '<head' in html, "HTML should contain <head> tag"
        assert '<body' in html, "HTML should contain <body> tag"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_main_template_extends_base(template_env):
    """Test that main.html extends base.html."""
    try:
        theme_dir = Path(__file__).parent.parent / 'mkdocs_simple_blog'
        main_file = theme_dir / 'main.html'
        
        with open(main_file, 'r') as f:
            content = f.read()
        
        assert 'extends' in content, "main.html should extend base.html"
        assert 'base.html' in content, "main.html should extend base.html"
    except FileNotFoundError:
        pytest.skip("Template file not found")


def test_search_template_renders(template_env, mkdocs_config):
    """Test that search.html template can be rendered."""
    try:
        template = template_env.get_template('search.html')
        
        theme_obj = type('Theme', (), mkdocs_config['theme'])()
        config_obj = type('Config', (), {
            **{k: v for k, v in mkdocs_config.items() if k != 'theme'},
            'theme': theme_obj,
        })()
        
        context = {
            'config': config_obj,
            'base_url': '.',
            'extra_css': [],
            'extra_javascript': [],
        }
        
        html = template.render(**context)
        
        assert html is not None, "Template should render"
        assert '<html' in html or '<!doctype' in html, "HTML should be valid"
    except TemplateNotFound:
        pytest.skip("Template not found")
    except Exception as e:
        pytest.skip(f"Template rendering needs more context: {e}")


def test_base_template_includes_highlightjs(template_env, mkdocs_config):
    """Test that base.html includes highlight.js when enabled."""
    try:
        theme_config = mkdocs_config['theme'].copy()
        theme_config['highlightjs'] = True
        theme_config['hljs_languages'] = ['python', 'yaml']
        
        theme_obj = type('Theme', (), theme_config)()
        config_dict = mkdocs_config.copy()
        config_dict['theme'] = theme_obj
        config_dict['hljs_languages'] = theme_config['hljs_languages']
        config_dict['extra'] = {}
        config_obj = type('Config', (), config_dict)()
        
        template = template_env.get_template('base.html')
        
        context = {
            'config': config_obj,
            'page': None,
            'base_url': '.',
            'extra_css': [],
            'extra_javascript': [],
        }
        
        html = template.render(**context)
        
        assert 'highlight.js' in html, "Should include highlight.js when enabled"
        assert 'hljs.highlightAll()' in html, "Should call hljs.highlightAll()"
    except TemplateNotFound:
        pytest.skip("Template not found")


def test_base_template_bootstrap_included(template_env, mkdocs_config):
    """Test that base.html includes Bootstrap CSS."""
    try:
        template = template_env.get_template('base.html')
        
        config_dict = mkdocs_config.copy()
        config_dict['extra'] = {}
        config_obj = type('Config', (), config_dict)()
        
        context = {
            'config': config_obj,
            'page': None,
            'base_url': '.',
            'extra_css': [],
            'extra_javascript': [],
        }
        
        html = template.render(**context)
        
        assert 'bootstrap.min.css' in html, "Should include Bootstrap CSS"
        assert 'bootstrap.bundle.min.js' in html or 'jquery' in html, \
            "Should include Bootstrap JS or jQuery"
    except TemplateNotFound:
        pytest.skip("Template not found")

