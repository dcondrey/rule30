#!/usr/bin/env python3
"""Round-4 kill tests (fourth external batch, BACKLOG.md section 13).

All entries are read in the source form: W in {1,2}^n and the unstopped
defect word Psi_n(W), since in the diagonal form the hit vector is constant.

  V  toggle / reversal / complement: min Hamming distance between Psi words
  W  reverse-affine-cancellation: A(q) o A(q^R) identity and translation
  X  spiral parity ladder: longest constant run of cumulative spiral parity
  Y  Fibonacci-word factors as sources, n <= 100, fully Fibonacci f
"""

from __future__ import annotations

from itertools import product

from backlog_screen_r1 import levels, window_cells
from psi_kernel import Endpoint, psi


def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


def section_V():
    print("== V  min Hamming distance between Psi words under single toggle / reversal / complement, n=6..15")
    for n in range(6, 16):
        P = {}
        for W in product((1, 2), repeat=n):
            P[W] = psi(W)[1]
        L = n + 2
        tog = min(ham(P[W], P[W[:i] + (3 - W[i],) + W[i + 1 :]]) for W in P for i in range(n))
        rev = min(ham(P[W], P[W[::-1]]) for W in P if W != W[::-1])
        comp = min(ham(P[W], P[tuple(3 - s for s in W)]) for W in P)
        print(f"   n={n} L={L}: toggle min={tog} (need {L/4:.1f})  reversal min={rev} (need {L/5:.1f})  complement min={comp} (need {L/6:.1f})")


def section_W():
    print("== W  reverse-affine-cancellation on forced columns of survivors, n=8..12")

    def compose(maps):
        L = ((1, 0), (0, 1))
        t = (0, 0)
        for a, b in maps:
            Ls = ((1, 0), (b, 1))
            ts = ((1 + a) & 1, 0)
            L = tuple(tuple(sum(Ls[i][k] * L[k][j] for k in range(2)) & 1 for j in range(2)) for i in range(2))
            t = tuple((sum(Ls[i][k] * t[k] for k in range(2)) + ts[i]) & 1 for i in range(2))
        return L, t

    def mult(A, B):  # A o B
        LA, tA = A
        LB, tB = B
        L = tuple(tuple(sum(LA[i][k] * LB[k][j] for k in range(2)) & 1 for j in range(2)) for i in range(2))
        t = tuple((sum(LA[i][k] * tB[k] for k in range(2)) + tA[i]) & 1 for i in range(2))
        return L, t

    ident = zero_t = total = 0
    for n in range(8, 13):
        for c in (2, 3):
            _, per = levels(n, c)
            for k, items in per.items():
                if k < 1:
                    continue
                for st, _ in items:
                    cells = window_cells(st, n + k, n)
                    maps = [((1 if x == 0 else 0), (1 if (x & 1) == 0 else 0)) for x in cells]
                    A = compose(maps)
                    AR = compose(maps[::-1])
                    L, t = mult(A, AR)
                    total += 1
                    if L == ((1, 0), (0, 1)) and t == (0, 0):
                        ident += 1
                    if t == (0, 0):
                        zero_t += 1
    print(f"   columns={total} identity={ident} zero-translation={zero_t}  -> {'KILLED' if ident or zero_t else 'holds'}")


def section_X():
    print("== X  spiral parity ladder: longest constant run of cumulative parity of (H+Lo) over spiral-ordered diagonal, n=8..14")
    for n in range(8, 15):
        worst = 0
        for W in product((1, 2), repeat=n):
            st = Endpoint()
            diag = []
            for m, s in enumerate(W):
                st.append(s)
                diag.append(st.diagonal[m])
            order = []
            lo, hi = 0, n - 1
            while lo <= hi:
                order.append(diag[lo])
                if hi != lo:
                    order.append(diag[hi])
                lo += 1
                hi -= 1
            par, run, best = 0, 1, 1
            prev = None
            for x in order:
                par ^= ((x >> 1) ^ (x & 1))
                if prev is not None and par == prev:
                    run += 1
                    best = max(best, run)
                else:
                    run = 1
                prev = par
            worst = max(worst, best)
        print(f"   n={n}: longest constant run {worst} (need < {n/4:.1f})  -> {'KILLED' if worst >= n/4 else 'holds'}")


def section_Y():
    print("== Y  Fibonacci-word factors as fully structured sources, n<=100, r=0, both c")
    w = "1"
    while len(w) < 4000:
        w = "".join("12" if ch == "1" else "1" for ch in w)
    best = (0, None)
    for n in range(4, 101):
        L = 2 * n + 2
        factors = {w[i : i + L] for i in range(len(w) - L)}
        for f in factors:
            fs = tuple(int(ch) for ch in f)
            for c in (2, 3):
                st = Endpoint()
                run = 0
                for i, s in enumerate(fs):
                    if i >= n:
                        _, dia = st.peek(s)
                        if dia[n] == c:
                            run += 1
                        else:
                            break
                    st.append(s)
                if run == n + 2:
                    print(f"   RW COUNTEREXAMPLE from Fibonacci factor at n={n} c={c}: {f}")
                if run - 0.6 * n > best[0]:
                    best = (run - 0.6 * n, (n, c, run))
    print(f"   max (run - 0.6n) = {best[0]:.1f} at (n,c,run)={best[1]}")


if __name__ == "__main__":
    for sec in (section_V, section_W, section_X, section_Y):
        sec()
        print(flush=True)
