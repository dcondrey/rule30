"""
Build M_T (using the CORRECTED, verified kernel from verify_identity_corrected2.py:
K_n(j) = actual Rule150 propagator value at offset j after n steps, n = t-1-s)
and measure rank(M_T) over GF(2) as a function of T, plus rank as a fraction of
the ambient column-space dimension (~T * (2T-1)).

Rows of M_T: t = 1..T  (T rows)
Columns of M_T: (s, i) pairs, 0 <= s <= T-1, i in light-cone range for that s
Entry M_T[t-1, col(s,i)] = K_{t-1-s}(-i)  (0 if t-1-s < 0)

Rank computed via GF(2) Gaussian elimination using Python big integers as
bit-packed row vectors (fast XOR at the C level).
"""
import numpy as np
import time


def rule150_propagator(T, width):
    """Return u150[n, :] for n=0..T, pure Rule150 evolution from lone seed at center c."""
    c = width // 2
    u = np.zeros((T + 1, width), dtype=np.uint8)
    u[0, c] = 1
    for t in range(T):
        row = u[t]
        left = np.roll(row, 1)
        right = np.roll(row, -1)
        left[0] = 0
        right[-1] = 0
        u[t + 1] = left ^ row ^ right
    return u, c


def gf2_rank(rows, ncols):
    """Rank of a list of Python-int bitmask rows (each < 2**ncols) over GF(2)."""
    rows = [r for r in rows if r != 0]
    rank = 0
    pivots = []  # (bit_position, row_value) sorted by descending bit position, kept reduced
    for r in rows:
        cur = r
        for pbit, prow in pivots:
            if (cur >> pbit) & 1:
                cur ^= prow
        if cur != 0:
            pbit = cur.bit_length() - 1
            pivots.append((pbit, cur))
            rank += 1
    return rank


def build_and_rank(T):
    maxn = T - 1  # max exponent n = t-1-s, t<=T, s>=0 => n<=T-1
    width = 2 * maxn + 5
    u150, c = rule150_propagator(maxn, width)  # u150[n, c+j]

    # column universe: (s, i) with 0<=s<=T-1, i in [-maxn+s .. ] -- just use i in [-(T-1-s), T-1-s]
    # We'll assign a fixed column ordering: for each s in 0..T-1, i ranges -(T-1-s)..(T-1-s)
    col_index = {}
    col_list = []
    for s in range(T):
        nmax_s = T - 1 - s  # largest n = t-1-s achievable is when t=T => n=T-1-s
        for i in range(-nmax_s, nmax_s + 1):
            col_index[(s, i)] = len(col_list)
            col_list.append((s, i))
    ncols = len(col_list)

    rows = []
    for t in range(1, T + 1):
        bits = 0
        for s in range(0, t):
            n = t - 1 - s
            if n < 0:
                continue
            nmax_s = T - 1 - s
            i_lo, i_hi = -n, n
            for i in range(i_lo, i_hi + 1):
                j = -i
                if abs(j) > maxn:
                    continue
                if u150[n, c + j]:
                    col = col_index[(s, i)]
                    bits |= (1 << col)
        rows.append(bits)

    rank = gf2_rank(rows, ncols)
    return rank, ncols, T


def main():
    Ts = [10, 20, 30, 50, 75, 100, 150, 200, 250, 300]
    print(f"{'T':>5} {'rank(M_T)':>10} {'ambient_cols':>14} {'rank/T':>8} {'rank/ambient':>14} {'time(s)':>8}")
    results = []
    for T in Ts:
        t0 = time.time()
        rank, ncols, _ = build_and_rank(T)
        dt = time.time() - t0
        results.append((T, rank, ncols, dt))
        print(f"{T:>5} {rank:>10} {ncols:>14} {rank/T:>8.4f} {rank/ncols:>14.6f} {dt:>8.2f}")

    print()
    print("Raw results (T, rank, ambient_cols, seconds):")
    for r in results:
        print(" ", r)


if __name__ == "__main__":
    main()
