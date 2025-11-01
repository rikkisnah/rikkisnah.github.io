# Rik Kisnah - Blog

A Hugo-based static site blog hosted on GitHub Pages at [https://rikkisnah.github.io/](https://rikkisnah.github.io/). The site uses the [hugo-paper](https://github.com/nanxiaobei/hugo-paper) theme as a Git submodule—a simple, clean, minimal theme perfect for blogging.

## Quick Start

### Prerequisites

**macOS:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Hugo
brew install hugo
```

**Ubuntu:**
```bash
# Install Hugo
sudo apt-get update
sudo apt-get install hugo
```

**Both platforms:**
- Git (usually pre-installed)
- Text editor (VS Code, vim, nano, etc.)

### Verify Installation

Check that Hugo is installed correctly:
```bash
hugo version
```

You should see version 0.57.1 or later. The hugo-paper theme requires Hugo 0.57.1+.

## Blog Structure

```
rikkisnah.github.io/
├── README.md                 # This file
├── CLAUDE.md                 # Claude Code instructions
├── hugo.toml                 # Site configuration
├── content/                  # All blog content
│   ├── _index.md            # Homepage content
│   ├── about.md             # About page
│   └── posts/               # Blog posts directory
│       ├── post-name-1.md
│       ├── post-name-2.md
│       └── ...
├── themes/
│   └── hugo-paper/          # Theme (Git submodule, don't modify)
├── static/                  # Custom static assets (css, js, images)
├── layouts/                 # Custom layout overrides
├── public/                  # Generated static site (git-ignored)
├── getall.sh                # Helper script to pull latest updates
└── saveall.sh               # Helper script to commit and deploy
```

## Creating Blog Posts

### 1. Create a New Post

```bash
hugo new content/posts/my-post-name.md
```

This creates a new file with the basic front matter template.

### 2. Edit Your Post

Open `content/posts/my-post-name.md` in your editor:

```markdown
---
title: "My Awesome Post"
date: 2025-10-19T14:30:00-07:00
draft: false
tags: ["tag1", "tag2", "tag3"]
---

## Your First Section

Your content here. You can use **bold**, *italic*, `code`, and more.

## Another Section

More content...
```

**Front matter fields:**
- `title`: Post title (required)
- `date`: Publication date in RFC3339 format (required)
- `draft`: Set to `false` to publish, `true` to keep as draft (required)
- `tags`: Array of tags for categorization (optional)

**Timezone hint:** Use `-07:00` (Pacific Time) to match the site's default timezone. Adjust as needed for your location.

### 3. Preview Your Work Locally

While writing, run the local development server:

**With draft posts (to see unpublished content):**
```bash
hugo server -D
```

**Without drafts (only published posts):**
```bash
hugo server
```

Visit `http://localhost:1313` in your browser to see your blog. The site auto-reloads as you edit—just save your file and refresh your browser.

### 4. Mark Draft as Complete

When you're ready to publish, edit the front matter and change `draft: false`:

```yaml
draft: false
```

## Deployment Workflow

### Option 1: Quick Deploy (Recommended)

Use the `saveall.sh` helper script:

```bash
./saveall.sh
```

This script:
1. Stages all your changes
2. Creates a commit with a summary of what changed
3. Pulls the latest from remote (in case of changes from another machine)
4. Pushes to GitHub
5. Triggers GitHub Actions to build and deploy

Your blog will be live at https://rikkisnah.github.io/ within 2-3 minutes.

### Option 2: Manual Deploy

```bash
# Stage your changes
git add -A

# Create a commit
git commit -m "Add new blog post about [topic]"

# Pull latest (safe merge only)
git pull --ff-only origin main

# Push to GitHub
git push origin main
```

GitHub Actions automatically builds and deploys after you push.

### Option 3: Local Build and Preview

Build the static site locally without deploying:

```bash
hugo
```

This generates the complete static site in the `public/` directory. Open `public/index.html` in your browser to preview.

## Pulling Latest Changes

If you work on multiple machines (work Mac and home Ubuntu), pull the latest changes before starting:

```bash
./getall.sh
```

This safely stashes any local uncommitted changes, pulls the latest from GitHub, and shows you what was updated.

## Helper Scripts

### `saveall.sh` - Commit and Deploy

```bash
./saveall.sh
```

Commits all changes with a summary and pushes to GitHub for deployment. Perfect for the end of your writing session.

**What it does:**
- Stages all changes
- Creates a commit message with file change summary
- Pulls latest updates safely
- Pushes to GitHub
- Triggers CI/CD pipeline

### `getall.sh` - Pull Latest

```bash
./getall.sh
```

Pulls the latest blog updates from GitHub, useful when switching between machines.

**What it does:**
- Stashes any uncommitted changes
- Pulls updates using fast-forward only (safe)
- Shows feedback on what was updated

## Common Workflows

### Complete Write-and-Deploy Cycle

```bash
# 1. Start fresh (pull any remote changes)
./getall.sh

# 2. Create a new post
hugo new content/posts/my-new-post.md

# 3. Edit your post
nano content/posts/my-new-post.md  # or use your editor

# 4. Preview locally
hugo server -D
# Visit http://localhost:1313 in your browser
# Keep this running while you edit

# 5. When satisfied, deploy
./saveall.sh

# That's it! Your blog is live.
```

### Working Across Machines

**On Machine A (e.g., work Mac):**
```bash
./getall.sh              # Pull latest
hugo new content/posts/my-post.md
# ... edit and preview ...
./saveall.sh             # Deploy
```

**On Machine B (e.g., home Ubuntu):**
```bash
./getall.sh              # Pull the post you just created
# ... make edits ...
./saveall.sh             # Deploy changes
```

### Drafting and Publishing Later

```bash
# Create a draft
hugo new content/posts/draft-post.md

# Edit with draft: true
# Work on it over time, preview with 'hugo server -D'

# When ready to publish
# Edit the file: change draft: false
./saveall.sh             # Deploy
```

## Site Configuration

The site configuration is in `hugo.toml`:

```toml
baseURL = "https://rikkisnah.github.io/"
languageCode = "en"
title = "Rik Kisnah - Blog"
theme = "hugo-paper"

[params]
author = "Rik Kisnah"
description = "..."
# ... more configuration
```

**Important:** Don't modify `theme = "hugo-paper"` or the theme submodule directly. The theme is managed as a Git submodule in `themes/hugo-paper/`.

## Customization

### Custom Styling

Create custom CSS in `static/custom.css` and reference it in the theme. The hugo-paper theme is minimal by design—if you need custom styling, add it here rather than modifying the theme.

### Custom Layouts

Override theme layouts by creating corresponding files in `layouts/`. For example:
- `layouts/partials/header.html` - overrides theme header
- `layouts/_default/single.html` - overrides post layout

### Adding Images to Posts

**Important:** Always organize post images in post-specific directories for better organization.

1. **Create the post-specific directory** (if it doesn't exist):
   ```bash
   mkdir -p static/posts/your-post-slug
   ```
   Note: The post slug matches your post filename (e.g., `the-circle-of-three.md` → `the-circle-of-three`)

2. **Place your images** in that directory:
   ```bash
   # Copy or move your image file
   cp /path/to/your-image.jpg static/posts/your-post-slug/your-image.jpg
   ```

3. **Reference them in your post** using the post-specific path:
   ```markdown
   ![Alt text](/posts/your-post-slug/your-image.jpg)
   ```

**Example workflow:**
```bash
# For a post named "my-awesome-post.md"
mkdir -p static/posts/my-awesome-post
cp ~/Pictures/photo.jpg static/posts/my-awesome-post/photo.jpg
```

Then in `content/posts/my-awesome-post.md`:
```markdown
![My Photo](/posts/my-awesome-post/photo.jpg)
```

**Common image formats:** `.jpg`, `.jpeg`, `.png`, `.gif`

**Tips:**
- Keep image filenames lowercase with hyphens (e.g., `family-photo.jpg`)
- Ensure file extensions match in your markdown reference
- Images in `static/posts/` are automatically copied to the final site during build

## Troubleshooting

### "command not found: hugo"

Make sure Hugo is installed:
- **macOS:** `brew install hugo`
- **Ubuntu:** `sudo apt-get install hugo`

### Port 1313 Already in Use

Hugo couldn't start the dev server because port 1313 is in use:
```bash
# Kill the existing process
lsof -i :1313
kill -9 <PID>

# Or use a different port
hugo server -D --port 1314
```

### Changes Not Appearing

- Make sure you changed `draft: false` in the front matter
- Run `hugo server` without `-D` to see only published posts
- Clear your browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)

### Git Push Fails

Make sure you've pulled latest first:
```bash
git pull --ff-only origin main
git push origin main
```

### Theme Not Loading

Initialize the theme submodule:
```bash
git submodule update --init --recursive
```

## GitHub Actions Deployment

The site is automatically deployed via GitHub Actions when you push to the `main` branch. The workflow (`.github/workflows/hugo.yaml`) handles:

- Building the site with Hugo 0.128.0 Extended
- Minifying CSS and JavaScript
- Garbage collection for optimal performance
- Deploying to GitHub Pages

**No action needed on your part**—just push and the site updates automatically within 2-3 minutes.

## Multi-Machine Development

This blog is designed for seamless development across machines:

**When switching machines:**
```bash
./getall.sh   # Pull latest from this machine
# ... make changes ...
./saveall.sh  # Deploy
```

**When working on multiple machines:**
- Always run `./getall.sh` before starting new work
- Always run `./saveall.sh` when done
- This prevents merge conflicts and keeps everything in sync

## Tips and Best Practices

- **Write often:** Keep posts concise and focused. Longer posts can be split into multiple related posts.
- **Use drafts:** Set `draft: true` while working, publish when ready.
- **Preview frequently:** Use `hugo server -D` to catch formatting issues early.
- **Commit often:** Small, focused commits make it easier to revert if needed.
- **Tag posts:** Use tags to help readers discover related content.
- **Dates matter:** Use accurate publication dates; they affect post ordering.

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo-Paper Theme](https://github.com/nanxiaobei/hugo-paper)
- [Markdown Syntax](https://www.markdownguide.org/)
- [GitHub Pages](https://pages.github.com/)

## License

This blog is open source. Feel free to fork, modify, and adapt for your own use.

---

**Questions or issues?** Check the troubleshooting section or review the `CLAUDE.md` file for technical details.
