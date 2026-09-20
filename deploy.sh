#!/usr/bin/env bash
# Deploy the site. Usage:  ./deploy.sh "what I changed"
set -euo pipefail

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "What did you change? Put it in quotes:"
  echo "   ./deploy.sh \"new hero copy\""
  exit 1
fi

if [ ! -d .git ]; then
  echo "This folder isn't a git repository yet."
  echo "Follow the one-time setup in DEPLOY.md first."
  exit 1
fi

if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "Nothing has changed since the last deploy."
  exit 0
fi

echo "→ Staging changes"
git add -A

echo "→ Committing:  $MSG"
git commit -m "$MSG"

echo "→ Pushing to GitHub"
git push

REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
# Plain shell rather than sed: macOS ships BSD sed, which has no lazy
# quantifier, so the old `([^/]+?)` pattern errored on every deploy.
REPO=${REMOTE##*/}; REPO=${REPO%.git}
_OWNER_PATH=${REMOTE%/*}; USER=${_OWNER_PATH##*[:/]}

echo
echo "Done. GitHub Pages usually rebuilds within a minute."
if [ -n "$USER" ] && [ -n "$REPO" ]; then
  echo "   Site:   https://${USER}.github.io/${REPO}/"
  echo "   Build:  https://github.com/${USER}/${REPO}/actions"
fi
echo "Hard-refresh with Cmd+Shift+R if you don't see the change."
