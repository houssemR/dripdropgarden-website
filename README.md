# gugostudios.com

The website of the game Drip Drop Garden: home page, privacy policy and terms of use. Plain static files in `site/`,
deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main` (custom domain in `site/CNAME`).

- `site/index.html`: the home page; `site/assets/site.css`: the styles.
- `legal/privacy.html`, `legal/terms.html`: the texts. After editing them run `python tools/gen_legal_pages.py`, which
  writes `site/privacy.html` and `site/terms.html` (keep the "last updated" date current). The game and the store
  listings link to `https://gugostudios.com/privacy.html` and `/terms.html`: keep those paths.
- `tools/build_assets.py`: makes `site/assets/img` from the game's art (the Unity project's store graphics, loading
  screen and character cards): `uv run --with pillow python tools/build_assets.py`.
- `site/app-ads.txt` (AdMob) goes next to `index.html` once the AdMob publisher id is known.
- Orbit Smash (the studio's second game): `site/orbitsmash/` (home, privacy, terms) built by
  `python tools/gen_orbit_pages.py` from `legal/orbitsmash/*.html`; its store listings link to
  `https://gugostudios.com/orbitsmash/privacy.html` and `/orbitsmash/terms.html`.
- Support mail: support@gugostudios.com (Cloudflare Email Routing, forwarded to the owner's inbox).

Preview locally: `python -m http.server 8000 --directory site`, then open http://localhost:8000.
