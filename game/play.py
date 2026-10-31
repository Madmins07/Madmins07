#!/usr/bin/env python3
"""Handle one Connect Four move from an issue title. Reads ISSUE_TITLE, ISSUE_USER, ISSUE_NUMBER from env.
Exit 0 = played, 2 = rejected (stale board, bad title, not allowed), else crash. Prints the reply markdown."""
import os, sys, re, json, hashlib, glob, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "tools"))
import engine as E
from common import *
COLS, ROWS = E.COLS, E.ROWS

OWNER = "Madmins07"
STATE = os.path.join(HERE, "state.json")
BOARD_DIR = os.path.join(ROOT, "assets", "board")
README = os.path.join(ROOT, "README.md")
DEPTH = 7

def load():
    if os.path.exists(STATE): return json.load(open(STATE))
    return dict(game=1, human=0, bot=0, mask=0, move=0, over=None, history=[], players={}, games=0, human_wins=0, bot_wins=0, draws=0, last=None)

def save(S): json.dump(S, open(STATE, "w"), indent=1)

def reject(msg):
    print(msg); sys.exit(2)

def new_game(S):
    S.update(human=0, bot=0, mask=0, move=0, over=None, history=[], game=S["game"] + (1 if S["games"] else 0))

def render(S):
    """Board panel in the house style. Returns the relative path of the new SVG."""
    u, Hh = "g", 420
    status = {"human": "YOU WON. THE BOT IS RETHINKING ITS LIFE.", "bot": "THE BOT WON. AGAIN.", "draw": "DRAW. BOARD FULL."}.get(S["over"], "YOUR MOVE. PICK A COLUMN BELOW.")
    s = open_svg(W, Hh, f"Connect Four against a minimax bot. Game {S['game']}, move {S['move']}. {status.title()}", u)
    s += section(u, Hh, "10", "CONNECT FOUR  ·  VS THE BOT", f"GAME {S['game']:03d}  ·  MOVE {S['move']:02d}  ·  {status}")
    # board
    cell, pad = 44, 6; bx, by = LEFT, 104
    bw, bh = COLS * cell, ROWS * cell
    s += f'<rect x="{bx-pad}" y="{by-pad}" width="{bw+2*pad}" height="{bh+2*pad}" fill="{P["surface"]}" stroke="{P["line"]}"/>\n'
    human, bot = E.cells(S["human"]), E.cells(S["bot"])
    line = E.win_line(S["human"]) if S["over"] == "human" else (E.win_line(S["bot"]) if S["over"] == "bot" else None)
    for c in range(COLS):
        s += text(bx + c * cell + cell / 2, by - 14, str(c + 1), 10, P["muted"], "mono", anchor="middle", ls="1")
        for r in range(ROWS):
            cx, cy = bx + c * cell + cell / 2, by + (ROWS - 1 - r) * cell + cell / 2
            if (c, r) in human: fill, stroke = P["accent"], P["accent"]
            elif (c, r) in bot: fill, stroke = P["accent2"], P["accent2"]
            else: fill, stroke = P["ground"], P["line2"]
            s += f'<circle cx="{cx}" cy="{cy}" r="17" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
            if S["last"] and tuple(S["last"]) == (c, r):
                s += f'<circle cx="{cx}" cy="{cy}" r="21" fill="none" stroke="{P["ink"]}" stroke-width="1.5"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
    if line:
        (c0, r0), (c3, r3) = line[0], line[-1]
        x0, y0 = bx + c0 * cell + cell / 2, by + (ROWS - 1 - r0) * cell + cell / 2
        x1, y1 = bx + c3 * cell + cell / 2, by + (ROWS - 1 - r3) * cell + cell / 2
        s += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{P["ink"]}" stroke-width="4" stroke-linecap="round" opacity=".9"/>'
    s += "\n"
    # legend
    ly = by + bh + 28
    s += f'<circle cx="{bx+8}" cy="{ly-4}" r="6" fill="{P["accent"]}"/>' + text(bx + 22, ly, "you, the visitors", 11, P["body"], "mono")
    s += f'<circle cx="{bx+178}" cy="{ly-4}" r="6" fill="{P["accent2"]}"/>' + text(bx + 192, ly, f"the bot, minimax depth {DEPTH}", 11, P["body"], "mono")
    # right column: how to play, last moves, leaderboard, record
    rx = 460
    s += label(rx, 104, "HOW TO PLAY")
    for i, l in enumerate(["Click a column number under the board. It opens a pre-filled issue; press Create.",
                           "A GitHub Action plays your move, the bot answers, and the board redraws in ~20 s.",
                           "Four in a row wins. Anyone can move; you can play a whole game alone."]):
        s += text(rx, 124 + i * 16, l, 11, P["body"], "sans")
    s += label(rx, 194, "LAST MOVES")
    hist = S["history"][-5:][::-1] or [None]
    for i, h in enumerate(hist):
        y = 214 + i * 16
        if h is None: s += text(rx, y, "no moves yet. be the first.", 11, P["muted"], "mono"); break
        s += text(rx, y, f"{h['n']:02d}", 10, P["muted"], "mono") + text(rx + 30, y, f"col {h['col']+1}", 11, P["body"], "mono")
        s += text(rx + 86, y, f"@{h['user']}" if h["who"] == "human" else "bot", 11, P["accent"] if h["who"] == "human" else P["accent2"], "mono")
    s += label(rx, 314, "RECORD")
    s += text(rx, 338, f"{S['games']}", 22, P["ink"], "mono", "700") + label(rx + 2, 354, "GAMES", size=9)
    s += text(rx + 90, 338, f"{S['human_wins']}", 22, P["accent"], "mono", "700") + label(rx + 92, 354, "VISITORS", size=9)
    s += text(rx + 190, 338, f"{S['bot_wins']}", 22, P["accent2"], "mono", "700") + label(rx + 192, 354, "BOT", size=9)
    s += text(rx + 270, 338, f"{S['draws']}", 22, P["body"], "mono", "700") + label(rx + 272, 354, "DRAWS", size=9)
    lb = sorted(S["players"].items(), key=lambda kv: (-kv[1]["wins"], -kv[1]["moves"]))[:5]
    s += label(760, 194, "LEADERBOARD  ·  WINS / MOVES")
    for i, (user, st) in enumerate(lb or [("nobody yet", {"wins": 0, "moves": 0})]):
        y = 214 + i * 16
        s += text(760, y, f"{i+1:02d}", 10, P["muted"], "mono") + text(790, y, f"@{user}" if st["moves"] else user, 11, P["ink"], "mono")
        s += text(RIGHT, y, f"{st['wins']} / {st['moves']}", 10.5, P["body"], "mono", anchor="end")
    s += text(rx, 386, "Stale boards are rejected, refresh and retry.  ·  The bot never resigns. Neither should you.", 10.5, P["muted"], "sans")
    s += close_svg(W, Hh)
    h = hashlib.sha256(s.encode()).hexdigest()[:8]
    os.makedirs(BOARD_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(BOARD_DIR, "c4-*.svg")): os.remove(old)
    path = os.path.join(BOARD_DIR, f"c4-{h}.svg"); open(path, "w").write(s)
    return f"assets/board/c4-{h}.svg"

def links(S):
    n = S["move"]
    def url(t): return f"https://github.com/{OWNER}/{OWNER}/issues/new?title={t}&body=Just+press+%22Create%22.+Don%27t+edit+the+title."
    cols = " ".join(f'<a href="{url(f"c4%7Cdrop%7C{c}%7C{n}")}"><img src="assets/game/col-{c}.svg" width="40" alt="drop in column {c}"/></a>' for c in range(1, 8))
    bot = f'<a href="{url(f"c4%7Cbot%7C{n}")}"><img src="assets/game/bot.svg" width="96" alt="let the bot move for you"/></a>'
    return f'<div align="center">{cols}&nbsp;&nbsp;{bot}</div>'

def write_readme(S, board_rel):
    md = open(README).read()
    block = (f'<!-- c4:start -->\n<div align="center"><img src="{board_rel}" align="top" width="100%" alt="Connect Four board, game {S["game"]}, move {S["move"]}"/></div>\n'
             f'{links(S)}\n<!-- c4:end -->')
    new = re.sub(r"<!-- c4:start -->.*?<!-- c4:end -->", lambda m: block, md, flags=re.S)
    if new == md: raise SystemExit("README has no c4 markers")
    open(README, "w").write(new)

def main():
    title = os.environ.get("ISSUE_TITLE", "").strip(); user = os.environ.get("ISSUE_USER", "someone"); S = load()
    m = re.fullmatch(r"c4\|(drop\|([1-7])|bot|new)\|?(\d*)", title)
    if not m: reject("That title is not a Connect Four move. Use the links under the board.")
    kind, col, n = m.group(1), m.group(2), m.group(3)
    if kind == "new":
        if S["over"] is None and S["move"] > 0 and user != OWNER: reject("A game is in progress. Finish it first.")
        new_game(S)
    else:
        if n == "" or int(n) != S["move"]: reject(f"That board is stale (you clicked move {n or '?'}, the game is at move {S['move']}). Refresh the profile and try again.")
        if S["over"]:
            S["games"] += 0; new_game(S)
        if kind == "bot":
            col = E.best_move(S["human"], S["mask"], depth=4)
        else:
            col = int(col) - 1
        if not E.can_play(S["mask"], col): reject(f"Column {col+1} is full. Pick another.")
        hp, mask = E.mover_after(S["human"], S["mask"], col)
        row = next(r for r in range(E.ROWS) if (mask ^ S["mask"]) & (1 << (col * E.H + r)))
        S["human"], S["mask"], S["move"] = hp, mask, S["move"] + 1; S["last"] = [col, row]
        S["history"].append(dict(n=S["move"], col=col, who="human", user=user))
        pl = S["players"].setdefault(user, dict(moves=0, wins=0)); pl["moves"] += 1
        reply = f"Dropped in column {col+1}."
        if E.wins(S["human"]):
            S["over"] = "human"; S["games"] += 1; S["human_wins"] += 1; pl["wins"] += 1
            reply += " **Four in a row. You beat the bot.** A new game starts with the next move."
        elif S["mask"] == E.FULL:
            S["over"] = "draw"; S["games"] += 1; S["draws"] += 1; reply += " Board full, it's a draw. A new game starts with the next move."
        else:
            bc = E.best_move(S["bot"], S["mask"], DEPTH)
            bp, mask = E.mover_after(S["bot"], S["mask"], bc)
            brow = next(r for r in range(E.ROWS) if (mask ^ S["mask"]) & (1 << (bc * E.H + r)))
            S["bot"], S["mask"], S["move"] = bp, mask, S["move"] + 1; S["last"] = [bc, brow]
            S["history"].append(dict(n=S["move"], col=bc, who="bot", user="bot"))
            reply += f" The bot answered in column {bc+1}."
            if E.wins(S["bot"]):
                S["over"] = "bot"; S["games"] += 1; S["bot_wins"] += 1; reply += " **The bot wins.** A new game starts with the next move."
            elif S["mask"] == E.FULL:
                S["over"] = "draw"; S["games"] += 1; S["draws"] += 1; reply += " Board full, it's a draw."
            else: reply += " Your move."
        S["updated"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rel = render(S); write_readme(S, rel); save(S)
    print(reply if kind != "new" else "New game. Your move.")

if __name__ == "__main__":
    main()
