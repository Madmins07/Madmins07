import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from repos import REPOS

def banner(name, r):
    W, H = 1000, 240
    uid = "b"
    s = open_svg(W, H, f"{r['title']}: {r['tagline']}", uid)
    s += glow_blob(uid, 860, 110, 220, 130, P["s2"], .22, "drift")
    s += glow_blob(uid, 120, 230, 260, 90, P["s1"], .18, "drift2")
    # orbital decoration, right side
    cx, cy = 866, 120
    s += f'<g class="spin" style="transform-origin:{cx}px {cy}px">'
    s += f'<circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{P["s1"]}" stroke-width="1" stroke-dasharray="3 7"/>'
    s += f'<circle cx="{cx+74}" cy="{cy}" r="3" fill="{P["s3"]}" filter="url(#{uid}glow)"/></g>\n'
    s += f'<g class="spinr" style="transform-origin:{cx}px {cy}px">'
    s += f'<circle cx="{cx}" cy="{cy}" r="48" fill="none" stroke="{P["s2"]}" stroke-width="1" stroke-dasharray="40 24" opacity=".8"/>'
    s += f'<circle cx="{cx}" cy="{cy-48}" r="2.4" fill="{P["ink"]}"/></g>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{P["s3"]}" stroke-width="1.2" stroke-dasharray="138" stroke-dashoffset="138"><animate attributeName="stroke-dashoffset" values="138;0" begin=".4s" dur="1.6s" fill="freeze"/></circle>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{P["s3"]}" class="pulse" filter="url(#{uid}glow)"/>\n'
    # left column
    s += reveal(eyebrow(48, 60, f"MADMINS07  /  {name.upper()}"), .1)
    s += reveal(text(48, 118, r["title"], 44, P["ink"], "sans", "700", ls="-1.4"), .25, .7, 14)
    s += f'<rect x="48" y="134" width="0" height="1.5" fill="url(#{uid}sage)"><animate attributeName="width" values="0;220" begin=".7s" dur=".9s" fill="freeze"/></rect>\n'
    s += reveal(text(48, 162, r["tagline"], 15.5, P["body"], "sans"), .55, .7, 10)
    x = 48
    inner = ""
    for i, c in enumerate(r["chips"]):
        piece, w = chip(x, 184, c)
        inner += piece
        x += w + 8
    s += reveal(inner, .85, .6, 8)
    # right meta
    s += reveal(eyebrow(952, 60, f"{r['kind']}  ·  {r['year']}", P["muted"], "end"), .4)
    s += reveal(text(952, 205, r["lang"].upper(), 10.5, P["muted"], "mono", anchor="end", ls="2.2"), .5)
    s += close_svg(W, H)
    return s

if __name__ == "__main__":
    for name, r in REPOS.items():
        os.makedirs(os.path.join(r["path"], "assets"), exist_ok=True)
        out = os.path.join(r["path"], "assets", "banner.svg")
        open(out, "w").write(banner(name, r))
        print("wrote", out, os.path.getsize(out))
