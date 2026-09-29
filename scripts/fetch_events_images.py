#!/usr/bin/env python3
"""Download and copy distinct /events/ photography into site/images/events/."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(SITE, "images", "events")

# Pexels (free license) — compressed for web
REMOTE = {
    "hotel-hospitality.jpg": "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "wedding-mandap.jpg": "https://images.pexels.com/photos/1444442/pexels-photo-1444442.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "party-celebration.jpg": "https://images.pexels.com/photos/2747448/pexels-photo-2747448.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "store-cafe-opening.jpg": "https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "festival-big-event.jpg": "https://images.pexels.com/photos/2774556/pexels-photo-2774556.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "reception-corner.jpg": "https://images.pexels.com/photos/1181406/pexels-photo-1181406.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "mandap-backdrop.jpg": "https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "entry-arch.jpg": "https://images.pexels.com/photos/265722/pexels-photo-265722.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "photo-corner.jpg": "https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "table-styling.jpg": "https://images.pexels.com/photos/587741/pexels-photo-587741.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "lobby-greens.jpg": "https://images.pexels.com/photos/2581922/pexels-photo-2581922.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "stage-backdrop.jpg": "https://images.pexels.com/photos/1105666/pexels-photo-1105666.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "hanging-installs.jpg": "https://images.pexels.com/photos/1084199/pexels-photo-1084199.jpeg?auto=compress&cs=tinysrgb&w=1400",
    "cafe-corner.jpg": "https://images.pexels.com/photos/224924/pexels-photo-224924.jpeg?auto=compress&cs=tinysrgb&w=1400",
}

COPY_FROM_REPO = {
    "corporate-gifting.jpg": os.path.join(SITE, "images", "2025_05_gifting-plants.jpeg"),
    "living-wall.jpg": os.path.join(SITE, "images", "2025_07_Vertical-Garden-for-outdoor-plants.jpg"),
    "feature-wall.jpg": os.path.join(SITE, "images", "2024_07_Vertical-planter-ideas-1-900x600.jpg"),
    "terrace-setup.jpg": os.path.join(SITE, "img", "home", "outdoor.jpg"),
}


def curl(url: str, dest: str) -> None:
    subprocess.check_call(
        ["curl", "-fsSL", "--retry", "3", "--retry-delay", "2", "-o", dest, url],
        stdout=subprocess.DEVNULL,
    )


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    for name, src in COPY_FROM_REPO.items():
        if not os.path.isfile(src):
            print("missing repo source:", src, file=sys.stderr)
            return 1
        dest = os.path.join(OUT, name)
        shutil.copy2(src, dest)
        print("copied", name, "from", os.path.relpath(src, ROOT))
    for name, url in REMOTE.items():
        dest = os.path.join(OUT, name)
        print("fetch", name)
        curl(url, dest)
    names = set(COPY_FROM_REPO) | set(REMOTE)
    if len(names) != len(COPY_FROM_REPO) + len(REMOTE):
        print("duplicate output names", file=sys.stderr)
        return 1
    print("wrote", len(names), "files to", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
