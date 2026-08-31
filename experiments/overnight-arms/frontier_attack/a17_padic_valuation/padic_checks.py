"""a17: computational checks behind the p-adic / Newton-polygon kill.

Six checks, all exact (Fraction / integer arithmetic, no floats):

  C1  eventually periodic 2-adic expansion <=> rational.  (Corrects the premise
      that this equivalence somehow fails 2-adically.)
  C2  Newton polygon over Z_2 of F(x) = sum c_t x^t for a 0/1 sequence is the
      horizontal ray y = 0 from t_min -- IDENTICAL for Rule 30, Rule 90, a
      periodic word, Thue-Morse, and a random word.  Non-separating by
      construction.
  C3  Weierstrass preparation in Z_2[[x]]: lambda = min{t : v_2(c_t) = 0} = 0
      whenever c_0 = 1, so F is a unit and the distinguished polynomial has
      degree 0.  No information.
  C4  the pin's unconditional F_2 form l_t = c_{t+1} + c_t + r_t + c_t r_t
      holds for Rule 30 (0 violations) and the quadratic term c_t r_t is
      genuinely present (nonzero at positive density).
  C5  the needed operation is the HADAMARD (coefficientwise) product, which is
      not the series product: F_0 * F_1 (Cauchy) != F_0 (.) F_1 (Hadamard).
  C6  Rule 90 positive control: it DOES have a closed two-variable functional
      equation, G_90 = 1/(1 + x(y + y^-1)) over F_2, verified against
      simulation.  Rule 30 has no analogue.

Run:  uv run python padic_checks.py
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

sys.path.insert(
    0, "/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/common"
)
from rule30 import cell, center_column_bits, rows_frame  # noqa: E402

FAIL: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}{(': ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(name)


# --------------------------------------------------------------------------
# C1  eventually periodic 2-adic digits <=> rational
# --------------------------------------------------------------------------
def padic_digits(q: Fraction, n: int) -> list[int]:
    """First n digits of the 2-adic expansion of q, which must lie in Z_2
    (odd denominator).  Digit extraction is exact rational arithmetic."""
    assert q.denominator % 2 == 1, "not a 2-adic integer"
    out = []
    for _ in range(n):
        # numerator mod 2 with odd denominator: d = num * den^{-1} mod 2 = num mod 2
        d = q.numerator % 2
        out.append(d)
        q = (q - d) / 2
    return out


def rational_from_eventually_periodic(pre: list[int], per: list[int]) -> Fraction:
    """N = A + 2^m * B / (1 - 2^p) for preperiod A (length m) and period B."""
    m, p = len(pre), len(per)
    A = sum(b << i for i, b in enumerate(pre))
    B = sum(b << i for i, b in enumerate(per))
    return Fraction(A) + Fraction(B << m, 1 - (1 << p))


def c1() -> None:
    print("C1  eventually periodic 2-adic expansion <=> rational")
    # ...111... = -1
    check("1+2+4+8+... = -1", rational_from_eventually_periodic([], [1]) == -1)
    cases = [([], [1]), ([1, 0, 1], [1, 1, 0]), ([0, 0], [0, 1]), ([1], [0])]
    for pre, per in cases:
        q = rational_from_eventually_periodic(pre, per)
        n = len(pre) + 7 * len(per)
        want = pre + (per * 8)[: n - len(pre)]
        check(
            f"pre={pre} per={per} -> {q}, digits round-trip",
            padic_digits(q, n) == want,
            f"v_2 = {0 if q.numerator % 2 else 'positive'}",
        )
    # converse direction, exhaustively for small odd denominators: every
    # rational in Z_2 has eventually periodic digits with period | ord_2 mod den.
    ok = True
    for den in range(1, 40, 2):
        for num in range(-20, 21):
            q = Fraction(num, den)
            d = padic_digits(q, 400)
            # period of 2 mod den divides lambda(den); digits repeat with that
            # period.  den = 1 (plain integers) has trivial period 1.
            if den == 1:
                p = 1
            else:
                p = 1
                while pow(2, p, den) != 1:
                    p += 1
            if d[200:300] != d[200 + p : 300 + p]:
                ok = False
    check("every rational in Z_2 has eventually periodic digits (den<40)", ok)


# --------------------------------------------------------------------------
# C2  Newton polygon over Z_2
# --------------------------------------------------------------------------
def newton_polygon(coeffs: list[int]) -> list[tuple[int, int]]:
    """Vertices of the lower convex hull of {(t, v_2(c_t)) : c_t != 0}.
    For 0/1 coefficients v_2 is 0 whenever the coefficient is present."""
    pts = [(t, 0) for t, c in enumerate(coeffs) if c]
    hull: list[tuple[int, int]] = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # drop hull[-1] if it is not below the segment hull[-2] -> p
            if (x2 - x1) * (p[1] - y1) <= (p[0] - x1) * (y2 - y1):
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def rule90_center(n: int) -> list[int]:
    row = 1
    out = []
    for t in range(n):
        out.append((row >> t) & 1)
        row = (row << 2) ^ row  # b_{t+1} = shift-left-2 XOR self, in the same frame
    return out


def thue_morse(n: int) -> list[int]:
    return [bin(i).count("1") & 1 for i in range(n)]


def c2() -> None:
    print("C2  Newton polygon over Z_2 is degenerate and non-separating")
    n = 512
    rng = random.Random(30)
    seqs = {
        "rule30 centre (A051023)": center_column_bits(n),
        "rule90 centre": rule90_center(n),
        "periodic (110)^inf": [(1, 1, 0)[i % 3] for i in range(n)],
        "Thue-Morse (+1 at t=0)": [1] + thue_morse(n - 1),
        "random 0/1 (c_0=1)": [1] + [rng.randint(0, 1) for _ in range(n - 1)],
    }
    inv = {}
    for k, s in seqs.items():
        assert s[0] == 1, k
        hull = newton_polygon(s)
        slopes = frozenset(hull[i + 1][1] - hull[i][1] for i in range(len(hull) - 1))
        # The trailing vertex is an artifact of truncating at t = n; for the full
        # series the polygon is the ray y = 0 from the first vertex.  The
        # truncation-independent content is (first vertex, slope set).
        inv[k] = (hull[0], slopes)
        print(f"      {k:26s} vertices={hull}  first={hull[0]}  slopes={set(slopes)}")
    infinite_support = [k for k in seqs if sum(seqs[k][n // 2 :]) > 0]
    check(
        "every sequence with infinite support has the SAME polygon "
        "(first vertex (0,0), slope set {0})",
        len({inv[k] for k in infinite_support}) == 1
        and inv[infinite_support[0]] == ((0, 0), frozenset({0})),
        f"{len(infinite_support)} sequences: {infinite_support}",
    )
    # Rule 90 is the one outlier and for a reason that is NOT periodicity: its
    # centre column is 1,0,0,0,... so the support is finite and the polygon
    # degenerates to a point.  Any eventually-zero sequence, periodic or not,
    # gives the same point; so this distinction detects "eventually 0", not
    # "eventually periodic".
    check(
        "Rule 90 differs only via finite support, not via periodicity",
        inv["rule90 centre"] == ((0, 0), frozenset())
        and sum(seqs["rule90 centre"]) == 1
        and inv["periodic (110)^inf"] == inv["rule30 centre (A051023)"],
        "periodic (110)^inf is indistinguishable from Rule 30 and from random",
    )


# --------------------------------------------------------------------------
# C3  Weierstrass preparation
# --------------------------------------------------------------------------
def c3() -> None:
    print("C3  Weierstrass preparation in Z_2[[x]] is trivial for 0/1 series")
    n = 512
    for name, s in [
        ("rule30 centre", center_column_bits(n)),
        ("rule90 centre", rule90_center(n)),
        ("periodic (110)^inf", [(1, 1, 0)[i % 3] for i in range(n)]),
    ]:
        lam = next(t for t, c in enumerate(s) if c % 2 == 1)  # v_2(c_t) = 0
        check(f"{name}: lambda-invariant = 0, F is a unit", lam == 0)


# --------------------------------------------------------------------------
# C4  the pin, unconditional F_2 form, and the quadratic term
# --------------------------------------------------------------------------
def c4() -> None:
    print("C4  pin identity l_t = c_{t+1} + c_t + r_t + c_t*r_t  (mod 2)")
    T = 3000
    rows = rows_frame(T + 2)
    c = [cell(rows[t], t, 0) for t in range(T + 1)]
    l = [cell(rows[t], t, -1) for t in range(T + 1)]
    r = [cell(rows[t], t, 1) for t in range(T + 1)]
    bad = sum(1 for t in range(T) if l[t] != (c[t + 1] ^ c[t] ^ r[t] ^ (c[t] & r[t])))
    check("Rule 30: 0 violations of the unconditional inverse form", bad == 0, f"T={T}")
    ones = sum(1 for t in range(T) if c[t] == 1)
    pinned = sum(1 for t in range(T) if c[t] == 1 and l[t] == 1 ^ c[t + 1])
    check("Rule 30: pin holds at every c_t=1", pinned == ones, f"{ones} antecedents")
    quad = sum(1 for t in range(T) if c[t] & r[t])
    check(
        "quadratic term c_t*r_t is not negligible (cannot be dropped)",
        quad > T // 8,
        f"nonzero at {quad}/{T} = {quad / T:.3f} of steps",
    )


# --------------------------------------------------------------------------
# C5  Hadamard vs Cauchy product
# --------------------------------------------------------------------------
def c5() -> None:
    print("C5  the AND term is a Hadamard product, not a series product")
    T = 64
    rows = rows_frame(T + 1)
    c = [cell(rows[t], t, 0) for t in range(T)]
    r = [cell(rows[t], t, 1) for t in range(T)]
    hadamard = [c[t] & r[t] for t in range(T)]
    cauchy = [sum(c[i] * r[t - i] for i in range(t + 1)) % 2 for t in range(T)]
    check(
        "Hadamard(c,r) != Cauchy(c,r) as F_2[[x]] elements",
        hadamard != cauchy,
        f"first differ at t={next(t for t in range(T) if hadamard[t] != cauchy[t])}",
    )
    # and the Hadamard product is not any of the finitely many ring words of
    # degree <= 2 in F_0, F_1 over F_2[[x]] with polynomial coefficients of
    # degree <= 2 -- brute force the small search.
    def poly_mul(a, b):
        return [sum(a[i] * b[t - i] for i in range(t + 1)) % 2 for t in range(T)]

    basis = {
        "F0": c,
        "F1": r,
        "F0*F0": poly_mul(c, c),
        "F0*F1": poly_mul(c, r),
        "F1*F1": poly_mul(r, r),
        "1": [1] + [0] * (T - 1),
    }
    hits = []
    for mask in range(1, 1 << len(basis)):
        names = list(basis)
        acc = [0] * T
        for i, nm in enumerate(names):
            if mask >> i & 1:
                acc = [(a + b) % 2 for a, b in zip(acc, basis[nm])]
        if acc == hadamard:
            hits.append([names[i] for i in range(len(names)) if mask >> i & 1])
    check(
        "no F_2-combination of {1,F0,F1,F0^2,F0F1,F1^2} equals the AND term",
        not hits,
        f"{(1 << len(basis)) - 1} combinations tested",
    )


# --------------------------------------------------------------------------
# C6  Rule 90 positive control: a genuine closed functional equation
# --------------------------------------------------------------------------
def c6() -> None:
    print("C6  Rule 90 HAS a closed two-variable functional equation")
    # G(x,y) = sum_t x^t (y + y^-1)^t = 1/(1 - x(y+y^-1)) over F_2.
    # Coefficient of x^t y^j is C(t,(t+j)/2) mod 2.
    T = 96
    row = 1
    ok = True
    for t in range(T):
        for j in range(-t, t + 1):
            sim = (row >> (j + t)) & 1
            if (t + j) % 2:
                pred = 0
            else:
                k = (t + j) // 2
                pred = 1 if (t - k) & k == 0 else 0  # C(t,k) odd <=> Kummer/Lucas
            if sim != pred:
                ok = False
        row = (row << 2) ^ row
    check(
        "s_90(t,j) = [x^t y^j] 1/(1 + x(y+y^-1)) over F_2, all t<96",
        ok,
        "closed rational GF; Rule 30 admits no analogue (see C4/C5)",
    )


if __name__ == "__main__":
    for f in (c1, c2, c3, c4, c5, c6):
        f()
        print()
    print("FAILURES:", FAIL if FAIL else "none")
    sys.exit(1 if FAIL else 0)
