"""Lemma B: exhaustive finite-state check of the leftward 2-periodic transduction.

Context.  Register row 31 proves: the lone-seed centre is eventually p-periodic
iff some nonzero finite row y satisfies Tr_0(y) = Tr_0(F^p(y)).  For p = 2 that
says exactly that the centre trace of y is 2-periodic from t = 0, i.e. the
trace is one of 0^inf, 1^inf, (01)^inf, (10)^inf.  Rows 25 and 26 close the two
constant words, so the whole p = 2 obligation is the two nonconstant words.

Lemma B (this script).  Let y be a row whose columns x and x+1 are BOTH
2-periodic in time.  Represent a 2-periodic column by the pair
(value at even t, value at odd t).  Left permutivity gives, for W = col_{x-1},

    U(t+1) = W(t) XOR (U(t) OR V(t))        [Rule 30, U = col_x, V = col_{x+1}]

so  W = (u1 XOR (u0 OR v0),  u0 XOR (u1 OR v1)),  and the leftward derivation
is the map  (U, V) |-> (W, U)  on the 16-element state set {0,1}^2 x {0,1}^2.

We verify EXHAUSTIVELY over all 16 states:
  (a) W is the unique 2-periodic column consistent with the rule;
  (b) the all-zero state ((0,0),(0,0)) is a FIXED POINT whose only predecessor
      is itself -- so it is unreachable from any other state;
  (c) every one of the other 15 states enters the 2-cycle
      ((1,1),(0,0)) <-> ((0,0),(1,1)) within at most 3 steps;
  (d) in that 2-cycle every second column is identically 1.

Hence if col_x and col_{x+1} are 2-periodic and the state is not all-zero, the
row has a 1 in infinitely many columns to the left of x, so it is NOT finitely
supported.  The initial state used below is (col_{-1}, col_0) with
col_0 in {(0,1), (1,0)} -- nonconstant trace -- so V != (0,0) and (b) applies.

Rule 90 control is run in the same frame: W = (u1 XOR v0, u0 XOR v1).

Stdlib only.  uv run python lemma_b_transduction.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

import rule30 as r30  # noqa: E402,F401  (repo shared substrate; used by the sibling script)

PAIRS = [(0, 0), (0, 1), (1, 0), (1, 1)]
STATES = [(u, v) for u in PAIRS for v in PAIRS]


def local(rule_num: int, l: int, m: int, rr: int) -> int:
    return (rule_num >> (l * 4 + m * 2 + rr)) & 1


def solve_W(rule_num: int, U: tuple[int, int], V: tuple[int, int]):
    """All 2-periodic W with U(t+1) = local(W(t), U(t), V(t)) for t = 0, 1."""
    out = []
    for W in PAIRS:
        ok = all(local(rule_num, W[t], U[t], V[t]) == U[(t + 1) % 2] for t in (0, 1))
        if ok:
            out.append(W)
    return out


def step(rule_num: int, st):
    U, V = st
    Ws = solve_W(rule_num, U, V)
    assert len(Ws) == 1, (rule_num, st, Ws)
    return (Ws[0], U)


def closed_form_check(rule_num: int) -> str:
    """Closed form vs brute-force inversion, all 16 states."""
    bad = []
    for U, V in STATES:
        (u0, u1), (v0, v1) = U, V
        if rule_num == 30:
            W = (u1 ^ (u0 | v0), u0 ^ (u1 | v1))
        else:
            W = (u1 ^ v0, u0 ^ v1)
        if solve_W(rule_num, U, V) != [W]:
            bad.append((U, V, W, solve_W(rule_num, U, V)))
    return f"closed form matches brute-force inversion on all 16 states: {not bad}" + (
        f"  MISMATCHES {bad}" if bad else ""
    )


def analyse(rule_num: int, out) -> None:
    p = lambda *a: print(*a, file=out)  # noqa: E731
    p(f"### rule {rule_num}: leftward 2-periodic transduction (U,V) -> (W,U)")
    p(closed_form_check(rule_num))
    p("")
    p("full transition table (state -> successor), 16 of 16 states:")
    succ = {}
    for st in STATES:
        succ[st] = step(rule_num, st)
        p(f"  {st} -> {succ[st]}")
    p("")

    ZERO = ((0, 0), (0, 0))
    preds = [s for s in STATES if succ[s] == ZERO]
    p(f"all-zero state {ZERO}: successor {succ[ZERO]}, "
      f"fixed point = {succ[ZERO] == ZERO}")
    p(f"predecessors of all-zero: {preds}")
    p(f"all-zero unreachable from any other state: {preds == [ZERO]}")
    p("")

    # Exhaustive cycle enumeration, not a heuristic walk.  On a 16-state
    # functional graph every transient is < 16, so the image of the state set
    # under succ^16 is EXACTLY the union of all cycles.
    img = set(STATES)
    for _ in range(len(STATES)):
        img = {succ[s] for s in img}
    p(f"union of all cycles (= image of all 16 states under succ^16), "
      f"{len(img)} states: {sorted(img)}")
    cycles = []
    left = set(img)
    while left:
        st = min(left)
        cyc, cur = [], st
        while cur not in cyc:
            cyc.append(cur)
            cur = succ[cur]
        assert cur == st, (st, cyc)
        left -= set(cyc)
        cycles.append(tuple(cyc))
    p(f"cycles, partitioning that image: {cycles}")
    p(f"number of cycles: {len(cycles)}  (sum of lengths {sum(len(c) for c in cycles)}"
      f" == |image| {len(img)}: {sum(len(c) for c in cycles) == len(img)})")

    # The load-bearing criterion is NOT "reaches one named 2-cycle".  It is:
    # every cycle other than all-zero contains a state with a NONZERO column,
    # so infinitely many columns x < 0 are nonzero at time 0 or time 1, and
    # then y or F(y) has infinite support.
    p("cycle audit (criterion: does the cycle contain a nonzero column?):")
    all_ok = True
    for cyc in cycles:
        cols = {st[0] for st in cyc} | {st[1] for st in cyc}
        nz = sorted(c for c in cols if c != (0, 0))
        ones_at_t0 = sorted(c for c in cols if c[0] == 1)
        tag = "ALL-ZERO (benign)" if not nz else "has nonzero column"
        if nz:
            all_ok = all_ok and True
        p(f"  cycle {cyc}: columns {sorted(cols)} -> {tag}; "
          f"columns with a 1 at t=0: {ones_at_t0}")
    nonbenign = [c for c in cycles if {st[0] for st in c} | {st[1] for st in c} != {(0, 0)}]
    p(f"cycles with NO nonzero column (would break Lemma B): "
      f"{[c for c in cycles if ({st[0] for st in c} | {st[1] for st in c}) == {(0, 0)} and c != (ZERO,)]}")
    p(f"every cycle except the all-zero fixed point contains a nonzero column: "
      f"{len(nonbenign) == len(cycles) - 1}")
    p("")

    # transients into a cycle, over the 15 non-all-zero states
    worst = 0
    for st in STATES:
        if st == ZERO:
            continue
        cur, path = st, []
        while cur not in path:
            path.append(cur)
            cur = succ[cur]
        worst = max(worst, path.index(cur))
    p(f"max transient before entering a cycle, over the 15 non-all-zero "
      f"states: {worst} steps")
    target = {((1, 1), (0, 0)), ((0, 0), (1, 1))}
    reach = 0
    for st in STATES:
        cur, k = st, 0
        while k <= 20 and cur not in target:
            cur = succ[cur]
            k += 1
        reach += cur in target
    p(f"states reaching the specific 2-cycle {sorted(target)}: {reach} of 16")
    p("")

    # states admissible as (col_{-1}, col_0) for a NONCONSTANT 2-periodic trace
    adm = [s for s in STATES if s[1] in ((0, 1), (1, 0))]
    p(f"admissible start states for a nonconstant 2-periodic centre trace "
      f"(V = col_0 in {{(0,1),(1,0)}}): {len(adm)} of 16")
    ok = all(st != ZERO for st in adm)
    p(f"no admissible start state is the all-zero state: {ok}")
    lands = []
    for st in adm:
        cur, path = st, []
        while cur not in path:
            path.append(cur)
            cur = succ[cur]
        lands.append(tuple(path[path.index(cur):]))
    benign = [c for c in lands if ({s[0] for s in c} | {s[1] for s in c}) == {(0, 0)}]
    p(f"admissible start states landing in an all-zero cycle: {len(benign)} of {len(adm)}")
    p(f"=> Lemma B conclusion (infinitely many nonzero columns to the left) "
      f"holds for every admissible start state: {not benign}")
    p("")


def rule90_finite_row_control(depth: int = 24, radius: int = 9) -> str:
    """Concrete Rule 90 control: how deep can a finite Rule 90 row match (01)^inf
    or (10)^inf in its centre trace?  Exhaustive over all rows supported in
    [-radius, radius]."""
    best = {}
    for phase in (0, 1):
        target = [(t + phase) % 2 for t in range(depth)]
        bestk, bestrow = -1, None
        for bits in range(1, 1 << (2 * radius + 1)):
            cells = {x - radius: (bits >> x) & 1 for x in range(2 * radius + 1)}
            cur = {x: v for x, v in cells.items() if v}
            k = 0
            for t in range(depth):
                if cur.get(0, 0) != target[t]:
                    break
                k += 1
                lo, hi = min(cur) - 1, max(cur) + 1
                nxt = {}
                for x in range(lo, hi + 1):
                    v = cur.get(x - 1, 0) ^ cur.get(x + 1, 0)
                    if v:
                        nxt[x] = 1
                cur = nxt
                if not cur:
                    break
            if k > bestk:
                bestk, bestrow = k, {x: v for x, v in cells.items() if v}
        best[phase] = (bestk, bestrow)
    return "\n".join(
        f"rule 90, all {2 ** (2 * radius + 1) - 1} nonzero rows in [-{radius},{radius}]: "
        f"max agreement with {'(01)' if ph == 0 else '(10)'}^inf = {best[ph][0]} of "
        f"{depth} steps, witness support {sorted(best[ph][1])}"
        for ph in (0, 1)
    )


def rule30_finite_row_control(depth: int = 24, radius: int = 9) -> str:
    from rule30 import simulate_seed  # noqa: F401  (kept: repo substrate import)
    best = {}
    for phase in (0, 1):
        target = [(t + phase) % 2 for t in range(depth)]
        bestk, bestrow = -1, None
        for bits in range(1, 1 << (2 * radius + 1)):
            cells = {x - radius: (bits >> x) & 1 for x in range(2 * radius + 1)}
            cur = {x: v for x, v in cells.items() if v}
            k = 0
            for t in range(depth):
                if cur.get(0, 0) != target[t]:
                    break
                k += 1
                lo, hi = min(cur) - 1, max(cur) + 1
                nxt = {}
                for x in range(lo, hi + 1):
                    v = cur.get(x - 1, 0) ^ (cur.get(x, 0) | cur.get(x + 1, 0))
                    if v:
                        nxt[x] = 1
                cur = nxt
            if k > bestk:
                bestk, bestrow = k, {x: v for x, v in cells.items() if v}
        best[phase] = (bestk, bestrow)
    return "\n".join(
        f"rule 30, all {2 ** (2 * radius + 1) - 1} nonzero rows in [-{radius},{radius}]: "
        f"max agreement with {'(01)' if ph == 0 else '(10)'}^inf = {best[ph][0]} of "
        f"{depth} steps, witness support {sorted(best[ph][1])}"
        for ph in (0, 1)
    )


if __name__ == "__main__":
    out = sys.stdout
    print("== Lemma B, exhaustive over all 16 states of {0,1}^2 x {0,1}^2 ==\n")
    analyse(30, out)
    print("== Rule 90 control, same frame ==\n")
    analyse(90, out)
    print("== Concrete finite-row control (MEASUREMENT, bounded; obstruction H) ==")
    print(rule30_finite_row_control())
    print(rule90_finite_row_control())
