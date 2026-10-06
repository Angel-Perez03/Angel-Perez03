"""Animated hero banner: name, degree, and a terminal that types itself."""

import math

from svgkit import C, Svg, width

W, H = 1000, 400


def _ico_frames(cx, cy, r, n=36, tilt=0.42):
    """Projected edges of a rotating icosahedron, one path per frame."""
    p = (1 + 5 ** 0.5) / 2
    verts = [(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0),
             (0, -1, p), (0, 1, p), (0, -1, -p), (0, 1, -p),
             (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)]
    edges = sorted({tuple(sorted((i, j))) for i in range(12) for j in range(12)
                    if i != j and abs(sum((a - b) ** 2 for a, b in zip(verts[i], verts[j])) - 4) < 1e-6})
    norm = (1 + p * p) ** 0.5
    frames = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        pts = []
        for x, y, z in verts:
            x, y, z = x / norm, y / norm, z / norm
            x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
            y, z = y * math.cos(tilt) - z * math.sin(tilt), y * math.sin(tilt) + z * math.cos(tilt)
            s = 1 / (1.9 - z * 0.45)
            pts.append((cx + x * r * s * 1.9, cy + y * r * s * 1.9))
        frames.append("".join(f"M{pts[i][0]:.1f} {pts[i][1]:.1f}L{pts[j][0]:.1f} {pts[j][1]:.1f}" for i, j in edges))
    return frames


def _check(x, y, color):
    return (f'<path d="M{x} {y - 4.5}l3.6 3.8l7-8" fill="none" stroke="{color}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def build(path):
    s = Svg(W, H, "Angel Peñaranda — Ingeniero de Software · Universidad de los Andes")
    s.defs += [
        f'<radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate(170 40) scale(520 360)">'
        f'<stop stop-color="{C["amber"]}" stop-opacity=".20"/><stop offset="1" stop-color="{C["amber"]}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="glow2" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate(900 420) scale(420 260)">'
        f'<stop stop-color="{C["amber2"]}" stop-opacity=".10"/><stop offset="1" stop-color="{C["amber2"]}" stop-opacity="0"/></radialGradient>',
        '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.1" fill="{C["line2"]}"/></pattern>',
        '<radialGradient id="fade" cx=".35" cy=".35" r=".8"><stop stop-color="#fff" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
        '<mask id="dotmask"><rect width="100%" height="100%" fill="url(#fade)"/></mask>',
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{C["amber"]}" stop-opacity="0"/>'
        f'<stop offset=".35" stop-color="{C["amber"]}" stop-opacity=".7"/><stop offset="1" stop-color="{C["amber"]}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="name" x1="56" y1="0" x2="470" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop stop-color="{C["amber"]}"/><stop offset=".5" stop-color="#FFE7A8"/><stop offset="1" stop-color="{C["amber2"]}"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" values="-140 0;140 0;-140 0" dur="9s" repeatCount="indefinite"/>'
        '</linearGradient>',
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>',
    ]

    s.add('<g clip-path="url(#card)">')
    s.add(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')
    s.add('<rect width="100%" height="100%" fill="url(#dots)" mask="url(#dotmask)"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="url(#glow)"/><rect width="{W}" height="{H}" fill="url(#glow2)"/>')

    frames = _ico_frames(400, 196, 150)
    s.add(f'<path d="{frames[0]}" fill="none" stroke="{C["amber"]}" stroke-opacity=".16" stroke-width="1.2">'
          f'<animate attributeName="d" values="{";".join(frames)}" dur="40s" repeatCount="indefinite"/></path>')
    s.add(f'<rect x="0" y="0" width="{W}" height="1.5" fill="url(#edge)"/>')
    s.add("</g>")
    s.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="{C["line"]}"/>')

    # Left column.
    x = 56
    s.add(f'<rect x="{x}" y="84" width="22" height="2" fill="{C["amber"]}"/>')
    s.text(x + 32, 90, "HOLA, SOY", "mono-m", 14, C["amber"], extra='letter-spacing="2.5"')
    s.text(x - 3, 168, "Angel", "display", 78, C["text"], extra='letter-spacing="-1.5"')
    s.text(x - 3, 244, "Peñaranda", "display", 78, "url(#name)", extra='letter-spacing="-1.5"')
    s.text(x, 290, "Ingeniero de Software", "sans-b", 25, C["text"])
    sub = "Ing. de Sistemas y Computación · Universidad de los Andes"
    size = 16.5
    while width(sub, "sans", size) > 452:
        size -= 0.5
    s.text(x, 318, sub, "sans", size, C["muted"])

    cx = x
    w = s.chip(cx, 340, "último semestre · 2026-20", C["amber"], fill="#1A1608", lead=13)
    s.add(f'<circle cx="{cx + 15}" cy="353" r="3.5" fill="{C["amber"]}">'
          '<animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    cx += w + 8
    cx += s.chip(cx, 340, "coterminal MISO") + 8
    s.chip(cx, 340, "Bogotá, CO")

    # Terminal.
    tx, ty, tw, th = 548, 46, 404, 308
    s.add(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{C["surface"]}" fill-opacity=".92" stroke="{C["line2"]}"/>')
    s.add(f'<path d="M{tx} {ty + 38}h{tw}" stroke="{C["line"]}"/>')
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        s.add(f'<circle cx="{tx + 20 + i * 18}" cy="{ty + 19}" r="5.5" fill="{col}" fill-opacity=".85"/>')
    s.text(tx + tw / 2, ty + 24, "angel@uniandes: ~", "mono", 12.5, C["muted"], anchor="middle")

    lines = [
        ("cmd", "whoami"),
        ("out", "angel · ingeniero de software"),
        ("cmd", "cat foco.txt"),
        ("out", "agentes LLM · testing E2E · web 3D"),
        ("cmd", "npm run test:e2e"),
        ("ok", "91 features · Kraken + Gherkin"),
        ("cmd", "docker compose up agentes"),
        ("ok", "agente ↔ riesgo · A2A + MCP"),
    ]
    fs, lh = 14.5, 27
    lx, ly = tx + 22, ty + 70
    # Every element's resting state is fully visible, so viewers that don't
    # run SMIL still show the whole terminal. The animations, all starting at
    # 0s and lasting the full sequence, hide each line until its turn.
    cw = width("a", "mono", fs)
    t, steps = 0.6, []
    for kind, txt in lines:
        if kind == "cmd":
            dur = 0.055 * (len(txt) + 1)
            steps.append((t, dur))
            t += dur + 0.35
        else:
            steps.append((t, 0))
            t += 0.5
    total = t

    def kt(v):
        return f"{min(v / total, 1):.4f}"

    for i, ((kind, txt), (start, dur)) in enumerate(zip(lines, steps)):
        y = ly + i * lh
        if kind == "cmd":
            s.text(lx, y, "$", "mono-m", fs, C["amber"])
            n = len(txt)
            vals = ["0"] + [f"{k * cw:.1f}" for k in range(n + 1)]
            times = ["0"] + [kt(start + dur * k / (n + 1)) for k in range(n + 1)]
            s.defs.append(f'<clipPath id="ty{i}"><rect x="{lx + 16}" y="{y - 16}" width="{n * cw + 4:.1f}" height="22">'
                          f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(times)}" '
                          f'calcMode="discrete" dur="{total:.2f}s" fill="freeze"/></rect></clipPath>')
            s.add(f'<g clip-path="url(#ty{i})">')
            s.text(lx + 16, y, txt, "mono", fs, C["text"])
            s.add("</g>")
        else:
            s.add(f'<g><animate attributeName="opacity" values="0;1" keyTimes="0;{kt(start)}" calcMode="discrete" '
                  f'dur="{total:.2f}s" fill="freeze"/>')
            if kind == "ok":
                s.add(_check(lx + 1, y, C["green"]))
                s.text(lx + 18, y, txt, "mono", fs, C["soft"])
            else:
                s.text(lx, y, txt, "mono", fs, C["muted"])
            s.add("</g>")
    y = ly + len(lines) * lh
    s.add(f'<g><animate attributeName="opacity" values="0;1" keyTimes="0;.999" calcMode="discrete" dur="{total:.2f}s" fill="freeze"/>')
    s.text(lx, y, "$", "mono-m", fs, C["amber"])
    s.add(f'<rect x="{lx + 16}" y="{y - 13}" width="8.5" height="16" fill="{C["amber"]}">'
          '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')

    s.save(path)
