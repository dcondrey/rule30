"""R8 diagnostic: block-frequency sup-deviation of the Rule 30 center column
against an i.i.d. Bernoulli(1/2) null, with the Rule 90 center column as the
pipeline control.  Pre-registered in
docs/rule30/RESULTS-orbit-closure-diagnostic.md; read that before editing
the metric, depths, or decision rule.

Usage:
    uv run python orbit_closure_diagnostic.py --gen-only 30 --steps T
    uv run python orbit_closure_diagnostic.py --gen-only 90 --steps T
    uv run python orbit_closure_diagnostic.py --steps T --out results.json
    uv run python orbit_closure_diagnostic.py --tables results.json
"""
import argparse, json, math, os, sys, time

import numpy as np

# OEIS A051023, first 60 terms, fetched 2026-08-30 from
# https://oeis.org/search?q=id:A051023&fmt=json
A051023 = [int(x) for x in
           "1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,0,0,1,1,1,0,1,0,1,1,"
           "1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,0".split(",")]

LS = [1, 2, 4, 8, 12]
WS = [2 ** 12, 2 ** 14, 2 ** 16, 2 ** 18, 2 ** 20]
DEPTHS = [0, 2 ** 10, 2 ** 12, 2 ** 14, 2 ** 16, 2 ** 18, 2 ** 19, 3 * 2 ** 18, 10 ** 6]
NSEEDS = 20
HERE = os.path.dirname(os.path.abspath(__file__))


def gen_column(rule: int, steps: int) -> np.ndarray:
    """Bit-parallel lone-seed center column.  Rule 30 recurrence is the one in
    experiments/rule30/center_column.py; rule 90 is new = (row<<1) ^ (row>>1)."""
    off = steps + 2
    row = 1 << off
    mask = 1 << off
    out = np.zeros(steps, dtype=np.uint8)
    if rule == 30:
        for t in range(steps):
            out[t] = 1 if row & mask else 0
            row = (row << 1) ^ (row | (row >> 1))
    elif rule == 90:
        for t in range(steps):
            out[t] = 1 if row & mask else 0
            row = (row << 1) ^ (row >> 1)
    else:
        raise ValueError(rule)
    return out


def cached_column(rule: int, steps: int) -> np.ndarray:
    path = os.path.join(HERE, f"col{rule}_{steps}.bin")
    if os.path.exists(path):
        col = np.fromfile(path, dtype=np.uint8)
        assert len(col) == steps, (path, len(col))
        return col
    t = time.time()
    col = gen_column(rule, steps)
    col.tofile(path)
    print(f"generated rule {rule} column, T={steps}, {time.time()-t:.1f}s", file=sys.stderr)
    return col


def block_codes(w: np.ndarray, L: int) -> np.ndarray:
    n = len(w) - L + 1
    codes = np.zeros(n, dtype=np.int64)
    for j in range(L):
        codes = (codes << 1) | w[j:j + n].astype(np.int64)
    return codes


def D_stat(w: np.ndarray, L: int):
    """(max |freq(b) - 2^-L|, freq of block b=1 for L=1 else None)."""
    codes = block_codes(w, L)
    freq = np.bincount(codes, minlength=2 ** L) / len(codes)
    dev = np.abs(freq - 2.0 ** -L)
    f1 = float(freq[1]) if L == 1 else None
    return float(dev.max()), f1, int(dev.argmax())


def depths_for(W: int, T: int):
    ds = [d for d in DEPTHS if d + W <= T]
    last = T - W
    if last not in ds:
        ds.append(last)
    return sorted(ds)


def analyze(col: np.ndarray, T: int):
    res = {}
    for L in LS:
        res[str(L)] = {}
        for W in WS:
            cells = []
            for t0 in depths_for(W, T):
                d, f1, argb = D_stat(col[t0:t0 + W], L)
                cells.append({"t0": t0, "D": d, "freq1": f1, "argmax_block": argb})
            res[str(L)][str(W)] = {"S": max(c["D"] for c in cells), "cells": cells}
    return res


def analytic_scale(L: int, W: int) -> float:
    p = 2.0 ** -L
    return math.sqrt(p * (1 - p) / W) * math.sqrt(2 * L * math.log(2))


def run(steps: int, out: str):
    col30 = cached_column(30, steps)
    assert list(col30[:len(A051023)]) == A051023, "A051023 mismatch"
    col90 = cached_column(90, steps)
    assert col90[0] == 1 and not col90[1:].any(), "rule 90 center column is not 1,0,0,..."
    results = {"T": steps, "LS": LS, "WS": WS, "nseeds": NSEEDS,
               "rule30": analyze(col30, steps), "rule90": analyze(col90, steps), "seeds": []}
    t = time.time()
    for s in range(NSEEDS):
        rng = np.random.default_rng(s)
        bits = rng.integers(0, 2, size=steps, dtype=np.uint8)
        results["seeds"].append(analyze(bits, steps))
    print(f"null seeds: {time.time()-t:.1f}s", file=sys.stderr)
    with open(out, "w") as f:
        json.dump(results, f)
    print(f"wrote {out}", file=sys.stderr)


def tables(path: str):
    R = json.load(open(path))
    T = R["T"]
    seeds = R["seeds"]
    exceed = 0
    slopes = {}
    print(f"T = {T}, seeds = {len(seeds)}\n")
    for L in LS:
        print(f"### L = {L}: S(L, W) = sup over depth of max-block deviation\n")
        print("| W | S rule 30 | analytic scale | seed min | seed mean | seed sd | seed max | exceeds seed max |")
        print("|---:|---:|---:|---:|---:|---:|---:|:---:|")
        xs, ys = [], []
        for W in WS:
            s30 = R["rule30"][str(L)][str(W)]["S"]
            ss = np.array([sd[str(L)][str(W)]["S"] for sd in seeds])
            ex = s30 > ss.max()
            exceed += ex
            xs.append(math.log2(W)); ys.append(math.log2(s30))
            print(f"| 2^{int(math.log2(W))} | {s30:.3e} | {analytic_scale(L, W):.3e} | {ss.min():.3e} | "
                  f"{ss.mean():.3e} | {ss.std(ddof=1):.3e} | {ss.max():.3e} | {'YES' if ex else 'no'} |")
        slope = float(np.polyfit(xs, ys, 1)[0])
        slopes[L] = slope
        seed_slopes = []
        for sd in seeds:
            sy = [math.log2(sd[str(L)][str(W)]["S"]) for W in WS]
            seed_slopes.append(float(np.polyfit(xs, sy, 1)[0]))
        print(f"\nslope of log2 S vs log2 W: rule 30 **{slope:+.3f}**; seeds mean {np.mean(seed_slopes):+.3f}, "
              f"sd {np.std(seed_slopes, ddof=1):.3f}, range [{min(seed_slopes):+.3f}, {max(seed_slopes):+.3f}]\n")
    print(f"**Cells exceeding the seed max: {exceed} of {len(LS)*len(WS)}** (null expectation about 1.2; 4 or more flags criterion C).\n")

    print("### L = 1, per depth: freq(1) and deviation in null s.d. units (0.5/sqrt(W))\n")
    hdr = "| t0 | " + " | ".join(f"W=2^{int(math.log2(W))}" for W in WS) + " |"
    print(hdr); print("|---:|" + "---:|" * len(WS))
    all_depths = sorted({c["t0"] for W in WS for c in R["rule30"]["1"][str(W)]["cells"]})
    driftA = 0
    for t0 in all_depths:
        row = [f"{t0}"]
        for W in WS:
            cell = next((c for c in R["rule30"]["1"][str(W)]["cells"] if c["t0"] == t0), None)
            if cell is None:
                row.append("")
            else:
                z = (cell["freq1"] - 0.5) / (0.5 / math.sqrt(W))
                row.append(f"{cell['freq1']:.5f} ({z:+.2f})")
        print("| " + " | ".join(row) + " |")
    for W in WS:
        if W >= 2 ** 16:
            deepest = R["rule30"]["1"][str(W)]["cells"][-1]
            z = abs(deepest["freq1"] - 0.5) / (0.5 / math.sqrt(W))
            driftA += z > 3
    print(f"\nCriterion A (drift, deepest window, |z| > 3 at two or more W >= 2^16): count = {driftA}\n")

    print("### L = 8, per depth: D(8, W, t0), seed max in brackets per column\n")
    print(hdr); print("|---:|" + "---:|" * len(WS))
    for t0 in all_depths:
        row = [f"{t0}"]
        for W in WS:
            cell = next((c for c in R["rule30"]["8"][str(W)]["cells"] if c["t0"] == t0), None)
            row.append("" if cell is None else f"{cell['D']:.3e}")
        print("| " + " | ".join(row) + " |")
    print("| seed max | " + " | ".join(f"{max(sd['8'][str(W)]['S'] for sd in seeds):.3e}" for W in WS) + " |")

    plateau = []
    for L in [1, 2, 4, 8]:
        top2 = [R["rule30"][str(L)][str(W)]["S"] > max(sd[str(L)][str(W)]["S"] for sd in seeds) for W in WS[-2:]]
        if slopes[L] > -0.25 and all(top2):
            plateau.append(L)
    print(f"\nCriterion B (plateau: slope > -0.25 and both largest W exceed seed max): L values = {plateau or 'none'}")
    ok_slopes = all(-0.65 <= slopes[L] <= -0.35 for L in [1, 2, 4, 8])
    print(f"Criterion C (4+ cells exceed seed max): {'FIRES' if exceed >= 4 else 'does not fire'}")
    verdict = ("EVIDENCE AGAINST unique ergodicity" if (driftA >= 2 or plateau or exceed >= 4)
               else ("CONSISTENT WITH unique ergodicity (proves nothing)" if (exceed <= 3 and ok_slopes)
                     else "INCONCLUSIVE"))
    print(f"\n**Pre-registered verdict: {verdict}**\n")

    print("### Rule 90 control: D(L, W, t0) must equal 1 - 2^-L for every t0 >= 1\n")
    print("| L | W | t0 = 0 | min over t0 >= 1 | max over t0 >= 1 | 1 - 2^-L | seed max | flagged |")
    print("|---:|---:|---:|---:|---:|---:|---:|:---:|")
    control_ok = True
    for L in LS:
        for W in WS:
            cells = R["rule90"][str(L)][str(W)]["cells"]
            d0 = next(c["D"] for c in cells if c["t0"] == 0)
            rest = [c["D"] for c in cells if c["t0"] >= 1]
            smax = max(sd[str(L)][str(W)]["S"] for sd in seeds)
            target = 1 - 2.0 ** -L
            flagged = min(rest) > smax and abs(min(rest) - target) < 1e-9 and abs(max(rest) - target) < 1e-9
            control_ok &= flagged
            print(f"| {L} | 2^{int(math.log2(W))} | {d0:.6f} | {min(rest):.6f} | {max(rest):.6f} | {target:.6f} | {smax:.3e} | {'YES' if flagged else 'NO'} |")
    print(f"\n**Rule 90 control: {'PASSED, pipeline flags the periodic column at every cell' if control_ok else 'FAILED, pipeline broken'}**")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2_000_000)
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--gen-only", type=int, default=None)
    ap.add_argument("--tables", default=None)
    a = ap.parse_args()
    if a.tables:
        tables(a.tables)
    elif a.gen_only:
        cached_column(a.gen_only, a.steps)
    else:
        run(a.steps, a.out)
