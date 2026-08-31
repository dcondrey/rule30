"""a21 step 1: the exact GF(2) defect equation, and the leftward closing cascade.

Two objects, both verified exhaustively before anything is built on them.

(A) THE DEFECT PDE.  For any two rule-30 diagrams s, s' put D = s XOR s'.  Then

      D(t+1,x) = D(t,x-1) XOR D(t,x) XOR D(t,x+1)
                 XOR D(t,x)*s(t,x+1) XOR D(t,x+1)*s(t,x)
                 XOR D(t,x)*D(t,x+1)                              (rule 30)

      D(t+1,x) = D(t,x-1) XOR D(t,x+1)                            (rule 90)

    Rule 90's defect equation does not see the underlying orbit at all; rule
    30's is quadratic and coupled to it.  That coupling IS the OR nonlinearity.

(B) THE CLOSING CASCADE.  If D(t,0)=0 and D(t,-1)=0 for all t >= t1 then
    D(t,-k) = D(t+k-1,-1) = 0 for every k >= 1 and t >= t1, so the whole left
    quarter-plane vanishes -- contradicting the speed-1 left edge, which forces
    D(t, L0-t-p) = 1.  This is the standard closing step (Jen 1990 Prop. 3 /
    Kopra Thm 3.5) re-derived from the PDE, and it is VALIDATION, not new.

Usage: uv run python defect_pde.py > defect_pde_output.txt
"""

from __future__ import annotations

import itertools
import random

from substrate import COMMON, cell, diagram, left_supported_row, step


def local(a: int, b: int, c: int, rule: int) -> int:
    """s(t+1,x) from (s(t,x-1), s(t,x), s(t,x+1))."""
    return (a ^ (b | c)) if rule == 30 else (a ^ c)


def pde_rhs(dl: int, dc: int, dr: int, sc: int, sr: int, rule: int) -> int:
    if rule == 30:
        return dl ^ dc ^ dr ^ (dc & sr) ^ (dr & sc) ^ (dc & dr)
    return dl ^ dr


def check_pde_exhaustive() -> None:
    """All 2^6 combinations of (s(t,x-1),s(t,x),s(t,x+1)) and defect triple."""
    for rule in (30, 90):
        n = 0
        for sl, sc, sr, dl, dc, dr in itertools.product((0, 1), repeat=6):
            lhs = local(sl, sc, sr, rule) ^ local(sl ^ dl, sc ^ dc, sr ^ dr, rule)
            rhs = pde_rhs(dl, dc, dr, sc, sr, rule)
            assert lhs == rhs, (rule, sl, sc, sr, dl, dc, dr, lhs, rhs)
            n += 1
        print(f"(A) rule {rule}: defect PDE exact on all {n} local states")


def check_pde_on_orbits(trials: int = 200, T: int = 60) -> None:
    """The PDE on genuine pairs of diagrams: the stroboscopic pair (t, t+p) of
    one finite orbit, which is the pairing R1 needs."""
    rng = random.Random(4242)
    for rule in (30, 90):
        checks = 0
        for _ in range(trials):
            w = rng.randint(1, 10)
            bits = [rng.randint(0, 1) for _ in range(w)]
            bits[0] = 1
            p = rng.randint(1, 6)
            K = w + T + p + 4
            rows = diagram(left_supported_row(bits, K), K, T + p + 2, rule)

            def D(t: int, x: int) -> int:
                return cell(rows[t + p], t + p, x, K) ^ cell(rows[t], t, x, K)

            for t in range(T):
                for x in range(-(t + p + w + 2), t + p + 3):
                    lhs = D(t + 1, x)
                    rhs = pde_rhs(
                        D(t, x - 1),
                        D(t, x),
                        D(t, x + 1),
                        cell(rows[t], t, x, K),
                        cell(rows[t], t, x + 1, K),
                        rule,
                    )
                    assert lhs == rhs, (rule, bits, p, t, x)
                    checks += 1
        print(f"(A) rule {rule}: defect PDE exact on {checks} stroboscopic cells")


def check_zeroset_simplification() -> None:
    """PATH.md section 2, restated and re-checked because the brief asked for it.

    c_t = 0  =>  c_{t+1} = l_t XOR r_t          (already in PATH.md 146-148)
    c_t = 1  =>  c_{t+1} = NOT l_t              (the pin)
    and the induced defect identity D(t,-1) = (1 XOR c_t) AND D(t,1)
    under the hypothesis D(.,0) == 0.
    """
    n = 3000
    K = 4
    rows = diagram(left_supported_row([1], K), K, n + 8, 30)
    a = b = 0
    for t in range(n):
        c = cell(rows[t], t, 0, K)
        l = cell(rows[t], t, -1, K)
        r = cell(rows[t], t, 1, K)
        c1 = cell(rows[t + 1], t + 1, 0, K)
        if c == 0:
            assert c1 == (l ^ r)
            a += 1
        else:
            assert c1 == (1 ^ l)
            b += 1
    print(
        f"(A) zero-set split verified on the lone seed: {a} zero-phase, "
        f"{b} one-phase steps, 0 violations  [KNOWN: PATH.md section 2]"
    )

    # The induced defect identity, on every stroboscopic pair with a centre
    # agreement at t (a bounded shadow, not the hypothesis).
    rng = random.Random(7)
    viol = tot = 0
    for _ in range(60):
        p = rng.randint(1, 40)
        for t in range(1, 400):
            c = cell(rows[t], t, 0, K)
            if c != cell(rows[t + p], t + p, 0, K):
                continue
            if cell(rows[t + 1], t + 1, 0, K) != cell(
                rows[t + p + 1], t + p + 1, 0, K
            ):
                continue
            d1 = cell(rows[t], t, 1, K) ^ cell(rows[t + p], t + p, 1, K)
            dm1 = cell(rows[t], t, -1, K) ^ cell(rows[t + p], t + p, -1, K)
            tot += 1
            viol += dm1 != ((1 ^ c) & d1)
    print(f"(A) D(t,-1) = (1 XOR c_t) AND D(t,1): {tot} checks, {viol} violations")


def check_left_edge_and_cascade() -> None:
    """(B) the two ingredients of the closing step."""
    rng = random.Random(11)
    for rule in (30, 90):
        bad = 0
        for _ in range(300):
            w = rng.randint(1, 10)
            bits = [rng.randint(0, 1) for _ in range(w)]
            bits[0] = 1
            K = w + 90
            rows = diagram(left_supported_row(bits, K), K, 80, rule)
            lo0 = -max(j for j in range(w) if bits[j])  # leftmost 1 at t=0
            for t in range(80):
                xs = [x for x in range(-K, K) if cell(rows[t], t, x, K)]
                bad += min(xs) != lo0 - t
        print(f"(B) rule {rule}: leftmost 1 at L0 - t exactly; {bad} deviations")

    # The cascade identity itself, as a statement about the PDE: if D(t,x)=0 and
    # D(t,x+1)=0 then D(t+1,x) = D(t,x-1); read backwards, D(t,x-1) = D(t+1,x).
    n = 0
    for sl, sc, sr, dl in itertools.product((0, 1), repeat=4):
        assert pde_rhs(dl, 0, 0, sc, sr, 30) == dl
        assert pde_rhs(dl, 0, 0, sc, sr, 90) == dl
        n += 1
    print(f"(B) D(t,x)=D(t,x+1)=0  =>  D(t+1,x)=D(t,x-1): exact, {n} states, both rules")


def main() -> None:
    print("a21 / defect_pde.py -- exact GF(2) defect equation and closing cascade")
    print(f"substrate cross-check: common.center_column_bits len 32 = "
          f"{''.join(map(str, COMMON.center_column_bits(32)))}")
    print()
    check_pde_exhaustive()
    check_pde_on_orbits()
    print()
    check_zeroset_simplification()
    print()
    check_left_edge_and_cascade()
    print()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
