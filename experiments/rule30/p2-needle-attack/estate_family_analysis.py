#!/usr/bin/env python3
"""Family + null analysis of the extremal forcing STATES (reads
estate_census.json).  Implements tests (i),(ii),(iii) of estate_PREREG.md with
the preregistered null model and thresholds.  Prints a structured report.
"""
from __future__ import annotations

import json
import random
import statistics
from itertools import combinations
from pathlib import Path

CENSUS = Path(__file__).with_name("estate_census.json")
NS = list(range(10, 21))
ARMS = ("all", "hardcore")
CS = (2, 3)


def lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def lcs(a, b):
    n = 0
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            break
        n += 1
    return n


def agree(a, b, alignment):
    return lcp(a, b) if alignment == "prefix" else lcs(a, b)


def load():
    cells = json.loads(CENSUS.read_text())
    return cells


def extremal_states(cells, n, c, arm):
    key = f"n{n}_c{c}_{arm}"
    if key not in cells:
        return None
    return [tuple(e["live_state"]) for e in cells[key]["extremal"]]


def typical(cells, n, c, arm):
    key = f"n{n}_c{c}_{arm}"
    if key not in cells:
        return []
    return [tuple(t) for t in cells[key]["typical_sample"]]


def pctl(data, p):
    if not data:
        return 0.0
    data = sorted(data)
    k = (len(data) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(data) - 1)
    return data[lo] + (data[hi] - data[lo]) * (k - lo)


# ---- Section B: within-cell forgetting (archaeology 2.2 reproduction) ------
def section_B(cells):
    print("=" * 78)
    print("B. Within-cell: multiple extremal states sharing a continuation")
    print("   (archaeology 2.2: should differ only in newest 1-2 high-index cells)")
    print("=" * 78)
    worst = 0
    checked = 0
    for arm in ARMS:
        for c in CS:
            for n in NS:
                key = f"n{n}_c{c}_{arm}"
                if key not in cells:
                    continue
                ex = cells[key]["extremal"]
                bycont = {}
                for e in ex:
                    bycont.setdefault(tuple(e["continuation"][:e["survival"]]), []).append(e)
                for cont, group in bycont.items():
                    if len(group) < 2:
                        continue
                    states = [tuple(e["live_state"]) for e in group]
                    # all same length; count cells differing from the first
                    L = len(states[0])
                    diffidx = sorted({i for s in states[1:]
                                      for i in range(L) if s[i] != states[0][i]})
                    checked += 1
                    # how deep (high index) are the differences?
                    topmost = L - 1 - min(diffidx) if diffidx else -1
                    worst = max(worst, len(diffidx))
                    print(f"  {key}: {len(group)} states, same continuation; "
                          f"differing cell indices={diffidx} "
                          f"(state len {L}; distance-from-top={sorted(L-1-i for i in diffidx)})")
    print(f"  --> {checked} multi-state continuation-classes; "
          f"max #differing cells in any class = {worst}")
    return worst


# ---- Section C: test (i) cross-n agreement vs null -------------------------
def section_C(cells):
    print("=" * 78)
    print("C. Test (i): extremal-state agreement across consecutive n vs NULL")
    print("   family iff A_a >= A_b(p95)+2 for >=70% of pairs in some (arm,align)")
    print("=" * 78)
    summary = {}
    for arm in ARMS:
        for c in CS:
            for alignment in ("prefix", "suffix"):
                rows = []
                for n in NS[:-1]:
                    Sn = extremal_states(cells, n, c, arm)
                    Sn1 = extremal_states(cells, n + 1, c, arm)
                    if not Sn or not Sn1:
                        continue
                    # (a) best extremal-extremal
                    Aa = max(agree(s, s2, alignment) for s in Sn for s2 in Sn1)
                    # (b) null: extremal(n) vs typical(n+1)
                    typ = typical(cells, n + 1, c, arm)
                    nulls = [agree(s, t, alignment) for s in Sn for t in typ]
                    Ab = pctl(nulls, 0.95)
                    nmed = statistics.median(nulls) if nulls else 0
                    rows.append((n, Aa, Ab, nmed, Aa - Ab))
                if not rows:
                    continue
                frac = sum(1 for r in rows if r[4] >= 2) / len(rows)
                summary[(arm, c, alignment)] = frac
                print(f"\n  arm={arm} c={c} align={alignment}: "
                      f"{sum(1 for r in rows if r[4]>=2)}/{len(rows)} pairs "
                      f"with A_a-p95(null)>=2  (frac={frac:.2f})")
                for n, Aa, Ab, nmed, sep in rows:
                    flag = " *" if sep >= 2 else ""
                    print(f"     n={n}->{n+1}: A_a={Aa:2d}  null_med={nmed:.1f} "
                          f"null_p95={Ab:.1f}  sep={sep:+.1f}{flag}")
    best = max(summary.values()) if summary else 0
    print(f"\n  --> best fraction over all (arm,c,align) = {best:.2f} "
          f"(family threshold 0.70)")
    return summary


# ---- Section D: test (ii) fixed operation ----------------------------------
def section_D(cells):
    print("=" * 78)
    print("D. Test (ii): fixed operation relating extremal state n -> n+1")
    print("=" * 78)
    for arm in ARMS:
        for c in CS:
            o1 = o2 = tot = 0
            src_lcs = []
            for n in NS[:-1]:
                Sn = extremal_states(cells, n, c, arm)
                Sn1 = extremal_states(cells, n + 1, c, arm)
                if not Sn or not Sn1:
                    continue
                tot += 1
                # o1: some s' has s as prefix (low-index extension)
                if any(s2[:len(s)] == s for s in Sn for s2 in Sn1):
                    o1 += 1
                # o2: some s' has s as high-index suffix
                if any(s2[-len(s):] == s for s in Sn for s2 in Sn1):
                    o2 += 1
                # cocycle proxy: longest common suffix of extremal SOURCE words
                kw = f"n{n}_c{c}_{arm}"
                kw1 = f"n{n+1}_c{c}_{arm}"
                w = [tuple(e["rep_word"]) for e in cells[kw]["extremal"]]
                w1 = [tuple(e["rep_word"]) for e in cells[kw1]["extremal"]]
                src_lcs.append(max(lcs(a, b) for a in w for b in w1))
            if tot:
                print(f"  arm={arm} c={c}: o1(prefix-extend)={o1}/{tot} "
                      f"o2(suffix-extend)={o2}/{tot}  "
                      f"src-word LCS across n (per pair)={src_lcs}")
    # o3 cocycle: is each extremal source word 2^k . (fixed core)?
    print("\n  o3 cocycle signature: leading-2 run + trailing core, per cell")
    for arm in ("hardcore",):  # the arm the template wants
        for c in CS:
            print(f"   arm={arm} c={c}:")
            for n in NS:
                kw = f"n{n}_c{c}_{arm}"
                if kw not in cells:
                    continue
                for e in cells[kw]["extremal"]:
                    w = e["rep_word"]
                    k = 0
                    while k < len(w) and w[k] == 2:
                        k += 1
                    print(f"     n={n} W={''.join(map(str,w))} "
                          f"lead2={k} core={''.join(map(str,w[k:]))} "
                          f"cont={''.join(map(str,e['continuation'][:e['survival']]))}")


# ---- Section E: test (iii) alpha support -----------------------------------
def section_E(cells):
    print("=" * 78)
    print("E. Test (iii): alpha SUPPORT at killing row across n")
    print("   (support = nonzero cells of live state; parity re-encodes the")
    print("    string and is NOT reported as new -- only the support geometry)")
    print("=" * 78)
    for arm in ARMS:
        for c in CS:
            print(f"\n  arm={arm} c={c}:")
            for n in NS:
                kw = f"n{n}_c{c}_{arm}"
                if kw not in cells:
                    continue
                for e in cells[kw]["extremal"][:1]:  # one representative
                    prof = e["alpha_profile"]
                    if not prof:
                        continue
                    kill = prof[-1]  # row == survival
                    aseq = "".join(str(p["alpha"]) for p in prof)
                    sp = kill["support_prefix"]
                    ss = kill["support_suffix"]
                    print(f"     n={n} surv={e['survival']} killer={e['killer']} "
                          f"alpha_seq={aseq}")
                    print(f"          kill support (from index0, first/last 6)="
                          f"{sp[:6]}..{sp[-6:]} |supp|={len(sp)}")
                    print(f"          kill support (depth from cut, sorted first 8)="
                          f"{ss[:8]}")


def main():
    cells = load()
    print(f"loaded {len(cells)} cells from {CENSUS.name}\n")
    section_B(cells)
    summary = section_C(cells)
    section_D(cells)
    section_E(cells)
    print("\n" + "=" * 78)
    best = max(summary.values()) if summary else 0
    print(f"VERDICT test (i): best cross-n separation fraction = {best:.2f}; "
          f"threshold 0.70 -> {'FAMILY' if best >= 0.70 else 'NO FAMILY'}")
    print("=" * 78)


if __name__ == "__main__":
    main()
