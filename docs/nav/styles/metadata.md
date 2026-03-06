# Page Metadata

March 06, 2026

---

## Overview

The theme supports page metadata through MkDocs' built-in `page.meta` property. This allows you to add metadata to your Markdown files using YAML frontmatter, which will be automatically rendered as meta tags in the HTML head section. This is particularly useful for social media previews and SEO.

## Supported Metadata Fields

You can add the following metadata fields to your Markdown files:

- `title` - Custom page title for meta tags
- `description` - Page description for meta tags and social media previews
- `author` - Author of the page
- `date` - Publication date
- `image` - Image URL for social media previews

## Usage

Add YAML frontmatter to the top of your Markdown files:

```markdown
---
title: My Amazing Article
description: A detailed description of the article content
author: John Doe
date: 2025-01-15
image: assets/article-image.png
---

# Article Content

Your article content goes here...
```

## Social Media Integration

The theme automatically generates meta tags for:

### Open Graph (Facebook, LinkedIn)

- `og:title` - Article title
- `og:description` - Article description
- `og:image` - Preview image
- `og:url` - Canonical URL
- `og:type` - Set to "article"
- `og:site_name` - Site name from config

### Twitter Cards

- `twitter:title` - Article title
- `twitter:description` - Article description
- `twitter:image` - Preview image
- `twitter:card` - Set to "summary_large_image"

## Example

Here's a complete example of a Markdown file with metadata:

```markdown
---
title: Getting Started with MkDocs Simple Blog
description: Learn how to set up and customize the MkDocs Simple Blog theme for your documentation site
author: Fernando Celmer
date: 2025-01-15
image: assets/getting-started.png
---

# Getting Started

This guide will help you get started with the theme...
```

When this page is shared on social media, it will display a rich preview card with the title, description, and image you specified.

## Benefits

- **Better Social Media Previews**: Links shared on Facebook, Twitter, and LinkedIn will show rich previews with your custom title, description, and image
- **Improved SEO**: Search engines can better understand your content through structured metadata
- **Professional Appearance**: Your shared links will look more polished and professional
- **Easy to Use**: Simply add YAML frontmatter to your Markdown files - no additional configuration needed

## Notes

- All metadata fields are optional - only include the fields you need
- Image paths are relative to your `docs` directory
- The `date` field should be in ISO format (YYYY-MM-DD) for best compatibility
- If `description` is not provided, the theme will use the site description from `mkdocs.yml` for the homepage only
