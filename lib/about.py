"""About page — editorial brand story (verified copy only)."""

from __future__ import annotations

from lib.brand import client_logo_marquee_html
from lib.location import homepage_visit_section_html
from lib.util import esc
from lib.whatsapp import general_message

# Genuine repository photography — distinct per section
IMG_HERO = "images/2025_10_Indore-nursery-3-768x1152.jpg"
IMG_INTRO = "img/home/outdoor.jpg"
IMG_PLANTS = "img/home/indoor.jpg"
IMG_GREEN = "images/2025_07_Vertical-Garden-for-outdoor-plants.jpg"
IMG_EVENTS = "images/2025_07_WhatsApp-Image-2025-07-09-at-16.44.38_bfb03f07-768x576.jpg"
IMG_HOME = "img/home/succulents.jpg"
IMG_BUSINESS = "images/2022_05_013A1558.jpg"

OFFERINGS = (
    (
        "/plants/",
        "Plants",
        "Curated plants for homes and everyday spaces.",
        IMG_PLANTS,
        "Indoor and outdoor plants at Indore Nursery",
        "center 45%",
    ),
    (
        "/pots/",
        "Pots &amp; Planters",
        "Planters and pots for different spaces and requirements.",
        "images/2024_07_jpeg-optimizer_Integrated-Planters.jpg",
        "Planters integrated into an indoor space",
        "center 55%",
    ),
    (
        "/green-spaces/",
        "Green Spaces",
        "Corporate greenery, plant rental, maintenance and landscaping.",
        IMG_GREEN,
        "Vertical garden and installed greenery",
        "center 40%",
    ),
    (
        "/events/",
        "Events &amp; Decor",
        "Greenery and plant styling for weddings, celebrations and events.",
        IMG_EVENTS,
        "Event space with plant styling",
        "center 42%",
    ),
)

STEPS = (
    ("01", "Understand the space", "We start with how the space is used — light, layout and what you want it to feel like."),
    ("02", "Recommend what fits", "Plants, planters or a fuller green-space plan — matched to your setting, not a generic list."),
    ("03", "Make it happen", "Supply, delivery and setup when you need it — from a single planter to a full install."),
)


def _offer_block(href: str, title: str, text: str, src: str, alt: str, pos: str, reverse: bool) -> str:
    mod = " about-offer--reverse" if reverse else ""
    return f"""<a class="about-offer{mod}" href="{esc(href)}" data-motion="fade-up">
<div class="about-offer-media"><img loading="lazy" src="/{esc(src)}" alt="{esc(alt)}" style="object-position:{esc(pos)}"></div>
<div class="about-offer-copy"><h3>{title}</h3><p>{esc(text)}</p><span class="about-offer-link">Explore &rarr;</span></div>
</a>"""


def about_page_body() -> str:
    wa = general_message()
    offers = "".join(
        _offer_block(h, t, txt, src, alt, pos, i % 2 == 1)
        for i, (h, t, txt, src, alt, pos) in enumerate(OFFERINGS)
    )
    steps = "".join(
        f"""<li class="about-step" data-motion="fade-up">
<span class="about-step-num">{esc(num)}</span>
<h3>{esc(title)}</h3>
<p>{esc(body)}</p>
</li>"""
        for num, title, body in STEPS
    )
    return f"""<main class="about-page">
<section class="about-hero section-breathe">
<div class="container about-hero-grid">
<div class="about-hero-copy" data-motion="fade-up">
<span class="eyebrow">About Indore Nursery</span>
<h1 class="sec sec-display">Bringing a little more nature into everyday spaces.</h1>
<p class="about-lede">Indore Nursery brings together plants, planters and green-space solutions for homes, workplaces, events and outdoor spaces.</p>
</div>
<div class="about-hero-media" data-motion="fade-up">
<img src="/{esc(IMG_HERO)}" alt="Plants and greenery at Indore Nursery" loading="eager" decoding="async" style="object-position:center 35%">
</div>
</div></section>

<section class="about-intro">
<div class="container about-split">
<div class="about-intro-media" data-motion="fade-up">
<img loading="lazy" src="/{esc(IMG_INTRO)}" alt="Outdoor planting and nursery greenery" style="object-position:center 50%">
</div>
<div class="about-intro-copy" data-motion="fade-up">
<h2 class="sec sec-display">More than a nursery.</h2>
<p>Indore Nursery is built around a simple idea — making it easier to bring nature closer to where we live, work and gather.</p>
<p>From curated plants and planters for homes to larger greenery requirements for offices, hospitality spaces, events and landscapes, we help customers find the right plants and create spaces that feel more alive.</p>
</div></div></section>

<section class="about-offerings section-breathe alt">
<div class="container">
<div class="about-section-head center" data-motion="fade-up">
<h2 class="sec sec-display">What we do</h2>
</div>
<div class="about-offer-list">{offers}</div>
</div></section>

<section class="about-approach section-breathe">
<div class="container">
<div class="about-section-head" data-motion="fade-up">
<h2 class="sec sec-display">A simple approach.</h2>
</div>
<ol class="about-steps">{steps}</ol>
</div></section>

<section class="about-audience alt">
<div class="container about-audience-grid">
<div class="about-audience-block" data-motion="fade-up">
<div class="about-audience-media"><img loading="lazy" src="/{esc(IMG_HOME)}" alt="Plants for home spaces" style="object-position:center 40%"></div>
<div class="about-audience-copy"><span class="eyebrow">Home</span><h3>Plants and planters for everyday spaces.</h3></div>
</div>
<div class="about-audience-block" data-motion="fade-up">
<div class="about-audience-media"><img loading="lazy" src="/{esc(IMG_BUSINESS)}" alt="Greenery for workplaces and commercial spaces" style="object-position:center 45%"></div>
<div class="about-audience-copy"><span class="eyebrow">Business</span><h3>Corporate greenery, rentals, maintenance, landscaping and event requirements.</h3></div>
</div>
</div></section>

<section class="clients-band about-clients"><div class="container center" data-motion="fade-up">
<span class="eyebrow">Our clients</span>
<h2 class="sec sec-display">Spaces we&apos;ve helped grow</h2>
{client_logo_marquee_html()}</div></section>

{homepage_visit_section_html()}

<section class="section-breathe about-cta-wrap"><div class="container"><div class="cta-band reveal" data-motion="fade-up">
<h2>Let&apos;s make your space greener.</h2>
<p>Plants, pots or a complete green-space requirement — connect with us.</p>
<div class="hero-actions"><a class="btn-wa" href="{wa}" target="_blank" rel="noopener">Connect With Us</a></div>
</div></div></section></main>"""
