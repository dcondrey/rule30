from __future__ import annotations

import unittest

from additive_conservation_probe import conservation_record, gf2_rank


class AdditiveConservationTest(unittest.TestCase):
    def test_gf2_rank(self) -> None:
        self.assertEqual(gf2_rank([0b0011, 0b0101, 0b0110]), 2)

    def test_rule30_has_only_trivial_densities_in_test_range(self) -> None:
        for window in range(1, 9):
            row = conservation_record(30, window)
            self.assertTrue(row.only_trivial_rational_densities_certified)
            self.assertEqual(
                row.mod2_density_projection_dimension,
                row.trivial_density_dimension,
            )

    def test_number_conserving_rule184_is_positive_control(self) -> None:
        for window in range(1, 6):
            row = conservation_record(184, window)
            self.assertFalse(row.only_trivial_rational_densities_certified)
            self.assertEqual(
                row.mod2_density_projection_dimension,
                row.trivial_density_dimension + 1,
            )

    def test_identity_rule_has_many_conserved_densities(self) -> None:
        row = conservation_record(204, 5)
        self.assertEqual(row.mod2_density_projection_dimension, 32)
        self.assertGreater(
            row.mod2_density_projection_dimension,
            row.trivial_density_dimension,
        )


if __name__ == "__main__":
    unittest.main()
