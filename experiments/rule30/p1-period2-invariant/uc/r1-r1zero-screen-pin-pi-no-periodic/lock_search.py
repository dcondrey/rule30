"""TEST 1 (lock search) for (PIN-Pi), corrected kernel.

For every primitive word w of period 1..pmax in every phase, and for prefixes = the lone-seed centre column
prefix of length 8 plus N random prefixes of length 24 (random.Random(7919*s + p), matching the earlier
scripts), simulate the left half-plane driven by c = prefix + w^inf from initial data y and count pin
violations in [T/2, T). A candidate with zero violations there is extended to 8T;
the follow-up checks [4T, 8T). These are late-window candidates, not all-time
pin-compatible witnesses or counterexamples to an infinite-time statement.
Also with random finite left data y (width ywidth, K per word) when --ywidth > 0.

The earlier lhp_lock_search.py (logs lhp_lock_search_T2048.log, lhp_lock_search_T8192_p4.log) has an operator
precedence bug in its update (`a ^ b & ~1` parses as `a ^ (b & ~1)`), so its bit 0 was s(t,-1) OR c_(t+1)
instead of c_(t+1); those two logs simulate a different drive than the one the pin was checked against.
This script uses lhp_lib.lhp_step, gated in gate.py.

Coverage correction 2026-09-15: the zero-initial random-prefix branch formerly recreated
Random(seed) for every bit, producing only constant prefixes. Historical ywidth=0 logs
retain their actual narrow coverage; they are not results of the corrected sampler.

usage: lock_search.py T N pmax [ywidth K]
"""
import sys, random, time, math
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-screen-pin-pi-no-periodic')
from r1zero_lib import lone_seed_columns
from lhp_lib import lhp_step, primitive_words, wstr

def random_prefix(sample, period, length=24):
    """A reproducible word from one generator advanced across all its bits."""
    rng = random.Random(7919 * sample + period)
    return [rng.getrandbits(1) for _ in range(length)]

def lhp_run(row, c, T):
    """Return (violations in [T/2,T), one-times in [T/2,T), time of last violation, longest violation-free
    gap between consecutive one-times' violations measured in one-times, total violations, total ones)."""
    viol = ones = 0
    tviol = tones = 0
    last_viol = -1
    ones_since = 0
    max_gap = 0
    half = T // 2
    for t in range(T):
        if row & 1:
            tones += 1
            if t >= half:
                ones += 1
            if ((row >> 1) & 1) != (1 ^ c[t + 1]):
                last_viol = t
                tviol += 1
                if t >= half:
                    viol += 1
                if ones_since > max_gap:
                    max_gap = ones_since
                ones_since = 0
            else:
                ones_since += 1
        row = lhp_step(row, c[t + 1])
    if ones_since > max_gap:
        max_gap = ones_since
    return viol, ones, last_viol, max_gap, tviol, tones

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    pmax = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    ywidth = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    K = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    out = [f"T={T} random prefixes per word={N} periods<={pmax} ywidth={ywidth} K={K}"]
    true_c = lone_seed_columns(64, [0])[0]
    words = primitive_words(pmax)
    out.append(f"words (all phases, primitive, at least one 1): {len(words)}")
    t0 = time.time()
    total_runs = 0
    candidates = []
    rate_num = rate_den = 0
    tv = to = 0
    worst = (T, None)
    gap_max = (0, None)
    for w in words:
        p = len(w)
        if ywidth == 0:
            cases = [(1, true_c[:8])] + [(1, random_prefix(s, p)) for s in range(N)]
        else:
            cases = []
            for s in range(K):
                rng = random.Random(104729 * s + p)
                y = rng.getrandbits(ywidth) | 1        # bit 0 is overwritten by the prefix's first symbol below
                prefix = [rng.getrandbits(1) for _ in range(16)]
                cases.append((y, prefix))
        for y, prefix in cases:
            L = len(prefix)
            c = prefix + [w[(t - L) % p] for t in range(L, 8 * T + 2)]
            c[0] = 1
            row = (y & ~1) | c[0]
            viol, ones, last_viol, max_gap, tviol, tones = lhp_run(row, c, T)
            total_runs += 1
            rate_num += viol
            rate_den += ones
            tv += tviol
            to += tones
            tag = (wstr(w), wstr(prefix), y)
            if ones > 0 and viol == 0:
                r8 = lhp_run(row, c, 8 * T)
                candidates.append((tag, last_viol, r8))
            if ones > 0 and last_viol < worst[0]:
                worst = (last_viol, tag)
            if max_gap > gap_max[0]:
                gap_max = (max_gap, tag)
    out.append(f"runs={total_runs} second-half violation rate per one-time={rate_num/max(rate_den,1):.4f} (null 0.5); all-time rate={tv/max(to,1):.4f} over {to} one-times")
    out.append(f"longest violation-free tail: last violation at t={worst[0]} (tail length {T-worst[0]}) for {worst[1]}")
    out.append(f"longest violation-free run of one-times anywhere in [0,T): {gap_max[0]} one-times for {gap_max[1]}; null expectation log2(total one-times)={math.log2(max(to,2)):.1f}")
    out.append(f"lock candidates (zero violations in [T/2,T)): {len(candidates)}")
    for tag, last, r8 in candidates:
        out.append(f"   candidate {tag}: last violation t={last} at T; at 8T violations in second half={r8[0]}, last violation t={r8[2]}")
    confirmed = [c for c in candidates if c[2][0] == 0]
    out.append(f"LATE-WINDOW SURVIVORS (no violations in [4T,8T); finite candidates only): {len(confirmed)}")
    out.append(f"elapsed {time.time()-t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
