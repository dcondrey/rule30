"""PRE-REGISTERED.  Is the RW survivor set an affine subspace of F_2^n once the
forced-symbol branch is fixed?

Motivation.  Every killed mechanism supplied a RATE.  A rate cannot give the
all-length quantifier because plateaus (ratio 1.0) exist at deep levels.  The
untried class is a DIMENSION count: if, along a fixed forced word
s_0..s_{j-1}, each level's E-condition is one affine equation over F_2 in the
source bits, the branch survivor set is an affine subspace, N_j is a sum of
2^(n-rank) over live branches, and N_j <= C 2^(n-j) reduces to independence of
j equations plus a branch count.

Test.  Sources W in {1,2}^n <-> F_2^n (bit i = 1 iff W[i] == 2).  Level-j
survivors are partitioned by their forced word.  A class A is an affine
subspace iff |A| is a power of two and x+y+z in A for all x,y,z in A.
(Equivalently A - a_0 is a linear subspace.)

Strong outcome: every class of size >= 4 is an affine subspace, at every
n, c, j.  Kill: classes fail affine closure at any level beyond noise, or
class sizes are not powers of two.  Either kills counting-by-F2-rank and
should be recorded next to the other killed mechanism classes.
"""
import sys
sys.path.insert(0,'/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant')
from itertools import product
from collections import defaultdict
from flip_pairing import census, E

def bits(src):
    v = 0
    for i, s in enumerate(src):
        if s == 2: v |= 1 << i
    return v

def is_affine(cl):
    m = len(cl)
    if m & (m-1): return False, "size not a power of 2"
    S = set(cl); a0 = cl[0]
    lin = {x ^ a0 for x in cl}
    for x in lin:
        for y in lin:
            if (x ^ y) not in lin:
                return False, "not closed"
    return True, ""

def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    for n in range(nmin, nmax+1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        srcs = [bits(s) for s in product((1,2), repeat=n)]
        for c in (2,3):
            ec = E(c)
            # survivors and their forced words
            print(f"# n={n} c={c}")
            classes = defaultdict(list)
            alive = list(range(1 << n))
            for j in range(levels):
                nxt = []
                for idx in alive:
                    if hcs[idx][j] and cells[idx][j] == c:
                        nxt.append(idx)
                alive = nxt
                if not alive: break
                by = defaultdict(list)
                for idx in alive:
                    by[tuple(syms[idx][:j+1])].append(srcs[idx])
                ok = bad = 0; sizes = []
                reasons = defaultdict(int)
                for w, cl in by.items():
                    if len(cl) < 4: continue
                    a, why = is_affine(cl)
                    sizes.append(len(cl))
                    if a: ok += 1
                    else: bad += 1; reasons[why] += 1
                print(f"  j={j:>2} N_j={len(alive):>7} branches={len(by):>6} "
                      f"testable={ok+bad:>5} affine={ok:>5} not-affine={bad:>5} "
                      f"{dict(reasons)} maxclass={max(sizes) if sizes else 0}")
                sys.stdout.flush()

main()
