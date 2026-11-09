"""Builds the profile images from real screenshots.

1. Crops each source picture into .preview/frames/.
2. Writes one HTML page per image into .preview/render/.
3. scripts/render.mjs screenshots those pages into assets/.

Run: python scripts/compose.py && node scripts/render.mjs
"""

import html
import pathlib
import re
import shutil

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = pathlib.Path("C:/Users/ajpp2/Documents")
PORT = DOCS / "Proyectos/Personales/portafolio/public/projects"
SHOTS = ROOT / ".preview/shots"
SLIDES = DOCS / "Universidad/Agentes MISW4412/Presentacion-Entrega-Final-Semana8/diapositivas_png"
GHERKIN = DOCS / "Proyectos/Universidad/AjHA-Kraken/features/individual/student/AJHA-005.feature"
FRAMES = ROOT / ".preview/frames"
RENDER = ROOT / ".preview/render"

# name: (source, crop box in source pixels or None)
SOURCES = {
    "banco-logs": (SLIDES / "slide-09.png", (102, 292, 1152, 654)),
    "banco-ci": (SLIDES / "slide-10.png", (102, 274, 1038, 470)),
    "beania": (SHOTS / "beania.png", None),
    "video-term": (SHOTS / "video-90.png", None),
    "crea-talleres": (SHOTS / "crea-talleres.png", None),
    "spider-lesson": (PORT / "creaspider/lesson.webp", None),
    "secre-juego": (PORT / "secrelogic/juego.webp", None),
    "recrea-prism": (PORT / "recrea/prism.webp", None),
}

FEATURED = (
    "Banco Andes",
    "Asistente de orientación financiera hecho de dos agentes que se hablan por la red con A2A. "
    "El primero conversa y recuerda al cliente; el segundo evalúa el riesgo con Tree of Thoughts, "
    "y al final decide una política en PostgreSQL: el modelo propone, los datos mandan. "
    "Mi parte fueron las tools, el servidor MCP y la arquitectura.",
    "LangGraph, MCP, A2A, FastAPI, PostgreSQL, Docker, Ollama. 40 pruebas en CI.",
)

# (slug, title, explanation, stack, frame, crop anchor)
TILES = [
    ("beania", "Sé una IA por un d-IA",
     "Actividad del laboratorio CREA: grupos de tres personas hacen de agente de IA (modelo, "
     "arnés y revisor) con memoria limitada, mientras construyen algo con las manos.",
     "Node.js, Socket.IO, Google Cloud. Hasta 50 personas.", "beania", "center"),
    ("videos", "Videos que explican código",
     "Le das un archivo o una carpeta y sale un video narrado que lo explica línea por línea. "
     "Un modelo local escribe el guion, Manim lo anima y el código se ejecuta de verdad.",
     "Python, Ollama, Manim, VoiceStudio, skill de Claude Code.", "video-term", "center"),
    ("crea-web", "Página web CREA",
     "El sitio del laboratorio CREA de Uniandes: talleres para niñas, niños y jóvenes, proyectos "
     "y equipo. Pensado para equipos modestos: el inicio bajó de 68 MB a 0,8 MB.",
     "React, Vite, Tailwind 4, FastAPI.", "crea-talleres", "top"),
    ("creaspider", "CreaSpider",
     "Un IDE para aprender Python moviendo una araña. Es Python real, con Pyodide en un Web "
     "Worker, y la vista 3D es un raycaster escrito a mano.",
     "React 19, TypeScript, Pyodide, CodeMirror 6.", "spider-lesson", "top"),
    ("secrelogic", "SecreLogic",
     "Juego tipo Karel para el departamento de Sistemas. Se programa en Python o con bloques, "
     "y una foto de bloques de papel se convierte en código con OCR.",
     "Pyodide, Tesseract.js, NestJS, Docker.", "secre-juego", "center"),
    ("recrea", "ReCREA tu luz",
     "Puzzles de óptica con física real: Snell con dispersión, Fresnel, polarización y "
     "absorción. Un prisma abre el arcoíris por sí solo, sin trucos de dibujo.",
     "React 19, Canvas 2D, TypeScript.", "recrea-prism", "center"),
]

SEMESTER = [
    ("Coterminal MISO", "Construcción de agentes y LLM",
     "Banco Andes empezó como un agente con tools y terminó como un sistema multiagente con "
     "memoria, A2A y una política en base de datos.", "LangGraph, MCP"),
    ("Ciberseguridad", "Aseguramiento de servidores",
     "Hardening de Ubuntu y Red Hat desde Kali: SSH solo con llave, firewall en DROP, SELinux y "
     "auditoría de integridad con AIDE y Lynis.", "Linux, Kali"),
]

CSS = """
:root{--bg:#161c1a;--surface:#1f2725;--ink:#e3e2da;--muted:#8e948d;--accent:#9fc7b8}
*{box-sizing:border-box}
body{margin:0;background:#000}
.frame{background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',sans-serif;
  -webkit-font-smoothing:antialiased;letter-spacing:-.005em}
img{display:block}
p{margin:0}
h2{font-weight:500;letter-spacing:-.035em;margin:0}
.muted{color:var(--muted)}
"""

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500'
        '&family=JetBrains+Mono:wght@400&display=block" rel="stylesheet">'
        '<style>{css}</style></head><body>{body}</body></html>')

e = html.escape


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
  <div class="cols">
    <p>Ingeniero de software en Bogotá. Me gusta construir el sistema completo y probarlo de punta a punta.</p>
    <p>Último semestre (<span class="nw">2026-20</span>) de Ingeniería de Sistemas y Computación en la Universidad de los Andes.</p>
    <p>Coterminal en la Maestría en Ingeniería de Software (MISO).</p>
  </div>
  <p class="muted focus">Agentes de IA, webs para aprender, 3D en el navegador y pruebas end-to-end.</p>
</div>"""
    css = """
.hero{width:1000px;padding:60px 40px 52px}
h1{font-weight:500;font-size:112px;line-height:.9;letter-spacing:-.05em;margin:0 0 44px -4px}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;font-size:19px;line-height:1.45}
.focus{font-size:19px;margin-top:28px}
.nw{white-space:nowrap}
"""
    page("hero", body, css)


def featured():
    title, text, stack = FEATURED
    body = f"""<div class="frame feat">
  <div class="pics"><img class="main" src="../frames/banco-logs.jpg"><img class="second" src="../frames/banco-ci.jpg"></div>
  <div class="text"><h2>{e(title)}</h2><p>{e(text)}</p><p class="muted stack">{e(stack)}</p></div>
</div>"""
    css = """
.feat{width:1000px;display:grid;grid-template-columns:540px 1fr;gap:36px;padding:36px}
.pics{display:flex;flex-direction:column;gap:8px}
.main{width:540px}.second{width:290px}
h2{font-size:44px;line-height:.95;margin:2px 0 20px}
.text p{font-size:17px;line-height:1.5}
.stack{font-size:15px;margin-top:18px}
"""
    page("card-banco-andes", body, css)


def tiles():
    for slug, title, text, stack, frame, anchor in TILES:
        body = f"""<div class="frame tile">
  <div class="pic" style="background-image:url('../frames/{frame}.jpg');background-position:center {anchor}"></div>
  <div class="body"><h2>{e(title)}</h2><p>{e(text)}</p><p class="muted stack">{e(stack)}</p></div>
</div>"""
        css = """
.tile{width:480px;height:490px;display:flex;flex-direction:column}
.pic{height:270px;background-size:cover}
.body{flex:1;display:flex;flex-direction:column;padding:24px 26px 26px}
h2{font-size:28px;line-height:1;margin-bottom:14px}
.body p{font-size:16.5px;line-height:1.45}
.stack{margin-top:auto;padding-top:14px;font-size:14.5px}
"""
        page(f"card-{slug}", body, css)


def gherkin_html():
    out = []
    lines = GHERKIN.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("@"))
    for line in lines[start:]:
        line = line[2:]
        if not line.strip():
            out.append("")
            continue
        s = e(line)
        s = re.sub(r"^(\s*)(Feature:|Scenario:|Given|When|Then|And)",
                   r'\1<b>\2</b>', s)
        s = re.sub(r"(@\w+)", r'<i>\1</i>', s)
        out.append(s)
    return "\n".join(out)


def semester():
    cols = "".join(
        f'<div><p class="muted">{e(k)}</p><h3>{e(t)}</h3><p>{e(d)}</p><p class="muted tag">{e(g)}</p></div>'
        for k, t, d, g in SEMESTER)
    body = f"""<div class="frame sem">
  <div class="grado">
    <div><p class="muted">Proyecto de grado</p><h2>Suite end-to-end de AjHA</h2>
      <p>AjHA es el sistema con el que los estudiantes de Uniandes ajustan su horario. Escribí más de 90
      escenarios en Gherkin que lo recorren como un estudiante y como administrador: inscripción,
      correquisitos, créditos y solicitudes. Los va a mantener el equipo de QA de la Vicerrectoría
      de Transformación Digital.</p>
      <p class="muted tag">Kraken, WebdriverIO, Gherkin, Node.js</p></div>
    <pre>{gherkin_html()}</pre>
  </div>
  <div class="cols">{cols}</div>
</div>"""
    css = """
.sem{width:1000px;padding:40px 36px 40px}
.grado{display:grid;grid-template-columns:1fr 1.3fr;gap:32px;align-items:start}
.sem h2{font-size:36px;line-height:1;margin:8px 0 18px}
.sem h3{font-weight:500;font-size:24px;letter-spacing:-.02em;margin:8px 0 12px}
.sem p{font-size:16.5px;line-height:1.5}
.sem p.muted:first-child{font-size:16px}
.tag{margin-top:14px;font-size:14.5px}
pre{margin:0;background:var(--surface);padding:22px 24px;font:12px/1.7 'JetBrains Mono',monospace;
  color:var(--ink);white-space:pre-wrap}
pre b{font-weight:400;color:var(--accent)}
pre i{font-style:normal;color:var(--muted)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:48px}
"""
    page("semester", body, css)


if __name__ == "__main__":
    shutil.rmtree(RENDER, ignore_errors=True)
    RENDER.mkdir(parents=True)
    crop_frames()
    hero()
    featured()
    tiles()
    semester()
    print("pages:", ", ".join(p.stem for p in sorted(RENDER.glob("*.html"))))
