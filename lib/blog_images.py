"""Deterministic blog / journal featured images (manifest-backed)."""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lib.util import FALLBACK_IMAGE, img_url, strip_html

MANIFEST_PATH = os.path.join(ROOT, "data", "blog-image-map.json")
SITE = os.path.join(ROOT, "site")

_manifest: dict | None = None


def _load_manifest() -> dict:
    global _manifest
    if _manifest is not None:
        return _manifest
    if not os.path.isfile(MANIFEST_PATH):
        _manifest = {}
        return _manifest
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        _manifest = json.load(f)
    return _manifest


def reload_manifest() -> None:
    global _manifest
    _manifest = None
    _load_manifest()


def _entry(slug: str) -> dict | None:
    m = _load_manifest()
    e = m.get(slug)
    return e if isinstance(e, dict) else None


def blog_image_path(b: dict) -> str:
    slug = b.get("slug") or ""
    ent = _entry(slug)
    if ent and ent.get("path"):
        path = str(ent["path"]).lstrip("/")
        if os.path.isfile(os.path.join(SITE, path)):
            return path
    # Legacy inline extraction (manifest should cover all posts after sync)
    content = b.get("content") or ""
    for pat in (
        r'<img[^>]+src=["\'](https://indorenursery\.com/wp-content/uploads/[^"\']+)["\']',
        r'<img[^>]+src=["\'](/wp-content/uploads/[^"\']+)["\']',
        r'<img[^>]+src=["\'](/images/[^"\']+)["\']',
        r"(https://indorenursery\.com/wp-content/uploads/[^\s\"'\)>]+)",
        r"(/wp-content/uploads/[^\s\"'\)>]+)",
    ):
        m = re.search(pat, content, re.I)
        if m:
            path = img_url(m.group(1))
            if path != FALLBACK_IMAGE and os.path.isfile(os.path.join(SITE, path)):
                return path
    return FALLBACK_IMAGE


def blog_image_alt(b: dict) -> str:
    slug = b.get("slug") or ""
    ent = _entry(slug)
    if ent and ent.get("alt"):
        return str(ent["alt"])
    title = strip_html(b.get("title") or "")
    if title:
        return title[:120]
    return "Journal article illustration"


def blog_featured_image(b: dict) -> str:
    return blog_image_path(b)


def validate_manifest() -> list[str]:
    warnings: list[str] = []
    m = _load_manifest()
    for slug, ent in m.items():
        if not isinstance(ent, dict):
            continue
        path = str(ent.get("path") or "").lstrip("/")
        if path and not os.path.isfile(os.path.join(SITE, path)):
            warnings.append(f"{slug}: {path}")
    return warnings


def manifest_stats() -> dict:
    m = _load_manifest()
    stats = {"original": 0, "stock": 0, "fallback": 0, "unique_paths": set()}
    for ent in m.values():
        if not isinstance(ent, dict):
            continue
        st = ent.get("source_type", "fallback")
        if st in stats:
            stats[st] += 1
        else:
            stats["fallback"] += 1
        p = ent.get("path")
        if p:
            stats["unique_paths"].add(p)
    stats["unique_paths"] = len(stats["unique_paths"])
    stats["total"] = len(m)
    return stats
