#!/usr/bin/env python3
"""Static site generator — premium IA, Excel-driven products, SEO-safe legacy URLs."""

from __future__ import annotations

import json
import html as html_lib
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lib.brand import client_logo_marquee_html
from lib.config import PLANTS_JSON, POTS_JSON, SITE_URL, WA_PHONE
from lib.presentation import (
    blog_featured_image,
    clean_plant_name,
    homepage_journal_posts,
    plant_teaser,
    pot_card_price_line,
    pot_variant_payload,
)
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

HOME_POT_SHOWCASE_SLUGS = (
    "milano-high-illuminated-planters",
    "tokyo-illuminated-round-planters",
    "venice-planter",
    "verona-eco",
)

HOME_WORK_PORTFOLIO = (
    {
        "src": "images/2025_07_Vertical-Garden-for-outdoor-plants.jpg",
        "alt": "Vertical garden and living wall installation with mixed foliage",
        "category": "Corporate",
        "title": "Living wall installation",
        "href": "/green-spaces/corporate-plant-rental/",
        "featured": True,
    },
    {
        "src": "images/2025_07_zen-garden.jpg",
        "alt": "Completed zen garden landscape with stone, water and planting",
        "category": "Landscaping",
        "title": "Landscape garden",
        "href": "/green-spaces/landscaping/",
        "featured": False,
    },
    {
        "src": "img/home/outdoor.jpg",
        "alt": "Terrace planting at a hospitality property with palms and seasonal colour",
        "category": "Hospitality",
        "title": "Terrace greenery",
        "href": "/events/corporate/",
        "featured": False,
    },
)

WORK_CATEGORY_LINKS = (
    ("Corporate", "/events/corporate/"),
    ("Landscaping", "/green-spaces/landscaping/"),
    ("Events", "/events/"),
    ("Weddings", "/events/weddings/"),
    ("Hospitality", "/events/corporate/"),
    ("Commercial", "/events/corporate/"),
)


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
    name = clean_plant_name(p["name"])
    desc = plant_teaser(p)
    tags = ",".join(p.get("tags") or [])
    return f"""<article class="plant-card-v2" data-tags="{esc(tags)}" data-motion="fade-up">
<a href="/plants/{esc(p['slug'])}/" class="pic"><img loading="lazy" src="/{esc(img_url(p.get('image')))}" alt="{esc(name)}"></a>
<div class="info"><h3><a href="/plants/{esc(p['slug'])}/">{esc(name)}</a></h3>
<p class="desc">{esc(desc)}</p>
<div class="foot"><p><span class="price">{money(p.get('price'))}</span>{(' <span class="old">'+money(p.get('regular_price'))+'</span>') if p.get('regular_price') and p.get('price') and p['regular_price']>p['price'] else ''}</p>
<a class="btn-wa" href="{plant_message(name)}" target="_blank" rel="noopener">Enquire</a></div></div></article>"""


def homepage_featured_pots():
    by_slug = {m["product_slug"]: m for m in ACTIVE_POTS}
    picked = []
    for slug in HOME_POT_SHOWCASE_SLUGS:
        m = by_slug.get(slug)
        if m:
            picked.append(m)
    if len(picked) < 4:
        for m in ACTIVE_POTS:
            if m not in picked:
                picked.append(m)
            if len(picked) >= 4:
                break
    return picked[:4]


def pot_card(m, featured=False, homepage=False):
    name = clean_plant_name(m["model_name"])
    price_line = pot_card_price_line(m)
    cls = "pot-card pot-card-v2"
    if homepage:
        cls += " pot-card-home"
    elif featured:
        cls += " pot-card-featured"
    return f"""<article class="{cls}" data-motion="fade-up">
<a class="pot-card-link" href="/pots/{esc(m['product_slug'])}/">
<img loading="lazy" src="/{esc(img_url(m.get('image')))}" alt="{esc(name)}">
<div class="info"><p class="eyebrow">{esc(m.get('collection',''))}</p>
<h3>{esc(name)}</h3>
<p class="meta">{price_line}</p></div></a>
<div class="pot-card-actions">
<a class="btn ghost" href="/pots/{esc(m['product_slug'])}/">Explore</a>
<a class="btn-wa" href="{pot_message(name)}" target="_blank" rel="noopener">WhatsApp</a>
</div></article>"""


def work_portfolio_piece(piece: dict) -> str:
    return f"""<a class="work-piece" href="{esc(piece['href'])}">
<div class="work-piece-media">
<img loading="lazy" src="/{esc(piece['src'])}" alt="{esc(piece['alt'])}">
<div class="work-piece-overlay">
<span class="work-piece-cat">{esc(piece['category'])}</span>
<span class="work-piece-title">{esc(piece['title'])}</span>
</div></div></a>"""


def homepage_work_portfolio_html() -> str:
    featured = next(p for p in HOME_WORK_PORTFOLIO if p.get("featured"))
    stack = [p for p in HOME_WORK_PORTFOLIO if not p.get("featured")]
    cats = []
    for i, (label, href) in enumerate(WORK_CATEGORY_LINKS):
        if i:
            cats.append('<span class="work-cat-sep" aria-hidden="true">·</span>')
        cats.append(f'<a href="{esc(href)}">{esc(label)}</a>')
    cat_line = "".join(cats)
    stack_html = "".join(work_portfolio_piece(p) for p in stack)
    mobile_html = "".join(work_portfolio_piece(p) for p in HOME_WORK_PORTFOLIO)
    return f"""<div class="work-portfolio" data-motion="fade-up">
<div class="work-portfolio-intro">
<span class="eyebrow">Our work</span>
<h2 class="sec sec-display">Spaces we&apos;ve helped grow</h2>
</div>
<div class="work-portfolio-grid work-portfolio-grid-desktop">
<a class="work-piece work-piece-feature" href="{esc(featured['href'])}">
<div class="work-piece-media">
<img loading="lazy" src="/{esc(featured['src'])}" alt="{esc(featured['alt'])}">
<div class="work-piece-overlay">
<span class="work-piece-cat">{esc(featured['category'])}</span>
<span class="work-piece-title">{esc(featured['title'])}</span>
</div></div></a>
<div class="work-portfolio-stack">{stack_html}</div>
</div>
<div class="work-portfolio-grid work-portfolio-grid-mobile">{mobile_html}</div>
<div class="work-portfolio-foot">
<p class="work-cat-inline">{cat_line}</p>
<a class="btn" href="/events/">Explore our work</a>
</div></div>"""


def home_page():
    pillars = [
        ("01", "Plants", "img/home/indoor.jpg", "/plants/", "Explore Plants"),
        ("02", "Pots & Planters", "images/2024_10_Milano-High-LED-1-scaled.jpg", "/pots/", "Explore Pots"),
        ("03", "Green Spaces", "images/2022_05_013A1506.jpg", "/green-spaces/", "Talk to Us"),
    ]
    pillar_html = "".join(
        f'<a class="pillar reveal" href="{href}"><img loading="lazy" src="/{img}" alt=""><div class="veil"></div>'
        f'<div class="content"><span class="num">{num}</span><h3>{esc(title)}</h3>'
        f'<span class="link">{cta} →</span></div></a>'
        for num, title, img, href, cta in pillars
    )
    featured_pots = "".join(pot_card(m, homepage=True) for m in homepage_featured_pots())
    curated = "".join(plant_card(p) for p in ACTIVE_PLANTS[:12])
    blog3 = homepage_journal_posts(BLOGS, limit=3)
    blog_html = ""
    for b in blog3:
        thumb = blog_featured_image(b)
        blog_html += f"""<a class="blog-card blog-card-home reveal" href="/blog/{esc(b['slug'])}/" data-motion="fade-up"><div class="blog-card-img"><img loading="lazy" src="/{esc(thumb)}" alt="{esc(b['title'])}"></div>
<div class="body"><p class="date">{esc(b['date'][:10])}</p><h3>{esc(b['title'])}</h3></div></a>"""

    body = f"""
<section class="hero-v4 hero-editorial" data-motion="fade-up"><div class="inner">
<span class="kicker">More than a nursery</span>
<h1>Plants for homes.<br>Pots for spaces.<br>Greenery for business.</h1>
<p class="lead">Indoor and outdoor plants, designer planters, and green-space styling for homes, offices and events across Indore.</p>
<div class="hero-actions">
<a class="btn" href="/plants/">Explore Plants</a>
<a class="btn ghost" href="/pots/">Explore Pots</a>
<a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">Connect With Us</a>
</div></div></section>

<section class="section-breathe pillar-intro"><div class="container" data-motion="fade-up">
<h2 class="sec center sec-display">Everything we grow and build</h2>
<div class="pillar-grid pillar-grid-editorial">{pillar_html}</div></div></section>

<section class="pots-editorial alt"><div class="container">
<div class="split-head" data-motion="fade-up">
<div><span class="eyebrow">Pots &amp; planters</span><h2 class="sec sec-display">Collections that define a room</h2></div>
<a class="btn" href="/pots/">View all pots</a></div>
<div class="pots-showcase-grid">{featured_pots}</div></div></section>

<section class="section-breathe"><div class="container">
<div class="split-head" data-motion="fade-up"><div><span class="eyebrow">Curated plants</span>
<h2 class="sec sec-display">Curated for greener spaces</h2></div>
<a class="btn ghost" href="/plants/">Shop all plants</a></div>
<div class="carousel-shell" data-carousel="plants">
<button type="button" class="carousel-arrow prev" aria-label="Previous plants">&#8249;</button>
<div class="plant-rail">{curated}</div>
<button type="button" class="carousel-arrow next" aria-label="Next plants">&#8250;</button>
</div></div></section>

<section class="green-spaces-editorial" data-motion="fade-up">
<div class="green-spaces-bg" aria-hidden="true"></div>
<div class="container green-spaces-inner">
<span class="eyebrow light">Green spaces</span>
<h2 class="sec-display light">From one office plant to a fully landscaped space.</h2>
<nav class="green-nav" aria-label="Green space services">
<a href="/green-spaces/corporate-plant-rental/"><span>01</span><strong>Corporate plant rental</strong><small>Lobbies, living walls, workspace greens</small></a>
<a href="/green-spaces/maintenance/"><span>02</span><strong>Plant maintenance</strong><small>Care for installed plant programs</small></a>
<a href="/green-spaces/landscaping/"><span>03</span><strong>Landscaping</strong><small>Terraces, gardens, commercial landscapes</small></a>
<a href="/events/"><span>04</span><strong>Events &amp; decor</strong><small>Weddings, venues, brand experiences</small></a>
</nav>
<a class="btn-wa btn-wa-light" href="{corporate_message()}" target="_blank" rel="noopener">Connect With Us</a>
</div></section>

<section class="work-editorial alt"><div class="container">
{homepage_work_portfolio_html()}</div></section>

<section class="clients-band"><div class="container center" data-motion="fade-up">
<h2 class="sec sec-display">Spaces we&apos;ve helped grow</h2>
{client_logo_marquee_html()}</div></section>

<section class="journal-editorial alt"><div class="container" data-motion="fade-up">
<div class="journal-head"><span class="eyebrow">Journal</span><h2 class="sec sec-display">Notes from the nursery</h2></div>
<div class="blog-grid blog-grid-home">{blog_html}</div>
<div class="journal-actions"><a class="btn" href="/blog/">Read the journal</a></div></div></section>

<section class="section-breathe"><div class="container"><div class="cta-band reveal" data-motion="fade-up">
<h2>Let&apos;s make your space greener.</h2>
<p>Plants, pots or a full green-space brief — message us on WhatsApp.</p>
<div class="hero-actions"><a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">WhatsApp Us</a>
<a class="btn ghost" href="/events/">Explore our work</a></div></div></div></section>"""
    return page_shell(
        "Best Plant Nursery in Indore | Plants, Pots & Green Spaces",
        "Indore Nursery — indoor & outdoor plants, designer pots, corporate greenery, landscaping and event decor. Enquire on WhatsApp.",
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
<h1>Shop plants</h1>
<div class="filters" role="group" aria-label="Plant filters">{filters}</div>
<div class="grid" id="plant-grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))">{grid}</div></div>"""
    return page_shell("Shop Plants | Indore Nursery", "Curated indoor and outdoor plants with WhatsApp enquiry.", body, "/plants/")


def plant_detail(p):
    fact = FACTS.get(p["slug"], "")
    name = clean_plant_name(p["name"])
    desc = plant_teaser(p, limit=600)
    related = [x for x in ACTIVE_PLANTS if x["slug"] != p["slug"]][:4]
    rel = "".join(plant_card(r) for r in related)
    title = p.get("seo_title") or f"{p['name']} | Indore Nursery"
    meta = p.get("seo_description") or desc[:155]
    body = f"""<div class="container listing-hd">
<nav class="crumbs"><a href="/">Home</a> / <a href="/plants/">Plants</a> / {esc(name)}</nav>
<div class="pd"><img class="main" src="/{esc(img_url(p.get('image')))}" alt="{esc(name)}">
<div><h1>{esc(name)}</h1>
<p class="variant-price">{money(p.get('price'))}{(' <span class="old">'+money(p.get('regular_price'))+'</span>') if p.get('regular_price') and p.get('price') and p['regular_price']>p['price'] else ''}</p>
<p style="margin-top:16px;color:var(--muted);max-width:52ch">{esc(desc)}</p>
<a class="btn-wa" href="{plant_message(name)}" target="_blank" rel="noopener">Enquire on WhatsApp</a></div></div>
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
<h1>Pots &amp; planters</h1></div></div>{blocks}"""
    return page_shell("Pots & Planters | Indore Nursery", "Designer planters and pot collections with variant pricing.", body, "/pots/")


def pot_detail(m):
    payload = pot_variant_payload(m)
    payload["wa_phone"] = WA_PHONE
    variant_json = json.dumps(payload)
    desc = html_lib.unescape(strip_html(m.get("short_description") or m.get("description") or "")[:700])
    name = clean_plant_name(m["model_name"])
    title = m.get("seo_title") or f"{name} | Indore Nursery"
    meta = m.get("seo_description") or desc[:155]
    extra = '<script src="/assets/js/pot-variants.js" defer></script>'
    size_fs = '<fieldset data-size-field><legend>Size</legend><div class="chip-row" data-size-options></div></fieldset>'
    colour_fs = '<fieldset data-colour-field><legend>Colour</legend><div class="chip-row" data-colour-options></div></fieldset>'
    body = f"""<div class="container listing-hd" id="pot-variant-root">
<nav class="crumbs"><a href="/">Home</a> / <a href="/pots/">Pots</a> / {esc(name)}</nav>
<div class="pd"><img class="main" src="/{esc(img_url(m.get('image')))}" alt="{esc(name)}">
<div><h1>{esc(name)}</h1><p class="eyebrow">{esc(m.get('collection',''))}</p>
<p style="margin-top:12px;color:var(--muted);max-width:52ch">{esc(desc)}</p>
<div class="variant-picker">
{size_fs}
{colour_fs}
<p class="variant-price" data-variant-price>—</p><p class="old" data-variant-regular></p>
<a class="btn-wa" data-variant-wa href="{pot_message(name)}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
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
<h1>Green space solutions</h1>
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
            f'<a class="blog-card" href="/blog/{esc(b["slug"])}/"><div class="blog-card-img"><img loading="lazy" src="/{esc(blog_featured_image(b))}" alt="{esc(b["title"])}"></div>'
            f'<div class="body"><p class="date">{esc(b["date"][:10])}</p><h3>{esc(b["title"])}</h3></div></a>'
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
        orig = s
        if "site-header" in s or '<div class="announce"' in s:
            s = re.sub(
                r'<div class="announce"[^>]*>.*?</header>',
                ns.HEAD,
                s,
                count=1,
                flags=re.S,
            )
        if "<footer>" in s:
            s = re.sub(r"<footer>.*?</footer>", ns.FOOT, s, count=1, flags=re.S)
        if "/assets/css/main.css" not in s:
            s = s.replace("/style.css", "/assets/css/main.css")
        if "/assets/js/core.js" not in s and "</body>" in s:
            s = s.replace("</body>", ns.SCRIPTS + "</body>")
        # Drop legacy duplicate float from old catalog templates.
        s = re.sub(
            r'<a class="wa-float" href="https://wa\.me/918305449559\?text=Hi%20Indore%20Nursery!"[^>]*>.*?</a>\s*',
            "",
            s,
            flags=re.S,
        )
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
