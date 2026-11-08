## Changing the fonts

### Site name style

- Default: normal

```yml
theme:
  site_name_style: normal
```

<button style-site-name="normal">
    <code class="normal style-swatch">normal</code>
</button>
<button style-site-name="bold">
    <code class="bold style-swatch">bold</code>
</button>
<button style-site-name="italic">
    <code class="italic style-swatch">italic</code>
</button>
<button style-site-name="scratched">
    <code class="scratched style-swatch">scratched</code>
</button>
<button style-site-name="underline">
    <code class="underline style-swatch">underline</code>
</button>
<button style-site-name="overline">
    <code class="overline style-swatch">overline</code>
</button>

### Title style

- Default: bold

```yml
theme:
  title_style: bold
```

<button style-title="normal">
    <code class="normal style-swatch">normal</code>
</button>
<button style-title="bold">
    <code class="bold style-swatch">bold</code>
</button>
<button style-title="italic">
    <code class="italic style-swatch">italic</code>
</button>
<button style-title="scratched">
    <code class="scratched style-swatch">scratched</code>
</button>
<button style-title="underline">
    <code class="underline style-swatch">underline</code>
</button>
<button style-title="overline">
    <code class="overline style-swatch">overline</code>
</button>

## Remote fonts and icons

By default the theme loads Fira Mono from Google Fonts and FontAwesome 4.7
from cdnjs. Highlight.js, when enabled, is loaded from cdnjs and unpkg.

- Default: true

```yml
theme:
  remote_assets: true
```

Set `remote_assets: false` to stop every request to these third-party
servers. Text falls back to the browser's `monospace` font, FontAwesome
icons are not rendered and Highlight.js is skipped even if `highlightjs`
is `true`.

```yml
theme:
  remote_assets: false
```

### Serving your own copies

The font and icon stylesheets live in their own `fonts` and `icons`
template blocks, so you can replace them without copying the rest of the
theme. Put the files under `docs/` and override the blocks from a
`custom_dir`:

```yml
theme:
  name: simple-blog
  custom_dir: overrides
```

```jinja
{# overrides/main.html #}
{% extends "base.html" %}

{% block fonts %}
<link rel="stylesheet" href="{{ 'assets/fonts/fira-mono.css'|url }}">
{% endblock %}

{% block icons %}
<link rel="stylesheet" href="{{ 'assets/font-awesome/css/font-awesome.min.css'|url }}">
{% endblock %}
```
