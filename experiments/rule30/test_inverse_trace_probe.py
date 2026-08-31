from __future__ import annotations

import random
import unittest

from inverse_trace_probe import (
    RULE_30,
    RULE_90,
    evolve_once_packed,
    is_left_permutive,
    periodic_reconstruction_certificate,
    reconstruct_left_column,
    reconstruct_left,
    rotated_defect_front,
    trace_from_halves,
)


class InverseTraceProbeTests(unittest.TestCase):
    def test_left_permutivity_classifier(self) -> None:
        self.assertTrue(is_left_permutive(RULE_30))
        self.assertTrue(is_left_permutive(RULE_90))
        self.assertFalse(is_left_permutive(110))

    def test_reconstructs_random_finite_rows(self) -> None:
        rng = random.Random(0x30)
        for rule in (30, 90, 120, 180, 210):
            self.assertTrue(is_left_permutive(rule))
            for horizon in range(1, 18):
                for _ in range(8):
                    left = tuple(rng.randrange(2) for _ in range(horizon))
                    right = tuple(rng.randrange(2) for _ in range(horizon + 1))
                    trace = trace_from_halves(rule, left, right)
                    self.assertEqual(reconstruct_left(rule, trace, right), left)

    def test_every_new_left_cell_has_unit_center_sensitivity(self) -> None:
        rng = random.Random(0x90)
        for rule in (RULE_30, RULE_90):
            horizon = 24
            left = [rng.randrange(2) for _ in range(horizon)]
            right = tuple(rng.randrange(2) for _ in range(horizon + 1))
            baseline = trace_from_halves(rule, left, right)
            for depth in range(1, horizon + 1):
                changed = left.copy()
                changed[depth - 1] ^= 1
                observed = trace_from_halves(rule, changed, right)
                self.assertEqual(observed[:depth], baseline[:depth])
                self.assertNotEqual(observed[depth], baseline[depth])

    def test_rule90_periodic_center_is_required_adversarial_control(self) -> None:
        certificate = periodic_reconstruction_certificate(
            RULE_90,
            base_time=1,
            period=1,
            horizon=256,
        )
        self.assertEqual(certificate.agreement_after_first_period, 256)
        self.assertIsNone(certificate.first_temporal_mismatch)
        self.assertIsNone(certificate.first_spatial_mismatch)
        self.assertIsNone(certificate.first_forced_one_outside_actual_support)

    def test_rule30_known_agreement_run_maps_to_same_spatial_depth(self) -> None:
        certificate = periodic_reconstruction_certificate(
            RULE_30,
            base_time=1855,
            period=148,
            horizon=256,
        )
        self.assertEqual(certificate.agreement_after_first_period, 18)
        self.assertEqual(certificate.first_temporal_mismatch, 166)
        self.assertEqual(certificate.first_spatial_mismatch, 166)

    def test_invalid_or_nonpermutive_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            reconstruct_left(110, (0, 0), (0, 0))
        with self.assertRaises(ValueError):
            reconstruct_left(RULE_30, (0, 0), (1, 0))
        with self.assertRaises(ValueError):
            reconstruct_left(RULE_30, (0, 0), (0,))

    def test_rotated_column_identity_matches_rule30_rows(self) -> None:
        left = (1, 0, 1, 1, 0, 1)
        right = (1, 1, 0, 1, 0, 0, 1)
        trace = trace_from_halves(RULE_30, left, right)
        # Reconstruct the position -1 column from the center and +1 columns
        # of an independently evolved finite row.
        horizon = len(left)
        columns = []
        for position in (0, 1):
            # Directly evolve the full row while reading the requested column.
            width = 2 * horizon + 5
            center = horizon + 2
            mask = (1 << width) - 1
            row = sum(bit << (center - depth) for depth, bit in enumerate(left, 1))
            row |= sum(bit << (center + offset) for offset, bit in enumerate(right))
            observed = []
            for _ in range(horizon + 1):
                observed.append((row >> (center + position)) & 1)
                row = evolve_once_packed(RULE_30, row, mask)
            columns.append(tuple(observed))
        reconstructed = reconstruct_left_column(columns[0], columns[1])

        width = 2 * horizon + 5
        center = horizon + 2
        mask = (1 << width) - 1
        row = sum(bit << (center - depth) for depth, bit in enumerate(left, 1))
        row |= sum(bit << (center + offset) for offset, bit in enumerate(right))
        actual_left_column = []
        for _ in range(horizon):
            actual_left_column.append((row >> (center - 1)) & 1)
            row = evolve_once_packed(RULE_30, row, mask)
        self.assertEqual(reconstructed, tuple(actual_left_column))
        self.assertEqual(trace, columns[0])

    def test_periodic_mask_erases_only_one_phase_defects(self) -> None:
        self.assertEqual(rotated_defect_front((0, 1), 64, 32), tuple(range(64, 32, -1)))
        self.assertEqual(rotated_defect_front((0, 1), 65, 32), (None,) * 32)


if __name__ == "__main__":
    unittest.main()
