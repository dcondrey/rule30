"""Cross-checks for the right-cone diagonal period engine.

The published period sequence is the oracle for the engine; the naive Rule 30
evaluator in ``right_cone_probe`` is the oracle for the diagonals themselves.
"""

import random
import unittest

import diagonal_period_probe as D
import right_cone_probe as R

# OEIS A094605 (Eric Rowland, 2004): "a(n) is the period of the n-th diagonal,
# from the right, of Rule 30 (begun from an initial black cell)".  Offset 1, so
# A094605(n) == PUBLISHED_PERIODS[n - 1].  Theorem: Rowland, "Local nested
# structure in rule 30", Complex Systems 16 (2006) 239-258, Lemma 2.
PUBLISHED_PERIODS = [
    1, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64, 64, 64, 64, 128,
    256, 256, 256, 256, 256, 256, 256, 256, 512, 1024, 1024, 2048, 2048, 4096,
]


def random_row(rng, lo=-8, hi=8):
    while True:
        cells = frozenset(x for x in range(lo, hi + 1) if rng.random() < 0.5)
        if cells:
            return cells


class Engine(unittest.TestCase):
    def test_center_column_matches_naive_evaluator(self):
        rng = random.Random(31)
        for _ in range(15):
            cells = random_row(rng)
            a_left, b = D.from_cells(cells)
            self.assertEqual(D.center_column(a_left, b, 30),
                             R.center_trace(cells, 30, 30), sorted(cells))

    def test_patterns_tile_to_the_diagonals(self):
        """One-period bookkeeping and the time-range engine must agree exactly."""
        rng = random.Random(32)
        horizon = (1 << 15) - 1
        for _ in range(6):
            cells = random_row(rng, -5, 5)
            a_left, _ = D.from_cells(cells)
            pats = D.diagonal_patterns(a_left, 24)
            ds = D.diagonals(a_left, 24, horizon)
            for j, (q, pat) in enumerate(pats):
                if q > horizon + 1:
                    continue
                self.assertEqual(D._tile(pat, q, horizon + 1), ds[j], (j, q))

    def test_periods_are_powers_of_two_and_pure(self):
        rng = random.Random(33)
        horizon = (1 << 16) - 1
        for _ in range(8):
            cells = random_row(rng)
            a_left, _ = D.from_cells(cells)
            pats = D.diagonal_patterns(a_left, 24)
            ds = D.diagonals(a_left, 24, horizon)
            for j, (q, _) in enumerate(pats):
                self.assertEqual(q & (q - 1), 0, (j, q))
                if 4 * q > horizon:
                    continue
                span = horizon - q
                self.assertEqual((ds[j] ^ (ds[j] >> q)) & ((1 << (span + 1)) - 1),
                                 0, ("preperiod is not zero", j, q))


class PublishedOracle(unittest.TestCase):
    def test_lone_seed_periods(self):
        got = D.diagonal_periods({0: 1}, len(PUBLISHED_PERIODS) - 1)
        self.assertEqual(got, PUBLISHED_PERIODS)

    def test_period_outruns_the_center_read(self):
        """c_t reads diagonal t at time t, and Q_j > j for 3 <= j <= 64.

        Monotonicity is measured here, not proved: Rowland's Lemma 2 bounds Q_j
        only by divisibility.  Given it, Q_64 = 2**27 extends this to j < 2**27.
        """
        periods = D.diagonal_periods({0: 1}, 64)
        self.assertEqual([j for j in range(65) if periods[j] <= j], [2])
        self.assertTrue(all(periods[j] >= periods[j - 1] for j in range(1, 65)))
        self.assertEqual(periods[64], 1 << 27)

    def test_closed_form_center(self):
        """c_t is the parity of the OR of the two diagonals above it, up to t-1."""
        horizon = 1 << 12
        ds = D.diagonals({0: 1}, 200, horizon)
        ref = R.center_trace(frozenset({0}), 200, 30)
        for t in range(1, 201):
            above = (ds[t - 1] if t >= 1 else 0) | (ds[t - 2] if t >= 2 else 0)
            self.assertEqual((above & ((1 << t) - 1)).bit_count() % 2, ref[t], t)


if __name__ == "__main__":
    unittest.main()
