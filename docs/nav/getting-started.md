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

Set `site_url` so the 404 page links and assets resolve from any URL.
