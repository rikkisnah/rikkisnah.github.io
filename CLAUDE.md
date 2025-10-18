# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based static site blog hosted on GitHub Pages at https://rikkisnah.github.io/. The site uses the hugo-paper theme as a Git submodule. Hugo-paper is a simple, clean, minimal theme perfect for blogging.

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
# Initialize/update the hugo-paper theme submodule
git submodule update --init --recursive

# The theme is hugo-paper which requires Hugo 0.57.1+
# Update theme to latest version:
cd themes/hugo-paper && git fetch --tags && git checkout main && git pull
```

## Architecture

### Site Structure
- `content/` - All site content in Markdown format
  - `content/posts/` - Blog posts
  - `content/_index.md` - Homepage content
- `themes/hugo-paper/` - Hugo-paper theme (Git submodule, do not modify directly)
- `hugo.toml` - Main site configuration
- `public/` - Generated static site (git-ignored, created by `hugo` build command)
- `saveall.sh` - Script for committing and deploying changes

### Configuration
The site configuration in `hugo.toml` includes:
- Theme: 'hugo-paper' (simple, clean, minimal blogging theme)
- Base URL: https://rikkisnah.github.io/
- Language: en
- Title: 'Rik Kisnah - Blog'
- Menu: Posts and About pages
- Params: Author name, bio, color scheme

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

### Hugo Version Compatibility

**Local Development:**
- Hugo-paper theme requires **Hugo 0.57.1+**
- Your local Hugo 0.123.7 is fully compatible
- You can build locally with `hugo` or `hugo server -D`
- Test locally: `hugo server` then visit http://localhost:1313

**GitHub Actions:**
- The workflow uses Hugo 0.128.0 Extended
- Builds will succeed on GitHub and push to https://rikkisnah.github.io/
