"""Builds the profile images from real screenshots.

1. Crops each source picture into .preview/frames/.
2. Writes one HTML page per image into .preview/render/.
3. scripts/render.mjs screenshots those pages into assets/.

Run: python scripts/compose.py && node scripts/render.mjs
"""

import html
import pathlib
import shutil

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = pathlib.Path("C:/Users/ajpp2/Documents")
PORT = DOCS / "Proyectos/Personales/portafolio/public/projects"
SHOTS = ROOT / ".preview/shots"
SLIDES = DOCS / "Universidad/Agentes MISW4412/Presentacion-Entrega-Final-Semana8/diapositivas_png"
FRAMES = ROOT / ".preview/frames"
RENDER = ROOT / ".preview/render"

# name: (source, crop box in source pixels or None)
SOURCES = {
    "banco-logs": (SLIDES / "slide-09.png", (102, 292, 1152, 654)),
    "beania": (SHOTS / "beania.png", None),
    "crea-talleres": (SHOTS / "crea-talleres.png", None),
    "spider-lesson": (PORT / "creaspider/lesson.webp", None),
}

# Four projects, agents first: (slug, title, one line, frame)
TILES = [
    ("banco-andes", "Banco Andes", "Dos agentes de IA que evalúan un crédito", "banco-logs"),
    ("beania", "Sé una IA por un d-IA", "Personas que juegan a ser un agente", "beania"),
    ("crea-web", "Página web CREA", "El sitio del laboratorio CREA de Uniandes", "crea-talleres"),
    ("creaspider", "CreaSpider", "Aprender Python moviendo una araña", "spider-lesson"),
]

CSS = """
:root{--bg:#161c1a;--ink:#e3e2da;--muted:#8e948d}
*{box-sizing:border-box}
body{margin:0;background:#000}
.frame{background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',sans-serif;
  -webkit-font-smoothing:antialiased;letter-spacing:-.005em}
img{display:block}
p{margin:0}
"""

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500&display=block" rel="stylesheet">'
        '<style>{css}</style></head><body>{body}</body></html>')


def crop_frames():
    FRAMES.mkdir(parents=True, exist_ok=True)
    for name, (src, box) in SOURCES.items():
        im = Image.open(src).convert("RGB")
        if box:
            im = im.crop(box)
        im.thumbnail((1400, 1400))
        im.save(FRAMES / f"{name}.jpg", quality=92)


def page(name, body, css):
    (RENDER / f"{name}.html").write_text(HEAD.format(css=CSS + css, body=body), encoding="utf-8")


def hero():
    body = """<div class="frame hero">
  <h1>Angel Peñaranda</h1>
  <p class="what">Ingeniero de software. Hago agentes de IA y webs para aprender.</p>
  <p class="where">Universidad de los Andes · Bogotá</p>
</div>"""
    css = """
.hero{width:1000px;padding:64px 40px 60px}
h1{font-weight:500;font-size:112px;line-height:.9;letter-spacing:-.05em;margin:0 0 40px -4px}
.what{font-size:24px;line-height:1.35}
.where{font-size:24px;line-height:1.35;color:var(--muted)}
"""
    page("hero", body, css)


def tiles():
    for slug, title, line, frame in TILES:
        body = f"""<div class="frame tile">
  <div class="pic" style="background-image:url('../frames/{frame}.jpg');background-position:{'left' if slug == 'banco-andes' else 'center'} top"></div>
  <p class="title">{html.escape(title)}</p>
  <p class="line">{html.escape(line)}</p>
</div>"""
        css = """
.tile{width:480px;padding-bottom:26px}
.pic{width:480px;height:300px;background-size:cover}
.title{font-weight:500;font-size:22px;letter-spacing:-.02em;margin:20px 22px 4px}
.line{font-size:17px;color:var(--muted);margin:0 22px}
"""
        page(f"tile-{slug}", body, css)


if __name__ == "__main__":
    shutil.rmtree(RENDER, ignore_errors=True)
    RENDER.mkdir(parents=True)
    crop_frames()
    hero()
    tiles()
    print("pages:", ", ".join(p.stem for p in sorted(RENDER.glob("*.html"))))
