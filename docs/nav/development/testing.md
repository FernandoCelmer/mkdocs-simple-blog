# Testing

Last updated December 13, 2024

---

## Overview

The mkdocs-simple-blog theme includes a comprehensive test suite to ensure code quality, functionality, and maintainability. All tests are written using [pytest](https://pytest.org/).

## Quick Start

### Install Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

## Test Structure

The test suite is organized into several modules:

### test_theme_config.py

Tests for theme configuration and metadata:

- Validates `mkdocs_theme.yml` exists and is valid YAML
- Checks default theme configuration values
- Verifies theme plugin registration in `pyproject.toml`

**Example:**

```python
def test_mkdocs_theme_yml_valid():
    """Test that mkdocs_theme.yml is valid YAML."""
    theme_dir = Path(__file__).parent.parent / 'mkdocs_simple_blog'
    theme_config = theme_dir / 'mkdocs_theme.yml'
    
    with open(theme_config, 'r') as f:
        config = yaml.safe_load(f)
    
    assert isinstance(config, dict)
```

### test_templates.py

Tests for Jinja2 template rendering:

- Verifies all template files exist (base.html, main.html, search.html)
- Tests template rendering with mock data
- Validates inclusion of Bootstrap, Highlight.js, and other dependencies
- Checks template inheritance (main.html extends base.html)

**Example:**

```python
def test_base_template_renders(template_env, mkdocs_config, mock_page):
    """Test that base.html template can be rendered."""
    template = template_env.get_template('base.html')
    html = template.render(**context)
    
    assert '<html' in html
    assert '<head' in html
    assert '<body' in html
```

### test_modules.py

Tests for theme module files:

- Verifies all required module files exist
- Validates HTML structure in modules
- Tests module loading as Jinja2 templates
- Checks module-specific structures (header, footer, sidebar)

**Example:**

```python
def test_required_modules_exist(modules_dir):
    """Test that all required module files exist."""
    required_modules = [
        'content.html',
        'header.html',
        'footer.html',
        # ... more modules
    ]
    
    for module in required_modules:
        assert (modules_dir / module).exists()
```

### test_assets.py

Tests for theme assets (CSS, JS, images):

- Verifies asset directories exist (css/, js/, img/)
- Checks required files are present
- Validates files are not empty
- Tests for favicon and logo

**Example:**

```python
def test_required_css_files_exist(assets_dir):
    """Test that required CSS files exist."""
    css_dir = assets_dir / 'css'
    required_css = [
        'bootstrap.min.css',
        'main.min.css',
        'root.min.css',
    ]
    
    for css_file in required_css:
        assert (css_dir / css_file).exists()
```

### test_package.py

Tests for package structure and metadata:

- Validates package structure
- Checks version and author metadata
- Verifies required files and directories

## Running Tests

### All Tests

```bash
pytest
```

### With Verbose Output

```bash
pytest -v
```

### Specific Test File

```bash
pytest tests/test_templates.py
```

### Specific Test Function

```bash
pytest tests/test_templates.py::test_base_template_renders
```

### With Coverage Report

```bash
pytest --cov=mkdocs_simple_blog --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

### Watch Mode (with pytest-watch)

```bash
pip install pytest-watch
ptw
```

## Test Fixtures

The test suite uses pytest fixtures defined in `tests/conftest.py`:

- `temp_dir`: Temporary directory for test files
- `mkdocs_config`: Minimal MkDocs configuration
- `mock_page`: Mock page object
- `theme_dir`: Path to theme directory
- `template_env`: Jinja2 environment for templates
- `modules_dir`: Path to modules directory
- `assets_dir`: Path to assets directory

## Writing New Tests

When adding new features, follow these guidelines:

1. **Create test files** following the naming convention: `test_*.py`
2. **Use descriptive test names**: `test_feature_name_behavior`
3. **Use fixtures** from `conftest.py` when possible
4. **Keep tests focused**: Each test should verify one specific behavior
5. **Add docstrings**: Document what each test verifies

**Example:**

```python
def test_new_feature_works(theme_dir):
    """Test that new feature works correctly."""
    feature_file = theme_dir / 'new_feature.html'
    
    assert feature_file.exists()
    # ... more assertions
```

## Continuous Integration

Tests are automatically run on:

- Every push to the repository
- Every pull request
- Scheduled runs (if configured)

See `.github/workflows/test.yml` for CI configuration.

## Test Coverage

Current test coverage includes:

- ✅ Theme configuration validation
- ✅ Template rendering
- ✅ Module structure
- ✅ Asset files
- ✅ Package metadata

## Troubleshooting

### Import Errors

If you encounter import errors, ensure all dependencies are installed:

```bash
pip install -e ".[dev]"
```

### Template Rendering Errors

Template tests require proper Jinja2 environment setup. The `template_env` fixture handles this automatically.

### Missing Files

If tests fail due to missing files, ensure you're running tests from the project root directory.

## Best Practices

1. **Run tests before committing**: `pytest`
2. **Maintain high coverage**: Aim for >80% coverage
3. **Fix failing tests immediately**: Don't commit broken tests
4. **Update tests with features**: Add tests for new functionality
5. **Keep tests fast**: Use mocks for slow operations

---

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

