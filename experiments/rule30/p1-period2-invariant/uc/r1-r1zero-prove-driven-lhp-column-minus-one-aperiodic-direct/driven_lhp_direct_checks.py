"""Finite checks backing PROOF.md for lemma driven-lhp-column-minus-one-aperiodic (direct proof).

Every check here is one of the finite exhaustive or gate items cited in PROOF.md.  Nothing here is
the proof; the proof is the written derivation.  The checks pin the three local identities the
derivation uses (exhaustively, over all argument tuples), gate the bigint kernel against an explicit
cell array, confirm the moving edge and the identification of the true left half-plane with the
driven one on a finite horizon, and confirm the Z-enumeration algebra of consequence (a).

Convention (this repo): s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
Mirrored rows: bit i of a row holds s(t,-i); bit 0 is c_t.
"""
import sys, random, itertools, time
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows, eventual_period

OUT = []
def log(s):
    OUT.append(s)
    print(s, flush=True)

def step30(row):
    return (row >> 1) ^ (row | (row << 1))

def step90(row):
    return (row >> 1) ^ (row << 1)

def lhp(y, c, T, step=step30):
    """Driven left half-plane.  y: mirrored initial row (bit 0 ignored, replaced by c[0]).
    Returns rows[0..T] as mirrored ints."""
    row = (y & ~1) | c[0]
    rows = [row]
    for t in range(T):
        row = (step(row) & ~1) | c[t + 1]
        rows.append(row)
    return rows

def lhp_reference(y_bits, c, T, rule):
    """Explicit cell-array reference: cells x in [-W, 0], W = T + len(y_bits) + 4 (edge never reaches -W)."""
    W = T + len(y_bits) + 4
    row = [0] * (W + 1)          # index i holds s(t, -i)
    for i, b in enumerate(y_bits):
        if i >= 1:
            row[i] = b
    row[0] = c[0]
    rows = []
    for t in range(T + 1):
        rows.append(list(row))
        new = [0] * (W + 1)
        for i in range(1, W):
            left, mid, right = row[i + 1], row[i], row[i - 1]   # x-1 = -(i+1), x = -i, x+1 = -(i-1)
            new[i] = left ^ (mid | right) if rule == 30 else left ^ right
        new[0] = c[t + 1]
        row = new
    return rows

# ----------------------------------------------------------------------------------------------
# CHECK 1: the rule at x = 0 with r free, exhaustive over (c_t, c_{t+1}, l_t) in {0,1}^3.
# Claim: some r_t in {0,1} satisfies c_{t+1} = l_t XOR (c_t OR r_t)  iff  (c_t = 0) or (l_t = 1 XOR c_{t+1});
#        when c_t = 0 the solution is unique, r_t = c_{t+1} XOR l_t; when c_t = 1 and the pin holds both r_t work.
def check1():
    bad = 0
    for ct, ct1, lt in itertools.product((0, 1), repeat=3):
        S = {rt for rt in (0, 1) if ct1 == lt ^ (ct | rt)}
        pin = (ct == 0) or (lt == 1 ^ ct1)
        if (len(S) > 0) != pin:
            bad += 1
        if ct == 0 and S != {ct1 ^ lt}:
            bad += 1
        if ct == 1 and pin and S != {0, 1}:
            bad += 1
    log(f"CHECK1 x=0 rule with r free: 8 tuples (c_t,c_t+1,l_t); solvable iff pin; unique r on c_t=0; failures={bad}")
    return bad == 0

# CHECK 2: inverse rule (left permutivity), exhaustive over the 8 neighbourhoods, rules 30 and 90.
def check2():
    bad = 0
    for a, b, d in itertools.product((0, 1), repeat=3):      # a = s(t,x-1), b = s(t,x), d = s(t,x+1)
        n30 = a ^ (b | d)
        if a != n30 ^ (b | d):
            bad += 1
        n90 = a ^ d
        if a != n90 ^ d:
            bad += 1
    log(f"CHECK2 inverse rule s(t,x-1) = s(t+1,x) XOR g(s(t,x),s(t,x+1)): 8 neighbourhoods x 2 rules, failures={bad}")
    return bad == 0

# CHECK 3: moving-edge step, exhaustive: neighbourhood (0,0,1) -> 1 and (0,0,0) -> 0, both rules.
def check3():
    bad = 0
    for rule in (30, 90):
        f = (lambda a, b, d: a ^ (b | d)) if rule == 30 else (lambda a, b, d: a ^ d)
        if f(0, 0, 1) != 1 or f(0, 0, 0) != 0:
            bad += 1
    log(f"CHECK3 moving-edge step: (0,0,1)->1 and (0,0,0)->0 for rules 30 and 90, failures={bad}")
    return bad == 0

# CHECK 4: bigint kernel vs explicit cell array, random (y, c), both rules.
def check4(seed=1, pairs=60, T=40):
    rng = random.Random(seed)
    bad = cells = 0
    for k in range(pairs):
        rule = 30 if k % 2 == 0 else 90
        step = step30 if rule == 30 else step90
        width = rng.randint(0, 12)
        y_bits = [0] + [rng.getrandbits(1) for _ in range(width)]
        y = sum(b << i for i, b in enumerate(y_bits))
        c = [rng.getrandbits(1) for _ in range(T + 2)]
        rows = lhp(y, c, T, step)
        ref = lhp_reference(y_bits, c, T, rule)
        for t in range(T + 1):
            for i in range(len(ref[t])):
                cells += 1
                if ((rows[t] >> i) & 1) != ref[t][i]:
                    bad += 1
    log(f"CHECK4 kernel vs cell-array reference: {pairs} random (y,c) pairs, rules 30 and 90, T={T}, cells={cells}, mismatches={bad}")
    return bad == 0

# CHECK 5: the moving edge on a finite horizon.  For t >= t0: s(t, a-(t-t0)) = 1 and s(t,x) = 0 for x < a-(t-t0),
# where (a, t0) = (leftmost 1 of y on x <= -1, 0) if y has one, else (0, first t with c_t = 1).
# Mirrored: row.bit_length() - 1 == m0 + (t - t0) with m0 = -a.  Before t0 in the y = 0 case: row == 0.
def check5(seed=2, drives=40, T=600):
    rng = random.Random(seed)
    bad = checked = 0
    for k in range(drives):
        step = step30 if k % 2 == 0 else step90
        if k % 4 < 2:
            width = rng.randint(1, 30)
            y = (rng.getrandbits(width) | (1 << (width - 1))) << 1      # nonzero on x <= -1, leftmost 1 at x = -width
            m0, t0 = width, 0
            c = [rng.getrandbits(1) for _ in range(T + 2)]
        else:
            y = 0
            t0 = rng.randint(0, 50)
            c = [0] * t0 + [1] + [rng.getrandbits(1) for _ in range(T + 2)]
            m0 = 0
        rows = lhp(y, c, T, step)
        for t in range(T + 1):
            checked += 1
            if t < t0:
                if rows[t] != 0:
                    bad += 1
            else:
                if rows[t].bit_length() - 1 != m0 + (t - t0):
                    bad += 1
    log(f"CHECK5 moving edge: {drives} drives (random y and y=0 cases, rules 30 and 90), T={T}, rows checked={checked}, violations={bad}")
    return bad == 0

# CHECK 6: the true lone-seed diagram restricted to x <= 0 equals LHP_seed(c*), all cells, t <= T.
def check6(T=3000):
    true_rows = []
    cstar = []
    off = None
    for t, row, o in lone_seed_rows(T):
        off = o
        low = row & ((1 << (off + 1)) - 1)
        s = format(low, f'0{off + 1}b')          # MSB first = x = 0 ... LSB = x = -off
        true_rows.append(int(s[::-1], 2))        # mirrored: bit i = s(t, -i)
        cstar.append((row >> off) & 1)
    cstar.append(0)                              # c[T+1] is never read for rows[0..T] except at the last step; pad
    driven = lhp(0, cstar, T, step30)
    bad = 0
    cells = 0
    for t in range(T + 1):
        cells += off + 1
        if driven[t] != true_rows[t]:
            bad += 1
    log(f"CHECK6 true lone-seed x<=0 half-plane vs LHP_seed(c*): T={T}, cells={cells}, row mismatches={bad}")
    return bad == 0

# CHECK 7: Z-enumeration algebra of consequence (a).  c = prefix + w^inf, p = |w|, k = zeros per period.
# (i) z_{i+k} = z_i + p for all i >= i0 (first index with z_i >= t0).
# (ii) if r|Z is q-periodic in the enumeration index from index i1, then l_t := c_{t+1} XOR (c_t OR r_t)
#      satisfies l_{t+qp} = l_t for all t >= max(t0, z_{i0}, z_{i1}).
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

def check7(seed=3, T=3000, pmax=6, reps=3):
    rng = random.Random(seed)
    bad_i = bad_ii = tests = 0
    for w in primitive_words(pmax):
        p = len(w)
        for _ in range(reps):
            t0 = rng.randint(0, 12)
            prefix = [rng.getrandbits(1) for _ in range(t0)]
            c = prefix + [w[(t - t0) % p] for t in range(t0, T + 2 * p + 2)]
            Z = [t for t in range(T + 1) if c[t] == 0]
            k = sum(1 for x in w if x == 0)
            i0 = next(i for i, z in enumerate(Z) if z >= t0)
            for i in range(i0, len(Z) - k):
                if Z[i + k] != Z[i] + p:
                    bad_i += 1
            q = rng.randint(1, 5)
            i1 = rng.randint(0, 20)
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
                    bad_ii += 1
            tests += 1
    log(f"CHECK7 Z-enumeration: {tests} drives (primitive words period<=6 with a 0 and a 1, random prefixes, T={T}); "
        f"z_(i+k)=z_i+p failures={bad_i}; r|Z q-periodic => l (qp)-periodic from max(t0,z_i0,z_i1) failures={bad_ii}")
    return bad_i == 0 and bad_ii == 0

# CHECK 8: the degenerate case and the single-one drive.
def check8(T=4096, Q=64):
    c0 = [0] * (T + 2)
    rows = lhp(0, c0, T, step30)
    l0 = [(r >> 1) & 1 for r in rows]
    z = all(r == 0 for r in rows)
    c1 = [1] + [0] * (T + 1)
    rows = lhp(0, c1, T, step30)
    l1 = [(r >> 1) & 1 for r in rows]
    edge_ok = all(rows[t].bit_length() - 1 == t for t in range(T + 1))
    ep = eventual_period(l1, Q)
    log(f"CHECK8 degenerate y=0, c=0^inf: half-plane identically zero={z}, l=0^inf periodic (hypothesis (N) is needed)")
    log(f"CHECK8 single-one drive y=0, c=1 0^inf: moving edge holds to T={T}: {edge_ok}; l eventual_period(q<={Q}, onset<=T/2)={ep}; ones(l)={sum(l1)}")
    return z and edge_ok and ep is None

def main():
    t0 = time.time()
    ok = all([check1(), check2(), check3(), check4(), check5(), check6(), check7(), check8()])
    log(f"ALL CHECKS PASS={ok} elapsed={time.time() - t0:.1f}s")
    with open('/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct/driven_lhp_direct_checks.log', 'w') as f:
        f.write("\n".join(OUT) + "\n")

if __name__ == '__main__':
    main()
