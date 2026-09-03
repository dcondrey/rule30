#!/usr/bin/env python3
"""Two checks behind the actual-right rotated wedge lemma.

1. Cross-check: the finite-type language R13 used by rw_restricted_margin.py
   (bits avoiding the recorded minimal forbidden factors through length 13)
   equals the exact realized right trace language of right_trace_forbidden.py
   for every length up to --max-exact (2^(2n-1) seeds each).

2. Balance of the first E constraint.  For the prefix sets {1,2}^n, HC_n and
   R13_n, count the prefixes whose first forced column has E(T[n][n]) = 0
   (c = 2 side), report the excess over half the set, and the same for the
   first two constraints (E ok at levels 0 and 1, and language ok at level 0
   for the restricted sets).  A bias that is O(sqrt(size)) is what an
   unstructured parity would give; an exact pattern would be a lead.
"""

from __future__ import annotations

import argparse
import math
import sys

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-hardcore")
from psi_kernel import CONE  # noqa: E402
from right_trace_forbidden import realized_language  # noqa: E402
from rw_restricted_margin import FORBIDDEN, allowed, bit_of  # noqa: E402


def words(language: str | None, n: int):
    """Yield (bits, symbols) for all prefixes of length n in the language."""
    forbidden = FORBIDDEN[language] if language else []
    stack = [("", ())]
    while stack:
        bits, syms = stack.pop()
        if len(syms) == n:
            yield bits, syms
            continue
        for e in (1, 2):
            nb = bits + bit_of(e)
            if forbidden and not allowed(nb, forbidden):
                continue
            stack.append((nb, syms + (e,)))


def forced_two(prefix: tuple[int, ...]) -> tuple[list[int], list[int]]:
    n = len(prefix)
    col: list[int] = []
    for u, e in enumerate(prefix):
        new = [0] * (2 * u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, 2 * u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        col = new
    syms, defs = [], []
    for j in range(2):
        u = n + j
        zeros = col.count(0)
        e = 2 if (n + u + zeros) & 1 else 1
        new = [0] * (n + u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, n + u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        cell = new[n + u + 1]
        syms.append(e)
        defs.append(1 ^ (cell >> 1) ^ (cell & 1))
        col = new[: n + u + 1]
    return syms, defs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-exact", type=int, default=11)
    ap.add_argument("--max-bin", type=int, default=18)
    ap.add_argument("--max-r13", type=int, default=36)
    ap.add_argument("--max-hc", type=int, default=24)
    args = ap.parse_args()

    print("## cross-check R13_n against realized_language(n)")
    for n in range(1, args.max_exact + 1):
        exact = realized_language(n)
        mine = {bits for bits, _ in words("R13", n)}
        print(f"n={n:2d} exact={len(exact):5d} R13={len(mine):5d} equal={exact == mine}")
        sys.stdout.flush()

    for language, max_n in ((None, args.max_bin), ("HC", args.max_hc), ("R13", args.max_r13)):
        name = language or "BIN"
        print(f"## balance on {name}: size, #E0=0, excess over half, excess/sqrt(size); "
              f"#(E0=0,E1=0), #(E0=1,E1=1), lang-ok@0 count")
        for n in range(3, max_n + 1):
            size = 0
            e0_zero = 0
            both_zero = 0
            both_one = 0
            lang0 = 0
            forbidden = FORBIDDEN[language] if language else []
            for bits, syms in words(language, n):
                size += 1
                s, d = forced_two(syms)
                if d[0] == 0:
                    e0_zero += 1
                if d[0] == 0 and d[1] == 0:
                    both_zero += 1
                if d[0] == 1 and d[1] == 1:
                    both_one += 1
                if not forbidden or allowed(bits + bit_of(s[0]), forbidden):
                    lang0 += 1
            excess = e0_zero - size / 2
            print(
                f"n={n:2d} size={size:8d} E0=0:{e0_zero:8d} excess={excess:+9.1f} "
                f"({excess / math.sqrt(size):+.2f} sd)  both0={both_zero:7d} both1={both_one:7d} "
                f"(quarter={size / 4:.0f})  lang0={lang0}"
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()
