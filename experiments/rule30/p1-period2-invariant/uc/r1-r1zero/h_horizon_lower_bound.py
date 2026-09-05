"""Does the period-2 prefix horizon grow without bound as the left support is
allowed to grow?  Constructive: prescribe the trace (01)^inf, take the EMPTY
t=0 right half, and derive s(0,-1..-D) by left permutivity for increasing D.
Each derived row is then evolved by the ordinary Rule 30 evaluator and its true
horizon measured, so the construction is never trusted.

Control: the same construction under Rule 90, whose centre column is NOT
excluded (Rule 90 has no pin), must NOT show a bounded horizon either.
"""
def make(D, tau, step):
    """Derive the t=0 row from the prescribed trace, empty right half."""
    PAD = 4 * D + 64
    # x >= 0 half: determined by the trace alone (right half empty at t=0)
    cols = []                              # cols[t] = row int restricted to x >= 0
    cur = (tau[0] & 1) << PAD
    for t in range(2 * D + 4):
        cols.append(cur)
        nxt = step(cur)
        nxt &= ~((1 << (PAD + 1)) - 1)     # keep only x >= 1
        nxt |= (tau[t + 1] & 1) << PAD
        cur = nxt
    # peel left columns:  s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))   [rule 30]
    #                     s(t,x-1) = s(t+1,x) XOR s(t,x+1)               [rule 90]
    left = {}                              # left[j][t] = s(t, -j)
    left[0] = [(cols[t] >> PAD) & 1 for t in range(2 * D + 4)]
    right1 = [(cols[t] >> (PAD + 1)) & 1 for t in range(2 * D + 4)]
    prev_out = right1
    prev = left[0]
    for j in range(1, D + 1):
        nxtcol = []
        for t in range(len(prev) - 1):
            a, b, c = prev[t + 1], prev[t], prev_out[t]
            nxtcol.append(a ^ (b | c) if step is r30 else a ^ c)
        prev_out, prev = prev, nxtcol
        left[j] = nxtcol
    return {-j: left[j][0] for j in range(0, D + 1) if left[j] and left[j][0]}

def r30(row): return (row << 1) ^ (row | (row >> 1))
def r90(row): return (row << 1) ^ (row >> 1)

def horizon(cells, tau, step, TMAX):
    if not cells:
        return -1
    PAD = TMAX + max(abs(min(cells)), abs(max(cells))) + 4
    row = 0
    for x, b in cells.items():
        if b:
            row |= 1 << (PAD + x)
    H = -1
    for t in range(TMAX):
        if ((row >> PAD) & 1) != tau[t]:
            break
        H = t
        row = step(row)
    return H

TMAX = 900
tau = [t % 2 for t in range(TMAX + 8)]
print("rule 30, trace (01)^inf, empty right half:")
print("   D   support radius w   true horizon H   H - w")
for D in (4, 8, 16, 32, 64, 128, 200, 300):
    cells = make(D, tau, r30)
    w = max(abs(min(cells)), abs(max(cells))) if cells else 0
    H = horizon(cells, tau, r30, TMAX)
    print(f"{D:4d} {w:18d} {H:16d} {H - w:7d}")

print()
print("rule 90 control (same construction, same trace):")
print("   D   support radius w   true horizon H   H - w")
for D in (4, 8, 16, 32, 64, 128, 200, 300):
    cells = make(D, tau, r90)
    w = max(abs(min(cells)), abs(max(cells))) if cells else 0
    H = horizon(cells, tau, r90, TMAX)
    print(f"{D:4d} {w:18d} {H:16d} {H - w:7d}")
