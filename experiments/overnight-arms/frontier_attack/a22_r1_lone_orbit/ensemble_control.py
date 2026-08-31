"""a22 control: is the test_err > eps30(m) gap seen in orbit_eps.py (at large m)
a genuine orbit-vs-ensemble mismatch, or just finite-sample estimation noise in
the majority-vote rule learned from a sparse training set?

Run the EXACT SAME held-out majority-vote procedure as orbit_eps.py, but on
K INDEPENDENT random left-supported rows instead of one long deterministic
orbit.  Each row contributes one (window, r_t) sample per m, at a fixed
t = tfix >= 2m+1 (Theorem S's stability threshold for every m in ms), so
Theorem S / Theorem U guarantee each sample's exact marginal law is the one
eps_30(m) is defined over.  Rows are i.i.d., so a row-level train/test split
gives genuinely independent test samples (no autocorrelation confound).

If this ensemble-sourced procedure ALSO shows test_err inflating above
eps_30(m) as coverage per bin (K / 2^m) shrinks, that is direct evidence the
same inflation in orbit_eps.py is a finite-sample estimation artifact, not
evidence the lone orbit differs from the ensemble.

Usage: uv run python ensemble_control.py [K] > ensemble_control_output.txt
"""

from __future__ import annotations

import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a21_r1_direct"))
from substrate import cell, diagram, left_supported_row  # noqa: E402

from orbit_eps import EPS30, one_sample_t_test  # noqa: E402


def main() -> None:
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    ms = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16]
    tfix = 2 * max(ms) + 1  # 33; valid (t>=2m+1) simultaneously for every m<=16
    L = tfix + 2            # free bits in the row; must exceed tfix
    K_off = L - 1            # K offset for left_supported_row / cell frame
    rng = random.Random(20260830)
    print("a22 / ensemble_control.py -- same held-out procedure, i.i.d. ensemble rows")
    print(f"K = {K} rows, tfix = {tfix}, free bits per row = {L}\n")

    # samples[m] = list of (window, r) pairs, one per row
    samples: dict[int, list[tuple[int, int]]] = {m: [] for m in ms}
    for i in range(K):
        bits = [rng.randint(0, 1) for _ in range(L)]
        row0 = left_supported_row(bits, K_off)
        rows = diagram(row0, K_off, tfix, 30)
        c = [cell(rows[t], t, 0, K_off) for t in range(tfix + 1)]
        r = [cell(rows[t], t, 1, K_off) for t in range(tfix + 1)]
        for m in ms:
            win = 0
            for j in range(tfix - m, tfix):
                win = (win << 1) | c[j]
            samples[m].append((win, r[tfix]))

    half = K // 2
    print(f"{'m':>3} {'eps30(m)':>10} {'train_err':>10} {'test_err':>10} "
          f"{'unseen%':>8} {'t_stat_vs_direct':>16} {'p_direct':>10} {'n_test':>8}")
    for m in ms:
        data = samples[m]
        train, test = data[:half], data[half:]
        counts: dict[int, list[int]] = {}
        ones = tot = 0
        for w, v in train:
            cnt = counts.setdefault(w, [0, 0])
            cnt[v] += 1
            ones += v
            tot += 1
        mp = {w: (1 if v[1] > v[0] else 0) for w, v in counts.items()}
        fallback = 1 if ones * 2 > tot else 0
        train_errs = sum(1 for w, v in train if mp[w] != v)
        train_err = train_errs / len(train)
        test_errs = 0
        unseen = 0
        for w, v in test:
            pred = mp.get(w)
            if pred is None:
                pred = fallback
                unseen += 1
            if pred != v:
                test_errs += 1
        test_err = test_errs / len(test)
        unseen_pct = 100.0 * unseen / len(test)
        # direct binomial test: is test_err's count of errors consistent with
        # a Binomial(len(test), eps30(m)) draw?  (test rows are i.i.d., so
        # this IS a valid test here, unlike on the single autocorrelated orbit.)
        n = len(test)
        p0 = EPS30[m]
        mean0 = n * p0
        sd0 = (n * p0 * (1 - p0)) ** 0.5
        z = (test_errs - mean0) / sd0 if sd0 > 0 else float("nan")
        from math import erf, sqrt
        pval = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
        print(f"{m:3d} {p0:10.6f} {train_err:10.6f} {test_err:10.6f} "
              f"{unseen_pct:8.3f} {z:16.3f} {pval:10.4g} {n:8d}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
