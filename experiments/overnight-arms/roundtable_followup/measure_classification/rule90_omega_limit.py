"""
Check the panel's Rule-90 screen for Direction 2 ("point-specific omega-limit
classification"): the claim that Omega(e), the omega-limit set of the
lone-seed row e under Rule 90's global map F acting on {0,1}^Z, is the
singleton {0^infinity}.

Method: exact bitmask simulation of Rule 90 (row_{t+1}[n] = row_t[n-1] XOR
row_t[n+1]) using Python big integers, cross-checked against the closed form
x_t(n) = 1 iff (n+t) even and C(t, (n+t)/2) is odd (Kummer/Lucas: odd iff
bits of (n+t)/2 are a submask of bits of t).

Three probes:
  (1) center column x_t(0): confirm it is 1 at t=0 and 0 for all t>=1
      (this is the one classically-cited "eventually-zero centre column"
      fact; not in question).
  (2) a fixed off-center column (n=1): show it returns to 1 infinitely
      often as t -> infinity (t = 2^k - 1), which means the FULL
      CONFIGURATION x_t does not converge to the all-zero point in the
      product topology, so Omega(e) is NOT the singleton {0^infinity}.
  (3) the all-zero configuration 0 IS a limit point of the orbit (find,
      for growing window W, a time t with x_t == 0 on [-W, W]) -- so 0
      belongs to Omega(e) as one recurrent point among others, not as the
      whole set.
"""
import sys


def simulate_rule90(seed_bit_index: int, n_steps: int, half_width: int):
    """Bitmask simulation. Row stored as a python int, bit k = site (k - half_width).
    Returns list of rows (as ints) for t = 0..n_steps, each masked to
    2*half_width+1 bits so it doesn't grow unboundedly."""
    width = 2 * half_width + 1
    mask = (1 << width) - 1
    row = 1 << (half_width + seed_bit_index)
    rows = [row]
    for _ in range(n_steps):
        row = ((row << 1) ^ (row >> 1)) & mask
        rows.append(row)
    return rows, half_width


def bit_at(row: int, half_width: int, n: int) -> int:
    idx = half_width + n
    if idx < 0:
        return 0
    return (row >> idx) & 1


def is_odd_binom(t: int, k: int) -> bool:
    """C(t,k) mod 2 via Kummer/Lucas: odd iff (k & (t-k)) == 0, for 0<=k<=t."""
    if k < 0 or k > t:
        return False
    return (k & (t - k)) == 0


def closed_form_x(t: int, n: int) -> int:
    if (n + t) % 2 != 0:
        return 0
    k = (n + t) // 2
    if k < 0 or k > t:
        return 0
    return 1 if is_odd_binom(t, k) else 0


def probe1_center_column(max_t: int, rows, half_width: int):
    print(f"--- Probe 1: center column x_t(0), t=0..{max_t} ---")
    bad = []
    for t in range(max_t + 1):
        v_sim = bit_at(rows[t], half_width, 0)
        v_cf = closed_form_x(t, 0)
        if v_sim != v_cf:
            bad.append((t, v_sim, v_cf))
        expect = 1 if t == 0 else 0
        if v_sim != expect:
            print(f"  UNEXPECTED at t={t}: x_t(0)={v_sim}, expected {expect}")
    if bad:
        print(f"  MISMATCH sim vs closed form at: {bad[:10]} ...")
    else:
        print("  sim matches closed form for all t in range; "
          "x_t(0)=1 only at t=0, else 0. Confirmed.")


def probe2_offcenter_recurrence(k_max: int):
    print(f"--- Probe 2: column n=1, t = 2^k - 1 for k=1..{k_max} ---")
    hits = []
    for k in range(1, k_max + 1):
        t = (1 << k) - 1
        v = closed_form_x(t, 1)
        hits.append((k, t, v))
    print("  k, t=2^k-1, x_t(1):")
    for k, t, v in hits:
        print(f"    k={k:2d}  t={t:>10d}  x_t(1)={v}")
    all_one = all(v == 1 for _, _, v in hits)
    print(f"  All equal to 1: {all_one}")
    if all_one:
        print("  => x_t(1) = 1 at t = 2^k - 1 for EVERY k checked, arbitrarily "
              "large t. The sequence x_t does not converge to the all-zero "
              "configuration in the product topology (coordinate 1 keeps "
              "returning to 1 at arbitrarily late times).")
        print("  => Omega(e) is NOT the singleton {0^infinity}.")


def probe3_zero_is_limit_point(rows, half_width: int, windows):
    print(f"--- Probe 3: is 0-configuration a limit point? "
          f"(scan for t with row==0 on window [-W,W]) ---")
    max_t = len(rows) - 1
    for W in windows:
        found_t = None
        for t in range(1, max_t + 1):
            row = rows[t]
            zero_on_window = all(bit_at(row, half_width, n) == 0
                                  for n in range(-W, W + 1))
            if zero_on_window:
                found_t = t
                break
        print(f"  W={W:5d}: first t>0 with window all-zero: {found_t}")
    print("  (nonempty hits at growing W indicate 0 recurs as a limit point; "
          "note this only searches early t, up to len(rows)-1; a full proof "
          "of 0 in Omega(e) needs t -> infinity for each fixed W, but any "
          "single hit already shows the *orbit itself* revisits 0 exactly "
          "on that window, which is the relevant witness for compactness "
          "arguments about limit points.)")


def main():
    half_width = 4200
    n_steps = 8200  # covers 2^13-1=8191 for probe1/live check, and gives lots of room for probe3
    rows, hw = simulate_rule90(seed_bit_index=0, n_steps=n_steps, half_width=half_width)

    probe1_center_column(max_t=min(4096, n_steps), rows=rows, half_width=hw)
    print()
    probe2_offcenter_recurrence(k_max=40)  # closed form only, no sim needed, exact ints
    print()
    probe3_zero_is_limit_point(rows, hw, windows=[1, 2, 4, 8, 16, 32, 64])


if __name__ == "__main__":
    sys.exit(main())
