"""
Verify (or refute) the claimed variation-of-constants identity for Rule 30:

  a_t = L_t[delta_0]  XOR  (XOR over 0<=s<t, all i of  K_{t-s, -i} * chi_{s,i})

where:
  - Rule 30: u_{t+1,i} = u_{t,i-1} XOR u_{t,i} XOR u_{t,i+1} XOR chi_{t,i}
             chi_{t,i} = u_{t,i} AND u_{t,i+1}
  - L_t[delta_0]: value at the origin after t steps of pure Rule 150
    (u_{t+1,i} = u_{t,i-1} XOR u_{t,i} XOR u_{t,i+1}, no defect term), same lone seed.
  - K_n(j) = C(n, (n+j)/2) mod 2, tested via Lucas/Kummer submask test:
        let p = (n+j)/2 (must be integer, 0<=p<=n); K_n(j) = 1 iff (n & p) == p.
    K_n(j) = 0 if n+j is odd, or |j|>n, or p out of range.

We simulate Rule 30 directly, extract a_t and chi from that same trajectory,
simulate Rule 150 separately for L_t, compute K_n(j) via the submask test,
then compute the claimed RHS for each t and compare bit-for-bit to a_t.
"""
import numpy as np

def simulate(rule_is_30, T, width):
    """Simulate width-array CA for T steps from lone-seed at center.
    rule_is_30=True -> Rule 30 (with chi term); False -> Rule 150 (linear only).
    Returns u[t,i] for t=0..T (T+1 rows), and if rule_is_30, also chi[t,i] for t=0..T-1.
    """
    c = width // 2
    u = np.zeros((T + 1, width), dtype=np.uint8)
    u[0, c] = 1
    chi = np.zeros((T, width), dtype=np.uint8) if rule_is_30 else None
    for t in range(T):
        row = u[t]
        left = np.roll(row, 1)
        right = np.roll(row, -1)
        # zero out wrap-around contributions (we have margin so this shouldn't matter
        # as long as nonzero region stays away from edges)
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


def kernel_table(T, maxj):
    """K[n][j+maxj] for n=0..T, j=-maxj..maxj via Lucas/Kummer submask test."""
    n_arr = np.arange(0, T + 1).reshape(-1, 1)
    j_arr = np.arange(-maxj, maxj + 1).reshape(1, -1)
    N = np.broadcast_to(n_arr, (T + 1, 2 * maxj + 1)).astype(np.int64)
    J = np.broadcast_to(j_arr, (T + 1, 2 * maxj + 1)).astype(np.int64)
    valid = ((N + J) % 2 == 0) & (J >= -N) & (J <= N) & (N >= 0)
    P = np.zeros_like(N)
    P[valid] = (N[valid] + J[valid]) // 2
    K = np.zeros_like(N, dtype=np.uint8)
    ok = valid & (P >= 0) & (P <= N)
    # submask test: (n & p) == p
    K[ok] = ((N[ok] & P[ok]) == P[ok]).astype(np.uint8)
    return K  # shape (T+1, 2*maxj+1), index [n, j+maxj]


def main():
    T = 220
    width = 6 * T + 20
    c = width // 2

    print(f"Simulating Rule 30 and Rule 150, T={T}, width={width}, center index c={c}")
    u30, chi = simulate(True, T, width)
    u150 = simulate(False, T, width)

    a_t = u30[:, c].astype(np.uint8)          # a_t for t=0..T
    L_t = u150[:, c].astype(np.uint8)         # L_t[delta_0] for t=0..T

    maxj = width // 2 + 2  # j ranges over full half-width, generous
    K = kernel_table(T, maxj)  # K[n, j+maxj], n=0..T

    def Kfun(n, j):
        if n < 0 or abs(j) > maxj:
            return 0
        return int(K[n, j + maxj])

    mismatches = []
    rhs_vals = np.zeros(T + 1, dtype=np.uint8)
    rhs_vals[0] = L_t[0]  # t=0: no defects have acted yet (s<0 empty), a_0 = L_0 = 1

    for t in range(1, T + 1):
        acc = 0
        for s in range(0, t):
            n = t - s
            if n > maxj:
                continue
            # j = -i (i measured relative to origin, i.e. array index - c)
            # chi[s, idx] where idx = i + c
            # restrict i to |i| <= n (kernel support) intersect array bounds
            i_lo = max(-n, -c)
            i_hi = min(n, width - 1 - c)
            if i_lo > i_hi:
                continue
            i_vals = np.arange(i_lo, i_hi + 1)
            j_vals = -i_vals
            k_row = K[n, j_vals + maxj]  # kernel weights for this n, over i_vals
            chi_row = chi[s, i_vals + c]
            contrib = int(np.bitwise_xor.reduce((k_row & chi_row).astype(np.uint8))) if len(i_vals) else 0
            acc ^= contrib
        rhs = L_t[t] ^ acc
        rhs_vals[t] = rhs
        if rhs != a_t[t]:
            mismatches.append((t, int(a_t[t]), int(rhs)))

    print(f"a_t computed for t=0..{T}")
    print(f"Total mismatches vs claimed RHS: {len(mismatches)} / {T+1} indices checked")
    if mismatches:
        print("First 20 mismatches (t, a_t, rhs):")
        for m in mismatches[:20]:
            print(" ", m)
        print("VERDICT: IDENTITY AS STATED IS REFUTED (mismatches found).")
    else:
        print("VERDICT: IDENTITY HOLDS EXACTLY for all t=0..%d (zero mismatches)." % T)

    # sanity: print a_t and L_t for first several t for a human sanity check
    print("t : a_t L_t (first 30)")
    for t in range(30):
        print(t, int(a_t[t]), int(L_t[t]))


if __name__ == "__main__":
    main()
