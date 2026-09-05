#!/usr/bin/env python3
"""H-forcing alone against the actual-right language: LANG-only survival.

Setting (BRIEF section 3, orbit form).  For a prefix W in {1,2}^n the symbol
e_u for u >= n is forced by H(T[u][n]) = 1, independently of c and of the
E-pin.  Write Q_n(W) for the forced word.  For the hypothetical period-two
counterexample the endpoint is eventually an actual right trace, the cut is
eventually c^omega, and for every large scale n the block e[n:2n] is in the
actual-right language R_n while e[2n:3n+2] = Q_n(e[n:2n]) (RESULTS-LATE-PULL-
DIAGONAL.md section 2, RESULTS-ACTUAL-RIGHT-FRONTIER.md section 3).  So the
E-free statement

    (HF-L)  for every W in L_n, W.Q_n(W) leaves L within alpha n + C steps

for any superset L of R contradicts the counterexample once alpha n + C < n+2.

This script measures, for finite-type supersets L of R (HC: no 11; R5: no
11, 00000; R11, R13: the recorded minimal forbidden factors; Rexact: the
factors found by r_exact_sat.py), exhaustively over every prefix in L_n:

    k_lang(W) = first forced step at which W.Q leaves L      (no E-pin at all)
    k_E2(W), k_E3(W) = first step at which E(T[u][n]) != E(c), c = 2, 3
    joint = min(k_lang, k_Ec)                                 (= RW restricted to L)

and reports the survivor counts N_k under LANG only, the deepest LANG-only
run, the number of prefixes whose forced continuation stays in L for all
n + 2 steps (an HF-L failure at scale n), the forbidden factor that kills,
E-only and joint deepest runs (the joint numbers must reproduce the earlier
rw_restricted_margin logs), and the independence null: with h = log2 of the
growth ratio of L, a forced symbol that is "random" for L survives a column
with probability 2^(h-1), so LANG-only survivors are 2^(h n - (1-h) k) and
vanish at k = h n / (1 - h); joint survivors vanish at k = h n / (2 - h).

Control: prefix set BIN (all 2^n), continuation language HC only (hard-core
alone, junction included).  At n = 16 this must give 1292 prefixes whose
forced continuation is hard-core through n + 2 steps (RESULTS-RW-LINEAR-
SLACK.md 9.6a).

Kernel: the column recursion of BRIEF section 2, vectorised over prefixes;
gated against psi_kernel.psi on every binary prefix through n = 9.

Symbols: endpoint 1 is rho bit 1, endpoint 2 is rho bit 0.  Bit words are
printed; forced part after '|'.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter, deque

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, psi  # noqa: E402

CONE_FLAT = np.array([CONE[l][r] for l in range(4) for r in range(4)], dtype=np.int8)

FORBIDDEN: dict[str, list[str]] = {
    "BIN": [],
    "HC": ["11"],
    "R5": ["11", "00000"],
}
FORBIDDEN["R11"] = FORBIDDEN["R5"] + [
    "101001", "0100101", "010010001", "0101000101", "0101010000", "01010001001", "10010001001",
]
FORBIDDEN["R13"] = FORBIDDEN["R11"] + [
    "010010000101", "010100010001", "100100010000", "0001000010001", "1001000010001",
]


class Dfa:
    """Aho-Corasick automaton for 'contains no forbidden factor'.  State 0 = root, DEAD = sink."""

    def __init__(self, forbidden: list[str]) -> None:
        goto: list[dict[str, int]] = [{}]
        out: list[str | None] = [None]
        for f in forbidden:
            s = 0
            for ch in f:
                if ch not in goto[s]:
                    goto.append({})
                    out.append(None)
                    goto[s][ch] = len(goto) - 1
                s = goto[s][ch]
            out[s] = f
        n = len(goto)
        fail = [0] * n
        order = deque()
        for ch, s in goto[0].items():
            order.append(s)
        while order:
            s = order.popleft()
            for ch, t in goto[s].items():
                order.append(t)
                f = fail[s]
                while f and ch not in goto[f]:
                    f = fail[f]
                fail[t] = goto[f][ch] if ch in goto[f] and goto[f][ch] != t else 0
                if out[t] is None and out[fail[t]] is not None:
                    out[t] = out[fail[t]]
        self.dead = n
        delta = np.full((n + 1, 2), n, dtype=np.int32)
        self.killer: list[str | None] = out + [None]
        for s in range(n):
            for bit, ch in ((0, "0"), (1, "1")):
                t = s
                while t and ch not in goto[t]:
                    t = fail[t]
                t = goto[t][ch] if ch in goto[t] else 0
                delta[s, bit] = n if out[t] is not None else t
                if out[t] is not None:
                    # remember which factor fires from (s, bit)
                    self.killer_edge = getattr(self, "killer_edge", {})
                    self.killer_edge[(s, bit)] = out[t]
        self.delta = delta
        self.size = n + 1

    def step(self, state: int, bit: int) -> int:
        return int(self.delta[state, bit])


def enumerate_prefixes(dfa: Dfa, n: int) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """All bit words of length n accepted by dfa: symbols (N, n) int8, states (N,), bit strings."""
    syms: list[list[int]] = []
    states: list[int] = []
    bits: list[str] = []
    stack = [(0, "", [])]
    while stack:
        state, b, s = stack.pop()
        if len(b) == n:
            syms.append(s)
            states.append(state)
            bits.append(b)
            continue
        for bit, sym in ((1, 1), (0, 2)):
            t = dfa.step(state, bit)
            if t == dfa.dead:
                continue
            stack.append((t, b + str(bit), s + [sym]))
    return np.array(syms, dtype=np.int8).reshape(len(syms), n), np.array(states, dtype=np.int32), bits


def count_prefixes(dfa: Dfa, n: int) -> int:
    vec = np.zeros(dfa.size, dtype=np.int64)
    vec[0] = 1
    for _ in range(n):
        nxt = np.zeros_like(vec)
        for bit in (0, 1):
            np.add.at(nxt, dfa.delta[:, bit], vec)
        nxt[dfa.dead] = 0
        vec = nxt
    return int(vec.sum())


def build_columns(syms: np.ndarray) -> np.ndarray:
    n = syms.shape[1]
    N = syms.shape[0]
    col = np.zeros((N, 0), dtype=np.int8)
    for u in range(n):
        e = syms[:, u]
        new = np.empty((N, 2 * u + 2), dtype=np.int8)
        new[:, 0] = e
        new[:, 1] = e ^ 3
        for i in range(2, 2 * u + 2):
            new[:, i] = CONE_FLAT[col[:, i - 2].astype(np.int16) * 4 + new[:, i - 1]]
        col = new
    return col


def gate_kernel(max_n: int) -> int:
    dfa = Dfa([])
    checked = 0
    for n in range(1, max_n + 1):
        syms, _, _ = enumerate_prefixes(dfa, n)
        col = build_columns(syms)
        N = syms.shape[0]
        steps = n + 2
        got_q = np.zeros((N, steps), dtype=np.int8)
        got_d = np.zeros((N, steps), dtype=np.int8)
        for j in range(steps):
            u = n + j
            zeros = (col == 0).sum(axis=1)
            high = (n + u + zeros) & 1
            e = np.where(high == 1, 2, 1).astype(np.int8)
            new = np.empty((N, n + u + 2), dtype=np.int8)
            new[:, 0] = e
            new[:, 1] = e ^ 3
            for i in range(2, n + u + 2):
                new[:, i] = CONE_FLAT[col[:, i - 2].astype(np.int16) * 4 + new[:, i - 1]]
            cell = new[:, n + u + 1]
            assert np.all(cell >> 1 == 1)
            got_q[:, j] = e
            got_d[:, j] = cell & 1
            col = new[:, : n + u + 1]
        for idx in range(N):
            q, d = psi(tuple(int(x) for x in syms[idx]))
            assert tuple(got_q[idx]) == q and tuple(got_d[idx]) == d, (syms[idx], got_q[idx], q, got_d[idx], d)
            checked += 1
    return checked


def run(prefix_lang: str, cont_lang: str, n: int, steps: int, forbidden_sets: dict[str, list[str]], nwit: int = 3) -> dict:
    pdfa = Dfa(forbidden_sets[prefix_lang])
    cdfa = Dfa(forbidden_sets[cont_lang])
    syms, pstates, bits = enumerate_prefixes(pdfa, n)
    N = syms.shape[0]
    if prefix_lang == cont_lang:
        cstate = pstates.copy()
    else:
        # continuation language checked from the junction on: feed the last
        # K-1 prefix bits, K = longest continuation factor (exact for HC).
        K = max(len(f) for f in forbidden_sets[cont_lang]) if forbidden_sets[cont_lang] else 1
        cstate = np.zeros(N, dtype=np.int32)
        for idx, b in enumerate(bits):
            s = 0
            for ch in b[max(0, n - (K - 1)):]:
                s = cdfa.step(s, int(ch))
                if s == cdfa.dead:
                    s = 0  # prefix itself may violate; only the junction matters
            cstate[idx] = s
    col = build_columns(syms)
    big = steps + 1
    k_lang = np.full(N, big, dtype=np.int32)
    k_e2 = np.full(N, big, dtype=np.int32)
    k_e3 = np.full(N, big, dtype=np.int32)
    forced_bits = [""] * N
    killer: Counter = Counter()
    alive_idx = np.arange(N)
    for j in range(steps):
        u = n + j
        M = alive_idx.size
        if M == 0:
            break
        zeros = (col == 0).sum(axis=1)
        high = (n + u + zeros) & 1
        e = np.where(high == 1, 2, 1).astype(np.int8)
        new = np.empty((M, n + u + 2), dtype=np.int8)
        new[:, 0] = e
        new[:, 1] = e ^ 3
        for i in range(2, n + u + 2):
            new[:, i] = CONE_FLAT[col[:, i - 2].astype(np.int16) * 4 + new[:, i - 1]]
        cell = new[:, n + u + 1]
        assert np.all(cell >> 1 == 1)
        E = cell & 1
        bit = (e == 1).astype(np.int32)
        cs = cstate[alive_idx]
        ns = cdfa.delta[cs, bit]
        lang_dead = ns == cdfa.dead
        # record first failures
        still_lang = k_lang[alive_idx] == big
        newly = still_lang & lang_dead
        for local in np.nonzero(newly)[0]:
            k_lang[alive_idx[local]] = j
            killer[cdfa.killer_edge.get((int(cs[local]), int(bit[local])), "?")] += 1
        for local in np.nonzero(still_lang)[0]:
            forced_bits[alive_idx[local]] += str(int(bit[local]))
        cstate[alive_idx] = ns
        e2_new = (k_e2[alive_idx] == big) & (E != 0)
        k_e2[alive_idx[e2_new]] = j
        e3_new = (k_e3[alive_idx] == big) & (E != 1)
        k_e3[alive_idx[e3_new]] = j
        col = new[:, : n + u + 1]
        # compact: keep prefixes alive under LANG or under E-only (either c)
        keep = (k_lang[alive_idx] == big) | (k_e2[alive_idx] == big) | (k_e3[alive_idx] == big)
        alive_idx = alive_idx[keep]
        col = col[keep]
    k_lang = np.minimum(k_lang, steps)
    k_e2 = np.minimum(k_e2, steps)
    k_e3 = np.minimum(k_e3, steps)
    joint2 = np.minimum(k_lang, k_e2)
    joint3 = np.minimum(k_lang, k_e3)
    N_lang = [int((k_lang >= k).sum()) for k in range(steps + 1)]
    deepest_lang = int(k_lang.max())
    order = np.argsort(-k_lang)
    witnesses = [f"{bits[i]}|{forced_bits[i]}" for i in order[:nwit]]
    return {
        "prefix_lang": prefix_lang,
        "cont_lang": cont_lang,
        "n": n,
        "steps": steps,
        "N": N,
        "N_lang": N_lang,
        "deepest_lang": deepest_lang,
        "n_full": int((k_lang >= n + 2).sum()),
        "deepest_e2": int(k_e2.max()),
        "deepest_e3": int(k_e3.max()),
        "deepest_joint2": int(joint2.max()),
        "deepest_joint3": int(joint3.max()),
        "killer": killer,
        "witnesses": witnesses,
        "k_lang_hist": Counter(int(x) for x in k_lang),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--languages", default="R13", help="comma list of prefix=cont pairs, e.g. R13,R5,BIN=HC")
    ap.add_argument("--min-n", type=int, default=13)
    ap.add_argument("--max-n", type=int, default=30)
    ap.add_argument("--steps", default="2n+2", help="forced steps: '2n+2' or 'n+2' or an integer")
    ap.add_argument("--gate", type=int, default=9)
    ap.add_argument("--exact-json", default="", help="r_exact_sat.py output; adds language Rexact")
    ap.add_argument("--nwit", type=int, default=3)
    args = ap.parse_args()
    forbidden_sets = dict(FORBIDDEN)
    if args.exact_json:
        with open(args.exact_json) as fh:
            data = json.load(fh)
        forbidden_sets["Rexact"] = list(data["forbidden"])
        print(f"Rexact: {len(forbidden_sets['Rexact'])} minimal forbidden factors through length {data['max_length']}")
    if args.gate:
        print(f"gate: {gate_kernel(args.gate)} binary prefixes agree with psi_kernel.psi through n={args.gate}")
    for spec in args.languages.split(","):
        if "=" in spec:
            pl, cl = spec.split("=")
        else:
            pl = cl = spec
        print(f"##### prefix language {pl}, continuation language {cl}")
        pdfa = Dfa(forbidden_sets[pl])
        for n in range(args.min_n, args.max_n + 1):
            if args.steps == "2n+2":
                steps = 2 * n + 2
            elif args.steps == "n+2":
                steps = n + 2
            else:
                steps = int(args.steps)
            t0 = time.time()
            size = count_prefixes(pdfa, n)
            prev = count_prefixes(pdfa, n - 1)
            h = math.log2(size / prev) if prev else float("nan")
            null_lang = h * n / (1 - h) if h < 1 else float("inf")
            null_joint = h * n / (2 - h)
            res = run(pl, cl, n, steps, forbidden_sets, args.nwit)
            print(
                f"n={n:2d} |L_n|={res['N']:7d} h={h:.3f} null_lang={null_lang:5.1f} null_joint={null_joint:5.1f} | "
                f"LANG-only deepest={res['deepest_lang']:3d} ({res['deepest_lang'] / n:.3f} n) full(n+2)={res['n_full']:6d} | "
                f"E-only deepest c2={res['deepest_e2']:3d} c3={res['deepest_e3']:3d} | "
                f"joint deepest c2={res['deepest_joint2']:3d} c3={res['deepest_joint3']:3d} need={n + 2}  ({time.time() - t0:.1f}s)"
            )
            nk = res["N_lang"]
            line = "    LANG-only N_k:"
            for k in range(len(nk)):
                if nk[k] == 0:
                    break
                line += f" {k}:{nk[k]}"
            print(line)
            kill = ", ".join(f"{f}:{c}" for f, c in res["killer"].most_common(8))
            print(f"    killing factor at first LANG failure: {kill}")
            print(f"    LANG-only deepest witnesses: {'  '.join(res['witnesses'])}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
