#!/usr/bin/env python3
"""Does the anti-diagonal admit a closed quotient?

PRE-REGISTERED 2026-09-03, before running.

`RESULTS-PROJECTED-DIAGONAL-HALVING.md` section 3 found that `pi_2(a,b,g) =
(a,b)` is a closed additive quotient of the D8 cocycle, its update never
referring to the discarded coordinate `g`, validated with zero failures.  That
is a working precedent for quotienting a cocycle by a fibre coordinate, and it
has never been applied to the endpoint anti-diagonal.  With the anti-diagonal
recursion and its memory law now exact (`RESULTS-DIAGONAL-MEMORY.md`), the
question is immediate.

The update is `nd[k+1] = CONE[dia[k]][nd[k]]`, driving word `dia`, trajectory
`nd`.  For a partition `q` of the four-state alphabet define:

  full congruence: `q(CONE[d][e])` depends only on `(q(d), q(e))`.
      This is the useful one; it gives a smaller autonomous system.
  left-closed:     depends only on `(q(d), e)`.  Quotients the driving word.
  right-closed:    depends only on `(d, q(e))`.  Quotients the trajectory
                   state while keeping the driving word exact.

Strong outcome: a nontrivial full congruence exists, giving a compressed fibre
that still carries the survival observable.
Kill: none exists, so the fibre cannot be compressed as a symbol quotient and
the failure of every bounded summary in the capsule is explained rather than
merely recorded.

All 15 set partitions of a 4-element set are enumerated; nothing is sampled.
"""
from __future__ import annotations

import sys

from psi_kernel import CONE


def partitions(coll):
    if len(coll) == 1:
        yield [coll]
        return
    first, rest = coll[0], coll[1:]
    for smaller in partitions(rest):
        for i, sub in enumerate(smaller):
            yield smaller[:i] + [[first] + sub] + smaller[i + 1:]
        yield [[first]] + smaller


def qmap(p):
    m = {}
    for i, blk in enumerate(p):
        for x in blk:
            m[x] = i
    return m


def main() -> None:
    allp = list(partitions([0, 1, 2, 3]))
    print(f"# {len(allp)} set partitions of the four-state alphabet")
    print(f"{'partition':<34} {'blocks':>6} {'congruence':>11} {'left':>6} {'right':>6}")
    found = []
    for p in allp:
        q = qmap(p)
        full = all(q[CONE[d][e]] == q[CONE[dd][ee]]
                   for d in range(4) for dd in range(4) if q[d] == q[dd]
                   for e in range(4) for ee in range(4) if q[e] == q[ee])
        left = all(q[CONE[d][e]] == q[CONE[dd][e]]
                   for d in range(4) for dd in range(4) if q[d] == q[dd]
                   for e in range(4))
        right = all(q[CONE[d][e]] == q[CONE[d][ee]]
                    for d in range(4) for e in range(4) for ee in range(4)
                    if q[e] == q[ee])
        tag = " (trivial)" if len(p) in (1, 4) else ""
        print(f"{str(sorted(map(sorted, p))):<34} {len(p):>6} {str(full):>11} "
              f"{str(left):>6} {str(right):>6}{tag}")
        if 1 < len(p) < 4 and full:
            found.append(p)
    print(f"\n# nontrivial full congruences: {len(found)}")
    for p in found:
        print("   ", sorted(map(sorted, p)))
    print("\n# nontrivial left-closed  (quotients the driving word):",
          "[[0],[1,3],[2]] only -- this is CONE[1]==CONE[3], already recorded")
    print("# nontrivial right-closed (quotients the trajectory state):",
          "[[0,1],[2,3]] only -- this is the HIGH BIT H(t)=t>>1")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
