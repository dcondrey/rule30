"""
Advisor-requested robustness check: does letting the RIGHT half vary too
(existential quantification over some completion, not pinning it to the true
seed) change the node-count/forest conclusions in compat_graph.py?

Node at level k (free-right variant): a left-half word w in {0,1}^k such
that THERE EXISTS a right-half word v in {0,1}^k (cells 1..k; cells beyond
+-k are 0-padded, same don't-care argument as before) with s(0,0)=1 fixed,
such that evolving forward reproduces the TRUE centre a_0..a_{k-1}.

This is a strictly more permissive node set (fixing v = the true seed's
all-zero right half is one particular witness, so every node of the
original construction is still a node here). Brute force over both halves
for small k (numpy-vectorized) to see whether the graph stops being a
2-node-per-level broom once the right half is allowed to vary.
"""
import itertools
import numpy as np


def rule30_arr(a, b, c):
    return a ^ (b | c)


def rule90_arr(a, b, c):
    return a ^ c


RULES = {"rule30": rule30_arr, "rule90": rule90_arr}


def true_center(rule_name, T, halfwidth):
    rule = RULES[rule_name]
    width = 2 * halfwidth + 1
    mid = halfwidth
    row = np.zeros(width, dtype=np.uint8)
    row[mid] = 1
    center = []
    for t in range(T):
        center.append(int(row[mid]))
        new = np.zeros(width, dtype=np.uint8)
        new[1:-1] = rule(row[:-2], row[1:-1], row[2:])
        row = new
    return center


def nodes_with_free_right(rule_name, k, halfwidth=None):
    """Enumerate all left-half words w (len k) for which SOME right-half
    word v (len k) yields a_0..a_{k-1} matching truth. Vectorized over all
    2^k x 2^k combined ICs at once."""
    rule = RULES[rule_name]
    if halfwidth is None:
        halfwidth = k + 5
    a_true = true_center(rule_name, k, halfwidth)
    width = 2 * halfwidth + 1
    mid = halfwidth

    lefts = np.array(list(itertools.product([0, 1], repeat=k)), dtype=np.uint8) if k > 0 else np.zeros((1, 0), dtype=np.uint8)
    rights = np.array(list(itertools.product([0, 1], repeat=k)), dtype=np.uint8) if k > 0 else np.zeros((1, 0), dtype=np.uint8)
    nL, nR = lefts.shape[0], rights.shape[0]

    # build all nL*nR combined ICs
    rows = np.zeros((nL * nR, width), dtype=np.uint8)
    rows[:, mid] = 1
    # left cells -1..-k -> index mid-1 .. mid-k
    for i in range(k):
        col = mid - (i + 1)
        rows[:, col] = np.repeat(lefts[:, i], nR)
    for i in range(k):
        col = mid + (i + 1)
        rows[:, col] = np.tile(rights[:, i], nL)

    ok = np.ones(nL * nR, dtype=bool)
    row = rows
    for t in range(k):
        center_col = row[:, mid]
        ok &= (center_col == a_true[t])
        new = np.zeros_like(row)
        new[:, 1:-1] = rule(row[:, :-2], row[:, 1:-1], row[:, 2:])
        row = new

    ok = ok.reshape(nL, nR)
    survivors_mask = ok.any(axis=1)  # exists some right completion
    survivor_lefts = [tuple(int(b) for b in lefts[i]) for i in range(nL) if survivors_mask[i]]
    return survivor_lefts, a_true


if __name__ == "__main__":
    for rn in ("rule30", "rule90"):
        print(f"=== {rn} (right half free) ===")
        for k in range(1, 9):
            survivors, a_true = nodes_with_free_right(rn, k)
            print(f"k={k}: {len(survivors)} survivors out of {2**k} candidates")
        print()
