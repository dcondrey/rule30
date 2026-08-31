"""a21 step 3: how hard does phi_t depend on the DISTANT past of c?

phi_anf.py established that phi_t exists and (rule 30) has full ANF support:
every c_j, j = 0..t-1, occurs in some monomial.  Formal occurrence is weak
evidence on its own -- a variable can occur in the ANF and have tiny influence.
Two exact quantities are computed here, both over the UNIFORM measure on the
2^t c-prefixes (exact counting, no sampling):

  1. INFLUENCE  Inf_j(phi_t) = Pr[ phi_t(c) != phi_t(c XOR e_j) ].
     Inf_j = 0 iff c_j does not occur in the ANF at all.

  2. BEST BOUNDED-WINDOW APPROXIMATION.  For a window width m, the minimum
     error of ANY function of the m most recent inputs c_{t-m}..c_{t-1}:
         err(m) = 2^-t * sum over the 2^m blocks of min(#ones, #zeros).
     err(m) = 0 for some bounded m is EXACTLY the hypothesis that would make
     Lemma Z immediate.  err(m) -> 1/2 says the recent window carries nothing.
     This is the exact, whole-distribution version of a19's sampled 0.4993.

Rule 90 is the live control: its Lemma-Z analogue is PROVED FALSE (a1 section 2,
Kummer), so its err(m) must NOT vanish at bounded m either.  If it did, the
method would be proving a false statement.

Usage: uv run python phi_reach.py [tmax] > phi_reach_output.txt
"""

from __future__ import annotations

import json
import sys

from phi_anf import build_table


def influences(table: bytearray, t: int) -> list[float]:
    out = []
    n = 1 << t
    for j in range(t):
        bit = 1 << j
        d = 0
        for idx in range(n):
            if idx & bit:
                d += table[idx] != table[idx ^ bit]
        out.append(2 * d / n)
    return out


def window_error(table: bytearray, t: int) -> list[float]:
    """err(m) for m = 0..t, using the m most recent inputs c_{t-m}..c_{t-1}."""
    n = 1 << t
    out = []
    for m in range(t + 1):
        blk = 1 << (t - m)
        err = 0
        for b in range(1 << m):
            ones = 0
            base = b * blk
            for i in range(base, base + blk):
                ones += table[i]
            err += min(ones, blk - ones)
        out.append(err / n)
    return out


def main() -> None:
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    print("a21 / phi_reach.py -- exact influence and bounded-window error of phi_t")
    print(f"tmax = {tmax}\n")
    res = {}
    for rule in (30, 90):
        print(f"=== rule {rule}: influence Inf_j(phi_t), j indexed from the OLDEST ===")
        print("   t | Inf_0   Inf_1   Inf_2   ...  (Inf_{t-1} is always 1.0)")
        rows = {}
        for t in range(1, tmax + 1):
            table, ok = build_table(t, rule)
            assert ok
            inf = influences(table, t)
            we = window_error(table, t)
            rows[t] = {"influence": inf, "window_error": we}
            head = "  ".join(f"{v:.4f}" for v in inf[: min(6, t)])
            print(f"  {t:2d} | {head}   (min over j: {min(inf):.4f})")
        print()
        print(f"=== rule {rule}: err(m), best predictor of r_t from the m most recent c ===")
        print("   t | m=1     m=2     m=3     m=4     m=6     m=8     | smallest m with err=0")
        for t in range(1, tmax + 1):
            we = rows[t]["window_error"]
            cells = []
            for m in (1, 2, 3, 4, 6, 8):
                cells.append(f"{we[m]:.4f}" if m <= t else "  --  ")
            zero = next((m for m in range(t + 1) if we[m] == 0.0), None)
            print(f"  {t:2d} | {'  '.join(cells)} | {zero}")
        print()
        res[str(rule)] = rows
    with open("phi_reach_results.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote phi_reach_results.json")


if __name__ == "__main__":
    main()
