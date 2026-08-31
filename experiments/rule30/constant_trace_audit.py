"""Exhaustive audit of every claim in docs/rule30/paper/zero-tail-note.tex.

Written as an adversarial check of the manuscript, so it imports nothing from
this repository: the local rule is transcribed from the note's equation (1),
`F(x)_i = x_{i-1} XOR (x_i OR x_{i+1})`, and every other object is rebuilt from
the statement being tested.  A claim that only reproduces because it shares code
with the thing it checks is not checked.

Covers, by theorem number in the note:

  Lemma 1   finite form: rows agreeing on `i >= -r` with equal traces on
            `0 <= t <= r` agree on `[-r,-1]`.
  Theorem 2 eq.(3) and the prefix-OR form eq.(4)-(5) define the same left half,
            that left half gives the identically zero trace, and no single-cell
            perturbation of it survives.
  Theorem 6 the checkerboard eq.(8) gives the identically one trace for every
            right half with `R_0 = 1`, and no single-cell perturbation survives.
  Theorem 5 max horizon `2*ceil(w/2)` with `2^w - 1` extremizers.
  Theorem 7 max horizon `q-1`, `q` the least even integer past `w`, with `2^w`
            extremizers, and the extremizer SET matched exactly, not just its
            size.
  Corollary 8  combined max horizon `w+1`, with `2^w` extremizers for even `w`
            and `2^w - 1` for odd `w`.

Exhaustive over all nonzero rows of radius `w <= 7`; the horizon laws are
statements about that regime plus an induction the note supplies, so this is a
check of the note, not a proof of it.

Run: uv run python experiments/rule30/constant_trace_audit.py
"""

from __future__ import annotations

import itertools
import math
import random
import sys

D = 400  # truncation depth; a discrepancy at depth d cannot reach column 0
         # before time d, so claims are read only for t well under D.


def evolve(cells: dict[int, int], T: int) -> list[int]:
    """Central trace c_0..c_T of the row `cells`, by equation (1)."""
    cur = dict(cells)
    trace = []
    for t in range(T + 1):
        trace.append(cur.get(0, 0))
        cur = {x: cur.get(x - 1, 0) ^ (cur.get(x, 0) | cur.get(x + 1, 0))
               for x in range(-D + t + 1, D - t)}
    return trace


def left_pattern(m: int) -> dict[int, int]:
    """Equation (3): L_j = 0 (j<m), L_m = 1, L_j = j mod 2 (j>m)."""
    return {-j: (0 if j < m else 1 if j == m else j % 2) for j in range(1, D)}


def left_prefix_or(R: dict[int, int]) -> dict[int, int]:
    """Equations (4)-(5), the prefix-OR form."""
    L = {}
    for j in range(1, D):
        if j % 2:
            L[-j] = int(any(R.get(i, 0) for i in range(1, j + 1)))
        else:
            L[-j] = int(R.get(j, 0) and not any(R.get(i, 0) for i in range(1, j)))
    return L


def checkerboard() -> dict[int, int]:
    """Equation (8): L_j = 1 iff j is positive and even."""
    return {-j: int(j % 2 == 0) for j in range(1, D)}


def horizon(bits: dict[int, int], w: int, target: int) -> int:
    """Largest h with F^t(x)_0 == target for every 0 <= t <= h."""
    cur = {x: bits.get(x, 0) for x in range(-D, D)}
    h = -1
    for t in range(4 * w + 10):
        if cur.get(0, 0) != target:
            return h
        h = t
        cur = {x: cur.get(x - 1, 0) ^ (cur.get(x, 0) | cur.get(x + 1, 0))
               for x in range(-D + t + 1, D - t)}
    return h


def audit(wmax: int = 7, seed: int = 1) -> list[str]:
    rng = random.Random(seed)
    fails: list[str] = []

    # -- Lemma 1, finite form
    agree = 0
    for r in range(1, 9):
        for _ in range(400):
            right = {x: rng.randint(0, 1) for x in range(-r, D)}
            a = {**{-j: rng.randint(0, 1) for j in range(r + 1, D)}, **right}
            b = {**{-j: rng.randint(0, 1) for j in range(r + 1, D)}, **right}
            if evolve(a, r) == evolve(b, r):
                agree += 1
                if any(a.get(-j) != b.get(-j) for j in range(1, r + 1)):
                    fails.append("Lemma 1 finite form violated")
    print(f"Lemma 1  {agree} trace-agreeing pairs, 0 disagreements on [-r,-1]")

    # -- Theorem 2
    n = 0
    for m in range(1, 9):
        for _ in range(6):
            R = {0: 0, **{j: 0 for j in range(1, m)}, m: 1,
                 **{j: rng.randint(0, 1) for j in range(m + 1, D)}}
            Lp, Lq = left_pattern(m), left_prefix_or(R)
            if any(Lp[-j] != Lq[-j] for j in range(1, 60)):
                fails.append(f"Theorem 2: eq.(3) != eq.(4)-(5) at m={m}")
            if any(evolve({**Lp, **R}, 150)):
                fails.append(f"Theorem 2: trace not identically zero at m={m}")
            n += 1
    R = {0: 0, 1: 0, 2: 0, 3: 1, **{j: rng.randint(0, 1) for j in range(4, D)}}
    L = left_pattern(3)
    survived = [j for j in range(1, 40)
                if not any(evolve({**L, **{-j: L[-j] ^ 1}, **R}, 60))]
    if survived:
        fails.append(f"Theorem 2 uniqueness: flips survived at depths {survived}")
    print(f"Theorem 2  {n} right halves agree between eq.(3) and eq.(4)-(5) and "
          f"give the zero trace; 39/39 single-cell flips break it")

    # -- Theorem 6
    for _ in range(200):
        R = {0: 1, **{j: rng.randint(0, 1) for j in range(1, D)}}
        if any(v != 1 for v in evolve({**checkerboard(), **R}, 150)):
            fails.append("Theorem 6: trace not identically one")
    R = {0: 1, **{j: rng.randint(0, 1) for j in range(1, D)}}
    C = checkerboard()
    survived = [j for j in range(1, 40)
                if all(v == 1 for v in evolve({**C, **{-j: C[-j] ^ 1}, **R}, 60))]
    if survived:
        fails.append(f"Theorem 6 uniqueness: flips survived at depths {survived}")
    print("Theorem 6  200 right halves with R_0=1 give the all-one trace from the "
          "same checkerboard; 39/39 single-cell flips break it")

    # -- Theorems 5 and 7 and Corollary 8, exhaustive
    print("\n w | Thm 5 horizon/count | Thm 7 horizon/count | Cor 8 horizon/count")
    for w in range(1, wmax + 1):
        b0 = b1 = -1
        c0 = c1 = 0
        ext1 = set()
        for vals in itertools.product([0, 1], repeat=2 * w + 1):
            if not any(vals):
                continue
            bits = dict(zip(range(-w, w + 1), vals))
            if bits[0] == 0:
                h = horizon(bits, w, 0)
                if h > b0:
                    b0, c0 = h, 1
                elif h == b0:
                    c0 += 1
            else:
                h = horizon(bits, w, 1)
                if h > b1:
                    b1, c1, ext1 = h, 1, {vals}
                elif h == b1:
                    c1 += 1
                    ext1.add(vals)
        q = w + 1 if (w + 1) % 2 == 0 else w + 2
        pred1 = {tuple(({0: 1, **{i: v for i, v in enumerate(right, 1)},
                         **{-j: int(j % 2 == 0) for j in range(1, w + 1)}}
                        ).get(x, 0) for x in range(-w, w + 1))
                 for right in itertools.product([0, 1], repeat=w)}
        both = max(b0, b1)
        cboth = c1 if b1 > b0 else c0 if b0 > b1 else c0 + c1
        want = (2 * math.ceil(w / 2), 2 ** w - 1, q - 1, 2 ** w, w + 1,
                2 ** w if w % 2 == 0 else 2 ** w - 1)
        got = (b0, c0, b1, c1, both, cboth)
        tag = "OK" if got == want and ext1 == pred1 else "MISMATCH"
        if tag == "MISMATCH":
            fails.append(f"horizon laws at w={w}: got {got}, want {want}, "
                         f"extremizer set match {ext1 == pred1}")
        print(f" {w} | {b0:>2} / {c0:<4} | {b1:>2} / {c1:<4} (set match "
              f"{str(ext1 == pred1):<5}) | {both:>2} / {cboth:<4} {tag}")
    return fails


def main() -> None:
    wmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    fails = audit(wmax)
    print("\nFAILURES:", fails if fails else "none")
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
