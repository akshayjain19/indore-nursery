"""Nursery location — maps embed, directions, and homepage visit section."""

from __future__ import annotations

from urllib.parse import quote

from lib.config import (
    NURSERY_ADDRESS_CITY,
    NURSERY_ADDRESS_LINE1,
    NURSERY_ADDRESS_LINE2,
    NURSERY_MAP_DESTINATION,
    SITE_EMAIL,
    TEL_URI,
    WA_PHONE_DISPLAY,
)
from lib.util import esc
from lib.whatsapp import general_message


def google_maps_directions_url() -> str:
    dest = quote(NURSERY_MAP_DESTINATION)
    return f"https://www.google.com/maps/dir/?api=1&destination={dest}"


def google_maps_embed_url() -> str:
    q = quote(NURSERY_MAP_DESTINATION)
    return f"https://www.google.com/maps?q={q}&hl=en&z=16&output=embed"


def homepage_visit_section_html() -> str:
    directions = google_maps_directions_url()
    embed = google_maps_embed_url()
    return f"""<section class="visit-editorial alt" data-motion="fade-up"><div class="container visit-layout">
<div class="visit-copy">
<span class="eyebrow">Visit us</span>
<h2 class="sec sec-display">Come see us.</h2>
<address class="visit-address">
{NURSERY_ADDRESS_LINE1}<br>
{NURSERY_ADDRESS_LINE2}<br>
{esc(NURSERY_ADDRESS_CITY)}
</address>
<div class="visit-actions">
<a class="btn" href="{esc(directions)}" target="_blank" rel="noopener noreferrer">Get Directions</a>
<a class="btn-wa" href="{general_message()}" target="_blank" rel="noopener">WhatsApp</a>
<a class="btn ghost visit-ghost" href="{TEL_URI}">Call</a>
<a class="btn ghost visit-ghost" href="mailto:{SITE_EMAIL}">Email</a>
</div></div>
<div class="visit-map-wrap">
<iframe class="visit-map" title="Indore Nursery on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen src="{esc(embed)}"></iframe>
</div></div></section>"""
