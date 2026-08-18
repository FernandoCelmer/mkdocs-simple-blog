## Overview

Renders a "Created on DATE" / "— updated on DATE" line below the page title, sourced from front matter or straight from git history — no extra plugin required.

## Enable and Disable

- Default: true

```yml
theme:
  components:
    page_dates: true
```

<button component-id="component-page-dates" status="false"><code>true</code></button>
<button component-id="component-page-dates" status="true"><code>false</code></button>

## Date resolution order

For both the "created" and "updated" date, front matter always wins:

```yaml
---
date: 2024-01-05      # created
updated: 2024-06-15   # updated
---
```

- **`date`** / **`updated`** — optional, set directly in front matter
- Falls back to the file's git history when the matching field isn't set: first commit date for "created", last commit date for "updated". Shells out to plain `git log`, no extra plugin or dependency needed.
- If the file has no git history yet (untracked, uncommitted) or isn't inside a git repository at all (e.g. building from a source tarball), falls back to the build date — today's date, at the time the site is built.
- "Updated on" only renders when it differs from "Created on", so a page with a single commit doesn't show the same date twice.
