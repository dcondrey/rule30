"""Regression gate for the incremental Psi kernel.

The kernel is a hand-derived rewrite of a two-stage ``O(L^2)`` pipeline into a
single ``O(L)`` column update.  Every number in
``RESULTS-PSI-ANCESTRY-LAW.md`` is computed with it, so the only test that
earns its place is the one pinning it to the reference implementation it
replaced.
"""

from psi_kernel import validate


def test_kernel_matches_reference() -> None:
    assert "agree with the reference" in validate(max_source=7)
