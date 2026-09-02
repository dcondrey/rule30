from __future__ import annotations

import unittest
from itertools import product

from period3_survival_automaton import (
    accepting_state,
    direct_survives,
    exhaustive_control,
    shortest_survivor,
    state_after_word,
)


class PeriodThreeSurvivalAutomatonTest(unittest.TestCase):
    def test_complete_small_control(self) -> None:
        exhaustive_control(6, 4)

    def test_shortest_witness_is_minimal(self) -> None:
        period = (0, 1, 1)
        phase = 0
        horizon = 11
        result = shortest_survivor(period, phase, horizon)
        self.assertEqual(result.length, 9)
        assert result.word is not None
        self.assertTrue(direct_survives(result.word, period, phase, horizon))
        for length in range(result.length):
            self.assertFalse(
                any(
                    direct_survives(word, period, phase, horizon)
                    for word in product(range(3), repeat=length)
                )
            )

    def test_empty_word_acceptance_matches_literal(self) -> None:
        for period in ((0, 1, 1), (0, 0, 1)):
            for phase in range(3):
                for horizon in range(12):
                    self.assertEqual(
                        accepting_state(0, period, phase, horizon),
                        direct_survives((), period, phase, horizon),
                    )

    def test_state_word_evaluator(self) -> None:
        word = (2, 0, 1, 2, 1)
        horizon = 8
        state = state_after_word(word, horizon)
        self.assertTrue(0 <= state < 1 << horizon)


if __name__ == "__main__":
    unittest.main()

