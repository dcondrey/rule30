"""a21 step 2, the discriminator: the exact function  r_t = phi_t(c_0..c_{t-1}).

CLAIM (verified below, not assumed).  Let s(0,.) be any configuration that is
LEFT-SUPPORTED, i.e. s(0,x) = 0 for every x >= 1.  The lone seed is one.  Write
c_t = s(t,0), r_t = s(t,1).  Then for every t >= 1 there is a single function

    phi_t : {0,1}^t -> {0,1},      r_t = phi_t(c_0, ..., c_{t-1})

the SAME function for every left-supported initial row.

WHY (proof; the script checks every step of it exhaustively).  Because
s(0,x)=0 for x >= 1, the cell s(t,x) depends only on s(0, x-t .. 0), i.e. on
b_j := s(0,-j) for 0 <= j <= t-x.  So r_t = s(t,1) is a function of b_0..b_{t-1}
and c_0..c_{t-1} is a function of b_0..b_{t-1}.  Left permutivity (a7 Lemma P)
makes b |-> c triangular with unit diagonal, hence a bijection on {0,1}^t.
Compose.  QED.

WHY IT MATTERS.  R1 / Lemma Z asks: does c eventually p-periodic force r
eventually p-periodic on {t : c_t = 0}?  Since r_t = phi_t(c_0..c_{t-1})
UNCONDITIONALLY, the entire question is a question about the ANF support of
phi_t.  If phi_t depended only on c_{t-m}..c_{t-1} for a bounded m, Lemma Z
would be immediate: a bounded-window function of an eventually periodic word is
eventually periodic.  So the discriminator is:

    how far back into c does phi_t actually reach?

This is an UNCONDITIONAL object.  It has no periodicity hypothesis, so it is not
subject to the vacuity that afflicts every conditional formulation (see the
write-up).  Obstruction H still binds any *extrapolation* of the table.

Usage: uv run python phi_anf.py > phi_anf_output.txt
"""

from __future__ import annotations

import json
import random
import sys

from substrate import cell, diagram, left_supported_row


def build_table(t: int, rule: int, extra_left: int = 0) -> tuple[bytearray, bool]:
    """Truth table of r_t indexed by the integer sum_j c_j << j.

    Enumerates all 2^(t+extra_left) left-supported rows with bits b_0..b_{t-1+extra}.
    Returns (table, well_defined).  well_defined is False if two rows share a
    c-prefix but disagree on r_t -- i.e. if phi_t does not exist.
    """
    n = t + extra_left
    K = n + 2
    size = 1 << t
    table = bytearray(size)
    seen = bytearray(size)
    ok = True
    for v in range(1 << n):
        row0 = left_supported_row([(v >> j) & 1 for j in range(n)], K)
        rows = diagram(row0, K, t, rule)
        idx = 0
        for j in range(t):
            if cell(rows[j], j, 0, K):
                idx |= 1 << j
        r = cell(rows[t], t, 1, K)
        if seen[idx]:
            if table[idx] != r:
                ok = False
        else:
            seen[idx] = 1
            table[idx] = r
    if extra_left == 0 and not all(seen):
        ok = False  # the b -> c map failed to be onto: bijection claim broken
    return table, ok


def moebius(table: bytearray, t: int) -> bytearray:
    """In-place ANF (Moebius) transform: coefficient of monomial `mask`."""
    a = bytearray(table)
    for j in range(t):
        bit = 1 << j
        for idx in range(1 << t):
            if idx & bit:
                a[idx] ^= a[idx ^ bit]
    return a


def analyse(anf: bytearray, t: int) -> dict:
    mons = [m for m in range(1 << t) if anf[m]]
    support = set()
    for m in mons:
        mm = m
        while mm:
            b = mm & -mm
            support.add(b.bit_length() - 1)
            mm ^= b
    deg = max((bin(m).count("1") for m in mons), default=0)
    top = t - 1
    top_linear = (1 << top) in set(mons) if t >= 1 else False
    top_only_linear = all(not (m & (1 << top)) or m == (1 << top) for m in mons)
    return {
        "t": t,
        "n_monomials": len(mons),
        "degree": deg,
        "support_size": len(support),
        "min_var": min(support) if support else None,
        "max_var": max(support) if support else None,
        "depends_on_c0": 0 in support,
        "missing_vars": sorted(set(range(t)) - support),
        "reach": (t - min(support)) if support else 0,
        "c_top_linear_and_isolated": bool(top_linear and top_only_linear),
    }


def main() -> None:
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    print("a21 / phi_anf.py -- exact ANF of  r_t = phi_t(c_0..c_{t-1})")
    print(f"tmax = {tmax}\n")

    results = {}
    for rule in (30, 90):
        print(f"=== rule {rule} ===")
        print(
            "  t  well-def   deg  #monomials  supp  min_var  reach  dep(c_0)  "
            "missing vars                c_{t-1} linear+isolated"
        )
        rows = []
        for t in range(1, tmax + 1):
            table, ok = build_table(t, rule)
            anf = moebius(table, t)
            info = analyse(anf, t)
            info["well_defined"] = ok
            rows.append(info)
            miss = info["missing_vars"]
            miss_s = str(miss) if len(miss) <= 6 else f"{miss[:6]}... ({len(miss)})"
            print(
                f"  {t:2d}  {str(ok):8s} {info['degree']:4d}  {info['n_monomials']:10d}"
                f"  {info['support_size']:4d}  {str(info['min_var']):7s}"
                f"  {info['reach']:5d}  {str(info['depends_on_c0']):8s}  {miss_s:26s}"
                f"  {info['c_top_linear_and_isolated']}"
            )
        results[str(rule)] = rows
        print()

    # Independence of the extra left width: phi_t must not change when the row
    # carries free bits beyond b_{t-1}.
    print("=== arity / width independence (extra free bits b_t..b_{t+e-1}) ===")
    for rule in (30, 90):
        for t in (4, 6, 8, 10):
            for e in (1, 2, 3):
                ta, oka = build_table(t, rule, 0)
                tb, okb = build_table(t, rule, e)
                same = ta == tb
                print(
                    f"  rule {rule}  t={t:2d}  extra={e}  well-defined={okb}  "
                    f"identical to extra=0: {same}"
                )
                assert oka and okb and same, (rule, t, e)
    print()

    # Independence check on genuine wide random left-supported rows: phi_t
    # predicts r_t from the observed c-prefix.
    print("=== phi_t predicts r_t on random wide left-supported rows ===")
    rng = random.Random(30303)
    for rule in (30, 90):
        t = 14
        table, ok = build_table(t, rule)
        assert ok
        bad = 0
        for _ in range(2000):
            n = rng.randint(t, t + 25)
            bits = [rng.randint(0, 1) for _ in range(n)]
            K = n + 2
            rws = diagram(left_supported_row(bits, K), K, t, rule)
            idx = 0
            for j in range(t):
                if cell(rws[j], j, 0, K):
                    idx |= 1 << j
            bad += table[idx] != cell(rws[t], t, 1, K)
        print(f"  rule {rule}  t={t}: 2000 random rows, {bad} mispredictions")
        assert bad == 0
    print()

    with open("phi_anf_results.json", "w") as fh:
        json.dump(results, fh, indent=1)
    print("wrote phi_anf_results.json")


if __name__ == "__main__":
    main()
