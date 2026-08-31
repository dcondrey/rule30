from __future__ import annotations

import unittest

from periodicity_bridge_probe import (
    RULE_30,
    RULE_90,
    classify_left_permutive_quiescent,
    defect_identity_violations,
    evolve_rows,
    first_doubling_separation_counterexample,
    longest_center_agreement,
    moving_collision_defect_holds,
    residual_is_nonlinear,
    rule_from_left_permutive_residual,
    trace_collision_holds,
)


def naive_rows(rule: int, max_time: int, initial: set[int]) -> list[set[int]]:
    rows = [set(initial)]
    for _ in range(max_time):
        prior = rows[-1]
        next_row = set()
        low = min(prior, default=0) - 1
        high = max(prior, default=0) + 1
        for position in range(low, high + 1):
            neighborhood = (
                (int(position - 1 in prior) << 2)
                | (int(position in prior) << 1)
                | int(position + 1 in prior)
            )
            if (rule >> neighborhood) & 1:
                next_row.add(position)
        rows.append(next_row)
    return rows


class PeriodicityBridgeProbeTests(unittest.TestCase):
    def test_oracle_matches_naive_rules_and_initial_conditions(self) -> None:
        max_time = 32
        for rule in (30, 90, 110):
            for initial in ({0}, {0, 1}):
                packed, center = evolve_rows(rule, max_time, initial)
                naive = naive_rows(rule, max_time, initial)
                for time, expected in enumerate(naive):
                    observed = {
                        position
                        for position in range(-max_time - 1, max_time + 2)
                        if (packed[time] >> (center + position)) & 1
                    }
                    self.assertEqual(observed, expected)

    def test_rule30_residual_and_nonlinear_subclass(self) -> None:
        self.assertEqual(rule_from_left_permutive_residual(0b1110), RULE_30)
        nonlinear = {
            item.rule
            for item in classify_left_permutive_quiescent(128)
            if item.nonlinear
        }
        self.assertEqual(nonlinear, {30, 120, 180, 210})
        self.assertTrue(residual_is_nonlinear(0b1110))
        self.assertFalse(residual_is_nonlinear(0b1010))

    def test_defect_identity_is_exact_for_rule30(self) -> None:
        for shift in (1, 2, 3, 7, 31, 64):
            self.assertEqual(defect_identity_violations(RULE_30, 512, shift), [])

    def test_rule90_is_adversarial_center_periodicity_control(self) -> None:
        run = longest_center_agreement(RULE_90, 512, 16)
        self.assertEqual(run.shift, 1)
        self.assertEqual(run.start_time, 1)
        self.assertEqual(run.length, 511)
        self.assertTrue(run.left_defect_seen or run.right_defect_seen)

    def test_rule30_has_finite_local_observability_counterexample(self) -> None:
        run = longest_center_agreement(RULE_30, 4096, 256)
        self.assertEqual((run.length, run.shift, run.start_time), (18, 148, 1855))
        self.assertTrue(run.left_defect_seen)
        self.assertTrue(run.right_defect_seen)

    def test_doubling_separation_fails_at_four(self) -> None:
        self.assertEqual(first_doubling_separation_counterexample(64), 4)

    def test_center_trace_collision_has_moving_defect_certificate(self) -> None:
        self.assertTrue(trace_collision_holds(1024))
        self.assertTrue(moving_collision_defect_holds(1024))


if __name__ == "__main__":
    unittest.main()
