"""a21 step 5: why err(m,t) stabilises in t, and eps(m) to much larger m.

THEOREM U (proved in the write-up, verified exhaustively here).  Let the initial
row be LEFT-SUPPORTED (s(0,x)=0 for x >= 1) with bits b_j = s(0,-j) drawn
uniformly.  Fix t and k <= t.  Then

    (s(t,0), s(t,1), ..., s(t,k))  is EXACTLY uniform on {0,1}^{k+1},

because s(t,x) = b_{t-x} XOR (a function of b_0..b_{t-x-1}) by left permutivity,
so the map (b_{t-k},...,b_t) -> (s(t,k),...,s(t,0)) is triangular with unit
diagonal at every fixed value of the earlier bits.  Rule 90 has the same
property; Theorem U is NOT rule-specific.

THEOREM S (corollary; this is the new content).  For t >= 2m+1,

    err(m,t) = eps(m),  independent of t,

where eps(m) is the Bayes error of predicting r_t from m boundary bits
gamma = (c_{t-m},...,c_{t-1}) when the m+1 hidden bits
w = (s(t-m,1),...,s(t-m,m+1)) are uniform and independent of gamma.
Reason: the quarter plane x >= 1 is driven forward by the boundary column x = 0,
its dependence cone from time t-m to time t needs exactly s(t-m,1..m+1), and by
Theorem U that block is uniform and independent of the fresh bits
b_{t-m},...,b_{t-1} that carry c_{t-m},...,c_{t-1}.

eps(m) is then a FIXED finite quantity, computable at 2^(2m+1) cost, with no
reference to t at all.  That is what lets this script reach m = 16 where the
direct 2^t enumeration of phi_epsilon.py stops at t = 21, i.e. m ~ 10.

Usage: uv run python eps_theorem.py [mmax] > eps_theorem_output.txt
"""

from __future__ import annotations

import itertools
import json
import random
import sys

from substrate import cell, diagram, left_supported_row


def verify_theorem_u(tmax: int = 12) -> None:
    """Exhaustive check that (s(t,0..k)) is uniform for k <= t, both rules."""
    for rule in (30, 90):
        worst = 0
        for t in range(1, tmax + 1):
            n = t + 1
            K = n + 2
            for k in range(0, t + 1):
                counts = [0] * (1 << (k + 1))
                for v in range(1 << n):
                    row0 = left_supported_row([(v >> j) & 1 for j in range(n)], K)
                    rows = diagram(row0, K, t, rule)
                    idx = 0
                    for x in range(k + 1):
                        if cell(rows[t], t, x, K):
                            idx |= 1 << x
                    counts[idx] += 1
                exp = (1 << n) >> (k + 1)
                worst = max(worst, max(abs(c - exp) for c in counts))
        print(f"Theorem U, rule {rule}: t<={tmax}, all k<=t, max deviation from "
              f"exact uniformity = {worst}")
        assert worst == 0


def eps(m: int, rule: int) -> tuple[int, int]:
    """(numerator, denominator) of eps(m), by bitslicing over the 2^(m+1) hidden
    blocks for each of the 2^m boundary words."""
    nh = m + 1
    size = 1 << nh
    # variable masks: bit v of var[x] is bit x of v
    var = []
    for x in range(nh):
        mask = 0
        block = 1 << x
        v = 0
        while v < size:
            if v & block:
                mask |= 1 << v
            v += 1
        var.append(mask)
    full = (1 << size) - 1
    num = 0
    for g in range(1 << m):
        row = list(var)  # row[i] = s(., 1+i), i = 0..m
        for j in range(m):
            gj = full if (g >> j) & 1 else 0
            new = []
            for i in range(len(row) - 1):
                left = gj if i == 0 else row[i - 1]
                if rule == 30:
                    new.append(left ^ (row[i] | row[i + 1]))
                else:
                    new.append(left ^ row[i + 1])
            row = new
        assert len(row) == 1
        ones = bin(row[0]).count("1")
        num += min(ones, size - ones)
    return num, 1 << (2 * m + 1)


def main() -> None:
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print("a21 / eps_theorem.py -- Theorem U, Theorem S, and eps(m) to large m\n")
    verify_theorem_u(11)
    print()

    print("Cross-check of Theorem S against the direct enumeration in")
    print("phi_epsilon_results.json (err(m,t) for t >= 2m+1 must equal eps(m)):")
    try:
        direct = json.load(open("phi_epsilon_results.json"))
    except FileNotFoundError:
        direct = None
        print("  phi_epsilon_results.json not present; run phi_epsilon.py first")
    out = {}
    for rule in (30, 90):
        print(f"\n=== rule {rule} ===")
        print("   m |    eps(m)    | exact fraction        | direct err(m,t) for t>=2m+1")
        vals = {}
        for m in range(1, mmax + 1):
            num, den = eps(m, rule)
            e = num / den
            vals[m] = [num, den]
            chk = "n/a"
            if direct is not None:
                ts = [t for t in range(2 * m + 1, 22)]
                got = {direct[str(rule)][str(t)][m] for t in ts if str(t) in direct[str(rule)]}
                if got:
                    ok = all(abs(x - e) < 1e-12 for x in got)
                    chk = f"{'MATCH' if ok else 'MISMATCH'} t={ts[0]}..21 {sorted(got)[:2]}"
                    assert ok, (rule, m, e, got)
            print(f"  {m:2d} | {e:.9f}  | {num}/{den:<18d} | {chk}")
            sys.stdout.flush()
        out[str(rule)] = vals
    with open("eps_theorem_results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote eps_theorem_results.json")


if __name__ == "__main__":
    main()
