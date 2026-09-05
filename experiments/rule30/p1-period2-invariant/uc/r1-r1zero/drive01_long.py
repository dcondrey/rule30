"""Long-horizon test of the period-two drive: does r|Z ever lock?  T = 2^19."""
import sys, random, time
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_rhp, eventual_period, lone_seed_columns

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 19
    out = [f"T={T}"]
    true_c = lone_seed_columns(64, [0])[0]
    t0 = time.time()
    cases = [("true[:0]", []), ("true[:16]", true_c[:16])]
    for seed in (11, 12):
        rng = random.Random(seed)
        cases.append((f"random{seed}", [rng.getrandbits(1) for _ in range(24)]))
    for name, prefix in cases:
        L = len(prefix)
        c = prefix + [[0, 1][(t - L) % 2] for t in range(L, T + 2)]
        c[0] = 1
        # stream: keep only r and Z
        row = c[0]
        rZ = []
        for t in range(T + 1):
            if c[t] == 0:
                rZ.append((row >> 1) & 1)
            nxt = (row << 1) ^ (row | (row >> 1))
            row = (nxt & ~1) | c[t + 1]
        n = len(rZ)
        tail = rZ[3 * n // 4:]
        ep = eventual_period(tail, 4096, min_tail_frac=0.5)
        nb = 16
        blk = n // nb
        dens = [round(sum(rZ[i * blk:(i + 1) * blk]) / blk, 4) for i in range(nb)]
        out.append(f"{name}: |Z|={n} last-quarter eventual period (q<=4096) = {ep}; block densities {dens}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
