"""Structural facts about Rule 30 backward dynamics, by exhaustive enumeration.

Three claims, each checked, none assumed:

 (1) FREE-BOUNDARY WINDOW PREIMAGE COUNT IS IDENTICALLY 4, for Rule 30 and for
     Rule 90 alike.  For a left-permutive ECA y[i] = x[i-1] XOR g(x[i],x[i+1]),
     a target segment y[0..W-1] constrains x[-1..W]; choosing x[W-1], x[W]
     freely determines every x[i-1] leftward from y[i].  So the count is 4^1
     ... exactly 4, with no dependence on y and no dependence on the rule.
     Checked by brute force over all 2^W targets and all 2^(W+2) sources.

 (2) RULE 30 IS INJECTIVE ON FINITELY SUPPORTED CONFIGURATIONS OF Z.
     Enumerate every configuration supported in a width-w window, apply one
     Rule 30 step, and count image collisions.  Register row 60's up-to-3
     preimages is a measurement on the ring Z_N; the lone-seed orbit is not on
     a ring.  Same enumeration for Rule 90 as the standing filter control.

 (3) CYCLIC PREIMAGE COUNT DOES BRANCH -- on Z_N, for Rule 30, reproducing
     row 60 -- and this branching is a property of the ring closure, not of
     the rule's local backward determination.  Reported for contrast so the
     (1)/(2) results cannot be misread as contradicting row 60.

Frame convention matches experiments/overnight-arms/common/rule30.py:
    Rule 30 step  b -> (b << 2) XOR ((b << 1) OR b)
    Rule 90 step  b -> (b << 2) XOR b
Both are conjugates of the true maps by a shift, so injectivity in the frame
is injectivity of the map.
"""

import json
import sys

F30 = lambda b: (b << 2) ^ ((b << 1) | b)  # noqa: E731
F90 = lambda b: (b << 2) ^ b  # noqa: E731

G = {30: lambda m, r: m | r, 90: lambda m, r: r}


def claim1_free_boundary(rule, W):
    """Brute-force: for every target y of length W, count x of length W+2 with
    y[i] = x[i] XOR g(x[i+1], x[i+2])."""
    g = G[rule]
    counts = {}
    for y in range(1 << W):
        counts[y] = 0
    for x in range(1 << (W + 2)):
        xs = [(x >> i) & 1 for i in range(W + 2)]
        y = 0
        for i in range(W):
            y |= (xs[i] ^ g(xs[i + 1], xs[i + 2])) << i
        counts[y] += 1
    vals = sorted(set(counts.values()))
    return {"rule": rule, "W": W, "distinct_counts": vals,
            "all_equal_4": vals == [4]}


def claim2_finite_support_injective(step, w):
    """All configs supported in [0,w): any image collisions?"""
    seen = {}
    collisions = []
    for b in range(1 << w):
        img = step(b)
        if img in seen:
            collisions.append((seen[img], b, img))
            if len(collisions) > 5:
                break
        else:
            seen[img] = b
    return collisions


def _transfer(rule, yi):
    g = G[rule]
    M = [[0] * 4 for _ in range(4)]
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                if (a ^ g(b, c)) == yi:
                    M[2 * a + b][2 * b + c] = 1
    return M


def _matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]


def cyclic_count(rule, word):
    P = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    for v in word:
        P = _matmul(P, _transfer(rule, v))
    return sum(P[i][i] for i in range(4))


def claim3_ring_branching(rule, N):
    """Distribution of cyclic preimage counts over all 2^N rings of size N."""
    dist = {}
    for y in range(1 << N):
        w = [(y >> i) & 1 for i in range(N)]
        n = cyclic_count(rule, w)
        dist[n] = dist.get(n, 0) + 1
    return {str(k): v for k, v in sorted(dist.items())}


def main():
    res = {}

    res["claim1_free_boundary_count"] = [
        claim1_free_boundary(rule, W) for rule in (30, 90) for W in (1, 2, 3, 4, 5)
    ]

    wmax = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    inj = []
    for name, step in (("rule30", F30), ("rule90", F90)):
        for w in range(1, wmax + 1):
            col = claim2_finite_support_injective(step, w)
            inj.append({"map": name, "support_width": w,
                        "configs": 1 << w, "collisions": len(col),
                        "injective": not col})
    res["claim2_finite_support_injectivity"] = inj

    res["claim3_ring_preimage_distribution"] = [
        {"rule": rule, "N": N, "count_histogram": claim3_ring_branching(rule, N)}
        for rule in (30, 90) for N in (3, 6, 9, 12, 14)
    ]

    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
