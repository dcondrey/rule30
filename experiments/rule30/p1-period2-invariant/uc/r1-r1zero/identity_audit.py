"""Audit the flagged 10/44-vs-0/44 discrepancy in RESULTS-R1-ZERO-SET-ATTACK.md section 6.

The flag: driven_halfplane.py reports r|Z eventually periodic in 10/44 drives but
l eventually periodic in 0/44, and the x=0 rule instance

    c_{t+1} = l_t XOR (c_t OR r_t)        (identity I)

was read as forcing l periodic whenever c and r|Z are.  Two things have to be true
for that reading: (a) identity I must hold between the two SEPARATE driven
simulations the script runs, and (b) periodicity of r on Z must transfer to l off Z.

This script tests (a) directly and reports the length-matched l|Z column so (b) is
not confounded by sequence length.  No new model, no fitting: the same drives,
the same T, the same eventual_period detector as the original run.
"""
import itertools
import sys

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_rhp, driven_lhp, eventual_period, lone_seed_columns


def drive_words():
    words = []
    for p in range(1, 7):
        for bits in itertools.product([0, 1], repeat=p):
            w = list(bits)
            if 1 not in w and p > 1:
                continue
            rots = [tuple(w[i:] + w[:i]) for i in range(p)]
            if tuple(w) != min(rots):
                continue
            if any(p % d == 0 and w == (w[:d] * (p // d)) for d in range(1, p)):
                continue
            words.append(w)
    return words


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4096
    max_period = int(sys.argv[2]) if len(sys.argv) > 2 else 512
    true_c = lone_seed_columns(64, [0])[0]
    out = [f"identity audit  T={T} max_period={max_period}",
           "columns: drive | |Z| | I-violations(all t) | I-violations(t in Z) | r|Z ep | l|Z ep | l ep"]
    tot = {'n': 0, 'rZ': 0, 'lZ': 0, 'l': 0, 'clean': 0}
    for w in drive_words():
        p = len(w)
        for prefix_len in (0, 8):
            c = true_c[:prefix_len] + [w[(t - prefix_len) % p] for t in range(prefix_len, T + 2)]
            if c[0] == 0:
                c = [1] + c[1:]
            Z = [t for t in range(T + 1) if c[t] == 0]
            if len(Z) < 64:
                continue
            r = [(row >> 1) & 1 for row in driven_rhp(c, T)]
            l = [(row >> 1) & 1 for row in driven_lhp(c, T)]
            # identity I at every t where all four values exist
            viol_all = sum(1 for t in range(T) if c[t + 1] != (l[t] ^ (c[t] | r[t])))
            viol_Z = sum(1 for t in Z if t < T and c[t + 1] != (l[t] ^ (c[t] | r[t])))
            rZ_ep = eventual_period([r[t] for t in Z], max_period)
            lZ_ep = eventual_period([l[t] for t in Z], max_period)
            l_ep = eventual_period(l, max_period)
            tot['n'] += 1
            tot['rZ'] += rZ_ep is not None
            tot['lZ'] += lZ_ep is not None
            tot['l'] += l_ep is not None
            tot['clean'] += viol_all == 0
            out.append(f"  {''.join(map(str, w)):6s} pre={prefix_len} |Z|={len(Z):5d} "
                       f"I_all={viol_all:5d}/{T} I_Z={viol_Z:5d}/{len(Z)} "
                       f"rZ={rZ_ep} lZ={lZ_ep} l={l_ep}")
    # Control A: identity I on a real diagram, where l, c, r share one configuration.
    cols = lone_seed_columns(T + 2, [-1, 0, 1])
    lc, cc, rc = cols[-1], cols[0], cols[1]
    ctrl = sum(1 for t in range(T) if cc[t + 1] != (lc[t] ^ (cc[t] | rc[t])))
    out.append(f"CONTROL A true lone-seed diagram (l, c, r from one configuration): "
               f"I-violations {ctrl}/{T}")
    # Control B: are the two driven models themselves faithful?  Feed them a
    # REALIZABLE drive -- the true lone-seed centre column -- and compare against
    # the true diagram's own columns, then re-test identity I on that driven pair.
    rr = [(row >> 1) & 1 for row in driven_rhp(cc, T)]
    ll = [(row >> 1) & 1 for row in driven_lhp(cc, T)]
    mr = sum(1 for t in range(T + 1) if rr[t] != rc[t])
    ml = sum(1 for t in range(T + 1) if ll[t] != lc[t])
    ib = sum(1 for t in range(T) if cc[t + 1] != (ll[t] ^ (cc[t] | rr[t])))
    # Control C: what identity I actually tests.  Both models use zero initial data
    # off the origin, so c determines l and r outright; I holds iff c is the centre
    # column of the diagram grown from (..0, c_0, 0..).  Only two such c exist.
    def viol(cc):
        a = [(row >> 1) & 1 for row in driven_rhp(cc, T)]
        b = [(row >> 1) & 1 for row in driven_lhp(cc, T)]
        return sum(1 for t in range(T) if cc[t + 1] != (b[t] ^ (cc[t] | a[t])))
    zero = viol([0] * (T + 3))
    flips = []
    for pos in (100, 3000, 4000):
        d = list(cc)
        d[pos] ^= 1
        flips.append((pos, viol(d)))
    out.append(f"CONTROL C all-zero drive c = 0^inf (the other admissible centre "
               f"column): I-violations {zero}/{T}")
    out.append("CONTROL C true centre column with ONE bit flipped: "
               + ", ".join(f"t={pos} -> {v}/{T}" for pos, v in flips))
    out.append(f"CONTROL B driven models fed the TRUE centre column: "
               f"driven_rhp vs true r mismatches {mr}/{T + 1}, "
               f"driven_lhp vs true l mismatches {ml}/{T + 1}, "
               f"identity I on that driven pair {ib}/{T} violations")
    out.append(f"TOTALS over {tot['n']} drives: r|Z periodic {tot['rZ']}, l|Z periodic {tot['lZ']}, "
               f"l periodic {tot['l']}, drives satisfying identity I everywhere: {tot['clean']}")
    print("\n".join(out))


if __name__ == '__main__':
    main()
