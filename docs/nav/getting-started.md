## Installation MkDocs

To install MkDocs, run the following command from the command line:

```bash
pip install mkdocs
```

## Installation theme

Install the theme using PIP:

```bash
pip install mkdocs-simple-blog
```

## Activating theme

After the theme is installed, edit your `mkdocs.yml` file and set the theme name to `simple-blog`:

```yml
theme:
    name: simple-blog
```

## 404 page

The theme ships a `404.html` page. To replace it, create `overrides/404.html`
and point `custom_dir` to that folder:

```yml
theme:
    name: simple-blog
    custom_dir: overrides
```

```jinja
{% extends "base.html" %}

{% block content %}
<h1>Page not found</h1>
{% endblock %}
```

Set `site_url` when the site is served from a subpath (for example
`https://user.github.io/repo/`), so the 404 page links and assets resolve.

A static `docs/404.html` is replaced by the theme's 404 page. Move it to
`overrides/404.html` as shown above to keep it.

## Extra JavaScript

Scripts listed in `extra_javascript` load once, in `<head>`, before the page
content. That way inline `<script>` blocks in your pages can use them. Scripts
that touch the page or use the theme's jQuery/Bootstrap at load time should be
deferred, with MkDocs' per-script options:

```yml
extra_javascript:
  - js/plotly.min.js
  - path: js/my-widgets.js
    defer: true
  - path: js/app.mjs
    type: module
```
