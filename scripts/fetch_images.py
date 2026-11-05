#!/usr/bin/env python3
"""
Download the openly licensed images listed in scripts/images.json.

For each entry with a "commons" file name this script:
  1. asks the Wikimedia API for the file's URL, author, license and source page,
  2. downloads a rendition at most MAX_SIDE pixels on its longer side,
  3. saves it as assets/img/<id>.webp,
  4. records the attribution in scripts/image-credits.json.

Entries with an "original" file are diagrams drawn for this guide; they already
live in assets/img/ and only get their size recorded.

Only files under a free license (public domain, CC0, CC BY, CC BY-SA and similar)
are accepted. Anything else stops the script so it can be replaced.

Run from anywhere:  python3 scripts/fetch_images.py          (fetch missing images)
                    python3 scripts/fetch_images.py --force  (re-fetch everything)
Then run scripts/build.py to place the figures in the pages.
"""
import html
import io
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "images.json"
CREDITS = ROOT / "scripts" / "image-credits.json"
IMG = ROOT / "assets" / "img"
API = "https://en.wikipedia.org/w/api.php"  # serves Commons file metadata, with gentler rate limits
UA = "VascularFieldGuide-ImageFetcher/1.0 (https://github.com/hashimsalar/VASCSurg)"
MAX_SIDE = 1400
QUALITY = 80

FREE = re.compile(r"^(public domain|pd|cc0|cc[ -]by(-sa)?[ -]?\d|cc-by(-sa)?-\d|cc by(-sa)? \d|no restrictions|"
                  r"wtfpl|attribution|licence ouverte|gfdl)", re.I)


def request(url, data=None):
    for attempt in range(20):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            # Honor the server's Retry-After; Wikimedia throttles busy shared IPs.
            wait = int(e.headers.get("retry-after") or 30) + random.randint(1, 5)
            print(f"  rate limited, retrying in {wait}s", file=sys.stderr, flush=True)
            time.sleep(wait)
    raise SystemExit(f"Gave up on {url}")


def text(value):
    """Plain text from the HTML fragments Commons returns in extmetadata."""
    value = re.sub(r"<br\s*/?>", " ", value or "")
    value = html.unescape(re.sub(r"<[^>]+>", "", value))
    return re.sub(r"\s+", " ", value).strip()


def file_info(titles):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        body = urllib.parse.urlencode({
            "action": "query", "format": "json", "formatversion": 2,
            "titles": "|".join("File:" + t for t in chunk),
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": MAX_SIDE,
        }).encode()
        data = json.loads(request(API, body))
        norm = {n["to"]: n["from"] for n in data["query"].get("normalized", [])}
        for page in data["query"]["pages"]:
            name = norm.get(page["title"], page["title"])[5:]
            if not page.get("imageinfo"):
                raise SystemExit(f"Not found on Commons: {name}")
            out[name] = page["imageinfo"][0]
    return out


def save_webp(raw, dest):
    im = Image.open(io.BytesIO(raw))
    im.seek(0)
    # Flatten transparency onto white: line drawings with clear backgrounds would vanish in dark mode.
    im = im.convert("RGBA")
    plate = Image.new("RGB", im.size, (255, 255, 255))
    plate.paste(im, mask=im.getchannel("A"))
    im = plate
    im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    im.save(dest, "WEBP", quality=QUALITY, method=6)
    return im.size


def svg_size(path):
    m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', path.read_text(encoding="utf-8"))
    return [round(float(m.group(1))), round(float(m.group(2)))]


def main():
    force = "--force" in sys.argv
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    credits = json.loads(CREDITS.read_text(encoding="utf-8")) if CREDITS.exists() else {}
    IMG.mkdir(parents=True, exist_ok=True)

    ids = [e["id"] for e in manifest]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"Duplicate ids in images.json: {', '.join(sorted(dupes))}")

    for e in manifest:
        if "original" in e:
            path = IMG / e["original"]
            if not path.exists():
                print(f'  missing original diagram: assets/img/{e["original"]}', file=sys.stderr)
                continue
            w, h = svg_size(path)
            credits[e["id"]] = {"file": f'assets/img/{e["original"]}', "width": w, "height": h,
                                "original": True, "basis": e.get("basis", "")}

    CREDITS.write_text(json.dumps(credits, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    todo = [e for e in manifest if "commons" in e and (force or e["id"] not in credits
            or credits[e["id"]].get("title") != e["commons"] or not (IMG / f'{e["id"]}.webp').exists())]
    info = file_info(sorted({e["commons"] for e in todo})) if todo else {}

    for e in todo:
        ii = info[e["commons"]]
        md = {k: v.get("value", "") for k, v in ii.get("extmetadata", {}).items()}
        lic = text(md.get("LicenseShortName")) or "unknown"
        if not FREE.search(lic):
            raise SystemExit(f'{e["id"]}: "{e["commons"]}" has license "{lic}", which is not a free license.')
        src = ii.get("thumburl") or ii["url"]
        if ii.get("mime") in ("image/jpeg", "image/png") and ii.get("width", 0) <= MAX_SIDE and ii.get("height", 0) <= MAX_SIDE:
            src = ii["url"]
        print(f'{e["id"]}: {e["commons"]} ({lic})', flush=True)
        size = save_webp(request(src), IMG / f'{e["id"]}.webp')
        credits[e["id"]] = {
            "title": e["commons"],
            "file": f'assets/img/{e["id"]}.webp',
            "width": size[0], "height": size[1],
            "author": text(md.get("Artist")) or text(md.get("Credit")) or "Unknown author",
            "credit": text(md.get("Credit")),
            "license": lic,
            "license_url": text(md.get("LicenseUrl")),
            "source": ii["descriptionurl"],
            "original_url": ii["url"].split("?")[0],
            "retrieved": time.strftime("%Y-%m-%d"),
        }
        CREDITS.write_text(json.dumps(credits, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        time.sleep(1)

    keep = set(ids)
    for stale in [k for k in credits if k not in keep]:
        del credits[stale]
    credits = {i: credits[i] for i in ids if i in credits}
    CREDITS.write_text(json.dumps(credits, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(credits)} images recorded in {CREDITS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
