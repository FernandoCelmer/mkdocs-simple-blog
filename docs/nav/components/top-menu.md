## Enable and Disable

- Default: true

```yml
theme:
  components:
    menu: true
```

<button component-id="component-menu" status="false"><code>true</code></button>
<button component-id="component-menu" status="true"><code>false</code></button>

## Search button

The search icon in the top menu is shown only when the `search` plugin is
enabled and `include_search_page` is not `false`, since it submits to
`search.html`:

```yml
plugins:
  - search

theme:
  include_search_page: true
```
