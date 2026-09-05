#!/usr/bin/env python3
"""Proof of the letter-space balance  #{q in {0,2,x}^m : Phi(q) = 0} = (3^m + 1)/2.

Let A be the 4x4 integer matrix on Moore states (h, F) summing the three
letter permutations (odd: h->h+1; two: h->h+1, F->F+h; zero: F->F+h).  The
number of letter words of length m with forced start (final h = 1) and
Phi = F_final = eps is  N_eps(m) = sum_{h0} (A^m)[(h0,0),(1,eps)], and
d(m) = N_0(m) - N_1(m).  d satisfies the linear recurrence given by the
characteristic polynomial p of A (Cayley-Hamilton).  If p(1) = 0 the constant
sequence 1 satisfies that recurrence, so d(m) = 1 for all m follows from
d(1) = d(2) = d(3) = d(4) = 1.  Then N_0 + N_1 = 3^m gives the claim.

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_balance_proof.py
"""
from __future__ import annotations

from fractions import Fraction

STATES = [(0, 0), (0, 1), (1, 0), (1, 1)]
LETTERS = [(0, 0), (0, 1), (1, 1)]


def step(state, letter):
    h, F = state
    a, b = letter
    return (h ^ 1 ^ a, F ^ (h & b))


def matmul(X, Y):
    n = len(X)
    return [[sum(X[i][k] * Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def charpoly(M):
    """Faddeev-LeVerrier: coefficients c_n..c_0 of det(xI - M)."""
    n = len(M)
    I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    Mf = [[Fraction(x) for x in row] for row in M]
    coeffs = [Fraction(1)]
    N = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        N = matmul(Mf, [[N[i][j] + coeffs[-1] * I[i][j] for j in range(n)] for i in range(n)])
        c = -sum(N[i][i] for i in range(n)) / k
        coeffs.append(c)
    return coeffs  # p(x) = sum coeffs[i] x^(n-i)


def main() -> None:
    A = [[0] * 4 for _ in range(4)]
    for i, s in enumerate(STATES):
        for L in LETTERS:
            A[i][STATES.index(step(s, L))] += 1
    print("A (rows from-state, cols to-state, states (h,F) =", STATES, "):")
    for row in A:
        print("   ", row)
    p = charpoly(A)
    print("characteristic polynomial coefficients (x^4 .. x^0):", [str(c) for c in p])
    p1 = sum(p[i] for i in range(5))
    print("p(1) =", p1, "  -> constant sequences satisfy the recurrence:", p1 == 0)
    # d(m) for m = 1..8 by direct powers
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    ds = []
    for m in range(1, 9):
        P = matmul(P, A)
        N0 = sum(P[STATES.index((h0, 0))][STATES.index((1, 0))] for h0 in (0, 1))
        N1 = sum(P[STATES.index((h0, 0))][STATES.index((1, 1))] for h0 in (0, 1))
        ds.append(N0 - N1)
        assert N0 + N1 == 3 ** m
    print("d(m) = N_0(m) - N_1(m) for m = 1..8:", ds)
    ok = p1 == 0 and ds[:4] == [1, 1, 1, 1]
    print("PROOF COMPLETE (p(1)=0 and d(1..4)=1):", ok)


if __name__ == "__main__":
    main()
