# gugostudios.com

The website of GuGo Studios and its games, Drip Drop Garden and Orbit Smash. Plain static files in `site/`, deployed to
GitHub Pages by `.github/workflows/deploy.yml` on every push to `main` (custom domain in `site/CNAME`).

| Address | File | Made by |
| --- | --- | --- |
| `/` | the studio's home page: a card per game | `tools/gen_studio_pages.py` |
| `/dripdropgarden/` | Drip Drop Garden's page (the home page until Orbit Smash came) | `tools/gen_studio_pages.py` |
| `/privacy.html`, `/terms.html` | Drip Drop Garden's privacy policy and terms | `tools/gen_legal_pages.py` from `legal/*.html` |
| `/orbitsmash/` | Orbit Smash's page | `tools/gen_orbit_pages.py` |
| `/orbitsmash/privacy.html`, `/orbitsmash/terms.html` | Orbit Smash's privacy policy and terms | `tools/gen_orbit_pages.py` from `legal/orbitsmash/*.html` |
| `/404.html`, `/sitemap.xml` | the "not found" page and the page list | `tools/gen_studio_pages.py` |
| `/app-ads.txt`, `/robots.txt`, `/CNAME` | AdMob's list, robots, the domain | by hand |

The games and their store listings link to `/privacy.html`, `/terms.html`, `/orbitsmash/privacy.html` and
`/orbitsmash/terms.html`, and AdMob reads `/app-ads.txt`: keep those paths. Old links to Drip Drop Garden's sections
on the home page (`/#play`, `/#families`, `/#support`) are sent on to `/dripdropgarden/`.

Never edit the generated `.html` files by hand: change the generators (or the texts in `legal/`) and run them again.

- `tools/site_common.py`: what every page shares: the head, the header, the footer (both games with their legal
  pages), and `GAMES`, where each game's store links go (`None` shows "Coming soon"; put the listing's address there
  once the game is public and the badges become "Get it on" buttons everywhere).
- `site/assets/site.css`: the styles (Orbit Smash's pages add the `theme-orbit` class for their space colours).
- Orbit Smash's screenshots: the `SCREENSHOTS` list at the top of `tools/gen_orbit_pages.py` (source picture + alt
  text; `CARD_SHOTS` picks the three on the home page's card). Change it and run the script again: it remakes
  `site/assets/img/orbitsmash/shot-N.webp` (at most 900 px tall) from the pictures, plus the icon, logo and feature
  graphic from the Unity project's `Docs/store`.
- Drip Drop Garden's images: `tools/build_assets.py` makes `site/assets/img` from the game's art (store graphics,
  loading screen, character cards); its screenshot alt texts are `DDG_SHOTS` in `tools/gen_studio_pages.py`.
- The studio's images (`site/assets/img/studio/`: logo, favicon, link preview) come from the GuGo Studios logo in the
  Drip Drop Garden Unity project, made by `tools/gen_studio_pages.py`.
- Support mail: support@gugostudios.com (Cloudflare Email Routing, forwarded to the owner's inbox).

Rebuild everything (the image steps need Pillow; without it the pages are still written and the images kept), then
check every link:

    python tools/gen_legal_pages.py
    uv run --with pillow python tools/gen_orbit_pages.py
    uv run --with pillow python tools/gen_studio_pages.py
    python tools/check_links.py

`check_links.py` checks that every link and image inside the site exists (anchors and sitemap included) and that every
file of `site/` in the last commit is still there.

Preview locally: `python -m http.server 8000 --directory site`, then open http://localhost:8000 (that server shows
its own error page for a missing address; GitHub Pages shows `404.html`, which you can open at /404.html).
