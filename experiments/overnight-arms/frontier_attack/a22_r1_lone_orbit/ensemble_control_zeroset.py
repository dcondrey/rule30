"""Close gap 2 (parent-session follow-up): orbit_eps.py compares the lone
orbit's zero-set-restricted (t in Z = {c_t=0}) test error against the same
EPS30(m) used for the unconditional case, with no matched control -- unlike
the "all t" numbers, which ARE checked against ensemble_control.py.

Claim to test: c_t is exactly independent of (gamma, r_t) in the i.i.d.
left-supported-row ensemble, where gamma = (c_{t-m},...,c_{t-1}). Reasoning
(not yet verified computationally, hence this script): by left permutivity,
s(t,x) = b_{t-x} XOR (function of b_0..b_{t-x-1}), so c_t = s(t,0) = b_t XOR
g(b_0..b_{t-1}) for a FRESH independent uniform bit b_t, while gamma and r_t
= s(t,1) both depend only on b_0..b_{t-1}. XOR with an independent uniform
bit randomizes c_t completely regardless of any correlation with
g(b_0..b_{t-1}), so c_t should be Bernoulli(1/2) and independent of
(gamma, r_t) jointly -- meaning EPS30(m) unconditional IS the correct
reference for the zero-set-restricted case too, and orbit_eps.py's reuse of
the same EPS30(m) was NOT a baseline mismatch.

This script tests that claim directly: same generation as ensemble_control.py,
but the held-out procedure is run TWICE per m -- once on all K/2 test rows
(reproducing ensemble_control.py exactly, as a self-check), once restricted
to test rows with c[tfix]==0 -- both against the SAME EPS30(m).  If
independence holds, the restricted test_err should ALSO track EPS30(m) with
no systematic offset beyond sampling noise (fewer rows -> wider CI, nothing
else).  If it does NOT track, that's evidence against the independence
argument above and a genuine gap in the reference used by orbit_eps.py.

Usage: uv run python ensemble_control_zeroset.py [K] > ensemble_control_zeroset_output.txt
"""

from __future__ import annotations

import random
import sys
from math import erf, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a21_r1_direct"))
from substrate import cell, diagram, left_supported_row  # noqa: E402

from orbit_eps import EPS30  # noqa: E402


def binom_p(errs: int, n: int, p0: float) -> tuple[float, float]:
    mean0 = n * p0
    sd0 = (n * p0 * (1 - p0)) ** 0.5
    z = (errs - mean0) / sd0 if sd0 > 0 else float("nan")
    pval = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
    return z, pval


def main() -> None:
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    ms = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16]
    tfix = 2 * max(ms) + 1  # 33
    L = tfix + 2
    K_off = L - 1
    rng = random.Random(20260830)
    print("a22 / ensemble_control_zeroset.py -- does c_t independence hold, "
          "i.e. is EPS30(m) the right reference for the zero-set restriction too?")
    print(f"K = {K} rows, tfix = {tfix}, free bits per row = {L}\n")

    # samples[m] = list of (window, r, c_t) triples, one per row
    samples: dict[int, list[tuple[int, int, int]]] = {m: [] for m in ms}
    for i in range(K):
        bits = [rng.randint(0, 1) for _ in range(L)]
        row0 = left_supported_row(bits, K_off)
        rows = diagram(row0, K_off, tfix, 30)
        c = [cell(rows[t], t, 0, K_off) for t in range(tfix + 1)]
        r = [cell(rows[t], t, 1, K_off) for t in range(tfix + 1)]
        ct = c[tfix]
        for m in ms:
            win = 0
            for j in range(tfix - m, tfix):
                win = (win << 1) | c[j]
            samples[m].append((win, r[tfix], ct))

    half = K // 2
    print(f"{'m':>3} {'eps30(m)':>10} {'c_t=0 frac (all rows)':>22} "
          f"{'test_err|all':>12} {'p|all':>10} "
          f"{'test_err|Z':>11} {'p|Z':>10} {'n_Z':>8}")
    for m in ms:
        data = samples[m]
        train, test = data[:half], data[half:]
        # c_t=0 fraction, sanity check on independence's first prediction
        ct0_frac = sum(1 for _, _, ct in train + test if ct == 0) / len(data)

        # train map on ALL train rows (reproduces ensemble_control.py)
        counts: dict[int, list[int]] = {}
        ones = tot = 0
        for w, v, _ in train:
            cnt = counts.setdefault(w, [0, 0])
            cnt[v] += 1
            ones += v
            tot += 1
        mp = {w: (1 if v[1] > v[0] else 0) for w, v in counts.items()}
        fallback = 1 if ones * 2 > tot else 0

        # test on all test rows
        errs_all = sum(1 for w, v, _ in test if mp.get(w, fallback) != v)
        n_all = len(test)
        _, p_all = binom_p(errs_all, n_all, EPS30[m])
        test_err_all = errs_all / n_all

        # test on ONLY test rows with c_t == 0, SAME trained map, SAME EPS30(m)
        test_Z = [(w, v) for w, v, ct in test if ct == 0]
        errs_Z = sum(1 for w, v in test_Z if mp.get(w, fallback) != v)
        n_Z = len(test_Z)
        _, p_Z = binom_p(errs_Z, n_Z, EPS30[m])
        test_err_Z = errs_Z / n_Z if n_Z else float("nan")

        print(f"{m:3d} {EPS30[m]:10.6f} {ct0_frac:22.6f} "
              f"{test_err_all:12.6f} {p_all:10.4g} "
              f"{test_err_Z:11.6f} {p_Z:10.4g} {n_Z:8d}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
