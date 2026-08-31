"""Measure exact support-state compression for Rules 22 and 30.

This probe turns the proposed Rule 22 comparison into an executable control.
For the right-half support

    S_m(rule) = {r >= 0 : the cell at position r and time m is 1},

the Rule 22 paper proposes

    S_1 = {0, 1}, S_2 = {2},
    S_m = union_{c in S_(m-1)} {c-1, c, c+1}       (m odd),
    S_(2k) = 2 * {r in S_k : r == k (mod 2)}.       (m even)

Every proposed set is compared with an independent bit-parallel cellular-
automaton oracle.  The same exact states for Rule 30 are then measured using
three canonical descriptions: cardinality, interval runs, and reduced binary
decision diagrams.  Finally, the probe measures the symmetric-difference
"defect" obtained by applying each Rule 22 composition law to Rule 30.

The paper prints |S_m| = 2**popcount(floor(m/2)) * 3**(m mod 2).  That conflicts
with its own S_2={2} base case.  The recurrence implies an exponent of
popcount(floor(m/2))-1 for m>=2; both forms are reported rather than silently
repairing the source.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable, Literal, Sequence


RULE_22 = 22
RULE_30 = 30
KNOWN_RULE30_PREFIX = b"11011100110001011001001110101110"


@dataclass(frozen=True)
class SupportState:
    rule: int
    time: int
    positions: frozenset[int]

    def __post_init__(self) -> None:
        if self.time < 0 or any(position < 0 or position > self.time for position in self.positions):
            raise ValueError("right-half support positions must lie in [0, time]")

    @property
    def cardinality(self) -> int:
        return len(self.positions)

    @property
    def runs(self) -> int:
        return interval_run_count(self.positions)

    def decision_nodes(self, reduction: Literal["bdd", "zdd"]) -> int:
        diagram = DecisionDiagram(reduction)
        root = diagram.build(self.positions, max(0, self.time.bit_length() - 1))
        return diagram.reachable_nonterminals(root)


class DecisionDiagram:
    """Canonical fixed-width BDD/ZDD for membership in a finite integer set."""

    ZERO = 0
    ONE = 1

    def __init__(self, reduction: Literal["bdd", "zdd"]) -> None:
        self.reduction = reduction
        self.nodes: dict[int, tuple[int, int, int]] = {}
        self.unique: dict[tuple[int, int, int], int] = {}
        self.max_bit = -1

    def intern(self, bit: int, low: int, high: int) -> int:
        if self.reduction == "bdd" and low == high:
            return low
        if self.reduction == "zdd" and high == self.ZERO:
            return low
        key = (bit, low, high)
        if key not in self.unique:
            identifier = len(self.nodes) + 2
            self.unique[key] = identifier
            self.nodes[identifier] = key
        return self.unique[key]

    def build(self, values: Iterable[int], bit: int) -> int:
        self.max_bit = max(self.max_bit, bit)
        return self._build(frozenset(values), bit)

    def _build(self, value_set: frozenset[int], bit: int) -> int:
        if not value_set:
            return self.ZERO
        if bit < 0:
            return self.ONE
        mask = 1 << bit
        low = self._build(frozenset(value for value in value_set if value & mask == 0), bit - 1)
        high = self._build(frozenset(value for value in value_set if value & mask), bit - 1)
        return self.intern(bit, low, high)

    def contains(self, root: int, value: int) -> bool:
        node = root
        expected_bit = self.max_bit
        while node >= 2:
            bit, low, high = self.nodes[node]
            if self.reduction == "zdd" and expected_bit > bit:
                skipped_mask = ((1 << (expected_bit + 1)) - 1) ^ ((1 << (bit + 1)) - 1)
                if value & skipped_mask:
                    return False
            node = high if value & (1 << bit) else low
            expected_bit = bit - 1
        if self.reduction == "zdd" and node == self.ONE and expected_bit >= 0:
            return value & ((1 << (expected_bit + 1)) - 1) == 0
        return node == self.ONE

    def reachable_nonterminals(self, root: int) -> int:
        pending = [root]
        seen: set[int] = set()
        while pending:
            node = pending.pop()
            if node < 2 or node in seen:
                continue
            seen.add(node)
            _, low, high = self.nodes[node]
            pending.extend((low, high))
        return len(seen)


def eca_rows(rule: int, max_time: int) -> list[int]:
    """Return exact rows as Python bitsets in a fixed, zero-padded window."""
    if rule < 0 or rule > 255 or max_time < 0:
        raise ValueError("rule must be an ECA number and max_time must be non-negative")
    width = 2 * max_time + 3
    center = max_time + 1
    mask = (1 << width) - 1
    row = 1 << center
    rows = [row]
    for _ in range(max_time):
        left = (row << 1) & mask
        middle = row
        right = row >> 1
        next_row = 0
        for neighborhood in range(8):
            if not (rule >> neighborhood) & 1:
                continue
            term = mask
            for source, flag in ((left, 4), (middle, 2), (right, 1)):
                term &= source if neighborhood & flag else (~source & mask)
            next_row |= term
        row = next_row & mask
        rows.append(row)
    return rows


def support_states(rule: int, max_time: int) -> list[SupportState]:
    center = max_time + 1
    return [
        SupportState(
            rule,
            time,
            frozenset(
                position
                for position in range(time + 1)
                if (row >> (center + position)) & 1
            ),
        )
        for time, row in enumerate(eca_rows(rule, max_time))
    ]


def rule22_recursive_support(time: int, memo: dict[int, frozenset[int]] | None = None) -> frozenset[int]:
    if time < 1:
        raise ValueError("the published Rule 22 recurrence begins at time 1")
    states = {} if memo is None else memo
    if 1 not in states:
        states[1] = frozenset((0, 1))
    if 2 not in states:
        states[2] = frozenset((2,))
    if time in states:
        return states[time]
    if time & 1:
        prior = rule22_recursive_support(time - 1, states)
        states[time] = frozenset(
            position
            for center in prior
            for position in (center - 1, center, center + 1)
            if position >= 0
        )
    else:
        half = time // 2
        prior = rule22_recursive_support(half, states)
        states[time] = frozenset(2 * position for position in prior if position % 2 == half % 2)
    return states[time]


def printed_rule22_cardinality(time: int) -> int:
    if time < 1:
        raise ValueError("time must be positive")
    return 2 ** ((time // 2).bit_count()) * 3 ** (time & 1)


def recurrence_rule22_cardinality(time: int) -> int:
    if time < 1:
        raise ValueError("time must be positive")
    if time == 1:
        return 2
    return 2 ** ((time // 2).bit_count() - 1) * 3 ** (time & 1)


def interval_run_count(values: Iterable[int]) -> int:
    ordered = sorted(values)
    return sum(index == 0 or value != ordered[index - 1] + 1 for index, value in enumerate(ordered))


def rule22_composition_guess(states: Sequence[SupportState], time: int) -> frozenset[int]:
    if time < 3:
        return states[time].positions
    if time & 1:
        return frozenset(
            position
            for center in states[time - 1].positions
            for position in (center - 1, center, center + 1)
            if position >= 0
        )
    half = time // 2
    return frozenset(
        2 * position
        for position in states[half].positions
        if position % 2 == half % 2
    )


def check_controls(max_time: int) -> tuple[int | None, int | None, int | None]:
    rule22 = support_states(RULE_22, max_time)
    recurrence_mismatch = None
    printed_formula_mismatch = None
    corrected_formula_mismatch = None
    memo: dict[int, frozenset[int]] = {}
    for time in range(1, max_time + 1):
        observed = rule22[time].positions
        if recurrence_mismatch is None and rule22_recursive_support(time, memo) != observed:
            recurrence_mismatch = time
        if printed_formula_mismatch is None and printed_rule22_cardinality(time) != len(observed):
            printed_formula_mismatch = time
        if corrected_formula_mismatch is None and recurrence_rule22_cardinality(time) != len(observed):
            corrected_formula_mismatch = time
    return recurrence_mismatch, printed_formula_mismatch, corrected_formula_mismatch


def fit_exponent(points: Sequence[tuple[int, int]]) -> float | None:
    usable = [(x, y) for x, y in points if x > 1 and y > 0]
    if len(usable) < 2:
        return None
    xs = [math.log(x) for x, _ in usable]
    ys = [math.log(y) for _, y in usable]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    denominator = sum((value - mean_x) ** 2 for value in xs)
    if denominator == 0:
        return None
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denominator


def report(max_time: int) -> None:
    recurrence_bad, printed_bad, corrected_bad = check_controls(max_time)
    print("## controls")
    print(f"rule22_recurrence_first_mismatch={recurrence_bad}")
    print(f"printed_cardinality_first_mismatch={printed_bad}")
    print(f"recurrence_cardinality_first_mismatch={corrected_bad}")

    rule22 = support_states(RULE_22, max_time)
    rule30 = support_states(RULE_30, max_time)
    prefix = bytes(
        ord("1") if rule30[time].positions and 0 in rule30[time].positions else ord("0")
        for time in range(min(len(KNOWN_RULE30_PREFIX), max_time + 1))
    )
    if max_time >= len(KNOWN_RULE30_PREFIX) - 1:
        assert prefix == KNOWN_RULE30_PREFIX, "Rule 30 center-column oracle mismatch"

    targets = sorted(
        {
            time
            for exponent in range(max_time.bit_length())
            for time in (1 << exponent, (1 << exponent) - 1)
            if 1 <= time <= max_time
        }
    )
    print("\n## canonical support states")
    print("rule time cells runs bdd zdd composition_defect defect_bdd defect_zdd")
    rule30_defect_points: list[tuple[int, int]] = []
    for rule, states in ((RULE_22, rule22), (RULE_30, rule30)):
        for time in targets:
            state = states[time]
            guess = rule22_composition_guess(states, time)
            defect = state.positions ^ guess
            defect_state = SupportState(rule, time, defect)
            if rule == RULE_30:
                rule30_defect_points.append((time, defect_state.decision_nodes("bdd")))
            print(
                f"{rule:4d} {time:5d} {state.cardinality:5d} {state.runs:4d} "
                f"{state.decision_nodes('bdd'):4d} {state.decision_nodes('zdd'):4d} "
                f"{defect_state.cardinality:18d} {defect_state.decision_nodes('bdd'):10d} "
                f"{defect_state.decision_nodes('zdd'):10d}"
            )

    exponent = fit_exponent(rule30_defect_points)
    print("\n## discriminator")
    print(
        "rule30_rule22_composition_defect_bdd_exponent="
        + ("unavailable" if exponent is None else f"{exponent:.6f}")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-time", type=int, default=1024)
    args = parser.parse_args()
    if args.max_time < len(KNOWN_RULE30_PREFIX) - 1:
        parser.error(f"max-time must be at least {len(KNOWN_RULE30_PREFIX) - 1}")
    report(args.max_time)


if __name__ == "__main__":
    main()
