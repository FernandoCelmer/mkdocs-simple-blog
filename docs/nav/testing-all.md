# Testing All

August 3, 2026

---

Reference page for manually checking that `pymdown-extensions` elements follow the theme (issue #70).

## Admonitions

!!! note "Note"
    Standard note admonition.

!!! warning "Warning"
    Something the reader should watch out for.

!!! tip "Tip"
    A helpful suggestion.

!!! danger "Danger"
    A destructive or high-risk action.

## Collapsible admonition (pymdownx.details)

??? info "Click to expand"
    Collapsed by default, uses `pymdownx.details`.

## Tabbed content

=== "Python"

    ```python
    print("hello")
    ```

=== "JavaScript"

    ```javascript
    console.log("hello");
    ```

## Footnotes

Static site generators skip the database entirely[^1].

[^1]: No runtime queries — everything is pre-rendered at build time.

## Task list

- [x] done
- [ ] pending

## Highlighted text (pymdownx.mark)

This is ==highlighted text==.

## Keys (pymdownx.keys)

Press ++ctrl+c++ to copy, ++cmd+v++ to paste.

## Emoji (pymdownx.emoji)

:tada: :rocket: :bug: :warning: :white_check_mark:

## Attribute lists / def_list

A paragraph with a custom class.
{: .example-class }

Term A
:   Definition for term A.
