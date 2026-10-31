"""Page order, heights and accents. Each panel's ground is a slice of one long gradient, and its spine
runs from its own accent into the next panel's accent, so stacked panels read as one continuous surface."""
from common import P, mix

GROUND_STOPS = [(0.0, "#07080D"), (0.22, "#0A0A1A"), (0.46, "#120915"), (0.70, "#120D0A"), (0.88, "#071210"), (1.0, "#07080D")]
SECTIONS = [  # (key, height, accent)
    ("header", 440, P["cyan"]), ("whoami", 330, P["blue"]), ("amoh", 300, P["violet"]), ("stack", 340, P["purple"]),
    ("timeline", 340, P["magenta"]), ("projects", 380, P["pink"]), ("positions", 360, P["coral"]),
    ("dayinthelife", 330, P["orange"]), ("metrics", 320, P["gold"]), ("music", 210, P["mint"]),
    ("contributions", 90, P["cyan"]), ("footer", 160, P["cyan"]),
]
SELECTED = ["cgpa_simulator", "OR2", "Time-series-models", "Competitive-Programming", "KDAG_Core_Tasks", "Quantitative-Finance"]
TOTAL = sum(h for _, h, _ in SECTIONS)

def ground_at(t):
    for (t0, c0), (t1, c1) in zip(GROUND_STOPS, GROUND_STOPS[1:]):
        if t <= t1: return mix(c0, c1, (t - t0) / (t1 - t0))
    return GROUND_STOPS[-1][1]

def slice_for(key):
    """(top colour, bottom colour, accent, next accent) for a panel."""
    y = 0
    for i, (k, h, a) in enumerate(SECTIONS):
        if k == key:
            nxt = SECTIONS[i + 1][2] if i + 1 < len(SECTIONS) else a
            return ground_at(y / TOTAL), ground_at((y + h) / TOTAL), a, nxt, h
        y += h
    raise KeyError(key)
