"""Structure of r|Z under the period-two drive: period-5 background with phase slips.

(1) 300 random prefixes (length 24), T = 4096: fraction whose r|Z locks (eventual period <= 64).
(2) empty prefix, T = 65536: gap sequence of ones in r|Z (gaps 3 or 5), slip (gap 3) positions,
    distribution of the number of 5-gaps between slips, block-wise slip density.
(3) locked example (prefix seed 5 of prefix_dependence.py): periodic strip width.
"""
import sys, random, time
from collections import Counter
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_rhp, eventual_period

def make_c(prefix, w, T):
    L = len(prefix)
    p = len(w)
    c = list(prefix) + [w[(t - L) % p] for t in range(L, T + 2)]
    c[0] = 1
    return c

def main():
    out = []
    t0 = time.time()
    w = [0, 1]
    # (1)
    T = 4096
    locked = 0
    lock_periods = Counter()
    for seed in range(300):
        rng = random.Random(1000 + seed)
        prefix = [rng.getrandbits(1) for _ in range(24)]
        c = make_c(prefix, w, T)
        Z = [t for t in range(T + 1) if c[t] == 0]
        rows = driven_rhp(c, T)
        rZ = [(rows[t] >> 1) & 1 for t in Z]
        ep = eventual_period(rZ, 64)
        if ep is not None:
            locked += 1
            lock_periods[ep[0]] += 1
    out.append(f"(1) drive (01)^inf, 300 random prefixes len 24, T={T}: locked (period<=64, onset<=|Z|/2) = {locked}/300; lock periods {dict(lock_periods)}")
    # (2)
    T = 65536
    c = make_c([], w, T)
    Z = [t for t in range(T + 1) if c[t] == 0]
    rows = driven_rhp(c, T)
    rZ = [(rows[t] >> 1) & 1 for t in Z]
    ones = [i for i, v in enumerate(rZ) if v]
    gaps = [ones[i + 1] - ones[i] for i in range(len(ones) - 1)]
    gc = Counter(gaps)
    out.append(f"(2) empty prefix T={T}: |Z|={len(Z)} ones={len(ones)} gap histogram {sorted(gc.items())}")
    slips = [i for i, g in enumerate(gaps) if g != 5]
    between = [slips[i + 1] - slips[i] - 1 for i in range(len(slips) - 1)]
    bc = Counter(between)
    out.append(f"    slips (gap != 5): {len(slips)}; 5-gaps between consecutive slips: histogram {sorted(bc.items())[:30]}")
    mean_between = sum(between) / len(between)
    out.append(f"    mean 5-gaps between slips {mean_between:.3f} (geometric fit p = {1/(mean_between+1):.3f})")
    nb = 16
    blk = len(gaps) // nb
    dens = [sum(1 for g in gaps[i * blk:(i + 1) * blk] if g != 5) / blk for i in range(nb)]
    out.append(f"    slip density per block of {blk} gaps: {[round(d, 3) for d in dens]}")
    # slip position parity / phase structure
    out.append(f"    first 40 between-slip counts: {between[:40]}")
    # (3) locked example
    T = 4096
    rng = random.Random(5)
    prefix = [rng.getrandbits(1) for _ in range(16)]
    c = make_c(prefix, w, T)
    Z = [t for t in range(T + 1) if c[t] == 0]
    rows = driven_rhp(c, T)
    rZ = [(rows[t] >> 1) & 1 for t in Z]
    ep = eventual_period(rZ, 64)
    out.append(f"(3) locked example prefix(seed5)={''.join(map(str, prefix))}: r|Z eventual period {ep}")
    if ep is not None:
        # find the periodic strip: for widths W, check whether columns 1..W are all eventually periodic (time period <= 64)
        for W in range(1, 40):
            col = [(rows[t] >> W) & 1 for t in range(T + 1)]
            epc = eventual_period(col, 64)
            out.append(f"    column {W}: eventual period {epc}")
            if epc is None:
                break
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
