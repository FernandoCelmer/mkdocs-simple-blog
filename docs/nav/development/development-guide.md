# Development guide

Last updated February 4, 2025

---

## How to test the local package?

#### Virtual environment

- Create your virtual environment.

```bash
python -m venv venv
```

#### Environment activation

- Activate the virtual environment.

```bash
source venv/bin/activate
```

#### Install the requirements

- Install the necessary requirements to be able to test the application.

```bash
pip install -r requirements.txt --no-cache-dir
```

#### Development

- Make your changes as desired in the `./mkdocs_simple_blog` folder. You can enjoy and change whatever you want, please have fun.

```bash
ls mkdocs_simple_blog
```

#### Build and Install

- Run the script that creates and installs the local package.


```bash
python scripts/install_local.py
```

#### Test

- Run the following command to run the server.

```bash
mkdocs serve
```

#### View Template

- Now you can access the [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Running Unit Tests

The project includes a comprehensive test suite to ensure code quality and functionality.

### Install Test Dependencies

First, install the development dependencies:

```bash
pip install -e ".[dev]"
```

Or using poetry:

```bash
poetry install
```

### Run All Tests

Execute all tests with:

```bash
pytest
```

### Run Tests with Coverage

Generate a coverage report:

```bash
pytest --cov=mkdocs_simple_blog --cov-report=html
```

The HTML coverage report will be available in `htmlcov/index.html`.

### Run Specific Tests

You can run specific test files or individual tests:

```bash
# Run only template tests
pytest tests/test_templates.py

# Run only configuration tests
pytest tests/test_theme_config.py

# Run a specific test
pytest tests/test_templates.py::test_base_template_renders
```

### Test Structure

The test suite is organized into the following modules:

- **test_theme_config.py**: Tests for theme configuration and YAML files
- **test_templates.py**: Tests for Jinja2 template rendering
- **test_modules.py**: Tests for theme module files
- **test_assets.py**: Tests for CSS, JS, and image assets
- **test_package.py**: Tests for package structure and metadata

### Verbose Output

For more detailed output, use the `-v` flag:

```bash
pytest -v
```

### Continuous Integration

Tests are automatically run on every push and pull request via GitHub Actions. The CI pipeline:

- Runs tests on Python versions 3.9 through 3.14
- Generates coverage reports
- Executes on pushes to `main`, `develop`, `master`, and `pypi` branches
- Can be triggered manually via `workflow_dispatch`

See `.github/workflows/test.yml` for the CI configuration.

---

## Code Quality

The project uses several code quality tools to maintain high standards:

### Tools

- **Ruff**: Fast Python linter and formatter
- **Flake8**: Style guide enforcement (PEP 8)
- **MyPy**: Static type checking

### Running Code Quality Checks Locally

Install code quality dependencies:

```bash
poetry install --with code-quality
```

Or using pip:

```bash
pip install -e ".[code-quality]"
```

### Ruff (Linting and Formatting)

Check for linting issues:

```bash
ruff check --config=.code_quality/ruff.toml mkdocs_simple_blog/ tests/
```

Format code:

```bash
ruff format --config=.code_quality/ruff.toml mkdocs_simple_blog/ tests/
```

### Flake8

Run Flake8 checks:

```bash
flake8 --config=.code_quality/.flake8 mkdocs_simple_blog/ tests/
```

### MyPy (Type Checking)

Run type checking:

```bash
mypy --config-file=.code_quality/mypy.ini mkdocs_simple_blog/ tests/
```

### Code Quality in CI/CD

Code quality checks are automatically run:

- On every push and pull request
- For Python versions 3.9 through 3.14
- Before package publication

See `.github/workflows/code-quality.yml` for the CI configuration.

### Configuration Files

All code quality configurations are in the `.code_quality/` directory:

- `.code_quality/ruff.toml` - Ruff configuration
- `.code_quality/.flake8` - Flake8 configuration
- `.code_quality/mypy.ini` - MyPy configuration

---

## Publishing

### Publishing to TestPyPI

The package is automatically published to TestPyPI when changes are pushed to the `pypi` branch. The publishing workflow:

1. Runs all tests (Python 3.9-3.14)
2. Runs code quality checks
3. Builds the package
4. Publishes to TestPyPI

See `.github/workflows/python-publish-pypi-test.yml` for the configuration.

### Publishing to PyPI

The package is automatically published to PyPI when a new release is published on GitHub. The publishing workflow:

1. Runs all tests (Python 3.9-3.14)
2. Runs code quality checks
3. Builds the package
4. Publishes to PyPI

See `.github/workflows/python-publish-pypi.yml` for the configuration.

### Manual Publishing

To publish manually:

```bash
# Build the package
python -m build

# Publish to TestPyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

---

## Commit Style

- ⚙️ FEATURE
- 📝 PEP8
- 📌 ISSUE
- 🪲 BUG
- 📘 DOCS
- 📦 PyPI
- ❤️️ TEST
- ⬆️ CI/CD
- ⚠️ SECURITY

## License

![GitHub](https://img.shields.io/github/license/FernandoCelmer/mkdocs-simple-blog?style=flat-square)

This project is licensed under the terms of the MIT license.
