"""Builds Drip Drop Garden's site/privacy.html and site/terms.html from the texts in legal/*.html (just the <main>
content), inside the site's header and footer (tools/site_common.py). The game and its store listing link to
https://gugostudios.com/privacy.html and /terms.html: keep those paths.

    python tools/gen_legal_pages.py
"""
import os

from site_common import GAME, ROOT, game_brand, page, write

DDG = GAME["dripdropgarden"]

for name, title in (("privacy", "Privacy Policy"), ("terms", "Terms of Use")):
    body = open(os.path.join(ROOT, "legal", name + ".html"), encoding="utf-8").read().strip()
    write(name + ".html", page(
        title=f"{title} - Drip Drop Garden",
        description=f"{title} for the Drip Drop Garden game.",
        root="",
        path=f"/{name}.html",
        brand=game_brand(DDG["page"], "assets/img/icon-192.png", DDG["name"]),
        nav=[("Privacy", "privacy.html", True, name == "privacy"),
             ("Terms", "terms.html", True, name == "terms"),
             ("All games", "./#games", False, False)],
        main=body,
        main_class="legal",
    ))
