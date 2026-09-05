#!/usr/bin/env python3
"""Bit-parallel complete census of the rotated wedge (RW) over all 2^n prefixes.

Skeptic lens, 2026-09-02.  This is the same object `rw_margin.py` measures, but
computed with the Moore transducer of BRIEF section 2 bit-sliced across 64
prefixes per machine word, so that the complete census reaches n well beyond
17 on one core.

Coordinates (BRIEF section 2): cell T[u][d] has state (h, F) = (H, E).  Column
u is the trajectory of

    (h, F) -> (h XOR 1 XOR a, F XOR (h AND b)),   a = [T==0], b = [Lo(T)==0]

read over column u-1 from depth d = -u upward, starting at (1 - H(e_u), 0).
In (h, F) coordinates of the previous column's cell, with Lo = 1 + h + F,

    a = (NOT h) AND F,   b = h XOR F.

The forced symbol at column u >= n is the unique binary e_u with H(T[u][n]) = 1
and the E constraint is E(T[u][n]) = E(c).  Hard-core kills e_u = 1 after
e_{u-1} = 1 (junction with the prefix included).

Every claim below is gated against `psi_kernel.Endpoint` by `validate()` before
any census is trusted; run with `--validate`.

Run from the kernel directory:
    cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/rw_bitsliced.py --validate
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time

import numpy as np

KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)

from psi_kernel import Endpoint  # noqa: E402

U64 = np.uint64
ONES = U64(0xFFFFFFFFFFFFFFFF)


def bit_patterns(B: int) -> list[np.ndarray]:
    """pattern[j][w] has bit i set iff bit j of (64 w + i) is 1, for 2^B indices."""
    assert B >= 6
    nwords = (1 << B) >> 6
    idx = np.arange(1 << B, dtype=np.uint64)
    out = []
    for j in range(B):
        bits = ((idx >> U64(j)) & U64(1)).astype(np.uint8)
        packed = np.packbits(bits.reshape(-1, 64), axis=1, bitorder="little")
        out.append(np.ascontiguousarray(packed).view(np.uint64).ravel().copy())
        assert out[-1].shape == (nwords,)
    return out


def const_array(nwords: int, bit: int) -> np.ndarray:
    return np.full(nwords, ONES if bit else U64(0), dtype=np.uint64)


def popcount(arr: np.ndarray) -> int:
    return int(np.bitwise_count(arr).sum())


def set_bits(arr: np.ndarray) -> np.ndarray:
    """Global bit indices (64 w + i) of set bits."""
    return np.flatnonzero(np.unpackbits(arr.view(np.uint8), bitorder="little"))


class Column:
    __slots__ = ("u", "top", "h", "F")

    def __init__(self, u: int, top: int, nwords: int):
        self.u = u
        self.top = top
        L = u + 2 + top
        self.h = np.empty((L, nwords), dtype=np.uint64)
        self.F = np.empty((L, nwords), dtype=np.uint64)

    def idx(self, d: int) -> int:
        return d + self.u + 1


def build_column(prev: Column | None, u: int, top: int, Hu: np.ndarray, nwords: int) -> Column:
    """Column u on depths [-u-1, top] from column u-1 and the high bit of e_u."""
    col = Column(u, top, nwords)
    h, F = col.h, col.F
    h[0] = Hu
    F[0] = 0
    h[1] = ~Hu
    F[1] = 0
    if top <= -u or prev is None:
        return col
    # depths d = -u .. top-1 produce depth d+1
    hp, Fp = prev.h, prev.F
    for d in range(-u, top):
        i = d + u + 1
        ip = d + u  # depth d in column u-1 (offset u)
        hpd = hp[ip]
        Fpd = Fp[ip]
        a = (~hpd) & Fpd
        b = hpd ^ Fpd
        h[i + 1] = h[i] ^ (~a)
        F[i + 1] = F[i] ^ (h[i] & b)
    return col


def forced_high(prev: Column, u: int, n: int, nwords: int) -> np.ndarray:
    """H(e_u) making H(T[u][n]) = 1: parity over d in [-u, n-1] of (1 XOR a_d)."""
    acc = const_array(nwords, (n + u) & 1)  # number of terms is n+u, each 1 XOR a
    hp, Fp = prev.h, prev.F
    for d in range(-u, n):
        ip = d + u
        acc ^= (~hp[ip]) & Fp[ip]
    return acc


class CensusResult:
    def __init__(self, n: int, c: int, K: int):
        self.n = n
        self.c = c
        self.K = K
        self.N = []  # N_k for k = 0..K (survivors after k forced columns)
        self.exact = {}  # (k, v) -> count with exactly v violations after k columns, v in 0,1,2
        self.exact_12a = {}  # (k, v) for k = n+2, n+3, n+4 with the 12a ending
        self.alive_masks = []  # alive mask after each k (kept for witness extraction)
        self.Hforced = []
        self.exact_masks = {}


def census(n: int, sources: list[np.ndarray], c: int, K: int, nwords: int, keep_masks: bool = True, early_stop: bool = True, hardcore: bool = True) -> CensusResult:
    """Complete forced-path census for prefix bits given by `sources` (H bits of e_0..e_{n-1})."""
    res = CensusResult(n, c, K)
    prev = None
    for u in range(n):
        top = min(u, n - 1)  # only depths up to n-1 are needed from prefix columns
        prev = build_column(prev, u, top, sources[u], nwords)
    Ec = c & 1  # E(2)=0, E(3)=1
    alive = const_array(nwords, 1)
    ex1 = const_array(nwords, 0)
    ex2 = const_array(nwords, 0)
    Hprev = sources[n - 1]
    res.N.append(popcount(alive))
    if keep_masks:
        res.alive_masks.append(alive.copy())
    for j in range(K):
        u = n + j
        Hu = forced_high(prev, u, n, nwords)
        col = build_column(prev, u, n, Hu, nwords)
        Fn = col.F[col.idx(n)]
        e_ok = ~(Fn ^ const_array(nwords, Ec))
        hc_kill = ((~Hu) & (~Hprev)) if hardcore else const_array(nwords, 0)
        ok = e_ok & (~hc_kill)
        # kill split: survivors before this column, and how many pass E alone / hard-core alone
        res.exact[("A", j + 1)] = popcount(alive)
        res.exact[("E", j + 1)] = popcount(alive & e_ok)
        res.exact[("HC", j + 1)] = popcount(alive & ~hc_kill)
        # violation counting (E mismatch and hard-core kill each count one; both at once counts one)
        ex2 = (ex2 & ok) | (ex1 & ~ok)
        ex1 = (ex1 & ok) | (alive & ~ok)
        alive = alive & ok
        res.N.append(popcount(alive))
        res.exact[(j + 1, 0)] = res.N[-1]
        res.exact[(j + 1, 1)] = popcount(ex1)
        res.exact[(j + 1, 2)] = popcount(ex2)
        res.Hforced.append(Hu)
        if keep_masks:
            res.alive_masks.append(alive.copy())
        if j + 1 in (n + 2, n + 3, n + 4):
            r = j + 1 - n - 2
            # f[-3:-1] = 12: e_{2n+r-1} = 1 (H=0), e_{2n+r} = 2 (H=1); forced indices n+r-1, n+r
            end = (~res.Hforced[n + r - 1]) & res.Hforced[n + r]
            res.exact_12a[(j + 1, 0)] = popcount(alive & end)
            res.exact_12a[(j + 1, 1)] = popcount(ex1 & end)
            res.exact_12a[(j + 1, 2)] = popcount(ex2 & end)
            res.exact_masks[(j + 1, 0)] = (alive & end).copy()
            res.exact_masks[(j + 1, 1)] = (ex1 & end).copy()
        prev = col
        Hprev = Hu
        if early_stop and res.N[-1] == 0 and popcount(ex1) == 0 and popcount(ex2) == 0:
            # nothing within two violations survives; fill the rest and stop
            for jj in range(j + 1, K):
                res.N.append(0)
                for v in range(3):
                    res.exact[(jj + 1, v)] = 0
                if jj + 1 in (n + 2, n + 3, n + 4):
                    for v in range(3):
                        res.exact_12a[(jj + 1, v)] = 0
            break
    return res


def decode_word(sources: list[np.ndarray], bit_index: int) -> str:
    w, b = divmod(bit_index, 64)
    return "".join("2" if (int(sources[u][w]) >> b) & 1 else "1" for u in range(len(sources)))


# ---------------------------------------------------------------- reference


def reference_path(word: str, c: int, K: int) -> tuple[int, str, str, int]:
    """Pure-Python forced path via psi_kernel: (run, forced symbols, E bits, violations)."""
    n = len(word)
    ep = Endpoint()
    for ch in word:
        ep.append(int(ch))
    prev = int(word[-1])
    forced = []
    ebits = []
    run = None
    viol = 0
    for j in range(K):
        chosen = None
        for s in (1, 2):
            _, diag = ep.peek(s)
            if diag[n] >> 1 == 1:
                assert chosen is None
                chosen = (s, diag[n])
        assert chosen is not None
        s, cell = chosen
        E = 1 ^ (cell >> 1) ^ (cell & 1)
        bad = (E != (c & 1)) or (s == 1 and prev == 1)
        if bad:
            viol += 1
            if run is None:
                run = j
        forced.append(str(s))
        ebits.append(str(E))
        ep.append(s)
        prev = s
    if run is None:
        run = K
    return run, "".join(forced), "".join(ebits), viol


def validate(seed: int = 1) -> str:
    rng = random.Random(seed)
    checked = 0
    for n in range(6, 13):
        B = n
        nwords = (1 << B) >> 6
        pats = bit_patterns(B)
        K = n + 4
        for c in (2, 3):
            res = census(n, pats, c, K, nwords, early_stop=False)
            # all prefixes' runs from the masks
            runs = np.zeros(1 << n, dtype=np.int64)
            for k in range(1, len(res.alive_masks)):
                runs[set_bits(res.alive_masks[k])] = k
            sample = rng.sample(range(1 << n), min(64, 1 << n))
            for i in sample:
                word = decode_word(pats, i)
                run, forced, ebits, viol = reference_path(word, c, K)
                assert run == runs[i], (n, c, word, run, runs[i])
                # forced symbols agree
                for j in range(K):
                    w, b = divmod(i, 64)
                    Hbit = (int(res.Hforced[j][w]) >> b) & 1
                    assert ("2" if Hbit else "1") == forced[j], (n, c, word, j, forced)
                checked += 1
            # violation counts for v=0 against N_k
            for k in range(1, K + 1):
                assert res.exact[(k, 0)] == res.N[k]
    # rw_margin cross-check on deepest for n = 6..11
    from rw_margin import deepest as ref_deepest

    for n in range(6, 12):
        pats = bit_patterns(n)
        nwords = (1 << n) >> 6
        for c in (2, 3):
            res = census(n, pats, c, n + 4, nwords)
            mine = max(k for k in range(len(res.N)) if res.N[k] > 0)
            ref, _ = ref_deepest(n, 0, c)
            assert mine == ref, (n, c, mine, ref)
    return f"bitsliced kernel: {checked} sampled forced paths agree with psi_kernel; deepest agrees with rw_margin for n=6..11"


# ---------------------------------------------------------------- census driver


def full_census(n: int, c: int, B: int, K: int, want_witness_masks: bool = True, hardcore: bool = True):
    """Complete census over all 2^n prefixes; first n-B symbols enumerated, last B bit-sliced."""
    B = min(B, n)
    nwords = (1 << B) >> 6
    pats = bit_patterns(B)
    agg_N = None
    agg_exact = {}
    agg_12a = {}
    witnesses = {}  # k -> list of words (only for the deepest levels)
    near = {}  # (k, v) -> words with 12a ending and v violations, v in (0,1)
    outer_count = 1 << (n - B)
    for outer in range(outer_count):
        sources = [const_array(nwords, (outer >> (n - B - 1 - t)) & 1) for t in range(n - B)] + pats
        res = census(n, sources, c, K, nwords, keep_masks=want_witness_masks, hardcore=hardcore)
        if agg_N is None:
            agg_N = list(res.N)
        else:
            agg_N = [x + y for x, y in zip(agg_N, res.N)]
        for key, v in res.exact.items():
            agg_exact[key] = agg_exact.get(key, 0) + v
        for key, v in res.exact_12a.items():
            agg_12a[key] = agg_12a.get(key, 0) + v
        if want_witness_masks:
            # deepest surviving level in this block
            ks = [k for k in range(len(res.alive_masks)) if popcount(res.alive_masks[k]) > 0]
            kd = max(ks)
            for k in range(max(1, kd - 1), kd + 1):
                for i in set_bits(res.alive_masks[k]):
                    witnesses.setdefault(k, []).append(decode_word(sources, int(i)))
            for key, m in res.exact_masks.items():
                for i in set_bits(m):
                    near.setdefault(key, []).append(decode_word(sources, int(i)))
    return agg_N, agg_exact, agg_12a, witnesses, near


def common_suffix(words: list[str]) -> str:
    if not words:
        return ""
    s = words[0]
    for w in words[1:]:
        k = 0
        while k < len(s) and k < len(w) and s[-1 - k] == w[-1 - k]:
            k += 1
        s = s[len(s) - k:] if k else ""
        if not s:
            break
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--min-n", type=int, default=7)
    ap.add_argument("--max-n", type=int, default=20)
    ap.add_argument("--block", type=int, default=22, help="bit-sliced symbols per block (2^B prefixes)")
    ap.add_argument("--json", type=str, default="", help="write per-n results to this JSON file")
    args = ap.parse_args()
    if args.validate:
        print(validate())
        return
    out = {}
    print(" n  c  deepest need  slack  N_k (k=0..)                       max_k N_k/2^(n-k) (at k)   v<=1@n+2  v<=1@n+2&12a  witnesses@deepest  common suffix")
    for n in range(args.min_n, args.max_n + 1):
        K = n + 4
        for c in (2, 3):
            t0 = time.time()
            N, exact, e12, wit, near = full_census(n, c, args.block, K)
            dt = time.time() - t0
            deepest = max(k for k in range(len(N)) if N[k] > 0)
            ratios = [(N[k] / 2 ** (n - k), k) for k in range(1, len(N)) if N[k] > 0]
            rmax, kmax = max(ratios)
            v1 = exact[(n + 2, 0)] + exact[(n + 2, 1)]
            v1a = e12[(n + 2, 0)] + e12[(n + 2, 1)]
            w = wit.get(deepest, [])
            cs = common_suffix(w)
            flag = "  <- RW COUNTEREXAMPLE" if any(e12[(n + 2 + r, 0)] > 0 for r in range(3)) else ""
            print(
                f"{n:<3}{c:<3}{deepest:<8}{n+2:<6}{n+2-deepest:<7}"
                f"{','.join(str(x) for x in N[:min(len(N), 14)]):<48}"
                f"{rmax:6.2f} (k={kmax:<2})   {v1:<9}{v1a:<13}{len(w):<18}{cs}{flag}   [{dt:.1f}s]"
            )
            sys.stdout.flush()
            out[f"{n},{c}"] = {
                "n": n,
                "c": c,
                "deepest": deepest,
                "N": N,
                "exact": {f"{k},{v}": val for (k, v), val in exact.items()},
                "exact_12a": {f"{k},{v}": val for (k, v), val in e12.items()},
                "witnesses": {str(k): v for k, v in wit.items()},
                "near": {f"{k},{v}": ws for (k, v), ws in near.items()},
                "seconds": dt,
            }
            if args.json:
                with open(args.json, "w") as fh:
                    json.dump(out, fh)


if __name__ == "__main__":
    main()
