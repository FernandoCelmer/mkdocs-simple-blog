---
title: Styling the Blog List and Sidebar
description: The CSS classes behind blog_list and blog_sidebar, for anyone overriding the look.
date: 2026-08-17
image: assets/blog-list-compact.png
category: Guides
tags:
  - styling
  - css
---

## Blog List classes

Each card rendered by `blog_list` is:

```html
<article class="blog-list-item">
  <h2 class="blog-list-item-title"><a href="...">Title</a></h2>
  <p class="blog-list-item-meta">Date · Category</p>
  <a class="blog-list-item-cta" href="...">Read more →</a>
</article>
```

## Blog Sidebar classes

Each widget is a `.blog-sidebar-widget` with a `.blog-sidebar-widget-title`
header, followed by either a `.blog-sidebar-list` (Recent Posts,
Categories) or a `.blog-sidebar-tags` flex container of
`.blog-sidebar-tag` pills (Tags).

## Overriding via extra_css

None of these classes need `!important` to override from a consuming
site's `extra_css` — they're loaded before `extra_css` in `base.html`,
so normal cascade order wins.
