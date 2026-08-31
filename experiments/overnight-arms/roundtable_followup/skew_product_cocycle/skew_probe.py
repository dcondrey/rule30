"""Direction 8 completion check: left-permutive skew-product cocycle over the
centre column, fibre r_t = u_{t,1}.

Claims checked here are ANALYTIC (they follow from the Rule 30 / Rule 90
local rules by direct substitution and are re-derivations of
RESULTS-ladder-rung1.md Lemma 1 / Lemma 1' at R=1) -- the simulation below is
a sanity check + collision-finder on the true lone-seed orbit, not a proof by
itself.

Bit-parallel convention follows experiments/rule30/center_column.py: a whole
row is one Python int, bit position p holds the cell at spatial coordinate
p - off (off is fixed so that p=off is x=0, the seed column).
"""
import sys


def run(steps: int, rule: int):
    """Return (a, r, u2) as lists of 0/1, length `steps`, for rule 30 or 90.

    a_t = s(t,0), r_t = s(t,1) =: u_{t,1}, u2_t = s(t,2) =: u_{t,2}.
    """
    off = steps + 4
    row = 1 << off
    a, r, u2 = [], [], []
    for t in range(steps):
        a.append((row >> off) & 1)
        r.append((row >> (off + 1)) & 1)
        u2.append((row >> (off + 2)) & 1)
        if rule == 30:
            row = (row << 1) ^ (row | (row >> 1))
        elif rule == 90:
            row = (row << 1) ^ (row >> 1)
        else:
            raise ValueError(rule)
    return a, r, u2


def check_identity(a, r, u2, rule, T):
    """r_{t+1} == a_t XOR (r_t OR u2_t)   [rule 30]
       r_{t+1} == a_t XOR u2_t            [rule 90]
    This is Lemma 1 / Lemma 1' at R=1 from RESULTS-ladder-rung1.md, applied
    to the true orbit as a regression check on this script's bit-parallel
    extraction, not a new fact."""
    viol = 0
    for t in range(T - 1):
        if rule == 30:
            pred = a[t] ^ (r[t] | u2[t])
        else:
            pred = a[t] ^ u2[t]
        if pred != r[t + 1]:
            viol += 1
    return viol


def scalar_fibre_map_exists(a, r, T):
    """Is r_{t+1} a function of (a_t, r_t) alone (a 2-state x 2-symbol table),
    i.e. does the naive Phi_a: {0,1}->{0,1} reading of the fragment hold on
    the true orbit?  Report collisions: same (a_t,r_t) pair, different
    r_{t+1}."""
    table = {}
    collisions = []
    for t in range(T - 1):
        key = (a[t], r[t])
        val = r[t + 1]
        if key in table and table[key] != val:
            collisions.append((t, key, table[key], val))
        else:
            table[key] = val
    return table, collisions


def bounded_history_map_exists(a, r, T, k):
    """Is r_t a function of the length-k window (a_{t-k+1},...,a_t) alone?
    Report the first collision (same window, different r_t) found scanning
    left to right, and the total collision count."""
    table = {}
    collisions = 0
    first = None
    for t in range(k - 1, T):
        window = tuple(a[t - k + 1:t + 1])
        val = r[t]
        if window in table:
            if table[window] != val:
                collisions += 1
                if first is None:
                    first = (t, window, table[window], val)
        else:
            table[window] = val
    return collisions, first, len(table)


def pin_fires_fraction(r, T):
    """Lemma 1: u2_t is FORCED when r_t == 0 (col_R(t)=0 case), FREE when
    r_t == 1.  Fraction of t with r_t == 1 is the fraction of time the fibre
    cascade is genuinely open (new bit of information required)."""
    ones = sum(r[:T])
    return ones / T


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    print(f"T={T}")
    for rule in (30, 90):
        a, r, u2 = run(T, rule)
        viol = check_identity(a, r, u2, rule, T)
        table, collisions = scalar_fibre_map_exists(a, r, T)
        pin_frac = pin_fires_fraction(r, T)
        print(f"\n=== rule {rule} ===")
        print(f"identity r_(t+1) = a_t XOR (r_t OR u2_t) [30] / a_t XOR u2_t [90]: "
              f"{viol} violations / {T-1} checked")
        print(f"scalar map Phi(a_t,r_t) -> r_(t+1): table size {len(table)}, "
              f"collisions (same input, different output): {len(collisions)}")
        for c in collisions[:5]:
            print(f"    collision: t={c[0]} (a_t,r_t)={c[1]} "
                  f"first_saw_r_(t+1)={c[2]} now_r_(t+1)={c[3]}")
        print(f"fraction of t with r_t=1 (pin FREE / cascade genuinely open per Lemma 1): "
              f"{pin_frac:.6f}")
        for k in (1, 2, 4, 8, 12, 16, 20):
            coll, first, tablesize = bounded_history_map_exists(a, r, T, k)
            flag = "collision found" if coll else "no collision in this run"
            print(f"  bounded-history k={k:2d}: distinct windows seen={tablesize:8d}, "
                  f"collisions={coll:6d} ({flag})"
                  + (f", first at t={first[0]}" if first else ""))


if __name__ == "__main__":
    main()
