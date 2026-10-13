#!/usr/bin/env python3
"""
Vascular Surgery Field Guide: stamp shared chrome into every page.

Each page is plain static HTML. Shared pieces live between marker comments
and are regenerated here, so one edit to the page list updates every page:

  <!-- @head --> ... <!-- /@head -->       meta, fonts, stylesheet, theme boot
  <!-- @nav --> ... <!-- /@nav -->         top bar + scrim
  <!-- @rail --> ... <!-- /@rail -->       chapter list (current page marked)
  <!-- @crumb --> ... <!-- /@crumb -->     "Field Guide / group" line
  <!-- @toc --> ... <!-- /@toc -->         collapsible "On this page" (small screens)
  <!-- @aside --> ... <!-- /@aside -->     "On this page" column (wide screens)
  <!-- @pager --> ... <!-- /@pager -->     previous / next chapter
  <!-- @footer --> ... <!-- /@footer -->   footer, back-to-top, script

It also writes assets/search-index.js from every <section class="sec">.

Run from anywhere:  python3 scripts/build.py            (all pages)
                    python3 scripts/build.py a.html   (stamp only the named pages)
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "Vascular Surgery Field Guide"
REVIEWED = "October 2026"

GROUPS = [
    ("Start here", [
        ("index.html", "Home", "Where to start for your role, the vascular mindset, and how the guide is organized."),
        ("first-day.html", "Your first day", "Badge, scrubs, PowerChart, parking, the team, and what to carry."),
        ("rounds.html", "Rounds and presenting", "Pre-rounding, the numbers a vascular team wants, presenting, and the operating room."),
    ]),
    ("Running the service", [
        ("charting.html", "History, exam and charting", "The vascular history by complaint, the focused exam, and copy-ready notes for PowerChart."),
        ("ctv-icu.html", "The CTV ICU", "Who goes to the cardiothoracic and vascular ICU, how they get there, and what to watch after each operation."),
        ("on-call.html", "On call and cross-cover", "Pager triage and the overnight calls that come up again and again, with first moves for each."),
    ]),
    ("The knowledge", [
        ("foundations.html", "Foundations", "Anatomy, hemodynamics, the exam, noninvasive testing, imaging, and anticoagulation."),
        ("presentations.html", "Presentations", "PAD, CLTI, acute limb ischemia, aneurysm, carotid, dissection, mesenteric, and venous disease."),
        ("operations.html", "Open operations", "Carotid endarterectomy, open aneurysm repair, bypass, access, amputation, and fasciotomy."),
        ("endovascular.html", "Endovascular", "Access, angiography, radiation and contrast, stenting, EVAR and TEVAR, and clot management."),
        ("devices.html", "Wires, catheters and devices", "Needles, sheaths, wires, catheters, balloons, stents, grafts and closure devices, by name."),
    ]),
    ("Sharpen up", [
        ("questions.html", "Questions you'll be asked", "The classic teaching questions, with the answer an attending wants to hear."),
        ("reference.html", "Quick reference", "Every table, classification, and number worth memorizing, on one page."),
    ]),
]

PAGES = []
for group, items in GROUPS:
    for f, title, desc in items:
        PAGES.append({"file": f, "title": title, "desc": desc, "group": group})
for i, p in enumerate(PAGES):
    p["n"] = i

BRAND_MARK = (
    '<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">'
    '<rect width="32" height="32" rx="8" fill="#B01E2E"/>'
    '<path d="M16 5v9.5c0 2.2-1.2 3.6-3 5L8.5 23.5V27M16 14.5c0 2.2 1.2 3.6 3 5l4.5 4V27" '
    'fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

ICON = {
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
}

FONTS = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,600;0,700;1,400"
         "&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap")


def ver(rel):
    """Short content hash so browsers refetch an asset only when it changes."""
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def esc(s):
    return html.escape(s, quote=True)


def head(page):
    title = SITE if page["file"] == "index.html" else f'{page["title"]} | {SITE}'
    return "\n".join([
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(page["desc"])}">',
        '<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">',
        '<meta name="theme-color" content="#111A22" media="(prefers-color-scheme: dark)">',
        '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="stylesheet" href="{FONTS}">',
        f'<link rel="stylesheet" href="assets/styles.css?v={ver("assets/styles.css")}">',
        "<script>(function(){var r=document.documentElement;r.classList.add('js');"
        "try{var t=localStorage.getItem('vfg-theme');if(t==='dark'||t==='light')r.setAttribute('data-theme',t);}catch(e){}})();</script>",
    ])


def nav(page):
    return "\n".join([
        '<a class="skip" href="#main">Skip to content</a>',
        '<header class="topbar">',
        f'  <button class="icon-btn menu-btn" type="button" data-nav-open aria-controls="rail" aria-expanded="false" aria-label="Open contents">{ICON["menu"]}</button>',
        f'  <a class="brand" href="index.html">{BRAND_MARK}<span class="brand-name">Vascular Surgery <span>Field Guide</span></span></a>',
        '  <div class="topbar-actions">',
        f'    <button class="icon-btn search-btn" type="button" data-search-open aria-label="Search the guide">{ICON["search"]}<span class="lbl">Search the guide</span><kbd>/</kbd></button>',
        f'    <button class="icon-btn theme-btn" type="button" data-theme-toggle aria-label="Switch color theme">{ICON["sun"]}{ICON["moon"]}</button>',
        "  </div>",
        "</header>",
        '<div class="scrim" data-nav-close></div>',
    ])


def rail(page):
    out = ['<nav class="rail" id="rail" aria-label="Guide contents">',
           f'  <div class="rail-close"><button class="icon-btn" type="button" data-nav-close aria-label="Close contents">{ICON["close"]}</button></div>']
    for group, items in GROUPS:
        out.append(f'  <div class="rail-group">\n    <p class="rail-label">{esc(group)}</p>\n    <ol>')
        for f, title, _ in items:
            p = next(x for x in PAGES if x["file"] == f)
            cur = ' aria-current="page"' if f == page["file"] else ""
            out.append(f'      <li><a class="rail-link" href="{f}"{cur}><span class="rail-n">{p["n"]}</span>{esc(title)}</a></li>')
        out.append("    </ol>\n  </div>")
    out.append('  <p class="rail-note">Inflow, outflow, conduit. The vascular patient is always a cardiac patient.</p>')
    out.append("</nav>")
    return "\n".join(out)


def crumb(page):
    if page["file"] == "index.html":
        return ""
    return f'<p class="crumb"><a href="index.html">Field Guide</a><span class="sep" aria-hidden="true">/</span>{esc(page["group"])}</p>'


SEC_RE = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S)
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def sections(src):
    out = []
    for m in SEC_RE.finditer(src):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        if "sec" not in attrs.get("class", "").split():
            continue
        if not attrs.get("id") or not attrs.get("data-title"):
            continue
        out.append({"id": attrs["id"], "title": html.unescape(attrs["data-title"]),
                    "bed": attrs.get("data-bed", ""), "body": m.group(2)})
    return out


def toc(page, secs):
    if len(secs) < 3:
        return ""
    items = "\n".join(f'    <li><a href="#{s["id"]}">{esc(s["title"])}</a></li>' for s in secs)
    return (f'<details class="toc-inline">\n  <summary>On this page <span class="count">{len(secs)} sections</span></summary>\n'
            f"  <ol>\n{items}\n  </ol>\n</details>")


def aside(page, secs):
    if len(secs) < 3:
        return ""
    items = "\n".join(
        f'    <li><a href="#{s["id"]}"{(" data-bed=" + chr(34) + s["bed"] + chr(34)) if s["bed"] else ""}>{esc(s["title"])}</a></li>'
        for s in secs)
    return f'<aside class="aside" aria-label="On this page">\n  <p class="aside-label">On this page</p>\n  <ol>\n{items}\n  </ol>\n</aside>'


def pager(page):
    i = page["n"]
    prev = PAGES[i - 1] if i > 0 else None
    nxt = PAGES[i + 1] if i + 1 < len(PAGES) else None
    out = ['<nav class="pager" aria-label="Chapters">']
    if prev:
        out.append(f'  <a class="prev" href="{prev["file"]}" rel="prev"><span class="dir">Previous</span><span class="ttl">{esc(prev["title"])}</span></a>')
    if nxt:
        out.append(f'  <a class="next" href="{nxt["file"]}" rel="next"><span class="dir">Next</span><span class="ttl">{esc(nxt["title"])}</span></a>')
    out.append("</nav>")
    return "\n".join(out)


def footer(page):
    return "\n".join([
        '<footer class="site-foot">',
        '  <div class="inner">',
        "    <div>",
        "      <p><b>An orientation and study aid, not a clinical protocol.</b> Thresholds, classifications and trial data change, "
        "and practice varies between hospitals. Check specifics against current SVS and ESVS guidance, your attendings, "
        "and local pathways before applying anything to a patient.</p>",
        "    </div>",
        "    <div>",
        "      <p>Compiled by <b>Hashim Salar</b>.</p>",
        f"      <p>Content last reviewed {REVIEWED}.</p>",
        "    </div>",
        "  </div>",
        "</footer>",
        f'<button class="to-top" type="button" aria-label="Back to top">{ICON["up"]}</button>',
        f'<script src="assets/app.js?v={ver("assets/app.js")}" data-index="{INDEX_VER}" defer></script>',
    ])


def stamp(src, name, content):
    pat = re.compile(r"(<!-- @%s -->)(.*?)(<!-- /@%s -->)" % (name, name), re.S)
    if not pat.search(src):
        return src, False
    body = ("\n" + content + "\n") if content else ""
    return pat.sub(lambda m: m.group(1) + body + m.group(3), src, count=1), True


TAG_RE = re.compile(r"<[^>]+>")


def text_of(fragment):
    fragment = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<(br|/p|/li|/h\d|/dt|/dd|/td|/th|/summary)\b[^>]*>", " ", fragment)
    t = html.unescape(TAG_RE.sub(" ", fragment))
    return re.sub(r"\s+", " ", t).strip()


INDEX_VER = ""


def build_index():
    index = []
    for page in PAGES:
        path = ROOT / page["file"]
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8")
        summary = re.search(r'<p class="summary">(.*?)</p>', src, re.S)
        index.append({"p": page["title"], "t": page["title"], "u": page["file"],
                      "x": text_of(summary.group(1)) if summary else page["desc"]})
        for s in sections(src):
            index.append({"p": page["title"], "t": s["title"], "u": f'{page["file"]}#{s["id"]}',
                          "x": text_of(s["body"])[:6000]})
    return index


def main():
    global INDEX_VER
    only = set(a for a in sys.argv[1:] if a.endswith(".html"))
    index = build_index()
    js = "window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (ROOT / "assets" / "search-index.js").write_text(js, encoding="utf-8")
    INDEX_VER = hashlib.sha1(js.encode("utf-8")).hexdigest()[:8]
    missing = []
    for page in PAGES:
        path = ROOT / page["file"]
        if not path.exists():
            missing.append(page["file"])
            continue
        src = path.read_text(encoding="utf-8")
        secs = sections(src)
        for name, fn in [("head", head), ("nav", nav), ("rail", rail), ("crumb", crumb),
                         ("pager", pager), ("footer", footer)]:
            src, _ = stamp(src, name, fn(page))
        src, _ = stamp(src, "toc", toc(page, secs))
        src, _ = stamp(src, "aside", aside(page, secs))
        if not only or page["file"] in only:
            path.write_text(src, encoding="utf-8")

    print(f"Stamped {len(PAGES) - len(missing)} pages, indexed {len(index)} sections.")
    if missing:
        print("Missing pages (skipped):", ", ".join(missing), file=sys.stderr)


if __name__ == "__main__":
    main()
