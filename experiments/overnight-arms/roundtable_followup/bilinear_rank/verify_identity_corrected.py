"""
Follow-up diagnostic (NOT part of the panel's claim as literally stated):
the panel's kernel K_n(j) = C(n,(n+j)/2) mod 2 is the Rule-90 / Pascal-mod-2
(Sierpinski) propagator, appropriate for a CA whose update is XOR of the two
OUTER neighbors only. Rule 150's update is XOR of THREE neighbors (left,
center, right), whose correct linear Green's function is the actual Rule 150
propagator itself (trinomial coefficients mod 2), not the binomial one.

The problem statement itself gives a second, self-consistent characterization:
"K_n(j) equals the value at position j after n steps of Rule 150 evolution
from a lone seed at 0." We test THAT definition (call it K150) instead of the
binomial formula, to see whether the Duhamel/variation-of-constants identity
holds with the CORRECT linear propagator.
"""
import numpy as np


def simulate(rule_is_30, T, width):
    c = width // 2
    u = np.zeros((T + 1, width), dtype=np.uint8)
    u[0, c] = 1
    chi = np.zeros((T, width), dtype=np.uint8) if rule_is_30 else None
    for t in range(T):
        row = u[t]
        left = np.roll(row, 1)
        right = np.roll(row, -1)
        left[0] = 0
        right[-1] = 0
        lin = left ^ row ^ right
        if rule_is_30:
            c_and_r = row & right
            chi[t] = c_and_r
            u[t + 1] = lin ^ c_and_r
        else:
            u[t + 1] = lin
    return (u, chi) if rule_is_30 else u


def main():
    T = 220
    width = 6 * T + 20
    c = width // 2

    print(f"T={T}, width={width}, c={c}")
    u30, chi = simulate(True, T, width)
    u150 = simulate(False, T, width)  # u150[n, c+j] = K150_n(j) by definition

    a_t = u30[:, c].astype(np.uint8)
    L_t = u150[:, c].astype(np.uint8)

    mismatches = []
    for t in range(1, T + 1):
        acc = 0
        for s in range(0, t):
            n = t - s
            if n > T:
                continue
            # K150_n(j) at j = -i  => index into u150 row n at column c + j = c - i
            i_lo = max(-n, -c)
            i_hi = min(n, width - 1 - c)
            if i_lo > i_hi:
                continue
            i_vals = np.arange(i_lo, i_hi + 1)
            j_vals = -i_vals
            k_row = u150[n, c + j_vals]
            chi_row = chi[s, i_vals + c]
            contrib = int(np.bitwise_xor.reduce((k_row & chi_row).astype(np.uint8))) if len(i_vals) else 0
            acc ^= contrib
        rhs = L_t[t] ^ acc
        if rhs != a_t[t]:
            mismatches.append((t, int(a_t[t]), int(rhs)))

    print(f"Mismatches with CORRECTED kernel K150_n(j) = Rule150 propagator: {len(mismatches)} / {T}")
    if mismatches:
        print("First 20 mismatches:", mismatches[:20])
        print("VERDICT: even with the corrected propagator, identity fails.")
    else:
        print("VERDICT: identity HOLDS EXACTLY with the corrected linear propagator "
              "(Rule150's own Green's function), for all t=1..%d." % T)


if __name__ == "__main__":
    main()
