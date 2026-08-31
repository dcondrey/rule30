"""
Task 2(b)/(c): pin down what DeepSeek's Direction-2 object chi_{s,i}, K, I_n
actually IS, verify the underlying exact algebraic decomposition, and measure
|I_n| growth as a data point (MEASURED, not a proof).

Exact fact used (verified by hand and computationally below):
    f_30(a,b,c) = a XOR (b OR c) = a XOR b XOR c XOR (b AND c)
So, writing L = Rule150 (the LINEAR/additive CA: L(x)_i = x_{i-1} XOR x_i XOR x_{i+1}):
    F30(x)_i = L(x)_i XOR chi(x)_i,     chi(x)_i := x_i AND x_{i+1}

Since L is GF(2)-linear, "variation of parameters" (Duhamel) gives, EXACTLY:
    x^{(t)} = L^t(x^{(0)})  XOR  XOR_{s=0}^{t-1} L^{t-1-s}( chi(x^{(s)}) )

so at the center column (position 0), for a_n = (F30^n x)_0:
    a_n = [L^n(e)]_0  XOR  XOR_{s=0}^{n-1} XOR_i  K_{n-1-s}(i) * chi(x^{(s)})_i

where K_d(i) = [L^d(delta_0)]_i is the d-step Rule150 propagator (a trinomial-
coefficient-mod-2 / Sierpinski-like fractal kernel -- this is almost certainly
what DeepSeek meant by "Sierpinski/Pascal-mod-2 kernel", up to the Rule90-vs-
Rule150 distinction addressed in the results doc).

chi(x^{(s)})_i = u_{s,i} AND u_{s,i+1} matches DeepSeek's chi_{s,i} definition
exactly. This script:
  1. Verifies the decomposition identity holds exactly against direct Rule 30
     simulation (sanity check that we've reconstructed the right object).
  2. Defines I_n := {(s,i) : K_{n-1-s}(i) = 1 and chi_{s,i} = 1} using this
     concrete kernel, and measures |I_n| vs n. MEASURED ONLY.
"""
import numpy as np


def simulate_rule30(n, width):
    x = np.zeros(width, dtype=np.uint8)
    c = width // 2
    x[c] = 1
    rows = [x.copy()]
    for t in range(n):
        left = np.roll(x, 1)
        right = np.roll(x, -1)
        x = left ^ (x | right)
        rows.append(x.copy())
    return rows, c


def rule150_propagator_table(n):
    """K[d] is a 1D array indexed by relative offset j in [-d, d] (stored with
    offset d, so array length 2d+1), giving L^d(delta_0)(j) mod 2, for
    d = 0..n (inclusive). Returns list of arrays and their center-offsets."""
    K = [np.array([1], dtype=np.uint8)]  # d=0: delta at 0
    for d in range(1, n + 1):
        prev = K[d - 1]
        padded = np.zeros(len(prev) + 2, dtype=np.uint8)
        padded[1:-1] = prev
        # L step: new[j] = old[j-1] xor old[j] xor old[j+1], on the padded array
        left = padded.copy()
        left[1:] = padded[:-1]
        left[0] = 0
        right = padded.copy()
        right[:-1] = padded[1:]
        right[-1] = 0
        newk = left ^ padded ^ right
        K.append(newk)
    return K  # K[d] has length 2d+1, index j+d corresponds to offset j in [-d,d]


def K_val(Ktab, d, j):
    arr = Ktab[d]
    half = (len(arr) - 1) // 2
    if abs(j) > half:
        return 0
    return int(arr[j + half])


def main():
    N = 400  # keep decomposition-verification small: O(n^2) work, exact check
    width = 2 * N + 5
    rows, c = simulate_rule30(N, width)
    Ktab = rule150_propagator_table(N)

    # chi(x^{(s)})_i for i in a window around center, stored relative to center
    # (only need i near 0 out to +-N since K_d has support radius d <= N)
    def chi_val(s, i):
        row = rows[s]
        idx = c + i
        return int(row[idx] & row[idx + 1])

    fails = 0
    for n in range(1, N + 1):
        a_n_direct = int(rows[n][c])
        base = K_val(Ktab, n, 0)  # [L^n(e)]_0 = K_n(0) since e is delta at 0
        acc = base
        for s in range(0, n):
            d = n - 1 - s
            arr = Ktab[d]
            half = (len(arr) - 1) // 2
            for j_off in range(-half, half + 1):
                if arr[j_off + half]:
                    acc ^= chi_val(s, j_off)
        if acc != a_n_direct:
            fails += 1
            if fails <= 3:
                print(f"MISMATCH at n={n}: direct={a_n_direct} decomposition={acc}")

    print(f"Decomposition verified exactly for n=1..{N}: "
          f"{'ALL MATCH' if fails == 0 else f'{fails} MISMATCHES'}")

    if fails == 0:
        # Now measure |I_n| growth for larger n using the same construction,
        # but only need chi and K up to radius, no need to re-verify.
        Nbig = 2000
        widthbig = 2 * Nbig + 5
        rows_big, cbig = simulate_rule30(Nbig, widthbig)
        Kbig = rule150_propagator_table(Nbig)

        def chi_val_big(s, i):
            row = rows_big[s]
            idx = cbig + i
            return int(row[idx] & row[idx + 1])

        sizes = []
        ns_to_check = [50, 100, 200, 400, 800, 1200, 1600, 2000]
        for n in ns_to_check:
            count = 0
            support = 0
            for s in range(0, n):
                d = n - 1 - s
                arr = Kbig[d]
                half = (len(arr) - 1) // 2
                for j_off in range(-half, half + 1):
                    if arr[j_off + half]:
                        support += 1
                        if chi_val_big(s, j_off):
                            count += 1
            sizes.append((n, support, count))
            print(f"n={n}: |support of K|={support}  |I_n|={count}  "
                  f"ratio |I_n|/support={count/support:.4f}  |I_n|/n={count/n:.4f}")

        # crude log-log growth fit for |I_n| vs n using last few points
        import math
        ns = [s[0] for s in sizes]
        cs = [s[2] for s in sizes]
        supp = [s[1] for s in sizes]
        def loglog_slope(xs, ys):
            lx = [math.log(x) for x in xs]
            ly = [math.log(y) for y in ys if y > 0]
            if len(ly) != len(lx):
                return None
            n_ = len(lx)
            mx = sum(lx) / n_
            my = sum(ly) / n_
            num = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
            den = sum((x - mx) ** 2 for x in lx)
            return num / den if den else None
        print("log-log slope |I_n| vs n (all points):", loglog_slope(ns, cs))
        print("log-log slope |support(K)| vs n (all points):", loglog_slope(ns, supp))


if __name__ == "__main__":
    main()
