"""Tightened ladder variants (route R7, second cycle).

Three constraint changes proposed against the rung-0 negative result:

  A. right-wedge on modelled columns  -- ALREADY IMPOSED by ladder.step_window
     (`ax = abs(x)` covers positive x).  `wedge_right=False` disables it, so
     the run below is a confirmation that the constraint is live, not a new
     constraint.
  B. pin-cascade safety, s(t,x+1)=1 and s(t,x)=0 => s(t+1,x+1)=1 -- entailed
     by INV[30] on every modelled column.  `pin_audit=True` checks it
     explicitly and counts violations; a zero count with unchanged state
     counts is the proof that it adds nothing.
  C. Diff quantified over ALL q <= Q simultaneously.  This is NOT a choice of
     q: L(q=1..Q) is a subset of L(q=1) for each q, so EMPTY is strictly
     easier, while EMPTY still yields "col_{-1} is eventually q-periodic for
     SOME q <= Q", which discharges Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5 the
     same way a fixed-q emptiness does.  Encoded with an exact Q-bit history
     of col_{-1} (cost 2^Q * Q) instead of the repo's guess gadget (cost
     prod_q 2(2q+1)); at Q=4 that is 64 versus 15,120.

Generalized-Buchi degeneralization: acc index cycles 0..Q-1, advancing when
the diff flag for q = acc+1 fires; the wrap transition sets the accept flag.
The index advances ONLY post-onset (phase is not None), so no run can earn
acceptance on diffs observed before the periodicity hypothesis is in force.
"""

from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass

sys.path.insert(0, "../ladder")

from ladder import FWD, INV, Params, _sccs, derive, simulate  # noqa: E402


@dataclass(frozen=True)
class CParams:
    rule: int
    right_depth: int
    left_depth: int
    period_word: tuple[int, ...]
    max_q: int                      # Q >= 1; conjunction over q = 1..Q
    wedge_right: bool = True        # False = drop the wedge for x > 0
    pin_audit: bool = False         # cascade corollary, all modelled pairs
    pin_full: bool = False          # general 1-pin, strictly stronger

    @property
    def x_min(self) -> int:
        return -max(self.left_depth, 1)

    @property
    def window_len(self) -> int:
        return self.right_depth - self.x_min

    @property
    def saturate(self) -> int:
        return self.right_depth + 2 * abs(self.x_min) + 1

    def base(self) -> Params:
        return Params(self.rule, self.right_depth, self.left_depth,
                      self.period_word, None)


def step_window(window, cnt, letter, P: CParams, pin_hits):
    """ladder.step_window with the right-wedge toggle and the pin audit."""
    new_window = window + (letter,)
    if len(new_window) > P.window_len:
        new_window = new_window[-P.window_len:]
    rows = derive(new_window, P.base())
    R = P.right_depth
    sat = cnt >= P.saturate
    c_val = None
    m1_val = None
    for x, vals in rows.items():
        if not vals:
            continue
        v = vals[-1]
        if not sat and (P.wedge_right or x <= 0):
            t = cnt - max(0, R - 1 - x)
            if t >= 0:
                ax = abs(x)
                if t < ax and v != 0:
                    return None
                if t == ax and v != 1:
                    return None
        if x == 0:
            c_val = v
        elif x == -1:
            m1_val = v
    if P.pin_audit or P.pin_full:
        # rows[x] is delayed by max(0, R-1-x); align on absolute time.
        def at(x, t):
            vals = rows.get(x)
            if vals is None:
                return None
            i = len(vals) - 1 - (cnt - max(0, R - 1 - x) - t)
            return vals[i] if 0 <= i < len(vals) else None
        lo = max(0, cnt - P.window_len)
        for x in range(P.x_min, R):
            for t in range(lo, cnt):
                if P.pin_audit:
                    # s(t,x+1)=1 and s(t,x)=0 => s(t+1,x+1)=1
                    a, b, c = at(x, t), at(x + 1, t), at(x + 1, t + 1)
                    if None not in (a, b, c) and b == 1 and a == 0 and c != 1:
                        pin_hits[0] += 1
                        return None
                if P.pin_full:
                    # s(t,x+1)=1 => s(t,x) = NOT s(t+1,x+1)   (general 1-pin)
                    a, b, c = at(x, t), at(x + 1, t), at(x + 1, t + 1)
                    if None not in (a, b, c) and b == 1 and a != 1 ^ c:
                        pin_hits[0] += 1
                        return None
    return new_window, c_val, m1_val


def successors(state, letter, P: CParams, memo, pin_hits):
    window, cnt, phase, hist, acc, _flag = state
    key = (window, min(cnt, P.saturate), letter)
    hit = memo.get(key)
    if hit is None:
        hit = step_window(window, cnt, letter, P, pin_hits)
        memo[key] = (hit,)
    else:
        hit = hit[0]
    if hit is None:
        return []
    new_window, c_val, m1_val = hit

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
    if not phases:
        return []

    if m1_val is None:
        new_hist = hist
    else:
        new_hist = (hist + (m1_val,))[-P.max_q:]

    out = []
    for ph in phases:
        acc2, flag = acc, False
        # advance only post-onset, and only on the flag for q = acc+1
        if ph is not None and m1_val is not None:
            q = acc2 + 1
            if len(hist) >= q and hist[-q] != m1_val:
                acc2 = (acc2 + 1) % P.max_q
                flag = acc2 == 0
        out.append((new_window, new_cnt, ph, new_hist, acc2, flag))
    return out


def explore(P: CParams, max_states=3_000_000):
    init = ((), 0, None, (), 0, False)
    ids = {init: 0}
    states = [init]
    adj = [[]]
    memo: dict = {}
    pin_hits = [0]
    dq = deque([0])
    capped = False
    while dq:
        sid = dq.popleft()
        st = states[sid]
        for letter in range(4):
            for ns in successors(st, letter, P, memo, pin_hits):
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
    return states, adj, capped, pin_hits[0]


def decide(P: CParams, max_states=3_000_000):
    states, adj, capped, pin_hits = explore(P, max_states)
    checking = [i for i, s in enumerate(states) if s[2] is not None]
    cset = set(checking)

    def adj_c(n):
        for m, _ in adj[n]:
            if m in cset:
                yield m

    self_loop = {n for n in checking for m, _ in adj[n] if m == n}
    good = None
    for comp in _sccs(checking, adj_c):
        if not (len(comp) > 1 or comp[0] in self_loop):
            continue
        if any(states[n][5] for n in comp):
            good = comp
            break
    res = {"params": {"rule": P.rule, "R": P.right_depth, "k": P.left_depth,
                      "w": "".join(map(str, P.period_word)), "Q": P.max_q,
                      "wedge_right": P.wedge_right, "pin_audit": P.pin_audit,
                      "pin_full": P.pin_full},
           "states": len(states), "edges": sum(len(a) for a in adj),
           "capped": capped, "pin_violations": pin_hits, "witness": None}
    if capped:
        res["verdict"] = "INCONCLUSIVE (state cap hit)"
        return res
    if good is None:
        res["verdict"] = "EMPTY"
        return res
    res["verdict"] = "NONEMPTY"
    res["witness"] = _witness(states, adj, good, P)
    return res


def _witness(states, adj, comp, P):
    cset = set(comp)
    prev = {0: None}
    dq = deque([0])
    entry = None
    while dq:
        n = dq.popleft()
        if n in cset:
            entry = n
            break
        for m, lt in adj[n]:
            if m not in prev:
                prev[m] = (n, lt)
                dq.append(m)
    prefix = []
    n = entry
    while prev[n] is not None:
        p_, lt = prev[n]
        prefix.append(lt)
        n = p_
    prefix.reverse()

    def bfs_in(src, targets):
        pv = {src: None}
        q_ = deque([src])
        while q_:
            u = q_.popleft()
            for mm, lt in adj[u]:
                if mm not in cset:
                    continue
                if mm in targets:
                    seq = []
                    x = u
                    while pv[x] is not None:
                        px, l2 = pv[x]
                        seq.append(l2)
                        x = px
                    seq.reverse()
                    seq.append(lt)
                    return mm, seq
                if mm not in pv:
                    pv[mm] = (u, lt)
                    q_.append(mm)
        return None, None

    accs = {n for n in comp if states[n][5]}
    if entry in accs:
        _, cyc = bfs_in(entry, {entry})
        return {"prefix": prefix, "cycle": cyc}
    mid, s1 = bfs_in(entry, accs)
    _, s2 = bfs_in(mid, {entry})
    return {"prefix": prefix, "cycle": s1 + s2}


def verify_witness(prefix, cycle, P: CParams, reps: int = 10):
    """Independent lasso check: forward rule, full wedge, centre periodicity,
    and infinitely many diffs at EVERY q <= Q (the conjunction)."""
    word = list(prefix) + list(cycle) * reps
    R = P.right_depth
    fwd, inv = FWD[P.rule], INV[P.rule]
    cols = {R: [ab & 1 for ab in word], R - 1: [ab >> 1 for ab in word]}
    x = R - 2
    while x >= P.x_min:
        up, upr = cols[x + 1], cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    for x in range(P.x_min + 1, R):
        for t in range(len(cols[x]) - 1):
            if t >= len(cols[x - 1]) or t >= len(cols[x + 1]):
                continue
            if cols[x][t + 1] != fwd(cols[x - 1][t], cols[x][t], cols[x + 1][t]):
                return False, f"forward rule fails at x={x}, t={t}"
    for x, vals in cols.items():
        if not P.wedge_right and x > 0:
            continue
        for t, v in enumerate(vals):
            if t < abs(x) and v != 0:
                return False, f"light cone fails at x={x}, t={t}"
            if t == abs(x) and v != 1:
                return False, f"edge fails at x={x}, t={t}"
    c, p = cols[0], len(P.period_word)
    onset = None
    for m in range(len(prefix) + 2 * p + 1):
        if all(c[t] == P.period_word[(t - m) % p] for t in range(m, len(c))):
            onset = m
            break
    if onset is None:
        return False, "no periodic onset in witness centre column"
    if P.pin_audit or P.pin_full:
        for x in range(P.x_min, R):
            for t in range(min(len(cols[x]), len(cols[x + 1])) - 1):
                a, b, c = cols[x][t], cols[x + 1][t], cols[x + 1][t + 1]
                if P.pin_audit and b == 1 and a == 0 and c != 1:
                    return False, f"pin cascade fails at x={x}, t={t}"
                if P.pin_full and b == 1 and a != 1 ^ c:
                    return False, f"full pin fails at x={x}, t={t}"
    m1 = cols[-1]
    tail = len(prefix) + len(cycle)
    for q in range(1, P.max_q + 1):
        d = sum(1 for t in range(tail, len(m1) - q) if m1[t] != m1[t + q])
        if d < max(1, reps - 5):
            return False, f"too few q={q} diffs in tail ({d})"
    return True, f"onset={onset}"


def regression(P: CParams, T: int = 300):
    """The true lone-seed letter sequence must never be rejected, and the
    derived columns must match simulation."""
    grid, B = simulate(P.rule, T + P.window_len + 4)
    word = [(grid[t][B + P.right_depth - 1] << 1) | grid[t][B + P.right_depth]
            for t in range(T)]
    mism = 0
    for n in range(P.window_len, T):
        win = tuple(word[n - P.window_len:n])
        rows = derive(win, P.base())
        for x, vals in rows.items():
            for i, v in enumerate(vals):
                t = n - 1 - max(0, P.right_depth - 1 - x) - (len(vals) - 1 - i)
                if 0 <= t < T and v != grid[t][B + x]:
                    mism += 1
    window, cnt, pin_hits = (), 0, [0]
    for letter in word[:T]:
        r = step_window(window, cnt, letter, P, pin_hits)
        if r is None:
            return mism, False, pin_hits[0]
        window, _, _ = r
        cnt += 1
    return mism, True, pin_hits[0]
