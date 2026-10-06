"""Project cards, each with a small animated illustration of what it does."""

import math

from svgkit import C, Svg, width, wrap

W, H = 490, 250
RAINBOW = ["#FF4D4D", "#FF9F1C", "#FFE14D", "#4ADE80", "#60A5FA", "#A78BFA"]


def _ill_tests(ox, oy, col):
    out = []
    for i in range(4):
        y = oy + 14 + i * 22
        begin = f"{0.6 + i * 0.45:.2f}s"
        out.append(f'<rect x="{ox + 30}" y="{y - 4}" width="{[62, 48, 56, 40][i]}" height="8" rx="4" fill="{C["line2"]}"/>')
        out.append(f'<circle cx="{ox + 14}" cy="{y}" r="8" fill="none" stroke="{C["line2"]}" stroke-width="1.5"/>')
        out.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" '
                   f'begin="{begin}" dur="5s" repeatCount="indefinite"/>'
                   f'<circle cx="{ox + 14}" cy="{y}" r="8" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.5"/>'
                   f'<path d="M{ox + 10} {y}l3 3l5-6" fill="none" stroke="{col}" stroke-width="1.8" '
                   'stroke-linecap="round" stroke-linejoin="round"/></g>')
    return "".join(out)


def _ill_agents(ox, oy, col):
    a, b, d = (ox + 16, oy + 22), (ox + 84, oy + 22), (ox + 84, oy + 84)
    out = [f'<path d="M{a[0]} {a[1]}H{b[0]}V{d[1]}" fill="none" stroke="{C["line2"]}" stroke-width="1.5" stroke-dasharray="3 4"/>',
           f'<path d="M{a[0]} {a[1]}V{d[1]}" fill="none" stroke="{C["line"]}" stroke-width="1.5" stroke-dasharray="1 5"/>',
           f'<circle r="3.5" fill="{col}"><animateMotion dur="3.2s" repeatCount="indefinite" '
           f'keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear" path="M{a[0]} {a[1]}H{b[0]}V{d[1]}"/></circle>']
    for (x, y), lab in [(a, "A1"), (b, "A2")]:
        out.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{C["raised"]}" stroke="{col}" stroke-width="1.5"/>')
    out.append(f'<rect x="{d[0] - 14}" y="{d[1] - 12}" width="28" height="24" rx="5" fill="{C["raised"]}" stroke="{C["line2"]}" stroke-width="1.5"/>')
    out.append(f'<path d="M{d[0] - 8} {d[1] - 4}h16M{d[0] - 8} {d[1] + 2}h16M{d[0] - 8} {d[1] + 8}h10" stroke="{C["faint"]}" stroke-width="1.5"/>')
    out.append(f'<rect x="{a[0] - 12}" y="{d[1] - 10}" width="24" height="20" rx="4" fill="none" stroke="{C["faint"]}" stroke-width="1.5"/>'
               f'<path d="M{a[0] - 12} {d[1] - 10}l12 9l12-9" fill="none" stroke="{C["faint"]}" stroke-width="1.5"/>')
    return "".join(out)


def _ill_grid(ox, oy, col):
    out, n, c = [], 5, 19
    for i in range(n + 1):
        out.append(f'<path d="M{ox + 3 + i * c} {oy + 3}v{n * c}M{ox + 3} {oy + 3 + i * c}h{n * c}" stroke="{C["line"]}"/>')
    for wx, wy in [(2, 1), (2, 2), (4, 3)]:
        out.append(f'<rect x="{ox + 3 + wx * c + 3}" y="{oy + 3 + wy * c + 3}" width="{c - 6}" height="{c - 6}" rx="2" fill="{C["line2"]}"/>')
    pts = [(0, 0), (1, 0), (1, 1), (1, 3), (3, 3), (3, 4), (4, 4)]
    d = "M" + "L".join(f"{ox + 3 + x * c + c / 2:.1f} {oy + 3 + y * c + c / 2:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="2 4"/>')
    gx, gy = ox + 3 + 4 * c + c / 2, oy + 3 + 4 * c + c / 2
    out.append(f'<path d="M{gx - 5} {gy + 6}v-12l8 4l-8 4" fill="{C["amber"]}" stroke="{C["amber"]}" stroke-linejoin="round"/>')
    out.append(f'<g><animateMotion dur="4.5s" repeatCount="indefinite" path="{d}" rotate="auto"/>'
               f'<circle r="5" fill="{col}"/><path d="M-9 -4l4 2M-9 4l4-2M9 -4l-4 2M9 4l-4-2M-7 0h14" stroke="{col}" stroke-width="1.3"/></g>')
    return "".join(out)


def _ill_prism(ox, oy, col):
    px = [(ox + 50, oy + 16), (ox + 20, oy + 76), (ox + 80, oy + 76)]
    tri = "M" + "L".join(f"{x} {y}" for x, y in px) + "Z"
    hit = (ox + 36, oy + 46)
    out_pt = (ox + 63, oy + 50)
    out = [f'<path d="M{ox - 6} {oy + 58}L{hit[0]} {hit[1]}" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
           f'<path d="M{hit[0]} {hit[1]}L{out_pt[0]} {out_pt[1]}" stroke="#fff" stroke-opacity=".6" stroke-width="1.6"/>']
    for i, c in enumerate(RAINBOW):
        ex, ey = ox + 112, oy + 38 + i * 9
        out.append(f'<path d="M{out_pt[0]} {out_pt[1]}L{ex} {ey}" stroke="{c}" stroke-width="2" stroke-linecap="round">'
                   f'<animate attributeName="stroke-opacity" values=".35;1;.35" dur="2.4s" begin="{i * 0.18:.2f}s" repeatCount="indefinite"/></path>')
    out.append(f'<path d="{tri}" fill="#fff" fill-opacity=".06" stroke="{C["soft"]}" stroke-width="1.6" stroke-linejoin="round"/>')
    return "".join(out)


def _ill_blocks(ox, oy, col):
    blocks = [(0, 52, col), (12, 64, C["violet"]), (12, 44, C["amber"]), (0, 70, col)]
    out = []
    for i, (dx, w, c) in enumerate(blocks):
        y = oy + 8 + i * 22
        out.append(f'<path d="M{ox + dx} {y + 3}a3 3 0 0 1 3-3h7l3 4h8l3-4h{w - 27}a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3h-{w - 3}a3 3 0 0 1-3-3z" '
                   f'fill="{c}" fill-opacity=".16" stroke="{c}" stroke-width="1.4">'
                   f'<animate attributeName="fill-opacity" values=".16;.4;.16" dur="3s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></path>')
        out.append(f'<rect x="{ox + dx + 8}" y="{y + 7}" width="{w * 0.45:.0f}" height="4" rx="2" fill="{c}" fill-opacity=".7"/>')
    out.append(f'<rect x="{ox + 76}" y="{oy + 6}" width="28" height="22" rx="5" fill="none" stroke="{C["soft"]}" stroke-width="1.4"/>'
               f'<circle cx="{ox + 90}" cy="{oy + 17}" r="5.5" fill="none" stroke="{C["soft"]}" stroke-width="1.4"/>'
               f'<rect x="{ox + 81}" y="{oy + 2}" width="9" height="4" rx="1.5" fill="{C["soft"]}"/>')
    return "".join(out)


def _ill_cube(ox, oy, col, n=24):
    v = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    e = [(i, j) for i in range(8) for j in range(i + 1, 8) if sum(a != b for a, b in zip(v[i], v[j])) == 1]
    frames = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        pts = []
        for x, y, z in v:
            x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
            y, z = y * math.cos(0.55) - z * math.sin(0.55), y * math.sin(0.55) + z * math.cos(0.55)
            s = 70 / (3.2 - z * 0.5)
            pts.append((ox + 50 + x * s, oy + 46 + y * s))
        frames.append("".join(f"M{pts[i][0]:.1f} {pts[i][1]:.1f}L{pts[j][0]:.1f} {pts[j][1]:.1f}" for i, j in e))
    floor = f'<path d="M{ox + 8} {oy + 92}L{ox + 50} {oy + 80}L{ox + 92} {oy + 92}L{ox + 50} {oy + 104}Z" fill="none" stroke="{C["line2"]}" stroke-dasharray="2 3"/>'
    return floor + (f'<path d="{frames[0]}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round">'
                    f'<animate attributeName="d" values="{";".join(frames)}" dur="12s" repeatCount="indefinite"/></path>')


ILLUSTRATIONS = {
    "tests": _ill_tests, "agents": _ill_agents, "grid": _ill_grid,
    "prism": _ill_prism, "blocks": _ill_blocks, "cube": _ill_cube,
}


def project(path, kicker, title, desc, chips, color, ill, status, live=False):
    s = Svg(W, H, f"{title} — {desc}")
    s.defs.append(f'<radialGradient id="g" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
                  f'gradientTransform="translate({W - 60} 30) scale(300 220)">'
                  f'<stop stop-color="{color}" stop-opacity=".16"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
                  f'<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    s.add(f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{C["surface"]}"/>'
          f'<rect width="{W}" height="{H}" fill="url(#g)"/>'
          f'<rect width="{W}" height="2" fill="{color}" fill-opacity=".8"/></g>')
    s.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{C["line"]}"/>')
    s.add(f'<g transform="translate({W - 128} 18) scale(.82)">{ILLUSTRATIONS[ill](0, 0, color)}</g>')

    s.add(f'<rect x="28" y="36" width="8" height="8" rx="2" fill="{color}"/>')
    s.text(44, 44.5, kicker.upper(), "mono-m", 12, color, extra='letter-spacing="1.6"')
    s.text(27, 88, title, "display", 32, C["text"], extra='letter-spacing="-.6"')
    for i, line in enumerate(wrap(desc, "sans", 15, W - 56)[:3]):
        s.text(28, 124 + i * 22, line, "sans", 15, "#A9AEBA")

    status_w = width(status, "mono-m", 12.5)
    limit = W - 28 - status_w - 24
    x = 28
    for c in chips:
        cw = width(c, "mono", 12.5) + 20
        if x + cw > limit:
            break
        x += s.chip(x, 198, c, C["soft"], size=12.5) + 7
    s.text(W - 28, 215.5, status, "mono-m", 12.5, C["amber"] if live else C["muted"], anchor="end")
    s.save(path)


def mini(path, kicker, title, desc, color, icon):
    w, h = 320, 168
    s = Svg(w, h, f"{title} — {desc}")
    s.defs.append(f'<clipPath id="c"><rect width="{w}" height="{h}" rx="16"/></clipPath>')
    s.add(f'<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{C["surface"]}"/>'
          f'<rect width="3" height="{h}" fill="{color}"/></g>')
    s.add(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="15.5" fill="none" stroke="{C["line"]}"/>')
    s.add(f'<g transform="translate({w - 52} 22)" fill="none" stroke="{color}" stroke-width="1.6" '
          f'stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
    s.text(24, 38, kicker.upper(), "mono-m", 11.5, color, extra='letter-spacing="1.5"')
    s.text(23, 70, title, "display", 23, C["text"], extra='letter-spacing="-.4"')
    for i, line in enumerate(wrap(desc, "sans", 14.5, w - 46)[:3]):
        s.text(24, 100 + i * 21, line, "sans", 14.5, "#A9AEBA")
    s.save(path)


ICONS = {
    "film": '<rect x="2" y="4" width="26" height="22" rx="3"/><path d="M8 4v22M22 4v22M2 11h6M2 19h6M22 11h6M22 19h6"/>',
    "sat": '<path d="M9 21l-5 5M6 14l10 10M10 10l10 10l4-4l-10-10z"/><path d="M20 4a8 8 0 0 1 6 6M19 9a3 3 0 0 1 2 2"/>',
    "shield": '<path d="M15 3l10 4v8c0 6-4.5 10-10 12C9.5 25 5 21 5 15V7z"/><path d="M11 15l3 3l6-7"/>',
}
