"""Hankel-rank / linear-complexity measurement for A051023 (Rule 30 center column),
with a Rule 90 control and a synthetic eventually-periodic control.

Over F_2, a sequence a(0), a(1), ... is RATIONAL (its generating function A(z) = P(z)/Q(z)
for polynomials P, Q in F_2[z]) iff it satisfies a linear recurrence with constant
coefficients, iff its (infinite) Hankel matrix H[i][j] = a(i+j) has FINITE rank, iff its
"linear complexity profile" L(N) (length of the shortest LFSR reproducing a(0..N-1)) is
bounded as N -> infinity. We compute L(N) via Berlekamp-Massey over GF(2), which for a
sequence of length N runs in O(N^2) and gives, at each prefix length N, the Hankel rank of
the N x N leading principal submatrix once N is a bit past 2*L(N) (standard BM fact).

This is EXACTLY the object row 46 of PATH.md already computed under a different name:
S(0,d) := "no order-0 Ore relation of height <= d" is *identical* to "L(N) has not
saturated below d by prefix length N" -- an order-0 Ore relation P_{-1}(x) + P_0(x) F(x) = 0
with deg <= d IS a linear recurrence (LFSR) of length <= d. So computing Hankel rank here
is a reformulation, not new information, relative to
docs/rule30/overnight/RESULTS-automaticity.md's certified S(0,50), S(0,200), S(0,800)
(nullity 0, i.e. no LFSR of length <= 800 reproduces the sequence through N ~ 3400).

Run: uv run python hankel_rank.py
"""
from __future__ import annotations


def berlekamp_massey_gf2(seq: list[int]) -> list[int]:
    """Standard BM over GF(2). Returns the linear-complexity profile L(N) for
    N = 1..len(seq)."""
    n = len(seq)
    C = [1] + [0] * n
    B = [1] + [0] * n
    L = 0
    m = 1
    b = 1
    profile = []
    for N in range(n):
        # discrepancy
        d = seq[N]
        for i in range(1, L + 1):
            d ^= C[i] & seq[N - i]
        if d == 1:
            T = C[:]
            coef = 1  # over GF(2), inverse of b is 1 (b is always 1)
            for i in range(len(B)):
                if i + m < len(C):
                    C[i + m] ^= (coef * B[i]) & 1
            if 2 * L <= N:
                L = N + 1 - L
                B = T
                b = d
                m = 1
            else:
                m += 1
        else:
            m += 1
        profile.append(L)
    return profile


def rule30_center(n: int) -> list[int]:
    off = n + 2
    row = 1 << off
    out = []
    for _ in range(n):
        out.append((row >> off) & 1)
        row = (row << 1) ^ (row | (row >> 1))
    return out


def rule90_center(n: int) -> list[int]:
    off = n + 2
    row = 1 << off
    out = []
    for _ in range(n):
        out.append((row >> off) & 1)
        row = (row << 1) ^ (row >> 1)
    return out


def synthetic_periodic(n: int, period: list[int]) -> list[int]:
    return [period[i % len(period)] for i in range(n)]


def report(name: str, seq: list[int], checkpoints: list[int]) -> None:
    profile = berlekamp_massey_gf2(seq)
    print(f"-- {name} (n={len(seq)}) --")
    for cp in checkpoints:
        if cp <= len(profile):
            print(f"   L({cp}) = {profile[cp-1]}")
    # saturation check: has L(N) stopped growing over the back half?
    half = len(profile) // 2
    grew = profile[-1] - profile[half]
    print(f"   L grew by {grew} over the back half ({half}..{len(profile)}) "
          f"[0 or O(1) => looks rational at this length; grows near N/2 => not]")
    print()


def main() -> None:
    N = 2000
    checkpoints = [50, 100, 200, 500, 1000, 2000]

    r30 = rule30_center(N)
    assert "".join(map(str, r30[:16])) == "1101110011000101", "A051023 ground-truth mismatch"
    report("Rule 30 center (A051023)", r30, checkpoints)

    r90 = rule90_center(N)
    print(f"Rule 90 center first 16 bits: {''.join(map(str, r90[:16]))}")
    print(f"Rule 90 center is identically zero after t=0: {all(b == 0 for b in r90[1:])}")
    report("Rule 90 center", r90, checkpoints)

    # eventually-periodic control with a nontrivial preperiod+period, comparable data volume
    ctrl = synthetic_periodic(N, [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1])
    report("synthetic eventually-periodic control (period 11)", ctrl, checkpoints)

    # a "hard" control: also feed BM a high-complexity pseudo-random sequence for scale
    import random
    random.seed(0)
    rnd = [random.randint(0, 1) for _ in range(N)]
    report("random control (expect L(N) ~ N/2)", rnd, checkpoints)


if __name__ == "__main__":
    main()
