---
title: Writing Front Matter for Posts
description: What title, date, category and tags do, and what happens when they're missing.
date: 2026-08-10
image: assets/home-page.png
category: Guides
tags:
  - front-matter
  - guides
---

## The contract

Only two fields are required for a file under `docs/post/` to be
picked up by the `simple-blog-posts` plugin:

```yaml
---
title: My Post
date: 2024-06-03
---
```

`category` and `tags` are optional — they only affect whether the post
shows up in the Blog Sidebar's Categories and Tags widgets.

## What happens if title or date is missing

Nothing breaks. The file still builds as a normal page; it's just
excluded from `blog_posts`, `blog_categories`, and `blog_tags`. This
lets non-post files (an `about.md`, an `index.md`) live alongside real
posts under the same directory without special-casing them.
