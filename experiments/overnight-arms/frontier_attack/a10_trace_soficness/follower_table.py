"""Two-dimensional follower-set table f(n, m) for the width-2 column subshift.

f(n, m) = #{ F_m(w) : w in L_n },  F_m(w) = { u in Sigma^m : wu in L_{n+m} }.

READ THE CAVEAT WITH EVERY NUMBER (obstruction H).  Distinct F_m => distinct
full follower set F, so f(n,m) is a LOWER BOUND on the number of follower sets
of the subshift, and it is monotone nondecreasing in n and in m.  Therefore:
  * f bounded over the computed region does NOT prove sofic;
  * f growing over the computed region does NOT prove non-sofic, because
    proving non-soficness needs a family of words with pairwise distinct
    followers that is uniform in n and m -- exactly the ingredient we lack.
The LANGUAGE L_N is exact (light-cone enumeration); only the follower
truncation at m is an approximation.

Run: uv run python follower_table.py --k 2 --N 12
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


CHUNK = 1 << 23


def language_words(n: int, k: int, rule: str) -> np.ndarray:
    """Exact L_n, chunked so the window may exceed RAM-sized arrays."""
    w = 2 * n + k - 2
    if w > 32:
        raise ValueError(f"window {w} too wide")
    mask = (1 << w) - 1
    base = np.uint64(n - 1)
    total = 1 << w
    acc = np.zeros(0, dtype=np.uint64)
    for lo in range(0, total, CHUNK):
        hi = min(lo + CHUNK, total)
        c = np.arange(lo, hi, dtype=np.uint64)
        out = np.zeros(hi - lo, dtype=np.uint64)
        for t in range(n):
            for j in range(k):
                out |= ((c >> (base + np.uint64(j))) & np.uint64(1)) << np.uint64(t * k + j)
            if t + 1 < n:
                c = step(c, mask, rule)
        acc = np.unique(np.concatenate((acc, np.unique(out))))
    return acc


def followers(words: np.ndarray, n: int, k: int) -> int:
    """#distinct follower sets among length-n prefixes of `words`."""
    shift = np.uint64(n * k)
    pref = words & np.uint64((1 << (n * k)) - 1)
    suf = words >> shift
    order = np.argsort(pref, kind="stable")
    p_s, s_s = pref[order], suf[order]
    bounds = np.flatnonzero(np.diff(p_s)) + 1
    starts = np.concatenate(([0], bounds))
    ends = np.concatenate((bounds, [len(p_s)]))
    return len({np.unique(s_s[a:b]).tobytes() for a, b in zip(starts, ends)})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=2)
    ap.add_argument("--N", type=int, default=12)
    ap.add_argument("--rules", type=str, default="30,90")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    k, N = args.k, args.N

    out = {}
    for rule in args.rules.split(","):
        cache = {L: language_words(L, k, rule) for L in range(2, N + 1)}
        tab = {}
        log.info("rule %s, k=%d   f(n,m) lower bounds  (rows n, cols m)", rule, k)
        header = "  n\\m " + "".join(f"{m:>8d}" for m in range(1, N))
        log.info(header)
        for n in range(1, N):
            row = []
            for m in range(1, N - n + 1):
                val = followers(cache[n + m], n, k)
                tab[f"{n},{m}"] = val
                row.append(val)
            log.info("  %3d " + "".join(f"{v:>8d}" for v in row), n)
        out[rule] = tab
    (here / "out" / f"follower_table_k{k}_N{N}.json").write_text(json.dumps(
        {"caveat": "LOWER BOUNDS on the number of follower sets; truncated at m. "
                   "Neither boundedness nor growth over this finite region "
                   "decides soficness (obstruction H).",
         "k": k, "N": N, "table": out}, indent=1))
    log.info("wrote out/follower_table_k%d_N%d.json", k, N)


if __name__ == "__main__":
    main()
