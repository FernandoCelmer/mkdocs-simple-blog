# Sidebar

January 28, 2025

---

## Overview

The sidebar displays the **Table of Contents (TOC)** of the current page, showing the page's heading structure. It does not display the site navigation (which appears in the top menu).

## How to activate?

- Default: false

### Configuration

Configure the sidebar in your `mkdocs.yml`:

```yml
theme:
  sidebar: false
```

<button id="sidebar-true"><code>true</code></button>
<button id="sidebar-false"><code>false</code></button>

## Navigation depth

The `navigation_depth` setting controls how many heading levels are displayed in the sidebar TOC.

- Default: 2

```yml
theme:
  navigation_depth: 2
```

This means headings up to level 2 (`##`) will be shown. For example:

- `# Heading 1` - Always shown
- `## Heading 2` - Shown (if navigation_depth >= 2)
- `### Heading 3` - Shown (if navigation_depth >= 3)
- `#### Heading 4` - Shown (if navigation_depth >= 4)

## How it works

The sidebar automatically generates a table of contents from the headings in your Markdown files. For the sidebar to display content:

1. **Your page must have headings** - Use `#`, `##`, `###`, etc. in your Markdown files
2. **The sidebar shows the current page's TOC** - It does not show site-wide navigation
3. **Site navigation appears in the top menu** - The `nav` section in `mkdocs.yml` controls the top menu, not the sidebar

## Example

If your Markdown file has:

```markdown
# Main Title

## Section 1
Content here...

### Subsection 1.1
More content...

## Section 2
More content...
```

With `navigation_depth: 2`, the sidebar will show:
- Main Title
  - Section 1
  - Section 2

With `navigation_depth: 3`, the sidebar will show:
- Main Title
  - Section 1
    - Subsection 1.1
  - Section 2

## Site Navigation vs Sidebar

- **Site Navigation** (`nav` in `mkdocs.yml`): Controls the top menu dropdown
- **Sidebar**: Shows the current page's table of contents (headings)

If you want to customize the site navigation, edit the `nav` section in your `mkdocs.yml` file. The sidebar is automatically generated from page headings.
