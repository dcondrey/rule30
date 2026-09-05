#!/usr/bin/env python3
"""Minimal Moore automaton of the k-fold column composite.

The k-fold composite reads the three-letter quotient word of column u-k and
writes column u.  Its natural state is the row segment
(x_{u-k+1}(d), ..., x_u(d)) in (Z_2^2)^k, 4^k states.  The question is whether
Nerode equivalence collapses that state space (bounded coordinates) or not.

Update (simultaneous, from BRIEF section 2): with input letter l in {t, s, ts}
    x_1' = l . x_1,    x_{i+1}' = lam(cell(x_i)) . x_{i+1}.
Output: the cell of x_k (4 symbols), or its quotient letter (3 symbols).

Nerode classes are computed by Moore partition refinement.  We also report the
number of refinement rounds, which is the length of the longest input needed
to separate two inequivalent segments.
"""

from __future__ import annotations

import sys
from itertools import product

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from d8_kernel import LAM, S, T10, TS, act, cell_of  # noqa: E402

LETTERS = (T10, S, TS)


def step(seg: tuple, letter) -> tuple:
    out = [act(letter, seg[0])]
    for i in range(1, len(seg)):
        out.append(act(LAM[cell_of(seg[i - 1])], seg[i]))
    return tuple(out)


def quotient_letter(x) -> int:
    c = cell_of(x)
    return {1: 0, 3: 0, 0: 1, 2: 2}[c]


def nerode(k: int, output) -> tuple[int, int]:
    states = list(product(product((0, 1), repeat=2), repeat=k))
    succ = {s: [step(s, l) for l in LETTERS] for s in states}
    cls = {s: output(s[-1]) for s in states}
    rounds = 0
    while True:
        sig = {s: (cls[s], tuple(cls[t] for t in succ[s])) for s in states}
        relabel = {}
        new = {}
        for s in states:
            new[s] = relabel.setdefault(sig[s], len(relabel))
        if len(set(new.values())) == len(set(cls.values())):
            return len(set(new.values())), rounds
        cls = new
        rounds += 1


def main() -> None:
    print(" k   4^k   classes(cell out)  rounds   classes(quotient out)  rounds")
    for k in range(1, 8):
        c1, r1 = nerode(k, cell_of)
        c2, r2 = nerode(k, quotient_letter)
        print(f"{k:2d} {4**k:6d} {c1:10d} {r1:12d} {c2:16d} {r2:10d}")


if __name__ == "__main__":
    main()
