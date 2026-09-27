#!/usr/bin/env bash
# Use python3 — many Linux environments do not provide a `python` command.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 build.py "$@"
