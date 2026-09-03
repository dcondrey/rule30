#!/usr/bin/env python3
"""Exact negative certificate for the subinvariant-weight LP of `rw_subinvariant_lp.py`.

The LP returns `t = 0`: no nonnegative position-indexed weight strictly decreases
along every RW survivor edge.  A returned optimum is not a proof, so this script
produces the Farkas witness and verifies it in exact integer arithmetic.

Infeasibility of `{ z >= 0, D z <= -t, t > 0 }` is certified by a nonnegative
integer multiset `y` of survivor edges with

    sum_i y_i * D_i  >=  0   componentwise,     sum_i y_i  >=  1.

Given such a `y`, any `z >= 0` has `sum_i y_i (D_i . z) >= 0`, so some edge has
`D_i . z >= 0`: the weight does not decrease there.  Coefficient magnitude is
irrelevant, so this kills the whole nonnegative class at once, exactly as the
locality-1..4 refutation in `RESULTS.md` section 4 does for its own class.

The edge set is first shrunk greedily to a core that still forces `t = 0`, so
the printed certificate is small enough to check by hand.
"""

from __future__ import annotations

import argparse
from functools import reduce
from math import gcd

import numpy as np
from scipy.optimize import linprog

from rw_subinvariant_lp import survivor_edges

TOL = 1e-9


def best_t(rows: list[tuple[int, ...]], dim: int) -> float:
    A = np.zeros((len(rows), dim + 1))
    A[:, :dim] = np.array(rows, dtype=float)
    A[:, dim] = 1.0
    obj = np.zeros(dim + 1)
    obj[dim] = -1.0
    res = linprog(
        obj,
        A_ub=A,
        b_ub=np.zeros(len(rows)),
        bounds=[(0.0, 1.0)] * dim + [(0.0, None)],
        method="highs",
    )
    return float(res.x[dim]) if res.success else float("inf")


def shrink(rows: list[tuple[int, ...]], dim: int) -> list[tuple[int, ...]]:
    core = list(rows)
    index = 0
    while index < len(core):
        trial = core[:index] + core[index + 1 :]
        if trial and best_t(trial, dim) <= TOL:
            core = trial
        else:
            index += 1
    return core


def certificate(core: list[tuple[int, ...]], dim: int, cap: int = 10**6):
    """Smallest nonnegative INTEGER multiset over ``core`` with nonnegative aggregate.

    Solved as a MIP rather than rationalised from an LP vertex: rounding a
    floating vertex produced aggregates off by 19 digits at ``K=40``, which is a
    rounding artefact and not a certificate.  Integrality here is what makes the
    exact check in ``verify`` meaningful.
    """
    D = np.array(core, dtype=float)
    rows = np.vstack([-D.T, -np.ones((1, len(core)))])
    rhs = np.concatenate([np.zeros(dim), [-1.0]])
    res = linprog(
        np.ones(len(core)),
        A_ub=rows,
        b_ub=rhs,
        bounds=[(0.0, float(cap))] * len(core),
        integrality=np.ones(len(core)),
        method="highs",
    )
    if not res.success:
        return None
    ints = [int(round(v)) for v in res.x]
    divisor = reduce(gcd, ints)
    if divisor > 1:
        ints = [i // divisor for i in ints]
    return ints


def verify(core: list[tuple[int, ...]], ints: list[int], dim: int) -> tuple[bool, list[int]]:
    total = [0] * dim
    for multiplicity, row in zip(ints, core):
        if multiplicity:
            for j, value in enumerate(row):
                total[j] += multiplicity * value
    return (sum(ints) >= 1 and all(v >= 0 for v in total)), total


def arm4_certificate(n: int, c: int, K: int, cap: int = 10**5):
    """Negative certificate for the contrast + sublanguage arm.

    That arm allows signed coefficients, requires ``log w >= 0`` only on the
    survivor states of the census, and quotients out the pure-length direction.
    Infeasibility of ``{ D x <= -t 1, S x >= 0, E x = 0, t > 0 }`` is certified,
    by Motzkin transposition, by

        y >= 0 over edges,  u >= 0 over survivor states,  v free over blocks,
        D^T y - S^T u + E^T v = 0,   sum y >= 1.

    Then for any admissible ``x``, ``sum y (D_i . x) = sum u (S_j . x) >= 0``, so
    some survivor edge fails to decrease.  ``E^T v`` says the aggregate is
    allowed to be a pure-length vector, constant within each position block,
    which is exactly the direction arm 4 excludes.
    """
    diffs, _, states = survivor_edges(n, c, n + 4, K)
    dim = 4 * K + 4
    D = np.array(diffs, dtype=float)
    S = np.array(states, dtype=float)
    blocks = K + 1
    ny, nu, nv = len(diffs), len(states), blocks
    E = np.zeros((blocks, dim))
    for k in range(blocks):
        E[k, 4 * k : 4 * k + 4] = 1.0
    # variables: y (ny), u (nu), v (nv)
    A_eq = np.hstack([D.T, -S.T, E.T])
    b_eq = np.zeros(dim)
    A_ub = np.zeros((1, ny + nu + nv))
    A_ub[0, :ny] = -1.0
    res = linprog(
        np.concatenate([np.ones(ny), np.zeros(nu + nv)]),
        A_ub=A_ub,
        b_ub=[-1.0],
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0.0, float(cap))] * (ny + nu) + [(-float(cap), float(cap))] * nv,
        integrality=np.ones(ny + nu + nv),
        method="highs",
    )
    if not res.success:
        return None
    values = [int(round(v)) for v in res.x]
    y, u, v = values[:ny], values[ny : ny + nu], values[ny + nu :]
    total = [0] * dim
    for mult, row in zip(y, diffs):
        for j, value in enumerate(row):
            total[j] += mult * value
    for mult, row in zip(u, states):
        for j, value in enumerate(row):
            total[j] -= mult * value
    for k in range(blocks):
        for j in range(4 * k, 4 * k + 4):
            total[j] += v[k]
    ok = sum(y) >= 1 and all(value == 0 for value in total)
    return ok, sum(y), sum(1 for value in y if value), sum(1 for value in u if value), v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--no-shrink", action="store_true")
    ap.add_argument("--arm4", action="store_true",
                    help="certify the contrast + sublanguage arm instead of arm 1")
    args = ap.parse_args()

    dim = 4 * args.K + 4
    if args.arm4:
        for c in (2, 3):
            out = arm4_certificate(args.n, c, args.K)
            print(f"\n## arm 4  n={args.n} c={c} K={args.K}")
            if out is None:
                print("no certificate found")
                continue
            ok, mass, ysup, usup, v = out
            print(f"verified={ok}  sum y={mass}  edge support={ysup}  state support={usup}")
            print(f"block multipliers v={v}")
        return
    for c in (2, 3):
        rows, _, _ = survivor_edges(args.n, c, args.n + 4, args.K)
        t_full = best_t(rows, dim)
        print(f"\n## n={args.n} c={c} K={args.K}: {len(rows)} survivor edges, optimal t={t_full:.2e}")
        if t_full > TOL:
            print("LP feasible with t > 0; no negative certificate exists, read alpha_hat instead")
            continue
        core = rows if args.no_shrink else shrink(rows, dim)
        ints = certificate(core, dim)
        if ints is None:
            print("no Farkas certificate found; the LP result stands alone")
            continue
        ok, total = verify(core, ints, dim)
        support = [(m, row) for m, row in zip(ints, core) if m]
        print(f"core edges={len(core)}  certificate support={len(support)}  verified={ok}")
        print(f"aggregate (must be componentwise >= 0): {total}")
        for m, row in support:
            print(f"  x{m:>4} : {list(row)}")


if __name__ == "__main__":
    main()
