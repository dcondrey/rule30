#!/usr/bin/env python3
"""V4 refined: which cells beyond depth n are (not) determined by the key (n, u, Z_{u-1}, Z_u).
T[u+1][n+1] = phi(T[u][n], T[u+1][n]) IS determined (both arguments are at depth <= n).
T[u][n+1] = phi(T[u-1][n], T[u][n]) reads T[u-1][n], outside the window, so it need not be.
Exhaustive over binary words u <= 9, n < u."""
import os, sys
from itertools import product
WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)
from psi_kernel import CONE
H = lambda t: t >> 1
def next_column(prev, e, u):
    col = {-u - 1: e, -u: e ^ 3}
    for d in range(-u + 1, u + 1):
        col[d] = CONE[prev[d - 1]][col[d - 1]]
    return col
def triangle(word):
    cols, prev = [], None
    for u, e in enumerate(word):
        prev = next_column(prev, e, u); cols.append(prev)
    return cols
def forced(prev, u, n):
    f = [(e, next_column(prev, e, u)) for e in (1, 2)]
    f = [(e, c) for e, c in f if H(c[n]) == 1]
    assert len(f) == 1
    return f[0]
seen = {}; wit_u = None; wit_u2 = None; keys = 0
for u in range(2, 10):
    for word in product((1, 2), repeat=u):
        prev = triangle(word)[u - 1]
        for n in range(1, u):
            e_u, cur = forced(prev, u, n)
            e2, nxt = forced(cur, u + 1, n)
            Zp = tuple(d for d in range(-u, n) if prev[d] == 0)
            Zu = tuple(d for d in range(-u - 1, n) if cur[d] == 0)
            key = (n, u, Zp, Zu)
            val = (cur[n + 1], nxt[n + 1], nxt[n + 2] if n + 2 <= u + 1 else None, word)
            if key in seen:
                o = seen[key]
                assert o[1] == val[1], ("T[u+1][n+1] must agree", key)
                if o[0] != val[0] and wit_u is None: wit_u = (key, o[3], val[3], o[0], val[0])
                if o[2] is not None and val[2] is not None and o[2] != val[2] and wit_u2 is None: wit_u2 = (key, o[3], val[3], o[2], val[2])
            else:
                seen[key] = val; keys += 1
print(f"keys={keys}; T[u+1][n+1] agrees on every repeated key (determined by the pair).")
print(f"T[u][n+1] first disagreement on equal key: {wit_u}")
print(f"T[u+1][n+2] first disagreement on equal key: {wit_u2}")
