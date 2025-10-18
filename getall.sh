#!/bin/bash
# getall - Pull latest updates from all sibling repositories

set -euo pipefail

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Pulling Updates from All Repositories ===${NC}"
echo ""

# Get parent directory (one level up from current repo)
PARENT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "Working in parent directory: $PARENT_DIR"
echo ""

# List of sibling project directories
dirs=(
  oci-designs
  oci-it
  oci-interviews
  oci-projects
  oci-runbooks
  romulus-log-scrapper
)

# Track results
updated=0
skipped=0

for d in "${dirs[@]}"; do
  REPO_PATH="$PARENT_DIR/$d"
  if [ -d "$REPO_PATH/.git" ]; then
    echo -e "${BLUE}>>> Updating $d${NC}"
    (
      cd "$REPO_PATH"
      # Stash any local changes
      if git stash push -u -m "auto-stash $(date +%F_%T)" 2>&1 | grep -q "No local changes"; then
        echo "  No local changes to stash"
      else
        echo "  Stashed local changes"
      fi
      # Pull with fast-forward only
      if git pull --ff-only; then
        echo "  Successfully pulled latest changes"
      else
        echo "  Note: Could not fast-forward (local changes exist)"
      fi
    )
    echo -e "${GREEN}✓ Updated $d${NC}"
    ((updated++))
    echo ""
  else
    echo -e "${YELLOW}!!! Skipping $d (not a git repo)${NC}"
    ((skipped++))
    echo ""
  fi
done

echo -e "${GREEN}=== Update Complete ===${NC}"
echo "Updated: $updated repos | Skipped: $skipped repos"
