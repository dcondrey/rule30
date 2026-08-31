"""R7 rung 1: boundary pin, depth dichotomy, and the projected tail language.

Extends ladder.py; does not modify it.

Three things live here.

1. THE BOUNDARY PIN, as a transition filter on letter pairs.  At the outermost
   modelled column R the forward rule has no col_{R+1} to hold against, so the
   strip's internal constraints never entail the OR-saturation pin there.
   Imposing it is sound (it is a fact of the lone-seed diagram) and strictly
   cuts the language.

       col_R(t) = 1  =>  col_{R-1}(t) = NOT col_R(t+1)

   Letters are packed (a << 1) | b with a = col_{R-1}(t), b = col_R(t), so this
   is a constraint on consecutive letters (prev, cur):

       prev & 1  =>  (prev >> 1) != (cur & 1)

2. THE EXTENSION LEMMA (proved in RESULTS-ladder-rung1.md).  The pin at depth R
   is *exactly* the solvability condition for col_{R+1}, so

       plain(R+1)  subset-of  pin(R)  subset-of  plain(R)

   as projections.  The pin buys part of one extra column, not a new kind of
   constraint.  This is why the escape relocates outward instead of dying.

3. THE PROJECTED TAIL LANGUAGE.  Raw product-state counts are dominated by the
   4^(R+k) alphabet factor and prove nothing (rung 0 section 3).  The probative
   object is the accepting tail system projected onto the letter alphabet and
   minimized: stabilization in R is evidence the escape is R-uniform, unbounded
   growth is evidence depth does real work.
"""

from __future__ import annotations

import argparse
import json
from collections import deque

from ladder import (INV, FWD, Params, is_diff_state, simulate, successors,
                    verify_witness, _sccs, _witness)


# ---------------------------------------------------------------- the pin

def pin_ok(prev: int | None, cur: int, rule: int = 30) -> bool:
    """Boundary EXTENDABILITY condition on consecutive letters.

    This is not a rule-30 gadget bolted onto the ladder; it is exactly the
    solvability condition for the unmodelled column R+1 in

        col_R(t+1) = col_{R-1}(t) XOR g(col_R(t), col_{R+1}(t)).

    Rule 30 has g = OR.  When col_R(t) = 1 the OR saturates, col_{R+1}(t)
    cannot influence the outcome, and solvability forces
    col_{R-1}(t) = NOT col_R(t+1).  When col_R(t) = 0 the value of col_{R+1}(t)
    is forced but always exists, so no constraint.

    Rule 90 has g(m, r) = r, so col_{R+1}(t) = col_R(t+1) XOR col_{R-1}(t) is
    always uniquely solvable and the condition is VACUOUS.  That asymmetry is
    the section-0 filter appearing inside the boundary condition itself, and it
    is why the rule-90 control survives: the correct control applies rule 90's
    own extendability condition, not rule 30's.
    """
    if prev is None or rule != 30:
        return True
    if not (prev & 1):          # col_R(t) = 0, OR does not saturate
        return True
    return (prev >> 1) != (cur & 1)


def pin_identity_check(rule: int, T: int = 400):
    """Re-derive the pin on the exact lone-seed diagram.

    Returns (antecedents, violations) over every cell with s(t,x)=1 whose
    partners are inside the simulated grid.  Rule 30 must give 0 violations;
    Rule 90 must violate it at every antecedent (the section-0 filter).
    """
    grid, B = simulate(rule, T)
    ante = 0
    bad = 0
    for t in range(T - 1):
        row = grid[t]
        nxt = grid[t + 1]
        for i in range(1, len(row) - 1):
            if row[i] != 1:
                continue
            ante += 1
            if row[i - 1] != 1 - nxt[i]:
                bad += 1
    return ante, bad


# -------------------------------------------------- explore with the pin

def explore_pin(P: Params, pin: bool, max_states: int = 3_000_000):
    """BFS the product graph, optionally filtering transitions by the pin.

    State gains a last-letter component so the pin is checkable; with pin=False
    that component is dropped so the graph matches ladder.explore exactly.
    """
    init = (((), 0, None, None, False), None)
    ids = {init: 0}
    states = [init]
    adj = [[]]
    memo: dict = {}
    dq = deque([0])
    capped = False
    while dq:
        sid = dq.popleft()
        base, prev = states[sid]
        for letter in range(4):
            if pin and not pin_ok(prev, letter, P.rule):
                continue
            for ns in successors(base, letter, P, memo):
                key = (ns, letter if pin else None)
                nid = ids.get(key)
                if nid is None:
                    if len(states) >= max_states:
                        capped = True
                        continue
                    nid = len(states)
                    ids[key] = nid
                    states.append(key)
                    adj.append([])
                    dq.append(nid)
                adj[sid].append((nid, letter))
    return states, adj, capped


def decide_pin(P: Params, pin: bool, max_states: int = 3_000_000):
    """Emptiness with the optional boundary pin.  Mirrors ladder.decide."""
    states, adj, capped = explore_pin(P, pin, max_states)
    checking = [i for i, s in enumerate(states) if s[0][2] is not None]
    cset = set(checking)

    def adj_checking(n):
        for m, _ in adj[n]:
            if m in cset:
                yield m

    comps = _sccs(checking, adj_checking)
    self_loop = {n for n in checking for m, _ in adj[n] if m == n}
    good = None
    for comp in comps:
        nontrivial = len(comp) > 1 or (comp[0] in self_loop)
        if not nontrivial:
            continue
        if P.diff_q is None or any(is_diff_state(states[n][0], P) for n in comp):
            good = comp
            break
    res = {
        "R": P.right_depth, "k": P.left_depth,
        "w": "".join(map(str, P.period_word)), "q": P.diff_q,
        "rule": P.rule, "pin": pin,
        "states": len(states), "capped": capped,
    }
    if capped:
        res["verdict"] = "INCONCLUSIVE (state cap hit)"
        return res
    if good is None:
        res["verdict"] = "EMPTY"
        return res
    res["verdict"] = "NONEMPTY"
    base_states = [s[0] for s in states]
    res["witness"] = _witness(base_states, adj, good, P)
    return res


# ------------------------------------------- projected tail language

def tail_language(P: Params, pin: bool, max_states: int = 3_000_000):
    """Minimized DFA for the letter language of the accepting tail system.

    The accepting tail system is the union of the nontrivial SCCs that carry a
    Buchi-accepting run (a diff state when diff_q is set).  Its letter language
    is projected, determinized by subset construction, and minimized by
    Hopcroft-style partition refinement.  Size is reported as the number of
    reachable minimized states; that is the R-comparable quantity, unlike the
    raw product count.
    """
    states, adj, capped = explore_pin(P, pin, max_states)
    if capped:
        return {"capped": True}
    checking = [i for i, s in enumerate(states) if s[0][2] is not None]
    cset = set(checking)

    def adj_checking(n):
        for m, _ in adj[n]:
            if m in cset:
                yield m

    comps = _sccs(checking, adj_checking)
    self_loop = {n for n in checking for m, _ in adj[n] if m == n}
    good_nodes = set()
    for comp in comps:
        if len(comp) <= 1 and comp[0] not in self_loop:
            continue
        if P.diff_q is None or any(is_diff_state(states[n][0], P) for n in comp):
            good_nodes.update(comp)
    if not good_nodes:
        return {"empty": True, "min_states": 0}

    # NFA over good_nodes; every state both initial and accepting (omega tail).
    trans: dict[int, dict[int, set]] = {}
    for n in good_nodes:
        d: dict[int, set] = {}
        for m, letter in adj[n]:
            if m in good_nodes:
                d.setdefault(letter, set()).add(m)
        trans[n] = d

    # Bisimulation quotient by partition refinement.  Determinizing the tail
    # NFA is exponential and blew up even at R = 1, so the R-comparable
    # invariant reported here is the number of bisimulation classes of the
    # accepting tail system: polynomial, canonical, and still sensitive to
    # whether added depth creates genuinely new tail behaviour.
    nodes = sorted(good_nodes)
    diff_lab = {n: bool(is_diff_state(states[n][0], P)) for n in nodes}
    part = {n: (1 if diff_lab[n] else 0) for n in nodes}
    ncls = len(set(part.values()))
    while True:
        sig = {}
        for n in nodes:
            key = (part[n], tuple(sorted(
                {(a, part[m]) for a, ms in trans[n].items() for m in ms})))
            sig.setdefault(key, []).append(n)
        # Convergence is refinement reaching a fixpoint, i.e. the block COUNT
        # stops growing.  Comparing label maps does not work: blocks are
        # renumbered every round, so equal partitions can compare unequal and
        # the loop never terminates.
        if len(sig) == ncls:
            break
        ncls = len(sig)
        newpart = {}
        for idx, key in enumerate(sorted(sig, key=str)):
            for n in sig[key]:
                newpart[n] = idx
        part = newpart
    classes = ncls
    return {"empty": False, "tail_nodes": len(nodes),
            "bisim_classes": classes, "raw_states": len(states)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True,
                    choices=("identity", "calibrate", "sweep", "language"))
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("--rmax", type=int, default=6)
    ap.add_argument("-k", type=int, default=2)
    ap.add_argument("-w", default="01")
    ap.add_argument("-q", type=int, default=1)
    ap.add_argument("--max-states", type=int, default=3_000_000)
    a = ap.parse_args()
    w = tuple(int(c) for c in a.w)

    if a.mode == "identity":
        for rule in (30, 90):
            ante, bad = pin_identity_check(rule)
            print(json.dumps({"rule": rule, "antecedents": ante,
                              "violations": bad}))
        return

    if a.mode == "calibrate":
        out = []
        for word in ((1,), (0,)):
            for R in (1, 2):
                P = Params(rule=30, right_depth=R, left_depth=a.k,
                           period_word=word, diff_q=1)
                out.append(decide_pin(P, True, a.max_states))
        for R in range(1, 6):
            P = Params(rule=90, right_depth=R, left_depth=a.k,
                       period_word=(0,), diff_q=1)
            out.append(decide_pin(P, True, a.max_states))
        for r in out:
            r.pop("witness", None)
            print(json.dumps(r))
        return

    if a.mode == "sweep":
        for R in range(1, a.rmax + 1):
            for pin in (False, True):
                P = Params(rule=a.rule, right_depth=R, left_depth=a.k,
                           period_word=w, diff_q=a.q)
                r = decide_pin(P, pin, a.max_states)
                wit = r.pop("witness", None)
                if wit is not None:
                    okv, note = verify_witness(wit["prefix"], wit["cycle"], P)
                    r["witness_verified"] = okv
                    r["witness_note"] = note
                    r["cycle_len"] = len(wit["cycle"])
                print(json.dumps(r), flush=True)
        return

    for R in range(1, a.rmax + 1):
        for pin in (False, True):
            P = Params(rule=a.rule, right_depth=R, left_depth=a.k,
                       period_word=w, diff_q=a.q)
            r = tail_language(P, pin, a.max_states)
            r.update({"R": R, "pin": pin, "k": a.k, "q": a.q,
                      "w": a.w, "rule": a.rule})
            print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
