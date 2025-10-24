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
- Params: Author name, bio, color scheme, social links (LinkedIn, GitHub)

### Navigation Menu
The main navigation menu is configured in `hugo.toml` and currently includes:
- Posts (`/posts/`) - Blog post listing
- About (`/about/`) - About page
- Publications (`/publications/`) - Featured publications and talks
- Resume (`/resume/`) - Resume/CV page

To add or modify menu items, edit the `[menu]` section in `hugo.toml`:
```toml
[menu]
  [[menu.main]]
    identifier = "page-id"
    name = "Display Name"
    url = "/path/"
    weight = 10  # Lower weight = appears first
```

### Content Front Matter
Blog posts should include front matter with at least:
```yaml
---
title: "Post Title"
date: YYYY-MM-DDTHH:MM:SS-07:00
draft: false
tags: ["tag1", "tag2"]
---
```

**Front Matter Fields:**
- `title`: Post title (required)
- `date`: Publication date in RFC3339 format with `-07:00` timezone (required)
- `draft`: Set to `false` to publish, `true` to keep as draft (required)
- `tags`: Array of tags for categorization (optional)

**Important:** Always use `-07:00` (Pacific Time) for dates to match the site's default timezone.

### Static Assets and Images
Images and other static assets should be organized in the `static/` directory:
- `static/posts/[post-slug]/` - Images for specific blog posts (organized by post filename)
- Reference images in posts using: `![Alt text](/posts/post-slug/image-name.jpg)`
- Example: For post `content/posts/my-post.md`, place images in `static/posts/my-post/`

This keeps post content and related images organized together while leveraging Hugo's static asset handling.

### Theme Customization
The hugo-paper theme is managed as a Git submodule. To customize:
- Create corresponding files in local `layouts/` directory to override theme layouts
- Create custom CSS in `static/custom.css` for styling overrides
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
- Build environment: Ubuntu latest
- Hugo version: 0.128.0 Extended
- CSS preprocessing: Dart Sass
- Build flags: `--gc` (garbage collection), `--minify` (minification)
- Timezone: America/Los_Angeles (affects date rendering)
- Deployment: Automatic push to GitHub Pages on every main branch push
- Build workflow file: `.github/workflows/hugo.yaml`

The workflow automatically handles:
- Checking out code with Git submodules
- Installing Hugo and dependencies
- Building with production settings
- Uploading artifacts to GitHub Pages
- All builds are live within 2-3 minutes
