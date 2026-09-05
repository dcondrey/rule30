"""Independent checks for the logic verification of PROOF.md (driven-lhp-column-minus-one-aperiodic, direct).

Written by the verify-logic arm.  Nothing here is the proof.  The checks are:
  V1  exhaustive I1, I2, I3 (independent code, no import from the proof directory);
  V2  independent cell-array simulation of LHP_y(c) (dict-based, no bitmask), Lemma A moving edge on
      random drives in both cases of the definition of (a, t0);
  V3  independent (a1) gate: full lone-seed diagram restricted to x <= 0 versus LHP_0(c*) to T = 400;
  V4  counterexample search for the theorem: all y supported in x in [-6,-1] (including y = 0), all
      c = prefix + w^omega with primitive w of period 1..5 and prefix length 0..2, hypothesis (N)
      enforced, T = 2048; l = LHP_y(c)(.,-1) tested for an eventual period q <= 256 with onset <= T/2
      under the strict definition (agreement at every i >= onset).  A hit contradicts the proof.
  V5  the (N)-failing case y = 0, c = 0^omega gives l = 0^omega (Correction 1 is necessary);
  V6  D4 versus time-index reading: for random periodic c and random r, "r|Z eventually periodic in the
      enumeration index" and "r_{t+mp} = r_t for all large t in Z, some m >= 1" agree on every sample.
Convention: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
"""
import itertools, random, sys, time

OUT = []
def log(s):
    OUT.append(s); print(s, flush=True)

def f30(a, b, d):
    return a ^ (b | d)

# ---------------- V1: the three local identities, exhaustively ----------------
def v1():
    bad = 0
    for a, b, d in itertools.product((0, 1), repeat=3):
        if a != (f30(a, b, d) ^ (b | d)):          # I1
            bad += 1
    if f30(0, 0, 1) != 1 or f30(0, 0, 0) != 0:     # I2
        bad += 1
    for ct, ct1, lt in itertools.product((0, 1), repeat=3):   # I3
        sols = [r for r in (0, 1) if ct1 == (lt ^ (ct | r))]
        pin = (ct == 0) or (lt == (1 ^ ct1))
        if (len(sols) > 0) != pin: bad += 1
        if ct == 0 and sols != [ct1 ^ lt]: bad += 1
        if ct == 1 and pin and sols != [0, 1]: bad += 1
    log(f"V1 I1/I2/I3 exhaustive over all argument tuples: failures={bad}")
    return bad == 0

# ---------------- independent cell-array LHP ----------------
def lhp_cells(y, c, T):
    """y: dict x -> bit for x <= -1 (finite support); c: list, len > T.  Returns list of dict rows over x in [-(T+W+2), 0]."""
    W = max([-x for x in y] + [0]) + 2
    lo = -(T + W + 2)
    row = {x: y.get(x, 0) for x in range(lo, 0)}
    row[0] = c[0]
    rows = [row]
    for t in range(T):
        new = {}
        for x in range(lo, 0):
            new[x] = f30(row.get(x - 1, 0), row[x], row[x + 1])
        new[0] = c[t + 1]
        rows.append(new)
        row = new
    return rows, lo

# ---------------- V2: Lemma A on random drives, both cases ----------------
def v2(seed=11, drives=24, T=200):
    rng = random.Random(seed)
    bad = rows_checked = 0
    for k in range(drives):
        if k % 2 == 0:
            width = rng.randint(1, 10)
            y = {-i: rng.getrandbits(1) for i in range(1, width + 1)}
            y[-width] = 1
            a, t0 = -width, 0
            c = [rng.getrandbits(1) for _ in range(T + 2)]
        else:
            y = {}
            t0 = rng.randint(0, 30)
            c = [0] * t0 + [1] + [rng.getrandbits(1) for _ in range(T + 2)]
            a = 0
        rows, lo = lhp_cells(y, c, T)
        for t in range(T + 1):
            rows_checked += 1
            r = rows[t]
            if t < t0:
                if any(r[x] for x in range(lo, 0)): bad += 1
                continue
            e = a - (t - t0)
            if r[e] != 1: bad += 1
            if any(r[x] for x in range(lo, e)): bad += 1
    log(f"V2 Lemma A (moving edge) on {drives} random drives, both cases of (a,t0), cell-array kernel, T={T}: rows checked={rows_checked}, violations={bad}")
    return bad == 0

# ---------------- V3: (a1) gate with an independent full-diagram simulation ----------------
def v3(T=400):
    lo, hi = -(T + 2), T + 2
    row = {x: 0 for x in range(lo, hi + 1)}; row[0] = 1
    full = [row]
    for t in range(T):
        new = {x: f30(row.get(x - 1, 0), row[x], row.get(x + 1, 0)) for x in range(lo, hi + 1)}
        full.append(new); row = new
    cstar = [full[t][0] for t in range(T + 1)] + [0]
    driven, dlo = lhp_cells({}, cstar, T)
    bad = cells = 0
    for t in range(T + 1):
        for x in range(max(lo, dlo), 1):
            cells += 1
            if full[t][x] != driven[t][x]: bad += 1
    log(f"V3 (a1) gate, independent cell-array lone seed vs LHP_0(c*): T={T}, cells={cells}, mismatches={bad}; c*_0={cstar[0]}")
    return bad == 0

# ---------------- V4: counterexample search for the theorem ----------------
def step30(row):
    return (row >> 1) ^ (row | (row << 1))

def lhp_bits(y, c, T):
    row = (y & ~1) | c[0]
    l = [(row >> 1) & 1]
    for t in range(T):
        row = (step30(row) & ~1) | c[t + 1]
        l.append((row >> 1) & 1)
    return l

def strict_eventual_period(seq, Q, onset_max):
    n = len(seq)
    for q in range(1, Q + 1):
        onset = 0
        for i in range(n - q - 1, -1, -1):
            if seq[i] != seq[i + q]:
                onset = i + 1; break
        if onset <= onset_max:
            return (q, onset)
    return None

def primitive_words(pmax):
    words = []
    for p in range(1, pmax + 1):
        for bits in itertools.product((0, 1), repeat=p):
            w = list(bits)
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)
    return words

def v4(T=2048, Q=256, ymax=6, pmax=5, prefmax=2):
    words = primitive_words(pmax)
    hits = drives = skipped = 0
    for y in range(0, 1 << ymax):           # bit i (i>=1) = y_{-i}; bit 0 unused
        y2 = y << 1
        for w in words:
            for plen in range(0, prefmax + 1):
                for pref in itertools.product((0, 1), repeat=plen):
                    c = list(pref) + [w[(t - plen) % len(w)] for t in range(plen, T + 2)]
                    if y2 == 0 and 1 not in c:
                        skipped += 1; continue          # (N) fails
                    drives += 1
                    l = lhp_bits(y2, c, T)
                    ep = strict_eventual_period(l, Q, T // 2)
                    if ep is not None:
                        hits += 1
                        log(f"V4 HIT y={y2:#x} w={''.join(map(str,w))} prefix={''.join(map(str,pref))} period,onset={ep}")
    log(f"V4 theorem counterexample search: y supported in [-{ymax},-1] ({1<<ymax} choices), primitive words period<=" 
        f"{pmax}, prefix len<={prefmax}, T={T}, Q={Q}, onset<=T/2: drives={drives}, (N)-failing skipped={skipped}, eventually periodic l found={hits}")
    return hits == 0

# ---------------- V5: (N) is necessary ----------------
def v5(T=512):
    l = lhp_bits(0, [0] * (T + 2), T)
    z = all(v == 0 for v in l)
    log(f"V5 y=0, c=0^omega: l identically zero to T={T}: {z} (so (N) is necessary; the lemma's literal text without (N) is false)")
    return z

# ---------------- V6: D4 versus time-index reading ----------------
def v6(seed=5, samples=400, T=600):
    rng = random.Random(seed)
    disagree = 0; n_enum = 0
    for _ in range(samples):
        p = rng.randint(1, 5)
        w = [rng.getrandbits(1) for _ in range(p)]
        if 0 not in w: w[rng.randrange(p)] = 0
        t0 = rng.randint(0, 8)
        c = [rng.getrandbits(1) for _ in range(t0)] + [w[(t - t0) % p] for t in range(t0, T + 1)]
        Z = [t for t in range(T + 1) if c[t] == 0]
        r = [rng.getrandbits(1) for _ in range(T + 1)]
        if rng.random() < 0.5:                       # make r|Z enumeration-periodic from some index
            q = rng.randint(1, 4); i1 = rng.randint(0, 10); pat = [rng.getrandbits(1) for _ in range(q)]
            for i, z in enumerate(Z):
                if i >= i1: r[z] = pat[(i - i1) % q]
        rZ = [r[z] for z in Z]
        enum_per = strict_eventual_period(rZ, 8, len(rZ) // 2) is not None
        # time-index reading with period a multiple of p: exists m <= 8 and onset <= T/2 with r_{t+mp} = r_t for all t in Z, t >= onset
        time_per = False
        for m in range(1, 9):
            P = m * p
            ok_from = None
            for t in range(T - P, -1, -1):
                if c[t] == 0 and r[t + P] != r[t]:
                    ok_from = t + 1; break
            if ok_from is None: ok_from = 0
            if ok_from <= T // 2:
                time_per = True; break
        n_enum += enum_per
        if enum_per != time_per: disagree += 1
    log(f"V6 D4 (enumeration) vs time-index (period multiple of p) reading of 'r|Z eventually periodic': {samples} samples, enumeration-periodic={n_enum}, disagreements={disagree}")
    return disagree == 0

def main():
    t = time.time()
    ok = all([v1(), v2(), v3(), v4(), v5(), v6()])
    log(f"ALL VERIFY-LOGIC CHECKS PASS={ok} elapsed={time.time()-t:.1f}s")
    with open('/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct-verify-logic/verify_logic_checks.log', 'w') as fh:
        fh.write("\n".join(OUT) + "\n")

if __name__ == '__main__':
    main()
