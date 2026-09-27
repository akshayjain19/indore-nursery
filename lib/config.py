"""Site-wide configuration — single source for contact and domain constants."""

SITE_NAME = "Indore Nursery"
SITE_URL = "https://indorenursery.com"
SITE_DESCRIPTION = (
    "Plants for your home. Pots for your space. Greenery for your business."
)

# WhatsApp (E.164 without + for wa.me paths)
WA_PHONE = "918305449559"
WA_PHONE_DISPLAY = "+91 83054 49559"
TEL_URI = f"tel:+{WA_PHONE}"

OWNER_EMAIL = "prakhar@indorenursery.com"

EXCEL_PATH = "data/excel/indore_nursery_products.xlsx"
GENERATED_DIR = "data/generated"
PLANTS_JSON = f"{GENERATED_DIR}/plants.json"
POTS_JSON = f"{GENERATED_DIR}/pots.json"
SEO_MIGRATION_JSON = "data/seo/url-migration.json"
SEO_INVENTORY_JSON = "data/seo/url-inventory.json"

# Curated retail plants surfaced in shop grids (legacy catalog remains in Excel as archived)
DEFAULT_ACTIVE_PLANT_SLUGS = [
    "snake-plant-senseveria",
    "zamia-zz-small",
    "jade-plant-m",
    "lucky-bamboo",
    "peace-lily",
    "aglaonema-snow-white",
    "rubber-plant-2",
    "spider-plant",
    "money-tree-pachira-aquatica",
    "broken-heart",
    "alocasia",
    "fiddle-leaf-ficus-lyrata",
    "dracaena-darasingh-plant",
    "croton-mammy",
    "jasmine-sambac-mogra",
    "thuja-vidya",
    "dracena-fragrans",
    "singonium-green",
    "echivera-succullent",
    "english-rose",
]

PLANT_FILTER_TAGS = [
    "Indoor",
    "Outdoor",
    "Low Maintenance",
    "Air Purifying",
    "Flowering",
    "Succulents",
    "Gifting",
]

POT_COLLECTIONS = [
    ("ECO SERIES", "eco-series"),
    ("Plastic Pots", "plastic-pots"),
    ("Statement Planters", "statement-planters"),
    ("Illuminated & Decorative", "illuminated-decorative"),
    ("Hanging Planters", "hanging-planters"),
]
