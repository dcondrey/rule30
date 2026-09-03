#!/usr/bin/env python3
"""Round-3 kill tests for the third external backlog (BACKLOG.md section 11).

  P  tri-inj-forced-suffix        W -> forced continuation Q_n(W) injective (all W, and hard-core W)
  Q  forced-column-prefix-uniformity  N_k <= 2^(n-k+2), extended to n = 17..20
  R  survivor-3over4-bound        N_k <= 2^n (3/4)^k for k <= n/2
  S  no-small-period-source       fully periodic f, period p <= 9, n multiple of p up to 100
  T  unstopped hit language       distinct length-k prefixes of Psi_n(W) over all W
  U  column cocycle               affine map of each forced column on (h,F): order and translation
"""

from __future__ import annotations

from itertools import product

from backlog_screen_r1 import forced_step, levels, window_cells
from psi_kernel import Endpoint, psi


def section_P():
    print("== P  tri-inj-forced-suffix: W -> Q_n(W) injective?")
    for n in range(4, 17):
        seen_all, seen_hc = {}, {}
        coll_all = coll_hc = 0
        for W in product((1, 2), repeat=n):
            q, _ = psi(W)
            if q in seen_all:
                coll_all += 1
            seen_all[q] = W
            if "11" not in "".join(map(str, W)):
                if q in seen_hc:
                    coll_hc += 1
                seen_hc[q] = W
        print(f"   n={n}: all W: {2**n} sources -> {len(seen_all)} distinct Q, collisions={coll_all};  hard-core W: {len(seen_hc)+coll_hc} sources -> {len(seen_hc)} distinct, collisions={coll_hc}")


def section_QR():
    print("== Q  N_k <= 2^(n-k+2) and R  N_k <= 2^n (3/4)^k, n=4..20")
    worstQ = (0.0, None)
    violR = []
    for n in range(4, 21):
        for c in (2, 3):
            counts, _ = levels(n, c, keep=False)
            for k, v in enumerate(counts):
                if v == 0:
                    break
                r = v / 2 ** (n - k + 2)
                if r > worstQ[0]:
                    worstQ = (r, (n, c, k, v))
                if k <= n // 2 and v > 2**n * 0.75**k:
                    violR.append((n, c, k, v))
        print(f"   n={n} done", flush=True)
    print(f"   Q: max N_k / 2^(n-k+2) = {worstQ[0]:.3f} at (n,c,k,N_k)={worstQ[1]}  -> {'KILLED' if worstQ[0] > 1 else 'HOLDS to n=20'}")
    print(f"   R: violations {violR[:5]}  -> {'KILLED' if violR else 'HOLDS to n=20'}")


def section_S():
    print("== S  no-small-period-source: fully periodic f, p<=9, n multiple of p, n<=100, r=0, both c")
    words = []
    for p in range(1, 10):
        for w in product((1, 2), repeat=p):
            s = "".join(map(str, w))
            if "11" in (s + s):
                continue
            words.append(w)
    best = (0, None)
    for w in words:
        p = len(w)
        for n in range(p, 101, p):
            f = (w * (3 * n))[: 2 * n + 2]
            for c in (2, 3):
                st = Endpoint()
                run = 0
                for i, s in enumerate(f):
                    if i >= n:
                        _, dia = st.peek(s)
                        if dia[n] == c:
                            run += 1
                        else:
                            break
                    st.append(s)
                if run == n + 2:
                    print(f"   RW COUNTEREXAMPLE: pattern {''.join(map(str,w))} n={n} c={c}")
                if run - 0.6 * n > best[0]:
                    best = (run - 0.6 * n, ("".join(map(str, w)), n, c, run))
    print(f"   {len(words)} hard-core periodic patterns; max (run - 0.6n) = {best[0]:.1f} at (pattern,n,c,run)={best[1]}")


def section_T():
    print("== T  unstopped hit language: distinct length-k prefixes of Psi_n(W), all W")
    for n in range(8, 16):
        words = set()
        for W in product((1, 2), repeat=n):
            _, w = psi(W)
            words.add(w)
        row = []
        for k in (4, 6, 8, 10, 12):
            if k <= n + 2:
                row.append(f"k={k}:{len({w[:k] for w in words})}/{2**k}")
        print(f"   n={n}: distinct Psi words {len(words)} of {2**n};  " + "  ".join(row))


def section_U():
    print("== U  column cocycle on (h,F): order and translation of each forced column's affine map, survivors n=8..12")
    def compose(maps):
        L = ((1, 0), (0, 1))
        t = (0, 0)
        for a, b in maps:
            # step: h' = h + 1 + a ; F' = F + b*h  ->  linear [[1,0],[b,1]], translation (1+a, 0)
            Ls = ((1, 0), (b, 1))
            ts = ((1 + a) & 1, 0)
            L = tuple(tuple(sum(Ls[i][k] * L[k][j] for k in range(2)) & 1 for j in range(2)) for i in range(2))
            t = tuple((sum(Ls[i][k] * t[k] for k in range(2)) + ts[i]) & 1 for i in range(2))
        return L, t

    def order(L, t):
        def apply(x):
            return tuple((sum(L[i][k] * x[k] for k in range(2)) + t[i]) & 1 for i in range(2))
        for m in range(1, 9):
            if all(_iter(apply, x, m) == x for x in [(0, 0), (0, 1), (1, 0), (1, 1)]):
                return m
        return -1

    def _iter(f, x, m):
        for _ in range(m):
            x = f(x)
        return x

    tally_order = {}
    zero_t = nonzero_t = 0
    for n in range(8, 13):
        for c in (2, 3):
            _, per = levels(n, c)
            for k, items in per.items():
                if k < 1:
                    continue
                u = n + k
                for st, word in items:
                    cells = window_cells(st, u, n)
                    maps = [((1 if x == 0 else 0), (1 if (x & 1) == 0 else 0)) for x in cells]
                    L, t = compose(maps)
                    o = order(L, t)
                    tally_order[o] = tally_order.get(o, 0) + 1
                    if t == (0, 0):
                        zero_t += 1
                    else:
                        nonzero_t += 1
    print(f"   order tally over forced columns of survivors: {dict(sorted(tally_order.items()))}")
    print(f"   translation zero: {zero_t}, nonzero: {nonzero_t}")
    print("   group-cocycle-4-cycle:", "KILLED" if any(o != 4 for o in tally_order) else "holds")
    print("   affine-translation-nonzero:", "KILLED" if zero_t else "holds")


if __name__ == "__main__":
    for sec in (section_P, section_T, section_U, section_QR, section_S):
        sec()
        print(flush=True)
