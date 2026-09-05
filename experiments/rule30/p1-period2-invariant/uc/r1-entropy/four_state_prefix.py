#!/usr/bin/env python3
"""Is the binary prefix load-bearing?  RW with a four-state prefix.

RW fixes a BINARY prefix W in {1,2}^n and asks for n+r+2 forced binary
hard-core symbols with T[u][n] = c.  Here the prefix ranges over ALL of
{0..3}^n (every column word at level n-1 is reachable this way, since the
endpoint-to-column map is a bijection), and the same forced continuation is
run.  Reported per (n, c): the number of four-state prefixes whose forced
continuation is binary hard-core with n+2 consecutive hits (an RW-shaped
full run, r = 0, condition 3 ignored), and the number with n+2 hits ignoring
hard-core.  The heuristic count is 4^n 2^(-1.306 (n+2)) which grows like
2^(0.69 n).  If these are nonzero and growing, any lemma quantified over all
column words (all orbits of the transducer) is false, and a proof of RW must
use the binarity of the whole prefix.

Also reported: the same count restricted to prefixes with exactly m
non-binary symbols, m = 0, 1, 2, to see how fast the count turns on.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/four_state_prefix.py --min 3 --max 9
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def run_len(prefix, target, need):
    """(E-only run length, joint run length) capped at need."""
    n = len(prefix)
    st = Endpoint()
    for s in prefix:
        st.append(s)
    prev = prefix[-1]
    kE = 0
    kJ = 0
    joint_alive = True
    for _ in range(need):
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                break
        st.append(sym)
        if diag[n] != target:
            break
        kE += 1
        if joint_alive:
            if prev == 1 and sym == 1:
                joint_alive = False
            else:
                kJ += 1
        prev = sym
    return kE, kJ


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/four_state_prefix.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        print("# n c  full_joint(n+2 hits, HC)  full_E(n+2 hits)  by #nonbinary symbols m: joint counts  | heuristic 4^n 2^(-1.306(n+2))", file=log)
        for n in range(args.min, args.max + 1):
            need = n + 2
            for c in (2, 3):
                full_joint = 0
                full_E = 0
                by_m = Counter()
                examples = []
                for prefix in product(range(4), repeat=n):
                    kE, kJ = run_len(prefix, c, need)
                    if kE >= need:
                        full_E += 1
                    if kJ >= need:
                        full_joint += 1
                        m = sum(1 for s in prefix if s in (0, 3))
                        by_m[m] += 1
                        if len(examples) < 3:
                            examples.append("".join(map(str, prefix)))
                heur = 4.0 ** n * 2.0 ** (-1.306 * need)
                print(f"{n:2d} {c}  {full_joint:8d}  {full_E:8d}   {dict(sorted(by_m.items()))}  | {heur:9.2f}  examples={examples}", file=log)
                log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()
