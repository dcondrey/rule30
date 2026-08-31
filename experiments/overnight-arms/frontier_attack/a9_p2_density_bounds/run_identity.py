"""Exact centre-run identity for Rule 30, and its adversarial controls.

CLAIM UNDER TEST (Identity R).  Let y be a nonzero finite Rule 30 row and let
c(t) = F^t(y)_0 be its centre trace.  Let v = c(0).  Define the *forced left
half* of y at depth k >= 1:

  v = 0 :  the prefix-OR transducer of RESULTS-zero-tail.md lines 52-55,
           P_(2k+1) = OR(R_1..R_(2k+1)),
           P_(2k)   = R_(2k) AND NOT OR(R_1..R_(2k-1)),      R_j = y(+j)
  v = 1 :  P_k = 1 iff k is even          (RESULTS-eventual-period.md, all-one fibre)

and let D(y) = min{ k >= 1 : y(-k) != P_k }.  Then

  run(y) := #{ leading t with c(t) = v }  ==  D(y).

Everything here is EXACT COMPUTATION.  The identity's proof is in
p2_density_bounds.md; the runs below are validation of the implementation and
of the two published horizon tables, not evidence for any infinite statement.

Run:  PYTHONDONTWRITEBYTECODE=1 uv run python run_identity.py
"""

from __future__ import annotations

import itertools
import random
import sys

REPO = "/Volumes/A/researchpapers/13-rule30"
sys.path.insert(0, REPO + "/experiments/overnight-arms")

from common.rule30 import cell, rows_frame, simulate_seed  # noqa: E402

OUT: list[str] = []


def say(msg: str = "") -> None:
    OUT.append(msg)
    print(msg)


# --------------------------------------------------------------------------
# forced left halves
# --------------------------------------------------------------------------


def forced_zero(right: list[int], depth: int) -> list[int]:
    """P_1..P_depth for the all-zero trace, from R_1.. = right[0].. .

    Uses the transducer verbatim; the closed form 'k mod 2 beyond the least
    one' is NOT used, because it is false at k = m (and for m >= 2 the pattern
    is not alternating at all).
    """
    p = [0] * (depth + 1)
    for k in range(1, depth + 1):
        rk = right[k - 1] if k - 1 < len(right) else 0
        pre_below = 1 if any(right[: k - 1]) else 0  # OR(R_1..R_(k-1))
        if k % 2 == 1:
            p[k] = 1 if (pre_below or rk) else 0
        else:
            p[k] = 1 if (rk and not pre_below) else 0
    return p[1:]


def forced_one(depth: int) -> list[int]:
    return [1 if k % 2 == 0 else 0 for k in range(1, depth + 1)]


# --------------------------------------------------------------------------
# generic finite-row machinery (dict rows, independent of the frame trick)
# --------------------------------------------------------------------------


def trace_run(seed: dict[int, int], limit: int) -> int:
    """Length of the leading constant run of the centre trace, capped at limit."""
    grid = simulate_seed(seed, limit + 1)
    v = grid[0].get(0, 0)
    n = 0
    for t in range(limit + 1):
        if grid[t].get(0, 0) != v:
            break
        n += 1
    return n


def depth_D(seed: dict[int, int], depth: int) -> int | None:
    """D(y), or None if no mismatch within `depth`.  Reads the ROW only."""
    v = seed.get(0, 0)
    if v == 0:
        right = [seed.get(j, 0) for j in range(1, depth + 2)]
        p = forced_zero(right, depth)
    else:
        p = forced_one(depth)
    for k in range(1, depth + 1):
        if seed.get(-k, 0) != p[k - 1]:
            return k
    return None


# --------------------------------------------------------------------------
# gate 1: reproduce the two published horizon tables from D alone
# --------------------------------------------------------------------------


def gate_horizon_tables(max_w: int = 8) -> bool:
    say("## Gate 1 - published horizon tables, recomputed two ways")
    say("")
    say("| w | zero H_max (sim) | 2*ceil(w/2) | extremal | 2^w-1 "
        "| one H_max (sim) | formula | extremizers | 2^w |")
    say("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    ok = True
    for w in range(1, max_w + 1):
        zh = zn = oh = on = -1
        zh, oh = -1, -1
        zn = on = 0
        for bits in itertools.product([0, 1], repeat=2 * w + 1):
            if not any(bits):
                continue
            seed = {x - w: b for x, b in enumerate(bits) if b}
            v = seed.get(0, 0)
            # inclusive horizon H: max H with c(t)=v for 0<=t<=H  ==  run-1
            h = trace_run(seed, 4 * w + 8) - 1
            if v == 0:
                if h > zh:
                    zh, zn = h, 1
                elif h == zh:
                    zn += 1
            else:
                if h > oh:
                    oh, on = h, 1
                elif h == oh:
                    on += 1
            # identity check on every row in the exhaustive space
            d = depth_D(seed, 4 * w + 8)
            if d != h + 1:
                ok = False
                say(f"  IDENTITY VIOLATION w={w} row={seed} run={h + 1} D={d}")
        zf = 2 * ((w + 1) // 2)
        of = w + 1 if w % 2 == 0 else w
        say(f"| {w} | {zh} | {zf} | {zn} | {2**w - 1} | {oh} | {of} | {on} | {2**w} |")
        ok &= (zh == zf) and (zn == 2**w - 1) and (oh == of) and (on == 2**w)
    say("")
    say(f"Gate 1: {'PASS' if ok else 'FAIL'}  (both tables reproduced; identity holds "
        f"on every nonzero row of radius <= {max_w}: "
        f"{sum(2 ** (2 * w + 1) - 1 for w in range(1, max_w + 1)):,} rows)")
    say("")
    return ok


# --------------------------------------------------------------------------
# gate 2: random finite rows (the disconfirming population)
# --------------------------------------------------------------------------


def gate_random_rows(n: int = 4000, seed: int = 30) -> bool:
    rng = random.Random(seed)
    ok = True
    worst = 0
    for _ in range(n):
        w = rng.randint(1, 14)
        bits = [rng.randint(0, 1) for _ in range(2 * w + 1)]
        if not any(bits):
            continue
        row = {x - w: b for x, b in enumerate(bits) if b}
        cap = 4 * w + 12
        run = trace_run(row, cap)
        d = depth_D(row, cap)
        worst = max(worst, run)
        if d != run:
            ok = False
            say(f"  RANDOM VIOLATION row={row} run={run} D={d}")
    say(f"Gate 2 (random finite rows, n={n}, radius 1..14): "
        f"{'PASS' if ok else 'FAIL'}; longest run seen {worst}")
    say("")
    return ok


# --------------------------------------------------------------------------
# gate 3: the lone seed
# --------------------------------------------------------------------------


def gate_lone_seed(tmax: int = 3000) -> bool:
    frames = rows_frame(2 * tmax + 16)
    col = [cell(frames[t], t, 0) for t in range(2 * tmax + 16)]

    # cross-check the row extraction against the independent naive simulator
    grid = simulate_seed({0: 1}, 300)
    for t in range(300):
        for x in range(-t - 2, t + 3):
            assert cell(frames[t], t, x) == grid[t].get(x, 0), (t, x)
    say("Gate 3a: frame-trick row extraction == naive simulator, all cells, t<300. PASS")

    ok = True
    ds = []
    m_hist: dict[int, int] = {}
    for T in range(1, tmax + 1):
        v = col[T]
        run = 0
        while col[T + run] == v:
            run += 1
        depth = run + 4
        row = {x: cell(frames[T], T, x) for x in range(-depth - 2, T + 1)}
        row = {x: b for x, b in row.items() if b}
        d = depth_D(row, depth)
        if d != run:
            ok = False
            say(f"  LONE-SEED VIOLATION T={T} run={run} D={d}")
        ds.append(run)
        if v == 0:
            m = next((j for j in range(1, T + 2)
                      if cell(frames[T], T, j)), 0)
            m_hist[m] = m_hist.get(m, 0) + 1
    say(f"Gate 3b: identity holds for every T in 1..{tmax}: {'PASS' if ok else 'FAIL'}")
    say(f"  max D(T) over that range = {max(ds)}  (EXACT COMPUTATION, validation only)")
    say(f"  m = index of nearest right-hand one, over centre-zero T: "
        + ", ".join(f"m={k}: {c}" for k, c in sorted(m_hist.items())))
    say("")

    # Theorem A of row 47, re-derived here as a corollary and re-checked
    import math
    bad1 = bad0 = 0
    n1 = n0 = 0
    for T in range(1, tmax + 1):
        n1 += col[T]
        n0 += 1 - col[T]
        if n1 < math.floor(math.log2(T + 4)) - 1:
            bad1 += 1
        if n0 < math.floor(math.log2(T + 6)) - 2:
            bad0 += 1
    say(f"Gate 3c: row 47 Theorem A, violations in 1..{tmax}: "
        f"N_1(T) >= floor(log2(T+4))-1 -> {bad1}; "
        f"N_0(T) >= floor(log2(T+6))-2 -> {bad0}  "
        f"(re-check only; the bound is NOT new here)")
    say("")
    return ok


# --------------------------------------------------------------------------
# gate 4: Rule 90 control
# --------------------------------------------------------------------------


def gate_rule90(tmax: int = 4096) -> bool:
    row = {0: 1}
    col = []
    for _ in range(tmax):
        col.append(row.get(0, 0))
        lo, hi = min(row) - 1, max(row) + 1
        row = {x: 1 for x in range(lo, hi + 1)
               if row.get(x - 1, 0) ^ row.get(x + 1, 0)}
    ones = [t for t, b in enumerate(col) if b]
    say(f"Gate 4a: Rule 90 lone-seed centre column, t<{tmax}: ones at {ones} "
        f"-> identically 0 for t>=1, density 0.")

    # the zero-trace fibre of Rule 90 is not a singleton: {-1,+1}
    r90 = {-1: 1, 1: 1}
    cur = dict(r90)
    zero = True
    for _ in range(256):
        if cur.get(0, 0):
            zero = False
            break
        lo, hi = min(cur) - 1, max(cur) + 1
        cur = {x: 1 for x in range(lo, hi + 1)
               if cur.get(x - 1, 0) ^ cur.get(x + 1, 0)}
    say(f"Gate 4b: Rule 90 finite row {{-1,+1}} has centre 0 through t=256: {zero}. "
        f"So Rule 90's zero-trace fibre contains a nonzero finite row, no left half "
        f"is forced, and D is UNDEFINED for Rule 90. The identity has no Rule 90 "
        f"analogue and cannot leak a positive-density conclusion to it.")
    say("")
    return len(ones) == 1 and ones[0] == 0 and zero


def gate_forced_depends_only_on_m(maxlen: int = 16) -> bool:
    """The zero-trace forced left half depends on the right half ONLY through
    m = least j with R_j = 1.  Closed form: P_k = 0 (k<m), P_m = 1,
    P_k = k mod 2 (k>m).  Exhaustive over every right word of length <= maxlen.
    """
    ok = True
    for n in range(1, maxlen + 1):
        for bits in itertools.product([0, 1], repeat=n):
            right = list(bits)
            p = forced_zero(right, n)
            m = next((j for j in range(1, n + 1) if right[j - 1]), None)
            if m is None:
                closed = [0] * n
            else:
                closed = [0 if k < m else (1 if k == m else k % 2)
                          for k in range(1, n + 1)]
            if p != closed:
                ok = False
                say(f"  FORCED-FORM VIOLATION right={right} p={p} closed={closed}")
    say(f"Gate 5 (forced zero-trace left half is a function of m alone, closed form "
        f"0^(m-1) 1 then k mod 2; exhaustive over all {2 ** (maxlen + 1) - 2:,} right "
        f"words of length <= {maxlen}): {'PASS' if ok else 'FAIL'}")
    say("  Consequence: every structure theorem about the right cone (Rowland 2006 "
        "Lemma 2 power-of-two periodic diagonals; row 47 obstruction 2) is inert for "
        "this criterion - only m survives.")
    say("  Note P_m = 1 and P_(m+1) = (m+1) mod 2, so for EVEN m the forced pattern "
        "has two adjacent ones at m, m+1 and is not alternating there.")
    say("")
    return ok


def main() -> None:
    results = {
        "gate1_horizon_tables": gate_horizon_tables(8),
        "gate2_random_rows": gate_random_rows(),
        "gate3_lone_seed": gate_lone_seed(3000),
        "gate4_rule90": gate_rule90(),
        "gate5_forced_form": gate_forced_depends_only_on_m(14),
    }
    say("## Summary")
    for k, v in results.items():
        say(f"- {k}: {'PASS' if v else 'FAIL'}")
    with open("identity_output.txt", "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
