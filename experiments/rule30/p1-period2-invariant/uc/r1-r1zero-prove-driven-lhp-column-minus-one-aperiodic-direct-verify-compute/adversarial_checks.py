"""Adversarial compute checks for the proof of lemma driven-lhp-column-minus-one-aperiodic.

Written by the verify-compute agent, 2026-09-03.  Independent of driven_lhp_direct_checks.py:
its own kernels (full-line bigint Rule 30, mirrored driven LHP, explicit numpy period search),
gated against each other and against known Rule 30 rows before anything else is trusted.

Parts
  P0  orientation: the bigint kernels reproduce the standard Rule 30 rows and OEIS A051023 prefix.
  P1  period detector gate: planted periods are found, random tails are not.
  P2  Lemma B with REAL periodic columns: driven cylinders (column 0 overwritten by an eventually
      periodic drive, wrap at width L) and plain cylinders.  Claim under test: columns 0 and -1
      periodic (p from t0', q from t1) force every column pq-periodic from max(t0', t1).
  P3  the theorem on structured families the screen did not cover: c = 0^omega with nonzero y,
      single ones far to the left, wide blocks, long zero prefixes, periods 9..12, T = 2^16, Q = 4096.
  P4  (a1) gate to T = 16384 with independent kernels, every cell x in [-T, 0].
  P5  (a5), (a6) and the D4 equivalence (time-index period a multiple of p <=> enumeration period)
      on synthetic r, primitive words to period 10.
  P6  Rule 90 versions of P3 (the proof claims the theorem verbatim for Rule 90).

Convention: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).  Mirrored LHP rows: bit i = s(t,-i).
"""
import sys, random, itertools, time, math
import numpy as np

OUT = []
LOGPATH = ('/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/'
           'r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct-verify-compute/adversarial_checks.log')

def log(s):
    OUT.append(s)
    print(s, flush=True)

# ------------------------------------------------------------------ kernels (independent)
def full_step30(row):            # bit i = s(t, i - off); larger bit = larger x
    return (row << 1) ^ (row | (row >> 1))

def full_step90(row):
    return (row << 1) ^ (row >> 1)

def mir_step30(row):             # bit i = s(t, -i)
    return (row >> 1) ^ (row | (row << 1))

def mir_step90(row):
    return (row >> 1) ^ (row << 1)

def driven_lhp_cols(y, c, T, ncols, step=mir_step30):
    """y: mirrored int (bit 0 ignored). c: sequence length >= T+2. Returns (cols[k][t] = s(t,-k), edge violations)."""
    row = (y & ~1) | c[0]
    if row:
        m0, t0 = row.bit_length() - 1, 0
    else:
        t0 = next(t for t in range(T + 1) if c[t] == 1)
        m0 = 0
    mask = (1 << ncols) - 1
    packed = np.empty(T + 1, dtype=np.int64)
    ev = 0
    for t in range(T + 1):
        packed[t] = row & mask
        if t >= t0 and row.bit_length() != m0 + (t - t0) + 1:
            ev += 1
        elif t < t0 and row != 0:
            ev += 1
        row = (step(row) & ~1) | c[t + 1]
    return [((packed >> k) & 1).astype(np.int8) for k in range(ncols)], ev

def periodic_tail_stats(seq, Q):
    """For q = 1..Q: last index i with seq[i] != seq[i+q] (or -1).  Returns
    (eventual period (q, onset) with onset <= len/2 and tail >= 4q, or None; longest periodic tail length, its q)."""
    n = len(seq)
    best_tail, best_q = 0, 0
    ep = None
    for q in range(1, Q + 1):
        d = np.flatnonzero(seq[:n - q] != seq[q:])
        onset = int(d[-1]) + 1 if len(d) else 0
        tail = n - onset
        if tail > best_tail:
            best_tail, best_q = tail, q
        if ep is None and onset <= n // 2 and tail >= 4 * q:
            ep = (q, onset)
    return ep, best_tail, best_q

# ------------------------------------------------------------------ P0 orientation
def p0():
    std = ['1', '111', '11001', '1101111', '110010001', '11011110111']
    off = 8
    row = 1 << off
    bad = 0
    for t in range(6):
        w = 2 * t + 1
        low = (row >> (off - t)) & ((1 << w) - 1)
        s = format(low, f'0{w}b')[::-1]      # char j = x = -t + j
        if s != std[t]:
            bad += 1
            log(f"  P0 row {t}: got {s} expected {std[t]}")
        row = full_step30(row)
    a051023 = [int(ch) for ch in '1101110011000101100100111010111001110101']  # OEIS A051023 first 40 terms; t=0..5 agree with the hand-derived standard rows above (memory of the prefix was wrong at t=5 in the first draft, corrected)
    off = 64
    row = 1 << off
    got = []
    for t in range(40):
        got.append((row >> off) & 1)
        row = full_step30(row)
    match = got == a051023
    log(f"P0 orientation: standard rows 0..5 mismatches={bad}; centre column first 40 == OEIS A051023 prefix: {match}")
    return bad == 0 and match

# ------------------------------------------------------------------ P1 detector gate
def p1(seed=11, trials=400):
    rng = random.Random(seed)
    bad = 0
    for k in range(trials):
        n = rng.randint(200, 2000)
        seq = np.array([rng.getrandbits(1) for _ in range(n)], dtype=np.int8)
        if k % 2 == 0:
            q = rng.randint(1, 40)
            onset = rng.randint(0, n // 3)
            for i in range(onset + q, n):
                seq[i] = seq[i - q]
            ep, tail, bq = periodic_tail_stats(seq, 64)
            if ep is None or (n - ep[1]) < (n - onset) or ep[0] > q:
                bad += 1
        else:
            ep, tail, bq = periodic_tail_stats(seq, 64)
            if ep is not None:
                bad += 1
    log(f"P1 detector gate: {trials} sequences ({trials//2} planted periods q<=40, {trials//2} random); failures={bad}")
    return bad == 0

# ------------------------------------------------------------------ P2 Lemma B with real periodic columns
def min_period_onset(col):
    """Exact minimal eventual period and onset of a finite sequence.  Trusted only when the onset is in the
    first half and at least 4 periods agree at the end (same acceptance as r1zero_lib.eventual_period)."""
    n = len(col)
    for p in range(1, n // 8 + 1):
        d = np.flatnonzero(col[:n - p] != col[p:])
        onset = int(d[-1]) + 1 if len(d) else 0
        if onset <= n // 2 and n - onset >= 4 * p:
            return p, onset
    return None

def cylinder_run(L, init, drive, T, step_rule=30):
    """Rule 30 on Z/L (numpy).  If drive is not None, column 0 is overwritten by drive[t] at every t.
    Returns array S[t][x], x = 0..L-1 (x = -k is index L-k)."""
    S = np.zeros((T + 1, L), dtype=np.int8)
    row = np.array(init, dtype=np.int8)
    if drive is not None:
        row[0] = drive[0]
    for t in range(T + 1):
        S[t] = row
        a = np.roll(row, 1); d = np.roll(row, -1)
        row = (a ^ (row | d)) if step_rule == 30 else (a ^ d)
        if drive is not None:
            row[0] = drive[t + 1]
    return S

def p2(seed=5, T=24000):
    rng = random.Random(seed)
    tests = fails = skipped = nofit = lcm_only = 0
    detail = []
    for L in range(3, 15):
        for rep in range(8):
            init = [rng.getrandbits(1) for _ in range(L)]
            if rep % 2 == 0:
                pl = rng.randint(0, 6)
                pw = rng.randint(1, 5)
                w = [rng.getrandbits(1) for _ in range(pw)]
                drive = [rng.getrandbits(1) for _ in range(pl)] + [w[(t - pl) % pw] for t in range(pl, T + 2)]
                S = cylinder_run(L, init, drive, T)
                kind = f"driven L={L} prefix={pl} word={''.join(map(str,w))}"
            else:
                S = cylinder_run(L, init, None, T)
                kind = f"plain L={L}"
            r0 = min_period_onset(S[:, 0])
            r1 = min_period_onset(S[:, L - 1])
            if r0 is None or r1 is None:
                skipped += 1
                continue
            p, t0p = r0
            q, t1 = r1
            Tb = max(t0p, t1)
            P = p * q
            if Tb + 3 * P > T:
                P = p * q // math.gcd(p, q)
                if Tb + 3 * P > T:
                    nofit += 1
                    continue
                lcm_only += 1
            ok = True
            for x in range(L):
                col = S[:, x]
                if not np.array_equal(col[Tb:T + 1 - P], col[Tb + P:T + 1]):
                    ok = False
            tests += 1
            if not ok:
                fails += 1
                detail.append(f"  P2 FAIL {kind} p={p} t0'={t0p} q={q} t1={t1} P={P}")
    for d in detail[:10]:
        log(d)
    log(f"P2 Lemma B on cylinders (driven and plain, L=3..14, T={T}): {tests} configurations with columns 0 and -1 "
        f"eventually periodic (onset <= T/2, >= 4 periods); every column P-periodic from max(t0',t1) failures={fails} "
        f"(P = pq in {tests - lcm_only}, P = lcm(p,q) in {lcm_only} where pq did not fit the horizon); "
        f"skipped: no trusted period={skipped}, no fit={nofit}")
    return fails == 0

# ------------------------------------------------------------------ P3 / P6 theorem on structured families
def drive_from(prefix, w, T, force_c0=None):
    pl = len(prefix)
    c = list(prefix) + [w[(t - pl) % len(w)] for t in range(pl, T + 2)]
    if force_c0 is not None:
        c[0] = force_c0
    return c

def family(step, tag, T=1 << 16, Q=4096):
    rng = random.Random(2026 + (30 if step is mir_step30 else 90))
    cases = []
    # c = 0^omega with nonzero y
    for k in (1, 2, 3, 5, 8, 21, 100):
        cases.append((f"y=1@x=-{k}, c=0^w", 1 << k, [0] * (T + 2)))
    for W in (2, 5, 16, 33, 64):
        cases.append((f"y=1^{W}@[-{W},-1], c=0^w", ((1 << W) - 1) << 1, [0] * (T + 2)))
    yr = sum(rng.getrandbits(1) << i for i in range(1, 41)) | (1 << 40)
    cases.append((f"y=random width 40, c=0^w", yr, [0] * (T + 2)))
    # y = 0, long zero prefix then a single 1 then periodic; and single one at time m only
    for m in (0, 7, 100, 1000):
        cases.append((f"y=0, c=0^{m} 1 0^w", 0, [0] * m + [1] + [0] * (T + 2)))
        cases.append((f"y=0, c=0^{m} 1 (01)^w", 0, [0] * m + [1] + [(t % 2) for t in range(T + 2)]))
        cases.append((f"y=0, c=0^{m} 1 (0111)^w", 0, [0] * m + [1] + [[0,1,1,1][t % 4] for t in range(T + 2)]))
    # y far left with periodic c starting at 0 (c_0 may be 0)
    cases.append(("y=1@x=-200, c=(01)^w", 1 << 200, [t % 2 for t in range(T + 2)]))
    cases.append(("y=1@x=-200, c=(10)^w", 1 << 200, [(t + 1) % 2 for t in range(T + 2)]))
    cases.append(("y=1^64, c=(001)^w", ((1 << 64) - 1) << 1, [[0,0,1][t % 3] for t in range(T + 2)]))
    cases.append(("y=1^64, c=1^w", ((1 << 64) - 1) << 1, [1] * (T + 2)))
    cases.append(("y=0, c=1^w", 0, [1] * (T + 2)))
    # periods 9..12: random primitive words, y = 0, c_0 forced 1
    for p in (9, 10, 11, 12):
        for rep in range(6):
            while True:
                w = [rng.getrandbits(1) for _ in range(p)]
                if 0 in w and 1 in w and not any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                    break
            cases.append((f"y=0, c=1 then {''.join(map(str,w))}^w (p={p})", 0, drive_from([], w, T, force_c0=1)))
    # random y plus period 9..12
    for p in (9, 12):
        for rep in range(3):
            w = [rng.getrandbits(1) for _ in range(p)]
            if 1 not in w:
                w[0] = 1
            width = rng.randint(2, 30)
            y = (rng.getrandbits(width) | (1 << (width - 1))) << 1
            cases.append((f"y=random width {width}, c={''.join(map(str,w))}^w (p={p})", y, drive_from([], w, T)))
    hits = evtot = 0
    tails = []
    wall = time.time()
    for label, y, c in cases:
        cols, ev = driven_lhp_cols(y, c, T, 2, step)
        l = cols[1]
        ep, tail, bq = periodic_tail_stats(l, Q)
        hits += ep is not None
        evtot += ev
        tails.append(tail)
        log(f"  {tag} {label}: T={T} Q={Q} ones(l)={int(l.sum())} l eventual_period={ep} longest periodic tail={tail} at q={bq} edge violations={ev}")
    log(f"{tag} SUMMARY ({'rule 30' if step is mir_step30 else 'rule 90'}): {len(cases)} structured drives, T={T}, Q={Q}: "
        f"l eventually periodic in {hits}/{len(cases)}; moving-edge violations {evtot}; "
        f"longest periodic tail min/median/max = {min(tails)}/{sorted(tails)[len(tails)//2]}/{max(tails)} "
        f"(random null about log2(T*Q) = {math.log2(T*Q):.1f}) [{time.time()-wall:.0f}s]")
    return hits == 0 and evtot == 0

def p3():
    return family(mir_step30, "P3")

def p6():
    return family(mir_step90, "P6")

# ------------------------------------------------------------------ P4 (a1) gate, independent kernels
def p4(T=16384):
    off = T + 2
    row = 1 << off
    cstar = []
    true_left = []                      # ints with bit (off - j) = s(t, -j), j = 0..off (the low off+1 bits of the full row)
    mask = (1 << (off + 1)) - 1
    for t in range(T + 1):
        cstar.append((row >> off) & 1)
        true_left.append(row & mask)     # bit i = x = i - off, i = 0..off
        row = full_step30(row)
    # driven LHP with y = 0, c = cstar; convert its mirrored rows to the same "bit (off - j) = x -j" layout
    cpad = cstar + [0]
    rowm = cpad[0]
    bad = 0
    cells = 0
    for t in range(T + 1):
        s = format(rowm & mask, f'0{off + 1}b')     # MSB = bit off = x -off ... LSB = bit 0 = x 0
        conv = int(s[::-1], 2)                        # now bit off = x 0, bit 0 = x -off
        cells += off + 1
        if conv != true_left[t]:
            bad += 1
        rowm = (mir_step30(rowm) & ~1) | cpad[t + 1]
    log(f"P4 (a1) gate with independent kernels: T={T}, cells={cells}, row mismatches={bad}")
    return bad == 0

# ------------------------------------------------------------------ P5 (a5), (a6), D4 equivalence
def primitive_words(pmax):
    words = []
    for p in range(1, pmax + 1):
        for bits in itertools.product((0, 1), repeat=p):
            w = list(bits)
            if 0 not in w or 1 not in w:
                continue
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)
    return words

def p5(seed=17, T=5000, pmax=10, reps=2):
    rng = random.Random(seed)
    bad_a5 = bad_a6 = bad_d4 = tests = 0
    for w in primitive_words(pmax):
        p = len(w)
        for _ in range(reps):
            t0 = rng.randint(0, 15)
            c = [rng.getrandbits(1) for _ in range(t0)] + [w[(t - t0) % p] for t in range(t0, T + 3 * p + 2)]
            Z = [t for t in range(T + 1) if c[t] == 0]
            k = sum(1 for x in w if x == 0)
            i0 = next(i for i, z in enumerate(Z) if z >= t0)
            for i in range(i0, len(Z) - k):
                if Z[i + k] != Z[i] + p:
                    bad_a5 += 1
            # (a6): enumeration-periodic r|Z from index i1 with period q  =>  l (qp)-periodic from max(t0, z_i0, z_i1)
            q = rng.randint(1, 6)
            i1 = rng.randint(0, 25)
            pat = [rng.getrandbits(1) for _ in range(q)]
            r = [rng.getrandbits(1) for _ in range(T + 1)]
            for i, z in enumerate(Z):
                if i >= i1:
                    r[z] = pat[(i - i1) % q]
            l = [c[t + 1] ^ (c[t] | r[t]) for t in range(T + 1)]
            Tpp = max(t0, Z[i0], Z[min(i1, len(Z) - 1)])
            P = q * p
            for t in range(Tpp, T + 1 - P):
                if l[t + P] != l[t]:
                    bad_a6 += 1
            # D4 equivalence.  (i) enumeration period q from i1 => time-index period qp on Z from z_{max(i0,i1)}
            T1 = Z[max(i0, min(i1, len(Z) - 1))]
            for t in Z:
                if t >= T1 and t + P <= T:
                    if c[t + P] != 0 or r[t + P] != r[t]:
                        bad_d4 += 1
            # (ii) time-index period m*p on Z from some T1' => enumeration period m*k from the matching index
            m = rng.randint(1, 4)
            Tq = rng.randint(t0, t0 + 3 * p)
            r2 = [rng.getrandbits(1) for _ in range(T + 1)]
            for t in range(Tq, T + 1 - m * p):
                if c[t] == 0:
                    r2[t + m * p] = r2[t]
            j0 = next(i for i, z in enumerate(Z) if z >= Tq)
            for i in range(j0, len(Z) - m * k):
                if Z[i + m * k] > T:
                    break
                if r2[Z[i + m * k]] != r2[Z[i]]:
                    bad_d4 += 1
            tests += 1
    log(f"P5 (a5)/(a6)/D4 on synthetic r: {tests} drives (primitive words period<=10, random prefixes, T={T}); "
        f"z_(i+k)=z_i+p failures={bad_a5}; enumeration-periodic r|Z => l (qp)-periodic failures={bad_a6}; "
        f"D4 equivalence (both directions) failures={bad_d4}")
    return bad_a5 == 0 and bad_a6 == 0 and bad_d4 == 0

def main():
    wall = time.time()
    results = {}
    for name, fn in (("P0", p0), ("P1", p1), ("P2", p2), ("P4", p4), ("P5", p5), ("P3", p3), ("P6", p6)):
        t = time.time()
        results[name] = fn()
        log(f"{name} done ok={results[name]} [{time.time()-t:.1f}s]")
    log(f"ALL ADVERSARIAL CHECKS PASS={all(results.values())} {results} elapsed={time.time()-wall:.0f}s")
    with open(LOGPATH, 'w') as f:
        f.write("\n".join(OUT) + "\n")

if __name__ == '__main__':
    main()
