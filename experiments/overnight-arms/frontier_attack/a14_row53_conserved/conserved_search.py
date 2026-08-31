"""Exhaustive search for conserved window functions of an ECA (row 53).

DEFINITION (made precise here; this is the object the register row names).
A *window function* of width w is a map phi: {0,1}^w -> K, K in {Q, Z/m}.
Its *aggregate* on a configuration s is the site sum

    Phi(s) = sum_x phi(s(x), s(x+1), ..., s(x+w-1)).

Phi is *conserved* by an ECA F on the class of SPATIALLY PERIODIC
configurations if, for every period p and every s of period p, the sum over
one period is unchanged by one step of F.  (This is the Hattori-Takesue /
Boccara-Fuks setting; on that class Phi is finite and well defined.  These
authors call the whole class "additive" because Phi is a site sum; the
register's "non-additive" means phi itself is not affine in the cells, and
both readings are answered below because the FULL solution space is computed.)

EXACT FINITE CHARACTERISATION (no bound guessing, no sampling).
Let n = w + 2.  For u in {0,1}^n read as s(x-1..x+w), define

    Lambda(u) = phi( F(s)(x..x+w-1) ) - phi( s(x..x+w-1) ),

a function of n cells only.  Then Phi(F(s)) - Phi(s) = sum_x Lambda(u_x).
Words of {0,1}^n are exactly the edges of the de Bruijn graph B(2, n-1) whose
vertices are words of length n-1; cyclic configurations are exactly its closed
walks.  An edge weighting has zero circulation on every closed walk iff it is a
potential difference.  Hence

    Phi conserved on ALL periodic configurations
      <=>  exists J: {0,1}^{n-1} -> K with
           Lambda(u) = J(u_0..u_{n-2}) - J(u_1..u_{n-1})  for all u in {0,1}^n.

That is a finite linear system in (phi, J), solved exactly below.  J is the
discrete current; the equation is the discrete continuity equation.  Because
de Bruijn graphs are connected, J is pinned by phi up to one constant, so
dim{phi conserved} = dim ker - 1.

TRIVIAL SUBSPACE (quotiented out before any claim of a find):
  * constants phi = c (1 dimension);
  * coboundaries phi(v) = g(v_0..v_{w-2}) - g(v_1..v_{w-1}), which make
    Phi identically 0 on every periodic configuration (2^{w-1} - 1 dims);
  * lifts of conserved width-(w-1) functions, phi(v) = psi(v_0..v_{w-2}),
    and their shifted twins psi(v_1..v_{w-1}).
A NEW conserved quantity at width w exists iff dim V_w > dim T_w, where T_w is
the span of the three families above.

Controls run in the same call: Rule 184 (proved number-conserving, so the
width-1 density MUST appear -- if it does not, the harness is broken),
Rule 90 (the repo's standing section-0 filter), Rule 30 (the target).

Run:  uv run python conserved_search.py --wmax 11 --primes 2147483647,1000003
"""

from __future__ import annotations

import argparse
import json
import time

import numpy as np

RULES = (30, 90, 184, 170, 204)


def rule_table(rule: int) -> np.ndarray:
    """t[l*4 + c*2 + r] = new centre cell, Wolfram numbering."""
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.int64)


def build_system(rule: int, w: int):
    """Rows of the (phi | J) linear system, dense int64 (entries in {-1,0,1}).

    Columns 0..2^w-1 are phi; columns 2^w..2^w+2^(n-1)-1 are J.
    One row per u in {0,1}^n, n = w+2.
    """
    n = w + 2
    tab = rule_table(rule)
    nu = 1 << n
    u = np.arange(nu, dtype=np.int64)
    # bit i of the word, i = 0 (leftmost, = s(x-1)) .. n-1
    bits = np.stack([(u >> (n - 1 - i)) & 1 for i in range(n)])

    # image window: cells f(u_i, u_{i+1}, u_{i+2}) for i = 0..w-1
    img = np.zeros(nu, dtype=np.int64)
    for i in range(w):
        nb = tab[bits[i] * 4 + bits[i + 1] * 2 + bits[i + 2]]
        img = (img << 1) | nb
    # source window: u_1..u_w
    src = np.zeros(nu, dtype=np.int64)
    for i in range(1, w + 1):
        src = (src << 1) | bits[i]
    # de Bruijn endpoints on words of length n-1
    left = u >> 1                      # u_0..u_{n-2}
    right = u & ((1 << (n - 1)) - 1)   # u_1..u_{n-1}

    nphi, nj = 1 << w, 1 << (n - 1)
    M = np.zeros((nu, nphi + nj), dtype=np.int64)
    rows = np.arange(nu)
    np.add.at(M, (rows, img), 1)
    np.add.at(M, (rows, src), -1)
    np.add.at(M, (rows, nphi + left), -1)
    np.add.at(M, (rows, nphi + right), 1)
    return M, nphi


def phi_constraints(rule: int, w: int, p: int):
    """Eliminate the current J exactly, leaving constraints on phi alone.

    J is a potential on the de Bruijn vertex set; fixing J(0)=0 and walking a
    spanning tree determines every J(v) as an explicit linear functional of
    phi.  The V-1 tree edges are then satisfied by construction and the
    remaining E-(V-1) = 2^(w+1)+1 edges become the complete constraint set.
    Returns a (2^(w+1)+1) x 2^w matrix mod p whose kernel is exactly
    {phi : Phi conserved on all spatially periodic configurations}.
    """
    n = w + 2
    tab = rule_table(rule)
    nu, nv, nphi = 1 << n, 1 << (n - 1), 1 << w
    u = np.arange(nu, dtype=np.int64)
    bits = [(u >> (n - 1 - i)) & 1 for i in range(n)]
    img = np.zeros(nu, dtype=np.int64)
    for i in range(w):
        img = (img << 1) | tab[bits[i] * 4 + bits[i + 1] * 2 + bits[i + 2]]
    src = np.zeros(nu, dtype=np.int64)
    for i in range(1, w + 1):
        src = (src << 1) | bits[i]
    a_of = u >> 1
    b_of = u & (nv - 1)

    # adjacency for the BFS (undirected use of the directed de Bruijn graph)
    adj: list[list[tuple[int, int, int]]] = [[] for _ in range(nv)]
    for e in range(nu):
        a, b = int(a_of[e]), int(b_of[e])
        adj[a].append((b, e, +1))   # from a: J[b] = J[a] - L[e]
        adj[b].append((a, e, -1))   # from b: J[a] = J[b] + L[e]

    P = np.zeros((nv, nphi), dtype=np.int64)
    seen = np.zeros(nv, dtype=bool)
    tree_edge = np.zeros(nu, dtype=bool)
    seen[0] = True
    stack = [0]
    while stack:
        v = stack.pop()
        for (nxt, e, sgn) in adj[v]:
            if seen[nxt] or tree_edge[e]:
                continue
            row = P[v].copy()
            # L[e] = e_img - e_src ; J[b] = J[a] - L[e], J[a] = J[b] + L[e]
            row[img[e]] = (row[img[e]] - sgn) % p
            row[src[e]] = (row[src[e]] + sgn) % p
            P[nxt] = row
            seen[nxt] = True
            tree_edge[e] = True
            stack.append(nxt)
    assert seen.all(), "de Bruijn graph must be connected"

    rest = np.nonzero(~tree_edge)[0]
    C = (P[a_of[rest]] - P[b_of[rest]]) % p
    ridx = np.arange(rest.size)
    C[ridx, img[rest]] = (C[ridx, img[rest]] - 1) % p
    C[ridx, src[rest]] = (C[ridx, src[rest]] + 1) % p
    return C


def rref_rank_nullspace(M: np.ndarray, p: int):
    """Row-reduce mod p; return (rank, nullspace basis as rows)."""
    A = M % p
    rows, cols = A.shape
    piv = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        i = r + nz[0]
        if i != r:
            A[[r, i]] = A[[i, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        col = A[:, c].copy()
        col[r] = 0
        idx = np.nonzero(col)[0]
        if idx.size:
            A[idx] = (A[idx] - np.outer(col[idx], A[r])) % p
        piv.append(c)
        r += 1
    rank = r
    free = [c for c in range(cols) if c not in set(piv)]
    ns = np.zeros((len(free), cols), dtype=np.int64)
    for k, f in enumerate(free):
        ns[k, f] = 1
        for i, c in enumerate(piv):
            ns[k, c] = (-A[i, f]) % p
    return rank, ns


def rank_of(M: np.ndarray, p: int) -> int:
    return rref_rank_nullspace(M, p)[0]


def trivial_generators(w: int, prev_basis: np.ndarray | None) -> np.ndarray:
    """Rows spanning T_w inside phi-space (dimension 2^w)."""
    nphi = 1 << w
    gens = [np.ones(nphi, dtype=np.int64)]  # constants
    if w >= 2:
        v = np.arange(nphi, dtype=np.int64)
        pl = v >> 1                      # v_0..v_{w-2}
        pr = v & ((1 << (w - 1)) - 1)    # v_1..v_{w-1}
        for gidx in range(1 << (w - 1)):
            g = np.zeros(nphi, dtype=np.int64)
            np.add.at(g, np.nonzero(pl == gidx)[0], 1)
            np.add.at(g, np.nonzero(pr == gidx)[0], -1)
            gens.append(g)
        if prev_basis is not None and prev_basis.size:
            for row in prev_basis:                 # lift psi(v_0..v_{w-2})
                gens.append(row[pl])
            for row in prev_basis:                 # shifted twin
                gens.append(row[pr])
    return np.array(gens, dtype=np.int64) if gens else np.zeros((0, nphi), np.int64)


def cross_check_elimination(rule: int, w: int, p: int) -> bool:
    """The J-eliminated system must have the same phi-solution space as the
    full (phi, J) system.  Checked directly at small w."""
    M, nphi = build_system(rule, w)
    rank, ns = rref_rank_nullspace(M, p)
    dim_full = (M.shape[1] - rank) - 1  # J is free by one additive constant
    C = phi_constraints(rule, w, p)
    dim_elim = (1 << w) - rank_of(C.copy(), p)
    return dim_full == dim_elim


def verify_phi(rule: int, w: int, phi: np.ndarray, p: int, trials: int = 400,
               seed: int = 30) -> bool:
    """Independent brute-force check: random cyclic configs, direct simulation."""
    rng = np.random.default_rng(seed)
    tab = rule_table(rule)
    for _ in range(trials):
        L = int(rng.integers(max(w + 2, 3), 40))
        s = rng.integers(0, 2, size=L)
        l, c, r = np.roll(s, 1), s, np.roll(s, -1)
        t = tab[l * 4 + c * 2 + r]

        def agg(x):
            idx = np.zeros(L, dtype=np.int64)
            for j in range(w):
                idx = (idx << 1) | np.roll(x, -j)
            return int(phi[idx].sum() % p)

        if agg(t) != agg(s):
            return False
    return True


def run_rule(rule: int, wmax: int, p: int, log) -> dict:
    out = {"rule": rule, "modulus": p, "widths": []}
    prev = None
    for w in range(1, wmax + 1):
        t0 = time.time()
        nphi = 1 << w
        C = phi_constraints(rule, w, p)
        rank, ns = rref_rank_nullspace(C.copy(), p)
        basis = ns % p                       # rows span V_w
        dim_V = nphi - rank
        triv = trivial_generators(w, prev)
        dim_triv = rank_of(triv.copy(), p) if triv.size else 0
        stacked = np.vstack([triv, basis]) if basis.size else triv
        dim_sum = rank_of(stacked.copy(), p) if stacked.size else 0
        rec = {"rule": rule, "modulus": p, "w": w, "phi_unknowns": nphi,
               "constraints": int(C.shape[0]),
               "dim_conserved": int(dim_V), "dim_trivial": int(dim_triv),
               "dim_span_trivial_plus_conserved": int(dim_sum),
               "new_nontrivial": int(dim_V - dim_triv),
               "secs": round(time.time() - t0, 2)}
        assert dim_sum == dim_V, (
            f"trivial space not contained in V_w at rule {rule} w {w}: "
            f"{dim_sum} vs {dim_V}")
        ok = True
        if basis.size:
            for row in basis[:min(8, basis.shape[0])]:
                ok = ok and verify_phi(rule, w, row, p)
        rec["bruteforce_verified"] = bool(ok)
        if w <= 5:
            rec["elimination_cross_check"] = cross_check_elimination(rule, w, p)
        out["widths"].append(rec)
        log(json.dumps(rec))
        prev = basis if basis.size else None
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wmax", type=int, default=9)
    ap.add_argument("--primes", type=str, default="2147483647,1000003,2,3")
    ap.add_argument("--rules", type=str,
                    default=",".join(str(r) for r in RULES))
    ap.add_argument("--out", type=str, default="conserved_search.jsonl")
    a = ap.parse_args()

    fh = open(a.out, "w")

    def log(line: str) -> None:
        print(line, flush=True)
        fh.write(line + "\n")
        fh.flush()

    log(json.dumps({"search": "conserved_window_functions", "wmax": a.wmax,
                    "primes": a.primes, "rules": a.rules,
                    "class": "phi:{0,1}^w -> Z/p, Phi(s)=sum_x phi(window), "
                             "conserved on ALL spatially periodic configs",
                    "characterisation": "exact de Bruijn potential/continuity "
                                        "equation, not sampling"}))
    for p in [int(x) for x in a.primes.split(",")]:
        for rule in [int(x) for x in a.rules.split(",")]:
            run_rule(rule, a.wmax, p, log)
    fh.close()


if __name__ == "__main__":
    main()
