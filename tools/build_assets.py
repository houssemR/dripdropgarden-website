"""Makes the website's images from the game's own art.

    uv run --with pillow python tools/build_assets.py [path to the DripDropGarden Unity project]

Writes into site/assets/img: the hero background, the app icon in a few sizes, the store feature graphic, the phone
screenshots and a row of character cards. Run it again whenever the store art changes.
"""
import os
import sys
from PIL import Image

GAME = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/houss/UnityProjects/DripDropGarden"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site", "assets", "img")
os.makedirs(OUT, exist_ok=True)


def src(*parts):
    return os.path.join(GAME, *parts)


def save_webp(im, name, quality=80):
    im.save(os.path.join(OUT, name), "WEBP", quality=quality, method=6)


# Hero: the loading screen's daisy hill (portrait); the page crops it to fit.
hill = Image.open(src("Assets", "Sprites", "UI", "Loading", "LoadingHill.png")).convert("RGB")
save_webp(hill, "hero-bg.webp", 78)
save_webp(hill.resize((540, 960), Image.LANCZOS), "hero-bg-small.webp", 78)

# App icon.
icon = Image.open(src("Docs", "store", "icon_512.png")).convert("RGB")
icon.save(os.path.join(OUT, "icon-512.png"))
icon.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "icon-192.png"))
icon.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))
icon.resize((64, 64), Image.LANCZOS).save(os.path.join(OUT, "favicon-64.png"))
save_webp(icon.resize((256, 256), Image.LANCZOS), "icon-256.webp", 85)

# Store feature graphic (also the link preview picture).
feature = Image.open(src("Docs", "store", "feature_1024x500.png")).convert("RGB")
feature.save(os.path.join(OUT, "og-image.png"))
save_webp(feature, "feature.webp", 82)

# Phone screenshots (1080x1920 store shots, halved).
for i in range(1, 8):
    p = src("Docs", "store", "phone_%d.png" % i)
    if os.path.exists(p):
        save_webp(Image.open(p).convert("RGB").resize((540, 960), Image.LANCZOS), "shot-%d.webp" % i, 80)

# Character cards (transparent cut-outs).
for cid in ("hen", "bunny", "lamb", "honk", "capy", "ghostkit", "pumpkid", "owl", "frog", "penguin"):
    p = src("Assets", "Sprites", "UI", "Characters", "char_%s.png" % cid)
    if os.path.exists(p):
        save_webp(Image.open(p).convert("RGBA").resize((240, 240), Image.LANCZOS), "char-%s.webp" % cid, 85)

total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print("%d files, %.1f KB" % (len(os.listdir(OUT)), total / 1024))
