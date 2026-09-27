#!/usr/bin/env python3
"""Build Indore Nursery static site: Excel sync → generate → SEO inventory."""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main():
    excel = os.path.join(ROOT, "data", "excel", "indore_nursery_products.xlsx")
    if not os.path.isfile(excel):
        run([sys.executable, "scripts/migrate_catalog_to_excel.py"])
    run([sys.executable, "scripts/sync_excel.py"])
    run([sys.executable, "build/generator.py"])
    run([sys.executable, "scripts/seo_inventory.py"])
    # Legacy single-file CSS alias for old bookmarks
    css_src = os.path.join(ROOT, "site", "assets", "css", "main.css")
    css_dst = os.path.join(ROOT, "site", "style.css")
    if os.path.isfile(css_src):
        with open(css_src, encoding="utf-8") as f:
            open(css_dst, "w", encoding="utf-8").write(f.read())
    print("\nBuild complete. Deploy the site/ folder (Cloudflare Pages).")


if __name__ == "__main__":
    main()
