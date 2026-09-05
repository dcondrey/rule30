#!/usr/bin/env python3
"""Structured RW search over periodic and eventually periodic hard-core endpoints.

For a fixed binary word f (given, not forced) the RW condition at (n, r, c) is
T[u][n] = c for u in [n, 2n+r+1], f[n:2n+r+2] hard-core including the junction
with f[n-1], and f[2n+r-1] f[2n+r] = 12.  Because c has high bit one, the
symbols f[u] on that range are automatically the forced ones, so this is the
same predicate `rw_bitsliced.py` searches, restricted to a structured family
and pushed to depths n far beyond exhaustive reach.

Families:
  (i)  purely periodic words with cyclically hard-core period p <= --max-period,
       every rotation as its own word;
  (ii) an arbitrary binary prefix of length <= --max-prefix followed by a
       cyclically hard-core periodic tail of period <= --tail-period.

For every word and every depth n <= --max-n the script records the run
run_n = #consecutive u >= n with T[u][n] = c, and reports the maximum excess
run_n - (n + 2) over the family (0 or more with the hard-core and 12a side
conditions would be an RW counterexample).

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/periodic_family.py
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)

from rw_bitsliced import build_column, reference_path  # noqa: E402
from psi_kernel import Endpoint  # noqa: E402


def pack_columns(Hbits: np.ndarray) -> tuple[list[np.ndarray], int]:
    """Hbits (batch, L) uint8 -> per-position packed uint64 arrays (nwords,)."""
    batch, L = Hbits.shape
    pad = (-batch) % 64
    if pad:
        Hbits = np.vstack([Hbits, np.zeros((pad, L), dtype=np.uint8)])
    nwords = Hbits.shape[0] // 64
    sources = []
    for u in range(L):
        packed = np.packbits(Hbits[:, u].reshape(-1, 64), axis=1, bitorder="little")
        sources.append(np.ascontiguousarray(packed).view(np.uint64).ravel().copy())
    return sources, nwords


def runs_for_words(Hbits: np.ndarray, c: int, n_max: int) -> np.ndarray:
    """run[b, n] = number of consecutive columns u >= n with T[u][n] = c, word b."""
    batch, L = Hbits.shape
    sources, nwords = pack_columns(Hbits)
    B = nwords * 64
    Ec = c & 1
    alive = np.full((n_max + 1, nwords), np.uint64(0xFFFFFFFFFFFFFFFF), dtype=np.uint64)
    run = np.full((B, n_max + 1), -1, dtype=np.int32)
    prev = None
    for u in range(L):
        top = min(u, n_max)
        col = build_column(prev, u, top, sources[u], nwords)
        if u >= 0:
            i0 = col.idx(0)
            h_rows = col.h[i0 : i0 + top + 1]
            F_rows = col.F[i0 : i0 + top + 1]
            match = h_rows & (F_rows if Ec else ~F_rows)
            old = alive[: top + 1]
            dead = old & ~match
            alive[: top + 1] = old & match
            if dead.any():
                bits = np.unpackbits(dead.view(np.uint8), axis=1, bitorder="little")  # (top+1, B)
                ns, bs = np.nonzero(bits)
                run[bs, ns] = u - ns
        prev = col
    # words still alive at the end have run = L - n
    still = np.unpackbits(alive.view(np.uint8), axis=1, bitorder="little")
    ns, bs = np.nonzero(still)
    run[bs, ns] = L - ns
    return run[:batch]


def cyclic_hardcore_words(p: int) -> list[str]:
    out = []
    for w in product("12", repeat=p):
        s = "".join(w)
        if "11" in s or (s[0] == "1" and s[-1] == "1"):
            continue
        out.append(s)
    return out


def hardcore_ok(f: str, n: int, r: int) -> bool:
    seg = f[n - 1 : 2 * n + r + 2]
    return "11" not in seg


def validate(n_max: int = 12, seed: int = 3) -> str:
    """Gate runs_for_words against psi_kernel on random words."""
    import random

    rng = random.Random(seed)
    L = 2 * n_max + 4
    words = ["".join(rng.choice("12") for _ in range(L)) for _ in range(200)]
    Hbits = np.array([[1 if ch == "2" else 0 for ch in w] for w in words], dtype=np.uint8)
    checked = 0
    for c in (2, 3):
        run = runs_for_words(Hbits, c, n_max)
        for b, w in enumerate(words):
            ep = Endpoint()
            for ch in w:
                ep.append(int(ch))
            # T[u][n] via full recomputation: diagonal after u+1 symbols gives T[u][.]
            for n in range(1, n_max + 1):
                ep2 = Endpoint()
                cnt = 0
                for u, ch in enumerate(w):
                    ep2.append(int(ch))
                    if u >= n:
                        if ep2.diagonal[n] == c and cnt == u - n:
                            cnt += 1
                assert cnt == run[b, n], (w, c, n, cnt, run[b, n])
                checked += 1
    return f"periodic_family kernel: {checked} (word, c, n) run values agree with psi_kernel"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--max-n", type=int, default=200)
    ap.add_argument("--max-period", type=int, default=16)
    ap.add_argument("--max-prefix", type=int, default=6)
    ap.add_argument("--tail-period", type=int, default=8)
    ap.add_argument("--batch", type=int, default=4096)
    args = ap.parse_args()
    if args.validate:
        print(validate())
        return
    n_max = args.max_n
    L = 2 * n_max + 4

    def run_family(label: str, words: list[str]) -> None:
        t0 = time.time()
        best = {2: (-10**9, None, None), 3: (-10**9, None, None)}  # excess, word, n
        best_admissible = {2: (-10**9, None, None), 3: (-10**9, None, None)}
        hist = {2: {}, 3: {}}
        counter = 0
        for start in range(0, len(words), args.batch):
            chunk = words[start : start + args.batch]
            Hbits = np.array([[1 if ch == "2" else 0 for ch in w] for w in chunk], dtype=np.uint8)
            for c in (2, 3):
                run = runs_for_words(Hbits, c, n_max)
                for b, w in enumerate(chunk):
                    for n in range(6, n_max + 1):
                        ex = int(run[b, n]) - (n + 2)
                        if ex > best[c][0]:
                            best[c] = (ex, w, n)
                        # admissible: hard-core on f[n-1:2n+r+2] and 12a ending, for some r
                        for r in range(3):
                            need = n + r + 2
                            if run[b, n] >= need and hardcore_ok(w, n, r) and w[2 * n + r - 1] == "1" and w[2 * n + r] == "2":
                                counter += 1
                                print(f"  RW COUNTEREXAMPLE in {label}: c={c} n={n} r={r} word={w[:2*n+r+2]}")
                        if hardcore_ok(w, n, 0):
                            if ex > best_admissible[c][0]:
                                best_admissible[c] = (ex, w, n)
                    # histogram of run/n over n >= 20
                    for n in range(20, n_max + 1, 20):
                        ratio = round(int(run[b, n]) / n, 2)
                        hist[c][n] = max(hist[c].get(n, 0), ratio)
        dt = time.time() - t0
        print(f"{label}: {len(words)} words, n <= {n_max}, {dt:.1f}s, counterexamples={counter}")
        for c in (2, 3):
            ex, w, n = best[c]
            print(f"  c={c} max excess run-(n+2) = {ex} at n={n}, run={ex+n+2}, word prefix {w[:min(len(w), 60)] if w else None}")
            ex, w, n = best_admissible[c]
            print(f"  c={c} max excess with hard-core f[n-1:2n+2] = {ex} at n={n}")
            print(f"  c={c} max run/n at n=20,40,...: {[(n, hist[c][n]) for n in sorted(hist[c])]}")
        sys.stdout.flush()

    # family (i)
    words = []
    for p in range(1, args.max_period + 1):
        for w in cyclic_hardcore_words(p):
            words.append((w * (L // p + 1))[:L])
    run_family(f"(i) purely periodic hard-core, p<={args.max_period}", words)

    # family (ii)
    tails = []
    for p in range(1, args.tail_period + 1):
        tails.extend(cyclic_hardcore_words(p))
    words = []
    for m in range(1, args.max_prefix + 1):
        for pre in product("12", repeat=m):
            s = "".join(pre)
            for t in tails:
                words.append((s + t * (L // len(t) + 1))[:L])
    run_family(f"(ii) prefix<={args.max_prefix} + hard-core periodic tail p<={args.tail_period}", words)


if __name__ == "__main__":
    main()
