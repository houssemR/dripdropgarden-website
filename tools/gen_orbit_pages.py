"""Builds Orbit Smash's pages under site/orbitsmash/: the game's page, the privacy policy and the terms of use (texts in
legal/orbitsmash/*.html, just the <main> content), in the site's look (tools/site_common.py). The game and its store
listings link to https://gugostudios.com/orbitsmash/privacy.html and /orbitsmash/terms.html: keep those paths.

It also makes the page's images in site/assets/img/orbitsmash/ from the game's store art (STORE below): the icon, the
feature graphic and the screenshots listed in SCREENSHOTS. That needs Pillow; without it, or without the art, the
images already there are kept.

    uv run --with pillow python tools/gen_orbit_pages.py
"""
import os

from site_common import (GAME, ROOT, SITE, SUPPORT, esc, fit, game_brand, image_size, page, pillow, save_image,
                         site_relpath, store_buttons, write)

ORBIT = GAME["orbitsmash"]
STORE = "C:/Users/houss/UnityProjects/TapTapIdeas/Docs/store"  # the Unity project's store graphics
IMG = "assets/img/orbitsmash/"                                  # where the web images go, in site/

# The screenshots on Orbit Smash's page, in order: (picture, alt text). To show other pictures (nicer marketing shots,
# say), change this list and run the script again: it remakes site/assets/img/orbitsmash/shot-1.webp, shot-2.webp...
# from them, at most 900 px tall. Portrait phone pictures fit best (the page shows them as 9:16 phones).
SCREENSHOTS = [
    (STORE + "/screens/play/en/01.jpg", "Smash space rocks: the hammer swings at asteroids around a smiling Earth"),
    (STORE + "/screens/play/en/02.jpg", "Swing all around: the hammer follows your finger past the Frosty Moon's comets"),
    (STORE + "/screens/play/en/03.jpg", "Epic boss battles: a big boom against the Mothership"),
    (STORE + "/screens/play/en/04.jpg", "Go HYPER: combos light up the Jungle Nebula"),
    (STORE + "/screens/play/en/05.jpg", "7 regions of space: the Journey map, with 49 levels to explore"),
    (STORE + "/screens/play/en/06.jpg", "Cool hammers: the Hangar's hammer skins and upgrades"),
    (STORE + "/screens/play/en/07.jpg", "Cute guardians: Moon Buddy, Night Owl and friends defend the Earth"),
    (STORE + "/screens/play/en/08.jpg", "A level every day: the monthly map for November"),
]
# Which of them (1 = the first) the studio's home page shows on Orbit Smash's card.
CARD_SHOTS = (1, 3, 7)

# The regions of the Journey, in order: name, levels, boss, the game's colour for the region.
REGIONS = [
    ("Meteor Meadow", 4, "the Rock King", "#5BD38A"),
    ("Frosty Moon", 5, "the Frost Titan", "#7FD3FF"),
    ("Solar Canyon", 7, "the Mothership", "#FF8A3D"),
    ("Crystal Belt", 10, "the Crystal Queen", "#B388FF"),
    ("Jungle Nebula", 10, "the Jungle Giant", "#3DDC84"),
    ("Robo Station", 10, "the Robo Overlord", "#5CE1FF"),
    ("Galaxy Core", 3, "the Void King", "#FFC93C"),
]

SHOT_SIZE = (506, 900)  # what a 1080 x 1920 store shot becomes


def shot(i):
    """The i-th screenshot (1 = the first): (path in site/, alt text, width, height)."""
    rel = f"{IMG}shot-{i}.webp"
    w, h = image_size(rel, SHOT_SIZE)
    return rel, SCREENSHOTS[i - 1][1], w, h


def build_images():
    Image = pillow()
    if Image is None:
        print("Pillow isn't installed: kept Orbit Smash's images as they are")
        return

    def load(path, mode="RGB"):
        if os.path.exists(path):
            return Image.open(path).convert(mode)
        print("missing", path, "- kept the image made from it before")
        return None

    icon = load(STORE + "/icon_512.png")
    if icon:
        save_image(icon, IMG + "icon-512.webp", 85)
        save_image(icon.resize((256, 256), Image.LANCZOS), IMG + "icon-256.webp", 85)
        save_image(icon.resize((180, 180), Image.LANCZOS), IMG + "apple-touch-icon.png")
        save_image(icon.resize((64, 64), Image.LANCZOS), IMG + "favicon-64.png")
    feature = load(STORE + "/feature_1024x500.png")
    if feature:
        save_image(feature, IMG + "feature.webp", 82)
        save_image(feature, IMG + "og-image.jpg", 85)  # the link preview picture
    logo = load(os.path.join(SITE, "orbitsmash", "logo.png"), "RGBA")
    if logo:
        save_image(logo, IMG + "logo.webp", 90)
    for i, (path, _alt) in enumerate(SCREENSHOTS, 1):
        im = load(path)
        if im:
            save_image(fit(im, 1600, 900), f"{IMG}shot-{i}.webp", 80)
    # Screenshots left over from a longer list.
    i = len(SCREENSHOTS) + 1
    while os.path.exists(os.path.join(SITE, f"{IMG}shot-{i}.webp")):
        os.remove(os.path.join(SITE, f"{IMG}shot-{i}.webp"))
        i += 1
    total = sum(os.path.getsize(os.path.join(SITE, IMG, f)) for f in os.listdir(os.path.join(SITE, IMG)))
    print("images in %s: %.0f KB" % (site_relpath(os.path.join(SITE, IMG)), total / 1024))


CARDS = [
    ("🌍", "A journey across space",
     "49 levels across 7 regions, from Meteor Meadow to the Galaxy Core. Every region has its own Earth, music and "
     "weather, and a boss waiting at the end."),
    ("👾", "Silly aliens, big bosses",
     "Snowball yetis, lava imps, crystal bats, spore puffs, spark bots and blinking void imps. Then the Rock King, the "
     "Frost Titan, the Mothership and more."),
    ("⚡", "Waves, combos and HYPER",
     "Levels play in waves and the music speeds up with each one. Chain smashes into combos, go HYPER, and tap the "
     "glowing Earth for a SUPERNOVA that blasts everything away."),
    ("🔨", "Hammers and guardians",
     "Upgrade your hammer's power, size and swing, collect 11 hammer skins and build a team of 12 cute guardians: "
     "Moon Buddy, Laser Bot, Night Owl, Star Whale and more."),
    ("📅", "A level every day",
     "The Monthly map has a new level every day. Spin the free daily wheel, keep your streak, take on challenges, fill "
     "a season of rewards and collect badges."),
    ("🧸", "A Kids land",
     "Gentle levels for the littlest players, and a guided first level that teaches everyone how to swing."),
]

CHECKS = [
    ("Child-safe ads",
     "The game asks your age once. Younger players only see ads suitable for children, never based on their "
     "behaviour. There are no ads in the Kids land or in your first levels."),
    ("No random purchases",
     "Every box in the shop shows the gems, coins and XP inside and the kind of surprise it holds, and the surprise is "
     "always the next item in a fixed order."),
    ("A grown-up check",
     "Before a child can buy anything, the game asks a question only a grown-up should answer."),
    ("No chat, no accounts",
     "Nothing to sign up for and no way for strangers to talk to your child."),
    ("10 languages",
     "English, French, German, Spanish, Portuguese, Russian, Japanese, Korean, and Chinese (simplified and "
     "traditional)."),
]


def home():
    shots = "\n".join(
        f'    <figure><img src="../{rel}" alt="{esc(alt)}" loading="lazy" width="{w}" height="{h}"></figure>'
        for rel, alt, w, h in (shot(i) for i in range(1, len(SCREENSHOTS) + 1)))
    cards = "\n".join(
        f'      <div class="card"><div class="emoji" aria-hidden="true">{emoji}</div><h3>{esc(title)}</h3><p>{esc(text)}</p></div>'
        for emoji, title, text in CARDS)
    regions = "\n".join(
        f'      <li style="--c: {colour}"><span class="planet" aria-hidden="true"></span><b>{esc(name)}</b>'
        f'<span>{levels} levels</span><span class="boss">Boss: {esc(boss)}</span></li>'
        for name, levels, boss, colour in REGIONS)
    checks = "\n".join(
        f'        <li><span class="dot" aria-hidden="true">✓</span><div><b>{esc(title)}</b><span class="txt">{esc(text)}</span></div></li>'
        for title, text in CHECKS)
    levels = sum(r[1] for r in REGIONS)
    lw, lh = image_size(IMG + "logo.webp", (640, 309))
    return f"""
<section class="hero space-bg">
  <div class="wrap">
    <div>
      <h1 class="hero-logo"><img src="../{IMG}logo.webp" alt="Orbit Smash" width="{lw}" height="{lh}" fetchpriority="high"></h1>
      <p class="tagline">Swing the hammer, save the planet!</p>
      <p class="lead">Asteroids, comets and silly aliens are flying at the Earth, and only your hammer can stop them. Touch anywhere around the planet to swing, smash them all before they land, and fly region by region across space.</p>
      <div class="ctas">
        {store_buttons(ORBIT)}
      </div>
    </div>
    <div class="art"><img src="../{IMG}icon-512.webp" alt="The Orbit Smash icon: a smiling Earth with a big hammer" width="320" height="320"></div>
  </div>
</section>

<section id="play">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The game</span>
      <h2>Touch, swing, SMASH!</h2>
      <p>Touch anywhere around the Earth and the hammer swings there. A gentle touch blocks, a fast swing smashes, and an even faster one makes a MEGA hit!</p>
    </div>
  </div>
  <div class="shots" tabindex="0" role="region" aria-label="Screenshots of Orbit Smash">
{shots}
  </div>
  <div class="wrap">
    <div class="grid spaced">
{cards}
    </div>
  </div>
</section>

<section id="regions" class="space-bg regions-band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The Journey</span>
      <h2>{len(REGIONS)} regions, {levels} levels</h2>
      <p>Each region of space brings its own Earth, music, weather and a special alien, and ends with a boss fight.</p>
    </div>
    <ol class="regions">
{regions}
    </ol>
    <p class="regions-more">Plus the Kids land for little players, and a Monthly map with a new level every day.</p>
  </div>
</section>

<section id="families">
  <div class="wrap families">
    <img class="feature-img" src="../{IMG}feature.webp" alt="Orbit Smash: the smiling Earth swings its hammer at an angry asteroid, an alien in a saucer and a comet" loading="lazy" width="1024" height="500">
    <div>
      <span class="eyebrow">For the whole family</span>
      <h2>Made for everyone</h2>
      <ul class="checks">
{checks}
      </ul>
    </div>
  </div>
</section>

<section id="support" class="tight-top">
  <div class="wrap duo">
    <div class="card premium">
      <div class="emoji" aria-hidden="true">👑</div>
      <h3>Free to play</h3>
      <p>Orbit Smash is free to play, with optional in-app purchases. The Premium Pass, monthly or yearly, is optional too: it removes all the ads, unlocks every season's premium rewards and gives the video rewards without watching. It renews until you cancel it in Google Play or the App Store.</p>
    </div>
    <div class="card support">
      <div class="emoji" aria-hidden="true">💌</div>
      <h3>Need help?</h3>
      <p>Questions, ideas or a problem with a purchase? We read every message.</p>
      <a class="mail" href="mailto:{SUPPORT}">{SUPPORT}</a>
      <p class="card-links"><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms of Use</a></p>
    </div>
  </div>
</section>
"""


def main():
    build_images()
    common = dict(root="../", body_class="theme-orbit", theme="#2b2f6b",
                  brand=game_brand("./", f"../{IMG}icon-256.webp", ORBIT["name"]),
                  icon=IMG + "favicon-64.png", apple=IMG + "apple-touch-icon.png")
    write("orbitsmash/index.html", page(
        title="Orbit Smash by GuGo Studios: Swing the Hammer, Save the Planet",
        description="Orbit Smash is a cute space arcade game: swing your hammer around the Earth and smash the "
                    "asteroids, comets and silly aliens flying at it, across 49 levels and 7 regions of space.",
        path="/orbitsmash/",
        og=("Orbit Smash", "Swing your hammer around the Earth and smash the space rocks before they land!",
            IMG + "og-image.jpg"),
        nav=[("The game", "#play", True, False), ("Regions", "#regions", True, False),
             ("Families", "#families", True, False), ("All games", "../#games", False, False)],
        main=home(),
        **common))
    for name, title in (("privacy", "Privacy Policy"), ("terms", "Terms of Use")):
        body = open(os.path.join(ROOT, "legal", "orbitsmash", name + ".html"), encoding="utf-8").read().strip()
        write(f"orbitsmash/{name}.html", page(
            title=f"{title} - Orbit Smash",
            description=f"{title} for the Orbit Smash game.",
            path=f"/orbitsmash/{name}.html",
            nav=[("Privacy", "privacy.html", True, name == "privacy"),
                 ("Terms", "terms.html", True, name == "terms"),
                 ("All games", "../#games", False, False)],
            main=body,
            main_class="legal",
            **common))


if __name__ == "__main__":
    main()
