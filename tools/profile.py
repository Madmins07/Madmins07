import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from layout import slice_for, SELECTED
from repos import PROFILE, REPOS

OUT = os.path.join(PROFILE["path"], "assets")
PREV = os.environ.get("PREVIEW_DIR", "/tmp/madmins07-preview")
W = 1000

def start(key, uid, label, dots=True):
    top, bottom, acc, nxt, h = slice_for(key)
    return open_svg(W, h, label, uid, acc, nxt, top, bottom, dots), acc, nxt, h

# ---------------------------------------------------------------- 00 header
def header():
    u = "h"
    s, acc, nxt, H = start("header", u, "Madhav Agarwal. Operations at Amoh, the medical AI research lab. Industrial and Systems Engineering, IIT Kharagpur, class of 2028.")
    s += glow_blob(u, 820, 90, 280, 150, P["cyan"], .16, "drift")
    s += glow_blob(u, 240, 470, 320, 120, P["violet"], .22, "drift2")
    s += glow_blob(u, 560, 300, 160, 90, P["magenta"], .10, "drift")
    s += f'<rect x="0" y="0" width="{W}" height="90" fill="url(#{u}accv)" opacity=".05" class="scan"/>\n'
    s += spine(u, H, acc, "00", None, 52)
    s += reveal(eyebrow(SPINE_X + 56, 56, "START  ·  PROFILE", acc), .05)
    s += reveal(eyebrow(66, 104, "IIT KHARAGPUR '28   ·   KOLKATA   ·   IST"), .1)
    s += reveal(text(66, 176, "Madhav Agarwal", 66, f"url(#{u}spec)", "sans", "800", ls="-2.8", extra=f'filter="url(#{u}glow2)"'), .3, .9, 18)
    s += f'<rect x="66" y="194" width="0" height="2" fill="url(#{u}spec)"><animate attributeName="width" values="0;420" begin=".9s" dur="1.1s" fill="freeze"/></rect>\n'
    roles = ["Operations at Amoh, the medical AI research lab.",
             "Quant research. Time series. Optimisation.",
             "Advisor, Kharagpur Data Analytics Group.",
             "Codeforces Specialist. Problems after midnight."]
    n, per = len(roles), 4.2
    for i, r_ in enumerate(roles):
        s += (f'<text x="66" y="232" class="sans" font-size="18" fill="{P["ink"]}" opacity="0">{r_}'
              f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.2;.24;1" dur="{n*per}s" begin="{1.2+i*per}s" repeatCount="indefinite"/></text>\n')
    s += reveal(text(66, 268, "Building the infrastructure that lets models do real clinical work.", 13.5, P["body"]) +
                text(66, 288, "Reading stochastic calculus on the side. Shipping on the other side.", 13.5, P["muted"]), 1.0, .8, 8)
    # signal panel
    px, py, pw, ph = 622, 72, 322, 236
    s += reveal(panel(px, py, pw, ph, 16, P["surface"]) + eyebrow(px + 18, py + 28, "SIGNAL  /  NOISE", acc) +
                text(px + pw - 18, py + 28, "ILLUSTRATIVE", 9.5, P["muted"], "mono", anchor="end", ls="2"), .5, .8, 12)
    rnd = random.Random(7); N = 46
    cx0, cx1, cy0, cy1 = px + 18, px + pw - 18, py + 54, py + ph - 26
    base, v = [], .45
    for i in range(N):
        v = min(max(v + (rnd.random() - .47) * .09 + .006, .12), .92); base.append(v)
    noisy = [min(max(b + (rnd.random() - .5) * .24, .05), .98) for b in base]
    smooth = [sum(base[max(0, i-3):i+4]) / len(base[max(0, i-3):i+4]) for i in range(N)]
    pts = lambda a: [(cx0 + (cx1 - cx0) * i / (N - 1), cy1 - (cy1 - cy0) * y) for i, y in enumerate(a)]
    path = lambda p: "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    length = lambda p: sum(math.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]) for i in range(len(p)-1))
    pn, ps = pts(noisy), pts(smooth)
    for gy in range(4):
        y = cy0 + (cy1 - cy0) * gy / 3
        s += f'<line x1="{cx0}" y1="{y:.1f}" x2="{cx1}" y2="{y:.1f}" stroke="{P["line"]}" stroke-dasharray="2 5"/>\n'
    s += f'<path d="{path(ps)} L{ps[-1][0]:.1f} {cy1} L{ps[0][0]:.1f} {cy1} Z" fill="url(#{u}accv)" opacity="0"><animate attributeName="opacity" values="0;.18" begin="2.6s" dur="1s" fill="freeze"/></path>\n'
    ln, ls_ = length(pn), length(ps)
    s += f'<path d="{path(pn)}" fill="none" stroke="{P["magenta"]}" stroke-width="1" opacity=".6" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"><animate attributeName="stroke-dashoffset" values="{ln:.0f};0" begin="1.1s" dur="2.2s" fill="freeze"/></path>\n'
    s += f'<path d="{path(ps)}" fill="none" stroke="{acc}" stroke-width="2.2" stroke-linejoin="round" filter="url(#{u}glow)" stroke-dasharray="{ls_:.0f}" stroke-dashoffset="{ls_:.0f}"><animate attributeName="stroke-dashoffset" values="{ls_:.0f};0" begin="1.4s" dur="2.4s" fill="freeze"/></path>\n'
    ex, ey = ps[-1]
    s += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{P["ink"]}" opacity="0" filter="url(#{u}glow)"><animate attributeName="opacity" values="0;1" begin="3.7s" dur=".3s" fill="freeze"/></circle>\n'
    s += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="9" fill="none" stroke="{acc}" opacity="0"><animate attributeName="opacity" values="0;.8;0" begin="3.8s" dur="2.4s" repeatCount="indefinite"/><animate attributeName="r" values="5;16" begin="3.8s" dur="2.4s" repeatCount="indefinite"/></circle>\n'
    s += text(cx0, cy1 + 18, "noise", 9.5, P["magenta"], "mono", ls="1.6") + text(cx1, cy1 + 18, "signal", 9.5, acc, "mono", anchor="end", ls="1.6")
    # chips
    x, inner = 66, ""
    lab = "AMOH  ·  OPERATIONS"; w = int(len(lab) * 10.5 * .66 + 24 + 50)
    inner += f'<rect x="{x}" y="356" width="{w}" height="28" rx="14" fill="{P["surface"]}" stroke="{P["violet"]}"/>' + mark(x + 14, 356 + 9.5, 9, 4) + text(x + 60, 356 + 18, lab, 10.5, P["ink"], "mono", "600", ls="1.4")
    x += w + 8
    for lab, col in [("KDAG  ·  ADVISOR", P["blue"]), ("WORLDQUANT  ·  GOLD", P["gold"]), ("CODEFORCES  ·  SPECIALIST", P["cyan"])]:
        piece, w = chip(x, 357, lab, textfill=col, h=26); inner += piece; x += w + 8
    s += reveal(inner, 1.3, .7, 8)
    s += reveal(f'<circle cx="{W-150}" cy="370" r="3.2" fill="{P["mint"]}" class="blink"/>' + text(W - 140, 374, "IST  ·  UTC+5:30", 10.5, P["muted"], "mono", ls="1.6"), 1.5)
    s += hairline(u, 0, H - 1, W)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 01 whoami
def whoami():
    u = "w"
    s, acc, nxt, H = start("whoami", u, "whoami. Industrial and Systems Engineering at IIT Kharagpur, class of 2028; operations at Amoh; advisor to the Kharagpur Data Analytics Group. You have a right to the work alone, never to its fruits.")
    s += glow_blob(u, 880, 260, 240, 120, acc, .14, "drift2")
    s += spine(u, H, acc, "01", "WHOAMI")
    lines = ["I read Industrial & Systems Engineering at IIT Kharagpur, class of 2028,",
             "and I run operations at Amoh, the medical AI research lab. The rest of my",
             "time goes where statistics meets markets: forecasting, factor research,",
             "optimisation, and the occasional 3 a.m. contest problem. Right now I am",
             "working through stochastic calculus, econometrics, and market microstructure."]
    inner = "".join(text(96, 100 + i * 21, l, 14.5, P["body"]) for i, l in enumerate(lines))
    inner += text(96, 214, "I advise the Kharagpur Data Analytics Group,", 14.5, P["ink"], "sans", "500")
    inner += text(96, 234, "having run it as Executive Head the year before.", 14.5, P["ink"], "sans", "500")
    s += reveal(inner, .3, .7, 8)
    s += reveal(f'<rect x="96" y="256" width="2" height="48" rx="1" fill="url(#{u}acc)"/>' +
                text(112, 274, "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन । मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥", 13.5, P["body"]) +
                text(112, 296, "You have a right to the work alone, never to its fruits.", 12.5, P["muted"], "sans", extra='font-style="italic"'), .8, .8, 6)
    # now card
    px, py, pw, ph = 700, 72, 244, 150
    inner = panel(px, py, pw, ph, 14, P["surface"]) + eyebrow(px + 18, py + 28, "NOW", acc)
    for i, (k, v) in enumerate([("reading", "Shreve, volume I"), ("building", "Amoh operations"), ("solving", "Codeforces, Div 2 C"), ("listening", "Sukoon")]):
        y = py + 56 + i * 24
        inner += text(px + 18, y, k, 10.5, P["muted"], "mono", ls="1.2") + text(px + 96, y, v, 12.5, P["ink"], "sans", "500")
    s += reveal(inner, .6, .8, 10)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 02 amoh
def amoh():
    u = "a"
    s, acc, nxt, H = start("amoh", u, "Building Amoh. The medical AI research lab. RL environments and data for models that do clinical work. 10+ US clinic partners.")
    s += glow_blob(u, 860, 150, 260, 150, acc, .18, "drift2")
    s += spine(u, H, acc, "02", "BUILDING")
    rnd = random.Random(3); inner = ""
    for gx in range(9):
        for gy in range(6):
            if rnd.random() < .42: continue
            c = AMOH[min(2, int(gx / 3))]; X, Y = 700 + gx * 26, 86 + gy * 26; d = .4 + rnd.random() * 1.4
            inner += (f'<rect x="{X}" y="{Y}" width="16" height="16" rx="3.5" fill="{c}" opacity="0">'
                      f'<animate attributeName="opacity" values="0;.9" begin="{d:.2f}s" dur=".5s" fill="freeze"/>'
                      f'<animate attributeName="opacity" values=".9;.35;.9" begin="{d+2:.2f}s" dur="{3+rnd.random()*4:.1f}s" repeatCount="indefinite"/></rect>')
    s += inner + "\n"
    s += reveal(mark(96, 88, 22, 9) + text(96 + 3 * 22 + 2 * 9 + 14, 106, "Amoh", 24, P["ink"], "sans", "600", ls="-0.5") + eyebrow(96, 140, "2026  ·  OPERATIONS", acc), .1)
    s += reveal(text(96, 176, "The medical AI research lab.", 30, P["ink"], "sans", "700", ls="-1.1"), .35, .7, 12)
    s += reveal(text(96, 200, "RL environments and data for models that do clinical work.", 14.5, P["body"]), .55, .7, 8)
    s += reveal(text(96, 224, "Frontier models pass medical exams and still stall on the actual work. Amoh trains them", 12, P["muted"]) +
                text(96, 240, "on hard cases from real clinics, verified against what was feasible for each patient.", 12, P["muted"]), .7, .7, 8)
    x, inner = 96, ""
    for i, lab in enumerate(["01  ENVIRONMENTS", "02  EVALS", "03  TRACES", "04  TRAINING"]):
        piece, w = chip(x, 262, lab, textfill=AMOH[2] if i == 0 else P["body"]); inner += piece; x += w + 8
    s += reveal(inner + text(x + 10, 278, "10+ US clinic partners", 11.5, P["muted"], "mono", ls="1"), .85, .6, 8)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 03 stack
def stack():
    u = "s"
    s, acc, nxt, H = start("stack", u, "Stack: Python, C++, machine learning, time series, optimisation, statistics, web, tooling")
    s += glow_blob(u, 500, 360, 460, 110, acc, .14, "drift")
    s += spine(u, H, acc, "03", "STACK")
    s += text(944, 56, "SEGMENTS = CONFIDENCE, NOT HOURS", 9.5, P["muted"], "mono", anchor="end", ls="2")
    mods = [("PYTHON", "research, modelling, most things", 9, P["cyan"]), ("C++", "contests, anything that must be fast", 7, P["blue"]),
            ("MACHINE LEARNING", "TensorFlow, scikit-learn, XGBoost", 7, P["violet"]), ("TIME SERIES", "ARIMA, Prophet, statsmodels", 7, P["purple"]),
            ("OPTIMISATION", "PuLP, dynamic and integer programming", 6, P["magenta"]), ("STATISTICS", "econometrics, stochastic calculus", 6, P["pink"]),
            ("WEB", "React, Node, Vite, Docker", 5, P["coral"]), ("TOOLING", "pandas, NumPy, Streamlit, git", 7, P["gold"])]
    cw, ch, gx, gy = 204, 112, 10, 12
    for i, (name, sub, lvl, col) in enumerate(mods):
        c, r = i % 4, i // 4
        x, y = 96 + c * (cw + gx) - 8, 84 + r * (ch + gy)
        inner = panel(x, y, cw, ch, 12, P["surface"]) + f'<rect x="{x}" y="{y+18}" width="2" height="{ch-36}" rx="1" fill="{col}" opacity=".9"/>'
        inner += text(x + 16, y + 26, f"{i+1:02d}", 10, P["muted"], "mono", ls="1.5")
        inner += text(x + 16, y + 50, name, 13, P["ink"], "mono", "700", ls="1.2") + text(x + 16, y + 68, sub, 10.5, P["muted"], "sans")
        for k in range(10):
            on = k < lvl; sx = x + 16 + k * 17.4
            inner += (f'<rect x="{sx:.1f}" y="{y+84}" width="12.5" height="6" rx="2" fill="{col if on else P["line"]}" opacity="{0 if on else 1}">'
                      + (f'<animate attributeName="opacity" values="0;1" begin="{.6+i*.08+k*.05:.2f}s" dur=".3s" fill="freeze"/>' if on else "") + '</rect>')
        s += reveal(inner, .15 + i * .09, .6, 10)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 04 timeline
def timeline():
    u = "t"
    s, acc, nxt, H = start("timeline", u, "Timeline: Seventh Triangle and Myntra in 2024, PharmEasy in 2025, KDAG Executive Head, Amoh Operations and KDAG Advisor in 2026, L.E.K. Consulting incoming in 2027")
    s += glow_blob(u, 640, 190, 260, 120, acc, .14, "drift")
    s += spine(u, H, acc, "04", "TRACK RECORD")
    nodes = [("JUL 2024", "Seventh Triangle", "R&D Intern", "four months, applied research", "past"),
             ("SEP 2024", "Myntra", "Strategy Intern", "brand launch, go to market", "past"),
             ("MAY 2025", "PharmEasy", "Summer Intern", "ten weeks, Bangalore", "past"),
             ("2025-26", "KDAG", "Executive Head", "curriculum, projects, inductions", "past"),
             ("2026", "Amoh", "Operations", "the medical AI research lab", "now"),
             ("2026-27", "KDAG", "Advisor", "steering the group", "now"),
             ("2027", "L.E.K. Consulting", "Summer Associate", "incoming", "next")]
    y0, x0, x1 = 200, 100, 940
    s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{P["line"]}" stroke-width="2"/>\n'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="url(#{u}spec)" stroke-width="2" stroke-dasharray="{x1-x0}" stroke-dashoffset="{x1-x0}"><animate attributeName="stroke-dashoffset" values="{x1-x0};0" begin=".3s" dur="2s" fill="freeze"/></line>\n'
    n = len(nodes)
    for i, (when, who, role, sub, state) in enumerate(nodes):
        x = x0 + 30 + i * (x1 - x0 - 60) / (n - 1); up = i % 2 == 0
        ty = y0 - 42 if up else y0 + 48; b = .55 + i * .22
        col = acc if state == "now" else (P["gold"] if state == "next" else P["muted"])
        inner = f'<line x1="{x:.0f}" y1="{y0 + (-12 if up else 12)}" x2="{x:.0f}" y2="{ty + (6 if up else -34)}" stroke="{P["line"]}"/>'
        if up:
            inner += eyebrow(x, ty - 44, when, col, "middle") + text(x, ty - 22, who, 16, P["ink"], "sans", "700", "middle", "-.4")
            inner += text(x, ty - 5, role, 12, P["body"], "sans", anchor="middle") + text(x, ty + 10, sub, 10.5, P["muted"], "sans", anchor="middle")
        else:
            inner += eyebrow(x, ty - 14, when, col, "middle") + text(x, ty + 8, who, 16, P["ink"], "sans", "700", "middle", "-.4")
            inner += text(x, ty + 25, role, 12, P["body"], "sans", anchor="middle") + text(x, ty + 40, sub, 10.5, P["muted"], "sans", anchor="middle")
        s += reveal(inner, b, .5, 6)
        dash = ' stroke-dasharray="3 3"' if state == "next" else ""
        s += f'<circle cx="{x:.0f}" cy="{y0}" r="7" fill="{P["ground"]}" stroke="{col}" stroke-width="2.2"{dash} opacity="0"><animate attributeName="opacity" values="0;1" begin="{b-.15:.2f}s" dur=".3s" fill="freeze"/></circle>\n'
        if state == "now":
            s += (f'<circle cx="{x:.0f}" cy="{y0}" r="7" fill="none" stroke="{acc}" opacity="0"><animate attributeName="r" values="7;22" begin="{b+.5:.2f}s" dur="2.4s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values=".9;0" begin="{b+.5:.2f}s" dur="2.4s" repeatCount="indefinite"/></circle>\n'
                  f'<circle cx="{x:.0f}" cy="{y0}" r="3" fill="{acc}" filter="url(#{u}glow)"/>\n')
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 06 positions
def positions():
    u = "p"
    s, acc, nxt, H = start("positions", u, "A tongue in cheek blotter: long Amoh, long stochastic calculus, long the Codeforces grind, short 8 a.m. lectures")
    s += glow_blob(u, 880, 330, 240, 120, acc, .12, "drift2")
    s += spine(u, H, acc, "06", "POSITIONS")
    s += text(944, 56, "MARKED TO MARKET  ·  NOT INVESTMENT ADVICE", 9.5, P["muted"], "mono", anchor="end", ls="2")
    rows = [("LONG", "Amoh", "position size: all in", "▲  open", True), ("LONG", "Stochastic calculus", "Shreve, volume I, second read", "▲  +412.6%", True),
            ("LONG", "The Codeforces grind", "rating goes up, eventually", "▲  +128.4%", True), ("LONG", "Chai at 2 a.m.", "the only reliable alpha", "▲  +96.2%", True),
            ("LONG", "K-pop during backtests", "inexplicable, but it works", "▲  +64.8%", True), ("SHORT", "8 a.m. lectures", "structurally impaired", "▼  -71.3%", False),
            ("SHORT", "Notebook outputs in git", "most of my repos, regrettably", "▼  -44.9%", False), ("SHORT", "Sleep, in exam week", "liquidated early", "▼  -88.1%", False)]
    s += text(96, 92, "SIDE", 9.5, P["muted"], "mono", ls="2") + text(190, 92, "POSITION", 9.5, P["muted"], "mono", ls="2") + text(944, 92, "P&L", 9.5, P["muted"], "mono", anchor="end", ls="2")
    s += f'<line x1="96" y1="102" x2="944" y2="102" stroke="{P["line"]}"/>\n'
    for i, (side, pos, sub, pnl, long) in enumerate(rows):
        y = 128 + i * 30; col = P["mint"] if long else P["coral"]
        inner = f'<rect x="96" y="{y-15}" width="60" height="20" rx="10" fill="{P["surface"]}" stroke="{col}" stroke-opacity=".6"/>'
        inner += text(126, y - 1, side, 9.5, col, "mono", "700", "middle", "1.5") + text(190, y, pos, 14, P["ink"], "sans", "600")
        inner += text(190 + len(pos) * 7.6 + 14, y, sub, 11, P["muted"], "sans") + text(944, y, pnl, 13, col, "mono", "600", "end")
        inner += f'<line x1="96" y1="{y+10}" x2="944" y2="{y+10}" stroke="{P["line"]}" opacity=".7"/>'
        s += reveal(inner, .2 + i * .1, .5, 6)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 07 day
def day():
    u = "d"
    s, acc, nxt, H = start("dayinthelife", u, "A twenty four hour ring of a typical day: late Codeforces, six hours of sleep, lectures, Amoh and KDAG in the afternoon, research at night")
    s += glow_blob(u, 250, 200, 170, 170, acc, .16, "drift2")
    s += spine(u, H, acc, "07", "A DAY AT THE DESK")
    s += text(944, 56, "IST  ·  SUBJECT TO DEADLINES", 9.5, P["muted"], "mono", anchor="end", ls="2")
    segs = [("00:00", "Codeforces, late problems", 2, P["cyan"]), ("02:00", "Sleep, allegedly", 6, P["line"]), ("08:00", "Lectures and labs", 5, P["violet"]),
            ("13:00", "Mess, chai, walking", 1, P["magenta"]), ("14:00", "Amoh, KDAG, projects", 3, P["pink"]), ("17:00", "Gym, music, offline", 2, P["orange"]),
            ("19:00", "Research and backtests", 5, P["gold"])]
    cx, cy, R, sw = 250, 198, 92, 20; C = 2 * math.pi * R; st = 0
    for i, (t, lab, h, col) in enumerate(segs):
        L = C * h / 24
        s += (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="0 {C:.1f}" stroke-dashoffset="{-st:.1f}" transform="rotate(-90 {cx} {cy})" opacity=".92">'
              f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};{L-2.5:.1f} {C-L+2.5:.1f}" begin="{.3+i*.18:.2f}s" dur=".7s" fill="freeze"/></circle>\n')
        st += L
    s += f'<circle cx="{cx}" cy="{cy}" r="{R-sw/2-6}" fill="none" stroke="{P["line"]}" stroke-dasharray="2 6"/>\n'
    for k, lab in [(0, "00"), (6, "06"), (12, "12"), (18, "18")]:
        a = math.radians(k * 15 - 90)
        s += text(cx + math.cos(a) * (R - sw / 2 - 20), cy + math.sin(a) * (R - sw / 2 - 20) + 3.5, lab, 9.5, P["muted"], "mono", anchor="middle", ls="1")
    s += text(cx, cy + 6, "24h", 16, P["ink"], "sans", "700", "middle", "-.5")
    for i, (t, lab, h, col) in enumerate(segs):
        y = 100 + i * 30
        inner = f'<rect x="420" y="{y-10}" width="10" height="10" rx="2.5" fill="{col}"/>' + text(442, y, t, 11, P["muted"], "mono", ls="1")
        inner += text(500, y, lab, 13.5, P["ink"], "sans", "500") + text(944, y, f"{h}h", 12, P["body"], "mono", anchor="end")
        inner += f'<line x1="420" y1="{y+10}" x2="944" y2="{y+10}" stroke="{P["line"]}" opacity=".7"/>'
        s += reveal(inner, .3 + i * .12, .5, 6)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 09 music
def music():
    u = "m"
    s, acc, nxt, H = start("music", u, "Frequencies: Sukoon, Calm Synths, K-pop, EDM")
    s += spine(u, H, acc, "09", "FREQUENCIES")
    s += text(944, 56, "APPLE MUSIC  ·  NOW PLAYING", 9.5, P["muted"], "mono", anchor="end", ls="2")
    rnd = random.Random(11); cw = 204
    for i, (name, sub, col) in enumerate([("Sukoon", "the late-desk playlist", P["mint"]), ("Calm Synths", "for long proofs and longer backtests", P["cyan"]), ("K-pop", "non negotiable", P["magenta"]), ("EDM", "contest mode", P["gold"])]):
        x, y = 88 + i * (cw + 10), 80
        inner = panel(x, y, cw, 110, 12, P["surface"]); bx0, by = x + 16, y + 56
        for k in range(13):
            h1, h2 = 4 + rnd.random() * 10, 10 + rnd.random() * 26; bx = bx0 + k * 13.2; d = .9 + rnd.random() * 1.4
            inner += (f'<rect x="{bx:.1f}" y="{by-h1:.1f}" width="7" height="{h1:.1f}" rx="2" fill="{col}" opacity="{.9 if k % 3 else .55}">'
                      f'<animate attributeName="height" values="{h1:.1f};{h2:.1f};{h1:.1f}" dur="{d:.2f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="y" values="{by-h1:.1f};{by-h2:.1f};{by-h1:.1f}" dur="{d:.2f}s" repeatCount="indefinite"/></rect>')
        inner += text(x + 16, y + 82, name, 14.5, P["ink"], "sans", "600", ls="-.3") + text(x + 16, y + 98, sub, 10.5, P["muted"], "sans")
        s += reveal(inner, .15 + i * .12, .6, 8)
    return s + close_svg(W, H)

# ---------------------------------------------------------------- 10 contributions strip
def contributions():
    u = "c"
    s, acc, nxt, H = start("contributions", u, "Contributions. A year of commits, eaten by a snake.")
    s += spine(u, H, acc, "10", "CONTRIBUTIONS")
    s += text(944, 56, "A YEAR OF COMMITS, EATEN BY A SNAKE", 9.5, P["muted"], "mono", anchor="end", ls="2")
    return s + close_svg(W, H)

# ---------------------------------------------------------------- footer
def footer():
    u = "f"
    s, acc, nxt, H = start("footer", u, "The market closes. Curiosity does not.")
    s += glow_blob(u, 500, 170, 320, 70, acc, .16, "drift")
    s += f'<rect x="{SPINE_X-1}" y="0" width="2" height="60" fill="url(#{u}spine)" opacity=".55"/>'
    s += f'<circle cx="{SPINE_X}" cy="64" r="3.5" fill="{acc}" filter="url(#{u}glow)"/>\n'
    s += hairline(u, 300, 50, 400)
    s += reveal(text(500, 92, "the market closes. curiosity doesn't.", 22, f"url(#{u}spec)", "sans", "600", "middle", "-.5", 'font-style="italic"'), .2, .9, 8)
    s += reveal(text(470, 124, "SESSION PERSISTS", 10.5, P["muted"], "mono", anchor="end", ls="2") + f'<circle cx="486" cy="120" r="3.2" fill="{P["mint"]}" class="blink"/>' +
                text(500, 124, "KOLKATA, IN", 10.5, P["muted"], "mono", ls="2"), .6)
    return s + close_svg(W, H)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(PREV, exist_ok=True)
    parts = dict(header=header(), whoami=whoami(), amoh=amoh(), stack=stack(), timeline=timeline(), positions=positions(),
                 dayinthelife=day(), music=music(), contributions=contributions(), footer=footer())
    for k, v in parts.items():
        open(os.path.join(OUT, k + ".svg"), "w").write(v); open(os.path.join(PREV, "p-" + k + ".svg"), "w").write(v)
        print("wrote", k, len(v))
