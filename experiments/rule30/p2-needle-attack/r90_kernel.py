#!/usr/bin/env python3
"""Rule 90 carry-kernel derivation, grounding, and pre-flight for the period-2
forced-continuation census control.

Self-contained: imports nothing from ../p1-period2-invariant. Fresh
reimplementation of the carry action / cone algebra so the control does not
inherit the Rule 30 arm's code (Control 2 wants an independent harness).

See r90_PREREG.md for the frozen method. Nothing here consumes a census number;
this module derives and validates the KERNEL only.
"""
from __future__ import annotations

from itertools import product

# ---------------------------------------------------------------------------
# Literal ground-truth simulators (both rules), for the kernel cross-check.
# ---------------------------------------------------------------------------


def f30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def f90(left: int, center: int, right: int) -> int:
    del center  # Rule 90 s(t+1,x)=s(t,x-1) XOR s(t,x+1): centre cell vanishes.
    return left ^ right


def step_integer(row: int, mask: int, rule: int) -> int:
    """One packed-row CA step. bit x = s(t,x); (row<<1) exposes s(t,x-1)."""
    if rule == 30:
        return ((row << 1) ^ (row | (row >> 1))) & mask
    if rule == 90:
        return ((row << 1) ^ (row >> 1)) & mask
    raise ValueError(rule)


def evolve_single_seed(steps: int, rule) -> list[dict[int, int]]:
    """Literal lone-seed space-time diagram (dict per row, position -> cell)."""
    rows = [{0: 1}]
    for _ in range(steps):
        old = rows[-1]
        lo, hi = min(old) - 1, max(old) + 1
        rows.append(
            {
                x: rule(old.get(x - 1, 0), old.get(x, 0), old.get(x + 1, 0))
                for x in range(lo, hi + 1)
            }
        )
    return rows


def two_phase_macro(bits5, rule) -> int:
    """F^2 at the centre from cells -2..2: two applications of the local rule."""
    row1 = [rule(bits5[j], bits5[j + 1], bits5[j + 2]) for j in range(3)]
    return rule(row1[0], row1[1], row1[2])


def two_phase_macro_packed(bits5, rule_number: int) -> int:
    """Independent grounding: step a packed row twice, read the centre."""
    offset = 6
    packed = sum(bit << (offset + i - 2) for i, bit in enumerate(bits5))
    mask = (1 << 13) - 1
    packed = step_integer(packed, mask, rule_number)
    packed = step_integer(packed, mask, rule_number)
    return (packed >> offset) & 1


# ---------------------------------------------------------------------------
# Carry actions. carry_action(symbol, state) -> 2*c' + d', symbol=(a,b),
# state=(c,d), a=symbol>>1, b=symbol&1, c=state>>1, d=state&1.
# ---------------------------------------------------------------------------


def _forward(rule_c, rule_d):
    """Build the 4x4 FORWARD table from bit-level c' and d' rules."""

    def action(symbol, state):
        a, b = symbol >> 1, symbol & 1
        c, d = state >> 1, state & 1
        return 2 * rule_c(a, b, c, d) + rule_d(a, b, c, d)

    return tuple(
        tuple(action(symbol, state) for state in range(4)) for symbol in range(4)
    )


# Rule 30: c' = c ^ (a|b) = f30(l=c, centre=a, right=b); d' = d ^ (c|a).
FORWARD_30 = _forward(lambda a, b, c, d: c ^ (a | b), lambda a, b, c, d: d ^ (c | a))

# Rule 150 (the mislabeled `use_or=False` in carry_transducer.py): c'=c^(a^b), d'=d^(c^a).
FORWARD_150 = _forward(lambda a, b, c, d: c ^ (a ^ b), lambda a, b, c, d: d ^ (c ^ a))

# The four genuine Rule 90 candidates (centre drops; each g keeps one argument).
FORWARD_K1 = _forward(lambda a, b, c, d: c ^ a, lambda a, b, c, d: d ^ a)  # collapse kept
FORWARD_K2 = _forward(lambda a, b, c, d: c ^ a, lambda a, b, c, d: d ^ c)  # collapse kept
FORWARD_K3 = _forward(lambda a, b, c, d: c ^ b, lambda a, b, c, d: d ^ a)  # collapse broken
FORWARD_K4 = _forward(lambda a, b, c, d: c ^ b, lambda a, b, c, d: d ^ c)  # collapse broken

KERNELS = {
    "R30": FORWARD_30,
    "K1(c^a,d^a)": FORWARD_K1,
    "K2(c^a,d^c)": FORWARD_K2,
    "K3(c^b,d^a)": FORWARD_K3,
    "K4(c^b,d^c)": FORWARD_K4,
}
RULE90_KERNELS = ["K1(c^a,d^a)", "K2(c^a,d^c)", "K3(c^b,d^a)", "K4(c^b,d^c)"]


def swap(state: int) -> int:
    return 2 * (state & 1) + (state >> 1)


def invert(transform):
    inverse = [0] * 4
    for state, following in enumerate(transform):
        inverse[following] = state
    return tuple(inverse)


def cone_algebra(forward):
    """Return (INVERSE, BOUNDARY, cone_local) derived from a FORWARD table."""
    inverse = tuple(map(invert, forward))
    boundary = inverse[3]

    def cone_local(left, right):
        return inverse[swap(left)][right]

    return inverse, boundary, cone_local


# ---------------------------------------------------------------------------
# Control 1: kernel cross-check against a direct Rule 90 simulation.
# ---------------------------------------------------------------------------


def control1_macro_grounding() -> dict:
    """The two-phase local rule reproduces a direct packed CA simulation, both
    rules, all 32 radius-2 neighbourhoods."""
    out = {}
    for name, local, number in (("rule30", f30, 30), ("rule90", f90, 90)):
        ok = all(
            two_phase_macro(b, local) == two_phase_macro_packed(b, number)
            for b in product((0, 1), repeat=5)
        )
        out[name] = ok
    return out


def control1_rule150_mislabel() -> dict:
    """`use_or=False` in carry_transducer.py is the Rule 150 double application,
    bit-for-bit, not Rule 90."""
    use_or_false = _forward(
        lambda a, b, c, d: c ^ (a ^ b), lambda a, b, c, d: d ^ (c ^ a)
    )
    return {
        "use_or_false_table": use_or_false,
        "equals_rule150": use_or_false == FORWARD_150,
        "differs_from_all_rule90": all(
            use_or_false != KERNELS[k] for k in RULE90_KERNELS
        ),
    }


def control1_reproduces_rule30_reference() -> dict:
    """Fresh FORWARD_30 and cone_local reproduce the published Rule 30 tables."""
    # Published values (dyadic_periodicity_analyzer.py):
    ref_forward = ((0, 1, 3, 2), (2, 3, 1, 0), (3, 2, 1, 0), (3, 2, 1, 0))
    ref_cone = ((0, 1, 3, 2), (3, 2, 1, 0), (3, 2, 0, 1), (3, 2, 1, 0))
    ref_boundary = (3, 2, 1, 0)
    _, boundary, cone_local = cone_algebra(FORWARD_30)
    cone = tuple(tuple(cone_local(l, r) for r in range(4)) for l in range(4))
    return {
        "forward_matches": FORWARD_30 == ref_forward,
        "cone_matches": cone == ref_cone,
        "boundary_matches": boundary == ref_boundary,
        "collapse_23": FORWARD_30[2] == FORWARD_30[3],
    }


# ---------------------------------------------------------------------------
# Pre-flight (frozen method): permutation + forced-continuation uniqueness.
# ---------------------------------------------------------------------------


def append_dependency_edge(cone_local, boundary, edge, previous_endpoint, value):
    following = [boundary[value]]
    if not edge:
        return tuple(following)
    following.append(cone_local(previous_endpoint, following[0]))
    for order in range(2, len(edge) + 1):
        following.append(cone_local(edge[order - 2], following[-1]))
    return tuple(following)


def preflight(name: str, forward, max_prefix: int = 6) -> dict:
    is_perm = all(set(t) == set(range(4)) for t in forward)
    _, boundary, cone_local = cone_algebra(forward)

    # Newest-cut uniqueness: for every reachable (edge, endpoint) prefix, the map
    # value -> append(...)[-1] must be a bijection over {0,1,2,3}.
    unique = True
    # Walk the {1,2}^k prefix trie with zero padding, exactly as the census does.
    states = set()
    edge = ()
    endpoint = None
    for _ in range(max_prefix):  # zero padding
        edge = append_dependency_edge(cone_local, boundary, edge, endpoint, 0)
        endpoint = 0
    frontier = {(edge, endpoint)}
    for _ in range(max_prefix):
        nxt = set()
        for (edge, endpoint) in frontier:
            cuts = [
                append_dependency_edge(cone_local, boundary, edge, endpoint, v)[-1]
                for v in range(4)
            ]
            if set(cuts) != set(range(4)):
                unique = False
            for v in (1, 2):
                ne = append_dependency_edge(cone_local, boundary, edge, endpoint, v)
                nxt.add((ne, v))
        frontier = nxt
        states |= frontier
    return {"permutation": is_perm, "forced_uniqueness": unique}


def main() -> None:
    print("=== Control 1a: two-phase macro grounded vs direct packed CA ===")
    for rule, ok in control1_macro_grounding().items():
        print(f"  {rule}: two_phase_macro == step_integer^2 over 32 nbhds -> {ok}")

    print("\n=== Control 1b: use_or=False in carry_transducer.py is RULE 150 ===")
    m = control1_rule150_mislabel()
    print(f"  use_or=False table = {m['use_or_false_table']}")
    print(f"  == Rule 150 double-application: {m['equals_rule150']}")
    print(f"  != every genuine Rule 90 kernel: {m['differs_from_all_rule90']}")

    print("\n=== Control 1c: fresh FORWARD_30/cone_local reproduce the reference ===")
    for k, v in control1_reproduces_rule30_reference().items():
        print(f"  {k}: {v}")

    print("\n=== Kernel tables and the collapse structure ===")
    for name in ["R30", "K1(c^a,d^a)", "K2(c^a,d^c)", "K3(c^b,d^a)", "K4(c^b,d^c)"]:
        fwd = KERNELS[name]
        print(
            f"  {name:12s} FORWARD={fwd}  collapse[2]==[3]={fwd[2] == fwd[3]}  "
            f"distinct_left_actions={len(set(fwd))}"
        )

    print("\n=== Pre-flight (permutation + forced-continuation uniqueness) ===")
    for name in ["R30"] + RULE90_KERNELS:
        pf = preflight(name, KERNELS[name])
        print(f"  {name:12s} permutation={pf['permutation']} "
              f"forced_uniqueness={pf['forced_uniqueness']}")


if __name__ == "__main__":
    main()
