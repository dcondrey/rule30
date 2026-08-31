"""Does the pair-correlation observable K_t(x) = sum_i u_{t,i} u_{t,i+1} x^i close
under the Rule 30 local map, or does its time-t+1 value require triple-point data
(u_{t,i-1} u_{t,i} u_{t,i+1}) that K_t alone (a pairwise object) does not carry?

This is the concrete version of the panel's claim that "the local rule ... lifts to
a quadratic relation Q(G)=0" in G alone. We check, by brute-force truth table over
all 2^5 = 32 windows (a_{i-2..i+2}), whether the bit

    K_{t+1,i} := u_{t+1,i} * u_{t+1,i+1}

is a function of pairwise products of a = u_t alone (degree <= 2 in the a's), or
whether its ANF (algebraic normal form over F_2) contains a genuine degree-3 (or
higher) monomial -- which would mean the "pair" observable's evolution needs
triple-point information not present in K_t itself, i.e. the hierarchy does not
close at the pair level (the BBGKY / Gutowitz local-structure-theory obstruction).

Run: uv run python hierarchy_check.py
"""
from __future__ import annotations
from itertools import product


def rule30_bit(am1: int, a0: int, a1: int) -> int:
    # u_{t+1,i} = a_{i-1} + a_i + a_{i+1} + a_i*a_{i+1}  (matches OR form a_i|a_{i+1} XOR a_{i-1})
    return am1 ^ a0 ^ a1 ^ (a0 & a1)


def anf_degree_and_monomials(f_table: dict[tuple[int, ...], int], nvars: int) -> list[tuple[int, ...]]:
    """Mobius/Zhegalkin transform: returns list of monomials (as tuples of variable indices
    present, sorted) with nonzero ANF coefficient."""
    n = nvars
    size = 1 << n
    f = [0] * size
    for bits, val in f_table.items():
        idx = 0
        for k, b in enumerate(bits):
            if b:
                idx |= 1 << k
        f[idx] = val
    # in-place Mobius transform (superset sum) over F_2
    coeff = f[:]
    for i in range(n):
        bit = 1 << i
        for mask in range(size):
            if mask & bit:
                coeff[mask] ^= coeff[mask ^ bit]
    monomials = []
    for mask in range(size):
        if coeff[mask]:
            vars_in = tuple(k for k in range(n) if mask & (1 << k))
            monomials.append(vars_in)
    return monomials


def main() -> None:
    # variables a_{-2}, a_{-1}, a_0, a_1, a_2  (indices 0..4), representing a window
    # of u_t centered so that we can compute u_{t+1,i} for i in {-1,0,1} and then
    # K_{t+1,-1} = u_{t+1,-1}*u_{t+1,0} depends on a_{-2..1}; we look at
    # K_{t+1,0} = u_{t+1,0}*u_{t+1,1}, which depends on a_{-1,0,1,2} (4 vars, indices 1..4).
    names = ["a_-2", "a_-1", "a_0", "a_1", "a_2"]
    table = {}
    for bits in product((0, 1), repeat=5):
        am2, am1, a0, a1, a2 = bits
        u_i0 = rule30_bit(am1, a0, a1)     # u_{t+1,0}
        u_i1 = rule30_bit(a0, a1, a2)      # u_{t+1,1}
        table[bits] = u_i0 & u_i1

    monomials = anf_degree_and_monomials(table, 5)
    deg = max((len(m) for m in monomials), default=0)
    print("K_{t+1,0} = u_{t+1,0}*u_{t+1,1} as ANF over a_-2,a_-1,a_0,a_1,a_2:")
    for m in monomials:
        term = "*".join(names[k] for k in m) if m else "1"
        print("  +", term)
    print(f"ANF degree = {deg}")
    print()

    # Does K_{t+1,0} depend only on a_-1 through a_2 (i.e. is a_-2 actually needed)?
    depends_on_am2 = any(0 in m for m in monomials)
    print(f"depends on a_-2: {depends_on_am2}")

    # Restrict to the pairwise-closure question: can K_{t+1,0} be written using only
    # K_t-type pair products (a_i*a_{i+1}) and single bits a_i, i.e. is every monomial
    # of degree <= 2, OR degree-3 monomials that happen to equal a consecutive pair
    # (which would already be "known" from K_t)? Report the actual degree-3 monomials.
    deg3 = [m for m in monomials if len(m) == 3]
    deg4 = [m for m in monomials if len(m) == 4]
    print(f"degree-3 monomials: {[tuple(names[k] for k in m) for m in deg3]}")
    print(f"degree-4 monomials: {[tuple(names[k] for k in m) for m in deg4]}")
    print()
    if deg >= 3:
        print("VERDICT: K_{t+1,i} genuinely requires order-3 (triple-point) correlation")
        print("data of u_t that is NOT contained in K_t = {pairwise products of u_t} alone.")
        print("The pair-correlation observable does not close under one Rule-30 step;")
        print("closing it requires the triple-point observable, whose own evolution will")
        print("in turn require quadruple-point data, etc. (Gutowitz/BBGKY-style hierarchy).")
    else:
        print("VERDICT: closes at pair level (unexpected -- re-derive).")


if __name__ == "__main__":
    main()
