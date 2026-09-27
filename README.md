# Indore Nursery — Website

Premium static site for **Indore Nursery**: curated plants, pots & planters (Excel-driven), green-space services, events, and journal (blog). WhatsApp-first — no checkout.

## Business pillars

1. **Plants** — ~20 active SKUs in shop UI; full legacy catalog preserved in Excel  
2. **Pots** — model pages with size/colour variants and dynamic pricing  
3. **Green spaces** — corporate rental, maintenance, landscaping, events (enquiry-led)

## Client workflow (products)

```
Edit data/excel/indore_nursery_products.xlsx
        ↓
python3 build.py    # or: ./build.sh
        ↓
Deploy site/ (Cloudflare Pages)
```

On Linux, if you see `python: command not found`, use **`python3`** (not `python`).

Sheets: **Plants**, **Pots** (one row per sellable variant; grouped by `product_slug` on the site).

Initial workbook: `python scripts/migrate_catalog_to_excel.py`

## Repository layout

| Path | Purpose |
|------|---------|
| `data/excel/` | Product source of truth (Excel) |
| `data/generated/` | `plants.json`, `pots.json` from sync |
| `data/catalog.json`, `blogs.json` | Legacy catalog & journal content |
| `data/seo/` | URL inventory + migration mapping |
| `lib/` | Config, shell, WhatsApp helpers |
| `build/generator.py` | Site generator |
| `scripts/sync_excel.py` | Excel → JSON |
| `site/` | Built static output (~590 URLs) |
| `parts/gen6–8`, `gen7` | Rich events/season pages (merged into build) |

## Build commands

```bash
python3 build.py                  # recommended — sync + generate + SEO inventory
./build.sh                        # same (wrapper when `python` is missing)
python3 scripts/sync_excel.py     # Excel → JSON only
python3 build/generator.py        # HTML only (requires synced JSON)
python3 scripts/seo_inventory.py  # refresh url-inventory + url-migration.json
```

Legacy: `generate_all.py` + `parts/gen5.py` — superseded by `build.py`; kept for reference.

## SEO migration

- **Keep** existing `/plants/*`, `/blog/*`, `/category/*`, `/events/*`, `/season/*` URLs where still generated  
- **Redirect** legacy pot product URLs `/plants/{slug}/` → `/pots/{model}/` via `site/_redirects` (Cloudflare Pages)  
- Machine-readable map: `data/seo/url-migration.json`  
- Full list: `data/seo/url-inventory.json`

## Deploy

Upload **`site/`** to Cloudflare Pages (static assets). Ensure `_redirects` is included.

Local preview:

```bash
python3 -m http.server 8123 --directory site
```

## Configuration

WhatsApp and domain constants: `lib/config.py` (single source — do not hard-code phone numbers in templates).
