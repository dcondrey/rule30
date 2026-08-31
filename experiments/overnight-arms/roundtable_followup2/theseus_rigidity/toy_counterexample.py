"""General fact-check, outside Rule 30: can a coarse projection of a sequence
be eventually periodic while a finer refinement of the same sequence is not?

Trivial counterexample: state_t = t (an ever-increasing counter, never
repeats -> not eventually periodic under any equivalence coarser than
equality). Output bit_t = state_t mod 2 -> strictly periodic with period 2.

This settles the *general* question the spark's kill condition raises:
there is NO generic theorem that a finer invariant must inherit periodicity
from a coarser one it refines. Any such claim for a specific system (Rule 30)
must come from a special property of THAT system's transition structure
(a genuine composition/rigidity law), not from refinement alone.
"""


def counter_automaton(steps: int):
    state = []
    bits = []
    for t in range(steps):
        state.append(t)          # finer invariant: strictly increasing, never periodic
        bits.append(t % 2)       # coarse projection: exactly periodic, period 2
    return state, bits


def is_eventually_periodic(seq, max_period=50, tail=200):
    """Cheap finite check: does seq have a period <= max_period over its last `tail` entries?"""
    n = len(seq)
    if n < tail:
        tail = n
    window = seq[-tail:]
    for p in range(1, max_period + 1):
        if all(window[i] == window[i - p] for i in range(p, len(window))):
            return p
    return None


if __name__ == "__main__":
    state, bits = counter_automaton(2000)
    p_bits = is_eventually_periodic(bits)
    p_state = is_eventually_periodic(state, max_period=100)
    print(f"coarse bit sequence: eventually periodic, period = {p_bits}")
    print(f"fine state sequence: eventually periodic, period = {p_state}  (expect None)")
    assert p_bits == 2
    assert p_state is None
    print()
    print("CONCLUSION: coarse periodicity does NOT force fine periodicity in")
    print("general. The spark's rigidity claim is therefore not a free lunch")
    print("from 'type refines bit' -- it needs an actual argument specific to")
    print("Rule 30's transition law, exactly the missing-composition-law gap")
    print("(PATH.md 7.3 obstruction D).")
