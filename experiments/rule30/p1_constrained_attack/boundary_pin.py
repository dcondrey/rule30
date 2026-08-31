"""Boundary-pin tightening of the periodicity ladder (P1 constrained attack).

Finding that motivates this module: the rung-0 escape family satisfies the
pin identity at every INTERIOR modelled column (forced, since those columns
are built by the inverse transduction) but violates it at the rightmost
modelled column R, exactly once per cycle, at the phase slip.  The identity
at column R is not implied by strip validity because the forward rule at
column R needs column R+1, which the strip does not model.  It is however a
fact of the true diagram, so imposing it is sound and strictly tightening.

THE PIN IDENTITY (Rule 30, every column x, every t):
    s(t,x) = 1  =>  s(t,x-1) = NOT s(t+1,x)
Proof: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)); with s(t,x)=1 the OR
saturates to 1 regardless of s(t,x+1), so s(t+1,x) = s(t,x-1) XOR 1.  No
knowledge of column x+1 is used, which is exactly why it constrains the
boundary column.  Rule 90 has no pin (its g is XOR, right-dependent), so
this constraint is Rule-30-specific and passes the Rule 90 filter by
construction.
"""

from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass, replace

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from ladder_base import (  # noqa: E402
    INV, FWD, Params, _sccs, _witness, derive, is_diff_state, simulate,
    step_window, verify_witness,
)


@dataclass(frozen=True)
class BParams(Params):
    boundary_pin: bool = True     # pin identity at column R
    joint_q: tuple = ()           # bounded universal Diff: all q in this set


def bstep(window, cnt, letter, P):
    """step_window plus the boundary pin identity at column R.

    Letters pack (col_{R-1}(t) << 1) | col_R(t), so the identity
        col_R(t)=1 => col_{R-1}(t) = NOT col_R(t+1)
    is a two-consecutive-letter condition, checkable on the letter stream
    with no extra state.
    """
    if P.boundary_pin and window:
        prev = window[-1]
        prev_a, prev_b = prev >> 1, prev & 1
        cur_b = letter & 1
        if prev_b == 1 and prev_a != (1 - cur_b):
            return None
    return step_window(window, cnt, letter, P)


def bsuccessors(state, letter, P, memo):
    """Successors with the boundary pin and a joint (bounded-universal) Diff.

    State: (window, cnt, phase, dstates, flags_round)
    dstates is one countdown slot per q in P.joint_q (or the single P.diff_q).
    Generalized Buchi over |Q| acceptance sets is reduced to a single Buchi
    condition by a round-robin index: the index advances only when the
    currently-awaited q fires, and a state is accepting when the index wraps.
    """
    window, cnt, phase, ds, ridx = state
    key = (window, min(cnt, P.saturate), letter, window[-1] if window else -1)
    hit = memo.get(key)
    if hit is None:
        hit = bstep(window, cnt, letter, P)
        memo[key] = (hit,)
    else:
        hit = hit[0]
    if hit is None:
        return []
    new_window, c_val, m1_val = hit

    qs = P.joint_q if P.joint_q else ((P.diff_q,) if P.diff_q else ())
    if qs and m1_val is not None:
        branches = [((), ridx, False)]
        for i, q in enumerate(qs):
            slot = ds[i] if i < len(ds) else None
            nxt = []
            for acc, r_, _f in branches:
                if slot is None:
                    nxt.append((acc + (None,), r_, False))
                    nxt.append((acc + ((m1_val, q),), r_, False))
                else:
                    b, j = slot
                    if j > 1:
                        nxt.append((acc + ((b, j - 1),), r_, False))
                    elif m1_val != b:
                        fired = (i == r_)
                        nr = (r_ + 1) % len(qs) if fired else r_
                        nxt.append((acc + (None,), nr, fired))
                        nxt.append((acc + ((m1_val, q),), nr, fired))
                    # equal value at distance q: this branch dies
            branches = nxt
            if not branches:
                return []
        dnexts = [(a, r_, f) for a, r_, f in branches]
    else:
        dnexts = [(ds, ridx, False)]

    new_cnt = cnt + 1 if cnt < P.saturate else cnt
    w = P.period_word
    if c_val is None:
        phases = (phase,)
    elif phase is None:
        phases = (None, 1 % len(w)) if c_val == w[0] else (None,)
    elif c_val == w[phase]:
        phases = ((phase + 1) % len(w),)
    else:
        phases = ()
    out = []
    for ph in phases:
        for nd, nr, fl in dnexts:
            acc = fl and (nr == 0 or len(qs) == 1)
            out.append((new_window, new_cnt, ph, nd, nr if qs else 0, acc))
    return out


def bexplore(P, max_states=3_000_000):
    qs = P.joint_q if P.joint_q else ((P.diff_q,) if P.diff_q else ())
    init = ((), 0, None, tuple(None for _ in qs), 0, False)
    ids = {init: 0}
    states = [init]
    adj = [[]]
    memo = {}
    dq = deque([0])
    capped = False
    while dq:
        sid = dq.popleft()
        for letter in range(4):
            for ns in bsuccessors(states[sid][:5], letter, P, memo):
                nid = ids.get(ns)
                if nid is None:
                    if len(states) >= max_states:
                        capped = True
                        continue
                    nid = len(states)
                    ids[ns] = nid
                    states.append(ns)
                    adj.append([])
                    dq.append(nid)
                adj[sid].append((nid, letter))
    return states, adj, capped


def bdecide(P, max_states=3_000_000):
    states, adj, capped = bexplore(P, max_states)
    checking = [i for i, s in enumerate(states) if s[2] is not None]
    cset = set(checking)

    def af(n):
        for m, _ in adj[n]:
            if m in cset:
                yield m

    comps = _sccs(checking, af)
    selfl = {n for n in checking for m, _ in adj[n] if m == n}
    qs = P.joint_q if P.joint_q else ((P.diff_q,) if P.diff_q else ())
    good = None
    for comp in comps:
        if not (len(comp) > 1 or comp[0] in selfl):
            continue
        if not qs:
            good = comp
            break
        if any(states[n][5] for n in comp):
            good = comp
            break
    res = {
        "rule": P.rule, "R": P.right_depth, "w": "".join(map(str, P.period_word)),
        "q": list(qs), "pin": P.boundary_pin,
        "states": len(states), "capped": capped,
    }
    if capped:
        res["verdict"] = "INCONCLUSIVE(cap)"
        return res, None
    if good is None:
        res["verdict"] = "EMPTY"
        return res, None
    res["verdict"] = "NONEMPTY"
    return res, (states, adj, good)


def regression_boundary_pin(rule, R, T=300):
    """The boundary pin identity holds on the true lone-seed diagram."""
    grid, B = simulate(rule, T)
    bad = 0
    ante = 0
    for t in range(T - 1):
        a, b = grid[t][B + R - 1], grid[t][B + R]
        if b == 1:
            ante += 1
            if a != 1 - grid[t + 1][B + R]:
                bad += 1
    return ante, bad
