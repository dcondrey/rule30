from __future__ import annotations

import unittest

from hashlife_center_probe import Hashlife1D, query_power_of_two
from right_cone_probe import center_trace


class HashlifeCenterTest(unittest.TestCase):
    def test_base_local_rule(self) -> None:
        for rule in (30, 90, 110):
            engine = Hashlife1D(rule)
            for word in range(16):
                bits = [(word >> shift) & 1 for shift in (3, 2, 1, 0)]
                node = engine.join(
                    engine.join(engine.leaves[bits[0]], engine.leaves[bits[1]]),
                    engine.join(engine.leaves[bits[2]], engine.leaves[bits[3]]),
                )
                self.assertEqual(
                    engine.bits(engine.advance(node)),
                    [
                        engine.local(bits[0], bits[1], bits[2]),
                        engine.local(bits[1], bits[2], bits[3]),
                    ],
                )

    def test_center_matches_direct_evolution(self) -> None:
        for rule in (30, 90):
            expected = center_trace(frozenset({0}), 128, rule)
            for time in (1, 2, 4, 8, 16, 32, 64, 128):
                self.assertEqual(query_power_of_two(rule, time).center, expected[time])

    def test_returned_center_block_matches_direct_row(self) -> None:
        rule = 30
        time = 16
        engine = Hashlife1D(rule)
        root = engine.set_bit(engine.zero(6), 2 * time)
        observed = engine.bits(engine.advance(root))

        row = frozenset({0})
        from right_cone_probe import step

        for _ in range(time):
            row = step(row, rule)
        expected = [int(position in row) for position in range(-time, time)]
        self.assertEqual(observed, expected)

    def test_rule90_is_compressed_positive_control(self) -> None:
        rule90 = query_power_of_two(90, 256)
        rule30 = query_power_of_two(30, 256)
        self.assertLess(rule90.advance_cache_misses, 64)
        self.assertGreater(rule30.advance_cache_misses, 1000)

    def test_rejects_non_power_of_two(self) -> None:
        with self.assertRaises(ValueError):
            query_power_of_two(30, 12)


if __name__ == "__main__":
    unittest.main()
