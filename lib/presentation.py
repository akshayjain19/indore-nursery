"""Customer-facing copy and media helpers (does not mutate source/Excel data)."""

from __future__ import annotations

import html as html_lib
import re

from lib.util import img_url, money, strip_html

_PLACEHOLDER_DIMS = frozenset({"standard", ""})


def is_placeholder_dimension(value: str | None) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in _PLACEHOLDER_DIMS


def clean_plant_name(name: str) -> str:
    s = html_lib.unescape(name or "")
    s = re.sub(r"\s+", " ", s).strip()
    fixes = {
        "(senseveria)": "(Sansevieria)",
        "senseveria": "Sansevieria",
        "Spathiphylum": "Spathiphyllum",
        "Dracena": "Dracaena",
        "echivera": "Echeveria",
        "succullent": "succulent",
    }
    for a, b in fixes.items():
        s = re.sub(re.escape(a), b, s, flags=re.I)
    return s


def plant_teaser(p, limit: int = 130) -> str:
    raw = strip_html(p.get("short_description") or p.get("description") or "")
    raw = html_lib.unescape(raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    if not raw:
        return "Curated at our nursery — enquire for availability and guidance."
    low = raw.lower()
    if low.startswith("fertilizer") or "repotting :" in low[:100] or raw.count(":") > 2:
        parts = re.split(r"(?<=[.!?])\s+", raw)
        for part in parts:
            part = part.strip()
            if 20 < len(part) <= limit and "fertiliz" not in part.lower()[:20]:
                return part[:limit].rstrip() + ("…" if len(part) > limit else "")
        return "A nursery favourite — message us on WhatsApp for details."
    if len(raw) <= limit:
        return raw
    cut = raw[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;") + "…"


def blog_featured_image(b) -> str:
    content = b.get("content") or ""
    for pat in (
        r'<img[^>]+src=["\'](https://indorenursery\.com/wp-content/uploads/[^"\']+)["\']',
        r'<img[^>]+src=["\'](/wp-content/uploads/[^"\']+)["\']',
        r'<img[^>]+src=["\'](/images/[^"\']+)["\']',
        r"(https://indorenursery\.com/wp-content/uploads/[^\s\"'\)>]+)",
        r"(/wp-content/uploads/[^\s\"'\)>]+)",
        r"(wp-content/uploads/[^\s\"'\)>]+)",
    ):
        m = re.search(pat, content, re.I)
        if m:
            return img_url(m.group(1))
    return img_url("")


def homepage_journal_posts(blogs: list, limit: int = 3, pool: int = 40) -> list:
    """Homepage journal: lead with the latest post, plus distinct featured images."""
    from lib.util import FALLBACK_IMAGE

    by_date = sorted(blogs, key=lambda x: x.get("date", ""), reverse=True)
    recent = by_date[:pool]
    chosen: list = []
    used_images: set[str] = set()

    if by_date:
        lead = by_date[0]
        chosen.append(lead)
        used_images.add(blog_featured_image(lead))

    for b in recent:
        if len(chosen) >= limit:
            break
        if b in chosen:
            continue
        thumb = blog_featured_image(b)
        if thumb != FALLBACK_IMAGE and thumb not in used_images:
            chosen.append(b)
            used_images.add(thumb)

    if len(chosen) < limit:
        for b in by_date:
            if len(chosen) >= limit:
                break
            thumb = blog_featured_image(b)
            if b in chosen:
                continue
            if thumb != FALLBACK_IMAGE and thumb not in used_images:
                chosen.append(b)
                used_images.add(thumb)

    for b in by_date:
        if len(chosen) >= limit:
            break
        if b not in chosen:
            chosen.append(b)

    return chosen[:limit]


def pot_customer_sizes(model: dict) -> list[str]:
    sizes = []
    for v in model.get("variants") or []:
        if not v.get("active"):
            continue
        s = str(v.get("size") or "").strip()
        if not is_placeholder_dimension(s) and s not in sizes:
            sizes.append(s)
    if not sizes:
        for v in model.get("variants") or []:
            if v.get("active"):
                s = str(v.get("size") or "").strip()
                if s and s not in sizes:
                    sizes.append(s)
    return sorted(sizes, key=lambda x: (len(x), x))


def pot_customer_colours(model: dict) -> list[str]:
    colours = []
    for v in model.get("variants") or []:
        if not v.get("active"):
            continue
        c = str(v.get("colour") or "").strip()
        if not is_placeholder_dimension(c) and c not in colours:
            colours.append(c)
    return sorted(colours, key=str.lower)


def pot_has_choice_variants(model: dict) -> bool:
    sizes = pot_customer_sizes(model)
    colours = pot_customer_colours(model)
    if len(sizes) > 1:
        return True
    if len(colours) > 0:
        return True
    active = [v for v in model.get("variants") or [] if v.get("active")]
    if len(active) > 1:
        return True
    return False


def pot_card_price_line(model: dict) -> str:
    fp = model.get("from_price")
    if pot_has_choice_variants(model):
        base = f"From {money(fp)}" if fp else "Enquire for pricing"
        return f'{base} · <span class="pot-tag">Multiple sizes &amp; colours</span>'
    return f"From {money(fp)}" if fp else "Enquire for pricing"


def pot_variant_payload(model: dict) -> dict:
    """JSON payload for PDP script — customer labels only in display arrays."""
    sizes = pot_customer_sizes(model)
    colours = pot_customer_colours(model)
    if not sizes:
        active = [v for v in model.get("variants") or [] if v.get("active")]
        if active:
            sizes = [str(active[0].get("size") or "")]
    if not colours:
        colours = []
    real_sizes = [s for s in sizes if not is_placeholder_dimension(s)]
    show_sizes = len(real_sizes) > 1
    show_colours = len(colours) > 0
    return {
        "model_name": model["model_name"],
        "sizes": real_sizes if real_sizes else sizes,
        "colours": colours,
        "show_sizes": show_sizes,
        "show_colours": show_colours,
        "from_price": model.get("from_price"),
        "variants": model.get("variants") or [],
    }
