"""Builds every SVG in ../assets. Run: python scripts/build.py"""

import pathlib

import cards
import hero
from svgkit import C, Svg, width, wrap

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

PROJECTS = [
    ("ajha", "Proyecto de grado", "AjHA · Suite E2E",
     "Pruebas end-to-end del sistema de ajuste de horario académico de Uniandes: "
     "inscripción, correquisitos, créditos y gestión de solicitudes, escritas como escenarios BDD.",
     ["Kraken", "WebdriverIO", "Gherkin", "Node.js"], C["green"], "tests", "91 features"),
    ("banco-andes", "Multiagente · LLM", "Banco Andes",
     "Asistente financiero con dos agentes que hablan por A2A. Memoria persistente, ReAct, "
     "Tree of Thoughts y una política en PostgreSQL que decide; el modelo solo propone.",
     ["LangGraph", "MCP", "FastAPI", "PostgreSQL", "Docker"], C["violet"], "agents", "2 agentes"),
    ("creaspider", "EdTech · Python en el navegador", "CreaSpider",
     "Mini IDE para aprender Python programando una araña. Python real con Pyodide en un "
     "Web Worker y una vista 3D con un raycaster DDA escrito a mano.",
     ["React 19", "Pyodide", "CodeMirror 6", "GSAP"], C["orange"], "grid", "demo ↗"),
    ("recrea", "Física · Juego de puzzles", "ReCREA tu luz",
     "Óptica con física de verdad: Snell con dispersión de Cauchy, Fresnel, polarización con "
     "Malus y Beer-Lambert. Un prisma abre el arcoíris sin trucos de dibujo.",
     ["React 19", "Canvas 2D", "TypeScript"], C["rose"], "prism", "demo ↗"),
    ("secrelogic", "Juego tipo Karel · DISC", "SecreLogic",
     "Se programa en Python o con bloques, y una foto de bloques físicos se vuelve código con "
     "OCR local. Arquitectura hexagonal y backend con calificador automático.",
     ["Pyodide", "Tesseract.js", "NestJS", "Docker"], C["teal"], "blocks", "en desarrollo"),
    ("motor3d", "3D · Impresión", "CORE / STUDIO",
     "Editor 3D en el navegador para la Prusa CORE One: plantillas paramétricas, imagen a "
     "sólido, soportes automáticos en un worker y exportación STL.",
     ["three.js", "React 19", "Cloudflare Workers"], C["sky"], "cube", "editor 3D"),
]

MINIS = [
    ("creacut", "Pipeline de video", "CREAcut",
     "Video en pantalla verde + guion → corte final pulido, de forma automática.", C["amber"], "film"),
    ("cansat", "Estación terrena", "CanSat Ground",
     "Telemetría en vivo por Web Serial, gráficas y orientación 3D del satélite.", C["sky"], "sat"),
    ("hardening", "Ciberseguridad", "Hardening Linux",
     "Ubuntu asegurado desde Kali: SSH solo con llave, iptables en DROP, AIDE y Lynis.", C["green"], "shield"),
]

STACK = [
    ("Frontend & 3D", C["orange"], ["TypeScript", "React 19", "Angular", "Next.js", "Vite", "Tailwind 4",
                                    "three.js", "Canvas 2D", "GSAP", "CodeMirror 6"]),
    ("Backend & Cloud", C["sky"], ["Node.js", "NestJS", "FastAPI", "Python", "Java", "Go", "PostgreSQL",
                                   "TypeORM", "Docker", "Cloudflare Workers"]),
    ("IA & Agentes", C["violet"], ["LangGraph", "MCP", "A2A · JSON-RPC", "RAG", "Ollama", "LangSmith",
                                   "ReAct", "Tree of Thoughts"]),
    ("Calidad", C["green"], ["Kraken", "WebdriverIO", "Gherkin · BDD", "Page Objects", "Pytest",
                             "GitHub Actions"]),
    ("Arquitectura", C["amber"], ["Hexagonal", "Microservicios", "Command · Observer", "Web Workers",
                                  "Pyodide", "Tesseract.js"]),
    ("Seguridad", C["rose"], ["Linux", "Kali", "SSH", "iptables", "AIDE", "Lynis", "AppArmor"]),
]

SEMESTER = [
    ("01", "Proyecto de grado", "Suite E2E de AjHA",
     "Pruebas automatizadas del sistema de ajuste de horario de Uniandes, en ciclos de cuatro semanas. "
     "Las mantendrá el equipo de QA de la Vicerrectoría de Transformación Digital.", "Kraken · BDD", C["green"]),
    ("02", "Coterminal MISO", "Agentes y LLM",
     "Banco Andes pasó de un agente con tools a un sistema multiagente con memoria, A2A y una política "
     "en PostgreSQL. CI en verde con 40 pruebas.", "LangGraph · MCP", C["violet"]),
    ("03", "Ciberseguridad", "Aseguramiento de hosts",
     "Diagnóstico y hardening de un servidor Ubuntu desde Kali, con auditoría de integridad y "
     "evidencias del antes y el después.", "Linux · Kali", C["rose"]),
]


def stack(path):
    w, row, top = 1000, 58, 34
    h = top * 2 + row * len(STACK) - 14
    s = Svg(w, h, "Stack técnico: " + "; ".join(f"{g}: {', '.join(items)}" for g, _, items in STACK))
    s.add(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="{C["surface"]}" stroke="{C["line"]}"/>')
    for i, (group, col, items) in enumerate(STACK):
        y = top + i * row
        if i:
            s.add(f'<path d="M32 {y - 15}H{w - 32}" stroke="{C["line"]}" stroke-dasharray="2 5"/>')
        s.add(f'<rect x="32" y="{y + 9}" width="8" height="8" rx="2" fill="{col}"/>')
        s.text(50, y + 18, group, "sans-b", 16, C["text"])
        x = 210
        for it in items:
            cw = width(it, "mono", 13) + 22
            if x + cw > w - 32:
                break
            x += s.chip(x, y, it, C["soft"], size=13, pad=11, h=27) + 8
    s.save(path)


def semester(path):
    w, h, gap = 1000, 258, 16
    cw = (w - gap * 2) / 3
    s = Svg(w, h, "Este semestre: " + "; ".join(f"{t}: {d}" for _, _, t, d, _, _ in SEMESTER))
    for i, (num, kicker, title, desc, tag, col) in enumerate(SEMESTER):
        x = i * (cw + gap)
        s.add(f'<rect x="{x + .5}" y=".5" width="{cw - 1}" height="{h - 1}" rx="16" fill="{C["surface"]}" stroke="{C["line"]}"/>')
        s.text(x + 24, 52, num, "display", 34, col)
        s.text(x + 24 + width(num, "display", 34) + 12, 50, kicker.upper(), "mono-m", 11.5, C["muted"],
               extra='letter-spacing="1.4"')
        s.text(x + 24, 88, title, "sans-b", 20, C["text"])
        for j, line in enumerate(wrap(desc, "sans", 14.5, cw - 48)[:5]):
            s.text(x + 24, 116 + j * 21, line, "sans", 14.5, "#A9AEBA")
        s.chip(x + 24, h - 46, tag, col, size=12, h=24, fill=C["raised"])
    s.save(path)


def button(path, label, icon, color):
    h = 44
    w = width(label, "sans-m", 15) + 66
    s = Svg(round(w), h, label)
    s.add(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{h / 2}" fill="{C["surface"]}" stroke="{C["line2"]}"/>')
    s.add(f'<g transform="translate(16 12)" fill="none" stroke="{color}" stroke-width="1.7" '
          f'stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
    s.text(46, 27.5, label, "sans-m", 15, C["text"])
    s.save(path)


def footer(path):
    w, h = 1000, 70
    s = Svg(w, h, "Hecho en Bogotá")
    s.defs.append(f'<linearGradient id="l" x1="0" x2="1"><stop stop-color="{C["amber"]}" stop-opacity="0"/>'
                  f'<stop offset=".5" stop-color="{C["amber"]}"/><stop offset="1" stop-color="{C["amber"]}" stop-opacity="0"/></linearGradient>')
    s.add(f'<rect x="100" y="10" width="800" height="1.5" fill="url(#l)"/>')
    s.add(f'<circle cx="500" cy="10.75" r="3.5" fill="{C["amber"]}"><animate attributeName="cx" values="140;860;140" '
          'dur="8s" repeatCount="indefinite"/></circle>')
    s.text(500, 50, "hecho en bogotá  ·  universidad de los andes  ·  2026", "mono", 13, C["muted"], anchor="middle",
           extra='letter-spacing="1"')
    s.save(path)


ICON_LINKEDIN = ('<rect x="0" y="0" width="20" height="20" rx="4.5"/><path d="M6 9v6M6 5.6v.1M10 15v-6M10 11.5c0-1.6 1.2-2.6 2.5-2.6'
                 's2.5.9 2.5 2.6V15"/>')
ICON_MAIL = '<rect x="0" y="2" width="20" height="16" rx="3.5"/><path d="M1 4.5l9 6.5l9-6.5"/>'
ICON_CAP = '<path d="M10 2L0 7l10 5l10-5z"/><path d="M4 9.2v4.8c3.5 3 8.5 3 12 0V9.2M20 7v6"/>'


def main():
    OUT.mkdir(exist_ok=True)
    hero.build(OUT / "hero.svg")
    for slug, *rest in PROJECTS:
        cards.project(OUT / f"card-{slug}.svg", *rest, live=rest[-1].startswith("demo"))
    for slug, kicker, title, desc, col, icon in MINIS:
        cards.mini(OUT / f"mini-{slug}.svg", kicker, title, desc, col, cards.ICONS[icon])
    stack(OUT / "stack.svg")
    semester(OUT / "semester.svg")
    button(OUT / "btn-linkedin.svg", "LinkedIn", ICON_LINKEDIN, C["sky"])
    button(OUT / "btn-gmail.svg", "ajpp2803@gmail.com", ICON_MAIL, C["amber"])
    button(OUT / "btn-uniandes.svg", "a.penarandap@uniandes.edu.co", ICON_CAP, C["amber"])
    footer(OUT / "footer.svg")
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:28} {f.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
