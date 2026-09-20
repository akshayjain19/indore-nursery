# Indore Nursery — Website

Static website for Indore Nursery (Indore, MP) — plant catalog, blog, events & decor pages.

## Structure
- `site/` — the built website (555 pages). Serve with `site\Start-Website.bat` (http://localhost:8123)
- `parts/` — Python page generators (`gen1–gen8`, `shell.py`, CSS modules `css*.py`/`v2*.css`)
- `generate_all.py` — main build script, generates the whole site from `data/catalog.json`
- `data/` — product catalog + blog content source

## Build
```
python generate_all.py        # rebuild all pages
python parts/gen5.py          # homepage overrides
python parts/gen6.py          # events page
python parts/gen7.py          # season pages
python parts/gen8.py          # service pages
```

## Deploying
Drag & drop the `site/` folder as a zip into Cloudflare Pages → Workers & Pages → Upload assets.
