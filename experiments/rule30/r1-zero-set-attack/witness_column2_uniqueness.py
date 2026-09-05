"""Independent, from-scratch verification of the column-2 (non-)uniqueness
claim made in extract_r7_witness.py, for the R=1 pin witness at p=2.

Does NOT reuse ladder.verify_witness's logic; re-derives everything from the
raw forward rule s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)) applied at
x=1, which is the one elementary fact this whole check rests on:

    r_{t+1} = c_t XOR (r_t OR s(t,2))

At r_t = 1 the OR saturates, so BOTH values of s(t,2) give the same
r_{t+1}: genuine two-way freedom, not a modelling gap in my own code.
At r_t = 0, r_{t+1} = c_t XOR s(t,2), so exactly one value of s(t,2) works:
forced, matching the census's `literal_extension` uniqueness at every step.

This script takes the SAME witness extraction as extract_r7_witness.py
(re-run here standalone) and checks, cell by cell over the cyclic tail, that
this dichotomy holds exactly as claimed -- i.e. that "freedom" is not an
artifact of my forcing/free bookkeeping but a directly checkable fact about
the local rule applied to the witness's own (c,r) values.
"""

from __future__ import annotations

import importlib.util
import sys

_LADDER_DIR = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/ladder"


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ladder = _load("ladder", f"{_LADDER_DIR}/ladder.py")
rung1 = _load("rung1", f"{_LADDER_DIR}/rung1.py")


def rule30_x1(c_t: int, r_t: int, s2_t: int) -> int:
    """r_{t+1} via the raw local rule at x=1, written out with no shortcuts."""
    left, center, right = c_t, r_t, s2_t
    return left ^ (center | right)


def main():
    R, k, word, q = 1, 2, (0, 1), 1
    P = ladder.Params(rule=30, right_depth=R, left_depth=k, period_word=word, diff_q=q)
    res = rung1.decide_pin(P, True)
    assert res["verdict"] == "NONEMPTY"
    wit = res["witness"]
    okv, note = ladder.verify_witness(wit["prefix"], wit["cycle"], P)
    assert okv, note

    reps = 8
    letters = list(wit["prefix"]) + list(wit["cycle"]) * reps
    cols = {R: [ab & 1 for ab in letters], R - 1: [ab >> 1 for ab in letters]}
    inv = ladder.INV[30]
    x = R - 2
    while x >= P.x_min:
        up = cols[x + 1]
        upr = cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    c, r = cols[0], cols[1]

    tail0 = len(wit["prefix"])
    n_free_checked = 0
    n_forced_checked = 0
    free_violations = 0
    forced_wrong_unique = 0
    for t in range(tail0, len(r) - 1):
        want_next = r[t + 1]
        if r[t] == 1:
            # claim: BOTH s2 values reproduce want_next (freedom is real)
            v0 = rule30_x1(c[t], r[t], 0)
            v1 = rule30_x1(c[t], r[t], 1)
            n_free_checked += 1
            if not (v0 == want_next and v1 == want_next):
                free_violations += 1
        else:
            # claim: EXACTLY one s2 value reproduces want_next
            v0 = rule30_x1(c[t], r[t], 0)
            v1 = rule30_x1(c[t], r[t], 1)
            matches = [v for v in (0, 1) if rule30_x1(c[t], r[t], v) == want_next]
            n_forced_checked += 1
            if len(matches) != 1:
                forced_wrong_unique += 1

    print(f"witness R={R} k={k} w={word} q={q}: verified={okv} ({note})")
    print(f"cells with r_t=1 (claimed FREE at column 2): {n_free_checked}, "
          f"violations of 'both s2 values work': {free_violations}")
    print(f"cells with r_t=0 (claimed FORCED at column 2): {n_forced_checked}, "
          f"violations of 'exactly one s2 value works': {forced_wrong_unique}")
    print("CONCLUSION:",
          "confirmed -- genuine 2-way freedom at every r_t=1 cell, "
          "genuine forcing at every r_t=0 cell"
          if free_violations == 0 and forced_wrong_unique == 0
          else "UNEXPECTED -- see violation counts above, do not trust the claim")


if __name__ == "__main__":
    main()
