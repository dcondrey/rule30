"""Deep look at the RHP driven by the period-two words (the PT2 case).

c = prefix + (01)^inf or (10)^inf, prefixes: true lone-seed prefix of length L in {0, 8, 32}.
Reports eventual period search (q <= max_period, onset <= len/2), density, zero-run histogram of r|Z,
one-positions, and block densities.  Rule 90 same drive as control.
"""
import sys, time
from collections import Counter
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_rhp, eventual_period, longest_shift_agreement, lone_seed_columns, rule30_step, rule90_step

def describe(name, seq, max_period, out):
    n = len(seq)
    ep = eventual_period(seq, max_period)
    run, q, i0 = longest_shift_agreement(seq, 512)
    ones = [i for i, v in enumerate(seq) if v]
    zr = Counter()
    cur = 0
    for v in seq:
        if v == 0:
            cur += 1
        else:
            if cur:
                zr[cur] += 1
            cur = 0
    if cur:
        zr[cur] += 1
    blocks = [sum(seq[i:i + n // 8]) / (n // 8) for i in range(0, n - n // 8 + 1, n // 8)]
    out.append(f"{name}: len={n} density={len(ones)/n:.4f} eventual_period={ep} longest_shift_run={run}@shift{q}")
    out.append(f"   block densities (8 blocks): {[round(b, 3) for b in blocks]}")
    out.append(f"   zero-run histogram (run:count): {sorted(zr.items())[:24]}")
    out.append(f"   first 60 one-positions (Z-index): {ones[:60]}")
    out.append(f"   last 10 one-positions: {ones[-10:]}")

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 65536
    max_period = int(sys.argv[2]) if len(sys.argv) > 2 else 8192
    out = [f"T={T} max_period={max_period}"]
    true_c = lone_seed_columns(64, [0])[0]
    t0 = time.time()
    for phase in ((0, 1), (1, 0)):
        for L in (0, 8, 32):
            c = true_c[:L] + [phase[(t - L) % 2] for t in range(L, T + 2)]
            c[0] = 1
            Z = [t for t in range(T + 1) if c[t] == 0]
            rows = driven_rhp(c, T)
            rZ = [(rows[t] >> 1) & 1 for t in Z]
            describe(f"rule30 RHP r|Z, c = true[:{L}] + {''.join(map(str, phase))}^inf", rZ, max_period, out)
            # also column 2 restricted to Z and full r
            r = [(rows[t] >> 1) & 1 for t in range(T + 1)]
            out.append(f"   full r: eventual_period={eventual_period(r, max_period)} density={sum(r)/len(r):.4f}")
            rows90 = driven_rhp(c, T, step=rule90_step)
            rZ90 = [(rows90[t] >> 1) & 1 for t in Z]
            out.append(f"   rule90 same drive: r|Z eventual_period={eventual_period(rZ90, max_period)} density={sum(rZ90)/len(rZ90):.4f}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
