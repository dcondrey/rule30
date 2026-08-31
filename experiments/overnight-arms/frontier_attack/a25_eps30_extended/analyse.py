"""a25: increment diagnostics on the exact eps_30(m) sequence.

The limit question -- does eps_30(m) -> 0? -- is exactly the question of
whether Delta(m) = eps(m-1) - eps(m) is summable.  This script reports
Delta(m) directly and fits its decay, which bears on the question far more
honestly than reading a limit off a fitted symbolic expression.

All eps values are exact rationals with power-of-two denominators; the
numerators are below 2^53 for every m computed here, so the float64
conversion used for plotting/fitting is EXACT, not rounded.

Usage: uv run python analyse.py
"""

from __future__ import annotations

import json
import os
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(rule: int = 30) -> dict[int, Fraction]:
    with open(os.path.join(HERE, "eps30_values.json")) as fh:
        store = json.load(fh)
    return {int(k): Fraction(v["num"], v["den"]) for k, v in store[str(rule)].items()}


def main() -> None:
    eps = load(30)
    ms = sorted(eps)
    print("m   eps(m) exact float64      Delta(m)=eps(m-1)-eps(m)   Delta ratio   exact fraction")
    prev = None
    prevd = None
    for m in ms:
        e = float(eps[m])
        # exactness of the float64 conversion
        assert Fraction(e) == eps[m], f"float64 conversion lossy at m={m}"
        d = prev - e if prev is not None else float("nan")
        r = d / prevd if (prevd not in (None, 0.0) and prevd == prevd) else float("nan")
        print(f"{m:2d}  {e:.15f}   {d: .9f}   {r: .5f}   "
              f"{eps[m].numerator}/{eps[m].denominator}")
        prev, prevd = e, d

    # exact ties
    ties = [(a, b) for a, b in zip(ms, ms[1:]) if eps[a] == eps[b]]
    print(f"\nexact ties eps(m)==eps(m+1): {ties if ties else 'none'}")

    arr = np.array([float(eps[m]) for m in ms])
    dm = np.array(ms[1:], dtype=float)
    dl = arr[:-1] - arr[1:]
    assert (dl >= 0).all(), "eps is not non-increasing"
    assert (dl[dm >= 5] > 0).all(), "eps is not strictly decreasing for m >= 5"
    print("\neps(m) is non-increasing throughout, and strictly decreasing for m >= 5.")

    # --- decay law of Delta ---
    print("\n--- decay of Delta(m): log Delta = a + b log m, over trailing windows ---")
    print("  b = -1 would make Delta ~ 1/m (divergent sum, eps -> 0 possible);")
    print("  b < -1 makes sum Delta finite, forcing a strictly positive limit.")
    for lo in (5, 9, 13, 15, 17):
        sel = dm >= lo
        if sel.sum() < 4:
            continue
        b, a = np.polyfit(np.log(dm[sel]), np.log(dl[sel]), 1)
        # implied tail sum from m_max to infinity if Delta = exp(a) m^b
        mmax = dm.max()
        if b < -1:
            tail = np.exp(a) * mmax ** (b + 1) / (-b - 1)
            lim = f"implied limit eps(inf) ~ {arr[-1] - tail:.6f}  (tail {tail:.6f})"
        else:
            lim = "b >= -1: tail sum diverges, consistent with eps -> 0"
        print(f"  window m>={lo:2d} (n={int(sel.sum()):2d}):  b = {b: .4f}   {lim}")

    # --- geometric-decay test on Delta ---
    print("\n--- geometric test: Delta(m+1)/Delta(m) over the trailing range ---")
    ratios = dl[1:] / dl[:-1]
    print(f"  last 8 ratios: {np.round(ratios[-8:], 4).tolist()}")
    print(f"  mean of last 8: {ratios[-8:].mean():.4f}  "
          "(a ratio bounded below 1 would force a positive limit)")

    # --- parity split: the sequence visibly oscillates in m mod 2 ---
    print("\n--- parity split of Delta ---")
    for par, name in ((0, "even m"), (1, "odd m")):
        sel = (dm.astype(int) % 2) == par
        s = dl[sel][-6:]
        print(f"  {name}: last 6 Delta = {np.round(s, 6).tolist()}")

    # --- Richardson / Aitken extrapolation of eps itself ---
    print("\n--- Aitken delta-squared on eps(m) (extrapolation, NOT a proof) ---")
    for i in range(len(arr) - 3, len(arr) - 8, -1):
        if i < 1:
            break
        x0, x1, x2 = arr[i - 1], arr[i], arr[i + 1]
        den = x2 - 2 * x1 + x0
        if den != 0:
            print(f"  anchored at m={ms[i]:2d}: Aitken limit = {x0 - (x1 - x0) ** 2 / den:.6f}")


def families(mfit: int = 21, mlo: int = 10) -> None:
    """Held-out comparison of hand-chosen parametric families.

    This is the instrument that actually bears on the limit question: it puts
    families with a STRICTLY POSITIVE limit and families with limit ZERO on
    the same held-out test, so the question is decided by predictive accuracy
    rather than by which form the search happened to emit.
    """
    from scipy.optimize import least_squares

    eps = load(30)
    ms = np.array(sorted(eps), dtype=float)
    y = np.array([float(eps[int(m)]) for m in ms])
    # mlo excludes the pre-asymptotic head.  m<=9 carries the exact ties
    # eps(1)=eps(2), eps(3)=eps(4) and increments up to 3.1e-2, two orders of
    # magnitude above the tail; fitting an asymptotic form there is meaningless
    # and it also makes log(m) singular at m=1.
    fit, hold = (ms <= mfit) & (ms >= mlo), ms > mfit
    d = y[:-1] - y[1:]
    thresh = 0.5 * float(np.min(d[hold[1:]]))

    # MULTISTART is mandatory here, not a refinement.  With a single start the
    # free-exponent family `a + b*m^-p` scored WORSE than its own restriction
    # `a + b/sqrt(m)`, which is impossible at the optimum: the free family
    # contains p=1/2.  That was a local minimum being reported as a result.
    P0 = [0.2, 0.35, 0.5, 0.7, 1.0, 1.5]
    C0 = [1.0, 5.0, 20.0, 100.0]
    F = [
        ("a + b/m",            lambda p, m: p[0] + p[1] / m,          [[0.15, 0.5]],  "a"),
        ("a + b/sqrt(m)",      lambda p, m: p[0] + p[1] / np.sqrt(m), [[0.14, 0.12]], "a"),
        ("a + b*m^-p",         lambda p, m: p[0] + p[1] * m ** (-abs(p[2])),
         [[0.14, 0.12, q] for q in P0], "a"),
        ("a + b*log(m)/m",     lambda p, m: p[0] + p[1] * np.log(m) / m, [[0.15, 0.3]], "a"),
        ("b*m^-p        (->0)", lambda p, m: p[0] * m ** (-abs(p[1])),
         [[0.3, q / 5] for q in P0], "0"),
        ("b/log(m)      (->0)", lambda p, m: p[0] / np.log(m), [[0.5]], "0"),
        ("b/log(m)^p    (->0)", lambda p, m: p[0] / np.log(m) ** abs(p[1]),
         [[0.5, q] for q in P0], "0"),
        ("b/log(c+m)^p  (->0)", lambda p, m: p[0] / np.log(abs(p[1]) + m) ** abs(p[2]),
         [[0.5, c, q] for c in C0 for q in P0], "0"),
        # shift OUTSIDE the log: the strongest limit-zero competitor, since a
        # large c makes it (const) - (small log term), i.e. a fake plateau over
        # any bounded window while still tending to 0.
        ("b/(c+log m)^p (->0)", lambda p, m: p[0] / (abs(p[1]) + np.log(m)) ** abs(p[2]),
         [[0.5 * (1 + c), c, q] for c in C0 for q in P0], "0"),
        ("b/(c+log m)   (->0)", lambda p, m: p[0] / (abs(p[1]) + np.log(m)),
         [[0.5 * (1 + c), c] for c in C0], "0"),
    ]
    print(f"\n--- parametric families, fit on {mlo}<=m<={mfit} "
          f"({int(fit.sum())} pts), held out m={[int(v) for v in ms[hold]]} ---")
    print(f"survival threshold: held-out max|err| < {thresh:.3e}\n")
    print(f"{'family':<22} {'limit':>6} {'fit maxerr':>11} {'HOLD maxerr':>12} "
          f"{'/thresh':>8}  {'eps(inf)':>10}  verdict")
    for name, f, starts, lim in F:
        best = None
        for p0 in starts:
            try:
                r = least_squares(lambda p: f(p, ms[fit]) - y[fit], p0,
                                  method="lm", max_nfev=200000)
            except Exception:  # noqa: BLE001
                continue
            if best is None or r.cost < best.cost:
                best = r
        r = best
        fm = float(np.max(np.abs(f(r.x, ms[fit]) - y[fit])))
        hm = float(np.max(np.abs(f(r.x, ms[hold]) - y[hold])))
        linf = f"{r.x[0]:.6f}" if lim == "a" else "0"
        print(f"{name:<22} {lim:>6} {fm:11.3e} {hm:12.3e} {hm/thresh:8.2f}  {linf:>10}  "
              f"{'SURVIVES' if hm < thresh else 'fails'}")


def window_stability() -> None:
    """Is the fitted asymptote `a` in eps ~ a + b*m^-p stable as the fit window
    slides right?  Stable => evidence for a positive limit.  Drifting down =>
    the positive limit is an artifact of the window and the verdict is
    UNDETERMINED.  This substitutes for a confidence interval, which cannot be
    legitimately constructed from 27 deterministic points."""
    from scipy.optimize import least_squares

    eps = load(30)
    ms = np.array(sorted(eps), dtype=float)
    y = np.array([float(eps[int(m)]) for m in ms])
    print("\n--- window stability of the fitted asymptote in eps ~ a + b*m^-p ---")
    print(f"{'fit window':>14} {'n':>3} {'a (asymptote)':>15} {'b':>10} {'p':>8} {'maxerr':>11}")
    for lo in (3, 5, 8, 10, 13, 16, 18):
        sel = (ms >= lo)
        if sel.sum() < 6:
            continue
        r = None
        for q in (0.2, 0.35, 0.5, 0.7, 1.0, 1.5):
            c = least_squares(
                lambda p: p[0] + p[1] * ms[sel] ** (-abs(p[2])) - y[sel],
                [0.14, 0.12, q], method="lm", max_nfev=200000)
            if r is None or c.cost < r.cost:
                r = c
        err = float(np.max(np.abs(r.x[0] + r.x[1] * ms[sel] ** (-abs(r.x[2])) - y[sel])))
        print(f"  m>={lo:2d}..{int(ms[-1]):2d} {int(sel.sum()):5d} {r.x[0]:15.6f} "
              f"{r.x[1]:10.5f} {abs(r.x[2]):8.4f} {err:11.3e}")


def parity_chains() -> None:
    """The one-step Delta oscillates strongly in m mod 2, which contaminates any
    log-log decay fit (the exponent then depends on which parities the window
    happens to contain).  The two-step increments eps(m)-eps(m+2) along each
    parity chain are clean; fit the decay exponent there instead."""
    eps = load(30)
    ms = sorted(eps)
    y = {m: float(eps[m]) for m in ms}
    print("\n--- parity-cleaned decay: fit log(eps(m)-eps(m+2)) = a + q log m ---")
    print("    Delta ~ C m^-s corresponds to two-step increments ~ 2C m^-s, so q = -s.")
    # The floor matters and is reported at both values: m>=9 lets the
    # pre-asymptotic head (excluded everywhere else via mlo=10) back into the
    # odd chain, and the odd exponent moves when it does.  m>=13 is consistent
    # with the mlo=10 decision used for every fit above.
    for floor in (9, 13):
        for par, name in ((1, "odd chain "), (0, "even chain")):
            pts = [(m, y[m] - y[m + 2]) for m in ms
                   if m % 2 == par and m + 2 in y and m >= floor]
            if len(pts) < 4:
                continue
            a = np.array([p[0] for p in pts], dtype=float)
            b = np.array([p[1] for p in pts], dtype=float)
            assert (b > 0).all()
            q, c = np.polyfit(np.log(a), np.log(b), 1)
            print(f"  floor m>={floor:2d}  {name} (n={len(pts)}): q = {q:.4f}"
                  f"  =>  Delta ~ m^{q:.3f}")


if __name__ == "__main__":
    main()
    try:
        families(21, 10)          # primary, pre-registered split
        families(18, 10)          # robustness: earlier split, 9 held-out points
        families(21, 5)           # robustness: longer fit head
        window_stability()
        parity_chains()
    except ImportError:
        print("\n(scipy not available; skipping parametric-family comparison)")
