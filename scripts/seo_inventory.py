#!/usr/bin/env python3
"""Generate SEO URL inventory and migration mapping."""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.config import SEO_INVENTORY_JSON, SEO_MIGRATION_JSON, SITE_URL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")


def path_to_url(path):
    rel = path.replace(SITE, "").replace("\\", "/")
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    if not rel.endswith("/"):
        rel += "/"
    return SITE_URL + (rel if rel != "/" else "/")


def main():
    urls = []
    for dirpath, _, files in os.walk(SITE):
        for f in files:
            if f == "index.html":
                full = os.path.join(dirpath, f)
                urls.append(path_to_url(full))

    urls = sorted(set(urls))
    inventory = [{"url": u, "path": u.replace(SITE_URL, "")} for u in urls]
    os.makedirs(os.path.join(ROOT, "data", "seo"), exist_ok=True)
    json.dump(inventory, open(os.path.join(ROOT, SEO_INVENTORY_JSON), "w"), indent=2)

    migration = []
    pots = json.load(open(os.path.join(ROOT, "data", "generated", "pots.json")))
    for model in pots:
        new_url = f"/pots/{model['product_slug']}/"
        for v in model.get("variants") or []:
            leg = v.get("legacy_slug")
            if not leg:
                continue
            old_url = f"/plants/{leg}/"
            migration.append(
                {
                    "legacy_url": old_url,
                    "current_status": "indexed_product",
                    "new_url": new_url,
                    "action": "REDIRECT",
                    "reason": "Pot model pages moved under /pots/",
                }
            )

    # Keep rules for major sections
    for path, action, reason in [
        ("/", "KEEP", "Homepage"),
        ("/plants/", "KEEP", "Plants shop hub"),
        ("/pots/", "KEEP", "Pots shop hub"),
        ("/green-spaces/", "KEEP", "Services hub"),
        ("/blog/", "KEEP", "Journal / SEO content"),
        ("/events/", "KEEP", "Events & decor"),
        ("/category/", "KEEP", "Legacy category archives"),
        ("/season/", "KEEP", "Seasonal landing pages"),
    ]:
        migration.append(
            {
                "legacy_url": path,
                "current_status": "primary",
                "new_url": path,
                "action": action,
                "reason": reason,
            }
        )

    json.dump(migration, open(os.path.join(ROOT, SEO_MIGRATION_JSON), "w"), indent=2)
    print(f"Inventory: {len(inventory)} URLs → {SEO_INVENTORY_JSON}")
    print(f"Migration rules: {len(migration)} → {SEO_MIGRATION_JSON}")


if __name__ == "__main__":
    main()
