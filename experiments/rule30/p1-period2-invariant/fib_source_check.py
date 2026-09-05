#!/usr/bin/env python3
"""Fibonacci-word factors as sources, WITH the hard-core check on f[n:] that
backlog_screen_r4.py section Y omitted (its printed 'counterexample' at n=5 has
11 in the forced part and is the known BWH+ constant, not an RW word)."""
from psi_kernel import Endpoint
w = "1"
while len(w) < 4000:
    w = "".join("12" if ch == "1" else "1" for ch in w)
best = (0, None); hc_factors = 0
for n in range(4, 101):
    L = 2 * n + 2
    for f in {w[i:i + L] for i in range(len(w) - L)}:
        if "11" in f[n - 1:]:
            continue
        hc_factors += 1
        fs = tuple(int(ch) for ch in f)
        for c in (2, 3):
            st = Endpoint(); run = 0
            for i, s in enumerate(fs):
                if i >= n:
                    _, dia = st.peek(s)
                    if dia[n] == c: run += 1
                    else: break
                st.append(s)
            if run == n + 2:
                print(f"RW COUNTEREXAMPLE n={n} c={c}: {f}")
            if run - 0.6 * n > best[0]:
                best = (run - 0.6 * n, (n, c, run))
print(f"hard-core Fibonacci factors tested: {hc_factors}; max (run - 0.6n) = {best[0]:.1f} at {best[1]}")
