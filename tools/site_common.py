"""What every page of gugostudios.com shares: the <head>, the header, the footer, the studio's games (with their store
links) and a helper that turns the games' art into web images. Used by gen_studio_pages.py, gen_legal_pages.py and
gen_orbit_pages.py.

Links are written relative to each page, so a page needs its `root`: "" for a page in site/, "../" for a page in a
folder (site/orbitsmash/...), and "/" for the 404 page, which GitHub Pages serves at any address.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
BASE_URL = "https://gugostudios.com"
SUPPORT = "support@gugostudios.com"
YEAR = 2026
TAGLINE = "Cute, cozy games for the whole family"

STUDIO_LOGO_SMALL = "assets/img/studio/gugo-logo-240.webp"  # 240 x 130

# The studio's games, in the order the site lists them. Store links: None shows a "Coming soon" badge. When a game goes
# live, put its store listing's address here and run the generators again: the badges become "Get it on" buttons.
GAMES = [
    {
        "id": "dripdropgarden",
        "name": "Drip Drop Garden",
        "page": "dripdropgarden/",
        "privacy": "privacy.html",
        "terms": "terms.html",
        "icon": "assets/img/icon-256.webp",
        "google_play": None,  # com.dripdropgarden.game, in closed testing
        "app_store": None,
    },
    {
        "id": "orbitsmash",
        "name": "Orbit Smash",
        "page": "orbitsmash/",
        "privacy": "orbitsmash/privacy.html",
        "terms": "orbitsmash/terms.html",
        "icon": "assets/img/orbitsmash/icon-256.webp",
        "google_play": None,  # com.gugostudios.orbitsmash, in closed testing
        "app_store": None,    # "Orbit Smash: Space Hammer"
    },
]
GAME = {g["id"]: g for g in GAMES}

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">"""


def esc(text):
    """Escapes text for HTML, attribute values included (they're always in double quotes)."""
    return html.escape(text, quote=False).replace('"', "&quot;")


def home_link(root):
    return root or "./"


def store_buttons(game, compact=False, indent="        "):
    """The game's two store buttons: a link once the listing is public, otherwise a "Coming soon" badge. Big ones
    (compact=False) are the hero's buttons; compact ones are the small pills on the studio's game cards."""
    out = []
    stores = (("google_play", "Google Play", "Coming soon on", "Get it on", "btn-orange"),
              ("app_store", "App Store", "Coming soon on the", "Download on the", "btn-ghost"))
    for key, store, soon, get, style in stores:
        url = game[key]
        if compact:
            if url:
                out.append(f'<a class="store-pill live" href="{esc(url)}"><small>{get}</small>{store}</a>')
            else:
                out.append(f'<span class="store-pill"><small>{soon}</small>{store}</span>')
        elif url:
            out.append(f'<a class="btn {style}" href="{esc(url)}"><span class="stack"><small>{get}</small>{store}</span></a>')
        else:
            out.append(f'<span class="btn {style}"><span class="stack"><small>{soon}</small>{store}</span></span>')
    return ("\n" + indent).join(out)


def studio_brand(root):
    return (f'<a class="brand brand-studio" href="{home_link(root)}"><img src="{root}{STUDIO_LOGO_SMALL}" '
            f'alt="GuGo Studios" width="81" height="44"></a>')


def game_brand(href, icon, name):
    return f'<a class="brand" href="{href}"><img src="{icon}" alt="" width="40" height="40"><span>{esc(name)}</span></a>'


def nav_links(items):
    """items: (label, href, optional, current). Optional links hide on phones (the footer still has them all)."""
    out = []
    for label, href, optional, current in items:
        attrs = ' class="optional"' if optional else ""
        if current:
            attrs += ' aria-current="page"'
        out.append(f'      <a{attrs} href="{href}">{esc(label)}</a>')
    return "\n".join(out)


def footer(root):
    cols = []
    for g in GAMES:
        cols.append(f"""    <nav class="foot-col" aria-label="{esc(g['name'])}">
      <p class="foot-title"><img src="{root}{g['icon']}" alt="" width="28" height="28" loading="lazy">{esc(g['name'])}</p>
      <a href="{root}{g['page']}">The game</a>
      <a href="{root}{g['privacy']}">Privacy Policy</a>
      <a href="{root}{g['terms']}">Terms of Use</a>
    </nav>""")
    cols = "\n".join(cols)
    return f"""<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-studio">
      <a href="{home_link(root)}"><img src="{root}{STUDIO_LOGO_SMALL}" alt="GuGo Studios" width="120" height="65" loading="lazy"></a>
      <p>{TAGLINE}.</p>
      <a href="mailto:{SUPPORT}">{SUPPORT}</a>
    </div>
{cols}
  </div>
  <div class="wrap foot-bottom">
    <span>© {YEAR} GuGo Studios</span>
    <a href="mailto:{SUPPORT}">Contact</a>
  </div>
</footer>"""


def page(*, title, description, root, brand, nav, main, path=None, main_class="", body_class="", theme="#149ba1",
         icon="assets/img/favicon-64.png", apple="assets/img/apple-touch-icon.png", og=None, head_extra=""):
    """A whole page. path: its address on the site ("/", "/orbitsmash/"...) for the canonical link and the link preview
    (None for the 404 page). og: (title, description, image path in site/) for the link preview, or None."""
    meta = []
    if og:
        og_title, og_description, og_image = og
        meta += [f'<meta property="og:title" content="{esc(og_title)}">',
                 f'<meta property="og:description" content="{esc(og_description)}">',
                 f'<meta property="og:image" content="{BASE_URL}/{og_image}">',
                 f'<meta property="og:url" content="{BASE_URL}{path}">',
                 '<meta property="og:type" content="website">',
                 '<meta name="twitter:card" content="summary_large_image">']
    meta.append(f'<meta name="theme-color" content="{theme}">')
    if path:
        meta.append(f'<link rel="canonical" href="{BASE_URL}{path}">')
    meta = "\n".join(meta)
    main_attrs = f' class="{main_class}"' if main_class else ""
    body_attrs = f' class="{body_class}"' if body_class else ""
    extra = "\n" + head_extra.strip() if head_extra.strip() else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{meta}
<link rel="icon" type="image/png" href="{root}{icon}">
<link rel="apple-touch-icon" href="{root}{apple}">
{FONTS}
<link rel="stylesheet" href="{root}assets/site.css">{extra}
</head>
<body{body_attrs}>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    {brand}
    <nav class="nav" aria-label="Main">
{nav_links(nav)}
    </nav>
  </div>
</header>

<main id="main"{main_attrs}>
{main.strip()}
</main>

{footer(root)}

</body>
</html>
"""


def write(rel, text):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", os.path.relpath(path, ROOT))


# ---- Images ---------------------------------------------------------------------------------------------------------

def pillow():
    """PIL's Image module, or None when Pillow isn't installed (the pages are still written, the images are kept)."""
    try:
        from PIL import Image
        return Image
    except ImportError:
        return None


def save_image(im, rel, quality=82):
    """Saves an image into site/ by its extension (.webp, .jpg or .png). The encoders are deterministic, so making an
    image again from the same source leaves the file byte for byte the same."""
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ext = os.path.splitext(rel)[1].lower()
    if ext == ".webp":
        im.save(path, "WEBP", quality=quality, method=6)
    elif ext in (".jpg", ".jpeg"):
        im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    else:
        im.save(path, "PNG", optimize=True)
    return path


def fit(im, max_w, max_h):
    """Scales an image down (never up) to fit in max_w x max_h, keeping its shape."""
    from PIL import Image
    s = min(max_w / im.width, max_h / im.height, 1.0)
    if s >= 1.0:
        return im.copy()
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def image_size(rel, default):
    """(width, height) of an image in site/, for the <img> tags; `default` when it can't be read."""
    Image = pillow()
    path = os.path.join(SITE, rel)
    if Image and os.path.exists(path):
        with Image.open(path) as im:
            return im.size
    return default


def site_relpath(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")
