"""Small toolkit to write self-contained SVGs for the GitHub profile.

GitHub shows README images through <img>, so an SVG cannot load web fonts.
Each SVG embeds a subset of the fonts it uses (only the glyphs it needs),
encoded as WOFF in a data URI.
"""

import base64
import io
import pathlib
import re
import urllib.request
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / ".fonts"

FONTS = {
    "display": ("Bricolage Grotesque", "opsz,wght@96,800", 800),
    "sans": ("Geist", "wght@400", 400),
    "sans-m": ("Geist", "wght@500", 500),
    "sans-b": ("Geist", "wght@600", 600),
    "mono": ("Geist Mono", "wght@400", 400),
    "mono-m": ("Geist Mono", "wght@500", 500),
}

# Palette shared by every SVG.
C = {
    "bg": "#0A0B0F",
    "surface": "#0F1117",
    "raised": "#151821",
    "line": "#22252F",
    "line2": "#2E3240",
    "text": "#EEF0F4",
    "soft": "#C4C8D2",
    "muted": "#868C9A",
    "faint": "#4A4F5C",
    "amber": "#FFC53D",
    "amber2": "#FF9F1C",
    "green": "#4ADE80",
    "sky": "#60A5FA",
    "violet": "#A78BFA",
    "rose": "#FB7185",
    "teal": "#2DD4BF",
    "orange": "#FB923C",
}


def _font_path(key):
    family, axes, weight = FONTS[key]
    path = CACHE / f"{family.replace(' ', '')}-{weight}.ttf"
    if path.exists():
        return path
    CACHE.mkdir(exist_ok=True)
    url = (
        "https://fonts.googleapis.com/css2?family="
        + family.replace(" ", "+")
        + ":"
        + axes
    )
    css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "python"})).read().decode()
    ttf = re.search(r"url\((https://[^)]+\.ttf)\)", css).group(1)
    path.write_bytes(urllib.request.urlopen(ttf).read())
    return path


_loaded = {}


def font(key):
    if key not in _loaded:
        _loaded[key] = TTFont(_font_path(key))
    return _loaded[key]


def width(text, key, size):
    """Advance width of `text` in px (no kerning)."""
    f = font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    total = 0
    for ch in text:
        glyph = cmap.get(ord(ch)) or cmap.get(ord("?"))
        total += hmtx[glyph][0]
    return total * size / upm


def wrap(text, key, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and width(trial, key, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def _embed(key, chars):
    f = TTFont(_font_path(key))
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff"
    f.save(buf)
    family, _, weight = FONTS[key]
    data = base64.b64encode(buf.getvalue()).decode()
    return (
        f"@font-face{{font-family:'{key}';font-weight:{weight};"
        f"src:url(data:font/woff;base64,{data}) format('woff');}}"
    )


FALLBACK = {
    "display": "'Segoe UI',Helvetica,Arial,sans-serif",
    "sans": "'Segoe UI',Helvetica,Arial,sans-serif",
    "mono": "ui-monospace,Consolas,'Courier New',monospace",
}


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.defs, self.body, self.css = [], [], []
        self.used = {}

    def add(self, s):
        self.body.append(s)
        return self

    def text(self, x, y, s, key="sans", size=16, fill=C["text"], anchor="start", extra=""):
        self.used.setdefault(key, set()).update(s)
        fam = key.split("-")[0]
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        self.body.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="\'{key}\',{FALLBACK[fam]}" '
            f'font-weight="{FONTS[key][2]}" font-size="{size}" fill="{fill}"{a} {extra}>{escape(s)}</text>'
        )
        return self

    def chip(self, x, y, label, color=C["soft"], key="mono", size=13, pad=10, h=26, fill=None, lead=0):
        """Outlined pill; returns its width so callers can lay chips in a row."""
        w = width(label, key, size) + pad * 2 + lead
        bg = fill or C["raised"]
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{bg}" stroke="{C["line2"]}"/>')
        self.text(x + pad + lead, y + h / 2 + size * 0.36, label, key, size, color)
        return w

    def render(self):
        faces = "".join(_embed(k, v) for k, v in self.used.items())
        style = f"<style>{faces}{''.join(self.css)}</style>"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
            f"<title>{escape(self.title)}</title>{style}<defs>{''.join(self.defs)}</defs>"
            f"{''.join(self.body)}</svg>"
        )

    def save(self, path):
        pathlib.Path(path).write_text(self.render(), encoding="utf-8")
