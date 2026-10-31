import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from repos import REPOS

def banner(name, r):
    W, H, uid = 1000, 240, "b"
    acc = P[r.get("accent", "cyan")]
    s = open_svg(W, H, f"{r['title']}: {r['tagline']}", uid, acc, acc, P["ground"], "#0A0A16", rx=18)
    s += glow_blob(uid, 860, 110, 240, 130, acc, .18, "drift")
    s += glow_blob(uid, 120, 240, 280, 90, P["violet"], .14, "drift2")
    cx, cy = 866, 120
    s += f'<g class="spin" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{P["line"]}" stroke-width="1" stroke-dasharray="3 7"/><circle cx="{cx+74}" cy="{cy}" r="3" fill="{acc}" filter="url(#{uid}glow)"/></g>\n'
    s += f'<g class="spinr" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy}" r="48" fill="none" stroke="{acc}" stroke-width="1" stroke-dasharray="40 24" opacity=".5"/><circle cx="{cx}" cy="{cy-48}" r="2.4" fill="{P["ink"]}"/></g>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="url(#{uid}spec)" stroke-width="1.4" stroke-dasharray="138" stroke-dashoffset="138"><animate attributeName="stroke-dashoffset" values="138;0" begin=".4s" dur="1.6s" fill="freeze"/></circle>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{acc}" class="pulse" filter="url(#{uid}glow)"/>\n'
    s += f'<rect x="{SPINE_X-1}" y="0" width="2" height="{H}" fill="url(#{uid}spine)" opacity=".5"/><circle cx="{SPINE_X}" cy="60" r="3.5" fill="{acc}" filter="url(#{uid}glow)"/>\n'
    s += reveal(eyebrow(66, 64, f"MADMINS07  /  {name.upper()}", acc), .1)
    s += reveal(text(66, 122, r["title"], 44, P["ink"], "sans", "800", ls="-1.6"), .25, .7, 14)
    s += f'<rect x="66" y="138" width="0" height="2" fill="url(#{uid}spec)"><animate attributeName="width" values="0;240" begin=".7s" dur=".9s" fill="freeze"/></rect>\n'
    s += reveal(text(66, 166, r["tagline"], 15.5, P["body"], "sans"), .55, .7, 10)
    x, inner = 66, ""
    for c in r["chips"]:
        piece, w = chip(x, 188, c, textfill=acc); inner += piece; x += w + 8
    s += reveal(inner, .85, .6, 8)
    s += reveal(eyebrow(952, 64, f"{r['kind']}  ·  {r['year']}", P["muted"], "end"), .4)
    s += reveal(text(952, 209, r["lang"].upper(), 10.5, P["muted"], "mono", anchor="end", ls="2.2"), .5)
    return s + close_svg(W, H, frame=True, rx=18)

if __name__ == "__main__":
    for name, r in REPOS.items():
        os.makedirs(os.path.join(r["path"], "assets"), exist_ok=True)
        out = os.path.join(r["path"], "assets", "banner.svg"); open(out, "w").write(banner(name, r)); print("wrote", out)
