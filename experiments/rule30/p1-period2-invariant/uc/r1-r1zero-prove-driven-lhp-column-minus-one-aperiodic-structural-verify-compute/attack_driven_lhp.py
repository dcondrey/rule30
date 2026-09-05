"""Adversarial compute checks on PROOF.md (lemma driven-lhp-column-minus-one-aperiodic).

Every section tries to produce a counterexample to a claim in PROOF.md, in a family the
screen (uc/r1-r1zero-screen-driven-lhp-column-minus-one-aperiodic) or the proof's own gates
(G1..G7) did not cover, or at a scale beyond them.  A section prints one or more lines
'ATTACK <name>: ... hits=<k>'; hits > 0 is a counterexample and is described in full.

Sections
  A0  the (ND) boundary: y zero on x <= -1 with c = 0^omega is identically zero, so the lemma's
      literal hypothesis 'nonzero finite y' (which in the lemma's own usage includes the seed
      delta_0, overridden at x = 0 by c_0) admits a degenerate counterexample; the proof's (ND)
      excludes exactly this.  Also confirms that every other 'finitely many ones' drive is fine.
  A1  (EDGE) at scale: T = 20000, y width up to 2000, random and periodic and constant drives,
      Rules 30 and 90.
  A2  Theorem 1 in families outside the screen: far-left seeds y = {-d}, long-period random
      primitive words (p up to 128), long true-trace prefixes c*[:N] with periodic tails,
      finitely-many-ones drives; T = 65536; a strong periodicity detector (KMP minimal period
      of the second half, any period up to T/8) in addition to the screen's q <= Q detector.
  A3  Theorem 2 beyond the screened columns: columns -1..-256 individually, T = 16384.
  A4  Theorem 2 in a family the screen cannot cover: arbitrary (non-periodic) drives constructed
      by DFS to make column -1 eventually periodic (targets 0^omega, (01)^omega, (0011)^omega,
      (011)^omega); then c itself and column -2 must both be aperiodic.
  A5  Exhaustive small-parameter search for the impossible configuration of Theorem 1: all y of
      width <= 8, all drives of period <= 6 (every rotation), T = 512; any l with a period
      q <= 64 from onset <= 256 is a hit.
  A6  Lemma 7 on random periodic drives; Proposition B exhaustive at T = 16.

usage: cd <p1-period2-invariant> && uv run python <this file> > attack_driven_lhp.log
"""
import sys, itertools, random, time, math
import numpy as np

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows, eventual_period, longest_shift_agreement

T_START = time.time()


def say(s):
    print(s, flush=True)


# ---------- kernels (mirrored ints, bit i = s(t,-i), bit 0 = c_t) ----------
def step30(row):
    return (row >> 1) ^ (row | (row << 1))


def step90(row):
    return (row >> 1) ^ (row << 1)


STEP = {'30': step30, '90': step90}


def lhp_rows(rule, y_int, c, T):
    """y_int bit i (i >= 1) = s(0,-i); bit 0 of y_int ignored.  c[t] for t <= T+1."""
    st = STEP[rule]
    row = (y_int & ~1) | c[0]
    rows = [row]
    for t in range(T):
        row = (st(row) & ~1) | c[t + 1]
        rows.append(row)
    return rows


def rhp_rows30(c, T):
    row = c[0]
    rows = [row]
    for t in range(T):
        nxt = (row << 1) ^ (row | (row >> 1))
        row = (nxt & ~1) | c[t + 1]
        rows.append(row)
    return rows


def column(rows, k):
    return [(r >> k) & 1 for r in rows]


def edge_violations(rows):
    """(EDGE): once the row is nonzero, its top bit index increases by exactly one per step."""
    t0 = None
    for t, row in enumerate(rows):
        if row:
            t0 = t
            top0 = row.bit_length() - 1
            break
    if t0 is None:
        return 0, None
    v = 0
    for t in range(t0, len(rows)):
        row = rows[t]
        if row == 0 or row.bit_length() - 1 != top0 + (t - t0):
            v += 1
    return v, t0


def longest_run_np(seq, Q):
    """max over shifts q <= Q of the longest run of i with seq[i] == seq[i+q]."""
    a = np.asarray(seq, dtype=np.int8)
    best = 0
    for q in range(1, Q + 1):
        eq = (a[:-q] == a[q:])
        if not eq.any():
            continue
        # longest run of True
        d = np.diff(np.concatenate(([0], eq.astype(np.int8), [0])))
        starts = np.flatnonzero(d == 1)
        ends = np.flatnonzero(d == -1)
        run = int((ends - starts).max())
        if run > best:
            best = run
    return best


# ---------- periodicity detectors ----------
def kmp_min_period(seq):
    n = len(seq)
    fail = [0] * n
    k = 0
    for i in range(1, n):
        while k and seq[i] != seq[k]:
            k = fail[k - 1]
        if seq[i] == seq[k]:
            k += 1
        fail[i] = k
    return n - fail[n - 1] if n else 0


def strong_period(seq, onset_frac=0.5, min_reps=8):
    """Minimal period p of seq[onset:] via KMP; report it only if the tail holds >= min_reps
    repetitions (so any period up to len(tail)/min_reps is detected).  Returns (p, onset) or None."""
    onset = int(len(seq) * onset_frac)
    tail = seq[onset:]
    p = kmp_min_period(tail)
    if p * min_reps <= len(tail):
        return p, onset
    return None


def is_periodic(seq, Q):
    """Either detector fires."""
    a = eventual_period(seq, Q)
    b = strong_period(seq)
    return a, b


# ---------- drives ----------
def cstar(T):
    return [(row >> off) & 1 for t, row, off in lone_seed_rows(T)]


def periodic_drive(w, T, prefix=()):
    p = len(w)
    n0 = len(prefix)
    return list(prefix) + [w[(t - n0) % p] for t in range(n0, T + 2)]


def primitive_words(pmin, pmax, rng=None, max_per_period=None):
    out = []
    for p in range(pmin, pmax + 1):
        ws = []
        if max_per_period is None or (1 << p) <= 4 * max_per_period:
            cands = [list(b) for b in itertools.product((0, 1), repeat=p)]
        else:
            cands = [[rng.getrandbits(1) for _ in range(p)] for _ in range(4 * max_per_period)]
        for w in cands:
            if 1 not in w and p > 1:
                continue
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            ws.append(w)
        if max_per_period is not None:
            ws = ws[:max_per_period]
        out.extend(ws)
    return out


# =====================================================================================
def attack_a0():
    say("== A0: the (ND) boundary, literal hypothesis 'nonzero finite y' ==")
    T = 256
    hits = 0
    # y = delta_0 (the seed: nonzero, but zero on x <= -1, overridden at x = 0 by c_0); c = 0^omega
    c = [0] * (T + 2)
    rows = lhp_rows('30', 1, c, T)          # y_int = 1 means only bit 0, which is ignored (x = 0 is c_0)
    l = column(rows, 1)
    if all(v == 0 for v in l):
        hits += 1
        say("  y = delta_0 (zero on x <= -1), c = 0^omega: LHP identically zero, l = 0^omega is periodic. "
            "COUNTEREXAMPLE to the literal text; excluded by the proof's (ND).")
    say(f"ATTACK A0a literal-hypothesis degenerate case: hits={hits} (expected 1: this is the case PROOF.md "
        f"section 0 names and (ND) removes)")
    # every other drive with finitely many ones, seed y: must be aperiodic (ND holds since some c_t = 1)
    hits2 = 0
    T = 16384
    cs = cstar(T)
    fams = []
    for N in (1, 2, 3, 5, 8, 16, 64, 256, 1024):
        fams.append((f"c*[:{N}] 0^omega", cs[:N] + [0] * (T + 2 - N)))
    for k in (1, 2, 3, 7, 100):
        fams.append((f"1^{k} 0^omega", [1] * k + [0] * (T + 2 - k)))
    fams.append(("0^100 1 0^omega", [0] * 100 + [1] + [0] * (T + 1 - 100)))
    for name, c in fams:
        rows = lhp_rows('30', 0, c, T)
        l = column(rows, 1)
        a, b = is_periodic(l, 1024)
        v, t0 = edge_violations(rows)
        if a or b or v:
            hits2 += 1
            say(f"  HIT {name}: eventual_period={a} strong={b} edge_violations={v}")
        else:
            say(f"  ok  {name}: ones(l)={sum(l)} run={longest_run_np(l, 256)} edge_violations={v} t0={t0}")
    say(f"ATTACK A0b finitely-many-ones drives with seed y, T={T}: families={len(fams)} hits={hits2}")
    return hits2


# =====================================================================================
def attack_a1():
    say("== A1: (EDGE) at scale ==")
    rng = random.Random(1)
    T = 20000
    total = 0
    viol = 0
    for rule in ('30', '90'):
        drives = [("random", [rng.getrandbits(1) for _ in range(T + 2)]),
                  ("ones", [1] * (T + 2)),
                  ("zeros", [0] * (T + 2)),
                  ("(01)", periodic_drive([0, 1], T)),
                  ("(0001)", periodic_drive([0, 0, 0, 1], T)),
                  ("(0000000000000001)", periodic_drive([0] * 15 + [1], T))]
        for width in (1, 7, 64, 513, 2000):
            y = (rng.getrandbits(width) | (1 << (width - 1))) << 1     # top bit set so the support has min -width
            for name, c in drives:
                rows = lhp_rows(rule, y, c, T)
                v, t0 = edge_violations(rows)
                total += 1
                viol += v
                # explicit (EDGE) content: at t = T the edge is at -(width + T) with all cells below zero
                if rows[T].bit_length() - 1 != width + T:
                    viol += 1
    say(f"ATTACK A1 (EDGE), T={T}, widths (1,7,64,513,2000) x 6 drives x 2 rules: runs={total} violations={viol}")
    return viol


# =====================================================================================
def attack_a2():
    say("== A2: Theorem 1 in families outside the screen (T = 65536) ==")
    T = 65536
    Q = 2048
    rng = random.Random(2)
    cs = cstar(T)
    fams = []
    # (i) far-left seeds y = {-d}
    for d in (1, 10, 100, 1000):
        for wname, w in (("0", [0]), ("1", [1]), ("01", [0, 1]), ("011", [0, 1, 1]), ("0001", [0, 0, 0, 1])):
            fams.append((f"y={{-{d}}} c=({wname})^omega", 1 << d, periodic_drive(w, T)))
    # (ii) long-period random primitive words with the seed
    for p in (16, 32, 64, 128):
        for w in primitive_words(p, p, rng, max_per_period=3):
            c = periodic_drive(w, T)
            if c[0] == 0:
                c[0] = 1
            fams.append((f"seed, random primitive word p={p} ({''.join(map(str, w))[:16]}...)", 0, c))
    # (iii) long true-trace prefixes with periodic tails
    for N in (64, 256, 1024, 4096):
        for wname, w in (("0", [0]), ("1", [1]), ("01", [0, 1]), ("011", [0, 1, 1]), ("0011", [0, 0, 1, 1])):
            fams.append((f"seed, c*[:{N}] then ({wname})^omega", 0, periodic_drive(w, T, prefix=cs[:N])))
    # (iv) both: far-left seed plus true-trace prefix
    fams.append(("y={-37}, c*[:512] then (01)^omega", 1 << 37, periodic_drive([0, 1], T, prefix=cs[:512])))
    hits = 0
    runs = []
    for name, y, c in fams:
        rows = lhp_rows('30', y, c, T)
        l = column(rows, 1)
        a, b = is_periodic(l, Q)
        v, t0 = edge_violations(rows)
        run = longest_run_np(l, 256)
        runs.append(run)
        if a or b or v:
            hits += 1
            say(f"  HIT {name}: eventual_period={a} strong_period={b} edge_violations={v}")
        else:
            say(f"  ok  {name}: ones(l)={sum(l)} kmp_min_period(tail)={kmp_min_period(l[T // 2:])} "
                f"run={run} edge_violations={v}")
    say(f"ATTACK A2 Theorem 1 outside the screen, T={T}, Q={Q} plus KMP tail detector: families={len(fams)} "
        f"hits={hits}; longest shift-agreement run min/median/max={min(runs)}/{sorted(runs)[len(runs) // 2]}/"
        f"{max(runs)} (random null log2(T*256)={math.log2(T * 256):.1f})")
    return hits


# =====================================================================================
def attack_a3():
    say("== A3: Theorem 2 beyond the screened columns (columns -1..-256, T = 16384) ==")
    T = 16384
    K = 256
    cs = cstar(T)
    drives = [("seed (01)^omega", 0, periodic_drive([0, 1], T)),
              ("seed 1 0^omega", 0, [1] + [0] * (T + 1)),
              ("seed 1^omega", 0, [1] * (T + 2)),
              ("seed (011)^omega", 0, periodic_drive([0, 1, 1], T)),
              ("seed c*[:64] (0001)^omega", 0, periodic_drive([0, 0, 0, 1], T, prefix=cs[:64])),
              ("y={-5,-2} (0111)^omega", (1 << 5) | (1 << 2), periodic_drive([0, 1, 1, 1], T))]
    hits = 0
    for name, y, c in drives:
        rows = lhp_rows('30', y, c, T)
        per = []
        for k in range(1, K + 1):
            col = column(rows, k)
            a, b = is_periodic(col, 256)
            if a or b:
                per.append((k, a, b))
        if per:
            hits += len(per)
            say(f"  HIT {name}: periodic columns {per[:10]}")
        else:
            say(f"  ok  {name}: 0 of {K} columns eventually periodic (both detectors)")
    say(f"ATTACK A3 Theorem 2 columns -1..-{K}, T={T}: drives={len(drives)} periodic columns found={hits}")
    return hits


# =====================================================================================
def dfs_drive_for_target(y_int, target, T, budget=400_000):
    """Find c (c_0 free) with l_t = target(t) for all onset <= t <= T, smallest feasible onset < 12.
    Backtracking DFS over c_{t+1}; returns (c, onset, nodes) or None."""
    nodes = 0
    for onset in range(0, 12):
        for c0 in (1, 0):
            row0 = (y_int & ~1) | c0
            if row0 == 0:
                continue
            if onset <= 1 and ((step30(row0) >> 1) & 1) != target(1):
                continue
            if onset == 0 and ((row0 >> 1) & 1) != target(0):
                continue
            stack = [[row0, 0]]      # [row_t, next choice index]
            c = [c0]
            while stack:
                t = len(stack) - 1
                row, idx = stack[-1]
                if t == T:
                    return c, onset, nodes
                if idx >= 2:
                    stack.pop()
                    if t >= 1:
                        c.pop()
                    continue
                stack[-1][1] = idx + 1
                nodes += 1
                if nodes > budget:
                    return None
                cn = (1, 0)[idx]
                base = step30(row)
                nrow = (base & ~1) | cn
                if t + 2 <= T and t + 2 >= onset and ((step30(nrow) >> 1) & 1) != target(t + 2):
                    continue
                stack.append([nrow, 0])
                c.append(cn)
    return None


def attack_a4():
    say("== A4: Theorem 2 with non-periodic drives constructed to make column -1 periodic ==")
    T = 4096
    targets = [("0^omega", lambda t: 0),
               ("1^omega", lambda t: 1),
               ("(01)^omega", lambda t: t & 1),
               ("(0011)^omega", lambda t: (t >> 1) & 1),
               ("(011)^omega", lambda t: 0 if t % 3 == 0 else 1),
               ("(0001)^omega", lambda t: 1 if t % 4 == 3 else 0)]
    hits = 0
    found = 0
    for y_name, y in (("y={-1}", 1 << 1), ("seed", 0), ("y={-3,-1}", (1 << 3) | (1 << 1))):
        for tname, tgt in targets:
            res = dfs_drive_for_target(y, tgt, T)
            if res is None:
                say(f"  {y_name} target l={tname}: no drive found within budget (not a hit; DFS exhausted or budget)")
                continue
            c, onset, nodes = res
            found += 1
            c = c + [0]
            rows = lhp_rows('30', y, c, T)
            l = column(rows, 1)
            assert all(l[t] == tgt(t) for t in range(onset, T + 1)), "DFS output does not meet target"
            l2 = column(rows, 2)
            ca, cb = is_periodic(c[:T + 1], 512)
            m2a, m2b = is_periodic(l2, 512)
            v, t0 = edge_violations(rows)
            kc = kmp_min_period(c[T // 2:T + 1])
            k2 = kmp_min_period(l2[T // 2:])
            if ca or cb or m2a or m2b or v:
                hits += 1
                say(f"  HIT {y_name} target l={tname}: c periodic={ca}/{cb} col-2 periodic={m2a}/{m2b} edge={v}")
            else:
                say(f"  ok  {y_name} target l={tname} onset={onset} nodes={nodes}: l periodic by construction; "
                    f"c aperiodic (kmp tail period {kc}, ones {sum(c[:T + 1])}), column -2 aperiodic "
                    f"(kmp tail period {k2}, ones {sum(l2)}), edge violations {v}; c[:48]={''.join(map(str, c[:48]))}")
    say(f"ATTACK A4 Theorem 2 adversarial drives, T={T}: drives found={found} hits={hits}")
    return hits


# =====================================================================================
def attack_a5():
    say("== A5: exhaustive small-parameter search for Theorem 1's impossible configuration ==")
    T = 512
    Q = 64
    words = []
    for p in range(1, 7):
        for b in itertools.product((0, 1), repeat=p):
            w = list(b)
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)          # every rotation kept: phase matters for the onset
    runs = 0
    hits = 0
    for ybits in range(256):
        y = ybits << 1
        for w in words:
            c = periodic_drive(w, T)
            if y == 0 and 1 not in w:
                continue
            rows = lhp_rows('30', y, c, T)
            l = column(rows, 1)
            runs += 1
            a = eventual_period(l, Q)
            b = strong_period(l, min_reps=4)
            if a or b:
                hits += 1
                say(f"  HIT y={ybits:08b} w={''.join(map(str, w))}: {a} {b}")
    say(f"ATTACK A5 exhaustive y width<=8 x primitive drives period<=6 (all rotations), T={T}, Q={Q} and "
        f"KMP(tail, >=4 reps): runs={runs} hits={hits}")
    return hits


# =====================================================================================
def attack_a6():
    say("== A6: Lemma 7 on random periodic drives; Proposition B exhaustive at T = 16 ==")
    rng = random.Random(6)
    bad = 0
    checks = 0
    for _ in range(200):
        p = rng.randint(1, 12)
        w = [rng.getrandbits(1) for _ in range(p)]
        if 0 not in w:
            w[0] = 0
        tc = rng.randint(0, 20)
        pre = [rng.getrandbits(1) for _ in range(tc)]
        N = 2000
        c = pre + [w[(t - tc) % p] for t in range(tc, N)]
        Z = [t for t in range(N) if c[t] == 0]
        kp = sum(1 for z in Z if tc <= z < tc + p)
        k0 = next(i for i, z in enumerate(Z) if z >= tc)
        for k in range(k0, len(Z) - kp):
            if Z[k + kp] - p > N - p - 1:
                break
            checks += 1
            if Z[k + kp] != Z[k] + p:
                bad += 1
    say(f"ATTACK A6a Lemma 7 z_(k+k_p) = z_k + p on 200 random eventually periodic drives: checks={checks} "
        f"violations={bad}")
    T = 16
    cs = cstar(T + 1)
    n_rule = 0
    sols = []
    for bits in range(1 << T):
        c = [1] + [(bits >> k) & 1 for k in range(T)] + [0]
        # incremental early exit
        lrow = c[0]
        rrow = c[0]
        ok = True
        for t in range(T):
            l = (lrow >> 1) & 1
            r = (rrow >> 1) & 1
            if c[t + 1] != (l ^ (c[t] | r)):
                ok = False
                break
            lrow = (step30(lrow) & ~1) | c[t + 1]
            rrow = (((rrow << 1) ^ (rrow | (rrow >> 1))) & ~1) | c[t + 1]
        if ok:
            n_rule += 1
            sols.append(c[:T + 1])
    match = (len(sols) == 1 and sols[0] == cs[:T + 1])
    say(f"ATTACK A6b Proposition B exhaustive T={T}, all 2^{T} words with c_0=1: solutions={n_rule} "
        f"equal to c*[:{T + 1}]={match}")
    return bad + (0 if match else 1)


def main():
    say("attack_driven_lhp.py: adversarial compute checks on PROOF.md (lemma driven-lhp-column-minus-one-aperiodic)")
    total = 0
    for fn in (attack_a0, attack_a1, attack_a2, attack_a3, attack_a4, attack_a5, attack_a6):
        t0 = time.time()
        total += fn()
        say(f"  [{fn.__name__} {time.time() - t0:.1f}s]")
    say(f"FINAL: hits against PROOF.md claims (excluding the A0a degenerate case the proof itself excludes) = {total}; "
        f"[{time.time() - T_START:.1f}s]")


if __name__ == '__main__':
    main()
