## Overview

Three widgets built from the same post collection [Blog List](blog-list.md) reads: **Recent Posts**, **Categories**, and **Tags**. Each is toggled independently. Requires the `simple-blog-posts` plugin.

Unlike the [Sidebar](sidebar.md) (which shows the current page's table of contents), the Blog Sidebar shows data aggregated across every post.

## How to activate?

- Default: false — each widget is off unless listed

### Configuration

```yml
plugins:
  - search
  - simple-blog-posts

theme:
  name: simple-blog
  components:
    blog_sidebar:
      recent_posts: true
      categories: true
      tags: true
      recent_count: 5
```

<button component-id="component-blog-sidebar" status="false"><code>true</code></button>
<button component-id="component-blog-sidebar" status="true"><code>false</code></button>

## Widgets

- **`recent_posts`** — links the `recent_count` most recent posts (default `5`)
- **`categories`** — one link per distinct `category` value
- **`tags`** — one link per distinct tag

Any widget can be omitted or set to `false` to hide it independently of the others.

## Categories and tags link to real listing pages

Clicking a category or tag doesn't just jump to "some post that has it" — the plugin generates an actual page per value (e.g. `category/python/`, `tag/django/`) that renders **only the posts carrying that category or tag**, using the same [Blog List](blog-list.md) layout as everywhere else. See [Category and tag pages](blog-list.md#category-and-tag-pages) for how these are generated and configured.

## Coexistence with the Table of Contents sidebar

Setting `theme.components.blog_sidebar` puts the theme into its two-column layout (same one used by `theme.sidebar: true`) even if `theme.sidebar` itself is left at its default `false`. If both are enabled, the page's table of contents renders above the blog widgets in the same sidebar column.

## Data source

Both this component and [Blog List](blog-list.md) read from the same collection built by the `simple-blog-posts` plugin — see its [front matter contract](blog-list.md#front-matter-contract).
