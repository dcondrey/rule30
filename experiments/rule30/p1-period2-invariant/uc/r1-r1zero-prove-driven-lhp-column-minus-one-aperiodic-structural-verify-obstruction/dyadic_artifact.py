"""Follow-up to adversarial_checks.py CHECK A1: the Rule 90 'hits' at T = 2048.

adversarial_checks.py reported Rule 90 hits (column -1 q-periodic on the window [T/2, T], T = 2048).
Hand analysis (linearity of Rule 90, method of images with the absorbing boundary at x = 0): the impulse
response of column -1 to c_{t'} = 1 is K(tau) = [tau = 2^j - 1], so for c = 0 (01)^omega
    l_t = 0 for even t,  l_t = floor(log2(t - 1)) mod 2 for odd t >= 3,
which is constant on every dyadic block (2^k, 2^(k+1)] and flips between blocks.  A window [1024, 2048]
is exactly one block, so a finite detector sees a constant.  This is not eventual periodicity.

This script re-examines every Rule 90 hit of A1 at larger and at non-dyadic horizons:
  B1  same (y, c), T = 8192: does the q found at T = 2048 still hold on [1024, 8192]?  Predicted: no.
  B2  same (y, c), T = 8192: any q <= 256 on [4096, 8192]?  (dyadic window again; artifact may recur)
  B3  same (y, c), T = 3001: any q <= 256 on [1500, 3001]?  (window straddles a block boundary at 2048)
  B4  the closed form above versus the simulated column for the first hit, t <= 8192.
  B5  A1 rerun for Rules 30 and 90 at the non-dyadic T = 3001 (same y and drive family).
"""
import itertools
import math
import sys
import time

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/'
                   'r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural-verify-obstruction')
from adversarial_checks import lhp_column_minus_one, periodic_on_tail, drives


def tail_period_window(col, lo, hi, qmax):
    b = bytes(col)
    for q in range(1, qmax + 1):
        if b[lo:hi + 1 - q] == b[lo + q:hi + 1]:
            return q
    return None


def main():
    t0 = time.time()
    T = 2048
    D = drives(5, 1, 8192 + 3)
    hits = []
    for y in range(64):
        y_int = y << 1
        for w, pref, c in D:
            if y_int == 0 and 1 not in c:
                continue
            cols = lhp_column_minus_one(90, y_int, c, T)
            q = periodic_on_tail(cols[0], T, 256)
            if q is not None:
                hits.append((y, w, pref, c, q))
    print(f"Rule 90 hits at T={T} (window [1024,2048], q<=256): {len(hits)}")
    still = 0
    b2 = 0
    b3 = 0
    for y, w, pref, c, q in hits:
        cols = lhp_column_minus_one(90, y << 1, c, 8192)
        col = cols[0]
        b = bytes(col)
        if b[1024:8193 - q] == b[1024 + q:8193]:
            still += 1
        if tail_period_window(col, 4096, 8192, 256) is not None:
            b2 += 1
        if tail_period_window(col, 1500, 3001, 256) is not None:
            b3 += 1
    print(f"CHECK B1 hits whose T=2048 period q persists on [1024, 8192]: {still} of {len(hits)}")
    print(f"CHECK B2 hits with some q<=256 on the dyadic window [4096, 8192]: {b2} of {len(hits)} (artifact recurs on dyadic windows)")
    print(f"CHECK B3 hits with some q<=256 on the straddling window [1500, 3001]: {b3} of {len(hits)}")
    # B4 closed form for the first hit y = 0, c = 0 (01)^omega
    y, w, pref, c, q = hits[0]
    print(f"first hit: y={y} w={w} prefix={pref} q={q}")
    if y == 0 and pref == [0] and w == [0, 1]:
        cols = lhp_column_minus_one(90, 0, c, 8192)
        col = cols[0]
        pred = bytearray(8193)
        for t in range(3, 8193):
            if t % 2 == 1:
                pred[t] = math.floor(math.log2(t - 1)) % 2
        mism = sum(1 for t in range(8193) if pred[t] != col[t])
        blocks = []
        for k in range(1, 13):
            lo, hi = (1 << k) + 1, (1 << (k + 1))
            vals = {col[t] for t in range(lo, hi + 1) if t % 2 == 1}
            blocks.append((k, sorted(vals)))
        print(f"CHECK B4 closed form l_t = [t odd] * (floor(log2(t-1)) mod 2) vs simulation, t<=8192: mismatches={mism}; "
              f"odd-t values per dyadic block (k, values): {blocks}")
    # B5 rerun A1 at non-dyadic T
    T = 3001
    D = drives(5, 1, T + 3)
    for rule in (30, 90):
        runs = 0
        h = 0
        ex = None
        for y in range(64):
            y_int = y << 1
            for w, pref, c in D:
                if y_int == 0 and 1 not in c:
                    continue
                runs += 1
                cols = lhp_column_minus_one(rule, y_int, c, T)
                q = periodic_on_tail(cols[0], T, 256)
                if q is not None:
                    h += 1
                    if ex is None:
                        ex = (y, w, pref, q)
        print(f"CHECK B5 rule {rule}: A1 rerun at non-dyadic T={T} (window [1500,3001]), q<=256: runs={runs} hits={h} first_hit={ex}")
    print(f"DONE [{time.time() - t0:.0f}s]")


if __name__ == '__main__':
    main()
