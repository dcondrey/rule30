"""PIN-tree search, version 2: wall location versus L, with controls.

Same as pin_survival.py but: full failure-time histogram near the maximum; tails may be
'1' (constant one, proved wall), 'R<seed>' (pseudo-random tail of length cap, shared by all leaves),
or a periodic word.  Survival counts steps past L until the first pin failure.
"""
import sys, time, random
from collections import Counter

def lhp_step(row, ct1):
    nxt = (row >> 1) ^ (row | (row << 1))
    return (nxt & ~1) | ct1

def tail_survival(row, tail, cap):
    """tail[k] = c_(L+k), tail[0] must equal row & 1."""
    for k in range(cap):
        ct = row & 1
        ct1 = tail[k + 1]
        if ct == 1:
            if ((row >> 1) & 1) != (1 ^ ct1):
                return k
        row = lhp_step(row, ct1)
    return cap

def leaves_at(L):
    leaves = []
    stack = [(1, 0)]
    while stack:
        row, t = stack.pop()
        if t == L:
            leaves.append(row)
            continue
        if row & 1:
            stack.append((lhp_step(row, 1 ^ ((row >> 1) & 1)), t + 1))
        else:
            stack.append((lhp_step(row, 0), t + 1))
            stack.append((lhp_step(row, 1), t + 1))
    return leaves

def main():
    Ls = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [8, 12, 16, 20, 24, 28, 32]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    specs = sys.argv[3].split(',') if len(sys.argv) > 3 else ["01", "0001", "011", "1", "R1", "R2"]
    out = [f"Ls={Ls} cap={cap} tails={specs}"]
    t0 = time.time()
    for L in Ls:
        leaves = leaves_at(L)
        out.append(f"L={L}: Pi-leaves={len(leaves)}")
        for spec in specs:
            if spec.startswith('R'):
                rng = random.Random(int(spec[1:]))
                base = [rng.getrandbits(1) for _ in range(cap + 2)]
                tails = [base]          # tail[0] will be overridden to match the leaf
                free0 = True
            else:
                w = [int(ch) for ch in spec]
                tails = [[w[(ph + k) % len(w)] for k in range(cap + 2)] for ph in range(len(w))]
                free0 = False
            hist = Counter()
            n = 0
            for row in leaves:
                for tail in tails:
                    if free0:
                        tail = [row & 1] + tail[1:]
                    elif tail[0] != (row & 1):
                        continue
                    s = tail_survival(row, tail, cap)
                    hist[s] += 1
                    n += 1
            mx = max(hist)
            top = sorted(hist.items())[-8:]
            # survivors >= s for a few s
            tot = n
            surv = {}
            cum = 0
            for s in sorted(hist):
                surv[s] = tot - cum
                cum += hist[s]
            marks = [s for s in (4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64) if s <= mx]
            out.append(f"  tail {spec}: tests={n} max={mx} atcap={hist[cap]} | fail-time hist (top): {top} | survivors>=s: "
                       + " ".join(f"{s}:{sum(v for k, v in hist.items() if k >= s)}" for s in marks))
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
