"""PIN-tree search: can an eventually periodic word satisfy the pin identity in the driven LHP forever?

Pi = { c : the left half-plane driven by c (zero initial data on x <= -1, s(t,0) = c_t) satisfies
        l_t = 1 + c_(t+1) at every t with c_t = 1 }.
The lone-seed trace is in Pi (it is the Rule 30 rule at x = 0 with c_t = 1).  In Pi, c_(t+1) is
forced when c_t = 1 and free when c_t = 0, so Pi is a tree branching at zeros.

Search: DFS over Pi-paths u of length L; at each leaf attach the tail w^inf (every rotation of w)
and count how many steps the pin survives past L.  Null: each 1-time is a fair coin, so the max over
N leaves is about log2(N) one-times.  A leaf surviving far beyond that kills the lemma
"Pi contains no eventually periodic word with infinitely many ones".
"""
import sys, time
from collections import Counter

def lhp_step(row, ct1):
    # bit i holds s(t, -i); bit 0 = c_t.  new[i] = old[i+1] XOR (old[i] OR old[i-1]) for i >= 1.
    nxt = (row >> 1) ^ (row | (row << 1))
    return (nxt & ~1) | ct1

def tail_survival(row, t, tail, phase, cap):
    """row = LHP row at time t with bit0 = c_t (already set to tail value).  Run the tail until the
    first pin failure or cap steps; return steps survived (cap if none)."""
    p = len(tail)
    for k in range(cap):
        ct = row & 1
        ct1 = tail[(phase + k + 1) % p]
        if ct == 1:
            l = (row >> 1) & 1
            if l != (1 ^ ct1):
                return k
        row = lhp_step(row, ct1)
    return cap

def main():
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    words = sys.argv[3].split(',') if len(sys.argv) > 3 else ["01", "001", "011", "0001", "0111", "00101"]
    out = [f"L={L} cap={cap} words={words}"]
    t0 = time.time()
    # DFS over Pi-paths: state (row, t).  c_0 = 1: row = 1 at t = 0.
    # At time t with bit0 = c_t: if c_t = 1 the next symbol is forced 1 + l_t; else branch.
    leaves = []
    stack = [(1, 0)]
    while stack:
        row, t = stack.pop()
        if t == L:
            leaves.append(row)
            continue
        ct = row & 1
        if ct == 1:
            l = (row >> 1) & 1
            stack.append((lhp_step(row, 1 ^ l), t + 1))
        else:
            stack.append((lhp_step(row, 0), t + 1))
            stack.append((lhp_step(row, 1), t + 1))
    out.append(f"Pi-tree leaves at depth {L}: {len(leaves)} (log2 = {len(leaves).bit_length() - 1})")
    for w in words:
        tail = [int(ch) for ch in w]
        p = len(tail)
        hist = Counter()
        best = (-1, None, None)
        n_tests = 0
        for row in leaves:
            for phase in range(p):
                # the leaf row has bit0 = c_L already chosen by the DFS; the tail must start with that symbol
                if tail[phase] != (row & 1):
                    continue
                s = tail_survival(row, L, tail, phase, cap)
                n_tests += 1
                hist[s] += 1
                if s > best[0]:
                    best = (s, row, phase)
        ones_in_tail = sum(tail) / p
        # null: number of one-times in s steps is about s * ones_in_tail; survival prob 2^-(one-times)
        exp_max_onetimes = (n_tests).bit_length() - 1
        out.append(f"word {w}: tests={n_tests} max survival={best[0]} steps "
                   f"(~{best[0] * ones_in_tail:.1f} one-times; null max ~{exp_max_onetimes} one-times ~ {exp_max_onetimes / max(ones_in_tail, 1e-9):.0f} steps); "
                   f"reached cap: {hist[cap]}")
        tot = sum(hist.values())
        cum = 0
        line = []
        for s in sorted(hist):
            cum += hist[s]
            if s % max(1, p) == 0 or s == best[0]:
                line.append(f"{s}:{tot - cum + hist[s]}")
        out.append(f"   survivors >= s (s multiples of p): {' '.join(line[:40])}")
        if best[1] is not None:
            # print the prefix word of the best leaf by re-deriving is costly; print its LHP row bits instead
            out.append(f"   best leaf: phase={best[2]} row_bits(len)={best[1].bit_length()}")
    out.append(f"elapsed {time.time() - t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
