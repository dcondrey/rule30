from __future__ import annotations

import unittest

from support_state_probe import (
    DecisionDiagram,
    RULE_22,
    RULE_30,
    check_controls,
    eca_rows,
    recurrence_rule22_cardinality,
    rule22_composition_guess,
    support_states,
)


def naive_rows(rule: int, max_time: int) -> list[set[int]]:
    rows = [{0}]
    for _ in range(max_time):
        prior = rows[-1]
        next_row = set()
        for position in range(min(prior) - 1, max(prior) + 2):
            neighborhood = (
                (int(position - 1 in prior) << 2)
                | (int(position in prior) << 1)
                | int(position + 1 in prior)
            )
            if (rule >> neighborhood) & 1:
                next_row.add(position)
        rows.append(next_row)
    return rows


class SupportStateProbeTests(unittest.TestCase):
    def test_bit_parallel_oracle_matches_naive_rule22_and_rule30(self) -> None:
        max_time = 64
        center = max_time + 1
        for rule in (RULE_22, RULE_30):
            packed = eca_rows(rule, max_time)
            naive = naive_rows(rule, max_time)
            for time, expected in enumerate(naive):
                observed = {
                    position
                    for position in range(-time, time + 1)
                    if (packed[time] >> (center + position)) & 1
                }
                self.assertEqual(observed, expected)

    def test_rule22_recurrence_and_corrected_cardinality(self) -> None:
        recurrence_bad, printed_bad, corrected_bad = check_controls(512)
        self.assertIsNone(recurrence_bad)
        self.assertEqual(printed_bad, 1)
        self.assertIsNone(corrected_bad)
        self.assertEqual(recurrence_rule22_cardinality(6), 2)

    def test_rule22_composition_has_no_defect(self) -> None:
        states = support_states(RULE_22, 256)
        for time in range(3, len(states)):
            self.assertEqual(rule22_composition_guess(states, time), states[time].positions)

    def test_decision_diagrams_preserve_membership(self) -> None:
        values = frozenset((0, 2, 3, 7, 11, 15))
        for reduction in ("bdd", "zdd"):
            diagram = DecisionDiagram(reduction)
            root = diagram.build(values, 3)
            self.assertGreater(diagram.reachable_nonterminals(root), 0)
            for value in range(16):
                self.assertEqual(diagram.contains(root, value), value in values)


if __name__ == "__main__":
    unittest.main()
