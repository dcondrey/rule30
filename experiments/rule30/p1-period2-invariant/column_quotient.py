#!/usr/bin/env python3
"""Does the endpoint map factor through a smaller state alphabet, and does that
lower the growth rate of the reachable column language?

Algebra (exact, printed by --tables).  ``_carry_action(symbol, state)`` reads
the symbol only through ``(a|b)`` and ``a``, where ``a, b`` are its bits, so
symbols 2 and 3 have the identical forward action and ``INVERSE[2] ==
INVERSE[3]``.  Since ``CONE[l][r] = INVERSE[swap(l)][r]`` and ``swap`` sends
``1 -> 2`` and ``3 -> 3``, this gives

    CONE[1] == CONE[3]  as full rows of the table.

Every retained column or diagonal entry enters the next append only as the
LEFT argument of ``CONE``, so the append map factors through the quotient

    q:  0 -> 0,  1 -> 1,  2 -> 2,  3 -> 1

on the retained state.  (The freshly produced values are needed in full inside
a pass, and the appended symbol itself is stored literally, so ``q`` is applied
to the column entries below the last one and to the whole diagonal.)  ``q`` is
therefore a genuine congruence, not an approximation: BFS over ``q``-classes
loses nothing.

Question.  ``RESULTS-CLUSTER-ANATOMY.md`` and ``uc/r1-entropy/state_language``
measure ``|C_u| ~ 1.765^u``, entropy ``0.82`` bits per step against the ``1.0``
of the source.  If ``q`` were the reason the base is below 2, the quotient
count would grow strictly slower and exhaustive census would reach further.

Strong outcome: ``|qC_u|`` grows at a base measurably below ``1.765``.
Kill: the ratio ``|qC_u| / |C_u|`` settles at a constant, so ``q`` is a
constant-factor collapse that leaves the growth rate untouched.
"""
from __future__ import annotations

import argparse
import math
import sys

from psi_kernel import BOUNDARY, CONE, FORWARD, INVERSE, _swap

Q = (0, 1, 2, 1)


def tables() -> None:
    print("FORWARD[symbol][state]:")
    for s in range(4):
        print("  sym", s, FORWARD[s])
    print("INVERSE[symbol][state]:")
    for s in range(4):
        print("  sym", s, INVERSE[s])
    print("BOUNDARY =", BOUNDARY)
    print("CONE[l][r]:")
    for l in range(4):
        print("  l =", l, CONE[l])
    print("\nCONE[1] == CONE[3]:", CONE[1] == CONE[3])
    print("swap:", tuple(_swap(l) for l in range(4)))
    print("\nfibres of l -> CONE[l][r] at fixed r (the merge mechanism):")
    for r in range(4):
        img = [CONE[l][r] for l in range(4)]
        fib = {v: [l for l in range(4) if CONE[l][r] == v] for v in sorted(set(img))}
        print(f"  r={r}: images {img}  distinct {len(set(img))}  fibres {fib}")
    print("\nrows of CONE are permutations (r -> CONE[l][r]):")
    for l in range(4):
        print(f"  l={l}: {list(CONE[l])}  distinct {len(set(CONE[l]))}")


def step(col, dia, sym):
    """One append.  ``col`` has ``L+1`` entries, ``dia`` has ``L``."""
    L = len(col) - 1
    nc = [0] * (L + 1)
    nc[L] = BOUNDARY[sym]
    for i in range(L - 1, -1, -1):
        nc[i] = CONE[col[i + 1]][nc[i + 1]]
    nd = [0] * (L + 1)
    nd[0] = nc[0]
    for i in range(L):
        nd[i + 1] = CONE[dia[i]][nd[i]]
    return tuple(nc) + (sym,), tuple(nd)


def q(t):
    return tuple(Q[x] for x in t)


def qclass(col, dia):
    return q(col[:-1]) + (col[-1],), q(dia)


def start():
    out = []
    for s in (1, 2):
        b = BOUNDARY[s]
        out.append(((b, s), (b,)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--umax", type=int, default=18)
    ap.add_argument("--tables", action="store_true")
    args = ap.parse_args()
    if args.tables:
        tables()
        print()
    cur = set(start())
    print("# BFS over full endpoint states; |qC_u| counts the q-classes among them")
    print(f"{'u':>3} {'|C_u|':>10} {'|qC_u|':>10} {'ratio':>7} {'C base':>8} {'qC base':>8} {'log2':>8}")
    pc = pq = None
    for u in range(1, args.umax + 1):
        if u > 1:
            cur = {step(list(c), list(d), s) for (c, d) in cur for s in (1, 2)}
        C = len(cur)
        Qn = len({qclass(c, d) for (c, d) in cur})
        gc = C / pc if pc else float("nan")
        gq = Qn / pq if pq else float("nan")
        lg = math.log2(gq) if pq else float("nan")
        print(f"{u:>3} {C:>10} {Qn:>10} {Qn / C:>7.4f} {gc:>8.4f} {gq:>8.4f} {lg:>8.4f}")
        sys.stdout.flush()
        pc, pq = C, Qn


if __name__ == "__main__":
    main()
