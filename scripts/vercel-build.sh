#!/usr/bin/env bash
# Vercel build: use committed site/ if present; otherwise run Python pipeline.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f site/index.html ]]; then
  echo "Prebuilt site/ found ($(find site -name 'index.html' | wc -l) pages) — skipping Python build."
  exit 0
fi

echo "No site/index.html — running full build..."
python3 -m pip install -r requirements.txt
python3 build.py
test -f site/index.html
