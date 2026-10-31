import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from repos import REPOS

def banner(name, r):
    Hh, uid = 220, "b"
    s = open_svg(W, Hh, f"{r['title']}: {r['tagline']}", uid, rx=14)
    s += f'<rect x="{RAIL-.5}" y="0" width="1" height="{Hh}" fill="{P["line2"]}"/><rect x="{RAIL-4}" y="52" width="8" height="8" fill="{P["accent"]}"/>\n'
    s += reveal(text(RAIL + 26, 60, f"MADMINS07  /  {name.upper()}", 10.5, P["accent"], "mono", "700", ls="2.4"), .1)
    s += reveal(label(RIGHT, 60, f"{r['kind']}  ·  {r['year']}  ·  {r['lang'].upper()}", P["muted"], "end"), .2)
    s += hline(RAIL + 26, RIGHT, 74)
    s += reveal(text(LEFT, 126, r["title"], 42, P["ink"], "sans", "800", ls="-1.6"), .25, .7, 12)
    s += grow(LEFT, 140, 44, 3, P["accent"], .7, 0, .5)
    s += reveal(text(LEFT, 168, r["tagline"], 14.5, P["body"], "sans"), .5, .6, 8)
    x, inner = LEFT, ""
    for c in r["chips"]:
        piece, w = chip(x, 184, c, P["body"]); inner += piece; x += w + 6
    s += reveal(inner, .75, .5, 6)
    return s + close_svg(W, Hh, frame=True, rx=14)

if __name__ == "__main__":
    for name, r in REPOS.items():
        os.makedirs(os.path.join(r["path"], "assets"), exist_ok=True)
        out = os.path.join(r["path"], "assets", "banner.svg"); open(out, "w").write(banner(name, r)); print("wrote", out)
