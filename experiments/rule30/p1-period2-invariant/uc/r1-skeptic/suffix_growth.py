#!/usr/bin/env python3
"""Grow the deepest RW witness cylinders to larger n.

The deepest witnesses at (n, c) form suffix cylinders P S (all sharing S).  By
the shift identity T_{yPS}[u+m][n] = T_{PS}[u][n+m] (any y, |y| = m), the run
of P S at depth n' = n + m equals the run of the depth-n row of y P S starting
at column n + 2m.  This script fixes S and enumerates every prefix P of length
n' - |S| for n' = n+1, ..., reporting the deepest run inside the cylinder
against the counterexample threshold n' + 2, and the cylinder survivor counts.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/suffix_growth.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)

from rw_bitsliced import bit_patterns, census, common_suffix, const_array, popcount, set_bits, decode_word  # noqa: E402
from quotient_multiplicity import quotient_column  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def cylinder_census(S: str, n2: int, c: int, max_block: int = 22):
    m = n2 - len(S)
    assert 6 <= m <= max_block
    nwords = (1 << m) >> 6
    pats = bit_patterns(m)
    sources = pats + [const_array(nwords, 1 if ch == "2" else 0) for ch in S]
    res = census(n2, sources, c, n2 + 4, nwords, keep_masks=True)
    deepest = max(k for k in range(len(res.N)) if res.N[k] > 0)
    wit = [decode_word(sources, int(i)) for i in set_bits(res.alive_masks[deepest])][:8]
    return res.N, deepest, wit, res.exact_12a


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=14)
    ap.add_argument("--max-n", type=int, default=30)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--max-block", type=int, default=22)
    args = ap.parse_args()
    data = {}
    for fname in ("census_n07_20.json", "census_n21_30.json"):
        path = os.path.join(HERE, fname)
        if os.path.exists(path):
            data.update(json.load(open(path)))
    for key, e in sorted(data.items(), key=lambda kv: (kv[1]["n"], kv[1]["c"])):
        n, c, d = e["n"], e["c"], e["deepest"]
        if n < args.min_n or n > args.max_n:
            continue
        ws = e["witnesses"].get(str(d), [])
        # largest fiber's common suffix
        fib = Counter()
        byq = {}
        for w in ws:
            q = quotient_column(w)
            fib[q] += 1
            byq.setdefault(q, []).append(w)
        qbest = max(fib, key=fib.get)
        S = common_suffix(byq[qbest])
        print(f"n={n} c={c} deepest={d} witnesses={len(ws)} largest fiber={fib[qbest]} suffix S={S} (|S|={len(S)})")
        for n2 in range(n + 1, n + 1 + args.steps):
            m = n2 - len(S)
            if m < 6:
                # pad S on the left with the witness's own symbols so the free prefix has >= 6 symbols
                continue
            if m > args.max_block:
                break
            N, deep, wit, e12 = cylinder_census(S, n2, c, args.max_block)
            ce = any(e12.get((n2 + 2 + r, 0), 0) > 0 for r in range(3))
            flag = "  <- RW COUNTEREXAMPLE" if ce else ""
            print(
                f"    n'={n2:<3} free prefix={m:<3} cylinder deepest={deep:<3} need={n2+2:<3} slack={n2+2-deep:<3} "
                f"N_k={N[:deep+1]} sample={wit[:2]}{flag}"
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()
