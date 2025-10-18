# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based static site blog hosted on GitHub Pages at https://rikkisnah.github.io/. The site uses the Ananke theme as a Git submodule.

## Core Commands

### Development
```bash
# Start local development server with drafts
hugo server -D

# Start local development server (published content only)
hugo server

# Build the site (output to public/ directory)
hugo

# Build including draft content
hugo -D
```

### Content Management
```bash
# Create a new blog post
hugo new content/posts/post-name.md

# Create other content
hugo new content/section-name/page-name.md
```

### Theme Management
```bash
# Initialize/update the Ananke theme submodule
git submodule update --init --recursive

# The theme is currently at v2.12.1 which requires Hugo 0.128.0+
# If you have Hugo 0.128.0+ installed locally, you can update the theme:
cd themes/ananke && git fetch --tags && git checkout <tag-version>
```

## Architecture

### Site Structure
- `content/` - All site content in Markdown format
  - `content/posts/` - Blog posts
  - `content/_index.md` - Homepage content placeholder (not rendered)
- `themes/ananke/` - Ananke theme (Git submodule, do not modify directly)
- `hugo.toml` - Main site configuration
- `public/` - Generated static site (git-ignored, created by `hugo` build command)

### Configuration
The site configuration in `hugo.toml` includes:
- Theme: 'ananke'
- Base URL: https://rikkisnah.github.io/
- Language: en-us
- Title: 'Rik Kisnah - Blog'

### Content Front Matter
Blog posts should include front matter with at least:
```yaml
---
title: "Post Title"
date: YYYY-MM-DDTHH:MM:SS-07:00
draft: false
---
```

### Theme Customization
The Ananke theme is managed as a Git submodule. To customize:
- Create corresponding files in local `layouts/` directory to override theme layouts
- Create `static/` directory for custom static assets
- Never modify files directly in `themes/ananke/`

## Deployment

This site is deployed to GitHub Pages using GitHub Actions (`.github/workflows/hugo.yaml`).

**Workflow:**
1. Make content changes locally
2. Test locally with `hugo server -D`
3. Commit and push to `main` branch
4. GitHub Actions automatically builds and deploys the site
5. Site is live at https://rikkisnah.github.io/

**GitHub Actions builds with Hugo 0.128.0**, so the site will deploy successfully even if your local Hugo version is older.

### Important Note on Hugo Version

**Local Development:**
- The Ananke theme is at **v2.12.1** which requires **Hugo 0.128.0+**
- If your local Hugo version is older (e.g., 0.123.7), you won't be able to build locally
- You have two options:
  1. Upgrade Hugo locally: Download from https://github.com/gohugoio/hugo/releases
  2. Skip local builds and rely on GitHub Actions (which uses Hugo 0.128.0)

**GitHub Actions:**
- The workflow uses Hugo 0.128.0, so builds will succeed on GitHub regardless of your local version
- Simply push your changes and GitHub Actions will build and deploy automatically
