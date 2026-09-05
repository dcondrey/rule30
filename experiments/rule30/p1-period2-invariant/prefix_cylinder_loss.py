#!/usr/bin/env python3
"""G4 over the only sufficient statistic: conditional survival by exact prefix state.

PRE-REGISTERED 2026-09-03, before running.

`RESULTS-COLUMN-DECOMPOSITION.md` section 10 killed the column-memory rate
route: the column is not a sufficient statistic for RW survival, the full
endpoint state is.  Any rate argument must therefore condition on the exact
state.  Within a fixed `n` the forced continuation is deterministic, so the
only branching is the choice of the `n` source symbols, and the right
conditional object is the prefix cylinder.

Setting.  `W in {1,2}^n`.  For `p < n` let `s = state(W[:p])` be the exact
endpoint state after `p` free symbols (column and diagonal, the statistic whose
sufficiency section 10 verified).  For a level `j` write

    N_j(s) = #{W with prefix state s that survive j forced levels}
    rho_j(s) = N_j(s) / 2^(n-p)

Reported per `(n, p, c)`: the maximum and the mean of `rho_j(s)` over prefix
states, the block ratio `max_s rho_{j+b}(s) / rho_j(s)`, the number of states
attaining the maximum, and the signature of the maximizers.

Discriminator, the distinction that decides whether a block lemma is possible:
  * UNIFORM loss: every state loses possibilities, `max_s` ratio `<= lambda < 1`
    for some block length `b`.  This can support a proof.
  * AVERAGE loss with RESERVOIRS: the aggregate decays but some states hold
    ratio 1 at growing depth.  Then no uniform `b`-block contraction exists for
    this state definition and the reservoirs must be classified separately.

Kill (pre-registered): a prefix state with block ratio 1.0 at every tested `b`
and a death depth growing with `n`.  That is the reservoir case and it kills
the uniform block lemma for the exact prefix state, which is the strongest
state definition available.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

from psi_kernel import Endpoint
from flip_pairing import census


def prefix_state(src, p):
    st = Endpoint()
    for s in src[:p]:
        st.append(s)
    return (tuple(st.column), tuple(st.diagonal))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=15)
    ap.add_argument("--blocks", type=str, default="1,2,3,4,6")
    args = ap.parse_args()
    blocks = [int(x) for x in args.blocks.split(",")]
    global THRESHOLDS
    THRESHOLDS = [1, 4, 16]

    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        srcs = list(product((1, 2), repeat=n))
        for p in (n // 3, n // 2, (2 * n) // 3):
            groups = defaultdict(list)
            for idx, w in enumerate(srcs):
                groups[prefix_state(w, p)].append(idx)
            for c in (2, 3):
                # per-group survivor counts by level
                per = {}
                for s, members in groups.items():
                    row = [0] * (levels + 1)
                    for idx in members:
                        d = levels
                        cl, hc = cells[idx], hcs[idx]
                        for j in range(levels):
                            if not hc[j] or cl[j] != c:
                                d = j
                                break
                        for j in range(d + 1):
                            row[j] += 1
                    per[s] = row
                tot = 1 << (n - p)
                out = []
                for b in blocks:
                    # worst[thr] = max ratio over states whose numerator count is >= thr
                    res = {}
                    for thr in THRESHOLDS:
                        worst, nmax, arg = 0.0, 0, None
                        for s, row in per.items():
                            for j in range(levels):
                                if row[j] < thr or row[j] == 0:
                                    continue
                                nxt = row[j + b] if j + b <= levels else 0
                                r = nxt / row[j]
                                if r > worst + 1e-12:
                                    worst, nmax, arg = r, 1, (j, row[j], nxt)
                                elif abs(r - worst) <= 1e-12:
                                    nmax += 1
                        res[thr] = (worst, nmax, arg)
                    out.append((b, res))
                maxdeep = max(max(j for j in range(levels + 1) if row[j] > 0) for row in per.values())
                nres = sum(1 for row in per.values()
                           if any(row[j] > 0 and j + 1 <= levels and row[j + 1] == row[j]
                                  for j in range(levels)))
                print(f"n={n:>2} p={p:>2} c={c} states={len(groups):>6} fibre={tot:>6} "
                      f"deepest={maxdeep:>2} plateau-states={nres:>5}")
                for b, res in out:
                    parts = []
                    for thr in THRESHOLDS:
                        w, k, arg = res[thr]
                        a = f"@j={arg[0]},{arg[1]}->{arg[2]}" if arg else "@none"
                        parts.append(f"thr>={thr}: {w:.3f} (x{k}) {a}")
                    print(f"    b={b:>2} | " + " | ".join(parts))
                sys.stdout.flush()


if __name__ == "__main__":
    main()
