"""Brand assets: site logo and client logo marquee (local files only)."""

from __future__ import annotations

import json
import os

from lib.util import esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_SRC = "/assets/brand/indore-nursery-logo.jpg"
LOGO_ALT = "Indore Nursery"


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
    return (
        f'<a class="{cls}" href="/">'
        f'<img src="{LOGO_SRC}" alt="{esc(LOGO_ALT)}" width="790" height="325" '
        f'decoding="async"{pri}></a>'
    )


def client_logo_marquee_html() -> str:
    logos = _load_client_logos()
    cells = "".join(
        f'<div class="client-logo-cell"><img loading="lazy" src="{esc(l["src"])}" alt="{esc(l["alt"])}"></div>'
        for l in logos
    )
    return (
        '<div class="client-marquee-wrap" aria-label="Our valued clients">'
        f'<div class="client-marquee-track">{cells}{cells}</div></div>'
    )
