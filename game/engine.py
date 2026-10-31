"""Connect Four on bitboards, with an alpha-beta minimax bot. Columns 0-6, rows 0-5 (bottom = 0)."""
import random

COLS, ROWS = 7, 6
H = ROWS + 1  # one sentinel row per column
ORDER = [3, 2, 4, 1, 5, 0, 6]

def bottom_mask(c): return 1 << (c * H)
def top_mask(c): return 1 << (c * H + ROWS - 1)
def column_mask(c): return ((1 << ROWS) - 1) << (c * H)
FULL = sum(column_mask(c) for c in range(COLS))

def can_play(mask, c): return (mask & top_mask(c)) == 0

def play(pos, mask, c):
    """pos = bitboard of the side to move, mask = all stones. Returns (new_pos_for_mover_after_switch, new_mask)."""
    new_mask = mask | (mask + bottom_mask(c))
    return pos ^ new_mask, new_mask  # opponent's position becomes current after switch: pos ^ mask trick

def wins(pos):
    for shift in (1, H, H - 1, H + 1):
        m = pos & (pos >> shift)
        if m & (m >> (2 * shift)): return True
    return False

def mover_after(pos, mask, c):
    """Apply c for the side whose stones are `pos`; return (mover_pos_after_move, new_mask)."""
    new_mask = mask | (mask + bottom_mask(c))
    return pos | (new_mask ^ mask), new_mask

def negamax(pos, mask, depth, alpha, beta, moves):
    # pos: stones of side to move; opponent = pos ^ mask
    if mask == FULL: return 0
    for c in ORDER:
        if can_play(mask, c):
            p2, m2 = mover_after(pos, mask, c)
            if wins(p2): return (COLS * ROWS + 1 - moves) // 2
    if depth == 0: return score_heuristic(pos, mask)
    best = -10**6
    for c in ORDER:
        if can_play(mask, c):
            p2, m2 = mover_after(pos, mask, c)
            val = -negamax(m2 ^ p2, m2, depth - 1, -beta, -alpha, moves + 1)
            if val > best: best = val
            if best > alpha: alpha = best
            if alpha >= beta: break
    return best

def score_heuristic(pos, mask):
    """Centre preference plus open threes, small numbers so wins always dominate."""
    s = 0
    opp = pos ^ mask
    for c in range(COLS):
        w = 3 - abs(3 - c)
        col = column_mask(c)
        s += w * (bin(pos & col).count("1") - bin(opp & col).count("1"))
    return s // 2

def best_move(pos, mask, depth=7):
    """pos = bot's stones, mask = all stones. Returns column."""
    legal = [c for c in ORDER if can_play(mask, c)]
    for c in legal:  # immediate win
        p2, m2 = mover_after(pos, mask, c)
        if wins(p2): return c
    opp = pos ^ mask
    for c in legal:  # block immediate loss
        o2, m2 = mover_after(opp, mask, c)
        if wins(o2): return c
    best, bestv = None, -10**6
    for c in legal:
        p2, m2 = mover_after(pos, mask, c)
        v = -negamax(m2 ^ p2, m2, depth - 1, -10**6, 10**6, 1)
        if v > bestv or (v == bestv and random.random() < .3):
            best, bestv = c, v
    return best

def cells(pos):
    """Set of (col,row) occupied by a bitboard."""
    out = set()
    for c in range(COLS):
        for r in range(ROWS):
            if pos & (1 << (c * H + r)): out.add((c, r))
    return out

def win_line(pos):
    """Return the four winning cells of pos, or None."""
    cs = cells(pos)
    for (c, r) in cs:
        for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
            line = [(c + k * dc, r + k * dr) for k in range(4)]
            if all(x in cs for x in line): return line
    return None
