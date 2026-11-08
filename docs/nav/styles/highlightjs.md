## Enable and Disable

- Default: false

```yml
theme:
  highlightjs: false
```

## Highlight.js with languages

```yml
theme:
  highlightjs: true
  hljs_languages:
    - yaml
    - python
```

## Supported Languages

The theme supports syntax highlighting for multiple languages. Currently configured:

- **YAML**: For configuration files
- **Python**: For code examples and scripts

To add more languages, add them to the `hljs_languages` list in `mkdocs.yml`.

## Remote loading

Highlight.js is loaded from cdnjs and unpkg. Setting
`remote_assets: false` disables it, see [Fonts](fonts.md#remote-fonts-and-icons).
