#!/usr/bin/env python3
"""Ad hoc Myhill-Nerode check for the N_j counting line (block_halving.py /
flip_pairing.py). Not part of the tracked experiment suite; scratch only.

Question: among survivors of level j (alive/hard-core/matching c through
level j-1), does the number of distinct FUTURE-BEHAVIOR classes (forced
symbol/cell/hard-core sequence over the next W levels) stay bounded as n
grows at fixed j, or does it grow with n (=> no finite state suffices)?
"""
from __future__ import annotations
import sys
from flip_pairing import census

W = 8  # look-ahead window for the behavior signature

def run(min_n, max_n):
    print(f"window W={W}")
    for n in range(min_n, max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        total = 1 << n
        for c in (2, 3):
            death = [levels] * total
            for w in range(total):
                for j in range(levels):
                    if not hcs[w][j] or cells[w][j] != c:
                        death[w] = j
                        break
            row = []
            for j in range(0, min(6, levels - W)):
                surv = [w for w in range(total) if death[w] >= j]
                if not surv:
                    break
                sigs = set()
                raw_states = set()
                for w in surv:
                    sig = tuple(zip(syms[w][j:j+W], cells[w][j:j+W], hcs[w][j:j+W]))
                    sigs.add(sig)
                    raw_states.add(keys[w])
                row.append((j, len(surv), len(sigs), len(raw_states)))
            print(f"n={n:2d} c={c}: " + "  ".join(f"j={j}:N={N},sig={S},raw={R}" for j,N,S,R in row))
            sys.stdout.flush()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=9)
    ap.add_argument("--max-n", type=int, default=15)
    a = ap.parse_args()
    run(a.min_n, a.max_n)
