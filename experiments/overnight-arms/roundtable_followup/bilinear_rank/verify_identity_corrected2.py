"""
Second diagnostic fix attempt: the Duhamel/variation-of-constants formula for
u_{s+1} = A(u_s) XOR chi_s implies a defect injected at time s (into u_{s+1})
propagates for n = t-1-s further linear steps to reach time t (not t-s steps).
Test with n = t-1-s, using the CORRECT Rule150 propagator K150_n(j) = u150[n, c+j].
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

    u30, chi = simulate(True, T, width)
    u150 = simulate(False, T, width)

    a_t = u30[:, c].astype(np.uint8)
    L_t = u150[:, c].astype(np.uint8)

    mismatches = []
    for t in range(1, T + 1):
        acc = 0
        for s in range(0, t):
            n = t - 1 - s
            if n < 0 or n > T:
                continue
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

    print(f"Mismatches with n=t-1-s, K150 propagator: {len(mismatches)} / {T}")
    if mismatches:
        print("First 20 mismatches:", mismatches[:20])
        print("VERDICT: still fails.")
    else:
        print("VERDICT: identity HOLDS EXACTLY with n=t-1-s and Rule150 propagator, t=1..%d" % T)


if __name__ == "__main__":
    main()
