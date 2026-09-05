"""TEST 2 (Pi-tree search) for (PIN-Pi), streaming and parallel.

DFS over pin-consistent prefixes from row = 1 at t = 0 (lone seed): if bit 0 = 1 the next symbol is forced to
1 XOR bit 1, else branch on both symbols.  At every leaf at depth L attach every phase of each periodic tail
w^inf whose first symbol matches bit 0 and count steps to the first pin violation, cap C.
FAILURE (kills the lemma) = any leaf reaching the cap.  Reports the full fail-time histogram per tail, the
maximum, the number at cap, and the null (log2 of tests, in one-times, converted to steps by period/ones).

usage: pin_tree.py L cap tails(comma) [workers] [split_depth]
"""
import sys, time, math
from collections import Counter
from multiprocessing import get_context
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-screen-pin-pi-no-periodic')
from lhp_lib import lhp_step, tail_survival, periodic_tail

SPECS = None
L = None
CAP = None

def subtree_leaves(row, t, L):
    stack = [(row, t)]
    while stack:
        row, t = stack.pop()
        if t == L:
            yield row
            continue
        if row & 1:
            stack.append((lhp_step(row, 1 ^ ((row >> 1) & 1)), t + 1))
        else:
            stack.append((lhp_step(row, 0), t + 1))
            stack.append((lhp_step(row, 1), t + 1))

def work(args):
    row0, t0 = args
    tails = {}
    for spec in SPECS:
        w = [int(ch) for ch in spec]
        tails[spec] = [(ph, periodic_tail(w, ph, CAP + 2)) for ph in range(len(w))]
    hists = {spec: Counter() for spec in SPECS}
    best = {spec: (-1, None, None) for spec in SPECS}
    nleaves = 0
    for row in subtree_leaves(row0, t0, L):
        nleaves += 1
        b0 = row & 1
        for spec, tl in tails.items():
            h = hists[spec]
            for ph, tail in tl:
                if tail[0] != b0:
                    continue
                s = tail_survival(row, tail, CAP)
                h[s] += 1
                if s > best[spec][0]:
                    best[spec] = (s, row, ph)
    return nleaves, hists, best

def main():
    global SPECS, L, CAP
    L = int(sys.argv[1])
    CAP = int(sys.argv[2])
    SPECS = sys.argv[3].split(',')
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    split = int(sys.argv[5]) if len(sys.argv) > 5 else min(20, L)
    out = [f"L={L} cap={CAP} tails={SPECS} workers={workers} split_depth={split}"]
    t0 = time.time()
    roots = [(r, split) for r in subtree_leaves(1, 0, split)]
    out.append(f"subtree roots at depth {split}: {len(roots)}")
    tot_leaves = 0
    hists = {spec: Counter() for spec in SPECS}
    best = {spec: (-1, None, None) for spec in SPECS}
    with get_context('fork').Pool(workers) as pool:
        for nl, h, b in pool.imap_unordered(work, roots, chunksize=max(1, len(roots) // (workers * 8))):
            tot_leaves += nl
            for spec in SPECS:
                hists[spec].update(h[spec])
                if b[spec][0] > best[spec][0]:
                    best[spec] = b[spec]
    out.append(f"L={L}: Pi-leaves={tot_leaves}")
    for spec in SPECS:
        h = hists[spec]
        n = sum(h.values())
        mx = max(h) if h else 0
        w = [int(ch) for ch in spec]
        ones_per_step = sum(w) / len(w)
        null_steps = math.log2(max(n, 2)) / ones_per_step
        top = sorted(h.items())[-8:]
        marks = [s for s in (4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64, 96, 128) if s <= mx]
        surv = " ".join(f"{s}:{sum(v for k, v in h.items() if k >= s)}" for s in marks)
        bs, brow, bph = best[spec]
        out.append(f"  tail {spec}: tests={n} max={mx} atcap={h[CAP]} null_max_steps~{null_steps:.0f} ratio max/null={mx/null_steps:.2f} | top hist {top} | survivors>=s: {surv} | witness row=0x{brow:x} phase={bph}")
    out.append(f"elapsed {time.time()-t0:.1f}s")
    print("\n".join(out))

if __name__ == '__main__':
    main()
