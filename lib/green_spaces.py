"""Green Spaces hub — premium B2B landing (verified copy, local imagery)."""

from __future__ import annotations

from lib.brand import client_logo_marquee_html
from lib.util import esc
from lib.whatsapp import corporate_message, event_message, landscaping_message

IMG_B2B = "images/2022_05_013A1558.jpg"
IMG_CORPORATE = "images/2025_10_Low-Maintenance-Plants-for-Busy-Professionals-For-Office-Spaces-4-600x400.jpg"
IMG_MAINTENANCE = "images/2025_07_Vertical-Garden-for-outdoor-plants.jpg"
IMG_LANDSCAPING = "images/2025_11_landscape-gardening-1-600x400.jpg"
IMG_EVENTS = "images/2025_07_WhatsApp-Image-2025-07-09-at-16.44.38_bfb03f07-768x576.jpg"

STEPS = (
    ("01", "Choose", "We understand your space, requirements and the kind of greenery that fits."),
    ("02", "Install", "Plants and planters are supplied and placed to work with the character of the space."),
    ("03", "Maintain", "Regular care, replacements and upkeep keep the greenery looking its best."),
)

SERVICES = (
    (
        "/green-spaces/corporate-plant-rental/",
        "Corporate plant rental",
        "Bring greenery into offices and commercial spaces without the commitment of owning and maintaining every plant yourself.",
        IMG_CORPORATE,
        "Office space with installed plants",
        "center 42%",
        corporate_message(),
    ),
    (
        "/green-spaces/maintenance/",
        "Plant maintenance",
        "Ongoing care for installed plants, including routine maintenance and replacement requirements.",
        IMG_MAINTENANCE,
        "Maintained vertical garden planting",
        "center 38%",
        corporate_message(),
    ),
    (
        "/green-spaces/landscaping/",
        "Landscaping",
        "From planting and planters to complete outdoor spaces, create landscapes designed around how the space is used.",
        IMG_LANDSCAPING,
        "Landscape planting and outdoor greenery",
        "center 45%",
        landscaping_message(),
    ),
    (
        "/events/",
        "Events &amp; decor",
        "Greenery for corporate events, weddings, celebrations, hospitality spaces and special occasions.",
        IMG_EVENTS,
        "Event venue with plant styling",
        "center 40%",
        event_message(),
    ),
)


def _service_block(
    href: str,
    title: str,
    text: str,
    src: str,
    alt: str,
    pos: str,
    wa: str,
    reverse: bool,
) -> str:
    mod = " gs-service--reverse" if reverse else ""
    return f"""<article class="gs-service{mod}" data-motion="fade-up">
<div class="gs-service-media"><img loading="lazy" src="/{esc(src)}" alt="{esc(alt)}" style="object-position:{esc(pos)}"></div>
<div class="gs-service-copy">
<h3>{title}</h3>
<p>{esc(text)}</p>
<div class="gs-service-actions">
<a class="btn-wa" href="{wa}" target="_blank" rel="noopener">Connect With Us</a>
<a class="btn ghost gs-learn" href="{esc(href)}">Learn More</a>
</div></div></article>"""


def green_spaces_page_body() -> str:
    wa = corporate_message()
    steps = "".join(
        f"""<li class="about-step gs-step" data-motion="fade-up">
<span class="about-step-num">{esc(num)}</span>
<h3>{esc(title)}</h3>
<p>{esc(body)}</p>
</li>"""
        for num, title, body in STEPS
    )
    services = "".join(
        _service_block(h, t, txt, src, alt, pos, wa_link, i % 2 == 1)
        for i, (h, t, txt, src, alt, pos, wa_link) in enumerate(SERVICES)
    )
    return f"""<main class="green-spaces-page">
<div class="green-hero"><div class="container">
<h1>Green space solutions</h1>
<div class="green-paths">
<a class="green-path" href="/green-spaces/corporate-plant-rental/"><h3>Corporate plant rental</h3><p>Install, maintain and refresh planted workspaces.</p></a>
<a class="green-path" href="/green-spaces/maintenance/"><h3>Plant maintenance</h3><p>Ongoing care for installed greens.</p></a>
<a class="green-path" href="/green-spaces/landscaping/"><h3>Landscaping</h3><p>Design, planting and terrace gardens.</p></a>
<a class="green-path" href="/events/"><h3>Events &amp; decor</h3><p>Weddings, corporate events and venue styling.</p></a>
</div></div></div>

<section class="gs-intro section-breathe">
<div class="container gs-intro-grid">
<div class="gs-intro-copy" data-motion="fade-up">
<h2 class="sec sec-display">Greenery, thoughtfully designed for the spaces people use every day.</h2>
<p class="gs-lede">From a single office corner to a complete landscaped environment, we provide plants, planters and ongoing care for commercial spaces, workplaces, hospitality venues and events.</p>
<nav class="gs-service-line" aria-label="Green space services">
<a href="/green-spaces/corporate-plant-rental/">Corporate plant rental</a>
<a href="/green-spaces/maintenance/">Plant maintenance</a>
<a href="/green-spaces/landscaping/">Landscaping</a>
<a href="/events/">Event &amp; venue greenery</a>
</nav>
</div></div></section>

<section class="gs-process alt">
<div class="container">
<div class="about-section-head center" data-motion="fade-up">
<h2 class="sec sec-display">From installation to ongoing care</h2>
</div>
<ol class="about-steps gs-steps">{steps}</ol>
</div></section>

<section class="gs-b2b section-breathe">
<div class="container gs-b2b-split">
<div class="gs-b2b-media" data-motion="fade-up">
<img loading="lazy" src="/{esc(IMG_B2B)}" alt="Installed greenery in a commercial setting" style="object-position:center 44%">
</div>
<div class="gs-b2b-copy" data-motion="fade-up">
<h2 class="sec sec-display">Green spaces that work as hard as the spaces around them.</h2>
<p>Offices, hotels, restaurants, commercial properties and event venues often need greenery that looks good without becoming another thing to manage. We take care of the plants, planters and ongoing maintenance so your space stays green and well-presented.</p>
</div></div></section>

<section class="gs-services">
<div class="container">
<div class="gs-service-list">{services}</div>
</div></section>

<section class="clients-band gs-clients"><div class="container center" data-motion="fade-up">
<span class="eyebrow">Our clients</span>
<h2 class="sec sec-display">Spaces we&apos;ve helped grow</h2>
{client_logo_marquee_html()}</div></section>

<section class="section-breathe gs-cta-wrap"><div class="container"><div class="cta-band reveal" data-motion="fade-up">
<h2>Have a space in mind?</h2>
<p>Tell us what you&apos;re working with, and we&apos;ll help you figure out the greenery.</p>
<div class="hero-actions"><a class="btn-wa" href="{wa}" target="_blank" rel="noopener">Connect With Us</a></div>
</div></div></section></main>"""
