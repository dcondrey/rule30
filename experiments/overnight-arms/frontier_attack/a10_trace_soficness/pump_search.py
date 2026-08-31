"""Search for a PUMPED SEPARATING FAMILY in the width-2 column subshift of an ECA.

A shift space is non-sofic iff it has infinitely many follower sets.  The usual
way to exhibit that is a family w_1, w_2, ... of words in L with pairwise
distinct follower sets, given by explicit separating continuations:

    w_i v_j in L   <=>   i = j        (or any pairwise-distinguishing table).

If the family is PUMPED, w_j = x y^j z, one has a chance of proving the
separation for all j by induction -- which is the ingredient this arm is
missing.  This script does the finite half: it searches over short x, y, z for
families whose members have pairwise distinct m-TRUNCATED follower sets, and
prints an explicit separating continuation for every pair it separates.

SCOPE / OBSTRUCTION H.  Everything here is computed inside the exact language
L_N (light-cone enumeration, N given).  A family separated for j <= J and
truncation m is EVIDENCE ONLY; it becomes a theorem only with a proof of
separation uniform in j -- the named missing lemma.

Run: uv run python pump_search.py --N 14 --rule 30
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)
K = 2  # width


def step(c: np.ndarray, mask: int, rule: str) -> np.ndarray:
    left = (c << np.uint64(1)) & np.uint64(mask)
    right = c >> np.uint64(1)
    if rule == "30":
        return (left ^ (c | right)) & np.uint64(mask)
    if rule == "90":
        return (left ^ right) & np.uint64(mask)
    raise ValueError(rule)


CHUNK = 1 << 23


def language_words(n: int, rule: str) -> np.ndarray:
    w = 2 * n + K - 2
    mask = (1 << w) - 1
    base = np.uint64(n - 1)
    total = 1 << w
    acc = np.zeros(0, dtype=np.uint64)
    for lo in range(0, total, CHUNK):
        hi = min(lo + CHUNK, total)
        c = np.arange(lo, hi, dtype=np.uint64)
        out = np.zeros(hi - lo, dtype=np.uint64)
        for t in range(n):
            for j in range(K):
                out |= ((c >> (base + np.uint64(j))) & np.uint64(1)) << np.uint64(t * K + j)
            if t + 1 < n:
                c = step(c, mask, rule)
        acc = np.unique(np.concatenate((acc, np.unique(out))))
    return acc


def cached_language(n: int, rule: str, here: pathlib.Path) -> np.ndarray:
    f = here / "out" / f"L_{rule}_k{K}_n{n}.npy"
    if f.exists():
        return np.load(f)
    a = language_words(n, rule)
    np.save(f, a)
    return a


def encode(letters: list[int]) -> int:
    v = 0
    for i, a in enumerate(letters):
        v |= a << (K * i)
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=14)
    ap.add_argument("--rule", type=str, default="30")
    ap.add_argument("--m", type=int, default=4)
    ap.add_argument("--maxj", type=int, default=6)
    ap.add_argument("--ylens", type=str, default="1,2")
    ap.add_argument("--minmembers", type=int, default=3)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    N, m = args.N, args.m

    words = set(int(x) for x in cached_language(N, args.rule, here))
    log.info("rule %s: |L_%d| = %d (exact)", args.rule, N, len(words))
    mask_n = {}
    for n in range(1, N + 1):
        mask_n[n] = (1 << (K * n)) - 1
    prefixes = {n: {w & mask_n[n] for w in words} for n in range(1, N + 1)}

    def followers(w: int, n: int) -> frozenset:
        """Exact F_m(w) for |w| = n, valid because n + m <= N."""
        out = set()
        for u in itertools.product(range(4), repeat=m):
            cand = w | (encode(list(u)) << (K * n))
            if cand in prefixes[n + m]:
                out.add(u)
        return frozenset(out)

    best = []
    for ylen in [int(v) for v in args.ylens.split(",")]:
        for y in itertools.product(range(4), repeat=ylen):
            for xlen in (0, 1, 2):
                for x in itertools.product(range(4), repeat=xlen):
                    fam = []
                    for j in range(1, args.maxj + 1):
                        letters = list(x) + list(y) * j
                        n = len(letters)
                        if n + m > N:
                            break
                        w = encode(letters)
                        if w not in prefixes[n]:
                            break
                        fam.append((j, letters, followers(w, n)))
                    if len(fam) < args.minmembers:
                        continue
                    sets = [f for _, _, f in fam]
                    distinct = len({s for s in sets})
                    if distinct == len(sets):
                        best.append({
                            "x": list(x), "y": list(y),
                            "j_range": [fam[0][0], fam[-1][0]],
                            "members": len(fam),
                            "m": m,
                        })
    best.sort(key=lambda r: -r["members"])
    log.info("families with pairwise-distinct %d-truncated follower sets: %d",
             m, len(best))
    for r in best[:10]:
        log.info("  x=%s y=%s  j=%d..%d  (%d members, all distinct)",
                 r["x"], r["y"], r["j_range"][0], r["j_range"][1], r["members"])

    # explicit separating continuations for the longest family found
    detail = None
    if best:
        r = best[0]
        x, y = r["x"], r["y"]
        fam = []
        for j in range(r["j_range"][0], r["j_range"][1] + 1):
            letters = x + y * j
            fam.append((j, letters, followers(encode(letters), len(letters))))
        sep = []
        for (i, li, fi), (j, lj, fj) in itertools.combinations(fam, 2):
            d = sorted(fi ^ fj)
            sep.append({"i": i, "j": j, "witness": list(d[0]),
                        "in_F_i": tuple(d[0]) in fi})
        detail = {"x": x, "y": y, "family": [
            {"j": j, "word": li, "follower_size": len(fi)} for j, li, fi in fam],
            "separating_continuations": sep}
        log.info("longest family x=%s y=%s: follower sizes %s",
                 x, y, [len(f) for _, _, f in fam])
        for s in sep[:12]:
            log.info("  j=%d vs j=%d separated by continuation %s (in F_%d: %s)",
                     s["i"], s["j"], s["witness"], s["i"], s["in_F_i"])

    (here / "out" / f"pump_search_rule{args.rule}_N{N}_m{m}_y{args.ylens.replace(',','')}.json").write_text(
        json.dumps({"caveat": "finite evidence only; separation is verified for "
                              "the listed j and truncation m, NOT for all j",
                    "rule": args.rule, "N": N, "m": m,
                    "families": best, "detail": detail}, indent=1))
    log.info("wrote out/pump_search_rule%s_N%d_m%d_y%s.json", args.rule, N, m,
             args.ylens.replace(",", ""))


if __name__ == "__main__":
    main()
