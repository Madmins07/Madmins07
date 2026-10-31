"""Shared design system: near-black ground, a spectrum of accents that travels down the page, ink type."""
from html import escape

P = dict(
    ground="#07080D", deep="#04050A", surface="#0E1019", surface2="#121528", line="#1C2032",
    ink="#F3F5FF", body="#B9BFD6", muted="#6F7693",
    cyan="#38E0FF", blue="#5B8CFF", violet="#8F5CFF", purple="#B45CFF", magenta="#FF4FD8",
    pink="#FF5FA8", coral="#FF6E7A", orange="#FF9A5C", gold="#FFC14D", mint="#5CFFB1",
)
AMOH = ("#5A6A60", "#788A7F", "#A6BDAD")   # the Amoh mark keeps its own colours, always
SPECTRUM = [P["cyan"], P["violet"], P["magenta"], P["gold"]]
SANS = "-apple-system,'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,Consolas,monospace"

STYLE = f"""<style>
  .sans{{font-family:{SANS}}}
  .mono{{font-family:{MONO}}}
  .pulse{{animation:pulse 2.6s ease-in-out infinite}}
  .blink{{animation:blink 1.4s step-end infinite}}
  .drift{{animation:drift 14s ease-in-out infinite alternate}}
  .drift2{{animation:drift2 18s ease-in-out infinite alternate}}
  .spin{{animation:spin 40s linear infinite}}
  .spinr{{animation:spinr 60s linear infinite}}
  .scan{{animation:scan 7s linear infinite}}
  .float{{animation:float 6s ease-in-out infinite alternate}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
  @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
  @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-70px,26px)}}}}
  @keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(60px,-34px)}}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @keyframes spinr{{to{{transform:rotate(-360deg)}}}}
  @keyframes scan{{from{{transform:translateY(-140%)}}to{{transform:translateY(140%)}}}}
  @keyframes float{{from{{transform:translateY(0)}}to{{transform:translateY(-8px)}}}}
</style>"""

def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    ra, rb = hexrgb(a), hexrgb(b)
    return "#%02x%02x%02x" % tuple(round(ra[i] + (rb[i] - ra[i]) * t) for i in range(3))

def defs(uid, w, h, accent=None, accent2=None, top=None, bottom=None, rx=0):
    """Clip, glow filters, dot grid, spectrum gradients, and this panel's slice of the page-long ground gradient."""
    accent = accent or P["cyan"]; accent2 = accent2 or accent
    top = top or P["ground"]; bottom = bottom or P["ground"]
    stops = "".join(f'<stop offset="{i/(len(SPECTRUM)-1):.2f}" stop-color="{c}"/>' for i, c in enumerate(SPECTRUM))
    return f"""<defs>
  <clipPath id="{uid}f"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
  <filter id="{uid}glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="{uid}glow2" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="12" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="{uid}soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="60"/></filter>
  <pattern id="{uid}dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P['line']}"/></pattern>
  <linearGradient id="{uid}ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>
  <linearGradient id="{uid}spine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
  <linearGradient id="{uid}spec" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>
  <linearGradient id="{uid}acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
  <linearGradient id="{uid}accv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
  <linearGradient id="{uid}rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
  <linearGradient id="{uid}hair" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}" stop-opacity="0"/></linearGradient>
  <linearGradient id="{uid}fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{top}" stop-opacity="0"/></linearGradient>
  <linearGradient id="{uid}fadeR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{top}" stop-opacity="0"/></linearGradient>
</defs>"""

def open_svg(w, h, label, uid, accent=None, accent2=None, top=None, bottom=None, dots=True, rx=0):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{escape(label, quote=True)}">\n{STYLE}\n{defs(uid, w, h, accent, accent2, top, bottom, rx)}\n'
            f'<g clip-path="url(#{uid}f)">\n<rect width="{w}" height="{h}" fill="url(#{uid}ground)"/>\n'
            + (f'<rect width="{w}" height="{h}" fill="url(#{uid}dots)" opacity=".5"/>\n' if dots else ""))

def close_svg(w, h, frame=False, rx=18):
    return "</g>\n" + (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{P["line"]}"/>\n' if frame else "") + "</svg>\n"

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
    return text(x, y, s, 10.5, fill or P["muted"], "mono", None, anchor, 2.2)

def reveal(inner, begin, dur=0.6, dy=10):
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin}s" dur="{dur}s" fill="freeze"/>\n'
            f'{inner}</g>\n')

def chip(x, y, label, fill=None, stroke=None, textfill=None, h=24, pad=12, size=10.5):
    w = int(len(label) * size * 0.66 + pad * 2)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill or P["surface"]}" stroke="{stroke or P["line"]}"/>'
            + text(x + w / 2, y + h / 2 + 3.6, label, size, textfill or P["body"], "mono", "600", "middle", 1.4)), w

def panel(x, y, w, h, rx=14, fill=None, stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or P["surface"]}" stroke="{stroke or P["line"]}"/>\n'

def mark(x, y, side=14, gap=None, colors=None):
    gap = gap if gap is not None else side * 0.4
    colors = colors or list(AMOH)
    r = side * 0.22
    return "".join(f'<rect x="{x + i*(side+gap):.1f}" y="{y}" width="{side}" height="{side}" rx="{r:.1f}" fill="{c}"/>' for i, c in enumerate(colors)) + "\n"

def hairline(uid, x, y, w):
    return f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="url(#{uid}hair)"/>\n'

SPINE_X = 40

def spine(uid, h, accent, num=None, title=None, ty=52, node=True):
    """The vertical rail that runs through every panel, with the section node and title."""
    s = f'<rect x="{SPINE_X-1}" y="0" width="2" height="{h}" fill="url(#{uid}spine)" opacity=".55"/>\n'
    if node:
        s += f'<circle cx="{SPINE_X}" cy="{ty}" r="9" fill="{P["ground"]}" stroke="{accent}" stroke-width="1.5"/>'
        s += f'<circle cx="{SPINE_X}" cy="{ty}" r="3.5" fill="{accent}" filter="url(#{uid}glow)" class="pulse"/>\n'
    if num is not None:
        s += text(SPINE_X + 26, ty + 4, num, 11, accent, "mono", "700", ls="2")
    if title:
        s += text(SPINE_X + 56, ty + 4.5, title, 13.5, P["ink"], "mono", "700", ls="2.6")
        s += f'<rect x="{SPINE_X+56}" y="{ty+14}" width="0" height="1.5" fill="url(#{uid}rule)"><animate attributeName="width" values="0;180" begin=".3s" dur=".9s" fill="freeze"/></rect>\n'
    return s
