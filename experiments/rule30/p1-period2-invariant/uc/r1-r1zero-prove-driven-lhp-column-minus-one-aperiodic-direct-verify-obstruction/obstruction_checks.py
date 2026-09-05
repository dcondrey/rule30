"""Obstruction-lens checks for the proof of lemma driven-lhp-column-minus-one-aperiodic (direct).

Independent of the proof's own kernel: an explicit cell-list simulation of the driven left half-plane
(no bigint tricks), an independent eventual-period search, and a full-diagram Rule 90 transport.

V1  Theorem sanity on a small exhaustive family for Rules 30 and 90 (0 hits expected), with two
    controls that violate one hypothesis each and therefore SHOULD produce hits: Rule 60 (left
    permutive, but f(0,0,1) = 0 so no moving edge; I2 fails) and Rule 110 (moving edge, but not
    left permutive; I1 fails).  A control that fires shows the search can fire.
V2  Rule 90 transport of the theorem and of consequence (a) on the lone seed: c* eventually periodic,
    l* and r* equal [t = 2^j - 1], r*|Z (enumeration sense) not eventually periodic.  So the
    transported statements are true and R1^90 and P1^90 are both false, as (a7) predicts.
V3  Hypothesis sharpness: (i) y = 0, c = 0^omega gives l = 0^omega (literal 'nonzero finite y' on
    x <= -1 is not enough; (N) is needed); (ii) infinite-support y = ...0101 (a Rule 30 fixed point)
    with c = 0^omega gives l = 1^omega (finite support is load-bearing); (iii) y = 0, c = 1 0^omega
    (one 1 only) gives aperiodic l (the lemma's 'infinitely many ones' is not needed).
V4  Independent (a5)/(a6) check: z_(i+k) = z_i + p, and enumeration-periodic r on Z forces l
    (qp)-periodic through the x = 0 rule.
V5  Glue form (b4), informational: for the driven family, the glued x = 0 rule between LHP_0(c) and
    RHP_0(c) must fail somewhere for every eventually periodic c != c* tested; record the first
    failure time and whether it is a one-time (pin) or a zero-time (coupling).

Convention: s(t+1,x) = f(s(t,x-1), s(t,x), s(t,x+1)) with f30(a,b,d) = a XOR (b OR d).
"""
import itertools, sys, time

OUT = []
def log(s):
    OUT.append(s)
    print(s, flush=True)

RULES = {
    30: lambda a, b, d: a ^ (b | d),
    90: lambda a, b, d: a ^ d,
    60: lambda a, b, d: a ^ b,
    110: lambda a, b, d: (b ^ d ^ (b & d) ^ (a & b & d)),
}

def lhp_cells(y_bits, c, T, rule, ghost=0):
    """Explicit cell-list driven left half-plane on x in [-W, 0].
    y_bits[i] = s(0,-i) for i >= 1.  c[t] = s(t,0).  ghost = value of every cell x < -W at all times
    (0 for finite support; used for the infinite-support control).  Returns column lists
    col[x] for x in -1..-8 as dicts and the moving-edge violation count for the finite-support case."""
    f = RULES[rule]
    W = T + len(y_bits) + 4
    row = [ghost] * (W + 1)                    # index i holds s(t,-i)
    for i, b in enumerate(y_bits):
        if i >= 1:
            row[i] = b
    row[0] = c[0]
    cols = {x: [] for x in range(-8, 0)}
    for t in range(T + 1):
        for x in cols:
            cols[x].append(row[-x])
        new = [ghost] * (W + 1)
        for i in range(1, W):
            new[i] = f(row[i + 1], row[i], row[i - 1])
        new[0] = c[t + 1]
        row = new
    return cols

def eventual_period(seq, qmax, onset_frac=0.5):
    """Smallest q <= qmax such that seq[i] == seq[i+q] for all i >= onset with onset <= onset_frac*len."""
    n = len(seq)
    lim = int(onset_frac * n)
    for q in range(1, qmax + 1):
        onset = 0
        for i in range(n - q - 1, -1, -1):
            if seq[i] != seq[i + q]:
                onset = i + 1
                break
        if onset <= lim and n - onset >= 4 * q:
            return (q, onset)
    return None

def primitive_words(pmax):
    words = []
    for p in range(1, pmax + 1):
        for bits in itertools.product((0, 1), repeat=p):
            w = list(bits)
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            rots = [tuple(w[i:] + w[:i]) for i in range(p)]
            if tuple(w) != min(rots):
                continue
            words.append(w)
    return words

def drive(word, prefix, T):
    p = len(word)
    n0 = len(prefix)
    return list(prefix) + [word[(t - n0) % p] for t in range(n0, T + 3)]

# ------------------------------------------------------------------------------------------------
def v1(T=1024, Q=64):
    words = primitive_words(4)            # 1-letter words 0 and 1 included
    ys = []
    for width in range(0, 5):
        for bits in itertools.product((0, 1), repeat=width):
            ys.append([0] + list(bits))   # y_bits[0] unused; y on x = -1..-width
    prefixes = [[], [1], [1, 1], [1, 1, 0]]
    results = {}
    for rule in (30, 90, 60, 110):
        hits = tested = skipped = 0
        first_hit = None
        for w in words:
            for pre in prefixes:
                c = drive(w, pre, T)
                for y in ys:
                    N = any(y[1:]) or any(c[:T + 1])
                    if not N:
                        skipped += 1
                        continue
                    cols = lhp_cells(y, c, T, rule)
                    l = cols[-1]
                    tested += 1
                    ep = eventual_period(l, Q)
                    if ep is not None:
                        hits += 1
                        if first_hit is None:
                            first_hit = (''.join(map(str, w)), ''.join(map(str, pre)), ''.join(map(str, y[1:])), ep)
        results[rule] = (hits, tested)
        log(f"V1 rule {rule}: l eventually periodic (q<={Q}, onset<=T/2) in {hits}/{tested} drives with (N) "
            f"(T={T}; words period<=4, prefixes {len(prefixes)}, y width<=4; {skipped} drives without (N) skipped); "
            f"first hit={first_hit}")
    ok = results[30][0] == 0 and results[90][0] == 0 and results[60][0] > 0 and results[110][0] > 0
    log(f"V1 verdict: theorem holds on the family for rules 30 and 90; controls 60 (no edge step) and 110 "
        f"(not left permutive) fire; test can fire={ok}")
    return ok

# ------------------------------------------------------------------------------------------------
def full_columns(rule, T, xs):
    f = RULES[rule]
    W = T + 3
    row = [0] * (2 * W + 1)
    row[W] = 1
    cols = {x: [] for x in xs}
    for t in range(T + 1):
        for x in xs:
            cols[x].append(row[W + x])
        new = [0] * (2 * W + 1)
        for i in range(1, 2 * W):
            new[i] = f(row[i - 1], row[i], row[i + 1])
        row = new
    return cols

def v2(T=4096, Q=256):
    cols = full_columns(90, T, [-1, 0, 1])
    c, l, r = cols[0], cols[-1], cols[1]
    ep_c = eventual_period(c, Q)
    ep_l = eventual_period(l, Q)
    ep_r = eventual_period(r, Q)
    ones_l = [t for t in range(T + 1) if l[t]]
    ones_r = [t for t in range(T + 1) if r[t]]
    expect = [2 ** j - 1 for j in range(1, 40) if 2 ** j - 1 <= T]
    Z = [t for t in range(T + 1) if c[t] == 0]
    rZ = [r[t] for t in Z]
    ep_rZ = eventual_period(rZ, Q)
    # driven version of Rule 90 LHP with c = c*, compare to the full diagram (transport of (a1))
    cl = lhp_cells([0], c + [0, 0], T, 90)[-1]
    same = cl == l
    log(f"V2 rule 90 lone seed T={T}: c* eventual_period={ep_c} (1 0^omega); l* eventual_period={ep_l}; "
        f"r* eventual_period={ep_r}; ones(l*)==ones(r*)=={expect}: {ones_l == expect and ones_r == expect}; "
        f"|Z|={len(Z)}; r*|Z eventual_period={ep_rZ}; driven LHP_0(c*) column -1 equals true column -1: {same}")
    ok = ep_c is not None and ep_l is None and ep_r is None and ep_rZ is None and same and ones_l == expect
    log(f"V2 verdict: transported theorem and (a) are TRUE for Rule 90 (c* e.p., l* and r*|Z aperiodic); "
        f"R1^90 is false and P1^90 is false, both together, as (a7) says; nothing false is proved={ok}")
    return ok

# ------------------------------------------------------------------------------------------------
def v3(T=2048, Q=64):
    # (i) y = 0, c = 0^omega
    c0 = [0] * (T + 3)
    l_i = lhp_cells([0], c0, T, 30)[-1]
    zero_i = all(v == 0 for v in l_i)
    # (ii) infinite support ...0101 fixed point with c = 0^omega: s(0,-1)=1, s(0,-2)=0, ...; ghost pattern
    # the window is x in [-W,0]; cell -W-1 has value [W+1 odd]; we choose W parity to match the pattern.
    T2 = 256
    W = T2 + 8
    if (W + 1) % 2 == 0:
        W += 1
    y_inf = [0] + [(i % 2) for i in range(1, W + 1)]   # s(0,-i) = 1 for i odd
    # ghost for x < -W is s(0, -(W+1)) = [(W+1) odd] = 1
    f = RULES[30]
    row = [0] + y_inf[1:]
    row[0] = 0
    l_ii = []
    ok_fixed = True
    for t in range(T2 + 1):
        l_ii.append(row[1])
        new = [0] * (W + 1)
        for i in range(1, W):
            new[i] = f(row[i + 1], row[i], row[i - 1])
        new[W] = f(1, row[W], row[W - 1])
        new[0] = 0
        row = new
    one_ii = all(v == 1 for v in l_ii)
    # (iii) y = 0, c = 1 0^omega
    c1 = [1] + [0] * (T + 3)
    l_iii = lhp_cells([0], c1, T, 30)[-1]
    ep_iii = eventual_period(l_iii, Q)
    log(f"V3 (i) y=0 on x<=-1, c=0^omega, Rule 30, T={T}: l identically zero={zero_i} (literal lemma fails without (N))")
    log(f"V3 (ii) infinite-support y=...0101 (Rule 30 fixed point), c=0^omega, T={T2}: l identically one={one_ii} "
        f"(finite support of y is load-bearing; both c and l periodic)")
    log(f"V3 (iii) y=0, c=1 0^omega (a single 1), Rule 30, T={T}: l eventual_period(q<={Q})={ep_iii}, ones(l)={sum(l_iii)} "
        f"('infinitely many ones' is not needed)")
    ok = zero_i and one_ii and ep_iii is None
    return ok

# ------------------------------------------------------------------------------------------------
def v4(T=2000):
    import random
    rng = random.Random(7)
    bad5 = bad6 = tests = 0
    for w in primitive_words(5):
        if 0 not in w or 1 not in w:
            continue
        p = len(w)
        for rep in range(4):
            t0 = rng.randint(0, 10)
            pre = [rng.getrandbits(1) for _ in range(t0)]
            c = drive(w, pre, T)
            Z = [t for t in range(T + 1) if c[t] == 0]
            k = w.count(0)
            i0 = next(i for i, z in enumerate(Z) if z >= t0)
            for i in range(i0, len(Z) - k):
                if Z[i + k] != Z[i] + p:
                    bad5 += 1
            q = rng.randint(1, 4)
            i1 = rng.randint(0, 15)
            pat = [rng.getrandbits(1) for _ in range(q)]
            r = [rng.getrandbits(1) for _ in range(T + 1)]
            for i, z in enumerate(Z):
                if i >= i1:
                    r[z] = pat[(i - i1) % q]
            l = [c[t + 1] ^ (c[t] | r[t]) for t in range(T + 1)]
            start = max(t0, Z[i0], Z[min(i1, len(Z) - 1)])
            P = q * p
            for t in range(start, T + 1 - P):
                if l[t + P] != l[t]:
                    bad6 += 1
            tests += 1
    log(f"V4 (a5)/(a6) independent: {tests} drives (primitive words period<=5 with both letters), T={T}; "
        f"z_(i+k)=z_i+p failures={bad5}; r enumeration-q-periodic on Z => l (qp)-periodic failures={bad6}")
    return bad5 == 0 and bad6 == 0

# ------------------------------------------------------------------------------------------------
def rhp_cells(c, T, rule=30):
    f = RULES[rule]
    W = T + 4
    row = [0] * (W + 1)          # index i holds s(t, i)
    row[0] = c[0]
    col1 = []
    for t in range(T + 1):
        col1.append(row[1])
        new = [0] * (W + 1)
        for i in range(1, W):
            new[i] = f(row[i - 1], row[i], row[i + 1])
        new[0] = c[t + 1]
        row = new
    return col1

def v5(T=512):
    words = primitive_words(4)
    n_pin = n_couple = n_none = 0
    rows = []
    for w in words:
        for pre in ([], [1, 1, 0]):
            c = drive(w, pre, T)
            if c[0] == 0:
                c = [1] + c[1:]
            l = lhp_cells([0], c, T, 30)[-1]
            r = rhp_cells(c, T)
            first = None
            for t in range(T):
                if c[t + 1] != (l[t] ^ (c[t] | r[t])):
                    first = t
                    break
            if first is None:
                n_none += 1
                kind = 'NONE'
            elif c[first] == 1:
                n_pin += 1
                kind = 'pin(one-time)'
            else:
                n_couple += 1
                kind = 'coupling(zero-time)'
            rows.append(f"  word {''.join(map(str, w))} prefix {''.join(map(str, pre)) or '-'}: first glue failure t={first} {kind}")
    for s in rows:
        log(s)
    log(f"V5 glue (b4) on {len(rows)} eventually periodic drives with c_0=1, T={T}: first failure at a one-time (pin) "
        f"in {n_pin}, at a zero-time (coupling) in {n_couple}, no failure to T in {n_none}")
    return n_none == 0

def main():
    t = time.time()
    ok = all([v1(), v2(), v3(), v4(), v5()])
    log(f"ALL VERIFY CHECKS PASS={ok} elapsed={time.time() - t:.1f}s")
    with open(sys.argv[0].replace('.py', '.log'), 'w') as fh:
        fh.write("\n".join(OUT) + "\n")

if __name__ == '__main__':
    main()
