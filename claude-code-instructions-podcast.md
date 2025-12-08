# Claude Code Prompt: Podcast Infrastructure Setup

## Context

I'm setting up a podcast infrastructure using my existing Hugo blog hosted on GitHub Pages, with media files stored in OCI Object Storage. The podcast will cover topics like OCI, GPUs, AI infrastructure, and engineering leadership.

## Current Setup

- **Blog**: Hugo static site deployed to GitHub Pages
- **Repository**: [Your GitHub repo path]
- **Media Storage**: OCI Object Storage (bucket to be created: `podcast-media`)
- **Video Mirror**: YouTube channel (for optional cross-posting)

## Task Overview

Set up a complete podcast pipeline that meets Apple Podcasts, Spotify, and Google Podcasts RSS requirements.

---

## Phase 1: Hugo Podcast Structure

### 1.1 Create the podcast section directory structure

```
content/podcast/
├── _index.md          # Podcast landing page
├── episode-001.md     # First episode template
└── episode-002.md     # Second episode template (placeholder)

layouts/podcast/
├── list.html          # Podcast listing page template
├── single.html        # Individual episode page template
└── rss.xml            # Custom RSS feed for podcast directories

static/images/podcast/
└── cover.png          # Podcast cover art placeholder (1400x1400 minimum)
```

### 1.2 Create the custom RSS feed template

Create `layouts/podcast/rss.xml` with full podcast RSS 2.0 compliance including:

- iTunes namespace declarations (`xmlns:itunes`, `xmlns:content`, `xmlns:atom`)
- Channel-level metadata: title, description, language, author, owner, category, explicit rating, cover image
- Episode-level metadata: title, description, enclosure (MP3 URL, length, type), pubDate, duration, guid, episode number
- Proper date formatting (RFC 2822)
- Self-referencing atom:link for feed validation

### 1.3 Create the podcast landing page

Create `content/podcast/_index.md` with:

```yaml
---
title: "Podcast"
description: "OCI, GPUs, AI Infrastructure, and Engineering Leadership"
author: "Rik"
email: "[your-email]"
cover: "/images/podcast/cover.png"
category: "Technology"
explicit: "no"
---
```

Include introductory content explaining the podcast focus.

### 1.4 Create episode content template

Create `content/podcast/episode-001.md` as a template:

```yaml
---
title: "Episode 1: [Title]"
date: 2025-01-15T10:00:00-08:00
draft: false
audio: "https://objectstorage.[region].oraclecloud.com/n/[namespace]/b/podcast-media/o/episode-001.mp3"
length: 0              # File size in bytes (update after upload)
duration: "00:00:00"   # HH:MM:SS format
episode: 1
season: 1
summary: "Episode summary for RSS feed (keep under 250 chars)"
description: "Longer description for show notes"
keywords: ["OCI", "GPU", "AI", "infrastructure"]
transcript: ""         # Optional: path to transcript file
---

## Show Notes

Episode content and show notes go here.

## Links Mentioned

- [Link 1](url)
- [Link 2](url)

## Timestamps

- 00:00 - Introduction
- 05:00 - Main topic
- 20:00 - Wrap-up
```

---

## Phase 2: Hugo Templates

### 2.1 Create episode single page template

Create `layouts/podcast/single.html` that displays:

- Episode title and metadata
- Embedded HTML5 audio player with the MP3 source
- Show notes content
- Links to subscribe on Apple Podcasts, Spotify, etc.
- Previous/Next episode navigation

### 2.2 Create podcast list page template

Create `layouts/podcast/list.html` that displays:

- Podcast header with cover art and description
- Subscribe buttons/links
- List of all episodes with titles, dates, summaries, and play buttons
- RSS feed link prominently displayed

### 2.3 Update Hugo config

Add to `hugo.toml` or `config.toml`:

```toml
[outputs]
  section = ["HTML", "RSS"]

[outputFormats.RSS]
  mediaType = "application/rss+xml"
  baseName = "feed"

[mediaTypes."application/rss+xml"]
  suffixes = ["xml"]

[params.podcast]
  title = "Your Podcast Name"
  author = "Rik"
  email = "your-email@domain.com"
  description = "OCI, GPUs, AI Infrastructure, and Engineering Leadership"
  language = "en-us"
  category = "Technology"
  subcategory = "Tech News"
  explicit = "no"
  cover = "/images/podcast/cover.png"
```

---

## Phase 3: OCI Object Storage Setup Script

Create a shell script `scripts/setup-oci-podcast-bucket.sh`:

```bash
#!/bin/bash
# Creates OCI Object Storage bucket for podcast media
# Requires: OCI CLI configured

BUCKET_NAME="podcast-media"
COMPARTMENT_ID="[your-compartment-ocid]"
NAMESPACE=$(oci os ns get --query 'data' --raw-output)

# Create bucket
oci os bucket create \
  --compartment-id $COMPARTMENT_ID \
  --name $BUCKET_NAME \
  --public-access-type ObjectRead

echo "Bucket created. Upload files with:"
echo "oci os object put --bucket-name $BUCKET_NAME --file episode-001.mp3"
echo ""
echo "Public URL format:"
echo "https://objectstorage.[region].oraclecloud.com/n/$NAMESPACE/b/$BUCKET_NAME/o/[filename]"
```

---

## Phase 4: GitHub Actions Workflow

Create `.github/workflows/podcast-build.yml`:

```yaml
name: Build and Deploy Podcast Site

on:
  push:
    branches: [main]
    paths:
      - 'content/podcast/**'
      - 'layouts/podcast/**'
      - 'static/images/podcast/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      
      - name: Build
        run: hugo --minify
      
      - name: Validate RSS Feed
        run: |
          # Basic XML validation
          xmllint --noout public/podcast/feed.xml
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

---

## Phase 5: Helper Scripts

### 5.1 Episode creation script

Create `scripts/new-episode.sh`:

```bash
#!/bin/bash
# Usage: ./new-episode.sh "Episode Title" episode-number

TITLE="$1"
EPISODE_NUM=$(printf "%03d" $2)
FILENAME="episode-${EPISODE_NUM}.md"
DATE=$(date +%Y-%m-%dT%H:%M:%S%z)

cat > "content/podcast/${FILENAME}" << EOF
---
title: "Episode ${2}: ${TITLE}"
date: ${DATE}
draft: true
audio: ""
length: 0
duration: "00:00:00"
episode: ${2}
season: 1
summary: ""
description: ""
keywords: []
transcript: ""
---

## Show Notes

## Links Mentioned

## Timestamps

- 00:00 - Introduction
EOF

echo "Created content/podcast/${FILENAME}"
```

### 5.2 Upload and update script

Create `scripts/upload-episode.sh`:

```bash
#!/bin/bash
# Usage: ./upload-episode.sh episode-001.mp3

FILE="$1"
BUCKET="podcast-media"
FILENAME=$(basename "$FILE")

# Upload to OCI
oci os object put --bucket-name $BUCKET --file "$FILE" --name "$FILENAME"

# Get file size
SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")

# Get namespace and region
NAMESPACE=$(oci os ns get --query 'data' --raw-output)
REGION="us-ashburn-1"  # Update to your region

echo ""
echo "Upload complete!"
echo "Audio URL: https://objectstorage.${REGION}.oraclecloud.com/n/${NAMESPACE}/b/${BUCKET}/o/${FILENAME}"
echo "File size (bytes): ${SIZE}"
echo ""
echo "Update your episode front matter with these values."
```

---

## Phase 6: Documentation

Create `docs/PODCAST-WORKFLOW.md` documenting:

1. How to record and export audio (MP3, 96-128 kbps for speech)
2. How to create episode artwork if needed
3. Step-by-step episode publishing workflow
4. How to submit to podcast directories (Apple, Spotify, Google)
5. RSS feed URL location
6. Troubleshooting common issues

---

## Validation Checklist

After setup, verify:

- [ ] RSS feed is valid XML (use `xmllint` or online validator)
- [ ] RSS feed passes Apple Podcasts validation (https://podcastsconnect.apple.com)
- [ ] RSS feed passes Spotify validation
- [ ] Audio player works on episode pages
- [ ] Episode list displays correctly
- [ ] OCI bucket objects are publicly accessible
- [ ] GitHub Actions workflow runs successfully

---

## Podcast Directory Submission URLs

Include these in documentation:

- **Apple Podcasts**: https://podcasters.apple.com/
- **Spotify**: https://podcasters.spotify.com/
- **Google/YouTube Music**: https://podcasters.google.com/
- **Pocket Casts**: https://pocketcasts.com/submit/
- **Overcast**: https://overcast.fm/podcasterinfo

---

## Notes

- Cover art must be 1400×1400 to 3000×3000 pixels, PNG or JPG
- MP3 files should be 96-128 kbps for speech content
- Episode GUIDs should be stable (use permalink or unique ID)
- Update `length` field with actual byte size after uploading MP3
- Test RSS feed in a podcast app before submitting to directories