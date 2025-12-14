# Highlightjs

January 28, 2025

---

## Enable and Disable

- Default: false

```yml
theme:
  highlightjs: false
```

## Highlightjs with languages

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

