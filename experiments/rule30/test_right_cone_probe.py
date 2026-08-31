"""Cross-checks for the right-cone reconstruction.

The SMT horizon table in ``docs/rule30/RESULTS-eventual-period.md`` is the
oracle: this file reproduces it cell for cell from the bit-parallel sweep, with
no solver in the trust base.
"""

import random
import unittest

import right_cone_probe as R

# docs/rule30/RESULTS-eventual-period.md, "maximum absolute periodic-prefix
# horizon H".  Rows are periods 2..6, columns support radii w=1..8.
H_TABLE = {
    2: [6, 6, 6, 6, 8, 9, 9, 14],
    3: [4, 5, 9, 9, 9, 13, 13, 16],
    4: [6, 6, 7, 10, 12, 13, 13, 16],
    5: [10, 10, 10, 10, 12, 12, 13, 15],
    6: [7, 9, 13, 13, 13, 15, 15, 17],
}
ORACLE_DEPTH = 32


def rows_from(cells, horizon, rule):
    out = []
    cur = frozenset(cells)
    for _ in range(horizon + 1):
        out.append(cur)
        cur = R.step(cur, rule)
    return out


def diagonal(rows, k, t):
    return 1 if (t - k) in rows[t] else 0


def measured_h(period, width, depth=ORACLE_DEPTH):
    """Max over rows supported in [-width, width] of the p-periodic prefix horizon."""
    best = -1
    for word in R.nonconstant_words(period):
        target = R.periodic_target(word, depth)
        count, left_bits = R.sweep_bits(width, target, depth, R.RULE30)
        for k0 in R.first_forced_one(left_bits, count, width):
            if k0 == 0:
                raise AssertionError("depth too small: no forced one beyond width")
            best = max(best, k0 - 1)
    return best


class DiagonalAlgebra(unittest.TestCase):
    def test_recursion_holds(self):
        rng = random.Random(20260828)
        for rule in (30, 90):
            for _ in range(20):
                cells = frozenset(x for x in range(-6, 7) if rng.random() < 0.5)
                if not cells:
                    continue
                horizon = 24
                rows = rows_from(cells, horizon, rule)
                for t in range(1, horizon + 1):
                    for k in range(-12, horizon + 1):
                        d = diagonal(rows, k, t)
                        a = diagonal(rows, k, t - 1)
                        b = diagonal(rows, k - 1, t - 1)
                        c = diagonal(rows, k - 2, t - 1)
                        want = a ^ ((b | c) if rule == 30 else c)
                        self.assertEqual(d, want, (rule, k, t))

    def test_center_and_initial_indices(self):
        rng = random.Random(7)
        for _ in range(20):
            cells = frozenset(x for x in range(-6, 7) if rng.random() < 0.5)
            if not cells:
                continue
            rows = rows_from(cells, 20, 30)
            for k in range(0, 21):
                self.assertEqual(diagonal(rows, k, k), 1 if 0 in rows[k] else 0)
                self.assertEqual(diagonal(rows, -k, 0), 1 if -(-k) in rows[0] else 0)

    def test_pinned_diagonals(self):
        """PROVED corollaries: the three top diagonals are boundary-determined."""
        rng = random.Random(11)
        for _ in range(30):
            cells = frozenset(x for x in range(-6, 7) if rng.random() < 0.5)
            if not cells:
                continue
            b = max(cells)
            rows = rows_from(cells, 30, 30)
            a1 = 1 if (b - 1) in cells else 0
            a2 = 1 if (b - 2) in cells else 0
            for t in range(31):
                self.assertEqual(1 if (b + t) in rows[t] else 0, 1)
                self.assertEqual(1 if (b + t - 1) in rows[t] else 0, a1 ^ (t % 2))
                self.assertEqual(1 if (b + t - 2) in rows[t] else 0, a2 ^ (t % 2))


class Reconstruction(unittest.TestCase):
    def test_round_trip(self):
        rng = random.Random(1234)
        for rule in (30, 90):
            for _ in range(40):
                cells = frozenset(x for x in range(-7, 8) if rng.random() < 0.5)
                if not cells:
                    continue
                width = max(max(cells), 0)
                depth = 40
                right = [1 if x in cells else 0 for x in range(width + 1)]
                target = R.center_trace(cells, depth, rule)
                left = R.reconstruct(right, target, depth, rule)
                want = [1 if -k in cells else 0 for k in range(1, depth + 1)]
                self.assertEqual(left, want, (rule, sorted(cells)))

    def test_sweep_bits_matches_scalar(self):
        depth = 24
        for rule in (30, 90):
            for width in range(0, 6):
                for word in ([0, 1], [1, 0, 0], [1, 1, 0], [0, 0, 1, 1]):
                    target = R.periodic_target(word, depth)
                    count, left_bits = R.sweep_bits(width, target, depth, rule)
                    self.assertEqual(count, 1 << width)
                    for case in range(count):
                        right = R.case_right_part(case, width, target[0])
                        want = R.reconstruct(right, target, depth, rule)
                        got = [(left_bits[k] >> case) & 1 for k in range(1, depth + 1)]
                        self.assertEqual(got, want, (rule, width, word, case))

    def test_forced_row_realises_its_horizon(self):
        """The forced row's actual trace agrees with the target exactly up to k0-1."""
        depth = ORACLE_DEPTH
        width = 4
        for word in R.nonconstant_words(3):
            target = R.periodic_target(word, depth)
            count, left_bits = R.sweep_bits(width, target, depth, R.RULE30)
            firsts = R.first_forced_one(left_bits, count, width)
            for case in range(count):
                right = R.case_right_part(case, width, target[0])
                cells = {x for x in range(width + 1) if right[x]}
                cells |= {-k for k in range(1, width + 1) if (left_bits[k] >> case) & 1}
                trace = R.center_trace(frozenset(cells), depth, R.RULE30)
                h = firsts[case] - 1
                self.assertEqual(trace[: h + 1], target[: h + 1], (word, case))
                self.assertNotEqual(trace[h + 1], target[h + 1], (word, case))


class OracleTable(unittest.TestCase):
    def test_reproduces_smt_horizons(self):
        for period, row in H_TABLE.items():
            got = [measured_h(period, w) for w in range(1, 9)]
            self.assertEqual(got, row, period)

    def test_horizon_monotone_in_width(self):
        for row in H_TABLE.values():
            self.assertEqual(row, sorted(row))

    def test_period_divides_dominates(self):
        """A p-periodic trace is kp-periodic, so H(kp,w) >= H(p,w)."""
        for p in (2, 3):
            for k in (2, 3):
                if p * k not in H_TABLE:
                    continue
                for w in range(8):
                    self.assertGreaterEqual(H_TABLE[p * k][w], H_TABLE[p][w], (p, k, w))


class Rule90Control(unittest.TestCase):
    """Rule 90 has genuine finite rows with constant center; the method must find them."""

    def test_row_minus1_plus1_has_zero_center(self):
        trace = R.center_trace(frozenset({-1, 1}), 128, 90)
        self.assertEqual(trace, [0] * 129)

    def test_reconstruction_terminates(self):
        depth = 128
        target = [0] * (depth + 1)
        left = R.reconstruct([0, 1], target, depth, 90)
        self.assertEqual(left, [1] + [0] * (depth - 1))

    def test_sweep_finds_finite_left_halves(self):
        """Case 0 is the zero row; every other right part must still go silent."""
        depth = 128
        width = 4
        target = [0] * (depth + 1)
        count, left_bits = R.sweep_bits(width, target, depth, 90)
        deepest = R.deepest_forced_one(left_bits, count)
        self.assertEqual(deepest[0], 0)
        self.assertTrue(all(0 < d <= width for d in deepest[1:]), deepest)
        self.assertEqual(deepest[1], 1)

    def test_rule30_zero_target_does_not_go_silent(self):
        """PROVED zero-tail: under Rule 30 no nonzero finite row has zero center."""
        depth = 128
        for width in (1, 4, 8):
            target = [0] * (depth + 1)
            count, left_bits = R.sweep_bits(width, target, depth, 30)
            deepest = R.deepest_forced_one(left_bits, count)
            self.assertEqual(deepest[0], 0)
            self.assertTrue(all(d == depth - 1 for d in deepest[1:]), (width, deepest))
            nonzero = (1 << count) - 2
            for k in range(width + 1, depth + 1):
                self.assertEqual(left_bits[k], nonzero if k % 2 else 0, (width, k))


class Certificate(unittest.TestCase):
    def test_extremal_case_is_a_real_row(self):
        """The sweep minimum is realised by a row whose simulated trace matches."""
        depth = 256
        width = 8
        word = [0, 1, 1]
        target = R.periodic_target(word, depth)
        count, left_bits = R.sweep_bits(width, target, depth, R.RULE30)
        deepest = R.deepest_forced_one(left_bits, count)
        m = min(deepest)
        case = deepest.index(m)
        right = R.case_right_part(case, width, target[0])
        cells = {x for x in range(width + 1) if right[x]}
        cells |= {-k for k in range(1, depth + 1) if (left_bits[k] >> case) & 1}
        self.assertEqual(min(cells), -m)
        self.assertEqual(R.center_trace(frozenset(cells), depth, R.RULE30), target)


if __name__ == "__main__":
    unittest.main()
