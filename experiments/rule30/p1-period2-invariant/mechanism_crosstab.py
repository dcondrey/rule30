#!/usr/bin/env python3
"""Crosstab of forced symbol, pin, and next-column pin along the unstopped forced orbit.
Verifies Phi = W + [e_u = 1] * beta on every column, then tabulates the transition law."""
from itertools import product
from psi_kernel import Endpoint
E = lambda s: 1 ^ (s >> 1) ^ (s & 1)
H = lambda s: s >> 1

def counts(cells):
    Z = sum(1 for t in cells if t == 0); W2 = sum(1 for t in cells if t == 2)
    A = 0; Wc = 0
    for t in cells:
        even = 1 if (t & 1) == 0 else 0
        Wc ^= A & even
        A ^= (0 if t == 0 else 1)
    return Z & 1, W2 & 1, Wc & 1, (Z + W2) & 1

for n in (6, 10, 12):
    for c in (2, 3):
        tot = 0; alg_fail = 0
        by_e = {1: [0, 0], 2: [0, 0]}                # [count, hits]
        trans = {}                                    # (e_u, hit_u) -> [count, hits at u+1]
        trans_e = {}                                  # (e_u, hit_u) -> [count, e_{u+1}==1]
        junction = {1: 0, 2: 0}
        for W in product((1, 2), repeat=n):
            st = Endpoint()
            for s in W: st.append(s)
            prev = W[-1]; seq = []
            for u in range(n, 2 * n + 2):
                m = n + u
                cells = [st.column[u]] + [st.column[k] for k in range(u - 1, 0, -1)] + [st.diagonal[k] for k in range(u)]
                cells = cells[:m]
                Z, W2, Wc, beta = counts(cells)
                s = None
                for cand in (1, 2):
                    col, dia = st.peek(cand)
                    if dia[n] >> 1 == 1: s = cand; break
                col, dia = st.peek(s)
                phi = E(dia[n]); hit = 1 if dia[n] == c else 0
                pred = (Wc ^ (beta if s == 1 else 0)) & 1
                if pred != phi: alg_fail += 1
                assert H(s) == (m + Z) & 1
                seq.append((s, hit, prev == 1 and s == 1))
                nxt = Endpoint(); nxt.column, nxt.diagonal, nxt.length = col + [s], dia, st.length + 1
                st, prev = nxt, s
                tot += 1
            for i, (s, hit, bad) in enumerate(seq):
                by_e[s][0] += 1; by_e[s][1] += hit
                if bad: junction[s] += 1
                if i + 1 < len(seq):
                    key = (s, hit)
                    t = trans.setdefault(key, [0, 0]); t[0] += 1; t[1] += seq[i + 1][1]
                    te = trans_e.setdefault(key, [0, 0]); te[0] += 1; te[1] += (seq[i + 1][0] == 1)
        print(f"n={n} c={c}: columns={tot}, Phi = W + [e=1]*beta failures={alg_fail}")
        for s in (1, 2):
            k, h = by_e[s]
            print(f"   e_u={s}: {k} columns ({k/tot:.3f}), P(hit | e_u={s}) = {h/k:.3f}")
        for key in sorted(trans):
            k, h = trans[key]; ke, e1 = trans_e[key]
            print(f"   given (e_u={key[0]}, hit={key[1]}): P(hit_{{u+1}}) = {h/k:.3f}   P(e_{{u+1}}=1) = {e1/ke:.3f}   [{k}]")
        print(f"   hard-core violations (11) at e_u=1: {junction[1]} of {by_e[1][0]} = {junction[1]/max(1,by_e[1][0]):.3f}")
