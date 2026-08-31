"""a25: symbolic regression on the exact eps_30(m) sequence (PySR).

PRE-REGISTERED PROTOCOL (fixed before any fit was run):

  * Data: the exact eps_30(m), m = 1..MMAX, computed by eps_dp.py.  Every
    value converts to float64 with zero error (power-of-two denominator,
    numerator < 2^53), so the regression input carries no rounding.
  * Split: fit on m <= MFIT, hold out m = MFIT+1 .. MMAX ENTIRELY.  The
    held-out block is never seen by the search.
  * SUCCESS CRITERION, stated before fitting.  eps(m) varies over
    [0.167, 0.25] while the increments Delta(m) = eps(m-1) - eps(m) near the
    held-out block are ~5e-4.  So a held-out error of "1% of eps" is ~30x the
    increment being predicted, and ANY smooth decreasing curve clears it.
    A candidate therefore survives only if

        max |pred(m) - eps(m)| over held-out m   <   0.5 * min Delta(m) over held-out m

    i.e. the expression must predict the next step better than half the step
    it is predicting.  Anything else is reported as a FAILURE, including
    expressions with visually tiny relative error.
  * We report the entire accuracy/complexity Pareto front, not the single
    best equation, with the held-out verdict per front member.
  * m -> infinity limits are read off surviving expressions via sympy and are
    labelled EXTRAPOLATION FROM A FIT, never a proof.

Usage: uv run python sr.py [MFIT]
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

import numpy as np
import sympy

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "eps30_values.json")) as fh:
        store = json.load(fh)["30"]
    ms = sorted(int(k) for k in store)
    vals = []
    for m in ms:
        f = Fraction(store[str(m)]["num"], store[str(m)]["den"])
        v = float(f)
        assert Fraction(v) == f, f"lossy float64 at m={m}"
        vals.append(v)
    return np.array(ms, dtype=float), np.array(vals)


def run_search(X, y, label, seed=20260831):
    from pysr import PySRRegressor

    model = PySRRegressor(
        niterations=300,
        binary_operators=["+", "-", "*", "/", "^"],
        unary_operators=["log", "exp", "sqrt", "inv(x) = 1/x"],
        extra_sympy_mappings={"inv": lambda x: 1 / x},
        maxsize=22,
        populations=24,
        population_size=40,
        elementwise_loss="loss(p, t) = (p - t)^2",
        model_selection="best",
        deterministic=True,
        parallelism="serial",
        random_state=seed,
        progress=False,
        temp_equation_file=True,
        verbosity=0,
        run_id=f"a25_{label}",
    )
    model.fit(X.reshape(-1, 1), y)
    return model


def report(model, ms_fit, y_fit, ms_hold, y_hold, deltas_hold, label):
    x = sympy.Symbol("x0")
    print(f"\n{'='*92}\nPARETO FRONT -- target: {label}")
    thresh = 0.5 * float(np.min(np.abs(deltas_hold)))
    print(f"held-out m = {[int(v) for v in ms_hold]}")
    print(f"survival threshold: max held-out |error| < 0.5 * min|Delta| = {thresh:.3e}\n")
    print(f"{'cplx':>4} {'fit MSE':>11} {'fit maxerr':>11} {'HOLD maxerr':>12} "
          f"{'/thresh':>9}  {'m->inf':>12}  verdict   equation")
    rows = []
    for _, r in model.equations_.iterrows():
        expr = r["sympy_format"]
        try:
            f = sympy.lambdify(x, expr, "numpy")
            pf = np.asarray(f(ms_fit), dtype=float) * np.ones_like(ms_fit)
            ph = np.asarray(f(ms_hold), dtype=float) * np.ones_like(ms_hold)
        except Exception as e:  # noqa: BLE001
            print(f"{int(r['complexity']):>4}  <uncomputable: {e}>")
            continue
        if not (np.isfinite(pf).all() and np.isfinite(ph).all()):
            continue
        fit_mse = float(np.mean((pf - y_fit) ** 2))
        fit_max = float(np.max(np.abs(pf - y_fit)))
        hold_max = float(np.max(np.abs(ph - y_hold)))
        try:
            lim = sympy.limit(expr, x, sympy.oo)
            lim_s = f"{float(lim):.6f}" if lim.is_number and lim.is_finite else str(lim)[:12]
        except Exception:  # noqa: BLE001
            lim_s = "?"
        verdict = "SURVIVES" if hold_max < thresh else "fails"
        print(f"{int(r['complexity']):>4} {fit_mse:11.3e} {fit_max:11.3e} {hold_max:12.3e} "
              f"{hold_max/thresh:9.1f}  {lim_s:>12}  {verdict:8}  {sympy.sstr(expr)[:70]}")
        rows.append({"complexity": int(r["complexity"]), "equation": sympy.sstr(expr),
                     "fit_mse": fit_mse, "fit_max": fit_max, "hold_max": hold_max,
                     "limit": lim_s, "survives": verdict == "SURVIVES"})
    return {"target": label, "threshold": thresh,
            "held_out_m": [int(v) for v in ms_hold], "front": rows}


def main() -> None:
    mfit = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    mlo = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    ms, eps = load()
    # mlo drops the pre-asymptotic head: m<=9 carries the exact ties
    # eps(1)=eps(2), eps(3)=eps(4) and increments up to 3.1e-2, ~70x the tail.
    fit = (ms <= mfit) & (ms >= mlo)
    hold = ms > mfit
    assert hold.sum() >= 3, "need at least 3 held-out points"
    print(f"a25 / sr.py -- PySR on exact eps_30(m), m = {int(ms[0])}..{int(ms[-1])}")
    print(f"fit on {mlo} <= m <= {mfit} ({int(fit.sum())} points); "
          f"held out m = {[int(v) for v in ms[hold]]} ({int(hold.sum())} points)")

    d = np.concatenate(([np.nan], eps[:-1] - eps[1:]))   # d[i] = eps(m_i-1)-eps(m_i)
    deltas_hold = d[hold]

    out = []
    # SEED REPLICATION: a low-complexity form that recurs across independent
    # searches is an attractor of the search; one that appears once was a lucky
    # draw and carries much less weight.
    for k, seed in enumerate((20260831, 7, 991)):
        m1 = run_search(ms[fit], eps[fit], f"eps_s{k}", seed=seed)
        out.append(report(m1, ms[fit], eps[fit], ms[hold], eps[hold], deltas_hold,
                          f"eps_30(m)  [seed {seed}]"))

    # second target: the increment, which is what actually carries the limit.
    dfit = fit & np.isfinite(d)
    dhold = hold
    m2 = run_search(ms[dfit], d[dfit], "delta")
    print(f"\n(For the Delta target the survival threshold is re-derived from the "
          f"second differences of Delta.)")
    dd = np.abs(np.diff(d[1:]))
    thr2 = np.array([np.min(dd[-len(deltas_hold):])] * len(deltas_hold))
    out.append(report(m2, ms[dfit], d[dfit], ms[dhold], d[dhold], thr2, "Delta(m)"))

    with open(os.path.join(HERE, "sr_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote sr_results.json")


if __name__ == "__main__":
    main()
