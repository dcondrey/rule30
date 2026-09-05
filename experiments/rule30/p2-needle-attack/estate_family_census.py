#!/usr/bin/env python3
"""Extremal forcing-STATE census for the p=2 needle (preregistered).

For each (n, c, arm) with r=0 this enumerates every source word, deduplicates
by the LIVE forcing state (edge[:-1], the dependency edge minus its unread cut
cell), forces n+4 continuation rows, and records the states that attain
max_survival(n,c).  It writes estate_census.json.  Family/null analysis is in
estate_family_analysis.py.

Reads (does not modify) ../p1-period2-invariant modules.  See estate_PREREG.md.
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

P1 = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant"
sys.path.insert(0, P1)

from constant_tail_scale import append_dependency_edge  # noqa: E402
from dyadic_periodicity_analyzer import BOUNDARY as _BND, cone_local  # noqa: E402
from late_pull_diagonal_sat import literal_extension  # noqa: E402

# --- inlined primitives (4x4 table) -----------------------------------------
BOUNDARY = tuple(_BND)                       # (3,2,1,0), an involution
PHI = tuple(tuple(cone_local(l, r) for r in range(4)) for l in range(4))


def append_edge(edge, prev, v):
    """Inlined append_dependency_edge; prev may be None iff edge is empty."""
    b0 = BOUNDARY[v]
    if not edge:
        return (b0,)
    out = [b0, PHI[prev][b0]]
    last = out[1]
    for order in range(2, len(edge) + 1):
        last = PHI[edge[order - 2]][last]
        out.append(last)
    return tuple(out)


def selftest_append(trials=4000, seed=0):
    rng = random.Random(seed)
    for _ in range(trials):
        L = rng.randint(0, 12)
        word = [rng.randint(0, 3) for _ in range(L)]
        edge_ref = ()
        edge_mine = ()
        prev = None
        for v in word:
            edge_ref = append_dependency_edge(edge_ref, prev, v)
            edge_mine = append_edge(edge_mine, prev, v)
            assert edge_ref == edge_mine, (word, edge_ref, edge_mine)
            prev = v
    return trials


# --- forcing ----------------------------------------------------------------
def padding_edge(n):
    edge = ()
    prev = None
    for _ in range(n):
        edge = append_edge(edge, prev, 0)
        prev = 0
    return edge  # length n, prev==0


def force(edge, tail, rows):
    """Force `rows` continuation symbols from live state `edge`.

    Returns (continuation, edges_before_row) where edges_before_row[t] is the
    full edge just before appending row t (used for the alpha identity).
    prev = BOUNDARY[edge[0]] is the last consumed endpoint symbol.
    """
    prev = BOUNDARY[edge[0]]
    cont = []
    edges_before = []
    e = edge
    for _ in range(rows):
        edges_before.append(e)
        hit = None
        for v in range(4):
            nf = append_edge(e, prev, v)
            if nf[-1] == tail:
                assert hit is None
                hit = (v, nf)
        assert hit is not None
        v, e = hit
        cont.append(v)
        prev = v
    return cont, edges_before


def hc_run(prev, cont):
    p = prev
    for i, v in enumerate(cont):
        if v not in (1, 2) or (p == 1 and v == 1):
            return i
        p = v
    return len(cont)


def killer_label(prev, cont, survival):
    if survival >= len(cont):
        return "none-in-window"
    p = prev if survival == 0 else cont[survival - 1]
    v = cont[survival]
    if v == 0:
        return "E-miss:0"
    if v == 3:
        return "E-miss:3"
    if p == 1 and v == 1:
        return "1-after-1"
    return f"other:{p}->{v}"


def alpha_profile(edge, cont, edges_before, rows_checked):
    """Per-row alpha via eq(3) and eq(4); assert they agree and predict the
    forced high bit.  Also return the alpha SUPPORT (nonzero cells of E[:-1])
    at each row, both prefix (from index 0) and suffix (depth from |E|-1)."""
    prev0 = BOUNDARY[edge[0]]
    profile = []
    for t in range(rows_checked):
        E = edges_before[t]
        p = prev0 if t == 0 else cont[t - 1]
        pbit = 1 if p != 0 else 0
        supp = [i for i in range(len(E) - 1) if E[i] != 0]
        par = len(supp) & 1
        a3 = 1 ^ pbit ^ par
        R = E[::-1]
        supp4 = [i for i in range(1, len(R)) if R[i] != 0]
        a4 = 1 ^ pbit ^ (len(supp4) & 1)
        assert a3 == a4, (t, a3, a4)
        forced = cont[t]
        assert (forced >> 1) == (1 ^ a3), (t, forced, a3)
        depth = len(E) - 1
        supp_suffix = sorted(depth - i for i in supp)  # offset from cut end
        profile.append(
            {"row": t, "alpha": a3, "forced": forced,
             "support_prefix": supp, "support_suffix": supp_suffix}
        )
    return profile


# --- census -----------------------------------------------------------------
def enumerate_leaves(n, arm):
    """BFS over source symbols, dedup frontier by live state edge[:-1].

    Returns dict key=edge[:-1] -> {"edge": full_edge, "word": rep_word,
    "count": fiber, "last": set(edge[-1])} at leaf depth n, plus the max
    frontier size seen.
    """
    base = padding_edge(n)
    frontier = {base[:-1]: {"edge": base, "word": (), "count": 1}}
    max_front = 1
    for depth in range(1, n + 1):
        nxt = {}
        leaf = depth == n
        for val in frontier.values():
            edge = val["edge"]
            word = val["word"]
            count = val["count"]
            prev = BOUNDARY[edge[0]]
            wl = word[-1] if word else None
            for v in (1, 2):
                if arm == "hardcore" and wl == 1 and v == 1:
                    continue
                ne = append_edge(edge, prev, v)
                key = ne[:-1]
                cur = nxt.get(key)
                if cur is None:
                    entry = {"edge": ne, "word": word + (v,), "count": count}
                    if leaf:
                        entry["last"] = {ne[-1]}
                    nxt[key] = entry
                else:
                    cur["count"] += count
                    if leaf:
                        cur["last"].add(ne[-1])
        frontier = nxt
        max_front = max(max_front, len(frontier))
    return frontier, max_front


def census_cell(n, c, arm, rows=None, sample_typical=1500, seed=0):
    if rows is None:
        rows = n + 4
    t0 = time.perf_counter()
    leaves, max_front = enumerate_leaves(n, arm)
    total_words = sum(v["count"] for v in leaves.values())
    # survival per live state
    records = []
    max_surv = -1
    for key, val in leaves.items():
        edge = val["edge"]
        prev = BOUNDARY[edge[0]]
        cont, edges_before = force(edge, c, rows)
        surv = hc_run(prev, cont)
        assert surv < n + 2, ("gamma<1!", n, c, arm, val["word"], surv)
        if surv > max_surv:
            max_surv = surv
        records.append((key, val, cont, edges_before, surv))
    gamma = (n + 2) - max_surv
    # extremal
    extremal = []
    typical_states = []
    for key, val, cont, edges_before, surv in records:
        if surv == max_surv:
            rows_checked = min(len(cont), surv + 1)
            prof = alpha_profile(val["edge"], cont, edges_before, rows_checked)
            prev = BOUNDARY[val["edge"][0]]
            extremal.append({
                "live_state": list(key),
                "full_edge": list(val["edge"]),
                "last_cells": sorted(val["last"]),
                "fiber": val["count"],
                "rep_word": list(val["word"]),
                "continuation": cont[:surv + 2],
                "survival": surv,
                "killer": killer_label(prev, cont, surv),
                "alpha_profile": prof,
            })
        else:
            typical_states.append(list(key))
    # sample typical for the null
    rng = random.Random(seed)
    if len(typical_states) > sample_typical:
        typical_states = rng.sample(typical_states, sample_typical)
    # continuation-class grouping (for the archaeology §2.2 cross-check)
    by_cont = {}
    for e in extremal:
        by_cont.setdefault(tuple(e["continuation"][:e["survival"]]), []).append(e)
    pooled_fiber = sum(e["fiber"] for e in extremal)
    cell = {
        "n": n, "c": c, "arm": arm, "rows": rows,
        "max_survival": max_surv, "gamma": gamma,
        "total_words": total_words,
        "distinct_live_states": len(leaves),
        "max_frontier": max_front,
        "num_extremal_states": len(extremal),
        "num_continuation_classes": len(by_cont),
        "pooled_fiber": pooled_fiber,
        "class_sizes": sorted(
            (sum(e["fiber"] for e in v) for v in by_cont.values()), reverse=True
        ),
        "states_per_class": sorted((len(v) for v in by_cont.values()), reverse=True),
        "extremal": extremal,
        "typical_sample": typical_states,
        "seconds": time.perf_counter() - t0,
    }
    return cell


def crosscheck_literal(cell):
    """Control 2: verify extremal survival/continuation against
    late_pull_diagonal_sat.literal_extension called directly on rep words."""
    n, c = cell["n"], cell["c"]
    rows = cell["rows"]
    for e in cell["extremal"]:
        W = tuple(e["rep_word"])
        ext = literal_extension(W, c, rows)
        surv = hc_run(W[-1], list(ext))
        assert surv == e["survival"], (n, c, W, surv, e["survival"])
        assert list(ext[:surv]) == e["continuation"][:surv], (n, c, W)
        # also verify our carried edge equals the literal edge after padded W
        edge = ()
        prev = None
        for v in (0,) * n + W:
            edge = append_dependency_edge(edge, prev, v)
            prev = v
        assert list(edge) == e["full_edge"], (n, c, W)
    return len(cell["extremal"])


def run(ns, cs=(2, 3), arms=("all", "hardcore"), out="estate_census.json"):
    print("selftest append:", selftest_append(), "trials PASS", flush=True)
    outpath = Path(__file__).with_name(out)
    cells = {}
    if outpath.exists():
        cells = json.loads(outpath.read_text())
    for n in ns:
        for arm in arms:
            for c in cs:
                ckey = f"n{n}_c{c}_{arm}"
                if ckey in cells:
                    print("skip", ckey, "(checkpointed)", flush=True)
                    continue
                cell = census_cell(n, c, arm)
                nx = crosscheck_literal(cell)
                print(
                    f"{ckey}: max_surv={cell['max_survival']} "
                    f"gamma={cell['gamma']} words={cell['total_words']} "
                    f"live_states={cell['distinct_live_states']} "
                    f"maxfront={cell['max_frontier']} "
                    f"extremal_states={cell['num_extremal_states']} "
                    f"cont_classes={cell['num_continuation_classes']} "
                    f"class_sizes={cell['class_sizes']} "
                    f"pooled_fiber={cell['pooled_fiber']} "
                    f"xcheck={nx} t={cell['seconds']:.1f}s",
                    flush=True,
                )
                cells[ckey] = cell
                outpath.write_text(json.dumps(cells))
    return cells


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if args and args[0] == "gate":
        # n=14 both tails, all-W, reproduce archaeology 2.1
        run([14], cs=(2, 3), arms=("all",), out="estate_census_gate.json")
    else:
        ns = [int(a) for a in args] if args else list(range(10, 21))
        run(ns)
