"""Falsified finite-suite P1 delay-potential conjecture.

Discovered after the 24-iteration OpenEvolve run by a deterministic census of
the same permitted expression grammar.  It passed all ten plateau edges at
widths at most 15, then failed the external width-18 plateau at offset 7:
``(22,2) -> (22,7)``.  It is retained as an overfitting control.
"""

# EVOLVE-BLOCK-START
def delay_potential(state):
    """Return the conjectured two-component plateau delay."""
    return (
        max(state["obstruction_span"], state["previous_rho_quadratic"]),
        state["pin_weight"] % 9,
    )
# EVOLVE-BLOCK-END
