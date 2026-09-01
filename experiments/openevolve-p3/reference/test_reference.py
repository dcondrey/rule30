"""Cross-validate bigint_reference against simple_reference (the ground-truth
authority) and pin known Rule 30 center-column values."""
from simple_reference import center_column as simple_center_column
from bigint_reference import center_column as bigint_center_column

# Rule 30 center column, c(0)..c(20), single 1-cell seed; c(0)=1 is the seed
# cell itself. c(0),c(1),c(2) = 1,1,0 verified by hand from the update rule
# (new(i) = old(i-1) XOR (old(i) OR old(i+1))) before pinning; the rest is
# taken from simple_reference.py's output, cross-checked against
# bigint_reference.py below. (Do not trust a "well-known sequence" pulled
# from memory here -- an earlier draft of this file had it wrong at index 2;
# these two independent, from-the-definition implementations are the
# authority, not recollection.)
KNOWN_PREFIX = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]


def test_simple_matches_known_prefix():
    got = simple_center_column(20)
    assert got == KNOWN_PREFIX, got


def test_bigint_matches_known_prefix():
    got = bigint_center_column(20)
    assert got == KNOWN_PREFIX, got


def test_bigint_matches_simple_over_range():
    n_max = 500
    simple = simple_center_column(n_max)
    fast = bigint_center_column(n_max)
    assert simple == fast


def test_bigint_matches_simple_odd_sizes():
    # Off-by-one bugs in bit conventions tend to show up at odd/even boundary
    # widths -- check several small n individually, not just one long run.
    for n in [0, 1, 2, 3, 4, 5, 7, 13, 31, 63, 100, 127, 200, 333]:
        s = simple_center_column(n)[-1]
        b = bigint_center_column(n)[-1]
        assert s == b, f"mismatch at n={n}: simple={s} bigint={b}"
