#!/usr/bin/env python3
"""Throwaway verification script for PREREGISTRATION-ENDPOINT-ENERGY-INVARIANT.md.

Executes Setup steps 1-4 and the required controls (section 6) of that
document.  Does NOT modify flip_pairing.py, peel_lift_monoid.py, or
constant_tail_frontier_graph.py -- it imports their existing objects
unmodified and adds new logging/analysis on top.

D8-class extraction (step 1): reuses, without modification, the exact
FIBER_PERMUTATIONS construction already used and already killed as a
per-step observer in constant_tail_frontier_graph.py ("path_monodromy",
lines ~162-170) and named in CONTINUATION-PROMPT.md lines 503-521 ("the
eight D8 prefix actions ... tested as deterministic weighted observers").
That construction is:

    FIBER_PERMUTATIONS[incoming] = tuple(LIFT_GENERATORS[state][incoming]
                                          for state in range(4))

built from peel_lift_monoid.LIFT_GENERATORS (unmodified import), and the
group these 4 permutations generate under peel_lift_monoid/dyadic_
periodicity_analyzer's `compose` is checked here (as it is in
constant_tail_frontier_graph.py) to be exactly the 8-element group
EXPECTED_FIBER_GROUP.

This script applies that *same* FIBER_PERMUTATIONS/compose machinery to a
*different* trace than constant_tail_frontier_graph.py used it on: instead
of the frontier's own projected state, it drives it with flip_pairing's own
forced-orbit `cells[w][j]` (the forced diagonal cell value in {0,1,2,3} at
level j, already computed by flip_pairing.census, completely unmodified).
sigma_j(w) is defined as the accumulated D8 group element after composing
in cells[w][0..j] in order, mapped to an index 0..7 via the fixed ordering
of EXPECTED_FIBER_GROUP. This is "the current D8 class of the forced step"
named in BACKLOG item 4 / CONTINUATION-PROMPT's killed weighted-potential
paragraph, applied here as a *running-sum* input rather than a per-step
snapshot bound, per section 3b of the preregistration.
"""
from __future__ import annotations

import sys
import time
from itertools import combinations

import numpy as np

from flip_pairing import census
from peel_lift_monoid import LIFT_GENERATORS
from dyadic_periodicity_analyzer import IDENTITY, compose
from constant_tail_frontier_graph import (
    FIBER_PERMUTATIONS as _REFERENCE_FIBER_PERMUTATIONS,
    EXPECTED_FIBER_GROUP,
    transformation_group,
)

# --- step 1: rebuild FIBER_PERMUTATIONS exactly as constant_tail_frontier_graph.py
# does (sanity: must equal the already-imported reference, byte for byte) ---
FIBER_PERMUTATIONS = tuple(
    tuple(LIFT_GENERATORS[state][incoming] for state in range(4)) for incoming in range(4)
)
assert FIBER_PERMUTATIONS == _REFERENCE_FIBER_PERMUTATIONS, "D8 class machinery diverged from constant_tail_frontier_graph.py"

GROUP = transformation_group(FIBER_PERMUTATIONS)
assert GROUP == EXPECTED_FIBER_GROUP, "generated group is not the expected 8-element D8"
assert len(GROUP) == 8
CLASS_ORDER = sorted(GROUP)  # fixed canonical order -> indices 0..7
CLASS_INDEX = {t: i for i, t in enumerate(CLASS_ORDER)}


def sigma_sequence(syms_w, levels: int) -> list[int]:
    """sigma_0(w), ..., sigma_{levels-1}(w): accumulated D8 class index after
    composing in syms_w[0..i], in order.

    IMPORTANT (found empirically, not assumed): the *cell* array
    (`cells[w][i]`, the emitted E-relevant state) is degenerate on the
    survivor population by construction -- w alive at level j means
    `cells[w][i] == c` for EVERY i<j, i.e. identical across every survivor,
    carrying zero per-w information (verified: Var=0 at every level, see
    results doc). The forced *symbol* (`syms[w][i] in {1,2}`, the RW binary
    alphabet used everywhere else in this project for W and the forced
    continuation) is NOT pinned by the alive condition and does vary across
    survivors (verified: 9 distinct length-5 prefixes among 33 survivors at
    n=12,c=2,j=5). sigma is therefore built from `syms`, using the same
    FIBER_PERMUTATIONS/compose D8 machinery, restricted to the {1,2} subset
    of its domain (a valid restriction: LIFT_GENERATORS/FIBER_PERMUTATIONS
    are indexed by all of range(4); syms only ever supplies 1 or 2, and
    composing any subset of the 4 generators stays inside the same
    8-element D8 group)."""
    action = IDENTITY
    out = []
    for i in range(levels):
        action = compose(FIBER_PERMUTATIONS[syms_w[i]], action)
        out.append(CLASS_INDEX[action])
    return out


def death_array(cells, hcs, total: int, c: int, levels: int) -> np.ndarray:
    d = np.full(total, levels, dtype=np.int32)
    for w in range(total):
        hc = hcs[w]
        cl = cells[w]
        for j in range(levels):
            if not hc[j] or cl[j] != c:
                d[w] = j
                break
    return d


def build_sigma_matrix(syms, total: int, levels: int) -> np.ndarray:
    sig = np.empty((total, levels), dtype=np.int8)
    for w in range(total):
        sig[w] = sigma_sequence(syms[w], levels)
    return sig


def score_and_prefix(sig: np.ndarray, F: frozenset) -> np.ndarray:
    """score[w,i] = +1 if sigma_i(w) in F else -1; prefix[w,j]=sum_{i<j} score[w,i]."""
    in_f = np.isin(sig, np.array(sorted(F), dtype=np.int8))
    score = np.where(in_f, 1, -1).astype(np.int32)
    total, levels = score.shape
    prefix = np.zeros((total, levels + 1), dtype=np.int32)
    np.cumsum(score, axis=1, out=prefix[:, 1:])
    return prefix


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    if x.size < 2 or np.std(x) == 0 or np.std(y) == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def pooled_k_label(prefix: np.ndarray, death: np.ndarray, levels: int):
    """Pool (k(w,j), died-at-j) over all j=0..levels-1, all alive w."""
    ks = []
    labels = []
    for j in range(levels):
        alive = death >= j
        if not np.any(alive):
            continue
        ks.append(prefix[alive, j])
        labels.append((death[alive] == j).astype(np.int8))
    if not ks:
        return np.array([]), np.array([])
    return np.concatenate(ks), np.concatenate(labels)


def all_partitions_f():
    """All 2^8/2=128 partitions F/F^c of {0..7} up to F<->F^c swap, F nonempty
    and != full set (both sides same info under swap, so fix class 0 in F)."""
    classes = list(range(8))
    rest = classes[1:]
    for r in range(0, len(rest) + 1):
        for combo in combinations(rest, r):
            F = frozenset({0, *combo})
            yield F


def main() -> None:
    t0 = time.time()
    ns_screen = list(range(9, 13))
    ns_full = list(range(9, 19))
    cs = (2, 3)

    # cache census + sigma + death per (n, c)
    cache = {}
    for n in ns_full:
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        sig = build_sigma_matrix(syms, 1 << n, levels)
        for c in cs:
            death = death_array(cells, hcs, 1 << n, c, levels)
            cache[(n, c)] = dict(levels=levels, cells=cells, hcs=hcs, sig=sig, death=death, keys=keys)
        print(f"# n={n} sigma+death build done, t={time.time()-t0:.1f}s")
        sys.stdout.flush()

    # ---------- CONTROL 1: regression check against block_halving / flip_pairing ----------
    print("\n## Control 1: regression check (same extended census)")
    from block_halving import chains, least_block
    for n in (9, 12, 16):
        levels = cache[(n, 2)]["levels"]
        keys = cache[(n, 2)]["keys"]
        for c in cs:
            cells = cache[(n, c)]["cells"]
            hcs = cache[(n, c)]["hcs"]
            src, sts = chains(n, c, levels, keys, cells, hcs)
            ks, ws = least_block(src)
            print(f"n={n} c={c}: block_halving k={ks} (worst ratio {ws:.3f})  [expect k<=3]")
    sys.stdout.flush()

    # ---------- step 2: screen all 128 partitions at n=9..12 ----------
    print(f"\n## Screening {sum(1 for _ in all_partitions_f())} partitions at n={ns_screen}")
    partitions = list(all_partitions_f())
    screen_scores = []
    for F in partitions:
        rs = []
        for n in ns_screen:
            for c in cs:
                d = cache[(n, c)]
                prefix = score_and_prefix(d["sig"], F)
                k, lab = pooled_k_label(prefix, d["death"], d["levels"])
                rs.append(pearson(k.astype(np.float64), lab.astype(np.float64)))
        screen_scores.append((float(np.mean(rs)), F, rs))
    screen_scores.sort(key=lambda t: abs(t[0]), reverse=True)
    print(f"swept ALL {len(partitions)} partitions at n=9..12 (both c) for the small-n screen")
    print("top 8 by |mean r| at n=9..12:")
    for meanr, F, rs in screen_scores[:8]:
        print(f"  F={sorted(F)} mean_r={meanr:+.4f}  per-(n,c) r={['%.3f'%v for v in rs]}")

    survivors = screen_scores[:5]
    print(f"\ntaking top {len(survivors)} partitions forward to the full n=9..18 stability check")

    # ---------- step 3/4: full n=9..18 stability, and kill-condition checks ----------
    print("\n## Full n=9..18 stability")
    survivor_info = []
    for meanr, F, _ in survivors:
        per_n = {}
        for n in ns_full:
            rs_c = []
            for c in cs:
                d = cache[(n, c)]
                prefix = score_and_prefix(d["sig"], F)
                k, lab = pooled_k_label(prefix, d["death"], d["levels"])
                rs_c.append(pearson(k.astype(np.float64), lab.astype(np.float64)))
            per_n[n] = rs_c
        survivor_info.append((F, per_n))
        line = " ".join(f"n={n}:[{','.join('%.3f'%v for v in per_n[n])}]" for n in ns_full)
        print(f"F={sorted(F)}: {line}")
    sys.stdout.flush()

    # ---------- kill bullet: absorption structure (variance of k among survivors vs j) ----------
    print("\n## Kill-check: absorption structure (Var(k | alive) vs level j)")
    for F, _ in survivor_info:
        n = 16
        d = cache[(n, 2)]
        prefix = score_and_prefix(d["sig"], F)
        death = d["death"]
        levels = d["levels"]
        vs = []
        for j in range(0, levels, 2):
            alive = death >= j
            if alive.sum() < 5:
                continue
            vs.append((j, float(np.var(prefix[alive, j]))))
        print(f"F={sorted(F)} n=16 c=2: Var(k|alive@j) = " + " ".join(f"j{j}:{v:.2f}" for j, v in vs))

    # ---------- kill bullet: reduces to sigma_{j-1} alone ----------
    print("\n## Kill-check: does correlation reduce to sigma_{j-1}(w) alone?")
    for F, _ in survivor_info:
        n = 16
        for c in cs:
            d = cache[(n, c)]
            sig = d["sig"]
            death = d["death"]
            levels = d["levels"]
            prefix = score_and_prefix(sig, F)
            k_full, lab_full = pooled_k_label(prefix, death, levels)
            # sigma_{j-1} indicator series: for j=0 there's no j-1, skip j=0
            last_in_f = []
            labs2 = []
            for j in range(1, levels):
                alive = death >= j
                if not np.any(alive):
                    continue
                last_in_f.append(np.isin(sig[alive, j - 1], np.array(sorted(F))).astype(np.float64))
                labs2.append((death[alive] == j).astype(np.float64))
            last_in_f = np.concatenate(last_in_f)
            labs2 = np.concatenate(labs2)
            r_full = pearson(k_full.astype(np.float64), lab_full.astype(np.float64))
            r_last = pearson(last_in_f, labs2)
            print(f"F={sorted(F)} n={n} c={c}: r(k,death)={r_full:+.4f}  r(sigma_(j-1) in F, death)={r_last:+.4f}")

    # ---------- CONTROL 3: shuffle control on survivors ----------
    print("\n## Control 3: shuffle control (permute each w's own sigma sequence)")
    rng = np.random.default_rng(20260904)
    for F, per_n in survivor_info:
        for n in (12, 16):
            for c in cs:
                d = cache[(n, c)]
                sig = d["sig"]
                death = d["death"]
                levels = d["levels"]
                prefix_real = score_and_prefix(sig, F)
                k_real, lab_real = pooled_k_label(prefix_real, death, levels)
                r_real = pearson(k_real.astype(np.float64), lab_real.astype(np.float64))
                sig_shuf = sig.copy()
                for w in range(sig_shuf.shape[0]):
                    rng.shuffle(sig_shuf[w])
                prefix_shuf = score_and_prefix(sig_shuf, F)
                k_shuf, lab_shuf = pooled_k_label(prefix_shuf, death, levels)
                r_shuf = pearson(k_shuf.astype(np.float64), lab_shuf.astype(np.float64))
                print(f"F={sorted(F)} n={n} c={c}: r_real={r_real:+.4f}  r_shuffled={r_shuf:+.4f}")

    print(f"\n# total time {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
