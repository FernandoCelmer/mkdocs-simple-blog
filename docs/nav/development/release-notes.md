## v0.6.2

- [📦 PyPI - Build 0.6.2](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.6.2)
- [⚙️ `remote_assets` option to stop loading Google Fonts, FontAwesome and Highlight.js from CDNs, with overridable `fonts`/`icons` blocks](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/100)
- [🪲 `theme.hljs_languages` now injects the Highlight.js language scripts (the template read the wrong config key)](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/102)
- [🪲 `theme.colors` now apply with `theme_style: light`; `dark` keeps its own palette. Sites that set both will now see their colors](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/103)
- [🪲 `extra_javascript` entries load once, blocking in `<head>`, instead of twice (head + deferred body copy)](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/104)
- [⚙️ Built-in `404.html` page, registered as a static template so `custom_dir` overrides render too. A static `docs/404.html` is now replaced; move it to `overrides/404.html`](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/105)
- [🪲 `theme.extra_css` alias paths resolve on nested pages and no longer duplicate top-level `extra_css` entries](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/106)
- [🪲 Fix 2-6px horizontal scroll on mobile caused by `.row` gutters inside the reduced-padding container](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/107)
- [🪲 Fix duplicate `id="component-content"` with the sidebar layout. The layout column is now `#component-main`; update custom CSS/JS that targeted the column through `#component-content`](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/108)
- [🪲 `<html lang>` follows `theme.locale` (`pt_BR` → `pt-BR`), `data-bs-theme` defaults to `light`, and the unused `language` default is replaced by `locale`](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/109)
- [🪲 `remote_assets: false` no longer loads shields.io badges, and the header search icon falls back to an inline SVG so search stays reachable](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/110)
- [📦 Remove stale `setup.py` and `MANIFEST.in`; `pyproject.toml` is the only build config](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/111)
- [🪲 Header search is shown only when the `search` plugin is enabled and `include_search_page` is not `false`, instead of linking to a 404 or a missing search box](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/112)

## v0.6.1

- [📦 PyPI - Build 0.6.1](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.6.1)
- [🪲 Fix crash on any page with a date front matter field when simple-blog-posts isn't installed](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/96)

## v0.6.0

- [📦 PyPI - Build 0.6.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.6.0)
- [🪲 Fix page-dates divider duplicating blog_list's first-item border on pages with empty body content](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/92)
- [⚠️ Fix Dependabot security alerts: pymdown-extensions, pytest -- drops Python 3.9 support (no 3.9-compatible patched release exists for either)](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/94)

## v0.5.0

- [📦 PyPI - Build 0.5.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.5.0)
- [⚙️ Blog post-list component: `blog_list`/`blog_sidebar`, featured/compact layouts, category and tag listing pages, author/avatar resolution from front matter or git history, drops `mkdocs-git-revision-date-localized-plugin` in favor of `babel`](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/82)
- [🪲 Fix generic `a:hover` rule overriding hover color/underline on componentized links (buttons, pills, tags)](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/84)
- [⚙️ Native `page_dates` component (Created on / Updated on) sourced from git history, locale-aware via `theme.locale` and babel, plus a fix for `mkdocs_theme.yml` defaults being silently ignored due to a nested `theme:` key](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/85)

## v0.4.3

- [📦 PyPI - Build 0.4.3](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.4.3)
- [🪲 Code blocks stay dark in dark theme; accept theme.extra_css alias](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/66)
- [⚠️ Fix Dependabot security alerts: black, pytest, Pygments](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/74)
- [⚙️ Style pymdown-extensions elements with theme CSS](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/70)

## v0.4.2

- [📦 PyPI - Build 0.4.2](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.4.2)
- [🪲 Code and Preformatted Text Blocks don't respect theming + extra_css does not work](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/66)
- [🪲 Custom theme.colors never apply due to broken Jinja syntax](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/68)

## v0.4.1

- [📦 PyPI - Build 0.4.1](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.4.1)
- [📌 next & previous arrows not clickable](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/33)

## v0.4.0

- [📦 PyPI - Build 0.4.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.4.0)
- [📌 Documentation for editing sidebar](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/52)
- [📌 Add page metadata from builtin page.meta property inside template](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/53)
- [🪲 BUG: Fix top menu dropdown not working on internal pages](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/961605217bf0d06b12413e12362bccb8bc005f10)

## v0.3.0

- [📦 PyPI - Build 0.3.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.3.0)
- [📌 Extendable head section in base.html](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/49)
- [📌 Issue/50](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/50)
- [📌 Issue/51](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/51)
- [⚙️ FEATURE: Create reusable GitHub Actions for workflows](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/b4951f5)
- [⚙️ FEATURE: Add jinja2 and code quality dependencies](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/0b512c4)
- [❤️️ TEST: Add comprehensive unit test suite](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/462dd25)
- [⬆️ CI/CD: Refactor workflows to use reusable actions](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/7edd691)
- [⬆️ CI/CD: Automate version update on release](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/035ee96)
- [⬆️ CI/CD: Simplify publish workflow](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/59cf3f7)
- [📝 PEP8: Add code quality configuration files](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/c26dc5d)
- [📘 DOCS: Update documentation with CI/CD and testing information](https://github.com/FernandoCelmer/mkdocs-simple-blog/commit/3e8cbe7)

## v0.2.0

- [📦 PyPI - Build 0.2.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.2.0)
- [📌 great product love it but](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/47)
- [📌 Mobile First Sidebar](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/45)

## v0.1.0

- [📦 PyPI - Build 0.1.0](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.1)
- [📌 [Feature Request] Simple code syntax highlighting](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/35)
- [📌 Software license update](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/39)
- [📌 Is there a sidebar in this theme?](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/23)

## v0.0.9

- [📦 PyPI - Build 0.0.9](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.9)
- [📌 ISSUE-27 - Minify CSS and JS](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/27)
- [📌 ISSUE-26 - Code indentation error](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/26)

## v0.0.8

- [📦 PyPI - Build 0.0.8](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.8)
- [📌 ISSUE-22 - Search](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/22)


## v0.0.7

- [📦 PyPI - Build 0.0.7](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.7)
- [📌 ISSUE-21 - Fix the extra_javascript include in base.html](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/21)


## v0.0.6

- [📦 PyPI - Build 0.0.6](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.6)
- [📌 ISSUE-16 - Include option to add and remove components](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/16)


## v0.0.5

- [📦 PyPI - Build 0.0.5](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.5)
- [📌 ISSUE-13 - Inclusion option to preview next and previous post](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/13)
- [📌 ISSUE-7 - Add additional theme settings](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/7)
- [📌 ISSUE-5 - Adjust blog interface for mobile devices](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/5)
- [📌 ISSUE-2 - Create dark mode and other color options](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/2)

## v0.0.4

- [📦 PyPI - Build 0.0.4](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.4)
- [📌 ISSUE-1 - Create custom menu](https://github.com/FernandoCelmer/mkdocs-simple-blog/issues/1)

## v0.0.3

- [📦 PyPI - Build 0.0.3](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.3)

## v0.0.2

- [📦 PyPI - Build 0.0.2](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.2)

## v0.0.1

- [📦 PyPI - Build 0.0.1](https://github.com/FernandoCelmer/mkdocs-simple-blog/releases/tag/v0.0.1)
