"""Triage the four proposed 'novel framework' arms against the two standing
PATH.md filters before any of them is built out.

PATH.md section 0.1 requires every proposed quantity to pass the single-column
sensitivity test: overwrite column 0 of the lone-seed diagram with a periodic
word, changing nothing else, and see whether the quantity moves by more than
O(1/W).  Section 0 requires it to fail for Rule 90.

Two of the four arms have a computable statistic and are run here:

  A2  Wasserstein W_1(mu_t, uniform) over k-blocks, Hamming cost, exact LP.
      Dropped into the discriminator harness (A = Rule 30, B = A with column 0
      overwritten by 0101..., C = Rule 90) plus the temporal contraction curve
      the arm's hypothesis asserts.
  A3  Exact GF(2) temporal-cut contraction rank of the backward lightcone, at
      the lone seed and over arbitrary inputs.
  A4  Exact subword complexity p(n) of the centre column for n <= 64, against
      the Morse-Hedlund threshold, with the period range it actually excludes.

A1 (Drinfeld modules) has no computable statistic to triage; it is closed on
algebraic grounds in TRIAGE-novel-frameworks.md.

PREDICTIONS, recorded before running:
  A2  |W1(A) - W1(B)| = O(1/W); column-blind; the positive control moves ~96%.
  A3  lone-seed cut rank identically 1 at every cut; arbitrary-input rank
      exponential, reproducing ARM8's ~1.88/step rather than adding to it.
  A4  p(n) > n for all n <= 64, which excludes only periods below ~64.
KILL CONDITIONS (would put an arm back in play): A2 moving more than O(1/W)
under the column-0 overwrite; A3 lone-seed rank exceeding 1; A4 p(n) <= n at
some n <= 64 (which would REFUTE P1's expected answer, not support it).

Run: uv run python experiments/overnight-arms/novel_frameworks/triage_probe.py
"""

from __future__ import annotations

import itertools
import json
import sys

import numpy as np
from scipy.optimize import linprog

FWD = {30: lambda l, m, r: l ^ (m | r), 90: lambda l, m, r: l ^ r}


def diagram(rule, T, B):
    w = 2 * B + 1
    row = np.zeros(w, dtype=np.uint8)
    row[B] = 1
    out = [row]
    for _ in range(T):
        p = out[-1]
        nxt = np.zeros(w, dtype=np.uint8)
        nxt[1:-1] = FWD[rule](p[:-2], p[1:-1], p[2:])
        out.append(nxt)
    return np.array(out)


def overwrite_centre(grid, B, word=(0, 1)):
    g = grid.copy()
    for t in range(g.shape[0]):
        g[t, B] = word[t % len(word)]
    return g


# ---------------------------------------------------------------- A2: W_1

def _hamming_cost(k):
    st = np.arange(1 << k)
    x = ((st[:, None] >> np.arange(k)) & 1).astype(np.int8)
    return (x[:, None, :] != x[None, :, :]).sum(-1).astype(float)


_COST_CACHE = {}


def w1_to_uniform(mu, k):
    """Exact W_1(mu, uniform) on {0,1}^k with Hamming cost, by LP."""
    if k not in _COST_CACHE:
        _COST_CACHE[k] = _hamming_cost(k)
    C = _COST_CACHE[k]
    n = 1 << k
    nu = np.full(n, 1.0 / n)
    # marginal constraints: sum_j P[i,j] = mu_i ; sum_i P[i,j] = nu_j
    rows, cols, vals = [], [], []
    for i in range(n):
        rows += [i] * n
        cols += list(range(i * n, (i + 1) * n))
        vals += [1.0] * n
    for j in range(n):
        rows += [n + j] * n
        cols += list(range(j, n * n, n))
        vals += [1.0] * n
    from scipy.sparse import coo_matrix
    A = coo_matrix((vals, (rows, cols)), shape=(2 * n, n * n))
    b = np.concatenate([mu, nu])
    res = linprog(C.ravel(), A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    return float(res.fun)


def block_hist(grid, B, W, t, k):
    half = W // 2
    seg = grid[t, B - half:B + half + 1].astype(np.int64)
    if seg.size < k:
        return None
    idx = np.zeros(seg.size - k + 1, dtype=np.int64)
    for j in range(k):
        idx += seg[j:seg.size - k + 1 + j] << j
    h = np.bincount(idx, minlength=1 << k).astype(float)
    return h / h.sum()


def s4_wasserstein(grid, B, W, k=5, samples=12):
    T = grid.shape[0]
    ts = np.linspace(T // 2, T - 1, samples).astype(int)
    vals = []
    for t in ts:
        mu = block_hist(grid, B, W, t, k)
        if mu is not None:
            vals.append(w1_to_uniform(mu, k))
    return float(np.mean(vals))


def s0_control(grid, B, W):
    c = grid[:, B]
    return float((c == (np.arange(c.size) % 2)).mean())


def a2_column_filter(T=400, k=5):
    B = T + 4
    A = diagram(30, T, B)
    Bg = overwrite_centre(A, B)
    C = diagram(90, T, B)
    assert (A != Bg).sum() == (A[:, B] != Bg[:, B]).sum()
    out = {"T": T, "k": k, "windows": []}
    for W in (32, 64, 128, 256):
        a, b, c = (s4_wasserstein(g, B, W, k) for g in (A, Bg, C))
        s0 = (s0_control(A, B, W), s0_control(Bg, B, W))
        out["windows"].append({
            "W": W,
            "W1_A_rule30": round(a, 8), "W1_B_col0_overwritten": round(b, 8),
            "W1_C_rule90": round(c, 8),
            "relAB": round(abs(a - b) / max(abs(a), 1e-12), 6),
            "relAC": round(abs(a - c) / max(abs(a), 1e-12), 6),
            "control_col0_A": round(s0[0], 6), "control_col0_B": round(s0[1], 6),
            "control_rel": round(abs(s0[0] - s0[1]) / max(s0[0], 1e-12), 6),
        })
    return out


def a2_contraction_curve(T=500, k=5, W=256):
    """The arm's actual hypothesis: does W_1(mu_t, uniform) strictly contract?"""
    B = T + 4
    curves = {}
    for rule in (30, 90):
        g = diagram(rule, T, B)
        ts = list(range(10, T, max(1, T // 25)))
        curves[str(rule)] = [
            {"t": int(t), "W1": round(w1_to_uniform(block_hist(g, B, W, t, k), k), 8)}
            for t in ts]
    # analytic kill: the all-zero configuration is a fixed point of both rules.
    zero = np.zeros(1 << k)
    zero[0] = 1.0
    curves["W1_delta_allzero_to_uniform"] = round(w1_to_uniform(zero, k), 8)
    curves["note"] = ("delta_allzero is F-invariant for every ECA with 000->0, "
                      "so F_* fixes it and no strict contraction of W_1 to "
                      "uniform can hold on the space of measures.")
    return curves


# ------------------------------------------- A3: temporal-cut contraction rank

def _step_row(bits):
    n = len(bits)
    return tuple(bits[(i - 1) % n] ^ (bits[i] | bits[(i + 1) % n]) for i in range(n))


def a3_cut_rank(dmax=12):
    """Exact contraction rank across the temporal cut of the backward lightcone.

    For a deterministic CA the tensor across a cut at height h is the 0/1 matrix
    M[input, layer-h state]; it has exactly one 1 per row, so its rank over any
    field equals the number of DISTINCT layer-h states reachable from the input
    set.  Two input sets:
      lone seed  -- the single-seed orbit, the object P1/P2/P3 are about;
      arbitrary  -- all 2^(2d+1) inputs to the depth-d lightcone.
    """
    out = {"lone_seed": [], "arbitrary_input": []}
    for d in range(1, dmax + 1):
        n = 2 * d + 1
        # lone seed: one input, so one state at every cut
        seed = tuple(1 if i == d else 0 for i in range(n))
        st = seed
        ranks = []
        for _ in range(d):
            st = _step_row(st)
            ranks.append(1)
        out["lone_seed"].append({"depth": d, "cut_ranks": ranks})
        if n <= 20:
            states = {tuple(int(b) for b in f"{v:0{n}b}") for v in range(1 << n)}
            ranks = []
            for _ in range(d):
                states = {_step_row(s) for s in states}
                ranks.append(len(states))
            out["arbitrary_input"].append({"depth": d, "n_vars": n, "cut_ranks": ranks})
    return out


# --------------------------------------------------- A4: subword complexity

def center_bits(n):
    row, out = 1, []
    for t in range(n):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row)
    return out


def a4_complexity(nmax=64, length=200000):
    c = center_bits(length)
    # validate against the fence-internal generator, itself validated against
    # the repo ground truth experiments/rule30/center_column.py.
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
    from common.rule30 import center_column_bits  # noqa: E402
    assert c[:5000] == center_column_bits(5000), "centre column mismatch"
    s = "".join(map(str, c))
    rows = []
    for n in range(1, nmax + 1):
        p = len({s[i:i + n] for i in range(len(s) - n + 1)})
        rows.append({"n": n, "p_n": p, "exceeds_n": p > n, "cap_2n": 1 << n})
    return {"prefix_length": length, "nmax": nmax, "rows": rows,
            "morse_hedlund": ("eventually periodic iff p(n) <= n for SOME n; "
                              "a word of eventual period q has p(n) <= q + preperiod "
                              "for all n, so p(n) > n on n <= 64 excludes only "
                              "periods in that range")}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    if which in ("all", "a2"):
        res["A2_column_filter"] = a2_column_filter()
        res["A2_contraction"] = a2_contraction_curve()
    if which in ("all", "a3"):
        res["A3_cut_rank"] = a3_cut_rank()
    if which in ("all", "a4"):
        res["A4_complexity"] = a4_complexity()
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
