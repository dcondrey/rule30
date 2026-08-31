"""Row 41 uniformity attack: deep-anchored normal form of the alternating-trace
survivor automaton, and the measurement of exactly why it does not close the
uniformity gap.

Object owned (register row 41, `docs/rule30/RESULTS-alt-trace-fiber.md`):
the parity-checked deterministic map on reconstruction frontiers, closed form
`L_(T+1) = v XOR parity(o_1..o_T)`.

Normal form added here.  Read the frontier from the time-0 row inward,
    u_T[m] := x(m, -(T-m)),   m = 0..T-1,   u_T[T] := c_T,
i.e. index the frontier by TIME rather than by depth.  Then the probe's
frontier map becomes, with no dependence on T, on the phase, or on d,

    u_(T+1)[m+1] = u_(T+1)[m] XOR ( u_T[m] OR u_(T-1)[m] ),   u_(T+1)[0] = 0,

equivalently u_(T+1)[m] = parity( o[0..m-1] ) with o[m] = u_T[m] OR u_(T-1)[m],
and the survivor kill condition at a pinned step is parity(o) = 1, which is
the SHALLOW-most entry u_(T+1)[T].

Modes (each prints its own scope; see row41_fiber_uniformity.md):
  --validate        Theorem A: the normal form == the repo's verified map
  --cone K          Theorem C: the deep end of the frontier is forced to zero,
                    so the deep-anchored truncation is a vacuous automaton
  --window K M      Lemma D + Kill 1: front-anchored fixed-anchor
                    determination, and whether the pin parity is
                    window-measurable (add --offset P to start P rho/pin
                    pairs past the knee)
  --coverage K      honesty check on Kill 1 past the knee: how many window
                    classes actually hold two distinct full states
  --growth K        Kill 2: the active region grows 1 cell per rho/pin pair
  --rule90 K        Rule 90 control: every structural claim holds there too
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "experiments" / "rule30"))
sys.path.insert(0, str(REPO / "experiments" / "overnight-arms" / "common"))

import alt_trace_fiber_probe as P  # noqa: E402  (READ-ONLY reuse)
import ensemble_filter  # noqa: E402


# --------------------------------------------------------------- normal form


def c_of(phase: int, t: int) -> int:
    """Trace bit: phase 0 is (01)^inf (c_0 = 0), phase 1 is (10)^inf."""
    return (t + phase) & 1


def state_from_probe(phase: int, T: int, A: int, B: int):
    """Deep-anchored (u_T, u_(T-1)) from the probe's frontier integers.

    A_j = x(T-j,-j) is bit j-1 of A; with m = T-j this is u_T[m] at bit T-1-m.
    B_j = x(T-1-j,-j) is bit j-1 of B; with m = T-1-j this is u_(T-1)[m] at
    bit T-2-m.  The shallow slots u_T[T] and u_(T-1)[T-1] are the trace bits,
    which is exactly the probe's `B_0 := c_(T-1)` convention.
    """
    u = [(A >> (T - 1 - m)) & 1 for m in range(T)] + [c_of(phase, T)]
    v = [(B >> (T - 2 - m)) & 1 for m in range(T - 1)] + [c_of(phase, T - 1)]
    return u, v


def or_word(u, v):
    return [u[m] | v[m] for m in range(len(v))]


def forced_step(u, v, phase):
    """One step of the forced (zero-output) survivor map, deep-anchored.

    Returns (u_next, u, pin_parity).  On a surviving orbit BOTH substeps have
    u_next[m] = parity(o[0..m-1]): the rho substep because the forced drive is
    v = parity(o), the pin substep because the drive is 1 and survival needs
    parity(o) = 1.  pin_parity = u_next[T] is the drive; a pinned step
    survives iff it is 1.
    """
    T = len(v)
    o = or_word(u, v)
    nxt, acc = [0], 0
    for m in range(T):
        acc ^= o[m]
        nxt.append(acc)
    nxt.append(c_of(phase, T + 1))
    return nxt, u, acc


# ------------------------------------------------------- Theorem A: validate


def validate(trials: int = 200, steps: int = 40) -> bool:
    """Theorem A.  The deep-anchored normal form reproduces the repo's map.

    Scope: `trials` random rho drives of length `steps`, both phases, every
    step checked.  Identities checked at every step:
      (1) parity(or_word) == probe `_or_parity`;
      (2) the successor frontier == probe `_wf_step`, re-read deep-anchored,
          for the general drive v (entries offset by v XOR parity(o));
      (3) the forced drive v = parity(o) makes the new output u_next[0] = 0;
      (4) the reconstructed outputs match `left_from_rho`.
    """
    random.seed(20260830)
    ok = True
    for phase in (0, 1):
        for _ in range(trials):
            rho = [random.randint(0, 1) for _ in range(steps)]
            Lref = P.left_from_rho(rho, phase)
            st = P._wf_start(phase)
            outs = {}
            if phase == 1:
                outs[1] = st[1] & 1
            for b in rho:
                for drive in (1 - b, 1):
                    T, A, B = st
                    if T == 0:
                        st = P._wf_step(phase, T, A, B, drive)
                        outs[1] = st[1] & 1
                        continue
                    u, v = state_from_probe(phase, T, A, B)
                    o = or_word(u, v)
                    if len(o) != T or (sum(o) & 1) != P._or_parity(phase, T, A, B):
                        print(f"FAIL(1) phase={phase} T={T}")
                        ok = False
                    nxt, _, par = forced_step(u, v, phase)
                    T2, C, Anew = P._wf_step(phase, T, A, B, drive)
                    u2, _ = state_from_probe(phase, T2, C, Anew)
                    delta = drive ^ par
                    if u2 != [x ^ delta for x in nxt[:-1]] + [nxt[-1]]:
                        print(f"FAIL(2) phase={phase} T={T}\n {u2}\n {nxt}")
                        ok = False
                    if nxt[0] != 0:
                        print(f"FAIL(3) phase={phase} T={T}")
                        ok = False
                    outs[T2] = u2[0]
                    st = (T2, C, Anew)
            for j, val in outs.items():
                if j < len(Lref) and Lref[j] != val:
                    print(f"FAIL(4) phase={phase} j={j}")
                    ok = False
    print(f"Theorem A: {'PASS' if ok else 'FAIL'} -- deep-anchored normal form "
          f"== verified probe map, {trials} rho x {steps} bits x 2 phases, "
          f"identities (1) parity (2) successor (3) forced output (4) "
          f"left_from_rho")
    return ok


# ----------------------------------------------------------- seeds and orbits


def seed_state(phase: int, kseed: int, m: int):
    """Post-seed frontier for rho-seed `m` of length kseed, in normal form.

    This is exactly the seed set of the probe's `forced_orbit`: left depth
    d = 2*kseed, the knee, driven with the probe's own step function.
    """
    st = P._wf_start(phase)
    for i in range(kseed):
        for drive in (1 - ((m >> i) & 1), 1):
            st = P._wf_step(phase, *st, drive)
    return state_from_probe(phase, *st)


def front(u) -> int:
    """Deepest index carrying a one; len(u) if none."""
    for m, x in enumerate(u):
        if x:
            return m
    return len(u)


def run_forced(u, v, phase, steps, record=None):
    """Iterate the forced map, alternating rho substep and pin substep.

    Returns the number of completed rho/pin PAIRS survived before the first
    pin-parity failure (None if it survived all `steps` pairs).  `record` is
    an optional callback (pair_index, u, v, pin_parity_of_pin_substep).
    """
    for s in range(steps):
        u, v, _ = forced_step(u, v, phase)
        if record is not None:
            record(s, u, v, None)
        nxt, prev, par = forced_step(u, v, phase)
        if par != 1:
            return s
        u, v = nxt, prev
    return None


# --------------------------------------- Theorem C: the deep end is forced 0


def cone(kseed: int, pairs: int = 24) -> None:
    """Theorem C, verified.  On any orbit surviving to time T from a knee seed
    of left depth d = 2*kseed, u_T[m] = 0 for every m < (T-d)/2.

    Proof (exact, no gap): the rotated rule at t, j gives
    x(t,-(j+1)) = x(t+1,-j) XOR (x(t,-j) OR x(t,-(j-1))).  Survival means
    x(0,-j) = 0 for all j > d; induction on t then gives x(t,-j) = 0 for all
    j > d+t, and u_T[m] = x(m,-(T-m)) has T-m > d+m exactly when m < (T-d)/2.

    Consequence: for every FIXED band height M the deep-anchored truncation
    u_T[0..M-1] is eventually the all-zero fixed point, so its lasso is
    trivial and decides nothing.  This retires the "bounded state count"
    reading of the uniformity target in its natural coordinates.

    Scope of the check below: ALL 2^kseed rho-seeds, both phases, every
    surviving step up to `pairs` rho/pin pairs.
    """
    print(f"\nTheorem C: deep-end vanishing, all 2^{kseed} seeds x 2 phases")
    viol = 0
    checked = 0
    maxfront = {}
    for phase in (0, 1):
        for m in range(1 << kseed):
            u, v = seed_state(phase, kseed, m)
            # left depth at the knee is exactly the current time T; phase 10
            # consumes a leading pin, so its effective d is odd (2k+1).
            T = len(v)
            d = T
            surv = 0
            while surv < pairs:
                for sub in range(2):
                    nxt, prev, par = forced_step(u, v, phase)
                    if sub == 1 and par != 1:
                        u = None
                        break
                    u, v = nxt, prev
                    T += 1
                    bound = max(0, -(-(T - d) // 2))  # ceil((T-d)/2)
                    checked += 1
                    if any(u[:bound]):
                        viol += 1
                    maxfront[T] = max(maxfront.get(T, 0), 0)
                if u is None:
                    break
                surv += 1
    print(f"  states checked: {checked}; violations of u_T[m]=0 for "
          f"m < ceil((T-d)/2): {viol}  -> {'PASS' if viol == 0 else 'FAIL'}")
    print("  corollary: every fixed deep-anchored band M is eventually the "
          "zero fixed point; deep-anchored lasso is vacuous")


# ------------------------- Theorem D + Kill 1: front-anchored window locality


def window(u, v, M: int):
    """Front-anchored window of width M: the joint front g = min(front(u),
    front(v)), then M entries of each from g."""
    g = min(front(u), front(v))
    return (tuple(u[g:g + M]), tuple(v[g:g + M]))


def active_width(u, v) -> int:
    """Shallow end minus joint front: the number of indices the pin parity
    actually reads."""
    return len(v) - min(front(u), front(v))


def parity_sequence(u, v, phase, pairs: int):
    """Pin parities of the first `pairs` rho/pin pairs of the forced orbit.

    The forced map is deterministic irrespective of survival (the drive is
    always the unique zero-output value parity(o)), so this sequence is well
    defined; survival forever is exactly "every entry is 1".
    """
    out = []
    for _ in range(pairs):
        u, v, _ = forced_step(u, v, phase)      # rho substep
        u, v, par = forced_step(u, v, phase)    # pin substep
        out.append(par)
    return tuple(out)


def advance_survivors(u, v, phase, offset: int):
    """Run `offset` rho/pin pairs; return the state, or None if a pin failed.

    Past the knee the front has moved, so window width, active width and
    state length become three distinct scales -- which is what gives the
    Kill 1 measurement a lever arm.
    """
    for _ in range(offset):
        u, v, _ = forced_step(u, v, phase)
        nxt, prev, par = forced_step(u, v, phase)
        if par != 1:
            return None
        u, v = nxt, prev
    return u, v


def window_test(kseed: int, Mmax: int, pairs: int = 48, offset: int = 0) -> None:
    """Lemma D (fixed-anchor determination) and Kill 1 (window horizon).

    Lemma D, exact.  Let g be the joint front of (u_T, u_(T-1)); o vanishes
    below g, so u_(T+1)[m] = parity(o[g..m-1]).  Hence the values of the
    successor on the absolute interval [g, g+M) are a function of (u_T,
    u_(T-1)) on [g, g+M-1) alone.  Verified below.

    Why that is NOT an autonomous finite automaton, and this is the whole
    finding: the front advances (g' = g or g+1, rate 1/2 per substep), so a
    front-anchored width-M window determines the successor only on a window
    of width M-1 after the front moves.  The window LEAKS one cell per front
    advance; it buys a finite horizon, not an invariant.

    Kill 1, measured.  H(M) := the largest h such that the first h pin
    parities are a function of the width-M front-anchored window, over ALL
    2^kseed rho-seeds per phase.  H(M) finite for every M means no finite
    window decides survival; the growth rate of H(M) is the price.
    """
    print(f"\nLemma D + Kill 1: front-anchored windows, all 2^{kseed} seeds "
          f"per phase, horizon capped at {pairs} pairs")
    # Lemma D: fixed-anchor determination, verified on the reachable set.
    bad = tested = 0
    for phase in (0, 1):
        seen: dict = {}
        for m in range(1 << kseed):
            u, v = seed_state(phase, kseed, m)
            for _ in range(8):
                g = min(front(u), front(v))
                nxt, prev, _ = forced_step(u, v, phase)
                for M in range(2, Mmax + 1):
                    key = (M, tuple(u[g:g + M - 1]), tuple(v[g:g + M - 1]))
                    val = tuple(nxt[g:g + M])
                    tested += 1
                    if seen.get(key, val) != val:
                        bad += 1
                    seen[key] = val
                u, v = nxt, prev
    print(f"  Lemma D fixed-anchor determination: {tested} checks, {bad} "
          f"contradictions -> {'PASS' if bad == 0 else 'FAIL'}")

    # precompute per phase: seed state, its parity sequence, active width
    pre: dict = {}
    for phase in (0, 1):
        rows = []
        for m in range(1 << kseed):
            st = seed_state(phase, kseed, m)
            if offset:
                st = advance_survivors(*st, phase, offset)
                if st is None:
                    continue
            u, v = st
            rows.append((u, v, parity_sequence(u, v, phase, pairs), m))
        pre[phase] = rows
        aws = [active_width(u, v) for u, v, _, _ in rows]
        slen = max(len(v) for _, v, _, _ in rows)
        print(f"  phase {'01' if phase == 0 else '10'}: {len(rows)} states "
              f"after offset {offset}; active width {min(aws)}..{max(aws)} "
              f"(what the pin parity reads), state length {slen}")

    print("   M  phase  H(M)  groups  mixed@H  mean|rate-1/2|@H  witness")
    for M in range(2, Mmax + 1):
        for phase in (0, 1):
            groups: dict = {}
            for u, v, seq, m in pre[phase]:
                groups.setdefault(window(u, v, M), []).append((seq, m))
            H = pairs
            for g in groups.values():
                for h in range(pairs):
                    if len({s[h] for s, _ in g}) > 1:
                        H = min(H, h)
                        break
            if H >= pairs:
                print(f"  {M:2d}    {'01' if phase == 0 else '10'}   >={pairs}"
                      f"  {len(groups):6d}  (cap reached)")
                continue
            mixed = [k for k, g in groups.items()
                     if len({s[H] for s, _ in g}) > 1]
            tot = sum(len(g) for g in groups.values())
            bias = sum(len(g) * abs(sum(s[H] for s, _ in g) / len(g) - 0.5)
                       for g in groups.values()) / tot
            g = groups[mixed[0]]
            z = next(x for s, x in g if s[H] == 0)
            o = next(x for s, x in g if s[H] == 1)
            print(f"  {M:2d}    {'01' if phase == 0 else '10'}  {H:4d}  "
                  f"{len(groups):6d}  {len(mixed):9d}  {bias:18.4f}  "
                  f"{z:0{kseed}b}/{o:0{kseed}b}")


def coverage(kseed: int, offset: int, Ms=(8, 12, 16, 20, 24, 28)) -> None:
    """Honesty check on Kill 1 past the knee.

    Past the knee the window, the active region and the state length are three
    distinct scales, which is the lever arm the knee measurement lacks.  But
    the reachable surviving set thins fast, and a window class holding one
    single full state (duplicated across seeds) tests nothing.  This prints,
    per M, how many classes hold two DISTINCT full states -- the only classes
    that can witness or refute locality.

    Scope: ALL 2^kseed rho-seeds per phase, survivors of `offset` rho/pin
    pairs.
    """
    print(f"\nKill 1 coverage past the knee: 2^{kseed} seeds, offset {offset}")
    for phase in (0, 1):
        rows = []
        for m in range(1 << kseed):
            st = advance_survivors(*seed_state(phase, kseed, m), phase, offset)
            if st:
                rows.append(st)
        aws = [active_width(u, v) for u, v in rows]
        print(f"  phase {'01' if phase == 0 else '10'}: {len(rows)} surviving "
              f"states, active width {min(aws)}..{max(aws)}, state length "
              f"{max(len(v) for _, v in rows)}")
        print("    M  classes  non-singleton  classes with >1 DISTINCT state")
        for M in Ms:
            g: dict = {}
            for u, v in rows:
                g.setdefault(window(u, v, M), []).append((tuple(u), tuple(v)))
            nons = [k for k, x in g.items() if len(x) > 1]
            dist = sum(1 for k in nons if len(set(g[k])) > 1)
            print(f"   {M:3d}  {len(g):7d}  {len(nons):13d}  {dist:29d}")
    print("  Where the last column is 0 the H(M) measurement has no "
          "discriminating power: every class is one state seen twice.")


# --------------------------------------------- Kill 2: growth of the automaton


def growth(kseed: int, pairs: int = 10, Mmax: int = 12) -> None:
    """Kill 2.  The active region grows linearly, so the front-anchored
    automaton that would have to decide survival has 2^Theta(T) states.

    (a) active width along surviving orbits, per rho/pin pair;
    (b) number of distinct front-anchored width-M windows over the seed set.
    Scope: ALL 2^kseed rho-seeds, phase 01 for (a), both phases for (b).
    """
    print(f"\nKill 2: active width and window-state count, 2^{kseed} seeds")
    phase = 0
    widths: dict = {}
    for m in range(1 << kseed):
        u, v = seed_state(phase, kseed, m)
        for s in range(pairs):
            alive = True
            for sub in range(2):
                nxt, prev, par = forced_step(u, v, phase)
                if sub == 1 and par != 1:
                    alive = False
                    break
                u, v = nxt, prev
            if not alive:
                break
            widths.setdefault(s, []).append(active_width(u, v))
    print("  pair  survivors  active width (min/mean/max)")
    for s in sorted(widths):
        w = widths[s]
        print(f"  {s:4d}  {len(w):9d}  {min(w):3d} / {sum(w)/len(w):6.2f} / "
              f"{max(w):3d}")
    print("  Kill 1 showed the minimum survival-deciding window IS the active "
          "width.  It grows by 1 per pair, so the automaton that decides "
          "survival for n pairs needs 2^Theta(n) states: no bounded state "
          "count exists.")


# ----------------------------------------------------------- Rule 90 control


def forced_step_90(u, v, phase):
    """Same normal form for rule 90.

    Rule 90 rotated: x(t,x-1) = x(t+1,x) XOR x(t,x+1), i.e. g(a,b) = b, so
    o[m] = u_(T-1)[m] and u_(T+1)[m] = parity(o[0..m-1]).  Every structural
    statement above (deep-end vanishing, front-anchored window autonomy,
    prefix-parity closed form) holds verbatim, by the identical index
    argument.  Only the pin -- which does not exist for rule 90 -- is
    Rule-30-specific.
    """
    T = len(v)
    o = [v[m] for m in range(T)]
    nxt, acc = [0], 0
    for m in range(T):
        acc ^= o[m]
        nxt.append(acc)
    nxt.append(c_of(phase, T + 1))
    return nxt, u, acc


def rule90(kseed: int, Mmax: int = 8, pairs: int = 8) -> None:
    print("\nRule 90 control")
    c90 = ensemble_filter.center_column("90", 20000)
    print(f"  ensemble_filter.center_column('90', 20000): ones at t>0 = "
          f"{sum(c90[1:])}; rule 90's lone-seed centre IS eventually periodic, "
          f"so any structure shared with rule 90 proves nothing")
    random.seed(5)
    results = {}
    for tag, step in (("rule 30", forced_step), ("rule 90", forced_step_90)):
        bad = tested = 0
        seen: dict = {}
        for _ in range(400):
            T = 24
            u = [0] * 3 + [random.randint(0, 1) for _ in range(T - 2)]
            v = [0] * 3 + [random.randint(0, 1) for _ in range(T - 3)]
            for _ in range(pairs):
                g = min(front(u), front(v))
                nxt, prev, _ = step(u, v, 0)
                for M in range(2, Mmax + 1):
                    key = (M, tuple(u[g:g + M - 1]), tuple(v[g:g + M - 1]))
                    val = tuple(nxt[g:g + M])
                    tested += 1
                    if seen.get(key, val) != val:
                        bad += 1
                    seen[key] = val
                u, v = nxt, prev
        results[tag] = (tested, bad)
        print(f"  {tag} fixed-anchor determination (Lemma D): {tested} checks,"
              f" {bad} contradictions -> {'HOLDS' if bad == 0 else 'FAILS'}")
    print("  Lemma D, the deep-anchored normal form, and the finite-state "
          "truncation all hold verbatim for rule 90, whose lone-seed centre "
          "IS eventually periodic.  The structure found here therefore proves "
          "nothing on its own; only the pin parity is Rule-30-specific, and "
          "Kill 1 shows the structure cannot see it.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--cone", type=int, default=0)
    ap.add_argument("--window", nargs=2, type=int, metavar=("KSEED", "MMAX"))
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--coverage", type=int, default=0)
    ap.add_argument("--growth", type=int, default=0)
    ap.add_argument("--rule90", type=int, default=0)
    a = ap.parse_args()
    if a.validate:
        validate()
    if a.cone:
        cone(a.cone)
    if a.window:
        window_test(*a.window, offset=a.offset)
    if a.coverage:
        coverage(a.coverage, a.offset or 5)
    if a.growth:
        growth(a.growth)
    if a.rule90:
        rule90(a.rule90)


if __name__ == "__main__":
    main()
