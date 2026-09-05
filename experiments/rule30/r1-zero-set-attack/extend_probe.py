"""Per-witness extension probe for the R7 ladder (route R1 reconciliation).

The ladder (`experiments/rule30/ladder/ladder.py`) decides a LANGUAGE: at right
depth R and left depth k it is nonempty for p = 2 at every (R,k) ever decided
(RESULTS-ladder-rung0.md section 3, RESULTS-ladder-rung1.md section 3).  That is
a statement about the language, not about any individual witness.

This file asks the per-witness question, which neither rung ran:

    take an actual accepting lasso of the p = 2 mode-(ii) ladder and try to
    extend it to a genuine lone-seed diagram.  How far does it get?

Two directions, both decidable on an ultimately periodic word:

  LEFT.  The inverse transduction col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR
  col_{x+1}(t)) is deterministic, so leftward extension is forced.  The wedge
  at depth j (col_{-j}(t) = 0 for t < j, col_{-j}(j) = 1) constrains only
  t <= j, i.e. finitely many cells per depth, all inside a long enough
  unrolling of the lasso.  So "does this witness extend to left depth D" is a
  finite check.  The ladder only ever imposes it out to depth k.

  RIGHT.  By rung 1 Lemma 1 a column col_{R+1} obeying the forward rule at
  x = R exists iff the pin col_R(t) = 1 => col_{R-1}(t) = NOT col_R(t+1) holds,
  and then col_{R+1}(t) is forced where col_R(t) = 0 and FREE where
  col_R(t) = 1.  So rightward extension is a nondeterministic search, and the
  lone-seed wedge (col_x(t) = 0 for t < x, col_x(x) = 1) is a constraint the
  ladder drops entirely for x > R -- obstruction F.

Soundness control for the probe itself: the TRUE lone-seed letter word must
survive both directions to any depth, for rule 30 AND rule 90.  If it does not,
the probe is broken and nothing it says about witnesses means anything.

Rule 90 filter (PATH.md row 55): every rule-30 measurement here is repeated on
rule 90 with rule 90's OWN extendability condition, which by rung 1 Lemma 1' is
vacuous.  Rule 30's pin is never applied to rule 90.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from collections import deque

_LADDER = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/ladder/ladder.py"


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


L = _load(_LADDER, "r1za_ladder")
Params = L.Params
INV = L.INV
FWD = L.FWD


# --------------------------------------------------------------------------
# column derivation, unbounded depth
# --------------------------------------------------------------------------


def derive_deep(word, R: int, depth: int, rule: int) -> dict[int, list[int]]:
    """cols[x] for x = R down to R - depth.  cols[x][t] is col_x(t), t from 0.

    Same recursion as ladder.derive, no x_min floor and no window slicing.
    Each step left shortens the array by one, so cols[R - j] has length
    len(word) - j.
    """
    inv = INV[rule]
    cols = {R: [ab & 1 for ab in word], R - 1: [ab >> 1 for ab in word]}
    x = R - 2
    while x >= R - depth:
        up = cols[x + 1]
        if len(up) < 2:
            break
        upr = cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    return cols


def wedge_violation(cols: dict[int, list[int]], x: int):
    """First lone-seed wedge/edge violation in column x, or None.

    Lone-seed facts: col_x(t) = 0 for t < |x| and col_x(|x|) = 1.  Returns
    (t, got, want) or None.  Cells past the end of the array are not checked.
    """
    vals = cols.get(x)
    if not vals:
        return None
    ax = abs(x)
    for t in range(min(ax + 1, len(vals))):
        want = 1 if t == ax else 0
        if vals[t] != want:
            return (t, vals[t], want)
    return None


def left_reach(word, R: int, rule: int, max_depth: int):
    """Deepest D such that columns R-1 .. -D all satisfy the wedge.

    Returns (D, detail).  D = max_depth means "survived the whole probe".
    detail records the first failure.  Only depths whose wedge window
    t = 0..|x| is fully present in the derived array are judged; a column too
    short to judge stops the probe with reason 'word too short'.
    """
    depth = R + max_depth
    cols = derive_deep(word, R, depth, rule)
    for d in range(0, max_depth + 1):
        x = -d
        vals = cols.get(x)
        if vals is None or len(vals) < abs(x) + 1:
            return d - 1, {"stopped": "word too short", "at_depth": d}
        bad = wedge_violation(cols, x)
        if bad is not None:
            t, got, want = bad
            return d - 1, {"stopped": "wedge", "at_depth": d, "t": t,
                           "got": got, "want": want}
    return max_depth, {"stopped": None}


# --------------------------------------------------------------------------
# rightward extension (rung 1 Lemma 1 / Lemma 1')
# --------------------------------------------------------------------------


def right_step_options(cx_prev, cx, rule: int):
    """Possible col_{x+1} given col_{x-1} = cx_prev and col_x = cx.

    Forward rule at x: cx(t+1) = cx_prev(t) XOR (cx(t) OR cx_next(t)) for rule
    30, and cx(t+1) = cx_prev(t) XOR cx_next(t) for rule 90.  Length is
    len(cx) - 1 (needs cx(t+1)).  Returns (forced, free) where forced[t] is the
    determined value or None, and free[t] is True where the choice is free.
    Returns None if no extension exists (the pin fails somewhere).
    """
    n = min(len(cx) - 1, len(cx_prev))
    forced = [None] * n
    free = [False] * n
    for t in range(n):
        a = cx[t + 1] ^ cx_prev[t]          # = cx(t) OR cx_next(t)  [rule 30]
        if rule == 90:
            forced[t] = a                    # always uniquely solvable
            continue
        if cx[t] == 0:
            forced[t] = a
        else:
            if a != 1:
                return None                  # pin violated: no extension
            free[t] = True                   # cx_next(t) unconstrained
    return forced, free


def right_reach(cols: dict[int, list[int]], R: int, rule: int, max_depth: int,
                rng: random.Random, tries: int = 400):
    """Deepest right column reachable while obeying the lone-seed wedge.

    Greedy/randomised search: at each new column, cells are forced where the
    current column is 0, free where it is 1; the wedge fixes the free cells at
    t <= x.  Explores `tries` random completions of the remaining free cells.
    Returns (deepest_x, detail).
    """
    best = R
    detail = {"stopped": "pin", "at_x": R + 1}
    base_prev = cols[R - 1]
    base_cur = cols[R]

    for _ in range(tries):
        prev, cur = base_prev, base_cur
        x = R
        while x - R < max_depth:
            opt = right_step_options(prev, cur, rule)
            if opt is None:
                if x > best:
                    best, detail = x, {"stopped": "pin", "at_x": x + 1}
                break
            forced, free = opt
            nxt = []
            ok = True
            for t in range(len(forced)):
                if forced[t] is not None:
                    v = forced[t]
                else:
                    v = rng.randint(0, 1)
                nxt.append(v)
            # lone-seed wedge on the new column x+1
            nx = x + 1
            for t in range(min(nx + 1, len(nxt))):
                want = 1 if t == nx else 0
                if forced[t] is not None:
                    if nxt[t] != want:
                        ok = False
                        break
                else:
                    nxt[t] = want
            if not ok:
                if x > best:
                    best, detail = x, {"stopped": "wedge", "at_x": x + 1}
                break
            if len(nxt) < nx + 1:
                if x > best:
                    best, detail = x, {"stopped": "word too short", "at_x": nx}
                break
            prev, cur = cur, nxt
            x = nx
            if x > best:
                best, detail = x, {"stopped": None, "at_x": x}
        if best - R >= max_depth:
            break
    return best, detail


# --------------------------------------------------------------------------
# witness sampling
# --------------------------------------------------------------------------


def good_component(P: Params, max_states: int = 3_000_000):
    """Return (states, adj, comp) for an accepting SCC, mirroring ladder.decide."""
    states, adj, capped = L.explore(P, max_states)
    assert not capped, "state cap hit; lower R/k"
    checking = [i for i, s in enumerate(states) if s[2] is not None]
    cset_all = set(checking)

    def adj_checking(n):
        for m, _ in adj[n]:
            if m in cset_all:
                yield m

    comps = L._sccs(checking, adj_checking)
    self_loop = {n for n in checking for m, _ in adj[n] if m == n}
    out = []
    for comp in comps:
        nontrivial = len(comp) > 1 or (comp[0] in self_loop)
        if not nontrivial:
            continue
        if P.diff_q is not None and not any(L.is_diff_state(states[n], P)
                                            for n in comp):
            continue
        out.append(comp)
    return states, adj, out


def _rand_path(adj, src, targets, rng, cset=None):
    """Randomised BFS path src -> any node in `targets`.  Returns (node, letters)."""
    prev = {src: None}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        edges = list(adj[u])
        rng.shuffle(edges)
        for m, letter in edges:
            if cset is not None and m not in cset:
                continue
            if m in targets:
                seq = []
                x = u
                while prev[x] is not None:
                    px, lt = prev[x]
                    seq.append(lt)
                    x = px
                seq.reverse()
                seq.append(letter)
                return m, seq
            if m not in prev:
                prev[m] = (u, letter)
                dq.append(m)
    return None, None


def sample_lassos(P: Params, n: int, rng: random.Random, max_states=3_000_000):
    """n distinct accepting lassos (prefix, cycle), each verified."""
    states, adj, comps = good_component(P, max_states)
    assert comps, "no accepting SCC -- language is EMPTY"
    out = []
    seen = set()
    for _ in range(n * 40):
        if len(out) >= n:
            break
        comp = rng.choice(comps)
        cset = set(comp)
        entry, prefix = _rand_path(adj, 0, cset, rng)
        if entry is None:
            continue
        if P.diff_q is None or L.is_diff_state(states[entry], P):
            _, cyc = _rand_path(adj, entry, {entry}, rng, cset)
        else:
            diffs = {n_ for n_ in comp if L.is_diff_state(states[n_], P)}
            mid, seg1 = _rand_path(adj, entry, diffs, rng, cset)
            if mid is None:
                continue
            _, seg2 = _rand_path(adj, mid, {entry}, rng, cset)
            if seg2 is None:
                continue
            cyc = seg1 + seg2
        if cyc is None:
            continue
        key = (tuple(prefix), tuple(cyc))
        if key in seen:
            continue
        ok, note = L.verify_witness(prefix, cyc, P)
        if not ok:
            raise AssertionError(f"sampled lasso failed verify_witness: {note}")
        seen.add(key)
        out.append({"prefix": prefix, "cycle": cyc, "note": note})
    return out


def lasso_word(prefix, cycle, length: int):
    word = list(prefix)
    while len(word) < length:
        word.extend(cycle)
    return word[:length]


def true_word(rule: int, R: int, T: int):
    grid, B = L.simulate(rule, T + 4)
    return [(grid[t][B + R - 1] << 1) | grid[t][B + R] for t in range(T)]


# --------------------------------------------------------------------------
# drivers
# --------------------------------------------------------------------------


def run_control(rule: int, R: int, max_depth: int, rng: random.Random):
    """The probe applied to the TRUE lone-seed word.  Must survive."""
    T = R + 2 * max_depth + 40
    word = true_word(rule, R, T)
    d, det = left_reach(word, R, rule, max_depth)
    cols = derive_deep(word, R, R + 2, rule)
    rd, rdet = right_reach(cols, R, rule, max_depth, rng, tries=200)
    return {"rule": rule, "R": R, "left_depth_reached": d, "left_detail": det,
            "right_depth_reached": rd - R, "right_detail": rdet,
            "max_depth": max_depth}


def run_witnesses(P: Params, n: int, max_depth: int, rng: random.Random):
    T = P.right_depth + 2 * max_depth + 60
    lassos = sample_lassos(P, n, rng)
    rows = []
    for i, w in enumerate(lassos):
        word = lasso_word(w["prefix"], w["cycle"], T)
        d, det = left_reach(word, P.right_depth, P.rule, max_depth)
        cols = derive_deep(word, P.right_depth, P.right_depth + 2, P.rule)
        rd, rdet = right_reach(cols, P.right_depth, P.rule, max_depth, rng)
        rows.append({
            "i": i,
            "prefix_len": len(w["prefix"]),
            "cycle_len": len(w["cycle"]),
            "left_depth_reached": d,
            "left_detail": det,
            "right_depth_reached": rd - P.right_depth,
            "right_detail": rdet,
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30, choices=(30, 90))
    ap.add_argument("-R", "--right-depth", type=int, default=2)
    ap.add_argument("-k", "--left-depth", type=int, default=2)
    ap.add_argument("-w", "--word", default="01")
    ap.add_argument("-q", "--diff-q", type=int, default=1)
    ap.add_argument("-n", "--samples", type=int, default=40)
    ap.add_argument("-D", "--max-depth", type=int, default=24)
    ap.add_argument("--seed", type=int, default=20260905)
    ap.add_argument("--mode", default="all",
                    choices=("all", "control", "witness"))
    args = ap.parse_args()
    rng = random.Random(args.seed)

    out = {"args": vars(args)}
    if args.mode in ("all", "control"):
        out["controls"] = [run_control(r, args.right_depth, args.max_depth, rng)
                           for r in (30, 90)]
    if args.mode in ("all", "witness"):
        P = Params(rule=args.rule, right_depth=args.right_depth,
                   left_depth=args.left_depth,
                   period_word=tuple(int(c) for c in args.word),
                   diff_q=args.diff_q)
        out["witnesses"] = run_witnesses(P, args.samples, args.max_depth, rng)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
