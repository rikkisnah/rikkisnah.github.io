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
The hugo-paper theme is managed as a Git submodule. To customize:
- Create corresponding files in local `layouts/` directory to override theme layouts
- Create `static/` directory for custom static assets
- Never modify files directly in `themes/hugo-paper/`

## Deployment & Workflow

This site is deployed to GitHub Pages using GitHub Actions (`.github/workflows/hugo.yaml`).

### Manual Deployment
Two helper scripts simplify the workflow:

- **`saveall.sh`** - Commit and deploy changes
  - Stages all changes, creates commit with summary
  - Pulls latest from remote and pushes to GitHub
  - Triggers GitHub Actions build and deployment
  - Usage: `./saveall.sh`

- **`getall.sh`** - Pull latest updates
  - Stashes local changes safely
  - Pulls updates with fast-forward only (safe merge)
  - Usage: `./getall.sh`

### Standard Deployment Workflow
1. Make content changes locally
2. Test locally with `hugo server -D` (view at http://localhost:1313)
3. Run `./saveall.sh` to commit and deploy
4. GitHub Actions automatically builds and deploys the site
5. Site is live at https://rikkisnah.github.io/ (usually within 2-3 minutes)

### Hugo Version Compatibility

**Local Development:**
- Hugo-paper theme requires **Hugo 0.57.1+**
- Any Hugo version 0.57.1 or later works for local development
- Build locally: `hugo` (output to `public/`)
- Preview locally: `hugo server -D` then visit http://localhost:1313

**GitHub Actions (CI/CD):**
- The workflow uses Hugo 0.128.0 Extended with Dart Sass
- Builds are minified and garbage-collected for optimal site performance
- Timezone: America/Los_Angeles (affects date rendering)
- All builds push to https://rikkisnah.github.io/
