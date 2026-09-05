"""(PIN-Pi) kill test with general finite left initial data y|_(x<=0) of width <= 12.

For each word w in the RHP-locking family and the period-two words (all phases), 150 random left data
(bits y(0), y(-1), ..., y(-11), with y(0) = c_0 forced to the word's first symbol if the prefix is empty),
drive c = w^inf directly (no prefix; PT2 needs exactly periodic traces) and c = random prefix (16) + w^inf.
T = 8192.  Report second-half pin-violation rate and lock candidates (zero violations in [T/2, T)).
"""
import sys, random, time
from collections import Counter

def lhp_run(row, c, T):
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
        row = (((row >> 1) ^ (row | (row << 1))) & ~1) | c[t + 1]
    return viol, ones, last_viol

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 8192
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    words = ["01", "10", "0001", "0010", "0100", "1000", "0011", "0110", "1100", "1001", "0111", "1110", "1101", "1011", "001", "010", "100"]
    out = [f"T={T} N={N} words={words}"]
    t0 = time.time()
    runs = 0
    num = 0
    den = 0
    cands = []
    longest_tail = (T, None)
    for w in words:
        wl = [int(ch) for ch in w]
        p = len(wl)
        for seed in range(N):
            rng = random.Random(100003 * seed + p * 31 + int(w, 2))
            ydata = [rng.getrandbits(1) for _ in range(12)]     # y(0), y(-1), ..., y(-11)
            if seed % 2 == 0:
                prefix = []
            else:
                prefix = [rng.getrandbits(1) for _ in range(16)]
            L = len(prefix)
            c = prefix + [wl[(t - L) % p] for t in range(L, T + 2)]
            ydata[0] = c[0]
            if all(v == 0 for v in ydata) and c[0] == 0:
                ydata[0] = 1
                c[0] = 1
            row = 0
            for i, v in enumerate(ydata):
                row |= v << i
            viol, ones, last = lhp_run(row, c, T)
            runs += 1
            num += viol
            den += ones
            if ones > 0 and viol == 0:
                cands.append((w, ''.join(map(str, ydata)), ''.join(map(str, prefix)), last))
            if ones > 0 and last < longest_tail[0]:
                longest_tail = (last, (w, ''.join(map(str, ydata)), ''.join(map(str, prefix))))
    out.append(f"runs={runs} second-half violation rate per one-time={num/max(den,1):.4f} lock candidates={len(cands)}")
    out.append(f"longest violation-free tail: from t={longest_tail[0]} (length {T - longest_tail[0]}) for {longest_tail[1]}")
    for cnd in cands[:10]:
        out.append(f"   candidate {cnd}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
