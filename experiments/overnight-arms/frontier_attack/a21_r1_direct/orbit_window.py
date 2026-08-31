"""a21 step 7: the SAME question on the actual lone-seed orbit, not universally.

Theorem W says the universal function phi_t is not a bounded-window function of
the centre trace.  That kills the route "prove Lemma Z by exhibiting a bounded
window that works for every left-supported row".  It does NOT by itself kill the
weaker route "on the single lone-seed orbit, r_t happens to agree with some
bounded-window function of c".  A single orbit is a measure-zero set and could be
special (obstruction E in PATH.md 7.3 has the same shape).

So: on the true lone-seed diagram, for each window width m, is the map
(c_{t-m},...,c_{t-1}) -> r_t single-valued over t < T?  A CONFLICT (two times
with the same window and different r_t) refutes width m at this horizon.

Reported both for all t and for t restricted to the zero set Z = {t : c_t = 0},
which is the only part Lemma Z needs.

OBSTRUCTION H.  A conflict is a refutation and is exact.  The absence of a
conflict at some m would be only "not refuted at T", never a proof.

Usage: uv run python orbit_window.py [T] [mmax] > orbit_window_output.txt
"""

from __future__ import annotations

import sys

from substrate import COMMON, step


def trace(T: int, rule: int) -> tuple[list[int], list[int]]:
    """c_t = s(t,0) and r_t = s(t,1) of the lone seed, t < T."""
    row = 1
    c, r = [], []
    for t in range(T):
        c.append((row >> t) & 1)
        r.append((row >> (t + 1)) & 1)
        row = step(row, rule)
    return c, r


def main() -> None:
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    print("a21 / orbit_window.py -- bounded-window determination on the true orbit")
    print(f"T = {T}, m = 1..{mmax}\n")
    for rule in (30, 90):
        c, r = trace(T, rule)
        if rule == 30:
            assert c[:4096] == COMMON.center_column_bits(4096), "trace cross-check"
            print("  cross-check: first 4096 centre bits match common.center_column_bits")
        nz = sum(1 for v in c if v == 0)
        print(f"=== rule {rule}: |Z| = {nz} of {T} ===")
        print(
            "   m | conflicts (all t)   first t | conflicts (t in Z)   first t "
            "| repeat-window opportunities (all t)"
        )
        for m in range(1, mmax + 1):
            seen_a: dict[int, int] = {}
            seen_z: dict[int, int] = {}
            ca = cz = 0
            opp = 0
            fa = fz = None
            win = 0
            mask = (1 << m) - 1
            for t in range(T):
                if t >= m:
                    v = r[t]
                    prev = seen_a.get(win)
                    if prev is None:
                        seen_a[win] = v
                    else:
                        opp += 1
                    if prev is not None and prev != v:
                        ca += 1
                        if fa is None:
                            fa = t
                    if c[t] == 0:
                        prevz = seen_z.get(win)
                        if prevz is None:
                            seen_z[win] = v
                        elif prevz != v:
                            cz += 1
                            if fz is None:
                                fz = t
                win = ((win << 1) | c[t]) & mask
            print(
                f"  {m:2d} | {ca:12d} {str(fa):>10s} | {cz:12d} {str(fz):>10s}"
                f" | {opp:12d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
