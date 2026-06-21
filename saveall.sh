#!/bin/bash
# saveall - Save blog posts and sync with GitHub Pages repository

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub SSH: port 443 + dedicated key (port 22 blocked on some networks)
export GIT_SSH_COMMAND='ssh -i ~/.ssh/id_github_rsa -o IdentitiesOnly=yes -o ConnectTimeout=30 -p 443 -o Hostname=ssh.github.com'

echo -e "${BLUE}=== Hugo Blog Sync ===${NC}"
echo "Repository: rikkisnah.github.io"
echo "Host: $(hostname)"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check for uncommitted or untracked changes
echo -e "${BLUE}Checking for changes...${NC}"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "No changes to commit"
else
    echo "Changes detected"

    # Stage all changes
    echo -e "${BLUE}Staging changes...${NC}"
    git add -A

    # Get diff summary for commit message
    DIFF_SUMMARY=$(git diff --cached --stat)

    # Create commit message with timestamp and change summary
    COMMIT_MSG="Blog update: $(date '+%Y-%m-%d %H:%M:%S') from $(hostname)

Summary of changes:
$DIFF_SUMMARY"

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
