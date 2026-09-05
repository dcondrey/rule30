#!/usr/bin/env python3
"""Scores PREREGISTRATION-PRODUCT-GEOMETRIC-MEAN.md.

The product / geometric-mean bound on the forced descent, replacing per-step
domination (dead three ways: entrywise, every weight vector, every population
floor).

Primary metric, per cell (n, c), from the exact integer row D_0 .. D_Z:
    k_p = argmax_k D_k          (first argmax on a tie)
    k_z = min{k : D_k == 0}
    k_l = k_z - 1               (last nonzero depth)
    m'  = k_l - k_p             (post-peak steps, EXCLUDING the step into zero)
    GM  = (D_{k_l} / D_{k_p}) ** (1/m')
GM is the geometric mean of the post-peak ratios; that product telescopes, so
GM is a function of three integers only. D_peak, m' and log_phi(D_peak) are
reported beside it because when GM moves, only the primitives say which factor
moved.

Kill condition: max_c GM(n,c) >= 1/phi at any n, OR monotone increasing across
the last four n. Either fires -> report plainly and stop.

Secondary metric (the task's S-side framing): telescoped S_{k_l}/S_0 vs 2^-n.

No new tree walker. n=17..24 are parsed from the overnight_census.py logs;
n=10..16 are recomputed by calling overnight_census.run() itself, the same
function that produced those logs, which calls the real
late_pull_diagonal_sat.literal_extension.
"""
from __future__ import annotations

import argparse
import ast
import math
import re
from pathlib import Path

PHI = (1 + 5 ** 0.5) / 2
THRESHOLD = 1.0 / PHI

LOGS = [
    "overnight_c2_even.log",
    "overnight_c2_odd.log",
    "overnight_c3_even.log",
    "overnight_c3_odd.log",
]

RESULT_RE = re.compile(
    r"RESULT n=(\d+) c=(\d+) .*?max_row=(\d+) margin=(-?\d+)"
)


def parse_logs(root: Path) -> dict[tuple[int, int], dict]:
    """Pull D and S rows out of the overnight census logs."""
    cells: dict[tuple[int, int], dict] = {}
    for name in LOGS:
        path = root / name
        if not path.exists():
            raise SystemExit(f"missing log: {path}")
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            m = RESULT_RE.search(line)
            if not m:
                continue
            n, tail, max_row, margin = (int(g) for g in m.groups())
            d_row = s_row = None
            for follow in lines[i + 1:i + 4]:
                follow = follow.strip()
                if follow.startswith("D="):
                    d_row = ast.literal_eval(follow[2:])
                elif follow.startswith("S="):
                    s_row = ast.literal_eval(follow[2:])
            if d_row is None or s_row is None:
                raise SystemExit(f"{name}: incomplete block for n={n} c={tail}")
            cells[(n, tail)] = {
                "D": d_row, "S": s_row, "max_row": max_row,
                "margin": margin, "src": name,
            }
    return cells


def compute_small(ns: list[int]) -> dict[tuple[int, int], dict]:
    """Recompute small n with the same function that produced the logs."""
    from overnight_census import run  # real literal_extension, rows = n+4
    cells: dict[tuple[int, int], dict] = {}
    for n in ns:
        for tail in (2, 3):
            r = run(n, tail)
            cells[(n, tail)] = {
                "D": r["D"], "S": r["S"], "max_row": r["max_row"],
                "margin": r["margin"], "src": "overnight_census.run()",
            }
    return cells


def score(cell: dict) -> dict:
    d, s = cell["D"], cell["S"]
    k_z = next(k for k, v in enumerate(d) if v == 0)
    k_l = k_z - 1
    k_p = max(range(k_z), key=lambda k: (d[k], -k))
    m = k_l - k_p
    gm = (d[k_l] / d[k_p]) ** (1.0 / m) if m > 0 else float("nan")
    return {
        "k_p": k_p, "D_peak": d[k_p], "k_l": k_l, "D_last": d[k_l],
        "m": m, "GM": gm, "log_phi_peak": math.log(d[k_p], PHI),
        "S0": s[0], "S_last": s[k_l],
        "S_ratio": s[k_l] / s[0],
        "max_row": cell["max_row"], "margin": cell["margin"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).parent)
    ap.add_argument("--small", type=int, nargs="*", default=[10, 12, 14, 16])
    args = ap.parse_args()

    cells = parse_logs(args.root)
    if args.small:
        cells.update(compute_small(args.small))
    scored = {k: score(v) for k, v in cells.items()}

    print("=" * 78)
    print("PRIMARY: geometric mean of post-peak D ratios, vs 1/phi = "
          f"{THRESHOLD:.5f}")
    print()
    print(f"{'n':>3} {'c':>2} {'k_p':>4} {'D_peak':>7} {'k_l':>4} {'D_l':>4} "
          f"{'m':>3} {'GM':>7} {'log_phi(pk)':>12} {'m<lp?':>6}")
    ns = sorted({n for n, _ in cells})
    for n in ns:
        for tail in (2, 3):
            if (n, tail) not in scored:
                continue
            r = scored[(n, tail)]
            ok = "yes" if r["m"] < r["log_phi_peak"] else "NO"
            print(f"{n:>3} {tail:>2} {r['k_p']:>4} {r['D_peak']:>7} "
                  f"{r['k_l']:>4} {r['D_last']:>4} {r['m']:>3} "
                  f"{r['GM']:>7.4f} {r['log_phi_peak']:>12.2f} {ok:>6}")

    print()
    print("-" * 78)
    print("max over c, per n (the primary metric) and its trend")
    trend = []
    for n in ns:
        vals = [(scored[(n, t)]["GM"], t) for t in (2, 3) if (n, t) in scored]
        mx, at = max(vals)
        trend.append((n, mx, at))
        flag = "  <-- EXCEEDS 1/phi" if mx >= THRESHOLD else ""
        print(f"  n={n:>3}: max_c GM = {mx:.4f}  (c={at}){flag}")

    print()
    print("=" * 78)
    over = [(n, g) for n, g, _ in trend if g >= THRESHOLD]
    tail4 = [g for _, g, _ in trend[-4:]]
    rising = len(tail4) == 4 and all(
        tail4[i] < tail4[i + 1] for i in range(3)
    )
    worst_n, worst_g, worst_c = max(trend, key=lambda x: x[1])
    print(f"  worst cell overall: GM = {worst_g:.4f} at n={worst_n} c={worst_c}"
          f"   (threshold {THRESHOLD:.5f}, margin {THRESHOLD - worst_g:+.4f})")
    print(f"  condition 1 (any n >= 1/phi): "
          f"{'FIRED at ' + str(over) if over else 'not fired'}")
    print(f"  condition 2 (last four n monotone increasing): "
          f"{'FIRED' if rising else 'not fired'}  last4={[round(g,4) for g in tail4]}")
    print(f"  => KILL {'FIRED' if (over or rising) else 'NOT fired'}")

    print()
    print("=" * 78)
    print("SECONDARY (S-side, as the task frames it): S_{k_l}/S_0 vs 2^-n")
    print(f"{'n':>3} {'c':>2} {'S_0':>10} {'S_last':>8} {'S_l/S_0':>12} "
          f"{'2^-n':>12} {'<2^-n?':>7}")
    for n in ns:
        for tail in (2, 3):
            if (n, tail) not in scored:
                continue
            r = scored[(n, tail)]
            tp = 2.0 ** -n
            print(f"{n:>3} {tail:>2} {r['S0']:>10} {r['S_last']:>8} "
                  f"{r['S_ratio']:>12.3e} {tp:>12.3e} "
                  f"{'yes' if r['S_ratio'] < tp else 'NO':>7}")

    print()
    print("=" * 78)
    print("EXTINCTION MARGIN (same source; margin = (n+2) - max_row)")
    for n in ns:
        row = "  ".join(
            f"c={t}: max_row={scored[(n,t)]['max_row']:>2} "
            f"margin={scored[(n,t)]['margin']:>2}"
            for t in (2, 3) if (n, t) in scored
        )
        print(f"  n={n:>3}  {row}")


if __name__ == "__main__":
    main()
