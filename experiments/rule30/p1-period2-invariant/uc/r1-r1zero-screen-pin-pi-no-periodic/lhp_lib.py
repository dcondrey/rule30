"""Shared kernel for the (PIN-Pi) kill test.

Convention (forward diagram, this repo): s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
Left half-plane row at time t is a Python int with bit i = s(t,-i); bit 0 = c_t (the boundary column).
Update: nxt = (row >> 1) XOR (row OR (row << 1)), then bit 0 overwritten by c_(t+1).
Pin at time t: c_t = 1  =>  s(t,-1) = 1 XOR c_(t+1), i.e. bit 1 of row(t) == 1 XOR c_(t+1).
"""
import itertools

def lhp_step(row, ct1):
    nxt = (row >> 1) ^ (row | (row << 1))
    return (nxt & ~1) | ct1

def tail_survival(row, tail, cap):
    """Steps until the first pin violation when the drive from now on is tail[0], tail[1], ...
    tail[0] must equal row & 1.  Returns cap if no violation within cap steps."""
    for k in range(cap):
        ct1 = tail[k + 1]
        if row & 1:
            if ((row >> 1) & 1) != (1 ^ ct1):
                return k
        row = (((row >> 1) ^ (row | (row << 1))) & ~1) | ct1
    return cap

def periodic_tail(w, phase, length):
    p = len(w)
    return [w[(phase + k) % p] for k in range(length)]

def primitive_words(pmax, pmin=1):
    """All primitive binary words with at least one 1, periods pmin..pmax, every rotation kept."""
    words = []
    for p in range(pmin, pmax + 1):
        for bits in itertools.product([0, 1], repeat=p):
            w = list(bits)
            if 1 not in w:
                continue
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)
    return words

def wstr(w):
    return ''.join(map(str, w))

def naive_lhp(y_bits, c, T, width):
    """Reference: dict-based cell-by-cell simulation of x in [-width, 0].
    y_bits[i] = s(0,-i) for i >= 1; c[t] = s(t,0).  Returns list of rows as ints (bit i = s(t,-i))."""
    cells = {x: 0 for x in range(-width, 1)}
    for i, b in enumerate(y_bits):
        if i >= 1 and -i >= -width:
            cells[-i] = b
    cells[0] = c[0]
    rows = []
    for t in range(T + 1):
        rows.append(sum(cells[x] << (-x) for x in range(-width, 1)))
        new = {}
        for x in range(-width, 0):
            left = cells.get(x - 1, 0)
            right = cells[x + 1]
            new[x] = left ^ (cells[x] | right)
        new[0] = c[t + 1]
        cells = new
    return rows
