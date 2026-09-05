"""GR1 / GL1 test: half-planes driven by an eventually periodic boundary word.

GR1: right half-plane x >= 1, zero initial data, boundary s(t,0) = c_t eventually periodic.
     Is r_t = s(t,1) restricted to Z = {c_t = 0} eventually periodic?
GL1: left half-plane x <= -1, same drive.  Is l_t = s(t,-1) eventually periodic?

Either statement, if true for the (hypothetically periodic) lone-seed trace, gives two adjacent
eventually periodic columns and hence P1 by the moving left edge.  Rule 90 control: GR1 fails
(c = 0^inf, r_t = [t = 2^j - 1]).
"""
import sys, itertools, time
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import (driven_rhp, driven_lhp, eventual_period, longest_shift_agreement,
                        bernoulli, lone_seed_columns, rule30_step, rule90_step)

def analyse(name, seq, max_period, out):
    ep = eventual_period(seq, max_period)
    run, q, i0 = longest_shift_agreement(seq, min(max_period, 256))
    ones = sum(seq)
    out.append(f"  {name}: len={len(seq)} ones={ones} eventual_period(q<={max_period}, onset<=len/2)={ep} "
               f"longest shift-agreement run={run} at shift {q} start {i0}")
    return ep

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4096
    max_period = int(sys.argv[2]) if len(sys.argv) > 2 else 512
    out = [f"T={T} max_period={max_period}"]
    # true lone-seed trace prefix for optional prefixes
    cols = lone_seed_columns(64, [0])
    true_c = cols[0]
    words = []
    for p in range(1, 7):
        for bits in itertools.product([0, 1], repeat=p):
            w = list(bits)
            if 1 not in w and p > 1:
                continue
            # canonical: skip rotations that are not lexicographically minimal
            rots = [tuple(w[i:] + w[:i]) for i in range(p)]
            if tuple(w) != min(rots):
                continue
            # primitive words only
            if any(p % d == 0 and w == (w[:d] * (p // d)) for d in range(1, p)):
                continue
            words.append(w)
    out.append(f"periodic words tested: {len(words)} (primitive, period 1..6, canonical rotation)")
    summary = {"rhp_periodic": 0, "rhp_total": 0, "lhp_periodic": 0, "lhp_total": 0}
    t0 = time.time()
    for w in words:
        p = len(w)
        for prefix_len in (0, 8):
            prefix = true_c[:prefix_len]
            c = prefix + [w[(t - prefix_len) % p] for t in range(prefix_len, T + 2)]
            if c[0] == 0:
                # seed must be 1 at time 0 so that a diagram with s(0,0)=1 exists; use prefix [1]
                c = [1] + c[1:]
            Z = [t for t in range(T + 1) if c[t] == 0]
            out.append(f"word {''.join(map(str, w))} prefix_len={prefix_len} |Z|={len(Z)}")
            if len(Z) < 64:
                out.append("  zero set too small, skipped")
                continue
            rows = driven_rhp(c, T)
            r = [(rows[t] >> 1) & 1 for t in range(T + 1)]
            rZ = [r[t] for t in Z]
            ep = analyse("RHP r|Z (rule 30)", rZ, max_period, out)
            summary["rhp_total"] += 1
            summary["rhp_periodic"] += int(ep is not None)
            rows = driven_lhp(c, T)
            l = [(rows[t] >> 1) & 1 for t in range(T + 1)]
            ep = analyse("LHP l (rule 30)", l, max_period, out)
            summary["lhp_total"] += 1
            summary["lhp_periodic"] += int(ep is not None)
            # also l on Z, and the pin check on the 1-set (for information)
            lZ = [l[t] for t in Z]
            analyse("LHP l|Z (rule 30)", lZ, max_period, out)
            pin_viol = sum(1 for t in range(T) if c[t] == 1 and l[t] != (1 ^ c[t + 1]))
            out.append(f"  pin violations (c_t=1, l_t != 1+c_(t+1)) in driven LHP: {pin_viol} of {sum(c[:T])}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    out.append(f"SUMMARY rule30: RHP r|Z eventually periodic in {summary['rhp_periodic']}/{summary['rhp_total']} drives; "
               f"LHP l eventually periodic in {summary['lhp_periodic']}/{summary['lhp_total']} drives")
    # controls
    out.append("CONTROLS")
    c0 = [1] + [0] * (T + 2)
    rows = driven_rhp(c0, T, step=rule90_step)
    r = [(rows[t] >> 1) & 1 for t in range(T + 1)]
    analyse("rule 90 RHP r, c = 1 0^inf (expect ones at t = 2^j - 1, aperiodic)", r, max_period, out)
    out.append(f"  rule 90 ones at t = {[t for t in range(T + 1) if r[t]][:12]}")
    c01 = [1] + [(t % 2) for t in range(1, T + 3)]
    rows = driven_rhp(c01, T, step=rule90_step)
    r = [(rows[t] >> 1) & 1 for t in range(T + 1)]
    analyse("rule 90 RHP r|Z, c = 1 (10)^inf", [r[t] for t in range(T + 1) if c01[t] == 0], max_period, out)
    # lone seed actual r|Z and l
    cols = lone_seed_columns(T, [-1, 0, 1])
    cZ = [t for t in range(T + 1) if cols[0][t] == 0]
    analyse("lone seed actual r|Z", [cols[1][t] for t in cZ], max_period, out)
    analyse("lone seed actual l", cols[-1], max_period, out)
    analyse("Bernoulli(1/2) seed 1", bernoulli(T // 2, 1), max_period, out)
    analyse("Bernoulli(1/2) seed 2", bernoulli(T // 2, 2), max_period, out)
    print("\n".join(out))

if __name__ == '__main__':
    main()
