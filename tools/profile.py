import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from repos import PROFILE

OUT = os.path.join(PROFILE["path"], "assets")
PREV = os.environ.get("PREVIEW_DIR", "/tmp/madmins07-preview")

# ---------------------------------------------------------------- header
def header():
    W, H, u = 1000, 400, "h"
    s = open_svg(W, H, "Madhav Agarwal. Operations at Amoh, the medical AI research lab. Industrial and Systems Engineering, IIT Kharagpur, class of 2028.", u)
    s += glow_blob(u, 790, 120, 260, 150, P["s2"], .22, "drift")
    s += glow_blob(u, 160, 420, 300, 110, P["s1"], .20, "drift2")
    s += hairline(u, 0, 300, W)
    # scanline, very faint
    s += f'<rect x="0" y="0" width="{W}" height="60" fill="url(#{u}sagev)" opacity=".035" class="scan"/>\n'
    s += reveal(eyebrow(56, 90, "MADHAV AGARWAL   ·   IIT KHARAGPUR '28   ·   KOLKATA"), .1)
    s += reveal(text(56, 152, "Madhav Agarwal", 60, f"url(#{u}inkfade)", "sans", "700", ls="-2.4"), .3, .8, 16)
    s += f'<rect x="56" y="170" width="0" height="1.5" fill="url(#{u}sage)"><animate attributeName="width" values="0;300" begin=".8s" dur="1s" fill="freeze"/></rect>\n'
    roles = ["Operations at Amoh, the medical AI research lab.",
             "Quant research. Time series. Optimisation.",
             "Advisor, Kharagpur Data Analytics Group.",
             "Codeforces Specialist. Problems after midnight."]
    n, per = len(roles), 4.2
    for i, r_ in enumerate(roles):
        s += (f'<text x="56" y="206" class="sans" font-size="17.5" fill="{P["body"]}" opacity="0">{r_}'
              f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.2;.24;1" dur="{n*per}s" begin="{1.2+i*per}s" repeatCount="indefinite"/></text>\n')
    s += reveal(text(56, 244, "Building the infrastructure that lets models do real clinical work.", 13.5, P["muted"]) +
                text(56, 264, "Reading stochastic calculus on the side.", 13.5, P["muted"]), 1.0, .8, 8)
    # signal / noise panel
    px, py, pw, ph = 622, 70, 322, 206
    s += reveal(panel(px, py, pw, ph, 16, P["surface"]) +
                eyebrow(px + 18, py + 28, "SIGNAL  /  NOISE") +
                text(px + pw - 18, py + 28, "ILLUSTRATIVE", 9.5, P["muted"], "mono", anchor="end", ls="2"), .5, .8, 12)
    rnd = random.Random(7)
    cx0, cx1, cy0, cy1 = px + 18, px + pw - 18, py + 52, py + ph - 22
    N = 44
    base = [0.0] * N
    v = 0.45
    for i in range(N):
        v += (rnd.random() - 0.47) * 0.09 + 0.006
        v = min(max(v, .12), .92)
        base[i] = v
    noisy = [min(max(b + (rnd.random() - .5) * .22, .05), .98) for b in base]
    smooth = [sum(base[max(0, i-3):i+4]) / len(base[max(0, i-3):i+4]) for i in range(N)]
    def pts(a):
        return [(cx0 + (cx1 - cx0) * i / (N - 1), cy1 - (cy1 - cy0) * y) for i, y in enumerate(a)]
    def path(p):
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    def length(p):
        return sum(math.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]) for i in range(len(p)-1))
    pn, ps = pts(noisy), pts(smooth)
    for gy in range(4):
        y = cy0 + (cy1 - cy0) * gy / 3
        s += f'<line x1="{cx0}" y1="{y:.1f}" x2="{cx1}" y2="{y:.1f}" stroke="{P["line"]}" stroke-dasharray="2 5"/>\n'
    s += f'<path d="{path(ps)} L{ps[-1][0]:.1f} {cy1} L{ps[0][0]:.1f} {cy1} Z" fill="url(#{u}sagev)" opacity="0"><animate attributeName="opacity" values="0;.16" begin="2.6s" dur="1s" fill="freeze"/></path>\n'
    ln = length(pn)
    s += f'<path d="{path(pn)}" fill="none" stroke="{P["muted"]}" stroke-width="1" opacity=".55" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"><animate attributeName="stroke-dashoffset" values="{ln:.0f};0" begin="1.1s" dur="2.2s" fill="freeze"/></path>\n'
    ls_ = length(ps)
    s += f'<path d="{path(ps)}" fill="none" stroke="{P["s3"]}" stroke-width="2" stroke-linejoin="round" filter="url(#{u}glow)" stroke-dasharray="{ls_:.0f}" stroke-dashoffset="{ls_:.0f}"><animate attributeName="stroke-dashoffset" values="{ls_:.0f};0" begin="1.4s" dur="2.4s" fill="freeze"/></path>\n'
    ex, ey = ps[-1]
    s += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{P["ink"]}" opacity="0" filter="url(#{u}glow)"><animate attributeName="opacity" values="0;1" begin="3.7s" dur=".3s" fill="freeze"/></circle>\n'
    s += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="9" fill="none" stroke="{P["s3"]}" opacity="0"><animate attributeName="opacity" values="0;.8;0" begin="3.8s" dur="2.4s" repeatCount="indefinite"/><animate attributeName="r" values="5;14" begin="3.8s" dur="2.4s" repeatCount="indefinite"/></circle>\n'
    s += text(cx0, cy1 + 16, "noise", 9.5, P["muted"], "mono", ls="1.6")
    s += text(cx1, cy1 + 16, "signal", 9.5, P["s3"], "mono", anchor="end", ls="1.6")
    # bottom chips
    x = 56
    inner = ""
    # Amoh chip with the mark
    lab = "AMOH  ·  OPERATIONS"
    w = int(len(lab) * 10.5 * .66 + 24 + 50)
    inner += f'<rect x="{x}" y="332" width="{w}" height="26" rx="13" fill="{P["surface"]}" stroke="{P["s1"]}"/>'
    inner += mark(x + 13, 332 + 8.5, 9, 4)
    inner += text(x + 60, 332 + 17, lab, 10.5, P["s3"], "mono", "600", ls="1.4")
    x += w + 8
    for lab in ["KDAG  ·  ADVISOR", "WORLDQUANT  ·  GOLD", "CODEFORCES  ·  1541"]:
        piece, w = chip(x, 333, lab, h=24)
        inner += piece
        x += w + 8
    s += reveal(inner, 1.3, .7, 8)
    s += reveal(f'<circle cx="{W-150}" cy="345" r="3.2" fill="{P["s3"]}" class="blink"/>' +
                text(W - 140, 349, "IST  ·  UTC+5:30", 10.5, P["muted"], "mono", ls="1.6"), 1.5)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- amoh
def amoh():
    W, H, u = 1000, 250, "a"
    s = open_svg(W, H, "Building Amoh. The medical AI research lab. RL environments and data for models that do clinical work.", u)
    s += glow_blob(u, 860, 130, 240, 140, P["s1"], .26, "drift2")
    # pixel motif, right
    rnd = random.Random(3)
    cols = [P["s1"], P["s2"], P["s3"]]
    inner = ""
    for gx in range(9):
        for gy in range(6):
            if rnd.random() < .42: continue
            c = cols[min(2, int(gx / 3))]
            sz = 16
            X, Y = 700 + gx * 26, 42 + gy * 26
            d = .4 + rnd.random() * 1.4
            inner += (f'<rect x="{X}" y="{Y}" width="{sz}" height="{sz}" rx="3.5" fill="{c}" opacity="0">'
                      f'<animate attributeName="opacity" values="0;.9" begin="{d:.2f}s" dur=".5s" fill="freeze"/>'
                      f'<animate attributeName="opacity" values=".9;.35;.9" begin="{d+2:.2f}s" dur="{3+rnd.random()*4:.1f}s" repeatCount="indefinite"/></rect>')
    s += inner + "\n"
    s += reveal(mark(56, 44, 22, 9) + text(56 + 3 * 22 + 2 * 9 + 14, 62, "Amoh", 24, P["ink"], "sans", "600", ls="-0.5") +
                eyebrow(56, 100, "BUILDING  ·  2026  ·  OPERATIONS"), .1)
    s += reveal(text(56, 136, "The medical AI research lab.", 30, P["ink"], "sans", "600", ls="-1.1"), .35, .7, 12)
    s += reveal(text(56, 162, "RL environments and data for models that do clinical work.", 14.5, P["body"]), .55, .7, 8)
    x = 56
    inner = ""
    for i, lab in enumerate(["01  ENVIRONMENTS", "02  EVALS", "03  TRACES", "04  TRAINING"]):
        piece, w = chip(x, 188, lab, textfill=P["s3"] if i == 0 else P["s2"])
        inner += piece
        x += w + 8
    s += reveal(inner, .85, .6, 8)
    s += reveal(text(x + 10, 204, "10+ US clinic partners", 11.5, P["muted"], "mono", ls="1"), 1.1)
    s += reveal(text(944, 232, "amoh.ai", 10.5, P["s3"], "mono", anchor="end", ls="2"), 1.2)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- stack
def stack():
    W, H, u = 1000, 330, "s"
    mods = [("PYTHON", "research, modelling, most things", 9),
            ("C++", "contests, anything that must be fast", 7),
            ("MACHINE LEARNING", "TensorFlow, scikit-learn, XGBoost", 7),
            ("TIME SERIES", "ARIMA, Prophet, statsmodels", 7),
            ("OPTIMISATION", "PuLP, dynamic and integer programming", 6),
            ("STATISTICS", "econometrics, stochastic calculus", 6),
            ("WEB", "React, Node, Vite, Docker", 5),
            ("TOOLING", "pandas, NumPy, Streamlit, git", 7)]
    s = open_svg(W, H, "Stack: Python, C++, machine learning, time series, optimisation, statistics, web, tooling", u)
    s += glow_blob(u, 500, 340, 420, 110, P["s1"], .16, "drift")
    s += eyebrow(56, 44, "STACK  ·  MODULES")
    s += text(944, 44, "SEGMENTS = CONFIDENCE, NOT HOURS", 9.5, P["muted"], "mono", anchor="end", ls="2")
    cw, ch, gx, gy = 214, 112, 10, 12
    for i, (name, sub, lvl) in enumerate(mods):
        col, row = i % 4, i // 4
        x, y = 56 + col * (cw + gx), 66 + row * (ch + gy)
        inner = panel(x, y, cw, ch, 12, P["surface"])
        inner += text(x + 16, y + 26, f"{i+1:02d}", 10, P["muted"], "mono", ls="1.5")
        inner += text(x + 16, y + 50, name, 13.5, P["ink"], "mono", "700", ls="1.2")
        inner += text(x + 16, y + 68, sub, 11, P["muted"], "sans")
        for k in range(10):
            on = k < lvl
            fill = P["s3"] if on else P["line"]
            sx = x + 16 + k * 18.4
            inner += (f'<rect x="{sx:.1f}" y="{y+84}" width="13" height="6" rx="2" fill="{fill}" opacity="{".0" if on else "1"}">'
                      + (f'<animate attributeName="opacity" values="0;1" begin="{.6+i*.08+k*.05:.2f}s" dur=".3s" fill="freeze"/>' if on else "") + '</rect>')
        s += reveal(inner, .15 + i * .09, .6, 10)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- timeline
def timeline():
    W, H, u = 1000, 330, "t"
    nodes = [("JUL 2024", "Seventh Triangle", "R&D Intern", "four months, applied research", "past"),
             ("SEP 2024", "Myntra", "Strategy Intern", "brand launch, go to market", "past"),
             ("MAY 2025", "PharmEasy", "Summer Intern", "ten weeks, Bangalore", "past"),
             ("2025-26", "KDAG", "Executive Head", "curriculum, projects, inductions", "past"),
             ("2026", "Amoh", "Operations", "the medical AI research lab", "now"),
             ("2026-27", "KDAG", "Advisor", "steering the group", "now"),
             ("2027", "L.E.K. Consulting", "Summer Associate", "incoming", "next")]
    s = open_svg(W, H, "Timeline: Seventh Triangle and Myntra in 2024, PharmEasy in 2025, KDAG Executive Head, Amoh Operations and KDAG Advisor in 2026, L.E.K. Consulting incoming in 2027", u)
    s += glow_blob(u, 640, 165, 230, 120, P["s1"], .18, "drift")
    s += eyebrow(56, 44, "TRACK RECORD  ·  FLIGHT PATH")
    y0 = 180
    x0, x1 = 80, 920
    s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{P["line"]}" stroke-width="2"/>\n'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="url(#{u}sage)" stroke-width="2" stroke-dasharray="{x1-x0}" stroke-dashoffset="{x1-x0}"><animate attributeName="stroke-dashoffset" values="{x1-x0};0" begin=".3s" dur="2s" fill="freeze"/></line>\n'
    n = len(nodes)
    for i, (when, who, role, sub, state) in enumerate(nodes):
        x = x0 + 28 + i * (x1 - x0 - 56) / (n - 1)
        up = i % 2 == 0
        ty = y0 - 42 if up else y0 + 48
        b = .55 + i * .22
        col = P["s3"] if state == "now" else (P["s2"] if state == "next" else P["s1"])
        inner = f'<line x1="{x:.0f}" y1="{y0 + (-12 if up else 12)}" x2="{x:.0f}" y2="{ty + (6 if up else -34)}" stroke="{P["line"]}"/>'
        if up:
            inner += eyebrow(x, ty - 44, when, col, "middle") + text(x, ty - 22, who, 16, P["ink"], "sans", "700", "middle", "-.4")
            inner += text(x, ty - 5, role, 12, P["body"], "sans", anchor="middle") + text(x, ty + 10, sub, 10.5, P["muted"], "sans", anchor="middle")
        else:
            inner += eyebrow(x, ty - 14, when, col, "middle") + text(x, ty + 8, who, 16, P["ink"], "sans", "700", "middle", "-.4")
            inner += text(x, ty + 25, role, 12, P["body"], "sans", anchor="middle") + text(x, ty + 40, sub, 10.5, P["muted"], "sans", anchor="middle")
        s += reveal(inner, b, .5, 6)
        dash = ' stroke-dasharray="3 3"' if state == "next" else ""
        s += (f'<circle cx="{x:.0f}" cy="{y0}" r="7" fill="{P["ground"]}" stroke="{col}" stroke-width="2.2"{dash} opacity="0">'
              f'<animate attributeName="opacity" values="0;1" begin="{b-.15:.2f}s" dur=".3s" fill="freeze"/></circle>\n')
        if state == "now":
            s += (f'<circle cx="{x:.0f}" cy="{y0}" r="7" fill="none" stroke="{P["s3"]}" opacity="0">'
                  f'<animate attributeName="r" values="7;20" begin="{b+.5:.2f}s" dur="2.4s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values=".9;0" begin="{b+.5:.2f}s" dur="2.4s" repeatCount="indefinite"/></circle>\n')
            s += f'<circle cx="{x:.0f}" cy="{y0}" r="3" fill="{P["s3"]}" filter="url(#{u}glow)"/>\n'
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- positions
def positions():
    W, H, u = 1000, 350, "p"
    rows = [("LONG", "Amoh", "position size: all in", "▲  open", True),
            ("LONG", "Stochastic calculus", "Shreve, volume I, second read", "▲  +412.6%", True),
            ("LONG", "The Codeforces grind", "rating goes up, eventually", "▲  +128.4%", True),
            ("LONG", "Chai at 2 a.m.", "the only reliable alpha", "▲  +96.2%", True),
            ("LONG", "K-pop during backtests", "inexplicable, but it works", "▲  +64.8%", True),
            ("SHORT", "8 a.m. lectures", "structurally impaired", "▼  -71.3%", False),
            ("SHORT", "Notebook outputs in git", "most of my repos, regrettably", "▼  -44.9%", False),
            ("SHORT", "Sleep, in exam week", "liquidated early", "▼  -88.1%", False)]
    s = open_svg(W, H, "A tongue in cheek blotter: long Amoh, long stochastic calculus, long the Codeforces grind, short 8 a.m. lectures", u)
    s += eyebrow(56, 44, "POSITIONS  ·  OPEN")
    s += text(944, 44, "MARKED TO MARKET  ·  NOT INVESTMENT ADVICE", 9.5, P["muted"], "mono", anchor="end", ls="2")
    s += text(56, 76, "SIDE", 9.5, P["muted"], "mono", ls="2") + text(150, 76, "POSITION", 9.5, P["muted"], "mono", ls="2") + text(944, 76, "P&L", 9.5, P["muted"], "mono", anchor="end", ls="2")
    s += f'<line x1="56" y1="86" x2="944" y2="86" stroke="{P["line"]}"/>\n'
    for i, (side, pos, sub, pnl, long) in enumerate(rows):
        y = 112 + i * 31
        col = P["s3"] if long else P["muted"]
        inner = f'<rect x="56" y="{y-15}" width="60" height="20" rx="10" fill="{P["surface"]}" stroke="{P["s1"] if long else P["line"]}"/>'
        inner += text(86, y - 1, side, 9.5, col, "mono", "700", "middle", "1.5")
        inner += text(150, y, pos, 14, P["ink"], "sans", "600")
        inner += text(150 + len(pos) * 7.6 + 14, y, sub, 11, P["muted"], "sans")
        inner += text(944, y, pnl, 13, col, "mono", "600", "end")
        inner += f'<line x1="56" y1="{y+10}" x2="944" y2="{y+10}" stroke="{P["line"]}" opacity=".7"/>'
        s += reveal(inner, .2 + i * .1, .5, 6)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- day
def day():
    W, H, u = 1000, 320, "d"
    segs = [("00:00", "Codeforces, late problems", 2, P["s3"]),
            ("02:00", "Sleep, allegedly", 6, P["line"]),
            ("08:00", "Lectures and labs", 5, P["s1"]),
            ("13:00", "Mess, chai, walking", 1, P["s2"]),
            ("14:00", "Amoh, KDAG, projects", 3, P["s3"]),
            ("17:00", "Gym, music, offline", 2, P["muted"]),
            ("19:00", "Research and backtests", 5, P["ink"])]
    s = open_svg(W, H, "A twenty four hour ring of a typical day: late Codeforces, six hours of sleep, lectures, Amoh and KDAG in the afternoon, research at night", u)
    s += glow_blob(u, 230, 170, 150, 150, P["s1"], .22, "drift2")
    s += eyebrow(56, 44, "A DAY AT THE DESK  ·  24H")
    s += text(944, 44, "IST  ·  SUBJECT TO DEADLINES", 9.5, P["muted"], "mono", anchor="end", ls="2")
    cx, cy, R, sw = 230, 178, 92, 20
    C = 2 * math.pi * R
    start = 0
    for i, (t, lab, h, col) in enumerate(segs):
        L = C * h / 24
        gap = 2.5
        s += (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{col}" stroke-width="{sw}" '
              f'stroke-dasharray="0 {C:.1f}" stroke-dashoffset="{-start:.1f}" transform="rotate(-90 {cx} {cy})" opacity=".92">'
              f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};{L-gap:.1f} {C-L+gap:.1f}" begin="{.3+i*.18:.2f}s" dur=".7s" fill="freeze"/></circle>\n')
        start += L
    s += f'<circle cx="{cx}" cy="{cy}" r="{R-sw/2-6}" fill="none" stroke="{P["line"]}" stroke-dasharray="2 6"/>\n'
    for k, lab in [(0, "00"), (6, "06"), (12, "12"), (18, "18")]:
        a = math.radians(k * 15 - 90)
        s += text(cx + math.cos(a) * (R - sw / 2 - 20), cy + math.sin(a) * (R - sw / 2 - 20) + 3.5, lab, 9.5, P["muted"], "mono", anchor="middle", ls="1")
    s += text(cx, cy + 6, "24h", 16, P["ink"], "sans", "700", "middle", "-.5")
    # legend
    for i, (t, lab, h, col) in enumerate(segs):
        y = 84 + i * 30
        inner = f'<rect x="420" y="{y-10}" width="10" height="10" rx="2.5" fill="{col}"/>'
        inner += text(442, y, t, 11, P["s2"], "mono", ls="1")
        inner += text(500, y, lab, 13.5, P["ink"], "sans", "500")
        inner += text(944, y, f"{h}h", 12, P["body"], "mono", anchor="end")
        inner += f'<line x1="420" y1="{y+10}" x2="944" y2="{y+10}" stroke="{P["line"]}" opacity=".7"/>'
        s += reveal(inner, .3 + i * .12, .5, 6)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- music
def music():
    W, H, u = 1000, 200, "m"
    st = [("Sukoon", "the late-desk playlist"), ("Calm Synths", "for long proofs and longer backtests"),
          ("K-pop", "non negotiable"), ("EDM", "contest mode")]
    s = open_svg(W, H, "Frequencies: Sukoon, Calm Synths, K-pop, EDM", u)
    s += eyebrow(56, 44, "FREQUENCIES  ·  NOW PLAYING")
    s += text(944, 44, "APPLE MUSIC", 9.5, P["muted"], "mono", anchor="end", ls="2")
    rnd = random.Random(11)
    cw = 214
    for i, (name, sub) in enumerate(st):
        x, y = 56 + i * (cw + 10), 64
        inner = panel(x, y, cw, 110, 12, P["surface"])
        bx0, by = x + 16, y + 56
        for k in range(14):
            h1, h2 = 4 + rnd.random() * 10, 10 + rnd.random() * 26
            bx = bx0 + k * 13.2
            inner += (f'<rect x="{bx:.1f}" y="{by-h1:.1f}" width="7" height="{h1:.1f}" rx="2" fill="{P["s3"] if k % 3 else P["s2"]}" opacity=".9">'
                      f'<animate attributeName="height" values="{h1:.1f};{h2:.1f};{h1:.1f}" dur="{.9+rnd.random()*1.4:.2f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="y" values="{by-h1:.1f};{by-h2:.1f};{by-h1:.1f}" dur="{.9+rnd.random()*1.4:.2f}s" repeatCount="indefinite"/></rect>')
        inner += text(x + 16, y + 82, name, 14.5, P["ink"], "sans", "600", ls="-.3")
        inner += text(x + 16, y + 98, sub, 10.5, P["muted"], "sans")
        s += reveal(inner, .15 + i * .12, .6, 8)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- footer
def footer():
    W, H, u = 1000, 150, "f"
    s = open_svg(W, H, "The market closes. Curiosity does not.", u)
    s += glow_blob(u, 500, 160, 300, 70, P["s1"], .2, "drift")
    s += hairline(u, 300, 44, 400)
    s += reveal(text(500, 86, "the market closes. curiosity doesn't.", 22, P["s3"], "sans", "500", "middle", "-.5", 'font-style="italic"'), .2, .9, 8)
    s += reveal(text(470, 118, "SESSION PERSISTS", 10.5, P["muted"], "mono", anchor="end", ls="2") +
                f'<circle cx="486" cy="114" r="3.2" fill="{P["s3"]}" class="blink"/>' +
                text(500, 118, "KOLKATA, IN", 10.5, P["muted"], "mono", ls="2"), .6)
    s += close_svg(W, H)
    return s

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(PREV, exist_ok=True)
    parts = dict(header=header(), amoh=amoh(), stack=stack(), timeline=timeline(), positions=positions(),
                 dayinthelife=day(), music=music(), footer=footer())
    html = ""
    for k, v in parts.items():
        open(os.path.join(OUT, k + ".svg"), "w").write(v)
        open(os.path.join(PREV, "p-" + k + ".svg"), "w").write(v)
        html += f'<h3>{k}</h3><img src="p-{k}.svg">\n'
        print("wrote", k, len(v))
    open(os.path.join(PREV, "index.html"), "w").write(
        '<!doctype html><meta charset="utf-8"><body style="background:#0d1117;padding:24px;color:#ccc;font-family:sans-serif">'
        '<style>img{width:900px;display:block;margin:0 0 18px}</style>' + html)
