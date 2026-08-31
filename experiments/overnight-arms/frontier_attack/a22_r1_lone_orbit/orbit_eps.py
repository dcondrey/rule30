"""a22: does the ENSEMBLE Bayes error eps_30(m) (a21, Theorem S) describe the
window-conditional prediction error actually realised on the LONE-SEED orbit's
own trace, or is the single orbit atypical (PATH.md obstruction E)?

a21 proved eps(m) is the exact Bayes error of predicting r_t = s(t,1) from the
window gamma = (c_{t-m},...,c_{t-1}) of centre-column bits, averaged uniformly
over the ENSEMBLE of left-supported rows.  It also showed (orbit_window.py,
section 7) that on the lone-seed orbit specifically, bounded-window
DETERMINATION fails up to m<=28 (some conflicting window survives) -- but that
is a yes/no test, not an error rate, and says nothing about whether the lone
orbit's error rate MATCHES eps(m) or is bigger/smaller.

This script measures that error rate directly, out of sample, on the actual
lone-seed trace, and compares it to eps_30(m) with an explicit statistic.

Design (out-of-sample, to avoid the trivial in-sample optimism of "majority
vote over the same data you test on"):
  - simulate the lone-seed trace to T steps (c_t, r_t for t < T)
  - TRAIN half: t in [0, T/2).  Build the empirical majority predictor
    win -> argmax_v count(r_t = v | window = win) from this half only.
  - TEST half: t in [T/2, T).  Evaluate that fixed predictor's error rate on
    this half (windows unseen in TRAIN fall back to the train-half global
    majority of r_t; their fraction is reported so this fallback never hides
    behind silence).
  - Because the trace is one deterministic, highly autocorrelated sequence
    (windows overlapping by m-1 symbols), individual t are NOT independent
    trials, so a naive binomial CI on all T/2 test points understates
    variance.  To get an honest CI, the TEST half is also split into B
    contiguous, non-overlapping BLOCKS; each block's error rate is one
    approximately-independent replicate (Rule 30's centre column mixes
    fast -- consecutive blocks of >= a few thousand steps are only weakly
    coupled through the O(1)-speed left light cone), and a one-sample t-test
    compares the B block means against the fixed reference value eps_30(m).

Both "all t" and "t restricted to Z = {t : c_t = 0}" are reported, since R1 /
Lemma Z is a statement about r|Z specifically.

Usage: uv run python orbit_eps.py [T] [B] > orbit_eps_output.txt
"""

from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "a21_r1_direct")
)
from substrate import COMMON, step  # noqa: E402

# eps_30(m), m=1..16, exact rationals from a21 r1_direct_attempt.md section 5 /
# eps_theorem_results.json ("verified" there by exhaustive 2^t enumeration,
# reused here verbatim, NOT recomputed by this arm).
EPS30_NUM = [
    2, 8, 28, 112, 416, 1644, 6280, 24612,
    95840, 380412, 1507680, 5969532, 23733628, 94203568, 374847204, 1488690544,
]
EPS30 = {m: EPS30_NUM[m - 1] / (2 ** (2 * m + 1)) for m in range(1, 17)}


def trace(T: int, rule: int) -> tuple[list[int], list[int]]:
    row = 1
    c, r = [], []
    for t in range(T):
        c.append((row >> t) & 1)
        r.append((row >> (t + 1)) & 1)
        row = step(row, rule)
    return c, r


def majority_map(c: list[int], r: list[int], lo: int, hi: int, m: int,
                  restrict_zero: bool) -> tuple[dict[int, int], int, int]:
    """win -> majority r-value, counted over t in [lo,hi) with t>=m.
    Returns (map, global_ones, global_total) for the fallback majority.
    """
    counts: dict[int, list[int]] = {}
    mask = (1 << m) - 1
    win = 0
    ones = total = 0
    for t in range(lo, hi):
        if t >= m:
            if (not restrict_zero) or c[t] == 0:
                cnt = counts.setdefault(win, [0, 0])
                cnt[r[t]] += 1
                ones += r[t]
                total += 1
        win = ((win << 1) | c[t]) & mask
    return {w: (1 if v[1] > v[0] else 0) for w, v in counts.items()}, ones, total


def eval_error(c: list[int], r: list[int], lo: int, hi: int, m: int,
                mp: dict[int, int], fallback: int,
                restrict_zero: bool, block_bounds: list[tuple[int, int]]):
    """Error over [lo,hi) using fixed map mp; also per-block error rates for
    the blocks in block_bounds (each a subrange of [lo,hi))."""
    mask = (1 << m) - 1
    win = 0
    errs = 0
    tot = 0
    unseen = 0
    block_idx = 0
    block_err = [0] * len(block_bounds)
    block_tot = [0] * len(block_bounds)
    for t in range(0, hi):
        if t >= lo and t >= m and ((not restrict_zero) or c[t] == 0):
            pred = mp.get(win)
            seen = pred is not None
            if not seen:
                pred = fallback
                unseen += 1
            wrong = 1 if pred != r[t] else 0
            errs += wrong
            tot += 1
            while block_idx < len(block_bounds) and t >= block_bounds[block_idx][1]:
                block_idx += 1
            if block_idx < len(block_bounds) and block_bounds[block_idx][0] <= t < block_bounds[block_idx][1]:
                block_tot[block_idx] += 1
                block_err[block_idx] += wrong
        win = ((win << 1) | c[t]) & mask
    rates = [be / bt if bt > 0 else None for be, bt in zip(block_err, block_tot)]
    return errs / tot if tot else None, tot, unseen, rates, block_tot


def one_sample_t_test(sample: list[float], mu0: float):
    n = len(sample)
    if n < 2:
        return None, None
    mean = statistics.fmean(sample)
    sd = statistics.stdev(sample)
    if sd == 0:
        return (float("inf") if mean != mu0 else 0.0), 0.0 if mean != mu0 else 1.0
    tstat = (mean - mu0) / (sd / (n ** 0.5))
    # two-sided p-value via Student-t CDF, implemented with the regularized
    # incomplete beta function (stdlib math only).
    p = student_t_two_sided_p(tstat, n - 1)
    return tstat, p


def student_t_two_sided_p(t: float, df: int) -> float:
    import math

    x = df / (df + t * t)
    ib = _betainc(x, df / 2, 0.5)
    return ib  # this equals the two-sided p-value directly


def _betainc(x: float, a: float, b: float) -> float:
    import math

    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log1p(-x) * b - lbeta)
    if x < (a + 1) / (a + b + 2):
        cf = _betacf(x, a, b)
        return front * cf / a
    else:
        cf = _betacf(1 - x, b, a)
        return 1.0 - front * cf / b


def _betacf(x: float, a: float, b: float, itmax: int = 200, eps: float = 3e-12) -> float:
    qab = a + b
    qap = a + 1
    qam = a - 1
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def main() -> None:
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    ms = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16]
    print("a22 / orbit_eps.py -- held-out window-conditional error rate on the "
          "lone-seed orbit vs ensemble eps_30(m)")
    print(f"T = {T}, B = {B} test blocks\n")

    c, r = trace(T, 30)
    assert c[:4096] == COMMON.center_column_bits(4096), "trace cross-check vs common.rule30"
    print("cross-check OK: first 4096 centre bits match common.center_column_bits\n")

    mid = T // 2
    block_len = (T - mid) // B
    block_bounds = [(mid + i * block_len, mid + (i + 1) * block_len if i < B - 1 else T)
                    for i in range(B)]

    for restrict_zero in (False, True):
        label = "t in Z (c_t=0)" if restrict_zero else "all t"
        print(f"=== {label} ===")
        print(f"{'m':>3} {'eps30(m)':>10} {'train_err':>10} {'test_err':>10} "
              f"{'unseen%':>8} {'blk_mean':>9} {'blk_sd':>8} {'t_stat':>9} {'p_value':>10} {'n_test':>8}")
        for m in ms:
            mp_train, ones_tr, tot_tr = majority_map(c, r, 0, mid, m, restrict_zero)
            fallback = 1 if ones_tr * 2 > tot_tr else 0
            train_err, train_tot, train_unseen, _, _ = eval_error(
                c, r, 0, mid, m, mp_train, fallback, restrict_zero, []
            )
            test_err, test_tot, test_unseen, block_rates, block_tot = eval_error(
                c, r, mid, T, m, mp_train, fallback, restrict_zero, block_bounds
            )
            valid_rates = [(rate, bt) for rate, bt in zip(block_rates, block_tot) if rate is not None and bt >= 20]
            rates_only = [x[0] for x in valid_rates]
            if len(rates_only) >= 2:
                bmean = statistics.fmean(rates_only)
                bsd = statistics.stdev(rates_only)
                tstat, pval = one_sample_t_test(rates_only, EPS30[m])
            else:
                bmean = bsd = tstat = pval = float("nan")
            unseen_pct = 100.0 * test_unseen / test_tot if test_tot else float("nan")
            print(f"{m:3d} {EPS30[m]:10.6f} {train_err:10.6f} {test_err:10.6f} "
                  f"{unseen_pct:8.3f} {bmean:9.6f} {bsd:8.6f} {tstat:9.3f} {pval:10.4g} {test_tot:8d}")
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
