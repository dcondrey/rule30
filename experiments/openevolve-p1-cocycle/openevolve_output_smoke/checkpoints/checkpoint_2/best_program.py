"""Seed delay potential for the exact Rule 30 P1 cocycle.

OpenEvolve may change only the marked function.  The evaluator combines its
output with the already-proved nonincreasing principal rank.  On a transition
where rank is unchanged, this secondary tuple must strictly decrease.
"""

# EVOLVE-BLOCK-START
def delay_potential(state):
    """Return a nonnegative integer tuple derived from exact state features."""
    return (state["factor_terms"],)
# EVOLVE-BLOCK-END
