from __future__ import annotations

import unittest
from itertools import product

from period3_active_core import quotient_step
from period3_signature import (
    exhaustive_control,
    interior_step,
    leading_zeros,
    signature,
    signature_step,
)


class PeriodThreeSignatureTest(unittest.TestCase):
    def test_complete_small_control(self) -> None:
        exhaustive_control(6)

    def test_two_steps_consume_a_deep_coordinate(self) -> None:
        for length in range(8):
            for word in product(range(3), repeat=length):
                twice = interior_step(interior_step(word))
                self.assertGreaterEqual(
                    leading_zeros(twice),
                    min(length, leading_zeros(word) + 1),
                )

    def test_signature_bits_are_successive_parities(self) -> None:
        word = (2, 0, 1, 2, 1, 0, 2)
        value = signature(word)
        current = word
        for layer in range(2 * len(word) + 3):
            expected = sum(symbol != 0 for symbol in current) & 1
            self.assertEqual((value >> layer) & 1, expected)
            current = interior_step(current)

    def test_free_step_semiconjugacy(self) -> None:
        word = (1, 2, 0, 2, 1, 1)
        for center in (0, 1):
            self.assertEqual(
                signature(quotient_step(word, center)),
                signature_step(signature(word), center),
            )


if __name__ == "__main__":
    unittest.main()
