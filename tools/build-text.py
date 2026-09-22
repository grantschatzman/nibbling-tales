"""Build the read-along text and recording script from the Project Gutenberg edition.

Usage:  python tools/build-text.py path/to/67098-h.htm path/to/gutenberg/images

Pagination rule (the recording script and the site both follow it):
  1. Every Shepard drawing starts a new page.
  2. A page over MAX_WORDS is split evenly at paragraph breaks; the extra pieces are text-only pages.
  3. A drawing with no text after it (end of a chapter) joins the page before it.
"""
import html as htmllib
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

MAX_WORDS = 250
NUMS = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
ROOT = Path(__file__).resolve().parent.parent

src_html = Path(sys.argv[1]).read_text(encoding="utf-8")
src_images = Path(sys.argv[2])

body = src_html[: src_html.index("*** END OF")]
starts = [m.start() for m in re.finditer(r'<h2><a name="CHAPTER_', body)] + [len(body)]
TOKEN = re.compile(
    r'<div class="figcenter">.*?src="images/(?P<img>illus\d+)\.jpg".*?</div>'
    r'|<h3>(?P<title>.*?)</h3>'
    r'|<p[^>]*>(?P<p>.*?)</p>'
    r'|<div class="poetry">(?P<verse>.*?)</div></div>'
    r'|(?P<tb><hr class="tb")',
    re.S,
)


def clean(fragment):
    """Keep <i>, drop every other tag, normalise whitespace and entities."""
    fragment = re.sub(r"<(?!/?i>)[^>]+>", "", fragment)
    fragment = htmllib.unescape(fragment)
    return " ".join(fragment.split())


def words(text):
    return len(re.sub(r"<[^>]+>", " ", text).split())


def first_words(blocks, n=8):
    for b in blocks:
        if b["type"] in ("p", "verse"):
            text = b["text"] if b["type"] == "p" else b["lines"][0]
            plain = re.sub(r"<[^>]+>", "", text).split()
            return " ".join(plain[:n]) + (" …" if len(plain) > n else "")
    return ""


used_images = set()
chapters = []
for n in range(1, 11):
    seg = body[starts[n - 1] : starts[n]]
    title = ""
    pages = []
    cur = None
    for m in TOKEN.finditer(seg):
        if m.group("title"):
            title = clean(m.group("title"))
            continue
        if m.group("img"):
            used_images.add(m.group("img"))
            if cur is None or cur["words"] > 0:
                cur = {"img": m.group("img"), "extra": [], "blocks": [], "words": 0}
                pages.append(cur)
            else:
                cur["extra"].append(m.group("img"))
            continue
        if cur is None:
            cur = {"img": None, "extra": [], "blocks": [], "words": 0}
            pages.append(cur)
        if m.group("p") is not None:
            t = clean(m.group("p"))
            if t:
                cur["blocks"].append({"type": "p", "text": t})
                cur["words"] += words(t)
        elif m.group("verse") is not None:
            lines = [clean(v) for v in re.findall(r'<div class="verse[^"]*">(.*?)</div>', m.group("verse"), re.S)]
            cur["blocks"].append({"type": "verse", "lines": lines})
            cur["words"] += sum(words(l) for l in lines)
        elif m.group("tb"):
            cur["blocks"].append({"type": "break"})

    # Rule 3: a trailing drawing with no text joins the previous page.
    if len(pages) > 1 and pages[-1]["words"] == 0:
        last = pages.pop()
        pages[-1]["blocks"].append({"type": "img", "img": last["img"]})
        for extra in last["extra"]:
            pages[-1]["blocks"].append({"type": "img", "img": extra})

    # Rule 2: split long pages evenly at block boundaries.
    final = []
    for pg in pages:
        if pg["words"] <= MAX_WORDS:
            final.append(pg)
            continue
        remaining = math.ceil(pg["words"] / MAX_WORDS)
        target = pg["words"] / remaining
        chunk, acc, first = [], 0, True
        for b in pg["blocks"]:
            chunk.append(b)
            acc += words(b.get("text", "")) + sum(words(l) for l in b.get("lines", []))
            if remaining > 1 and acc >= target * 0.9 and b["type"] != "break":
                final.append({"img": pg["img"] if first else None, "extra": pg["extra"] if first else [], "blocks": chunk, "words": acc})
                chunk, acc, first, remaining = [], 0, False, remaining - 1
        if chunk:
            final.append({"img": pg["img"] if first else None, "extra": pg["extra"] if first else [], "blocks": chunk, "words": acc})

    out_pages = []
    for pg in final:
        blocks = []
        if pg["img"]:
            blocks.append({"type": "img", "img": pg["img"]})
        for extra in pg["extra"]:
            blocks.append({"type": "img", "img": extra})
        blocks += [b for b in pg["blocks"] if not (b["type"] == "break" and not blocks)]
        out_pages.append({"blocks": blocks, "starts": first_words(pg["blocks"]), "words": pg["words"]})

    chapters.append({"number": n, "title": title, "pages": out_pages})
    out = ROOT / "text" / f"ch{n}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"number": n, "title": title, "pages": [{"blocks": p["blocks"]} for p in out_pages]}, ensure_ascii=False, indent=1), encoding="utf-8")

# Drawings, re-inked warm brown on transparent.
book_art = ROOT / "art" / "book"
book_art.mkdir(parents=True, exist_ok=True)
for name in sorted(used_images):
    g = Image.open(src_images / f"{name}.jpg").convert("L")
    a = ImageOps.invert(g).point(lambda v: 0 if v < 28 else min(255, int((v - 28) * 1.25)))
    bbox = a.point(lambda v: 255 if v > 60 else 0).getbbox()
    a = a.crop(bbox)
    im = Image.new("RGBA", a.size, (62, 47, 35, 0))
    im.putalpha(a)
    im.thumbnail((560, 560), Image.LANCZOS)
    im.quantize(colors=24, method=Image.Quantize.FASTOCTREE).save(book_art / f"{name}.png", optimize=True)

# Recording script: one page per chapter section, printable, with page breaks called out.
esc = htmllib.escape
parts = []
for ch in chapters:
    n = ch["number"]
    parts.append(f'<section class="chapter" id="ch{n}"><h2>Chapter {NUMS[n]}</h2><p class="title">{esc(ch["title"])}</p>')
    parts.append(f'<p class="count">{len(ch["pages"])} pages · {len(ch["pages"]) - 1} page labels</p>')
    for i, pg in enumerate(ch["pages"], 1):
        if i > 1:
            parts.append(f'<div class="turn"><span>PAGE {i}</span> Ctrl+B → type <b>page</b></div>')
        else:
            parts.append('<div class="turn first"><span>PAGE 1</span> no label, the chapter starts here</div>')
        for b in pg["blocks"]:
            if b["type"] == "p":
                parts.append(f"<p>{b['text']}</p>")
            elif b["type"] == "verse":
                parts.append('<p class="verse">' + "<br>".join(b["lines"]) + "</p>")
            elif b["type"] == "break":
                parts.append('<p class="orn">* * *</p>')
            elif b["type"] == "img":
                parts.append(f'<img src="art/book/{b["img"]}.png" alt="">')
    parts.append("</section>")

toc = " · ".join(f'<a href="#ch{c["number"]}">{c["number"]}</a>' for c in chapters)
script_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Recording Script</title>
<style>
:root {{ --ink:#3E2F23; --soft:#6B5846; --honey:#E3A51F; --paper:#FBF3E1; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:20px/1.55 Georgia, serif; }}
main {{ max-width:680px; margin:0 auto; padding:24px 16px 80px; }}
h1 {{ font-weight:400; margin:0 0 4px; }}
.how {{ background:#fff8e6; border:1.5px solid var(--ink); border-radius:12px; padding:12px 16px; font-size:17px; }}
nav {{ margin:14px 0; font-size:18px; }}
h2 {{ font-weight:400; margin:48px 0 0; border-top:2px solid var(--ink); padding-top:16px; }}
.title {{ font-style:italic; color:var(--soft); margin:2px 0; }}
.count {{ font-size:16px; color:var(--soft); }}
.turn {{ margin:28px 0 14px; padding:8px 12px; background:var(--honey); border:1.5px solid var(--ink); border-radius:8px; font:600 16px system-ui, sans-serif; }}
.turn.first {{ background:#efe3c6; }}
.turn span {{ display:inline-block; min-width:92px; font-size:19px; }}
.verse {{ font-style:italic; padding-left:24px; }}
.orn {{ text-align:center; color:var(--soft); }}
img {{ display:block; max-width:220px; max-height:180px; margin:10px auto; opacity:.8; }}
@media print {{ .turn {{ break-after:avoid; }} img {{ max-height:110px; }} }}
</style></head><body><main>
<h1>Recording Script</h1>
<p class="how">Read straight through. At each honey bar, press <b>Ctrl+B</b> in Audacity and type <b>page</b>,
right before the first word of that page (you can also add them afterwards while listening back).
Scene labels use any other name. Export with <b>File → Export → Export Labels</b> into <code>audio/</code>,
named like the mp3 but ending <code>.txt</code>.</p>
<nav>Chapter: {toc}</nav>
{''.join(parts)}
</main></body></html>
"""
(ROOT / "recording-script.html").write_text(script_html, encoding="utf-8")

for ch in chapters:
    print(ch["number"], len(ch["pages"]), [p["words"] for p in ch["pages"]])
