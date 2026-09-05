#!/usr/bin/env python3
"""Anatomy of the survivor clusters that die together.

Two known clusters (BACKLOG.md section 8 K, RESULTS-BINARY-WEDGE-HORIZON.md
section 5):
  RW,   n = 9,  c = 3: six survivors persist through k = 5..8 and die at k = 9.
  BWH+, n = 15, c = 3: eighteen sources reach the 16-cell plateau and die at 17.

For each cluster this prints the member words, their forced continuations,
the reason each dies (no forceable H, wrong E, or a hard-core 11), the column
window at the death level with its Z / W2 / N counts, the diagonal trajectory
T[u][n] over the continuation, and the cells every member shares.  Complete
finite computation on the validated kernel; nothing is sampled.
"""
from __future__ import annotations

import argparse
from itertools import product

from backlog_screen_r1 import E, H, window_cells
from psi_kernel import Endpoint


def step_all(st: Endpoint, prev: int, n: int, c: int, hardcore: bool):
    """Every legal continuation symbol with its diagnostics."""
    out = []
    for s in (1, 2):
        col, dia = st.peek(s)
        h, e = H(dia[n]), E(dia[n])
        hc = not (hardcore and prev == 1 and s == 1)
        nxt = Endpoint()
        nxt.column, nxt.diagonal, nxt.length = col + [s], dia, st.length + 1
        out.append((s, dia[n], h, e, hc, nxt))
    return out


def deepest_orbits(n: int, c: int, hardcore: bool):
    """Return (depth, [(source, symbols, states)]) at the deepest level."""
    best, members = 0, []

    def walk(st, prev, src, syms, states, depth):
        nonlocal best, members
        if depth > best:
            best, members = depth, []
        if depth == best:
            members.append((src, tuple(syms), states + [st]))
        if depth >= 2 * n + 2:
            return
        for s, t, h, e, hc, nxt in step_all(st, prev, n, c, hardcore):
            if t == c and hc:
                walk(nxt, s, src, syms + [s], states + [st], depth + 1)

    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for s in src:
            st.append(s)
        walk(st, src[-1], src, [], [], 0)
    return best, members


def cause(st, prev, n, c, hardcore):
    parts = []
    for s, t, h, e, hc, _ in step_all(st, prev, n, c, hardcore):
        parts.append(f"e={s}: T[u][n]={t} (H={h},E={e}) hc={'ok' if hc else 'VIOL'}")
    forced = [x for x in step_all(st, prev, n, c, hardcore) if x[2] == 1]
    if not forced:
        verdict = "no forceable H"
    else:
        s, t, h, e, hc, _ = forced[0]
        if t != c:
            verdict = f"forced e={s} gives E={e}, need E={E(c)}"
        elif not hc:
            verdict = f"forced e={s} is a hard-core 11"
        else:
            verdict = "survives"
    return verdict, "; ".join(parts)


def report(n, c, hardcore, label):
    depth, members = deepest_orbits(n, c, hardcore)
    print(f"== {label}: n={n} c={c} hardcore={hardcore}: deepest={depth}, {len(members)} members")
    u = n + depth
    conts = {}
    windows = []
    for src, syms, states in members:
        st = states[-1]
        prev = (syms or src)[-1]
        verdict, detail = cause(st, prev, n, c, hardcore)
        w = window_cells(st, u, n)
        z = w.count(0)
        w2 = w.count(2)
        nz = len(w) - z
        traj = "".join(str(s_.diagonal[n]) for s_ in states[1:]) if depth else "-"
        conts.setdefault(syms, []).append(src)
        windows.append(w)
        print(f"  src={''.join(map(str, src))} cont={''.join(map(str, syms))}")
        print(f"     death: {verdict} [{detail}]")
        print(f"     window u-1={u-1} (m={len(w)}): {''.join(map(str, w))}  |Z|={z} |W2|={w2} |N|={nz}")
        print(f"     T[u][n] trajectory over continuation: {traj}")
        print(f"     diagonal Q at death: {''.join(map(str, st.diagonal))}")
    print(f"  distinct forced continuations: {len(conts)}")
    for k, v in conts.items():
        print(f"     {''.join(map(str, k))} <- {len(v)} sources")
    m = len(windows[0])
    shared = ["".join(str(w[i]) for w in windows) for i in range(m)]
    agree = "".join(s[0] if len(set(s)) == 1 else "." for s in shared)
    print(f"  shared window cells (d=-u..n-1, '.' = differs): {agree}  ({agree.count('.')} of {m} differ)")
    keys = {(tuple(st.column), tuple(st.diagonal)) for _, _, states in members for st in states[:1]}
    print(f"  distinct full endpoint states at k=0 among members: {len(keys)}")
    srcs = [s for s, _, _ in members]
    agree_src = "".join(str(srcs[0][i]) if len({s[i] for s in srcs}) == 1 else "." for i in range(n))
    print(f"  shared source bits: {agree_src}")
    cs = 0
    while cs < n and len({s[n - 1 - cs] for s in srcs}) == 1:
        cs += 1
    print(f"  common source suffix length: {cs}")
    zs = sorted({w.count(0) for w in windows})
    w2s = sorted({w.count(2) for w in windows})
    print(f"  |Z| values: {zs}; |W2| values: {w2s}")
    print()


def merge_levels(n, c, hardcore):
    """Per level: sources alive, distinct endpoint states alive, largest fibre."""
    by_level = {}

    def walk(st, prev, depth):
        key = (tuple(st.column), tuple(st.diagonal))
        by_level.setdefault(depth, {}).setdefault(key, 0)
        by_level[depth][key] += 1
        if depth >= 2 * n + 2:
            return
        for s, t, h, e, hc, nxt in step_all(st, prev, n, c, hardcore):
            if t == c and hc:
                walk(nxt, s, depth + 1)

    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for s in src:
            st.append(s)
        walk(st, src[-1], 0)
    return by_level


def state_census(min_n, max_n, hardcore):
    print(f"== survivors counted as sources vs as distinct endpoint states, hardcore={hardcore}")
    print("   (the state at k=0 is (Q_n, Psi_n) with the source appended; a fibre is one state's preimage)")
    for n in range(min_n, max_n + 1):
        for c in (2, 3):
            lv = merge_levels(n, c, hardcore)
            row = []
            for k in sorted(lv):
                fib = lv[k]
                row.append(f"{sum(fib.values())}/{len(fib)}/{max(fib.values())}")
            print(f"  n={n:<3}c={c}: k=0..: " + " ".join(row))
    print("   entries are sources/states/max-fibre per level")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--extra", action="store_true", help="also n=12 c=2 RW and n=16 c=3 RW")
    p.add_argument("--census", type=int, default=0, help="state census for n=6..N (RW)")
    a = p.parse_args()
    report(9, 3, True, "RW cluster")
    report(15, 3, False, "BWH+ cluster")
    if a.extra:
        report(12, 2, True, "RW")
        report(16, 3, True, "RW")
    if a.census:
        state_census(6, a.census, True)


if __name__ == "__main__":
    main()
