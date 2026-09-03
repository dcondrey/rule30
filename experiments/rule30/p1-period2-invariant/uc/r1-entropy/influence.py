#!/usr/bin/env python3
"""Influence of each source coordinate on the next hit, conditional on survival.

For each (n, c), each level k (number of joint hits + hard-core survived so
far) and each coordinate j of the source W in {1,2}^n, over all level-k
survivors W:

  keep[k][j]  = fraction of survivors W such that flipping W_j gives a W' that
                is also a level-k survivor (same first k hits, hard-core);
  flip[k][j]  = fraction of survivors W such that W' is a level-k survivor AND
                hit_{k+1}(W') != hit_{k+1}(W)   (the E-bit at column n+k flips);
  hcflip[k][j]= fraction such that W' is a level-k survivor and the hard-core
                legality of the forced symbol at column n+k differs.

An exact halving of N_{k+1} <= N_k / 2 by an involution needs some j with
keep = 1 and flip = 1 at level k.  The script reports, per level, the best j
by flip fraction, and the number of coordinates with keep = 1.

Also reports the multiplicity structure: at each level k the survivors are
grouped by their forced continuation word e[n..n+k); the size distribution of
these groups is printed (clusters).

Run:  cd <kernel dir> && uv run python uc/r1-entropy/influence.py --min 8 --max 14
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def run(source, target, max_steps):
    """Return (hits, symbols, hc) lists along the forced continuation.

    hits[j] = 1 iff T[n+j][n] == target.  hc[j] = 1 iff symbol j is hard-core
    legal w.r.t. its predecessor.  Continues for max_steps regardless of hits
    so that the caller can evaluate survival at every level.
    """
    n = len(source)
    st = Endpoint()
    for s in source:
        st.append(s)
    hits, symbols, hc = [], [], []
    prev = source[-1]
    for _ in range(max_steps):
        chosen = None
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                chosen = (sym, diag[n])
                break
        sym, cell = chosen
        st.append(sym)
        symbols.append(sym)
        hits.append(1 if cell == target else 0)
        hc.append(0 if (prev == 1 and sym == 1) else 1)
        prev = sym
    return hits, symbols, hc


def level(hits, hc):
    """Largest k such that hits[0..k) all 1 and hc[0..k) all 1."""
    k = 0
    while k < len(hits) and hits[k] and hc[k]:
        k += 1
    return k


def analyse(n, target, log, max_level):
    max_steps = n + 3
    data = {}
    for source in product((1, 2), repeat=n):
        data[source] = run(source, target, max_steps)
    print(f"\n# n={n} c={target}", file=log)
    for k in range(0, max_level + 1):
        surv = [w for w, (h, s, c) in data.items() if level(h, c) >= k]
        if not surv:
            break
        Nk = len(surv)
        keep = [0] * n
        flip = [0] * n
        hcf = [0] * n
        for w in surv:
            h, s, c = data[w]
            for j in range(n):
                w2 = list(w)
                w2[j] = 3 - w2[j]
                w2 = tuple(w2)
                h2, s2, c2 = data[w2]
                if level(h2, c2) >= k:
                    keep[j] += 1
                    if h2[k] != h[k]:
                        flip[j] += 1
                    if c2[k] != c[k]:
                        hcf[j] += 1
        # cluster structure by continuation word
        groups = Counter(tuple(data[w][1][:k]) for w in surv)
        sizes = Counter(groups.values())
        nxt = sum(1 for w in surv if data[w][0][k] and data[w][2][k])
        print(f"level {k}: N_k={Nk} N_k+1={nxt} ratio={nxt/Nk:.3f}  groups={len(groups)} sizes={dict(sorted(sizes.items()))}", file=log)
        line = "   j: " + " ".join(f"{j:5d}" for j in range(n))
        print(line, file=log)
        print("keep: " + " ".join(f"{keep[j]/Nk:5.2f}" for j in range(n)), file=log)
        print("flip: " + " ".join(f"{flip[j]/Nk:5.2f}" for j in range(n)), file=log)
        print("hcfl: " + " ".join(f"{hcf[j]/Nk:5.2f}" for j in range(n)), file=log)
        best = max(range(n), key=lambda j: flip[j])
        full_keep = [j for j in range(n) if keep[j] == Nk]
        print(f"   best flip j={best} flip={flip[best]/Nk:.3f} keep={keep[best]/Nk:.3f}; coordinates with keep=1: {full_keep}", file=log)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=8)
    ap.add_argument("--max", type=int, default=12)
    ap.add_argument("--max-level", type=int, default=12)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/influence.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                analyse(n, c, log, args.max_level)
                log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()
