from __future__ import annotations

import random
import unittest

from inverse_trace_probe import reconstruct_left
from zero_tail_probe import (
    RULE_30,
    RULE_90,
    center_trace,
    class_m_finite_window,
    class_m_left_bit,
    eca_step,
    exhaustive_radius_check,
    forced_one_trace_left,
    forced_zero_trace_left,
    one_radius_certificate,
    radius_certificate,
)


class ZeroTailProbeTests(unittest.TestCase):
    def test_closed_transducer_matches_independent_triangular_inverse(self) -> None:
        rng = random.Random(0x30_0000)
        for depth in range(1, 25):
            for _ in range(20):
                right = (0,) + tuple(rng.randrange(2) for _ in range(depth))
                expected = reconstruct_left(RULE_30, (0,) * (depth + 1), right)
                self.assertEqual(forced_zero_trace_left(right, depth), expected)

    def test_first_one_closed_form(self) -> None:
        for first_one in range(1, 16):
            right = (
                (0,) * first_one
                + (1,)
                + tuple((position * 7 + first_one) & 1 for position in range(40))
            )
            observed = forced_zero_trace_left(right, len(right) - 1)
            expected = tuple(
                class_m_left_bit(first_one, depth) for depth in range(1, len(right))
            )
            self.assertEqual(observed, expected)

    def test_all_one_inverse_is_independent_of_the_right_half(self) -> None:
        rng = random.Random(0x30_1111)
        for depth in range(1, 25):
            for _ in range(20):
                right = (1,) + tuple(rng.randrange(2) for _ in range(depth))
                expected = reconstruct_left(RULE_30, (1,) * (depth + 1), right)
                self.assertEqual(forced_one_trace_left(right, depth), expected)

    def test_invariant_classes_map_down_to_c1(self) -> None:
        rng = random.Random(0xC1A55)
        for first_one in range(1, 10):
            for _ in range(20):
                extent = 40
                right = [0] * (extent + 1)
                right[first_one] = 1
                for position in range(first_one + 1, extent + 1):
                    right[position] = rng.randrange(2)
                row = class_m_finite_window(first_one, extent, right)
                evolved = eca_step(row, RULE_30)
                target_m = max(1, first_one - 1)
                # Ignore the two artificial truncation boundaries.  On the
                # exact infinite class this equality holds at every position.
                for position in range(-extent + 2, extent - 1):
                    if position < -target_m:
                        expected = position & 1
                    elif position == -target_m:
                        expected = 1
                    elif abs(position) < target_m:
                        expected = 0
                    elif position == target_m:
                        expected = 1
                    else:
                        continue
                    self.assertEqual(int(position in evolved), expected)

    def test_constructed_classes_have_zero_center_trace(self) -> None:
        rng = random.Random(0x2E20)
        horizon = 32
        for first_one in range(1, 12):
            right = [0] * (horizon + first_one + 3)
            right[first_one] = 1
            for position in range(first_one + 1, len(right)):
                right[position] = rng.randrange(2)
            row = class_m_finite_window(first_one, len(right) - 1, right)
            self.assertEqual(center_trace(row, horizon, RULE_30), (0,) * (horizon + 1))

    def test_symbolic_radius_certificates_match_forward_exhaustion(self) -> None:
        for radius in range(1, 8):
            certificate = radius_certificate(radius)
            exhaustive = exhaustive_radius_check(radius)
            self.assertTrue(exhaustive.matches_symbolic_certificate)
            self.assertEqual(
                certificate.maximum_zero_center_horizon,
                radius + (radius & 1),
            )
            self.assertEqual(certificate.forced_conflict_time % 2, 1)

    def test_every_symbolic_extremal_right_word_attains_the_bound(self) -> None:
        for radius in range(1, 8):
            certificate = radius_certificate(radius)
            for packed_right in range(1, 1 << radius):
                right = (0,) + tuple(
                    packed_right >> (position - 1) & 1
                    for position in range(1, radius + 1)
                )
                forced = forced_zero_trace_left(right, radius)
                offsets = tuple(
                    [-depth for depth, bit in enumerate(forced, 1) if bit]
                    + [position for position, bit in enumerate(right) if bit]
                )
                trace = center_trace(offsets, certificate.forced_conflict_time, RULE_30)
                self.assertEqual(
                    trace[: certificate.forced_conflict_time],
                    (0,) * certificate.forced_conflict_time,
                )
                self.assertEqual(trace[certificate.forced_conflict_time], 1)

    def test_rule90_finite_support_control(self) -> None:
        self.assertEqual(center_trace((-1, 1), 128, RULE_90), (0,) * 129)

    def test_all_one_radius_certificates_match_forward_exhaustion(self) -> None:
        for radius in range(1, 6):
            certificate = one_radius_certificate(radius)
            best = -1
            count = 0
            positions = tuple(range(-radius, 0)) + tuple(range(1, radius + 1))
            for packed in range(1 << (2 * radius)):
                offsets = (0,) + tuple(
                    position
                    for index, position in enumerate(positions)
                    if packed >> index & 1
                )
                trace = center_trace(offsets, certificate.forced_conflict_time, RULE_30)
                first_zero = next((time for time, bit in enumerate(trace) if not bit), None)
                horizon = (
                    certificate.forced_conflict_time
                    if first_zero is None
                    else first_zero - 1
                )
                if horizon > best:
                    best = horizon
                    count = 1
                elif horizon == best:
                    count += 1
            self.assertEqual(best, certificate.maximum_one_center_horizon)
            self.assertEqual(count, certificate.extremal_witness_count)

    def test_finite_set_oracle_rejects_nonquiescent_zero_rules(self) -> None:
        with self.assertRaises(ValueError):
            eca_step(set(), 1)

    def test_zero_trace_radius_bound_does_not_extend_phasewise(self) -> None:
        trace = center_trace((-1,), 7, RULE_30)
        self.assertEqual(trace, (0, 1, 0, 1, 0, 1, 0, 0))
        self.assertEqual(trace[:7], tuple(time & 1 for time in range(7)))
        self.assertNotEqual(trace[7], 7 & 1)


if __name__ == "__main__":
    unittest.main()
