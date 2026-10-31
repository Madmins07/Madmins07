#!/usr/bin/env python3
"""Render the data-driven panels (projects, metrics) from stats.json. Usage: cards.py stats.json outdir"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from layout import slice_for, SELECTED
W = 1000

def projects(S):
    u = "j"; top, bottom, acc, nxt, H = slice_for("projects")
    s = open_svg(W, H, "Selected work: " + ", ".join(SELECTED), u, acc, nxt, top, bottom)
    s += glow_blob(u, 820, 360, 300, 110, acc, .14, "drift")
    s += spine(u, H, acc, "05", "SELECTED WORK")
    s += text(944, 56, f"STARS AND FORKS REFRESH NIGHTLY  ·  {S.get('generated','')}", 9.5, P["muted"], "mono", anchor="end", ls="2")
    cols = [P["cyan"], P["violet"], P["magenta"], P["pink"], P["orange"], P["gold"]]
    cw, ch = 272, 124
    for i, name in enumerate(S.get("selected", SELECTED)):
        r = S["repos"].get(name, {}); c, rr = i % 3, i // 3
        x, y = 88 + c * (cw + 12), 84 + rr * (ch + 12); col = cols[i % 6]
        desc = r.get("description", "") or ""
        words, lines, cur = desc.split(), [], ""
        for w_ in words:
            if len(cur) + len(w_) + 1 > 40 and cur: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
            if len(lines) == 2: break
        if cur and len(lines) < 2: lines.append(cur)
        if len(lines) == 2 and len(" ".join(lines)) < len(desc): lines[1] = lines[1][:37].rstrip() + "…"
        inner = panel(x, y, cw, ch, 12, P["surface"]) + f'<rect x="{x}" y="{y+16}" width="2" height="{ch-32}" rx="1" fill="{col}"/>'
        inner += text(x + 18, y + 30, name, 13, P["ink"], "mono", "700", ls="-.2")
        for k, l in enumerate(lines): inner += text(x + 18, y + 52 + k * 16, l, 11, P["body"], "sans")
        yb = y + ch - 18
        inner += f'<circle cx="{x+22}" cy="{yb-4}" r="4" fill="{r.get("color") or col}"/>' + text(x + 32, yb, r.get("language", "") or "", 10.5, P["muted"], "mono")
        inner += text(x + cw - 18, yb, f"★ {r.get('stars', 0)}    ⑂ {r.get('forks', 0)}", 10.5, P["body"], "mono", anchor="end")
        s += reveal(inner, .15 + i * .1, .6, 10)
    return s + close_svg(W, H)

def metrics(S):
    u = "k"; top, bottom, acc, nxt, H = slice_for("metrics")
    T, L, C, K = S["totals"], S["languages"], S.get("codeforces", {}), S["streak"]
    s = open_svg(W, H, f"Metrics: {T['stars']} stars, {T['repos']} repositories, {T['commits_year']} commits in the last year, Codeforces {C.get('rating','')}", u, acc, nxt, top, bottom)
    s += glow_blob(u, 200, 340, 300, 100, acc, .14, "drift2")
    s += spine(u, H, acc, "08", "METRICS")
    s += text(944, 56, f"GITHUB  ·  CODEFORCES  ·  LAST 365 DAYS  ·  {S.get('generated','')}", 9.5, P["muted"], "mono", anchor="end", ls="2")
    tiles = [("STARS", T["stars"], P["gold"]), ("REPOS", T["repos"], P["cyan"]), ("COMMITS / YR", T["commits_year"], P["violet"]), ("CONTRIBUTIONS", T["contributions_year"], P["magenta"])]
    for i, (lab, val, col) in enumerate(tiles):
        x, y = 88 + i * 152, 84
        inner = panel(x, y, 140, 76, 12, P["surface"]) + eyebrow(x + 14, y + 24, lab, P["muted"]) + text(x + 14, y + 58, f"{val:,}", 26, col, "mono", "700", ls="-1")
        s += reveal(inner, .15 + i * .1, .6, 8)
    # streak + codeforces
    x, y = 88 + 4 * 152, 84
    inner = panel(x, y, 248, 76, 12, P["surface"]) + eyebrow(x + 14, y + 24, "STREAK", P["muted"]) + text(x + 14, y + 58, f"{K['current']}d", 26, P["mint"], "mono", "700", ls="-1")
    inner += text(x + 90, y + 58, f"longest {K['longest']}d", 11, P["muted"], "mono")
    s += reveal(inner, .55, .6, 8)
    # languages
    s += reveal(eyebrow(88, 196, "LANGUAGES BY BYTES", P["muted"]), .6)
    bx, bw = 88, 520
    xx = bx
    cols = [P["cyan"], P["violet"], P["magenta"], P["pink"], P["gold"], P["mint"]]
    for i, (n, pct, color) in enumerate(L):
        w_ = bw * pct / 100
        s += f'<rect x="{xx:.1f}" y="208" width="0" height="10" rx="2" fill="{cols[i % 6]}"><animate attributeName="width" values="0;{max(w_-2,0):.1f}" begin="{.7+i*.1:.2f}s" dur=".8s" fill="freeze"/></rect>\n'
        xx += w_
    for i, (n, pct, color) in enumerate(L):
        cx_, cy_ = 88 + (i % 3) * 174, 244 + (i // 3) * 24
        s += reveal(f'<rect x="{cx_}" y="{cy_-9}" width="9" height="9" rx="2" fill="{cols[i % 6]}"/>' + text(cx_ + 16, cy_, n, 11.5, P["body"], "sans") + text(cx_ + 16 + len(n) * 7 + 8, cy_, f"{pct}%", 10.5, P["muted"], "mono"), .9 + i * .08)
    # codeforces ring
    if C.get("rating"):
        cx, cy, R = 760, 250, 44; circ = 2 * 3.14159 * R; frac = min(C["rating"] / 3000, 1)
        s += reveal(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{P["line"]}" stroke-width="8"/>'
                    f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{P["cyan"]}" stroke-width="8" stroke-linecap="round" transform="rotate(-90 {cx} {cy})" stroke-dasharray="0 {circ:.1f}"><animate attributeName="stroke-dasharray" values="0 {circ:.1f};{circ*frac:.1f} {circ*(1-frac):.1f}" begin="1s" dur="1.2s" fill="freeze"/></circle>'
                    + text(cx, cy + 6, str(C["rating"]), 17, P["ink"], "mono", "700", "middle", "-.5")
                    + eyebrow(cx + 64, cy - 10, "CODEFORCES", P["cyan"]) + text(cx + 64, cy + 10, (C.get("rank") or "").title(), 14, P["ink"], "sans", "600")
                    + text(cx + 64, cy + 28, f"peak {C.get('maxRating')}  ·  @Madmins07", 10.5, P["muted"], "mono"), 1.0, .7, 8)
    return s + close_svg(W, H)

if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for k, f in [("projects", projects), ("metrics", metrics)]:
        p = os.path.join(out, k + ".svg"); open(p, "w").write(f(S)); print("wrote", p, os.path.getsize(p))
