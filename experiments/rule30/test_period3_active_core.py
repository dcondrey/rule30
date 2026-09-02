from __future__ import annotations

import unittest

from period3_active_core import (
    check_frontier_conjugacy,
    core_step,
    deep_quotient,
    driven_step,
    lifetime,
    normalize,
    pair_parity,
    quotient_driven_step,
    quotient_step,
    raw_symbol_quotient,
)


class PeriodThreeActiveCoreTest(unittest.TestCase):
    def test_normalization_and_parity(self) -> None:
        self.assertEqual(normalize((1, 2, 0, 0)), (1, 2))
        self.assertEqual(pair_parity((0, 1, 2, 3)), 1)

    def test_selected_scan_finishes_at_zero(self) -> None:
        for core in ((), (1,), (2, 0, 1), (3, 2, 1, 3)):
            for center in (0, 1):
                result = core_step(core, center)
                self.assertFalse(result and result[-1] == 0)

    def test_pin_schedules(self) -> None:
        # 011 checks parity 0 at phase one and parity 1 at phase two.
        self.assertIsNotNone(driven_step((1, 1), (0, 1, 1), 1))
        self.assertIsNone(driven_step((1,), (0, 1, 1), 1))
        self.assertIsNotNone(driven_step((1,), (0, 1, 1), 2))
        self.assertIsNone(driven_step((1, 1), (0, 1, 1), 2))

    def test_three_symbol_quotient_is_exact(self) -> None:
        self.assertEqual([raw_symbol_quotient(symbol) for symbol in range(4)], [0, 1, 2, 2])
        cores = ((), (1,), (2,), (3,), (0, 1, 2), (3, 0, 1, 2))
        for core in cores:
            for center in (0, 1):
                self.assertEqual(
                    deep_quotient(core_step(core, center)),
                    quotient_step(deep_quotient(core), center),
                )
            for period in ((0, 1, 1), (0, 0, 1)):
                for phase in range(3):
                    raw = driven_step(core, period, phase)
                    quotient = quotient_driven_step(deep_quotient(core), period, phase)
                    self.assertEqual(None if raw is None else deep_quotient(raw), quotient)

    def test_frontier_conjugacy(self) -> None:
        check_frontier_conjugacy(7)

    def test_recorded_long_lived_cores(self) -> None:
        result_011 = lifetime((2, 0, 1, 0, 1, 0, 1, 2), (0, 1, 1), 2)
        self.assertEqual(result_011.steps, 21)
        result_001 = lifetime((0, 1, 0, 1, 2, 1, 0, 0, 0, 1), (0, 0, 1), 2)
        self.assertEqual(result_001.steps, 37)


if __name__ == "__main__":
    unittest.main()
