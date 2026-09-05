"""Forward Rule 30 in (H, E) pair coordinates: exhaustive law check and diagonal integrals.

Pair cell at (t; x, x-1): H = s(t,x), Lo = s(t,x-1), E = 1 + H + Lo (mod 2).
Input pair at (t; x+2, x+1): H(l) = s(t,x+2), Lo(l) = s(t,x+1),
quotient letters a = [l == 0] = [s(t,x+1) = s(t,x+2) = 0], b = [Lo(l) = 0] = [s(t,x+1) = 0].
Claimed forward step along the diagonal (t; x, x-1) -> (t+1; x+1, x):
    H' = H + 1 + a
    E' = E + b * (H + H(l))      (equivalently E + b*H + b + a)
Then the diagonal integrals from the left edge give c_t, r_t, l_t as parities.
"""
import sys
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows

def rule30(l, c, r):
    return l ^ (c | r)

def main():
    out = []
    # 1. exhaustive law over the 4 cells s(t,x-1), s(t,x), s(t,x+1), s(t,x+2)
    bad = 0
    for bits in range(16):
        sxm1, sx, sx1, sx2 = (bits >> 3) & 1, (bits >> 2) & 1, (bits >> 1) & 1, bits & 1
        H, Lo = sx, sxm1
        E = (1 + H + Lo) & 1
        Hl, Lol = sx2, sx1
        a = int(sx1 == 0 and sx2 == 0)
        b = int(sx1 == 0)
        # forward cells: s(t+1,x+1) and s(t+1,x)
        nH = rule30(sx, sx1, sx2)
        nLo = rule30(sxm1, sx, sx1)
        nE = (1 + nH + nLo) & 1
        predH = (H + 1 + a) & 1
        predE = (E + b * ((H + Hl) & 1)) & 1
        predE2 = (E + b * H + b + a) & 1
        if nH != predH or nE != predE or nE != predE2:
            bad += 1
    out.append(f"exhaustive 16-case check of forward (H,E) law: failures = {bad}")

    # 2. diagonal integrals on the lone seed, T = 2000
    T = 2000
    rows = {}
    off = None
    for t, row, o in lone_seed_rows(T):
        rows[t] = row
        off = o
    def s(t, x):
        if t < 0 or t > T:
            raise IndexError
        return (rows[t] >> (off + x)) & 1
    # H-integral for diagonal k from time t0 to t1:
    # D_k(t1) = D_k(t0) + (t1 - t0) + #{t' in [t0,t1): D_{k+1}(t') = D_{k+2}(t') = 0}
    failH = 0
    failE = 0
    checksH = 0
    checksE = 0
    for t in range(2, T):
        # c_t = D_{-t}(t), integrate from t0 = 0 (D_{-t}(0) = 0 for t >= 1)
        k = -t
        cnt = 0
        for tp in range(0, t):
            if s(tp, tp + k + 1) == 0 and s(tp, tp + k + 2) == 0:
                cnt += 1
        pred = (0 + t + cnt) & 1
        checksH += 1
        if pred != s(t, 0):
            failH += 1
        # r_t = D_{1-t}(t): D_{1-t}(0) = [t == 1] = 0 for t >= 2
        k = 1 - t
        cnt = 0
        for tp in range(0, t):
            if s(tp, tp + k + 1) == 0 and s(tp, tp + k + 2) == 0:
                cnt += 1
        pred = (t + cnt) & 1
        checksH += 1
        if pred != s(t, 1):
            failH += 1
        # E-integral along the pair diagonal (k, k-1) with k = -t (pair (c_t, l_t)) from time 0:
        # E(t1) = E(0) + #{t': [D_{k+1}(t') = 0] * (D_k(t') + D_{k+2}(t'))}
        # at time 0 the pair is (0,0) so E(0) = 1.
        for k in (-t, 1 - t):
            cnt = 0
            for tp in range(0, t):
                if s(tp, tp + k + 1) == 0 and (s(tp, tp + k) != s(tp, tp + k + 2)):
                    cnt += 1
            pred = (1 + cnt) & 1
            actual = (1 + s(t, t + k) + s(t, t + k - 1)) & 1
            checksE += 1
            if pred != actual:
                failE += 1
    out.append(f"lone seed T={T}: H-integral checks={checksH} failures={failH}; E-integral checks={checksE} failures={failE}")

    # 3. r on the zero set as E of the crossing pair (r_t, c_t) at odd t and (c_t, l_t) at even t
    failZ = 0
    checksZ = 0
    for t in range(2, T):
        if s(t, 0) != 0:
            continue
        if t % 2 == 1:
            # pair (r_t, c_t) on diagonals (1-t, -t): E = 1 + r_t + 0 -> r_t = 1 + E
            k = 1 - t
            cnt = sum(1 for tp in range(0, t) if s(tp, tp + k + 1) == 0 and s(tp, tp + k) != s(tp, tp + k + 2))
            E = (1 + cnt) & 1
            pred = (1 + E) & 1
        else:
            # pair (c_t, l_t) on diagonals (-t, -t-1): E = 1 + 0 + l_t; r_t = c_{t+1} + l_t
            k = -t
            cnt = sum(1 for tp in range(0, t) if s(tp, tp + k + 1) == 0 and s(tp, tp + k) != s(tp, tp + k + 2))
            E = (1 + cnt) & 1
            l = (1 + E) & 1
            pred = (s(t + 1, 0) + l) & 1
        checksZ += 1
        if pred != s(t, 1):
            failZ += 1
    out.append(f"r on zero set via crossing-pair E-integral: checks={checksZ} failures={failZ}")
    # 4. the count is over the left half plane: report the range of x visited for one t
    t = 1001
    k = -t
    xs = [tp + k + 1 for tp in range(0, t)]
    out.append(f"for t={t}: the H-integral for c_t sums over x in [{min(xs)},{max(xs)}] (cells left of the centre; outside-cone cells contribute 1 each)")
    print("\n".join(out))

if __name__ == '__main__':
    main()
