#!/usr/bin/env python3
"""RW margin census with the prefix restricted to actual-right factor languages.

The period-two application (RESULTS-LATE-PULL-DIAGONAL.md section 2 and
RESULTS-ACTUAL-RIGHT-FRONTIER.md section 3) supplies, for a pull at absolute
position m = 3n + r with n larger than the artificial rank-descent prefix, a
factor f = e[n : 2n + r + 2] of the ACTUAL right trace.  So it is sound for
that application to restrict the whole word f (prefix and forced suffix) to
any superset of the actual right trace language R.  This script measures the
deepest run of target cells when the prefix W and the forced continuation are
restricted to the finite-type supersets

    HC   : bits avoid 11                       (symbol 1 = bit 1, 2 = bit 0)
    R5   : bits avoid 11, 00000
    R11  : bits avoid every minimal forbidden factor through length 11
           (RESULTS-RIGHT-FILTERED-MORTALITY.md section list)
    R13  : R11 plus the SAT-audited length 12 and 13 factors of
           RESULTS-ACTUAL-RIGHT-FRONTIER.md section 6

Each is a superset of R, so the deepest run reported is an upper bound on the
deepest run any genuine actual-right factor achieves, and a slack lower bound.

Output per (language, n, c): |L_n|, deepest run, need = n + 2 (r = 0, the
hardest case), and the survivor counts N_k with the E-ok fraction per level.
The forced kernel is the column recursion gated against psi_kernel.psi in
forced_symbol_census.py.
"""

from __future__ import annotations

import argparse
import sys
import time

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE  # noqa: E402

FORBIDDEN = {
    "HC": ["11"],
    "R5": ["11", "00000"],
    "R11": [
        "11",
        "00000",
        "101001",
        "0100101",
        "010010001",
        "0101000101",
        "0101010000",
        "01010001001",
        "10010001001",
    ],
}
FORBIDDEN["R13"] = FORBIDDEN["R11"] + [
    "010010000101",
    "010100010001",
    "100100010000",
    "0001000010001",
    "1001000010001",
]

# Orientation control: the same factors reversed.  The lemma uses the repo's
# convention (constant_tail_actual_frontier.endpoint_bits: e_0 is the earliest
# rho bit); if the two runs differed materially the orientation would matter.
FORBIDDEN["R13rev"] = [f[::-1] for f in FORBIDDEN["R13"]]


def bit_of(symbol: int) -> str:
    return "1" if symbol == 1 else "0"


def allowed(bits: str, forbidden: list[str]) -> bool:
    return not any(bits.endswith(f) for f in forbidden)


def run(language: str, n: int, c: int, extra: int = 0) -> dict:
    forbidden = FORBIDDEN[language]
    target_e = 0 if c == 2 else 1
    steps = n + 2 + extra
    counts = [0] * (steps + 1)
    eok_at = [0] * steps  # number of nodes at level j (surviving to j) with E ok
    lang_at = [0] * steps  # number of nodes at level j whose forced symbol keeps the language
    deepest = 0
    witness = ""
    prefixes = 0

    def forced(col: list[int], bits: str) -> None:
        nonlocal deepest, witness, prefixes
        prefixes += 1
        col = col[:]
        k = 0
        counts[0] += 1
        word = bits
        while k < steps:
            u = n + k
            zeros = col.count(0)
            high = (n + u + zeros) & 1
            e = 2 if high else 1
            new = [0] * (n + u + 2)
            new[0] = e
            new[1] = e ^ 3
            for i in range(2, n + u + 2):
                new[i] = CONE[col[i - 2]][new[i - 1]]
            cell = new[n + u + 1]
            defect = 1 ^ (cell >> 1) ^ (cell & 1)
            word = word + bit_of(e)
            ok_lang = allowed(word, forbidden)
            ok_e = defect == target_e
            if ok_e:
                eok_at[k] += 1
            if ok_lang:
                lang_at[k] += 1
            if not (ok_e and ok_lang):
                break
            k += 1
            counts[k] += 1
            col = new[: n + u + 1]
        if k > deepest:
            deepest = k
            witness = word

    def dfs(u: int, col: list[int], bits: str) -> None:
        if u == n:
            forced(col, bits)
            return
        for e in (1, 2):
            nb = bits + bit_of(e)
            if not allowed(nb, forbidden):
                continue
            new = [0] * (2 * u + 2)
            new[0] = e
            new[1] = e ^ 3
            for i in range(2, 2 * u + 2):
                new[i] = CONE[col[i - 2]][new[i - 1]]
            dfs(u + 1, new, nb)

    dfs(0, [], "")
    return {
        "language": language,
        "n": n,
        "c": c,
        "prefixes": prefixes,
        "deepest": deepest,
        "need": n + 2,
        "counts": counts,
        "eok_at": eok_at,
        "lang_at": lang_at,
        "witness": witness,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--languages", default="HC,R5,R11,R13")
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=20)
    ap.add_argument("--detail", action="store_true", help="print N_k tables")
    args = ap.parse_args()
    for language in args.languages.split(","):
        print(f"##### language {language}: forbidden bit factors {FORBIDDEN[language]}")
        print(" n  c  |L_n|   deepest  need  slack  deepest/n   witness(bits, prefix|forced)")
        for n in range(args.min_n, args.max_n + 1):
            for c in (2, 3):
                t0 = time.time()
                res = run(language, n, c)
                w = res["witness"]
                wit = w[:n] + "|" + w[n:]
                print(
                    f"{n:2d}  {c}  {res['prefixes']:7d}  {res['deepest']:5d}  {res['need']:4d}  "
                    f"{res['need'] - res['deepest']:4d}   {res['deepest'] / n:6.3f}   {wit}   ({time.time() - t0:.1f}s)"
                )
                if args.detail:
                    cs = res["counts"]
                    line = "    k:N_k(Eok frac, lang frac): "
                    for k in range(len(cs)):
                        if cs[k] == 0:
                            break
                        if k < len(res["eok_at"]) and cs[k]:
                            line += f" {k}:{cs[k]}({res['eok_at'][k] / cs[k]:.2f},{res['lang_at'][k] / cs[k]:.2f})"
                    print(line)
                sys.stdout.flush()


if __name__ == "__main__":
    main()
