#!/usr/bin/env bash
set -euo pipefail

# Usage: ./release.sh [major|minor|patch]
# Default: patch

BUMP="${1:-patch}"

# Get current version
CURRENT=$(python3 -c "
import re
with open('pyproject.toml') as f:
    m = re.search(r'version\s*=\s*\"(.+?)\"', f.read())
    print(m.group(1))
")

# Bump version
IFS='.' read -r major minor patch <<< "$CURRENT"
case "$BUMP" in
    major) major=$((major + 1)); minor=0; patch=0 ;;
    minor) minor=$((minor + 1)); patch=0 ;;
    patch) patch=$((patch + 1)) ;;
    *) echo "Usage: $0 [major|minor|patch]"; exit 1 ;;
esac
NEW="${major}.${minor}.${patch}"

echo "Bumping $CURRENT -> $NEW"

# Update pyproject.toml
sed -i '' "s/version = \"$CURRENT\"/version = \"$NEW\"/" pyproject.toml

# Build
rm -rf dist/
python3 -m build

# Upload to PyPI
python3 -m twine upload dist/*

# Commit, tag, push
git add pyproject.toml
git commit -m "Release v${NEW}"
git tag "v${NEW}"
git push && git push --tags

# Create GitHub release
if command -v gh &> /dev/null; then
    gh release create "v${NEW}" --title "v${NEW}" --generate-notes
    echo "GitHub release created."
else
    echo "gh CLI not installed — skipping GitHub release."
fi

echo "Published claudible $NEW"
