#!/usr/bin/env python3
"""Hit census for the rotated wedge, split into the E part and the hard-core part.

For each n and c in {2,3}, every binary source W in {1,2}^n is run through the
forced continuation (e_u in {1,2} chosen so that H(T[u][n]) = 1).  Two chains
are counted:

  NE_k : W whose first k forced columns all satisfy T[u][n] = c (hits), with
         no hard-core condition at all;
  N_k  : W whose first k forced columns are hits AND the forced symbols are
         hard-core across the junction with W[n-1] (the RW condition 1).

Reported per (n, c):
  * N_k, NE_k for all k until both vanish;
  * per-step ratios N_{k+1}/N_k and NE_{k+1}/NE_k;
  * the constants C1(n,c) = max_k N_k 2^(k-n) and C1E = max_k NE_k 2^(k-n),
    i.e. the smallest C for which N_k <= C 2^(n-k) holds at this n;
  * the number of distinct forced continuation words e[n..n+k) among the
    E-survivors at each level (injectivity of W -> continuation);
  * the fraction of E-survivors at level k whose forced symbol at column n+k
    is 1 and whose previous symbol is 1 (the hard-core kill fraction).

Run:  cd <kernel dir> && uv run python uc/r1-entropy/hit_census.py --min 3 --max 15
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from itertools import product

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def forced_run(source: tuple[int, ...], target: int, max_steps: int):
    """Follow the forced continuation, return (hits, symbols).

    hits[k] is 1 iff T[n+k][n] == target; symbols[k] is the forced e_{n+k}.
    Stops after the first non-hit (the E-only chain is a prefix property), or
    after max_steps hits.
    """
    n = len(source)
    state = Endpoint()
    for s in source:
        state.append(s)
    hits: list[int] = []
    symbols: list[int] = []
    for _ in range(max_steps):
        chosen = None
        for sym in (1, 2):
            _, diag = state.peek(sym)
            if diag[n] >> 1 == 1:
                chosen = (sym, diag[n])
                break
        assert chosen is not None
        sym, cell = chosen
        state.append(sym)
        symbols.append(sym)
        hit = 1 if cell == target else 0
        hits.append(hit)
        if not hit:
            break
    return hits, symbols


def census(n: int, target: int, log) -> dict:
    max_steps = n + 3
    NE = Counter()
    N = Counter()
    cont_words: dict[int, set] = defaultdict(set)
    hc_kill = Counter()  # level k -> number of E-survivors at level k+1 killed by HC at k+1
    e_surv_next = Counter()
    for source in product((1, 2), repeat=n):
        hits, symbols = forced_run(source, target, max_steps)
        prev = source[-1]
        hc_ok = True
        k = 0
        NE[0] += 1
        N[0] += 1
        for j, h in enumerate(hits):
            sym = symbols[j]
            if not h:
                break
            k = j + 1
            NE[k] += 1
            cont_words[k].add(tuple(symbols[:k]))
            if hc_ok:
                if prev == 1 and sym == 1:
                    hc_ok = False
                    hc_kill[k] += 1
                else:
                    N[k] += 1
            prev = sym
    out = {"n": n, "c": target, "NE": NE, "N": N}
    kmax = max(max(NE), max(N))
    print(f"\n# n={n} c={target}", file=log)
    print(" k    NE_k   N_k   NE_k/NE_k-1  N_k/N_k-1  NE_k*2^(k-n)  N_k*2^(k-n)  distinct_cont  hc_kill_frac", file=log)
    C1 = 0.0
    C1E = 0.0
    for k in range(0, kmax + 1):
        ne = NE.get(k, 0)
        nn = N.get(k, 0)
        rE = ne / NE[k - 1] if k > 0 and NE.get(k - 1, 0) else float("nan")
        rN = nn / N[k - 1] if k > 0 and N.get(k - 1, 0) else float("nan")
        cE = ne * 2.0 ** (k - n)
        cN = nn * 2.0 ** (k - n)
        C1 = max(C1, cN)
        C1E = max(C1E, cE)
        dc = len(cont_words.get(k, ())) if k > 0 else 1
        # hc kill fraction among those that were HC-legal at k-1 and hit at k
        legal_prev = N.get(k - 1, 0) if k > 0 else 0
        killed = hc_kill.get(k, 0)
        frac = killed / (nn + killed) if (nn + killed) > 0 else float("nan")
        print(f"{k:2d} {ne:7d} {nn:6d}   {rE:9.4f}  {rN:9.4f}   {cE:10.4f}   {cN:10.4f}   {dc:8d}      {frac:7.4f}", file=log)
    print(f"C1(n={n},c={target}) = max_k N_k 2^(k-n) = {C1:.4f};  C1E = {C1E:.4f}", file=log)
    out["C1"] = C1
    out["C1E"] = C1E
    out["kmax_N"] = max(k for k in N if N[k] > 0)
    out["kmax_NE"] = max(k for k in NE if NE[k] > 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--max", type=int, default=13)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/hit_census.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        summary = []
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                r = census(n, c, log)
                summary.append(r)
                log.flush()
        print("\n# summary: n c C1(joint) C1E(E-only) kmax_N kmax_NE  kmax_N/n", file=log)
        for r in summary:
            print(f"{r['n']:3d} {r['c']} {r['C1']:8.4f} {r['C1E']:8.4f} {r['kmax_N']:4d} {r['kmax_NE']:4d}  {r['kmax_N']/r['n']:.3f}", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()
