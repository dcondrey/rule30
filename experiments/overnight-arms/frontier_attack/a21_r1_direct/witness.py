"""a21 step 6: the explicit witness that makes eps(m) > 0 a THEOREM for all m.

THEOREM W.  Fix m >= 1.  In the quarter-plane block used by Theorem S, take the
boundary word gamma = 0^m and the hidden block w = (0,...,0,b) with the single
free bit b in the LAST slot, w_{m+1} = s(t-m, m+1) = b.  Then after m steps
r_t = s(t,1) = b.  Consequently, for every m, r_t is NOT a function of
(c_{t-m},...,c_{t-1}) alone, and

    eps(m) >= 2^{-(2m+1)} > 0.

Proof.  With all of row 1..m+1 zero except the last cell, one step of rule 30
gives, at position m, 0 XOR (0 OR b) = b, and 0 elsewhere; the block shortens by
one from the right, so the shape (0,...,0,b) is reproduced.  Induction gives
the single cell b after m steps.  Rule 90 is identical: at position m,
0 XOR b = b.  QED.

THEOREM N (rule 90 only).  eps_90(m) = 1/2 exactly for every m >= 1.
Proof.  Rule 90's quarter-plane map is GF(2)-linear, so r_t = L(gamma) XOR M(w)
with L, M linear.  Theorem W shows M has a nonzero coefficient on w_{m+1}, so M
is a nonzero linear form and M(w) is uniform under uniform w, independently of
gamma.  Hence r_t | gamma is uniform and the Bayes error is exactly 1/2.  QED.

Both theorems are verified below by direct computation.  Note that Theorem W is
RULE-GENERIC: it holds for rule 90 too.  That is stated, not hidden; see the
write-up's discussion of what the Rule 90 filter does and does not bite on.

Usage: uv run python witness.py > witness_output.txt
"""

from __future__ import annotations

import itertools
import random
import sys


def step_block(row: list[int], g: int, rule: int) -> list[int]:
    new = []
    for i in range(len(row) - 1):
        left = g if i == 0 else row[i - 1]
        new.append(left ^ (row[i] | row[i + 1]) if rule == 30 else left ^ row[i + 1])
    return new


def run_block(gamma: list[int], w: list[int], rule: int) -> int:
    row = list(w)
    for g in gamma:
        row = step_block(row, g, rule)
    assert len(row) == 1
    return row[0]


def main() -> None:
    print("a21 / witness.py -- Theorem W (eps(m) > 0 for all m) and Theorem N\n")

    print("Theorem W witness: gamma = 0^m, w = (0,...,0,b)  =>  r_t = b")
    for rule in (30, 90):
        bad = 0
        for m in range(1, 65):
            for b in (0, 1):
                w = [0] * m + [b]
                if run_block([0] * m, w, rule) != b:
                    bad += 1
        print(f"  rule {rule}: m = 1..64, both b: {bad} failures")
        assert bad == 0

    print("\nTheorem W consistency with the block simulator used by eps_theorem.py:")
    # the block simulator must agree with a genuine rule-30 diagram
    from substrate import cell, diagram, left_supported_row

    rng = random.Random(99)
    for rule in (30, 90):
        bad = 0
        for _ in range(3000):
            m = rng.randint(1, 8)
            t = rng.randint(2 * m + 1, 2 * m + 6)
            n = t + 1
            K = n + 2
            bits = [rng.randint(0, 1) for _ in range(n)]
            rows = diagram(left_supported_row(bits, K), K, t, rule)
            gamma = [cell(rows[t - m + j], t - m + j, 0, K) for j in range(m)]
            w = [cell(rows[t - m], t - m, 1 + i, K) for i in range(m + 1)]
            if run_block(gamma, w, rule) != cell(rows[t], t, 1, K):
                bad += 1
        print(f"  rule {rule}: 3000 random (m,t,row) triples, {bad} mismatches")
        assert bad == 0

    print("\nRealisability of the Theorem W witness by ACTUAL left-supported rows")
    print("(Theorem U guarantees every (gamma,w) occurs; this exhibits the pair):")
    for rule in (30, 90):
        for m in (2, 3, 4, 5):
            t = 2 * m + 1
            n = t + 1
            K = n + 2
            found = {}
            for v in range(1, 1 << n):  # v = 0 is the all-zero row; excluded
                bits = [(v >> j) & 1 for j in range(n)]
                rws = diagram(left_supported_row(bits, K), K, t, rule)
                gam = tuple(cell(rws[t - m + j], t - m + j, 0, K) for j in range(m))
                if any(gam):
                    continue
                w = tuple(cell(rws[t - m], t - m, 1 + i, K) for i in range(m + 1))
                if w[:-1] != tuple([0] * m):
                    continue
                key = w[-1]
                if key not in found:
                    found[key] = (bits, cell(rws[t], t, 1, K))
            assert set(found) == {0, 1}, (rule, m, found)
            (b0, r0), (b1, r1) = found[0], found[1]
            assert r0 == 0 and r1 == 1, (rule, m, r0, r1)
            print(
                f"  rule {rule} m={m} t={t}: gamma=0^{m}, both hidden blocks realised; "
                f"b=(s(0,0),s(0,-1),..) = {b0} -> r_t=0   {b1} -> r_t=1"
            )

    print("\nTheorem N check: rule 90, r_t is affine in (gamma, w); "
          "coefficient of w_{m+1} is 1")
    for m in range(1, 13):
        base = run_block([0] * m, [0] * (m + 1), 90)
        coeffs_w = []
        for i in range(m + 1):
            w = [0] * (m + 1)
            w[i] = 1
            coeffs_w.append(run_block([0] * m, w, 90) ^ base)
        # affinity check: exhaustive for small m
        ok = True
        if m <= 6:
            for gam in itertools.product((0, 1), repeat=m):
                cg = 0
                for j in range(m):
                    e = [0] * m
                    e[j] = 1
                    cg ^= (run_block(e, [0] * (m + 1), 90) ^ base) & gam[j]
                for w in itertools.product((0, 1), repeat=m + 1):
                    pred = base ^ cg
                    for i in range(m + 1):
                        pred ^= coeffs_w[i] & w[i]
                    if pred != run_block(list(gam), list(w), 90):
                        ok = False
        print(f"  m={m:2d}: coeff(w_{{m+1}}) = {coeffs_w[-1]}, "
              f"w-coefficients {coeffs_w}, affine={ok if m <= 6 else 'not tested'}")
        assert coeffs_w[-1] == 1 and ok

    print("\nRule 30 contrast: the same coefficient probe is meaningless because "
          "r_t is NOT affine.")
    for m in (2, 3, 4):
        base = run_block([0] * m, [0] * (m + 1), 30)
        nonaffine = 0
        coeffs_w = []
        for i in range(m + 1):
            w = [0] * (m + 1)
            w[i] = 1
            coeffs_w.append(run_block([0] * m, w, 30) ^ base)
        for w in itertools.product((0, 1), repeat=m + 1):
            pred = base
            for i in range(m + 1):
                pred ^= coeffs_w[i] & w[i]
            if pred != run_block([0] * m, list(w), 30):
                nonaffine += 1
        print(f"  m={m}: gamma=0^m, {nonaffine} of {2**(m+1)} hidden blocks "
              f"violate affinity")
        assert nonaffine > 0

    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
