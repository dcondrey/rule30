"""Seed generator for finite-support rank-zero separator witnesses.

OpenEvolve may change only the marked function.  The evaluator treats the
returned hard-core endpoint prefix as a proposal, reconstructs its unique cut
prefix, appends an exact zero ray, and computes the terminal cone itself.
"""


# EVOLVE-BLOCK-START
def endpoint_prefix(cutoff):
    """Return ``cutoff`` endpoint symbols from {1,2}, with no adjacent 1s."""
    result = []
    for index in range(cutoff):
        if index % 2 == 0:
            result.append(1)
        else:
            result.append(2)
    return tuple(result)
# EVOLVE-BLOCK-END
