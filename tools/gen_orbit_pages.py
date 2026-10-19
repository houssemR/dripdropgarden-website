"""Builds Orbit Smash's pages under site/orbitsmash/: a small home page, the privacy policy and the terms of use (texts in
legal/orbitsmash/*.html, just the <main> content), in the site's look. The game and its store listings link to
https://gugostudios.com/orbitsmash/privacy.html and /orbitsmash/terms.html: keep those paths.

    python tools/gen_orbit_pages.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "site", "orbitsmash")

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}Orbit Smash</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#2b2f6b">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><img src="icon-192.png" alt=""><span>Orbit Smash</span></a>
    <nav class="nav">
      <a href="./">Home</a>
      <a class="optional" href="privacy.html">Privacy</a>
      <a class="optional" href="terms.html">Terms</a>
    </nav>
  </div>
</header>

<main class="{main_class}">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 GuGo Studios</span>
    <nav>
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Use</a>
      <a href="mailto:support@gugostudios.com">Contact</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

HOME = """<h1>Orbit Smash</h1>
<p><img src="logo.png" alt="Orbit Smash" style="max-width:100%;width:520px"></p>
<p>Protect the planet! Swing your hammer around the Earth and smash the asteroids, comets and silly aliens flying at it,
region by region across space. A cute, colourful arcade game for everyone, kids included.</p>
<p>Made by GuGo Studios. Questions: <a href="mailto:support@gugostudios.com">support@gugostudios.com</a></p>
<p><a href="privacy.html">Privacy Policy</a> &middot; <a href="terms.html">Terms of Use</a></p>
"""

os.makedirs(OUT, exist_ok=True)
pages = [("index", "", "Orbit Smash, a space arcade game by GuGo Studios.", "legal", HOME)]
for name, title in (("privacy", "Privacy Policy"), ("terms", "Terms of Use")):
    body = open(os.path.join(ROOT, "legal", "orbitsmash", name + ".html"), encoding="utf-8").read().strip()
    pages.append((name, title + " - ", f"{title} for the Orbit Smash game.", "legal", body))
for name, title, description, main_class, body in pages:
    path = os.path.join(OUT, name + ".html")
    open(path, "w", encoding="utf-8").write(PAGE.format(title=title, description=description, main_class=main_class, body=body))
    print("wrote", path)
