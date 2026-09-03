#!/usr/bin/env python3
"""Class-level census of the forced continuation, (BWH+) and (RW).

State at column u (u >= n-1): the three-letter quotient word of column u on
depths [-u-1, n-1] (top symbol e_u included at depth -u-1).  By BRIEF section
2 this determines the forced symbol e_{u+1} (parity of zeros), the whole of
column u+1 on depths <= n, and hence every later depth-n cell.  So two sources
with the same state are the same trial forever after; a class is one trial.

Level k = column u = n-1+k.  For each of three regimes the script propagates
classes with multiplicities and reports N_k (sources) and S_k (classes):
  free : forced high bit only, no kill (measures class MERGING in the run region);
  bwh  : plus E(T[u][n]) = E(c) for every run column (BWH+ survivors);
  rw   : plus hard-core on the forced symbols including the junction e_{n-1} e_n.
Moore step (BRIEF section 2): (h,F) -> (h ^ 1 ^ a, F ^ (h & b)); letter of a
state: a = [h==0 and F==1], b = [h != F]; letters of symbols 1 -> (0,0), 2 -> (0,1).
"""
from __future__ import annotations

import sys
from math import log2
from collections import defaultdict

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402

LET = {0: 2, 1: 0, 2: 1, 3: 0}  # cell -> letter code: 0 -> (1,1)=2, 2 -> (0,1)=1, {1,3} -> (0,0)=0
AB = {0: (0, 0), 1: (0, 1), 2: (1, 1)}


def initial_classes(n: int) -> dict[bytes, int]:
    """Quotient of column n-1 (depths -n..n-1) -> multiplicity, over all 2^n sources."""
    classes: dict[bytes, int] = defaultdict(int)

    def rec(u: int, prev: list[int] | None) -> None:
        for e in (1, 2):
            col = [0] * (2 * u + 2)
            col[0] = e
            col[1] = BOUNDARY[e]
            for d in range(-u + 1, u + 1):
                col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
            if u == n - 1:
                classes[bytes(LET[t] for t in col[: n + u + 1])] += 1  # depths -u-1..n-1
            else:
                rec(u + 1, col)

    rec(0, None)
    return dict(classes)


def step(key: bytes, n: int, u: int, c: int, regime: str) -> bytes | None:
    """Advance class `key` (column u-1, depths -u..n-1) to column u; None if killed."""
    # forced symbol: H(e_u) = 1 + (n + u + 1) + #zeros  (BRIEF (H-forcing)), zeros = letter code 2
    zeros = key.count(2)
    He = (1 + (n + u + 1) + zeros) & 1
    e = 2 if He else 1
    if regime == "rw":
        prev_e = 1 if key[0] == 0 else 2  # top letter of column u-1 encodes e_{u-1}
        if prev_e == 1 and e == 1:
            return None
    h, F = 1 - He, 0
    out = bytearray(n + u + 2)  # depths -u-1..n
    out[0] = 0 if e == 1 else 1
    idx = 1
    for code in key:  # depths -u .. n-1 of column u-1 -> states at depths -u .. n of column u
        # state at current depth is (h,F); emit its letter, then read letter `code` to get the next depth
        out[idx] = 2 if (h == 0 and F == 1) else (1 if h != F else 0)
        idx += 1
        a, b = AB[code]
        h, F = h ^ 1 ^ a, F ^ (h & b)
    # (h,F) is now the state at depth n; h must be 1 by forcing
    assert h == 1, (n, u, key)
    if regime in ("bwh", "rw") and F != (c & 1):  # E(c) = c & 1 when H(c) = 1
        return None
    return bytes(out[: n + u + 1])  # depths -u-1..n-1


def main() -> None:
    ns = [int(x) for x in sys.argv[1:]] or [10, 12, 14]
    for n in ns:
        init = initial_classes(n)
        S0 = len(init)
        print(f"\n===== n={n}: sources {2**n}, initial classes {S0} (log2 {log2(S0):.3f})")
        for c in (2, 3):
            for regime in ("free", "bwh", "rw"):
                classes = dict(init)
                rows = []
                for k in range(1, n + 3):
                    u = n - 1 + k
                    nxt: dict[bytes, int] = defaultdict(int)
                    for key, mult in classes.items():
                        nk = step(key, n, u, c, regime)
                        if nk is not None:
                            nxt[nk] += mult
                    classes = dict(nxt)
                    N = sum(classes.values())
                    S = len(classes)
                    rows.append((k, N, S))
                    if S == 0:
                        break
                line = " ".join(f"k{k}:{N}/{S}" for k, N, S in rows)
                # bits per column lost in classes, from the initial count to the last nonzero
                nz = [(k, S) for k, N, S in rows if S > 0]
                if regime == "free":
                    print(f"  c={c} {regime:4s}: " + line)
                    if len(nz) >= 2:
                        k1, S1 = nz[-1]
                        print(f"           class log2 drop over {k1} run columns: {log2(S0) - log2(S1):.3f} ({(log2(S0) - log2(S1))/k1:.3f} bits/column of pure merging)")
                else:
                    print(f"  c={c} {regime:4s}: " + line)
                    if nz:
                        kl, Sl = nz[-1]
                        print(f"           deepest surviving level {kl} (need {n+2}); last surviving classes {Sl}; per-column class loss {(log2(S0) - log2(Sl))/kl:.3f} bits")


if __name__ == "__main__":
    main()
