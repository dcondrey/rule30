"""Follower-set ladder (Myhill-Nerode criterion) for the width-k column subshift.

Lind & Marcus criterion: a shift space is sofic iff its collection of follower
sets { F(w) = { u : wu in L } : w in L } is FINITE.

OBSTRUCTION H, stated in the same breath as every number below: we can only
compute the TRUNCATED follower set F_m(w) = { u in Sigma^m : wu in L }.  Two
words with distinct F_m have distinct F, so

    f(n, m) := #{ F_m(w) : w in L_n }   is a LOWER BOUND on #follower sets,

and it is monotone nondecreasing in both n and m.  Finitely many observed does
NOT prove sofic (a larger m could split classes).  Unboundedly many observed up
to (n, m) does NOT prove non-sofic without an argument uniform in n and m.

The language L itself is EXACT here (light-cone enumeration, see
width_k_language.py); only the follower TRUNCATION is an approximation.

Run: uv run python follower_ladder.py --k 2 --N 12
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)


def step(c: np.ndarray, mask: int, rule: str) -> np.ndarray:
    left = (c << np.uint64(1)) & np.uint64(mask)
    right = c >> np.uint64(1)
    if rule == "30":
        return (left ^ (c | right)) & np.uint64(mask)
    if rule == "90":
        return (left ^ right) & np.uint64(mask)
    raise ValueError(rule)


def language_words(n: int, k: int, rule: str) -> np.ndarray:
    """Exact L_n as ints; letter at time t occupies bits [t*k, t*k+k)."""
    w = 2 * n + k - 2
    if w > 26:
        raise ValueError(f"window {w} too wide for brute force")
    mask = (1 << w) - 1
    c = np.arange(1 << w, dtype=np.uint64)
    base = np.uint64(n - 1)
    out = np.zeros(1 << w, dtype=np.uint64)
    for t in range(n):
        for j in range(k):
            out |= ((c >> (base + np.uint64(j))) & np.uint64(1)) << np.uint64(t * k + j)
        if t + 1 < n:
            c = step(c, mask, rule)
    return np.unique(out)


def ladder(rule: str, k: int, N: int) -> list[dict]:
    """f(n, m) for all n + m = N, from the exact length-N language."""
    words = language_words(N, k, rule)
    log.info("rule %s k=%d: |L_%d| = %d (exact)", rule, k, N, len(words))
    rows = []
    for n in range(1, N):
        m = N - n
        shift = np.uint64(n * k)
        pref = words & np.uint64((1 << (n * k)) - 1)
        suf = words >> shift
        order = np.argsort(pref, kind="stable")
        p_s, s_s = pref[order], suf[order]
        # group by prefix, hash each follower set
        bounds = np.flatnonzero(np.diff(p_s)) + 1
        starts = np.concatenate(([0], bounds))
        ends = np.concatenate((bounds, [len(p_s)]))
        sets = set()
        for a, b in zip(starts, ends):
            sets.add(np.sort(s_s[a:b]).tobytes())
        rows.append({"n": n, "m": m, "prefixes": int(len(starts)),
                     "distinct_followers_lower_bound": len(sets)})
        log.info(
            "  n=%2d m=%2d  |L_n|=%7d  f(n,m) >= %6d",
            n, m, len(starts), len(sets),
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--N", type=int, default=12)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    res = {}
    for rule in ("30", "90"):
        res[rule] = ladder(rule, args.k, args.N)
    (here / "out" / f"follower_ladder_k{args.k}_N{args.N}.json").write_text(
        json.dumps({"caveat": "LOWER BOUND ONLY -- truncated follower sets; see "
                              "obstruction H", "k": args.k, "N": args.N,
                    "results": res}, indent=1))
    log.info("wrote out/follower_ladder_k%d_N%d.json", args.k, args.N)


if __name__ == "__main__":
    main()
