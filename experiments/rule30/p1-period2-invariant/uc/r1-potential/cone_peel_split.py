#!/usr/bin/env python3
"""Verify the cone/peel split of the hit condition, both directions.

Claims checked exhaustively (all binary W, n in a range, both c):

 (S1) Light cone: T[u][d] depends only on e_j with j >= ceil((u-d-1)/2).
      Checked by flipping every source bit e_j with j < ceil((u-d-1)/2)
      on the full triangle of the binary word W + (forced continuation)
      and confirming the cell is unchanged when the later symbols are held.
 (S2) Two-sided equivalence at every column u >= n on the forced orbit,
      whether or not the run has already died:
        T[u+1][n] == c   <=>   T[u+1][0] == BU_c(peel_u)[0]
      where peel_u = (T[u][0], ..., T[u][n-1]) and BU_c is the bottom-up
      map of peel_orbit.py.  (The forced symbol e_{u+1} is always applied;
      hard-core is not part of this identity.)
 (S3) Along a hit run, peel_{n+j} = BU_c^j(peel_n) (re-check of peel_orbit).

    cd .../p1-period2-invariant && uv run python uc/r1-potential/cone_peel_split.py
"""

from __future__ import annotations

import argparse
import sys
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import Column, cell, forced_step, hf, letter, transduce  # noqa: E402
from peel_orbit import bu  # noqa: E402


def full_triangle(word: tuple[int, ...]) -> list[list[int]]:
    """cols[u][i] = T[u][-u-1+i] for i in 0..2u+1 (i=0 is e_u)."""
    cols: list[list[int]] = []
    prev: list[int] = []
    for u, e in enumerate(word):
        h, f = hf(e ^ 3)
        out = [e, cell(h, f)]
        if u > 0:
            for t in prev:  # letters of column u-1 at depths -u .. u-1
                a, b = letter(t)
                h, f = h ^ 1 ^ a, f ^ (h & b)
                out.append(cell(h, f))
        cols.append(out)
        prev = out
    return cols


def T(cols, u: int, d: int) -> int:
    return cols[u][d + u + 1]


def forced_word(source: tuple[int, ...], target: int, steps: int) -> tuple[list[int], list[bool]]:
    """Forced continuation of length ``steps`` (ignores death; always forces H)."""
    n = len(source)
    # column n-1 window from the full triangle
    cols = full_triangle(source)
    col = Column(n - 1, n, source[-1], [T(cols, n - 1, d) for d in range(-(n - 1), n)] + [None])  # type: ignore
    word = list(source)
    hits = []
    for _ in range(steps):
        e, nxt = forced_step(col)
        word.append(e)
        hits.append(nxt.states[-1] == target)
        col = nxt
    return word, hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=4)
    ap.add_argument("--max-n", type=int, default=11)
    ap.add_argument("--log", default="uc/r1-potential/cone_peel_split.log")
    args = ap.parse_args()
    s1 = s2 = s3 = 0
    with open(args.log, "w") as log:
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                for source in product((1, 2), repeat=n):
                    steps = n + 3
                    word, hits = forced_word(source, target, steps)
                    cols = full_triangle(tuple(word))
                    L = len(word)
                    # (S1) light cone, cells with d <= n and u <= L-1
                    for j in range(n):
                        flipped = list(word)
                        flipped[j] = 3 - flipped[j]
                        cols2 = full_triangle(tuple(flipped))
                        for u in range(j + 1, L):
                            for d in range(-u - 1, min(u, n) + 1):
                                if (u - d - 1 + 1) // 2 > j:  # ceil((u-d-1)/2) > j
                                    assert T(cols, u, d) == T(cols2, u, d), (source, target, j, u, d)
                                    s1 += 1
                    # (S2) equivalence at every forced column
                    for u in range(n, L - 1):
                        peel_u = tuple(T(cols, u, d) for d in range(n))
                        pred = bu(peel_u, target)[0]
                        lhs = T(cols, u + 1, n) == target
                        rhs = T(cols, u + 1, 0) == pred
                        assert lhs == rhs, (source, target, u, lhs, rhs)
                        s2 += 1
                    # (S3) autonomy along the run
                    q = tuple(T(cols, n, d) for d in range(n))
                    u = n
                    if hits[0]:
                        while u + 1 < L and hits[u + 1 - n]:
                            q = bu(q, target)
                            actual = tuple(T(cols, u + 1, d) for d in range(n))
                            assert actual == q, (source, target, u)
                            s3 += 1
                            u += 1
                print(f"n={n} c={target}: S1 cells={s1} S2 columns={s2} S3 peels={s3}", file=log)
                log.flush()
        print(f"ALL PASS: light-cone cells {s1}, hit<=>target equivalences {s2}, autonomous peel steps {s3}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()
