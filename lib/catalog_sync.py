"""Validate product rows and write generated catalog JSON (Excel or Sheets)."""

from __future__ import annotations

import json
import os

from lib.config import GENERATED_DIR, PLANTS_JSON, POTS_JSON
from lib.util import slugify

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SyncError(Exception):
    pass


def yn(val, default=False):
    if val is None or val == "":
        return default
    return str(val).strip().upper() in ("YES", "Y", "TRUE", "1", "ACTIVE")


def num(val):
    if val is None or val == "":
        return None
    try:
        return int(float(val))
    except (TypeError, ValueError):
        raise SyncError(f"Invalid price: {val!r}")


def normalize_row_value(val):
    if val is None:
        return None
    if isinstance(val, str) and not val.strip():
        return None
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def rows_from_table(table: list[list]) -> list[dict]:
    """First row = headers; skip blank data rows."""
    if not table:
        raise SyncError("Sheet is empty")
    headers = [str(h or "").strip() for h in table[0]]
    if not any(headers):
        raise SyncError("Sheet missing header row")
    out = []
    for row in table[1:]:
        if not row or not any(c not in (None, "") for c in row):
            continue
        cells = [normalize_row_value(c) for c in row]
        out.append({headers[i]: cells[i] if i < len(cells) else None for i in range(len(headers))})
    return out


def validate_plants(rows):
    out = []
    ids = set()
    slugs = set()
    for r in rows:
        if not r.get("slug"):
            raise SyncError("Plant row missing slug")
        if not r.get("name"):
            raise SyncError(f"Plant {r['slug']} missing name")
        pid = r.get("product_id")
        if pid in ids:
            raise SyncError(f"Duplicate plant product_id {pid}")
        ids.add(pid)
        s = slugify(r["slug"])
        if s in slugs:
            raise SyncError(f"Duplicate plant slug {s}")
        slugs.add(s)
        price = num(r.get("price")) if r.get("price") not in (None, "") else None
        reg = num(r.get("regular_price")) if r.get("regular_price") not in (None, "") else None
        tags = [t.strip() for t in str(r.get("tags") or "").split(",") if t.strip()]
        out.append(
            {
                "product_id": pid,
                "legacy_id": r.get("legacy_id"),
                "name": str(r["name"]).strip(),
                "slug": s,
                "active": yn(r.get("active")),
                "status": (r.get("status") or "archived").strip().lower(),
                "price": price,
                "regular_price": reg,
                "short_description": r.get("short_description") or "",
                "description": r.get("description") or "",
                "image": r.get("image") or "",
                "gallery": [g for g in str(r.get("gallery") or "").split("|") if g],
                "product_type": "plant",
                "collection": r.get("collection") or "",
                "tags": tags,
                "featured": yn(r.get("featured")),
                "sort_order": int(float(r.get("sort_order") or 0)),
                "whatsapp_enabled": yn(r.get("whatsapp_enabled"), True),
                "seo_title": r.get("seo_title") or "",
                "seo_description": r.get("seo_description") or "",
            }
        )
    out.sort(key=lambda x: x["sort_order"])
    return out


def validate_pots(rows):
    models = {}
    ids = set()
    for r in rows:
        pid = r.get("product_id")
        if pid in ids:
            raise SyncError(f"Duplicate pot variant id {pid}")
        ids.add(pid)
        pslug = slugify(r.get("product_slug") or "")
        if not pslug:
            raise SyncError(f"Pot variant {pid} missing product_slug")
        price = num(r.get("price")) if r.get("price") not in (None, "") else None
        reg = num(r.get("regular_price")) if r.get("regular_price") not in (None, "") else None
        variant = {
            "product_id": pid,
            "size": str(r.get("size") or "Standard").strip(),
            "colour": str(r.get("colour") or "Standard").strip(),
            "price": price,
            "regular_price": reg,
            "active": yn(r.get("active"), True),
            "legacy_slug": (r.get("legacy_slug") or "").strip(),
        }
        m = models.setdefault(
            pslug,
            {
                "product_slug": pslug,
                "model_name": str(r.get("model_name") or pslug).strip(),
                "collection": str(r.get("collection") or "Plastic Pots").strip(),
                "material": str(r.get("material") or "").strip(),
                "description": r.get("description") or "",
                "short_description": r.get("short_description") or "",
                "image": r.get("image") or "",
                "gallery": [g for g in str(r.get("gallery") or "").split("|") if g],
                "featured": yn(r.get("featured")),
                "sort_order": int(float(r.get("sort_order") or 0)),
                "whatsapp_enabled": yn(r.get("whatsapp_enabled"), True),
                "seo_title": r.get("seo_title") or "",
                "seo_description": r.get("seo_description") or "",
                "status": (r.get("status") or "active").strip().lower(),
                "variants": [],
            },
        )
        m["variants"].append(variant)
    out = []
    for _pslug, m in models.items():
        dedup = {}
        for v in m["variants"]:
            key = (v["size"], v["colour"])
            prev = dedup.get(key)
            if not prev:
                dedup[key] = v
                continue
            if "set-of" in (prev.get("legacy_slug") or "") and "set-of" not in (v.get("legacy_slug") or ""):
                dedup[key] = v
        m["variants"] = list(dedup.values())
        active_variants = [v for v in m["variants"] if v["active"]]
        if not active_variants:
            m["status"] = "archived"
        prices = [v["price"] for v in active_variants if v["price"] is not None]
        m["from_price"] = min(prices) if prices else None
        sizes = sorted({v["size"] for v in active_variants}, key=lambda x: (len(x), x))
        colours = sorted({v["colour"] for v in active_variants})
        m["sizes"] = sizes
        m["colours"] = colours
        out.append(m)
    out.sort(key=lambda x: x["sort_order"])
    return out


def write_generated_catalog(plants: list, pots: list, *, source: str = "unknown") -> None:
    os.makedirs(os.path.join(ROOT, GENERATED_DIR), exist_ok=True)
    meta_path = os.path.join(ROOT, GENERATED_DIR, "catalog-sync-meta.json")
    with open(os.path.join(ROOT, PLANTS_JSON), "w", encoding="utf-8") as f:
        json.dump(plants, f, indent=2)
        f.write("\n")
    with open(os.path.join(ROOT, POTS_JSON), "w", encoding="utf-8") as f:
        json.dump(pots, f, indent=2)
        f.write("\n")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(
            {"source": source, "plants": len(plants), "pot_models": len(pots)},
            f,
            indent=2,
        )
        f.write("\n")


def sync_from_row_dicts(plant_rows: list[dict], pot_rows: list[dict], *, source: str) -> tuple[int, int]:
    plants = validate_plants(plant_rows)
    pots = validate_pots(pot_rows)
    write_generated_catalog(plants, pots, source=source)
    return len(plants), len(pots)
