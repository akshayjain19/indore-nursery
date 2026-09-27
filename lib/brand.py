"""Brand assets: site logo and client logo marquee (local files only)."""

from __future__ import annotations

import json
import os

from lib.util import esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_SRC = "/assets/brand/indore-nursery-logo.jpg"
LOGO_FOOTER_SRC = "/assets/brand/indore-nursery-logo.png"
LOGO_ALT = "Indore Nursery"
LOGO_WIDTH = 757
LOGO_HEIGHT = 279


def _load_client_logos() -> list[dict]:
    path = os.path.join(ROOT, "data", "client-logos.json")
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    out = []
    for item in raw:
        alt = item.get("alt") or "Partner logo"
        out.append({"src": item["src"], "alt": alt})
    return out


def logo_link(extra_class: str = "", *, priority: bool = False) -> str:
    cls = "logo logo-img"
    if extra_class:
        cls += f" {extra_class}"
    pri = ' fetchpriority="high"' if priority else ""
    src = LOGO_FOOTER_SRC if "logo-footer" in extra_class else LOGO_SRC
    return (
        f'<a class="{cls}" href="/">'
        f'<img src="{src}" alt="{esc(LOGO_ALT)}" width="{LOGO_WIDTH}" height="{LOGO_HEIGHT}" '
        f'decoding="async"{pri}></a>'
    )


def _client_logo_set_html(logos: list[dict]) -> str:
    return "".join(
        f'<div class="client-logo-cell"><img loading="lazy" src="{esc(l["src"])}" alt="{esc(l["alt"])}"></div>'
        for l in logos
    )


def client_logo_marquee_html() -> str:
    logos = _load_client_logos()
    one_set = _client_logo_set_html(logos)
    return (
        '<div class="client-marquee-wrap" aria-label="Our valued clients">'
        '<div class="client-marquee-track">'
        f'<div class="client-marquee-set">{one_set}</div>'
        f'<div class="client-marquee-set" aria-hidden="true">{one_set}</div>'
        "</div></div>"
    )
