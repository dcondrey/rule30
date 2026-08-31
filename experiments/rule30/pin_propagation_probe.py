"""Fixpoint: start knowing only the centre column, propagate every exact
Rule 30 inference, report how much of the space-time diagram gets determined."""
import sys

def spacetime(T, N):
    row = [0]*(2*N+1); row[N] = 1; S = []
    for _ in range(T+1):
        S.append(row[:]); nr = [0]*(2*N+1)
        for x in range(1, 2*N): nr[x] = row[x-1] ^ (row[x] | row[x+1])
        row = nr
    return S

def propagate(T, W, known):
    """known[t][x] in {None,0,1}; x index 0..2W for columns -W..W."""
    changed = True
    while changed:
        changed = False
        for t in range(T):
            for x in range(1, 2*W):
                a, b, cc = known[t][x-1], known[t][x], known[t][x+1]
                d = known[t+1][x]
                # forward
                if d is None and a is not None and b is not None and cc is not None:
                    known[t+1][x] = a ^ (b | cc); changed = True; continue
                if d is None: continue
                # 1 pins the LEFT neighbour
                if b == 1 and a is None:
                    known[t][x-1] = d ^ 1; changed = True; continue
                # 0 pins the RIGHT neighbour, given the left one
                if b == 0 and a is not None and cc is None:
                    known[t][x+1] = d ^ a; changed = True; continue
                # left neighbour from a known OR
                if a is None and b is not None and cc is not None:
                    known[t][x-1] = d ^ (b | cc); changed = True; continue
    return known

T, W = 220, 90
S = spacetime(T, T+5); N = T+5
known = [[None]*(2*W+1) for _ in range(T+1)]
for t in range(T+1): known[t][W] = S[t][N]          # centre column only
propagate(T, W, known)

tot = det = 0; wrong = 0
per_col = {}
for x in range(2*W+1):
    d = sum(1 for t in range(T+1) if known[t][x] is not None)
    per_col[x-W] = d
for t in range(T+1):
    for x in range(2*W+1):
        tot += 1
        if known[t][x] is not None:
            det += 1
            if known[t][x] != S[t][N+x-W]: wrong += 1
print("determined %d / %d cells (%.3f%%), inconsistencies %d" % (det, tot, 100*det/tot, wrong))
print("columns with >0 determined:", sorted(k for k,v in per_col.items() if v>0))
for k in sorted(per_col):
    if per_col[k] > 0 and abs(k) <= 6:
        print("  column %+d: %d / %d times determined" % (k, per_col[k], T+1))
