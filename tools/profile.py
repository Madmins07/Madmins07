import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from layout import H
from repos import PROFILE
OUT = os.path.join(PROFILE["path"], "assets")
PREV = os.environ.get("PREVIEW_DIR", "/tmp/madmins07-preview")

def header():
    u, h = "h", H["header"]
    s = open_svg(W, h, "Madhav Agarwal. Operations at Amoh, the medical AI research lab. Industrial and Systems Engineering, IIT Kharagpur, class of 2028. Kolkata.", u)
    s += section(u, h, "00", "MADHAV AGARWAL", "IIT KHARAGPUR '28  ·  KOLKATA  ·  IST")
    s += reveal(text(LEFT, 168, "Madhav Agarwal", 76, P["ink"], "sans", "800", ls="-3.4"), .2, .8, 14)
    s += grow(LEFT, 186, 56, 3, P["accent"], .7, 0, .6)
    s += reveal(text(LEFT, 228, "Operations at Amoh. Quant research, time series, optimisation.", 19, P["body"], "sans", "500", ls="-.3"), .5, .7, 10)
    s += reveal(text(LEFT, 258, "Building the infrastructure that lets models do real clinical work.", 13.5, P["muted"]) +
                text(LEFT, 278, "Reading stochastic calculus on the side.", 13.5, P["muted"]), .8, .7, 8)
    facts = [("AMOH", "Operations"), ("KDAG", "Advisor"), ("WORLDQUANT", "Challenge, Gold"), ("CODEFORCES", "Specialist")]
    fx = 700
    for i, (k, v) in enumerate(facts):
        y = 118 + i * 40
        s += reveal(label(fx, y, k) + text(RIGHT, y, v, 14, P["ink"], "sans", "600", "end") + hline(fx, RIGHT, y + 14), .4 + i * .1)
    s += reveal(f'<rect x="{LEFT}" y="{h-46}" width="6" height="6" fill="{P["accent"]}" class="blink"/>' + label(LEFT + 16, h - 40, "OPEN TO HARD PROBLEMS  ·  MADHAVAGARWAL50@GMAIL.COM", P["muted"]), 1.1)
    return s + close_svg(W, h)

def whoami():
    u, h = "w", H["whoami"]
    s = open_svg(W, h, "whoami, as a terminal session. Madhav Agarwal, Industrial and Systems Engineering at IIT Kharagpur, class of 2028; operations at Amoh; advisor to the Kharagpur Data Analytics Group. Interests: forecasting, factor research, optimisation, stochastic calculus. Now: reading Shreve, building Amoh operations, solving Codeforces Div 2 C. You have a right to the work alone, never to its fruits.", u)
    s += section(u, h, "01", "WHOAMI", "ZSH  ·  PLAYS ONCE, THEN HOLDS")
    tx, ty, tw, th = LEFT, 90, RIGHT - LEFT, h - 110
    s += f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="{P["surface"]}" stroke="{P["line"]}"/>'
    s += f'<rect x="{tx}" y="{ty}" width="{tw}" height="26" fill="{P["surface2"]}"/>'
    for i, c in enumerate((P["faint"], P["faint"], P["faint"])): s += f'<circle cx="{tx+16+i*16}" cy="{ty+13}" r="4.5" fill="{c}"/>'
    s += text(tx + tw / 2, ty + 17, "madhav@kgp — zsh — 110×24", 10.5, P["muted"], "mono", anchor="middle")
    cw, lh, fs = 7.45, 17, 12.4   # mono advance at 12.4px, line height
    lines = [("cmd", "whoami"), ("out", "Madhav Agarwal  ·  ISE '28, IIT Kharagpur  ·  operations @ Amoh  ·  advisor @ KDAG"),
             ("cmd", "cat ~/interests"), ("out", "forecasting · factor research · optimisation · stochastic calculus · 3 a.m. contest problems"),
             ("cmd", "cat ~/now"), ("out", "reading    Shreve, Stochastic Calculus for Finance I"), ("out", "building   Amoh operations"), ("out", "solving    Codeforces, Div 2 C"),
             ("cmd", "fortune --gita 2.47"), ("out", "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।  you have a right to the work alone, never to its fruits."),
             ("cmd", "")]
    t = .6; y = ty + 48; prompt = "madhav@kgp ~ % "; pw = len(prompt) * cw
    for i, (kind, body) in enumerate(lines):
        if kind == "cmd":
            s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>' + text(tx + 16, y, prompt, fs, P["accent"], "mono", "600") + "</g>"
            if body:
                dur = max(.3, len(body) * .055); cwid = len(body) * cw
                s += (f'<clipPath id="{u}c{i}"><rect x="{tx+16+pw:.1f}" y="{y-13}" width="0" height="18"><animate attributeName="width" begin="{t+.15:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" keyTimes="' + ";".join(f"{k/len(body):.3f}" for k in range(len(body)+1)) + '" values="' + ";".join(f"{k*cw:.1f}" for k in range(len(body)+1)) + '"/></rect></clipPath>')
                s += f'<g clip-path="url(#{u}c{i})">' + text(tx + 16 + pw, y, body, fs, P["ink"], "mono") + "</g>"
                t += .15 + dur + .25
            else:
                s += f'<rect x="{tx+16+pw:.1f}" y="{y-12}" width="{cw:.1f}" height="15" fill="{P["ink"]}" opacity="0"><set attributeName="opacity" to="1" begin="{t+.1:.2f}s" fill="freeze"/><animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{t+.1:.2f}s" repeatCount="indefinite" calcMode="discrete"/></rect>'
        else:
            s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>' + text(tx + 16, y, body, fs, P["body"], "mono") + "</g>"
            t += .12
        y += lh
    return s + close_svg(W, h)

def amoh():
    u, h = "a", H["amoh"]
    s = open_svg(W, h, "Building Amoh. The medical AI research lab. RL environments and data for models that do clinical work. 10+ US clinic partners.", u)
    s += section(u, h, "02", "BUILDING", "AMOH.AI  ·  2026")
    s += reveal(mark(LEFT, 98, 20, 8) + text(LEFT + 3 * 20 + 2 * 8 + 12, 115, "Amoh", 22, P["ink"], "sans", "600", ls="-.5"), .2)
    s += reveal(text(LEFT, 158, "The medical AI research lab.", 30, P["ink"], "sans", "700", ls="-1.1"), .4, .7, 10)
    s += reveal(text(LEFT, 182, "RL environments and data for models that do clinical work.", 14, P["body"]), .55)
    s += reveal(text(LEFT, 206, "Frontier models pass medical exams and still stall on the actual work. Amoh trains them on hard", 12, P["muted"]) +
                text(LEFT, 222, "cases from real clinics, verified against what was feasible for each patient. I run operations.", 12, P["muted"]), .7)
    offers = [("01", "Environments"), ("02", "Evals and benchmarks"), ("03", "Feedback and traces"), ("04", "Training for health systems")]
    for i, (n, t) in enumerate(offers):
        y = 106 + i * 30
        s += reveal(text(700, y, n, 10, P["accent"], "mono", "700", ls="2") + text(730, y, t, 12.5, P["ink"], "sans", "500") + hline(700, RIGHT, y + 11), .5 + i * .08)
    s += reveal(label(700, 238, "10+ US CLINIC PARTNERS", P["muted"]), .9)
    return s + close_svg(W, h)

def stack():
    u, h = "s", H["stack"]
    s = open_svg(W, h, "Stack: Python, C++, machine learning, time series, optimisation, statistics, web, tooling. Icons orbit: Python, C++, Jupyter, TensorFlow, scikit-learn, pandas, NumPy, React, Node, Docker, Streamlit, git, Plotly.", u)
    s += section(u, h, "03", "STACK", "ORBITS BY DISTANCE FROM DAILY USE  ·  DOTS = DEPTH")
    cx, cy = 250, 246
    rings = [(58, 70, ["python", "cplusplus", "jupyter"]), (104, 110, ["tensorflow", "scikitlearn", "pandas", "numpy"]), (148, 160, ["react", "nodedotjs", "docker", "streamlit", "git", "plotly"])]
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="{P["ground"]}" stroke="{P["accent"]}" stroke-width="1.5"/><circle cx="{cx}" cy="{cy}" r="4" fill="{P["accent"]}"/>'
    for ri, (r, dur, slugs) in enumerate(rings):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["line2"]}" stroke-dasharray="2 5"/>'
        direction = -1 if ri % 2 else 1
        s += f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360*direction} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
        for k, slug in enumerate(slugs):
            a = 2 * math.pi * k / len(slugs); ix, iy = cx + r * math.cos(a), cy + r * math.sin(a)
            fill = P["ink"] if ri == 0 else (P["body"] if ri == 1 else P["muted"]); sz = 20 if ri == 0 else 17
            s += (f'<g transform="translate({ix:.1f},{iy:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{-360*direction}" dur="{dur}s" repeatCount="indefinite"/>'
                  f'<circle r="{sz/2+7}" fill="{P["ground"]}" stroke="{P["line"]}"/><path d="{icon_path(slug)}" fill="{fill}" transform="translate({-sz/2:.1f},{-sz/2:.1f}) scale({sz/24:.3f})"/></g></g>')
        s += "</g>\n"
    mods = [("PYTHON", "research, modelling, most things", 5), ("C++", "contests, anything that must be fast", 4),
            ("MACHINE LEARNING", "TensorFlow, scikit-learn, XGBoost", 4), ("TIME SERIES", "ARIMA, Prophet, statsmodels", 4),
            ("OPTIMISATION", "PuLP, dynamic and integer programming", 3), ("STATISTICS", "econometrics, stochastic calculus", 3),
            ("WEB", "React, Node, Vite, Docker", 2), ("TOOLING", "pandas, NumPy, Streamlit, git", 4)]
    for i, (name, sub, lvl) in enumerate(mods):
        col, row = i % 2, i // 2
        x, y = 470 + col * 240, 122 + row * 66
        inner = text(x, y, name, 11.5, P["ink"], "mono", "700", ls="1.4") + text(x, y + 16, sub, 10, P["muted"], "sans")
        for k in range(5):
            dx = x + 150 + k * 15
            inner += f'<rect x="{dx}" y="{y-8}" width="9" height="9" fill="{P["accent"] if k < lvl else "none"}" stroke="{P["accent"] if k < lvl else P["line2"]}"/>'
        inner += hline(x, x + 224, y + 28)
        s += reveal(inner, .2 + i * .07)
    return s + close_svg(W, h)

def timeline():
    u, h = "t", H["timeline"]
    s = open_svg(W, h, "Timeline: Seventh Triangle and Myntra in 2024, PharmEasy in 2025, KDAG Executive Head, Amoh Operations and KDAG Advisor in 2026, L.E.K. Consulting incoming in 2027", u)
    s += section(u, h, "04", "TRACK RECORD", "2024  →  2027")
    nodes = [("JUL 2024", "Seventh Triangle", "R&D Intern", "past"), ("SEP 2024", "Myntra", "Strategy Intern", "past"),
             ("MAY 2025", "PharmEasy", "Summer Intern", "past"), ("2025-26", "KDAG", "Executive Head", "past"),
             ("2026", "Amoh", "Operations", "now"), ("2026-27", "KDAG", "Advisor", "now"), ("2027", "L.E.K. Consulting", "Summer Associate", "next")]
    y0, x0, x1 = 190, LEFT + 20, RIGHT - 20
    s += hline(x0, x1, y0, P["line2"])
    s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{P["accent"]}" stroke-width="1.5" stroke-dasharray="{x1-x0}" stroke-dashoffset="{x1-x0}"><animate attributeName="stroke-dashoffset" values="{x1-x0};0" begin=".3s" dur="1.6s" fill="freeze"/></line>\n'
    n = len(nodes)
    for i, (when, who, role, state) in enumerate(nodes):
        x = x0 + i * (x1 - x0) / (n - 1); up = i % 2 == 0; b = .5 + i * .18
        col = P["accent"] if state != "past" else P["muted"]
        if up:
            inner = label(x, y0 - 58, when, col, "middle") + text(x, y0 - 38, who, 14.5, P["ink"], "sans", "700", "middle", "-.3") + text(x, y0 - 22, role, 11, P["body"], "sans", anchor="middle")
            inner += f'<line x1="{x:.0f}" y1="{y0-14}" x2="{x:.0f}" y2="{y0-6}" stroke="{P["line2"]}"/>'
        else:
            inner = label(x, y0 + 34, when, col, "middle") + text(x, y0 + 54, who, 14.5, P["ink"], "sans", "700", "middle", "-.3") + text(x, y0 + 70, role, 11, P["body"], "sans", anchor="middle")
            inner += f'<line x1="{x:.0f}" y1="{y0+6}" x2="{x:.0f}" y2="{y0+14}" stroke="{P["line2"]}"/>'
        s += reveal(inner, b, .5, 6)
        dash = ' stroke-dasharray="2 2"' if state == "next" else ""
        fill = P["accent"] if state == "now" else P["ground"]
        s += f'<rect x="{x-5:.0f}" y="{y0-5}" width="10" height="10" fill="{fill}" stroke="{col}" stroke-width="1.5"{dash} opacity="0"><animate attributeName="opacity" values="0;1" begin="{b-.1:.2f}s" dur=".3s" fill="freeze"/></rect>\n'
    return s + close_svg(W, h)

def day():
    u, h = "d", H["dayinthelife"]
    s = open_svg(W, h, "A twenty four hour ring of a typical day: late Codeforces, six hours of sleep, lectures, Amoh and KDAG in the afternoon, research at night", u)
    s += section(u, h, "08", "A DAY AT THE DESK", "IST  ·  SUBJECT TO DEADLINES")
    segs = [("00:00", "Codeforces, late problems", 2, P["accent"], .55), ("02:00", "Sleep, allegedly", 6, P["faint"], 1), ("08:00", "Lectures and labs", 5, P["muted"], .5),
            ("13:00", "Mess, chai, walking", 1, P["muted"], .8), ("14:00", "Amoh, KDAG, projects", 3, P["accent"], .8), ("17:00", "Gym, music, offline", 2, P["muted"], .35),
            ("19:00", "Research and backtests", 5, P["accent"], 1)]
    cx, cy, R, sw = 230, 188, 78, 18; C = 2 * math.pi * R; st = 0
    for i, (t, lab, hrs, col, op) in enumerate(segs):
        L = C * hrs / 24
        s += (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}" stroke-dasharray="0 {C:.1f}" stroke-dashoffset="{-st:.1f}" transform="rotate(-90 {cx} {cy})">'
              f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};{L-2:.1f} {C-L+2:.1f}" begin="{.3+i*.15:.2f}s" dur=".6s" fill="freeze"/></circle>\n')
        st += L
    for k, lab in [(0, "00"), (6, "06"), (12, "12"), (18, "18")]:
        a = math.radians(k * 15 - 90)
        s += text(cx + math.cos(a) * (R - sw / 2 - 16), cy + math.sin(a) * (R - sw / 2 - 16) + 3.5, lab, 9, P["muted"], "mono", anchor="middle", ls="1")
    s += text(cx, cy + 6, "24h", 15, P["ink"], "sans", "700", "middle", "-.5")
    for i, (t, lab, hrs, col, op) in enumerate(segs):
        y = 108 + i * 27
        inner = f'<rect x="400" y="{y-9}" width="9" height="9" fill="{col}" fill-opacity="{op}"/>' + text(420, y, t, 10.5, P["muted"], "mono", ls="1")
        inner += text(476, y, lab, 13, P["ink"], "sans", "500") + text(RIGHT, y, f"{hrs}h", 11.5, P["body"], "mono", anchor="end") + hline(400, RIGHT, y + 9, P["line"], .8)
        s += reveal(inner, .3 + i * .1, .5, 6)
    return s + close_svg(W, h)

def positions():
    u, h = "p", H["positions"]
    s = open_svg(W, h, "A tongue in cheek blotter: long Amoh, long stochastic calculus, long the Codeforces grind, short 8 a.m. lectures", u)
    s += section(u, h, "09", "POSITIONS", "MARKED TO MARKET  ·  NOT INVESTMENT ADVICE")
    rows = [("LONG", "Amoh", "position size: all in", "open", True), ("LONG", "Stochastic calculus", "Shreve, volume I, second read", "+412.6%", True),
            ("LONG", "The Codeforces grind", "rating goes up, eventually", "+128.4%", True), ("LONG", "Chai at 2 a.m.", "the only reliable alpha", "+96.2%", True),
            ("LONG", "K-pop during backtests", "inexplicable, but it works", "+64.8%", True), ("SHORT", "8 a.m. lectures", "structurally impaired", "-71.3%", False),
            ("SHORT", "Notebook outputs in git", "most of my repos, regrettably", "-44.9%", False), ("SHORT", "Sleep, in exam week", "liquidated early", "-88.1%", False)]
    s += label(LEFT, 96, "SIDE") + label(LEFT + 90, 96, "POSITION") + label(RIGHT, 96, "P&L", anchor="end")
    for i, (side, pos, sub, pnl, long) in enumerate(rows):
        y = 124 + i * 25; col = P["accent"] if long else P["muted"]
        inner = text(LEFT, y, side, 10, col, "mono", "700", ls="1.6") + text(LEFT + 90, y, pos, 13.5, P["ink"], "sans", "600")
        inner += text(LEFT + 90 + len(pos) * 7.4 + 12, y, sub, 11, P["muted"], "sans") + text(RIGHT, y, ("▲ " if long else "▼ ") + pnl, 12, col, "mono", "600", "end")
        inner += hline(LEFT, RIGHT, y + 8, P["line"], .8)
        s += reveal(inner, .2 + i * .08, .45, 5)
    return s + close_svg(W, h)

def footer():
    u, h = "f", H["footer"]
    s = open_svg(W, h, "The market closes. Curiosity does not.", u)
    s += f'<rect x="{RAIL-.5}" y="0" width="1" height="54" fill="{P["line2"]}"/><rect x="{RAIL-4}" y="50" width="8" height="8" fill="{P["accent"]}"/>\n'
    s += reveal(text(LEFT, 60, "the market closes. curiosity doesn't.", 20, P["ink"], "sans", "600", ls="-.5", extra='font-style="italic"'), .2, .7)
    s += reveal(label(LEFT, 96, "SESSION PERSISTS  ·  KOLKATA, IN") + label(RIGHT, 96, "MADMINS07  ·  PANELS RENDER NIGHTLY", anchor="end"), .5)
    return s + close_svg(W, h)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(PREV, exist_ok=True)
    parts = dict(header=header(), whoami=whoami(), amoh=amoh(), stack=stack(), timeline=timeline(), dayinthelife=day(), positions=positions(), footer=footer())
    for k, v in parts.items():
        open(os.path.join(OUT, k + ".svg"), "w").write(v); open(os.path.join(PREV, "p-" + k + ".svg"), "w").write(v); print("wrote", k, len(v))
    for stale in ["music.svg", "contributions.svg", "metrics.svg", "projects.svg"]:
        p = os.path.join(OUT, stale)
        if os.path.exists(p): os.remove(p); print("removed", stale)
