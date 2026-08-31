"""Omega-automaton periodicity ladder for the Rule 30 center column (route R7).

Sound over-approximation: every constraint imposed here is a fact of the
lone-seed spacetime diagram (proofs in docs/rule30/RESULTS-ladder-rung0.md).

The automaton reads the pair of columns (R-1, R) as an omega-word over
{0,1}^2.  By left permutivity every column to the left is a function of that
pair through the inverse transduction

    col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))   [rule 30]
    col_{x-1}(t) = col_x(t+1) XOR col_{x+1}(t)                 [rule 90]

so any letter word is the column pair of a valid left half-plane, and the
lone-seed word is one of them.  Constraints imposed on the derived columns
down to x_min:

  * light cone: col_x(t) = 0 for t < |x|;
  * both edges: col_x(|x|) = 1;
  * center eventually periodic with tail word w (Buchi, onset guessed);
  * optionally Diff_q: col_{-1}(t) != col_{-1}(t-q) infinitely often.

Emptiness with Diff_q proves: center eventually-w-periodic forces col_{-1}
eventually q-periodic on every word the constraints admit, the lone-seed word
included.  Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5 then forbid the two adjacent
eventually periodic columns, so the true center is not eventually w-periodic
for any transient.  Nonemptiness proves nothing.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import dataclass

INV = {
    30: lambda an, a, b: an ^ (a | b),
    90: lambda an, a, b: an ^ b,
}
FWD = {
    30: lambda l, m, r: l ^ (m | r),
    90: lambda l, m, r: l ^ r,
}


@dataclass(frozen=True)
class Params:
    rule: int
    right_depth: int                # R >= 1; letters are columns (R-1, R)
    left_depth: int                 # k >= 0; wedge-checked down to column -k
    period_word: tuple[int, ...]    # tail word w of length p
    diff_q: int | None              # None = plain emptiness mode

    @property
    def x_min(self) -> int:
        k = self.left_depth
        if self.diff_q is not None:
            k = max(k, 1)           # Diff needs col_{-1}
        return -k

    @property
    def window_len(self) -> int:
        # col_x needs letters back to time t, delay R-1-x, so R - x letters.
        return self.right_depth - self.x_min

    @property
    def saturate(self) -> int:
        # wedge check for column x fires at letter time s = t + max(0, R-1-x)
        # with t <= |x|; the largest such s is R + 2|x_min| - 1.
        return self.right_depth + 2 * abs(self.x_min) + 1


def derive(window: tuple[int, ...], P: Params) -> dict[int, list[int]]:
    """rows[x] = values of column x over the window's time range.

    Letters are packed (a << 1) | b with a = col_{R-1}(t), b = col_R(t).
    rows[x] has length n - max(0, R-1-x); its last entry is the newest value.
    """
    R = P.right_depth
    inv = INV[P.rule]
    rows = {R: [ab & 1 for ab in window], R - 1: [ab >> 1 for ab in window]}
    x = R - 2
    while x >= P.x_min:
        up = rows[x + 1]
        if len(up) < 2:
            break
        upr = rows[x + 2]
        rows[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    return rows


def step_window(window, cnt, letter, P):
    """Advance the window by one letter; run wedge checks.

    Returns (new_window, c_val, m1_val) or None if a wedge check fails.
    cnt is the exact letter time when cnt < P.saturate, else saturated.
    """
    new_window = window + (letter,)
    if len(new_window) > P.window_len:
        new_window = new_window[-P.window_len:]
    rows = derive(new_window, P)
    R = P.right_depth
    sat = cnt >= P.saturate
    c_val = None
    m1_val = None
    for x, vals in rows.items():
        if not vals:
            continue
        v = vals[-1]
        if not sat:
            t = cnt - max(0, R - 1 - x)
            if t < 0:
                continue
            ax = abs(x)
            if t < ax:
                if v != 0:
                    return None
            elif t == ax:
                if v != 1:
                    return None
        if x == 0:
            c_val = v
        elif x == -1:
            m1_val = v
    return new_window, c_val, m1_val


def successors(state, letter, P, memo):
    """Nondeterministic successor states for one input letter.

    The Diff_q condition uses a guess-and-verify gadget instead of a full
    (q+1)-bit history: nondeterministically arm on a col_{-1} value, count
    down q further arrivals, then require the compared value to differ.  A
    run accepts (flag True) exactly at genuine diff events, so accepting
    runs exist iff the word has infinitely many q-diffs; the language is
    unchanged while the state cost drops from 2^(q+1) to 2(2q+1).
    """
    window, cnt, phase, d, _flag = state
    key = (window, min(cnt, P.saturate), letter)
    hit = memo.get(key)
    if hit is None:
        hit = step_window(window, cnt, letter, P)
        memo[key] = (hit,)
    else:
        hit = hit[0]
    if hit is None:
        return []
    new_window, c_val, m1_val = hit
    q = P.diff_q
    if q is not None and m1_val is not None:
        if d is None:
            dnexts = ((None, False), ((m1_val, q), False))
        else:
            b, j = d
            if j > 1:
                dnexts = (((b, j - 1), False),)
            elif m1_val != b:
                dnexts = ((None, True), ((m1_val, q), True))
            else:
                return []
    else:
        dnexts = ((d, False),)
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
    return [(new_window, new_cnt, ph, nd, fl)
            for ph in phases for nd, fl in dnexts]


def is_diff_state(state, P) -> bool:
    return state[4]


def explore(P: Params, max_states: int = 3_000_000):
    """BFS the reachable product graph.  Returns (states, adj, capped)."""
    init = ((), 0, None, None, False)
    ids = {init: 0}
    states = [init]
    adj = [[]]
    memo: dict = {}
    dq = deque([0])
    capped = False
    while dq:
        sid = dq.popleft()
        st = states[sid]
        for letter in range(4):
            for ns in successors(st, letter, P, memo):
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


def _sccs(nodes, adj_f):
    """Iterative Tarjan over the node subset; adj_f(n) yields successors."""
    index = {}
    low = {}
    on = set()
    stack = []
    out = []
    counter = [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(adj_f(root)))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for wnode in it:
                if wnode not in index:
                    index[wnode] = low[wnode] = counter[0]
                    counter[0] += 1
                    stack.append(wnode)
                    on.add(wnode)
                    work.append((wnode, iter(adj_f(wnode))))
                    advanced = True
                    break
                if wnode in on:
                    low[v] = min(low[v], index[wnode])
            if advanced:
                continue
            work.pop()
            if work:
                pv = work[-1][0]
                low[pv] = min(low[pv], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    u = stack.pop()
                    on.discard(u)
                    comp.append(u)
                    if u == v:
                        break
                out.append(comp)
    return out


def decide(P: Params, max_states: int = 3_000_000):
    """Decide emptiness.  Returns a result dict; 'empty' True is the theorem-
    grade outcome (subject to the soundness regression), False comes with a
    verified witness lasso."""
    states, adj, capped = explore(P, max_states)
    checking = [i for i, s in enumerate(states) if s[2] is not None]
    checking_set = set(checking)

    def adj_checking(n):
        for m, _ in adj[n]:
            if m in checking_set:
                yield m

    comps = _sccs(checking, adj_checking)
    self_loop = {n for n in checking for m, _ in adj[n] if m == n}
    good = None
    for comp in comps:
        cset = set(comp)
        nontrivial = len(comp) > 1 or (comp[0] in self_loop)
        if not nontrivial:
            continue
        if P.diff_q is None:
            good = comp
            break
        if any(is_diff_state(states[n], P) for n in comp):
            good = comp
            break
    result = {
        "params": {
            "rule": P.rule,
            "R": P.right_depth,
            "k": P.left_depth,
            "w": "".join(map(str, P.period_word)),
            "q": P.diff_q,
        },
        "states": len(states),
        "edges": sum(len(a) for a in adj),
        "capped": capped,
        "empty": good is None and not capped,
        "verdict": None,
        "witness": None,
    }
    if capped:
        result["verdict"] = "INCONCLUSIVE (state cap hit)"
        result["empty"] = False
        return result
    if good is None:
        result["verdict"] = "EMPTY"
        return result
    result["verdict"] = "NONEMPTY"
    result["witness"] = _witness(states, adj, good, P)
    return result


def _witness(states, adj, comp, P):
    """Letters of a prefix reaching the SCC and of an accepting cycle."""
    cset = set(comp)
    # BFS from init to any SCC node.
    prev = {0: None}
    dq = deque([0])
    entry = None
    while dq:
        n = dq.popleft()
        if n in cset:
            entry = n
            break
        for m, letter in adj[n]:
            if m not in prev:
                prev[m] = (n, letter)
                dq.append(m)
    prefix = []
    n = entry
    while prev[n] is not None:
        p_, letter = prev[n]
        prefix.append(letter)
        n = p_
    prefix.reverse()

    # cycle within the SCC from entry through a diff state (if diff mode).
    # Targets are tested on edge traversal so a path back to the source is
    # found even though the source is marked visited.
    def bfs_in(src, targets):
        pv = {src: None}
        q_ = deque([src])
        while q_:
            u = q_.popleft()
            for mm, letter in adj[u]:
                if mm not in cset:
                    continue
                if mm in targets:
                    seq = []
                    x = u
                    while pv[x] is not None:
                        px, lt = pv[x]
                        seq.append(lt)
                        x = px
                    seq.reverse()
                    seq.append(letter)
                    return mm, seq
                if mm not in pv:
                    pv[mm] = (u, letter)
                    q_.append(mm)
        return None, None

    if P.diff_q is None or is_diff_state(states[entry], P):
        _, cyc = bfs_in(entry, {entry})
        return {"prefix": prefix, "cycle": cyc}
    diffs = {n for n in comp if is_diff_state(states[n], P)}
    mid, seg1 = bfs_in(entry, diffs)
    _, seg2 = bfs_in(mid, {entry})
    return {"prefix": prefix, "cycle": seg1 + seg2}


def verify_witness(prefix, cycle, P: Params, reps: int = 8):
    """Independently verify a lasso via the forward rule, wedge facts,
    center periodicity of the tail, and diff events per cycle."""
    word = list(prefix) + list(cycle) * reps
    T = len(word)
    R = P.right_depth
    fwd = FWD[P.rule]
    cols = {R: [ab & 1 for ab in word], R - 1: [ab >> 1 for ab in word]}
    inv = INV[P.rule]
    x = R - 2
    while x >= P.x_min:
        up = cols[x + 1]
        upr = cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    # forward-rule check at every cell whose three parents are in the strip
    for x in range(P.x_min + 1, R):
        for t in range(len(cols[x]) - 1):
            if t >= len(cols[x - 1]) or t >= len(cols[x + 1]):
                continue
            want = fwd(cols[x - 1][t], cols[x][t], cols[x + 1][t])
            if cols[x][t + 1] != want:
                return False, f"forward rule fails at x={x}, t={t}"
    # wedge facts
    for x, vals in cols.items():
        ax = abs(x)
        for t, v in enumerate(vals):
            if t < ax and v != 0:
                return False, f"light cone fails at x={x}, t={t}"
            if t == ax and v != 1:
                return False, f"edge fails at x={x}, t={t}"
    # center tail periodicity for some onset in the first prefix+2p steps
    c = cols[0]
    p = len(P.period_word)
    onset_ok = None
    for m in range(len(prefix) + 2 * p + 1):
        if all(c[t] == P.period_word[(t - m) % p] for t in range(m, len(c))):
            onset_ok = m
            break
    if onset_ok is None:
        return False, "no periodic onset found in witness center column"
    # diff events in the cyclic tail
    if P.diff_q is not None:
        q = P.diff_q
        m1 = cols[-1]
        tail_from = len(prefix) + len(cycle)
        diffs = sum(
            1 for t in range(tail_from, len(m1) - q) if m1[t] != m1[t + q]
        )
        if diffs < max(1, reps - 3):
            return False, f"too few diff events in tail ({diffs})"
    return True, f"onset={onset_ok}"


def simulate(rule, T, extra=2):
    """Exact lone-seed evolution; grid[t][B + x] = s(t, x)."""
    B = T + extra
    width = 2 * B + 1
    fwd = FWD[rule]
    row = [0] * width
    row[B] = 1
    grid = [row]
    for _ in range(T):
        prev = grid[-1]
        nxt = [0] * width
        for i in range(1, width - 1):
            nxt[i] = fwd(prev[i - 1], prev[i], prev[i + 1])
        grid.append(nxt)
    return grid, B


def regression(rule, R, k, T=300):
    """Two checks against the exact diagram: (1) the derived columns match the
    simulation everywhere defined; (2) the true letter word threads the safety
    automaton (phase held at None) with zero wedge rejections."""
    P = Params(rule=rule, right_depth=R, left_depth=max(k, 1),
               period_word=(0,), diff_q=None)
    grid, B = simulate(rule, T)
    letters = [(grid[t][B + R - 1] << 1) | grid[t][B + R] for t in range(T)]
    # (1) transduction matches simulation
    cols = {R: [l & 1 for l in letters], R - 1: [l >> 1 for l in letters]}
    inv = INV[rule]
    x = R - 2
    while x >= P.x_min:
        up = cols[x + 1]
        upr = cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    mismatches = 0
    for x, vals in cols.items():
        for t, v in enumerate(vals):
            if v != grid[t][B + x]:
                mismatches += 1
    # (2) safety run
    state = ((), 0, None, None, False)
    memo: dict = {}
    ok = True
    for letter in letters:
        nxt = [s for s in successors(state, letter, P, memo) if s[2] is None]
        if not nxt:
            ok = False
            break
        state = nxt[0]
    return mismatches, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30, choices=(30, 90))
    ap.add_argument("--right-depth", "-R", type=int, required=True)
    ap.add_argument("--left-depth", "-k", type=int, default=1)
    ap.add_argument("--word", "-w", required=True,
                    help="tail word, e.g. 01")
    ap.add_argument("--diff-q", "-q", type=int, default=None)
    ap.add_argument("--max-states", type=int, default=3_000_000)
    args = ap.parse_args()
    P = Params(rule=args.rule, right_depth=args.right_depth,
               left_depth=args.left_depth,
               period_word=tuple(int(ch) for ch in args.word),
               diff_q=args.diff_q)
    res = decide(P, args.max_states)
    if res["witness"] is not None:
        okv, note = verify_witness(res["witness"]["prefix"],
                                   res["witness"]["cycle"], P)
        res["witness_verified"] = okv
        res["witness_note"] = note
    print(json.dumps(res))


if __name__ == "__main__":
    main()
