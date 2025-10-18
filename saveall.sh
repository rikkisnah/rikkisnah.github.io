#!/bin/bash
# saveall - Save blog posts and sync with GitHub Pages repository

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Hugo Blog Sync ===${NC}"
echo "Repository: rikkisnah.github.io"
echo "Host: $(hostname)"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check for uncommitted changes
echo -e "${BLUE}Checking for changes...${NC}"
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
else
    echo "Changes detected"

    # Stage all changes
    echo -e "${BLUE}Staging changes...${NC}"
    git add -A

    # Create commit message with timestamp
    COMMIT_MSG="Blog update: $(date '+%Y-%m-%d %H:%M:%S') from $(hostname)"

    # Commit
    echo -e "${BLUE}Committing changes...${NC}"
    git commit -m "$COMMIT_MSG"
fi

# Pull latest from remote (rebase to avoid merge commits)
echo -e "${BLUE}Pulling latest from remote...${NC}"
git pull --rebase

# Push to GitHub (triggers GitHub Actions deployment)
echo -e "${BLUE}Pushing to GitHub...${NC}"
git push

echo -e "${GREEN}✓ Blog synced and deployed${NC}"
echo "Your changes will be live at: https://rikkisnah.github.io/"
