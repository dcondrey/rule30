from __future__ import annotations

import unittest
from collections import Counter

from center_column import center_column
from nersissian_block_audit import (
    block_increment,
    block_or_convolution,
    center_bit_via_blocks,
    evaluate_blocks,
    expand_blocks,
    support_blocks,
)


def direct_or_convolution(left: set[int], right: set[int]) -> set[int]:
    counts = Counter(a | b for a in left for b in right)
    return {value for value, count in counts.items() if count & 1}


class NersissianBlockAuditTest(unittest.TestCase):
    def test_published_support_rows(self) -> None:
        expected = {
            1: {0},
            2: {1},
            3: {1},
            4: {2},
            5: {2, 3, 4},
            6: {3, 5, 7},
            7: {3, 5, 8},
            8: {4, 6, 8, 9, 12, 14, 16},
        }
        for m, support in expected.items():
            self.assertEqual(expand_blocks(support_blocks(m)), support)

    def test_block_operations_against_expansion(self) -> None:
        left = [(4, 10), (8, 1), (16, 0)]
        right = [(3, 4), (5, 0)]
        expanded_left = expand_blocks(left)
        expanded_right = expand_blocks(right)
        self.assertEqual(
            expand_blocks(block_or_convolution(left, right)),
            direct_or_convolution(expanded_left, expanded_right),
        )
        self.assertEqual(
            expand_blocks(block_increment(left)),
            {value + 1 for value in expanded_left},
        )

    def test_zero_enforcer_evaluation(self) -> None:
        blocks = [(4, 10), (8, 1), (16, 0)]
        support = expand_blocks(blocks)
        for n in range(64):
            direct = sum((value & n) == value for value in support) & 1
            self.assertEqual(evaluate_blocks(blocks, n), direct)

    def test_center_bits_match_independent_oracle(self) -> None:
        expected = center_column(24)
        actual = bytes(center_bit_via_blocks(n) for n in range(24))
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
