"""Checks the site before a push: every link and image in site/*.html and site/assets/*.css that points inside the site
(relative, /..., or https://gugostudios.com/...) must exist, #anchors included; every address in sitemap.xml must exist;
and every file of site/ in the last commit must still be there (the games and their store listings link to some of them,
like /privacy.html, /terms.html and /orbitsmash/privacy.html; AdMob reads /app-ads.txt).

    python tools/check_links.py

Prints what's wrong and exits with 1, or prints a summary and exits with 0.
"""
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
DOMAIN = "gugostudios.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append((tag, attrs[name]))
        if attrs.get("srcset"):
            for part in attrs["srcset"].split(","):
                if part.strip():
                    self.links.append((tag, part.strip().split()[0]))
        if tag == "meta" and attrs.get("content", "").startswith("https://" + DOMAIN):
            self.links.append((tag, attrs["content"]))


def site_files():
    for folder, _dirs, files in os.walk(SITE):
        for f in files:
            yield os.path.join(folder, f)


def target(base_dir, url):
    """The file in site/ a link points to and its #anchor, or None for a link that leaves the site."""
    parts = urlsplit(url)
    if parts.scheme in ("http", "https"):
        if parts.netloc != DOMAIN:
            return None
        path = parts.path or "/"
    elif parts.scheme or url.startswith("//"):
        return None  # mailto:, data:, another site
    else:
        path = parts.path
    if path.startswith("/"):
        file = os.path.join(SITE, unquote(path.lstrip("/")))
    elif path:
        file = os.path.join(base_dir, unquote(path))
    else:
        file = None  # just "#anchor": this page
    if file is not None:
        file = os.path.normpath(file)
        if path.endswith("/") or os.path.isdir(file):
            file = os.path.join(file, "index.html")
    return file, parts.fragment


def main():
    problems, pages, count = [], {}, 0
    for file in site_files():
        if file.endswith(".html"):
            p = Page()
            p.feed(open(file, encoding="utf-8").read())
            pages[os.path.normpath(file)] = p

    def check(source, base_dir, url, page_ids=None):
        nonlocal count
        t = target(base_dir, url)
        if t is None:
            return
        count += 1
        file, fragment = t
        where = os.path.relpath(source, SITE).replace("\\", "/")
        if file is not None and not file.startswith(SITE):
            problems.append(f"{where}: {url} points outside site/")
            return
        if file is not None and not os.path.isfile(file):
            problems.append(f"{where}: {url} -> missing {os.path.relpath(file, SITE)}")
            return
        if fragment:
            ids = page_ids if file is None else (pages[file].ids if file in pages else None)
            if ids is not None and fragment not in ids:
                problems.append(f"{where}: {url} -> no id=\"{fragment}\"")

    for file, p in pages.items():
        for _tag, url in p.links:
            check(file, os.path.dirname(file), url, p.ids)
    for file in site_files():
        if file.endswith(".css"):
            for url in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", open(file, encoding="utf-8").read()):
                check(file, os.path.dirname(file), url)
    sitemap = os.path.join(SITE, "sitemap.xml")
    for url in re.findall(r"<loc>([^<]+)</loc>", open(sitemap, encoding="utf-8").read()):
        check(sitemap, SITE, url)

    # Every file of site/ in the last commit is still there.
    kept = 0
    try:
        tracked = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "site/"], cwd=ROOT,
                                 capture_output=True, text=True, check=True).stdout.split()
        for rel in tracked:
            kept += 1
            if not os.path.isfile(os.path.join(ROOT, rel)):
                problems.append(f"{rel} was in the last commit but is gone (an old address would break)")
        changed = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "site/app-ads.txt", "site/CNAME"],
                                 cwd=ROOT).returncode
        if changed:
            print("note: app-ads.txt or CNAME differs from the last commit")
    except (OSError, subprocess.CalledProcessError):
        print("note: git isn't available, skipped the check against the last commit")

    for p in problems:
        print("BROKEN", p)
    print(f"{len(pages)} pages, {count} links inside the site checked, {kept} committed files still there, "
          f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
