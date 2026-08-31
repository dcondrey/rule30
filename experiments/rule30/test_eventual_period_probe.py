from __future__ import annotations

import importlib.util
import unittest

from eventual_period_probe import (
    RULE_30,
    RULE_90,
    direct_center_trace,
    exact_period_search,
)
from inverse_trace_probe import reconstruct_left
from zero_tail_probe import eca_step


@unittest.skipIf(importlib.util.find_spec("z3") is None, "z3-solver is not installed")
class EventualPeriodProbeTests(unittest.TestCase):
    def test_period_two_radius_one_returns_known_extremal_and_unsat_core(self) -> None:
        certificate = exact_period_search(RULE_30, 1, 2, 12)
        self.assertEqual(certificate.maximum_certified_periodic_horizon, 6)
        self.assertEqual(certificate.first_unsatisfiable_time, 7)
        self.assertEqual(certificate.extremal_witness_offsets, (-1,))
        self.assertEqual(certificate.extremal_witness_trace, (0, 1, 0, 1, 0, 1, 0))
        self.assertTrue(certificate.irreducible_core_times)

    def test_symbolic_results_match_direct_exhaustion_on_cheap_grid(self) -> None:
        for period in range(2, 5):
            for radius in range(1, 4):
                certificate = exact_period_search(RULE_30, radius, period, 16)
                best = period - 1
                for packed in range(1, 1 << (2 * radius + 1)):
                    offsets = tuple(
                        position
                        for index, position in enumerate(range(-radius, radius + 1))
                        if packed >> index & 1
                    )
                    trace = direct_center_trace(RULE_30, offsets, 16)
                    if len(set(trace[:period])) != 2:
                        continue
                    horizon = period - 1
                    for time in range(period, 17):
                        if trace[time] != trace[time - period]:
                            break
                        horizon = time
                    best = max(best, horizon)
                self.assertEqual(certificate.maximum_certified_periodic_horizon, best)

    def test_rule90_constant_zero_is_a_required_sat_control(self) -> None:
        certificate = exact_period_search(
            RULE_90,
            support_radius=1,
            period=1,
            search_horizon=24,
            require_nonconstant_word=False,
        )
        self.assertIsNone(certificate.first_unsatisfiable_time)
        self.assertTrue(certificate.stopped_at_search_horizon)
        self.assertEqual(set(certificate.extremal_witness_offsets), {-1, 1})
        self.assertEqual(certificate.extremal_witness_trace, (0,) * 25)

    def test_period_two_inverse_stencil_is_exact(self) -> None:
        desired = (0, 1, 0, 1, 0)
        for packed_right in range(1 << 4):
            right = (0,) + tuple(packed_right >> index & 1 for index in range(4))
            left = reconstruct_left(RULE_30, desired, right)
            r1, r2, r3 = right[1:4]
            self.assertEqual(
                left,
                (1 ^ r1, r1, r1 | r2 | r3, 0),
            )

    def test_two_zero_phases_do_not_force_radius_two_mirror_symmetry(self) -> None:
        horizon = 8
        desired = tuple((0, 0, 1)[time % 3] for time in range(horizon + 1))
        right = (0, 1, 1) + (0,) * (horizon - 2)
        left = reconstruct_left(RULE_30, desired, right)
        self.assertEqual(left[:8], (1, 1, 0, 1, 0, 0, 0, 1))
        row = {
            -depth for depth, bit in enumerate(left, 1) if bit
        } | {
            position for position, bit in enumerate(right) if bit
        }
        evolved = set(row)
        for _ in range(3):
            evolved = eca_step(evolved, RULE_30)
        defect = row ^ evolved
        self.assertEqual((int(-1 in defect), int(1 in defect)), (1, 1))
        self.assertEqual((int(-2 in defect), int(2 in defect)), (0, 1))

    def test_invalid_nonconstant_period_one_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            exact_period_search(RULE_30, 1, 1, 8)


if __name__ == "__main__":
    unittest.main()
