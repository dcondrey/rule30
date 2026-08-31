"""
Fixed-output-length accumulation test (replaces the informal depth-2/3 check
that compared image size against a shrinking denominator 2^(n-d), which the
advisor correctly flagged as reading the yardstick rather than the image).

Design, to make counts directly comparable across depth:
  - Fix the OUTPUT length L (the length of the reconstructed column we
    actually measure).
  - For each depth d = 1..D, enumerate INPUT length n = L + d (since each
    leftward step consumes one time step).
  - col_0 (the assumed periodic centre) is exactly p-periodic over [0,n).
  - col_1 obeys its own light-cone wedge: col_1(t) = 0 for t < 1, free for
    t >= 1.
  - Chain the inverse map d times to reach col_{-d}.
  - CRITICAL FIX over the earlier version: every intermediate reconstructed
    column col_{-k} (k=1..d) must itself satisfy seed-compatibility
    (col_{-k}(t) = 0 for t < k) -- this is the actual light-cone condition
    for a ray descended from the lone seed, and it was missing before. Chains
    that violate it at any level are discarded (they are not elements of R).
  - Truncate col_{-d} to its first L admissible entries (t = d .. d+L-1,
    which is exactly L values) and count DISTINCT such length-L words across
    all surviving (col_0, col_1) pairs.

Same L at every d means the counts are on a common yardstick: if compression
accumulates with depth, this count must fall monotonically in d. If it is a
one-column boundary artifact, the count should be flat (or its ratio to the
number of surviving chains flat) from d=2 on.
"""
from __future__ import annotations
import itertools

def periodic_word(n: int, base):
    p = len(base)
    return tuple(base[t % p] for t in range(n))

def admissible_column0_words(n: int, p: int):
    words = set()
    for base in itertools.product([0, 1], repeat=p):
        words.add(periodic_word(n, base))
    return sorted(words)

def admissible_column1_words(n: int):
    return [(0,) + fb for fb in itertools.product([0, 1], repeat=n - 1)]

def inv30(cen, right, n):
    return tuple(cen[t + 1] ^ (cen[t] | right[t]) for t in range(n - 1))

def inv90(cen, right, n):
    return tuple(cen[t + 1] ^ right[t] for t in range(n - 1))

def wedge_ok(col, k):
    """col is indexed from t=0; representing col_{-k}, so it must be 0 for
    t < k (light cone: |x|<=t)."""
    for t in range(min(k, len(col))):
        if col[t] != 0:
            return False
    return True

def measure(rule: str, L: int, p: int, Dmax: int):
    inv = inv30 if rule == "30" else inv90
    results = []
    for d in range(1, Dmax + 1):
        n = L + d
        w_words = admissible_column0_words(n, p)
        c1_words = admissible_column1_words(n)
        survivors = 0
        outputs = set()
        for w in w_words:
            for c1 in c1_words:
                cen, right = w, c1
                ok = True
                for k in range(1, d + 1):
                    m = inv(cen, right, len(cen))
                    if not wedge_ok(m, k):
                        ok = False
                        break
                    right = cen[:len(m)]
                    cen = m
                if not ok:
                    continue
                # cen is now col_{-d}, length n-d = L; its first index t=0
                # corresponds to true time t=d in the original frame, so the
                # wedge for t<d has already been enforced above; take the
                # remaining L admissible entries as-is (already length L).
                survivors += 1
                outputs.add(cen)
        results.append((d, len(w_words) * len(c1_words), survivors, len(outputs)))
    return results

if __name__ == "__main__":
    print("=== Fixed-output-length accumulation test ===")
    print("Same yardstick L at every depth d; pairs = raw (w,c1) combos before")
    print("the seed-compatibility (wedge) filter on every intermediate column;")
    print("survivors = pairs that pass the wedge filter at every depth up to d;")
    print("distinct = number of distinct length-L outputs among survivors.")
    print()
    for L in (8, 10):
        for rule in ("30", "90"):
            for p in (1, 2):
                print(f"--- rule={rule} p={p} L={L} ---")
                print(f"{'d':<3}{'raw_pairs':<11}{'survivors':<11}{'distinct':<10}{'distinct/survivors':<20}{'distinct/2^L':<14}")
                res = measure(rule, L, p, 5)
                for d, raw, surv, dist in res:
                    ratio = dist / surv if surv else float("nan")
                    frac_full = dist / (2 ** L)
                    print(f"{d:<3}{raw:<11}{surv:<11}{dist:<10}{ratio:<20.4f}{frac_full:<14.4f}")
                print()
