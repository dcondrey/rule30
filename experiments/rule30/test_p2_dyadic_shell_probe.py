from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from center_column import center_column
from p2_dyadic_shell_probe import (
    integrated_prefix_energy,
    read_band_cache,
    records,
    shell_record,
)


class DyadicShellTest(unittest.TestCase):
    def test_small_rule30_records(self) -> None:
        bits = center_column(32)
        found = records(bits, 1, 4)
        self.assertEqual(
            [
                (row.shell_sum, row.shell_max_abs, row.prefix_at_end)
                for row in found
            ],
            [(0, 1, 2), (0, 2, 2), (0, 2, 2), (2, 3, 4)],
        )

    def test_maximum_uses_partial_shells(self) -> None:
        # Prefix and shell endpoint discrepancies vanish, while the shell has
        # a strict internal excursion.  Endpoint-only tests would miss it.
        bits = bytes([1, 0, 1, 0, 1, 1, 0, 0])
        row = shell_record(bits, 2)
        self.assertEqual(row.prefix_at_start, 0)
        self.assertEqual(row.shell_sum, 0)
        self.assertEqual(row.prefix_at_end, 0)
        self.assertEqual(row.shell_max_abs, 2)
        self.assertEqual(row.integrated_prefix_energy, 6)

    def test_integrated_energy_and_peak_inequalities(self) -> None:
        # Exhaust every signed word of length eight.  These are the two
        # deterministic inequalities behind the energy equivalence.
        for encoded in range(1 << 8):
            values = [1 if encoded & (1 << index) else -1 for index in range(8)]
            running = 0
            maximum = 0
            for value in values:
                running += value
                maximum = max(maximum, abs(running))
            energy = integrated_prefix_energy(values)
            self.assertLessEqual(energy, len(values) * maximum * maximum)
            self.assertGreaterEqual(8 * energy, maximum**3)

    def test_cache_format_is_little_endian_uint32(self) -> None:
        words = [0, 1 << 15, (1 << 15) | 7, 9]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "band.bin"
            path.write_bytes(b"".join(word.to_bytes(4, "little") for word in words))
            self.assertEqual(read_band_cache(path, 4), bytes([0, 1, 1, 0]))

    def test_rejects_short_input(self) -> None:
        with self.assertRaises(ValueError):
            shell_record(bytes(7), 2)


if __name__ == "__main__":
    unittest.main()
