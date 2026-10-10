"""Builds site/privacy.html and site/terms.html from the texts in legal/*.html (just the <main> content), inside the
site's header and footer.

    python tools/gen_legal_pages.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Drip Drop Garden</title>
<meta name="description" content="{title} for the Drip Drop Garden game.">
<meta name="theme-color" content="#149ba1">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><img src="assets/img/icon-192.png" alt=""><span>Drip Drop Garden</span></a>
    <nav class="nav">
      <a href="./">Home</a>
      <a class="optional" href="privacy.html">Privacy</a>
      <a class="optional" href="terms.html">Terms</a>
    </nav>
  </div>
</header>

<main class="legal">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 Drip Drop Garden</span>
    <nav>
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Use</a>
      <a href="mailto:support@dripdropgarden.com">Contact</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

for name, title in (("privacy", "Privacy Policy"), ("terms", "Terms of Use")):
    body = open(os.path.join(ROOT, "legal", name + ".html"), encoding="utf-8").read().strip()
    out = os.path.join(ROOT, "site", name + ".html")
    open(out, "w", encoding="utf-8").write(PAGE.format(title=title, body=body))
    print("wrote", out)
