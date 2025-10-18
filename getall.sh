#!/bin/bash
# getall - Pull latest updates for current repository

set -euo pipefail

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Pulling Updates ===${NC}"
echo ""

# Get current repository
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Updating: $(basename "$REPO_DIR")"
echo ""

cd "$REPO_DIR"

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

echo ""
echo -e "${GREEN}=== Update Complete ===${NC}"
