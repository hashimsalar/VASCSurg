#!/usr/bin/env python3
"""Generate the original SVG diagrams drawn for the field guide (written to assets/img/).

Run:  python3 scripts/diagrams.py
The diagrams use the site's color tokens (with light-theme fallbacks), so when the
build inlines them into a page they follow the light and dark themes.
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets" / "img"

STYLE = """<style>
.dg text{font-family:"Atkinson Hyperlegible Next",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:15px;fill:var(--ink-2,#4E5B67)}
.dg .th{fill:var(--ink,#17222D);font-weight:700}
.dg .sm{font-size:13px}
.dg .ink{stroke:var(--ink,#17222D);fill:none}
.dg .inkf{fill:var(--ink,#17222D)}
.dg .rule{stroke:var(--rule-2,#C4CCD4);fill:none}
.dg .sunk{fill:var(--sunk,#E7EBEF)}
.dg .sheet{fill:var(--sheet,#FFFFFF)}
.dg .wall{stroke:var(--artery,#B01E2E);fill:none}
.dg .lumen{fill:var(--artery-tint,#FBEEEF)}
.dg .tube-o{stroke:var(--artery,#B01E2E);fill:none;stroke-linecap:round;stroke-linejoin:round}
.dg .tube-i{stroke:var(--artery-tint,#FBEEEF);fill:none;stroke-linecap:round;stroke-linejoin:round}
.dg .artf{fill:var(--artery,#B01E2E)}
.dg .artl{stroke:var(--artery,#B01E2E);fill:none}
.dg .graft{stroke:var(--pearl,#0B7559);fill:var(--pearl-tint,#E7F4EE)}
.dg .graftl{stroke:var(--pearl,#0B7559);fill:none;stroke-linecap:round;stroke-linejoin:round}
.dg .graftf{fill:var(--pearl,#0B7559)}
.dg .clot{fill:var(--mnem,#8A5A00);fill-opacity:.8}
.dg .vein{stroke:var(--vein,#23539E);fill:none}
.dg .veinf{fill:var(--vein,#23539E)}
.dg .dev{stroke:var(--tip,#583D96);fill:none;stroke-linecap:round;stroke-linejoin:round}
.dg .devf{fill:var(--tip,#583D96)}
.dg .ghost{stroke:var(--rule-2,#C4CCD4);fill:none;stroke-dasharray:6 6;stroke-linecap:round}
</style>"""


def svg(name, w, h, body):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="dg">\n'
           f'{STYLE}\n{body}\n</svg>\n')
    (OUT / name).write_text(doc, encoding="utf-8")


def smooth(pts):
    """Catmull-Rom through points -> cubic Bezier path."""
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def arrow_marker(mid, cls):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="{cls}"/></marker>')


def tube(d, outer=16, inner=10, extra=""):
    return (f'<path d="{d}" class="tube-o" stroke-width="{outer}" {extra}/>'
            f'<path d="{d}" class="tube-i" stroke-width="{inner}" {extra}/>')


# ---------------------------------------------------------------- critical stenosis
def critical_stenosis():
    x0, x1, y0, y1 = 80, 620, 50, 310
    X = lambda p: x0 + (x1 - x0) * p / 100
    Y = lambda f: y1 - (y1 - y0) * f / 100
    rest = [(0, 100), (40, 99.5), (50, 98), (60, 94), (70, 84), (80, 63), (90, 32), (100, 0)]
    ex = [(0, 100), (25, 99.5), (35, 96), (45, 86), (55, 70), (65, 50), (75, 30), (85, 13), (100, 0)]
    b = []
    for f in (0, 25, 50, 75, 100):
        b.append(f'<line x1="{x0}" y1="{Y(f)}" x2="{x1}" y2="{Y(f)}" class="rule" stroke-width="1"/>')
        b.append(f'<text x="{x0-10}" y="{Y(f)+5}" text-anchor="end" class="sm">{f}%</text>')
    for p in (0, 25, 50, 75, 100):
        b.append(f'<text x="{X(p)}" y="{y1+24}" text-anchor="middle" class="sm">{p}%</text>')
    b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" class="ink" stroke-width="1.5"/>')
    b.append(f'<line x1="{x0}" y1="{y0-10}" x2="{x0}" y2="{y1}" class="ink" stroke-width="1.5"/>')
    b.append(f'<rect x="{X(50)}" y="{y0}" width="{X(100)-X(50)}" height="{y1-y0}" class="sunk" opacity=".55"/>')
    b.append(f'<line x1="{X(50)}" y1="{y0-14}" x2="{X(50)}" y2="{y1}" class="ink" stroke-width="1.5" stroke-dasharray="5 5"/>')
    b.append(f'<text x="{X(50)+12}" y="{Y(18)}" class="th sm">Critical stenosis</text>')
    b.append(f'<text x="{X(50)+12}" y="{Y(18)+18}" class="sm">≈ 50% diameter,</text>')
    b.append(f'<text x="{X(50)+12}" y="{Y(18)+36}" class="sm">75% area</text>')
    b.append(f'<path d="{smooth([(X(p), Y(f)) for p, f in rest])}" class="artl" stroke-width="4" fill="none"/>')
    b.append(f'<path d="{smooth([(X(p), Y(f)) for p, f in ex])}" class="artl" stroke-width="3" stroke-dasharray="9 6" fill="none"/>')
    b.append(f'<line x1="{x0+20}" y1="{y1-70}" x2="{x0+56}" y2="{y1-70}" class="artl" stroke-width="4"/>')
    b.append(f'<text x="{x0+64}" y="{y1-65}">At rest</text>')
    b.append(f'<line x1="{x0+20}" y1="{y1-44}" x2="{x0+56}" y2="{y1-44}" class="artl" stroke-width="3" stroke-dasharray="9 6"/>')
    b.append(f'<text x="{x0+64}" y="{y1-39}">High flow (exercise)</text>')
    b.append(f'<text x="{(x0+x1)/2}" y="{y1+50}" text-anchor="middle" class="th">Diameter reduction</text>')
    b.append(f'<text transform="translate(22 {(y0+y1)/2}) rotate(-90)" text-anchor="middle" class="th">Flow beyond the stenosis</text>')
    svg("critical-stenosis.svg", 660, 380, "\n".join(b))


# ---------------------------------------------------------------- endoleaks
def endoleaks():
    W = 184
    b = [f'<defs>{arrow_marker("el-a", "artf")}</defs>']
    labels = [("Type I", "Seal zone leak:", "Ia proximal, Ib distal"),
              ("Type II", "Branch backflow:", "lumbar or IMA"),
              ("Type III", "Junction separation", "or fabric tear"),
              ("Type IV", "Flow through", "porous fabric"),
              ("Type V", "Endotension: sac grows,", "no leak seen")]
    for k in range(5):
        ox = k * W + 6
        g = [f'<g transform="translate({ox} 0)">']
        big = k == 4
        s = 1.12 if big else 1.0
        # sac fill + walls (scaled about center for type V)
        sac = "M70,80 C30,100 30,205 72,232 L90,248 L108,232 C150,205 150,100 110,80 Z"
        lw = "M70,18 L70,80 C30,100 30,205 72,232 L48,300"
        rw = "M110,18 L110,80 C150,100 150,205 108,232 L132,300"
        if big:
            sac = "M70,80 C20,100 20,215 72,234 L90,248 L108,234 C160,215 160,100 110,80 Z"
            lw = "M70,18 L70,80 C20,100 20,215 72,234 L48,300"
            rw = "M110,18 L110,80 C160,100 160,215 108,234 L132,300"
        g.append(f'<path d="M70,18 L110,18 L110,80 L70,80 Z" class="lumen"/>')
        g.append(f'<path d="{sac}" class="sunk"/>')
        g.append(f'<path d="M48,300 L72,232 L90,248 L78,300 Z M132,300 L108,232 L90,248 L102,300 Z" class="lumen"/>')
        g.append(f'<path d="{lw}" class="wall" stroke-width="3"/><path d="{rw}" class="wall" stroke-width="3"/>')
        g.append('<path d="M78,300 L90,250 L102,300" class="wall" stroke-width="3"/>')
        # graft
        g.append('<path d="M77,26 L103,26 L103,186 L121,292 L106,292 L92,206 L88,206 L74,292 L59,292 L77,186 Z" class="graft" stroke-width="2.2" stroke-linejoin="round"/>')
        for y in range(46, 186, 26):
            g.append(f'<line x1="77" y1="{y}" x2="103" y2="{y}" class="graftl" stroke-width="1.6"/>')
        if k == 0:
            g.append('<path d="M74,40 C74,70 70,95 58,118" class="artl" stroke-width="3.5" marker-end="url(#el-a)"/>')
            g.append('<path d="M66,290 C64,262 66,245 70,222" class="artl" stroke-width="3.5" marker-end="url(#el-a)"/>')
            g.append('<text x="40" y="40" class="th sm">Ia</text><text x="36" y="282" class="th sm">Ib</text>')
        elif k == 1:
            g.append('<path d="M141,140 L178,128" class="tube-o" stroke-width="14"/><path d="M139,140 L178,128" class="tube-i" stroke-width="8"/>')
            g.append('<path d="M176,129 C160,134 140,142 118,150" class="artl" stroke-width="3.5" marker-end="url(#el-a)"/>')
        elif k == 2:
            g.append('<path d="M100,192 C118,186 128,166 130,138" class="artl" stroke-width="3.5" marker-end="url(#el-a)"/>')
            g.append('<line x1="96" y1="196" x2="104" y2="188" class="sheet" stroke-width="5"/>')
        elif k == 3:
            for y in range(40, 180, 16):
                g.append(f'<circle cx="69" cy="{y+6}" r="2.6" class="artf"/><circle cx="111" cy="{y}" r="2.6" class="artf"/>')
        else:
            for (x1, y1, x2, y2) in ((36, 150, 14, 150), (144, 150, 166, 150), (50, 214, 34, 230), (130, 214, 146, 230)):
                g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="ink" stroke-width="2.5" marker-end="url(#el-a)"/>')
        t1, t2, t3 = labels[k]
        g.append(f'<text x="90" y="328" text-anchor="middle" class="th">{t1}</text>')
        g.append(f'<text x="90" y="349" text-anchor="middle" class="sm">{t2}</text>')
        g.append(f'<text x="90" y="366" text-anchor="middle" class="sm">{t3}</text>')
        g.append("</g>")
        b.extend(g)
    svg("endoleak-types.svg", 5 * W + 12, 378, "\n".join(b))


# ---------------------------------------------------------------- aortoiliac bypass configurations
def aortoiliac():
    W = 230
    b = []
    titles = [("Aortobifemoral", "Anatomic; best patency,", "but needs a laparotomy"),
              ("Axillobifemoral", "Extra-anatomic; for patients", "too sick for the abdomen"),
              ("Femoral-femoral", "Extra-anatomic; one iliac", "blocked, the other healthy")]
    for k in range(3):
        g = [f'<g transform="translate({k*W} 0)">']
        cx = 115
        aorta_top = 70 if k else 40
        # arteries
        if k == 1:
            g.append(tube(f"M{cx},20 L{cx},140"))
            g.append(tube(f"M{cx-6},34 C80,40 50,48 22,62", 12, 7))
            g.append(f'<text x="18" y="40" class="sm">axillary</text>')
        else:
            g.append(tube(f"M{cx},{aorta_top} L{cx},{176 if k == 2 else 140}"))
        if k == 2:
            g.append(tube(f"M{cx},176 L72,262 L62,350"))
            g.append(f'<path d="M{cx},176 L158,262" class="ghost" stroke-width="4"/>')
            g.append(tube("M158,262 L168,350"))
        else:
            g.append(f'<path d="M{cx},140 L{cx},176 L72,262 M{cx},176 L158,262" class="ghost" stroke-width="4"/>')
            g.append(tube("M72,262 L62,350"))
            g.append(tube("M158,262 L168,350"))
        # grafts
        if k == 0:
            g.append(f'<path d="M{cx},96 L{cx},150 L66,300 M{cx},150 L164,300" class="graftl" stroke-width="7"/>')
        elif k == 1:
            g.append(f'<path d="M30,58 C10,110 8,250 64,300" class="graftl" stroke-width="7"/>')
            g.append(f'<path d="M64,300 C96,326 134,326 164,300" class="graftl" stroke-width="7"/>')
        else:
            g.append(f'<path d="M66,300 C96,262 134,262 164,300" class="graftl" stroke-width="7"/>')
        for x in (66, 164):
            g.append(f'<circle cx="{x}" cy="300" r="5" class="graftf"/>')
        g.append(f'<text x="{cx}" y="384" text-anchor="middle" class="th">{titles[k][0]}</text>')
        g.append(f'<text x="{cx}" y="405" text-anchor="middle" class="sm">{titles[k][1]}</text>')
        g.append(f'<text x="{cx}" y="422" text-anchor="middle" class="sm">{titles[k][2]}</text>')
        g.append("</g>")
        b.extend(g)
    # legend
    ly = 452
    b.append(tube(f"M40,{ly} L80,{ly}", 12, 7))
    b.append(f'<text x="90" y="{ly+5}" class="sm">Patent artery</text>')
    b.append(f'<path d="M220,{ly} L260,{ly}" class="ghost" stroke-width="4"/><text x="270" y="{ly+5}" class="sm">Occluded segment</text>')
    b.append(f'<path d="M430,{ly} L470,{ly}" class="graftl" stroke-width="7"/><text x="480" y="{ly+5}" class="sm">Graft</text>')
    svg("aortoiliac-bypass.svg", 3 * W, 472, "\n".join(b))


# ---------------------------------------------------------------- Fogarty embolectomy
def fogarty():
    b = [f'<defs>{arrow_marker("fg-a", "inkf")}</defs>']
    rows = [("1", "Pass the deflated catheter beyond the clot"),
            ("2", "Inflate the balloon gently, just enough to touch the wall"),
            ("3", "Withdraw steadily: the clot comes out ahead of the balloon")]
    for i, (n, label) in enumerate(rows):
        cy = 82 + i * 128
        top, bot = cy - 24, cy + 24
        g = []
        g.append(f'<rect x="40" y="{top}" width="640" height="48" class="lumen"/>')
        g.append(f'<line x1="40" y1="{top}" x2="96" y2="{top}" class="wall" stroke-width="4"/>')
        g.append(f'<line x1="124" y1="{top}" x2="680" y2="{top}" class="wall" stroke-width="4"/>')
        g.append(f'<line x1="40" y1="{bot}" x2="680" y2="{bot}" class="wall" stroke-width="4"/>')
        if i < 2:
            g.append(f'<path d="M330,{top+2} C360,{top+8} 410,{top+2} 470,{top+6} L470,{bot-4} C420,{bot-1} 370,{bot-6} 330,{bot-2} Z" class="clot"/>')
        if i == 0:
            g.append(f'<path d="M110,{top-40} C110,{top-6} 116,{cy} 160,{cy} L560,{cy}" class="dev" stroke-width="4"/>')
            g.append(f'<ellipse cx="566" cy="{cy}" rx="10" ry="4" class="devf"/>')
        elif i == 1:
            g.append(f'<path d="M110,{top-40} C110,{top-6} 116,{cy} 160,{cy} L516,{cy}" class="dev" stroke-width="4"/>')
            g.append(f'<ellipse cx="536" cy="{cy}" rx="24" ry="21" class="devf" fill-opacity=".85"/>')
        else:
            g.append(f'<path d="M150,{top+4} C185,{top+2} 225,{top+8} 268,{top+4} L268,{bot-4} C230,{bot-2} 190,{bot-6} 150,{bot-4} C138,{cy+8} 138,{cy-8} 150,{top+4} Z" class="clot"/>')
            g.append(f'<path d="M110,{top-40} C110,{top-6} 116,{cy} 160,{cy} L272,{cy}" class="dev" stroke-width="4"/>')
            g.append(f'<ellipse cx="292" cy="{cy}" rx="24" ry="21" class="devf" fill-opacity=".85"/>')
            g.append(f'<line x1="400" y1="{cy}" x2="330" y2="{cy}" class="ink" stroke-width="2.5" marker-end="url(#fg-a)"/>')
        g.append(f'<circle cx="22" cy="{top-26}" r="13" class="inkf"/>')
        g.append(f'<text x="22" y="{top-21}" text-anchor="middle" class="th" style="fill:var(--sheet,#fff)">{n}</text>')
        g.append(f'<text x="148" y="{top-21}">{label}</text>')
        b.extend(g)
    b.append('<text x="110" y="126" text-anchor="middle" class="sm">arteriotomy</text>')
    b.append('<text x="400" y="126" text-anchor="middle" class="sm">clot</text>')
    svg("fogarty-embolectomy.svg", 700, 372, "\n".join(b))


# ---------------------------------------------------------------- CFA landmarks
def cfa():
    b = [f'<defs>{arrow_marker("cf-a", "inkf")}</defs>']
    # bones
    b.append('<circle cx="220" cy="196" r="64" class="sunk"/><circle cx="220" cy="196" r="64" class="ink" stroke-width="2.5" opacity=".7"/>')
    b.append('<path d="M180,244 C160,262 140,280 122,300 L122,446 L182,446 L182,320 C196,300 224,280 246,252 Z" class="sunk"/>')
    b.append('<path d="M180,244 C160,262 140,280 122,300 L122,446 M246,252 C224,280 196,300 182,320 L182,446" class="ink" stroke-width="2.5" opacity=".7"/>')
    b.append('<text x="220" y="201" text-anchor="middle" class="sm">femoral head</text>')
    # inguinal ligament
    b.append('<line x1="56" y1="70" x2="440" y2="168" class="ink" stroke-width="3" stroke-dasharray="10 6"/>')
    b.append('<text x="40" y="58" class="sm">ASIS</text><text x="446" y="182" class="sm">pubic tubercle</text>')
    # arteries
    eia = "M330,24 C318,70 300,104 286,140"
    cfa = "M286,140 C276,180 270,214 266,292"
    sfa = "M266,292 C266,350 272,400 280,446"
    pfa = "M266,292 C250,330 236,380 226,446"
    iea = "M300,104 C330,96 360,70 380,24"
    for d, w, wi in ((eia, 18, 12), (cfa, 18, 12), (sfa, 16, 10), (pfa, 14, 8), (iea, 10, 5)):
        b.append(tube(d, w, wi))
    # target band
    b.append('<path d="M272,176 L264,248" stroke="var(--pearl,#0B7559)" stroke-width="26" stroke-linecap="round" opacity=".35"/>')
    b.append('<path d="M272,176 L264,248" stroke="var(--pearl,#0B7559)" stroke-width="3" stroke-dasharray="4 4"/>')
    # labels
    lab = [
        (318, 22, "end", "external iliac"),
        (388, 30, "start", "inferior epigastric"),
        (330, 120, "start", "Too high: above the ligament,"),
        (330, 138, "start", "bleeding into the retroperitoneum"),
        (312, 206, "start", "Target: common femoral artery"),
        (312, 224, "start", "over the middle of the femoral head"),
        (300, 302, "start", "Too low: at or past the bifurcation,"),
        (300, 320, "start", "pseudoaneurysm or AV fistula"),
        (284, 440, "start", "SFA"),
        (186, 440, "end", "profunda"),
    ]
    for x, y, a, t in lab:
        cls = "th sm" if t.startswith(("Too", "Target")) else "sm"
        b.append(f'<text x="{x}" y="{y}" text-anchor="{a}" class="{cls}">{t}</text>')
    b.append('<circle cx="298" cy="118" r="5" class="inkf"/><line x1="303" y1="118" x2="326" y2="118" class="ink" stroke-width="1.5"/>')
    b.append('<circle cx="268" cy="212" r="5" class="inkf"/><line x1="273" y1="212" x2="308" y2="206" class="ink" stroke-width="1.5"/>')
    b.append('<circle cx="266" cy="294" r="5" class="inkf"/><line x1="271" y1="296" x2="296" y2="300" class="ink" stroke-width="1.5"/>')
    b.append('<text transform="translate(70 92) rotate(14.3)" class="sm">inguinal ligament</text>')
    svg("cfa-landmarks.svg", 600, 456, "\n".join(b))


# ---------------------------------------------------------------- EVAR modular graft
def evar():
    b = []
    sac = "M236,160 C170,190 165,300 238,340 L260,360 L282,340 C355,300 350,190 284,160 Z"
    b.append('<path d="M236,16 L284,16 L284,160 L236,160 Z" class="lumen"/>')
    b.append(f'<path d="{sac}" class="sunk"/>')
    b.append('<path d="M238,340 L260,360 L222,500 L190,500 Z M282,340 L260,360 L298,500 L330,500 Z" class="lumen"/>')
    b.append('<path d="M236,16 L236,160 C170,190 165,300 238,340 L190,500" class="wall" stroke-width="3.5"/>')
    b.append('<path d="M284,16 L284,160 C350,190 355,300 282,340 L330,500" class="wall" stroke-width="3.5"/>')
    b.append('<path d="M222,500 L260,362 L298,500" class="wall" stroke-width="3.5"/>')
    # renals
    b.append('<path d="M236,104 L150,98 L150,118 L236,118 Z M284,104 L370,98 L370,118 L284,118 Z" class="lumen"/>')
    b.append('<path d="M236,104 L150,98 M236,118 L150,118 M284,104 L370,98 M284,118 L370,118" class="wall" stroke-width="3"/>')
    b.append('<rect x="233" y="105" width="54" height="12" class="lumen"/>')
    # graft pieces
    b.append('<path d="M243,124 L277,124 L277,284 L262,284 L262,284 L258,284 L243,284 Z" class="graft" stroke-width="2.4"/>')
    b.append('<path d="M243,282 L258,282 L224,482 L205,482 Z" class="graft" stroke-width="2.4" stroke-linejoin="round"/>')
    b.append('<path d="M262,282 L277,282 L281,306 L265,306 Z" class="graft" stroke-width="2.4" stroke-linejoin="round"/>')
    b.append('<path d="M265,292 L280,292 L318,482 L300,482 Z" class="graft" stroke-width="2.4" stroke-linejoin="round" stroke-dasharray="6 3"/>')
    for y in range(144, 282, 22):
        b.append(f'<line x1="243" y1="{y}" x2="277" y2="{y}" class="graftl" stroke-width="1.8"/>')
    # labels
    L = [
        ((150, 92), "end", None, "renal artery", None),
        ((236, 140), "end", (120, 150), "Infrarenal neck:", "proximal seal"),
        ((243, 200), "end", (120, 220), "Main body", None),
        ((214, 430), "end", (120, 420), "Ipsilateral limb", None),
        ((205, 478), "end", (120, 478), "Iliac seal zones", None),
        ((278, 300), "start", (380, 330), "Contralateral gate", None),
        ((308, 420), "start", (380, 410), "Contralateral limb,", "placed from the other groin"),
        ((330, 230), "start", (380, 236), "Aneurysm sac:", "excluded"),
    ]
    for (px, py), anchor, tp, t1, t2 in L:
        if tp is None:
            b.append(f'<text x="{px}" y="{py}" text-anchor="{anchor}" class="sm">{t1}</text>')
            continue
        tx, ty = tp
        b.append(f'<line x1="{px}" y1="{py}" x2="{tx + (6 if anchor == "end" else -6)}" y2="{ty-5}" class="ink" stroke-width="1.2"/>')
        b.append(f'<circle cx="{px}" cy="{py}" r="3.5" class="inkf"/>')
        b.append(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" class="th sm">{t1}</text>')
        if t2:
            b.append(f'<text x="{tx}" y="{ty+17}" text-anchor="{anchor}" class="sm">{t2}</text>')
    svg("evar-modular-graft.svg", 620, 510, "\n".join(b))


# ---------------------------------------------------------------- aortic zones
def zones():
    b = []
    C = (250, 150)
    R = 74
    P = lambda th, r=R: (C[0] + r * math.cos(math.radians(th)), C[1] - r * math.sin(math.radians(th)))
    asc_x, desc_x = C[0] - R, C[0] + R
    root_y = 300
    bif_y = 600
    # heart
    b.append(f'<ellipse cx="{asc_x-20}" cy="{root_y+40}" rx="70" ry="52" class="sunk"/>')
    b.append(f'<text x="{asc_x-20}" y="{root_y+46}" text-anchor="middle" class="sm">heart</text>')
    main = (f"M{asc_x},{root_y} L{asc_x},{C[1]} A{R},{R} 0 0 1 {desc_x},{C[1]} L{desc_x},{bif_y}")
    # branches (drawn first)
    br = []
    for th, end in ((138, (150, 26)), (101, (226, 22)), (66, (318, 30))):
        x, y = P(th)
        br.append(f"M{x:.1f},{y:.1f} L{end[0]},{end[1]}")
    cel_y, sma_y, ren_y = 430, 462, 504
    br.append(f"M{desc_x},{cel_y} L{desc_x+70},{cel_y-14}")
    br.append(f"M{desc_x},{sma_y} L{desc_x+70},{sma_y+10}")
    br.append(f"M{desc_x},{ren_y} L{desc_x+64},{ren_y} M{desc_x},{ren_y} L{desc_x-64},{ren_y}")
    il = (desc_x - 56, 680)
    ir = (desc_x + 56, 680)
    br.append(f"M{il[0]},{il[1]} L{il[0]+22},{il[1]+60} M{ir[0]},{ir[1]} L{ir[0]-22},{ir[1]+60}")
    for d in br:
        b.append(tube(d, 14, 8))
    iliac = f"M{desc_x},{bif_y} L{il[0]},{il[1]} L{il[0]-24},{il[1]+90} M{desc_x},{bif_y} L{ir[0]},{ir[1]} L{ir[0]+24},{ir[1]+90}"
    b.append(tube(iliac, 22, 15))
    b.append(tube(main, 34, 26))
    # zone boundaries
    def tick_arch(th):
        a, c = P(th, R - 22), P(th, R + 22)
        return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{c[0]:.1f}" y2="{c[1]:.1f}" class="ink" stroke-width="2.5"/>'
    def tick_h(y, x=desc_x, half=22):
        return f'<line x1="{x-half}" y1="{y}" x2="{x+half}" y2="{y}" class="ink" stroke-width="2.5"/>'
    b.append(f'<line x1="{asc_x-22}" y1="{root_y-6}" x2="{asc_x+22}" y2="{root_y-6}" class="ink" stroke-width="2.5"/>')
    for th in (128, 92, 57):
        b.append(tick_arch(th))
    z3_end, z4_end = 200, 330
    for y in (z3_end, z4_end, cel_y, sma_y, ren_y - 12, ren_y + 12, bif_y):
        b.append(tick_h(y))
    # iliac bifurcations
    for (x, y) in (il, ir):
        b.append(f'<circle cx="{x}" cy="{y}" r="4" class="inkf"/>')
    # zone badges
    def badge(x, y, n):
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" class="inkf"/>'
                f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" class="th sm" style="fill:var(--sheet,#fff)">{n}</text>')
    b.append(badge(asc_x - 42, 220, 0))
    for th, n, r in ((119, 1, R + 40), (84, 2, R + 42), (34, 3, R + 36)):
        x, y = P(th, r)
        b.append(badge(x, y, n))
    side = desc_x + 44
    for y, n in (((z3_end + z4_end) / 2, 4), ((z4_end + cel_y) / 2, 5), ((cel_y + sma_y) / 2, 6),
                 ((sma_y + ren_y - 12) / 2, 7), (ren_y, 8), ((ren_y + 12 + bif_y) / 2, 9)):
        b.append(badge(desc_x - 44 if n in (6, 7, 8) else side, y, n))
    b.append(badge(desc_x - 54, 640, 10))
    b.append(badge(il[0] - 46, 728, 11))
    # labels
    T = [
        (138, 22, "end", "innominate"), (226, 14, "middle", "left common carotid"), (330, 30, "start", "left subclavian"),
        (desc_x + 80, cel_y - 16, "start", "celiac"), (desc_x + 80, sma_y + 20, "start", "SMA"),
        (desc_x + 74, ren_y + 5, "start", "renal"),
        (ir[0] + 34, ir[1] + 84, "start", "external iliac"), (ir[0] - 10, ir[1] + 78, "end", "internal iliac"),
    ]
    for x, y, a, t in T:
        b.append(f'<text x="{x}" y="{y}" text-anchor="{a}" class="sm">{t}</text>')
    # key
    kx, ky = 420, 120
    key = [("0", "Ascending aorta to the innominate"), ("1", "Innominate to left carotid"),
           ("2", "Left carotid to left subclavian"), ("3", "First 2 cm past the subclavian"),
           ("4", "To the mid-descending (T6)"), ("5", "To the celiac"), ("6", "Celiac to SMA"),
           ("7", "SMA to renals"), ("8", "Renal segment"), ("9", "Infrarenal aorta"),
           ("10", "Common iliacs"), ("11", "External iliacs")]
    b.append(f'<text x="{kx}" y="{ky-28}" class="th">Zones</text>')
    for i, (n, t) in enumerate(key):
        y = ky + i * 22
        b.append(f'<text x="{kx+16}" y="{y}" text-anchor="end" class="th sm">{n}</text>')
        b.append(f'<text x="{kx+26}" y="{y}" class="sm">{t}</text>')
    b.append(f'<path d="M{kx-10},{ky-14} L{kx-16},{ky-14} L{kx-16},{ky+4*22+4} L{kx-10},{ky+4*22+4}" class="ink" stroke-width="1.5"/>')
    b.append(f'<text transform="translate({kx-24} {ky+44}) rotate(-90)" text-anchor="middle" class="sm">Ishimaru</text>')
    svg("aortic-zones.svg", 680, 790, "\n".join(b))


# ---------------------------------------------------------------- French scale
def french():
    s = 11.0  # px per mm
    sizes = [4, 5, 6, 7, 8, 10, 12, 14, 18, 20, 24]
    b = []
    x = 84
    cy = 110
    b.append(f'<text x="30" y="{cy+66}" class="sm">size</text><text x="30" y="{cy+84}" class="sm">mm</text>')
    b.append('<text x="30" y="30" class="th">Catheters and sheaths, drawn to scale (French)</text>')
    for f in sizes:
        d = f / 3 * s
        cx = x + d / 2
        b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{d/2:.1f}" class="lumen"/>'
                 f'<circle cx="{cx:.1f}" cy="{cy}" r="{d/2:.1f}" class="wall" stroke-width="2"/>')
        b.append(f'<text x="{cx:.1f}" y="{cy+66}" text-anchor="middle" class="th sm">{f}F</text>')
        b.append(f'<text x="{cx:.1f}" y="{cy+84}" text-anchor="middle" class="sm">{f/3:.1f}</text>')
        x += d + 24
    wy = 280
    b.append(f'<text x="30" y="{wy-34}" class="th">Guidewires, same scale (inches)</text>')
    x = 40
    for inch in (0.014, 0.018, 0.035, 0.038):
        mm = inch * 25.4
        r = mm * s / 2
        b.append(f'<circle cx="{x}" cy="{wy}" r="{r:.2f}" class="devf"/>')
        b.append(f'<text x="{x+18}" y="{wy+5}" class="sm"><tspan class="th">{inch:.3f}"</tspan> = {mm:.2f} mm ≈ {mm*3:.1f}F</text>')
        x += 186
    b.append(f'<text x="30" y="{wy+50}" class="sm">French ÷ 3 = millimeters. A sheath is sized by the catheter it accepts (inner diameter);</text>')
    b.append(f'<text x="30" y="{wy+70}" class="sm">its outer diameter, which is the hole in the artery, is larger. A catheter is sized by its outer diameter.</text>')
    svg("french-scale.svg", 820, 360, "\n".join(b))


# ---------------------------------------------------------------- guidewire anatomy
def guidewire():
    b = []
    y = 90
    b.append(f'<rect x="40" y="{y-9}" width="440" height="18" rx="9" class="sunk"/>')
    b.append(f'<line x1="40" y1="{y}" x2="430" y2="{y}" class="ink" stroke-width="8" stroke-linecap="round"/>')
    b.append(f'<path d="M430,{y-4} L560,{y-1} L640,{y-0.6} L640,{y+0.6} L560,{y+1} L430,{y+4} Z" class="inkf"/>')
    b.append(f'<rect x="480" y="{y-9}" width="200" height="18" rx="9" class="lumen"/>')
    for i in range(0, 200, 7):
        b.append(f'<line x1="{482+i}" y1="{y-8}" x2="{486+i}" y2="{y+8}" class="wall" stroke-width="1.6"/>')
    b.append(f'<line x1="480" y1="{y}" x2="676" y2="{y}" class="ink" stroke-width="1.4"/>')
    b.append(f'<circle cx="680" cy="{y}" r="9" class="artf"/>')
    for x1, x2, t in ((40, 430, "Stiff body: support and pushability"), (430, 560, "Taper"), (560, 690, "Floppy tip")):
        b.append(f'<path d="M{x1},{y-26} L{x1},{y-32} L{x2},{y-32} L{x2},{y-26}" class="ink" stroke-width="1.4"/>')
        b.append(f'<text x="{(x1+x2)/2}" y="{y-40}" text-anchor="middle" class="th sm">{t}</text>')
    b.append(f'<line x1="300" y1="{y+4}" x2="300" y2="{y+40}" class="ink" stroke-width="1.2"/><text x="300" y="{y+56}" text-anchor="middle" class="sm">steel or nitinol core</text>')
    b.append(f'<line x1="590" y1="{y+9}" x2="590" y2="{y+40}" class="ink" stroke-width="1.2"/><text x="590" y="{y+56}" text-anchor="middle" class="sm">coil or hydrophilic jacket</text>')
    ty = 250
    b.append(f'<text x="40" y="{ty-46}" class="th">Tip shapes</text>')
    shapes = [("Straight", f"M60,{ty} L200,{ty}"),
              ("Angled", f"M290,{ty} L400,{ty} L436,{ty-22}"),
              ("J", f"M530,{ty} L640,{ty} C676,{ty} 680,{ty-40} 650,{ty-40} C634,{ty-40} 628,{ty-28} 636,{ty-20}")]
    for name, d in shapes:
        b.append(f'<path d="{d}" class="dev" stroke-width="6"/>')
    for x, name in ((130, "Straight"), (362, "Angled: steerable"), (600, "J: atraumatic")):
        b.append(f'<text x="{x}" y="{ty+30}" text-anchor="middle" class="sm">{name}</text>')
    svg("guidewire-anatomy.svg", 720, 300, "\n".join(b))


# ---------------------------------------------------------------- catheter shapes
def catheters():
    col = 118
    b = []
    shapes = [
        ("Pigtail", "flush", "M0,250 L0,96 C0,52 52,44 52,80 C52,110 18,112 16,88 C15,74 28,68 36,76"),
        ("Omni Flush", "flush, reverse curve", "M0,250 L0,110 C0,60 56,52 60,96 C62,120 44,132 34,118"),
        ("Berenstein", "short angle", "M0,250 L0,96 L22,64"),
        ("Vertebral", "slight angle", "M0,250 L0,104 C0,90 4,84 14,72 L34,52"),
        ("Cobra", "double curve, downgoing", "M0,250 L0,140 C0,100 30,82 54,100 L70,124"),
        ("Simmons", "reverse curve, formed in aorta", "M0,250 L0,96 C0,30 74,30 74,96 L74,170"),
        ("SOS Omni", "small reverse, curve", "M0,250 L0,118 C0,72 54,70 56,102 C57,120 46,128 40,118"),
    ]
    for i, (name, sub, d) in enumerate(shapes):
        x = 34 + i * col
        b.append(f'<g transform="translate({x} 20)"><path d="{d}" class="dev" stroke-width="6"/></g>')
        if name in ("Pigtail", "Omni Flush"):
            pass
        b.append(f'<text x="{x+26}" y="300" text-anchor="middle" class="th sm">{name}</text>')
        words = sub.split(", ")
        for j, w in enumerate(words):
            b.append(f'<text x="{x+26}" y="{318+j*17}" text-anchor="middle" class="sm">{w}</text>')
    for x, y in ((34, 110), (34, 128), (34, 146)):
        b.append(f'<circle cx="{x}" cy="{y}" r="2.2" class="sheet"/>')
    svg("catheter-shapes.svg", 7 * col + 20, 356, "\n".join(b))


# ---------------------------------------------------------------- re-entry
def reentry():
    b = [f'<defs>{arrow_marker("re-a", "devf")}</defs>']
    b.append('<rect x="20" y="60" width="680" height="96" class="lumen"/>')
    b.append('<rect x="20" y="156" width="680" height="34" class="sunk"/>')
    b.append('<line x1="20" y1="52" x2="700" y2="52" class="wall" stroke-width="6"/>')
    b.append('<line x1="20" y1="156" x2="700" y2="156" class="wall" stroke-width="2.5"/>')
    b.append('<line x1="20" y1="194" x2="700" y2="194" class="wall" stroke-width="6"/>')
    b.append('<path d="M240,58 C300,64 400,56 470,60 L470,154 C400,150 300,156 240,152 C226,120 226,90 240,58 Z" class="clot"/>')
    for x in range(256, 470, 18):
        b.append(f'<line x1="{x}" y1="64" x2="{x+30}" y2="150" class="sheet" stroke-width="1.2" opacity=".5"/>')
    # wire: lumen -> subintimal loop -> along
    b.append('<path d="M20,108 L170,108 C200,108 205,170 230,172 L470,172" class="dev" stroke-width="4"/>')
    # knuckle loop leading edge
    # re-entry catheter + needle
    b.append('<path d="M330,173 L540,173" class="ink" stroke-width="9" stroke-linecap="round" opacity=".55"/>')
    b.append('<path d="M540,172 C556,170 566,150 568,112" class="dev" stroke-width="3" marker-end="url(#re-a)"/>')
    b.append('<path d="M568,108 L690,108" class="dev" stroke-width="4" stroke-dasharray="2 7"/>')
    lab = [
        (110, 92, "middle", "true lumen", ""),
        (355, 40, "middle", "occlusion", "th"),
        (300, 222, "middle", "wire tracks through the subintimal space", ""),
        (600, 92, "middle", "back into the true lumen", "th"),
        (630, 222, "middle", "re-entry needle", ""),
    ]
    for x, y, a, t, c in lab:
        b.append(f'<text x="{x}" y="{y}" text-anchor="{a}" class="sm {c}">{t}</text>')
    svg("reentry.svg", 720, 236, "\n".join(b))


for fn in (critical_stenosis, endoleaks, aortoiliac, fogarty, cfa, evar, zones, french, guidewire, catheters, reentry):
    fn()
print("ok")
