#!/usr/bin/env python3
"""The autonomous peel map BU_c and the transient of its top row.

Bottom-up rule (inverse of phi in its right argument): with
G(l, y) = the r such that phi(l, r) = y,

    BU_c(p)[d] = G(p[d], BU_c(p)[d+1]),  BU_c(p)[n] = c,  d = n-1 .. 0.

In a hit run (T[u][n] = c for u = n .. n+k-1) the peel parts satisfy
peel_{u+1} = BU_c(peel_u), so the peel evolves autonomously and the cone part
of every column must reproduce the top peel cell T[u][0] = BU_c^{u-n}(peel_n)[0].

This script measures, for the autonomous orbit q_j = BU_c^j(q_0):
  (a) the eventual period of each row d of q_j (as a sequence in j), and the
      transient t_d after which the row is periodic, on random and exhaustive
      words q_0 in {0..3}^n (W-free, 4^n words);
  (b) for real prefixes W, the actual run length k(W) against t_0 (top row).

    cd .../p1-period2-invariant && uv run python uc/r1-potential/peel_orbit.py
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import cell, forced_orbit, hf  # noqa: E402


def G(l: int, y: int) -> int:
    hy, ey = hf(y)
    hr = hy ^ 1 ^ (1 if l == 0 else 0)
    er = ey ^ (hr & (1 if (l & 1) == 0 else 0))
    return cell(hr, er)


def bu(p: tuple[int, ...], target: int) -> tuple[int, ...]:
    n = len(p)
    out = [0] * n
    below = target
    for d in range(n - 1, -1, -1):
        out[d] = G(p[d], below)
        below = out[d]
    return tuple(out)


def row_period_transient(seq: list[int], max_period: int = 64) -> tuple[int | None, int | None]:
    """Smallest (period, transient) with seq[j] == seq[j+p] for all j >= t."""
    L = len(seq)
    for p in range(1, max_period + 1):
        # find smallest t such that periodic from t
        t = L - p
        while t > 0 and seq[t - 1] == seq[t - 1 + p]:
            t -= 1
        if t <= L // 2:  # require at least half the horizon to be periodic
            return p, t
    return None, None


def orbit_rows(q0: tuple[int, ...], target: int, steps: int) -> list[list[int]]:
    n = len(q0)
    rows = [[] for _ in range(n)]
    q = q0
    for _ in range(steps):
        for d in range(n):
            rows[d].append(q[d])
        q = bu(q, target)
    return rows


def part_a(n: int, target: int, samples: int, log, exhaustive: bool) -> None:
    steps = 6 * n + 40
    per_row_period: dict[int, Counter] = defaultdict(Counter)
    per_row_transient_max = [0] * n
    per_row_transient_sum = [0] * n
    count = 0
    words = product(range(4), repeat=n) if exhaustive else (tuple(random.randrange(4) for _ in range(n)) for _ in range(samples))
    for q0 in words:
        rows = orbit_rows(q0, target, steps)
        count += 1
        for d in range(n):
            p, t = row_period_transient(rows[d])
            per_row_period[d][p] += 1
            if t is not None:
                per_row_transient_max[d] = max(per_row_transient_max[d], t)
                per_row_transient_sum[d] += t
    print(f"[A] n={n} c={target} words={count} ({'exhaustive' if exhaustive else 'random'}) horizon={steps}", file=log)
    for d in range(n - 1, -1, -1):
        i = n - d
        pers = " ".join(f"p{p}:{c}" for p, c in sorted(per_row_period[d].items(), key=lambda x: (x[0] is None, x[0])))
        print(f"    row n-{i:2d} (d={d:2d}): periods {pers}; transient max={per_row_transient_max[d]:3d} mean={per_row_transient_sum[d]/count:6.2f}", file=log)


def part_b(n: int, target: int, log) -> None:
    """Real prefixes: run length k(W) versus top-row transient t_0 of the peel orbit."""
    steps = 6 * n + 40
    gap: Counter = Counter()  # k - t_0
    worst = None
    rows_hist: Counter = Counter()
    for source in product((1, 2), repeat=n):
        cols = []
        for u, e, hit, col in forced_orbit(source, target, n + 3):
            if hit:
                cols.append(col)
            else:
                break
        k = len(cols)
        if k == 0:
            continue
        # peel part of column n: depths 0 .. n-1 are states[u + d] with u = n
        first = cols[0]
        q0 = tuple(first.states[n + d] for d in range(n))
        rows = orbit_rows(q0, target, steps)
        p0, t0 = row_period_transient(rows[0])
        # sanity: the actual peel parts along the run equal the autonomous orbit
        q = q0
        for j, col in enumerate(cols):
            actual = tuple(col.states[col.u + d] for d in range(n))
            assert actual == q, (source, j)
            q = bu(q, target)
        # the death column: the required top cell vs the actual
        g = k - (t0 if t0 is not None else -1)
        gap[g] += 1
        rows_hist[(k, t0, p0)] += 1
        if worst is None or g > worst[0]:
            worst = (g, "".join(map(str, source)), k, t0, p0)
    print(f"[B] n={n} c={target}: distribution of k(W) - t_0(peel orbit of column n):", file=log)
    print("     " + " ".join(f"{g:+d}:{c}" for g, c in sorted(gap.items())), file=log)
    print(f"     worst (k - t_0, W, k, t_0, period_0) = {worst}", file=log)
    # joint table of (k, t0)
    ks = sorted({k for k, _, _ in rows_hist})
    ts = sorted({t for _, t, _ in rows_hist if t is not None})
    print("     rows k, cols t_0, entries = number of W", file=log)
    print("     k\\t0 " + " ".join(f"{t:4d}" for t in ts), file=log)
    for k in ks:
        line = " ".join(f"{sum(c for (kk, tt, _), c in rows_hist.items() if kk == k and tt == t):4d}" for t in ts)
        print(f"     {k:4d}  {line}", file=log)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="uc/r1-potential/peel_orbit.log")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    random.seed(args.seed)
    with open(args.log, "w") as log:
        for target in (2, 3):
            part_a(6, target, 0, log, exhaustive=True)
            part_a(12, target, 3000, log, exhaustive=False)
            part_a(20, target, 1000, log, exhaustive=False)
            log.flush()
        for n in range(8, 15):
            for target in (2, 3):
                part_b(n, target, log)
                log.flush()
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()
