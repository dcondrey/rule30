"""a23: empirical Myhill-Nerode index lower bound for Lemma S' (row41
streaming compressibility, see a22_row41_alt_strategy/alt_strategy.md part B).

Read-only reuse of a5's band_automaton.py (BA.forced_step, BA.forced_step_90,
BA.seed_state), itself read-only reuse of the repo probe -- same import
pattern as a22/bilinear_decomp_check.py.

What this measures
-------------------
For a fixed left-depth d = 2*kseed, enumerate ALL 2^kseed rho-seeds (both
phases). For each seed, run the UNCONDITIONAL forced map (no halting on pin
failure -- the same convention BA's own parity_sequence/window_test already
use: the forced formula is evaluated at every substep regardless of whether
the pin constraint par==1 would actually hold for a real surviving orbit)
for `pairs + W` rho/pin pairs, recording:
  rho_bits[s]  := forced_step's `par` output at the rho substep of pair s
  pin_bits[s]  := forced_step's `par` output at the pin substep of pair s

At each pair-index s in [0, pairs), define:
  rho-prefix(s, seed) := tuple(rho_bits[0 .. s])       (what a streaming
                          transducer would have read so far)
  future-window(s, seed) := tuple(pin_bits[s .. s+W))  (what it would need
                          to predict, W steps of lookahead)

index_lower_bound(s) := number of DISTINCT future-window values realized
across all seeds at that s. This under-counts the true Myhill-Nerode index
(two seeds with an identical W-window may still require different states
for a longer future), but never over-counts (two seeds with genuinely
different infinite futures must diverge within SOME finite window, so this
bound tightens monotonically as W grows -- see PREREGISTRATION.md).

Also flagged: `n_anomalous_prefixes(s)` = number of DISTINCT rho-prefix
strings that are shared by two seeds whose future-W-windows differ. This is
a stronger, out-of-scope-but-worth-reporting event: it would mean no
finite-state device of ANY size (bounded or not) can predict the future from
the visible rho-bit stream alone, since two seeds sharing a rho-prefix ought
to be indistinguishable to any reader of that stream.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "a5_row41_fiber_uniform"))
import band_automaton as BA  # noqa: E402  (READ-ONLY reuse)


def full_sequence(u, v, phase, steps, step_fn):
    """Run `steps` rho/pin PAIRS of the forced map, unconditionally (no
    halting on pin failure -- matches BA.parity_sequence's own convention).
    Returns (rho_bits, pin_bits), each a list of length `steps`."""
    rho_bits = []
    pin_bits = []
    for _ in range(steps):
        u, v, r = step_fn(u, v, phase)
        rho_bits.append(r)
        u, v, p = step_fn(u, v, phase)
        pin_bits.append(p)
    return rho_bits, pin_bits


def drive_step_90(u, v, phase, drive):
    """General-drive Rule 90 step, mirroring how BA.validate() derives a
    general-drive Rule 30 step from the forced (zero-output) one:

        delta = drive ^ par
        u2 == [x ^ delta for x in nxt[:-1]] + [nxt[-1]]

    (band_automaton.py lines ~130-133). forced_step_90 has no drive
    parameter at all (it is the unconditional, always-zero-output linear
    recursion); this reintroduces the missing free choice so that seed
    construction can inject kseed bits ONE PER PAIR, streamed in over time
    exactly the way BA.seed_state injects them for Rule 30, instead of
    baking all kseed bits into the t=0 vector simultaneously (see
    SECOND ATTEMPT note on rule90_seed below for why that mattered).
    """
    nxt, prev, par = BA.forced_step_90(u, v, phase)
    delta = drive ^ par
    return [x ^ delta for x in nxt[:-1]] + [nxt[-1]], prev, par


def rule90_seed_streamed(phase: int, kseed: int, m: int):
    """Left-depth-kseed Rule 90 seed, built by STREAMING the kseed bits of m
    in one-per-pair as drives -- the direct Rule-90 analogue of
    BA.seed_state, using drive_step_90 in place of P._wf_step.

    THIRD ATTEMPT, the one actually used below (see SECOND ATTEMPT dead end
    documented on rule90_seed): the first two attempts baked all kseed seed
    bits into the t=0 (u, v) vectors simultaneously, which gives every seed
    a full read-in of its own information for free, with no "forgetting"
    possible even in principle -- realized-future-window counts then
    saturate at the population size for ANY rule, linear or not, so they
    cannot distinguish "genuinely hard" from "trivially over-seeded". A
    bounded transducer plateaus specifically because it forgets all but a
    bounded suffix of a STREAMED input; the population must therefore be
    built the same way BA.seed_state builds it for Rule 30, one drive bit
    injected per pair over kseed pairs, not as a single upfront vector.
    """
    u, v = [BA.c_of(phase, 0)], []  # quiescent T=0-equivalent: an empty band
    for i in range(kseed):
        for drive in (1 - ((m >> i) & 1), 1):
            u, v, _ = drive_step_90(u, v, phase, drive)
    return u, v


def rule90_seed_v4(phase: int, kseed: int, m: int):
    """FOURTH ATTEMPT, the one actually used in RESULTS.md.

    rule90_seed_streamed (THIRD ATTEMPT) was ALSO an artifact, caught the
    same way as the first two: post-seeding `u` was confirmed (by direct
    inspection across seeds) to be byte-identical for every m, so pin=
    parity(f^s(u_0)) was forced to be seed-independent by the handoff
    state itself, not because Rule 90 is genuinely compressible. Root cause,
    traced by hand: seed_state's own seeding convention injects a free
    drive on the FIRST substep of each pair and a FORCED drive=1 on the
    SECOND (that forced substep is what encodes Rule 30's PIN SURVIVAL
    constraint -- Rule 90 has no such constraint, no death condition at
    all). Under forced_step_90's u/v decoupling, that forced substep resets
    the "A" (u) track to a seed-independent fixed point after every pair,
    regardless of what the free substep put there. So exactly one of
    (u_0, v_0) is ever live at the point full_sequence takes over, and which
    one is live depends only on the parity of "did seeding end with a
    forced substep" -- never both.

    Fix: Rule 90 has no pin/survival mechanism to justify a forced second
    substep at all, so don't inject one. Feed one free drive bit per
    SUBSTEP, consecutively, kseed substeps total (not kseed pairs). Checked
    directly (see dev notes) that this makes BOTH the handed-off u_0 and
    v_0 vary with m.
    """
    u, v = [BA.c_of(phase, 0)], []
    for i in range(kseed):
        u, v, _ = drive_step_90(u, v, phase, (m >> i) & 1)
    return u, v


def rule90_seed(kseed: int, m: int):
    """Synthetic left-depth-kseed seed for the Rule 90 control population.

    band_automaton.py has no Rule-90 analogue of seed_state: seed_state
    drives the real Rule-30 probe (P._wf_step, from alt_trace_fiber_probe),
    which has no Rule-90 counterpart imported anywhere in this codebase.
    forced_step_90 itself takes no free "drive" parameter at all -- it is
    the fully autonomous linear recursion -- so there is no way to inject
    free seed bits through it the way seed_state injects them through
    _wf_step.

    FIRST ATTEMPT (found broken, kept here as a documented dead end): setting
    v := bits(m), u := all-zero. forced_step_90 passes its `u` argument
    through UNCHANGED as the returned `prev` (`return nxt, u, acc`), and
    `nxt` is a pure function of `v` alone. Tracing the recursion under the
    rho/pin alternation (`u, v = nxt, prev` after every call) shows the
    "A" sequence (the running `u`) splits into two INDEPENDENT interleaved
    tracks that never mix: even-indexed terms are `f^s(A_0)` (a pure
    function of the ORIGINAL u), odd-indexed are `f^s(B_0)` (a pure function
    of the ORIGINAL v) -- `f` being one forced_step_90 call. Since pin_bits
    read the even track and rho_bits read the odd track, setting the
    original u to an all-zero CONSTANT (same for every seed) made every
    seed's pin-bit stream identical regardless of v/seed content: an
    artifact of this specific initial condition, not a fact about Rule 90.
    Empirically this gave index_lower_bound == 1 at every kseed and every
    s, which is why it was caught before being reported as a result:
    `uv run python mn_index.py --kind 90 --kseed 8` with that seed gave
    n_prefixes growing (seed content DOES reach the rho track) while index
    stayed pinned at 1 (seed content NEVER reaches the pin track) -- a
    dead giveaway that the pin track was structurally decoupled from the
    seed, not that Rule 90 is trivially compressible.

    FIX USED: split the kseed bits of m between the two initial vectors so
    BOTH the even track (u = A_0) and the odd track (v = B_0) receive
    genuine, independently-varying seed content: v gets the low
    `kseed // 2` bits of m, u gets the remaining `kseed - kseed // 2` bits.
    This still enumerates all 2^kseed distinct (u, v) pairs exhaustively
    (the two halves of m are disjoint bit ranges), and confirmed by direct
    inspection (see dev notes) that rho_bits now depend only on the v-half
    of m and pin_bits only on the u-half, both genuinely varying.
    """
    half = kseed // 2
    v = [(m >> i) & 1 for i in range(half)]
    u = [(m >> (half + i)) & 1 for i in range(kseed - half)]
    return u, v


def mn_index_sweep(kind: str, phase: int, kseed: int, pairs: int, W: int):
    """kind in {'30', '90'}. Returns {s: dict(index, n_seeds, n_prefixes,
    n_anomalous_prefixes)} for s in range(pairs)."""
    step_fn = BA.forced_step if kind == "30" else BA.forced_step_90
    total = pairs + W
    n = 1 << kseed
    prefixes = []
    pin_hist = []
    for m in range(n):
        if kind == "30":
            u, v = BA.seed_state(phase, kseed, m)
        else:
            u, v = rule90_seed_v4(phase, kseed, m)
        rho_bits, pin_bits = full_sequence(u, v, phase, total, step_fn)
        prefixes.append(rho_bits)
        pin_hist.append(pin_bits)

    results = {}
    for s in range(pairs):
        fut_by_pre: dict = {}
        windows = set()
        for m in range(n):
            pre = tuple(prefixes[m][: s + 1])
            fut = tuple(pin_hist[m][s : s + W])
            windows.add(fut)
            fut_by_pre.setdefault(pre, set()).add(fut)
        n_anom = sum(1 for fs in fut_by_pre.values() if len(fs) > 1)
        results[s] = dict(
            index=len(windows),
            n_seeds=n,
            n_prefixes=len(fut_by_pre),
            n_anomalous_prefixes=n_anom,
        )
    return results


def run_one(kind: str, kseed: int, pairs: int, W: int, verbose=True):
    t0 = time.time()
    out = {}
    for phase in (0, 1):
        out[phase] = mn_index_sweep(kind, phase, kseed, pairs, W)
    dt = time.time() - t0
    if verbose:
        print(f"kind=rule{kind} kseed={kseed} pairs={pairs} W={W} "
              f"time={dt:.1f}s")
    return out, dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["30", "90"], default="30")
    ap.add_argument("--kseed", type=int, required=True)
    ap.add_argument("--pairs", type=int, default=20)
    ap.add_argument("--W", type=int, default=30)
    ap.add_argument("--time-only", action="store_true",
                     help="just report wall-clock, print index at s=pairs-1")
    a = ap.parse_args()
    out, dt = run_one(a.kind, a.kseed, a.pairs, a.W)
    for phase in (0, 1):
        row = out[phase]
        s_last = a.pairs - 1
        r = row[s_last]
        print(f"  phase {'01' if phase == 0 else '10'}: "
              f"index({s_last})={r['index']} / {r['n_seeds']} seeds, "
              f"n_prefixes={r['n_prefixes']}, anomalies={r['n_anomalous_prefixes']}")
        if not a.time_only:
            for s in range(a.pairs):
                rr = row[s]
                print(f"    s={s:3d}  index={rr['index']:6d}  "
                      f"n_prefixes={rr['n_prefixes']:6d}  "
                      f"anomalies={rr['n_anomalous_prefixes']:4d}")


if __name__ == "__main__":
    main()
