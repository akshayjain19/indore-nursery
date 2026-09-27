from lib.config import SITE_NAME, SITE_URL, TEL_URI, WA_PHONE, WA_PHONE_DISPLAY
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
    '<a class="logo" href="/">Indore<span>Nursery</span></a>'
    '<nav class="main" aria-label="Primary">'
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

FOOT = (
    "<footer><div class=\"container foot\">"
    '<div class="fbrand">'
    '<a class="logo" href="/">Indore<span>Nursery</span></a>'
    "<p>Plants for homes. Pots for spaces. Greenery for businesses — with expert guidance on WhatsApp.</p>"
    "</div>"
    '<div class="fcols">'
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
    "<span>Indore, Madhya Pradesh</span>"
    "</div></div>"
    '<div class="client-strip" aria-label="Clients">'
    "<b>PRIDE Hotels</b><b>&#2360;&#2371;&#2332;&#2344;</b><b>SAJDHAJ</b>"
    "<b>&#2354;&#2325;&#2381;&#2359;&#2381;&#2350;&#2368; Sweets</b><b>Kashiwal Honda</b>"
    "</div>"
    f'<div class="copy">&copy; 2026 {esc(SITE_NAME)} &middot; All rights reserved</div>'
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
