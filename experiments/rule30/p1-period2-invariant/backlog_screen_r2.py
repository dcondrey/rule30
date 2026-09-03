#!/usr/bin/env python3
"""Round-2 kill tests: the three testable entries of the 7-page PDF backlog
(`candidate_lemmas_for_the_rule_30_period-two_attack`), all about the survivor
set in DIAGONAL coordinates, plus a corrected transfer-operator eigenvalue.

Survivors S_k(n, c) = {diagonals D(W) : W in {1,2}^n survives k hits}.  Each
diagonal symbol carries two bits (H, E), so S_k sits in {0,1}^(2n).

  K  diagonal-martingale     count coordinates DETERMINED by the others on S_k
  L  diagonal-cube-separation  C_needed = max over fixings of q symbols of
                              (fraction of S_k in the subcube) * 4^q
  M  diagonal-permutation-cylinder  free bits per survivor and the largest
                              sub-box of {0,1}^(2n) inside S_k, giving a lower
                              bound |S_k| / 2^maxbox on the cylinder cover
  N  plain 4x4 transition matrix on (h,F) for i.i.d. letters: eigenvalues
"""

from __future__ import annotations

from itertools import combinations, product

from backlog_screen_r1 import forced_step, window_cells
from psi_kernel import Endpoint

E = lambda s: 1 ^ (s >> 1) ^ (s & 1)  # noqa: E731
H = lambda s: s >> 1  # noqa: E731


def survivors(n, c):
    """Per level k: list of diagonals (as tuples of (H,E) bits, length 2n)."""
    per = {}

    def walk(st, word, depth, diag):
        per.setdefault(depth, []).append(diag)
        if depth >= 2 * n + 2:
            return
        step = forced_step(st, word[-1], n, c)
        if step is None:
            return
        s, hit, hc, nxt = step
        if hit and hc:
            walk(nxt, word + [s], depth + 1, diag)

    for src in product((1, 2), repeat=n):
        st = Endpoint()
        diag = []
        for m, s in enumerate(src):
            st.append(s)
            t = st.diagonal[m]
            diag.extend((H(t), E(t)))
        walk(st, list(src), 0, tuple(diag))
    return per


def section_K(max_n=12):
    print("== K  diagonal-martingale: coordinates determined by the others on S_k (bits, then whole symbols)")
    for n in range(6, max_n + 1):
        for c in (2, 3):
            per = survivors(n, c)
            rows = []
            for k in sorted(per):
                S = set(per[k])
                if len(S) < 2:
                    break
                det_bits = 0
                for b in range(2 * n):
                    fib = {}
                    ok = True
                    for D in S:
                        key = D[:b] + D[b + 1 :]
                        if key in fib and fib[key] != D[b]:
                            ok = False
                            break
                        fib[key] = D[b]
                    det_bits += ok
                det_sym = 0
                for m in range(n):
                    fib = {}
                    ok = True
                    for D in S:
                        key = D[: 2 * m] + D[2 * m + 2 :]
                        val = D[2 * m : 2 * m + 2]
                        if key in fib and fib[key] != val:
                            ok = False
                            break
                        fib[key] = val
                    det_sym += ok
                rows.append(f"k={k}:|S|={len(S)},detbits={det_bits},detsym={det_sym}")
            print(f"   n={n} c={c}  " + "  ".join(rows))


def section_L(max_n=12):
    print("== L  diagonal-cube-separation: C_needed = max_subcube fraction * 4^q, q=1..3 symbols fixed")
    for n in range(8, max_n + 1):
        for c in (2, 3):
            per = survivors(n, c)
            rows = []
            for k in sorted(per):
                S = per[k]
                if len(S) < 32:
                    break
                worst = 0.0
                for q in (1, 2, 3):
                    for coords in combinations(range(n), q):
                        cnt = {}
                        for D in S:
                            key = tuple(D[2 * m : 2 * m + 2] for m in coords)
                            cnt[key] = cnt.get(key, 0) + 1
                        worst = max(worst, max(cnt.values()) / len(S) * 4**q)
                rows.append(f"k={k}:|S|={len(S)},C={worst:.1f}")
            print(f"   n={n} c={c}  " + "  ".join(rows))


def section_M(max_n=12):
    print("== M  diagonal-permutation-cylinder: free bits per survivor, largest box, cover lower bound |S|/2^box")
    for n in range(8, max_n + 1):
        for c in (2, 3):
            per = survivors(n, c)
            rows = []
            for k in sorted(per):
                S = set(per[k])
                if len(S) < 8:
                    break
                maxbox = 0
                free_hist = {}
                for D in S:
                    free = [b for b in range(2 * n) if (D[:b] + (D[b] ^ 1,) + D[b + 1 :]) in S]
                    free_hist[len(free)] = free_hist.get(len(free), 0) + 1
                    # greedy box growth from D over its free bits
                    box = []
                    for b in free:
                        cand = box + [b]
                        ok = True
                        for bits in product((0, 1), repeat=len(cand)):
                            P = list(D)
                            for bb, v in zip(cand, bits):
                                P[bb] = v
                            if tuple(P) not in S:
                                ok = False
                                break
                        if ok:
                            box = cand
                    maxbox = max(maxbox, len(box))
                lb = len(S) / 2**maxbox
                nofree = free_hist.get(0, 0)
                rows.append(f"k={k}:|S|={len(S)},maxbox={maxbox},cover>={lb:.0f},isolated={nofree}")
            print(f"   n={n} c={c}  " + "  ".join(rows))


def section_N():
    print("== N  plain transition matrix on (h,F), i.i.d. letters with empirical frequencies: eigenvalues")
    p = {(0, 0): 0.500, (0, 1): 0.286, (1, 1): 0.214}
    states = [(h, F) for h in (0, 1) for F in (0, 1)]
    M = [[0.0] * 4 for _ in range(4)]
    for j, (h, F) in enumerate(states):
        for (a, b), pr in p.items():
            i = states.index((h ^ 1 ^ a, F ^ (h & b)))
            M[i][j] += pr
    # characteristic polynomial via numpy if present, else power iteration on M - (1/4)J
    try:
        import numpy as np

        ev = np.linalg.eigvals(np.array(M))
        print("   eigenvalues:", sorted((round(abs(x), 4) for x in ev), reverse=True))
    except Exception as exc:  # noqa: BLE001
        print("   numpy unavailable:", exc)
    print("   heuristic only: the real input to column u is column u-1")


if __name__ == "__main__":
    for sec in (section_K, section_L, section_M, section_N):
        sec()
        print(flush=True)
