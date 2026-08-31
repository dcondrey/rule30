"""Greatest-fixed-point attack on soficness of the WIDTH-2 column subshift.

SETUP.  For a left-permutive ECA with neighbourhood {-1,0,+1}, write c_x(t) =
s(t,x).  The local rule at position x+1,

    c_{x+1}(t+1) = c_x(t) XOR ( c_{x+1}(t) OR c_{x+2}(t) )      [rule 30]
    c_{x+1}(t+1) = c_x(t) XOR   c_{x+2}(t)                      [rule 90]

determines the column pair (c_{x+1}, c_{x+2}) from (c_x, c_{x+1}) up to the
choices left free by the OR.  Left permutivity makes the LEFT half free: given
(c_0, c_1), the columns c_{-1}, c_{-2}, ... are defined outright by
c_{x-1}(t) := c_x(t+1) XOR (c_x(t) OR c_{x+1}(t)) and satisfy the rule at every
x <= 0.  So

    (c_0, c_1) is the width-2 column trace of some configuration of Z
    <=>  the RIGHTWARD chain c_2, c_3, ... can be continued forever.

Define the monotone operator on subshifts of ({0,1}^2)^N

    Phi(Q) = { (c_0,c_1) : exists c_2 with the rule at x=1 holding for all t
                            and (c_1,c_2) in Q }.

Then W^(2) = the greatest fixed point of Phi = intersection of the decreasing
chain Q_0 = everything, Q_{k+1} = Phi(Q_k).  Each Q_k is SOFIC by construction
(one existential projection of a memory-1 SFT).  Q_k = pairs extendable to
depth k+1.

DECISION RULE.
  * If Q_{k+1} = Q_k for some k, the greatest fixed point IS Q_k, hence
    W^(2) = Q_k is SOFIC -- a proof, not evidence.
  * If the chain is strictly decreasing as far as computed, that proves
    NOTHING about soficness (obstruction H): a strictly decreasing chain of
    sofic shifts can still have sofic intersection.

Run: uv run python fixpoint.py --rule 30 --rounds 8
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib

log = logging.getLogger(__name__)

DEAD = -1
NLET = 4  # letter = c_0(t) + 2*c_1(t)


class DFA:
    """Deterministic safety automaton; every live state accepts."""

    def __init__(self, delta: list[list[int]], start: int = 0):
        self.delta = delta
        self.start = start

    @property
    def n(self) -> int:
        return len(self.delta)

    def word_count(self, length: int) -> int:
        """Number of length-`length` words with no dead transition."""
        cur = {self.start: 1}
        for _ in range(length):
            nxt: dict[int, int] = {}
            for q, c in cur.items():
                for a in range(NLET):
                    p = self.delta[q][a]
                    if p != DEAD:
                        nxt[p] = nxt.get(p, 0) + c
            cur = nxt
        return sum(cur.values())

    def accepts(self, word: list[int]) -> bool:
        q = self.start
        for a in word:
            q = self.delta[q][a]
            if q == DEAD:
                return False
        return True


def full_dfa() -> DFA:
    return DFA([[0] * NLET])


def trim(d: DFA) -> DFA:
    """Drop states not reachable from start or with no infinite forward path."""
    # forward-infinite: greatest fixed point of "has a live successor"
    live = [True] * d.n
    changed = True
    while changed:
        changed = False
        for q in range(d.n):
            if not live[q]:
                continue
            if not any(d.delta[q][a] != DEAD and live[d.delta[q][a]]
                       for a in range(NLET)):
                live[q] = False
                changed = True
    if not live[d.start]:
        return DFA([[DEAD] * NLET])  # empty language
    seen = {d.start}
    stack = [d.start]
    while stack:
        q = stack.pop()
        for a in range(NLET):
            p = d.delta[q][a]
            if p != DEAD and live[p] and p not in seen:
                seen.add(p)
                stack.append(p)
    idx = {q: i for i, q in enumerate(sorted(seen))}
    delta = [[DEAD] * NLET for _ in idx]
    for q, i in idx.items():
        for a in range(NLET):
            p = d.delta[q][a]
            if p != DEAD and live[p] and p in idx:
                delta[i][a] = idx[p]
    return DFA(delta, idx[d.start])


def minimize(d: DFA) -> DFA:
    """Partition refinement over {live, dead}; all live states are accepting."""
    d = trim(d)
    if d.n == 1 and all(x == DEAD for x in d.delta[0]):
        return d
    part = [0] * d.n  # all live states start in one class; DEAD is class -1
    while True:
        sig: dict[tuple, int] = {}
        new = [0] * d.n
        for q in range(d.n):
            key = (part[q],) + tuple(
                -1 if d.delta[q][a] == DEAD else part[d.delta[q][a]]
                for a in range(NLET)
            )
            if key not in sig:
                sig[key] = len(sig)
            new[q] = sig[key]
        if new == part:
            break
        part = new
    k = max(part) + 1
    delta = [[DEAD] * NLET for _ in range(k)]
    for q in range(d.n):
        for a in range(NLET):
            p = d.delta[q][a]
            delta[part[q]][a] = DEAD if p == DEAD else part[p]
    return trim(DFA(delta, part[d.start]))


def phi(q_dfa: DFA, rule: str) -> DFA:
    """One round: Phi(Q).  Letters are (c_0(t), c_1(t)); c_2(t) is projected out.

    NFA state: ('I',) or (q, a, b, e) = Q-state after reading (c_1,c_2) up to t,
    plus the pending obligation c_1(t+1) == a XOR (b OR e)  [rule 30]
                                          == a XOR e        [rule 90].
    """
    def q_letter(c1: int, c2: int) -> int:
        return c1 + 2 * c2

    def obligation(a: int, b: int, e: int) -> int:
        return a ^ ((b | e) if rule == "30" else e)

    init = ("I",)
    start_set = frozenset({init})
    seen = {start_set: 0}
    order = [start_set]
    delta: list[list[int]] = []
    i = 0
    while i < len(order):
        cur = order[i]
        row = [DEAD] * NLET
        for lt in range(NLET):
            a2, b2 = lt & 1, (lt >> 1) & 1  # c_0(t+1), c_1(t+1)
            nxt = set()
            for st in cur:
                if st == init:
                    for e2 in (0, 1):
                        p = q_dfa.delta[q_dfa.start][q_letter(b2, e2)]
                        if p != DEAD:
                            nxt.add((p, a2, b2, e2))
                else:
                    q, a, b, e = st
                    if b2 != obligation(a, b, e):
                        continue
                    for e2 in (0, 1):
                        p = q_dfa.delta[q][q_letter(b2, e2)]
                        if p != DEAD:
                            nxt.add((p, a2, b2, e2))
            if nxt:
                fs = frozenset(nxt)
                if fs not in seen:
                    seen[fs] = len(order)
                    order.append(fs)
                row[lt] = seen[fs]
        delta.append(row)
        i += 1
    return minimize(DFA(delta, 0))


def equal(a: DFA, b: DFA) -> bool:
    """Exact language equality of two safety automata (product reachability)."""
    seen = {(a.start, b.start)}
    stack = [(a.start, b.start)]
    while stack:
        p, q = stack.pop()
        for c in range(NLET):
            pa = a.delta[p][c] if p != DEAD else DEAD
            qb = b.delta[q][c] if q != DEAD else DEAD
            if (pa == DEAD) != (qb == DEAD):
                return False
            if pa != DEAD and (pa, qb) not in seen:
                seen.add((pa, qb))
                stack.append((pa, qb))
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--cap", type=int, default=2_000_000)
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--save", type=str, default="")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    dest = here / "out" / "fixpoint.json"

    out: dict[str, dict] = {}
    for rule in ("90", "30"):
        q = full_dfa()
        rows: list[dict] = []
        prev_counts: list[int] | None = None
        verdict = f"no fixed point within {args.rounds} rounds"
        for k in range(args.rounds):
            nq = phi(q, rule)
            counts = [nq.word_count(n) for n in range(1, args.nmax + 1)]
            # first word length at which depth k+1 is strictly stronger than k
            first_diff = None
            if prev_counts is not None:
                for i, (x, y) in enumerate(zip(prev_counts, counts)):
                    if x != y:
                        first_diff = i + 1
                        break
            rows.append({"round": k + 1, "states": nq.n, "word_counts": counts,
                         "first_length_where_depth_bites": first_diff})
            log.info("rule %s  round %2d: |Q| = %7d states  first-new-constraint"
                     " at length %s  L_n = %s",
                     rule, k + 1, nq.n, first_diff, counts[:12])
            dest.write_text(json.dumps({**out, rule: {"rounds": rows,
                                                      "verdict": "in progress"}},
                                       indent=1))
            if k > 0 and equal(nq, q):
                verdict = (f"FIXED POINT at round {k + 1}: Q_{k+1} = Q_{k}, so the "
                           f"greatest fixed point is Q_{k} -> width-2 column "
                           f"subshift is SOFIC with {nq.n} states")
                q = nq
                break
            q = nq
            if q.n > args.cap:
                verdict = f"state cap {args.cap} exceeded after round {k + 1}"
                break
        out[rule] = {"rounds": rows, "verdict": verdict}
        log.info("rule %s VERDICT: %s\n", rule, verdict)
        if args.save and rule == "30":
            (here / "out" / args.save).write_text(
                json.dumps({"start": q.start, "delta": q.delta}))
        dest.write_text(json.dumps(out, indent=1))
    log.info("wrote %s", dest)


if __name__ == "__main__":
    main()
