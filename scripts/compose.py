"""Builds the profile images from real screenshots.

1. Crops each source picture into .preview/frames/.
2. Writes one HTML page per image into .preview/render/.
3. scripts/render.mjs screenshots those pages into assets/.

Run: python scripts/compose.py && node scripts/render.mjs
"""

import html
import pathlib

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
    "banco-sql": (SLIDES / "slide-08.png", (102, 288, 894, 619)),
    "banco-ci": (SLIDES / "slide-10.png", (102, 274, 1038, 470)),
    "beania": (SHOTS / "beania.png", None),
    "beania-title": (SHOTS / "beania.png", (250, 150, 1190, 420)),
    "video-docker": (SHOTS / "video-8.png", None),
    "video-arq": (SHOTS / "video-150.png", None),
    "video-term": (SHOTS / "video-90.png", None),
    "video-tabla": (SHOTS / "video-40.png", None),
    "crea-home": (SHOTS / "crea-home.png", None),
    "crea-talleres": (SHOTS / "crea-talleres.png", None),
    "crea-proyectos": (SHOTS / "crea-proyectos.png", None),
    "spider-hero": (PORT / "creaspider/hero.webp", None),
    "spider-lesson": (PORT / "creaspider/lesson.webp", None),
    "spider-cond": (PORT / "creaspider/cond.webp", None),
    "secre-landing": (PORT / "secrelogic/landing.webp", None),
    "secre-juego": (PORT / "secrelogic/juego.webp", None),
    "secre-login": (SHOTS / "secrelogic-live.png", None),
    "recrea-prism": (PORT / "recrea/prism.webp", None),
    "recrea-intro": (PORT / "recrea/intro.webp", None),
    "core-editor": (PORT / "motor3d/editor.webp", None),
    "core-landing": (PORT / "motor3d/landing.webp", None),
    "cut-intro": (PORT / "creacut/intro.webp", None),
    "cut-editor": (PORT / "creacut/editor.webp", None),
    "game-hero": (PORT / "creagame/hero.webp", None),
    "game-mario": (PORT / "creagame/juego-mario.webp", None),
    "game-mundo": (PORT / "creagame/tumundo.webp", None),
}

# The contact sheet: one run of frames per project, agents first.
SHEET = [
    ("Banco Andes", ["banco-logs", "banco-sql", "banco-ci"]),
    ("Sé una IA por un d-IA", ["beania", "beania-title"]),
    ("Videos que explican código", ["video-docker", "video-arq", "video-term", "video-tabla"]),
    ("Página web CREA", ["crea-home", "crea-talleres", "crea-proyectos"]),
    ("CreaSpider", ["spider-hero", "spider-lesson", "spider-cond"]),
    ("SecreLogic", ["secre-landing", "secre-juego", "secre-login"]),
    ("ReCREA tu luz", ["recrea-prism", "recrea-intro"]),
    ("CORE / STUDIO", ["core-editor", "core-landing"]),
    ("CREAcut", ["cut-intro", "cut-editor"]),
    ("CREA tu propio videojuego", ["game-hero", "game-mario", "game-mundo"]),
]

# Featured rows: (slug, title, text, stack, main frame, second frame or None)
ROWS = [
    ("banco-andes", "Banco Andes",
     "Un asistente financiero hecho de dos agentes que se hablan por la red con A2A. "
     "El segundo evalúa el riesgo con Tree of Thoughts, pero decide una política en "
     "PostgreSQL: el modelo propone, los datos mandan. Hice las tools, el servidor MCP "
     "y la arquitectura.",
     "LangGraph, MCP, A2A, FastAPI, PostgreSQL, Docker, Ollama. 40 pruebas en CI.",
     "banco-logs", "banco-ci"),
    ("beania", "Sé una IA\npor un d-IA",
     "Una actividad del laboratorio CREA en la que grupos de tres personas hacen de agente: "
     "una es el modelo, otra el arnés y otra el revisor, con memoria limitada, mientras "
     "construyen algo con las manos. Un PC sirve la sala y los iPads solo abren el navegador.",
     "Node.js, Socket.IO, Google Cloud. Hasta 50 personas a la vez.",
     "beania", None),
    ("videos", "Videos que explican código",
     "Le paso un archivo o una carpeta y sale un video narrado que lo explica línea por línea. "
     "Un modelo local escribe el guion en JSON validado, Manim lo anima y el código se ejecuta "
     "de verdad, así que la salida que se ve en pantalla es la real.",
     "Python, Ollama con Gemma, Manim, VoiceStudio, una skill para Claude Code.",
     "video-term", "video-arq"),
    ("crea-web", "Página web CREA",
     "El sitio del laboratorio CREA de Uniandes: talleres para niñas, niños y jóvenes, "
     "proyectos y equipo, con aire de cuaderno de inventor. Muchos visitantes llegan desde "
     "equipos modestos, así que el inicio bajó de 68 MB a 0,8 MB.",
     "React, Vite, Tailwind 4, FastAPI, Apache.",
     "crea-talleres", "crea-home"),
    ("creaspider", "CreaSpider",
     "Un IDE para aprender Python moviendo una araña. Es Python real, con Pyodide en un "
     "Web Worker, y la vista 3D es un raycaster DDA escrito a mano, sin motor.",
     "React 19, TypeScript, Pyodide, CodeMirror 6, GSAP.",
     "spider-lesson", "spider-hero"),
    ("secrelogic", "SecreLogic",
     "Un juego tipo Karel para el departamento de Sistemas. Se programa en Python o con "
     "bloques, y una foto de bloques de papel se convierte en código con OCR local. "
     "Tiene backend propio con calificador automático.",
     "TypeScript, Pyodide, Tesseract.js, NestJS, TypeORM, Docker.",
     "secre-juego", "secre-login"),
]

CSS = """
:root{--bg:#161c1a;--surface:#1f2725;--ink:#e3e2da;--muted:#8e948d;--accent:#9fc7b8}
*{box-sizing:border-box}
body{margin:0;background:#000}
.frame{width:1000px;background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',sans-serif;
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


def img(name, cls=""):
    return f'<img class="{cls}" src="../frames/{name}.jpg" alt="">'


def page(name, body, css):
    RENDER.mkdir(parents=True, exist_ok=True)
    (RENDER / f"{name}.html").write_text(HEAD.format(css=CSS + css, body=body), encoding="utf-8")


def hero():
    runs = "".join(
        f'<div class="run"><p>{html.escape(title)}</p><div class="strip">{"".join(img(f) for f in frames)}</div></div>'
        for title, frames in SHEET)
    body = f"""<div class="frame hero">
  <h1>Angel Peñaranda</h1>
  <div class="band">
    <p>Ingeniero de software en Bogotá.</p>
    <p>Termino Ingeniería de Sistemas y Computación en la Universidad de los Andes y hago el
       coterminal de la Maestría en Ingeniería de Software.</p>
    <p>Agentes de IA<br>Webs para aprender<br>3D y física en el navegador<br>Pruebas end-to-end</p>
    <p class="soft">Lo que sigue son pantallas reales de lo que he construido este año.</p>
  </div>
  <div class="sheet">{runs}</div>
</div>"""
    css = """
.hero{padding:30px 28px 34px}
h1{font-weight:500;font-size:118px;line-height:.9;letter-spacing:-.05em;margin:0 0 30px -4px}
.band{display:grid;grid-template-columns:1fr 1.7fr 1.1fr 1.1fr;gap:22px;font-size:16px;line-height:1.45;margin-bottom:46px}
.soft{color:var(--muted)}
.sheet{display:flex;flex-wrap:wrap;gap:22px 16px}
.run p{font-size:14px;line-height:1;margin-bottom:8px}
.strip{display:flex;gap:6px}
.strip img{height:86px;width:auto}
"""
    page("hero", body, css)


def rows():
    for i, (slug, title, text, stack, main, second) in enumerate(ROWS):
        flip = " flip" if i % 2 else ""
        extra = img(second, "second") if second else ""
        body = f"""<div class="frame row{flip}">
  <div class="pics">{img(main, "main")}{extra}</div>
  <div class="text"><h2>{html.escape(title).replace(chr(10), "<br>")}</h2><p>{html.escape(text)}</p><p class="stack">{html.escape(stack)}</p></div>
</div>"""
        css = """
.row{display:grid;grid-template-columns:560px 1fr;gap:36px;padding:28px;align-items:start}
.row.flip{grid-template-columns:1fr 560px}
.row.flip .pics{order:2}
.pics{display:flex;flex-direction:column;gap:8px}
.pics .main{width:560px;height:auto}
.pics .second{width:276px;height:auto}
.row.flip .pics .second{align-self:flex-end}
h2{font-weight:500;font-size:44px;line-height:.95;letter-spacing:-.04em;margin:4px 0 22px}
.text p{font-size:17px;line-height:1.5}
.text .stack{color:var(--muted);font-size:15px;margin-top:18px}
"""
        page(f"row-{slug}", body, css)


def footer():
    body = """<div class="frame foot">
  <p class="name">Angel Peñaranda</p>
  <p class="line">Bogotá · Universidad de los Andes · 2026</p>
</div>"""
    css = """
.foot{background:var(--accent);color:var(--bg);padding:40px 28px 30px}
.name{font-weight:500;font-size:131px;line-height:.85;letter-spacing:-.055em;margin-left:-6px}
.line{font-size:16px;margin-top:26px}
"""
    page("footer", body, css)


if __name__ == "__main__":
    crop_frames()
    hero()
    rows()
    footer()
    print("pages:", ", ".join(p.stem for p in sorted(RENDER.glob("*.html"))))
