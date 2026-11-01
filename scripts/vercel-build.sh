#!/usr/bin/env bash
# Vercel build: live catalog from Google Sheets when configured; else prebuilt site/ or full build.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -n "${GOOGLE_SHEETS_SPREADSHEET_ID:-}" ]]; then
  echo "GOOGLE_SHEETS_SPREADSHEET_ID set — syncing catalog and running full build."
  python3 -m pip install -q -r requirements.txt
  python3 build.py
  test -f site/index.html
  exit 0
fi

if [[ -f site/index.html ]]; then
  echo "Prebuilt site/ found ($(find site -name 'index.html' | wc -l) pages) — skipping Python build."
  exit 0
fi

echo "No site/index.html — running full build..."
python3 -m pip install -r requirements.txt
python3 build.py
test -f site/index.html
