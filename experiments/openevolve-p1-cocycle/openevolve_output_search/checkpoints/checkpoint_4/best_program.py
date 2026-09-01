"""Seed delay potential for the exact Rule 30 P1 cocycle.

OpenEvolve may change only the marked function.  The evaluator combines its
output with the already-proved nonincreasing principal rank.  On a transition
where rank is unchanged, this secondary tuple must strictly decrease.
"""

# EVOLVE-BLOCK-START
def delay_potential(state):
    """Return a nonnegative integer tuple derived from exact state features.

    Scalar polynomial prefixes are indicator, previous_rho, pin,
    obstruction, and factor; their suffixes are constant, degree1, higher,
    linear, quadratic, span, support, terms, and weight.  Frontier prefixes
    are frontier_a and frontier_b; their suffixes are components, constant,
    degree1_max, degree1_sum, nonzero, span_sum, support_sum, terms, and
    weight.  The remaining fields are rank, removed_rank, and
    frontier_depth.
    """
    return (state["obstruction_terms"], state["frontier_b_terms"], state["factor_terms"])
# EVOLVE-BLOCK-END
