"""a22: verify the OR = XOR + AND decomposition of the pin-parity quantity
on actual reachable survivor states, read-only reuse of a5's band_automaton
(itself read-only reuse of the repo probe).

Claim checked: for state (u, v) with o[m] = u[m] OR v[m], m = 0..T-1,

    parity(o) = parity(u) XOR parity(v) XOR corr(u, v)

where corr(u, v) = XOR_{m=0}^{T-1} (u[m] AND v[m]) is the same-index GF(2)
bilinear (dot-product) correlation of u and v.  This is pure boolean algebra
(a OR b = a XOR b XOR (a AND b) applied termwise then summed mod 2), but it
is checked here against the actual forced-orbit generator to confirm indices
line up as claimed with no off-by-one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a5_row41_fiber_uniform"))
import band_automaton as BA  # noqa: E402  (READ-ONLY reuse)


def corr(u, v):
    return sum(a & b for a, b in zip(u, v)) & 1


def check(kseed: int, pairs: int, phases=(0, 1)) -> bool:
    ok = True
    n_checked = 0
    for phase in phases:
        for m in range(2 ** kseed):
            u, v = BA.seed_state(phase, kseed, m)
            for _ in range(pairs):
                # rho substep
                nxt, prev, par = BA.forced_step(u, v, phase)
                T = len(v)
                claim = (sum(prev[:T]) & 1) ^ (sum(v) & 1) ^ corr(prev, v)
                n_checked += 1
                if claim != par:
                    ok = False
                    print("MISMATCH (rho substep)", phase, m, T, claim, par)
                u, v = nxt, prev
                # pin substep
                nxt, prev, par = BA.forced_step(u, v, phase)
                T = len(v)
                claim = (sum(prev[:T]) & 1) ^ (sum(v) & 1) ^ corr(prev, v)
                n_checked += 1
                if claim != par:
                    ok = False
                    print("MISMATCH (pin substep)", phase, m, T, claim, par)
                if par != 1:
                    break  # died
                u, v = nxt, prev
    print(f"kseed={kseed} pairs={pairs}: {n_checked} checks, ok={ok}")
    return ok


if __name__ == "__main__":
    kseed = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    pairs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    check(kseed, pairs)
