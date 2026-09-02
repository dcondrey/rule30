from __future__ import annotations

import unittest

from center_column import center_column
from p2_time_index_walsh_probe import (
    anf_profile,
    bit_derivative_correlations,
    dyadic_block_energies,
    maximum_aligned_restriction,
    record,
    walsh_transform,
    xor_autocorrelations,
)


class TimeIndexWalshTest(unittest.TestCase):
    def test_known_transforms(self) -> None:
        self.assertEqual(walsh_transform([1, 1, 1, 1]), [4, 0, 0, 0])
        self.assertEqual(walsh_transform([1, -1, 1, -1]), [0, 4, 0, 0])

    def test_parseval(self) -> None:
        values = [1, -1, -1, 1, -1, -1, 1, 1]
        spectrum = walsh_transform(values)
        self.assertEqual(sum(value * value for value in spectrum), len(values) ** 2)

    def test_aligned_restriction(self) -> None:
        values = [1, 1, -1, -1, 1, -1, 1, -1]
        self.assertEqual(maximum_aligned_restriction(values), 2)

    def test_dyadic_block_energies(self) -> None:
        values = [1, 1, -1, -1, 1, -1, 1, -1]
        # Leaves, pairs, blocks of four, and the root.
        self.assertEqual(dyadic_block_energies(values), [8, 8, 0, 0])

    def test_tree_energy_bounds_every_prefix(self) -> None:
        values = [1, 1, -1, 1, -1, -1, 1, -1]
        energy = sum(dyadic_block_energies(values))
        bound_squared = len(values).bit_length() * energy
        running = 0
        for value in values:
            running += value
            self.assertLessEqual(running * running, bound_squared)

    def test_bit_derivatives(self) -> None:
        parity = [1, -1, -1, 1]
        self.assertEqual(bit_derivative_correlations(parity), [-4, -4])

    def test_xor_autocorrelations_against_direct_sum(self) -> None:
        values = [1, -1, -1, -1, 1, 1, -1, 1]
        direct = [
            sum(values[index] * values[index ^ shift] for index in range(8))
            for shift in range(8)
        ]
        self.assertEqual(xor_autocorrelations(values), direct)

    def test_anf_profile(self) -> None:
        # x0 XOR x1 on inputs 00,01,10,11.
        self.assertEqual(anf_profile([0, 1, 1, 0]), (1, 2))

    def test_small_rule30_shell(self) -> None:
        row = record(center_column(32), 4)
        self.assertEqual(row.dc, -2)
        self.assertEqual(row.max_shell_prefix, 3)
        self.assertEqual(row.max_abs_walsh, 6)
        self.assertEqual(row.dyadic_tree_energy, 40)
        self.assertEqual((row.anf_degree, row.anf_terms), (4, 8))

    def test_rejects_non_power_of_two(self) -> None:
        with self.assertRaises(ValueError):
            walsh_transform([1, -1, 1])


if __name__ == "__main__":
    unittest.main()
