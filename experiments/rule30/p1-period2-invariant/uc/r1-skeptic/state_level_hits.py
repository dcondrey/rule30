#!/usr/bin/env python3
"""Per-level E-hit and hard-core survival of DISTINCT forced-process states at large k.

Skeptic lens, second pass.  `kill_split.log` (same directory) pooled the RW
census over n = 12..26 by absolute level k and found the source-level E-pass
fraction rising to 0.70 at k = 14, 15 (858 and 474 survivors).  Sources
cluster into fibers of one state (RESULTS-CLUSTER-ANATOMY.md), so that number
may be a fiber artifact.  This script measures the same quantity in STATES.

State at level k (after k admissible forced columns, before column u = n+k):
the three-letter quotient (a, b) = ([T==0], [Lo(T)==0]) of column u-1 on depths
[-u, n-1].  By BRIEF section 2 the whole future of the forced orbit is a
function of this state, and so are the outcomes of step k+1: the E-hit
(E(T[u][n]) = E(c)) and the hard-core kill (e_{u-1} = e_u = 1).

Reported per (n, c, k >= kmin): N_k (sources), D_k (distinct states), the
number of states passing E, passing hard-core, passing both (= D_{k+1}), the
largest fiber at that level, and the fiber-weighted versus state-level E-pass
fractions.  Then pooled by absolute k over all (n, c), and pooled by offset
from the deepest level.  A state-level p_E clearly above 1/2 at large k, with
enough states to matter, is the clustering that would break the one-bit-per-
column rate; p_E = 1/2 within noise says the source-level 0.70 is fibers.

Also reports Q_n = D_0 exactly for n <= --q-max (the k = 0 state count is
independent of c), extending quotient_multiplicity.log beyond n = 20.

Kernel: the bit-sliced Moore machine of rw_bitsliced.py (validated there
against psi_kernel); the state extraction here is validated at small n against
quotient_multiplicity.quotient_column by --validate.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/state_level_hits.py --min-n 18 --max-n 30
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KERNEL_DIR = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KERNEL_DIR)
sys.path.insert(0, HERE)

from quotient_multiplicity import quotient_column  # noqa: E402
from rw_bitsliced import (  # noqa: E402
    bit_patterns,
    build_column,
    const_array,
    decode_word,
    forced_high,
    popcount,
    set_bits,
)

U64 = np.uint64
CHUNK = 1 << 17


def extract_states(col, nrows: int, idx: np.ndarray) -> np.ndarray:
    """Packed (a, b) quotient letters of rows 0..nrows-1 of `col` for global bit indices idx.

    Returns an array of shape (len(idx), nbytes) of dtype uint8; rows are hashable via .tobytes().
    """
    out = []
    a_rows = ((~col.h[:nrows]) & col.F[:nrows])
    b_rows = (col.h[:nrows] ^ col.F[:nrows])
    for s in range(0, len(idx), CHUNK):
        sub = idx[s : s + CHUNK]
        w = (sub >> 6).astype(np.int64)
        b = (sub & 63).astype(np.uint64)
        A = ((a_rows[:, w] >> b[None, :]) & U64(1)).astype(np.uint8)  # (nrows, m)
        Bm = ((b_rows[:, w] >> b[None, :]) & U64(1)).astype(np.uint8)
        both = np.concatenate([A, Bm], axis=0)  # (2*nrows, m)
        packed = np.packbits(both, axis=0, bitorder="little")  # (ceil(2*nrows/8), m)
        out.append(np.ascontiguousarray(packed.T))
    return np.concatenate(out, axis=0) if out else np.zeros((0, 1), dtype=np.uint8)


def unique_with_counts(packed: np.ndarray):
    """Unique rows of a (m, nbytes) uint8 array with counts and one representative index."""
    if packed.shape[0] == 0:
        return packed, np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64)
    view = np.ascontiguousarray(packed).view(np.dtype((np.void, packed.shape[1]))).ravel()
    uniq, first, counts = np.unique(view, return_index=True, return_counts=True)
    return uniq, first, counts


def state_census(n: int, sources, c: int, K: int, nwords: int, kmin: int, acc: dict, want_q0: bool, q0: set):
    """One block of the census; accumulates per-level state statistics into acc[k]."""
    prev = None
    for u in range(n):
        prev = build_column(prev, u, min(u, n - 1), sources[u], nwords)
    Ec = const_array(nwords, c & 1)
    alive = const_array(nwords, 1)
    Hprev = sources[n - 1]
    Ns = [popcount(alive)]
    for j in range(K):
        u = n + j
        k = j  # level before this step
        Hu = forced_high(prev, u, n, nwords)
        col = build_column(prev, u, n, Hu, nwords)
        Fn = col.F[col.idx(n)]
        e_ok = ~(Fn ^ Ec)
        hc_ok = ~((~Hu) & (~Hprev))
        if k >= kmin or (k == 0 and want_q0):
            idx = set_bits(alive)
            if len(idx):
                nrows = n + u  # depths -u .. n-1 of column u-1 (prev.u = u-1): rows 0..n+u-1
                packed = extract_states(prev, nrows, idx)
                uniq, first, counts = unique_with_counts(packed)
                if k == 0 and want_q0:
                    for row in uniq:
                        q0.add(row.tobytes())
                if k >= kmin:
                    rep = idx[first]
                    w = (rep >> 6).astype(np.int64)
                    b = (rep & 63).astype(np.uint64)
                    e_flag = ((e_ok[w] >> b) & U64(1)).astype(bool)
                    h_flag = ((hc_ok[w] >> b) & U64(1)).astype(bool)
                    d = acc[k]
                    for row, cnt, ef, hf in zip(uniq, counts, e_flag, h_flag):
                        key = row.tobytes()
                        rec = d.get(key)
                        if rec is None:
                            d[key] = [int(cnt), bool(ef), bool(hf)]
                        else:
                            rec[0] += int(cnt)
                            assert rec[1] == bool(ef) and rec[2] == bool(hf), "state flags must be state functions"
        alive = alive & e_ok & hc_ok
        Ns.append(popcount(alive))
        prev = col
        Hprev = Hu
        if Ns[-1] == 0:
            break
    return Ns


def validate() -> str:
    """State extraction at k = 0 must reproduce quotient_column exactly, n = 6..9."""
    checked = 0
    for n in range(6, 10):
        nwords = (1 << n) >> 6
        pats = bit_patterns(n)
        prev = None
        for u in range(n):
            prev = build_column(prev, u, min(u, n - 1), pats[u], nwords)
        idx = np.arange(1 << n, dtype=np.uint64)
        packed = extract_states(prev, 2 * n, idx)
        by_state: dict[bytes, set] = defaultdict(set)
        for i in range(1 << n):
            word = decode_word(pats, i)
            by_state[packed[i].tobytes()].add(quotient_column(word))
        for s in by_state.values():
            assert len(s) == 1, "packed state does not refine quotient_column"
        # and the converse: same quotient_column -> same packed
        by_q: dict[str, set] = defaultdict(set)
        for i in range(1 << n):
            word = decode_word(pats, i)
            by_q[quotient_column(word)].add(packed[i].tobytes())
        for s in by_q.values():
            assert len(s) == 1, "quotient_column does not refine packed state"
        checked += 1 << n
    return f"state extraction agrees with quotient_column on {checked} prefixes (n=6..9)"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--min-n", type=int, default=18)
    ap.add_argument("--max-n", type=int, default=30)
    ap.add_argument("--kmin", type=int, default=6, help="lowest level to resolve in states (raised to n-22 for large n)")
    ap.add_argument("--q-max", type=int, default=24, help="compute Q_n = D_0 exactly for n <= this")
    ap.add_argument("--block", type=int, default=22)
    args = ap.parse_args()
    if args.validate:
        print(validate())
        return
    pooled_k: dict[int, list] = defaultdict(lambda: [0, 0, 0, 0, 0, 0])  # N, D, D_E, D_HC, D_both, maxfib
    pooled_off: dict[int, list] = defaultdict(lambda: [0, 0, 0, 0, 0])
    for n in range(args.min_n, args.max_n + 1):
        K = n + 2
        B = min(args.block, n)
        nwords = (1 << B) >> 6
        pats = bit_patterns(B)
        kmin = max(args.kmin, n - 22)
        q0: set = set()
        for c in (2, 3):
            t0 = time.time()
            acc: dict[int, dict] = defaultdict(dict)
            Ntot = None
            want_q0 = (c == 2) and n <= args.q_max
            for outer in range(1 << (n - B)):
                sources = [const_array(nwords, (outer >> (n - B - 1 - t)) & 1) for t in range(n - B)] + pats
                Ns = state_census(n, sources, c, K, nwords, kmin, acc, want_q0, q0)
                if Ntot is None:
                    Ntot = [0] * (K + 1)
                for k, v in enumerate(Ns):
                    Ntot[k] += v
            deepest = max(k for k in range(len(Ntot)) if Ntot[k] > 0)
            dt = time.time() - t0
            qtxt = f" Q_n=D_0={len(q0)}" if want_q0 else ""
            print(f"n={n} c={c} deepest={deepest}{qtxt} [{dt:.0f}s]")
            print("   k     N_k      D_k    D_E   D_HC  D_both  maxfib  pE_src  pE_st  pHC_st  pboth_st")
            for k in sorted(acc):
                d = acc[k]
                D = len(d)
                if D == 0:
                    continue
                N = sum(r[0] for r in d.values())
                DE = sum(1 for r in d.values() if r[1])
                DH = sum(1 for r in d.values() if r[2])
                DB = sum(1 for r in d.values() if r[1] and r[2])
                NE = sum(r[0] for r in d.values() if r[1])
                maxfib = max(r[0] for r in d.values())
                assert N == Ntot[k], (k, N, Ntot[k])
                print(
                    f"  {k:<3} {N:>9} {D:>8} {DE:>6} {DH:>6} {DB:>7} {maxfib:>7}  "
                    f"{NE / N:6.3f} {DE / D:6.3f} {DH / D:6.3f} {DB / D:7.3f}"
                )
                p = pooled_k[k]
                p[0] += N
                p[1] += D
                p[2] += DE
                p[3] += DH
                p[4] += DB
                p[5] = max(p[5], maxfib)
                q = pooled_off[k - deepest]
                q[0] += N
                q[1] += D
                q[2] += DE
                q[3] += DH
                q[4] += DB
            sys.stdout.flush()
    print()
    print("pooled by absolute level k (all n, c above):  N  D  pE_src  pE_states  pHC_states  pboth_states  maxfib")
    for k in sorted(pooled_k):
        N, D, DE, DH, DB, mf = pooled_k[k]
        if D:
            print(f"  k={k:<3} N={N:>9} D={D:>8} pE_st={DE / D:6.3f} pHC_st={DH / D:6.3f} pboth_st={DB / D:6.3f} maxfib={mf}")
    print()
    print("pooled by offset k - deepest:  D  pE_states  pHC_states  pboth_states")
    for off in sorted(pooled_off):
        N, D, DE, DH, DB = pooled_off[off]
        if D:
            print(f"  off={off:<4} N={N:>9} D={D:>8} pE_st={DE / D:6.3f} pHC_st={DH / D:6.3f} pboth_st={DB / D:6.3f}")


if __name__ == "__main__":
    main()
