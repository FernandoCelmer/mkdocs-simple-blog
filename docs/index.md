# Home

February 4, 2025

---

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

```bash
mkdocs.yml    # The configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
```

## Installation MkDocs

To install MkDocs, run the following command from the command line:

```bash
pip install mkdocs
```

## Installation theme

### Using pip

Install the theme using pip:

```bash
pip install mkdocs-simple-blog
```

### Using Poetry

Install the theme using Poetry:

```bash
poetry add mkdocs-simple-blog
```

### Development Installation

Install from source for development:

```bash
git clone https://github.com/FernandoCelmer/mkdocs-simple-blog.git
cd mkdocs-simple-blog
pip install -e ".[dev]"
```

Or using Poetry:

```bash
git clone https://github.com/FernandoCelmer/mkdocs-simple-blog.git
cd mkdocs-simple-blog
poetry install --with dev
```

> **Note**: The `[dev]` extra includes development dependencies like pytest, pytest-cov, and pytest-mock for running tests.

> **Note**: For code quality tools (ruff, flake8, mypy), use `pip install -e ".[code-quality]"` or `poetry install --with code-quality`.

## Activating theme

After the theme is installed, edit your `mkdocs.yml` file and set the theme name to `simple-blog`:

```yml
theme:
    name: simple-blog
```

## CI/CD Status

This project uses GitHub Actions for continuous integration and deployment:

- 🧪 **Tests**: Automatically run on every push and pull request across Python 3.9-3.14
- 🔍 **Code Quality**: Ruff, Flake8, and MyPy checks ensure code standards
- 📦 **Publishing**: Automatic publishing to TestPyPI and PyPI with dependency checks

All workflows ensure that only tested and validated code is published.

## Getting Help

We use GitHub issues for tracking bugs and feature requests and have limited bandwidth to address them. If you need anything, I ask you to please follow our templates for opening issues or discussions.

- 🐛 [Bug Report](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/new/choose)
- 📕 [Documentation Issue](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/new/choose)
- 🚀 [Feature Request](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/new/choose)
- ⚠️ [Security Request](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/new/choose)
- 💬 [General Question](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/new/choose)

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
![GitHub License](https://img.shields.io/github/license/FernandoCelmer/mkdocs-simple-blog)

This project is licensed under the terms of the MIT License.
