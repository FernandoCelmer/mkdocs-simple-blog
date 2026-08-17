# Blog List

August 17, 2026

---

## Overview

Renders every post under `docs/post/` as a card (title, date, category, "Read more" link), sorted by date descending. Requires the `simple-blog-posts` plugin — it scans front matter and builds the collection this component reads.

## How to activate?

- Default: false

### Configuration

```yml
plugins:
  - search
  - simple-blog-posts

theme:
  name: simple-blog
  components:
    blog_list: true
```

<button component-id="component-blog-list" status="false"><code>true</code></button>
<button component-id="component-blog-list" status="true"><code>false</code></button>

## Front matter contract

Only files under `docs/post/` with both `title` and `date` are collected. Everything else in `docs/post/` is skipped — a post missing `date`, or a non-post file that happens to live in that directory, is not an error.

```yaml
---
title: Yes Hello!
date: 2023-12-17
category: Geral
tags: [pessoal]
---
```

- `title`, `date` — required
- `category` — optional, used by [Blog Sidebar](blog-sidebar.md)
- `tags` — optional list, used by [Blog Sidebar](blog-sidebar.md)

## Where it renders

`blog_list` renders inside `modules/content.html`, after the page body — so `index.md` can still have its own intro text above the auto-generated card list.

## Custom posts directory

- Default: `post`

```yml
plugins:
  - simple-blog-posts:
      posts_dir: articles
```

Scans `docs/articles/**/*.md` instead of `docs/post/**/*.md`.
