#!/usr/bin/env python3
"""Batch kill tests for the round-1 external backlog (BACKLOG.md).

Every test here is a complete finite computation on the validated kernel.  A
test that passes establishes the statement on the tested range and nothing
more; a test that fails kills the statement with the printed counterexample.

Sections, keyed by backlog id:
  A  L5-ALLORB-CONST     N_k <= 4 * 2^n * 0.47^k
  B  L10-PERSIST-INFLUENCE  every source bit changes the hit vector w.p. >= 1/4
  C  L6-COND-HIT-GAP     conditional hit fraction <= 0.44 in every history bucket
  D  L6-Z-DENSITY-FORCE  |Z|/m in [0.17, 0.33] on surviving columns, u >= n+5
  E  L1-DIAG-INJ-MOD     diagonal -> forced suffix injective
  F  L7-PERIODIC-SOURCE-CAP  periodic sources, run <= 0.6n + 4 (two readings)
  G  L6-FORBIDDEN-FACTOR  which hard-core 6-blocks co-occur with 6 hits
  H  L1-DIAG-DEGREE (corrected)  degree of E(e_u) in the 2n diagonal bits
  I  L10-FIB-TRANSFER    growth of the survivors' forced-symbol block language
  J  L4 transfer operator, corrected alphabet: twisted second eigenvalue
"""

from __future__ import annotations

import math
from itertools import product

from psi_kernel import CONE, Endpoint

E = lambda s: 1 ^ (s >> 1) ^ (s & 1)  # noqa: E731
H = lambda s: s >> 1  # noqa: E731

CONE_INV = [[0] * 4 for _ in range(4)]
for _l in range(4):
    for _r in range(4):
        CONE_INV[_l][CONE[_l][_r]] = _r


# ---------------------------------------------------------------- orbit tools


def forced_step(state: Endpoint, prev: int, n: int, c: int):
    """Return (symbol, hit, hardcore_ok, new_state) or None if H cannot be forced."""
    for s in (1, 2):
        col, dia = state.peek(s)
        if dia[n] >> 1 == 1:
            nxt = Endpoint()
            nxt.column, nxt.diagonal, nxt.length = col + [s], dia, state.length + 1
            return s, (dia[n] == c), not (prev == 1 and s == 1), nxt
    return None


def forced_run(W, n, c, max_len=None):
    """Follow the forced orbit from W; return (hit_vector, symbols, states)."""
    if max_len is None:
        max_len = n + 2
    st = Endpoint()
    for s in W:
        st.append(s)
    prev = W[-1]
    hits, syms, states = [], [], [st]
    for _ in range(max_len):
        step = forced_step(st, prev, n, c)
        if step is None:
            break
        s, hit, hc, st = step
        if not (hit and hc):
            break
        hits.append(1)
        syms.append(s)
        states.append(st)
        prev = s
    return hits, syms, states


def levels(n, c, keep=True):
    """Survivor counts N_k and, per level, the list of surviving (state, word)."""
    counts = [0] * (3 * n)
    per_level_words = {}

    def walk(st, word, depth):
        counts[depth] += 1
        if keep:
            per_level_words.setdefault(depth, []).append((st, tuple(word)))
        if depth >= 2 * n + 2:
            return
        step = forced_step(st, word[-1], n, c)
        if step is None:
            return
        s, hit, hc, nxt = step
        if hit and hc:
            walk(nxt, word + [s], depth + 1)

    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for s in src:
            st.append(s)
        walk(st, list(src), 0)
    return counts, per_level_words


def window_cells(st, u, n):
    """Cells of column u-1 on d in [-u, n-1], st holding e_0..e_{u-1}."""
    cells = [st.column[u]] + [st.column[k] for k in range(u - 1, 0, -1)] + [
        st.diagonal[k] for k in range(u)
    ]
    return cells[: n + u]


# ---------------------------------------------------------------- diagonal form


def diag_to_edge(D, n, c, r=0):
    """Edge word e_0..e_{L-1} of the solution with diagonal D and T[u][n]=c."""
    L = 2 * n + r + 2
    T = {}
    for u in range(n, L):
        T[(u, n)] = c
    for d in range(n - 1, -1, -1):
        T[(d, d)] = D[d]
        for u in range(d + 1, L):
            T[(u, d)] = CONE_INV[T[(u - 1, d)]][T[(u, d + 1)]]
    for d in range(-1, -L - 1, -1):
        u0 = -d - 1
        T[(u0, d)] = T[(u0, d + 1)] ^ 3
        for u in range(u0 + 1, L):
            T[(u, d)] = CONE_INV[T[(u - 1, d)]][T[(u, d + 1)]]
    return tuple(T[(u, -u - 1)] for u in range(L))


def validate_diag(n, c):
    ok = 0
    for D in product(range(4), repeat=n):
        e = diag_to_edge(D, n, c)
        st = Endpoint()
        for m, s in enumerate(e):
            st.append(s)
            if m < n:
                assert st.diagonal[m] == D[m], (D, m)
            else:
                assert st.diagonal[n] == c, (D, m)
        ok += 1
    return ok


def moebius(vals):
    f = vals[:]
    step = 1
    while step < len(f):
        for i in range(0, len(f), step * 2):
            for j in range(i, i + step):
                f[j + step] ^= f[j]
        step *= 2
    return f


# ---------------------------------------------------------------- sections


def section_A():
    print("== A  L5-ALLORB-CONST: N_k <= 4 * 2^n * 0.47^k, n=4..16, both c")
    worst = (0.0, None)
    viol = []
    for n in range(4, 17):
        for c in (2, 3):
            counts, _ = levels(n, c, keep=False)
            for k, v in enumerate(counts):
                if v == 0:
                    break
                bound = 4 * 2**n * 0.47**k
                ratio = v / bound
                if ratio > worst[0]:
                    worst = (ratio, (n, c, k, v, round(bound, 1)))
                if v > bound:
                    viol.append((n, c, k, v, round(bound, 1)))
    print(f"   violations: {viol[:6]}")
    print(f"   tightest N_k / bound = {worst[0]:.3f} at (n,c,k,N_k,bound)={worst[1]}")
    print("   verdict:", "KILLED" if viol else "HOLDS on tested range")


def section_B():
    print("== B  L10-PERSIST-INFLUENCE: min_i Pr[S(f) != S(f xor e_i)] >= 1/4, n=6..11")
    for n in range(6, 12):
        for c in (2, 3):
            vec = {}
            for W in product((1, 2), repeat=n):
                hits, _, _ = forced_run(W, n, c)
                vec[W] = len(hits)  # hit vector is 1^k 0^(n+2-k); k determines it
            infl = []
            for i in range(n):
                diff = 0
                for W in vec:
                    W2 = W[:i] + (3 - W[i],) + W[i + 1 :]
                    if vec[W] != vec[W2]:
                        diff += 1
                infl.append(diff / len(vec))
            print(f"   n={n} c={c} min influence={min(infl):.3f} (at i={infl.index(min(infl))}) max={max(infl):.3f}")


def section_C():
    print("== C  L6-COND-HIT-GAP: hit fraction given last-3 forced symbols <= 0.44, n=8..13")
    worst = (0.0, None)
    for n in range(8, 14):
        for c in (2, 3):
            counts, per = levels(n, c)
            for k, items in per.items():
                if k < 1:
                    continue
                bucket = {}
                for st, word in items:
                    step = forced_step(st, word[-1], n, c)
                    if step is None:
                        continue
                    s, hit, hc, _ = step
                    key = word[-3:]
                    tot, h = bucket.get(key, (0, 0))
                    bucket[key] = (tot + 1, h + (1 if hit else 0))
                for key, (tot, h) in bucket.items():
                    if tot >= 30 and h / tot > worst[0]:
                        worst = (h / tot, (n, c, k, key, tot))
    print(f"   max conditional hit fraction (buckets with >=30 samples) = {worst[0]:.3f} at (n,c,k,history,count)={worst[1]}")
    print("   verdict:", "KILLED (exceeds 0.44)" if worst[0] > 0.44 else "HOLDS on tested range")


def section_D():
    print("== D  L6-Z-DENSITY-FORCE: |Z|/m in [0.17,0.33] on surviving columns with u >= n+5, n=8..14")
    lo, hi = (1.0, None), (0.0, None)
    for n in range(8, 15):
        for c in (2, 3):
            counts, per = levels(n, c)
            for k, items in per.items():
                u = n + k
                if u < n + 5:
                    continue
                for st, word in items:
                    cells = window_cells(st, u, n)
                    z = sum(1 for t in cells if t == 0) / len(cells)
                    if z < lo[0]:
                        lo = (z, (n, c, u))
                    if z > hi[0]:
                        hi = (z, (n, c, u))
    print(f"   min density {lo[0]:.3f} at {lo[1]};  max density {hi[0]:.3f} at {hi[1]}")
    print("   verdict:", "KILLED" if (lo[0] < 0.17 or hi[0] > 0.33) else "HOLDS on tested range")


def section_E():
    print("== E  L1-DIAG-INJ-MOD: diagonal -> forced suffix e[n:] injective, n=3..7")
    for n in (3, 4):
        print(f"   diag_to_edge validated against the kernel on all 4^{n} diagonals: {validate_diag(n, 2)} / {validate_diag(n, 3)} OK")
    for n in range(3, 8):
        for c in (2, 3):
            seen = {}
            collisions = 0
            example = None
            for D in product(range(4), repeat=n):
                e = diag_to_edge(D, n, c)
                key = e[n:]
                if key in seen:
                    collisions += 1
                    if example is None:
                        example = (seen[key], D, key)
                else:
                    seen[key] = D
            print(f"   n={n} c={c}: {4**n} diagonals, {len(seen)} distinct suffixes, collisions={collisions}" + (f"  e.g. {example}" if example else ""))


def section_F():
    print("== F  L7-PERIODIC-SOURCE-CAP: periodic sources, p<=7, n=6..40")
    words = [w for p in range(1, 8) for w in product((1, 2), repeat=p)]
    worst_forced, worst_periodic = (0.0, None), (0.0, None)
    for n in range(6, 41):
        for c in (2, 3):
            for w in words:
                W = tuple((w * (n // len(w) + 1))[:n])
                # reading (ii): W periodic, continuation forced
                hits, _, _ = forced_run(W, n, c)
                k = len(hits)
                if k - 0.6 * n > worst_forced[0]:
                    worst_forced = (k - 0.6 * n, (n, c, "".join(map(str, w)), k))
                # reading (i): the whole word f periodic; count run of T[u][n]==c from u=n with f[n:] hard-core
                f = (w * (3 * n))[: 2 * n + 4]
                st = Endpoint()
                run = 0
                alive = True
                for i, s in enumerate(f):
                    if i >= n:
                        if alive and (i > 0 and f[i - 1] == 1 and s == 1):
                            alive = False
                        _, dia = st.peek(s)
                        if alive and dia[n] == c:
                            run += 1
                        else:
                            alive = False
                    st.append(s)
                if run - 0.6 * n > worst_periodic[0]:
                    worst_periodic = (run - 0.6 * n, (n, c, "".join(map(str, w)), run))
    print(f"   reading (ii) forced continuation: max (run - 0.6n) = {worst_forced[0]:.1f} at (n,c,pattern,run)={worst_forced[1]}")
    print(f"   reading (i) fully periodic f:      max (run - 0.6n) = {worst_periodic[0]:.1f} at {worst_periodic[1]}")
    print("   verdict (cap 0.6n+4):", "KILLED" if max(worst_forced[0], worst_periodic[0]) > 4 else "HOLDS to n=40")


def section_G():
    print("== G  L6-FORBIDDEN-FACTOR: hard-core 6-blocks of forced symbols inside runs of >= 6 hits, n=6..12")
    seen = {}
    for n in range(6, 13):
        for c in (2, 3):
            for W in product((1, 2), repeat=n):
                hits, syms, _ = forced_run(W, n, c)
                if len(syms) >= 6:
                    for i in range(len(syms) - 5):
                        seen["".join(map(str, syms[i : i + 6]))] = seen.get("".join(map(str, syms[i : i + 6])), 0) + 1
    hc6 = ["".join(map(str, w)) for w in product((1, 2), repeat=6) if "11" not in "".join(map(str, w))]
    absent = [w for w in hc6 if w not in seen]
    print(f"   hard-core 6-blocks: {len(hc6)}; occurring inside 6-hit runs: {len(seen)}; absent: {absent}")
    print(f"   212121 occurrences: {seen.get('212121', 0)}")
    print("   verdict: KILLED as stated (212121 co-occurs)" if seen.get("212121", 0) else "   212121 never co-occurs on tested range")


def section_H():
    print("== H  L1-DIAG-DEGREE (corrected): algebraic degree of E(e_u) and H(e_u) in the 2n diagonal bits (H,E of each D_m), n=3..7")
    for n in range(3, 8):
        for c in (2, 3):
            L = 2 * n + 2
            size = 1 << (2 * n)
            cols_E = [[0] * size for _ in range(L)]
            cols_H = [[0] * size for _ in range(L)]
            for idx in range(size):
                D = []
                for m in range(n):
                    h = (idx >> (2 * m)) & 1
                    e = (idx >> (2 * m + 1)) & 1
                    lo = 1 ^ h ^ e
                    D.append(2 * h + lo)
                edge = diag_to_edge(tuple(D), n, c)
                for u in range(L):
                    cols_E[u][idx] = E(edge[u])
                    cols_H[u][idx] = H(edge[u])

            def deg(col):
                anf = moebius(col)
                return max((bin(m).count("1") for m in range(size) if anf[m]), default=0)

            dE = [deg(cols_E[u]) for u in range(L)]
            dH = [deg(cols_H[u]) for u in range(L)]
            print(f"   n={n} c={c} deg E(e_u) u=0..{L-1}: {dE}")
            print(f"            deg H(e_u):          {dH}")


def section_I():
    print("== I  L10-FIB-TRANSFER: distinct forced-symbol m-blocks among survivors with >= 4 hits vs Fibonacci, n=10..13")
    for n in range(10, 14):
        blocks = {m: set() for m in range(3, 9)}
        for c in (2, 3):
            for W in product((1, 2), repeat=n):
                hits, syms, _ = forced_run(W, n, c)
                if len(syms) >= 4:
                    s = "".join(map(str, syms))
                    for m in blocks:
                        for i in range(len(s) - m + 1):
                            blocks[m].add(s[i : i + m])
        fib = {m: len([w for w in product((1, 2), repeat=m) if "11" not in "".join(map(str, w))]) for m in blocks}
        print(f"   n={n}: " + "  ".join(f"m={m}:{len(blocks[m])}/{fib[m]}" for m in blocks))


def section_J():
    print("== J  transfer operator on (h,F), corrected alphabet {(0,0),(0,1),(1,1)}, i.i.d. letters with empirical column frequencies")
    freq = {}
    tot = 0
    for n in (10, 12):
        for c in (2, 3):
            counts, per = levels(n, c)
            for k, items in per.items():
                for st, word in items:
                    for t in window_cells(st, n + k, n):
                        a, b = (1 if t == 0 else 0), (1 if (t & 1) == 0 else 0)
                        freq[(a, b)] = freq.get((a, b), 0) + 1
                        tot += 1
    p = {k: v / tot for k, v in freq.items()}
    print(f"   empirical letter frequencies on surviving columns: {p}")
    states = [(h, F) for h in (0, 1) for F in (0, 1)]
    M = [[0.0] * 4 for _ in range(4)]
    for i, (h, F) in enumerate(states):
        for (a, b), pr in p.items():
            h2, F2 = h ^ 1 ^ a, F ^ (h & b)
            M[states.index((h2, F2))][i] += pr
    # characters chi_t(h,F) = (-1)^(t1 h + t2 F); twisted operator = D_t M D_t on the group algebra
    for t1, t2 in ((0, 1), (1, 0), (1, 1)):
        # projection of M onto the character subspace: eigenvalue = sum over letters of pr * chi(delta)
        # for an affine action, the twisted operator is not diagonal; compute the 4x4 twisted matrix numerically
        Mt = [[M[i][j] * ((-1) ** (t1 * (states[i][0] ^ states[j][0]) + t2 * (states[i][1] ^ states[j][1]))) for j in range(4)] for i in range(4)]
        # power iteration for spectral radius
        v = [1.0, 0.7, 0.3, 0.1]
        rad = 0.0
        for _ in range(200):
            w = [sum(Mt[i][j] * v[j] for j in range(4)) for i in range(4)]
            norm = math.sqrt(sum(x * x for x in w))
            if norm < 1e-12:
                rad = 0.0
                break
            rad = norm / math.sqrt(sum(x * x for x in v))
            v = [x / norm for x in w]
        print(f"   character t=({t1},{t2}): twisted spectral radius ~ {rad:.3f}")
    print("   note: heuristic only; the real input to column u is column u-1, not i.i.d. letters")


if __name__ == "__main__":
    for sec in (section_A, section_B, section_C, section_D, section_E, section_F, section_G, section_H, section_I, section_J):
        sec()
        print(flush=True)
