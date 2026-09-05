#!/usr/bin/env python3
"""Gate: the direct column recursion used in my scripts reproduces psi_kernel.Endpoint
(column = depths <= 0, diagonal = depths >= 0) on all binary sources to length 9
and all four-state endpoints to length 6."""
import sys
from itertools import product
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY, Endpoint


def columns(endpoint):
    cols = []
    prev = None
    for k, e in enumerate(endpoint):
        col = [0] * (2 * k + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        for d in range(-k + 1, k + 1):
            col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
        cols.append(col)
        prev = col
    return cols


checked = 0
for L in range(1, 10):
    for ep in product((1, 2), repeat=L):
        st = Endpoint()
        for e in ep:
            st.append(e)
        u = L - 1
        col = columns(ep)[u]
        # depths -u-1..u at index d+u+1 ; Endpoint.column[i] = T[u][-i], diagonal[k] = T[u][k]
        for i in range(u + 2):
            assert col[-i + u + 1] == st.column[i], (ep, i)
        for k in range(u + 1):
            assert col[k + u + 1] == st.diagonal[k], (ep, k)
        checked += 1
for L in range(1, 7):
    for ep in product(range(4), repeat=L):
        st = Endpoint()
        for e in ep:
            st.append(e)
        u = L - 1
        col = columns(ep)[u]
        for i in range(u + 2):
            assert col[-i + u + 1] == st.column[i], (ep, i)
        for k in range(u + 1):
            assert col[k + u + 1] == st.diagonal[k], (ep, k)
        checked += 1
print(f"gate passed: {checked} endpoints, direct column recursion == psi_kernel.Endpoint")
