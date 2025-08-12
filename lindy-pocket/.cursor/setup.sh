#!/usr/bin/env bash
set -euo pipefail

# Clone PocketFlow and copy the single-file core
if [ ! -d /tmp/pf ]; then
  git clone https://github.com/The-Pocket/PocketFlow.git /tmp/pf
fi
mkdir -p backend
cp /tmp/pf/pocketflow.py backend/pocketflow.py || true

# Backend env
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend deps
cd ../frontend || true
if [ -f package.json ]; then
  npm install
fi