#!/usr/bin/env python3
"""Periodic prefixes inside the actual-right language: does H-forcing keep them in it?

A dead-on-arrival check for (HF-L) of hf_lang_survival.py.  If some purely
periodic bit pattern p^omega lies in L (all its factors avoid L's forbidden
list) and the H-forced continuation of every truncation (p^omega)[:n] stays in
L for all n + 2 steps at every n, then HF-L is false for that L.  The
alternating source 1212... (bits 1010...) is the obvious candidate: it is in
R13 for every length and its Psi depends on one to three source bits
(BACKLOG.md section 16).

For every primitive pattern of period p <= --max-period whose infinite
periodic word is in L, every rotation, and every n in [--min-n, --max-n],
run the forced continuation for n + 2 steps (no E-pin) and record k_lang, the
first step at which the word leaves L.  Report, per pattern, max_n k_lang / n
and the number of n at which k_lang = n + 2 (full survival).  Also report the
E-only run for c = 2, 3 as a control against no-small-period-source
(BACKLOG.md section 13, held to n = 100 with the E-pin).

Pure Python column recursion (BRIEF section 2); the same recursion is gated
against psi_kernel.psi in hf_lang_survival.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import product

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-hardcore")
from psi_kernel import CONE  # noqa: E402
from hf_lang_survival import FORBIDDEN, Dfa  # noqa: E402


def forced_run(prefix_syms: list[int], steps: int, dfa: Dfa, state: int) -> tuple[int, int, int, str]:
    """Return (k_lang, k_E2, k_E3, forced bits) along the H-forced orbit."""
    n = len(prefix_syms)
    col: list[int] = []
    for u, e in enumerate(prefix_syms):
        new = [0] * (2 * u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, 2 * u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        col = new
    k_lang = k_e2 = k_e3 = steps
    fbits = ""
    for j in range(steps):
        u = n + j
        zeros = col.count(0)
        e = 2 if (n + u + zeros) & 1 else 1
        new = [0] * (n + u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, n + u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        cell = new[n + u + 1]
        assert cell >> 1 == 1
        E = cell & 1
        bit = 1 if e == 1 else 0
        if k_lang == steps:
            state = dfa.step(state, bit)
            fbits += str(bit)
            if state == dfa.dead:
                k_lang = j
        if k_e2 == steps and E != 0:
            k_e2 = j
        if k_e3 == steps and E != 1:
            k_e3 = j
        col = new[: n + u + 1]
    return k_lang, k_e2, k_e3, fbits


def primitive(p: str) -> bool:
    for d in range(1, len(p)):
        if len(p) % d == 0 and p == p[: d] * (len(p) // d):
            return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--language", default="R13")
    ap.add_argument("--exact-json", default="")
    ap.add_argument("--max-period", type=int, default=12)
    ap.add_argument("--min-n", type=int, default=13)
    ap.add_argument("--max-n", type=int, default=60)
    ap.add_argument("--step-n", type=int, default=1)
    args = ap.parse_args()
    forbidden = dict(FORBIDDEN)
    if args.exact_json:
        with open(args.exact_json) as fh:
            forbidden["Rexact"] = list(json.load(fh)["forbidden"])
    dfa = Dfa(forbidden[args.language])
    K = max((len(f) for f in forbidden[args.language]), default=1)
    patterns = []
    seen = set()
    for p in range(1, args.max_period + 1):
        for bits in product("01", repeat=p):
            pat = "".join(bits)
            if not primitive(pat):
                continue
            # canonical rotation representative; all rotations run below
            rots = {pat[i:] + pat[:i] for i in range(p)}
            canon = min(rots)
            if canon in seen:
                continue
            seen.add(canon)
            # in L iff the periodic word of length p + K avoids the list
            s = 0
            ok = True
            word = (canon * ((p + K) // p + 2))[: p + K + p]
            for ch in word:
                s = dfa.step(s, int(ch))
                if s == dfa.dead:
                    ok = False
                    break
            if ok:
                patterns.append(canon)
    print(f"language {args.language}: {len(patterns)} primitive patterns of period <= {args.max_period} lie in it: {patterns}")
    print(" pattern      rot  max k_lang/n (at n)   #n with full survival   max E2/n  max E3/n   worst witness (bits prefix|forced through failure)")
    overall = []
    for pat in patterns:
        p = len(pat)
        for r in range(p):
            rot = pat[r:] + pat[:r]
            best = (0.0, 0)
            full = 0
            best_e2 = best_e3 = 0.0
            wit = ""
            for n in range(args.min_n, args.max_n + 1, args.step_n):
                bits = (rot * (n // p + 1))[:n]
                syms = [1 if ch == "1" else 2 for ch in bits]
                s = 0
                for ch in bits:
                    s = dfa.step(s, int(ch))
                assert s != dfa.dead
                k_lang, k_e2, k_e3, fbits = forced_run(syms, n + 2, dfa, s)
                if k_lang >= n + 2:
                    full += 1
                if k_lang / n > best[0]:
                    best = (k_lang / n, n)
                    wit = f"{bits}|{fbits}"
                best_e2 = max(best_e2, k_e2 / n)
                best_e3 = max(best_e3, k_e3 / n)
            overall.append((best[0], rot))
            print(f" {rot:12s} {r:3d}   {best[0]:.3f} (n={best[1]:3d})        {full:5d}               {best_e2:.3f}   {best_e3:.3f}    {wit[:90]}")
            sys.stdout.flush()
    overall.sort(reverse=True)
    print(f"largest max k_lang/n over all patterns and rotations: {overall[:5]}")


if __name__ == "__main__":
    main()
