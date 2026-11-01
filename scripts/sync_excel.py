#!/usr/bin/env python3
"""Backward-compatible entry: delegates to sync_catalog (Sheets if configured, else Excel)."""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    subprocess.check_call([sys.executable, os.path.join(ROOT, "scripts", "sync_catalog.py")])
