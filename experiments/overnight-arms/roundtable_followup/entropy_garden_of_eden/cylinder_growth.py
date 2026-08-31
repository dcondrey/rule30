"""
Steps 2-4: precise subshift R, cylinder-count evidence for the entropy-drop
claim, and the Rule 90 screen.

Setup (see RESULTS doc section 2 for the justification of this exact
formalization, and where/why the literal panel wording had to be fixed):

A "light-cone ray of depth D, length n" is a binary matrix
  b[x][t],  x = 0..D,  t = 0..n-1
subject to the ONLY structural constraint the lone seed imposes at this
truncation: b[x][t] = 0 whenever x > t (light cone from a single seed at
x=0,t=0 travels at speed <=1). This is exactly the "one-sided subshift of
light-cone rays, support in [0,t]" from the panel's P1, restricted to a
finite window (x in [0,D], t in [0,n)) because that is the only way the
phrase "topological entropy" can be given a computable meaning here (see
finding 2 below).

R(D,n) = the set of all such matrices. |R(D,n)| = 2^(number of free cells)
where free cells are {(x,t): 0<=x<=D, x<=t<=n-1}. This is a clean,
combinatorial, non-asymptotic stand-in for "cylinder sets of R of length n"
at fixed depth D. Growth of log2|R(D,n)| in n, per unit depth D, is exactly
the "entropy of R" the proposal needs -- and it is manifestly full (rate 1
bit/cell up to the wedge deficit), independent of the rule. That is the
entropy of the *undetermined* ray ensemble, before any dynamics or
periodicity is imposed.

T_w(R) restricted to this window: apply the INV formula for the given rule,
LEFTWARD, from column D down to column 0, to reconstruct column x=-1 (using
columns 0 and 1), i.e. treat b[0] as the assumed eventually-periodic center
w and b[1] as the free right neighbour data, and compute what col_{-1} comes
out as. We then measure, among all 2^(free cells) elements of R(D,n):
  - how many have column 0 (b[0][0..n-1]) exactly period-p (this is a
    property of the input alone, not of T_w -- it is the domain slice R_w
    the map is restricted to), and
  - among THOSE, how many distinct column x=-1 traces arise as output
    (the image size |T_w(R_w)| at this cylinder length), which is the
    quantity whose growth rate is the actual "entropy of the image."

If the image count grows strictly slower (sub-exponentially relative to the
domain slice, or with a strictly smaller exponential base) than the domain
slice itself, that IS a measured entropy drop, in the same sense rung1
measured "R^2.75 bisimulation classes against 4^R raw states." If the growth
rates match, there is no drop at this cylinder length.

This script measures, for Rule 30 and Rule 90, at small n and p in {1,2}:
  (i) |R_w(n)| = number of length-n column-0 words that are exactly p-periodic
      and light-cone-admissible (only the p=1 all-zero/all-one and general
      p-periodic words starting appropriately -- see code),
  (ii) for each such w and each admissible right-neighbour column b[1],
       the resulting col_{-1}, collected into a set (dedup), giving the
       image size,
  (iii) the ratio image_size / (number of admissible (w,b1) pairs), i.e.
       how much the map compresses -- this is the direct empirical
       entropy-drop measurement, done fresh in THIS directory (independent
       of, but consistent with, the ladder machinery in
       experiments/rule30/ladder/).
"""
from __future__ import annotations
import itertools

def admissible_column0_words(n: int, p: int):
    """All length-n binary words w with w[t]=0 for t< (light cone at x=0 is
    always active, x=0<=t for all t>=0, so no wedge constraint on column 0
    itself) that are exactly periodic with period dividing p (i.e. w[t] =
    w[t mod p] for all t) -- both phases / all base words of length p."""
    words = []
    for base in itertools.product([0, 1], repeat=p):
        w = [base[t % p] for t in range(n)]
        words.append(tuple(w))
    # dedupe (different bases can coincide if base isn't primitive, fine)
    return sorted(set(words))


def admissible_column1_words(n: int):
    """Column 1's light-cone constraint: b[1][t] = 0 for t < 1, free for
    t>=1. Enumerate all such words (2^(n-1) of them)."""
    out = []
    for free_bits in itertools.product([0, 1], repeat=n - 1):
        w = (0,) + free_bits
        out.append(w)
    return out


def inv_rule30(col0, col1, n):
    # need col0[t+1], so usable range is t=0..n-2
    return tuple(col0[t + 1] ^ (col0[t] | col1[t]) for t in range(n - 1))


def inv_rule90(col0, col1, n):
    return tuple(col0[t + 1] ^ col1[t] for t in range(n - 1))


def measure(rule: str, n: int, p: int):
    inv = inv_rule30 if rule == "30" else inv_rule90
    w_words = admissible_column0_words(n, p)
    c1_words = admissible_column1_words(n)
    total_pairs = 0
    images = set()
    for w in w_words:
        for c1 in c1_words:
            total_pairs += 1
            out = inv(w, c1, n)
            images.add(out)
    domain_size = total_pairs
    image_size = len(images)
    # Also: the UNCONSTRAINED baseline -- domain slice if column 0 were free
    # (not periodicity-restricted) instead of forced p-periodic, i.e. the
    # ambient R(D=1,n) cylinder count, for the "entropy of R" comparison.
    ambient_c0 = 2 ** n  # column 0 has no wedge constraint (x=0<=t always)
    ambient_pairs = ambient_c0 * len(c1_words)
    return {
        "rule": rule, "n": n, "p": p,
        "num_w_words": len(w_words),
        "num_c1_words": len(c1_words),
        "domain_pairs": domain_size,
        "image_size": image_size,
        "compression_ratio": image_size / domain_size if domain_size else float("nan"),
        "ambient_pairs": ambient_pairs,
    }


if __name__ == "__main__":
    print("=== Steps 2-4: cylinder-count entropy-drop measurement ===")
    print()
    print("MEASURED, not proved. Finite n, finite p. Sample sizes given inline.")
    print()
    header = f"{'rule':<5}{'p':<3}{'n':<4}{'#w':<5}{'#c1':<7}{'domain':<9}{'image':<8}{'ratio':<10}{'ambient':<10}"
    print(header)
    print("-" * len(header))
    rows = []
    for rule in ("30", "90"):
        for p in (1, 2):
            for n in (4, 6, 8, 10, 12):
                r = measure(rule, n, p)
                rows.append(r)
                print(f"{r['rule']:<5}{r['p']:<3}{r['n']:<4}{r['num_w_words']:<5}"
                      f"{r['num_c1_words']:<7}{r['domain_pairs']:<9}{r['image_size']:<8}"
                      f"{r['compression_ratio']:<10.4f}{r['ambient_pairs']:<10}")
    print()
    print("Growth-rate check: fit image_size ~ C * base^n per (rule,p),")
    print("compare base to 2 (the per-cell entropy of an uncompressed column).")
    import math
    print()
    for rule in ("30", "90"):
        for p in (1, 2):
            sub = [r for r in rows if r["rule"] == rule and r["p"] == p]
            ns = [r["n"] for r in sub]
            ys = [math.log2(r["image_size"]) for r in sub]
            # simple slope estimate between consecutive points (n step = 2)
            slopes = [(ys[i+1]-ys[i])/(ns[i+1]-ns[i]) for i in range(len(ns)-1)]
            print(f"rule={rule} p={p}: log2(image_size) per-n slopes = "
                  + ", ".join(f"{s:.3f}" for s in slopes))
