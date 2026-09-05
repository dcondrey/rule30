#!/usr/bin/env python3
"""The period-2 forced-continuation census, kernel-parameterized, for the Rule
90 soundness control. Self-contained (imports only r90_kernel, no p1 imports).

Fresh reimplementation of continuation_image_analysis.full_continuations /
late_pull_diagonal_sat.literal_extension / constant_tail_scale.append_dependency_edge,
so Control 2 (Rule 30 reproduction) is an independent check of the harness.

Run: python3 r90_census.py control2      # reproduce Rule 30 gamma checkpoints
     python3 r90_census.py grid N0 N1     # 4 Rule 90 kernels, c in {2,3}, n in [N0,N1] even
     python3 r90_census.py grid_tails N0 N1  # K3/K4 across all tails c in {0,1,2,3}
"""
from __future__ import annotations

import sys
from itertools import product

from r90_kernel import (
    KERNELS,
    RULE90_KERNELS,
    append_dependency_edge,
    cone_algebra,
)


def literal_extension(cone_local, boundary, word, tail, rows):
    endpoint = []
    edge = ()
    for value in (0,) * len(word) + tuple(word):
        edge = append_dependency_edge(
            cone_local, boundary, edge, endpoint[-1] if endpoint else None, value
        )
        endpoint.append(value)
    extension = []
    for _ in range(rows):
        candidates = []
        for value in range(4):
            following = append_dependency_edge(
                cone_local, boundary, edge, endpoint[-1], value
            )
            if following[-1] == tail:
                candidates.append((value, following))
        # Forced-continuation uniqueness (pre-flight-verified for every kernel).
        assert len(candidates) == 1, (
            f"forced-continuation NOT unique: {len(candidates)} candidates"
        )
        value, edge = candidates[0]
        endpoint.append(value)
        extension.append(value)
    return tuple(extension)


def survived_length(cont, prev_last_symbol):
    """First row violating hard-core (value not in {1,2}, or 11 across junction)."""
    prev = prev_last_symbol
    for i, v in enumerate(cont):
        if v not in (1, 2) or (prev == 1 and v == 1):
            return i
        prev = v
    return len(cont)


def census(forward, n, tail, residue=0):
    """Return (rows, max_survival, gamma, survival_distribution)."""
    _, boundary, cone_local = cone_algebra(forward)
    target = n + residue
    rows = target + 2
    max_survival = 0
    dist = {}
    for w in product((1, 2), repeat=n):
        cont = literal_extension(cone_local, boundary, w, tail, rows)
        s = survived_length(cont, w[-1])
        if s > max_survival:
            max_survival = s
        dist[s] = dist.get(s, 0) + 1
    return rows, max_survival, rows - max_survival, dist


def run_control2(ns=(8, 10, 12, 14)):
    """Reproduce published Rule 30 gamma: c=2 -> 7,7,5,6 ; c=3 -> 4,5,6,8."""
    expected = {2: {8: 7, 10: 7, 12: 5, 14: 6}, 3: {8: 4, 10: 5, 12: 6, 14: 8}}
    print("=== Control 2: Rule 30 harness reproduction (fresh code) ===")
    all_ok = True
    for tail in (2, 3):
        for n in ns:
            rows, msr, gamma, _ = census(KERNELS["R30"], n, tail)
            exp = expected[tail].get(n)
            ok = exp is None or gamma == exp
            all_ok = all_ok and ok
            print(
                f"  R30 c={tail} n={n:2d}: max_survival={msr:2d} rows={rows:2d} "
                f"gamma={gamma:2d}  expected={exp}  {'OK' if ok else 'MISMATCH'}"
            )
    print(f"  Control 2 verdict: {'ALL 8 CHECKPOINTS PASS' if all_ok else 'FAILED'}")
    return all_ok


def run_grid(n0, n1, tails=(2, 3), kernels=None):
    kernels = kernels or (["R30"] + RULE90_KERNELS)
    ns = range(n0, n1 + 1, 2)
    for tail in tails:
        print(f"\n=== grid tail c={tail} ===")
        header = "n   " + "  ".join(f"{k:>13s}" for k in kernels)
        print(header)
        for n in ns:
            cells = []
            for k in kernels:
                rows, msr, gamma, _ = census(KERNELS[k], n, tail)
                cells.append(f"msr{msr:2d}/g{gamma:2d}")
            print(f"{n:2d}  " + "  ".join(f"{c:>13s}" for c in cells))
            sys.stdout.flush()


def run_grid_tails(n0, n1, kernels=("K3(c^b,d^a)", "K4(c^b,d^c)")):
    """K3/K4 across all tails (collapse absent -> tail choice not vacuous)."""
    ns = range(n0, n1 + 1, 2)
    for k in kernels:
        print(f"\n=== {k} across tails c in 0,1,2,3 ===")
        print("n   " + "  ".join(f"c={c}:msr/g" for c in range(4)))
        for n in ns:
            cells = []
            for c in range(4):
                rows, msr, gamma, _ = census(KERNELS[k], n, c)
                cells.append(f"{msr:2d}/{gamma:2d}")
            print(f"{n:2d}  " + "  ".join(f"{x:>9s}" for x in cells))
            sys.stdout.flush()


def run_distribution(n, tail, kernels=None):
    """Survival-depth distribution shape, one n, for the SHAPE comparison."""
    kernels = kernels or (["R30"] + RULE90_KERNELS)
    print(f"\n=== survival-depth distribution n={n} c={tail} ===")
    for k in kernels:
        rows, msr, gamma, dist = census(KERNELS[k], n, tail)
        items = " ".join(f"{s}:{dist[s]}" for s in sorted(dist))
        print(f"  {k:12s} rows={rows} max_survival={msr} gamma={gamma}")
        print(f"      survival->count: {items}")


def main():
    if len(sys.argv) < 2:
        run_control2()
        return
    cmd = sys.argv[1]
    if cmd == "control2":
        run_control2()
    elif cmd == "grid":
        n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        n1 = int(sys.argv[3]) if len(sys.argv) > 3 else 14
        run_grid(n0, n1)
    elif cmd == "grid_tails":
        n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        n1 = int(sys.argv[3]) if len(sys.argv) > 3 else 14
        run_grid_tails(n0, n1)
    elif cmd == "dist":
        n = int(sys.argv[2])
        tail = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        run_distribution(n, tail)
    else:
        raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
