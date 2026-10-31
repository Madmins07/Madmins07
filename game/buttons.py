"""Static column buttons and the bot button, rendered once."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from common import *
out = os.path.join(ROOT, "assets", "game"); os.makedirs(out, exist_ok=True)
for c in range(1, 8):
    s = (f'<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="drop in column {c}">'
         f'<rect x=".5" y=".5" width="39" height="39" fill="{P["surface"]}" stroke="{P["line2"]}"/>'
         f'<text x="20" y="25" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{P["accent"]}">{c}</text></svg>')
    open(os.path.join(out, f"col-{c}.svg"), "w").write(s)
s = (f'<svg width="96" height="40" viewBox="0 0 96 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="let the bot move for you">'
     f'<rect x=".5" y=".5" width="95" height="39" fill="{P["surface"]}" stroke="{P["line2"]}"/>'
     f'<text x="48" y="24.5" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="2" fill="{P["accent2"]}">BOT MOVES</text></svg>')
open(os.path.join(out, "bot.svg"), "w").write(s); print("buttons written")
