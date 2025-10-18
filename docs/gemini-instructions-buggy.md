-----

## 🚀 Hugo Blog Deployment Master Guide

This guide ensures your local environment is correct, your Hugo files are properly configured, and your deployment is automated via GitHub Actions.

### Prerequisites

| Item | Command / Status | Notes |
| :--- | :--- | :--- |
| **Hugo (Extended)** | Installed via Snap: `sudo snap install hugo` | Confirmed as the correct, modern installation method for Ubuntu. |
| **Git** | Installed and Initialized | Assumed installed and set up for user `rikkisnah`. |
| **Repository** | **`rikkisnah.github.io`** | Must be named **exactly** to serve as your personal user site URL. |

-----

## Stage 1: Correct Project Configuration & Files

This stage ensures all file-related errors encountered previously are fixed in your local project.

### 1\. Configure the Site Files

In your project root (`rikkisnah.github.io/`), ensure these files exist and are correct:

| File | Content / Command | Action Taken in Chat |
| :--- | :--- | :--- |
| **`hugo.toml`** | Set to your URL and one theme line. | **Fixed:** Manually removed duplicate `theme = 'ananke'` line that caused a config error. |
| **`content/`** | The main content directory. | **Fixed:** Directory was missing and manually created (`mkdir content`). |
| **`themes/ananke`** | Theme files. | Installed via `git submodule add...` |

### 2\. Correct Front Matter Syntax

The syntax error (`failed to unmarshal YAML... expected ':'`) was due to mixing YAML delimiters (`---`) with TOML syntax (`=`).

**Action:** Open your post file (`content/posts/my-first-post.md`) and ensure the front matter uses the correct **YAML** syntax (colon and space).

**Example Correct Front Matter:**

```yaml
---
title: "My First Post"
date: 2024-10-18T00:00:00-07:00
draft: false  # <-- CORRECT: Colon and space (YAML syntax)
---
```

### 3\. Create the Homepage File

To fix the issue where the page only showed "Rik," the site needs an explicit homepage file.

**Command:**

```bash
# Must be run from the project root: /mnt/data/src/rikkisnah/rikkisnah.github.io
hugo new content _index.md
```

**Action:** Open `content/_index.md` and set **`draft: false`**.

-----

## Stage 2: Automated Deployment Setup (The Workflow)

This uses the modern, automated GitHub Actions approach to build and deploy your static site.

### 1\. The GitHub Actions Workflow

Ensure the file **`.github/workflows/hugo.yaml`** exists in your repository with the following content:

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - main 
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Install Hugo CLI
        run: |
          HUGO_VERSION=$(curl -s https://api.github.com/repos/gohugoio/hugo/releases/latest | grep '"tag_name"' | cut -d ':' -f 2 | tr -d '",v ' | cut -d '.' -f 1-3)
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Build with Hugo
        env:
          HUGO_ENV: production
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

-----

## Stage 3: Final Clean-Up and Deployment Workflow

Use this final script to automate your build, commit, and push process, eliminating the need to type multiple commands.

### 1\. Final Deployment Script (`deploy.sh`)

Create a file named **`deploy.sh`** in your project root and make it executable (`chmod +x deploy.sh`):

```bash
#!/bin/bash

# --- Hugo/Git Deployment Script for GitHub Pages ---

# 1. Configuration Variables
# ---------------------------------------------------------------------
SOURCE_BRANCH="main" 
REMOTE_NAME="origin" 

# 2. Get Commit Message from command line argument
# ---------------------------------------------------------------------
if [ -z "$1" ]; then
    MSG="Site rebuild $(date)"
else
    MSG="$*"
fi

# 3. Output Function for Clean Terminal Messages
# ---------------------------------------------------------------------
msg() {
    printf "\n\033[1;32m%s\033[0m\n" "$1"
}

# 4. Main Deployment Logic
# ---------------------------------------------------------------------

# Exit immediately if a command returns a non-zero status
set -e

msg "--- Starting Hugo Source Push ---"

# Clear out local public directory
msg "Cleaning local 'public' folder..."
rm -rf public

# Generate the public folder locally (optional local check)
msg "Building static files locally..."
hugo --minify

# Add all changes in the root directory
msg "Staging all changes (source code, new posts, etc.)..."
git add .

# Commit the changes
msg "Committing source files with message: $MSG"
if git commit -m "$MSG"; then
    : # Successful commit
else
    msg "No changes to commit. Exiting."
    exit 0
fi

# Push the source files to GitHub
msg "Pushing source files to GitHub..."
git push $REMOTE_NAME $SOURCE_BRANCH

msg "--- PUSH COMPLETE! ---"
msg "Deployment triggered on GitHub Actions. Check status online."
```

### 2\. Daily Workflow

For any future post or update, run this single command from your project root:

```bash
./deploy.sh "Your descriptive commit message here"
```

Your final blog URL is: **`https://rikkisnah.github.io/`**
