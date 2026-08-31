"""Rule 30 fiber over the alternating trace (01)^inf / (10)^inf.

Target (Jarkko Kari's suggested extension of the zero-tail note): exclude
nonconstant periodic central traces for finite configurations, starting with
period two.

Structure exploited (proved in RESULTS-alt-trace-fiber.md):
  * For any trace c and right half R there is exactly one compatible
    configuration (left-permutive reconstruction; Lemma 1 of the zero-tail
    note).
  * The forced left half-plane is a function of c and of column 1 restricted
    to the zero set {t : c_t = 0} of the trace.  For the alternating trace the
    zero set is one parity class; write rho_k for column 1 at those times.

Main measurement: BFS over free rho-prefixes under the constraint
"L_j = 0 for all j > d" (left support depth <= d).  Death of the tree at a
finite level is a machine-checkable certificate that NO configuration with
left support depth <= d has the alternating central trace, regardless of its
right half.  For d <= 12 the certificate is re-verified by unpruned exhaustive
enumeration.

Controls (run first, assert):
  C1 zero-trace fiber matches the prefix-OR classification (Theorem 2, note)
  C2 all-one-trace fiber matches the checkerboard (RESULTS-eventual-period.md)
  C3 alternating stencil L1..L4 matches the recorded stencil
  C4 forward brute-force p=2 horizons w=1..6 match the SMT table 6,6,6,6,8,9
  C5 rho-reduction crosschecked against direct fiber reconstruction, both
     phases, random right halves

Kill condition (fires on a plausible negative): a rho-prefix tree that
survives past the level cap, or a finite right half whose forced left half is
eventually zero; either would be a candidate configuration with eventually
periodic center column and would be verified forward before being believed.

Parity closed form (proved in RESULTS-alt-trace-fiber.md): the frontier
sweep telescopes, L_{T+1} = v XOR parity(A | shift(B)); past the knee T = d
the surviving rho bit is forced and each pinned step is a pure parity check,
so the survivor BFS is a set of non-branching orbits of a parameter-free
map.  --parity verifies this against the BFS transition-by-transition;
--orbit measures forced-orbit survival from exhaustive seeds.

Usage:
  uv run python alt_trace_fiber_probe.py                # controls + defaults
  uv run python alt_trace_fiber_probe.py --certify 24   # certificates to d=24
  uv run python alt_trace_fiber_probe.py --enumerate 12 288
  uv run python alt_trace_fiber_probe.py --wallpaper
  uv run python alt_trace_fiber_probe.py --automaton 24 --dump out.json
  uv run python alt_trace_fiber_probe.py --parity 32
  uv run python alt_trace_fiber_probe.py --orbit 16
"""

import argparse
import random

# ---------------------------------------------------------------- fiber core


def fiber_left_half(W, D, trace_bit, rule30=True):
    """Bit-parallel forced left half over all 2^W finite right halves.

    Returns (L, r, c): L[j] for 1<=j<=D is an int whose bit i is the forced
    cell x_{-j}(0) for right half R_1..R_W = bits of i; r[t] is column 1.
    """
    N = 1 << W
    FULL = (1 << N) - 1

    def cmask(t):
        return FULL if trace_bit(t) else 0

    M = D + 3
    row = [0] * (M + 1)
    row[0] = cmask(0)
    for j in range(1, W + 1):
        m = 0
        for i in range(N):
            if (i >> (j - 1)) & 1:
                m |= 1 << i
        row[j] = m
    r = []
    c = [cmask(t) for t in range(D + 2)]
    for t in range(D + 1):
        r.append(row[1])
        new = [0] * (M + 1)
        new[0] = cmask(t + 1)
        for j in range(1, M):
            if rule30:
                new[j] = row[j - 1] ^ (row[j] | row[j + 1])
            else:  # rule 90 control
                new[j] = row[j - 1] ^ row[j + 1]
        row = new
    L = [None] * (D + 1)
    colprev = c[: D + 2]
    if rule30:
        colcur = [c[t + 1] ^ (c[t] | r[t]) for t in range(D + 1)]
    else:
        colcur = [c[t + 1] ^ r[t] for t in range(D + 1)]
    L[1] = colcur[0]
    for k in range(1, D):
        if rule30:
            nxt = [colcur[t + 1] ^ (colcur[t] | colprev[t])
                   for t in range(len(colcur) - 1)]
        else:
            nxt = [colcur[t + 1] ^ colprev[t]
                   for t in range(len(colcur) - 1)]
        colprev, colcur = colcur, nxt
        L[k + 1] = colcur[0]
    return L, r, c


def left_from_rho(rho, phase):
    """Forced left cells at time 0 from the zero-set column-1 values alone.

    phase 0: trace 0101... (zero set = even t, rho_k = r_{2k})
    phase 1: trace 1010... (zero set = odd t,  rho_k = r_{2k+1})
    Returns L with L[j] = x_{-j}(0), computable depth ~2*len(rho).
    """
    K = len(rho)
    Tmax = 2 * K - 1 + phase
    c = [(t + phase) % 2 for t in range(Tmax + 3)]
    l = []
    for t in range(Tmax + 1):
        if t % 2 == 1 - phase:
            l.append(1)  # pinned parity: c_t = 1 there, l_t = NOT c_{t+1} = 1
        else:
            l.append(1 - rho[t // 2])
    L = [None, l[0]]
    colprev, colcur = c[: Tmax + 2], l
    while len(colcur) >= 2:
        nxt = [colcur[t + 1] ^ (colcur[t] | colprev[t])
               for t in range(len(colcur) - 1)]
        colprev, colcur = colcur, nxt
        L.append(colcur[0])
    return L


def violates(rho, d, phase):
    L = left_from_rho(rho, phase)
    return any(L[j] for j in range(d + 1, len(L)))


# ---------------------------------------------------------------- controls


def bits_of(mask, i):
    return (mask >> i) & 1


def run_controls():
    W, D = 8, 40
    N = 1 << W
    # C1 zero fiber == prefix-OR classification
    L, _, _ = fiber_left_half(W, D, lambda t: 0)
    for i in range(N):
        R = [(i >> (j - 1)) & 1 if 1 <= j <= W else 0 for j in range(D + 2)]
        pref = 0
        for j in range(1, D + 1):
            prev = pref
            pref |= R[j]
            expect = pref if j % 2 == 1 else R[j] & (1 - prev)
            assert bits_of(L[j], i) == expect, (i, j)
    # C2 one fiber == checkerboard
    L, _, _ = fiber_left_half(W, D, lambda t: 1)
    for j in range(1, D + 1):
        assert L[j] == (((1 << N) - 1) if j % 2 == 0 else 0), j
    # C3 alternating stencil
    L, _, _ = fiber_left_half(W, 12, lambda t: t % 2)
    for i in range(N):
        R1, R2, R3 = i & 1, (i >> 1) & 1, (i >> 2) & 1
        assert bits_of(L[1], i) == 1 ^ R1
        assert bits_of(L[2], i) == R1
        assert bits_of(L[3], i) == (R1 | R2 | R3)
        assert bits_of(L[4], i) == 0
    # C4 forward p=2 horizons w=1..6 vs SMT table
    expect = {1: 6, 2: 6, 3: 6, 4: 6, 5: 8, 6: 9}
    T = 40
    for w in range(1, 7):
        best = -1
        off = w + T + 2
        for cfg in range(1, 1 << (2 * w + 1)):
            row = cfg << (off - w)
            center = []
            for t in range(T + 1):
                center.append((row >> off) & 1)
                row = (row << 1) ^ (row | (row >> 1))
                row &= (1 << (2 * off + 1)) - 1
            if center[0] == center[1]:
                continue
            h = 1
            while h + 1 <= T and center[h + 1] == center[h - 1]:
                h += 1
            best = max(best, h)
        assert best == expect[w], (w, best)
    # C5 rho reduction vs direct fiber, both phases
    random.seed(11)
    for phase in (0, 1):
        for _ in range(48):
            Rbits = [random.randint(0, 1) for _ in range(9)]
            L, rr = direct_left(Rbits, 80, phase)
            rho = [rr[2 * k + phase] for k in range(30)]
            L2 = left_from_rho(rho, phase)
            depth = min(len(L2), 56)
            assert all(L[j] == L2[j] for j in range(1, depth)), (phase, Rbits)
    print("controls C1-C5: PASS")


def direct_left(Rbits, D, phase):
    """Plain forced left half for one finite right half; returns (L, r)."""
    M = D + 3
    row = [0] * (M + 1)
    row[0] = phase % 2
    for j, b in enumerate(Rbits, start=1):
        row[j] = b
    c = [(t + phase) % 2 for t in range(D + 2)]
    r = []
    for t in range(D + 1):
        r.append(row[1])
        new = [0] * (M + 1)
        new[0] = c[t + 1]
        for j in range(1, M):
            new[j] = row[j - 1] ^ (row[j] | row[j + 1])
        row = new
    L = [None] * (D + 1)
    colprev = c[: D + 2]
    colcur = [c[t + 1] ^ (c[t] | r[t]) for t in range(D + 1)]
    L[1] = colcur[0]
    for k in range(1, D):
        nxt = [colcur[t + 1] ^ (colcur[t] | colprev[t])
               for t in range(len(colcur) - 1)]
        colprev, colcur = colcur, nxt
        L[k + 1] = colcur[0]
    return L, r


# ------------------------------------------------------------- measurements


def certify(dmax, exhaustive_to=12, maxlevel=200):
    """Certificates: for each d, level at which every rho-prefix violates."""
    for phase in (0, 1):
        print(f"phase {'01' if phase == 0 else '10'}:")
        for d in range(0, dmax + 1):
            if d <= exhaustive_to:
                k = None
                for kk in range(1, 17):
                    if all(violates([(m >> i) & 1 for i in range(kk)], d, phase)
                           for m in range(1 << kk)):
                        k = kk
                        break
                tag = "exhaustive"
            else:
                frontier = [()]
                k = None
                for lvl in range(maxlevel):
                    frontier = [p + (b,) for p in frontier for b in (0, 1)
                                if not violates(list(p + (b,)), d, phase)]
                    if not frontier:
                        k = lvl + 1
                        break
                tag = "bfs"
            status = f"certified at level {k} ({tag})" if k else "NO CERTIFICATE (kill condition fires)"
            print(f"  d={d:2d}: {status}")


def _wf_step(phase, T, A, B, v):
    """Advance the reconstruction frontier by one time step.

    A is the anti-diagonal t + j = T (bit j-1 = x(T-j, -j)), B the
    anti-diagonal t + j = T - 1.  Consuming l_T = v computes the new
    anti-diagonal C (t + j = T + 1) shallow-to-deep via
        x(t, -(j+1)) = x(t+1, -j) XOR (x(t, -j) OR x(t, -(j-1))),
    whose deepest entry C bit T is x(0, -(T+1)) = L_{T+1}, the one new
    forced output.  (phase, T, A, B) determines all future forced outputs.
    Returns (T+1, C, A).
    """
    C = v & 1
    prev = C
    for j in range(1, T + 1):
        if j == 1:
            right2 = (T - 1 + phase) & 1          # x(T-1, 0) = c_{T-1}
        else:
            right2 = (B >> (j - 2)) & 1           # x(T-j, -(j-1))
        cur = (A >> (j - 1)) & 1                  # x(T-j, -j)
        prev = prev ^ (cur | right2)              # x(T-j, -(j+1))
        C |= prev << j
    return T + 1, C, A


def _wf_start(phase):
    """Initial frontier; phase 10 consumes its leading pinned l_0 = 1."""
    st = (0, 0, 0)
    if phase == 1:
        st = _wf_step(phase, *st, 1)
    return st


def _wf_advance(phase, st, rho_bit, d, cone):
    """Feed both column -1 values for one rho bit (NOT rho, then the pin).

    Returns (new_state, violated).  violated: some forced value contradicts
    left depth <= d.  cone=False checks only the time-0 outputs L_j, j > d
    (the certificate semantics of certify()); cone=True also rejects any
    forced x(t, -j) = 1 with j > d + t, sound for the same claim since a
    left depth <= d configuration is zero strictly left of its light cone.
    """
    T, A, B = st
    bad = False
    for v in (1 - rho_bit, 1):
        T, A, B = _wf_step(phase, T, A, B, v)
        if cone:
            jmin = (d + T) // 2 + 1               # j > d + (T - j)
            if A >> (jmin - 1):
                bad = True
        elif T > d and (A >> (T - 1)) & 1:
            bad = True
    return (T, A, B), bad


def _wf_controls():
    """C6 incremental frontier == left_from_rho; C7 BFS == violates() BFS."""
    random.seed(7)
    for phase in (0, 1):
        for _ in range(64):
            rho = [random.randint(0, 1) for _ in range(30)]
            Lref = left_from_rho(rho, phase)
            st = _wf_start(phase)
            outs = [None] * (len(Lref) + 1)
            if phase == 1:
                outs[1] = st[1] & 1               # L_1 from the leading pin
            for b in rho:
                for v in (1 - b, 1):
                    st = _wf_step(phase, *st, v)
                    T, A = st[0], st[1]
                    if T < len(outs):
                        outs[T] = (A >> (T - 1)) & 1
            assert all(outs[j] == Lref[j] for j in range(1, len(Lref))), phase
    for phase in (0, 1):
        for d in (6, 10):
            ref = [()]
            inc = [((), _wf_start(phase), False)]
            for lvl in range(60):
                ref = [p + (b,) for p in ref for b in (0, 1)
                       if not violates(list(p + (b,)), d, phase)]
                nxt = []
                for p, st, _ in inc:
                    for b in (0, 1):
                        st2, bad = _wf_advance(phase, st, b, d, cone=False)
                        if not bad:
                            nxt.append((p + (b,), st2, False))
                inc = nxt
                assert sorted(p for p, _, _ in inc) == sorted(ref), (phase, d, lvl)
                if not ref:
                    break
    print("controls C6-C7: PASS")


def _bits_str(x, T, d):
    s = "".join(str((x >> (j - 1)) & 1) for j in range(1, T + 1))
    return s[:d] + "|" + s[d:] if T > d else s


def automaton(d, cone=False, maxlevel=200, dump=None, show=32):
    """A1 instrumentation: survivor wavefront states per level.

    BFS over rho bits with survivors merged by exact frontier state.  Emits
    per level the distinct states, and scans shallow-window quotients for a
    collision-free transition function (a candidate closed transition set).
    """
    _wf_controls()
    record = {}
    for phase in (0, 1):
        print(f"phase {'01' if phase == 0 else '10'} d={d} "
              f"prune={'cone' if cone else 'outputs'}:")
        states = {_wf_start(phase): 1}
        levels, trans = [], []
        for lvl in range(1, maxlevel + 1):
            nxt = {}
            for st, mult in states.items():
                for b in (0, 1):
                    st2, bad = _wf_advance(phase, st, b, d, cone)
                    trans.append((st, b, None if bad else st2))
                    if not bad:
                        nxt[st2] = nxt.get(st2, 0) + mult
            states = nxt
            n = sum(states.values())
            tailsA = {A >> d for _, A, _ in states}
            tailsB = {B >> d for _, _, B in states}
            levels.append({"k": lvl, "prefixes": n, "states": len(states),
                           "tails_beyond_d": len(tailsA),
                           "list": [{"mult": m, "T": st[0], "A": st[1],
                                     "B": st[2]}
                                    for st, m in sorted(states.items())]})
            line = (f"  k={lvl:3d}: prefixes {n:6d}  states {len(states):3d}  "
                    f"distinct A>>d {len(tailsA)}  B>>d {len(tailsB)}")
            if states:
                T0 = next(iter(states))[0]
                if len(tailsA) == 1 and T0 > d:
                    line += f"  forced tail A {_bits_str(tailsA.pop() << d, T0, d)[d + 1:]}"
            print(line)
            if states and len(states) <= show:
                for st, m in sorted(states.items(), key=lambda x: -x[1]):
                    print(f"      x{m:<5d} A {_bits_str(st[1], st[0], d)}  "
                          f"B {_bits_str(st[2], st[0] - 1, d)}")
            if not states:
                print(f"  certified at level {lvl}")
                break
        else:
            print("  NO CERTIFICATE within maxlevel (kill condition fires)")
        for w in (4, 6, 8, 10, 12, 16):
            seen, coll = {}, 0
            mask = (1 << w) - 1
            for st, b, st2 in trans:
                key = (st[1] & mask, st[2] & mask, b)
                val = (None if st2 is None
                       else (st2[1] & mask, st2[2] & mask))
                if key in seen and seen[key] != val:
                    coll += 1
                seen[key] = val
            print(f"  window w={w:2d}: quotient states {len(seen)}, "
                  f"transition collisions {coll}")
        record[phase] = levels
    if dump:
        import json
        import os
        os.makedirs(os.path.dirname(dump), exist_ok=True)
        with open(dump, "w") as f:
            json.dump({"d": d, "cone": cone, "phases": record}, f)
        print(f"dumped {dump}")


def _or_parity(phase, T, A, B):
    """Parity of the OR-word o_j = A_j | B_{j-1}, j = 1..T, B_0 = c_{T-1}.

    The sweep C[j+1] = C[j] XOR o_j never absorbs, so the new forced output
    is L_{T+1} = v XOR parity(o) for fed column -1 value v.
    """
    o = A | ((B << 1) | ((T - 1 + phase) & 1))
    o &= (1 << T) - 1
    return bin(o).count("1") & 1


def parity_structure(d, maxlevel=200):
    """Verify the parity closed form against the BFS, both phases.

    Post-knee claims: (i) branching factor exactly 1 at the rho substep,
    with the viable bit rho = 1 XOR parity(o); (ii) the pinned substep
    survives iff parity(o) = 1 at that substep.
    """
    for phase in (0, 1):
        states = {_wf_start(phase)}
        checked = 0
        for lvl in range(1, maxlevel + 1):
            nxt = set()
            for st in states:
                T, A, B = st
                post_rho = T + 1 > d    # rho-substep output depth T+1
                post_pin = T + 2 > d    # pin-substep output depth T+2
                alive = []
                for b in (0, 1):
                    st2, bad = _wf_advance(phase, st, b, d, cone=False)
                    rho_out = (1 - b) ^ _or_parity(phase, T, A, B)
                    Tm, Am, Bm = _wf_step(phase, T, A, B, 1 - b)
                    pin_out = 1 ^ _or_parity(phase, Tm, Am, Bm)
                    exp_bad = (post_rho and rho_out == 1) or \
                              (post_pin and pin_out == 1)
                    assert bad == exp_bad, (phase, lvl, st, b)
                    if not bad:
                        alive.append((b, st2))
                if post_rho:
                    want = 1 ^ _or_parity(phase, T, A, B)
                    assert all(b == want for b, _ in alive), (phase, lvl, st)
                    assert len(alive) <= 1, (phase, lvl, st)
                    checked += 1
                nxt.update(s for _, s in alive)
            states = nxt
            if not states:
                print(f"phase {'01' if phase == 0 else '10'} d={d}: parity "
                      f"closed form verified on every transition "
                      f"({checked} post-knee states), certified level {lvl}")
                break
        else:
            print("NO CERTIFICATE within maxlevel (kill condition fires)")


def forced_orbit(kseed, maxsteps=4000, sample=None, top=8):
    """Iterate the forced continuation from every rho-seed of length kseed.

    Post-seed the dynamics is parameter-free: rho substep feeds the single
    viable value v = parity(o); pin substep feeds 1 and survives iff
    parity(o) = 1.  Survival steps until the first pin failure measure how
    long a left depth <= 2*kseed candidate can persist; uniformity in d is
    exactly 'this is finite for every finite seed'.
    """
    for phase in (0, 1):
        seeds = range(1 << kseed) if sample is None else sample
        best = []
        for m in seeds:
            st = _wf_start(phase)
            for i in range(kseed):
                for v in (1 - ((m >> i) & 1), 1):
                    st = _wf_step(phase, *st, v)
            T, A, B = st
            steps = None
            for s in range(maxsteps):
                # rho substep: feed the unique zero-output value
                v = _or_parity(phase, T, A, B)
                T, A, B = _wf_step(phase, T, A, B, v)
                # pin substep: forced v = 1, output = 1 XOR parity(o)
                if _or_parity(phase, T, A, B) != 1:
                    steps = s
                    break
                T, A, B = _wf_step(phase, T, A, B, 1)
            if steps is None:
                print(f"  SEED {m:0{kseed}b} phase {phase} SURVIVES "
                      f"{maxsteps} steps: KILL CONDITION, candidate "
                      f"left-finite counterexample")
                steps = maxsteps
            best.append((steps, m))
        best.sort(reverse=True)
        n = len(best)
        mean = sum(s for s, _ in best) / n
        print(f"phase {'01' if phase == 0 else '10'} kseed={kseed}: "
              f"{n} seeds, survival mean {mean:.2f} max {best[0][0]}  "
              f"top: {[(s, format(m, f'0{kseed}b')) for s, m in best[:top]]}")


def enumerate_fiber(W, D, tailwin=120):
    """Finite right halves: candidates for finite members, forced-one gaps."""
    for phase in (0, 1):
        L, _, _ = fiber_left_half(W, D, lambda t: (t + phase) % 2)
        N = 1 << W
        candidates, maxgap, minlast = [], 0, None
        for i in range(N):
            bits = [bits_of(L[j], i) for j in range(1, D + 1)]
            ones = [j + 1 for j, b in enumerate(bits) if b]
            if not ones or ones[-1] < D - tailwin:
                candidates.append(i)
                continue
            prev, g = 0, 0
            for p in ones:
                g = max(g, p - prev - 1)
                prev = p
            maxgap = max(maxgap, g)
            minlast = ones[-1] if minlast is None else min(minlast, ones[-1])
        print(f"phase {'01' if phase == 0 else '10'} W={W} D={D}: "
              f"finite candidates {len(candidates)}, max forced-zero gap {maxgap}, "
              f"shallowest deepest-one {minlast}")
        assert not candidates, f"kill condition: candidates {candidates[:4]}"


def wallpaper_checks(T=20000):
    """The left-periodic member: right half {1,4}, phase 01."""
    # forced left half is 7-periodic word 1001100 from depth 1 (checked deep)
    L, _ = direct_left([1, 0, 0, 1], 1024, 0)
    word = [0, 1, 1, 0, 0, 1, 0]  # L_1..L_7; rotation class of 1001100
    ok = all(L[j] == word[(j - 1) % 7] for j in range(1, 1025))
    print(f"wallpaper member {{1,4}}: left half 7-periodic (word 0110010 "
          f"from depth 1) to depth 1024: {ok}")
    assert ok
    # rho lock: column 1 at even times alternates, driven simulation
    M = T + 8
    row = (1 << 1) | (1 << 4)
    mask = (1 << M) - 1
    first_break = None
    for t in range(T):
        if t % 2 == 0:
            expect = 1 if (t // 2) % 2 == 0 else 0
            if ((row >> 1) & 1) != expect and first_break is None:
                first_break = t
        row = ((row << 1) ^ (row | (row >> 1))) & mask
        row &= ~1
        row |= (t + 1) % 2
    print(f"wallpaper member rho lock (col 1 even times alternating): "
          f"first break {first_break} (checked to t={T})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certify", type=int, default=None, metavar="DMAX")
    ap.add_argument("--enumerate", type=int, nargs=2, default=None,
                    metavar=("W", "D"))
    ap.add_argument("--wallpaper", action="store_true")
    ap.add_argument("--automaton", type=int, default=None, metavar="D")
    ap.add_argument("--cone", action="store_true")
    ap.add_argument("--dump", type=str, default=None)
    ap.add_argument("--parity", type=int, default=None, metavar="D")
    ap.add_argument("--orbit", type=int, default=None, metavar="KSEED")
    ap.add_argument("--orbit-steps", type=int, default=4000)
    ap.add_argument("--skip-controls", action="store_true")
    args = ap.parse_args()
    if not args.skip_controls:
        run_controls()
    ran = False
    if args.certify is not None:
        certify(args.certify)
        ran = True
    if args.enumerate is not None:
        enumerate_fiber(*args.enumerate)
        ran = True
    if args.wallpaper:
        wallpaper_checks()
        ran = True
    if args.automaton is not None:
        automaton(args.automaton, cone=args.cone, dump=args.dump)
        ran = True
    if args.parity is not None:
        _wf_controls()
        parity_structure(args.parity)
        ran = True
    if args.orbit is not None:
        _wf_controls()
        forced_orbit(args.orbit, maxsteps=args.orbit_steps)
        ran = True
    if not ran:
        certify(16)
        enumerate_fiber(10, 192)
        wallpaper_checks()


if __name__ == "__main__":
    main()
