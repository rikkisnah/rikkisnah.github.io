# AGENTS.md

> **Dual-Tool Environment**: This repository uses both **Claude Code** and **Codex CLI** interchangeably.
> - `AGENTS.md` is the source instruction file
> - `CLAUDE.md` is a symlink to `AGENTS.md`
> - Both tools read their respective files but follow the same instructions

This file provides guidance to Claude Code (claude.ai/code) and Codex CLI when working with code in this repository.

## Project Overview

This is a Hugo-based static site blog hosted on GitHub Pages at https://www.rik-kisnah.ai/. The site uses the hugo-paper theme as a Git submodule. Hugo-paper is a simple, clean, minimal theme perfect for blogging.

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
- Base URL: https://www.rik-kisnah.ai/
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

### Hugo front matter: avoid YAML/Markdown mix-ups

Hugo treats everything between the **first** `---` and the **second** `---` as YAML. The Markdown body starts **after** that second delimiter.

- **Always close front matter with a second `---` on its own line.** If you omit it, Hugo keeps parsing the rest of the file as YAML. Lines that start with `*` are YAML **alias** syntax (not Markdown italics), which produces errors like `yaml: unknown anchor 'Disclaimer' referenced` when your disclaimer lines follow immediately after `tags:` with no closing delimiter.
- **Use YAML keys only in that block.** Write `title: "..."` as a normal key. Do **not** write `## title:` — `#` begins a YAML comment, so `title` may not be set, and `##` does not belong in front matter.
- **Place `*Disclaimer` / `*Caveat` lines only in the Markdown body**, after the closing `---`. Those lines intentionally start with `*` for italics; they must not appear inside the YAML block.

### Blog Post Disclaimer Requirement

Every blog post in `content/posts/` must include a disclaimer and caveat immediately after the lead image and before the main title/body.

Use this default pattern unless the user explicitly requests different wording:

```md
*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*
```

If a post has no lead image, place the disclaimer and caveat directly below the front matter.

### Blog Post Reading Metadata Requirement

Every blog post in `content/posts/` must include a single italic line with the body word count and estimated reading time. Place it **immediately below the lead image and above the disclaimer/caveat block** (or directly below the front matter when there is no lead image).

Format:

```md
*<word count> words · <minutes> min read*
```

Example:

```md
*1,658 words · 8 min read*
```

**How to compute the numbers:**

- **Word count:** Count only the article body. Exclude:
  - YAML front matter
  - The lead image line (`![...](...)`)
  - The reading-metadata line itself
  - The disclaimer, caveat, and image-credit italic lines
  - All heading lines (lines starting with `#`)
  - Everything from the `## References` heading onward (heading plus all reference entries)
- **Reading time:** `ceil(word_count / 200)` minutes (web-reading rate of ~200 wpm).
- **Formatting:** Use a thin-space-friendly middle dot (`·`, U+00B7) between the two values. Include a comma thousands separator for word counts ≥ 1,000.

**Quick shell snippet for the word count:**

```bash
awk '
/^## References/ {stop=1}
stop {next}
NR<=6 {next}
/^!\[/ {next}
/^\*[0-9]/ {next}
/^\*Disclaimer/ {next}
/^\*Caveat/ {next}
/^\*Image:/ {next}
/^## / {next}
{print}
' content/posts/<post>.md | wc -w
```

Adjust the `NR<=6` guard if the front matter is longer or shorter than six lines.

### Standard Top-of-Post Stack

Every new blog post should follow this exact order at the top, directly below the closing `---` of the front matter:

1. Lead image (`![...](/posts/<slug>/lead.png)`)
2. Reading metadata line (`*<count> words · <minutes> min read*`)
3. Disclaimer line (`*Disclaimer: ...*`)
4. Caveat line (`*Caveat: ...*`)
5. Image credit line when the lead image is AI-generated (`*Image: The illustration above was generated with <tool>.*`)
6. First section heading (`## ...`)

Separate each of the above with a single blank line.

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
5. Site is live at https://www.rik-kisnah.ai/ (usually within 2-3 minutes)

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

## Preventing Common Deployment Issues

### Critical Files (Never Delete or Modify)

These files are **essential** for GitHub Pages to work correctly with Hugo:

```
.nojekyll              # CRITICAL: Disables Jekyll processing
_config.yml            # CRITICAL: GitHub Pages configuration
.github/workflows/hugo.yaml  # CI/CD workflow
```

**Why:** Without `.nojekyll` and `_config.yml`, GitHub Pages defaults to Jekyll processing instead of serving your Hugo-generated static files, breaking the entire site.

### Theme Submodule Protection

**NEVER modify files in `themes/hugo-paper/` directly.** This breaks Git submodule tracking.

**Correct way to customize:**
```bash
# ✅ DO: Override theme files in local layouts/
layouts/partials/head.html      # Overrides theme's head partial
layouts/partials/footer.html    # Overrides theme's footer partial

# ✅ DO: Add custom CSS to static/
static/custom.css               # Custom styles (included in head.html)
static/css/theme-overrides.css  # Additional theme overrides

# ❌ DON'T: Modify theme files directly
themes/hugo-paper/assets/main.css           # NEVER EDIT
themes/hugo-paper/layouts/partials/...      # NEVER EDIT
```

**If you accidentally modify the theme:**
```bash
# Reset the theme submodule to clean state
cd themes/hugo-paper
git checkout .                  # Reset all changes
git clean -fd                   # Remove untracked files
cd ../..

# Verify it's clean
git status                      # Should show clean working tree
```

### Pre-deployment Checklist

Before running `./saveall.sh`, verify:

```bash
# 1. Check for uncommitted theme changes
git status
# ✅ GOOD: No changes in themes/hugo-paper/
# ❌ BAD: "modified: themes/hugo-paper" → fix with git checkout

# 2. Verify critical files exist
ls -la .nojekyll _config.yml .github/workflows/hugo.yaml
# All three must exist and be committed

# 3. Test local build with GitHub Actions flags
hugo --gc --minify --buildFuture
# Should complete without errors

# 4. Verify no broken image links
# Check that static/posts/[post-slug]/ directories exist
# and images are referenced correctly in markdown
```

### Local Build vs GitHub Build

**Always test locally first to catch issues early:**

```bash
# Test with exact GitHub Actions settings
hugo --gc --minify --buildFuture

# Or use the development server to preview
hugo server -D
# Visit http://localhost:1313 to verify
```

**Key differences between local and GitHub:**
- Local: Hugo 0.123.7+ (current version)
- GitHub: Hugo 0.128.0 Extended (fixed version in workflow)
- Local: Runs with your timezone
- GitHub: Always uses America/Los_Angeles timezone

If build succeeds locally but fails on GitHub:
1. Check GitHub Actions logs: https://github.com/rikkisnah/rikkisnah.github.io/actions
2. Look for Hugo version mismatches or missing dependencies
3. Verify all content files have proper front matter

### GitHub Pages Configuration

**Current working setup:**
- `.nojekyll` - Signals GitHub Pages to skip Jekyll
- `_config.yml` - Minimal config (just `future: true`)
- `.github/workflows/hugo.yaml` - Builds and deploys to Pages

**Never:**
- Delete `.nojekyll` or `_config.yml`
- Change GitHub Pages source to "Branch: main" (must be "GitHub Actions")
- Use the GitHub Pages API to update custom domains unless `build_type=workflow` is preserved. A plain Pages API update can silently switch the site to legacy branch deployment, which may serve unstyled or stale Hugo output.
- Commit the `public/` directory (it's git-ignored for a reason)

### Deployment Recovery

**If site goes down or shows wrong content:**

1. **Check current status:**
   ```bash
   curl -s https://rikkisnah.github.io/ | grep -o 'generator.*>'
   # Should show: Hugo 0.128.0
   # If shows: Jekyll v3... then GitHub is processing with Jekyll (wrong!)
   ```

2. **Verify critical files exist:**
   ```bash
   git log --oneline -1 -- .nojekyll _config.yml
   # Both should appear in recent commits
   ```

3. **Force GitHub Actions rebuild:**
   ```bash
   git commit --allow-empty -m "Force rebuild"
   git push
   # GitHub Actions will rebuild the site
   ```

4. **Last resort - full reset:**
   ```bash
   # Push a commit that ensures critical files are present
   git add .nojekyll _config.yml
   git commit -m "Restore critical GitHub Pages configuration"
   git push
   ```
