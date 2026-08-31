"""p=2 stroboscopic obligation: the forced LEFT half of a 2-periodic centre trace.

Row 31 reduces eventual p-periodicity to: some nonzero finite row y with
Tr_0(y) = Tr_0(F^p(y)).  For p=2 that says exactly: the trace of y is
2-periodic from t=0.  The 2-periodic words are 0^inf, 1^inf, (01)^inf, (10)^inf;
the two constant cases are closed (rows 25, 26).  So the whole p=2 obligation is

    no nonzero finite row has centre trace (01)^inf or (10)^inf.

Given the trace c and the right half R = (a(0,1), a(0,2), ...), the quarter
plane x>=1 evolves autonomously (its left input at x=1 is the known column 0),
and the left half is then forced cell by cell by left permutivity:

    a(t, x-1) = a(t+1, x) XOR (a(t, x) OR a(t, x+1)).

This script computes that forced left half exactly and looks for a finite-state
description of the map R -> L.

Stdlib only.  uv run python left_half_transducer.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

import rule30 as r30  # noqa: E402  (repo shared substrate, read-only)


def rule(rule_num: int, l: int, m: int, rr: int) -> int:
    return (rule_num >> (l * 4 + m * 2 + rr)) & 1


def forced_left_half(trace: list[int], right: list[int], depth: int,
                     rule_num: int = 30) -> list[int]:
    """L[k] = a(0,-k) for k = 1..depth, forced by `trace` and right half `right`.

    trace  : c_0 .. c_T with T >= depth (c_t = a(t,0))
    right  : R_1 .. R_M, a(0,j) for j>=1, zero beyond
    Returns [L_1, ..., L_depth].
    """
    T = depth + 1
    assert len(trace) >= T + 1
    # width of right region needed: a(t,1) at t<=T needs R up to T+1
    W = T + 2
    # grid[t][x] for x in 0..W, index x directly
    grid = [[0] * (W + 1) for _ in range(T + 1)]
    for x in range(1, W + 1):
        grid[0][x] = right[x - 1] if x - 1 < len(right) else 0
    for t in range(T + 1):
        grid[t][0] = trace[t]
    for t in range(T):
        for x in range(1, W):
            grid[t + 1][x] = rule(rule_num, grid[t][x - 1], grid[t][x], grid[t][x + 1])
    # leftward: left[k][t] = a(t,-k), valid for t <= T-k
    left = [[0] * (T + 1) for _ in range(depth + 1)]
    for t in range(T + 1):
        left[0][t] = grid[t][0]

    for k in range(1, depth + 1):
        for t in range(0, T - k + 1):
            # a(t,-k) from a(t+1,-k+1), a(t,-k+1), a(t,-k+2)
            up = left[k - 1][t + 1]
            mid = left[k - 1][t]
            rgt = left[k - 2][t] if k >= 2 else grid[t][1]
            # invert rule in the leftmost argument: a(t,-k) = f^{-1}
            # rule 30: up = a(t,-k) XOR (mid OR rgt)  -> a(t,-k) = up XOR (mid OR rgt)
            # rule 90: up = a(t,-k) XOR rgt          -> a(t,-k) = up XOR rgt
            if rule_num == 30:
                left[k][t] = up ^ (mid | rgt)
            elif rule_num == 90:
                left[k][t] = up ^ rgt
            else:
                # generic left-permutive inversion by search
                for b in (0, 1):
                    if rule(rule_num, b, mid, rgt) == up:
                        left[k][t] = b
                        break
    return [left[k][0] for k in range(1, depth + 1)]


def selfcheck() -> None:
    """Round-trip: take a genuine finite row, read its trace, re-derive its left
    half from (trace, right half), and require an exact match."""
    import random

    rng = random.Random(7)
    for _ in range(200):
        w = rng.randint(1, 6)
        cells = {x: rng.randint(0, 1) for x in range(-w, w + 1)}
        if not any(cells.values()):
            continue
        depth = 12
        n = depth + 4
        rows = r30.simulate_seed(cells, n + 2)
        trace = [rows[t].get(0, 0) for t in range(n + 2)]
        right = [cells.get(j, 0) for j in range(1, 40)]
        L = forced_left_half(trace, right, depth)
        want = [cells.get(-k, 0) for k in range(1, depth + 1)]
        assert L == want, (cells, L, want)
    print("selfcheck: 200 random finite rows round-trip exactly (rule 30)")


def longest_zero_run(L: list[int]) -> int:
    best = cur = 0
    for b in L:
        cur = 0 if b else cur + 1
        best = max(best, cur)
    return best


def eventually_periodic_within(L: list[int], max_p: int = 40) -> str:
    """Smallest (preperiod, period) explaining the tail of L, or 'none<=max_p'."""
    n = len(L)
    for p in range(1, max_p + 1):
        for pre in range(0, n - 4 * p):
            if all(L[i] == L[i + p] for i in range(pre, n - p)):
                return f"pre={pre},p={p}"
    return f"none<= {max_p}"


def survey(rule_num: int, depth: int, radius: int) -> None:
    T = depth + 4
    for phase in (0, 1):
        trace = [(t + phase) % 2 for t in range(T + 2)]
        name = "(01)^inf" if phase == 0 else "(10)^inf"
        ones = zruns = 0
        per = {}
        n = 0
        for bits in range(1 << radius):
            right = [(bits >> j) & 1 for j in range(radius)]
            L = forced_left_half(trace, right, depth, rule_num)
            n += 1
            ones += sum(L)
            zruns = max(zruns, longest_zero_run(L))
            k = eventually_periodic_within(L)
            per[k] = per.get(k, 0) + 1
        print(f"rule {rule_num}, trace {name}, depth {depth}, all {n} right halves "
              f"R_1..R_{radius} (zero beyond):")
        print(f"    mean density of ones in the forced left half = {ones / (n * depth):.4f}")
        print(f"    longest run of zeros anywhere in any forced left half = {zruns}")
        print(f"    eventual-periodicity of the forced left half within the window: {per}")


if __name__ == "__main__":
    selfcheck()
    depth = 60
    T = depth + 4
    for phase in (0, 1):
        trace = [(t + phase) % 2 for t in range(T + 2)]
        print(f"\n=== rule 30, trace ({'01' if phase == 0 else '10'})^inf, "
              f"forced left halves L_1..L_60 ===")
        for right in ([0], [1], [1, 0, 1], [0, 1], [1, 1], [1, 1, 1], [0, 0, 1]):
            L = forced_left_half(trace, right, depth)
            print(f"R={''.join(map(str,right)):>6}  L=" + "".join(map(str, L)))

    print("\n=== MEASUREMENT: is there a row-25-style invariant class for the "
          "nonconstant 2-periodic traces? ===")
    print("(row 25's forced left half for the ZERO trace is the checkerboard "
          "L_k = k mod 2 beyond one index: an eventually periodic word with "
          "period 2 and no zero run longer than 1.)")
    survey(30, 200, 12)
    print("\n=== Rule 90 comparison, same computation ===")
    survey(90, 200, 12)
