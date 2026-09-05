"""Does eventual periodicity of r|Z under a periodic drive depend on the prefix?

For words w in {001, 0001, 0011, 0111, 01, 011, 00101}, prefixes: 10 random prefixes of length 16 (seeded)
plus the empty prefix, c_0 forced to 1.  T = 16384, max_period 1024.
"""
import sys, random, time
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_rhp, eventual_period

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 16384
    max_period = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    out = [f"T={T} max_period={max_period}"]
    words = ["001", "0001", "0011", "0111", "01", "011", "00101", "010", "100"]
    t0 = time.time()
    for w in words:
        p = len(w)
        wl = [int(ch) for ch in w]
        results = []
        for seed in range(11):
            if seed == 0:
                prefix = []
            else:
                rng = random.Random(seed)
                prefix = [rng.getrandbits(1) for _ in range(16)]
            L = len(prefix)
            c = prefix + [wl[(t - L) % p] for t in range(L, T + 2)]
            c[0] = 1
            Z = [t for t in range(T + 1) if c[t] == 0]
            rows = driven_rhp(c, T)
            rZ = [(rows[t] >> 1) & 1 for t in Z]
            ep = eventual_period(rZ, max_period)
            results.append((seed, ep, round(sum(rZ) / max(1, len(rZ)), 3)))
        n_per = sum(1 for _, ep, _ in results if ep is not None)
        out.append(f"word {w}: periodic r|Z in {n_per}/11 prefixes; details (seed, (q, onset), density): {results}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
