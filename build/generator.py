#!/usr/bin/env python3
"""Static site generator — premium IA, Excel-driven products, SEO-safe legacy URLs."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lib.config import PLANTS_JSON, POTS_JSON, SITE_URL, WA_PHONE
from lib.shell import page_shell
from lib.util import esc, img_url, money, strip_html, wa_link
from lib.whatsapp import (
    corporate_message,
    event_message,
    general_message,
    landscaping_message,
    plant_message,
    pot_message,
)

SITE = os.path.join(ROOT, "site")
FACTS = json.load(open(os.path.join(ROOT, "data", "facts.json"), encoding="utf-8"))
BLOGS = json.load(open(os.path.join(ROOT, "data", "blogs.json"), encoding="utf-8"))
CATALOG = json.load(open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8"))
PLANTS = json.load(open(os.path.join(ROOT, PLANTS_JSON), encoding="utf-8"))
POTS = json.load(open(os.path.join(ROOT, POTS_JSON), encoding="utf-8"))

PLANT_BY_SLUG = {p["slug"]: p for p in PLANTS}
POT_BY_SLUG = {p["product_slug"]: p for p in POTS}
POT_LEGACY_REDIRECTS = {}
for m in POTS:
    for v in m.get("variants") or []:
        if v.get("legacy_slug"):
            POT_LEGACY_REDIRECTS[v["legacy_slug"]] = m["product_slug"]

ACTIVE_PLANTS = [p for p in PLANTS if p.get("active")]
ACTIVE_POTS = [p for p in POTS if p.get("status") != "archived"]


def write(path, content):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def slugify(s):
    s = (s or "").lower().replace("&", "and").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def plant_card(p, compact=False):
    desc = strip_html(p.get("short_description") or "")[:140]
    tags = ",".join(p.get("tags") or [])
    return f"""<article class="plant-card-v2" data-tags="{esc(tags)}">
<a href="/plants/{esc(p['slug'])}/" class="pic"><img loading="lazy" src="/{esc(img_url(p.get('image')))}" alt="{esc(p['name'])}"></a>
<div class="info"><h3><a href="/plants/{esc(p['slug'])}/">{esc(p['name'])}</a></h3>
<p class="desc">{esc(desc)}</p>
<div class="foot"><p><span class="price">{money(p.get('price'))}</span>{(' <span class="old">'+money(p.get('regular_price'))+'</span>') if p.get('regular_price') and p.get('price') and p['regular_price']>p['price'] else ''}</p>
<a class="btn-wa" href="{plant_message(p['name'])}" target="_blank" rel="noopener">Enquire</a></div></div></article>"""


def pot_card(m):
    fp = money(m.get("from_price"))
    sizes = ", ".join(m.get("sizes") or [])[:60]
    return f"""<a class="pot-card" href="/pots/{esc(m['product_slug'])}/">
<img loading="lazy" src="/{esc(img_url(m.get('image')))}" alt="{esc(m['model_name'])}">
<div class="info"><p class="eyebrow">{esc(m.get('collection',''))}</p>
<h3>{esc(m['model_name'])}</h3>
<p class="meta">From {fp} · {esc(sizes or 'Multiple options')}</p>
<span class="btn ghost" style="margin-top:10px;display:inline-block">Explore</span></div></a>"""


def home_page():
    pillars = [
        ("01", "Plants", "Curated plants for homes and everyday spaces.", "img/home/indoor.jpg", "/plants/", "Explore Plants"),
        ("02", "Pots & Planters", "Statement planters, eco collections and functional pots.", "images/2024_10_Milano-High-LED-1-scaled.jpg", "/pots/", "Explore Pots"),
        ("03", "Green Spaces", "Corporate greenery, rentals, landscaping and installations.", "images/2022_05_013A1506.jpg", "/green-spaces/", "Talk to Us"),
    ]
    pillar_html = "".join(
        f'<a class="pillar reveal" href="{href}"><img loading="lazy" src="/{img}" alt=""><div class="veil"></div>'
        f'<div class="content"><span class="num">{num}</span><h3>{esc(title)}</h3><p>{esc(text)}</p>'
        f'<span class="link">{cta} →</span></div></a>'
        for num, title, text, img, href, cta in pillars
    )
    featured_pots = "".join(pot_card(m) for m in ACTIVE_POTS[:6])
    curated = "".join(plant_card(p) for p in ACTIVE_PLANTS[:12])
    blog3 = BLOGS[:3]
    blog_html = ""
    for b in blog3:
        m = re.search(r'wp-content/uploads/[^"\')\s]+', b.get("content", "") or "")
        thumb = img_url(m.group(0)) if m else "images/2022_03_ALOCASIA-BLACK.jpg"
        blog_html += f"""<a class="blog-card reveal" href="/blog/{esc(b['slug'])}/"><img loading="lazy" src="/{esc(thumb)}" alt="">
<div class="body"><p class="date">{esc(b['date'][:10])}</p><h3>{esc(b['title'])}</h3></div></a>"""

    body = f"""
<section class="hero-v4" data-motion="fade-up"><div class="inner">
<span class="kicker">More than a nursery</span>
<h1>Plants for homes.<br>Pots for spaces.<br>Greenery for business.</h1>
<p class="lead">A premium plant and green-space brand — curated retail, designer planters, and enquiry-led solutions for offices, landscapes and events.</p>
<div class="hero-actions">
<a class="btn" href="/plants/">Explore Plants</a>
<a class="btn ghost" href="/pots/">Explore Pots</a>
<a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">Connect With Us</a>
</div></div></section>

<section class="container" data-motion="fade-up"><span class="eyebrow center">Three pillars</span>
<h2 class="sec center">Everything we grow and build</h2>
<div class="pillar-grid" style="margin-top:32px">{pillar_html}</div></section>

<section class="alt"><div class="container" data-motion="fade-up">
<span class="eyebrow">Pots &amp; planters</span><h2 class="sec">Collections that define a room</h2>
<p class="sub">Eco series, statement silhouettes and illuminated planters — priced from Excel, enquired on WhatsApp.</p>
<div class="collection-row">{featured_pots}</div>
<div style="margin-top:28px"><a class="btn" href="/pots/">View all pots</a></div></div></section>

<section><div class="container" data-motion="fade-up">
<span class="eyebrow">Curated plants</span><h2 class="sec">Curated for greener spaces</h2>
<p class="sub">A focused selection of our best-selling greens — not an endless catalog.</p>
<div class="rail">{curated}</div></div></section>

<section class="green-hero"><div class="container" data-motion="fade-up">
<span class="eyebrow" style="color:var(--lime)">Green spaces</span>
<h1>From a single office plant to a complete landscaped space.</h1>
<p style="opacity:.88;max-width:560px;margin-top:14px">Corporate plant rental, maintenance, commercial greenery, landscaping and event installations — enquiry-led, professionally delivered.</p>
<div class="green-paths">
<a class="green-path" href="/green-spaces/corporate-plant-rental/"><h3>Corporate plant rental</h3><p>Lobbies, living walls and workspace greens.</p></a>
<a class="green-path" href="/green-spaces/landscaping/"><h3>Landscaping</h3><p>Residential terraces to commercial landscapes.</p></a>
<a class="green-path" href="/green-spaces/maintenance/"><h3>Plant maintenance</h3><p>Keep installed greens healthy year-round.</p></a>
<a class="green-path" href="/events/"><h3>Events &amp; decor</h3><p>Weddings, corporate events and venue styling.</p></a>
</div>
<a class="btn-wa" style="margin-top:28px;display:inline-block" href="{corporate_message()}" target="_blank" rel="noopener">Connect With Us</a>
</div></section>

<section class="alt"><div class="container center" data-motion="fade-up">
<span class="eyebrow">Our work</span><h2 class="sec">Spaces we&apos;ve helped grow</h2>
<p class="sub">Corporate, hospitality, weddings and commercial installs — real projects from our nursery team.</p>
<div class="events-grid">
<a class="event reveal" href="/events/corporate/"><img loading="lazy" src="/img/home/test.jpg" alt="Corporate greenery"><div class="cap">Corporate</div></a>
<a class="event reveal" href="/events/weddings/"><img loading="lazy" src="/img/home/test.jpg" alt="Weddings"><div class="cap">Weddings</div></a>
<a class="event reveal" href="/events/landscaping/"><img loading="lazy" src="/img/home/test.jpg" alt="Landscaping"><div class="cap">Landscaping</div></a>
<a class="event reveal" href="/events/parties/"><img loading="lazy" src="/img/home/test.jpg" alt="Events"><div class="cap">Events</div></a>
</div></div></section>

<section><div class="container"><div class="reviews-placeholder reveal" data-motion="fade-up">
<h3 style="font-family:Fraunces,serif;color:var(--forest);margin-bottom:8px">Client reviews</h3>
<p>Genuine Google and client reviews will appear here — placeholder reserved for verified testimonials.</p></div></div></section>

<section class="alt"><div class="container" data-motion="fade-up">
<span class="eyebrow">Journal</span><h2 class="sec">Notes from the nursery</h2>
<div class="blog-grid">{blog_html}</div>
<a class="btn" style="margin-top:24px" href="/blog/">Read the journal</a></div></section>

<section><div class="container"><div class="cta-band reveal" data-motion="fade-up">
<h2>Let&apos;s make your space greener.</h2>
<p style="opacity:.9">Plants, pots or a full green-space brief — message us on WhatsApp.</p>
<div class="hero-actions"><a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">WhatsApp Us</a>
<a class="btn ghost" href="/events/">Explore our work</a></div></div></div></section>"""
    return page_shell(
        "Indore Nursery | Plants, Pots & Green-Space Solutions",
        "Premium plants for homes, designer pots and planters, and corporate greenery, landscaping and event decor. Enquire on WhatsApp.",
        body,
        "/",
    )


def plants_hub():
    filters = '<button type="button" class="on" data-plant-filter="all">All Plants</button>'
    tag_set = set()
    for p in ACTIVE_PLANTS:
        tag_set.update(p.get("tags") or [])
    for t in ["Indoor", "Outdoor", "Low Maintenance", "Air Purifying", "Flowering", "Succulents", "Gifting"]:
        if t in tag_set:
            filters += f'<button type="button" data-plant-filter="{esc(t)}">{esc(t)}</button>'
    grid = "".join(plant_card(p) for p in ACTIVE_PLANTS)
    body = f"""<div class="container listing-hd" data-motion="fade-up">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Plants</nav>
<h1>Shop plants</h1><p class="sub">A curated collection — lightweight filters, WhatsApp-first enquiry.</p>
<div class="filters" role="group" aria-label="Plant filters">{filters}</div>
<div class="grid" id="plant-grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))">{grid}</div></div>"""
    return page_shell("Shop Plants | Indore Nursery", "Curated indoor and outdoor plants with WhatsApp enquiry.", body, "/plants/")


def plant_detail(p):
    fact = FACTS.get(p["slug"], "")
    desc = strip_html(p.get("short_description") or p.get("description") or "")
    related = [x for x in ACTIVE_PLANTS if x["slug"] != p["slug"]][:4]
    rel = "".join(plant_card(r) for r in related)
    title = p.get("seo_title") or f"{p['name']} | Indore Nursery"
    meta = p.get("seo_description") or desc[:155]
    body = f"""<div class="container listing-hd">
<nav class="crumbs"><a href="/">Home</a> / <a href="/plants/">Plants</a> / {esc(p['name'])}</nav>
<div class="pd"><img class="main" src="/{esc(img_url(p.get('image')))}" alt="{esc(p['name'])}">
<div><h1>{esc(p['name'])}</h1>
<p class="variant-price">{money(p.get('price'))}{(' <span class="old">'+money(p.get('regular_price'))+'</span>') if p.get('regular_price') and p.get('price') and p['regular_price']>p['price'] else ''}</p>
<p style="margin-top:16px;color:var(--muted)">{esc(desc[:600])}</p>
<a class="btn-wa" href="{plant_message(p['name'])}" target="_blank" rel="noopener">Enquire on WhatsApp</a></div></div>
{f'<div class="funfact"><span class="ff-tag">Did you know?</span><p>{esc(fact)}</p></div>' if fact else ''}
<section style="margin-top:40px"><h2 class="sec">You may also like</h2><div class="grid">{rel}</div></section></div>"""
    return page_shell(title, meta, body, f"/plants/{p['slug']}/")


def pots_hub():
    by_col = {}
    for m in ACTIVE_POTS:
        by_col.setdefault(m.get("collection") or "Planters", []).append(m)
    blocks = ""
    for col, items in sorted(by_col.items()):
        cards = "".join(pot_card(m) for m in items)
        blocks += f'<section class="container" style="padding-top:40px"><span class="eyebrow">{esc(col)}</span><h2 class="sec">{esc(col)}</h2><div class="collection-row">{cards}</div></section>'
    body = f"""<div class="green-hero" style="padding-bottom:40px"><div class="container">
<h1>Pots &amp; planters</h1><p style="opacity:.88;max-width:560px;margin-top:12px">Model pages with size and colour options — select a variant, then enquire on WhatsApp with your choice.</p></div></div>{blocks}"""
    return page_shell("Pots & Planters | Indore Nursery", "Designer planters and pot collections with variant pricing.", body, "/pots/")


def pot_detail(m):
    payload = {
        "model_name": m["model_name"],
        "wa_phone": WA_PHONE,
        "sizes": m.get("sizes") or [],
        "colours": m.get("colours") or [],
        "variants": m.get("variants") or [],
    }
    variant_json = json.dumps(payload)
    desc = strip_html(m.get("short_description") or m.get("description") or "")[:700]
    title = m.get("seo_title") or f"{m['model_name']} | Indore Nursery"
    meta = m.get("seo_description") or desc[:155]
    extra = '<script src="/assets/js/pot-variants.js" defer></script>'
    body = f"""<div class="container listing-hd" id="pot-variant-root">
<nav class="crumbs"><a href="/">Home</a> / <a href="/pots/">Pots</a> / {esc(m['model_name'])}</nav>
<div class="pd"><img class="main" src="/{esc(img_url(m.get('image')))}" alt="{esc(m['model_name'])}">
<div><h1>{esc(m['model_name'])}</h1><p class="eyebrow">{esc(m.get('collection',''))}</p>
<p style="margin-top:12px;color:var(--muted)">{esc(desc)}</p>
<div class="variant-picker">
<fieldset><legend>Size</legend><div class="chip-row" data-size-options></div></fieldset>
<fieldset><legend>Colour</legend><div class="chip-row" data-colour-options></div></fieldset>
<p class="variant-price" data-variant-price>—</p><p class="old" data-variant-regular></p>
<a class="btn-wa" data-variant-wa href="{pot_message(m['model_name'])}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
</div></div></div>
<script type="application/json" id="pot-variant-data">{variant_json}</script></div>"""
    return page_shell(title, meta, body, f"/pots/{m['product_slug']}/", extra_scripts=extra)


def service_page(title, h1, lede, bullets, canonical):
    items = "".join(f"<li>{esc(b)}</li>" for b in bullets)
    body = f"""<div class="container svc-hero"><span class="eyebrow">Green Spaces</span>
<h1>{h1}</h1><p class="lede">{esc(lede)}</p><ul style="margin:18px 0 0 20px;color:var(--muted)">{items}</ul>
<a class="btn-wa" style="margin-top:24px;display:inline-block" href="{corporate_message()}" target="_blank" rel="noopener">Connect With Us</a></div>"""
    return page_shell(title, lede[:155], body, canonical)


def green_hub():
    body = f"""<div class="green-hero"><div class="container">
<h1>Green space solutions</h1><p style="opacity:.88;max-width:620px;margin-top:12px">Enquiry-led services for offices, commercial spaces, landscapes and events.</p>
<div class="green-paths">
<a class="green-path" href="/green-spaces/corporate-plant-rental/"><h3>Corporate plant rental</h3><p>Install, maintain and refresh planted workspaces.</p></a>
<a class="green-path" href="/green-spaces/maintenance/"><h3>Plant maintenance</h3><p>Ongoing care for installed greens.</p></a>
<a class="green-path" href="/green-spaces/landscaping/"><h3>Landscaping</h3><p>Design, planting and terrace gardens.</p></a>
<a class="green-path" href="/events/"><h3>Events &amp; decor</h3><p>Weddings, corporate events and venue styling.</p></a>
</div></div></div>"""
    return page_shell("Green Space Solutions | Indore Nursery", "Corporate greenery, rental, maintenance and landscaping.", body, "/green-spaces/")


def legacy_plant_page(p):
    """Preserve /plants/slug URLs for catalog items not in Excel plants sheet."""
    if p["slug"] in PLANT_BY_SLUG:
        return plant_detail(PLANT_BY_SLUG[p["slug"]])
    g = strip_html(p.get("short_description") or p.get("description") or "")
    title = f"{p['name']} | Indore Nursery"
    body = f"""<div class="container listing-hd">
<nav class="crumbs"><a href="/">Home</a> / <a href="/plants/">Plants</a> / {esc(p['name'])}</nav>
<div class="pd"><img class="main" src="/{esc(img_url(p.get('image')))}" alt="{esc(p['name'])}">
<div><h1>{esc(p['name'])}</h1>
<p class="variant-price">{money(p.get('price'))}</p>
<p style="margin-top:14px">{esc(g[:500])}</p>
<a class="btn-wa" href="{plant_message(p['name'])}" target="_blank" rel="noopener">Enquire on WhatsApp</a></div></div></div>"""
    return page_shell(title, g[:155], body, f"/plants/{p['slug']}/")


def blog_pages():
    write("blog/index.html", page_shell(
        "Journal | Indore Nursery",
        "Plant care guides and green living articles.",
        f'<div class="container listing-hd"><h1>Journal</h1><p class="sub">{len(BLOGS)} articles</p><div class="blog-grid">'
        + "".join(
            f'<a class="blog-card" href="/blog/{esc(b["slug"])}/"><div class="body"><p class="date">{esc(b["date"][:10])}</p><h3>{esc(b["title"])}</h3></div></a>'
            for b in sorted(BLOGS, key=lambda x: x["date"], reverse=True)
        )
        + "</div></div>",
        "/blog/",
    ))
    for b in BLOGS:
        c = b["content"]
        c = re.sub(
            r"https://indorenursery\.com/wp-content/uploads/([^\"\s\)\?]+)",
            lambda m: "/images/"
            + re.sub(r"-\d+x\d+(?=\.[a-zA-Z]+$)", "", m.group(1)).replace("/", "_"),
            c,
        )
        write(
            f"blog/{b['slug']}/index.html",
            page_shell(
                f"{b['title']} | Indore Nursery",
                b["title"],
                f'<div class="container listing-hd" style="max-width:860px"><nav class="crumbs"><a href="/">Home</a> / <a href="/blog/">Journal</a></nav>'
                f"<h1>{esc(b['title'])}</h1><p class=\"date\" style=\"color:var(--muted);margin:8px 0 24px\">{esc(b['date'][:10])}</p>"
                f'<div class="guide">{c}</div></div>',
                f"/blog/{b['slug']}/",
            ),
        )


def category_pages():
    by_cat = {}
    for p in CATALOG:
        for c in p.get("categories") or []:
            by_cat.setdefault(c, []).append(p)
    for c, ps in by_cat.items():
        s = slugify(c)
        cards = "".join(
            f'<a class="card" href="/plants/{esc(p["slug"])}/"><img loading="lazy" src="/{esc(img_url(p.get("image")))}"><div class="body"><h3>{esc(p["name"])}</h3><p><span class="price">{money(p.get("price"))}</span></p></div></a>'
            for p in ps
        )
        write(
            f"category/{s}/index.html",
            page_shell(
                f"{c} | Indore Nursery",
                f"Browse {c} — legacy category archive preserved for SEO.",
                f'<div class="container listing-hd"><h1>{esc(c)}</h1><div class="grid">{cards}</div></div>',
                f"/category/{s}/",
            ),
        )


def static_pages():
    write("about/index.html", page_shell(
        "About | Indore Nursery",
        "Indore Nursery — plants, pots and green-space solutions.",
        '<div class="container listing-hd"><h1>About Indore Nursery</h1><p style="margin-top:16px;max-width:680px">A working nursery serving homes, offices and events — live plants, designer planters, garden care and professional green-space installations with guidance on WhatsApp.</p></div>',
        "/about/",
    ))
    write("contact/index.html", page_shell(
        "Contact | Indore Nursery",
        "Contact Indore Nursery on WhatsApp.",
        f'<div class="container listing-hd"><h1>Contact</h1><p style="margin-top:16px"><a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">WhatsApp Us</a></p></div>',
        "/contact/",
    ))


def redirects():
    lines = []
    for leg, model in POT_LEGACY_REDIRECTS.items():
        lines.append(f"/plants/{leg}/ /pots/{model}/ 301")
    lines.append("/journal/ /blog/ 301")
    write("_redirects", "\n".join(lines) + "\n")


def sitemap():
    urls = ["/", "/plants/", "/pots/", "/green-spaces/", "/about/", "/contact/", "/blog/", "/events/"]
    urls += [f"/green-spaces/corporate-plant-rental/", "/green-spaces/landscaping/", "/green-spaces/maintenance/"]
    urls += [f"/events/{s}/" for s in ("corporate", "weddings", "parties", "landscaping")]
    urls += [f"/plants/{p['slug']}/" for p in PLANTS]
    urls += [f"/plants/{p['slug']}/" for p in CATALOG if p["slug"] not in PLANT_BY_SLUG]
    urls += [f"/pots/{m['product_slug']}/" for m in POTS]
    urls += [f"/blog/{b['slug']}/" for b in BLOGS]
    urls += [f"/category/{slugify(c)}/" for c in {c for p in CATALOG for c in p.get('categories', [])}]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    xml += "".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in sorted(set(urls)))
    xml += "</urlset>"
    write("sitemap.xml", xml)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


def copy_assets():
    src_js = os.path.join(ROOT, "parts", "suggester.js")
    if os.path.isfile(src_js):
        shutil.copy(src_js, os.path.join(SITE, "suggester.js"))


def regenerate_events():
    """Reuse existing rich event pages, re-shell via subprocess generators if present."""
    import subprocess

    for script in ("parts/gen6.py", "parts/gen8.py", "parts/gen7.py"):
        path = os.path.join(ROOT, script)
        if os.path.isfile(path):
            subprocess.run([sys.executable, path], cwd=ROOT, check=False)


def inject_shell_on_events():
    import glob

    from lib import shell as ns

    for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
        if "/assets/" in f:
            continue
        s = open(f, encoding="utf-8").read()
        if "site-header" in s:
            continue
        orig = s
        s = re.sub(r"<div class=\"announce\">.*?</header>", ns.HEAD, s, flags=re.S)
        s = re.sub(r"<footer>.*?</footer>", ns.FOOT, s, flags=re.S)
        if "/assets/css/main.css" not in s:
            s = s.replace("/style.css", "/assets/css/main.css")
        if "/assets/js/core.js" not in s and "</body>" in s:
            s = s.replace("</body>", ns.SCRIPTS + "</body>")
        if s != orig:
            open(f, "w", encoding="utf-8").write(s)


def main():
    write("index.html", home_page())
    write("plants/index.html", plants_hub())
    for p in PLANTS:
        write(f"plants/{p['slug']}/index.html", plant_detail(p))
    for p in CATALOG:
        if p["slug"] in PLANT_BY_SLUG:
            continue
        if p["slug"] in POT_LEGACY_REDIRECTS:
            continue
        write(f"plants/{p['slug']}/index.html", legacy_plant_page(p))
    write("pots/index.html", pots_hub())
    for m in POTS:
        write(f"pots/{m['product_slug']}/index.html", pot_detail(m))
    write("green-spaces/index.html", green_hub())
    write(
        "green-spaces/corporate-plant-rental/index.html",
        service_page(
            "Corporate Plant Rental | Indore Nursery",
            "Corporate plant rental &amp; greenery",
            "End-to-end planted workspaces — design, install, maintain and refresh for offices, hotels and commercial spaces.",
            [
                "Living walls and lobby statements",
                "Workstation and cabin planting",
                "Festive and launch-day refreshes",
                "Corporate plant gifting",
            ],
            "/green-spaces/corporate-plant-rental/",
        ),
    )
    write(
        "green-spaces/landscaping/index.html",
        service_page(
            "Landscaping | Indore Nursery",
            "Landscaping &amp; outdoor green spaces",
            "Residential terraces, commercial landscapes and garden planting with nursery-grown stock.",
            ["Terrace and balcony gardens", "Commercial landscape planting", "Planters and soil works", "Seasonal refreshes"],
            "/green-spaces/landscaping/",
        ),
    )
    write(
        "green-spaces/maintenance/index.html",
        service_page(
            "Plant Maintenance | Indore Nursery",
            "Plant maintenance services",
            "Keep installed plants healthy with scheduled care, replacements and seasonal adjustments.",
            ["Watering and feeding schedules", "Replacement of stressed plants", "Planter and soil checks"],
            "/green-spaces/maintenance/",
        ),
    )
    blog_pages()
    category_pages()
    static_pages()
    redirects()
    sitemap()
    copy_assets()
    regenerate_events()
    inject_shell_on_events()
    print("Site generated in site/")


if __name__ == "__main__":
    main()
