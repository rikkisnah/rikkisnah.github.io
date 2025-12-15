# Claude Code Instructions

**Project: "Markdown Is the New Source Code" — Podcast Integration**

## Prime Directive (Read First)

Before making **any changes**, you must:

1. Read `CLAUDE.md` (note: uppercase, not `claude.md`)
2. Read `README.md`
3. Inspect `content/podcast/` directory and examine existing episodes

These files define:

* How podcasts are structured in this Hugo repository
* Required front matter fields and naming conventions
* Metadata format and reserved field names
* Blog post integration patterns
* File paths and directory structure

**Do not assume defaults.**
**Follow existing repository conventions exactly.**

---

## Objective

Create and integrate a podcast episode for the blog post:

**“Markdown Is the New Source Code”**

This work has **two deliverables**, implemented according to the repo’s documented podcast workflow.

---

## Source Material

### Blog Post (Local File)

**File path:** `content/posts/markdown-Is-the-new-source-code.md`

**Published URL:** https://rikkisnah.github.io/posts/markdown-is-the-new-source-code/

### Podcast Audio (Already Produced)

**MP3 URL:**
```
https://objectstorage.us-phoenix-1.oraclecloud.com/n/axbtr6skl2h2/b/rikkisnah-github-podcast-media/o/markdown-is-the-new-source-code-podcast.mp3
```

**Note:** File extension is `.mp3` (lowercase). Verify case sensitivity matches OCI Object Storage.

### Podcast Script

Use the provided script text **exactly as-is** for the podcast show notes.
Do not rewrite, summarize, or stylistically modify it.

---

## Tasks

### Task 1 — Create Podcast Episode

**File path:** `content/podcast/markdown-is-the-new-source-code.md`

**Reference:** See `content/podcast/rekha-15th-birthday.md` as the template.

**Required steps:**

1. **Create the episode file** using Hugo command or manually:
   ```bash
   hugo new content/podcast/markdown-is-the-new-source-code.md
   ```

2. **Set front matter** (see `CLAUDE.md` section "Episode Front Matter Fields"):
   - `title`: "Episode 2: Markdown Is the New Source Code" (Episode 1 exists, so this is Episode 2)
   - `date`: Use the blog post date: `2025-12-14T10:00:00-07:00`
   - `draft`: `false`
   - `audioUrl`: Use the provided MP3 URL exactly
   - `duration`: Calculate from audio file (HH:MM:SS format)
   - `episode`: `2`
   - `season`: `1`
   - `summary`: Short description for RSS feed (< 250 chars)
   - `description`: Longer description for show notes
   - `keywords`: Array of relevant tags (e.g., `["AI", "markdown", "development", "documentation"]`)

3. **Add show notes** in the body using the provided script text.

4. **Add related link** to the blog post:
   ```markdown
   ## Related
   
   - [Blog post: Markdown Is the New Source Code](/posts/markdown-is-the-new-source-code/)
   ```

**Critical:** Use `audioUrl` (not `audio`) and `episodeImage` (not `image`) to avoid Hugo OpenGraph conflicts. See `CLAUDE.md` section "CRITICAL: Reserved Front Matter Field Names".

---

### Task 2 — Integrate Podcast into Blog Post

**File path:** `content/posts/markdown-Is-the-new-source-code.md`

**Reference:** See `content/posts/rekha-fifteen-years-old-birthday.md` lines 34-39 for the exact pattern.

**Required steps:**

1. **Add a "Listen" or "Watch & Listen" section** at the end of the blog post (before the author bio/footer).

2. **Use this exact pattern:**
   ```markdown
   ---
   
   ## Listen
   
   - [Listen to Podcast Episode](/podcast/markdown-is-the-new-source-code/)
   ```

3. **Alternative pattern** (if YouTube video exists):
   ```markdown
   ---
   
   ## Watch & Listen
   
   - [Listen to Podcast Episode](/podcast/markdown-is-the-new-source-code/)
   ```

**Requirements:**

* Use the exact markdown link format shown above
* Place the section at the end of the post content, before any author bio or references
* Do **not** alter the original blog prose, structure, or tone
* Do **not** duplicate content between podcast show notes and blog post
* The link path should match the podcast episode filename (without `.md` extension)

---

## Constraints

* **Repository conventions override all assumptions** — Follow `CLAUDE.md` and `README.md` exactly
* **Blog content is immutable** — Only add the podcast link section; do not modify existing prose
* **No stylistic changes** — Match existing patterns exactly (see `rekha-15th-birthday.md` example)
* **No content duplication** — Podcast show notes and blog post should complement, not duplicate
* **File naming** — Use kebab-case: `markdown-is-the-new-source-code.md`
* **Episode numbering** — This is Episode 2 (Episode 1 is `rekha-15th-birthday.md`)

---

## Output Expectations

* **Clean, minimal changes** — Only the two files mentioned above
* **Markdown-first** — All content in Markdown format
* **Scoped changes** — No modifications to layouts, themes, or configuration files
* **Infer from examples** — If unclear, reference `content/podcast/rekha-15th-birthday.md` and `content/posts/rekha-fifteen-years-old-birthday.md`
* **Production-ready** — Changes should work immediately after deployment

---

## Definition of Done

**Checklist:**

- [ ] Podcast episode file created at `content/podcast/markdown-is-the-new-source-code.md`
- [ ] Front matter includes all required fields (see `CLAUDE.md` table)
- [ ] Episode number is `2` (Episode 1 exists)
- [ ] `audioUrl` field uses the provided MP3 URL exactly
- [ ] Show notes include the provided script text
- [ ] Show notes include a "Related" section linking to the blog post
- [ ] Blog post (`content/posts/markdown-Is-the-new-source-code.md`) includes podcast link section
- [ ] Podcast link uses format: `[Listen to Podcast Episode](/podcast/markdown-is-the-new-source-code/)`
- [ ] No changes to existing blog post content (only addition of link section)
- [ ] No use of reserved front matter field names (`image`, `audio`, `video`, etc.)
- [ ] File paths match Hugo content structure (`content/podcast/` and `content/posts/`)

**Verification:**

After implementation, verify:
1. Episode appears on `/podcast/` listing page
2. Episode has working audio player on its detail page
3. Blog post shows the podcast link at the end
4. Link navigates correctly to the episode page
5. RSS feed includes the new episode (check `/podcast/feed.xml`)

---

## Additional Notes

* **Hugo commands:** Use `hugo server -D` to preview locally with drafts
* **Deployment:** Changes deploy automatically via GitHub Actions on push
* **RSS feed:** Updates automatically; no manual RSS editing required
* **File extensions:** OCI Object Storage URLs are case-sensitive (`.mp3` vs `.MP3`)
