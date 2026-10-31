"""Design system: graphite neutrals, one accent, flat fills, hairlines. No gradients, no glows."""
from html import escape

P = dict(
    ground="#0A0B0E", surface="#111318", surface2="#15181F", line="#1F232B", line2="#2A2F39",
    ink="#F4F5F7", body="#AEB4BF", muted="#6A7280", faint="#3A4049",
    accent="#FF7A1A", accent2="#C45A0F",
)
AMOH = ("#5A6A60", "#788A7F", "#A6BDAD")   # the Amoh mark keeps its own colours
SANS = "-apple-system,'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,Consolas,monospace"
W = 1000
RAIL = 40
LEFT = 88
RIGHT = 944

STYLE = f"""<style>
  .sans{{font-family:{SANS}}}
  .mono{{font-family:{MONO}}}
  .blink{{animation:blink 1.2s step-end infinite}}
  @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
</style>"""

def defs(uid, w, h, rx=0):
    return f"""<defs>
  <clipPath id="{uid}f"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
  <pattern id="{uid}dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P['line']}"/></pattern>
</defs>"""

def open_svg(w, h, label, uid, rx=0, dots=True):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(label, quote=True)}">\n'
            f'{STYLE}\n{defs(uid, w, h, rx)}\n<g clip-path="url(#{uid}f)">\n<rect width="{w}" height="{h}" fill="{P["ground"]}"/>\n'
            + (f'<rect width="{w}" height="{h}" fill="url(#{uid}dots)" opacity=".45"/>\n' if dots else ""))

def close_svg(w, h, frame=False, rx=0):
    return "</g>\n" + (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{P["line"]}"/>\n' if frame else "") + "</svg>\n"

def text(x, y, s, size=12, fill=None, cls="sans", weight=None, anchor=None, ls=None, extra=""):
    fill = fill or P["body"]
    a = [f'x="{x}"', f'y="{y}"', f'class="{cls}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight: a.append(f'font-weight="{weight}"')
    if anchor: a.append(f'text-anchor="{anchor}"')
    if ls is not None: a.append(f'letter-spacing="{ls}"')
    if extra: a.append(extra)
    return f'<text {" ".join(a)}>{escape(str(s))}</text>\n'

def label(x, y, s, fill=None, anchor=None, size=10):
    return text(x, y, s, size, fill or P["muted"], "mono", None, anchor, 2.4)

def reveal(inner, begin, dur=0.55, dy=8):
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin}s" dur="{dur}s" fill="freeze"/>\n{inner}</g>\n')

def hline(x1, x2, y, color=None, op=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color or P["line"]}" opacity="{op}"/>\n'

def grow(x, y, w, h, fill, begin, rx=0, dur=.8):
    """A bar that grows from zero width."""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="0" height="{h:.1f}" rx="{rx}" fill="{fill}"><animate attributeName="width" values="0;{w:.1f}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/></rect>\n'

def section(uid, h, num, title, right=None, y=52):
    """Rail, square node, number, title, hairline. Shared by every panel."""
    s = f'<rect x="{RAIL-.5}" y="0" width="1" height="{h}" fill="{P["line2"]}"/>\n'
    s += f'<rect x="{RAIL-4}" y="{y-4}" width="8" height="8" fill="{P["accent"]}"/>\n'
    s += text(RAIL + 26, y + 4, num, 11, P["accent"], "mono", "700", ls="2")
    s += text(LEFT, y + 4.5, title, 13, P["ink"], "mono", "700", ls="3")
    if right: s += label(RIGHT, y + 4, right, P["muted"], "end")
    s += hline(LEFT, RIGHT, y + 22)
    return s

def mark(x, y, side=14, gap=None, colors=None):
    gap = gap if gap is not None else side * 0.4
    colors = colors or list(AMOH); r = side * 0.22
    return "".join(f'<rect x="{x + i*(side+gap):.1f}" y="{y}" width="{side}" height="{side}" rx="{r:.1f}" fill="{c}"/>' for i, c in enumerate(colors)) + "\n"

def chip(x, y, s, fill=None, h=22, size=10):
    w = int(len(s) * size * 0.66 + 22)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{P["surface"]}" stroke="{P["line"]}"/>'
            + text(x + w / 2, y + h / 2 + 3.4, s, size, fill or P["body"], "mono", "600", "middle", 1.6)), w

def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n and cur: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    if cur: lines.append(cur)
    return lines
