from __future__ import annotations

import unittest

from period3_zero_tail_dual import (
    BRANCH_SECTION,
    LEX_FACTORS,
    factor_vector,
    finite_lex_control,
    verify_equality_is_zero_language,
    verify_lex_theorem,
    word_action,
    zero_transition,
)


class PeriodThreeZeroTailDualTest(unittest.TestCase):
    def test_inverse_branch_sections(self) -> None:
        self.assertEqual(BRANCH_SECTION, ((2, 0, 0), (2, 0, 2)))

    def test_zero_transition_examples(self) -> None:
        first = zero_transition(tuple(map(int, "110101011")))
        self.assertEqual(first, (0, tuple(map(int, "200212021200"))))
        assert first is not None
        self.assertLessEqual(factor_vector(first[1]), factor_vector(tuple(map(int, "110101011"))))

    def test_word_action_is_injective_on_level_three(self) -> None:
        word = (2, 0, 1, 2, 1)
        outputs = [word_action(word, value)[0] for value in range(8)]
        self.assertEqual(sorted(outputs), list(range(8)))

    def test_complete_small_control(self) -> None:
        finite_lex_control(7)

    def test_all_length_graph_certificate(self) -> None:
        report = verify_lex_theorem()
        self.assertEqual(tuple(row[0] for row in report), LEX_FACTORS)
        self.assertTrue(all(row[1] <= 0 for row in report))

    def test_full_equality_is_zero_language(self) -> None:
        self.assertEqual(
            verify_equality_is_zero_language(),
            (452, 452, 452, 452),
        )


if __name__ == "__main__":
    unittest.main()
