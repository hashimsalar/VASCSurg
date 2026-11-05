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

  <!-- @fig ID --> ... <!-- /@fig -->   a figure from scripts/images.json
  <!-- @credits --> ... <!-- /@credits --> the image credits list (credits.html)

Figure markers are inserted automatically where scripts/images.json says a
figure belongs (a section, optionally under a named <h3>). Once a marker exists
you can move it anywhere in the page and the build will keep it there.
Images are downloaded by scripts/fetch_images.py.

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
    ("About", [
        ("credits.html", "Image credits", "Sources, authors and licenses for every image and diagram in the guide."),
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
        '      <p>Images are credited on the <a href="credits.html">image credits</a> page.</p>',
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


# ---------------------------------------------------------------- figures

FIG_MANIFEST = ROOT / "scripts" / "images.json"
FIG_CREDITS = ROOT / "scripts" / "image-credits.json"
FIG_RE = re.compile(r"\n?[ \t]*<!-- @fig ([\w-]+) -->.*?<!-- /@fig \1 -->", re.S)


def load_figures():
    if not FIG_MANIFEST.exists():
        return [], {}
    figs = json.loads(FIG_MANIFEST.read_text(encoding="utf-8"))
    credits = json.loads(FIG_CREDITS.read_text(encoding="utf-8")) if FIG_CREDITS.exists() else {}
    return figs, credits


def short_author(fig, cr):
    """A readable author name for a caption; full details live on the credits page."""
    name = fig.get("author") or cr.get("author") or "Unknown author"
    if len(name) > 70:
        name = re.split(r"(?<=[a-z0-9])\. |; | \(", name)[0]
    return name.strip(" .")


def first_sentence(text):
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def inline_svg(path, label):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<\?xml[^>]*\?>\s*", "", raw).strip()
    return raw.replace("<svg ", f'<svg role="img" aria-label="{esc(label)}" focusable="false" ', 1)


def figure_html(fig, cr):
    fid = fig["id"]
    if cr.get("original"):
        media = (f'<div class="fig-media fig-diagram">{inline_svg(ROOT / cr["file"], fig["alt"])}</div>')
        credit = ('<span class="fig-credit">Diagram drawn for this guide. Based on '
                  f'{esc(fig.get("basis", ""))} <a href="credits.html#credit-{fid}">Credits</a></span>')
    else:
        media = (f'<a class="fig-media" href="{cr["file"]}" aria-label="Open the full image">'
                 f'<img src="{cr["file"]}" width="{cr["width"]}" height="{cr["height"]}" alt="{esc(fig["alt"])}" '
                 'loading="lazy" decoding="async"></a>')
        lic = esc(cr["license"])
        if cr.get("license_url"):
            lic = f'<a href="{esc(cr["license_url"])}" rel="license">{lic}</a>'
        credit = (f'<span class="fig-credit">Image: {esc(short_author(fig, cr))}, {lic}, '
                  f'via <a href="{esc(cr["source"])}">Wikimedia Commons</a>.</span>')
    return (f'<figure class="fig" id="fig-{fid}">\n  {media}\n'
            f'  <figcaption>{esc(fig["caption"])} {credit}</figcaption>\n</figure>')


def _section_bounds(src, sec_id):
    m = re.search(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(sec_id), src)
    if not m:
        return None
    end = src.find("</section>", m.end())
    return m.end(), end


def _anchor(src, fig):
    """Where a new figure marker goes: after the first paragraph under the named <h3>,
    or after the section lede."""
    bounds = _section_bounds(src, fig["section"])
    if not bounds:
        return None
    start, end = bounds
    body = src[start:end]
    pos = None
    if fig.get("h3"):
        for h in re.finditer(r"<h3\b[^>]*>(.*?)</h3>", body, re.S):
            if text_of(h.group(1)).startswith(fig["h3"]):
                pos = h.end()
                nxt = re.match(r"\s*<p\b[^>]*>.*?</p>", body[pos:], re.S)
                if nxt:
                    pos += nxt.end()
                break
        if pos is None:
            print(f'  figure {fig["id"]}: no <h3> "{fig["h3"]}" in #{fig["section"]}; placed after the lede', file=sys.stderr)
    if pos is None:
        lede = re.search(r'<p class="sec-lede">.*?</p>', body, re.S) or re.search(r"</h2>", body)
        pos = lede.end() if lede else 0
    # keep figures that share an anchor in manifest order
    while True:
        m = re.match(r"\s*<!-- @fig ([\w-]+) -->.*?<!-- /@fig \1 -->", body[pos:], re.S)
        if not m:
            break
        pos += m.end()
    return start + pos


def stamp_figures(src, page, figs, credits):
    mine = [f for f in figs if f["page"] == page["file"]]
    wanted = {f["id"] for f in mine}
    # drop markers whose figure is gone from the manifest
    src = FIG_RE.sub(lambda m: m.group(0) if m.group(1) in wanted else "", src)
    for fig in mine:
        if f'<!-- @fig {fig["id"]} -->' not in src:
            at = _anchor(src, fig)
            if at is None:
                print(f'  figure {fig["id"]}: no section #{fig["section"]} in {page["file"]}', file=sys.stderr)
                continue
            src = src[:at] + f'\n    <!-- @fig {fig["id"]} --><!-- /@fig {fig["id"]} -->' + src[at:]
        cr = credits.get(fig["id"])
        content = figure_html(fig, cr) if cr and (ROOT / cr["file"]).exists() else ""
        pat = re.compile(r"(<!-- @fig %s -->)(.*?)(<!-- /@fig %s -->)" % (re.escape(fig["id"]), re.escape(fig["id"])), re.S)
        body = ("\n" + content + "\n") if content else ""
        src = pat.sub(lambda m: m.group(1) + body + m.group(3), src, count=1)
    return src


def credits_html(figs, credits):
    out = []
    titles = {}
    for page in PAGES:
        path = ROOT / page["file"]
        if path.exists():
            titles[page["file"]] = {s["id"]: s["title"] for s in sections(path.read_text(encoding="utf-8"))}
    for page in PAGES:
        mine = [f for f in figs if f["page"] == page["file"] and f["id"] in credits]
        if not mine:
            continue
        out.append(f'<h3>{esc(page["title"])}</h3>\n<ol class="img-credits">')
        for fig in mine:
            cr = credits[fig["id"]]
            where = f'{page["file"]}#fig-{fig["id"]}'
            sec = titles.get(page["file"], {}).get(fig["section"], fig["section"])
            thumb = (f'<a class="img-credit-thumb" href="{where}" tabindex="-1" aria-hidden="true">'
                     f'<img src="{cr["file"]}" alt="" width="{cr["width"]}" height="{cr["height"]}" loading="lazy" decoding="async"></a>')
            lines = [f'<p class="img-credit-title"><a href="{where}">{esc(first_sentence(fig["caption"]))}</a></p>',
                     f'<p class="img-credit-where">{esc(page["title"])} / {esc(sec)}</p>']
            if cr.get("original"):
                lines.append("<p>Original diagram drawn for this guide. Schematic, not to scale where noted.</p>")
                if fig.get("basis"):
                    lines.append(f'<p><b>Based on:</b> {esc(fig["basis"])}</p>')
                lines.append(f'<p><a href="{cr["file"]}">SVG file</a></p>')
            else:
                lic = esc(cr["license"])
                if cr.get("license_url"):
                    lic = f'<a href="{esc(cr["license_url"])}" rel="license">{lic}</a>'
                author = fig.get("author") or cr.get("author") or "Unknown author"
                lines.append(f'<p><b>Author:</b> {esc(author)}</p>')
                if cr.get("credit") and cr["credit"] != author:
                    lines.append(f'<p><b>Source credit:</b> {esc(cr["credit"])}</p>')
                lines.append(f'<p><b>License:</b> {lic}</p>')
                lines.append(f'<p><b>Original file:</b> <a href="{esc(cr["source"])}">{esc(cr["title"])}</a> on Wikimedia Commons, retrieved {esc(cr.get("retrieved", ""))}</p>')
            out.append(f'  <li class="img-credit" id="credit-{fig["id"]}">{thumb}<div class="img-credit-body">' + "".join(lines) + "</div></li>")
        out.append("</ol>")
    return "\n".join(out)


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
    figs, credits = load_figures()
    placed = 0
    for page in PAGES:
        path = ROOT / page["file"]
        if not path.exists() or (only and page["file"] not in only):
            continue
        src = path.read_text(encoding="utf-8")
        new = stamp_figures(src, page, figs, credits)
        if page["file"] == "credits.html":
            new, _ = stamp(new, "credits", credits_html(figs, credits))
        placed += new.count('<figure class="fig"')
        if new != src:
            path.write_text(new, encoding="utf-8")
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

    print(f"Stamped {len(PAGES) - len(missing)} pages, placed {placed} figures, indexed {len(index)} sections.")
    waiting = [f["id"] for f in figs if f["id"] not in credits]
    if waiting:
        print(f"{len(waiting)} figures have no image yet (run scripts/fetch_images.py): {', '.join(waiting)}", file=sys.stderr)
    if missing:
        print("Missing pages (skipped):", ", ".join(missing), file=sys.stderr)


if __name__ == "__main__":
    main()
