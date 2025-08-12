#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

# Fetch PocketFlow core
mkdir -p "$REPO_ROOT/backend"
if [ ! -d "$REPO_ROOT/backend/pocketflow" ] && [ ! -f "$REPO_ROOT/backend/pocketflow.py" ]; then
  git clone --depth 1 https://github.com/The-Pocket/PocketFlow.git /tmp/pf
  if [ -d /tmp/pf/pocketflow ]; then
    cp -r /tmp/pf/pocketflow "$REPO_ROOT/backend/pocketflow"
  elif [ -f /tmp/pf/pocketflow.py ]; then
    cp /tmp/pf/pocketflow.py "$REPO_ROOT/backend/pocketflow.py"
  else
    echo "Could not find pocketflow core in cloned repo" >&2
    exit 1
  fi
fi

# Backend deps
cd "$REPO_ROOT/backend"
if python3 -c "import sys; assert sys.version_info >= (3,7)" 2>/dev/null; then
  if python3 -m venv .venv 2>/dev/null; then
    echo "Using virtualenv at .venv"
    source .venv/bin/activate
    pip install -r requirements.txt
  else
    echo "venv unavailable; installing requirements to user site-packages (break-system-packages)"
    python3 -m pip install --user --break-system-packages -r requirements.txt
  fi
else
  echo "Python3 not found or too old" >&2
  exit 1
fi

# Frontend deps
cd "$REPO_ROOT/frontend"
npm install