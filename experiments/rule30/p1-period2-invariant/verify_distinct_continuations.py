#!/usr/bin/env python3
"""Independent verification of D_k, the distinct-surviving-continuation count.

D_k = number of DISTINCT surviving continuation prefixes of length k+1
(prefix includes the junction symbol = last symbol of the source word).
This is the right object for an existence theorem: a witness exists iff at
least one distinct continuation survives, regardless of how many source
words map onto it. The word count S_k overcounts, because leading source
symbols are free (many words share one continuation).

Two independent code paths, by DIFFERENT forcing rules:
  A: late_pull_diagonal_sat.literal_extension -- searches all four values,
     keeps the unique one whose edge last cell equals the tail.
  B: flip_pairing.forced_orbit (psi_kernel.Endpoint) -- tries only {1,2},
     keeps the unique one with H(dia[n]) == 1.
These are genuinely different rules. If both yield identical D_k, that is
real cross-validation, not a restatement.

Checks performed (per the verification plan):
  1. A vs B agreement on D_k, exactly.
  2. Fibonacci phase: D_k == F_{k+3} (= 2,3,5,8,13,21) for k < 6, i.e. the
     forced map is SURJECTIVE onto the full hard-core shift there.
  3. Stability in n: is D_k(n) independent of n for fixed k?
  4. True maximum post-Fibonacci ratio r_k = D_{k+1}/D_k over ALL k and
     both tails (not just adjacent/cherry-picked pairs).
Throwaway verification script; not wired into any pipeline.
"""
from __future__ import annotations

import argparse
from itertools import product

from late_pull_diagonal_sat import literal_extension
from flip_pairing import forced_orbit


def fib_hardcore(k: int) -> int:
    """Number of hard-core (no '11') strings of length k+1 over {1,2}."""
    a, b = 1, 2  # counts for length 0 (empty=1) and length 1 (2)
    for _ in range(k + 1):
        a, b = b, a + b
    return a


def legal_step(prev: int, value: int) -> bool:
    return value in (1, 2) and not (prev == 1 and value == 1)


def distinct_counts(n: int, tail: int, rows: int, path: str):
    """D_k via path 'A' (literal_extension) or 'B' (forced_orbit)."""
    sets: list[set] = [set() for _ in range(rows + 2)]
    for word in product((1, 2), repeat=n):
        if path == "A":
            seq = literal_extension(word, tail, rows)
        else:
            _key, syms, cells, _hcs = forced_orbit(word, n, rows)
            # forced_orbit's own survival predicate is (hard-core AND cell==tail);
            # emit its symbol stream and let the shared legality walk below apply,
            # additionally cutting where its forced cell misses the tail.
            seq = []
            for j, s in enumerate(syms):
                seq.append(s)
                if cells[j] != tail:
                    seq[-1] = 0  # force death here, same as an illegal value
                    break
        prev = word[-1]
        pref = [prev]
        sets[0].add(tuple(pref))
        for value in seq:
            if not legal_step(prev, value):
                break
            pref.append(value)
            prev = value
            sets[len(pref) - 1].add(tuple(pref))
    return [len(s) for s in sets]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[12, 14, 16])
    ap.add_argument("--skip-b-above", type=int, default=99)
    args = ap.parse_args()

    table = {}
    print("=" * 72)
    print("CHECK 1: path A (literal_extension) vs path B (forced_orbit)")
    for n in args.ns:
        rows = n + 4
        for tail in (2, 3):
            da = distinct_counts(n, tail, rows, "A")
            trim_a = da[: (max(k for k in range(len(da)) if da[k] > 0) + 2)]
            table[(n, tail)] = trim_a
            if n <= args.skip_b_above:
                db = distinct_counts(n, tail, rows, "B")
                trim_b = db[: len(trim_a)]
                ok = trim_a == trim_b
                print(f"  n={n} c={tail}: A={trim_a}")
                print(f"            B={trim_b}   AGREE={ok}")
                if not ok:
                    print("            *** MISMATCH ***")
            else:
                print(f"  n={n} c={tail}: A={trim_a}  (B skipped)")

    print()
    print("=" * 72)
    print("CHECK 2: Fibonacci phase  D_k == F (2,3,5,8,13,21) for k < 6")
    expected = [fib_hardcore(k) for k in range(6)]
    print(f"  expected hard-core counts for k=0..5: {expected}")
    all_fib = True
    for (n, tail), d in sorted(table.items()):
        got = d[:6]
        ok = got == expected[: len(got)]
        all_fib &= ok
        print(f"  n={n} c={tail}: {got}  {'OK' if ok else '*** DEPARTS ***'}")
    print(f"  => Fibonacci/surjectivity phase {'HOLDS' if all_fib else 'FAILS'}")

    print()
    print("=" * 72)
    print("CHECK 3: stability of D_k in n (fixed k, varying n)")
    maxlen = max(len(d) for d in table.values())
    for tail in (2, 3):
        print(f"  tail c={tail}:")
        for k in range(maxlen):
            vals = [(n, table[(n, tail)][k]) for n in args.ns
                    if (n, tail) in table and k < len(table[(n, tail)])]
            if len(vals) >= 2:
                stable = len({v for _, v in vals}) == 1
                print(f"    k={k:2d}: {[f'n={n}:{v}' for n, v in vals]}"
                      f"   {'stable' if stable else 'varies with n'}")

    print()
    print("=" * 72)
    print("CHECK 4: TRUE max post-Fibonacci ratio r_k = D_(k+1)/D_k")
    worst = []
    for (n, tail), d in sorted(table.items()):
        last = max(k for k in range(len(d)) if d[k] > 0)
        rs = []
        for k in range(6, last + 1):
            if d[k] > 0:
                rs.append((d[k + 1] / d[k] if k + 1 < len(d) else 0.0, k))
        if rs:
            mx = max(rs)
            worst.append((mx[0], n, tail, mx[1]))
            print(f"  n={n} c={tail}: ratios k>=6 = "
                  f"{[round(r, 3) for r, _ in rs]}   max={mx[0]:.3f} at k={mx[1]}")
    if worst:
        worst.sort(reverse=True)
        gm = worst[0][0]
        print(f"  => TRUE max over all (n,c,k>=6) = {gm:.4f} "
              f"at n={worst[0][1]} c={worst[0][2]} k={worst[0][3]}")
        print(f"  => strict contraction (<1) {'HOLDS' if gm < 1 else 'FAILS'}")


if __name__ == "__main__":
    main()
