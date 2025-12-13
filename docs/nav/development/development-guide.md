# Development guide

Last updated December 13, 2024

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

Tests are automatically run on every push and pull request via GitHub Actions. See `.github/workflows/test.yml` for the CI configuration.

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