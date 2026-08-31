from __future__ import annotations

import unittest

from transfer_monoid_probe import (
    candidate_center_bit,
    first_mismatch,
    gf2_poly_square_mod,
)


class TransferMonoidProbeTests(unittest.TestCase):
    def test_truncated_polynomial_square(self) -> None:
        self.assertEqual(gf2_poly_square_mod(0b1011, 6), 0b000101)

    def test_candidate_has_a_small_counterexample(self) -> None:
        mismatch = first_mismatch(64)
        self.assertIsNotNone(mismatch)
        assert mismatch is not None
        index, candidate, oracle = mismatch
        self.assertEqual(candidate, candidate_center_bit(index))
        self.assertNotEqual(candidate, oracle)


if __name__ == "__main__":
    unittest.main()
