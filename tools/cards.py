#!/usr/bin/env python3
"""Render the data panels from stats.json: projects, codeforces, activity. Usage: cards.py stats.json outdir"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from layout import H, SELECTED

def projects(S):
    u, h = "j", H["projects"]
    try: fallback = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "repos.json")))
    except Exception: fallback = {}
    s = open_svg(W, h, "Selected work: " + ", ".join(SELECTED), u)
    s += section(u, h, "05", "SELECTED WORK", f"STARS REFRESH NIGHTLY  ·  {S.get('generated','')}")
    repos = S.get("repos", {})
    for i, name in enumerate(S.get("selected", SELECTED)):
        r = repos.get(name, {}); col, row = i % 2, i // 2
        x, y = LEFT + col * 440, 110 + row * 70
        lines_ = wrap(r.get("description") or fallback.get(name, {}).get("desc", ""), 52); desc = lines_[:2]
        if len(lines_) > 2: desc[1] = desc[1][:49].rstrip(" ,.;:") + "…"
        inner = text(x, y, f"{i+1:02d}", 10, P["accent"], "mono", "700", ls="2") + text(x + 30, y, name, 13.5, P["ink"], "mono", "700")
        for k, l in enumerate(desc): inner += text(x + 30, y + 18 + k * 15, l, 11, P["body"], "sans")
        inner += text(x + 416, y, f"★ {r.get('stars', 0)}", 11, P["muted"], "mono", anchor="end")
        inner += text(x + 416, y + 18, r.get("language", "") or "", 10, P["muted"], "mono", anchor="end", ls="1")
        inner += hline(x, x + 416, y + 50, P["line"], .9)
        s += reveal(inner, .15 + i * .08)
    return s + close_svg(W, h)

def codeforces(S):
    u, h = "c", H["codeforces"]
    C = S.get("codeforces", {}); hist = S.get("cf_history", [])
    s = open_svg(W, h, f"Competitive programming: Codeforces rating {C.get('rating')} ({C.get('rank')}), {C.get('solved')} problems solved over {C.get('contests')} rated contests", u)
    s += section(u, h, "06", "COMPETITIVE PROGRAMMING", f"CODEFORCES  ·  @{'MADMINS07'}  ·  {S.get('generated','')}")
    # big numbers
    nums = [("RATING", C.get("rating", "–")), ("PEAK", C.get("maxRating", "–")), ("SOLVED", C.get("solved", "–")), ("CONTESTS", C.get("contests", "–"))]
    for i, (k, v) in enumerate(nums):
        x = LEFT + i * 140
        s += reveal(label(x, 100, k) + text(x, 134, v, 30, P["ink"] if i else P["accent"], "mono", "700", ls="-1"), .2 + i * .08)
    s += reveal(label(RIGHT, 100, (C.get("rank") or "").upper(), P["accent"], "end") + label(RIGHT, 134, "RANK", anchor="end"), .5)
    # rating curve
    gx0, gx1, gy0, gy1 = LEFT, 600, 170, 380
    if hist:
        rs = [c["r"] for c in hist]; lo, hi = 0, max(1700, max(rs) + 100)
        ys = lambda r: gy1 - (gy1 - gy0) * (r - lo) / (hi - lo)
        for band, name in [(1200, "PUPIL"), (1400, "SPECIALIST"), (1600, "EXPERT")]:
            if band < hi:
                s += hline(gx0, gx1, ys(band), P["line"], 1) + label(gx0 + 4, ys(band) - 4, f"{band}  {name}", P["faint"], size=9)
        s += hline(gx0, gx1, gy1, P["line2"])
        pts = [(gx0 + (gx1 - gx0) * i / max(1, len(hist) - 1), ys(c["r"])) for i, c in enumerate(hist)]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        L = sum(((pts[i+1][0]-pts[i][0])**2 + (pts[i+1][1]-pts[i][1])**2) ** .5 for i in range(len(pts)-1))
        s += f'<path d="{d} L{pts[-1][0]:.1f} {gy1} L{pts[0][0]:.1f} {gy1} Z" fill="{P["accent"]}" opacity="0"><animate attributeName="opacity" values="0;.1" begin="1.6s" dur=".8s" fill="freeze"/></path>\n'
        s += f'<path d="{d}" fill="none" stroke="{P["accent"]}" stroke-width="2" stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"><animate attributeName="stroke-dashoffset" values="{L:.0f};0" begin=".6s" dur="1.6s" fill="freeze"/></path>\n'
        for (x, y), c in zip(pts, hist):
            s += f'<rect x="{x-2.5:.1f}" y="{y-2.5:.1f}" width="5" height="5" fill="{P["ground"]}" stroke="{P["accent"]}" opacity="0"><animate attributeName="opacity" values="0;1" begin="2s" dur=".4s" fill="freeze"/></rect>\n'
        first, last = dt.datetime.fromtimestamp(hist[0]["t"]), dt.datetime.fromtimestamp(hist[-1]["t"])
        s += label(gx0, gy1 + 18, first.strftime("%b %Y").upper(), P["muted"], size=9) + label(gx1, gy1 + 18, last.strftime("%b %Y").upper(), P["muted"], "end", 9)
        best = C.get("best")
        if best:
            bi = next(i for i, c in enumerate(hist) if c["t"] == best["t"]); bx, by = pts[bi]
            right_half = bx > (gx0 + gx1) / 2; tx = bx - 8 if right_half else bx + 8; anc = "end" if right_half else None
            s += reveal(f'<line x1="{bx:.1f}" y1="{by+8:.1f}" x2="{bx:.1f}" y2="{by+54:.1f}" stroke="{P["line2"]}"/>' +
                        text(tx, by + 46, f"+{best['d']}  ·  rank {best['rank']}", 10, P["ink"], "mono", "700", anc) +
                        text(tx, by + 58, best["name"][:36], 9.5, P["muted"], "sans", anchor=anc), 2.3)
    # difficulty histogram (right)
    dx0, dw = 660, 284
    diff = C.get("difficulty", [])
    s += label(dx0, 172, "SOLVED BY DIFFICULTY", P["muted"])
    if diff:
        mx = max(v for _, v in diff) or 1; n = len(diff); bw = min(22, (dw - 4 * (n - 1)) / n); base = 262
        for i, (r, v) in enumerate(diff):
            bh = 6 + 52 * (v / mx) ** .5; x = dx0 + i * (bw + 4)
            s += f'<rect x="{x:.1f}" y="{base}" width="{bw:.1f}" height="0" fill="{P["accent"]}" fill-opacity="{.35 + .65 * v / mx:.2f}"><animate attributeName="height" values="0;{bh:.1f}" begin="{.8+i*.05:.2f}s" dur=".6s" fill="freeze"/><animate attributeName="y" values="{base};{base-bh:.1f}" begin="{.8+i*.05:.2f}s" dur=".6s" fill="freeze"/></rect>\n'
            s += text(x + bw / 2, base + 14, str(r), 8, P["muted"], "mono", anchor="middle")
            if v == mx or i == len(diff) - 1: s += text(x + bw / 2, base - bh - 5, str(v), 9, P["body"], "mono", anchor="middle")
    # tags (right, lower)
    tags = C.get("tags", [])[:6]
    s += label(dx0, 300, "TOP TAGS", P["muted"])
    if tags:
        mx = tags[0][1]
        for i, (t, v) in enumerate(tags):
            y = 318 + i * 17
            s += text(dx0, y + 8, t, 10, P["body"], "mono") + text(dx0 + dw, y + 8, str(v), 9.5, P["muted"], "mono", anchor="end")
            s += grow(dx0 + 150, y + 1, (dw - 150 - 30) * v / mx, 7, P["accent"], 1 + i * .08)
    return s + close_svg(W, h)

def activity(S):
    u, h = "v", H["activity"]
    T, K, L = S.get("totals", {}), S.get("streak", {}), S.get("languages", [])
    s = open_svg(W, h, f"Activity: {T.get('contributions_year','')} contributions in the last year, {T.get('commits_year','')} commits, streak {K.get('current','')} days", u)
    s += section(u, h, "07", "ACTIVITY", f"GITHUB  ·  {T.get('repos', '–')} REPOS  ·  {T.get('stars', '–')} STARS  ·  LAST 365 DAYS  ·  {S.get('generated','')}")
    weeks = S.get("weeks", [])
    cell, gap = 10, 3; hx, hy = LEFT, 112
    if weeks:
        mx = max((c for w in weeks for _, c in w), default=1) or 1
        last_month = None; last_label_x = -100
        for wi, w in enumerate(weeks):
            for di, (date, c) in enumerate(w):
                x, y = hx + wi * (cell + gap), hy + di * (cell + gap)
                if c == 0: s += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{P["surface2"]}"/>'
                else:
                    op = .3 + .7 * min(1, (c / mx) ** .5)
                    s += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{P["accent"]}" fill-opacity="{op:.2f}" opacity="0"><animate attributeName="opacity" values="0;1" begin="{.3+wi*.02:.2f}s" dur=".4s" fill="freeze"/></rect>'
            m = w[-1][0][:7]
            lx = hx + wi * (cell + gap)
            if m != last_month and lx - last_label_x >= 28:
                last_month = m; last_label_x = lx
                s += text(lx, hy - 8, dt.datetime.strptime(m, "%Y-%m").strftime("%b").upper(), 8, P["muted"], "mono", ls="1")
        s += "\n"
    nums = [("CONTRIBUTIONS", T.get("contributions_year", "–")), ("COMMITS", T.get("commits_year", "–")), ("STREAK", f"{K.get('current', '–')}d"), ("LONGEST", f"{K.get('longest', '–')}d")]
    for i, (k, v) in enumerate(nums):
        y = 104 + i * 46
        s += reveal(label(820, y, k, size=9) + text(820, y + 24, v, 22, P["ink"], "mono", "700", ls="-.5") + hline(820, RIGHT, y + 32), .3 + i * .08)
    # languages bar
    s += label(LEFT, 226, "LANGUAGES BY BYTES", P["muted"])
    bx, bw, by = LEFT, 690, 238; xx = bx
    for i, (n, pct) in enumerate(L):
        w_ = bw * pct / 100
        s += grow(xx, by, max(w_ - 2, 0), 8, P["accent"], .6 + i * .1) .replace('fill="#FF7A1A"', f'fill="{P["accent"]}" fill-opacity="{1 - i * .15:.2f}"')
        xx += w_
    x = LEFT
    for i, (n, pct) in enumerate(L):
        lab_ = f"{n}  {pct}%"
        s += reveal(f'<rect x="{x}" y="{262}" width="8" height="8" fill="{P["accent"]}" fill-opacity="{1 - i * .15:.2f}"/>' + text(x + 14, 270, lab_, 10, P["body"], "mono"), .8 + i * .05)
        x += 14 + len(lab_) * 6.3 + 22
    return s + close_svg(W, h)

if __name__ == "__main__":
    S = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for k, f in [("projects", projects), ("codeforces", codeforces), ("activity", activity)]:
        p = os.path.join(out, k + ".svg"); open(p, "w").write(f(S)); print("wrote", p, os.path.getsize(p))
