---

## Overview

Renders every post under `docs/post/` as a card (thumbnail, author avatar, title, date, category, description, "Read more" link), sorted by date descending. Requires the `simple-blog-posts` plugin — it scans front matter and builds the collection this component reads.

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
author: Fernando Celmer
github: FernandoCelmer
description: Why saying a simple 'hi' still matters.
image: assets/yes-hello-cover.png
---
```

- `title`, `date` — required
- `category` — optional, used by [Blog Sidebar](blog-sidebar.md)
- `tags` — optional list, used by [Blog Sidebar](blog-sidebar.md)
- `author` — optional, shown in the card's meta line
- `github` — optional GitHub username; when set, the card shows the author's GitHub avatar (`https://github.com/{username}.png`) next to the title. No API call, no token needed — GitHub serves that path directly for any username.
- `avatar` — optional direct image URL, for any provider that isn't GitHub (GitLab, Bitbucket, Gravatar, a custom CDN, ...). GitLab and Bitbucket don't have a stable "avatar by username" URL the way GitHub does, so there's no equivalent shortcut field for them — paste the direct URL instead. Takes priority over `github` when both are set.
- `description` — optional excerpt shown below the meta line. This is the same field already used for the page's SEO `<meta name="description">` (see [Page Metadata](../styles/metadata.md)) — one field, two uses.
- `image` — optional thumbnail, path relative to `docs/` (e.g. `assets/cover.png`). Also reused as the page's `og:image`/`twitter:image` if set (see [Page Metadata](../styles/metadata.md)).

## Where it renders

`blog_list` renders inside `modules/content.html`, after the page body — so `index.md` can still have its own intro text above the auto-generated card list.

## `theme.blog` config

All blog-wide settings live under one `theme.blog` block instead of separate top-level keys:

```yml
theme:
  blog:
    layout: featured        # or: compact -- default: featured
    author: Fernando Celmer # site-wide default author
    github: FernandoCelmer  # site-wide default GitHub username
    avatar: ""              # site-wide default avatar URL (any provider)
    cta_label: Continue Reading
```

- **`layout`** — `featured` is a WordPress-style card: centered title, centered "Published on DATE — in CATEGORY — by AUTHOR" meta line, large centered thumbnail (700×320), left-aligned description, full-width black CTA button. `compact` is a dense row: small 200×130 thumbnail beside the content, avatar next to the title, one-line meta, inline CTA button — better when a page lists many posts. Both read the exact same post data; switching doesn't require touching front matter.
- **`author`** / **`github`** — used for any post whose own front matter doesn't set `author`/`github`. A post's own front matter always wins when present, so a guest post can still override the site default.
- **`cta_label`** — text on the "Read more" button (defaults differ per layout: "Continue Reading" for `featured`, "Read more" for `compact`).

## Custom posts directory

- Default: `post`

```yml
plugins:
  - simple-blog-posts:
      posts_dir: articles
```

Scans `docs/articles/**/*.md` instead of `docs/post/**/*.md`.
