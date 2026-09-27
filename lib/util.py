import html as html_lib
import re
from urllib.parse import quote

from lib.config import WA_PHONE

FALLBACK_IMAGE = "images/2022_03_ALOCASIA-BLACK.jpg"


def esc(s):
    return html_lib.escape(str(s or ""), quote=True)


def slugify(s):
    s = (s or "").lower().replace("&", "and").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def money(n):
    if n is None or n == "":
        return "On Request"
    try:
        return "₹" + format(int(float(n)), ",d")
    except (TypeError, ValueError):
        return "On Request"


def img_url(u):
    if not u:
        return FALLBACK_IMAGE
    if u.startswith("/") or u.startswith("images/"):
        return u.lstrip("/")
    m = re.search(r"wp-content/uploads/(.+)$", u)
    if m:
        return "images/" + m.group(1).replace("/", "_")
    return FALLBACK_IMAGE


def wa_link(message):
    return f"https://wa.me/{WA_PHONE}?text={quote(message)}"


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()
