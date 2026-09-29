"""Image paths and metadata for /events/ occasion cards and styling gallery."""

EVENTS_IMG = "/images/events"

# (name, tag, description, filename, alt, object_position)
OCCASION_CARDS = (
    (
        "Corporate Gifting",
        "For clients & teams",
        "Branded plants and green hampers for employee onboarding, client thank-yous and festive gifting \u2014 packed and delivered across Indore.",
        "corporate-gifting.jpg",
        "Corporate plant gifting arrangement",
        "50% 42%",
    ),
    (
        "Hotels & Hospitality",
        "Lobbies & restaurants",
        "Statement plants supplied and placed to match your interiors \u2014 lobby corners, restaurant greens and banquet entrances.",
        "hotel-hospitality.jpg",
        "Greenery in a hotel lobby",
        "50% 55%",
    ),
    (
        "Weddings & Mandaps",
        "Stage to entry",
        "Mandap backdrops, entry arches and photo-corner greens \u2014 designed, delivered and installed fresh for your date.",
        "wedding-mandap.jpg",
        "Indian wedding mandap with plant decor",
        "50% 38%",
    ),
    (
        "Parties & Celebrations",
        "Birthdays to anniversaries",
        "Birthday backdrops, anniversary corners and feature walls \u2014 set up in hours, cleared the same night if you need.",
        "party-celebration.jpg",
        "Plant styling at a celebration",
        "50% 45%",
    ),
    (
        "Store & Caf\u00e9 Openings",
        "Launch-day greenery",
        "Grand-opening plants that make every photo pop \u2014 from entrance statements to counter corners.",
        "store-cafe-opening.jpg",
        "Greenery at a store opening",
        "50% 40%",
    ),
    (
        "Festivals & Big Events",
        "Venues of any size",
        "Diwali, New Year, exhibitions and stage shows \u2014 bulk plants, planters and styling supplied and set up on schedule.",
        "festival-big-event.jpg",
        "Large-scale event greenery",
        "50% 35%",
    ),
)

# (caption, filename, alt, object_position)
STYLING_GALLERY = (
    ("Reception corner", "reception-corner.jpg", "Reception corner plant styling", "50% 35%"),
    ("Living wall detail", "living-wall.jpg", "Living wall with mixed greenery", "50% 50%"),
    ("Mandap backdrop", "mandap-backdrop.jpg", "Wedding mandap backdrop with greenery", "50% 40%"),
    ("Entry arch", "entry-arch.jpg", "Floral entry arch with plants", "60% 45%"),
    ("Photo corner", "photo-corner.jpg", "Photo corner with green backdrop", "50% 30%"),
    ("Table styling", "table-styling.jpg", "Event table styling with plants", "50% 55%"),
    ("Feature wall", "feature-wall.jpg", "Vertical feature wall planting", "50% 45%"),
    ("Terrace setup", "terrace-setup.jpg", "Terrace event plant setup", "50% 60%"),
    ("Lobby greens", "lobby-greens.jpg", "Lobby planting with tall greens", "45% 50%"),
    ("Stage backdrop", "stage-backdrop.jpg", "Stage backdrop with event greenery", "50% 25%"),
    ("Hanging installs", "hanging-installs.jpg", "Hanging plant installation", "50% 40%"),
    ("Caf\u00e9 corner", "cafe-corner.jpg", "Caf\u00e9 corner with potted plants", "55% 50%"),
)


def occ_src(filename: str) -> str:
    return f"{EVENTS_IMG}/{filename}"


def gallery_src(filename: str) -> str:
    return f"{EVENTS_IMG}/{filename}"
