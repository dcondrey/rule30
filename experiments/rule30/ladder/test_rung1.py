"""Regression tests for R7 rung 1: the boundary extendability condition."""

import itertools
import random

from ladder import FWD, Params, simulate
from rung1 import decide_pin, pin_identity_check, pin_ok


def _extendable(a_seq, b_seq, rule):
    """Brute force: does some col_{R+1} satisfy the forward rule at x=R?

    a_seq = col_{R-1}(t), b_seq = col_R(t).  The rule at x=R reads
    b(t+1) = fwd(a(t), b(t), c(t)) with c = col_{R+1} free per time step,
    so extendability is a per-t existence question.
    """
    fwd = FWD[rule]
    for t in range(len(b_seq) - 1):
        if not any(fwd(a_seq[t], b_seq[t], c) == b_seq[t + 1] for c in (0, 1)):
            return False
    return True


def test_pin_is_exactly_extendability_rule30():
    """The pin holds on every consecutive pair iff the strip extends."""
    rng = random.Random(0)
    for _ in range(400):
        n = rng.randint(2, 12)
        letters = [rng.randrange(4) for _ in range(n)]
        a = [l >> 1 for l in letters]
        b = [l & 1 for l in letters]
        by_pin = all(pin_ok(letters[i], letters[i + 1], 30)
                     for i in range(n - 1))
        assert by_pin == _extendable(a, b, 30), (letters, by_pin)


def test_pin_exhaustive_short_words_rule30():
    for n in (2, 3, 4):
        for letters in itertools.product(range(4), repeat=n):
            a = [l >> 1 for l in letters]
            b = [l & 1 for l in letters]
            by_pin = all(pin_ok(letters[i], letters[i + 1], 30)
                         for i in range(n - 1))
            assert by_pin == _extendable(a, b, 30), letters


def test_rule90_extendability_is_vacuous():
    """Rule 90 always extends, so its boundary condition imposes nothing."""
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(2, 12)
        letters = [rng.randrange(4) for _ in range(n)]
        a = [l >> 1 for l in letters]
        b = [l & 1 for l in letters]
        assert _extendable(a, b, 90)
        assert all(pin_ok(letters[i], letters[i + 1], 90)
                   for i in range(n - 1))


def test_pin_identity_holds_on_true_diagram():
    ante30, bad30 = pin_identity_check(30, T=200)
    assert ante30 > 0 and bad30 == 0
    ante90, bad90 = pin_identity_check(90, T=200)
    assert ante90 > 0 and bad90 == ante90


def test_true_lone_seed_word_satisfies_pin():
    """The real rule-30 letter word must never be rejected by the pin."""
    grid, B = simulate(30, 300)
    for R in (1, 2, 3, 5):
        letters = [(grid[t][B + R - 1] << 1) | grid[t][B + R]
                   for t in range(300)]
        assert all(pin_ok(letters[i], letters[i + 1], 30)
                   for i in range(len(letters) - 1)), R


def test_calibration_A_still_empty_with_pin():
    for word in ((1,), (0,)):
        P = Params(rule=30, right_depth=2, left_depth=2,
                   period_word=word, diff_q=1)
        assert decide_pin(P, True)["verdict"] == "EMPTY", word


def test_calibration_B_rule90_control_survives_pin():
    for R in (1, 2, 3):
        P = Params(rule=90, right_depth=R, left_depth=2,
                   period_word=(0,), diff_q=1)
        assert decide_pin(P, True)["verdict"] == "NONEMPTY", R


def test_pin_never_flips_a_nonempty_verdict_p2():
    for R in (1, 2, 3):
        P = Params(rule=30, right_depth=R, left_depth=2,
                   period_word=(0, 1), diff_q=1)
        assert decide_pin(P, False)["verdict"] == "NONEMPTY"
        assert decide_pin(P, True)["verdict"] == "NONEMPTY"
