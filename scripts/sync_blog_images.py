#!/usr/bin/env python3
"""Build deterministic blog-image-map.json and optional blog-stock assets."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lib.util import FALLBACK_IMAGE, img_url, strip_html

SITE = os.path.join(ROOT, "site")
BLOGS_PATH = os.path.join(ROOT, "data", "blogs.json")
MANIFEST_PATH = os.path.join(ROOT, "data", "blog-image-map.json")
STOCK_DIR = os.path.join(SITE, "images", "blog-stock")

# Curated local pool (repo paths, no hotlinks). Expanded by fetch_blog_stock.py.
STOCK_BY_CATEGORY: dict[str, list[str]] = {
    "indoor-plants": [
        "images/blog-stock/indoor-plants-01.jpg",
        "images/blog-stock/indoor-plants-02.jpg",
        "images/blog-stock/indoor-plants-03.jpg",
        "img/home/indoor.jpg",
        "images/2025_11_indoor-plants-1-600x400.jpg",
        "images/2025_11_semi-indoor-plants-1-600x400.jpg",
    ],
    "outdoor-plants": [
        "images/blog-stock/outdoor-plants-01.jpg",
        "images/blog-stock/outdoor-plants-02.jpg",
        "img/home/outdoor.jpg",
        "images/2025_10_small-gardens-plants-900x600.jpg",
        "images/2025_07_Vertical-Garden-for-outdoor-plants.jpg",
    ],
    "succulents": [
        "images/blog-stock/succulents-01.jpg",
        "images/blog-stock/succulents-02.jpg",
        "images/2023_03_aglaonema-chinese-evergreen-900x600.webp",
    ],
    "flowering-plants": [
        "images/blog-stock/flowering-plants-01.jpg",
        "images/blog-stock/flowering-plants-02.jpg",
        "images/2025_10_Creepers-for-home-1024x683.jpg",
    ],
    "vegetable-gardening": [
        "images/blog-stock/vegetable-gardening-01.jpg",
        "images/blog-stock/vegetable-gardening-02.jpg",
        "images/2023_02_13-Easy-Tips-for-Broccoli-Growing-and-Care-900x600.jpg",
    ],
    "plant-care": [
        "images/blog-stock/plant-care-01.jpg",
        "images/blog-stock/plant-care-02.jpg",
        "images/2025_07_Essential-Gardening-Tools-and-How-to-Use-Them-Effectively-768x512.jpg",
        "images/2025_05_seasonal-garding-tips-300x177.jpg",
        "images/2022_05_013A1558.jpg",
    ],
    "soil-fertilizer": [
        "images/blog-stock/soil-fertilizer-01.jpg",
        "images/blog-stock/soil-fertilizer-02.jpg",
        "images/2025_04_mulch-768x439.jpg",
        "images/2024_10_FloraDiet-ReadyToUse.jpg",
    ],
    "pots-planters": [
        "images/blog-stock/pots-planters-01.jpg",
        "images/blog-stock/pots-planters-02.jpg",
        "images/2024_07_jpeg-optimizer_Integrated-Planters.jpg",
    ],
    "landscaping": [
        "images/blog-stock/landscaping-01.jpg",
        "images/blog-stock/landscaping-02.jpg",
        "images/2025_11_landscape-gardening-1-600x400.jpg",
        "images/2025_07_zen-garden.jpg",
    ],
    "plant-benefits": [
        "images/blog-stock/plant-benefits-01.jpg",
        "images/blog-stock/plant-benefits-02.jpg",
        "images/2025_10_Low-Maintenance-Plants-for-Busy-Professionals-For-Office-Spaces-4-600x400.jpg",
    ],
    "seasonal": [
        "images/blog-stock/seasonal-01.jpg",
        "images/blog-stock/seasonal-02.jpg",
        "images/2025_05_seasonal-garding-tips-300x177.jpg",
    ],
    "general-botanical": [
        "images/blog-stock/general-botanical-01.jpg",
        "images/blog-stock/general-botanical-02.jpg",
        "images/2025_10_Indore-nursery-3-768x1152.jpg",
        "images/2022_05_013A1558.jpg",
    ],
}

PEXELS_DOWNLOADS = {
    "images/blog-stock/indoor-plants-01.jpg": "https://images.pexels.com/photos/1084199/pexels-photo-1084199.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/indoor-plants-02.jpg": "https://images.pexels.com/photos/1459495/pexels-photo-1459495.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/indoor-plants-03.jpg": "https://images.pexels.com/photos/941871/pexels-photo-941871.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/outdoor-plants-01.jpg": "https://images.pexels.com/photos/1131458/pexels-photo-1131458.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/outdoor-plants-02.jpg": "https://images.pexels.com/photos/269558/pexels-photo-269558.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/succulents-01.jpg": "https://images.pexels.com/photos/1287368/pexels-photo-1287368.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/succulents-02.jpg": "https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/flowering-plants-01.jpg": "https://images.pexels.com/photos/2877795/pexels-photo-2877795.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/flowering-plants-02.jpg": "https://images.pexels.com/photos/36764/marguerite-daisy-beautiful-beauty.jpg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/vegetable-gardening-01.jpg": "https://images.pexels.com/photos/1327838/pexels-photo-1327838.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/vegetable-gardening-02.jpg": "https://images.pexels.com/photos/2751755/pexels-photo-2751755.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/plant-care-01.jpg": "https://images.pexels.com/photos/3408353/pexels-photo-3408353.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/plant-care-02.jpg": "https://images.pexels.com/photos/450035/pexels-photo-450035.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/soil-fertilizer-01.jpg": "https://images.pexels.com/photos/8777513/pexels-photo-8777513.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/soil-fertilizer-02.jpg": "https://images.pexels.com/photos/625325/pexels-photo-625325.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/pots-planters-01.jpg": "https://images.pexels.com/photos/1005058/pexels-photo-1005058.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/pots-planters-02.jpg": "https://images.pexels.com/photos/6231298/pexels-photo-6231298.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/landscaping-01.jpg": "https://images.pexels.com/photos/812229/pexels-photo-812229.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/landscaping-02.jpg": "https://images.pexels.com/photos/1133957/pexels-photo-1133957.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/plant-benefits-01.jpg": "https://images.pexels.com/photos/3800517/pexels-photo-3800517.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/plant-benefits-02.jpg": "https://images.pexels.com/photos/3807388/pexels-photo-3807388.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/seasonal-01.jpg": "https://images.pexels.com/photos/360912/pexels-photo-360912.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/seasonal-02.jpg": "https://images.pexels.com/photos/189563/pexels-photo-189563.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/general-botanical-01.jpg": "https://images.pexels.com/photos/3076899/pexels-photo-3076899.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "images/blog-stock/general-botanical-02.jpg": "https://images.pexels.com/photos/189563/pexels-photo-189563.jpeg?auto=compress&cs=tinysrgb&w=1200",
}

CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("succulents", ("succulent", "cactus", "echeveria", "sedum", "haworthia", "crassula")),
    ("vegetable-gardening", ("tomato", "vegetable", "broccoli", "capsicum", "cucumber", "spinach", "radish", "beetroot", "kitchen garden", "giy", "oregano", "herb garden")),
    ("flowering-plants", ("flowering", "flower", "mogra", "jasmine", "ixora", "rose", "marigold", "bloom", "ornamental")),
    ("pots-planters", ("pot", "planter", "container garden")),
    ("soil-fertilizer", ("soil", "fertiliz", "compost", "mulch", "nutrient", "epsom", "vermicompost", "manure")),
    ("landscaping", ("landscap", "vertical garden", "lawn", "terrace garden", "zen garden", "bonsai")),
    ("plant-benefits", ("benefit", "air purif", "health", "mental", "gifting plant", "betel leaf")),
    ("seasonal", ("winter", "summer", "monsoon", "seasonal", "spring")),
    (
        "indoor-plants",
        (
            "indoor",
            "office",
            "apartment",
            "houseplant",
            "low light",
            "semi-indoor",
            "spider plant",
            "snake plant",
            "money plant",
            "pothos",
            "monstera",
            "philodendron",
            "dracaena",
            "aglaonema",
            "sansevieria",
            "calathea",
            "croton",
            "broken heart",
            "syngonium",
            "ficus",
            "peace lily",
        ),
    ),
    ("outdoor-plants", ("outdoor", "balcony", "terrace", "creeper", "sunlight requirement", "garden bed")),
    ("plant-care", ("drooping", "yellow leaf", "brown tip", "root rot", "pest", "fungal", "wilting")),
]

STOP_TOKENS = frozenset(
    {
        "indore",
        "nursery",
        "plant",
        "plants",
        "best",
        "guide",
        "tips",
        "your",
        "with",
        "that",
        "this",
        "from",
        "have",
        "home",
        "blog",
        "article",
        "2024",
        "2025",
    }
)


def curl(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    subprocess.check_call(
        ["curl", "-fsSL", "--retry", "3", "--retry-delay", "2", "-o", dest, url],
        stdout=subprocess.DEVNULL,
    )


def ensure_stock_files() -> None:
    os.makedirs(STOCK_DIR, exist_ok=True)
    for rel, url in PEXELS_DOWNLOADS.items():
        dest = os.path.join(SITE, rel)
        if os.path.isfile(dest):
            continue
        print("+ fetch", rel)
        try:
            curl(url, dest)
        except subprocess.CalledProcessError:
            print("WARN: failed to fetch", rel, file=sys.stderr)


def extract_content_image(b: dict) -> str | None:
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
    return None


def classify_category(title: str, slug: str) -> str:
    text = f"{title} {slug}".lower().replace("-", " ")
    for cat, keys in CATEGORY_RULES:
        if any(k in text for k in keys):
            return cat
    return "general-botanical"


def pick_stock_path(slug: str, category: str) -> str:
    pool = [p for p in STOCK_BY_CATEGORY.get(category, []) if os.path.isfile(os.path.join(SITE, p))]
    if not pool:
        pool = [p for p in STOCK_BY_CATEGORY["general-botanical"] if os.path.isfile(os.path.join(SITE, p))]
    if not pool:
        return FALLBACK_IMAGE
    digest = hashlib.sha256(slug.encode("utf-8")).hexdigest()
    idx = int(digest[:8], 16) % len(pool)
    return pool[idx]


def alt_for_category(category: str, title: str) -> str:
    title_clean = strip_html(title).strip()
    if title_clean and len(title_clean) <= 100:
        return title_clean[:120]
    templates = {
        "succulents": "Succulent plants in a bright setting",
        "vegetable-gardening": "Vegetable garden with healthy produce",
        "flowering-plants": "Flowering plants in a garden setting",
        "pots-planters": "Planters arranged with green plants",
        "soil-fertilizer": "Garden soil and plant nutrition",
        "landscaping": "Landscaped garden with layered planting",
        "plant-benefits": "Healthy indoor plants in a living space",
        "seasonal": "Seasonal plants in a home garden",
        "outdoor-plants": "Outdoor garden planting",
        "plant-care": "Houseplant care and watering",
        "indoor-plants": "Indoor plants by a window",
        "general-botanical": "Green plants in natural light",
    }
    return templates.get(category, "Green plants in natural light")


def build_manifest(blogs: list) -> dict:
    manifest: dict = {}
    warnings: list[str] = []
    for b in blogs:
        slug = b.get("slug") or ""
        if not slug:
            continue
        title = b.get("title") or ""
        original = extract_content_image(b)
        if original:
            cat = classify_category(title, slug)
            title_clean = strip_html(title).strip()
            manifest[slug] = {
                "path": original,
                "source_type": "original",
                "category": cat,
                "alt": (title_clean[:120] if title_clean else alt_for_category(cat, title)),
            }
            continue
        category = classify_category(title, slug)
        path = pick_stock_path(slug, category)
        source_type = "stock" if path != FALLBACK_IMAGE else "fallback"
        if not os.path.isfile(os.path.join(SITE, path)):
            warnings.append(f"missing image for {slug}: {path}")
            path = FALLBACK_IMAGE
            source_type = "fallback"
        manifest[slug] = {
            "path": path,
            "source_type": source_type,
            "category": category,
            "alt": alt_for_category(category, title),
        }
    if warnings:
        for w in warnings[:20]:
            print("WARN:", w, file=sys.stderr)
        if len(warnings) > 20:
            print(f"WARN: ... and {len(warnings) - 20} more", file=sys.stderr)
    return manifest


def main() -> int:
    ensure_stock_files()
    # Validate pool files exist (filter STOCK_BY_CATEGORY in memory for missing)
    for cat, paths in list(STOCK_BY_CATEGORY.items()):
        STOCK_BY_CATEGORY[cat] = [p for p in paths if os.path.isfile(os.path.join(SITE, p))]

    blogs = json.load(open(BLOGS_PATH, encoding="utf-8"))
    manifest = build_manifest(blogs)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    stats = {"original": 0, "stock": 0, "fallback": 0, "unique": set()}
    for ent in manifest.values():
        stats[ent["source_type"]] += 1
        stats["unique"].add(ent["path"])
    print(
        f"blog-image-map: {len(manifest)} entries — "
        f"original={stats['original']} stock={stats['stock']} fallback={stats['fallback']} "
        f"unique_paths={len(stats['unique'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
