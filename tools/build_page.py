"""Build a printable HTML page beside each Markdown file named.

The markdown is the source of truth and is never modified. Re-run after
every edit, from the repository root:

    python tools/build_page.py events/2026-09-05-madison-foxconn/report.md
    python tools/build_page.py events/*/*.md dockets/*/*.md

Standard library only. Handles the subset of markdown the pages use:
headings, paragraphs, bold/italic/code, links, tables, blockquotes, rules,
lists, and images. An image line followed by an italic line becomes a figure
with that line as its caption; consecutive figures of the same image are
merged, captions kept in order. Links to other .md files point at their .html
builds. The Sortition USA logo in assets/ heads every page.
"""
import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT              # folder of the page being built; set per file

# Letterhead: shown top right, level with the page title.
LOGO_FILE = ROOT / "assets" / "sortition-usa-logo.png"
LOGO_ALT = "Sortition USA"

# Masthead template. The first "#" heading is split on the first separator:
#   "# The Saturday Board - The Foxconn Decision"
# gives the title "The Saturday Board" and the subtitle "The Foxconn Decision".
# The title keeps its size and the subtitle is stretched to its width. The
# logo sits on the right, a little shorter than the title block, and it is the
# logo that shrinks if the two do not fit side by side.
TITLE_SPLIT = re.compile(r"\s+[-–—]\s+|:\s+")

CSS = """
  .masthead{--mast:104px;display:flex;align-items:center;justify-content:space-between;
    gap:26px;margin:0 0 18px}
  .masthead img{flex:0 1 auto;min-width:0;max-width:100%;
    max-height:calc(var(--mast) * .72);width:auto;height:auto;display:block}
  .titleblock{display:flex;flex-direction:column;justify-content:center;
    height:var(--mast);flex:0 0 auto}
  .titleblock h1{margin:0;white-space:nowrap;
    font-size:calc(var(--mast) * .52);line-height:1;letter-spacing:-.015em}
  .titleblock .subtitle{white-space:nowrap;margin-top:calc(var(--mast) * .08);
    font:600 calc(var(--mast) * .2)/1 ui-sans-serif,system-ui,sans-serif;
    text-transform:uppercase;color:var(--soft)}
  @media (max-width:720px){
    .masthead{--mast:64px;flex-direction:column-reverse;align-items:flex-start;gap:14px}
    .titleblock{height:auto}
    .titleblock h1,.titleblock .subtitle{white-space:normal}}
  :root{--ink:#1a1a1f;--soft:#5d5d68;--line:#d7d2c6;--paper:#fdfcf8;
        --red:#c0392b;--wash:#f5f2ea}
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--wash);color:var(--ink);
    font:16.5px/1.65 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
  .sheet{max-width:52rem;margin:0 auto;background:var(--paper);
    padding:56px 60px 80px;box-shadow:0 2px 24px rgba(40,36,28,.12)}
  h1{font-size:clamp(28px,4.4vw,40px);line-height:1.12;letter-spacing:-.02em;margin:0 0 10px}
  h2{font-size:23px;line-height:1.25;margin:46px 0 14px;padding-top:16px;
    border-top:1px solid var(--line)}
  h3{font-size:17.5px;margin:30px 0 8px}
  p{margin:0 0 15px}
  ul,ol{margin:0 0 15px;padding-left:22px} li{margin-bottom:9px}
  a{color:inherit;text-decoration-color:var(--red);text-underline-offset:2px}
  hr{border:0;border-top:1px solid var(--line);margin:34px 0}
  code{font:500 13.5px/1 ui-monospace,Consolas,monospace;background:var(--wash);
    padding:1px 5px;border-radius:3px}
  blockquote{margin:22px 0;padding:16px 22px;border-left:5px solid var(--red);
    background:var(--wash);font-size:18px}
  blockquote p:last-child{margin:0}
  table{border-collapse:collapse;width:100%;margin:0 0 18px;
    font:14.5px/1.5 ui-sans-serif,system-ui,sans-serif}
  .tablewrap{overflow-x:auto}
  th,td{border-bottom:1px solid var(--line);padding:9px;text-align:left;vertical-align:top}
  th{font-weight:700;background:var(--wash);font-size:12.5px;
    text-transform:uppercase;letter-spacing:.05em;color:var(--soft)}
  figure{margin:28px 0}
  /* every figure fits the page width; height follows the aspect ratio */
  figure img{width:100%;max-width:100%;height:auto;display:block;
    border:1px solid var(--line);border-radius:2px}
  figcaption{font:13.5px/1.55 ui-sans-serif,system-ui,sans-serif;color:var(--soft);margin-top:9px}
  figcaption p{margin:0 0 6px}
  @media (max-width:720px){.sheet{padding:34px 20px 60px}}
  @media print{body{background:#fff}.sheet{box-shadow:none;max-width:none;padding:0}
    h2{break-after:avoid} figure,table,blockquote{break-inside:avoid}
  }
"""


def inline(text):
    """Escape, then apply code, bold, italic."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<em>\1</em>", p)
        out.append(p)
    return "".join(out)


def link(m):
    text, href = m.group(1), m.group(2)
    if "://" not in href:
        href = re.sub(r"\.md(?=$|#)", ".html", href)
    return f'<a href="{href}">{text}</a>'


def resolve_image(src):
    return src


def is_caption(line):
    s = line.strip()
    return s.startswith("*") and not s.startswith("**") and s.endswith("*")


def build(md):
    lines = md.splitlines()
    out, i = [], 0
    last_fig = None                      # [src, alt, [captions]] of the previous block, if a figure
    missing = []

    def flush_fig():
        nonlocal last_fig
        if last_fig is None:
            return
        src, alt, caps = last_fig
        img = f'<img src="{html.escape(src)}" alt="{html.escape(alt)}">'
        cap = "".join(f"<p>{inline(c)}</p>" for c in caps)
        out.append(f"<figure>{img}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
        last_fig = None

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            alt, src = m.group(1), resolve_image(m.group(2))
            if not (HERE / src).exists():
                missing.append(src)
            i += 1
            cap_lines = []
            if i < len(lines) and lines[i].strip().startswith("*") and not lines[i].strip().startswith("**"):
                while i < len(lines) and lines[i].strip():
                    cap_lines.append(lines[i].strip())
                    if lines[i].strip().endswith("*"):
                        i += 1
                        break
                    i += 1
            caption = " ".join(cap_lines)
            if caption.startswith("*") and caption.endswith("*"):
                caption = caption[1:-1]
            if last_fig and last_fig[0] == src:
                if caption:
                    last_fig[2].append(caption)
            else:
                flush_fig()
                last_fig = [src, alt, [caption] if caption else []]
            continue

        flush_fig()

        h = re.match(r"(#{1,6})\s+(.*)", s)
        if h:
            n = len(h.group(1))
            heading = f"<h{n}>{inline(h.group(2))}</h{n}>"
            if n == 1 and not any("masthead" in o for o in out):
                parts = TITLE_SPLIT.split(h.group(2).strip(), maxsplit=1)
                block = f"<h1>{inline(parts[0])}</h1>"
                if len(parts) > 1:
                    block += f'<div class="subtitle">{inline(parts[1])}</div>'
                logo = ""
                logo_src = Path(os.path.relpath(LOGO_FILE, HERE)).as_posix()
                if LOGO_FILE.exists():
                    logo = f'<img src="{html.escape(logo_src)}" alt="{html.escape(LOGO_ALT)}">'
                else:
                    missing.append(logo_src)
                heading = f'<header class="masthead"><div class="titleblock">{block}</div>{logo}</header>'
            out.append(heading)
            i += 1
            continue

        if re.fullmatch(r"-{3,}|\*{3,}", s):
            out.append("<hr>")
            i += 1
            continue

        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = lambda r: [c.strip() for c in r.strip("|").split("|")]
            head = cells(rows[0])
            body = [cells(r) for r in rows[1:] if not re.fullmatch(r"\|?[\s:\-|]+\|?", r)]
            t = "<div class='tablewrap'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>")
            continue

        if s.startswith(">"):
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(q))}</p></blockquote>")
            continue

        if re.match(r"([-*]|\d+\.)\s+", s):
            ordered = bool(re.match(r"\d+\.", s))
            items = []
            while i < len(lines) and lines[i].strip():
                t = lines[i].strip()
                if re.match(r"([-*]|\d+\.)\s+", t):
                    items.append(re.sub(r"^([-*]|\d+\.)\s+", "", t))
                else:
                    items[-1] += " " + t
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,6}\s|\||>|!\[|-{3,}\s*$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")

    flush_fig()
    return "\n".join(out), missing


# Stretch the subtitle to the title's width with letter-spacing, shrinking
# the subtitle's type first if it is already wider. Skipped on narrow screens, where
# both lines are allowed to wrap. Re-runs once web fonts settle and on resize.
FIT_JS = """
(function(){
  function fit(){
    var h = document.querySelector('.titleblock h1');
    var s = document.querySelector('.titleblock .subtitle');
    if (!h) return;
    h.style.fontSize = '';
    if (s){ s.style.letterSpacing = ''; s.style.fontSize = ''; }
    if (window.matchMedia('(max-width:720px)').matches) return;
    var range = document.createRange();
    function width(el){ range.selectNodeContents(el); return range.getBoundingClientRect().width; }
    if (!s) return;
    var target = width(h), text = s.textContent, gaps = Math.max(1, text.length - 1);
    var now = width(s);
    if (now > target){
      var fs = parseFloat(getComputedStyle(s).fontSize);
      s.style.fontSize = (fs * target / now) + 'px';
      now = width(s);
    }
    // letter-spacing also trails the last glyph, so spread over len-1 gaps
    s.style.letterSpacing = ((target - now) / gaps) + 'px';
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', fit);
  window.addEventListener('resize', fit);
  window.addEventListener('beforeprint', fit);
})();
"""


def build_file(src):
    global HERE
    src = Path(src).resolve()
    HERE = src.parent
    out = src.with_suffix(".html")
    md = src.read_text(encoding="utf-8")
    body, missing = build(md)
    title = re.search(r"^#\s+(.*)$", md, re.M)
    title = html.escape(title.group(1).strip()) if title else src.stem
    page = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{title}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
        f"<div class=\"sheet\">\n{body}\n</div>\n<script>{FIT_JS}</script>\n</body>\n</html>\n"
    )
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT).as_posix()} ({len(page):,} chars)")
    for m in missing:
        print(f"  MISSING IMAGE: {m}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for src in sys.argv[1:]:
        build_file(src)


if __name__ == "__main__":
    main()
