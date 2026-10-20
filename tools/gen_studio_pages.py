"""Builds the studio's pages: the GuGo Studios home page (site/index.html) with a card for each game, Drip Drop Garden's
page (site/dripdropgarden/index.html), the 404 page and site/sitemap.xml, in the site's look (tools/site_common.py).

It also makes the studio's images in site/assets/img/studio/ (logo, favicon, link preview) from the GuGo Studios logo
in the Drip Drop Garden Unity project. That needs Pillow; without it, or without the logo, the images already there are
kept. Run tools/gen_orbit_pages.py first: the home page shows Orbit Smash's screenshots.

    uv run --with pillow python tools/gen_studio_pages.py

Drip Drop Garden's page used to be the home page, so the home page sends the old links to its sections
(gugostudios.com/#play, #families, #support) on to the same sections of /dripdropgarden/.
"""
import os

import gen_orbit_pages as orbit
from site_common import (GAME, SITE, SUPPORT, TAGLINE, esc, fit, game_brand, image_size, page, pillow, save_image,
                         store_buttons, studio_brand, write)

DDG = GAME["dripdropgarden"]
ORBIT = GAME["orbitsmash"]
STUDIO = "assets/img/studio/"

# The GuGo Studios logo (the studio intro's art), and where its smiley "O" is in it (centre x, y and radius).
LOGO_SOURCES = ["C:/Users/houss/UnityProjects/DripDropGarden/Assets/Sprites/UI/Studio/GuGoStudios.png",
                "C:/Users/houss/UnityProjects/TapTapIdeas/Assets/Resources/Art/logo_gugo.png"]
FACE = (921, 255, 125)

# Drip Drop Garden's screenshots (made by tools/build_assets.py), in the order its page shows them: (image, alt text).
DDG_SHOTS = [
    ("assets/img/shot-1.webp", "Catching raindrops by a red barn"),
    ("assets/img/shot-2.webp", "Rain over a hilltop manor"),
    ("assets/img/shot-3.webp", "Golden drops on a hayride farm"),
    ("assets/img/shot-4.webp", "A storm over the corn maze"),
    ("assets/img/shot-5.webp", "The Sunny Meadow map"),
    ("assets/img/shot-6.webp", "The October Garden map"),
    ("assets/img/shot-7.webp", "A beautiful bloom"),
]
# Which of them (1 = the first) the home page shows on Drip Drop Garden's card.
DDG_CARD_SHOTS = (1, 5, 7)

# Every page, for sitemap.xml.
SITEMAP = ["/", "/dripdropgarden/", "/privacy.html", "/terms.html",
           "/orbitsmash/", "/orbitsmash/privacy.html", "/orbitsmash/terms.html"]


# ---- Images ---------------------------------------------------------------------------------------------------------

def build_images():
    Image = pillow()
    if Image is None:
        print("Pillow isn't installed: kept the studio's images as they are")
        return
    from PIL import ImageChops, ImageDraw, ImageFilter

    src = next((p for p in LOGO_SOURCES if os.path.exists(p)), None)
    if src is None:
        print("missing the GuGo Studios logo - kept the studio's images as they are")
        return
    im = Image.open(src).convert("RGBA")
    logo = im.crop(im.getbbox())
    save_image(fit(logo, 880, 880), STUDIO + "gugo-logo.webp", 85)
    save_image(fit(logo, 240, 240), STUDIO + "gugo-logo-240.webp", 88)

    # The smiley "O", cut out round: the favicon and the 404 page's face.
    cx, cy, r = FACE
    face = im.crop((cx - r, cy - r, cx + r, cy + r))
    big = Image.new("L", (face.width * 4, face.height * 4), 0)
    ImageDraw.Draw(big).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    face.putalpha(ImageChops.multiply(face.getchannel("A"), big.resize(face.size, Image.LANCZOS)))
    save_image(face.resize((256, 256), Image.LANCZOS), STUDIO + "face-256.webp", 88)
    save_image(face.resize((64, 64), Image.LANCZOS), STUDIO + "favicon-64.png")

    def soft_background(w, h):
        """The studio intro's soft white-to-turquoise glow."""
        glow = Image.radial_gradient("L").resize((w, h), Image.LANCZOS)
        return Image.composite(Image.new("RGB", (w, h), (184, 237, 235)), Image.new("RGB", (w, h), (255, 255, 255)),
                               glow).convert("RGBA")

    apple = soft_background(180, 180)
    apple.alpha_composite(face.resize((148, 148), Image.LANCZOS), (16, 16))
    save_image(apple.convert("RGB"), STUDIO + "apple-touch-icon.png")

    # Link preview (1200 x 630): the logo between the two games' icons.
    icons = [os.path.join(SITE, "assets", "img", "icon-512.png"), os.path.join(SITE, orbit.IMG, "icon-512.webp")]
    if not all(os.path.exists(p) for p in icons):
        print("missing a game icon - kept the studio's link preview as it is")
        return
    og = soft_background(1200, 630)
    lg = fit(logo, 600, 600)
    og.alpha_composite(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2))
    size, radius = 210, 54
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * 4 - 1, size * 4 - 1), radius * 4, fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    for path, x in zip(icons, (52, 1200 - 52 - size)):
        y = (630 - size) // 2
        shadow = Image.new("RGBA", og.size, (0, 0, 0, 0))
        shadow.paste((20, 70, 75, 90), (x, y + 14), mask)
        og.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
        icon = Image.open(path).convert("RGB").resize((size, size), Image.LANCZOS).convert("RGBA")
        icon.putalpha(mask)
        og.alpha_composite(icon, (x, y))
    save_image(og, STUDIO + "og-image.jpg", 86)


# ---- The home page --------------------------------------------------------------------------------------------------

def shots_html(shots, indent):
    return "\n".join(f'{indent}<img src="{rel}" alt="{esc(alt)}" loading="lazy" width="{w}" height="{h}">'
                     for rel, alt, w, h in shots)


def game_card(g, top, pitch, text, shots, cta):
    """A game's card on the home page; top: the class that paints its top band (ddg-sky or space-bg)."""
    return f"""      <article class="game-card game-{g['id']}" aria-labelledby="game-{g['id']}">
        <div class="game-top {top}">
          <img class="game-icon" src="{g['icon']}" alt="" width="96" height="96">
          <div>
            <h3 id="game-{g['id']}"><a href="{g['page']}">{esc(g['name'])}</a></h3>
            <p class="pitch">{esc(pitch)}</p>
          </div>
        </div>
        <div class="game-body">
          <p>{esc(text)}</p>
          <div class="mini-shots">
{shots_html(shots, "            ")}
          </div>
          <div class="store-row">
            {store_buttons(g, compact=True, indent="            ")}
          </div>
          <div class="game-links">
            <a class="btn btn-teal" href="{g['page']}">{esc(cta)}</a>
            <a href="{g['privacy']}">Privacy Policy</a>
            <a href="{g['terms']}">Terms of Use</a>
          </div>
        </div>
      </article>"""


def home():
    ddg_shots = [(DDG_SHOTS[i - 1][0], DDG_SHOTS[i - 1][1], *image_size(DDG_SHOTS[i - 1][0], (540, 960)))
                 for i in DDG_CARD_SHOTS]
    orbit_shots = [orbit.shot(i) for i in orbit.CARD_SHOTS]
    lw, lh = image_size(STUDIO + "gugo-logo.webp", (880, 475))
    cards = "\n".join([
        game_card(DDG, "ddg-sky", "Catch the rain, grow a garden!",
                  "Catch clean raindrops in your watering can, dodge the junk that cheeky garden friends throw and grow "
                  "a garden full of happy flowers.", ddg_shots, "Visit Drip Drop Garden"),
        game_card(ORBIT, "space-bg", "Swing the hammer, save the planet!",
                  "Swing your hammer around the Earth and smash the asteroids, comets and silly aliens flying at it, "
                  "across 49 levels and 7 regions of space.", orbit_shots, "Visit Orbit Smash"),
    ])
    links = "\n".join(
        f'        <li><b>{esc(g["name"])}</b><a href="{g["privacy"]}">Privacy Policy</a><a href="{g["terms"]}">Terms of Use</a></li>'
        for g in (DDG, ORBIT))
    return f"""
<section class="studio-hero">
  <img class="float float-left" src="{DDG['icon']}" alt="" width="256" height="256">
  <img class="float float-right" src="{ORBIT['icon']}" alt="" width="256" height="256">
  <div class="wrap">
    <h1><img src="{STUDIO}gugo-logo.webp" alt="GuGo Studios" width="{lw}" height="{lh}" fetchpriority="high"></h1>
    <p class="tagline">{TAGLINE}</p>
    <p class="lead">GuGo Studios is a small independent game studio. We make colourful mobile games that are easy to pick up, fun to master and safe for kids: no chat, no strangers and child-safe ads.</p>
    <div class="ctas">
      <a class="btn btn-orange" href="#games">Meet our games</a>
      <a class="btn btn-ghost" href="#contact">Say hello</a>
    </div>
  </div>
</section>

<section id="games">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Our games</span>
      <h2>Two little worlds to play in</h2>
      <p>A cozy garden and a whole galaxy. Both are free to play, and both are made for kids and grown-ups alike.</p>
    </div>
    <div class="games">
{cards}
    </div>
  </div>
</section>

<section id="about" class="friends-band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What we care about</span>
      <h2>Games you can hand to your kids</h2>
      <p>Every GuGo game is made to be safe, fair and fun for the whole family.</p>
    </div>
    <div class="grid">
      <div class="card"><div class="emoji" aria-hidden="true">🧸</div><h3>Made for families</h3><p>Bright, gentle and easy to learn, with a Kids land made for the youngest players. No chat, no accounts and no way for strangers to reach your child.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">🛡️</div><h3>Child-safe ads</h3><p>Our games ask the player's age once. Younger players only see ads suitable for children, never based on their behaviour, and the Kids lands have no ads at all.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">💛</div><h3>Fair to play</h3><p>Both games are free. Everything in the shop says what's inside, and a grown-up check comes before any purchase by a child.</p></div>
    </div>
  </div>
</section>

<section id="contact" class="tight-top">
  <div class="wrap duo">
    <div class="card support">
      <div class="emoji" aria-hidden="true">💌</div>
      <h3>Say hello</h3>
      <p>Questions about a game, ideas, or a problem with a purchase? We read every message.</p>
      <a class="mail" href="mailto:{SUPPORT}">{SUPPORT}</a>
    </div>
    <div class="card parents">
      <div class="emoji" aria-hidden="true">📄</div>
      <h3>For parents</h3>
      <p>What each game does with information, and the rules for playing it:</p>
      <ul class="legal-links">
{links}
      </ul>
    </div>
  </div>
</section>
"""


# Old links to Drip Drop Garden's sections, from when its page was the home page.
OLD_ANCHORS = """<script>
if (/^#(play|families|support)$/.test(location.hash)) location.replace("dripdropgarden/" + location.hash);
</script>"""


# ---- Drip Drop Garden's page (the home page until the studio had two games) ----------------------------------------

def ddg_page():
    shots = "\n".join(
        f'    <figure><img src="../{rel}" alt="{esc(alt)}" loading="lazy" width="{w}" height="{h}"></figure>'
        for rel, alt, w, h in ((rel, alt, *image_size(rel, (540, 960))) for rel, alt in DDG_SHOTS))
    return f"""
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Drip Drop Garden</h1>
      <p class="tagline">Catch the rain, grow a garden!</p>
      <p class="lead">Hold a glass watering can under the sky, catch the clean raindrops, dodge the junk that cheeky garden friends throw, and pour fresh water into your flower pot. The cleaner the water, the more beautiful the bloom.</p>
      <div class="ctas">
        {store_buttons(DDG)}
      </div>
    </div>
    <div class="art"><img src="../assets/img/icon-512.png" alt="The Drip Drop Garden icon: a happy water drop with a little sprout" width="320" height="320"></div>
  </div>
</section>

<section id="play">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The game</span>
      <h2>Easy to play, fun to master</h2>
      <p>Slide your finger to move the can. Catch drops in a row for combos and Fever, grab golden drops, and smash junk before it lands.</p>
    </div>
  </div>
  <div class="shots" tabindex="0" role="region" aria-label="Screenshots of Drip Drop Garden">
{shots}
  </div>
  <div class="wrap">
    <div class="grid spaced">
      <div class="card"><div class="emoji" aria-hidden="true">🌸</div><h3>A world of gardens</h3><p>From the Sunny Meadow to the Old Town, the Seaside Village, the Emerald Jungle, the Sunny Dunes, the Bubble Reef and the Frosty Peaks: 50 levels and a grumpy boss in every garden.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">📅</div><h3>A new garden every month</h3><p>The Monthly garden has a new level every day, with apples to pick, gift fruits, star chests and a hidden friend to find.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">🧸</div><h3>Gardens for little ones</h3><p>The Kids gardens are slow, gentle and full of cute friends, made for the youngest players.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">🌦️</div><h3>Every kind of weather</h3><p>Sunrises, sunsets, starry nights, storms and snow: every garden has its own sky.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">🎒</div><h3>Collect everything</h3><p>Characters, pots, watering cans, trails and butterflies. Spin the free daily wheel, fill the sticker album and earn badges.</p></div>
      <div class="card"><div class="emoji" aria-hidden="true">🏆</div><h3>A season every month</h3><p>Daily and monthly challenges, season rewards, a daily streak and bonus rewards for keen gardeners.</p></div>
    </div>
  </div>
</section>

<section class="friends-band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Garden friends</span>
      <h2>Meet the gang</h2>
      <p>Henrietta the hen waters your garden, and dozens of friends join her along the way.</p>
    </div>
    <div class="friends">
      <img src="../assets/img/char-hen.webp" alt="Henrietta the hen" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-bunny.webp" alt="Bun-Bun the bunny" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-lamb.webp" alt="Woolly the lamb" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-frog.webp" alt="A frog friend" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-capy.webp" alt="Capy the capybara" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-honk.webp" alt="Honk the goose" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-penguin.webp" alt="A penguin friend" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-pumpkid.webp" alt="Jack the pumpkin kid" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-ghostkit.webp" alt="Boo the ghost kitten" loading="lazy" width="240" height="240">
      <img src="../assets/img/char-owl.webp" alt="Hootie the owl" loading="lazy" width="240" height="240">
    </div>
  </div>
</section>

<section id="families">
  <div class="wrap families">
    <img class="feature-img" src="../assets/img/feature.webp" alt="Drip Drop Garden" loading="lazy" width="1024" height="500">
    <div>
      <span class="eyebrow">For the whole family</span>
      <h2>Made with kids in mind</h2>
      <ul class="checks">
        <li><span class="dot" aria-hidden="true">✓</span><div><b>Child-safe ads</b><span class="txt">The game asks your age once. On Android, younger players only see ads suitable for children, never based on their behaviour. The Kids gardens, and the game on iPhone and iPad, have no ads at all.</span></div></li>
        <li><span class="dot" aria-hidden="true">✓</span><div><b>No surprise purchases</b><span class="txt">Everything you can buy shows exactly what you get: the boxes in the shop list every item inside, and the daily spin is free.</span></div></li>
        <li><span class="dot" aria-hidden="true">✓</span><div><b>A grown-up check</b><span class="txt">Before a child can buy anything, the game asks a question only a grown-up should answer.</span></div></li>
        <li><span class="dot" aria-hidden="true">✓</span><div><b>No chat, no accounts</b><span class="txt">Nothing to sign up for and no way for strangers to talk to your child.</span></div></li>
      </ul>
    </div>
  </div>
</section>

<section id="support" class="tight-top">
  <div class="wrap duo">
    <div class="card premium">
      <div class="emoji" aria-hidden="true">👑</div>
      <h3>Premium</h3>
      <p>Drip Drop Garden is free to play. The Premium Pass, monthly or yearly, unlocks every season's premium rewards, gives the video rewards without watching and removes the ads on Android. It renews until you cancel it in Google Play or the App Store.</p>
    </div>
    <div class="card support">
      <div class="emoji" aria-hidden="true">💌</div>
      <h3>Need help?</h3>
      <p>Questions, ideas or a problem with a purchase? We read every message.</p>
      <a class="mail" href="mailto:{SUPPORT}">{SUPPORT}</a>
      <p class="card-links"><a href="../privacy.html">Privacy Policy</a> · <a href="../terms.html">Terms of Use</a></p>
    </div>
  </div>
</section>
"""


# ---- The 404 page ---------------------------------------------------------------------------------------------------

def not_found():
    games = "\n".join(
        f'      <li><a href="/{g["page"]}"><img src="/{g["icon"]}" alt="" width="48" height="48">{esc(g["name"])}</a></li>'
        for g in (DDG, ORBIT))
    return f"""
<section class="notfound">
  <div class="wrap">
    <img class="face" src="/{STUDIO}face-256.webp" alt="" width="160" height="160">
    <h1>Oops! This page wandered off</h1>
    <p>Maybe it's out watering a garden, or smashing asteroids. The page you were looking for isn't here.</p>
    <p><a class="btn btn-orange" href="/">Back to GuGo Studios</a></p>
    <ul class="notfound-games">
{games}
    </ul>
  </div>
</section>
"""


def main():
    build_images()
    studio = dict(brand=None, icon=STUDIO + "favicon-64.png", apple=STUDIO + "apple-touch-icon.png")

    write("index.html", page(
        title="GuGo Studios: Cute, Cozy Games for the Whole Family",
        description="GuGo Studios makes cute, family-friendly mobile games: Drip Drop Garden, a cozy rain-catching "
                    "garden game, and Orbit Smash, a space arcade game.",
        root="", path="/",
        og=("GuGo Studios", TAGLINE + ": Drip Drop Garden and Orbit Smash.", STUDIO + "og-image.jpg"),
        nav=[(DDG["name"], DDG["page"], True, False), (ORBIT["name"], ORBIT["page"], True, False),
             ("Contact", "#contact", False, False)],
        main=home(), head_extra=OLD_ANCHORS,
        **{**studio, "brand": studio_brand("")}))

    write("dripdropgarden/index.html", page(
        title="Drip Drop Garden by GuGo Studios: Catch the Rain, Grow a Garden",
        description="Drip Drop Garden is a cozy game for the whole family: catch clean raindrops in your watering can, "
                    "dodge the junk and grow a garden full of happy flowers.",
        root="../", path="/dripdropgarden/",
        og=("Drip Drop Garden", "Catch clean raindrops, dodge the junk and grow a garden full of happy flowers.",
            "assets/img/og-image.png"),
        brand=game_brand("./", "../assets/img/icon-192.png", DDG["name"]),
        nav=[("The game", "#play", True, False), ("Families", "#families", True, False),
             ("Support", "#support", True, False), ("All games", "../#games", False, False)],
        main=ddg_page()))

    write("404.html", page(
        title="Page not found - GuGo Studios",
        description="This page isn't here.",
        root="/",
        nav=[(DDG["name"], "/" + DDG["page"], True, False), (ORBIT["name"], "/" + ORBIT["page"], True, False),
             ("All games", "/#games", False, False)],
        main=not_found(), head_extra='<meta name="robots" content="noindex">',
        **{**studio, "brand": studio_brand("/")}))

    urls = "\n".join(f"  <url><loc>https://gugostudios.com{p}</loc></url>" for p in SITEMAP)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")


if __name__ == "__main__":
    main()
