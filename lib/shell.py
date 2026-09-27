from lib.brand import logo_link
from lib.config import (
    NURSERY_ADDRESS_CITY,
    NURSERY_ADDRESS_LINE1,
    NURSERY_ADDRESS_LINE2,
    NURSERY_MAP_DESTINATION,
    SITE_EMAIL,
    SITE_NAME,
    SITE_URL,
    TEL_URI,
    WA_PHONE_DISPLAY,
)
from lib.location import google_maps_directions_url
from lib.util import esc, wa_link
from lib.whatsapp import general_message

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;0,700;1,500;1,600&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">'
)

NAV = [
    ("Plants", "/plants/"),
    ("Pots", "/pots/"),
    ("Green Spaces", "/green-spaces/"),
    ("Events & Decor", "/events/"),
    ("About", "/about/"),
    ("Journal", "/blog/"),
]

ANNOUNCE = (
    '<div class="announce" aria-label="Announcements">'
    '<div class="an-track">'
    '<span class="an-pill">Free delivery on qualifying orders</span>'
    '<span class="an-pill">Plants, pots &amp; green-space solutions</span>'
    f'<span class="an-pill"><a href="{TEL_URI}">{esc(WA_PHONE_DISPLAY)}</a></span>'
    '<span class="an-pill">Events &amp; corporate greenery</span>'
    "</div></div>"
)

HEAD = (
    ANNOUNCE
    + '<header class="site-header"><div class="container hd">'
    '<button class="burger" type="button" aria-label="Open menu" aria-expanded="false">&#9776;</button>'
    + logo_link(priority=True)
    + '<nav class="main" aria-label="Primary">'
    + "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    + "</nav>"
    f'<a class="btn-wa hd-wa" href="{general_message()}" target="_blank" rel="noopener">Connect</a>'
    "</div></header>"
    '<div class="drawer" id="nav-drawer" aria-hidden="true">'
    '<button class="x" type="button" aria-label="Close menu">&#10005;</button>'
    '<a href="/">Home</a>'
    + "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    + '<a href="/contact/">Contact</a>'
    f'<a class="btn-wa drawer-wa" href="{general_message()}" target="_blank" rel="noopener">WhatsApp Us</a>'
    "</div>"
    f'<a class="wa-float" href="{general_message()}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">&#128994;</a>'
    '<button id="top" type="button" aria-label="Back to top">&#8593;</button>'
)

FOOT_LINKS = (
    ("Plants", "/plants/"),
    ("Pots", "/pots/"),
    ("Green Spaces", "/green-spaces/"),
    ("Events & Decor", "/events/"),
    ("About", "/about/"),
    ("Journal", "/blog/"),
    ("Contact", "/contact/"),
)

FOOT_ADDRESS = (
    f'<address class="footer-address" itemscope itemtype="https://schema.org/PostalAddress">'
    f'<span itemprop="streetAddress">{esc(NURSERY_ADDRESS_LINE1)} {esc(NURSERY_ADDRESS_LINE2)}</span><br>'
    f'<span itemprop="addressLocality">Indore</span>, '
    f'<span itemprop="addressRegion">Madhya Pradesh</span> '
    f'<span itemprop="postalCode">452011</span>'
    f"</address>"
)

FOOT = (
    '<footer itemscope itemtype="https://schema.org/GardenStore">'
    f'<meta itemprop="name" content="{esc(SITE_NAME)}">'
    f'<meta itemprop="email" content="{esc(SITE_EMAIL)}">'
    f'<meta itemprop="telephone" content="{esc(WA_PHONE_DISPLAY)}">'
    f'<link itemprop="url" href="https://indorenursery.com/">'
    "<div class=\"container foot\">"
    '<div class="fbrand">'
    + logo_link("logo-footer")
    + "<p>Plants for homes. Pots for spaces. Greenery for businesses.</p>"
    + "</div>"
    + '<div class="fcols">'
    "<div><h4>Explore</h4>"
    + "".join(f'<a href="{h}">{esc(l)}</a>' for l, h in FOOT_LINKS)
    + "</div>"
    "<div><h4>Green Spaces</h4>"
    '<a href="/green-spaces/corporate-plant-rental/">Corporate plant rental</a>'
    '<a href="/green-spaces/landscaping/">Landscaping</a>'
    '<a href="/green-spaces/maintenance/">Plant maintenance</a>'
    "</div>"
    "<div><h4>Contact</h4>"
    f'<a href="{general_message()}" target="_blank" rel="noopener">{esc(WA_PHONE_DISPLAY)} (WhatsApp)</a>'
    f'<a href="{TEL_URI}">Call us</a>'
    f'<a href="mailto:{SITE_EMAIL}">{esc(SITE_EMAIL)}</a>'
    f'<a href="{google_maps_directions_url()}" target="_blank" rel="noopener noreferrer">Get directions</a>'
    + FOOT_ADDRESS
    + "</div></div>"
    + f'<div class="copy">&copy; 2026 {esc(SITE_NAME)} &middot; All rights reserved</div>'
    "</div></footer>"
)

SCRIPTS = (
    '<script src="/assets/js/core.js" defer></script>'
    '<script src="/assets/js/motion.js" defer></script>'
)


def page_head(title, description, canonical_path="", extra_head=""):
    canon = f"{SITE_URL}{canonical_path}" if canonical_path else SITE_URL + "/"
    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(title)}</title>"
        f'<meta name="description" content="{esc(description)}">'
        f'<link rel="canonical" href="{esc(canon)}">'
        f"{FONTS}"
        f'<link rel="stylesheet" href="/assets/css/main.css">'
        f"{extra_head}</head><body>"
    )


def page_shell(title, description, body, canonical_path="", extra_scripts="", extra_head=""):
    return (
        page_head(title, description, canonical_path, extra_head)
        + HEAD
        + body
        + FOOT
        + SCRIPTS
        + extra_scripts
        + "</body></html>"
    )
