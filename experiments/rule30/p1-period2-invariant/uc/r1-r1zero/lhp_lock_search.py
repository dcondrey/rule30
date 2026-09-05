"""Kill test for (PIN-Pi): does the driven LHP ever satisfy the pin identity persistently under a periodic drive?

For every primitive word w of period 1..7, every phase, and prefixes (the lone-seed prefix of length 8 and
N random prefixes of length 24, seeded), simulate the LHP driven by c = prefix + w^inf to time T and count
pin violations (c_t = 1 and l_t != 1 + c_(t+1)) in the second half [T/2, T).  A run with zero violations in the
second half is a lock candidate; it is then extended to 8T and re-checked.  Any confirmed lock kills the lemma.
Also reports the violation rate per one-time (null: 1/2).
"""
import sys, random, time, itertools
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_columns

def lhp_run(c, T):
    """Return number of pin violations in [T//2, T), number of one-times there, and the min violation-free run length."""
    row = c[0]
    viol = 0
    ones = 0
    last_viol = -1
    for t in range(T):
        ct = row & 1
        if ct == 1:
            if t >= T // 2:
                ones += 1
            if ((row >> 1) & 1) != (1 ^ c[t + 1]):
                last_viol = t
                if t >= T // 2:
                    viol += 1
        row = ((row >> 1) ^ (row | (row << 1)) & ~1) | c[t + 1]
    return viol, ones, last_viol

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    pmax = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    out = [f"T={T} random prefixes per word={N} periods<={pmax}"]
    true_c = lone_seed_columns(64, [0])[0]
    words = []
    for p in range(1, pmax + 1):
        for bits in itertools.product([0, 1], repeat=p):
            w = list(bits)
            if 1 not in w:
                continue
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)   # all phases kept (no rotation canonicalisation)
    out.append(f"words (all phases, primitive, with at least one 1): {len(words)}")
    t0 = time.time()
    total_runs = 0
    lock_candidates = []
    rate_num = 0
    rate_den = 0
    worst = (T, None)   # smallest 'last violation' time seen, i.e. longest violation-free tail
    for w in words:
        p = len(w)
        prefixes = [true_c[:8]] + [[random.Random(7919 * seed + p).getrandbits(1) for _ in range(24)] for seed in range(N)]
        for prefix in prefixes:
            L = len(prefix)
            c = prefix + [w[(t - L) % p] for t in range(L, T + 2)]
            c[0] = 1
            viol, ones, last_viol = lhp_run(c, T)
            total_runs += 1
            rate_num += viol
            rate_den += ones
            if ones > 0 and viol == 0:
                lock_candidates.append((''.join(map(str, w)), ''.join(map(str, prefix)), last_viol))
            if ones > 0 and last_viol < worst[0]:
                worst = (last_viol, (''.join(map(str, w)), ''.join(map(str, prefix))))
    out.append(f"runs={total_runs} second-half violation rate per one-time = {rate_num/max(rate_den,1):.4f} (null 0.5)")
    out.append(f"earliest last-violation time over all runs (longest violation-free tail): t={worst[0]} for {worst[1]}  (tail length {T - worst[0]})")
    out.append(f"lock candidates (zero violations in [T/2,T)): {len(lock_candidates)}")
    for w, prefix, last in lock_candidates[:20]:
        # confirm at 8T
        p = len(w)
        wl = [int(ch) for ch in w]
        pl = [int(ch) for ch in prefix]
        L = len(pl)
        T8 = 8 * T
        c = pl + [wl[(t - L) % p] for t in range(L, T8 + 2)]
        c[0] = 1
        viol, ones, last_viol = lhp_run(c, T8)
        out.append(f"   candidate w={w} prefix={prefix}: last violation at t={last} (T={T}); at 8T: violations in second half={viol}, last violation t={last_viol}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
