"""Shared design system for every generated SVG: obsidian ground, sage trio, ink."""
from html import escape

P = dict(
    ground="#0B0E0D", deep="#060807", surface="#111614", surface2="#141917",
    line="#202723", ink="#EEF1ED", body="#C2C9C3", muted="#7E8781",
    s1="#5A6A60", s2="#788A7F", s3="#A6BDAD",
)
SANS = "-apple-system,'Instrument Sans','Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Geist Mono','JetBrains Mono',Menlo,Consolas,monospace"

STYLE = f"""<style>
  .sans{{font-family:{SANS}}}
  .mono{{font-family:{MONO}}}
  .pulse{{animation:pulse 2.6s ease-in-out infinite}}
  .blink{{animation:blink 1.4s step-end infinite}}
  .drift{{animation:drift 14s ease-in-out infinite alternate}}
  .drift2{{animation:drift2 18s ease-in-out infinite alternate}}
  .spin{{transform-origin:center;animation:spin 40s linear infinite}}
  .spinr{{transform-origin:center;animation:spinr 60s linear infinite}}
  .scan{{animation:scan 9s linear infinite}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
  @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
  @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-60px,24px)}}}}
  @keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(50px,-30px)}}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @keyframes spinr{{to{{transform:rotate(-360deg)}}}}
  @keyframes scan{{from{{transform:translateY(-120%)}}to{{transform:translateY(120%)}}}}
</style>"""

def defs(uid, w, h, rx=18):
    """Clip frame, glow filter, dot grid, and sage gradients. uid keeps ids unique per file."""
    return f"""<defs>
  <clipPath id="{uid}f"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
  <filter id="{uid}glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="{uid}soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="55"/></filter>
  <filter id="{uid}soft2" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="28"/></filter>
  <pattern id="{uid}dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{P['line']}"/>
  </pattern>
  <linearGradient id="{uid}sage" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{P['s1']}"/><stop offset="1" stop-color="{P['s3']}"/>
  </linearGradient>
  <linearGradient id="{uid}sagev" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{P['s3']}"/><stop offset="1" stop-color="{P['s1']}"/>
  </linearGradient>
  <linearGradient id="{uid}inkfade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{P['ink']}"/><stop offset="1" stop-color="{P['s3']}"/>
  </linearGradient>
  <linearGradient id="{uid}hair" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{P['s2']}" stop-opacity="0"/><stop offset=".5" stop-color="{P['s3']}"/><stop offset="1" stop-color="{P['s2']}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="{uid}fadeL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{P['ground']}"/><stop offset="1" stop-color="{P['ground']}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="{uid}fadeR" x1="1" y1="0" x2="0" y2="0">
    <stop offset="0" stop-color="{P['ground']}"/><stop offset="1" stop-color="{P['ground']}" stop-opacity="0"/>
  </linearGradient>
</defs>"""

def open_svg(w, h, label, uid, rx=18):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{escape(label, quote=True)}">\n{STYLE}\n{defs(uid, w, h, rx)}\n'
            f'<g clip-path="url(#{uid}f)">\n<rect width="{w}" height="{h}" fill="{P["ground"]}"/>\n'
            f'<rect width="{w}" height="{h}" fill="url(#{uid}dots)" opacity=".55"/>\n')

def close_svg(w, h, rx=18):
    return (f'</g>\n<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{P["line"]}"/>\n</svg>\n')

def glow_blob(uid, cx, cy, rx, ry, color, opacity, cls="drift"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{opacity}" filter="url(#{uid}soft)" class="{cls}"/>\n'

def text(x, y, s, size=12, fill=None, cls="sans", weight=None, anchor=None, ls=None, extra=""):
    fill = fill or P["body"]
    a = [f'x="{x}"', f'y="{y}"', f'class="{cls}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight: a.append(f'font-weight="{weight}"')
    if anchor: a.append(f'text-anchor="{anchor}"')
    if ls is not None: a.append(f'letter-spacing="{ls}"')
    if extra: a.append(extra)
    return f'<text {" ".join(a)}>{escape(s)}</text>\n'

def eyebrow(x, y, s, fill=None, anchor=None):
    return text(x, y, s, 10.5, fill or P["s2"], "mono", None, anchor, 2.2)

def reveal(inner, begin, dur=0.6, dy=10):
    """Fade-and-rise reveal for a group of elements."""
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin}s" dur="{dur}s" fill="freeze"/>\n'
            f'{inner}</g>\n')

def chip(x, y, label, fill=None, stroke=None, textfill=None, h=24, pad=12, size=10.5):
    w = int(len(label) * size * 0.66 + pad * 2)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill or P["surface"]}" stroke="{stroke or P["line"]}"/>'
            + text(x + w / 2, y + h / 2 + 3.6, label, size, textfill or P["s3"], "mono", "600", "middle", 1.4)), w

def panel(x, y, w, h, rx=14, fill=None, stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or P["surface"]}" stroke="{stroke or P["line"]}"/>\n'

def mark(x, y, side=14, gap=None, colors=None):
    """The three rounded squares, left to right s1, s2, s3."""
    gap = gap if gap is not None else side * 0.4
    colors = colors or [P["s1"], P["s2"], P["s3"]]
    r = side * 0.22
    return "".join(f'<rect x="{x + i*(side+gap):.1f}" y="{y}" width="{side}" height="{side}" rx="{r:.1f}" fill="{c}"/>' for i, c in enumerate(colors)) + "\n"

def hairline(uid, x, y, w):
    return f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="url(#{uid}hair)"/>\n'
