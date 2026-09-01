#!/usr/bin/env python3
"""Exact derivation and preregistered controls for the period-two attack.

This script is deliberately solver-free.  It derives F^2 from the Rule 30
truth table, checks every radius-two neighborhood, and runs the bounded
controls fixed in PREREGISTRATION.md.  Its finite enumerations are controls,
not evidence for the infinite theorem.
"""

from __future__ import annotations

from dataclasses import dataclass


def f30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def f90(left: int, center: int, right: int) -> int:
    del center
    return left ^ right


def g30(bits: tuple[int, int, int, int, int]) -> int:
    """F^2 at the center from cells -2,-1,0,1,2."""
    am2, am1, a0, a1, a2 = bits
    return f30(
        f30(am2, am1, a0),
        f30(am1, a0, a1),
        f30(a0, a1, a2),
    )


def anf_terms(values: list[int], names: tuple[str, ...]) -> list[str]:
    """Return ANF monomials from a truth table indexed by bit mask."""
    coeff = values[:]
    n = len(names)
    for bit in range(n):
        for mask in range(1 << n):
            if mask & (1 << bit):
                coeff[mask] ^= coeff[mask ^ (1 << bit)]
    terms: list[str] = []
    for mask, coefficient in enumerate(coeff):
        if not coefficient:
            continue
        factors = [names[i] for i in range(n) if mask & (1 << i)]
        terms.append("1" if not factors else "*".join(factors))
    return terms


def derive_macro_rule() -> tuple[list[str], list[str]]:
    names = ("a[-2]", "a[-1]", "a[0]", "a[1]", "a[2]")
    g_values: list[int] = []
    d_values: list[int] = []
    phase01_count = 0
    for mask in range(32):
        bits = tuple((mask >> i) & 1 for i in range(5))
        direct = g30(bits)

        # Independent two-row evaluation of the same radius-two cone.
        row1 = [f30(bits[j], bits[j + 1], bits[j + 2]) for j in range(3)]
        twice = f30(row1[0], row1[1], row1[2])
        assert direct == twice, (bits, direct, twice)

        offset = 6
        packed = sum(bit << (offset + i - 2) for i, bit in enumerate(bits))
        packed_mask = (1 << 13) - 1
        packed = step_integer(packed, packed_mask, 30)
        packed = step_integer(packed, packed_mask, 30)
        assert direct == ((packed >> offset) & 1), (bits, direct, packed)

        g_values.append(direct)
        d_values.append(bits[2] ^ direct)

        even0_odd1_next0 = (
            bits[2] == 0
            and f30(bits[1], bits[2], bits[3]) == 1
            and direct == 0
        )
        spatial_pattern = (
            bits[2] == 0
            and bits[0] == bits[3]
            and bits[1] == 1 - bits[3]
        )
        assert even0_odd1_next0 == spatial_pattern, bits
        phase01_count += int(even0_odd1_next0)

    assert phase01_count == 4  # two central patterns, with a[2] free
    return anf_terms(g_values, names), anf_terms(d_values, names)


def check_defect_recurrence() -> None:
    """Exhaust the exact two-orbit Rule 30 defect recurrence (64/64)."""
    for mask in range(64):
        sl, sc, sr, dl, dc, dr = ((mask >> i) & 1 for i in range(6))
        direct = f30(sl ^ dl, sc ^ dc, sr ^ dr) ^ f30(sl, sc, sr)
        formula = (
            dl ^ dc ^ dr
            ^ (sc & dr) ^ (sr & dc) ^ (dc & dr)
        )
        assert direct == formula, mask

    # If both consecutive center defects vanish, the center equation reduces
    # to d(-1)=(1 XOR center)*d(1).
    for center in (0, 1):
        for right_defect in (0, 1):
            left_defect = (1 ^ center) & right_defect
            next_center = left_defect ^ right_defect ^ (center & right_defect)
            assert next_center == 0


def step_integer(row: int, mask: int, rule: int) -> int:
    if rule == 30:
        return ((row << 1) ^ (row | (row >> 1))) & mask
    if rule == 90:
        return ((row << 1) ^ (row >> 1)) & mask
    raise ValueError(rule)


def trace_for_support(
    support: set[int], horizon: int, rule: int = 30
) -> list[int]:
    radius = max((abs(x) for x in support), default=0)
    offset = radius + horizon + 3
    width = 2 * offset + 1
    mask = (1 << width) - 1
    row = sum(1 << (offset + x) for x in support)
    trace: list[int] = []
    for _ in range(horizon + 1):
        trace.append((row >> offset) & 1)
        row = step_integer(row, mask, rule)
    return trace


def alternating_horizon(trace: list[int]) -> int:
    """Largest h such that trace[0..h] alternates and is nonconstant."""
    if len(trace) < 2 or trace[0] == trace[1]:
        return 0
    h = 1
    while h + 1 < len(trace) and trace[h + 1] == trace[h - 1]:
        h += 1
    return h


@dataclass(frozen=True)
class RadiusSweep:
    rows: int
    max_alternating_horizon: int
    alternating_witness: tuple[int, ...]
    max_zero_horizon: int
    max_one_horizon: int


def config_support(config: int, radius: int) -> tuple[int, ...]:
    return tuple(
        x for x in range(-radius, radius + 1)
        if (config >> (x + radius)) & 1
    )


def first_constant_failure(trace: list[int], bit: int) -> int:
    """Largest inclusive horizon on which every trace bit equals bit."""
    h = -1
    for value in trace:
        if value != bit:
            break
        h += 1
    return h


def exhaustive_radius_sweep(radius: int = 8, horizon: int = 64) -> RadiusSweep:
    offset = radius + horizon + 3
    width = 2 * offset + 1
    row_mask = (1 << width) - 1
    shift = offset - radius
    best_alt = -1
    best_cfg = 0
    best_zero = -1
    best_one = -1
    total = (1 << (2 * radius + 1)) - 1
    for config in range(1, total + 1):
        row = config << shift
        trace: list[int] = []
        for _ in range(horizon + 1):
            trace.append((row >> offset) & 1)
            row = step_integer(row, row_mask, 30)
        ah = alternating_horizon(trace)
        if ah > best_alt:
            best_alt, best_cfg = ah, config
        best_zero = max(best_zero, first_constant_failure(trace, 0))
        best_one = max(best_one, first_constant_failure(trace, 1))
    return RadiusSweep(
        rows=total,
        max_alternating_horizon=best_alt,
        alternating_witness=config_support(best_cfg, radius),
        max_zero_horizon=best_zero,
        max_one_horizon=best_one,
    )


def run_controls() -> None:
    g_terms, d_terms = derive_macro_rule()
    check_defect_recurrence()
    print("G=F^2 ANF:", " XOR ".join(g_terms))
    print("d=a XOR G(a) ANF:", " XOR ".join(d_terms))
    print("radius-two truth table: PASS (32/32)")
    print("two-orbit defect recurrence: PASS (64/64)")
    print(
        "phase 01 macro pattern: PASS; at every strobe "
        "(a[-2],a[-1],a[0],a[1]) is 1001 or 0100"
    )

    adversarial = trace_for_support({-8, -1, 6}, 20, 30)
    assert alternating_horizon(adversarial) == 14, adversarial
    assert adversarial[15] != adversarial[13]
    print("Rule 30 adversarial {-8,-1,6}: PASS (alternates through t=14, fails t=15)")

    rule90 = trace_for_support({-1, 1}, 128, 90)
    assert not any(rule90)
    print("Rule 90 {-1,1}: PASS (zero center for t=0..128)")

    sweep = exhaustive_radius_sweep()
    assert sweep.rows == 131071
    assert sweep.max_alternating_horizon == 14, sweep
    assert set(sweep.alternating_witness) == {-8, -1, 6}, sweep
    # Recorded sharp bounded validations for even support radius w=8.
    assert sweep.max_zero_horizon == 8, sweep
    assert sweep.max_one_horizon == 9, sweep
    print(
        "Rule 30 exhaustive [-8,8]: PASS; "
        f"{sweep.rows} nonzero rows, max alternating h="
        f"{sweep.max_alternating_horizon} witness={sweep.alternating_witness}, "
        f"max zero h={sweep.max_zero_horizon}, max one h={sweep.max_one_horizon}"
    )
    print("constant-fiber checks are bounded validation only, not new proofs")


if __name__ == "__main__":
    run_controls()
