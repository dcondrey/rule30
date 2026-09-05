#!/usr/bin/env python3
"""Counting-lemma threat table from the complete RW census JSONs (n = 7..33).

Skeptic lens, second pass, 2026-09-02.  Reads the census written by
`rw_bitsliced.py` (census_n07_20.json, census_n21_30.json, census_n31.json,
census_n32.json, census_n33.json) and tabulates, per (n, c):

  deepest        deepest admissible run (E-hit and hard-core at every column)
  R_all          max over k >= 1 of N_k / 2^(n-k)      (Lemma A: must be <= 1)
  R_deep         max over k >= 2 of N_k / 2^(n-k), with its argmax k
  R_last         N_deepest / 2^(n-deepest)             (the fiber of the last state
                                                        against its headroom)
  sup_lambda     sup_k N_k 2^(lambda k - n) for lambda in {1.1, 1.2, 1.3}
  B-margin       log2 Q_n - deepest, where Q_n is the number of distinct
                 forced-process states at k = 0 (exact from quotient_multiplicity
                 and state_survival logs for n <= 20; extrapolated at the fitted
                 rate 1.766^n beyond, marked with *)

Lemma A (N_k <= 2^(n-k) for all k, n >= 10) fails iff R_all > 1.
Lemma B (S_k <= Q_n 2^-k for all k, n >= 10) fails iff B-margin < 0.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/counting_threat.py
"""

from __future__ import annotations

import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

CENSUS_FILES = (
    "census_n07_20.json",
    "census_n21_30.json",
    "census_n31.json",
    "census_n32.json",
    "census_n33.json",
)


def load_census() -> dict:
    data = {}
    for fname in CENSUS_FILES:
        path = os.path.join(HERE, fname)
        if os.path.exists(path):
            data.update(json.load(open(path)))
    return data


def load_state_counts() -> dict[int, int]:
    """Q_n from quotient_multiplicity.log (n <= 16) and state_survival logs (17..20)."""
    q: dict[int, int] = {}
    path = os.path.join(HERE, "quotient_multiplicity.log")
    if os.path.exists(path):
        for line in open(path):
            m = re.match(r"^(\d+)\s+(\d+)\s+(\d+)\s+", line)
            if m:
                q[int(m.group(1))] = int(m.group(3))
    for fname in ("state_survival.log", "state_survival_n17_20.log", "state_survival_n6_9.log"):
        path = os.path.join(HERE, fname)
        if os.path.exists(path):
            for line in open(path):
                m = re.match(r"^n=(\d+)\s+c=\d\s+Q_n=(\d+)", line)
                if m:
                    q[int(m.group(1))] = int(m.group(2))
    return q


def main() -> None:
    data = load_census()
    qn = load_state_counts()
    # growth-rate fit for extrapolation
    ns = sorted(n for n in qn if n >= 12)
    rate = (qn[ns[-1]] / qn[ns[0]]) ** (1.0 / (ns[-1] - ns[0]))
    print(f"Q_n known exactly for n in {sorted(qn)}; fitted rate {rate:.4f} per n over n={ns[0]}..{ns[-1]}")
    print()
    hdr = (
        " n  c  deepest  d/n    R_all   R_deep (k)   R_last      sup1.1  sup1.2  sup1.3   log2Q_n  B-margin"
    )
    print(hdr)
    worst_all = (0.0, None)
    worst_deep = (0.0, None)
    worst_margin = (1e9, None)
    for key in sorted(data, key=lambda s: tuple(int(x) for x in s.split(","))):
        e = data[key]
        n, c, N = e["n"], e["c"], e["N"]
        deepest = max(k for k in range(len(N)) if N[k] > 0)
        r_all = max(N[k] / 2 ** (n - k) for k in range(1, len(N)) if N[k] > 0)
        deep = [(N[k] / 2 ** (n - k), k) for k in range(2, len(N)) if N[k] > 0]
        r_deep, k_deep = max(deep) if deep else (0.0, -1)
        r_last = N[deepest] / 2 ** (n - deepest)
        sups = []
        for lam in (1.1, 1.2, 1.3):
            sups.append(max(N[k] * 2 ** (lam * k - n) for k in range(0, len(N)) if N[k] > 0))
        if n in qn:
            lq = math.log2(qn[n])
            mark = " "
        else:
            base = max(m for m in qn if m <= 20)
            lq = math.log2(qn[base]) + (n - base) * math.log2(rate)
            mark = "*"
        margin = lq - deepest
        print(
            f"{n:<3}{c:<3}{deepest:<8} {deepest/n:5.2f}  {r_all:6.3f}  {r_deep:6.3f} ({k_deep:<2})  {r_last:8.4f}   "
            f"{sups[0]:6.2f}  {sups[1]:6.2f}  {sups[2]:6.2f}   {lq:6.2f}{mark}  {margin:6.2f}"
        )
        if n >= 10:
            if r_all > worst_all[0]:
                worst_all = (r_all, key)
            if r_deep > worst_deep[0]:
                worst_deep = (r_deep, key)
            if margin < worst_margin[0]:
                worst_margin = (margin, key)
    print()
    print(f"n >= 10: max R_all = {worst_all[0]:.3f} at (n,c)={worst_all[1]}  [Lemma A holds iff <= 1]")
    print(f"n >= 10: max R_deep = {worst_deep[0]:.3f} at (n,c)={worst_deep[1]}")
    print(f"n >= 10: min B-margin = {worst_margin[0]:.2f} at (n,c)={worst_margin[1]}  [Lemma B holds iff >= 0]")
    # small-n failures of Lemma A for the record
    fails = []
    for key in data:
        e = data[key]
        n, N = e["n"], e["N"]
        for k in range(1, len(N)):
            if N[k] > 2 ** (n - k):
                fails.append((n, e["c"], k, N[k], 2 ** (n - k)))
    print(f"all (n,c,k) with N_k > 2^(n-k): {sorted(fails)}")


if __name__ == "__main__":
    main()
